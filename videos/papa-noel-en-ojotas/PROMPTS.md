# Prompts para Gemini

Generado por `videos/biblioteca/tools/gen_prompts.py`. No editar a mano: cambiar el JSON y regenerar.
Orden = orden de aprobación (ver `videos/biblioteca/ESTILO.md`, sección 8). Cada imagen aprobada se guarda con el nombre indicado y se adjunta en los prompts siguientes.

## Gate 1 · Paleta

`palette.png` ya está generada (32 colores). No hace falta pedirla.

## Gate 2 · Model sheets de los personajes

### El Mago: model sheet (gate 2)

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

### Papá Noel de verano: model sheet (gate 2)

Archivo: `papa_noel_model.png`

Adjuntar:
- `palette.png`
- `mago_model.png (referencia de estilo y escala)`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 368 image pixels (92 art pixels).

SUBJECT: Papá Noel de verano, a jolly, round Santa Claus dressed for a very hot Uruguayan summer: big white beard, rosy sunburned cheeks, a red Santa hat with a white pompom, small round sunglasses, a white sleeveless undershirt, his red Santa jacket tied around the waist by the sleeves, red shorts with white fur trim, black flip-flops (ojotas) and bare legs. Same chibi proportions as the attached wizard (head about one third of the height), slightly taller and wider than him. Colours: reds #7A1E22 #C0392B #E86A4A, whites #FBF4E4 #E9D8B4, skin #F0C090 #E1AE73 #D9826A, outline #150A34.

MODEL SHEET:
Cell 1: front three-quarter view facing the camera (S), standing, hands on the belly
Cell 2: side view facing LEFT (W), standing
Cell 3: back view (N), standing
Cell 4: front view (S) sitting on an invisible stool, hands on the knees
```

## Gate 3 y 4 · Escenario

### Taller · imagen maestra (gate 3)

Archivo: `plate_taller_master.png`

Adjuntar:
- `palette.png`
- `mago_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

FORMAT: 9:16 vertical PNG, the whole scene is 270x480 art pixels (each art pixel a 4x4 block).

SCENE: the cosy one-room workshop of a wizard who makes 3D printed things, seen from a top-down three-quarter view like a 1990s farming RPG interior. Back wall: warm honey-coloured wooden planks; in the centre a square window with a summer blue sky, a bright sun and the green leafy branch of a plane tree; on the left half of the back wall two wooden shelves with small colourful 3D printed objects and four spools of filament (red, blue, gold, green). Against the back wall on the left: a sturdy wooden workbench (no printer on it, the printer is a separate sprite). Right side wall: a wooden door (closed) with a small brass knob, the door is a separate sprite so leave a door-shaped dark frame. Floor: warm wooden boards running left-right, a round woven rug in the centre, a small empty patch near the door for a stool. Bottom edge: a strip of terracotta and cream checkered tiles. Bright summer daylight coming from the window (upper-left light). Nothing on the floor, no characters, no animals, no furniture other than the shelves and the workbench. Christmas decorations (they will be separate sprites, so just suggest them lightly): a garland with lights above the window, a tiny Christmas tree in the back-right corner, a wreath on the door.
For scale only: El Mago (attached model sheet) stands at the workbench, 96 art pixels tall.
```

### Taller · fondo vacío (gate 4)

Archivo: `plate_taller.png`

Adjuntar:
- `plate_taller_master.png`

```
Same image, same camera, same pixel grid, same palette and light. Remove the wizard and any seasonal decoration. Keep only the empty room exactly as it is. Fill the hidden areas naturally. 9:16 PNG.
```

## Gate 5 · Animaciones de los personajes

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

### El Mago · sip_mate_S · 6 cuadros · once · P0 (hoja 1/2)

Archivo: `mago_sip_mate_S_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`
- `mate.png (si ya existe)`

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
- `mate.png (si ya existe)`

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
ACTION: surprised_S (something unexpected happens), facing the camera in a front three-quarter view, frames 1-4 of 4, played once.
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
ACTION: idea_S (eureka moment (add fx_idea above the head)), facing the camera in a front three-quarter view, frames 1-4 of 4, played once.
Cell 1: thinking pose, hand on beard
Cell 2: eyes snap wide open, back straightens
Cell 3: right index finger raised high, big smile
Cell 4: same pose, eyes sparkling (hold)
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
ACTION: item_get_S (RPG 'item get' reveal; the item sprite is placed above the hands), facing the camera in a front three-quarter view, frames 1-4 of 4, played once.
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

### El Mago · offer_mate_E · 3 cuadros · hold · P0

Archivo: `mago_offer_mate_E_1.png`

Adjuntar:
- `palette.png`
- `mago_model.png`
- `mate.png (si ya existe)`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 384 image pixels.

SUBJECT: El Mago exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: offer_mate_E (offering mate to a guest), seen from the side, facing RIGHT, frames 1-3 of 3, played once.
Cell 1: side view, holding the mate gourd at the chest with the right hand
Cell 2: extending the arm forward
Cell 3: arm fully extended offering the gourd to the right, friendly smile
Cell 4: leave empty (plain magenta)
```

