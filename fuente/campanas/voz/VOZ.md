# Voz de la marca · Creaciones del Mago

Voz en off de los reels, aprobada por el dueño el 2/11/2026 (Reel 1 «Huevito»). Se usa en todos los reels
nuevos, en primera persona y según `fuente/COPY-RULES.md`.

| | |
|---|---|
| Servicio | Gemini API, text-to-speech |
| Modelo | `gemini-3.8-flash-tts` |
| Voz | `es-419-techagent-10` (biblioteca extendida de voces de Gemini; argentina, 34 años, «conversational, slightly dry humor») |
| Acento | Rioplatense, con voseo |
| Formato que devuelve | WAV mono 24 kHz |
| Referencia aprobada | `referencia-huevito.wav` («Esta no come, no se muere y hace clic. Un clicker para el amigo invisible. Escribime y te paso el precio.») |

## Cómo generarla

```bash
python3 fuente/campanas/voz/generar_voz.py "Mandame una foto y te digo si se puede." voz.wav
python3 fuente/campanas/voz/generar_voz.py "..." voz.wav --tomas 3          # tres tomas para elegir
python3 fuente/campanas/voz/generar_voz.py "..." voz.wav --notas "Más calmo, de tarde de verano."
```

El script arma el prompt que dio la toma aprobada (perfil, escena, notas de dirección y el texto). Las notas de
dirección:

- Español rioplatense con voseo, como alguien que le cuenta algo a un amigo.
- Cercano, relajado, humor seco, con una sonrisa leve. Nada de locutor ni de tono publicitario.
- Ritmo ágil, sin apuro, con una pausa corta después de cada punto.

## A tener en cuenta

- **El timbre es siempre el mismo, la interpretación cambia un poco en cada toma.** Conviene pedir 2 o 3 tomas
  (`--tomas 3`) y quedarse con la que más se parezca a `referencia-huevito.wav`.
- **Una sola toma con todo el texto** suena más natural que frase por frase. Después se corta por los silencios:
  `armar.py` del Huevito lo hace solo (`tramos_de_voz`), y en CapCut se corta a mano.
- **Fondo:** mientras habla, el resto del audio baja 6 dB.
- **Clave:** variable `GEMINI_API_KEY`. En las sesiones de Claude Code la pone el proxy. Con el plan gratis, el
  límite diario de TTS se agota rápido: el 2/11 se cortó después de unas 6 tomas.
- **Si Google cambia o retira la voz,** cualquier voz argentina de la biblioteca sirve para salir del paso
  (`GET /v1beta/voices`, `language_code` = `es-419`, acento «Argentina Spanish»). Para un reemplazo fijo, buscar
  una con el mismo tono y comparar contra la referencia.
- **Nunca el número de teléfono en la voz** (regla de los reels).
