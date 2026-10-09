---
name: crea-dashboard-html
description: Crea una dashboard interattiva in un solo file HTML (controlli a sinistra, risultati e grafico di dettaglio a destra, barra mobile, tema chiaro/scuro) per un modello, un'analisi o dei dati. Usare quando l'utente chiede una dashboard, un simulatore o una pagina interattiva e non una pagina di presentazione (per quella c'è la skill `crea-pagina-html`).
---

# dashboard

Un solo file HTML, nessun build, nessuna dipendenza, nessun font esterno. Stessa identità della skill `crea-pagina-html` (carta calda con grana, Georgia, Inter/system-ui, monospace per i numeri, righe nere da 3px, tema scuro di default). Struttura da `template.html`; esempio completo e funzionante in `esempio.html` (predizione BEV: form di 14 campi, indicatore ad arco, cascata dei contributi).

## Struttura (non cambiarla)

1. **Barra fissa**: "← Progetti" (logo, già nel template), 0-2 link, pulsante Tema.
2. **Banner** (come nei simulatori): fondo `docs/img/banner_sfondo.svg` + soggetto `banner_soggetto.svg` (i due livelli della cover del progetto: copia `cover_sfondo.svg` e `cover_soggetto.svg`, oppure scomponi un banner 1200x400 con `crea-copertina/livelli.py banner.svg <indici>`). Dentro: `h1` con 1-2 parole chiave in `<em>` e un sottotitolo breve in maiuscoletto. `{{BANNER_FONDO}}` = colore di fondo dello sfondo, `{{BANNER_TESTO}}`/`{{BANNER_EM}}` = colori leggibili sopra. Su desktop il soggetto sta a destra; se è una striscia a tutta larghezza (classe `largo`, es. la tesi) si ruota di 90° con la base a destra (`banner_soggetto_ruotato.svg`, in un `<picture>` con `<source media="(min-width: 701px)">`) e occupa tutta l'altezza del banner, largo metà schermo (ritagliato sopra e sotto), allineato al bordo destro. Su telefono va sotto il titolo, con il sottotitolo sopra la sua parte bassa su una sfumatura. La barra è trasparente sopra il banner e piena quando si scorre.
2b. **Testata**: `.intro` di 1-2 frasi, pillole `.dati-modello` (metriche o provenienza dei dati).
3. **Barra azioni** (facoltativa): preset `.pulsante[data-esempio]`, Ripristina, Copia link.
4. **Griglia 2 colonne**: a sinistra `<form>` con una `.scheda.sezione` per gruppo (legend con `.passo` numerato); a destra `<aside class="esiti">` sticky su desktop: scheda KPI (`#risultato`) + scheda dettaglio/grafico + `details.metodo` ("Come leggere il grafico").
5. **Barra mobile** `.barra-mobile` col KPI, visibile quando `#risultato` esce dallo schermo.
6. **Footer** con nota di cautela (cosa il numero NON dice) e firma.

Componenti già nel CSS dell'esempio: segmenti (radio), select, contatore ±, numero con unità, cursore (range), arco/indicatore SVG, verdetto, cascata a barre, legenda. Se ne serve uno nuovo, aggiungilo con le variabili `--*` (teal = verso positivo/principale, arancio = negativo/accento), mai colori fissi.

## Flusso

1. **Capisci i dati.** Cosa si controlla (input), cosa si calcola (output), con quale logica. Non inventare numeri: tutto viene dai dati o dal modello dell'utente. Se il modello è un file (joblib, JSON, CSV), esportalo in JSON inline nello `<script>`; il calcolo avviene nel browser.
2. **Scegli i componenti.** Un controllo per tipo di campo (radio per poche scelte, select per liste, contatore per interi piccoli, numero+unità per misure, range per scale). Gruppi da 3-5 campi. Un KPI principale + un grafico di dettaglio che spieghi il perché.
3. **Favicon.** Richiama prima `crea-scheda-progetto` (verifica/crea `docs/progetto.json`). Cerca `docs/img/favicon.svg` (quadrato con angoli arrotondati) e mettila come data URI al posto di `<!--__FAVICON__-->`. Se manca, creala con la skill `crea-copertina` e salvala in `docs/img/`.
4. **Compila `template.html`.** Sostituisci i `{{SEGNAPOSTO}}`; togli le parti facoltative non usate e i commenti. Scrivi la logica nel secondo `<script>` seguendo i 5 punti del commento (vedi `esempio.html`): leggi/imposta/valida, `aggiorna()`, stato nel link `#campo=valore`, eventi. Il blocco `/*__LOGICA__*/` serve solo se la logica sta in un file a parte: altrimenti eliminalo.
5. **Accessibilità e robustezza** (non negoziabili): `label`/`legend` su ogni controllo, target ≥ 44px, `:focus-visible`, errori accanto al campo (`aria-invalid`, `role="alert"`), `aria-live` sul KPI, input non valido = l'ultimo risultato valido resta (classe `.inattivo`), `prefers-reduced-motion`, numeri con `Intl.NumberFormat("it-IT")`.
6. **Controlla nel browser** (skill `browser-automation` o Chrome): console senza errori, ogni controllo cambia il risultato, valori fuori range bloccano, link condiviso ricarica lo stesso stato, tema chiaro e scuro, larghezza mobile con barra fissa. `grep "{{" file.html` deve essere vuoto.
7. **Salva** in `docs/` del progetto (crea la cartella se manca): `docs/dashboard.html` (o `docs/index.html` se la dashboard è l'unica pagina), pubblicabile con GitHub Pages (Settings → Pages → branch `main`, cartella `/docs`). Dati e modello restano inline nel file; link verso altre pagine solo relativi (`index.html`). Se l'utente indica un altro percorso, usa quello. **Subito dopo** richiama `crea-scheda-progetto` per scrivere `live` in `docs/progetto.json` (`/<repo>/`, oppure `/<repo>/dashboard.html` se non è `index.html`).

## Telefono (fino a 700px)

Il blocco `FONT MOBILE` del template fissa la gerarchia: h1 ≈ 33px > titoli di sezione (h2, `legend` dei gruppi) 20 > testo 16 > etichette 14,4 > note 12,8. Non scendere sotto questi valori con regole più specifiche.

## Regole

- Lingua della pagina = lingua dell'utente.
- Deve funzionare da `file://` e su GitHub Pages (`https://<utente>.github.io/<repo>/`), quindi percorsi relativi, niente `/assoluti`, niente CDN: `history.replaceState` e clipboard in `try`/con fallback.
- Nessun dato lascia il browser: dillo nel footer.
- Footer onesto: modello moderato o dati limitati = scrivilo (es. ROC-AUC), e che gli effetti descrivono il modello, non causalità.
