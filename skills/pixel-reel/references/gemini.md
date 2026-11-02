# Pedirle las hojas al modelo de imagen

`gen_prompts.py` escribe cada prompt completo, con el bloque de estilo, el bloque de hoja, el sujeto y cada cuadro. Este archivo explica cómo usarlos y qué hacer cuando el modelo no cumple.

## Rutina

1. Pedir en el orden de `PROMPTS.md`. Si un paso no está aprobado, no se sigue: todo lo que viene después lo usa como referencia.
2. Adjuntar exactamente lo que dice cada bloque: `palette.png`, el model sheet del personaje y, en la segunda hoja de una animación, la primera.
3. Guardar lo aprobado con el **nombre exacto** en `biblioteca/sheets/`. Así el recorte la usa en lugar de la provisoria.
4. Correr el ensamblado y revisar `review/`. Ahí se ve la línea de ancla roja y la superposición en papel cebolla: si los cuadros no se apilan bien, la hoja vuelve a pedirse.

Cuando hay un límite de uso, conviene pedir primero los P0 y empezar por los model sheets, la maestra y el fondo. Con eso ya se valida que el modelo respeta la grilla.

## Qué revisar al aprobar

- Fondo magenta plano. Si hay sombras o degradé, se pide de nuevo.
- Las 4 celdas respetadas, sin personajes que crucen de celda.
- El mismo tamaño de personaje en todas las celdas. El reporte avisa si la altura difiere más de un 10 % de la pedida.
- Píxeles en bloques parejos. El recorte tolera bordes suaves y una grilla corrida, pero no un cambio de escala dentro de la hoja.
- Sin texto ni números.
- Colores parecidos a la paleta. El recorte cuantiza, pero si el modelo inventa un color nuevo, se va a ver distinto.

## Problemas típicos y cómo pedirlo de nuevo

| Problema | Re-pedido |
|---|---|
| Cambia el diseño del personaje entre hojas | Adjuntar el model sheet y agregar: "identical character design, compare with the attached model sheet before drawing" |
| Tamaños distintos por celda | "the character has exactly the same height in all four cells, {H} image pixels" y adjuntar una hoja aprobada como ejemplo de escala |
| Celdas desordenadas o cuadros de más | Pedir 2 cuadros por hoja (celdas 3 y 4 vacías) |
| Píxeles borrosos o "pintados" | "crisp pixel art, every art pixel is a 4x4 block, no painterly shading, no blur" |
| Sombra sobre el magenta | "no drop shadow, no ground shadow, the background is one flat colour #FF00FF" |
| Texto o firmas | "no text, no letters, no signature anywhere" |
| Objeto en la mano equivocada en W | Pedir la animación en W aparte y marcar `mirror_to_W: false` |

## Generación automática (`gemini_generate.py`)

### Preparar el entorno

- **Clave**: guardarla como variable de entorno `GEMINI_API_KEY` en la configuración del entorno, nunca en el chat ni en un archivo del repo. El SDK la lee sola y el script no la imprime ni la escribe: todo mensaje pasa por un filtro que la reemplaza por `***`.
- **Red**: tiene que permitir `generativelanguage.googleapis.com`.
- **Clave como secreto de red** (alternativa a la variable): en la configuración del entorno, un secreto para `generativelanguage.googleapis.com` con el encabezado `x-goog-api-key`, sin prefijo. El proxy agrega la clave y los scripts usan un valor de relleno, así que la clave no queda nunca a la vista de la sesión.
- **Facturación**: en el plan gratuito, los modelos de imagen tienen cuota 0 (`limit: 0`). Hay que activar la facturación en el proyecto de Google AI Studio. Con cuota 0 el script corta sin reintentar.
- **SDK**: `pip install google-genai`.
- **Verificar sin gastar**: `python3 scripts/gemini_check.py` muestra el largo de la clave, si la API responde y qué modelos de imagen hay.
- **Repo**: ignorar `.env`, `*.key`, `*.pem` y archivos de credenciales, y también `biblioteca/candidates/` (las variantes no aprobadas).

### Modelo

Si no se indica con `--model` o con `PIXEL_REEL_IMAGE_MODEL`, el script le pide a la API la lista de modelos (una llamada gratuita) y elige el primero disponible en este orden: `gemini-3-pro-image-preview` (acepta hasta 14 imágenes de referencia), `gemini-3.1-flash-image-preview` y `gemini-2.5-flash-image`. `--list-models` muestra los disponibles para la clave. Las hojas se piden en `1:1` a `1K`, que da 1024×1024, el formato de las hojas; los fondos se piden en `9:16`.

### Uso

```bash
python3 scripts/gemini_generate.py biblioteca/sprites.json --reel <reel>/reel.json --gate 2 --dry-run
```

```bash
python3 scripts/gemini_generate.py biblioteca/sprites.json --reel <reel>/reel.json --gate 2 --variants 3 --max-images 6
```

```bash
python3 scripts/gemini_generate.py biblioteca/sprites.json --approve mago_model.png=2
```

```bash
python3 scripts/gemini_generate.py biblioteca/sprites.json --reel <reel>/reel.json --gate 5 --variants 2 --max-images 30
```

| Opción | Qué hace |
|---|---|
| `--reel` | Solo lo que necesita ese reel |
| `--gate N` / `--only a.png,b.png` | Limitar a un gate o a hojas puntuales |
| `--variants N` | Variantes por hoja (3 para los gates 2 a 4; 2 alcanza para el 5) |
| `--max-images N` | Tope de imágenes pedidas por corrida, incluidos los re-pedidos y los errores |
| `--fix-rounds N` | Re-pedidos con correcciones en el gate 5 si ninguna variante pasa (por defecto 1) |
| `--dry-run` | Muestra qué pediría, con qué adjuntos y cuántas imágenes. No llama a la API ni necesita clave |
| `--approve HOJA=N` | Aprueba una variante a mano y la copia a `sheets/` |
| `--regen` | Vuelve a pedir una hoja que ya tiene variantes esperando elección |
| `--image-size 1K/2K/4K`, `--model`, `--list-models`, `--retries` | Avanzadas |

### Reglas

- **Dependencias**: una hoja solo se pide si sus adjuntos ya están aprobados (model sheet, imagen maestra, parte 1, fotos). Si no, sale como "bloqueada" y no gasta.
- **Gates 2 a 4**: nunca se aprueban solos. El script deja `candidates/<hoja>/contact.png` con las variantes, su puntaje y sus problemas, y espera `--approve`.
- **Gate 5**: se aprueba sola la variante con mejor puntaje si pasa el control de calidad. Si ninguna pasa, se vuelve a pedir agregando al prompt las correcciones de cada problema (la tabla de arriba). La hoja de contacto queda igual para revisarla.
- **Límites de uso y errores del servidor** (429 y 5xx): reintenta con esperas de 8, 16, 32 s y así.
- **Log**: `biblioteca/generation_log.jsonl` registra por cada pedido la fecha, la hoja, el gate, el modelo, la variante, la ronda, el prompt completo con su hash, los adjuntos, el control de calidad y las aprobaciones (a mano o automáticas). Nunca la clave.

## Seguridad de marca

Para productos de terceros (personajes de videojuegos, consolas, escudos), pedir el objeto **sin logos ni texto**. La silueta y los colores alcanzan para reconocerlo.
