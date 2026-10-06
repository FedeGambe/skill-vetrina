---
name: html
description: Crea una pagina HTML singola (riassunto o presentazione) di un repository GitHub, con cover a tutto schermo, indice laterale, barra di avanzamento e tema chiaro/scuro. Usare quando l'utente chiede una pagina, report, presentazione o riassunto HTML di un repo o di un progetto.
---

# html

Claude legge il repo e produce **un solo file HTML** partendo da `template.html` (stessa cartella di questa skill). Nessun build, nessuna dipendenza, nessun font esterno. Stile del sito `FedeGambe.github.io`: carta calda con grana, titoli Georgia, testo Inter/system-ui, etichette monospace maiuscole, righe nere da 3px, tema scuro di default (salvato in localStorage). Nel titolo metti 1-2 parole chiave in `<em>` (corsivo arancio).

## Flusso

1. **Leggi il repo.** README, struttura cartelle, file chiave, ultimi commit. Capisci a che serve, come si usa, com'è fatto. Non inventare: ogni affermazione viene dal repo.
2. **Scegli i capitoli** (4-8). Tipici: Sintesi (`c0`, grigio), A cosa serve, Come funziona/architettura, Uso/installazione, Esempi, Stato e limiti. `data-parte`: `""` grigio (sintesi), `"a"` colore 1, `"b"` colore 2 (es. "oggi/stato attuale"). Classe CSS `parte-a`/`parte-b` sulla `<section>`; `<h2 data-n="Capitolo 01">` mostra l'etichetta sopra il titolo.
3. **Cover.** Usa la skill `copertine` (formato `schermo`, 1600x900) e incolla l'SVG in `{{COVER_SVG}}` con `class="bauhaus"` e `preserveAspectRatio="xMidYMax slice"`. Favicon con `favicon_uri` (vedi commento nel template).
   **Colori dalla cover:** nel `:root` del template `--c2` = colore caldo della cover (a metà del gradiente della forma principale, lo stesso del corsivo `<em>` nel titolo), `--c1` = colore freddo/secondario (linee, griglia), versione chiara scurita per il contrasto e versione scura più luminosa. `--g1/--g2/--g3/--bg/--surface` del tema scuro = fondo della cover appena schiarito. Imposta anche `--cover` (colore di fondo dell'SVG) e `--c2-cover` (colore del corsivo nel titolo, sulla cover scura) in cima al `:root`.
   **Logo (già nel template, non toccare):** pulsante "← Progetti" nella barra, logo bianco in basso a destra sulla cover (`.logo-cover`) e firma "Federico Gamberini" in fondo al footer; tutti puntano a https://progetti.federicogamberini.it/.
4. **Compila il template.** Sostituisci ogni `{{SEGNAPOSTO}}`: `LINGUA`, `TITOLO` (testo semplice), `TITOLO_HTML` (stesso titolo con le parole chiave in `<em>`), `DESCRIZIONE`, `SOTTOTITOLO`, `TAG` (2-4 `<span>` con temi/tecnologie del repo, es. Scraping, Machine Learning: pillole in cover sotto il sottotitolo), `COVER_SVG`, `INDICE_VOCI`, `CAPITOLI`, `FOOTER`. Rimuovi i commenti di istruzione. Id capitoli `c0`, `c1`... uguali ai link dell'indice; `data-titolo` uguale al testo del link.
5. **Contenuti.** Elementi pronti nel CSS: `.tabella > table`, `figure` (cornice scura, per immagini/grafici), `.conclusione` (riquadro di sintesi), `code`, liste. Diagrammi: SVG inline. Niente librerie se non servono.
6. **Controlla nel browser** (skill `browser-automation` con screenshot, o Chrome): cover a schermo intero, titolo leggibile, indice e barra che seguono lo scroll, tema scuro, larghezza mobile. Nessun segnaposto `{{` rimasto: `grep "{{" file.html`.
7. **Salva** come `<nome-repo>.html` dove chiede l'utente (default: cartella corrente).

## Regole

- Lingua della pagina = lingua dell'utente, salvo diversa richiesta.
- Il file deve funzionare aperto da disco (`file://`): immagini del repo come data URI o percorsi relativi esistenti.
- Non cambiare JS e struttura della barra/indice: dipendono da ids (`barra`, `copertina`, `indice`, `apri-indice`, `tema`, `barra-capitolo`) e classi (`capitolo`, `data-titolo`, `data-parte`).
- Se serve un componente nuovo, aggiungilo al CSS del file in stile coerente (variabili `--*`, niente colori fissi).
- Esempio completo di riferimento: `when-to-buy-iphone/analisi/analisi.html`.
