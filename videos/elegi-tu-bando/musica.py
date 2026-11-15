"""Music and effects for "Elegí tu bando" (videos/AUDIT_MUSICA.md): painting your own set.
A bright strummed ukulele with claps and a glockenspiel tune (G major, 116 bpm). The four-colour king gets a sparkle.
"¡Ese rey soy yo!": a smug glint (the role of the viral 'rizz' sound). "Bueno… vikingo sos.": a quick ba-dum-tss.
No effect on a word."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "biblioteca"))
from estilos import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
T = dict(s1=0.1, sweepS=3.05, m1=3.05, sweepM=4.35, kingCU=5.95, m2=6.3, s2=8.25, turn=9.4, m3=10.05, proof=11.95, cta=14.45, m4=14.55, card=18.4)
S = Song("hf3d", bpm=116, duck=0.28)
GL = [[(0, "B5", .5), (.5, "D6", .5), (1, "G6", 1), (2.5, "F#6", .5), (3, "D6", 1)], [(0, "C6", .5), (.5, "E6", .5), (1, "G6", 1), (2, "E6", 1), (3, "C6", 1)],
      [(0, "D6", .5), (.5, "B5", .5), (1, "G5", 1), (2, "A5", 1), (3, "B5", 1)], [(0, "A5", 1), (1, "F#5", 1), (2, "D5", 2)]]
ukulele_pop(S, 0.0, S.dur, ["G", "C", "Em", "D"], lead=loop(GL, 9))
final_chord(S, T["card"] + 0.05, ["G4", "B4", "D5", "G5"], inst=glock)
S.old_sfx("cues.json", skip=("surprise", ("chime", T["card"])))
S.fx("sparkle", T["kingCU"] - 0.02, 0.5)                                     # the king in four colours
S.fx("rizz", 9.4, 0.7, d=0.62)                                               # "¡Ese rey soy yo!" ... the smug glint
S.fx("rimshot", 11.87, 0.55, fast=True)                                      # "Bueno… vikingo sos." ba-dum-tss
S.fx("chime", T["card"] + 0.1, 0.5)
S.gallery_swipes()                                                           # the real photos changing
S.write()
