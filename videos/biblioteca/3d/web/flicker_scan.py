#!/usr/bin/env python3
"""Image-based glitch check on a RENDERED reel: a frame unlike both neighbours while the neighbours look alike is a
flicker (a one-frame pose pop, a prop teleport, a T-pose). Camera cuts are excluded.

  python3 flicker_scan.py video.mp4 [--cuts 3.2,8.0,12.5] [--fps 60]     exit 1 if any flicker frame
"""
import argparse, subprocess, sys
import numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("--cuts", default=""); ap.add_argument("--fps", type=float, default=60)
a = ap.parse_args(); W, H = 135, 240
raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", a.video, "-vf", f"scale={W}:{H},format=gray", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
F = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32); n = len(F)
cuts = [float(x) for x in a.cuts.split(",") if x]
d = lambda i, j: float(np.abs(F[i] - F[j]).mean())
bad = []
for i in range(1, n - 1):
    t = i / a.fps
    if any(abs(t - c) < 0.05 for c in cuts): continue
    x, y, z = d(i - 1, i), d(i, i + 1), d(i - 1, i + 1)
    if x > 3 and y > 3 and z < 0.5 * min(x, y): bad.append((round(t, 3), round(x, 2), round(y, 2), round(z, 2)))
print(f"{n} frames, {len(bad)} flicker frames", bad[:20])
sys.exit(1 if bad else 0)
