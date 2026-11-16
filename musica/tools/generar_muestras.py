import json, re, math, wave, struct, subprocess, sys, os

SR = 44100
REPO = "/home/user/Creaciones-del-mago"
ARR_DIR = os.path.join(REPO, "musica", "arreglos")
OUT_DIR = os.path.join(REPO, "musica", "muestras")
os.makedirs(OUT_DIR, exist_ok=True)

PIECES = {
    1: dict(bpm=70,  beats=4),
    2: dict(bpm=130, beats=4),
    3: dict(bpm=170, beats=3),
    4: dict(bpm=155, beats=4),
    5: dict(bpm=120, beats=4),
    6: dict(bpm=188, beats=3),
    7: dict(bpm=90,  beats=4),
    8: dict(bpm=60,  beats=4, beats_override={23: 3, 24: 3, 25: 3}),
}

SEMITONE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
DUR_BEATS = {"w": 4, "dh": 3, "h": 2, "dq": 1.5, "q": 1, "d8": 0.75, "8": 0.5, "16": 0.25, "32": 0.125}

NOTE_RE = re.compile(r"^([A-Ga-g])([#b]?)(-?\d+)")

def note_to_freq(s):
    if not s:
        return None
    m = NOTE_RE.match(s.strip())
    if not m:
        return None
    letter, acc, octave = m.group(1).upper(), m.group(2), int(m.group(3))
    semitone = SEMITONE[letter] + (1 if acc == "#" else -1 if acc == "b" else 0)
    midi = (octave + 1) * 12 + semitone
    return 440.0 * (2 ** ((midi - 69) / 12))

def clean_note(entry, prefer_key="nota_ajustada_rango", fallback_key="nota"):
    s = entry.get(prefer_key) or entry.get(fallback_key)
    return note_to_freq(s) if s else None

def measure_events(entry, beats_per_measure):
    if "notas" in entry:
        notes = entry["notas"]
        freqs = [note_to_freq(n) for n in notes]
        if "duracion" in entry:
            codes = [c.strip() for c in entry["duracion"].split(",")]
            durs = [DUR_BEATS.get(c, 1) for c in codes]
        else:
            durs = [beats_per_measure / len(notes)] * len(notes)
        return list(zip(freqs, durs))
    else:
        f = clean_note(entry)
        return [(f, beats_per_measure)]

def envelope(n, attack, release):
    env = [1.0] * n
    a = min(attack, n)
    r = min(release, n)
    for i in range(a):
        env[i] = i / max(a, 1)
    for i in range(r):
        env[n - 1 - i] = i / max(r, 1)
    return env

def tone(freq, duration, sr=SR, wave_shape="sine", vibrato=0.0, decay=False):
    n = max(1, int(duration * sr))
    out = [0.0] * n
    if freq is None:
        return out
    for i in range(n):
        t = i / sr
        f = freq
        if vibrato:
            f = freq * (1 + vibrato * math.sin(2 * math.pi * 5.5 * t))
        s = math.sin(2 * math.pi * f * t)
        if wave_shape == "warm":
            s += 0.3 * math.sin(2 * math.pi * f * 2 * t)
            s += 0.15 * math.sin(2 * math.pi * f * 3 * t)
        amp = 1.0
        if decay:
            amp = math.exp(-3.0 * t / max(duration, 1e-6))
        out[i] = s * amp
    a = int(0.01 * sr)
    r = int(0.04 * sr)
    env = envelope(n, a, r)
    return [out[i] * env[i] for i in range(n)]

def kick(duration=0.18, sr=SR):
    n = int(duration * sr)
    out = []
    for i in range(n):
        t = i / sr
        f = 150 - (110 * t / duration)
        amp = math.exp(-14 * t)
        out.append(math.sin(2 * math.pi * f * t) * amp)
    return out

def hat(duration=0.05, sr=SR):
    import random
    n = int(duration * sr)
    out = []
    for i in range(n):
        t = i / sr
        amp = math.exp(-40 * t)
        out.append((random.uniform(-1, 1)) * amp)
    return out

def snare(duration=0.14, sr=SR):
    import random
    n = int(duration * sr)
    out = []
    for i in range(n):
        t = i / sr
        amp = math.exp(-18 * t)
        tone_part = math.sin(2 * math.pi * 190 * t) * 0.4
        noise_part = random.uniform(-1, 1) * 0.8
        out.append((tone_part + noise_part) * amp)
    return out

def mix_into(master, start_sample, chunk, gain=1.0):
    for i, v in enumerate(chunk):
        idx = start_sample + i
        if idx < len(master):
            master[idx] += v * gain

def write_wav(path, samples, sr=SR):
    peak = max(0.001, max(abs(s) for s in samples))
    scale = 0.9 / peak
    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        frames = b"".join(struct.pack("<h", int(max(-32767, min(32767, s * scale * 32767)))) for s in samples)
        wf.writeframes(frames)

def render_piece(pid):
    cfg = PIECES[pid]
    bpm = cfg["bpm"]
    default_beats = cfg["beats"]
    overrides = cfg.get("beats_override", {})
    sec_per_beat = 60.0 / bpm

    with open(os.path.join(ARR_DIR, f"partitura-{pid}.json"), encoding="utf-8") as f:
        data = json.load(f)

    bajo = data.get("bajo", [])
    theremin = data.get("theremin", [])

    def events_for(track):
        out = []
        t = 0.0
        for entry in track:
            compas = entry.get("compas", "")
            m = re.match(r"\d+", str(compas))
            beats = overrides.get(int(m.group()), default_beats) if m else default_beats
            for freq, dur_beats in measure_events(entry, beats):
                out.append((t, freq, dur_beats * sec_per_beat))
                t += dur_beats * sec_per_beat
        return out, t

    bajo_ev, bajo_len = events_for(bajo)
    ther_ev, ther_len = events_for(theremin)

    target = 20.0
    total_len = min(max(bajo_len, ther_len), target if max(bajo_len, ther_len) > target else max(bajo_len, ther_len))
    total_len = max(total_len, 4.0)

    n_samples = int((total_len + 1.0) * SR)
    master = [0.0] * n_samples

    for t, freq, dur in bajo_ev:
        if t >= total_len:
            break
        chunk = tone(freq, min(dur, total_len - t + 0.3), wave_shape="warm", decay=True)
        mix_into(master, int(t * SR), chunk, gain=0.55)

    for t, freq, dur in ther_ev:
        if t >= total_len:
            break
        chunk = tone(freq, min(dur, total_len - t + 0.3), wave_shape="sine", vibrato=0.01)
        mix_into(master, int(t * SR), chunk, gain=0.5)

    beat = 0
    t = 0.0
    while t < total_len:
        pos = int(t * SR)
        if beat == 0:
            mix_into(master, pos, kick(), gain=0.8)
        elif beat == default_beats // 2:
            mix_into(master, pos, snare(), gain=0.6)
        mix_into(master, pos, hat(), gain=0.25)
        t += sec_per_beat
        beat = (beat + 1) % default_beats

    wav_path = os.path.join(OUT_DIR, f"partitura-{pid}.wav")
    mp3_path = os.path.join(OUT_DIR, f"partitura-{pid}.mp3")
    write_wav(wav_path, master)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", wav_path, "-b:a", "128k", mp3_path],
        check=True,
    )
    os.remove(wav_path)
    print(f"partitura-{pid}: {total_len:.1f}s -> {mp3_path}")

if __name__ == "__main__":
    ids = [int(a) for a in sys.argv[1:]] or list(PIECES.keys())
    for pid in ids:
        render_piece(pid)
