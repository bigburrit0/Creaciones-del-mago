# "Un regalo para cada amigo": everything on screen, by category

Reach reel N1 from `../PLAN_NOVIEMBRE.md` (publish Fri 13 Nov). Its job is to be **sent and tagged**. Same rule as the last reel: every item on screen is listed here, with its detail, its motion and the check that proves it is done.

## Result (2026-11-07)

✅ Built and checked. Render: `un-regalo-para-cada-amigo.mp4` (25.3 s, 1080×1920, 60 fps).
- **QA gate:** 0 bad frames out of 1518, 0 pose jumps, deterministic. The first run had 4 frames of Papá Noel's forearm touching the closed door during the stretch; that arm now stretches forward.
- **Flicker scan of the render:** 0 frames.
- **Loudness:** -14.0 LUFS, peak -1.8 dBFS.
- **Voices:** 8 of 8 lines intelligible in the final mix (transcription). On the full mix the transcriber once heard "banana" as "boludo", the commoner phrase. The clip alone and the mixed segment both transcribe as "banana", and the subtitle and the banana in sunglasses show it on screen.
- **Contact sheet** of the real frames reviewed.
- **Audio fix (after delivery):** the person heard a buzz in the background. It was the cicada ambience. The synth ignored its level, and it is noise switched on and off at 37 Hz, measured in the mix at 34 dB above the background. The music also carried a DC offset. Fixes: no ambience; DC removed from every stem; the music level restored (volume 0.6, matching the approved balance). The mix was rebuilt and swapped in with `biblioteca/remezclar.py`, with the video stream byte-identical. Result: buzz 4.7 dB (none), -14.2 LUFS, peak -2.7 dBFS, every spoken line clear (transcription with `gemini-3.5-flash-lite`).

## 1. Selling structure (voice first; measured lines: m1 2.52, m2 1.56, m3 1.55, m4 1.80, m5 2.48, m6 1.25, m7 1.65, s1 1.50 (yawn), s2 1.10)

