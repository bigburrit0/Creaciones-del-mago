# Traspaso — Creaciones del Mago: reel de Navidad "Papá Noel en ojotas" — actualizado 2026-11-14

## Próximo paso exacto
**ESTADO DE LA SEGUNDA TANDA (14/11, noche; el dueño pidió "empezá a trabajar en los videos de ajedrez"; la ocarina de 12 huecos es para OTRA sesión):**
- **W1 "Los gatos tiran todo":** TERMINADO. `videos/los-gatos-tiran-todo/los-gatos-tiran-todo.mp4` (23,0 s), commiteado y enviado. Controles en la sección "Result" de `GUION.md`. El render salió a -15,8 LUFS y se remezcló a -14,6.
- **W2 "La gaviota":** renderizando (3 workers). Al terminar:
  - parpadeos, LUFS (remezclar si hace falta), zumbido, voces de la mezcla, hoja de contacto;
  - sección "Result" en `GUION.md`, commit del mp4, enviarlo.
- **W3 "El laberinto":**
  - kit nuevo `videos/biblioteca/3d/web/grecia3d.js`: muros de dos filas con pasillo, templo, Minotauro, Hércules, hoplitas, columnas, pegasos;
  - escena en un patio mediterráneo;
  - puerta de calidad 0/1380, 0 saltos; música medida;
  - caption y DM en `GUION.md`;
  - falta renderizar DESPUÉS de W2 (nunca dos renders juntos), con los mismos controles.
- **W4 "El mantel":** `videos/el-mantel/voces.json` listo; la cuota de TTS se renueva a las 08:00 UTC. Después: kit del tablero rompecabezas (4 cuadrantes + 4 lados del marco), mantel a cuadros, mesa de Nochebuena, cues (C ionian), QA, render, copy.
- **Las tareas programadas de las 2:00 (15-18/11)** siguen con el próximo reel W sin terminar; primero terminan lo que esté a medias.

**NOVIEMBRE, SEGUNDA TANDA (pedido del 14/11):** "más reels de noviembre", investigación con Haiku, foco ajedrez pero con otras imágenes; la música era muy alta y molesta, que sea suave, tipo ambience.
- **Investigación:** `videos/RESEARCH_NOVIEMBRE_2_2026.md`. Cinco Haiku: formatos visuales, calendario de Uruguay, embudo y personas, humor, música ambiental.
- **Otras imágenes:** los otros ajedreces del catálogo: perros vs gatos, antigua Grecia (trae tablero de 52 × 50), de viaje (tubo de 24 cm), tablero rompecabezas, escultórico, minimalista. También escenarios nuevos fuera del taller.
- **Guiones:** `videos/PLAN_NOVIEMBRE_2.md` (reescritos el 14/11 a pedido del dueño: otros ajedreces, historias nuevas; se crean programados a las 2:00 del 15, 16, 17 y 18/11):
  - W1 "Los gatos tiran todo" (15/11);
  - W2 "La gaviota" (16/11);
  - W3 "El laberinto" (17/11);
  - W4 "El mantel" (18/11).
- **Música:** `chiptune.py` tiene `"style": "ambient"`; los seis reels de noviembre se remezclaron (imagen idéntica) con la música 22-25 dB bajo las voces. Medidor: `videos/biblioteca/nivel_musica.py`.
- **Preguntas al dueño:**
  - ¿el tubo de viaje se abre en tablero?
  - ¿para qué son los imanes del escultórico?
  - ¿colores por bando en perros vs gatos?
  - ¿cuántas partes y qué colores tiene el tablero rompecabezas?

**"CULPA DE LAS PIEZAS" (tarea programada del 13/11 a las 2:00, llegó a tiempo):** reel 5 de ajedrez, el último de la serie.
- **Fecha límite de Navidad (la dio el dueño el 12/11):** el último día para pedir es el 23 de diciembre ("hasta el 23 de diciembre"). Es el último día de pedido, no una promesa de entrega.
- **Auditoría:** `videos/culpa-de-las-piezas/AUDIT.md`:
  - el producto se nombra en el cuadro 1;
  - la revancha es el mate del pastor: el rey vikingo cae y sus propios vikingos se dan vuelta a mirar a Papá Noel ("Las piezas no pierden. Vos sí.");
  - un rey vikingo rojo se imprime capa por capa;
  - Papá Noel pregunta "¿Hasta cuándo lo puedo pedir?" y aparece la hoja de calendario con el 23;
  - el caption borrador prometía entrega ("para que llegue antes de Navidad") y se corrigió.
