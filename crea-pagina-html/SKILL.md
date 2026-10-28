---
name: crea-pagina-html
description: Crea una pagina HTML singola (riassunto o presentazione) di un repository GitHub, con intro tipografica (titolo su una riga da bordo a bordo, senza immagine), indice laterale, barra di avanzamento e tema chiaro/scuro. Usare quando l'utente chiede una pagina, report, presentazione o riassunto HTML di un repo o di un progetto.
---

# html

Claude legge il repo e produce **un solo file HTML** partendo da `template.html` (stessa cartella di questa skill). Nessun build, nessuna dipendenza, nessun font esterno. Stile del sito `FedeGambe.github.io`: carta calda con grana, titoli Georgia, testo Inter/system-ui, etichette monospace maiuscole, righe nere da 3px, tema scuro di default (salvato in localStorage). Nel titolo metti 1-2 parole chiave in `<em>` (corsivo arancio).

## L'intro

Niente immagine in testa e niente ombre: l'intro è solo tipografia, sul fondo della pagina. Blocco CSS `INTRO` + funzione `adattaTitolo()` nel JS del template (non toccarli):

- **occhiello** (`{{OCCHIELLO}}`): 2-3 voci separate da ` · ` (tipo di progetto · tecnologia principale · anno), in monospace maiuscolo con un trattino `--c2` davanti;
- **titolo** su una riga, da bordo a bordo: il JS scala il font sulla larghezza della colonna (max 220px). Se scenderebbe sotto i 44px (telefono, titoli lunghi) torna a capo con il font normale. Titolo breve: 2-5 parole;
- **sottotitolo** (1-2 frasi, a tutta larghezza come il titolo) e **tag**, poi una riga da 3px che chiude l'intro.

La cover del progetto (`docs/img/cover_*.svg`) non va più nella pagina: resta per la card del sito, i social e la favicon.

## Aggiornare una pagina fatta con la vecchia cover

`nuova_intro.py` (stessa cartella) porta una pagina con la cover a tutto schermo all'intro tipografica: `python nuova_intro.py <progetto>/docs/index.html "Tipo · Tecnologia · Anno"`. Toglie la cover e le ombre, tiene titolo, sottotitolo e tag. Le diciture della copertina (es. frontespizio della tesi) diventano una riga di dati sotto i tag. Se la pagina chiama il colore caldo `--arancio` lo usa come `--c2`, e se scorre a scatti mette l'intro come primo punto d'aggancio. Se la conversione fallisce il file non viene toccato. Dopo, controlla la pagina nel browser (punto 6 del flusso).

## Flusso

1. **Leggi il repo.** README, struttura cartelle, file chiave, ultimi commit. Capisci a che serve, come si usa, com'è fatto. Non inventare: ogni affermazione viene dal repo.
2. **Scegli i capitoli** (4-8). Tipici: Sintesi (`c0`, grigio), A cosa serve, Come funziona/architettura, Uso/installazione, Esempi, Stato e limiti. `data-parte`: `""` grigio (sintesi), `"a"` colore 1, `"b"` colore 2 (es. "oggi/stato attuale"). Classe CSS `parte-a`/`parte-b` sulla `<section>`; `<h2 data-n="Capitolo 01">` mostra l'etichetta sopra il titolo.
3. **Cover e scheda.** Richiama la skill `crea-scheda-progetto` (verifica/crea `docs/progetto.json`). Controlla in `docs/img/` la cover (`cover_orizzontale.svg`, per la scheda) e `favicon.svg`; se mancano, creale con la skill `crea-copertina`. La favicon va come data URI in `{{FAVICON}}` (vedi commento nel template).
   **Colori dalla cover:** nel `:root` `--c2` = colore caldo del soggetto (lo stesso del corsivo `<em>`), `--c1` = colore freddo/secondario, versione chiara scurita per il contrasto e versione scura più luminosa. `--g1/--g2/--g3/--bg/--surface` del tema scuro = fondo della cover appena schiarito. `--cover` = fondo della cover (usato dai riquadri scuri e dai pulsanti attivi).
   **Logo (già nel template, non toccare):** pulsante "← Progetti" nella barra, firma "Federico Gamberini" nel footer; tutti puntano a https://progetti.federicogamberini.it/.
