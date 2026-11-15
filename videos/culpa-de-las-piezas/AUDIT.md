# "Culpa de las piezas": script audit (scheduled run, 2026-11-13, 2:00 Montevideo; arrived on time)

The first draft is reel 5 in `../PLAN_AJEDREZ.md` (2026-11-07). I audited it against:
- the rules that changed in `../RESEARCH_AJEDREZ_2_2026.md`;
- the synthesis in `../RESEARCH_AJEDREZ_2026.md`;
- the skill's lessons.

As asked, no new research team was used. The owner gave the Christmas cut-off on 12/11: **the last day to order is 23 December**.

## Checklist

| Check | First draft | Verdict | Change |
|---|---|---|---|
| Product named in words in frame 1 | Hook "Revancha" over a mid-game board | **Missing**: "revancha" means nothing to a new viewer | Hook "Ajedrez vikingo vs. medieval / impreso en 3D" from the first frame, with a small "LA REVANCHA" badge (the callback for followers of reel 1) |
| One joke, a comic engine | "¡Me hicieron trampa las piezas!" — every piece turns to face him — "Las piezas no pierden. Vos sí." | **Keep**, sharpen | The viking king tips over (mate again, the scholar's mate position: a real chess joke for players). His own army, the vikings, turn round one by one to stare at him, while he sweats. El Mago, deadpan: "Las piezas no pierden. Vos sí." |
| From the joke to the want | "Quiero el mío. Para Navidad." | **Keep** | The take added a sulking "Mmm…" before it: kept, and the subtitle matches what was said. Papá Noel wanting a gift for himself is the second smile |
| The work shown honestly | "The printer starts, the warm glow" | Vague | A red viking king (his colours, a callback to reel 3) rises layer by layer under the glow cap, no failed print, while El Mago says "un juego lleva muchas horas de impresora" |
| Honest urgency with the real date | "Pedí antes del [fecha]" | **The date was missing**; "antes del" would have meant the 22nd | The owner's date, as the last day included: Papá Noel asks "¿Hasta cuándo lo puedo pedir?", El Mago answers "Hasta el veintitrés de diciembre." A calendar page shows **23 DICIEMBRE · último día para pedir**, circled in red. It is the last order day, never a delivery promise |
| Real proof BEFORE the CTA | Photos, then CTA | **Keep** | "Así son de verdad": vikingo, medieval, medieval in colours |
| ONE comment CTA with a reward | "Comentá PEDIR y te paso precio y fecha." | **Keep** | — |
| "Las piezas; el tablero va aparte" | — | Fits the caption, not the video | In the caption |
| No price, weight, felt or finish claims | — | OK | — |
| The draft caption | "Para que llegue antes de Navidad, pedilo antes del [fecha]" | **A delivery promise**, and the wrong day | Rewritten: "Los pedidos para Navidad van hasta el 23 de diciembre. Un juego completo lleva muchas horas de impresora: cuanto antes, mejor." |
| The loop | Card with the date | Accepted as a reset | The card shows the same mid-game as frame 1, the king standing again (the reset happens under the proof panel) |
| Length | about 22 s planned | 24.2 s measured | — |

## The voices (measured)

| Line | Text | Length |
|---|---|---|
| s1 | ¡Me hicieron trampa las piezas! | 1.98 s |
| m1 | Las piezas no pierden. Vos sí. | 2.45 s (pause after "no pierden" 0.62 → 0.42 s) |
| s2 | Mmm… quiero el mío. ¡Para Navidad! | 2.39 s (two inner pauses shortened) |
| m2 | Entonces no esperes: un juego lleva muchas horas de impresora. | 3.43 s |
| s3 | ¿Hasta cuándo lo puedo pedir? | 1.05 s |
| m3 | Hasta el veintitrés de diciembre. | 1.61 s |
| m4 | Comentá PEDIR y te paso precio y fecha. | 2.73 s |

The automatic split put "¡Para Navidad!" at the start of s3: the take added a sulking "Mmm…", and its pauses were as long
as the gaps between lines. s2 and s3 were re-cut by hand from the take (`voces.json` → `_cuts_from_take`). `tts_lineas.py`
now takes a list of squeezes for one line. Every clip was checked by transcription; m3 read back as "hasta el 23 de
diciembre".
