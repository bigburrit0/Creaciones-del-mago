"""Builds a reel's .blend from the GLB that web/exportar_glb.cjs baked (the owner, 22/11: assets to edit in Blender).
  /opt/bpy/bin/python armar_blend.py REEL.glb REEL_hf3d_dir REEL_final.mp4 OUT.blend
In the .blend:
- the whole scene with its animation (set, props, pieces, both characters with their bones, the camera);
- the camera active, its lens keyed per frame from the reel's field of view;
- 1080 x 1920 at 30 fps, the frame range of the reel;
- in the Video Sequencer: the voices, the music, the effects (each at its time and volume) and the final mp4 as a
  reference strip (muted), to edit timing against.
Materials come in as plain colours and textures (the toon shading and the outlines were made in three.js)."""
import bpy, json, math, os, re, sys
glb, hf3d, mp4, out = sys.argv[-4:]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=os.path.abspath(glb))
sc = bpy.context.scene; cam_info = json.load(open(glb.replace(".glb", ".camara.json")))
fps = cam_info["fps"]; n = len(cam_info["fov_vertical_deg"])
sc.render.fps = fps; sc.frame_start = 1; sc.frame_end = n
sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
cam = next((o for o in bpy.data.objects if o.type == "CAMERA"), None)
if cam:
    sc.camera = cam; cd = cam.data; cd.sensor_fit = "VERTICAL"; cd.sensor_height = 36.0
    for i, fov in enumerate(cam_info["fov_vertical_deg"]):
        cd.lens = 18.0 / math.tan(math.radians(fov) / 2); cd.keyframe_insert("lens", frame=i + 1)
for o in bpy.data.objects:                                   # every animated object plays the baked clip from frame 1
    ad = o.animation_data
    if ad and ad.action is None and ad.nla_tracks:
        st = ad.nla_tracks[0].strips
        if st: ad.action = st[0].action
# the sound and the final picture, in the Video Sequencer
html = open(os.path.join(hf3d, "index.html"), encoding="utf-8").read()
sc.sequence_editor_create(); seqs = sc.sequence_editor.strips if hasattr(sc.sequence_editor, "strips") else sc.sequence_editor.sequences
ch = 2
for tag in re.findall(r'<audio[^>]*class="clip"[^>]*>', html):
    at = dict(re.findall(r'([\w-]+)="([^"]*)"', tag)); path = os.path.abspath(os.path.join(hf3d, at["src"]))
    if not os.path.exists(path): continue
    s = seqs.new_sound(at.get("id", "audio"), path, ch, int(round(float(at["data-start"]) * fps)) + 1); s.volume = float(at.get("data-volume", 1)); ch += 1
if os.path.exists(mp4):                                      # the final mp4 as a muted reference; it is looked for next to the .blend
    v = seqs.new_movie("video final (referencia)", os.path.abspath(mp4), ch, 1); v.mute = True; v.filepath = "//" + os.path.basename(mp4)
bpy.ops.file.pack_all()                                       # images and sounds travel inside the .blend
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(out), compress=True)
print("saved", out, "| objects", len(bpy.data.objects), "| actions", len(bpy.data.actions), "| frames", n)
