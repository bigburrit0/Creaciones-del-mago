"""banda.py: original music and comic sound effects for the reels, synthesised with numpy (no samples, no network).

The owner found the ambient bed meaningless ("la música no tiene mucho sentido") and asked for music that fits each video
and for humorous, trending effects (`videos/AUDIT_MUSICA.md`). This module replaces the 8-bit square waves of
`chiptune.py` with real-sounding instruments built by additive and noise synthesis:
- plucks (pizzicato, guitar, ukulele, harp/lyre);
- mallets (marimba, xylophone, vibraphone, glockenspiel, celesta, music box, steel drum);
- piano, bells, sleigh bells;
- reeds (bandoneón, clarinet), flute and whistle;
- brass, string pads, upright bass;
- drums: kit, brushes, timpani, toms, candombe drums (chico, repique, piano, madera), shaker, tambourine, claps.

There is a stereo-free reverb (FFT convolution, mono like the rest of the pipeline) and a Song class: tracks with gains,
automatic ducking under the voice clips read from the page (`<audio data-who>`), "stops" (the music cut dead for a
comic beat), and a check that no effect starts inside a spoken word.

Comic effects (`FX`) are ORIGINAL sounds with the function of today's trending meme effects (a deep boom with a tail for
reveals, a metal pipe that clangs and bounces for falls, a record scratch that stops everything, a sad trombone, "dun
dun duuun", a rimshot, crickets, a boing, slide whistles, a cash register, a bonk, a clown horn), never copies of any
recording.

Each reel has its own `banda_REEL.py` (in its folder) that composes the score with these pieces and writes
`hf3d/assets/audio/music.wav` and `sfx.wav`; `remezclar.py` then swaps the new mix into the rendered mp4.
"""
import json, os, re, wave
import numpy as np

SR = 48000
rng = np.random.default_rng(7)


# ---------------------------------------------------------------- basics
def T(d): return np.arange(max(1, int(d * SR))) / SR
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def seq(song, track, inst, notes, t0, beat, g=1.0, **kw):
    """place a phrase: notes = [(beat_offset, name_or_midi, length_in_beats), ...]; inst(freq, seconds)"""
    for off, nm, ln in notes:
        if nm is None: continue
        song.put(track, inst(f(nm), max(0.05, ln * beat), **kw), t0 + off * beat, g)
def mid(name):
    """'C4' -> 60, 'F#3' -> 54, 'Bb2' -> 46"""
    m = re.match(r"([A-G])([#b]?)(-?\d)", name); n = NOTE[m.group(1)] + {"#": 1, "b": -1, "": 0}[m.group(2)]
    return 12 * (int(m.group(3)) + 1) + n
def f(name): return hz(mid(name)) if isinstance(name, str) else hz(name)
def noise(d): return rng.uniform(-1, 1, len(T(d)))
def env(d, a=0.005, r=0.05, hold=None):
    n = len(T(d)); e = np.ones(n); A = max(1, int(a * SR)); R = max(1, min(int(r * SR), n))
    e[:A] = np.linspace(0, 1, A)[:min(A, n)] if A <= n else np.linspace(0, 1, n); e[n - R:] *= np.linspace(1, 0, R); return e
def edec(d, k): return np.exp(-T(d) * k)
def fft_filter(x, lo=None, hi=None, order=2):
    """zero-phase band filter by FFT with soft (Butterworth-like) slopes"""
    if len(x) < 8: return x
    X = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / SR) + 1e-9; g = np.ones_like(fr)
    if hi: g *= 1 / np.sqrt(1 + (fr / hi) ** (2 * order))
    if lo: g *= 1 / np.sqrt(1 + (lo / fr) ** (2 * order))
    return np.fft.irfft(X * g, len(x))
def lp(x, hi, order=2): return fft_filter(x, hi=hi, order=order)
def hp(x, lo, order=2): return fft_filter(x, lo=lo, order=order)
def bp(x, lo, hi, order=2): return fft_filter(x, lo=lo, hi=hi, order=order)
def norm(x, p=1.0): m = np.abs(x).max(); return x / m * p if m > 0 else x
def sat(x, drive=2.0): return np.tanh(x * drive) / np.tanh(drive)
def additive(fr, d, partials, vib=0.0, vib_rate=5.5, phase_rand=True):
    """partials: [(ratio, amp, decay_per_s)]; vib in semitones"""
    t = T(d); y = np.zeros(len(t)); fm = 1.0
    if vib: fm = 2 ** (vib / 12 * np.sin(2 * np.pi * vib_rate * t) * np.clip(t / 0.25, 0, 1))
    for r, a, k in partials:
        ff = fr * r
        if ff > SR / 2.2: continue
        ph = np.cumsum(ff * fm) / SR * 2 * np.pi if vib else 2 * np.pi * ff * t
        y += a * np.sin(ph + (rng.uniform(0, 6.28) if phase_rand else 0)) * np.exp(-k * t)
    return y
