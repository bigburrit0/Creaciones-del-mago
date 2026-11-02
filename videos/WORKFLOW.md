# Videos pixel art con Claude + Gemini + HyperFrames: qué se retrabajó y cómo evitarlo

Informe de los dos videos hechos hasta ahora (`mate-power-up/` y `mago-jardin/`) y propuesta de workflow para los próximos.

## 1. El problema en una frase

HyperFrames no "imagina" cuadros: **mueve y cambia piezas** (sprites, fondos, partículas) sobre una línea de tiempo. Si solo entran 4 keyframes "pintados", Claude tiene que **desarmar** esas imágenes en piezas. Todo lo que falta (el fondo detrás de un personaje, una pose intermedia, el pájaro con las alas cerradas) se inventa, se recorta a mano o se resuelve con trucos. De ahí salen los resultados raros.

**Regla de oro:** generar desde el principio **las piezas** (fondo vacío + hojas de sprites con sus poses) y usar los keyframes solo como **referencia de composición**.

## 2. Por qué el video del mate salió bien y el del jardín no

| | Mate (power-up) | Mago en el jardín |
|---|---|---|
| ¿Keyframes alineados píxel a píxel? | Sí, los 4 | Del 1 al 3 sí; **el 4 es otra escena** (pasto, cerca alta, árbol grande) |
| ¿Cuánto cambia entre keyframes? | Poco y localizado (manija, color, vapor, gaviotas) | Mucho: personaje en 4 poses, planta en 4 estados, 4 pájaros, silla |
| ¿Había fondo sin personajes? | No hacía falta: el fondo casi no cambia | No: hubo que **reconstruirlo** |
| ¿Poses intermedias? | No hacían falta (objetos rígidos) | Faltaban todas (pararse, caminar, aletear, sentarse) |
| Resultado | Limpio | Tuvo que pasar por varias rondas de limpieza |

Conclusión: los keyframes funcionan cuando son **ediciones de una misma imagen** ("la misma imagen, pero cambiando solo X"). Fallan cuando cada uno se genera por separado.

## 3. Inventario: qué hubo que retrabajar y cómo evitarlo

### Video del jardín

