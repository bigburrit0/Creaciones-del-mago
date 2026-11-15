# Brief: shared scene kit + "Invisible no era" (scheduled for 2026-11-07 01:20, Montevideo)

The user's words (2026-11-07): "Go ahead with the shared kit and Invisible no era. Run all the necessary checks to make
sure the work is nice and proper. Also let's try not to make a 'lazy looking' creation. Add detail. Create categories
for everything that will go on screen and make sure everything in that list is carefully crafted."

## What to do
1. **Step 0, shared scene kit**: `videos/biblioteca/3d/web/escena3d.js` from `papa-noel-en-ojotas/hf3d/index.html`
   (room and door, characters and colliders, IK queue and contact guard, props helpers, subtitles, talk nods, end card,
   `qa()` with every check, shots, lighting presets day/night/dawn, rigid accessories on bones). The Christmas reel
   must still pass its QA gate and look the same after being moved onto the kit (re-check, no re-render needed unless it changes).
2. **Reel 1, "Invisible no era"** (script in `videos/PLAN_PROXIMOS_REELS.md`), following `skills/reel-3d-toon/SKILL.md`
   and every lesson in `references/lecciones.md`. Voice first.

## Quality bar: nothing lazy-looking
- Before building, write `ON_SCREEN.md` in this folder: **a category list of EVERYTHING that will be on screen**
  (characters, faces and expressions, hands and props in hands, hero props, set and set dressing, lighting per time of
  day, effects and particles, camera and composition, text: subtitles, labels, card; motion details: weight,
  anticipation, follow-through, secondary motion; sound that sells what's on screen). For each item: what it must look
  like, the detail it needs (secondary forms, wear, bevels, colour variation, AO), how it moves, and the check that
  proves it is done.
- Craft every item on that list; tick each one off with evidence (a frame from the preview sheet, a QA line).
- Add detail where a viewer's eye goes: the papelitos (folded, handwritten names), the bowl, the night workshop
  (moonlight through the window, printer LED glow, desk lamp pool, dust in the light), the mini clicker figures (real
  little versions of each character, with a ring and a clicker base), the sneaking (crouch, exaggerated tiptoe, a
  freeze with eye darts), the exchange and the synced clicks.

## Checks (all must pass before delivering)
QA gate 0 bad frames, 0 jumps, deterministic; frame preview sheets of every risky moment and every item in
ON_SCREEN.md; flicker scan 0; loudness about -13/-14 LUFS; every voice line intelligible in the final mix; captions
inside the safe area; caption text (three Haiku writers, curated). Commit and push after each working step; deliver
the video with a short summary.
