# "Culpa de las piezas": everything on screen, by category

Chess reel 5, the last of the series (`../PLAN_AJEDREZ.md`), audited in `AUDIT.md`. The rules come from
`../RESEARCH_AJEDREZ_2_2026.md`:
- the product is named in frame 1;
- magic reads as magic;
- the work is shown honestly;
- the CTA asks only about what was shown and rewards the comment;
- honest urgency only: the owner's real cut-off (23 December, the last day to order, not a delivery promise).

## 1. Story beats (24.2 s; the measured lines are in `AUDIT.md`)

| Time | Beat | Line |
|---|---|---|
| 0.0-1.0 | the rematch, mid-game (the scholar's mate); the viking king wobbles and tips over onto the empty e7 square; hook "Ajedrez vikingo vs. medieval / impreso en 3D", badge "LA REVANCHA" | — |
| 1.0-2.6 | Papá Noel points at the board, outraged | S: "¡Me hicieron trampa las piezas!" |
| 2.6-3.95 | his POV: his own vikings turn round one by one and tilt back to look up at him | — |
| 3.95-4.45 | Papá Noel sweats, glasses down | — |
| 4.45-7.3 | El Mago, deadpan, a slow blink after "Vos sí" (snap zoom) | M: "Las piezas no pierden. Vos sí." |
| 7.3-9.8 | Papá Noel sulks, turned away… then both arms up | S: "Mmm… quiero el mío. ¡Para Navidad!" |
| 9.8-11.55 | the printer: a red viking king rises layer by layer under the glow cap | M: "Entonces no esperes:" |
| 11.55-13.45 | El Mago, the printer at work behind him | M: "…un juego lleva muchas horas de impresora." |
| 13.45-14.65 | Papá Noel leans in | S: "¿Hasta cuándo lo puedo pedir?" |
| 14.65-16.75 | El Mago to the viewer; a calendar page drops in: DICIEMBRE 23, "último día para pedir"; the 23 is circled in red on "veintitrés" | M: "Hasta el 23 de diciembre." |
| 16.75-19.0 | "Así son de verdad": vikingo, medieval, medieval in colours (the board is reset underneath) | — |
| 19.0-21.7 | El Mago points at the viewer | M: "Comentá PEDIR y te paso precio y fecha." |
| 21.7-24.2 | card over the board, the king standing again | — |

## 2. Product and props

| Item | Detail | Check |
|---|---|---|
| The two sets | `ajedrez3d.js`, modelled from the site's photos: medieval in red (El Mago), viking in bronze (Papá Noel), as in reel 1; both kings at 9.5 cm | hook and card frames |
| The position | the scholar's mate: 1.e4 e5 2.Bc4 Nc6 3.Qh5 Nf6?? 4.Qxf7# (a real mate players will recognise; the f7 pawn is gone) | the 0.05 s frame |
| The king's fall | a wobble, then a fall forward onto the empty e7 square, pivoting on the base edge | QA "king-into-board" and "king-on-piece"; frames 0.45-0.8 |
| The stare | 13 vikings (all but the fallen king) turn half round in a wave (0.055 s apart, 0.42 s each, a tiny lift), then tilt back 0.28 rad to look up at him; none leaves its square | frames 2.65-3.9 |
| The print | a red viking king (his colours, a callback to reel 3), scaled to 9.5 cm, revealed bottom-up by a rising cut plane, the head and bed moving; a ding and sparkles when done; no failed print | 10.8 s frame |
| The calendar | a DOM page (not a prop): red header "DICIEMBRE", a big "23", "último día para pedir" in Caveat; a red ring drawn around the 23 | 15.3 and 15.9 s frames; clear of the top area and of El Mago's face |

## 3. Characters and acting

| Item | Detail | Check |
|---|---|---|
| Papá Noel | watches the mate (a downward look taken from the upper spine and head); points with his left hand (camera side, a 0.55 s reach); sweats and his glasses slide down under the stare; sulks (upper spine turned away, brows down), then both arms up for "¡Para Navidad!"; leans in to ask | hands vs own face and the other character 0; beard gate 0 |
| El Mago | watches the board; deadpan with brows down and a slow blink; turns to the viewer for the date and the CTA; points (a 0.55 s reach) | jumps 0 |

## 4. Camera and editing

- A cut every 0.5-2.8 s; whip pans into the sulk, the print, the date and the CTA.
- The fall is shot from the side away from the attacking queen, raised above the pawns.
- The stare is his POV, from just in front of his beard, looking down at his own pieces.
- El Mago's close-ups from below his brim (el -9°). The date shot puts him on the left, the calendar on the right.
- Snap zooms on the fall, "Vos sí", "¡Para Navidad!" and the ring.

## 5. Text

- Badge "LA REVANCHA".
- Hook "Ajedrez vikingo / vs. medieval / impreso en 3D" (0-1.0 s).
- Kinetic captions.
- The calendar page.
- "Así son de verdad".
- The card:
  - "¿Lo querés para Navidad?";
  - "Ajedrez vikingo y medieval, impreso en 3D pieza por pieza";
  - "¡Comentá PEDIR!";
  - "Pedidos hasta el 23 de diciembre / Te paso precio y fecha por mensaje";
  - the brand.

No phone number, no price, no delivery promise, no emoji. The only date is the owner's cut-off.

## 6. Sound

- The viking tune (E Aeolian, 120 bpm), ducked under every line and under the stare.
- The fall: a bell, two wobble taps, a thud, a sad little tune.
- The stare: a soft scrape per viking, then a surprise and a sting.
- A pop on "Vos sí"; an item-get jingle on "¡Para Navidad!".
- The printer whir only under its close-up, a ding when the king is done.
- The calendar: a whoosh, a tap, a chime when the 23 is circled.
- No ambience.

Check: about -14 LUFS, no steady buzz, every line clear (the date heard as "veintitrés de diciembre").
