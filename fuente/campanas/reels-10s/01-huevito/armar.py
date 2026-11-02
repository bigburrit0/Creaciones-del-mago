#!/usr/bin/env python3
"""Arma el Reel 1 «Huevito» a partir del video de Gemini: textos pixel, cierre, SFX, música y voz.

Uso (desde esta carpeta):
  python3 armar.py                       # versión con la voz de timeline.json (voz/toma-gemini-...)
  python3 armar.py --sin-voz             # versión sin voz (para pegar otra voz en CapCut)
  python3 armar.py --voz mi-toma.wav     # otra toma de la frase completa: se corta en 5 frases y se ubica sola
  python3 armar.py --voz mi-toma.wav --una-toma 0.3   # la toma entera, sin cortar, desde 0,3 s

Requiere: ffmpeg, Python 3 con numpy, Pillow y fontTools. El video base va en base/huevito-gemini.mp4
(no se versiona). Todo lo que se genera queda en salida/.
"""
import argparse, json, os, subprocess, sys, wave
sys.dont_write_bytecode = True
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, "../../../.."))
W, H = 1080, 1920
SR = 44100


def ruta(p):
    return p if os.path.isabs(p) else os.path.join(AQUI, p)


def hexrgb(h, a=255):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


# ---------------------------------------------------------------- fuente pixel

def fuente_ttf(salida):
    """MagoPixel viene en WOFF (la del sitio): se pasa a TTF para Pillow."""
    from fontTools.ttLib import TTFont
    ttf = os.path.join(salida, "MagoPixel-Bold.ttf")
    if not os.path.exists(ttf):
        f = TTFont(os.path.join(RAIZ, "fonts/MagoPixel-Bold.woff")); f.flavor = None; f.save(ttf)
    return ttf


class Texto:
    """Texto en MagoPixel con un píxel de fuente = k píxeles de pantalla (la fuente usa una grilla de 100 unidades/em 1000)."""
    _cache = {}

    def __init__(self, ttf):
        self.ttf = ttf

    def font(self, k):
        if k not in self._cache:
            f = ImageFont.truetype(self.ttf, 10 * k); self._cache[k] = f
        return self._cache[k]

    def ancho(self, s, k):
        return int(round(self.font(k).getlength(s)))

    def mascara(self, s, k):
        f = self.font(k); w = self.ancho(s, k) + 4 * k; h = 13 * k
        m = Image.new("L", (w, h), 0); d = ImageDraw.Draw(m); d.fontmode = "1"
        d.text((2 * k, 2 * k), s, font=f, fill=255)
        return m  # origen del texto en (2k, 2k)

    def dibujar(self, lienzo, s, k, x, y, relleno, contorno=None, sombra=True):
        """x, y = esquina sup. izq. de la caja del texto. Contorno cuadrado de 1 píxel de fuente + sombra de 1 píxel abajo."""
        if not s:
            return
        m = self.mascara(s, k); ox, oy = x - 2 * k, y - 2 * k
        if contorno:
            dil = m.filter(ImageFilter.MaxFilter(2 * k + 1))
            capa = Image.new("RGBA", m.size, contorno)
            if sombra:
                lienzo.paste(capa, (ox, oy + k), dil)
            lienzo.paste(capa, (ox, oy), dil)
        lienzo.paste(Image.new("RGBA", m.size, relleno), (ox, oy), m)


def visibles(s, t, desde, cps):
    if t < desde:
        return 0
    return min(len(s), int((t - desde) * cps + 1e-6) + 1)


def tiempo_fin_tipeo(s, desde, cps):
    return desde + (len(s) - 1) / cps


# ---------------------------------------------------------------- capa de textos (RGBA por cuadro)