def reverb(x, rt=1.2, mix=0.2, pre=0.012, bright=5000):
    """mono convolution reverb: exponentially decaying filtered noise plus a few early reflections"""
    n = int(rt * 1.2 * SR); t = np.arange(n) / SR
    ir = rng.standard_normal(n) * np.exp(-6.9 * t / rt); ir = lp(ir, bright, 1); ir[:int(pre * SR)] = 0
    for dt, g in ((0.011, 0.5), (0.019, 0.35), (0.027, 0.3), (0.041, 0.2)): ir[int(dt * SR)] += g * 3
    ir /= np.sqrt(np.sum(ir ** 2)) + 1e-9
    L = len(x) + n; N = 1 << (L - 1).bit_length(); wet = np.fft.irfft(np.fft.rfft(x, N) * np.fft.rfft(ir, N), N)[:len(x)]
    return x * (1 - mix) + wet * mix * 1.4


# ---------------------------------------------------------------- pitched instruments (f = frequency in Hz)
def pluck(fr, d=1.2, bright=0.5, decay=2.5, body=True):
    """plucked string (guitar / harp / ukulele): decaying harmonics, the higher ones die faster, a short pick noise"""
    N = int(min(40, (SR / 2.4) // fr)); parts = [(k, (1 / k) ** (1.6 - bright) * (1 + 0.3 * np.sin(k * 1.7)), decay * (1 + (k - 1) * (0.55 - 0.35 * bright))) for k in range(1, N + 1)]
    y = additive(fr, d, parts) * env(d, 0.002, 0.06)
    pick = bp(noise(0.01), 1200, 7000) * edec(0.01, 400) * 0.25 * bright; y[:len(pick)] += pick
    return y
def pizz(fr, d=0.45): return pluck(fr, d, bright=0.32, decay=7.0) * 1.1
def guitar(fr, d=1.0): return pluck(fr, d, bright=0.45, decay=3.0)
def muted(fr, d=0.18): return pluck(fr, d, bright=0.3, decay=18.0)
def harp(fr, d=1.8): return pluck(fr, d, bright=0.62, decay=1.4)
def ukulele(fr, d=0.8): return pluck(fr, d, bright=0.7, decay=4.5)
def upright(fr, d=0.5): return lp(pluck(fr, d, bright=0.25, decay=5.0), 1800) * 1.4
def ebass(fr, d=0.4):
    t = T(d); y = (np.sin(2 * np.pi * fr * t) + 0.35 * np.sin(4 * np.pi * fr * t) + 0.15 * np.sin(6 * np.pi * fr * t)) * env(d, 0.004, 0.06) * edec(d, 2.5)
    return sat(y, 1.5)
def marimba(fr, d=0.7):
    y = additive(fr, d, [(1, 1.0, 5.5), (3.93, 0.32, 22), (9.0, 0.09, 55)]) * env(d, 0.001, 0.05)
    k = bp(noise(0.006), 800, 4000) * 0.2; y[:len(k)] += k; return y
def xylo(fr, d=0.45): return additive(fr, d, [(1, 1.0, 12), (3.0, 0.45, 30), (6.0, 0.18, 55)]) * env(d, 0.001, 0.04)
def vibes(fr, d=1.4):
    t = T(d); y = additive(fr, d, [(1, 1.0, 1.4), (4.0, 0.22, 5.0), (10.0, 0.05, 12)]) * env(d, 0.002, 0.2)
    return y * (1 - 0.25 * (0.5 + 0.5 * np.sin(2 * np.pi * 5.5 * t)))
def glock(fr, d=1.2): return additive(fr, d, [(1, 1.0, 2.6), (2.76, 0.35, 5.5), (5.4, 0.22, 9), (8.93, 0.12, 14)]) * env(d, 0.001, 0.15)
def celesta(fr, d=1.0): return additive(fr, d, [(1, 1.0, 3.5), (2.0, 0.35, 6), (3.0, 0.12, 10), (4.02, 0.05, 15)]) * env(d, 0.003, 0.15)
def musicbox(fr, d=0.9): return additive(fr, d, [(1, 1.0, 4.5), (3.0, 0.25, 12), (5.98, 0.12, 20)]) * env(d, 0.001, 0.1)
def bell(fr, d=2.2):
    t = T(d); I = 3.0 * np.exp(-t * 2.5)
    return np.sin(2 * np.pi * fr * t + I * np.sin(2 * np.pi * fr * 1.41 * t)) * np.exp(-t * 1.6) * env(d, 0.002, 0.3)
def steel(fr, d=1.1):
    y = additive(fr, d, [(1, 1.0, 3.2), (2.0, 0.55, 4.5), (3.01, 0.3, 7), (4.03, 0.18, 9), (5.1, 0.08, 14)]) * env(d, 0.004, 0.15)
    return y + 0.25 * additive(fr * 1.003, d, [(1, 1.0, 3.6)])
def piano(fr, d=1.6):
    B = 0.0004; parts = [(k * np.sqrt(1 + B * k * k), (1 / k) ** 1.1, 1.2 + 0.9 * k) for k in range(1, 14)]
    y = additive(fr, d, parts) * env(d, 0.002, 0.2); h = bp(noise(0.008), 500, 3000) * 0.15; y[:len(h)] += h; return y
def reed(fr, d, duty=0.32, det=4.0, bright=2600, trem=0.0):
    """bandoneón / accordion: two slightly detuned reeds (pulse waves), low-passed, a soft bellows envelope"""
    t = T(d); y = np.zeros(len(t))
    for cents in (-det, det):
        ff = fr * 2 ** (cents / 1200); ph = (ff * t + rng.uniform()) % 1; y += np.where(ph < duty, 1.0, -duty / (1 - duty))
    y = lp(y, bright, 2) * env(d, 0.03, 0.08)
    if trem: y *= 1 - trem * (0.5 + 0.5 * np.sin(2 * np.pi * 6 * t))
    return y * 0.5
def clarinet(fr, d, vib=0.08):
    return additive(fr, d, [(1, 1.0, 0), (3, 0.45, 0), (5, 0.25, 0), (7, 0.12, 0), (9, 0.06, 0)], vib=vib) * env(d, 0.025, 0.06)
def flute(fr, d, vib=0.12):
    y = additive(fr, d, [(1, 1.0, 0), (2, 0.18, 0), (3, 0.06, 0)], vib=vib) * env(d, 0.04, 0.08)
    return y + bp(noise(d), fr * 1.5, fr * 4) * 0.06 * env(d, 0.02, 0.08)
def whistle(fr, d, vib=0.18):
    return additive(fr, d, [(1, 1.0, 0), (2, 0.05, 0)], vib=vib, vib_rate=6) * env(d, 0.03, 0.06) + bp(noise(d), fr, fr * 2) * 0.04 * env(d, 0.02, 0.05)
def brass(fr, d, bright=1.0):
    t = T(d); swell = np.clip(t / 0.06, 0, 1); N = int(min(18, (SR / 2.4) // fr))
    y = np.zeros(len(t))
    for k in range(1, N + 1):
        amp = (1 / k) * np.clip(1.2 * bright * swell * (1.0 if k < 4 else np.exp(-(k - 4) / (2.5 * bright))), 0, 1)
        y += amp * np.sin(2 * np.pi * fr * k * t + rng.uniform(0, 6.28))
    return sat(y * env(d, 0.02, 0.08), 1.3) * 0.6
def strings(fr, d, a=0.25):
    t = T(d); y = np.zeros(len(t))
    for cents in (-7, 0, 7):
        ff = fr * 2 ** (cents / 1200); ph = (ff * t + rng.uniform()) % 1; y += 2 * ph - 1
    return lp(y, 2200, 2) * env(d, a, 0.3) * 0.25


# ---------------------------------------------------------------- drums and noises
def kick(g=1.0):
    d = 0.35; t = T(d); fr = 45 + 90 * np.exp(-t * 30); y = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 9)
    c = hp(noise(0.004), 2000) * 0.25; y[:len(c)] += c; return sat(y, 1.4) * g
def snare(g=1.0):
    d = 0.22; t = T(d); y = bp(noise(d), 1200, 7000) * np.exp(-t * 22) + 0.5 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30); return y * g * 0.7
def hat(g=1.0, d=0.05): return hp(noise(d), 7000) * edec(d, 70) * g * 0.5
def brush(g=1.0, d=0.18):
    t = T(d); return bp(noise(d), 1500, 6000) * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.5 * g * 0.35
def rim(g=1.0): d = 0.03; return (hp(noise(d), 2000) * edec(d, 200) + np.sin(2 * np.pi * 1700 * T(d)) * edec(d, 160)) * g * 0.5
def wood(fr=900, g=1.0): return additive(fr, 0.12, [(1, 1.0, 45), (2.3, 0.4, 70)]) * g
def shaker(g=1.0, d=0.09):
    t = T(d); return bp(noise(d), 4000, 10000) * np.sin(np.pi * np.clip(t / d, 0, 1)) * g * 0.3
def tamb(g=1.0, d=0.25):
    t = T(d); y = np.zeros(len(t))
    for k in range(6): y += np.sin(2 * np.pi * rng.uniform(4500, 9000) * t) * np.exp(-t * rng.uniform(10, 20))
    return (y * 0.15 + hp(noise(d), 5000) * np.exp(-t * 25) * 0.3) * g
def sleigh(g=1.0, d=0.35):
    t = T(d); y = np.zeros(len(t))
    for k in range(10):
        o = int(rng.uniform(0, 0.03) * SR); z = np.sin(2 * np.pi * rng.uniform(3000, 8000) * t) * np.exp(-t * rng.uniform(8, 16)); y[o:] += z[:len(t) - o]
    return y * 0.1 * g
def clap(g=1.0):
    d = 0.18; y = np.zeros(len(T(d)))
    for k, o in enumerate((0, 0.008, 0.016, 0.026)):
        z = bp(noise(0.06 if k == 3 else 0.012), 900, 5000) * edec(0.06 if k == 3 else 0.012, 60 if k == 3 else 250); i = int(o * SR); y[i:i + len(z)] += z[:len(y) - i]
    return y * g * 0.6
def tom(fr=120, g=1.0, d=0.45):
    t = T(d); ff = fr * (1 + 0.5 * np.exp(-t * 25)); return np.sin(2 * np.pi * np.cumsum(ff) / SR) * np.exp(-t * 7) * g
def timpani(fr=f("D2"), g=1.0, d=1.6):
    y = additive(fr, d, [(1, 1.0, 2.2), (1.5, 0.5, 3.0), (1.99, 0.35, 3.5), (2.44, 0.2, 4.5)])
    th = lp(noise(0.06), 300) * edec(0.06, 50); y[:len(th)] += th * 0.8; return y * g
def candombe(kind, g=1.0):
    """the three tambores of candombe: chico (high, short), repique (middle, open), piano (low, deep) and the 'madera' (stick on the shell)"""
    if kind == "madera": return wood(1300, 0.7 * g)
    fr, d, k = {"chico": (360, 0.12, 30), "repique": (240, 0.25, 14), "piano": (110, 0.45, 7)}[kind]
    t = T(d); ff = fr * (1 + 0.25 * np.exp(-t * 40)); y = np.sin(2 * np.pi * np.cumsum(ff) / SR) * np.exp(-t * k)
    y += bp(noise(d), 600, 3000) * np.exp(-t * k * 2.5) * 0.35; return y * g


# ---------------------------------------------------------------- comic effects (original sounds with the function of the trending ones)
def fx_boom(p=1.0):
    """deep hit with a long tail: the reveal / 'did he just say that' punch (the role of the viral bass boom)"""
    d = 2.2; t = T(d); fr = (40 + 45 * np.exp(-t * 6)) * p
    y = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 2.2) + 0.5 * np.sin(2 * np.pi * np.cumsum(fr * 2) / SR) * np.exp(-t * 3)
    y = sat(y * 1.8, 2.2); th = lp(noise(0.08), 900) * edec(0.08, 30); y[:len(th)] += th * 0.6
    return reverb(y, 1.6, 0.35) * 0.9
def fx_clang(p=1.0, bounces=4, ring=1.0):
    """a metal pipe hitting the floor and bouncing (the role of the viral metal pipe); ring > 1 shortens the tail"""
    def hit(g, d=1.6):
        y = additive(430 * p, d, [(1, 1.0, 1.6 * ring), (2.76, 0.7, 2.2 * ring), (5.40, 0.5, 3.0 * ring), (8.93, 0.35, 4.0 * ring), (13.34, 0.2, 6.0 * ring)])
        k = hp(noise(0.01), 3000) * edec(0.01, 300); y[:len(k)] += k * 0.8; return y * g
    out = np.zeros(int(2.4 * SR)); at, g, gap = 0.0, 1.0, 0.22
    for b in range(bounces):
        z = hit(g, 2.4 - at); i = int(at * SR); out[i:i + len(z)] += z[:len(out) - i]; at += gap; gap *= 0.62; g *= 0.5
    return reverb(out, 1.0, 0.2) * 0.6
def fx_scratch(p=1.0):
    """record scratch: a snippet dragged back and forth under a needle, then a stop (freezes the moment)"""
    d = 0.55; t = T(d); src = lp(noise(1.0), 3500) + 0.6 * np.sin(2 * np.pi * 220 * T(1.0)) * 0.3
    speed = np.where(t < 0.22, 2.2 * np.sin(2 * np.pi * 4.5 * t), -1.6 * np.exp(-(t - 0.22) * 6) * np.sin(2 * np.pi * 3 * (t - 0.22)))
    pos = 0.4 * SR + np.cumsum(speed) * p; idx = np.clip(pos.astype(int), 0, len(src) - 1)
    y = bp(src[idx], 300, 5000) * (0.4 + np.abs(speed) / 2.2) * env(d, 0.005, 0.08); return sat(y * 1.2, 1.5) * 0.8
def fx_sadtrombone(p=1.0):
    """'wah wah wah waaah' (a fail)"""
    out = []; notes = [mid("Bb3"), mid("A3"), mid("Ab3"), mid("G3")]
    for k, m in enumerate(notes):
        d = 0.38 if k < 3 else 1.3; y = brass(hz(m) * p, d, 0.8); tt = T(d)
        wah = 0.55 + 0.45 * np.sin(np.pi * np.clip(tt / min(d, 0.35), 0, 1))
        if k == 3: wah = 0.85 + 0.15 * np.sin(2 * np.pi * 6 * tt)               # the last note wobbles
        out.append(lp(y * wah, 1800) * env(d, 0.02, 0.12))
    return np.concatenate(out) * 1.2
def fx_dundun(p=1.0):
    """'dun dun duuun': dramatic stabs for a reveal"""
    def chord(ms, d, g):
        y = sum(brass(hz(m) * p, d, 1.1) + strings(hz(m) * p, d, 0.01) * 1.5 for m in ms); return y * g * env(d, 0.005, 0.1)
    a = chord([mid("C3"), mid("G3"), mid("C4"), mid("Eb4")], 0.32, 0.6); b = chord([mid("C3"), mid("G3"), mid("C4"), mid("Eb4")], 0.32, 0.6)
    c = chord([mid("B2"), mid("F#3"), mid("B3"), mid("D4")], 1.6, 0.75); gap = np.zeros(int(0.08 * SR))
    y = np.concatenate([a, gap, b, gap, c])
    for at in (0.0, 0.4, 0.8):
        k = timpani(f("C2") if at < 0.8 else f("B1"), 0.6, 1.2); i = int(at * SR); y[i:i + len(k)] += k[:len(y) - i]
    return reverb(y, 1.4, 0.25) * 0.5
def fx_rimshot(p=1.0):
    """'ba-dum-tss' after a bad joke"""
    y = np.zeros(int(1.3 * SR))
    for at, z in ((0.0, tom(160 * p, 0.8, 0.3)), (0.16, tom(110 * p, 0.9, 0.35)), (0.34, kick(0.6))):
        i = int(at * SR); y[i:i + len(z)] += z[:len(y) - i]
    cy = hp(noise(0.95), 5500) * np.exp(-T(0.95) * 4.5) * 0.45; i = int(0.34 * SR); y[i:i + len(cy)] += cy[:len(y) - i]
    return y * 0.8
def fx_crickets(p=1.0, d=1.6):
    """awkward silence"""
    y = np.zeros(len(T(d)))
    for c in np.arange(0.05, d - 0.2, 0.42):
        for k in range(3):
            tt = T(0.025); z = np.sin(2 * np.pi * 4600 * p * tt) * np.sin(np.pi * tt / 0.025); i = int((c + k * 0.04) * SR); y[i:i + len(z)] += z[:len(y) - i]
    return reverb(y * 0.25, 0.8, 0.3)
def fx_boing(p=1.0):
    d = 0.7; t = T(d); fr = 180 * p * (1 + 0.6 * np.exp(-t * 4) * np.sin(2 * np.pi * 14 * t) + 0.5 * t)
    y = np.sin(2 * np.pi * np.cumsum(fr) / SR) + 0.3 * np.sin(4 * np.pi * np.cumsum(fr) / SR); return y * np.exp(-t * 4) * env(d, 0.002, 0.1) * 0.7
def fx_slide_up(p=1.0, d=0.45):
    t = T(d); fr = 380 * p * 2 ** (2.2 * t / d); return (np.sin(2 * np.pi * np.cumsum(fr) / SR) + bp(noise(d), 800, 3000) * 0.08) * env(d, 0.02, 0.08) * 0.6
def fx_slide_down(p=1.0, d=0.7):
    t = T(d); fr = 1500 * p * 2 ** (-2.4 * t / d); return (np.sin(2 * np.pi * np.cumsum(fr) / SR) + bp(noise(d), 800, 3000) * 0.08) * env(d, 0.02, 0.1) * 0.6
def fx_cash(p=1.0):
    """'ka-ching'"""
    y = np.zeros(int(1.4 * SR)); dr = bp(noise(0.12), 600, 3000) * edec(0.12, 18) * 0.5; y[:len(dr)] += dr
    for at, fr in ((0.1, 2600), (0.16, 3300)):
        z = bell(fr * p, 1.1) * 0.6; i = int(at * SR); y[i:i + len(z)] += z[:len(y) - i]
    return y * 0.7
def fx_bonk(p=1.0):
    d = 0.4; t = T(d)
    w = additive(700 * p, d, [(1, 1.0, 30), (2.3, 0.5, 45)]); th = np.sin(2 * np.pi * np.cumsum(220 * p * np.exp(-t * 4)) / SR) * np.exp(-t * 14)
    return (w + th * 0.8) * 0.7
def fx_honk(p=1.0, n=2):
    def one(fr):
        d = 0.22; t = T(d); ph = (fr * t) % 1; y = np.where(ph < 0.4, 1.0, -0.66) * env(d, 0.01, 0.05)
        return bp(y, 400, 2500) * (1 + 0.1 * np.sin(2 * np.pi * 30 * t))
    parts = []
    for k in range(n): parts += [one(330 * p if k % 2 == 0 else 280 * p), np.zeros(int(0.06 * SR))]
    return np.concatenate(parts) * 0.6
def fx_tada(p=1.0):
    y = np.zeros(int(1.6 * SR))
    for k, m in enumerate(["C4", "E4", "G4"]):
        z = brass(f(m) * p, 0.12, 1.1); i = int(k * 0.07 * SR); y[i:i + len(z)] += z
    for m in ["C4", "E4", "G4", "C5"]:
        z = brass(f(m) * p, 1.2, 1.2) * env(1.2, 0.01, 0.5); i = int(0.21 * SR); y[i:i + len(z)] += z * 0.6
    z = timpani(f("C2"), 0.5, 1.2); i = int(0.21 * SR); y[i:i + len(z)] += z[:len(y) - i]
    return reverb(y, 1.2, 0.2) * 0.45
def fx_sparkle(p=1.0):
    y = np.zeros(int(1.2 * SR))
    for k, m in enumerate([84, 88, 91, 96, 100]):
        z = glock(hz(m) * p, 0.8) * 0.35; i = int(k * 0.045 * SR); y[i:i + len(z)] += z[:len(y) - i]
    return reverb(y, 1.0, 0.3)
def fx_rizz(p=1.0):
    """a smug glint: a bass swell under a sparkle (the role of the viral 'rizz' sound)"""
    d = 1.0; t = T(d); fr = 70 * p * (1 + 0.35 * np.clip(t / 0.5, 0, 1))
    b = sat(np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * np.clip(t / d, 0, 1)) * (0.7 + 0.3 * np.sin(2 * np.pi * 7 * t)), 2.0) * 0.6
    s = fx_sparkle(1.2 * p)[:len(b)]; y = b.copy(); y[:len(s)] += s * 0.7; return y
