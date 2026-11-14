# Lessons: mistakes we already made, and the rule that prevents each

Each row: what the person saw → the real cause → the rule now → where it is enforced. Sources: the Christmas reel
(`videos/papa-noel-en-ojotas`, 2026-11-06/07) and `videos/RESEARCH_3D_CONTACT.md`.

## Glitches and determinism

| Seen | Cause | Rule | Where |
|---|---|---|---|
| Characters "glitching" (twitches, arms jumping) | three.js `AnimationMixer` skips writing a bone whose value did not change; HyperFrames draws some t twice, so procedural layers (IK, rotations) stacked on last frame's pose | Restore the pure clip pose snapshot before `mixer.update`, snapshot after; draw each t once (`lastT`) | `toon3d.js` `Character.apply`, `renderAt` |
| One-frame T-pose | Two back-to-back clips with zero total weight in between | Crossfades overlap and are eased; with no active clip, hold the nearest one | `Character.apply` |
| Elbow flips at the start of a reach | IK pole jumped to the designed one | Bend plane starts as the clip's own and turns gradually; eased takeover | `armNow` |
| NaN bones | Degenerate IK vectors | Guards in `aim` and `ikArm` | `toon3d.js` |

## Contact (nothing passes through anything)

| Seen | Cause | Rule | Where |
|---|---|---|---|
| Mate "ghosting" through faces | IK targets ignored the bodies | Colliders per character (head, face, beard, robe/belly, hat, brim as a disc, arms); targets pushed out with clearance; palm checked after solving; contact guard every frame | `addCollider`, `armNow`, `pushOut` |
| Hand through the beard when throwing | A casting clip swept through the body | No clip that sweeps through the body; throws are IK keyframes beside the head | scene |
| **Beard through the body "at the end"** | NOT only at the end: the beard tip was 4-6.5 cm inside the robe and belt in 1059 of 1140 frames. The beard followed chest bones (and springs) while the belt followed the hips: any pose bending the spine away from the bind pose drives them through each other | **A part resting on another takes the skin weights of the surface under it** (`toonchar.transfer_weights(part, supports, mask)`): beard on chin/robe/belt/shirt. Apply to every belt, scarf, cape, necklace, strap, hair on shoulders | `toonchar.py`, `mago3d.py`, `santa3d.py` |
| Springs did nothing | Spring gains gave 0.004 rad (invisible) | Measure spring amplitude after simulating; never let a spring rotate into the body (find the inward sign by probing, don't assume) | `simulateSprings` |
| **Santa through the door** | Walked from the door to the stool on a straight diagonal: crossed the wall plane beside the opening; the door panel swung into his path | **Walls, frames and door panels are solid** (QA checks them). Doorway width = widest body + carried prop + arm swing + 3 cm each side (Santa: 0.90 m). Cross through the MIDDLE, square to the wall (curve: straight through the door, then turn). Gestures (waving) at least 0.5 m inside the room | `PIN`/`POUT`, `qa()` |
| A sack floating in the doorway | Santa turned aside behind the wall; the sack trailed 0.3 m behind him and stayed visible | Carried props hide with their carrier: centre them on the body when exiting, walk straight away | `props` |
| Door closing would hit him | The door opened outward; its sweep covered his exit path | Choose the swing so a closing door never sweeps through anyone: here it opens INTO the room and closes behind him while he walks away | door setup |
| Mate jumping from the shelf to the hand | Owner changed from "bench" to "M" on one frame | Every change of owner is animated (hand-off at a meeting point, toss with an arc, a magic float with sparkles), and the hand reaches to catch | `poseAt` mate section |
| The floating mate went unchecked | QA had `owner = null` during the float window | QA has no blind windows: a prop in flight is checked against everyone | `qa()` |

## Camera and staging

| Seen | Cause | Rule |
|---|---|---|
| El Mago's face hidden by his hat in the last shot | Camera high (1.3 m) and close, looking down | For a character talking to camera: eye level (~0.8 m), ~3 m away, look target below him so he sits in the upper half (above the card) |
| Characters too close for the hand-off | Positions chosen by eye | Meeting points computed from the poses, between the bodies, toward the camera, outside both |

| V2 shots were extreme close-ups or the camera ended up behind a character | Camera coordinates guessed by eye; the characters are bigger than assumed, and the head bone sits at the neck | Frame character shots from the measured head position: frame height in metres at the subject, azimuth, elevation and vertical offset (`shotCam` in `hf3d-v2`), aim 10 cm above the head bone |
| Shots blocked by the foreground tree or the open door panel; the void showing | The set has no front wall; set dressing near the camera | Every camera looks toward the back or side walls; check frames for blockers (tree at (1.12, 0.65), the open door panel on the right) before rendering |

## Voices, subtitles, audio

| Seen | Cause | Rule |
|---|---|---|
| Lines too long for their beats | Voices generated after the animation was timed | Voice first: generate, measure, then time the beats. Interjections ("¡Ahh…!") are cheap to trim; full sentences are not |
| Short lines mangled (earlier reel: "No da" came out "Ah") | One request per short line | One TTS request per character with all its lines, cut at the N-1 longest pauses |
| Transcription ids shifted | Several clips in one transcription request | Transcribe clips one by one; send 16 kHz mp3 (a multi-WAV request failed with 502); no example words in the prompt (it biased "jo, jo, jo") |
| Voices vs music | — | Each line normalised to -16 LUFS; music ducked to 0.38 under each line; final mix around -13 LUFS; check the mix by transcription |
| Talking characters looked frozen | No mouths (beards) | Head nods and brow lift driven by the line's loudness envelope (60 fps), built by `build3d.sh` |
| Two subtitles on screen at once | Fade-out tails overlapped the next line | Each subtitle leaves before the next starts; no subtitle when the end card says the same |

## Process

- Renders and the QA gate run with the Bash tool's `run_in_background` (a plain `&` gets killed). Gate ~25 min, render
  ~15 min for 21 s: preview frames and window checks first.
- Commit and push after each working step.
- Free-tier Gemini TTS: about 3 requests per minute and 10 per day. Plan one request per character.
- Fonts are bundled from `@fontsource` (OFL), never fetched from Google Fonts at render time.
- The key is never printed: scripts send `proxy-injected`.
- Trademarked characters (Minecraft, Pokémon, One Piece, Star Wars) appear in the catalogue; in NEW reels prefer
  original or commercially licensed designs on screen (MakerWorld default licence is personal use only).

## From "Invisible no era" (2026-11-07, the first reel on the shared kit)

| Seen | Cause | Rule |
|---|---|---|
| — | 700-line scenes copied per reel | Build on `escena3d.js` (stage, set, light presets, cast, rig, props, voices, overlays, camera rig, QA). A refactor is finished only when the old reel renders **pixel-identical** frames (hash at 10 times) and passes its gate |
| Shots at the printer showed only backs and hats | Characters at a workbench face the back wall, and every camera must also look toward the walls | Stage so faces point at a usable camera: turn them to face each other, use POV inserts, or a high top view. Over-the-shoulder from above fails with big hats: put the camera at face height or re-stage |
| Hands brushing faces when reaching from a crouch | Crouch clips put the head at hand height | Rise out of the crouch to reach; give reaches near faces extra clearance (`arm(..., clear = 0.09)`) |
| El Mago inside the bench all day; Papá Noel's knot in the table | Positions chosen without measuring bodies against furniture | Furniture is solid in QA (boxes and cylinders vs every body collider). Measure first: robe r 0.23, belly r 0.26, Papá Noel's jacket knot reaches 0.36 m in front |
| Papá Noel could not reach the printer bed | His belly keeps him 0.6 m away | Bring the prop to the hand (a hand-over, or the workshop's magic: the figures hop into the hands) instead of stepping into furniture |
| Hands passing through the beard between two targets | Straight lines between targets cross the beard | Move hands along arcs that bulge forward (`via()`); hand-overs on the camera side; never reach across the belly |
| Pose jumps (elbow flips) | Moves under 0.4 s, hands going behind the back | At least 0.6 s for behind-the-back moves, 0.4–0.5 s for reaches; one arm never has two overlapping reaches (release first, then the next) |
| Night looked like day in close shots | The desk lamp at 2.4 lit the whole bench | Check every light preset on real frames; night lamp 0.8, LED 0.6 |
| A head turn read the camera position | `turnTo(…, camera.position)` used the previous frame's camera | Poses never read the camera (determinism): aim at a fixed point where the shot puts the lens |
| Staging changes and teleports | — | Hide them under a full-frame time card ("Esa noche…") and declare those windows in `window.__JUMP_OK` (the gate skips jumps only there) |
| The paper slip hidden by the hand | Slip centred on the palm | Hold paper above the mitten, facing the reader; POV insert at fov 55 so the slip fills the frame and the handwriting (Caveat) reads at phone size |
| A line came out different from the script ("¿Soy yo?") | TTS acting | Keep what works and change the subtitle to match what was said |
| One frame where the back wall drew over the bench and printer, dark and fogged (17.617 s) | The wall was one huge quad; from a steep top view its corners fell far outside the frustum and the software renderer lost depth and fog precision interpolating across it (CPU ray casts and every material setting were identical) | Tile big planes in ~0.5 m cells (done in the kit: walls, side walls, floor). The flicker scan on the rendered video is what caught it: never skip it |
| A debug hook silently missing | A `//` comment added on a one-line statement swallowed the code after it | Use `/* */` for comments in the middle of a line |

## From "Un regalo para cada amigo" (2026-11-07, the first selling reel; see `videos/RESEARCH_NOVIEMBRE_2026.md`)

| Seen | Cause | Rule |
|---|---|---|
| — | A reel made only to entertain doesn't sell | Selling structure: **hook with speech and text in the first 1.5 s, the product in frame 1 → identity or tension beats → process → real proof (the site's photos, `assets/p`) → ONE comment-type CTA** ("Etiquetá a ese amigo", "Comentá FOTO"). The WhatsApp number goes in the caption |
| A line came back as two lines and another got lost when the take was cut | An exclamation inside a line ("dice: ¡me muero!, por todo") has pauses longer than the gaps between lines | Read the take's silences (`silencedetect`), cut by hand, and store the cut points in `voces.json` → `_cuts_from_take`. Check each clip by transcription; one transcription can mishear a short clip ("mata" heard as "va"), so check it again before re-recording |
| Paper tags under every product sat behind the subtitles | In a close-up of a 9 cm piece, anything in front of it falls in the caption zone (y 1150-1470) | Label props with the counter badge and the voice line, not with objects in front of them |
| The neighbouring piece covered half of the hero piece | Products in an arc: each piece's neighbour is closer to the camera | Put products for hero shots **in a straight row facing the camera**, so neighbours stand beside each other, never in front |
| El Mago's hat in every product close-up | The brim is 0.58 m wide. At 0.3-0.6 m from the props it enters the frame from any angle | Keep characters ≥ 0.6 m from the hero props. If a character only narrates the close-ups, hide them (`W.visible = false`) **while posed in place**: no jump for the QA, nothing for the viewer to miss |
| "Hand to the forehead" (a faint) read as a fist at the mouth | The contact guard pushes a hand out of the face and brim colliders, so the hand lands lower | Gestures at the face don't work with these hats. Give the gag to the prop instead (the skull's ghost and x eyes) or to the whole body |
| A half-printed piece looked like a flat disc | Seen from straight above, a cut plane only shows the cross-section, and a big glow plane washes it out | Show printing from a 3/4 view (el ~30°) with a small glow cap the size of the piece |
| A forearm touched the closed door during a stretch | The stretching arm on the door side swung back | Point stretches toward the camera side. Here the full gate (1518 frames) took about 5 minutes: re-run all of it rather than a window |
| **"A weird buzz in the background"** (the person heard it at once) | Two synth bugs. (1) `write()` normalised every stem to a fixed peak, so the ambience's `level` was ignored: the cicadas (high-passed noise switched on and off at 37 Hz) played at full stem level under the whole reel. (2) Pulse waves carry a DC offset, which the music ducking moved up and down | Fixed in `chiptune.py`: ambience keeps its level (`boost=False`), and every stem goes through a 20 Hz DC block. **No cicadas under voices**; if a reel needs summer sound, use birds at a low level. After the render, check the mix for steady noise: look in the band above 6 kHz for a periodic envelope; the cicadas showed as a 37 Hz peak, 34 dB above the background |
| A sound-only fix would cost a 30-minute re-render | — | `videos/biblioteca/remezclar.py HF3D_DIR IN.mp4 OUT.mp4` rebuilds the mix from the page's `<audio>` clips (a plain sum matches HyperFrames' track, correlation 0.986), brings it to -14 LUFS with a gentle limiter, and swaps it in with the video stream copied byte for byte |
| The transcription check returned 429 all afternoon | The free tier allows 20 requests a day per model for `gemini-3.5-flash` | When it runs out, use `CHECK_MODEL=gemini-3.5-flash-lite` (its own quota). Keep a budget: about 9 clip checks plus 2 mix checks per reel |

