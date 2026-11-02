# Reel 2 · «Continue?» (la manija del termo)

**Resumen:** en un banco de la rambla se parte la manija del termo. Todo se pone gris, aparece «CONTINUE? 9, 8, 7»
como en los arcades, y cae una manija dorada nueva que encastra y devuelve el color. Repuesto a medida.
9:16, 10 s.

Es la **manija** y no el tapón ni el pico: según la guía del termo, solo se imprimen las piezas que no tocan el agua
caliente.

---

## PASO 1 · Generar las imágenes (una por una, en este orden)

Copiá cada prompt entero en Gemini y generá una imagen por vez. Guardalas como `imagen-1.png` a `imagen-4.png`.

> **Para que salgan parecidas entre sí:** desde la imagen 2 en adelante, adjuntá la imagen 1 junto con el prompt.

### Imagen 1 · 0:00 · El termo en la rambla

```
Vertical 9:16 image (1080x1920). Static side view of a wooden bench on the seaside promenade of Montevideo, Uruguay, at golden hour. On the bench, in the center of the frame: a tall brushed-steel vacuum flask with a cup lid and a dark gray plastic side handle that has a thin visible crack, and next to it a round mate gourd with a metal straw. Behind: a low stone sea wall, the wide river-sea with small sparkling waves, a warm gold and indigo sky with the sun low on the horizon, and the faint silhouette of a lighthouse on a hill far away on the left. Quiet summer evening. Generic flask and gourd, no brand shapes or colors.

Style: authentic 16-bit home-console pixel art from the early 1990s. Hard square pixels on a visible grid, 1-pixel dark outlines, no anti-aliasing, no blur, no soft gradients (only ordered dithering), limited palette of about 24 colors: deep night indigo #1F1A3D and #2A2350, violet-blue #4E4399, warm cream #F3E9D2, gold #F2A93B as the main accent, small touches of pine green #2F6B4F and warm red #E2504C. Flat 2D game look, not a 3D render, not photorealistic. Keep the top 13% and the bottom 22% of the image calm and plain (sky at the top, plain bench and pavement at the bottom) for text. No text, no letters, no numbers, no logos, no watermarks.
```

### Imagen 2 · 0:03 · Se rompió: todo en gris

```
Vertical 9:16 image (1080x1920). Exactly the same scene and framing as before: static side view of a wooden bench on the seaside promenade of Montevideo, a low stone sea wall, the wide river-sea, the sun low on the horizon, a faint lighthouse silhouette far away on the left. On the bench, in the center: the tall brushed-steel vacuum flask with a cup lid now has NO handle; the broken dark gray plastic handle lies on the bench next to it in two pieces, with a few tiny pixel sparks. The round mate gourd with a metal straw is still next to the flask. The whole image is in grayscale and slightly dimmed, like a game-over screen in an arcade game: no color at all, only grays, with the darkest areas in near-black. Generic flask and gourd, no brand shapes.

Style: authentic 16-bit home-console pixel art from the early 1990s. Hard square pixels on a visible grid, 1-pixel dark outlines, no anti-aliasing, no blur, no soft gradients (only ordered dithering), limited palette. Flat 2D game look, not a 3D render, not photorealistic. Keep the top 13% and the bottom 22% of the image calm and plain for text, and leave the middle of the sky fairly empty for a big word that will be added later. No text, no letters, no numbers, no logos, no watermarks.
```

### Imagen 3 · 0:06 · Cae la manija nueva

