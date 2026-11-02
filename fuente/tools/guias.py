"""Builds the Guías section: /guias/index.html, one /guias/<slug>/index.html per guide,
/guias/guia.css, and regenerates sitemap.xml and the "## Guías" block of llms.txt.

Run from the repo root:  python3 -I fuente/tools/guias.py

Each guide is a text file in fuente/guias/*.md: a front matter between --- lines and a
small Markdown subset (see fuente/guias/LEEME.md). Product cards read the catalog in
tools/shelves.py, so a name or a line changes in one place only.
"""
import os, re, sys, html, json, shutil
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
FUENTE = os.path.dirname(HERE)
REPO = os.path.dirname(FUENTE)
sys.path.insert(0, HERE)
from catalog import SHELVES, icon_svg

SITE = "https://creacionesdelmago.com/"
WA_NUM = "59892104419"
PHONE = "092 104 419"
PHONE_INTL = "+598 92 104 419"
IG_URL = "https://www.instagram.com/creacionesdelmago/"
IG_HANDLE = "@creacionesdelmago"
SRC_DIR = os.path.join(FUENTE, "guias")
OUT_DIR = os.path.join(REPO, "guias")
IMG_DIR = os.path.join(REPO, "assets", "guias")   # Gemini images land here
e = html.escape
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]

def wa(text): return f"https://wa.me/{WA_NUM}?text=" + quote(text, safe='')
def fecha(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return f"{d} de {MESES[m - 1]} de {y}"

WA_ICON = ('<svg viewBox="0 0 12 12" class="pix" aria-hidden="true" shape-rendering="crispEdges"><path fill="currentColor" '
           'd="M2 1h8v1h1v6h-1v1H5v1H4v1H3V9H2V8H1V2h1zM3 4h1v1H3zm3 0h1v1H6zm3 0h1v1H9z"/></svg>')

# ---------------------------------------------------------------- catalog
PRODUCTS = {}
for s in SHELVES:
    for it in s["items"]:
        PRODUCTS.setdefault(it[0], {"id": it[0], "name": it[1], "fact": it[2], "shelf": s["id"], "shelf_name": s.get("name", s["tab"])})

# ---------------------------------------------------------------- parsing
def parse(path):
    raw = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    if not m: raise SystemExit(f"{path}: falta el encabezado entre ---")
    meta = {}
    for line in m.group(1).splitlines():
        if line.strip() and not line.lstrip().startswith("#"):
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
    for k in ("titulo", "slug", "descripcion", "publicada", "actualizada", "foto"):
        if k not in meta: raise SystemExit(f"{path}: falta «{k}» en el encabezado")
    meta["body"] = m.group(2)
    return meta

def inline(t):
    t = e(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    def link(m):
        href = m.group(2)
        ext = href.startswith("http") and not href.startswith(SITE)
        return f'<a href="{e(href)}"' + (' rel="noopener" target="_blank"' if ext else '') + f'>{m.group(1)}</a>'
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, t)

def slugify(t):
    t = t.lower()
    for a, b in zip("áéíóúüñ¿?¡!", "aeiouun    "): t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:60]

def product_card(pid, guide_title):
    p = PRODUCTS.get(pid)
    if not p: raise SystemExit(f"producto desconocido: {pid}")
    msg = f"Hola, vi la guía «{guide_title}». Me interesa: {p['name']}. ¿Me pasás precio y fecha?"
    return (f'<article class="card">'
            f'<img src="/assets/p/{pid}.webp" width="600" height="600" alt="{e(p["name"])}, impreso en 3D" loading="lazy" decoding="async">'
            f'<i class="plank" aria-hidden="true"></i>'
            f'<h4>{e(p["name"])}</h4><p>{inline(p["fact"])}</p>'
            f'<a class="card__wa" href="{e(wa(msg))}">{WA_ICON}<span>Lo quiero</span></a></article>')

