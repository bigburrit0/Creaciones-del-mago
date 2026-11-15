# "Los gatos tiran todo": everything on screen, by category

W1 of the November second wave (`../PLAN_NOVIEMBRE_2.md`), audited in `AUDIT.md`.

## 1. Story beats (23.0 s)

| Time | Beat | Line |
|---|---|---|
| 0.0-1.1 | the dogs-vs-cats set on the game table, both armies face to face; hook "Ajedrez perros vs. gatos / impreso en 3D" | S: "¡Yo juego con los perros!" |
| 1.1-2.45 | Papá Noel, a hand on his chest | (the line goes on) |
| 2.45-4.15 | El Mago, a hand on his chest | M: "Los gatos, conmigo." |
| 4.15-6.0 | the dogs face us; an eager pug pawn hops two squares forward, its tail wagging | — |
| 6.0-7.1 | the cat queen leaps across the board (cats jump) and steps next to the pawn | — |
| 7.1-9.37 | side view: she looks up at him and taps the pawn with her right paw, three slow taps; the third sends it over the edge | — |
| 9.37-9.75 | looking down: the pug lands on the rug, on its side | — |
| 9.75-11.75 | Papá Noel, outraged, points at the board | S: "¡Eso no es una jugada!" |
| 11.75-13.15 | El Mago, deadpan, a slow blink | M: "Para un gato, sí." |
| 13.15-14.8 | every cat looks up at him, smug; the dog king's ears droop | — |
| 14.8-17.0 | "Así son de verdad": the real photo (the dogs' side), "Los gatos de un lado, los perros del otro" | — |
| 17.0-20.55 | El Mago points at the viewer | M: "¿Perro o gato? Comentá cuál y te paso precio y fecha." |
| 20.55-23.0 | card over the set, back at the start | — |

## 2. Product and props

| Item | Detail | Check |
|---|---|---|
| The dogs | `biblioteca/3d/web/mascotas3d.js`, from the photo: seated pugs (pawns), hounds in capes with a medallion (bishops), a boxer with a cape and crown (king), a retriever with a small crown (queen); a terrier with a scarf (knight) and a big dog with a collar (rook), which the photo does not show. Brown | the hop and smug frames |
| The cats | the same style (the photo shows only the dogs): kittens, hooded cats, a crowned cat with a cape, a tiara for the queen, a cat with a scarf, a loaf cat with a collar. Cream | the hook and leap frames |
| Sizes | each piece scaled by its measured toon meshes: king 9.5 cm, queen 8.6, bishop 8, knight 7.2, rook 7, pawn 5.6 | — |
| The board | the chess kit's board, 5 cm nearer the table's front edge (0.8 cm left), so a pawn can go over it | — |
| The push | the queen's right foreleg pivots at the shoulder, out to her side; the pawn moves 1.65 cm per tap (she follows it); the third tap slides it over the edge; it tips and falls (gravity) onto the rug and lies there | QA "pawn-table" and "queen-pawn" |
| The living room | the workshop shell redressed: sage striped wallpaper, a window with the sea, the rambla's wall and gulls, a sofa with two cushions, a floor lamp, a framed picture, a plant, the tree; the rug under the game table | QA furniture (table, legs, sofa, lamp) |

## 3. Characters and acting

| Item | Detail | Check |
|---|---|---|
| Papá Noel | a hand on his chest; watches the cat (a downward look taken mostly from the upper spine); outraged, points at the board (left hand, a 0.55 s reach); leans back, offended; glasses down when the pawn lands | hands vs faces 0; beard gate 0 |
| El Mago | a hand on his chest; watches his cat; deadpan with a slow blink; points at the viewer for the CTA (a 0.55 s reach) | jumps 0 |

## 4. Camera and editing

- A cut every 0.4-2.4 s.
- The dogs' hop is shot from the cats' side, so we see their faces.
- The push is a side view from the front-left, clear of the cats' front file.
- A quick top-down insert of the pawn on the rug.
- Snap zooms on the third tap, on "¡Eso no es…!" and on "Para un gato, sí".

## 5. Text

- Hook "Ajedrez / perros vs. gatos / impreso en 3D".
- Kinetic captions.
- "Así son de verdad", with one large polaroid.
- The card:
  - "¿Perro o gato?";
  - "Ajedrez perros vs. gatos, impreso en 3D pieza por pieza";
  - "¡Comentá tu bando!";
  - "Te paso precio y fecha por mensaje / Pedidos para Navidad: hasta el 23 de diciembre";
  - the brand.

No phone number, no price, no delivery promise, no emoji.

## 6. Sound

- The soft ambient bed (C major, page volume 0.22): 25 dB under the voices, 14 dB under them in the gaps.
- A small pop for the hop.
- A whoosh and a tap for the leap.
- Three soft taps.
- A plop and a small thud on the rug.
- A sting for the smug cats.
- No effect starts inside a spoken line (`cues.py` checks it).

Check: about -14 LUFS, no steady buzz, every line clear.
