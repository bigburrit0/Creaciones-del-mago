"""cues.json from the scene's timing table. Music: the soft ambient bed (C ionian, page volume 0.22), OUT while the ocarina
plays (it is the music then: a duck window at 0 from 0.5 s before the first note to 0.3 s after the last). Effects never on
a spoken word and never under a note: a whoosh for the lift, a pop as the caps land, a whoosh into the product beat and the
CTA, the card chime."""
import json
T = dict(lift=5.35, caps=7.85, oca=8.4, ocaEnd=13.7, prod=16.35, cta=18.65, card=22.8)
DUR = 25.3
V = {"a1": (0.2, 2.322), "a3": (2.65, 2.622), "a2": (6.7, 1.442), "a4": (14.75, 1.476), "a5": (18.7, 3.992)}
sfx = [{"t": T["lift"] + 0.02, "s": "whoosh", "pitch": 1.2, "gain": 0.3},
       {"t": T["caps"] + 0.3, "s": "pop", "gain": 0.3},
       {"t": T["prod"] - 0.08, "s": "whoosh", "gain": 0.28},
       {"t": T["cta"] - 0.09, "s": "whoosh", "gain": 0.28},
       {"t": T["card"], "s": "chime", "gain": 0.6}]
duck = [[round(a - 0.05, 2), round(a + d + 0.08, 2), 0.18 if k in ("a5",) else 0.34] for k, (a, d) in V.items()]
duck.append([round(T["oca"] - 0.5, 2), round(T["ocaEnd"] + 0.3, 2), 0.0])
cues = {"duration": DUR, "sfx": sfx,
        "music": {"style": "ambient", "bpm": 120, "start": 0.0, "tonic": 0, "mode": "ionian", "chords": [0, 5, 7, 0], "chord_beats": 8, "drone": False,
                  "duck": duck, "end_chord": {"t": T["card"]}, "fade_out": [24.5, DUR]},
        "ambience": [], "_voices": "the voice lines live in hf3d/index.html (<audio data-who>); the ocarina is its own clip (aud-oca)"}
inside = [(e["s"], e["t"]) for e in sfx for a, d in list(V.values()) + [(T["oca"], T["ocaEnd"] - T["oca"])] if a + 0.05 < e["t"] < a + d - 0.05 and e["s"] != "chime"]
json.dump(cues, open("cues.json", "w"), indent=1); print(len(sfx), "effects; inside a line or a note:", inside)
