---
name: crea-dashboard-html
description: Crea una dashboard interattiva in un solo file HTML in stile app moderno e clean (testata solo testo, due fasi a tutta larghezza: prima i controlli, poi il form si comprime e mostra risultati e grafico; tema chiaro di default), per un modello, un'analisi o dei dati. Usare quando l'utente chiede una dashboard, un simulatore o una pagina interattiva e non una pagina di presentazione (per quella c'è la skill `crea-pagina-html`).
---

# dashboard

Un solo file HTML, nessun build, nessuna dipendenza, nessun font esterno. Stile app moderno e clean: tutto in Inter/system-ui (niente serif, cifre tabellari), fondo grigio chiarissimo, card bianche con bordo da 1px, raggio 12px e ombra appena accennata, niente grana né immagini decorative. Tema **chiaro di default**; lo scuro solo se l'utente preme Tema (scelta salvata in localStorage). Struttura da `template.html`; esempio completo e funzionante in `esempio.html` (la dashboard della tesi, predizione BEV: form di 14 campi, indicatore ad arco, cascata dei contributi). Riferimenti già online con la stessa struttura: le dashboard dei simulatori (busta paga, conto deposito), Vehicle Price Monitor e la dashboard della tesi.

## Struttura (non cambiarla)

1. **Barra fissa**: "← Progetti" (logo, già nel template), 0-2 link, pulsante Tema. Sempre piena, semitrasparente con sfocatura e riga sottile sotto.
2. **Testata** (`.pagina > header`, solo testo, niente banner né immagini): `.occhiello` (tipo di dashboard · modello o fonte, maiuscoletto grigio), `h1` grande in grassetto con 1-2 parole chiave in `<em>` (colore accento, non corsivo), `.intro` di 1-2 frasi, pillole `.dati-modello` (metriche o provenienza dei dati).
3. **Barra azioni** (facoltativa): preset `.pulsante[data-esempio]`, Ripristina, Copia link.
4. **Fase input** (`.pagina[data-fase="input"]`): `<form id="profilo">` a tutta larghezza, una `.scheda.sezione` per gruppo (legend con `.passo` numerato; campi su 3 colonne da desktop, `.largo` per una riga intera), in cima la barra dei passi `.passi` (si costruisce da sola dalle `.sezione`: fissa sotto la barra, evidenzia la sezione in vista e colora quelle già passate), in fondo `.invio` con il pulsante `.primario` "Mostra i risultati" (submit).
5. **Fase risultati** (`data-fase="risultati"`): il form sparisce e al suo posto c'è `.riepilogo` (una pillola `<li>Nome <b>valore</b></li>` per campo + pulsante Modifica che riapre il form); sotto, `.esiti` a tutta larghezza: scheda KPI (`#risultato`, protagonista: fondo sfumato teal o arancio secondo l'esito con le classi `.bev`/`.altro`, arco grande che parte da zero, numero che conta fino al valore) e scheda dettaglio/grafico (barre arrotondate con sfumatura, riga sotto il mouse in evidenza e le altre spente, barre che crescono una dopo l'altra con `--i` e `.entra`) affiancate su desktop (1 : 1,5), una sotto l'altra su telefono, con `details.metodo` ("Come leggere il grafico"). I preset `[data-esempio]` e un link condiviso con lo stato (`#campo=valore`) aprono direttamente i risultati; Ripristina torna al form.
6. **Footer** con nota di cautela (cosa il numero NON dice) e firma.

Componenti già nel CSS dell'esempio: segmenti (radio, la scelta attiva è piena col colore del testo), select, contatore ±, numero con unità, cursore (range), arco/indicatore SVG, verdetto, cascata a barre, legenda. Se ne serve uno nuovo, aggiungilo con le variabili `--*` (teal = verso positivo/principale, arancio = negativo/accento), mai colori fissi, bordi da 1px, ombra solo `var(--ombra)` sulle card.

## Flusso

1. **Capisci i dati.** Cosa si controlla (input), cosa si calcola (output), con quale logica. Non inventare numeri: tutto viene dai dati o dal modello dell'utente. Se il modello è un file (joblib, JSON, CSV), esportalo in JSON inline nello `<script>`; il calcolo avviene nel browser.
2. **Scegli i componenti.** Un controllo per tipo di campo (radio per poche scelte, select per liste, contatore per interi piccoli, numero+unità per misure, range per scale). Gruppi da 3-5 campi. Un KPI principale + un grafico di dettaglio che spieghi il perché.
3. **Scheda e favicon.** Richiama `crea-scheda-progetto` (verifica/crea `docs/progetto.json`). Cerca `docs/img/favicon.svg` (va come data URI in `{{FAVICON}}`); se manca, creala con la skill `crea-copertina`.
4. **Compila `template.html`.** Sostituisci i `{{SEGNAPOSTO}}` (compreso `OCCHIELLO`); togli le parti facoltative non usate e i commenti. Scrivi la logica nel secondo `<script>` seguendo i punti del commento (vedi `esempio.html`): leggi/imposta/valida, `aggiorna()` (disegna solo in fase risultati), `mostraRisultati()` (valida tutto, riempie il riepilogo, cambia fase), stato nel link `#campo=valore`, eventi. `mostraFase()` e il pulsante Modifica sono già nel template. Il blocco `/*__LOGICA__*/` serve solo se la logica sta in un file a parte: altrimenti eliminalo.
5. **Accessibilità e robustezza** (non negoziabili): `label`/`legend` su ogni controllo, target ≥ 44px, `:focus-visible`, errori accanto al campo (`aria-invalid`, `role="alert"`), `aria-live` sul KPI, tasto Invio sul form = Mostra i risultati, input non valido = l'ultimo risultato valido resta (classe `.inattivo`), `prefers-reduced-motion`, numeri con `Intl.NumberFormat("it-IT")`.
6. **Controlla nel browser** (Playwright o Chrome, poi Read sugli screenshot), **a 1280px e a 390px**: testata ariosa e leggibile, console senza errori, Mostra i risultati comprime il form e porta ai risultati, Modifica lo riapre, ogni controllo cambia il risultato, valori fuori range bloccano il passaggio (fuoco sul campo errato), link condiviso apre gli stessi risultati, apertura in tema chiaro, poi tema scuro col pulsante, nessuno scorrimento laterale. `grep "{{" file.html` deve essere vuoto.
7. **Salva** in `docs/` del progetto (crea la cartella se manca): `docs/dashboard.html` (o `docs/index.html` se la dashboard è l'unica pagina), pubblicabile con GitHub Pages (Settings → Pages → branch `main`, cartella `/docs`). Dati e modello restano inline nel file; link verso altre pagine solo relativi (`index.html`). **Subito dopo** richiama `crea-scheda-progetto` per scrivere `live` in `docs/progetto.json` (`/<repo>/`, oppure `/<repo>/dashboard.html` se non è `index.html`).

## Telefono: gerarchia dei font

Il blocco `FONT MOBILE` del template la fissa: h1 ≈ 37px > titoli di sezione (h2, `legend` dei gruppi) 17,6 > testo 16 > etichette 14,4 > note 12,8. Non scendere sotto questi valori con regole più specifiche.

## Regole

- Lingua della pagina = lingua dell'utente.
- Deve funzionare da `file://` e su GitHub Pages, quindi percorsi relativi, niente `/assoluti`, niente CDN: `history.replaceState` e clipboard in `try`/con fallback.
- Nessun dato lascia il browser: dillo nel footer.
- Footer onesto: modello moderato o dati limitati = scrivilo (es. ROC-AUC), e che gli effetti descrivono il modello, non causalità.
