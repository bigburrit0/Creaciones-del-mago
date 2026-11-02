# Formato de los manifiestos

## `biblioteca/sprites.json`

```json
{
  "project": {
    "name": "Mi marca",
    "scale_reference": "mascota",
    "style": { "palette": ["#150A34", "..."], "outline": "#150A34",
               "view": "top-down three-quarter view like a 1990s farming RPG",
               "light": "upper-left, shadows fall to the lower-right", "extra": "" }
  },
  "grid": { "art_canvas": [270, 480], "scale": 4, "video": [1080, 1920], "fps_video": 30 },
  "sheet_formats": { },
  "characters": {
    "mascota": {
      "model": { "name": "La Mascota", "height_px": 96,
                 "description": "aspecto completo, ropa, proporciones y colores en hex",
                 "cells": ["front view (S) standing", "side view facing right (E)", "back view (N)", "pose característica"] },
      "placeholder": { "body": "#4B3A8E", "hat": "#4B3A8E", "beard": null, "skin": "#F0C090" },
      "animations": [
        { "id": "walk_E", "group": "locomotion", "dir": "E", "mode": "loop", "fps": 8,
          "mirror_to_W": true, "priority": "P0", "holds": null, "use": "cruzar de izquierda a derecha",
          "poses": ["contacto pie derecho", "abajo", "paso, arriba", "contacto pie izquierdo", "abajo", "paso, arriba"] }
      ]
    }
  },
  "sets": {
    "taller": {
      "name": "El taller",
      "plate": { "id": "plate_taller", "description": "escena completa en palabras, sin personajes",
                 "anchors_art": { "puerta": [238, 262], "mesa": [80, 240] } },
      "objects": [ { "id": "door_R", "format": "char", "mode": "states", "fps": 8, "priority": "P0",
                     "use": "entradas y salidas", "description": "~34x80 px de arte",
                     "poses": ["cerrada", "entreabierta", "abierta"] } ],
      "seasonal_overlays": { "navidad": [ { "id": "xmas_tree", "format": "small", "mode": "loop", "fps": 2,
                                             "poses": ["luces apagadas", "luces prendidas"], "use": "rincón" } ] }
    }
  },
  "fx": [ { "id": "fx_sparkle", "format": "small", "mode": "once", "fps": 12, "use": "aparecer",
            "poses": ["estrella chica", "grande", "más grande con puntos", "se apaga"] } ],
  "items": { "format": "item", "photos_dir": "fotos/<id>.jpg",
             "list": [ { "id": "taza", "description": "taza blanca con tapa negra" } ] }
}
```

- `group` (para el catálogo): `locomotion`, `idle`, `emotion`, `work`, `magic`, `social`, `sitting` o `reel`.
- `dir`: `S`, `E`, `N`, `W` o `S>N` (giro).
- `mode`: `loop` (bucle), `once` (una vez), `hold` (queda en el último), `states` (estados que se eligen a mano) o `static` (fijo).
- `holds`: id de un objeto que la animación lleva en la mano (se agrega como adjunto si ya existe).
- `placeholder`: solo colores para el animatic. Los que no se pongan usan los del ejemplo.
- `format` de los objetos: `char` (2×2, 128 px de arte) o `small` (filas en 4×4, 64 px de arte).
- `priority`: P0 (lo usa el reel actual), P1, P2. Sirve para ordenar qué se pide primero.

Las hojas reciben nombres estables que nunca dependen del reel:
- `<char>_model.png`
- `<char>_<anim>_<parte>.png`
- `plate_<set>_master.png` y `plate_<set>.png`
- `<objeto>.png` (formato `char`)
- `objects_<set>_<n>.png` (objetos chicos de a 4, en el orden del manifiesto)
- `fx_<n>.png` y `items_<n>.png` (de a 4, en el orden del manifiesto)

Agregar elementos **al final** de las listas de efectos e ítems, para no correr las hojas ya aprobadas.

## `<reel>/reel.json`

```json
{
  "id": "mi-reel", "duration": 15, "set": "taller",
  "decorations": "adornos de temporada sugeridos en la imagen maestra",
  "characters": { "invitado": { "model": {}, "placeholder": {}, "animations": [] } },
  "uses": { "mascota": ["walk_E", "idle_S"], "objects": ["door_R"], "fx": ["fx_sparkle"], "items": ["taza"] },
  "positions_art": { "puerta": [238, 262] },
  "beats": [ { "t": [0.0, 0.25], "mascota": "press_button_N", "door_R": "se abre de golpe" } ]
}
```

Los personajes del reel se usan completos. Si van a volver a aparecer, se pasan a la biblioteca.

## Atlas (salida del recorte)

`hf/assets/pr/atlas.json` (y `atlas.js`, que define `window.PR_ATLAS`):

```json
{ "scale": 4,
  "sprites": { "mascota.walk_E": { "file": "sprites/mascota/walk_E.png", "frames": 6, "w": 128, "h": 128,
                                   "ax": 64, "ay": 124, "fps": 8, "mode": "loop", "mirror": true } },
  "plates": { "taller": "plates/taller.png", "taller_master": "plates/taller_master.png" } }
```

Claves: `<char>.<anim>`, `<char>.model` (los 4 cuadros del model sheet), `obj.<id>`, `fx.<id>` e `item.<id>`.
