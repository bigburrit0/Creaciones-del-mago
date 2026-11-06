"""pixel3d: model props or characters in Blender (bpy) and render them for pixelize3d.py ("pre-rendered sprites").

Run a prop script with a Python that has bpy (`python3 -m venv /opt/bpy && /opt/bpy/bin/pip install bpy`):

    import pixel3d as P
    P.scene("out/printer", cell=(64, 64), anchor=(32, 58))
    white = P.mat("white", ["#5B4636", "#C8AE88", "#D8D4C8", "#FBF4E4"])
    glow = P.mat("nozzle", ["#E86A4A"], emissive=True)
    base = P.box((3.6, 2.4, 0.35), (0, 0, 0.175), white)
    P.render("obj.printer3d_idle", 1, lambda i, n: None, fps=8, mode="static")
    P.finish()

How it works: two renders per frame at `ss` times the art size, saved as EXR: f_NNNN (every material white, so it holds
only the light, plus the shadow catcher's shadow in alpha) and i_NNNN (flat emission: red = material id / 64,
green = depth / 200, no anti-aliasing). A view-layer property ("idpass") switches the materials between the two. pixelize3d.py then picks one material
per art pixel (majority vote), maps the light to that material's palette ramp (toon bands), and draws the outline.
So colours always come from the palette and edges never get anti-aliased.

Units: 1 Blender unit = `ppu` art pixels (default 10). The origin (0,0,0) lands on the anchor pixel; build the
prop standing on z=0 around the origin. Camera: orthographic, looking at the back wall from `elev` degrees above
the floor (37 matches the workshop's floor foreshortening). Turn a prop with `yaw` to show a side face.
Light: key from the upper-left front (pixel-art convention: top and left faces lit), soft fill, sky.
"""
import bpy, json, math, os
from mathutils import Vector

ST = {"mats": [], "anims": [], "out": None, "cfg": {}}