### Papá Noel de verano · walk_hot_W · 6 cuadros · loop · P0 (hoja 1/2)

Archivo: `papa_noel_walk_hot_W_1.png`

Adjuntar:
- `palette.png`
- `papa_noel_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 368 image pixels.

SUBJECT: Papá Noel de verano exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: walk_hot_W (stumbles in from the door, exhausted by the heat), seen from the side, facing LEFT, frames 1-4 of 6, looping.
Cell 1: side view facing LEFT, dragging the right flip-flop forward, tongue out, sweating, shoulders slumped
Cell 2: body low, knees bent, arms hanging
Cell 3: passing pose, body up, sunglasses sliding down the nose
Cell 4: dragging the left flip-flop forward
```

### Papá Noel de verano · walk_hot_W · 6 cuadros · loop · P0 (hoja 2/2)

Archivo: `papa_noel_walk_hot_W_2.png`

Adjuntar:
- `palette.png`
- `papa_noel_model.png`
- `papa_noel_walk_hot_W_1.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 368 image pixels.

SUBJECT: Papá Noel de verano exactly as in the attached model sheet (same face, colours, proportions and size). This sheet continues the attached first sheet of the same animation: keep exactly the same size, position and baseline.
ACTION: walk_hot_W (stumbles in from the door, exhausted by the heat), seen from the side, facing LEFT, frames 5-6 of 6, looping.
Cell 1: body low, arms hanging
Cell 2: passing pose, body up
Cell 3: leave empty (plain magenta)
Cell 4: leave empty (plain magenta)
```

### Papá Noel de verano · sit_plop_S · 4 cuadros · once · P0

Archivo: `papa_noel_sit_plop_S_1.png`

Adjuntar:
- `palette.png`
- `papa_noel_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 368 image pixels.

SUBJECT: Papá Noel de verano exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: sit_plop_S (drops onto the stool), facing the camera in a front three-quarter view, frames 1-4 of 4, played once.
Cell 1: standing in front of a stool, knees giving way
Cell 2: falling backwards, arms up
Cell 3: landing sitting on the stool (stool drawn separately), body squashed, belly bouncing
Cell 4: sitting slumped, legs stretched out
```

### Papá Noel de verano · fan_hot_S · 4 cuadros · loop · P0

Archivo: `papa_noel_fan_hot_S_1.png`

Adjuntar:
- `palette.png`
- `papa_noel_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 368 image pixels.

SUBJECT: Papá Noel de verano exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: fan_hot_S (sitting and fanning himself, sweat (add fx_sweat)), facing the camera in a front three-quarter view, frames 1-4 of 4, looping.
Cell 1: sitting, holding his Santa hat in the right hand fanning his face, eyes closed, mouth open panting
Cell 2: hat moved to the left of the face
Cell 3: hat in front of the face
Cell 4: hat moved to the right
```

