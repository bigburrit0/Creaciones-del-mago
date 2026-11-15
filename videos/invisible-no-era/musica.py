"""Music and effects for "Invisible no era" (videos/AUDIT_MUSICA.md): a secret mission at 3 a.m.
Spy music (E minor, 104 bpm: a muted guitar ostinato, an upright bass, brushes, a whistled tune). They meet at the
printer: a record scratch and silence; "¿Vos también acá?" "Yo… pasaba."; an innocent whistle, crickets. The morning:
the spy theme, lighter; "¿Soy yo?" gets the smug glint. No effect on a word."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "biblioteca"))
from estilos import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
S = Song("hf3d", bpm=104, duck=0.3)
WH = [[(0, "B5", .5), (.5, "B5", .5), (1, "C6", 1), (2, "B5", .5), (2.5, "A5", .5), (3, "G5", 1)], [(0, "E5", 1), (1, "G5", .5), (1.5, "A5", .5), (2, "B5", 2)]]
spy(S, 0.0, 10.9, ["Em", "Em", "C", "B7"], lead=loop(WH, 4, 1))
S.stop(10.9, 17.0, 0.03)                                                     # caught: silence, the alibis, the crickets
spy(S, 17.0, S.dur, ["Em", "C", "Am", "B7"], lead=loop(WH, 5), g=0.85)
final_chord(S, 24.5, ["E3", "B3", "E4", "G4"], inst=vibes, g=0.5)
S.old_sfx("cues.json", skip=("tiptoe", "sting", "whistle", "item_get"))
S.fx("scratch", 10.93, 0.75)                                                 # the trending record scratch: they meet
S.fx("silbido", 14.72, 0.5)                                                  # both whistle, innocently
S.fx("crickets", 16.0, 0.5, d=1.0)
S.fx("rizz", 22.7, 0.65, d=0.6)                                              # "¿Soy yo?" ... smug
S.gallery_swipes()                                                           # the real photos changing
S.write()
