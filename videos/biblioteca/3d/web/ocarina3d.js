// The 12-hole transverse ocarina ("sweet potato" shape) for the ocarina reels (../../PLAN_OCARINA.md), modelled from the
// owner's description of their photos: a dark, matte teardrop about hand length, eight finger holes plus two small sub-holes
// on top, two thumb holes underneath, an angled mouthpiece, a rectangular window (the labium), visible layer lines.
// Local frame: the length along x (the round end at -x, the tail at +x), the top +y, the player's side +z.
// Each hole has a gold "magic cap" (El Mago's sparkle closing it): caps show while the ocarina plays by magic, and a cap
// pops off when the note opens that hole. Notes come from ocarina_synth.py (open-hole lists per note).
import * as THREE from "three";
import { toon, outline, shade } from "./toon3d.js";

export function ocarina(scene, o = {}) {
  const WO = o.wo ?? 0.0024, L = o.length ?? 0.18, k = L / 0.18;
  const g = new THREE.Group(); scene.add(g);
  const inner = new THREE.Group(); inner.scale.setScalar(k); g.add(inner);
  // ---- body: a lathe about its long axis, flattened top to bottom; the layer lines run along the length (printed lying flat)
  const R = (s) => 0.046 * Math.pow(Math.max(0, 4 * s * (1 - s)), 0.52) * (1 - 0.32 * s) + 0.0005;
  const prof = []; for (let i = 0; i <= 40; i++) { const s = i / 40; prof.push(new THREE.Vector2(R(s), -0.09 + 0.18 * s)); }
  const geo = new THREE.LatheGeometry(prof, 48); geo.rotateZ(-Math.PI / 2); geo.scale(1, 0.62, 1); geo.computeVertexNormals();
  const layers = new THREE.CanvasTexture((() => { const c = document.createElement("canvas"); c.width = 8; c.height = 128; const x = c.getContext("2d");
    for (let y = 0; y < 128; y++) { x.fillStyle = y % 4 < 2 ? "#34333C" : "#28272F"; x.fillRect(0, y, 8, 1); } return c; })());
  layers.colorSpace = THREE.SRGBColorSpace; layers.wrapS = layers.wrapT = THREE.RepeatWrapping; layers.repeat.set(1, 1.6);
  layers.magFilter = THREE.NearestFilter;
  // the lathe's u runs round the long axis: rotate the stripes so they follow u (constant height = a print layer)
  const uv = geo.attributes.uv; for (let i = 0; i < uv.count; i++) { const u = uv.getX(i), v = uv.getY(i); uv.setXY(i, v, u); }
  const bodyMat = toon("#ffffff", { map: layers, spec: 0 });
  const body = new THREE.Mesh(geo, bodyMat); shade(body); inner.add(body); outline(body, WO / k);
  const W = (x) => R((x + 0.09) / 0.18), H = (x) => 0.62 * W(x);
  const top = (x, z) => H(x) * Math.sqrt(Math.max(0, 1 - (z / Math.max(1e-4, W(x))) ** 2));
  // ---- the mouthpiece: out of the round end toward the player, angled down; the windway's slot at its tip
  const mp = new THREE.Group(); mp.position.set(-0.06, -0.002, 0.02); mp.rotation.set(0.22, 0.9, 0); inner.add(mp);
  { const pts = [[0.0095, 0], [0.0095, 0.012], [0.0088, 0.03], [0.0075, 0.044], [0.0068, 0.046], [0.001, 0.046]].map(([r, y]) => new THREE.Vector2(r, y));
    const mg = new THREE.LatheGeometry(pts, 20); mg.rotateX(Math.PI / 2); mg.scale(1.35, 0.62, 1);           // a flattened, slightly tapered beak
    const m = new THREE.Mesh(mg, bodyMat); shade(m); mp.add(m); outline(m, WO / k);
    const slot = new THREE.Mesh(new THREE.PlaneGeometry(0.011, 0.0022), new THREE.MeshBasicMaterial({ color: "#050408" })); slot.position.set(0, 0.0, 0.0465); mp.add(slot); }
  // ---- the labium window: a small rectangle on top, where the mouthpiece meets the body
  { const x = -0.047, z = 0.006, y = top(x, z) + 0.0006;
    const win = new THREE.Mesh(new THREE.PlaneGeometry(0.013, 0.008), new THREE.MeshBasicMaterial({ color: "#050408" })); win.rotation.set(-Math.PI / 2, 0, 0.95); win.position.set(x, y, z); inner.add(win);
    const edge = new THREE.Mesh(new THREE.PlaneGeometry(0.013, 0.0016), new THREE.MeshBasicMaterial({ color: "#6E6C78" })); edge.rotation.copy(win.rotation); edge.position.set(x + 0.0035, y + 0.0002, z - 0.003); inner.add(edge); }
  // ---- holes: left hand near the mouthpiece, right hand toward the tail, the sub-holes beside the ring fingers, thumbs below
  const SPEC = { L1: [-0.028, -0.010, 0.0047], L2: [-0.012, -0.012, 0.0050], L3: [0.004, -0.011, 0.0050], L4: [0.019, -0.006, 0.0042],
    R1: [0.033, 0.000, 0.0046], R2: [0.046, 0.002, 0.0044], R3: [0.058, 0.004, 0.0040], R4: [0.069, 0.002, 0.0034],
    SL: [0.007, 0.010, 0.0026], SR: [0.059, 0.016, 0.0024], TL: [-0.006, 0.004, 0.0046], TR: [0.040, 0.004, 0.0044] };
  const holeMat = new THREE.MeshBasicMaterial({ color: "#040306" }), rimMat = new THREE.MeshBasicMaterial({ color: "#5E5C68" });
  const capMat = new THREE.MeshBasicMaterial({ color: "#F2C14E", fog: false }), capHi = new THREE.MeshBasicMaterial({ color: "#FFF3B0", fog: false });
  const holes = {};
  for (const [id, [x, z, r]] of Object.entries(SPEC)) {
    const under = id[0] === "T", y0 = top(x, z), y = (under ? -y0 : y0);
    // the surface normal of the flattened ellipsoid at (x, y, z) (approximate: from the cross-section ellipse)
    const n = new THREE.Vector3(0, y / (H(x) ** 2 || 1), z / (W(x) ** 2 || 1)).normalize();
    const hg = new THREE.Group(); hg.position.set(x, y, z); hg.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), n); inner.add(hg);
    const hole = new THREE.Mesh(new THREE.CircleGeometry(r, 18), holeMat); hole.position.z = 0.0007; hg.add(hole);
    const rim = new THREE.Mesh(new THREE.RingGeometry(r, r * 1.28, 20), rimMat); rim.position.z = 0.0006; hg.add(rim);
    const cap = new THREE.Group(); cap.position.z = 0.0016; hg.add(cap);
    cap.add(new THREE.Mesh(new THREE.CircleGeometry(r * 1.32, 18), capMat));
    const hi = new THREE.Mesh(new THREE.CircleGeometry(r * 0.55, 12), capHi); hi.position.set(-r * 0.3, r * 0.3, 0.0003); cap.add(hi);
    cap.visible = false;
    holes[id] = { id, g: hg, cap, r: r * k, under };
  }
  const ALL = Object.keys(SPEC);
  const holeWorld = (id) => holes[id].g.getWorldPosition(new THREE.Vector3());
  // play state: notes = the synth's notes file, t0 = when the phrase starts. Returns the open holes and each hole's
  // time since it last opened (for its sparkle). Outside the phrase: every cap shows if magic > 0, none otherwise.
  function play(t, notes, t0, magic = 1) {
    const dt = t - t0; let cur = null;
    if (notes && dt >= 0 && dt < notes.duration) for (const n of notes.notes) if (dt >= n.t) cur = n;
    const open = new Set(cur ? cur.open : []), since = {};
    if (cur) { const i = notes.notes.indexOf(cur), prev = i > 0 ? new Set(notes.notes[i - 1].open) : new Set();
      for (const id of cur.open) if (!prev.has(id)) since[id] = dt - cur.t; }
    for (const id of ALL) { const c = holes[id].cap, show = magic > 0.01 && !open.has(id);
      c.visible = show; if (show) c.scale.setScalar(Math.max(0.001, Math.min(1, magic * 1.2))); }
    return { open, since, note: cur, playing: !!cur };
  }
  function capsOff() { for (const id of ALL) holes[id].cap.visible = false; }
  return { g, inner, body, holes, ALL, holeWorld, play, capsOff, length: L, H: (x) => H(x / k) * k, W: (x) => W(x / k) * k };
}
