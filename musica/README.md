# Base de datos de música (para reels)

Carpeta con las transcripciones de piano recibidas y los arreglos derivados para
la banda (batería, sintetizador, bajo y theremín) que se usa para generar música
de los reels.

**Importante:** la especificación exacta de la banda (rangos de cada instrumento,
reglas de mezcla, etc.) se decidió en otra sesión a la que esta sesión no tiene
acceso. Lo que hay aquí es un mapeo por defecto, documentado abajo, para no perder
las transcripciones mientras se recupera/confirma esa especificación. Si la spec
real es distinta, lo que hay que ajustar son las reglas de esta sección y volver
a generar `musica/arreglos/*.json` — las fuentes de piano (`musica/partituras/*.md`)
no cambian.

## Estructura

- `index.json` — catálogo de todas las partituras (id, compás, armadura, tempo,
  alcance/páginas visibles, y rutas a sus archivos).
- `partituras/partitura-N.md` — transcripción de piano tal cual se recibió
  (texto íntegro, misma notación: SPN, acordes entre `[]`, duraciones `w/dh/h/dq/q/d8/8/16`, etc.).
- `arreglos/partitura-N.json` — arreglo derivado para el resto de la banda, con
  esta estructura por pieza:
  - `bajo`: nota raíz (la más baja de la mano izquierda) por compás o por grupo
    de tiempos cuando el compás cambia de armonía a mitad.
  - `theremin`: línea monofónica = la nota más aguda de la mano derecha por
    compás/grupo (es la melodía principal). El theremin es monofónico, así que
    nunca toca acordes, solo esa nota, ligada/con glissando entre notas.
  - `synth`: pad sostenido con el acorde implícito de cada compás (raíz + acorde
    de la mano izquierda cuando hay acorde, o tríada de la tonalidad cuando la
    mano izquierda es una sola nota/octava).
  - `bateria`: patrón por sección, derivado de compás + tempo + acentos (>) de
    la partitura original (ver reglas abajo).

## Reglas usadas para derivar el arreglo (mapeo por defecto)

- **Bajo**: nota más grave de la mano izquierda en cada compás (o por mitad de
  compás si la armonía cambia a mitad). Duración: la de la figura dominante de
  ese compás/grupo en el original (simplificada).
- **Theremin**: nota más aguda de la mano derecha en cada compás/grupo —
  siempre una sola nota (es el instrumento solista/melódico). Si el registro de
  esa nota es muy agudo (por encima de C6), se baja una octava para quedar en el
  rango cómodo del theremin (~C3–C7).
- **Synth**: pad sostenido (nota larga) con las notas del acorde de mano
  izquierda de ese compás; si la mano izquierda solo tiene una nota u octava,
  se completa con la tríada de la tonalidad de la pieza sobre esa raíz.
- **Batería**: patrón genérico por tipo de compás, acentuado por los `(>)` del
  original:
  - 4/4: bombo (K) tiempos 1 y 3, caja (S) tiempos 2 y 4, hi-hat (H) subdividiendo
    al valor más rápido que toque la mano derecha en ese compás, platillo/crash
    (C) en cada nota marcada `(>)`.
  - 3/4: K en tiempo 1, S en tiempo 3, H subdividiendo igual que en 4/4, C en
    los acentos.
  - 3/8 / compasillo (cut time): un solo golpe fuerte de K por compás (o K-S si
    el compás se siente partido en dos), H en la subdivisión más rápida.
  - En los `accel.`/`rit.` marcados en el original, la batería agrega un relleno
    (fill) con redoble hacia el siguiente compás en vez de mantener el patrón fijo.

## Reglas de teoría musical aplicadas en las muestras de audio (`muestras/`)

El primer intento de generar `muestras/*.mp3` sonaba "raro" porque sólo tocaba
una nota estática de bajo y una de theremín por compás contra un pulso de
batería genérico, sin verificar que bajo y melodía formaran un intervalo
consonante. Se investigó teoría musical básica (líneas de bajo funcional,
notas no armónicas, contrapunto de primera especie) y se aplicaron estas
reglas en `tools/generar_muestras.py`:

- **Línea de bajo raíz-quinta ("oom-pah")**: en vez de un solo bajo sostenido
  por compás, el bajo toca la raíz del acorde en el tiempo fuerte y su quinta
  justa en el siguiente tiempo fuerte (p. ej. 4/4: raíz-raíz-quinta-raíz), que
  es la construcción básica de una línea de bajo funcional.
- **Consonancia bajo-melodía (estilo contrapunto de primera especie)**: el
  theremín debe sonar un intervalo consonante contra el bajo (unísono, 3ª,
  5ª, 6ª u 8ª). Si el intervalo cae en una disonancia dura (2ª, tritono, 7ª),
  la nota se ajusta a la nota consonante más cercana del acorde en vez de
  dejar sonar el choque.
- **Movimiento por grado/portamento en vez de saltos estáticos**: el theremín
  (monofónico) conecta cada nota estructural con la siguiente mediante un
  glissando continuo en la última parte de su duración — el equivalente de
  una nota de paso/vecina que conecta dos notas del acorde, en vez de saltar
  de golpe compás a compás.
- **Acentuación métrica en la batería**: bombo en el tiempo fuerte (tiempo 1),
  caja en el contratiempo correspondiente al compás (tiempo 2 en 3/4, mitad
  del compás en 4/4), hi-hat en cada tiempo — sigue la jerarquía métrica
  básica en vez de un patrón arbitrario.

Fuentes consultadas:
- Construcción de líneas de bajo (raíz y quinta, tonos de acorde en tiempos
  fuertes, notas de paso/vecinas entre ellos): [Lesson: Basic Line Construction Types](https://www.notreble.com/?p=5924),
  [Rhythmic and Melodic Development in the Construction of Bass Lines](https://jonburr.com/rhythmic-and-melodic-development-in-the-construction-of-bass-lines/),
  [How to Build a Jazz Walking Bass Line](https://bass.tonebase.co/blog/how-to-build-a-jazz-walking-bass-line-on-the-double-bass).
- Contrapunto de primera especie (consonancias perfectas/imperfectas,
  prohibición de quintas/octavas paralelas, preferencia por movimiento por
  grado): [The Westergaard Rules](https://westerparse.readthedocs.io/en/v2.5/speciesrules.html),
  [Open Music Theory — First Species Counterpoint](https://viva.pressbooks.pub/openmusictheory/chapter/first-species-counterpoint/).

Nota: la verificación automática cubre consonancia bajo-melodía nota a nota;
no implementa todavía una revisión completa de quintas/octavas paralelas
entre líneas consecutivas (eso queda documentado aquí como regla pendiente
para una futura mejora, no como algo ya aplicado).

## Catálogo

Ver `index.json`.