## From "¿Vikingo o caballero?" (2026-11-07, chess series reel 1; `videos/RESEARCH_AJEDREZ_2026.md`)

| Seen | Cause | Rule |
|---|---|---|
| A joke built on a piece we don't sell (the Lewis berserker rook) | History research ran ahead of the product | Jokes and close-ups use only the shop's real pieces, modelled from its photos (`biblioteca/3d/web/ajedrez3d.js`). History appears only as an "inspired by" hook |
| "48 h" was about to promise a 32-piece set | The shop's minimum lead time is not the time to print a set | For sets: "te paso precio y fecha antes de empezar" and "un juego completo lleva muchas horas de impresora". A cut-off date only once the shop confirms it |
| "Y yo, caballero" transcribed as "hijo caballero"; "cebá uno" as "si va uno" | Rioplatense "y yo" sounds like "hijo"; a short imperative blurs | Avoid "y yo" at the start of a line and very short imperatives. Check every clip by transcription and re-record the line with clearer words |
| Low close-ups of a piece in its starting rank showed only its neighbours | A packed rank: every low line of sight passes through another piece | Shoot pieces from a raised three-quarter view (about 12 cm above the board, 20 cm out), from the empty middle of the board, or once they have moved. The low side view only works across the empty centre (the knights' face-off) |
| The red queen hid the viking king's fall | The piece that gives mate sits right in front of the king from the camera side | Place the camera for a falling piece on the side away from the attacker, raised above the pawns |
| Close-ups of El Mago hid his eyes | The brim is above the eye line | El Mago's close-ups at el -9° (from below the brim), aim slightly above the head |
| The gate passed the first time | No hands touch pieces (the pieces move by magic); characters stand outside the table's footprint (the slab is checked as a box, plus the legs) | Keep pieces character-free; check characters against furniture slabs and legs, not a solid box under a table |
| One flicker frame in a close-up while Papá Noel laughs (16.7 s) | The talk-nod envelope had an instant attack: a laugh made it zigzag 0.36 → 1.0 → 0.8 → 1.0 between frames, so the head snapped for one frame. The pose-jump gate (4 cm) is too coarse to see it; the flicker scan of the render caught it | `build.sh` smooths the envelope with a 5-frame window (one-frame rises fall from 0.89 to under 0.4, no zigzags). Copy it from `videos/vikingo-o-caballero/build.sh` for new reels |

## From "Una más" (2026-11-08, chess reel 2; `videos/RESEARCH_AJEDREZ_2_2026.md`, `videos/una-mas/AUDIT.md`)

| Seen | Cause | Rule |
|---|---|---|
| The first draft's hook meant nothing to a non-player; its CTA asked about a set it never showed; an unplugged printer that kept printing read as a glitch, and its "puff" as smoke | Jokes written from inside the product | Name the product in words in frame 1; make numbers visible (a counter); magic reads as magic (a gesture and sparkles, no smoke near a printer); the CTA asks only about what was shown, and rewards the comment (price and date) |
| — | The labour illusion (Buell & Norton 2011) and the handmade effect (Fuchs et al. 2015) are the strongest evidence we have | Show the work honestly (piece by piece, layers rising), with time passing (the light: day, night, dawn) and no failed prints or stalling; frame it as care ("lo hago yo, pieza por pieza, a pedido") |
| Board shots showed an empty middle while the pieces landed at the ends | The board was framed from the front, centred | Frame the side that is filling (three-quarter views from the left, then the right); go wide only for the full board |
| El Mago's "Una más" close-ups showed the side of his head | He was turned towards the printer behind him | A character delivering a line looks at something in front of the camera; the action he watches can be off screen |
| 42 frames with Papá Noel's chin in his beard while dozing | A deep head bend (0.42 rad) | Take droops mostly from the upper spine (0.14) and only a little from the head (0.26) |
| Voice trims cut words | The `_raw` clips are already cut to speech, so trims are measured in the raw clip (`silencedetect` on `<id>_raw.wav`), not in the take | Measure in the raw clip; a `squeeze` uses absolute times in the raw clip |
| **A background render ran in the repository root** (it rendered the website and left a `.hyperframes/` cache there) | The `cd` at the start of a `run_in_background` command did not take effect | Start background renders as `bash -c 'cd DIR \|\| exit 9; echo "cwd: $(pwd)" > ../render.log; npx hyperframes render ... >> ../render.log 2>&1'`, and check the first log line |
| The transcription model returned 429 in bursts | Per-minute limits on the free tier (the daily quota had reset) | Retry with 20 s waits; fall back to `CHECK_MODEL=gemini-3.5-flash-lite` |
| The printer whir is a buzzy square wave | — | The printer whir plays only under the printer close-ups, never under the whole reel |

## From "Elegí tu bando" (chess reel 3; scheduled for 2026-11-09, run on 2026-11-12)

| Seen | Cause | Rule |
|---|---|---|
| The scheduled run reached the session 3.5 days late | The session or container was idle or reclaimed when the trigger fired | Scheduled work can arrive late: check the date when it runs, say so in the summary, and still do the whole job |
| A question line ended up inside the previous clip (m3 had "Bueno… vikingo sos." plus "¿Qué colores le pondrías vos?") | The pauses inside a two-sentence CTA are as long as the pauses between lines | Check every clip's length against its words (about 2.5-3 words per second). Re-cut from the take at the measured pauses, and record the cuts in `_cuts_from_take` |
| — | A customisation feature needs to be *seen* | Show the choice as the two decisions it is (both sides repainted, labelled) and a "4 colores" piece built part by part. Recolour toon materials by blending each mesh's own colour to the new one, matching the old colour to the nearest of the side's three (exact hex compare breaks under colour management) |
| An elbow flip at the start of a pointing gesture | A 0.35 s reach | Reaches that start from the idle pose take at least 0.5 s |

## From "Las preguntas de Papá Noel" (chess reel 4, scheduled for 2026-11-12 20:00, arrived on time)

| Seen | Cause | Rule |
|---|---|---|
| A FAQ reel had no comic engine | Four answers in a row are a list, not a story | Give the questions an engine: the character's own prop (Papá Noel's list), a visible counter (1/4 … 4/4, an open loop) and a payoff that breaks it (5/87). The punchline can also be the bridge to the CTA ("Las demás… en comentarios") |
| `_cuts_from_take` looked like a script option | It is only a record: `tts_lineas.py` does not read it | Re-cut by hand with the split's own trim filter (`silenceremove` both ends), store the cut points in `voces.json`, then `--post-only` for the squeezes |
| The list's handwriting faced away from the camera | A strip built from code: the side vector and the triangle winding decide the front face | Check the written side on a frame; flip the width vector (not the texture) so the text reads left to right from the camera |
| A head turn read last frame's prop position | The list's place is set after the arms are solved, so `poseAt` saw the previous frame's value (breaks determinism) | Poses aim at fixed points (`LISTREF`), never at props placed later in the frame |
| The falling pawn showed mostly table legs and the list | Cameras placed for the start of a move, not its whole path | Frame the whole path (board edge to floor), and route the motion across the frame (the pawn rolls along x past a front camera), away from other props |
| A lying piece would sink into the floor when tumbling | Rotating about the base origin | Rotate a piece about its centre: origin = centre − q·(0, h/2, 0); a lying piece rolls about its long axis at its radius |
| One frame of beard in body while he looked down at the list | A 0.2 rad head bend | As for dozing: take part of a downward look from the upper spine |
| A ruler "at true scale" needs a true model | The kit's king was ~9.6 cm | Measure the toon meshes (`Box3` without outlines) and scale the piece to the stated size (0.095 m), then draw the ruler in real centimetres |

