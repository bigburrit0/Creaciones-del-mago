# Reel 4 · «La huerta de los pájaros» (simulador de granja)

| | |
|---|---|
| **Formato** | 9:16 vertical, 1080 × 1920, 10 s, una sola toma |
| **Género retro** | Simulador de granja de 16 bits: vista de arriba en tres cuartos, tierra en cuadrícula, cultivos que crecen por etapas |
| **Producto** | Comedero casita (catálogo: «Comen varios pájaros a la vez.»). Foto del diseñador: `assets/p/casita.webp` |
| **Público** | Gente con fondo, patio o balcón y gusto por los pájaros y las plantas, 30 a 70. Regalo para mamá o la abuela |
| **Mensaje único** | Un comedero para el fondo, en PETG si va al sol |
| **Tono** | Tranquilo, de verano, con un chiste |
| **Aparece el Mago** | Sí: planta la semilla y al final se sienta a tomar mate |

## 1. La idea

En los juegos de granja plantás una semilla y en tres pasos crece el tomate. Acá el Mago planta una semilla en el
fondo de una casa de Montevideo, crece un arbolito en tres saltos y, en vez de fruta, de la rama cuelga un comedero.
Llegan un benteveo, un hornero y dos chingolos. El Mago se sienta con el mate. «Plantás esto. Cosechás esto.»

- **Por qué engancha:** en el primer segundo hay un brote que sale de la tierra con un «pop». El crecimiento por
  saltos es raro de ver en un anuncio y se entiende sin sonido.
- **Por qué vende:** le habla a un público que los otros reels no tocan (jardín, pájaros, gente más grande) y es
  buen regalo de Navidad para alguien con fondo o balcón.
- **Lo local:** pájaros de acá (benteveo, hornero, chingolo), patio con baldosas y mate, mañana de verano.
- **Loop:** el último cuadro tiene a los pájaros comiendo y el Mago sentado; al repetirse, el Mago vuelve a la tierra
  con la semilla. Si se nota el salto, sirve igual, porque el juego «empieza otro día».

## 2. Guion (0 a 10 s)

| Tiempo | Imagen (pixel art 16 bits, vista de arriba en tres cuartos, cámara fija) | Texto en pantalla (en edición) | Audio |
|---|---|---|---|
| **0:00 – 0:03** | Fondo de una casa en verano: baldosas, un cantero de tierra arada en cuadritos, plantas de tomate, un cerco. El Mago planta una semilla en el cuadrito del centro. Pop: sale un brote, después un arbolito, después un árbol chico. | `PLANTÁS ESTO.` | **SFX:** golpecito de pala, tres «pop» de crecimiento subiendo de tono. **Voz:** «No da tomates:» |
| **0:03 – 0:06** | De una rama, como si fuera fruta, aparece colgado un comedero lila de seis lados con techito, lleno de semillas. Llega un benteveo (panza amarilla, cabeza con rayas blancas y negras). Después un hornero (marrón anaranjado). | `COSECHÁS ESTO.` | **SFX:** campanita de «cosecha lista», aleteos de 8 bits, el «bien-te-veo» del benteveo hecho con chiptune. **Voz:** «da benteveos.» |
| **0:06 – 0:08** | Llegan dos chingolos. Todos picotean y caen semillitas al piso. El Mago se sienta en una silla plegable con un mate. | (se va el texto) | **SFX:** picoteos rápidos, música alegre en mayor. **Voz:** «Es un comedero impreso en 3D, en PETG para el sol.» |
| **0:08 – 0:10** | Los pájaros comen. El Mago toma mate. Una hoja se mueve con el viento. | `Comedero casita · comen varios pájaros a la vez` y abajo: `En PETG si va al sol · WhatsApp 092 104 419` | **SFX:** acorde suave y pájaros. **Voz:** «Escribime y te paso el precio.» |

**Voz en off completa** (21 palabras):
> «No da tomates: da benteveos. Es un comedero impreso en 3D, en PETG para el sol. Escribime y te paso el precio.»

