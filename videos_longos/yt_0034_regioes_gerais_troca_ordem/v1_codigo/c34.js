// yt_0034 · cenas 3D (porte de referencia/c3d34.html, three.js r128; motor do c32.js do yt_0032). Uma página por cena (cena1.html, cena2.html)
// define window.CENA_ID. Estilo do c3d34: opaco e sem luz (MeshBasicMaterial), topo na cor por altura (rampa escura → ciano), paredes a 70 % / 48 %
// sobre o fundo, face cortada em pé âmbar / deitada magenta com contorno escuro fino, sem sombra/névoa/brilho/transparência, outputEncoding linear,
// antialias, fundo transparente (o Manim põe o violeta liso por baixo). Mundo: x e y em metros × SC; z desenhado = SC · ZS · valor; up = +z.
// A CÂMERA VEM DO MANIM no estado: {pos, tgt, up, cx, cy, fov} (perspectiva + setViewOffset: o alvo cai em (cx, cy) px de 1080p) ou, com
// orto = true, a OrthographicCamera de k px por unidade do mundo (último quadro do pouso lateral).
// cena1 = cunha z = y sobre o quarto de disco de raio 2 (SC 1, ZS 1, VMAX 2): tipo 'pe' (faca em x = 1, alvo b31) ou 'dei' (faca em y = 1, b32).
// cena2 = sino z = e^(−y²) sobre o triângulo 0 ≤ x ≤ y ≤ 1 (SC 2, ZS 1 ou o zs do estado, VMAX 1,15): 'pe' (x = 0,4, b42p) ou 'dei' (y = 0,6, b42).
// Estados (0..1): cresce (o sólido sobe do chão), faca (o plano da faca, só a borda, desce até o lugar), corte (a parte cortada recua até o
// deslocamento do alvo), face (a face cortada acende), sai (a parte cortada desliza para baixo e sai do quadro, antes do pouso).
// Em cresce = faca... = 1 e na câmera do alvo cada chave reproduz o c3d34.html.
const T = THREE, PI = Math.PI, K = window.CENA_ID;
const W = window.innerWidth, H = window.innerHeight, ESC = W / 1920;
const R = new T.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
R.setPixelRatio(1); R.setSize(W, H, false); R.setClearColor(0x000000, 0); R.outputEncoding = T.LinearEncoding;
document.body.appendChild(R.domElement);
const S = new T.Scene(); T.Object3D.DefaultUp.set(0, 0, 1);
const camP = new T.PerspectiveCamera(22, W / H, .05, 4000), camO = new T.OrthographicCamera(-1, 1, 1, -1, .05, 4000);
let cam = camP;
const BG = '#131030', CI = '#35D9FF', E1 = '#FFC24D', E2 = '#EA63FF', GEO = '#B8C4DA', RAMP0 = '#10243A';
const C = h => new T.Color(h), mixc = (a, b, t) => C(a).lerp(C(b), t);
let SC = 1, ZS = 1, VMAX = 2, G = null, PTS = {}, CRESCE = 1;

