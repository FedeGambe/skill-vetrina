"""Stili: ogni funzione disegna nel rettangolo (0,0)-(w,h) e restituisce frammenti SVG.
Firma: stile(w, h, p, rng, pid, parola) con p = palette, rng = random.Random, pid = prefisso per gli id,
parola = testo per gli stili tipografici (gli altri la ignorano)."""
import math
from html import escape

from .palette import chiaro

FONT = "Archivo, 'Archivo Black', 'Helvetica Neue', Arial, sans-serif"


def bersaglio(w, h, p, rng, pid, parola=""):
    R, a = min(w, h) * .45, p["acc"]
    anelli = [(1, a[3]), (.76, p["carta"]), (.52, a[3]), (.28, a[0]), (.08, p["sfondo"])]
    return "".join(f'<circle cx="{w/2}" cy="{h/2}" r="{R*k:.1f}" fill="{c}"/>' for k, c in anelli)


def cerchio_diviso(w, h, p, rng, pid, parola=""):
    cx, cy, R, a = w / 2, h / 2, min(w, h) * .45, p["acc"]
    sinistra = f"M{cx} {cy-R}A{R} {R} 0 0 0 {cx} {cy+R}Z"
    fasce = "".join(f'<rect x="{cx-R}" y="{cy-R+i*R/2:.1f}" width="{R}" height="{R/2+1:.1f}" fill="{a[i]}"/>' for i in range(4))
    return (f'<clipPath id="{pid}c"><path d="{sinistra}"/></clipPath>'
            f'<path d="M{cx} {cy-R}A{R} {R} 0 0 1 {cx} {cy+R}Z" fill="{p["carta"]}"/><g clip-path="url(#{pid}c)">{fasce}</g>')


def diagonali(w, h, p, rng, pid, parola=""):
    larg, n, a = w / 11, 5, p["acc"]
    x0 = w * (.18 + rng.random() * .1)
    return "".join(
        f'<path d="M{x0+i*larg*1.7:.1f} {h}L{x0+i*larg*1.7+h*.6:.1f} 0h{larg:.1f}L{x0+i*larg*1.7+larg:.1f} {h}Z" fill="{a[i % 4]}"/>'
        for i in range(n))


def spirale(w, h, p, rng, pid, parola=""):
    R, giri = min(w, h) * .46, 9
    pts = []
    for i in range(int(giri * 60)):
        t = i / 60 * 2 * math.pi
        r = R * t / (giri * 2 * math.pi)
        pts.append(f"{w/2 + r*math.cos(t):.1f},{h/2 + r*math.sin(t):.1f}")
    return (f'<polyline points="{" ".join(pts)}" fill="none" stroke="{p["acc"][0]}" stroke-width="{R/26:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="{w/2}" cy="{h/2}" r="{R/12:.1f}" fill="{p["carta"]}"/>')


def cornici(w, h, p, rng, pid, parola=""):
    S, a = min(w, h) * .86, p["acc"]
    livelli = [(1, a[0]), (.8, a[1]), (.6, a[2]), (.42, p["sfondo"])]
    quadrati = "".join(f'<rect x="{(w-S*k)/2:.1f}" y="{(h-S*k)/2:.1f}" width="{S*k:.1f}" height="{S*k:.1f}" fill="{c}"/>' for k, c in livelli)
    return quadrati + f'<circle cx="{w/2}" cy="{h/2}" r="{S*.14:.1f}" fill="{p["carta"]}"/>'


def onde(w, h, p, rng, pid, parola=""):
    n, A, lam, fase = 8, h * .07, w * (.35 + rng.random() * .25), rng.random() * 6
    colori = p["acc"] + [p["carta"], p["sfondo"]]

    def curva(i):
        return [(x, h * i / n - h * .1 + A * math.sin(2 * math.pi * x / lam + fase + i * .7)) for x in range(0, int(w) + 21, 20)]
    fasce = ""
    for i in range(n + 1):
        sopra, sotto = curva(i), curva(i + 1)[::-1]
        d = "M" + "L".join(f"{x},{y:.1f}" for x, y in sopra + sotto) + "Z"
        fasce += f'<path d="{d}" fill="{colori[i % len(colori)]}"/>'
    return fasce


