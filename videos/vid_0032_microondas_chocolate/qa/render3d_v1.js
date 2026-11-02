// Render determinístico do 3D do vid_0032 (só o C01): Playwright (Chromium) chama window.setFrame(f) e salva PNGs.
// No render completo, grava em timeline.json → projecao_3d os pixels dos 4 centros das manchas e dos 4 cantos da barra.
// Uso: node render3d.js [--w 540 --h 960 --fps 15] [--out frames3d_540x960] [--quadros 0,45,195]
const { chromium } = require('playwright-core');
const fs = require('fs'), path = require('path'), { pathToFileURL } = require('url');

const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const W = +arg('w', 540), H = +arg('h', 960), FPS = +arg('fps', 15);
const OUT = path.resolve(__dirname, arg('out', `frames3d_${W}x${H}`));
const TLP = path.join(__dirname, 'timeline.json');
const TL = JSON.parse(fs.readFileSync(TLP, 'utf8'));
const total = Math.round(TL.duracao_3d_s * FPS);
const lista = arg('quadros') ? arg('quadros').split(',').map(Number) : [...Array(total).keys()];

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ args: ['--use-angle=d3d11', '--enable-gpu', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  page.on('console', m => console.log('[página]', m.text()));
  page.on('pageerror', e => { console.error(e); process.exit(1); });
  await page.addInitScript(([tl, fps]) => { window.TIMELINE = tl; window.FPS = fps; }, [TL, FPS]);
  await page.goto(pathToFileURL(path.join(__dirname, 'cena3d', 'index.html')).href);
  await page.waitForFunction(() => window.cenaPronta === true);
  const G = TL.geometria, zt = await page.evaluate(() => window.TOPO_BARRA);
  const hx = G.barra.comprimento_cm / 2, hy = G.barra.largura_cm / 2;
  const pontos = [...G.manchas_x_cm.map(x => [x, 0, zt]), [-hx, hy, zt], [hx, hy, zt], [hx, -hy, zt], [-hx, -hy, zt]];
  const manchas = [], barra = [];
  const t0 = Date.now();
  for (const [n, f] of lista.entries()) {
    await page.evaluate(q => window.setFrame(q), f);
    await page.screenshot({ path: path.join(OUT, `f${String(f).padStart(5, '0')}.png`) });
    const px = await page.evaluate(ps => ps.map(p => window.projeta(p).map(v => +v.toFixed(2))), pontos);
    manchas.push(px.slice(0, 4)); barra.push(px.slice(4));
    if (n % 50 === 0) console.log(`quadro ${f} (${n + 1}/${lista.length})`);
  }
  const s = (Date.now() - t0) / 1000;
  const info = { resolucao: `${W}x${H}`, fps: FPS, quadros: lista.length, segundos: +s.toFixed(1), s_por_quadro: +(s / lista.length).toFixed(4) };
  console.log(JSON.stringify(info));
  if (!arg('quadros')) {
    fs.writeFileSync(path.join(OUT, 'custo.json'), JSON.stringify(info, null, 2));
    TL.projecao_3d = { resolucao: [W, H], fps: FPS, ordem_barra: 'sup-esq, sup-dir, inf-dir, inf-esq', manchas_px: manchas, barra_px: barra };
    fs.writeFileSync(TLP, JSON.stringify(TL, null, 1));
  }
  await browser.close();
})();
