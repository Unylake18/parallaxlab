// Render determinístico do 3D do vid_0033: Playwright (Chromium) chama window.setFrame(f), salva PNGs e as projeções (proj.json).
// Uso: node render3d.js [--w 540 --h 960] [--out frames3d_540x960] [--quadros 0,45,480] [--debug 1]
const { chromium } = require('playwright-core');
const fs = require('fs'), path = require('path'), { pathToFileURL } = require('url');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const W = +arg('w', 540), H = +arg('h', 960);
const DEBUG = !!arg('debug', ''), AUDIT = !!arg('audit', ''), SEMFOTO = !!arg('semfoto', '');
const OUT = path.resolve(__dirname, arg('out', DEBUG ? `qa/debug_${W}x${H}` : `frames3d_${W}x${H}`));
const TL = JSON.parse(fs.readFileSync(path.join(__dirname, 'timeline.json'), 'utf8'));
const lista = arg('quadros') ? arg('quadros').split(',').map(Number) : [...Array(TL.nq).keys()];
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ args: ['--use-angle=d3d11', '--enable-gpu', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  page.on('console', m => console.log('[página]', m.text()));
  page.on('pageerror', e => { console.error(e); process.exit(1); });
  await page.addInitScript(([tl, dbg, aud]) => { window.TIMELINE = tl; window.DEBUG_ALINHA = dbg; window.AUDIT = aud; }, [TL, DEBUG, AUDIT]);
  await page.goto(pathToFileURL(path.join(__dirname, 'cena3d', 'index.html')).href);
  await page.waitForFunction(() => window.cenaPronta === true);
  console.log('GPU:', await page.evaluate(() => { const gl = document.querySelector('canvas').getContext('webgl2') || document.querySelector('canvas').getContext('webgl'); const e = gl.getExtension('WEBGL_debug_renderer_info'); return e ? gl.getParameter(e.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER); }));
  const proj = {}, t0 = Date.now();
  for (const [n, f] of lista.entries()) {
    proj[f] = await page.evaluate(q => { window.setFrame(q); return window.getProj(); }, f);
    if (!SEMFOTO) await page.screenshot({ path: path.join(OUT, `f${String(f).padStart(5, '0')}.png`) });
    if (n % 300 === 0) console.log(`quadro ${f} (${n + 1}/${lista.length})`);
  }
  const s = (Date.now() - t0) / 1000;
  const info = { resolucao: `${W}x${H}`, quadros: lista.length, segundos: +s.toFixed(1), s_por_quadro: +(s / lista.length).toFixed(4) };
  console.log(JSON.stringify(info));
  if (!arg('quadros')) { fs.writeFileSync(path.join(OUT, 'custo.json'), JSON.stringify(info, null, 2)); }
  if (AUDIT) fs.writeFileSync(path.join(__dirname, 'qa', 'proj_auditoria.json'), JSON.stringify(proj));
  else if (!DEBUG) { const pf = arg('quadros') ? path.join(__dirname, 'qa', 'proj_amostra.json') : path.join(__dirname, W === 540 ? 'proj.json' : `proj_${W}x${H}.json`); fs.writeFileSync(pf, JSON.stringify(proj)); }
  else fs.writeFileSync(path.join(OUT, 'proj.json'), JSON.stringify(proj));
  await browser.close();
})();
