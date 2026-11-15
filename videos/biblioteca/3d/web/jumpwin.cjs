// The QA gate's pose-jump detector on a time window only (fast iteration before the full gate). Serve hf3d on 8768:
//   node jumpwin.cjs T0 T1     -> jumps in [T0, T1] with the gate's thresholds, plus frames with contact violations
const { chromium } = require('playwright'); const [a, b] = process.argv.slice(2).map(Number);
(async () => { const br = await chromium.launch(); const p = await br.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('http://localhost:8768/index.html'); await p.waitForFunction(() => window.__qa, null, { timeout: 240000 });
  const res = await p.evaluate(([a, b]) => { const r = []; for (let f = Math.round(a * 60) - 3; f <= Math.round(b * 60) + 3; f++) { const q = window.__qa(f / 60); r.push({ t: f / 60, J: q.J, n: q.out.length }); } return r; }, [a, b]);
  const ok = await p.evaluate(() => window.__JUMP_OK || []);
  const step = (i, k) => { const x = res[i - 1].J[k], c = res[i].J[k]; return Math.hypot(x[0] - c[0], x[1] - c[1], x[2] - c[2]); };
  const jumps = []; for (let i = 3; i < res.length - 3; i++) for (const k in res[i].J) { if (ok.some(([u, v]) => res[i].t >= u && res[i].t <= v)) continue;
    const d = step(i, k), nb = [step(i - 2, k), step(i - 1, k), step(i + 1, k), step(i + 2, k)].sort((x, y) => x - y), med = (nb[1] + nb[2]) / 2;
    if ((d > 0.04 && d > 2.5 * med + 0.01) || d > 0.15) jumps.push([+res[i].t.toFixed(3), k, +d.toFixed(3), +med.toFixed(3)]); }
  console.log('jumps', JSON.stringify(jumps), 'violation frames', res.filter((x) => x.n).length); await br.close(); })();
