/* escena3d.js: the shared scene kit for Creaciones del Mago's 3D toon reels (skills/reel-3d-toon).
   Moved verbatim from the first reel (videos/papa-noel-en-ojotas/hf3d), where it passed the QA gate, so every reel
   starts from the same tested pieces: stage, the workshop set (with day/night/dawn light), the cast with its collision
   proxies and beard tracking, the printer, props and effects, arm IK with the contact guard, springs, voices and talk
   nods, subtitles (pills or kinetic words), the end card, the camera rig (framed shots, whip pans, snap zooms, shake,
   flash) and the common QA checks. A reel keeps only its timing, routes, actions, props timeline and shots.
   Every frame stays a pure function of t. */
import * as THREE from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { toon, outline, shade, Character, rotWorld, ikArm, simulateSprings, ss, seg, clamp, lerp, pulse, rnd, pushOut, colDist, minDistToMeshes } from "./toon3d.js";

export const V3 = (x, y, z) => new THREE.Vector3(x, y, z);
let scene = null, WO = 0.0024;

// ---------- stage ----------
export function stage(o = {}) {
  WO = o.wo ?? 0.0024;
  const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById("c"), antialias: true, preserveDrawingBuffer: true });
  renderer.setSize(1080, 1920, false); renderer.setPixelRatio(1);
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.toneMapping = THREE.NoToneMapping;
  scene = new THREE.Scene(); scene.background = new THREE.Color("#3a2a4a"); scene.fog = new THREE.FogExp2("#d9a874", 0.045);
  const camera = new THREE.PerspectiveCamera(36, 1080 / 1920, 0.05, 40);
  return { renderer, scene, camera, WO };
}

// ---------- helpers ----------
  export function canvasTex(w, h, draw) {
    const cv = document.createElement("canvas"); cv.width = w; cv.height = h; draw(cv.getContext("2d"), w, h);
    const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; return t;
  }
  export function rbox(w, h, d, c, x, y, z, parent, o = {}) {
    const m = new THREE.Mesh(new RoundedBoxGeometry(w, h, d, 2, Math.min(w, h, d) * (o.r ?? 0.12)), o.mat || toon(c, o.mo || {}));
    m.position.set(x, y, z); if (o.rot) m.rotation.set(...o.rot); shade(m); (parent || scene).add(m); if (o.line !== false) outline(m, (o.w ?? WO) / (o.s ?? 1)); return m;
  }
  export function cyl(r1, r2, h, c, x, y, z, parent, o = {}) {
    const m = new THREE.Mesh(new THREE.CylinderGeometry(r1, r2, h, o.seg || 16), toon(c, o.mo || {})); m.position.set(x, y, z);
    if (o.rot) m.rotation.set(...o.rot); shade(m); (parent || scene).add(m); if (o.line !== false) outline(m, (o.w ?? WO) / (o.s ?? 1)); return m;
  }
  export function sph(r, c, x, y, z, parent, o = {}) {
    const m = new THREE.Mesh(new THREE.SphereGeometry(r, o.seg || 16, o.seg ? o.seg / 2 : 10), o.basic ? new THREE.MeshBasicMaterial({ color: c, fog: false }) : toon(c, o.mo || {}));
    m.position.set(x, y, z); if (o.scale) m.scale.set(...o.scale); shade(m); (parent || scene).add(m); if (o.line) outline(m, (o.w ?? WO) / (o.s ?? 1)); return m;
  }

