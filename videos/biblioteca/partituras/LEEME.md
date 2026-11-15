# Partituras del dueño (música para los reels)

El dueño las mandó el 15/11/2026 con este mensaje: "Estas son partituras a las que me ha dado permiso usar. En base a estas
partituras crea la musica para estos reels te voy a estar dando mas partituras en un futuro. Todas las que te doy es porque
tengo permiso usarlas y guardalas en la memoria para usar en futuros casos o reels".

**Regla:** las partituras de esta carpeta se pueden usar como música de los reels (el permiso es del dueño). Cuando lleguen
partituras nuevas, se guardan acá con el mismo formato y se anotan en la tabla.

| Archivo | Qué es | Imagen | Usada en |
|---|---|---|---|
| `p01-la-menor-130.json` | "Main Theme Easy" (Koji Kondo), la menor, 4/4, ♩=130, los 24 compases | `p01-la-menor-130.png` | La batata |
| `p02-vals-la-menor.json` | "Kass' Theme" (Kataoka, Iwata; arr. StefCopp), la menor, 3/4, ♩=170, compases 1-16 y 19-34 | `p02-vals-la-menor-a.png`, `-b.png` | Doce agujeros |
| `p03-sol-menor-155.json` | "The Great Fairy Fountain" (Koji Kondo; arr. saltandlight02), sol menor, 2/2, ♩=155, los 16 compases | `p03-sol-menor-155.png` | El ensayo (al 80 % del tempo) |
| `p04-sol-menor-60.json` | "Great Fairy Fountain", estudio para piano (arr. Erik C), sol menor, 4/4, ♩=60, compases 1-10 | `p04-sol-menor-60.png` | El piano |
| (misma pieza, más páginas) | Continuación de la pieza 4, recibida el 15/11: compases 11-18 (pág. 2), 19-23 (pág. 3), 24-29 con el cambio a 6/4 y 2/2 (pág. 4), 30-34 *maestoso*, *ff* (pág. 5), 39-48 hasta *fff* (pág. 7). Aún sin transcribir: se pasa a JSON cuando un reel la use. Los compases marcados en rosa (15, 22, 42) vienen así en las imágenes | `p04-sol-menor-60-pag2.png` … `-pag7.png` | — |

**Formato:** `bpm`, `beats_per_bar` y una lista de compases, cada uno con `mel` (nota y duración en negras; `"r"` es
silencio), y `chord` (las notas del acorde del compás) o `bass` (la línea del bajo).

**Transcripciones exactas:** el dueño mandó `transcripciones-del-duenio.txt` (15/11) con las notas de cada partitura; los JSON se pasaron de ahí (campo `exact`). Las páginas pagas de MuseScore no están incluidas.

**Con banda (15/11, a pedido del dueño: "la música se siente muy vacía"):** `../partitura_banda.py` toca la partitura con piano, batería, bajo, sintetizador y theremin (el theremin lleva la melodía entre las líneas habladas y se corre debajo de las voces). Es la versión que usan los reels de la ocarina.

**Cómo se usan (versión simple, cajita de música):** `python3 ../partitura_synth.py partituras/<pieza>.json <reel>/cues.json <reel>/hf3d/assets/audio/music.wav --ref <bed anterior> --bars A-B --tempo T`,
o el tercer argumento de `videos/ocarina/build_reel.sh`. La música queda suave, por debajo de las voces (20-25 dB) y se
corta debajo de la ocarina; se revisa con `nivel_musica.py` y la transcripción de la mezcla.