def fx_uhoh(p=1.0):
    """two falling xylophone notes: 'uh-oh'"""
    a, b = xylo(f("E5") * p, 0.25), xylo(f("C5") * p, 0.5); return np.concatenate([a, b]) * 0.6
def fx_whoosh(p=1.0, d=0.45):
    t = T(d); y = noise(d) * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2; lo = 300 * p; out = np.zeros(len(t))
    for k in range(6):
        seg = slice(int(k * len(t) / 6), int((k + 1) * len(t) / 6)); c = lo * 2 ** (2.5 * np.sin(np.pi * (k + 0.5) / 6)); out[seg] = bp(y[seg], c, c * 3)
    return lp(out, 6000) * 0.8
def fx_pop(p=1.0):
    d = 0.06; t = T(d); fr = 700 * p * np.exp(-t * 25) + 180; return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 50) * 0.8
def fx_toc(p=1.0): return wood(1100 * p, 0.8)
def fx_tap(p=1.0): return wood(1500 * p, 0.5)
def fx_clack(p=1.0): return wood(1700 * p, 0.55)
def fx_thud(p=1.0):
    d = 0.3; t = T(d); return (np.sin(2 * np.pi * np.cumsum(90 * p * np.exp(-t * 3)) / SR) * np.exp(-t * 14) + lp(noise(d), 500) * np.exp(-t * 30) * 0.5) * 0.9
