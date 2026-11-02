# Catálogo de sprites

Generado desde `sprites.json` por `tools/gen_prompts.py`. Prioridad: P0 = lo usa el reel de Navidad, P1 = siguiente tanda, P2 = cuando haga falta.

## El Mago (48 animaciones)

### Movimiento

| id | dir | cuadros | modo | fps | prio | para qué |
|---|---|---|---|---|---|---|
| `walk_E` | E (+W espejo) | 6 | bucle | 8 | P0 | cross the room left to right (W = mirrored) |
| `walk_S` | S | 6 | bucle | 8 | P1 | walk towards the camera |
| `walk_N` | N | 6 | bucle | 8 | P1 | walk away from the camera |
| `run_E` | E (+W espejo) | 6 | bucle | 12 | P2 | hurry, chase something |
| `turn_S_to_N` | S>N | 3 | una vez | 8 | P0 | turn to the workbench; play reversed for N to S |

### Reposo

| id | dir | cuadros | modo | fps | prio | para qué |
|---|---|---|---|---|---|---|
| `idle_S` | S | 4 | bucle | 4 | P0 | default standing loop |
| `idle_N` | N | 4 | bucle | 4 | P0 | default loop while working at the bench |
| `blink_S` | S | 3 | una vez | 12 | P1 | life in long holds (play 1-2-3-2-1) |
| `look_around_S` | S | 4 | una vez | 8 | P1 | waiting, curiosity |
| `sip_mate_S` | S | 6 | una vez | 8 | P0 | signature mate sip, calm endings |
| `sleepy_S` | S | 4 | bucle | 4 | P2 | late night, waiting for a long print |

### Emociones y reacciones

| id | dir | cuadros | modo | fps | prio | para qué |
|---|---|---|---|---|---|---|
| `surprised_S` | S | 4 | queda en el último | 8 | P0 | something unexpected happens |
| `joy_jump_S` | S | 6 | una vez | 8 | P0 | victory, happy reveal, a sale |
| `laugh_S` | S | 4 | bucle | 10 | P1 | funny moment |
| `proud_S` | S | 4 | queda en el último | 8 | P1 | showing a finished piece |
| `thinking_S` | S | 4 | bucle | 4 | P0 | considering, planning |
| `idea_S` | S | 4 | queda en el último | 8 | P0 | eureka moment (add fx_idea above the head) |
| `confused_S` | S | 4 | bucle | 6 | P1 | doesn't understand an order (add fx_swirl) |
| `facepalm_S` | S | 4 | queda en el último | 8 | P1 | a failed print, a funny mistake |
| `sad_S` | S | 4 | queda en el último | 8 | P1 | something broke, sold out |
| `grumpy_S` | S | 4 | bucle | 6 | P2 | printer jam (add fx_steam) |
| `love_S` | S | 4 | bucle | 4 | P2 | a lovely gift, a customer photo (add fx_hearts) |
| `shy_S` | S | 4 | bucle | 4 | P2 | receiving a compliment |
| `nervous_S` | S | 4 | bucle | 6 | P2 | deadline, Christmas rush (add fx_sweat) |
| `impatient_S` | S | 4 | bucle | 8 | P2 | waiting for a long print |
| `scared_S` | S | 4 | bucle | 12 | P2 | a spooky print, Halloween |
| `celebrate_spin_S` | S | 6 | una vez | 10 | P1 | big celebration, end of a reel |

### Trabajo

| id | dir | cuadros | modo | fps | prio | para qué |
|---|---|---|---|---|---|---|
| `press_button_N` | N | 4 | bucle | 6 | P0 | starting a print, working at the printer |
| `take_print_N` | N | 4 | una vez | 8 | P1 | taking a finished piece out |
| `item_get_S` | S | 4 | queda en el último | 8 | P0 | RPG 'item get' reveal; the item sprite is placed above the hands |
| `toss_E` | E | 4 | una vez | 10 | P0 | throw a piece to someone on the right (W = mirrored if the hand is not visible) |
| `inspect_S` | S | 4 | bucle | 4 | P1 | quality check (piece drawn separately) |
| `carry_box_E` | E (+W espejo) | 6 | bucle | 8 | P1 | deliveries, carrying gifts |
| `wrap_gift_S` | S | 4 | bucle | 6 | P2 | Christmas packing |
| `sand_piece_S` | S | 4 | bucle | 8 | P2 | post-processing |

