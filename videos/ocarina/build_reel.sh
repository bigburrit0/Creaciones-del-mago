#!/usr/bin/env bash
# Shared build for the four ocarina reels (../PLAN_OCARINA.md). Usage, from a reel folder: bash ../ocarina/build_reel.sh "a1 a2 a3" "oda chirrido"
# Copies three.js, the kit (toon3d, escena3d, ocarina3d), the GLBs, fonts, the reel's voices (from ../ocarina/voz) and its
# synthesised ocarina phrases (from ../ocarina/sonido, made by biblioteca/ocarina_synth.py), makes the talk envelopes and
# synthesises the ambient bed and effects from cues.json (run cues.py first).
set -e
IDS="$1"; PHR="$2"
THREE=${THREE:-/opt/three/node_modules/three}
[ -d "$THREE" ] || (mkdir -p /opt/three && cd /opt/three && npm init -y >/dev/null && npm install three@0.170.0)
F=/opt/fonts/node_modules/@fontsource
[ -d "$F/fredoka" ] && [ -d "$F/caveat" ] || (mkdir -p /opt/fonts && cd /opt/fonts && npm init -y >/dev/null && npm install @fontsource/fredoka@5.1.1 @fontsource/caveat@5.1.0)
rm -rf hf3d/assets/voz hf3d/assets/oca; mkdir -p hf3d/lib/addons/loaders hf3d/lib/addons/utils hf3d/lib/addons/geometries hf3d/assets/fonts hf3d/assets/voz hf3d/assets/oca
cp "$THREE/build/three.module.js" hf3d/lib/
cp "$THREE/examples/jsm/loaders/GLTFLoader.js" hf3d/lib/addons/loaders/
cp "$THREE/examples/jsm/utils/BufferGeometryUtils.js" hf3d/lib/addons/utils/
cp "$THREE/examples/jsm/geometries/RoundedBoxGeometry.js" hf3d/lib/addons/geometries/
[ -f /opt/three/node_modules/gsap/dist/gsap.min.js ] || (cd /opt/three && npm install gsap@3.12.5 >/dev/null)
cp /opt/three/node_modules/gsap/dist/gsap.min.js hf3d/lib/
cp ../biblioteca/3d/web/toon3d.js ../biblioteca/3d/web/escena3d.js ../biblioteca/3d/web/ocarina3d.js hf3d/lib/
cp ../biblioteca/3d/glb/mago.glb ../biblioteca/3d/glb/santa.glb ../biblioteca/3d/glb/printer.glb hf3d/assets/
cp "$F/fredoka/files/fredoka-latin-700-normal.woff2" hf3d/assets/fonts/fredoka-700.woff2
cp "$F/fredoka/files/fredoka-latin-600-normal.woff2" hf3d/assets/fonts/fredoka-600.woff2
cp "$F/caveat/files/caveat-latin-700-normal.woff2" hf3d/assets/fonts/caveat-700.woff2
for i in $IDS; do cp ../ocarina/voz/$i.wav hf3d/assets/voz/; done
# the ocarina: loudness-matched to about -19 LUFS (the voices sit at -16), notes files for the holes
for p in $PHR; do ffmpeg -loglevel error -y -i ../ocarina/sonido/$p.wav -af loudnorm=I=-19:TP=-3:LRA=7,aresample=48000 -ar 48000 hf3d/assets/oca/$p.wav; cp ../ocarina/sonido/$p.json hf3d/assets/oca/; done
python3 - <<'PY'
import glob, json, os, subprocess, numpy as np
env = {}
for f in sorted(glob.glob("hf3d/assets/voz/*.wav")):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-loglevel", "error", "-i", f, "-ac", "1", "-ar", "48000", "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32)
    hop = 800; n = len(x) // hop; r = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)); r = r / max(1e-6, np.percentile(r, 95))
    y = np.zeros(n); v = 0.0
    for i, a in enumerate(np.clip(r, 0, 1)): v = a if a > v else v * 0.8; y[i] = v
    y = np.convolve(np.pad(y, 2, mode='edge'), [0.1, 0.2, 0.4, 0.2, 0.1], 'valid')
    env[os.path.basename(f)[:-4]] = [round(float(a), 3) for a in y]
json.dump(env, open("hf3d/assets/voz/env.json", "w"))
PY
python3 ../../skills/pixel-reel/scripts/chiptune.py cues.json hf3d/assets/audio
echo ok
