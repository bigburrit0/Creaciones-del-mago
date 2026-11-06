"""Clean-up pass after build_garden.py: a clean feeder, a taller trunk and a short rope.

The feeder cut from keyframe 3 carried leaf fringes, a chunk of trunk and specks, and
the branch it hung from floated with no tree under it. Instead the canopy rises (the
tree grows taller), the trunk stretches up behind the feeder, and the feeder hangs from
the canopy on a short rope.

Usage: python3 tools/fix_feeder.py garden/assets
Writes feeder.png (cleaned, in place), trunk_up.png and rope2.png; prints CANOPY_DY.
"""
import sys
import numpy as np
from PIL import Image

A = sys.argv[1]
CANOPY_DY = -300          # canopy moves up by this many px once the tree grows taller


def load(name):
    return np.array(Image.open(f"{A}/{name}").convert("RGBA")).astype(int)


def save(arr, name):
    Image.fromarray(arr.clip(0, 255).astype(np.uint8), "RGBA").save(f"{A}/{name}", optimize=True)


def dilate(m):
    d = m.copy()
    d[1:] |= m[:-1]; d[:-1] |= m[1:]; d[:, 1:] |= m[:, :-1]; d[:, :-1] |= m[:, 1:]
    return d


def components(m):
    """label 4-connected components (small images only)"""
    lab = np.zeros(m.shape, int); n = 0
    ys, xs = np.nonzero(m)
    for y0, x0 in zip(ys, xs):
        if lab[y0, x0]:
            continue
        n += 1; stack = [(y0, x0)]; lab[y0, x0] = n
        while stack:
            y, x = stack.pop()
            for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= yy < m.shape[0] and 0 <= xx < m.shape[1] and m[yy, xx] and not lab[yy, xx]:
                    lab[yy, xx] = n; stack.append((yy, xx))
    return lab, n


# ---------- feeder: rebuilt symmetric from its cleaner right half, trimmed to its silhouette
f = load("feeder.png")
r, g, b, a = f[..., 0], f[..., 1], f[..., 2], f[..., 3]
lilac = (a > 0) & (b > r - 10) & (b > g) & (r + g + b > 330)
lrows = np.nonzero(lilac.sum(1) > 20)[0]
centres = [(np.nonzero(lilac[y])[0].min() + np.nonzero(lilac[y])[0].max()) / 2 for y in lrows]
cx = int(round(np.median(centres)))
out = np.zeros_like(f)
H, W = a.shape
for y in range(H):
    for x in range(cx, min(W, 2 * cx + 1)):
        out[y, x] = f[y, x]
        if 2 * cx - x >= 0:
            out[y, 2 * cx - x] = f[y, x]
OUTLINE = 6
for y in range(H):
    xs = np.nonzero(lilac[y, cx:])[0]
    if y < lrows.min():
        half = 16 if y >= lrows.min() - 40 else -1          # the hanging ring above the dome
    elif y <= lrows.max() and xs.size:
        half = xs.max() + OUTLINE
    elif y <= lrows.max() + OUTLINE:
        half = prev
    else:
        half = -1
    prev = half
    keep = np.abs(np.arange(W) - cx) <= half
    out[y, ~keep] = 0
out[..., 3] = np.where(out[..., 3] > 0, 255, 0)
# pinholes inside the silhouette take the colour above; stray gold at the eave tips goes
for y in range(1, H):
    xs = np.nonzero(out[y, :, 3])[0]
    if xs.size < 2:
        continue
    for x in range(xs.min(), xs.max() + 1):
        if out[y, x, 3] == 0:
            out[y, x] = out[y - 1, x]
    for x in list(range(xs.min(), xs.min() + 8)) + list(range(xs.max() - 7, xs.max() + 1)):
        pr, pg, pb = out[y, x, :3]
        if pr > 170 and pg > 120 and pb < 120:
            out[y, x, 3] = 0
save(out, "feeder.png")
keep = out[..., 3] > 0
fy, fx = np.nonzero(keep)
ring_top = fy.min()
ring_x = cx
print("feeder", fx.min(), fx.max(), fy.min(), fy.max(), "axis", cx)

# ---------- trunk stretched upward (sits behind the feeder, under the raised canopy)
t = load("trunk.png")
H, W = t.shape[:2]
ta = t[..., 3] > 0
rows = np.nonzero(ta.any(1))[0]
# drawn clean in the stem's own palette (tiling a cut-out section repeated its specks as dashes):
# dark outline | light bark | mid | green | dark outline, with a bark notch every few art-pixels
y0 = rows.min() + 60                                                       # a clean row of the real stem
xs = np.nonzero(ta[y0])[0]
mid = int(np.median(xs[np.abs(xs - np.median(xs)) < 40]))
xs = xs[np.abs(xs - mid) < 20]
x0, x1 = xs.min(), xs.max() + 1                                            # same width as the real stem
OUT, HI, MIDC, GREEN, NOTCH = (8, 14, 40), (150, 134, 106), (108, 119, 90), (61, 104, 81), (44, 80, 66)
w = x1 - x0
profile = [OUT] * 3 + [HI] * round(w * 0.22) + [MIDC] * round(w * 0.2)
profile += [GREEN] * (w - len(profile) - 3) + [OUT] * 3
c = load("canopy.png")
cy = np.nonzero((c[..., 3] > 0).any(1))[0]
top = cy.max() + CANOPY_DY - 40                                            # hidden under the canopy
bottom = rows.min() + 40                                                   # overlaps the real trunk a little
up = np.zeros_like(t)
for x, col in zip(range(x0, x1), profile):
    up[top:bottom, x, :3] = col
    up[top:bottom, x, 3] = 255
ART = 5                                                                    # one art-pixel in this layer
for k, y in enumerate(range(top + 12, bottom - 10, 7 * ART)):
    gx = x0 + 3 + round(w * 0.42) + (ART if k % 2 else 0)                  # notch on the green side
    up[y:y + ART, gx:gx + 2 * ART, :3] = NOTCH
    hx = x0 + 3 + (ART if k % 2 else 0)                                    # small dark mark on the light side
    up[y + 3 * ART:y + 4 * ART, hx:hx + ART, :3] = MIDC
cols = np.arange(x0, x1)
save(up, "trunk_up.png")
print("trunk_up cols", x0, x1, "rows", top, bottom)

# ---------- short rope from the canopy to the feeder ring (2 art-pixels wide)
rope = np.zeros_like(t)
canopy_bot = cy.max() + CANOPY_DY - 24
dark, light = (74, 52, 38, 255), (139, 101, 64, 255)
for yy in range(canopy_bot, ring_top + 6):
    rope[yy, ring_x - 4: ring_x] = dark
    rope[yy, ring_x: ring_x + 3] = light if (yy // 6) % 2 else dark
save(rope, "rope2.png")
print("CANOPY_DY", CANOPY_DY, "rope", canopy_bot, ring_top)
