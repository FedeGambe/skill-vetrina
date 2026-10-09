# python3 componi.py <cartella img> [...]: rigenera cover_orizzontale.svg (1600x900) e cover_verticale.svg (1080x1350)
# dai due livelli cover_sfondo.svg + cover_soggetto.svg. Il fondo riempie la tela; il soggetto sta nella metà bassa, appoggiato al fondo
# (i soggetti molto larghi, rapporto > 2,6, riempiono la larghezza e si tagliano ai lati).
import re, sys
from pathlib import Path

def interno(svg, pref):
    """Contenuto dell'svg con gli id prefissati (per non scontrarsi con l'altro livello) + viewBox."""
    vb = re.search(r'viewBox="([^"]+)"', svg).group(1)
    corpo = re.sub(r"^<svg[^>]*>", "", svg.strip(), count=1)
    corpo = re.sub(r"</svg>\s*$", "", corpo)
    corpo = re.sub(r'\bid="([^"]+)"', rf'id="{pref}\1"', corpo)
    corpo = re.sub(r"url\(#([^)]+)\)", rf"url(#{pref}\1)", corpo)
    corpo = re.sub(r'href="#([^"]+)"', rf'href="#{pref}\1"', corpo)
    return vb, corpo

def componi(cartella, W, H, nome):
    sf = (cartella / "cover_sfondo.svg").read_text(encoding="utf-8")
    so = (cartella / "cover_soggetto.svg").read_text(encoding="utf-8")
    vb_s, c_s = interno(sf, "f-")
    vb_g, c_g = interno(so, "s-")
    _, _, gw, gh = map(float, vb_g.split())
    largo = gw / gh > 2.6
    y0 = round(H * 0.5); pad = 0 if largo else round(W * 0.06)
    basso = 0 if largo else round(H * 0.07)  # margine sotto il soggetto (le strisce larghe arrivano al bordo)
    adatta = "xMidYMax slice" if largo else "xMidYMin meet"  # i soggetti partono da metà tela
    out = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">'
           f'<svg width="{W}" height="{H}" viewBox="{vb_s}" preserveAspectRatio="xMidYMax slice">{c_s}</svg>'
           f'<svg x="{pad}" y="{y0}" width="{W - 2 * pad}" height="{H - y0 - basso}" viewBox="{vb_g}" preserveAspectRatio="{adatta}" overflow="hidden">{c_g}</svg>'
           f'</svg>\n')
    (cartella / nome).write_text(out, encoding="utf-8")
    return largo

for d in sys.argv[1:]:
    c = Path(d)
    l = componi(c, 1600, 900, "cover_orizzontale.svg"); componi(c, 1080, 1350, "cover_verticale.svg")
    print(d, "largo" if l else "")
