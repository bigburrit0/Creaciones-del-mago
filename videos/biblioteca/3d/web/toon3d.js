/* toon3d.js: shared helpers for 3D toon reels rendered frame by frame in HyperFrames (three.js r170).
   Research: videos/RESEARCH_3D_TOON.md, videos/RESEARCH_3D_FORMS.md.
   - toon(): 3-band gradient tinted (purple shadows, warm light), Fresnel rim, baked AO from vertex colours (tinted),
     optional hard toon specular.
   - outline(): inverted hull on smoothed normals (no spikes), works on skinned meshes.
   - Character: wraps a GLB from biblioteca/3d (mago.glb, santa.glb): toon materials, bones by name, a clip scheduler
     with crossfades (every pose is a pure function of t), world-space bone rotation, two-bone arm IK.
   - simulateSprings(): hat/beard/belly springs integrated once over the whole timeline (deterministic seeking). */
import * as THREE from "three";

export const ss = (x) => x * x * (3 - 2 * x), clamp = (x, a, b) => Math.min(b, Math.max(a, x)), lerp = (a, b, f) => a + (b - a) * f;
export const seg = (t, a, b) => ss(clamp((t - a) / (b - a), 0, 1));
export const pulse = (t, a, b, c, d) => seg(t, a, b) - seg(t, c, d);          // up between a-b, down between c-d
export const rnd = (i) => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };

// tinted ramp: shadow band purple, mid neutral-lilac, lit band warm (hue shift instead of grey shadows)
const RAMP = new Uint8Array([122, 108, 168, 255, 208, 194, 214, 255, 255, 248, 236, 255]);
const grad = new THREE.DataTexture(RAMP, 3, 1); grad.minFilter = grad.magFilter = THREE.NearestFilter; grad.needsUpdate = true;
export const OUTLINE = new THREE.Color("#2A1636");

export function toon(color, o = {}) {
  const { ao = false, spec = 0, rim = 0.3, ...rest } = o;
  const m = new THREE.MeshToonMaterial(Object.assign({ color, gradientMap: grad, vertexColors: ao }, rest));
  m.onBeforeCompile = (s) => {
    s.uniforms.rimColor = { value: new THREE.Color("#FFE2B8") };
    let f = "uniform vec3 rimColor;\n" + s.fragmentShader;
    if (ao) f = f.replace("#include <color_fragment>", "diffuseColor.rgb *= mix(vec3(0.5, 0.4, 0.68), vec3(1.0), vColor.r);");
    f = f.replace("#include <opaque_fragment>",
      "float rim = pow(1.0 - saturate(dot(normal, normalize(vViewPosition))), 3.0);\n" +
      "outgoingLight += smoothstep(0.55, 0.72, rim) * rimColor * " + rim.toFixed(2) + ";\n" +
      (spec ? "vec3 H = normalize(normalize(vec3(-0.35, 0.75, 0.55)) + normalize(vViewPosition));\noutgoingLight += step(0.955, dot(normal, H)) * vec3(1.0, 0.97, 0.9) * " + spec.toFixed(2) + ";\n" : "") +
      "#include <opaque_fragment>");
    s.fragmentShader = f;
  };
  return m;
}

function smoothNormals(g) {
  const p = g.attributes.position, n = g.attributes.normal, acc = new Map(), out = new Float32Array(p.count * 3);
  const key = (i) => p.getX(i).toFixed(4) + "," + p.getY(i).toFixed(4) + "," + p.getZ(i).toFixed(4);
  for (let i = 0; i < p.count; i++) { const k = key(i), a = acc.get(k) || [0, 0, 0]; a[0] += n.getX(i); a[1] += n.getY(i); a[2] += n.getZ(i); acc.set(k, a); }
  for (let i = 0; i < p.count; i++) { const a = acc.get(key(i)), l = Math.hypot(a[0], a[1], a[2]) || 1; out.set([a[0] / l, a[1] / l, a[2] / l], i * 3); }
  g.setAttribute("outlineNormal", new THREE.BufferAttribute(out, 3));
}
export function outline(mesh, w) {
  if (!mesh.geometry.attributes.normal) mesh.geometry.computeVertexNormals();
  if (!mesh.geometry.attributes.outlineNormal) smoothNormals(mesh.geometry);
  const m = new THREE.MeshBasicMaterial({ color: OUTLINE, side: THREE.BackSide });
  m.onBeforeCompile = (s) => { s.vertexShader = "attribute vec3 outlineNormal;\n" + s.vertexShader.replace("#include <begin_vertex>", "#include <begin_vertex>\ntransformed += outlineNormal * " + w.toFixed(5) + ";"); };
  const o = mesh.isSkinnedMesh ? new THREE.SkinnedMesh(mesh.geometry, m) : new THREE.Mesh(mesh.geometry, m);
  if (mesh.isSkinnedMesh) o.bind(mesh.skeleton, mesh.bindMatrix);
  o.frustumCulled = false; o.castShadow = false; mesh.add(o); return o;
}
export function shade(o) { o.traverse((m) => { if (m.isMesh) { m.castShadow = true; m.receiveShadow = true; } }); return o; }

