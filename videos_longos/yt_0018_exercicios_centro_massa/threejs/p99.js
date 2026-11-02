// yt_0018 v3 §5: teste de exposição. Para alguns quadros do lago (pedidos3d/<LOTE>.json), grava o quadro inteiro e as máscaras (só a folha,
// só o gafanhoto) em ../renders/v5/p99/; o p99.py mede o percentil 99 dos pixels de cada máscara no quadro inteiro.
// uso: node p99.js --lote PH --q 30,90,150
const { chromium } = require('playwright-core');
const fs = require('fs'), path = require('path'), { pathToFileURL } = require('url');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const W = 960, H = 540;
(async () => {
  const browser = await chromium.launch({ args: ['--use-angle=d3d11', '--enable-gpu', '--ignore-gpu-blocklist'], executablePath: process.env.CHROMIUM_PATH || undefined });
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(path.join(__dirname, 'cena3d', 'lago.html')).href);
  await page.waitForFunction(() => window.cenaPronta === true, null, { timeout: 60000 });
  const LOTE = arg('lote'), qs = new Set(arg('q').split(',').map(Number));
  const lista = JSON.parse(fs.readFileSync(path.join(__dirname, 'pedidos3d', `${LOTE}.json`), 'utf8')).cenas.lago;
  const OUT = path.join(__dirname, '..', 'renders', 'v7', 'p99'); fs.mkdirSync(OUT, { recursive: true });
  for (const [f, e] of lista) {
    if (!qs.has(f)) continue;
    for (const [nome, extra] of [['full', {}], ['gaf', { mascara: 'gaf' }], ['folha', { mascara: 'folha' }]]) {
      await page.evaluate(x => window.setEstado(x), Object.assign({}, e, extra));
      await page.screenshot({ path: path.join(OUT, `${LOTE}_${f}_${nome}.png`), omitBackground: true });
    }
  }
  console.log('ok');
  await browser.close();
})();
