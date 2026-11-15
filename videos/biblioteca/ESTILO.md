# Biblia de estilo para los reels pixel art

Reglas fijas para **todas** las imágenes que se le piden a Gemini y para todo lo que se anima en HyperFrames. Si una imagen no las cumple, se vuelve a pedir: no se parchea después (ver `../WORKFLOW.md`).

## 1. Grilla

| Qué | Valor |
|---|---|
| Lienzo del video | 1080×1920, 30 fps |
| Grilla de arte | **270×480 píxeles de arte**, cada uno es un bloque de **4×4** píxeles del video |
| Escala | Siempre ×4 entera, con vecino más cercano. **Nunca** se reescala un sprite al 80 % ni a otro porcentaje |
| Cámara | Fija, vista cenital a tres cuartos (como un RPG o un juego de granja de 16 bits). Un reel = un escenario |
| Animación | Cambio de cuadros por pasos, a **8 fps** (125 ms por cuadro) salvo que se indique otra cosa. Los recorridos también van por pasos |

## 2. Tamaños

| Elemento | Altura en px de arte | Celda | Ancla |
|---|---|---|---|
| El Mago parado (punta del sombrero a la suela) | 96 | 128×128 | pies, en (64, 124) |
| Personajes adultos (Papá Noel, clientes) | 84 a 92 | 128×128 | pies, en (64, 124) |
| Animales chicos (gorrión, gato) | 16 a 32 | 64×64 | pies, en (32, 60) |
| Productos (ítems del catálogo) | hasta 40 | 64×64 | base, en (32, 56) |
| Muebles y objetos con estados (impresora, puerta, bolsa) | según el objeto | 128×128 | base, en (64, 124) |
| Efectos (destellos, polvo, corazones) | 8 a 32 | 64×64 | centro, en (32, 32) |

La **ancla** queda en el mismo píxel en todos los cuadros de una animación. Por eso, al cambiar de cuadro el sprite no salta.

## 3. Formato de las hojas para Gemini

- **Siempre 1024×1024 PNG**, fondo **magenta puro #FF00FF** que llene todo, sin sombras sobre el fondo, sin piso, sin texto, sin números, sin bordes ni líneas de grilla.
- Personajes y objetos: **grilla 2×2** de celdas de 512×512 px de imagen = 128×128 px de arte a ×4. Hasta 4 cuadros por hoja; los cuadros se leen de izquierda a derecha y de arriba abajo. Las animaciones de 6 u 8 cuadros van en 2 hojas, y la segunda se pide adjuntando la primera.
- Animales, ítems y efectos: **grilla 4×4** de celdas de 256×256 px = 64×64 px de arte a ×4.
- El píxel de arte debe verse como un bloque de 4×4 px de la imagen. Si Gemini devuelve bloques irregulares, el procesado los ajusta a la grilla, pero hay que pedirlo así.
- Fondos (plates): **9:16**, la escena completa a 270×480 píxeles de arte.

## 4. Paleta

Paleta maestra de 32 colores. La parte de El Mago está sacada de los keyframes que ya usamos; el resto se completa con la imagen maestra del taller y se congela.

| Uso | Hex |
|---|---|
| Contorno (único para todos los sprites) | `#150A34` |
| Túnica y sombrero: luz / medio / sombra | `#6A58B8` `#4B3A8E` `#2E2160` |
| Banda del sombrero y hebilla: luz / sombra | `#F2C14E` `#C98A2B` |
| Barba y pelo: luz / sombra | `#F0D8B2` `#C8AE88` |
| Piel: luz / sombra / mejillas | `#F0C090` `#E1AE73` `#D9826A` |
| Botas y cinturón: luz / sombra | `#8A5638` `#5A3424` |
| Mate (calabaza): luz / sombra; bombilla | `#A0603A` `#6E3B22`; `#D8D4C8` |
| Brillo mágico | `#FFF3B0` `#F2B640` |

Reglas de color:
- Ningún color de sprite a menos de 60 de distancia RGB del magenta #FF00FF. Por eso la túnica es violeta azulado y no magenta.
- 3 tonos por material (luz, medio, sombra). Sin degradés ni semitransparencias.

## 5. Luz, contorno y dither

- Luz desde **arriba a la izquierda**, sombra hacia abajo a la derecha, en todos los sprites y fondos.
- Contorno oscuro de 1 px de arte (`#150A34`) alrededor de cada sprite. Sin antialiasing contra el fondo.
- **Dither solo en los fondos** (cielo, pared), nunca en personajes ni objetos animados.
- La sombra en el piso de cada personaje **no** va en el sprite: se dibuja aparte (elipse de 2 tonos) para que no salte en los saltos.

## 6. Direcciones

- **S**: de frente, a tres cuartos mirando hacia la cámara. Es la dirección por defecto.
- **E**: perfil mirando a la derecha. **W** = E espejado (solo para caminar, correr y cargar).
- **N**: de espaldas (cuando trabaja en la mesa contra la pared del fondo).
- La mano que sostiene objetos (mate, ítems) es siempre la **derecha** del personaje. Si el espejo la pasa a la izquierda, esa animación no se espeja: se pide aparte.

## 7. Bloque de estilo (pegar al principio de cada prompt de Gemini)

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter
view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image
pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in
backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline
#150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per
material. Use only colours from the attached palette. No text, no letters, no numbers,
no logos, no watermark, no signature.
```

Para hojas de sprites se agrega:

```
SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no
shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal
512x512 cells, frames read left-to-right then top-to-bottom. The same character, same
size and same proportions in every cell; only the pose changes. The character's feet sit
on the same baseline in every cell, 16 image pixels above the bottom edge of the cell,
horizontally centred. Standing height: {ALTURA_PX} image pixels.
```

## 8. Orden de aprobación (gates)

Cada paso se aprueba antes de seguir, y lo aprobado se **adjunta** como referencia en todos los prompts que vienen después:

1. Paleta (imagen de 32 cuadraditos, sin texto).
2. Model sheet de cada personaje (S, E, N parado).
3. Imagen maestra del escenario.
4. Fondo vacío (edición de la maestra).
5. Hojas de animación y de estados de objetos.
6. Prueba de armado: Claude compone los beats del guion con las piezas y se revisan **antes** de animar.

## 9. Nombres de archivo

`<personaje|objeto>_<accion>_<direccion>_<parte>.png`, por ejemplo `mago_walk_E_1.png` (cuadros 1 a 4) y `mago_walk_E_2.png` (5 a 8). Los fondos: `plate_<escenario>.png`. Los ítems: `item_<producto>.png` (hoja 4×4).