| Elemento | Qué faltaba o estaba mal | Cómo se resolvió (parche) | Qué generar desde el principio |
|---|---|---|---|
| **Fondo del patio** | No había ninguna imagen sin el mago, el árbol ni el comedero | Mediana de los keyframes 1 a 3, franjas de arena copiadas fila por fila, parcelas copiadas de la parcela vecina. Dejó manchas y costuras que hubo que limpiar en 4 rondas | **Fondo vacío** (plate): la escena sin personajes ni objetos que se muevan |
| **Mago arrodillado / parado / señalando** | Solo 3 poses sueltas, mezcladas con el fondo | Recorte por diferencia entre keyframes. Arrastró la cola del benteveo, un pedazo de copa y tierra | **Hoja de sprites del mago** sobre fondo de color plano |
| **Mago se levanta** | No había pose intermedia | Se estira el sprite parado ("squash") | Cuadros: arrodillado → medio parado → parado |
| **Mago camina** | Sin ciclo de caminata | Saltitos de un solo sprite con inclinación ±4° | **Ciclo de caminata de 4 cuadros** (y de perfil si cruza la escena) |
| **Mago se sienta con el mate** | Solo existía en el keyframe 4 (otra escena), con la silla incluida | Recorte con varita mágica + "puf" de polvo para tapar el cambio | Cuadros: parado junto a la silla → sentándose → sentado; 2 cuadros de sorbo |
| **Silla** | Plegada en 1 a 3, abierta en el 4; nunca se ve la transición | Se borró la silla plegada del fondo (inpainting) y se tapó con el "puf" | Silla **plegada / a medio abrir / abierta** como sprites aparte (no pintada en el fondo) |
| **Semilla** | Solo un brillito en la mano | Punto dorado dibujado en CSS | Sprite de semilla + destello |
| **Planta (4 estados)** | Solo existía el árbol joven. El brote no existía y el arbolito era el árbol achicado (mezcla de escalas de píxel) | Brote dibujado a mano en código; arbolito = árbol al 55 % | **Hoja de etapas de crecimiento**: semilla, brote, plantín, árbol joven, a la misma escala de píxel |
| **Copa del árbol → comedero** | El keyframe 3 **no tiene copa** (contradice al 2) | La copa estalla en hojas mientras crece el comedero | Keyframes coherentes: el comedero cuelga del árbol **con** copa; o un sprite "la copa se abre y aparece el comedero" |
| **Comedero** | El benteveo lo tapaba en el keyframe 3 | Se rellenó el hueco espejando la otra mitad del hexágono | **Comedero solo**, más 2 o 3 cuadros de balanceo |
| **Benteveo** | En vuelo (keyframe 3) con restos lilas del comedero; posado (keyframe 4) a otra escala | Limpieza por color; para el aleteo se alterna el sprite en vuelo con el posado reescalado al 80 % | **Hoja del benteveo**: aleteo A/B, planeo, aterrizaje, posado, picoteo A/B |
| **Hornero** | **Naranja** en el keyframe 3 y **rojizo** en el 4 (diseños distintos) | Se tiñó el posado de naranja y se cambia el color de a poco | Mismo **model sheet** (diseño de referencia) para cada personaje; una sola paleta |
| **Gorriones** | Solo en el keyframe 4 | Recortados, reescalados al 85 %; el picoteo es una rotación | Hoja: saltito A/B, picoteo A/B, parado |
| **Cambio de escena (keyframe 4)** | Otro patio | Disolución por bloques de 0,5 s | **Todos los keyframes en la misma escena y cámara** |
| **Escala de píxel** | Las imágenes de IA tienen "píxeles" irregulares (~6 px no enteros) y JPEG | Reescalado a 1080 px + sprites al 80 % y 85 % = píxeles de distinto tamaño en la misma toma | Fijar una **grilla nativa** (ver 5.2) y llevar todo a esa grilla |

### Video del mate (para comparar)

| Elemento | Retrabajo | Prevención |
|---|---|---|
| Manija gris / dorada | Recorte por diferencia, limpio | Ya funcionó: keyframes alineados |
| Fondo detrás de la manija | Parche tomado del keyframe 3 con corrección de color (tenía viñeta) | Fondo sin manija |
| Keyframe 3 | La conservera tenía **otra tapa** (oscura) y viñeta, así que no se usó tal cual | Pedir siempre "misma imagen, solo cambia X" |
| Olas | Animación sintetizada desplazando filas | Hoja de 4 cuadros de agua en bucle |
| Vapor y gaviotas | Recorte por diferencia (las gaviotas con ruido) | Sprites aparte; gaviota con aleteo A/B |

## 4. Patrones que se repitieron

1. **Fondo oculto**: cada objeto que se mueve deja un hueco. → *Fondo vacío siempre.*
2. **Contaminación entre recortes**: el pájaro se lleva parte del comedero, el mago la cola del pájaro. → *Cada sprite generado aislado, sobre color plano.*
3. **Poses intermedias inexistentes**: pararse, caminar, aletear, sentarse. → *Hojas de sprites con los cuadros de cada acción.*
4. **Inconsistencia de diseño entre keyframes** (hornero, copa, tapa de la conservera). → *Model sheet + edición incremental en lugar de generar cada keyframe de cero.*
5. **Escalas de píxel mezcladas**. → *Grilla nativa y escala entera.*
6. **Saltos de estado sin transición** (silla, planta, escena). → *Pedir explícitamente los estados intermedios.*

## 5. Workflow propuesto (Claude + Gemini + HyperFrames)

### 5.1 Etapas

