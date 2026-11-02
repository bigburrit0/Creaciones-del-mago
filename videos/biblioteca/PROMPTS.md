# Prompts para el modelo de imagen

Generado por `pixel-reel/scripts/gen_prompts.py`. No editar a mano: cambiar el manifiesto y regenerar.
Pedir en este orden. Cada imagen aprobada se guarda con el nombre indicado en la carpeta de hojas y se adjunta en los prompts siguientes.

## Gate 1 · Paleta

`palette.png` ya está generada. No hace falta pedirla.

## Gate 2 · Model sheets

### El Mago · model sheet

Archivo: `mago_model.png`

Adjuntar:
- `palette.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels (96 art pixels).

SUBJECT: El Mago, an old, kind, friendly wizard with a long white beard covering his chest, rosy cheeks, small black eyes and a round nose; a tall floppy purple wizard hat whose tip curls backwards, with a gold band; a long violet-blue robe with wide sleeves; a brown belt with a square gold buckle; brown boots. He is short and round, cute chibi proportions (head about one third of his height). Colours: robe and hat #6A58B8 #4B3A8E #2E2160, gold #F2C14E #C98A2B, beard #F0D8B2 #C8AE88, skin #F0C090 #E1AE73 #D9826A, boots and belt #8A5638 #5A3424, outline #150A34.

MODEL SHEET:
Cell 1: front three-quarter view facing the camera (S), standing, hands resting on the belly
Cell 2: side view facing right (E), standing
Cell 3: back view (N), standing
Cell 4: front view (S) holding a mate gourd with a metal straw at chest height with his right hand
```

## Gate 3 · Imagen maestra del escenario

### El taller del Mago · imagen maestra

Archivo: `plate_taller_master.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

FORMAT: 9:16 vertical PNG, the whole scene is 270x480 art pixels (each art pixel a 4x4 block).

SCENE: the cosy one-room workshop of a wizard who makes 3D printed things, seen from a top-down three-quarter view like a 1990s farming RPG interior. Back wall: warm honey-coloured wooden planks; in the centre a square window with a summer blue sky, a bright sun and the green leafy branch of a plane tree; on the left half of the back wall two wooden shelves with small colourful 3D printed objects and four spools of filament (red, blue, gold, green). Against the back wall on the left: a sturdy wooden workbench (no printer on it, the printer is a separate sprite). Right side wall: a wooden door (closed) with a small brass knob, the door is a separate sprite so leave a door-shaped dark frame. Floor: warm wooden boards running left-right, a round woven rug in the centre, a small empty patch near the door for a stool. Bottom edge: a strip of terracotta and cream checkered tiles. Bright summer daylight coming from the window (upper-left light). Nothing on the floor, no characters, no animals, no furniture other than the shelves and the workbench. 
For scale only: El Mago (attached model sheet) stands in the scene, 96 art pixels tall.
```

## Gate 4 · Fondo vacío

### El taller del Mago · fondo vacío

Archivo: `plate_taller.png`

Adjuntar:
- `plate_taller_master.png`

```
Same image, same camera, same pixel grid, same palette and light. Remove every character and any seasonal decoration. Keep only the empty set exactly as it is. Fill the hidden areas naturally. 9:16 PNG.
```

## Gate 5 · Animaciones, objetos, efectos e ítems

### El Mago · walk_E · 6 cuadros · loop · P0 (hoja 1/2)

Archivo: `mago_walk_E_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: walk_E (cross the room left to right (W = mirrored)), seen from the side, facing RIGHT, frames 1-4 of 6, looping.
Cell 1: right foot forward touching ground, left arm forward
Cell 2: body lowest, knees bent, hat tip dips
Cell 3: passing pose, legs together, body highest
Cell 4: left foot forward touching ground, right arm forward
```

### El Mago · walk_E · 6 cuadros · loop · P0 (hoja 2/2)

Archivo: `mago_walk_E_2.png`

Adjuntar:
- `palette.png`
- `mago_model.png`
- `mago_walk_E_1.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size). This sheet continues the attached first sheet of the same animation: keep exactly the same size, position and baseline.
ACTION: walk_E (cross the room left to right (W = mirrored)), seen from the side, facing RIGHT, frames 5-6 of 6, looping.
Cell 1: body lowest, knees bent, hat tip dips
Cell 2: passing pose, legs together, body highest
Cell 3: leave empty (plain magenta)
Cell 4: leave empty (plain magenta)
```

### El Mago · walk_S · 6 cuadros · loop · P1 (hoja 1/2)

Archivo: `mago_walk_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: walk_S (walk towards the camera), facing the camera in a front three-quarter view, frames 1-4 of 6, looping.
Cell 1: right boot forward, left hand swinging
Cell 2: body down, robe hem flares
Cell 3: passing, body up
Cell 4: left boot forward, right hand swinging
```

### El Mago · walk_S · 6 cuadros · loop · P1 (hoja 2/2)

Archivo: `mago_walk_S_2.png`

Adjuntar:
- `palette.png`
- `mago_model.png`
- `mago_walk_S_1.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size). This sheet continues the attached first sheet of the same animation: keep exactly the same size, position and baseline.
ACTION: walk_S (walk towards the camera), facing the camera in a front three-quarter view, frames 5-6 of 6, looping.
Cell 1: body down, robe hem flares
Cell 2: passing, body up
Cell 3: leave empty (plain magenta)
Cell 4: leave empty (plain magenta)
```

### El Mago · walk_N · 6 cuadros · loop · P1 (hoja 1/2)

