# Auditoría de música y efectos (15/11/2026)

Pedido del dueño: «La música no tiene mucho sentido. Hacé un audit y que los reels tengan música acorde a los videos y la
temática. Además los videos tienen que tener sound effects humorísticos y que estén trending.»

## Qué hay hoy

| Reel | Música | Efectos | Problema |
|---|---|---|---|
| ¿Vikingo o caballero? | colchón «ambient» (pads lentos, re dórico) | clacks, campanas, «lur» de 8 bits | una batalla con fondo de spa |
| Un regalo para cada amigo | ambient (do mayor) | pops, clicks, taps de 8 bits | una vidriera de regalos sin ritmo |
| Una más | ambient (mi menor) | clacks, impresora, ronquido de 8 bits | la noche que pasa no se oye; no hay reloj ni amanecer |
| Elegí tu bando | ambient (re dórico) | brillos, taps | pintar y personalizar sin alegría |
| Papá Noel en ojotas | chiptune de videojuego (volumen 0,45) | 25 efectos de 8 bits | el estilo que el dueño encontró «alto y molesto» |
| Las preguntas de Papá Noel | ambient (mi menor) | papel, campanas | el juego de preguntas no suena a concurso |
| Culpa de las piezas | ambient (mi menor) | taps, «sting» | el duelo y la culpa no tienen drama |
| Los gatos tiran todo | ambient (do mayor) | taps, un «plop» | el gato tramposo no tiene música de travesura; la caída no tiene remate |
| Invisible no era | chiptune (0,45) + chicharras, grillos, pájaros | silbidos de 8 bits | misión secreta de madrugada sin suspenso |
| La gaviota | ambient (sol mixolidio) | graznidos de 8 bits | el robo no corta la música; la venganza no tiene remate |
| El laberinto | ambient (re dórico) | un golpe, whooshes | Minotauro contra Hércules sin épica |
| El mantel | ambient (do mayor) | taps, un pop | Nochebuena sin nada navideño |

**Diagnóstico:**
1. **Diez reels comparten el mismo colchón:** acordes lentos a 120 bpm que solo cambian de tonalidad. No sigue la historia, no tiene ritmo ni género, no se frena en los chistes y no crece en las revelaciones. Por eso «no tiene sentido»: es la misma música para una batalla, un gato, una playa y Nochebuena.
2. **Los tres reels más viejos** usan chiptune de 8 bits, el sonido que el dueño ya había encontrado molesto.
3. **Los efectos son pitidos de 8 bits** (taps, pops, clicks). Marcan las acciones pero no hacen reír: los remates no tienen ningún efecto cómico (el gato que tira el peón, la gaviota que roba el rey, «Las piezas no pierden. Vos sí.», el peón que se cae en el pliegue).

## Qué está de moda (búsqueda del 15/11/2026)

- **Lo más usado sigue siendo:**
  - el **«Vine Boom»**, un golpe grave con eco para revelaciones y caras de sorpresa;
  - el **caño de metal que cae**, para caídas y desastres;
  - el **«rizz»**, para cuando alguien se agranda;
  - los audios de reacción («bruh», «emotional damage»).
- **Siguen vigentes los clásicos del humor:** el rayón de disco (record scratch) que frena todo, el trombón triste («wah wah waaah»), el «dun dun duuun», la claque de redoblante (ba-dum-tss), los grillos del silencio incómodo, el «boing», la sirena de payaso y el «ka-ching» de la caja registradora.
- **Licencias:** esos audios virales son grabaciones de terceros y una cuenta de negocio no los puede usar tal cual (Instagram restringe la música comercial en cuentas de empresa). Los hago **originales y con la misma función**: un golpe grave con eco, un caño que rebota, un rayón de disco, un trombón triste… sintetizados acá, sin copiar ninguna grabación.
- **Para un audio de moda de verdad** (una canción del momento), lo correcto es elegirlo en Instagram al publicar, desde su biblioteca con licencia. Si el dueño quiere, se entrega además una versión de cada reel **sin música** (voces y efectos), para sumarle ese audio en la app.

