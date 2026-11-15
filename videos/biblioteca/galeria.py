#!/usr/bin/env python3
"""Real product photos, one after another, in the reels (the owner, 15/11: "que vayan cambiando las imágenes de
productos ... para que las personas puedan ver realmente el producto y no únicamente los renders 3D").

  python3 galeria.py REEL            build REEL/galeria/ (a small HyperFrames page: no 3D), render it, and lay it over
                                     the reel's mp4 between t0 and t1 (the picture outside the window is untouched;
                                     the audio is copied, then rehacer_audio.py adds a soft swipe on each change)

REEL/galeria.json:
  {"t0": 14.8, "t1": 17.0, "title": "Así son<br>de verdad", "sub": "the site's line", "flash": true,
   "mp4s": ["REEL.mp4"],                                      (optional; the Christmas reel has two edits)
   "slides": [{"src": "perros-gatos", "label": "los perros", "zoom": 1.0, "fx": 0.5, "fy": 0.5}, ...]}
  src: a photo name. A studio photo in assets/estudio/<name>.(png|jpg|webp) is used when there is one (from the
  Gemini instructions in videos/ENTREGA/fotos_para_gemini/); otherwise the site's assets/p/<name>.webp.
  zoom > 1 shows a detail of the same photo around (fx, fy).
Slide changes are written to REEL/galeria_cambios.json for the swipes in musica.py.
"""
import json, os, re, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); VIDEOS = os.path.dirname(HERE); ROOT = os.path.dirname(VIDEOS)
reel = sys.argv[1]; R = os.path.join(VIDEOS, reel); cfg = json.load(open(os.path.join(R, "galeria.json")))
G = os.path.join(R, "galeria"); os.makedirs(os.path.join(G, "assets", "fotos"), exist_ok=True); os.makedirs(os.path.join(G, "assets", "fonts"), exist_ok=True)
F = "/opt/fonts/node_modules/@fontsource"
for src, dst in ((f"{F}/fredoka/files/fredoka-latin-700-normal.woff2", "fredoka-700.woff2"), (f"{F}/fredoka/files/fredoka-latin-600-normal.woff2", "fredoka-600.woff2"), (f"{F}/caveat/files/caveat-latin-700-normal.woff2", "caveat-700.woff2")):
    shutil.copy(src, os.path.join(G, "assets", "fonts", dst))
shutil.copy(os.path.join(VIDEOS, "papa-noel-en-ojotas", "hf", "assets", "gsap.min.js"), os.path.join(G, "gsap.min.js"))
for fn in ("hyperframes.json",): shutil.copy(os.path.join(VIDEOS, "la-gaviota", "hf3d", fn), os.path.join(G, fn))
json.dump({"id": reel + "-galeria", "name": reel + "-galeria", "createdAt": "2026-11-15T00:00:00.000Z"}, open(os.path.join(G, "meta.json"), "w"), indent=2)

def photo(name):
    for ext in ("png", "jpg", "jpeg", "webp"):
        p = os.path.join(ROOT, "assets", "estudio", f"{name}.{ext}")
        if os.path.exists(p): return p, True
    return os.path.join(ROOT, "assets", "p", f"{name}.webp"), False
slides, used = [], {}
for s in cfg["slides"]:
    if s.get("zoom", 1) > 1:                                    # a detail crop gives way to a NEW studio photo of the product (name-2, name-3...)
        k = used.get(s["src"], 1) + 1; extra = photo(f'{s["src"]}-{k}')
        if extra[1]: used[s["src"]] = k; s = dict(s, src=f'{s["src"]}-{k}', zoom=1.0, fx=0.5, fy=0.5)
    p, studio = photo(s["src"]); dst = os.path.basename(p); shutil.copy(p, os.path.join(G, "assets", "fotos", dst))
    slides.append(dict(s, file="assets/fotos/" + dst, studio=studio))
t0, t1 = cfg["t0"], cfg["t1"]; D = round(t1 - t0, 3); n = len(slides)
first = min(0.75, D / n * 1.25); rest = (D - first) / max(1, n - 1)                 # the first photo stays a little longer
starts = [0.0] + [round(first + k * rest, 3) for k in range(n - 1)]
json.dump({"t0": t0, "changes": [round(t0 + s, 3) for s in starts[1:]]}, open(os.path.join(R, "galeria_cambios.json"), "w"))

