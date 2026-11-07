# BRIEF · Creaciones del Mago, v5 ("La tienda del Mago", texto humano)

v5 takes the v4 item-shop build (never published) and rewrites it around the
owner's message of 17/10/2026, plus a three-agent research pass on selling copy,
honest persuasion, and sounding human. Interview answers are verbatim where
quoted; anything else is **authored** under his request to use the skill "para
cambiar el rumbo de la página".

## The eight topics

1. **Vibe.** "minimalista, pixel art pero que muestre la información relevante".
   Reference medium: the item shop of a 16-bit RPG. *Authored, kept from v4.*
2. **Journey, in his words.** "me gustó la intro y la pirámide" (keep) ·
   "debería tener más referencia a las impresiones 3D" · "la parte capas por
   capas no me gustó" (no layer-by-layer act) · "hacer más enfoque en el
   catálogo pero definir bien las categorías. Muchas cosas son clickers, etc" ·
   "las descripciones suenan muy IA" · "que suene más humana y natural en ciertas
   cosas como el contactanos" · "que al final del día haga que las personas
   escriban por WhatsApp para hacer sus pedidos".
3. **Energy curve.** Calm night opening, straight into the catalog, the catalog
   is where the time goes, the close is quiet and practical. *Authored.*
4. **Feeling, stage by stage + the one moment.** See curve below.
5. **Something no other site does.** *Authored (v4):* the page writes your
   WhatsApp order as you pick things, like filling an inventory.
6. **Distance from premium-minimal.** Retro (16-bit), minimal in amount of text.
7. **One world or scenes.** Distinct scenes (title screen, shop, counter).
8. **Assets.** Logo glyph and pyramid sprites, his own photos (Pics) and the
   designers' photos (Proyecto 3D). No generation, no spend.

## Grammar

Item shop (gallery/catalog variant), unchanged from v4. Nav carries state (the
order counter). Hero: title screen, the glyph prints itself. Sequence: title
(pin) → shop (flow) → a medida (flow + reveal) → cómo pedir (flow) → counter
(pin, holds). Bans: layer-by-layer storytelling, kinetic headlines, invented
prices, stock, reviews or urgency.

## Feeling curve

```
1  Curiosity   night, pyramid, a toolhead prints the golden glyph
2  Appetite    the shop: 9 categories you can see at once, real names
3  Agency      "Lo quiero" drops a piece into your inventory   <- peak
4  Trust       made-to-order work, photos straight off the printer
5  Ease        four steps, short answers, nothing hidden
6  Resolve     the counter: your message already written, one button
```

**Peak:** "toqué 'lo quiero' en un par de cosas y abajo se me fue armando el
pedido, y el WhatsApp ya estaba escrito".

**Tell-someone sentence:** "es la página donde elegís cosas como en un
videojuego y te deja el WhatsApp escrito".

**Authored silence:** none.

## What changed from v4

- Categories: every category visible at once (desktop row, phone 3×3 grid),
  each shelf has a real name, a one-line intro and a "next shelf" button.
- Copy: rewritten from the research (see COPY-RULES.md).
- Title copy no longer fades out mid-pin (v4 left three frames of empty sky).
- Own photos marked item by item ("Foto mía") instead of a line per shelf.

## v6 (17/10/2026, segunda pasada)

Owner: "quita esto" (the workshop photo) · "más enfoque en el catálogo" · "que el
catálogo sea un poco más interactivo y que siga con el scroll" · "pensá en las
animaciones" · "que todo sea harmonioso, siguiendo la onda pixel art, con charm".

- Shelves are stacked and the scroll walks past them; the menu follows with an
  RPG cursor (desktop) or a sticky ◀ name ▶ line (phone).
- Each row of items stands on a pixel plank. One row per shelf on wide screens,
  two on smaller ones, then "Ver los N".
- Tapping a photo opens an RPG item window (prev/next, keyboard, swipe).
- "Lo quiero" throws a pixel thumbnail along an arc into the bag, then "+1".
- Rooms rise out of each other as rows of little stepped pyramids.
- "Cómo pedir" became four pixel-icon steps on a dotted path.
- Occasional shooting star; the small temple returns at the phone close.
- Workshop photo removed.

## v7 (1/11/2026, copy para vender y para que lo encuentren los LLM)

Owner: "puedo hacer casi todo" no vende la marca; hay que venderse mejor y que ChatGPT y
otros modelos encuentren la marca (ya llegaron clientes hablando con ChatGPT). "Precios
súper accesibles" se mantiene: se confirma cuando escriben. Hay Instagram con el mismo nombre.
Base: investigación de 20 perfiles (resultados con evidencia floja: casi todo por resúmenes de
búsqueda, ver nota al final), cruzada con las 5 propuestas de copy.

- Hero: "Precios súper accesibles" arriba (gancho), H1 "Imprimo en 3D en Montevideo. Mandame tu
  idea." (palabra clave + acción de poco esfuerzo), WhatsApp pasa a botón principal (en celular el
  secundario se oculta) y el catálogo queda segundo.
- "Casi cualquier cosa" sale de todos lados. Lo reemplaza un límite real (25 cm, PLA/PETG, 4
  colores) y la promesa de avisar antes si algo no se puede imprimir.
- "Ficha del taller" (en A medida): datos en líneas sueltas y citables (impresora, tamaño,
  material, colores, archivos, precio, plazo, zona, pedidos).
- Preguntas frecuentes: 12, cada respuesta se entiende sola; salen de `FAQ` en `tools/build.py`
  y se generan igual en el HTML visible y en el JSON-LD (`FAQPage`), así no se desfasan.
