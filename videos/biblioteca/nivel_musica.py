#!/usr/bin/env python3
"""Music bed vs voices, from a reel's page: python3 nivel_musica.py HF3D_DIR
Reads the <audio class="clip"> tags like remezclar.py (src, start, duration, data-volume), sums the voice clips
(data-who) and the music clip, and prints the music's K-weighted RMS level under the voices and in the gaps, relative to the
voices' RMS while they speak. Target (RESEARCH_NOVIEMBRE_2_2026.md, the sound team): the bed 15-20 dB under the voice
while someone talks, about 10-12 dB under it in the gaps."""
import re, subprocess, sys, os
import numpy as np
SR = 48000
d = sys.argv[1]; html = open(os.path.join(d, "index.html")).read()
dur = float(re.search(r'data-composition-id="main"[^>]*data-duration="([0-9.]+)"', html).group(1)); n = int(dur * SR)
def load(p): return np.frombuffer(subprocess.run(["ffmpeg", "-loglevel", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32)
voice, music, mask = np.zeros(n), np.zeros(n), np.zeros(n, bool)
for tag in re.findall(r"<audio[^>]*>", html):
    at = dict(re.findall(r'([\w-]+)="([^"]*)"', tag)); x = load(os.path.join(d, at["src"]))[:int(float(at["data-duration"]) * SR)] * float(at.get("data-volume", 1))
    i = int(float(at["data-start"]) * SR); k = max(0, min(len(x), n - i))
    if "data-who" in at: voice[i:i + k] += x[:k]; mask[i:i + k] = True
    elif "music" in at["src"]: music[i:i + k] += x[:k]
def kw(v):   # an approximate K-weighting (as loudness meters hear it): a high-pass near 100 Hz and +4 dB above 1.5 kHz
    X = np.fft.rfft(v); f = np.fft.rfftfreq(len(v), 1 / SR); X *= (f / 100) ** 2 / (1 + (f / 100) ** 2) * (1 + 0.58 * (f / 1500) ** 2 / (1 + (f / 1500) ** 2)); return np.fft.irfft(X, len(v))
voice, music = kw(voice), kw(music)
rms = lambda v: 20 * np.log10(np.sqrt(np.mean(v ** 2)) + 1e-9)
V = rms(voice[mask]); under = rms(music[mask]); gaps = rms(music[~mask][: int(SR * 0.0) or None])
print(f"voices {V:.1f} dB | music under voices {under - V:+.1f} dB | music in the gaps {gaps - V:+.1f} dB (relative to the voices)")
