"""estilos.py: musical styles for the reels' new scores (videos/AUDIT_MUSICA.md), on top of banda.py.

Each style fills a stretch of a Song with a genre that fits a story: an epic battle, a TV quiz, a tango, a bossa on the
beach, candombe, a lullaby with a ticking clock, a bouncy showcase, a Greek lyre, a Christmas carol, a spy mission, a
ukulele. A style takes the stretch (t0, t1), the chords one per bar ("Dm", "A7", "Bb", "F#dim"...) and options; the
melody, when there is one, is built from the chord tones with the style's own rhythm, or given note by note.
Times are seconds on the reel's timeline; one bar is 4 beats of the Song's bpm.
"""
import re
from banda import *

QUAL = {"": (0, 4, 7), "m": (0, 3, 7), "7": (0, 4, 7, 10), "m7": (0, 3, 7, 10), "maj7": (0, 4, 7, 11), "dim": (0, 3, 6), "6": (0, 4, 7, 9), "sus": (0, 5, 7)}
def chord(name, octave=3):
    m = re.match(r"([A-G][#b]?)(.*)", name); root = mid(m.group(1) + str(octave)); return [root + x for x in QUAL[m.group(2)]]
def bars(S, t0, t1, prog):
    """yields (bar_start, chord_name, bar_index) over the stretch"""
    B = 4 * S.b(); k, t = 0, t0
    while t < t1 - 0.05: yield t, prog[k % len(prog)], k; k += 1; t += B
def inside(t, t1): return t < t1 - 0.02
def melody(S, track, inst, notes, t0, t1, g=1.0, **kw):
    """notes: [(beat, 'A4' or midi, beats), ...] from t0; anything that starts after t1 is dropped"""
    b = S.b()
    for off, nm, ln in notes:
        at = t0 + off * b
        if nm is not None and inside(at, t1): S.put(track, inst(f(nm) if isinstance(nm, str) else hz(nm), max(0.05, ln * b), **kw), at, g)

def epic(S, t0, t1, prog, horn=True, drums=True, g=1.0):
    """a battle (in fun): timpani on 1 and 3, low strings in eighths, horn calls every other bar, a snare march"""
    b = S.b(); st, hn, dr = S.tr("ep_str", 0.5 * g, 0.25, 1.6), S.tr("ep_horn", 0.45 * g, 0.3, 1.6), S.tr("ep_drum", 0.7 * g, 0.2, 1.4)
    for bt, ch, k in bars(S, t0, t1, prog):
        c = chord(ch, 2)
        for q in range(8):
            at = bt + q * b / 2
            if inside(at, t1): S.put(st, strings(hz(c[0] if q % 4 != 3 else c[0] + 7), b / 2 * 0.9, 0.01), at, 0.9)
        if drums:
            for q in (0, 2):
                if inside(bt + q * b, t1): S.put(dr, timpani(hz(c[0] - 12 if q == 0 else c[0] - 5), 0.9, 1.0), bt + q * b)
            for q in range(4):
                if inside(bt + q * b + b / 2, t1): S.put(dr, snare(0.35), bt + q * b + b / 2)
        if horn and k % 2 == 0:
            c3 = chord(ch, 3); call = [(0, c3[0], 1.5), (1.5, c3[1], .5), (2, c3[2], 2)]
            melody(S, hn, brass, call, bt, t1, 0.8)

def quiz(S, t0, t1, prog, lead=None, g=1.0):
    """a TV quiz: a walking bass, swung brushes, vibraphone chords on 2 and 4, an optional vibraphone melody"""
    b = S.b(); bs, dr, vb = S.tr("qz_bass", 0.9 * g, 0.12), S.tr("qz_drum", 0.5 * g, 0.12), S.tr("qz_vibes", 0.4 * g, 0.3)
    for bt, ch, k in bars(S, t0, t1, prog):
        c = chord(ch, 2); walk = [c[0], c[1] if len(c) > 1 else c[0] + 4, c[2], c[0] + 11 if k % 2 else c[2] + 2]
        for q in range(4):
            if inside(bt + q * b, t1): S.put(bs, upright(hz(walk[q]), b * 0.9), bt + q * b, 0.9)
            if inside(bt + q * b, t1): S.put(dr, brush(0.5 if q % 2 else 0.3), bt + q * b)
            if inside(bt + q * b + 2 * b / 3, t1): S.put(dr, hat(0.3), bt + q * b + 2 * b / 3)
        for q in (1, 3):
            if inside(bt + q * b, t1):
                for m in chord(ch, 4)[:3]: S.put(vb, vibes(hz(m), b * 0.8), bt + q * b, 0.35)
    if lead: melody(S, vb, vibes, lead, t0, t1, 0.9)

