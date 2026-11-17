# Doce agujeros (ocarina reel O2, consideration; script in `../PLAN_OCARINA.md`)

Publish: Wed 2/12. CTA keyword: DOCE (reward: price and date). Sound: synthesised (`../biblioteca/ocarina_synth.py`),
labelled "Sonido digital" on screen; the ocarina is a 3D illustration (the owner's decision, 15/11/2026).

## Caption (curated from the three caption writers: humour, practical, character)

```
Papá Noel cree que a mi ocarina hecha en 3D se le escapa el aire. Son doce agujeros, no un colador. 🎶

Ocarina de 12 agujeros, hecha en 3D en Montevideo: 10 arriba y 2 para los pulgares.
En la ocarina, cada agujero que destapás es otra nota. ¿Y la ocarina se aprende? Si alguna vez tocaste flauta dulce, ya sabés la idea.
La hago a pedido.
El video es una animación.
¿Cuántos agujeros tiene la ocarina? Comentá DOCE y te paso precio y fecha.
Precio y fecha por WhatsApp al 092 104 419, antes de empezar y sin compromiso.
Envío gratis solo en La Unión, La Blanqueada y parte de Buceo; mando a todo Uruguay.
Pedidos para Navidad: hasta el 23 de diciembre.

#Montevideo #Uruguay #impresion3d #ocarina #flautadulce #regalosdenavidad
```

## DM (private reply to whoever comments DOCE)

```
¡Hola! Gracias por comentar DOCE 🎶
¿Para quién es la ocarina? ¿Ya toca algo o arranca de cero?
Te paso precio y fecha por WhatsApp, antes de empezar y sin compromiso.
```

## Result (2026-11-15)

`doce-agujeros.mp4`: 24.65 s, 1080×1920, 60 fps.
- QA gate 0/1479 bad frames, 0 jumps, deterministic; flicker scan 0 frames.
- Sound rebuilt with `remezclar.py` to -14.1 LUFS (peak -4.2 dBFS); music 25 dB under the voices, 18 dB under them in the gaps.
- Mix transcription: every line clear.
- The scale (synthesised, "Sonido digital") climbs as each gold cap pops off a hole; the product beat turns it over (10 on top, 2 for the thumbs); it floats back to Papá Noel's mittens for the CTA.

### Music from the owner's score (2026-11-15, second mix)

The ambient bed was replaced by music made from the owner's score p02 (vals en la menor, 3/4), bars 1-13 (`../biblioteca/partituras/`, used with the owner's
permission), with `../biblioteca/partitura_synth.py`: a soft music box, a pad and a bass, ducked under the voices and out
under the ocarina. Rebuild: `bash ../ocarina/build_reel.sh "b1 b2 b3 b4 b5" "escala" "p02-vals-la-menor 1-13 1.0"`, then `remezclar.py` (the picture is byte-identical).
Levels: music -24.1 dB under the voices, -16.6 dB in the gaps; -14.1 LUFS; every line clear in the mix transcription.

### The band (2026-11-15, third mix)

The owner found the music-box version too empty and asked for piano, percussion, bass, a synthesiser and a theremin. Now
`../biblioteca/partitura_banda.py` plays the same score as a band: the piano (melody and chords on each beat), a soft drum
groove, the bass, a detuned saw pad and a theremin that carries the melody in the gaps between spoken lines (out under the
voices; the piano carries it there). Everything ducks under the voices and is out under the ocarina; +2.5 dB over the old
bed. Levels: music -23.0 dB under the voices, -13.7 dB in the gaps; -14.1 LUFS; every line clear in the mix transcription.

### Exact notes (2026-11-15, fourth mix)

The band now plays the owner's exact transcription (`../biblioteca/partituras/transcripciones-del-duenio.txt`): score args `p02-vals-la-menor 1-34 0.85`. -14.1 LUFS; every line clear.

### No badge (2026-11-15)

The owner asked to remove the "Sonido digital" badge and the "Ilustración 3D · sonido digital" line ("queda super implícito"); the caption keeps "El video es una animación."

### More "ocarina" (2026-11-17)

The owner asked for more "ocarina hecha en 3D" and the word "ocarina" more often: the hook, product beat and card say "Ocarina hecha en 3D"; most lines now name the ocarina (new takes `../ocarina/voz2`, `voz3`; "esa ocarina" and "tu ocarina" were heard as "eso, Karina" and were reworded); the caption follows. Re-timed, re-rendered.
