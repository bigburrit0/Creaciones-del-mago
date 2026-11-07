/* ajedrez3d.js: the shop's best sellers as toon props: a wooden board and the VIKING and MEDIEVAL chess sets, modelled
   from the site's own photos (assets/p/vikingos.webp, medieval.webp, medieval-p.webp).
   Viking: king in furs with a sword, shieldmaiden queen with a round shield, a bear-hooded seer (bishop), a dragon-prow
   knight, a stave-church rook, shield-and-helmet pawns, all on turned pedestals. Medieval: armoured king with a great
   helm, crown and heater shield; crowned queen; mitred bishop with a crosier; a barded warhorse knight; a crenellated
   castle rook; foot-soldier pawns with kettle helms. Sizes in metres (a 10 cm king), so they sit at real scale in the
   workshop. Every piece is a Group whose origin is the centre of its base; animate g.position / g.rotation freely.
   Usage: const CK = chessKit(scene, { wo }); const b = CK.board(); const k = CK.piece("viking", "king", CK.SIDES.bronze); */
import * as THREE from "three";
import { toon, outline, shade } from "./toon3d.js";

export function chessKit(scene, o = {}) {
  const WO = (o.wo ?? 0.0024) * 0.4;
  const V2 = (x, y) => new THREE.Vector2(x, y);
  const SIDES = {                               // [main, accent, dark detail]
    bronze: ["#B8873A", "#E2B95C", "#5A3A16"], silver: ["#9AA3AE", "#D7DCE2", "#3C4250"],
    gold: ["#C9A23A", "#F0D277", "#5A4210"], grey: ["#6E7480", "#A9AFB9", "#2A2E36"],
    red: ["#B5302A", "#E06A4A", "#4A1210"], black: ["#2E2B36", "#6A6578", "#121016"],
  };
  function P(geo, c, parent, x = 0, y = 0, z = 0, opt = {}) {
    const m = new THREE.Mesh(geo, toon(c, { spec: opt.spec ?? 0.45 })); m.position.set(x, y, z);
    if (opt.rot) m.rotation.set(...opt.rot); if (opt.scale) m.scale.set(...opt.scale); shade(m); parent.add(m);
    if (opt.line !== false) outline(m, opt.w ?? WO); return m;
  }
  const lathe = (pts, n = 28) => new THREE.LatheGeometry(pts.map(([r, y]) => V2(r, y)), n);
  function pedestal(g, r, col) {                // a turned base: foot, bead, waist, collar. Returns the top height
    P(lathe([[0.001, 0], [r, 0], [r, 0.0035], [r * 0.95, 0.0055], [r * 0.95, 0.0075], [r * 0.82, 0.0095], [r * 0.72, 0.013], [r * 0.7, 0.0155], [r * 0.78, 0.0175], [r * 0.6, 0.019], [0.001, 0.019]]), col[0], g);
    P(new THREE.TorusGeometry(r * 0.96, 0.0012, 6, 28), col[1], g, 0, 0.0065, 0, { rot: [Math.PI / 2, 0, 0], line: false });
    return 0.019;
  }
  const robe = (g, y0, r0, r1, h, c, n = 24) => P(lathe([[0.001, 0], [r0, 0], [r0 * 1.02, h * 0.15], [(r0 + r1) / 2, h * 0.6], [r1, h * 0.92], [r1 * 0.6, h], [0.001, h]], n), c, g, 0, y0, 0);
  function heater(w, h, d = 0.0018) {           // a heater (knight's) shield outline, extruded
    const s = new THREE.Shape(); s.moveTo(-w, h * 0.45); s.lineTo(w, h * 0.45); s.lineTo(w, 0); s.quadraticCurveTo(w, -h * 0.35, 0, -h * 0.55); s.quadraticCurveTo(-w, -h * 0.35, -w, 0); s.closePath();
    const geo = new THREE.ExtrudeGeometry(s, { depth: d, bevelEnabled: true, bevelThickness: 0.0006, bevelSize: 0.0006, bevelSegments: 1 }); geo.translate(0, 0, -d / 2); return geo;
  }
  function crossOn(g, x, y, z, s, c) { P(new THREE.BoxGeometry(s * 0.22, s, 0.0012), c, g, x, y, z, { line: false }); P(new THREE.BoxGeometry(s * 0.7, s * 0.22, 0.0012), c, g, x, y + s * 0.15, z, { line: false }); }
  function roundShield(g, x, y, z, r, col, rotY = 0) {
    const sh = new THREE.Group(); sh.position.set(x, y, z); sh.rotation.y = rotY; g.add(sh);
    P(new THREE.CylinderGeometry(r, r, 0.0028, 24), col[0], sh, 0, 0, 0, { rot: [Math.PI / 2, 0, 0] });
    P(new THREE.TorusGeometry(r, 0.0011, 6, 24), col[1], sh, 0, 0, 0.0012, { line: false });
    P(new THREE.SphereGeometry(r * 0.28, 12, 8), col[1], sh, 0, 0, 0.0016, { scale: [1, 1, 0.6], line: false });
    for (let k = 0; k < 4; k++) P(new THREE.BoxGeometry(0.0009, r * 1.6, 0.0006), col[2], sh, 0, 0, 0.0015, { rot: [0, 0, k * Math.PI / 4], line: false });
    return sh;
  }
  const furLathe = (pts, amp = 0.0011) => { const geo = lathe(pts, 32), p = geo.attributes.position; for (let i = 0; i < p.count; i++) { const x = p.getX(i), y = p.getY(i), z = p.getZ(i), a = Math.atan2(z, x), f = 1 + amp * 40 * Math.sin(a * 11 + y * 500) * Math.sin(y * 900); p.setXYZ(i, x * f, y, z * f); } geo.computeVertexNormals(); return geo; };

  // ---------------- VIKING ----------------
  function viking(type, col) {
    const g = new THREE.Group(), y0 = pedestal(g, type === "pawn" ? 0.0165 : 0.0205, col), C = col[0], A = col[1], D = col[2];
    const head = (y, r = 0.0085) => P(new THREE.SphereGeometry(r, 16, 12), C, g, 0, y, 0.001);
    if (type === "king") {                       // fur-clad warrior king, both hands on a sword planted in front
      P(furLathe([[0.001, 0], [0.0175, 0], [0.018, 0.012], [0.0165, 0.035], [0.0175, 0.046], [0.0185, 0.052], [0.011, 0.058], [0.001, 0.059]]), C, g, 0, y0, 0);
      head(y0 + 0.066); P(new THREE.ConeGeometry(0.0075, 0.018, 10), C, g, 0, y0 + 0.056, 0.007, { rot: [Math.PI + 0.25, 0, 0] });
      for (let k = 0; k < 5; k++) { const a = k / 5 * Math.PI * 2; P(new THREE.ConeGeometry(0.0022, 0.006, 4), A, g, Math.cos(a) * 0.0068, y0 + 0.0755, Math.sin(a) * 0.0068, { line: false }); }
      P(new THREE.TorusGeometry(0.0072, 0.0016, 6, 16), A, g, 0, y0 + 0.0725, 0.001, { rot: [Math.PI / 2, 0, 0] });
      P(new THREE.BoxGeometry(0.0034, 0.04, 0.0014), A, g, 0, y0 + 0.022, 0.0195); P(new THREE.BoxGeometry(0.016, 0.0024, 0.003), D, g, 0, y0 + 0.043, 0.0195);
      P(new THREE.CylinderGeometry(0.0016, 0.0016, 0.007, 8), D, g, 0, y0 + 0.048, 0.0195); P(new THREE.SphereGeometry(0.0026, 8, 6), A, g, 0, y0 + 0.0525, 0.0195);
      for (const s of [-1, 1]) P(new THREE.SphereGeometry(0.0032, 8, 6), C, g, s * 0.0034, y0 + 0.047, 0.0185);
    } else if (type === "queen") {               // shieldmaiden: long dress, long hair, a round shield held in front
      P(lathe([[0.001, 0], [0.0165, 0], [0.0155, 0.014], [0.012, 0.04], [0.0125, 0.05], [0.0085, 0.057], [0.001, 0.058]]), C, g, 0, y0, 0);
      head(y0 + 0.064, 0.0078); P(new THREE.SphereGeometry(0.0085, 12, 10), D, g, 0, y0 + 0.058, -0.004, { scale: [1, 2.1, 0.7] });
      P(new THREE.TorusGeometry(0.0068, 0.0012, 6, 16), A, g, 0, y0 + 0.069, 0.001, { rot: [Math.PI / 2, 0, 0], line: false });
      roundShield(g, 0, y0 + 0.028, 0.0175, 0.0145, col);
    } else if (type === "bishop") {              // the seer: a bear-skin hood with ears and snout, a long beard, a tall staff
      P(furLathe([[0.001, 0], [0.0165, 0], [0.016, 0.02], [0.013, 0.045], [0.0135, 0.058], [0.009, 0.064], [0.001, 0.065]], 0.0008), C, g, 0, y0, 0);
      head(y0 + 0.07, 0.0082); P(new THREE.SphereGeometry(0.0105, 14, 10), D, g, 0, y0 + 0.0745, -0.002, { scale: [1, 0.85, 1.05] });
      for (const s of [-1, 1]) P(new THREE.SphereGeometry(0.0032, 8, 6), D, g, s * 0.0072, y0 + 0.083, -0.002);
      P(new THREE.SphereGeometry(0.0045, 10, 8), D, g, 0, y0 + 0.0775, 0.0085, { scale: [0.9, 0.7, 1.3] });
      P(new THREE.ConeGeometry(0.0068, 0.022, 10), C, g, 0, y0 + 0.056, 0.0072, { rot: [Math.PI + 0.18, 0, 0] });
      P(new THREE.CylinderGeometry(0.0013, 0.0013, 0.085, 6), D, g, 0.0145, y0 + 0.042, 0.006); P(new THREE.TorusGeometry(0.0038, 0.0012, 6, 12), A, g, 0.0145, y0 + 0.087, 0.006, { line: false });
    } else if (type === "knight") {              // the dragon prow of a longship: a curled neck, a dragon head, a spiral
      const cv = new THREE.CatmullRomCurve3([[0, 0, -0.004], [0, 0.02, -0.007], [0, 0.04, -0.003], [0, 0.054, 0.006], [0, 0.058, 0.016]].map((p) => new THREE.Vector3(...p)));
      P(new THREE.TubeGeometry(cv, 20, 0.0078, 12), C, g, 0, y0, 0); P(new THREE.SphereGeometry(0.0085, 12, 10), C, g, 0, y0 + 0.001, -0.004, { scale: [1, 0.6, 1] });
      const hd = new THREE.Group(); hd.position.set(0, y0 + 0.058, 0.018); hd.rotation.x = 0.35; g.add(hd);
      P(new THREE.CapsuleGeometry(0.006, 0.014, 6, 12), C, hd, 0, 0, 0.004, { rot: [Math.PI / 2, 0, 0] });
      P(new THREE.CapsuleGeometry(0.0035, 0.006, 4, 8), C, hd, 0, -0.0045, 0.009, { rot: [Math.PI / 2, 0, 0] });
      for (const s of [-1, 1]) { P(new THREE.SphereGeometry(0.0018, 8, 6), D, hd, s * 0.0052, 0.0025, 0.004, { line: false }); P(new THREE.ConeGeometry(0.0017, 0.008, 6), A, hd, s * 0.0035, 0.007, -0.004, { rot: [-0.9, 0, s * 0.3] }); }
      P(new THREE.TorusGeometry(0.0085, 0.0018, 6, 18, Math.PI * 1.6), A, g, 0, y0 + 0.042, -0.0105, { rot: [0, Math.PI / 2, 0.6] });
      for (const s of [-1, 1]) P(new THREE.TorusGeometry(0.0042, 0.0009, 6, 14, Math.PI * 1.7), D, g, s * 0.0075, y0 + 0.026, -0.006, { rot: [0, Math.PI / 2, 0], line: false });
    } else if (type === "rook") {                // a stave church: a box nave, three tiered roofs, a spire
      P(new THREE.BoxGeometry(0.026, 0.022, 0.026), C, g, 0, y0 + 0.011, 0); P(new THREE.BoxGeometry(0.007, 0.012, 0.0016), D, g, 0, y0 + 0.006, 0.0131, { line: false });
      [[0.022, 0.012, 0.026], [0.016, 0.011, 0.037], [0.011, 0.011, 0.047]].forEach(([r, h, y], i) => { P(new THREE.ConeGeometry(r, h, 4), i % 2 ? A : C, g, 0, y0 + y, 0, { rot: [0, Math.PI / 4, 0] }); if (i < 2) P(new THREE.BoxGeometry(r * 1.05, 0.006, r * 1.05), C, g, 0, y0 + y + h * 0.45, 0); });
      P(new THREE.ConeGeometry(0.004, 0.02, 6), A, g, 0, y0 + 0.062, 0); P(new THREE.SphereGeometry(0.0018, 6, 4), A, g, 0, y0 + 0.073, 0, { line: false });
      for (const s of [-1, 1]) P(new THREE.ConeGeometry(0.0016, 0.007, 4), D, g, s * 0.012, y0 + 0.033, 0.012, { rot: [0.3, 0, -s * 0.9], line: false });
    } else {                                     // pawn: a warrior behind his round shield, with a helmet
      P(lathe([[0.001, 0], [0.0125, 0], [0.012, 0.016], [0.0095, 0.026], [0.006, 0.029], [0.001, 0.03]]), C, g, 0, y0, 0);
      head(y0 + 0.034, 0.0068); P(new THREE.SphereGeometry(0.0072, 12, 8, 0, Math.PI * 2, 0, Math.PI / 2), A, g, 0, y0 + 0.0355, 0.001); P(new THREE.BoxGeometry(0.0015, 0.006, 0.0015), A, g, 0, y0 + 0.033, 0.0075, { line: false });
      roundShield(g, 0, y0 + 0.015, 0.0125, 0.0105, col);
    }
    return g;
  }

  // ---------------- MEDIEVAL ----------------
  function medieval(type, col) {
    const g = new THREE.Group(), y0 = pedestal(g, type === "pawn" ? 0.0165 : 0.0205, col), C = col[0], A = col[1], D = col[2];
    const helm = (y, r = 0.0078) => { P(new THREE.CylinderGeometry(r, r * 1.05, r * 2, 14), C, g, 0, y, 0); P(new THREE.BoxGeometry(r * 1.4, 0.0011, 0.002), D, g, 0, y + r * 0.2, r * 0.98, { line: false }); P(new THREE.BoxGeometry(0.0011, r * 0.9, 0.002), D, g, 0, y - r * 0.25, r * 0.98, { line: false }); };
    if (type === "king") {                       // armoured king: surcoat, great helm with a crown, a heater shield with a cross
      robe(g, y0, 0.0172, 0.013, 0.05, C); P(new THREE.SphereGeometry(0.0105, 14, 10), C, g, 0, y0 + 0.05, 0, { scale: [1.25, 0.7, 1] });
      helm(y0 + 0.061); P(new THREE.CylinderGeometry(0.0088, 0.0088, 0.004, 16, 1, true), A, g, 0, y0 + 0.071, 0);
      for (let k = 0; k < 6; k++) { const a = k / 6 * Math.PI * 2; P(new THREE.ConeGeometry(0.0018, 0.005, 4), A, g, Math.cos(a) * 0.0086, y0 + 0.0755, Math.sin(a) * 0.0086, { line: false }); }
      P(new THREE.SphereGeometry(0.0022, 8, 6), A, g, 0, y0 + 0.0775, 0, { line: false }); crossOn(g, 0, y0 + 0.076, 0, 0.007, A);
      const sh = new THREE.Group(); sh.position.set(-0.004, y0 + 0.027, 0.0175); sh.rotation.y = 0.15; g.add(sh); P(heater(0.0105, 0.03), C, sh); crossOn(sh, 0, 0.0005, 0.0015, 0.014, A);
      P(new THREE.BoxGeometry(0.0024, 0.038, 0.0012), A, g, 0.0145, y0 + 0.022, 0.008); P(new THREE.BoxGeometry(0.011, 0.002, 0.0025), D, g, 0.0145, y0 + 0.041, 0.008);
    } else if (type === "queen") {               // crowned queen: a bell gown, wimple, tall crown
      P(lathe([[0.001, 0], [0.0175, 0], [0.0165, 0.01], [0.0115, 0.035], [0.009, 0.047], [0.0105, 0.051], [0.006, 0.055], [0.001, 0.056]]), C, g, 0, y0, 0);
      P(new THREE.SphereGeometry(0.0078, 14, 10), A, g, 0, y0 + 0.061, 0); P(new THREE.SphereGeometry(0.0092, 14, 10), C, g, 0, y0 + 0.059, -0.0025, { scale: [1, 1.15, 0.9] });
      P(new THREE.CylinderGeometry(0.0078, 0.0068, 0.009, 14, 1, true), A, g, 0, y0 + 0.0715, 0);
      for (let k = 0; k < 8; k++) { const a = k / 8 * Math.PI * 2; P(new THREE.SphereGeometry(0.0014, 6, 4), A, g, Math.cos(a) * 0.0078, y0 + 0.077, Math.sin(a) * 0.0078, { line: false }); }
      P(new THREE.TorusGeometry(0.0105, 0.0011, 6, 20), A, g, 0, y0 + 0.049, 0, { rot: [Math.PI / 2, 0, 0], line: false });
    } else if (type === "bishop") {              // mitre (split), robe with a cross, a crosier
      robe(g, y0, 0.0165, 0.012, 0.052, C); P(new THREE.SphereGeometry(0.0075, 14, 10), A, g, 0, y0 + 0.058, 0.001);
      P(new THREE.ConeGeometry(0.0082, 0.022, 4), C, g, 0, y0 + 0.074, 0, { rot: [0, Math.PI / 4, 0], scale: [1, 1, 0.62] }); P(new THREE.BoxGeometry(0.012, 0.009, 0.0016), D, g, 0, y0 + 0.077, 0.0012, { rot: [0, 0, 0.35], line: false });
      crossOn(g, 0, y0 + 0.032, 0.0128, 0.012, A);
      P(new THREE.CylinderGeometry(0.0012, 0.0012, 0.078, 6), A, g, -0.0145, y0 + 0.04, 0.005); P(new THREE.TorusGeometry(0.0042, 0.0012, 6, 14, Math.PI * 1.4), A, g, -0.0125, y0 + 0.081, 0.005, { rot: [0, 0, 0.4] });
    } else if (type === "knight") {              // a barded warhorse: arched neck, head and snout under a caparison with a cross, a plume
      const nk = new THREE.Group(); nk.position.set(0, y0, -0.002); g.add(nk);
      P(new THREE.CapsuleGeometry(0.0095, 0.03, 6, 14), C, nk, 0, 0.022, -0.002, { rot: [-0.25, 0, 0] });
      const hd = new THREE.Group(); hd.position.set(0, 0.045, 0.004); hd.rotation.x = 0.95; nk.add(hd);
      P(new THREE.CapsuleGeometry(0.0075, 0.018, 6, 12), C, hd, 0, 0.006, 0); P(new THREE.CapsuleGeometry(0.0055, 0.01, 4, 10), D, hd, 0, 0.018, 0.0012);
      for (const s of [-1, 1]) { P(new THREE.ConeGeometry(0.0022, 0.008, 6), C, nk, s * 0.0042, 0.06, -0.006, { rot: [-0.4, 0, -s * 0.2] }); P(new THREE.SphereGeometry(0.0015, 6, 4), D, hd, s * 0.0068, 0.004, 0.0035, { line: false }); }
      P(new THREE.CylinderGeometry(0.0125, 0.018, 0.03, 16, 1, true), A, nk, 0, 0.016, -0.001); crossOn(nk, 0, 0.015, 0.0175, 0.012, C);
      P(new THREE.SphereGeometry(0.0045, 8, 6), A, nk, 0, 0.064, -0.01, { scale: [0.7, 1.3, 1.4] });
    } else if (type === "rook") {                // castle tower: a cylinder, crenellations, an arched door, arrow slits
      P(lathe([[0.001, 0], [0.0155, 0], [0.0145, 0.04], [0.0165, 0.043], [0.0165, 0.05], [0.001, 0.05]]), C, g, 0, y0, 0);
      for (let k = 0; k < 8; k++) { const a = k / 8 * Math.PI * 2; P(new THREE.BoxGeometry(0.0055, 0.0065, 0.004), C, g, Math.cos(a) * 0.014, y0 + 0.0535, Math.sin(a) * 0.014, { rot: [0, -a, 0] }); }
      P(new THREE.BoxGeometry(0.0065, 0.011, 0.0016), D, g, 0, y0 + 0.0055, 0.0152, { line: false }); P(new THREE.SphereGeometry(0.0033, 10, 6, 0, Math.PI * 2, 0, Math.PI / 2), D, g, 0, y0 + 0.011, 0.0146, { scale: [1, 1, 0.4], line: false });
      for (const [a, y] of [[0.5, 0.028], [-0.9, 0.022]]) P(new THREE.BoxGeometry(0.0014, 0.0065, 0.0016), D, g, Math.sin(a) * 0.0149, y0 + y, Math.cos(a) * 0.0149, { rot: [0, a, 0], line: false });
      P(new THREE.CylinderGeometry(0.0007, 0.0007, 0.016, 4), D, g, 0, y0 + 0.058, 0, { line: false }); P(new THREE.BoxGeometry(0.0075, 0.005, 0.0008), A, g, 0.0038, y0 + 0.0635, 0, { line: false });
    } else {                                     // pawn: a foot soldier with a kettle helm and a small heater shield
      P(lathe([[0.001, 0], [0.0125, 0], [0.0118, 0.012], [0.0092, 0.025], [0.006, 0.028], [0.001, 0.029]]), C, g, 0, y0, 0);
      P(new THREE.SphereGeometry(0.0062, 12, 8), A, g, 0, y0 + 0.033, 0.0005); P(new THREE.SphereGeometry(0.0066, 12, 8, 0, Math.PI * 2, 0, Math.PI / 2), C, g, 0, y0 + 0.0345, 0); P(new THREE.TorusGeometry(0.0085, 0.0011, 6, 18), C, g, 0, y0 + 0.0345, 0, { rot: [Math.PI / 2, 0, 0] });
      const sh = new THREE.Group(); sh.position.set(0, y0 + 0.016, 0.012); g.add(sh); P(heater(0.0072, 0.019), C, sh); crossOn(sh, 0, 0.0005, 0.0013, 0.009, A);
    }
    return g;
  }

  function piece(set, type, col) { const g = set === "viking" ? viking(type, col) : medieval(type, col); g.userData = { set, type }; scene.add(g); return g; }

  // ---------------- the board: maple and walnut squares, a walnut frame ----------------
  function board(opt = {}) {
    const S = opt.square ?? 0.05, F = opt.frame ?? 0.022, T = opt.thick ?? 0.022, W = S * 8 + F * 2, g = new THREE.Group(); scene.add(g);
    const frame = new THREE.Mesh(new THREE.BoxGeometry(W, T, W), toon(opt.frameCol ?? "#6B3E22", { spec: 0.35 })); frame.position.y = T / 2; shade(frame); g.add(frame); outline(frame, WO * 1.5);
    const cv = document.createElement("canvas"); cv.width = cv.height = 512; const c = cv.getContext("2d"), q = 64;
    for (let i = 0; i < 8; i++) for (let j = 0; j < 8; j++) { const light = (i + j) % 2 === 1; c.fillStyle = light ? (opt.light ?? "#DDB57E") : (opt.dark ?? "#8A5532"); c.fillRect(i * q, j * q, q, q);
      c.strokeStyle = light ? "rgba(150,100,50,0.18)" : "rgba(40,20,10,0.22)"; c.lineWidth = 1.2; for (let k = 0; k < 6; k++) { const y = j * q + 6 + k * 10 + ((i * 7 + j * 3 + k) % 4); c.beginPath(); c.moveTo(i * q, y); c.bezierCurveTo(i * q + 20, y - 3, i * q + 44, y + 3, i * q + q, y - 1); c.stroke(); } }
    c.strokeStyle = "rgba(30,15,8,0.55)"; c.lineWidth = 2; c.strokeRect(1, 1, 510, 510);
    const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
    const top = new THREE.Mesh(new THREE.PlaneGeometry(S * 8, S * 8), toon("#ffffff", { map: tex, rim: 0 })); top.rotation.x = -Math.PI / 2; top.position.y = T + 0.0004; top.receiveShadow = true; g.add(top);
    const sq = (file, rank) => g.localToWorld(new THREE.Vector3((file - 3.5) * S, T, (3.5 - rank) * S));   // file 0..7 = a..h (left to right from White), rank 0..7 = 1..8 (away from White)
    return { g, sq, S, T, W, top: () => g.position.y + T };
  }
  // the 16 + 16 pieces in their starting squares; White on ranks 1-2 (nearest the camera when the board is not rotated)
  function setup(b, set, colW, colB) {
    const back = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"], out = { W: [], B: [] };
    for (const [side, col, r0, r1, rot] of [["W", colW, 0, 1, 0], ["B", colB, 7, 6, Math.PI]]) for (let f = 0; f < 8; f++) {
      const a = piece(set, back[f], col), p = piece(set, "pawn", col); a.position.copy(b.sq(f, r0)); p.position.copy(b.sq(f, r1)); a.rotation.y = p.rotation.y = rot + b.g.rotation.y;
      a.userData.home = [f, r0]; p.userData.home = [f, r1]; out[side].push(a, p); }
    return out;
  }
  return { SIDES, piece, board, setup };
}
