(function () {
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var root = document.documentElement;
  var WA_NUM = '59892104419';
  var WA = 'https://wa.me/' + WA_NUM + '?text=';

  // One art pixel, in whole screen pixels, so every sprite shares a grid.
  function setPx() {
    var w = innerWidth, h = innerHeight;
    var px = w <= 900 ? Math.max(2, Math.floor(w / 190)) : Math.max(2, Math.floor(Math.min(w / 380, h / 225)));
    root.style.setProperty('--px', px + 'px');
    return px;
  }
  var PX = setPx();

  var api = ScrollCraft.mount(document.body);

  // ------------------------------------------------------------ stars, sparks
  function starfield(cv) {
    var ctx = cv.getContext('2d'), stars = [], w, h;
    function size() {
      w = cv.width = Math.ceil(cv.clientWidth / PX); h = cv.height = Math.ceil(cv.clientHeight / PX);
      stars = [];
      var n = Math.round(w * h / 260), seed = 11;
      function rnd() { seed = (seed * 16807) % 2147483647; return seed / 2147483647; }
      var copy = cv.parentNode.querySelector('.title__copy, .counter__copy'), box = null;
      if (copy) {
        var cr = copy.getBoundingClientRect(), sr = cv.getBoundingClientRect(), pad = 28;
        box = { x0: (cr.left - sr.left - pad) / PX, x1: (cr.right - sr.left + pad) / PX, y0: (cr.top - sr.top - pad) / PX, y1: (cr.bottom - sr.top + pad) / PX };
      }
      for (var i = 0; i < n; i++) {
        var st = { x: Math.floor(rnd() * w), y: Math.floor(rnd() * h * 0.78), b: rnd(), s: rnd() < 0.08 };
        if (box && st.x > box.x0 && st.x < box.x1 && st.y > box.y0 && st.y < box.y1) continue;
        stars.push(st);
      }
    }
    // now and then a shooting star crosses the right side of the sky
    var met = null, nextMet = 2500 + Math.random() * 4000;
    function draw(t) {
      ctx.clearRect(0, 0, w, h);
      stars.forEach(function (s) {
        var on = reduce ? 1 : (Math.sin(t / 700 + s.b * 40) > -0.6 ? 1 : 0.35);
        ctx.fillStyle = s.b > 0.85 ? 'rgba(242,169,59,' + on + ')' : 'rgba(201,194,242,' + (0.55 * on) + ')';
        ctx.fillRect(s.x, s.y, 1, 1);
        if (s.s) { ctx.fillRect(s.x - 1, s.y, 3, 1); ctx.fillRect(s.x, s.y - 1, 1, 3); }
      });
      if (reduce) return;
      if (!met && t > nextMet) met = { x: Math.round(w * (0.55 + Math.random() * 0.4)), y: Math.round(h * (0.05 + Math.random() * 0.25)), l: 0 };
      if (met) {
        met.l += 1;
        var hx = met.x - Math.floor(met.l * 1.4), hy = met.y + Math.floor(met.l * 0.7);
        for (var k = 0; k < 7; k++) {
          ctx.fillStyle = k === 0 ? 'rgba(255,240,200,1)' : 'rgba(242,169,59,' + (0.85 - k * 0.12).toFixed(2) + ')';
          ctx.fillRect(hx + k * 2, hy - k, 2, 1);
        }
        if (met.l > 46) { met = null; nextMet = t + 7000 + Math.random() * 9000; }
      }
    }
    size(); addEventListener('resize', size);
    if (document.fonts) document.fonts.ready.then(size);
    return draw;
  }
  function sparks(cv, anchor) {
    var ctx = cv.getContext('2d'), w, h, ps = [];
    function size() { w = cv.width = Math.ceil(cv.clientWidth / PX); h = cv.height = Math.ceil(cv.clientHeight / PX); }
    size(); addEventListener('resize', size);
    return function () {
      ctx.clearRect(0, 0, w, h);
      var r = anchor.getBoundingClientRect(), sr = cv.getBoundingClientRect();
      var cx = (r.left - sr.left + r.width / 2) / PX, cy = (r.top - sr.top + r.height * 0.55) / PX, half = r.width / PX / 2;
      if (!reduce && ps.length < 26 && Math.random() < 0.3) ps.push({ x: cx + (Math.random() * 2 - 1) * half * 1.15, y: cy + Math.random() * half, v: 0.12 + Math.random() * 0.25, l: 1 });
      ps = ps.filter(function (p) { return p.l > 0; });
      ps.forEach(function (p) {
        p.y -= p.v; p.l -= 0.006 + p.v * 0.01;
        ctx.fillStyle = p.l > 0.5 ? '#FFD98A' : '#F2A93B';
        ctx.fillRect(Math.round(p.x), Math.round(p.y), 1, 1);
      });
    };
  }
  var drawers = [];
  document.querySelectorAll('[data-stars]').forEach(function (cv) { drawers.push({ el: cv, fn: starfield(cv) }); });
  var sp = document.querySelector('[data-sparks]');
  var titleGlyph = document.querySelector('.title .glyph');
  if (sp && titleGlyph) drawers.push({ el: sp, fn: sparks(sp, titleGlyph) });

  // ------------------------------------------- the glyph prints itself on load
  // 92 art rows, two rows a pass, the head zig-zagging across each pass.
  (function printGlyph() {
    var g = titleGlyph; if (!g) return;
    if (reduce) { g.style.setProperty('--printed', '100%'); g.style.setProperty('--head-o', '1'); g.style.setProperty('--head-x', '96%'); g.classList.add('is-parked'); return; }
    var ROWS = 92, STEP = 2, passMs = 42, start = null, lastPass = -1;
    g.style.setProperty('--printed', '0%');
    g.style.setProperty('--ghost', '0.22');
    g.style.setProperty('--head-o', '1');
    function tick(t) {
      if (start === null) start = t + 350;
      var e = t - start;
      if (e < 0) { requestAnimationFrame(tick); return; }
      var passes = ROWS / STEP, pass = Math.min(passes, e / passMs), whole = Math.floor(pass), frac = pass - whole;
      var rows = Math.min(ROWS, whole * STEP);
      if (whole !== lastPass) { lastPass = whole; g.style.setProperty('--printed', (rows / ROWS * 100).toFixed(2) + '%'); }
      var dir = whole % 2 ? -1 : 1, x = dir > 0 ? frac : 1 - frac;
      g.style.setProperty('--head-x', (10 + x * 80).toFixed(1) + '%');
      if (pass < passes) requestAnimationFrame(tick);
      else {
        g.style.setProperty('--printed', '100%');
        g.style.setProperty('--ghost', '0');
        // the head parks at the side, like a printer that just finished
        g.classList.add('is-parked');
        g.style.setProperty('--head-x', '96%');
      }
    }
    requestAnimationFrame(tick);
  })();

  // ------------------------------------------- photos print in as they appear
  var shots = Array.prototype.slice.call(document.querySelectorAll('.item .shot'));
  shots.forEach(function (s, i) {
    s._rows = 32; s._head = (i * 37) % 100; s._k = -1;
    if (reduce) s.classList.add('is-done');
  });
  var printing = false;
  function queuePrint() { if (!printing && !reduce) { printing = true; requestAnimationFrame(printStep); } }
  function printStep() {
    var vh = innerHeight, busy = false;
    shots.forEach(function (s) {
      if (s.classList.contains('is-done') || s.closest('[hidden]')) return;
      var r = s.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) { if (s._k >= 0) busy = true; return; }
      if (s._k < 0) s._k = 0;
      s._k = Math.min(1, s._k + 0.045);
      var done = Math.floor(s._k * s._rows) / s._rows;
      s.style.setProperty('--done', (done * 100).toFixed(2) + '%');
      s._head = (s._head + 29) % 100;
      s.style.setProperty('--head', (8 + s._head * 0.84).toFixed(1) + '%');
      if (s._k >= 1) s.classList.add('is-done'); else busy = true;
    });
    if (busy) requestAnimationFrame(printStep); else printing = false;
  }
  addEventListener('scroll', queuePrint, { passive: true });

  // ---------------------------------------------------------------- shelves
  // Every shelf is on the page; the scroll walks you past them and the menu
  // follows with an RPG cursor. Tabs are plain links, so it works without JS.
  var shelves = Array.prototype.slice.call(document.querySelectorAll('.shelf'));
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.shelf-tab'));
  var menu = document.querySelector('.shelves');
  var cursor = document.querySelector('.menu-cursor');
  var nowBar = document.querySelector('.shelf-now');
  var nowName = document.querySelector('[data-now]');
  var nowIcon = document.querySelector('.now-icon');
  var hud = document.querySelector('.hud');
  var shopEl = document.getElementById('catalogo');
  var active = -1;
  var wide = function () { return innerWidth > 900; };

  // a shelf shows one row on a wide screen and two rows otherwise; "ver los N" opens the rest
  function limits() {
    shelves.forEach(function (sh) {
      var grid = sh.querySelector('.grid');
      var cols = getComputedStyle(grid).gridTemplateColumns.split(' ').length;
      var lim = cols >= 5 ? cols : cols * 2;
      var items = Array.prototype.slice.call(grid.children);
      var open = sh.classList.contains('is-open');
      items.forEach(function (it, i) { it.hidden = !open && i >= lim; });
      var btn = sh.querySelector('.shelf__all');
      btn.hidden = items.length <= lim;
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.querySelector('span').textContent = open ? 'Ver menos' : 'Ver los ' + items.length;
    });
    queuePrint();
  }
  shelves.forEach(function (sh) {
    sh.querySelector('.shelf__all').addEventListener('click', function () {
      var opening = !sh.classList.contains('is-open');
      var shown = sh.querySelectorAll('.item:not([hidden])').length;
      sh.classList.toggle('is-open', opening);
      limits();
      if (opening && !reduce) {
        Array.prototype.slice.call(sh.querySelectorAll('.item')).slice(shown).forEach(function (it, k) {
          it.style.animationDelay = (k * 45) + 'ms';
          it.classList.remove('is-new'); void it.offsetWidth; it.classList.add('is-new');
        });
      }
      if (!opening) {
        var top = sh.querySelector('.shelf__head').getBoundingClientRect().top;
        if (top < 0) scrollTo({ top: top + scrollY - hud.offsetHeight - (wide() ? 70 : 52) - 16 });
      }
    });
  });

  function toShelf(i) {
    var head = shelves[i].querySelector('.shelf__head');
    var target = head.getBoundingClientRect().top + scrollY - hud.offsetHeight - (wide() ? 70 : 52) - 20;
    scrollTo({ top: target, behavior: reduce ? 'auto' : 'smooth' });
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function (ev) { ev.preventDefault(); toShelf(i); });
  });
  document.querySelectorAll('[data-step]').forEach(function (b) {
    b.addEventListener('click', function () {
      var n = shelves.length, to = ((active < 0 ? 0 : active) + (+b.getAttribute('data-step')) + n) % n;
      toShelf(to);
    });
  });

  function placeCursor() {
    if (!cursor || !menu) return;
    if (active < 0 || !wide()) { menu.classList.remove('has-cursor'); return; }
    var t = tabs[active];
    cursor.style.setProperty('--cur-x', Math.round(t.offsetLeft + t.offsetWidth / 2 - 12) + 'px');
    menu.classList.add('has-cursor');
  }
  function mark() {
    tabs.forEach(function (t, i) { if (i === active) t.setAttribute('aria-current', 'true'); else t.removeAttribute('aria-current'); });
    if (active > -1) {
      if (nowName) nowName.textContent = shelves[active].getAttribute('data-name');
      if (nowIcon) nowIcon.innerHTML = tabs[active].querySelector('svg').outerHTML;
    }
    placeCursor();
  }
  // which shelf are you standing in front of
  function spy() {
    if (!menu) return;
    var navH = hud.offsetHeight, mr = menu.getBoundingClientRect(), sr = shopEl.getBoundingClientRect();
    menu.classList.toggle('is-stuck', wide() && mr.top <= navH + 1 && sr.bottom > navH + 200);
    var line = navH + (wide() ? 70 : 52) + 80, cur = -1;
    shelves.forEach(function (sh, i) { if (sh.getBoundingClientRect().top <= line) cur = i; });
    if (sr.top > innerHeight * 0.5) cur = -1;
    if (cur !== active) { active = cur; mark(); }
    if (nowBar) nowBar.classList.toggle('is-shown', !wide() && cur > -1 && mr.bottom < navH && sr.bottom > navH + 160);
  }
  // each shelf's badge pops the first time its title comes into view
  if ('IntersectionObserver' in window) {
    var seenIO = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.closest('.shelf').classList.add('is-seen'); seenIO.unobserve(e.target); } });
    }, { threshold: 0.6 });
    shelves.forEach(function (sh) { seenIO.observe(sh.querySelector('.shelf__head')); });
  }
  limits();
  addEventListener('resize', function () { limits(); placeCursor(); });

  // -------------------------------------------- the order: an inventory
  var KEY = 'mago-pedido-v1';
  var order = [];
  try { order = JSON.parse(localStorage.getItem(KEY) || '[]').filter(function (o) { return o && o.id && o.n; }); } catch (e) { order = []; }
  var byId = {};
  document.querySelectorAll('.item').forEach(function (it) { byId[it.getAttribute('data-id')] = it; });
  order = order.filter(function (o) { return byId[o.id]; });

  var bag = document.querySelector('.bag b');
  var bagBtn = document.querySelector('.bag');
  var inv = document.querySelector('.inv');
  var invSlots = inv && inv.querySelector('.inv__slots');
  var invSay = inv && inv.querySelector('.inv__say');
  var dlgMsg = document.querySelector('[data-msg]');
  var dlgInv = document.querySelector('.dialog__inv');
  var dlgSay = document.querySelector('[data-say]');

  function save() { try { localStorage.setItem(KEY, JSON.stringify(order)); } catch (e) {} }
  function message() {
    if (!order.length) return document.querySelector('[data-msg-empty]').getAttribute('data-msg-empty');
    var lines = order.map(function (o) { return '- ' + (byId[o.id].getAttribute('data-line') || o.n); });
    return 'Hola, vi la web y quiero:\n' + lines.join('\n') + '\n¿Me pasás precio y para cuándo estaría?';
  }
  function waHref() { return WA + encodeURIComponent(message()); }
  function thumb(o) { var it = byId[o.id]; var px = it && it.querySelector('.shot .px'); return px ? px.getAttribute('src') : ''; }

  function render(added) {
    var n = order.length;
    if (bag) bag.textContent = n;
    if (bagBtn) bagBtn.setAttribute('aria-label', n ? 'Tu pedido: ' + n + (n === 1 ? ' cosa' : ' cosas') : 'Tu pedido, vacío');
    document.querySelectorAll('.item .pick').forEach(function (b) {
      var id = b.closest('.item').getAttribute('data-id');
      var on = order.some(function (o) { return o.id === id; });
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      b.querySelector('span').textContent = on ? 'En tu pedido' : 'Lo quiero';
    });
    if (inv) {
      inv.classList.toggle('is-on', n > 0);
      invSlots.innerHTML = '';
      order.slice(-6).forEach(function (o) {
        var s = document.createElement('span'); s.className = 'slot' + (added === o.id ? ' is-new' : '');
        var im = document.createElement('img'); im.src = thumb(o); im.alt = ''; s.appendChild(im); invSlots.appendChild(s);
      });
      invSay.innerHTML = '<b>' + n + (n === 1 ? ' cosa' : ' cosas') + ' en tu pedido</b><span>' + order.map(function (o) { return o.n; }).join(', ') + '</span>';
    }
    if (dlgInv) {
      dlgInv.innerHTML = '';
      order.forEach(function (o) {
        var b = document.createElement('button'); b.type = 'button';
        b.setAttribute('aria-label', 'Sacar ' + o.n + ' del pedido');
        var im = document.createElement('img'); im.src = thumb(o); im.alt = ''; b.appendChild(im);
        b.addEventListener('click', function () { toggle(o.id); });
        dlgInv.appendChild(b);
      });
    }
    if (dlgSay) dlgSay.textContent = n ? dlgSay.getAttribute('data-full') : dlgSay.getAttribute('data-empty');
    document.querySelectorAll('[data-send]').forEach(function (sp) { sp.textContent = n ? 'Mandar pedido por WhatsApp' : 'Escribime por WhatsApp'; });
    document.querySelectorAll('[data-wa-order]').forEach(function (a) { a.href = waHref(); });
    type();
    if (typeof syncPeek === 'function') syncPeek();
    fitHome();
  }
  // on a phone the little temple at the close steps aside if the order grows into it
  function fitHome() {
    var c = document.querySelector('.counter__copy'), st = document.querySelector('.counter [data-sc-stage]');
    if (!c || !st) return;
    var tight = innerWidth <= 900 && c.getBoundingClientRect().bottom + 16 > st.getBoundingClientRect().bottom - 252;
    document.getElementById('pedido').classList.toggle('is-tight', tight);
  }
  addEventListener('resize', fitHome);
  function toggle(id, fromEl) {
    var i = -1;
    order.forEach(function (o, j) { if (o.id === id) i = j; });
    var added = null;
    if (i > -1) order.splice(i, 1);
    else { order.push({ id: id, n: byId[id].getAttribute('data-name') }); added = id; }
    save(); render(added);
    if (added) fly(fromEl, id);
    announce(added ? byId[id].getAttribute('data-name') + ' está en tu pedido.' : 'Lo saqué del pedido.');
  }
  var live = document.querySelector('[data-live]');
  function announce(t) { if (live) { live.textContent = ''; setTimeout(function () { live.textContent = t; }, 30); } }

  document.querySelectorAll('.item .pick').forEach(function (b) {
    b.addEventListener('click', function () { var it = b.closest('.item'); toggle(it.getAttribute('data-id'), it.querySelector('.shot')); });
  });
  // ------------------------------------------------- the peek: an item window
  var peek = document.querySelector('.peek');
  var peekCur = null;
  var peekPick = peek && peek.querySelector('[data-peek-pick]');
  function syncPeek() {
    if (!peekCur || !peekPick) return;
    var id = peekCur.getAttribute('data-id');
    var on = order.some(function (o) { return o.id === id; });
    peekPick.setAttribute('aria-pressed', on ? 'true' : 'false');
    peekPick.querySelector('span').textContent = on ? 'En tu pedido' : 'Lo quiero';
  }
  function openPeek(it) {
    if (!peek) return;
    var swap = peek.open && peekCur !== it;
    peekCur = it;
    var full = it.querySelector('.full');
    peek.querySelector('[data-peek-where]').textContent = it.closest('.shelf').getAttribute('data-name');
    var img = peek.querySelector('[data-peek-img]');
    img.src = full.getAttribute('src'); img.alt = full.getAttribute('alt');
    peek.querySelector('[data-peek-name]').textContent = it.getAttribute('data-name');
    peek.querySelector('[data-peek-line]').innerHTML = it.querySelector('p').innerHTML;
    peek.querySelector('[data-peek-tag]').hidden = !it.hasAttribute('data-mine');
    syncPeek();
    if (!peek.open) {
      if (typeof peek.showModal === 'function') peek.showModal(); else peek.setAttribute('open', '');
    } else if (swap && !reduce) {
      var s = peek.querySelector('.peek__shot'); s.classList.remove('is-swap'); void s.offsetWidth; s.classList.add('is-swap');
    }
  }
  function stepPeek(d) {
    if (!peekCur) return;
    var list = Array.prototype.slice.call(peekCur.closest('.grid').children);
    var i = list.indexOf(peekCur);
    openPeek(list[(i + d + list.length) % list.length]);
  }
  function closePeek() { if (peek && peek.open) { if (typeof peek.close === 'function') peek.close(); else peek.removeAttribute('open'); } }
  if (peek) {
    document.querySelectorAll('.item .shot').forEach(function (s) {
      s.addEventListener('click', function () { openPeek(s.closest('.item')); });
    });
    peek.querySelector('[data-peek-close]').addEventListener('click', closePeek);
    peek.querySelectorAll('[data-peek-go]').forEach(function (b) {
      b.addEventListener('click', function () { stepPeek(+b.getAttribute('data-peek-go')); });
    });
    peek.addEventListener('click', function (e) { if (e.target === peek) closePeek(); });
    peek.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); stepPeek(1); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); stepPeek(-1); }
    });
    peekPick.addEventListener('click', function () {
      if (peekCur) toggle(peekCur.getAttribute('data-id'), peek.querySelector('.peek__shot'));
    });
    // swipe on a phone
    var sx = null;
    peek.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    peek.addEventListener('touchend', function (e) {
      if (sx === null) return; var dx = e.changedTouches[0].clientX - sx; sx = null;
      if (Math.abs(dx) > 60) stepPeek(dx < 0 ? 1 : -1);
    });
  }

  // ------------------------------------------------- the pick flies to the bag
  function bump() { if (!bagBtn || reduce) return; bagBtn.classList.remove('is-bump'); void bagBtn.offsetWidth; bagBtn.classList.add('is-bump'); }
  function fly(fromEl, id) {
    if (reduce || !bagBtn || !fromEl || !fromEl.animate) { bump(); return; }
    var a = fromEl.getBoundingClientRect(), b = bagBtn.getBoundingClientRect();
    var f = document.createElement('img'); f.className = 'flyer'; f.src = thumb({ id: id }); f.alt = '';
    var host = (peek && peek.open) ? peek : document.body;
    host.appendChild(f);
    var x0 = a.left + a.width / 2 - 24, y0 = a.top + a.height / 2 - 24;
    var x1 = b.left + b.width / 2 - 24, y1 = b.top + b.height / 2 - 24;
    var cx = (x0 + x1) / 2, cy = Math.max(8, Math.min(y0, y1) - 140);
    var frames = [];
    for (var k = 0; k <= 8; k++) {
      var t = k / 8, u = 1 - t;
      var x = u * u * x0 + 2 * u * t * cx + t * t * x1, y = u * u * y0 + 2 * u * t * cy + t * t * y1;
      frames.push({ transform: 'translate(' + Math.round(x) + 'px,' + Math.round(y) + 'px) scale(' + (1 - t * 0.55).toFixed(2) + ')' });
    }
    var anim = f.animate(frames, { duration: 640, easing: 'steps(16, end)', fill: 'forwards' });
    anim.onfinish = function () {
      f.remove(); bump();
      var p = document.createElement('span'); p.className = 'plus'; p.textContent = '+1';
      p.style.left = Math.round(b.left + b.width / 2 - 14) + 'px'; p.style.top = Math.round(b.bottom + 6) + 'px';
      host.appendChild(p); setTimeout(function () { p.remove(); }, 760);
    };
  }


  // the dialog types the message, like a shopkeeper talking
  var typed = '', typing = null;
  function type() {
    if (!dlgMsg) return;
    var full = message();
    if (reduce || !counterSeen) { dlgMsg.textContent = full; typed = full; fitHome(); return; }
    var keep = 0;
    while (keep < typed.length && keep < full.length && typed[keep] === full[keep]) keep++;
    typed = full.slice(0, keep);
    clearInterval(typing);
    typing = setInterval(function () {
      if (typed.length >= full.length) { clearInterval(typing); dlgMsg.textContent = full; fitHome(); return; }
      typed = full.slice(0, typed.length + 2);
      dlgMsg.innerHTML = '';
      dlgMsg.appendChild(document.createTextNode(typed));
      var c = document.createElement('span'); c.className = 'caret'; c.setAttribute('aria-hidden', 'true'); dlgMsg.appendChild(c);
    }, 24);
  }
  var counterSeen = false;
  var counter = document.getElementById('pedido');
  if (counter && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (inv) inv.classList.toggle('is-parked', e.isIntersecting);
        if (e.isIntersecting && !counterSeen) { counterSeen = true; typed = ''; type(); }
      });
    }, { threshold: 0.35 }).observe(counter);
  }
  render(null);

  // ------------------------------------------------------- HUD print bar
  var bar = document.querySelector('.hud__bar i');
  function hudBar() {
    if (!bar) return;
    var max = document.documentElement.scrollHeight - innerHeight;
    var k = max > 0 ? scrollY / max : 0;
    bar.style.width = (Math.round(k * 50) * 2) + '%';
  }

  function visible(el) { var r = el.getBoundingClientRect(); return r.bottom > 0 && r.top < innerHeight; }
  function frame(t) {
    drawers.forEach(function (d) { if (visible(d.el)) d.fn(t); });
    hudBar(); spy();
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
  if (reduce) drawers.forEach(function (d) { d.fn(0); });
  addEventListener('resize', function () { var n = setPx(); if (n !== PX) { PX = n; api.layout(); } });

  // ------------------------------------------------------- copy the number
  document.querySelectorAll('[data-copy]').forEach(function (b) {
    var label = b.textContent;
    b.addEventListener('click', function () {
      var v = b.getAttribute('data-copy');
      var done = function () { b.textContent = 'Copiado'; setTimeout(function () { b.textContent = label; }, 1800); };
      if (navigator.clipboard) navigator.clipboard.writeText(v).then(done, function () { selectPhone(b); });
      else selectPhone(b);
    });
  });
  function selectPhone(b) {
    var s = b.parentNode.querySelector('.phone'); if (!s) return;
    var r = document.createRange(); r.selectNodeContents(s); var sel = getSelection(); sel.removeAllRanges(); sel.addRange(r);
  }
})();
