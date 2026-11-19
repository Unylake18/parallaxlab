// yt_0032 · cenas 3D (porte de referencia/c3d32.html, three.js r128; motor copiado do c31.js do yt_0031). Uma página por cena
// (b12.html, b14.html, b21.html, b22.html, b31.html, b32.html, b61.html) define window.CENA_ID.
// Estilo do c3d32: opaco e sem luz (MeshBasicMaterial), tom por face (topo = cor; faces x 70 %; faces y 48 % sobre o fundo), contorno escuro fino
// até n = 16 e sem contorno de n = 32 em diante, sem sombra/névoa/brilho/transparência, outputEncoding linear, fundo transparente (o Manim põe o
// violeta liso por baixo). Mundo: x e y em metros (chapa [0,2]²), z desenhado = ZS · valor. Câmera perspectiva fov 22°, up = +z.
// A CÂMERA VEM DO MANIM no estado ({pos, tgt, up, cx, cy}); setEstado(e) refaz a cena e devolve os pontos de proj() em px de 1920×1080.
// Os estados intermediários (cresceA, pousoB, k, c1, c2, cresceF, cresceG, folga, cresce, lajes, cob, muro, alt, n, nivel, acende, nivela, arco)
// são desta unidade; em 1 (e nos n/alt do alvo) cada cena reproduz o c3d32.html.
const T = THREE, PI = Math.PI, K = window.CENA_ID;
const W = window.innerWidth, H = window.innerHeight, ESC = W / 1920;
const R = new T.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
R.setPixelRatio(1); R.setSize(W, H, false); R.setClearColor(0x000000, 0); R.outputEncoding = T.LinearEncoding;
document.body.appendChild(R.domElement);
const S = new T.Scene(); T.Object3D.DefaultUp.set(0, 0, 1);
const cam = new T.PerspectiveCamera(22, W / H, .05, 200);
const BG = '#131030', CI = '#35D9FF', AZC = '#7FB2FF', CORAL = '#FF7A8A', POS = '#E08A3C', E1 = '#FFC24D', E2 = '#EA63FF', GEO = '#B8C4DA',
  LEVE = '#1E5072', PESADO = '#30BBE0', BR = '#F5F7FF', LIL = '#C9A7FF', MEN = '#8CFFD2';
const C = h => new T.Color(h), mixc = (a, b, t) => C(a).lerp(C(b), t);
let ZS = .25, G = null, PTS = {};
const f = (x, y) => x * x + y * y;
const g = a => 1 + .42 * Math.sin(1.7 * a - .4);
const sm = u => { u = Math.min(1, Math.max(0, u)); return u * u * (3 - 2 * u); };
const cl = u => Math.min(1, Math.max(0, u));

