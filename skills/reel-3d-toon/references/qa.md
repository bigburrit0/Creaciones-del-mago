# QA gate and checks

## The gate (before every render)

`node videos/biblioteca/3d/web/qa3d.cjs PORT report.json` with the reel's `hf3d/` served over http. It loads the page,
reads the length from `window.__timelines.main`, calls `window.__qa(t)` for every frame and exits 1 on any failure.
The page's `qa(t)` returns `{ t, out: [violations], J: {joint positions} }`.

What `qa(t)` must check (copy the reference implementation in `papa-noel-en-ojotas/hf3d/index.html`):

| Check | Threshold |
|---|---|
| NaN in any bone | none |
| Mate (or any held prop) vs every body; the holder's arms excluded only while held; also while in flight | 5 cm from the gourd centre |
| Hands vs the other character; hands vs own face, beard, hat | 0.75 × hand radius |
| Sack vs bodies (arms excluded while held) | 0.85 × its real radius |
| Gifts in flight vs bodies | 3.5 cm |
| Bodies vs bodies (colliders) | no overlap |
| **Walls**: every collider (arms included) and the sack vs the back wall, except through the opening (3.5 cm margin from the jambs, under the lintel) | none |
| **Door panel** (a box on its hinge) vs every collider and the sack | none |
| **Beards**: ~450 beard points that rest on the body (bind pose, < 3 cm) are tracked against their body point along its normal | body may not come within 8 mm of the beard's OUTER surface; 1.2 cm where the beard is thin |
| Pose jumps: a joint step much larger than its neighbours' (`d > 0.04 && d > 2.5·median + 0.01`, or `d > 0.15`) | none (characters skipped after they leave, `window.__T.exit`) |
| Determinism: the same t drawn twice, and after other frames, gives identical pixels | true at 5 sample times |

Gate history in the Christmas reel: 1140 → 299 → 82 → 5 → 0 bad frames.

## Faster loops

- Window check: load the page in Playwright and call `__qa(t)` over just the seconds you changed.
- Frames: `node videos/biblioteca/3d/web/frames3d.cjs PORT OUT t1 t2 ...` → `OUT/sheet.png`.
- Expose internals for probing with `window.__dbg = { mago, santa, SPR, ... }` (left in the reference scene).

## After the render

1. `python3 videos/biblioteca/3d/web/flicker_scan.py reel.mp4 --cuts 3.2,8.0,12.5,17.95` → 0 flicker frames.
2. `ffmpeg -i reel.mp4 -af ebur128=peak=true -f null -` → about -13 to -14 LUFS integrated, peaks under -1 dB.
3. `python3 videos/biblioteca/check_voces.py mix reel.mp4` → every line clear.
4. A contact sheet of real frames from the mp4 at the key moments.