// ---------- the workshop set (metres): floor, walls, door on a hinge, window, shelves, bench, rug, tree, light ----------
// Big planes are tiled in ~0.5 m cells: a single huge quad seen at a steep angle lost depth/fog precision in the
// software renderer and drew the back wall over the bench for one frame ("Invisible no era", t = 17.617).
export function workshop(o = {}) {
  let beam = null;
    const planks = canvasTex(64, 64, (g, w, h) => { g.fillStyle = "#A0603A"; g.fillRect(0, 0, w, h); g.fillStyle = "#8A5638";
      for (let y = 0; y < h; y += 16) g.fillRect(0, y, w, 2); [[14, 0], [44, 16], [6, 32], [36, 48]].forEach(([x, y]) => g.fillRect(x, y, 2, 16));
      g.fillStyle = "#B0703F"; for (let y = 4; y < h; y += 16) g.fillRect(0, y, w, 1); g.fillStyle = "#94593A"; g.fillRect(20, 22, 10, 1); g.fillRect(48, 54, 8, 1); });
    planks.repeat.set(14, 14);
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(10, 10, 20, 20), toon("#ffffff", { map: planks, rim: 0 })); floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; scene.add(floor);
    const wallTex = () => { const t = canvasTex(64, 64, (g, w, h) => { g.fillStyle = "#E8A846"; g.fillRect(0, 0, w, h);
      for (let y = 0; y < h; y += 16) { g.fillStyle = "#F2C14E"; g.fillRect(0, y, w, 3); g.fillStyle = "#C98A2B"; g.fillRect(0, y + 14, w, 2); } }); return t; };
    const DOOR = { x0: 0.4, x1: 1.3, h: 1.55, z: -1.1 };
    function wall(x0, x1, y0, y1, z) { const t = wallTex(); t.repeat.set((x1 - x0) / 0.7, (y1 - y0) / 0.7);
      const m = new THREE.Mesh(new THREE.PlaneGeometry(x1 - x0, y1 - y0, Math.max(1, Math.ceil((x1 - x0) / 0.5)), Math.max(1, Math.ceil((y1 - y0) / 0.5))), toon("#ffffff", { map: t, rim: 0 })); m.position.set((x0 + x1) / 2, (y0 + y1) / 2, z); m.receiveShadow = true; scene.add(m); return m; }
    wall(-3, DOOR.x0, 0, 3, -1.1); wall(DOOR.x1, 3, 0, 3, -1.1); wall(DOOR.x0, DOOR.x1, DOOR.h, 3, -1.1);
    { const t = wallTex(); t.repeat.set(9, 4.3); const l = new THREE.Mesh(new THREE.PlaneGeometry(9, 3, 18, 6), toon("#ffffff", { map: t, rim: 0 })); l.rotation.y = Math.PI / 2; l.position.set(-1.45, 1.5, 3.4); l.receiveShadow = true; scene.add(l);
      const r = l.clone(); r.rotation.y = -Math.PI / 2; r.position.set(1.5, 1.5, 3.4); scene.add(r); }
    rbox(9, 0.08, 0.03, "#6E3B22", 0, 0.04, -1.09, null, { line: false });
    // door: frame, outside (bright summer yard), panel on a hinge with a wreath, light spilling in when open
    const yard = canvasTex(64, 96, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "#9CC9E8"); gr.addColorStop(0.55, "#E9F4F8"); gr.addColorStop(0.56, "#9BC46A"); gr.addColorStop(1, "#5C9A4A"); g.fillStyle = gr; g.fillRect(0, 0, w, h); g.fillStyle = "#FFF6D8"; g.beginPath(); g.arc(46, 16, 9, 0, 7); g.fill(); });
    const outside = new THREE.Mesh(new THREE.PlaneGeometry(1.4, 2.2), new THREE.MeshBasicMaterial({ map: yard, fog: false })); outside.position.set(0.85, 1.0, -2.75); outside.scale.set(2.0, 1.4, 1); scene.add(outside);
    for (const [w, h, x, y] of [[0.07, 1.6, DOOR.x0 - 0.02, 0.8], [0.07, 1.6, DOOR.x1 + 0.02, 0.8], [1.04, 0.08, 0.85, 1.57]]) rbox(w, h, 0.07, "#6E3B22", x, y, -1.08);
    const hinge = new THREE.Group(); hinge.position.set(DOOR.x1 - 0.005, 0, -1.08); scene.add(hinge);   // hinge on the right: opens against the side wall
    const doorTex = canvasTex(32, 64, (g, w, h) => { g.fillStyle = "#8A5638"; g.fillRect(0, 0, w, h); g.fillStyle = "#6E3B22"; for (let x = 0; x < w; x += 8) g.fillRect(x, 0, 1, h); g.fillStyle = "#A0603A"; g.fillRect(3, 6, 1, 20); g.fillRect(19, 30, 1, 22); });
    rbox(0.88, 1.52, 0.05, "#ffffff", -0.445, 0.765, 0, hinge, { mo: { map: doorTex } });
    rbox(0.84, 0.06, 0.03, "#6E3B22", -0.445, 1.24, 0.035, hinge); rbox(0.84, 0.06, 0.03, "#6E3B22", -0.445, 0.3, 0.035, hinge);
    sph(0.028, "#F2C14E", -0.8, 0.78, 0.05, hinge, { mo: { spec: 0.4 }, line: true });
    const wreath = new THREE.Mesh(new THREE.TorusGeometry(0.1, 0.035, 8, 20), toon("#2F5A32")); wreath.position.set(-0.445, 1.1, 0.06); shade(wreath); hinge.add(wreath); outline(wreath, WO);
    rbox(0.07, 0.05, 0.03, "#C0392B", -0.445, 1.0, 0.09, hinge, { line: false });
    const spillTex = canvasTex(32, 32, (g) => { const gr = g.createRadialGradient(16, 8, 1, 16, 14, 18); gr.addColorStop(0, "rgba(255,236,190,0.9)"); gr.addColorStop(1, "rgba(255,236,190,0)"); g.fillStyle = gr; g.fillRect(0, 0, 32, 32); });
    const spill = new THREE.Mesh(new THREE.PlaneGeometry(0.9, 1.3), new THREE.MeshBasicMaterial({ map: spillTex, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, fog: false }));
    spill.rotation.x = -Math.PI / 2; spill.position.set(0.82, 0.004, -0.5); scene.add(spill);
    // window, garland, light shaft and dust
    const sky = canvasTex(128, 96, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "#7FB6E0"); gr.addColorStop(1, "#BFE0F2"); g.fillStyle = gr; g.fillRect(0, 0, w, h);
      g.fillStyle = "#FFF6D8"; g.beginPath(); g.arc(30, 26, 12, 0, 7); g.fill();
      [["#5C9A4A", 96, 44, 26], ["#2F5A32", 110, 64, 20], ["#9BC46A", 84, 30, 14], ["#5C9A4A", 120, 30, 16]].forEach(([c, x, y, r]) => { g.fillStyle = c; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); }); });
    sky.wrapS = sky.wrapT = THREE.ClampToEdgeWrapping;
    const WIN = V3(-0.28, 1.32, -1.095);
    const glass = new THREE.Mesh(new THREE.PlaneGeometry(0.72, 0.56), new THREE.MeshBasicMaterial({ map: sky, fog: false })); glass.position.copy(WIN); scene.add(glass);
    for (const [w, h, x, y] of [[0.82, 0.06, 0, 0.31], [0.82, 0.06, 0, -0.31], [0.06, 0.68, -0.38, 0], [0.06, 0.68, 0.38, 0], [0.035, 0.56, 0, 0], [0.72, 0.035, 0, 0]]) rbox(w, h, 0.05, "#8A5638", WIN.x + x, WIN.y + y, -1.075);
    for (let k = 0; k < 12; k++) { const b = new THREE.Mesh(new THREE.IcosahedronGeometry(0.034, 0), toon(k % 2 ? "#2F5A32" : "#5C9A4A")); b.position.set(WIN.x - 0.44 + k * 0.08, WIN.y + 0.4 - Math.sin(k / 11 * Math.PI) * 0.06, -1.07); shade(b); scene.add(b); }
    for (let k = 0; k < 3; k++) sph(0.022, ["#C0392B", "#F2C14E", "#C0392B"][k], WIN.x - 0.3 + k * 0.3, WIN.y + 0.36 - Math.sin((k + 0.6) / 3 * Math.PI) * 0.05, -1.05, null, { mo: { spec: 0.3 } });
    const beamTex = canvasTex(4, 64, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "rgba(255,240,200,0.9)"); gr.addColorStop(1, "rgba(255,240,200,0)"); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
    beamTex.wrapS = beamTex.wrapT = THREE.ClampToEdgeWrapping;
    { const bg = new THREE.BufferGeometry();
      bg.setAttribute("position", new THREE.Float32BufferAttribute([WIN.x - 0.36, WIN.y + 0.28, -1.09, WIN.x + 0.36, WIN.y + 0.28, -1.09, 0.45, 0.01, 0.3, -0.45, 0.01, 0.3], 3));
      bg.setAttribute("uv", new THREE.Float32BufferAttribute([0, 0, 1, 0, 1, 1, 0, 1], 2)); bg.setIndex([0, 1, 2, 0, 2, 3]);
      beam = new THREE.Mesh(bg, new THREE.MeshBasicMaterial({ map: beamTex, transparent: true, opacity: 0.07, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide, fog: false })); scene.add(beam); }
    const NM = 40, mpos = new Float32Array(NM * 3), motes = new THREE.Points(new THREE.BufferGeometry(), new THREE.PointsMaterial({ color: "#FFF3B0", size: 4, sizeAttenuation: false, transparent: true, opacity: 0.7, fog: false }));
    motes.geometry.setAttribute("position", new THREE.BufferAttribute(mpos, 3)); scene.add(motes);
    // rug, bench, shelves with prints, spools, thermos, mandarins
    const rugTex = canvasTex(128, 128, (g) => { for (let r = 64; r > 0; r -= 8) { g.fillStyle = (r / 8) % 2 ? "#D7B98A" : "#B08A5A"; g.beginPath(); g.arc(64, 64, r, 0, 7); g.fill(); } });
    const rug = new THREE.Mesh(new THREE.CircleGeometry(0.62, 40), toon("#ffffff", { map: rugTex, rim: 0 })); rug.rotation.x = -Math.PI / 2; rug.position.set(-0.05, 0.004, 0.0); rug.receiveShadow = true; scene.add(rug);
    const bench = new THREE.Group(); bench.position.set(-0.62, 0, -0.84); scene.add(bench);
    rbox(1.27, 0.055, 0.47, "#B08A5A", 0, 0.55, 0, bench); rbox(1.2, 0.03, 0.4, "#8A5638", 0, 0.16, 0, bench);
    for (const [x, z] of [[-0.58, -0.18], [0.58, -0.18], [-0.58, 0.18], [0.58, 0.18]]) rbox(0.055, 0.53, 0.055, "#8A5638", x, 0.265, z, bench);
    for (const y of [0.98, 1.24]) {
      rbox(0.72, 0.03, 0.16, "#8A5638", -0.98, y, -1.02);
      [["#C0392B", -1.22, "c"], ["#4F86C6", -1.0, "k"], ["#5C9A4A", -0.78, "c"]].forEach(([c, x, k]) => {
        const g = k === "k" ? new THREE.ConeGeometry(0.045, 0.12, 8) : new THREE.CylinderGeometry(0.04, 0.045, 0.1, 12);
        const m = new THREE.Mesh(g, toon(c, { spec: 0.2 })); m.position.set(x, y + 0.07, -1.0); shade(m); scene.add(m); outline(m, WO); });
    }
    [["#C0392B", -1.15], ["#2B4C7E", -1.0], ["#F2C14E", -0.85]].forEach(([c, x]) => cyl(0.06, 0.06, 0.07, c, x, 0.65, -0.99, null, { rot: [Math.PI / 2, 0, 0] }));
    cyl(0.045, 0.045, 0.2, "#2B4C7E", -1.15, 0.68, -0.72); cyl(0.03, 0.035, 0.04, "#2E2160", -1.15, 0.8, -0.72);           // thermos (mate water)
    cyl(0.075, 0.055, 0.04, "#E9D8B4", -0.95, 0.6, -0.65); [[-0.97, -0.66], [-0.93, -0.64], [-0.95, -0.68]].forEach(([x, z], i) => sph(0.026, "#E86A4A", x, 0.635 + (i === 2 ? 0.02 : 0), z, null, { line: true }));
    // stool for Santa (height set from his sitting pose below), sack, tree (foreground), printer
    const S = o.S || V3(0.42, 0, -0.38), K = o.K || V3(0.97, 0, -0.16);
    const stool = new THREE.Group(); stool.position.copy(S); scene.add(stool);
    const tree = new THREE.Group(); tree.position.set(1.12, 0, 0.65); scene.add(tree);
    rbox(0.18, 0.15, 0.18, "#C0392B", 0, 0.075, 0, tree);
    [[0.3, 0.38, 0.33], [0.23, 0.32, 0.56], [0.16, 0.27, 0.77]].forEach(([r, h, y]) => { const c = new THREE.Mesh(new THREE.ConeGeometry(r, h, 10), toon("#2F5A32")); c.position.y = y; shade(c); tree.add(c); outline(c, WO); });
    sph(0.05, "#FFF3B0", 0, 0.94, 0, tree, { basic: true });
    const bulbs = []; for (let k = 0; k < 12; k++) { const a = k * 2.3, y = 0.24 + k * 0.05, r = 0.27 - k * 0.018; bulbs.push(sph(0.02, "#E86A4A", Math.cos(a) * r, y, Math.sin(a) * r, tree, { basic: true, seg: 8 })); }

    // light: warm sun through the window (hot summer), warm sky fill, soft front fill
    const sun = new THREE.DirectionalLight("#FFE0A0", 2.3); sun.position.set(0.2, 3.2, -2.6); sun.target.position.set(0.1, 0, 0.3);
    sun.castShadow = true; sun.shadow.mapSize.set(1536, 1536); Object.assign(sun.shadow.camera, { left: -2.2, right: 2.2, top: 2.2, bottom: -2.2, near: 0.5, far: 9 });
    sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.02; scene.add(sun, sun.target);
    const hemi = new THREE.HemisphereLight("#FFE9CC", "#5A4650", 1.0); scene.add(hemi);
    const front = new THREE.DirectionalLight("#FFF1DC", 0.75); front.position.set(1.0, 1.8, 3.2); scene.add(front);
  // light presets (day = the first reel's look). night: moonlight through the window, cool fill, a warm desk lamp pool
  // and the printer's LED glow; dawn: low warm pink sun. light(t-free) mixing: setLight(a, b, f) blends two presets.
  const nightSky = canvasTex(128, 96, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "#141A3E"); gr.addColorStop(1, "#2B3570"); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    g.fillStyle = "#F4F1D8"; g.beginPath(); g.arc(34, 26, 11, 0, 7); g.fill(); g.fillStyle = "#2B3570"; g.beginPath(); g.arc(39, 23, 9, 0, 7); g.fill();
    g.fillStyle = "#FFFFFF"; [[70, 12], [96, 30], [110, 14], [58, 50], [88, 60], [120, 46], [16, 60], [76, 80]].forEach(([x, y], i) => g.fillRect(x, y, i % 3 ? 1 : 2, i % 3 ? 1 : 2));
    [["#1E3A2A", 96, 70, 26], ["#13261C", 112, 84, 20], ["#24452F", 84, 60, 14]].forEach(([c, x, y, r]) => { g.fillStyle = c; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); }); });
  nightSky.wrapS = nightSky.wrapT = THREE.ClampToEdgeWrapping;
  const glassN = new THREE.Mesh(new THREE.PlaneGeometry(0.72, 0.56), new THREE.MeshBasicMaterial({ map: nightSky, fog: false, transparent: true, opacity: 0 })); glassN.position.copy(WIN).add(V3(0, 0, 0.001)); scene.add(glassN);
  const lamp = new THREE.PointLight("#FFC27A", 0, 2.2, 1.6); lamp.position.set(-1.05, 1.05, -0.62); scene.add(lamp);
  const led = new THREE.PointLight("#7FD3FF", 0, 1.2, 1.8); led.position.set(-0.36, 0.8, -0.66); scene.add(led);
  const PRESET = {
    day: { sun: ["#FFE0A0", 2.3], hemi: ["#FFE9CC", "#5A4650", 1.0], front: ["#FFF1DC", 0.75], fog: "#d9a874", bg: "#3a2a4a", night: 0, lamp: 0, led: 0, beam: ["#FFF0C8", 0.07], motes: "#FFF3B0" },
    night: { sun: ["#8FA6FF", 0.7], hemi: ["#4E5C9E", "#1C1530", 0.45], front: ["#9FB0F0", 0.2], fog: "#2A2B55", bg: "#120E2A", night: 1, lamp: 0.8, led: 0.6, beam: ["#AFC4FF", 0.09], motes: "#CFE0FF" },
    dawn: { sun: ["#FFB98A", 1.9], hemi: ["#FFD7C2", "#4A3650", 0.9], front: ["#FFE2D0", 0.6], fog: "#E0A58A", bg: "#3A2A4A", night: 0, lamp: 0.4, led: 0, beam: ["#FFD2B0", 0.08], motes: "#FFE3C8" },
  };
  const _a = new THREE.Color(), _b = new THREE.Color();
  const mixC = (target, ca, cb, f) => target.copy(_a.set(ca)).lerp(_b.set(cb), f);
  function setLight(pa, pb = pa, f = 0) { const A = PRESET[pa], B = PRESET[pb];
    mixC(sun.color, A.sun[0], B.sun[0], f); sun.intensity = lerp(A.sun[1], B.sun[1], f);
    mixC(hemi.color, A.hemi[0], B.hemi[0], f); mixC(hemi.groundColor, A.hemi[1], B.hemi[1], f); hemi.intensity = lerp(A.hemi[2], B.hemi[2], f);
    mixC(front.color, A.front[0], B.front[0], f); front.intensity = lerp(A.front[1], B.front[1], f);
    mixC(scene.fog.color, A.fog, B.fog, f); mixC(scene.background, A.bg, B.bg, f);
    glassN.material.opacity = lerp(A.night, B.night, f); glassN.visible = glassN.material.opacity > 0.001;
    lamp.intensity = lerp(A.lamp, B.lamp, f); led.intensity = lerp(A.led, B.led, f);
    if (beam) { mixC(beam.material.color, A.beam[0], B.beam[0], f); beam.material.opacity = lerp(A.beam[1], B.beam[1], f); }
    mixC(motes.material.color, A.motes, B.motes, f); }
  return { planks, floor, DOOR, wall, hinge, spill, outside, yard, glass, glassN, sky, nightSky, WIN, beam, motes, mpos, NM, rug, bench, S, K, stool, tree, bulbs, sun, hemi, front, lamp, led, setLight, PRESET };
}

