# 3D avatars and props with Blender: plan, pros and cons, viability

## Short answer

Yes. The approach I recommend is the **"pre-rendered sprites" pipeline** (Donkey Kong Country, Dead Cells):
- Build El Mago, Papá Noel and the props once in 3D.
- Animate them with free motion-capture animations.
- Render them as pixel art: low resolution, the reel's palette, 1 px outline, no anti-aliasing.

The result keeps the pixel-art look, but the motion comes from real animation. It is no longer 4 AI drawings, so it is neither choppy nor robotic. And the characters are always identical, because there is one model instead of one drawing per frame.

## Status (2026-11-06, evening): phase 1 done, fully-3D test made

**Installed in this cloud session** (they disappear with the container; see "Reinstall" below):
- Blender 5.2.3 as a Python module (`/opt/bpy`), plus trimesh, pygltflib, scipy, scikit-image, OpenCV, OpenEXR and gradio_client. Rigify and the FBX, glTF and BVH importers come bundled.
- Mesa software OpenGL, so EEVEE and Workbench run without a GPU.
- three.js 0.170.0 and gltf-transform (`/opt/three`).
- **Quaternius Universal Animation Library** (CC0, commercial use OK): a mannequin with 46 game-quality animations (walk, jog, idle, sit down and stand up, interact, pick up, spell cast, dance, jump, punch, push, roll, swim). Path: `/opt/assets3d/ual`.
- The FBX version of the same library: `/opt/assets3d/ual2`.
- **CMU motion capture** (free for any use) is reachable on GitHub in BVH (`una-dinosauria/cmu-mocap`, 1 GB, not downloaded yet).

**Blocked by this session's network** (the user declined opening it): Hugging Face (so no local TRELLIS / Hunyuan3D / TripoSR, and no calls to their free web demos from here), Poly Haven, Kenney, blender.org, Mixamo. Those steps stay on the user's side: web demos and Mixamo in the browser, files sent as a zip.

**Phase 1, 3D prop kit:** done.
- `videos/biblioteca/3d/taller_props.py`: printer (idle, print 13 frames with the gift growing layer by layer, printing loop, rapid fire, done), stool, sack (4 fill states + squash), Christmas tree with blinking lights, oscillating fan.
- These are rendered as pixel sprites by the new skill scripts:
  - `skills/pixel-reel/scripts/blender/pixel3d.py`, which renders light and material ids;
  - `skills/pixel-reel/scripts/pixelize3d.py`, which maps them to palette toon bands, outline, depth lines and a separate cast-shadow strip.
- The runtime got a `cast` option for those shadows.
- Result: `papa-noel-en-ojotas/avance-4.mp4`, before and after in `experimentos/antes_despues_props.png`.
- The printer moved to the right end of the bench so the wizard no longer hides it.
- Not done: the door opening in perspective. It needs a perspective camera fitted to the door painted in the background; that is the next prop.

**Fully-3D test:** `experimentos/3d-full/` (8 s, 60 fps).
- The workshop in low-poly 3D, with the Blender printer exported to `.glb`.
- The free mannequin dressed as the wizard: robe, hat, beard, nose, big chibi head. It walks in, presses the printer, watches the gift grow, and dances when the sparkles burst. All motion is mocap clips crossfaded by time, so every frame is reproducible.
- Two looks from the same scene: `3d-toon.mp4` (smooth toon 3D) and `3d-pixel.mp4` (rendered at the 270x480 art grid, snapped to the 32-colour palette with ordered dither).
- The mannequin is a stand-in: the real El Mago model comes from phase 2.

## How the "AI model comparison" 3D reels are made (the rooster videos)

Each model is given the same prompt ("make a 3D scene where a rooster runs, jumps over boxes, crashes...") and writes **one HTML file with three.js**:
- Everything is built in code from primitives (spheres, cones, boxes) with flat-shaded materials.
- Lighting is one directional light with shadow maps, plus fog.
- Animation is hand-coded with sine waves (wing flaps, hops) and simple physics for the crash and feathers.
- The page is screen-recorded, four recordings are put in a 2x2 grid, and the label shows what the API call cost.

The appeal is the side-by-side challenge format, not the quality. Our pipeline does the same kind of thing better:
- real models (Blender, image-to-3D), not primitive stacks;
- mocap animation instead of sine-wave wobbles;
- rendering frame by frame from a timeline (HyperFrames), so there are no dropped frames from screen recording;
- the brand palette, toon shading and outlines.

## Viability, tested in this environment (2026-11-06)