## From "Culpa de las piezas" (chess reel 5, scheduled for 2026-11-13 2:00, arrived on time)

| Seen | Cause | Rule |
|---|---|---|
| The draft caption said "para que llegue antes de Navidad, pedilo antes del [fecha]" | A cut-off written as a delivery promise, and "antes del 23" means the 22nd | Say the owner's date exactly as the last day included ("hasta el 23 de diciembre"), call it the last day to ORDER, and keep the honest "un juego lleva muchas horas: cuanto antes, mejor" next to it |
| The TTS added a sulking "Mmm…" and the split cut the line in the wrong place | Acting adds words and pauses | Check each clip's words against its length; keep what works and make the subtitle match what was said. `tts_lineas.py` now takes a list of squeezes for one line |
| A piece's fall was hidden by its neighbours from three camera positions | The falling piece sits among its own pieces and the attacker | Pick the piece's fall direction first (onto an empty square), then the camera on the side away from the attacker, raised above the pawns, close (fov 38) |
| A crowd gag (pieces turning round) barely read | 180° turns of small pieces look alike from far away | Shoot it as the character's POV from close above, and add a second, readable beat: after turning, each piece tilts back to look up at him |
| A "character at work" wide shot showed only his hat | High camera, the character between the lens and the work | When the work is the point, cut to a second angle of the work itself (two printer angles), not to the worker's back |
| The mix check heard "Vos sí" as "o sí" (the clean clip read fine) | A pop effect placed exactly on the punchline's first word masked the soft Rioplatense "v" | Never put an effect on a word: place it after the line. Duck the music deeper (0.18) under a short punchline and under the CTA, and re-check the mix with `remezclar.py` (no re-render) |

