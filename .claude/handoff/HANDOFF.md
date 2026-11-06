# Traspaso — Creaciones del Mago: reel de Navidad "Papá Noel en ojotas" — actualizado 2026-11-06

## Próximo paso exacto
**Estado 2026-11-06 (tarde):** tanda 5 v2 importada y aprobada completa (8 hojas, originales en `recibidas/tanda5/`). Ensamblado y render de avance: `videos/papa-noel-en-ojotas/avance-1.mp4` (fondo, objetos y Papá Noel reales; Mago a medias; ítems y efectos provisorios). Posiciones de `hf/index.html` re-medidas sobre el fondo real (P.door/seat/sack/offer, árbol, corona); el sprite `door_R` NO se usa (la puerta del fondo es grande y en perspectiva): entrada y salida con polvo. Falta del usuario: resto de la tanda 3 (11 animaciones del Mago, fx_1..3, items_1/2/3/5/6) + segundas hojas `mago_sip_mate_S_2`, `mago_joy_jump_S_2` cuando sus partes 1 estén aprobadas. Después: re-ensamblar y render final `papa-noel-en-ojotas.mp4`.

**Estado 2026-11-06:** tanda 4 importada (originales en `videos/biblioteca/recibidas/tanda4/`). Aprobadas solas (gate 5): 11 animaciones de Papá Noel parte 1 (todas menos sad_S), printer, door_R, sack, garland, objects_taller_1, objects_taller_2. Revocada `papa_noel_sad_S_1` (camisa hawaiana, fuera de diseño). `plate_taller` aprobado v1 (2026-11-06). Revocadas además `papa_noel_sit_plop_S_1` y `papa_noel_startled_S_1` (banquito dibujado; borrado automático por color descartado: la madera clara del asiento tiene el tono de la piel). Enviada **tanda 5 v2** (8 paquetes, reemplaza a la tanda 5) con las correcciones; instrucciones para Gemini en `videos/papa-noel-en-ojotas/CORRECCIONES_GEMINI.md`. gen_prompts ahora agrega en todas las hojas la regla SUBJECT_ONLY (sin muebles, misma ropa del model sheet). Enviada **tanda 5** (zip regenerable con `--pack --only ...` y corrección agregada a mano al final del PROMPT.txt): mago_walk_E_2, mago_press_button_N_1 (corrección: sin mesa), papa_noel_walk_hot_W_2, papa_noel_sad_S_1 (corrección: ropa del model sheet), papa_noel_joy_jump_S_2, papa_noel_walk_sack_E_2. De la tanda 3 el usuario todavía no mandó el resto (11 animaciones del Mago, fx_1..3, items).
El usuario puede mandar imágenes como zip con nombres exactos (así llegó la tanda 4); su PC es Windows, no se puede conectar como carpeta.

Paso anterior (sigue valiendo):
Pedirle al usuario las imágenes que haya generado de las tandas 3 y 4. Guardar cada original en `videos/biblioteca/recibidas/<hoja>_vN.webp` y luego, convertidas a PNG con nombre `<hoja>_vN.png` en una carpeta temporal, importarlas:
`cd videos && python3 -I ../skills/pixel-reel/scripts/gemini_generate.py biblioteca/sprites.json --reel papa-noel-en-ojotas/reel.json --import <carpeta>`
Comprobar: gate 5 se aprueba solo si pasa QC (queda en `videos/biblioteca/sheets/`); gates 2-4 dejan `candidates/<hoja>/contact.png` para que el usuario elija (`--approve hoja.png=N`). Mirar SIEMPRE la hoja de contacto: el QC no detecta errores de contenido (ver "No repetir").

## Objetivo
Producir el reel de 15 s "Papá Noel en ojotas" (pixel art, 9:16) con la skill propia `skills/pixel-reel`, generando las hojas de sprites a mano en la app de Gemini (plan Google AI Pro del usuario) e importándolas. La biblioteca de sprites (El Mago, taller) se reutiliza en futuros reels.

