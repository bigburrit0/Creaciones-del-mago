"""Draw the small FX sheets procedurally (no image model needed): crisp pixel art in the project palette.

  python3 draw_fx.py LIBRARY/sprites.json OUT_DIR [--reel reel.json] [--only fx_1.png,...] [--preview P.png]

Writes the same fx_N.png sheets the plan expects (1024x1024, 4x4 cells of 64 art px, one effect per row, magenta
background), so they go through slice_sheets/assemble exactly like generated ones. Effects without a drawer here are
left empty and reported, so they can still go to the image model.
"""
import argparse, math, os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prmanifest as M

MAG = (255, 0, 255)
C = {k: M.hex2rgb(v) for k, v in {
    "out": "#150A34", "y1": "#FFF3B0", "y2": "#F2C14E", "y3": "#C98A2B", "cream": "#FBF4E4", "sand": "#E9D8B4",
    "tan": "#B08A5A", "brown": "#5B4636", "red": "#C0392B", "red2": "#7A1E22", "pink": "#E86A4A", "green": "#5C9A4A",
    "green2": "#2F5A32", "blue1": "#9CC9E8", "blue2": "#4F86C6", "blue3": "#2B4C7E", "grey": "#D8D4C8", "grey2": "#B08A5A",
    "violet": "#6A58B8"}.items()}


class Cell:
    def __init__(self, n=64): self.a = np.zeros((n, n, 3), np.uint8); self.a[:] = MAG; self.n = n
    def px(self, x, y, c):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < self.n and 0 <= y < self.n: self.a[y, x] = C[c] if isinstance(c, str) else c
    def rect(self, x, y, w, h, c):
        for yy in range(int(y), int(y + h)):
            for xx in range(int(x), int(x + w)): self.px(xx, yy, c)
    def bitmap(self, rows, x0, y0, pal):
        for j, r in enumerate(rows):
            for i, ch in enumerate(r):
                if ch in pal: self.px(x0 + i, y0 + j, pal[ch])
    def disc(self, cx, cy, r, fill, edge="out"):
        for y in range(int(cy - r - 1), int(cy + r + 2)):
            for x in range(int(cx - r - 1), int(cx + r + 2)):
                d = math.hypot(x - cx, y - cy)
                if d <= r - 0.6: self.px(x, y, fill)
                elif d <= r + 0.4 and edge: self.px(x, y, edge)


def star(c, cx, cy, s, col="y1", edge="y2"):
    for k in range(-s, s + 1):
        c.px(cx + k, cy, col if abs(k) < s else edge); c.px(cx, cy + k, col if abs(k) < s else edge)
    if s >= 3: c.px(cx - 1, cy - 1, "y1"); c.px(cx + 1, cy - 1, "y1"); c.px(cx - 1, cy + 1, "y1"); c.px(cx + 1, cy + 1, "y1")


HEART = [".XX.XX.", "XRRXRRX", "XRPRRRX", "XRRRRRX", ".XRRRX.", "..XRX..", "...X..."]
DROP = ["..X..", ".XBX.", ".XBX.", "XBWBX", "XBBBX", ".XXX."]
BULB = ["..XXXX..", ".XYYYYX.", "XYWYYYYX", "XYYYYYYX", "XYYYYYYX", ".XYYYYX.", "..XYYX..", "..XTTX..", "..XTTX..", "...XX..."]
NOTE = ["...XX", "...XYX", "...X.X", "...X..", "...X..", ".XXX..", "XYYX..", ".XX..."]
MOTH_UP = ["X...........X", "XX.........XX", "XWX.......XWX", "XWWX.....XWWX", ".XWWX.X.XWWX.", "..XWWXBXWWX..",
           "...XXXBXXX...", "......X......"]
MOTH_DN = ["......X......", "...XXXBXXX...", "..XWWXBXWWX..", ".XWWWXBXWWWX.", "XWWWX...XWWWX", "XXXX.....XXXX"]
SPIRAL = [".XXXXX.", "X.....X", "X.XXX.X", "X.X.X.X", "X.X...X", "X.XXXX.", "X......"]
PAL = {"X": "out", "R": "red", "P": "pink", "B": "blue1", "W": "cream", "Y": "y1", "T": "tan"}


def fx_sparkle(i, c):
    s = [1, 3, 5, 0][i]
    if s: star(c, 32, 32, s)
    if i >= 2:
        for dx, dy in ((-9, -9), (9, -9), (-9, 9), (9, 9)): c.px(32 + dx, 32 + dy, "y2")
    if i == 3:
        for dx, dy in ((-12, 0), (12, 0), (0, -12), (0, 12)): c.px(32 + dx, 32 + dy, "y1")


