# Auditoría de las hojas aprobadas (2026-11-06)

34 hojas en `sheets/`: 29 de Gemini, 4 hechas por Claude y 1 de Gemini corregida. Cada una se revisó a ojo, cuadro por cuadro, además de medirla (altura de cada cuadro, línea de los pies, cortes en el borde de la celda, paleta).

Puntaje sobre 10 en dos ejes:
- **Integridad**: que respete el modelo (diseño y ropa), que no traiga objetos de más, que estén todos los cuadros y que mire hacia donde debe.
- **Calidad**: píxel nítido, coherencia de tamaño y posición entre cuadros, y que la acción se lea a tamaño chico.

## Ranking

| # | Hoja | Origen | Integridad | Calidad | Total | Notas |
|---|---|---|---|---|---|---|
| 1 | `printer` | Gemini | 10 | 10 | **10** | 4 estados claros y alineados |
| 2 | `sack` | Gemini | 10 | 10 | **10** | Vacía → llena, con la misma base |
| 3 | `plate_taller` | Gemini | 10 | 9 | **9.5** | Fondo vacío fiel a la maestra |
| 4 | `papa_noel_wave_S_1` | Gemini | 10 | 9 | **9.5** | Los 4 cuadros con la misma altura (105) |
| 5 | `papa_noel_sip_mate_S_1` | Gemini | 10 | 9 | **9.5** | Lectura perfecta del sorbo |
| 6 | `garland` | Gemini | 10 | 9 | **9.5** | Apagada y prendida |
| 7 | `mago_model` | Gemini | 10 | 9 | **9.5** | Base de todo el Mago |
| 8 | `fx_1` a `fx_3` | Claude | 10 | 9 | **9.5** | Dibujados con la paleta exacta; no pueden salir torcidos |
| 9 | `papa_noel_sack_shoulder_S_1` | Gemini | 10 | 9 | **9.5** | |
| 10 | `papa_noel_refreshed_S_1` | Gemini | 10 | 9 | **9.5** | |
| 11 | `papa_noel_startled_S_1` | Gemini (re-pedido) | 10 | 9 | **9.5** | Sin banquito |
| 12 | `papa_noel_sit_plop_S_1` | Gemini (re-pedido) | 10 | 8.5 | **9** | Sin banquito. Caída corta pero clara |
| 13 | `papa_noel_model` | Gemini | 9 | 9 | **9** | Mide 107 px contra 92 pedidos: ~11 % más alto que el Mago. Se ve bien y el reel ya está armado con esa escala |
| 14 | `objects_taller_2` | Gemini | 10 | 8.5 | **9** | Corona |
| 15 | `mago_idle_S_1` | Gemini | 9 | 9 | **9** | Variación de altura de 4 px, aceptable para respirar |
| 16 | `papa_noel_fan_hot_S_1` | Gemini | 9 | 9 | **9** | Sin gorro en la cabeza: lo usa de abanico, como pide la acción |
| 17 | `papa_noel_joy_jump_S_1` y `_2` | Gemini | 9 | 8.5 | **9** | En el pico, el gorro queda a 1 px del borde de la celda, sin cortarse |
| 18 | `mago_idle_N_1` | Claude (derivada) | 9 | 8.5 | **9** | La vista de espaldas del model sheet con respiración de 1 px |
| 19 | `papa_noel_sack_shake_S_1` | Gemini + arreglo | 8 | 8.5 | **8.5** | Gemini cortó la bolsa contra el borde de arriba en el cuadro 1; se le cerró la parte de arriba con contorno. Trae una polilla dibujada en un cuadro, que se suma a la animada |
| 20 | `objects_taller_1` | Gemini | 9 | 8 | **8.5** | Banquito, ventilador, mate y arbolito. Las luces del arbolito cambian poco entre los dos cuadros |
| 21 | `papa_noel_walk_hot_W_1` y `_2` | Gemini | 9 | 8 | **8.5** | Rebote de altura grande (103 a 114), se lee como andar pesado |
| 22 | `papa_noel_walk_sack_E_1` y `_2` | Gemini | 9 | 8 | **8.5** | Igual que la anterior |
| 23 | `mago_walk_E_1` y `_2` | Gemini + arreglo | 8 | 8 | **8** | Mezcla vistas de perfil y de tres cuartos. El cuadro 1 era 5 a 7 px más alto y hacía saltar el sombrero: se reemplazó por el cuadro 3, que tiene la misma vista |
| 24 | `mago_press_button_N_1` | Gemini (re-pedido) | 9 | 7.5 | **8** | Sin mesa. Sostiene algo dorado en lugar de apretar un botón: se lee igual |
| 25 | `mago_turn_S_to_N_1` | Gemini | 8 | 7.5 | **7.5** | El cuadro 1 es de tres cuartos, no de frente. El giro se entiende |
| 26 | `plate_taller_master` | Gemini | 8 | 9 | **7.5** | No trae al Mago para dar escala. Solo sirvió de referencia |
| 27 | `papa_noel_sad_S_1` | Gemini (re-pedido) | 7 | 6 | **6.5** | Ropa correcta, pero la bolsa parece una barra y la tristeza casi no se lee. Va como re-pedido **opcional** en la tanda 7 |
| 28 | `door_R` | Gemini | 9 | 8 | **—** | Correcta, pero no se usa: la puerta del fondo está en perspectiva y ningún sprite de puerta calza con ella |

## Qué se arregló (hecho por Claude)

- `mago_walk_E_1`: cuadro 1 reemplazado por el cuadro 3 (eliminaba el salto de tamaño). Original en `candidates/mago_walk_E_1/v1.png`.
- `papa_noel_sack_shake_S_1`: parte de arriba de la bolsa cerrada y con contorno en el cuadro 1.
- `fx_1`, `fx_2`, `fx_3`: hechos desde cero con `skills/pixel-reel/scripts/draw_fx.py`.
- `mago_idle_N_1`: derivada del model sheet del Mago.

## Qué no se puede arreglar sin Gemini

- Poses nuevas de personajes: las 9 animaciones del Mago que faltan y sus 2 segundas hojas.
- Productos: las 5 hojas de ítems.
- Una expresión que no se lee (`papa_noel_sad_S_1`, opcional).

Todo eso está en la **tanda 7**.

## Patrones de Gemini

1. Agrega muebles del contexto (mesa, banquito). Ya está corregido en todos los prompts.
2. Mezcla diseños en chats largos (la camisa hawaiana). Solución: un chat por hoja.
3. Varía la altura entre cuadros de la misma hoja (hasta 7 px). Se arregla repitiendo o descartando cuadros.
4. Corta contra el borde de la celda cuando la pose sube mucho (la bolsa en alto). Se puede pedir "keep 32 px of margin above".
5. Muy buen resultado en objetos con estados y en poses sentadas o de frente.