## En curso (interrumpido)
- Gate 5 (animaciones, objetos, efectos, ítems) a medio generar. Aprobadas: `mago_walk_E_1`, `mago_idle_S_1`, `mago_turn_S_to_N_1`.
- `mago_press_button_N_1` revocada (borrada de sheets; motivo en `generation_log.jsonl`): Gemini dibujó la mesa dentro del sprite. Hay que volver a pedirla agregando al prompt: "Only the wizard, NO table or workbench in the sprite (the workbench is part of the background); his hands reach forward to an invisible printer at chest height."
- Gate 4 `plate_taller` (fondo vacío = maestra v3 sin arbolito, guirnalda ni corona) pendiente: paquete enviado al usuario en la tanda 4.
- Segundas hojas (`*_2`) de animaciones de 6 cuadros (walk_E, sip_mate_S, joy_jump_S del Mago; walk_hot_W, joy_jump_S, walk_sack_E de Papá Noel): se arman con `--pack` cuando la parte 1 está aprobada (llevan la parte 1 adjunta). `mago_walk_E_2` ya se puede empaquetar.

## Contexto que solo estaba en la conversación
- Gemini API: la clave está como **secreto de red** del entorno (encabezado `x-goog-api-key` para `generativelanguage.googleapis.com`; el proxy la inyecta, la variable `GEMINI_API_KEY` no existe y los scripts usan un relleno). Funciona para listar modelos, pero **el plan gratuito tiene cuota 0 para modelos de imagen** (`limit: 0`). El usuario NO quiere pagar API: usa la app de Gemini con su plan Pro y el modo `--pack` / `--import`.
- Paquetes enviados al usuario (zip, se regeneran con `--pack`): tanda 3 = 14 animaciones del Mago (parte 1) + fx_1..3 + items_1,2,3,5,6; tanda 4 = plate_taller + 12 animaciones de Papá Noel + printer, door_R, sack, garland, objects_taller_1/2. Con 2 variantes por hoja.
- Lo que devuelve la app de Gemini: PNG/WebP de 2000×2000, píxel de arte ≈10 px, celdas de ≈100 px de arte. `qc.normalize_sheet` lo convierte al formato canónico (1024, celdas de 128) al importar. A veces dibuja líneas de grilla (se borran solas).
- `ai.google.dev` está bloqueado por la red de la sesión (WebFetch y curl).

## Decisiones (no reabrir)
- Aprobados: Mago v1 (`mago_model.png`; el usuario primero dijo v3 y corrigió a v1), Papá Noel v1, taller maestra v3 (mesa vacía, sin impresora dibujada).
- Productos de Minecraft/Pokémon (Creeper, TNT, caja tipo Game Boy, dragón) SÍ van en el reel (pedido explícito); se piden sin logos ni texto.
- Gates 2-4 nunca se autoaprueban; gate 5 sí si pasa QC.
- Música: Jingle Bells (dominio público), arreglo chiptune propio en `videos/papa-noel-en-ojotas/cues.json`.
- Un reel = un escenario y una cámara; todo por piezas (no keyframes sueltos).

## No repetir
- Confiar solo en el puntaje del QC: `press_button_N` sacó 100 y traía una mesa dentro. Revisar `contact.png`.
- Llamar a la API para generar imágenes: cuota 0 en plan gratuito (el script ya corta sin reintentar).
- Importar con nombres que empiecen igual: ya corregido (regex exacta `<hoja>_vN`), pero nombrar bien los archivos.