// ---------- the cast: El Mago and Papá Noel with collision proxies, beard tracking, blob shadows; the printer ----------
export async function cast() {
    const loader = new GLTFLoader();
    const [gm, gs, gp] = await Promise.all(["mago", "santa", "printer"].map((n) => loader.loadAsync("assets/" + n + ".glb")));
    const mago = new Character(gm, WO), santa = new Character(gs, WO);
    // collision proxies (RESEARCH_3D_CONTACT.md): bone-attached spheres and capsules covering head, face, beard, belly, robe
    [["head", "DEF-head", [0, 0.79, 0.005], null, 0.152], ["face", "DEF-head", [0, 0.765, 0.12], null, 0.078],
     ["beardTop", "DEF-spine.003", [0, 0.66, 0.125], null, 0.14], ["beardLow", "DEF-spine.002", [0, 0.6, 0.165], [0, 0.38, 0.18], 0.1],
     ["moustL", "DEF-head", [0.05, 0.745, 0.15], null, 0.052], ["moustR", "DEF-head", [-0.05, 0.745, 0.15], null, 0.052],
     ["robeUp", "DEF-spine.003", [0, 0.42, 0], [0, 0.6, 0], 0.19], ["robeLow", "DEF-hips", [0, 0.13, 0], [0, 0.42, 0], 0.232],
     ["brim", "DEF-head", [0, 0.878, 0], null, 0.018, { normal: [0, 1, 0], R: 0.29 }], ["hatBase", "DEF-head", [0, 0.95, 0], null, 0.175],
     ["hatTip", "DEF-head", [0.01, 1.05, -0.05], [0.03, 1.12, -0.26], 0.075]].forEach((c) => mago.addCollider(...c));
    [["head", "DEF-head", [0, 0.85, 0.005], null, 0.166], ["face", "DEF-head", [0, 0.83, 0.12], null, 0.088],
     ["beardTop", "DEF-spine.003", [0, 0.72, 0.14], null, 0.14], ["beardLow", "DEF-spine.002", [0, 0.66, 0.2], [0, 0.54, 0.23], 0.085],
     ["moustL", "DEF-head", [0.05, 0.81, 0.165], null, 0.058], ["moustR", "DEF-head", [-0.05, 0.81, 0.165], null, 0.058],
     ["belly", "DEF-spine.001", [0, 0.49, 0.045], null, 0.255], ["chest", "DEF-spine.003", [0, 0.5, 0], [0, 0.68, 0], 0.235],
     ["hips", "DEF-hips", [0, 0.22, 0], [0, 0.4, 0], 0.255],
     ["hatBase", "DEF-head", [0, 1.0, 0], null, 0.185], ["hatTip", "DEF-head", [0.05, 1.12, -0.06], [0.22, 1.1, -0.12], 0.085],
     ["pompom", "DEF-head", [0.245, 1.035, -0.12], null, 0.062]].forEach((c) => santa.addCollider(...c));
    for (const sd of ["L", "R"]) { const P3 = (n) => { const v = new THREE.Vector3(); santa.b(n).getWorldPosition(v); return v.toArray(); };
      santa.addCollider("thigh" + sd, "DEF-thigh." + sd, P3("DEF-thigh." + sd), P3("DEF-shin." + sd), 0.12);
      santa.addCollider("shin" + sd, "DEF-shin." + sd, P3("DEF-shin." + sd), P3("DEF-foot." + sd), 0.065);
      santa.addCollider("foot" + sd, "DEF-foot." + sd, P3("DEF-foot." + sd), P3("DEF-toe." + sd), 0.06); }
    santa.addCollider("knot", "DEF-hips", [0.07, 0.392, 0.27], [0.06, 0.21, 0.29], 0.07);     // the tied jacket's knot and hanging sleeves
    // arms (upper arm and forearm capsules, from the bind pose): props and the other character keep out of them
    for (const [c, r] of [[mago, 0.064], [santa, 0.082]]) for (const sd of ["L", "R"]) {
      const P3 = (n) => { const v = new THREE.Vector3(); c.b(n).getWorldPosition(v); return v.toArray(); };
      c.addCollider("upper" + sd, "DEF-upper_arm." + sd, P3("DEF-upper_arm." + sd), P3("DEF-forearm." + sd), r, null, sd);
      c.addCollider("fore" + sd, "DEF-forearm." + sd, P3("DEF-forearm." + sd), P3("DEF-hand." + sd), r * 0.9, null, sd); }
    const ALLCOLS = () => [...mago.colliders(), ...santa.colliders()];
    function beardTrack(c) {           // beard vertices lying on the body (< 3 cm) paired with their nearest body vertex, its normal and the beard thickness above
      const beard = c.meshes.find((m) => m.name === "beard"), bodies = c.meshes.filter((m) => /^(robe|shirt|head|belt|jacket)$/.test(m.name)), out = [];
      c.W.updateMatrixWorld(true); const v = new THREE.Vector3(), nm = new THREE.Matrix3();
      const bp = bodies.map((m) => { const a = m.geometry.attributes.position, P = []; for (let j = 0; j < a.count; j++) P.push(v.fromBufferAttribute(a, j).clone().applyMatrix4(m.matrixWorld)); return P; });
      const ba = beard.geometry.attributes.position, BP = []; for (let i = 0; i < ba.count; i++) BP.push(v.fromBufferAttribute(ba, i).clone().applyMatrix4(beard.matrixWorld));
      for (let i = 0; i < ba.count; i++) { const p = v.fromBufferAttribute(ba, i).clone().applyMatrix4(beard.matrixWorld); let best = 1e9, bm = -1, bj = -1;
        bp.forEach((P, k) => P.forEach((q, j) => { const d = q.distanceToSquared(p); if (d < best) { best = d; bm = k; bj = j; } }));
        if (Math.sqrt(best) > 0.03) continue; const m = bodies[bm]; nm.getNormalMatrix(m.matrixWorld);
        const nl = new THREE.Vector3().fromBufferAttribute(m.geometry.attributes.normal, bj), nw = nl.clone().applyMatrix3(nm).normalize();
        let th = 0; for (const q of BP) { const w = q.clone().sub(p), a = w.dot(nw); if (a > th && w.lengthSq() - a * a < 0.015 * 0.015) th = a; }
        out.push({ i, m, j: bj, nl, d0: p.clone().sub(bp[bm][bj]).dot(nw), th }); }
      return { beard, pairs: out };
    }
    const BTRACK = [beardTrack(mago), beardTrack(santa)];
    scene.add(mago.W, santa.W);
    const blobTex = canvasTex(64, 64, (g) => { const gr = g.createRadialGradient(32, 32, 2, 32, 32, 32); gr.addColorStop(0, "rgba(42,22,54,0.55)"); gr.addColorStop(1, "rgba(42,22,54,0)"); g.fillStyle = gr; g.fillRect(0, 0, 64, 64); });
    const blob = (s) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(s, s), new THREE.MeshBasicMaterial({ map: blobTex, transparent: true, depthWrite: false })); m.rotation.x = -Math.PI / 2; scene.add(m); return m; };
    const blobM = blob(0.62), blobS = blob(0.78), blobK = blob(0.5);
    const printer = gp.scene; printer.scale.setScalar(0.085); printer.position.set(-0.42, 0.578, -0.84); printer.rotation.y = 0.3;
    const prM = []; printer.traverse((m) => { if (m.isMesh) prM.push(m); });
    prM.forEach((m) => { const e = m.material.emissive && m.material.emissive.getHex() !== 0;
      m.material = e ? new THREE.MeshBasicMaterial({ color: m.material.emissive }) : toon(m.material.color.clone()); shade(m); if (!e) outline(m, WO / 0.085); });
    scene.add(printer);
    const PR = {}; for (const n of ["head", "bed", "gantry", "print", "bow", "nozzle", "tube"]) PR[n] = printer.getObjectByName(n);
    const PRrest = {}; for (const n in PR) if (PR[n]) PRrest[n] = PR[n].position.clone();
    if (PR.tube) PR.tube.visible = false; if (PR.print) PR.print.visible = false; if (PR.bow) PR.bow.visible = false;
    const nozzleMat = PR.nozzle && PR.nozzle.isMesh ? PR.nozzle.material : null;
    const PRINT_OUT = V3(-0.42, 0.72, -0.8);
  return { mago, santa, gp, ALLCOLS, beardTrack, BTRACK, blob, blobTex, blobM, blobS, blobK, printer, prM, PR, PRrest, nozzleMat, PRINT_OUT };
}

