// Âncoras 3D → 2D por quadro: roda window.setFrame(f) (sem screenshot), projeta os pontos nomeados de window.ancoras()
// e grava ancoras.json em coordenadas do Manim (quadro 9 × 16, y de −8 a 8) + os números do quadro (window.valores()).
// O Manim (cena.py) e o Remotion leem este arquivo para pôr rótulos, réguas e contadores em cima do 3D.
// Uso (dentro da unidade): node ancoras.js [--fps 15]   → ancoras_15fps.json
// As coordenadas são normalizadas (independem da resolução, só da proporção 9 × 16).
const { chromium } = require('playwright-core');
const fs = require('fs'), path = require('path'), { pathToFileURL } = require('url');

const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const FPS = +arg('fps', 15), W = 540, H = 960;
const TL = JSON.parse(fs.readFileSync(path.join(__dirname, 'timeline.json'), 'utf8'));
const total = Math.round(TL.duracao_s * FPS);
const GPU = process.platform === 'win32' ? ['--use-angle=d3d11'] : ['--use-gl=swiftshader', '--enable-webgl'];

(async () => {
  const browser = await chromium.launch({ args: GPU, executablePath: process.env.CHROMIUM_PATH || undefined });
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  page.on('pageerror', e => { console.error(e); process.exit(1); });
  await page.addInitScript(([tl, fps]) => { window.TIMELINE = tl; window.FPS = fps; }, [TL, FPS]);
  await page.goto(pathToFileURL(path.join(__dirname, 'cena3d', 'index.html')).href);
  await page.waitForFunction(() => window.cenaPronta === true);
  const t0 = Date.now();
  const res = await page.evaluate(([n, W, H]) => {
    const r = (x, k = 4) => +x.toFixed(k);
    let nomes = null, vnomes = null; const quadros = [], valores = [], caixas = [];
    for (let f = 0; f < n; f++) {
      window.setFrame(f);
      const A = window.ancoras(), V = window.valores(), CX = window.caixas();
      if (!nomes) { nomes = Object.keys(A); vnomes = Object.keys(V); }
      quadros.push(nomes.map(k => { const [px, py] = window.projeta(A[k]); return [r(px / W * 9 - 4.5), r(8 - py / H * 16)]; }));
      valores.push(vnomes.map(k => r(V[k], 5)));
      // caixas de silhueta em px do 540×960 [x0, y0, x1, y1] (y para baixo); só as visíveis no quadro
      caixas.push(Object.fromEntries(Object.entries(CX).map(([k, b]) => [k, b.map(x => r(x, 1))])));
    }
    return { nomes, vnomes, quadros, valores, caixas };
  }, [total, W, H]);
  const out = path.join(__dirname, `ancoras_${FPS}fps.json`);
  fs.writeFileSync(out, JSON.stringify({ _leia_me: 'gerado por ancoras.js; não editar', fps: FPS, quadros_total: total,
    nomes: res.nomes, valores_nomes: res.vnomes, quadros: res.quadros, valores: res.valores, caixas: res.caixas }));
  console.log(JSON.stringify({ arquivo: path.basename(out), quadros: total, nomes: res.nomes.length, segundos: (Date.now() - t0) / 1000 }));
  await browser.close();
})();