## Pendientes en orden
1. Importar lo que traiga el usuario (tandas 3 y 4); revocar a mano lo que tenga contenido incorrecto.
2. Elegir con el usuario el fondo vacío (`plate_taller`, gate 4).
3. Re-empaquetar `mago_press_button_N_1` con la corrección, las segundas hojas `*_2` y lo que falle QC: `python3 -I ../skills/pixel-reel/scripts/gemini_generate.py biblioteca/sprites.json --reel papa-noel-en-ojotas/reel.json --variants 2 --pack <dir> --max-images 60` (filtrar lo ya enviado) y mandarlo como zip.
4. Con fondo vacío aprobado: medir de nuevo las anclas del taller y actualizar `sets.taller.plate.anchors_art` en `videos/biblioteca/sprites.json` y `P` en `videos/papa-noel-en-ojotas/hf/index.html` si cambian.
5. Ensamblar y renderizar con piezas reales + provisorias de respaldo (comandos abajo); revisar snapshots en cada beat.

## Preguntas abiertas para el usuario
- Qué hojas de las tandas 3 y 4 ya generó (y que nombre bien los archivos `<hoja>_vN`).

## Hecho en esta sesión
- Videos `videos/mate-power-up/` y `videos/mago-jardin/` (renderizados) → commiteados — verificado.
- Skill exportable `skills/pixel-reel/` (+ `skills/pixel-reel.skill`): gen_prompts, placeholders, slice_sheets, chiptune, assemble, qc (con normalize_sheet), gemini_generate (API, --pack, --import, --approve), gemini_check, runtime `assets/pixel-reel.js` → commiteado — verificado con pruebas.
- Biblioteca `videos/biblioteca/` (sprites.json con 48 animaciones del Mago, taller, 12 fx, 25 ítems) y reel `videos/papa-noel-en-ojotas/` (GUION.md, reel.json, cues.json, PROMPTS.md, hf/index.html, animatic.mp4) → commiteado.
- Aprobaciones de esta sesión e imágenes recibidas (`videos/biblioteca/recibidas/`, 12 webp originales) → ver cambios sin commitear.

## Mapa
- Leer si hace falta: `skills/pixel-reel/SKILL.md` (etapas y scripts); `skills/pixel-reel/references/gemini.md` (modo paquetes, QC, re-pedidos); `videos/papa-noel-en-ojotas/GUION.md` (beats); `videos/biblioteca/generation_log.jsonl` (historial de cada hoja).
- No hace falta releer: `videos/WORKFLOW.md`, `videos/biblioteca/ESTILO.md` (resumidos en la skill).
- Comandos (desde la raíz):
  - Provisorias: `python3 skills/pixel-reel/scripts/placeholders.py videos/biblioteca/sprites.json videos/papa-noel-en-ojotas/placeholder-sheets --reel videos/papa-noel-en-ojotas/reel.json`
  - Ensamblar: `python3 skills/pixel-reel/scripts/assemble.py videos/biblioteca/sprites.json videos/biblioteca/sheets:videos/papa-noel-en-ojotas/placeholder-sheets videos/papa-noel-en-ojotas/reel.json videos/papa-noel-en-ojotas/hf` (necesita `hf/assets/gsap.min.js`: `npm i gsap@3.15.0` y copiar `dist/gsap.min.js`; `pip install google-genai numpy pillow`)
  - Render: `cd videos/papa-noel-en-ojotas/hf && npx hyperframes render -o ../papa-noel-en-ojotas.mp4`
  - Reempaquetar skill: `python3 -m scripts.package_skill skills/pixel-reel skills` desde la skill `skill-creator`.
- Rama: `claude/pensive-johnson-l0jerg`. `videos/biblioteca/candidates/` está en .gitignore (se regenera importando desde `recibidas/`).
- Cambios sin commitear al escribir esto: generation_log.jsonl, recibidas/, 3 hojas nuevas en sheets/ (se commitean junto con este traspaso).

## Preferencias del usuario
- Español rioplatense, voseo. Respuestas concisas con recomendación clara.
- Quiere todo en pixel art 16 bits, armonioso, con animación cuidada; workflow reutilizable fuera del proyecto.
- Nunca pedir ni pegar claves en el chat. Repo público: nada de credenciales.
