#!/usr/bin/env python3
"""A second pair of ears for the new music (videos/AUDIT_MUSICA.md): sends a reel's soundtrack to Gemini (audio
understanding) with a description of the video and asks for an honest critique: genre and instruments heard, whether
it fits the story, every effect with its time, anything harsh, distorted, cheap-sounding or masking a word, and a 1-10
score for fit and for production quality.
  python3 critica_audio.py REEL.mp4 "what happens in the video, beat by beat"
The key is never read here: the session's proxy injects it (CHECK_MODEL overrides the model, as in check_voces.py)."""
import base64, json, os, subprocess, sys, tempfile, urllib.request, urllib.error
MODEL = os.environ.get("CHECK_MODEL", "gemini-3.5-flash")
path, desc = sys.argv[1], sys.argv[2]
with tempfile.TemporaryDirectory() as td:
    mp3 = os.path.join(td, "a.mp3"); subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-vn", "-ac", "1", "-ar", "44100", "-b:a", "128k", mp3], check=True)
    data = base64.b64encode(open(mp3, "rb").read()).decode()
prompt = ("You are a strict music supervisor for comedic short-form videos (Instagram Reels). This is the full soundtrack of an animated reel: "
          "music, sound effects and two characters speaking Rioplatense Spanish. What happens in the video: " + desc + "\n"
          "Answer as JSON: {\"genre_and_instruments\": \"...\", \"fits_the_story\": \"...\", \"effects\": [{\"t\": seconds, \"what\": \"...\", \"funny_or_fitting\": \"yes/no\"}], "
          "\"problems\": [\"anything harsh, distorted, cheap or synthetic-sounding, too loud, masking a word, badly timed\"], \"fit_score\": 1-10, \"quality_score\": 1-10, "
          "\"top_fixes\": [\"the three changes that would help most\"]}")
body = {"contents": [{"parts": [{"text": prompt}, {"inlineData": {"mimeType": "audio/mp3", "data": data}}]}], "generationConfig": {"responseMimeType": "application/json"}}
req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent", data=json.dumps(body).encode(), method="POST",
                             headers={"Content-Type": "application/json", "x-goog-api-key": os.environ.get("GEMINI_API_KEY", "proxy-injected")})
try:
    d = json.load(urllib.request.urlopen(req, timeout=240)); print(d["candidates"][0]["content"]["parts"][0]["text"].strip())
except urllib.error.HTTPError as e: print(f"HTTP {e.code}")
