# Fotos de los vendidos: qué ya está hecho y qué le toca a la IA

Fotos sacadas con el celular y mandadas por WhatsApp (7/11/2026). Llegaron en 1600 × 1200 y
comprimidas por WhatsApp: la poca resolución viene sobre todo de esa compresión, no de la cámara.
Los originales están en `fuente/fotos/vendidos/`, con nombre según lo que muestran.

## Ya hecho, automático (`fuente/tools/imgs.py`, fotos con la marca "m" en `photos.py`)

- Recorte cuadrado de cada producto (centro y zoom en `photos.py`).
- Balance de blancos calculado solo con los píxeles casi neutros (paredes, casillas blancas, piezas
  grises). La mesa roja no cuenta, así no tiñe el resultado.
- Niveles (percentiles 0,5 y 99,5), un poco de luz en los medios tonos si la foto está oscura.
- Reducción a 600 px (eso solo ya limpia bastante ruido) y nitidez suave (unsharp 1,1 px, 55 %).
- Versión pixelada de 32 px para la animación de impresión.

Lo que el retoque automático **no puede** arreglar: el fondo (mesa roja pintada, cuadernos, cajas,
lápices, la caja de cereal), los artefactos de compresión en las piezas negras, el desenfoque de las
fotos de cerca, el reflejo de la mesa de vidrio y la luz pobre del ascensor. Eso va para la IA o,
mejor, para volver a sacar la foto (ver al final).

## Reglas para la IA (no se negocian)

1. **El producto no cambia.** Misma cantidad de piezas, misma forma, mismo color, misma posición.
   Si la IA "mejora" una pieza (le agrega detalle, la redibuja, cambia el dorado por otro dorado),
   esa versión se descarta. Lo que se vende tiene que ser lo que se ve (Ley 17.250, art. 24).
2. **Solo la foto de la tarjeta.** La IA edita la primera foto de cada producto (la que se ve en el
   catálogo). Las demás de la galería (`-2`, `-3`...) quedan con el retoque automático: así siempre
   hay fotos reales sin IA.
3. **Mismo encuadre y misma proporción** que el original (4:3 o 3:4). El recorte cuadrado lo hace
   `imgs.py` con los mismos números de siempre.
4. **Nada agregado:** ni texto, ni logos, ni reflejos, ni accesorios, ni manos.
5. Revisar cada resultado al lado del original antes de usarlo: contar las piezas (16 por bando),
   mirar caballos y torres, y en el contador que los números sigan siendo los mismos.

## Cómo se usa

1. Para cada foto de la tabla, generar la versión editada y guardarla en `fuente/fotos/ia/` con el
   **mismo nombre** que el original (`.png`, `.jpg` o `.webp`). Ej.:
   `fuente/fotos/ia/medieval-negro-dorado.png`.
2. Rehacer las fotos de esos productos: `python3 -I fuente/tools/imgs.py medieval vikingos ...`
   (si existe la versión de `fotos/ia/`, se usa esa y se saltea el retoque automático).
3. Rearmar la página: `python3 -I fuente/tools/build.py` (escribe `index.html` en la raíz).
4. Mirar la página en el celular antes de subir.

## Foto por foto

Prioridad 1 = la tarjeta del producto, se ve en el catálogo. Prioridad 2 = opcional.

