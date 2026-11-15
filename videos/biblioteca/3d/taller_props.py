"""3D prop kit for the workshop set (taller), rendered as pixel-art sprites (pre-rendered sprites pipeline).

  EGL_PLATFORM=surfaceless /opt/bpy/bin/python taller_props.py -- PROP RENDER_ROOT
  /opt/bpy/bin/python ../../../skills/pixel-reel/scripts/pixelize3d.py RENDER_ROOT/PROP sprites

PROP: printer | stool | sack | tree | fan | all. Units: 1 BU = 10 art px. Origin = floor contact point (anchor).
Palette ramps come from biblioteca/sprites.json (project.style.palette).
"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "skills", "pixel-reel", "scripts", "blender"))
import bpy
import pixel3d as P

args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
WHICH, ROOT = args[0], args[1]
ease = lambda f: 0.5 - 0.5 * math.cos(math.pi * f)
OUT = "#150A34"


def ramps():
    return dict(
        white=P.mat("white", ["#C8AE88", "#D8D4C8", "#FBF4E4"], line="#5B4636"),
        dark=P.mat("dark", ["#150A34", "#2E2160", "#4B3A8E"], line=OUT),
        gold_bed=P.mat("bed", ["#6E3B22", "#C98A2B", "#F2B640"], line="#5A3424"),
        red=P.mat("red", ["#7A1E22", "#C0392B", "#E86A4A"], line="#5A3424"),
        gold=P.mat("gold", ["#C98A2B", "#F2C14E", "#FFF3B0"], line="#6E3B22"),
        wood=P.mat("wood", ["#5A3424", "#8A5638", "#A0603A", "#B08A5A"], line="#5A3424"),
    )


# ------------------------------------------------------------------ printer (A1-mini style bed slinger)
def printer():
    P.scene(os.path.join(ROOT, "printer"), cell=(80, 80), anchor=(40, 71), ppu=13)
    M = ramps()
    scr_blue = P.mat("screen", ["#9CC9E8"], emissive=True); scr_green = P.mat("screen_ok", ["#9BC46A"], emissive=True)
    glow = P.mat("nozzle_hot", ["#F2C14E"], emissive=True)
    root = P.empty("root"); root.rotation_euler.z = math.radians(-14)          # left of centre: show the right side
    P.box((3.4, 2.2, 0.38), (0, 0, 0.19), M["white"], root, name="base")
    screen = P.box((0.7, 0.06, 0.2), (0.95, -1.11, 0.2), scr_blue, root, bevel=0, name="screen")
    P.box((2.0, 0.08, 0.06), (-0.2, -1.11, 0.33), M["dark"], root, bevel=0, name="lip")
    bed = P.empty("bed", (0.25, 0, 0.38), root)
    P.box((2.3, 1.9, 0.1), (0, 0, 0.05), M["dark"], bed, name="carrier")
    P.box((2.5, 2.0, 0.07), (0, 0, 0.13), M["gold_bed"], bed, bevel=0.02, name="plate")
    # the gift being printed (sits on the plate, grows in z)
    prt = P.empty("print", (0, 0.05, 0.17), bed)
    P.box((0.8, 0.8, 0.85), (0, 0, 0.425), M["red"], prt, bevel=0.03, name="giftbox")
    P.box((0.83, 0.18, 0.86), (0, 0, 0.43), M["gold"], prt, bevel=0, name="ribbon1")
    P.box((0.18, 0.83, 0.86), (0, 0, 0.43), M["gold"], prt, bevel=0, name="ribbon2")
    bow = P.empty("bow", (0, 0, 0.9), prt)
    P.torus(0.16, 0.06, (-0.14, 0, 0.05), M["gold"], (0, math.radians(90), math.radians(30)), bow)
    P.torus(0.16, 0.06, (0.14, 0, 0.05), M["gold"], (0, math.radians(90), math.radians(-30)), bow)
    # column, spool
    P.box((0.42, 0.5, 3.25), (-1.5, 0.45, 0.38 + 1.62), M["white"], root, name="column")
    P.box((0.12, 0.04, 2.8), (-1.5, 0.19, 0.38 + 1.55), M["dark"], root, bevel=0, name="slot")
    P.box((0.5, 0.6, 0.18), (-1.5, 0.45, 3.68), M["dark"], root, name="cap")
    sp = P.empty("spool", (-1.45, 0.45, 4.4), root)                          # axis along x, turned: flange + red band
    sp.rotation_euler.z = math.radians(38)
    P.cyl(0.62, 0.52, (0, 0, 0), M["red"], (0, math.radians(90), 0), 24, sp, name="filament")
    for s in (-1, 1): P.cyl(0.74, 0.07, (s * 0.3, 0, 0), M["dark"], (0, math.radians(90), 0), 24, sp, name="flange")
    P.cyl(0.2, 0.75, (0, 0, 0), M["white"], (0, math.radians(90), 0), 12, sp, name="hub")
    # gantry + toolhead (move together in z; head slides in x)
    gan = P.empty("gantry", (0, 0, 2.0), root)
    P.box((3.0, 0.26, 0.28), (0.1, 0.25, 0), M["dark"], gan, name="xrail")
    head = P.empty("head", (0.25, 0, 0), gan)
    P.box((0.62, 0.56, 0.74), (0, 0.02, -0.12), M["white"], head, name="toolhead")
    P.cyl(0.17, 0.04, (0, -0.27, -0.08), M["dark"], (math.radians(90), 0, 0), 12, head, name="fan")
    noz = P.cyl(0.1, 0.16, (0, 0.02, -0.57), M["dark"], (0, 0, 0), 8, head, name="nozzle", r2=0.03)
    # filament tube: a bezier from the spool to the top of the head
    cu = bpy.data.curves.new("tube", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = 0.07; cu.bevel_resolution = 1
    spl = cu.splines.new("BEZIER"); spl.bezier_points.add(2)
    tube = bpy.data.objects.new("tube", cu); bpy.context.scene.collection.objects.link(tube); tube.parent = root
    tube.data.materials.append(M["white"])
    BED_TOP = 0.38 + 0.17

    def set_tube():
        hx, hz = head.location.x, gan.location.z + 0.25
        pts = [(-1.1, 0.3, 4.0), (-0.3, 0.1, 4.1), (hx, 0.02, hz)]
        for bp, p in zip(spl.bezier_points, pts):
            bp.co = p; bp.handle_left_type = bp.handle_right_type = "AUTO"

    def pose(hx, by, h, hot, ok=False, bowon=False, nozzle_z=None):
        head.location.x = hx; bed.location.y = by
        prt.scale.z = max(h, 1e-3) / 0.85; prt.hide_render = h <= 0.01
        bow.hide_render = not bowon
        for o in bow.children: o.hide_render = not bowon
        for o in prt.children: o.hide_render = h <= 0.01 or (o in bow.children and not bowon)
        nz = nozzle_z if nozzle_z is not None else BED_TOP + h + 0.02
        gan.location.z = nz + 0.65
        noz.data.materials[0] = glow if hot else M["dark"]
        screen.data.materials[0] = scr_green if ok else scr_blue
        set_tube()

    P.render("obj.printer3d_idle", 1, lambda i, n: pose(0.75, 0.25, 0, False, nozzle_z=1.75), fps=8, mode="static")
    def printing(i, n):
        f = (i + 1) / n
        pose(0.25 + 0.32 * math.sin(i * 2.3), 0.28 * math.sin(i * 1.15), 0.85 * f, True)
    P.render("obj.printer3d_print", 13, printing, fps=20, mode="once")
    def loop(i, n):                       # steady printing, print half done (for long holds)
        pose(0.25 + 0.32 * math.sin(2 * math.pi * i / n * 2), 0.28 * math.sin(2 * math.pi * i / n), 0.45, True)
    P.render("obj.printer3d_loop", 12, loop, fps=20, mode="loop")
    def rapid(i, n):                      # three frames at 30 fps = one gift every 0.1 s
        pose([0.0, 0.5, 0.25][i], [-0.2, 0.2, 0.0][i], [0.4, 0.85, 0][i], i < 2)
    P.render("obj.printer3d_rapid", 3, rapid, fps=30, mode="loop")
    P.render("obj.printer3d_done", 1, lambda i, n: pose(0.9, 0.0, 0.85, False, ok=True, bowon=True, nozzle_z=1.75),
             fps=8, mode="static")
    P.finish()


# ------------------------------------------------------------------ stool
def stool():
    P.scene(os.path.join(ROOT, "stool"), cell=(40, 40), anchor=(20, 34), ppu=13)
    M = ramps()
    root = P.empty("root"); root.rotation_euler.z = math.radians(20)
    P.cyl(0.85, 0.22, (0, 0, 1.24), M["wood"], verts=20, parent=root, name="seat")
    for k in range(3):
        a = math.radians(90 + k * 120); x, y = 0.55 * math.cos(a), 0.55 * math.sin(a)
        leg = P.cyl(0.11, 1.3, (x * 0.9, y * 0.9, 0.62), M["wood"], verts=6, parent=root, name="leg", r2=0.09)
        leg.rotation_euler = (-y * 0.18, x * 0.18, 0)
    P.torus(0.5, 0.05, (0, 0, 0.45), M["wood"], parent=root, name="ring")
    P.render("obj.stool3d", 1, lambda i, n: None, fps=8, mode="static")
    P.finish()


# ------------------------------------------------------------------ sack (fill states)
def sack():
    P.scene(os.path.join(ROOT, "sack"), cell=(48, 48), anchor=(24, 42))
    M = ramps()
    red = P.mat("sack", ["#5A3424", "#7A1E22", "#C0392B", "#E86A4A"], dither=0.6, line="#5A3424")
    root = P.empty("root"); root.rotation_euler.z = math.radians(15)
    objs = []

    def build(fill):
        for o in objs: bpy.data.objects.remove(o, do_unlink=True)
        objs.clear()
        R = 0.55 + 0.75 * fill; Ht = 0.5 + 1.6 * fill          # body radius and height grow with the fill
        flat = 1.0 + 0.6 * (1 - fill)                           # an empty sack slumps wide
        prof = [(R * flat * 0.7, 0.0), (R * flat, 0.12 + 0.1 * fill), (R * flat * 1.02, Ht * 0.45),
                (R * 0.9, Ht * 0.75), (R * 0.45, Ht * 0.95), (0.16, Ht + 0.12), (0.2, Ht + 0.3), (0.34, Ht + 0.55), (0.1, Ht + 0.62)]
        lumps = lambda a, z: 1 + fill * 0.07 * math.sin(3 * a + z * 4) + 0.04 * math.sin(5 * a)
        body = P.lathe(prof, red, parent=root, name="sack", wobble=lumps)
        body.rotation_euler.y = math.radians(8 * (1 - fill))   # empty: tips over a little
        rope = P.torus(0.22, 0.07, (0, 0, Ht + 0.15), M["gold"], parent=root, name="rope")
        rope.rotation_euler.y = body.rotation_euler.y
        objs.extend([body, rope])

    states = [0.05, 0.4, 0.7, 1.0]
    P.render("obj.sack3d", 4, lambda i, n: build(states[i]), fps=8, mode="states")
    # squash on impact: full sack, 6 frames at 20 fps (scale wobble), use after a gift lands
    def squash(i, n):
        build(1.0); s = [0.82, 1.12, 0.94, 1.04, 0.98, 1.0][i]
        root.scale = (1 / math.sqrt(s), 1 / math.sqrt(s), s)
    P.render("obj.sack3d_squash", 6, squash, fps=20, mode="once")
    root.scale = (1, 1, 1)
    P.finish()


# ------------------------------------------------------------------ Christmas tree with blinking lights
def tree():
    P.scene(os.path.join(ROOT, "tree"), cell=(32, 40), anchor=(16, 36))
    M = ramps()
    green = P.mat("leaves", ["#1E3A2A", "#2F5A32", "#5C9A4A", "#9BC46A"], dither=0.5, line="#1E3A2A")
    pot = P.mat("pot", ["#7A1E22", "#C0392B", "#E86A4A"], line="#5A3424")
    star = P.mat("star", ["#FFF3B0"], emissive=True)
    bulbs = [P.mat("bulb_r", ["#E86A4A"], emissive=True), P.mat("bulb_y", ["#F2C14E"], emissive=True),
             P.mat("bulb_b", ["#9CC9E8"], emissive=True), P.mat("bulb_off", ["#2E2160"], emissive=True)]
    root = P.empty("root")
    P.cyl(0.38, 0.4, (0, 0, 0.2), pot, verts=12, parent=root, name="pot", r2=0.46)
    P.cyl(0.12, 0.4, (0, 0, 0.55), M["wood"], verts=6, parent=root)
    for k, (r, z, h) in enumerate([(0.95, 0.65, 1.1), (0.75, 1.3, 0.95), (0.52, 1.9, 0.85)]):
        P.cyl(r, h, (0, 0, z + h / 2), green, verts=10, parent=root, name="tier", r2=0.08)
    st = P.sphere(0.16, (0, 0, 2.85), star, scale=(1, 0.5, 1), parent=root)
    lights = []
    for k in range(9):                    # a spiral of bulbs on the front half
        f = k / 8; a = math.radians(-160 + 140 * (k % 3) + 20 * k); z = 0.8 + 1.85 * f; r = 0.9 - 0.6 * f + 0.06
        lights.append(P.sphere(0.13, (r * math.cos(a), -abs(r * math.sin(a)) - 0.1, z), bulbs[0], parent=root, seg=8))
    def blink(i, n):
        for k, o in enumerate(lights):
            o.data.materials[0] = bulbs[(k + i) % 3] if (k + i) % 4 != 3 else bulbs[3]
    P.render("obj.tree3d", 4, blink, fps=4, mode="loop")
    P.finish()


# ------------------------------------------------------------------ desk fan, oscillating, spinning blades
def fan():
    P.scene(os.path.join(ROOT, "fan"), cell=(40, 40), anchor=(20, 35), ppu=16)
    M = ramps()
    blue = P.mat("fan_blue", ["#2B4C7E", "#4F86C6", "#9CC9E8"], line="#150A34")
    cage = P.mat("cage", ["#4B3A8E", "#D8D4C8", "#FBF4E4"], line="#2E2160")
    root = P.empty("root")
    P.cyl(0.6, 0.12, (0, 0, 0.06), blue, verts=16, parent=root, name="base")
    P.cyl(0.08, 0.9, (0, 0, 0.55), cage, verts=6, parent=root, name="stem")
    head = P.empty("head", (0, 0, 1.1), root)
    P.sphere(0.25, (0, 0.2, 0), blue, scale=(1, 1.3, 1), parent=head, name="motor")
    P.torus(0.62, 0.035, (0, -0.15, 0), cage, (math.radians(90), 0, 0), head, name="rim")
    rotor = P.empty("rotor", (0, -0.1, 0), head); rotor.rotation_euler.x = math.radians(90)
    for k in range(3):
        b = P.sphere(0.3, (0, 0.3, 0), blue, scale=(0.55, 1, 0.12), parent=rotor, name="blade", seg=10)
        piv = P.empty("bp", (0, 0, 0), rotor); b.parent = piv; piv.rotation_euler.z = math.radians(120 * k)
    P.cyl(0.08, 0.1, (0, -0.2, 0), cage, (math.radians(90), 0, 0), 8, head, name="cap")
    def osc(i, n):
        head.rotation_euler.z = math.radians(38 * math.sin(2 * math.pi * i / n))
        rotor.rotation_euler.y = math.radians(i * 47)     # strobe-friendly step
    P.render("obj.fan3d", 24, osc, fps=12, mode="loop")
    P.finish()


ALL = dict(printer=printer, stool=stool, sack=sack, tree=tree, fan=fan)
for name in (ALL if WHICH == "all" else [WHICH]):
    ALL[name]()
