"""Builds cues.json (music, effects, ambience) from the scene's timing table, so sound and picture share one source."""
import json
T = dict(m1=0.15, b1=2.75, m2=2.85, lid=4.2, s1=4.45, b2=5.95, m3=6.05, note=7.6, b3=8.6, m4=8.7, duck=10.3, b4=11.0, m5=11.1, faint=11.85,
         faint1=12.75, brain=13.3, b5=14.05, m6=14.1, shades=14.95, b6=15.4, s2=15.55, slide=16.0, proc=16.9, proof=18.4, b7=20.9, m7=21.0, card=22.75)
DUR = 25.3
V = {"m1": (0.15, 2.52), "m2": (2.85, 1.56), "s1": (4.45, 1.5), "m3": (6.05, 1.55), "m4": (8.7, 1.8), "m5": (11.1, 2.48), "m6": (14.1, 1.25), "s2": (15.55, 1.104), "m7": (21.0, 1.651)}
sfx = []
for i, b in enumerate([T["b1"], T["b2"], T["b3"], T["b4"], T["b5"], T["proc"], T["b7"]]):
    sfx.append({"t": round(b - 0.09, 3), "s": "whoosh", "pitch": 1.0 + 0.05 * i, "gain": 0.8})
for i, b in enumerate([T["b1"], T["b2"], T["b3"], T["b4"], T["b5"]]):
    sfx.append({"t": round(b + 0.03, 3), "s": "pop", "pitch": 1.0 + 0.12 * i, "gain": 0.7})                 # the counter badge
sfx += [{"t": T["lid"], "s": "click"}, {"t": T["lid"] + 0.22, "s": "click", "pitch": 1.1},                     # café lid
        {"t": T["m3"] + 0.65, "s": "sad", "gain": 0.55},                                                       # the cactus droops
        {"t": T["note"], "s": "sparkle", "gain": 0.8}, {"t": T["note"] + 0.05, "s": "click", "pitch": 0.95},
        {"t": 9.6, "s": "pop", "pitch": 1.5, "gain": 0.5}, {"t": T["duck"], "s": "plop", "pitch": 1.3, "gain": 0.7}, {"t": T["duck"] + 0.3, "s": "click", "pitch": 1.05},
        {"t": T["faint"] + 0.05, "s": "sting", "gain": 0.6}, {"t": T["faint"] + 0.1, "s": "flutter", "pitch": 0.8, "gain": 0.6},
        {"t": T["brain"], "s": "click", "pitch": 0.9}, {"t": T["brain"] + 0.2, "s": "click", "pitch": 1.0},
        {"t": T["shades"] - 0.05, "s": "pop", "pitch": 1.25}, {"t": T["shades"], "s": "sparkle", "gain": 0.7}, {"t": T["m6"] + 0.5, "s": "click", "pitch": 1.15},
        {"t": T["s2"] + 0.05, "s": "surprise", "gain": 0.6}, {"t": T["slide"], "s": "tap", "gain": 0.8},
        {"t": T["proc"], "s": "printer", "d": T["proof"] - T["proc"] - 0.25, "gain": 0.7},
        {"t": T["proof"] - 0.25, "s": "ding"},
        {"t": T["card"], "s": "chime", "gain": 0.8}]
for i in range(5):
    sfx.append({"t": round(T["proc"] + 0.3 * i + 0.25, 3), "s": "tap", "pitch": 1.2 + 0.08 * i, "gain": 0.5})   # each copy done
    sfx.append({"t": round(T["proof"] + 0.33 + 0.17 * i, 3), "s": "tap", "pitch": 0.9 + 0.06 * i, "gain": 0.9})  # each polaroid lands
bar = [[[0, .5], [4, .5], [7, .5], [9, .5], [7, 1], [4, 1]], [[5, .5], [4, .5], [2, .5], [4, .5], [0, 2]],
       [[0, .5], [4, .5], [7, .5], [12, .5], [11, 1], [9, 1]], [[7, .5], [9, .5], [7, .5], [4, .5], [2, 2]]]
melody = [n for _ in range(3) for b in bar for n in b] + [[0, 4]]
duck = [[round(a - 0.05, 2), round(a + d + 0.08, 2), 0.36] for a, d in V.values()]
cues = {"duration": DUR, "sfx": sfx,
        "music": {"style": "ambient", "bpm": 120, "start": 0.0, "tonic": 0, "mode": "ionian", "chords": [0,5,9,7], "chord_beats": 8, "drone": False,
                  "duck": duck, "end_chord": {"t": T["card"]}, "fade_out": [24.6, DUR]},
        "ambience": [],   # no cicadas: high-passed noise gated at 37 Hz, heard as a buzz under the whole reel
        "_voices": "the voice lines live in hf3d/index.html (<audio data-who>); the music ducks under each one"}
json.dump(cues, open("cues.json", "w"), indent=1)
print(len(sfx), "effects")
