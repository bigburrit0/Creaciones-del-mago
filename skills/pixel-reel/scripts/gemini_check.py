"""Check the Gemini setup without spending and without revealing the key.
Works with GEMINI_API_KEY in the environment or with a network secret (proxy-injected x-goog-api-key header).
models.list is a free metadata call; no image is generated."""
import os, sys
key = os.environ.get("GEMINI_API_KEY") or ""
print(f"GEMINI_API_KEY: presente ({len(key)} caracteres)" if key else "GEMINI_API_KEY: no definida; se prueba el secreto de red (el proxy agrega la clave)")
if not key: os.environ["GEMINI_API_KEY"] = "proxy-injected"
try:
    from google import genai
except ImportError:
    print("falta el SDK: pip install google-genai"); sys.exit(1)
try:
    cl = genai.Client(); names = [(m.name or "").split("/")[-1] for m in cl.models.list()]
    print(f"API: conectada ({len(names)} modelos)"); print("modelos de imagen:", ", ".join(sorted(n for n in names if "image" in n)))
except Exception as e:
    print("API: error ->", (str(e).replace(key, "***") if key else str(e))[:300]); sys.exit(2)
