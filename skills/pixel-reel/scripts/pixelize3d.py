"""3D renders -> pixel-art sprite strips (the second half of the pre-rendered sprites pipeline).

  python pixelize3d.py RENDER_DIR DEST_DIR [--scale 4] [--depth-edge 0.35] [--shadow 0.9] [--lref P]

RENDER_DIR is what blender/pixel3d.py wrote (meta.json + <key>/f_NNNN.exr light + <key>/i_NNNN.exr id/depth). For every art pixel:
  1. majority vote of the ss x ss sub-pixels: object (which material) or empty;
  2. the material's light, normalised by a reference taken over ALL frames (no flicker), mapped to its palette
     ramp in toon bands (optional ordered dither at the band edges); emissive materials keep their brightest colour;
  3. a 1-px outline outside the silhouette and a darker line on the far side of depth steps (occluding contours);
  4. the shadow-catcher shadow becomes a separate dithered strip (<key>.shadow) meant for a multiply-blend actor.
Writes DEST_DIR/<key>.png (strip, frames side by side, x scale, nearest), merges DEST_DIR/atlas3d.json and saves
DEST_DIR/preview/<render name>.png (all frames, for review).
"""
import argparse, glob, json, os
import numpy as np
from PIL import Image

BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0
EDGES = {1: [], 2: [0.45], 3: [0.32, 0.72], 4: [0.28, 0.58, 0.9], 5: [0.22, 0.45, 0.7, 0.92]}


def hexrgb(h): return [int(h[i:i + 2], 16) for i in (1, 3, 5)]


def _rgba(path):
    import OpenEXR
    with OpenEXR.File(path, separate_channels=True) as f:
        ch = {k.split(".")[-1]: np.asarray(v.pixels, dtype=np.float32) for k, v in f.channels().items()}
    return ch["R"], ch["G"], ch["B"], ch["A"]


def read_exr(path):
    """f_NNNN.exr (light) + i_NNNN.exr (id, depth) -> luminance, light alpha, depth, material id"""
    r, g, b, a = _rgba(path)
    d, n = os.path.split(path)
    ir, ig, _, ia = _rgba(os.path.join(d, "i_" + n[2:]))
    mid = np.where(ia > 0.5, np.rint(ir * 64), 0).astype(int)
    a = np.where(mid > 0, np.maximum(a, ia), a)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b, a, ig * 200.0, mid


def downsample(L, A, Z, I, ss, nmat, emis=()):
    H, W = L.shape[0] // ss, L.shape[1] // ss
    blk = lambda x: x[:H * ss, :W * ss].reshape(H, ss, W, ss).transpose(0, 2, 1, 3).reshape(H, W, ss * ss)
    L, A, Z, I = blk(L), blk(A), blk(Z), blk(I)
    obj = (I > 0) & (A > 0.5)
    counts = np.stack([((I == m) & obj).sum(-1) * (3 if m in emis else 1) for m in range(1, nmat + 1)], -1)
    # (emissive bits - lights, LEDs - win the vote from a quarter of the pixel: they would vanish otherwise)
    mid = counts.argmax(-1) + 1; total = obj.sum(-1)
    isobj = (total * 2 >= ss * ss) | np.isin(mid, emis) & (counts.max(-1) >= ss * ss * 3 / 4)
    sel = (I == mid[..., None]) & obj
    with np.errstate(invalid="ignore", divide="ignore"):
        Lu = np.where(A > 1e-4, L / np.maximum(A, 1e-4), 0)                                 # un-premultiply
        light = (Lu * sel).sum(-1) / np.maximum(sel.sum(-1), 1)
    depth = np.where(obj, Z, np.inf).min(-1)
    shadow = (np.where((I == 0) & ~obj, A, 0)).sum(-1) / (ss * ss)
    return np.where(isobj, mid, 0), light, depth, shadow


