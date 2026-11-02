"""Generate the missing sheets of a pixel-reel library with the Gemini API (google-genai SDK).

  python3 gemini_generate.py LIBRARY/sprites.json [--reel REEL/reel.json] [--gate N] [--only a.png,b.png]
                             [--variants 3] [--max-images 12] [--fix-rounds 1] [--image-size 1K] [--model ID]
                             [--dry-run] [--regen] [--list-models] [--approve SHEET=N ...]

What it does, in approval order (gates):
  * reads the sheet plan (prmanifest.py) and the exact prompt + attachments that gen_prompts.py writes;
  * generates only sheets that are not yet approved in LIBRARY/sheets/, never more than --max-images images per run;
  * asks for --variants variants per sheet, saves them in LIBRARY/candidates/<sheet>/vN.png, scores them with qc.py
    and draws candidates/<sheet>/contact.png;
  * gates 2-4 (model sheets, master scene, empty background) are NEVER approved automatically: it stops and waits
    for `--approve SHEET=N`; gate 5 approves the best variant if it passes QC, otherwise it re-asks once with the
    corrections from references/gemini.md and, if still failing, leaves the contact sheet for a person;
  * retries with growing waits on rate limits and server errors;
  * appends every request and decision to LIBRARY/generation_log.jsonl.

The API key is read by the SDK from GEMINI_API_KEY in the environment. It is never printed, logged or written:
every message that could echo it goes through redact().
"""
import argparse, datetime, hashlib, io, json, os, shutil, sys, time
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prmanifest as M
import gen_prompts as GP
import qc as QC

PREFERRED = ["gemini-3-pro-image", "gemini-3-pro-image-preview", "gemini-3.1-flash-image-preview", "gemini-2.5-flash-image", "gemini-2.5-flash-image-preview"]
AUTO_GATES = {5}
_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or ""


def redact(s):
    s = str(s)
    return s.replace(_KEY, "***") if _KEY else s


def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


class Log:
    def __init__(self, path): self.path = path
    def __call__(self, **e):
        e = {"ts": now(), **e}
        with open(self.path, "a") as f: f.write(redact(json.dumps(e, ensure_ascii=False)) + "\n")


# ------------------------------------------------------------------ attachments
def find_file(rel, lib):
    for base in (lib["_dir"], os.path.join(lib["_dir"], ".."), os.path.join(lib["_dir"], "..", "..")):
        p = os.path.normpath(os.path.join(base, rel))
        if os.path.exists(p): return p
    return None


def resolve(attach, lib, sheets):
    """-> (paths, missing_required). Optional attachments (descriptions with ':') are skipped when absent."""
    paths, missing = [], []
    for a in attach:
        name = a.split(" (")[0].strip()
        if ":" in name and not name.endswith(".png"): continue          # "mate: el sprite del objeto si ya existe"
        if name == "palette.png":
            p = os.path.join(lib["_dir"], "palette.png")
            if not os.path.exists(p): GP.palette_png(lib, p)
            paths.append(p)
        elif name.endswith(".png"):
            p = os.path.join(sheets, name)
            (paths if os.path.exists(p) else missing).append(p if os.path.exists(p) else name)
        else:
            p = find_file(name, lib)
            (paths if p else missing).append(p or name)
    return paths, missing


def load_ref(p):
    im = Image.open(p)
    return im.convert("RGB") if im.mode not in ("RGB", "RGBA") else im


# ------------------------------------------------------------------ Gemini
def client():
    from google import genai
    if not _KEY:  # network secret: the egress proxy injects x-goog-api-key, the SDK only needs a placeholder
        os.environ["GEMINI_API_KEY"] = "proxy-injected"
    return genai.Client()


def image_models(cl):
    out = []
    for m in cl.models.list():
        name = (m.name or "").split("/")[-1]
        acts = getattr(m, "supported_actions", None) or []
        if "image" in name and (not acts or "generateContent" in acts): out.append(name)
    return sorted(set(out))


def pick_model(cl, wanted):
    if wanted: return wanted
    avail = image_models(cl)
    for p in PREFERRED:
        if p in avail: return p
    if avail: return avail[0]
    sys.exit("La clave no tiene ningún modelo de imagen disponible (models.list).")


