# "Culpa de las piezas" (chess series reel 5, conversion, 24.2 s)

Script and audit: `AUDIT.md`; everything on screen: `ON_SCREEN.md`; the series: `../PLAN_AJEDREZ.md`.
The Christmas cut-off is the owner's: **the last day to order is 23 December** (not a delivery promise).

## Dialogue (measured)

| t (s) | Who | Line |
|---|---|---|
| 0.55 | Papá Noel | ¡Me hicieron trampa las piezas! |
| 4.50 | El Mago | Las piezas no pierden. Vos sí. |
| 7.35 | Papá Noel | Mmm… quiero el mío. ¡Para Navidad! |
| 9.90 | El Mago | Entonces no esperes: un juego lleva muchas horas de impresora. |
| 13.50 | Papá Noel | ¿Hasta cuándo lo puedo pedir? |
| 14.70 | El Mago | Hasta el 23 de diciembre. |
| 19.05 | El Mago | Comentá PEDIR y te paso precio y fecha. |

## Caption (ready to paste)

Curated by hand from the three caption writers (humour, practical, character). None wrote "envío gratis a todo Uruguay".
One wrote "No te prometo que llegue para Navidad"; it was left out (true, but it reads as a warning). The cut-off is
stated as the last order day, next to the honest "cuanto antes, mejor".

```
Papá Noel perdió otra vez con su ajedrez vikingo impreso en 3D… y le echó la culpa a las piezas ♟️

"¡Me hicieron trampa las piezas!" Y las piezas lo miraron, una por una. Yo le contesté: las piezas no pierden. Vos sí.

Ahora quiere el suyo, rojo como él, para Navidad 🎄
Los pedidos para Navidad van hasta el 23 de diciembre. Un juego completo lleva muchas horas de impresora: cuanto antes lo pidas, mejor.

Lo hago yo, pieza por pieza, en Montevideo. Vikingo o medieval, y vos elegís:
• Los colores de cada bando, hasta 4 por pieza.
• El tamaño: el rey de torneo mide 9,5 cm; puedo llegar a 25 cm por pieza.
• El material: PLA para adentro, PETG si va al sol o se usa mucho.
Son las piezas; el tablero va aparte.

¿Querés el tuyo? Comentá PEDIR y te paso precio y fecha 👇

Por WhatsApp al 092 104 419, antes de empezar y sin compromiso.
Entrego sin costo en La Unión, La Blanqueada y parte de Buceo, y mando a todo Uruguay.

#AjedrezVikingo #AjedrezMedieval #RegalosDeNavidad #Impresion3D #Montevideo #CreacionesDelMago
```

## Private reply to each PEDIR comment (within 7 days)

> ¡Hola! Gracias por comentar 🎄 ¿Para quién es el ajedrez? Contame si lo querés vikingo o medieval y en qué colores, y te paso precio y fecha por WhatsApp al 092 104 419, sin compromiso. Los pedidos para Navidad van hasta el 23 de diciembre.

If there is no answer in about 24 h, send once:

> ¿Te quedó alguna duda? Te mando medidas y colores para que lo pienses tranquilo.

## Suggested publish date

Thursday 26/11, in Black Week, as in the plan (after reel 4 on Sunday 22/11). It leaves almost four weeks before the
cut-off.

## Result (2026-11-13)

`culpa-de-las-piezas.mp4`: 24.2 s, 1080×1920, 60 fps.
- QA gate: 0 bad frames out of 1452, 0 pose jumps, deterministic (it passed the first time).
- Flicker scan: 0 frames.
- Loudness: -14.1 LUFS, true peak -2.3 dBFS (the render's own mix peaked at -1.0 dB; the sound was rebuilt with
  `remezclar.py`, the picture byte-identical).
- No steady buzz: 37 Hz is 5.7 dB above the median in the band above 6 kHz (the cicadas were 34 dB); the 16 Hz
  modulation is the music, as in reels 1-4.
- Voices: the first mix check heard "Vos sí" as "o sí" and "Comentá PEDIR" as "Comenzá a pedir". A pop sat on "Vos";
  it moved after the word, and the music now ducks deeper (0.18) under the punchline and the CTA. The new mix reads
  "Las piezas no pierden, vos sí" and "Hasta el 23 de diciembre". One check still heard "Comená a pedir"; the subtitles
  and the card spell PEDIR.
- The container restarted at 64% of the first render; it was relaunched.