### Papá Noel de verano · sip_mate_S · 4 cuadros · once · P0

Archivo: `papa_noel_sip_mate_S_1.png`

Adjuntar:
- `palette.png`
- `papa_noel_model.png`
- `mate.png (si ya existe)`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 368 image pixels.

SUBJECT: Papá Noel de verano exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: sip_mate_S (takes the mate the wizard offers), facing the camera in a front three-quarter view, frames 1-4 of 4, played once.
Cell 1: sitting, holding a mate gourd with both hands at the chest, surprised
Cell 2: lifting the gourd to the beard
Cell 3: sipping, eyes closed, cheeks puffed
Cell 4: lowering the gourd, eyes wide open, refreshed
```

### Papá Noel de verano · refreshed_S · 4 cuadros · hold · P0

Archivo: `papa_noel_refreshed_S_1.png`

Adjuntar:
- `palette.png`
- `papa_noel_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 368 image pixels.

SUBJECT: Papá Noel de verano exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: refreshed_S (relief after the mate), facing the camera in a front three-quarter view, frames 1-4 of 4, played once.
Cell 1: sitting, long sigh of relief, shoulders dropping
Cell 2: big smile, eyes closed
Cell 3: sitting upright, happy, sunglasses back on, giving the mate back with an extended right arm
Cell 4: same pose (hold)
```

### Papá Noel de verano · sack_shake_S · 4 cuadros · once · P0

Archivo: `papa_noel_sack_shake_S_1.png`

Adjuntar:
- `palette.png`
- `papa_noel_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 368 image pixels.

SUBJECT: Papá Noel de verano exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: sack_shake_S (nothing left in the sack (sack is part of this sprite; add fx_moth)), facing the camera in a front three-quarter view, frames 1-4 of 4, played once.
Cell 1: standing, holding an empty red sack upside down with both hands above his head
Cell 2: shaking it, sack to the left
Cell 3: shaking it, sack to the right
Cell 4: looking into the empty sack, puzzled
```

### Papá Noel de verano · sad_S · 4 cuadros · hold · P0

Archivo: `papa_noel_sad_S_1.png`

Adjuntar:
- `palette.png`
- `papa_noel_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 368 image pixels.

SUBJECT: Papá Noel de verano exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: sad_S (no gifts to deliver), facing the camera in a front three-quarter view, frames 1-4 of 4, played once.
Cell 1: sitting, empty sack on his lap
Cell 2: shoulders dropping
Cell 3: head down, hat drooping, mouth turned down
Cell 4: same, one tear (hold)
```

### Papá Noel de verano · joy_jump_S · 6 cuadros · once · P0 (hoja 1/2)

Archivo: `papa_noel_joy_jump_S_1.png`

Adjuntar:
- `palette.png`
- `papa_noel_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 368 image pixels.

SUBJECT: Papá Noel de verano exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: joy_jump_S (celebration when the sack is full), facing the camera in a front three-quarter view, frames 1-4 of 6, played once.
Cell 1: crouching, fists at the chest, huge smile
Cell 2: taking off, fists up
Cell 3: apex, arms up, beard and hat flying
Cell 4: falling
```

### Papá Noel de verano · joy_jump_S · 6 cuadros · once · P0 (hoja 2/2)

Archivo: `papa_noel_joy_jump_S_2.png`

Adjuntar:
- `palette.png`
- `papa_noel_model.png`
- `papa_noel_joy_jump_S_1.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 368 image pixels.

