"""toonchar: build stylised toon characters in Blender Python (headless) on the CC0 Quaternius skeleton.

Used by mago3d.py and santa3d.py. Research: videos/RESEARCH_3D_TOON.md (proportions, retarget) and
videos/RESEARCH_3D_FORMS.md (draping, weight, volume, secondary forms, baked light).

- setup(SHAPE, LEG, extra_bones): import the skeleton and 46 clips, reshape the bones (orientation and roll kept, so
  the clips still fit), scale hips translation by the leg ratio, add extra bones (springs, face).
- Parts: lathe / ellipsoid / tube with seeded wobble (folds, dents, scallops), all in metres, Z up, facing -Y.
- drape(): a shell that RESTS on other parts (procedural shrinkwrap: rays onto the support surface + thickness), thin
  where it touches, edges tapered, tip lifting off; its inner face sits slightly under the support (no gap).
- Weights: distance falloff to bone segments, custom per-vertex functions, Laplacian smoothing, max 4, normalised.
- bake_ao(): ambient occlusion by ray casting into a vertex colour layer "AO" (contact darkening where parts touch).
- export(): GLB with all clips and the AO colours.
"""
import bpy, bmesh, math, os, random
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

UAL = os.environ.get("UAL", "/opt/assets3d/ual/glTF/AnimationLibrary_Godot_Standard.gltf")
ST = {"arm": None, "B": {}, "MAT": {}, "parts": []}
V = lambda s: Vector(s) if isinstance(s, tuple) else Vector((s, s, s))
smooth01 = lambda e0, e1, x: (lambda t: t * t * (3 - 2 * t))(max(0.0, min(1.0, (x - e0) / (e1 - e0))))


def setup(SHAPE, LEG, extra=()):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=UAL)
    arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
    for o in list(bpy.data.objects):
        if o.type == "MESH": bpy.data.objects.remove(o, do_unlink=True)
    def shape_of(name):
        base = name.rsplit(".", 1)[0] if name.endswith((".L", ".R")) else name
        return SHAPE.get(base, (0.8, 0.8))
    bpy.context.view_layer.objects.active = arm; arm.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    eb = arm.data.edit_bones
    orig = {b.name: (b.head.copy(), b.tail.copy(), b.roll) for b in eb}; new = {}
    def place(b):
        oh, ot, _ = orig[b.name]; off, ln = shape_of(b.name)
        nh = oh.copy() if b.parent is None else new[b.parent.name][0] + (oh - orig[b.parent.name][0]) * V(off)
        new[b.name] = (nh, nh + (ot - oh) * ln)
        for c in b.children: place(c)
    for b in eb:
        if b.parent is None: place(b)
    for b in eb: b.use_connect = False
    for b in eb:
        h, t = new[b.name]; b.head = h; b.tail = t; b.roll = orig[b.name][2]
    for name, h, t, parent in extra:
        b = eb.new(name); b.head = Vector(h); b.tail = Vector(t); b.parent = eb[parent]; b.use_deform = True; b.roll = 0
    bpy.ops.object.mode_set(mode="OBJECT")
    for act in bpy.data.actions:
        act.use_fake_user = True
        for fc in _fcurves(act):
            if fc.data_path.endswith(".location"):
                for k in fc.keyframe_points:
                    k.co.y *= LEG; k.handle_left.y *= LEG; k.handle_right.y *= LEG
    ST["arm"] = arm; ST["B"] = {b.name: (b.head_local.copy(), b.tail_local.copy()) for b in arm.data.bones}
    ST["parts"] = []; ST["MAT"] = {}
    return arm, ST["B"]


def _fcurves(act):
    out = []
    for layer in getattr(act, "layers", []):
        for strip in layer.strips:
            for cb in strip.channelbags: out.extend(cb.fcurves)
    return out or list(getattr(act, "fcurves", []))


