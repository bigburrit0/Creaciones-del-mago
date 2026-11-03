# Reel 2 · «Falta uno» · versión final

Video: `videos/02-falta-uno-final.mp4` (1080×1920, 10 s, 30 fps, H.264 + AAC, −14,1 LUFS).
Sin voz: `videos/02-falta-uno-sin-voz.mp4` · Voz sola en la línea de tiempo: `videos/02-falta-uno-voz.wav`.
Se rearma con `python3 fuente/campanas/reels-ajedrez/armar_reel.py fuente/campanas/reels-ajedrez/videos/02-falta-uno.json`
(tiempos y textos están en ese JSON).

## Formato

El crudo de Gemini salió en 16:9 (1280×720, 24 fps). Igual que en el reel 1, no lo recorto al centro: un recorte
9:16 se queda con 405 px de ancho y corta lo importante de dos escenas. Debajo del sillón, la linterna está a la
izquierda y el perro a la derecha (x 1000–1280). En la impresora, la impresora va de 0 a 850 px y el caballo blanco
que sirve de modelo está en x ≈ 880. Va a todo el ancho (1080×608, escalado con vecino más cercano) entre y = 540 e
y = 1148, con bandas índigo #1F1A3D arriba y abajo. Quedan libres los 250 px de arriba y los 420 px de abajo.

**Bordes negros del principio:** de 0 a 2 s el crudo es la imagen 1 (vertical) centrada en el cuadro 16:9, con
barras negras en las columnas 0–278 y 1002–1279. Las pinto del mismo índigo de las bandas, así esos 2 s se ven como
un cuadro de 608×608 en el centro, rodeado de índigo. El crudo pasa a la escena del sillón con un fundido de
1,975 a 2,21 s (medido cuadro a cuadro). Ahí el script no corta: suma el índigo en proporción inversa al fundido.
La barra fundida vale p × escena; sumándole (1 − p) × índigo queda el mismo fundido, pero empezando desde el
índigo. No se ve negro ni salto. Es la opción `bordes_negros` de `armar_reel.py` (el reel 1 no la usa y se
sigue armando igual: mismos cuadros, mismo MD5).

## Qué pasa en el crudo (medido cuadro a cuadro)

| Tiempo | Imagen |
|---|---|
| 0 – 2 s | El tablero con el hueco: el contorno dorado del caballo negro titila; el perro duerme en la alfombra (con bordes negros, ver arriba) |
| 2 – 2,2 s | Fundido a debajo del sillón |
| 2,2 – 5 s | Debajo del sillón, con la linterna: pelusas, una tapita, un botón, la media rayada; el perro levanta las orejas (≈ 3 s) y vuelve a dormirse |
| 5 – 5,3 s | Transición de mosaico a la impresora |
| 5,3 – 7,4 s | La impresora termina la cabeza del caballo negro; al lado, el caballo blanco de modelo y una regla; destellos sobre el blanco (≈ 6,4 s) |
| 7,4 – 7,7 s | Transición al tablero |
| 7,7 – 10 s | Otra vista del living con el tablero completo; de 8 a 8,8 s el perro sale de abajo de la **mesa ratona** (no del sillón) con el caballo viejo en la boca y se sienta. Después de 8,8 s, el sonido del crudo se apaga |

## Guion

| Tiempo | Texto arriba (caja de diálogo) | Texto abajo | Voz en off |
|---|---|---|---|
| 0,05 – 5,1 s | `FALTA UNO` (dorado, entra letra por letra en 0,3 s) | | 0,38 – 1,5 s: «¿Se te perdió el caballo?» |
| 2,25 – 5,05 s | `BUSCANDO... 0 DE 1` (contador de juego, letra chica, alineado a la izquierda entre la caja y el video) | | 2,8 – 5,26 s: «Mandame fotos de su pareja y las medidas, y te lo imprimo.» |
| 5,1 – 7,6 s | `Lo copio` / `del otro bando` | | (impresora y destellos, sin voz) |
| 7,6 – 10 s | `Piezas de repuesto` / `impresas en 3D` | | 7,9 – 9,1 s: «Si no se puede, te aviso antes.» |
| 8,3 – 10 s | | Cierre: glifo dorado + caja `Escribime por mensaje` / `TE PASO EL PRECIO` (dorado) | |

Voz completa (22 palabras, la del guion base sin cambios): «¿Se te perdió el caballo? Mandame fotos de su pareja y
las medidas, y te lo imprimo. Si no se puede, te aviso antes.»

Cambios contra el guion base:
- `FALTA UNO` queda arriba hasta los 5,1 s, y el contador `BUSCANDO... 0 DE 1` aparece debajo mientras dura la
  búsqueda bajo el sillón: el título de la misión con el contador abajo, como en un juego. La letra MagoPixel no
  tiene «…», así que el contador usa tres puntos.
- `Lo copio del otro bando` va en dos renglones (en uno no entra a tamaño 70) y queda sobre la impresora, que es
  donde se ven el caballo negro imprimiéndose y el blanco de modelo.
- `Piezas de repuesto · impresas en 3D` va en la caja de arriba, en dos renglones sin el «·», y el cierre va abajo,
  como en el reel 1. El cierre no lleva número de teléfono (COPY-RULES 17): «Escribime por mensaje / TE PASO EL
  PRECIO». La voz no repite el cierre: la última frase es «Si no se puede, te aviso antes», como en el guion base.
