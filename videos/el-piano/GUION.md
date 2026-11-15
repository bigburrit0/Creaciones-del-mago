# El piano (ocarina reel O3, reach; script in `../PLAN_OCARINA.md`)

Publish: Wed 9/12. CTA keyword: RAMBLA (reward: price and date). Sound: synthesised (`../biblioteca/ocarina_synth.py`),
labelled "Sonido digital" on screen; the ocarina is a 3D illustration (the owner's decision, 15/11/2026).

## Caption (curated from the three caption writers: humour, practical, character)

```
Papá Noel llegó a la rambla empujando un piano. Yo llegué con una ocarina de 12 agujeros. 🎹

Ocarina impresa en 3D en Montevideo: 10 agujeros arriba y 2 para los pulgares.
¿Entra en una mano? En una mano. Y va a todos lados.
La hago a pedido.
El video es una animación.
¿Qué te llevás a la rambla? Comentá RAMBLA y te paso precio y fecha.
Precio y fecha por WhatsApp al 092 104 419, antes de empezar y sin compromiso.
Envío gratis solo en La Unión, La Blanqueada y parte de Buceo; mando a todo Uruguay.
Pedidos para Navidad: hasta el 23 de diciembre.

#Montevideo #Uruguay #ramblamontevideo #impresion3d #ocarina #regalosdenavidad
```

## DM (private reply to whoever comments RAMBLA)

```
¡Hola! Gracias por comentar RAMBLA 🎹
¿Para quién es? ¿Para la rambla o para regalar?
Te paso precio y fecha por WhatsApp, antes de empezar y sin compromiso.
```

## Result (2026-11-15)

`el-piano.mp4`: 23.05 s, 1080×1920, 60 fps.
- QA gate 0 bad frames (the second run: the piano kept 45 cm ahead of him so his jacket's knot clears it), 0 jumps, deterministic; flicker scan 0 frames.
- Sound rebuilt with `remezclar.py` to -14.1 LUFS (peak -4.3 dBFS); music 25 dB under the voices, 17 dB under them in the gaps.
- Mix transcription: every line clear.
- A new set: the rambla (paving, the low wall, the water, a bench, a lamp post); the ocarina plays an original phrase (synthesised, "Sonido digital") and lands in El Mago's hand.

### Music from the owner's score (2026-11-15, second mix)

The ambient bed was replaced by music made from the owner's score p04 (sol menor, ♩=60, expressivo), bars 1-6 (`../biblioteca/partituras/`, used with the owner's
permission), with `../biblioteca/partitura_synth.py`: a soft music box, a pad and a bass, ducked under the voices and out
under the ocarina. Rebuild: `bash ../ocarina/build_reel.sh "c1 c2 c3 c4 c5" "rambla" "p04-sol-menor-60 1-8 1.0"`, then `remezclar.py` (the picture is byte-identical).
Levels: music -23.6 dB under the voices, -14.8 dB in the gaps; -14.1 LUFS; every line clear in the mix transcription.

### The band (2026-11-15, third mix)

The owner found the music-box version too empty and asked for piano, percussion, bass, a synthesiser and a theremin. Now
`../biblioteca/partitura_banda.py` plays the same score as a band: the piano (melody and chords on each beat), a soft drum
groove, the bass, a detuned saw pad and a theremin that carries the melody in the gaps between spoken lines (out under the
voices; the piano carries it there). Everything ducks under the voices and is out under the ocarina; +2.5 dB over the old
bed. Levels: music -24.9 dB under the voices, -13.3 dB in the gaps; -14.1 LUFS; every line clear in the mix transcription.

### Exact notes (2026-11-15, fourth mix)

The band now plays the owner's exact transcription (`../biblioteca/partituras/transcripciones-del-duenio.txt`): score args `p04-sol-menor-60 1-10 1.0`. -14.1 LUFS; every line clear.

### No badge (2026-11-15)

The owner asked to remove the "Sonido digital" badge and the "Ilustración 3D · sonido digital" line ("queda super implícito"); the caption keeps "El video es una animación."