- Datos estructurados: `LocalBusiness` + `WebSite` + `FAQPage`, con `sameAs` a Instagram.
- Instagram: link en el hero, la ficha, el cierre y el pie. Constantes `IG_URL` e `IG_HANDLE`
  al principio de `tools/build.py`.
- Raíz: `robots.txt`, `sitemap.xml`, `llms.txt`. og:image y og:url con URL absoluta.
- Psicología usada sin inventar nada: ancla de precio con mecanismo (peso y tiempo), reversión
  del riesgo ("sin compromiso", "si no se puede, te aviso antes"), poco esfuerzo para el primer
  mensaje (una foto alcanza), esfuerzo visible ("más de un día de impresora"), prueba social real
  (Instagram y fotos propias). No hay reseñas, escasez ni urgencia inventadas.

Nota de evidencia: ningún informe pudo abrir páginas completas (dominios bloqueados) y la
búsqueda era solo de EE.UU. Lo más firme es que casi todos coinciden en cambiar la vaguedad por
datos concretos. Sin verificar: registro de la marca, licencias y marcas de terceros
(One Piece, Pokémon, Minecraft, Star Wars, clubes), arrepentimiento en compras a distancia.

## v8 (1/11/2026, guías para Google, los asistentes de IA y Navidad)

Dueño: un "blog" que ayude a aparecer en buscadores y en los LLM, con enfoque de Navidad y regalos, con su
propio botón y fuera del contenido de la landing.

- `/guias/`: cinco guías (regalos de Navidad, amigo invisible, exhibidores 1:64, PLA o PETG, qué mandar para
  pedir). Fuente en `fuente/guias/`, generador `tools/guias.py`, estilos `src/guia.css`.
- Única entrada desde la landing: botón «Guías» con un libro pixel en la barra de arriba, entre el menú y el pedido.
- Cada guía: "respuesta corta" citable, tabla, tarjetas del catálogo con «Lo quiero» por WhatsApp, preguntas
  frecuentes autocontenidas, fecha visible. Datos: `BlogPosting`, `BreadcrumbList`, `FAQPage`.
- Base: 20 perfiles en paralelo (compradores, SEO local, GEO, ChatGPT/Perplexity/AI Overviews simulados,
  evaluador de calidad, abogado del consumidor, tráfico). Coincidencias: sin jerga en la guía de regalos,
  marcas solo en el cuerpo y con aclaración, no prometer fechas de Navidad, faltan datos del dueño
  (pago, embalaje, fecha límite). Plan y preguntas en `fuente/guias/PLAN-NAVIDAD.md`.
- Imágenes: ilustraciones pixel art a generar con Gemini (`fuente/guias/IMAGENES-GEMINI.md`), nunca como
  foto de producto. Mientras no existan, la portada usa una foto del catálogo.

## v9 (1/11/2026, guías de ajedrez)

Dueño: guías de ajedrez que terminen en un giro hacia la venta, para que los asistentes de IA recomienden
a Creaciones del Mago a quien busca un ajedrez o un ajedrez personalizado.

- Cinco guías: ajedrez personalizado en Uruguay (central, enlaza a las demás), medidas de un ajedrez
  (normas FIDE), se me perdió una pieza, historia de las piezas (Lewis y Staunton) y ajedrez para chicos.
- Base: 12 perfiles en paralelo (jugador de club, profesora, regalo personalizado, pieza perdida,
  coleccionista, historiador, viajero, ChatGPT simulado, GEO, tamaños especiales, abogado, copywriter).
- Datos de historia y medidas verificados en la web (Museo Británico, manual de la FIDE, registro de 1849).
- Personalización: solo lo confirmado (colores, tamaño, material, tema, diseño desde foto). Grabado de
  nombres y caras: "preguntame", nunca prometido. Marcas ajenas solo en el cuerpo y en las tarjetas.
- El giro de venta va siempre al final, después de resolver la pregunta.

## v10 (7/11/2026, catálogo lite y ajedrez primero)

Dueño: actualizar el catálogo con las fotos de los ajedrez vendidos (celular, por WhatsApp), que sea
más fácil llegar al fondo y pedir o hablar por WhatsApp, y foco en ajedrez, el nicho que mejor anda.
Base: cuatro investigaciones en paralelo, resumidas en `INVESTIGACION-CATALOGO-LITE.md`.

- Ajedrez es el primer estante (y link "Ajedrez" arriba). Siete juegos con fotos propias de vendidos;
  la foto del diseñador pasa a la galería. Nuevos: "Pieza suelta" (caballo dragón) y, en clickers,
  "Contador de vidas para Magic". Casita, élfico, repisa y ascensor también con foto propia.
- Galería por producto (`FOTOS` en `tools/catalog.py`): la ventana del producto muestra todas las
  fotos con lo que se ve en cada una (los colores en que ya se hizo).
- "Armá tu ajedrez": juego, color de cada bando y tablero; el WhatsApp se escribe solo.
- Celular: los demás estantes se deslizan de costado (la página bajó de ~22 a ~19 pantallas) y la
  barra de pedido está siempre desde el catálogo, aunque esté vacía.
- Fotos: retoque automático honesto en `tools/imgs.py`; lo que necesita IA (fondos, detalle en
  piezas negras) está en `fotos/IMAGENES-ANTIGRAVITY.md`, con reglas para no cambiar el producto.
- La etiqueta «Foto mía» sigue fuera (decisión del dueño): qué fotos son propias lo dicen el texto
  de cada estante y los pies de la galería.
