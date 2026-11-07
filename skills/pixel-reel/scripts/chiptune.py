"""Chiptune audio from a cue sheet: sound effects, music and ambience as separate WAV stems.

  python3 chiptune.py cues.json OUT_DIR          -> OUT_DIR/sfx.wav, music.wav, ambience.wav
  python3 chiptune.py --list                     -> list the sound-effect names

cues.json:
{
  "duration": 15,
  "sfx": [ {"t": 0.0, "s": "door_bang"}, {"t": 0.3, "s": "flipflop", "n": 6, "every": 0.18},
           {"t": 8.6, "s": "item_get", "pitch": 1.12, "gain": 0.9} ],
  "music": {"bpm": 140, "start": 0.3, "melody": [[4, 1], [4, 1], [4, 2]], "chords": [0, 0, 5, 7],
            "beats_per_bar": 4, "octave": 0, "duck": [[5.0, 6.9, 0.35]], "fade_out": [14.2, 15.0],
            "end_chord": {"t": 14.0, "notes": [0, 4, 7, 12]}},
  "ambience": [ {"type": "cicadas", "from": 0, "to": 15, "level": 0.15} ]
}
Melody notes are semitones from C5 (0 = C, 4 = E, 7 = G, 12 = next C, null = rest); durations in beats.
Every cue accepts "gain"; repeated cues accept "n" and "every". All randomness is seeded: same file, same audio.
Only use public-domain tunes or original melodies.
"""
import json, math, os, sys, wave
import numpy as np

SR = 44100
rng = np.random.default_rng(5)


def t(d): return np.arange(int(d * SR)) / SR
def sq(f, d, duty=0.5):
    n = int(d * SR)
    ph = np.cumsum(np.broadcast_to(np.asarray(f, float), n) / SR) if np.ndim(f) else t(d) * f
    return np.where((ph % 1) < duty, 1.0, -1.0)
def tri(f, d): ph = (t(d) * f) % 1; return 4 * np.abs(ph - 0.5) - 1
def noise(d): return rng.uniform(-1, 1, int(d * SR))
def env(n, a=0.005, r=0.1):
    e = np.ones(n); A = max(1, int(a * SR)); e[:A] = np.linspace(0, 1, A); R = min(int(r * SR), n); e[n - R:] *= np.linspace(1, 0, R); return e
def dec(d, k): return np.exp(-t(d) * k)
def crush(x, bits=5): q = 2 ** bits; return np.round(x * q) / q
def lp(x, a):
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x): acc += a * (v - acc); y[i] = acc
    return y
def hp(x, a): return x - lp(x, a)
def note(s, octave=0): return 523.25 * 2 ** ((s + 12 * octave) / 12)
def cat(*xs): return np.concatenate(xs)
def mix(*xs):
    n = max(len(x) for x in xs); out = np.zeros(n)
    for x in xs: out[:len(x)] += x
    return out


# ------------------------------------------------------------- effect catalogue (each returns a mono array)
def fx_tap(p=1): return noise(0.03) * dec(0.03, 120) * 0.5 + sq(1800 * p, 0.03) * dec(0.03, 160) * 0.4
def fx_door_bang(p=1): return mix(crush(hp(noise(0.12), 0.2) * dec(0.12, 30)) * 0.8, crush(sq(np.geomspace(160 * p, 60, int(0.18 * SR)), 0.18) * dec(0.18, 14)) * 0.6)
def fx_door_close(p=1): return mix(crush(sq(np.geomspace(200 * p, 90, int(0.1 * SR)), 0.1) * dec(0.1, 30)) * 0.5, noise(0.05) * dec(0.05, 80) * 0.3)
def fx_creak(p=1): return crush(sq(np.linspace(240 * p, 150 * p, int(0.2 * SR)), 0.2, 0.125) * env(int(0.2 * SR), 0.01, 0.05)) * 0.3
def fx_step(p=1): return crush(sq(np.linspace(180 * p, 110 * p, int(0.035 * SR)), 0.035) * dec(0.035, 90)) * 0.35
def fx_flipflop(p=1): return mix(crush(hp(noise(0.03), 0.4) * dec(0.03, 110)) * 0.45, sq(900 * p, 0.015) * dec(0.015, 200) * 0.25)
def fx_plop(p=1): return crush(sq(np.geomspace(320 * p, 90 * p, int(0.12 * SR)), 0.12) * dec(0.12, 18)) * 0.6
def fx_pop(p=1):
    f = np.geomspace(300 * p, 900 * p, int(0.08 * SR)); return crush(sq(f, 0.08) * env(int(0.08 * SR), 0.002, 0.03)) * 0.5
