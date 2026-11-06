"""El Mago in 3D (toon): chibi body built to the approved model sheet, skinned to the CC0 Quaternius Universal
Animation Library skeleton reshaped to chibi proportions, exported as a GLB with all 46 animations.

  EGL_PLATFORM=surfaceless /opt/bpy/bin/python mago3d.py -- OUT.glb [PREVIEW_DIR]

Proportions (research: videos/RESEARCH_3D_TOON.md): body 3 heads tall without the hat, no neck, shoulders right under
the chin, belt at ~0.36 of the height, robe hem just above stubby boots, short arms with mitten hands at belt level,
hat ~1.3 head heights with a wide brim and a tip that droops back and curls, beard from the cheeks to the belt.
Retarget: bone lengths change, bone orientation and roll do not, so the clips' local rotations still fit; the hips'
translation is scaled by the leg ratio. Extra bones for code-driven life: hat.1-3 and beard.1-2 (springs),
eyes (blink by scaling), brows (raise).
Units: metres, Blender Z up, the character faces -Y (glTF +Z).
"""
import bpy, bmesh, math, os, sys
from mathutils import Vector

args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = args[0] if args else "mago.glb"; PREV = args[1] if len(args) > 1 else None
UAL = os.environ.get("UAL", "/opt/assets3d/ual/glTF/AnimationLibrary_Godot_Standard.gltf")

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=UAL)
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
for o in list(bpy.data.objects):
    if o.type == "MESH": bpy.data.objects.remove(o, do_unlink=True)

# ------------------------------------------------------------------ 1. reshape the skeleton
LEG = 0.32                      # new hip height / old hip height
# per bone: (offset scale of the head relative to the parent's head, length scale); vectors are per-axis (x, y, z)
SPINE = 0.56
SHAPE = {
    "DEF-hips": ((1, 0.4, 0.327), 0.6),
    "DEF-thigh": ((0.85, 0.4, 0.5), 0.35), "DEF-shin": (0.35, 0.25), "DEF-foot": (0.25, 0.6), "DEF-toe": (0.6, 0.45),
    "DEF-spine.001": (SPINE, SPINE), "DEF-spine.002": (SPINE, SPINE), "DEF-spine.003": (SPINE, SPINE),
    "DEF-neck": (SPINE, 0.3), "DEF-head": (0.3, 1.0),
    "DEF-shoulder": ((1, 0.5, 0.55), 0.9), "DEF-upper_arm": ((0.93, 0.3, 0.5), 0.47), "DEF-forearm": (0.47, 0.40),
    "DEF-hand": (0.40, 0.8),
}
def shape_of(name):
    base = name.rsplit(".", 1)[0] if name.endswith((".L", ".R")) else name
    if base in SHAPE: return SHAPE[base]
    return (0.8, 0.8)            # fingers and thumbs: scaled with the hand
V = lambda s: Vector(s) if isinstance(s, tuple) else Vector((s, s, s))

bpy.context.view_layer.objects.active = arm; arm.select_set(True)
bpy.ops.object.mode_set(mode="EDIT")
eb = arm.data.edit_bones
orig = {b.name: (b.head.copy(), b.tail.copy(), b.roll) for b in eb}
new = {}
def place(b):
    oh, ot, roll = orig[b.name]
    off, ln = shape_of(b.name)
    if b.parent is None:
        nh = oh.copy()
    else:
        ph = orig[b.parent.name][0]; nph = new[b.parent.name][0]
        nh = nph + (oh - ph) * V(off)
    nt = nh + (ot - oh) * ln
    new[b.name] = (nh, nt)
    for c in b.children: place(c)
for b in eb:
    if b.parent is None: place(b)
for b in eb:
    b.use_connect = False
for b in eb:
    h, t = new[b.name]; r = orig[b.name][2]
    b.head = h; b.tail = t; b.roll = r
# extra bones for code-driven secondary motion and face
hd = eb["DEF-head"]
def add(name, h, t, parent):
    b = eb.new(name); b.head = Vector(h); b.tail = Vector(t); b.parent = eb[parent]; b.use_deform = True; b.roll = 0; return b
