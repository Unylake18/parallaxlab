// QA: erro (px) entre a projeção 3D dos cruzamentos das espiras com z = 0 e as posições do Manim, na vista de cima.
// Uso (na unidade): node qa/alinhamento.js [quadro]
const { chromium } = require('playwright-core');
const fs = require('fs'), path = require('path'), { pathToFileURL } = require('url');
const UNIT = path.resolve(__dirname, '..');
const TL = JSON.parse(fs.readFileSync(path.join(UNIT, 'timeline.json'), 'utf8'));
const W = 540, H = 960, FPS = 15, f = +(process.argv[2] || 1250);
const G = TL.geometria, K = G.fator_3d_manim, [cx, cy] = G.centro_topo_manim;
(async () => {
  const browser = await chromium.launch({ args: ['--use-angle=d3d11'] });
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  await page.addInitScript(([tl, fps]) => { window.TIMELINE = tl; window.FPS = fps; }, [TL, FPS]);
  await page.goto(pathToFileURL(path.join(UNIT, 'cena3d', 'index.html')).href);
  await page.waitForFunction(() => window.cenaPronta === true);
  await page.evaluate(q => window.setFrame(q), f);
  let pior = 0;
  for (const [r, meio] of [[G.raio_maior - G.raio_menor, 0], [G.raio_maior + G.raio_menor, 0.5], [G.raio_maior, 0]]) {
    for (let k = 0; k < G.n_espiras; k++) {
      const phi = G.phi0 + 2 * Math.PI * (k + meio) / G.n_espiras;
      const [px, py] = await page.evaluate(p => window.projeta(p), [r * Math.cos(phi), r * Math.sin(phi), 0]);
      const mx = (cx + K * r * Math.cos(phi) + 4.5) / 9 * W, my = (8 - (cy + K * r * Math.sin(phi))) / 16 * H;
      pior = Math.max(pior, Math.hypot(px - mx, py - my));
    }
  }
  console.log(JSON.stringify({ quadro: f, t: f / FPS, pior_erro_px: +pior.toFixed(4) }));
  await browser.close();
})();