def fx_sparkle(p=1):
    x = np.zeros(int(0.3 * SR))
    for k in range(5):
        s = sq(2093 * p * 2 ** (k * 2 / 12), 0.05, 0.25) * dec(0.05, 50) * 0.2; i = int(k * 0.05 * SR); x[i:i + len(s)] += s
    return x
def fx_chime(p=1):
    x = np.zeros(int(0.9 * SR))
    for j, s in enumerate([0, 4, 7, 12, 16]):
        y = (sq(note(s) * p, 0.5, 0.25) * dec(0.5, 5) * 0.3 + tri(note(s + 12) * p, 0.5) * dec(0.5, 4) * 0.25); i = int(j * 0.06 * SR); x[i:i + len(y)] += crush(y, 6)
    return x
def fx_idea(p=1): return cat(sq(note(12) * p, 0.06, 0.25) * dec(0.06, 30), sq(note(19) * p, 0.25, 0.25) * dec(0.25, 9)) * 0.4
def fx_item_get(p=1):
    x = np.zeros(int(0.5 * SR))
    for k, s in enumerate([0, 4, 7, 12]):
        y = sq(note(s) * p, 0.09, 0.25) * env(int(0.09 * SR), 0.002, 0.03); i = int(k * 0.07 * SR); x[i:i + len(y)] += y * 0.35
    y = sq(note(19) * p, 0.2, 0.125) * dec(0.2, 8) * 0.3; i = int(0.28 * SR); x[i:i + len(y)] += y
    return crush(x, 6)
def fx_whoosh(p=1): return crush(lp(noise(0.18), 0.12 * p) * np.sin(np.linspace(0, np.pi, int(0.18 * SR)))) * 0.5
def fx_sack_plop(p=1): return mix(crush(lp(noise(0.1), 0.15) * dec(0.1, 25)) * 0.6, sq(np.geomspace(200 * p, 120, int(0.08 * SR)), 0.08) * dec(0.08, 30) * 0.3)
def fx_boom(p=1): return mix(crush(lp(noise(0.5), 0.08) * dec(0.5, 7), 4) * 0.9, sq(np.geomspace(90 * p, 40, int(0.4 * SR)), 0.4) * dec(0.4, 8) * 0.5)
def fx_victory(p=1):
    x = np.zeros(int(1.4 * SR))
    for k, s in enumerate([0, 4, 7]):
        y = sq(note(s - 5) * p, 0.12, 0.25) * env(int(0.12 * SR), 0.002, 0.03) * 0.3; i = int(k * 0.09 * SR); x[i:i + len(y)] += y
    for s in [0, 4, 7, 12]:
        y = sq(note(s) * p, 1.0, 0.25 if s else 0.5) * dec(1.0, 1.4) * env(int(SR), 0.003, 0.5) * 0.22; i = int(0.3 * SR); x[i:i + len(y)] += y
    return crush(x, 6)
