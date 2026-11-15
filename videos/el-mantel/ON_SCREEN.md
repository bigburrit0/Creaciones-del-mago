# "El mantel": everything on screen, by category

W4 of the November second wave (`../PLAN_NOVIEMBRE_2.md`), audited in `AUDIT.md`.

## 1. Story beats (24.5 s)

| Time | Beat | Line |
|---|---|---|
| 0.0-2.25 | Christmas Eve in his living room at sunset: his red vikings against bronze, set out on a red-and-white checked tablecloth; Papá Noel proud, arms open; hook "Tablero / de ajedrez / impreso en 3D, por partes" | S: "¡Ya tengo mi ajedrez!" |
| 2.25-3.72 | El Mago, deadpan, looking down at the cloth | M: "Eso es un mantel." |
| 3.72-4.45 | close and low: his pawns wobble on the cloth's fold; one tips over toward the empty middle (a soft "toc") | — |
| 4.45-5.95 | Papá Noel shrugs, head tilted | S: "¿Y qué tiene?" |
| 5.95-6.6 | El Mago raises his hand: the pieces leave in a sparkle (a pop), and the fold smooths out | — |
| 6.6-9.65 | from above: four quadrants fly in and fit together, then the four sides of the frame | M: "Un tablero reglamentario, que se arma por partes…" |
| 9.65-12.6 | the pieces land on the board rank by rank, his red vikings first | "…Para las piezas que ya tenés." |
| 12.6-15.25 | El Mago; the calendar page drops in: DICIEMBRE 23, "último día para pedir", the 23 circled | M: "Pedidos hasta el 23 de diciembre." |
| 15.25-17.4 | "Así es de verdad": the real photo, "Tamaño reglamentario. Se arma por partes y no trae piezas" | — |
| 17.4-22.0 | El Mago points at the viewer | M: "¿Ya tenés las piezas? Comentá TABLERO y te paso precio y fecha." |
| 22.0-24.5 | card over the board | — |

## 2. Product and props

| Item | Detail | Check |
|---|---|---|
| The puzzle board | from `tablero.webp`: black and white squares on a dark base, a grey frame with rounded corners. The reel shows four quadrants of 4 × 4 and the four sides of the frame (5 cm squares, 46 cm across; `biblioteca/3d/web/tablero3d.js`). h1 is a light square | the assembly frames |
| The tablecloth | red-and-white gingham, 4.4 cm checks (ten across the board's width), hanging over the table's edges; a soft fold under his pawns that smooths out at El Mago's snap | the opening frames, the pawn's fall |
| The pieces | the shop's viking set: his red against bronze; on the cloth they keep a board's 8 × 8 spacing, so they sit across the checks' lines | — |
| The feast | at the back of the table: pan dulce on a plate, a bottle of cider (no label), two red candles with flames, a small pine centrepiece | QA "feast" box |
| The room | Papá Noel's holiday living room ("Los gatos tiran todo"), with a garland of red and gold baubles, the tree, the sofa, a sunset over the rambla in the window | QA: sofa, lamp, walls, door |

## 3. Characters and acting

| Item | Detail | Check |
|---|---|---|
| Papá Noel | proud, arms open; shrugs with a head tilt; watches the board fit together | hands vs faces; beard gate; hands vs the table |
| El Mago | heavy lids at the cloth; raises his magic hand for the board; points at the viewer for the CTA (a 0.55 s reach) | jumps 0 |

## 4. Camera and editing

- Cuts every 0.65-3 s.
- The pawn's fall is shot low across the empty middle of the board, toward the falling pawn.
- The assembly is shot straight down.
- The landing pieces are a raised three-quarter view from the front.
- Every other camera looks toward a wall.

## 5. Text

- Hook "Tablero / de ajedrez / impreso en 3D, por partes".
- Kinetic captions.
- The calendar page "DICIEMBRE / 23 / último día para pedir".
- "Así es de verdad".
- The card:
  - "¿Ya tenés las piezas?";
  - "Tablero de ajedrez impreso en 3D, reglamentario, se arma por partes";
  - "¡Comentá TABLERO!";
  - "Te paso precio y fecha por mensaje / Pedidos para Navidad: hasta el 23 de diciembre";
  - the brand.

## 6. Sound

- The soft ambient bed (C ionian, page volume 0.22).
- The pawn's "toc", the snap's pop, the calendar's whoosh, the proof's tap, the chime on the card.
- No effect starts inside a spoken line (`cues.py` checks it).
