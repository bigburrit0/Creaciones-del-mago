# Reels de 10 segundos en pixel art · Creaciones del Mago

Cuatro guiones nuevos para Reels, TikTok y Shorts (9:16, 1080 × 1920, 10 s). Cada uno tiene un concepto
y un género de videojuego distinto, y ninguno repite las ideas de la campaña anterior (clicker que transforma
el escritorio, forja con rayos de filamento, vitrinas de inventario, panales tipo Tetris, foto rota que se
vuelve wireframe, estadios con franjas, pantalla de victoria).

| # | Archivo | Género retro | Producto | Público | Tono |
|---|---|---|---|---|---|
| 1 | `01-huevito-mascota-virtual.md` | Mascota virtual de bolsillo | Clicker hámster en el huevo | Amigo invisible, Navidad | Ternura con humor seco |
| 2 | `02-continue-manija-del-termo.md` | Pantalla de «Continue? 9, 8, 7» | Repuesto a medida (manija de termo) | Gente con algo roto, mateadores | Humor seco |
| 3 | `03-carrera-por-la-rambla.md` | Carreras con piso en perspectiva (Mode 7) | Fiat 500 de 1965 y Escarabajo para armar | Nostálgicos, regalo para el viejo | Épico y nostálgico |
| 4 | `04-la-huerta-de-los-pajaros.md` | Simulador de granja | Comedero casita | Gente con fondo o balcón | Tranquilo, de verano |

Los cuatro se pueden pautar desde ya. El 1 y el 3 están pensados para Navidad y el 4 sirve como regalo.

## Cómo se usa cada archivo

Cada guion tiene el mismo orden:

1. **Paso 1 · Imágenes.** Cuatro prompts, uno por escena (imagen 1 a 4). Cada uno está completo (estilo,
   paleta y Mago incluidos): se copia entero en Gemini y se genera una imagen por vez. Desde la imagen 2,
   conviene adjuntar la imagen 1 para que el fondo no cambie.
2. **Paso 2 · Video.** Se adjuntan las cuatro imágenes en orden y se pega el prompt del video de 10 s. Abajo
   del prompt dice qué hacer si la herramienta acepta solo primer y último cuadro, una sola imagen, o da 8 s.
3. **Después.** Guion con los tiempos, voz en off, texto del post, otros cierres y cómo editarlo.

Según lo que encontró la investigación, Veo 3.1 genera clips de 4, 6 u 8 s y Gemini Omni Flash de 3 a 10 s.
Si te da 8 s, se congela el último cuadro 2 s en la edición. En pixel art un cuadro quieto no se nota raro.

## Bloque de estilo (ya está incluido en cada prompt)

Queda acá como referencia, por si generás alguna imagen extra.

```
Style: authentic 16-bit home-console pixel art from the early 1990s. Hard square pixels on a visible grid, 1-pixel dark outlines, no anti-aliasing, no blur, no soft gradients (only ordered Bayer dithering), limited palette of about 24 colors. Brand palette: deep night indigo #1F1A3D and #2A2350, violet-blue #4E4399 for mid-tones, warm cream #F3E9D2 for light surfaces, gold #F2A93B as the main accent, with small touches of pine green #2F6B4F and warm red #E2504C only where the scene needs them. Flat 2D game look, not a 3D render, not photorealistic. Vertical 9:16 (1080x1920). Keep the top 13% and the bottom 22% of the frame calm and uncluttered (plain sky, wall, floor or sea) for on-screen text and app buttons. No text, no letters, no numbers, no logos, no brand marks, no watermarks.
```

## Hoja de personaje del Mago (opcional)

El sitio no tiene un sprite del Mago, solo el glifo y la pirámide. Los prompts de los guiones 3 y 4 ya lo
describen igual en cada imagen. Si aun así cambia de una imagen a otra, generá esta hoja y adjuntala. Si ya tenés
un Mago aprobado de la campaña anterior, usá ese.

```
Character reference sheet for a 16-bit pixel art video game hero called the Wizard. One small friendly wizard sprite, about 48 pixels tall, shown three times side by side on a plain cream #F3E9D2 background: facing front, walking to the right in side view, and waving. Deep indigo robe #2A2350 with violet-blue #4E4399 folds, a tall pointed hat with a wide brim and a gold #F2A93B band, a short cream beard, round dark eyes, rosy cheeks, a small gold buckle on the belt, simple brown boots. Friendly and a bit mischievous. Same proportions in the three poses. Hard pixel edges, 1-pixel dark outline, no anti-aliasing, limited palette. No text, no letters, no logos.
```

