# Pagine HTML da repository GitHub

Skill per Claude che trasformano un repository in una pagina HTML di riassunto/presentazione.

- `crea-copertina/`: libreria Python `copertine` + skill `crea-copertina` (SVG: cover a due livelli, fondo + soggetto, da cui si rigenerano cover orizzontale, verticale e banner; favicon) + script `livelli.py`, `livelli_bbox*.js`, `componi.py`. Vedi `crea-copertina/README.md`.
- `crea-pagina-html/`: skill `crea-pagina-html` + `template.html` (barra fissa, indice, capitoli, carta chiara con grana leggera, tema chiaro di default con scuro a richiesta, intro tipografica con il titolo da bordo a bordo, senza immagine). Claude compila il template leggendo il repo; la cover di `crea-copertina` serve alla scheda e alla favicon.
- `crea-scheda-progetto/`: skill `crea-scheda-progetto` (crea/verifica `docs/progetto.json`, la scheda per la card del sito; richiamata dalle altre tre).
- `crea-dashboard-html/`: skill `crea-dashboard-html` + `template.html` + `esempio.html` (dashboard interattiva in stile app moderno e clean: testata solo testo, prima i controlli a tutta larghezza, poi il form si comprime e mostra KPI e grafico, tema chiaro di default).

## Installazione

Servono Python 3.9+ e Git.

```
git clone https://github.com/FedeGambe/skill-vetrina
cd skill-vetrina/crea-copertina
pip install -e .
python -m copertine installa-skill                      # skill crea-copertina -> ~/.claude/skills/crea-copertina
cp -r ../crea-pagina-html ~/.claude/skills/crea-pagina-html  # skill crea-pagina-html (SKILL.md + template.html)
cp -r ../crea-dashboard-html ~/.claude/skills/crea-dashboard-html  # skill crea-dashboard-html
cp -r ../crea-scheda-progetto ~/.claude/skills/crea-scheda-progetto  # skill crea-scheda-progetto
```
In PowerShell: `Copy-Item -Recurse ..\crea-pagina-html $HOME\.claude\skills\crea-pagina-html` (idem per `crea-dashboard-html` e `crea-scheda-progetto`).
Poi riavvia Claude Code.

## Uso

- **Copertina**: in qualsiasi progetto chiedi "fammi una copertina per questo progetto" (skill `crea-copertina`).
- **Pagina HTML**: chiedi "fai la pagina HTML di questo repo" (skill `crea-pagina-html`).
- **A mano**:
  ```
  python -m copertine galleria -o galleria.html
  python -m copertine vortice -p girandola -f poster -t "Titolo" -o cover.svg
  ```

## Note

- Usa il clone con `pip install -e .`, non `pip install git+...`: la cartella `crea-copertina/fatte/` (copertine registrate) sta nel clone, non è su GitHub e su un altro PC parte vuota. Il clone serve anche per aggiungere stili e palette.
- `python -m copertine pubblica` è del vecchio flusso e riscrive tutto `progetti.json` del sito: per aggiungere un progetto al sito basta una riga `{ "repo": ... }` (vedi `ISTRUZIONI.md` di `FedeGambe.github.io`).
