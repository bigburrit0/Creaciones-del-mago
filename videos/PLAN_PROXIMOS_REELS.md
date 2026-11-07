# The next three 3D reels: drafts and execution plan

Drafted 2026-11-07 from the Haiku research team's findings (`RESEARCH_IDEAS_2026.md`) and built with the
`skills/reel-3d-toon` workflow and its lessons. One story per selling moment, each with a format people already
recognise, a product that is safe to sell, and El Mago's running gags: the mate, the printer, and "¡A imprimir!".

| # | Reel | Selling moment | Format | Product on screen | Publish |
|---|---|---|---|---|---|
| 0 | Papá Noel en ojotas (done) | Christmas | story + reveal | clickers, gifts | **by Fri 20 Nov** (before Black Week) |
| 1 | **Invisible no era** | Amigo invisible (December) | deadpan two-character comedy + reveal gag + clicker ASMR | clickers and keychains, two mini figures of the characters | **Tue 1 Dec** |
| 2 | **¿Reyes Magos? Mago soy yo** | Día de Reyes (6 Jan) | process reveal (layer by layer) + pun | an original articulated camel, a model car | **Mon 28 Dec** (latest Mon 4 Jan) |
| 3 | **Ola de calor, vuelta a clases** | Back to school (early March) | transform on the beat (beach → workshop) | multicolour name keychains for backpacks, pencil holder | **Fri 20 Feb** (latest Fri 26 Feb) |

The dialogue lengths below are estimates: in each reel the voices are generated first and the beats are timed to them.

---

## Reel 1: "Invisible no era" (20 s) — made 2026-11-07 (27 s), see `invisible-no-era/`

**Logline.** The workshop does its amigo invisible. Papá Noel and El Mago each draw the other's name and sneak to the
printer at night to make the gift in secret. They bump into each other at the printer. The gifts: a tiny El Mago
clicker and a tiny Papá Noel in ojotas keychain. Both click them at once.

**Why it works.** Amigo invisible is the most common, dated gift problem in December; the two-character deadpan and the
reveal gag are 2026 formats; and the clicker ends the reel on a satisfying ASMR click loop. Papá Noel comes back from
the Christmas reel (a recurring cast builds the series).

| Time | Shot | Action | Line (who) |
|---|---|---|---|
| 0–2.5 | close, bowl of papelitos | Papá Noel draws a slip, reads it, looks sideways at El Mago, hides it | S: "¡Me tocó…!" |
| 2.5–4.5 | two-shot | El Mago draws his, reads, looks at Papá Noel, finger to his lips | M: "Shhh." |
| 4.5–9 | wide, NIGHT (moonlight, printer LED) | both sneak to the printer from opposite sides (`Crouch_Fwd_Loop`), flip-flops squeak; they meet at the printer | — |
| 9–11 | two-shot | freeze, deadpan stare; both whistle and look away | S: "¿Vos también acá?" M: "Yo… pasaba." |
| 11–13.5 | insert, printer | the printer runs; each hides his piece behind his back | — |
| 13.5–17.5 | two-shot, day | the exchange: Papá Noel gives El Mago a tiny El Mago clicker, El Mago gives Papá Noel a tiny Papá Noel-in-ojotas keychain; both click in sync (click, click, click) | S: "¡Jo, jo! ¡Soy yo!" M: "Invisible no era." |
| 17.5–20 | close on the two minis + card | "Clickers y llaveros para el amigo invisible · ¡Pedí el tuyo! · Escribime por mensaje" | M: "Clickers para el amigo invisible. ¡Pedí el tuyo!" |

**Assets.** Reuse the workshop, both characters, the printer. New: a bowl and paper slips; a night lighting preset
(blue moonlight, warm printer LED, desk lamp) blended to day; the two mini figures (the character GLBs cloned at
~0.08 scale in a fixed pose, with a ring and a clicker base); click sound and a sneaking "squeak" in the synth.
Clips: `Crouch_Fwd_Loop`, `Crouch_Idle_Loop`, `Idle_Talking_Loop`, `PickUp_Table`, `Interact`.

