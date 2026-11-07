#!/usr/bin/env bash
# Builds skills/reel-3d-toon.skill (upload it in claude.ai to use the skill outside this repo). The package carries a
# snapshot of the scripts (scripts/) and the reference scene (assets/escena-ejemplo.html); the canonical copies stay in
# videos/biblioteca and videos/papa-noel-en-ojotas.
set -e
cd "$(dirname "$0")/../.."
T=$(mktemp -d); P=$T/reel-3d-toon; mkdir -p $P/scripts $P/assets
cp skills/reel-3d-toon/SKILL.md $P/; cp -r skills/reel-3d-toon/references $P/
cp videos/biblioteca/3d/toonchar.py videos/biblioteca/3d/web/toon3d.js videos/biblioteca/3d/web/qa3d.cjs videos/biblioteca/3d/web/frames3d.cjs \
   videos/biblioteca/3d/web/flicker_scan.py videos/biblioteca/tts_lineas.py videos/biblioteca/check_voces.py $P/scripts/
cp videos/papa-noel-en-ojotas/hf3d/index.html $P/assets/escena-ejemplo.html
cp videos/papa-noel-en-ojotas/build3d.sh $P/assets/build3d-ejemplo.sh; cp videos/papa-noel-en-ojotas/voces3d.json $P/assets/voces-ejemplo.json
rm -f skills/reel-3d-toon.skill; (cd $T && zip -qr - reel-3d-toon) > skills/reel-3d-toon.skill; rm -rf $T
unzip -l skills/reel-3d-toon.skill | tail -1
