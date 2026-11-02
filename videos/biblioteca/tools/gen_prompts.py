"""Generate copy-paste Gemini prompts (and the palette image) from a sprite manifest.

usage:
  python3 gen_prompts.py ../sprites.json OUT_DIR                      # whole library
  python3 gen_prompts.py ../sprites.json OUT_DIR --reel REEL.json     # only what a reel needs (+ its own characters)

Writes OUT_DIR/PROMPTS.md (one block per image to request, in approval order) and OUT_DIR/palette.png.
The manifest is the source of truth: add an animation there and regenerate, never hand-edit PROMPTS.md.
"""
import json, os, sys

STYLE = ("STYLE (must follow exactly): authentic 16-bit SNES-era pixel art, top-down three-quarter view like a 1990s "
         "farming RPG. Hard square pixels, every art pixel is a 4x4 block of image pixels. No anti-aliasing, no blur, no "
         "gradients, no semi-transparency. Dithering only in backgrounds, never on characters or props. Every sprite has a "
         "1-art-pixel dark outline #150A34. Light comes from the upper-left, shadows fall to the lower-right, 3 tones per "
         "material. Use only colours from the attached palette. No text, no letters, no numbers, no logos, no watermark.")
SHEET = {
    "char": ("SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, "
             "no floor, no grid lines, no borders. A 2x2 grid of equal 512x512 cells; frames read left-to-right then "
             "top-to-bottom. Same subject, same size and same proportions in every cell; only the pose or state changes. "
             "The subject's base (feet) sits on the same baseline in every cell, 16 image pixels above the bottom of the "
             "cell, horizontally centred."),
    "small": ("SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, "
              "no grid lines, no borders. A 4x4 grid of equal 256x256 cells. Each ROW is one animation of up to 4 frames, "
              "read left to right; unused cells stay plain magenta. Every subject is centred in its cell and stays the "
              "same size across its row; each subject fits inside 128x128 image pixels."),
    "item": ("SHEET: 1024x1024 PNG. Flat pure magenta #FF00FF background filling the whole image, no shadow on the background, "
             "no grid lines, no borders. A 2x2 grid of equal 512x512 cells, one object per cell, each object at most 160x160 "
             "image pixels (40x40 art pixels), centred, resting on an invisible baseline 128 image pixels above the bottom "
             "of the cell. All four objects drawn at the same pixel scale."),
}
DIRS = {"S": "facing the camera in a front three-quarter view", "E": "seen from the side, facing RIGHT",
        "N": "seen from behind, facing away from the camera", "W": "seen from the side, facing LEFT",
        "S>N": "turning from facing the camera to facing away"}
PALETTE = ["#150A34", "#2E2160", "#4B3A8E", "#6A58B8", "#C98A2B", "#F2C14E", "#C8AE88", "#F0D8B2",
           "#D9826A", "#E1AE73", "#F0C090", "#5A3424", "#8A5638", "#6E3B22", "#A0603A", "#D8D4C8",
           "#FFF3B0", "#F2B640", "#1E3A2A", "#2F5A32", "#5C9A4A", "#9BC46A", "#7A1E22", "#C0392B",
           "#E86A4A", "#2B4C7E", "#4F86C6", "#9CC9E8", "#5B4636", "#B08A5A", "#E9D8B4", "#FBF4E4"]


