# Mago en el jardín (video vertical 10 s)

Video 1080×1920, 30 fps, hecho con [HyperFrames](https://hyperframes.heygen.com) a partir de los 4 keyframes de `keyframes/` (numerados en el orden de la acción: 1 semilla, 2 arbolito, 3 comedero, 4 mago sentado).

- `mago-jardin.mp4`: el video final.
- `index.html`: la composición de HyperFrames (línea de tiempo GSAP).
- `tools/build_garden.py`: arma el fondo limpio del patio, recorta los sprites (por diferencia entre los keyframes 1 a 3 y con "varita mágica" sobre el contorno en el keyframe 4) y genera el brote y el arbolito intermedios.
- `tools/dissolve.py`: genera los cuadros de la disolución por bloques hacia el keyframe 4.
- `tools/synth_garden.py`: sintetiza el audio chiptune (efectos, melodía y pájaros de fondo).
- `tools/garden_lib.py`: utilidades compartidas.

Los keyframes 1 a 3 comparten el mismo patio, pero el 4 tiene otro diseño (pasto, cerca alta, árbol grande). Por eso, entre los 7,4 s y los 8 s la escena pasa al keyframe 4 con una disolución por bloques al estilo 16 bits.

Para regenerar (requiere numpy y Pillow):

```bash
npx hyperframes@0.9.3 init garden --resolution portrait --non-interactive
python3 tools/build_garden.py keyframes garden/assets
python3 tools/dissolve.py garden/assets 8
python3 tools/synth_garden.py garden/assets
cp index.html garden/
cp node_modules/gsap/dist/gsap.min.js garden/assets/   # gsap@3.15.0 (npm i gsap@3.15.0)
cd garden && npx hyperframes render -o mago-jardin.mp4
```
