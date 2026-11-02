// Render determinístico do 3D do vid_0032 v2 (trechos do timeline: gancho C01 e C05/C06): Playwright (Chromium)
// chama window.setFrame(f) e salva PNGs com o número absoluto do quadro. No render completo, grava em timeline.json →
// projecao_3d, por quadro: pixels das 4 manchas, dos 4 cantos da barra e da etiqueta; caixas (Manim) de barra, prato, gotas, relevo.
// Uso: node render3d.js [--w 540 --h 960 --fps 15] [--out frames3d_540x960] [--quadros 0,45,195]
const { chromium } = require('playwright-core');
const fs = require('fs'), path = require('path'), { pathToFileURL } = require('url');

const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const W = +arg('w', 540), H = +arg('h', 960), FPS = +arg('fps', 15);
const OUT = path.resolve(__dirname, arg('out', `frames3d_${W}x${H}`));
const TLP = path.join(__dirname, 'timeline.json');
const TL = JSON.parse(fs.readFileSync(TLP, 'utf8'));
const CAMPO = JSON.parse(fs.readFileSync(path.join(__dirname, 'cena3d', 'campo.json'), 'utf8'));
const RELEVO = 'data:image/png;base64,' + fs.readFileSync(path.join(__dirname, 'cena3d', 'relevo.png')).toString('base64');
const todos = TL.trechos_3d.flatMap(([a, b]) => [...Array(Math.round((b - a) * FPS)).keys()].map(k => Math.round(a * FPS) + k));
const lista = arg('quadros') ? arg('quadros').split(',').map(Number) : todos;

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ args: ['--use-angle=d3d11', '--enable-gpu', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  page.on('console', m => console.log('[página]', m.text()));
  page.on('pageerror', e => { console.error(e); process.exit(1); });
  await page.addInitScript(([tl, fps, campo, rel, luz]) => { Object.assign(window, { TIMELINE: tl, FPS: fps, CAMPO: campo, RELEVO_URL: rel }); },
    [TL, FPS, CAMPO, RELEVO]);
  await page.goto(pathToFileURL(path.join(__dirname, 'cena3d', 'index.html')).href);
  await page.waitForFunction(() => window.cenaPronta === true);
  console.log('erro dos ventres da fita (1 − |sen|):', await page.evaluate(() => window.erroVentres));
  const G = TL.geometria, zt = await page.evaluate(() => window.TOPO_BARRA);
  const hx = G.barra.comprimento_cm / 2, hy = G.barra.largura_cm / 2, [ex, ez] = G.etiqueta_cm.centro, [ew, eh] = G.etiqueta_cm.tamanho;
  const yf = G.corpo_cm.y[0] - 0.03;
  const pontos = [...G.manchas_x_cm.map(x => [x, 0, zt]), [-hx, hy, zt], [hx, hy, zt], [hx, -hy, zt], [-hx, -hy, zt],
    [ex - ew / 2, yf, ez + eh / 2], [ex + ew / 2, yf, ez + eh / 2], [ex + ew / 2, yf, ez - eh / 2], [ex - ew / 2, yf, ez - eh / 2],
    [0, 0, G.prato.altura_cm + G.prato.espessura_cm]];
  const proj = {};
  const t0 = Date.now();
  for (const [n, f] of lista.entries()) {
    await page.evaluate(q => window.setFrame(q), f);
    await page.screenshot({ path: path.join(OUT, `f${String(f).padStart(5, '0')}.png`) });
    const px = await page.evaluate(ps => ps.map(p => window.projeta(p).map(v => +v.toFixed(2))), pontos);
    proj[f] = { manchas: px.slice(0, 4), barra: px.slice(4, 8), etiqueta: px.slice(8, 12), prato_centro: px[12], caixas: await page.evaluate(() => window.caixas3d()) };
    if (n % 100 === 0) console.log(`quadro ${f} (${n + 1}/${lista.length})`);
  }
  const s = (Date.now() - t0) / 1000;
  const info = { resolucao: `${W}x${H}`, fps: FPS, quadros: lista.length, segundos: +s.toFixed(1), s_por_quadro: +(s / lista.length).toFixed(4) };
  console.log(JSON.stringify(info));
  if (!arg('quadros')) {
    fs.writeFileSync(path.join(OUT, 'custo.json'), JSON.stringify(info, null, 2));
    TL.projecao_3d = { resolucao: [W, H], fps: FPS, nota: 'px no quadro WxH; caixas em unidades do Manim [x0, y0, x1, y1]', quadros: proj };
    fs.writeFileSync(TLP, JSON.stringify(TL, null, 1));
  }
  await browser.close();
})();
