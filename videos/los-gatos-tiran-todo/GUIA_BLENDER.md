# "Los gatos tiran todo": animation and timing guide for Blender

Paste everything below the line into the agent that edits the reel in Blender.

---

You are editing the Instagram reel **"Los gatos tiran todo"** (Creaciones del Mago, a 3D-printing shop in Montevideo) in
Blender. The file is `escenas/los-gatos-tiran-todo.blend`. Your job is to make the picture match the timing below,
**to the frame**. The voices, music and effects are already in the Video Sequencer and are correct: **do not move,
trim or re-time any sound strip.** The picture must fit the sound, never the other way round.

## 1. Golden rules (the timing broke because of these)

1. **30 fps, frame 1 = 0.00 s.** Convert any time with `frame = round(t × 30) + 1` (half rounds up). The reel lasts
   **23.0 s = frames 1-691**. Do not change the frame rate, the start frame or the scene length; do not use time
   stretching or the "Time Remapping" old/new settings.
2. **The sound strips are the master clock.** Each voice strip starts exactly at the time in section 3. If a strip
   does not start there, put it back, then fix the picture.
3. **The muted strip "video final (referencia)"** is the finished reel. Unmute it (or view it in a Sequencer
   preview) and scrub against it: every cut, hop, tap and fall must land on the same frame as in the reference.
4. **Hard cuts must be hard.** The camera was imported with LINEAR keys, so every cut slides across one frame (for
   example frames 282-283). Select all the camera's keys and set interpolation to **Constant** (or at least make
   the two keys on each side of a cut Constant). A cut happens between two frames: the new shot owns the first frame
   at or after the cut time.
5. **Keep the baked animation unless a beat is wrong.** The characters, pieces and camera already carry the reel's
   animation, sampled at 30 fps. If you re-animate something, keep its keys on the frames listed here; do not
   offset whole actions or NLA strips.
6. **The text is not in the .blend.** The hook, word-by-word subtitles, the real-photo gallery and the end card
   were page overlays (section 6). Leave room for them; do not burn other text in.
7. **Render 1080 × 1920, 30 fps, frames 1-691,** with the sound strips mixed in (FFmpeg, H.264 + AAC). Finish by
   checking section 7.

## 2. The scene

- **Set:** Papá Noel's holiday living room in Montevideo (sage striped wallpaper, window to the sea and the rambla,
  sofa, floor lamp, Christmas tree with blinking bulbs, rug). A small game table with a chessboard in the middle.
- **The set:** dogs vs. cats chess. The **dogs** (brown) are Papá Noel's, on his side; the **cats** (cream) are
  El Mago's. Key pieces: the **dog pug pawn** on the h-file (h7) and the **cat queen** (tiara, d1).
- **Papá Noel** stands at the dogs' end; **El Mago** at the cats' end, facing each other across the table.
- **Tone:** a deadpan cat joke. Clear poses, quick cuts (every 0.4-2.4 s), small snap zooms on the punchlines.

## 3. Voices (fixed; Spanish)

| Start s | Frame | End s | Who | Line |
|---|---|---|---|---|
| 0.15 | 6 | 2.38 | Papá Noel | ¡Yo juego con los perros! |
| 2.50 | 76 | 4.08 | El Mago | Los gatos, conmigo. |
| 9.75 | 294 | 11.67 | Papá Noel | ¡Eso no es una jugada! |
| 11.85 | 357 | 12.61 | El Mago | Para un gato, sí. |
| 17.10 | 514 | 20.63 | El Mago | ¿Perro o gato? Comentá cuál y te paso precio y fecha. |

The speaking character's mouth moves only inside his own line, and stops by its end.

## 4. Shot list (the cuts)

