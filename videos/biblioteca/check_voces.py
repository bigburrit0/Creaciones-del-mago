#!/usr/bin/env python3
"""Listen-check voices with Gemini (audio understanding): transcribe each line ONE BY ONE (several clips in one request
can shift the ids), or the final mix of a rendered reel to confirm every line is intelligible over music and effects.

  python3 check_voces.py clips voz3d/s1.wav voz3d/m1.wav ...
  python3 check_voces.py mix reel.mp4

Audio is sent as 16 kHz mono mp3 (a request with several WAV clips failed with 502). Do not put example words in the
prompt (an example "jo, jo, jo" made the transcriber add it). The API key is never read here: the session's proxy
injects it for generativelanguage.googleapis.com; outside such a proxy, set GEMINI_API_KEY.
"""
import base64, json, os, subprocess, sys, tempfile, urllib.request
MODEL = os.environ.get("CHECK_MODEL", "gemini-3.5-flash")

def ask(prompt, path, mime_json=False):
    with tempfile.TemporaryDirectory() as td:
        mp3 = os.path.join(td, "a.mp3")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-vn", "-ac", "1", "-ar", "16000", "-b:a", "48k", mp3], check=True)
        data = base64.b64encode(open(mp3, "rb").read()).decode()
    body = {"contents": [{"parts": [{"text": prompt}, {"inlineData": {"mimeType": "audio/mp3", "data": data}}]}]}
    if mime_json: body["generationConfig"] = {"responseMimeType": "application/json"}
    req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent", data=json.dumps(body).encode(),
                                 method="POST", headers={"Content-Type": "application/json", "x-goog-api-key": os.environ.get("GEMINI_API_KEY", "proxy-injected")})
    try:
        d = json.load(urllib.request.urlopen(req, timeout=180)); return d["candidates"][0]["content"]["parts"][0]["text"].strip()
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}"

if __name__ == "__main__":
    mode, files = sys.argv[1], sys.argv[2:]
    if mode == "clips":
        for f in files: print(os.path.basename(f), "->", ask("Transcribe this short Spanish audio clip exactly, laughs and interjections included. Answer only the transcript.", f))
    else:
        print(ask("This is the soundtrack of a short animated reel (music, sound effects and characters speaking Rioplatense Spanish). List every spoken line with "
                  "its approximate start time in seconds and whether it is clearly intelligible over the music and effects (yes/partly/no), then one sentence on "
                  "the voice-vs-music balance. Answer as JSON: {\"lines\": [{\"t\", \"text\", \"clear\"}], \"balance\": \"...\"}.", files[0], True))
