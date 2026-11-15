#!/usr/bin/env python3
"""A full band from the owner's scores (videos/biblioteca/partituras/*.json): piano (melody and chords), drums, bass, a
synth pad and a theremin, for the reels' background music. The owner asked on 15/11/2026: "la musica se siente muy vacia
... además de piano agrega percusión, bajo, un sintetizador y un theremin".

  python3 partitura_banda.py SCORE.json CUES.json OUT.wav [--ref OLD_MUSIC.wav] [--bars 5-12] [--tempo 1.0] [--stems DIR]

Arrangement: the piano plays the melody and comps the chord on every beat; the bass plays the root (octave-jumping eighths
in 4/4, oom on beat 1 in 3/4); the drums keep a soft groove (kick, snare or clap, hats); the synth holds the chord as a
filtered, detuned saw pad; the theremin carries the melody with a glide and vibrato, but only in the gaps between spoken
lines (it sits in the speech band), handing it to the piano under the voices. The whole band ducks under the voices and is
OUT under the ocarina (duck windows from cues.json). The mix is matched in loudness to --ref (the ambient bed it replaces),
so the page volume and the levels checked by nivel_musica.py stay put. All synthesised, seeded: same input, same audio.
"""
import argparse, json, re, subprocess, wave
import numpy as np

SR = 44100
NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
rng = np.random.default_rng(11)


def midi(n):
    m = re.fullmatch(r"([A-G])([#b]?)(-?\d)", n); return NOTE[m[1]] + (1 if m[2] == "#" else -1 if m[2] == "b" else 0) + 12 * (int(m[3]) + 1)
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def T(d): return np.arange(int(d * SR)) / SR
def add(buf, x, t):
    i = int(t * SR); j = min(len(buf), i + len(x))
    if i < len(buf): buf[i:j] += x[:j - i]
def lowpass(x, fc):
    a = 1 - np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x): acc += a * (v - acc); y[i] = acc
    return y


# ---------------- instruments ----------------
def piano(f, d, amp):                      # additive: decaying partials (higher ones faster), slight stretch, a hammer tick
    t = T(d + 1.2); x = np.zeros(len(t))
    for k in range(1, 8):
        fk = f * k * (1 + 0.0004 * k * k)
        if fk > 9000: break
        x += np.sin(2 * np.pi * fk * t) * (1 / k ** 1.25) * np.exp(-t * (1.6 + 0.9 * k) * (f / 400) ** 0.3)
    x += rng.standard_normal(len(t)) * np.exp(-t * 180) * 0.08
    rel = np.clip((d + 0.25 - t) / 0.25, 0, 1) * 0.85 + 0.15 * np.exp(-np.maximum(0, t - d) * 6)   # damper
    return amp * x * np.minimum(1, t / 0.003) * rel
def bass(f, d, amp):                       # a round bass: saw low-passed by a decaying filter, sine sub
    t = T(d + 0.1); ph = (t * f) % 1; saw = 2 * ph - 1
    x = lowpass(saw, 380) * 0.8 + np.sin(2 * np.pi * f * t) * 0.6
    return amp * x * np.minimum(1, t / 0.01) * np.clip((d + 0.05 - t) / 0.08, 0, 1)
def pad(fs, d, amp):                       # a synth pad: detuned saws, slow attack, low-passed later
    t = T(d + 0.5); x = np.zeros(len(t))
    for f in fs:
        for det in (0.994, 1.0, 1.006): x += 2 * ((t * f * det) % 1) - 1
    return amp * x / (3 * len(fs)) * np.minimum(1, t / 0.35) * np.clip((d + 0.5 - t) / 0.5, 0, 1)
def kick(amp):
    t = T(0.35); f = 45 + 90 * np.exp(-t * 28); ph = 2 * np.pi * np.cumsum(f) / SR
    return amp * np.sin(ph) * np.exp(-t * 9)
def snare(amp):
    t = T(0.22); n = rng.standard_normal(len(t)); n = n - lowpass(n, 1500)
    return amp * (n * np.exp(-t * 22) * 0.7 + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * 0.5)
def hat(amp, open_=False):
    t = T(0.25 if open_ else 0.06); n = rng.standard_normal(len(t)); n = n - lowpass(n, 6500)
    return amp * n * np.exp(-t * (14 if open_ else 70))
def theremin_line(notes, dur):             # one continuous voice: glide between notes, delayed vibrato, soft attack per phrase
    n = int(dur * SR); f = np.zeros(n); g = np.zeros(n)
    for t0, d, m in notes:
        i, j = int(t0 * SR), min(n, int((t0 + d) * SR)); f[i:j] = hz(m); g[i:j] = 1
    # glide: smooth the pitch (60 ms), fill rests with the last pitch so the glide never drops to 0
    last = 0.0
    for i in range(n):
        if f[i] == 0: f[i] = last
        else: last = f[i]
    f = lowpass(f, 1 / (2 * np.pi * 0.06)); g = lowpass(g, 1 / (2 * np.pi * 0.05))
    t = np.arange(n) / SR; vib = 1 + 0.012 * np.sin(2 * np.pi * 5.8 * t)
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    return (np.sin(ph) + 0.08 * np.sin(2 * ph)) * g


