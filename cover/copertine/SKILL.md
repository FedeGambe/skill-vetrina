---
name: copertine
description: Crea copertine, banner, poster e favicon in SVG in stile paperback vintage / bauhaus / tipografico, prendendo spunto da riferimenti (screenshot, siti, profili). Usare quando l'utente chiede una copertina, cover, banner, header, favicon o "grafica" per una pagina, un report, un progetto o un post, o quando condivide immagini/link di ispirazione grafica.
---

# copertine

Claude genera le copertine: guarda i riferimenti, sceglie forme e colori, produce SVG, controlla il risultato e lo inserisce nel progetto.
La libreria Python `copertine` è il punto di partenza, non un limite: se un riferimento chiede una forma che non c'è, si disegna a mano o si aggiunge uno stile.

## Prima di iniziare

Trova la libreria: `python -c "import copertine, os; print(os.path.dirname(copertine.__file__))"` (di seguito `LIB`; contiene `stili.py`, `palette.py`).
Se l'import fallisce: `pip install git+https://github.com/<utente>/copertine` oppure, nel clone del repo, `pip install -e .`.
Per estendere stili e palette in modo duraturo serve l'installazione editabile da un clone (le modifiche vanno poi committate e pushate).

## Flusso

0. **Cosa è già stato fatto.** Prima di tutto leggi `fatte/indice.md` nella radice del repo (`LIB/../fatte/`) e guarda gli SVG elencati (Read o browser). Ogni nuova copertina deve essere diversa da quelle già fatte per stile di partenza, composizione e palette: non copiarle, a meno che l'utente chieda esplicitamente di riprenderne una.
1. **Riferimenti.** Se l'utente li dà, leggili: screenshot (Read sul file immagine), link o profili (Chrome con `mcp__claude-in-chrome__*`; se serve il login, l'utente lo fa da sé nella finestra, mai inserire credenziali). Annota palette, famiglie di forme (cerchi, strisce, tipografia gigante, op-art...), fondo (carta/nero/piatto), grana, peso dei titoli.
2. **Scelta.** Confronta con gli stili e le palette della libreria (`python -m copertine galleria -o galleria.html` per vederli). Opzioni, in ordine:
   - uno stile esistente con una palette presa dal riferimento (aggiungila in `LIB/palette.py` se è riusabile);
   - un nuovo stile: funzione in `LIB/stili.py` + voce in `STILI`, poi `python test_copertine.py` dalla radice del repo;
   - un SVG disegnato a mano per un caso unico.
   Preferire sempre di variare: copertine di progetti diversi non devono sembrare la stessa.
3. **Genera.**
   ```
   python -m copertine <stile> -p <palette> -f banner|poster|favicon -t "Titolo" -s "Sottotitolo" [--parola X] [--seed N] -o file.svg
   ```
   In Python: `from copertine import genera, favicon_uri`.
4. **Guarda il risultato.** Apri l'SVG o la pagina con una skill/strumento da browser (es. `browser-automation` con `--screenshot`, poi Read sul PNG) o con Chrome. Con `file://` su Windows usa percorsi `C:/...` con `%20` per gli spazi. Un grafico non è finito finché non l'hai visto.
5. **Integra.** Se la pagina ha titolo e testo di apertura, fai una **cover a grandezza schermo** (non un banner sotto il testo): sezione alta esattamente `100svh`, SVG assoluto a tutto schermo (`inset:0`, `preserveAspectRatio="xMidYMax slice"`, formato `schermo` 1600x900 con la grafica nel 62% inferiore), titolo e sottotitolo HTML a tutta larghezza in alto nei colori della palette (z-index sopra l'SVG), diciture in basso. Banner: SVG inline nella pagina (`preserveAspectRatio="xMidYMid slice"` con altezza fissata via CSS). Favicon: `<link rel="icon" type="image/svg+xml" href="{favicon_uri(...)}">`. Allinea i colori della pagina alla palette (variabili CSS, tema scuro compreso).
6. **Itera** sui commenti dell'utente: cambiare solo ciò che chiede (forme, colori, complessità).
7. **Registra la copertina fatta**, quando l'utente la accetta: salva l'SVG a sé (se è inline nella pagina, estrailo) e lancia
   `python -m copertine registra --svg file.svg --progetto <nome-repo-github> --note "stile di partenza, palette, elemento legato al tema" --titolo "Titolo card" --desc "Descrizione breve" --tag "Tema1,Tema2" [--anno 2026] [--live <link pagina online>]`.
   Copia lo SVG in `fatte/`, aggiunge una riga a `fatte/indice.md` e (con `--titolo` e `--desc`) la voce della card in `fatte/progetti.json`. `--progetto` = nome esatto della repo su GitHub (serve al link "Codice"). Se ne fai una nuova per lo stesso progetto, registra la versione finale.
8. **Pubblica nel sito dei progetti** (`FedeGambe.github.io`, cartella `C:/Users/federico.gamberini/OneDrive - CNA SERVIZI MODENA S.R.L/Desktop/Documenti Personali/Progetti_Personali/FedeGambe.github.io`). Quando l'utente accetta la cover usata nella pagina (SVG in `docs/` della repo del progetto), è **obbligatorio**: usa quell'SVG come `--svg` e il sito come `-o`, così la copia finisce anche in `img/` del sito. Comando unico, al posto dei passi 7 e 8 a mano:
   `python -m copertine pubblica --svg file.svg --progetto <nome-repo-github> --titolo "…" --desc "…" --tag "A,B" --note "…" [--anno 2026] [--live /nome-repo/] -o <cartella-del-sito>`
   Registra la cover, copia le cover in `img/`, riscrive `progetti.json` (che `index.html` legge per le card) e fa commit nelle due repo (`copertine` e sito). Il push solo con `--push`: chiedere prima all'utente. In Git Bash un `--live /nome/` viene riscritto come percorso Windows: usare `MSYS_NO_PATHCONV=1` davanti al comando. Le cover devono reggere il taglio 5:7 delle card (`object-fit: cover`, ancorata in basso).

## Regole

- Stili e galleria sono **esempi da cui prendere ispirazione**, non da usare tali e quali: per ogni progetto adattali (cambia composizione, palette, proporzioni) e aggiungi un elemento legato al tema (es. i prezzi che scendono a gradini sul tramonto). **Non creare file `copertina.py` (né altri script generatori) nel progetto di destinazione**: genera con `python -m copertine ...` o con Python al volo (`python -c`), tieni gli script temporanei nello scratchpad, e nel progetto lascia solo l'SVG/HTML finale. Per rigenerare basta il comando, annotato in `--note` alla registrazione.
- Ispirazione, non copia: prendi palette, composizione e atmosfera; non riprodurre illustrazioni, loghi, titoli o testi del riferimento.
- Riferimenti da siti/profili: solo ciò che è visibile pubblicamente o con l'accesso che l'utente stesso ha dato; nessuna password, nessun download dei contenuti.
- Il font Archivo nel poster SVG compare solo se installato o caricato dalla pagina; altrimenti c'è un ripiego. Dirlo se rilevante.
- Niente PNG per ora (non c'è un rasterizzatore nel progetto); se serve, esportare dal browser.
- Mantieni la libreria piccola: una funzione per stile, nessuna dipendenza.