// ---------- props: mate, sack, gifts; effects ----------
  export function makeMate() { const g = new THREE.Group();
    const pts = [[0.001, 0], [0.03, 0.004], [0.043, 0.03], [0.04, 0.06], [0.03, 0.08], [0.033, 0.088], [0.001, 0.09]].map(([r, y]) => new THREE.Vector2(r, y));
    const gourd = new THREE.Mesh(new THREE.LatheGeometry(pts, 16), toon("#8A5638", { spec: 0.15 })); shade(gourd); g.add(gourd); outline(gourd, WO);
    const rim = new THREE.Mesh(new THREE.TorusGeometry(0.031, 0.006, 6, 16), toon("#D8D4C8", { spec: 0.5 })); rim.rotation.x = Math.PI / 2; rim.position.y = 0.086; g.add(rim);
    const bomb = new THREE.Mesh(new THREE.CylinderGeometry(0.004, 0.004, 0.11, 6), toon("#D8D4C8", { spec: 0.5 })); bomb.position.set(0.012, 0.12, 0); bomb.rotation.z = -0.25; g.add(bomb);
    const herb = new THREE.Mesh(new THREE.CircleGeometry(0.028, 12), toon("#5C9A4A")); herb.rotation.x = -Math.PI / 2; herb.position.y = 0.085; g.add(herb);
    scene.add(g); return g; }