## 3. Texto del post y variantes de cierre

**Texto del post (principal):**
> No da tomates: da benteveos. El comedero casita lo imprimo en 3D en Montevideo, y comen varios pájaros a la vez.
> Si va al sol, conviene PETG, que aguanta mejor la intemperie: preguntame. En el catálogo hay más comederos,
> pajareras y un bebedero para abejas. Te paso precio y fecha por WhatsApp antes de empezar, sin compromiso.
> 092 104 419 · creacionesdelmago.com

| Variante | Texto en pantalla (0:08 – 0:10) | Voz | Para qué |
|---|---|---|---|
| **A · Comedero** (principal) | `En PETG si va al sol · WhatsApp 092 104 419` | «Escribime y te paso el precio.» | Conversión por WhatsApp |
| **B · Navidad** | `Para la que tiene fondo · Si es para Navidad, decímelo` | «Si es para Navidad, decímelo y te digo si llego.» | Regalo para mamá o la abuela, sin prometer fecha |
| **C · Balcón** | `¿Tenés balcón? También hay comederos chicos` | «¿Solo balcón? Hay comederos y pajareras más chicos.» | Gente de apartamento. En el catálogo están el comedero hoja y la pajarera gota |
| **D · Comentarios** | `¿Qué pájaros vienen a tu fondo?` | «¿Qué pájaros vienen a tu fondo? Contame.» | Alcance orgánico |

## 4. Imágenes fijas

Generá primero la **hoja del Mago** (está en `LEEME.md`) y subila en los dos keyframes. Subí también
`assets/p/casita.webp` para el keyframe B: comedero de seis lados, lila, con techo de cúpula, adornos en relieve,
lados abiertos con una bandeja de semillas y una cuerda arriba para colgarlo.

Pegá el **bloque de estilo** del `LEEME.md` al final de cada prompt. En este reel, cambiá en el bloque
«deep night indigo» por el cielo de día: el índigo queda para las sombras y los contornos.

### Keyframe A · primer cuadro (0:00)

```
16-bit farming game view, top-down three-quarter perspective, vertical 9:16, static. A small backyard of a house in Montevideo on a bright summer morning: cream and terracotta floor tiles at the bottom, a low brick wall and a wooden fence at the top, a few tomato plants with red tomatoes on stakes on the left, a folded wooden garden chair on the right. In the center, a patch of tilled brown soil drawn as a neat grid of square plots. The Wizard from the attached reference sheet kneels at the center plot, dropping one glowing gold seed into the soil, a small trowel next to him. Soft shadows in indigo #2A2350, sunlight in warm cream and gold. The tiled floor fills the bottom fifth of the frame and stays plain. Calm, cozy, a little funny.
```
+ bloque de estilo + `Use the attached Wizard reference sheet and keep the Wizard exactly the same (robe, hat, beard, proportions).`

### Keyframe B · último cuadro (0:10)

Pedilo como edición del keyframe A.

```
Edit the attached image and keep everything else the same: same backyard, same tiles, fence, tomato plants and camera. In the center plot there is now a small young tree with round green leaves. Hanging from its main branch by a short rope, like a fruit, is a hexagonal bird feeder shaped like the attached reference photo: pale lilac (#D6D0F7) with a domed roof, ornamental relief patterns, open sides and a tray full of seeds. On the feeder: a great kiskadee (bright yellow belly, black-and-white striped head, brown back) and a rufous hornero (orange-brown, pale belly). Two small rufous-collared sparrows peck seeds on the ground below. The Wizard sits on the unfolded wooden garden chair on the right, holding a mate gourd with a metal straw, relaxed. Keep the bottom fifth of the frame plain tiled floor for text.
```
+ bloque de estilo + la frase de la hoja del Mago.

**Revisá antes de seguir:** que el comedero sea el de la foto (seis lados, lila, cúpula), que los pájaros sean de acá
(el benteveo con la panza amarilla es el que más se reconoce) y que el Mago sea el de la hoja.

