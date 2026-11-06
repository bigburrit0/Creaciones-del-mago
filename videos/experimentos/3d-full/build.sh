#!/usr/bin/env bash
# Copies the libraries and models the fully-3D test needs into hf/ (not versioned: big, and all re-downloadable).
#   three.js 0.170.0 (MIT, npm), Quaternius Universal Animation Library (CC0, github.com/J-Ponzo/gltf-universal-animation-library),
#   printer.glb exported from videos/biblioteca/3d/taller_props.py (PIXEL3D_GLB=... ).
set -e
cd "$(dirname "$0")"
THREE=${THREE:-/opt/three/node_modules/three}
UAL=${UAL:-/opt/assets3d/ual/glTF}
[ -d "$THREE" ] || (mkdir -p /opt/three && cd /opt/three && npm init -y >/dev/null && npm install three@0.170.0)
[ -d "$UAL" ] || git clone --depth 1 https://github.com/J-Ponzo/gltf-universal-animation-library.git /opt/assets3d/ual
mkdir -p hf/lib/addons/loaders hf/lib/addons/utils hf/assets
cp "$THREE/build/three.module.js" hf/lib/
cp "$THREE/examples/jsm/loaders/GLTFLoader.js" hf/lib/addons/loaders/
cp "$THREE/examples/jsm/utils/BufferGeometryUtils.js" hf/lib/addons/utils/
cp ../../papa-noel-en-ojotas/hf/assets/gsap.min.js hf/lib/ 2>/dev/null || cp "$(npm root -g)/gsap/dist/gsap.min.js" hf/lib/
cp "$UAL/AnimationLibrary_Godot_Standard.gltf" "$UAL/AnimationLibrary_Godot_Standard.bin" hf/assets/
cp ../../biblioteca/3d/glb/printer.glb hf/assets/
echo "ok: hf/lib, hf/assets"
