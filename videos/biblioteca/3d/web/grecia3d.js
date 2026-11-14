/* grecia3d.js: the shop's "Antigua Grecia" chess set as toon props, modelled from its photo (assets/p/grecia.webp).
   The board: red and gold squares inside a ring of white, rocky ruin walls (two rows of hewn blocks with a narrow
   passage between them, taller blocks at the corners), and a Greek temple (columns and a pediment) set into one long
   side. 52 × 50 cm including the walls (the site's own words). The gold army: the Minotaur king standing on a column
   drum, columns with a brazier for rooks, winged horses for knights, a laurel-crowned sage for bishops, a goddess with a
   torch for the queen, crested hoplites with round shields and spears for pawns. The red army: the same, with Hercules
   for the king (a lion pelt over his head and a club).
   Sizes in metres; the scene scales each king to the tournament size it states. Every piece is a Group whose origin is
   the centre of its base and whose FRONT is local +z; animate g.position / g.rotation freely.
   Animated parts in g.userData: head (the Minotaur's head, a Group pivoting at the neck: lower the horns with
   rotation.x > 0), club (Hercules' right arm with the club, a Group pivoting at the shoulder: raise it with
   rotation.x < 0).
   Usage: const GK = greekKit(scene, { wo }); const b = GK.board(); const k = GK.piece("king", GK.SIDES.gold); */
import * as THREE from "three";
import { toon, outline, shade } from "./toon3d.js";

