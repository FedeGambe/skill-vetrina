// node bbox.js file1.svg ... : stringe il viewBox di ogni cover_soggetto.svg al riquadro del disegno (+ margine per ombre e sfocature)
const { chromium } = require("playwright");
const fs = require("fs");
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  for (const f of process.argv.slice(2)) {
    let svg = fs.readFileSync(f, "utf8");
    await p.setContent(`<html><body style="margin:0">${svg}</body></html>`);
    const bb = await p.evaluate(() => {
      const s = document.querySelector("svg");
      let x1 = 1e9, y1 = 1e9, x2 = -1e9, y2 = -1e9;
      for (const c of s.children) {
        if (c.tagName === "defs") continue;
        const r = c.getBBox(); if (!r.width && !r.height) continue;
        // riquadro nel sistema del viewBox (gestisce transform del figlio)
        const m = c.getCTM(), sm = s.getCTM().inverse(), pts = [[r.x, r.y], [r.x + r.width, r.y], [r.x, r.y + r.height], [r.x + r.width, r.y + r.height]];
        for (const [x, y] of pts) { const pt = new DOMPoint(x, y).matrixTransform(m).matrixTransform(sm); x1 = Math.min(x1, pt.x); y1 = Math.min(y1, pt.y); x2 = Math.max(x2, pt.x); y2 = Math.max(y2, pt.y); }
      }
      const vb = s.viewBox.baseVal;  // non uscire dalla tela originale
      const r = [Math.max(vb.x, x1), Math.max(vb.y, y1), Math.min(vb.x + vb.width, x2), Math.min(vb.y + vb.height, y2)]; r.tela = [vb.x, vb.y, vb.x + vb.width, vb.y + vb.height]; return {0:r[0],1:r[1],2:r[2],3:r[3],tela:r.tela};
    });
    const pad = 12, t = bb.tela, [x1, y1, x2, y2] = [Math.max(t[0], bb[0] - pad), Math.max(t[1], bb[1] - pad), Math.min(t[2], bb[2] + pad), bb[3]];
    const vb = [x1, y1, x2 - x1, y2 - y1].map(v => Math.round(v * 10) / 10).join(" ");
    svg = svg.replace(/viewBox="[^"]*"/, `viewBox="${vb}"`);
    fs.writeFileSync(f, svg);
    console.log(f.split("/").slice(-4).join("/"), "viewBox", vb);
  }
  await b.close();
})();
