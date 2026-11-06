"""Pixel-crisp lighting and depth overlays for a set, from the "lighting" block of reel.json.

  python3 draw_light.py LIBRARY/sprites.json REEL/reel.json OUT_DIR

Writes, at x scale (nearest-neighbour, no blur, no gradients, palette colours only, ordered Bayer dithering):
  light.png    window light shaft + floor pool (blend: screen)
  shadows.png  contact / ambient-occlusion shadows under static props (blend: multiply)
  vignette.png dark dithered edges (normal blend)
  shadow.png   a small dithered ellipse used under moving characters (follows them on the floor)

reel.json "lighting": {
  "shaft": {"top": [x0, x1, y], "bottom": [x0, x1, y], "density": [0.35, 0.08], "colour": "#FFF3B0"},
  "contact": [[x, y, w, h], ...],                 # ellipses under props (art px, centre x, floor y)
  "vignette": 0.35,                               # max density at the corners
  "shadow_colour": "#2E2160", "character_shadow": [30, 7]
}
"""
import json, os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prmanifest as M

BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0


def dither(density):
    """density map (H,W) in 0..1 -> boolean pixels using a 4x4 ordered dither (stable, no noise)"""
    h, w = density.shape
    t = np.tile(BAYER, (h // 4 + 1, w // 4 + 1))[:h, :w]
    return density > t


def ellipse_density(W, H, cx, cy, rw, rh, core=0.6, edge=0.25):
    yy, xx = np.mgrid[0:H, 0:W]
    d = ((xx - cx) / max(rw, 1)) ** 2 + ((yy - cy) / max(rh, 1)) ** 2
    out = np.zeros((H, W)); out[d <= 1] = edge; out[d <= 0.45] = core
    return out


def save(rgba, path, S):
    Image.fromarray(rgba, "RGBA").resize((rgba.shape[1] * S, rgba.shape[0] * S), Image.NEAREST).save(path, optimize=True)


def layer(mask, colour):
    a = np.zeros(mask.shape + (4,), np.uint8); a[mask, :3] = M.hex2rgb(colour); a[mask, 3] = 255; return a


def main():
    lib, reel = M.load(sys.argv[1], sys.argv[2]); out = sys.argv[3]; os.makedirs(out, exist_ok=True)
    W, H = lib["grid"]["art_canvas"]; S = lib["grid"]["scale"]; L = reel.get("lighting", {})
    sc = L.get("shadow_colour", "#2E2160")
    # --- light shaft: quad between the window's bottom edge and the floor pool, density fading with distance
    dens = np.zeros((H, W))
    if "shaft" in L:
        (tx0, tx1, ty), (bx0, bx1, by) = L["shaft"]["top"], L["shaft"]["bottom"]; d0, d1 = L["shaft"].get("density", [0.35, 0.08])
        for y in range(int(ty), int(by) + 1):
            f = (y - ty) / max(1, by - ty)
            x0 = tx0 + (bx0 - tx0) * f; x1 = tx1 + (bx1 - tx1) * f
            row = d0 + (d1 - d0) * f
            xs = np.arange(int(x0), int(x1) + 1)
            edge = np.minimum(xs - x0, x1 - xs)                       # softer (sparser) near the shaft edges
            dens[y, xs.clip(0, W - 1)] = np.maximum(dens[y, xs.clip(0, W - 1)], row * np.clip(edge / 6, 0.35, 1))
        pool = ellipse_density(W, H, (bx0 + bx1) / 2, by - 4, (bx1 - bx0) / 2, 14, core=d1 * 2.2, edge=d1 * 1.2)
        dens = np.maximum(dens, pool)
    save(layer(dither(dens), L.get("shaft", {}).get("colour", "#FFF3B0")), os.path.join(out, "light.png"), S)
    # --- contact shadows under static props
    sd = np.zeros((H, W))
    for x, y, w, h in L.get("contact", []): sd = np.maximum(sd, ellipse_density(W, H, x, y, w / 2, h / 2))
    save(layer(dither(sd), sc), os.path.join(out, "shadows.png"), S)
    # --- vignette
    v = float(L.get("vignette", 0))
    yy, xx = np.mgrid[0:H, 0:W]; r = np.maximum(np.abs(xx - W / 2) / (W / 2), np.abs(yy - H / 2) / (H / 2))
    save(layer(dither(np.clip((r - 0.86) / 0.14, 0, 1) * v), "#150A34"), os.path.join(out, "vignette.png"), S)
    # --- character shadow sprite (centred on its own canvas)
    cw, ch = L.get("character_shadow", [30, 7]); cv = 40
    sp = layer(dither(ellipse_density(cv, 12, cv / 2, 6, cw / 2, ch / 2, core=0.55, edge=0.3)), sc)
    save(sp, os.path.join(out, "shadow.png"), S)
    print("overlays ->", out)


if __name__ == "__main__":
    main()
