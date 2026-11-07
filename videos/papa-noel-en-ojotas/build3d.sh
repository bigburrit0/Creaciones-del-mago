#!/usr/bin/env bash
# 3D toon version of the reel: copies three.js, the shared toon3d.js and the character/prop GLBs into hf3d/ (not versioned).
set -e
cd "$(dirname "$0")"
THREE=${THREE:-/opt/three/node_modules/three}
[ -d "$THREE" ] || (mkdir -p /opt/three && cd /opt/three && npm init -y >/dev/null && npm install three@0.170.0)
mkdir -p hf3d/lib/addons/loaders hf3d/lib/addons/utils hf3d/lib/addons/geometries hf3d/assets
cp "$THREE/build/three.module.js" hf3d/lib/
cp "$THREE/examples/jsm/loaders/GLTFLoader.js" hf3d/lib/addons/loaders/
cp "$THREE/examples/jsm/utils/BufferGeometryUtils.js" hf3d/lib/addons/utils/
cp "$THREE/examples/jsm/geometries/RoundedBoxGeometry.js" hf3d/lib/addons/geometries/
cp hf/assets/gsap.min.js hf3d/lib/
cp ../biblioteca/3d/web/toon3d.js hf3d/lib/
cp ../biblioteca/3d/glb/mago.glb ../biblioteca/3d/glb/santa.glb ../biblioteca/3d/glb/printer.glb hf3d/assets/
python3 ../../skills/pixel-reel/scripts/chiptune.py cues3d.json hf3d/assets/audio
# subtitles font (Fredoka, OFL) and the voices (voz3d/, made with ../biblioteca/tts_lineas.py voces3d.json voz3d)
FONTS=${FONTS:-/opt/fonts/node_modules/@fontsource/fredoka/files}
[ -d "$FONTS" ] || (mkdir -p /opt/fonts && cd /opt/fonts && npm init -y >/dev/null && npm install @fontsource/fredoka@5.1.1)
mkdir -p hf3d/assets/fonts hf3d/assets/voz
cp "$FONTS/fredoka-latin-700-normal.woff2" hf3d/assets/fonts/fredoka-700.woff2
cp "$FONTS/fredoka-latin-600-normal.woff2" hf3d/assets/fonts/fredoka-600.woff2
for f in voz3d/[sm][0-9].wav; do cp "$f" hf3d/assets/voz/; done
python3 - <<'PY'
# loudness envelope of each line at 60 fps (drives the head nods while a character talks)
import glob, json, os, subprocess, numpy as np
env = {}
for f in sorted(glob.glob("hf3d/assets/voz/*.wav")):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-loglevel", "error", "-i", f, "-ac", "1", "-ar", "48000", "-f", "f32le", "-"],
                                     capture_output=True, check=True).stdout, np.float32)
    hop = 800; n = len(x) // hop; r = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)); r = r / max(1e-6, np.percentile(r, 95))
    y = np.zeros(n); v = 0.0
    for i, a in enumerate(np.clip(r, 0, 1)): v = a if a > v else v * 0.8; y[i] = v      # fast attack, ~80 ms release
    env[os.path.basename(f)[:-4]] = [round(float(a), 3) for a in y]
json.dump(env, open("hf3d/assets/voz/env.json", "w"))
print("voices:", {k: len(v) for k, v in env.items()})
PY
# V2 (same scene and sound, new camera and editing) shares the built libs and assets
mkdir -p hf3d-v2 && rm -rf hf3d-v2/lib hf3d-v2/assets && cp -r hf3d/lib hf3d/assets hf3d-v2/
echo ok
# QA gate (run before rendering): cd hf3d && python3 -m http.server 8768 &  then  node ../../biblioteca/3d/web/qa3d.cjs 8768 qa.json
# Render: cd hf3d && npx hyperframes render --fps 60 --workers 4 -o ../papa-noel-en-ojotas-3d.mp4
