"""Builds index.html: real markup for every shelf and item, engine + page CSS/JS inlined.
Run from the build folder: python3 -I tools/build.py"""
import os, sys, html, json
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from catalog import SHELVES, icon_svg

WA = "https://wa.me/59892104419?text="
from urllib.parse import quote
def wa(text): return WA + quote(text, safe='')

GENERAL = "Hola, vi la web y te quiero consultar algo."
CUSTOM = "Hola, quiero una pieza a medida. Es esto:"
WA_ICON = ('<svg viewBox="0 0 12 12" class="pix" aria-hidden="true" shape-rendering="crispEdges"><path fill="currentColor" '
           'd="M2 1h8v1h1v6h-1v1H5v1H4v1H3V9H2V8H1V2h1zM3 4h1v1H3zm3 0h1v1H6zm3 0h1v1H9z"/></svg>')
BAG_ICON = ('<svg viewBox="0 0 12 12" aria-hidden="true" shape-rendering="crispEdges"><path fill="currentColor" '
            'd="M4 1h4v1h1v2h2v7H1V4h2V2h1zm1 1v2h2V2zM2 5v5h8V5z"/></svg>')
e = html.escape

def item_html(shelf, it):
    iid, name, fact = it[0], it[1], it[2]
    mine = shelf.get("mine") == "all" or iid in shelf.get("mine", ())
    tag = ''
    msg = it[3] if len(it) > 3 else (shelf.get("pre", "") + name)
    return (f'<article class="item" data-id="{iid}" data-name="{e(name)}" data-line="{e(msg)}"{" data-mine" if mine else ""}>'
            f'<button class="shot" type="button" aria-label="Ver {e(name)} más grande">'
            f'<img class="full" src="assets/p/{iid}.webp" width="600" height="600" alt="{e(name)} impreso en 3D" loading="lazy" decoding="async">'
            f'<img class="px pix" src="assets/p/{iid}-px.png" width="32" height="32" alt="" loading="lazy"><i class="line" aria-hidden="true"></i>{tag}</button>'
            f'<i class="plank" aria-hidden="true"></i>'
            f'<h4>{e(name)}</h4><p>{fact}</p>'
            f'<button class="pick" type="button" aria-pressed="false"><span>Lo quiero</span></button></article>')

def shop_html():
    tabs, panels = [], []
    for i, s in enumerate(SHELVES):
        name = s.get("name", s["tab"])
        tabs.append(f'<a class="shelf-tab" href="#estante-{s["id"]}" data-i="{i}" aria-label="{e(name)}, {len(s["items"])}">'
                    f'{icon_svg(s["icon"])}<span>{e(s["tab"])}</span><small>{len(s["items"])}</small></a>')
        items = ''.join(item_html(s, it) for it in s["items"])
        panels.append(f'<section class="shelf" id="estante-{s["id"]}" data-i="{i}" data-name="{e(name)}" aria-labelledby="h-{s["id"]}">'
                      f'<header class="shelf__head"><span class="shelf__badge">{icon_svg(s["icon"])}</span>'
                      f'<div><h3 id="h-{s["id"]}">{e(name)}</h3><p class="shelf__intro">{s["intro"]}</p></div></header>'
                      f'<div class="grid">{items}</div>'
                      f'<button class="shelf__all" type="button" aria-expanded="false" hidden>{icon_svg("down")}<span>Ver los {len(s["items"])}</span></button>'
                      f'</section>')
    return ('<nav class="shelves" id="categorias" aria-label="Categorías">' + ''.join(tabs)
            + f'<span class="menu-cursor" aria-hidden="true">{icon_svg("cursor")}</span></nav>'
            '<div class="shelf-now">'
            f'<button class="now-step" type="button" data-step="-1" aria-label="Categoría anterior">{icon_svg("left")}</button>'
            '<a class="now-name" href="#categorias"><span class="now-icon" aria-hidden="true"></span><span data-now></span></a>'
            f'<button class="now-step" type="button" data-step="1" aria-label="Categoría siguiente">{icon_svg("right")}</button>'
            '</div>'
            + ''.join(panels))

def read(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()

TEMPLATE = read('src/index.tpl.html')
out = (TEMPLATE
       .replace('<!--SHOP-->', shop_html())
       .replace('/*ENGINE_CSS*/', read('scrollcraft.css'))
       .replace('/*PAGE_CSS*/', read('src/page.css'))
       .replace('/*ENGINE_JS*/', read('scrollcraft.js'))
       .replace('/*PAGE_JS*/', read('src/page.js'))
       .replace('{{WA_GENERAL}}', e(wa(GENERAL)))
       .replace('{{WA_CUSTOM}}', e(wa(CUSTOM)))
       .replace('{{MSG_EMPTY}}', e(GENERAL))
       .replace('{{WA_ICON}}', WA_ICON)
       .replace('{{BAG_ICON}}', BAG_ICON)
       .replace('{{I_CHAT}}', icon_svg('chat')).replace('{{I_COIN}}', icon_svg('coin'))
       .replace('{{I_PRINTER}}', icon_svg('printer')).replace('{{I_BOX}}', icon_svg('box'))
       .replace('{{I_LEFT}}', icon_svg('left')).replace('{{I_RIGHT}}', icon_svg('right'))
       .replace('{{N_ITEMS}}', str(sum(len(s["items"]) for s in SHELVES))))
assert '{{' not in out, out[out.index('{{'):out.index('{{') + 40]
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(out)
print('index.html', len(out), 'bytes,', sum(len(s["items"]) for s in SHELVES), 'items')
