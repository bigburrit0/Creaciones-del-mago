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
