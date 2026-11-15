"""Builds ENTREGA/COPYS.md: every finished reel with its caption and DM, copied verbatim from each GUION.md (or PLAN_AJEDREZ.md
for reel 1 of the chess series), in publishing order."""
import re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")

def block_after(path, marker, n=0):
    s = open(path).read(); i = s.index(marker); blocks = re.findall(r"```\n(.*?)\n```", s[i:], re.S); return blocks[n]

def quotes_after(path, marker, stop=r"\n## "):
    s = open(path).read(); i = s.index(marker); rest = s[i + len(marker):]; m = re.search(stop, rest); rest = rest[:m.start()] if m else rest
    return [l[2:].strip() for l in rest.splitlines() if l.startswith("> ")]

R = [  # folder, title, files, length, proposed date, caption source, DM source, note
 ("vikingo-o-caballero", "¿Vikingo o caballero?", ["vikingo-o-caballero.mp4"], "26,8 s", "martes 10/11", ("PLAN_AJEDREZ.md", "**1. ¿Vikingo o caballero?**"), ("PLAN_AJEDREZ.md", "**DM by private reply**", r"\n\n\*\*|\n## "), "Historia el mismo día: encuesta «¿Vikingo o caballero?»."),
 ("un-regalo-para-cada-amigo", "Un regalo para cada amigo", ["un-regalo-para-cada-amigo.mp4"], "25,3 s", "viernes 13/11", ("un-regalo-para-cada-amigo/GUION.md", "## Caption"), None, "El CTA es etiquetar a un amigo. A cada etiqueta o comentario: «¿Te paso precio? Escribime 😉». Historia el mismo día: encuesta «¿Cuál le regalás?»."),
 ("una-mas", "Una más", ["una-mas.mp4"], "27,2 s", "sábado 14/11", ("una-mas/GUION.md", "## Caption"), ("una-mas/GUION.md", "**Private reply**", r"\n\n\*\*|\n## "), "Historia el mismo día: encuesta «¿Vikingo o medieval?» y sticker con link a WhatsApp."),
 ("elegi-tu-bando", "Elegí tu bando", ["elegi-tu-bando.mp4"], "21,6 s", "miércoles 18/11", ("elegi-tu-bando/GUION.md", "## Caption"), ("elegi-tu-bando/GUION.md", "**Private reply**", r"\n\n\*\*|\n## "), "Historia el mismo día: encuesta «¿Qué colores le pondrías a tu bando?» y sticker con link a WhatsApp."),
 ("papa-noel-en-ojotas", "Papá Noel en ojotas", ["papa-noel-en-ojotas-3d.mp4", "papa-noel-en-ojotas-3d-v2.mp4"], "21 s", "viernes 20/11", ("papa-noel-en-ojotas/GUION.md", "**Principal**"), None, "Hay dos ediciones del mismo reel, con las mismas voces: la 3D y la V2, con otros planos y otra edición. Publicá una. En `GUION.md` hay dos captions alternativos («diario del Mago» y «diálogo»). El CTA es escribir por WhatsApp, sin palabra clave."),
 ("las-preguntas-de-papa-noel", "Las preguntas de Papá Noel", ["las-preguntas-de-papa-noel.mp4"], "27,2 s", "domingo 22/11", ("las-preguntas-de-papa-noel/GUION.md", "## Caption"), ("las-preguntas-de-papa-noel/GUION.md", "## Private reply"), None),
 ("culpa-de-las-piezas", "Culpa de las piezas", ["culpa-de-las-piezas.mp4"], "24,2 s", "jueves 26/11 (Black Week)", ("culpa-de-las-piezas/GUION.md", "## Caption"), ("culpa-de-las-piezas/GUION.md", "## Private reply"), None),
 ("los-gatos-tiran-todo", "Los gatos tiran todo", ["los-gatos-tiran-todo.mp4"], "23 s", "domingo 29/11", ("los-gatos-tiran-todo/GUION.md", "## Caption"), ("los-gatos-tiran-todo/GUION.md", "## Private reply"), None),
 ("invisible-no-era", "Invisible no era", ["invisible-no-era.mp4"], "27,4 s", "martes 1/12", ("invisible-no-era/GUION.md", "**Principal**"), None, "En `GUION.md` hay dos captions alternativos («la confesión» y «el chat del día después»). El CTA es escribir por WhatsApp, sin palabra clave. Historia el mismo día: encuesta «¿Ya te tocó alguien?»."),
 ("la-gaviota", "La gaviota", ["la-gaviota.mp4"], "26 s", "jueves 3/12", ("la-gaviota/GUION.md", "## Caption"), ("la-gaviota/GUION.md", "## Private reply"), None),
 ("el-laberinto", "El laberinto", ["el-laberinto.mp4"], "23 s", "domingo 6/12", ("el-laberinto/GUION.md", "## Caption"), ("el-laberinto/GUION.md", "## Private reply"), None),
 ("el-mantel", "El mantel", ["el-mantel.mp4"], "24,5 s", "domingo 13/12", ("el-mantel/GUION.md", "## Caption"), ("el-mantel/GUION.md", "## Private reply"), None),
]
out = ["# Creaciones del Mago: todos los reels con su copy", "",
       "Están ordenados por la fecha de publicación que propusimos. Cada caption está copiado tal cual de su `GUION.md`.",
       "Los cuatro primeros tenían fecha antes del 15/11: si todavía no los publicaste, conviene moverlos (ver al final).", ""]
for k, (folder, title, files, dur, date, cap, dm, note) in enumerate(R, 1):
    out += [f"## {k}. {title}", "", f"- **Archivo:** {', '.join('`' + folder + '/' + f + '`' for f in files)} ({dur}, 1080 × 1920)", f"- **Fecha propuesta:** {date}", ""]
    out += ["**Caption**", "", "```", block_after(*cap), "```", ""]
    if dm:
        q = quotes_after(*dm); out += ["**DM a cada comentario** (por mensaje privado, dentro de los 7 días)", "", f"> {q[0]}", ""]
        if len(q) > 1: out += ["Si no contesta en unas 24 h, una sola vez:", "", f"> {q[1]}", ""]
    if note: out += [f"_{note}_", ""]
out += ["## Si los primeros todavía no salieron", "",
        "«¿Vikingo o caballero?», «Un regalo para cada amigo» y «Una más» tenían fecha del 10 al 14/11.",
        "Para no amontonar, se pueden intercalar en los huecos: lunes 16/11, martes 24/11 y lunes 30/11.",
        "Así quedaría un reel cada dos o tres días hasta el 13/12, con el último día de pedidos (23/12) siempre por delante.", ""]
open("ENTREGA/COPYS.md", "w").write("\n".join(out)); print("ok", len(R))
