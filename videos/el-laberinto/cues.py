"""cues.json from the scene's timing table. Music: the soft ambient bed (D dorian with a root drone: old stone, a little
mystery; "style": "ambient", page volume 0.22). Effects never on a spoken word: the Minotaur lowers its horns in silence (under
"Minotauro contra Hércules"), a thud and a whoosh for Hercules' club, a tap when Papá Noel's mitten
hits a dead end, a pop for the magic tape measures, a click as the second one locks, the chime on the card."""
import json
T = dict(m1=0.25, mino=1.55, herc=2.7, lean=3.7, s1=4.3, m2=6.9, m3=9.75, tape1=10.75, tape2=11.75, s2=13.15, proof=14.95, cta=17.15, m4=17.25, card=20.3)
DUR = 23.0
V = {"m1": (0.25, 2.425), "s1": (4.3, 2.121), "m2": (6.9, 2.489), "m3": (9.75, 3.108), "s2": (13.15, 1.474), "m4": (17.25, 2.7)}
sfx = [{"t": T["herc"] + 0.1, "s": "thud", "pitch": 0.8, "gain": 0.5}, {"t": T["herc"] + 0.45, "s": "whoosh", "pitch": 1.1, "gain": 0.4}]
sfx += [{"t": 6.55, "s": "tap", "pitch": 0.7, "gain": 0.3}]                                    # his mitten finds a dead end (after "¿Y por dónde se sale?")
sfx += [{"t": T["m3"] - 0.25, "s": "pop", "gain": 0.35}]                                       # the tape measures appear, just before the line
sfx += [{"t": T["s2"] - 0.3, "s": "click", "pitch": 0.9, "gain": 0.4}]                          # the second tape locks
sfx += [{"t": T["card"], "s": "chime", "gain": 0.6}]
for b in (T["lean"], T["m2"] - 0.15, T["cta"]):
    sfx.append({"t": round(b - 0.09, 3), "s": "whoosh", "gain": 0.3})
sfx.append({"t": round(T["proof"] + 0.37, 3), "s": "tap", "pitch": 0.9, "gain": 0.7})
duck = [[round(a - 0.05, 2), round(a + d + 0.08, 2), 0.18 if k in ("m2", "m4") else 0.34] for k, (a, d) in V.items()]
cues = {"duration": DUR, "sfx": sfx,
        "music": {"style": "ambient", "bpm": 120, "start": 0.0, "tonic": 2, "mode": "dorian", "chords": [2, 0, 7, 2], "chord_beats": 8, "drone": True,
                  "duck": duck, "end_chord": {"t": T["card"]}, "fade_out": [22.2, DUR]},
        "ambience": [], "_voices": "the voice lines live in hf3d/index.html (<audio data-who>); the music ducks under each one"}
inside = [(e["s"], e["t"]) for e in sfx for a, d in V.values() if a + 0.05 < e["t"] < a + d - 0.05 and e["s"] not in ("chime",)]   # never on a word: must stay empty
json.dump(cues, open("cues.json", "w"), indent=1); print(len(sfx), "effects; inside a line:", inside)
