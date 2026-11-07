# The shop, v5. Copy follows COPY-RULES.md: yo, voseo, a fact instead of an
# adjective, one line per item, nothing invented. Facts come from the MakerWorld
# profiles in the project docs, the v3 brief (Drive) or what the photo shows.
# Each item: (id, name, line[, whatsapp line]). "mine" = his own photos.
# "feature": the shelf goes first and shows more items (v10: ajedrez).

SHELVES = [
  {
    "id": "ajedrez", "tab": "Ajedrez", "name": "Ajedrez y dominó", "icon": "caballo",
    "go": "ajedrez y dominó", "mine": ("medieval", "vikingos", "perros-gatos", "minimal", "mc-ajedrez", "tablero", "pieza"),
    "feature": True,
    "intro": "Los siete primeros los imprimí yo: tocá la foto y mirá los colores en que ya los hice. Casi todos son solo las piezas; el tablero va aparte.",
    "items": [
      ("medieval", "Ajedrez medieval", "Caballeros a caballo y torres de castillo. Más de 10 horas de impresora."),
      ("vikingos", "Ajedrez vikingo", "Reyes con espada y reinas con escudo."),
      ("perros-gatos", "Perros contra gatos", "Los gatos de un lado, los perros del otro. Vos elegís bando."),
      ("minimal", "Ajedrez minimalista", "Piezas lisas, sin adornos. Sirve para jugar todos los días."),
      ("mc-ajedrez", "Ajedrez de Minecraft", "Trae tablero y caja para guardar todo."),
      ("tablero", "Tablero rompecabezas", "Tamaño reglamentario. Se arma por partes y no trae piezas."),
      ("pieza", "Pieza suelta", "Un caballo dragón, o la que le falte a tu juego. Mandame una foto.", "Pieza suelta de ajedrez (te mando una foto)"),
      ("medieval-p", "Ajedrez medieval detallado", "Otra versión del medieval, con más detalle en cada pieza."),
      ("grecia", "Ajedrez de la antigua Grecia", "Minotauro contra Hércules. Este sí trae tablero: 52 × 50 cm."),
      ("escultorico", "Ajedrez escultórico", "Rey de 8 cm. Tiene lugar para imanes."),
      ("plegable", "Ajedrez de viaje", "Se pliega en un tubo de 24 cm con las piezas adentro."),
      ("hp", "Ajedrez de Harry Potter", "Con Harry, Hermione, Ron y el Sombrero Seleccionador."),
      ("sw-caja", "Ajedrez de Star Wars con caja", "Piezas de unos 5 cm y una caja para llevarlas."),
      ("sw-piezas", "Ajedrez de Star Wars", "Con X-Wings, AT-ST y tauntauns. Son piezas delicadas."),
      ("domino", "Dominó", "Las 28 fichas, con su caja."),
    ],
  },
  {
    "id": "clickers", "tab": "Clickers", "name": "Clickers y llaveros", "icon": "clicker",
    "go": "clickers y llaveros", "pre": "Clicker: ", "mine": "all",
    "intro": "Se aprietan y hacen clic. Para tener en la mano mientras esperás o estudiás. También hago flexis y torres de dados: preguntame.",
    "items": [
      ("contador", "Contador de vidas para Magic", "Dos ruedas del 0 al 9 para llevar la cuenta en la partida.", "Contador de vidas para Magic"),
      ("cafe", "Vasito de café", "Tapa negra y faja marrón, como el de la cafetería."),
      ("banana", "Banana", "Media pelada. Esta no se pone negra."),
      ("suculenta", "Suculenta", "En su macetita. No hay que regarla."),
      ("calavera", "Calavera con cerebro", "Trae argolla para colgarla de las llaves."),
      ("hamster", "Hámster en el huevo", "Se asoma por la cáscara."),
      ("rana", "Ranita en flor", "Verde, sentada en una flor rosada."),
      ("osito", "Osito en canasta", "Marrón, en su canasta trenzada."),
      ("lata", "Latita", "Una lata de refresco, en rojo."),
      ("ovni", "Platillo volador", "Con un marcianito verde adentro."),
      ("aceitera", "WD-40", "La lata de siempre, en chiquito."),
      ("hongo", "Hongo", "Marrón y con cara de contento."),
    ],
  },
  {
    "id": "autos", "tab": "Autos", "name": "Autos a escala", "icon": "auto", "go": "autos a escala",
    "intro": "Para armar o para la repisa. Varios doblan cuando girás el volante. Fotos de los diseñadores.",
    "items": [
      ("f40", "Ferrari F40", "Escala 1:19. Se arma por partes, con faros y frenos."),
      ("gallardo", "Lamborghini Gallardo", "Escala 1:19. Girás el volante y doblan las ruedas."),
      ("mclaren", "McLaren 675LT", "Escala 1:19. También dobla con el volante."),
      ("spyder", "Porsche 718 Spyder", "Descapotable, y dobla con el volante."),
      ("amg", "Mercedes-AMG GT", "Mide 23 cm y encastra sin pegamento."),
      ("gt40", "Ford GT40 de 1969", "Escala 1:32. Se ven el piloto y el motor."),
      ("mustang", "Shelby Mustang GT500", "El del 67, con franjas de carrera."),
      ("cobra", "Shelby Cobra", "El del 65, descapotable."),
      ("fiat", "Fiat 500 de 1965", "Escala 1:20. Adentro tiene asientos y volante."),
      ("escarabajo", "Escarabajo 1300", "Tiene partes que se sacan."),
      ("kombi", "Kombi T1", "Con la tabla de surf en el techo."),
      ("jeep", "Willys Jeep", "Las ruedas giran. Es todo impreso, no lleva nada comprado."),
    ],
  },
  {
    "id": "exhibidores", "tab": "Exhibidores", "name": "Exhibidores para autitos", "icon": "panal",
    "go": "exhibidores para autitos", "pre": "Exhibidor: ",
    "mine": ("ascensor",),
    "intro": "Para sacar los Hot Wheels y los Matchbox de la caja y tenerlos a la vista. Todos son para escala 1:64, menos el estante 1:32. El ascensor negro lo imprimí yo; el resto son fotos de los diseñadores.",
    "items": [
      ("garaje", "Garaje de pared", "Entran 6 autitos. Se cuelga y se puede apilar."),
      ("panal", "Panal de pared", "Celdas que se enganchan. Si crece la colección, le sumás más."),
      ("rack-hex", "Estante panal", "Dos columnas de celdas, para la pared."),
      ("tres-en-uno", "Exhibidor 3 en 1", "Tres módulos de pared en una pieza, con fondo."),
      ("modular", "Estante apilable", "Cuando te quedás sin lugar, le agregás un piso."),
      ("ascensor", "Ascensor de exhibición", "Copia del ascensor de autos del museo de Audi. No sube: es para mirar."),
      ("kaido", "Torre Kaido House y Mini GT", "Muestra el auto al lado de su caja."),
      ("infinito", "Módulo infinito", "Los módulos se encastran de costado y la fila sigue."),
      ("podio", "Podio", "Para un solo auto: el preferido."),
      ("torre", "Torre de pared", "Estantes finitos, un auto en cada uno."),
      ("rack-132", "Estante 1:32", "Para autos más grandes, de escala 1:32."),
    ],
  },
  {
    "id": "onepiece", "tab": "One Piece", "name": "One Piece y figuras", "icon": "barco",
    "go": "One Piece y figuras", "mine": "all",
    "intro": "Todo esto salió de mi impresora, y las fotos las saqué yo.",
    "items": [
      ("sunny", "Thousand Sunny", "El barco de Luffy. Lo imprimí por partes y lo armé yo."),
      ("merry", "Going Merry", "Cerca de 200 piezas, armadas una por una."),
      ("striker", "Striker de Ace", "El bote de Ace, sobre una base de olas."),
      ("tiburon", "Submarino tiburón", "El submarino del Sunny, con dientes y todo."),
      ("fruta", "Frutas del diablo", "Gomu Gomu, Mera Mera, Ito Ito y otras, con su soporte."),
      ("articulados", "Figuras articuladas", "Vienen con sus espadas."),
      ("kitty", "Hello Kitty robot", "Hello Kitty con armadura de robot."),
      ("mascara", "Máscara de cosplay", "Plateada, para ponértela con el disfraz."),
    ],
  },
  {
    "id": "gamer", "tab": "Minecraft y Star Wars", "name": "Minecraft, Star Wars y Pokémon", "icon": "joystick",
    "go": "Minecraft, Star Wars y Pokémon", "mine": ("sprigatito",),
    "intro": "Acá también están el ajedrez de Minecraft y el de Star Wars.",
    "items": [
      ("tnt", "Bloque de TNT", "Con la mecha arriba."),
      ("dragon", "Dragón del End", "28 cm. Mueve las alas, las patas y la cola."),
      ("diorama-mc", "Diorama de Minecraft", "Girás la manija y andan las vagonetas y el bote."),
      ("bonsai", "Bonsái de bloques", "Un arbolito de Minecraft en su maceta."),
      ("torta", "Torta de Minecraft", "Es una caja: la torta es la tapa."),
      ("creeper", "Alcancía Creeper", "Ranura arriba. La tapa se saca para vaciarla."),
      ("mc-ajedrez", "Ajedrez de Minecraft", "Trae tablero y caja para guardar todo."),
      ("r2", "R2-D2", "Cúpula azul y plateada, para la repisa."),
      ("tie", "Caza TIE de Vader", "La nave de Darth Vader, sobre su base."),
      ("estrella", "Estrella de la Muerte", "A medio construir, como en El retorno del Jedi."),
      ("hoth", "Diorama de Hoth", "Los AT-AT avanzando en la nieve."),
      ("sw-piezas", "Ajedrez de Star Wars", "Con X-Wings, AT-ST y tauntauns. Son piezas delicadas."),
      ("pokebox", "Caja para cartas Pokémon", "Guarda un mazo y parece una Game Boy."),
      ("sprigatito", "Sprigatito", "El gatito verde de Pokémon, recién salido de la impresora."),
    ],
  },
  {
    "id": "hobbies", "tab": "Fútbol y RC", "name": "Fútbol, aviones RC y fingerboard", "icon": "pelota",
    "go": "fútbol, aviones RC y fingerboard", "mine": ("penarol", "nacional"),
    "intro": "Los estadios los imprimí yo, y las fotos son mías.",
    "items": [
      ("penarol", "Estadio de Peñarol", "El Campeón del Siglo, con las tribunas y el nombre."),
      ("nacional", "Estadio de Nacional", "El Gran Parque Central, con el nombre del club."),
      ("ala", "Ala volante RC", "Un avión a radiocontrol sin cola. Se imprime en partes."),
      ("cub", "Avión RC de ala alta", "Para volar en el campito."),
      ("rampa", "Rampa de fingerboard", "Para hacer trucos con dos dedos arriba de la mesa."),
      ("baranda", "Baranda de fingerboard", "Para grindear con el skate de dedo."),
    ],
  },
  {
    "id": "jardin", "tab": "Jardín", "name": "Pájaros y jardín", "icon": "pajaro",
    "go": "pájaros y jardín",
    "mine": ("elfico", "casita"),
    "intro": "Para el balcón, el fondo o la huerta. Si va al sol, conviene PETG: preguntame. Los comederos élfico y casita los imprimí yo; el resto son fotos de los diseñadores.",
    "items": [
      ("hoja", "Comedero hoja", "Tiene forma de hoja y se cuelga de una rama."),
      ("redondo", "Comedero redondo", "Abierto y con techito. Se cuelga o se apoya."),
      ("elfico", "Comedero élfico", "La bandeja de las semillas sale para lavarla."),
      ("casita", "Comedero casita", "Comen varios pájaros a la vez."),
      ("driftwood", "Pajarera rústica", "Parece madera de playa. Se abre por atrás para limpiarla."),
      ("gota", "Pajarera gota", "Lisa, para colgar de una rama."),
      ("espiral", "Pajarera espiral", "Para pájaros chicos."),
      ("abejas", "Bebedero de abejas", "Se enrosca en una botella. Las abejas toman sin ahogarse."),
      ("maceta", "Maceta capitoné", "Parece de tela acolchada. Es para macetas de 9 cm."),
      ("cosechador", "Cosechador de frutas", "Va en la punta de un palo y corta la fruta de arriba. La hoja de cutter no viene."),
    ],
  },
  {
    "id": "casa", "tab": "Casa", "name": "Casa", "icon": "casa",
    "go": "cosas para la casa",
    "mine": ("repisa",),
    "intro": "Cosas raras y útiles para la casa. La repisa roja la imprimí yo; el resto son fotos de los diseñadores.",
    "items": [
      ("repisa", "Repisa derretida", "Un estante de pared que parece que gotea."),
      ("bowl", "Bowl derretido", "Para dejar las llaves cuando llegás."),
      ("cassette", "Cassette gigante", "24 × 15 cm. Se le puede poner una luz adentro (la luz no viene)."),
      ("mesa-luz", "Organizador de mesa de luz", "Sostiene el libro abierto y tiene cajones."),
      ("bolso", "Cartera de costillas", "Para Halloween, o para todo el año."),
      ("casco-gato", "Casco de Maléfica para gatos", "Para gatos medianos. Un ratito para la foto, y con vos al lado."),
    ],
  },
]


