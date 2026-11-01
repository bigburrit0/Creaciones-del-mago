# Imágenes de las guías: instrucciones para Gemini

Cada guía ya funciona sin estas imágenes: mientras no existan, la portada usa una foto del catálogo y las
figuras del texto no se muestran. Cuando generes una, guardala con el **nombre exacto** en `assets/guias/`
y corré `python3 -I fuente/tools/guias.py`. El generador la detecta solo.

## Reglas para todas

- **Son ilustraciones, nunca fotos de producto.** No pedirle a Gemini que muestre una pieza del catálogo
  "como si fuera real": quien compra tiene que ver la pieza real en las fotos del catálogo.
- **Sin texto, sin logos, sin marcas** (ni Hot Wheels, ni Minecraft, ni escudos de clubes, ni el logo
  del Mago). Gemini dibuja mal las letras y las marcas son de otros.
- **Sin personas reales.** No inventar "clientes" ni retratos del dueño.
- **Formato:** portada 2100 × 800 px (21:8). En celular se recorta a 4:3, así que **lo importante va
  en el tercio del medio**. Exportar a WebP (calidad 80) o PNG y convertir.
- **Estilo común** (pegarlo al final de cada instrucción):

```
Style: 16-bit pixel art, like the item shop of a 1990s console RPG. Hard pixel edges, no anti-aliasing, no gradients except dithering. Limited palette: deep night indigo #1F1A3D and #2A2350 for backgrounds, warm cream #F3E9D2 for light surfaces, gold #F2A93B as the single accent, small touches of pine green #2F6B4F and festive red #E2504C. Calm, warm, a little whimsical. No text, no letters, no logos, no brand characters, no people's faces. Wide composition 21:8, main subject centered in the middle third so it survives a 4:3 crop.
```

## 1. Regalos de Navidad · `navidad-hero.webp`

Guía: `/guias/regalos-de-navidad-impresos-en-3d/`. Texto alternativo ya cargado: "Ilustración en pixel art de
una impresora 3D en una noche de verano, imprimiendo un arbolito de Navidad dorado".

```
A small desktop 3D printer (open-frame bed-slinger type, no brand marks) on a wooden workbench by an open window, on a warm SUMMER night in Montevideo, Uruguay (Christmas in Uruguay is in summer: no snow). The printer is finishing a small golden Christmas tree; the nozzle glows. Around it on the bench: three little wrapped gift boxes with ribbons, a spool of gold filament, a tiny toy car and a chess knight as silhouettes (generic, no brands). Through the window: a starry indigo sky, a full moon, distant low city lights and the silhouette of palm fronds. A string of tiny red, gold and green pixel lights runs along the top edge.
```
+ estilo común.

## 2. Amigo invisible · `amigo-invisible-hero.webp`

Guía: `/guias/regalos-para-amigo-invisible-impresos-en-3d/`.

```
An office desk seen from slightly above at night, lit by a desk lamp. On the desk, a row of small wrapped gifts in cream paper with gold ribbons, each with a blank tag (no writing). Between them, tiny colorful palm-sized toy figures with a round button on top (fidget clickers): a coffee cup, a banana, a potted succulent, a little mushroom. A paper bag with a ribbon. Cozy, playful, generic objects, no brands.
```
+ estilo común.

## 3. Exhibidores para autitos · `exhibidores-hero.webp`

Guía: `/guias/exhibidores-para-autitos-1-64/`.

```
A living-room wall at night with a modular wall display for small 1:64 die-cast toy cars: dark hexagonal honeycomb cells and a small stacked garage shelf, each cell holding one tiny colorful generic car (no real car brands, no logos). A warm lamp lights the wall from below. A shoebox full of more tiny cars sits on the floor, half open. Calm collector mood.
```
+ estilo común.

## 4. PLA o PETG · `pla-petg-hero.webp`

Guía: `/guias/pla-o-petg-cual-elegir/`.

```
A split scene divided vertically in the middle. Left half: indoors at night, a wooden shelf with a chess piece, a small figure and a desk organizer, lit by a lamp, cool indigo tones. Right half: a sunny garden in the afternoon, a bird feeder hanging from a branch with two small birds, a flower pot, a strong pixel sun. Both halves share the same horizon line so they read as one image. No text, no labels.
```
+ estilo común.

## 5. Qué mandar para pedir · `que-mandar-hero.webp`

Guía: `/guias/que-mandar-para-pedir-una-pieza-en-3d/`.

```
A workbench seen from above: a smartphone showing a blank photo frame, a metal ruler, a hand-drawn sketch on cream paper with dimension arrows (no numbers or letters), a broken plastic knob in two pieces, a pencil, and a small 3D printed replacement knob in gold next to it. Orderly flat-lay, warm lamp light.
```
+ estilo común.

## 5b. Figura dentro del texto · `que-mandar-foto.webp` (1600 × 900, 16:9)

Va en la sección "Si tenés una foto". Se muestra sola cuando existe el archivo.

```
Instructional pixel art diagram in two panels side by side, separated by a thin gold line. Left panel: a small plastic knob photographed FROM THE FRONT, with a ruler lying right next to it. Right panel: the same knob photographed FROM THE SIDE, with the same ruler. Above each panel a simple pixel camera icon pointing at the object. Plain cream background. No text, no numbers.
```
+ estilo común (cambiar "Wide composition 21:8" por "16:9").

## Cuando las tengas

1. Guardalas en `assets/guias/` con estos nombres.
2. Revisá que pesen menos de 300 KB cada una.
3. `python3 -I fuente/tools/guias.py` y listo: portada, tarjeta del índice y vista previa al compartir usan la imagen nueva.