| Time | Stage | Content | Line |
|---|---|---|---|
| 0.0–2.7 | hook | El Mago beside the display with the five pieces in a row; he presents them. Hook text from the first frame | M: "Un regalo para cada amigo que tenés." |
| 2.75–5.9 | 1/5 | the coffee cup clicker; its lid clicks; Papá Noel behind it, a huge yawn | M: "Para el que no arranca sin café." S: "Aaaahhh…" |
| 5.95–8.6 | 2/5 | a dead cactus on the bench droops (sad trombone); whip to the printed succulent, perfect; handwritten note "(esta no se muere)" | M: "Para el que mata hasta los cactus." |
| 8.55–10.95 | 3/5 | the hamster pops up and ducks back into its egg | M: "Para el que no sale de su casa." |
| 11.0–14.05 | 4/5 | the skull keychain: on "¡me muero!" its eyes become x's and a little ghost floats out of it; then the brain clicks | M: "Para el que dice: ¡me muero!, por todo." |
| 14.0–15.35 | 5/5 | the banana clicker; its core pops up wearing tiny sunglasses | M: "Y para el que se hace el banana…" |
| 15.35–16.85 | punchline | Papá Noel, in his sunglasses, caught; the glasses slide down | S: "¿Quién? ¿Yo?" |
| 16.85–18.35 | process | top view of the printer: the five print layer by layer, 0.3 s each; "Impresos en 3D en mi taller" | — |
| 18.35–20.85 | proof | five polaroids of the real pieces (the site's photos); "Así son de verdad" | — |
| 20.85–22.7 | CTA | back to the opening shot (loop); El Mago points at the viewer | M: "¿Cuál es tu amigo? Etiquetalo." |
| 22.7–25.2 | card | "¿Cuál es tu amigo? · Clickers y llaveros impresos en 3D · ¡Etiquetalo! · Te paso precio y fecha por mensaje · Creaciones del Mago · Montevideo" | — |

## 2. The five products (hero props; must match the real photos in `assets/p`)

| Item | Detail (from the photo) | Motion | Check |
|---|---|---|---|
| Café clicker | white cup tapering to the base, a tan ribbed sleeve, a big black lid with a rim and a sip hole | the lid dips 4 mm on the click | the hero frame next to the photo |
| Suculenta | olive pot with horizontal print lines and a rim, brown soil, a teal rosette of pointed leaves in three rings | the rosette dips on the click; a sparkle | the hero frame next to the photo |
| Hámster en su huevo | a grey half egg with a zigzag rim, a navy cushion, a beige hamster with brown patches, round ears, black eyes, a pink nose and little paws | pops up 1 cm, then ducks into the egg | the hero frame next to the photo |
| Calavera keychain | a white skull (sockets, nose, teeth line), a red brain cap with folds, a metal split ring | the brain dips (click); the ring swings | the hero frame next to the photo |
| Banana clicker | yellow peel petals splayed out, a white rounded core | the core pops up, tiny sunglasses appear on it | the hero frame next to the photo |
| Display | the round side table, the five in a straight row facing the camera (no piece hides another in its close-up), a felt disc under each | — | each hero frame shows one whole piece |
| Dead cactus | a terracotta pot with a three-segment cactus, browned and drooping | droops further on "mata" | — |

## 3. Characters and acting

| Item | Detail | Check |
|---|---|---|
| El Mago | presents the display with an open hand (hook); points at the viewer (CTA); talk nods; blinks. He narrates the close-ups off screen: hidden while posed in place, because his 58 cm brim sat in every product shot | hand vs own face/beard 0; nothing through the table or bench |
| Papá Noel | a big yawn with a stretch (café); caught in his sunglasses for "¿Quién? ¿Yo?" (head to camera, glasses slide down, brows up, hand to chest) | hands vs hat, pompom and beard 0; table and walls 0 |

## 4. Camera and editing

- A cut or a new event every 1.2-2.5 s.
- Whip pans between products.
- Snap zooms on each gag.
- A low hero lens at product height for each piece (fov 30-40, the character behind it).
- A top view of the bed for the montage.
- The CTA shot repeats the hook framing, so the reel loops.
- Every camera looks toward the walls.

Check: a contact sheet of every shot; nothing blocked by the tree.

## 5. Text on screen (safe area: y 220-1470)

- Hook: "Un regalo para cada amigo".
- Kinetic captions for every line.
- Counter badge "1/5 … 5/5".
- Handwritten note "(esta no se muere)".
- Banner "Impresos en 3D en mi taller".
- "Así son de verdad" with Caveat captions on the polaroids.
- End card.
- No phone number; no emoji (the renderer has no emoji font).

## Changes made while building, and why

- **Paper tags removed.** In every close-up they sat in the caption zone (y 1150-1470). The counter badge and the captions already name each piece.
- **Pieces in a straight row, not an arc.** In the arc, the succulent stood in front of the café in its close-up.
- **The dead cactus moved to the bench.** On the table, any camera aimed at it looked through the café.
- **El Mago's faint replaced by the skull's ghost.** A hand to the forehead gets pushed down by the contact guard (the face and brim colliders), so it read as a fist at the mouth. The ghost is clearer, and it is the product's own joke.
- **El Mago hidden during the close-ups.** His brim is 0.58 m wide, so at 0.3-0.6 m from the café it entered the frame from every angle.

## 6. Sound

- Voices at -16 LUFS, the music ducked under each one.
- An upbeat track, 124 bpm.
- A whoosh on each whip.
- Clicks on every clicker press.
- A sad trombone for the cactus, a sparkle for the succulent, a pop for the sunglasses.
- A printer whir under the montage.
- A tap as each polaroid lands.
- A chime and the end chord on the card.

Check: final mix around -13/-14 LUFS; every line intelligible (transcription).
