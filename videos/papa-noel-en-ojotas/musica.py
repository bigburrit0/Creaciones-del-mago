"""Music and effects for "Papá Noel en ojotas" (videos/AUDIT_MUSICA.md): Christmas in a Montevideo summer.
Candombe (the tambores of Montevideo: madera, chico, repique, piano) with "Jingle Bells" (public domain) on a marimba,
C major, 116 bpm. He arrives melted in flip-flops: the drums alone, slow to warm up. "¡Tengo una idea! ¡A imprimir!":
the full candombe with the tune; a cash register as the gifts come out; the TNT bursts into confetti. Shared by both
edits (hf3d and hf3d-v2). No effect on a word."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "biblioteca"))
from estilos import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
S = Song("hf3d", bpm=116, duck=0.3)
JB = [[(0, "E5", 1), (1, "E5", 1), (2, "E5", 2)], [(0, "E5", 1), (1, "E5", 1), (2, "E5", 2)], [(0, "E5", 1), (1, "G5", 1), (2, "C5", 1.5), (3.5, "D5", .5)], [(0, "E5", 4)],
      [(0, "F5", 1), (1, "F5", 1), (2, "F5", 1.5), (3.5, "F5", .5)], [(0, "F5", 1), (1, "E5", 1), (2, "E5", 1), (3, "E5", .5), (3.5, "E5", .5)], [(0, "E5", 1), (1, "D5", 1), (2, "D5", 1), (3, "E5", 1)], [(0, "D5", 2), (2, "G5", 2)]]
candombe(S, 0.0, 7.9, ["C", "G7"], g=1.0)                                   # melted: the drums and the bass only
candombe(S, 7.9, S.dur, ["C", "C", "C", "C", "F", "C", "G7", "C"], lead=loop(JB, 12))
final_chord(S, 17.9, ["C4", "E4", "G4"], inst=marimba, g=0.5)
S.old_sfx("cues3d.json", skip=("item_get", "victory", "boom", "sad", "surprise"))
S.fx("cash", 10.4, 0.55)                                                     # the gifts come out: ka-ching
S.fx("confetti", 12.2, 0.8, d=0.45)                                                 # the TNT bursts into confetti
S.gallery_swipes()                                                           # the real photos changing
S.write()
