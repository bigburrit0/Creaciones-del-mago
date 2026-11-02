"""Build HyperFrames assets for the garden video from keyframes 1..4.jpg.
L layout = 1.jpg (seed), 2.jpg (tree), 3.jpg (feeder); final layout = 4.jpg (wizard sitting).
Variable names keep the original numbering: i6 = keyframe 1, i7 = 2, i8 = 3, i5 = 4."""
import sys, json, os
sys.path.insert(0, os.path.dirname(__file__))
from garden_lib import *
SRC, OUT = sys.argv[1], sys.argv[2]
DBG = sys.argv[3] if len(sys.argv) > 3 else None
# keyframes: 1 = seed, 2 = young tree, 3 = feeder, 4 = wizard sitting (final)
i6, i7, i8, i5 = [load(SRC, i) for i in (1, 2, 3, 4)]
H, W = i6.shape[:2]
meta = {}

# ---------- clean plate of the L layout
# everything left of x=400 and right of x=800 is clean in keyframe 1 (6.jpg); the centre is rebuilt:
#   wall rows from keyframe 2 (7.jpg, the young tree starts below the wall),
#   the shadow/sand band row by row from a clean column, the plots copied from the plot one or two cells to the right.
P = i6.copy()
kneel_box = (400, 590, 800, 1228)
yy, xx = np.mgrid[0:H, 0:W]
wallR = (xx >= 400) & (xx < 800) & (yy >= 590) & (yy < 790)
P[wallR] = i7[wallR]
cen = (xx >= 400) & (xx < 830) & (yy >= 790) & (yy < 1228)
plots = cen & (yy >= 992)
med = np.median(np.stack([i6, i7, i8]), 0)          # kneeling wizard (6), sparkles (7), hornero (8) each appear once
P[plots] = med[plots]
# plot pitch is ~175 px. Top row under the canopy/feeder/hat: copy from two cells to the right;
# trunk and planted-soil patch (present in 7 and 8): copy from one cell to the right.
z1 = plots & (yy < 1068) & (xx >= 440) & (xx < 700)
ys, xs = np.where(z1); P[ys, xs] = i7[ys, np.where(xs < 620, xs + 350, xs + 175)]
z2 = plots & (yy >= 1068) & (xx >= 480) & (xx < 660)
ys, xs = np.where(z2); P[ys, xs] = i7[ys, xs + 175]
band = cen & ~plots
rowval = np.median(i7[:, 805:842], 1)
ys, xs = np.where(band); P[ys, xs] = rowval[ys]

# folded chair removed (for the "unfold" swap)
cbox = (835, 548, 1116, 1002)
best, bdx = 1e18, 0
for dx in range(120, 420, 2):
    e = diff(P[560:780, 700:835], P[560:780, 700-dx:835-dx]).mean()
    if e < best: best, bdx = e, dx
PN = P.copy()
CB = boxmask(P.shape, *cbox)
shift = np.zeros_like(P); shift[:, bdx:] = P[:, :-bdx]
wall_rows = np.arange(H)[:, None] < 792
chair_w = CB & wall_rows & (diff(P, shift) > 60)
sand = P[930:950, 760:800].reshape(-1, 3).mean(0); teal = P[800:815, 760:800].reshape(-1, 3).mean(0)
ground = CB & ~wall_rows
chair_g = ground & (np.abs(P - sand).sum(2) > 45) & (np.abs(P - teal).sum(2) > 45)
chair = dilate(mf(chair_w | chair_g, ImageFilter.MedianFilter(3)), 4) & CB
yy, xx = np.where(chair & wall_rows); PN[yy, xx] = P[yy, xx - bdx]
PN = inpaint(PN, chair & ~wall_rows, 300)
meta['chair_dx'] = bdx

# ---------- L-layout sprites (difference against the plate)
def dsprite(img, thr, bx, base=P, grow=1, med=5):
    m = box(diff(img, base) > thr, *bx)
    m = mf(m, ImageFilter.MedianFilter(med)); m = dilate(m, grow)
    return m