export function makeSack() {
    const sack = new THREE.Group(); scene.add(sack);
    { const pts = [[0.001, 0], [0.12, 0.01], [0.165, 0.08], [0.17, 0.17], [0.14, 0.26], [0.07, 0.31], [0.04, 0.33], [0.06, 0.37], [0.075, 0.4], [0.001, 0.41]].map(([r, y]) => new THREE.Vector2(r, y));
      const g = new THREE.LatheGeometry(pts, 22); const p = g.attributes.position;
      for (let i = 0; i < p.count; i++) { const x = p.getX(i), y = p.getY(i), z = p.getZ(i), a = Math.atan2(z, x), f = 1 + 0.06 * Math.sin(3 * a + y * 14) + 0.03 * Math.sin(7 * a); p.setXYZ(i, x * f, y, z * f); }
      g.computeVertexNormals(); const m = new THREE.Mesh(g, toon("#C0392B", { spec: 0.08 })); shade(m); sack.add(m); outline(m, WO);
      const rope = new THREE.Mesh(new THREE.TorusGeometry(0.05, 0.012, 6, 16), toon("#F2C14E", { spec: 0.3 })); rope.rotation.x = Math.PI / 2; rope.position.y = 0.335; sack.add(rope); }
  return sack;
}
  export function gift(kind) {
    const g = new THREE.Group(), C = (c) => toon(c, { spec: 0.25 }), add = (geo, c, x = 0, y = 0, z = 0, rot) => { const m = new THREE.Mesh(geo, C(c)); m.position.set(x, y, z); if (rot) m.rotation.set(...rot); shade(m); g.add(m); outline(m, WO * 0.8); return m; };
    const B = (w, h, d) => new RoundedBoxGeometry(w, h, d, 2, Math.min(w, h, d) * 0.15);
    switch (kind) {
      case "cafe": add(new THREE.CylinderGeometry(0.03, 0.025, 0.05, 14), "#FBF4E4", 0, 0.025); add(new THREE.TorusGeometry(0.014, 0.005, 6, 10), "#FBF4E4", 0.032, 0.026); add(new THREE.CircleGeometry(0.026, 12), "#5A3424", 0, 0.051, 0, [-Math.PI / 2, 0, 0]); break;
      case "banana": { const c = new THREE.CatmullRomCurve3([V3(-0.05, 0.03, 0), V3(-0.015, 0.008, 0), V3(0.02, 0.012, 0), V3(0.05, 0.04, 0)]); add(new THREE.TubeGeometry(c, 10, 0.014, 8), "#F2C14E"); break; }
      case "suculenta": add(new THREE.CylinderGeometry(0.03, 0.022, 0.035, 12), "#D9826A", 0, 0.017); for (let k = 0; k < 6; k++) add(new THREE.ConeGeometry(0.011, 0.04, 6), "#5C9A4A", Math.cos(k) * 0.012, 0.05, Math.sin(k) * 0.012, [Math.cos(k) * 0.5, 0, Math.sin(k) * 0.5]); break;
      case "hamster": add(new THREE.SphereGeometry(0.035, 14, 10), "#E1AE73", 0, 0.03).scale.set(1.2, 0.85, 1); add(new THREE.SphereGeometry(0.01, 8, 6), "#D9826A", -0.018, 0.06, 0.01); add(new THREE.SphereGeometry(0.01, 8, 6), "#D9826A", 0.018, 0.06, 0.01); break;
      case "creeper": add(B(0.07, 0.11, 0.07), "#5C9A4A", 0, 0.055); add(B(0.016, 0.016, 0.004), "#1E3A2A", -0.016, 0.085, 0.036); add(B(0.016, 0.016, 0.004), "#1E3A2A", 0.016, 0.085, 0.036); add(B(0.014, 0.028, 0.004), "#1E3A2A", 0, 0.062, 0.036); break;
      case "pokebox": add(B(0.075, 0.105, 0.025), "#D8D4C8", 0, 0.052); add(B(0.05, 0.036, 0.004), "#2F5A32", 0, 0.072, 0.013); add(new THREE.CylinderGeometry(0.008, 0.008, 0.006, 10), "#C0392B", 0.018, 0.034, 0.014, [Math.PI / 2, 0, 0]); break;
      case "dragon": add(new THREE.SphereGeometry(0.035, 12, 8), "#2F5A32", 0, 0.035).scale.set(1.3, 0.9, 0.9); add(new THREE.SphereGeometry(0.02, 10, 8), "#5C9A4A", 0.045, 0.06); add(new THREE.ConeGeometry(0.03, 0.05, 3), "#9BC46A", -0.01, 0.07, -0.02, [0.6, 0, 0.3]); add(new THREE.ConeGeometry(0.012, 0.05, 6), "#2F5A32", -0.055, 0.03, 0, [0, 0, 1.4]); break;
      case "f40": add(B(0.11, 0.028, 0.05), "#C0392B", 0, 0.024); add(B(0.05, 0.022, 0.04), "#C0392B", -0.01, 0.046); for (const [x, z] of [[-0.035, 0.026], [0.035, 0.026], [-0.035, -0.026], [0.035, -0.026]]) add(new THREE.CylinderGeometry(0.013, 0.013, 0.01, 10), "#2E2160", x, 0.013, z, [Math.PI / 2, 0, 0]); break;
      case "garaje": add(B(0.09, 0.06, 0.07), "#E9D8B4", 0, 0.03); add(B(0.1, 0.012, 0.08), "#C0392B", 0, 0.066); add(B(0.05, 0.04, 0.004), "#4F86C6", 0, 0.025, 0.036); break;
      case "plegable": add(B(0.1, 0.018, 0.1), "#5A3424", 0, 0.009); for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) if ((i + j) % 2) add(new THREE.PlaneGeometry(0.02, 0.02), "#FBF4E4", -0.03 + i * 0.02, 0.0185, -0.03 + j * 0.02, [-Math.PI / 2, 0, 0]); break;
      case "hoja": add(new THREE.SphereGeometry(0.05, 14, 8), "#9BC46A", 0, 0.012).scale.set(1, 0.25, 0.6); add(B(0.08, 0.004, 0.006), "#5C9A4A", 0, 0.026); break;
      case "penarol": add(new THREE.CylinderGeometry(0.05, 0.055, 0.035, 16, 1, true), "#F2C14E", 0, 0.018); add(new THREE.TorusGeometry(0.052, 0.006, 6, 16), "#150A34", 0, 0.033, 0, [Math.PI / 2, 0, 0]); add(new THREE.CircleGeometry(0.048, 16), "#5C9A4A", 0, 0.006, 0, [-Math.PI / 2, 0, 0]); break;
      case "nacional": add(new THREE.CylinderGeometry(0.05, 0.055, 0.035, 16, 1, true), "#FBF4E4", 0, 0.018); add(new THREE.TorusGeometry(0.052, 0.006, 6, 16), "#2B4C7E", 0, 0.033, 0, [Math.PI / 2, 0, 0]); add(new THREE.TorusGeometry(0.054, 0.004, 6, 16), "#C0392B", 0, 0.02, 0, [Math.PI / 2, 0, 0]); add(new THREE.CircleGeometry(0.048, 16), "#5C9A4A", 0, 0.006, 0, [-Math.PI / 2, 0, 0]); break;
      case "tnt": add(B(0.085, 0.085, 0.085), "#C0392B", 0, 0.043); add(B(0.088, 0.03, 0.088), "#E9D8B4", 0, 0.045); add(new THREE.CylinderGeometry(0.004, 0.004, 0.04, 6), "#150A34", 0, 0.1); break;
    }
    g.visible = false; scene.add(g); return g;
  }
export function makeFX() {
    const sparkM = (c) => new THREE.MeshBasicMaterial({ color: c, fog: false });
    const SPK = Array.from({ length: 30 }, (_, i) => { const m = new THREE.Mesh(new THREE.OctahedronGeometry(i % 5 ? 0.011 : 0.018), sparkM(i % 3 ? "#F2C14E" : "#FFF3B0")); m.visible = false; scene.add(m); return m; });
    const CONF = Array.from({ length: 70 }, (_, i) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(0.025, 0.014), new THREE.MeshBasicMaterial({ color: ["#C0392B", "#F2C14E", "#4F86C6", "#5C9A4A", "#E86A4A", "#FBF4E4"][i % 6], side: THREE.DoubleSide, fog: false })); m.visible = false; scene.add(m); return m; });
    const SWEAT = Array.from({ length: 3 }, () => { const m = sph(0.014, "#9CC9E8", 0, 0, 0, null, { mo: { spec: 0.6 }, line: true }); m.scale.set(1, 1.4, 1); m.visible = false; return m; });
    const moth = new THREE.Group(); scene.add(moth); { sph(0.012, "#8A5638", 0, 0, 0, moth, { scale: [1, 1, 1.8] }); for (const s of [-1, 1]) { const w = new THREE.Mesh(new THREE.CircleGeometry(0.03, 8), new THREE.MeshBasicMaterial({ color: "#C8AE88", side: THREE.DoubleSide })); w.position.x = s * 0.025; w.name = "w" + s; moth.add(w); } } moth.visible = false;
    const bulb = new THREE.Group(); scene.add(bulb); sph(0.05, "#FFF3B0", 0, 0, 0, bulb, { basic: true }); cyl(0.022, 0.018, 0.035, "#8C8A92", 0, -0.055, 0, bulb); bulb.visible = false;
    const PUFF = Array.from({ length: 18 }, () => { const m = new THREE.Mesh(new THREE.SphereGeometry(0.05, 8, 6), new THREE.MeshBasicMaterial({ color: "#E9D8B4", transparent: true, depthWrite: false, fog: false })); m.visible = false; scene.add(m); return m; });
  return { sparkM, SPK, CONF, SWEAT, moth, bulb, PUFF };
}

// ---------- headings ----------
  export const unwrap = (a, ref) => { while (a - ref > Math.PI) a -= 2 * Math.PI; while (a - ref < -Math.PI) a += 2 * Math.PI; return a; };
  export const hd = (a, b) => Math.atan2(b.x - a.x, b.z - a.z);
  export const hTurn = (t, keys) => { keys = keys.slice().sort((a, b) => a[0] - b[0]); let h = keys[0][1]; for (let i = 1; i < keys.length; i++) { const [t0, h0] = keys[i - 1], [t1, h1] = keys[i]; if (t >= t0) h = lerp(h0, unwrap(h1, h0), seg(t, t0, t1)); } return h; };

