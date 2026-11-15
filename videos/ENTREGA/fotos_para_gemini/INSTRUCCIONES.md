# Fotos de estudio con Gemini: instrucciones

Para qué: en los reels, la parte «Así es de verdad» ahora muestra varias fotos reales que van cambiando. Las fotos de
la web son chicas (600 × 600) y varias son caseras (mesa de madera, mesada, living). Con Gemini se pueden convertir en
**fotos de estudio**: fondo liso, buena luz, nítidas y grandes, **sin cambiar el producto**.

En `originales/` están las 16 fotos (las que usan los reels, más el ajedrez minimalista y el escultórico). Las de
Minecraft, Star Wars, Harry Potter y Hello Kitty quedan afuera por ser marcas registradas.

## Paso a paso (en la app de Gemini o en gemini.google.com)

1. Abrí un chat nuevo y elegí la herramienta de **crear o editar imágenes**.
2. Subí **una sola** foto de `originales/`.
3. Pegá el **pedido base** (abajo, en inglés: Gemini respeta mejor el producto así) y, al final, la **línea propia de
   esa foto** (en `PEDIDOS.md`).
4. **Revisá antes de guardar:** compará con el original.
   - ¿Están todas las piezas? ¿Mismo número, mismas formas, mismos colores?
   - ¿No inventó detalles, texto ni logos? ¿El fondo quedó liso, sin la mesa ni la casa?
   - Si algo cambió, escribile: *«The product changed. Keep every piece exactly as in the original photo; only
     change the background and the lighting.»* y pedí otra.
   - **Nunca** uses una foto donde el producto no sea el real: el cliente tiene que recibir lo que vio.
5. Guardala en PNG con **el mismo nombre** (`grecia.png`, `tablero.png`…).
6. Mandámelas por acá, o ponelas en la carpeta `assets/estudio/` del repositorio. Las galerías de los reels se
   rehacen solas con las fotos nuevas.

## Pedido base (copiar y pegar)

```
Edit this photo into a professional studio product photograph of the exact same 3D-printed product.
Keep the product 100% identical: the same pieces, the same number of pieces, the same shapes, colors, textures,
proportions and positions. Do not add, remove, redesign, repaint or "improve" anything, and do not add text or logos.
Replace everything around the product with a seamless studio backdrop (an infinity curve) in a soft warm light grey
(#EDEAE4): no table, no room, no clutter.
Lighting: a large soft key light from the upper left, a soft fill from the right and a subtle rim light so the pieces
stand out from the background; soft, natural contact shadows under every piece.
Sharp focus across the whole product, true-to-life colors, no glare, no blur, no vignette.
Square 1:1, high resolution (2048 x 2048), the product centered and filling about 80% of the frame.
```

## Mejor todavía: fotos nuevas de cada producto

Una sola foto por producto no alcanza para «ver realmente el producto». Si sacás **3 o 4 fotos más de cada uno** con el
celular y las pasás por el mismo pedido, las galerías las muestran en lugar de los acercamientos de la foto única.
`FOTOS_NUEVAS.md` dice qué tomas sacar y cómo sacarlas. Se llaman con número: `grecia-2.png`, `grecia-3.png`…
