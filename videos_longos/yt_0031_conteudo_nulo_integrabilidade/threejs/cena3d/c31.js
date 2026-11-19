// yt_0031 · cenas 3D (porte de referencia/c3d31.html, three.js r128). Uma página por cena (b13.html, b21.html, b52.html) define window.CENA_ID.
// Mesmo estilo do c3d31: opaco e sem luz (MeshBasicMaterial), tom por face (topo = cor; faces x 70 %; faces y 48 % sobre o fundo), contorno escuro fino
// até n = 16 e sem contorno de n = 32 em diante, sem sombra/névoa/brilho/transparência, fundo transparente (o Manim põe o violeta liso por baixo).
// Mundo: x e y em metros (chapa [0,2]²), z desenhado = ZS · valor. Câmera perspectiva fov 22°.
// A CÂMERA VEM DO MANIM no estado ({pos, tgt, up, cx, cy}), já interpolada no pouso; assim o Python projeta os mesmos pontos (rótulos) e este
// arquivo devolve os pontos projetados pelo three.js em px de 1920×1080 (pontos.json, QA de alinhamento ≤ 2 px).
// setEstado(e): e = {cam, n, cresce, muro, afunda, tampas, chao}; a cena é refeita a cada quadro (geometria pequena).
const T = THREE, PI = Math.PI, K = window.CENA_ID;
const W = window.innerWidth, H = window.innerHeight, ESC = W / 1920;
const R = new T.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
R.setPixelRatio(1); R.setSize(W, H, false); R.setClearColor(0x000000, 0); R.outputEncoding = T.LinearEncoding;
document.body.appendChild(R.domElement);
const S = new T.Scene(); T.Object3D.DefaultUp.set(0, 0, 1);
const cam = new T.PerspectiveCamera(22, W / H, .05, 200);
const BG = '#131030', CI = '#35D9FF', AZC = '#7FB2FF', CORAL = '#FF7A8A', E1 = '#FFC24D', E2 = '#EA63FF', GEO = '#B8C4DA',
  LEVE = '#1E5072', PESADO = '#30BBE0', BR = '#F5F7FF', RAMP0 = '#10243A';
const C = h => new T.Color(h), mixc = (a, b, t) => C(a).lerp(C(b), t);
let ZS = .25, G = null, PTS = {};
const f = (x, y) => x * x + y * y;
const g = a => 1 + .42 * Math.sin(1.7 * a - .4);

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
function base(cor = GEO, { x1 = 2, y1 = 2, fill = '#1C1846' } = {}) {
  const p = add(new T.Mesh(new T.PlaneGeometry(x1, y1), new T.MeshBasicMaterial({ color: C(fill) }))); p.position.set(x1 / 2, y1 / 2, -.002);
  tubo([[0, 0, 0], [x1, 0, 0], [x1, y1, 0], [0, y1, 0], [0, 0, 0]].map(q => [q[0], q[1], .001]), .006, cor);
}
// chão com o mapa da densidade (só no pouso do b13: casa com a chapa 2D do Manim); `chao` mistura o mapa com o fundo da base (cor, sem transparência)
function chaoMapa(t) {
  const n = 64, d = new Uint8Array(n * n * 4), b = C('#1C1846');
  for (let j = 0; j < n; j++) for (let i = 0; i < n; i++) {
    const v = f((i + .5) * 2 / n, (j + .5) * 2 / n), c = mixc(RAMP0, CI, Math.pow(Math.min(1, v / 8), .85)), k = 4 * (j * n + i);
    const cc = b.clone().lerp(c, t); d[k] = Math.round(cc.r * 255); d[k + 1] = Math.round(cc.g * 255); d[k + 2] = Math.round(cc.b * 255); d[k + 3] = 255;
  }
  const tx = new T.DataTexture(d, n, n, T.RGBAFormat); tx.magFilter = T.NearestFilter; tx.minFilter = T.NearestFilter; tx.needsUpdate = true;
  const p = add(new T.Mesh(new T.PlaneGeometry(2, 2), new T.MeshBasicMaterial({ map: tx }))); p.position.set(1, 1, -.001);
}
function malha(n, cor, r, k) {
  for (let q = 0; q <= n; q++) {
    const a = 2 * q / n, L1 = [], L2 = [];
    for (let t = 0; t <= 48; t++) { const b = 2 * t / 48; L1.push([a, b, k * ZS * f(a, b)]); L2.push([b, a, k * ZS * f(b, a)]); }
    const rr = (q === 0 || q === n) ? .008 : r; tubo(L1, rr, (q === 0 || q === n) ? CI : cor); tubo(L2, rr, (q === 0 || q === n) ? CI : cor);
  }
}
function faixa(a, b, am = 400) { let mn = 9, mx = -9; for (let s = 0; s <= am; s++) { const v = g(a + (b - a) * s / am); mn = Math.min(mn, v); mx = Math.max(mx, v); } return [mn, mx]; }
function celulaMetal(a, b, c, d) { const [mn, mx] = faixa(a, b); const leve = c <= mx, pesado = d > mn; return { piso: leve ? 1 : 3, teto: pesado ? 3 : 1, vermelha: leve && pesado }; }
const sm = u => { u = Math.min(1, Math.max(0, u)); return u * u * (3 - 2 * u); };

