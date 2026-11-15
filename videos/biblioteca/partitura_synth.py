#!/usr/bin/env python3
"""Soft background music from the owner's scores (videos/biblioteca/partituras/*.json): a music-box melody, a warm low
chord pad and a soft bass, low-passed, looped to the reel's length, ducked under the voices and OUT under the ocarina
(the duck windows come from the reel's cues.json), then matched in loudness to a reference stem.

  python3 partitura_synth.py SCORE.json CUES.json OUT.wav [--ref OLD_MUSIC.wav] [--bars 5-12] [--tempo 0.9] [--transpose 0]

--ref: the reel's previous ambient bed; the new stem gets the same integrated loudness, so the page volume (0.22) and the
levels checked by nivel_musica.py stay where they were. --tempo scales the score's bpm (a calmer bed under dialogue).
The owner gave permission to use these scores (15/11/2026, see partituras/LEEME.md).
"""
import argparse, json, re, subprocess, wave
import numpy as np

SR = 44100
NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def hz(n, tr=0):
    m = re.fullmatch(r"([A-G])([#b]?)(-?\d)", n); s = NOTE[m[1]] + (1 if m[2] == "#" else -1 if m[2] == "b" else 0)
    return 440 * 2 ** ((s + 12 * (int(m[3]) + 1) - 69 + tr) / 12)


def pluck(f, d, amp):                       # a soft music box: sine + a little octave, quick attack, long decay
    n = int((d + 0.6) * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) + 0.18 * np.sin(4 * np.pi * f * t) * np.exp(-t * 6)
    return amp * x * np.minimum(1, t / 0.006) * np.exp(-t * 3.2)


def pad(fs, d, amp):                        # a warm pad: detuned triangles, slow attack and release
    n = int((d + 0.4) * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for f in fs:
        for det in (0.997, 1.003):
            ph = (t * f * det) % 1; x += 4 * np.abs(ph - 0.5) - 1
    e = np.minimum(1, t / 0.25) * np.clip((d + 0.4 - t) / 0.4, 0, 1)
    return amp * x / (2 * len(fs)) * e


def lowpass(x, fc):
    a = 1 - np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x): acc += a * (v - acc); y[i] = acc
    return y


def lufs(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1])


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("score"); ap.add_argument("cues"); ap.add_argument("out")
    ap.add_argument("--ref"); ap.add_argument("--bars"); ap.add_argument("--tempo", type=float, default=1.0); ap.add_argument("--transpose", type=int, default=0)
    a = ap.parse_args()
    S = json.load(open(a.score)); C = json.load(open(a.cues)); DUR = C["duration"]; M = C.get("music", {})
    bars = S["bars"]
    if a.bars: lo, hi = map(int, a.bars.split("-")); bars = [b for b in bars if lo <= b["n"] <= hi]
    beat = 60 / (S["bpm"] * a.tempo); bpb = S["beats_per_bar"]
    out = np.zeros(int((DUR + 2) * SR)); t0 = 0.0; k = 0
    while t0 < DUR:
        b = bars[k % len(bars)]; k += 1; t = t0
        for n, d in b["mel"]:
            if n != "r": x = pluck(hz(n, a.transpose), d * beat, 0.32); i = int(t * SR); out[i:i + len(x)] += x[:len(out) - i]
            t += d * beat
        if b.get("chord"):
            x = pad([hz(n, a.transpose) for n in b["chord"]], bpb * beat, 0.22); i = int(t0 * SR); out[i:i + len(x)] += x[:len(out) - i]
        t = t0
        for n, d in b.get("bass") or ([[b["chord"][0], bpb]] if b.get("chord") else []):
            if n != "r": x = pluck(hz(n, a.transpose), d * beat, 0.26); i = int(t * SR); out[i:i + len(x)] += x[:len(out) - i]
            t += d * beat
        t0 += bpb * beat
    out = lowpass(out[:int(DUR * SR)], 2400)
    # ducking (voices) and the ocarina windows at 0: 60 ms in, 400 ms out
    g = np.ones(len(out)); tt = np.arange(len(out)) / SR
    for s, e, lvl in M.get("duck", []):
        w = np.clip(np.minimum((tt - (s - 0.06)) / 0.06, ((e + 0.4) - tt) / 0.4), 0, 1); g = np.minimum(g, 1 - (1 - lvl) * w)
    fo = M.get("fade_out")
    if fo: g *= np.clip((fo[1] - tt) / max(0.05, fo[1] - fo[0]), 0, 1)
    out *= g
    out = out / max(1e-9, np.abs(out).max()) * 0.5
    y = (np.clip(out, -1, 1) * 32767).astype(np.int16)
    with wave.open(a.out, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(y.tobytes())
    if a.ref:
        diff = lufs(a.ref) - lufs(a.out)
        x = np.frombuffer(open(a.out, "rb").read()[44:], np.int16) / 32767 * 10 ** (diff / 20)
        y = (np.clip(x, -1, 1) * 32767).astype(np.int16)
        with wave.open(a.out, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(y.tobytes())
        print(f"matched to the reference: {diff:+.1f} dB")
    print(a.out, round(DUR, 2), "s,", k, "bars")


if __name__ == "__main__":
    main()