Archivo: `mago_walk_N_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: walk_N (walk away from the camera), seen from behind, facing away from the camera, frames 1-4 of 6, looping.
Cell 1: seen from behind, right boot forward
Cell 2: body down
Cell 3: passing, body up
Cell 4: left boot forward
```

### El Mago · walk_N · 6 cuadros · loop · P1 (hoja 2/2)

Archivo: `mago_walk_N_2.png`

Adjuntar:
- `palette.png`
- `mago_model.png`
- `mago_walk_N_1.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size). This sheet continues the attached first sheet of the same animation: keep exactly the same size, position and baseline.
ACTION: walk_N (walk away from the camera), seen from behind, facing away from the camera, frames 5-6 of 6, looping.
Cell 1: body down
Cell 2: passing, body up
Cell 3: leave empty (plain magenta)
Cell 4: leave empty (plain magenta)
```

### El Mago · run_E · 6 cuadros · loop · P2 (hoja 1/2)

Archivo: `mago_run_E_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: run_E (hurry, chase something), seen from the side, facing RIGHT, frames 1-4 of 6, looping.
Cell 1: long stride, right leg forward, left hand holding the hat on his head
Cell 2: both feet off the ground, robe streaming back
Cell 3: landing on right foot, body low
Cell 4: long stride, left leg forward, hand on hat
```

### El Mago · run_E · 6 cuadros · loop · P2 (hoja 2/2)

Archivo: `mago_run_E_2.png`

Adjuntar:
- `palette.png`
- `mago_model.png`
- `mago_run_E_1.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size). This sheet continues the attached first sheet of the same animation: keep exactly the same size, position and baseline.
ACTION: run_E (hurry, chase something), seen from the side, facing RIGHT, frames 5-6 of 6, looping.
Cell 1: both feet off the ground
Cell 2: landing on left foot
Cell 3: leave empty (plain magenta)
Cell 4: leave empty (plain magenta)
```

### El Mago · turn_S_to_N · 3 cuadros · once · P0

Archivo: `mago_turn_S_to_N_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: turn_S_to_N (turn to the workbench; play reversed for N to S), turning from facing the camera to facing away, frames 1-3 of 3, played once.
Cell 1: facing the camera (S), neutral
Cell 2: three-quarter back view, head turning
Cell 3: seen fully from behind (N)
Cell 4: leave empty (plain magenta)
```

### El Mago · idle_S · 4 cuadros · loop · P0

Archivo: `mago_idle_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: idle_S (default standing loop), facing the camera in a front three-quarter view, frames 1-4 of 4, looping.
Cell 1: neutral standing, hands resting on belly
Cell 2: chest slightly up, beard lifts one pixel
Cell 3: neutral standing
Cell 4: chest slightly down, hat brim one pixel lower
```

### El Mago · idle_N · 4 cuadros · loop · P0

Archivo: `mago_idle_N_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: idle_N (default loop while working at the bench), seen from behind, facing away from the camera, frames 1-4 of 4, looping.
Cell 1: seen from behind, standing at the bench
Cell 2: shoulders up one pixel
Cell 3: neutral
Cell 4: shoulders down one pixel
```

### El Mago · blink_S · 3 cuadros · once · P1

Archivo: `mago_blink_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: blink_S (life in long holds (play 1-2-3-2-1)), facing the camera in a front three-quarter view, frames 1-3 of 3, played once.
Cell 1: eyes open
Cell 2: eyes half closed
Cell 3: eyes closed
Cell 4: leave empty (plain magenta)
```

### El Mago · look_around_S · 4 cuadros · once · P1

Archivo: `mago_look_around_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: look_around_S (waiting, curiosity), facing the camera in a front three-quarter view, frames 1-4 of 4, played once.
Cell 1: looking at the camera
Cell 2: head and eyes turned to his left
Cell 3: looking at the camera
Cell 4: head and eyes turned to his right
```

### El Mago · sip_mate_S · 6 cuadros · once · P0 (hoja 1/2)

Archivo: `mago_sip_mate_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`
- `mate: el sprite del objeto si ya existe`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: sip_mate_S (signature mate sip, calm endings), facing the camera in a front three-quarter view, frames 1-4 of 6, played once.
Cell 1: holding the mate gourd at chest height with the right hand
Cell 2: lifting the gourd, straw approaching the beard
Cell 3: sipping, eyes closed, cheeks puffed
Cell 4: sipping, eyes closed, cheeks in
```

### El Mago · sip_mate_S · 6 cuadros · once · P0 (hoja 2/2)

Archivo: `mago_sip_mate_S_2.png`

Adjuntar:
- `palette.png`
- `mago_model.png`
- `mago_sip_mate_S_1.png`
- `mate: el sprite del objeto si ya existe`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size). This sheet continues the attached first sheet of the same animation: keep exactly the same size, position and baseline.
ACTION: sip_mate_S (signature mate sip, calm endings), facing the camera in a front three-quarter view, frames 5-6 of 6, played once.
Cell 1: lowering the gourd, content smile
Cell 2: gourd back at chest, relaxed sigh
Cell 3: leave empty (plain magenta)
Cell 4: leave empty (plain magenta)
```

### El Mago · sleepy_S · 4 cuadros · loop · P2

Archivo: `mago_sleepy_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: sleepy_S (late night, waiting for a long print), facing the camera in a front three-quarter view, frames 1-4 of 4, looping.
Cell 1: eyes half closed, head upright
Cell 2: head drooping forward
Cell 3: head low, hat brim covering the eyes
Cell 4: jerks awake, eyes wide, back upright
```