| Prioridad | Archivo (`fotos/vendidos/`) | Producto (`id`) | Qué tiene | Qué pedirle |
|---|---|---|---|---|
| 1 | `medieval-negro-dorado.jpg` | `medieval` | Mesa roja, cuaderno arriba, piezas negras con poco detalle | Prompt A + B. "Recover shadow detail in the black pieces without changing their color." |
| 1 | `vikingos-dorado-gris-tablero-1.jpg` | `vikingos` | Mesa de vidrio con reflejos, juguetes y cajas atrás | Prompt A + B. El tablero gris con marco es parte de la foto: se queda. |
| 1 | `perros-gatos-perros-1.jpg` | `perros-gatos` | Fondo con lápices, foto de cerca algo blanda | Prompt A + B. "Keep the orange-yellow color of the dogs exactly as is." |
| 1 | `minimal-negro-blanco-1.jpg` | `minimal` | Mesa roja, tablero en diagonal | Prompt A + B. "White pieces stay pure white, black pieces stay matte black." |
| 1 | `minecraft-ajedrez-piezas.jpg` | `mc-ajedrez` | Cajas y lápices atrás, piezas negras desenfocadas | Prompt A + B. "Keep the green and black tiles and their icons exactly as they are." |
| 1 | `vikingos-dorado-gris-tablero-2.jpg` | `tablero` | Mesa de vidrio, silla y cajas | Prompt A + B. |
| 1 | `caballo-dragon.jpg` | `pieza` | Fondo de caja de cereal y cuaderno | Prompt A + B. "Keep every spike of the dragon's mane as it is." |
| 1 | `contador-magic-frente.jpg` | `contador` | Mesa blanca con brillo, polvo | Prompt A. "Do not change any digit or symbol on the dials." Fondo: solo emparejar el blanco. |
| 1 | `comedero-casita.jpg` | `casita` | Mesa de vidrio, muñeco y cajas atrás | Prompt A + B. Colores: lila con techo rosa, no cambiarlos. |
| 1 | `comedero-elfico-dorado.jpg` | `elfico` | En la mano, escritorio desordenado | Prompt A + B. La mano se puede sacar solo si no tapa el objeto; si lo tapa, dejarla. |
| 1 | `repisa-derretida-roja.jpg` | `repisa` | Pared blanca, sombra dura | Prompt A. Fondo casi listo: solo emparejar. |
| 1 | `ascensor-negro.jpg` | `ascensor` | Poca luz, fondo de living | Prompt A + B. "Brighten the scene; the towers are matte black plastic." |
| 2 | `medieval-gris-dorado-detalle.jpg` | `medieval-2` | Buena foto de cerca, fondo de taller | Solo si sobra tiempo: Prompt A. |
| 2 | `perros-gatos-gatos-1.jpg` | `perros-gatos-2` | Fondo de taller | Solo si sobra tiempo: Prompt A. |

Las otras fotos de `vendidos/` se usan en las galerías tal como quedaron con el retoque automático.

## Prompts (en inglés, que es como mejor responden estos modelos)

**A. Mejorar la foto sin tocar el producto**

> Edit this photo of a 3D-printed object. Improve only the photographic quality: neutralize the
> white balance, even out the lighting, reduce JPEG compression noise and blur, and gently sharpen
> edges. Keep the object exactly as it is: identical shapes, proportions, number of pieces,
> positions, colors, surface texture and visible print layer lines. Do not add, remove, move, rotate
> or redesign anything. Do not invent details, text, logos or reflections. Keep the same framing
> and the same aspect ratio as the original.

**B. Fondo limpio de catálogo** (después de A, en la misma imagen)

> Replace everything that is not the product (the table, papers, boxes, pens, wall, toys) with a
> seamless light warm-gray studio background (#E8E4DC) and a soft, natural contact shadow under the
> product. The product, including the chess board if there is one, must stay pixel-identical in
> shape, color, position and count: only the background changes. Same framing and aspect ratio.
> No added props, text, logos or reflections.

Si el modelo cambia el producto aunque se lo pidas, pedile solo la parte de B (fondo) y que devuelva
una máscara del producto: se pega el producto original encima del fondo nuevo.

## Mejor que la IA: volver a sacar la foto (para las próximas)

1. **Mandarlas como documento** por WhatsApp (o por Drive / Google Fotos en calidad original). Como
   foto, WhatsApp las achica y las comprime: esa es la mayor parte de la "poca resolución".
2. Luz de día, al lado de una ventana, sin flash.
3. Fondo liso: una cartulina o una sábana clara detrás y debajo, en vez de la mesa roja.
4. Para el juego completo: el tablero con las piezas en posición inicial, desde un costado y un poco
   de arriba (45°), con todo el tablero adentro de la foto.
5. Una foto de cerca del rey y del caballo, a la altura de las piezas.
6. Una foto con una moneda o una mano al lado, para que se vea el tamaño.

## Resultado de la primera tanda (8/11/2026)

Aceptadas (en `fotos/ia/`): ascensor, caballo dragón, casita, comedero élfico, contador, medieval
(negro y dorado y el detalle), minimalista, gatos, repisa, vikingo (tablero 1). Las que cambiaron el
fondo dicen "(fondo retocado)" en la galería.

Rechazadas (cambiaban el producto), siguen con el retoque automático:
- `minecraft-ajedrez-piezas.jpg`: las piezas negras quedaron derretidas.
- `vikingos-dorado-gris-tablero-2.jpg`: borró la esquina del tablero.
- `perros-gatos-perros-1.jpg`: contorno marrón recortado alrededor de los perros.
