"""Prepare a HyperFrames project for a pixel reel: slice the sheets, synthesise the audio, copy the runtime.

  python3 assemble.py LIBRARY/sprites.json SHEETS_DIR REEL/reel.json HF_PROJECT_DIR [--cues REEL/cues.json] [--no-quantize]

Writes into HF_PROJECT_DIR/assets/:  pr/ (atlas.js, atlas.json, sprites/, plates/, review/, slice_report.md),
audio/ (sfx.wav, music.wav, ambience.wav), pixel-reel.js, gsap.min.js (copied from a local node_modules if found).
Run placeholders.py first to get an animatic while the real sheets are not ready: same names, drop-in replacement.
"""
import argparse, glob, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); SKILL = os.path.dirname(HERE)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("library"); ap.add_argument("sheets"); ap.add_argument("reel"); ap.add_argument("hf")
    ap.add_argument("--cues"); ap.add_argument("--no-quantize", action="store_true"); a = ap.parse_args()
    assets = os.path.join(a.hf, "assets"); os.makedirs(assets, exist_ok=True)
    cmd = [sys.executable, os.path.join(HERE, "slice_sheets.py"), a.library, a.sheets, os.path.join(assets, "pr"), "--reel", a.reel]
    if a.no_quantize: cmd.append("--no-quantize")
    subprocess.run(cmd, check=True)
    cues = a.cues or os.path.join(os.path.dirname(a.reel), "cues.json")
    if os.path.exists(cues): subprocess.run([sys.executable, os.path.join(HERE, "chiptune.py"), cues, os.path.join(assets, "audio")], check=True)
    shutil.copy(os.path.join(SKILL, "assets", "pixel-reel.js"), assets)
    if not os.path.exists(os.path.join(assets, "gsap.min.js")):
        found = glob.glob(os.path.join(a.hf, "**", "node_modules", "gsap", "dist", "gsap.min.js"), recursive=True) + \
                glob.glob(os.path.join(os.path.dirname(os.path.abspath(a.hf)), "**", "node_modules", "gsap", "dist", "gsap.min.js"), recursive=True)
        if found: shutil.copy(found[0], assets)
        else: print("ojo: falta assets/gsap.min.js (npm i gsap@3.15.0 y copiar dist/gsap.min.js); el render no puede bajarlo de un CDN")
    print("listo:", assets)


if __name__ == "__main__":
    main()
