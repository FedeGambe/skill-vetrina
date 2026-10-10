---
name: crea-dashboard-html
description: Crea una dashboard interattiva in un solo file HTML con banner a due livelli in testa (come i simulatori), controlli a sinistra, risultati e grafico di dettaglio a destra, barra mobile e tema chiaro/scuro, per un modello, un'analisi o dei dati. Usare quando l'utente chiede una dashboard, un simulatore o una pagina interattiva e non una pagina di presentazione (per quella c'è la skill `crea-pagina-html`).
---

# dashboard

Un solo file HTML, nessun build, nessuna dipendenza, nessun font esterno. Stessa identità della skill `crea-pagina-html` (carta calda con grana, Georgia, Inter/system-ui, monospace per i numeri, righe nere da 3px, tema scuro di default). Struttura da `template.html`; esempio completo e funzionante in `esempio.html` (la dashboard della tesi, predizione BEV: banner a due livelli con soggetto a striscia ruotato, form di 14 campi, indicatore ad arco, cascata dei contributi; i file del banner sono in `img/` accanto). Riferimenti già online con la stessa struttura: le dashboard dei simulatori (busta paga, conto deposito), Vehicle Price Monitor e la dashboard della tesi.

## Struttura (non cambiarla)

1. **Barra fissa**: "← Progetti" (logo, già nel template), 0-2 link, pulsante Tema. È **trasparente sopra il banner**, con i pulsanti nel colore del titolo, e diventa piena quando si scorre (classe `compatta`, script già nel template).
2. **Banner a due livelli** (`<section class="banner">`): fondo `docs/img/banner_sfondo.svg` (nel CSS) + soggetto `<img class="soggetto" src="img/banner_soggetto.svg">`. Dentro `.dentro`: `h1` con 1-2 parole chiave in `<em>` e un sottotitolo breve (`<p>`, maiuscoletto).
3. **Testata** (`.pagina > header`): `.intro` di 1-2 frasi, pillole `.dati-modello` (metriche o provenienza dei dati).
4. **Barra azioni** (facoltativa): preset `.pulsante[data-esempio]`, Ripristina, Copia link.
5. **Griglia 2 colonne**: a sinistra `<form>` con una `.scheda.sezione` per gruppo (legend con `.passo` numerato); a destra `<aside class="esiti">` sticky su desktop: scheda KPI (`#risultato`) + scheda dettaglio/grafico + `details.metodo` ("Come leggere il grafico").
6. **Barra mobile** `.barra-mobile` col KPI, visibile quando `#risultato` esce dallo schermo.
7. **Footer** con nota di cautela (cosa il numero NON dice) e firma.

Componenti già nel CSS dell'esempio: segmenti (radio), select, contatore ±, numero con unità, cursore (range), arco/indicatore SVG, verdetto, cascata a barre, legenda. Se ne serve uno nuovo, aggiungilo con le variabili `--*` (teal = verso positivo/principale, arancio = negativo/accento), mai colori fissi.

## Il banner

I file vengono dalla skill `crea-copertina` (passo 6), in `docs/img/`:

- `banner_sfondo.svg` e `banner_soggetto.svg`: di solito copia di `cover_sfondo.svg` e `cover_soggetto.svg` del progetto; per un banner disegnato apposta (1200x400) si scompone con `livelli.py banner.svg <indici>`.
- Se il soggetto è una **striscia a tutta larghezza** (es. le bande della tesi): classe `largo` sull'img e, per il desktop, `banner_soggetto_ruotato.svg` (ruotato di 90°, base a destra) in un `<picture>`:
  `<picture><source media="(min-width: 701px)" srcset="img/banner_soggetto_ruotato.svg"><img class="soggetto largo" src="img/banner_soggetto.svg" alt=""></picture>`

Segnaposto del template: `{{BANNER_FONDO}}` = colore di fondo di `banner_sfondo.svg` (serve alla sfumatura su telefono), `{{BANNER_TESTO}}` = colore del titolo e dei pulsanti della barra sopra il banner, `{{BANNER_EM}}` = colore del corsivo del titolo; tutti leggibili sul fondo. `{{SOTTOTITOLO}}` = la riga sotto il titolo.

Il blocco CSS `BANNER A DUE LIVELLI` (non toccarlo) lo dispone:

- **Desktop**: titolo e sottotitolo a sinistra, soggetto a destra dentro il banner. Striscia: ruotata, a tutta altezza del banner, larga metà schermo (ritagliata sopra e sotto), allineata al bordo destro.
- **Telefono (fino a 700px)**: solo il titolo prima della grafica; poi il soggetto, con il sottotitolo sopra la sua parte bassa su una sfumatura del fondo. La striscia resta orizzontale.

## Flusso

1. **Capisci i dati.** Cosa si controlla (input), cosa si calcola (output), con quale logica. Non inventare numeri: tutto viene dai dati o dal modello dell'utente. Se il modello è un file (joblib, JSON, CSV), esportalo in JSON inline nello `<script>`; il calcolo avviene nel browser.
2. **Scegli i componenti.** Un controllo per tipo di campo (radio per poche scelte, select per liste, contatore per interi piccoli, numero+unità per misure, range per scale). Gruppi da 3-5 campi. Un KPI principale + un grafico di dettaglio che spieghi il perché.
3. **Scheda, favicon e banner.** Richiama `crea-scheda-progetto` (verifica/crea `docs/progetto.json`). Cerca in `docs/img/` `favicon.svg` (va come data URI in `{{FAVICON}}`), `banner_sfondo.svg` e `banner_soggetto.svg`. Se mancano: se il progetto ha già `cover_sfondo.svg`/`cover_soggetto.svg` copiali; altrimenti creali con la skill `crea-copertina`.
4. **Compila `template.html`.** Sostituisci i `{{SEGNAPOSTO}}` (compresi `BANNER_*` e `SOTTOTITOLO`); togli le parti facoltative non usate e i commenti. Scrivi la logica nel secondo `<script>` seguendo i 5 punti del commento (vedi `esempio.html`): leggi/imposta/valida, `aggiorna()`, stato nel link `#campo=valore`, eventi. Il blocco `/*__LOGICA__*/` serve solo se la logica sta in un file a parte: altrimenti eliminalo.
5. **Accessibilità e robustezza** (non negoziabili): `label`/`legend` su ogni controllo, target ≥ 44px, `:focus-visible`, errori accanto al campo (`aria-invalid`, `role="alert"`), `aria-live` sul KPI, input non valido = l'ultimo risultato valido resta (classe `.inattivo`), `prefers-reduced-motion`, numeri con `Intl.NumberFormat("it-IT")`.
6. **Controlla nel browser** (Playwright o Chrome, poi Read sugli screenshot), **a 1280px e a 390px**: banner (soggetto intero dentro il banner su desktop, sotto il titolo su telefono), barra trasparente sopra il banner e piena scorrendo, pulsanti della barra leggibili sul banner, console senza errori, ogni controllo cambia il risultato, valori fuori range bloccano, link condiviso ricarica lo stesso stato, tema chiaro e scuro, barra mobile, nessuno scorrimento laterale. `grep "{{" file.html` deve essere vuoto.
7. **Salva** in `docs/` del progetto (crea la cartella se manca): `docs/dashboard.html` (o `docs/index.html` se la dashboard è l'unica pagina), pubblicabile con GitHub Pages (Settings → Pages → branch `main`, cartella `/docs`). Dati e modello restano inline nel file; link verso altre pagine solo relativi (`index.html`). **Subito dopo** richiama `crea-scheda-progetto` per scrivere `live` in `docs/progetto.json` (`/<repo>/`, oppure `/<repo>/dashboard.html` se non è `index.html`).

## Telefono: gerarchia dei font

Il blocco `FONT MOBILE` del template la fissa: h1 ≈ 33px > titoli di sezione (h2, `legend` dei gruppi) 20 > testo 16 > etichette 14,4 > note 12,8. Non scendere sotto questi valori con regole più specifiche.

## Regole

- Lingua della pagina = lingua dell'utente.
- Deve funzionare da `file://` e su GitHub Pages, quindi percorsi relativi (`img/...`), niente `/assoluti`, niente CDN: `history.replaceState` e clipboard in `try`/con fallback.
- Le variabili `--banner-*` stanno su `:root` (non su `.banner`): la barra, che sta fuori dal banner, le usa per i pulsanti.
- Nessun dato lascia il browser: dillo nel footer.
- Footer onesto: modello moderato o dati limitati = scrivilo (es. ROC-AUC), e che gli effetti descrivono il modello, non causalità.