html = """<!doctype html>
<html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="gsap.min.js"></script>
<script>window.__timelines = window.__timelines || {}; window.__draw = null;
const tl = gsap.timeline({ paused: true }); tl.to({}, { duration: %(D)s, ease: "none", onUpdate: () => window.__draw && window.__draw(tl.time()) }); window.__timelines["main"] = tl;</script>
<style>
@font-face { font-family: "Fredoka"; src: url("assets/fonts/fredoka-700.woff2") format("woff2"); font-weight: 700; }
@font-face { font-family: "Fredoka"; src: url("assets/fonts/fredoka-600.woff2") format("woff2"); font-weight: 600; }
@font-face { font-family: "Caveat"; src: url("assets/fonts/caveat-700.woff2") format("woff2"); font-weight: 700; }
html, body { margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #150A34; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: radial-gradient(ellipse at 50%% 45%%, #3A2A6E 0%%, #150A34 78%%); }
.tt { position: absolute; left: 0; right: 0; top: 250px; text-align: center; font: 700 96px/1 "Fredoka", sans-serif; color: #F2C14E; -webkit-text-stroke: 12px #150A34; paint-order: stroke fill; text-shadow: 0 10px 0 rgba(0,0,0,0.35); }
.st { position: absolute; left: 60px; right: 60px; top: 1500px; text-align: center; font: 600 44px/1.25 "Fredoka", sans-serif; color: #FFF6E5; letter-spacing: 1px; }
.card { position: absolute; left: 110px; top: 480px; width: 860px; padding: 20px 20px 0; background: #FFFDF6; border-radius: 22px; box-shadow: 0 18px 0 rgba(0,0,0,0.3); transform-origin: 50%% 60%%; will-change: transform; }
.win { width: 820px; height: 820px; overflow: hidden; border-radius: 12px; background: #fff; }
.win img { width: 820px; height: 820px; object-fit: cover; display: block; transform-origin: 50%% 50%%; }
.lab { font: 700 60px/1 "Caveat", cursive; color: #24306B; text-align: center; padding: 14px 0 18px; }
#dots { position: absolute; left: 0; right: 0; top: 1418px; text-align: center; }
#dots span { display: inline-block; width: 20px; height: 20px; border-radius: 10px; margin: 0 9px; background: rgba(255,246,229,0.35); }
#dots span.on { background: #F2C14E; }
#flash { position: absolute; inset: 0; background: #FFFDF2; opacity: 0; }
</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="%(D)s" data-width="1080" data-height="1920">
<div class="tt">%(title)s</div>
%(cards)s
<div id="dots">%(dots)s</div>
<div class="st">%(sub)s</div>
<div id="flash"></div>
</div>
<script>
const S = %(slides)s, ST = %(starts)s, D = %(D)s, FLASH = %(flash)s;
const cards = [...document.querySelectorAll(".card")], imgs = cards.map((c) => c.querySelector("img")), dots = [...document.querySelectorAll("#dots span")];
const ease = (x) => 1 - Math.pow(1 - Math.min(1, Math.max(0, x)), 3), TR = 0.18;
function draw(t) {
  let k = 0; for (let i = 0; i < ST.length; i++) if (t >= ST[i]) k = i;
  cards.forEach((c, i) => {
    const end = i + 1 < ST.length ? ST[i + 1] : D + 1, a = ease((t - ST[i]) / TR), out = i + 1 < ST.length ? ease((t - ST[i + 1]) / TR) : 0;
    const vis = t >= ST[i] && (i + 1 >= ST.length || t < ST[i + 1] + TR);
    c.style.visibility = vis ? "visible" : "hidden"; if (!vis) return;
    const rot = (i %% 2 ? 2.5 : -2.5);
    const x = i === 0 && t < TR ? 0 : (1 - a) * 1150 - out * 1150, r = (1 - a) * (rot + 7) + rot * (1 - out) - out * 9, sc = (i === 0 ? 0.85 + 0.15 * ease(t / 0.3) : 1);
    c.style.transform = `translateX(${x.toFixed(1)}px) rotate(${r.toFixed(2)}deg) scale(${sc.toFixed(3)})`; c.style.zIndex = String(10 + i);
    const s = S[i], u = Math.min(1, Math.max(0, (t - ST[i]) / (end - ST[i]))), z = s.zoom * (1 + 0.06 * u);
    imgs[i].style.transformOrigin = `${(s.fx * 100).toFixed(1)}%% ${(s.fy * 100).toFixed(1)}%%`; imgs[i].style.transform = `scale(${z.toFixed(4)})`;
  });
  dots.forEach((d, i) => d.classList.toggle("on", i === k));
  document.getElementById("flash").style.opacity = FLASH ? Math.max(0, 0.9 * (1 - t / 0.12)).toFixed(3) : "0";
}
window.__draw = draw; window.addEventListener("hf-seek", (e) => draw(e.detail.time)); draw(0);
</script></body></html>
""" % dict(D=D, title=cfg["title"], sub=cfg.get("sub", ""), flash="true" if cfg.get("flash", True) else "false",
           cards="\n".join(f'<div class="card"><div class="win"><img src="{s["file"]}" alt=""></div><div class="lab">{s["label"]}</div></div>' for s in slides),
           dots="".join("<span></span>" for _ in slides),
           slides=json.dumps([{"zoom": s.get("zoom", 1.0), "fx": s.get("fx", 0.5), "fy": s.get("fy", 0.5)} for s in slides]), starts=json.dumps(starts))
open(os.path.join(G, "index.html"), "w", encoding="utf-8").write(html)
if "--no-render" in sys.argv: print("page only ->", G); sys.exit()
clip = os.path.join(R, "galeria.mp4")
r = subprocess.run(["npx", "hyperframes", "render", "--fps", "60", "--workers", "2", "-o", clip], cwd=G, capture_output=True, text=True)
if r.returncode: print(r.stdout[-1500:], r.stderr[-1500:]); sys.exit(1)
for mp4 in cfg.get("mp4s", [reel + ".mp4"]):
    src = os.path.join(R, mp4); orig = os.path.join(R, mp4.replace(".mp4", "_sin_galeria.mp4"))
    if not os.path.exists(orig): shutil.copy(src, orig)                             # keep the one-photo version (not versioned)
    out = src + ".tmp.mp4"
    fc = f"[1:v]setpts=PTS-STARTPTS+{t0}/TB[g];[0:v][g]overlay=0:0:enable='between(t,{t0},{t1 - 0.001})'[v]"
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", orig, "-i", clip, "-filter_complex", fc, "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
                        "-pix_fmt", "yuv420p", "-r", "60", "-c:a", "copy", "-movflags", "+faststart", out], capture_output=True, text=True)
    if r.returncode: print(r.stderr[-1500:]); sys.exit(1)
    os.replace(out, src); print("gallery", t0, "->", t1, f"({n} photos, {sum(s['studio'] for s in slides)} studio) ->", src)
