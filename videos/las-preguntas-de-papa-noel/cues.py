"""cues.json from the scene's timing table. Music: a soft ambient bed since 2026-11-14 (the owner found the chiptune
lead loud and annoying): slow pads, nothing above 900 Hz, a sparse bell; the page plays it at volume 0.22. Viking palette (RESEARCH_AJEDREZ_2026.md, sound team): E Aeolian at 120 bpm with
a lur call; a page-turn rustle and a bell tick for each question on the list; a hop and a wooden clack for the king; a
sparkle for the ruler and a pop for the growth; the lost pawn: a clack on the board's edge, two bounces on the floor and
a sad little fall; the printer whir ONLY under its close-up; a pop and a ding for the reprint; the board: a whoosh out, a
thud when it stands; the list: a rustle, a thud of the roller on the floor and a long rolling rustle, the counter's spin
in rising ticks, a surprise. No ambience."""
import json
T = dict(s1=0.1, m1=1.4, q2=3.75, s2=3.8, m2=6.18, hop=6.2, ruler=6.95, grow=7.95, q3=8.65, s3=8.7, fall=9.0, m3=10.65, print0=10.7, print1=11.75, popBack=12.05,
         q4=12.4, s4=12.45, m4=13.35, lift=13.45, slide=13.85, stand=14.4, settle=14.95, drop=15.45, s5=15.65, m5=17.75, proof=19.6, cta=21.85, m6=21.95, card=24.8)
DUR = 27.2
V = {"s1": (0.1, 1.198), "m1": (1.4, 2.269), "s2": (3.8, 2.283), "m2": (6.18, 2.344), "s3": (8.7, 1.844), "m3": (10.65, 1.138),
     "s4": (12.45, 0.79), "m4": (13.35, 1.955), "s5": (15.65, 1.83), "m5": (17.75, 1.728), "m6": (21.95, 2.946)}
sfx = [{"t": 0.02, "s": "lur", "d": 1.0, "gain": 0.5}, {"t": 0.05, "s": "rustle", "gain": 0.5}]
for q in (T["q2"], T["q3"], T["q4"]):                                     # each new question: a rustle of the list, a tick of the counter
    sfx += [{"t": round(q - 0.25, 3), "s": "rustle", "gain": 0.45}, {"t": q, "s": "bell", "pitch": 1.5, "gain": 0.25}]
for i, w in enumerate((0.45, 0.95)):                                       # the stickers pop on "precio" and "fecha"
    sfx.append({"t": round(T["m1"] + w, 3), "s": "pop", "pitch": 1.1 + 0.15 * i, "gain": 0.5})
sfx += [{"t": T["hop"], "s": "sparkle", "gain": 0.5}, {"t": T["hop"] + 0.02, "s": "heave", "pitch": 1.4, "gain": 0.4}, {"t": T["hop"] + 0.42, "s": "clack", "gain": 0.5},
        {"t": T["ruler"], "s": "sparkle", "pitch": 1.2, "gain": 0.6}, {"t": T["ruler"] + 0.4, "s": "ding", "pitch": 1.1, "gain": 0.45},
        {"t": T["grow"], "s": "pop", "pitch": 0.75, "gain": 0.7}, {"t": T["grow"] + 0.03, "s": "sparkle", "pitch": 0.9, "gain": 0.5}]
fall_land = T["fall"] + 0.454
sfx += [{"t": T["fall"], "s": "clack", "pitch": 1.2, "gain": 0.45}, {"t": round(fall_land, 3), "s": "clack", "pitch": 0.8, "gain": 0.55},
        {"t": round(fall_land + 0.22, 3), "s": "clack", "pitch": 0.9, "gain": 0.35}, {"t": round(fall_land + 0.36, 3), "s": "tap", "pitch": 0.8, "gain": 0.3},
        {"t": round(fall_land + 0.12, 3), "s": "sad", "gain": 0.35}]
