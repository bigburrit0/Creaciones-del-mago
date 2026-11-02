# Pedirle las hojas al modelo de imagen

`gen_prompts.py` escribe cada prompt completo, con el bloque de estilo, el bloque de hoja, el sujeto y cada cuadro. Este archivo explica cómo usarlos y qué hacer cuando el modelo no cumple.

## Rutina

1. Pedir en el orden de `PROMPTS.md`. Si un paso no está aprobado, no se sigue: todo lo que viene después lo usa como referencia.
2. Adjuntar exactamente lo que dice cada bloque: `palette.png`, el model sheet del personaje y, en la segunda hoja de una animación, la primera.
3. Guardar lo aprobado con el **nombre exacto** en `biblioteca/sheets/`. Así el recorte la usa en lugar de la provisoria.
4. Correr el ensamblado y revisar `review/`. Ahí se ve la línea de ancla roja y la superposición en papel cebolla: si los cuadros no se apilan bien, la hoja vuelve a pedirse.

Cuando hay un límite de uso, conviene pedir primero los P0 y empezar por los model sheets, la maestra y el fondo. Con eso ya se valida que el modelo respeta la grilla.

## Qué revisar al aprobar

- Fondo magenta plano. Si hay sombras o degradé, se pide de nuevo.
- Las 4 celdas respetadas, sin personajes que crucen de celda.
- El mismo tamaño de personaje en todas las celdas. El reporte avisa si la altura difiere más de un 10 % de la pedida.
- Píxeles en bloques parejos. El recorte tolera bordes suaves y una grilla corrida, pero no un cambio de escala dentro de la hoja.
- Sin texto ni números.
- Colores parecidos a la paleta. El recorte cuantiza, pero si el modelo inventa un color nuevo, se va a ver distinto.

## Problemas típicos y cómo pedirlo de nuevo

| Problema | Re-pedido |
|---|---|
| Cambia el diseño del personaje entre hojas | Adjuntar el model sheet y agregar: "identical character design, compare with the attached model sheet before drawing" |
| Tamaños distintos por celda | "the character has exactly the same height in all four cells, {H} image pixels" y adjuntar una hoja aprobada como ejemplo de escala |
| Celdas desordenadas o cuadros de más | Pedir 2 cuadros por hoja (celdas 3 y 4 vacías) |
| Píxeles borrosos o "pintados" | "crisp pixel art, every art pixel is a 4x4 block, no painterly shading, no blur" |
| Sombra sobre el magenta | "no drop shadow, no ground shadow, the background is one flat colour #FF00FF" |
| Texto o firmas | "no text, no letters, no signature anywhere" |
| Objeto en la mano equivocada en W | Pedir la animación en W aparte y marcar `mirror_to_W: false` |

## Seguridad de marca

Para productos de terceros (personajes de videojuegos, consolas, escudos), pedir el objeto **sin logos ni texto**. La silueta y los colores alcanzan para reconocerlo.
