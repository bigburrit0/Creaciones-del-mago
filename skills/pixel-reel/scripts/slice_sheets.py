"""Turn approved image-model sheets into animation strips + atlas for pixel-reel.js.

  python3 slice_sheets.py LIBRARY/sprites.json SHEETS_DIR[:FALLBACK_DIR...] OUT_DIR [--reel reel.json] [--no-quantize]

SHEETS_DIR can list several folders separated by ':' (first match wins): approved sheets first, placeholders
after, so every real sheet replaces its placeholder as soon as it exists.

For every sheet of the plan that exists in SHEETS_DIR:
  1. key out the magenta background (and its anti-aliased fringe);
  2. find the art-pixel grid (block size from the format, phase found by minimum in-block variance)
     and rebuild the sprite at ART resolution, one colour per art pixel;
  3. snap colours to the project palette (unless --no-quantize);
  4. align the anchor: the median feet/base point of the sheet is moved to the format's anchor, so frames
     never jitter (jumps keep their height because one shift is applied to the whole sheet);
  5. write a horizontal strip per animation at x scale, atlas.json / atlas.js, review images and a report.
"""
import argparse, json, os, sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prmanifest as M


def bg_mask(a):
    r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    return (r > 150) & (b > 150) & (g < 120) & (np.abs(r - b) < 90)


def to_art(img, s, out_w, out_h):
    """img: RGB array whose art pixels are s x s blocks (any phase). Returns RGBA art array out_h x out_w."""
    a = np.asarray(img).astype(np.int16)
    best = None
    for py in range(s):
        for px in range(s):
            sub = a[py:py + out_h * s, px:px + out_w * s]
            if sub.shape[0] < (out_h - 1) * s or sub.shape[1] < (out_w - 1) * s: continue
            hh, ww = sub.shape[0] // s, sub.shape[1] // s
            blk = sub[:hh * s, :ww * s].reshape(hh, s, ww, s, 3)
            v = blk.var(axis=(1, 3)).mean()
            if best is None or v < best[0]: best = (v, px, py)
    _, px, py = best
    pad = np.zeros((out_h * s + s, out_w * s + s, 3), np.int16); pad[..., 0] = 255; pad[..., 2] = 255
    sub = a[py:py + out_h * s, px:px + out_w * s]; pad[:sub.shape[0], :sub.shape[1]] = sub
    blk = pad[:out_h * s, :out_w * s].reshape(out_h, s, out_w, s, 3).transpose(0, 2, 1, 3, 4).reshape(out_h, out_w, s * s, 3)
    # use the inner part of every block (its edges are where soft anti-aliasing lives)
    lo, hi = s // 4, s - s // 4
    inner = blk.reshape(out_h, out_w, s, s, 3)[:, :, lo:hi, lo:hi].reshape(out_h, out_w, -1, 3)
    inm = ~bg_mask(inner)
    alpha = inm.mean(axis=2) >= 0.5
    srt = np.where(inm[..., None], inner, 9999).astype(np.int32)
    srt.sort(axis=2)                      # background pushed to the end; take the median of the valid ones
    cnt = np.maximum(inm.sum(axis=2), 1)
    idx = (cnt - 1) // 2
    col = np.take_along_axis(srt, idx[:, :, None, None].repeat(3, axis=3), axis=2)[:, :, 0, :]
    col = np.clip(col, 0, 255).astype(np.uint8)
    out = np.zeros((out_h, out_w, 4), np.uint8); out[..., :3] = col; out[..., 3] = alpha * 255
    return out


def quantize(art, pal):
    if not pal: return art
    P = np.array([M.hex2rgb(h) for h in pal], np.int32)
    rgb = art[..., :3].astype(np.int32)
    d = ((rgb[:, :, None, :] - P[None, None]) ** 2).sum(-1)
    q = P[d.argmin(-1)].astype(np.uint8)
    out = art.copy(); out[..., :3] = np.where(art[..., 3:] > 0, q, 0); return out


def cell_metrics(c):
    al = c[..., 3] > 0
    if al.sum() < 6: return None
    ys, xs = np.where(al); base = ys.max()
    feet = al[max(0, base - 7):base + 1]; fx = np.where(feet)[1]
    return dict(base=int(base), cx=float(fx.mean()), top=int(ys.min()), left=int(xs.min()), right=int(xs.max()),
                touches=bool(al[0].any() or al[-1].any() or al[:, 0].any() or al[:, -1].any()), area=int(al.sum()),
                ccx=float(xs.mean()), ccy=float(ys.mean()))


