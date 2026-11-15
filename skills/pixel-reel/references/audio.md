# Audio con chiptune.py

```bash
python3 scripts/chiptune.py <reel>/cues.json <reel>/hf/assets/audio
python3 scripts/chiptune.py --list
```

Genera tres pistas: `sfx.wav` (efectos), `music.wav` (música) y `ambience.wav` (ambiente). En la composición van como tres `<audio>` con su volumen (`data-volume`): música 0,5, efectos 1 y ambiente 0,35 suelen funcionar bien.

## cues.json

```json
{
  "duration": 15,
  "sfx": [
    {"t": 0.0, "s": "door_bang"},
    {"t": 0.3, "s": "flipflop", "n": 6, "every": 0.18},
    {"t": 8.6, "s": "item_get", "pitch": 1.12},
    {"t": 10.0, "s": "pop", "n": 8, "every": 0.1, "pitch_step": 1.09},
    {"t": 7.7, "s": "printer", "d": 0.7}
  ],
  "music": {"bpm": 140, "start": 0.3, "melody": [[4, 1], [4, 1], [4, 2]], "chords": [0, 0, 5, 7],
            "duck": [[5.75, 6.95, 0.3]], "end_chord": {"t": 14.0, "notes": [0, 4, 7, 12]}, "fade_out": [14.4, 15.0]},
  "ambience": [{"type": "cicadas", "from": 0, "to": 15, "level": 0.15}]
}
```

- **Melodía**: semitonos desde do5 (0 = do, 4 = mi, 7 = sol, 12 = el do siguiente, `null` = silencio). Duraciones en tiempos. Los acordes son la fundamental de cada compás.
- **Bajar la música** (`duck`): en momentos tristes o de suspenso, y bajo los efectos importantes.
- **Efectos disponibles**: tap, door_bang, door_close, creak, step, flipflop, plop, pop, sparkle, chime, idea, item_get, whoosh, sack_plop, boom, victory, sad, surprise, relief, sip, flutter, flap, peck, click, ding, printer (con `d`), fuse (con `d`), heave, puff, chirp.
- **Ambiente**: `cicadas`, `waves`, `birds`.

## Criterios

- Cada acción visible tiene su sonido, sincronizado con el cuadro que la muestra (el pie que pisa, la mano que suelta el ítem).
- Si algo se repite, subir el tono en cada vez (`pitch_step`): se siente que crece.
- Usar solo melodías propias o de dominio público (por ejemplo villancicos tradicionales), con arreglo propio.
- Sin voces ni letras. El mensaje va en el caption.