HEADC = Vector((0, -0.005, 0.79))                      # head centre (head radius ~0.155)
add("hat.1", (0, 0.0, 0.9), (0, 0.04, 1.06), "DEF-head")
add("hat.2", (0, 0.04, 1.06), (0, 0.18, 1.16), "hat.1")
add("hat.3", (0, 0.18, 1.16), (0, 0.27, 1.07), "hat.2")
add("beard.1", (0, -0.16, 0.72), (0, -0.19, 0.56), "DEF-head")
add("beard.2", (0, -0.19, 0.56), (0, -0.18, 0.40), "beard.1")
add("eyes", (0, -0.13, 0.805), (0, -0.13, 0.84), "DEF-head")
add("brows", (0, -0.13, 0.84), (0, -0.13, 0.87), "DEF-head")
bpy.ops.object.mode_set(mode="OBJECT")
B = {b.name: (b.head_local.copy(), b.tail_local.copy()) for b in arm.data.bones}
print("hips", B["DEF-hips"][0], "knee", B["DEF-shin.L"][0], "ankle", B["DEF-foot.L"][0], "shoulder", B["DEF-upper_arm.L"][0],
      "hand", B["DEF-hand.L"][0], "head", B["DEF-head"][0])

# hips translation scaled by the leg ratio, in every clip (layered/slotted actions in Blender 4.4+)
def fcurves(act):
    out = []
    for layer in getattr(act, "layers", []):
        for strip in layer.strips:
            for cb in strip.channelbags: out.extend(cb.fcurves)
    return out or list(getattr(act, "fcurves", []))
for act in bpy.data.actions:
    act.use_fake_user = True
    for fc in fcurves(act):
        if fc.data_path.endswith(".location"):
            for k in fc.keyframe_points:
                k.co.y *= LEG; k.handle_left.y *= LEG; k.handle_right.y *= LEG

# ------------------------------------------------------------------ 2. materials (palette)
def lin(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return tuple((v / 12.92) if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c) + (1,)
MAT = {}
for n, h in dict(robe="#6A58B8", robe_dark="#4B3A8E", hat="#6A58B8", band="#F2C14E", skin="#F0C090", cheek="#E1867A",
                 beard="#FBF4E4", eye="#150A34", glint="#FFFFFF", belt="#6E3B22", buckle="#F2C14E", boot="#5A3424", sole="#2E2160").items():
    m = bpy.data.materials.new(n); m.use_nodes = True
    bs = m.node_tree.nodes["Principled BSDF"]; bs.inputs["Base Color"].default_value = lin(h); bs.inputs["Roughness"].default_value = 0.8
    MAT[n] = m

# ------------------------------------------------------------------ 3. parts
def new_obj(name, bm, mat):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    me.materials.append(MAT[mat])
    for p in me.polygons: p.use_smooth = True
    return o

def lathe(name, prof, mat, segs=28, center=(0, 0, 0), sy=1.0, cap_top=True, cap_bot=True, wob=None):
    """surface of revolution around Z: prof = [(r, z), ...] bottom -> top; sy flattens front-back"""
    bm = bmesh.new(); rings = []
    for r, z in prof:
        ring = []
        for k in range(segs):
            a = 2 * math.pi * k / segs; f = wob(a, z) if wob else 1
            ring.append(bm.verts.new((center[0] + r * f * math.cos(a), center[1] + r * f * math.sin(a) * sy, center[2] + z)))
        rings.append(ring)
    for j in range(len(rings) - 1):
        for k in range(segs):
            bm.faces.new((rings[j][k], rings[j][(k + 1) % segs], rings[j + 1][(k + 1) % segs], rings[j + 1][k]))
    if cap_bot: bm.faces.new(list(reversed(rings[0])))
    if cap_top: bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return new_obj(name, bm, mat)

def ellipsoid(name, c, r, mat, seg=20, rings=12):
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=1.0)
    for v in bm.verts: v.co = Vector((c[0] + v.co.x * r[0], c[1] + v.co.y * r[1], c[2] + v.co.z * r[2]))
    return new_obj(name, bm, mat)

