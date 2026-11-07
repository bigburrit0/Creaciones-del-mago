# Fuente de la web

Acá está lo que arma `index.html`. No hace falta para que la web funcione: GitHub Pages sirve el `index.html` de la raíz.

- `src/index.tpl.html`, `src/page.css`, `src/page.js`: la plantilla, los estilos y la interacción.
- `tools/catalog.py`: las categorías, los textos de cada producto y las fotos extra de la galería (`FOTOS`). Para cambiar un texto o agregar un producto, se edita acá. (`tools/shelves.py` es una copia vieja que ya no se usa.)
- `tools/build.py`: junta todo en un solo `index.html`. Desde la raíz del repo: `python3 -I fuente/tools/build.py` (escribe el `index.html` de la raíz). Si la carpeta `fuente/` tiene su propio `assets/`, lo escribe ahí.
- `tools/photos.py` e `imgs.py`: recortan las fotos a cuadrado (600 px) y hacen la versión pixelada de 32 px. Las fotos de celular (marca "m") se retocan solas; si hay una versión editada con IA en `fotos/ia/`, se usa esa. `python3 -I fuente/tools/imgs.py medieval vikingos` rehace solo esas.
- `fotos/vendidos/`: los originales de las fotos propias de vendidos. `fotos/IMAGENES-ANTIGRAVITY.md`: qué le toca a la IA y con qué reglas.
- `INVESTIGACION-CATALOGO-LITE.md`: la investigación del catálogo lite (v10) y qué se hizo.
- `COPY-RULES.md`: las reglas de texto. `BRIEF.md`: las decisiones de diseño.

Guías (blog): `guias/` en la raíz se genera con `python3 -I fuente/tools/guias.py` desde los textos de `fuente/guias/`. Ver `fuente/guias/LEEME.md`. Ese script también regenera `sitemap.xml` y la sección «Guías» de `llms.txt`.

Extras en la raíz del sitio (`robots.txt` se edita a mano; `sitemap.xml` y la sección «Guías» de `llms.txt` los regenera `guias.py`): `robots.txt`, `sitemap.xml`, `llms.txt`. Si cambian los datos (tamaño, materiales, zona, teléfono), actualizarlos junto con `FAQ` en `tools/build.py`. El usuario de Instagram está en `IG_URL` e `IG_HANDLE` (arriba de `tools/build.py`).
