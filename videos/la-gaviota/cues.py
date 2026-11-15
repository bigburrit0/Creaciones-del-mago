"""cues.json from the scene's timing table. Music: the soft ambient bed (G mixolydian, summer; "style": "ambient", page
volume 0.22). No wave noise (the buzz lesson): the sea is only seen. Effects never on a spoken word: the seagull's calls
(a low chirp), a whoosh for its swoop, a pop for the swap, soft taps as the travel pieces hop, a click for the fold and
for the cap, three pecks, a sting for the miffed gull."""
import json
T = dict(s1=0.15, gull=2.95, grab=3.75, away=4.6, s2=4.7, magic=5.6, m1=5.8, swap=6.0, off=7.15, fold=8.0, len=9.35, into=10.75, cap=12.2, back=12.6, miffed=14.0, s3=14.15, leave=15.95, sunset=16.0, proof=17.7, cta=19.9, m2=20.0, card=23.45)
pecks = [13.2, 13.5, 13.8]
DUR = 26.0
V = {"s1": (0.15, 2.649), "s2": (4.7, 0.819), "m1": (5.8, 6.408), "s3": (14.15, 1.804), "m2": (20.0, 3.538)}
sfx = [{"t": T["gull"] + 0.1, "s": "chirp", "pitch": 0.55, "gain": 0.4}, {"t": T["grab"] - 0.3, "s": "whoosh", "pitch": 1.2, "gain": 0.45}, {"t": T["grab"], "s": "tap", "pitch": 1.2, "gain": 0.4},
       {"t": T["grab"] + 0.25, "s": "chirp", "pitch": 0.6, "gain": 0.45}, {"t": T["back"] + 0.6, "s": "tap", "pitch": 0.9, "gain": 0.3}]
sfx += [{"t": T["cap"] + 0.15, "s": "click", "pitch": 0.8, "gain": 0.45}]          # the hops and the fold happen under El Mago's long line: silent (never an effect on a word)
for p in pecks:
    sfx.append({"t": p + 0.08, "s": "peck", "pitch": 0.8, "gain": 0.45})
sfx += [{"t": T["leave"] + 0.1, "s": "chirp", "pitch": 0.55, "gain": 0.35}, {"t": T["card"], "s": "chime", "gain": 0.6}]
for b in (T["gull"], T["magic"], T["back"] - 0.05, T["cta"]):
    sfx.append({"t": round(b - 0.09, 3), "s": "whoosh", "gain": 0.3})
sfx.append({"t": round(T["proof"] + 0.37, 3), "s": "tap", "pitch": 0.9, "gain": 0.7})
duck = [[round(a - 0.05, 2), round(a + d + 0.08, 2), 0.18 if k in ("m1", "m2") else 0.34] for k, (a, d) in V.items()]
cues = {"duration": DUR, "sfx": sfx,
        "music": {"style": "ambient", "bpm": 120, "start": 0.0, "tonic": 7, "mode": "mixolydian", "chords": [7, 5, 0, 7], "chord_beats": 8, "drone": False,
                  "duck": duck, "end_chord": {"t": T["card"]}, "fade_out": [25.2, DUR]},
        "ambience": [], "_voices": "the voice lines live in hf3d/index.html (<audio data-who>); the music ducks under each one"}
inside = [(e["s"], e["t"]) for e in sfx for a, d in V.values() if a + 0.05 < e["t"] < a + d - 0.05 and e["s"] not in ("chime",)]   # never on a word: must stay empty
json.dump(cues, open("cues.json", "w"), indent=1); print(len(sfx), "effects; inside a line:", inside)