def tango(S, t0, t1, prog, lead=None, g=1.0):
    """a tango: the bandoneón marking four beats (accents on 1 and 3), a pizzicato bass with a drag into beat 1, string stabs"""
    b = S.b(); bd, bs, st = S.tr("tg_band", 0.5 * g, 0.18, 1.3), S.tr("tg_bass", 1.0 * g, 0.12), S.tr("tg_str", 0.45 * g, 0.22, 1.4)
    for bt, ch, k in bars(S, t0, t1, prog):
        c = chord(ch, 3)
        for q in range(4):
            if inside(bt + q * b, t1):
                for m in c[:3]: S.put(bd, reed(hz(m), b * (0.55 if q % 2 else 0.4)), bt + q * b, 0.55 if q % 2 == 0 else 0.35)
        for q, m in ((0, c[0] - 12), (2, c[0] - 5)):
            if inside(bt + q * b, t1): S.put(bs, pizz(hz(m), 0.5), bt + q * b, 1.0)
        for j, m in enumerate((c[0] - 14, c[0] - 13)):                       # the arrastre: a drag into the next bar
            at = bt + 3.5 * b + j * b / 4
            if inside(at, t1): S.put(bs, pizz(hz(m), 0.2), at, 0.6)
        if k % 2 == 1 and inside(bt + 3 * b, t1):
            for m in chord(ch, 4)[:3]: S.put(st, strings(hz(m), b * 0.5, 0.01) * 2, bt + 3 * b, 0.7)
    if lead: melody(S, bd, reed, lead, t0, t1, 0.9)

def bossa(S, t0, t1, prog, lead=None, g=1.0):
    """a bossa on the beach: nylon guitar (thumb on 1 and 3, syncopated chords), shaker, rim clicks, steel drum on top"""
    b = S.b(); gt, pc, ld = S.tr("bs_gtr", 0.7 * g, 0.18), S.tr("bs_perc", 0.45 * g, 0.1), S.tr("bs_lead", 0.45 * g, 0.25)
    rim_at = (0, 1.5, 3, 4.5, 6)                                           # a two-bar clave, in eighths
    for bt, ch, k in bars(S, t0, t1, prog):
        c = chord(ch, 3)
        for q in (0, 2):
            if inside(bt + q * b, t1): S.put(gt, guitar(hz(c[0] - 12 if q == 0 else c[0] - 5), b * 1.6), bt + q * b, 0.8)
        for e in (0, 1.5, 2.5, 3.5):
            if inside(bt + e * b, t1):
                for m in c[1:] + [c[0] + 12]: S.put(gt, guitar(hz(m), b * 0.7), bt + e * b + rng.uniform(0, 0.012), 0.35)
        for q in range(8):
            if inside(bt + q * b / 2, t1): S.put(pc, shaker(0.6 if q % 2 else 0.35), bt + q * b / 2)
        for e in rim_at:
            at = bt + (e - (4 if k % 2 else 0)) * b
            if bt <= at < bt + 4 * b and inside(at, t1) and (e >= 4) == (k % 2 == 1): S.put(pc, rim(0.5), at)
    if lead: melody(S, ld, steel, lead, t0, t1, 0.9)

