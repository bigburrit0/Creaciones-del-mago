# "El laberinto" (November second wave W3, reach, 23.0 s)

Script and audit: `AUDIT.md`; everything on screen: `ON_SCREEN.md`; the wave: `../PLAN_NOVIEMBRE_2.md`.

## Dialogue (measured)

| t (s) | Who | Line |
|---|---|---|
| 0.25 | El Mago | Minotauro contra Hércules. |
| 4.30 | Papá Noel | ¿Y por dónde se sale? |
| 6.90 | El Mago | Es un ajedrez. Se sale ganando. |
| 9.75 | El Mago | Y este trae su tablero: cincuenta y dos por cincuenta. |
| 13.15 | Papá Noel | ¡Qué tablero! |
| 17.25 | El Mago | Comentá MINOTAURO y te paso precio y fecha. |

## Caption (ready to paste)

Curated by hand from the three caption writers (humour, practical, character). Left out:
- "el tablero le dijo": it was El Mago who said it;
- "Envío gratis solo en…": the shop's own words are "entrego sin costo";
- "#ajedrezdecorativo": not a stated use;
- "fecha límite para pedir, no de entrega": true, but it reads as small print. "Los pedidos van hasta el 23" says the same.

```
Minotauro contra Hércules 🏛️ Ajedrez Antigua Grecia impreso en 3D en Montevideo, con su propio tablero

Desde arriba parece un laberinto. Papá Noel buscó la salida con la manopla: un muro, la vuelta, otro muro… Yo le dije la verdad: es un ajedrez, se sale ganando.

Piezas rojas contra doradas: el Minotauro y Hércules de reyes, columnas, caballos alados y hoplitas. Y trae su tablero: 52 × 50 cm, con muros de piedra blanca y un templo.

Lo hago yo, pieza por pieza, a pedido. PLA si va adentro, PETG si va al sol o se usa mucho.

Comentá MINOTAURO y te paso precio y fecha 👇

Por WhatsApp al 092 104 419, antes de empezar y sin compromiso. Para Navidad, los pedidos van hasta el 23 de diciembre: cuanto antes, mejor.
Entrego sin costo en La Unión, La Blanqueada y parte de Buceo, y mando a todo Uruguay.

#AjedrezAntiguaGrecia #Ajedrez #Impresion3D #Montevideo #MitologiaGriega #CreacionesDelMago
```

## Private reply to each MINOTAURO comment (within 7 days)

> ¡Hola! Gracias por comentar 🏛️ ¿Para quién es el ajedrez? Te paso precio y fecha por WhatsApp al 092 104 419, sin compromiso. Los pedidos para Navidad van hasta el 23 de diciembre.

If there is no answer in about 24 h, send once:

> ¿Te quedó alguna duda? Te mando fotos del tablero con sus muros y el templo para que lo pienses tranquilo.

## Suggested publish date

Sunday 6/12 (after "La gaviota" on Thursday 3/12).

## Result (2026-11-15)

`el-laberinto.mp4`: 23.0 s, 1080 × 1920, 60 fps.

| Check | Result |
|---|---|
| QA gate | 0 bad frames of 1380, 0 pose jumps, deterministic. The gate covers his mitten against every wall block, the temple and the pieces |
| Flicker scan | 0 frames (cuts at 1.55, 2.7, 3.7, 4.65, 6.8, 9.55, 13.05, 14.95, 17.15, 20.3) |
| Loudness | the render came out at -14.9 LUFS. It was re-mixed with `remezclar.py` to -14.5 LUFS, peak -4.0 dBFS, the same as the other reels. The picture is byte-identical (same md5) |
| Steady buzz | none: no 37 Hz line above 6 kHz, and the high band sits at -33.7 dBFS |
| Music | 24.2 dB under the voices and 14.6 dB under them in the gaps (`nivel_musica.py`) |
| Voices in the mix | every line is clear ("Y este trae su tablero, 52 por 50") |
| Contact sheet | 15 real frames were looked at: the labyrinth from above rising into the board, the Minotaur, Hercules raising his club, Papá Noel leaning in, his mitten on the walls from above, the deadpan, the tapes with "52 cm" and then "52 × 50 cm", "¡Qué tablero!", the proof, the CTA |