// ---------- arm IK for two characters (queue, contact-safe reach, palm check, drinking pose) and the contact guard ----------
export function makeRig(chars) {
    function frame(c) { const h = c.W.rotation.y; return { fwd: V3(Math.sin(h), 0, Math.cos(h)), right: V3(-Math.cos(h), 0, Math.sin(h)), left: V3(Math.cos(h), 0, -Math.sin(h)), up: V3(0, 1, 0) }; }
    const wp = (bone, off) => { const p = new THREE.Vector3(); bone.getWorldPosition(p); return off ? p.add(off) : p; };
    const IKQ = [];                     // arm IK runs after both characters' bodies are posed (targets avoid both)
    function arm(c, side, target, w, poleOff, clear = 0.055) { if (w > 0.001) IKQ.push([c, side, target.clone(), w, poleOff, clear]); }
    function armNow(c, side, target, w, poleOff, clear, colsOverride) {
      // the hand travels from where the clip has it to the goal along a path kept outside every body (each frame);
      // after solving, the PALM (not the wrist) is checked and the target pushed again: arms never pass through anyone
      const other = chars.find((x) => x !== c), cols = colsOverride || [...other.colliders(), ...c.colliders(true)];
      const w0 = clamp(w, 0, 1), h0 = wp(c.b("DEF-hand." + side)); let tgt = pushOut(h0.lerp(target, ss(w0)), clear, cols); w = ss(Math.min(1, w0 * 1.6));   // eased takeover
      const F = frame(c), sh = wp(c.b("DEF-upper_arm." + side));
      let pole = sh.clone().add(F.up.clone().multiplyScalar(-0.35)).add(F.fwd.clone().multiplyScalar(-0.12)).add((side === "R" ? F.right : F.left).clone().multiplyScalar(0.25)).add(poleOff && poleOff.isVector3 ? poleOff : V3(0, 0, 0));
      // the bend plane starts as the clip's own (no elbow flip when a reach begins) and turns to the designed one
      { const el = wp(c.b("DEF-forearm." + side)), mid = sh.clone().lerp(wp(c.b("DEF-hand." + side)), 0.5), k = el.clone().sub(mid);
        if (k.lengthSq() > 1e-6) { const keep = el.clone().add(k.normalize().multiplyScalar(0.3)); pole = poleOff === "keep" ? keep : keep.lerp(pole, ss(w0)); } }
      const up = c.b("DEF-upper_arm." + side), fo = c.b("DEF-forearm." + side), ha = c.b("DEF-hand." + side), q0 = up.quaternion.clone(), q1 = fo.quaternion.clone();
      for (let it = 0; it < 3; it++) {
        up.quaternion.copy(q0); fo.quaternion.copy(q1); up.updateMatrixWorld(true);
        ikArm(up, fo, ha, tgt, pole, w);
        const hc = handC(c, side), hc2 = pushOut(hc, clear, cols);
        if (hc2.distanceToSquared(hc) < 1e-8) break;
        tgt = tgt.clone().add(hc2.sub(hc));
      }
    }
    const handC = (c, side) => { const h = wp(c.b("DEF-hand." + side)), f = wp(c.b("DEF-forearm." + side)); return h.clone().add(h.clone().sub(f).normalize().multiplyScalar(0.035)); };
    // drinking (research): the straw tip reaches the moustache line, the gourd stays in front of the beard with
    // clearance, the head leans in. Mate local geometry (scale 1.25): straw tip (0.032, 0.216, 0), gourd centre (0, 0.05, 0) r 0.054
    const TH = 0.75, DP = {};
    function drinkPose(c, upA, fwdB) {
      const F = frame(c), M = headPt(c, upA, fwdB);
      const ym = F.up.clone().multiplyScalar(Math.cos(TH)).sub(F.fwd.clone().multiplyScalar(Math.sin(TH)));
      const xm = F.fwd.clone().multiplyScalar(-Math.cos(TH)).sub(F.up.clone().multiplyScalar(Math.sin(TH)));
      const zm = xm.clone().cross(ym); const q = new THREE.Quaternion().setFromRotationMatrix(new THREE.Matrix4().makeBasis(xm, ym, zm));
      let base = M.clone().sub(xm.clone().multiplyScalar(0.032)).sub(ym.clone().multiplyScalar(0.216));
      const cen = base.clone().add(ym.clone().multiplyScalar(0.05)), cen2 = pushOut(cen, 0.064, c.colliders());
      base.add(cen2.clone().sub(cen));
      return { base, q, center: cen2, grip: cen2.clone().add(F.right.clone().multiplyScalar(0.072)).add(F.fwd.clone().multiplyScalar(0.01)) };
    }
    const towards = (P, X, k) => P.clone().add(V3(X.x - P.x, 0, X.z - P.z).normalize().multiplyScalar(k));
    const headPt = (c, up, fwd, side = 0) => { const F = frame(c); return wp(c.b("DEF-head")).add(F.up.clone().multiplyScalar(up)).add(F.fwd.clone().multiplyScalar(fwd)).add(F.right.clone().multiplyScalar(side)); };
  function solveArms(guardOrder = chars.slice().reverse()) {      // run the queued reaches, then the contact guard
    for (const job of IKQ) armNow(...job);
    // contact guard (every frame, after clips and IK): a hand about to enter a face, beard or hat, or the other
    // character, is bent back out to the surface with clearance. Clip-driven gestures can't pass through anyone.
    const FACE = /^(head|face|beard|brim|hat|moust)/;
    const steered = new Set(IKQ.filter((j) => j[3] >= 0.5).map((j) => chars.indexOf(j[0]) + j[1]));   // arms a reach already steers (its own palm check ran)
    for (const c of guardOrder) { const other = chars.find((x) => x !== c), cols = [...other.colliders(), ...c.colliders(true).filter((k) => FACE.test(k.name))];
      for (const side of ["L", "R"]) { if (steered.has(chars.indexOf(c) + side)) continue;
        const hc = handC(c, side), hc2 = pushOut(hc, 0.05, cols);
        if (hc2.distanceToSquared(hc) > 1e-8) armNow(c, side, wp(c.b("DEF-hand." + side)).add(hc2.sub(hc)), 1, "keep", 0.055, cols); } }
  }
  return { frame, wp, IKQ, arm, armNow, handC, TH, DP, drinkPose, towards, headPt, solveArms };
}

// ---------- voices: lines from the <audio data-who> clips, loudness envelopes, talk nods ----------
export async function voices(FPS) {
    const LINES = [...document.querySelectorAll("audio[data-who]")].map((a) => ({ id: a.id.slice(2), who: a.dataset.who, t0: +a.dataset.start, d: +a.dataset.duration, text: a.dataset.text, sub: a.dataset.sub !== "no" }));
    const ENV = await (await fetch("assets/voz/env.json")).json();
    function talk(c, who, t, F) { let e = 0;
      for (const L of LINES) if (L.who === who && t >= L.t0 && t < L.t0 + L.d) { const k = (t - L.t0) * FPS, a = ENV[L.id] || [], i = Math.floor(k), f = k - i; e = Math.max(e, lerp(a[i] || 0, a[i + 1] || 0, f)); }
      if (e <= 0) return; rotWorld(c.b("DEF-head"), F.left, 0.055 * e); rotWorld(c.b("DEF-head"), F.fwd, 0.02 * e * Math.sin(t * 5.3)); c.b("brows").position.y += 0.006 * e; }
  return { LINES, ENV, talk };
}

// ---------- secondary motion (simulated once): hats, beards, Santa's belly ----------
export function characterSprings(mago, santa, DUR, FPS, poseAt) {
    const N = DUR * FPS + 1, qW = (b) => { const q = new THREE.Quaternion(); b.getWorldQuaternion(q); return q; };
    const pt = (b, x, y, z) => () => { const p = V3(x, y, z); b.localToWorld(p); return p; };
    const SPR = simulateSprings(N, FPS, poseAt, [
      { ref: pt(mago.b("DEF-head"), 0, 0.35, 0), frame: () => qW(mago.b("DEF-head")), f: 2.3, z: 0.3, g: 0.06, lim: 0.5 },
      { ref: pt(mago.b("DEF-spine.003"), 0, 0.1, 0.2), frame: () => qW(mago.b("DEF-spine.003")), f: 2.6, z: 0.3, g: 0.035, lim: 0.25, minB: -0.02 },
      { ref: pt(santa.b("DEF-head"), 0, 0.35, 0), frame: () => qW(santa.b("DEF-head")), f: 1.9, z: 0.3, g: 0.045, lim: 0.32 },
      { ref: pt(santa.b("DEF-spine.003"), 0, 0.1, 0.25), frame: () => qW(santa.b("DEF-spine.003")), f: 2.4, z: 0.3, g: 0.035, lim: 0.25, minB: -0.02 },
      { ref: pt(santa.b("DEF-hips"), 0, 0.1, 0.2), frame: () => qW(santa.b("DEF-hips")), f: 1.9, z: 0.2, g: 0.025, lim: 0.12, gy: true },
    ]);
    const eu = new THREE.Euler(), qq = new THREE.Quaternion();
    const tilt = (b, x, z) => { if (!b) return; eu.set(z, 0, -x); b.quaternion.multiply(qq.setFromEuler(eu)); };
    function springs(t) {
      const f = clamp(Math.round(t * FPS), 0, N - 1), g = (k, i) => SPR[k][f * 2 + i];
      [0.35, 0.6, 0.9].forEach((k, i) => tilt(mago.b("hat." + (i + 1)), g(0, 0) * k, g(0, 1) * k));
      [0.5, 0.8].forEach((k, i) => tilt(mago.b("beard." + (i + 1)), g(1, 0) * k, g(1, 1) * k));
      [0.35, 0.65, 1.0].forEach((k, i) => tilt(santa.b("hat." + (i + 1)), g(2, 0) * k, g(2, 1) * k));
      [0.5, 0.8].forEach((k, i) => tilt(santa.b("beard." + (i + 1)), g(3, 0) * k, g(3, 1) * k));
      const bl = santa.b("belly"); if (bl) { const v = g(4, 1); bl.scale.set(1 + v * 0.8, 1 - v * 1.2, 1 + v * 0.8); }
    }
  return { N, SPR, springs, tilt };
}

