#!/usr/bin/env python3
"""Rebuild a rendered reel's audio from its page and swap it in, without re-rendering the picture.

  python3 remezclar.py HF3D_DIR VIDEO_IN VIDEO_OUT [--lufs -14]

Reads every <audio class="clip"> in HF3D_DIR/index.html (src, data-start, data-duration, data-volume) and sums them as
HyperFrames does (checked on "Un regalo para cada amigo": a plain sum correlates 0.986 with the rendered track, which
HyperFrames then brings to about -14 LUFS). The sum is measured (loudnorm), brought to the target by a plain gain and a gentle peak limiter (-1.9 dBFS), and muxed with the video stream copied untouched (AAC 192k, 48 kHz, stereo).
Use it for sound-only fixes: a stem changed (music, effects, ambience), a voice re-cut at the same length.
"""
import argparse
import json
import os
import re
import subprocess
import tempfile

import numpy as np

SR = 48000


def load(path):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("hf3d"); ap.add_argument("video_in"); ap.add_argument("video_out")
    ap.add_argument("--lufs", type=float, default=-14.0)
    a = ap.parse_args()
    html = open(os.path.join(a.hf3d, "index.html"), encoding="utf-8").read()
    dur = float(re.search(r'data-composition-id="main"[^>]*data-duration="([0-9.]+)"', html).group(1))
    mix = np.zeros(int(dur * SR))
    for tag in re.findall(r'<audio[^>]*class="clip"[^>]*>', html):
        at = dict(re.findall(r'([\w-]+)="([^"]*)"', tag))
        x = load(os.path.join(a.hf3d, at["src"]))[:int(float(at["data-duration"]) * SR)] * float(at.get("data-volume", 1))
        i = int(float(at["data-start"]) * SR); n = max(0, min(len(x), len(mix) - i)); mix[i:i + n] += x[:n]
        print(f"  {at['id']:10s} at {float(at['data-start']):6.2f} s  vol {at.get('data-volume', '1')}")
    with tempfile.TemporaryDirectory() as td:
        raw = os.path.join(td, "sum.wav"); out = os.path.join(td, "mix.wav")
        pcm = (np.clip(mix / max(1.0, np.abs(mix).max()), -1, 1) * 32767).astype("<i2")     # headroom: loudnorm sets the level
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", raw], input=pcm.tobytes(), check=True)
        ln = f"loudnorm=I={a.lufs}:TP=-1.5:LRA=11"
        r = subprocess.run(["ffmpeg", "-hide_banner", "-i", raw, "-af", ln + ":print_format=json", "-f", "null", "-"], capture_output=True, text=True)
        m = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
        # a plain gain to the target, then a gentle peak limiter (clicks and pops would otherwise cap a linear gain)
        gain = a.lufs - float(m["input_i"])
        for _ in range(4):                     # the limiter and the stereo conversion move the result: measure the output and correct
            af = f"volume={gain:.2f}dB,alimiter=limit=0.8:attack=2:release=60:level=false,aresample=48000"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", af, "-ac", "2", out], check=True)
            r = subprocess.run(["ffmpeg", "-hide_banner", "-i", out, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
            got = float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", r.stderr)[-1])
            print(f"  gain {gain:+.2f} dB -> {got} LUFS")
            if abs(got - a.lufs) < 0.15: break
            gain += a.lufs - got
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", a.video_in, "-i", out, "-map", "0:v:0", "-map", "1:a:0",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-shortest", "-movflags", "+faststart", a.video_out], check=True)
    print("->", a.video_out)


if __name__ == "__main__":
    main()