function aplicaCam(c) {
  if (c.orto) {
    cam = camO;
    const k = c.k;                                        // px de 1080p por unidade do mundo
    camO.left = -c.cx / k; camO.right = (1920 - c.cx) / k; camO.top = c.cy / k; camO.bottom = -(1080 - c.cy) / k;
    camO.up.set(...c.up); camO.position.set(...c.pos); camO.lookAt(...c.tgt);
    camO.updateProjectionMatrix(); camO.updateMatrixWorld(true);
  } else {
    cam = camP;
    camP.fov = c.fov || 22;
    camP.up.set(...c.up); camP.position.set(...c.pos); camP.lookAt(...c.tgt);
    camP.setViewOffset(W, H, (960 - c.cx) * ESC, (540 - c.cy) * ESC, W, H);
    camP.updateProjectionMatrix(); camP.updateMatrixWorld(true);
  }
}
function proj(nome, v) { const q = new T.Vector3(...v).project(cam); PTS[nome] = [+((q.x + 1) / 2 * 1920).toFixed(2), +((1 - q.y) / 2 * 1080).toFixed(2)]; }
function add(o) { G.add(o); return o; }
function poli(pts) { const cp = new T.CurvePath(); for (let i = 0; i + 1 < pts.length; i++) cp.add(new T.LineCurve3(new T.Vector3(...pts[i]), new T.Vector3(...pts[i + 1]))); return cp; }
const tubo = (pts, r, cor) => add(new T.Mesh(new T.TubeGeometry(poli(pts), Math.max(8, (pts.length - 1) * 4), r, 8, false), new T.MeshBasicMaterial({ color: C(cor) })));
function seta(a, b, r, cor) {
  const A = new T.Vector3(...a), B = new T.Vector3(...b), d = B.clone().sub(A), L = d.length(), hl = Math.min(.16, .3 * L), gr = new T.Group(), m = new T.MeshBasicMaterial({ color: C(cor) });
  const s = new T.Mesh(new T.CylinderGeometry(r, r, L - hl, 12), m); s.position.y = (L - hl) / 2; const c = new T.Mesh(new T.ConeGeometry(r * 3, hl, 18), m); c.position.y = L - hl / 2; gr.add(s, c);
  gr.position.copy(A); gr.quaternion.setFromUnitVectors(new T.Vector3(0, 1, 0), d.normalize()); add(gr); return gr;
}
function malhaTri(tris) {
  const pos = [], col = []; for (const [a, b, c, cc] of tris) { for (const p of [a, b, c]) { pos.push(...p); col.push(cc.r, cc.g, cc.b); } }
  const g = new T.BufferGeometry(); g.setAttribute('position', new T.Float32BufferAttribute(pos, 3)); g.setAttribute('color', new T.Float32BufferAttribute(col, 3));
  return add(new T.Mesh(g, new T.MeshBasicMaterial({ vertexColors: true, side: T.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 })));
}
const corAlt = v => mixc(RAMP0, CI, Math.pow(Math.min(1, Math.max(0, v) / VMAX), .85));
const W3 = (X, Y, v, off) => [SC * (X + off[0]), SC * (Y + off[1]), SC * ZS * v * CRESCE + SC * (off[2] || 0)];
// sólido embaixo de h sobre a região parametrizada p(u, v) → [x, y]; paredes nas 4 bordas; cor = {u0, u1, v0, v1: [cor forçada, mistura]}
function solido(p, h, { nu = 30, nv = 30, off = [0, 0, 0], cor = {} } = {}) {
  const T3 = [];
  for (let i = 0; i < nu; i++) for (let j = 0; j < nv; j++) {
    const q = [p(i / nu, j / nv), p((i + 1) / nu, j / nv), p((i + 1) / nu, (j + 1) / nv), p(i / nu, (j + 1) / nv)];
    const m = p((i + .5) / nu, (j + .5) / nv), cc = corAlt(h(...m)), z = a => W3(a[0], a[1], h(a[0], a[1]), off);
    T3.push([z(q[0]), z(q[1]), z(q[2]), cc], [z(q[0]), z(q[2]), z(q[3]), cc]);
  }
  const parede = (pts, forca) => {
    for (let k = 0; k + 1 < pts.length; k++) {
      const a = pts[k], b = pts[k + 1]; const dx = b[0] - a[0], dy = b[1] - a[1]; if (Math.hypot(dx, dy) < 1e-9) continue;
      const mid = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2], top = corAlt(h(...mid)).getStyle();
      let cc = mixc(BG, top, Math.abs(dy) > Math.abs(dx) ? .70 : .48);
      if (forca) cc = cc.clone().lerp(C(forca[0]), forca[1]);
      const A0 = W3(a[0], a[1], 0, off), B0 = W3(b[0], b[1], 0, off), A1 = W3(a[0], a[1], h(...a), off), B1 = W3(b[0], b[1], h(...b), off);
      T3.push([A0, B0, B1, cc], [A0, B1, A1, cc]);
    }
  };
  const N = 60, borda = f => Array.from({ length: N + 1 }, (_, s) => f(s / N));
  parede(borda(t => p(0, t)), cor.u0); parede(borda(t => p(1, t)), cor.u1); parede(borda(t => p(t, 0)), cor.v0); parede(borda(t => p(t, 1)), cor.v1);
  const laco = [].concat(borda(t => p(t, 0)), borda(t => p(1, t)), borda(t => p(1 - t, 1)), borda(t => p(0, 1 - t)));
  chao(laco, off);
  return malhaTri(T3);
}
function contorno(pts, h, cor, r = .009, off = [0, 0, 0]) {
  const c = [W3(pts[0][0], pts[0][1], 0, off)]; for (const a of pts) c.push(W3(a[0], a[1], h(...a), off));
  const z = pts[pts.length - 1]; c.push(W3(z[0], z[1], 0, off), W3(pts[0][0], pts[0][1], 0, off)); tubo(c, r, cor);
}
function chao(pts, off = [0, 0, 0], fill = '#1C1846', cor = GEO) {
  const oz = SC * (off[2] || 0);
  const sh = new T.Shape(pts.map(a => new T.Vector2(SC * (a[0] + off[0]), SC * (a[1] + off[1]))));
  const m = add(new T.Mesh(new T.ShapeGeometry(sh), new T.MeshBasicMaterial({ color: C(fill) }))); m.position.z = oz - .002;
  tubo(pts.concat([pts[0]]).map(a => [SC * (a[0] + off[0]), SC * (a[1] + off[1]), oz + .001]), .006, cor);
}
function eixos(lx, ly, lz) {
  seta([0, 0, .014], [lx, 0, .014], .011, E1); seta([0, 0, .014], [0, ly, .014], .011, E2); seta([0, 0, 0], [0, 0, lz], .011, CI);
  proj('ex', [lx + .12, 0, 0]); proj('ey', [0, ly + .12, 0]); proj('ez', [0, 0, lz + .12]);
}
// plano da faca: retângulo opaco e fino, SÓ A BORDA (tubo), descendo do alto até o lugar (faca de 0 a 1)
function faca(cantos, cor, fz) {
  if (fz <= 1e-3) return;
  const dz = (1 - fz) * 3.2 * SC;
  tubo(cantos.concat([cantos[0]]).map(q => [q[0], q[1], q[2] + dz]), .012 * SC, cor);
}
const sm = u => { u = Math.min(1, Math.max(0, u)); return u * u * (3 - 2 * u); };

