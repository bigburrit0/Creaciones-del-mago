#!/usr/bin/env python3
"""Regla del dueño (2/11/2026): NUNCA el número de teléfono en un reel (pantalla, voz ni texto del post).

Revisa los guiones (desde «## Después»: guion, voz, post y cierres), los EDICION.md y todos los textos de los
timeline.json de los proyectos de edición. Sale con error si encuentra un teléfono.

Uso, desde la raíz del repo:  python3 -I fuente/campanas/reels-10s/revisar_reglas.py
También lo usa armar.py antes de exportar (no exporta si el timeline tiene un teléfono).
"""
import json, re, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent

# 7 o más dígitos seguidos o separados por espacio, punto o guion (092 104 419, 092104419, +598 92 104 419),
# o pistas directas de un número de contacto.
TELEFONO = re.compile(r"(?<![\w#/])\+?\d(?:[ .\-]?\d){6,}(?![\w/])|wa\.me/|\+598|WhatsApp:?\s*\d", re.I)


def buscar_telefonos(texto):
    return [m.group(0) for m in TELEFONO.finditer(texto or "")]


def textos_de(obj):
    """Todos los strings de un timeline que van a la pantalla o a la voz (claves «texto»)."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "texto" and isinstance(v, str):
                yield v
            else:
                yield from textos_de(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from textos_de(v)


def revisar_timeline(tl, nombre="timeline.json"):
    return [f"{nombre}: «{t}» → {hit}" for t in textos_de(tl) for hit in buscar_telefonos(t)]


def revisar_todo():
    errores = []
    for md in sorted(AQUI.glob("[0-9][0-9]-*.md")):
        s = md.read_text(encoding="utf-8")
        i = s.find("## Después")
        parte = s[i:] if i >= 0 else s
        for n, linea in enumerate(parte.splitlines()):
            for hit in buscar_telefonos(linea):
                errores.append(f"{md.name}: {hit!r} en «{linea.strip()[:90]}»")
    for ed in sorted(AQUI.glob("*/EDICION.md")):
        for linea in ed.read_text(encoding="utf-8").splitlines():
            for hit in buscar_telefonos(linea):
                errores.append(f"{ed.relative_to(AQUI)}: {hit!r} en «{linea.strip()[:90]}»")
    for tlp in sorted(AQUI.glob("*/timeline.json")):
        errores += revisar_timeline(json.loads(tlp.read_text(encoding="utf-8")), str(tlp.relative_to(AQUI)))
    return errores


def main():
    errores = revisar_todo()
    if errores:
        print("NO: hay números de teléfono en los reels (regla: nunca el teléfono en un reel).")
        for e in errores:
            print("  -", e)
        sys.exit(1)
    print("OK: ningún reel tiene número de teléfono.")


if __name__ == "__main__":
    main()
