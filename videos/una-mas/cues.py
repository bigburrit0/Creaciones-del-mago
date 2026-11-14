"""cues.json from the scene's timing table. Music: a soft ambient bed since 2026-11-14 (the owner found the chiptune
lead loud and annoying): slow pads, nothing above 900 Hz, a sparse bell; the page plays it at volume 0.22. Viking palette (RESEARCH_AJEDREZ_2026.md, sound team): E Aeolian at 120 bpm with
a lur call; a soft wooden clack for every piece that lands on the board (the montage's rhythm); the printer whir ONLY under
the printer close-ups (it is a buzzy sound: never under the whole reel); snores at night; a ding and a chime at 32/32.
No ambience. The print schedule mirrors the one in hf3d/index.html."""
import json
T = dict(m1=0.1, firstPop=2.65, s1=5.05, m2=6.9, dusk0=7.4, s2=9.75, m3=10.7, night=11.3, doze=11.5, lastPop=13.9, dawn=13.75, s3=14.25, spare=15.3, m4=15.4, proof=18.15, cta=20.5, m5=20.6, card=24.5)
DUR = 27.2
V = {"m1": (0.1, 2.538), "s1": (5.05, 1.763), "m2": (6.9, 0.561), "s2": (9.75, 0.85), "m3": (10.7, 0.549), "s3": (14.25, 0.929), "m4": (15.4, 2.667), "m5": (20.6, 3.819)}
pops = [T["firstPop"]] + [T["firstPop"] + (T["lastPop"] - 0.25 - T["firstPop"]) * ((i - 1) / 30) ** 0.85 for i in range(2, 32)] + [T["lastPop"]]
sfx = [{"t": 0.02, "s": "lur", "d": 1.1, "gain": 0.6}]
for i, p in enumerate(pops):                                                       # a soft clack per piece, a touch higher as the set fills
    sfx.append({"t": round(p, 3), "s": "clack", "pitch": round(0.95 + 0.012 * i, 3), "gain": 0.32})
for a, b in [(0.05, T["firstPop"]), (3.65, 4.4), (T["night"], 12.4), (T["spare"], T["spare"] + 0.75)]:
    sfx.append({"t": a, "s": "printer", "d": round(b - a, 2), "gain": 0.35})
sfx += [{"t": T["lastPop"], "s": "ding"}, {"t": T["lastPop"] + 0.05, "s": "chime", "gain": 0.6}, {"t": T["lastPop"] + 0.16, "s": "surprise", "gain": 0.5},
        {"t": T["doze"] + 0.5, "s": "snore", "d": 0.9, "gain": 0.6}, {"t": T["doze"] + 1.6, "s": "snore", "d": 0.9, "pitch": 0.9, "gain": 0.6},
        {"t": T["spare"] + 0.76, "s": "ding", "pitch": 1.2, "gain": 0.6}, {"t": T["m4"] + 2.0, "s": "pop", "pitch": 1.2, "gain": 0.6},
        {"t": T["card"], "s": "chime", "gain": 0.7}]
for b in [3.65, 4.4, 8.7, T["dawn"], T["spare"], T["cta"]]:
    sfx.append({"t": round(b - 0.09, 3), "s": "whoosh", "gain": 0.55})
for i in range(3):
    sfx.append({"t": round(T["proof"] + 0.15 + i * 0.3 + 0.22, 3), "s": "tap", "pitch": 0.9 + 0.08 * i, "gain": 0.9})
# E Aeolian (semitones from C): E 4, F# 6, G 7, A 9, B 11, C 12, D 14, E 16
b1 = [[4, 1.5], [7, .5], [9, .5], [11, .5], [9, .5], [7, .5]]; b2 = [[4, 1], [2, 1], [4, 2]]
b3 = [[11, .5], [12, .5], [11, .5], [9, .5], [7, 1], [9, 1]]; b4 = [[7, .5], [6, .5], [4, 1], [4, 2]]
b5 = [[16, 1], [14, 1], [11, 1], [12, 1]]; b6 = [[16, 4]]
melody = [n for b in (b1, b2, b3, b4, b1, b2, b3, b4, b1, b2, b3, b4, b5, b6) for n in b]
duck = [[round(a - 0.05, 2), round(a + d + 0.08, 2), 0.34] for a, d in V.values()] + [[T["night"], T["dawn"], 0.55]]
cues = {"duration": DUR, "sfx": sfx,
        "music": {"style": "ambient", "bpm": 120, "start": 0.0, "tonic": 4, "mode": "aeolian", "chords": [4,0,7,2], "chord_beats": 8, "drone": True,
                  "duck": duck, "end_chord": {"t": T["card"]}, "fade_out": [26.4, DUR]},
        "ambience": [], "_voices": "the voice lines live in hf3d/index.html (<audio data-who>); the music ducks under each one"}
json.dump(cues, open("cues.json", "w"), indent=1); print(len(sfx), "effects")
