// QA de alinhamento 3D × Manim/Remotion do vid_0030 (aceitação: pior erro ≤ 2 px no preview 540×960).
//  1) Vista 'frente' (corte vertical, C02): pelo dolly-zoom, o ponto 3D (x, 0, z) tem de cair no Manim em
//     (K·x, yc + K·z), K = 16/alt. Testa n pontos do perfil do anel (círculo de raio R e parede do furo).
//  2) Âncoras: o ancoras_<fps>fps.json (lido pelo Manim e pelo Remotion) tem de bater com window.projeta ao vivo em
//     quadros de vários beats, inclusive em 1080×1920.
//  3) Réguas de h (v2): em ≥ 20 quadros de C01, C06 e C07, altura em px da haste desenhada (âncoras salvas n_cima/n_baixo,
//     exatamente o que o Remotion desenha) × altura projetada da aresta do anel (pontos 3D −a·u, ±h/2 da borda do furo,
//     conferidos contra a geometria: raio = a do quadro e z = zc ± h/2). Também o rótulo "h = 6 cm" do C06 ≥ 16 px da borda.
//  4) Pontas das linhas auxiliares (C02–C04): ponta real do tubo desenhado (matriz do mesh) × âncora usada pelos rótulos.
// Uso (dentro da unidade): node qa/alinhamento.js   → imprime JSON e grava qa/alinhamento_v5.json
const { chromium } = require('playwright-core');
const fs = require('fs'), path = require('path'), { pathToFileURL } = require('url');
const UNIT = path.resolve(__dirname, '..');
const TL = JSON.parse(fs.readFileSync(path.join(UNIT, 'timeline.json'), 'utf8'));
const FPS = 15, G = TL.geometria, V = TL.vistas.frente, K = 16 / V.alt, E = TL.eventos;
const ANC = JSON.parse(fs.readFileSync(path.join(UNIT, `ancoras_${FPS}fps.json`), 'utf8'));
const GPU = process.platform === 'win32' ? ['--use-angle=d3d11'] : ['--use-gl=swiftshader', '--enable-webgl'];
const fr = t => Math.round(t * FPS);
const QUADROS = [fr(3), fr(42), fr(60), fr(75), fr(95), fr(105), fr(125), fr(150), fr(160), fr(174)];
const REGUAS = [
  ...[32.4, 33.0, 33.6, 34.2, 34.8].map(t => ['C01', fr(t), ['regua0', 'regua1', 'regua2']]),
  ...[144.4, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155].map(t => ['C06', fr(t), ['regua_anel']]),
  ...[168.2, 168.8, 169.4, 170.0, 170.6].map(t => ['C07', fr(t), ['regua0', 'regua1', 'regua2']]),
];
// tubo → [âncora da ponta inicial | null, âncora da ponta final]
const PONTAS = {
  triR: ['O', 'P'], triA: ['O', 'Q'], triH: ['Q', 'P'],
  fatZ: ['O', 'fat_zc'], fatExt: ['fat_zc', 'fat_ext'], fatInt: ['fat_zc', 'fat_int'], fatR: ['O', 'fat_ext'],
  cavZ: ['esf_centro', 'cav_zc'], cavRho: ['cav_zc', 'esf_ext'], cavHip: ['esf_centro', 'esf_ext'],
};
const Q_PONTAS = [fr(42), fr(46), fr(61), fr(70), fr(78), fr(93), fr(95), fr(97)];

async function abre(browser, W, H) {
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  await page.addInitScript(([tl, fps]) => { window.TIMELINE = tl; window.FPS = fps; }, [TL, FPS]);
  await page.goto(pathToFileURL(path.join(UNIT, 'cena3d', 'index.html')).href);
  await page.waitForFunction(() => window.cenaPronta === true);
  return page;
}

async function mede(browser, W, H) {
  const page = await abre(browser, W, H);
  const px = ([x, y]) => [(x + 4.5) / 9 * W, (8 - y) / 16 * H];
  await page.evaluate(q => window.setFrame(q), TL.qa_alinhamento.quadro);
  let piorFrente = 0;
  const pts = [];
  for (let k = 0; k <= 12; k++) { const z = -G.h / 2 + G.h * k / 12; pts.push([Math.sqrt(G.R * G.R - z * z), 0, z], [-G.a, 0, z]); }
  for (const p of pts) {
    const [a, b] = await page.evaluate(q => window.projeta(q), p);
    const [mx, my] = px([K * p[0], V.yc + K * p[2]]);
    piorFrente = Math.max(piorFrente, Math.hypot(a - mx, b - my));
  }
  let piorAnc = 0;
  for (const f of QUADROS) {
    await page.evaluate(q => window.setFrame(q), f);
    const vivos = await page.evaluate(() => { const A = window.ancoras(); const o = {}; for (const k in A) o[k] = window.projeta(A[k]); return o; });
    ANC.nomes.forEach((n, i) => {
      const [a, b] = px(ANC.quadros[f][i]), [c, d] = vivos[n];
      piorAnc = Math.max(piorAnc, Math.hypot(a - c, b - d));
    });
  }
  await page.close();
  return { resolucao: `${W}x${H}`, frente_pior_px: +piorFrente.toFixed(4), ancoras_pior_px: +piorAnc.toFixed(4) };
}

