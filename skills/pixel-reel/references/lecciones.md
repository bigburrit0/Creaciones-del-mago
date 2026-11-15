# Lecciones: por qué este workflow es así

Salen de dos videos hechos a partir de keyframes sueltos. El primero quedó limpio y el segundo necesitó varias rondas de parches.

| Pasó | Por qué | Cómo lo evita este workflow |
|---|---|---|
| No había fondo detrás de los personajes; reconstruirlo dejó manchas y costuras | Los keyframes traían el personaje pintado encima | Fondo vacío como etapa propia, editado desde la imagen maestra |
| Los recortes se contaminaban (el pájaro se llevaba un pedazo del comedero, el mago la cola del pájaro) | Los objetos se superponían en la misma imagen | Cada sprite se genera aislado sobre magenta plano |
| Faltaban las poses intermedias (pararse, caminar, aletear, sentarse) | Un keyframe es un instante, no una acción | Cada acción es una animación descrita cuadro por cuadro |
| El mismo personaje cambiaba de diseño entre imágenes | Cada imagen se generaba de cero | Model sheet aprobado y adjunto en cada prompt |
| Objetos que cambiaban de estado sin transición (silla plegada y abierta, planta, escena) | Nadie pidió los estados intermedios | Los objetos llevan sus estados como cuadros |
| El último keyframe era otra escena | Generación independiente | Un reel = un escenario y una cámara |
| Píxeles de distinto tamaño en la misma toma | Imágenes de IA reescaladas al 80-85 % | Grilla nativa ×4 y escala entera; el recorte reconstruye a resolución de arte y cuantiza a la paleta |
| Mucho tiempo esperando imágenes | El video dependía de tenerlas todas | Animatic con provisorias del mismo formato y nombre; las reales se reemplazan solas |

Lo que sí funcionó y se mantiene:
- Editar una imagen ("la misma imagen, pero cambiando solo X") en lugar de generar otra.
- Animar por pasos con anticipación, rebote y aplaste.
- Dos poses para el aleteo.
- Ancla en los pies para que nada salte.
- Audio sincronizado a cada acción.
