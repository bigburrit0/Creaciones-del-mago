# 3D toon El Mago: research synthesis and what was applied

The user chose **3D toon** as the direction (2026-11-06) and asked for a Haiku research team to fix the "weird proportions" and get good animation.

Six agents, each with a different angle:
1. character designer (chibi proportions);
2. technical animator (mocap retargeting);
3. feature/Nintendo animator (toon motion);
4. real-time graphics engineer (three.js toon rendering);
5. Blender technical artist (modelling in Python);
6. short-form video director (vertical reels).

Many sites were blocked by the session's network (docs.blender.org, threejs.org, clip-studio and others). The agents worked from search snippets and marked their own inferences. The numbers below are starting points, and each was checked on renders.

## Why the first try looked wrong

- A realistic adult mannequin, 7.5 heads tall, under a scaled-up head and a cone robe. Long thin limbs and a tiny body under a big head: the classic chibi mistake (R1).
- Inverted-hull outlines on split normals made spikes on the hat cone and brim (R4).
- The camera was too close, so the character filled the frame and hid the printer. The staging had his back to the camera.

## Decisions

| Topic | Rule | Applied in |
|---|---|---|
| Proportions | Body ~3 heads without the hat. No neck: shoulders right under the chin. Belt at ~0.36 of height. Robe hem just above stubby boots. Short arms with mitten hands at belt level. Shoulders ~1.4 head widths. The hat counts outside the body: ~1 head high, brim ~1.9 face widths, tip droops back and curls (as on the model sheet). Beard from the cheeks to the belt | `biblioteca/3d/mago3d.py` |
| Retarget | Shorten bones and keep orientation and roll, so the clips' local rotations still fit. Scale hips translation by the leg ratio (0.32) | `mago3d.py`, applied to all 46 clips |
| Foot sliding | Walk speed is measured from the clip: how fast a planted foot slides back, times playback speed. Path length / speed = walk duration | `mago-toon/hf/index.html` (`stanceSpeed`) |
| Robe | Weighted to the torso. Only the lower robe follows the thighs, at most 28%: a heavy robe, no skew | `skin_robe` |
| Secondary motion | Springs on the hat (2.3 Hz, damping 0.3) and beard (1.8 Hz, 0.35), tapered along the chain and driven by the head's acceleration. Simulated once over the whole timeline, so seeking stays deterministic | `springs()` |
| Face | Blink every 3–5 s: close in 4 frames, closed 2, open in 6 (at 60 fps). Double blink after the surprise. Brows up at the press and the pop. Head tilt ~8° while watching. Dot eyes with a white glint | `poseAt()`, `mago3d.py` |
| Squash | Volume-preserving stretch on the surprise, capped at 6% | `poseAt()` |
| Toon look | 3 bands (0.42 / 0.72 / 1.0). Warm Fresnel rim light. Plum outlines (not black) on smoothed normals. No tone mapping. Warm fog. Hemisphere ~1.0 plus a warm key from the window. Additive light shaft and dust motes. Blob contact shadow. CSS vignette | `index.html` |
| Framing | Longer lens (28°), camera 3–4.5 m away for a cozy diorama feel. Keep the action away from the top 220 px and bottom 450 px (Instagram UI). Character ~35–45% of frame height. The camera arcs to see his face while he watches; it goes low and frontal for the payoff, so his face reads under the brim | camera keys `CAM` |
| Story | Hook in the first 1.5 s (he is already walking in, the printer glows). One clear action every 1–1.5 s. Celebration under 2 s, then a calmer end pose | 10 s timeline |
| Sound | SFX on every hit (steps, click, printer, ding, pop, sparkle, whoosh, victory), a light original melody, birds | `mago-toon/cues.json` |

## Still open

- **Mocap clips are generic.** Dance and Interact are game moves. For signature actions (offering the mate, drinking it, a magic gesture), film yourself and convert the video to mocap, or keyframe a few poses in Blender.
- **Arms can clip into the robe** in some clips. There is a hook in `poseAt()` for an arm-spread offset.
- **Papá Noel 3D:** same recipe, different body.
