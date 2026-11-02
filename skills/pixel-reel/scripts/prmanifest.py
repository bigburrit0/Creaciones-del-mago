"""Shared manifest logic for pixel-reel: loads the library (sprites.json) and an optional reel (reel.json)
and builds the SHEET PLAN, the list of images to request from the image model, with stable file names.

Every script (gen_prompts, placeholders, slice_sheets) uses this plan, so a sheet name always means the
same content whether you work on the whole library or on one reel.
"""
import json, os

DEFAULT_GRID = {"art_canvas": [270, 480], "scale": 4, "video": [1080, 1920], "fps_video": 30}
DEFAULT_FORMATS = {
    "char": {"image": [1024, 1024], "grid": [2, 2], "cell_art": 128, "anchor_art": [64, 124]},
    "small": {"image": [1024, 1024], "grid": [4, 4], "cell_art": 64, "anchor_art": [32, 32]},
    "item": {"image": [1024, 1024], "grid": [2, 2], "cell_art": 128, "anchor_art": [64, 84], "item_max_art": 40},
}


def load(lib_path, reel_path=None):
    lib = json.load(open(lib_path))
    reel = json.load(open(reel_path)) if reel_path else None
    lib.setdefault("grid", DEFAULT_GRID)
    fmts = dict(DEFAULT_FORMATS); fmts.update(lib.get("sheet_formats", {})); lib["sheet_formats"] = fmts
    lib["_dir"] = os.path.dirname(os.path.abspath(lib_path))
    if reel is not None: reel["_dir"] = os.path.dirname(os.path.abspath(reel_path))
    return lib, reel


def characters(lib, reel):
    chars = {k: dict(v, _from="library") for k, v in lib.get("characters", {}).items()}
    for k, v in (reel or {}).get("characters", {}).items(): chars[k] = dict(v, _from="reel")
    return chars


def _chunks(seq, n): return [seq[i:i + n] for i in range(0, len(seq), n)]


def plan(lib, reel=None):
    """Return the ordered list of sheets. Each sheet: dict(name, kind, fmt, gate, needed, ...)."""
    need = (reel or {}).get("uses")
    sheets = []
    chars = characters(lib, reel)

    def char_needed(cid, aid):
        if need is None: return True
        if chars[cid]["_from"] == "reel": return True
        return aid in set(need.get(cid, []))

    # gate 2: model sheets
    for cid, ch in chars.items():
        used = need is None or chars[cid]["_from"] == "reel" or bool(need.get(cid))
        sheets.append(dict(name=f"{cid}_model.png", kind="model", fmt="char", gate=2, needed=used, owner=cid,
                           cells=ch["model"]["cells"], key=f"{cid}.model", mode="states", fps=1))
    # gate 3-4: plates
    sets = lib.get("sets", {})
    for sid, st in sets.items():
        used = need is None or (reel or {}).get("set") == sid
        sheets.append(dict(name=f"plate_{sid}_master.png", kind="plate_master", fmt="plate", gate=3, needed=used, set=sid))
        sheets.append(dict(name=f"plate_{sid}.png", kind="plate", fmt="plate", gate=4, needed=used, set=sid))
    # gate 5: character animations (4 frames per sheet)
    for cid, ch in chars.items():
        for a in ch.get("animations", []):
            parts = _chunks(a["poses"], 4)
            for k, part in enumerate(parts):
                sheets.append(dict(name=f"{cid}_{a['id']}_{k + 1}.png", kind="anim", fmt="char", gate=5,
                                   needed=char_needed(cid, a["id"]), owner=cid, anim=a, part=k, nparts=len(parts),
                                   cells=part, key=f"{cid}.{a['id']}", mode=a["mode"], fps=a.get("fps", 8)))
    # gate 5: objects (stable grouping in library order)
    want_obj = None if need is None else set(need.get("objects", []))
    for sid, st in sets.items():
        objs = list(st.get("objects", [])) + [o for grp in st.get("seasonal_overlays", {}).values() for o in grp]
        for o in [o for o in objs if o["format"] != "small"]:
            sheets.append(dict(name=f"{o['id']}.png", kind="object", fmt=o["format"], gate=5, set=sid,
                               needed=want_obj is None or o["id"] in want_obj, obj=o, cells=o["poses"],
                               key=f"obj.{o['id']}", mode=o["mode"], fps=o.get("fps", 8)))
        small = [o for o in objs if o["format"] == "small"]
        for i, grp in enumerate(_chunks(small, 4)):
            sheets.append(dict(name=f"objects_{sid}_{i + 1}.png", kind="rows", fmt="small", gate=5, set=sid,
                               needed=want_obj is None or any(o["id"] in want_obj for o in grp), rows=grp, prefix="obj"))
    want_fx = None if need is None else set(need.get("fx", []))
    for i, grp in enumerate(_chunks(lib.get("fx", []), 4)):
        sheets.append(dict(name=f"fx_{i + 1}.png", kind="rows", fmt="small", gate=5,
                           needed=want_fx is None or any(f["id"] in want_fx for f in grp), rows=grp, prefix="fx"))
    want_it = None if need is None else set(need.get("items", []))
    items = lib.get("items", {}).get("list", [])
    for i, grp in enumerate(_chunks(items, 4)):
        sheets.append(dict(name=f"items_{i + 1}.png", kind="items", fmt="item", gate=5,
                           needed=want_it is None or any(it["id"] in want_it for it in grp), items=grp))
    return sheets


def palette(lib):
    return lib.get("project", {}).get("style", {}).get("palette", [])


def hex2rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
