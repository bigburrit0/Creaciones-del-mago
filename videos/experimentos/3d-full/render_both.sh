#!/usr/bin/env bash
# Renders the fully-3D test twice: smooth toon 3D and 3D-as-pixel-art (same scene, same motion).
set -e
cd "$(dirname "$0")/hf"
echo 'window.MODE = "toon";' > mode.js;  npx hyperframes render --fps 60 -o ../3d-toon.mp4
echo 'window.MODE = "pixel";' > mode.js; npx hyperframes render --fps 60 -o ../3d-pixel.mp4
echo 'window.MODE = "toon";' > mode.js
