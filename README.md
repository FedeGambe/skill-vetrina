# Pagine HTML da repository GitHub

Skill per Claude che trasformano un repository in una pagina HTML di riassunto/presentazione.

- `cover/`: libreria Python `copertine` + skill `copertine` (SVG: cover a schermo intero, banner, poster, favicon). Vedi `cover/README.md`.
- `html/`: skill `html` + `template.html` (barra fissa, indice, capitoli, tema chiaro/scuro, cover a tutto schermo). Claude compila il template leggendo il repo e usa `cover/` per la cover.

## Installazione

Servono Python 3.9+ e Git.

```
git clone https://github.com/FedeGambe/skill-vetrina
cd skill-vetrina/cover
pip install -e .
python -m copertine installa-skill                      # skill copertine -> ~/.claude/skills/copertine
cp -r ../html ~/.claude/skills/html                     # skill html (SKILL.md + template.html)
```
In PowerShell l'ultima riga è `Copy-Item -Recurse ..\html $HOME\.claude\skills\html`.
Poi riavvia Claude Code.

## Uso

- **Copertina**: in qualsiasi progetto chiedi "fammi una copertina per questo progetto" (skill `copertine`).
- **Pagina HTML**: chiedi "fai la pagina HTML di questo repo" (skill `html`).
- **A mano**:
  ```
  python -m copertine galleria -o galleria.html
  python -m copertine vortice -p girandola -f poster -t "Titolo" -o cover.svg
  ```

## Note

- Usa il clone con `pip install -e .`, non `pip install git+...`: la cartella `cover/fatte/` (copertine registrate) sta nel clone, non è su GitHub e su un altro PC parte vuota. Il clone serve anche per aggiungere stili e palette.
- `python -m copertine pubblica` è legato al setup dell'autore: cerca il sito `FedeGambe.github.io` accanto alla cartella di lavoro. Chi scarica la skill può ignorarlo o cambiare il percorso in `cover/copertine/__main__.py`.