4. **Compila il template.** Sostituisci ogni `{{SEGNAPOSTO}}`: `LINGUA`, `TITOLO` (testo semplice), `TITOLO_HTML` (stesso titolo con le parole chiave in `<em>`), `OCCHIELLO` (vedi L'intro), `DESCRIZIONE`, `SOTTOTITOLO` (1-2 frasi), `TAG` (2-4 `<span>` con temi/tecnologie), `FAVICON`, `INDICE_VOCI`, `CAPITOLI`, `FOOTER`. Rimuovi i commenti di istruzione. Id capitoli `c0`, `c1`... uguali ai link dell'indice; `data-titolo` uguale al testo del link.
5. **Contenuti.** Elementi pronti nel CSS: `.kpi > div > b + span` (numeri chiave nella Sintesi), `.tabella > table` (con `th[data-k]` ordinabili, `.badge`, `.pager`), `.conclusione` (riquadro di sintesi), `.barra-filtri` (filtri globali sticky sotto la barra, gruppi di pillole `.gruppo button.on` + `input[type=search]`), `figure` + `.leg` (legenda), `code`, liste. Esempio completo: `esempio.html` (stessa cartella): copia da lì struttura e JS dei filtri.
   **Grafici (stile dell'esempio):**
   - Plotly 2.35.2 da CDN (`<script src="https://cdn.jsdelivr.net/npm/plotly.js-dist-min@2.35.2/plotly.min.js">`) per grafici interattivi; è l'unica dipendenza esterna ammessa. Per grafici semplici e statici vale ancora l'SVG inline.
   - Dati in `<script id="dati" type="application/json">` (un solo JSON), letti con `JSON.parse`; ogni grafico in `<figure><div id="g-..." class="plot"></div></figure>` (430px, 360px su mobile). `figure` è un riquadro "vetro" scuro in entrambi i temi, quindi tutti i testi dei grafici sono chiari.
   - Layout base unico per tutti: sfondo trasparente, font monospace 11px colore `#d9ccaf`, griglia `rgba(255,255,255,.1)`, niente `zeroline`, legenda orizzontale sotto (`y:-.18`), modebar orizzontale trasparente senza select/lasso/zoom +/- /autoscale, `displaylogo:false`, `responsive:true`, `Plotly.react` a ogni cambio filtro. Hover: `"x unified"` per serie temporali, `"closest"` per scatter; hoverlabel scuro (`#0a1018`, bordo chiaro).
   - Colori: palette della cover (primo = caldo `--c2`, secondo = freddo `--c1`), poi pastello distinguibili (`#9db4f0 #c9a8e8 #a6d96a #f4a6c0 #d9d9d9`). Linee 2.2-2.6px, marker 6-8px, nuvole di punti con `opacity:.5`. Unità sugli assi (`ticksuffix`), formato italiano (virgola decimale).
   - Dopo il grafico una riga che spiega come leggerlo e come interagire. Con nessun dato: annotazione "Nessun dato con questi filtri".
6. **Controlla nel browser** (Playwright o Chrome, poi Read sugli screenshot), **a 1280px e a 390px**:
   - desktop: titolo su una riga da bordo a bordo, intro chiusa dalla riga da 3px;
   - telefono: titolo a capo leggibile (non sotto i 44px), la pagina non scorre di lato (`document.documentElement.scrollWidth` = larghezza; occhio a link lunghi e tabelle);
   - indice e barra che seguono lo scroll, tema chiaro e scuro, console senza errori, nessun `{{` rimasto (`grep "{{" file.html`).
7. **Salva** in `docs/index.html` del progetto (crea `docs/` se manca), pubblicabile con GitHub Pages (Settings → Pages → branch `main`, cartella `/docs`). Se l'utente indica un altro percorso, usa quello. **Subito dopo** richiama `crea-scheda-progetto` per scrivere in `docs/progetto.json` il campo `live` (`/<repo>/`).

## Telefono: gerarchia dei font

h1 ≈ 42px > h2 27 > h3 21 > testo 16 > note 13 (il template la rispetta già). Non introdurre testi più grandi dei titoli né titoli piccoli quanto il testo.

## Regole

- Lingua della pagina = lingua dell'utente, salvo diversa richiesta.
- Il file deve funzionare sia da disco (`file://`) sia su GitHub Pages: immagini con percorsi **relativi** dentro `docs/` (`img/...`, mai `/percorso` assoluto né `C:/...`), niente font esterni; unica CDN ammessa Plotly.
- Non cambiare JS e struttura della barra/indice: dipendono da ids (`barra`, `copertina`, `indice`, `apri-indice`, `tema`, `barra-capitolo`) e classi (`capitolo`, `data-titolo`, `data-parte`).
- Non toccare il blocco CSS `INTRO` e `adattaTitolo()`: sono uguali in tutte le pagine dei progetti. Se serve un componente nuovo, aggiungilo al CSS del file in stile coerente (variabili `--*`, niente colori fissi).
- Esempio completo di riferimento: `esempio.html` (Target Maturity ETF Planner).
