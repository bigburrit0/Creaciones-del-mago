/* mascotas3d.js: the shop's "Perros contra gatos" chess set as toon props, modelled from its photo
   (assets/p/perros-gatos.webp: brown dogs on round bases. Pawns are seated pugs; bishops are hounds in hooded capes with
   a round medallion; the king is a boxer with a cape and a crown; the queen is a retriever with a small crown and a cape).
   The photo shows only the dogs: the cats are built in the same style (seated cats on round bases; kittens for pawns,
   a crowned cat with a cape for the king, a tiara for the queen, hooded capes for the bishops). Knights and rooks are
   not in the photo either: a terrier with a scarf and a big sitting dog with a collar; a cat with a raised tail and a
   loaf cat. Sizes in metres (king 9.5 cm, as the shop's tournament size). Every piece is a Group whose origin is the
   centre of its base and whose FRONT (the muzzle) is local +z; animate g.position / g.rotation freely.
   Animated parts in g.userData: head (a Group: nod, look), tail (a Group: wag), paw (the right front leg, a Group
   pivoting at the shoulder: a cat's push), ears (Groups: droop).
   Usage: const PK = petKit(scene, { wo }); const k = PK.piece("dog", "king", PK.COLS.dog); */
import * as THREE from "three";
import { toon, outline, shade } from "./toon3d.js";

