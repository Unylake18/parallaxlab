// QA 3D × Manim (16:9, 960×540): erro em px entre a projeção 3D de pontos do plano y = 0 e onde o Manim os desenharia.
// Mapeamento: Manim = (cx + K·(x − x_cam), cy + K·z); pixel = ((mx + 8)/16·W, (4,5 − my)/9·H).
// Uso: node qa/alinhamento.js --trecho c01|c13   (quadros em timeline.qa_alinhamento.quadros). Aceitação: ≤ 2 px.
const { chromium } = require('playwright-core');
const fs = require('fs'), path = require('path'), { pathToFileURL } = require('url');
const UNIT = path.resolve(__dirname, '..');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const TR = arg('trecho', 'c01'), W = 960, H = 540, FPS = 15;
const TL = JSON.parse(fs.readFileSync(path.join(UNIT, `timeline_${TR}.json`), 'utf8'));
const [cx, cy] = TL.geometria.centro_manim, K = TL.geometria.fator_3d_manim;
(async () => {
  const browser = await chromium.launch({ args: ['--use-angle=d3d11', '--enable-gpu'], executablePath: process.env.CHROMIUM_PATH || undefined });
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  await page.addInitScript(([tl, fps]) => { window.TIMELINE = tl; window.FPS = fps; }, [TL, FPS]);
  await page.goto(pathToFileURL(path.join(UNIT, 'cena3d', `${TR}.html`)).href);
  await page.waitForFunction(() => window.cenaPronta === true);
  let pior = 0; const linhas = [];
  for (const f of TL.qa_alinhamento.quadros) {
    const t = f / FPS;
    await page.evaluate(q => window.setFrame(q), f);
    const camx = await page.evaluate(t => (window.TIMELINE.cam_x ? window.B3D.chaves(window.TIMELINE.cam_x, t, 'x') : 0), t);
    let pts = [];
    if (TR === 'c01' || TR === 'trilho') {
      const s = await page.evaluate(t => window.estadoCarrinhos(t), t);
      for (const x of [s.xa, s.xb]) for (const z of [0.0, 0.45, 0.9]) pts.push([x, 0, z]);
    } else {
      const R = TL.raio, th1 = R.theta1 * Math.PI / 180, th2 = Math.asin(Math.sin(th1) / R.n);
      pts = [[0, 0, 0], [-R.L * Math.sin(th1), 0, R.L * Math.cos(th1)], [R.L * Math.sin(th1), 0, R.L * Math.cos(th1)],
        [-R.z_fundo / Math.cos(th2) * Math.sin(th2), 0, R.z_fundo], [TL.tanque.x0, 0, 0], [TL.tanque.x1, 0, R.z_fundo]];
    }
    let pf = 0;
    for (const p of pts) {
      const [px, py] = await page.evaluate(p => window.projeta(p), p);
      const mx = cx + K * (p[0] - camx), my = cy + K * p[2];
      pf = Math.max(pf, Math.hypot(px - (mx + 8) / 16 * W, py - (4.5 - my) / 9 * H));
    }
    linhas.push({ quadro: f, t: +t.toFixed(2), pior_erro_px: +pf.toFixed(3) }); pior = Math.max(pior, pf);
  }
  console.log(JSON.stringify({ trecho: TR, pior_erro_px: +pior.toFixed(3), quadros: linhas }));
  await browser.close();
})();
