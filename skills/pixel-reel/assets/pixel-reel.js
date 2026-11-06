/* pixel-reel.js: stepped sprite animation for HyperFrames (GSAP timeline, seek-safe).
 *
 * Every sprite is a horizontal strip PNG (all frames side by side, already at x4) described in atlas.json.
 * An "actor" is one <div> in the HTML; the runtime swaps its strip and background-position with tl.set,
 * so frames change in hard steps like a 16-bit game, and every frame is a pure function of timeline time.
 *
 * Positions are given in ART PIXELS of the 270x480 grid; the runtime multiplies by atlas.scale (4).
 * The actor's anchor (feet / base / centre, from the atlas) is what lands on (x, y).
 *
 * Author each actor's calls in time order: moves remember where the actor ended, so the next move starts there.
 *
 * Motion model (v2, "smooth"): sprite FRAMES change in steps (that is what makes it pixel art), but POSITIONS are
 * interpolated on every video frame and snapped to the art-pixel grid (multiples of the scale), so movement is
 * continuous and never leaves the pixel grid. Sprite fps are rounded to a divisor of the video fps (opts.videoFps,
 * default 60) so every frame is held for the same number of video frames (8 fps in a 30 fps video judders 4-3-4-3).
 * opts.smooth=false restores the old stepped motion.
 */
