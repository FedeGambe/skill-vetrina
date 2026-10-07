"""Stili nati dai riferimenti in esempi/ispirazioni (poster tipografici): stessa firma di stili.py."""
import math
from html import escape

from .palette import mescola
from .stili import FONT


def _testo(x, y, size, fill, t, extra="", peso=900):
    return (f'<text x="{x:.0f}" y="{y:.0f}" font-family="{FONT}" font-weight="{peso}" font-size="{size:.0f}" fill="{fill}" {extra}>{escape(t)}</text>')


def specchio(w, h, p, rng, pid, parola=""):
    """La parola in tre fasce, specchiata e schiacciata verso i lati (simmetria)."""
    t, fs = (parola or "Aa").upper()[:4], h / 3 * .95
    out = ""
    for i in range(3):
        for j, (off, sx) in enumerate(((0, 1), (.3, .5), (.43, .18))):
            for lato in ((1,) if j == 0 else (-1, 1)):
                out += (f'<g transform="translate({w/2 + lato*off*w:.0f} 0) scale({sx*lato} 1)">'
                        + _testo(0, (i + .85) * h / 3, fs, p["acc"][i % 2], t, f'text-anchor="middle" textLength="{w*.3:.0f}" lengthAdjust="spacingAndGlyphs"') + '</g>')
    return out


def ornamento(w, h, p, rng, pid, parola=""):
    """Macchie scure ripetute a specchio in quattro quadranti, tono su tono."""
    forme = "".join(
        f'<ellipse cx="{rng.uniform(0, w/2):.0f}" cy="{rng.uniform(0, h/2):.0f}" rx="{rng.uniform(w*.02, w*.09):.0f}" ry="{rng.uniform(w*.02, w*.09):.0f}" '
        f'transform="rotate({rng.uniform(0, 180):.0f} {w/4:.0f} {h/4:.0f})" fill="{mescola(p["acc"][i % 4], p["sfondo"], .45)}"/>' for i in range(70))
    q = f'<g id="{pid}q"><rect width="{w/2}" height="{h/2}" fill="{p["sfondo"]}"/>{forme}</g>'
    specchi = "".join(f'<use href="#{pid}q" transform="{t}"/>' for t in (f"translate({w} 0) scale(-1 1)", f"translate(0 {h}) scale(1 -1)", f"translate({w} {h}) scale(-1 -1)"))
    return q + specchi + _testo(w / 2, h / 2, w * .1, mescola(p["carta"], p["sfondo"], .6), parola.upper()[:8], 'text-anchor="middle"')


def gonfiato(w, h, p, rng, pid, parola=""):
    """Parola in tre righe, lettere grasse e lucide come palloncini."""
    t, fs, a = (parola or "Aa").upper(), h / 3 * .8, p["acc"][0]
    out = f'<filter id="{pid}b"><feGaussianBlur stdDeviation="{fs*.02:.1f}"/></filter>'
    for i in range(3):
        y = (i + .8) * h / 3
        for stroke, sw, dx, op in ((mescola(a, "#000000", .35), .24, 0, 1), (a, .2, 0, 1), (mescola(a, "#ffffff", .7), .05, -.06, .9)):
            out += _testo(w / 2 + dx * fs, y + dx * fs, fs, "none" if dx else stroke, t,
                          f'text-anchor="middle" textLength="{w*.84:.0f}" lengthAdjust="spacingAndGlyphs" stroke="{stroke}" stroke-width="{fs*sw:.0f}" '
                          f'stroke-linejoin="round" opacity="{op}"' + (f' filter="url(#{pid}b)"' if dx else ""))
    return out


def xilografia(w, h, p, rng, pid, parola=""):
    """Lettere massicce su due righe e stecche oblique, con l'inchiostro a macchie."""
    t = (parola or "Aa").upper()[:8]
    meta = (len(t) + 1) // 2
    defs = (f'<filter id="{pid}f"><feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="3" seed="{rng.randrange(99)}"/>'
            '<feColorMatrix values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 -2.9"/><feComposite in="SourceGraphic" operator="in"/></filter>')
    righe = "".join(_testo(w * .04, h * y, h * .26, p["ink"], r, f'textLength="{w*.92*len(r)/meta:.0f}" lengthAdjust="spacingAndGlyphs"')
                    for y, r in ((.52, t[:meta]), (.74, t[meta:])) if r)
    stecche = "".join(f'<polygon points="{x:.0f},{y:.0f} {x+w*.4:.0f},{y-h*.07:.0f} {x+w*.4:.0f},{y-h*.02:.0f} {x:.0f},{y+h*.05:.0f}" fill="{p["ink"]}"/>'
                      for x, y in ((w * .03, h * .08), (w * .6, h * .3), (w * .1, h * .88)))
    return defs + f'<g filter="url(#{pid}f)">{righe}{stecche}</g><circle cx="{w*.3:.0f}" cy="{h*.77:.0f}" r="{w*.05:.0f}" fill="{p["acc"][1]}"/>'


