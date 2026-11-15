#!/usr/bin/env bash
# "El laberinto" (3D toon, November wave 2, W3): copies three.js, the shared kit (toon3d.js + escena3d.js), the character and printer
# GLBs, the fonts (Fredoka for text, Caveat for the hand-lettered tags and notes) and the voices into hf3d/ (not
# versioned), makes the talk envelopes and synthesises music, effects and ambience from cues.json.
set -e
cd "$(dirname "$0")"
THREE=${THREE:-/opt/three/node_modules/three}
[ -d "$THREE" ] || (mkdir -p /opt/three && cd /opt/three && npm init -y >/dev/null && npm install three@0.170.0)
F=/opt/fonts/node_modules/@fontsource
[ -d "$F/fredoka" ] && [ -d "$F/caveat" ] || (mkdir -p /opt/fonts && cd /opt/fonts && npm init -y >/dev/null && npm install @fontsource/fredoka@5.1.1 @fontsource/caveat@5.1.0)
rm -f hf3d/assets/voz/*.wav
mkdir -p hf3d/lib/addons/loaders hf3d/lib/addons/utils hf3d/lib/addons/geometries hf3d/assets/fonts hf3d/assets/voz
cp "$THREE/build/three.module.js" hf3d/lib/
cp "$THREE/examples/jsm/loaders/GLTFLoader.js" hf3d/lib/addons/loaders/
cp "$THREE/examples/jsm/utils/BufferGeometryUtils.js" hf3d/lib/addons/utils/
cp "$THREE/examples/jsm/geometries/RoundedBoxGeometry.js" hf3d/lib/addons/geometries/
cp ../papa-noel-en-ojotas/hf/assets/gsap.min.js hf3d/lib/
cp ../biblioteca/3d/web/toon3d.js ../biblioteca/3d/web/escena3d.js ../biblioteca/3d/web/ajedrez3d.js ../biblioteca/3d/web/grecia3d.js hf3d/lib/
cp ../biblioteca/3d/glb/mago.glb ../biblioteca/3d/glb/santa.glb ../biblioteca/3d/glb/printer.glb hf3d/assets/
cp "$F/fredoka/files/fredoka-latin-700-normal.woff2" hf3d/assets/fonts/fredoka-700.woff2
cp "$F/fredoka/files/fredoka-latin-600-normal.woff2" hf3d/assets/fonts/fredoka-600.woff2
cp "$F/caveat/files/caveat-latin-700-normal.woff2" hf3d/assets/fonts/caveat-700.woff2
for f in voz/[sm][0-9].wav; do cp "$f" hf3d/assets/voz/; done
# the real product photos (the site's own, assets/p): the "Así son de verdad" proof (the chess sets)
mkdir -p hf3d/assets/p && for p in grecia; do cp ../../assets/p/$p.webp hf3d/assets/p/; done
python3 - <<'PY'
import glob, json, os, subprocess, numpy as np
env = {}
for f in sorted(glob.glob("hf3d/assets/voz/*.wav")):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-loglevel", "error", "-i", f, "-ac", "1", "-ar", "48000", "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32)
    hop = 800; n = len(x) // hop; r = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)); r = r / max(1e-6, np.percentile(r, 95))
    y = np.zeros(n); v = 0.0
    for i, a in enumerate(np.clip(r, 0, 1)): v = a if a > v else v * 0.8; y[i] = v
    y = np.convolve(np.pad(y, 2, mode='edge'), [0.1, 0.2, 0.4, 0.2, 0.1], 'valid')   # no one-frame head snaps on laughs and plosives (flicker scan, 'Vikingo o caballero' 16.7 s)
    env[os.path.basename(f)[:-4]] = [round(float(a), 3) for a in y]
json.dump(env, open("hf3d/assets/voz/env.json", "w"))
PY
python3 ../../skills/pixel-reel/scripts/chiptune.py cues.json hf3d/assets/audio
echo ok
# QA gate: cd hf3d && python3 -m http.server 8782 &  then  node ../../biblioteca/3d/web/qa3d.cjs 8782 qa.json
# Render:  cd hf3d && npx hyperframes render --fps 60 --workers 4 -o ../el-laberinto.mp4