### El Mago · surprised_S · 4 cuadros · hold · P0

Archivo: `mago_surprised_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: surprised_S (something unexpected happens), facing the camera in a front three-quarter view, frames 1-4 of 4, played once, the last frame is held.
Cell 1: neutral
Cell 2: anticipation: body squashed down, eyes closing
Cell 3: jolt: body stretched up, eyes wide, mouth open, both hands up at shoulder height, hat lifting off the head
Cell 4: eyes wide, hands up, hat back on (hold this frame)
```

### El Mago · joy_jump_S · 6 cuadros · once · P0 (hoja 1/2)

Archivo: `mago_joy_jump_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: joy_jump_S (victory, happy reveal, a sale), facing the camera in a front three-quarter view, frames 1-4 of 6, played once.
Cell 1: anticipation crouch, fists at the chest, big smile
Cell 2: takes off, both fists up, feet together
Cell 3: apex, arms fully up, robe flaring, hat floating above the head
Cell 4: falling, arms up, hat coming down
```

### El Mago · joy_jump_S · 6 cuadros · once · P0 (hoja 2/2)

Archivo: `mago_joy_jump_S_2.png`

Adjuntar:
- `palette.png`
- `mago_model.png`
- `mago_joy_jump_S_1.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size). This sheet continues the attached first sheet of the same animation: keep exactly the same size, position and baseline.
ACTION: joy_jump_S (victory, happy reveal, a sale), facing the camera in a front three-quarter view, frames 5-6 of 6, played once.
Cell 1: landing squash, knees bent
Cell 2: recover, both fists up, eyes closed with joy
Cell 3: leave empty (plain magenta)
Cell 4: leave empty (plain magenta)
```

### El Mago · laugh_S · 4 cuadros · loop · P1

Archivo: `mago_laugh_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: laugh_S (funny moment), facing the camera in a front three-quarter view, frames 1-4 of 4, looping.
Cell 1: leaning back, hand on belly, eyes closed, mouth open
Cell 2: shoulders up, beard shaking
Cell 3: leaning back, mouth open
Cell 4: shoulders down
```

### El Mago · proud_S · 4 cuadros · hold · P1

Archivo: `mago_proud_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: proud_S (showing a finished piece), facing the camera in a front three-quarter view, frames 1-4 of 4, played once, the last frame is held.
Cell 1: neutral
Cell 2: chest puffing out, chin rising
Cell 3: chin up, eyes closed, thumbs hooked in the belt
Cell 4: same pose, small sparkle on the gold buckle (hold)
```

### El Mago · thinking_S · 4 cuadros · loop · P0

Archivo: `mago_thinking_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: thinking_S (considering, planning), facing the camera in a front three-quarter view, frames 1-4 of 4, looping.
Cell 1: right hand stroking the beard, eyes looking up-left
Cell 2: hand lower on the beard
Cell 3: hand stroking the beard, eyes looking up-right
Cell 4: hand lower on the beard
```

### El Mago · idea_S · 4 cuadros · hold · P0

Archivo: `mago_idea_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: idea_S (eureka moment (add fx_idea above the head)), facing the camera in a front three-quarter view, frames 1-4 of 4, played once, the last frame is held.
Cell 1: thinking pose, hand on beard
Cell 2: eyes snap wide open, back straightens
Cell 3: right index finger raised high, big smile
Cell 4: same pose, eyes sparkling (hold)
```

### El Mago · confused_S · 4 cuadros · loop · P1

Archivo: `mago_confused_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: confused_S (doesn't understand an order (add fx_swirl)), facing the camera in a front three-quarter view, frames 1-4 of 4, looping.
Cell 1: head tilted left, right hand scratching under the hat brim
Cell 2: hat lifted one pixel, scratching
Cell 3: head tilted right, scratching
Cell 4: hat lifted one pixel
```

### El Mago · facepalm_S · 4 cuadros · hold · P1

Archivo: `mago_facepalm_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: facepalm_S (a failed print, a funny mistake), facing the camera in a front three-quarter view, frames 1-4 of 4, played once, the last frame is held.
Cell 1: neutral
Cell 2: right hand rising to the face
Cell 3: palm covering the eyes, head tilted down, shoulders slumped
Cell 4: same, small sigh (hold)
```

### El Mago · sad_S · 4 cuadros · hold · P1

Archivo: `mago_sad_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: sad_S (something broke, sold out), facing the camera in a front three-quarter view, frames 1-4 of 4, played once, the last frame is held.
Cell 1: neutral
Cell 2: shoulders dropping
Cell 3: head down, hat brim low, mouth turned down
Cell 4: same, one small tear (hold)
```

### El Mago · grumpy_S · 4 cuadros · loop · P2

Archivo: `mago_grumpy_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: grumpy_S (printer jam (add fx_steam)), facing the camera in a front three-quarter view, frames 1-4 of 4, looping.
Cell 1: arms crossed, frowning, eyebrows down
Cell 2: cheeks puffed, frowning
Cell 3: arms crossed, frowning
Cell 4: cheeks puffed, small huff
```

### El Mago · love_S · 4 cuadros · loop · P2

Archivo: `mago_love_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: love_S (a lovely gift, a customer photo (add fx_hearts)), facing the camera in a front three-quarter view, frames 1-4 of 4, looping.
Cell 1: hands clasped at the chest, eyes closed, blushing
Cell 2: leaning slightly left
Cell 3: hands clasped, blushing
Cell 4: leaning slightly right
```

### El Mago · shy_S · 4 cuadros · loop · P2