- **Reel:** `videos/culpa-de-las-piezas/` (24,2 s). Puerta de calidad 0/1452, 0 saltos.
- **Caption y DM:** en `GUION.md`.
- **La serie de ajedrez está completa** (5 reels). No empezar nada nuevo sin pedido.

**"LAS PREGUNTAS DE PAPÁ NOEL" (tarea programada del 12/11 a las 20:00, llegó a tiempo):** reel 4 de ajedrez.
- **Auditoría:** `videos/las-preguntas-de-papa-noel/AUDIT.md`. El borrador era un FAQ seco; ahora:
  - el chiste es la lista de Papá Noel, con un contador "Pregunta 1/4 … 4/4";
  - a 4/4 la lista se desenrolla hasta el piso y el contador salta a 5/87: "¡Esperá, que tengo más!", y El Mago responde seco: "Las demás… en comentarios.";
  - cada respuesta tiene su imagen: stickers de precio y fecha (sin número), la regla con el rey a 9,5 cm reales, el peón que se cae y se reimprime capa por capa, el tablero que se va aparte;
  - el CTA ofrece precio y fecha ("Comentá DUDA y te contesto, con precio y fecha").
- **Reel:** `videos/las-preguntas-de-papa-noel/` (27,2 s). Puerta de calidad 0/1632, 0 saltos.
- **Caption y DM:** en `GUION.md` (los 3 redactores, curado; esta vez ninguno escribió "envío gratis a todo Uruguay").
- **Siguiente:** reel 5, "Culpa de las piezas" (hecho el 13/11, ver arriba).

**"ELEGÍ TU BANDO" (tarea programada del 9/11 a las 2:00, que llegó y se hizo el 12/11):** reel 3 de ajedrez.
- **Auditoría:** `videos/elegi-tu-bando/AUDIT.md`:
  - el producto se nombra en el cuadro 1;
  - se repintan los dos bandos ("un bando" y "el otro");
  - el rey en 4 colores queda igual a Papá Noel (el chiste y la función a la vez);
  - el CTA ofrece precio y fecha.
- **Reel:** `videos/elegi-tu-bando/` (21,6 s). Puerta de calidad 0/1296, 0 saltos.
- **Caption y DM:** en `GUION.md`.
- **Siguiente:** reel 4, "Las preguntas de Papá Noel" (hecho el 12/11, ver arriba).

**"UNA MÁS" (tarea programada, 2026-11-08 2:00 Montevideo):** reel 2 de ajedrez, con auditoría del guion y una investigación desde otro punto de vista.
- **Investigación:** `videos/RESEARCH_AJEDREZ_2_2026.md`, con cuatro ángulos nuevos y el análisis de toda la investigación anterior:
  - la voz del cliente;
  - la competencia en Uruguay;
  - la psicología del regalo hecho a mano (labor illusion, handmade effect);
  - un crítico.
- **Auditoría:** `videos/una-mas/AUDIT.md`. El guion se reescribió:
  - el producto se nombra en el cuadro 1 y hay un contador 1/32;
  - el paso de las horas se cuenta con la luz;
  - sale el gag de la impresora desenchufada;
  - el CTA ofrece precio y fecha.
- **Reel:** `videos/una-mas/` (27,2 s). Puerta de calidad 0/1632. El primer intento de render corrió en la raíz del repo (el `cd` no tomó) y se relanzó con `bash -c`.
- **Caption y DM:** en `videos/una-mas/GUION.md` (los 3 redactores, curado).
- **Siguiente:** reel 3, "Elegí tu bando", cuando el usuario lo pida.

**SERIE DE AJEDREZ (2026-11-07, noche):** el usuario dijo que los ajedreces medieval y vikingo son de lo que más se vende y pidió:
- tres equipos de 3 Haiku cada uno (marketing, humor y guion, edición y ritmo);
- guardar la investigación;
- 5 guiones;
- el copy con los mismos redactores de antes;
- renderizar el primero.

Hecho:
- **Investigación:** `videos/RESEARCH_AJEDREZ_2026.md` (incluye la auditoría y corrección de la investigación de noviembre).
- **Guiones y copy:** `videos/PLAN_AJEDREZ.md` (los 5 guiones y los 5 captions curados de los 3 redactores; un error de envío gratis corregido).
- **Kit de ajedrez:** `videos/biblioteca/3d/web/ajedrez3d.js` (tablero, set vikingo y set medieval modelados desde las fotos del sitio).
- **Reel 1:** `videos/vikingo-o-caballero/` → `vikingo-o-caballero.mp4` (26,8 s). Puerta de calidad 0/1608, 0 saltos; -13,6 LUFS; todas las voces claras.
  - El primer render tuvo 1 cuadro de parpadeo: un cabeceo de un cuadro por la risa en "¡Cebame uno!".
  - Se suavizó la envolvente de voz en `build.sh` y se volvió a renderizar.
