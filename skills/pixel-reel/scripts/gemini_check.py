"""Check the Gemini setup without spending and without revealing the key.

  python3 gemini_check.py

Prints whether GEMINI_API_KEY is set (only its length), whether the API host is reachable, and the image models the
key can use (models.list is a free metadata call; no image is generated).
"""
import os, sys

key = os.environ.get("GEMINI_API_KEY") or ""
if not key:
    print("GEMINI_API_KEY: no está definida en esta sesión"); sys.exit(1)
print(f"GEMINI_API_KEY: presente ({len(key)} caracteres)")
try:
    from google import genai
except ImportError:
    print("falta el SDK: pip install google-genai"); sys.exit(1)
try:
    cl = genai.Client()
    names = [(m.name or "").split("/")[-1] for m in cl.models.list()]
    img = sorted(n for n in names if "image" in n)
    print(f"API: conectada ({len(names)} modelos visibles)")
    print("modelos de imagen:", ", ".join(img) or "(ninguno)")
except Exception as e:  # never echo the key
    print("API: error ->", str(e).replace(key, "***")[:300]); sys.exit(2)