window.setEstado = e => {
  if (G) { S.remove(G); G.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.material) { if (o.material.map) o.material.map.dispose(); o.material.dispose(); } }); }
  G = new T.Group(); S.add(G); PTS = {};
  aplicaCam(e.cam);
  const cresce = e.cresce ?? 1, muro = e.muro ?? 1, eix = (e.eixos ?? 1) > 0;
  const CT = mixc(CORAL, '#FFE1E6', e.acende ?? 0).getStyle();   // v2: 'acender' = a cor clareia e volta (sem brilho)
  if (K === 'b13') {
    ZS = .25; const n = 4, h = 2 / n, L = [], Tp = [], afunda = e.afunda ?? 0, tampas = e.tampas ?? 1;
    if ((e.chao ?? 0) > 0) chaoMapa(e.chao); else base();
    if ((e.chao ?? 0) > 0) tubo([[0, 0, .001], [2, 0, .001], [2, 2, .001], [0, 2, .001], [0, 0, .001]], .006, GEO);
    for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
      const lo = ZS * f(i * h, j * h) * cresce, hi = ZS * f((i + 1) * h, (j + 1) * h) * cresce;
      const topo = lo * (1 - afunda);                      // o prédio desce inteiro abaixo do chão (corte em z = 0)
      if (topo > 1e-4) L.push({ x0: i * h, x1: (i + 1) * h, y0: j * h, y1: (j + 1) * h, z0: 0, z1: Math.max(.0015, topo), c: AZC });
      if (tampas > 0) Tp.push({ x0: i * h, x1: (i + 1) * h, y0: j * h, y1: (j + 1) * h, z0: lo, z1: lo + (hi - lo) * tampas, c: CT });
    }
    if (L.length) caixas(L, { corBorda: '#0A1A3A' }); if (Tp.length) caixas(Tp, { corBorda: '#3A1220' });
    if (afunda > .02) {                                    // o prédio afundou: fica o contorno do chão das colunas (cor misturada pelo quanto afundou)
      const c = mixc('#1C1846', mixc(BG, GEO, .5).getStyle(), Math.min(1, afunda)).getStyle();
      for (let i = 0; i <= n; i++) { tubo([[i * h, 0, .002], [i * h, 2, .002]], .004, c); tubo([[0, i * h, .002], [2, i * h, .002]], .004, c); }
    }
    if (cresce > 0) malha(8, mixc(BG, CI, .8).getStyle(), .0035, cresce);
    if (eix) {
      seta([0, 0, .014], [2.45, 0, .014], .011, E1); seta([0, 0, .014], [0, 3.3, .014], .011, E2); seta([0, 0, 0], [0, 0, 2.25], .011, CI);
      for (const v of [2, 4, 6, 8]) tubo([[-.05, 0, v * ZS], [.05, 0, v * ZS]], .008, CI);
    }
    proj('ex', [2.57, 0, 0]); proj('ey', [0, 3.42, 0]); proj('ez', [0, 0, 2.37]);
    for (const v of [2, 4, 6, 8]) proj('m' + v, [-.13, -.02, v * ZS]);
    const i = 3, j = 3; proj('tampaTopo', [(i + .5) * h, (j + .5) * h, ZS * f(2, 2)]); proj('tampaBase', [(i + 1) * h, j * h, ZS * f(i * h, j * h)]);
    proj('tampaAlto', [(i + 1) * h, j * h, ZS * f(2, 2)]); proj('canto', [2, 2, ZS * 8]);
  }
  if (K === 'b21') {
    ZS = .5; const n = e.n || 16, h = 2 / n, L = [], Tp = []; base();
    for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
      const a = i * h, b = a + h, c = j * h, d = c + h, cel = celulaMetal(a, b, c, d);
      L.push({ x0: a, x1: b, y0: c, y1: d, z0: 0, z1: Math.max(.0015, ZS * cel.piso * cresce), c: cel.piso === 1 ? LEVE : PESADO });
      if (cel.vermelha && muro > 0) Tp.push({ x0: a, x1: b, y0: c, y1: d, z0: ZS * cel.piso, z1: ZS * (cel.piso + (cel.teto - cel.piso) * muro), c: CT });
    }
    caixas(L, { bordas: n <= 16, corBorda: '#08142A' }); if (Tp.length) caixas(Tp, { bordas: n <= 16, corBorda: '#3A1220' });
    seta([0, 0, .014], [2.45, 0, .014], .011, E1); seta([0, 0, .014], [0, 2.45, .014], .011, E2); seta([0, 0, 0], [0, 0, 1.95], .011, CI);
    proj('ex', [2.57, 0, 0]); proj('ey', [0, 2.57, 0]); proj('ez', [0, 0, 2.07]);
    tubo([[-.05, 0, ZS * 1], [.05, 0, ZS * 1]], .008, CI); tubo([[-.05, 0, ZS * 3], [.05, 0, ZS * 3]], .008, CI); proj('m1', [-.13, -.02, ZS * 1]); proj('m3', [-.13, -.02, ZS * 3]);
    proj('leve', [1.75, .35, ZS * 1]); proj('pesado', [.35, 1.75, ZS * 3]); proj('muro', [1.159, g(1.159), ZS * 3 + .04]); proj('muroE', [.05, g(.05), ZS * 3]);
  }
  if (K === 'b52') {
    ZS = .5; const n = 16, h = 2 / n, L = [], Tp = []; base();
    for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
      const a = i * h, b = a + h, c = j * h, d = c + h, near = a * a + c * c, far = b * b + d * d;
      if (far <= 4) L.push({ x0: a, x1: b, y0: c, y1: d, z0: 0, z1: Math.max(.0015, ZS * cresce), c: mixc(BG, CI, .82).getStyle() });
      else if (near < 4 && muro > 0) Tp.push({ x0: a, x1: b, y0: c, y1: d, z0: 0, z1: ZS * muro, c: CT });
    }
    caixas(L, { corBorda: '#06101F' }); if (Tp.length) caixas(Tp, { corBorda: '#3A1220' });
    const arc = []; for (let k = 0; k <= 90; k++) { const t = PI / 2 * k / 90; arc.push([2 * Math.cos(t), 2 * Math.sin(t), .003]); } tubo(arc, .01, BR);
    seta([0, 0, .014], [2.45, 0, .014], .011, E1); seta([0, 0, .014], [0, 2.45, .014], .011, E2);
    proj('ex', [2.57, 0, 0]); proj('ey', [0, 2.57, 0]); proj('B', [.6, .6, ZS]); proj('muro', [1.41, 1.41, ZS + .03]); proj('fora', [1.85, 1.85, 0]);
  }
  for (const [nm, v] of [['c00', [0, 0, 0]], ['c20', [2, 0, 0]], ['c22', [2, 2, 0]], ['c02', [0, 2, 0]]]) proj(nm, v);
  R.render(S, cam);
  return PTS;
};
window.cenaPronta = true;
