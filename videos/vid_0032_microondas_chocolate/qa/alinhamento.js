// QA: erro (px) entre a projeção 3D (centros das manchas e cantos da barra, no topo da barra) e as posições do Manim.
// Uso (na unidade): node qa/alinhamento.js [quadro]   (padrão: quadro da troca, c01_camera_topo)
const { chromium } = require('playwright-core');
const fs = require('fs'), path = require('path'), { pathToFileURL } = require('url');
const UNIT = path.resolve(__dirname, '..');
const TL = JSON.parse(fs.readFileSync(path.join(UNIT, 'timeline.json'), 'utf8'));
const CAMPO = JSON.parse(fs.readFileSync(path.join(UNIT, 'cena3d', 'campo.json'), 'utf8'));
const RELEVO = 'data:image/png;base64,' + fs.readFileSync(path.join(UNIT, 'cena3d', 'relevo.png')).toString('base64');
const W = 540, H = 960, FPS = 15, f = +(process.argv[2] || Math.round(TL.eventos.c01_camera_topo * FPS));
const G = TL.geometria, K = G.manim_por_cm, [cx, cy] = G.centro_barra_manim;
(async () => {
  const browser = await chromium.launch({ args: ['--use-angle=d3d11'] });
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  await page.addInitScript(([tl, fps, campo, rel]) => { Object.assign(window, { TIMELINE: tl, FPS: fps, CAMPO: campo, RELEVO_URL: rel }); }, [TL, FPS, CAMPO, RELEVO]);
  await page.goto(pathToFileURL(path.join(UNIT, 'cena3d', 'index.html')).href);
  await page.waitForFunction(() => window.cenaPronta === true);
  await page.evaluate(q => window.setFrame(q), f);
  const zt = await page.evaluate(() => window.TOPO_BARRA), hx = G.barra.comprimento_cm / 2, hy = G.barra.largura_cm / 2;
  const pts = [...G.manchas_x_cm.map(x => [x, 0]), [-hx, hy], [hx, hy], [hx, -hy], [-hx, -hy]];
  const erros = [];
  for (const [x, y] of pts) {
    const [px, py] = await page.evaluate(p => window.projeta(p), [x, y, zt]);
    const mx = (cx + K * x + 4.5) / 9 * W, my = (8 - (cy + K * y)) / 16 * H;
    erros.push(+Math.hypot(px - mx, py - my).toFixed(3));
  }
  console.log(JSON.stringify({ quadro: f, t: f / FPS, erros_px_manchas: erros.slice(0, 4), erros_px_cantos: erros.slice(4), pior_erro_px: Math.max(...erros) }));
  await browser.close();
})();
