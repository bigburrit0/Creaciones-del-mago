# 3D avatars and props with Blender: plan, pros and cons, viability

## Short answer

Yes. The approach I recommend is the **"pre-rendered sprites" pipeline** (Donkey Kong Country, Dead Cells):
- Build El Mago, Papá Noel and the props once in 3D.
- Animate them with free motion-capture animations.
- Render them as pixel art: low resolution, the reel's palette, 1 px outline, no anti-aliasing.

The result keeps the pixel-art look, but the motion comes from real animation. It is no longer 4 AI drawings, so it is neither choppy nor robotic. And the characters are always identical, because there is one model instead of one drawing per frame.

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
| 1 | **3D prop kit for the workshop**: detailed A1 printer with the print visibly growing, stool, sack with fill states, the door opening in real perspective, tree with blinking lights. Rendered as sprites into the current reel | Claude | Props with real depth in `avance-4` |
| 2 | **El Mago in 3D**: you generate a model from the approved model sheet in TRELLIS or Hunyuan3D (free web demo) and send me the `.glb`; I clean it, flatten it to toon and palette, and add the pixel face-texture system | you + Claude | A 3D Mago turntable as pixel art, for your approval |
| 3 | **Rig and animations**: upload to Mixamo, auto-rig, download 10 animations (walk, idle, happy jump, surprised, thinking, wave, throw, pick up, sit, drink). Optional: film yourself for custom moves | you | `.fbx` files |
| 4 | **Sprite factory**: I render every animation in the directions we need, as pixel-art strips at 12 fps, into the existing `pixel-reel` atlas, and re-render the reel | Claude | `avance-5`, side by side with the 2D version |
| 5 | Papá Noel, same path | you + Claude | |

Decision point after phase 2: if the 3D Mago doesn't have the charm of the 2D one, we keep 3D only for props and light (phase 1), which is already a clear win.
