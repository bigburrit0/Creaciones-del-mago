# "El mantel" (November second wave W4, conversion and cross-sell, 24.5 s)

Script and audit: `AUDIT.md`; everything on screen: `ON_SCREEN.md`; the wave: `../PLAN_NOVIEMBRE_2.md`.

## Dialogue (measured)

| t (s) | Who | Line |
|---|---|---|
| 0.20 | Papá Noel | ¡Ya tengo mi ajedrez! |
| 2.30 | El Mago | Eso es un mantel. |
| 4.50 | Papá Noel | ¿Y qué tiene? |
| 6.30 | El Mago | Un tablero reglamentario, que se arma por partes. Para las piezas que ya tenés. |
| 12.75 | El Mago | Pedidos hasta el veintitrés de diciembre. |
| 17.50 | El Mago | ¿Ya tenés las piezas? Comentá TABLERO y te paso precio y fecha. |

## Caption (ready to paste)

Curated by hand from the three caption writers (humour, practical, character). Left out:
- "Envío gratis en…": the shop's own words are "entrego sin costo";
- "pieza por pieza": it's a board;
- "(fecha límite para pedir, no de entrega)": it reads as small print.

```
¿Eso es un mantel? ♟️ Tablero de ajedrez impreso en 3D en Montevideo, para las piezas que ya tenés

Nochebuena. Papá Noel armó la partida sobre el mantel a cuadros: demasiados cuadros, las piezas arriba de las rayas y un peón que se cae en el pliegue. "¿Y qué tiene?" Que es un mantel 🙃

El tablero:
• tamaño reglamentario;
• se arma por partes;
• cuadros blancos y negros, con marco gris;
• no trae piezas: es para las que ya tenés.

Lo hago yo, a pedido. PLA si va adentro, PETG si va al sol o se usa mucho.

¿Ya tenés las piezas? Comentá TABLERO y te paso precio y fecha 👇

Por WhatsApp al 092 104 419, antes de empezar y sin compromiso. Para Navidad, los pedidos van hasta el 23 de diciembre: cuanto antes, mejor.
Entrego sin costo en La Unión, La Blanqueada y parte de Buceo, y mando a todo Uruguay.

#TableroDeAjedrez #Ajedrez #Impresion3D #Montevideo #Navidad #CreacionesDelMago
```

## Private reply to each TABLERO comment (within 7 days)

> ¡Hola! Gracias por comentar ♟️ ¿Para quién es el tablero? Te paso precio y fecha por WhatsApp al 092 104 419, sin compromiso. Los pedidos para Navidad van hasta el 23 de diciembre.

If there is no answer in about 24 h, send once:

> ¿Te quedó alguna duda? Te mando fotos del tablero armado para que lo pienses tranquilo.

## Suggested publish date

Sunday 13/12 (after "El laberinto" on Sunday 6/12; ten days before the last order day).

## Result (2026-11-15)

`el-mantel.mp4`: 24.5 s, 1080 × 1920, 60 fps.

| Check | Result |
|---|---|
| QA gate | 0 bad frames of 1470, 0 pose jumps, deterministic. The gate covers the table with its hanging cloth, the feast, every piece and every board part against both bodies, and the hands against the table |
| Flicker scan | 0 frames (cuts at 2.25, 3.72, 4.45, 5.95, 6.6, 9.65, 12.6, 15.25, 17.4, 22.0) |
| Loudness | -14.5 LUFS, peak -1.5 dBFS, straight from the render (no remix needed) |
| Steady buzz | none: no 37 Hz line above 6 kHz, and the high band sits at -35.2 dBFS |
| Music | 26.0 dB under the voices and 16.3 dB under them in the gaps (`nivel_musica.py`): a little softer than the others |
| Voices in the mix | every line is clear |
| Contact sheet | 15 real frames were looked at: the hook along the table, "Eso es un mantel", the pawn tipping over on the fold, the shrug, the magic hand, the quadrants and frame sides fitting together from above, the pieces landing, the calendar page with the 23 circled, the CTA, the card |