def candombe(S, t0, t1, prog, lead=None, lead_inst=None, g=1.0):
    """candombe (Montevideo): the madera pattern, the chico on the off sixteenths, the repique's calls, the piano's
    accents, a bass on the root; an optional melody (marimba by default)"""
    b = S.b(); dr, bs, ld = S.tr("cd_drum", 0.6 * g, 0.12, 0.9), S.tr("cd_bass", 0.8 * g, 0.1), S.tr("cd_lead", 0.5 * g, 0.22)
    madera = (0, 0.75, 1.5, 2.5, 3)                                        # beats (a 3-2 clave feel)
    for bt, ch, k in bars(S, t0, t1, prog):
        c = chord(ch, 2)
        for e in madera:
            if inside(bt + e * b, t1): S.put(dr, candombe_drum("madera"), bt + e * b, 0.8)
        for q in range(4):
            for s16 in (1, 2, 3):                                         # chico: three off sixteenths per beat
                at = bt + q * b + s16 * b / 4
                if inside(at, t1): S.put(dr, candombe_drum("chico"), at, 0.45 if s16 != 3 else 0.6)
            if inside(bt + q * b, t1) and q in (1, 3): S.put(dr, candombe_drum("piano"), bt + q * b + b / 2, 0.8)
            if inside(bt + q * b, t1) and q == 0: S.put(dr, candombe_drum("piano"), bt, 0.6)
        if k % 2 == 1:
            for j in range(3):
                at = bt + 3 * b + j * b / 3
                if inside(at, t1): S.put(dr, candombe_drum("repique"), at, 0.7)
        for q, m in ((0, c[0]), (1.5, c[0] + 7), (2, c[0]), (3.5, c[0] + 7)):
            if inside(bt + q * b, t1): S.put(bs, ebass(hz(m), b * 0.45), bt + q * b, 0.8)
    if lead: melody(S, ld, lead_inst or marimba, lead, t0, t1, 0.9)

def lullaby(S, t0, t1, prog, clock=True, g=1.0):
    """a music box at night, a soft celesta, a ticking clock"""
    b = S.b(); mb, ck, pd = S.tr("lb_box", 0.5 * g, 0.35, 1.8), S.tr("lb_clock", 0.35 * g, 0.05), S.tr("lb_pad", 0.25 * g, 0.3, 2.0)
    for bt, ch, k in bars(S, t0, t1, prog):
        c = chord(ch, 5); pat = [c[0], c[1], c[2], c[1], c[0] + 12, c[2], c[1], c[2]]
        for q, m in enumerate(pat):
            at = bt + q * b / 2
            if inside(at, t1): S.put(mb, musicbox(hz(m), b * 1.2), at, 0.6)
        if inside(bt, t1):
            for m in chord(ch, 3): S.put(pd, strings(hz(m), 4 * b, 0.6), bt, 0.5)
        if clock:
            for q in range(4):
                if inside(bt + q * b, t1): S.put(ck, wood(2400 if q % 2 else 1900, 0.5), bt + q * b)

def bouncy(S, t0, t1, prog, lead=None, g=1.0):
    """a bouncy showcase: pizzicato bass, marimba chords, claps on 2 and 4, a light kick"""
    b = S.b(); bs, mr, dr = S.tr("bn_bass", 0.9 * g, 0.12), S.tr("bn_mar", 0.5 * g, 0.2), S.tr("bn_drum", 0.5 * g, 0.12)
    for bt, ch, k in bars(S, t0, t1, prog):
        c = chord(ch, 2)
        for q, m in ((0, c[0]), (1, c[2]), (2, c[0] + 12), (3, c[2])):
            if inside(bt + q * b, t1): S.put(bs, pizz(hz(m), b * 0.8), bt + q * b, 0.9)
        for e in (0.5, 1.5, 2.5, 3.5):
            if inside(bt + e * b, t1):
                for m in chord(ch, 4)[:3]: S.put(mr, marimba(hz(m), b * 0.6), bt + e * b, 0.3)
        for q in range(4):
            if inside(bt + q * b, t1): S.put(dr, kick(0.5) if q % 2 == 0 else clap(0.6), bt + q * b)
    if lead: melody(S, mr, xylo, lead, t0, t1, 0.9)

def greek(S, t0, t1, prog, lead=None, g=1.0):
    """ancient Greece: lyre arpeggios, a frame drum, a flute melody, timpani on the bar"""
    b = S.b(); ly, dr, fl = S.tr("gk_lyre", 0.6 * g, 0.3, 1.8), S.tr("gk_drum", 0.6 * g, 0.2, 1.4), S.tr("gk_flute", 0.4 * g, 0.35, 1.8)
    for bt, ch, k in bars(S, t0, t1, prog):
        c = chord(ch, 3); arp = [c[0], c[1], c[2], c[0] + 12, c[2], c[1]]
        for q, m in enumerate(arp):
            at = bt + q * (4 * b / 6)
            if inside(at, t1): S.put(ly, harp(hz(m), 1.4), at, 0.6)
        for e, gg in ((0, 1.0), (1.5, 0.5), (2, 0.8), (3, 0.5), (3.5, 0.4)):
            if inside(bt + e * b, t1): S.put(dr, tom(f("D2") if e in (0, 2) else f("A2"), gg, 0.35), bt + e * b)
    if lead: melody(S, fl, flute, lead, t0, t1, 0.9)

