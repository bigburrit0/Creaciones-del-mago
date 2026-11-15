"""cues.json from the scene's timing table. Music: a soft ambient bed (the owner found the chiptune lead loud and
annoying, 2026-11-14): slow E Aeolian pads with a root drone, a sparse bell, nothing above 900 Hz. Viking palette (RESEARCH_AJEDREZ_2026.md, sound team: E Aeolian, 120 bpm, a lur
call) for Papá Noel's rematch; the mate: a bell, a wobble and a thud, a sad little tune; the stare: a soft scrape per
viking turning round and a sting when the last one faces him, a gulp-like surprise as he sweats; a pop on "Vos sí"; a
cheer on "¡Para Navidad!" (item_get); the printer whir ONLY under its close-up, a ding when the king is done; the calendar
page: a whoosh in, a chime when the 23 is circled. No ambience."""
import json
T = dict(tip=0.1, s1=0.55, stare=2.7, m1=4.5, vos=6.48, s2=7.35, navidad=9.13, m2=9.9, print0=9.85, print1=13.2, s3=13.5, m3=14.7, cal=14.75, ring=15.2,
         proof=16.75, cta=19.0, m4=19.05, card=21.7)
DUR = 24.2
V = {"s1": (0.55, 1.976), "m1": (4.5, 2.448), "s2": (7.35, 2.389), "m2": (9.9, 3.427), "s3": (13.5, 1.05), "m3": (14.7, 1.608), "m4": (19.05, 2.729)}
sfx = [{"t": 0.02, "s": "bell", "pitch": 0.8, "gain": 0.4}, {"t": T["tip"] + 0.05, "s": "tap", "pitch": 0.8, "gain": 0.35}, {"t": T["tip"] + 0.2, "s": "tap", "pitch": 0.85, "gain": 0.3},
       {"t": T["tip"] + 0.6, "s": "thud", "gain": 0.7}, {"t": T["tip"] + 0.7, "s": "sad", "gain": 0.35}]
for i in range(13):                                                          # each viking turning round: a soft scrape, a touch lower each time
    sfx.append({"t": round(T["stare"] + i * 0.055 + 0.15, 3), "s": "tap", "pitch": round(0.75 - 0.012 * i, 3), "gain": 0.28})
sfx += [{"t": T["stare"] + 1.4, "s": "sting", "gain": 0.55}, {"t": T["stare"] + 1.25, "s": "surprise", "pitch": 0.7, "gain": 0.35},
        {"t": T["vos"] + 0.55, "s": "pop", "pitch": 0.85, "gain": 0.45}, {"t": T["navidad"], "s": "item_get", "gain": 0.6},
        {"t": T["print0"] - 0.05, "s": "printer", "d": round(T["print1"] - T["print0"] + 0.05, 2), "gain": 0.3}, {"t": T["print1"], "s": "ding", "gain": 0.5},
        {"t": T["print1"] + 0.03, "s": "sparkle", "gain": 0.45}, {"t": T["cal"], "s": "whoosh", "pitch": 1.1, "gain": 0.5}, {"t": T["cal"] + 0.28, "s": "tap", "gain": 0.6},
        {"t": T["ring"] + 0.1, "s": "chime", "gain": 0.55}, {"t": T["card"], "s": "chime", "gain": 0.7}]
for b in (1.0, T["stare"] - 0.1, 3.95, T["s2"] - 0.05, 9.8, 11.55, T["m3"] - 0.05, T["cta"]):
    sfx.append({"t": round(b - 0.09, 3), "s": "whoosh", "gain": 0.45})
for i in range(3):
    sfx.append({"t": round(T["proof"] + 0.15 + i * 0.3 + 0.22, 3), "s": "tap", "pitch": 0.9 + 0.08 * i, "gain": 0.9})
# E Aeolian (semitones from C): E 4, F# 6, G 7, A 9, B 11, C 12, D 14, E 16
b1 = [[4, 1.5], [7, .5], [9, .5], [11, .5], [9, .5], [7, .5]]; b2 = [[4, 1], [2, 1], [4, 2]]
b3 = [[11, .5], [12, .5], [11, .5], [9, .5], [7, 1], [9, 1]]; b4 = [[7, .5], [6, .5], [4, 1], [4, 2]]
b5 = [[16, 1], [14, 1], [11, 1], [12, 1]]; b6 = [[16, 4]]
melody = [n for b in (b1, b2, b3, b4, b1, b2, b3, b4, b1, b5, b6) for n in b]
duck = [[round(a - 0.05, 2), round(a + d + 0.08, 2), 0.18 if k in ("m1", "m4") else 0.34] for k, (a, d) in V.items()]   # deeper under the punchline and the CTA: "Vos sí" and "Comentá PEDIR" must read in the mix + [[T["stare"], T["m1"], 0.5]]
cues = {"duration": DUR, "sfx": sfx,
        "music": {"style": "ambient", "bpm": 120, "start": 0.0, "tonic": 4, "mode": "aeolian", "chords": [4, 0, 7, 2], "chord_beats": 8, "drone": True,
                  "duck": duck, "end_chord": {"t": T["card"]}, "fade_out": [23.4, DUR]},
        "ambience": [], "_voices": "the voice lines live in hf3d/index.html (<audio data-who>); the music ducks under each one (and under the stare)"}
json.dump(cues, open("cues.json", "w"), indent=1); print(len(sfx), "effects")
