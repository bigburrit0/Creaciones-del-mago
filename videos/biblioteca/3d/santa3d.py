"""Papá Noel de verano in 3D toon, built to the approved model sheet (biblioteca/sheets/papa_noel_model.png).

  EGL_PLATFORM=surfaceless /opt/bpy/bin/python santa3d.py -- OUT.glb [PREVIEW_DIR]

A round, jolly Santa dressed for an Uruguayan summer:
- Santa hat with a white fur band and a pompom flopping to the side, small round sunglasses, rosy sunburnt cheeks;
- a big beard draped over a white tank top and belly;
- the red jacket tied around the waist (knot, sleeves hanging, fur trims), red shorts with white fur trim, bare legs,
  black flip-flops.
~3.2 heads tall, a little taller and much rounder than El Mago. Same skeleton, clips and techniques (toonchar.py).
Extra bones: hat.1-3 (floppy hat spring), beard.1-2, belly (jiggle), glasses (they slide down the nose), brows.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: F401  (registers mathutils)
from mathutils import Vector
import toonchar as T

args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = args[0] if args else "santa.glb"; PREV = args[1] if len(args) > 1 else None

SP = 0.58
SHAPE = {
    "DEF-hips": ((1, 0.4, 0.39), 0.6),
    "DEF-thigh": ((1.0, 0.4, 0.5), 0.45), "DEF-shin": (0.45, 0.3), "DEF-foot": (0.3, 0.62), "DEF-toe": (0.62, 0.5),
    "DEF-spine.001": (SP, SP), "DEF-spine.002": (SP, SP), "DEF-spine.003": (SP, SP),
    "DEF-neck": (SP, 0.3), "DEF-head": (0.3, 1.0),
    "DEF-shoulder": ((1.1, 0.5, 0.55), 1.0), "DEF-upper_arm": ((1.05, 0.3, 0.5), 0.55), "DEF-forearm": (0.55, 0.48),
    "DEF-hand": (0.48, 0.9),
}
EXTRA = [("hat.1", (0, 0.01, 0.97), (0.01, 0.05, 1.11), "DEF-head"), ("hat.2", (0.01, 0.05, 1.11), (0.12, 0.1, 1.2), "hat.1"),
         ("hat.3", (0.12, 0.1, 1.2), (0.24, 0.12, 1.06), "hat.2"),
         ("beard.1", (0, -0.24, 0.74), (0, -0.28, 0.6), "DEF-spine.003"), ("beard.2", (0, -0.28, 0.6), (0, -0.29, 0.5), "beard.1"),
         ("belly", (0, -0.12, 0.47), (0, -0.26, 0.47), "DEF-spine.001"),
         ("glasses", (0, -0.15, 0.87), (0, -0.15, 0.9), "DEF-head"), ("brows", (0, -0.14, 0.915), (0, -0.14, 0.94), "DEF-head")]
arm, B = T.setup(SHAPE, 0.39, EXTRA)
T.materials(dict(shirt="#FBF4E4", red="#C0392B", red_dark="#7A1E22", fur="#FBF4E4", skin="#F0C090", sunburn="#E1867A",
                 beard="#FBF4E4", lens="#150A34", glint="#FFFFFF", frame="#2E2160", flop="#150A34", knot="#C0392B"))
print("hips", B["DEF-hips"][0].z, "knee", B["DEF-shin.L"][0].z, "ankle", B["DEF-foot.L"][0].z, "shoulder", B["DEF-upper_arm.L"][0],
      "hand", B["DEF-hand.L"][0], "head", B["DEF-head"][0].z)
front = lambda a: max(0.0, -math.sin(a))                     # 1 at the front (-Y), 0 at the sides and back

# ---- torso: tank top over a big round belly (front bulge), a little asymmetry
belly_w = lambda a, z: 1 + 0.16 * front(a) ** 1.6 * math.exp(-((z - 0.49) / 0.09) ** 2) + 0.004 * math.sin(3 * a + 1)
torso = T.lathe("shirt", [(0.19, 0.35), (0.235, 0.39), (0.258, 0.45), (0.262, 0.52), (0.25, 0.58), (0.225, 0.635), (0.18, 0.675),
                          (0.11, 0.7), (0.05, 0.71)], "shirt", sy=0.88, wob=belly_w)
T.displace(torso, 0.003, 8, seed=2)
# ---- the jacket tied around the waist: band, back flap, fur trims, front knot and hanging sleeves
wr_ = lambda a, z: belly_w(a, z) * 1.0
band = T.lathe("jacket", [(0.236, 0.335), (0.262, 0.345), (0.27, 0.38), (0.262, 0.43), (0.24, 0.44)], "red", sy=0.88, caps=(False, False),
               wob=lambda a, z: belly_w(a, z) * (1 + 0.02 * math.sin(6 * a)),
               zwob=lambda a, j: (-0.09 * max(0.0, math.sin(a)) ** 1.5) if j == 0 else 0.0)          # the back flap hangs lower
T.lathe("fur_top", [(0.24, 0.43), (0.262, 0.436), (0.262, 0.452), (0.24, 0.458)], "fur", sy=0.88, caps=(False, False),
        wob=lambda a, z: belly_w(a, z) * (1 + 0.025 * math.sin(9 * a)))
kn = Vector((0.07, -0.266, 0.392))                          # knot off-centre; the two sleeves hang at different lengths
T.ellipsoid("knot", kn, (0.058, 0.04, 0.046), "knot", 14, 8, wob=lambda c: 1 + 0.08 * math.sin(c.x * 60) * math.sin(c.z * 50))
for s, tail in ((1, [(0.02, 0, -0.012), (0.052, -0.012, -0.06), (0.068, -0.006, -0.105)]), (-1, [(-0.02, 0, -0.012), (-0.045, -0.014, -0.085), (-0.058, -0.008, -0.175)])):
    side = "L" if s > 0 else "R"; pts = [kn + Vector(t) for t in tail]
    T.tube("tail." + side, pts, [0.03, 0.034, 0.036], "red", 12)
    end = pts[-1]; dvec = (pts[-1] - pts[-2]).normalized()
    T.tube("tailfur." + side, [end - dvec * 0.01, end + dvec * 0.03], [0.043, 0.042], "fur", 12)
# ---- shorts: seat plus two legs ending in fur trims
T.lathe("shorts", [(0.2, 0.26), (0.235, 0.3), (0.245, 0.34)], "red", sy=0.88, caps=(True, False))
for s, side in ((1, "L"), (-1, "R")):
    th = B["DEF-thigh." + side][0]; kn_ = B["DEF-shin." + side][0]; an = B["DEF-foot." + side][0]; toe = B["DEF-toe." + side][1]
    T.tube("shortleg." + side, [(th.x * 1.25, th.y, 0.33), (th.x * 1.3, th.y, 0.26), (th.x * 1.3, th.y, 0.205)], [0.12, 0.118, 0.112], "red", 16)
    T.tube("legfur." + side, [(th.x * 1.3, th.y, 0.215), (th.x * 1.3, th.y, 0.188)], [0.122, 0.12], "fur", 16, wob=lambda i, a: 1 + 0.03 * math.sin(8 * a))
    T.tube("leg." + side, [(kn_.x, kn_.y, 0.215), (kn_.x, kn_.y, kn_.z), ((kn_.x + an.x) / 2, an.y, 0.11), (an.x, an.y, an.z + 0.01)],
           [0.062, 0.058, 0.056, 0.045], "skin", 14, wob=lambda i, a: 1 + (0.08 if i == 2 else 0) * max(0.0, math.sin(a)))      # calves
    c = Vector(((an.x + toe.x) / 2, (an.y + toe.y) / 2 - 0.01, 0.0))
    T.ellipsoid("foot." + side, c + Vector((0, 0, 0.032)), (0.05, 0.085, 0.032), "skin", 16, 8)
    T.ellipsoid("flop." + side, c + Vector((0, -0.006, 0.008)), (0.064, 0.105, 0.01), "flop", 16, 6)
    T.tube("strap." + side, [c + Vector((-0.045, 0.02, 0.012)), c + Vector((0, -0.05, 0.05)), c + Vector((0.045, 0.02, 0.012))], [0.009, 0.01, 0.009], "flop", 8)
# ---- bare chubby arms, mitten hands (rest T-pose along X)
for s, side in ((1, "L"), (-1, "R")):
    sh = B["DEF-upper_arm." + side][0]; el = B["DEF-forearm." + side][0]; wr = B["DEF-hand." + side][0]
    T.tube("arm." + side, [sh - Vector((s * 0.04, 0, 0)), sh, (sh + el) / 2, el, (el + wr) / 2, wr], [0.07, 0.072, 0.07, 0.058, 0.056, 0.048], "skin", 16,
           wob=lambda i, a: 1 + (0.06 if i == 2 else 0) * max(0.0, math.sin(a + 1.0)))
    hc = wr + Vector((s * 0.042, -0.004, 0))
    T.ellipsoid("hand." + side, hc, (0.05, 0.042, 0.047), "skin", 14, 8)
    T.ellipsoid("thumb." + side, hc + Vector((-s * 0.014, -0.035, 0.014)), (0.019, 0.019, 0.019), "skin", 8, 6)
# ---- head and face: sunglasses, sunburnt nose and cheeks, bushy brows, big mustache
HEADC = Vector((0, -0.005, 0.85))
head = T.ellipsoid("head", HEADC, (0.162, 0.152, 0.16), "skin", 24, 14)
T.ellipsoid("nose", (0, -0.163, 0.84), (0.04, 0.033, 0.034), "sunburn", 14, 8)
for s in (1, -1):
    T.ellipsoid("cheek", (s * 0.085, -0.13, 0.828), (0.036, 0.013, 0.024), "sunburn", 10, 6)
    T.ellipsoid("lens", (s * 0.05, -0.155, 0.872), (0.032, 0.008, 0.03), "lens", 16, 8)
    T.ellipsoid("lglint", (s * 0.05 + 0.012, -0.164, 0.882), (0.008, 0.002, 0.006), "glint", 8, 4)
    T.tube("rim", [(s * 0.05 + 0.033, -0.153, 0.872), (s * 0.15, -0.06, 0.885), (s * 0.158, 0.02, 0.88)], [0.006, 0.006, 0.006], "frame", 6)
    T.ellipsoid("brow", (s * 0.055, -0.145, 0.915), (0.038, 0.016, 0.014), "beard", 10, 6)
    T.ellipsoid("mustache", (s * 0.045, -0.166, 0.81), (0.056, 0.028, 0.026), "beard", 12, 6,
                wob=lambda c, s=s: 1 + 0.25 * max(0.0, c.x * s) * max(0.0, -c.z))
T.tube("bridge", [(-0.02, -0.162, 0.878), (0.02, -0.162, 0.878)], [0.006, 0.006], "frame", 6)
T.lathe("hair", [(0.158, 0.8), (0.17, 0.85), (0.168, 0.9), (0.152, 0.94)], "beard", sy=0.95, caps=(False, False),
        wob=lambda a, z: (0.0 if math.sin(a) < -0.4 else 1.0) * (1 + 0.06 * math.sin(7 * a)))
# ---- Santa hat: fur band, red cone flopping to the side and back, pompom
T.tube("hatband", [(0, 0.0, 0.925), (0, 0.003, 0.985)], [0.178, 0.17], "fur", 24, wob=lambda i, a: 1 + 0.035 * math.sin(7 * a + 1))
hp = [(0, 0.004, 0.975), (0.004, 0.02, 1.06), (0.025, 0.05, 1.13), (0.07, 0.08, 1.18), (0.13, 0.1, 1.195), (0.19, 0.115, 1.165), (0.225, 0.12, 1.11), (0.24, 0.12, 1.07)]
T.tube("hatcone", hp, [0.162, 0.13, 0.1, 0.075, 0.055, 0.04, 0.03, 0.022], "red", 20,
       wob=lambda i, a: 1 - 0.06 * math.exp(-((i - 3.5) / 1.0) ** 2) * (0.5 + 0.5 * math.cos(2 * a)))
T.ellipsoid("pompom", (0.245, 0.12, 1.035), (0.052, 0.052, 0.052), "fur", 14, 10, wob=lambda c: 1 + 0.06 * math.sin(c.x * 20) * math.sin(c.z * 17))

# ---- beard draped over the chin, chest and upper belly
LOCKS, DOM = 5, -0.12
def lockf(u):
    x = (u + 1) / 2 * LOCKS; return math.cos(math.pi * (x - math.floor(x) - 0.5)) ** 2
def bplace(u, v):
    ztop = 0.815 + 0.06 * u * u
    zbot = 0.53 + 0.12 * u * u - 0.025 * lockf(u) - 0.03 * math.exp(-((u - DOM) / 0.2) ** 2)
    return u * (1.25 - 0.3 * v), ztop + (zbot - ztop) * (v ** 0.95)      # stays on the front: the arms hang free at the sides
def bthick(u, v):
    return 0.075 * max(0.0, 1 - abs(u) ** 3) ** 0.6 * (0.5 + 0.5 * math.sin(math.pi * min(1.0, 0.1 + v * 1.3))) * (0.8 + 0.2 * lockf(u))
T.drape("beard", [torso, head], "beard", 23, 16, bplace, bthick, lambda u, v: 0.025 * max(0.0, v - 0.55) ** 2 * 4 * (1 - abs(u)))

# ---- weights
def w_torso(p):
    torso_b = ["DEF-hips", "DEF-spine.001", "DEF-spine.002", "DEF-spine.003"]
    ws = sorted(((1.0 / (T.seg_dist(p, *B[n]) ** 3 + 1e-7), n) for n in torso_b), reverse=True)[:2]; tot = sum(w for w, _ in ws)
    bel = 0.55 * T.smooth01(-0.15, -0.26, p.y) * math.exp(-((p.z - 0.49) / 0.1) ** 2)
    out = {n: (w / tot) * (1 - bel) for w, n in ws}; out["belly"] = bel; return out
def w_beard(p):
    up = T.smooth01(0.74, 0.8, p.z); low = 1 - up; mid = T.smooth01(0.55, 0.7, p.z)
    return {"DEF-head": up, "DEF-spine.003": low * mid, "DEF-spine.002": low * (1 - mid) * 0.5, "belly": low * (1 - mid) * 0.3,
            "beard.1": low * 0.3 * T.smooth01(0.74, 0.6, p.z), "beard.2": low * 0.5 * T.smooth01(0.62, 0.5, p.z)}
for o in list(T.ST["parts"]):
    n = o.name.split(".")[0]; side = o.name.split(".")[1] if "." in o.name and o.name.split(".")[1] in ("L", "R") else None
    if n in ("head", "nose", "cheek", "mustache", "hair", "hatband"): T.skin(o, ["DEF-head"])
    elif n in ("lens", "lglint", "rim", "bridge"): T.skin(o, ["glasses"])
    elif n == "brow": T.skin(o, ["brows"])
    elif n == "hatcone": T.skin(o, ["DEF-head", "hat.1", "hat.2", "hat.3"], 3); T.smooth_weights(o, 3)
    elif n == "pompom": T.skin(o, ["hat.3"])
    elif n == "beard": T.skin_fn(o, w_beard); T.smooth_weights(o, 2)
    elif n == "shirt": T.skin_fn(o, w_torso); T.smooth_weights(o, 2)
    elif n in ("jacket", "fur_top", "knot", "tail", "tailfur"): T.skin(o, ["DEF-hips", "DEF-spine.001"], 3)
    elif n == "shorts": T.skin(o, ["DEF-hips", "DEF-thigh.L", "DEF-thigh.R"], 3); T.smooth_weights(o, 2)
    elif n in ("shortleg", "legfur"): T.skin(o, ["DEF-hips", "DEF-thigh." + side], 2); T.smooth_weights(o, 2)
    elif n == "leg": T.skin(o, ["DEF-thigh." + side, "DEF-shin." + side, "DEF-foot." + side], 3); T.smooth_weights(o, 3)
    elif n in ("foot", "flop", "strap"): T.skin(o, ["DEF-foot." + side, "DEF-toe." + side], 3, 2)
    elif n == "arm": T.skin(o, ["DEF-upper_arm." + side, "DEF-forearm." + side, "DEF-hand." + side], 4); T.smooth_weights(o, 4)
    elif n in ("hand", "thumb"): T.skin(o, ["DEF-hand." + side])
# the beard rests on the chin, tank top and belly: every point takes the weights of the surface under it (the chin
# part follows the head, the rest the body and the belly jiggle), so it never sinks in whatever the pose
beard = next(o for o in T.ST["parts"] if o.name.split(".")[0] == "beard")
T.transfer_weights(beard, [o for o in T.ST["parts"] if o.name.split(".")[0] in ("shirt", "head", "cheek")], lambda p: 1.0)
T.smooth_weights(beard, 1)
T.bind_all()
static = [o for o in T.ST["parts"] if o.name.split(".")[0] not in ("arm", "hand", "thumb", "lens", "lglint", "rim", "bridge")]
T.bake_ao(static, static)
T.export(OUT)
if PREV:
    r = math.radians
    T.preview(PREV, [("front_rest", (0, -5, 0.68), (r(90), 0, 0), None, 0), ("side_rest", (5, 0, 0.68), (r(90), 0, r(90)), None, 0),
                     ("q_rest", (3.6, -3.6, 1.7), (r(76), 0, r(45)), None, 0), ("front_idle", (0, -5, 0.68), (r(90), 0, 0), "Idle_Loop", 10),
                     ("q_walk", (3.5, -3.5, 1.5), (r(78), 0, r(45)), "Walk_Loop", 8), ("sit", (2.5, -4.2, 0.9), (r(84), 0, r(30)), "Sitting_Idle_Loop", 10)])
