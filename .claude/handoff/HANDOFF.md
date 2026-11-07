# Traspaso — Creaciones del Mago: reel de Navidad "Papá Noel en ojotas" — actualizado 2026-11-06

## Próximo paso exacto
**SIN GLITCHES NI FANTASMAS (2026-11-07):** el usuario vio "glitching" en los personajes y el mate atravesando los cuerpos al tomar; pidió que no pase NUNCA, con el equipo de investigación. Detalle en `videos/RESEARCH_3D_CONTACT.md`.
- Glitch: AnimationMixer no reescribe huesos sin cambio → dibujar el mismo t dos veces (HyperFrames lo hace) apilaba IK y rotaciones. Arreglado en `toon3d.js` (snapshot del pose puro de los clips, cada t se dibuja una vez), más pesos con ease, sin bind pose si no hay clip, IK sin NaN.
- Contacto: colisionadores por personaje (`addCollider`, incluido el ala del sombrero como disco), IK con objetivos y palma fuera de los cuerpos, pose de tomar mate (bombilla al bigote, mate delante de la barba), punto de pasaje del mate entre los dos, guardia de contacto en cada cuadro, lanzamiento por IK (el clip de hechizo atravesaba la barba).
- PUERTA DE CALIDAD obligatoria antes de renderizar: `node videos/biblioteca/3d/web/qa3d.cjs PUERTO informe.json` con `hf3d` servido por http (sale 1 si hay contacto, salto de pose o no determinismo). Resultado: 1020/1020 cuadros sin violaciones.

**REEL 3D TOON (2026-11-07):** el usuario pidió aprender y aplicar peso, volumen y formas que se apoyan en otras (ej.: la barba tiene que caer sobre el cuerpo, no meterse adentro) con agentes Haiku, armar una lista de categorías, aplicarlas y hacer el reel.
- Categorías y reglas: `videos/RESEARCH_3D_FORMS.md` (contacto/drapeado, peso, volumen/deformación, formas secundarias, superficie y luz horneada, set y cámara) + qué se aplicó.
- Biblioteca de personajes: `videos/biblioteca/3d/toonchar.py`; El Mago v2 `mago3d.py`; Papá Noel `santa3d.py` → `glb/mago.glb`, `glb/santa.glb` (46 clips cada uno). Ayudas web compartidas: `videos/biblioteca/3d/web/toon3d.js`.
- Reel: `videos/papa-noel-en-ojotas/hf3d/` (17 s, 4 planos), audio `cues3d.json`, armado con `../build3d.sh` (copia three.js, toon3d.js, glbs y sintetiza el audio). Render: `papa-noel-en-ojotas-3d.mp4` (60 fps).
- Siguiente: comentarios del usuario sobre el reel 3D; pulir las acciones que no tienen clip propio; caption.

**DIRECCIÓN: 3D TOON (2026-11-06, noche):** el usuario eligió el 3D toon (no pixel) y pidió proporciones y animación correctas con un equipo de investigación Haiku. Síntesis en `videos/RESEARCH_3D_TOON.md`.
- El Mago 3D: `videos/biblioteca/3d/mago3d.py` → `glb/mago.glb` (cuerpo de 3 cabezas, sin cuello, sombrero con punta curvada, barba hasta el cinturón, botas, manos de mitón; esqueleto CC0 acortado, 46 clips, huesos extra hat.1-3, beard.1-2, eyes, brows).
- Reel: `videos/experimentos/mago-toon/` (`build.sh` copia libs y glb; `cues.json` → audio con chiptune.py; `npx hyperframes render --fps 60`). Velocidad de caminata medida del clip (sin patinar), resortes simulados una vez, parpadeos, contornos sin picos (normales suavizadas), cámara con lente larga.
- El usuario rechazó el entorno nuevo SOLO porque desde el teléfono no se puede aprobar: si lo pide desde la PC, proponerlo de nuevo (Hugging Face, Poly Haven, Kenney, blender.org).
- Siguiente: comentarios del usuario sobre `mago-toon.mp4`; acciones propias (mate, magia) con mocap de video del usuario o poses a mano; Papá Noel 3D; reel completo de Navidad en 3D.

