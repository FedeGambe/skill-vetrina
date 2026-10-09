// node bbox_intero.js cover_soggetto.svg ... : mostra il soggetto per intero (niente ritaglio dei riquadri interni)
// e stringe il viewBox attorno a tutti gli elementi disegnati, con margine su tutti i lati; scrive anche width/height.
const { chromium } = require("playwright");
const fs = require("fs");
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  for (const f of process.argv.slice(2)) {
    let svg = fs.readFileSync(f, "utf8").replace(/overflow="hidden"/g, 'overflow="visible"');
    // viewBox provvisorio molto largo, per misurare senza tagli
    const h0 = svg.slice(0, svg.indexOf(">") + 1);
    const prov = h0.replace(/\s(width|height)="[^"]*"/g, "").replace(/viewBox="[^"]*"/, 'viewBox="-2000 -2000 6000 6000"') + svg.slice(h0.length);
    await p.setContent(`<html><body style="margin:0">${prov}</body></html>`);
    const bb = await p.evaluate(() => {
      const root = document.querySelector("svg"), inv = root.getCTM().inverse();
      let x1 = 1e9, y1 = 1e9, x2 = -1e9, y2 = -1e9;
      for (const e of root.querySelectorAll("path,rect,circle,ellipse,polygon,polyline,line,image,text,use")) {
        if (e.closest("defs,clipPath,mask,pattern,filter,linearGradient,radialGradient")) continue;
        if (e.parentElement === root && e.tagName === "rect" && e.getAttribute("width") === "1600") continue;  // eventuale velo a tutta tela
        const r = e.getBBox(); if (!r.width || !r.height) continue;
        const m = e.getCTM();
        for (const [x, y] of [[r.x, r.y], [r.x + r.width, r.y], [r.x, r.y + r.height], [r.x + r.width, r.y + r.height]]) {
          const q = new DOMPoint(x, y).matrixTransform(m).matrixTransform(inv);
          x1 = Math.min(x1, q.x); y1 = Math.min(y1, q.y); x2 = Math.max(x2, q.x); y2 = Math.max(y2, q.y);
        }
      }
      return [x1, y1, x2, y2];
    });
    const pad = 16, [x1, y1, x2, y2] = [bb[0] - pad, bb[1] - pad, bb[2] + pad, bb[3] + pad];
    const vb = [x1, y1, x2 - x1, y2 - y1].map(v => Math.round(v * 10) / 10);
    const head = svg.slice(0, svg.indexOf(">") + 1);
    const nuovo = head.replace(/\s(width|height)="[^"]*"/g, "").replace(/viewBox="[^"]*"/, `viewBox="${vb.join(" ")}"`)
      .replace("<svg ", `<svg width="${Math.round(vb[2])}" height="${Math.round(vb[3])}" `);
    fs.writeFileSync(f, nuovo + svg.slice(head.length));
    console.log(f.split("/").slice(-4).join("/"), "viewBox", vb.join(" "));
  }
  await b.close();
})();
