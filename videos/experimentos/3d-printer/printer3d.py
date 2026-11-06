"""Proof of concept: low-poly bed-slinger 3D printer (A1-like) rendered as a pixel-art sprite strip.
run: python printer3d.py -- OUT_DIR
"""
import bpy, math, sys, os
out = sys.argv[-1]; os.makedirs(out, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
FPS, N = 60, 60                      # one-second loop at 60 fps

def mat(name, rgb, rough=0.6, emit=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough
    if emit:
        b.inputs["Emission Color"].default_value = (*rgb, 1); b.inputs["Emission Strength"].default_value = emit
    return m

def hexrgb(h):  # sRGB hex -> linear
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return tuple((v / 12.92) if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c)

def box(name, size, loc, m, parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.name = name
    o.scale = size; bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m)
    bev = o.modifiers.new("bev", "BEVEL"); bev.width = min(size) * 0.12; bev.segments = 1
    if parent: o.parent = parent
    return o

def cyl(name, r, d, loc, rot, m):
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=r, depth=d, location=loc, rotation=rot); o = bpy.context.object
    o.name = name; o.data.materials.append(m); return o

white = mat("white", hexrgb("#E9E4DA")); grey = mat("grey", hexrgb("#8C8A92")); dark = mat("dark", hexrgb("#2A2733"))
plate = mat("plate", hexrgb("#3A3550"), 0.3); gold = mat("gold", hexrgb("#F2C14E"), 0.4)
screen = mat("screen", hexrgb("#9BC46A"), 0.2, emit=2.0); nozzle = mat("nozzle", hexrgb("#E86A4A"), 0.3, emit=4.0)
red = mat("red", hexrgb("#C0392B"), 0.5)

# --- static frame
base = box("base", (1.9, 1.5, 0.22), (0, 0, 0.11), white)
box("screen", (0.38, 0.04, 0.14), (0.55, -0.76, 0.13), screen)
col = box("column", (0.18, 0.22, 1.7), (-0.88, 0.25, 1.05), grey)
box("top", (0.3, 0.3, 0.12), (-0.88, 0.25, 1.95), white)
spool = cyl("spool", 0.32, 0.16, (-0.88, 0.55, 2.2), (math.pi / 2, 0, 0), gold)
cyl("hub", 0.12, 0.2, (-0.88, 0.55, 2.2), (math.pi / 2, 0, 0), dark)
# --- moving parts
bed = box("bed", (1.35, 1.25, 0.06), (0.1, 0, 0.3), plate)
box("print", (0.34, 0.34, 0.2), (0.1, 0, 0.43), red, parent=bed)          # the gift being printed
gantry = box("gantry", (1.75, 0.12, 0.1), (0.02, 0.25, 1.35), dark)
head = box("head", (0.3, 0.28, 0.36), (0.1, 0.12, 1.2), white)
box("nozzle", (0.06, 0.06, 0.14), (0.1, 0.1, 0.96), nozzle, parent=head)
box("fan", (0.22, 0.03, 0.22), (0.1, -0.03, 1.2), dark, parent=head)

sc.frame_start, sc.frame_end, sc.render.fps = 0, N - 1, FPS
for f in range(N):
    t = f / N
    head.location.x = -0.35 + 0.7 * (0.5 - 0.5 * math.cos(2 * math.pi * t * 2))     # X back and forth twice
    head.keyframe_insert("location", index=0, frame=f)
    bed.location.y = 0.25 * math.sin(2 * math.pi * t)                                # bed slings front/back
    bed.keyframe_insert("location", index=1, frame=f)
for o in (head, bed):
    for fc in o.animation_data.action.fcurves if hasattr(o.animation_data.action, "fcurves") else []:
        for k in fc.keyframe_points: k.interpolation = "LINEAR"

# --- light: warm key from upper-left (window), cool fill
bpy.ops.object.light_add(type="SUN", rotation=(math.radians(50), math.radians(-25), math.radians(-40)))
bpy.context.object.data.energy = 4.0; bpy.context.object.data.color = (1.0, 0.92, 0.75)
bpy.ops.object.light_add(type="SUN", rotation=(math.radians(60), math.radians(30), math.radians(140)))
bpy.context.object.data.energy = 0.8; bpy.context.object.data.color = (0.6, 0.65, 1.0)
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.35, 0.3, 0.4, 1); w.node_tree.nodes["Background"].inputs[1].default_value = 0.6

# --- camera: orthographic 3/4 top-down, like the room
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = "ORTHO"; cam.data.ortho_scale = 4.3
cam.location = (0.1, -6.0, 6.0); cam.rotation_euler = (math.radians(47), 0, 0)
sc.render.resolution_x = sc.render.resolution_y = 64; sc.render.resolution_percentage = 100                 # one art pixel per render pixel
sc.render.film_transparent = True
sc.render.engine = "CYCLES"; sc.cycles.samples = 96; sc.cycles.device = "CPU"; sc.cycles.use_denoising = True
sc.render.filter_size = 0.01                                          # no anti-aliasing blur across pixels
sc.view_settings.view_transform = "Standard"
# outline: Freestyle, 1 px
sc.render.use_freestyle = True; sc.render.line_thickness_mode = "ABSOLUTE"; sc.render.line_thickness = 1.0
fs = bpy.context.view_layer.freestyle_settings
ls = fs.linesets[0] if len(fs.linesets) else fs.linesets.new("outline")
if ls.linestyle is None: ls.linestyle = bpy.data.linestyles.new("outline")
ls.linestyle.color = hexrgb("#150A34"); ls.linestyle.thickness = 1.0
ls.select_by_visibility = True; ls.select_silhouette = True; ls.select_border = True; ls.select_crease = True
sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_mode = "RGBA"
sc.render.filepath = os.path.join(out, "f_")
bpy.ops.render.render(animation=True)
print("rendered", N, "frames ->", out)