def rilievo(w, h, p, rng, pid, parola=""):
    """Paesaggio a reticolo (fili di ferro) con la parola stesa sopra, inclinata."""
    n, f1, f2 = 30, rng.uniform(2, 3.5), rng.uniform(5, 8)
    righe = ""
    for r in range(n):
        v = r / (n - 1)
        y0 = h * (.2 + .85 * v ** 1.6)
        pts = " ".join(f"{x:.0f},{y0 - h*.16*(1 - v*.5)*(math.sin(x/w*f1 + r*.15) * .6 + math.sin(x/w*f2 - r*.3) * .4 + 1) * (.5 + v):.0f}" for x in range(-20, int(w) + 40, 20))
        righe += f'<polyline points="{pts} {w+20},{h+20} -20,{h+20}" fill="{p["sfondo"]}" stroke="{p["ink"]}" stroke-width="{1+v*1.5:.1f}"/>'
    return righe + (f'<g transform="rotate(-9 {w/2} {h/2})">' + _testo(w * .06, h * .55, h * .13, p["ink"], (parola or "Aa").upper()[:10], f'textLength="{w*.88:.0f}" lengthAdjust="spacingAndGlyphs"') + '</g>')


def vortice(w, h, p, rng, pid, parola=""):
    """Raggi alternati che si torcono verso un punto: effetto girandola."""
    n, tw, R, cx, cy = 20, rng.uniform(1.1, 1.7), max(w, h) * .95, w * .55, h * .5
    def bordo(a0):
        return [(cx + r * math.cos(a0 + tw * (r / R) ** .6), cy + r * math.sin(a0 + tw * (r / R) ** .6)) for r in (R * k / 40 for k in range(1, 41))]
    out = ""
    for k in range(n):
        a0 = k * 2 * math.pi / n
        poly = bordo(a0) + bordo(a0 + math.pi / n)[::-1]
        out += f'<polygon points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in poly)}" fill="{p["acc"][0]}"/>'
    return out


def acquerello(w, h, p, rng, pid, parola=""):
    """Macchie d'acqua e pigmento nella metà bassa, bordi mossi da un filtro."""
    defs = (f'<filter id="{pid}f" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency=".008 .015" numOctaves="2" seed="{rng.randrange(99)}"/>'
            f'<feDisplacementMap in="SourceGraphic" scale="{w*.08:.0f}"/><feGaussianBlur stdDeviation="1.5"/></filter>')
    macchie = ""
    for i in range(14):
        y = h * (.4 + .6 * i / 14)
        macchie += (f'<ellipse cx="{rng.uniform(0, w):.0f}" cy="{y:.0f}" rx="{rng.uniform(w*.25, w*.6):.0f}" ry="{rng.uniform(h*.03, h*.08):.0f}" '
                    f'fill="{p["acc"][i % 4]}" opacity="{rng.uniform(.35, .7):.2f}"/>')
    return defs + f'<g filter="url(#{pid}f)">{macchie}</g>' + _testo(w * .06, h * .09, h * .035, p["ink"], parola.upper()[:24], peso=600)


def matrice(w, h, p, rng, pid, parola=""):
    """Lettere in griglia a puntini, con un alone sfocato dietro come luce in movimento."""
    t, cols, rows = ((parola or "Aa").upper() * 12), 3, 4
    cw, ch = w * .86 / cols, h * .86 / rows
    defs = f'<filter id="{pid}b"><feGaussianBlur stdDeviation="{w*.02:.0f}"/></filter>'
    alone = punti = ""
    for i in range(cols * rows):
        x, y = w * .07 + (i % cols) * cw + cw / 2, h * .07 + (i // cols) * ch + ch * .82
        base = f'text-anchor="middle" textLength="{cw*.8:.0f}" lengthAdjust="spacingAndGlyphs"'
        alone += _testo(x + cw * .05, y + ch * .04, ch * .95, p["carta"], t[i], base + ' opacity=".55"')
        punti += _testo(x, y, ch * .95, "none", t[i], base + f' stroke="{p["carta"]}" stroke-width="{ch*.035:.1f}" stroke-dasharray="{ch*.03:.1f} {ch*.05:.1f}"')
    return defs + f'<g filter="url(#{pid}b)">{alone}</g>{punti}'


def stropicciato(w, h, p, rng, pid, parola=""):
    """Righe di testo nero a sinistra, coperte da strisce di carta stropicciata."""
    n, t = 8, (parola or "Aa").upper()[:12]
    defs = (f'<filter id="{pid}f" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".03" numOctaves="3" seed="{rng.randrange(99)}"/>'
            f'<feDisplacementMap in="SourceGraphic" scale="{w*.05:.0f}"/><feDropShadow dx="2" dy="3" stdDeviation="2.5" flood-color="#000" flood-opacity=".3"/></filter>')
    righe = "".join(_testo(w * .04, (i + .88) * h / n, h / n * .9, p["ink"], t, peso=800) for i in range(n))
    strisce = ""
    for _ in range(9):
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        d = "M" + "L".join(f"{(x := x + rng.uniform(-.2, .25) * w):.0f} {(y := y + rng.uniform(-.1, .2) * h):.0f}" for _ in range(5))
        strisce += f'<path d="{d}" fill="none" stroke="{p["carta"]}" stroke-width="{w*.07:.0f}" stroke-linecap="round" stroke-linejoin="round" opacity=".85"/>'
    return defs + righe + f'<g filter="url(#{pid}f)">{strisce}</g>'


TIPOGRAFICI = (specchio, ornamento, gonfiato, xilografia, rilievo, vortice, acquerello, matrice, stropicciato)