window.setEstado = e => {
  if (G) { S.remove(G); G.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.material) o.material.dispose(); }); }
  G = new T.Group(); S.add(G); PTS = {};
  aplicaCam(e.cam);
  CRESCE = e.cresce ?? 1;
  const tipo = e.tipo || 'pe', fz = e.faca ?? 0, ct = e.corte ?? 0, fc = e.face ?? 0, sai = e.sai ?? 0;
  const S3 = Math.sqrt(3);

  if (K === 'cena1') {                                   // cunha z = y sobre o quarto de disco
    SC = 1; ZS = 1; VMAX = 2; const hy = (X, Y) => Y;
    eixos(e.lx ?? 3.3, e.ly ?? 2.45, e.lz ?? 2.35);
    if (tipo === 'pe') {                                 // b31: em pé em x = 1; a parte x > 1 recua D = 0,75 em +x
      const D = .75 * ct, off = [D, 0, -9 * sm(sai)];
      solido((u, v) => { const X = u; return [X, v * Math.sqrt(4 - X * X)]; }, hy, { cor: { u1: [E1, fc] } });
      if (sai < .999) solido((u, v) => { const X = 1 + u; return [X, v * Math.sqrt(Math.max(0, 4 - X * X))]; }, hy, { off });
      if (fc > .01) contorno(Array.from({ length: 41 }, (_, s) => [1, S3 * s / 40]), hy, '#7A5A10', .008);
      faca([[1, -.25, 0], [1, 2.2, 0], [1, 2.2, 2.25], [1, -.25, 2.25]], E1, fz);
      proj('fatia', [1, 1.15, .42 * CRESCE]); proj('faca', [1, S3, (S3 + .14) * CRESCE]); proj('base', [1, S3 / 2, 0]); proj('alt', [1, S3, S3 / 2 * CRESCE]); proj('x1', [1, 0, 0]);
      proj('f0', [1, 0, 0]); proj('f1', [1, S3, 0]); proj('f2', [1, S3, S3 * CRESCE]);
    } else {                                             // b32: deitada em y = 1; a parte y < 1 desliza para a frente e para o lado
      const off = [2.35 * ct, -.9 * ct, -9 * sm(sai)];
      solido((u, v) => { const Y = 1 + u; return [v * Math.sqrt(Math.max(0, 4 - Y * Y)), Y]; }, hy, { cor: { u0: [E2, fc] } });
      if (sai < .999) solido((u, v) => { const Y = u; return [v * Math.sqrt(4 - Y * Y), Y]; }, hy, { off });
      if (fc > .01) contorno(Array.from({ length: 41 }, (_, s) => [S3 * s / 40, 1]), hy, '#6A1E78', .008);
      faca([[-.25, 1, 0], [2.2, 1, 0], [2.2, 1, 2.25], [-.25, 1, 2.25]], E2, fz);
      proj('fatia', [S3 / 2, 1, .5 * CRESCE]); proj('faca', [S3, 1, 1.14 * CRESCE]); proj('base', [S3 / 2, 1, 0]); proj('alt', [0, 1, .5 * CRESCE]); proj('y1', [0, 1, 0]);
      proj('f0', [0, 1, 0]); proj('f1', [S3, 1, 0]); proj('f2', [S3, 1, CRESCE]); proj('f3', [0, 1, CRESCE]);
    }
  }

  if (K === 'cena2') {                                   // sino z = e^(−y²) sobre o triângulo 0 ≤ x ≤ y ≤ 1 (mundo × 2)
    SC = 2; ZS = e.zs ?? 1; VMAX = 1.15; const hs = (X, Y) => Math.exp(-Y * Y);
    eixos(e.lx ?? (tipo === 'pe' ? 3.6 : 2.45), e.ly ?? (tipo === 'pe' ? 2.35 : 2.4), e.lz ?? 1.75);
    const Z = v => SC * ZS * v * CRESCE;
    if (tipo === 'pe') {                                 // b42p: em pé em x = 0,4 (teto curvo); a parte x > 0,4 recua D = 0,85
      const x0 = .4, off = [.85 * ct, 0, -9 * sm(sai)];
      solido((u, v) => { const X = x0 * u; return [X, X + (1 - X) * v]; }, hs, { cor: { u1: [E1, fc] } });
      if (sai < .999) solido((u, v) => { const X = x0 + (1 - x0) * u; return [X, X + (1 - X) * v]; }, hs, { off });
      if (fc > .01) contorno(Array.from({ length: 41 }, (_, s) => [x0, x0 + (1 - x0) * s / 40]), hs, '#7A5A10', .008);
      faca([[2 * x0, -.3, 0], [2 * x0, 2.3, 0], [2 * x0, 2.3, 2.0], [2 * x0, -.3, 2.0]], E1, fz);
      proj('fatia', [2 * x0, 2 * .7, .5 * CRESCE]); proj('teto', [2 * x0, 2 * .72, Z(hs(0, .72)) + .12]); proj('faca', [2 * x0, 2, Z(hs(0, 1)) + .14]); proj('x1', [2 * x0, 0, 0]);
    } else {                                             // b42: deitada em y = 0,6 (retângulo); a parte y < 0,6 desliza para a frente e para o lado
      const y0 = .6, off = [1.75 * ct, -.55 * ct, -9 * sm(sai)];
      solido((u, v) => { const Y = y0 + (1 - y0) * u; return [Y * v, Y]; }, hs, { cor: { u0: [E2, fc] } });
      if (sai < .999) solido((u, v) => { const Y = y0 * u; return [Y * v, Y]; }, hs, { off });
      if (fc > .01) contorno(Array.from({ length: 41 }, (_, s) => [y0 * s / 40, y0]), hs, '#6A1E78', .008);
      faca([[-.3, 2 * y0, 0], [2.3, 2 * y0, 0], [2.3, 2 * y0, 2.0], [-.3, 2 * y0, 2.0]], E2, fz);
      proj('fatia', [2 * y0 / 2, 2 * y0, .6 * CRESCE]); proj('teto', [2 * y0 / 2, 2 * y0, Z(hs(0, y0)) + .12]); proj('faca', [2 * y0, 2 * y0, Z(hs(0, y0)) + .14]);
      proj('base', [2 * y0 / 2, 2 * y0, 0]); proj('alt', [0, 2 * y0, Z(hs(0, y0)) / 2]); proj('y1', [0, 2 * y0, 0]);
      proj('f0', [0, 2 * y0, 0]); proj('f1', [2 * y0, 2 * y0, 0]); proj('f2', [2 * y0, 2 * y0, Z(hs(0, y0))]); proj('f3', [0, 2 * y0, Z(hs(0, y0))]);
    }
  }
  R.render(S, cam);
  return PTS;
};
window.cenaPronta = true;