## 5. Prompt del video (Gemini, 10 s)

**Configuración:** video, 9:16, 10 segundos. Imagen inicial: **keyframe A**. Si te deja sumar imagen final o
referencias, agregá el **keyframe B**, la hoja del Mago y la foto del comedero.

```
Single continuous shot, no cuts. Locked-off static camera, top-down three-quarter view like a 1990s 16-bit farming game, no zoom, no pan, no depth of field, no motion blur. Authentic 16-bit pixel art: hard square pixels, limited palette, low frame-rate sprite animation, things grow in distinct stage jumps like a video game, not smoothly. Flat 2D for the whole clip.

Subject: the small Wizard in an indigo robe and pointed hat with a gold band, in the sunny backyard of a house in Montevideo with tiled floor, tomato plants and a patch of tilled soil.

Action, in order:
0 to 3 seconds: the Wizard drops a glowing gold seed into the center plot and steps back; the plant grows in three quick stage jumps with a small sparkle each time: a green sprout, then a sapling, then a small young tree with round leaves.
3 to 6 seconds: from the main branch, like a fruit growing, a pale lilac hexagonal bird feeder with a domed roof appears hanging from a short rope, full of seeds; a great kiskadee with a bright yellow belly and black-and-white striped head flies in and lands on it; then a rufous orange-brown hornero lands on the other side.
6 to 8 seconds: two small rufous-collared sparrows hop in and peck fallen seeds on the ground; the birds on the feeder peck, a few seeds drop; the Wizard unfolds the wooden chair on the right and sits down with a mate gourd.
8 to 10 seconds: the birds keep pecking in a simple loop, the Wizard sips the mate, the leaves sway slightly. The last second is calm.

Audio: a soft trowel tap, three rising pops as the plant grows, a cheerful harvest chime when the feeder appears, 8-bit wing flaps, a chiptune version of a kiskadee call, quick pecking ticks, a light happy chiptune melody in a major key, birdsong in the background. No dialogue, no voice, no music with lyrics.

No text, no letters, no numbers, no subtitles, no captions, no logos anywhere in the video.
```

## 6. Plan B (si la herramienta da 8 s)

Primer cuadro: keyframe A. Último cuadro: keyframe B. Mismo prompt con estos tiempos:

```
0 to 2.5 seconds: the Wizard plants the gold seed, the plant grows in three stage jumps into a small tree. 2.5 to 5 seconds: the lilac feeder appears hanging from the branch like a fruit, the kiskadee and then the hornero land on it. 5 to 8 seconds: two sparrows hop in and peck seeds, the Wizard sits on the chair with his mate.
```

En la edición, congelá el último cuadro 2 s (de 0:08 a 0:10) para el cierre.

## 7. Edición

- **`PLANTÁS ESTO.` / `COSECHÁS ESTO.`:** mismo lugar, misma tipografía, en crema `#F3E9D2` con contorno índigo. El
  segundo reemplaza al primero de golpe, sin transición, en el momento en que aparece el comedero. El chiste está en
  ese corte.
- **Detalle de juego de granja (opcional):** arriba a la derecha, debajo de la zona segura, un solcito pixel con un
  arco que avanza de 0 a 10 s, como el reloj del día. Se puede dibujar en Canva con cuadraditos.
- **Cierre (0:08 – 0:10):** caja índigo al 85 % con borde dorado, justo arriba de la zona de botones de Instagram.
  Arriba de la caja, el glifo `assets/px/glifo-oro.png`.
- **Voz:** con calma, este es el reel más tranquilo de los cuatro.

## 8. Antes de publicar

- [ ] El comedero se parece al de la foto del catálogo (seis lados, lila, cúpula).
- [ ] Los pájaros son de acá y no salen pájaros con colores inventados de más.
- [ ] El Mago es el de la hoja de personaje.
- [ ] No hay letras ni números generados por la IA.
- [ ] El texto del post dice «si va al sol, conviene PETG» y no promete fecha ni precio.