function aplicaCam(c) {
  cam.up.set(...c.up); cam.position.set(...c.pos); cam.lookAt(...c.tgt);
  cam.setViewOffset(W, H, (960 - c.cx) * ESC, (540 - c.cy) * ESC, W, H);
  cam.updateProjectionMatrix(); cam.updateMatrixWorld(true);
}
function proj(nome, v) { const q = new T.Vector3(...v).project(cam); PTS[nome] = [+((q.x + 1) / 2 * 1920).toFixed(2), +((1 - q.y) / 2 * 1080).toFixed(2)]; }
function add(o) { G.add(o); return o; }
function caixas(lista, { bordas = true, corBorda = null } = {}) {
  const pos = [], col = [], ed = [];
  const quad = (a, b, c, d, cc) => { for (const p of [a, b, c, a, c, d]) { pos.push(...p); col.push(cc.r, cc.g, cc.b); } };
  for (const b of lista) {
    const { x0, x1, y0, y1, z0, z1 } = b, c = C(b.c), cx = mixc(BG, b.c, .70), cy = mixc(BG, b.c, .48);
    if (z1 - z0 < 1e-5) continue;
    quad([x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1], c);
    quad([x1, y0, z0], [x1, y1, z0], [x1, y1, z1], [x1, y0, z1], cx); quad([x0, y1, z0], [x0, y0, z0], [x0, y0, z1], [x0, y1, z1], cx);
    quad([x0, y0, z0], [x1, y0, z0], [x1, y0, z1], [x0, y0, z1], cy); quad([x1, y1, z0], [x0, y1, z0], [x0, y1, z1], [x1, y1, z1], cy);
    if (bordas) { const v = [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]; for (let k = 0; k < 4; k++) { const a = v[k], n = v[(k + 1) % 4]; ed.push(a[0], a[1], z1, n[0], n[1], z1, a[0], a[1], z0, a[0], a[1], z1); } }
  }
  if (!pos.length) return null;
  const gg = new T.BufferGeometry(); gg.setAttribute('position', new T.Float32BufferAttribute(pos, 3)); gg.setAttribute('color', new T.Float32BufferAttribute(col, 3));
  const m = add(new T.Mesh(gg, new T.MeshBasicMaterial({ vertexColors: true, side: T.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 })));
  if (bordas && ed.length) {
    const ge = new T.BufferGeometry(); ge.setAttribute('position', new T.Float32BufferAttribute(ed, 3));
    add(new T.LineSegments(ge, new T.LineBasicMaterial({ color: corBorda ? C(corBorda) : mixc(BG, '#0B1530', .6) })));
  }
  return m;
}
function poli(pts) { const cp = new T.CurvePath(); for (let i = 0; i + 1 < pts.length; i++) cp.add(new T.LineCurve3(new T.Vector3(...pts[i]), new T.Vector3(...pts[i + 1]))); return cp; }
const tubo = (pts, r, cor) => add(new T.Mesh(new T.TubeGeometry(poli(pts), Math.max(8, (pts.length - 1) * 4), r, 8, false), new T.MeshBasicMaterial({ color: C(cor) })));
function seta(a, b, r, cor) {
  const A = new T.Vector3(...a), B = new T.Vector3(...b), d = B.clone().sub(A), L = d.length(), hl = Math.min(.16, .3 * L), gr = new T.Group(), m = new T.MeshBasicMaterial({ color: C(cor) });
  const s = new T.Mesh(new T.CylinderGeometry(r, r, L - hl, 12), m); s.position.y = (L - hl) / 2; const c = new T.Mesh(new T.ConeGeometry(r * 3, hl, 18), m); c.position.y = L - hl / 2; gr.add(s, c);
  gr.position.copy(A); gr.quaternion.setFromUnitVectors(new T.Vector3(0, 1, 0), d.normalize()); add(gr); return gr;
}
// arestas (o que precisa "aparecer através": nunca transparência)
function arame(lista, cor, r = .006) {
  for (const b of lista) {
    const { x0, x1, y0, y1, z0, z1 } = b; if (z1 - z0 < 1e-4) continue;
    tubo([[x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1], [x0, y0, z1]], r, cor);
    for (const [a, c] of [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]) tubo([[a, c, z0], [a, c, z1]], r * .8, cor);
  }
}
function base(cor = GEO, { x1 = 2, y1 = 2, fill = '#1C1846' } = {}) {
  const p = add(new T.Mesh(new T.PlaneGeometry(x1, y1), new T.MeshBasicMaterial({ color: C(fill) }))); p.position.set(x1 / 2, y1 / 2, -.002);
  tubo([[0, 0, 0], [x1, 0, 0], [x1, y1, 0], [0, y1, 0], [0, 0, 0]].map(q => [q[0], q[1], .001]), .006, cor);
}
// eixos do c3d32: eixos() (b12, b21, b61; ly = 3,3, marcas 2–8) e eixos2() (b14, b22, b31/b32; ly = 2,45)
function eixos(ly, lz, marcas) {
  seta([0, 0, .014], [2.45, 0, .014], .011, E1); seta([0, 0, .014], [0, ly, .014], .011, E2); seta([0, 0, 0], [0, 0, lz], .011, CI);
  proj('ex', [2.57, 0, 0]); proj('ey', [0, ly + .12, 0]); proj('ez', [0, 0, lz + .12]);
  for (const v of marcas) { tubo([[-.05, 0, v * ZS], [.05, 0, v * ZS]], .008, CI); proj('m' + v, [-.13, -.02, v * ZS]); }
}
function faixa(a, b, am = 400) { let mn = 9, mx = -9; for (let s = 0; s <= am; s++) { const v = g(a + (b - a) * s / am); mn = Math.min(mn, v); mx = Math.max(mx, v); } return [mn, mx]; }
const soldaTubo = (z, cor = BR, r = .012) => { const c = []; for (let s = 0; s <= 80; s++) { const a = 2 * s / 80; c.push([a, g(a), z]); } tubo(c, r, cor); };
const ESCALA_K = 1;

