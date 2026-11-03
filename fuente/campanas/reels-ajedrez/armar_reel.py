#!/usr/bin/env python3
"""Arma un reel vertical 1080x1920 a partir de un video de Gemini, una toma de voz y un JSON.

Uso:
    python3 fuente/campanas/reels-ajedrez/armar_reel.py fuente/campanas/reels-ajedrez/videos/01-torre.json

Hace todo con Pillow + ffmpeg:
  1. Pone el video en vertical: "bandas" (a todo el ancho, con bandas índigo arriba y abajo)
     o "recorte" (recorta el centro 9:16). Escala con vecino más cercano para no borronear el pixel art.
  2. Dibuja los textos en letra pixel (MagoPixel convertida a TTF): cajas de diálogo índigo con
     borde dorado, letra crema con contorno índigo, tipeo letra por letra, y el cierre con el glifo.
  3. Corta la toma de voz en frases y pone cada frase en su segundo (sin cambiarle la velocidad).
  4. Baja la música con ducking mientras habla la voz y normaliza a -14 LUFS (dos pasadas).
  5. Exporta H.264 + AAC, yuv420p, faststart. También una versión sin voz y la voz sola en la línea de tiempo.

Necesita: ffmpeg, Pillow y fontTools (pip install fonttools brotli).
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
W, H = 1080, 1920
INDIGO, INDIGO2, CREMA, DORADO, ROJO = "#1F1A3D", "#2A2350", "#F3E9D2", "#F2A93B", "#E2504C"


def ruta(p):
    return p if os.path.isabs(p) else os.path.join(RAIZ, p)


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode:
        sys.exit("Falló: " + " ".join(cmd) + "\n" + r.stderr[-2000:])
    return r


def fuente_ttf(woff, tmp):
    from fontTools.ttLib import TTFont
    f = TTFont(ruta(woff))
    f.flavor = None
    out = os.path.join(tmp, os.path.basename(woff).rsplit(".", 1)[0] + ".ttf")
    f.save(out)
    return out


# ---------------------------------------------------------------- dibujo de textos

class Pintor:
    """Dibuja con la grilla de la fuente: MagoPixel tiene 10 píxeles por em, así que con
    tamaño 60 cada píxel de la letra mide 6 px, y los bordes de las cajas usan esa misma unidad."""

    def __init__(self, ttf):
        self.ttf = ttf
        self._cache = {}

    def font(self, size):
        if size not in self._cache:
            self._cache[size] = ImageFont.truetype(self.ttf, size)
        return self._cache[size]

    def ancho(self, txt, size):
        return self.font(size).getlength(txt)

    def texto(self, d, xy, txt, size, color=CREMA, contorno=INDIGO):
        """Texto con contorno de 1 píxel de fuente en 8 direcciones (contorno duro, sin suavizado)."""
        u = max(1, size // 10)
        f = self.font(size)
        x, y = xy
        for dx in (-u, 0, u):
            for dy in (-u, 0, u):
                if dx or dy:
                    d.text((x + dx, y + dy), txt, font=f, fill=contorno)
        d.text((x, y), txt, font=f, fill=color)

    @staticmethod
    def caja(d, x0, y0, x1, y1, u, fondo=INDIGO2, borde=DORADO):
        """Caja de aventura gráfica: esquinas mordidas en escalón, borde dorado y filete índigo interior."""
        # sombra dura
        d.rectangle([x0 + u, y1, x1 + u, y1 + u], fill="#120F26")
        d.rectangle([x1, y0 + u, x1 + u, y1], fill="#120F26")
        # borde dorado con esquinas en escalón
        d.rectangle([x0 + u, y0, x1 - u, y1], fill=borde)
        d.rectangle([x0, y0 + u, x1, y1 - u], fill=borde)
        # filete oscuro + fondo
        d.rectangle([x0 + u, y0 + u, x1 - u, y1 - u], fill=INDIGO)
        d.rectangle([x0 + 2 * u, y0 + 2 * u, x1 - 2 * u, y1 - 2 * u], fill=fondo)

    @staticmethod
    def flecha(d, cx, y, u, color=DORADO):
        """Triangulito de "seguir" de las cajas de diálogo, en píxeles de fuente."""
        for i, w in enumerate((5, 3, 1)):
            x0 = cx - (w * u) // 2
            d.rectangle([x0, y + i * u, x0 + w * u - 1, y + (i + 1) * u - 1], fill=color)


def lineas_de(t):
    return t["texto"].split("\n")


def dibujar_caja_texto(p, d, t, tiempo, glifo=None):
    """Dibuja un bloque de texto (estilo "dialogo", "cierre" o "suelto") según cuánto lleva en pantalla."""
    size = t.get("tam", 60)
    tams = t.get("tams") or [size] * len(lineas_de(t))
    u = max(1, max(tams) // 10)
    lineas = lineas_de(t)
    gap = t.get("interlinea", 2 * u)
    pad_x, pad_y = t.get("pad_x", 5 * u), t.get("pad_y", 4 * u)
    # alto de línea: la letra va de 0 a 0,9 em (sin descendentes, ignoramos 0,3 em de abajo salvo g/j/p/q/y)
    altos = [int(s * (1.2 if re.search(r"[gjpqy,]", ln) else 0.9)) for ln, s in zip(lineas, tams)]
    anchos = [p.ancho(ln, s) for ln, s in zip(lineas, tams)]
    caja_w = int(max(anchos) + 2 * pad_x)
    caja_h = int(sum(altos) + gap * (len(lineas) - 1) + 2 * pad_y)
    cx = W // 2
    y_ancla = t["y"]  # y de arriba de la caja, o de abajo si "abajo": true
    y0 = y_ancla - caja_h if t.get("abajo") else y_ancla
    x0 = cx - caja_w // 2
    x0 -= x0 % u
    y0 -= y0 % u

    # entrada: la caja aparece en 3 cuadros (se estira de arriba a abajo en escalones)
    ent = tiempo - t["desde"]
    estilo = t.get("estilo", "dialogo")
    if estilo in ("dialogo", "cierre"):
        paso = min(1.0, ent / 0.1)
        h_vis = max(4 * u, int(caja_h * paso))
        yc0 = y0 + (caja_h - h_vis) // 2
        p.caja(d, x0, yc0, x0 + caja_w, yc0 + h_vis, u)
        if paso < 1:
            return (x0, y0, caja_w, caja_h)

    # tipeo letra por letra
    total = sum(len(ln) for ln in lineas)
    tipeo = t.get("tipeo", 0)
    mostrar = total if not tipeo else int(total * min(1.0, max(0.0, (ent - 0.1) / tipeo)))
    y = y0 + pad_y
    for ln, s, a, h in zip(lineas, tams, anchos, altos):
        vis = ln[:max(0, mostrar)]
        mostrar -= len(ln)
        x = cx - a / 2
        x -= x % u
        color = t.get("colores", {}).get(ln, CREMA)
        if vis:
            p.texto(d, (x, y), vis, s, color=color)
        y += h + gap
    # flecha de "seguir" que titila cuando terminó de tipear
    if estilo == "dialogo" and t.get("flecha", True) and mostrar >= 0 and tipeo and int(ent * 3) % 2 == 0:
        p.flecha(d, x0 + caja_w - 6 * u, y0 + caja_h + 2 * u, u)
    return (x0, y0, caja_w, caja_h)


def capa(p, cfg, tiempo, glifo):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for t in cfg["textos"]:
        if not (t["desde"] <= tiempo < t["hasta"]):
            continue
        x0, y0, cw, ch = dibujar_caja_texto(p, d, t, tiempo)
        if t.get("glifo") and glifo is not None and tiempo - t["desde"] >= 0.1:
            g = glifo
            gx = W // 2 - g.width // 2
            gy = y0 - g.height + t.get("glifo_solapa", 0)
            im.alpha_composite(g, (gx, gy))
    return im


# ---------------------------------------------------------------- video y audio

def filtro_video(cfg):
    fmt = cfg.get("formato", "bandas")
    fps = cfg.get("fps", 30)
    if fmt == "recorte":
        v = f"crop=ih*9/16:ih,scale={W}:{H}:flags=neighbor"
    else:
        vy = cfg.get("video_y")
        v = f"scale={W}:-2:flags=neighbor,pad={W}:{H}:0:{vy if vy is not None else '(oh-ih)/2'}:color={INDIGO}"
    return f"[0:v]{v},fps={fps},setsar=1,trim=0:{cfg['duracion']},setpts=PTS-STARTPTS[base]"


def voz_en_linea(cfg, tmp):
    """Corta la toma en frases y las pone en su segundo. Devuelve un WAV 48 kHz mono de duración exacta."""
    v = cfg.get("voz")
    if not v:
        return None
    out = os.path.join(tmp, "voz.wav")
    ins, fil, et = [], [], []
    for i, fr in enumerate(v["frases"]):
        ins += ["-i", ruta(v["toma"])]
        fil.append(f"[{i}:a]atrim={fr['corte'][0]}:{fr['corte'][1]},asetpts=PTS-STARTPTS,aresample=48000,"
                   f"afade=t=in:d=0.02,afade=t=out:st={fr['corte'][1]-fr['corte'][0]-0.03:.3f}:d=0.03,"
                   f"adelay={int(fr['en']*1000)}:all=1[f{i}]")
        et.append(f"[f{i}]")
    fil.append("".join(et) + f"amix=inputs={len(et)}:normalize=0,apad,atrim=0:{cfg['duracion']},"
               f"volume={v.get('ganancia_db', 0)}dB[v]")
    run(["ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", ";".join(fil), "-map", "[v]",
         "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", out])
    return out


def filtro_audio(cfg, con_voz, idx_voz):
    d = cfg["duracion"]
    musica = f"[0:a]aresample=48000,atrim=0:{d},apad,atrim=0:{d},volume={cfg.get('musica_db', 0)}dB"
    if not con_voz:
        return musica + "[mix]"
    duck = cfg.get("ducking", {})
    return (f"{musica}[mus];[{idx_voz}:a]aformat=channel_layouts=stereo,asplit=2[vz][sc];"
            f"[mus][sc]sidechaincompress=threshold={duck.get('umbral', 0.02)}:ratio={duck.get('ratio', 8)}:"
            f"attack={duck.get('ataque', 15)}:release={duck.get('suelta', 350)}:makeup=1[duck];"
            f"[duck][vz]amix=inputs=2:normalize=0:duration=first[mix]")


def loudnorm_2pasadas(fc, fc_audio, inputs, lufs):
    medir = fc_audio + f";[mix]loudnorm=I={lufs}:TP=-1.5:LRA=11:print_format=json[o]"
    r = run(["ffmpeg", "-y", "-v", "info", *inputs, "-filter_complex", medir, "-map", "[o]", "-f", "null", "-"])
    m = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    return (fc + f";[mix]loudnorm=I={lufs}:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
            f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,"
            f"aresample=48000[aout]")


def exportar(cfg, capas_dir, voz, salida, tmp):
    fps = cfg.get("fps", 30)
    inputs = ["-i", ruta(cfg["video"]), "-framerate", str(fps), "-i", os.path.join(capas_dir, "%04d.png")]
    idx_voz = None
    if voz:
        inputs += ["-i", voz]
        idx_voz = 2
    fa = filtro_audio(cfg, bool(voz), idx_voz)
    fc = filtro_video(cfg) + ";[base][1:v]overlay=0:0:format=auto,format=yuv420p[vout];" + fa
    fc = loudnorm_2pasadas(fc, fa, inputs, cfg.get("lufs", -14))
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", fc, "-map", "[vout]", "-map", "[aout]",
         "-t", str(cfg["duracion"]), "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high",
         "-pix_fmt", "yuv420p", "-r", str(fps), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
         "-movflags", "+faststart", ruta(salida)])
    print("listo:", salida)


def hoja_de_contacto(cfg, video, salida, tiempos):
    tmp = tempfile.mkdtemp()
    imgs = []
    for i, t in enumerate(tiempos):
        fn = os.path.join(tmp, f"{i}.png")
        run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", ruta(video), "-frames:v", "1", fn])
        imgs.append(Image.open(fn).convert("RGB"))
    esc = 0.4
    w, h = int(W * esc), int(H * esc)
    hoja = Image.new("RGB", (len(imgs) * (w + 20) + 20, h + 80), "#120F26")
    d = ImageDraw.Draw(hoja)
    for i, (im, t) in enumerate(zip(imgs, tiempos)):
        x = 20 + i * (w + 20)
        hoja.paste(im.resize((w, h), Image.LANCZOS), (x, 60))
        # zonas de botones de Instagram (250 px arriba, 420 px abajo), marcadas en rojo
        d.rectangle([x, 60, x + w - 1, 60 + int(250 * esc)], outline=ROJO, width=2)
        d.rectangle([x, 60 + h - int(420 * esc), x + w - 1, 60 + h - 1], outline=ROJO, width=2)
        d.text((x, 20), f"{t:.1f} s", fill=CREMA, font=ImageFont.load_default(28))
    hoja.save(ruta(salida))
    shutil.rmtree(tmp)
    print("hoja:", salida)


def main():
    cfg_path = sys.argv[1]
    cfg = json.load(open(ruta(cfg_path)))
    tmp = tempfile.mkdtemp(prefix="reel-")
    try:
        p = Pintor(fuente_ttf(cfg.get("fuente", "fonts/MagoPixel-Bold.woff"), tmp))
        glifo = None
        if cfg.get("glifo"):
            g = Image.open(ruta(cfg["glifo"])).convert("RGBA")
            k = cfg.get("glifo_escala", 2)
            glifo = g.resize((g.width * k, g.height * k), Image.NEAREST)
        fps, dur = cfg.get("fps", 30), cfg["duracion"]
        capas = os.path.join(tmp, "capas")
        os.makedirs(capas)
        for n in range(int(round(dur * fps))):
            capa(p, cfg, n / fps, glifo).save(os.path.join(capas, f"{n + 1:04d}.png"), optimize=False, compress_level=1)
        voz = voz_en_linea(cfg, tmp)
        sal = cfg["salidas"]
        if voz and sal.get("voz"):
            shutil.copy(voz, ruta(sal["voz"]))
            print("listo:", sal["voz"])
        if sal.get("sin_voz"):
            exportar(cfg, capas, None, sal["sin_voz"], tmp)
        exportar(cfg, capas, voz, sal["final"], tmp)
        if sal.get("hoja"):
            hoja_de_contacto(cfg, sal["final"], sal["hoja"], cfg.get("hoja_tiempos", [0.5, 3, 6, 9.5]))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
