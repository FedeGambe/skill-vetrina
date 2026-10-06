"""Ogni stile x palette x formato deve produrre SVG ben formato:  python test_copertine.py"""
import xml.etree.ElementTree as ET

from copertine import FORMATI, favicon_uri, genera
from copertine.palette import PALETTE
from copertine.stili import STILI

for s in STILI:
    for p in PALETTE:
        for f in FORMATI:
            ET.fromstring(genera(s, p, f, titolo="Titolo di prova abbastanza lungo", sottotitolo="Sotto & titolo"))
assert favicon_uri("bersaglio").startswith("data:image/svg+xml,")
print("ok", len(STILI) * len(PALETTE) * len(FORMATI), "combinazioni")
