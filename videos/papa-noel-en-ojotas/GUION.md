# Papá Noel en ojotas (reel de Navidad, 15 s)

Reel vertical 1080×1920, 15 s, pixel art 16 bits, cámara fija en el taller del Mago. Sin texto en pantalla: el mensaje va en el caption.

## La idea

En pleno verano uruguayo, Papá Noel entra al taller derretido de calor y con la bolsa vacía. El Mago le convida un mate, prende la impresora y le llena la bolsa de regalos impresos en 3D, empezando por los clickers para el amigo invisible.

### Cómo se eligió

Tres subagentes trabajaron en paralelo: historia, gancho comercial y biblioteca de sprites.

- **Historia**: de 5 conceptos, el recomendado fue *Papá Noel en ojotas*, por el chiste local del verano y porque usa solo dos personajes. Lo llevé al **taller con la impresora**: así el regalo sale de la impresora 3D, que es lo que se vende, y el taller queda como escenario fijo para próximos reels.
- **Marketing**: el ángulo más fuerte es el **amigo invisible**. Tiene fecha fija, empuja a pedir temprano (por el mínimo de 48 h) y un solo comprador resuelve todo el grupo con clickers. Por eso el primer regalo que sale de la impresora es el combo de clickers.
- **Los productos de juegos**: la alcancía Creeper, la caja tipo Game Boy, el dragón y el bloque de TNT son los de mejor silueta según el análisis de marketing. Entran todos, y el TNT es el remate del pico. En los prompts se piden sin logos ni texto: la silueta y los colores alcanzan para reconocerlos.

## Escenario y posiciones

Taller visto desde arriba a tres cuartos, en la grilla de 270×480 px de arte (×4):

```
 y
 40 ┌───────────────────────────────┐  pared de madera
    │ estantes      ventana  guirn. │  ventana con cielo de verano, sol y rama de plátano
150 │ [mesa+impresora]        árbol │  arbolito de Navidad en el rincón derecho
    │                         puerta│  puerta en la pared derecha (238, 262)
240 │  Mago en la mesa (80,240)     │
    │          alfombra             │
330 │ventilador   Mago (160,336) ◯  │  banquito (210, 340), bolsa (176, 352)
430 ├───────────────────────────────┤
480 └ baldosas terracota y crema ───┘
```

## Beats

| Tiempo | El Mago | Papá Noel | Objetos y efectos | Sonido |
|---|---|---|---|---|
| **0,0–0,25** gancho | En la mesa, de espaldas, apretando la impresora | | La puerta se abre de golpe; nube de polvo | Portazo |
| 0,25–1,35 | Se da vuelta (0,5 s) y se sorprende (0,8 s) | Entra arrastrando las ojotas, transpirado, hasta el banquito | Gotas de sudor | Flip-flop de ojotas, "¡uh!" chiptune |
| 1,35–1,75 | Sorprendido (queda) | Se desploma en el banquito | Polvo bajo el banquito | Plop con rebote |
| 1,75–3,2 | Camina hasta él | Se abanica con el gorro | Sudor; el ventilador gira todo el reel | Pasos |
| 3,2–3,7 | Le ofrece el mate | Se abanica | | |
| 3,7–4,4 | Reposo, sin mate | Toma mate, abre los ojos | | Sorbo |
| 4,4–5,0 | Recibe el mate y toma | Alivio, sonrisa, devuelve el mate | Destello sobre Papá Noel | "Aaah" en arpegio |
| 5,0–5,8 | Toma mate | Da vuelta la bolsa vacía y la sacude | Sale una polilla | Sacudón, aleteo cómico |
| 5,8–6,4 | Piensa | Triste, con la bolsa en la falda | | Nota triste |
| 6,4–6,9 | ¡Idea! | | Lamparita sobre el Mago | Ding de idea |
| 6,9–7,6 | Vuelve a la mesa y se da vuelta | | | Pasos |
| 7,6–8,4 | Aprieta el botón | | La impresora imprime (2 cuadros en bucle) | Zumbido de impresora chiptune |
| **8,4–9,2** pico | Se da vuelta; levanta los 4 clickers juntos ("item get") y los tira a la bolsa | Mira | Destello en la impresora; los clickers (café, banana, suculenta, hámster) vuelan en 4 pasos; la bolsa pasa a 1/3 | Ding, "item get", whoosh, plop |
| 9,2–10,0 | "Item get" con la alcancía Creeper, la tira | Sonríe | Destello; Creeper a la bolsa | "Item get" un tono más agudo |
| 10,0–10,8 | Brazos en alto, maravillado | Sonríe | **Ráfaga**: la impresora escupe 8 productos seguidos directo a la bolsa (caja Game Boy, dragón, Ferrari F40, garaje de autitos, ajedrez de viaje, comedero hoja, estadio de Peñarol, estadio de Nacional); la bolsa pasa a 2/3 | 8 pops ascendentes |
| 10,8–11,6 | "Item get" con el **bloque de TNT**, la mecha chispea; lo tira | Salta del susto | El TNT cae en la bolsa, que se llena y suelta polvo y confeti | Mecha, "¡uy!", boom ahogado |
| 11,6–12,8 | Salto de alegría | Salto de alegría | Confeti y corazones | Acorde de victoria |
| 12,8–13,3 | Reposo | Se carga la bolsa al hombro | | Esfuerzo chiptune |
| 13,3–14,0 | Saluda | Sale por la puerta saludando; la puerta se cierra | | Ojotas, puerta |
| 14,0–15,0 | Toma mate y se queda quieto (último 0,4 s fijo) | | Las luces del arbolito titilan | Acorde final suave |

