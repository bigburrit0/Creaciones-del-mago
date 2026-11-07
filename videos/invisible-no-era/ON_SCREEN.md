# "Invisible no era": everything on screen, by category

Written before building (BRIEF.md: "create categories for everything that will go on screen and make sure everything in
that list is carefully crafted"). Each item: what it must look like, the detail it needs, how it moves, and the check
that proves it is done. ✅ = done and checked (evidence in brackets).

## 1. Story beats (27 s, voice first; line lengths measured: s1 2.45, m1 1.83, s2 1.75, m2 1.37, s3 2.47, m3 1.05, m4 2.57)

| Time | Beat | Lines |
|---|---|---|
| 0.0–3.6 | Day. A bowl of folded slips under a hand-lettered "AMIGO INVISIBLE" sign. Papá Noel draws a slip, unfolds it, reads "El Mago" (insert), glances at El Mago and hides it behind his back | S: "¡Uy… me tocó!" |
| 3.6–7.2 | El Mago draws, reads "Papá Noel" (insert), looks at him, finger to his moustache | M: "Shhh… es secreto." |
| 7.2–7.9 | Time card "Esa noche…" (the light turns to night behind it) | — |
| 7.9–11.4 | Night. Both tiptoe to the printer in a crouch from opposite sides; they reach for the button together; freeze, heads turn, eyes meet | — |
| 11.4–15.3 | Caught: "¿Vos también acá?" / "Yo… pasaba." Both look away and whistle | S, M |
| 15.3–17.7 | Insert: the printer builds two tiny figures layer by layer; ding; each grabs one and hides it behind his back | — |
| 17.7–18.3 | Time card "A la mañana…" (dawn light) | — |
| 18.3–24.0 | Exchange: Papá Noel gives El Mago a tiny El Mago clicker; El Mago gives Papá Noel a tiny Papá Noel keychain. Each looks at himself in miniature; three clicks in sync; deadpan to camera | S: "¡Jo, jo! ¿Soy yo?" M: "Invisible no era." |
| 24.0–27.0 | End card | M: "Clickers para el amigo invisible. ¡Pedí el tuyo!" |

## 2. Characters and acting

| Item | Must look like / detail | Motion | Check |
|---|---|---|---|
| Papá Noel | the approved model (beard on the tank top via transferred weights, sunglasses, floppy hat) | idle → reach into the bowl → read → glance (head turn) → hide hand behind his back; crouch-walk (`Crouch_Fwd_Loop`); freeze with head turn; look away and up while whistling; hand-off and click; laugh nods driven by his voice | beard gate 0; hands vs own face 0; preview frames at each beat |
| El Mago | approved v2 model | same arc mirrored; finger in front of the moustache (never inside the beard) for "Shhh"; deadpan to camera for the punchline (head turns to the lens) | hand-own-face 0; preview of the "Shhh" and punchline frames |
| Faces | eyes, brows, blinks | blinks every 3–5 s; brows up on the reveal and when caught; El Mago's eyes dart left-right in the freeze | preview frames at 2.5, 5.4, 11.2, 22.5 |
| Weight and timing | anticipation before each reach, follow-through after, a small settle after the freeze | eased IK weights (0.25–0.35 s in, 0.2 s out) | no pose jumps (gate) |

## 3. Hands and props in hands

| Item | Detail | Check |
|---|---|---|
| Paper slips (2 drawn + 7 in the bowl) | folded paper, two panels on a hinge, cream with a slight blue ruling, the name hand-lettered in marker ("El Mago", "Papá Noel") on the inner face, a crease line, outline | the slip follows the palm (attached to the hand, not floating); readable at phone size in the insert |
| Hide behind the back | hand target behind the hips, outside the robe/belly colliders | hand-other, bodies 0; no wall/bench crossing |
| Finger to the moustache | target 6 cm in front of the moustache | hand-own-face 0 |
| Reach for the printer button | hands converge from both sides, stop 10+ cm apart | hand-other 0 |
| Tiny figures (gifts) | real miniature El Mago and Papá Noel (the same models, about 12 cm), on a clicker base (a keycap) / with a keyring; outlines; printed colours | owner changes are animated (picked from the printer bed, hidden, handed over at a meeting point); gift vs bodies 3.5 cm |
| The clicks | three presses in sync, thumbs dip 1 cm, a click sound each | sound on the frames of the press |

## 4. Hero props and set dressing

| Item | Detail | Check |
|---|---|---|
| Bowl of slips | glazed ceramic bowl (lathe with a lip, two-tone glaze, a darker inner colour), the slips heaped inside with jittered angles | on a small round table between them; nobody passes through it (furniture check in QA) |
| "AMIGO INVISIBLE" sign | paper taped to the back wall with two strips of tape, hand-lettered, a little gift doodle, a slight tilt | readable in the wide shots |
| Printer | builds the minis: head moving, nozzle glowing, the minis revealed bottom-up by a rising cut plane, a faint glowing line at the cut | insert preview at 15.8 and 16.5 |
| Workshop | the same set as the Christmas reel (shelves, spools, thermos, mandarins, tree, rug) | — |
| Furniture | bench, side table, stool are solid for the characters | QA furniture boxes: 0 |

## 5. Light, time of day and atmosphere

| Item | Detail | Check |
|---|---|---|
| Day | the Christmas reel's warm summer light | — |
| Night | moonlight through the window (night sky with a moon and stars), cool blue fill, a warm desk-lamp pool on the bench, the printer's blue LED glow, cool dust motes | preview at 9.0 and 13.0: faces still readable, outlines visible |
| Dawn | warm pink low sun | preview at 19.0 |
| Changes | only under the time cards (no visible pop) | previews at the card edges |

## 6. Camera and editing (the V2 style)

Framed shots from measured heads; hook title; snap zooms on the reveals and the freeze; whip pans into the sneaking and
out of it; inserts on the slips and the printer bed; a two-shot for the exchange; a deadpan close-up for the punchline.
Every camera looks toward the back or side walls. Check: preview of every shot (contact sheet), nothing blocked by the
tree or the door.

## 7. Text on screen

| Item | Detail | Check |
|---|---|---|
| Hook title | "Amigo invisible en el taller" 0.15–1.9 s | inside the top safe area (y ≥ 220) |
| Kinetic captions | word by word, speaker colours | bottom of the pill row at y ≤ 1470 |
| Time cards | "Esa noche…", "A la mañana…" on a dark purple band, Fredoka, short pop | readable, 0.6 s each |
| End card | "¿Amigo invisible? · Clickers y llaveros impresos en 3D · ¡Pedí el tuyo! · Escribime por mensaje · Creaciones del Mago · Montevideo" | no phone number in the video |

## 8. Sound

Voices (-16 LUFS per line, music ducked under each); paper rustle on each draw and unfold; tiptoe pizzicato steps during
the sneak; a "freeze" sting when they meet; whistling; printer whir and a ding; pops on each hand-off; three clicks in
sync; the end chord. Check: final mix about -13/-14 LUFS, every line intelligible (transcription), no clipping.
