---
name: reel-3d-toon
description: Make short 3D toon reels (9:16, 15-25 s, 60 fps) with recurring mascot characters (El Mago, Papá Noel) for Creaciones del Mago - characters and props built in Blender (bpy), animated with three.js toon shading and mocap clips inside HyperFrames, voices with Gemini TTS, subtitles and an end card, and a QA gate that blocks any glitch or interpenetration before rendering. Use it for any new 3D/toon/animated reel, a new 3D character or prop, adding voices or subtitles to a reel, or fixing glitches, "ghosting" (things passing through bodies, walls or doors), beards or clothes sinking into a body. Reel 3D, video animado 3D, personaje 3D, voces, subtítulos, placa final, QA de contacto.
---

# reel-3d-toon

How Creaciones del Mago's 3D toon reels are made, and the mistakes we already paid for. The first full reel is
`videos/papa-noel-en-ojotas/` (`hf3d/index.html` is the reference scene: copy it to start a new one).

**Golden rules** (each one cost a re-render; the full list with causes is in `references/lecciones.md`):
1. **Voice first.** Write the dialogue and generate the voices BEFORE fixing the animation timing; the measured line
   lengths decide the beats (the Christmas reel grew from 17 to 21 s and lost half a line because voices came last).
2. **Every frame is a pure function of t.** Restore the clip snapshot before `mixer.update`, draw each t once.
3. **Nothing passes through anything**: bodies, faces, beards, hands, props, walls, door frames, door panels.
   Characters cross a doorway through its middle, square to the wall.
4. **A part resting on another moves with it**: beards, belts, scarves, capes, straps take the skin weights of the
   surface under them (`toonchar.transfer_weights`).
5. **No prop teleports**: every change of owner is animated (hand-off, toss, magic float), and the QA checks it then too.
6. **The QA gate passes before any render** (0 bad frames), then the render is checked again from pixels and audio.
7. **Measure the whole timeline.** When the person reports a problem "at the end", check every frame: the beard was
   inside the robe in 1059 of 1140 frames, not only at the end.

## Where things live (this repo)

Outside this repo, the packaged `reel-3d-toon.skill` (built by `empaquetar.sh`) carries a snapshot of these scripts in
`scripts/` and the reference scene in `assets/escena-ejemplo.html`.

| What | Path |
|---|---|
| **Shared scene kit** (stage, workshop set with day/night/dawn light, cast with colliders and beard tracking, printer, props and effects, arm IK with contact guard, springs, voices and talk nods, pill or kinetic subtitles, end card, camera rig with framed shots/whips/snap zooms/shake/flash/POV, common QA) | `videos/biblioteca/3d/web/escena3d.js` (example: `videos/invisible-no-era/hf3d/index.html`) |
| Character builder library (Blender, headless) | `videos/biblioteca/3d/toonchar.py` (lathe, tube, drape, displace, skin, smooth and **transfer** weights, AO bake, export) |
| Characters | `videos/biblioteca/3d/mago3d.py`, `santa3d.py` → `glb/*.glb` (46 CC0 mocap clips each) |
| Props | `videos/biblioteca/3d/taller_props.py`, printer `glb/printer.glb` |
| Web runtime (toon shading, outlines, Character, IK, springs, pushOut, camera) | `videos/biblioteca/3d/web/toon3d.js` |
| QA gate | `videos/biblioteca/3d/web/qa3d.cjs` (the page exposes `window.__qa(t)`) |
| Frame previews and contact sheet | `videos/biblioteca/3d/web/frames3d.cjs` |
| Flicker scan of a rendered video | `videos/biblioteca/3d/web/flicker_scan.py` |
| Voices (Gemini TTS, one take per character, cut at pauses) | `videos/biblioteca/tts_lineas.py` |
| Voice check (transcribe lines or the final mix) | `videos/biblioteca/check_voces.py` |
| Music and effects synth | `skills/pixel-reel/scripts/chiptune.py` (cues JSON, ducking, end chord) |
| Research behind the rules | `videos/RESEARCH_3D_TOON.md` (proportions), `RESEARCH_3D_FORMS.md` (weight, volume, drape), `RESEARCH_3D_CONTACT.md` (glitches and contact, rules 1-14) |