def fx_puff(i, c):
    r = [4, 7, 9, 0][i]
    if r:
        for dx, dy, k in ((-r, 2, 0.8), (r, 2, 0.8), (0, -r // 2, 1.0)): c.disc(32 + dx, 34 + dy, r * k, "cream", "tan")
        c.disc(32, 35, r, "sand", "tan")
    else:
        for dx, dy in ((-12, 2), (10, -4), (-4, -10), (12, 8), (-10, 10)): c.px(32 + dx, 32 + dy, "sand")


def fx_confetti(i, c):
    rnd = np.random.default_rng(7); cols = ["red", "y2", "green", "blue2", "pink"]
    for k in range(18):
        ang = rnd.uniform(0, 2 * math.pi); sp = rnd.uniform(0.5, 1.0)
        rr = [3, 10, 17, 22][i] * sp; fall = [0, 1, 5, 11][i]
        x, y = 32 + math.cos(ang) * rr, 30 + math.sin(ang) * rr * 0.8 + fall
        if i == 3 and k % 3 == 0: continue
        c.rect(x, y, 2, 2 if k % 2 else 1, cols[k % len(cols)])


def fx_hearts(i, c):
    pos = [[(29, 30)], [(29, 24), (40, 34)], [(29, 16), (40, 26)], [(29, 8), (40, 18)]][i]
    for k, (x, y) in enumerate(pos):
        if i == 3 and k == 0: continue
        c.bitmap(HEART, x - 3, y, PAL)


def fx_sweat(i, c):
    drops = [[(30, 30)], [(24, 28), (36, 26)], [(20, 26), (31, 22), (42, 26)], [(18, 30), (44, 30)]][i]
    for x, y in drops: c.bitmap(DROP, x - 2, y, PAL)


def fx_idea(i, c):
    c.bitmap(BULB, 28, 24, PAL)
    L = [0, 3, 6, 4][i]
    for k in range(1, L + 1):
        c.px(32, 22 - k, "y2"); c.px(25 - k, 28, "y2"); c.px(38 + k, 28, "y2")
        c.px(27 - k, 23 - k, "y1"); c.px(36 + k, 23 - k, "y1")


def fx_steam(i, c):
    for k in range(min(3, i + 1)):
        y = 40 - k * 9 - i * 2
        if i == 3 and k == 0: continue
        c.disc(30 + (k % 2) * 6, y, 3 + k, "grey", "tan")


def fx_swirl(i, c):
    b = np.array([list(r) for r in SPIRAL]); b = np.rot90(b, -i)
    c.bitmap(["".join(r) for r in b], 29, 28, PAL)


def fx_moth(i, c):
    c.bitmap(MOTH_UP if i % 2 == 0 else MOTH_DN, 26, 28, {"X": "out", "W": "grey", "B": "brown"})


def fx_magic_ring(i, c):
    r = [6, 11, 16, 18][i]
    for k in range(12):
        a = k / 12 * 2 * math.pi
        x, y = 32 + math.cos(a) * r, 32 + math.sin(a) * r * 0.9
        if i == 3 and k % 2: continue
        if k % 3 == 0 and i < 3: star(c, int(x), int(y), 1)
        else: c.px(x, y, "y2" if i < 2 else "y1")


def fx_notes(i, c):
    pos = [[(26, 34)], [(26, 28), (36, 36)], [(26, 22), (36, 30)], [(36, 24)]][i]
    for x, y in pos: c.bitmap(NOTE, x, y, PAL)


def fx_dust_motes(i, c):
    pts = [(20, 22), (34, 30), (44, 18), (26, 42), (40, 44)]
    for k, (x, y) in enumerate(pts): c.rect(x + (i * 2 if k % 2 else -i), y - i * 2, 2, 2, "y1" if k % 2 else "sand")


DRAW = {k[3:] if False else k: v for k, v in globals().items() if k.startswith("fx_") and callable(v)}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("library"); ap.add_argument("out"); ap.add_argument("--reel")
    ap.add_argument("--only"); ap.add_argument("--preview")
    a = ap.parse_args(); lib, reel = M.load(a.library, a.reel); S = lib["grid"]["scale"]; os.makedirs(a.out, exist_ok=True)
    only = set(a.only.split(",")) if a.only else None; previews = []
    for sh in [s for s in M.plan(lib, None) if s["kind"] == "rows" and s["prefix"] == "fx"]:
        if only and sh["name"] not in only: continue
        sheet = np.zeros((256, 256, 3), np.uint8); sheet[:] = MAG; missing = []
        for r, g in enumerate(sh["rows"]):
            fn = DRAW.get(g["id"])
            if not fn: missing.append(g["id"]); continue
            for i in range(len(g["poses"])):
                c = Cell(); fn(i, c); sheet[r * 64:(r + 1) * 64, i * 64:(i + 1) * 64] = c.a
        im = Image.fromarray(sheet).resize((256 * S, 256 * S), Image.NEAREST); im.save(os.path.join(a.out, sh["name"])); previews.append(im)
        print(sh["name"], "dibujada" + (f"; sin dibujante: {missing}" if missing else ""))
    if a.preview and previews:
        o = Image.new("RGB", (512 * len(previews), 512))
        for k, im in enumerate(previews): o.paste(im.resize((512, 512), Image.NEAREST), (k * 512, 0))
        o.save(a.preview)


if __name__ == "__main__":
    main()
