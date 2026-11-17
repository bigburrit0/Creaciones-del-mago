"""cues.json for El piano (G mixolydian, summer), from the scene's timing table. Music: the soft ambient bed (C ionian, page volume 0.22), OUT while the ocarina
plays (it is the music then: a duck window at 0 from 0.5 s before the first note to 0.3 s after the last). Effects never on
a spoken word and never under a note: a whoosh for the lift, a pop as the caps land, a whoosh into the product beat and the
CTA, the card chime."""
import json
T = dict(lift=4.95, caps=6.0, oca=6.5, ocaEnd=10.55, prod=15.8, cta=17.9, card=21.8)
DUR = 24.3
V = {"c1": (0.2, 2.828), "c3": (3.2, 1.634), "c2": (10.75, 1.951), "c4": (12.9, 2.75), "c5": (17.95, 3.737)}
sfx = [{"t": T["lift"] + 0.02, "s": "whoosh", "pitch": 1.2, "gain": 0.3},
       {"t": T["caps"] + 0.3, "s": "pop", "gain": 0.3},
       {"t": T["prod"] - 0.08, "s": "whoosh", "gain": 0.28},
       {"t": T["cta"] - 0.09, "s": "whoosh", "gain": 0.28},
       {"t": T["card"], "s": "chime", "gain": 0.6}]
duck = [[round(a - 0.05, 2), round(a + d + 0.08, 2), 0.18 if k in ("c5",) else 0.34] for k, (a, d) in V.items()]
duck.append([round(T["oca"] - 0.5, 2), round(T["ocaEnd"] + 0.3, 2), 0.0])
cues = {"duration": DUR, "sfx": sfx,
        "music": {"style": "ambient", "bpm": 120, "start": 0.0, "tonic": 7, "mode": "mixolydian", "chords": [7, 5, 0, 7], "chord_beats": 8, "drone": False,
                  "duck": duck, "end_chord": {"t": T["card"]}, "fade_out": [23.5, DUR]},
        "ambience": [], "_voices": "the voice lines live in hf3d/index.html (<audio data-who>); the ocarina is its own clip (aud-oca)"}
inside = [(e["s"], e["t"]) for e in sfx for a, d in list(V.values()) + [(T["oca"], T["ocaEnd"] - T["oca"])] if a + 0.05 < e["t"] < a + d - 0.05 and e["s"] != "chime"]
json.dump(cues, open("cues.json", "w"), indent=1); print(len(sfx), "effects; inside a line or a note:", inside)
