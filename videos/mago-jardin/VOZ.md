# Reel «La huerta de los pájaros»: la voz

**Listo para publicar:** `mago-jardin-final.mp4` (10 s, 9:16), con textos, música, efectos y voz en off
generada con la API de Gemini (TTS, voz Charon, acento rioplatense). Las tomas están en `voz/v1.wav` … `v4.wav`.

Para regenerar la voz (cuota gratis: 3 pedidos por minuto y unos 10 por día y modelo; el script espera solo):

```bash
python3 tools/tts_gemini.py voz --model gemini-3.1-flash-tts-preview      # --voice para cambiar la voz
python3 tools/mix_voice.py mago-jardin-texto.mp4 mago-jardin-final.mp4 voz/v1.wav voz/v2.wav voz/v3.wav voz/v4.wav
```

`tts_gemini.py` pide «No da tomates... da benteveos.» en una sola toma (sola, la frase corta salía «Ah, tomates»)
y la corta en la pausa. Si preferís tu propia voz, seguí con lo de abajo.

## 1. Grabar

Mirá `guia-voz.mp4` (es solo para vos, no se publica): muestra cada frase en el momento en que va.
Grabá con el celular, en un lugar sin eco (un placard con ropa sirve), a un palmo del micrófono, con calma.

| Empieza en | Frase | Pasa en pantalla |
|---|---|---|
| 0,3 s | «No da tomates:» | `PLANTÁS ESTO.`, crece el arbolito |
| 2,45 s | «da benteveos.» | `COSECHÁS ESTO.`, sale el comedero (decilo justo ahí) |
| 3,95 s | «Es un comedero impreso en 3D, en PETG para el sol.» | llegan los pájaros, el Mago va a la silla |
| 8,1 s | «Escribime y te paso el precio.» | se abre el cuadro final («Escribime por mensaje») |

Dos formas de grabarla:
- **Una toma** con la frase entera (`voz.m4a`). El script la pone a los 0,3 s. Hacé una pausa corta después de «tomates» y otra antes de «Escribime».
- **Cuatro audios**, uno por frase (`v1.m4a` … `v4.m4a`). Cada uno cae solo en su momento. Es lo más prolijo.

## 2. Mezclar (desde esta carpeta)

```bash
python3 tools/mix_voice.py mago-jardin-texto.mp4 mago-jardin-final.mp4 voz.m4a
# o, con cuatro audios:
python3 tools/mix_voice.py mago-jardin-texto.mp4 mago-jardin-final.mp4 v1.m4a v2.m4a v3.m4a v4.m4a
```

El script corta los silencios del principio y del final, limpia y empareja el volumen de la voz y baja la música
mientras hablás. Si la voz se pasa de los 10 s, avisa. Requiere ffmpeg.
Si preferís CapCut: subí `mago-jardin-texto.mp4`, poné la voz encima y bajá el audio original a un 40 %.

## 3. Texto del post

> No da tomates: da benteveos. El comedero casita lo imprimo en 3D en Montevideo, y comen varios pájaros a la vez.
> Si va al sol, conviene PETG, que aguanta mejor la intemperie: preguntame. En el catálogo hay más comederos,
> pajareras y un bebedero para abejas. Te paso precio y fecha por WhatsApp antes de empezar, sin compromiso.
> 092 104 419 · creacionesdelmago.com

En el video no va el número de WhatsApp: el cuadro final dice «Escribime por mensaje».

Otros cierres (cambian el cuadro final en `index.html`, `#card-text`, y la última frase de la voz):
- Navidad: «Si es para Navidad, decímelo y te digo si llego.»
- Balcón: «¿Solo balcón? Hay comederos y pajareras más chicos.»
- Comentarios: «¿Qué pájaros vienen a tu fondo? Contame.»
