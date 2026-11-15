"""Music and effects for "El mantel" (videos/AUDIT_MUSICA.md): Christmas Eve.
C major, 112 bpm: sleigh bells, a pizzicato bass, celesta, and "Deck the Halls" (a traditional carol, public domain).
Before "Eso es un mantel." a record scratch cuts the carol; in the silence the pawn wobbles (a small boing) and tips over
(a bonk); "¿Y qué tiene?". El Mago's snap brings the carol back while the board assembles; a bell after the cut-off date;
the carol to the end. No effect on a word."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "biblioteca"))
from estilos import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
T = dict(s1=0.2, m1=2.3, wob=3.75, tip=4.1, s2=4.5, snap=6.0, m2=6.3, parts=6.6, pieces=9.75, m3=12.75, cal=12.8, ring=13.5, proof=15.25, cta=17.4, m4=17.5, card=22.0)
S = Song("hf3d", bpm=112, duck=0.28)
DECK = [[(0, "G5", 1.5), (1.5, "F5", .5), (2, "E5", 1), (3, "D5", 1)], [(0, "C5", 1), (1, "D5", 1), (2, "E5", 1), (3, "C5", 1)],
        [(0, "D5", .5), (.5, "E5", .5), (1, "F5", .5), (1.5, "D5", .5), (2, "E5", 1.5), (3.5, "D5", .5)], [(0, "C5", 1), (1, "B4", 1), (2, "C5", 2)]]
PROG = ["C", "C", "G7", "C"]
xmas(S, 0.0, 1.85, PROG, lead=loop(DECK, 1))
S.stop(1.85, T["snap"], 0.02)                                         # "Eso es un mantel." the carol scratched to a halt
xmas(S, T["snap"], T["m3"], PROG, lead=loop(DECK, 6), g=0.9)          # the snap: the board assembles to the carol
xmas(S, T["m3"], S.dur, PROG, lead=loop(DECK, 6, 0))
final_chord(S, T["card"] + 0.05, ["C4", "E4", "G4", "C5"], inst=celesta)
S.old_sfx("cues.json", skip=(("tap", T["tip"] + 0.27), ("chime", T["card"])))
S.fx("scratch", 1.79, 0.75)                                           # the trending record scratch
S.fx("boing", T["wob"] + 0.02, 0.35, 1.8)                             # the pawn wobbles on the fold
S.fx("bonk", T["tip"] + 0.27, 0.75)                                   # ... and tips over
S.fx("sparkle", T["snap"] + 0.05, 0.5)                                # El Mago's magic
S.fx("ding", 14.95, 0.45)                                             # after the cut-off date
S.fx("chime", T["card"] + 0.1, 0.5)
S.write()
