# Papá Noel en ojotas (reel de Navidad, 15 s)

Reel vertical 1080×1920, 15 s, pixel art 16 bits, cámara fija en el taller del Mago. Sin texto en pantalla: el mensaje va en el caption.

## La idea

En pleno verano uruguayo, Papá Noel entra al taller derretido de calor y con la bolsa vacía. El Mago le convida un mate, prende la impresora y le llena la bolsa de regalos impresos en 3D, empezando por los clickers para el amigo invisible.

### Cómo se eligió

Tres subagentes trabajaron en paralelo: historia, gancho comercial y biblioteca de sprites.

- **Historia**: de 5 conceptos, el recomendado fue *Papá Noel en ojotas*, por el chiste local del verano y porque usa solo dos personajes. Lo llevé al **taller con la impresora**: así el regalo sale de la impresora 3D, que es lo que se vende, y el taller queda como escenario fijo para próximos reels.
- **Marketing**: el ángulo más fuerte es el **amigo invisible**. Tiene fecha fija, empuja a pedir temprano (por el mínimo de 48 h) y un solo comprador resuelve todo el grupo con clickers. Por eso el primer regalo que sale de la impresora es el combo de clickers.
- **Fuera del reel**: la alcancía Creeper, el bloque de TNT, la caja tipo Game Boy y el dragón del End. Se reconocen muy bien, pero son de marcas de terceros (Minecraft, Pokémon, Nintendo) y esto es un aviso. Se pueden sumar si lo decidís vos.

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
| **8,4–11,6** pico | 4 veces: la impresora destella, el Mago levanta el regalo "item get" (0,4 s) y lo tira hacia la bolsa (0,25 s) | Mira cómo se llena la bolsa | 1) los 4 clickers juntos (café, banana, suculenta, hámster); 2) garaje de autitos; 3) ajedrez de viaje en tubo; 4) comedero hoja. Cada uno vuela en 4 pasos y la bolsa crece: vacía, 1/3, 2/3, llena | "Item get" ascendente (cada uno un tono más agudo), whoosh, plop en la bolsa |
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

`PROMPTS.md` tiene los **45 prompts** de este reel, en orden de aprobación:

- **2 model sheets**: El Mago y Papá Noel de verano.
- **2 imágenes del escenario**: la maestra del taller y el fondo vacío.
- **28 hojas de animación**: 14 animaciones del Mago (17 hojas) y 11 de Papá Noel (14 hojas). Las de 6 cuadros van en 2 hojas.
- **6 hojas de objetos y adornos**: impresora, puerta, bolsa, guirnalda, una hoja con banquito, ventilador, mate y arbolito, y otra con la corona.
- **2 hojas de efectos**: destello, polvo, confeti, corazones, sudor, idea y polilla.
- **2 hojas de ítems**: clickers, calavera, garaje, ajedrez de viaje y comedero hoja, adjuntando las fotos reales de `assets/p/`.

Todo lo que se apruebe queda en la biblioteca: el próximo reel del Mago ya tiene el taller, la impresora, los efectos y 14 animaciones hechas.

## Caption para Instagram

> Papá Noel llegó al taller derretido y con la bolsa vacía. Por suerte la impresora no se toma vacaciones.
> ¿Amigo invisible antes del 24? Pedí con tiempo: cada pedido lleva mínimo 48 horas.
> Escribime al 092 104 419 y te paso precio y fecha, sin compromiso. Entrego sin costo en La Unión, La Blanqueada y parte de Buceo, y mando a todo Uruguay.
