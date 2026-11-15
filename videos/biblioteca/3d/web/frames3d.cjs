// Preview frames of a 3D toon reel without rendering the whole video (serve the hf folder over http first).
//   node frames3d.cjs PORT OUT_DIR t1 t2 ...      -> OUT_DIR/f<t>.png (1080x1920, overlays included) + OUT_DIR/sheet.png
// Use it after every change to look at the moments that matter (doors, contacts, subtitles, the end card) BEFORE the
// 25-minute QA gate and the 15-minute render.
const { chromium } = require('playwright'); const { execFileSync } = require('child_process');
const [PORT, OUT, ...T] = process.argv.slice(2); const ts = T.map(Number);
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', (e) => console.log('page error:', e.message));
  await p.goto(`http://localhost:${PORT}/index.html`); await p.waitForFunction(() => window.__qa || window.__draw3d, null, { timeout: 240000 });
  await p.evaluate(() => document.fonts.ready);
  for (const t of ts) { await p.evaluate((t) => window.__draw3d(t), t); await p.screenshot({ path: `${OUT}/f${t.toFixed(2)}.png` }); }
  await b.close();
  execFileSync('python3', ['-c', `
from PIL import Image; import sys
fs = sys.argv[1:]; ims = [Image.open(f).resize((270, 480)) for f in fs]; cols = min(5, len(ims)); rows = (len(ims) + cols - 1) // cols
W = Image.new('RGB', (270 * cols, 480 * rows)); [W.paste(im, ((i % cols) * 270, (i // cols) * 480)) for i, im in enumerate(ims)]; W.save('${OUT}/sheet.png')`,
    ...ts.map((t) => `${OUT}/f${t.toFixed(2)}.png`)]);
  console.log(`${ts.length} frames -> ${OUT}/sheet.png`); })();