Setup in a fresh container (lost when it is reclaimed): `videos/PLAN_3D.md` → "Reinstall" (bpy in `/opt/bpy`, three.js
0.170.0 in `/opt/three`, CC0 clips in `/opt/assets3d/ual`); the build script installs Fredoka in `/opt/fonts`.

## Stages

**0. Idea and script** (`GUION.md`): one set, 2 characters max, 4-5 shots cut on action, 15-25 s. Hook in the first
2 s. Every action is a clip (walk, idle, sit, dance, interact, wave...) or an IK reach; no clip that sweeps through the
body. Ideas bank and calendar: `videos/RESEARCH_IDEAS_2026.md`, `videos/PLAN_PROXIMOS_REELS.md`.

**1. Voices first** (`references/voces-y-texto.md`): lines in `voces.json`, `python3 videos/biblioteca/tts_lineas.py
voces.json voz/` (one request per character), check each line with `check_voces.py clips`, trim with `_edits`, read
`voz/durations.json`. Now place the beats around the lines (no overlaps, ~0.05 s gaps, interjections may overlap action).

**2. Characters and props.** Reuse the library. New part resting on a body → `transfer_weights`. New character →
proportions per `RESEARCH_3D_TOON.md`, colliders sized from the meshes, beard/hat springs with gains you have MEASURED
to move visibly (the beard springs once moved 0.004 rad: invisible). Rebuild: `EGL_PLATFORM=surfaceless
/opt/bpy/bin/python mago3d.py -- glb/mago.glb` (both characters in parallel take ~1 min).

**3. Scene** (`hf3d/index.html` on the kit; copy `videos/invisible-no-era/hf3d/index.html` as the starting point): timing table `T`, routes as curves (`CatmullRomCurve3`, arc-length,
heading from the tangent), clips with measured walk speed, IK reaches queued then solved after both bodies are posed,
the contact guard, props with real radii, shots. Voices as `<audio data-who data-text>`; subtitles, talk nods and the
end card read them (one source of truth). Build: `build3d.sh` (copies libs, models, fonts, voices; makes the talk
envelopes; synthesises music and effects from `cues3d.json`).

**4. Look before you wait.** `node frames3d.cjs PORT OUT t1 t2 ...` on the risky moments (doors, contacts, hand-offs,
subtitles, card). Iterate on a window with `__qa(t)` over a few seconds before the full gate.

**5. QA gate** (`references/qa.md`): `cd hf3d && python3 -m http.server 8768 &` then
`node videos/biblioteca/3d/web/qa3d.cjs 8768 qa.json`. ~25 min for 21 s. Must report 0 violation frames, 0 jumps,
determinism true.

**6. Render**: `cd hf3d && npx hyperframes render --fps 60 --workers 4 -o ../<reel>-3d.mp4` (~15 min for 21 s on this
container's software GL). Always with the Bash tool's `run_in_background`, never `( ... ) &`.

**7. After the render**: `flicker_scan.py video.mp4 --cuts ...` (0 frames), loudness (`ffmpeg -af ebur128`, ~-13 to
-14 LUFS, peaks under -1 dB), `check_voces.py mix video.mp4` (every line intelligible), a contact sheet of real frames.

**8. Caption and delivery**: caption in `GUION.md` (hook under ~110 characters, first person singular like the website,
WhatsApp, 48 h minimum, delivery zones; no phone number in the video itself). Commit and push often; send the video.

## Secrets

The Gemini key is a network secret injected by the session proxy for `generativelanguage.googleapis.com`. Scripts send
the placeholder `proxy-injected` and never read or print a key. `.env` and `*.key` are in `.gitignore`. The repo is
public: never put a key in logs, commits, reports or generated files.
