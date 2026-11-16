import json, re, math, wave, struct, subprocess, sys, os
import numpy as np

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

# Consonant intervals above a bass note (mod 12): unison, min3, maj3, 5th, min6, maj6, octave.
# Grounded in first-species counterpoint (perfect + imperfect consonances) -- see README.
CONSONANT_PCS = [0, 3, 4, 7, 8, 9]
DISSONANT_PCS = {1, 2, 6, 10, 11}  # m2/M2/tritone/m7/M7 against the bass: resolve these


def midi_from_note(s):
    if not s:
        return None
    m = NOTE_RE.match(s.strip())
    if not m:
        return None
    letter, acc, octave = m.group(1).upper(), m.group(2), int(m.group(3))
    semitone = SEMITONE[letter] + (1 if acc == "#" else -1 if acc == "b" else 0)
    return (octave + 1) * 12 + semitone


def freq_from_midi(m):
    return 440.0 * (2 ** ((m - 69) / 12.0))


def parse_durs(entry, beats_per_measure, n):
    if "duracion" in entry:
        codes = [c.strip() for c in entry["duracion"].split(",")]
        return [DUR_BEATS.get(c, 1) for c in codes]
    return [beats_per_measure / n] * n


def beats_for(cfg, compas_str):
    m = re.match(r"\d+", str(compas_str))
    if not m:
        return cfg["beats"]
    return cfg.get("beats_override", {}).get(int(m.group()), cfg["beats"])


def build_bass_hits(bajo, cfg, sec_per_beat):
    """Real bass-line rule: state the chord root on the downbeat and its fifth on
    the next strong beat (root-fifth 'oom-pah' pattern), the classic foundation
    of a functional bass line, instead of one static drone per measure."""
    hits = []  # (start, dur, midi)
    t = 0.0
    for entry in bajo:
        beats = beats_for(cfg, entry.get("compas", ""))
        if "notas" in entry:
            notes = entry["notas"]
            durs = parse_durs(entry, beats, len(notes))
            for n, d in zip(notes, durs):
                midi = midi_from_note(n)
                if midi is not None:
                    hits.append((t, d * sec_per_beat, midi))
                t += d * sec_per_beat
            continue
        root = midi_from_note(entry.get("nota"))
        if root is None:
            t += beats * sec_per_beat
            continue
        fifth = root + 7
        if beats >= 4:
            pattern = [(root, 2), (fifth, 1), (root, 1)]
        elif beats == 3:
            pattern = [(root, 1), (fifth, 1), (root, 1)]
        elif beats == 2:
            pattern = [(root, 1), (fifth, 1)]
        else:
            pattern = [(root, beats)]
        for midi, d in pattern:
            hits.append((t, d * sec_per_beat, midi))
            t += d * sec_per_beat
    return hits, t


def build_theremin_targets(theremin, cfg, sec_per_beat):
    """Structural melody tones (the extracted top-voice line). These become the
    anchor points; the renderer connects them with a portamento glide, acting
    as the passing/neighbor-tone motion a monophonic theremin would play
    between chord tones instead of jumping statically bar to bar."""
    targets = []  # (time, midi)
    t = 0.0
    for entry in theremin:
        beats = beats_for(cfg, entry.get("compas", ""))
        if "notas" in entry:
            notes = entry["notas"]
            durs = parse_durs(entry, beats, len(notes))
            for n, d in zip(notes, durs):
                midi = midi_from_note(n)
                if midi is not None:
                    targets.append([t, midi])
                t += d * sec_per_beat
            continue
        note = entry.get("nota_ajustada_rango") or entry.get("nota")
        midi = midi_from_note(note) if note else None
        if midi is not None:
            targets.append([t, midi])
        t += beats * sec_per_beat
    return targets, t


def bass_midi_at(hits, time):
    best = None
    for s, d, m in hits:
        if s <= time < s + d:
            return m
        if s <= time:
            best = m
    return best


def snap_to_consonance(midi, bass_midi):
    """First-species-style rule: the melody must sound a consonance (unison,
    3rd, 5th, 6th, octave) against the bass on a structural tone. A clashing
    2nd/tritone/7th gets pulled to the nearest consonant chord tone instead."""
    if bass_midi is None:
        return midi
    interval = (midi - bass_midi) % 12
    if interval not in DISSONANT_PCS:
        return midi
    best, best_diff = midi, 999
    for pc in CONSONANT_PCS:
        for oct_shift in (-12, 0, 12):
            cand = bass_midi + pc + oct_shift
            diff = abs(cand - midi)
            if diff < best_diff:
                best_diff, best = diff, cand
    return best


def render_bass(hits, total_len, sr=SR):
    n = int((total_len + 1.5) * sr)
    out = np.zeros(n)
    for start, dur, midi in hits:
        if start >= total_len:
            continue
        freq = freq_from_midi(midi)
        d = min(dur, total_len - start + 0.4)
        ns = max(1, int(d * sr))
        t = np.arange(ns) / sr
        tone = (np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(2 * np.pi * freq * 2 * t)
                + 0.15 * np.sin(2 * np.pi * freq * 3 * t))
        env = np.exp(-2.2 * t / max(d, 1e-6))
        a = min(int(0.008 * sr), ns)
        if a > 1:
            env[:a] *= np.linspace(0, 1, a)
        tone = tone * env
        s0 = int(start * sr)
        s1 = min(n, s0 + ns)
        out[s0:s1] += tone[: s1 - s0] * 0.5
    return out


