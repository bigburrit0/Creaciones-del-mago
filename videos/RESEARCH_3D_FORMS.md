# 3D toon: weight, volume, shapes that rest on shapes. Improvement categories

The user asked (2026-11-06) for 3D shapes that behave like real things: the beard must lie on the chest instead of going into it, objects must have weight, and the forms need more appeal.

Six Haiku agents researched one category each. Several sources were blocked by the session network (80.lv, graphics.pixar.com, docs.blender.org, littlepolygon), so many numbers are marked as the agents' own inference. They are starting values, checked on renders.

## The categories

| # | Category | What was wrong | Rules we adopt (numbers to start from) |
|---|---|---|---|
| 1 | **Contact and draping** | The beard was a separate wedge pushed into the chest. The belt and brim are approximate | Build parts that rest on others by projecting onto the support surface: ray-cast or BVH nearest point on the body, plus a thickness offset (a procedural shrinkwrap). Thin where it touches, thicker where it hangs free; the tip lifts off. Extend the contact edge 0.5–1% under the support so there is no gap. Size belt and brim radii from the measured body and head radius. Springs collide: the beard can't rotate into the chest, cone limits of 15–25° (beard) and more for the hat tip |
| 2 | **Weight and mass in motion** | Mocap feels light and floaty | Hip drop of 2.5–4 cm at contact, reached 3–4 frames after it. Side weight shift ±1.5 cm. The head lags the hips (spring 3–4 Hz, ζ 0.5). Heavy parts on springs: belly 1.6–2.2 Hz ζ 0.2, beard 2.5–3 Hz ζ 0.3, robe hem 3–4 Hz ζ 0.35. A heavy sit ("plop"): 6-frame drop with ease-in, impact squash Y 0.88 / XZ 1.06, a 1.5 cm rebound, settle in 20 frames; the stool dips 1.5 cm at 3 Hz. Exhausted Santa: torso 6–10° forward, head 5° down, steps ×0.8, slow breathing (0.3 Hz, 2%). Toss: 5 frames of anticipation, follow-through 4–6 frames, a gravity arc. Slow the mocap 10–15% for heavy characters |
| 3 | **Volume and deformation** | Linear skinning collapses joints; the robe can skew with the legs | Distance falloff weights plus 3–5 Laplacian smoothing passes at the joints, at most 4 influences, normalised. Robe on the pelvis and spine only, with the hem following the legs at most 28%. Seams share weights; parts overlap 1–2 rings. Enough rings at the elbows and knees (5+), 12–16 segments around |
| 4 | **Shapes and secondary forms** | Smooth lathes and ellipsoids read as plastic primitives | Big, medium and small forms; at phone size, drop detail under ~1% of frame height. Beard: 5–8 locks, tapered, one dominant lock off-centre. Robe: 3–5 folds fading up, hem with 4–6 scallops. Hat: 2–3 dents at the bend, tip leaning 5–10°, a slightly drooping brim, a thicker band. Sleeves: a cuff lip. Boots: a flared top and a wide toe. Seeded noise along normals (1–3% low frequency). Break symmetry 5–10%. Vary thickness ~20%. Bevels 2–4% on props |
| 5 | **Surface and baked light** | Flat and clean; contact areas don't darken | Ambient occlusion baked into vertex colours (BVH ray-cast, ~24–32 rays, radius 0.1–0.2 m), multiplied in with a purple tint. Toon gradient tinted: shadow band purple (0.48, 0.42, 0.62), lit band warm. Hard-edged toon specular on the nose, buckle, boots and gifts. One grade: saturation ~1.08, slight contrast; vignette. Bloom only on emissive parts (skipped: cost on software WebGL) |
| 6 | **Set dressing and camera** | Bare room, a single continuous move | Three tiers of props, one hero (the printer) with space around it, foreground elements for depth. Christmas plus summer cues (mate and thermos, a paper fan, mandarins, a faded wreath). Stage in depth: characters separated in z, faces in the upper half. About 4 shots cut on action (wide entrance, two-shot, printer and sack insert, wide hero). Hot light: warm low sun, cooler sky, dappled patches on the floor, warmth lifted into the shadows. Pans under 10°/s |

## Applied

See the end of this file once the changes are in (El Mago v2, Papá Noel, props, the 15 s reel).