class Capa:
    def __init__(self, tl, ttf):
        self.tl = tl; self.tx = Texto(ttf); c = tl["colores"]
        self.crema, self.indigo, self.oro = hexrgb(c["crema"]), hexrgb(c["indigo"]), hexrgb(c["oro"])
        self.indigo2 = hexrgb(c["indigo2"])
        g = tl["cierre"]["glifo"]
        self.glifo = Image.open(ruta(g["archivo"])).convert("RGBA")
        self._cache = {}
        self._prep_cierre()

    def _prep_cierre(self):
        ci = self.tl["cierre"]; cj = ci["caja"]; tx = self.tx
        filas = []; y = cj["y"] + cj["borde"] + 50
        for ln in ci["lineas"]:
            if ln.get("separador"):
                filas.append(dict(ln, y=y + 6)); y += 28; continue
            filas.append(dict(ln, y=y, w=tx.ancho(ln["texto"], ln["k"]))); y += 10 * ln["k"] + 8
        ancho = max(f["w"] for f in filas if "w" in f) + 2 * cj["padding_x"]
        ancho = min(ancho, W - 2 * 60)
        self.caja = (W // 2 - ancho // 2, cj["y"], W // 2 + ancho // 2, y + 22)
        self.filas = filas

    def _clave(self, t):
        """Estado visible en t (para no redibujar cuadros iguales)."""
        tl = self.tl; cps = tl["tipeo_cps"]; partes = []
        for bloque in tl["textos"]:
            if bloque["desde"] <= t < bloque["hasta"]:
                for ln in bloque["lineas"]:
                    n = visibles(ln["texto"], t, ln.get("desde", bloque["desde"]), cps["titulos"])
                    partes.append(n)
                partes.append(self._cursor(t, bloque))
            else:
                partes.append(None)
        ci = tl["cierre"]
        if t >= ci["desde"]:
            f = int((t - ci["desde"]) * tl["fps"] + 1e-6)
            partes.append(min(f, 6))
            for ln in self.filas:
                if "texto" in ln:
                    partes.append(visibles(ln["texto"], t, ln["desde"], cps["cierre"]))
        return tuple(partes)

    def _cursor(self, t, bloque):
        """Cursor dorado que parpadea mientras tipea y hasta 0,5 s después; devuelve índice de línea o -1."""
        cps = self.tl["tipeo_cps"]["titulos"]; activo = -1
        for i, ln in enumerate(bloque["lineas"]):
            d = ln.get("desde", bloque["desde"])
            if t >= d:
                activo = i
        if activo < 0:
            return -1
        ln = bloque["lineas"][activo]; d = ln.get("desde", bloque["desde"])
        fin = tiempo_fin_tipeo(ln["texto"], d, cps)
        if t <= fin:
            return activo
        if t - fin < 0.5 and int((t - fin) * 8) % 2 == 0:
            return activo
        return -1

    def cuadro(self, t):
        clave = self._clave(t)
        if clave in self._cache:
            return self._cache[clave]
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        tl = self.tl; cps = tl["tipeo_cps"]; tx = self.tx
        for bloque in tl["textos"]:
            if not (bloque["desde"] <= t < bloque["hasta"]):
                continue
            cur = self._cursor(t, bloque)
            for i, ln in enumerate(bloque["lineas"]):
                s, k = ln["texto"], ln["k"]; w = tx.ancho(s, k); x = (W - w) // 2
                n = visibles(s, t, ln.get("desde", bloque["desde"]), cps["titulos"])
                tx.dibujar(im, s[:n], k, x, ln["y"], self.crema, self.indigo)
                if i == cur and n > 0:
                    cx = x + tx.ancho(s[:n], k) + k
                    d = ImageDraw.Draw(im)
                    d.rectangle([cx - k, ln["y"] + k, cx + 5 * k, ln["y"] + 9 * k], fill=self.indigo)
                    d.rectangle([cx, ln["y"] + 2 * k, cx + 4 * k - 1, ln["y"] + 8 * k - 1], fill=self.oro)
        ci = tl["cierre"]
        if t >= ci["desde"]:
            f = int((t - ci["desde"]) * tl["fps"] + 1e-6)
            self._caja(im, min(1.0, (f + 1) / 4))
            self._glifo(im, f)
            if f >= 3:
                for ln in self.filas:
                    if ln.get("separador"):
                        if t >= ln.get("desde", 9.3):
                            self._separador(im, ln["y"])
                        continue
                    n = visibles(ln["texto"], t, ln["desde"], cps["cierre"])
                    col = self.oro if ln["color"] == "oro" else self.crema
                    x = (W - ln["w"]) // 2
                    tx.dibujar(im, ln["texto"][:n], ln["k"], x, ln["y"], col, self.indigo2, sombra=False)
        self._cache[clave] = im
        return im

    def _caja(self, im, frac):
        x0, y0, x1, y1 = self.caja; b = self.tl["cierre"]["caja"]["borde"]
        cy = (y0 + y1) // 2; h = int((y1 - y0) * frac) // 2
        y0, y1 = cy - h, cy + h
        d = ImageDraw.Draw(im)
        d.rectangle([x0 + 2 * b, y0 + 2 * b, x1 + 2 * b, y1 + 2 * b], fill=(0, 0, 0, 90))      # sombra
        # borde dorado con esquinas en escalón (estilo ventana de RPG)
        d.rectangle([x0 + b, y0, x1 - b, y1], fill=self.oro)
        d.rectangle([x0, y0 + b, x1, y1 - b], fill=self.oro)
        d.rectangle([x0 + b, y0 + b, x1 - b, y1 - b], fill=self.indigo)
        if y1 - y0 > 6 * b:
            d.rectangle([x0 + 2 * b, y0 + 2 * b, x1 - 2 * b, y1 - 2 * b], outline=self.indigo2, width=b // 2)

    def _glifo(self, im, f):
        g = self.tl["cierre"]["glifo"]; esc = g["escala"]
        if f < 1:
            return
        s = {1: 1, 2: 3}.get(f, esc)                 # aparece chico, se pasa y vuelve: pop por pasos
        gi = self.glifo.resize((self.glifo.width * s, self.glifo.height * s), Image.NEAREST)
        cx = W // 2; base_y = g["y"] + self.glifo.height * esc
        x, y = cx - gi.width // 2, base_y - gi.height
        y = max(y, 252)
        # contorno índigo de 1 px de arte alrededor del glifo, para que se despegue del cielo
        a = gi.getchannel("A").point(lambda v: 255 if v > 0 else 0).filter(ImageFilter.MaxFilter(2 * s + 1))
        im.paste(Image.new("RGBA", gi.size, self.indigo), (x, y), a)
        im.alpha_composite(gi, (x, y))

    def _separador(self, im, y):
        x0, _, x1, _ = self.caja; d = ImageDraw.Draw(im); p = 6
        for x in range(x0 + 60, x1 - 60, 3 * p):
            d.rectangle([x, y, x + p - 1, y + p - 1], fill=self.oro)


# ---------------------------------------------------------------- audio

def leer_wav(path):
    """Cualquier audio -> float32 mono 44,1 kHz (vía ffmpeg)."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def escribir_wav(path, x):
    x = np.clip(x, -1, 1)
    st = np.stack([x, x], 1)
    w = wave.open(path, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype("<i2").tobytes()); w.close()


def tramos_de_voz(x, n_frases, umbral_db=-40, min_sil=0.08):
    """Corta una toma en n frases usando los n-1 silencios más largos."""
    win = int(0.01 * SR); e = np.sqrt(np.convolve(x ** 2, np.ones(win) / win, "same") + 1e-12)
    habla = 20 * np.log10(e) > umbral_db
    idx = np.flatnonzero(habla)
    if len(idx) == 0:
        sys.exit("La toma de voz está en silencio.")
    ini, fin = idx[0], idx[-1]
    sil = []; i = ini
    while i < fin:
        if not habla[i]:
            j = i
            while j < fin and not habla[j]:
                j += 1
            if (j - i) / SR >= min_sil:
                sil.append((j - i, i, j))
            i = j
        else:
            i += 1
    if len(sil) < n_frases - 1:
        return None
    cortes = sorted(sorted(sil, reverse=True)[:n_frases - 1], key=lambda s: s[1])
    tramos = []; a = ini
    for _, s0, s1 in cortes:
        tramos.append((a, s0)); a = s1
    tramos.append((a, fin))
    return tramos


def colocar_voz(tl, toma, una_toma=None):
    D = tl["duracion"]; voz = np.zeros(int(D * SR)); x = leer_wav(toma)
    x = x / max(1e-9, np.abs(x).max()) * 0.89
    activo = []
    pre, post = int(0.04 * SR), int(0.08 * SR)
    if una_toma is not None:
        tramos = [(0, len(x))]; ens = [una_toma]
    else:
        frases = tl["voz"]["frases"]; tramos = tramos_de_voz(x, len(frases))
        if tramos is None:
            print("No encontré", len(frases), "pausas en la toma: la pego entera desde", frases[0]["en"])
            tramos = [(0, len(x))]; ens = [frases[0]["en"]]; pre = 0
        else:
            ens = [f["en"] for f in frases]
    for (a, b), en in zip(tramos, ens):
        seg = x[max(0, a - pre):min(len(x), b + post)].copy()
        f = min(len(seg) // 4, int(0.015 * SR)); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
        i = int(en * SR) - (a - max(0, a - pre))
        n = min(len(seg), len(voz) - i)
        if i < 0 or n <= 0:
            continue
        voz[i:i + n] += seg[:n]; activo.append((i / SR, (i + n) / SR))
        print(f"  voz {i / SR:5.2f} – {(i + n) / SR:5.2f} s")
    if activo and activo[-1][1] > D - 0.3:
        print("AVISO: la voz termina en", round(activo[-1][1], 2), "s; subí 'duracion' en timeline.json.")
    return voz, activo


def envolvente_duck(n, tramos, db, rampa=0.12):
    g = np.ones(n); lvl = 10 ** (db / 20); r = int(rampa * SR)
    for a, b in tramos:
        i0, i1 = int(a * SR), int(b * SR)
        g[i0:i1] = np.minimum(g[i0:i1], lvl)
        if i0 > 0:
            k0 = max(0, i0 - r); g[k0:i0] = np.minimum(g[k0:i0], np.linspace(1, lvl, i0 - k0))
        k1 = min(n, i1 + r); g[i1:k1] = np.minimum(g[i1:k1], np.linspace(lvl, 1, k1 - i1))
    return g


def cues_chiptune(tl):
    """Música propia + tic de máquina de escribir + pop del cierre + grillos de verano."""
    sfx = []; cps = tl["tipeo_cps"]
    for bloque in tl["textos"]:
        for ln in bloque["lineas"]:
            d = ln.get("desde", bloque["desde"]); n = len(ln["texto"].replace(" ", ""))
            sfx.append({"t": d, "s": "tap", "pitch": 1.6, "n": (n + 1) // 2, "every": 2 / cps["titulos"], "gain": 0.35})
    ci = tl["cierre"]
    sfx.append({"t": ci["desde"], "s": "pop", "pitch": 1.2, "gain": 0.9})
    sfx.append({"t": ci["desde"] + 2 / tl["fps"], "s": "sparkle", "gain": 0.5})
    for ln in ci["lineas"]:
        if "texto" in ln:
            n = len(ln["texto"].replace(" ", ""))
            sfx.append({"t": ln["desde"], "s": "tap", "pitch": 1.9, "n": (n + 3) // 4, "every": 4 / cps["cierre"], "gain": 0.25})
    D = tl["duracion"]
    musica = {"bpm": 120, "start": 0.0,
              "melody": [[7, 1], [4, 1], [7, 1], [12, 1],  [9, 1], [7, 1], [4, 2],
                         [5, 1], [9, 1], [12, 1], [9, 1],  [7, 1], [11, 1], [14, 2]],
              "chords": [0, 9, 5, 7],
              "duck": [[1.95, 2.6, 0.45], [7.25, 8.4, 0.45]],
              "end_chord": {"t": ci["desde"], "notes": [0, 4, 7, 12]},
              "fade_out": [D - 0.9, D]}
    return {"duration": D, "sfx": sfx, "music": musica,
            "ambience": [{"type": "cicadas", "from": 0, "to": D, "level": 0.12}]}


def armar_audio(tl, salida, voz_cfg):
    D = tl["duracion"]; n = int(D * SR); mz = tl["mezcla"]
    cues = cues_chiptune(tl); cpath = os.path.join(salida, "cues.json")
    json.dump(cues, open(cpath, "w"), indent=1)
    subprocess.run([sys.executable, os.path.join(AQUI, "chiptune.py"), cpath, os.path.join(salida, "chip")], check=True)

    def pista(p):
        x = leer_wav(p); y = np.zeros(n); y[:min(n, len(x))] = x[:n]; return y

    base = pista(ruta(tl["base"]["archivo"]))
    c = int(tl["base"]["corte"] * SR); fo = int(0.25 * SR)
    base[c - fo:c] *= np.linspace(1, 0, fo); base[c:] = 0
    fondo = (base * mz["video"] + pista(os.path.join(salida, "chip/music.wav")) * mz["musica"]
             + pista(os.path.join(salida, "chip/sfx.wav")) * mz["efectos"]
             + pista(os.path.join(salida, "chip/ambience.wav")) * mz["ambiente"])
    voz = np.zeros(n)
    if voz_cfg:
        voz, act = colocar_voz(tl, *voz_cfg)
        fondo = fondo * envolvente_duck(n, act, tl["voz"]["bajar_fondo_db"])
        voz = voz * mz["voz"]
    x = fondo + voz
    x = x / max(1e-9, np.abs(x).max()) * 0.89          # pico a -1 dBFS; la sonoridad final se ajusta en ffmpeg
    return x


# ---------------------------------------------------------------- video

def armar(tl, salida, nombre, voz_cfg):
    os.makedirs(salida, exist_ok=True)
    ttf = fuente_ttf(salida); capa = Capa(tl, ttf)
    fps, D = tl["fps"], tl["duracion"]; N = int(round(D * fps))
    corte = int(tl["base"]["corte"] * fps)          # último cuadro del video base que se usa
    wav = os.path.join(salida, nombre + ".wav")
    escribir_wav(wav, armar_audio(tl, salida, voz_cfg))

    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", ruta(tl["base"]["archivo"]),
                            "-vf", f"fps={fps},scale={W}:{H}:flags=lanczos", "-frames:v", str(corte + 1),
                            "-f", "rawvideo", "-pix_fmt", "rgba", "-"], stdout=subprocess.PIPE)
    mp4 = os.path.join(salida, nombre + ".mp4")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}",
                            "-r", str(fps), "-i", "-", "-i", wav,
                            "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.84:level=false",
                            "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", "17",
                            "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k",
                            "-ar", "48000", "-shortest", mp4], stdin=subprocess.PIPE)
    ultimo = None
    for i in range(N):
        if i <= corte:
            buf = dec.stdout.read(W * H * 4)
            if len(buf) == W * H * 4:
                ultimo = Image.frombuffer("RGBA", (W, H), buf, "raw", "RGBA", 0, 1).copy()
        cuadro = ultimo.copy(); cuadro.alpha_composite(capa.cuadro(i / fps))
        enc.stdin.write(cuadro.tobytes())
    enc.stdin.close(); enc.wait(); dec.wait()
    print("listo ->", mp4)
    return mp4


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sin-voz", action="store_true")
    ap.add_argument("--voz", help="toma de voz (wav/mp3/m4a) con la frase completa")
    ap.add_argument("--una-toma", type=float, help="pegar la toma entera desde este segundo, sin cortar")
    ap.add_argument("--salida", default=os.path.join(AQUI, "salida"))
    ap.add_argument("--nombre")
    ap.add_argument("--snapshots", help="lista de segundos separados por coma: solo exporta PNG de esos cuadros")
    a = ap.parse_args()
    tl = json.load(open(os.path.join(AQUI, "timeline.json")))
    sys.path.insert(0, os.path.dirname(AQUI))
    from revisar_reglas import revisar_timeline          # regla: nunca el teléfono en un reel
    errores = revisar_timeline(tl)
    if errores:
        sys.exit("No se exporta: hay un número de teléfono en el reel.\n  " + "\n  ".join(errores))
    if not os.path.exists(ruta(tl["base"]["archivo"])):
        sys.exit("Falta el video base en " + ruta(tl["base"]["archivo"]) + " (bajalo de Drive, ver EDICION.md).")
    if a.snapshots:
        os.makedirs(a.salida, exist_ok=True); capa = Capa(tl, fuente_ttf(a.salida))
        for s in a.snapshots.split(","):
            t = float(s); tb = min(t, tl["base"]["corte"])
            png = os.path.join(a.salida, f"snap-{t:05.2f}.png")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(tb), "-i", ruta(tl["base"]["archivo"]), "-frames:v", "1",
                            "-vf", f"scale={W}:{H}:flags=lanczos", png], check=True)
            im = Image.open(png).convert("RGBA"); im.alpha_composite(capa.cuadro(t)); im.save(png)
            print(png)
        return
    if a.sin_voz:
        voz_cfg, nombre = None, a.nombre or "huevito-sin-voz"
    else:
        voz_cfg = (ruta(a.voz or tl["voz"]["toma"]), a.una_toma)
        nombre = a.nombre or "huevito-con-voz"
    armar(tl, a.salida, nombre, voz_cfg)


if __name__ == "__main__":
    main()