def tube(name, path, radii, mat, segs=16):
    """tube along a polyline with per-point radius (hat cone, sleeves); closed at both ends"""
    bm = bmesh.new(); rings = []; a = None
    for i, (p, r) in enumerate(zip(path, radii)):
        p = Vector(p); d = (Vector(path[min(i + 1, len(path) - 1)]) - Vector(path[max(i - 1, 0)])).normalized()
        a = Vector((1, 0, 0)) if a is None else a           # parallel transport: no twist along a bent hat
        a = (a - d * a.dot(d)).normalized(); b = d.cross(a).normalized()
        rings.append([bm.verts.new(p + (a * math.cos(2 * math.pi * k / segs) + b * math.sin(2 * math.pi * k / segs)) * max(r, 1e-4)) for k in range(segs)])
    for j in range(len(rings) - 1):
        for k in range(segs):
            bm.faces.new((rings[j][k], rings[j][(k + 1) % segs], rings[j + 1][(k + 1) % segs], rings[j + 1][k]))
    bm.faces.new(list(reversed(rings[0]))); bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return new_obj(name, bm, mat)

parts = []
# robe: a stocky barrel from the hem to the shoulders, slightly flattened front-back
parts.append(lathe("robe", [(0.205, 0.115), (0.222, 0.13), (0.215, 0.2), (0.21, 0.3), (0.208, 0.4), (0.198, 0.5),
                            (0.175, 0.58), (0.13, 0.64), (0.06, 0.67)], "robe", sy=0.86))
parts.append(lathe("belt", [(0.214, 0.335), (0.216, 0.36), (0.214, 0.385)], "belt", sy=0.88, cap_top=False, cap_bot=False))
parts.append(ellipsoid("buckle", (0, -0.188, 0.36), (0.042, 0.014, 0.034), "buckle", 4, 4))
# legs (mostly hidden) and boots
for s, side in ((1, "L"), (-1, "R")):
    k = B["DEF-shin." + side][0]; an = B["DEF-foot." + side][0]
    parts.append(tube("leg." + side, [(k.x, k.y, k.z + 0.05), (an.x, an.y, an.z + 0.02)], [0.045, 0.042], "robe_dark", 10))
    toe = B["DEF-toe." + side][1]
    parts.append(ellipsoid("boot." + side, ((an.x + toe.x) / 2, (an.y + toe.y) / 2 - 0.01, 0.045), (0.056, 0.088, 0.05), "boot", 16, 10))
    parts.append(tube("shaft." + side, [(an.x, an.y + 0.005, 0.04), (an.x, an.y + 0.005, 0.15)], [0.05, 0.052], "boot", 12))
# arms (modelled in the rest T-pose: horizontal along x): bell sleeves and mitten hands
for s, side in ((1, "L"), (-1, "R")):
    sh = B["DEF-upper_arm." + side][0]; el = B["DEF-forearm." + side][0]; wr = B["DEF-hand." + side][0]
    parts.append(tube("sleeve." + side, [sh - Vector((s * 0.03, 0, 0)), sh, el, wr - Vector((s * 0.005, 0, 0))], [0.05, 0.052, 0.05, 0.062], "robe", 14))
    hc = wr + Vector((s * 0.035, -0.005, 0))
    parts.append(ellipsoid("hand." + side, hc, (0.042, 0.036, 0.04), "skin", 14, 8))
    parts.append(ellipsoid("thumb." + side, hc + Vector((-s * 0.012, -0.03, 0.012)), (0.016, 0.016, 0.016), "skin", 8, 6))
