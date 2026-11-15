"""Music and effects for "Los gatos tiran todo" (videos/AUDIT_MUSICA.md): a cat's mischief.

Sneaky pizzicato and a tiptoeing clarinet in D minor (100 bpm), brushes. The dog pawn's eager hop gets a boing. While
the cat queen taps the pawn three times the music stops dead: only the taps. The pawn goes over the edge and lands
like a metal pipe (clang, bounce). After "Para un gato, sí." a deep boom, and the theme comes back smug, with a glockenspiel
on top. It ends on a D major chord under the card. No effect starts on a word (checked).
Run: python3 musica.py  (writes hf3d/assets/audio/music.wav and sfx.wav; then remezclar.py)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "biblioteca"))
from banda import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))
T = dict(s1=0.15, m1=2.5, hop=4.35, leap=6.05, step=6.75, look=7.1, land=9.42, s2=9.75, m2=11.85, smug=13.15, proof=14.8, cta=17.0, m3=17.1, card=20.55)
taps = [7.75, 8.35, 8.95]
S = Song("hf3d", bpm=100, duck=0.28); b = S.b()
bass, clar, glk, drum, xyl = S.tr("bass", 1.0, 0.12), S.tr("clar", 0.55, 0.2), S.tr("glock", 0.35, 0.3), S.tr("drums", 0.5, 0.1), S.tr("xylo", 0.45, 0.2)

BAR = 4 * b
CH = [("D2", "A2", "D3", "A2"), ("D2", "A2", "F2", "E2"), ("Bb1", "F2", "Bb2", "F2"), ("A1", "E2", "A2", "C#3")]
MOTIF = [[(0, "A4", .25), (.5, "Bb4", .25), (1, "A4", .25), (1.5, "F4", .25), (2, "D4", .5)],
         [(0, "E4", .25), (.5, "F4", .25), (1, "G#4", .25), (1.5, "A4", .75)],
         [(0, "D5", .25), (.5, "C5", .25), (1, "Bb4", .25), (1.5, "A4", .25), (2, "G4", .5)],
         [(0, "E4", .25), (.5, "G4", .25), (1, "C#5", .25), (1.5, "E5", .25), (2.5, "A4", .5)]]

def theme(t0, t1, melody=True, bells=False, brushes=True, sparse=False):
    k, t = 0, t0
    while t < t1 - 0.05:
        ch = CH[k % 4]
        for q, nm in enumerate(ch):
            if t + q * b < t1 and not (sparse and q % 2): S.put(bass, upright(f(nm), 0.4), t + q * b, 0.9)
        if melody: seq(S, clar, clarinet, [n for n in MOTIF[k % 4] if t + n[0] * b < t1], t, b, 0.8)
        if bells: seq(S, glk, glock, [n for n in MOTIF[k % 4] if t + n[0] * b < t1][::2], t, b, 0.7)
        if brushes:
            for q in range(4):
                if t + q * b < t1: S.put(drum, brush(0.6 if q % 2 else 0.35), t + q * b, 1)
            for q in range(8):
                if t + q * b / 2 < t1 and q % 2: S.put(drum, hat(0.25), t + q * b / 2, 1)
        k += 1; t += BAR

theme(0.0, 6.0)                                     # the living room: dogs and cats choose sides
for k, nm in enumerate(["D3", "F3", "A3", "D4"]):   # the eager dog pawn: a happy xylophone run into the hop
    S.put(xyl, xylo(f(nm), 0.3), T["hop"] - 0.36 + k * 0.09, 0.8)
theme(6.0, 7.6, melody=False, brushes=False, sparse=True)       # the cat queen creeps in: only the bass, half the notes
seq(S, clar, clarinet, [(0, "D4", .5), (1, "Eb4", .5), (2, "E4", .5)], 6.15, b, 0.7)   # a chromatic creep
S.stop(7.6, 13.0, 0.04)                             # silence for the three taps, the fall, the argument
theme(13.0, T["card"], bells=True)                  # smug cats: the theme back, with a glockenspiel
for nm in ("D2", "A2"): S.put(bass, upright(f(nm), 2.2), T["card"] + 0.05, 0.8)        # the card: a D major chord (a happy ending for the cats)
for nm in ("D4", "F#4", "A4"): S.put(glk, celesta(f(nm), 2.2), T["card"] + 0.05, 0.9)
S.put(glk, glock(f("D5"), 1.5), T["card"] + 0.3, 0.8)

# effects: the eager hop, the leap, the taps, the fall like a metal pipe, the smug boom, the proof, the card
S.fx("boing", T["hop"], 0.75, 1.2)
S.fx("whoosh", T["leap"], 0.35, 1.2); S.fx("toc", T["leap"] + 0.55, 0.4, 1.1); S.fx("toc", T["step"] + 0.3, 0.3, 1.25)
for i, tt in enumerate(taps): S.fx("tap", tt + 0.14, 0.55, 1.15 - 0.06 * i)
S.fx("clang", T["land"] - 0.02, 0.95, 1.0, bounces=2, ring=1.8)        # the trending "metal pipe" fall
S.fx("boom", T["m2"] + 0.82, 0.9)                                      # "Para un gato, sí." ... boom
S.fx("whoosh", T["hop"] - 0.29, 0.25); S.fx("whoosh", T["cta"] - 0.09, 0.3)
S.fx("toc", T["proof"] + 0.37, 0.5, 0.8)
S.fx("chime", T["card"] + 0.15, 0.5)
S.write()
