---
name: crea-copertina
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
3. **Genera.** Salva sempre nella cartella `docs/img/` del progetto (la crea se manca): `docs/img/cover_orizzontale.svg`, `docs/img/cover_verticale.svg` e `docs/img/favicon.svg` (questi nomi esatti), che la skill `crea-pagina-html` e `pubblica` cercano lì. Percorsi relativi, pronti per GitHub Pages.
   ```
   python -m copertine <stile> -p <palette> -f banner|poster|favicon -t "Titolo" -s "Sottotitolo" [--parola X] [--seed N] -o file.svg
   ```
   In Python: `from copertine import genera, favicon_uri`.
4. **Guarda il risultato.** Apri l'SVG o la pagina con una skill/strumento da browser (es. `browser-automation` con `--screenshot`, poi Read sul PNG) o con Chrome. Con `file://` su Windows usa percorsi `C:/...` con `%20` per gli spazi. Un grafico non è finito finché non l'hai visto.
5. **Integra.** Se la pagina ha titolo e testo di apertura, fai una **cover a grandezza schermo** (non un banner sotto il testo): sezione alta esattamente `100svh`, SVG assoluto a tutto schermo (`inset:0`, `preserveAspectRatio="xMidYMax slice"`, formato `schermo` 1600x900 con la grafica nel 62% inferiore), titolo e sottotitolo HTML a tutta larghezza in alto nei colori della palette (z-index sopra l'SVG), diciture in basso. Banner: SVG inline nella pagina (`preserveAspectRatio="xMidYMid slice"` con altezza fissata via CSS). Favicon: `<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,...">` con il contenuto di `docs/img/favicon.svg` (URL-encoded, come fa `favicon_uri`), così il file resta autonomo. Allinea i colori della pagina alla palette (variabili CSS, tema scuro compreso). **Inserisci entrambe le versioni della cover** (orizzontale `bauhaus-o`, verticale `bauhaus-v` con id prefissati `v-`): il CSS del template `crea-pagina-html` mostra la verticale quando lo schermo è in portrait.
6. **Itera** sui commenti dell'utente: cambiare solo ciò che chiede (forme, colori, complessità).
7. **Registra la copertina fatta**, quando l'utente la accetta: salva l'SVG a sé (se è inline nella pagina, estrailo) e lancia
   `python -m copertine registra --svg file.svg --progetto <nome-repo-github> --note "stile di partenza, palette, elemento legato al tema" --titolo "Titolo card" --desc "Descrizione breve" --tag "Tema1,Tema2" [--anno 2026] [--live <link pagina online>]`.
   Copia lo SVG in `fatte/`, aggiunge una riga a `fatte/indice.md` e (con `--titolo` e `--desc`) la voce della card in `fatte/progetti.json`. `--progetto` = nome esatto della repo su GitHub (serve al link "Codice"). Se ne fai una nuova per lo stesso progetto, registra la versione finale.
7b. **Tre file per ogni cover, generati insieme al passo 3**: orizzontale, verticale e **favicon**. La favicon (`docs/img/favicon.svg`) è un **quadrato 64x64 con angoli arrotondati** (`rx` ≈ 14, contenuto ritagliato con `clipPath`; il formato `favicon` della libreria lo fa già). Può essere ricomposta e semplificata (la cover intera non si legge a 16px), ma deve riprendere gli elementi che riconducono alla cover: palette, forma principale, elemento legato al tema, eventuale lettera/parola. Guardala anche rimpicciolita (32 e 16px). Per la verticale: orizzontale (`schermo`, `docs/img/cover_orizzontale.svg`) e verticale (`poster`, `docs/img/cover_verticale.svg`). Stessa palette, stile, seed ed elemento legato al tema; la verticale è 1080x1350 (4:5), senza titolo (lo scrive la pagina/card in HTML), grafica ancorata in basso e composta per reggere il taglio 5:7. Vanno guardate tutte e tre (passo 4) e committate nel progetto. L'orizzontale serve anche alla card del sito su telefono (card 4:3 e titolo sul fondo pieno, quindi la grafica va nella parte bassa) e alla cover delle pagine su telefono. La verticale serve alla card (`pubblica` la copia nel sito) e alla pagina HTML su schermi in verticale (`orientation:portrait`, vedi skill `crea-pagina-html`).
8. **Pubblica nel sito dei progetti** (`FedeGambe.github.io`, accanto a `Elaborati_Repo`). Quando l'utente accetta la cover, **è obbligatorio**, al posto dei passi 7 e 8 a mano:
   `python -m copertine pubblica --progetto <nome-repo-github> [--note "stile di partenza, palette, elemento legato al tema"] [--push]`
   L'SVG per la card è `~/<repo>/docs/img/cover_verticale.svg` (altrimenti `--svg`), il sito è la cartella accanto a `Elaborati_Repo`, la card (titolo, descrizione, tag, anno, link live) è presa da `progetti.json`. Solo per un **progetto nuovo** servono anche `--titolo "…" --desc "…" --tag "A,B" [--live /nome-repo/]`. Registra in `fatte/`, copia in `img/` (e toglie le cover non più usate), riscrive `progetti.json` e committa le due repo. Il push solo con `--push`: chiedere prima all'utente. In Git Bash un `--live /nome/` viene riscritto come percorso Windows: usare `MSYS_NO_PATHCONV=1`. Le cover devono reggere il taglio 5:7 delle card (`object-fit: cover`, ancorata in basso). La repo del progetto va committata e pushata dall'utente (`docs/` deve già avere la cover).

8b. **Due livelli per il telefono.** Dalla cover orizzontale ricava `docs/img/cover_sfondo.svg` (solo il fondo: colore, sfumatura, grafica leggera di fondo, grana; niente bordi netti a metà altezza, perché su telefono ci va sopra il titolo) e `docs/img/cover_soggetto.svg` (solo il soggetto su fondo trasparente, viewBox stretto attorno al disegno). Metodo: `python livelli.py docs/img/cover_orizzontale.svg <indici dei figli della radice che sono il soggetto>` (dalla radice del repo skill-vetrina, `crea-copertina/livelli.py`), poi `node livelli_bbox.js docs/img/cover_soggetto.svg` (serve Playwright). Per disegnare cover nuove conviene comporle già a livelli: un gruppo per il fondo, uno per il soggetto e la grana per ultima. Guarda i due file anche separati.

9. **Scheda progetto.** Appena le tre immagini sono in `docs/img/`, richiama la skill `crea-scheda-progetto`: verifica che `docs/progetto.json` esista (altrimenti lo crea) e che `img` punti a `img/cover_verticale.svg`.

## Regole

- Stili e galleria sono **esempi da cui prendere ispirazione**, non da usare tali e quali: per ogni progetto adattali (cambia composizione, palette, proporzioni) e aggiungi un elemento legato al tema (es. i prezzi che scendono a gradini sul tramonto). **Non creare file `copertina.py` (né altri script generatori) nel progetto di destinazione**: genera con `python -m copertine ...` o con Python al volo (`python -c`), tieni gli script temporanei nello scratchpad, e nel progetto lascia solo l'SVG/HTML finale. Per rigenerare basta il comando, annotato in `--note` alla registrazione.
- Ispirazione, non copia: prendi palette, composizione e atmosfera; non riprodurre illustrazioni, loghi, titoli o testi del riferimento.
- Riferimenti da siti/profili: solo ciò che è visibile pubblicamente o con l'accesso che l'utente stesso ha dato; nessuna password, nessun download dei contenuti.
- Il font Archivo nel poster SVG compare solo se installato o caricato dalla pagina; altrimenti c'è un ripiego. Dirlo se rilevante.
- Niente PNG per ora (non c'è un rasterizzatore nel progetto); se serve, esportare dal browser.
- Mantieni la libreria piccola: una funzione per stile, nessuna dipendenza.
