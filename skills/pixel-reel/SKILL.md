---
name: pixel-reel
description: Producir reels y videos cortos en pixel art 16 bits (9:16, 10-30 s) con personajes recurrentes, usando un modelo de imagen (Gemini u otro) para generar hojas de sprites y HyperFrames para animar y renderizar. Usar siempre que alguien quiera un reel, short, TikTok o video animado en pixel art o estilo videojuego retro con su mascota o personaje, armar o ampliar una biblioteca de sprites reutilizable (animaciones, emociones, escenarios, objetos, efectos), escribir prompts para generar sprite sheets, convertir sprite sheets en animaciones, o planificar el guion de un video animado por sprites; también cuando pase keyframes sueltos y pida "animarlos" en estilo pixel art. Pixel art reels, sprite sheet pipeline, Gemini sprites, HyperFrames pixel animation.
---

# pixel-reel

Workflow para hacer reels de pixel art **a partir de piezas** (fondo vacío + hojas de sprites con sus poses) en lugar de desarmar keyframes pintados. Es lo que aprendimos a la fuerza: cuando entran 4 imágenes sueltas, todo lo que falta (fondo detrás del personaje, poses intermedias, estados de objetos) termina inventado o parchado, y el resultado se ve raro. Ver `references/lecciones.md`.

La regla de oro: **se diseña todo antes de generar** (guion, beats, posiciones, cada animación cuadro por cuadro, cada objeto con sus estados, efectos, audio) en un manifiesto. Las imágenes se piden en un formato fijo pensado para cortarse solo, y el video se arma con un runtime de animación por pasos.

Requiere: Python 3 con numpy y Pillow; Node con `npx hyperframes` (y su skill `/hyperframes` para el contrato de render); un modelo de imagen que acepte imágenes de referencia. Para generar las hojas automáticamente con Gemini: `pip install google-genai`, la clave en la variable de entorno `GEMINI_API_KEY` y salida de red a `generativelanguage.googleapis.com`.

## Estructura de un proyecto

```
<proyecto>/
├── biblioteca/                 # se reutiliza en todos los reels
│   ├── sprites.json            # FUENTE DE VERDAD: estilo, personajes, animaciones, sets, efectos, ítems
│   ├── sheets/                 # hojas aprobadas del modelo de imagen (nombres fijos)
│   ├── PROMPTS.md, CATALOGO.md, palette.png   # generados
└── <reel>/
    ├── reel.json               # qué usa de la biblioteca, personajes propios, posiciones y beats
    ├── cues.json               # audio: efectos con tiempo, música, ambiente
    ├── GUION.md                # guion legible: idea, beats, caption
    ├── PROMPTS.md              # solo las hojas que necesita este reel (generado)
    ├── placeholder-sheets/     # provisorias para el animatic (generadas, no se versionan)
    └── hf/                     # proyecto HyperFrames (index.html + assets/ armados por assemble.py)
```

Para empezar de cero: copiar `assets/templates/` (manifiesto, reel y cues de ejemplo) y adaptarlos.

## Etapas

Trabajar en este orden. Cada etapa tiene una salida concreta y, cuando corresponde, una aprobación de la persona antes de seguir.

**0. Guion.** Con la persona: idea, tono, duración, personajes, un solo escenario y una sola cámara fija por reel. Si hace falta, explorar temas con subagentes (historia, gancho comercial, reutilización). Escribir `GUION.md` y los `beats` de `reel.json` con tiempos y posiciones en píxeles de arte. Cada acción de un personaje es una animación corta con nombre (`walk_E`, `surprised_S`...). Si no existe en la biblioteca, se agrega.

**1. Manifiesto.** Completar `biblioteca/sprites.json` y `reel.json` (formato en `references/manifiesto.md`). Describir cada animación **cuadro por cuadro** (`poses`), con dirección, modo (bucle / una vez / queda en el último) y fps. Cada objeto que cambia lleva sus estados como cuadros. Los adornos de temporada van aparte del fondo. Las reglas de estilo están en `references/estilo.md`.

**2. Prompts.** `python3 scripts/gen_prompts.py biblioteca/sprites.json <reel> --reel <reel>/reel.json [--only-missing biblioteca/sheets]`. Escribe `PROMPTS.md` en orden de aprobación (paleta → model sheets → imagen maestra → fondo vacío → animaciones, objetos, efectos e ítems) y `palette.png`. Claude no llama al modelo de imagen: la persona pega cada prompt con sus adjuntos y guarda lo aprobado en `biblioteca/sheets/` con el nombre indicado. Cómo pedir y qué hacer cuando el modelo falla: `references/gemini.md`.

**2b. Generación automática con Gemini (opcional).** Si `GEMINI_API_KEY` está en el entorno, `scripts/gemini_generate.py` reemplaza el copiar y pegar. Usa el mismo plan y los mismos prompts y adjuntos de `PROMPTS.md`, pide solo lo que falta en `biblioteca/sheets/` y respeta el orden de los gates. Por cada hoja:
- pide varias variantes y las guarda en `biblioteca/candidates/<hoja>/`;
- las puntúa con el control de calidad (`scripts/qc.py`): celdas vacías o de más, sprite que toca el borde, altura, ancla, paleta, magenta plano, nitidez del píxel;
- arma `contact.png`;
- deja todo registrado en `biblioteca/generation_log.jsonl`, sin la clave.

