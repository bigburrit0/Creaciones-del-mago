# Fuente de la web

Acá está lo que arma `index.html`. No hace falta para que la web funcione: GitHub Pages sirve el `index.html` de la raíz.

- `src/index.tpl.html`, `src/page.css`, `src/page.js`: la plantilla, los estilos y la interacción.
- `tools/shelves.py`: las categorías y los textos de cada producto. Para cambiar un texto o agregar un producto, se edita acá.
- `tools/build.py`: junta todo en un solo `index.html` (`python3 tools/build.py`, desde una carpeta que tenga también `assets/`, `fonts/`, `scrollcraft.css` y `scrollcraft.js`).
- `tools/photos.py` e `imgs.py`: recortan las fotos a cuadrado (600 px) y hacen la versión pixelada de 32 px.
- `COPY-RULES.md`: las reglas de texto. `BRIEF.md`: las decisiones de diseño.
