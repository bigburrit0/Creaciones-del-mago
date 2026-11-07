# Catálogo "lite": investigación y decisiones (v10, 7/11/2026)

Pedido del dueño: actualizar el catálogo con las fotos de los ajedrez vendidos, que sea más fácil
llegar al fondo y pedir o hablar por WhatsApp, y poner el foco en los ajedrez, que es el nicho que
mejor le funciona.

Base: cuatro investigaciones en paralelo (diseño de catálogo para celular, flujo hacia WhatsApp,
venta de ajedrez, arreglo de fotos de celular). [E] = estudio o dato verificable, [P] = práctica de
expertos o de tiendas, [D] = evidencia débil o de una sola fuente.

**Aviso de evidencia:** la red de la sesión no dejó abrir Baymard, Nielsen Norman Group, House of
Staunton ni Chess Bazaar. Lo de esas fuentes sale de resúmenes de búsqueda; las cifras de
conversión son de agencias y vendedores. Sirven para elegir dirección, no para prometer números.

## Lo que coincide entre las cuatro

1. **Un camino a WhatsApp siempre a mano en el celular.** Barra fija abajo con el contador del
   pedido y el botón. Tests A/B de agencias: +8 a +9 % de conversión con barra fija en celular, con
   la contra de que puede bajar el ingreso por visitante si empuja compras chicas [P]
   (zipify.com/mobile-sticky-button-split-test-results, blendcommerce.com). No tapar contenido ni el
   pie [P].
2. **Menos productos de entrada.** No mostrar los 90 juntos. Baymard: la cantidad ideal varía mucho
   según producto y dispositivo; conviene cargar menos y dejar ver más [E en el principio, D en el
   número]. Filas que se deslizan de costado, con la tarjeta siguiente asomando, para los estantes
   secundarios [P]. Nada de carruseles que pasan solos (casi nadie los usa: Runyon 2013) [E débil].
3. **El nicho estrella arriba, sin esconder el resto.** Sección propia de ajedrez primero, con un
   "ver todos", y el resto del catálogo abajo con su navegación [P].
4. **"Armá el tuyo".** Un mensaje pre-armado con tema, colores y tablero baja el esfuerzo del
   primer mensaje; es el mismo patrón que usan las tiendas de ajedrez personalizado
   (chesshouse.com/collections/personalized-chess-boards) [P].
5. **Fotos reales primero.** La foto de portada de un ajedrez: el juego completo en el tablero, en
   posición inicial; después detalle del rey y el caballo, y algo para dar escala [P]. Etsy (oct.
   2026) pide al menos una foto sin editar del objeto real [P, fuente secundaria].
6. **Mensaje corto y codificado:** producto, colores y "¿me pasás precio y para cuándo?", un solo
   `?text=` codificado con `encodeURIComponent` [P]. Ya era así.

## Qué se hizo (v10)

| Recomendación | Hecho en la página |
|---|---|
| Nicho estrella primero | Ajedrez es el primer estante del menú y del catálogo, y tiene link propio arriba ("Ajedrez"). Muestra una fila más que los demás (12 en compu, 6 en celular) y "Ver los 15". |
| Fotos reales | 7 productos de ajedrez con fotos propias de juegos vendidos, más contador de Magic, casita, comedero élfico, repisa y ascensor. La foto del diseñador queda como una más en la galería. |
| Galería con colores | Tocar la foto abre la ventana con todas las fotos del producto y qué muestra cada una ("Negro contra dorado", "Plateado contra negro"...). En la tarjeta, un número con una camarita dice cuántas hay. |
| "Armá el tuyo" | Bloque al final del estante: juego, color de cada bando y tablero. El link de WhatsApp se arma solo (funciona también sin JavaScript, con la opción por defecto). |
| Catálogo lite en celular | Los otros 8 estantes son filas que se deslizan de costado, con la tarjeta siguiente asomando y "Deslizá para ver los N". La página en celular bajó de unas 22 a unas 19 pantallas, y el ajedrez quedó en la pantalla 2 (antes en la 7). |
| WhatsApp a mano | En celular, la barra de pedido aparece apenas empezás el catálogo, aunque no hayas elegido nada ("Tocá «Lo quiero»" + "Escribime"). Con cosas elegidas: "N cosas" + "Mandar pedido". Se esconde sola al llegar al mostrador del final. |

## Qué no se hizo, y por qué

- **"Lo más pedido" / "más vendido":** no hay datos de ventas por producto. Prohibido inventarlo
  (COPY-RULES 8). Si el dueño cuenta cuáles vende más, se puede ordenar el estante por eso.
- **Altura del rey en cada tarjeta:** es el dato que más busca el comprador de ajedrez [P], pero no
  está medido. Pendiente: medir el rey de cada juego vendido y sumarlo a la línea.
- **Medir clics en WhatsApp:** un link wa.me no cuenta nada. Se podría sumar analítica, pero la
  página hoy no tiene ninguna y eso es decisión del dueño.
- **Ajedrez con marcas (Harry Potter, Star Wars, Minecraft):** se dejaron como estaban. Los
  vendedores que los usan corren riesgo de reclamo del dueño de la marca [D]. Conviene consultarlo.
- **Catálogo de WhatsApp Business:** con ~90 productos y sin carrito propio, no reemplaza a la
  página [D].

## Para la próxima

- Medir el rey de cada ajedrez vendido (cm) y sumarlo a la tarjeta.
- Fotos nuevas mandadas como documento (ver `fotos/IMAGENES-ANTIGRAVITY.md`).
- Confirmar el contador de vidas para Magic (nombre y si hay otros colores de maná).