def lin(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return tuple((v / 12.92) if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c) + (1,)


def materials(table):
    for n, h in table.items():
        m = bpy.data.materials.new(n); m.use_nodes = True
        bs = m.node_tree.nodes["Principled BSDF"]; bs.inputs["Base Color"].default_value = lin(h); bs.inputs["Roughness"].default_value = 0.8
        m.diffuse_color = lin(h); ST["MAT"][n] = m


def _obj(name, bm, mat):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    me.materials.append(ST["MAT"][mat])
    for p in me.polygons: p.use_smooth = True
    ST["parts"].append(o); return o


def lathe(name, prof, mat, segs=32, center=(0, 0, 0), sy=1.0, caps=(True, True), wob=None, zwob=None):
    """surface of revolution around Z, prof = [(r, z)] bottom -> top. wob(a, z) scales r (folds, lumps);
    zwob(a, ring_index) shifts z (hem scallops, droopy brim). a = 0 points +X, a = -pi/2 is the front (-Y)."""
    bm = bmesh.new(); rings = []
    for j, (r, z) in enumerate(prof):
        ring = []
        for k in range(segs):
            a = 2 * math.pi * k / segs; f = wob(a, z) if wob else 1.0; dz = zwob(a, j) if zwob else 0.0
            ring.append(bm.verts.new((center[0] + r * f * math.cos(a), center[1] + r * f * math.sin(a) * sy, center[2] + z + dz)))
        rings.append(ring)
    for j in range(len(rings) - 1):
        for k in range(segs):
            bm.faces.new((rings[j][k], rings[j][(k + 1) % segs], rings[j + 1][(k + 1) % segs], rings[j + 1][k]))
    if caps[0]: bm.faces.new(list(reversed(rings[0])))
    if caps[1]: bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _obj(name, bm, mat)


def ellipsoid(name, c, r, mat, seg=20, rings=12, wob=None):
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=1.0)
    for v in bm.verts:
        f = wob(v.co) if wob else 1.0
        v.co = Vector((c[0] + v.co.x * r[0] * f, c[1] + v.co.y * r[1] * f, c[2] + v.co.z * r[2] * f))
    return _obj(name, bm, mat)


def tube(name, path, radii, mat, segs=16, wob=None, caps=(True, True)):
    """tube along a polyline (parallel-transport frames, no twist); wob(i, angle) scales the radius per ring/angle"""
    bm = bmesh.new(); rings = []; a = None
    for i, (p, r) in enumerate(zip(path, radii)):
        p = Vector(p); d = (Vector(path[min(i + 1, len(path) - 1)]) - Vector(path[max(i - 1, 0)])).normalized()
        a = Vector((1, 0, 0)) if a is None else a
        if abs(a.dot(d)) > 0.99: a = Vector((0, 1, 0))
        a = (a - d * a.dot(d)).normalized(); b = d.cross(a).normalized(); ring = []
        for k in range(segs):
            ang = 2 * math.pi * k / segs; rr = max(r, 1e-4) * (wob(i, ang) if wob else 1.0)
            ring.append(bm.verts.new(p + (a * math.cos(ang) + b * math.sin(ang)) * rr))
        rings.append(ring)
    for j in range(len(rings) - 1):
        for k in range(segs):
            bm.faces.new((rings[j][k], rings[j][(k + 1) % segs], rings[j + 1][(k + 1) % segs], rings[j + 1][k]))
    if caps[0]: bm.faces.new(list(reversed(rings[0])))
    if caps[1]: bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _obj(name, bm, mat)


def bvh_of(objs):
    verts, polys, off = [], [], 0
    for o in objs:
        mw = o.matrix_world; verts += [mw @ v.co for v in o.data.vertices]
        polys += [[i + off for i in p.vertices] for p in o.data.polygons]; off += len(o.data.vertices)
    return BVHTree.FromPolygons(verts, polys)