window.setEstado = e => {
  if (G) { S.remove(G); G.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.material) { if (o.material.map) o.material.map.dispose(); o.material.dispose(); } }); }
  G = new T.Group(); S.add(G); PTS = {};
  aplicaCam(e.cam);

  // b12: rampas empilhadas: x² (âmbar) embaixo cresce do chão (cresceA); y² (magenta) desce e pousa em cima (pousoB); n = 4
  if (K === 'b12') {
    ZS = .25; const n = 4, h = 2 / n, A = [], B = [], cA = e.cresceA ?? 1, pB = e.pousoB ?? 1; base(); eixos(3.3, 2.25, [2, 4, 6, 8]);
    for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
      const xc = (i + .5) * h, yc = (j + .5) * h, k = i * n + j;
      if (cA > 0) A.push({ x0: i * h, x1: (i + 1) * h, y0: j * h, y1: (j + 1) * h, z0: 0, z1: Math.max(.0015, ZS * xc * xc * cA), c: E1 });
      const u = sm(pB * 1.6 - k * .6 / 15), alto = 3.2 * (1 - u);          // cada caixa desce de 3,2 m acima, em cascata; pousa em u = 1
      if (pB > 0 && u > 0) B.push({ x0: i * h, x1: (i + 1) * h, y0: j * h, y1: (j + 1) * h, z0: ZS * xc * xc + alto, z1: ZS * (xc * xc + yc * yc) + alto, c: E2 });
    }
    caixas(A, { corBorda: '#3A2A08' }); if (B.length) caixas(B, { corBorda: '#3A0A40' });
    proj('xq', [1.75, 0, ZS * 1.75 * 1.75 * .5 * cA]); proj('yq', [1.75, .25, ZS * (1.75 * 1.75 + .25 * .25) + .02]); proj('topo', [1.75, 1.75, ZS * (2 * 1.75 * 1.75)]);
  }

  // b14: fase k (16 caixas de x² + y² com altura × k) e fase camadas (1 kg/m² na chapa toda + reforço de 2 kg/m² no pedaço de cima, n = 32)
  if (K === 'b14') {
    const ly = e.ly ?? 3.3, lz = e.lz ?? 2.25;
    if ((e.modo ?? 'k') === 'k') {
      ZS = .25; base(); eixos(ly, lz, [2, 4, 6, 8]);
      const n = 4, h = 2 / n, L = [], k = e.k ?? 1;
      for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) { const xc = (i + .5) * h, yc = (j + .5) * h; L.push({ x0: i * h, x1: (i + 1) * h, y0: j * h, y1: (j + 1) * h, z0: 0, z1: Math.max(.0015, ZS * f(xc, yc) * k), c: CI }); }
      if (k > .002) caixas(L, { corBorda: '#08303A' });
      proj('topo', [1.75, 1.75, ZS * 2 * 1.75 * 1.75 * k]);
    } else {
      ZS = .4; base(); eixos(ly, lz, [1, 3]);
      const n = 32, h = 2 / n, L = [], Rf = [], c1 = e.c1 ?? 1, c2 = e.c2 ?? 1;
      for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
        const a = i * h, c = j * h;
        if (c1 > 0) L.push({ x0: a, x1: a + h, y0: c, y1: c + h, z0: 0, z1: Math.max(.0015, ZS * c1), c: LEVE });
        if (c2 > 0 && c + h / 2 > g(a + h / 2)) Rf.push({ x0: a, x1: a + h, y0: c, y1: c + h, z0: ZS, z1: ZS + 2 * ZS * c2, c: PESADO });
      }
      caixas(L, { bordas: false }); caixas(Rf, { bordas: false }); if (c1 > .999) soldaTubo(ZS + .004);
      proj('camada', [1.9, .15, ZS * .5]); proj('reforco', [.25, 1.85, ZS * 2.2]);
    }
  }

  // b21: f = x² + y² (ciano, sólido, cresceF) e g = f + 1 + x/2 (lilás, só arestas, cresceG); folga de uma caixa acende em lilás (folga)
  if (K === 'b21') {
    ZS = .25; const n = 4, h = 2 / n, F = [], Gg = [], Fo = [], cF = e.cresceF ?? 1, cG = e.cresceG ?? 1, fo = e.folga ?? 0; base(); eixos(3.3, 2.25, [2, 4, 6, 8]);
    for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
      const xc = (i + .5) * h, yc = (j + .5) * h, v = xc * xc + yc * yc, w = v + 1 + xc / 2, b = { x0: i * h, x1: (i + 1) * h, y0: j * h, y1: (j + 1) * h };
      if (cF > 0) F.push({ ...b, z0: 0, z1: Math.max(.0015, ZS * v * cF), c: CI });
      if (cG > 0) Gg.push({ ...b, z0: ZS * v, z1: ZS * (v + (w - v) * cG) });
      if (fo > 0 && i === 2 && j === 0) Fo.push({ ...b, z0: ZS * v, z1: ZS * (v + (w - v) * fo), c: LIL });
    }
    if (F.length) caixas(F, { corBorda: '#08303A' }); if (Fo.length) caixas(Fo, { corBorda: '#2A1A48' }); if (Gg.length) arame(Gg, LIL, .006);
    proj('f', [1.75, 0, ZS * 1.75 * 1.75 * .6 * cF]); proj('g', [1.75, .25, ZS * (1.75 * 1.75 + .0625 + 1 + .875) + .03]); proj('folga', [1.5, 0, ZS * (1.5625 + .0625 + .6)]);
    proj('folgaC', [1.25, .25, ZS * (1.5625 + .0625 + .8125)]);
  }

  // b22: chapa de dois metais (n = 16, cresce) entre duas lajes planas: altura 1 (azul-claro) e 3 (coral), só o contorno (lajes)
  if (K === 'b22') {
    ZS = .5; const n = 16, h = 2 / n, L = [], cr = e.cresce ?? 1, lj = e.lajes ?? 1; base(); eixos(2.45, 1.95, [1, 3]);
    for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) { const a = i * h, c = j * h, cel = (c + h / 2 > g(a + h / 2)) ? 3 : 1; L.push({ x0: a, x1: a + h, y0: c, y1: c + h, z0: 0, z1: Math.max(.0015, ZS * cel * cr), c: cel === 1 ? LEVE : PESADO }); }
    caixas(L, { corBorda: '#08142A' });
    if (lj > 0) for (const [z, cor] of [[1, AZC], [3, CORAL]]) {
      const zz = ZS * z * sm(lj);                    // a laje sobe do chão até a altura dela (arestas verticais crescem junto)
      tubo([[0, 0, zz], [2, 0, zz], [2, 2, zz], [0, 2, zz], [0, 0, zz]], .012, cor);
      if (zz > .01) for (const [a, c] of [[0, 0], [2, 0], [2, 2], [0, 2]]) tubo([[a, c, 0], [a, c, zz]], .005, cor);
    }
    proj('l1', [2, 0, ZS * 1]); proj('l3', [2, 0, ZS * 3]);
  }

  // b31/b32: a solda sozinha: chão dos dois metais, solda branca, cobertura menta (tampas baixas, cob), muro coral (muro) de altura alt nas células
  // que a solda cruza (n). b31 = n 16, alt = M = 3·ZS; b32 = n 64 → 1024, alt = 2,0 (100 com escala vertical reduzida).
  if (K === 'b31' || K === 'b32') {
    ZS = .5; const n = e.n || 16, h = 2 / n, Ch = [], Mu = [], Cb = [], alt = e.alt ?? 1.5, mu = e.muro ?? 1, cob = e.cob ?? 0, lz = e.lz ?? 1.95;
    tubo([[0, 0, .001], [2, 0, .001], [2, 2, .001], [0, 2, .001], [0, 0, .001]], .006, GEO);   // sem o plano de base: o chão de metais cobre a chapa (evita z-fighting a 540p)
    const m = 64, hm = 2 / m; for (let i = 0; i < m; i++) for (let j = 0; j < m; j++) { const a = i * hm, c = j * hm; Ch.push({ x0: a, x1: a + hm, y0: c, y1: c + hm, z0: 0, z1: .004, c: (c + hm / 2 > g(a + hm / 2)) ? PESADO : LEVE }); }
    caixas(Ch, { bordas: false }); soldaTubo(.007, BR, .008);
    for (let i = 0; i < n; i++) { const a = i * h, [mn, mx] = faixa(a, a + h); for (let j = 0; j < n; j++) { const c = j * h, d = c + h;
      if (c <= mx && d > mn) { if (mu > .002) Mu.push({ x0: a, x1: a + h, y0: c, y1: d, z0: 0, z1: alt * mu, c: CORAL }); else if (cob > 0) Cb.push({ x0: a, x1: a + h, y0: c, y1: d, z0: 0, z1: .012 + .02 * cob, c: MEN }); } } }
    if (Cb.length) caixas(Cb, { bordas: n <= 16, corBorda: '#1A4A3A' }); if (Mu.length) caixas(Mu, { bordas: n <= 16, corBorda: '#3A1220' });
    seta([0, 0, .014], [2.45, 0, .014], .011, E1); seta([0, 0, .014], [0, 2.45, .014], .011, E2); seta([0, 0, 0], [0, 0, lz], .011, CI);
    proj('ex', [2.57, 0, 0]); proj('ey', [0, 2.57, 0]); proj('ez', [0, 0, lz + .12]);
    if ((e.marca ?? 1) > 0) tubo([[-.05, 0, alt], [.05, 0, alt]], .008, CI);
    proj('M', [-.13, -.02, alt]); proj('muro', [1.159, g(1.159), alt + .04]); proj('leve', [1.75, .3, 0]); proj('pesado', [.3, 1.8, 0]);
  }

  // b61: terraplanagem de x² + y² até o nível 8/3 (n = 16): prédio ciano (cresce); contorno do nível (nivel); acima do nível acende em coral (acende);
  // nivela: o coral desce até o nível e os buracos se enchem de menta no mesmo movimento (volume conservado); arco laranja onde f = 8/3 (arco)
  if (K === 'b61') {
    ZS = .25; const n = 16, h = 2 / n, Lw = [], Up = [], Dn = [], Lv = 8 / 3, cr = e.cresce ?? 1, nv = e.nivel ?? 1, ac = e.acende ?? 1, nl = e.nivela ?? 0, ar = e.arco ?? 0;
    base(); eixos(3.3, 2.25, [2, 4, 6, 8]);
    const corBaixo = mixc(CI, mixc(BG, CI, .55).getStyle(), ac).getStyle(), corCima = mixc(CI, CORAL, ac).getStyle();
    for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
      const xc = (i + .5) * h, yc = (j + .5) * h, v = xc * xc + yc * yc, b = { x0: i * h, x1: (i + 1) * h, y0: j * h, y1: (j + 1) * h };
      if (v > Lv) { Lw.push({ ...b, z0: 0, z1: Math.max(.0015, ZS * Math.min(v * cr, Lv)), c: corBaixo }); const top = Lv + (v - Lv) * (1 - nl); if (cr * v > Lv && top > Lv + 1e-4) Up.push({ ...b, z0: ZS * Lv, z1: ZS * Math.min(top, cr * v), c: corCima }); }
      else { Lw.push({ ...b, z0: 0, z1: Math.max(.0015, ZS * v * cr), c: corBaixo }); if (nl > 0) Dn.push({ ...b, z0: ZS * v, z1: ZS * (v + (Lv - v) * nl), c: MEN }); }
    }
    caixas(Lw, { bordas: ac < .5, corBorda: '#08303A' }); if (Dn.length) caixas(Dn, { bordas: true, corBorda: '#1A4A3A' }); if (Up.length) caixas(Up, { bordas: true, corBorda: ac < .5 ? '#08303A' : '#3A1220' });
    if (nv > 0) { const z = ZS * Lv, q = sm(nv) * 8, P = [[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]], pts = [[0, 0, z]];
      for (let k = 0; k < 4; k++) { const u = cl(q / 2 - k); if (u <= 0) break; const a = P[k], b = P[k + 1]; pts.push([a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, z]); }
      if (pts.length > 1) tubo(pts, .011, CI); }
    if (ar > 0) { const r = Math.sqrt(Lv), arc = [], N = Math.max(2, Math.round(90 * cl(ar))); for (let k = 0; k <= N; k++) { const t = PI / 2 * cl(ar) * k / N; arc.push([r * Math.cos(t), r * Math.sin(t), ZS * Lv + .006]); } tubo(arc, .014, POS); }
    proj('acima', [1.94, 1.94, ZS * 7.6]); proj('abaixo', [.3, .3, ZS * 2]); proj('nivel', [2, 0, ZS * Lv]); proj('arco', [Math.sqrt(Lv) * Math.cos(.35), Math.sqrt(Lv) * Math.sin(.35), 0]);
  }
  for (const [nm, v] of [['c00', [0, 0, 0]], ['c20', [2, 0, 0]], ['c22', [2, 2, 0]], ['c02', [0, 2, 0]]]) proj(nm, v);
  R.render(S, cam);
  return PTS;
};
window.cenaPronta = true;