def hex2lin(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return tuple((v / 12.92) if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c)


def scene(out, cell=(64, 64), anchor=None, ss=4, elev=37.0, ppu=10.0, samples=48, key=(0.55, 0.5, -1.0),
          key_energy=3.0, fill_energy=0.6, sky=0.35, catcher=True, outline="#150A34", shadow="#2E2160", bounces=2):
    """Fresh scene, camera, lights and shadow catcher. Everything is in art pixels except geometry (BU)."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    W, H = cell; ax, ay = anchor or (W / 2, H - 4)
    ST.update(out=out, mats=[], mobj=[], anims=[], cfg=dict(cell=[W, H], anchor=[ax, ay], ss=ss, ppu=ppu, elev=elev,
                                                    outline=outline, shadow=shadow))
    os.makedirs(out, exist_ok=True)
    sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = samples; sc.cycles.use_denoising = False
    sc.cycles.seed = 0; sc.cycles.use_animated_seed = False                    # same noise every frame: no shimmer
    sc.cycles.max_bounces = bounces + 1; sc.cycles.diffuse_bounces = bounces; sc.cycles.glossy_bounces = 0
    sc.cycles.transmission_bounces = 0; sc.cycles.volume_bounces = 0; sc.cycles.transparent_max_bounces = 2
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = W * ss, H * ss, 100
    sc.render.film_transparent = True; sc.render.filter_size = 0.01            # no AA: ids must stay exact
    sc.view_settings.view_transform = "Standard"; sc.render.use_compositing = False
    im = sc.render.image_settings; im.media_type = "MULTI_LAYER_IMAGE"; im.file_format = "OPEN_EXR_MULTILAYER"
    im.color_depth = "32"; im.exr_codec = "ZIP"
    # camera: ortho, pitched down; origin projected exactly on the anchor pixel
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
    cam.data.type = "ORTHO"; cam.data.ortho_scale = max(W, H) / ppu; cam.data.clip_end = 400
    pitch = math.radians(90 - elev); cam.rotation_euler = (pitch, 0, 0)
    fwd = Vector((0, math.sin(pitch), -math.cos(pitch))); up = Vector((0, math.cos(pitch), math.sin(pitch)))
    cam.location = -fwd * 100 + up * ((ay - H / 2) / ppu) + Vector(((W / 2 - ax) / ppu, 0, 0))
    # lights (white: only the amount of light matters, colours come from the palette ramps)
    def sun(d, e, ang):
        o = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN")); sc.collection.objects.link(o)
        o.data.energy = e; o.data.angle = math.radians(ang)
        o.rotation_euler = Vector(d).normalized().to_track_quat("-Z", "Y").to_euler(); return o
    sun(key, key_energy, 3); sun((-0.6, -0.4, -0.6), fill_energy, 30)
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (1, 1, 1, 1); bg.inputs[1].default_value = sky
    if catcher:
        bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, 0)); p = bpy.context.object; p.name = "catcher"
        p.is_shadow_catcher = True
    return sc


def mat(name, ramp, emissive=False, bands=None, dither=0.0, line=None):
    """A palette material. ramp: hex colours dark -> light (toon bands). emissive: always the brightest colour.
    bands: band edges on normalised light (len(ramp)-1 values in 0..1); dither: 0..1 ordered dither at band edges.
    line: colour for internal depth edges (default: the darkest ramp colour)."""
    i = len(ST["mats"]) + 1
    m = bpy.data.materials.new(name); m.use_nodes = True; m.pass_index = i
    nt = m.node_tree; N = nt.nodes; b = N.get("Principled BSDF"); out = N.get("Material Output")
    b.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1); b.inputs["Roughness"].default_value = 1.0
    for k in ("Specular IOR Level", "Specular"):
        if k in b.inputs: b.inputs[k].default_value = 0.0
    em = N.new("ShaderNodeEmission"); cc = N.new("ShaderNodeCombineColor"); cd = N.new("ShaderNodeCameraData")
    dv = N.new("ShaderNodeMath"); dv.operation = "DIVIDE"; dv.inputs[1].default_value = 200.0
    nt.links.new(cd.outputs["View Z Depth"], dv.inputs[0]); cc.inputs["Red"].default_value = i / 64.0
    nt.links.new(dv.outputs[0], cc.inputs["Green"]); nt.links.new(cc.outputs[0], em.inputs["Color"])
    mx = N.new("ShaderNodeMixShader"); at = N.new("ShaderNodeAttribute"); at.attribute_type = "VIEW_LAYER"
    at.attribute_name = "idpass"
    nt.links.new(at.outputs["Fac"], mx.inputs["Fac"]); nt.links.new(b.outputs[0], mx.inputs[1])
    nt.links.new(em.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs["Surface"])
    m.diffuse_color = (*hex2lin(ramp[-1]), 1); ST["mobj"].append(m)
    ST["mats"].append(dict(id=i, name=name, ramp=ramp, emissive=emissive, bands=bands, dither=dither, line=line))
    return m


def _fin(o, m, parent=None, bevel=0.0, smooth=False):
    if m is not None: o.data.materials.append(m)
    if bevel:
        bv = o.modifiers.new("bev", "BEVEL"); bv.width = bevel; bv.segments = 1
    if smooth:
        for p in o.data.polygons: p.use_smooth = True
    if parent is not None: o.parent = parent
    return o


def box(size, loc, m, parent=None, bevel=None, name="box", rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.name = name
    o.scale = size; bpy.ops.object.transform_apply(scale=True)
    return _fin(o, m, parent, min(size) * 0.15 if bevel is None else bevel)


def cyl(r, depth, loc, m, rot=(0, 0, 0), verts=16, parent=None, name="cyl", r2=None, smooth=True):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot)
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r2, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; return _fin(o, m, parent, smooth=smooth)


def sphere(r, loc, m, scale=(1, 1, 1), parent=None, name="sph", seg=16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, radius=r, location=loc)
    o = bpy.context.object; o.name = name; o.scale = scale; bpy.ops.object.transform_apply(scale=True)
    return _fin(o, m, parent, smooth=True)


def torus(R, r, loc, m, rot=(0, 0, 0), parent=None, name="tor"):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc, rotation=rot,
                                     major_segments=24, minor_segments=8)
    o = bpy.context.object; o.name = name; return _fin(o, m, parent, smooth=True)


def lathe(profile, m, loc=(0, 0, 0), segs=24, parent=None, name="lathe", wobble=None):
    """Surface of revolution from [(radius, z), ...] bottom -> top. wobble(angle, z) -> radius factor (lumps)."""
    import bmesh
    me = bpy.data.meshes.new(name); o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    bm = bmesh.new(); rings = []
    for r, z in profile:
        ring = []
        for k in range(segs):
            a = 2 * math.pi * k / segs; f = wobble(a, z) if wobble else 1.0
            ring.append(bm.verts.new((r * f * math.cos(a), r * f * math.sin(a), z)))
        rings.append(ring)
    for j in range(len(rings) - 1):
        for k in range(segs):
            bm.faces.new((rings[j][k], rings[j][(k + 1) % segs], rings[j + 1][(k + 1) % segs], rings[j + 1][k]))
    bm.faces.new(list(reversed(rings[0]))); bm.faces.new(rings[-1])
    bm.normal_update(); bm.to_mesh(me); bm.free(); o.location = loc
    return _fin(o, m, parent, smooth=True)


def empty(name="pivot", loc=(0, 0, 0), parent=None):
    o = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(o); o.location = loc
    if parent is not None: o.parent = parent
    return o


def render(key, frames, pose, fps=12, mode="loop", mirror=False, note=""):
    """Render one animation: pose(i, n) sets the scene for frame i, then a multilayer EXR is written."""
    if os.environ.get("PIXEL3D_GLB"):        # export mode: first pose of the first animation as a .glb, then stop
        pose(0, frames); bpy.context.view_layer.update(); export_glb(os.environ["PIXEL3D_GLB"]); raise SystemExit(0)
    d = os.path.join(ST["out"], key); os.makedirs(d, exist_ok=True)
    sc = bpy.context.scene; vl = bpy.context.view_layer; spp = sc.cycles.samples
    for i in range(frames):
        pose(i, frames)
        for pas, n_spp, name in ((0.0, spp, "f_%04d.exr"), (1.0, 1, "i_%04d.exr")):
            vl["idpass"] = pas; sc.cycles.samples = n_spp; vl.update()
            sc.render.filepath = os.path.join(d, name % i)
            bpy.ops.render.render(write_still=True)
    sc.cycles.samples = spp; vl["idpass"] = 0.0
    ST["anims"].append(dict(key=key, frames=frames, fps=fps, mode=mode, mirror=mirror, note=note))
    print("rendered", key, frames, "frames")


def export_glb(path):
    """The same model for real-time 3D (three.js, game engines): palette colours (mid tone of each ramp), no camera,
    lights or shadow catcher. Empties keep their names, so moving parts (e.g. "head", "bed") can be animated there."""
    for o in list(bpy.data.objects):
        if o.type in ("CAMERA", "LIGHT") or o.name == "catcher": bpy.data.objects.remove(o, do_unlink=True)
    for m, d in zip(ST["mobj"], ST["mats"]):
        nt = m.node_tree; b = nt.nodes.get("Principled BSDF"); out = nt.nodes.get("Material Output")
        col = (*hex2lin(d["ramp"][len(d["ramp"]) // 2]), 1)
        b.inputs["Base Color"].default_value = col
        if d["emissive"]:
            b.inputs["Emission Color"].default_value = col; b.inputs["Emission Strength"].default_value = 2.0
        nt.links.new(b.outputs[0], out.inputs["Surface"])
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", export_cameras=False, export_lights=False, export_apply=True)
    json.dump({d["name"]: d["ramp"] for d in ST["mats"]}, open(os.path.splitext(path)[0] + ".ramps.json", "w"), indent=1)
    print("glb ->", path)


def finish():
    meta = dict(ST["cfg"], mats=ST["mats"], anims=ST["anims"])
    json.dump(meta, open(os.path.join(ST["out"], "meta.json"), "w"), indent=1)
    print("meta ->", os.path.join(ST["out"], "meta.json"))
