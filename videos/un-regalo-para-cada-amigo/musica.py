"""Music and effects for "Un regalo para cada amigo" (videos/AUDIT_MUSICA.md): a gift for each friend.
A bouncy showcase (C major, 120 bpm: pizzicato bass, marimba, claps, a xylophone tune), a pop for each gift. After the
cactus line an "uh-oh"; after "¡me muero!" a slide whistle down; the banana in sunglasses ("¿Quién? ¿Yo?") gets the smug
glint. No effect on a word."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "biblioteca"))
from estilos import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
S = Song("hf3d", bpm=120, duck=0.3)
XY = [[(0, "E5", .5), (.5, "G5", .5), (1, "C6", .5), (1.5, "G5", .5), (2, "A5", 1), (3, "G5", 1)], [(0, "F5", .5), (.5, "E5", .5), (1, "D5", .5), (1.5, "E5", .5), (2, "C5", 2)],
      [(0, "E5", .5), (.5, "G5", .5), (1, "C6", .5), (1.5, "E6", .5), (2, "D6", 1), (3, "B5", 1)], [(0, "G5", .5), (.5, "A5", .5), (1, "G5", .5), (1.5, "E5", .5), (2, "D5", 2)]]
bouncy(S, 0.0, S.dur, ["C", "F", "C", "G"], lead=loop(XY, 13))
final_chord(S, 22.8, ["C4", "E4", "G4", "C5"], inst=marimba)
S.old_sfx("cues.json", skip=(("chime", 22.75),))
S.fx("uhoh", 7.63, 0.5)                                                      # the cactus ... uh-oh
S.fx("slide_down", 13.6, 0.55, d=0.4)                                        # "¡me muero!" ... the faint
S.fx("rizz", 16.68, 0.7, d=0.8)                                              # the banana: "¿Quién? ¿Yo?" ... smug
S.fx("chime", 22.85, 0.5)
S.gallery_swipes()                                                           # the real photos changing
S.write()