def fx_ding(p=1.0): return bell(1760 * p, 1.6) * 0.5
def fx_chime(p=1.0):
    y = np.zeros(int(2.0 * SR))
    for k, m in enumerate(["G5", "C6", "E6"]):
        z = celesta(f(m) * p, 1.6) * 0.4; i = int(k * 0.09 * SR); y[i:i + len(z)] += z[:len(y) - i]
    return reverb(y, 1.2, 0.3)
def fx_drumroll(p=1.0, d=1.0):
    y = np.zeros(len(T(d + 0.3)))
    for at in np.arange(0, d, 0.035):
        z = snare(0.25 + 0.5 * at / d) * 0.6; i = int(at * SR); y[i:i + len(z)] += z[:len(y) - i]
    return y
def fx_tiptoe(p=1.0):
    y = np.zeros(int(0.9 * SR))
    for k, m in enumerate(["E4", "G4", "E4", "G4"]):
        z = pizz(f(m) * p, 0.25); i = int(k * 0.2 * SR); y[i:i + len(z)] += z[:len(y) - i]
    return y * 0.6
def fx_gull(p=1.0):
    """a seagull's call: a falling, raspy squawk"""
    d = 0.42; t = T(d); fr = (1700 - 900 * t / d) * p
    y = np.sin(2 * np.pi * np.cumsum(fr) / SR + 2.5 * np.sin(2 * np.pi * np.cumsum(fr * 0.5) / SR)) * env(d, 0.01, 0.1)
    return bp(y + 0.2 * noise(d), 800, 4000) * 0.4
