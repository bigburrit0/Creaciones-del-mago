"""Quality control of an image-model sheet, using the same pixel logic as slice_sheets.py.

score(lib, reel, sheet_plan_entry, PIL_image) -> {"score": 0-100, "pass": bool, "issues": [...], "fixes": [...], "metrics": {...}}

Hard failures (pass = False): background not flat magenta, an expected frame is empty, content in cells that must stay
empty, a sprite touching its cell border, height more than 20 % off, anchor more than 16 art px off.
"fixes" are the re-ask sentences from references/gemini.md that address each issue.
"""
import os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prmanifest as M
from slice_sheets import bg_mask, to_art, cell_metrics

FIX = {
    "bg": "No drop shadow, no ground shadow, no gradient: the background is one flat colour, pure magenta #FF00FF, everywhere outside the sprites.",
    "empty": "Draw exactly {n} frames, one per cell, in cells 1 to {n}; every one of those cells contains the full subject.",
    "extra": "Cells {cells} must stay plain magenta: nothing drawn there.",
    "border": "Keep every sprite fully inside its own cell with at least 32 image pixels of magenta margin on every side; nothing crosses into another cell.",
    "height": "The subject has exactly the same height in every cell: {h} image pixels from the top of the head (or hat) to the soles of the feet.",
    "anchor": "Feet on one baseline 16 image pixels above the bottom edge of each cell, horizontally centred in the cell.",
    "palette": "Use only the colours of the attached palette image; no new colours.",
    "blocky": "Crisp pixel art: every art pixel is an exact 4x4 block of image pixels, no blur, no painterly shading, no anti-aliasing.",
    "size": "Output exactly a square 1024x1024 image.",
    "magenta_plate": "This is a full scene: no magenta anywhere, fill the whole canvas.",
}


def palette_distance(rgb_pixels, pal):
    if not len(rgb_pixels) or not pal: return 0.0
    P = np.array([M.hex2rgb(h) for h in pal], np.float32)
    px = rgb_pixels[np.random.default_rng(0).choice(len(rgb_pixels), min(4000, len(rgb_pixels)), replace=False)].astype(np.float32)
    return float(np.sqrt(((px[:, None, :] - P[None]) ** 2).sum(-1)).min(1).mean())


