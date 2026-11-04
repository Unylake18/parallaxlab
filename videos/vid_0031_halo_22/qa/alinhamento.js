// QA do vid_0031 v7: alinhamento 3D × Manim (px, 540×960) e contagem de objetos do 3D (a lupa do C02 gira com corpo e não prende nada do Manim: fora da medida).
// 1) Cristal 2.5D: em TODOS os quadros com cristal (inclusive o giro), os 6 vértices da face da frente projetados pela câmera
//    do Three.js × os vértices do roteiro.py (os mesmos que o Manim usa). Conta também os objetos da cena do cristal (constante).
// 2) Céu (C01): o shader pinta de vermelho as direções a 21,84° ± 0,04° do Sol; distância do ponto da seta ao pixel vermelho.
// Uso: node qa/alinhamento.js  → qa/alinhamento.json
const { chromium } = require('playwright-core');
const fs = require('fs'), path = require('path'), { pathToFileURL } = require('url');
const UNIT = path.resolve(__dirname, '..'), W = 540, H = 960, FPS = 15;
const TL = JSON.parse(fs.readFileSync(path.join(UNIT, 'timeline.json'), 'utf8'));
const px = ([x, y]) => [(x / 9 + 0.5) * W, (0.5 - y / 16) * H];

(async () => {
  const browser = await chromium.launch({ args: ['--use-angle=d3d11', '--enable-gpu', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  await page.addInitScript(([tl, fps]) => { window.TIMELINE = tl; window.FPS = fps; }, [TL, FPS]);
  await page.goto(pathToFileURL(path.join(UNIT, 'cena3d', 'index.html')).href);
  await page.waitForFunction(() => window.cenaPronta === true);
  const out = {};

  // 1) cristal 2.5D, todos os quadros
  const CR = TL.cristal, quadros = [];
  CR.quadros.forEach((st, q) => { if (st && st.a > 0.002 && st.caso !== 'lupa') quadros.push(CR.quadro_inicial + q); });
  const res = await page.evaluate(fs_ => fs_.map(f => { window.setFrame(f); return [f, window.verticesFrente(), window.objetosCristal()]; }), quadros);
  let pior = { erro: 0 }, objetos = new Set();
  for (const [f, proj, nobj] of res) {
    objetos.add(nobj);
    const esperado = CR.quadros[f - CR.quadro_inicial].v.map(px);
    const e = Math.max(...esperado.map(p => Math.min(...proj.map(q => Math.hypot(p[0] - q[0], p[1] - q[1])))));
    if (e > pior.erro) pior = { erro: e, quadro: f, t: +(f / FPS).toFixed(3) };
  }
  const giro = res.filter(([f]) => f / FPS >= TL.eventos.giro_ini && f / FPS <= TL.eventos.giro_fim).length;
  out.cristal = { quadros: res.length, quadros_no_giro: giro, erro_max_px: +pior.erro.toFixed(3), pior_quadro: pior,
                  objetos_na_cena_do_cristal: [...objetos] };

  // 2) céu
  const g = 2;                                                     // v5: C01 antes do push-in (escala 1 da vista do céu)
  const sol = px(TL.ceu.sol_manim), borda = px(TL.ceu.borda_manim);
  const ceu = await page.evaluate(([g, sol, borda, W, H]) => {
    window.debugBorda(true); window.setFrame(g); window.debugBorda(false);
    const gl = document.querySelector('canvas').getContext('webgl2') || document.querySelector('canvas').getContext('webgl');
    const buf = new Uint8Array(W * H * 4);
    gl.readPixels(0, 0, W, H, gl.RGBA, gl.UNSIGNED_BYTE, buf);
    const vermelho = (x, y) => { const i = 4 * ((H - 1 - y) * W + x); return buf[i] > 240 && buf[i + 1] < 20 && buf[i + 2] < 20; };
    let melhor = 1e9, n = 0;
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (vermelho(x, y)) {
      n++; melhor = Math.min(melhor, Math.hypot(x + 0.5 - borda[0], y + 0.5 - borda[1]));
    }
    const u = [borda[0] - sol[0], borda[1] - sol[1]], L = Math.hypot(...u), hits = [];
    for (let s = 0; s < 2 * L; s += 0.25) {
      const x = Math.round(sol[0] + u[0] / L * s - 0.5), y = Math.round(sol[1] + u[1] / L * s - 0.5);
      if (x >= 0 && x < W && y >= 0 && y < H && vermelho(x, y)) hits.push(s);
    }
    const centro = hits.length ? (Math.min(...hits) + Math.max(...hits)) / 2 : null;
    return { pixels_vermelhos: n, dist_ponto_seta_ao_vermelho_px: melhor, raio_seta_px: L, raio_vermelho_px: centro };
  }, [g, sol, borda, W, H]);
  ceu.erro_raio_px = ceu.raio_vermelho_px === null ? null : +(ceu.raio_vermelho_px - ceu.raio_seta_px).toFixed(3);
  out.ceu = { quadro: g, ...ceu };
  fs.writeFileSync(path.join(UNIT, 'qa', 'alinhamento.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify(out, null, 2));
  await browser.close();
})();
