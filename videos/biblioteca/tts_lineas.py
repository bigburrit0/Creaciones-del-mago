#!/usr/bin/env python3
"""Character dialogue with the Gemini TTS API: ONE request per character (all their lines in one take,
so short lines are not swallowed), then the take is cut at its pauses into one WAV per line.

Usage: python3 tts_lineas.py LINES.json OUT_DIR [--model MODEL]

LINES.json: {"Santa": {"voice": "Algenib", "style": "...", "lines": [["s1", "text"], ...]}, ...}
Writes OUT_DIR/<id>_raw.wav (the cut takes), then OUT_DIR/<id>.wav after the optional "_edits" (keep a span with
"from"/"to", or shorten an inner pause with "squeeze": [start, end, new_length]) and loudness matching, and
OUT_DIR/durations.json. --post-only redoes the edits without calling the API.

The API key is never read or printed here: the session's network proxy injects it for
generativelanguage.googleapis.com (a placeholder header is sent). Outside such a proxy, set GEMINI_API_KEY.
Free tier: about 3 requests per minute and 10 per day, so a character's lines always go in a single request.
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

PROMPT = """# AUDIO PROFILE: {name}
{style}

### DIRECTOR'S NOTES
Accent: Rioplatense Spanish from Montevideo, Uruguay (voseo, "sh" sound for "ll" and "y").
Each line is a separate moment of a short animated video: act each one fully, then leave a clear pause of
about one second of silence before the next line.
Read ONLY the transcript below, exactly as written, nothing else.

#### TRANSCRIPT
"""


def tts(prompt, voice, model):
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        data=json.dumps(body).encode(), method="POST",
        headers={"Content-Type": "application/json", "x-goog-api-key": os.environ.get("GEMINI_API_KEY", "proxy-injected")})
    for _ in range(6):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                data = json.load(r)
            break
        except urllib.error.HTTPError as e:
            msg = e.read().decode()
            if (e.code == 429 and "per minute" in msg.lower()) or e.code in (500, 503):
                m = re.search(r"retry in ([0-9.]+)s", msg)
                wait = float(m.group(1)) + 2 if m else 25
                print(f"  rate limit or busy, waiting {wait:.0f} s", file=sys.stderr)
                time.sleep(wait)
                continue
            sys.exit(f"TTS error {e.code}: {msg[:400]}")
    else:
        sys.exit("TTS: too many retries")
    part = data["candidates"][0]["content"]["parts"][0]["inlineData"]
    return base64.b64decode(part["data"]), part.get("mimeType", "")


def to_wav(pcm, mime, out):
    if pcm[:4] == b"RIFF":
        src = ["-i", "-"]
    else:
        rate = int(mime.split("rate=")[1].split(";")[0]) if "rate=" in mime else 24000
        src = ["-f", "s16le", "-ar", str(rate), "-ac", "1", "-i", "-"]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *src, "-ar", "48000", out], input=pcm, check=True)


def silences(path, db=-38, d=0.18):
    log = subprocess.run(["ffmpeg", "-i", path, "-af", f"silencedetect=n={db}dB:d={d}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    s = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", log)]
    e = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", log)]
    dur = float(re.search(r"Duration: (\d+):(\d+):([0-9.]+)", log).group(3))
    return list(zip(s, e)), dur


def split(take, ids, out_dir):
    """cut at the len(ids)-1 longest inner pauses, trim each piece, write <id>.wav"""
    sil, dur = silences(take)
    inner = [(e - s, s, e) for s, e in sil if s > 0.25 and e < dur - 0.05]
    if len(inner) < len(ids) - 1:
        sys.exit(f"{take}: found {len(inner)} pauses, need {len(ids) - 1}")
    cuts = sorted(inner, reverse=True)[:len(ids) - 1]
    cuts = sorted(((s + e) / 2, s, e) for _, s, e in cuts)
    bounds = [0.0] + [m for m, _, _ in cuts] + [dur]
    out = {}
    for k, i in enumerate(ids):
        a, b = bounds[k], bounds[k + 1]
        dst = os.path.join(out_dir, f"{i}_raw.wav")
        # trim silence at both ends, keep 40 ms of air, short fades so cuts never click
        af = ("silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.04,areverse,"
              "silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.06,areverse,"
              "afade=t=in:d=0.012")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", take,
                        "-af", af, dst], check=True)
        d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", dst],
                                 capture_output=True, text=True).stdout)
        out[i] = round(d, 3)
        print(f"  {i}: {a:.2f}-{b:.2f} s -> {d:.2f} s")
    return out


def post(out_dir, cfg):
    """final <id>.wav from <id>_raw.wav: optional cuts from cfg["edits"] (keep a span, or shorten a pause), then
    loudness matched across all lines (-16 LUFS, peaks under -2 dBTP) at 48 kHz"""
    durs = {}
    edits = cfg.get("_edits", {})
    for name, c in cfg.items():
        if name.startswith("_"):
            continue
        for i, _ in c["lines"]:
            src, dst, ed = os.path.join(out_dir, f"{i}_raw.wav"), os.path.join(out_dir, f"{i}.wav"), edits.get(i, {})
            if "squeeze" in ed:                    # [start, end, new_length] of an inner pause
                s0, e0, keep = ed["squeeze"]
                cut = f"aselect='not(between(t,{s0 + keep / 2:.3f},{e0 - keep / 2:.3f}))',asetpts=N/SR/TB,"
            else:
                cut = ""
            span = ["-ss", f"{ed.get('from', 0):.3f}"] + (["-to", f"{ed['to']:.3f}"] if "to" in ed else [])
            af = cut + "afade=t=in:d=0.01,areverse,afade=t=in:d=0.03,areverse,loudnorm=I=-16:TP=-2:LRA=7,aresample=48000"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *span, "-i", src, "-af", af, "-ar", "48000", dst], check=True)
            d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", dst],
                                     capture_output=True, text=True).stdout)
            durs[i] = round(d, 3)
    json.dump(durs, open(os.path.join(out_dir, "durations.json"), "w"), indent=1)
    print("final:", durs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lines")
    ap.add_argument("out")
    ap.add_argument("--model", default="gemini-3.8-flash-tts")
    ap.add_argument("--only", default="", help="comma-separated character names to (re)generate")
    ap.add_argument("--post-only", action="store_true", help="only redo the cuts and loudness from the raw takes")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    cfg = json.load(open(a.lines))
    durs = {}
    only = [x for x in a.only.split(",") if x]
    if a.post_only:
        post(a.out, cfg); return
    for name, c in cfg.items():
        if name.startswith("_") or (only and name not in only):
            continue
        ids = [i for i, _ in c["lines"]]
        text = "\n\n".join(t for _, t in c["lines"])
        print(f"{name} ({c['voice']}): {len(ids)} lines in one request")
        pcm, mime = tts(PROMPT.format(name=name, style=c["style"]) + text, c["voice"], a.model)
        take = os.path.join(a.out, f"_take_{name}.wav")
        to_wav(pcm, mime, take)
        durs.update(split(take, ids, a.out))
    post(a.out, cfg)


if __name__ == "__main__":
    main()
