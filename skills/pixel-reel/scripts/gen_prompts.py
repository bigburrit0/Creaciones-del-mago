"""Write the image-model prompts (PROMPTS.md), a readable catalogue (CATALOGO.md) and palette.png from a
sprite library manifest, optionally filtered to what one reel needs.

  python3 gen_prompts.py LIBRARY/sprites.json OUT_DIR [--reel REEL/reel.json] [--only-missing SHEETS_DIR]

The manifest is the source of truth: edit it and regenerate; never hand-edit PROMPTS.md.
"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prmanifest as M

DIRS = {"S": "facing the camera in a front three-quarter view", "E": "seen from the side, facing RIGHT",
        "N": "seen from behind, facing away from the camera", "W": "seen from the side, facing LEFT",
        "S>N": "turning from facing the camera to facing away"}
MODES = {"loop": "looping", "once": "played once", "hold": "played once, the last frame is held", "states": "separate states", "static": "a single still"}


def style_block(lib):
    st = lib.get("project", {}).get("style", {})
    outline = st.get("outline", "#150A34"); s = lib["grid"]["scale"]
    txt = (f"STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, {st.get('view', 'top-down three-quarter view like a 1990s farming RPG')}. "
           f"Hard square pixels, every art pixel is a {s}x{s} block of image pixels. No anti-aliasing, no blur, no gradients, "
           f"no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a 1-art-pixel "
           f"dark outline {outline}. Light comes from the {st.get('light', 'upper-left, shadows fall to the lower-right')}, "
           f"3 tones per material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.")
    if st.get("extra"): txt += " " + st["extra"]
    return txt


def sheet_block(lib, fmt):
    f = lib["sheet_formats"][fmt]; s = lib["grid"]["scale"]
    w, h = f["image"]; gx, gy = f["grid"]; cw = w // gx
    base = (f"SHEET: {w}x{h} PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, "
            f"no floor, no grid lines, no borders. ")
    if fmt == "small":
        return base + (f"A {gx}x{gy} grid of equal {cw}x{cw} cells. Each ROW is one animation of up to {gx} frames, read left to "
                       f"right; unused cells stay plain magenta. Every subject is centred in its cell, keeps the same size along its "
                       f"row and fits inside {cw // 2}x{cw // 2} image pixels.")
    if fmt == "item":
        m = f.get("item_max_art", 40) * s
        return base + (f"A {gx}x{gy} grid of equal {cw}x{cw} cells, one object per cell, each object at most {m}x{m} image pixels, "
                       f"centred and resting on an invisible baseline {(f['cell_art'] - f['anchor_art'][1]) * s} image pixels above the "
                       f"bottom of its cell. All objects drawn at the same pixel scale.")
    return base + (f"A {gx}x{gy} grid of equal {cw}x{cw} cells; frames read left-to-right then top-to-bottom. Same subject, same size "
                   f"and same proportions in every cell; only the pose or state changes. The subject's base (feet) sits on the same "
                   f"baseline in every cell, {(f['cell_art'] - f['anchor_art'][1]) * s} image pixels above the bottom of the cell, "
                   f"horizontally centred.")


def cells(lst, n=4):
    out = [f"Cell {i + 1}: {p}" for i, p in enumerate(lst)]
    out += [f"Cell {i + 1}: leave empty (plain magenta)" for i in range(len(lst), n)]
    return "\n".join(out)


def block(sh, title, attach, body):
    att = "\n".join(f"- `{a}`" for a in attach) or "- (ninguno)"
    return f"### {title}\n\nArchivo: `{sh['name']}`\n\nAdjuntar:\n{att}\n\n```\n{body}\n```\n"


def build(lib, reel, sheets):
    chars = M.characters(lib, reel); S = lib["grid"]["scale"]
    ref = lib.get("project", {}).get("scale_reference")
    STY = style_block(lib); out = []
    for sh in sheets:
        k = sh["kind"]
        if k == "model":
            m = chars[sh["owner"]]["model"]
            att = ["palette.png"] + ([f"{ref}_model.png (referencia de estilo y escala)"] if ref and sh["owner"] != ref else [])
            body = (f"{STY}\n\n{sheet_block(lib, 'char')}\nStanding height: {m['height_px'] * S} image pixels ({m['height_px']} art pixels).\n\n"
                    f"SUBJECT: {m['name']}, {m['description']}\n\nMODEL SHEET:\n{cells(m['cells'])}")
            out.append((sh, block(sh, f"{m['name']} · model sheet", att, body)))
        elif k in ("plate_master", "plate"):
            st = lib["sets"][sh["set"]]; grid = lib["grid"]["art_canvas"]
            if k == "plate_master":
                deco = (reel or {}).get("decorations", "")
                scale = (f"\nFor scale only: {chars[ref]['model']['name']} (attached model sheet) stands in the scene, "
                         f"{chars[ref]['model']['height_px']} art pixels tall.") if ref in chars else ""
                body = (f"{STY}\n\nFORMAT: 9:16 vertical PNG, the whole scene is {grid[0]}x{grid[1]} art pixels (each art pixel a "
                        f"{S}x{S} block).\n\nSCENE: {st['plate']['description']} {deco}{scale}")
                out.append((sh, block(sh, f"{st['name']} · imagen maestra", ["palette.png"] + ([f"{ref}_model.png"] if ref in chars else []), body)))
            else:
                body = ("Same image, same camera, same pixel grid, same palette and light. Remove every character and any seasonal "
                        "decoration. Keep only the empty set exactly as it is. Fill the hidden areas naturally. 9:16 PNG.")
                out.append((sh, block(sh, f"{st['name']} · fondo vacío", [f"plate_{sh['set']}_master.png"], body)))
        elif k == "anim":
            cid, a = sh["owner"], sh["anim"]; m = chars[cid]["model"]
            att = ["palette.png", f"{cid}_model.png"] + ([f"{cid}_{a['id']}_1.png"] if sh["part"] else [])
            if a.get("holds"): att.append(f"{a['holds']}: el sprite del objeto si ya existe")
            first = sh["part"] * 4 + 1
            cont = (" This sheet continues the attached first sheet of the same animation: keep exactly the same size, position "
                    "and baseline.") if sh["part"] else ""
            body = (f"{STY}\n\n{sheet_block(lib, 'char')}\nStanding height: {m['height_px'] * S} image pixels.\n\n"
                    f"SUBJECT: {m['name']} exactly as in the attached model sheet (same face, colours, proportions and size).{cont}\n"
                    f"ACTION: {a['id']} ({a['use']}), {DIRS.get(a['dir'], a['dir'])}, frames {first}-{first + len(sh['cells']) - 1} "
                    f"of {len(a['poses'])}, {MODES[a['mode']]}.\n{cells(sh['cells'])}")
            title = f"{m['name']} · {a['id']} · {len(a['poses'])} cuadros · {a['mode']} · {a.get('priority', '')}"
            if sh["nparts"] > 1: title += f" (hoja {sh['part'] + 1}/{sh['nparts']})"
            out.append((sh, block(sh, title, att, body)))
        elif k == "object":
            o = sh["obj"]; st = lib["sets"][sh["set"]]
            body = (f"{STY}\n\n{sheet_block(lib, o['format'])}\n\nSUBJECT: {o['id'].replace('_', ' ')} for {st['name']} "
                    f"({o['use']}). {o.get('description', '')}\nSTATES:\n{cells(o['poses'])}")
            out.append((sh, block(sh, f"Objeto · {o['id']} · {len(o['poses'])} estados", ["palette.png", f"plate_{sh['set']}_master.png"], body)))
        elif k == "rows":
            rows = "\n".join(f"Row {r + 1} ({g['id']}, {g['use']}): " + " | ".join(f"frame {j + 1}: {p}" for j, p in enumerate(g["poses"]))
                             for r, g in enumerate(sh["rows"]))
            rows += "".join(f"\nRow {r + 1}: leave empty" for r in range(len(sh["rows"]), 4))
            body = f"{STY}\n\n{sheet_block(lib, 'small')}\n\nROWS:\n{rows}"
            refimg = [f"plate_{sh['set']}_master.png"] if sh.get("set") else []
            out.append((sh, block(sh, f"{'Objetos' if sh['prefix'] == 'obj' else 'Efectos'} · " + ", ".join(g["id"] for g in sh["rows"]),
                                  ["palette.png"] + refimg, body)))
        elif k == "items":
            photos = lib["items"].get("photos_dir", "photos/<id>.jpg")
            body = (f"{STY}\n\n{sheet_block(lib, 'item')}\n\nSUBJECT: products of a small shop, as RPG inventory items.\n"
                    + cells([f"{it['description']} (draw it from the attached photo of '{it['id']}', simplified to pixel art)" for it in sh["items"]]))
            out.append((sh, block(sh, "Ítems · " + ", ".join(it["id"] for it in sh["items"]),
                                  ["palette.png"] + [photos.replace("<id>", it["id"]) for it in sh["items"]], body)))
    return out


def palette_png(lib, path):
    from PIL import Image, ImageDraw
    pal = M.palette(lib); n = max(1, len(pal)); cols = 8; rows = -(-n // cols)
    im = Image.new("RGB", (cols * 64, rows * 64), "#FF00FF"); d = ImageDraw.Draw(im)
    for i, h in enumerate(pal):
        x, y = (i % cols) * 64, (i // cols) * 64; d.rectangle([x + 4, y + 4, x + 59, y + 59], fill=h)
    im.save(path)


GATES = {2: "Gate 2 · Model sheets", 3: "Gate 3 · Imagen maestra del escenario", 4: "Gate 4 · Fondo vacío",
         5: "Gate 5 · Animaciones, objetos, efectos e ítems"}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("library"); ap.add_argument("out")
    ap.add_argument("--reel"); ap.add_argument("--only-missing", help="skip sheets that already exist in this folder")
    a = ap.parse_args()
    lib, reel = M.load(a.library, a.reel); os.makedirs(a.out, exist_ok=True)
    sheets = [s for s in M.plan(lib, reel) if s["needed"]]
    if a.only_missing: sheets = [s for s in sheets if not os.path.exists(os.path.join(a.only_missing, s["name"]))]
    palette_png(lib, os.path.join(a.out, "palette.png"))
    md = ["# Prompts para el modelo de imagen", "",
          "Generado por `pixel-reel/scripts/gen_prompts.py`. No editar a mano: cambiar el manifiesto y regenerar.",
          "Pedir en este orden. Cada imagen aprobada se guarda con el nombre indicado en la carpeta de hojas y se adjunta en los prompts siguientes.",
          "", "## Gate 1 · Paleta", "", "`palette.png` ya está generada. No hace falta pedirla.", ""]
    gate = None
    for sh, txt in build(lib, reel, sheets):
        if sh["gate"] != gate: gate = sh["gate"]; md += [f"## {GATES[gate]}", ""]
        md.append(txt)
    open(os.path.join(a.out, "PROMPTS.md"), "w").write("\n".join(md))
    if not reel: write_catalog(lib, os.path.join(a.out, "CATALOGO.md"))
    print(f"{len(sheets)} prompts -> {os.path.join(a.out, 'PROMPTS.md')}")


GROUPS = {"locomotion": "Movimiento", "idle": "Reposo", "emotion": "Emociones y reacciones", "work": "Trabajo", "magic": "Magia",
          "social": "Gestos y social", "sitting": "Sentado", "reel": "Del reel"}
MODES_ES = {"loop": "bucle", "once": "una vez", "hold": "queda en el último", "states": "estados", "static": "fijo"}


def write_catalog(lib, path):
    md = ["# Catálogo de sprites", "", "Generado desde el manifiesto por `pixel-reel/scripts/gen_prompts.py`.", ""]
    for cid, ch in lib.get("characters", {}).items():
        an = ch.get("animations", []); md += [f"## {ch['model']['name']} ({len(an)} animaciones)", ""]
        for g, gname in GROUPS.items():
            rows = [x for x in an if x.get("group") == g]
            if not rows: continue
            md += [f"### {gname}", "", "| id | dir | cuadros | modo | fps | prio | para qué |", "|---|---|---|---|---|---|---|"]
            md += [f"| `{x['id']}` | {x['dir']}{' (+W espejo)' if x.get('mirror_to_W') else ''} | {len(x['poses'])} | {MODES_ES[x['mode']]} | {x.get('fps', 8)} | {x.get('priority', '')} | {x['use']} |" for x in rows]
            md.append("")
    for sid, st in lib.get("sets", {}).items():
        md += [f"## {st['name']}: objetos", "", "| id | estados | modo | prio | para qué |", "|---|---|---|---|---|"]
        md += [f"| `{o['id']}` | {len(o['poses'])} | {MODES_ES[o['mode']]} | {o.get('priority', '')} | {o['use']} |" for o in st.get("objects", [])]
        for season, objs in st.get("seasonal_overlays", {}).items():
            md += [f"| `{o['id']}` ({season}) | {len(o['poses'])} | {MODES_ES[o['mode']]} | {o.get('priority', '')} | {o['use']} |" for o in objs]
        md.append("")
    md += ["## Efectos", "", "| id | cuadros | modo | prio | para qué |", "|---|---|---|---|---|"]
    md += [f"| `{f['id']}` | {len(f['poses'])} | {MODES_ES[f['mode']]} | {f.get('priority', '')} | {f['use']} |" for f in lib.get("fx", [])]
    md += ["", "## Ítems", "", ", ".join(f"`{i['id']}`" for i in lib.get("items", {}).get("list", [])), ""]
    open(path, "w").write("\n".join(md))


if __name__ == "__main__":
    main()