(function (global) {
  function PixelReel(tl, atlas, opts) {
    opts = opts || {};
    const S = atlas.scale || 4, base = opts.base || "", R = { tl, atlas, S };
    const SMOOTH = opts.smooth !== false, VFPS = opts.videoFps || 60;
    const snapPx = (v) => Math.round(parseFloat(v) / S) * S + "px";
    const SNAP = { x: snapPx, y: snapPx };
    // nearest sprite rate that divides the video rate (60 -> 6,10,12,15,20,30)
    R.fps = function (f) {
      const ok = []; for (let d = 1; d <= VFPS; d++) if (VFPS % d === 0) ok.push(VFPS / d);
      return ok.reduce((b, c) => (Math.abs(c - f) < Math.abs(b - f) ? c : b), ok[0]);
    };
    // dense samples of a path, linearly interpolated per video frame and snapped -> smooth curves on the pixel grid
    const pathKf = (n, fn, dur) => { const kf = []; for (let i = 1; i <= n; i++) kf.push(Object.assign(fn(i / n), { duration: dur / n, ease: "none" })); return kf; };
    const spec = (key) => {
      const s = atlas.sprites[key];
      if (!s) throw new Error("pixel-reel: sprite not in atlas: " + key);
      return s;
    };
    const frameCss = (s, f) => ({ backgroundPosition: -f * s.w * S + "px 0px" });

    /* ---------- actors ---------- */
    R.actor = function (sel, startKey, x, y, o) {
      o = o || {};
      const a = { sel, key: null, x: x || 0, y: y || 0, flip: !!o.flip, sc: o.scale || 1 };
      // optional cast-shadow element (a pre-rendered 3D sprite's "<key>.shadow" strip, shown with a multiply blend):
      // it gets the same frames, position and squash as the actor; keys without a shadow strip leave it empty
      const cast = o.cast || null, ALL = cast ? [sel, cast] : sel;
      a.use = function (t, key, frame, flip) {
        const s = spec(key);
        if (flip !== undefined) a.flip = flip;
        const fl = a.flip && s.mirror !== false;
        tl.set(sel, {
          width: s.w * S, height: s.h * S,
          backgroundImage: "url(" + base + s.file + ")",
          backgroundSize: s.frames * s.w * S + "px " + s.h * S + "px",
          marginLeft: -s.ax * S, marginTop: -s.ay * S,
          transformOrigin: s.ax * S + "px " + s.ay * S + "px",
          scaleX: (fl ? -1 : 1) * a.sc, scaleY: a.sc, backgroundPosition: -(frame || 0) * s.w * S + "px 0px",
        }, t);
        if (cast) {
          const cs = atlas.sprites[key + ".shadow"];
          tl.set(cast, cs ? { width: s.w * S, height: s.h * S, backgroundImage: "url(" + base + cs.file + ")",
            backgroundSize: s.frames * s.w * S + "px " + s.h * S + "px", marginLeft: -s.ax * S, marginTop: -s.ay * S,
            transformOrigin: s.ax * S + "px " + s.ay * S + "px", scaleX: (fl ? -1 : 1) * a.sc, scaleY: a.sc,
            backgroundPosition: -(frame || 0) * s.w * S + "px 0px" } : { backgroundImage: "none" }, t);
        }
        a.key = key; return a;
      };
      // play an animation: {dur} for loops, {frames:[...]} custom order, {reverse}, {fps}, {flip}
      a.play = function (t, key, p) {
        p = p || {};
        const s = spec(key), fps = R.fps(p.fps || s.fps || 8), dt = 1 / fps;
        a.use(t, key, 0, p.flip);
        let order = p.frames || [...Array(s.frames).keys()];
        if (p.reverse) order = order.slice().reverse();
        let end;
        if ((p.mode || s.mode) === "loop") {
          const dur = p.dur || order.length * dt;
          let k = 0;
          for (let tt = t; tt < t + dur - 1e-6; tt += dt, k++) tl.set(ALL, frameCss(s, order[k % order.length]), tt);
          end = t + dur;
        } else {
          order.forEach((f, k) => tl.set(ALL, frameCss(s, f), t + k * dt));
          end = t + order.length * dt;
        }
        return end;
      };
      a.frame = function (t, key, f, flip) { a.use(t, key, f, flip); return t; };
      const sh = o.shadow || null;              // optional contact-shadow element: follows x, stays on the floor
      a.place = function (t, x, y) { a.x = x; a.y = y; tl.set(ALL, { x: x * S, y: y * S }, t); if (sh) tl.set(sh, { x: x * S, y: y * S }, t); return t; };
      const ground = (t, dur, x0, y0, x1, y1, ease) => { if (sh) tl.fromTo(sh, { x: x0 * S, y: y0 * S }, { x: x1 * S, y: y1 * S, duration: dur, ease: ease || "none", modifiers: SNAP, immediateRender: false }, t); };
      const VIS = [sel].concat(sh ? [sh] : [], cast ? [cast] : []);
      a.show = function (t) { tl.set(VIS, { opacity: 1 }, t); return t; };
      a.hide = function (t) { tl.set(VIS, { opacity: 0 }, t); return t; };
      a.z = function (t, z) { tl.set(sel, { zIndex: z }, t); return t; };
      // stepped straight move
      // straight move: smooth (eased, snapped to the art grid) or stepped (legacy)
      a.moveTo = function (t, dur, x, y, steps, ease) {
        const e = SMOOTH ? (ease || "power1.inOut") : "steps(" + (steps || Math.max(1, Math.round(dur * 8))) + ")";
        tl.fromTo(ALL, { x: a.x * S, y: a.y * S }, { x: x * S, y: y * S, duration: dur, ease: e, modifiers: SMOOTH ? SNAP : {}, immediateRender: false }, t);
        ground(t, dur, a.x, a.y, x, y, e);
        a.x = x; a.y = y; return t + dur;
      };
      // walk: moves while a walk loop plays (key = walk animation), bob is already in the frames
      a.walk = function (t, dur, x, y, key, p) {
        p = p || {}; a.play(t, key, Object.assign({ dur }, p));
        // constant speed while walking (feet stay in sync with distance); a short ease only at start and end
        return a.moveTo(t, dur, x, y, p.steps || Math.max(1, Math.round(dur * (spec(key).fps || 8))), p.ease || "sine.inOut");
      };
      // hops with landing squash (n hops of height h art px)
      a.hops = function (t, dur, x, y, n, h) {
        const x0 = a.x, y0 = a.y;
        if (SMOOTH) {      // each hop: parabolic air time, then a quick landing squash
          const per = dur / n, air = per * 0.72, land = per - air, kf = [];
          for (let i = 0; i < n; i++) {
            const xa = x0 + (x - x0) * i / n, ya = y0 + (y - y0) * i / n, xb = x0 + (x - x0) * (i + 1) / n, yb = y0 + (y - y0) * (i + 1) / n;
            pathKf(Math.max(4, Math.round(air * VFPS / 2)), (f) => ({ x: (xa + (xb - xa) * f) * S, y: (ya + (yb - ya) * f - 4 * h * f * (1 - f)) * S, scaleY: a.sc * (f < 0.5 ? 1.05 : 1) }), air).forEach((k) => kf.push(k));
            kf.push({ scaleY: 0.9 * a.sc, duration: land * 0.5, ease: "power2.out" }, { scaleY: a.sc, duration: land * 0.5, ease: "back.out(3)" });
          }
          tl.fromTo(sel, { x: x0 * S, y: y0 * S, scaleY: a.sc }, { keyframes: kf, modifiers: SNAP, immediateRender: false }, t);
          ground(t, dur, x0, y0, x, y);
          a.x = x; a.y = y; return t + dur;
        }
        const kf = [], d = dur / n / 3;
        for (let i = 1; i <= n; i++) {
          const fm = (i - 0.5) / n, f = i / n;
          kf.push({ x: (x0 + (x - x0) * fm) * S, y: (y0 + (y - y0) * fm - h) * S, scaleY: 1.06 * a.sc, duration: d, ease: "steps(1)" });
          kf.push({ x: (x0 + (x - x0) * f) * S, y: (y0 + (y - y0) * f) * S, scaleY: 0.9 * a.sc, duration: d, ease: "steps(1)" });
          kf.push({ scaleY: a.sc, duration: d, ease: "steps(1)" });
        }
        tl.fromTo(sel, { x: x0 * S, y: y0 * S, scaleY: a.sc }, { keyframes: kf, immediateRender: false }, t);
        a.x = x; a.y = y; return t + dur;
      };
      // squash & stretch pop (appear, land, sit)
      a.pop = function (t, from) {
        if (SMOOTH) {
          tl.fromTo(ALL, { scaleY: (from || 0.8) * a.sc, scaleX: (a.flip ? -1 : 1) * a.sc * 1.08 }, { scaleY: a.sc, scaleX: (a.flip ? -1 : 1) * a.sc, duration: 0.28, ease: "elastic.out(1.1, 0.45)", immediateRender: false }, t);
          return t + 0.28;
        }
        tl.fromTo(sel, { scaleY: (from || 0.8) * a.sc }, { keyframes: [{ scaleY: 1.12 * a.sc, duration: 0.07, ease: "steps(1)" }, { scaleY: 0.96 * a.sc, duration: 0.07, ease: "steps(1)" }, { scaleY: a.sc, duration: 0.07, ease: "steps(1)" }], immediateRender: false }, t);
        return t + 0.21;
      };
      // flight along a stepped parabola (items thrown, birds)
      a.arc = function (t, dur, x, y, h, steps) {
        const x0 = a.x, y0 = a.y;
        if (SMOOTH) {      // real parabola sampled per video frame, slight ease-in on the fall
          const kf = pathKf(Math.max(6, Math.round(dur * VFPS)), (f) => { const g = f * f * (3 - 2 * f) * 0.35 + f * 0.65; return { x: (x0 + (x - x0) * g) * S, y: (y0 + (y - y0) * g - 4 * h * g * (1 - g)) * S }; }, dur);
          tl.fromTo(sel, { x: x0 * S, y: y0 * S }, { keyframes: kf, modifiers: SNAP, immediateRender: false }, t);
          a.x = x; a.y = y; return t + dur;
        }
        steps = steps || 4; const kf = [];
        for (let i = 1; i <= steps; i++) {
          const f = i / steps;
          kf.push({ x: (x0 + (x - x0) * f) * S, y: (y0 + (y - y0) * f - 4 * h * f * (1 - f)) * S, duration: dur / steps, ease: "steps(1)" });
        }
        tl.fromTo(sel, { x: x0 * S, y: y0 * S }, { keyframes: kf, immediateRender: false }, t);
        a.x = x; a.y = y; return t + dur;
      };
      a.shake = function (t, dur, amp) {
        const kf = []; const n = Math.max(2, Math.round(dur * 20));
        for (let i = 0; i < n; i++) kf.push({ x: (a.x + (i % 2 ? -amp : amp)) * S, duration: dur / n, ease: "steps(1)" });
        kf.push({ x: a.x * S, duration: 0.001 });
        tl.fromTo(ALL, { x: a.x * S }, { keyframes: kf, immediateRender: false }, t);
        return t + dur;
      };
      if (startKey) a.use(0, startKey, 0);
      tl.set(ALL, { x: a.x * S, y: a.y * S }, 0);
      if (sh) tl.set(sh, { x: a.x * S, y: a.y * S }, 0);
      return a;
    };

    /* ---------- one-shot effects from a pool of <div class="pr-fx"> ---------- */
    const pool = opts.fxPool || [];
    let next = 0;
    R.fx = function (t, key, x, y, p) {
      p = p || {};
      if (!pool.length) throw new Error("pixel-reel: no fx pool");
      const sel = pool[next++ % pool.length];
      const a = R.actor(sel, null, x, y);
      tl.set(sel, { opacity: 1 }, t);
      a.place(t, x, y);
      const end = a.play(t, key, p);
      tl.set(sel, { opacity: 0 }, p.loop ? t + (p.dur || 0.5) : end);
      return end;
    };

    /* ---------- block dissolve between two full-frame images ---------- */
    R.dissolve = function (t, frameSels, step) {
      frameSels.forEach((s, i) => {
        tl.set(s, { opacity: 1 }, t + i * step);
        if (i) tl.set(frameSels[i - 1], { opacity: 0 }, t + i * step);
      });
      return t + frameSels.length * step;
    };
    return R;
  }
  global.PixelReel = PixelReel;
})(window);
