# Animar con pixel-reel.js

El runtime está en `assets/pixel-reel.js` y lo copia `assemble.py`. Cada sprite es una tira PNG ya escalada ×4, descrita en `atlas.js`. Un **actor** es un `<div class="act">` del HTML: el runtime le cambia la tira y la posición del fondo con `tl.set`, así que los cuadros saltan como en un juego de 16 bits. Todo depende del tiempo de la línea de tiempo, de modo que se puede saltar a cualquier punto sin que cambie el resultado.

## Reglas de movimiento (v2, "smooth"; ver `videos/RESEARCH_PIXEL_REELS.md`)

- Los **cuadros** del sprite cambian por pasos (8 a 12 fps), pero la **posición** se interpola en cada cuadro de video y se ajusta a la grilla de píxeles de arte. Es el modo por defecto (`smooth: true`); `smooth: false` vuelve al movimiento escalonado viejo.
- Los fps del sprite se redondean a un divisor de los fps del video (`videoFps`, 60 por defecto): 10, 12, 15 o 20. Así cada cuadro dura lo mismo. Con 8 fps en 30, los cuadros alternan 4-3-4-3 y el movimiento tiembla.
- Renderizar a **60 fps**: `npx hyperframes render --fps 60`.
- `walk` va a velocidad constante con un suavizado corto al arrancar y al frenar. `arc` y `hops` siguen parábolas reales. `pop` usa un rebote elástico.
- Sombras en el piso: `R.actor(sel, key, x, y, { shadow: "#id-sombra" })` con un `<div class="csh">`. La sombra sigue al personaje en x y se queda en el piso cuando salta.
- Luz y profundidad: `scripts/draw_light.py` genera el haz de luz de la ventana, las sombras de contacto, la viñeta y la sombra de los personajes, a partir de `reel.json` → `lighting`. Todo va con dithering ordenado y colores de la paleta, sin difuminados.

## Inicio

```html
<script src="assets/gsap.min.js"></script>
<script src="assets/pixel-reel.js"></script>
<script src="assets/pr/atlas.js"></script>
...
const tl = gsap.timeline({ paused: true });
const R = PixelReel(tl, window.PR_ATLAS, { base: "assets/pr/", fxPool: ["#fx1", "#fx2", "..."] });
```

## API (posiciones en píxeles de arte de la grilla 270×480)

| Llamada | Qué hace | Devuelve |
|---|---|---|
| `R.actor(sel, key, x, y, {scale, flip, shadow, cast})` | Crea un actor con su sprite inicial, con el ancla en (x, y). `shadow`: elipse en el piso que lo sigue (personajes). `cast`: sombra proyectada de un sprite 3D (tira `<key>.shadow`), con los mismos cuadros | actor |
| `a.play(t, key, {dur, fps, frames, reverse, flip, mode})` | Reproduce una animación. Si es un bucle, `dur` dice cuánto dura | tiempo de fin |
| `a.frame(t, key, i)` | Pone un cuadro fijo (estados de objetos) | t |
| `a.walk(t, dur, x, y, key, {flip})` | Camina hasta (x, y) en pasos mientras corre el bucle | fin |
| `a.moveTo(t, dur, x, y, steps)` | Movimiento recto por pasos | fin |
| `a.hops(t, dur, x, y, n, h)` | n saltitos de altura h, con aplaste al aterrizar | fin |
| `a.arc(t, dur, x, y, h, steps)` | Vuelo en parábola por pasos (ítems lanzados, pájaros) | fin |
| `a.pop(t, from)` | Aplastar y estirar (aparecer, aterrizar, sentarse) | fin |
| `a.shake(t, dur, amp)` | Temblor | fin |
| `a.show(t)`, `a.hide(t)`, `a.z(t, z)`, `a.place(t, x, y)` | Visibilidad, orden de pintado y posición | t |
| `R.fx(t, key, x, y, {loop, dur})` | Efecto de un solo uso, tomado del pool | fin |
| `R.dissolve(t, [sel...], step)` | Disolución por bloques: muestra cuadros a pantalla completa en secuencia | fin |

Reglas:
- **Escribir las llamadas de cada actor en orden de tiempo**: los movimientos recuerdan dónde terminó el anterior.
- Para la dirección W se usa `flip: true` sobre la animación E. El espejo se hace sobre el ancla (los pies).
- Para los ítems chicos, `scale: 0.5` (bloques de 2×2, sigue siendo pixel art).
- Sprites renderizados desde 3D (`pixelize3d.py`): la sombra proyectada va en un `<div class="cs3d">` aparte con `mix-blend-mode: multiply` y `opacity` ~0.6, debajo de los personajes, pasado como `{ cast: "#id" }`.
- El orden de pintado va por `z-index` en el CSS. Para pasar por detrás de algo, se cambia con `a.z(t, n)` en el momento justo, por ejemplo cuando un personaje se va hacia el fondo.

## Recetas

- **Entrada**: `door.play(0, "obj.door", {frames:[0,1,2], fps:12})`, después el personaje con `show` y `walk`.
- **Sorpresa**: `play(t, "x.surprised_S")` queda en el último cuadro. Sumar `R.fx` de sudor o destello.
- **Item get**: `play(t, "x.item_get_S")`. El ítem es otro actor puesto sobre las manos (`hands = pies - 90 px de arte`) que aparece en el cuadro 2. Después `toss_E` y `item.arc(...)` hasta el destino.
- **Ráfaga**: varios ítems con `arc` separados por 0,1 s y un `pop` por cada uno en el sonido.
- **Estados de un objeto que crece** (bolsa, planta): `frame(t, "obj.bolsa", k)` más `pop` en cada cambio.
- **Ambiente**: los bucles largos (`play(0, "obj.fan", {dur: 15})`) van al principio del script.
- **Final tranquilo**: dejar quieto el último 0,4 a 1 s.
- **Cambio de escenario**: evitarlo. Si es inevitable, usar disolución por bloques de 0,5 s.

## Composición base

`assets/reel-template.html` trae el escenario, los actores de ejemplo, el pool de efectos y las tres pistas de audio. Copiarlo a `hf/index.html` y escribir la línea de tiempo siguiendo los beats de `reel.json`.