```
Vertical 9:16 image (1080x1920). Same scene and framing: static side view of a wooden bench on the seaside promenade of Montevideo at golden hour, low stone sea wall, sparkling river-sea, the sun low on the horizon, faint lighthouse silhouette far away on the left. On the bench, in the center: the tall brushed-steel vacuum flask without a handle and the round mate gourd with a metal straw. Just above the flask, a brand-new handle in bright gold (#F2A93B) plastic is floating down like a video game power-up item, tilted mid-spin, surrounded by small twinkling gold sparkles; it is clearly a separate 3D-printed part with fine horizontal layer lines. Color is coming back into the scene: a circle of full warm color spreads out from the gold handle, while the edges of the image are still grayscale.

Style: authentic 16-bit home-console pixel art from the early 1990s. Hard square pixels on a visible grid, 1-pixel dark outlines, no anti-aliasing, no blur, no soft gradients (only ordered dithering), limited palette of about 24 colors: deep night indigo #1F1A3D and #2A2350, violet-blue #4E4399, warm cream #F3E9D2, gold #F2A93B as the main accent, small touches of pine green #2F6B4F and warm red #E2504C. Flat 2D game look, not a 3D render, not photorealistic. Keep the top 13% and the bottom 22% of the image calm and plain for text. No text, no letters, no numbers, no logos, no watermarks.
```

### Imagen 4 · 0:10 · El termo arreglado (último cuadro)

```
Vertical 9:16 image (1080x1920). Same scene and framing, in full warm color: static side view of a wooden bench on the seaside promenade of Montevideo at golden hour, low stone sea wall, sparkling river-sea, the sun low on the horizon, faint lighthouse silhouette far away on the left. On the bench, in the center: the tall brushed-steel vacuum flask with a cup lid, now with a brand-new bright gold (#F2A93B) plastic side handle firmly attached, clearly a separate 3D-printed part with fine horizontal layer lines. Next to it, the round mate gourd with a metal straw, with a thin wisp of steam rising from it. Two small seagulls glide in the sky on the right. Calm, satisfied mood. Generic flask and gourd, no brand shapes.

Style: authentic 16-bit home-console pixel art from the early 1990s. Hard square pixels on a visible grid, 1-pixel dark outlines, no anti-aliasing, no blur, no soft gradients (only ordered dithering), limited palette of about 24 colors: deep night indigo #1F1A3D and #2A2350, violet-blue #4E4399, warm cream #F3E9D2, gold #F2A93B as the main accent, small touches of pine green #2F6B4F and warm red #E2504C. Flat 2D game look, not a 3D render, not photorealistic. Keep the top 13% and the bottom 22% of the image calm and plain (sky at the top, plain bench and pavement at the bottom) for text. No text, no letters, no numbers, no logos, no watermarks.
```

**Antes de pasar al video, revisá:** que el termo no tenga logo ni el verde típico de una marca, que la manija nueva
sea dorada y se vea como pieza aparte, y que el fondo sea el mismo en las cuatro.

---

## PASO 2 · Generar el video completo con las imágenes

En Gemini, video **9:16 de 10 segundos**. Adjuntá las cuatro imágenes **en orden** (imagen 1, 2, 3 y 4) y pegá este
prompt:

```
Create one 10-second vertical 9:16 video using the four attached images as keyframes, in this order: Image 1 is the first frame (0 s), Image 2 appears at about 3 s, Image 3 at about 6 s, and Image 4 is the final frame (10 s). Keep exactly the look, objects, colors and pixel art style of the images and animate smoothly from one to the next.

Single continuous shot, no cuts. Locked-off static camera, side view, no zoom, no pan, no depth of field, no motion blur. Authentic 16-bit pixel art animated like a 1990s arcade game: hard square pixels, limited palette, low frame-rate sprite animation, flat 2D for the whole clip.

Action:
0 to 2 seconds (Image 1): half a second in, the gray handle snaps off the flask with a small burst of pixel sparks and falls onto the bench in two pieces; the whole image shakes for a moment, like a hit in a fighting game.
2 to 5 seconds (Image 1 to Image 2): all colors drain to grayscale and the scene dims, like a game-over screen; the waves almost stop; nothing else moves.
5 to 7 seconds (Image 2 to Image 3 to Image 4): a new bright gold handle drops from the top of the frame, spinning slowly like a video game power-up, with twinkling sparkles; it snaps onto the flask; full color floods back into the scene, spreading outward from the gold handle.
7 to 10 seconds (Image 4): a thin wisp of steam rises from the mate gourd, two seagulls glide across the sky, the waves sparkle again. The last second holds still.

Audio: a sharp plastic crack and a punchy 16-bit hit; then three low tense beeps, one per second, like an arcade continue countdown; then a bright rising chiptune arpeggio and a satisfying snap-fit click; then a short victory chord, gentle waves and distant seagulls. No dialogue, no voice, no music with lyrics.

No text, no letters, no numbers, no subtitles, no captions, no logos anywhere in the video.
```