SUBJECT: Papá Noel de verano exactly as in the attached model sheet (same face, colours, proportions and size). This sheet continues the attached first sheet of the same animation: keep exactly the same size, position and baseline.
ACTION: joy_jump_S (celebration when the sack is full), facing the camera in a front three-quarter view, frames 5-6 of 6, played once.
Cell 1: landing squash
Cell 2: recover, arms up wide, laughing
Cell 3: leave empty (plain magenta)
Cell 4: leave empty (plain magenta)
```

### Papá Noel de verano · sack_shoulder_S · 4 cuadros · once · P0

Archivo: `papa_noel_sack_shoulder_S_1.png`

Adjuntar:
- `palette.png`
- `papa_noel_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 368 image pixels.

SUBJECT: Papá Noel de verano exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: sack_shoulder_S (lifts the full sack), facing the camera in a front three-quarter view, frames 1-4 of 4, played once.
Cell 1: standing next to a full round red sack on the floor (sack drawn in this sprite)
Cell 2: bending, grabbing the sack
Cell 3: swinging the sack up
Cell 4: full sack on the right shoulder, proud grin
```

### Papá Noel de verano · walk_sack_E · 6 cuadros · loop · P0 (hoja 1/2)

Archivo: `papa_noel_walk_sack_E_1.png`

Adjuntar:
- `palette.png`
- `papa_noel_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 368 image pixels.

SUBJECT: Papá Noel de verano exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: walk_sack_E (leaves through the door with the sack), seen from the side, facing RIGHT, frames 1-4 of 6, looping.
Cell 1: side view facing RIGHT, full red sack on the shoulder, right flip-flop forward, happy
Cell 2: body low
Cell 3: passing, body up
Cell 4: left flip-flop forward
```

### Papá Noel de verano · walk_sack_E · 6 cuadros · loop · P0 (hoja 2/2)

Archivo: `papa_noel_walk_sack_E_2.png`

Adjuntar:
- `palette.png`
- `papa_noel_model.png`
- `papa_noel_walk_sack_E_1.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 368 image pixels.

SUBJECT: Papá Noel de verano exactly as in the attached model sheet (same face, colours, proportions and size). This sheet continues the attached first sheet of the same animation: keep exactly the same size, position and baseline.
ACTION: walk_sack_E (leaves through the door with the sack), seen from the side, facing RIGHT, frames 5-6 of 6, looping.
Cell 1: body low
Cell 2: passing, body up
Cell 3: leave empty (plain magenta)
Cell 4: leave empty (plain magenta)
```

### Papá Noel de verano · wave_S · 4 cuadros · loop · P0

Archivo: `papa_noel_wave_S_1.png`

Adjuntar:
- `palette.png`
- `papa_noel_model.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.
Standing height: 368 image pixels.

SUBJECT: Papá Noel de verano exactly as in the attached model sheet (same face, colours, proportions and size).
ACTION: wave_S (goodbye from the door), facing the camera in a front three-quarter view, frames 1-4 of 4, looping.
Cell 1: standing, full sack on the left shoulder, right hand raised waving, big smile
Cell 2: hand tilted out
Cell 3: hand raised
Cell 4: hand tilted in
```

## Gate 5 · Objetos y efectos

### Objeto · printer · 4 estados · P0

Archivo: `printer.png`

Adjuntar:
- `palette.png`
- `plate_taller_master.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.

SUBJECT: printer for the wizard's workshop (the shop's printer; frames 2-3 loop while printing). about 52x44 art px, base anchored at the bottom centre of the cell
STATES:
Cell 1: idle: compact desktop 3D printer, open frame with one upright gantry on the left side and a moving bed, light grey and charcoal, small screen on the front, a gold filament spool on top, no logo
Cell 2: printing: the nozzle carriage at the left, the bed pushed back, a tiny orange glow at the nozzle
Cell 3: printing: the nozzle carriage at the right, the bed pulled forward, tiny orange glow
Cell 4: done: nozzle parked, a small green light on the screen, a soft gold sparkle above the empty bed
```

### Objeto · door_R · 3 estados · P0

Archivo: `door_R.png`

Adjuntar:
- `palette.png`
- `plate_taller_master.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.