kneel = dsprite(i6, 40, kneel_box)
stand = dsprite(i7, 40, (90, 970, 520, 1570)) & ~boxmask(i7.shape, 415, 0, W, 1100) & ~boxmask(i7.shape, 480, 1100, W, 1200)
point = dsprite(i8, 40, (90, 970, 520, 1570)) & ~boxmask(i8.shape, 400, 0, W, 1080)
tree = dsprite(i7, 35, (400, 780, 745, 1240))
red8 = (i8[..., 0] > 150) & (i8[..., 1] < 100)
struct8 = dsprite(i8, 35, (330, 600, 720, 1240)) & ~(boxmask(i8.shape, 0, 990, 520, 2000)) & ~dilate(red8, 3)
horn8 = keep_component(dsprite(i8, 40, (780, 950, 1040, 1230)), (900, 1080), r=2)
# kiskadee (flying, image 3): non-lilac part of the left side of the feeder area
lilac = (i8[..., 2] > 170) & (i8[..., 2] > i8[..., 0] + 5) & (i8[..., 0] > 140)
kis = struct8 & boxmask(P.shape, 330, 780, 560, 1060) & ~lilac
kis = erode(dilate(kis, 2), 2)
kis = keep_component(mf(kis, ImageFilter.MedianFilter(5)), (440, 900), r=2)
# feeder = struct8 above the trunk minus the bird, the hole mirrored from the right half
feeder_m = struct8 & ~kis & (np.arange(H)[:, None] < 1082)
feeder_img = i8.copy()
fx = 574
cx = int(round(np.median(np.where(feeder_m & (np.arange(H)[:, None] > 800) & (np.arange(H)[:, None] < 1070))[1])))
fx = cx
hole_m = kis & boxmask(P.shape, 470, 780, 700, 1082)
yy, xx = np.where(hole_m); mx = np.clip(2*fx - xx, 0, W-1)
ok = feeder_m[yy, mx]
feeder_img[yy[ok], xx[ok]] = i8[yy[ok], mx[ok]]; feeder_m[yy[ok], xx[ok]] = True
meta['feeder_cx'] = fx
# split: branch+rope (above feeder top) and feeder box
fy = np.where((feeder_m & (lilac | (lum(i8) < 80))).any(1) & (np.arange(H) > 760))[0]
rope_m = feeder_m & (np.arange(H)[:, None] < 780) & (lum(i8) < 175)
rope_m = keep_component(rope_m, (520, 690), r=4)
box_m = feeder_m & (np.arange(H)[:, None] >= 780) & (np.arange(W)[None, :] >= 470)
canopy = tree & (np.arange(H)[:, None] < 1060)
trunk = tree & (np.arange(H)[:, None] >= 1060)
trunk8 = struct8 & (np.arange(H)[:, None] >= 1060) & ~kis

# ---------- final layout (5.jpg): wand cut-outs
k5 = i5.copy()
sp1 = wand(i5, (338, 1228, 482, 1334), navy=False)
sp2 = wand(i5, (503, 1228, 640, 1334), navy=False)
kis5 = wand(i5, (330, 850, 515, 1020), navy=False)
hor5 = wand(i5, (596, 862, 770, 1000), navy=False)
wiz5 = wand(i5, (700, 878, 1112, 1548), dark=80)
wiz5 &= ~boxmask(i5.shape, 0, 0, 800, 1195)
lawn = (i5[..., 1] > i5[..., 0] + 12) & (i5[..., 1] > i5[..., 2] - 5)
wiz5 &= ~(lawn & (np.arange(H)[:, None] > 1380))
# mate + hands (skin, gourd, straw) inside the sitting wizard
mb = boxmask(i5.shape, 812, 1150, 935, 1292)
purple = (i5[..., 2] > i5[..., 0] + 15) & (i5[..., 2] > 90)
mate = mb & wiz5 & ~purple & (lum(i5) > 50)
mate = erode(dilate(mate, 2), 1) & mb
B5 = inpaint(i5, dilate(sp1 | sp2, 2), 200)
B5 = inpaint(B5, dilate(mate, 1), 200)
# leaves for the sway: green pixels of the canopy over the wall/fence
green = (i5[..., 1] > i5[..., 0] + 15) & (i5[..., 1] > i5[..., 2] + 5)
leaves = green & boxmask(i5.shape, 290, 120, 1000, 545)

# ---------- small drawn sprout (palette taken from the tree)
def sprout_layer():
    a = np.zeros((H, W, 4), np.float32)
    ol = np.array([38, 44, 40, 255.]); g1 = np.array([92, 150, 74, 255.]); g2 = np.array([60, 112, 56, 255.])
    soil = np.array([84, 52, 34, 255.])
    px = 7; bx, by = 562, 1196   # base of the trunk
    def r(x, y, w, h, c): a[by + y*px: by + (y+h)*px, bx + x*px: bx + (x+w)*px] = c
    r(-3, -1, 7, 2, soil)
    r(-1, -6, 2, 6, ol); r(0, -6, 1, 5, g2)
    r(-5, -9, 4, 3, ol); r(-4, -8, 3, 2, g1)
    r(1, -10, 4, 3, ol); r(2, -9, 3, 2, g1)
    r(-1, -8, 2, 2, ol); r(0, -8, 1, 1, g2)
    return a

