# November, second wave: four chess reels with the shop's other sets (scripts, 2026-11-14)

The research is in `RESEARCH_NOVIEMBRE_2_2026.md`. The owner chose **other chess sets, new stories**: the first draft of
this plan (a dogs-eager joke, a suitcase, a broken running gag, a puzzle Papá Noel can't solve) was replaced by the four
scripts below.

The rules stay the same:
- the product is named in words in frame 1;
- one joke, which a non-player gets in 3 s and which proves a real feature;
- real photos (the product's own photo from `assets/p`), then ONE comment CTA that rewards the comment with price and date;
- honest urgency: the last day to order for Christmas is 23 December, never a delivery promise;
- no prices, weights, finish claims or trademarks.

What is new for this wave:
- **Other sets:** dogs vs cats, the travel chess, ancient Greece, the puzzle board.
- **Other settings:** none of these reels happens at the workshop's chess table:
  - Papá Noel's holiday living room;
  - the beach;
  - a top-down labyrinth;
  - the Christmas Eve table.
- **Music:** the soft ambient bed (`"style": "ambient"` in `chiptune.py`, page volume 0.22, checked with `biblioteca/nivel_musica.py`).
- **Sound effects:** never on a spoken word.

The scheduled runs build them one per night at 2:00 (15, 16, 17 and 18 November). Voices first, as always: the times
below are estimates until the voices are measured.

| # | Reel | Stage | Set (photo) | Setting | Joke | CTA | Publish |
|---|---|---|---|---|---|---|---|
| W1 | **Los gatos tiran todo** | reach | Perros contra gatos (`perros-gatos.webp`) | Papá Noel's holiday living room | The cat queen pushes a dog pawn off the table, slowly, looking at him | PERRO / GATO | Sun 29/11 |
| W2 | **La gaviota** | consideration | Ajedrez de viaje (`plegable.webp`) | The beach, a summer afternoon | A seagull steals his king from an open board; the travel set keeps the pieces inside | VIAJE | Thu 3/12 |
| W3 | **El laberinto** | reach | Antigua Grecia (`grecia.webp`) | Top-down: a stone labyrinth that becomes the board | Papá Noel gets lost in the board's Greek-key border | MINOTAURO | Sun 6/12 |
| W4 | **El mantel** | conversion, cross-sell | Tablero rompecabezas (`tablero.webp`) | The Christmas Eve table | He plays his new pieces on a checked tablecloth | TABLERO | Sun 13/12 |

The chess series' reel 5 ("Culpa de las piezas") stays on Thu 26/11 (Black Friday week). N2 "Mandame una foto" and N3
in `PLAN_NOVIEMBRE.md` are still waiting for the owner's decision.

**Facts to confirm with the owner (until then, only the site's own words):**
- Travel chess: the site says "se pliega en un tubo de 24 cm con las piezas adentro". Does the board fold into the tube?
- Dogs vs cats: can each side be in its own colours?
- Puzzle board: how many parts, and what colours?

---

## W1 "Los gatos tiran todo" (reach, about 24 s)

**Idea.** Everyone who has had a cat knows it: cats push things off tables, slowly, while looking at you. Here the cat
side plays like a cat. The feature: cats on one side, dogs on the other, and you choose your side. The two-choice CTA
brings comments and tags.

| Time | Visual | Line |
|---|---|---|
| 0-2 | Papá Noel's holiday living room (sofa, rug, a small tree, the sea in the window); the dogs-vs-cats set on a low table; hook "Ajedrez perros vs. gatos / impreso en 3D" | S: "¡Yo juego con los perros!" |
| 2-4 | El Mago settles on the other side | M: "Y yo, con los gatos." |
| 4-6.5 | a dog pawn hops forward, eager, its tail wagging (a spring) | — |
| 6.5-10 | the cats' turn. The cat queen walks to a dog pawn at the edge of the table, looks at Papá Noel, and pushes it off with a paw, slowly. A beat. It drops onto the rug (a soft "toc") | — |
| 10-12 | Papá Noel, outraged | S: "¡Eso no es una jugada!" |
| 12-14.5 | El Mago, deadpan | M: "Para un gato, sí." |
| 14.5-16 | every cat piece turns its head to Papá Noel, smug; the dog king's ears droop | — |
| 16-18.5 | real photo: "Así son de verdad" (`perros-gatos.webp`), "Los gatos de un lado, los perros del otro" | — |
| 18.5-22 | El Mago points at the viewer | M: "¿Perro o gato? Comentá tu bando y te paso precio y fecha." |
| 22-24.5 | card: "¿Perro o gato?", "¡Comentá tu bando!", "Pedidos para Navidad: hasta el 23 de diciembre" | — |

**To build:**
- the dog and cat pieces, modelled from the photo like `ajedrez3d.js`: hounds and pugs on round pedestals, cats with pointed ears; kings and queens with crowns;
- the living-room set;
- the cat queen's paw (a small arm on the piece, or the whole piece leaning and nudging).

The pushed pawn lands on the rug, never through the table or a body.

---

## W2 "La gaviota" (consideration, about 24 s)

**Idea.** Summer in Montevideo, and the city's seagulls. Papá Noel plays on the sand with an ordinary open board; a
seagull steals his king. The travel set keeps the pieces inside. Peak summer travel starts on 20 December.

| Time | Visual | Line |
|---|---|---|
| 0-2 | the beach on a summer afternoon: Papá Noel in flip-flops, an open board on a towel; hook "Ajedrez de viaje / impreso en 3D" | S: "¡Partidita en la playa!" |
| 2-4.5 | a seagull swoops in, grabs his king and flies off (a squawk) | — |
| 4.5-6 | Papá Noel jumps up, arms out | S: "¡Mi rey!" |
| 6-10 | El Mago pulls a small tube from his sleeve (sparkles); it shows the pieces inside, then closes with a click | M: "Por eso, el de viaje: se pliega en un tubo de veinticuatro centímetros, con las piezas adentro." |
| 10-12.5 | the seagull lands beside the closed tube, pecks it, gets nothing, and looks offended | — |
| 12.5-14.5 | Papá Noel, to the seagull, triumphant | S: "¡Ja! ¡Ahora no podés!" |
| 14.5-16.5 | the two playing on the towel at sunset | — |
| 16.5-19 | real photo: "Así son de verdad" (`plegable.webp`) | — |
| 19-22 | El Mago points at the viewer | M: "¿Te vas de vacaciones? Comentá VIAJE y te paso precio y fecha." |
| 22-24.5 | card with the 23 December order date | — |

**To confirm first:** the beat at 6-10 s shows what the site says (it folds into a tube, the pieces inside). If the owner
confirms the board folds into the tube, show the board folding up. Otherwise show the closed tube and the pieces coming
out of it, and keep the site's words.

**To build:**
- the tube and its pieces, from `plegable.webp`;
- the beach set: sand, sea, sky at sunset, a towel, an umbrella;
- the seagull, white and grey, with a wing flap and a beak that grips the king. The king flies off with it, carried and never teleported.

---

## W3 "El laberinto" (reach, about 23 s)

**Idea.** The Minotaur lived in a labyrinth, and the Greek board has a Greek-key (meander) border. Papá Noel follows it
with his finger and gets lost. The feature: Minotaur against Hercules, and this set comes with its own board, 52 × 50 cm.

| Time | Visual | Line |
|---|---|---|
| 0-2 | top-down: a stone labyrinth; the camera rises and it resolves into the Greek board; hook "Ajedrez de la antigua Grecia / impreso en 3D" | M: "Minotauro contra Hércules." |
| 2-4 | the two kings face off: the Minotaur lowers its horns, Hercules raises his club | — |
| 4-7 | Papá Noel follows the meander border with his finger, round and round, lost | S: "¿Y por dónde se sale?" |
| 7-9.5 | El Mago, deadpan | M: "Es un ajedrez. Se sale ganando." |
| 9.5-12.5 | a slow push-in over the whole board, a measuring tape along two sides | M: "Y este trae su tablero: cincuenta y dos por cincuenta." |
| 12.5-14.5 | Papá Noel, impressed, glasses down | S: "¡Qué tablero!" |
| 14.5-17 | real photo: "Así son de verdad" (`grecia.webp`) | — |
| 17-20.5 | El Mago points at the viewer | M: "Comentá MINOTAURO y te paso precio y fecha." |
| 20.5-23 | card | — |

**To build:**
- the Greek pieces from `grecia.webp`: a Minotaur king and Hercules king, plus simpler pieces (columns, helmets, amphorae, whatever the photo shows);
- the 52 × 50 board with a meander border;
- the top-down labyrinth that dissolves into it.

His finger follows the border without entering any piece.

---

## W4 "El mantel" (conversion and cross-sell, about 24 s)

**Idea.** Christmas Eve (24 December is officially "Día de la Familia" in Uruguay). Papá Noel got his red viking set
(reel 5) and plays it on his checked Christmas tablecloth. The puzzle board, for anyone who already has pieces.

| Time | Visual | Line |
|---|---|---|
| 0-2 | the Christmas Eve table: the red viking pieces set out on a red-and-white checked tablecloth; hook "Tablero de ajedrez impreso en 3D, por partes" | S: "¡Ya tengo mi ajedrez!" |
| 2-4.5 | El Mago looks at the tablecloth: too many squares, the pieces sitting on the lines and wobbling on a fold | M: "Eso es un mantel." |
| 4.5-6.5 | a pawn tips over on the fold; Papá Noel, unbothered | S: "¿Y qué tiene?" |
| 6.5-10.5 | El Mago snaps his fingers: the puzzle board's parts fly in one by one and click together on the table (top-down, satisfying) | M: "Un tablero reglamentario, que se arma por partes. Para las piezas que ya tenés." |
| 10.5-12.5 | the red vikings hop onto the board, rank by rank, steady | — |
| 12.5-15 | a calendar page: 23 DICIEMBRE, "último día para pedir" | M: "Pedidos hasta el veintitrés de diciembre." |
| 15-17.5 | real photo: "Así son de verdad" (`tablero.webp`) | — |
| 17.5-21 | El Mago points at the viewer | M: "¿Ya tenés las piezas? Comentá TABLERO y te paso precio y fecha." |
| 21-23.5 | card | — |

**To build:**
- the board's parts, from `tablero.webp`;
- the tablecloth: a cloth with a soft fold and 10 × 10 checks;
- the Christmas Eve table set;
- the calendar page, reused from "Culpa de las piezas".

The board "se arma por partes y no trae piezas": the viking pieces are his own, already bought.

---

## Caption notes (for the three caption writers, when each reel is made)

- Each caption names the product in its first line.
- Each caption answers the reel's one objection: which side, does it travel, is the board included, what about the board.
- Each caption ends with the WhatsApp number and the delivery zones.
- "Hasta el 23 de diciembre" is the last order day, never a delivery promise.

---

## Production steps for the scheduled runs (W1-W4, one per night at 2:00, 15-18 November)

Each run reads this section. `REEL` is the reel's folder name: `los-gatos-tiran-todo`, `la-gaviota`, `el-laberinto` or
`el-mantel`.

0. **Setup check.**
   - The container may have been rebuilt or restarted. Confirm `/opt/bpy`, `/opt/three/node_modules/three`,
     `/opt/fonts/node_modules/@fontsource` and `/opt/assets3d/ual` exist; if not, follow `videos/PLAN_3D.md` → "Reinstall".
   - Read `skills/reel-3d-toon/SKILL.md`, `references/lecciones.md` (all of it) and `references/qa.md`.
1. **Quick audit** (no new research team). Check the script against the rules above and in `RESEARCH_AJEDREZ_2_2026.md`:
   - the product is named in frame 1;
   - one joke that proves a real feature;
   - a real photo before the CTA;
   - ONE CTA with a reward;
   - honest urgency;
   - no price, weight, finish or trademark.
   Fix what fails, voice first, and write `videos/REEL/AUDIT.md` (keep / change / why).
2. **The reel**, in `videos/REEL/`, following `skills/reel-3d-toon`.
   - **Voices first.** Use `videos/biblioteca/tts_lineas.py`, one request per character (El Mago is Charon, Papá Noel is Algenib).
     - Check every clip's length against its words. When a split is wrong, re-cut by hand from the take with the split's own trim filter, record the cuts in `_cuts_from_take`, then run `--post-only` (a squeeze can be a list).
     - Transcribe every clip with `check_voces.py`. On a 429, wait 20 s or use `CHECK_MODEL=gemini-3.5-flash-lite`. Print the whole JSON.
   - **ON_SCREEN.md:** everything on screen, by category, each with its check.
   - **The scene.** Start from the latest finished scene (`videos/culpa-de-las-piezas/hf3d/index.html` and `build.sh` at first).
     - Model the new pieces from the product photo like `videos/biblioteca/3d/web/ajedrez3d.js`, without changing the existing pieces.
     - Build the new setting with every camera looking toward a wall, the sea or a backdrop.
     - Poses never read props placed later in the frame.
     - Nothing passes through anything (table, bodies, pieces). No prop teleports.
   - **Music:** only the soft ambient bed.
     - In `cues.py`: `"music": {"style": "ambient", "bpm": 120, "tonic": …, "mode": …, "chords": […], "chord_beats": 8, "duck": …, "end_chord": {"t": T["card"]}, "fade_out": […]}`. The page plays it at volume **0.22**.
     - Check with `python3 videos/biblioteca/nivel_musica.py videos/REEL/hf3d`: the bed about 20-25 dB under the voices and 12-16 dB under them in the gaps.
     - Never put a sound effect on a spoken word. No steady noise.
   - **Preview frames** at every risky moment.
     - El Mago's close-ups from below his brim.
     - No text in the top 232-400 px except the hook or badge.
     - Reaches last at least 0.5 s.
   - **QA gate:** 0 bad frames, the new set's furniture included.
   - **Render in the background with an explicit cd**:
     `bash -c 'cd /home/user/Creaciones-del-mago/videos/REEL/hf3d || exit 9; echo "cwd: $(pwd)" > ../render.log; npx hyperframes render --fps 60 --workers 4 -o ../REEL.mp4 >> ../render.log 2>&1; echo "exit $?" >> ../render.log'`.
     Check the first log line. If the container restarts mid-render, delete any stale `work-*` folder and relaunch.
   - **After the render:**
     - flicker scan: 0 frames;
     - loudness about -14 LUFS, peak under -1 dB (a sound-only fix goes through `remezclar.py`);
     - the steady-buzz check;
     - voices by transcription of the mix;
     - a contact sheet of REAL frames from the mp4, looked at before delivery.
3. **Copy.**
   - Use the three Haiku caption writers via SendMessage: `ad2446449fd1e351f` (humour), `ad05eff09effdc36b` (practical), `a5498758dc63992a4` (character). If one is unreachable, spawn a new Haiku writer with that angle.
   - Curate by hand into one caption plus the private-reply DM (ask "¿para quién es?"). Put them in `videos/REEL/GUION.md` and update this plan.
   - **Facts only** (first person singular, Rioplatense "vos"):
     - the product's own site line;
     - colours per side, up to 4 per piece, where the set allows it;
     - up to 25 cm per piece;
     - PLA (indoors) or PETG (sun, heavy use);
     - made to order, piece by piece;
     - price and date by WhatsApp 092 104 419, before starting, no commitment;
     - most sets are pieces only and the board is separate. Ancient Greece includes a 52 × 50 board; the travel chess folds into a 24 cm tube with the pieces inside;
     - the last day to order for Christmas is 23 December;
     - free delivery ONLY in La Unión, La Blanqueada and part of Buceo, shipping to all of Uruguay.
   - **Never:**
     - a phone number in the video;
     - a price;
     - any other date;
     - a delivery promise;
     - "48 h" for a set;
     - weight, felt, finish or magnet-strength claims;
     - trademarks or real people;
     - "envío gratis a todo Uruguay".
4. **Wrap up.**
   - Commit and push, the final mp4 included; never leave a stale render untracked.
   - Send the video with SendUserFile.
   - Update `.claude/handoff/HANDOFF.md` and the skill's lessons.
   - Write a short summary for the user IN SPANISH: what the audit changed, the checks, the caption and DM ready to paste, and the publish date.
   - Then stop. The next reel has its own run.

The Gemini key is a proxy-injected network secret: never print it. Keep model identifiers out of commits and files.

## Per-reel notes for the runs (order: W1 → W2 → W3 → W4)

| Reel | Folder (REEL) | Music (ambient) | Model and build | Publish |
|---|---|---|---|---|
| W1 Los gatos tiran todo | `los-gatos-tiran-todo` | tonic 0, ionian (cozy) | dog and cat pieces from `perros-gatos.webp`; the living room; the cat queen's slow push; the pawn falls onto the rug | Sun 29/11 |
| W2 La gaviota | `la-gaviota` | tonic 7, mixolydian (summer); a soft seagull call never on a word; no steady wave noise (a sea swell only below 300 Hz, checked with the buzz test) | the tube and its pieces from `plegable.webp`; the seagull (the king flies off WITH it, carried); the beach set, cameras toward the sea or a backdrop | Thu 3/12 |
| W3 El laberinto | `el-laberinto` | tonic 2, dorian, drone | the Minotaur and Hercules kings and simpler pieces from `grecia.webp`; the 52 × 50 board with a meander border at true size; the top-down labyrinth; the measuring tape at true scale; his finger never enters a piece | Sun 6/12 |
| W4 El mantel | `el-mantel` | tonic 0, ionian (warm, Christmas), sparse bells | the board's parts from `tablero.webp`; the tablecloth (10 × 10 checks, a soft fold that tips a pawn); the Christmas Eve table; the red vikings and the calendar page from `culpa-de-las-piezas` | Sun 13/12 |

**What the photos show (looked at on 14/11, before building):**
- `grecia.webp`: the board has red and gold squares inside a ring of white, rocky ruin walls with a Greek temple (columns and a pediment) on one side; the gold side has the Minotaur king on a column, the red side Hercules; the soldiers are hoplites with round shields. W3's "labyrinth" is these white walls seen from above (no meander border on the real board). Model the walls, the temple, the two kings and hoplites; the 52 × 50 cm includes the walls.
- `tablero.webp`: a black-and-white board in a grey frame with rounded corners. The photo does not show where its parts join: show four quadrants and the four sides of the frame clicking together, and keep the line to the site's words ("se arma por partes").
- `plegable.webp` (W2, done): an octagonal tube with the squares on its faces, toothed caps, faceted pieces in cream and tan inside.

A reel is **finished** when `videos/REEL/REEL.mp4` is committed and `videos/REEL/GUION.md` has a "Result" section.