def fx_peck(p=1.0): return wood(2200 * p, 0.6)
def fx_snore(p=1.0, d=1.2):
    t = T(d); y = lp(noise(d), 600) * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2 * (0.6 + 0.4 * np.sin(2 * np.pi * 28 * t)); return y * 0.6
def fx_rustle(p=1.0, d=0.3): t = T(d); return bp(noise(d), 2000, 8000) * np.abs(np.sin(np.pi * 3 * t / d)) * env(d, 0.01, 0.08) * 0.35
def fx_flipflop(p=1.0): d = 0.08; return (bp(noise(d), 500, 4000) * edec(d, 60) + np.sin(2 * np.pi * 220 * T(d)) * edec(d, 70) * 0.4) * 0.9
def fx_sip(p=1.0, d=0.6): t = T(d); return bp(noise(d), 1500, 5000) * (0.4 + 0.6 * np.abs(np.sin(2 * np.pi * 7 * t))) * env(d, 0.03, 0.1) * 0.25
def fx_confetti(p=1.0):
    y = fx_boom(1.6 * p)[: int(1.2 * SR)] * 0.5; s = fx_sparkle(p); y[:len(s)] += s; return y
def fx_printer(p=1.0, d=0.8):
    t = T(d); return lp(np.sin(2 * np.pi * 180 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 9 * t)) + 0.2 * noise(d), 1200) * env(d, 0.05, 0.1) * 0.25