Para usarlo después, en cada prompt: `Use the attached Wizard reference sheet and keep the Wizard exactly the same (robe, hat, beard, proportions).`

## Reglas para los cuatro

- **Sin texto generado.** Ni en imágenes ni en video: la IA escribe mal. Todo el texto va en la edición, con
  una fuente pixel. La del sitio es MagoPixel (`fonts/MagoPixel-Bold.woff`); CapCut pide TTF u OTF, así que
  hay que convertirla, o usar Press Start 2P o Silkscreen de Google Fonts.
- **El logo es el real.** El glifo dorado (`assets/px/glifo-oro.png`) se pega en la edición, nunca se le pide
  a la IA.
- **Sin marcas ajenas en la imagen.** Nada de logos de autos, termos, juguetes ni clubes. Los nombres de los
  modelos (Fiat 500, Escarabajo) van solo en el texto, igual que en el catálogo.
- **Son ilustraciones.** La pieza real se ve en el catálogo. En el texto del post se puede decir «mirá las fotos
  en la web».
- **Audio en el video, voz aparte.** En el prompt de video se piden efectos y música chiptune, sin diálogo
  (la investigación no encontró confirmación de que el español rioplatense salga bien). La voz en off la grabás
  vos con el celular, en primera persona: suena a persona, que es lo que piden las reglas de texto.
- **Texto según `fuente/COPY-RULES.md`.** Yo y voseo, un dato en vez de un adjetivo, nada inventado: ni
  reseñas, ni «quedan pocos», ni plazos que no sean «mínimo 48 horas de preparación». Para Navidad no se promete
  fecha: «si es para Navidad, decímelo y te digo si llego».
- **Zona segura de Instagram.** Arriba 250 px y abajo 420 px libres de cosas importantes. Los textos van en la
  franja del medio y el CTA, justo arriba de los 420 px de abajo.

## Qué dijo la investigación (tres subagentes, 2/11/2026)

**Cómo generar el video.** Lo que sigue sale de extractos de búsqueda de páginas de Google, porque las páginas
completas no se pudieron abrir desde la sesión. Conviene revisarlo en la herramienta antes de producir.
- Gemini Omni Flash: 9:16 y de 3 a 10 s, con audio nativo y una imagen como primer cuadro. Veo 3.1: 4, 6 u 8 s,
  con primer y último cuadro («Frames to video») y extensión de 7 s.
- Estructura de prompt que recomienda Google: cámara, sujeto, acción, contexto, estilo y audio.
- Para que el pixel art no se derrita: **cámara fija** (el movimiento de cámara obliga al modelo a inventar
  profundidad y rompe el estilo), un solo plano («single continuous shot, no cuts») y describir lo que querés
  en vez de listar lo que no.
- El texto dentro del video sale deformado: hay que agregarlo en la edición.
- No se encontró una lista oficial de bloqueos por marcas o personajes. Por las dudas, ninguno de estos guiones
  usa personajes de franquicias ni escudos.

**Ganchos y loops.** Hay pocos datos firmes.
- Emplifi (10.110 Reels de Facebook, marzo 2026, correlacional): voz en los primeros 3 s se asocia a +24,7 % de
  retención a los 10 s, y los loops de hasta 7 s, a +18,7 % de repeticiones. Por eso los cuatro arrancan con
  movimiento y voz desde el primer segundo, y el último cuadro empalma con el primero.
- No se encontraron campañas de pixel art 2023-2026 con métricas publicadas. Las referencias (McDonald's Japón con
  Street Fighter en 2025, el juego arcade de Nissan Formula E en 2025) usan el pixel art como juego o parodia de un
  género, que es lo que hacen estos guiones.

**Uruguay y Navidad.** TaTa ya hizo «Navidad con nieve en Montevideo» en 2024. Acá se va al revés: Navidad en
verano, sin nieve. Lo local entra por la rambla, el mate y los pájaros de acá (benteveo, hornero), sin tango, sin
gaucho y sin bandera en todo.

Fuentes principales: ai.google.dev/gemini-api/docs/omni · ai.google.dev/gemini-api/docs/veo ·
cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1 ·
deepmind.google/models/gemini-image/prompt-guide · socialmediatoday.com (estudio de Emplifi sobre Reels) ·
elobservador.com.uy (campaña de Navidad de TaTa 2024).
