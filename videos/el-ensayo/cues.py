"""cues.json for El ensayo, from the scene's timing table. Music: the soft ambient bed (C ionian, page volume 0.22), OUT while the ocarina
plays (it is the music then: a duck window at 0 from 0.5 s before the first note to 0.3 s after the last). Effects never on
a spoken word and never under a note: a whoosh for the lift, a pop as the caps land, a whoosh into the product beat and the
CTA, the card chime."""
import json
T = dict(lift=5.75, caps=6.5, oca=7.0, ocaEnd=11.55, prod=15.95, cta=18.05, card=22.1, cal=11.8)
DUR = 24.6
V = {"d1": (0.2, 2.585), "d2": (4.4, 1.212), "d3": (11.75, 3.985), "d4": (18.1, 3.914)}
sfx = [{"t": T["lift"] + 0.02, "s": "whoosh", "pitch": 1.2, "gain": 0.3},
       {"t": T["caps"] + 0.25, "s": "pop", "gain": 0.3},
       {"t": T["cal"] - 0.2, "s": "whoosh", "pitch": 0.9, "gain": 0.26},
       {"t": T["prod"] - 0.08, "s": "whoosh", "gain": 0.28},
       {"t": T["cta"] - 0.09, "s": "whoosh", "gain": 0.28},
       {"t": T["card"], "s": "chime", "gain": 0.6}]
duck = [[round(a - 0.05, 2), round(a + d + 0.08, 2), 0.18 if k in ("d3", "d4") else 0.34] for k, (a, d) in V.items()]
duck.append([round(T["oca"] - 0.5, 2), round(T["ocaEnd"] + 0.3, 2), 0.0])
duck.append([2.85, 3.9, 0.0])            # the squeak (a real sound of the scene, the ocarina): the bed out under it too
cues = {"duration": DUR, "sfx": sfx,
        "music": {"style": "ambient", "bpm": 120, "start": 0.0, "tonic": 0, "mode": "ionian", "chords": [0, 5, 7, 0], "bells": True, "chord_beats": 8, "drone": False,
                  "duck": duck, "end_chord": {"t": T["card"]}, "fade_out": [23.8, DUR]},
        "ambience": [], "_voices": "the voice lines live in hf3d/index.html (<audio data-who>); the ocarina is its own clip (aud-oca)"}
inside = [(e["s"], e["t"]) for e in sfx for a, d in list(V.values()) + [(T["oca"], T["ocaEnd"] - T["oca"])] if a + 0.05 < e["t"] < a + d - 0.05 and e["s"] != "chime"]
json.dump(cues, open("cues.json", "w"), indent=1); print(len(sfx), "effects; inside a line or a note:", inside)
