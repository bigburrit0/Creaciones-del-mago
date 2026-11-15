"""Music and effects for "¿Vikingo o caballero?" (videos/AUDIT_MUSICA.md): a mock-epic chess battle.
D minor, 100 bpm: timpani, low strings, horn calls. The vikings' early "¡Ganamos!" turns it to D major. "Jaque mate." in
silence, then a deep boom as the viking king falls. Papá Noel hears "mate": a candombe (Montevideo) with a marimba while
he asks for one; a ba-dum-tss after his line. The battle theme again, lighter, to the end. No effect on a word."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "biblioteca"))
from estilos import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
T = dict(m1=0.1, s1=2.35, m2=6.38, hopM=7.6, hopV=8.45, face=9.05, s2=9.85, slide=12.15, m3=12.85, tip=13.55, s3=14.3, react=17.5, proof=18.2, cta=20.75, m4=20.85, card=24.05)
S = Song("hf3d", bpm=100, duck=0.28)
MATE = [[(0, "A5", .5), (.5, "F#5", .5), (1, "D5", 1), (2.5, "E5", .5), (3, "F#5", 1)], [(0, "E5", .5), (.5, "C#5", .5), (1, "A4", 1), (2.5, "C#5", .5), (3, "E5", 1)]]
epic(S, 0.0, T["s2"] - 0.1, ["Dm", "Bb", "C", "A"])
epic(S, T["s2"] - 0.1, 12.7, ["D", "G", "A", "D"], g=0.9)                     # the vikings celebrate too soon (major)
S.stop(12.7, 14.2, 0.04)                                                     # "Jaque mate." ... the king falls
candombe(S, 14.2, T["proof"], ["D", "A7"], lead=loop(MATE, 3))               # "¿Mate? ¡Dale! ¡Cebame uno!"
epic(S, T["proof"], S.dur, ["Dm", "Bb", "C", "A"], drums=False, g=0.7)
final_chord(S, T["card"] + 0.05, ["D3", "A3", "D4", "F#4"], inst=harp)
S.old_sfx("cues.json", skip=("boom", "lur", "sting", ("chime", T["card"])))
S.fx("boom", T["tip"] + 0.03, 0.95)                                          # the trending boom: checkmate
S.fx("rimshot", T["react"], 0.6)                                             # ba-dum-tss after the mate joke
S.fx("chime", T["card"] + 0.1, 0.5)
S.gallery_swipes()                                                           # the real photos changing
S.write()