# head and face
parts.append(ellipsoid("head", HEADC, (0.15, 0.14, 0.15), "skin", 24, 14))
parts.append(ellipsoid("nose", (0, -0.15, 0.775), (0.042, 0.035, 0.036), "skin", 14, 8))
for s in (1, -1):
    parts.append(ellipsoid("cheek", (s * 0.075, -0.12, 0.768), (0.032, 0.012, 0.022), "cheek", 10, 6))
    parts.append(ellipsoid("eye", (s * 0.046, -0.136, 0.802), (0.017, 0.01, 0.024), "eye", 12, 8))
    parts.append(ellipsoid("glint", (s * 0.046 + 0.006, -0.146, 0.81), (0.0055, 0.003, 0.0065), "glint", 8, 5))
    parts.append(ellipsoid("brow", (s * 0.05, -0.13, 0.838), (0.03, 0.014, 0.011), "beard", 10, 6))
    parts.append(ellipsoid("mustache", (s * 0.04, -0.155, 0.745), (0.048, 0.025, 0.022), "beard", 12, 6))
# hair at the back and sides, under the hat
parts.append(lathe("hair", [(0.148, 0.75), (0.158, 0.785), (0.156, 0.84), (0.14, 0.87)], "beard", sy=0.95, cap_top=False, cap_bot=False,
                   wob=lambda a, z: 0.0 if math.sin(a) < -0.45 else 1.0))
# beard: rounded wedge from the cheeks to the belt
bprof = [(0.005, 0.37), (0.05, 0.39), (0.1, 0.45), (0.13, 0.54), (0.142, 0.63), (0.135, 0.71), (0.11, 0.76)]
parts.append(lathe("beard", bprof, "beard", center=(0, -0.11, 0), sy=0.55, wob=lambda a, z: 1 + 0.04 * math.sin(6 * a + z * 30)))
# hat: brim, cone along a bent path that droops back and curls, gold band
parts.append(lathe("brim", [(0.06, 0.88), (0.27, 0.873), (0.285, 0.865), (0.27, 0.891), (0.07, 0.9)], "hat", sy=0.97))
hp = [(0, 0.0, 0.89), (0, 0.008, 0.96), (0, 0.035, 1.05), (0, 0.09, 1.12), (0, 0.16, 1.155), (0, 0.225, 1.15), (0, 0.268, 1.11),
      (0, 0.272, 1.065), (0, 0.245, 1.045), (0, 0.222, 1.06)]
hr = [0.165, 0.138, 0.108, 0.08, 0.058, 0.042, 0.03, 0.022, 0.016, 0.011]
parts.append(tube("cone", hp, hr, "hat", 20))
parts.append(tube("band", [(0, 0.0, 0.895), (0, 0.002, 0.93)], [0.166, 0.156], "band", 24))

# ------------------------------------------------------------------ 4. skin weights (procedural, per part)
def seg_dist(p, a, b):
    ab = b - a; t = max(0.0, min(1.0, (p - a).dot(ab) / max(ab.length_squared, 1e-9))); return (p - (a + ab * t)).length
def skin(o, bones, power=4.0, top=3):
    vgs = {n: o.vertex_groups.new(name=n) for n in bones}
    for v in o.data.vertices:
        p = o.matrix_world @ v.co
        ws = sorted(((1.0 / (seg_dist(p, *B[n]) ** power + 1e-7), n) for n in bones), reverse=True)[:top]
        tot = sum(w for w, _ in ws)
        for w, n in ws: vgs[n].add([v.index], w / tot, "REPLACE")
def skin_robe(o):
    """torso bones by distance; only the lower robe follows the legs a little (a stiff, heavy robe, no skew)"""
    torso = ["DEF-hips", "DEF-spine.001", "DEF-spine.002", "DEF-spine.003"]
    vgs = {n: o.vertex_groups.new(name=n) for n in torso + ["DEF-thigh.L", "DEF-thigh.R"]}
    for v in o.data.vertices:
        p = o.matrix_world @ v.co
        ws = sorted(((1.0 / (seg_dist(p, *B[n]) ** 3 + 1e-7), n) for n in torso), reverse=True)[:2]
        tot = sum(w for w, _ in ws); leg = 0.28 * max(0.0, min(1.0, (0.27 - p.z) / 0.15)) * min(1.0, abs(p.x) / 0.12)
        for w, n in ws: vgs[n].add([v.index], (w / tot) * (1 - leg), "REPLACE")
        if leg > 0: vgs["DEF-thigh.L" if p.x > 0 else "DEF-thigh.R"].add([v.index], leg, "REPLACE")
