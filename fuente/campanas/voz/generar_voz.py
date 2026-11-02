#!/usr/bin/env python3
"""Genera una voz en off con la voz de la marca (Gemini TTS). Ver VOZ.md.

Uso:
  python3 generar_voz.py "Esta no come, no se muere y hace clic." salida.wav
  python3 generar_voz.py --archivo texto.txt salida.wav --notas "Más calmo, como de tarde de verano."
  python3 generar_voz.py "..." salida.wav --tomas 3        # 3 tomas (salida-1.wav, -2, -3) para elegir

Clave: variable GEMINI_API_KEY (en la sesión de Claude Code la pone el proxy y alcanza con cualquier valor).
Solo usa la biblioteca estándar de Python.
"""
import argparse, base64, json, os, sys, time, urllib.error, urllib.request

MODELO = "gemini-3.8-flash-tts"
VOZ = "es-419-techagent-10"          # voz de la marca, aprobada por el dueño el 2/11/2026

PERFIL = """# AUDIO PROFILE: El dueño de un taller chico de impresión 3D en Montevideo
## THE SCENE: Graba la voz en off de un reel de Instagram de 10 segundos, en su casa, cerca del micrófono.
### DIRECTOR'S NOTES
Estilo: español rioplatense con voseo, como alguien que le cuenta algo a un amigo. Cercano, relajado, humor seco, con una sonrisa leve. Nada de locutor ni de tono publicitario.
Ritmo: ágil, sin apuro. Pausa corta después de cada punto.{notas}
#### TRANSCRIPT
{texto}"""


def pedir(texto, voz, modelo, notas):
    prompt = PERFIL.format(texto=texto.strip(), notas=("\n" + notas.strip()) if notas else "")
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voz}}}}}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent",
        data=json.dumps(body).encode(), method="POST",
        headers={"Content-Type": "application/json", "x-goog-api-key": os.environ.get("GEMINI_API_KEY", "proxy")})
    for intento in range(4):
        try:
            d = json.load(urllib.request.urlopen(req, timeout=120))
            parte = d["candidates"][0]["content"]["parts"][0]["inlineData"]
            return base64.b64decode(parte["data"]), parte.get("mimeType", "")
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:300]
            if e.code in (429, 500, 503) and intento < 3:
                print(f"  {e.code}, reintento en {10 * (intento + 1)} s…"); time.sleep(10 * (intento + 1)); continue
            sys.exit(f"Error {e.code}: {msg}")


def a_wav(datos, mime, ruta):
    if datos[:4] == b"RIFF":                       # 3.8 devuelve WAV con cabecera
        open(ruta, "wb").write(datos); return
    import wave                                     # modelos viejos: PCM 16 bit 24 kHz sin cabecera
    w = wave.open(ruta, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(datos); w.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("texto", nargs="?")
    ap.add_argument("salida")
    ap.add_argument("--archivo")
    ap.add_argument("--voz", default=VOZ)
    ap.add_argument("--modelo", default=MODELO)
    ap.add_argument("--notas", help="indicaciones extra de tono o ritmo")
    ap.add_argument("--tomas", type=int, default=1)
    a = ap.parse_args()
    texto = open(a.archivo).read() if a.archivo else a.texto
    if not texto:
        sys.exit("Falta el texto.")
    for i in range(a.tomas):
        ruta = a.salida if a.tomas == 1 else a.salida.replace(".wav", f"-{i + 1}.wav")
        datos, mime = pedir(texto, a.voz, a.modelo, a.notas)
        a_wav(datos, mime, ruta); print("voz ->", ruta)


if __name__ == "__main__":
    main()
