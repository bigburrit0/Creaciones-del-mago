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

## Result

- **Gate:** 1020 of 1020 frames with zero contact violations and zero pose jumps, and identical pixels for a frame drawn in any order.
- The gate's history while fixing (bad frames): 448 → 313 → 22 → 6 → 1 → 0.
- After the render, the frame-difference scan is run again on the video as a second, image-based signal.