def colourise(mid, light, depth, shadow, mats, lref, cfg, depth_edge, shadow_k):
    H, W = mid.shape
    out = np.zeros((H, W, 4), np.uint8); sh = np.zeros((H, W, 4), np.uint8)
    yy, xx = np.mgrid[0:H, 0:W]; bay = BAYER[yy % 4, xx % 4]
    Ln = np.clip(light / lref, 0, 1.2)
    for m in mats:
        msk = mid == m["id"]
        if not msk.any(): continue
        ramp = [hexrgb(c) for c in m["ramp"]]
        if m.get("emissive"):
            out[msk, :3] = ramp[-1]; out[msk, 3] = 255; continue
        edges = m.get("bands") or EDGES[len(ramp)]
        t = Ln + (bay - 0.5) * float(m.get("dither") or 0) * 0.2
        band = np.zeros((H, W), int)
        for e in edges: band += (t >= e)
        cols = np.array(ramp)[band]
        out[msk, :3] = cols[msk]; out[msk, 3] = 255
    objm = mid > 0
    # darker line on the far side of a depth step (occluding contour), not on emissive parts
    emis = np.isin(mid, [m["id"] for m in mats if m.get("emissive")])
    line = np.zeros((H, W), bool)
    for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        nb_obj = np.roll(objm, (dy, dx), (0, 1)); nb_d = np.roll(depth, (dy, dx), (0, 1))
        with np.errstate(invalid="ignore"): line |= objm & nb_obj & (depth - nb_d > depth_edge)
    line &= ~emis
    for m in mats:
        msk = line & (mid == m["id"])
        out[msk, :3] = hexrgb(m.get("line") or m["ramp"][0])
    # 1-px outline outside the silhouette
    pad = np.pad(objm, 1)
    ring = (pad[:-2, 1:-1] | pad[2:, 1:-1] | pad[1:-1, :-2] | pad[1:-1, 2:]) & ~objm
    out[ring, :3] = hexrgb(cfg["outline"]); out[ring, 3] = 255
    # cast shadow: separate strip, ordered dither
    dens = np.clip((shadow - 0.12) / 0.5, 0, 1) * shadow_k * 0.5      # ignore render noise; at most a 50% dither
    son = (dens > bay) & ~objm & ~ring
    sh[son, :3] = hexrgb(cfg["shadow"]); sh[son, 3] = 255
    return out, sh


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("render"); ap.add_argument("dest")
    ap.add_argument("--scale", type=int, default=4); ap.add_argument("--depth-edge", type=float, default=0.35)
    ap.add_argument("--shadow", type=float, default=0.9, help="shadow density multiplier (0 = no shadow strip)")
    ap.add_argument("--lref", type=float, help="light reference (default: 97th percentile over all frames)")
    a = ap.parse_args()
    meta = json.load(open(os.path.join(a.render, "meta.json"))); cfg = meta; ss = meta["ss"]; mats = meta["mats"]
    W, H = meta["cell"]; ax, ay = meta["anchor"]
    os.makedirs(os.path.join(a.dest, "preview"), exist_ok=True)
    data = {}
    for an in meta["anims"]:
        fr = sorted(glob.glob(os.path.join(a.render, an["key"], "f_*.exr")))[:an["frames"]]
        data[an["key"]] = [downsample(*read_exr(f), ss, len(mats), [m["id"] for m in mats if m.get("emissive")]) for f in fr]
    emis_ids = [m["id"] for m in mats if m.get("emissive")]
    allL = np.concatenate([l[(mid > 0) & ~np.isin(mid, emis_ids)] for v in data.values() for mid, l, _, _ in v] or [np.ones(1)])
    lref = a.lref or float(np.percentile(allL, 97)) or 1.0
    atlas_p = os.path.join(a.dest, "atlas3d.json")
    atlas = json.load(open(atlas_p)) if os.path.exists(atlas_p) else {}
    rows = []
    for an in meta["anims"]:
        frames = [colourise(*f, mats, lref, cfg, a.depth_edge, a.shadow) for f in data[an["key"]]]
        strip = np.concatenate([f[0] for f in frames], 1); shs = np.concatenate([f[1] for f in frames], 1)
        n = len(frames); key = an["key"]
        big = lambda arr: Image.fromarray(arr, "RGBA").resize((arr.shape[1] * a.scale, arr.shape[0] * a.scale), Image.NEAREST)
        big(strip).save(os.path.join(a.dest, key + ".png"), optimize=True)
        ent = dict(file="sprites/3d/" + key + ".png", frames=n, w=W, h=H, ax=ax, ay=ay, fps=an["fps"],
                   mode=an["mode"], mirror=an.get("mirror", False), source="3d")
        atlas[key] = ent
        if a.shadow > 0 and shs[..., 3].any():
            big(shs).save(os.path.join(a.dest, key + ".shadow.png"), optimize=True)
            atlas[key + ".shadow"] = dict(ent, file="sprites/3d/" + key + ".shadow.png")
        else:
            atlas.pop(key + ".shadow", None)
        rows.append((key, strip, shs))
    json.dump(atlas, open(atlas_p, "w"), indent=1)
    # preview: every animation on a row, over a warm floor colour, x scale
    bgc = np.array(hexrgb("#C98A2B") + [255], np.uint8)
    wmax = max(r[1].shape[1] for r in rows); prev = np.tile(bgc, (H * len(rows), wmax, 1))
    for k, (_, s, shs) in enumerate(rows):
        reg = prev[k * H:(k + 1) * H, :s.shape[1]]
        m = shs[..., 3] > 0; reg[m] = (reg[m] * 0.45).astype(np.uint8)
        m = s[..., 3] > 0; reg[m] = s[m]
    name = os.path.basename(os.path.normpath(a.render))
    Image.fromarray(prev, "RGBA").resize((wmax * a.scale, H * len(rows) * a.scale), Image.NEAREST).save(
        os.path.join(a.dest, "preview", name + ".png"))
    print("lref %.4f" % lref, "->", a.dest, [r[0] for r in rows])


if __name__ == "__main__":
    main()
