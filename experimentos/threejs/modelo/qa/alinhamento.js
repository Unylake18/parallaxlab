// QA: erro (px) entre a projeção 3D de pontos do plano z = 0 e onde o Manim os desenharia, na vista de cima.
// Mapeamento esperado: ponto 3D (x, y, 0) → Manim (cx + K·x, cy + K·y) → pixel.
// Uso (dentro da unidade): node qa/alinhamento.js [quadro]   (padrão: timeline.qa_alinhamento.quadro)
// Aceitação: pior erro ≤ 2 px no preview 540×960.
const { chromium } = require('playwright-core');
const fs = require('fs'), path = require('path'), { pathToFileURL } = require('url');
const UNIT = path.resolve(__dirname, '..');
const TL = JSON.parse(fs.readFileSync(path.join(UNIT, 'timeline.json'), 'utf8'));
const QA = TL.qa_alinhamento, W = 540, H = 960, FPS = 15, f = +(process.argv[2] || QA.quadro);
const K = TL.geometria.fator_3d_manim, [cx, cy] = TL.geometria.centro_topo_manim;
const GPU = process.platform === 'win32' ? ['--use-angle=d3d11'] : ['--use-gl=swiftshader', '--enable-webgl'];
(async () => {
  const browser = await chromium.launch({ args: GPU, executablePath: process.env.CHROMIUM_PATH || undefined });
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  await page.addInitScript(([tl, fps]) => { window.TIMELINE = tl; window.FPS = fps; }, [TL, FPS]);
  await page.goto(pathToFileURL(path.join(UNIT, 'cena3d', 'index.html')).href);
  await page.waitForFunction(() => window.cenaPronta === true);
  await page.evaluate(q => window.setFrame(q), f);
  let pior = 0;
  for (let k = 0; k < QA.n_pontos; k++) {
    const phi = 2 * Math.PI * k / QA.n_pontos, x = QA.raio_3d * Math.cos(phi), y = QA.raio_3d * Math.sin(phi);
    const [px, py] = await page.evaluate(p => window.projeta(p), [x, y, 0]);
    const mx = (cx + K * x + 4.5) / 9 * W, my = (8 - (cy + K * y)) / 16 * H;
    pior = Math.max(pior, Math.hypot(px - mx, py - my));
  }
  console.log(JSON.stringify({ quadro: f, t: f / FPS, pior_erro_px: +pior.toFixed(4) }));
  await browser.close();
})();
