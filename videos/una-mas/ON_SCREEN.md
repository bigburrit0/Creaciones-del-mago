# "Una más": everything on screen, by category

Chess reel 2 (`../PLAN_AJEDREZ.md`), audited in `AUDIT.md`. The rules come from `../RESEARCH_AJEDREZ_2_2026.md`:
- the product is named in frame 1;
- the work is shown honestly;
- magic reads as magic;
- the CTA asks only about what was shown.

## 1. Story beats (27.2 s; measured lines: m1 2.54, s1 1.76, m2 0.56, s2 0.85, m3 0.55, s3 0.93, m4 2.67, m5 3.82)

| Time | Beat | Line |
|---|---|---|
| 0.0-2.65 | the viking king prints layer by layer (already 1/3 printed in frame 1); "Ajedrez vikingo impreso en 3D", counter 1/32 | M: "Treinta y dos piezas. ¡A imprimir!" |
| 2.65-5.05 | each finished piece sparkles from the bed onto its square (clack); the bronze side fills | — |
| 5.05-7.45 | Papá Noel, eager; El Mago, calm | S: "¿Ya está?" M: "Una más." |
| 7.45-9.75 | the bronze pawns; a wide shot: the moon rises in the window behind El Mago | — |
| 9.75-11.3 | Papá Noel, tired; El Mago, same shot, same calm | S: "¿Y ahora?" M: "Una más." |
| 11.3-13.75 | night: the printer keeps going under its light; Papá Noel dozes standing up (z z z, snores); the silver side fills | — |
| 13.75-14.25 | dawn: 32/32, a ding, sparkles, the full board in both colours | — |
| 14.25-15.3 | Papá Noel wakes with a start, arms up | S: "¡¿Ya está?!" |
| 15.3-18.15 | a 33rd pawn prints; El Mago, with a smile | M: "Y si se te pierde una… ¡una más!" |
| 18.15-20.5 | "Así son de verdad": vikingo, medieval, medieval in colours | — |
| 20.5-24.5 | El Mago points at the viewer | M: "¿Vikingo o medieval? Comentá cuál y te paso precio y fecha." |
| 24.5-27.2 | card over the full board | — |

## 2. Product and props

| Item | Detail | Check |
|---|---|---|
| The viking set (32 pieces) | `ajedrez3d.js`, modelled from `assets/p/vikingos.webp`: a king in furs with a sword, a shieldmaiden queen, the bear-hood seer, the dragon prow, the stave church, shield pawns. **Two colours, one per side** (bronze, silver): the per-side choice no competitor shows | frames at each phase; both colours readable at night |
| The print on the bed | a template of the right piece and colour, revealed bottom-up by a rising cut plane, with a small warm glow cap at the cut; the head and bed move; the nozzle glows. No failed prints, no stalling | hook frames 0.0 / 2.3; the night bed shot |
| The pops | each piece appears on its square with a scale pop and a few sparkles (magic, not a teleport glitch) | board frames |
| The 33rd pawn | prints on the bed after 32/32 and stays there (the spare): "si se te pierde una" | 15.9 |
| The board and table | as in reel 1 | QA furniture 0 |

## 3. Characters and acting

| Item | Detail | Check |
|---|---|---|
| El Mago | conducts the printing with a raised left hand (the magic); calm, eyes on the board; the same close-up for both "Una más" (the repetition is the joke); points at the viewer for the CTA | hands vs own face/beard 0 |
| Papá Noel | eager (leans in); tired; dozes standing up, the droop mostly from the upper spine (a deeper head bend pressed his chin into his beard: QA caught 42 frames); wakes with a start, arms up | beard gate 0; walls and table 0 |

## 4. Light: the hours, told honestly

- Day until 7.4 s, then a slow blend to night by 11.3 s: the moon in the window, a blue fill, the printer's light.
- Night until 13.75 s, then dawn in 0.6 s, then towards day.
- The printer's lit parts dim by 70% at night.

This is the "un juego completo lleva muchas horas de impresora" fact, shown instead of said.

## 5. Camera and editing

- A cut every 0.7-2 s while the work stays on screen.
- Three-quarter board shots that follow the side being filled (bronze from the left, silver from the right); a wide shot at 32/32.
- The printer bed in three-quarter view.
- Whip pans between phases.
- Snap zooms on "Una más", 32/32 and "¡¿Ya está?!".
- Every camera looks toward the walls; El Mago's close-ups from below his brim.

## 6. Text

- Hook "Ajedrez vikingo / impreso en 3D" from frame 1.
- The counter badge (yellow, turning green at 32/32).
- Kinetic captions.
- "Así son de verdad".
- The card:
  - "¿Vikingo o medieval?";
  - "Ajedreces impresos en 3D, pieza por pieza";
  - "¡Comentá cuál!";
  - "Elegís los colores de cada bando / Te paso precio y fecha por mensaje";
  - the brand.

No phone number, no price, no emoji.

## 7. Sound

- An E Aeolian tune at 120 bpm, opening on a lur call, ducked under every line and lower at night.
- A soft clack for every piece, rising slightly in pitch as the set fills.
- Printer whir only under the printer close-ups.
- Two snores; a ding, a chime and a "!" at 32/32; a ding for the spare.
- No ambience.

Check: about -14 LUFS, no steady buzz, every line clear.
