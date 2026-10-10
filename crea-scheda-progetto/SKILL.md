---
name: crea-scheda-progetto
description: Verifica che il progetto abbia docs/progetto.json (la scheda per la card del sito dei progetti) e lo crea o aggiorna. Richiamata dalle skill crea-copertina, crea-pagina-html e crea-dashboard-html; usare anche quando l'utente chiede la scheda o la card di un progetto.
---

# crea-scheda-progetto

`docs/progetto.json` descrive il progetto per la card del sito `FedeGambe.github.io`. Lo leggono `python -m copertine pubblica` e le altre skill. Un solo file per repo, in `docs/`.

## Formato

```json
{
    "repo": "Target_Maturity_ETF_Planner",
    "t": "Target Maturity ETF Planner",
    "d": "Scraping dei rendimenti e simulazione di strategie di investimento con ETF obbligazionari a scadenza.",
    "tags": ["Finanza", "Scraping", "Simulazione"],
    "y": 2026,
    "live": "/Target_Maturity_ETF_Planner/",
    "img": "img/cover_verticale.svg"
}
```

- `repo`: nome esatto della repo su GitHub (`git remote get-url origin`, ultimo segmento senza `.git`; se manca il remote, nome della cartella del progetto).
- `t`: titolo leggibile. `d`: una frase (max ~110 caratteri) su cosa fa. `tags`: 2-4 temi/tecnologie, in maiuscola iniziale. `y`: anno di inizio (primo commit o anno corrente).
- `live`: percorso della pagina su GitHub Pages, **vuoto finché non esiste l'HTML** (vedi sotto).
- `img`: sempre `img/cover_verticale.svg` (relativo a `docs/`). Il sito ne ricava anche gli altri file della card: `cover_sfondo.svg` e `cover_soggetto.svg` (i due livelli, stessa cartella) per la card su desktop e su telefono. Se mancano, la card su telefono resta senza immagine: creali con la skill `crea-copertina`.
- Contenuti ricavati da README e struttura della repo, senza inventare.

## Flusso

1. **Controlla** se `docs/progetto.json` esiste (cartella `docs/` del progetto; creala se manca).
2. **Non c'è**: crealo con il formato sopra, `live` = `""`. Mostra all'utente titolo, descrizione e tag in una riga.
3. **C'è già**: tienilo; correggi solo campi mancanti o sbagliati (`img`, `repo`) e non riscrivere titolo/descrizione che l'utente ha già approvato.
4. **Dopo aver salvato l'HTML** (chiamata da `crea-pagina-html` o `crea-dashboard-html`): imposta `live`:
   - `docs/index.html` → `"/<repo>/"` (es. `"/Target_Maturity_ETF_Planner/"`)
   - altro file (`docs/dashboard.html`) → `"/<repo>/dashboard.html"`
   Se esistono sia `index.html` sia `dashboard.html`, `live` resta quello di `index.html`.
5. JSON valido, 4 spazi di indentazione, UTF-8, accenti non escapati.

Per mettere il progetto sul sito basta aggiungere `{ "repo": "<repo>" }` in `progetti.json` di `FedeGambe.github.io` (vedi il suo `ISTRUZIONI.md`): il sito legge questa scheda e le immagini direttamente dalla repo. Non serve (e non va usato) `python -m copertine pubblica`, che riscrive tutto `progetti.json`.
