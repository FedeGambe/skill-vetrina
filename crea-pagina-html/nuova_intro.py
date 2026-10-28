"""Porta una pagina fatta con crea-pagina-html dalla cover a tutto schermo all'intro tipografica (titolo da bordo a bordo).

Uso: python nuova_intro.py <pagina.html> "Occhiello · Python · 2026"
"""
import re
import sys

INTRO_CSS = """
/* INTRO: niente immagine, niente ombre. Occhiello mono con trattino colorato, titolo su una riga da bordo a bordo
   (il JS in fondo scala il font sulla larghezza; sotto i 44px torna a capo), sottotitolo, tag, riga da 3px. */
.intro{max-width:1320px; margin:0 auto; padding:calc(var(--barra) + clamp(32px,6vw,88px)) 20px 0}
.intro-testo{padding-bottom:48px; border-bottom:3px solid var(--ink)}
.occhiello{display:flex; gap:12px; align-items:center; margin:0 0 24px; font:600 .72rem/1 var(--f-data); letter-spacing:.1em; text-transform:uppercase; color:var(--ink-3)}
.occhiello::before{content:""; flex:none; width:32px; height:3px; background:var(--c2)}
.intro h1{font-size:clamp(2.6rem,8.6vw,7.4rem); line-height:.95; letter-spacing:-.04em; text-wrap:pretty}
.intro h1.adatta{white-space:nowrap; text-wrap:nowrap}
.intro h1 em{color:var(--c2); font-style:italic}
.intro .sottotitolo{font-size:clamp(1.05rem,1.6vw,1.25rem); line-height:1.5; color:var(--ink-2); margin:24px 0 0}
.intro .sottotitolo p{margin:0} .intro .sottotitolo strong{color:var(--ink)}
.tags{display:flex; flex-wrap:wrap; gap:6px; margin-top:24px}
.tags span{font:600 .7rem/1 var(--f-data); border:1px solid var(--line); padding:5px 8px; border-radius:999px; color:var(--ink-2)}
"""
DICITURE_CSS = """/* Diciture (frontespizio): una riga di dati sotto i tag */
.intro .diciture{display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:18px 40px; margin-top:40px; padding-top:20px;
  border-top:1px solid var(--line); font-size:.9rem; line-height:1.45; color:var(--ink-2)}
.intro .diciture .sx, .intro .diciture .dx{display:contents}
.intro .diciture hr{display:none}
.intro .diciture b{font-family:var(--f-display); font-weight:800; font-size:1.05rem; color:var(--ink)}
"""
MOBILE = """@media (max-width:700px){
  .solo-largo{display:none}
  .azioni{gap:6px}
  .bottone-barra{padding:7px 10px; letter-spacing:.05em}
  footer{overflow-wrap:anywhere}
}
"""
FIT_JS = """
// INTRO: titolo su una riga da bordo a bordo; se il font scende sotto i 44px (telefono) torna a capo normale
const h1 = document.querySelector(".intro h1");
function adattaTitolo() {
  h1.classList.add("adatta"); h1.style.fontSize = "100px";
  const f = 100 * h1.clientWidth / h1.scrollWidth;
  if (f < 44) { h1.classList.remove("adatta"); h1.style.fontSize = ""; } else h1.style.fontSize = Math.min(f, 220) + "px";
}
adattaTitolo(); addEventListener("resize", adattaTitolo); document.fonts?.ready.then(adattaTitolo);
"""
# selettori della vecchia cover: le regole che li nominano spariscono intere
VECCHIE = (".copertina", ".logo-cover", ".barra:not(.compatta) .bottone-barra", ".bauhaus", ".slide-testa", ".soggetto", ".diciture", ".tags")
OMBRE = ("; box-shadow:0 14px 28px #0003", "; box-shadow:0 18px 40px -22px #000a, inset 0 1px 0 #ffffff14",
         "; box-shadow:0 18px 40px -22px #000a", "; box-shadow:0 1px 0 var(--line), 0 12px 30px -18px rgba(28,27,25,.35)")


def togli_regole(css):
    """Toglie dalle regole i selettori della vecchia cover; se non ne resta nessuno toglie la regola intera."""
    def via(m):
        testa, corpo = m.group(1), m.group(2)
        i = testa.rfind("*/") + 2 if "*/" in testa else 0  # i commenti davanti al selettore restano
        commento, sel = testa[:i], testa[i:]
        tieni = [x for x in sel.split(",") if not any(v in x for v in VECCHIE)]
        if len(tieni) == len(sel.split(",")):
            return m.group(0)
        return commento + ("\n" + ",".join(t.strip() for t in tieni) + "{" + corpo + "}" if tieni else "\n")
    return re.sub(r"([^{}]*)\{([^{}]*)\}", via, css)


def converti(s, occhiello):
    s = re.sub(r"/\* COVER A DUE LIVELLI:.*?/\* /COVER A DUE LIVELLI \*/\n", "", s, flags=re.S)
    a, b = s.index("<style>") + len("<style>"), s.index("</style>")
    css = togli_regole(s[a:b])
    css = re.sub(r"@media[^{]*\{\s*\}", "", css)  # media query rimaste vuote
    for o in OMBRE:
        css = css.replace(o, "")
    css = re.sub(r" --c2-cover:#[0-9a-fA-F]+;", "", css)
    css = re.sub(r"\n\s*\n(\s*\n)+", "\n\n", css)

    m = re.search(r'<section class="copertina[^"]*" id="copertina">.*?</section>', s, re.S).group(0)
    h1 = re.search(r"<h1>.*?</h1>", m, re.S).group(0)
    sotto = re.search(r'<(div|p) class="sottotitolo">.*?</\1>', m, re.S).group(0)
    tags = re.search(r'<div class="tags">.*?</div>', m, re.S).group(0)
    dic = re.search(r'<div class="diciture">.*?</div>\s*</div>\s*</div>', m, re.S)
    if "--c2:" not in css and "--arancio:" in css:  # pagine più vecchie: il colore caldo si chiama --arancio
        css += "\n:root{--c2:var(--arancio)}\n"
    if "scroll-snap-type" in css:  # pagine con lo scroll a scatti: l'intro resta il primo punto d'aggancio
        css += "\n.intro{scroll-snap-align:start}\n"
    css += INTRO_CSS + (DICITURE_CSS if dic else "") + MOBILE
    s = s[:a] + css + s[b:]
    extra = "\n  " + dic.group(0) if dic else ""
    s = s.replace(m, f'<section class="intro" id="copertina"><div class="intro-testo">\n  {occhiello}\n  {h1}\n  {sotto}\n  {tags}{extra}\n</div></section>')

    s = re.sub(r'\n *if \(!riduciMovimento\) copertina\.style\.setProperty\("--p"[^\n]*', "", s)
    if s.count("riduciMovimento") == 1:
        s = re.sub(r"\nconst riduciMovimento = [^\n]*", "", s)
    i = s.rindex("</script>")
    return s[:i] + FIT_JS + s[i:]


if __name__ == "__main__":
    f, testo = sys.argv[1], sys.argv[2]
    nuovo = converti(open(f, encoding="utf-8").read(), f'<p class="occhiello">{testo}</p>')  # prima converte, poi scrive
    open(f, "w", encoding="utf-8").write(nuovo)
