import sys, json
from PIL import Image, ImageFilter
import numpy as np
SRC, OUT = sys.argv[1], sys.argv[2]
L = lambda i: np.asarray(Image.open(f'{SRC}/{i}.jpg').convert('RGB')).astype(np.float32)
i1, i2, i3, i4 = L(1), L(2), L(3), L(4)
H, W = i1.shape[:2]

def dilate(m, r):
    return np.asarray(Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(2*r+1))) > 127
def box(m, x0, y0, x1, y1):
    z = np.zeros_like(m); z[y0:y1, x0:x1] = m[y0:y1, x0:x1]; return z
def diff(a, b): return np.abs(a-b).sum(2)

# ---- B: broken handle, colour (img1 + patches from img3, colour-matched)
d13 = diff(i1, i3) > 70
patch = box(d13, 565, 975, 690, 1320) | box(d13, 345, 1385, 690, 1560)
patch = dilate(patch, 6)
ring = dilate(patch, 20) & ~patch
gain = i1[ring].mean(0) / np.maximum(i3[ring].mean(0), 1)
i3c = np.clip(i3 * gain, 0, 255)
alpha = np.asarray(Image.fromarray((patch*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3)), np.float32)[..., None]/255
B = i1*(1-alpha) + i3c*alpha
ph = dilate(box(d13, 565, 975, 690, 1320), 6)
ah = np.asarray(Image.fromarray((ph*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3)), np.float32)[..., None]/255
N = i1*(1-ah) + i3c*ah

# ---- sprites
def sat(a): return a.max(2)-a.min(2)
def lum(a): return a.mean(2)
def sprite(src, ref, thr, bx, keep=None):
    m = box(diff(src, ref) > thr, *bx)
    if keep is not None: m &= keep
    m = np.asarray(Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5))) > 127
    m = dilate(m, 1)
    rgba = np.zeros((H, W, 4), np.float32); rgba[..., :3] = src; rgba[..., 3] = m*255
    return rgba, m
gray_handle, gm = sprite(i1, B, 60, (570, 975, 690, 1310), (sat(i1) < 45) & (lum(i1) < 150))
gold_handle, om = sprite(i4, B, 60, (570, 975, 690, 1310), ((i4[...,0]>140)&(i4[...,2]<120)) | (lum(i4) < 95))
steam, sm = sprite(i4, i1, 30, (640, 940, 760, 1235), (sat(i4) < 40) & (lum(i4) > 95))
gulls, um = sprite(i4, i1, 40, (860, 490, 1100, 640))
core = np.asarray(Image.fromarray((um*255).astype(np.uint8)).filter(ImageFilter.MinFilter(7)).filter(ImageFilter.MaxFilter(25))) > 127
um = um & core; gulls[..., 3] = um*255
D = i4.copy(); D[dilate(sm,3)] = i1[dilate(sm,3)]; D[dilate(um,3)] = i1[dilate(um,3)]

def bb(m):
    ys, xs = np.where(m); return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
meta = {'gray_handle': bb(gm), 'gold_handle': bb(om), 'steam': bb(sm), 'gulls': bb(um)}
# split gulls into two by x gap
xs = np.where(um.any(0))[0]; gaps = np.where(np.diff(xs) > 8)[0]
split = int(xs[gaps[0]]+4) if len(gaps) else 990
g1 = gulls.copy(); g1[:, split:, 3] = 0
g2 = gulls.copy(); g2[:, :split, 3] = 0
meta['gull1'] = bb(um & (np.arange(W)[None, :] < split)); meta['gull2'] = bb(um & (np.arange(W)[None, :] >= split))
# split gray handle into two pieces (top / bottom)
cy = (meta['gray_handle'][1] + meta['gray_handle'][3])//2
ht = gray_handle.copy(); ht[cy:, :, 3] = 0
hb = gray_handle.copy(); hb[:cy, :, 3] = 0
meta['handle_top'] = bb(gm & (np.arange(H)[:, None] < cy)); meta['handle_bot'] = bb(gm & (np.arange(H)[:, None] >= cy))

# ---- waves: row displacement inside the sea band
yy, xx = np.mgrid[0:H, 0:W]
wall = 822 + (xx/W)*95          # top of the stone wall
sea = (yy >= 706) & (yy < wall) & ~((xx > 425) & (xx < 615) & (yy > 795))
def waves(img, k):
    out = img.copy()
    px = 6
    for y in range(706, 960):
        s = int(round(np.sin(2*np.pi*(k/4 + (y-706)/38.0)) * 1.0)) * px * (1 + (y-706)//90)
        row = np.roll(img[y], s, axis=0)
        msk = sea[y]
        out[y][msk] = row[msk]
    return out

# ---- output: scale to 1080 wide, crop to 1920
OW, OH = 1080, 1920
sc = OW / W; nh = round(H*sc); top = (nh-OH)//2
def save(arr, name, rgba=False, nearest=False):
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), 'RGBA' if rgba else 'RGB')
    im = im.resize((OW, nh), Image.NEAREST if nearest else Image.LANCZOS).crop((0, top, OW, top+OH))
    if name.startswith('w'): im = im.crop((0, round(706*sc-top), OW, round(960*sc-top)))
    im.save(f'{OUT}/{name}.png' if rgba or name.startswith('w') else f'{OUT}/{name}.jpg', quality=95)
save(i1, 'k1'); save(i2, 'k2'); save(i4, 'k4'); save(B, 'broken'); save(N, 'nohandle'); save(D, 'fixed')
for k in range(4):
    save(waves(B, k), f'wc{k}'); save(waves(i2, k), f'wg{k}'); save(waves(D, k), f'wf{k}')
for n, a in [('handle_top', ht), ('handle_bot', hb), ('gold', gold_handle), ('steam', steam), ('gull1', g1), ('gull2', g2)]:
    save(a, n, rgba=True, nearest=True)
# sea mask as png band (for cropping wave layers)
for k in meta: meta[k] = [round(meta[k][0]*sc), round(meta[k][1]*sc - top), round(meta[k][2]*sc), round(meta[k][3]*sc - top)]
meta['sea_y'] = [round(706*sc-top), round(960*sc-top)]
json.dump(meta, open(f'{OUT}/meta.json', 'w'), indent=1); print(json.dumps(meta))