def fx_sad(p=1): return cat(*[sq(note(s - 12) * p, 0.22, 0.5) * env(int(0.22 * SR), 0.01, 0.08) * 0.3 for s in (4, 3, 2, -1)])
def fx_surprise(p=1): return crush(sq(np.geomspace(300 * p, 1200 * p, int(0.12 * SR)), 0.12, 0.25) * env(int(0.12 * SR), 0.002, 0.04)) * 0.45
def fx_relief(p=1): return cat(*[sq(note(s) * p, 0.08, 0.25) * env(int(0.08 * SR), 0.002, 0.03) * 0.3 for s in (12, 7, 4, 7, 12, 16)])
def fx_sip(p=1): return cat(*[crush(sq(np.linspace(500 * p, 380 * p, int(0.05 * SR)), 0.05) * dec(0.05, 40)) * 0.15 for _ in range(3)])
def fx_flutter(p=1): return cat(*[crush(lp(noise(0.04), 0.35) * dec(0.04, 45), 4) * 0.4 for _ in range(4)])
def fx_flap(p=1): return crush(lp(noise(0.05), 0.35) * dec(0.05, 45), 4) * 0.45
def fx_peck(p=1): return sq(2600 * p, 0.018) * dec(0.018, 220) * 0.35
def fx_click(p=1): return noise(0.02) * dec(0.02, 300) * 0.6 + sq(2400 * p, 0.02) * dec(0.02, 250) * 0.4
def fx_rustle(p=1): return crush(hp(noise(0.16), 0.5) * np.abs(np.sin(np.linspace(0, 3 * np.pi, int(0.16 * SR)))) * dec(0.16, 6)) * 0.35
def fx_tiptoe(p=1):
    x = tri(note(-5) * p, 0.07) * dec(0.07, 45); y = sq(note(7) * p, 0.02, 0.125) * dec(0.02, 160) * 0.3; x[:len(y)] += y; return x * 0.45
def fx_sting(p=1): return mix(*[sq(note(s) * p, 0.35, 0.25) * dec(0.35, 9) * 0.22 for s in (0, 6, 11)])
def fx_whistle(p=1, d=0.7):
    tt = t(d); f = note(19) * p * (1 + 0.12 * np.sin(2 * np.pi * 1.6 * tt) + 0.05 * np.sin(2 * np.pi * 7 * tt))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(tt), 0.04, 0.12) * 0.28
def fx_ding(p=1): return (sq(note(24) * p, 0.25, 0.25) * dec(0.25, 10) + tri(note(31) * p, 0.25) * dec(0.25, 12) * 0.5) * 0.3
def fx_printer(p=1, d=0.8):
    tt = t(d); f = 140 * p + 20 * np.sign(np.sin(2 * np.pi * 6 * tt))
    return crush(sq(f, d, 0.5) * 0.12 + hp(noise(d), 0.5) * 0.04)
def fx_fuse(p=1, d=0.5): return crush(hp(noise(d), 0.6) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 9 * t(d))))) * 0.25
def fx_heave(p=1): return crush(sq(np.linspace(150 * p, 230 * p, int(0.25 * SR)), 0.25, 0.25) * env(int(0.25 * SR), 0.02, 0.08)) * 0.3
def fx_puff(p=1): return crush(lp(noise(0.25), 0.15) * dec(0.25, 12)) * 0.4
def fx_chirp(p=1):
    x = np.zeros(int(0.3 * SR))
    for j in range(2):
        f = np.linspace(2600 * p, 3200 * p if j % 2 == 0 else 2200 * p, int(0.05 * SR)); y = lp(sq(f, 0.05), 0.25) * env(len(f), 0.005, 0.02) * 0.5
        i = int(j * 0.07 * SR); x[i:i + len(y)] += y
    return x


