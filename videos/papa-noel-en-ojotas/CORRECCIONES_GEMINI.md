# Instrucciones para Gemini: qué corregir y cómo pedirlo

Lo que salió mal en las tandas 3 y 4, y cómo pedirlo para que no se repita. Los prompts de los paquetes nuevos ya traen todo esto incluido. Si usás un prompt viejo, o Gemini se desvía en medio de un chat, pegale el bloque de la sección 1.

## 1. Reglas que Gemini olvidó (pegar si se desvía)

```
Draw ONLY the subject described: no furniture, no stool, chair or table, no floor, no props unless a cell names them (the set and its furniture are separate images). A character keeps exactly the outfit and colours of its attached model sheet in every cell. Flat pure magenta #FF00FF background, 2x2 grid, same size and baseline in every cell, no text, no grid lines.
```

Consejos:
- **Un chat nuevo por hoja**, con el model sheet adjunto. En chats largos Gemini mezcla diseños entre hojas: así apareció la camisa hawaiana.
- Si una versión sale rara, decile **"same character design as the attached model sheet, try again"** en lugar de explicarle todo de nuevo.
- Nombres de archivo: `<hoja>_v1.png`, `<hoja>_v2.png`, como en la tanda 4. Con esos nombres, el zip se importa entero de una.

## 2. Hojas a volver a pedir (tanda 5)

| Hoja | Qué salió mal | Corrección (ya está al final de su `PROMPT.txt`) |
|---|---|---|
| `mago_press_button_N_1` | Dibujó la mesa de trabajo dentro del sprite | Sin mesa: la mesa ya está en el fondo |
| `papa_noel_sad_S_1` | Camisa hawaiana en lugar de la musculosa blanca (las dos versiones) | La ropa exacta del model sheet, con la bolsa roja vacía en la falda |
| `papa_noel_sit_plop_S_1` | Dibujó el banquito en los cuadros | Sin banquito: se sienta sobre un asiento invisible |
| `papa_noel_startled_S_1` | Dibujó el banquito (y en un cuadro, flotando) | Igual que la anterior |

## 3. Segundas hojas (tanda 5)

Son las animaciones de 6 cuadros. Adjuntá también la **primera hoja aprobada** (va en el paquete como adjunto), para que mantenga el tamaño y la posición:

- `mago_walk_E_2`
- `papa_noel_walk_hot_W_2`
- `papa_noel_joy_jump_S_2`
- `papa_noel_walk_sack_E_2`

## 4. Lo que todavía falta de la tanda 3

Con los paquetes que ya tenés:
- **11 animaciones del Mago**: tomar mate, sorpresa, salto, pensar, idea, levantar el regalo, tirarlo, saludar, ofrecer mate, reposo de espaldas y apretar el botón (esta última, mejor con el paquete nuevo de la tanda 5).
- **Efectos**: `fx_1`, `fx_2` y `fx_3`.
- **Ítems**: `items_1`, `items_2`, `items_3`, `items_5` e `items_6`.

Esos prompts no traen la regla nueva de la sección 1. Agregásela al final antes de enviar, sobre todo en las de efectos e ítems, porque son las que más tienden a dibujar mesa o piso.
