# copertine

Copertine SVG in stile paperback vintage (palette piatte, forme geometriche, grana). Nessuna dipendenza.

- **Stili** (17): geometrici (bersaglio, cerchio_diviso, diagonali, spirale, cornici, onde, moire), tipografici (tipo_gigante, glifo, lettere_ruotate, stecche), 3D (sfere, cubi_isometrici, orizzonte), illustrati (testa_labirinto, occhio, organico) in `copertine/stili.py` e `stili_illustrati.py`
- **Palette**: retro, mattone, mostarda, notte, smeraldo, rosa, carbone, mare (`copertine/palette.py`)
- **Formati**: banner 1200x400, poster 1080x1350 (con titolo), schermo 1600x900 (cover a tutto schermo, titolo in HTML sopra), favicon 64x64

```
pip install -e .                      # una volta, poi si usa da qualsiasi progetto
python -m copertine galleria          # anteprima di tutti gli stili -> galleria.html
python -m copertine spirale -p mattone -f poster -t "Titolo" -s "Sottotitolo" -o copertina.svg
```

```python
from copertine import genera, favicon_uri
svg = genera("cerchio_diviso", "retro", "banner")
href = favicon_uri("cerchio_diviso", "retro")   # <link rel="icon" href="...">
```

Nuovo stile: una funzione in `stili.py` e aggiungila a `STILI`. Nuova palette: una voce in `PALETTE`. `python test_copertine.py` controlla tutte le combinazioni.

## Installazione (su qualsiasi PC)

```
pip install git+https://github.com/<utente>/copertine     # libreria + comando
python -m copertine installa-skill                         # copia la skill in ~/.claude/skills/copertine
```

Per modificare o aggiungere stili e palette: `git clone`, poi `pip install -e .` nel clone, e committa/pusha le modifiche.
Dopo l'installazione riavvia Claude Code: basta chiedere una copertina in qualsiasi progetto.

## Uso con Claude

La skill (`copertine/SKILL.md`, unica fonte, viaggia dentro il pacchetto) dice a Claude come usare la libreria: legge i riferimenti (screenshot, siti), sceglie o crea stile e palette, genera l'SVG, lo controlla nel browser e lo inserisce nel progetto.

## Esempi

- `esempi/galleria.html`: copertine di esempio per tutti gli stili, da cui prendere ispirazione e da adattare a ogni progetto (`python -m copertine galleria`).
- `esempi/ispirazioni/`: riferimenti grafici da cui sono nati stili e palette. `tiktok-gcanale.jpg` è uno screenshot di copertine del profilo TikTok @_gcanale: il lavoro grafico è dell'autore, qui solo come riferimento di ispirazione (rimuovere se richiesto).

## Copertine fatte

`fatte/` raccoglie le copertine realizzate per i progetti (SVG) con `fatte/indice.md`: progetto, data, stile di partenza, palette, note. Claude la legge prima di crearne una nuova per non ripetersi, e dopo ogni copertina accettata la registra con:

```
python -m copertine registra --svg copertina.svg --progetto nome --note "stile, palette, elemento legato al tema"
```

Funziona dal clone del repo (installazione `pip install -e .`), perché `fatte/` sta nella radice del repository.
