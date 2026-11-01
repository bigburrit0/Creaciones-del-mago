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

## Ajedrez (guías 6 a 10)

Mismo estilo común. Ninguna imagen muestra piezas de marcas o personajes de películas o videojuegos.

### 6. Ajedrez personalizado · `ajedrez-personalizado-hero.webp`
```
A chessboard on a wooden table at night, mid-game. One army is gold #F2A93B, the other is a deep teal, clearly different colors. Next to the board, four small spools of filament in gold, teal, cream and red, and a small pixel-art color swatch card with blank squares (no text). Warm lamp light from the left, starry window behind.
```

### 7. Medidas de un ajedrez · `medidas-ajedrez-hero.webp`
```
Six classic chess pieces (king, queen, bishop, knight, rook, pawn) lined up from tallest to shortest on a cream surface, with a long wooden ruler lying in front of them and a single board square drawn beside the king's base. Clean side view, like a museum display. No numbers or text on the ruler: just tick marks.
```

### 8. Pieza perdida · `pieza-perdida-hero.webp`
```
A chessboard seen from above, mid-game, with one empty square glowing softly where a knight should be. Next to the board: the matching knight of the other color lying on its side, a ruler, a smartphone and a bottle cap used as a stand-in piece. Cozy living room at night, warm light.
```

### 8b. Figura · `pieza-perdida-medir.webp` (1600 × 900)
```
Instructional diagram in two panels. Left: a chess knight seen from the side next to a vertical ruler, with a gold arrow showing its height. Right: the same knight seen from above, with a gold arrow across the width of its round base. Plain cream background. No text, no numbers.
```

### 9. Historia de las piezas · `historia-piezas-hero.webp`
```
Medieval-style carved chess pieces inspired by 12th-century Norse ivory chessmen, in cream ivory color: a seated king with a sword across his knees, a seated queen resting her cheek on her hand, a bishop with a mitre, and a foot warrior biting the top of his shield. They stand on a dark stone surface in a museum display case at night, a single warm spotlight from above. Next to them, a plain classic modern chess knight in gold for contrast.
```

### 10. Ajedrez para chicos · `ajedrez-chicos-hero.webp`
```
A child's bedroom table seen from slightly above. A chessboard where one army is cartoon dogs and the other is cartoon cats, in bright orange and blue. A few pieces have been captured and sit to the side. Colorful, friendly, warm afternoon light through the window. No people visible, no text.
```

## Aeromodelismo (guías 11 a 14)

Mismo estilo común. Aviones genéricos, sin marcas ni matrículas.

### 11. Avión RC impreso en 3D · `avion-rc-hero.webp`
```
A small radio-controlled airplane with a high wing, white and orange, flying low over a wide green field at golden hour, Uruguayan countryside with eucalyptus trees on the horizon. In the foreground, a small table with a 3D printer and a few orange printed airplane parts. Warm sunset sky with gold #F2A93B, pixel clouds.
```

### 12. Repuestos RC · `repuestos-rc-hero.webp`
```
A workbench seen from above at night: a radio-controlled airplane partially disassembled, a cracked orange plastic motor mount next to an identical new gold printed one, a small screwdriver, a ruler and a smartphone. Warm lamp light, cozy workshop.
```

### 13. PLA o PETG para RC · `pla-petg-rc-hero.webp`
```
Two filament spools on a workbench, one matte gold and one glossy translucent teal, between them printed airplane parts: a wing section, a motor mount, a landing gear cover. Behind, a small RC airplane hanging on the wall. Night workshop, warm lamp light.
```

### 14. Avión con chicos · `avion-chicos-hero.webp`
```
A white and orange hand-launched glider flying over a summer field in Uruguay, bright blue sky with a few pixel clouds. Far away and small, two silhouettes (an adult and a child, no faces visible) watching it fly. Warm, joyful summer afternoon.
```

## Cuando las tengas

1. Guardalas en `assets/guias/` con estos nombres.
2. Revisá que pesen menos de 300 KB cada una.
3. `python3 -I fuente/tools/guias.py` y listo: portada, tarjeta del índice y vista previa al compartir usan la imagen nueva.