def fx_door(p=1.0): return fx_thud(0.8 * p) * 1.2
def fx_heave(p=1.0): return fx_slide_up(0.6 * p, 0.3) * 0.5
def fx_fuse(p=1.0, d=0.5): t = T(d); return hp(noise(d), 3000) * (0.4 + 0.6 * (rng.uniform(size=len(t)) > 0.92)) * env(d, 0.01, 0.05) * 0.3
def fx_lur(p=1.0): return reverb(brass(f("D3") * p, 1.4, 0.9) * env(1.4, 0.15, 0.4), 1.5, 0.3) * 0.7

FX = {k[3:]: v for k, v in globals().items() if k.startswith("fx_")}
# the old 8-bit names in the reels' cues, mapped to the new sounds
OLD = {"tap": "tap", "clack": "clack", "pop": "pop", "whoosh": "whoosh", "chime": "chime", "sparkle": "sparkle", "ding": "ding",
       "bell": "ding", "thud": "thud", "boom": "boom", "sting": "dundun", "sad": "sadtrombone", "surprise": "slide_up",
       "item_get": "tada", "victory": "tada", "plop": "thud", "sack_plop": "thud", "click": "toc", "printer": "printer",
       "snore": "snore", "rustle": "rustle", "flutter": "rustle", "flap": "rustle", "chirp": "gull", "peck": "peck",
       "tiptoe": "tiptoe", "whistle": "slide_up", "flipflop": "flipflop", "door_bang": "door", "door_close": "door",
       "step": "toc", "sip": "sip", "relief": "chime", "idea": "ding", "heave": "heave", "fuse": "fuse", "puff": "whoosh",
       "lur": "lur", "creak": "toc"}