| # | Etapa | Quién | Sale |
|---|---|---|---|
| 0 | **Guion y storyboard** a partir del prompt del video: beats con tiempos, lista de elementos y de los estados de cada uno | Claude | `storyboard.md` + `assets.json` (manifiesto, ver 5.4) |
| 1 | **Imagen maestra** de la escena (estilo, paleta, cámara, escala de píxel) | Gemini | `master.png` |
| 2 | **Fondo vacío**: la maestra sin personajes ni objetos que se mueven | Gemini (edición de la maestra) | `plate.png` (+ variantes si la escena cambia: `plate_night.png`, etc.) |
| 3 | **Model sheets**: un diseño de referencia por personaje u objeto, usando la maestra como referencia | Gemini | `ref_<elemento>.png` |
| 4 | **Hojas de sprites**: cada acción en una fila, sobre magenta plano, a la escala de la maestra | Gemini (con la referencia adjunta) | `sheet_<elemento>_<accion>.png` |
| 5 | **Procesado** automático: quitar el magenta, cortar los cuadros, ajustar a la grilla, cuantizar a la paleta, fijar puntos de anclaje (pies), atlas JSON | Claude (scripts) | `sprites/…png` + `atlas.json` + hoja de control visual |
| 6 | **Prueba de armado**: componer las piezas sobre el fondo para recrear cada beat del storyboard y compararlo con la intención | Claude | `proof_beatN.png` |
| 7 | **Animación** en HyperFrames: cambio de cuadros con `steps`, recorridos, partículas, con una librería de helpers (`hops`, `walk`, `flap`, `pop`, `idle`, `sparkle`, `burst`, ya escritos en `mago-jardin/index.html`) | Claude + skill `/hyperframes` | `index.html` |
| 8 | **Audio**: hoja de cues sacada del storyboard; chiptune sintetizado o librería | Claude | `*.wav` |
| 9 | **Revisión**: `hyperframes check`, contact sheets cada 1/3 s, corrección | Claude | `REVIEW.md`, `video.mp4` |

Los keyframes del prompt pasan a ser **un resultado de la etapa 6** (se arman con las piezas), no la materia prima.

### 5.2 Grilla y formato

- **Grilla nativa** de 270×480 "píxeles de arte", escalada ×4 a 1080×1920 con vecino más cercano. Todo sprite se dibuja y se escala en enteros, nunca al 80 %.
- Pedir a Gemini **PNG**, no JPEG. Si devuelve otra resolución, el script detecta el tamaño del píxel de arte, reduce con vecino más cercano y cuantiza a la paleta de la maestra.
- **Paleta**: se extrae de la maestra (16 a 32 colores) y todo se cuantiza a ella.
- **Puntos de anclaje**: cada cuadro con su "pie" (personajes) o "gancho" (comedero), para que al cambiar de cuadro el sprite no salte.

### 5.3 Plantillas de prompt para Gemini

**Fondo vacío** (editando la maestra):
> Same image, same camera, same pixel art style and palette. Remove the wizard, the birds, the feeder, the chair and the young tree. Keep only the empty garden: wall, fence, tomato plants, soil plots, sand and tiles. Fill the hidden areas naturally. Output PNG.

**Model sheet** (con la maestra adjunta):
> Using the attached image as style reference: a character model sheet of the wizard in 16-bit pixel art, same pixel size, same palette, front three-quarter view, on a flat #FF00FF background, no shadows on the background, no text.

**Hoja de sprites** (con la maestra y el model sheet adjuntos):
> 16-bit pixel art sprite sheet of [the wizard], same design and pixel size as the reference. One row of [4] frames, evenly spaced, each centred in its own square cell of equal size, feet on the same baseline: [walk cycle facing right: contact, down, passing, up]. Flat #FF00FF background, no anti-aliasing against the background, no text, no grid lines. PNG.