def figure(spec):
    # [[imagen: archivo.webp | texto alternativo | pie]] ; rendered only once the file exists
    parts = [x.strip() for x in spec.split("|")]
    fname, alt = parts[0], parts[1] if len(parts) > 1 else ""
    cap = parts[2] if len(parts) > 2 else ""
    if not os.path.exists(os.path.join(IMG_DIR, fname)):
        return ""
    return (f'<figure class="fig"><img src="/assets/guias/{e(fname)}" alt="{e(alt)}" loading="lazy" decoding="async">'
            + (f'<figcaption>{inline(cap)}</figcaption>' if cap else '') + '</figure>')

def render(meta):
    """Markdown subset -> (html, toc, faq pairs)."""
    lines = meta["body"].strip("\n").split("\n")
    out, toc, faq = [], [], []
    i, in_faq = 0, False
    para = []
    def flush():
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>"); para.clear()
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            flush(); i += 1; continue
        if ln.startswith("## "):
            flush(); t = ln[3:].strip(); hid = slugify(t)
            in_faq = t.lower().startswith("preguntas frecuentes")
            toc.append((hid, t))
            out.append(f'<h2 id="{hid}">{inline(t)}</h2>'); i += 1; continue
        if ln.startswith("### "):
            flush(); q = ln[4:].strip(); i += 1
            if in_faq:
                ans = []
                while i < len(lines) and lines[i].strip() and not lines[i].startswith("#"):
                    ans.append(lines[i].strip()); i += 1
                a = " ".join(ans)
                faq.append((q, re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", a).replace("**", "")))
                out.append(f'<details><summary>{inline(q)}</summary><p>{inline(a)}</p></details>')
            else:
                out.append(f'<h3 id="{slugify(q)}">{inline(q)}</h3>')
            continue
        if ln.startswith("[[") and ln.endswith("]]"):
            flush(); kind, _, arg = ln[2:-2].partition(":"); kind = kind.strip(); arg = arg.strip()
            if kind == "productos":
                cards = "".join(product_card(x.strip(), meta["titulo"]) for x in arg.split(","))
                out.append(f'<div class="cards">{cards}</div>')
            elif kind == "imagen":
                out.append(figure(arg))
            elif kind == "whatsapp":
                label, _, msg = (x.strip() for x in arg.partition("|"))
                out.append(f'<p class="cta-inline"><a class="btn" href="{e(wa(msg))}">{WA_ICON}<span>{e(label)}</span></a></p>')
            else:
                raise SystemExit(f"bloque desconocido: {ln}")
            i += 1; continue
        if ln.startswith("> "):
            flush(); buf = []
            while i < len(lines) and lines[i].startswith("> "):
                buf.append(lines[i][2:].strip()); i += 1
            head, body = (buf[0], buf[1:]) if buf[0].startswith("**") and len(buf) > 1 else (None, buf)
            out.append('<aside class="note">' + (f'<p class="note__head">{inline(head)}</p>' if head else '')
                       + "".join(f"<p>{inline(b)}</p>" for b in body) + "</aside>")
            continue
        if re.match(r"^(- |\d+\. )", ln):
            flush(); ordered = not ln.startswith("- "); items = []
            while i < len(lines) and re.match(r"^(- |\d+\. )", lines[i]):
                items.append(re.sub(r"^(- |\d+\. )", "", lines[i]).strip()); i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
            continue
        if ln.startswith("|"):
            flush(); rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", c) for c in cells): rows.append(cells)
                i += 1
            head, body = rows[0], rows[1:]
            out.append('<div class="table"><table><thead><tr>' + "".join(f'<th scope="col">{inline(c)}</th>' for c in head)
                       + "</tr></thead><tbody>" + "".join("<tr>" + "".join(
                           (f'<th scope="row">{inline(c)}</th>' if j == 0 else f"<td>{inline(c)}</td>") for j, c in enumerate(r)) + "</tr>" for r in body)
                       + "</tbody></table></div>")
            continue
        para.append(ln.strip()); i += 1
    flush()
    return "\n".join(x for x in out if x), toc, faq

# ---------------------------------------------------------------- page shell
def hero_img(meta):
    g = meta.get("imagen")
    if g and os.path.exists(os.path.join(IMG_DIR, g)):
        return f"/assets/guias/{g}", True
    return f"/assets/p/{meta['foto']}.webp", False

def business():
    return {"@type": ["LocalBusiness", "ProfessionalService"], "@id": SITE + "#negocio", "name": "Creaciones del Mago",
            "url": SITE, "telephone": PHONE_INTL, "sameAs": [IG_URL], "image": SITE + "assets/px/og.png",
            "address": {"@type": "PostalAddress", "addressLocality": "Montevideo", "addressCountry": "UY"},
            "areaServed": [{"@type": "City", "name": "Montevideo"}, {"@type": "Country", "name": "Uruguay"}]}

def shell(*, title, description, canonical, og_image, body, jsonld, theme=""):
    data = json.dumps({"@context": "https://schema.org", "@graph": jsonld}, ensure_ascii=False, indent=1)
    return f"""<!doctype html>
<html lang="es-UY">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#1F1A3D">
<meta property="og:type" content="article">
<meta property="og:locale" content="es_UY">
<meta property="og:site_name" content="Creaciones del Mago">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="/assets/px/favicon.png">
<link rel="apple-touch-icon" href="/assets/px/apple-touch-icon.png">
<link rel="preload" href="/fonts/MagoPixel-Bold.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="/guias/guia.css">
<script type="application/ld+json">
{data}
</script>
</head>
<body class="{theme}">
<header class="top">
  <a class="top__mark" href="/"><img class="pix" src="/assets/px/glifo-linea.png" width="52" height="56" alt=""><span>Creaciones del Mago</span></a>
  <a class="top__link" href="/guias/">{icon_svg("libro")}<span>Guías</span></a>
  <a class="btn btn--sm" href="{e(wa("Hola, vi las guías y te quiero consultar algo."))}">{WA_ICON}<span>Escribime</span></a>
</header>
{body}
<footer class="foot">
  <p><b>Creaciones del Mago</b> · Impresión y diseño 3D en Montevideo, Uruguay.</p>
  <p>WhatsApp <a href="{e(wa("Hola, vi las guías y te quiero consultar algo."))}">{PHONE}</a> · Instagram <a href="{IG_URL}" rel="me noopener" target="_blank">{IG_HANDLE}</a> · <a href="/">Volver a la tienda</a></p>
</footer>
</body>
</html>
"""

def crumbs(items):
    vis = " <span aria-hidden=\"true\">›</span> ".join(
        (f'<a href="{u}">{e(n)}</a>' if u else f'<span aria-current="page">{e(n)}</span>') for n, u in items)
    ld = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": k + 1, "name": n, **({"item": SITE.rstrip("/") + u} if u else {})} for k, (n, u) in enumerate(items)]}
    return f'<nav class="crumbs" aria-label="Estás en">{vis}</nav>', ld

def guide_page(meta, others):
    body_html, toc, faq = render(meta)
    url = f"{SITE}guias/{meta['slug']}/"
    img, is_gemini = hero_img(meta)
    crumb_html, crumb_ld = crumbs([("Inicio", "/"), ("Guías", "/guias/"), (meta.get("corto", meta["titulo"]), None)])
    toc_html = ""
    if len(toc) > 2:
        toc_html = ('<nav class="toc" aria-label="En esta guía"><p class="label">En esta guía</p><ol>'
                    + "".join(f'<li><a href="#{h}">{inline(t)}</a></li>' for h, t in toc) + "</ol></nav>")
    rel = [o for o in others if o["slug"] in [x.strip() for x in meta.get("relacionadas", "").split(",")]] or others[:3]
    rel_html = "".join(f'<li><a href="/guias/{o["slug"]}/"><b>{e(o["titulo"])}</b><span>{e(o["bajada"])}</span></a></li>' for o in rel)
    brands = ('<p class="fine">Las piezas que llevan nombres de marcas, personajes o clubes son impresiones independientes, '
              'hechas a partir de modelos de diseñadores. No son productos oficiales ni tienen relación con esas marcas.</p>'
              if meta.get("marcas") == "si" else "")
    cta_msg = meta.get("whatsapp", f"Hola, vi la guía «{meta['titulo']}» y te quiero consultar algo.")
    body = f"""<main class="guide">
  <div class="hero{' hero--' + meta['tema'] if meta.get('tema') else ''}">
    <div class="wrap">
      {crumb_html}
      <p class="label">{e(meta.get("etiqueta", "Guía"))}</p>
      <h1>{inline(meta["titulo"])}</h1>
      <p class="hero__lead">{inline(meta["bajada"])}</p>
      <p class="meta">Actualizada el <time datetime="{meta['actualizada']}">{fecha(meta['actualizada'])}</time> · Por El Mago</p>
    </div>
    <figure class="hero__img{' is-photo' if not is_gemini else ''}"><img src="{img}" alt="{e(meta.get('imagen_alt', meta['titulo']))}" width="{2100 if is_gemini else 600}" height="{800 if is_gemini else 600}" fetchpriority="high"></figure>
  </div>
  <div class="wrap paper-wrap">
    <article class="paper">
      <div class="answer"><p class="label">Respuesta corta</p><p>{inline(meta["respuesta"])}</p></div>
      {toc_html}
      {body_html}
      {brands}
    </article>
    <aside class="end">
      <div class="end__cta">
        <p class="end__title">¿Te paso precio y fecha?</p>
        <p>Escribime por WhatsApp con lo que te gustó, una foto o una idea. Te contesto yo, sin compromiso.</p>
        <a class="btn" href="{e(wa(cta_msg))}">{WA_ICON}<span>{e(meta.get("boton", "Escribime por WhatsApp"))}</span></a>
      </div>
      <div class="end__more"><p class="label">Otras guías</p><ul class="more">{rel_html}</ul></div>
    </aside>
  </div>
</main>"""
    ld = [business(),
          {"@type": "BlogPosting", "@id": url + "#guia", "headline": meta["titulo"], "description": meta["descripcion"],
           "abstract": meta["respuesta"].replace("**", ""),
           "datePublished": meta["publicada"], "dateModified": meta["actualizada"], "inLanguage": "es-UY",
           "image": SITE.rstrip("/") + img, "url": url, "mainEntityOfPage": url,
           "author": {"@type": "Person", "name": "El Mago", "worksFor": {"@id": SITE + "#negocio"}}, "publisher": {"@id": SITE + "#negocio"},
           "isPartOf": {"@type": "Blog", "@id": SITE + "guias/#blog", "name": "Guías de Creaciones del Mago", "url": SITE + "guias/"},
           "about": [x.strip() for x in meta.get("temas", "").split(",") if x.strip()]},
          crumb_ld]
    if faq:
        ld.append({"@type": "FAQPage", "@id": url + "#preguntas", "inLanguage": "es-UY", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    return shell(title=meta.get("title_tag", meta["titulo"]) + " | Creaciones del Mago", description=meta["descripcion"],
                 canonical=url, og_image=SITE.rstrip("/") + img, body=body, jsonld=ld)

def index_page(guides):
    crumb_html, crumb_ld = crumbs([("Inicio", "/"), ("Guías", None)])
    cards = []
    for g in guides:
        img, _ = hero_img(g)
        cards.append(f'<li class="gcard{" gcard--" + g["tema"] if g.get("tema") else ""}"><a href="/guias/{g["slug"]}/">'
                     f'<img src="{img}" width="600" height="600" alt="" loading="lazy">'
                     f'<span class="label">{e(g.get("etiqueta", "Guía"))}</span>'
                     f'<b>{e(g["titulo"])}</b><span class="gcard__lead">{e(g["bajada"])}</span>'
                     f'<span class="gcard__go">Leer la guía {icon_svg("right")}</span></a></li>')
    body = f"""<main class="guide">
  <div class="hero hero--index">
    <div class="wrap">
      {crumb_html}
      <p class="label">Guías</p>
      <h1>Guías para regalar y pedir en 3D</h1>
      <p class="hero__lead">Lo que me preguntan por WhatsApp, contestado con calma: qué regalar, cómo elegir un ajedrez, qué material conviene y qué mandarme para pedir.</p>
    </div>
  </div>
  <div class="wrap">
    <ul class="gcards">{''.join(cards)}</ul>
  </div>
</main>"""
    url = SITE + "guias/"
    ld = [business(),
          {"@type": ["CollectionPage", "Blog"], "@id": url + "#blog", "name": "Guías de Creaciones del Mago", "url": url, "inLanguage": "es-UY",
           "description": "Guías de impresión 3D en Montevideo: regalos de Navidad, amigo invisible, exhibidores para autitos 1:64, ajedrez personalizado, medidas e historia del ajedrez, PLA o PETG y cómo pedir una pieza.",
           "publisher": {"@id": SITE + "#negocio"},
           "mainEntity": {"@type": "ItemList", "itemListElement": [
               {"@type": "ListItem", "position": k + 1, "url": f"{url}{g['slug']}/", "name": g["titulo"]} for k, g in enumerate(guides)]}},
          crumb_ld]
    return shell(title="Guías de impresión 3D en Montevideo: regalos y pedidos | Creaciones del Mago",
                 description="Qué regalar impreso en 3D esta Navidad, ajedrez personalizado, PLA o PETG, exhibidores para autitos 1:64 y qué mandar para pedir una pieza. Desde Montevideo.",
                 canonical=url, og_image=SITE + "assets/px/og.png", body=body, jsonld=ld)

# ---------------------------------------------------------------- sitemap + llms.txt
def write_sitemap(guides, today):
    urls = [(SITE, today, "monthly", "1.0"), (SITE + "guias/", today, "weekly", "0.8")]
    urls += [(f"{SITE}guias/{g['slug']}/", g["actualizada"], "monthly", "0.7") for g in guides]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, mod, freq, pri in urls:
        xml.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{mod}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{pri}</priority>\n  </url>")
    xml.append("</urlset>\n")
    open(os.path.join(REPO, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(xml))

def write_llms(guides):
    p = os.path.join(REPO, "llms.txt")
    txt = open(p, encoding="utf-8").read()
    txt = re.sub(r"\n## Guías\n.*?(?=\n## )", "", txt, flags=re.S)
    block = ("\n## Guías\n\n- [Todas las guías](" + SITE + "guias/): regalos impresos en 3D, ajedrez personalizado, materiales y cómo pedir, desde Montevideo.\n"
             + "".join(f"- [{g['titulo']}]({SITE}guias/{g['slug']}/): {g['respuesta'].replace('**', '')}\n" for g in guides))
    txt = txt.replace("\n## Catálogo", block + "\n## Catálogo", 1)
    open(p, "w", encoding="utf-8").write(txt)

def main():
    files = sorted(f for f in os.listdir(SRC_DIR) if f.endswith(".md") and f[0].isdigit())
    guides = [parse(os.path.join(SRC_DIR, f)) for f in files]
    guides = [g for g in guides if g.get("estado", "publicada") == "publicada"]
    if os.path.isdir(OUT_DIR):
        for d in os.listdir(OUT_DIR):
            full = os.path.join(OUT_DIR, d)
            if os.path.isdir(full) and d not in {g["slug"] for g in guides}: shutil.rmtree(full)
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copy(os.path.join(FUENTE, "src", "guia.css"), os.path.join(OUT_DIR, "guia.css"))
    for g in guides:
        d = os.path.join(OUT_DIR, g["slug"]); os.makedirs(d, exist_ok=True)
        page = guide_page(g, [o for o in guides if o is not g])
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page)
    open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8").write(index_page(guides))
    write_sitemap(guides, max(g["actualizada"] for g in guides))
    write_llms(guides)
    print(len(guides), "guías:", ", ".join(g["slug"] for g in guides))

if __name__ == "__main__":
    main()