export function petKit(scene, o = {}) {
  const WO = (o.wo ?? 0.0024) * 0.4;
  const COLS = { dog: ["#8A5A3B", "#C9A26B", "#3A2416"], cat: ["#D9D2C5", "#F2C14E", "#4A4038"] };   // [main, accent (crowns, medallions), dark (noses, eyes)]
  function P(geo, c, parent, x = 0, y = 0, z = 0, opt = {}) {
    const m = new THREE.Mesh(geo, toon(c, { spec: opt.spec ?? 0.35 })); m.position.set(x, y, z);
    if (opt.rot) m.rotation.set(...opt.rot); if (opt.scale) m.scale.set(...opt.scale); shade(m); parent.add(m);
    if (opt.line !== false) outline(m, opt.w ?? WO); return m;
  }
  const S = (r, w = 14, h = 10) => new THREE.SphereGeometry(r, w, h);
  const lathe = (pts, n = 28) => new THREE.LatheGeometry(pts.map(([r, y]) => new THREE.Vector2(r, y)), n);
  function base(g, r, col) { P(lathe([[0.001, 0], [r, 0], [r, 0.004], [r * 0.96, 0.0055], [0.001, 0.0058]]), col[0], g); return 0.0055; }
  // a seated four-legged body: haunches, chest, two front legs (the right one is a pivoting paw), a tail
  function body(g, y0, sz, col, kind) {
    const C = col[0];
    P(S(0.0125 * sz), C, g, 0, y0 + 0.011 * sz, -0.003 * sz, { scale: [1.05, 0.95, 1.15] });                  // haunches
    P(S(0.0105 * sz), C, g, 0, y0 + 0.024 * sz, 0.002 * sz, { scale: [0.95, 1.25, 0.9] });                     // chest
    const legs = {};
    for (const s of [-1, 1]) { const lg = new THREE.Group(); lg.position.set(s * 0.0052 * sz, y0 + 0.022 * sz, 0.0065 * sz); g.add(lg);
      P(new THREE.CapsuleGeometry(0.0026 * sz, 0.016 * sz, 4, 8), C, lg, 0, -0.0105 * sz, 0.001 * sz);
      P(S(0.0032 * sz, 10, 8), C, lg, 0, -0.02 * sz, 0.0028 * sz, { scale: [1, 0.65, 1.3] });                  // the paw
      legs[s] = lg; }
    const tail = new THREE.Group(); tail.position.set(0, y0 + 0.006 * sz, -0.014 * sz); g.add(tail);
    if (kind === "cat") { const cv = new THREE.CatmullRomCurve3([[0, 0, 0], [0.006, 0.002, -0.006], [0.012, 0.01, -0.004], [0.013, 0.02, 0.0]].map((p) => new THREE.Vector3(...p).multiplyScalar(sz)));
      P(new THREE.TubeGeometry(cv, 12, 0.0022 * sz, 8), C, tail); }
    else P(new THREE.CapsuleGeometry(0.0022 * sz, 0.008 * sz, 4, 8), C, tail, 0, 0.004 * sz, -0.002 * sz, { rot: [-0.7, 0, 0] });
    return { legs, tail };
  }
  function dogHead(g, y, sz, col, breed) {
    const C = col[0], D = col[2], hd = new THREE.Group(); hd.position.set(0, y, 0.004 * sz); g.add(hd);
    const r = 0.0085 * sz; P(S(r), C, hd, 0, 0, 0, { scale: breed === "pug" ? [1.1, 1, 1] : [1, 1.05, 1.05] });
    const snout = breed === "pug" ? [0.006, 0.004, 0.75] : breed === "hound" ? [0.0058, 0.011, 1.0] : breed === "boxer" ? [0.0065, 0.007, 0.9] : [0.0052, 0.009, 1.0];
    P(new THREE.CapsuleGeometry(snout[0] * sz, snout[1] * sz, 4, 10), C, hd, 0, -0.002 * sz, r * snout[2] + snout[1] * sz * 0.35, { rot: [Math.PI / 2, 0, 0] });
    P(S(0.0022 * sz, 8, 6), D, hd, 0, -0.0005 * sz, r * snout[2] + snout[1] * sz * 0.9 + 0.003 * sz, { line: false });        // nose
    for (const s of [-1, 1]) P(S(0.0013 * sz, 8, 6), D, hd, s * 0.0036 * sz, 0.0025 * sz, r * 0.86, { line: false });    // eyes
    const ears = [];
    for (const s of [-1, 1]) { const e = new THREE.Group(); e.position.set(s * r * 0.82, r * 0.45, -0.001 * sz); hd.add(e);
      const long = breed === "hound" ? 2.4 : breed === "retriever" ? 1.7 : breed === "terrier" ? 1.0 : 1.1;
      if (breed === "terrier") P(new THREE.ConeGeometry(0.003 * sz, 0.007 * sz, 6), C, e, s * 0.001 * sz, 0.003 * sz, 0, { rot: [0, 0, -s * 0.3] });
      else P(S(0.0038 * sz, 10, 8), C, e, s * 0.0012 * sz, -0.004 * sz * long, 0, { scale: [0.55, long, 0.9] });
      e.userData.s = s; ears.push(e); }
    if (breed === "pug") for (const s of [-1, 1]) P(new THREE.TorusGeometry(0.003 * sz, 0.0006 * sz, 4, 10, Math.PI), D, hd, s * 0.0016 * sz, 0.0042 * sz, r * 0.9, { rot: [0, 0, 0], line: false });   // forehead wrinkles
    return { hd, ears };
  }
  function catHead(g, y, sz, col) {
    const C = col[0], D = col[2], hd = new THREE.Group(); hd.position.set(0, y, 0.003 * sz); g.add(hd);
    const r = 0.0082 * sz; P(S(r), C, hd, 0, 0, 0, { scale: [1.12, 0.95, 1] });
    P(S(0.0038 * sz, 10, 8), C, hd, 0, -0.0028 * sz, r * 0.82, { scale: [1.3, 0.8, 0.8] });                       // muzzle
    P(S(0.0012 * sz, 8, 6), "#C9787A", hd, 0, -0.0015 * sz, r * 1.08, { line: false });                          // nose
    for (const s of [-1, 1]) P(new THREE.SphereGeometry(0.0016 * sz, 8, 6), D, hd, s * 0.0036 * sz, 0.0012 * sz, r * 0.88, { scale: [1, 1.3, 0.6], line: false });
    const ears = [];
    for (const s of [-1, 1]) { const e = new THREE.Group(); e.position.set(s * r * 0.62, r * 0.72, 0); hd.add(e);
      P(new THREE.ConeGeometry(0.0034 * sz, 0.0075 * sz, 4), C, e, 0, 0.0028 * sz, 0, { rot: [0, Math.PI / 4, -s * 0.25] }); e.userData.s = s; ears.push(e); }
    return { hd, ears };
  }
  const crown = (parent, y, r, col, tall = 0.005) => { P(new THREE.CylinderGeometry(r, r * 1.04, 0.003, 16, 1, true), col[1], parent, 0, y, 0, { line: false });
    for (let k = 0; k < 5; k++) { const a = k / 5 * Math.PI * 2; P(new THREE.ConeGeometry(0.0016, tall, 4), col[1], parent, Math.cos(a) * r, y + 0.003 + tall / 2, Math.sin(a) * r, { line: false }); } };
  const cape = (g, y0, r0, h, col, hood = false) => { P(lathe([[r0 * 1.1, 0], [r0 * 1.05, h * 0.5], [r0 * 0.75, h * 0.9], [r0 * 0.45, h]], 24), col[0], g, 0, y0, -0.002, { scale: [1, 1, 0.92] });
    if (hood) P(S(0.0105, 12, 10, ), col[0], g, 0, y0 + h + 0.004, -0.0035, { scale: [1.05, 1.05, 1.0] }); };

  function piece(kind, type, col) {
    const g = new THREE.Group(), sz = { king: 1.38, queen: 1.26, bishop: 1.2, knight: 1.12, rook: 1.18, pawn: 0.86 }[type];
    const y0 = base(g, (type === "pawn" ? 0.0165 : 0.0205), col);
    const { legs, tail } = body(g, y0, sz, col, kind);
    const yHead = y0 + 0.041 * sz;
    let head;
    if (kind === "dog") {
      const breed = { pawn: "pug", bishop: "hound", king: "boxer", queen: "retriever", knight: "terrier", rook: "boxer" }[type];
      if (type === "bishop" || type === "king" || type === "queen") cape(g, y0 + 0.002, 0.0125 * sz, 0.032 * sz, col, false);
      head = dogHead(g, yHead, sz, col, breed);
      if (type === "bishop") { P(new THREE.CylinderGeometry(0.0035, 0.0035, 0.0012, 14), col[1], g, 0, y0 + 0.03 * sz, 0.0105 * sz, { rot: [Math.PI / 2, 0, 0], line: false }); }   // the medallion
    } else {
      if (type === "bishop") cape(g, y0 + 0.002, 0.0125 * sz, 0.03 * sz, col, true);
      if (type === "king" || type === "queen") cape(g, y0 + 0.002, 0.0125 * sz, 0.032 * sz, col, false);
      head = catHead(g, yHead, sz, col);
      if (type === "bishop") P(new THREE.CylinderGeometry(0.0035, 0.0035, 0.0012, 14), col[1], g, 0, y0 + 0.03 * sz, 0.0105 * sz, { rot: [Math.PI / 2, 0, 0], line: false });
    }
    const hd = head.hd;
    if (type === "king") crown(hd, 0.0078 * sz, 0.0058 * sz, col, 0.0065);
    if (type === "queen") crown(hd, 0.0076 * sz, 0.0042 * sz, col, 0.0038);
    if (type === "knight") P(new THREE.TorusGeometry(0.0072 * sz, 0.0018 * sz, 6, 16), kind === "dog" ? "#C0392B" : "#4F86C6", g, 0, y0 + 0.032 * sz, 0.001, { rot: [Math.PI / 2 - 0.2, 0, 0] });   // a scarf
    if (type === "rook") P(new THREE.TorusGeometry(0.0074 * sz, 0.0014 * sz, 6, 18), col[1], g, 0, y0 + 0.033 * sz, 0.001, { rot: [Math.PI / 2 - 0.15, 0, 0], line: false });            // a collar
    g.userData = { kind, type, head: hd, ears: head.ears, tail, paw: legs[-1], sz };
    scene.add(g); return g;
  }
  return { COLS, piece };
}
