"""Music and effects for "Culpa de las piezas" (videos/AUDIT_MUSICA.md): a sore loser.
A tango (A minor, 120 bpm: bandoneón, pizzicato bass, string stabs) while he blames the pieces. His own vikings turn to
stare at him: the tango stops, "dun dun duuun". "Las piezas no pierden. Vos sí." in silence, then a deep boom. He wants
his own set for Christmas: sleigh bells and celesta (C major) to the end; a bell after the cut-off date. No effect on a word."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "biblioteca"))
from estilos import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
T = dict(tip=0.1, s1=0.55, stare=2.7, m1=4.5, vos=6.48, s2=7.35, navidad=9.13, m2=9.9, print0=9.85, print1=13.2, s3=13.5, m3=14.7, cal=14.75, ring=15.2, proof=16.75, cta=19.0, m4=19.05, card=21.7)
S = Song("hf3d", bpm=120, duck=0.28)
JB = [[(0, "E5", 1), (1, "E5", 1), (2, "E5", 2)], [(0, "E5", 1), (1, "E5", 1), (2, "E5", 2)], [(0, "E5", 1), (1, "G5", 1), (2, "C5", 1.5), (3.5, "D5", .5)], [(0, "E5", 4)]]
tango(S, 0.0, 2.58, ["Am", "E7"])
S.stop(2.58, 7.3, 0.03)                                                      # the stare, and "Vos sí."
xmas(S, 7.3, S.dur, ["C", "C", "G7", "C"], lead=loop(JB, 8))                 # "¡Para Navidad!" (Jingle Bells, public domain)
final_chord(S, T["card"] + 0.05, ["C4", "E4", "G4", "C5"], inst=celesta)
S.old_sfx("cues.json", skip=("sting", "surprise", "item_get", ("chime", T["card"])))
S.fx("dundun", 2.58, 0.6)                                                    # his own vikings turn to stare at him
S.fx("boom", 6.98, 0.85)                                                     # "Las piezas no pierden. Vos sí." ... boom
S.fx("ding", 16.36, 0.45)                                                    # after the cut-off date
S.fx("chime", T["card"] + 0.1, 0.5)
S.gallery_swipes()                                                           # the real photos changing
S.write()