/* ---------- characters ---------- */
const NO_LINE = /^(eye|glint|lglint|cheek|brow|mustache|buckle|thumb|band|lens|rim|bridge)/;
const BASIC = { eye: "#150A34", lens: "#150A34", glint: "#ffffff" };
const SPEC = { buckle: 0.35, nose: 0.25, boot: 0.2, flop: 0.2, knot: 0.12 };
export class Character {
  constructor(gltf, wOut = 0.0024) {
    this.root = gltf.scene; this.W = new THREE.Group(); this.W.add(this.root); this.anims = gltf.animations;
    this.mixer = new THREE.AnimationMixer(this.root); this.sched = []; this.bones = {};
    this.root.traverse((o) => { if (o.isBone) this.bones[o.name.replace(/\./g, "")] = o; });
    const sk = []; this.root.traverse((o) => { if (o.isSkinnedMesh) sk.push(o); });
    for (const m of sk) {
      const name = m.material.name, c = m.material.color.clone(), hasAO = !!m.geometry.attributes.color;
      m.material = BASIC[name] ? new THREE.MeshBasicMaterial({ color: BASIC[name] }) : toon(c, { ao: hasAO, spec: SPEC[name] || 0 });
      m.castShadow = !BASIC[name]; m.receiveShadow = !BASIC[name]; m.frustumCulled = false;
      if (!NO_LINE.test(name) && !NO_LINE.test(m.name)) outline(m, wOut);
    }
    this.rest = {}; for (const k in this.bones) this.rest[k] = { q: this.bones[k].quaternion.clone(), p: this.bones[k].position.clone(), s: this.bones[k].scale.clone() };
  }
  b(n) { return this.bones[n.replace(/\./g, "")]; }
  clip(n) { const c = THREE.AnimationClip.findByName(this.anims, n); if (!c) throw new Error("no clip " + n); return c; }
  add(name, a, b, o = {}) { const e = Object.assign({ c: name, a, b, fade: 0.22, loop: true, speed: 1, off: 0 }, o); e.act = this.mixer.clipAction(this.clip(name).clone()); e.act.play(); e.act.setEffectiveWeight(0); this.sched.push(e); return e; }
  apply(t) {
    for (const k of ["hat1", "hat2", "hat3", "beard1", "beard2", "belly", "eyes", "brows", "glasses"]) {
      const b = this.bones[k]; if (b) { b.quaternion.copy(this.rest[k].q); b.position.copy(this.rest[k].p); b.scale.copy(this.rest[k].s); } }
    const ws = this.sched.map((e) => (t < e.a || t > e.b ? 0 : Math.min(1, (t - e.a) / e.fade, (e.b - t) / e.fade)));
    const sum = ws.reduce((x, y) => x + y, 0) || 1;
    this.sched.forEach((e, i) => { const d = e.act.getClip().duration, lt = (t - e.a) * e.speed + e.off;
      e.act.time = e.loop ? ((lt % d) + d) % d : clamp(lt, 0, d - 1e-3); e.act.setEffectiveWeight(ws[i] / sum); });
    this.mixer.update(0); this.W.updateMatrixWorld(true);
  }
  // walking speed of a clip: how fast a planted foot slides back (no foot sliding when the path matches it)
  stanceSpeed(name) {
    const m = new THREE.AnimationMixer(this.root), a = m.clipAction(this.clip(name)); a.play();
    const d = this.clip(name).duration, foot = this.b("DEF-foot.L"), S = [], p = new THREE.Vector3(), W0 = this.W.matrixWorld.clone();
    this.W.position.set(0, 0, 0); this.W.rotation.set(0, 0, 0); this.W.scale.set(1, 1, 1);
    for (let i = 0; i <= 120; i++) { a.time = d * i / 120; m.update(0); this.W.updateMatrixWorld(true); foot.getWorldPosition(p); S.push(p.clone()); }
    const ymin = Math.min(...S.map((q) => q.y)); let v = 0, n = 0;
    for (let i = 1; i < S.length; i++) if (S[i].y < ymin + 0.006 && S[i - 1].y < ymin + 0.006) { v += (S[i - 1].z - S[i].z) / (d / 120); n++; }
    a.stop(); m.uncacheRoot(this.root); return Math.abs(v / Math.max(n, 1));
  }
}