# ---------------------------------------------------------------- the song: tracks, voices, ducking, stops, writing
class Song:
    """A score on a timeline. tr(name) gives a track; put(track, y, t, g) places a sound. The voice clips are read from the
    page so the music ducks under them and effects can be checked against them."""
    def __init__(self, hf3d, dur=None, duck=0.3, bpm=110, cta_duck=0.16):
        self.hf3d = hf3d; html = open(os.path.join(hf3d, "index.html"), encoding="utf-8").read()
        self.dur = dur or float(re.search(r'data-composition-id="main"[^>]*data-duration="([0-9.]+)"', html).group(1))
        self.voices = []
        for tag in re.findall(r'<audio[^>]*data-who="[^"]*"[^>]*>', html):
            at = dict(re.findall(r'([\w-]+)="([^"]*)"', tag)); self.voices.append((float(at["data-start"]), float(at["data-start"]) + float(at["data-duration"]), at.get("data-text", "")))
        self.n = int(self.dur * SR); self.tracks = {}; self.sfx = np.zeros(self.n); self.stops = []; self.duck = duck; self.bpm = bpm; self.fxlog = []
        self.cta_duck = cta_duck                                   # deeper under the call to action and the cut-off date (lesson: "Vos sí")
    def b(self, k=1.0): return 60 / self.bpm * k
    def tr(self, name, gain=1.0, rv=0.15, rt=1.2, hi=None, lo=None):
        if name not in self.tracks: self.tracks[name] = {"x": np.zeros(self.n), "g": gain, "rv": rv, "rt": rt, "hi": hi, "lo": lo}
        return name
    def put(self, track, y, t, g=1.0):
        x = self.tracks[track]["x"]; i = int(t * SR)
        if i >= self.n or i + len(y) <= 0: return
        if i < 0: y = y[-i:]; i = 0
        n = min(len(y), self.n - i); x[i:i + n] += y[:n] * g
    def fx(self, name, t, g=0.6, p=1.0, allow_on_word=False, **kw):
        fn = FX[OLD.get(name, name)]; y = fn(p, **kw) if kw else fn(p); i = int(t * SR)
        if i < self.n: n = min(len(y), self.n - i); self.sfx[i:i + n] += y[:n] * g
        self.fxlog.append((round(t, 3), OLD.get(name, name), allow_on_word))
    def stop(self, t0, t1, ramp=0.03): self.stops.append((t0, t1, ramp))
    def on_word(self):
        """effects that start inside a spoken line (never allowed unless marked): (t, name, the line)"""
        return [(t, n, txt[:30]) for t, n, ok in self.fxlog for a, b, txt in self.voices if a + 0.05 < t < b - 0.05 and not ok]
    def music(self, fade_in=0.3, fade_out=1.2, master_hi=None):
        m = np.zeros(self.n)
        for nm, tk in self.tracks.items():
            x = tk["x"]
            if tk["hi"] or tk["lo"]: x = fft_filter(x, lo=tk["lo"], hi=tk["hi"])
            if tk["rv"] > 0: x = reverb(x, tk["rt"], tk["rv"])
            m += x * tk["g"]
        if master_hi: m = lp(m, master_hi)
        g = np.ones(self.n); r = int(0.12 * SR)
        for a, b, txt in self.voices:                            # duck under every line, with soft ramps
            dk = self.cta_duck if re.search(r"Coment|Pedidos|Escrib|Etiquet|diciembre", txt) else self.duck
            i0, i1 = int((a - 0.06) * SR), int((b + 0.1) * SR); g[max(0, i0):i1] = np.minimum(g[max(0, i0):i1], dk)
            g[max(0, i0 - r):max(0, i0)] = np.minimum(g[max(0, i0 - r):max(0, i0)], np.linspace(1, dk, len(g[max(0, i0 - r):max(0, i0)])))
            g[i1:i1 + r] = np.minimum(g[i1:i1 + r], np.linspace(dk, 1, len(g[i1:i1 + r])))
        for a, b, rp in self.stops:                               # comic stops: the music cut dead
            i0, i1, k = int(a * SR), int(b * SR), max(1, int(rp * SR)); g[i0:i1] = 0
            g[max(0, i0 - k):i0] *= np.linspace(1, 0, len(g[max(0, i0 - k):i0])); g[i1:i1 + k] *= np.linspace(0, 1, len(g[i1:i1 + k]))
        fi = int(fade_in * SR); g[:fi] *= np.linspace(0, 1, fi); fo = int(fade_out * SR); g[-fo:] *= np.linspace(1, 0, fo)
        return m * g
    def write(self, out_dir=None, music_peak=0.8, sfx_peak=0.9, master_hi=None):
        out = out_dir or os.path.join(self.hf3d, "assets", "audio"); os.makedirs(out, exist_ok=True)
        def w(path, x, peak):
            if peak:
                X = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / SR); X *= np.clip(fr / 25.0, 0, 1) ** 2; x = np.fft.irfft(X, len(x))   # no DC, no sub-audio rumble
                m = np.abs(x).max(); x = x / m * peak if m > 0 else x
            wv = wave.open(path, "wb"); wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes()); wv.close()
        w(os.path.join(out, "music.wav"), self.music(master_hi=master_hi), music_peak)
        w(os.path.join(out, "sfx.wav"), self.sfx + 1e-9, sfx_peak)
        amb = os.path.join(out, "ambience.wav")
        if os.path.exists(amb): w(amb, np.zeros(self.n), None)            # the 8-bit ambience is retired (crickets now live in the effects)
        bad = self.on_word(); print("music + sfx ->", out, "| effects on a word:", bad if bad else "none")
        return bad
