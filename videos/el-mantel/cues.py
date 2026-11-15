"""cues.json from the scene's timing table. Music: the soft ambient bed (C ionian, warm, Christmas Eve; "style": "ambient",
page volume 0.22). Effects never on a spoken word: a soft "toc" when the pawn tips over on the fold, El Mago's snap (a pop),
a whoosh as the calendar page drops in, the proof's tap, the chime on the card. The board's parts and the pieces land under
El Mago's long line: silent."""
import json
T = dict(s1=0.2, m1=2.3, tip=4.1, s2=4.5, snap=6.0, m2=6.3, m3=12.75, proof=15.25, cta=17.4, m4=17.5, card=22.0)
DUR = 24.5
V = {"s1": (0.2, 1.586), "m1": (2.3, 1.365), "s2": (4.5, 1.333), "m2": (6.3, 5.896), "m3": (12.75, 2.149), "m4": (17.5, 4.175)}
sfx = [{"t": T["tip"] + 0.27, "s": "tap", "pitch": 0.7, "gain": 0.4},          # the pawn lands on the cloth
       {"t": T["snap"] + 0.02, "s": "pop", "gain": 0.45},                        # El Mago's snap
       {"t": T["m3"] - 0.15, "s": "whoosh", "pitch": 0.9, "gain": 0.3},          # the calendar page drops in
       {"t": T["card"], "s": "chime", "gain": 0.6}]
for b in (T["cta"],):
    sfx.append({"t": round(b - 0.09, 3), "s": "whoosh", "gain": 0.3})
sfx.append({"t": round(T["proof"] + 0.37, 3), "s": "tap", "pitch": 0.9, "gain": 0.7})
duck = [[round(a - 0.05, 2), round(a + d + 0.08, 2), 0.18 if k in ("m3", "m4") else 0.34] for k, (a, d) in V.items()]
cues = {"duration": DUR, "sfx": sfx,
        "music": {"style": "ambient", "bpm": 120, "start": 0.0, "tonic": 0, "mode": "ionian", "chords": [0, 5, 7, 0], "chord_beats": 8, "drone": False,
                  "duck": duck, "end_chord": {"t": T["card"]}, "fade_out": [23.7, DUR]},
        "ambience": [], "_voices": "the voice lines live in hf3d/index.html (<audio data-who>); the music ducks under each one"}
inside = [(e["s"], e["t"]) for e in sfx for a, d in V.values() if a + 0.05 < e["t"] < a + d - 0.05 and e["s"] not in ("chime",)]   # never on a word: must stay empty
json.dump(cues, open("cues.json", "w"), indent=1); print(len(sfx), "effects; inside a line:", inside)
