// Renderiza a cena 3D quadro a quadro em PNG (1080×1920), sem tempo real.
// Uso: node render3d.js <pasta_saida> [frames separados por vírgula | todos]
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const out = path.resolve(process.argv[2] || 'frames3d');
  const sel = process.argv[3] || 'todos';
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => console.log('PAGEERR', e.message));
  await page.goto('file://' + path.join(__dirname, 'cena3d.html'));
  await page.waitForFunction(() => window.ready === true, null, { timeout: 60000 });
  const total = await page.evaluate(() => window.TOTAL);
  console.log('B no centro (μ0 I/4π):', await page.evaluate(() => window.B_centro.map(x => x.toFixed(2)).join(', ')));
  const frames = sel === 'todos' ? [...Array(total).keys()] : sel.split(',').map(Number);
  const canvas = await page.$('canvas');
  for (const f of frames) {
    await page.evaluate(f => window.setFrame(f), f);
    await canvas.screenshot({ path: path.join(out, `f${String(f).padStart(4, '0')}.png`) });
  }
  console.log(`${frames.length} quadros em ${out}`);
  await browser.close();
})();
