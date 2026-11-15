# "El laberinto": everything on screen, by category

W3 of the November second wave (`../PLAN_NOVIEMBRE_2.md`), audited in `AUDIT.md`.

## 1. Story beats (23.0 s)

| Time | Beat | Line |
|---|---|---|
| 0.0-1.55 | straight down over a corner: white stone walls with a passage between them, a labyrinth; the camera rises and it is a chess board inside its walls, with a temple; hook "Ajedrez de la / antigua Grecia / impreso en 3D" | M: "Minotauro contra Hércules." |
| 1.55-2.7 | low, from the middle of the board: the Minotaur king lowers its horns and leans in | (the line goes on) |
| 2.7-3.7 | Hercules raises his club over his head (a thud, a whoosh) | — |
| 3.7-4.65 | Papá Noel leans over the walls at his end, his mitten reaching | — |
| 4.65-6.8 | from above: his mitten follows the passage to the corner (a dead end), turns back, runs to another dead end, comes back again | S: "¿Y por dónde se sale?" |
| 6.8-9.55 | El Mago, deadpan, heavy-lidded | M: "Es un ajedrez. Se sale ganando." |
| 9.55-13.05 | the whole board from the front: El Mago's magic hand; two tape measures pop in; one runs 52 cm along the front, the other 50 cm along Papá Noel's end; the tag "52 cm", then "52 × 50 cm / con su tablero" | M: "Y este trae su tablero: 52 por 50." |
| 13.05-14.95 | Papá Noel, both hands open, brows up | S: "¡Qué tablero!" |
| 14.95-17.15 | "Así es de verdad": the real photo, "Con su tablero de 52 × 50 cm, muros y templo incluidos" | — |
| 17.15-20.3 | El Mago points at the viewer | M: "Comentá MINOTAURO y te paso precio y fecha." |
| 20.3-23.0 | card over the board | — |

## 2. Product and props

| Item | Detail | Check |
|---|---|---|
| The board | from `grecia.webp`: red and gold squares (5 cm) with fine gold lines, inside a ring of white, rocky ruin walls: an inner and an outer row of hewn blocks with a narrow passage between them, cross blocks closing the passage here and there, taller blocks at the corners. 52 × 50 cm with the walls (`biblioteca/3d/web/grecia3d.js`) | the opening frames; the tapes' frame |
| The temple | in the middle of the far long side: two steps, six columns in front and six behind, an entablature, a pediment | the wide frames |
| The gold army | the Minotaur king on a column drum (bull's head, horns, a ring in its nose), columns with a brazier (rooks), winged horses (knights), laurel-crowned sages with a scroll (bishops), a goddess with a diadem and a torch (queen), crested hoplites with a round shield and a spear (pawns) | the face-off frames |
| The red army | the same pieces, with Hercules for king: a lion's head as a hood, its paws knotted on his chest, a club | the face-off frames |
| The tape measures | yellow, real centimetres (a tick every cm, numbers every 10); cases pop in by magic with sparkles, never held | the tapes' frame |
| The courtyard | terracotta tiles, whitewashed walls on three sides, a blue door, a window with open blue shutters and the sea in it, bougainvillea, an olive tree and a lemon tree in pots, an amphora, string lights; a wooden table with white legs | QA furniture (table top, legs) |

## 3. Characters and acting

| Item | Detail | Check |
|---|---|---|
| Papá Noel | leans in (upper spine), follows the passage with his left mitten above the blocks (the mitten never enters a block or a piece); both hands open, brows up for "¡Qué tablero!" | QA: walls and temple vs every collider; pieces vs both bodies; hands vs faces; beard gate |
| El Mago | heavy lids for the deadpan line; raises his hand for the tapes; points at the viewer for the CTA (a 0.55 s reach) | jumps 0 |
| The kings | the Minotaur lowers its horns (the head pivots at the neck); Hercules raises his club (the arm pivots at the shoulder) | QA: the club's head vs both bodies |

## 4. Camera and editing

- The opening looks straight down and rises.
- The face-off is shot from the empty middle of the board, a little above the pawns, so each king shows over its own pieces.
- His mitten in the labyrinth is seen from above, his arm coming in from the right.
- The tapes are a frontal push-in over the whole board.
- Every other camera looks toward a wall of the courtyard.
- Snap zooms on the raised club and "¡Qué tablero!".

## 5. Text

- Hook "Ajedrez de la / antigua Grecia / impreso en 3D".
- The size tag: "52 cm", then "52 × 50 cm / con su tablero".
- Kinetic captions.
- "Así es de verdad".
- The card:
  - "Minotauro contra Hércules";
  - "Ajedrez de la antigua Grecia, impreso en 3D, con su tablero";
  - "¡Comentá MINOTAURO!";
  - "Te paso precio y fecha por mensaje / Pedidos para Navidad: hasta el 23 de diciembre";
  - the brand.

## 6. Sound

- The soft ambient bed (D dorian with a root drone, page volume 0.22).
- The Minotaur in silence (under the first line).
- A thud and a whoosh for the club.
- A tap at the dead end.
- A pop for the tapes, a click as the second one locks.
- No effect starts inside a spoken line (`cues.py` checks it).
