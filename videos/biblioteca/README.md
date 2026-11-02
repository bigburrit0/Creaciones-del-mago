# Biblioteca de sprites de los reels

Personajes, escenarios, objetos, efectos e ítems que se generan **una vez** con Gemini y se reutilizan en todos los reels. Cada reel nuevo pide a Gemini solo lo que falta.

| Archivo | Qué es |
|---|---|
| `ESTILO.md` | Biblia de estilo: grilla 270×480 ×4, tamaños, formato de hojas 1024×1024, paleta, luz, direcciones y orden de aprobación. |
| `sprites.json` | **Fuente de verdad.** Personajes con sus animaciones (cuadro por cuadro), el taller (fondo, anclas, objetos con estados, adornos de temporada), efectos e ítems del catálogo. |
| `CATALOGO.md` | Tabla legible de todo lo que hay (generada). |
| `PROMPTS.md` | Los 74 prompts para Gemini de la biblioteca completa, en orden de aprobación (generado). |
| `palette.png` | Paleta de 32 colores para adjuntar en cada prompt (generada, sin Gemini). |
| `tools/gen_prompts.py` | Genera `PROMPTS.md`, `CATALOGO.md` y `palette.png`, para la biblioteca o filtrado para un reel. |

## Qué hay

- **El Mago: 48 animaciones.** 16 son emociones y reacciones: sorpresa, salto de alegría, risa, orgullo, pensar, idea, confusión, facepalm, tristeza, enojo, amor, vergüenza, nervios, impaciencia, miedo y festejo con giro. El resto se reparte en movimiento, reposo, trabajo en la impresora, magia, gestos (saludar, señalar, pulgar arriba, hablar, ofrecer mate, reverencia, encogerse de hombros) y sentado.
- **Taller del Mago**: fondo neutro todo el año, con anclas con nombre (mesa, impresora, centro, banquito, puerta, ventana). Los objetos con estados son sprites aparte: impresora (quieta, imprimiendo, lista), puerta, banquito, ventilador, caja de regalo, bolsa y mate. Los adornos de temporada también van aparte (Navidad: arbolito, guirnalda, corona), para que el mismo fondo sirva en cualquier época.
- **12 efectos**: destello, polvo, confeti, corazones, gotas de sudor, idea, vapor, espiral de confusión, polilla, anillo mágico, notas y partículas de luz. Ninguno usa letras.
- **16 ítems** del catálogo de Navidad, dibujados desde las fotos reales de `assets/p/`.

Las animaciones están marcadas con prioridad: **P0** (las usa el reel de Navidad), **P1** (siguiente tanda, las más útiles para cualquier reel) y **P2** (cuando haga falta).

## Cómo se usa en un reel

1. Escribir el `reel.json` del reel: personajes nuevos (si hay), lista `uses` con lo que toma de la biblioteca y los beats con tiempos (ver `../papa-noel-en-ojotas/reel.json`).
2. Generar sus prompts:
   ```bash
   python3 videos/biblioteca/tools/gen_prompts.py videos/biblioteca/sprites.json videos/<reel> --reel videos/<reel>/reel.json
   ```
3. Pedirle a Gemini **solo** las hojas que todavía no están aprobadas, en el orden de `PROMPTS.md`, adjuntando lo que dice cada bloque.
4. Guardar las aprobadas en `videos/biblioteca/sheets/` con el nombre indicado. Ahí quedan para el próximo reel.
5. Claude corta las hojas (el formato es fijo: 2×2 o 4×4 celdas, fondo magenta, ancla en el mismo píxel). Arma la **prueba de armado** de los beats y, cuando está aprobada, anima en HyperFrames.

## Cómo crece

- ¿Falta una emoción o una acción? Se agrega una entrada en `sprites.json` con sus poses cuadro por cuadro y se regeneran los prompts.
- ¿Personaje nuevo que se va a repetir (cliente, gato del taller, Papá Noel)? Se pasa del `reel.json` a `characters` en `sprites.json`.
- ¿Escenario nuevo (feria, playa, rambla)? Se agrega un set con su fondo, sus anclas y sus objetos. El Mago y los efectos sirven igual.
