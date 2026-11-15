"""cues.json from the scene's timing table. Music: a soft ambient bed since 2026-11-14 (the owner found the chiptune
lead loud and annoying): slow pads, nothing above 900 Hz, a sparse bell; the page plays it at volume 0.22. The medieval tune of reel 1 (D Dorian, 100 bpm); a sparkle swish per rank as it
repaints and a soft tap per piece; a pop and a chime at each of the king's colour steps; a 'surprise' on "¡Ese rey soy
yo!"; a hop for the king turning round. No ambience, no printer."""
import json
T = dict(s1=0.1, sweepS=3.05, m1=3.05, sweepM=4.35, kingCU=5.95, m2=6.3, s2=8.25, turn=9.4, m3=10.05, proof=11.95, cta=14.45, m4=14.55, card=18.4)
steps = [6.45, 6.9, 7.35]
DUR = 21.6
V = {"s1": (0.1, 2.824), "m1": (3.05, 1.889), "m2": (6.3, 1.176), "s2": (8.25, 1.117), "m3": (10.05, 1.8), "m4": (14.55, 3.705)}
sfx = [{"t": 0.02, "s": "bell", "pitch": 0.75, "gain": 0.4}]
for base in (T["sweepS"], T["sweepM"]):
    for rank in range(2):
        sfx.append({"t": round(base + rank * 0.55, 3), "s": "sparkle", "pitch": 1.0 + 0.1 * rank, "gain": 0.7})
        for f in range(0, 8, 2):
            sfx.append({"t": round(base + rank * 0.55 + f * 0.06 + 0.03, 3), "s": "tap", "pitch": 1.3 + 0.05 * f, "gain": 0.22})
for i, s in enumerate(steps):
    sfx += [{"t": s, "s": "pop", "pitch": 1.1 + 0.1 * i, "gain": 0.7}, {"t": s + 0.02, "s": "sparkle", "pitch": 1.2 + 0.1 * i, "gain": 0.6}]
sfx += [{"t": steps[2] + 0.25, "s": "chime", "gain": 0.6}, {"t": T["s2"] + 0.05, "s": "surprise", "gain": 0.5},
        {"t": T["turn"], "s": "pop", "pitch": 0.9, "gain": 0.6}, {"t": T["turn"] + 0.35, "s": "clack"},
        {"t": T["card"], "s": "chime", "gain": 0.7}]
for b in (T["sweepS"], T["sweepM"], T["kingCU"], T["cta"]):
    sfx.append({"t": round(b - 0.09, 3), "s": "whoosh", "gain": 0.55})
for i in range(3):
    sfx.append({"t": round(T["proof"] + 0.15 + i * 0.3 + 0.22, 3), "s": "tap", "pitch": 0.9 + 0.08 * i, "gain": 0.9})
b1 = [[2, .5], [4, .5], [5, .5], [9, .5], [7, 1], [5, 1]]; b2 = [[4, 1], [2, 1], [0, 1], [2, 1]]
b3 = [[9, .5], [7, .5], [9, .5], [12, .5], [11, 1], [9, 1]]; b4 = [[7, .5], [5, .5], [4, .5], [0, .5], [2, 2]]
b5 = [[14, 1], [12, 1], [9, 1], [11, 1]]; b6 = [[14, 4]]
melody = [n for b in (b1, b2, b3, b4, b1, b2, b3, b5, b6) for n in b]
duck = [[round(a - 0.05, 2), round(a + d + 0.08, 2), 0.34] for a, d in V.values()]
cues = {"duration": DUR, "sfx": sfx,
        "music": {"style": "ambient", "bpm": 120, "start": 0.0, "tonic": 2, "mode": "dorian", "chords": [2,7,0,2], "chord_beats": 8, "drone": True,
                  "duck": duck, "end_chord": {"t": T["card"]}, "fade_out": [20.8, DUR]},
        "ambience": [], "_voices": "the voice lines live in hf3d/index.html (<audio data-who>); the music ducks under each one"}
json.dump(cues, open("cues.json", "w"), indent=1); print(len(sfx), "effects")