Archivo: `mago_shy_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: shy_S (receiving a compliment), facing the camera in a front three-quarter view, frames 1-4 of 4, looping.
Cell 1: blushing, looking down, fingers touching
Cell 2: pulling the hat brim down with the right hand
Cell 3: blushing, looking down
Cell 4: peeking up from under the brim
```

### El Mago · nervous_S · 4 cuadros · loop · P2

Archivo: `mago_nervous_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: nervous_S (deadline, Christmas rush (add fx_sweat)), facing the camera in a front three-quarter view, frames 1-4 of 4, looping.
Cell 1: forced smile, two sweat drops on the forehead, fingers fidgeting
Cell 2: glancing left
Cell 3: forced smile, sweat drops
Cell 4: glancing right
```

### El Mago · impatient_S · 4 cuadros · loop · P2

Archivo: `mago_impatient_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: impatient_S (waiting for a long print), facing the camera in a front three-quarter view, frames 1-4 of 4, looping.
Cell 1: arms crossed, right foot raised
Cell 2: arms crossed, right foot tapping down
Cell 3: arms crossed, right foot raised
Cell 4: arms crossed, foot down, eyes rolling up
```

### El Mago · scared_S · 4 cuadros · loop · P2

Archivo: `mago_scared_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: scared_S (a spooky print, Halloween), facing the camera in a front three-quarter view, frames 1-4 of 4, looping.
Cell 1: shivering, knees together, hands up near the face, eyes wide
Cell 2: same pose shifted one pixel left
Cell 3: same pose
Cell 4: same pose shifted one pixel right
```

### El Mago · celebrate_spin_S · 6 cuadros · once · P1 (hoja 1/2)

Archivo: `mago_celebrate_spin_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: celebrate_spin_S (big celebration, end of a reel), facing the camera in a front three-quarter view, frames 1-4 of 6, played once.
Cell 1: arms up, facing the camera
Cell 2: spinning, side view, robe flaring
Cell 3: spinning, seen from behind, arms up
Cell 4: spinning, other side, robe flaring
```

### El Mago · celebrate_spin_S · 6 cuadros · once · P1 (hoja 2/2)

Archivo: `mago_celebrate_spin_S_2.png`

Adjuntar:
- `palette.png`
- `mago_model.png`
- `mago_celebrate_spin_S_1.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size). This sheet continues the attached first sheet of the same animation: keep exactly the same size, position and baseline.
ACTION: celebrate_spin_S (big celebration, end of a reel), facing the camera in a front three-quarter view, frames 5-6 of 6, played once.
Cell 1: facing the camera, arms up wide
Cell 2: final pose, one fist up, wink
Cell 3: leave empty (plain magenta)
Cell 4: leave empty (plain magenta)
```

### El Mago · press_button_N · 4 cuadros · loop · P0

Archivo: `mago_press_button_N_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: press_button_N (starting a print, working at the printer), seen from behind, facing away from the camera, frames 1-4 of 4, looping.
Cell 1: seen from behind at the bench, right arm reaching to the printer screen
Cell 2: index finger pressing
Cell 3: arm pulling back
Cell 4: head tilting, watching the printer
```

### El Mago · take_print_N · 4 cuadros · once · P1

Archivo: `mago_take_print_N_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: take_print_N (taking a finished piece out), seen from behind, facing away from the camera, frames 1-4 of 4, played once.
Cell 1: seen from behind, both hands reaching into the printer
Cell 2: lifting the build plate
Cell 3: bending the plate, piece popping off
Cell 4: holding the piece up
```

### El Mago · item_get_S · 4 cuadros · hold · P0

Archivo: `mago_item_get_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: item_get_S (RPG 'item get' reveal; the item sprite is placed above the hands), facing the camera in a front three-quarter view, frames 1-4 of 4, played once, the last frame is held.
Cell 1: facing the camera, both hands at the chest
Cell 2: lifting both hands, body stretching
Cell 3: both hands holding an object high above the head, triumphant smile (the object is drawn separately)
Cell 4: same pose, eyes closed with pride (hold)
```

### El Mago · toss_E · 4 cuadros · once · P0

Archivo: `mago_toss_E_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: toss_E (throw a piece to someone on the right (W = mirrored if the hand is not visible)), seen from the side, facing RIGHT, frames 1-4 of 4, played once.
Cell 1: side view, right hand low behind the body holding a small object position
Cell 2: swinging the arm forward underhand
Cell 3: arm forward and up, hand open (object released)
Cell 4: follow-through, smiling
```

### El Mago · inspect_S · 4 cuadros · loop · P1

Archivo: `mago_inspect_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: inspect_S (quality check (piece drawn separately)), facing the camera in a front three-quarter view, frames 1-4 of 4, looping.
Cell 1: holding a small piece close to the face with both hands, one eye squinting
Cell 2: turning the piece
Cell 3: looking at it from the other side
Cell 4: nodding, satisfied
```

### El Mago · carry_box_E · 6 cuadros · loop · P1 (hoja 1/2)

Archivo: `mago_carry_box_E_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: carry_box_E (deliveries, carrying gifts), seen from the side, facing RIGHT, frames 1-4 of 6, looping.
Cell 1: walking, holding a box at the chest with both arms (box drawn separately), right foot forward
Cell 2: body down
Cell 3: passing, body up
Cell 4: left foot forward
```

### El Mago · carry_box_E · 6 cuadros · loop · P1 (hoja 2/2)

Archivo: `mago_carry_box_E_2.png`

