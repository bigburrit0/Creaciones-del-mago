"""El Mago in 3D toon (v2): chibi body built to the approved model sheet, on the CC0 Quaternius skeleton reshaped to
chibi proportions, exported as a GLB with all 46 clips and baked contact shading.

  EGL_PLATFORM=surfaceless /opt/bpy/bin/python mago3d.py -- OUT.glb [PREVIEW_DIR]

v2 (videos/RESEARCH_3D_FORMS.md): the beard DRAPES over the chest, belly and belt (shell projected onto the body, thin at
the edges, 6 tapered locks, the dominant one off-centre, the tip lifting off); robe with folds that fade upward and a
scalloped hem; hat with dents at the bend, tip leaning, wavy brim, thicker band; belt sized from the robe; cuffs;
flared boots; seeded surface noise; smoothed joint weights; ambient occlusion baked into vertex colours.
Units: metres, Z up, facing -Y (glTF +Z).
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: F401  (registers mathutils)
from mathutils import Vector
import toonchar as T

args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = args[0] if args else "mago.glb"; PREV = args[1] if len(args) > 1 else None

SPINE = 0.56
SHAPE = {
    "DEF-hips": ((1, 0.4, 0.327), 0.6),
    "DEF-thigh": ((0.85, 0.4, 0.5), 0.35), "DEF-shin": (0.35, 0.25), "DEF-foot": (0.25, 0.6), "DEF-toe": (0.6, 0.45),
    "DEF-spine.001": (SPINE, SPINE), "DEF-spine.002": (SPINE, SPINE), "DEF-spine.003": (SPINE, SPINE),
    "DEF-neck": (SPINE, 0.3), "DEF-head": (0.3, 1.0),
    "DEF-shoulder": ((1, 0.5, 0.55), 0.9), "DEF-upper_arm": ((0.93, 0.3, 0.5), 0.47), "DEF-forearm": (0.47, 0.40),
    "DEF-hand": (0.40, 0.8),
}
EXTRA = [("hat.1", (0, 0.0, 0.91), (0, 0.04, 1.07), "DEF-head"), ("hat.2", (0, 0.04, 1.07), (0, 0.18, 1.17), "hat.1"),
         ("hat.3", (0, 0.18, 1.17), (0, 0.27, 1.08), "hat.2"),
         ("beard.1", (0, -0.21, 0.66), (0, -0.23, 0.52), "DEF-spine.003"), ("beard.2", (0, -0.23, 0.52), (0, -0.22, 0.38), "beard.1"),
         ("eyes", (0, -0.13, 0.802), (0, -0.13, 0.84), "DEF-head"), ("brows", (0, -0.13, 0.838), (0, -0.13, 0.87), "DEF-head")]
arm, B = T.setup(SHAPE, 0.32, EXTRA)
T.materials(dict(robe="#6A58B8", robe_dark="#4B3A8E", hat="#6A58B8", band="#F2C14E", skin="#F0C090", cheek="#E1867A",
                 beard="#FBF4E4", eye="#150A34", glint="#FFFFFF", belt="#6E3B22", buckle="#F2C14E", boot="#5A3424", sole="#2E2160"))

# ---- robe: stocky barrel, folds fading up from the hem, scalloped hem, slight asymmetry
fold = lambda a, z: 1 + (0.03 * math.sin(4 * a + 0.7 * math.sin(2 * a + 1.3)) + 0.012 * math.sin(9 * a + 2)) * T.smooth01(0.42, 0.12, z) \
                      + 0.006 * math.sin(a + 0.4)
robe = T.lathe("robe", [(0.203, 0.115), (0.222, 0.128), (0.217, 0.2), (0.211, 0.3), (0.208, 0.4), (0.198, 0.5),
                        (0.175, 0.58), (0.13, 0.64), (0.06, 0.67)], "robe", sy=0.86, wob=fold,
               zwob=lambda a, j: (0.011 * math.sin(5 * a + 0.7) - 0.004) if j <= 1 else 0.0)
T.displace(robe, 0.003, 9, seed=1)
# ---- belt hugs the robe (radius from the profile at belt height), thicker than fabric; buckle projects
rb = 0.209
belt = T.lathe("belt", [(rb - 0.002, 0.33), (rb + 0.013, 0.336), (rb + 0.015, 0.36), (rb + 0.013, 0.384), (rb - 0.002, 0.39)], "belt", sy=0.86, caps=(False, False))
buckle = T.tube("buckle", [(0, -(rb + 0.015) * 0.86 + 0.004, 0.36), (0, -(rb + 0.015) * 0.86 - 0.016, 0.36)], [0.034, 0.032], "buckle", 4)
# ---- legs and flared boots with a wide toe and a dark sole
for s, side in ((1, "L"), (-1, "R")):
    k = B["DEF-shin." + side][0]; an = B["DEF-foot." + side][0]; toe = B["DEF-toe." + side][1]
    T.tube("leg." + side, [(k.x, k.y, k.z + 0.05), (an.x, an.y, an.z + 0.02)], [0.045, 0.042], "robe_dark", 10)
    T.tube("shaft." + side, [(an.x, an.y + 0.005, 0.035), (an.x, an.y + 0.005, 0.12), (an.x, an.y + 0.005, 0.158)], [0.05, 0.053, 0.064], "boot", 14)
    T.ellipsoid("boot." + side, ((an.x + toe.x) / 2, (an.y + toe.y) / 2 - 0.012, 0.045), (0.058, 0.09, 0.05), "boot", 18, 10,
                wob=lambda c: 1 + 0.12 * max(0.0, -c.y) ** 2)                 # wider toe cap
    T.ellipsoid("sole." + side, ((an.x + toe.x) / 2, (an.y + toe.y) / 2 - 0.012, 0.008), (0.06, 0.094, 0.012), "sole", 16, 6)
# ---- arms (rest T-pose, along X): sleeves with an elbow crease and a darker cuff lip, mitten hands
for s, side in ((1, "L"), (-1, "R")):
    sh = B["DEF-upper_arm." + side][0]; el = B["DEF-forearm." + side][0]; wr = B["DEF-hand." + side][0]
    path = [sh - Vector((s * 0.03, 0, 0)), sh, (sh + el) / 2, el, (el + wr) / 2, wr - Vector((s * 0.008, 0, 0))]
    T.tube("sleeve." + side, path, [0.05, 0.052, 0.05, 0.046, 0.054, 0.06], "robe", 16,
           wob=lambda i, a: 1 - (0.08 if i == 3 else 0) * (0.5 + 0.5 * math.cos(a)))
    T.tube("cuff." + side, [wr - Vector((s * 0.014, 0, 0)), wr + Vector((s * 0.004, 0, 0))], [0.064, 0.066], "robe_dark", 16)
    hc = wr + Vector((s * 0.035, -0.005, 0))
    T.ellipsoid("hand." + side, hc, (0.042, 0.036, 0.04), "skin", 14, 8)
    T.ellipsoid("thumb." + side, hc + Vector((-s * 0.012, -0.03, 0.012)), (0.016, 0.016, 0.016), "skin", 8, 6)
# ---- head and face
HEADC = Vector((0, -0.005, 0.79))
head = T.ellipsoid("head", HEADC, (0.15, 0.14, 0.15), "skin", 24, 14)
T.ellipsoid("nose", (0, -0.15, 0.775), (0.042, 0.035, 0.036), "skin", 14, 8)
for s in (1, -1):
    T.ellipsoid("cheek", (s * 0.075, -0.12, 0.768), (0.032, 0.012, 0.022), "cheek", 10, 6)
    T.ellipsoid("eye", (s * 0.046, -0.136, 0.802), (0.017, 0.01, 0.024), "eye", 12, 8)
    T.ellipsoid("glint", (s * 0.046 + 0.006, -0.146, 0.81), (0.0055, 0.003, 0.0065), "glint", 8, 5)
    T.ellipsoid("brow", (s * 0.05, -0.13, 0.838), (0.032 + 0.003 * s, 0.014, 0.012), "beard", 10, 6)
    T.ellipsoid("mustache", (s * 0.042, -0.152, 0.747), (0.05, 0.026, 0.023), "beard", 12, 6,
                wob=lambda c, s=s: 1 + 0.25 * max(0.0, c.x * s) * max(0.0, -c.z))      # tips curl down and out
T.lathe("hair", [(0.148, 0.75), (0.158, 0.785), (0.156, 0.84), (0.14, 0.87)], "beard", sy=0.95, caps=(False, False),
        wob=lambda a, z: (0.0 if math.sin(a) < -0.45 else 1.0) * (1 + 0.05 * math.sin(7 * a)))
# ---- hat: wavy drooping brim, cone with dents at the bend and the tip leaning to one side, thick band
T.lathe("brim", [(0.06, 0.88), (0.27, 0.873), (0.288, 0.864), (0.272, 0.891), (0.07, 0.9)], "hat", sy=0.97,
        zwob=lambda a, j: (-0.009 * (1 + math.sin(3 * a + 1.1)) - (0.006 if math.sin(a) < -0.5 else 0.0)) if 1 <= j <= 3 else 0.0)
hp = [(0, 0.0, 0.89), (0, 0.008, 0.96), (0.003, 0.035, 1.05), (0.008, 0.09, 1.12), (0.016, 0.16, 1.155), (0.025, 0.225, 1.15),
      (0.032, 0.268, 1.11), (0.034, 0.272, 1.065), (0.03, 0.245, 1.045), (0.026, 0.222, 1.06)]
hr = [0.165, 0.138, 0.108, 0.08, 0.058, 0.042, 0.03, 0.022, 0.016, 0.011]
T.tube("cone", hp, hr, "hat", 20, wob=lambda i, a: 1 - 0.07 * math.exp(-((i - 4.5) / 1.1) ** 2) * (0.5 + 0.5 * math.cos(2 * a + 0.5)))
T.tube("band", [(0, 0.0, 0.893), (0, 0.002, 0.934)], [0.17, 0.159], "band", 24, wob=lambda i, a: 1 + 0.03 * math.sin(3 * a))

# ---- beard: a shell DRAPED over the chin, chest, belly and belt (rests on them, wraps around the sides)
LOCKS, DOM = 6, 0.14            # six locks; the dominant one a little right of centre
def lockf(u):                   # 1 at the centre of a lock, 0 between locks
    x = (u + 1) / 2 * LOCKS; return math.cos(math.pi * (x - math.floor(x) - 0.5)) ** 2
def bplace(u, v):
    ztop = 0.748 + 0.05 * u * u
    zbot = 0.352 + 0.15 * u * u - 0.03 * lockf(u) - 0.035 * math.exp(-((u - DOM) / 0.18) ** 2)
    return u * (1.28 - 0.3 * v), ztop + (zbot - ztop) * (v ** 0.92)      # stays on the front: the arms hang free at the sides
def bthick(u, v):
    side = max(0.0, 1 - abs(u) ** 3) ** 0.6
    body = 0.5 + 0.5 * math.sin(math.pi * min(1.0, 0.12 + v * 1.25))     # fuller under the chin, thinner at the tip
    return 0.072 * side * body * (0.8 + 0.2 * lockf(u))
blift = lambda u, v: 0.03 * max(0.0, v - 0.5) ** 2 * 4 * (1 - abs(u))  # the free tip lifts off the belly
T.drape("beard", [robe, head, belt], "beard", 25, 18, bplace, bthick, blift)

# ---- weights
def w_beard(p):
    up = T.smooth01(0.66, 0.74, p.z); low = 1 - up; mid = T.smooth01(0.42, 0.62, p.z)
    return {"DEF-head": up, "DEF-spine.003": low * mid, "DEF-spine.002": low * (1 - mid) * 0.6,
            "beard.1": low * 0.35 * T.smooth01(0.66, 0.5, p.z), "beard.2": low * 0.6 * T.smooth01(0.5, 0.38, p.z)}
def w_robe(p):
    torso = ["DEF-hips", "DEF-spine.001", "DEF-spine.002", "DEF-spine.003"]
    ws = sorted(((1.0 / (T.seg_dist(p, *B[n]) ** 3 + 1e-7), n) for n in torso), reverse=True)[:2]; tot = sum(w for w, _ in ws)
    leg = 0.28 * T.smooth01(0.27, 0.12, p.z) * min(1.0, abs(p.x) / 0.12)
    out = {n: (w / tot) * (1 - leg) for w, n in ws}
    if leg > 0: out["DEF-thigh.L" if p.x > 0 else "DEF-thigh.R"] = leg
    return out
for o in list(T.ST["parts"]):
    n = o.name.split(".")[0]; side = o.name.split(".")[1] if "." in o.name and o.name.split(".")[1] in ("L", "R") else None
    if n in ("head", "nose", "cheek", "mustache", "hair", "brim", "band"): T.skin(o, ["DEF-head"])
    elif n in ("eye", "glint"): T.skin(o, ["eyes"])
    elif n == "brow": T.skin(o, ["brows"])
    elif n == "cone": T.skin(o, ["DEF-head", "hat.1", "hat.2", "hat.3"], 3); T.smooth_weights(o, 3)
    elif n == "beard": T.skin_fn(o, w_beard); T.smooth_weights(o, 2)
    elif n in ("robe", "belt", "buckle"):
        T.skin_fn(o, w_robe)
        if n == "robe": T.smooth_weights(o, 2)
    elif n == "leg": T.skin(o, ["DEF-thigh." + side, "DEF-shin." + side], 3)
    elif n in ("boot", "sole"): T.skin(o, ["DEF-foot." + side, "DEF-toe." + side], 3, 2)
    elif n == "shaft": T.skin(o, ["DEF-shin." + side, "DEF-foot." + side], 3, 2)
    elif n in ("sleeve", "cuff"): T.skin(o, ["DEF-upper_arm." + side, "DEF-forearm." + side, "DEF-hand." + side], 4); T.smooth_weights(o, 4)
    elif n in ("hand", "thumb"): T.skin(o, ["DEF-hand." + side])
T.bind_all()
# ---- baked contact shading (rest pose; arms excluded because they move away from the body)
static = [o for o in T.ST["parts"] if o.name.split(".")[0] not in ("sleeve", "cuff", "hand", "thumb", "eye", "glint")]
T.bake_ao(static, static)
T.export(OUT)
if PREV:
    r = math.radians
    T.preview(PREV, [("front_rest", (0, -5, 0.62), (r(90), 0, 0), None, 0), ("side_rest", (5, 0, 0.62), (r(90), 0, r(90)), None, 0),
                     ("q_rest", (3.6, -3.6, 1.6), (r(76), 0, r(45)), None, 0), ("front_idle", (0, -5, 0.62), (r(90), 0, 0), "Idle_Loop", 10),
                     ("q_walk", (3.5, -3.5, 1.4), (r(78), 0, r(45)), "Walk_Loop", 8), ("front_dance", (0, -5, 0.62), (r(90), 0, 0), "Dance_Loop", 12)])