def xmas(S, t0, t1, prog, lead=None, lead_inst=None, g=1.0):
    """Christmas: sleigh bells, a pizzicato bass, celesta chords; an optional carol melody (celesta by default)"""
    b = S.b(); sb, bs, cl = S.tr("xm_bells", 0.45 * g, 0.15), S.tr("xm_bass", 0.8 * g, 0.12), S.tr("xm_cel", 0.45 * g, 0.3, 1.6)
    for bt, ch, k in bars(S, t0, t1, prog):
        c = chord(ch, 2)
        for q in range(8):
            if inside(bt + q * b / 2, t1): S.put(sb, sleigh(0.9 if q % 2 == 0 else 0.5), bt + q * b / 2)
        for q, m in ((0, c[0]), (1, c[2]), (2, c[0]), (3, c[2])):
            if inside(bt + q * b, t1): S.put(bs, pizz(hz(m), b * 0.8), bt + q * b, 0.8)
        for q in (1, 3):
            if inside(bt + q * b, t1):
                for m in chord(ch, 4)[:3]: S.put(cl, celesta(hz(m), b), bt + q * b, 0.25)
    if lead: melody(S, cl, lead_inst or celesta, lead, t0, t1, 1.0)

def spy(S, t0, t1, prog, lead=None, g=1.0):
    """a secret mission at night: a muted guitar ostinato, an upright bass, brushes and a whistled tune"""
    b = S.b(); gt, bs, dr, wh = S.tr("sp_gtr", 0.6 * g, 0.15), S.tr("sp_bass", 0.9 * g, 0.1), S.tr("sp_drum", 0.45 * g, 0.12), S.tr("sp_wh", 0.4 * g, 0.35, 1.6)
    for bt, ch, k in bars(S, t0, t1, prog):
        c = chord(ch, 2); ost = [c[0] + 12, c[0] + 12, c[0] + 13, c[0] + 13, c[0] + 14, c[0] + 14, c[0] + 13, c[0] + 13]
        for q, m in enumerate(ost):
            if inside(bt + q * b / 2, t1): S.put(gt, muted(hz(m), 0.2), bt + q * b / 2, 0.7)
        for q, m in ((0, c[0]), (2, c[0] + 7)):
            if inside(bt + q * b, t1): S.put(bs, upright(hz(m), b * 1.5), bt + q * b, 0.9)
        for q in range(4):
            if inside(bt + q * b, t1): S.put(dr, brush(0.5 if q % 2 else 0.3), bt + q * b)
    if lead: melody(S, wh, whistle, lead, t0, t1, 0.9)

def ukulele_pop(S, t0, t1, prog, lead=None, g=1.0):
    """bright and crafty: a strummed ukulele, claps, a glockenspiel melody"""
    b = S.b(); uk, dr, gl = S.tr("uk_uke", 0.55 * g, 0.15), S.tr("uk_drum", 0.45 * g, 0.1), S.tr("uk_glock", 0.35 * g, 0.3)
    strum = (0, 1, 1.5, 2.5, 3, 3.5)
    for bt, ch, k in bars(S, t0, t1, prog):
        c = chord(ch, 4)
        for e in strum:
            if inside(bt + e * b, t1):
                for j, m in enumerate(c[:3] + [c[0] + 12]): S.put(uk, ukulele(hz(m), b * 0.6), bt + e * b + j * 0.012, 0.35)
        for q in range(4):
            if inside(bt + q * b, t1): S.put(dr, kick(0.45) if q in (0, 2) else clap(0.5), bt + q * b)
    if lead: melody(S, gl, glock, lead, t0, t1, 0.9)


def loop(motifs, nbars, start_bar=0):
    """a melody of bar motifs repeated over nbars: motifs = [[(beat, note, beats), ...], ...] -> one note list with offsets"""
    out = []
    for k in range(nbars):
        for off, nm, ln in motifs[(start_bar + k) % len(motifs)]: out.append((4 * k + off, nm, ln))
    return out
def final_chord(S, t, names, track="end", inst=None, g=0.8, d=2.4):
    tr = S.tr(track, 0.6, 0.3, 1.8)
    for nm in names: S.put(tr, (inst or celesta)(f(nm), d), t, g)
