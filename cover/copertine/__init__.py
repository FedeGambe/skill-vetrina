"""Copertine in stile paperback vintage, generate come SVG.

    from copertine import genera, favicon_uri
    svg = genera("cerchio_diviso", "retro", "banner")          # 1200x400, solo grafica
    svg = genera("spirale", "mattone", "poster", titolo="Titolo", sottotitolo="Sottotitolo")  # 1080x1350
    href = favicon_uri("cerchio_diviso", "retro")               # per <link rel="icon" href=...>
"""
import random
import textwrap
from html import escape
from urllib.parse import quote

from .palette import PALETTE, chiaro
from .stili import STILI

FORMATI = {"banner": (1200, 400), "poster": (1080, 1350), "schermo": (1600, 900), "favicon": (64, 64)}
GRANA = ('<filter id="grana"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2"/>'
         '<feColorMatrix values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .55 0"/></filter>')
FONT = "Archivo, 'Archivo Black', 'Helvetica Neue', Arial, sans-serif"


def genera(stile, palette="retro", formato="banner", titolo="", sottotitolo="", seed=0, grana=True, parola=""):
    p, (w, h) = PALETTE[palette], FORMATI[formato]
    rng = random.Random(seed)
    parola = parola or (titolo.split() or ["Aa"])[0]  # per gli stili tipografici
    arte_x, arte_y, arte_w, arte_h = 0, 0, w, h
    testo = ""
    if formato == "poster":  # titolo in alto a sinistra, grafica sotto
        colore = p["ink"] if chiaro(p["sfondo"]) else p["carta"]
        righe = textwrap.wrap(titolo, 16)[:4]
        fs = 104 if len(righe) <= 3 else 84
        testo = "".join(f'<text x="70" y="{150+i*fs*1.05:.0f}" font-family="{FONT}" font-weight="900" font-size="{fs}" fill="{colore}">{escape(r)}</text>' for i, r in enumerate(righe))
        if sottotitolo:
            testo += f'<text x="70" y="{150+len(righe)*fs*1.05+30:.0f}" font-family="{FONT}" font-weight="600" font-size="34" fill="{colore}">{escape(sottotitolo)}</text>'
        arte_y, arte_h = 520, h - 520 - 40
    if formato == "schermo":  # cover a tutto schermo: titolo in HTML sopra, grafica nel 62% inferiore
        arte_y = int(h * .38)
        arte_h = h - arte_y
    arte = STILI[stile](arte_w, arte_h, p, rng, "a", parola)
    sfondo = f'<rect width="{w}" height="{h}" fill="{p["sfondo"]}"/>'
    if formato == "favicon":
        sfondo = f'<clipPath id="r"><rect width="64" height="64" rx="14"/></clipPath>' + sfondo.replace("<rect", '<rect clip-path="url(#r)"')
        arte = f'<g clip-path="url(#r)">{arte}</g>'
    velo = f'<rect width="{w}" height="{h}" filter="url(#grana)" opacity=".35"/>' if grana and formato != "favicon" else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><defs>{GRANA}</defs>{sfondo}'
            f'<svg x="{arte_x}" y="{arte_y}" width="{arte_w}" height="{arte_h}" viewBox="0 0 {arte_w} {arte_h}" overflow="hidden">{arte}</svg>{testo}{velo}</svg>')


def favicon_uri(stile, palette="retro", seed=0):
    return "data:image/svg+xml," + quote(genera(stile, palette, "favicon", seed=seed), safe="/:=,")