**Ambiente durante todo el reel:** el ventilador gira (12 fps) y la guirnalda y el arbolito titilan (2 fps). Suena una melodía chiptune liviana en tono mayor, con el motivo de *Jingle Bells* (dominio público) en arreglo propio, y chicharras de fondo (verano).

## Prueba de armado (antes de animar)

Con las hojas aprobadas, Claude compone estos 6 cuadros con el fondo y los sprites y los revisa antes de tocar HyperFrames:

1. **0,3 s**: puerta abierta, Papá Noel entrando, Mago dándose vuelta.
2. **3,9 s**: Papá Noel sentado tomando mate, Mago al lado.
3. **5,4 s**: bolsa dada vuelta, polilla, Mago con mate.
4. **9,0 s**: Mago con los clickers en alto, impresora destellando, bolsa vacía.
5. **12,0 s**: los dos en el aire, confeti, bolsa llena.
6. **15,0 s**: Mago solo tomando mate, puerta cerrada.

## Lo que hay que pedirle a Gemini

`PROMPTS.md` tiene los **50 prompts** de este reel, en orden de aprobación:

- **2 model sheets**: El Mago y Papá Noel de verano.
- **2 imágenes del escenario**: la maestra del taller y el fondo vacío.
- **32 hojas de animación**: 14 animaciones del Mago (17 hojas) y 12 de Papá Noel (15 hojas). Las de 6 cuadros van en 2 hojas.
- **6 hojas de objetos y adornos**: impresora, puerta, bolsa, guirnalda, una hoja con banquito, ventilador, mate y arbolito, y otra con la corona.
- **3 hojas de efectos** con los 12 efectos de la biblioteca (el reel usa 7).
- **5 hojas de ítems** (de a 4) con los 14 productos del reel y algunos más de la biblioteca, adjuntando las fotos reales de `assets/p/`.

Todo lo que se apruebe queda en la biblioteca: el próximo reel del Mago ya tiene el taller, la impresora, los efectos y 14 animaciones hechas.

## Caption para Instagram

Versión 3D (2026-11-07). Salió de tres redactores (subagentes Haiku: humor, urgencia práctica y voz de personaje); se
eligió y se pulió a mano: gancho de menos de 110 caracteres, primera persona como en la web, solo datos reales.

**Principal**

```
En Montevideo, en diciembre, hasta Papá Noel se derrite. 🥵

Llegó al taller en ojotas, con la bolsa vacía y una polilla de compañía. El Mago le dio un mate 🧉, prendió la impresora y salvó la Navidad: clickers, una alcancía, ocho regalos más y un TNT que explota en confeti.

¿Amigo invisible en el laburo y cero ideas? Te lo imprimo yo 🎁
Escribime al 092 104 419 con una foto o el link de MakerWorld y te paso precio y fecha, sin compromiso. Cada pedido lleva mínimo 48 horas: no lo dejes para el 23.
Entrego sin costo en La Unión, La Blanqueada y parte de Buceo, y mando a todo Uruguay.

#Montevideo #RegalosDeNavidad #AmigoInvisible #Impresion3D #HechoEnUruguay #RegalosOriginales #CreacionesDelMago
```