Fuentes:
- [Later, tendencias de Reels](https://later.com/blog/instagram-reels-trends/)
- [Best US Viral Meme Sounds 2026](https://myinstantplay.com/blog/best-us-viral-meme-sounds-tiktok-reels-shorts-2026)
- [Top 100 meme sounds en Reels 2026](https://myinstantplay.com/blog/top-100-viral-meme-sounds-instagram-reels-2026)
- [Dubbing AI, directorio de efectos de TikTok](https://dubbingai.io/articles/en/collection/trending-tiktok-sound-effects-memes)
- [que.es, audios virales de Reels, julio de 2026](https://www.que.es/2026/07/28/audios-virales-instagram-reels-julio-2026/)

## De dónde sale la música

- El catálogo de música de HeyGen y el banco de efectos grabados de Openverse están **bloqueados por la red** de este entorno; HeyGen además pide iniciar sesión.
- El generador de música de Google (Lyria 3) tiene **cuota 0** en el plan gratis de esta clave.
- Por eso la música y los efectos se **componen y sintetizan acá** (`videos/biblioteca/banda.py`), con instrumentos de verdad (pizzicato, marimba, bandoneón, tambores de candombe, lira, steel drum, cascabeles, metales) en vez de 8 bits.
- **Si se quiere un salto de calidad**, hay dos caminos:
  - iniciar sesión gratis en HeyGen y habilitar su acceso de red, para usar su catálogo de 10 000 temas;
  - habilitar Openverse, para efectos grabados con licencia CC0 o CC BY (con créditos).

## Reglas que se mantienen

- **Nunca un efecto sobre una palabra:** los remates van en los silencios, después de la línea (lección de «Culpa de las piezas»).
- **La música va debajo de las voces** (unos 20 dB menos mientras hablan) y respira en los silencios.
- **Pocos efectos cómicos por reel (3 a 6):** si suenan todo el tiempo dejan de ser graciosos.
- **Solo se cambia el sonido:** la imagen queda idéntica byte a byte (`remezclar.py`); no se vuelve a renderizar nada.

## Propuesta por reel

| Reel | Música nueva (original) | Efectos cómicos (en los silencios) |
|---|---|---|
| ¿Vikingo o caballero? | épica de batalla en broma: timbales, cuerdas graves en ostinato, llamadas de corno; se corta en seco en «jaque mate» | golpe grave al mate, rayón de disco cuando Papá Noel entiende «mate», «ba-dum-tss» al final |
| Un regalo para cada amigo | vidriera saltarina: pizzicato, marimba y palmas, do mayor | «pop» por regalo, «boing», brillo «rizz» para la banana con lentes |
| Una más | nana de caja de música que se va durmiendo, con tic-tac de reloj; amanece con cascabeles y metales | trombón triste cuando se duerme parado, «ta-da» con las 32 piezas |
| Elegí tu bando | ukelele y glockenspiel alegres, como de taller de pintura | brillo «rizz» + golpe grave en «¡Ese rey soy yo!» |
| Papá Noel en ojotas | **candombe navideño**: tambores (chico, repique, piano) y «Jingle Bells» (dominio público) en marimba | chancletazo de ojotas, «ka-ching» con los regalos, explosión de confeti |
| Las preguntas de Papá Noel | música de concurso de TV: contrabajo caminando, escobillas y vibráfono | «ding» por pregunta, silbato que baja cuando la lista llega al piso, «ba-dum-tss» en «Las demás… en comentarios» |
| Culpa de las piezas | **tango**: bandoneón, contrabajo y cuerdas marcadas | el tango se frena con rayón de disco, «dun dun duuun» cuando las piezas lo miran, golpe grave después de «Vos sí.» |
| Los gatos tiran todo | travesura de gato: pizzicato sigiloso y clarinete en puntas de pie | la música se calla en los tres golpecitos, el peón cae con **caño de metal**, golpe grave después de «Para un gato, sí.» |
| Invisible no era | misión secreta de madrugada: bajo en ostinato, guitarra apagada, silbido de espía | rayón de disco cuando se encuentran, grillos del silencio incómodo |
| La gaviota | verano en la playa: bossa con guitarra, shaker y steel drum | **rayón de disco + la música se corta** cuando roba el rey; picotazos «bonk»; trombón triste para la gaviota |
| El laberinto | épica griega: lira, timbales, flauta en re dórico | golpe grave con el Minotauro, grillos cuando se pierde, «ba-dum-tss» después de «Se sale ganando», redoble para las cintas |
| El mantel | Nochebuena: cascabeles, celesta y pizzicato con un villancico tradicional | «bonk» del peón en el pliegue, rayón de disco en «Eso es un mantel», magia con brillo, campanita del 23 |
