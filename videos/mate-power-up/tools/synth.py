import sys, wave, numpy as np
OUT = sys.argv[1]; SR = 44100
rng = np.random.default_rng(7)
def t(d): return np.arange(int(d*SR))/SR
def sq(f, d, duty=0.5):
    ph = np.cumsum(np.broadcast_to(f, int(d*SR))/SR) if np.ndim(f) else t(d)*f
    return np.where((ph % 1) < duty, 1.0, -1.0)
def env(n, a=0.005, r=0.1, sus=None):
    e = np.ones(n); A = int(a*SR); e[:A] = np.linspace(0, 1, A)
    R = min(int(r*SR), n); e[-R:] *= np.linspace(1, 0, R); return e
def crush(x, bits=5): q = 2**bits; return np.round(x*q)/q
def lp(x, a): 
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x): acc += a*(v-acc); y[i] = acc
    return y
def put(buf, x, at): i = int(at*SR); buf[i:i+len(x)] += x[:len(buf)-i]
def write(name, x, peak=0.85):
    x = x/ max(1e-9, np.abs(x).max())*peak
    w = wave.open(f'{OUT}/{name}.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x*32767).astype('<i2').tobytes()); w.close()

# 1. crack + 16-bit hit (file starts at the snap)
b = np.zeros(int(1.2*SR))
n = rng.uniform(-1, 1, int(0.06*SR)); crack = (n - lp(n, 0.25)) * np.exp(-t(0.06)*70)
put(b, crack*1.0, 0)
f = np.geomspace(420, 55, int(0.28*SR)); hit = sq(f, 0.28, 0.5)*np.exp(-t(0.28)*9)
nz = rng.uniform(-1, 1, int(0.12*SR))*np.exp(-t(0.12)*30)
put(b, crush(hit*0.8), 0.01); put(b, crush(lp(nz, 0.4))*0.6, 0.01)
# small clatter when the pieces land (~0.65 s later)
for k, at in enumerate([0.62, 0.70]):
    c = sq(np.geomspace(300-60*k, 120, int(0.07*SR)), 0.07, 0.25)*np.exp(-t(0.07)*40)
    put(b, crush(c)*0.35, at)
write('hit', b)

# 2. three low tense beeps (one per second)
b = np.zeros(int(2.6*SR))
for k in range(3):
    beep = sq(110, 0.32, 0.5)*0.6 + sq(110*1.5, 0.32, 0.25)*0.15
    put(b, crush(beep*env(len(beep), 0.004, 0.05)), k*1.0)
write('countdown', b, 0.7)

# 3. rising chiptune arpeggio (1.4 s) + snap-fit click at its end
notes = [0, 4, 7, 12, 4, 7, 12, 16, 7, 12, 16, 19, 12, 16, 19, 24, 19, 24, 28, 31]
b = np.zeros(int(1.75*SR)); step = 1.4/len(notes)
for k, s in enumerate(notes):
    f0 = 523.25*2**(s/12)
    x = sq(f0, step, 0.125 if k % 2 else 0.25)*env(int(step*SR), 0.002, step*0.4)
    put(b, x*0.45, k*step)
clk = rng.uniform(-1, 1, int(0.02*SR))*np.exp(-t(0.02)*300) + sq(2400, 0.02, 0.5)*np.exp(-t(0.02)*250)*0.6
put(b, clk*1.2, 1.45)
put(b, crush(sq(np.geomspace(1500, 3000, int(0.08*SR)), 0.08, 0.5)*np.exp(-t(0.08)*30))*0.35, 1.47)
write('powerup', b)

# 4. victory chord
b = np.zeros(int(1.4*SR)); d = 1.2
for k, s in enumerate([0, 4, 7]):
    x = sq(392*2**(s/12), 0.12, 0.25)*env(int(0.12*SR), 0.002, 0.03); put(b, x*0.3, k*0.09)
for s in [0, 4, 7, 12]:
    x = sq(523.25*2**(s/12), d, 0.25 if s else 0.5)*env(int(d*SR), 0.003, 0.7)*np.exp(-t(d)*1.2)
    put(b, x*0.25, 0.3)
put(b, sq(130.81, d, 0.5)*env(int(d*SR), 0.003, 0.6)*np.exp(-t(d)*1.5)*0.3, 0.3)
write('victory', b, 0.75)

# 5. gentle waves (noise, slow swells) - 10 s bed, quiet during grey part set by envelopes in file
D = 10.0; n = rng.uniform(-1, 1, int(D*SR)); w = lp(n, 0.05); w = w - lp(w, 0.002)
tt = t(D); swell = 0.55 + 0.45*np.sin(2*np.pi*tt/3.1)**2
lvl = np.interp(tt, [0, 2, 3, 5, 6.5, 7.2, 10], [0.6, 0.6, 0.12, 0.12, 0.2, 0.8, 0.8])
write('waves', w*swell*lvl, 0.5)

# 6. distant seagulls
b = np.zeros(int(2.4*SR))
def gull(at, f0):
    for j in range(2):
        d = 0.22; f = f0*(1.0 + 0.5*np.sin(np.pi*t(d)/d))  # rise and fall
        f = f*(1 + 0.02*np.sin(2*np.pi*35*t(d)))
        x = sq(f, d, 0.3)*env(int(d*SR), 0.02, 0.1)
        put(b, lp(x, 0.3)*0.5, at + j*0.28)
gull(0.0, 1100); gull(1.1, 1250)
write('gulls', b, 0.4)
