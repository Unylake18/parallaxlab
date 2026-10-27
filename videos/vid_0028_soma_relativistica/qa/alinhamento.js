// QA de alinhamento 3D × Manim do vid_0028 (vista lateral, K = 1, centro (0, 0)).
// Para cada quadro de timeline.qa_alinhamento.quadros: projeta pelo 3D (window.projeta) os pontos onde o Manim desenha
// por cima — centro de cada foguete (chips A/B, origem das setas) e base da Terra (rótulo e seta da Terra) — e compara
// com o pixel que o Manim calcula a partir da MESMA trajetória: (x, y) → ((x + 4,5)/9·W, (8 − y)/16·H).
// Uso (dentro da unidade): node qa/alinhamento.js [quadro ...]     Aceitação: pior erro ≤ 2 px no preview 540×960.
const { chromium } = require('playwright-core');
const fs = require('fs'), path = require('path'), { pathToFileURL } = require('url');
const UNIT = path.resolve(__dirname, '..');
const TL = JSON.parse(fs.readFileSync(path.join(UNIT, 'timeline.json'), 'utf8'));
const W = 540, H = 960, FPS = 15, G = TL.geometria, TR = TL.trajetoria;
const quadros = process.argv.length > 2 ? process.argv.slice(2).map(Number) : TL.qa_alinhamento.quadros;
const amostra = (nome, t) => TR[nome][Math.max(0, Math.min(TR[nome].length - 1, Math.round(t / TR.passo_s)))];
const manimPx = (x, y) => [(x + 4.5) / 9 * W, (8 - y) / 16 * H];
const GPU = process.platform === 'win32' ? ['--use-angle=d3d11'] : ['--use-gl=swiftshader', '--enable-webgl'];
(async () => {
  const browser = await chromium.launch({ args: GPU, executablePath: process.env.CHROMIUM_PATH || undefined });
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  await page.addInitScript(([tl, fps]) => { window.TIMELINE = tl; window.FPS = fps; }, [TL, FPS]);
  await page.goto(pathToFileURL(path.join(UNIT, 'cena3d', 'index.html')).href);
  await page.waitForFunction(() => window.cenaPronta === true);
  const saida = [];
  let pior = 0;
  for (const f of quadros) {
    await page.evaluate(q => window.setFrame(q), f);
    const t = f / FPS, pos = await page.evaluate(() => window.posicoes());
    const alvos = { A: [amostra('xA', t), G.y_foguete_A], B: [amostra('xB', t), G.y_foguete_B], E: [amostra('xE', t), G.y_chao] };
    const erros = {};
    for (const k of ['A', 'B', 'E']) {
      const p3 = await page.evaluate(p => window.projeta(p), [pos[k][0], pos[k][1], pos[k][2]]);
      const pm = manimPx(...alvos[k]);
      erros[k] = +Math.hypot(p3[0] - pm[0], p3[1] - pm[1]).toFixed(4);
      pior = Math.max(pior, erros[k]);
    }
    saida.push({ quadro: f, t: +t.toFixed(3), erro_px: erros });
  }
  console.log(JSON.stringify({ quadros: saida, pior_erro_px: +pior.toFixed(4) }, null, 1));
  await browser.close();
})();
