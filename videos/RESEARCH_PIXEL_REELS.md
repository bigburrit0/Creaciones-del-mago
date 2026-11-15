# How to make premium pixel-art reels: research synthesis and plan

Ten research agents, each with a different point of view and set of sources:
1. pixel animator (Saint11, Slynyrd)
2. game programmer (pixel-perfect movement)
3. prop and environment artist
4. short-form creator
5. AI-pipeline researcher
6. 3D-to-pixel technical artist
7. game-feel / juice designer
8. lighting artist
9. harsh critic
10. creative coder (GSAP/canvas)

Several hosts (lospec, slynyrd, threejs.org, ai.google.dev, pixellab) were blocked by the session's network. Those claims come from search snippets, and the agents marked their own inferences as such.

## Why the reel looked choppy (diagnosis, measured)

| Cause | Measured in `avance-2` | Agreed by |
|---|---|---|
| **Stepped positions**: characters jumped ~6 art px (24 screen px) about 8 times per second | Papá Noel's entrance: 9 jumps in 1.1 s | R1, R2, R9, R10 |
| **Uneven frame holds**: 8 fps sprites in a 30 fps video hold frames 4-3-4-3 video frames (judder) | every loop | R1, R9 |
| **Too few drawings** per action (4–6) and no in-betweens | Gemini sheets | R1, R5, R9 |
| **Frame drift** between drawings (size, baseline) | up to 7 px in the Mago walk (fixed) | R9, R5 |
| **Flat props**: no contact shadows, no shared light, front-facing drawings in a 3/4 room | printer, stool, sack | R3, R8, R9 |

## What all sources agree on

1. **Frames step, positions glide.** Sprite drawings change at 8–12 fps (that is the pixel-art look), but the sprite's *position* updates every video frame, snapped to the art-pixel grid. Never move a character "at animation rate".
2. **Sprite fps must divide the video fps**: 10, 12, 15 or 20 at 60 fps; 6, 10 or 15 at 30 fps.
3. **Render at 60 fps.** Slow 1-px moves read as steps at 30 fps. Instagram may serve 30 fps; it still looks smoother because each step is even.
4. **One pixel grid, integer scale, nearest-neighbour, one palette.** No blur, no CSS gradients, no bloom. Light and shadow are drawn with ordered dithering in palette colours.
5. **Depth comes from light, not from more detail.** Contact shadows / ambient occlusion where things touch the floor, one light direction, a window light shaft with dust, a vignette, and props drawn in the room's 3/4 perspective (top face visible).
6. **Ambient life everywhere, quietly.** Blinking lights, breathing idles, dust, a fan. Premium loops have many small cycles running at different speeds.
7. **Juice on every event**: anticipation before a throw (~110 ms), a parabolic arc (500–600 ms), a squash on landing, hit-stop of 50–90 ms on big moments, 2–4 px screen shake, and particle bursts with gravity and fade.
8. **More drawings for the actions that matter.** 8 for walks, 6–8 for jumps and throws, generated key-pose first and then in-betweens by editing the previous frame. AI frame interpolation blurs pixel art: avoid it.

## Applied now: `avance-3.mp4` (60 fps)

- **New motion engine** (`skills/pixel-reel/assets/pixel-reel.js`, smooth mode): positions interpolated per video frame and snapped to the art grid, eased starts and stops, real parabolas for arcs and hops, elastic pops, and sprite fps rounded to divisors of 60. Measured: Papá Noel now moves 0–2 art px per frame (was 6 px jumps 8 times per second).
- **Depth overlays** (`skills/pixel-reel/scripts/draw_light.py`): window light shaft and floor pool (dithered, screen blend, under the characters), contact shadows under the bench printer, stool, tree and fan, a vignette, and floor shadows that follow the characters and stay on the ground when they jump.
- **Dust motes** drifting in the light.

## Next, in order of impact

| # | Change | Who | Effort |
|---|---|---|---|
| 1 | **Juice pass on the gift sequence**: anticipation before each toss, printer flash + 50 ms hit-stop, sparkle burst with gravity, 2–3 px shake on the TNT, sack bounce, confetti with physics | Claude (code) | low |
| 2 | **Ambient life**: colour-cycled garland and tree lights, steam from the mate, blinking eyes on long holds, fan light flicker | Claude | low |
| 3 | **Props redrawn in 3/4 perspective** with top faces and selective outlines: printer (also with a visible moving print head), stool, sack. Prompts with the phrases below | Gemini + Claude QC | medium |
| 4 | **8-frame walks** for the Mago and Papá Noel, generated key-pose first and then in-betweens by editing the previous frame in the same chat | Gemini | medium |
| 5 | Optional: try a dedicated animation tool (PixelLab, Ludo keyframes, Retro Diffusion) for walks and big actions; they keep the character consistent across 8+ frames | you (account/cost) + Claude | medium |
| 6 | Optional, only if we want camera moves or many angles of the same room: low-poly 3D room rendered as pixel art (three.js, 270x480 target, palette quantization, edge outlines) | Claude | high |

Prompt phrases for props with volume (from R3):

```
three-quarter top-down view, camera about 45 degrees above, orthographic, no perspective distortion,
showing the top surface and the front face; light from the upper-left, lit top and left faces,
core shadow on the right-front, thin rim highlight on the top edge; no cast shadow, no floor
```

## How we work together

- **You**: art direction and taste. Generate the drawings (Gemini on your plan, or an animation tool if you choose one), pick variants, and judge each avance on the phone.
- **Claude**: everything that is code or measurement. Motion, light, particles, audio, QC of every sheet, fixes, assembly, renders, and before/after measurements of choppiness.
- **Loop**: every round ends with a rendered `avance-N.mp4` that you watch on your phone. Comments go back as concrete notes ("the toss feels slow", "the printer looks flat").

What the good "made with Claude" reels have in common (R5): drawn at the true low resolution, one palette, upscaled with nearest-neighbour, rendered frame by frame from code, and iterated several times as video. Our hybrid (AI-drawn characters plus code-driven motion and light) follows the same rules. The difference is in polish passes, not in tools.
