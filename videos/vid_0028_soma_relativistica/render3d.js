// Render determinístico do 3D: o Chromium (Playwright) chama window.setFrame(f) e salva um PNG por quadro.
// Uso (dentro da unidade): node render3d.js [--w 540 --h 960 --fps 15] [--out frames3d_540x960] [--quadros 0,45,100]
//   --quadros: só esses quadros (iteração rápida; não grava custo.json).
// GPU: no Windows usa ANGLE/Direct3D 11 (rápido); no Linux/macOS usa SwiftShader (CPU, mais lento, mesmo resultado).
// Chromium: o do Playwright (npx playwright@1.55.0 install chromium) ou o caminho em CHROMIUM_PATH.
const { chromium } = require('playwright-core');
const fs = require('fs'), path = require('path'), { pathToFileURL } = require('url');

const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const W = +arg('w', 540), H = +arg('h', 960), FPS = +arg('fps', 15);
const OUT = path.resolve(__dirname, arg('out', `frames3d_${W}x${H}`));
const TL = JSON.parse(fs.readFileSync(path.join(__dirname, 'timeline.json'), 'utf8'));
const total = Math.round(TL.duracao_s * FPS);
const lista = arg('quadros') ? arg('quadros').split(',').map(Number) : [...Array(total).keys()];
const GPU = process.platform === 'win32'
  ? ['--use-angle=d3d11', '--enable-gpu', '--ignore-gpu-blocklist']
  : ['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist'];

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ args: GPU, executablePath: process.env.CHROMIUM_PATH || undefined });
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  page.on('console', m => console.log('[página]', m.text()));
  page.on('pageerror', e => { console.error(e); process.exit(1); });
  await page.addInitScript(([tl, fps]) => { window.TIMELINE = tl; window.FPS = fps; }, [TL, FPS]);
  await page.goto(pathToFileURL(path.join(__dirname, 'cena3d', 'index.html')).href);
  await page.waitForFunction(() => window.cenaPronta === true);
  const t0 = Date.now();
  for (const [n, f] of lista.entries()) {
    await page.evaluate(q => window.setFrame(q), f);
    await page.screenshot({ path: path.join(OUT, `f${String(f).padStart(5, '0')}.png`) });
    if (n % 300 === 0) console.log(`quadro ${f} (${n + 1}/${lista.length})`);
  }
  const s = (Date.now() - t0) / 1000;
  const info = { resolucao: `${W}x${H}`, fps: FPS, quadros: lista.length, segundos: +s.toFixed(1), s_por_quadro: +(s / lista.length).toFixed(4) };
  console.log(JSON.stringify(info));
  if (!arg('quadros')) fs.writeFileSync(path.join(OUT, 'custo.json'), JSON.stringify(info, null, 2));
  await browser.close();
})();