- **Sintetizador:** sonidos nuevos clack, thud, lur y bell.
- **Lecciones:** en `skills/reel-3d-toon/references/lecciones.md`.

Pendiente del usuario:
- la fecha de corte para Navidad (reel 5);
- la licencia comercial de los diseños vikingo y medieval;
- si la serie de ajedrez va antes que N2 y N3 de noviembre.

Siguiente: reel 2 "Una más" cuando lo pida.

**POSTEO DE NOVIEMBRE PARA VENDER (2026-11-07, tarde):** el usuario pidió un equipo de 5 investigadores Haiku muy enfocados en marketing (ventas, embudo, estructura de reel), analizar, escribir 3 guiones de noviembre y hacer el primero.
- Investigación y análisis: `videos/RESEARCH_NOVIEMBRE_2026.md` (señales de Instagram: tiempo de visualización, likes y envíos por alcance; gancho en 1,5 s; un solo CTA tipo comentario; producto real al final; calendario uruguayo; qué es sólido y qué no).
- Guiones: `videos/PLAN_NOVIEMBRE.md`: N1 "Un regalo para cada amigo" (alcance, vie 13/11), N2 "Mandame una foto" (consideración, mar 17/11), N3 "¿Llego para Navidad?" (conversión, lun 23/11). Hay decisiones pendientes del usuario: fecha de corte, oferta, foto de una pieza real hecha desde una foto, respuesta a "Comentá FOTO".
- Hecho N1: `videos/un-regalo-para-cada-amigo/` → `un-regalo-para-cada-amigo.mp4` (25,3 s). Cinco productos reales del catálogo modelados desde las fotos del sitio, prueba real con esas fotos ("Así son de verdad") y CTA "Etiquetalo". Puerta de calidad 0/1518, 0 saltos, determinista; 0 parpadeos; -14,0 LUFS; 8/8 voces. Caption, texto alternativo e historia del mismo día en `GUION.md`.
- Lecciones nuevas en `skills/reel-3d-toon/references/lecciones.md` (estructura de venta, fila recta de productos, ala del sombrero, etiquetas en la zona de subtítulos, cortar tomas a mano).
- Siguiente: comentarios del usuario; N2 cuando lo pida.

**KIT COMPARTIDO + "INVISIBLE NO ERA" (tarea programada, 2026-11-07 1:20 Montevideo):** el usuario pidió el kit y el reel 1, con todos los chequeos, nada "lazy" y categorías de todo lo que sale en pantalla.
- Kit: `videos/biblioteca/3d/web/escena3d.js` (escenario con luz de día/noche/amanecer, elenco con colisionadores y barbas, impresora, props, IK con guardia de contacto, resortes, voces, subtítulos píldora o cinéticos, placa, cámara con planos encuadrados/barridos/zooms/POV, QA común). El reel de Navidad se pasó al kit: cuadros idénticos píxel a píxel y puerta de calidad 0/1260.
- Reel: `videos/invisible-no-era/` (27,4 s): `BRIEF.md`, `ON_SCREEN.md` (categorías y evidencia), `GUION.md` (beats y caption: principal + 2 alternativas de los 3 redactores Haiku), `voces.json` → `voz/`, `cues.json`, `build.sh`, `hf3d/`. Render: `invisible-no-era.mp4`. Puerta de calidad 0/1644, 0 saltos, determinista; 0 parpadeos; -13,9 LUFS; las 7 líneas se entienden. Publicar el martes 1/12.
- Lecciones nuevas en `skills/reel-3d-toon/references/lecciones.md` (escenificar mirando a cámara, muebles sólidos, arcos de manos, placas que tapan cambios, paredes teseladas). Herramienta nueva: `videos/biblioteca/3d/web/jumpwin.cjs` (saltos en una ventana, 2 min).
- Siguiente: comentarios del usuario; reel 2 "¿Reyes Magos? Mago soy yo" (publicar 28/12).

