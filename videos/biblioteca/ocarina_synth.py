#!/usr/bin/env python3
"""A digital (synthesised) 12-hole ocarina for the ocarina reels. The owner asked on 15/11 for a synthesised sound; the
reels label it "Sonido digital" on screen, so nobody takes it for a recording of the real piece.

  python3 ocarina_synth.py PHRASE OUT.wav OUT_notes.json     PHRASE: oda | escala | rambla | nochedepaz | chirrido

The tone: a near-sine fundamental with weak 2nd and 3rd harmonics, a breathy chiff at each attack, a little breath noise,
a slow vibrato that comes in after 0.25 s. The notes file gives, for each note, its onset and length (s), its name and the
holes left OPEN on an Alto C 12-hole (a simplified cumulative chart: the sub-holes first, then from the tail to the
mouthpiece, then the thumbs). The 3D model (ocarina3d.js) reads it to light the holes.
Melodies: "Oda a la alegría" (Beethoven, 1824) and "Noche de paz" (Gruber, 1818) are public domain, played plainly; the
rambla phrase is original; the scale is a scale.
"""
import json, sys, wave
import numpy as np

SR = 48000
NAMES = ["A4", "B4", "C5", "D5", "E5", "F5", "G5", "A5", "B5", "C6", "D6", "E6", "F6"]
OPEN_ORDER = ["SR", "SL", "R4", "R3", "R2", "R1", "L4", "L3", "L2", "L1", "TR", "TL"]   # A4: all closed; each step up opens one more
MIDI = {"A4": 69, "B4": 71, "C5": 72, "D5": 74, "E5": 76, "F5": 77, "G5": 79, "A5": 81, "B5": 83, "C6": 84, "D6": 86, "E6": 88, "F6": 89}

PHRASES = {
    # bpm, [(note, beats)]
    "oda": (196, [("E5", 1), ("E5", 1), ("F5", 1), ("G5", 1), ("G5", 1), ("F5", 1), ("E5", 1), ("D5", 1),
                  ("C5", 1), ("C5", 1), ("D5", 1), ("E5", 1), ("E5", 1.5), ("D5", 0.5), ("D5", 2)]),
    "escala": (176, [(n, 1) for n in NAMES[:-1]] + [("F6", 2)]),
    "rambla": (132, [("G5", 0.5), ("A5", 0.5), ("G5", 0.5), ("E5", 0.5), ("C6", 1), ("B5", 0.5), ("A5", 0.5),
                     ("G5", 0.5), ("E5", 0.5), ("F5", 0.5), ("A5", 0.5), ("G5", 2)]),
    "nochedepaz": (168, [("G5", 1.5), ("A5", 0.5), ("G5", 1), ("E5", 2.5), ("G5", 1.5), ("A5", 0.5), ("G5", 1), ("E5", 3)]),
}


def tone(f, d, rng, vib=True):
    n = int(d * SR); t = np.arange(n) / SR
    v = 1 + (0.0035 * np.sin(2 * np.pi * 5.2 * t) * np.clip((t - 0.25) / 0.3, 0, 1) if vib else 0)
    ph = 2 * np.pi * np.cumsum(f * v) / SR
    x = np.sin(ph) + 0.06 * np.sin(2 * ph + 0.3) + 0.018 * np.sin(3 * ph + 1.1)
    a = np.clip(t / 0.045, 0, 1) ** 1.5; r = np.clip((d - t) / 0.07, 0, 1); x *= a * r
    br = rng.standard_normal(n); br = np.convolve(br, np.ones(9) / 9, "same")
    chiff = br * np.exp(-t / 0.025) * 0.35                                   # the breathy start of each note
    x += chiff + br * 0.02 * a * r                                           # a little breath under the tone
    return x


def phrase(name):
    rng = np.random.default_rng(7)
    if name == "chirrido":                                                   # an overblown squeak: a breathy screech
        d = 0.6; n = int(d * SR); t = np.arange(n) / SR
        f = 1480 * (1 + 0.04 * np.sin(2 * np.pi * 9 * t)) * (1 + 0.08 * t)
        ph = 2 * np.pi * np.cumsum(f) / SR
        x = np.sign(np.sin(ph)) * 0.35 + np.sin(2 * ph) * 0.3 + rng.standard_normal(n) * 0.25
        x *= np.clip(t / 0.02, 0, 1) * np.clip((d - t) / 0.08, 0, 1)
        return x, [{"t": 0.0, "d": d, "note": "squeak", "open": []}]
    bpm, notes = PHRASES[name]; beat = 60 / bpm
    out = np.zeros(int((sum(b for _, b in notes) * beat + 0.4) * SR)); t0 = 0.0; ev = []
    for nm, b in notes:
        d = b * beat; f = 440 * 2 ** ((MIDI[nm] - 69) / 12)
        x = tone(f, d - 0.02, rng); i = int(t0 * SR); out[i:i + len(x)] += x
        k = NAMES.index(nm); ev.append({"t": round(t0, 3), "d": round(d, 3), "note": nm, "open": OPEN_ORDER[:k]})
        t0 += d
    return out, ev


def write(path, x):
    x = x / max(1e-9, np.abs(x).max()) * 0.6
    y = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(y.tobytes())


if __name__ == "__main__":
    name, wav, js = sys.argv[1:4]
    x, ev = phrase(name); write(wav, x)
    json.dump({"phrase": name, "duration": round(len(x) / SR, 3), "notes": ev}, open(js, "w"), indent=1)
    print(name, round(len(x) / SR, 2), "s,", len(ev), "notes")
