# "Elegí tu bando": script audit (scheduled run; done on 2026-11-12)

The first draft is reel 3 in `../PLAN_AJEDREZ.md` (2026-11-07). I audited it against:
- the rules that changed in `../RESEARCH_AJEDREZ_2_2026.md`;
- the synthesis in `../RESEARCH_AJEDREZ_2026.md`;
- the skill's lessons.

As asked, no new research team was used.

## Checklist

| Check | First draft | Verdict | Change |
|---|---|---|---|
| Product named in words in frame 1 | The viking army in bronze; Papá Noel points | **Missing** | Hook "Ajedrez vikingo / impreso en 3D, en tus colores" from the first frame, over the whole set and Papá Noel |
| One joke | "¡Ese rey soy yo!" / "Bueno… vikingo sos." | **Keep**, and make it the feature | The joke *is* the four colours: the king gets red, white, skin and black one step at a time, until it looks like Papá Noel. Then it turns round to face him |
| Magic reads as magic | "A wand sweep" (there is no wand prop) | Keep the idea | El Mago's raised hand plus sparkles swirling over each piece as it changes, rank by rank. No smoke |
| The per-side choice (the gap no competitor shows) | Only Papá Noel's side changed | **Unclear**: one side only | Two simple decisions, seen and labelled: his side red and white, then El Mago's side purple and gold (his own colours); badges "un bando" / "el otro" with the colour dots |
| "Hasta cuatro por pieza" | "Close-up: a four-colour piece" | Vague | The king close-up with a "4 colores" palette whose dots pop in as each colour lands |
| The product after the joke; real proof before the CTA | Photos, then CTA | **Keep** | Three real colourways from the site: bronze (vikingo), red and black (medieval), gold and grey (medieval) |
| ONE comment CTA with a reward | "¿Qué colores le pondrías vos? Comentá COLORES." | **No reward** | "…Comentá COLORES y te paso precio y fecha." |
| No weight, felt or finish claims | — | OK | — |
| The loop | Card over the set | Accepted as a before → after | The first frame shows the set in bronze and silver; the card shows it in red and white against purple and gold. It is a transformation, not a loop |
| Length | 22 s planned | 21.6 s measured | — |

## Changes made while building

- **The TTS split put "¿Qué colores le pondrías vos?" into m3.** m3 and m4 were re-cut from the take at the measured pauses (`voces.json` → `_cuts_from_take`), and m4's pause between its two sentences was shortened.
- **The king's close-up was too tight** (head cut off) and blocked by neighbours. The camera moved to a raised three-quarter view, 23 cm out and 16 cm up.
- **The king's turn was seen from behind.** It is now shot from Papá Noel's side, so the king turns to face him and the viewer.
- **QA flagged an elbow flip** at the start of El Mago's pointing (a 0.35 s reach). It is now 0.55 s; the gate passes with 0 jumps.