# Más fotos de un producto: se ven en su ventana (tocando la foto). La primera es la de la tarjeta.
# Cada una: (archivo en assets/p sin .webp, qué se ve).
FOTOS = {
  "medieval": [("medieval", "Negro contra dorado"), ("medieval-2", "Gris contra dorado, de cerca"),
               ("medieval-3", "Gris contra blanco"), ("medieval-4", "Plateado contra negro"),
               ("medieval-5", "Gris contra dorado"), ("medieval-d", "Dorado y gris, en un tablero de madera")],
  "vikingos": [("vikingos", "Dorado contra gris, en el tablero rompecabezas"), ("vikingos-2", "Blanco contra negro"),
               ("vikingos-d", "Foto del diseñador")],
  "perros-gatos": [("perros-gatos", "Los perros, en amarillo"), ("perros-gatos-2", "Los gatos, en gris"),
                   ("perros-gatos-3", "Los perros de cerca"), ("perros-gatos-4", "Los gatos, con su torre"),
                   ("perros-gatos-d", "Foto del diseñador")],
  "minimal": [("minimal", "Negro contra blanco"), ("minimal-2", "Visto de arriba"), ("minimal-3", "Desde el lado blanco"),
              ("minimal-d", "Foto del diseñador")],
  "mc-ajedrez": [("mc-ajedrez", "Las piezas y las casillas del tablero"), ("mc-ajedrez-2", "Con su caja"),
                 ("mc-ajedrez-3", "Todo junto, visto de arriba"), ("mc-ajedrez-d", "Foto del diseñador")],
  "tablero": [("tablero", "Con el ajedrez vikingo arriba (las piezas van aparte)"), ("tablero-d", "Foto del diseñador")],
  "contador": [("contador", "De frente"), ("contador-2", "En la mano, para ver el tamaño"), ("contador-3", "De costado"),
               ("contador-4", "La tapa")],
  "ascensor": [("ascensor", "Dos torres, en negro"), ("ascensor-d", "Foto del diseñador")],
  "elfico": [("elfico", "En dorado"), ("elfico-d", "Foto del diseñador")],
  "casita": [("casita", "Lila, con el techo rosa"), ("casita-d", "Foto del diseñador")],
  "repisa": [("repisa", "En rojo"), ("repisa-d", "Foto del diseñador")],
}