# chess (RESEARCH_AJEDREZ_2026.md, sound team): a wooden "clack" = a 5 ms noise tick + a 1.8 kHz ping (30 ms) + a ~420 Hz
# wooden body (60 ms); a heavier "thud" when a piece falls; a viking lur (a low horn with a slow attack and a bend up);
# a small bell for check
def fx_clack(p=1):
    n = int(0.09 * SR); y = np.zeros(n); tk = hp(noise(0.005), 0.5) * np.linspace(1, 0, int(0.005 * SR)); y[:len(tk)] += tk * 0.5
    tt = t(0.09); y += np.sin(2 * np.pi * 1800 * p * tt) * np.exp(-tt * 110) * 0.35 + np.sin(2 * np.pi * 420 * p * tt) * np.exp(-tt * 45) * 0.55
    return y * 0.8
def fx_thud(p=1):
    tt = t(0.22); f = 180 * p * np.exp(-tt * 9); ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * np.exp(-tt * 14) * 0.8 + lp(noise(0.22), 0.2) * np.exp(-tt * 30) * 0.3) * 0.9
def fx_lur(p=1, d=0.9):
    tt = t(d); f = note(-29) * p * (1 + 0.335 * np.clip(tt / 0.25, 0, 1) ** 2)                 # E2 bending up a fourth
    ph = 2 * np.pi * np.cumsum(f) / SR; x = np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.3 * np.sin(3 * ph) + 0.12 * np.sin(4 * ph)
    return lp(x, 0.25) * env(len(tt), 0.12, 0.25) * 0.45
def fx_bell(p=1):
    tt = t(1.0); return (np.sin(2 * np.pi * 1320 * p * tt) * 0.5 + np.sin(2 * np.pi * 2640 * p * tt) * 0.25 + np.sin(2 * np.pi * 3960 * p * tt) * 0.1) * np.exp(-tt * 4.5) * 0.5
FX = {k[3:]: v for k, v in globals().items() if k.startswith("fx_") and callable(v)}


# ------------------------------------------------------------- ambience
def amb_cicadas(d, level):
    tt = t(d); base = hp(noise(d), 0.7) * (0.6 + 0.4 * (np.sin(2 * np.pi * 37 * tt) > 0))
    swell = 0.5 + 0.5 * np.sin(2 * np.pi * tt / 4.3) ** 2; return base * swell * level
def amb_crickets(d, level):
    y = np.zeros(int(d * SR)); r = np.random.default_rng(7)
    for k in range(int(d * 2.2)):
        at = r.uniform(0, max(0.01, d - 0.3)); n = int(0.025 * SR); tt = np.arange(n) / SR; f = r.uniform(4200, 4800)
        for j in range(3): i = int((at + j * 0.045) * SR); seg = np.sin(2 * np.pi * f * tt) * np.sin(np.pi * tt / 0.025) * r.uniform(0.4, 1.0); y[i:i + n] += seg[:max(0, min(n, len(y) - i))]
    return y * level
def amb_waves(d, level):
    w = lp(noise(d), 0.05); w = w - lp(w, 0.002); return w * (0.55 + 0.45 * np.sin(2 * np.pi * t(d) / 3.1) ** 2) * level * 4
def amb_birds(d, level):
    x = np.zeros(int(d * SR)); k = 0; tt = 0.4
    while tt < d - 0.4:
        y = fx_chirp(0.9 + (k * 0.37) % 0.4); i = int(tt * SR); x[i:i + len(y)] += y[:len(x) - i] * level * 2; tt += 0.7 + (k * 0.53) % 0.9; k += 1
    return x
AMB = {"cicadas": amb_cicadas, "waves": amb_waves, "birds": amb_birds, "crickets": amb_crickets}


def put(buf, x, at, gain=1.0):
    i = int(at * SR); n = min(len(x), len(buf) - i)
    if n > 0 and i >= 0: buf[i:i + n] += x[:n] * gain