def lufs(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1])
def write(path, x):
    y = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(y.tobytes())


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("score"); ap.add_argument("cues"); ap.add_argument("out")
    ap.add_argument("--ref"); ap.add_argument("--bars"); ap.add_argument("--tempo", type=float, default=1.0); ap.add_argument("--stems")
    a = ap.parse_args()
    S = json.load(open(a.score)); C = json.load(open(a.cues)); DUR = C["duration"]; M = C.get("music", {})
    bars = S["bars"]
    if a.bars: lo, hi = map(int, a.bars.split("-")); bars = [b for b in bars if lo <= b["n"] <= hi]
    beat = 60 / (S["bpm"] * a.tempo); bpb = S["beats_per_bar"]; N = int((DUR + 2) * SR)
    st = {k: np.zeros(N) for k in ("piano", "bass", "drums", "synth", "theremin")}
    thr = []; t0 = 0.0; k = 0; chord = None
    while t0 < DUR:
        b = bars[k % len(bars)]; k += 1
        chord = [midi(n) for n in b["chord"]] if b.get("chord") else chord or [midi("G3"), midi("Bb3"), midi("D4")]
        # piano melody, and the theremin's copy of it (an octave below when the melody runs high)
        t = t0
        for n, d in b["mel"]:
            if n != "r":
                m = midi(n); add(st["piano"], piano(hz(m), d * beat, 0.30), t); thr.append((t, d * beat, m - 12 if m >= 84 else m))
            t += d * beat
        # piano comping: the chord (an octave up from the bass register) on each beat, softly
        cm = [c + 12 if c < 55 else c for c in chord]
        for q in range(bpb):
            if bpb == 3 and q == 0: continue                        # waltz: beats 2 and 3 only
            for c in cm: add(st["piano"], piano(hz(c), beat * 0.9, 0.07), t0 + q * beat)
        # bass: the written line when there is one, else the root (4/4: root and octave in eighths; 3/4: oom on beat 1)
        root = min(chord) % 12 + 36
        if b.get("bass"):
            t = t0
            for n, d in b["bass"]:
                if n != "r":
                    m = midi(n)
                    while m > 52: m -= 12
                    add(st["bass"], bass(hz(m), d * beat * 0.9, 0.5), t)
                t += d * beat
        elif bpb == 3: add(st["bass"], bass(hz(root), beat * 0.9, 0.55), t0)
        else:
            for e in range(bpb * 2): add(st["bass"], bass(hz(root + (12 if e % 4 == 3 else 0)), beat * 0.42, 0.45 if e % 2 == 0 else 0.3), t0 + e * beat / 2)
        # synth pad: the chord, held for the bar
        add(st["synth"], pad([hz(c) for c in cm], bpb * beat, 0.5), t0)
        # drums
        if bpb == 3:
            add(st["drums"], kick(0.8), t0)
            for q in (1, 2): add(st["drums"], hat(0.25, open_=True), t0 + q * beat); add(st["drums"], snare(0.12), t0 + q * beat)
        else:
            fast = S["bpm"] * a.tempo < 90                            # slow pieces: a half-time feel with sixteenth hats
            for q in range(bpb):
                tq = t0 + q * beat
                if q in (0, 2) or (q == 3 and k % 2 == 0 and not fast): add(st["drums"], kick(0.85), tq if q != 3 else tq + beat / 2)
                if (q == 2 if fast else q in (1, 3)): add(st["drums"], snare(0.45), tq)
                for s in range(4 if fast else 2): add(st["drums"], hat(0.22 if s % 2 == 0 else 0.13), tq + s * beat / (4 if fast else 2))
        t0 += bpb * beat
    st["theremin"] = np.concatenate([theremin_line(thr, DUR + 2)[:N], np.zeros(max(0, N - int((DUR + 2) * SR)))])[:N] * 0.32
    for k2 in ("piano", "synth"): st[k2] = lowpass(st[k2], 5200 if k2 == "piano" else 1300)
    st["theremin"] = lowpass(st["theremin"], 3000)
    # gains: the full duck (voices, the ocarina at 0), and the theremin out under every spoken line
    tt = np.arange(N) / SR; g = np.ones(N); gt = np.ones(N)
    for s, e, lvl in M.get("duck", []):
        w = np.clip(np.minimum((tt - (s - 0.06)) / 0.06, ((e + 0.4) - tt) / 0.4), 0, 1); g = np.minimum(g, 1 - (1 - lvl) * w)
        if lvl > 0: gt = np.minimum(gt, 1 - w)                     # theremin: out under the voices (lvl 0 windows are the ocarina: g already 0)
    fo = M.get("fade_out")
    if fo: g *= np.clip((fo[1] - tt) / max(0.05, fo[1] - fo[0]), 0, 1)
    MIX = {"piano": 1.0, "bass": 0.9, "drums": 0.55, "synth": 0.35, "theremin": 0.8}
    out = sum(st[k2] * MIX[k2] * (gt if k2 == "theremin" else 1) for k2 in st) * g
    out = out[:int(DUR * SR)]; out = out / max(1e-9, np.abs(out).max()) * 0.6
    write(a.out, out)
    if a.stems:
        import os; os.makedirs(a.stems, exist_ok=True)
        for k2, x in st.items(): write(f"{a.stems}/{k2}.wav", (x * MIX[k2] * g)[:int(DUR * SR)] / max(1e-9, np.abs(out).max() * 1.7))
    if a.ref:
        diff = lufs(a.ref) - lufs(a.out)
        x = np.frombuffer(open(a.out, "rb").read()[44:], np.int16) / 32767 * 10 ** (diff / 20); write(a.out, x)
        print(f"matched to the reference: {diff:+.1f} dB")
    print(a.out, round(DUR, 2), "s,", k, "bars")


if __name__ == "__main__":
    main()