| # | Start s | Frame | End s | Shot | What happens |
|---|---|---|---|---|---|
| 1 | 0.00 | 1 | 1.10 | Wide, high, over the board, living room behind (lens ~46° vertical FOV) | Hook: both armies face to face. Papá Noel's line starts (off screen). |
| 2 | 1.10 | 34 | 2.45 | Medium on Papá Noel, slightly low, 35° to his right | He puts a hand on his chest, brows up: "¡Yo juego con los perros!" |
| 3 | 2.45 | 75 | 4.15 | Medium on El Mago, from 48° to his side, slightly high | Hand on his chest, brows up: "Los gatos, conmigo." |
| 4 | 4.15 | 126 | 6.00 | Low over the cats' side, looking at the dogs' faces (whip-pan in) | The pug pawn hops h7 → h5 (4.35-4.80), tail wagging hard. |
| 5 | 6.00 | 181 | 7.10 | From the dogs' side, looking back across the board (whip-pan in) | The cat queen leaps d1 → g4 (6.05-6.60), steps to g5 (6.75-7.05), next to the pawn. |
| 6 | 7.10 | 214 | 9.37 | Side view at table height, from the front-left | She looks up at the pawn (7.10-7.40), then three slow taps; the third sends it over the edge. Snap zoom +6 % on the third tap (8.95). |
| 7 | 9.37 | 282 | 9.75 | Looking straight down at the rug in front of the table | The pug falls and lands on the rug, on its side (≈9.66, frame 291). Tiny camera shake, sparkles. |
| 8 | 9.75 | 294 | 11.75 | Medium on Papá Noel (as shot 2) | Outraged: points at the board with his left hand, leans back. Snap zoom +8 % at 9.80. |
| 9 | 11.75 | 354 | 13.15 | Close-up on El Mago, low | Deadpan: "Para un gato, sí." Snap zoom +10 % at 11.90; then a slow blink (12.70-13.20). |
| 10 | 13.15 | 396 | 14.80 | Over the dogs, toward the cats | Every cat looks up at Papá Noel, smug (13.15-13.50); the dog king's ears droop. |
| 11 | 14.80 | 445 | 17.00 | Close-up on El Mago (as shot 9) | Hidden under the real-photo gallery (section 6). The board is reset to the start position here. |
| 12 | 17.00 | 511 | 20.55 | Medium on El Mago, he faces the lens (whip-pan in) | He turns to the viewer (16.80-17.10) and points at us (17.75-20.85): "¿Perro o gato? …" |
| 13 | 20.55 | 618 | 23.00 | Wide, from the front, the whole set at the start position | End card over the set. Hold to the end. |

## 5. Acting, beat by beat

### The pieces

- **The pug pawn (dog, h7):**
  - still until 4.35 (frame 132);
  - hops in one arc to h5, 0.45 s long (lands 4.80, frame 145), 5 cm high;
  - its tail wags hard from 3.95 to 8.05, then normally.
- **The cat queen:**
  - still on d1 until 6.05 (frame 183);
  - leaps in one 0.55 s arc, 9 cm high, to g4 (lands 6.60, frame 199);
  - a little 0.30 s hop to g5 (6.75-7.05);
  - looks up at the pawn: head turns 7.10-7.40 and holds until 14.80.
- **The three taps.** Each tap moves the pawn 1.65 cm toward the table's front edge. On taps 1 and 2 the queen follows it.

  | Tap | Paw out | Paw holds | Paw back | Pawn slides |
  |---|---|---|---|---|
  | 1 | 7.75-7.93 (frames 234-239) | to 8.07 | by 8.25 | 7.87-8.09 |
  | 2 | 8.35-8.53 (frames 252-257) | to 8.67 | by 8.85 | 8.47-8.69 |
  | 3 | 8.95-9.13 (frames 270-275) | to 9.27 | by 9.45 | 9.07-9.32, off the edge |

  The paw goes out sideways from the shoulder, toward the pawn.
- **The fall:**
  - the pawn tips and drops with gravity from 9.32 (frame 281);
  - it hits the rug at ≈9.66 (frame 291) and lies there on its side.
