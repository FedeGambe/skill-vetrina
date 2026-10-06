# Pagine HTML da repository GitHub

Skill per Claude che trasformano un repository in una pagina HTML di riassunto/presentazione.

- `cover/`: libreria Python `copertine` + skill `copertine` (SVG: cover a schermo intero, banner, poster, favicon). Vedi `cover/README.md`.
- `html/`: skill `html` + `template.html` (barra fissa, indice, capitoli, tema chiaro/scuro, cover a tutto schermo). Claude compila il template leggendo il repo e usa `cover/` per la cover.

## Installazione skill

```
cd cover && pip install -e .
python -m copertine installa-skill                      # skill copertine -> ~/.claude/skills/copertine
cp -r html ~/.claude/skills/html                        # skill html (SKILL.md + template.html)
```
Poi riavvia Claude Code e chiedi: "fai la pagina HTML di questo repo".