async function reguas(browser, W, H) {
  const page = await abre(browser, W, H);
  const px = ([x, y]) => [(x + 4.5) / 9 * W, (8 - y) / 16 * H];
  const ix = n => ANC.nomes.indexOf(n), linhas = [];
  for (const [beat, f, nomes] of REGUAS) {
    await page.evaluate(q => window.setFrame(q), f);
    const vivo = await page.evaluate(() => ({ A: window.ancoras(), V: window.valores() }));
    for (const n of nomes) {
      const zc = n === 'regua_anel' ? 0 : G.trio[+n.slice(-1)].zc;
      const a = n === 'regua_anel' ? vivo.V.a_furo : Math.sqrt(G.trio[+n.slice(-1)].R ** 2 - G.h ** 2 / 4);
      const ec = vivo.A[`${n}_aresta_cima`], eb = vivo.A[`${n}_aresta_baixo`];
      // a aresta tem de estar na borda do furo: raio a, z = zc ± h/2
      const geo = Math.max(Math.abs(Math.hypot(ec[0], ec[1]) - a), Math.abs(Math.hypot(eb[0], eb[1]) - a),
        Math.abs(ec[2] - zc - G.h / 2), Math.abs(eb[2] - zc + G.h / 2));
      const [pc, pb] = await page.evaluate(([p, q]) => [window.projeta(p), window.projeta(q)], [ec, eb]);
      const hAresta = Math.hypot(pc[0] - pb[0], pc[1] - pb[1]);
      const [ax, ay] = px(ANC.quadros[f][ix(`${n}_cima`)]), [bx, by] = px(ANC.quadros[f][ix(`${n}_baixo`)]);
      const hHaste = Math.hypot(ax - bx, ay - by);
      const ln = { beat, quadro: f, t: +(f / FPS).toFixed(2), regua: n, R: +vivo.V.R.toFixed(2), haste_px: +hHaste.toFixed(2),
        aresta_px: +hAresta.toFixed(2), erro_px: +Math.abs(hHaste - hAresta).toFixed(3), aresta_fora_da_borda_cm: +geo.toExponential(1) };
      // v3: margem e folga do rótulo vêm das caixas reais do Remotion (qa/sobreposicao.py)
      linhas.push(ln);
    }
  }
  await page.close();
  return linhas;
}

async function pontas(browser, W, H) {
  const page = await abre(browser, W, H);
  const px = ([x, y]) => [(x + 4.5) / 9 * W, (8 - y) / 16 * H];
  const ix = n => ANC.nomes.indexOf(n), linhas = [];
  for (const f of Q_PONTAS) {
    await page.evaluate(q => window.setFrame(q), f);
    const P = await page.evaluate(() => { const o = window.pontas(), r = {}; for (const k in o) r[k] = o[k].map(window.projeta); return r; });
    for (const [tubo, [ini, fim]] of Object.entries(PONTAS)) {
      if (!P[tubo]) continue;
      const e0 = Math.hypot(...px(ANC.quadros[f][ix(ini)]).map((v, k) => v - P[tubo][0][k]));
      const e1 = Math.hypot(...px(ANC.quadros[f][ix(fim)]).map((v, k) => v - P[tubo][1][k]));
      linhas.push({ quadro: f, t: +(f / FPS).toFixed(2), tubo, ini, fim, erro_ini_px: +e0.toFixed(3), erro_fim_px: +e1.toFixed(3) });
    }
  }
  await page.close();
  return linhas;
}

(async () => {
  const browser = await chromium.launch({ args: GPU, executablePath: process.env.CHROMIUM_PATH || undefined });
  const geral = [];
  for (const [W, H] of [[540, 960], [1080, 1920]]) geral.push(await mede(browser, W, H));
  const rg = await reguas(browser, 540, 960), pt = await pontas(browser, 540, 960);
  await browser.close();
  const res = { geral, reguas: { quadros: new Set(rg.map(l => l.quadro)).size, medidas: rg.length,
      pior_erro_px: Math.max(...rg.map(l => l.erro_px)), pior_aresta_fora_cm: Math.max(...rg.map(l => l.aresta_fora_da_borda_cm)) },
    pontas: { medidas: pt.length, pior_erro_px: Math.max(...pt.map(l => Math.max(l.erro_ini_px, l.erro_fim_px))) },
    tabela_reguas: rg, tabela_pontas: pt };
  fs.writeFileSync(path.join(__dirname, 'alinhamento_v5.json'), JSON.stringify(res, null, 1));
  console.log(JSON.stringify({ geral, reguas: res.reguas, pontas: res.pontas }, null, 1));
})();
