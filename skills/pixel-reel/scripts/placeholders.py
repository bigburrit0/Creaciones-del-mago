"""Placeholder sheets in the exact format the image model must return (same names, grid, magenta, 4x4 art pixels).

Two uses:
  * an ANIMATIC before the real art exists: timing, staging and audio get locked early, real sheets drop in later;
  * a test bench for slice_sheets.py (--noisy imitates image-model defects: grid offset, soft edges, colour drift).

  python3 placeholders.py LIBRARY/sprites.json SHEETS_DIR [--reel reel.json] [--noisy] [--overwrite]

Existing (real) sheets are never overwritten unless --overwrite is given.
Characters are drawn as chibi silhouettes whose pose follows keywords in each frame description
(walk, sit, jump, arms up, offer, wave, eyes closed, mate, sack...). Items use the product photo when found.
"""
import argparse, os, random, sys
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prmanifest as M

MAG = (255, 0, 255)


def C(h, default="#888888"):
    return M.hex2rgb(h or default)


def has(t, *words): return any(w in t for w in words)


# ---------------------------------------------------------------- characters
def draw_char(d, pose, frame, direction, H, col, ax=64, ay=124):
    t = pose.lower(); side = direction in ("E", "W"); back = direction == "N"
    sit = has(t, "sitting", "sit ", "sits", "on the stool", "landing sitting")
    lift = 0
    if has(t, "apex"): lift = 22
    elif has(t, "takes off", "taking off", "jolt", "both feet off", "falling"): lift = 12
    squash = 0.86 if has(t, "squash", "crouch", "anticipation", "knees bent", "body lowest", "body low", "bending", "knees giving") else 1.0
    bob = 2 if has(t, "lowest", "body low", "body down", "down one pixel") else (-2 if has(t, "highest", "body up", "passing", "up one pixel") else 0)
    h = int(H * squash * (0.78 if sit else 1.0)); feet = ay - lift + bob
    top = feet - h; head_r = max(8, h // 6); head_cy = top + int(h * 0.28) + head_r // 2
    body_top = head_cy + head_r - 2; body_w = int(H * 0.42)
    lean = 6 if has(t, "bow", "bowing", "bending", "leaning") else 0
    outl = C(col.get("outline"), "#150A34")
    # legs / boots
    step = (frame % 2) * 2 - 1 if has(t, "foot forward", "flip-flop forward", "boot forward", "leg forward", "stride", "dragging") else 0
    if sit:
        d.rectangle([ax - 14, feet - 8, ax + 14, feet], fill=C(col.get("boots")), outline=outl)
    else:
        for sx, off in ((-8, step * 4), (8, -step * 4)):
            x = ax + sx + (off if side else 0)
            d.rectangle([x - 6, feet - 9, x + 6, feet], fill=C(col.get("boots")), outline=outl)
    # robe / body
    d.polygon([(ax - body_w // 3 + lean, body_top), (ax + body_w // 3 + lean, body_top), (ax + body_w // 2, feet - 8), (ax - body_w // 2, feet - 8)],
              fill=C(col.get("body")), outline=outl)
    d.rectangle([ax - body_w // 2 + 3, body_top + int(h * 0.32), ax + body_w // 2 - 3, body_top + int(h * 0.32) + 4], fill=C(col.get("belt", "#5A3424")))
    # arms
    sh_y = body_top + 6; hand = C(col.get("skin"))
    up = has(t, "arms up", "fists up", "hands up", "arms raised", "above the head", "arms fully up", "arms spread", "arms rise", "arms rising", "high above", "holding an object high")
    one_up = has(t, "hand raised", "wave", "index finger raised", "finger raised", "thumb up", "fanning")
    fwd = has(t, "extend", "offering", "pointing", "arm forward", "fully extended", "reaching", "swinging the arm", "toss", "arm pulling")
    for sgn in (-1, 1):
        sx = ax + sgn * (body_w // 3 + 4) + lean
        if up or (one_up and sgn == 1):
            ex, ey = sx + sgn * 6, top - 6
        elif fwd and sgn == 1:
            ex, ey = sx + (22 if direction != "W" else -22), sh_y + 6
        else:
            ex, ey = sx + sgn * 4, sh_y + int(h * 0.3)
        d.line([(sx, sh_y), (ex, ey)], fill=C(col.get("body")), width=7); d.line([(sx, sh_y), (ex, ey)], fill=outl, width=1)
        d.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=hand, outline=outl)
        if sgn == 1 and has(t, "mate", "gourd"):
            d.ellipse([ex - 6, ey - 12, ex + 6, ey], fill=C("#A0603A"), outline=outl); d.line([(ex + 2, ey - 12), (ex + 6, ey - 20)], fill=C("#D8D4C8"), width=2)
        if sgn == 1 and has(t, "sack") and not has(t, "empty"):
            d.ellipse([ex - 4, ey - 26, ex + 22, ey + 2], fill=C("#C0392B"), outline=outl)
        if sgn == 1 and has(t, "sack") and has(t, "empty", "upside"):
            d.polygon([(ex - 10, ey - 30), (ex + 10, ey - 30), (ex + 4, ey), (ex - 4, ey)], fill=C("#C0392B"), outline=outl)
    # head, beard, face
    hx = ax + lean + (4 if direction == "E" else -4 if direction == "W" else 0)
    d.ellipse([hx - head_r, head_cy - head_r, hx + head_r, head_cy + head_r], fill=C(col.get("skin")), outline=outl)
    if col.get("beard") and not back:
        bx = hx + (4 if direction == "E" else -4 if direction == "W" else 0)
        d.polygon([(bx - head_r, head_cy), (bx + head_r, head_cy), (bx, head_cy + int(h * 0.3))], fill=C(col.get("beard")), outline=outl)
    if not back:
        closed = has(t, "eyes closed", "sipping", "eyes squeezed", "closed with")
        wide = has(t, "eyes wide", "wide open", "eyes huge", "snap wide")
        for ex in ((hx - 4, hx + 4) if not side else ((hx + 4,) if direction == "E" else (hx - 4,))):
            if closed: d.line([(ex - 2, head_cy - 3), (ex + 2, head_cy - 3)], fill=outl, width=1)
            else: d.rectangle([ex - (2 if wide else 1), head_cy - 5, ex + (2 if wide else 1), head_cy - 2 + (2 if wide else 0)], fill=outl)
    # hat
    hat_y = head_cy - head_r + 3 - (6 if has(t, "hat lifting", "hat floating", "hat flying") else 0)
    if not has(t, "holding his santa hat", "hat in the right hand"):
        d.rectangle([hx - head_r - 4, hat_y - 2, hx + head_r + 4, hat_y + 3], fill=C(col.get("hat")), outline=outl)
        d.polygon([(hx - head_r + 2, hat_y - 2), (hx + head_r - 2, hat_y - 2), (hx + (8 if col.get("hat_tip") == "back" else 2), top - 2)], fill=C(col.get("hat")), outline=outl)
        if col.get("hat_band"): d.rectangle([hx - head_r + 1, hat_y - 6, hx + head_r - 1, hat_y - 3], fill=C(col.get("hat_band")))
        if col.get("pompom"): d.ellipse([hx + 2 - 4, top - 6, hx + 2 + 4, top + 2], fill=C(col.get("pompom")), outline=outl)


def char_colors(ch):
    p = ch.get("placeholder") or {}
    base = {"body": "#4B3A8E", "hat": "#4B3A8E", "hat_band": "#F2C14E", "beard": "#F0D8B2", "skin": "#F0C090", "boots": "#8A5638", "outline": "#150A34", "hat_tip": "back"}
    base.update(p); return base


# ---------------------------------------------------------------- objects / fx / items
def draw_object(d, oid, frame, n, cell, desc=""):
    c = cell // 2; o = C("#150A34"); t = (oid + " " + desc).lower()
    if "printer" in t:
        d.rectangle([c - 26, c + 8, c + 26, c + 28], fill=C("#B9B4C0"), outline=o)
        d.rectangle([c - 26, c - 30, c - 18, c + 8], fill=C("#5B4636"), outline=o)
        d.rectangle([c - 18, c - 30, c + 22, c - 24], fill=C("#5B4636"), outline=o)
        nx = c - 14 + (frame % 3) * 14; d.rectangle([nx, c - 24, nx + 8, c - 14], fill=C("#D8D4C8"), outline=o)
        if frame in (1, 2): d.rectangle([nx + 3, c - 14, nx + 5, c - 12], fill=C("#E86A4A"))
        d.ellipse([c + 8, c - 44, c + 22, c - 30], fill=C("#F2C14E"), outline=o)
        d.rectangle([c + 14, c + 14, c + 22, c + 20], fill=C("#5C9A4A" if frame == n - 1 else "#2B4C7E"))
    elif "door" in t:
        w = [34, 18, 6][min(frame, 2)]
        d.rectangle([c - 18, c - 40, c + 18, c + 40], fill=C("#FBF4E4") if frame else C("#5B4636"), outline=o)
        d.rectangle([c - 18, c - 40, c - 18 + w, c + 40], fill=C("#8A5638"), outline=o)
    elif "sack" in t:
        r = [6, 12, 18, 24][min(frame, 3)]
        if frame == 0: d.rectangle([c - 22, c + 14, c + 22, c + 22], fill=C("#C0392B"), outline=o)
        else: d.ellipse([c - r, c + 24 - 2 * r, c + r, c + 24], fill=C("#C0392B"), outline=o)
        if frame == 3: d.rectangle([c - 4, c - 26, c + 4, c - 22], fill=C("#F2C14E"))
    elif "gift" in t:
        d.rectangle([c - 18, c - 4, c + 18, c + 24], fill=C("#C0392B"), outline=o); d.rectangle([c - 3, c - 4, c + 3, c + 24], fill=C("#F2C14E"))
        ly = c - 8 - frame * 8; d.rectangle([c - 20 + frame * 6, ly, c + 20 + frame * 6, ly + 6], fill=C("#C0392B"), outline=o)
    elif "stool" in t:
        d.ellipse([c - 14, c - 6, c + 14, c + 2], fill=C("#B08A5A"), outline=o)
        for x in (c - 10, c, c + 10): d.line([(x, c), (x, c + 18)], fill=C("#5A3424"), width=3)
    elif "fan" in t:
        d.rectangle([c - 3, c, c + 3, c + 18], fill=C("#2B4C7E")); d.ellipse([c - 14, c - 26, c + 14, c + 2], outline=o, fill=C("#9CC9E8"))
        import math
        for k in range(3):
            a = math.radians(frame * 30 + k * 120); d.line([(c, c - 12), (c + 12 * math.cos(a), c - 12 + 12 * math.sin(a))], fill=C("#2B4C7E"), width=3)
    elif "tree" in t:
        d.polygon([(c, c - 28), (c - 18, c + 14), (c + 18, c + 14)], fill=C("#2F5A32"), outline=o); d.rectangle([c - 8, c + 14, c + 8, c + 24], fill=C("#A0603A"), outline=o)
        for k, (x, y) in enumerate([(c - 6, c - 6), (c + 7, c), (c - 2, c + 8), (c + 2, c - 14), (c - 10, c + 10)]):
            d.rectangle([x, y, x + 2, y + 2], fill=C("#FFF3B0" if frame else "#7A1E22"))
    elif "garland" in t:
        d.rectangle([4, c - 4, cell - 4, c + 4], fill=C("#2F5A32"), outline=o)
        for x in range(10, cell - 6, 10): d.rectangle([x, c + 4, x + 2, c + 6], fill=C("#FFF3B0" if frame else "#C0392B"))
    elif "wreath" in t:
        d.ellipse([c - 14, c - 14, c + 14, c + 14], outline=C("#2F5A32"), width=6); d.rectangle([c - 4, c + 10, c + 4, c + 16], fill=C("#C0392B"))
    elif "mate" in t:
        d.ellipse([c - 8, c - 8, c + 8, c + 10], fill=C("#A0603A"), outline=o); d.line([(c + 2, c - 8), (c + 8, c - 18)], fill=C("#D8D4C8"), width=2)
    else:
        d.rectangle([c - 12, c - 12, c + 12, c + 12], fill=C("#B08A5A"), outline=o)


def draw_fx(d, fid, frame, cell):
    c = cell // 2; s = frame + 1; o = C("#150A34")
    if "sparkle" in fid or "magic" in fid:
        r = [3, 7, 10, 5][frame % 4]; col = C("#FFF3B0")
        d.line([(c - r, c), (c + r, c)], fill=col, width=2); d.line([(c, c - r), (c, c + r)], fill=col, width=2)
        if frame >= 2: [d.rectangle([c + dx, c + dy, c + dx + 1, c + dy + 1], fill=C("#F2B640")) for dx, dy in ((-9, -9), (9, -9), (-9, 9), (9, 9))]
    elif "puff" in fid or "steam" in fid or "dust" in fid:
        for k in range(3): d.ellipse([c - 4 * s + k * 4 * s // 2 - 4, c - 3 * s, c - 4 * s + k * 4 * s // 2 + 4 * s // 2 + 4, c + 3 * s], fill=C("#E9D8B4"), outline=C("#B08A5A"))
    elif "confetti" in fid:
        rnd = random.Random(7)
        for k in range(14):
            x = c + int((rnd.random() - 0.5) * 8 * s); y = c + int((rnd.random() - 0.5) * 6 * s) + frame * 3
            d.rectangle([x, y, x + 2, y + 2], fill=C(["#C0392B", "#F2C14E", "#5C9A4A"][k % 3]))
    elif "heart" in fid:
        for k in range(min(2, s)):
            x, y = c - 6 + k * 10, c - frame * 4 - k * 6
            d.polygon([(x - 4, y), (x + 4, y), (x, y + 6)], fill=C("#C0392B")); d.ellipse([x - 4, y - 3, x, y + 1], fill=C("#C0392B")); d.ellipse([x, y - 3, x + 4, y + 1], fill=C("#C0392B"))
    elif "sweat" in fid:
        for k in range(min(3, s)): d.ellipse([c - 8 + k * 8, c - 4 - k * 3 - frame, c - 4 + k * 8, c + 2 - k * 3 - frame], fill=C("#9CC9E8"), outline=C("#2B4C7E"))
    elif "idea" in fid:
        d.ellipse([c - 6, c - 8, c + 6, c + 4], fill=C("#FFF3B0"), outline=o); d.rectangle([c - 3, c + 4, c + 3, c + 8], fill=C("#B08A5A"))
        if frame: [d.line([(c, c - 2), (c + dx * (6 + 3 * frame), c - 2 + dy * (6 + 3 * frame))], fill=C("#F2B640"), width=1) for dx, dy in ((1, 0), (-1, 0), (0, -1), (1, -1), (-1, -1))]
    elif "moth" in fid:
        d.ellipse([c - 2, c - 3, c + 2, c + 3], fill=C("#5B4636")); w = 7 if frame % 2 == 0 else 3
        d.polygon([(c, c), (c - w, c - 5), (c - w, c + 2)], fill=C("#B08A5A")); d.polygon([(c, c), (c + w, c - 5), (c + w, c + 2)], fill=C("#B08A5A"))
    elif "swirl" in fid:
        import math
        pts = [(c + int(math.cos(a / 3 + frame) * a / 3), c + int(math.sin(a / 3 + frame) * a / 3)) for a in range(0, 30)]
        d.line(pts, fill=o, width=2)
    elif "notes" in fid:
        x, y = c - 4, c - frame * 4; d.rectangle([x, y, x + 3, y + 3], fill=o); d.line([(x + 3, y + 3), (x + 3, y - 8)], fill=o, width=1)
    else:
        d.ellipse([c - s * 2, c - s * 2, c + s * 2, c + s * 2], fill=C("#FFF3B0"))


def draw_item(img_cell, item, lib, art_box):
    """paste a pixelated product photo (or a plain token) into an art-res cell"""
    photos = lib.get("items", {}).get("photos_dir")
    path = None
    if photos:
        cand = photos.replace("<id>", item["id"])
        for base in (lib["_dir"], os.path.join(lib["_dir"], ".."), os.path.join(lib["_dir"], "..", "..")):
            if os.path.exists(os.path.join(base, cand)): path = os.path.join(base, cand); break
    x0, y0, s = art_box
    d = ImageDraw.Draw(img_cell)
    if path:
        ph = Image.open(path).convert("RGB"); w, h = ph.size; m = min(w, h)
        ph = ph.crop(((w - m) // 2, (h - m) // 2, (w + m) // 2, (h + m) // 2)).resize((s - 2, s - 2), Image.LANCZOS).quantize(16).convert("RGB")
        d.rectangle([x0, y0, x0 + s - 1, y0 + s - 1], outline=C("#150A34")); img_cell.paste(ph, (x0 + 1, y0 + 1))
    else:
        d.rectangle([x0, y0, x0 + s - 1, y0 + s - 1], fill=C("#B08A5A"), outline=C("#150A34"))


# ---------------------------------------------------------------- plates
def draw_plate(lib, sid, master=False):
    W, H = lib["grid"]["art_canvas"]; st = lib["sets"][sid]; A = st.get("plate", {}).get("anchors_art", {})
    im = Image.new("RGB", (W, H), C("#E9D8B4")); d = ImageDraw.Draw(im); o = C("#150A34")
    d.rectangle([0, 0, W, 190], fill=C("#B08A5A"))
    for x in range(0, W, 18): d.line([(x, 0), (x, 190)], fill=C("#8A5638"))
    d.rectangle([0, 190, W, 430], fill=C("#C8AE88"))
    for y in range(196, 430, 14): d.line([(0, y), (W, y)], fill=C("#B08A5A"))
    for i, x in enumerate(range(0, W, 30)):
        for j, y in enumerate(range(430, H, 25)): d.rectangle([x, y, x + 30, y + 25], fill=C("#E86A4A" if (i + j) % 2 else "#FBF4E4"))
    if "window" in A:
        x, y = A["window"]; d.rectangle([x - 34, y - 34, x + 34, y + 30], fill=C("#9CC9E8"), outline=o, width=2); d.ellipse([x + 8, y - 26, x + 22, y - 12], fill=C("#F2C14E"))
    if "bench_front" in A:
        x, y = A["bench_front"]; d.rectangle([x - 46, y - 70, x + 46, y - 38], fill=C("#8A5638"), outline=o)
    if "door" in A:
        x, y = A["door"]; d.rectangle([x - 18, y - 82, x + 18, y], fill=C("#2E2160"), outline=o)
    d.ellipse([90, 300, 180, 360], fill=C("#D9826A"), outline=C("#A0603A"))
    for y0 in (60, 100):
        d.rectangle([10, y0, 70, y0 + 4], fill=C("#5A3424"))
        for k in range(4): d.rectangle([14 + k * 14, y0 - 10, 22 + k * 14, y0], fill=C(["#C0392B", "#2B4C7E", "#F2C14E", "#5C9A4A"][k]))
    return im


# ---------------------------------------------------------------- sheet assembly
def finish(art, scale, noisy, rnd):
    big = art.resize((art.width * scale, art.height * scale), Image.NEAREST)
    if noisy:  # imitate an image model: off-grid shift, soft edges, slight colour drift
        dx, dy = rnd.randint(1, scale - 1), rnd.randint(1, scale - 1)
        sh = Image.new("RGB", big.size, MAG); sh.paste(big, (dx, dy)); big = sh.filter(ImageFilter.GaussianBlur(0.7))
        px = big.load()
        for _ in range(4000):
            x, y = rnd.randrange(big.width), rnd.randrange(big.height); r, g, b = px[x, y]
            px[x, y] = (min(255, r + rnd.randint(-8, 8)), min(255, max(0, g + rnd.randint(-8, 8))), min(255, b + rnd.randint(-8, 8)))
    return big


def make_sheet(lib, reel, sh, chars, rnd, noisy):
    S = lib["grid"]["scale"]; f = lib["sheet_formats"].get(sh["fmt"], {})
    if sh["kind"] in ("plate", "plate_master"):
        im = draw_plate(lib, sh["set"], sh["kind"] == "plate_master")
        return finish(im, S, noisy, rnd)
    cell = f["cell_art"]; gx, gy = f["grid"]
    art = Image.new("RGB", (cell * gx, cell * gy), MAG)
    def cell_img(i):
        c = Image.new("RGB", (cell, cell), MAG); return c
    if sh["kind"] in ("model", "anim"):
        ch = chars[sh["owner"]]; col = char_colors(ch); H = ch["model"]["height_px"]
        for i, pose in enumerate(sh["cells"]):
            c = cell_img(i); d = ImageDraw.Draw(c)
            direction = sh["anim"]["dir"] if sh["kind"] == "anim" else ["S", "E", "N", "S"][i]
            if direction == "S>N": direction = ["S", "E", "N"][min(i, 2)]
            flip = direction == "W"
            draw_char(d, pose, sh.get("part", 0) * 4 + i, "E" if flip else direction, H, col, f["anchor_art"][0], f["anchor_art"][1])
            if flip: c = c.transpose(Image.FLIP_LEFT_RIGHT)
            art.paste(c, ((i % gx) * cell, (i // gx) * cell))
    elif sh["kind"] == "object":
        o = sh["obj"]
        for i in range(len(o["poses"])):
            c = cell_img(i); draw_object(ImageDraw.Draw(c), o["id"], i, len(o["poses"]), cell, o.get("description", "")); art.paste(c, ((i % gx) * cell, (i // gx) * cell))
    elif sh["kind"] == "rows":
        for r, g in enumerate(sh["rows"]):
            for i in range(len(g["poses"])):
                c = cell_img(i); dd = ImageDraw.Draw(c)
                if sh["prefix"] == "fx": draw_fx(dd, g["id"], i, cell)
                else: draw_object(dd, g["id"], i, len(g["poses"]), cell, g.get("description", ""))
                art.paste(c, (i * cell, r * cell))
    elif sh["kind"] == "items":
        m = f.get("item_max_art", 40); ay = f["anchor_art"][1]
        for i, it in enumerate(sh["items"]):
            c = cell_img(i); draw_item(c, it, lib, ((cell - m) // 2, ay - m, m)); art.paste(c, ((i % gx) * cell, (i // gx) * cell))
    big = finish(art, S, noisy, rnd)
    return big.resize(tuple(f["image"]), Image.NEAREST) if big.size != tuple(f["image"]) else big


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("library"); ap.add_argument("out"); ap.add_argument("--reel")
    ap.add_argument("--noisy", action="store_true"); ap.add_argument("--overwrite", action="store_true"); ap.add_argument("--seed", type=int, default=3)
    a = ap.parse_args(); lib, reel = M.load(a.library, a.reel); os.makedirs(a.out, exist_ok=True)
    chars = M.characters(lib, reel); rnd = random.Random(a.seed); n = 0
    for sh in [s for s in M.plan(lib, reel) if s["needed"]]:
        p = os.path.join(a.out, sh["name"])
        if os.path.exists(p) and not a.overwrite: continue
        make_sheet(lib, reel, sh, chars, rnd, a.noisy).save(p); n += 1
    print(f"{n} placeholder sheets -> {a.out}")


if __name__ == "__main__":
    main()
