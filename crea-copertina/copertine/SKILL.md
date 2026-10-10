---
name: crea-copertina
description: Crea copertine, banner, poster e favicon in SVG in stile paperback vintage / bauhaus / tipografico, prendendo spunto da riferimenti (screenshot, siti, profili). Ogni cover è fatta di due livelli (fondo + soggetto) da cui si rigenerano la cover orizzontale, la verticale e il banner delle dashboard. Usare quando l'utente chiede una copertina, cover, banner, header, favicon o "grafica" per una pagina, un report, un progetto o un post, o quando condivide immagini/link di ispirazione grafica.
---

# copertine

Claude genera le copertine: guarda i riferimenti, sceglie forme e colori, disegna **due livelli** in SVG (fondo e soggetto), ne ricava le cover, controlla il risultato e lo mette nel progetto.
La libreria Python `copertine` è il punto di partenza, non un limite: se un riferimento chiede una forma che non c'è, si disegna a mano o si aggiunge uno stile.

## Prima di iniziare

Trova la libreria: `python -c "import copertine, os; print(os.path.dirname(copertine.__file__))"` (di seguito `LIB`; contiene `stili.py`, `palette.py`). Gli script dei livelli stanno un livello sopra, in `LIB/..` (la cartella `crea-copertina` del clone di `skill-vetrina`): `livelli.py`, `livelli_bbox.js`, `livelli_bbox_intero.js`, `componi.py`.
Se l'import fallisce: nel clone di `skill-vetrina`, `cd crea-copertina && pip install -e .`. Gli script `.js` usano Playwright per Node (`npm i playwright` e `npx playwright install chromium`).

## I file di una cover (sempre in `docs/img/` del progetto, nomi esatti)

| File | Cosa contiene | Dove si usa |
|---|---|---|
| `cover_sfondo.svg` | **solo il fondo**: colore, sfumatura, grafica leggera di fondo, grana. 1600x900, `preserveAspectRatio="xMidYMax slice"` | fondo continuo della cover delle pagine (desktop e telefono) e delle card del sito |
| `cover_soggetto.svg` | **solo il soggetto** (la B di Bitcoin, l'auto, l'icona…) su fondo trasparente; `viewBox` stretto attorno al disegno con un margine, più `width`/`height` uguali al viewBox | sotto i testi: da metà schermo su desktop, sotto il titolo su telefono |
| `cover_orizzontale.svg`, `cover_verticale.svg` | 1600x900 e 1080x1350, **generate** dai due livelli con `componi.py` (fondo su tutta la tela, soggetto da metà altezza in giù) | card del sito su desktop (`progetto.json` → `img`), ripiego delle pagine senza livelli |
| `favicon.svg` | quadrato 64x64 con angoli arrotondati | icona di pagine e dashboard |
| `banner_sfondo.svg`, `banner_soggetto.svg` | i due livelli del **banner delle dashboard** (di solito copia di `cover_sfondo`/`cover_soggetto`) | testata delle dashboard (skill `crea-dashboard-html`) |
| `banner_soggetto_ruotato.svg` | solo per soggetti a striscia: il soggetto ruotato di 90°, base a destra | banner delle dashboard su desktop |

**I due livelli sono la fonte**: orizzontale e verticale non si ritoccano a mano, si rigenerano con `python LIB/../componi.py docs/img`.

## Come devono essere i due livelli

- **Fondo** (`cover_sfondo.svg`): sopra ci va il titolo, anche su telefono, quindi niente bordi netti o bande che cambiano colore a metà altezza (al massimo una sfumatura morbida). Le decorazioni (cerchi, archi, barre, linee) vanno **nella fascia centrale** della tela (circa x 450–1150): le card verticali (5:7) e le card su telefono tagliano i lati, e ai bordi non si vedrebbero. Grana come ultimo elemento.
- **Soggetto** (`cover_soggetto.svg`): il disegno **intero**, mai tagliato da un bordo (se nella cover originale usciva dal fondo, nel soggetto va completato o chiuso), con un margine attorno anche sotto: le pagine e le card lo mettono da metà altezza in giù **con spazio sotto**.
  - **Striscia a tutta larghezza** (rapporto larghezza/altezza > 2,6, es. onde o bande): è l'unico caso che arriva al bordo inferiore. Nelle pagine e nel banner l'`<img>` prende la classe `largo`; per il banner su desktop serve anche `banner_soggetto_ruotato.svg`.
  - **Niente `filter` su `<image>`** (es. `feDropShadow` su un PNG): Safari lo disegna con un rettangolo nero. Per l'ombra metti sotto un rettangolo arrotondato sfocato (`feGaussianBlur` su una forma).
- Per cover nuove disegna già a livelli: un gruppo per il fondo, uno per il soggetto, la grana per ultima, così la separazione è immediata.

## Flusso