def generate(cl, model, req, refs, extra, size, retries, log):
    from google.genai import types, errors
    cfg = types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"],
                                      image_config=types.ImageConfig(aspect_ratio=req["aspect"], image_size=size))
    contents = [req["body"] + (("\n\nCORRECTIONS (the previous attempt failed quality control):\n- " + "\n- ".join(extra)) if extra else "")]
    contents += [load_ref(p) for p in refs]
    wait = 8
    for attempt in range(retries + 1):
        try:
            resp = cl.models.generate_content(model=model, contents=contents, config=cfg)
            text, img = [], None
            for cand in (resp.candidates or []):
                for part in (getattr(cand.content, "parts", None) or []):
                    if getattr(part, "inline_data", None) and part.inline_data.data and img is None:
                        img = Image.open(io.BytesIO(part.inline_data.data)); img.load()
                    elif getattr(part, "text", None): text.append(part.text)
            return img, redact(" ".join(text))[:400], contents[0]
        except errors.APIError as e:
            code = getattr(e, "code", None)
            if code == 429 and "limit: 0" in str(e):
                raise RuntimeError("cuota 0 para este modelo: la clave no tiene generación de imágenes habilitada (plan gratuito); "
                                   "activar facturación en el proyecto de Google AI Studio")
            if code in (429, 500, 502, 503, 504) and attempt < retries:
                log(event="retry", model=model, sheet=req["sheet"], code=code, wait_s=wait)
                print(f"  límite o error {code}: espero {wait} s"); time.sleep(wait); wait *= 2; continue
            raise RuntimeError(redact(f"{code}: {getattr(e, 'message', e)}"))
    raise RuntimeError("sin respuesta")


# ------------------------------------------------------------------ contact sheet
def contact(folder, variants, sheet):
    if not variants: return None
    th = 360; ims = []
    for v in variants:
        im = Image.open(v["path"]).convert("RGB"); r = th / im.height; ims.append(im.resize((max(1, int(im.width * r)), th), Image.NEAREST))
    W = sum(i.width for i in ims) + 12 * (len(ims) + 1); out = Image.new("RGB", (W, th + 74), (40, 40, 48)); d = ImageDraw.Draw(out)
    d.text((12, 6), sheet, fill=(255, 255, 255)); x = 12
    for v, im in zip(variants, ims):
        out.paste(im, (x, 24)); q = v["qc"]
        d.text((x, th + 30), f"v{v['n']}  score {q['score']}  {'OK' if q['pass'] else 'NO'}", fill=(120, 230, 120) if q["pass"] else (240, 130, 120))
        d.text((x, th + 46), "; ".join(q["issues"])[:70], fill=(220, 220, 220)); x += im.width + 12
    p = os.path.join(folder, "contact.png"); out.save(p); return p