Los **gates 2 a 4 nunca se aprueban solos**: mostrarle `contact.png` a la persona y aprobar con `--approve hoja.png=N`. En el gate 5 se aprueba sola la mejor variante que pase el control; si ninguna pasa, se vuelve a pedir una vez con las correcciones de `references/gemini.md`. Siempre conviene correr primero `--dry-run` y fijar un tope de gasto con `--max-images`. Para verificar la clave sin gastar: `scripts/gemini_check.py`, que muestra solo el largo de la clave y los modelos de imagen disponibles. Detalles en `references/gemini.md`.

**3. Animatic, sin esperar a las imágenes.** `python3 scripts/placeholders.py biblioteca/sprites.json <reel>/placeholder-sheets --reel <reel>/reel.json` genera hojas provisorias con los mismos nombres y formato, así que todo lo que sigue funciona igual. Con eso se arma, anima y renderiza el reel completo: se fijan el timing, la puesta y el audio mientras se generan las imágenes reales.

**4. Ensamblado.** `python3 scripts/assemble.py biblioteca/sprites.json biblioteca/sheets:<reel>/placeholder-sheets <reel>/reel.json <reel>/hf`. Hace tres cosas:
- recorta las hojas (las aprobadas primero; las provisorias cubren lo que falte), con magenta fuera, grilla de píxel, paleta y ancla en los pies;
- escribe `hf/assets/pr/atlas.js` y las tiras de cuadros;
- sintetiza el audio de `cues.json` y copia el runtime.

Leer `hf/assets/pr/slice_report.md` y mirar `hf/assets/pr/review/`, donde cada hoja aparece con su línea de ancla y una vista en papel cebolla. Si una hoja real sale torcida, cortada o fuera de escala, se vuelve a pedir: no se parchea.

**5. Animación.** Inicializar el proyecto con `npx hyperframes init <reel>/hf --resolution portrait --non-interactive`, partir de `assets/reel-template.html` y escribir la línea de tiempo con el runtime `pixel-reel.js` (API y recetas en `references/animacion.md`): actores, `play`, `walk`, `hops`, `arc`, `pop`, efectos de un pool y disolución por bloques. Las posiciones van en píxeles de arte y los cambios siempre por pasos. Seguir el contrato de HyperFrames: `npx hyperframes check`.

**6. Audio.** Un `cues.json` por reel con efectos sincronizados a los beats, música y ambiente (`references/audio.md`). `scripts/chiptune.py` lo sintetiza en tres pistas: efectos, música y ambiente. Usar solo melodías propias o de dominio público.

**7. Revisión y render.** Tomar snapshots en cada beat (`npx hyperframes snapshot --at ...`), revisarlos y renderizar a 60 fps (`npx hyperframes render --fps 60 -o <reel>/<reel>.mp4`). Si GSAP no se puede bajar de un CDN, tiene que estar en `hf/assets/gsap.min.js`; `assemble.py` lo copia si encuentra un `node_modules/gsap` cerca.

Cuando llegan hojas reales nuevas, se vuelve a correr la etapa 4 y se renderiza. La línea de tiempo no cambia, porque los nombres y anclas son los mismos.

## Qué entregar en cada vuelta

- Antes de las imágenes: guion, prompts y animatic renderizado (MP4) para validar timing y sonido.
- Con imágenes parciales: el mismo video con las piezas reales que ya estén; el reporte del recorte dice cuáles son todavía provisorias.
- Al final: el MP4, el caption y la lista de lo que se agregó a la biblioteca (queda para el próximo reel).

## Scripts

| Script | Qué hace |
|---|---|
| `scripts/prmanifest.py` | Lee el manifiesto y arma el plan de hojas con nombres estables (lo usan todos) |
| `scripts/gen_prompts.py` | Prompts en orden de aprobación, catálogo legible y `palette.png` |
| `scripts/gemini_generate.py` | Genera las hojas que faltan con Gemini: variantes, control de calidad, hoja de contacto, aprobación y log |
| `scripts/gemini_check.py` | Verifica la clave (solo su largo) y la conexión, y lista los modelos de imagen, sin gastar |
| `scripts/draw_fx.py` | Dibuja las hojas de efectos sin modelo de imagen (destellos, polvo, confeti, corazones, sudor, idea, vapor, espiral, polilla, anillo, notas, motas) |
| `scripts/draw_light.py` | Luz de ventana, sombras de contacto, viñeta y sombra de personajes, pixel-crisp con dithering |
| `scripts/qc.py` | Control de calidad de una hoja (lo usa el generador; sirve también para hojas hechas a mano) |
| `scripts/placeholders.py` | Hojas provisorias en el formato exacto (`--noisy` imita los defectos del modelo, para probar) |
| `scripts/slice_sheets.py` | Hoja → tiras por animación + `atlas.json`/`atlas.js` + revisión + reporte |
| `scripts/chiptune.py` | Cues → `sfx.wav`, `music.wav`, `ambience.wav` (`--list` muestra los 30 efectos) |
| `scripts/assemble.py` | Recorte + audio + runtime dentro del proyecto HyperFrames |
| `assets/pixel-reel.js` | Runtime de animación por pasos para HyperFrames |
| `assets/reel-template.html` | Composición base con escenario, actores, pool de efectos y audio |