export function greekKit(scene, o = {}) {
  const WO = (o.wo ?? 0.0024) * 0.4;
  const SIDES = { gold: ["#D9A92E", "#F4D575", "#5A3E0C"], red: ["#B8432F", "#DE7254", "#3E120C"] };   // [main, accent, dark (eyes, nostrils)]
  const STONE = "#F1EDE4", STONE_B = "#D9D3C6";
  const V = (x, y, z) => new THREE.Vector3(x, y, z);
  const facets = (geo) => { const g = geo.index ? geo.toNonIndexed() : geo; g.computeVertexNormals(); return g; };   // flat facets (MeshToonMaterial has no flatShading)
  const rnd = (i) => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
  function P(geo, c, parent, x = 0, y = 0, z = 0, opt = {}) {
    const m = new THREE.Mesh(opt.flat ? facets(geo) : geo, toon(c, { spec: opt.spec ?? 0.5 })); m.position.set(x, y, z);
    if (opt.rot) m.rotation.set(...opt.rot); if (opt.scale) m.scale.set(...opt.scale); shade(m); parent.add(m);
    if (opt.line !== false) outline(m, opt.w ?? WO); return m;
  }
  const S = (r, w = 14, h = 10) => new THREE.SphereGeometry(r, w, h);
  const lathe = (pts, n = 24) => new THREE.LatheGeometry(pts.map(([r, y]) => new THREE.Vector2(r, y)), n);
  function limb(g, a, b, r0, r1, c, opt = {}) {          // a tapered cylinder from a to b (r0 at a, r1 at b)
    const A = V(...a), B = V(...b), d = B.clone().sub(A), L = d.length();
    const m = P(new THREE.CylinderGeometry(r1, r0, L, 10), c, g, 0, 0, 0, opt); m.position.copy(A).addScaledVector(d, 0.5);
    m.quaternion.setFromUnitVectors(V(0, 1, 0), d.normalize()); return m;
  }
  function base(g, r, col) { P(lathe([[0.001, 0], [r, 0], [r, 0.0035], [r * 0.92, 0.006], [0.001, 0.006]], 28), col[0], g); return 0.006; }

  // ---------------- the pieces ----------------
  function hoplite(g, y0, col) {                 // pawn: crested helmet, round shield on the left arm, a spear on the right
    const C = col[0], A = col[1];
    for (const s of [-1, 1]) limb(g, [s * 0.0032, y0, 0.0005], [s * 0.003, y0 + 0.012, 0], 0.0026, 0.003, C);
    P(lathe([[0.001, 0], [0.0086, 0], [0.008, 0.006], [0.0071, 0.012], [0.0079, 0.017], [0.0068, 0.021], [0.003, 0.023], [0.001, 0.023]]), C, g, 0, y0 + 0.009, 0);
    P(S(0.0052), C, g, 0, y0 + 0.0355, 0.0004);
    P(new THREE.SphereGeometry(0.0059, 14, 10, 0, Math.PI * 2, 0, Math.PI * 0.62), C, g, 0, y0 + 0.0362, 0, { scale: [1, 1.12, 1.1] });     // the helmet
    P(new THREE.TorusGeometry(0.0064, 0.0017, 6, 14, Math.PI), A, g, 0, y0 + 0.0385, -0.0004, { rot: [0, Math.PI / 2, 0] });              // the crest, front to back
    limb(g, [0.0072, y0 + 0.029, 0], [0.0098, y0 + 0.02, 0.0042], 0.0024, 0.0021, C);
    limb(g, [0.0098, y0 + 0.003, 0.0046], [0.0098, y0 + 0.054, 0.0046], 0.0008, 0.0008, C, { line: false });                              // the spear
    P(new THREE.ConeGeometry(0.0018, 0.006, 8), A, g, 0.0098, y0 + 0.057, 0.0046);
    const sh = new THREE.Group(); sh.position.set(-0.0052, y0 + 0.0215, 0.0078); sh.rotation.y = -0.28; g.add(sh);
    P(new THREE.CylinderGeometry(0.0088, 0.0088, 0.0018, 24), C, sh, 0, 0, 0, { rot: [Math.PI / 2, 0, 0] });
    P(new THREE.TorusGeometry(0.0086, 0.0009, 6, 24), A, sh, 0, 0, 0.0009, { line: false });
    P(S(0.0026, 10, 8), A, sh, 0, 0, 0.0012, { scale: [1, 1, 0.6], line: false });
  }
  function column(g, y0, col) {                  // rook: a fluted column with a brazier
    const C = col[0], A = col[1];
    P(new THREE.BoxGeometry(0.023, 0.005, 0.023), C, g, 0, y0 + 0.0025, 0);
    P(new THREE.TorusGeometry(0.0093, 0.0018, 8, 20), C, g, 0, y0 + 0.0062, 0, { rot: [Math.PI / 2, 0, 0] });
    P(new THREE.CylinderGeometry(0.0077, 0.0088, 0.027, 14), C, g, 0, y0 + 0.0195, 0, { flat: true });                                     // the shaft (facets read as flutes)
    P(new THREE.CylinderGeometry(0.0108, 0.0078, 0.0045, 16), C, g, 0, y0 + 0.0355, 0);
    P(new THREE.BoxGeometry(0.023, 0.0038, 0.023), C, g, 0, y0 + 0.0396, 0);
    for (const s of [-1, 1]) P(new THREE.TorusGeometry(0.0022, 0.0011, 6, 12), A, g, s * 0.0105, y0 + 0.0365, 0.0, { rot: [0, Math.PI / 2, 0], line: false });   // the volutes
    P(lathe([[0.001, 0], [0.004, 0], [0.0088, 0.0058], [0.0095, 0.0085], [0.0084, 0.0088], [0.001, 0.0062]]), C, g, 0, y0 + 0.0414, 0);    // the brazier
    P(new THREE.ConeGeometry(0.0042, 0.009, 8), A, g, 0, y0 + 0.054, 0, { flat: true });                                                  // its flame
  }
  function pegasus(g, y0, col) {                 // knight: a winged horse
    const C = col[0], A = col[1];
    P(lathe([[0.001, 0], [0.0105, 0], [0.0098, 0.006], [0.0072, 0.01], [0.001, 0.0105]]), C, g, 0, y0, 0, { flat: true });                 // a rock under the hooves
    P(S(0.0092), C, g, 0, y0 + 0.017, 0.0005, { scale: [0.85, 1.05, 1.15] });                                                             // chest
    for (const s of [-1, 1]) limb(g, [s * 0.0042, y0 + 0.012, 0.004], [s * 0.004, y0 + 0.007, 0.0105], 0.0022, 0.0019, C);                // forelegs, folded
    limb(g, [0, y0 + 0.02, 0.002], [0, y0 + 0.036, 0.0075], 0.0062, 0.0046, C);                                                            // neck
    P(S(0.006), C, g, 0, y0 + 0.0385, 0.0112, { scale: [0.78, 0.82, 1.6], rot: [0.55, 0, 0] });                                            // head, the muzzle down
    for (const s of [-1, 1]) { P(new THREE.ConeGeometry(0.0014, 0.0052, 6), C, g, s * 0.0024, y0 + 0.0445, 0.0068, { rot: [-0.25, 0, s * -0.2] });
      P(S(0.0009, 8, 6), col[2], g, s * 0.0036, y0 + 0.0395, 0.0118, { line: false }); }
    P(new THREE.BoxGeometry(0.0022, 0.021, 0.0042), A, g, 0, y0 + 0.031, 0.0016, { rot: [-0.32, 0, 0] });                                 // the mane
    for (const s of [-1, 1]) { const w = new THREE.Group(); w.position.set(s * 0.0062, y0 + 0.024, -0.0035); w.rotation.set(-0.35, 0, 0); g.add(w);
      [0.35, 0.68, 1.0].forEach((a, k) => { const m = P(S(0.0056, 10, 8), k === 1 ? A : C, w, 0, 0, 0, { scale: [0.34, 1.95 - k * 0.3, 0.75] });
        m.rotation.z = -s * a; m.position.set(s * Math.sin(a) * 0.0095, Math.cos(a) * 0.0095, -k * 0.0012); }); }
  }
  function sage(g, y0, col) {                    // bishop: a robed sage with a laurel wreath and a scroll
    const C = col[0], A = col[1];
    P(lathe([[0.001, 0], [0.0112, 0], [0.0106, 0.008], [0.0084, 0.027], [0.0088, 0.035], [0.006, 0.0415], [0.001, 0.0425]]), C, g, 0, y0, 0);
    P(new THREE.TorusGeometry(0.0094, 0.0016, 6, 20), C, g, 0.0006, y0 + 0.024, 0.0004, { rot: [Math.PI / 2 + 0.55, 0, 0.3], line: false });   // the himation's fold
    P(S(0.0061), C, g, 0, y0 + 0.048, 0.0006);
    P(new THREE.ConeGeometry(0.0043, 0.0092, 10), C, g, 0, y0 + 0.0425, 0.0042, { rot: [Math.PI + 0.22, 0, 0] });                          // beard
    P(new THREE.TorusGeometry(0.0061, 0.0013, 6, 20), A, g, 0, y0 + 0.0508, 0.0004, { rot: [Math.PI / 2 + 0.12, 0, 0] });                  // laurel
    for (let k = 0; k < 8; k++) { const a = k / 8 * Math.PI * 2; P(S(0.0013, 6, 4), A, g, Math.cos(a) * 0.0061, y0 + 0.0512, Math.sin(a) * 0.0061 + 0.0004, { scale: [1, 0.6, 1.6], line: false }); }
    for (const s of [-1, 1]) limb(g, [s * 0.0068, y0 + 0.037, 0.0005], [s * 0.004, y0 + 0.029, 0.0085], 0.0024, 0.0021, C);
    P(new THREE.CylinderGeometry(0.0021, 0.0021, 0.013, 10), A, g, 0, y0 + 0.029, 0.0098, { rot: [0, 0, Math.PI / 2] });                  // the scroll
  }
  function goddess(g, y0, col) {                 // queen: a long dress, a diadem, a torch raised in her right hand
    const C = col[0], A = col[1];
    P(lathe([[0.001, 0], [0.0122, 0], [0.0116, 0.006], [0.0084, 0.03], [0.0071, 0.039], [0.0081, 0.045], [0.0059, 0.0495], [0.001, 0.0505]]), C, g, 0, y0, 0);
    P(S(0.0061), C, g, 0, y0 + 0.0562, 0.0005);
    P(S(0.0041), C, g, 0, y0 + 0.058, -0.0052);                                                                                            // hair bun
    P(new THREE.CylinderGeometry(0.0063, 0.0059, 0.0034, 18, 1, true), A, g, 0, y0 + 0.0608, 0.0003, { line: false });
    for (let k = 0; k < 5; k++) { const a = Math.PI / 2 + (k - 2) * 0.42; P(new THREE.ConeGeometry(0.0012, 0.0042, 5), A, g, Math.cos(a) * 0.0059, y0 + 0.0642, Math.sin(a) * 0.0059, { line: false }); }
    limb(g, [0.0066, y0 + 0.046, 0], [0.0102, y0 + 0.054, 0.0022], 0.0022, 0.002, C); limb(g, [0.0102, y0 + 0.054, 0.0022], [0.0092, y0 + 0.064, 0.0026], 0.002, 0.0019, C);
    limb(g, [0.0092, y0 + 0.061, 0.0026], [0.0092, y0 + 0.073, 0.0026], 0.0013, 0.0018, C);                                              // the torch
    P(new THREE.ConeGeometry(0.0034, 0.0078, 8), A, g, 0.0092, y0 + 0.0772, 0.0026, { flat: true });
    limb(g, [-0.0066, y0 + 0.046, 0], [-0.0078, y0 + 0.032, 0.0062], 0.0022, 0.002, C);
  }
  function hero(g, y1, col, kind) {              // the kings' shared body: legs, a loincloth, a broad chest, shoulders
    const C = col[0];
    for (const s of [-1, 1]) { limb(g, [s * 0.0046, y1, 0.0008], [s * 0.0041, y1 + 0.021, 0], 0.0034, 0.0043, C); P(new THREE.BoxGeometry(0.0046, 0.0028, 0.0078), C, g, s * 0.0046, y1 + 0.0014, 0.0026); }
    P(lathe([[0.001, 0], [0.0092, 0], [0.0087, 0.0075], [0.0081, 0.0102], [0.001, 0.0102]]), kind === "hercules" ? col[1] : C, g, 0, y1 + 0.0165, 0);
    P(S(0.0104), C, g, 0, y1 + 0.035, 0, { scale: [1.16, 1.2, 0.8] });
    for (const s of [-1, 1]) { P(S(0.0042, 10, 8), C, g, s * 0.0042, y1 + 0.039, 0.0062, { scale: [1, 0.8, 0.6], line: false }); P(S(0.0048), C, g, s * 0.0119, y1 + 0.0425, 0); }
  }
  function minotaur(g, y0, col) {                // the gold king on a column drum
    const C = col[0], A = col[1], D = col[2];
    P(new THREE.CylinderGeometry(0.0124, 0.0134, 0.014, 14), C, g, 0, y0 + 0.007, 0, { flat: true });
    P(new THREE.BoxGeometry(0.027, 0.003, 0.027), C, g, 0, y0 + 0.0155, 0);
    const y1 = y0 + 0.017; hero(g, y1, col, "minotaur");
    for (const s of [-1, 1]) { limb(g, [s * 0.0126, y1 + 0.041, 0], [s * 0.0146, y1 + 0.026, 0.002], 0.0037, 0.0032, C); limb(g, [s * 0.0146, y1 + 0.026, 0.002], [s * 0.0142, y1 + 0.0135, 0.0042], 0.003, 0.0034, C);
      P(S(0.0036), C, g, s * 0.0142, y1 + 0.0115, 0.0045); }
    const hd = new THREE.Group(); hd.position.set(0, y1 + 0.0455, 0.001); g.add(hd);
    limb(hd, [0, -0.002, 0], [0, 0.0065, 0.0018], 0.0058, 0.0052, C);
    P(S(0.0073), C, hd, 0, 0.0098, 0.0018, { scale: [1, 0.95, 1.1] });
    P(S(0.0053), C, hd, 0, 0.0062, 0.0082, { scale: [1.05, 0.85, 1.0] });                                                                  // the muzzle
    for (const s of [-1, 1]) { P(S(0.0009, 8, 6), D, hd, s * 0.0022, 0.0058, 0.0131, { line: false }); P(S(0.001, 8, 6), D, hd, s * 0.0041, 0.0118, 0.0081, { line: false });
      P(new THREE.ConeGeometry(0.0021, 0.0058, 6), C, hd, s * 0.0083, 0.0108, 0.0004, { rot: [0, 0, -s * 1.35], scale: [1, 1, 0.55] });     // ears
      const h = new THREE.Group(); h.position.set(s * 0.0062, 0.0142, 0.0012); h.rotation.y = s > 0 ? 0 : Math.PI; hd.add(h);
      P(new THREE.TorusGeometry(0.0062, 0.0016, 6, 12, Math.PI * 0.78), A, h, 0, 0.0062, 0, { rot: [0, 0, -Math.PI / 2] });                // the horns: out, then up
      P(new THREE.ConeGeometry(0.0016, 0.0042, 6), A, h, 0.0062 * Math.cos(Math.PI * 0.28), 0.0062 + 0.0062 * Math.sin(Math.PI * 0.28) + 0.0012, 0, { rot: [0, 0, 0.5], line: false }); }
    P(new THREE.TorusGeometry(0.0021, 0.0006, 6, 14), A, hd, 0, 0.0034, 0.0124, { line: false });                                         // a ring in its nose
    g.userData.head = hd;
  }
  function hercules(g, y0, col) {                // the red king: a lion pelt over his head, a club in his right hand
    const C = col[0], A = col[1], D = col[2];
    P(new THREE.DodecahedronGeometry(0.0118, 0), C, g, 0, y0 + 0.002, 0, { scale: [1.3, 0.55, 1.2], flat: true });                         // a rock
    const y1 = y0 + 0.0085; hero(g, y1, col, "hercules");
    P(S(0.0118), C, g, 0, y1 + 0.031, -0.0078, { scale: [1.12, 1.65, 0.36] });                                                             // the pelt down his back
    P(S(0.0066), C, g, 0, y1 + 0.0528, 0.0014);
    P(S(0.0049), C, g, 0, y1 + 0.0488, 0.0046, { scale: [1, 1.12, 0.72] });                                                                // beard
    P(new THREE.SphereGeometry(0.0078, 14, 10, 0, Math.PI * 2, 0, Math.PI * 0.56), A, g, 0, y1 + 0.0538, -0.0004, { scale: [1.05, 1.08, 1.12] });   // the lion's head as a hood
    P(S(0.0036), A, g, 0, y1 + 0.0598, 0.0062, { scale: [1.25, 0.7, 1] });
    for (const s of [-1, 1]) { P(S(0.0022, 8, 6), A, g, s * 0.0056, y1 + 0.0612, -0.0008); P(S(0.0028, 8, 6), A, g, s * 0.003, y1 + 0.0438, 0.0084);   // ears; the paws knotted on his chest
      P(S(0.0008, 8, 6), D, g, s * 0.0025, y1 + 0.0605, 0.0094, { line: false }); }
    limb(g, [-0.0126, y1 + 0.041, 0], [-0.0146, y1 + 0.026, 0.002], 0.0037, 0.0032, C); limb(g, [-0.0146, y1 + 0.026, 0.002], [-0.014, y1 + 0.0135, 0.0045], 0.003, 0.0034, C);
    P(S(0.0036), C, g, -0.014, y1 + 0.0115, 0.0048);
    const arm = new THREE.Group(); arm.position.set(0.0126, y1 + 0.041, 0); g.add(arm);
    limb(arm, [0, 0, 0], [0.002, -0.015, 0.002], 0.0037, 0.0032, C); limb(arm, [0.002, -0.015, 0.002], [0.0022, -0.0255, 0.0072], 0.003, 0.0034, C);
    P(S(0.0036), C, arm, 0.0022, -0.0272, 0.0078);
    const club = new THREE.Group(); club.position.set(0.0022, -0.0272, 0.0078); arm.add(club);                                           // the club: grip in the fist, the head toward the base
    const dir = V(0.12, -0.55, 0.83).normalize(), cm = P(new THREE.CylinderGeometry(0.0021, 0.0046, 0.0235, 9), C, club, 0, 0, 0, { flat: true });
    cm.quaternion.setFromUnitVectors(V(0, -1, 0), dir); cm.position.copy(dir.clone().multiplyScalar(0.0105));
    for (let k = 0; k < 3; k++) P(S(0.0013, 6, 4), C, club, ...dir.clone().multiplyScalar(0.012 + k * 0.004).add(V(Math.cos(k * 2.1) * 0.0034, 0, Math.sin(k * 2.1) * 0.0034)).toArray(), { line: false });
    g.userData.club = arm;
  }
  function piece(type, col) {
    const g = new THREE.Group(), y0 = base(g, { pawn: 0.0148, king: 0.0188, queen: 0.0172 }[type] ?? 0.0165, col);
    ({ pawn: hoplite, rook: column, knight: pegasus, bishop: sage, queen: goddess })[type]?.(g, y0, col);
    if (type === "king") (col === SIDES.gold ? minotaur : hercules)(g, y0, col);
    g.userData.type = type; scene.add(g); return g;
  }

  // ---------------- the board: 52 × 50 cm with its walls and temple ----------------
  // local axes as the shop's other boards: file 0..7 = a..h along x, rank 0..7 = 1..8 along -z (sq() gives the centre
  // of a square on the board's top). BD = 0.52 along the ranks (the walls at the two ends are 6 cm thick), BW = 0.50
  // along the files (5 cm walls at the sides). The temple stands in the middle of the a-file side (local -x).
  function rock(w, h, d, seed, c = STONE) {
    const geo = new THREE.BoxGeometry(w, h, d, 2, 2, 2), p = geo.attributes.position;
    for (let i = 0; i < p.count; i++) { const x = p.getX(i), y = p.getY(i), z = p.getZ(i), k = seed * 31 + i * 7.3;
      if (y > -h / 2 + 1e-6) { const top = y > h / 2 - 1e-6, f = top ? 0.88 : 1;
        p.setXYZ(i, x * f + (rnd(k) - 0.5) * Math.min(w, 0.03) * 0.16, y + (top ? (rnd(k + 2) - 0.5) * h * 0.18 : (rnd(k + 3) - 0.5) * h * 0.06), z * f + (rnd(k + 1) - 0.5) * Math.min(d, 0.03) * 0.16); } }
    const m = new THREE.Mesh(facets(geo), toon(c, { rim: 0.2 })); shade(m); outline(m, WO * 1.4); return m;
  }
  function board(opt = {}) {
    const SQ = 0.05, BW = 0.5, BD = 0.52, T = 0.012, IN = SQ * 4, g = new THREE.Group(); scene.add(g);
    const slab = new THREE.Mesh(new THREE.BoxGeometry(BW, T, BD), toon(STONE_B, { spec: 0.1 })); slab.position.y = T / 2; shade(slab); g.add(slab); outline(slab, WO * 1.5);
    const cv = document.createElement("canvas"); cv.width = cv.height = 512; const c = cv.getContext("2d"), q = 64;
    for (let i = 0; i < 8; i++) for (let j = 0; j < 8; j++) { const light = (i + j) % 2 === 1; c.fillStyle = light ? "#E6B23E" : "#C44A31"; c.fillRect(i * q, j * q, q, q);
      c.fillStyle = light ? "rgba(255,240,180,0.35)" : "rgba(240,120,80,0.25)"; c.fillRect(i * q + 5, j * q + 5, q - 10, 4); }
    c.strokeStyle = "#E9C870"; c.lineWidth = 3; for (let k = 0; k <= 8; k++) { c.beginPath(); c.moveTo(k * q, 0); c.lineTo(k * q, 512); c.stroke(); c.beginPath(); c.moveTo(0, k * q); c.lineTo(512, k * q); c.stroke(); }
    const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
    const top = new THREE.Mesh(new THREE.PlaneGeometry(SQ * 8, SQ * 8), toon("#ffffff", { map: tex, rim: 0 })); top.rotation.x = -Math.PI / 2; top.position.y = T + 0.0004; top.receiveShadow = true; g.add(top);
    // the walls: on each side an inner row and an outer row of hewn blocks, a narrow passage between them, cross blocks
    // that close the passage here and there (seen from above: a labyrinth), taller blocks at the corners
    const BLOCKS = [], TEMPLE_Z = 0.085;
    const add = (cx, cz, w, d, h, seed) => { const m = rock(w, h, d, seed); m.position.set(cx, T + h / 2, cz); g.add(m);
      BLOCKS.push({ min: V(cx - w / 2, T, cz - d / 2), max: V(cx + w / 2, T + h, cz + d / 2), m }); };
    let seed = 1;
    const sides = [   // [along: "x" or "z", fixed coordinate sign, band from IN to the edge, which side is the front (lower walls)]
      { along: "x", fix: BD / 2, band: BD / 2 - IN, lo: 0.75 },     // rank-1 end (local +z)
      { along: "x", fix: -BD / 2, band: BD / 2 - IN, lo: 0.75 },    // rank-8 end (local -z)
      { along: "z", fix: BW / 2, band: BW / 2 - IN, lo: 0.6 },      // h-file side (local +x): the front in the reel, kept low
      { along: "z", fix: -BW / 2, band: BW / 2 - IN, lo: 1.0 },     // a-file side (local -x): the temple
    ];
    const CORR = 0.011, PASS = [];
    for (const sd of sides) {
      const sg = Math.sign(sd.fix), inner = (sd.band - CORR) * 0.52, outer = sd.band - CORR - inner;
      const cIn = sg * (IN + inner / 2), cOut = sg * (IN + inner + CORR + outer / 2), cPass = sg * (IN + inner + CORR / 2);
      const L = sd.along === "x" ? BW / 2 : BD / 2;                   // run from -L to L along the side (corners belong to the end walls)
      const from = sd.along === "x" ? -L : -(BD / 2 - (BD / 2 - IN)), to = -from;
      PASS.push({ along: sd.along, at: cPass, from, to });
      for (const [row, cc, wid] of [[0, cIn, inner], [1, cOut, outer]]) {
        let u = from;
        while (u < to - 0.004) {
          let len = 0.055 + rnd(seed * 3.1) * 0.05; if (to - u - len < 0.03) len = to - u;
          if (sd.fix < 0 && sd.along === "z") {                                     // the temple's place: no wall there
            if (u >= -TEMPLE_Z - 0.001 && u < TEMPLE_Z) { u = TEMPLE_Z; continue; }
            if (u < -TEMPLE_Z && u + len > -TEMPLE_Z) { len = -TEMPLE_Z - u; if (len < 0.015) { u = TEMPLE_Z; continue; } } }
          const mid = u + len / 2;
          const corner = sd.along === "x" && Math.abs(mid) > L - 0.06;
          const h = (corner ? 0.062 + rnd(seed) * 0.022 : (0.028 + rnd(seed + 0.5) * 0.03 + (row === 0 ? 0.008 : 0)) * sd.lo);
          const gap = 0.0025;
          if (sd.along === "x") add(mid, cc, len - gap, wid, h, seed); else add(cc, mid, wid, len - gap, h, seed);
          if (row === 0 && rnd(seed + 7.7) > 0.55 && to - u - len > 0.02) {          // a cross block closes the passage after this one
            const ch = Math.min(h, 0.03 + rnd(seed + 1.3) * 0.02) * sd.lo + 0.004, at = u + len;
            if (sd.along === "x") add(at, cPass, 0.012, CORR + 0.004, ch, seed + 50); else if (!(sd.fix < 0 && Math.abs(at) < TEMPLE_Z + 0.01)) add(cPass, at, CORR + 0.004, 0.012, ch, seed + 50); }
          u += len; seed++;
        }
      }
    }
    // the temple: two steps, six columns facing the board, an entablature and a pediment
    const TPL = new THREE.Group(); TPL.position.set(-BW / 2 + (BW / 2 - IN) / 2, T, 0); g.add(TPL);
    const dW = BW / 2 - IN - 0.002, wZ = TEMPLE_Z * 2 - 0.006, mat = (cc) => toon(cc, { spec: 0.15 });
    const box = (w, h, d, x, y, z) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat(STONE)); m.position.set(x, y, z); shade(m); TPL.add(m); outline(m, WO * 1.4); return m; };
    box(dW, 0.005, wZ, 0, 0.0025, 0); box(dW - 0.006, 0.005, wZ - 0.008, 0, 0.0075, 0);
    const colH = 0.05;
    for (let k = 0; k < 6; k++) { const z = (k - 2.5) * (wZ - 0.024) / 5;
      for (const x of [dW / 2 - 0.009, -dW / 2 + 0.009]) { const m = new THREE.Mesh(facets(new THREE.CylinderGeometry(0.0042, 0.0049, colH, 12)), toon(STONE, { spec: 0.15 })); m.position.set(x, 0.01 + colH / 2, z); shade(m); TPL.add(m); outline(m, WO * 1.2);
        box(0.011, 0.003, 0.011, x, 0.01 + colH + 0.0015, z); } }
    box(dW - 0.004, 0.009, wZ - 0.004, 0, 0.01 + colH + 0.0075, 0);
    { const sh = new THREE.Shape(); sh.moveTo(-(wZ - 0.004) / 2, 0); sh.lineTo((wZ - 0.004) / 2, 0); sh.lineTo(0, 0.026); sh.closePath();
      const geo = new THREE.ExtrudeGeometry(sh, { depth: dW - 0.004, bevelEnabled: false }); geo.translate(0, 0, -(dW - 0.004) / 2);
      const m = new THREE.Mesh(geo, mat(STONE)); m.rotation.y = Math.PI / 2; m.position.y = 0.01 + colH + 0.012; shade(m); TPL.add(m); outline(m, WO * 1.4);
      const fr = new THREE.Shape(); fr.moveTo(-(wZ - 0.03) / 2, 0.003); fr.lineTo((wZ - 0.03) / 2, 0.003); fr.lineTo(0, 0.019); fr.closePath();     // the tympanum, a shade darker
      const f2 = new THREE.Mesh(new THREE.ShapeGeometry(fr), mat(STONE_B)); f2.rotation.y = Math.PI / 2; f2.position.set(dW / 2 - 0.0015, 0.01 + colH + 0.012, 0); TPL.add(f2); }
    const TBOX = { min: V(-BW / 2, T, -TEMPLE_Z), max: V(-IN, T + 0.01 + colH + 0.04, TEMPLE_Z) };
    const sq = (file, rank) => g.localToWorld(V((file - 3.5) * SQ, T, (3.5 - rank) * SQ));
    return { g, sq, S: SQ, T, BW, BD, IN, BLOCKS, PASS, TBOX, TPL, top: () => g.position.y + T };
  }
  return { SIDES, piece, board, STONE };
}