- **Blender runs here headless:** `bpy` 5.2.3 installs from PyPI in 30 s.
- **All three render engines work without a GPU** (after installing Mesa's software OpenGL):
  - Cycles: 0.3 s per sprite-sized frame.
  - Workbench: 0.6 s.
  - EEVEE: works, but compiles shaders slowly the first time.
- **Proof of concept:** `experimentos/3d-printer/`, a low-poly A1-style printer made in code.
  - 60-frame loop at 60 fps: bed moving front to back, head moving along the gantry.
  - Ortho 3/4 camera that matches the room; warm key light from the window, cool fill.
  - Freestyle 1-px outline, snapped to the palette (+ 5 neutral greys).
  - Render time: 18 s for the whole loop.
  - Compare it with the current flat printer in `comparacion.png`.
- **Not reachable from this session:** your Windows PC (so no live Blender connection from here) and several model-hosting sites. Steps that need a browser login (Mixamo) are yours.

## Pros and cons

| | 3D pre-rendered sprites | Current 2D (Gemini sheets) |
|---|---|---|
| Smoothness | Any number of frames, real in-betweens, mocap timing | 4–6 drawings per action |
| Consistency | One model, so it never drifts | Every frame redrawn, drift and outfit changes |
| New actions | Minutes (pick a Mixamo animation) | A new Gemini sheet, QC, often a re-ask |
| Angles and camera | Any direction, camera moves, real perspective on doors and props | One view per drawing |
| Depth and light | Real light, shadows, volume; window light can move | Faked with overlays |
| Look | Risk of looking like "3D with a pixel filter" if not tuned | Hand-drawn charm |
| Expressions | Need face textures or shape keys (more setup) | Gemini draws them easily |
| Beard, robe, hat | Need careful rigging (cloth swinging is a plus once done) | Free |
| Upfront effort | High: model, clean-up, rig, shading look | Low per sheet, high per reel |
| Cost | All free tools (see below) | Free with your Gemini plan |

The 3D route **front-loads** the work: the first character is expensive, and every reel after that is cheap. With a recurring mascot, that is the right trade.

## How to avoid choppy and robotic (the rules that matter)

1. **Motion from motion capture, not keyframes typed by me.** Mixamo's library (free, thousands of moves: walks, cheering, sitting, throwing, drinking, surprised, sad idles) or your own phone video turned into mocap.
2. **Hold the drawings, not the motion.** Render the character pose at 12 fps ("on twos/fives") for the pixel feel, while root position, camera and props move at 60 fps snapped to the grid, using the motion engine from avance 3.
3. **Hand-made look on top of 3D:**
   - flat toon shading (2–3 tones per material);
   - the reel palette;
   - 1 px outline, selective in colour;
   - render resolution equal to the art grid, never smoothed;
   - expressions as swapped 2D face textures drawn in pixel art (eyes and mouth sets), which keeps the charm and lets us reuse the 16 emotions.
4. **Secondary motion:** beard, hat tip and robe with simple bone chains or cloth, so they lag behind the body.
5. **Review loop on video** at phone size every round, as now.

## Free tools

| Need | Tool | Notes |
|---|---|---|
| 3D app | **Blender** | Runs headless here; you can open the same `.blend` files on your PC |
| Live collaboration in your Blender | **blender-mcp** (open source) + Claude Desktop on your PC | Claude creates and edits objects in your open Blender while you watch and tweak. Includes Poly Haven assets (free textures/models) |
| Model from our approved model sheet | **TRELLIS** (Microsoft, MIT), **Hunyuan3D 2.x** (Tencent, community licence), free web demos; **Meshy / Tripo / Rodin** free tiers | Image to 3D in minutes; topology is messy, Claude cleans it in Blender. Check each tool's licence for commercial use |
| Rigging | **Mixamo** auto-rigger (free with an Adobe account), **AccuRIG** (free), **Rigify** (in Blender) | Mixamo is easiest; AccuRIG handles chibi proportions better |
| Animation | **Mixamo** animations (free, commercial use OK) | Retargeted in Blender |
| Your own moves | **Rokoko Vision** (free tier, phone video → animation), **FreeMoCap** (open source) | Film yourself offering the mate, then use it as the Mago's animation |
| Assets | **Poly Haven** (CC0), **Kenney** (CC0 low-poly) | Furniture and props base meshes |
| Pixel-art look | Blender Freestyle / Line Art, palette quantize (our scripts), `pixel-reel` atlas | Already working in the proof of concept |

## Plan

| Phase | What | Who | Result |
|---|---|---|---|
| 0 | Proof of concept: 3D printer prop | Claude | **Done** (`experimentos/3d-printer/`) |
| 1 ✅ | **3D prop kit for the workshop** (done; door still pending): detailed A1 printer with the print visibly growing, stool, sack with fill states, the door opening in real perspective, tree with blinking lights. Rendered as sprites into the current reel | Claude | Props with real depth in `avance-4` |
| 2 | **El Mago in 3D**: you generate a model from the approved model sheet in TRELLIS or Hunyuan3D (free web demo) and send me the `.glb`; I clean it, flatten it to toon and palette, and add the pixel face-texture system | you + Claude | A 3D Mago turntable as pixel art, for your approval |
| 3 | **Rig and animations**: upload to Mixamo, auto-rig, download 10 animations (walk, idle, happy jump, surprised, thinking, wave, throw, pick up, sit, drink). Optional: film yourself for custom moves | you | `.fbx` files |
| 4 | **Sprite factory**: I render every animation in the directions we need, as pixel-art strips at 12 fps, into the existing `pixel-reel` atlas, and re-render the reel | Claude | `avance-5`, side by side with the 2D version |
| 5 | Papá Noel, same path | you + Claude | |

Decision point after phase 2: if the 3D Mago doesn't have the charm of the 2D one, we keep 3D only for props and light (phase 1), which is already a clear win.

## Reinstall in a new cloud session

```
apt-get install -y libegl1 libgl1 libegl-mesa0 libgl1-mesa-dri libgles2 libxi6 libxkbcommon0 libsm6 libxxf86vm1 libxfixes3 libxrender1
python3 -m venv /opt/bpy && /opt/bpy/bin/pip install bpy==5.2.3 numpy pillow scipy scikit-image trimesh pygltflib opencv-python-headless gradio_client OpenEXR
git clone --depth 1 https://github.com/J-Ponzo/gltf-universal-animation-library.git /opt/assets3d/ual
videos/experimentos/3d-full/build.sh        # three.js + mocap library + printer.glb into hf/
```
Run Blender scripts with `EGL_PLATFORM=surfaceless /opt/bpy/bin/python script.py -- args`.
Props: `cd videos/biblioteca/3d && EGL_PLATFORM=surfaceless /opt/bpy/bin/python taller_props.py -- all RENDER_DIR`, then `pixelize3d.py RENDER_DIR/<prop> sprites` for each prop, then `assemble.py` as usual.