def music(cfg, D):
    m = np.zeros(int(D * SR)); b = 60 / cfg.get("bpm", 132); pos = cfg.get("start", 0.0); oc = cfg.get("octave", 0)
    for s, beats in cfg.get("melody", []):
        dur = beats * b
        if s is not None and pos < D:
            put(m, sq(note(s, oc), dur * 0.9, 0.25) * env(int(dur * 0.9 * SR), 0.004, min(0.12, dur * 0.35)), pos, 0.22)
        pos += dur
    bar = cfg.get("beats_per_bar", 4) * b
    for k, r in enumerate(cfg.get("chords", [])):
        at = cfg.get("start", 0.0) + k * bar
        for q in range(cfg.get("beats_per_bar", 4)):
            put(m, tri(note(r - 24 + (7 if q % 2 else 0)), b * 0.8) * env(int(b * 0.8 * SR), 0.004, 0.08), at + q * b, 0.28)
    ec = cfg.get("end_chord")
    if ec:
        for s in ec["notes"]: put(m, sq(note(s), 1.4, 0.25) * dec(1.4, 2.2) * env(int(1.4 * SR), 0.01, 0.6), ec["t"], 0.12)
    g = np.ones(len(m))
    for t0, t1, lvl in cfg.get("duck", []):
        i0, i1 = int(t0 * SR), int(t1 * SR); ramp = int(0.08 * SR)
        g[i0:i1] = np.minimum(g[i0:i1], lvl)
        g[max(0, i0 - ramp):i0] = np.minimum(g[max(0, i0 - ramp):i0], np.linspace(1, lvl, len(g[max(0, i0 - ramp):i0])))
        g[i1:i1 + ramp] = np.minimum(g[i1:i1 + ramp], np.linspace(lvl, 1, len(g[i1:i1 + ramp])))
    if cfg.get("fade_out"):
        i0, i1 = (int(x * SR) for x in cfg["fade_out"]); g[i0:i1] *= np.linspace(1, 0, i1 - i0); g[i1:] = 0
    return m * g


def dc_block(x, f0=20.0):
    """removes DC and sub-audio drift: pulse waves are not centred on zero, and the music ducking moved that offset
    up and down (a thump at every duck). A zero-phase high-pass at f0 (FFT; no scipy needed)."""
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X *= np.clip(f / f0, 0, 1) ** 2; return np.fft.irfft(X, len(x))


def write(path, x, peak=0.85, boost=True):
    """boost=True normalises the stem to `peak` (music, effects). boost=False only scales DOWN if it would pass `peak`, so
    levels set in the cues are kept (ambience: before, any ambience was boosted to a 0.5 peak and its level ignored)."""
    x = dc_block(x); m = np.abs(x).max()
    if boost or m > peak: x = x / max(1e-9, m) * peak
    w = wave.open(path, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes()); w.close()


def main():
    if "--list" in sys.argv: print(", ".join(sorted(FX)), "| ambience:", ", ".join(AMB)); return
    cues = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True); D = cues["duration"]
    sfx = np.zeros(int(D * SR))
    for c in cues.get("sfx", []):
        fn = FX[c["s"]]; n = c.get("n", 1)
        for k in range(n):
            p = c.get("pitch", 1.0) * (c.get("pitch_step", 1.0) ** k)
            y = fn(p, c["d"]) if "d" in c else fn(p)
            put(sfx, y, c["t"] + k * c.get("every", 0), c.get("gain", 1.0))
    write(os.path.join(out, "sfx.wav"), sfx, 0.9)
    if cues.get("music"): write(os.path.join(out, "music.wav"), music(cues["music"], D), 0.8)
    amb = np.zeros(int(D * SR))
    for a in cues.get("ambience", []):
        y = AMB[a["type"]](a["to"] - a["from"], a.get("level", 0.2)); put(amb, y, a["from"])
    if np.abs(amb).max() > 0: write(os.path.join(out, "ambience.wav"), amb, 0.5, boost=False)
    elif os.path.exists(os.path.join(out, "ambience.wav")): write(os.path.join(out, "ambience.wav"), amb + 1e-9, 0.5, boost=False)   # silent stem, so the page still finds it
    print("audio ->", out)


if __name__ == "__main__":
    main()
