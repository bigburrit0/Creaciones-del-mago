#!/usr/bin/env python3
"""Voice-over with the Gemini TTS API: one WAV per phrase, ready for mix_voice.py.

Usage: python3 tools/tts_gemini.py OUT_DIR [--voice NAME] [--model MODEL]

The API key is never read here: the session's network proxy injects it for
generativelanguage.googleapis.com (a placeholder header is sent instead). Outside such
a proxy, set GEMINI_API_KEY.
"""
import argparse
import base64
import json
import os
import re
import subprocess
import sys
import time
import urllib.request

# the opening goes in one request (short lines alone get swallowed: "No da" came out as "Ah"),
# then it is split at its pause into v1 / v2 so each half lands on its cue
TAKES = [
    ("v1+v2", "No da tomates... da benteveos."),
    ("v3", "Es un comedero impreso en 3D, en PETG para el sol."),
    ("v4", "Escribime y te paso el precio."),
]
STYLE = """# AUDIO PROFILE: El narrador del Mago
A warm, calm man from Montevideo, Uruguay, narrating a cozy pixel-art farming video game.

### DIRECTOR'S NOTES
Accent: Rioplatense Spanish from Montevideo (voseo, "sh" sound for "ll" and "y").
Style: friendly, relaxed, a little playful smile in the voice. Natural pace, not slow.
Read ONLY the transcript below, exactly as written, nothing else.

#### TRANSCRIPT
"""


def tts(text, voice, model):
    body = {
        "contents": [{"parts": [{"text": STYLE + text}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}},
        },
    }
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        data=json.dumps(body).encode(), method="POST",
        headers={"Content-Type": "application/json", "x-goog-api-key": os.environ.get("GEMINI_API_KEY", "proxy-injected")})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.load(r)
            break
        except urllib.error.HTTPError as e:
            msg = e.read().decode()
            if e.code == 429 and "per minute" in msg.lower() or e.code in (500, 503):
                m = re.search(r"retry in ([0-9.]+)s", msg)
                wait = float(m.group(1)) + 2 if m else 25
                print(f"  rate limit, waiting {wait:.0f} s", file=sys.stderr)
                time.sleep(wait)
                continue
            sys.exit(f"TTS error {e.code}: {msg[:600]}")
    else:
        sys.exit("TTS: too many retries")
    part = data["candidates"][0]["content"]["parts"][0]["inlineData"]
    return base64.b64decode(part["data"]), part.get("mimeType", "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--voice", default="Charon")
    ap.add_argument("--model", default="gemini-3.8-flash-tts")   # free tier: 3 per minute, 10 per day
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    for name, text in TAKES:
        pcm, mime = tts(text, a.voice, a.model)
        out = os.path.join(a.out, name.split("+")[0] + ".wav")
        if pcm[:4] == b"RIFF":                       # already a WAV file
            src = ["-i", "-"]
        else:                                        # raw 16-bit PCM, e.g. audio/L16;rate=24000
            rate = int(mime.split("rate=")[1].split(";")[0]) if "rate=" in mime else 24000
            src = ["-f", "s16le", "-ar", str(rate), "-ac", "1", "-i", "-"]
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *src, out], input=pcm, check=True)
        if "+" in name:
            split_at_pause(out, os.path.join(a.out, "v2.wav"))
        print(name, out, mime)


def split_at_pause(path, second):
    """cut a two-part take at its longest inner silence: first half stays in path, second goes to `second`"""
    log = subprocess.run(["ffmpeg", "-i", path, "-af", "silencedetect=n=-40dB:d=0.15", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", log)]
    ends = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", log)]
    inner = [(e - s, s, e) for s, e in zip(starts, ends) if s > 0.3]
    if not inner:
        sys.exit(f"no pause found in {path}")
    _, s, e = max(inner)
    tmp = path + ".tmp.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-t", f"{s + 0.05:.3f}", tmp], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{max(0, e - 0.05):.3f}", "-i", path, second], check=True)
    os.replace(tmp, path)
    print(f"  split at pause {s:.2f}-{e:.2f} s")

if __name__ == "__main__":
    main()
