#!/usr/bin/env python3
"""Re-scores one finished reel without touching its picture (videos/AUDIT_MUSICA.md).
  python3 rehacer_audio.py REEL [--swap]
1. runs REEL/musica.py (writes hf3d/assets/audio/music.wav and sfx.wav);
2. sets the page's music volume so the bed sits about 22 dB under the voices while they speak (nivel_musica.py);
3. remezclar.py -> a new mp4 in the scratchpad, picture stream byte-identical (md5 checked), about -14 LUFS;
4. prints the levels, the loudness, the steady-buzz test; with --swap, replaces REEL/REEL.mp4 (or the mp4s the page renders to)."""
import os, re, subprocess, sys, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); VIDEOS = os.path.dirname(HERE)
SCR = os.environ.get("SCRATCH", "/tmp/claude-0/-home-user-Creaciones-del-mago/a1980014-4b5c-5dd5-b5b7-e1635c566019/scratchpad")
reel = sys.argv[1]; swap = "--swap" in sys.argv; R = os.path.join(VIDEOS, reel)
TARGET = float(os.environ.get("BED_DB", "-22"))
def run(*a, **k): return subprocess.run(list(a), capture_output=True, text=True, **k)
def level(hf3d):
    o = run("python3", os.path.join(HERE, "nivel_musica.py"), hf3d).stdout.strip().splitlines()[-1]
    m = re.search(r"under voices (-?[0-9.]+) dB \| music in the gaps (-?[0-9.]+)", o); return float(m.group(1)), float(m.group(2)), o
def vmd5(p): return hashlib.md5(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-map", "0:v", "-c", "copy", "-f", "rawvideo", "-"], capture_output=True).stdout).hexdigest()[:12]
jobs = [(os.path.join(R, "hf3d"), os.path.join(R, reel + ".mp4"))]
if reel == "papa-noel-en-ojotas": jobs = [(os.path.join(R, "hf3d"), os.path.join(R, "papa-noel-en-ojotas-3d.mp4")), (os.path.join(R, "hf3d-v2"), os.path.join(R, "papa-noel-en-ojotas-3d-v2.mp4"))]
r = run("python3", os.path.join(R, "musica.py"), cwd=R); print(r.stdout.strip()[-300:], r.stderr.strip()[-800:])
for hf3d, mp4 in jobs:
    if hf3d != jobs[0][0]:                                                  # a second edit of the same reel (the Christmas V2) shares the stems
        for s in ("music.wav", "sfx.wav", "ambience.wav"):
            src = os.path.join(jobs[0][0], "assets", "audio", s)
            if os.path.exists(src): subprocess.run(["cp", src, os.path.join(hf3d, "assets", "audio", s)])
    page = os.path.join(hf3d, "index.html"); html = open(page, encoding="utf-8").read()
    mv = float(re.search(r'id="aud-music"[^>]*data-volume="([0-9.]+)"', html).group(1))
    under, gaps, _ = level(hf3d); nv = round(min(1.0, max(0.12, mv * 10 ** ((TARGET - under) / 20))), 3)
    html = re.sub(r'(id="aud-music"[^>]*data-volume=")[0-9.]+(")', lambda m: m.group(1) + str(nv) + m.group(2), html); open(page, "w", encoding="utf-8").write(html)
    under, gaps, line = level(hf3d); print(os.path.basename(hf3d), "music volume", mv, "->", nv, "|", line)
    out = os.path.join(SCR, os.path.basename(mp4).replace(".mp4", "_new.mp4"))
    print(run("python3", os.path.join(HERE, "remezclar.py"), hf3d, mp4, out).stdout.strip().splitlines()[-1])
    eb = run("ffmpeg", "-nostats", "-i", out, "-af", "ebur128=peak=true", "-f", "null", "-").stderr
    I = re.findall(r"I:\s+(-?[0-9.]+) LUFS", eb)[-1]; P = re.findall(r"Peak:\s+(-?[0-9.]+) dBFS", eb)[-1]
    same = vmd5(mp4) == vmd5(out); bz = run("python3", os.path.join(SCR, "buzz.py"), out).stdout.strip()
    print(f"  {I} LUFS, peak {P} dBFS, picture identical: {same} | {bz}")
    if swap and same: subprocess.run(["cp", out, mp4]); print("  swapped ->", mp4)