def drape(name, support, mat, nu, nv, place, thick, lift=None, inset=0.004):
    """A shell resting on `support` objects. place(u, v) -> (phi, z): u in [-1, 1] across, v in [0, 1] down; phi is the
    angle from the front (-Y) around Z. A horizontal ray from outside hits the support; the outer surface sits at
    thickness thick(u, v) along the support normal, the inner one `inset` below it (overlap, no gap).
    lift(u, v) -> extra outward offset (a free tip lifting off the body)."""
    tree = bvh_of(support); bm = bmesh.new(); O, I = [], []
    for j in range(nv):
        v = j / (nv - 1); ro, ri = [], []
        for i in range(nu):
            u = -1 + 2 * i / (nu - 1); phi, z = place(u, v)
            d = Vector((-math.sin(phi), math.cos(phi), 0.0))          # ray pointing inward, from the front-ish side
            org = Vector((0, 0, z)) - d * 2.0
            hit, nrm, _, _ = tree.ray_cast(org, d, 4.0)
            if hit is None: hit = Vector((0, 0, z)) - d * 0.2; nrm = -d
            nrm = nrm.normalized(); t = thick(u, v); lf = lift(u, v) if lift else 0.0
            out = -d * lf
            ro.append(bm.verts.new(hit + nrm * t + out)); ri.append(bm.verts.new(hit - nrm * inset + out * 0.6))
        O.append(ro); I.append(ri)
    for j in range(nv - 1):
        for i in range(nu - 1):
            bm.faces.new((O[j][i], O[j + 1][i], O[j + 1][i + 1], O[j][i + 1]))
            bm.faces.new((I[j][i], I[j][i + 1], I[j + 1][i + 1], I[j + 1][i]))
    for j in range(nv - 1):            # side walls
        bm.faces.new((O[j][0], I[j][0], I[j + 1][0], O[j + 1][0]))
        bm.faces.new((O[j][-1], O[j + 1][-1], I[j + 1][-1], I[j][-1]))
    for i in range(nu - 1):            # top and bottom walls
        bm.faces.new((O[0][i], O[0][i + 1], I[0][i + 1], I[0][i]))
        bm.faces.new((O[-1][i], I[-1][i], I[-1][i + 1], O[-1][i + 1]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _obj(name, bm, mat)


def displace(o, amp, freq, seed=0):
    """seeded low-frequency noise along normals (breaks the CG-primitive look; 1-3 % of the part size)"""
    rnd = random.Random(seed); ph = [rnd.uniform(0, 6.28) for _ in range(6)]
    me = o.data
    for v in me.vertices:
        p = v.co; n = v.normal
        s = (math.sin(p.x * freq + ph[0]) * math.sin(p.y * freq * 1.3 + ph[1]) + math.sin(p.z * freq * 0.8 + ph[2]) * 0.6
             + math.sin((p.x + p.z) * freq * 2.1 + ph[3]) * 0.3)
        v.co = p + n * amp * s


# ---------------------------------------------------------------- weights
def seg_dist(p, a, b):
    ab = b - a; t = max(0.0, min(1.0, (p - a).dot(ab) / max(ab.length_squared, 1e-9))); return (p - (a + ab * t)).length


def skin_fn(o, fn):
    """fn(world_pos) -> {bone: weight}; normalised, max 4 influences"""
    B = ST["B"]; groups = {}
    for v in o.data.vertices:
        p = o.matrix_world @ v.co; w = {k: x for k, x in fn(p).items() if x > 1e-4}
        top = sorted(w.items(), key=lambda kv: -kv[1])[:4]; tot = sum(x for _, x in top) or 1
        for n, x in top:
            g = groups.get(n) or o.vertex_groups.get(n) or o.vertex_groups.new(name=n); groups[n] = g
            g.add([v.index], x / tot, "REPLACE")


def skin(o, bones, power=4.0, top=3):
    B = ST["B"]
    def fn(p):
        ws = sorted(((1.0 / (seg_dist(p, *B[n]) ** power + 1e-7), n) for n in bones), reverse=True)[:top]
        return {n: w for w, n in ws}
    skin_fn(o, fn)


def smooth_weights(o, passes=3, k=0.5):
    """Laplacian smoothing of all vertex groups over mesh edges, renormalised (smoother joints, fewer collapses)"""
    me = o.data; n = len(me.vertices); G = list(o.vertex_groups)
    if len(G) < 2: return
    W = np.zeros((n, len(G)))
    for v in me.vertices:
        for g in v.groups: W[v.index, g.group] = g.weight
    nb = [[] for _ in range(n)]
    for e in me.edges: a, b = e.vertices; nb[a].append(b); nb[b].append(a)
    for _ in range(passes):
        avg = np.array([W[l].mean(0) if l else W[i] for i, l in enumerate(nb)])
        W = (1 - k) * W + k * avg; W /= np.maximum(W.sum(1, keepdims=True), 1e-9)
    for gi, g in enumerate(G):
        for i in range(n):
            if W[i, gi] > 1e-3: g.add([i], float(W[i, gi]), "REPLACE")
            else: g.remove([i])


def bind_all():
    arm = ST["arm"]
    for o in ST["parts"]:
        o.parent = arm; md = o.modifiers.new("arm", "ARMATURE"); md.object = arm


# ---------------------------------------------------------------- baked ambient occlusion
def bake_ao(receivers, occluders, rays=28, dist=0.13, strength=0.95, seed=3):
    """contact darkening: fraction of cosine-weighted rays hitting nearby geometry, stored as vertex colour AO"""
    tree = bvh_of(occluders); rnd = random.Random(seed)
    dirs = []
    for _ in range(rays):
        u1, u2 = rnd.random(), rnd.random(); r = math.sqrt(u1); th = 2 * math.pi * u2
        dirs.append((r * math.cos(th), r * math.sin(th), math.sqrt(max(0.0, 1 - u1))))
    rec = set(o.name for o in receivers)
    for o in ST["parts"]:
        me = o.data; att = me.color_attributes.new("AO", "BYTE_COLOR", "POINT"); me.color_attributes.active_color = att
        if o.name not in rec:
            for i in range(len(me.vertices)): att.data[i].color = (1, 1, 1, 1)
            continue
        mw = o.matrix_world; nm = mw.to_3x3()
        for v in me.vertices:
            p = mw @ v.co; n = (nm @ v.normal).normalized()
            t = n.orthogonal().normalized(); b = n.cross(t); hit = 0.0
            for dx, dy, dz in dirs:
                d = t * dx + b * dy + n * dz
                h = tree.ray_cast(p + n * 0.003, d, dist)
                if h[0] is not None: hit += 1.0 - (h[3] / dist) * 0.5
            ao = max(0.0, 1.0 - strength * hit / rays)
            att.data[v.index].color = (ao, ao, ao, 1)


def export(path):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    ST["arm"].animation_data_create()
    bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", export_animations=True, export_animation_mode="ACTIONS",
                              export_skins=True, export_yup=True, export_apply=False, export_vertex_color="ACTIVE")
    print("glb ->", path, os.path.getsize(path) // 1024, "KB", "faces", sum(len(o.data.polygons) for o in ST["parts"]))


def preview(out_dir, shots):
    """workbench previews: shots = [(name, cam_loc, cam_rot, action or None, frame)]"""
    sc = bpy.context.scene; arm = ST["arm"]; os.makedirs(out_dir, exist_ok=True)
    sc.render.engine = "BLENDER_WORKBENCH"; sc.display.shading.light = "STUDIO"; sc.display.shading.color_type = "MATERIAL"
    sc.display.shading.show_object_outline = True; sc.display.shading.show_cavity = True
    sc.render.resolution_x, sc.render.resolution_y = 640, 960; sc.world = bpy.data.worlds.new("w")
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
    cam.data.type = "ORTHO"; cam.data.ortho_scale = 1.6
    for name, loc, rot, action, frame in shots:
        arm.animation_data.action = bpy.data.actions[action] if action else None
        if action and arm.animation_data.action.slots: arm.animation_data.action_slot = arm.animation_data.action.slots[0]
        sc.frame_set(frame); cam.location = loc; cam.rotation_euler = rot
        sc.render.filepath = os.path.join(out_dir, name + ".png"); bpy.ops.render.render(write_still=True)