- **Smug cats:** all cats tilt their heads up toward Papá Noel, 13.15-13.50, and hold until 14.80.
- **The dog king:** his ears droop over the same span.
- **Reset:** from 14.80 every piece is back on its starting square (the end card shows the start position).
- **Tree bulbs:** they cycle colour 3 times a second all through.

### Papá Noel

| Time s | Action |
|---|---|
| 0.05-2.55 | Left hand to his chest (reach 0.55 s), brows up 0.15-1.45. |
| 5.95-9.85 | Watches the cat: head and upper back tilt down toward the board. |
| 8.95-11.85 | Brows up (from the third tap). |
| 9.32-11.65 | Glasses slide down his nose (from when the pawn drops). |
| 9.60-11.90 | Points at the board with his left hand (reach 0.55 s, fully out 9.95-11.35), leaning back, offended. |

### El Mago

| Time s | Action |
|---|---|
| 2.25-4.40 | Right hand to his chest; brows up 2.50-3.80. |
| 5.85-10.05 | Watches his cat (head turned toward the board). |
| 11.65-13.35 | Brows slightly down (deadpan). |
| 12.70-13.20 | One slow blink, eyes shut 12.83-13.03. |
| 16.80 to the end | Head turned to the lens. |
| 17.20-21.35 | Right arm points at the viewer: fully out 17.75-20.85, back down by 21.35. |

- **Blinks, both characters:** 1.40, 3.60, 6.40, 10.40, 15.90, 18.20 and 21.60 s, each 0.2 s.
- **Idle:** both breathe and sway gently the whole reel (an idle loop), never frozen.

## 6. Overlays (added after Blender; keep these areas readable)

- **Safe area:** keep faces and key action out of the top 220 px and the bottom 450 px.

| When s | Overlay |
|---|---|
| -0.2 to 1.10 (fades out from 0.90) | Hook at the top (y ≈ 300 px): "Ajedrez / perros vs. gatos / impreso en 3D" |
| with each voice line | Kinetic subtitles, word by word, in the lower middle |
| 14.80-17.00 | White flash at 14.80; the real-photo gallery "Así son de verdad" covers the frame. The photo changes at 15.55 and 16.275. |
| 20.55 to the end | The end card slides up over 0.3 s in the middle of the frame (y ≈ 960 px): "¿Perro o gato? / Ajedrez perros vs. gatos, impreso en 3D pieza por pieza / ¡Comentá tu bando! / …" |

## 7. Sound sync check (the effects are already in the mix)

Use these to check that the picture lands on the sounds.

| Time s | Frame | Sound | Must see |
|---|---|---|---|
| 4.06 | 123 | whoosh | the whip into shot 4 |
| 4.35 | 132 | boing (with a xylophone run just before) | the pawn's hop starts |
| 6.05 | 183 | whoosh | the queen's leap starts |
| 6.60 | 199 | toc | she lands on g4 |
| 7.05 | 213 | toc | she lands on g5 |
| 7.60-13.00 | 229-391 | the music stops dead | only the taps and the fall play |
| 7.89 / 8.49 / 9.09 | 238 / 256 / 274 | three taps | the paw touching the pawn, each time |
| 9.40 | 283 | metal-pipe clang (bounces, rings 1.8 s) | the fall, cut to the rug |
| 12.67 | 381 | deep boom | right after "sí", on El Mago's deadpan face |
| 13.00 | 391 | the music comes back, smug, with glockenspiel | shot 10 (13.15) right after |
| 15.17 | 456 | toc | gallery |
| 15.50 / 16.225 | 466 / 488 | soft swipes | the gallery photo changes |
| 16.91 | 508 | whoosh | the whip into the CTA (17.00) |
| 20.70 | 622 | chime, then a D-major chord | the end card |
| 22.2-23.0 | 667-691 | fade out | hold the wide shot |

Done when:
- every cut and beat above is on its frame;
- the reference strip and your render play in sync over the whole 23 s;
- no cut leaves an in-between frame;
- the render is 691 frames at 1080 × 1920.
