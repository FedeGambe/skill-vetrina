"""CLI:  python -m copertine <stile> [-p palette] [-f banner|poster|favicon] [-t titolo] [-s sottotitolo] [-o file.svg]
       python -m copertine galleria [-o galleria.html]     anteprima di tutti gli stili
       python -m copertine installa-skill                  installa la skill per Claude Code"""
import argparse
import shutil
from datetime import date
from pathlib import Path

from . import FORMATI, genera
from .palette import PALETTE
from .stili import STILI

# stile -> (palette, titolo, sottotitolo, parola, seed) per la galleria
DEMO = {
    "bersaglio": ("retro", "Il punto di mira", "Concentrazione", "", 0),
    "cerchio_diviso": ("mattone", "Metà e metà", "Due modi di guardare", "", 0),
    "diagonali": ("mostarda", "In salita", "Sempre più su", "", 3),
    "spirale": ("notte", "Senza uscita", "Un giro dopo l'altro", "", 0),
    "cornici": ("smeraldo", "Dentro la cornice", "Quadro nel quadro", "", 0),
    "onde": ("rosa", "Maree", "Andata e ritorno", "", 4),
    "sfere": ("carbone", "Due mondi", "Luce e ombra", "", 0),
    "tipo_gigante": ("mare", "Ad alta voce", "Il titolo è l'immagine", "GRIDA", 0),
    "glifo": ("retro", "Tra parentesi", "Un segno, tutto il resto", "", 1),
    "lettere_ruotate": ("mattone", "In verticale", "Tre dimensioni di carta", "ALTO", 0),
    "moire": ("mostarda", "Vertigine", "Gli occhi non stanno fermi", "", 0),
    "stecche": ("notte", "Caos calmo", "Tutto in disordine", "CAOS", 7),
    "testa_labirinto": ("retro", "Pensieri a spirale", "Il labirinto è dentro", "", 2),
    "cubi_isometrici": ("mostarda", "Costruire", "Un cubo alla volta", "", 0),
    "occhio": ("notte", "Sguardo", "Vedere oltre", "", 0),
    "organico": ("smeraldo", "Fioritura", "Forme che crescono", "", 5),
    "orizzonte": ("retro", "Tramonto", "L'ultima ora di luce", "", 0),
}


def galleria(uscita):
    celle = "".join(
        f'<figure><div>{genera(s, p, "poster", titolo=t, sottotitolo=sub, parola=parola, seed=seed)}</div>'
        f'<figcaption><b>{s}</b> · {p}</figcaption></figure>' for s, (p, t, sub, parola, seed) in DEMO.items() if s in STILI)
    Path(uscita).write_text(
        "<!doctype html><meta charset='utf-8'><title>Copertine</title>"
        "<link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Archivo:wght@600;900&display=swap'>"
        "<style>body{font:14px 'Archivo',sans-serif;background:#eee;margin:24px}h1{font-weight:900;margin:0 0 4px}p{margin:0 0 20px;color:#555}"
        "main{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:24px}figure{margin:0}"
        "svg{width:100%;height:auto;display:block;box-shadow:0 2px 12px #0003}figcaption{margin-top:8px}</style>"
        f"<h1>Copertine</h1><p>{len(DEMO)} stili, formato poster. Generate con <code>python -m copertine galleria</code>.</p><main>{celle}</main>",
        encoding="utf-8")


FATTE = Path(__file__).resolve().parent.parent / "fatte"  # richiede il clone / installazione editabile


def registra(svg, progetto, note):
    """Copia l'SVG in fatte/ e aggiunge una riga a fatte/indice.md: Claude le legge per non ripetere le copertine."""
    FATTE.mkdir(exist_ok=True)
    oggi = date.today().isoformat()
    nome = f"{oggi}-{progetto}.svg".replace(" ", "-")
    shutil.copy(svg, FATTE / nome)
    indice = FATTE / "indice.md"
    if not indice.exists():
        intestazione = ["# Copertine fatte", "", "Lette da Claude prima di crearne una nuova: non ripetere stile, composizione e palette già usati.", "",
                        "| Data | Progetto | File | Note |", "|---|---|---|---|"]
        indice.write_text("\n".join(intestazione) + "\n", encoding="utf-8")
    with indice.open("a", encoding="utf-8") as f:
        f.write(f"| {oggi} | {progetto} | [{nome}]({nome}) | {note} |\n")
    print("registrata in", FATTE / nome)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(prog="copertine")
    ap.add_argument("stile", choices=[*STILI, "galleria", "installa-skill", "registra"])
    ap.add_argument("--svg", help="registra: file SVG della copertina fatta")
    ap.add_argument("--progetto", help="registra: progetto per cui è stata fatta")
    ap.add_argument("--note", default="", help="registra: stile di partenza, palette, elemento legato al tema")
    ap.add_argument("-p", "--palette", choices=PALETTE, default="retro")
    ap.add_argument("-f", "--formato", choices=FORMATI, default="banner")
    ap.add_argument("-t", "--titolo", default="")
    ap.add_argument("-s", "--sottotitolo", default="")
    ap.add_argument("--parola", default="", help="parola per gli stili tipografici (default: prima parola del titolo)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("-o", "--output")
    a = ap.parse_args()
    if a.stile == "installa-skill":  # copia la skill di Claude Code in ~/.claude/skills/copertine
        dest = Path.home() / ".claude" / "skills" / "copertine"
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copy(Path(__file__).with_name("SKILL.md"), dest / "SKILL.md")
        print("skill installata in", dest)
    elif a.stile == "registra":  # salva la copertina in fatte/ e la annota in fatte/indice.md
        registra(Path(a.svg), a.progetto, a.note)
    elif a.stile == "galleria":
        galleria(a.output or "galleria.html")
    else:
        Path(a.output or f"{a.stile}-{a.palette}-{a.formato}.svg").write_text(
            genera(a.stile, a.palette, a.formato, a.titolo, a.sottotitolo, a.seed, parola=a.parola), encoding="utf-8")
