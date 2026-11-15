"""Music and effects for "Las preguntas de Papá Noel" (videos/AUDIT_MUSICA.md): a TV quiz.
F major, 120 bpm: a walking bass, swung brushes, a vibraphone tune. A quiz-show ding before each question. The list
unrolls to the floor: a slide whistle down. "Las demás… en comentarios.": a ba-dum-tss. No effect on a word."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "biblioteca"))
from estilos import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
T = dict(s1=0.1, m1=1.4, q2=3.75, s2=3.8, m2=6.18, hop=6.2, ruler=6.95, grow=7.95, q3=8.65, s3=8.7, fall=9.0, m3=10.65, print0=10.7, print1=11.75, popBack=12.05, q4=12.4, s4=12.45, m4=13.35, lift=13.45, slide=13.85, stand=14.4, settle=14.95, drop=15.45, s5=15.65, m5=17.75, proof=19.6, cta=21.85, m6=21.95, card=24.8)
S = Song("hf3d", bpm=120, duck=0.28)
VB = [[(0, "A5", 1), (1, "C6", .5), (1.5, "A5", .5), (2, "F5", 2)], [(0, "D5", .5), (.5, "F5", .5), (1, "A5", 1), (2, "G5", 2)],
      [(0, "Bb5", 1), (1, "A5", .5), (1.5, "G5", .5), (2, "F5", 1), (3, "D5", 1)], [(0, "E5", 1), (1, "G5", 1), (2, "C6", 2)]]
quiz(S, 0.0, S.dur, ["F", "Dm", "Gm7", "C7"], lead=loop(VB, 13))
final_chord(S, T["card"] + 0.05, ["F3", "A3", "C4", "E4"], inst=vibes)
S.old_sfx("cues.json", skip=("lur", ("chime", T["card"])))
for q in ("q2", "q3", "q4"): S.fx("ding", T[q] - 0.03, 0.4, 1.2)            # quiz-show ding: next question
S.fx("slide_down", 15.33, 0.6, d=0.3)                                        # the list unrolls to the floor
S.fx("rimshot", 19.5, 0.6)                                                   # "Las demás… en comentarios." ba-dum-tss
S.fx("chime", T["card"] + 0.1, 0.5)
S.write()