def sfere(w, h, p, rng, pid, parola=""):
    R, a = min(w, h) * .3, p["acc"]
    defs = (f'<radialGradient id="{pid}l" cx=".32" cy=".28" r=".5"><stop offset="0" stop-color="#fff" stop-opacity=".7"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="{pid}o" cx=".5" cy=".5" r=".5"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".45"/></radialGradient>')
    sfera = lambda cx, cy, r, c: "".join(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{f}"/>' for f in (c, f"url(#{pid}o)", f"url(#{pid}l)"))
    return defs + sfera(w * .36, h * .5, R, a[0]) + sfera(w * .66, h * .52, R * .62, a[1])


def tipo_gigante(w, h, p, rng, pid, parola=""):
    """La parola ripetuta su più righe, compressa a tutta larghezza."""
    n, base = 3, (p["ink"] if chiaro(p["sfondo"]) else p["carta"])
    colori = [base, p["acc"][0], p["acc"][2]]
    return "".join(
        f'<text x="{w*.03:.0f}" y="{(i+.92)*h/n:.0f}" font-family="{FONT}" font-weight="900" font-size="{h/n*1.05:.0f}" '
        f'textLength="{w*.94:.0f}" lengthAdjust="spacingAndGlyphs" fill="{colori[i % 3]}">{escape(parola.upper() or "AA")}</text>' for i in range(n))


def glifo(w, h, p, rng, pid, parola=""):
    """Un segno tipografico enorme al centro."""
    segno = ["{}", "()", "[]", "&", "?", "@", "%"][rng.randrange(7)]
    return (f'<text x="{w/2}" y="{h/2}" text-anchor="middle" dominant-baseline="central" font-family="Georgia, serif" '
            f'font-size="{min(w, h*1.5)*.75:.0f}" fill="{p["acc"][0]}">{escape(segno)}</text>')


def lettere_ruotate(w, h, p, rng, pid, parola=""):
    """Lettere in verticale con estrusione 3D."""
    t = escape((parola or "Aa").upper()[:6])
    def copia(dx, colore):
        return (f'<g transform="translate({w/2+dx:.1f} {h/2+dx:.1f}) rotate(-90)"><text text-anchor="middle" dominant-baseline="central" font-family="{FONT}" font-weight="900" '
                f'font-size="{w*.6:.0f}" textLength="{h*.72:.0f}" lengthAdjust="spacingAndGlyphs" fill="{colore}">{t}</text></g>')
    return "".join(copia(i * 2.2, p["acc"][0]) for i in range(14, 0, -1)) + copia(0, p["carta"])


def moire(w, h, p, rng, pid, parola=""):
    """Cerchi concentrici sfalsati: effetto op-art."""
    R, n = min(w, h) * .48, 60
    return "".join(
        f'<circle cx="{w/2 + i/n*R*.35:.1f}" cy="{h/2 - i/n*R*.2:.1f}" r="{R*(1-i/n):.1f}" fill="none" '
        f'stroke="{p["acc"][0] if i % 2 else p["carta"]}" stroke-width="{R/n*.9:.2f}"/>' for i in range(n))


def stecche(w, h, p, rng, pid, parola=""):
    """Stecche sparse e inclinate, con la parola tagliata a destra."""
    grigi = [p["carta"], p["acc"][1], p["acc"][3]]
    stecche = "".join(
        f'<rect x="{rng.uniform(0, w*.8):.0f}" y="{rng.uniform(0, h):.0f}" width="{rng.uniform(w*.08, w*.22):.0f}" height="{rng.uniform(h*.03, h*.06):.0f}" '
        f'fill="{grigi[i % 3]}" opacity=".85" transform="rotate({rng.uniform(-70, 70):.0f} {w/2} {h/2})"/>' for i in range(26))
    return stecche + (f'<text x="{w*1.02:.0f}" y="{h*.92:.0f}" text-anchor="end" font-family="{FONT}" font-weight="900" font-size="{h*.95:.0f}" '
                      f'textLength="{w*.55:.0f}" lengthAdjust="spacingAndGlyphs" fill="{p["acc"][0]}">{escape((parola or "Aa").upper())}</text>')


STILI = {f.__name__: f for f in (bersaglio, cerchio_diviso, diagonali, spirale, cornici, onde, sfere,
                                  tipo_gigante, glifo, lettere_ruotate, moire, stecche)}

from .stili_illustrati import NUOVI  # noqa: E402

STILI.update({f.__name__: f for f in NUOVI})