def blockiness(img, s):
    """mean in-block variance at the best grid phase (low = clean s x s pixel blocks)"""
    a = np.asarray(img.convert("RGB")).astype(np.float32)[:512, :512]
    best = 1e9
    for py in range(s):
        for px in range(s):
            sub = a[py:py + (a.shape[0] - s) // s * s, px:px + (a.shape[1] - s) // s * s]
            h, w = sub.shape[0] // s, sub.shape[1] // s
            best = min(best, float(sub.reshape(h, s, w, s, 3).var(axis=(1, 3)).mean()))
    return best


def score(lib, reel, sh, img):
    S = lib["grid"]["scale"]; pal = M.palette(lib); issues, fixes, m = [], [], {}
    img = img.convert("RGB"); a = np.asarray(img)
    if sh["fmt"] == "plate":
        w, h = img.size; m["aspect"] = round(w / h, 3)
        if abs(w / h - 9 / 16) > 0.03: issues.append(f"aspecto {w}x{h} no es 9:16")
        mag = float(bg_mask(a).mean()); m["magenta"] = round(mag, 4)
        if mag > 0.01: issues.append("hay magenta en el fondo"); fixes.append(FIX["magenta_plate"])
        m["palette_dist"] = round(palette_distance(a.reshape(-1, 3), pal), 1)
        if m["palette_dist"] > 45: issues.append(f"colores lejos de la paleta ({m['palette_dist']})"); fixes.append(FIX["palette"])
        sc = max(0, 100 - 25 * len(issues))
        return {"score": sc, "pass": not issues, "issues": issues, "fixes": fixes, "metrics": m}

    f = lib["sheet_formats"][sh["fmt"]]; gx, gy = f["grid"]; ca = f["cell_art"]; ax, ay = f["anchor_art"]
    expect = (gx * ca * S, gy * ca * S)
    if img.size != expect:
        m["size"] = list(img.size); issues.append(f"tamaño {img.size[0]}x{img.size[1]}"); fixes.append(FIX["size"])
        img = img.resize(expect, Image.NEAREST); a = np.asarray(img)
    bg = bg_mask(a)
    # background: border band of every cell should be magenta
    cw = expect[0] // gx; band = []
    for gyi in range(gy):
        for gxi in range(gx):
            c = bg[gyi * cw:(gyi + 1) * cw, gxi * cw:(gxi + 1) * cw]
            band.append(np.concatenate([c[:8].ravel(), c[-8:].ravel(), c[:, :8].ravel(), c[:, -8:].ravel()]).mean())
    m["bg_border"] = round(float(np.mean(band)), 3)
    fringe = (a[..., 0].astype(int) > 140) & (a[..., 2].astype(int) > 140) & (a[..., 1].astype(int) < 170) & ~bg
    m["fringe"] = round(float(fringe.mean()), 4)
    if m["bg_border"] < 0.93 or m["fringe"] > 0.02: issues.append("fondo no es magenta plano"); fixes.append(FIX["bg"])
    m["blockiness"] = round(blockiness(img, S), 1)
    if m["blockiness"] > 120: issues.append("píxeles borrosos"); fixes.append(FIX["blocky"])
    art = to_art(img, S, gx * ca, gy * ca)
    cells = [art[(i // gx) * ca:(i // gx + 1) * ca, (i % gx) * ca:(i % gx + 1) * ca] for i in range(gx * gy)]
    if sh["kind"] == "rows":
        n_per_row = [len(r["poses"]) for r in sh["rows"]]
        exp = set(r * gx + c for r, n in enumerate(n_per_row) for c in range(n))
    else:
        n = len(sh["cells"]) if "cells" in sh else len(sh["items"]); exp = set(range(n))
    mets = [cell_metrics(c) for c in cells]
    empty = [i + 1 for i in sorted(exp) if mets[i] is None]
    extra = [i + 1 for i in range(gx * gy) if i not in exp and mets[i] and mets[i]["area"] > 30]
    touch = [i + 1 for i in sorted(exp) if mets[i] and mets[i]["touches"]]
    if empty: issues.append(f"celdas vacías {empty}"); fixes.append(FIX["empty"].format(n=len(exp)))
    if extra: issues.append(f"dibujo en celdas que van vacías {extra}"); fixes.append(FIX["extra"].format(cells=", ".join(map(str, extra))))
    if touch: issues.append(f"sprite toca el borde en {touch}"); fixes.append(FIX["border"])
    ok = [mets[i] for i in sorted(exp) if mets[i]]
    opaque = art[..., :3][art[..., 3] > 0]
    m["palette_dist"] = round(palette_distance(opaque, pal), 1)
    if m["palette_dist"] > 40: issues.append(f"colores lejos de la paleta ({m['palette_dist']})"); fixes.append(FIX["palette"])
    if sh["kind"] in ("model", "anim") and ok:
        H = M.characters(lib, reel)[sh["owner"]]["model"]["height_px"]
        hs = [mm["base"] - mm["top"] + 1 for mm in ok]
        ref = hs[0] if sh["kind"] == "model" else float(np.median(hs))
        m["height"] = int(ref); m["height_target"] = H
        tol = 0.2 if sh["kind"] == "model" else 0.3
        if abs(ref - H) > H * tol: issues.append(f"altura {int(ref)} px de arte, se pidió {H}"); fixes.append(FIX["height"].format(h=H * S))
        poses = " ".join(sh["cells"]).lower()
        varies = any(w in poses for w in ("sit", "jump", "crouch", "squash", "bend", "bow", "fall", "apex", "landing"))
        if sh["kind"] == "anim" and max(hs) - min(hs) > H * 0.35 and not varies:
            issues.append("variación de altura entre cuadros (aviso)"); fixes.append(FIX["height"].format(h=H * S))
    if sh["kind"] in ("model", "anim", "object") and ok:
        dx = ax - float(np.median([mm["cx"] for mm in ok])); dy = ay - float(np.median([mm["base"] for mm in ok]))
        m["anchor_off"] = [round(dx, 1), round(dy, 1)]
        if abs(dx) > 16 or abs(dy) > 16: issues.append(f"ancla corrida {m['anchor_off']}"); fixes.append(FIX["anchor"])
    hard = bool(empty or extra or touch or any(i.startswith(("fondo", "altura", "ancla", "tamaño")) for i in issues))
    sc = 100 - 20 * len(empty) - 15 * len(extra) - 10 * len(touch) - min(20, max(0, m["palette_dist"] - 20)) \
        - (15 if "fondo no es magenta plano" in issues else 0) - (10 if "píxeles borrosos" in issues else 0) \
        - (15 if any(i.startswith("altura") for i in issues) else 0) - (10 if any(i.startswith("ancla") for i in issues) else 0)
    sc = int(max(0, min(100, sc)))
    return {"score": sc, "pass": (not hard) and sc >= 70, "issues": issues, "fixes": list(dict.fromkeys(fixes)), "metrics": m}


# ------------------------------------------------------------------ normalisation of real image-model output
def pixel_pitch(img):
    """size of one art pixel in image pixels, from the autocorrelation of colour edges (both axes)"""
    a = np.asarray(img.convert("L")).astype(np.float32); best = []
    for g in (np.abs(np.diff(a, axis=1)).sum(0), np.abs(np.diff(a, axis=0)).sum(1)):
        g = g - g.mean(); ac = np.correlate(g, g, "full")[len(g) - 1:]; ac /= max(ac[0], 1e-6)
        best.append(int(np.arange(3, 40)[np.argmax(ac[3:40])]))
    return int(round(float(np.median(best))))


def strip_grid_lines(a):
    """paint magenta any full-length dark line (cell separators the model sometimes draws)"""
    a = a.copy(); dark = a.astype(int).sum(2) < 200
    for axis in (0, 1):
        frac = dark.mean(axis=1 - axis)
        for i in np.where(frac > 0.6)[0]:
            if axis == 0: a[i, :] = (255, 0, 255)
            else: a[:, i] = (255, 0, 255)
    return a


def normalize_sheet(lib, sh, img):
    """Rebuild any-size model output as the canonical sheet (grid x cell_art x scale), keeping its art pixels.
    Returns (normalized PIL image, info dict). Plates are only resized to 9:16 at x scale."""
    S = lib["grid"]["scale"]
    if sh["fmt"] == "plate":
        W, H = lib["grid"]["art_canvas"]; return img.convert("RGB").resize((W * S, H * S), Image.BOX), {"plate": True}
    f = lib["sheet_formats"][sh["fmt"]]; gx, gy = f["grid"]; ca = f["cell_art"]
    img = img.convert("RGB"); p = pixel_pitch(img)
    A = int(round(img.width / p)); Ah = int(round(img.height / p))
    img = img.resize((A * p, Ah * p), Image.NEAREST)
    a = strip_grid_lines(np.asarray(img))
    art = to_art(Image.fromarray(a), p, A, Ah)                 # RGBA art at the model's own resolution
    cw, ch = A // gx, Ah // gy; out = np.zeros((gy * ca, gx * ca, 4), np.uint8)
    for gyi in range(gy):
        for gxi in range(gx):
            c = art[gyi * ch:(gyi + 1) * ch, gxi * cw:(gxi + 1) * cw]
            al = c[..., 3] > 0
            if al.sum() < 6: continue
            ys, xs = np.where(al); c = c[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
            h, w = c.shape[:2]
            if h > ca - 4 or w > ca - 4:                         # too big for our cell: integer shrink is not possible, crop safely
                c = c[max(0, h - (ca - 4)):, max(0, (w - (ca - 4)) // 2):][: ca - 4, : ca - 4]; h, w = c.shape[:2]
            ax, ay = f["anchor_art"]
            y0 = max(0, min(ca - h, ay + 1 - h)); x0 = max(0, min(ca - w, ax - w // 2))
            out[gyi * ca + y0:gyi * ca + y0 + h, gxi * ca + x0:gxi * ca + x0 + w] = c
    rgb = np.where(out[..., 3:] > 0, out[..., :3], np.array([255, 0, 255], np.uint8))
    norm = Image.fromarray(rgb.astype(np.uint8)).resize((gx * ca * S, gy * ca * S), Image.NEAREST)
    return norm, {"pitch": p, "model_cell_art": [cw, ch]}
