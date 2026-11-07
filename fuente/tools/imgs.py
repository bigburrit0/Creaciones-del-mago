"""Product photos: square webp for the card + a 32px version for the print-in.
Jobs (id starts with job-) get a 4:5 webp instead. Run: python3 -I tools/imgs.py [ids...]

Phone photos (flag "m" in photos.py) get a light, honest touch-up before the crop is
resized: white balance from the near-neutral pixels, levels, a small midtone lift and a
mild sharpen. Nothing is added or removed from the object.

If an edited version of a source photo exists in fuente/fotos/ia/ (same base name,
.png, .jpg or .webp, same framing as the original), it is used instead and the
touch-up is skipped. That is where the AI-edited photos go (see IMAGENES-ANTIGRAVITY.md).
Gallery photos (flag "g") only get the big webp, not the 32px version."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from photos import PHOTOS
from PIL import Image, ImageOps, ImageFile, ImageFilter
import numpy as np
ImageFile.LOAD_TRUNCATED_IMAGES = True
# assets/ next to fuente/ (the repo) unless the build folder has its own copy
BASE = os.path.join(HERE, '..') if os.path.isdir(os.path.join(HERE, '..', 'assets')) else os.path.join(HERE, '..', '..')
OUT = os.path.join(BASE, 'assets', 'p')
IA = os.path.join(HERE, '..', 'fotos', 'ia')

def crop(im, ar, fx, fy, zoom):
    w, h = im.size
    cw = min(w, h * ar); ch = cw / ar
    cw, ch = cw / zoom, ch / zoom
    x0 = min(max(fx * w - cw / 2, 0), w - cw); y0 = min(max(fy * h - ch / 2, 0), h - ch)
    return im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch)))

def ai_version(src):
    base = os.path.splitext(os.path.basename(src))[0]
    for ext in ('.png', '.jpg', '.jpeg', '.webp'):
        p = os.path.join(IA, base + ext)
        if os.path.exists(p): return p
    return None

def touch_up(im):
    """White balance on near-neutral pixels (the red table or a colored piece does not
    count), levels from the 0.5/99.5 percentiles, a small midtone lift if it is dark."""
    a = np.asarray(im, dtype=np.float32) / 255.0
    mx, mn = a.max(axis=2), a.min(axis=2)
    lum = a @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    chroma = (mx - mn) / np.maximum(mx, 1e-3)
    lo, hi = np.percentile(lum, 40), np.percentile(lum, 99)
    neutral = (chroma < 0.14) & (lum > lo) & (lum < hi)
    if neutral.sum() > a.shape[0] * a.shape[1] * 0.02:
        m = a[neutral].mean(axis=0)
        gain = np.clip(m.mean() / np.maximum(m, 1e-3), 0.85, 1.18)
        a = a * (1 + 0.75 * (gain - 1))
    lum = a @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    p_lo, p_hi = np.percentile(lum, 0.5), np.percentile(lum, 99.5)
    p_lo, p_hi = min(p_lo, 0.08), max(p_hi, 0.85)
    a = (a - p_lo) / (p_hi - p_lo)
    a = np.clip(a, 0, 1)
    med = float(np.median(a @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)))
    if med < 0.42:
        g = np.clip(np.log(0.42) / np.log(max(med, 1e-3)), 0.78, 1.0)
        g = 1 - 0.6 * (1 - g)
        a = a ** g
    return Image.fromarray((a * 255 + 0.5).astype(np.uint8))

def sharpen(im):
    return im.filter(ImageFilter.UnsharpMask(radius=1.1, percent=55, threshold=3))

ids = sys.argv[1:] or [k for k in PHOTOS if os.path.exists(PHOTOS[k][0]) or ai_version(PHOTOS[k][0])]
os.makedirs(OUT, exist_ok=True)
for k in ids:
    src, fx, fy, zoom = PHOTOS[k][:4]
    flags = PHOTOS[k][4] if len(PHOTOS[k]) > 4 else ''
    ai = ai_version(src)
    im = ImageOps.exif_transpose(Image.open(ai or src)).convert('RGB')
    if k.startswith('job-'):
        c = crop(im, 4 / 5, fx, fy, zoom).resize((720, 900), Image.LANCZOS)
        c.save(os.path.join(OUT, k + '.webp'), 'WEBP', quality=78, method=6)
        continue
    c = crop(im, 1, fx, fy, zoom)
    if 'm' in flags and not ai: c = touch_up(c)
    big = c.resize((600, 600), Image.LANCZOS)
    if 'm' in flags and not ai: big = sharpen(big)
    big.save(os.path.join(OUT, k + '.webp'), 'WEBP', quality=76, method=6)
    if 'g' not in flags:
        c.resize((32, 32), Image.BOX).quantize(colors=24).convert('RGB').save(os.path.join(OUT, k + '-px.png'), optimize=True)
    print(k, '(IA)' if ai else '')
print('ok', len(ids))
