# "Las preguntas de Papá Noel": everything on screen, by category

Chess reel 4 (`../PLAN_AJEDREZ.md`), audited in `AUDIT.md`. The rules come from `../RESEARCH_AJEDREZ_2_2026.md`:
- the product is named in frame 1;
- numbers are visible (the counter);
- magic reads as magic;
- the work is shown honestly;
- the CTA asks only about what was shown and rewards the comment.

## 1. Story beats (27.2 s; the measured lines are in `AUDIT.md`)

| Time | Beat | Line |
|---|---|---|
| 0.0-1.35 | the set on its table, Papá Noel behind it reading his list; hook "Ajedrez vikingo / impreso en 3D"; counter "Pregunta 1/4" | S: "¿Cuánto sale?" |
| 1.35-3.75 | El Mago, from below his brim; stickers "precio ✔" and "fecha ✔" pop on those words | M: "Te paso precio y fecha antes de empezar." |
| 3.75-5.25 | 2/4. Papá Noel reads the list (its handwriting readable: "1. ¿Cuánto sale? 2. ¿Jugar o mirar?…") | S: "¿Es para jugar o para mirar?" |
| 5.25-6.85 | El Mago's hand up; the bronze king hops from e1 to the empty centre (a move: "para jugar") | M: "Para jugar." |
| 6.85-8.65 | across the empty board: a ruler rises beside the king, a red mark and "9,5 cm" at its crown; on "o más grande" the king grows (the camera pulls back) | M: "Tamaño torneo, o más grande." |
| 8.65-10.6 | 3/4. From the front: the h2 pawn hops off the board, falls to the floor, bounces, tips over and rolls away out of the shot | S: "¿Y si se me pierde una?" |
| 10.6-11.93 | the printer bed: a new bronze pawn rises layer by layer under the glow cap | M: "Te la imprimo de nuevo." |
| 11.93-12.4 | it pops onto h2 with sparkles | — |
| 12.4-13.3 | 4/4. Papá Noel leans in | S: "¿Y el tablero?" |
| 13.3-15.4 | El Mago's hand up: every piece floats up, the board slides out toward the camera, turns and stands on the floor in front of the table; the pieces settle on the bare table; tags "el tablero: aparte", "las piezas" | M: "Va aparte: yo hago las piezas." |
| 15.4-17.7 | the list drops, unrolls to the floor and rolls toward the camera (the numbered questions go on and on); the counter spins 5/4 → 5/87 and turns red | S: "¡Esperá, que tengo más!" |
| 17.7-19.6 | El Mago, deadpan, a slow blink | M: "Las demás… en comentarios." |
| 19.6-21.85 | "Así son de verdad": vikingo, medieval, medieval in colours (the set is reset underneath) | — |
| 21.85-24.8 | El Mago points at the viewer | M: "Comentá DUDA y te contesto, con precio y fecha." |
| 24.8-27.2 | card over the set, back on its board | — |

## 2. Product and props

| Item | Detail | Check |
|---|---|---|
| The viking set (32 pieces) | `ajedrez3d.js`, modelled from `assets/p/vikingos.webp`; bronze (El Mago's end) and silver (Papá Noel's end) | hook, board and card frames |
| The king at true size | both kings scaled so their toon meshes measure exactly 0.095 m; the ruler is a true 16 cm (32 px per cm on the texture), its foot on the board | the red mark sits at the crown in the 7.5 s frame |
| "O más grande" | the king grows ×1.7 (about 16 cm; the real limit is 25 cm, said in the caption) | 8.4 s frame: the whole king in shot |
| The lost pawn | h2 (El Mago's side, so it falls away from the list): a hop clears the table's front edge (the base is above the top at the edge), a gravity fall, two bounces, tips onto its side, rolls along the floor out of the shot; hidden once out of shot | QA "pawn-table"; frames 9.1-10.2 |
| The reprint | the una-mas print: a bronze pawn revealed bottom-up by a rising cut plane with a small glow cap; the head and bed move; no failed print | 11.2 s frame |
| The board apart | slides 0.58 m out over the table (the whole board clears the front edge before it turns), turns up and stands on its edge on the floor, leaning back 3°; the pieces float 6 cm while it moves, then land a board's thickness lower, on the bare table | QA "board" (vs both bodies), "board-table"; frames 13.9-15.2 |
| The list | a parchment strip between two rollers (red knobs), held by its top roller in his left hand, out to his left. Handwritten in Caveat: "Preguntas", the four questions, then "5. ¿…?" scribbles to 87. At the drop the bottom roller falls with gravity, bends at the floor and rolls away (decelerating, 1.15 m) | QA "list" (vs both bodies, his holding arm excepted) and "list-furniture"; frames 15.9-17.4 |
| The tree | moved behind Papá Noel, by the side wall (it stood in the list's path) | payoff frames |

## 3. Characters and acting

| Item | Detail | Check |
|---|---|---|
| Papá Noel | holds the list all through; glances down at it before each question, then asks; leans in, eager; watches the list unroll, then turns to the camera with his right hand up ("¡Esperá!"); brows up at each question | hands vs own face and the other character 0; beard gate 0 |
| El Mago | calm, faces his friend; left hand raised for the magic (the hop and ruler, the board); eyes on the board while it works; deadpan for "Las demás…" (brows down, a slow blink); points at the viewer for the CTA (a 0.55 s reach) | jumps 0 |

## 4. Camera and editing

- A cut every 0.5-2.5 s; whip pans into the 2/4, 3/4, 4/4 and CTA shots.
- The ruler shot looks across the empty middle of the board (no packed rank in the line of sight) and pulls back as the king grows.
- The pawn shot is a front view of the table and the floor, so the fall and the roll cross the frame.
- The payoff is a high front view: the list runs down and along the floor toward the lens, with Papá Noel above it, under the counter.
- El Mago's close-ups from below his brim (el -9°).
- Snap zooms on the "9,5 cm" mark, on "¡Esperá!" and on "en comentarios"; a small shake when the roller hits the floor.

## 5. Text

- Hook "Ajedrez vikingo / impreso en 3D" (0-1.4 s).
- The counter "PREGUNTA 1/4 … 4/4", then 5/9, 5/17, 5/31, 5/52, 5/87, in red.
- Stickers "precio ✔", "fecha ✔" (no number).
- The "9,5 cm" label on the ruler.
- The tags "el tablero: aparte", "las piezas".
- Kinetic captions.
- "Así son de verdad".
- The card:
  - "¿Otra duda?";
  - "Ajedrez vikingo y medieval, impreso en 3D pieza por pieza";
  - "¡Comentá DUDA!";
  - "Te contesto, con precio y fecha / Son las piezas; el tablero va aparte";
  - the brand.

No phone number, no price, no date, no emoji.

## 6. Sound

- The viking tune (E Aeolian, 120 bpm, a lur call), ducked under every line.
- A rustle of the list and a bell tick for each new question.
- Pops on the stickers.
- The hop: a heave and a clack.
- The ruler: a sparkle and a ding.
- The growth: a low pop.
- The lost pawn: a clack off the board, two bounces, a short sad tune.
- The printer whir only under its close-up; a pop, a clack and a ding for the reprint.
- The board: a whoosh out, a thud when it stands, two clacks as the pieces land.
- The list: a rustle, a thud of the roller, a rolling rustle, the counter's rising ticks, a surprise.
- No ambience.

Check: about -14 LUFS, no steady buzz, every line clear.
