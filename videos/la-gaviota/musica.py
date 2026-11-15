"""Music and effects for "La gaviota" (videos/AUDIT_MUSICA.md): summer at the beach.
A bossa in D (nylon guitar, shaker, rim clicks) with a steel drum tune. When the gull grabs the king: a record scratch
and the music stops dead ("¡Mi rey!" in silence). El Mago's travel chess: the bossa comes back, lighter. The gull is
back: the music stops again for its three pecks (bonks on the closed tube); "¡Ja! ¡Ahora no podés!", then a sad
trombone as it gives up and leaves. Sunset: the bossa with the steel drum to the end. No effect on a word."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "biblioteca"))
from estilos import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
T = dict(s1=0.15, gull=2.95, grab=3.75, away=4.6, s2=4.7, magic=5.6, m1=5.8, swap=6.0, off=7.15, fold=8.0, len=9.35, into=10.75, cap=12.2, back=12.6, miffed=14.0, s3=14.15, leave=15.95, sunset=16.0, proof=17.7, cta=19.9, m2=20.0, card=23.45)
pecks = [13.2, 13.5, 13.8]
S = Song("hf3d", bpm=104, duck=0.28)
PROG = ["Dmaj7", "G7", "Em7", "A7"]
LEAD = [[(0, "F#5", 1), (1, "A5", .5), (1.5, "F#5", .5), (2, "E5", 1.5)], [(0, "D5", .5), (.5, "E5", .5), (1, "F5", 1), (2, "B4", 2)],
        [(0, "G5", 1), (1, "E5", .5), (1.5, "D5", .5), (2, "B4", 1.5)], [(0, "C#5", .5), (.5, "E5", .5), (1, "A5", 1), (2, "G5", 1)]]
bossa(S, 0.0, T["grab"] + 0.05, PROG, lead=loop(LEAD, 3))
S.stop(T["grab"] + 0.05, T["magic"], 0.02)                                   # the theft: a record scratch, then silence
bossa(S, T["magic"], T["back"], PROG, g=1.1)                                 # the travel chess, lighter (under El Mago's long line)
S.stop(T["back"] - 0.05, T["sunset"], 0.05)                                  # the gull is back: silence for the pecks and the taunt
bossa(S, T["sunset"], S.dur, PROG, lead=loop(LEAD, 4))                       # sunset: the bossa to the end
final_chord(S, T["card"] + 0.05, ["D4", "F#4", "A4", "C#5"], inst=steel)
S.old_sfx("cues.json", skip=("peck", ("chirp", T["leave"] + 0.1), ("chime", T["card"])))
S.fx("scratch", T["grab"] + 0.06, 0.8)                                       # the trending record scratch: the king is gone
for i, p in enumerate(pecks): S.fx("bonk", p + 0.08, 0.85, 1.25 + 0.08 * i)   # three bonks on the closed tube
S.fx("sadtrombone", T["leave"] + 0.05, 0.55)                                 # the gull gives up
S.fx("chime", T["card"] + 0.1, 0.5)
S.gallery_swipes()                                                           # the real photos changing
S.write()
