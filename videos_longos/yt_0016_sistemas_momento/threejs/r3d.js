// Render 3D por pedidos (yt_0016). A passagem seca do Manim (PEDIDOS3D=1) grava pedidos3d/<LOTE>.json:
//   {"cenas": {"cavalo": [[quadro, estado], ...], ...}}
// Este script abre cena3d/<cena>.html, chama window.setEstado(estado) quadro a quadro e grava
//   q3d/<LOTE>_<W>x<H>/<cena>/fNNNNN.png  e  .../<cena>/pontos.json ({quadro: pontos projetados em px}).
// Estados repetidos viram cópia do PNG (sem novo render).
// Uso: node r3d.js --lote PH [--w 960 --h 540] [--so f1,f2]      Sonda: node r3d.js --sonda cavalo --estado '{...}' --png x.png
const { chromium } = require('playwright-core');
const fs = require('fs'), path = require('path'), { pathToFileURL } = require('url');
// cópia por hard link (mesmo disco: não ocupa espaço novo); cai para cópia se o link falhar
const liga = (a, b) => { try { if (fs.existsSync(b)) fs.unlinkSync(b); fs.linkSync(a, b); } catch (e) { fs.copyFileSync(a, b); } };
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const W = +arg('w', 960), H = +arg('h', 540);
const GPU = process.platform === 'win32' ? ['--use-angle=d3d11', '--enable-gpu', '--ignore-gpu-blocklist']
  : ['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist'];

async function abre(browser, cena) {
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  page.on('console', m => console.log(`[${cena}]`, m.text()));
  page.on('pageerror', e => { console.error(e); process.exit(1); });
  await page.goto(pathToFileURL(path.join(__dirname, 'cena3d', `${cena}.html`)).href);
  await page.waitForFunction(() => window.cenaPronta === true && window.fundoPronto !== false, null, { timeout: 60000 });
  return page;
}

(async () => {
  const browser = await chromium.launch({ args: GPU, executablePath: process.env.CHROMIUM_PATH || undefined });
  if (arg('sonda')) {
    const page = await abre(browser, arg('sonda'));
    const r = await page.evaluate(e => ({ pts: window.setEstado(e), med: window.medidas ? window.medidas() : null }), JSON.parse(arg('estado', '{}')));
    console.log(JSON.stringify(r));
    if (arg('png')) await page.screenshot({ path: arg('png') });
    await browser.close(); return;
  }
  const LOTE = arg('lote');
  const ped = JSON.parse(fs.readFileSync(path.join(__dirname, 'pedidos3d', `${LOTE}.json`), 'utf8'));
  const so = arg('so') ? new Set(arg('so').split(',').map(Number)) : null;
  const t0 = Date.now(); let n = 0, cop = 0;
  for (const [cena, lista] of Object.entries(ped.cenas)) {
    const OUT = path.join(__dirname, 'q3d', `${LOTE}_${W}x${H}`, cena);
    fs.mkdirSync(OUT, { recursive: true });
    const page = await abre(browser, cena.split('@')[0]);
    const vistos = new Map(), pontos = {};
    // --reusa DIR: render anterior do mesmo lote (DIR/pedidos.json + DIR/<cena>/fNNNNN.png + pontos.json); estado igual vira cópia
    const RE = arg('reusa'), dRe = RE && path.join(RE, cena);
    if (RE && fs.existsSync(path.join(dRe, 'pontos.json'))) {
      const pa = JSON.parse(fs.readFileSync(path.join(RE, 'pedidos.json'), 'utf8')).cenas[cena] || [];
      const pp = JSON.parse(fs.readFileSync(path.join(dRe, 'pontos.json'), 'utf8'));
      for (const [f, e] of pa) {
        const a = path.join(dRe, `f${String(f).padStart(5, '0')}.png`), k = JSON.stringify(e);
        if (!vistos.has(k) && fs.existsSync(a) && pp[f] !== undefined) vistos.set(k, [a, pp[f]]);
      }
    }
    for (const [f, e] of lista) {
      if (so && !so.has(f)) continue;
      const arq = path.join(OUT, `f${String(f).padStart(5, '0')}.png`), k = JSON.stringify(e);
      if (vistos.has(k)) { liga(vistos.get(k)[0], arq); pontos[f] = vistos.get(k)[1]; cop++; continue; }
      const p = await page.evaluate(x => window.setEstado(x), e);
      await page.screenshot({ path: arq });
      vistos.set(k, [arq, p]); pontos[f] = p; n++;
      if (n % 300 === 0) console.log(`${cena}: ${n} quadros`);
    }
    fs.writeFileSync(path.join(OUT, 'pontos.json'), JSON.stringify(pontos));
    await page.close();
  }
  const s = (Date.now() - t0) / 1000;
  console.log(JSON.stringify({ lote: LOTE, res: `${W}x${H}`, renderizados: n, copiados: cop, segundos: +s.toFixed(1), s_por_quadro: n ? +(s / n).toFixed(4) : 0 }));
  await browser.close();
})();
