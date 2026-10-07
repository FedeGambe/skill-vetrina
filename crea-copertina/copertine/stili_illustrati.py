"""Stili illustrati e 3D: testa con labirinto, cubi isometrici, occhio, forme organiche, orizzonte retrò.
Stessa firma degli stili in stili.py: stile(w, h, p, rng, pid, parola)."""
import math

from .palette import chiaro, mescola


def testa_labirinto(w, h, p, rng, pid, parola=""):
    """Profilo di testa con un labirinto di anelli al posto del pensiero."""
    k = h * .9 / 120
    profilo = "M30 114L32 90C17 80 11 62 13 44C15 21 33 6 54 6C73 6 85 18 87 34L91 49L99 65L91 69L92 75L88 79L92 83L87 91L89 99L70 102L68 114Z"
    anelli = ""
    for r in range(7, 46, 5):
        c = 2 * math.pi * r
        anelli += (f'<circle cx="52" cy="46" r="{r}" fill="none" stroke="{p["acc"][3]}" stroke-width="2.6" stroke-dasharray="{c*.86:.1f} {c*.14:.1f}" '
                   f'transform="rotate({rng.randrange(360)} 52 46)"/>')
    return (f'<g transform="translate({w/2-52*k:.1f} {h*.05:.1f}) scale({k:.3f})"><clipPath id="{pid}t"><path d="{profilo}"/></clipPath>'
            f'<path d="{profilo}" fill="{p["carta"]}"/><g clip-path="url(#{pid}t)">{anelli}<circle cx="52" cy="46" r="4.5" fill="{p["acc"][0]}"/></g></g>')


def cubi_isometrici(w, h, p, rng, pid, parola=""):
    """Piramide di cubi in prospettiva isometrica, con tre facce in tre tonalità."""
    n = 5
    s = min(w / (1.732 * n + 1), h / (1.5 * n + .8)) * .98
    x0, y0 = w / 2, (h - s * (1.5 * (n - 1) + 2)) / 2 + s
    d, out = .866 * s, ""
    for r in range(n):
        for c in range(r + 1):
            x, y = x0 + (c - r / 2) * 1.732 * s, y0 + r * 1.5 * s
            col = p["acc"][(r + c) % 4]
            facce = [(f"{x:.1f},{y-s:.1f} {x+d:.1f},{y-s/2:.1f} {x:.1f},{y:.1f} {x-d:.1f},{y-s/2:.1f}", mescola(col, "#ffffff", .35)),
                     (f"{x-d:.1f},{y-s/2:.1f} {x:.1f},{y:.1f} {x:.1f},{y+s:.1f} {x-d:.1f},{y+s/2:.1f}", col),
                     (f"{x:.1f},{y:.1f} {x+d:.1f},{y-s/2:.1f} {x+d:.1f},{y+s/2:.1f} {x:.1f},{y+s:.1f}", mescola(col, "#000000", .4))]
            out += "".join(f'<polygon points="{pt}" fill="{f}" stroke="{p["sfondo"]}" stroke-width="{s*.04:.1f}" stroke-linejoin="round"/>' for pt, f in facce)
    return out


def occhio(w, h, p, rng, pid, parola=""):
    """Occhio stilizzato circondato da raggi."""
    cx, cy = w / 2, h / 2
    a = min(w * .36, h * .36)
    b = a * .5
    raggi = "".join(
        f'<line x1="{cx+a*1.12*math.cos(t):.1f}" y1="{cy+a*1.12*math.sin(t):.1f}" x2="{cx+a*(1.3+.12*(i%2))*math.cos(t):.1f}" y2="{cy+a*(1.3+.12*(i%2))*math.sin(t):.1f}" '
        f'stroke="{p["acc"][2]}" stroke-width="{a*.04:.1f}" stroke-linecap="round"/>'
        for i, t in enumerate(2 * math.pi * j / 36 for j in range(36)))
    mandorla = f"M{cx-a} {cy}Q{cx} {cy-2*b} {cx+a} {cy}Q{cx} {cy+2*b} {cx-a} {cy}Z"
    iride = "".join(f'<circle cx="{cx}" cy="{cy}" r="{b*k:.1f}" fill="{c}"/>' for k, c in [(.95, p["acc"][3]), (.7, p["acc"][1]), (.45, p["acc"][0]), (.22, p["sfondo"])])
    contorno = p["ink"] if chiaro(p["sfondo"]) else p["carta"]
    return (raggi + f'<clipPath id="{pid}o"><path d="{mandorla}"/></clipPath><path d="{mandorla}" fill="{p["carta"]}"/>'
            f'<g clip-path="url(#{pid}o)">{iride}<circle cx="{cx-b*.18:.1f}" cy="{cy-b*.2:.1f}" r="{b*.1:.1f}" fill="{p["carta"]}"/></g>'
            f'<path d="{mandorla}" fill="none" stroke="{contorno}" stroke-width="{a*.035:.1f}" stroke-linejoin="round"/>')