# 12x12 pixel icons, one string per row ('#' = ink)
ICONS = {
  "clicker": ["............","....####....","...######...","...######...","....####....","..########..",".##########.",".##########.",".##########.","..########..","............","............"],
  "auto":    ["............","............","....#####...","...#.#..##..","..#..#...#..",".##########.","############","############",".##.....##..",".##.....##..","............","............"],
  "panal":   ["............","..###..###..",".#...##...#.",".#...##...#.","..###..###..",".....##.....","....#..#....","...#....#...","....#..#....",".....##.....","............","............"],
  "caballo": ["............",".....###....","....#####...","...###.###..","..########..","..##..####..",".......###..","......####..",".....#####..","....######..","...########.","............"],
  "joystick":["............",".....##.....",".....##.....","......#.....","......#.....","..########..",".##########.",".#.#####.##.",".##########.","..########..","............","............"],
  "barco":   ["............","......#.....","......##....","......###...","......####..","......#.....","......#.....","############",".##########.","..########..","............","............"],
  "pajaro":  ["............","............","...###......","..#####.....","..##.###....","######......","..#########.","...########.","....#####...",".....#.#....","....##.##...","............"],
  "casa":    ["............",".....##.....","....####....","...######...","..########..",".##########.","..########..","..##.##.##..","..##.##.##..","..##....##..","..########..","............"],
  "pelota":  ["............","....####....","..##.##.##..","..#.####.#..",".##.####.##.",".###....###.",".##.####.##.","..#.####.#..","..##.##.##..","....####....","............","............"],
}

