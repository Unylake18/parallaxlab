// Projeções dos pontos com rótulo do Manim (cota do muro, pouso) nos trechos do manequim + QA de alinhamento.
// Uso: node qa/muro_proj.js --trecho hook|e4  → threejs/proj_<trecho>.json  {ref: {nome: {quadro: [mx, my]}}, qa: [...]}
// O Manim desenha nas coordenadas do quadro de referência de cada janela; o QA mede, em todos os quadros da janela, a distância (px a
// 960×540) entre a projeção real do 3D e a referência. Aceitação: ≤ 2 px.
const { chromium } = require('playwright-core');
const fs = require('fs'), path = require('path'), { pathToFileURL } = require('url');
const UNIT = path.resolve(__dirname, '..');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const TR = arg('trecho', 'hook'), W = 960, H = 540, FPS = +(process.env.FPS3D || 15);
const TL = JSON.parse(fs.readFileSync(path.join(UNIT, `timeline_${TR}.json`), 'utf8'));
const paraManim = ([px, py]) => [px / W * 16 - 8, 4.5 - py / H * 9];
(async () => {
  const browser = await chromium.launch({ args: ['--use-angle=d3d11', '--enable-gpu'], executablePath: process.env.CHROMIUM_PATH || undefined });
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  await page.addInitScript(([tl, fps]) => { window.TIMELINE = tl; window.FPS = fps; }, [TL, FPS]);
  await page.goto(pathToFileURL(path.join(UNIT, 'cena3d', `${TR}.html`)).href);
  await page.waitForFunction(() => window.cenaPronta === true);
  const proj = async f => {
    await page.evaluate(q => window.setFrame(q), f);
    return page.evaluate(() => { const p = window.pontos3d(), r = {}; for (const k in p) r[k] = window.projeta(p[k]); return r; });
  };
  const ref = {}, qa = [];
  for (const [nome, f] of Object.entries(TL.proj)) ref[nome] = { quadro: f, pontos: Object.fromEntries(Object.entries(await proj(f)).map(([k, v]) => [k, paraManim(v)])) };
  for (const [f0, f1, fr] of TL.qa_alinhamento.janelas) {
    const r = await proj(fr); let pior = 0;
    for (let f = f0; f <= f1; f += 3) {
      const p = await proj(f);
      for (const k in r) if (k.startsWith('A_') || f >= fr) pior = Math.max(pior, Math.hypot(p[k][0] - r[k][0], p[k][1] - r[k][1]));
    }
    qa.push({ janela: [f0, f1], referencia: fr, pior_erro_px: +pior.toFixed(3) });
  }
  fs.writeFileSync(path.join(UNIT, `proj_${TR}.json`), JSON.stringify({ ref, qa }, null, 1));
  console.log(JSON.stringify(qa));
  await browser.close();
})();