Adjuntar:
- `palette.png`
- `mago_model.png`
- `mago_carry_box_E_1.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size). This sheet continues the attached first sheet of the same animation: keep exactly the same size, position and baseline.
ACTION: carry_box_E (deliveries, carrying gifts), seen from the side, facing RIGHT, frames 5-6 of 6, looping.
Cell 1: body down
Cell 2: passing, body up
Cell 3: leave empty (plain magenta)
Cell 4: leave empty (plain magenta)
```

### El Mago · wrap_gift_S · 4 cuadros · loop · P2

Archivo: `mago_wrap_gift_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: wrap_gift_S (Christmas packing), facing the camera in a front three-quarter view, frames 1-4 of 4, looping.
Cell 1: hands folding paper on a box in front of him
Cell 2: pulling a ribbon tight
Cell 3: tying a bow
Cell 4: patting the box, smiling
```

### El Mago · sand_piece_S · 4 cuadros · loop · P2

Archivo: `mago_sand_piece_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: sand_piece_S (post-processing), facing the camera in a front three-quarter view, frames 1-4 of 4, looping.
Cell 1: holding a piece in the left hand, sanding with the right
Cell 2: sanding stroke right
Cell 3: sanding stroke left
Cell 4: blowing the dust off
```

### El Mago · cast_S · 6 cuadros · once · P1 (hoja 1/2)

Archivo: `mago_cast_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: cast_S (big magic moment (add fx_magic_ring)), facing the camera in a front three-quarter view, frames 1-4 of 6, played once.
Cell 1: hands together at the chest
Cell 2: arms rising, hands glowing gold
Cell 3: arms spread wide up, hands glowing, robe lifting
Cell 4: arms forward, releasing the glow, smiling
```

### El Mago · cast_S · 6 cuadros · once · P1 (hoja 2/2)

Archivo: `mago_cast_S_2.png`

Adjuntar:
- `palette.png`
- `mago_model.png`
- `mago_cast_S_1.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size). This sheet continues the attached first sheet of the same animation: keep exactly the same size, position and baseline.
ACTION: cast_S (big magic moment (add fx_magic_ring)), facing the camera in a front three-quarter view, frames 5-6 of 6, played once.
Cell 1: arms lowering
Cell 2: neutral, satisfied
Cell 3: leave empty (plain magenta)
Cell 4: leave empty (plain magenta)
```

### El Mago · snap_summon_S · 4 cuadros · once · P1

Archivo: `mago_snap_summon_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: snap_summon_S (make something appear (add fx_puff where it appears)), facing the camera in a front three-quarter view, frames 1-4 of 4, played once.
Cell 1: right hand raised, fingers ready to snap
Cell 2: snap: fingers clicked, small star at the fingertips
Cell 3: hand still raised, looking to his right with a grin
Cell 4: hand lowering
```

### El Mago · levitate_S · 4 cuadros · loop · P2

Archivo: `mago_levitate_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: levitate_S (an object floating over his hands (object drawn separately)), facing the camera in a front three-quarter view, frames 1-4 of 4, looping.
Cell 1: both palms up at chest height, eyes on something floating above
Cell 2: palms one pixel higher
Cell 3: palms up
Cell 4: palms one pixel lower
```

### El Mago · wave_S · 4 cuadros · loop · P0

Archivo: `mago_wave_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: wave_S (hello / goodbye), facing the camera in a front three-quarter view, frames 1-4 of 4, looping.
Cell 1: right hand raised to the side, open palm, smiling
Cell 2: hand tilted outward
Cell 3: hand raised, open palm
Cell 4: hand tilted inward
```

### El Mago · point_E · 3 cuadros · hold · P1

Archivo: `mago_point_E_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: point_E (look at this (W = mirrored)), seen from the side, facing RIGHT, frames 1-3 of 3, played once, the last frame is held.
Cell 1: side view, neutral
Cell 2: arm extending forward
Cell 3: arm fully extended, index finger pointing right, eyebrows up
Cell 4: leave empty (plain magenta)
```

### El Mago · thumbs_up_S · 3 cuadros · hold · P1

Archivo: `mago_thumbs_up_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: thumbs_up_S (approval, 'listo'), facing the camera in a front three-quarter view, frames 1-3 of 3, played once, the last frame is held.
Cell 1: neutral
Cell 2: right arm rising
Cell 3: thumb up at chest height, wink, big smile
Cell 4: leave empty (plain magenta)
```

### El Mago · talk_S · 4 cuadros · loop · P1

Archivo: `mago_talk_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: talk_S (explaining something to the camera (no speech bubble text)), facing the camera in a front three-quarter view, frames 1-4 of 4, looping.
Cell 1: mouth open, right hand open at chest height
Cell 2: mouth closed, eyebrows up
Cell 3: mouth open, both hands slightly apart
Cell 4: mouth half open, nodding
```

### El Mago · offer_mate_E · 3 cuadros · hold · P0