Consejos:
- Siempre adjuntar la maestra y el model sheet (consistencia).
- **Una acción por hoja**; si Gemini mezcla tamaños, se piden de a 2 cuadros.
- Para estados de un objeto (planta, silla, comedero), pedirlos "en la misma escala y misma base" en una sola hoja.
- No confiar en que respete la grilla: el script corta por componentes conectados sobre el magenta, no por celdas fijas.
- Validar cada hoja con una hoja de control (los cuadros superpuestos con papel cebolla) antes de animar.

### 5.4 Manifiesto de assets (ejemplo para el video del jardín)

```json
{
  "canvas": { "native": [270, 480], "scale": 4, "fps": 30, "duration": 10 },
  "plates": ["patio_empty", "garden_empty"],
  "elements": {
    "wizard":   { "anchor": "feet", "actions": {
                    "kneel_plant": 3, "stand_up": 3, "walk_right": 4, "walk_up": 4,
                    "point": 2, "idle_breathe": 2, "sit_down": 3, "sit_idle": 2, "sip_mate": 3 } },
    "seed":     { "anchor": "center", "actions": { "glow": 2 } },
    "plant":    { "anchor": "base", "states": ["seed_mound", "sprout", "sapling", "young_tree", "tree_with_branch"] },
    "feeder":   { "anchor": "hook", "actions": { "grow": 3, "sway": 3 } },
    "kiskadee": { "anchor": "feet", "actions": { "flap": 2, "glide": 1, "land": 2, "perch": 1, "peck": 2 } },
    "hornero":  { "anchor": "feet", "actions": { "flap": 2, "glide": 1, "land": 2, "perch": 1, "peck": 2 } },
    "sparrow":  { "anchor": "feet", "actions": { "hop": 2, "peck": 2, "stand": 1 } },
    "chair":    { "anchor": "feet", "states": ["folded", "half_open", "open"] },
    "fx":       { "actions": { "sparkle": 4, "dust_puff": 4, "leaf_burst": 4 } }
  },
  "beats": [
    { "t": 0.0, "id": "plant_seed" }, { "t": 0.8, "id": "growth" }, { "t": 2.3, "id": "feeder" },
    { "t": 3.0, "id": "birds_arrive" }, { "t": 5.2, "id": "landing" }, { "t": 5.5, "id": "walk_and_sit" },
    { "t": 8.0, "id": "idle_loop" }, { "t": 9.2, "id": "hold" }
  ]
}
```

Con esto Claude sabe exactamente qué pedirle a Gemini (una lista de hojas), qué validar y cómo nombrar cada pieza en HyperFrames.

### 5.5 Qué reutilizar de lo ya hecho

- `mago-jardin/index.html`: helpers de animación por pasos (`hops`, `walk`, `path`, `flap`, `pop`, `idle`, `sparkle`, `burst`) y la disolución por bloques.
- `mago-jardin/tools/garden_lib.py`: varita mágica con contorno, relleno de huecos, "solo la pieza principal", inpainting simple. Sirve para limpiar sprites de Gemini que no vengan perfectos.
- `mago-jardin/tools/synth_garden.py` y `mate-power-up/tools/synth.py`: síntesis chiptune (golpes, pops, aleteos, canto, melodía) sincronizada a tiempos.
- `mago-jardin/tools/dissolve.py`: transición por bloques estilo 16 bits.

### 5.6 Herramientas que convendría construir para el workflow

1. `sheet_to_sprites.py`: magenta → alfa, corte por componentes, detección del tamaño de píxel, ajuste a la grilla, cuantización a la paleta, anclajes, `atlas.json` y hoja de control visual.
2. `proof.py`: arma cada beat del storyboard con el fondo y los sprites (prueba de armado, etapa 6).
3. Un componente HyperFrames `sprite-anim` que lea `atlas.json` y cambie de cuadro por tiempo (en lugar de un `<img>` por cuadro escrito a mano).
4. Una skill de Claude que encadene las etapas 0 a 9 y llame a Gemini con las plantillas de 5.3.