def _blob(cx, cy, r, rng, n=9):
    """Contorno morbido e irregolare (spline di Catmull-Rom chiusa)."""
    pts = [(cx + r * (.65 + .55 * rng.random()) * math.cos(2 * math.pi * i / n), cy + r * (.65 + .55 * rng.random()) * math.sin(2 * math.pi * i / n)) for i in range(n)]
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        d += f"C{p1[0]+(p2[0]-p0[0])/6:.1f} {p1[1]+(p2[1]-p0[1])/6:.1f} {p2[0]-(p3[0]-p1[0])/6:.1f} {p2[1]-(p3[1]-p1[1])/6:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d + "Z"


def organico(w, h, p, rng, pid, parola=""):
    """Forme morbide sovrapposte con contorno spesso, come un disegno a inchiostro."""
    colori = p["acc"] + [p["carta"]]
    tratto = p["ink"] if chiaro(p["sfondo"]) else p["sfondo"]
    m = min(w, h)
    forme = "".join(
        f'<path d="{_blob(rng.uniform(w*.15, w*.85), rng.uniform(h*.15, h*.85), m*rng.uniform(.18, .34), rng)}" fill="{colori[i % 5]}" stroke="{tratto}" stroke-width="{m*.012:.1f}" stroke-linejoin="round"/>'
        for i in range(9))
    puntini = "".join(f'<circle cx="{rng.uniform(0, w):.0f}" cy="{rng.uniform(0, h):.0f}" r="{m*rng.uniform(.004, .012):.1f}" fill="{p["carta"]}"/>' for _ in range(40))
    return forme + puntini


def orizzonte(w, h, p, rng, pid, parola=""):
    """Sole a strisce su una griglia in prospettiva."""
    y0, R, a = h * .58, min(w, h) * .3, p["acc"]
    sole = (f'<linearGradient id="{pid}s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a[2]}"/><stop offset="1" stop-color="{a[0]}"/></linearGradient>'
            f'<circle cx="{w/2}" cy="{y0-R*.55:.1f}" r="{R:.1f}" fill="url(#{pid}s)"/>')
    strisce = "".join(f'<rect x="{w/2-R}" y="{y0-R*.55+R*(.12+i*.09):.1f}" width="{2*R}" height="{R*.012*(i+1)*1.6:.1f}" fill="{p["sfondo"]}"/>' for i in range(5))
    terra = f'<rect y="{y0:.1f}" width="{w}" height="{h-y0:.1f}" fill="{mescola(p["sfondo"], "#000000", .35)}"/>'
    raggi = "".join(f'<line x1="{w/2}" y1="{y0}" x2="{w/2+(i-9)*w*.14:.0f}" y2="{h}" stroke="{a[3]}" stroke-width="{h*.006:.1f}"/>' for i in range(19))
    righe = "".join(f'<line x1="0" y1="{y0+(h-y0)*(k/7)**2:.1f}" x2="{w}" y2="{y0+(h-y0)*(k/7)**2:.1f}" stroke="{a[3]}" stroke-width="{h*.006:.1f}"/>' for k in range(1, 8))
    return sole + strisce + terra + raggi + righe


NUOVI = (testa_labirinto, cubi_isometrici, occhio, organico, orizzonte)