Archivo: `mago_offer_mate_E_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`
- `mate: el sprite del objeto si ya existe`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: offer_mate_E (offering mate to a guest), seen from the side, facing RIGHT, frames 1-3 of 3, played once, the last frame is held.
Cell 1: side view, holding the mate gourd at the chest with the right hand
Cell 2: extending the arm forward
Cell 3: arm fully extended offering the gourd to the right, friendly smile
Cell 4: leave empty (plain magenta)
```

### El Mago · bow_S · 4 cuadros · once · P2

Archivo: `mago_bow_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: bow_S (thank you), facing the camera in a front three-quarter view, frames 1-4 of 4, played once.
Cell 1: neutral
Cell 2: bowing, one hand on the chest, hat tilting
Cell 3: deep bow, hat held on the head with the other hand
Cell 4: back up, smiling
```

### El Mago · shrug_S · 3 cuadros · hold · P1

Archivo: `mago_shrug_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: shrug_S ('qué le vas a hacer'), facing the camera in a front three-quarter view, frames 1-3 of 3, played once, the last frame is held.
Cell 1: neutral
Cell 2: shoulders rising, palms turning up
Cell 3: shrug: palms up at the sides, eyebrows raised, crooked smile
Cell 4: leave empty (plain magenta)
```

### El Mago · sit_down_S · 4 cuadros · once · P1

Archivo: `mago_sit_down_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: sit_down_S (sit on a stool or chair (seat drawn separately)), facing the camera in a front three-quarter view, frames 1-4 of 4, played once.
Cell 1: standing in front of a stool
Cell 2: bending the knees
Cell 3: sitting on the stool (stool drawn separately), hands on the knees
Cell 4: settled, relaxed
```

### El Mago · sit_mate_S · 4 cuadros · loop · P1

Archivo: `mago_sit_mate_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`
- `mate: el sprite del objeto si ya existe`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: sit_mate_S (calm ending), facing the camera in a front three-quarter view, frames 1-4 of 4, looping.
Cell 1: sitting, mate at the chest
Cell 2: lifting the gourd
Cell 3: sipping, eyes closed
Cell 4: lowering, content
```

### El Mago · sit_doze_S · 4 cuadros · loop · P2

Archivo: `mago_sit_doze_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: sit_doze_S (night shift while a print runs), facing the camera in a front three-quarter view, frames 1-4 of 4, looping.
Cell 1: sitting, head dropping forward
Cell 2: hat brim over the eyes, chest down
Cell 3: chest up
Cell 4: head low
```

### Objeto · printer · 4 estados

Archivo: `printer.png`

Adjuntar:
- `palette.png`
- `plate_taller_master.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.

SUBJECT: printer for El taller del Mago (the shop's printer; frames 2-3 loop while printing). about 52x44 art px, base anchored at the bottom centre of the cell
STATES:
Cell 1: idle: compact desktop 3D printer, open frame with one upright gantry on the left side and a moving bed, light grey and charcoal, small screen on the front, a gold filament spool on top, no logo
Cell 2: printing: the nozzle carriage at the left, the bed pushed back, a tiny orange glow at the nozzle
Cell 3: printing: the nozzle carriage at the right, the bed pulled forward, tiny orange glow
Cell 4: done: nozzle parked, a small green light on the screen, a soft gold sparkle above the empty bed
```

### Objeto · door_R · 3 estados

Archivo: `door_R.png`

Adjuntar:
- `palette.png`
- `plate_taller_master.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.

SUBJECT: door R for El taller del Mago (people come in and out). about 34x80 art px
STATES:
Cell 1: closed wooden door on a right-hand side wall seen in three-quarter view, brass knob
Cell 2: door ajar, a thin slice of bright sunlight
Cell 3: door wide open, swung inward, a rectangle of bright summer sunlight on the floor
Cell 4: leave empty (plain magenta)
```

### Objeto · gift_box · 4 estados

Archivo: `gift_box.png`

Adjuntar:
- `palette.png`
- `plate_taller_master.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.

SUBJECT: gift box for El taller del Mago (reveals and unboxings). about 40x40 art px
STATES:
Cell 1: closed square gift box wrapped in red paper with a gold ribbon and bow
Cell 2: lid lifting, gold light leaking out
Cell 3: lid off to the side, box open, gold light beam
Cell 4: open empty box, lid leaning on it
```

### Objeto · sack · 4 estados

Archivo: `sack.png`

Adjuntar:
- `palette.png`
- `plate_taller_master.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.

SUBJECT: sack for El taller del Mago (Santa's sack filling up). about 44x48 art px when full
STATES:
Cell 1: empty red cloth sack lying flat and wrinkled on the floor
Cell 2: the same sack one third full, a few round lumps
Cell 3: the same sack two thirds full, standing up
Cell 4: the same sack completely full and round, tied with a gold cord, small sparkles
```

### Objeto · garland · 2 estados

Archivo: `garland.png`

Adjuntar:
- `palette.png`
- `plate_taller_master.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.

SUBJECT: garland for El taller del Mago (above the window, blink at 2 fps). 
STATES:
Cell 1: a short garland of green leaves with red bows and warm string lights, lights off, drawn horizontally to hang above a window
Cell 2: same garland, lights on
Cell 3: leave empty (plain magenta)
Cell 4: leave empty (plain magenta)
```

### Objetos · stool, fan, mate, xmas_tree

Archivo: `objects_taller_1.png`

Adjuntar:
- `palette.png`
- `plate_taller_master.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 4x4 grid of equal 256x256 cells. Each ROW is one animation of up to 4 frames, read left to right; unused cells stay plain magenta. Every subject is centred in its cell, keeps the same size along its row and fits inside 128x128 image pixels.

ROWS:
Row 1 (stool, seat for guests (separate so a sitting character can overlap it)): frame 1: simple round wooden stool with three legs
Row 2 (fan, summer heat gag, ambient loop): frame 1: small blue electric floor fan, blades at angle 0 with motion lines | frame 2: blades rotated 30 degrees | frame 3: blades rotated 60 degrees
Row 3 (mate, the wizard's mate when it is not in his hand): frame 1: a mate gourd (brown, rounded) with a silver metal straw, standalone
Row 4 (xmas_tree, corner decoration, blink at 2 fps): frame 1: tiny potted Christmas tree in a terracotta pot, red and gold baubles, lights off | frame 2: same tree, lights on (warm yellow dots)
```