**Alternativa: diario del Mago**

```
Diario del Mago, diciembre: entró Papá Noel en ojotas, derretido. 🧙

Le di un mate. Sacudió la bolsa: vacía. «¡Me quedé sin regalos!»
Tuve una idea: ¡a imprimir! La impresora escupió clickers, una alcancía y un TNT que explotó en confeti 🎉
Se fue diciendo «¡Jo, jo, jo!». Yo me quedé con el mate.

¿Te falta un regalo? Escribime al 092 104 419 y te paso precio y fecha, sin compromiso. Mínimo 48 horas.
Entrego sin costo en La Unión, La Blanqueada y parte de Buceo, y mando a todo Uruguay.

#Navidad #RegalosUruguay #Impresion3D #Montevideo #ElMago #CreacionesDelMago
```

**Alternativa: diálogo**

```
Papá Noel: —¡Me quedé sin regalos! 😱
El Mago: —Tomá un mate. Tengo una idea.
Papá Noel: —¿Cuál?
El Mago: —¡A imprimir! 🖨️

Moraleja: si te quedaste corto de regalos, no te estreses. Y si el calor de diciembre te tiene sin ganas de nada, primero un matecito. 🧉

Escribime al 092 104 419: te paso precio y fecha, sin compromiso. Cada pedido lleva mínimo 48 horas.
Entrego sin costo en La Unión, La Blanqueada y parte de Buceo, y mando a todo Uruguay.

#RegalosDeNavidad #Impresion3D #Montevideo #AmigoInvisible #HechoEnUruguay #CreacionesDelMago
```

Versión anterior (pixel art): "Papá Noel llegó al taller derretido y con la bolsa vacía. Por suerte la impresora no se toma vacaciones…"

## Estado

- **Animatic listo**: `animatic.mp4` es el reel completo con figuras provisorias, con el timing y el audio definitivos. Se arma con la skill `pixel-reel` (ver `skills/pixel-reel/SKILL.md`).
- **Falta**: las hojas reales de Gemini. Cada una que se aprueba va a `videos/biblioteca/sheets/` con su nombre. Después se vuelve a ensamblar y renderizar, sin tocar la línea de tiempo:

```bash
python3 skills/pixel-reel/scripts/assemble.py videos/biblioteca/sprites.json videos/biblioteca/sheets:videos/papa-noel-en-ojotas/placeholder-sheets videos/papa-noel-en-ojotas/reel.json videos/papa-noel-en-ojotas/hf
```

```bash
cd videos/papa-noel-en-ojotas/hf && npx hyperframes render -o ../papa-noel-en-ojotas.mp4
```

Para regenerar las provisorias (no se versionan): `python3 skills/pixel-reel/scripts/placeholders.py videos/biblioteca/sprites.json videos/papa-noel-en-ojotas/placeholder-sheets --reel videos/papa-noel-en-ojotas/reel.json`.

## Versión 3D toon (2026-11-07)

El usuario eligió la dirección 3D toon. La misma historia en 21 s (en 3D cada acción necesita un poco más de tiempo para leerse), con voces, subtítulos y placa final; cinco planos cortados en la acción. Proyecto: `hf3d/` (armado con `build3d.sh`), audio `cues3d.json`, voces `voces3d.json` → `voz3d/`, render `papa-noel-en-ojotas-3d.mp4`.

| Tiempo | Plano | Qué pasa |
|---|---|---|
| 0,0–3,2 | General, se acerca despacio | La puerta se abre de golpe (polvo, entra la luz del verano). El Mago, en la impresora, se da vuelta sorprendido. Papá Noel entra arrastrando las ojotas, transpirado, con la bolsa a la espalda, y se desploma en el banquito (aplaste); la bolsa cae al lado |
| 3,2–8,0 | Dos personajes | Papá Noel se abanica. El Mago llega con el mate y se lo ofrece; Papá Noel toma, alivio (se le bajan los lentes), lo devuelve y el Mago toma. Papá Noel da vuelta la bolsa vacía y la sacude: sale una polilla. Tristeza; el Mago piensa y salta con la idea (lamparita) |
| 8,0–12,5 | Impresora y bolsa | El Mago vuelve a la impresora y aprieta. Presenta los cuatro clickers delante de la cara y los tira a la bolsa; después la alcancía Creeper; la impresora escupe ocho productos seguidos; el TNT con la mecha chispeando: Papá Noel salta del susto, cae en la bolsa y explota en confeti |
| 12,5–17,95 | General final | Festejo (el Mago baila, Papá Noel se levanta con los brazos arriba). Papá Noel se carga la bolsa al hombro, camina hacia la puerta y saluda desde adentro del taller. Se da vuelta, se pasa la bolsa a la espalda y sale derecho por el medio de la puerta; la puerta (abre hacia adentro) se cierra detrás de él. El mate vuela solo del estante a la mano del Mago (magia) y toma |
| 17,95–21,0 | El Mago de frente | El Mago baja el mate y le habla a cámara. Placa final: "Regalos impresos en 3D · ¡Pedí el tuyo! · Escribime por mensaje · Creaciones del Mago · Montevideo" (sin teléfono en el video; el número va en el caption) |

