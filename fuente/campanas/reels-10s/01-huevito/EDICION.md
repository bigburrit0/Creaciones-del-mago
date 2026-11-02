# Reel 1 · «Huevito» · edición final

Proyecto de edición del guion `../01-huevito-mascota-virtual.md`. Parte del video que generó Gemini
(720 × 1280, 24 fps, 10 s, con efectos de sonido propios) y le suma textos en MagoPixel, la caja de cierre
con el glifo real, música chiptune propia, grillos y la voz en off.

Salida: MP4 1080 × 1920, H.264 High, 24 fps, AAC 48 kHz, −14 LUFS, **11,5 s**.

## Cómo se arma

```bash
# 1. Bajar el video de Gemini (Drive) y dejarlo en base/huevito-gemini.mp4 (no se versiona)
# 2. Requisitos: ffmpeg, Python 3 con numpy, Pillow y fontTools (pip install numpy pillow fonttools)
python3 armar.py                  # salida/huevito-con-voz.mp4  (voz de IA ya incluida)
python3 armar.py --sin-voz        # salida/huevito-sin-voz.mp4  (para pegar otra voz en CapCut)
python3 armar.py --snapshots 2,7.3,11   # cuadros sueltos en PNG para revisar
```

Todo sale de `timeline.json`: tiempos, textos, tamaños, voz y mezcla. Para cambiar el cierre (por ejemplo
«Regalo chico para Navidad»), se cambia ahí y se vuelve a correr.

## Tiempos reales (cuadro a cuadro del video de Gemini)

El video generado no sigue exacto el guion: el hámster nace en 2,0 s, sale en 4,0 s y el clic es en 7,3 s.

| Tiempo | Qué pasa en el video | Texto en pantalla | Voz en off | Audio |
|---|---|---|---|---|
| 0,0 – 2,0 | Huevo en la pantallita, el dedo entra y aprieta el botón (0,9 s) | `NACIÓ TU MASCOTA` se tipea 1,3 → 1,95 | 0,3 «Esta no come,» | pitido del video en 0,9 |
| 2,0 – 4,0 | Se rompe el huevo, nace el hámster con corazones (2,0) | (sigue hasta 4,0) | 3,2 «no se muere» | sonido de nacimiento del video en 2,0 |
| 4,0 – 5,8 | El hámster sale de la pantalla, salta (4,75 – 5,5) y cae en la cáscara gris (5,8) | (limpio: el salto pasa por el cielo) | | salto y caída del video |
| 5,8 – 7,3 | Ya es el clicker en su cáscara. El dedo entra en 6,9 | `NO COME.` 5,8 · `NO SE MUERE.` 6,25 · `HACE CLIC.` 6,9 → 7,3 | 6,3 «y hace clic.» | |
| 7,3 – 8,5 | Clic en la cabeza (7,3), cierra los ojos, destello dorado | (sigue hasta 8,25) | 7,6 «Un clicker para el amigo invisible.» | clic y acorde del video |
| 8,25 – 9,7 | El dedo se va. La pantalla vuelve a mostrar un huevo nuevo (8,75) | Caja de cierre: glifo + `Hámster en el huevo` / `clicker impreso en 3D` / `Para el amigo invisible` / `Escribime por mensaje` | 9,3 «Escribime y te paso el precio.» | pop y destello del cierre |
| 9,7 – 11,5 | Cuadro quieto con el huevo nuevo: empalma con el primer cuadro (loop) | (caja completa) | | grillos y acorde final |

- El video de Gemini se corta en 9,67 s, porque en 9,75 vuelve a aparecer el hámster en la pantalla y rompía
  el loop. Desde ahí queda quieto el cuadro del huevo, como dice el LEEME (en pixel art no se nota).
- Se alarga de 10 a 11,5 s para que la voz entre sin apuro y el cierre quede legible ~1,2 s completo.
- Zona segura: todos los textos van entre y = 262 y y = 800 (cielo de la ventana). Arriba quedan libres los
  250 px y abajo los 420 px. La caja va arriba y no abajo porque en este video la parte de abajo es el clicker y
  la mesa: una caja ahí tapaba el producto.

## Estilo de los textos

- MagoPixel Bold (`fonts/MagoPixel-Bold.woff`, se pasa a TTF al armar). Un píxel de la fuente = 8 o 9 px en
  los títulos, 6 o 7 px en la caja: queda en grilla, sin antialias.
