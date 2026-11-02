# Biblia de estilo (por defecto)

Valores por defecto de la skill. Cada proyecto puede cambiarlos en `sprites.json` (`project.style`, `grid`, `sheet_formats`), pero conviene no tocarlos: todo el pipeline está pensado para que el píxel del modelo de imagen caiga 1:1 en el video.

## Grilla

| Qué | Valor |
|---|---|
| Video | 1080×1920, 30 fps |
| Grilla de arte | 270×480 píxeles de arte; cada uno es un bloque de 4×4 del video |
| Escala | ×4 entera, siempre con vecino más cercano. Nunca reescalar un sprite a un porcentaje no entero (0,5 está bien para objetos chiquitos: queda en bloques de 2×2) |
| Cámara | Fija, cenital a tres cuartos. Un reel = un escenario |
| Animación | Por pasos, 8 fps por defecto (4 para respiración, 10-12 para cosas rápidas) |

## Tamaños y anclas

| Elemento | Altura en px de arte | Celda | Ancla |
|---|---|---|---|
| Personaje principal | ~96 | 128×128 | pies en (64, 124) |
| Otros personajes | 84-96 | 128×128 | pies en (64, 124) |
| Animales chicos, efectos, objetos chicos | 8-40 | 64×64 | centro (32, 32) |
| Ítems (productos) | hasta 40 | 128×128 (hoja de ítems) | base en (64, 84) |
| Objetos con estados (puerta, máquina, bolsa) | según el objeto | 128×128 | base en (64, 124) |

El recorte mueve cada hoja para que la mediana de los pies quede en el ancla. Como el desplazamiento es el mismo para toda la hoja, los saltos conservan su altura.

## Hojas para el modelo de imagen

- 1024×1024 PNG, fondo magenta puro `#FF00FF` que llene todo, sin sombra sobre el fondo, sin piso, sin texto, sin bordes ni líneas de grilla.
- **Personajes y objetos con estados**: grilla 2×2 de celdas de 512 px (128 px de arte ×4), hasta 4 cuadros por hoja, leídos de izquierda a derecha y de arriba abajo. Las animaciones de 5 a 8 cuadros van en 2 hojas; la segunda se pide adjuntando la primera.
- **Efectos y objetos chicos**: grilla 4×4 de celdas de 256 px; cada fila es una animación de hasta 4 cuadros.
- **Ítems**: grilla 2×2, un producto por celda, de hasta 40 px de arte (160 px de imagen).
- **Fondos**: 9:16, la escena completa a 270×480 px de arte.

## Paleta, luz y contorno

- Una paleta de 24 a 32 colores por proyecto (`project.style.palette`), que se adjunta como `palette.png` en cada prompt. El recorte cuantiza todo a esa paleta.
- Ningún color de sprite cerca del magenta: los violetas tienen que ser azulados.
- Contorno oscuro de 1 px de arte en todos los sprites, sin antialiasing.
- Luz desde arriba a la izquierda y 3 tonos por material.
- Dither solo en los fondos.
- La sombra en el piso no va en el sprite (si hace falta, se dibuja aparte), para que no salte con los saltos.

## Direcciones

`S` de frente a tres cuartos (la de siempre), `E` perfil a la derecha, `N` de espaldas, `W` = `E` espejado. Los objetos en la mano van siempre en la mano derecha. Si al espejar el objeto cambia de mano y se nota, esa animación se pide en `W` aparte (`mirror_to_W: false`).

## Orden de aprobación

1. Paleta (la genera `gen_prompts.py`).
2. Model sheets: cada personaje de frente, perfil y espalda, más una pose característica.
3. Imagen maestra del escenario, con el personaje principal para dar escala.
4. Fondo vacío: la misma imagen sin personajes ni adornos de temporada.
5. Animaciones, objetos, efectos e ítems.

Lo aprobado se adjunta como referencia en todo lo que viene después. Es la principal herramienta de consistencia.