## Music (2026-11-14: "la música es muy alta y molesta")

| Seen | Cause | Rule |
|---|---|---|
| The owner found the music loud and annoying | Measured on reel 5: the chiptune bed sat only 8 dB under the voices while they spoke and level with them in the gaps; square-wave harmonics sit in the 1-4 kHz speech band | Use `"style": "ambient"` in `chiptune.py` (slow detuned pads, a root drone, a sparse bell, low-passed at 900 Hz) at page volume 0.22. Check with `videos/biblioteca/nivel_musica.py HF3D_DIR`: the bed 20-25 dB under the voices, 12-16 dB under them in the gaps (K-weighted). A sound-only change goes through `remezclar.py`, the picture byte-identical |

## From "Los gatos tiran todo" (November second wave W1, 2026-11-14)

| Seen | Cause | Rule |
|---|---|---|
| — | A new setting without building a new room | Redress the workshop: hide the workshop props (bench, shelves, printer) by region, re-texture the walls (toon materials only: the window glass and the night sky are basic materials and must be left alone), swap the window's picture, add furniture with QA boxes |
| — | A new chess set with animal pieces | `biblioteca/3d/web/mascotas3d.js`: seated animals on round bases, built from the product photo; animated parts in `userData` (head, ears, tail, a pivoting front paw); each piece scaled from its measured toon height |
| A falling pawn grazed the table's edge for 8 frames | It dropped as soon as its centre passed the edge, while half its base was still over the table | A piece drops only when its whole base is past the edge (centre + base radius + a margin) |
| The dogs read as brown blobs | They were shot from behind (they face the other army) | Shoot each army from the opposite side, so the camera sees their faces |
