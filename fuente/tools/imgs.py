"""Product photos: square webp for the card + a 32px version for the print-in.
Jobs (id starts with job-) get a 4:5 webp instead. Run: python3 -I tools/imgs.py [ids...]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from photos import PHOTOS
from PIL import Image, ImageOps, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'p')
os.makedirs(OUT, exist_ok=True)

def crop(im, ar, fx, fy, zoom):
    w, h = im.size
    cw = min(w, h * ar); ch = cw / ar
    cw, ch = cw / zoom, ch / zoom
    x0 = min(max(fx * w - cw / 2, 0), w - cw); y0 = min(max(fy * h - ch / 2, 0), h - ch)
    return im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch)))

ids = sys.argv[1:] or list(PHOTOS)
for k in ids:
    src, fx, fy, zoom = PHOTOS[k]
    im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    if k.startswith('job-'):
        c = crop(im, 4 / 5, fx, fy, zoom).resize((720, 900), Image.LANCZOS)
        c.save(os.path.join(OUT, k + '.webp'), 'WEBP', quality=78, method=6)
    else:
        c = crop(im, 1, fx, fy, zoom)
        c.resize((600, 600), Image.LANCZOS).save(os.path.join(OUT, k + '.webp'), 'WEBP', quality=76, method=6)
        c.resize((32, 32), Image.BOX).quantize(colors=24).convert('RGB').save(os.path.join(OUT, k + '-px.png'), optimize=True)
print('ok', len(ids))
