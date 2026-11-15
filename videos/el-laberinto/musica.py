"""Music and effects for "El laberinto" (videos/AUDIT_MUSICA.md): ancient Greece, in fun.
D dorian, 92 bpm. An epic opening (timpani, low strings, horn calls, a lyre) for "Minotauro contra Hércules"; a deep boom
as Hercules raises his club. Papá Noel lost in the walls: only a sparse lyre; after "¿Y por dónde se sale?" the music
stops for one cricket. El Mago, deadpan, "Se sale ganando": a quick ba-dum-tss. The tapes: the lyre and the flute; "¡Qué
tablero!", a ta-da into the real photo. It ends on a D major chord. No effect on a word."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "biblioteca"))
from estilos import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
T = dict(m1=0.25, mino=1.55, herc=2.7, lean=3.7, s1=4.3, trace=4.45, traceEnd=6.75, m2=6.9, m3=9.75, tapes=9.5, tape1=10.75, tape2=11.75, s2=13.15, proof=14.95, cta=17.15, m4=17.25, card=20.3)
S = Song("hf3d", bpm=92, duck=0.28)
FL = [[(0, "A5", 1.5), (1.5, "G5", .5), (2, "F5", 1), (3, "E5", 1)], [(0, "D5", 2), (2, "E5", 1), (3, "C5", 1)],
      [(0, "F5", 1), (1, "G5", 1), (2, "A5", 1.5), (3.5, "C6", .5)], [(0, "B5", 1), (1, "A5", 1), (2, "D5", 2)]]
epic(S, 0.0, T["lean"] + 0.6, ["Dm", "C", "Dm", "A"])            # its last bar overlaps the lyre: a crossfade, not a cut
greek(S, 0.0, T["lean"], ["Dm", "C", "Dm", "A"], g=0.7)
greek(S, T["lean"], 6.45, ["Dm", "Em", "Dm", "C"], g=0.55)                  # lost in the walls: the lyre alone (and a soft drum)
S.stop(6.45, T["m2"] + 0.1, 0.04)                                           # one cricket of awkward silence
greek(S, T["m2"], T["m3"], ["Dm", "G", "Dm", "A"], g=0.4)            # quieter under the deadpan line
greek(S, T["m3"], T["proof"], ["Dm", "C", "Bb", "A"], lead=loop(FL, 4))     # the tape measures, the whole board
greek(S, T["proof"], S.dur, ["Dm", "G", "Dm", "A", "Dm", "C", "Bb", "A"], lead=loop(FL, 6, 2), g=0.9)
epic(S, T["card"], S.dur, ["D"], horn=True, drums=False, g=0.6)
final_chord(S, T["card"] + 0.05, ["D3", "A3", "D4", "F#4", "A4"], inst=harp)
S.old_sfx("cues.json", skip=(("thud", T["herc"] + 0.1), ("chime", T["card"]), ("tap", 6.55)))
S.stop(T["herc"] + 0.05, T["herc"] + 0.55, 0.05)                          # the music holds its breath for the club
S.fx("boom", T["herc"] + 0.08, 1.0)                                         # Hercules raises his club
S.fx("crickets", 6.45, 0.6, d=0.42)                                         # "¿Y por dónde se sale?" ... a cricket
S.fx("rimshot", T["m2"] + 2.5, 0.6, fast=True)                              # "Se sale ganando." ba-dum-tss
S.fx("tada", 14.66, 0.55)                                                   # "¡Qué tablero!" -> the real photo
S.fx("chime", T["card"] + 0.1, 0.5)
S.write()
