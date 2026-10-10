# copertine

Copertine SVG in stile paperback vintage (palette piatte, forme geometriche, grana). Nessuna dipendenza.

- **Stili** (26): geometrici (bersaglio, cerchio_diviso, diagonali, spirale, cornici, onde, moire), tipografici (tipo_gigante, glifo, lettere_ruotate, stecche), 3D (sfere, cubi_isometrici, orizzonte), illustrati (testa_labirinto, occhio, organico), da poster tipografici (specchio, ornamento, gonfiato, xilografia, rilievo, vortice, acquerello, matrice, stropicciato) in `copertine/stili.py`, `stili_illustrati.py` e `stili_tipografici.py`
- **Palette**: retro, mattone, mostarda, notte, smeraldo, rosa, carbone, mare, neon, girandola, burro, acquerello, inchiostro, grafite (`copertine/palette.py`)
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
git clone https://github.com/FedeGambe/skill-vetrina
cd skill-vetrina/crea-copertina
pip install -e .
python -m copertine installa-skill                         # copia la skill in ~/.claude/skills/crea-copertina
```

Serve il clone con `-e` (non `pip install git+...`): `fatte/` sta nel clone e non è su GitHub; il clone serve anche per modificare stili e palette (poi committa/pusha).
`pubblica` cerca il sito `FedeGambe.github.io` accanto alla cartella di lavoro: è il setup dell'autore, altrimenti ignoralo.
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

## Cover a due livelli

Ogni cover di progetto è fatta di due file in `docs/img/`: `cover_sfondo.svg` (solo il fondo: colore, sfumatura, grafica leggera, grana) e `cover_soggetto.svg` (solo il soggetto su fondo trasparente, viewBox stretto attorno al disegno). Sono la fonte: pagine, card del sito e banner delle dashboard li usano separati, e le cover intere si rigenerano da loro.

```
python livelli.py docs/img/cover_orizzontale.svg 2      # scompone una cover esistente (2 = indice del figlio che è il soggetto; g1:1- = figli 1.. del gruppo 1)
node livelli_bbox.js docs/img/cover_soggetto.svg         # stringe il viewBox del soggetto (Playwright per Node)
node livelli_bbox_intero.js docs/img/cover_soggetto.svg  # idem, ma misura il disegno intero (se era tagliato in fondo)
python componi.py docs/img                               # rigenera cover_orizzontale.svg e cover_verticale.svg dai due livelli
```

`livelli.py banner.svg …` scrive invece `banner_sfondo.svg` e `banner_soggetto.svg` (banner delle dashboard). Regole per disegnarli: `copertine/SKILL.md`.

## Sito dei progetti

Il sito `FedeGambe.github.io` legge card, scheda (`docs/progetto.json`) e immagini direttamente dalle repo dei progetti: per aggiungere un progetto basta una riga `{ "repo": "nome" }` nel suo `progetti.json` (vedi `ISTRUZIONI.md` del sito). I comandi `sito` e `pubblica` qui sotto sono del vecchio flusso e **riscrivono tutto `progetti.json`**: non usarli per aggiornare il sito.

`fatte/progetti.json` è l'elenco delle card (titolo, descrizione, tag, anno, link, cover). Per aggiornare il sito:

```
python -m copertine sito -o ../FedeGambe.github.io     # copia le cover in img/ e scrive progetti.json
```

`index.html` del sito legge `progetti.json` (serve un server: GitHub Pages va bene, in locale `python -m http.server`). Nuovo progetto, in un comando (registra + sito + commit nelle due repo; `--push` per pubblicare):

```
python -m copertine pubblica --svg cover.svg --progetto <repo> --titolo "Titolo" --desc "Descrizione" --tag "A,B" --live /<repo>/ -o ../FedeGambe.github.io
```