for o in parts:
    n = o.name.split(".")[0]
    side = o.name.split(".")[1] if "." in o.name and o.name.split(".")[1] in ("L", "R") else None
    if n in ("head", "nose", "cheek", "mustache", "hair", "brim", "band"): skin(o, ["DEF-head"])
    elif n in ("eye", "glint"): skin(o, ["eyes"])
    elif n in ("brow",): skin(o, ["brows"])
    elif n == "cone": skin(o, ["DEF-head", "hat.1", "hat.2", "hat.3"], 3)
    elif n == "beard": skin(o, ["DEF-head", "beard.1", "beard.2", "DEF-spine.003"], 3)
    elif n in ("robe", "belt", "buckle"): skin_robe(o)
    elif n == "leg": skin(o, ["DEF-thigh." + side, "DEF-shin." + side], 3)
    elif n == "boot": skin(o, ["DEF-foot." + side, "DEF-toe." + side], 3, 2)
    elif n == "shaft": skin(o, ["DEF-shin." + side, "DEF-foot." + side], 3, 2)
    elif n == "sleeve": skin(o, ["DEF-upper_arm." + side, "DEF-forearm." + side, "DEF-hand." + side], 4)
    elif n in ("hand", "thumb"): skin(o, ["DEF-hand." + side])
    o.parent = arm; md = o.modifiers.new("arm", "ARMATURE"); md.object = arm
tris = sum(len(o.data.polygons) for o in parts)
print("parts", len(parts), "faces", tris)

# ------------------------------------------------------------------ 5. export + preview
arm.animation_data_create()
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB", export_animations=True, export_animation_mode="ACTIONS",
                          export_skins=True, export_yup=True, export_apply=False)
print("glb ->", OUT, os.path.getsize(OUT) // 1024, "KB")

if PREV:
    sc = bpy.context.scene; os.makedirs(PREV, exist_ok=True)
    sc.render.engine = "BLENDER_WORKBENCH"; sc.display.shading.light = "STUDIO"; sc.display.shading.color_type = "MATERIAL"
    sc.display.shading.show_object_outline = True; sc.render.resolution_x, sc.render.resolution_y = 640, 960
    sc.render.film_transparent = False; sc.world = bpy.data.worlds.new("w")
    for m in MAT.values(): m.diffuse_color = m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
    cam.data.type = "ORTHO"; cam.data.ortho_scale = 1.45
    def shot(name, loc, rot, action=None, frame=0):
        if action: arm.animation_data.action = bpy.data.actions[action]
        else: arm.animation_data.action = None
        if action and hasattr(arm.animation_data, "action_slot") and arm.animation_data.action.slots:
            arm.animation_data.action_slot = arm.animation_data.action.slots[0]
        sc.frame_set(frame); cam.location = loc; cam.rotation_euler = rot
        sc.render.filepath = os.path.join(PREV, name + ".png"); bpy.ops.render.render(write_still=True)
    shot("front_rest", (0, -5, 0.62), (math.radians(90), 0, 0))
    shot("side_rest", (5, 0, 0.62), (math.radians(90), 0, math.radians(90)))
    shot("front_idle", (0, -5, 0.62), (math.radians(90), 0, 0), "Idle_Loop", 10)
    shot("q_walk", (3.5, -3.5, 1.4), (math.radians(78), 0, math.radians(45)), "Walk_Loop", 8)
    shot("front_dance", (0, -5, 0.62), (math.radians(90), 0, 0), "Dance_Loop", 12)
    shot("front_interact", (1.5, -4.6, 0.8), (math.radians(87), 0, math.radians(18)), "Interact", 30)