// ---------- subtitles as pills (one per line, speaker colours) and the end card ----------
export function pillOverlay(LINES, T) {
    const subsEl = document.getElementById("subs"), cardEl = document.getElementById("card");
    LINES.forEach((L, k) => { if (!L.sub) return; const e = document.createElement("div"), w = document.createElement("span");
      e.className = "sub " + L.who; w.className = "who"; w.textContent = L.who === "santa" ? "PAPÁ NOEL" : "EL MAGO"; e.append(w, document.createTextNode(L.text)); subsEl.appendChild(e); L.el = e;
      const nx = LINES.slice(k + 1).find((x) => x.sub); L.end = Math.min(L.t0 + L.d + 0.3, nx ? nx.t0 - 0.03 : 99); });
    const backOut = (x) => 1 + 2.2 * Math.pow(x - 1, 3) + 1.2 * Math.pow(x - 1, 2);
    function overlay(t) {
      for (const L of LINES) if (L.el) { const a = clamp((t - L.t0 + 0.06) / 0.16, 0, 1), b = clamp((L.end - t) / 0.12, 0, 1), v = Math.min(a, b);
        L.el.style.opacity = v.toFixed(3); L.el.style.transform = `translateY(${((1 - a) * 30).toFixed(1)}px) scale(${(0.86 + 0.14 * backOut(a)).toFixed(3)})`; L.el.style.visibility = v > 0 ? "visible" : "hidden"; }
      const c = clamp((t - T.card) / 0.3, 0, 1); cardEl.style.opacity = Math.min(1, c * 1.6).toFixed(3);
      cardEl.style.transform = `translateY(${((1 - c) * 60).toFixed(1)}px) rotate(${(-1.5 + 0.6 * Math.sin(Math.max(0, t - T.card) * 2.2)).toFixed(2)}deg) scale(${(0.8 + 0.2 * backOut(c) + 0.012 * Math.sin(Math.max(0, t - T.card - 0.3) * 4)).toFixed(3)})`;
      cardEl.style.visibility = c > 0 ? "visible" : "hidden"; }
  return overlay;
}

// ---------- subtitles as kinetic words (word by word over the voiced span; the word being said in the speaker colour) ----------
// needs .kin / .w / .cur CSS (see papa-noel-en-ojotas/hf3d-v2/index.html) and an optional hook element
export function kineticOverlay({ LINES, ENV, FPS, T, subsEl, cardEl, hookEl = null, hook = [0.15, 2.3] }) {
  LINES.forEach((L, k) => { if (!L.sub) return; const e = document.createElement("div"); e.className = "kin " + L.who; subsEl.appendChild(e); L.el = e;
    const env = ENV[L.id] || []; let a = env.findIndex((v) => v > 0.18), b = env.length - 1 - [...env].reverse().findIndex((v) => v > 0.18); if (a < 0) { a = 0; b = env.length - 1; }
    const words = L.text.split(" "), wts = words.map((w) => w.replace(/[^A-Za-zÁÉÍÓÚáéíóúñÑ]/g, "").length + 1.5), tot = wts.reduce((x, y) => x + y, 0);
    let acc = a / FPS; L.words = words.map((w, j) => { const sp = document.createElement("span"); sp.className = "w"; sp.textContent = w; e.appendChild(sp); e.appendChild(document.createTextNode(" "));
      const t0 = L.t0 + acc; acc += (b - a) / FPS * wts[j] / tot; return { sp, t0 }; });
    const nx = LINES.slice(k + 1).find((x) => x.sub); L.end = Math.min(L.t0 + L.d + 0.35, nx ? nx.t0 - 0.03 : 99); });
  const backOut = (x) => 1 + 2.2 * Math.pow(x - 1, 3) + 1.2 * Math.pow(x - 1, 2);
  return function overlay(t) {
    for (const L of LINES) if (L.el) { const out = clamp((L.end - t) / 0.1, 0, 1), on = t >= L.words[0].t0 - 0.02 && out > 0;
      L.el.style.visibility = on ? "visible" : "hidden"; L.el.style.opacity = out.toFixed(3); if (!on) continue;
      L.words.forEach((w, j) => { const a = clamp((t - w.t0) / 0.1, 0, 1), cur = t >= w.t0 && (j === L.words.length - 1 ? t < L.t0 + L.d : t < L.words[j + 1].t0);
        w.sp.style.opacity = a > 0 ? "1" : "0"; w.sp.style.transform = `translateY(${((1 - a) * 18).toFixed(1)}px) scale(${((cur ? 1.12 : 1) * (0.7 + 0.3 * backOut(a))).toFixed(3)})`;
        w.sp.classList.toggle("cur", cur); }); }
    if (hookEl) { const h = Math.min(clamp((t - hook[0]) / 0.18, 0, 1), clamp((hook[1] - t) / 0.2, 0, 1)); hookEl.style.visibility = h > 0 ? "visible" : "hidden"; hookEl.style.opacity = h.toFixed(3);
      hookEl.style.transform = `rotate(${(-3 + 1.2 * Math.sin(t * 3)).toFixed(2)}deg) scale(${(0.6 + 0.4 * backOut(clamp((t - hook[0]) / 0.22, 0, 1))).toFixed(3)})`; }
    if (cardEl) { const c = clamp((t - T.card) / 0.3, 0, 1); cardEl.style.opacity = Math.min(1, c * 1.6).toFixed(3);
      cardEl.style.transform = `translateY(${((1 - c) * 60).toFixed(1)}px) rotate(${(-1.5 + 0.6 * Math.sin(Math.max(0, t - T.card) * 2.2)).toFixed(2)}deg) scale(${(0.8 + 0.2 * backOut(c) + 0.012 * Math.sin(Math.max(0, t - T.card - 0.3) * 4)).toFixed(3)})`;
      cardEl.style.visibility = c > 0 ? "visible" : "hidden"; } };
}