const _q = new THREE.Quaternion(), _q2 = new THREE.Quaternion(), _v = new THREE.Vector3(), _v2 = new THREE.Vector3();
// rotate a bone about a WORLD axis by angle (independent of the bone's local axes)
export function rotWorld(bone, axis, angle) {
  if (!angle) return;
  bone.parent.getWorldQuaternion(_q2); const bw = new THREE.Quaternion(); bone.getWorldQuaternion(bw);
  _q.setFromAxisAngle(axis, angle); const nw = _q.multiply(bw);
  bone.quaternion.copy(_q2.invert().multiply(nw)); bone.updateMatrixWorld(true);
}
// aim a bone so that its child point moves from `from` toward `to` (world), weight w
function aim(bone, from, to, w) {
  const o = new THREE.Vector3(); bone.getWorldPosition(o);
  const a = from.clone().sub(o).normalize(), b = to.clone().sub(o).normalize();
  const dq = new THREE.Quaternion().setFromUnitVectors(a, b); const id = new THREE.Quaternion(); id.slerp(dq, w);
  bone.parent.getWorldQuaternion(_q2); const bw = new THREE.Quaternion(); bone.getWorldQuaternion(bw);
  bone.quaternion.copy(_q2.invert().multiply(id.multiply(bw))); bone.updateMatrixWorld(true);
}
// two-bone IK for an arm: hand reaches `target` (world), elbow bends toward `pole` (world point), blend weight w
export function ikArm(upper, fore, hand, target, pole, w) {
  if (w <= 0) return;
  const s = new THREE.Vector3(), e = new THREE.Vector3(), h = new THREE.Vector3();
  upper.getWorldPosition(s); fore.getWorldPosition(e); hand.getWorldPosition(h);
  const a = s.distanceTo(e), b = e.distanceTo(h); let d = clamp(s.distanceTo(target), 0.05, (a + b) * 0.999);
  const dir = target.clone().sub(s).normalize(); const tgt = s.clone().add(dir.clone().multiplyScalar(d));
  const cosA = clamp((a * a + d * d - b * b) / (2 * a * d), -1, 1), ang = Math.acos(cosA);
  const pv = pole.clone().sub(s); pv.sub(dir.clone().multiplyScalar(pv.dot(dir))).normalize();
  const elbow = s.clone().add(dir.clone().multiplyScalar(Math.cos(ang) * a)).add(pv.multiplyScalar(Math.sin(ang) * a));
  aim(upper, e, elbow, w); fore.getWorldPosition(e); hand.getWorldPosition(h); aim(fore, h, tgt, w);
}

/* springs: secondary motion simulated once for every frame (seeking stays deterministic).
   parts: [{ ref: () => Vector3 world point (e.g. above the head), frame: () => Quaternion (world) of the driving bone,
             f: Hz, z: damping ratio, g: gain }] -> arrays of 2D offsets per frame */
export function simulateSprings(N, FPS, poseAt, parts) {
  const out = parts.map(() => new Float32Array(N * 2)), st = parts.map(() => [0, 0, 0, 0]), prev = parts.map(() => []);
  const q = new THREE.Quaternion();
  for (let f = 0; f < N; f++) {
    poseAt(f / FPS);
    parts.forEach((P, k) => {
      const p = P.ref(); prev[k].push(p.clone()); const a = new THREE.Vector3();
      if (f >= 2) a.copy(prev[k][f]).sub(prev[k][f - 1].clone().multiplyScalar(2)).add(prev[k][f - 2]).multiplyScalar(FPS * FPS);
      q.copy(P.frame()).invert(); a.applyQuaternion(q);
      const K = (2 * Math.PI * P.f) ** 2, C = 2 * P.z * Math.sqrt(K), s = st[k];
      for (let sub = 0; sub < 4; sub++) { const dt = 1 / FPS / 4;
        s[2] += (-K * s[0] - C * s[2] - P.g * a.x) * dt; s[3] += (-K * s[1] - C * s[3] - P.g * (P.gy ? a.y : a.z)) * dt; s[0] += s[2] * dt; s[1] += s[3] * dt; }
      out[k][f * 2] = clamp(s[0], -P.lim, P.lim); out[k][f * 2 + 1] = clamp(s[1], P.minB ?? -P.lim, P.lim);
    });
  }
  return out;
}

/* camera shots: [[t0, pos, look, fov], ...]; within a shot the camera eases between its keys; a shot list with cut
   times makes hard cuts (research: ~4 shots, cut on action) */
export function cameraAt(cam, shots, t) {
  let s = shots[0]; for (const sh of shots) if (t >= sh.t) s = sh;
  const f = seg(t, s.t, s.t + s.d), p = s.from.map((v, i) => lerp(v, s.to[i], f)), l = s.lookFrom.map((v, i) => lerp(v, s.lookTo[i], f));
  cam.fov = s.fov; cam.updateProjectionMatrix(); cam.position.set(...p); cam.lookAt(...l);
}
