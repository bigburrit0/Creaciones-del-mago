# La batata (ocarina reel O1, reach; script in `../PLAN_OCARINA.md`)

Publish: Fri 27/11. CTA keyword: BATATA (reward: price and date). Sound: synthesised (`../biblioteca/ocarina_synth.py`),
labelled "Sonido digital" on screen; the ocarina is a 3D illustration (the owner's decision, 15/11/2026).

## Caption (curated from the three caption writers: humour, practical, character)

```
¿Imprimí una batata? Casi: es una ocarina hecha en 3D en Montevideo. 🍠

Una ocarina de 12 agujeros: 10 arriba y 2 para los pulgares. Tiene forma de batata, pero la ocarina se sopla, no se come.
Cada ocarina la imprimo yo, a pedido.
El video es una animación.
¿Batata u ocarina? Comentá BATATA y te paso precio y fecha.
Precio y fecha por WhatsApp al 092 104 419, antes de empezar y sin compromiso.
Envío gratis solo en La Unión, La Blanqueada y parte de Buceo; mando a todo Uruguay.
Pedidos para Navidad: hasta el 23 de diciembre.

#Montevideo #Uruguay #impresion3d #ocarina #regalosdenavidad #instrumentosmusicales
```

## DM (private reply to whoever comments BATATA)

```
¡Hola! Gracias por comentar BATATA 🍠
¿Para quién es la ocarina?
Te paso precio y fecha por WhatsApp, antes de empezar y sin compromiso.
```

## Result (2026-11-15)

`la-batata.mp4`: 25.3 s, 1080×1920, 60 fps.
- QA gate 0/1518 bad frames, 0 jumps, deterministic; flicker scan 0 frames.
- Sound rebuilt with `remezclar.py` to -14.1 LUFS (peak -4.4 dBFS); music 24 dB under the voices, 16 dB under them in the gaps.
- Mix transcription: every line clear ("Comentá BATATA" read as written).
- The ocarina plays the opening of "Oda a la alegría" (synthesised; badge "Sonido digital"); it ends in El Mago's hand for the product beat and the CTA.

### Music from the owner's score (2026-11-15, second mix)

The ambient bed was replaced by music made from the owner's score p01 (la menor, ♩=130), bars 5-18 (`../biblioteca/partituras/`, used with the owner's
permission), with `../biblioteca/partitura_synth.py`: a soft music box, a pad and a bass, ducked under the voices and out
under the ocarina. Rebuild: `bash ../ocarina/build_reel.sh "a1 a2 a3 a4 a5" "oda" "p01-la-menor-130 5-18 1.0"`, then `remezclar.py` (the picture is byte-identical).
Levels: music -23.0 dB under the voices, -14.7 dB in the gaps; -14.1 LUFS; every line clear in the mix transcription.

### The band (2026-11-15, third mix)

The owner found the music-box version too empty and asked for piano, percussion, bass, a synthesiser and a theremin. Now
`../biblioteca/partitura_banda.py` plays the same score as a band: the piano (melody and chords on each beat), a soft drum
groove, the bass, a detuned saw pad and a theremin that carries the melody in the gaps between spoken lines (out under the
voices; the piano carries it there). Everything ducks under the voices and is out under the ocarina; +2.5 dB over the old
bed. Levels: music -22.1 dB under the voices, -11.9 dB in the gaps; -14.1 LUFS; every line clear in the mix transcription.

### Exact notes (2026-11-15, fourth mix)

The band now plays the owner's exact transcription (`../biblioteca/partituras/transcripciones-del-duenio.txt`): score args `p01-la-menor-130 5-24 1.0`. -14.1 LUFS; every line clear.

### No badge (2026-11-15)

The owner asked to remove the "Sonido digital" badge and the "Ilustración 3D · sonido digital" line ("queda super implícito"); the caption keeps "El video es una animación."

### More "ocarina" (2026-11-17)

The owner asked for more "ocarina hecha en 3D" and the word "ocarina" more often: the hook, product beat and card say "Ocarina hecha en 3D"; most lines now name the ocarina (new takes `../ocarina/voz2`, `voz3`; "esa ocarina" and "tu ocarina" were heard as "eso, Karina" and were reworded); the caption follows. Re-timed, re-rendered.

## Resultado 17/11/2026: más "ocarina hecha en 3D"

Render final con el texto nuevo: QA 0 cuadros malos, flicker 0, mezcla a -14 LUFS, todas las líneas claras en la transcripción de la mezcla.