### Objetos · wreath

Archivo: `objects_taller_2.png`

Adjuntar:
- `palette.png`
- `plate_taller_master.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 4x4 grid of equal 256x256 cells. Each ROW is one animation of up to 4 frames, read left to right; unused cells stay plain magenta. Every subject is centred in its cell, keeps the same size along its row and fits inside 128x128 image pixels.

ROWS:
Row 1 (wreath, on the door): frame 1: small Christmas wreath with a red bow, to hang on a door
Row 2: leave empty
Row 3: leave empty
Row 4: leave empty
```

### Efectos · fx_sparkle, fx_puff, fx_confetti, fx_hearts

Archivo: `fx_1.png`

Adjuntar:
- `palette.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 4x4 grid of equal 256x256 cells. Each ROW is one animation of up to 4 frames, read left to right; unused cells stay plain magenta. Every subject is centred in its cell, keeps the same size along its row and fits inside 128x128 image pixels.

ROWS:
Row 1 (fx_sparkle, anything appearing or shining): frame 1: tiny 4-point star, pale yellow #FFF3B0 | frame 2: bigger 4-point star with gold edge #F2B640 | frame 3: biggest star with 4 small dots around | frame 4: fading: small dots only
Row 2 (fx_puff, poof, landing, disappearing): frame 1: small round cream dust cloud | frame 2: bigger cloud, three bumps | frame 3: biggest cloud, breaking apart | frame 4: a few small dust dots
Row 3 (fx_confetti, celebration): frame 1: burst of small red, gold and green squares close together | frame 2: squares spreading out | frame 3: squares falling and spreading | frame 4: a few squares at the bottom
Row 4 (fx_hearts, love, gift received): frame 1: one small red pixel heart | frame 2: heart rising, a second smaller heart | frame 3: two hearts higher | frame 4: hearts fading
```

### Efectos · fx_sweat, fx_idea, fx_steam, fx_swirl

Archivo: `fx_2.png`

Adjuntar:
- `palette.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 4x4 grid of equal 256x256 cells. Each ROW is one animation of up to 4 frames, read left to right; unused cells stay plain magenta. Every subject is centred in its cell, keeps the same size along its row and fits inside 128x128 image pixels.

ROWS:
Row 1 (fx_sweat, heat, nerves): frame 1: one light blue sweat drop | frame 2: two drops flying outward | frame 3: three drops | frame 4: drops fading
Row 2 (fx_idea, eureka (no text)): frame 1: small yellow glow | frame 2: a glowing yellow light bulb with short rays | frame 3: bulb with long rays | frame 4: bulb with short rays
Row 3 (fx_steam, anger, heat): frame 1: small grey puff | frame 2: two puffs rising | frame 3: puffs bigger | frame 4: puffs fading
Row 4 (fx_swirl, confusion (instead of a question mark)): frame 1: small dark spiral | frame 2: spiral rotated | frame 3: spiral rotated again | frame 4: spiral rotated again
```

### Efectos · fx_moth, fx_magic_ring, fx_notes, fx_dust_motes

Archivo: `fx_3.png`

Adjuntar:
- `palette.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 4x4 grid of equal 256x256 cells. Each ROW is one animation of up to 4 frames, read left to right; unused cells stay plain magenta. Every subject is centred in its cell, keeps the same size along its row and fits inside 128x128 image pixels.

ROWS:
Row 1 (fx_moth, empty sack / empty wallet gag): frame 1: small grey moth, wings up | frame 2: small grey moth, wings down
Row 2 (fx_magic_ring, spells): frame 1: thin gold ring of sparkles, small | frame 2: ring bigger | frame 3: ring biggest, sparkles separating | frame 4: only sparkles
Row 3 (fx_notes, happy, music): frame 1: one small musical note | frame 2: two notes rising | frame 3: notes higher | frame 4: notes fading
Row 4 (fx_dust_motes, ambient sunbeam): frame 1: three tiny pale dots | frame 2: dots shifted
```

### Ítems · cafe, banana, suculenta, hamster

Archivo: `items_1.png`

Adjuntar:
- `palette.png`
- `assets/p/cafe.webp`
- `assets/p/banana.webp`
- `assets/p/suculenta.webp`
- `assets/p/hamster.webp`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells, one object per cell, each object at most 160x160 image pixels, centred and resting on an invisible baseline 176 image pixels above the bottom of its cell. All objects drawn at the same pixel scale.

SUBJECT: products of a small shop, as RPG inventory items.
Cell 1: takeaway coffee cup fidget clicker: white cup, black lid, brown sleeve (draw it from the attached photo of 'cafe', simplified to pixel art)
Cell 2: half-peeled yellow banana fidget clicker (draw it from the attached photo of 'banana', simplified to pixel art)
Cell 3: tiny green succulent in a small pot, fidget clicker (draw it from the attached photo of 'suculenta', simplified to pixel art)
Cell 4: little hamster peeking out of a cracked egg shell, fidget clicker (draw it from the attached photo of 'hamster', simplified to pixel art)
```

### Ítems · calavera, garaje, panal, plegable

Archivo: `items_2.png`

Adjuntar:
- `palette.png`
- `assets/p/calavera.webp`
- `assets/p/garaje.webp`
- `assets/p/panal.webp`
- `assets/p/plegable.webp`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells, one object per cell, each object at most 160x160 image pixels, centred and resting on an invisible baseline 176 image pixels above the bottom of its cell. All objects drawn at the same pixel scale.

SUBJECT: products of a small shop, as RPG inventory items.
Cell 1: small white skull keychain with a metal ring (draw it from the attached photo of 'calavera', simplified to pixel art)
Cell 2: black wall display grid holding six tiny colourful toy cars (2 columns x 3 rows) (draw it from the attached photo of 'garaje', simplified to pixel art)
Cell 3: black hexagon honeycomb wall display cells with two tiny toy cars (draw it from the attached photo of 'panal', simplified to pixel art)
Cell 4: wooden-coloured octagonal tube that is a travel chess set, slightly open with chess pieces inside (draw it from the attached photo of 'plegable', simplified to pixel art)
```