**Risks (lessons that apply).** Two bodies meeting at the printer: meeting distance from the colliders, never
overlapping (the brim disc vs Papá Noel's floppy hat). Hands behind the back: IK targets pushed out of the robe and the
belly, palms checked. Tiny props in hands: the hold point and the QA radius scaled to the prop. Night lighting: keep
the outlines readable (check frames at night before the gate).

**Caption hook.** "¿Te tocó alguien en el amigo invisible y cero ideas? El Mago tampoco sabía disimular."

---

## Reel 2: "¿Reyes Magos? Mago soy yo" (20 s)

**Logline.** The night of 5 January. Kids' shoes by the door with grass and a bowl of water for the camels. El Mago
puts a crown on his hat: "¿Reyes Magos? ¡Mago soy yo!". A letter asks for a camel. The printer builds an articulated
camel layer by layer; it comes alive, drinks the camels' water and eats the grass, while El Mago sips his mate. In the
morning the shoes have gifts.

**Why it works.** The pun is built into the brand (Reyes **Magos** / El **Mago**); the Uruguayan shoes-with-grass-and-
water tradition is instantly local; the layer-by-layer process reveal is the strongest 3D-printing format; and
articulated animals are among 2026's most-printed products (use an original or commercially licensed camel).

| Time | Shot | Action | Line |
|---|---|---|---|
| 0–2 | close | three pairs of kids' shoes, grass, a bowl of water, moonlight | — |
| 2–5 | medium | El Mago puts a little gold crown on his hat, proud | M: "¿Reyes Magos? ¡Mago soy yo!" |
| 5–7.5 | insert | a kid's letter: "Querido Rey Mago: quiero un camello" | M: "¿Un camello? ¡A imprimir!" |
| 7.5–12.5 | insert, printer | the camel grows layer by layer (a rising clip plane, glowing nozzle line, time-lapse), then a model car | — |
| 12.5–16 | wide | the camel wobbles to life, walks (articulated segments) to the bowl, drinks and eats the grass; El Mago sips his mate beside it | M: "Cada uno con lo suyo." |
| 16–17.5 | wide, dawn | gifts in the shoes; a postcard in the window shows Papá Noel on holiday at the beach (cameo) | — |
| 17.5–20 | card | "Regalos de Reyes impresos en 3D · Pedí con tiempo: mínimo 48 h · Escribime por mensaje" | M: "Para Reyes, pedí con tiempo." |

**Assets.** New: a crown (a rigid prop on the head bone), kids' shoes, a grass tuft, a water bowl, a letter, a model
car, and **the camel**: segmented and rigged procedurally in Blender (body, neck, head, four three-segment legs), animated
with procedural cycles (no humanoid mocap fits it). A layer-reveal material: a clip plane rising with the print, with
the outline clipped too. A night-to-dawn light change.

**Risks.** The camel is the longest job: its legs must plant without sliding (measure its stride like the walk
speed), and its head must reach the water without entering the bowl's rim (add bowl and camel colliders to the gate).
The crown rests on the hat, so it takes the hat's weights (or is parented to the hat's base bone). The clipped outline
must not leave a floating ring.

**Caption hook.** "Los Reyes Magos son tres. El Mago es uno solo, pero tiene impresora."

---

## Reel 3: "Ola de calor, vuelta a clases" (18 s)

**Logline.** A heat wave on the rambla at Pocitos. El Mago under a beach umbrella in his robe, sweating, with his mate
and termo: "Ahh… esto es vida". His phone buzzes: "Vuelta a clases: lunes 1 de marzo". Panic. A magic spin on the beat
and he is in the workshop: "¡A imprimir!". The printer turns out multicolour name keychains (SOFI, MATEO, JOACO) and a
pencil holder, which jump onto a row of backpacks.

**Why it works.** The heat wave and the beach are this summer's safest, most local joke; the transform on the beat
(beach → workshop) is a known 2026 structure; personalised name keychains are a top trending product and the most
obvious back-to-school buy; and "Ahh… esto es vida" calls back to Papá Noel's line.

