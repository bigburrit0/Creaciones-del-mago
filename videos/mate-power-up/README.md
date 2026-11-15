# Mate power-up (video vertical 10 s)

Video 1080×1920, 30 fps, hecho con [HyperFrames](https://hyperframes.heygen.com) a partir de los 4 keyframes de `keyframes/`.

- `mate-power-up.mp4`: el video final.
- `index.html`: la composición de HyperFrames (línea de tiempo GSAP).
- `tools/build_assets.py`: recorta los sprites (manija gris, manija dorada, vapor, gaviotas) y arma las bases intermedias y los cuadros de olas a partir de los keyframes.
- `tools/synth.py`: sintetiza los efectos chiptune (golpe, cuenta regresiva, arpegio + clic, acorde de victoria, olas, gaviotas).

Para regenerar:

```bash
npx hyperframes@0.9.3 init mate --resolution portrait --non-interactive
python3 tools/build_assets.py keyframes mate/assets
python3 tools/synth.py mate/assets
cp index.html mate/
cp node_modules/gsap/dist/gsap.min.js mate/assets/   # gsap@3.15.0 (npm i gsap@3.15.0)
cd mate && npx hyperframes render -o mate-power-up.mp4
```

`build_assets.py` necesita numpy y Pillow.
