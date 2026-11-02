from PIL import Image, ImageFilter
import numpy as np
def load(src, i): return np.asarray(Image.open(f'{src}/{i}.jpg').convert('RGB')).astype(np.float32)
def diff(a, b): return np.abs(a-b).sum(2)
def lum(a): return a.mean(2)
def mf(m, f): return np.asarray(Image.fromarray((m*255).astype(np.uint8)).filter(f)) > 127
def dilate(m, r): return mf(m, ImageFilter.MaxFilter(2*r+1)) if r else m
def erode(m, r): return mf(m, ImageFilter.MinFilter(2*r+1)) if r else m
def box(m, x0, y0, x1, y1):
    z = np.zeros_like(m); z[y0:y1, x0:x1] = m[y0:y1, x0:x1]; return z
def boxmask(shape, x0, y0, x1, y1):
    z = np.zeros(shape[:2], bool); z[y0:y1, x0:x1] = True; return z
def flood(passable, seed):
    m = seed & passable
    while True:
        n = dilate(m, 1) & passable
        if n.sum() == m.sum(): return n
        m = n
def wand(img, bx, dark=62, close=3, extra_bar=None, navy=True, bgtol=0, open_r=0):
    """sprite mask inside bx: everything not reachable from the box border through non-outline pixels.
    The outline barrier is thickened by `close` px so small gaps do not leak; the mask is grown back after."""
    x0, y0, x1, y1 = bx
    sub = img[y0:y1, x0:x1]
    bar = lum(sub) <= dark
    if navy: bar &= (sub[..., 2] >= sub[..., 0] - 6)   # navy outlines only (soil/trunk are brown)
    if extra_bar is not None: bar |= extra_bar[y0:y1, x0:x1]
    bar = dilate(bar, close)
    seed = np.zeros(bar.shape, bool); seed[0, :] = seed[-1, :] = seed[:, 0] = seed[:, -1] = True
    bg = flood(~bar, seed)
    fg = dilate(~bg, close) & ~erode(bg, close) if False else ~dilate(erode(bg, 0), 0)
    fg = ~bg
    # grow back the eroded rim: pixels of bg within `close` of fg that are outline-dark
    rim = dilate(fg, close) & (lum(sub) <= dark + 20)
    if navy: rim &= (sub[..., 2] >= sub[..., 0] - 6)
    fg = fg | rim
    if bgtol:
        border = np.concatenate([sub[0], sub[-1], sub[:, 0], sub[:, -1]])
        pal = np.unique((border // 12).astype(int), axis=0) * 12 + 6
        d = np.min(np.abs(sub[:, :, None, :] - pal[None, None]).sum(3), 2)
        fg &= d > bgtol
    if open_r:
        fg = dilate(erode(fg, open_r), open_r) & fg
    m = np.zeros(img.shape[:2], bool); m[y0:y1, x0:x1] = fg
    return m
def inpaint(img, mask, iters=60):
    """diffusion fill of masked pixels from their surroundings (works on the mask's bbox)"""
    if not mask.any(): return img
    ys, xs = np.where(mask); m = 4
    y0, y1 = max(ys.min()-m, 0), min(ys.max()+m+1, img.shape[0]); x0, x1 = max(xs.min()-m, 0), min(xs.max()+m+1, img.shape[1])
    full = img.copy(); full[y0:y1, x0:x1] = _inpaint(img[y0:y1, x0:x1], mask[y0:y1, x0:x1], iters); return full
def _inpaint(img, mask, iters):
    out = img.copy(); known = ~mask
    for _ in range(iters):
        if known.all(): break
        acc = np.zeros_like(out); cnt = np.zeros(out.shape[:2], np.float32)
        for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
            k = np.roll(known, (dy, dx), (0, 1)); v = np.roll(out, (dy, dx), (0, 1))
            acc += v * k[..., None]; cnt += k
        new = (~known) & (cnt > 0)
        out[new] = acc[new] / cnt[new][:, None]; known = known | new
    return out
def rgba(img, m):
    a = np.zeros(img.shape[:2] + (4,), np.float32); a[..., :3] = img; a[..., 3] = m*255; return a
def bb(m):
    ys, xs = np.where(m); return [int(xs.min()), int(ys.min()), int(xs.max())+1, int(ys.max())+1]
def keep_component(m, seed_xy, r=0):
    """keep only the connected part of m that contains (or is nearest to) seed_xy"""
    ys, xs = np.where(m)
    if not len(xs): return m
    k = np.argmin((xs - seed_xy[0])**2 + (ys - seed_xy[1])**2)
    x0, x1, y0, y1 = xs.min(), xs.max()+1, ys.min(), ys.max()+1
    sub = dilate(m, r)[y0:y1, x0:x1] if r else m[y0:y1, x0:x1]
    seed = np.zeros(sub.shape, bool); seed[ys[k]-y0, xs[k]-x0] = True
    c = flood(sub, seed)
    out = np.zeros_like(m); out[y0:y1, x0:x1] = c & m[y0:y1, x0:x1]; return out