def shift(c, dx, dy):
    out = np.zeros_like(c); h, w = c.shape[:2]
    ys, xs = slice(max(0, dy), min(h, h + dy)), slice(max(0, dx), min(w, w + dx))
    ys0, xs0 = slice(max(0, -dy), min(h, h - dy)), slice(max(0, -dx), min(w, w - dx))
    out[ys, xs] = c[ys0, xs0]; return out


def save_strip(frames, path, S):
    h, w = frames[0].shape[:2]
    strip = np.zeros((h, w * len(frames), 4), np.uint8)
    for i, f in enumerate(frames): strip[:, i * w:(i + 1) * w] = f
    im = Image.fromarray(strip, "RGBA")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.resize((im.width * S, im.height * S), Image.NEAREST).save(path, optimize=True)
    return im


def review(frames, anchor, path, title_dots=0):
    h, w = frames[0].shape[:2]; z = 3
    sheet = Image.new("RGBA", ((w + 4) * (len(frames) + 1) * z, h * z), (60, 60, 70, 255))
    onion = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        im = Image.fromarray(f, "RGBA")
        bg = Image.new("RGBA", (w, h), (205, 205, 215, 255)); bg.alpha_composite(im)
        d = ImageDraw.Draw(bg); ax, ay = anchor
        d.line([(0, ay), (w, ay)], fill=(255, 0, 0, 255)); d.line([(ax, 0), (ax, h)], fill=(255, 0, 0, 160))
        sheet.paste(bg.resize((w * z, h * z), Image.NEAREST), (i * (w + 4) * z, 0))
        ghost = im.copy(); ghost.putalpha(Image.fromarray((f[..., 3] > 0).astype(np.uint8) * min(255, int(255 / max(1, len(frames)) + 40))))
        onion.alpha_composite(ghost)
    bg = Image.new("RGBA", (w, h), (205, 205, 215, 255)); bg.alpha_composite(onion)
    sheet.paste(bg.resize((w * z, h * z), Image.NEAREST), (len(frames) * (w + 4) * z, 0))
    os.makedirs(os.path.dirname(path), exist_ok=True); sheet.save(path)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("library"); ap.add_argument("sheets"); ap.add_argument("out")
    ap.add_argument("--reel"); ap.add_argument("--no-quantize", action="store_true")
    a = ap.parse_args(); lib, reel = M.load(a.library, a.reel)
    S = lib["grid"]["scale"]; pal = [] if a.no_quantize else M.palette(lib); chars = M.characters(lib, reel)
    atlas = {"scale": S, "sprites": {}, "plates": {}}; report = []; parts = {}
    for sh in [s for s in M.plan(lib, reel) if s["needed"]]:
        p = next((os.path.join(d, sh["name"]) for d in a.sheets.split(os.pathsep) if os.path.exists(os.path.join(d, sh["name"]))), None)
        if not p: report.append(f"- falta `{sh['name']}`"); continue
        src_tag = "" if p.startswith(a.sheets.split(os.pathsep)[0]) else " (provisoria)"
        img = Image.open(p).convert("RGB")
        if sh["kind"] in ("plate", "plate_master"):
            W, H = lib["grid"]["art_canvas"]
            art = img.resize((W, H), Image.BOX)
            arr = np.asarray(art.convert("RGBA")).copy()
            if pal: arr = quantize(arr, pal)
            out = Image.fromarray(arr, "RGBA").convert("RGB").resize((W * S, H * S), Image.NEAREST)
            rel = f"plates/{sh['name'][6:-4]}.png"; os.makedirs(os.path.join(a.out, "plates"), exist_ok=True)
            out.save(os.path.join(a.out, rel)); atlas["plates"][sh["name"][6:-4]] = rel
            report.append(f"- `{sh['name']}` → `{rel}`"); continue
        f = lib["sheet_formats"][sh["fmt"]]; gx, gy = f["grid"]; ca = f["cell_art"]; ax, ay = f["anchor_art"]
        expect = (gx * ca * S, gy * ca * S)
        if img.size != expect:
            img = img.resize(expect, Image.NEAREST); report.append(f"- `{sh['name']}`: tamaño {Image.open(p).size} ≠ {expect}, reescalada")
        art = quantize(to_art(img, S, gx * ca, gy * ca), pal)
        cells = [art[(i // gx) * ca:(i // gx + 1) * ca, (i % gx) * ca:(i % gx + 1) * ca] for i in range(gx * gy)]
        warn = []
        if sh["kind"] in ("model", "anim", "object", "items"):
            n = len(sh["cells"]) if "cells" in sh else len(sh["items"])
            used = cells[:n]; mets = [cell_metrics(c) for c in used]
            if any(m is None for m in mets): warn.append("cuadro vacío")
            if any(m and m["touches"] for m in mets): warn.append("un sprite toca el borde de la celda (¿cortado?)")
            if sh["kind"] == "items":
                fixed = []
                for c, m in zip(used, mets):
                    fixed.append(shift(c, int(round(ax - (m["left"] + m["right"]) / 2)), ay - m["base"]) if m else c)
                for it, c in zip(sh["items"], fixed):
                    key = f"item.{it['id']}"; rel = f"sprites/items/{it['id']}.png"
                    save_strip([c], os.path.join(a.out, rel), S)
                    atlas["sprites"][key] = dict(file=rel, frames=1, w=ca, h=ca, ax=ax, ay=ay, fps=1, mode="states", mirror=True)
                review(fixed, (ax, ay), os.path.join(a.out, "review", sh["name"]))
            else:
                ok = [m for m in mets if m]
                dx = int(round(ax - np.median([m["cx"] for m in ok]))); dy = int(round(ay - np.median([m["base"] for m in ok])))
                if abs(dx) > 12 or abs(dy) > 12: warn.append(f"ancla corrida {dx},{dy} px de arte")
                fixed = [shift(c, dx, dy) for c in used]
                if sh["kind"] == "model":
                    m0 = mets[0]; H = chars[sh["owner"]]["model"]["height_px"]
                    if m0:
                        hh = m0["base"] - m0["top"] + 1
                        if abs(hh - H) > H * 0.1: warn.append(f"altura {hh} px de arte, se pidió {H}")
                key = sh["key"]; parts.setdefault(key, {})[sh.get("part", 0)] = (sh, fixed)
                review(fixed, (ax, ay), os.path.join(a.out, "review", sh["name"]))
        elif sh["kind"] == "rows":
            for r, g in enumerate(sh["rows"]):
                fr = [art[r * ca:(r + 1) * ca, i * ca:(i + 1) * ca] for i in range(len(g["poses"]))]
                mets = [cell_metrics(c) for c in fr]; ok = [m for m in mets if m]
                if not ok: warn.append(f"fila {g['id']} vacía"); continue
                dx = int(round(ca / 2 - np.median([m["ccx"] for m in ok]))); dy = int(round(ca / 2 - np.median([m["ccy"] for m in ok])))
                fr = [shift(c, dx, dy) for c in fr]
                key = f"{sh['prefix']}.{g['id']}"; rel = f"sprites/{sh['prefix']}/{g['id']}.png"
                save_strip(fr, os.path.join(a.out, rel), S)
                atlas["sprites"][key] = dict(file=rel, frames=len(fr), w=ca, h=ca, ax=ca // 2, ay=ca // 2, fps=g.get("fps", 8), mode=g["mode"], mirror=True)
                review(fr, (ca // 2, ca // 2), os.path.join(a.out, "review", f"{sh['name'][:-4]}_{g['id']}.png"))
        report.append(f"- `{sh['name']}`{src_tag}" + (": " + "; ".join(warn) if warn else ": ok"))
    # join multi-sheet animations
    for key, ps in parts.items():
        sh0 = ps[min(ps)][0]
        if sh0["kind"] == "anim" and len(ps) < sh0["nparts"]:
            report.append(f"- `{key}`: faltan hojas ({len(ps)}/{sh0['nparts']}), no se exporta"); continue
        frames = [f for k in sorted(ps) for f in ps[k][1]]
        owner = sh0.get("owner", "obj"); name = key.split(".", 1)[1]
        rel = f"sprites/{owner}/{name}.png"
        save_strip(frames, os.path.join(a.out, rel), S)
        fm = lib["sheet_formats"][sh0["fmt"]]
        mirror = sh0["anim"].get("mirror_to_W", True) if sh0["kind"] == "anim" else True
        atlas["sprites"][key] = dict(file=rel, frames=len(frames), w=fm["cell_art"], h=fm["cell_art"], ax=fm["anchor_art"][0],
                                     ay=fm["anchor_art"][1], fps=sh0.get("fps", 8), mode=sh0.get("mode", "once"), mirror=mirror)
    os.makedirs(a.out, exist_ok=True)
    json.dump(atlas, open(os.path.join(a.out, "atlas.json"), "w"), indent=1)
    open(os.path.join(a.out, "atlas.js"), "w").write("window.PR_ATLAS = " + json.dumps(atlas) + ";\n")
    open(os.path.join(a.out, "slice_report.md"), "w").write("# Recorte de hojas\n\n" + "\n".join(report) + "\n")
    print(f"{len(atlas['sprites'])} sprites, {len(atlas['plates'])} plates -> {a.out}")
    print("\n".join(r for r in report if not r.endswith(": ok")))


if __name__ == "__main__":
    main()
