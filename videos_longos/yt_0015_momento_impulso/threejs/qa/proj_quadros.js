// Projeção, quadro a quadro, dos pontos com rótulo do Manim (window.pontos3d) → threejs/proj_<trecho>_quadros.json
// {"quadros": [{nome: [mx, my]}, ...]} em coordenadas do Manim. Usado quando a câmera ou o objeto se movem (ex.: F2, cavalo).
// Uso: node qa/proj_quadros.js --trecho cavalo
const { chromium } = require('playwright-core');
const fs = require('fs'), path = require('path'), { pathToFileURL } = require('url');
const UNIT = path.resolve(__dirname, '..');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const TR = arg('trecho', 'cavalo'), W = 960, H = 540, FPS = 15;
const TL = JSON.parse(fs.readFileSync(path.join(UNIT, `timeline_${TR}.json`), 'utf8'));
const total = Math.round(TL.duracao_s * FPS);
(async () => {
  const browser = await chromium.launch({ args: ['--use-angle=d3d11', '--enable-gpu'], executablePath: process.env.CHROMIUM_PATH || undefined });
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  await page.addInitScript(([tl, fps]) => { window.TIMELINE = tl; window.FPS = fps; }, [TL, FPS]);
  await page.goto(pathToFileURL(path.join(UNIT, 'cena3d', `${TR}.html`)).href);
  await page.waitForFunction(() => window.cenaPronta === true, null, { timeout: 60000 });
  const quadros = [];
  for (let f = 0; f < total; f++) {
    const r = await page.evaluate(q => {
      window.setFrame(q);
      const p = window.pontos3d(), o = {};
      for (const k in p) { const [px, py] = window.projeta(p[k]); o[k] = [px / innerWidth * 16 - 8, 4.5 - py / innerHeight * 9]; }
      return o;
    }, f);
    quadros.push(r);
  }
  const medidas = await page.evaluate(() => window.medidas);
  fs.writeFileSync(path.join(UNIT, `proj_${TR}_quadros.json`), JSON.stringify({ quadros, medidas }));
  console.log(JSON.stringify({ trecho: TR, quadros: total, medidas }));
  await browser.close();
})();