// ---------- camera rig: framed shots, whip pans, snap zooms, shake, flash (from the V2 edit) ----------
// shots: raw { t, d, fov, from, to, look, roll } or framed { t, d, fov, subj, h, az, el, v, track, roll, aim? } where subj
// names a character (its head, aimed 10 cm above the neck bone) or a key of `points` (fixed world points); whip: +1/-1
// on the shot a whip pan cuts INTO. Head heights are measured once from the poses (measure() after poseAt exists).
export function camRig({ camera, shots, chars, points = {}, poseAt, props = null, shake = [], punch = [], flash = [], canvasEl = null, flashEl = null, filter = "saturate(1.08) contrast(1.04)" }) {
  const WHIP = 0.1, WHIP_YAW = 0.85;
  function measure() { const hp = new THREE.Vector3();
    for (const s of shots) if (s.subj) { const P = V3(0, 0, 0), n = 5;
      for (let k = 0; k < n; k++) { const tt = s.t + s.d * (k + 0.5) / n; poseAt(tt); if (props) props(tt);
        if (points[s.subj]) hp.copy(typeof points[s.subj] === "function" ? points[s.subj]() : points[s.subj]); else { chars[s.subj].b("DEF-head").getWorldPosition(hp); hp.y += 0.1; } if (s.aim) hp.add(V3(...s.aim)); P.add(hp); }
      s.P = P.multiplyScalar(1 / n); if (s.track) { poseAt(s.t + s.d / 2); s.rx0 = chars[s.subj].W.position.x; s.rz0 = chars[s.subj].W.position.z; } } }
  function shotCam(s, t) {
    const f = ss(clamp((t - s.t) / s.d, 0, 1));
    if (s.fn) return s.fn(t, f);                       // custom shot (a POV, a shot tied to a moving prop): { p, l, fov, roll }
    if (!s.subj) return { p: V3(...s.from).lerp(V3(...s.to), f), l: s.look2 ? V3(...s.look).lerp(V3(...s.look2), f) : V3(...s.look), fov: s.fov, roll: s.roll || 0 };
    const P = s.P.clone(); if (s.track) { const r = chars[s.subj].W.position; P.x = r.x + (s.P.x - s.rx0); P.z = r.z + (s.P.z - s.rz0); }
    const D = s.h / 2 / Math.tan(THREE.MathUtils.degToRad(s.fov / 2)) * lerp(s.push ? s.push[0] : 1.05, s.push ? s.push[1] : 0.95, f), az = THREE.MathUtils.degToRad(s.az), el = THREE.MathUtils.degToRad(s.el);
    const dir = V3(Math.sin(az) * Math.cos(el), Math.sin(el), Math.cos(az) * Math.cos(el));
    return { p: P.clone().add(dir.multiplyScalar(D)), l: P.clone().sub(V3(0, s.v * s.h, 0)), fov: s.fov, roll: s.roll || 0 };
  }
  function at(t) {
    let i = 0; for (let k = 0; k < shots.length; k++) if (t >= shots[k].t) i = k;
    const s = shots[i], c = shotCam(s, t), nx = shots[i + 1]; let yaw = 0, blur = 0;
    if (nx && nx.whip && t > nx.t - WHIP) { const k = (t - (nx.t - WHIP)) / WHIP; yaw = nx.whip * WHIP_YAW * k * k; blur = 16 * k; }
    if (s.whip && t < s.t + WHIP * 1.2) { const k = (t - s.t) / (WHIP * 1.2); yaw = -s.whip * WHIP_YAW * (1 - k) * (1 - k); blur = 16 * (1 - k); }
    let fov = c.fov; for (const [t0, a] of punch) if (t0 >= s.t && t >= t0) fov *= 1 - a * ss(clamp((t - t0) / 0.09, 0, 1));
    const sh = V3(0, 0, 0); let sr = 0;
    for (const [t0, a, d] of shake) { const u = t - t0; if (u < 0 || u > d) continue; const e = a * Math.exp(-u * 7);
      sh.add(V3(Math.sin(u * 61.3) + 0.5 * Math.sin(u * 23.1), Math.sin(u * 47.9 + 1.3), Math.sin(u * 53.7 + 2.1)).multiplyScalar(e)); sr += 0.6 * e * Math.sin(u * 39.7); }
    camera.fov = fov; camera.updateProjectionMatrix(); camera.position.copy(c.p).add(sh);
    const dir = c.l.clone().sub(c.p).applyAxisAngle(V3(0, 1, 0), yaw); camera.lookAt(camera.position.clone().add(dir)); camera.rotateZ(c.roll + sr);
    if (canvasEl) canvasEl.style.filter = `${filter}${blur > 0.3 ? ` blur(${blur.toFixed(1)}px)` : ""}`;
    if (flashEl) { let fl = 0; for (const [t0, d, col] of flash) if (t >= t0 && t < t0 + d) { fl = Math.max(fl, 1 - (t - t0) / d); if (col) flashEl.style.background = col; } flashEl.style.opacity = (0.9 * fl).toFixed(3); }
  }
  const cuts = shots.slice(1).map((s) => s.t), whips = shots.filter((s) => s.whip).map((s) => s.t);
  return { measure, at, shotCam, cuts, whips };
}

// ---------- QA: the checks every reel shares (props are checked by the reel itself) ----------
// nan bones; hands vs the other character and vs own face/beard/hat; walls, door frame and door panel (all colliders,
// arms included, plus extra samples such as a sack); beards resting on the body; bodies vs bodies; joint positions for
// the pose-jump detector. chars: { name: Character } (two of them); DOOR, hinge from workshop(); BTRACK from cast().
export function qaBase({ chars, DOOR, hinge, BTRACK, rig, handR = { mago: 0.042, santa: 0.05 }, doorPanel = { c: [-0.445, 0.765, 0], half: [0.44, 0.76, 0.025] } }) {
  const names = Object.keys(chars), C = names.map((n) => chars[n]);
  const FACEM = /^(head|nose|mustache|beard|cheek|brim|cone|band|hatband|hatcone|lens|rim|bridge|brow|eye)/;
  return function base(out, extraSamples = []) {
    const bad = (q) => !(Number.isFinite(q.x) && Number.isFinite(q.y) && Number.isFinite(q.z) && Number.isFinite(q.w));
    for (const c of C) for (const b of c.all) if (bad(b.quaternion)) { out.push(["nan", b.name]); break; }
    for (const [i, c] of C.entries()) { const o = C[1 - i], rH = handR[names[i]] ?? 0.045; if (!c.W.visible) continue;
      for (const side of ["L", "R"]) { const hc = rig.handC(c, side);
        if (o.W.visible) { const r1 = minDistToMeshes(hc, o.meshes); if (r1.d < rH * 0.75) out.push(["hand-other", names[i], side, r1.mesh, +r1.d.toFixed(3)]); }
        const r2 = minDistToMeshes(hc, c.meshes.filter((m) => FACEM.test(m.name))); if (r2.d < rH * 0.75) out.push(["hand-own-face", names[i], side, r2.mesh, +r2.d.toFixed(3)]); } }
    const samples = []; for (const [i, c] of C.entries()) if (c.W.visible) for (const k of c.colliders()) { samples.push([names[i], k.name, k.a, k.r]); if (k.b) { samples.push([names[i], k.name, k.b, k.r]); samples.push([names[i], k.name, k.a.clone().lerp(k.b, 0.5), k.r]); } }
    samples.push(...extraSamples);
    const dq = new THREE.Quaternion(); hinge.getWorldQuaternion(dq); const dc = hinge.localToWorld(V3(...doorPanel.c)), axes = [V3(1, 0, 0), V3(0, 1, 0), V3(0, 0, 1)].map((x) => x.applyQuaternion(dq)), half = doorPanel.half;
    for (const [who, nm2, p, r] of samples) {
      if (Math.abs(p.z + 1.1) < r && !(p.x - r > DOOR.x0 + 0.035 && p.x + r < DOOR.x1 - 0.035 && p.y + r < DOOR.h)) out.push(["wall", who, nm2, +p.x.toFixed(2), +p.z.toFixed(2)]);
      const d = p.clone().sub(dc), loc = axes.map((ax, i) => clamp(d.dot(ax), -half[i], half[i])), q = dc.clone(); loc.forEach((v, i) => q.add(axes[i].clone().multiplyScalar(v)));
      if (q.distanceTo(p) < r - 0.005) out.push(["door", who, nm2, +(r - q.distanceTo(p)).toFixed(3)]); }
    for (const [k, B] of BTRACK.entries()) { const c = C[k]; if (!c || !c.W.visible) continue; let worst = 0, wm = null;
      const P = new THREE.Vector3(), Bq = new THREE.Vector3(), O = new THREE.Vector3();
      for (const pr of B.pairs) { B.beard.getVertexPosition(pr.i, P); P.applyMatrix4(B.beard.matrixWorld);
        pr.m.getVertexPosition(pr.j, Bq); Bq.applyMatrix4(pr.m.matrixWorld);
        O.fromBufferAttribute(pr.m.geometry.attributes.position, pr.j).addScaledVector(pr.nl, 0.02); pr.m.applyBoneTransform(pr.j, O); O.applyMatrix4(pr.m.matrixWorld);
        const n = O.sub(Bq).normalize(), d = P.sub(Bq).dot(n), sink = pr.d0 - d, over = sink - Math.max(0.012, pr.th - 0.008); if (d < -0.004 && over > worst) { worst = over; wm = pr.m.name; } }
      if (worst > 0) out.push(["beard-in-body", names[k], wm, +worst.toFixed(3)]); }
    if (C[0].W.visible && C[1].W.visible) for (const a of C[0].colliders()) for (const b of C[1].colliders()) { const q1 = a.b ? a.a.clone().lerp(a.b, 0.5) : a.a; if (colDist(q1, b).d < a.r - 0.02) out.push(["bodies", a.name, b.name]); }
    const J = {}; for (const [i, c] of C.entries()) for (const b of ["DEF-head", "DEF-hips", "DEF-hand.L", "DEF-hand.R", "DEF-forearm.L", "DEF-forearm.R"]) J[names[i][0] + b] = rig.wp(c.b(b)).toArray().map((v) => +v.toFixed(4));
    return J;
  };
}
