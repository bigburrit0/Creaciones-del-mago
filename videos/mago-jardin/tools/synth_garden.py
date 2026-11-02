import sys, wave, numpy as np
OUT = sys.argv[1]; SR = 44100
rng = np.random.default_rng(3)
def t(d): return np.arange(int(d*SR))/SR
def sq(f, d, duty=0.5):
    n = int(d*SR)
    ph = np.cumsum(np.broadcast_to(np.asarray(f, float), n)/SR) if np.ndim(f) else t(d)*f
    return np.where((ph % 1) < duty, 1.0, -1.0)
def tri(f, d):
    ph = (t(d)*f) % 1; return 4*np.abs(ph-0.5)-1
def env(n, a=0.005, r=0.1):
    e = np.ones(n); A = max(1, int(a*SR)); e[:A] = np.linspace(0, 1, A)
    R = min(int(r*SR), n); e[n-R:] *= np.linspace(1, 0, R); return e
def crush(x, bits=5): q = 2**bits; return np.round(x*q)/q
def lp(x, a):
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x): acc += a*(v-acc); y[i] = acc
    return y
def put(buf, x, at):
    i = int(at*SR); n = min(len(x), len(buf)-i)
    if n > 0: buf[i:i+n] += x[:n]
def write(name, x, peak=0.85):
    x = x/max(1e-9, np.abs(x).max())*peak
    w = wave.open(f'{OUT}/{name}.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x*32767).astype('<i2').tobytes()); w.close()
D = 10.0
N = lambda: np.zeros(int(D*SR))
note = lambda s: 440*2**((s-9)/12)   # s: semitones from C4... (C4 = -9 -> 261.6)

# ---- sfx track (absolute times, 10 s)
fx = N()
# trowel tap
for k, at in enumerate([0.12, 0.2]):
    n = rng.uniform(-1, 1, int(0.03*SR)) * np.exp(-t(0.03)*120)
    put(fx, n*0.5 + sq(1800-300*k, 0.03, 0.5)*np.exp(-t(0.03)*160)*0.4, at)
# seed sparkle
for k in range(5):
    put(fx, crush(sq(2093*2**(k/12*2), 0.05, 0.25)*np.exp(-t(0.05)*50))*0.18, 0.32 + k*0.05)
# three rising pops (plant stages)
for k, at in enumerate([0.8, 1.2, 1.6]):
    f = np.geomspace(300*1.35**k, 900*1.35**k, int(0.09*SR))
    put(fx, crush(sq(f, 0.09, 0.5)*env(int(0.09*SR), 0.002, 0.04))*0.55, at)
    for j in range(3): put(fx, sq(1568*1.26**k*2**(j*4/12), 0.04, 0.25)*np.exp(-t(0.04)*60)*0.12, at+0.09+j*0.035)
# harvest chime (feeder appears)
for j, s in enumerate([0, 4, 7, 12, 16]):
    x = sq(note(12+s), 0.5, 0.25)*np.exp(-t(0.5)*5) * 0.3 + tri(note(24+s), 0.5)*np.exp(-t(0.5)*4)*0.25
    put(fx, crush(x, 6), 2.48 + j*0.06)
# 8-bit wing flaps
def flaps(start, end, rate):
    tt = start
    while tt < end:
        n = rng.uniform(-1, 1, int(0.05*SR)); x = lp(n, 0.35)*np.exp(-t(0.05)*45)
        put(fx, crush(x, 4)*0.45, tt); tt += rate
flaps(3.0, 4.0, 0.18); flaps(4.0, 5.2, 0.28); flaps(3.6, 4.8, 0.18); flaps(5.0, 5.6, 0.18); flaps(5.6, 6.4, 0.2)
# leaf burst as the canopy pops
n = rng.uniform(-1, 1, int(0.22*SR)); put(fx, crush(n - lp(n, 0.3), 4)*np.exp(-t(0.22)*14)*0.35, 2.4)
# soft footsteps: wizard hops back, then walks to the chair
def step(at, f=180, g=0.3):
    put(fx, crush(sq(np.linspace(f, f*0.6, int(0.035*SR)), 0.035, 0.5)*np.exp(-t(0.035)*90))*g, at)
for k in range(3): step(0.46 + 0.14*k + 0.047, 200)
for k in range(5): step(5.52 + 0.11*k + 0.055, 170 + 15*(k % 2), 0.22)
for k in range(5): step(6.07 + 0.13*k + 0.065, 170 + 15*(k % 2), 0.22)
# landing taps on the feeder
for at in (5.32, 5.66): put(fx, sq(1300, 0.025, 0.5)*np.exp(-t(0.025)*150)*0.25, at)
# chiptune kiskadee call  ("bien-te-veo": short, short, long falling)
def kiskadee(at, base=1500):
    for d, f0, f1, gap in [(0.09, base*1.3, base*1.45, 0.0), (0.08, base*1.1, base*1.2, 0.13), (0.28, base*1.5, base*0.95, 0.26)]:
        f = np.linspace(f0, f1, int(d*SR)); x = sq(f, d, 0.25)*env(int(d*SR), 0.004, 0.05)
        put(fx, crush(x)*0.32, at + gap)
kiskadee(4.15); kiskadee(8.55, 1400)
# chair unfold: creak + clack, poof
put(fx, crush(sq(np.linspace(220, 140, int(0.18*SR)), 0.18, 0.125)*env(int(0.18*SR), 0.01, 0.05))*0.25, 6.7)
for at in (6.86, 6.93):
    put(fx, (rng.uniform(-1, 1, int(0.04*SR))*np.exp(-t(0.04)*90)*0.6 + sq(700, 0.04, 0.5)*np.exp(-t(0.04)*80)*0.4), at)
n = rng.uniform(-1, 1, int(0.25*SR)); put(fx, crush(lp(n, 0.15))*np.exp(-t(0.25)*12)*0.4, 6.74)
# dissolve shimmer
for k in range(8): put(fx, sq(1046*2**(k/8), 0.06, 0.25)*np.exp(-t(0.06)*40)*0.1, 7.4 + k*0.075)
# pecking ticks
def ticks(start, end, step, pitch):
    tt = start; k = 0
    while tt < end:
        put(fx, sq(pitch*(1.0 + 0.1*(k % 2)), 0.018, 0.5)*np.exp(-t(0.018)*220)*0.35, tt); tt += step; k += 1
ticks(6.55, 7.4, 0.3, 2600); ticks(6.7, 7.4, 0.3, 2900); ticks(8.0, 9.2, 0.3, 2600); ticks(8.15, 9.2, 0.3, 2900)
# sip (tiny gurgle)
for k in range(3): put(fx, crush(sq(np.linspace(500, 380, int(0.05*SR)), 0.05, 0.5)*np.exp(-t(0.05)*40))*0.12, 8.35 + k*0.07)
write('g_sfx', fx, 0.9)

# ---- light happy chiptune melody (C major, 132 bpm) ending calmly
bpm = 132; b = 60/bpm
mel = [(7,1),(12,1),(11,.5),(12,.5),(14,1),(12,1),(9,1),(7,2),
       (5,1),(9,1),(12,1),(11,.5),(9,.5),(7,2),(4,1),(5,1),
       (7,1),(12,1),(14,.5),(16,.5),(14,1),(12,2),(7,1),(9,1)]
m = N(); pos = 0.25
for s, d in mel:
    if pos > 9.0: break
    dur = d*b
    x = sq(note(12+s), dur*0.9, 0.25)*env(int(dur*0.9*SR), 0.004, dur*0.35)
    put(m, x*0.22, pos); pos += dur
# bass + chords (triangle) per bar
prog = [0, 5, 9, 7, 0, 5, 7, 0]   # C F Am G C F G C (roots, semitones)
bar = 4*b
for k, r in enumerate(prog):
    at = 0.25 + k*bar
    if at > 9.3: break
    for q in range(4):
        x = tri(note(-12+r if r < 7 else -24+r), b*0.8)*env(int(b*0.8*SR), 0.004, 0.08)
        put(m, x*0.3, at + q*b)
# final calm chord
for s in (0, 4, 7, 12):
    x = sq(note(s), 1.4, 0.25)*np.exp(-t(1.4)*2.2)*env(int(1.4*SR), 0.01, 0.6)
    put(m, x*0.12, 8.55)
m[int(9.6*SR):] *= np.linspace(1, 0, len(m)-int(9.6*SR))
write('g_music', m, 0.8)

# ---- birdsong ambience (soft chiptune chirps)
bs = N()
times = [0.5, 1.4, 2.2, 3.1, 3.4, 4.6, 5.3, 6.1, 7.0, 7.7, 8.1, 8.9, 9.5]
for k, at in enumerate(times):
    base = 2600 + (k*397 % 900)
    for j in range(2 + k % 3):
        d = 0.05; f = np.linspace(base, base*1.25 if j % 2 == 0 else base*0.85, int(d*SR))
        put(bs, lp(sq(f, d, 0.5), 0.25)*env(int(d*SR), 0.005, 0.02)*0.5, at + j*0.07)
write('g_birds', bs, 0.5)
