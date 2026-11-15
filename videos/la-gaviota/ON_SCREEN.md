# "La gaviota": everything on screen, by category

W2 of the November second wave (`../PLAN_NOVIEMBRE_2.md`), audited in `AUDIT.md`.

## 1. Story beats (26.0 s)

| Time | Beat | Line |
|---|---|---|
| 0.0-2.95 | the beach on a summer afternoon: Papá Noel at a camping table under an umbrella, his red vikings against silver on an open board, the sea and the bay's skyline behind; hook "Ajedrez de viaje / impreso en 3D" | S: "Uff… ¡partidita en la playa!" |
| 2.95-4.65 | a seagull swoops in, takes his king in its beak and flies off with it | — |
| 4.65-5.6 | Papá Noel, both arms up, looking up after it | S: "¡Mi rey!" |
| 5.6-6.95 | El Mago raises his hand: the open board and its pieces vanish (sparkles); the travel board appears, flat, with its faceted pieces | M: "Por eso, el de viaje:" |
| 6.95-7.95 | the pieces hop off into a pile | (the line goes on) |
| 7.95-9.3 | end-on view: the eight strips fold up into an octagonal tube, the squares outside; its caps appear | "…se pliega en un tubo…" |
| 9.3-10.65 | the whole tube; a tag "24 cm · con las piezas adentro" | "…de 24 centímetros," |
| 10.65-12.55 | from its end: the pieces hop into the open tube; the cap closes (a click) | "…y las piezas van adentro." |
| 12.55-14.15 | the gull is back: it lands by the tube and pecks it three times, for nothing; it tilts its head, miffed | — |
| 14.15-16.0 | Papá Noel points at the gull, triumphant | S: "¡Ja! ¡Ahora no podés!" |
| 16.0-17.7 | sunset, wide: the two at the table with the travel board open; the gull leaves | — |
| 17.7-19.9 | "Así es de verdad": the real photo, "Se pliega en un tubo de 24 cm con las piezas adentro" | — |
| 19.9-23.45 | El Mago points at the viewer | M: "¿Te vas de vacaciones? Comentá VIAJE y te paso precio y fecha." |
| 23.45-26.0 | card over the travel board, at sunset | — |

## 2. Product and props

| Item | Detail | Check |
|---|---|---|
| The travel chess | from `plegable.webp`: eight strips of eight squares (3 cm squares, a 24 × 24 board), cream and tan; folded, an octagonal tube 24 cm long with the squares on its faces and toothed caps at both ends; faceted pieces (prisms and polyhedra) in cream and tan | the fold frames, the 24 cm frame |
| The fold | each strip moves from its flat pose to its face of the octagon (the squares outward), the outer strips first, with a small lift | frames 8.2-9.2 |
| The pieces going in | from a pile beside the board, along arcs into the open end; each one shrinks as it enters | frame 11.2 |
| The open board | the chess kit's board with the viking set, red (his) against silver; the stolen king is carried in the beak (never teleported) and leaves with the gull | frames 3.75-4.2 |
| The seagull | white body and head, grey wings with black tips, a yellow beak with a red spot, orange legs; it flaps in flight, folds its wings when perched, pecks by pitching forward | QA "prop gull" vs both bodies, "gull-table" |
| The beach | sand (60 m, tiled), the sea (a scrolling texture, no sound), a foam line, a wet band, the sky with the bay's skyline (a generic city), the umbrella (red and white), a towel, a bucket, a camping table | QA furniture (table, legs, umbrella pole) |

## 3. Characters and acting

| Item | Detail | Check |
|---|---|---|
| Papá Noel | relaxed (a stretch); both arms up after his king, looking up; leans in when the gull is back; points at it, triumphant (left hand, a 0.55 s reach) | hands vs faces 0; beard gate 0 |
| El Mago | raises his hand for the swap only; watches the fold; points at the viewer for the CTA (a 0.55 s reach) | jumps 0 |

## 4. Camera and editing

- A cut every 0.9-2.9 s; every camera looks toward the sea.
- The theft is a wide shot from the front-left.
- The fold is end-on, so the octagon forms.
- The length is a frontal view of the whole tube.
- The pieces going in are seen from the tube's end, as in the product photo.
- Snap zooms on the grab, "¡Mi rey!", the 24 cm tag and "¡Ja!".

## 5. Text

- Hook "Ajedrez / de viaje / impreso en 3D".
- The "24 cm" tag.
- Kinetic captions.
- "Así es de verdad".
- The card:
  - "¿Te vas de vacaciones?";
  - "Ajedrez de viaje, impreso en 3D";
  - "¡Comentá VIAJE!";
  - "Te paso precio y fecha por mensaje / Pedidos para Navidad: hasta el 23 de diciembre";
  - the brand.

## 6. Sound

- The soft ambient bed (G mixolydian, page volume 0.22).
- No wave noise.
- The gull's calls (a low chirp), a whoosh for its swoop, a tap for the grab.
- Three pecks, the cap's click.
- No effect starts inside a spoken line (`cues.py` checks it).
