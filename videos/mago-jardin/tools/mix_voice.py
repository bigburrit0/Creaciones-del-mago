#!/usr/bin/env python3
"""Mix a phone voice-over into the finished reel, ducking the music under the voice.

Usage:
  python3 tools/mix_voice.py VIDEO OUT VOICE                 # one take with the whole line
  python3 tools/mix_voice.py VIDEO OUT V1 V2 V3 V4           # one clip per phrase, placed on its cue

Any format the phone records (m4a, mp3, wav, ogg, opus...) works. Leading and
trailing silence is trimmed, the voice is cleaned (high-pass, gentle compression)
and normalised, and the original soundtrack is ducked while the voice speaks.
The video stream is copied untouched.
"""
import json
import subprocess
import sys

# when each phrase starts (seconds), matching the on-screen beats
CUES = [0.30, 2.45, 4.00, 8.10]   # «No da tomates:» / «da benteveos.» / «Es un comedero...» / «Escribime...»
SINGLE_START = 0.30
VOICE_CLEAN = ("highpass=f=90,lowpass=f=12000,"
               "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,"
               "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,"
               "acompressor=threshold=-20dB:ratio=3:attack=5:release=120,"
               "loudnorm=I=-15:TP=-1.5:LRA=7,aresample=48000,aformat=channel_layouts=stereo")


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", path],
                         check=True, capture_output=True, text=True).stdout
    return float(json.loads(out)["format"]["duration"])


def main(argv):
    if len(argv) not in (4, 7):
        sys.exit(__doc__)
    video, out, voices = argv[1], argv[2], argv[3:]
    total = duration(video)
    starts = [SINGLE_START] if len(voices) == 1 else CUES

    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", video]
    for v in voices:
        cmd += ["-i", v]
    parts, labels = [], []
    for i, t in enumerate(starts):
        ms = int(t * 1000)
        parts.append(f"[{i + 1}:a]{VOICE_CLEAN},adelay={ms}|{ms}[v{i}]")
        labels.append(f"[v{i}]")
    if len(labels) > 1:
        parts.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0,apad[vo]")
    else:
        parts.append(f"{labels[0]}apad[vo]")
    parts += [
        "[vo]asplit=2[vo_mix][vo_key]",
        # music, effects and birds drop ~10 dB while the voice speaks
        "[0:a]aresample=48000,aformat=channel_layouts=stereo[bed]",
        "[bed][vo_key]sidechaincompress=threshold=0.03:ratio=5:attack=15:release=350:makeup=1[ducked]",
        f"[ducked][vo_mix]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89,atrim=0:{total}[aout]",
    ]
    cmd += ["-filter_complex", ";".join(parts), "-map", "0:v", "-map", "[aout]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)

    # warn if the voice runs past the end of the video
    probe = subprocess.run(["ffmpeg", "-v", "error", "-i", voices[-1], "-af", VOICE_CLEAN, "-f", "wav", "-"],
                           check=True, capture_output=True).stdout
    last = (len(probe) - 44) / (48000 * 2 * 2)
    end = starts[-1] + last
    note = "OK" if end <= total - 0.2 else "ATENCIÓN: la voz se pasa del final; grabala un poco más rápido"
    print(f"{out}: voz termina en {end:.2f} s de {total:.2f} s — {note}")


if __name__ == "__main__":
    main(sys.argv)
