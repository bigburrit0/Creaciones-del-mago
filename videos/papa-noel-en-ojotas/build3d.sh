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
echo ok