def existing_variants(folder):
    if not os.path.isdir(folder): return []
    return sorted(int(f[1:-4]) for f in os.listdir(folder) if f.startswith("v") and f.endswith(".png") and f[1:-4].isdigit())


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("library"); ap.add_argument("--reel"); ap.add_argument("--sheets"); ap.add_argument("--candidates")
    ap.add_argument("--gate", type=int); ap.add_argument("--only"); ap.add_argument("--variants", type=int, default=3)
    ap.add_argument("--max-images", type=int, default=12); ap.add_argument("--fix-rounds", type=int, default=1)
    ap.add_argument("--image-size", default="1K"); ap.add_argument("--model"); ap.add_argument("--retries", type=int, default=5)
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--regen", action="store_true")
    ap.add_argument("--list-models", action="store_true"); ap.add_argument("--approve", action="append", default=[])
    a = ap.parse_args()
    lib, reel = M.load(a.library, a.reel)
    sheets = a.sheets or os.path.join(lib["_dir"], "sheets"); cands = a.candidates or os.path.join(lib["_dir"], "candidates")
    os.makedirs(sheets, exist_ok=True); os.makedirs(cands, exist_ok=True)
    log = Log(os.path.join(lib["_dir"], "generation_log.jsonl"))

    # manual approvals (no API needed)
    for ap_ in a.approve:
        name, n = ap_.split("="); folder = os.path.join(cands, name[:-4]); src = os.path.join(folder, f"v{int(n)}.png")
        if not os.path.exists(src): sys.exit(f"no existe {src}")
        shutil.copy(src, os.path.join(sheets, name)); log(event="approve", sheet=name, variant=int(n), by="person")
        print(f"aprobada {name} (v{n})")
    if a.approve and not (a.gate or a.only or a.list_models): return

    plan = [s for s in M.plan(lib, reel) if s["needed"]]
    reqs = {sh["name"]: req for sh, req in GP.requests(lib, reel, plan)}
    todo = [s for s in plan if not os.path.exists(os.path.join(sheets, s["name"]))]
    if a.gate: todo = [s for s in todo if s["gate"] == a.gate]
    if a.only: only = set(x.strip() for x in a.only.split(",")); todo = [s for s in todo if s["name"] in only]
    todo.sort(key=lambda s: s["gate"])

    cl = model = None
    if not a.dry_run or a.list_models:
        cl = client(); model = pick_model(cl, a.model or os.environ.get("PIXEL_REEL_IMAGE_MODEL"))
        if a.list_models: print("modelos de imagen:", ", ".join(image_models(cl)), "| elegido:", model); return
        print("modelo:", model)

    used = 0; summary = []
    for sh in todo:
        req = reqs[sh["name"]]; folder = os.path.join(cands, sh["name"][:-4])
        refs, missing = resolve(req["attach"], lib, sheets)
        if missing:
            summary.append((sh["name"], "bloqueada: falta aprobar " + ", ".join(os.path.basename(m) for m in missing))); continue
        have = existing_variants(folder)
        if have and not a.regen and sh["gate"] not in AUTO_GATES:
            summary.append((sh["name"], f"esperando elección: {os.path.join(folder, 'contact.png')}")); continue
        if a.dry_run:
            summary.append((sh["name"], f"generaría {a.variants} variantes (gate {sh['gate']}) con {len(refs)} adjuntos")); used += a.variants; continue
        if used >= a.max_images: summary.append((sh["name"], "sin presupuesto en esta corrida (--max-images)")); continue
        os.makedirs(folder, exist_ok=True)
        results = [dict(n=n, path=os.path.join(folder, f"v{n}.png"), qc=QC.score(lib, reel, sh, Image.open(os.path.join(folder, f"v{n}.png"))))
                   for n in have] if (have and not a.regen) else []
        extra = []
        for rnd in range(a.fix_rounds + 1):
            for _ in range(a.variants):
                if used >= a.max_images: break
                n = max([r["n"] for r in results] + existing_variants(folder) + [0]) + 1
                try:
                    img, text, prompt = generate(cl, model, req, refs, extra, a.image_size, a.retries, log); used += 1
                except Exception as e:  # noqa: BLE001 - logged and reported, never with the key
                    used += 1; log(event="error", sheet=sh["name"], gate=sh["gate"], model=model, error=redact(e)); print("  error:", redact(e)); break
                if img is None:
                    log(event="no_image", sheet=sh["name"], model=model, response_text=text); print("  sin imagen:", text[:120]); continue
                p = os.path.join(folder, f"v{n}.png"); img.convert("RGB").save(p)
                q = QC.score(lib, reel, sh, Image.open(p)); results.append(dict(n=n, path=p, qc=q))
                log(event="generate", sheet=sh["name"], gate=sh["gate"], model=model, variant=n, round=rnd,
                    prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(), prompt=prompt,
                    attachments=[os.path.relpath(r, lib["_dir"]) for r in refs], aspect=req["aspect"],
                    image_size=a.image_size, size=list(img.size), qc=q, response_text=text)
                print(f"  {sh['name']} v{n}: score {q['score']} {'OK' if q['pass'] else 'NO'} {'; '.join(q['issues'])}")
            passing = [r for r in results if r["qc"]["pass"]]
            if passing or sh["gate"] not in AUTO_GATES or used >= a.max_images or not results or rnd == a.fix_rounds: break
            best = max(results, key=lambda r: r["qc"]["score"]); extra = best["qc"]["fixes"]
            log(event="qc_fail_reask", sheet=sh["name"], corrections=extra)
        cpath = contact(folder, results, sh["name"])
        json.dump([{k: v for k, v in r.items() if k != "path"} for r in results], open(os.path.join(folder, "qc.json"), "w"), indent=1, ensure_ascii=False)
        passing = sorted([r for r in results if r["qc"]["pass"]], key=lambda r: -r["qc"]["score"])
        if sh["gate"] in AUTO_GATES and passing:
            shutil.copy(passing[0]["path"], os.path.join(sheets, sh["name"]))
            log(event="approve", sheet=sh["name"], variant=passing[0]["n"], by="auto", qc=passing[0]["qc"])
            summary.append((sh["name"], f"aprobada automáticamente v{passing[0]['n']} (score {passing[0]['qc']['score']}); revisar {cpath}"))
        else:
            summary.append((sh["name"], f"esperando elección: {cpath}" if results else "sin variantes"))
    print(f"\nimágenes pedidas en esta corrida: {used} (tope {a.max_images})" + (" [simulación]" if a.dry_run else ""))
    for name, st in summary: print(f"- {name}: {st}")


if __name__ == "__main__":
    main()