### Ítems · medieval, perros-gatos, domino, hoja

Archivo: `items_3.png`

Adjuntar:
- `palette.png`
- `assets/p/medieval.webp`
- `assets/p/perros-gatos.webp`
- `assets/p/domino.webp`
- `assets/p/hoja.webp`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells, one object per cell, each object at most 160x160 image pixels, centred and resting on an invisible baseline 176 image pixels above the bottom of its cell. All objects drawn at the same pixel scale.

SUBJECT: products of a small shop, as RPG inventory items.
Cell 1: medieval chess knight and castle tower pieces, grey stone colour (draw it from the attached photo of 'medieval', simplified to pixel art)
Cell 2: two chess pieces: a cat king and a dog king (draw it from the attached photo of 'perros-gatos', simplified to pixel art)
Cell 3: a small white box with domino tiles stacked beside it (draw it from the attached photo of 'domino', simplified to pixel art)
Cell 4: white leaf-shaped hanging bird feeder, a curved leaf with veins (draw it from the attached photo of 'hoja', simplified to pixel art)
```

### Ítems · driftwood, maceta, bowl, cassette

Archivo: `items_4.png`

Adjuntar:
- `palette.png`
- `assets/p/driftwood.webp`
- `assets/p/maceta.webp`
- `assets/p/bowl.webp`
- `assets/p/cassette.webp`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells, one object per cell, each object at most 160x160 image pixels, centred and resting on an invisible baseline 176 image pixels above the bottom of its cell. All objects drawn at the same pixel scale.

SUBJECT: products of a small shop, as RPG inventory items.
Cell 1: rustic birdhouse that looks like driftwood planks, round hole (draw it from the attached photo of 'driftwood', simplified to pixel art)
Cell 2: quilted gold planter that looks like padded fabric (draw it from the attached photo of 'maceta', simplified to pixel art)
Cell 3: melted-looking bowl for keys, dripping edges (draw it from the attached photo of 'bowl', simplified to pixel art)
Cell 4: giant retro cassette tape (draw it from the attached photo of 'cassette', simplified to pixel art)
```

### Ítems · creeper, tnt, pokebox, dragon

Archivo: `items_5.png`

Adjuntar:
- `palette.png`
- `assets/p/creeper.webp`
- `assets/p/tnt.webp`
- `assets/p/pokebox.webp`
- `assets/p/dragon.webp`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells, one object per cell, each object at most 160x160 image pixels, centred and resting on an invisible baseline 176 image pixels above the bottom of its cell. All objects drawn at the same pixel scale.

SUBJECT: products of a small shop, as RPG inventory items.
Cell 1: green Creeper-style money box: a green pixel cube head with a dark face, coin slot on top (draw it from the attached photo of 'creeper', simplified to pixel art)
Cell 2: TNT block: red block with a white band (no letters, just a plain white band) and a fuse on top (draw it from the attached photo of 'tnt', simplified to pixel art)
Cell 3: card box shaped like a grey retro handheld console with a little screen and buttons (no logo) (draw it from the attached photo of 'pokebox', simplified to pixel art)
Cell 4: articulated black dragon with purple eyes and big wings, End-dragon style (draw it from the attached photo of 'dragon', simplified to pixel art)
```

### Ítems · f40, penarol, nacional, repisa

Archivo: `items_6.png`

Adjuntar:
- `palette.png`
- `assets/p/f40.webp`
- `assets/p/penarol.webp`
- `assets/p/nacional.webp`
- `assets/p/repisa.webp`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells, one object per cell, each object at most 160x160 image pixels, centred and resting on an invisible baseline 176 image pixels above the bottom of its cell. All objects drawn at the same pixel scale.

SUBJECT: products of a small shop, as RPG inventory items.
Cell 1: red 1980s Italian sports car model kit, low wedge shape, pop-up headlights (draw it from the attached photo of 'f40', simplified to pixel art)
Cell 2: football stadium model with yellow and black stands (draw it from the attached photo of 'penarol', simplified to pixel art)
Cell 3: football stadium model with white, blue and red stands (draw it from the attached photo of 'nacional', simplified to pixel art)
Cell 4: melted-looking wall shelf that seems to drip (draw it from the attached photo of 'repisa', simplified to pixel art)
```

### Ítems · mesa-luz

Archivo: `items_7.png`

Adjuntar:
- `palette.png`
- `assets/p/mesa-luz.webp`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells, one object per cell, each object at most 160x160 image pixels, centred and resting on an invisible baseline 176 image pixels above the bottom of its cell. All objects drawn at the same pixel scale.

SUBJECT: products of a small shop, as RPG inventory items.
Cell 1: bedside organizer that holds an open book, with small drawers (draw it from the attached photo of 'mesa-luz', simplified to pixel art)
Cell 2: leave empty (plain magenta)
Cell 3: leave empty (plain magenta)
Cell 4: leave empty (plain magenta)
```
