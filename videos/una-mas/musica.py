"""Music and effects for "Una más" (videos/AUDIT_MUSICA.md): one night of printing.
Day: a bouncy workshop tune (C major, 112 bpm). Dusk: it slows into a music box with a ticking clock. Night: the music box
alone while Papá Noel falls asleep standing (snores). Dawn: a ta-da with all 32 pieces, the bouncy tune again. A quick
ba-dum-tss after "¡una más!". No effect on a word."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "biblioteca"))
from estilos import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
T = dict(m1=0.1, firstPop=2.65, s1=5.05, m2=6.9, dusk0=7.4, s2=9.75, m3=10.7, night=11.3, doze=11.5, lastPop=13.9, dawn=13.75, s3=14.25, spare=15.3, m4=15.4, proof=18.15, cta=20.5, m5=20.6, card=24.5)
S = Song("hf3d", bpm=112, duck=0.28)
TUNE = [[(0, "E5", .5), (.5, "G5", .5), (1, "C6", 1), (2, "G5", .5), (2.5, "E5", .5), (3, "D5", 1)], [(0, "F5", .5), (.5, "A5", .5), (1, "C6", 1), (2, "B5", 1), (3, "G5", 1)]]
bouncy(S, 0.0, T["dusk0"], ["C", "F", "G", "C"], lead=loop(TUNE, 4))
lullaby(S, T["dusk0"], T["night"], ["Am", "F"], clock=True)
lullaby(S, T["night"], T["dawn"], ["F", "C"], clock=True, g=0.8)
bouncy(S, T["dawn"] + 0.2, S.dur, ["C", "F", "G", "C"], lead=loop(TUNE, 8))
final_chord(S, T["card"] + 0.05, ["C4", "E4", "G4", "C5"], inst=marimba)
S.old_sfx("cues.json", skip=("lur", ("ding", 13.9), ("chime", 13.95), "surprise", ("chime", T["card"])))
S.fx("tada", T["dawn"] - 0.25, 0.6)                                          # dawn: all 32 pieces
S.fx("rimshot", 18.09, 0.55, fast=True)                                      # "¡una más!" ba-dum-tss
S.fx("chime", T["card"] + 0.1, 0.5)
S.gallery_swipes()                                                           # the real photos changing
S.write()
