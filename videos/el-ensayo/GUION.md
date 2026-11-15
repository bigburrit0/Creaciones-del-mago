# El ensayo (ocarina reel O4, conversion; script in `../PLAN_OCARINA.md`)

Publish: Thu 17/12. CTA keyword: NAVIDAD (reward: price and date). Sound: synthesised (`../biblioteca/ocarina_synth.py`),
labelled "Sonido digital" on screen; the ocarina is a 3D illustration (the owner's decision, 15/11/2026).

## Caption (curated from the three caption writers: humour, practical, character)

```
Papá Noel prometió tocar Noche de paz en Nochebuena. Le salió un chirrido. 🎄

Ocarina de 12 agujeros, impresa en 3D en Montevideo: 10 arriba y 2 para los pulgares.
El primer intento suena a chirrido: para eso está el ensayo.
Pedidos para Navidad: hasta el 23 de diciembre. Cuanto antes, más ensayás.
La hago a pedido.
El video es una animación: la ocarina es una ilustración 3D y el sonido es digital.
¿Quién la toca en tu casa? Comentá NAVIDAD y te paso precio y fecha.
Precio y fecha por WhatsApp al 092 104 419, antes de empezar y sin compromiso.
Envío gratis solo en La Unión, La Blanqueada y parte de Buceo; mando a todo Uruguay.

#Montevideo #Uruguay #impresion3d #ocarina #regalosdenavidad #Navidad
```

## DM (private reply to whoever comments NAVIDAD)

```
¡Hola! Gracias por comentar NAVIDAD 🎄
¿Para quién es la ocarina?
Te paso precio y fecha por WhatsApp, antes de empezar y sin compromiso. El último día para pedir es el 23 de diciembre.
```

## Result (2026-11-15)

`el-ensayo.mp4`: 24.6 s, 1080×1920, 60 fps.
- QA gate 0 bad frames (the mouthpiece checked against his face, moustache and beard every frame), 0 jumps, deterministic; flicker scan 0 frames.
- Sound rebuilt with `remezclar.py` to -14.2 LUFS (peak -4.3 dBFS); music 27 dB under the voices, 18 dB under them in the gaps.
- Mix transcription: every line clear.
- The squeak and "Noche de paz" are synthesised ("Sonido digital"); the ocarina goes back to Papá Noel's mittens for the product beat.

### Music from the owner's score (2026-11-15, second mix)

The ambient bed was replaced by music made from the owner's score p03 (sol menor, ♩=155, at 0.8 of the tempo), bars 1-8 (`../biblioteca/partituras/`, used with the owner's
permission), with `../biblioteca/partitura_synth.py`: a soft music box, a pad and a bass, ducked under the voices and out
under the ocarina. Rebuild: `bash ../ocarina/build_reel.sh "d1 d2 d3 d4" "nochedepaz chirrido" "p03-sol-menor-155 1-8 0.8"`, then `remezclar.py` (the picture is byte-identical).
Levels: music -22.4 dB under the voices, -14.5 dB in the gaps; -14.1 LUFS; every line clear in the mix transcription.

### The band (2026-11-15, third mix)

The owner found the music-box version too empty and asked for piano, percussion, bass, a synthesiser and a theremin. Now
`../biblioteca/partitura_banda.py` plays the same score as a band: the piano (melody and chords on each beat), a soft drum
groove, the bass, a detuned saw pad and a theremin that carries the melody in the gaps between spoken lines (out under the
voices; the piano carries it there). Everything ducks under the voices and is out under the ocarina; +2.5 dB over the old
bed. Levels: music -23.1 dB under the voices, -13.1 dB in the gaps; -14.1 LUFS; every line clear in the mix transcription.

### Exact notes (2026-11-15, fourth mix)

The band now plays the owner's exact transcription (`../biblioteca/partituras/transcripciones-del-duenio.txt`): score args `p03-sol-menor-155 1-16 0.8`. -14.1 LUFS; every line clear.
