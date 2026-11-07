# 3D toon: no glitches, nothing passes through a body

The user saw "glitching on the characters", and the mate "ghosting" through bodies when they drink. They asked for this to absolutely not happen, using the research team.

Three Haiku agents researched it:
1. rendering-glitch debugger;
2. gameplay animator for props, drinking and hand-offs;
3. QA tools engineer for interpenetration and glitch detection.

Several hosts were blocked (threejs.org, littlepolygon, vulkan docs), so numbers marked as inference were checked on our own frames.

## What was wrong (measured)

- **Glitch:** one frame in three, in four windows (4.75–5.15 s, 7.15–7.85 s, 9.15–10.0 s, around 10.55 s), showed a different pose: Santa's head dropped and the image shifted. Found by a frame-difference scan of the render: frames unlike both neighbours.
- **Cause:** three.js `AnimationMixer` only writes a bone when its sampled value changed since the last update. HyperFrames sometimes draws the same frame twice, through both the GSAP `onUpdate` and `hf-seek`. On the second draw the mixer skipped the bones, so our layers on top (world rotations, IK) were applied twice. Proved by rendering the same t twice: different pixels.
- **Ghosting:**
  - The drinking IK target was the mouth itself, inside the beard and moustache volume.
  - The hand-over point was inside Santa's belly, and the characters stood 2 cm apart.
  - El Mago's casting clip swept his arm 15 cm through his own beard.
  - The sack slid through Santa's legs, and gifts flew through hat tips.

## Rules applied

| # | Rule | Where |
|---|---|---|
| 1 | Every frame is rebuilt from the pure clip pose: restore the last clip snapshot before `mixer.update`, snapshot after. Draw each t once | `toon3d.js` `Character.apply`, `renderAt` |
| 2 | Crossfades are eased and overlap; if no clip is active, hold the nearest (never the bind pose: that caused a one-frame T-pose) | `Character.apply` |
| 3 | IK guarded against NaN: degenerate vectors, opposite `setFromUnitVectors` inputs, zero pole | `aim`, `ikArm` |
| 4 | Collision proxies per character, bone-attached and sized from the meshes: head, face, moustache tips, beard (two), robe or belly, chest, hips, legs, the jacket knot, hat base and tip, the brim as a flat disc, arms | `addCollider`, scene |
| 5 | IK targets = surface + normal × clearance (0.055 m). The hand travels along a path pushed outside every body on each frame. After solving, the **palm** (not the wrist) is checked and the target pushed again | `armNow`, `pushOut` |
| 6 | The elbow's bend plane starts as the clip's own and turns gradually to the designed pole (no elbow flip), and the IK takes over with an ease | `armNow` |
| 7 | **Drinking:** the straw tip reaches the moustache line; the gourd (r 0.054) stays in front of the beard with clearance and is tilted 43° toward the face; the head leans in 5°; the hand grips the side of the gourd | `drinkPose` |
| 8 | **Hand-over:** at a meeting point between the two bodies, at chest height, toward the camera and outside both; the hands meet 9 cm from it; the mate is pinned there during the swap | `P1`, `P2` |
| 9 | A contact guard every frame, after clips and IK: a hand about to enter a face, beard or hat, or the other character, is bent back out with minimal change. Arms already steered by a reach are skipped | end of `poseAt` |
| 10 | Props are kept outside bodies with their real size: the sack (lathe radius 0.17 × fill scale), gifts, the mate | `props` |
| 11 | Choreography rules: no clip that sweeps through the body (El Mago's throw is IK: wind-up beside the head, release, follow-through). Santa fans with the hand away from El Mago. The sack is lifted over his legs. Gifts fly high. Heading keys are sorted and start inside their own segment. Two reaches never overlap on the same arm | scene |
| 12 | **QA gate** before every render (`biblioteca/3d/web/qa3d.cjs`), every frame, exact checks against the posed skinned meshes. It covers the mate, hands, the sack, gifts, bodies vs bodies, NaN bones, pose jumps and determinism. Exit 1 on any failure | |
| 13 | **Walls and doors are solid too** (added 2026-11-07, after "Santa ghosts through the door"). The gate samples every collider (arms included) and the sack against the back wall, the door frame and the swinging door panel (a box on its hinge). A wide character crosses a doorway through its MIDDLE and square to the wall (a curve: in through the centre, then turn), never on the diagonal. The doorway is sized from the widest body plus the sack (0.84 m for Santa). He waves well inside the room, puts the sack on his back (centred) only while turning to leave, and walks straight out; the door swings into the room, so it closes behind him without touching him | `PIN`, `POUT`, `qa()` |
| 14 | **A part that rests on another takes the weights of the surface under it** (added 2026-11-07, after "the beard ghosts through the body at the end"). Measured: the beard tip sank 4–6.5 cm into the robe and belt in EVERY frame (Santa: 1.6–3.6 cm into the tank top). The beard followed the chest bones (spine.003/.002 and the springs) while the belt and robe follow the hips, so any pose that bends the spine apart from the bind pose drives them through each other. Fix: `toonchar.transfer_weights()` gives each beard vertex below the chin the interpolated weights of the nearest robe, belt or shirt point, blending to the head weights at the chin; no spring bones on the resting part. The gate tracks 460 (El Mago) and 439 (Santa) beard points that rest on the body: none may sink more than 1.2 cm along the body normal | `toonchar.py`, `mago3d.py`, `santa3d.py`, `qa()` |

| 15 | **The gate measures what is visible.** A beard's inner face compressing against the chin is fine; the body coming within 8 mm of the beard's OUTER surface is not (1.2 cm where the beard is thin). Thresholds are written next to each check | `qa()` |
| 16 | **No blind windows and no teleports.** A prop changing hands is animated (hand-off, toss, magic float with a catch reach) and checked while in flight | `poseAt`, `qa()` |
| 17 | **Carried props hide with their carrier.** A sack trailing behind someone who turns behind a wall stays visible and floats: centre it on the body and walk straight away | `props` |

The full list of lessons (with the voice, subtitle, camera and process ones) is in `skills/reel-3d-toon/references/lecciones.md`.

## Result

- **Gate:** 1020 of 1020 frames with zero contact violations and zero pose jumps, and identical pixels for a frame drawn in any order.
- The gate's history while fixing (bad frames): 448 → 313 → 22 → 6 → 1 → 0.
- After the render, the frame-difference scan is run again on the video as a second, image-based signal.
- **21 s version (2026-11-07), with rules 13–14:** before the fix, the new checks found Santa crossing the wall at the door (entering on the diagonal, the sack and the waving arm behind the wall on the way out) and the beard sunk into the body in 1059 (El Mago) and 1047 (Santa) of 1140 frames. Gate history (bad frames): 1140 → 299 → 82 → 5 → **0 of 1260**, zero pose jumps, deterministic. The render's flicker scan found 0 flicker frames. The final mix was transcribed with Gemini to check that every voice line is intelligible over the music and effects (all 7 spoken lines: yes).