def render_theremin(targets, total_len, sr=SR, hold_frac=0.72):
    n = int((total_len + 1.5) * sr)
    out = np.zeros(n)
    if not targets:
        return out
    # tail hold for the final note
    targets = targets + [[total_len + 1.0, targets[-1][1]]]
    for i in range(len(targets) - 1):
        t0, m0 = targets[i]
        t1, m1 = targets[i + 1]
        if t0 >= total_len + 1.0:
            break
        seg_dur = max(t1 - t0, 0.05)
        hold_dur = seg_dur * hold_frac
        glide_dur = seg_dur - hold_dur
        n_hold = max(1, int(hold_dur * sr))
        n_glide = max(1, int(glide_dur * sr))
        f0, f1 = freq_from_midi(m0), freq_from_midi(m1)
        freqs = np.concatenate([np.full(n_hold, f0), np.linspace(f0, f1, n_glide)])
        tt = np.arange(len(freqs)) / sr
        vibrato = 1 + 0.01 * np.sin(2 * np.pi * 5.5 * tt)
        phase = np.cumsum(2 * np.pi * (freqs * vibrato) / sr)
        tone = np.sin(phase)
        s0 = int(t0 * sr)
        s1 = min(n, s0 + len(tone))
        if s1 > s0:
            out[s0:s1] += tone[: s1 - s0] * 0.45
    # overall attack/release so it doesn't click at the very start/end
    a = min(int(0.03 * sr), n)
    out[:a] *= np.linspace(0, 1, a)
    return out


def kick(sr=SR, duration=0.18):
    n = int(duration * sr)
    t = np.arange(n) / sr
    f = 150 - 110 * t / duration
    phase = np.cumsum(2 * np.pi * f / sr)
    return np.sin(phase) * np.exp(-14 * t)


def hat(sr=SR, duration=0.05):
    n = int(duration * sr)
    t = np.arange(n) / sr
    rng = np.random.default_rng(0)
    return rng.uniform(-1, 1, n) * np.exp(-40 * t)


def snare(sr=SR, duration=0.14):
    n = int(duration * sr)
    t = np.arange(n) / sr
    rng = np.random.default_rng(1)
    tone_part = np.sin(2 * np.pi * 190 * t) * 0.4
    noise_part = rng.uniform(-1, 1, n) * 0.8
    return (tone_part + noise_part) * np.exp(-18 * t)


def mix(master, start_sample, chunk, gain=1.0):
    n = len(master)
    s0 = max(0, start_sample)
    s1 = min(n, start_sample + len(chunk))
    if s1 > s0:
        master[s0:s1] += chunk[: s1 - s0] * gain


def add_reverb(buf, sr=SR):
    out = buf.copy()
    for delay_s, g in [(0.045, 0.22), (0.09, 0.12)]:
        d = int(delay_s * sr)
        out[d:] += buf[: len(buf) - d] * g
    return out


def write_wav(path, samples, sr=SR):
    peak = max(0.001, float(np.max(np.abs(samples))))
    scale = 0.9 / peak
    ints = np.clip(samples * scale * 32767, -32767, 32767).astype(np.int16)
    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(ints.tobytes())


def render_piece(pid, target_seconds=20.0):
    cfg = PIECES[pid]
    bpm = cfg["bpm"]
    sec_per_beat = 60.0 / bpm

    with open(os.path.join(ARR_DIR, f"partitura-{pid}.json"), encoding="utf-8") as f:
        data = json.load(f)

    bajo = data.get("bajo", [])
    theremin = data.get("theremin", [])

    bass_hits, bass_len = build_bass_hits(bajo, cfg, sec_per_beat)
    targets, ther_len = build_theremin_targets(theremin, cfg, sec_per_beat)

    # consonance rule: snap each structural melody tone against the bass sounding then
    for pair in targets:
        pair[1] = snap_to_consonance(pair[1], bass_midi_at(bass_hits, pair[0]))

    total_len = max(bass_len, ther_len, 4.0)
    total_len = min(total_len, target_seconds) if total_len > target_seconds else total_len

    n = int((total_len + 1.5) * SR)
    master = np.zeros(n)

    master += render_bass([h for h in bass_hits if h[0] < total_len], total_len)
    master += render_theremin([p for p in targets if p[0] < total_len], total_len)

    default_beats = cfg["beats"]
    t, beat = 0.0, 0
    while t < total_len:
        pos = int(t * SR)
        if beat == 0:
            mix(master, pos, kick(), gain=0.8)
        elif beat == default_beats // 2:
            mix(master, pos, snare(), gain=0.55)
        mix(master, pos, hat(), gain=0.22)
        t += sec_per_beat
        beat = (beat + 1) % default_beats

    master = add_reverb(master)

    wav_path = os.path.join(OUT_DIR, f"partitura-{pid}.wav")
    mp3_path = os.path.join(OUT_DIR, f"partitura-{pid}.mp3")
    write_wav(wav_path, master)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav_path, "-b:a", "128k", mp3_path], check=True)
    os.remove(wav_path)
    print(f"partitura-{pid}: {total_len:.1f}s -> {mp3_path}")


if __name__ == "__main__":
    ids = [int(a) for a in sys.argv[1:]] or list(PIECES.keys())
    for pid in ids:
        render_piece(pid)
