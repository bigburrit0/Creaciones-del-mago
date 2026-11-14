"""cues.json from the scene's timing table. Music: the soft ambient bed (C major, cozy; "style": "ambient", page volume
0.22). Effects never on a spoken word: a little pop for the eager dog pawn's hop; a soft whoosh and a tap for the cat
queen's leap; three soft taps of her paw; a plop and a small thud when the pawn lands on the rug; a sting for the
smug cats. No ambience."""
import json
T = dict(s1=0.15, m1=2.5, hop=4.35, leap=6.05, step=6.75, look=7.1, land=9.42, s2=9.75, m2=11.85, smug=13.15, proof=14.8, cta=17.0, m3=17.1, card=20.55)
taps = [7.75, 8.35, 8.95]
DUR = 23.0
V = {"s1": (0.15, 2.227), "m1": (2.5, 1.584), "s2": (9.75, 1.919), "m2": (11.85, 0.759), "m3": (17.1, 3.532)}
sfx = [{"t": T["hop"], "s": "pop", "pitch": 1.3, "gain": 0.4}, {"t": T["hop"] + 0.45, "s": "tap", "pitch": 1.0, "gain": 0.35},
       {"t": T["leap"], "s": "whoosh", "pitch": 1.4, "gain": 0.35}, {"t": T["leap"] + 0.55, "s": "tap", "pitch": 1.1, "gain": 0.35}, {"t": T["step"] + 0.3, "s": "tap", "pitch": 1.2, "gain": 0.25}]
for i, tt in enumerate(taps):
    sfx.append({"t": round(tt + 0.14, 3), "s": "tap", "pitch": round(1.3 - 0.08 * i, 3), "gain": 0.4})
sfx += [{"t": T["land"] - 0.05, "s": "plop", "pitch": 1.2, "gain": 0.45}, {"t": T["land"], "s": "thud", "pitch": 1.4, "gain": 0.35},
        {"t": T["smug"] + 0.1, "s": "sting", "gain": 0.4}, {"t": T["card"], "s": "chime", "gain": 0.6}]
for b in (T["hop"] - 0.2, T["leap"] - 0.05, T["cta"]):        # whooshes only on cuts between lines
    sfx.append({"t": round(b - 0.09, 3), "s": "whoosh", "gain": 0.35})
sfx.append({"t": round(T["proof"] + 0.15 + 0.22, 3), "s": "tap", "pitch": 0.9, "gain": 0.7})
duck = [[round(a - 0.05, 2), round(a + d + 0.08, 2), 0.18 if k in ("m2", "m3") else 0.34] for k, (a, d) in V.items()]
cues = {"duration": DUR, "sfx": sfx,
        "music": {"style": "ambient", "bpm": 120, "start": 0.0, "tonic": 0, "mode": "ionian", "chords": [0, 5, 9, 7], "chord_beats": 8, "drone": False,
                  "duck": duck, "end_chord": {"t": T["card"]}, "fade_out": [22.2, DUR]},
        "ambience": [], "_voices": "the voice lines live in hf3d/index.html (<audio data-who>); the music ducks under each one"}
inside = [   # never on a word: this must stay empty
    (e["s"], e["t"]) for e in sfx for a, d in V.values() if a + 0.05 < e["t"] < a + d - 0.05 and e["s"] not in ("chime",)]
json.dump(cues, open("cues.json", "w"), indent=1); print(len(sfx), "effects; inside a line:", inside)