sfx += [{"t": T["print0"] - 0.05, "s": "printer", "d": round(T["print1"] - T["print0"] + 0.1, 2), "gain": 0.32},
        {"t": T["print1"] + 0.05, "s": "sparkle", "gain": 0.5}, {"t": T["popBack"], "s": "pop", "pitch": 1.2, "gain": 0.6}, {"t": T["popBack"] + 0.04, "s": "clack", "gain": 0.45},
        {"t": T["popBack"] + 0.1, "s": "ding", "pitch": 1.2, "gain": 0.5}]
sfx += [{"t": T["lift"], "s": "sparkle", "pitch": 0.9, "gain": 0.6}, {"t": T["slide"], "s": "whoosh", "pitch": 0.8, "gain": 0.6},
        {"t": T["stand"] + 0.48, "s": "thud", "gain": 0.6}, {"t": T["settle"] + 0.22, "s": "clack", "pitch": 0.9, "gain": 0.45}, {"t": T["settle"] + 0.26, "s": "clack", "pitch": 1.05, "gain": 0.35}]
land = T["drop"] + 0.34                                                       # the list: drops, the roller hits the floor, rolls away; the counter spins
sfx += [{"t": T["drop"], "s": "rustle", "gain": 0.7}, {"t": round(land, 3), "s": "thud", "pitch": 1.3, "gain": 0.5}]
for k in range(5):
    sfx.append({"t": round(land + 0.05 + k * 0.16, 3), "s": "rustle", "pitch": 1.0 - 0.05 * k, "gain": 0.5 - 0.07 * k})
for k in range(6):
    sfx.append({"t": round(T["drop"] + 0.05 + k * 0.11, 3), "s": "bell", "pitch": round(1.2 + 0.12 * k, 3), "gain": 0.3})
sfx += [{"t": T["drop"] + 0.72, "s": "surprise", "gain": 0.5}, {"t": T["m5"] + 1.0, "s": "pop", "pitch": 0.8, "gain": 0.45}, {"t": T["card"], "s": "chime", "gain": 0.7}]
for b in (T["q2"], T["q3"], T["m3"] - 0.05, T["q4"], T["cta"]):
    sfx.append({"t": round(b - 0.09, 3), "s": "whoosh", "gain": 0.5})
for i in range(3):
    sfx.append({"t": round(T["proof"] + 0.15 + i * 0.3 + 0.22, 3), "s": "tap", "pitch": 0.9 + 0.08 * i, "gain": 0.9})
# E Aeolian (semitones from C): E 4, F# 6, G 7, A 9, B 11, C 12, D 14, E 16
b1 = [[4, 1.5], [7, .5], [9, .5], [11, .5], [9, .5], [7, .5]]; b2 = [[4, 1], [2, 1], [4, 2]]
b3 = [[11, .5], [12, .5], [11, .5], [9, .5], [7, 1], [9, 1]]; b4 = [[7, .5], [6, .5], [4, 1], [4, 2]]
b5 = [[16, 1], [14, 1], [11, 1], [12, 1]]; b6 = [[16, 4]]
melody = [n for b in (b1, b2, b3, b4, b1, b2, b3, b4, b1, b2, b3, b4, b5, b6) for n in b]
duck = [[round(a - 0.05, 2), round(a + d + 0.08, 2), 0.34] for a, d in V.values()]
cues = {"duration": DUR, "sfx": sfx,
        "music": {"style": "ambient", "bpm": 120, "start": 0.0, "tonic": 4, "mode": "aeolian", "chords": [4,0,7,2], "chord_beats": 8, "drone": True,
                  "duck": duck, "end_chord": {"t": T["card"]}, "fade_out": [26.4, DUR]},
        "ambience": [], "_voices": "the voice lines live in hf3d/index.html (<audio data-who>); the music ducks under each one"}
json.dump(cues, open("cues.json", "w"), indent=1); print(len(sfx), "effects")
