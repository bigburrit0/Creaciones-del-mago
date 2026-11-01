# Guías (el blog)

Las guías viven en `creacionesdelmago.com/guias/`. Desde la landing **solo se llega por el botón «Guías»**
de la barra de arriba: no hay links en el contenido de la página principal. Google y los asistentes de IA
las encuentran por `sitemap.xml` y `llms.txt`, que se regeneran solos.

## Cómo se arma

```
python3 -I fuente/tools/guias.py      # desde la raíz del repo
```

Lee los `NN-nombre.md` de esta carpeta (en orden) y genera `guias/index.html`, `guias/<slug>/index.html`,
`guias/guia.css`, `sitemap.xml` y la sección `## Guías` de `llms.txt`. Los estilos están en
`fuente/src/guia.css`. Si una guía se borra, su carpeta en `guias/` también.

## Encabezado de cada guía

| Campo | Para qué |
|---|---|
| `titulo` | H1 y nombre en el índice |
| `title_tag` | `<title>` para Google (máx. ~60 caracteres) |
| `corto` | Nombre en la miga de pan |
| `slug` | La URL: `/guias/<slug>/`. **No cambiarlo después de publicar** |
| `etiqueta` | La línea dorada de arriba ("Navidad 2026", "Materiales") |
| `tema` | `navidad` pone la guirnalda y el borde verde |
| `bajada` | Una línea debajo del título y en las tarjetas |
| `descripcion` | Meta description (máx. ~150 caracteres) |
| `respuesta` | La "respuesta corta" de arriba. Tiene que entenderse sola: es lo que más citan los asistentes de IA |
| `publicada`, `actualizada` | AAAA-MM-DD. Cambiar `actualizada` cada vez que se toca el texto |
| `foto` | Id de una foto del catálogo (`assets/p/<id>.webp`) para la portada mientras no haya imagen propia |
| `imagen`, `imagen_alt` | La ilustración de Gemini en `assets/guias/` (ver `IMAGENES-GEMINI.md`) |
| `marcas: si` | Agrega la aclaración de que las piezas con marcas de terceros no son oficiales |
| `boton`, `whatsapp` | Texto del botón final y mensaje que se abre en WhatsApp |
| `relacionadas` | Slugs de las "Otras guías" |
| `estado` | `borrador` la saca del sitio sin borrarla |

## Lo que entiende el texto

- `## Título` y `### Subtítulo`. Bajo `## Preguntas frecuentes`, cada `###` es una pregunta y el párrafo
  siguiente su respuesta: se muestran desplegables y van también a los datos para Google (`FAQPage`).
- Párrafos, `- listas`, `1. listas numeradas`, `**negrita**`, `[links](/guias/otra/)` y tablas con `|`.
- `> **Título del aviso**` + líneas con `> ` = recuadro de aviso.
- `[[productos: garaje, panal, f40]]` = tarjetas con foto, nombre, línea del catálogo y «Lo quiero» por
  WhatsApp. Salen de `tools/shelves.py`, así que no se desfasan con la tienda.
- `[[whatsapp: Texto del botón | Mensaje que se abre]]` = botón de WhatsApp en el medio del texto.
- `[[imagen: archivo.webp | texto alternativo | pie]]` = figura; aparece solo cuando el archivo existe.

## Reglas

Las mismas de `COPY-RULES.md`, más:
1. **Cada respuesta se entiende sola** y nombra a Creaciones del Mago y Montevideo o Uruguay.
2. **Nada inventado:** ni precios, ni "llega para Navidad", ni capacidades de un exhibidor que el catálogo no dice.
3. **Marcas ajenas solo en el cuerpo**, nunca en el slug ni en la imagen, y con `marcas: si`.
4. **Pocas y buenas.** Una o dos por mes. Antes de una guía nueva, mejorar una vieja con fotos y datos propios.