### Magia

| id | dir | cuadros | modo | fps | prio | para qué |
|---|---|---|---|---|---|---|
| `cast_S` | S | 6 | una vez | 8 | P1 | big magic moment (add fx_magic_ring) |
| `snap_summon_S` | S | 4 | una vez | 10 | P1 | make something appear (add fx_puff where it appears) |
| `levitate_S` | S | 4 | bucle | 4 | P2 | an object floating over his hands (object drawn separately) |

### Gestos y social

| id | dir | cuadros | modo | fps | prio | para qué |
|---|---|---|---|---|---|---|
| `wave_S` | S | 4 | bucle | 8 | P0 | hello / goodbye |
| `point_E` | E (+W espejo) | 3 | queda en el último | 8 | P1 | look at this (W = mirrored) |
| `thumbs_up_S` | S | 3 | queda en el último | 8 | P1 | approval, 'listo' |
| `talk_S` | S | 4 | bucle | 8 | P1 | explaining something to the camera (no speech bubble text) |
| `offer_mate_E` | E | 3 | queda en el último | 8 | P0 | offering mate to a guest |
| `bow_S` | S | 4 | una vez | 8 | P2 | thank you |
| `shrug_S` | S | 3 | queda en el último | 8 | P1 | 'qué le vas a hacer' |

### Sentado

| id | dir | cuadros | modo | fps | prio | para qué |
|---|---|---|---|---|---|---|
| `sit_down_S` | S | 4 | una vez | 8 | P1 | sit on a stool or chair (seat drawn separately) |
| `sit_mate_S` | S | 4 | bucle | 4 | P1 | calm ending |
| `sit_doze_S` | S | 4 | bucle | 3 | P2 | night shift while a print runs |

## Taller: objetos con estados

| id | estados | modo | prio | para qué |
|---|---|---|---|---|
| `printer` | 4 | estados | P0 | the shop's printer; frames 2-3 loop while printing |
| `door_R` | 3 | estados | P0 | people come in and out |
| `stool` | 1 | fijo | P0 | seat for guests (separate so a sitting character can overlap it) |
| `fan` | 3 | bucle | P1 | summer heat gag, ambient loop |
| `gift_box` | 4 | estados | P1 | reveals and unboxings |
| `sack` | 4 | estados | P0 | Santa's sack filling up |
| `mate` | 1 | fijo | P1 | the wizard's mate when it is not in his hand |
| `xmas_tree` (navidad) | 2 | bucle | P0 | corner decoration, blink at 2 fps |
| `garland` (navidad) | 2 | bucle | P0 | above the window, blink at 2 fps |
| `wreath` (navidad) | 1 | fijo | P1 | on the door |

## Efectos

| id | cuadros | modo | prio | para qué |
|---|---|---|---|---|
| `fx_sparkle` | 4 | una vez | P0 | anything appearing or shining |
| `fx_puff` | 4 | una vez | P0 | poof, landing, disappearing |
| `fx_confetti` | 4 | una vez | P0 | celebration |
| `fx_hearts` | 4 | una vez | P1 | love, gift received |
| `fx_sweat` | 4 | bucle | P0 | heat, nerves |
| `fx_idea` | 4 | una vez | P0 | eureka (no text) |
| `fx_steam` | 4 | bucle | P2 | anger, heat |
| `fx_swirl` | 4 | bucle | P1 | confusion (instead of a question mark) |
| `fx_moth` | 2 | bucle | P0 | empty sack / empty wallet gag |
| `fx_magic_ring` | 4 | una vez | P1 | spells |
| `fx_notes` | 4 | bucle | P2 | happy, music |
| `fx_dust_motes` | 2 | bucle | P2 | ambient sunbeam |

## Ítems del catálogo

`cafe`, `banana`, `suculenta`, `hamster`, `calavera`, `garaje`, `panal`, `plegable`, `medieval`, `perros-gatos`, `domino`, `hoja`, `driftwood`, `maceta`, `bowl`, `cassette`