**V2 DEL REEL DE NAVIDAD (2026-11-07, noche):** el usuario pidió una V2 con las mismas voces y otro ángulo de cámara y estilo de edición. Hecho en `videos/papa-noel-en-ojotas/hf3d-v2/` → `papa-noel-en-ojotas-3d-v2.mp4`: 16 planos encuadrados midiendo la cabeza (contrapicados, picados, travellings, plano a dos, detrás de la impresora, holandés), zooms de golpe, barridos, sacudones, destello y subtítulos palabra por palabra con título gancho. Puerta de calidad 0/1260, 0 parpadeos, -12,7 LUFS. Detalle en `GUION.md` → "Versión 2". Programado: a la 1:20 (Montevideo) arranca el kit compartido + "Invisible no era" (`videos/invisible-no-era/BRIEF.md`).

**LECCIONES, CAPTION Y PRÓXIMOS REELS (2026-11-07, tarde):** al usuario le encantó el reel. Pidió guardar todo lo aprendido para no repetir errores, el texto para la descripción (con subagentes Haiku, algo "marketinero") y planificar 3 reels más con un equipo Haiku que busque ideas (memes y referencias 2026).
- Lecciones: nueva skill `skills/reel-3d-toon/` (SKILL.md + `references/lecciones.md`, `voces-y-texto.md`, `qa.md`; paquete `skills/reel-3d-toon.skill` con `empaquetar.sh` para subirla a claude.ai). Ayudas nuevas: `videos/biblioteca/3d/web/frames3d.cjs`, `flicker_scan.py`, `videos/biblioteca/check_voces.py`. Reglas 15–17 en `RESEARCH_3D_CONTACT.md`.
- Caption: `papa-noel-en-ojotas/GUION.md` → "Caption para Instagram" (principal + 2 alternativas). Publicar antes del 20/11.
- Ideas: `videos/RESEARCH_IDEAS_2026.md` (formatos 2026, referencias locales, productos y licencias, calendario a marzo 2027).
- Plan: `videos/PLAN_PROXIMOS_REELS.md` → 1) "Invisible no era" (amigo invisible, publicar 1/12), 2) "¿Reyes Magos? Mago soy yo" (Reyes, 28/12), 3) "Ola de calor, vuelta a clases" (llaveros con nombre, 20/2). Paso 0: sacar un kit de escena compartido (`escena3d.js`).
- Siguiente: que el usuario apruebe los tres guiones; empezar por el paso 0 y el reel 1.

**PUERTA, BARBA, VOCES, TEXTO Y CIERRE (2026-11-07):** el usuario vio a Papá Noel atravesar la puerta y la barba metiéndose en el cuerpo al final; pidió arreglarlo, sumar voces y texto y cerrar el reel.
- Puerta: abre hacia adentro (bisagra a la derecha), vano de 0,90 m. Papá Noel entra y sale por el MEDIO, de frente a la pared (curvas `PIN`/`POUT`), saluda bien adentro, se pasa la bolsa a la espalda al darse vuelta y sale derecho; la puerta se cierra detrás de él.
- Barba: la punta se hundía 4–6,5 cm en la túnica y el cinturón en TODOS los cuadros (seguía a los huesos del pecho; el cinturón, a la cadera). Ahora cada punto de la barba toma los pesos de la superficie que tiene debajo: `toonchar.transfer_weights()` en `mago3d.py` y `santa3d.py`.
- La puerta de calidad (`qa3d.cjs`) ahora también revisa paredes, marco, hoja de la puerta y ~450 puntos de cada barba apoyados en el cuerpo. Reglas 13 y 14 en `videos/RESEARCH_3D_CONTACT.md`.
- Voces (Gemini TTS, clave inyectada por el proxy, nunca impresa): `videos/biblioteca/tts_lineas.py` (una toma por personaje, cortada en las pausas, recortes y -16 LUFS) con `papa-noel-en-ojotas/voces3d.json` → `voz3d/`. Papá Noel: Algenib; el Mago: Charon. Líneas, tiempos y subtítulos: `GUION.md` → "Diálogo".
- Texto: subtítulos con el color de cada personaje (Fredoka, zona segura) y placa final "Regalos impresos en 3D · ¡Pedí el tuyo! · Escribime por mensaje". El reel dura 21 s, con 5 planos.
- Resultado: puerta de calidad 0/1260 cuadros con problemas, 0 saltos, determinista; 0 cuadros con parpadeo en el render; mezcla -12,7 LUFS con todas las voces inteligibles. Render: `videos/papa-noel-en-ojotas/papa-noel-en-ojotas-3d.mp4` (21 s, 60 fps; `cd hf3d && npx hyperframes render --fps 60 --workers 4 -o ../papa-noel-en-ojotas-3d.mp4`, unos 15 min).
- Siguiente: comentarios del usuario; publicar con el caption de `GUION.md`.

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
