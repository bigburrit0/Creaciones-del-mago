"""Arma estudio-reels.html (página para producir los reels) desde los .md de esta carpeta.

Uso, desde la raíz del repo: python3 -I fuente/campanas/reels-10s/armar_estudio.py
"""
import base64, html, json, re, sys
sys.dont_write_bytecode = True
from pathlib import Path

here = Path(__file__).resolve().parent
sys.path.insert(0, str(here))
from revisar_reglas import revisar_todo  # regla: nunca el teléfono en un reel
if revisar_todo():
    sys.exit("No se arma el estudio: hay un número de teléfono en un reel. Correr revisar_reglas.py para ver dónde.")
repo = here.parents[2]
out = here / "estudio-reels.html"
d = repo / "fuente/campanas/reels-10s"
FILES = [
    ("huevito", "01-huevito-mascota-virtual.md", "assets/p/hamster-px.png", "Mascota virtual"),
    ("continue", "02-continue-manija-del-termo.md", None, "Continue? 9, 8, 7"),
    ("rambla", "03-carrera-por-la-rambla.md", "assets/p/fiat-px.png", "Carreras Mode 7"),
    ("huerta", "04-la-huerta-de-los-pajaros.md", "assets/p/casita-px.png", "Simulador de granja"),
]

def b64(p, mime):
    return f"data:{mime};base64," + base64.b64encode((repo / p).read_bytes()).decode()

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    return s

def join_lines(lines):
    return " ".join(l.strip() for l in lines if l.strip())

def section(text, start, end_pats):
    i = text.index(start)
    rest = text[i + len(start):]
    j = len(rest)
    for p in end_pats:
        k = rest.find(p)
        if k != -1: j = min(j, k)
    return rest[:j]

def blockquote(s):
    return join_lines(l.lstrip("> ") for l in s.splitlines() if l.startswith(">"))

def bullets(s):
    items, cur = [], None
    for l in s.splitlines():
        if l.startswith("- "):
            if cur is not None: items.append(cur)
            cur = l[2:].strip()
        elif cur is not None and l.startswith("  ") and l.strip():
            cur += " " + l.strip()
        elif cur is not None and not l.strip():
            pass
    if cur is not None: items.append(cur)
    return items

def code_blocks(s):
    return re.findall(r"```\n(.*?)\n```", s, re.S)

data = []
for slug, fn, thumb, genre in FILES:
    t = (d / fn).read_text()
    title = t.splitlines()[0].lstrip("# ").strip()
    name = re.search(r"«([^»]+)»", title).group(1)
    head = t.split("## PASO 1")[0]
    summary = join_lines(head.split("**Resumen:**")[1].split("\n\n")[0].splitlines())
    paras = [p for p in head.split("\n\n")[2:] if p.strip() and not p.startswith("---")]
    extra = [join_lines(p.splitlines()) for p in paras]

    p1 = section(t, "## PASO 1", ["## PASO 2"])
    tip = blockquote(p1.split("###")[0])
    images = []
    for m in re.finditer(r"### Imagen (\d) · ([^·\n]+) · ([^\n]+)\n\n```\n(.*?)\n```", p1, re.S):
        images.append({"n": m.group(1), "t": m.group(2).strip(), "title": m.group(3).strip(), "prompt": m.group(4)})
    review = join_lines(p1.split("**Antes de pasar al video, revisá:**")[1].split("\n\n")[0].splitlines())

    p2 = section(t, "## PASO 2", ["## Después"])
    video = code_blocks(p2)[0]
    setup = join_lines(p2.split("\n\n")[1].splitlines())
    fb_part = p2.split("**Si tu herramienta no acepta 4 imágenes:**")[1]
    fb_codes = code_blocks(fb_part)
    fallbacks = []
    for b in bullets(re.sub(r"```\n.*?\n```", "", fb_part, flags=re.S)):
        fallbacks.append(b)

    rows = []
    g = section(t, "### Guion", ["**Voz en off"])
    for l in g.splitlines():
        if l.startswith("| ") and not l.startswith("| Tiempo") and not l.startswith("|---"):
            c = [x.strip() for x in l.strip("|").split("|")]
            rows.append(c)
    voz = blockquote(section(t, "**Voz en off completa**", ["### Texto del post"]))
    post = blockquote(section(t, "### Texto del post", ["**Otros cierres"]))
    cierres = []
    for b in bullets(section(t, "**Otros cierres", ["### Edición"])):
        m = re.match(r"\*\*([^*]+):\*\* `([^`]+)` · «(.+)»", b)
        cierres.append({"name": m.group(1), "text": m.group(2), "vo": m.group(3)})
    edicion = bullets(section(t, "### Edición", ["\n## ", "\x00"]))

    data.append({
        "slug": slug, "file": f"fuente/campanas/reels-10s/{fn}", "name": name, "title": title,
        "genre": genre, "summary": inline(summary[:1].upper() + summary[1:]), "extra": [inline(x) for x in extra],
        "thumb": b64(thumb, "image/png") if thumb else None,
        "tip": inline(tip), "images": [{**i, "title": inline(i["title"])} for i in images],
        "review": inline(review), "video": video, "setup": inline(setup),
        "fallbacks": [inline(f) for f in fallbacks], "fbcode": fb_codes,
        "rows": [[inline(c) for c in r] for r in rows], "voz": voz, "post": post,
        "cierres": cierres, "edicion": [inline(e) for e in edicion],
    })
    assert len(images) == 4, fn

tpl = (here / "estudio.tpl.html").read_text()
page = (tpl.replace("/*DATA*/", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
           .replace("FONT_BOLD", b64("fonts/MagoPixel-Bold.woff", "font/woff"))
           .replace("FONT_REG", b64("fonts/MagoPixel-Regular.woff", "font/woff"))
           .replace("GLIFO", b64("assets/px/glifo-oro.png", "image/png")))
out.write_text(page)
print("ok", len(page), [ (x["slug"], len(x["rows"]), len(x["cierres"]), len(x["fallbacks"]), len(x["fbcode"])) for x in data])
