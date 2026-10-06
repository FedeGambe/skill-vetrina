"""Palette: sfondo, carta (colore chiaro), ink (testo su fondo chiaro) e 4 colori d'accento."""

PALETTE = {
    "retro":    dict(sfondo="#14161f", carta="#efe3c8", ink="#14161f", acc=["#d6452a", "#e8872b", "#e8b923", "#2a8c99"]),
    "mattone":  dict(sfondo="#b3261e", carta="#f0e6d2", ink="#0d0d0d", acc=["#0d0d0d", "#e8b923", "#f0e6d2", "#7a1410"]),
    "mostarda": dict(sfondo="#e8b923", carta="#f6efd9", ink="#14110a", acc=["#14110a", "#f6efd9", "#c98a12", "#a8301a"]),
    "notte":    dict(sfondo="#101a33", carta="#f2ead7", ink="#101a33", acc=["#e0a82e", "#d6452a", "#4aa3b5", "#f2ead7"]),
    "smeraldo": dict(sfondo="#101612", carta="#e9efe3", ink="#101612", acc=["#2fae74", "#8fe0a8", "#1d6a4a", "#e9efe3"]),
    "rosa":     dict(sfondo="#f4a0c0", carta="#ffffff", ink="#111111", acc=["#e30613", "#111111", "#ffffff", "#ffd0e0"]),
    "carbone":  dict(sfondo="#0a0a0a", carta="#ffffff", ink="#0a0a0a", acc=["#ffffff", "#9a9a9a", "#e30613", "#4a4a4a"]),
    "mare":     dict(sfondo="#3d8fc4", carta="#f0e6d2", ink="#0d1a2b", acc=["#d6452a", "#0d1a2b", "#f0e6d2", "#8fc3e0"]),
    "neon":     dict(sfondo="#050805", carta="#eaffe0", ink="#050805", acc=["#39ff14", "#1fa30a", "#b6ff9e", "#0d4d05"]),
    "girandola": dict(sfondo="#ffcc00", carta="#fff3c4", ink="#1a1200", acc=["#d4003c", "#1a1200", "#fff3c4", "#a30030"]),
    "burro":    dict(sfondo="#ffd400", carta="#fff6b8", ink="#2a2000", acc=["#f2bf00", "#fff6b8", "#c99700", "#2a2000"]),
    "acquerello": dict(sfondo="#f1ead9", carta="#fbf7ea", ink="#1b2a33", acc=["#1d4e6b", "#4f8fa6", "#a9c9d1", "#0f2a3a"]),
    "inchiostro": dict(sfondo="#f4f4f1", carta="#ffffff", ink="#0b0b0b", acc=["#0b0b0b", "#b9a86a", "#555555", "#e0e0dc"]),
    "grafite":  dict(sfondo="#12100d", carta="#8a8f8f", ink="#12100d", acc=["#3b4a4a", "#5a3a32", "#2c3a3b", "#c9502a"]),
}


def chiaro(colore):
    """True se il colore #rrggbb è chiaro (serve testo scuro sopra)."""
    r, g, b = (int(colore[i:i + 2], 16) for i in (1, 3, 5))
    return 0.299 * r + 0.587 * g + 0.114 * b > 140


def mescola(colore, altro, t):
    """Colore mescolato con `altro` (#rrggbb) in misura t (0..1): per ombre e luci."""
    a = [int(colore[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(altro[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(a, b))