SUBJECT: door R for the wizard's workshop (people come in and out). about 34x80 art px
STATES:
Cell 1: closed wooden door on a right-hand side wall seen in three-quarter view, brass knob
Cell 2: door ajar, a thin slice of bright sunlight
Cell 3: door wide open, swung inward, a rectangle of bright summer sunlight on the floor
Cell 4: leave empty (plain magenta)
```

### Objeto · sack · 4 estados · P0

Archivo: `sack.png`

Adjuntar:
- `palette.png`
- `plate_taller_master.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.

SUBJECT: sack for the wizard's workshop (Santa's sack filling up). about 44x48 art px when full
STATES:
Cell 1: empty red cloth sack lying flat and wrinkled on the floor
Cell 2: the same sack one third full, a few round lumps
Cell 3: the same sack two thirds full, standing up
Cell 4: the same sack completely full and round, tied with a gold cord, small sparkles
```

### Objeto · garland · 2 estados · P0

Archivo: `garland.png`

Adjuntar:
- `palette.png`
- `plate_taller_master.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the cell, horizontally centred.

SUBJECT: garland for the wizard's workshop (above the window, blink at 2 fps). 
STATES:
Cell 1: a short garland of green leaves with red bows and warm string lights, lights off, drawn horizontally to hang above a window
Cell 2: same garland, lights on
Cell 3: leave empty (plain magenta)
Cell 4: leave empty (plain magenta)
```

### Objeto · stool, fan, mate, xmas_tree

Archivo: `objects_1.png`

Adjuntar:
- `palette.png`
- `plate_taller_master.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no grid lines, no borders. A 4x4 grid of equal 256x256 cells. Each ROW is one animation of up to 4 frames, read left to right; unused cells stay plain magenta. Every subject is centred in its cell and stays the same size across its row; each subject fits inside 128x128 image pixels.

