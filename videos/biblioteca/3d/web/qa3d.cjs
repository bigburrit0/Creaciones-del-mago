// QA gate for 3D toon reels (RESEARCH_3D_CONTACT.md). Serve the hf project folder, then:
//   node qa3d.cjs PORT report.json      (the page must expose window.__qa(t) and window.__draw3d(t))
// Every frame: exact contact checks against the posed skinned meshes (mate, hands, sack, gifts, bodies), NaN bones,
// pose jumps (a joint step much larger than its neighbours'), and determinism (same t drawn in any order = same pixels).
// Exit code 1 on any failure: do not render until it passes.
const { chromium } = require('playwright'); const fs = require('fs');
const PORT = process.argv[2] || 8768, OUT = process.argv[3] || 'qa.json', FPS = 60;
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  const errs = []; p.on('pageerror', (e) => errs.push(e.message)); p.on('console', (m) => { if (m.type() === 'error' || /meeting|speeds/.test(m.text())) console.log('console:', m.text()); });
  await p.goto(`http://localhost:${PORT}/index.html`); await p.waitForFunction(() => window.__qa, null, { timeout: 240000 });
  const N = await p.evaluate(() => Math.round(window.__timelines.main.duration() * 60)); const res = [];
  for (let f0 = 0; f0 <= N; f0 += 60) res.push(...await p.evaluate(([a, b]) => { const r = []; for (let f = a; f < b; f++) r.push(window.__qa(f / 60)); return r; }, [f0, Math.min(N, f0 + 60)]));
  // determinism: the same frame drawn twice, and after another frame, must give identical pixels
  const det = await p.evaluate(() => { const c = document.getElementById('c'), g = c.getContext('webgl2'); const hash = () => { const px = new Uint8Array(4 * 256 * 4); g.readPixels(412, 900, 256, 4, g.RGBA, g.UNSIGNED_BYTE, px); let h = 0; for (const v of px) h = (h * 31 + v) >>> 0; return h; };
    const out = []; for (const t of [4.8, 6.0, 7.5, 9.9, 16.5]) { window.__draw3d(t); const a = hash(); window.__draw3d(t + 0.5); window.__draw3d(t); const b2 = hash(); window.__qa(t); window.__draw3d(t - 1); window.__draw3d(t); const c2 = hash(); out.push([t, a === b2 && b2 === c2]); } return out; });
  // pose jumps: joint world speed between consecutive frames (exclude Santa leaving through the door)
  // a jump = a discontinuity: this frame's step is large AND much larger than its neighbours' steps (not just fast motion)
  const step = (i, k) => { const a = res[i - 1].J[k], c = res[i].J[k]; return Math.hypot(a[0] - c[0], a[1] - c[1], a[2] - c[2]); };
  const jumps = []; for (let i = 3; i < res.length - 3; i++) for (const k in res[i].J) { if (k[0] === 's' && res[i].t > 15.85) continue;      // Santa has left through the door (he is moved outside)
    const d = step(i, k), nb = [step(i - 2, k), step(i - 1, k), step(i + 1, k), step(i + 2, k)].sort((x, y) => x - y), med = (nb[1] + nb[2]) / 2;
    if ((d > 0.04 && d > 2.5 * med + 0.01) || d > 0.15) jumps.push([+res[i].t.toFixed(3), k, +d.toFixed(3), +med.toFixed(3)]); }
  const viol = res.filter((r) => r.out.length).map((r) => [r.t, r.out]);
  const spans = {}; for (const [t, o] of viol) for (const v of o) { const k = v.slice(0, 4).join(' '); (spans[k] = spans[k] || []).push(+t.toFixed(2)); }
  for (const k in spans) { const a = spans[k]; spans[k] = [a.length, a[0], a[a.length - 1]]; }
  const kinds = {}; for (const [, o] of viol) for (const v of o) { const k = v.slice(0, 3).join(' '); kinds[k] = (kinds[k] || 0) + 1; }
  const report = { spans, frames: res.length, violationFrames: viol.length, kinds, firstViolations: viol.slice(0, 25), jumps: jumps.slice(0, 40), determinism: det, pageErrors: errs };
  fs.writeFileSync(OUT, JSON.stringify(report, null, 1)); console.log(JSON.stringify({ frames: report.frames, violationFrames: report.violationFrames, kinds, jumps: jumps.length, determinism: det, pageErrors: errs.length }, null, 0));
  await b.close(); process.exit(viol.length || jumps.length || det.some((d) => !d[1]) || errs.length ? 1 : 0); })();