### Versión 2 (2026-11-07): misma animación, voces y sonido; otra cámara y otra edición

`hf3d-v2/` (mismo `build3d.sh`), render `papa-noel-en-ojotas-3d-v2.mp4`. Lo único que cambia es la cámara y la edición, así que la animación y el sonido son los mismos de la V1 (la puerta de calidad da lo mismo).
- 16 planos en vez de 5, cortados en la acción y en el diálogo: picado desde abajo a la puerta, primer plano del Mago sorprendido, travelling siguiendo a Papá Noel, plano a dos desde abajo para el mate, primer plano del "¡Ahh…!", picado desde arriba sobre la bolsa vacía, contrapicado del Mago con la idea, plano desde detrás de la impresora para "¡A imprimir!", plano holandés del TNT, contrapicado del festejo, plano profundo con el Mago en primer término mientras Papá Noel se va.
- Los planos de personajes se encuadran midiendo la cabeza en la pose (altura de cuadro en metros, ángulo y elevación), no con coordenadas a ojo: así no salen ni demasiado cerca ni tapados.
- Zooms de golpe (sorpresa, idea, explosión), barridos con desenfoque en tres cortes, sacudón de cámara (portazo, desplome, explosión, puerta), destello blanco en la explosión.
- Subtítulos cinéticos: palabra por palabra al ritmo de la voz, la palabra que se dice en el color del personaje. Título gancho al principio: "Papá Noel vs. el diciembre uruguayo".
- Regla nueva: el set no tiene pared delantera, así que todas las cámaras miran hacia el fondo o las paredes laterales; el árbol de adelante y la hoja abierta de la puerta tapan algunos ángulos (revisar cuadros antes de renderizar).

### Diálogo (voces con Gemini TTS)

Papá Noel: voz Algenib (grave, un poco rasposa, gordo bonachón). El Mago: voz Charon (la misma del reel del jardín). Acento rioplatense de Montevideo. Cada personaje se grabó en UNA sola toma (las líneas cortas solas salen mal) y se cortó en las pausas con `biblioteca/tts_lineas.py`; recortes y volumen parejo (-16 LUFS) en `voces3d.json` → `_edits`. La música baja debajo de cada línea. Mientras habla, cada personaje asiente al ritmo de su voz (envolvente de volumen, sin boca: la tapa la barba).

| Entra | Quién | Línea (subtítulo) | Momento |
|---|---|---|---|
| 0,85 | Papá Noel | ¡Uf… qué calor, che! | Entra derretido |
| 3,6 | El Mago | Tomá, un matecito. | Le ofrece el mate |
| 5,08 | Papá Noel | ¡Ahh…! | Alivio después del sorbo |
| 6,29 | Papá Noel | ¡Me quedé sin regalos! | Sacude la bolsa vacía |
| 7,9 | El Mago | ¡Tengo una idea! | Salta con la lamparita |
| 9,18 | El Mago | ¡A imprimir! | Aprieta el botón de la impresora |
| 12,68 | Papá Noel | ¡Jo, jo, jo! ¡Gracias, Mago! | Festejo después del confeti |
| 15,45 | Papá Noel | ¡Feliz Navidad! | Saluda antes de irse |
| 17,9 | El Mago | Regalos impresos en 3D. ¡Pedí el tuyo! | Placa final (sin subtítulo: la placa dice lo mismo) |

Subtítulos: una píldora por línea con el color de cada personaje (Papá Noel rojo, el Mago violeta con letra dorada), letra Fredoka, dentro de la zona segura de Instagram (ni los 220 px de arriba ni los 450 de abajo).