**3D fase 1 + prueba 3D completa (2026-11-06, noche):** el usuario (escribe en inglés) pidió instalar todas las herramientas gratis posibles, avanzar con la fase 1 y explicar cómo se hacen los reels 3D tipo "4 modelos de IA, un gallo" (three.js de una sola página, primitivas, grabación de pantalla; explicado en `videos/PLAN_3D.md`). Le gusta el estilo Dead Cells y también le interesa 3D completo si es de calidad.
- Instalado (se pierde con el contenedor; comandos en `videos/PLAN_3D.md` "Reinstall"): `bpy` 5.2.3 en `/opt/bpy` (+ OpenEXR, trimesh, OpenCV...), three.js 0.170.0 en `/opt/three`, biblioteca de animaciones CC0 de Quaternius (46 clips) en `/opt/assets3d/ual`.
- El usuario RECHAZÓ crear un entorno nuevo con Hugging Face, Poly Haven, Kenney y blender.org: no volver a proponerlo. Imagen→3D (TRELLIS/Hunyuan3D) y Mixamo quedan del lado del usuario.
- Fase 1 hecha: `videos/biblioteca/3d/taller_props.py` (impresora con regalo que crece, banquito, bolsa con 4 estados, arbolito con luces, ventilador que oscila) → `skills/pixel-reel/scripts/blender/pixel3d.py` + `pixelize3d.py` → `videos/biblioteca/3d/sprites/` (atlas3d.json, assemble.py lo suma solo). Runtime: opción `cast` para la sombra proyectada. Reel: `avance-4.mp4` (60 fps); la impresora pasó a x=98 (no la tapa el Mago). Falta la puerta en perspectiva.
- Prueba 3D completa: `videos/experimentos/3d-full/` (three.js en HyperFrames, maniquí CC0 vestido de mago, impresora .glb, mocap; `render_both.sh` → `3d-toon.mp4` y `3d-pixel.mp4`). `build.sh` copia librerías y modelos a `hf/` (no versionados).
- Próximo: que el usuario elija entre Dead Cells (sprites desde 3D), 3D completo toon o 3D pixelado; fase 2 (GLB del Mago desde el model sheet aprobado, en la web de TRELLIS/Hunyuan3D); la puerta.

**3D (2026-11-06):** el usuario preguntó por avatares 3D y Blender. Plan en `videos/PLAN_3D.md` (sprites pre-renderizados desde 3D, herramientas gratis, fases). Probado: `bpy` 5.2.3 se instala con pip en un venv (`python3 -m venv bl && bl/bin/pip install bpy`); para EEVEE hay que instalar Mesa (`apt-get install -y libegl1 libgl1 libegl-mesa0 libgl1-mesa-dri libgles2 libxi6 libxkbcommon0 libsm6 libxxf86vm1 libxfixes3 libxrender1`) y correr con `EGL_PLATFORM=surfaceless`; Cycles CPU ~0,3 s por cuadro de sprite. Prueba de concepto: `videos/experimentos/3d-printer/` (impresora low-poly, 60 cuadros, Freestyle 1 px, paleta + 5 grises). Esperando decisión del usuario sobre las fases.

**2026-11-06 (noche):** el usuario dijo que el reel se ve "very very choppy" y los objetos planos; pidió investigar con 10 agentes Haiku. Síntesis y plan en `videos/RESEARCH_PIXEL_REELS.md`. Aplicado: motor de movimiento v2 (posiciones suaves ajustadas a la grilla, fps divisores, 60 fps), `draw_light.py` (luz, sombras de contacto, viñeta, sombra de personajes), polvo en la luz → `avance-3.mp4` (60 fps). Siguiente según el plan: pasada de "juice" en la secuencia de regalos y vida ambiente (Claude); props en 3/4 y caminatas de 8 cuadros (Gemini). El usuario escribió en inglés en este pedido.

**Tanda 7 (2026-11-06, reemplaza a la 6):** Claude hizo fx_1..3 (`draw_fx.py`) y `mago_idle_N_1` (derivada), y arregló `mago_walk_E_1` y `papa_noel_sack_shake_S_1`; ranking en `videos/biblioteca/AUDITORIA.md`. A Gemini van solo 16 hojas: 9 animaciones del Mago, `mago_sip_mate_S_2` y `mago_joy_jump_S_2` (en el mismo chat que su parte 1), items_1/2/3/5/6, más `papa_noel_sad_S_1` opcional (la aprobada es floja). Al importar fx hechos por Claude NO usar `--import`: el QC marca como vacíos los cuadros chicos a propósito y la normalización no hace falta. Último avance: `avance-2.mp4`.

**Tanda 6 enviada (2026-11-06):** las 20 hojas que faltan (11 animaciones del Mago incl. `mago_sip_mate_S_2` y `mago_joy_jump_S_2` armadas a mano para hacer en el mismo chat que su parte 1, fx_1..3, items_1/2/3/5/6). 30 aprobadas + 20 = las 50 del reel. Al llegar el zip: importar (`--import`), revisar contactos (si la parte 1 aprobada de sip_mate/joy_jump no es la que usó para la parte 2, re-pedir la 2), re-ensamblar y render final.

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