**Si tu herramienta no acepta 4 imágenes:**
- Si acepta **primer y último cuadro**: usá la imagen 1 y la imagen 4, con el mismo prompt.
- Si acepta **una sola imagen**: usá la imagen 1, con el mismo prompt.
- Si el video sale de **8 s**: en la edición, congelá el último cuadro 2 s más.
- Si el paso a gris no sale: en la edición, bajá la saturación a 0 entre 0:02 y 0:05 y subila de golpe en 0:05.

---

## Después: guion, voz, texto y edición

### Guion (para la edición)

| Tiempo | Qué pasa | Texto en pantalla (se pone en la edición) | Voz en off |
|---|---|---|---|
| 0:00 – 0:02 | Se parte la manija, la imagen tiembla | `¡CRAC!` chiquito, al lado de la manija | «¿Se te rompió la manija del termo?» |
| 0:02 – 0:05 | Todo gris, el termo solo | `CONTINUE?` grande y la cuenta `9`, `8`, `7` (uno por segundo) | «No lo tires.» |
| 0:05 – 0:07 | Cae la manija dorada, vuelve el color | `+1 MANIJA` en dorado | «Mandame fotos y medidas» |
| 0:07 – 0:10 | Vapor del mate, gaviotas | `¿Se rompió una pieza del termo?` / `Mandame fotos y medidas · WhatsApp 092 104 419` | «y, si se puede imprimir, te la hago.» |

**Voz en off completa** (grabala vos con el celular):
> «¿Se te rompió la manija del termo? No lo tires. Mandame fotos y medidas y, si se puede imprimir, te la hago.»

### Texto del post

> ¿Se te rompió la manija del termo? Las piezas que no tocan el agua caliente (la manija, el anillo de agarre, la
> base) las imprimo en 3D a partir de fotos y medidas, en PETG para que aguanten. Las que tocan el agua, como el
> tapón o la rosca del pico, no: te lo digo antes y no perdés nada. Te paso precio y fecha por WhatsApp antes de
> empezar, sin compromiso. 092 104 419 · Montevideo

**Otros cierres para probar** (cambian el texto de 0:07 a 0:10 y la última frase de la voz):
- **Cualquier repuesto:** `¿Una manija, una perilla, un clip? Mandame una foto` · «Mandame una foto y te digo si se puede.»
- **Sin riesgo:** `Si no se puede imprimir, te aviso antes` · «Si no se puede imprimir, te lo digo antes de empezar.»
- **Comentarios:** `¿Qué tenés roto en un cajón?` · «¿Qué tenés roto en un cajón esperando? Contame.»

### Edición (CapCut o Canva)

- `CONTINUE?` es lo más importante: grande, centrado, crema `#F3E9D2` con contorno índigo `#1F1A3D`, que parpadee
  una vez por segundo. Los números abajo, más grandes, en sincronía con los pitidos.
- `+1 MANIJA` en dorado `#F2A93B`: que suba un poco y se desvanezca en 1 s.
- Cierre: caja índigo con borde dorado arriba de la zona de botones de Instagram, y el glifo real
  `assets/px/glifo-oro.png` arriba de la caja.
- La voz arranca en 0:00, sobre el «crac».
- Dejá libres los 250 px de arriba y los 420 px de abajo (ahí van los botones de la app).
