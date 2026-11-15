/* tablero3d.js: the shop's "Tablero rompecabezas" as a toon prop, modelled from its photo (assets/p/tablero.webp): black
   and white squares in a grey frame with rounded corners, "tamaño reglamentario, se arma por partes y no trae piezas"
   (the site). The photo does not show where the parts join: the reel shows four quadrants of 4 × 4 squares and the four
   sides of the frame (the long sides carry the rounded corners). Sizes in metres (5 cm squares, a 3 cm frame: 46 cm).
   Local axes as the shop's other boards: file 0..7 = a..h along x, rank 0..7 = 1..8 along -z; sq() gives the centre of a
   square on the board's top. Each part is a Group placed at its home; animate part.g.position / rotation freely and
   put it back at part.home.
   Usage: const PB = puzzleBoard(scene, { wo }); PB.g.position.set(...); PB.parts.forEach((p) => ...); PB.sq(f, r) */
import * as THREE from "three";
import { toon, outline, shade } from "./toon3d.js";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";

export function puzzleBoard(scene, o = {}) {
  const WO = (o.wo ?? 0.0024) * 0.4, S = 0.05, F = 0.03, T = 0.012, FH = 0.016, HALF = S * 4;
  const LIGHT = "#F3F1EA", DARK = "#1F1F25", FRAME = "#A3A8AE", BASE = "#4A4D55";
  const g = new THREE.Group(); scene.add(g);
  const parts = [];
  // four quadrants of 4 × 4 squares; square (file, rank) is light when (file + rank) is odd (h1 light, as on a real board)
  for (const [qi, qj] of [[0, 0], [1, 0], [0, 1], [1, 1]]) {
    const p = new THREE.Group(); g.add(p);
    const slab = new THREE.Mesh(new RoundedBoxGeometry(HALF - 0.0008, T, HALF - 0.0008, 2, 0.0015), toon(BASE, { spec: 0.2 })); slab.position.y = T / 2; shade(slab); p.add(slab); outline(slab, WO * 1.2);
    const cv = document.createElement("canvas"); cv.width = cv.height = 256; const c = cv.getContext("2d"), q = 64;
    for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) { const file = qi * 4 + i, rank = (1 - qj) * 4 + (3 - j); c.fillStyle = (file + rank) % 2 === 1 ? LIGHT : DARK; c.fillRect(i * q, j * q, q, q);
      c.fillStyle = (file + rank) % 2 === 1 ? "rgba(255,255,255,0.5)" : "rgba(255,255,255,0.08)"; c.fillRect(i * q + 5, j * q + 5, q - 10, 3); }
    const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
    const top = new THREE.Mesh(new THREE.PlaneGeometry(HALF - 0.001, HALF - 0.001), toon("#ffffff", { map: tex, rim: 0, spec: 0.25 })); top.rotation.x = -Math.PI / 2; top.position.y = T + 0.0004; top.receiveShadow = true; p.add(top);
    const home = new THREE.Vector3((qi - 0.5) * HALF, 0, (qj - 0.5) * HALF); p.position.copy(home);
    parts.push({ g: p, home, kind: "quadrant", out: new THREE.Vector3(qi - 0.5, 0, qj - 0.5).normalize() });
  }
  // the frame: two long sides (rounded corners) along x, two short sides along z between them
  const W = HALF * 2 + F * 2;
  for (const s of [-1, 1]) {
    const p = new THREE.Group(); g.add(p);
    const m = new THREE.Mesh(new RoundedBoxGeometry(W, FH, F, 3, 0.008), toon(FRAME, { spec: 0.45 })); m.position.y = FH / 2; shade(m); p.add(m); outline(m, WO * 1.4);
    const home = new THREE.Vector3(0, 0, s * (HALF + F / 2)); p.position.copy(home); parts.push({ g: p, home, kind: "side", out: new THREE.Vector3(0, 0, s) });
  }
  for (const s of [-1, 1]) {
    const p = new THREE.Group(); g.add(p);
    const m = new THREE.Mesh(new RoundedBoxGeometry(F, FH, HALF * 2 - 0.001, 3, 0.004), toon(FRAME, { spec: 0.45 })); m.position.y = FH / 2; shade(m); p.add(m); outline(m, WO * 1.4);
    const home = new THREE.Vector3(s * (HALF + F / 2), 0, 0); p.position.copy(home); parts.push({ g: p, home, kind: "side", out: new THREE.Vector3(s, 0, 0) });
  }
  const sq = (file, rank) => g.localToWorld(new THREE.Vector3((file - 3.5) * S, T, (3.5 - rank) * S));
  return { g, parts, sq, S, T, F, FH, W, top: () => g.position.y + T };
}