ICONS.update({
  "chat":    ["............",".##########.",".#........#.",".#........#.",".#.#.#.#..#.",".#........#.",".##########.","..##........","..#.........","............","............","............"],
  "coin":    ["............","...#....#...",".##########.",".##########.",".#........#.",".#.##.##..#.",".#.##.##..#.",".#........#.",".#.##.....#.",".#.##.....#.",".##########.","............"],
  "printer": ["............",".##########.",".#........#.",".#..####..#.",".#..####..#.",".#...##...#.",".#........#.",".#.######.#.",".#........#.",".##########.",".##......##.","............"],
  "box":     ["............","..########..",".#...##...#.","############","#....##....#","#....##....#","#..........#","#..........#","#..........#","############","............","............"],
  "left":    ["............","............",".......#....","......##....",".....###....","....####....",".....###....","......##....",".......#....","............","............","............"],
  "right":   ["............","............","....#.......","....##......","....###.....","....####....","....###.....","....##......","....#.......","............","............","............"],
  "down":    ["............","............","............","...######...","....####....",".....##.....","............","...######...","....####....",".....##.....","............","............"],
  "libro":   ["............",".####.####..",".#..#.#..#..",".#..#.#..#..",".#..#.#..#..",".#..#.#..#..",".#..#.#..#..",".####.####..","....###.....","............","............","............"],
  "foto":    ["............","....###.....",".##########.",".#...##...#.",".#..#..#..#.",".#.#....#.#.",".#.#....#.#.",".#..#..#..#.",".#...##...#.",".##########.","............","............"],
  "cursor":  ["............","...#........","...##.......","...###......","...####.....","...#####....","...####.....","...###......","...##.......","...#........","............","............"],
})

def icon_svg(name):
    rows = ICONS[name]
    d = []
    for y, row in enumerate(rows):
        x = 0
        while x < len(row):
            if row[x] == '#':
                s = x
                while x < len(row) and row[x] == '#': x += 1
                d.append(f"M{s} {y}h{x - s}v1h-{x - s}z")
            else:
                x += 1
    return ('<svg viewBox="0 0 12 12" aria-hidden="true" shape-rendering="crispEdges">'
            f'<path fill="currentColor" d="{"".join(d)}"/></svg>')
