// Exports a reel's 3D scene to a GLB that Blender opens, with its whole animation baked (the owner, 22/11: "dame los
// assets de los reels para poderlos editar desde blender").
//   node exportar_glb.cjs PORT OUT.glb [FPS=30]      (serve the reel's hf3d folder over http first)
// What goes in: every mesh of the set, the props, the chess pieces, both characters (skinned, with their bones), and
// the camera. The procedural animation (clips + IK + springs + props) is sampled at FPS and written as one glTF
// animation: position / rotation / scale of every node that moves (a hidden node gets scale 0). The toon outlines (the
// inverted black shells) are left out. The camera's field of view per frame goes to OUT.camara.json (glTF cannot
// animate it). Text, subtitles, the end card and the photo gallery are page overlays: they are not 3D, so not here.
const { chromium } = require("playwright"); const fs = require("fs");
const [PORT, OUT, FPS0] = process.argv.slice(2); const FPS = +(FPS0 || 30);
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on("pageerror", (e) => console.log("page error:", e.message));
  await p.goto(`http://localhost:${PORT}/index.html`); await p.waitForFunction(() => window.__draw3d && window.__dbg, null, { timeout: 900000 });
  const r = await p.evaluate(async (FPS) => {
    const THREE = window.__dbg.THREE, cap = {};
    THREE.Scene.prototype.onBeforeRender = function (r, s, c) { cap.s = s; cap.c = c; };      // the renderer's render() lives on the instance: catch the scene and camera here
    window.__draw3d(0.0123); const scene = cap.s, cam = cap.c, D = window.__timelines.main.duration();
    // drop the outlines (BackSide basic shells), give every node a unique name, put the camera in the scene
    const drop = []; scene.traverse((o) => { if (o.isMesh && o.material && o.material.isMeshBasicMaterial && o.material.side === THREE.BackSide) drop.push(o); });
    drop.forEach((o) => o.parent.remove(o));
    if (cam.parent !== scene) scene.add(cam); cam.name = "Camara";
    const seen = new Map(); const nodes = [];
    scene.traverse((o) => { if (o === scene) return; let n = (o.name || (o.isBone ? "hueso" : o.type)).replace(/[.\s/]+/g, "_"); const k = seen.get(n) || 0; seen.set(n, k + 1); o.name = k ? `${n}_${k}` : n; nodes.push(o); });
    // sample: every node's local transform and visibility
    const N = Math.floor(D * FPS) + 1, rec = nodes.map(() => ({ p: [], q: [], s: [] })), fov = [];
    for (let i = 0; i < N; i++) {
      const t = Math.min(D - 1e-3, i / FPS + 1e-4); window.__draw3d(t); fov.push(+cam.fov.toFixed(3));
      nodes.forEach((o, j) => { const v = o.visible ? 1 : 0; rec[j].p.push(o.position.x, o.position.y, o.position.z); rec[j].q.push(o.quaternion.x, o.quaternion.y, o.quaternion.z, o.quaternion.w);
        rec[j].s.push(o.scale.x * v || 1e-4, o.scale.y * v || 1e-4, o.scale.z * v || 1e-4); }); }
    const times = Array.from({ length: N }, (_, i) => i / FPS), tracks = []; let moving = 0;
    const varies = (a, w) => { for (let i = w; i < a.length; i++) if (Math.abs(a[i] - a[i % w]) > 1e-5) return true; return false; };
    nodes.forEach((o, j) => { const R0 = rec[j]; let m = false;
      if (varies(R0.p, 3)) { tracks.push(new THREE.VectorKeyframeTrack(o.name + ".position", times, R0.p)); m = true; }
      if (varies(R0.q, 4)) { tracks.push(new THREE.QuaternionKeyframeTrack(o.name + ".quaternion", times, R0.q)); m = true; }
      if (varies(R0.s, 3)) { tracks.push(new THREE.VectorKeyframeTrack(o.name + ".scale", times, R0.s)); m = true; }
      if (m) moving++; });
    window.__draw3d(0.0124);                                              // leave the scene at its first frame
    const clip = new THREE.AnimationClip("reel", D, tracks);
    const { GLTFExporter } = await import("./lib/addons/exporters/GLTFExporter.js");
    const buf = await new GLTFExporter().parseAsync(scene, { binary: true, animations: [clip], onlyVisible: false, maxTextureSize: 2048 });
    let s = ""; const u = new Uint8Array(buf); for (let i = 0; i < u.length; i += 0x8000) s += String.fromCharCode.apply(null, u.subarray(i, i + 0x8000));
    return { b64: btoa(s), fov, D, N, nodes: nodes.length, moving, fps: FPS };
  }, FPS);
  fs.writeFileSync(OUT, Buffer.from(r.b64, "base64"));
  fs.writeFileSync(OUT.replace(/\.glb$/, ".camara.json"), JSON.stringify({ fps: r.fps, duration: r.D, sensor_height_mm: 36, fov_vertical_deg: r.fov }));
  console.log(`${OUT}: ${r.nodes} nodes, ${r.moving} animated, ${r.N} frames at ${r.fps} fps, ${(fs.statSync(OUT).size / 1e6).toFixed(1)} MB`);
  await b.close();
})();
