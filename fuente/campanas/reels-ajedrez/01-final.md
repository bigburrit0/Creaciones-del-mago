# Reel 1 · «La torre que muerde el escudo» · versión final

Video: `videos/01-torre-final.mp4` (1080×1920, 10 s, 30 fps, H.264 + AAC, −14,7 LUFS).
Sin voz: `videos/01-torre-sin-voz.mp4` · Voz sola en la línea de tiempo: `videos/01-torre-voz.wav`.
Se rearma con `python3 fuente/campanas/reels-ajedrez/armar_reel.py fuente/campanas/reels-ajedrez/videos/01-torre.json`
(tiempos y textos están en ese JSON).

## Formato

El crudo de Gemini salió en 16:9 (1280×720). No lo recorto al centro: un recorte 9:16 se queda con 405 px
de ancho y corta la fila del ejército dorado (de 4 a 7 s ocupa todo el ancho) y el tablero (unos 720 px).
Va a todo el ancho (1080×608, escalado con vecino más cercano) entre y = 540 y y = 1148, con bandas índigo
#1F1A3D arriba y abajo. Arriba la caja de diálogo, abajo el dato y el cierre. Quedan libres los 250 px de
arriba y los 420 px de abajo.

## Qué pasa en el crudo (medido cuadro a cuadro)

| Tiempo | Imagen |
|---|---|
| 0 – 1,5 s | Museo de noche, la vitrina en el centro, el cursor se acerca y hace clic |
| 1,5 – 3 s | La vitrina brilla, la torre de marfil gira la cabeza mordiendo el escudo, se abre la puerta |
| 3 – 6,5 s | La torre baja de la vitrina y entra el ejército dorado desde los dos costados |
| 6,5 – 7,5 s | Aparecen el tablero y la mesa, el ejército plateado se acomoda |
| 7,5 – 10 s | Set vikingo dorado contra plateado en la mesa, la torre vuelve a la vitrina, destellos |

## Guion

| Tiempo | Texto arriba (caja de diálogo) | Texto abajo | Voz en off |
|---|---|---|---|
| 0,15 – 6,8 s | `ESTA TORRE` / `MUERDE EL ESCUDO` (entra letra por letra) | | 0,55 – 3,7 s: «Hace más de ochocientos años alguien talló una torre que muerde su escudo.» |
| 2,4 – 8,3 s | | `PIEZAS DE LEWIS` / `SIGLO XII` (dorado) | (música y marcha del ejército, sin voz) |
| 6,8 – 10 s | `Ajedrez vikingo` / `impreso en 3D` | | 7,0 – 8,2 s: «Yo imprimo el ajedrez vikingo.» |
| 8,3 – 10 s | | Cierre: glifo dorado + caja `Escribime por mensaje` / `TE PASO EL PRECIO` (dorado) | 8,45 – 9,6 s: «Escribime y te paso el precio.» |

Voz completa (22 palabras): «Hace más de ochocientos años alguien talló una torre que muerde su escudo. Yo imprimo el
ajedrez vikingo. Escribime y te paso el precio.»

Cambios contra el guion base:
- El dato de Lewis pasa a la banda de abajo y queda en pantalla de 2,4 a 8,3 s, mientras la caja de arriba sigue
  con el gancho. Así no hay bandas vacías y el gancho dura lo que dura la frase.
- El cierre no lleva número de teléfono (decisión del dueño, COPY-RULES 17): el cierre del guion base pasa a
  «Escribime por mensaje / TE PASO EL PRECIO». El botón dice la acción (COPY-RULES 12) y repite la frase de la voz.
- La voz no va pegada: la frase 1 va sobre el clic y el brillo, la 2 cuando aparece el set en la mesa y la 3 con el
  cierre. Entre 3,7 y 7 s se escucha la marcha del ejército.

Datos (fuente en `INVESTIGACION.md`, informe 9): las piezas de Lewis son de 1150-1200 (más de 800 años en 2026);
cuatro torres son guerreros que muerden el escudo. El set es de estilo vikingo: no se dice que es una réplica de
Lewis ni que los vikingos jugaban ajedrez.

## Voz (Gemini TTS)

- Modelo: `gemini-3.8-flash-tts` (el TTS vigente en la API; también están `gemini-3.8-flash-lite-tts`,
  `gemini-3.1-flash-tts-preview` y los `2.5`). Voz prediseñada **Charon**, sin `languageCode`: el idioma y el
  acento van en el prompt.
- Prompt (estructura de perfil, escena, notas de dirección y transcripción):

```
# AUDIO PROFILE: Martín
Un tipo porteño de unos 35 años, de Buenos Aires, Argentina. Habla español rioplatense con acento argentino bien marcado: voseo, la "ll" y la "y" suenan "sh", entonación porteña.

## LA ESCENA
Le está contando a un amigo, en la mesa de un bar, un dato curioso que acaba de leer. Voz masculina cálida y cercana, con media sonrisa. No es un locutor de radio ni una publicidad.

### NOTAS DE DIRECCIÓN
Ritmo ágil y natural, casi sin pausas: todo el texto dura unos 8 segundos. Una mínima pausa después de "escudo" y después de "vikingo". "Escribime" con acento en la "i" de "bi".

#### TRANSCRIPCIÓN
Hace más de ochocientos años alguien talló una torre que muerde su escudo. Yo imprimo el ajedrez vikingo. Escribime y te paso el precio.
```

- Tomas probadas, controladas con transcripción automática (`gemini-3.5-flash`) y detección de silencios:

| Toma | Duración | Resultado |
|---|---|---|
| Charon | 6,7 s | Palabras exactas («ochocientos», «escribime»), rioplatense, conversación natural. **Elegida** |
| Umbriel | 6,7 s | Palabras exactas, pero suena a locutor de publicidad |
| Algenib | 7,2 s | Dice «hace **unos** ochocientos años»: descartada |
| Achird | 20,5 s | Lenta, con pausas largas: descartada |
| Charon (primer prompt, con `languageCode` es-AR) | 24,7 s | Leyó cosas de más: descartada |

- La toma elegida está en `videos/01-torre-voz-toma-gemini.wav`. Se corta en sus tres frases y cada una se pone en
  su segundo, a velocidad original (sin acelerar).

## Mezcla

- Música y efectos del crudo con ducking (sidechain con la voz): baja de 7 a 19 dB mientras habla la voz (7,4 dB
  en la fanfarria, que es la parte más fuerte) y vuelve sola entre frases.
- Normalizado en dos pasadas a −14 LUFS, pico −1,5 dBTP. Resultado: −14,7 LUFS con voz y −15,5 sin voz (el
  limitador de picos no deja subir más un clip tan corto).

## Texto del post

> Las piezas de Lewis aparecieron en 1831 en una isla de Escocia y son del siglo XII: hay torres que son guerreros
> mordiendo el escudo. Hoy 82 están en el Museo Británico y 11 en Edimburgo. Mi ajedrez vikingo no es una copia de
> esas piezas, es otro diseño con el mismo espíritu: reyes con espada y reinas con escudo, impreso en 3D en
> Montevideo, en los colores que elijas. Te paso precio y fecha por mensaje antes de empezar, sin compromiso.
> creacionesdelmago.com

## Revisión

Hoja de contacto en `videos/01-torre-hoja-contacto.png` (0,5 s, 3 s, 6 s, 7,5 s y 9,5 s, con las zonas de botones
marcadas en rojo): ningún texto entra en esas zonas ni queda cortado. En ningún cuadro aparece el número de teléfono.