| Time | Shot | Action | Line |
|---|---|---|---|
| 0–3 | wide, beach | sun, sand, the rambla wall, a seagull; El Mago in a beach chair under an umbrella, fanning himself with his hat brim | M: "Ahh… esto es vida." |
| 3–5.5 | close | his phone buzzes: "Vuelta a clases: lunes 1/3" | M: "¿¡Marzo!? ¿¡Ya!?" |
| 5.5–7 | on the beat | magic spin with sparkles: a whip cut from the beach to the workshop | M: "¡A imprimir!" |
| 7–12.5 | insert, printer | time-lapse of three multicolour name keychains and a pencil holder | — |
| 12.5–15 | wide | the keychains hop onto three backpacks, one by one, with a "ding" each | M: "Uno para Sofi, uno para Mateo…" |
| 15–18 | card | "Llaveros con tu nombre · Vuelta a clases · Escribime por mensaje" | M: "Con tu nombre. ¡Pedí el tuyo!" |

**Assets.** New set: beach (sand, sea and sky backdrop, the rambla wall, an umbrella, a beach chair, a termo, a
seagull with procedural flapping). A name-keychain generator in Blender (text to mesh with bpy, multicolour layers, a
ring), so any name can be made later for orders. Three backpacks. A phone prop. The spin transition (a camera whip and
a sparkle burst, cut on the beat). Clips: `Sitting_Idle_Loop` or a reclined pose for the chair, `Sitting_Talking_Loop`,
`Jump_Start` for the panic, `Spell_Simple_*` for the spin (check that it doesn't sweep through the beard: if it does, use
IK as in the throws).

**Risks.** Sitting in a beach chair: the robe and beard against the chair (chair colliders; the beard rests on the
body, not the chair). Hat-brim fanning is a hand at the face: contact guard and palm check. Keychains jumping onto
backpacks: arcs and their landing points outside the straps. Text legibility of the names at phone size (letters at
least 4% of the frame height in the insert).

**Caption hook.** "Estabas en Pocitos con 35° y te acordaste de la mochila. Tranqui: el Mago imprime los nombres."

---

## Execution plan

**Step 0: a shared scene kit (do once, before Reel 1).** Move the reusable parts of `papa-noel-en-ojotas/hf3d/index.html`
into `videos/biblioteca/3d/web/escena3d.js`:
- the room and door builder;
- characters and colliders;
- the IK queue and contact guard;
- the props helpers;
- the subtitles, talk nods and end card;
- `qa()` with every check;
- the shot list.

A new reel's `index.html` should then hold only its timing, routes, actions and shots. Add a lighting preset switch (day,
night, dawn) and rigid accessory props on bones (crown, sunglasses). Estimate: one session.

**For each reel, in order** (the workflow in `skills/reel-3d-toon/SKILL.md`):
1. Script and dialogue in `GUION.md`.
2. Voices: one TTS request per character, checked and trimmed. Then time the beats to the measured lines.
3. Build the new props and characters, with the QA additions listed for each reel.
4. Scene, then frame previews of the risky moments, then window QA.
5. Full QA gate (0 bad frames), then render (~15 min), then the flicker scan, loudness check and voice check.
6. Caption: three Haiku writers, curated by hand.
7. Commit, push and deliver for approval.

**Schedule.** Production goes a week or more ahead of each publish date, leaving room for changes:

| Window | Work |
|---|---|
| 9–20 Nov | Step 0; publish the Christmas reel (by 20 Nov) |
| 16–27 Nov | Reel 1 (amigo invisible); publish Tue 1 Dec |
| 30 Nov – 18 Dec | Reel 2 (Reyes): the camel rig is the long pole; publish Mon 28 Dec |
| 4 Jan – 12 Feb | Reel 3 (vuelta a clases): new beach set, name generator; publish Fri 20 Feb |

**Before each publish date, check locally:**
- the last order date for delivery in time (48 h minimum);
- the ANEP 2027 school calendar, for Reel 3;
- that every model shown on screen can be sold (original, or a commercial licence).

**Backups if a slot needs replacing:**
- Carnaval or Enamorados (publish by 5–9 Feb). Keep Llamadas and candombe respectful, not a costume gag.
- Semana de Turismo (publish by 24 Mar).
- An evergreen "ómnibus que no viene" reel with a chess set or a model car to kill the wait.
