#!/usr/bin/env bash
# Copies libraries and models into hf/ (not versioned). Models come from videos/biblioteca/3d (mago3d.py, taller_props.py).
set -e
cd "$(dirname "$0")"
THREE=${THREE:-/opt/three/node_modules/three}
[ -d "$THREE" ] || (mkdir -p /opt/three && cd /opt/three && npm init -y >/dev/null && npm install three@0.170.0)
mkdir -p hf/lib/addons/loaders hf/lib/addons/utils hf/assets
cp "$THREE/build/three.module.js" hf/lib/
cp "$THREE/examples/jsm/loaders/GLTFLoader.js" hf/lib/addons/loaders/
cp "$THREE/examples/jsm/utils/BufferGeometryUtils.js" hf/lib/addons/utils/
cp ../../papa-noel-en-ojotas/hf/assets/gsap.min.js hf/lib/
cp ../../biblioteca/3d/glb/mago.glb ../../biblioteca/3d/glb/printer.glb hf/assets/
echo "ok"
