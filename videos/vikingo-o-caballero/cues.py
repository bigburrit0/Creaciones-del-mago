"""cues.json (music, effects) from the scene's timing table. Palette from RESEARCH_AJEDREZ_2026.md (sound team): a medieval
tune in D Dorian at 100 bpm (lute-like lead, root-fifth bass), a viking lur for Papá Noel, a wooden clack for every piece
that lands, a bell for the mate, a thud for the king. No ambience (the buzz lesson)."""
import json
T = dict(m1=0.1, s1=2.35, m2=6.38, hopM=7.6, hopV=8.45, face=9.05, s2=9.85, slide=12.15, m3=12.85, tip=13.55, s3=14.3, react=17.5, proof=18.2, cta=20.75, m4=20.85, card=24.05)
DUR = 26.8
V = {"m1": (0.1, 2.166), "s1": (2.35, 3.95), "m2": (6.38, 1.098), "s2": (9.85, 2.124), "m3": (12.85, 0.699), "s3": (14.3, 3.151), "m4": (20.85, 3.125)}
sfx = [{"t": 0.02, "s": "boom", "gain": 0.45},
       {"t": T["s1"] - 0.1, "s": "lur", "d": 1.0, "gain": 0.8},                                   # Papá Noel's vikings
       {"t": T["m2"] - 0.05, "s": "bell", "pitch": 0.75, "gain": 0.35},                            # El Mago's knights
       {"t": T["hopM"], "s": "pop", "pitch": 1.2, "gain": 0.5}, {"t": T["hopM"] + 0.55, "s": "clack"},
       {"t": T["hopV"], "s": "pop", "pitch": 1.1, "gain": 0.5}, {"t": T["hopV"] + 0.55, "s": "clack", "pitch": 0.95},
       {"t": T["face"] + 0.15, "s": "sting", "gain": 0.45},
       {"t": T["slide"], "s": "whoosh", "pitch": 0.8, "gain": 0.7}, {"t": T["slide"] + 0.55, "s": "pop", "pitch": 0.9, "gain": 0.5},
       {"t": T["slide"] + 0.6, "s": "clack", "pitch": 1.05}, {"t": T["slide"] + 0.62, "s": "bell", "gain": 0.6}, {"t": T["slide"] + 0.97, "s": "clack", "pitch": 0.85, "gain": 0.6},
       {"t": T["tip"] + 0.05, "s": "tap", "pitch": 0.8, "gain": 0.4}, {"t": T["tip"] + 0.55, "s": "thud"},
       {"t": T["s3"], "s": "tap", "gain": 0.6},
       {"t": T["card"], "s": "chime", "gain": 0.7}]
for b in [T["m2"], T["hopM"] - 0.05, T["hopV"] - 0.05, T["cta"]]:
    sfx.append({"t": round(b - 0.09, 3), "s": "whoosh", "gain": 0.6})
for f in range(8):                                                                                  # the vikings' cheering clatter
    for k in (0.349, 1.047):
        sfx.append({"t": round(T["s2"] + 0.1 + f * 0.07 + k, 3), "s": "clack", "pitch": 1.25 + 0.03 * f, "gain": 0.22})
for i in range(3):
    sfx.append({"t": round(T["proof"] + 0.15 + i * 0.3 + 0.22, 3), "s": "tap", "pitch": 0.9 + 0.08 * i, "gain": 0.9})
b1 = [[2, .5], [4, .5], [5, .5], [9, .5], [7, 1], [5, 1]]; b2 = [[4, 1], [2, 1], [0, 1], [2, 1]]
b3 = [[9, .5], [7, .5], [9, .5], [12, .5], [11, 1], [9, 1]]; b4 = [[7, .5], [5, .5], [4, .5], [0, .5], [2, 2]]
b5 = [[14, 1], [12, 1], [9, 1], [11, 1]]; b6 = [[14, 4]]
melody = [n for b in (b1, b2, b3, b4, b1, b2, b3, b4, b5, b6) for n in b]
duck = [[round(a - 0.05, 2), round(a + d + 0.08, 2), 0.34] for a, d in V.values()]
cues = {"duration": DUR, "sfx": sfx,
        "music": {"bpm": 100, "start": 0.15, "melody": melody, "chords": [2, 0, 2, 9, 2, 0, 7, 2, 2, 9, 2], "duck": duck,
                  "end_chord": {"t": T["card"], "notes": [2, 5, 9, 14]}, "fade_out": [26.0, DUR]},
        "ambience": [], "_voices": "the voice lines live in hf3d/index.html (<audio data-who>); the music ducks under each one"}
json.dump(cues, open("cues.json", "w"), indent=1); print(len(sfx), "effects")