ROWS:
Row 1 (stool, seat for guests (separate so a sitting character can overlap it)): frame 1: simple round wooden stool with three legs
Row 2 (fan, summer heat gag, ambient loop): frame 1: small blue electric floor fan, blades at angle 0 with motion lines | frame 2: blades rotated 30 degrees | frame 3: blades rotated 60 degrees
Row 3 (mate, the wizard's mate when it is not in his hand): frame 1: a mate gourd (brown, rounded) with a silver metal straw, standalone
Row 4 (xmas_tree, corner decoration, blink at 2 fps): frame 1: tiny potted Christmas tree in a terracotta pot, red and gold baubles, lights off | frame 2: same tree, lights on (warm yellow dots)
```

### Objeto · wreath

Archivo: `objects_2.png`

Adjuntar:
- `palette.png`
- `plate_taller_master.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no grid lines, no borders. A 4x4 grid of equal 256x256 cells. Each ROW is one animation of up to 4 frames, read left to right; unused cells stay plain magenta. Every subject is centred in its cell and stays the same size across its row; each subject fits inside 128x128 image pixels.

ROWS:
Row 1 (wreath, on the door): frame 1: small Christmas wreath with a red bow, to hang on a door
Row 2: leave empty
Row 3: leave empty
Row 4: leave empty
```

### FX · fx_sparkle, fx_puff, fx_confetti, fx_hearts

Archivo: `fx_1.png`

Adjuntar:
- `palette.png`
- `plate_taller_master.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no grid lines, no borders. A 4x4 grid of equal 256x256 cells. Each ROW is one animation of up to 4 frames, read left to right; unused cells stay plain magenta. Every subject is centred in its cell and stays the same size across its row; each subject fits inside 128x128 image pixels.

ROWS:
Row 1 (fx_sparkle, anything appearing or shining): frame 1: tiny 4-point star, pale yellow #FFF3B0 | frame 2: bigger 4-point star with gold edge #F2B640 | frame 3: biggest star with 4 small dots around | frame 4: fading: small dots only
Row 2 (fx_puff, poof, landing, disappearing): frame 1: small round cream dust cloud | frame 2: bigger cloud, three bumps | frame 3: biggest cloud, breaking apart | frame 4: a few small dust dots
Row 3 (fx_confetti, celebration): frame 1: burst of small red, gold and green squares close together | frame 2: squares spreading out | frame 3: squares falling and spreading | frame 4: a few squares at the bottom
Row 4 (fx_hearts, love, gift received): frame 1: one small red pixel heart | frame 2: heart rising, a second smaller heart | frame 3: two hearts higher | frame 4: hearts fading
```

### FX · fx_sweat, fx_idea, fx_moth

Archivo: `fx_2.png`

Adjuntar:
- `palette.png`
- `plate_taller_master.png`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no grid lines, no borders. A 4x4 grid of equal 256x256 cells. Each ROW is one animation of up to 4 frames, read left to right; unused cells stay plain magenta. Every subject is centred in its cell and stays the same size across its row; each subject fits inside 128x128 image pixels.

ROWS:
Row 1 (fx_sweat, heat, nerves): frame 1: one light blue sweat drop | frame 2: two drops flying outward | frame 3: three drops | frame 4: drops fading
Row 2 (fx_idea, eureka (no text)): frame 1: small yellow glow | frame 2: a glowing yellow light bulb with short rays | frame 3: bulb with long rays | frame 4: bulb with short rays
Row 3 (fx_moth, empty sack / empty wallet gag): frame 1: small grey moth, wings up | frame 2: small grey moth, wings down
Row 4: leave empty
```

## Gate 5 · Ítems del catálogo

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

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no grid lines, no borders. A 2x2 grid of equal 512x512 cells, one object per cell, each object at most 160x160 image pixels (40x40 art pixels), centred, resting on an invisible baseline 128 image pixels above the bottom of the cell. All four objects drawn at the same pixel scale.

SUBJECT: 3D printed products from a small shop, as RPG inventory items.
Cell 1: takeaway coffee cup fidget clicker: white cup, black lid, brown sleeve (draw it from the attached photo of 'cafe', simplified to pixel art)
Cell 2: half-peeled yellow banana fidget clicker (draw it from the attached photo of 'banana', simplified to pixel art)
Cell 3: tiny green succulent in a small pot, fidget clicker (draw it from the attached photo of 'suculenta', simplified to pixel art)
Cell 4: little hamster peeking out of a cracked egg shell, fidget clicker (draw it from the attached photo of 'hamster', simplified to pixel art)
```

### Ítems · calavera, garaje, plegable, hoja

Archivo: `items_2.png`

Adjuntar:
- `palette.png`
- `assets/p/calavera.webp`
- `assets/p/garaje.webp`
- `assets/p/plegable.webp`
- `assets/p/hoja.webp`

```
STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.

SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, no grid lines, no borders. A 2x2 grid of equal 512x512 cells, one object per cell, each object at most 160x160 image pixels (40x40 art pixels), centred, resting on an invisible baseline 128 image pixels above the bottom of the cell. All four objects drawn at the same pixel scale.

SUBJECT: 3D printed products from a small shop, as RPG inventory items.
Cell 1: small white skull keychain with a metal ring (draw it from the attached photo of 'calavera', simplified to pixel art)
Cell 2: black wall display grid holding six tiny colourful toy cars (2 columns x 3 rows) (draw it from the attached photo of 'garaje', simplified to pixel art)
Cell 3: wooden-coloured octagonal tube that is a travel chess set, slightly open with chess pieces inside (draw it from the attached photo of 'plegable', simplified to pixel art)
Cell 4: white leaf-shaped hanging bird feeder, a curved leaf with veins (draw it from the attached photo of 'hoja', simplified to pixel art)
```