- La segunda frase va entera, sin cortar «y te lo imprimo» para ponerlo sobre la impresora: al cortarla, la «y»
  (40 ms) quedaba tapada por el zumbido de la impresora y el transcriptor no la oía. Entera, «te lo imprimo» cae en
  la transición a la impresora (4,6 – 5,3 s).
- El perro sale de abajo de la mesa ratona, no del sillón: ningún texto dice de dónde sale.
- En pantalla no se dice «idéntico» ni hay precios, plazos ni urgencia: dice que se copia de la pieza del otro
  bando, y la voz avisa que, si no se puede, se dice antes.

## Voz (Gemini TTS)

- Mismo modelo, voz y perfil que el reel 1: `gemini-3.8-flash-tts`, voz prediseñada **Charon**, sin `languageCode`
  (el idioma y el acento van en el prompt). Cambian la escena y las notas de dirección.
- Prompt:

```
# AUDIO PROFILE: Martín
Un tipo porteño de unos 35 años, de Buenos Aires, Argentina. Habla español rioplatense con acento argentino bien marcado: voseo, la "ll" y la "y" suenan "sh", entonación porteña.

## LA ESCENA
Le está hablando a un amigo, en la mesa de un bar, que le cuenta que se le perdió una pieza del ajedrez de la familia. Voz masculina cálida y cercana, con media sonrisa. No es un locutor de radio ni una publicidad.

### NOTAS DE DIRECCIÓN
Ritmo ágil y natural, casi sin pausas: todo el texto dura unos 7 segundos. La primera frase es una pregunta, con entonación de pregunta. Una mínima pausa después de "caballo" y después de "imprimo". "Mandame" con voseo, acento en "da" (man-DA-me). "Fotos" en plural, con la "s". "Medidas" bien claro.

#### TRANSCRIPCIÓN
¿Se te perdió el caballo? Mandame fotos de su pareja y las medidas, y te lo imprimo. Si no se puede, te aviso antes.
```

- Tomas probadas, controladas con transcripción automática (`gemini-3.5-flash`) y detección de silencios:

| Toma | Duración | Resultado |
|---|---|---|
| 1 (primer prompt) | 6,4 s | Rioplatense, «mandame» llano y «medidas» claras, pero dice «foto» en singular: descartada |
| 2 (primer prompt) | 6,3 s | Igual que la 1, «foto»: descartada |
| 3 (primer prompt) | 6,5 s | «Fotos» bien; en una de dos transcripciones el principio sale «Si se te perdió»: descartada |
| 5 (prompt corregido) | 5,8 s | Se transcribe «Si se te perdió…» y «foto»: descartada |
| 6 (prompt corregido) | 6,6 s | Palabras exactas en las dos transcripciones, rioplatense, «mandame» con voseo (man-DA-me), «medidas» clara. **Elegida** |

  El primer prompt pedía, por error, el acento de «mandame» en «man». En voseo va en «da» (mandá + me), y el modelo
  lo dijo bien igual. El prompt de arriba es el corregido, el de las tomas 5 y 6. La toma 4 dio error de cuota de la
  API y no se generó.
- La toma elegida está en `videos/02-falta-uno-voz-toma-gemini.wav`. Se corta en tres frases (0,04–1,24 s,
  1,92–4,47 s y 4,78–6,08 s) y cada una va en su segundo (0,35 s, 2,75 s y 7,85 s), a velocidad original. La voz
  ocupa de 0,38 a 9,1 s.
- Control de la mezcla final: la transcripción del MP4 dice «¿Se te perdió el caballo? Mandame fotos de su pareja y
  las medidas y te lo imprimo. Si no se puede, te aviso antes.» En dos de cuatro pasadas el transcriptor escribió
  «Si/Si se te perdió» con el texto entero; la apertura sola se transcribe siempre «¿Se te perdió el caballo?».

## Mezcla

- Música y efectos del crudo con el mismo ducking que el reel 1 (sidechain con la voz: umbral 0,012, ratio 10,
  ataque 15 ms, suelta 350 ms). Baja de 19 a 21 dB mientras habla la voz y vuelve sola: la impresora y el
  «encontrado» (5,3 – 7,9 s) suenan enteros.
- Normalizado en dos pasadas a −14 LUFS, pico −1,5 dBTP. Resultado: −14,1 LUFS con voz y −14,3 sin voz.

## Texto del post

> Para jugar hoy: si falta un peón, usá una tapita; si falta la dama, una torre dada vuelta, como en los clubes.
> Para reponerla, mandame fotos de la pieza que falta en su pareja del otro bando (si perdiste el caballo negro, el
> blanco tiene la misma forma), la altura y el ancho de la base. La imprimo en 3D en Montevideo y te paso el precio
> por mensaje antes de empezar, sin compromiso. Si no se puede imprimir, te aviso antes.
> creacionesdelmago.com

(El del guion base, sin cambios: no tiene teléfono ni precio.)

## Revisión

Hoja de contacto en `videos/02-falta-uno-hoja-contacto.png` (0,5 s, 3 s, 6 s y 9,5 s, con las zonas de botones
marcadas en rojo): ningún texto entra en esas zonas ni queda cortado. La flecha de «seguir» de la caja de
`Lo copio` está apagada para que no pise el video. El paso de los 2 s se revisó cuadro a cuadro: los costados van
del índigo a la escena del sillón, sin negro. En ningún cuadro, ni en la voz, ni en el texto del post aparece un
número de teléfono. En el borde del tablero se ven las coordenadas del crudo (letras y números chiquitos, ilegibles):
son parte del dibujo de Gemini, no un número.