- Crema `#F3E9D2` con contorno índigo `#1F1A3D` de un píxel de fuente y sombra de un píxel abajo.
- Máquina de escribir: 24 letras/s en los títulos, con cursor dorado que parpadea y un tic por cada dos letras;
  48 letras/s en la caja.
- Cierre: caja índigo con borde dorado `#F2A93B` en escalón (ventana de RPG), se abre en 4 cuadros; el glifo
  real `assets/px/glifo-oro.png` a ×2 con contorno índigo, aparece con un pop por pasos (×1, ×3, ×2).
- El llamado a la acción («Escribime por mensaje») en dorado; el resto en crema.
- **Nunca el número de teléfono** en el reel (pantalla, voz ni post). `armar.py` no exporta si el
  `timeline.json` tiene uno; para revisar todo: `python3 ../revisar_reglas.py`.

## Audio

- Se usa el audio del video de Gemini (pitidos, nacimiento, salto, caída, clic y acorde). Tenía audio usable.
- Encima: música chiptune propia (do mayor, 120 bpm, `cues` generados en `salida/cues.json`, sintetizada con
  `chiptune.py` de la skill pixel-reel), grillos de verano, tics de máquina de escribir y pop del cierre.
- Mientras habla la voz, todo el fondo baja 6 dB (con rampa de 0,12 s).
- Mezcla final normalizada a −14 LUFS (Instagram), pico a −1 dBFS.

## Voz en off

Texto (sin cambios): «Esta no come, no se muere y hace clic. Un clicker para el amigo invisible. Escribime y te
paso el precio.»

**La que va en `huevito-con-voz.mp4`:** Gemini 3.8 Flash TTS (`gemini-3.8-flash-tts`), voz
`es-419-techagent-10` de la biblioteca extendida (argentina, «conversational, slightly dry humor»). Es
rioplatense y con voseo natural. Prompt y script en `../../voz/` (`VOZ.md`); toma en
`../../voz/referencia-huevito.wav` (7,7 s, 24 kHz). `armar.py` la corta sola en las 5 frases por los silencios
y pone cada una en su tiempo.

Por qué esa: al 2/11/2026, las comparativas ponen a ElevenLabs (v3 / multilingual) y Gemini TTS arriba en
naturalidad, casi empatados, y a OpenAI un escalón abajo en expresividad. No hay un benchmark propio de español.
Gemini tiene 53 voces argentinas, que es lo más cerca del acento de Montevideo, y la clave ya estaba en la
sesión. Se generaron 5 voces (techagent-10, podcaster-12, tutor-11, training-6, assistant-5).

La voz quedó como **voz de la marca** para los próximos reels: `../../voz/VOZ.md`.

**Si querés otra voz** (ElevenLabs, otra de Gemini o la tuya):

1. Generá una sola toma con la frase completa, con pausas marcadas entre las 5 frases.
   - ElevenLabs: modelo Eleven v3 (o Multilingual v2), una voz en español de Argentina de la Voice Library,
     Stability ~45 %, Similarity ~75 %, Style ~20 %, speaker boost activado, velocidad 1,0. Texto:
     `Esta no come, ... no se muere ... y hace clic. Un clicker para el amigo invisible. Escribime y te paso el precio.`
   - Gemini: `python3 ../../voz/generar_voz.py "texto" salida.wav --voz OTRA_VOZ`.
2. `python3 armar.py --voz mi-toma.wav --nombre huevito-voz2`. Corta la toma en 5 frases y las pone en
   0,3 · 3,2 · 6,3 · 7,6 · 9,3 s. Si no encuentra las 4 pausas, la pega entera desde 0,3 s.
   `--una-toma 0.3` la pega entera sin cortar.
3. En CapCut, sin correr nada: usá `huevito-sin-voz.mp4`, poné cada frase en esos tiempos y bajá el video 6 dB
   mientras habla.

## Texto del post

> Una mascota que no come, no se muere y hace clic. Es el hámster en el huevo: un clicker impreso en 3D, acá en
> Montevideo. Para el amigo invisible podés pedir uno o varios para todo el grupo y te paso el precio total por
> mensaje antes de empezar, sin compromiso. creacionesdelmago.com