0. **Cosa è già stato fatto.** Leggi `fatte/indice.md` (`LIB/../fatte/`) e guarda gli SVG elencati. Ogni nuova copertina deve essere diversa da quelle già fatte per stile, composizione e palette, salvo richiesta esplicita.
1. **Riferimenti.** Se l'utente li dà, leggili: screenshot (Read sul file), link o profili (Chrome; se serve il login lo fa l'utente, mai inserire credenziali). Annota palette, famiglie di forme, fondo (carta/nero/piatto), grana, peso dei titoli.
2. **Scelta.** Confronta con stili e palette della libreria (`python -m copertine galleria -o galleria.html`). In ordine: uno stile esistente con una palette presa dal riferimento (aggiungila in `LIB/palette.py` se riusabile); un nuovo stile (`LIB/stili.py` + voce in `STILI`, poi `python test_copertine.py`); un SVG disegnato a mano. Copertine di progetti diversi non devono sembrare la stessa; aggiungi sempre un elemento legato al tema.
3. **Disegna i due livelli** in `docs/img/`:
   - **cover nuova**: scrivi direttamente `cover_sfondo.svg` e `cover_soggetto.svg` (regole sopra); per il soggetto lancia `node LIB/../livelli_bbox_intero.js docs/img/cover_soggetto.svg`, che stringe il viewBox attorno al disegno intero e scrive `width`/`height`.
   - **da una cover esistente** (o da un SVG generato con `python -m copertine <stile> -p <palette> -f banner|poster -o file.svg`): `python LIB/../livelli.py file.svg <indici dei figli della radice che sono il soggetto>` (es. `2`, `22-68`, oppure `g1:1-` se il soggetto è dentro il primo gruppo) scrive i due livelli accanto al file; poi `node LIB/../livelli_bbox.js docs/img/cover_soggetto.svg`. Se il soggetto risulta tagliato in fondo, usa `livelli_bbox_intero.js` (attenzione: i riquadri interni con `overflow="hidden"` diventano visibili; controlla che non spuntino elementi nascosti).
4. **Rigenera le cover**: `python LIB/../componi.py docs/img` → `cover_orizzontale.svg` e `cover_verticale.svg`.
5. **Favicon** `docs/img/favicon.svg`: quadrato 64x64, `rx` ≈ 14, contenuto ritagliato con `clipPath` (il formato `favicon` della libreria lo fa già). Può essere semplificata, ma deve riprendere palette, forma principale ed elemento del tema. Guardala anche a 32 e 16px.
6. **Banner per le dashboard** (solo se il progetto ha una dashboard): copia `cover_sfondo.svg` → `banner_sfondo.svg` e `cover_soggetto.svg` → `banner_soggetto.svg` (oppure scomponi un banner 1200x400 con `livelli.py banner.svg <indici>`: scrive `banner_sfondo`/`banner_soggetto`). Se il soggetto è una striscia, crea anche `banner_soggetto_ruotato.svg`: lo stesso disegno in un `<g transform="translate(0 W) rotate(-90) translate(-x -y)">` con viewBox `0 0 H W` (base della striscia sul bordo destro).
7. **Guarda il risultato** (Playwright/Chrome, poi Read sullo screenshot): i due livelli separati (il soggetto su una scacchiera, per vedere trasparenze e tagli), le cover rigenerate, e la pagina o la card dove andranno, **su desktop e a 390px**. Un grafico non è finito finché non l'hai visto.
8. **Itera** sui commenti dell'utente: cambia solo ciò che chiede, poi rigenera con `componi.py`.
9. **Registra la copertina fatta**, quando l'utente la accetta: `python -m copertine registra --svg docs/img/cover_orizzontale.svg --progetto <nome-repo-github> --note "stile di partenza, palette, elemento legato al tema"`. Copia lo SVG in `fatte/` e aggiunge una riga a `fatte/indice.md` (serve a non ripetere le copertine).
10. **Scheda e sito.** Richiama la skill `crea-scheda-progetto` (`docs/progetto.json`, `img` = `img/cover_verticale.svg`). Per mettere il progetto sul sito `FedeGambe.github.io` basta aggiungere `{ "repo": "<nome-repo>" }` in `progetti.json` (vedi `ISTRUZIONI.md` del sito): card, cover e livelli si leggono dalla repo del progetto.

## Come vengono usati (per controllare il risultato)

- **Pagine HTML** (skill `crea-pagina-html`): desktop → fondo a tutto schermo, testi in alto, soggetto da metà schermo con margine sotto (le strisce arrivano al bordo). Telefono → solo il titolo prima della grafica; poi il soggetto, con testo introduttivo e tag sopra la sua parte bassa su una sfumatura di `--cover` (le strisce arrivano al bordo inferiore, dietro ai testi).
- **Card del sito**: desktop (5:7) → fondo, testi in alto, soggetto nella metà bassa. Telefono (orizzontali) → titolo, soggetto, descrizione e tag sopra la sua parte bassa su una sfumatura.
- **Banner delle dashboard** (skill `crea-dashboard-html`): desktop → titolo a sinistra, soggetto a destra (striscia: ruotata, a tutta altezza, larga metà schermo); telefono → come le pagine.

## Regole

- Stili e galleria sono **esempi da cui prendere ispirazione**: per ogni progetto adattali e aggiungi un elemento legato al tema. **Non creare script generatori nel progetto di destinazione**: genera con i comandi sopra o con Python al volo, tieni gli script temporanei nello scratchpad, nel progetto lascia solo gli SVG.
- Ispirazione, non copia: prendi palette, composizione e atmosfera; non riprodurre illustrazioni, loghi, titoli o testi del riferimento.
- Riferimenti da siti/profili: solo ciò che è visibile pubblicamente o con l'accesso che l'utente stesso ha dato.
- Il font Archivo nel poster SVG compare solo se installato o caricato dalla pagina; altrimenti c'è un ripiego.
- `python -m copertine pubblica` riscrive tutto `progetti.json` del sito con voci complete prese da `fatte/` (solo locale): non usarlo per aggiungere un progetto al sito, basta la riga `{ "repo": ... }`.
- Mantieni la libreria piccola: una funzione per stile, nessuna dipendenza.
