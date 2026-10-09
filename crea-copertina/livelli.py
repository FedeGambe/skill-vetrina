# python3 livelli.py <cover_orizzontale.svg> <indici soggetto, es. 2 oppure 22-68 oppure g1:1->
# Scrive accanto cover_sfondo.svg (fondo: colore, grafica leggera, grana) e cover_soggetto.svg (solo il soggetto, fondo trasparente).
# Il viewBox del soggetto è provvisorio (tutta la tela): lo stringe bbox.js.
import copy, sys, xml.etree.ElementTree as ET
from pathlib import Path
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS); ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
src, spec = Path(sys.argv[1]), sys.argv[2]
root = ET.parse(src).getroot()

def indici(s, n):
    out = set()
    for parte in s.split(","):
        a, _, b = parte.partition("-")
        out |= set(range(int(a), (int(b) if b else n - 1) + 1)) if _ else {int(a)}
    return out

sfondo, soggetto = copy.deepcopy(root), copy.deepcopy(root)
if spec.startswith("g"):  # soggetto dentro un gruppo: "g1:1-" = figli 1.. del figlio 1 della radice
    g, sub = spec[1:].split(":"); g = int(g)
    for el, tieni in ((sfondo, False), (soggetto, True)):
        gr = list(el)[g]; scelti = indici(sub, len(gr))
        for i, c in reversed(list(enumerate(list(gr)))):
            if (i in scelti) != tieni: gr.remove(c)
        if tieni:  # nel soggetto restano solo defs e il gruppo
            for i, c in reversed(list(enumerate(list(el)))):
                if i != g and not c.tag.endswith("defs"): el.remove(c)
else:
    scelti = indici(spec, len(root))
    for el, tieni in ((sfondo, False), (soggetto, True)):
        for i, c in reversed(list(enumerate(list(el)))):
            if c.tag.endswith("defs"): continue
            if (i in scelti) != tieni: el.remove(c)

sfondo.set("preserveAspectRatio", "xMidYMax slice")
for el, nome in ((sfondo, "cover_sfondo.svg"), (soggetto, "cover_soggetto.svg")):
    ET.ElementTree(el).write(src.with_name(nome), encoding="unicode", xml_declaration=False)
    print("scritto", src.with_name(nome))