# ---------- output scaling
OW, OH = 1080, 1920
sc = OW / W; nh = round(H * sc); top = (nh - OH) // 2
def save_rgb(arr, name):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).resize((OW, nh), Image.LANCZOS).crop((0, top, OW, top + OH)).save(f'{OUT}/{name}.jpg', quality=94)
def save_rgba(arr, name):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), 'RGBA').resize((OW, nh), Image.NEAREST).crop((0, top, OW, top + OH)).save(f'{OUT}/{name}.png', optimize=True)
def conv(b): return [round(b[0]*sc), round(b[1]*sc - top), round(b[2]*sc), round(b[3]*sc - top)]
def transplant(img, m, s, dst_anchor, src_anchor):
    """move a sprite from 5.jpg into the L layout: scale s around src_anchor, place at dst_anchor"""
    x0, y0, x1, y1 = bb(m)
    crop = rgba(img, m)[y0:y1, x0:x1]
    im = Image.fromarray(crop.astype(np.uint8), 'RGBA')
    im = im.resize((max(1, round(im.width*s)), max(1, round(im.height*s))), Image.NEAREST)
    canvas = Image.new('RGBA', (W, H))
    ox = round(dst_anchor[0] - (src_anchor[0]-x0)*s); oy = round(dst_anchor[1] - (src_anchor[1]-y0)*s)
    canvas.alpha_composite(im, (ox, oy))
    return np.asarray(canvas).astype(np.float32), [ox, oy, ox+im.width, oy+im.height]

save_rgb(P, 'plate'); save_rgb(PN, 'plate_nochair'); save_rgb(i6, 'k1'); save_rgb(i7, 'k2'); save_rgb(i8, 'k3')
save_rgb(i5, 'k4'); save_rgb(B5, 'k4_base')
for name, img, m in [('kneel', i6, kneel), ('stand', i7, stand), ('point', i8, point), ('canopy', i7, canopy),
                     ('trunk', i7, trunk), ('trunk8', i8, trunk8), ('rope', i8, rope_m), ('feeder', feeder_img, box_m),
                     ('kis_fly', i8, kis), ('hor_fly', i8, horn8),
                     ('f_sp1', i5, sp1), ('f_sp2', i5, sp2), ('f_mate', i5, mate)]:
    save_rgba(rgba(img, m), name); meta[name] = conv(bb(m))
# leaves layer
save_rgba(rgba(i5, leaves), 'f_leaves'); meta['f_leaves'] = conv(bb(leaves))
# sapling = tree at 55 % anchored at trunk base
base_pt = (565, 1198)
tr = rgba(i7, tree)[...]
x0, y0, x1, y1 = bb(tree)
t_im = Image.fromarray(tr[y0:y1, x0:x1].astype(np.uint8), 'RGBA')
t_im = t_im.resize((round(t_im.width*.55), round(t_im.height*.55)), Image.NEAREST)
cv = Image.new('RGBA', (W, H)); cv.alpha_composite(t_im, (round(base_pt[0] - (base_pt[0]-x0)*.55), round(base_pt[1] - (base_pt[1]-y0)*.55)))
save_rgba(np.asarray(cv).astype(np.float32), 'sapling')
save_rgba(sprout_layer(), 'sprout')
# 5.jpg sprites transplanted into the L layout
s_b = 0.80
feeder_bot = int(np.where((box_m & lilac).any(1))[0].max())
meta['feeder_bot'] = conv((0, feeder_bot, 0, feeder_bot))[1]
fb5 = (557, 1004)  # feeder base centre in 5.jpg
def to8(p): return (fx + (p[0]-fb5[0])*s_b, feeder_bot + (p[1]-fb5[1])*s_b)
a, bxx = transplant(i5, kis5, s_b, to8((bb(kis5)[2], bb(kis5)[3])), (bb(kis5)[2], bb(kis5)[3])); save_rgba(a, 'l_kis'); meta['l_kis'] = conv(bxx)
a, bxx = transplant(i5, hor5, s_b, to8((bb(hor5)[0], bb(hor5)[3])), (bb(hor5)[0], bb(hor5)[3])); save_rgba(a, 'l_hor'); meta['l_hor'] = conv(bxx)
a, bxx = transplant(i5, sp1, 0.85, (430, 1300), (bb(sp1)[0]+60, bb(sp1)[3])); save_rgba(a, 'l_sp1'); meta['l_sp1'] = conv(bxx)
a, bxx = transplant(i5, sp2, 0.85, (705, 1300), (bb(sp2)[0]+60, bb(sp2)[3])); save_rgba(a, 'l_sp2'); meta['l_sp2'] = conv(bxx)
wb = bb(wiz5)
a, bxx = transplant(i5, wiz5, 1.0, (1108, 1002), (wb[2], wb[3])); save_rgba(a, 'l_wiz'); meta['l_wiz'] = conv(bxx)
meta['trunk_base'] = conv((565, 1198, 565, 1198))[:2]
meta['f_sp1'] = conv(bb(sp1)); meta['f_sp2'] = conv(bb(sp2))
json.dump(meta, open(f'{OUT}/meta.json', 'w'), indent=1)
print(json.dumps(meta))
if DBG:
    for nm, arr in [('P', P), ('PN', PN), ('B5', B5)]:
        Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(f'{DBG}/{nm}.png')