def palette_png(path):
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return False
    im = Image.new("RGB", (8 * 64, 4 * 64), "#FF00FF"); d = ImageDraw.Draw(im)
    for i, h in enumerate(PALETTE):
        x, y = (i % 8) * 64, (i // 8) * 64
        d.rectangle([x + 4, y + 4, x + 59, y + 59], fill=h)
    im.save(path); return True


def block(title, filename, attach, body):
    att = "\n".join(f"- `{a}`" for a in attach) if attach else "- (ninguno)"
    return f"### {title}\n\nArchivo: `{filename}`\n\nAdjuntar:\n{att}\n\n```\n{body}\n```\n"


def cells_text(poses, offset=0):
    return "\n".join(f"Cell {i + 1}: {p}" for i, p in enumerate(poses)) + (
        "" if len(poses) == 4 else "\n" + "\n".join(f"Cell {i + 1}: leave empty (plain magenta)" for i in range(len(poses), 4)))


def char_prompts(cid, ch, wanted=None):
    out = []; m = ch["model"]; model_file = f"{cid}_model.png"
    body = (f"{STYLE}\n\n{SHEET['char']}\nStanding height: {m['height_px'] * 4} image pixels ({m['height_px']} art pixels).\n\n"
            f"SUBJECT: {m['name']}, {m['description']}\n\nMODEL SHEET:\n{cells_text(m['cells'])}")
    ref = ["palette.png"] + (["mago_model.png (referencia de estilo y escala)"] if cid != "mago" else [])
    model = block(f"{m['name']}: model sheet (gate 2)", model_file, ref, body)
    for a in ch["animations"]:
        if wanted is not None and a["id"] not in wanted: continue
        poses = a["poses"]; parts = [poses[i:i + 4] for i in range(0, len(poses), 4)]
        for k, part in enumerate(parts):
            fname = f"{cid}_{a['id']}_{k + 1}.png"
            attach = ["palette.png", model_file] + ([f"{cid}_{a['id']}_1.png"] if k else [])
            if a.get("holds") == "mate": attach.append("mate.png (si ya existe)")
            frames = f"frames {k * 4 + 1}-{k * 4 + len(part)} of {len(poses)}"
            cont = (" This sheet continues the attached first sheet of the same animation: keep exactly the same size, "
                    "position and baseline.") if k else ""
            body = (f"{STYLE}\n\n{SHEET['char']}\nStanding height: {m['height_px'] * 4} image pixels.\n\n"
                    f"SUBJECT: {m['name']} exactly as in the attached model sheet (same face, colours, proportions and size).{cont}\n"
                    f"ACTION: {a['id']} ({a['use']}), {DIRS.get(a['dir'], a['dir'])}, {frames}, "
                    f"{'looping' if a['mode'] == 'loop' else 'played once'}.\n{cells_text(part)}")
            out.append(block(f"{m['name']} · {a['id']} · {a['frames']} cuadros · {a['mode']} · {a['priority']}"
                             + (f" (hoja {k + 1}/{len(parts)})" if len(parts) > 1 else ""), fname, attach, body))
    return model, out


def object_prompts(objs, ref, kind):
    out = []
    small = [o for o in objs if o["format"] == "small"]
    for o in [o for o in objs if o["format"] != "small"]:
        body = (f"{STYLE}\n\n{SHEET[o['format']]}\n\nSUBJECT: {o['id'].replace('_', ' ')} for the wizard's workshop "
                f"({o['use']}). {o.get('description', '')}\nSTATES:\n{cells_text(o['poses'])}")
        out.append(block(f"{kind} · {o['id']} · {o['frames']} estados · {o['priority']}", f"{o['id']}.png", ["palette.png", ref], body))
    for i in range(0, len(small), 4):
        group = small[i:i + 4]
        rows = "\n".join(f"Row {r + 1} ({g['id']}, {g['use']}): " + " | ".join(f"frame {j + 1}: {p}" for j, p in enumerate(g["poses"]))
                         for r, g in enumerate(group))
        rows += "".join(f"\nRow {r + 1}: leave empty" for r in range(len(group), 4))
        body = f"{STYLE}\n\n{SHEET['small']}\n\nROWS:\n{rows}"
        name = "_".join(g["id"] for g in group)
        out.append(block(f"{kind} · {', '.join(g['id'] for g in group)}", f"{'objects' if kind == 'Objeto' else 'fx'}_{i // 4 + 1}.png", ["palette.png", ref], body))
    return out


def item_prompts(items, photos_dir):
    out = []
    for i in range(0, len(items), 4):
        group = items[i:i + 4]
        cells = cells_text([f"{it['description']} (draw it from the attached photo of '{it['id']}', simplified to pixel art)" for it in group])
        body = f"{STYLE}\n\n{SHEET['item']}\n\nSUBJECT: 3D printed products from a small shop, as RPG inventory items.\n{cells}"
        out.append(block(f"Ítems · {', '.join(it['id'] for it in group)}", f"items_{i // 4 + 1}.png",
                         ["palette.png"] + [photos_dir.replace("<id>", it["id"]) for it in group], body))
    return out


GROUPS = {"locomotion": "Movimiento", "idle": "Reposo", "emotion": "Emociones y reacciones", "work": "Trabajo",
          "magic": "Magia", "social": "Gestos y social", "sitting": "Sentado"}
MODES = {"loop": "bucle", "once": "una vez", "hold": "queda en el último", "states": "estados", "static": "fijo"}


def write_catalog(lib, path):
    md = ["# Catálogo de sprites", "", "Generado desde `sprites.json` por `tools/gen_prompts.py`. Prioridad: P0 = lo usa el reel de Navidad, "
          "P1 = siguiente tanda, P2 = cuando haga falta.", ""]
    for cid, ch in lib["characters"].items():
        an = ch["animations"]
        md += [f"## {ch['model']['name']} ({len(an)} animaciones)", ""]
        for g, gname in GROUPS.items():
            rows = [a for a in an if a["group"] == g]
            if not rows: continue
            md += [f"### {gname}", "", "| id | dir | cuadros | modo | fps | prio | para qué |", "|---|---|---|---|---|---|---|"]
            md += [f"| `{a['id']}` | {a['dir']}{' (+W espejo)' if a.get('mirror_to_W') else ''} | {a['frames']} | {MODES[a['mode']]} | {a['fps']} | {a['priority']} | {a['use']} |" for a in rows]
            md.append("")
    t = lib["sets"]["taller"]
    md += ["## Taller: objetos con estados", "", "| id | estados | modo | prio | para qué |", "|---|---|---|---|---|"]
    md += [f"| `{o['id']}` | {o['frames']} | {MODES[o['mode']]} | {o['priority']} | {o['use']} |" for o in t["objects"]]
    for season, objs in t["seasonal_overlays"].items():
        md += [f"| `{o['id']}` ({season}) | {o['frames']} | {MODES[o['mode']]} | {o['priority']} | {o['use']} |" for o in objs]
    md += ["", "## Efectos", "", "| id | cuadros | modo | prio | para qué |", "|---|---|---|---|---|"]
    md += [f"| `{f['id']}` | {f['frames']} | {MODES[f['mode']]} | {f['priority']} | {f['use']} |" for f in lib["fx"]]
    md += ["", "## Ítems del catálogo", "", ", ".join(f"`{i['id']}`" for i in lib["items"]["list"]), ""]
    open(path, "w").write("\n".join(md))


def main():
    src, out_dir = sys.argv[1], sys.argv[2]
    reel = json.load(open(sys.argv[sys.argv.index("--reel") + 1])) if "--reel" in sys.argv else None
    lib = json.load(open(src)); os.makedirs(out_dir, exist_ok=True)
    palette_png(os.path.join(out_dir, "palette.png"))
    need = reel["uses"] if reel else None
    md = ["# Prompts para Gemini", "",
          "Generado por `videos/biblioteca/tools/gen_prompts.py`. No editar a mano: cambiar el JSON y regenerar.",
          "Orden = orden de aprobación (ver `videos/biblioteca/ESTILO.md`, sección 8). Cada imagen aprobada se guarda con el nombre indicado y se adjunta en los prompts siguientes.",
          "", "## Gate 1 · Paleta", "", "`palette.png` ya está generada (32 colores). No hace falta pedirla.", ""]
    chars = dict(lib["characters"]); chars.update((reel or {}).get("characters", {}))
    models, anims = [], []
    for cid, ch in chars.items():
        wanted = None if not need else set(need.get(cid, [])) if cid in need else (None if cid in (reel or {}).get("characters", {}) else set())
        if wanted == set(): continue
        mb, ab = char_prompts(cid, ch, wanted); models.append(mb); anims += ab
    md += ["## Gate 2 · Model sheets de los personajes", ""] + models
    taller = lib["sets"]["taller"]
    md += ["## Gate 3 y 4 · Escenario", ""]
    plate = taller["plate"]
    deco = (reel or {}).get("decorations", "")
    md.append(block("Taller · imagen maestra (gate 3)", "plate_taller_master.png", ["palette.png", "mago_model.png"],
                    f"{STYLE}\n\nFORMAT: 9:16 vertical PNG, the whole scene is 270x480 art pixels (each art pixel a 4x4 block).\n\n"
                    f"SCENE: {plate['description']} {deco}\nFor scale only: El Mago (attached model sheet) stands at the workbench, "
                    f"96 art pixels tall."))
    md.append(block("Taller · fondo vacío (gate 4)", "plate_taller.png", ["plate_taller_master.png"],
                    "Same image, same camera, same pixel grid, same palette and light. Remove the wizard and any seasonal decoration. "
                    "Keep only the empty room exactly as it is. Fill the hidden areas naturally. 9:16 PNG."))
    objs = taller["objects"] + [o for s in taller["seasonal_overlays"].values() for o in s]
    if need: objs = [o for o in objs if o["id"] in need.get("objects", [])]
    md += ["## Gate 5 · Animaciones de los personajes", ""] + anims
    md += ["## Gate 5 · Objetos y efectos", ""]
    md += object_prompts(objs, "plate_taller_master.png", "Objeto")
    fx = lib["fx"] if not need else [f for f in lib["fx"] if f["id"] in need.get("fx", [])]
    md += object_prompts([dict(f, format="small") for f in fx], "plate_taller_master.png", "FX")
    items = lib["items"]["list"] if not need else [it for it in lib["items"]["list"] if it["id"] in need.get("items", [])]
    md += ["## Gate 5 · Ítems del catálogo", ""] + item_prompts(items, lib["items"]["photos_dir"])
    open(os.path.join(out_dir, "PROMPTS.md"), "w").write("\n".join(md))
    if not reel: write_catalog(lib, os.path.join(out_dir, "CATALOGO.md"))
    print("prompts:", sum(1 for l in md if l.startswith("### ")), "->", os.path.join(out_dir, "PROMPTS.md"))


if __name__ == "__main__":
    main()
