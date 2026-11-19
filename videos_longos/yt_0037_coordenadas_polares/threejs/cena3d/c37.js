// yt_0037 · cenas 3D (porte de referencia/c3d34t2.html, three.js r128; motor do c35.js do yt_0035). Uma página por cena (sino.html,
// gauss.html) define window.CENA_ID. Estilo da série: opaco e sem luz (MeshBasicMaterial), topo na cor por altura (rampa #10243A → ciano),
// sem sombra/névoa/brilho/transparência, outputEncoding linear, antialias, fundo transparente (o Manim põe o violeta liso por baixo).
// A CÂMERA VEM DO MANIM no estado: {pos, tgt, up, cx, cy, fov} (perspectiva + setViewOffset: o alvo cai em (cx, cy) px de 1080p) ou, com
// orto = true, a OrthographicCamera de k px por unidade do mundo (último quadro da subida do gauss).
// sino  = z = e^(−(x²+y²)) sobre o disco unitário (SC = 2, ZS = 0,95). Estados: cresce (0 → 1: o sino sobe do chão), casca (0 → 1: a borda
//   laranja do corte cilíndrico r = 0,55 desce de cima; em 1 o corte acontece: o miolo fica opaco e o lado de fora vira TRAÇO #6C7698 — a peça
//   nunca se separa), parede (0 → 1: a face do corte acende em laranja escurecido, bordas laranja vivas).
// gauss = o mesmo sino sobre o quadrado [−1,25; 1,25]² (SC = 1,15, ZS = 1,3). Estados: cresce (0 → 1), discos (0 → 1: o inscrito azul-claro e
//   o circunscrito coral se desenham no chão). A subida da câmera é só câmera (vem do Manim).
const T = THREE, PI = Math.PI, K = window.CENA_ID;
const W = window.innerWidth, H = window.innerHeight, ESC = W / 1920;
const R = new T.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
R.setPixelRatio(1); R.setSize(W, H, false); R.setClearColor(0x000000, 0); R.outputEncoding = T.LinearEncoding;
document.body.appendChild(R.domElement);
const S = new T.Scene(); T.Object3D.DefaultUp.set(0, 0, 1);
const camP = new T.PerspectiveCamera(22, W / H, .05, 4000), camO = new T.OrthographicCamera(-1, 1, 1, -1, .05, 4000);
let cam = camP;
const BG = '#131030', CI = '#35D9FF', E1 = '#FFC24D', E2 = '#EA63FF', GEO = '#B8C4DA', RAMP0 = '#10243A', RR = '#FF9440',
  AZC = '#7FB2FF', CORAL = '#FF7A8A', TR = '#6C7698', LI = '#C6F26B';
const C = h => new T.Color(h), mixc = (a, b, t) => C(a).lerp(C(b), t);
let SC = 2, ZS = 1, VMAX = 1, G = null, PTS = {}, CR = 1;
const sm = u => { u = Math.min(1, Math.max(0, u)); return u * u * (3 - 2 * u); };

function aplicaCam(c) {
  if (c.orto) {
    cam = camO;
    const k = c.k;
    camO.left = -c.cx / k; camO.right = (1920 - c.cx) / k; camO.top = c.cy / k; camO.bottom = -(1080 - c.cy) / k;
    camO.up.set(...c.up); camO.position.set(...c.pos); camO.lookAt(...c.tgt);
    camO.updateProjectionMatrix(); camO.updateMatrixWorld(true);
  } else {
    cam = camP;
    camP.fov = c.fov || 22;
    // v2: near/far em volta da cena (a subida do gauss chega a ~700 unidades com fov 0,5°; near fixo 0,05 dava ruído de profundidade)
    const dd = Math.hypot(c.pos[0] - c.tgt[0], c.pos[1] - c.tgt[1], c.pos[2] - c.tgt[2]);
    camP.near = Math.max(.05, dd - 12); camP.far = dd + 12;
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
// superfície paramétrica em (a,b) -> [x, y, valor]; cor por altura (o valor SEM o fator de crescimento: a cor é a do sino pronto) ou cor fixa
function sup(F, a0, a1, b0, b1, na, nb, cor = null) {
  const tris = []; const P = (a, b) => { const q = F(a, b); return [SC * q[0], SC * q[1], SC * ZS * q[2] * (q[3] ?? CR)]; };
  for (let i = 0; i < na; i++) for (let j = 0; j < nb; j++) {
    const a = a0 + (a1 - a0) * i / na, b = a0 + (a1 - a0) * (i + 1) / na, c = b0 + (b1 - b0) * j / nb, d = b0 + (b1 - b0) * (j + 1) / nb;
    const v = F((a + b) / 2, (c + d) / 2)[2], cc = cor ? (typeof cor === 'function' ? cor((a + b) / 2, (c + d) / 2) : C(cor)) : corAlt(Math.abs(v));
    tris.push([P(a, c), P(b, c), P(b, d), cc], [P(a, c), P(b, d), P(a, d), cc]);
  }
  return malhaTri(tris);
}
const anel = (f, n = 120, t0 = 0, t1 = 2 * PI) => Array.from({ length: n + 1 }, (_, k) => f(t0 + (t1 - t0) * k / n));
const W3 = (X, Y, v) => [SC * X, SC * Y, SC * ZS * v * CR];
const W0 = (X, Y, z = 0) => [SC * X, SC * Y, z];
function chaoDisco(Rr, fill = '#1C1846') { const m = add(new T.Mesh(new T.CircleGeometry(SC * Rr, 128), new T.MeshBasicMaterial({ color: C(fill) }))); m.position.z = -.003; }
function gradePolar(Rr, nr, nt, cor = '#3A3470') {
  for (let i = 1; i <= nr; i++) { const r = Rr * i / nr; tubo(anel(t => W0(r * Math.cos(t), r * Math.sin(t))), .0045, cor); }
  for (let k = 0; k < nt; k++) { const t = 2 * PI * k / nt; tubo([W0(0, 0), W0(Rr * Math.cos(t), Rr * Math.sin(t))], .0045, cor); }
}
function eixos(lx, ly, lz, z0 = 0) {
  seta([0, 0, .012], [lx, 0, .012], .011, E1); seta([0, 0, .012], [0, ly, .012], .011, E2); seta([0, 0, z0], [0, 0, lz], .011, CI);
  proj('ex', [lx + .13, 0, 0]); proj('ey', [0, ly + .13, 0]); proj('ez', [0, 0, lz + .13]);
}
const fb = r => Math.exp(-r * r);

window.setEstado = e => {
  if (G) { S.remove(G); G.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.material) o.material.dispose(); }); }
  G = new T.Group(); S.add(G); PTS = {};
  aplicaCam(e.cam);
  CR = Math.max(1e-3, e.cresce ?? 1);

  if (K === 'sino') {
    SC = 2; ZS = .95; VMAX = 1; const r0 = .55;
    const ca = e.casca ?? 0, pa = e.parede ?? 0, cortado = ca > .999;
    chaoDisco(1); gradePolar(1, 4, 12); tubo(anel(t => W0(Math.cos(t), Math.sin(t))), .007, GEO);
    if (!cortado) {
      sup((r, t) => [r * Math.cos(t), r * Math.sin(t), fb(r)], 0, 1, 0, 2 * PI, 40, 96);
      if (ca > 1e-3) {                                   // a borda do corte cilíndrico desce de cima até o chão (a "faca" das polares)
        const zc = (1 - sm(ca)) * 3.0 + .002;
        tubo(anel(t => [SC * r0 * Math.cos(t), SC * r0 * Math.sin(t), zc]), .011, RR);
      }
    } else {
      // miolo opaco: teto e^(−r²) para r ≤ r0
      sup((r, t) => [r * Math.cos(t), r * Math.sin(t), fb(r)], 0, r0, 0, 2 * PI, 22, 96);
      // parede da casca (face do corte): antes de acender, o tom da borda do teto escurecido; aceso, laranja escurecido (handoff §2.2)
      const base = mixc(BG, corAlt(fb(r0)).getStyle(), .62);
      sup((s, t) => [r0 * Math.cos(t), r0 * Math.sin(t), s * fb(r0)], 0, 1, 0, 2 * PI, 2, 96,
        (s, t) => base.clone().lerp(mixc(BG, RR, .36 + .16 * Math.max(0, Math.cos(t + .75))), sm(pa)));
      const cb = pa > 1e-3 ? RR : mixc(TR, RR, 0).getStyle();
      tubo(anel(t => W3(r0 * Math.cos(t), r0 * Math.sin(t), fb(r0))), .009, pa > 1e-3 ? RR : TR);
      tubo(anel(t => W0(r0 * Math.cos(t), r0 * Math.sin(t), .002)), .009, pa > 1e-3 ? RR : TR);
      // fora do corte: traço (anéis e meridianos do teto, geratrizes da borda)
      for (const r of [.7, .85, 1]) tubo(anel(t => W3(r * Math.cos(t), r * Math.sin(t), fb(r))), .0055, TR);
      for (let k = 0; k < 12; k++) {
        const t = 2 * PI * k / 12;
        tubo(Array.from({ length: 21 }, (_, s) => { const r = r0 + (1 - r0) * s / 20; return W3(r * Math.cos(t), r * Math.sin(t), fb(r)); }), .0055, TR);
        tubo([W0(Math.cos(t), Math.sin(t), 0), W3(Math.cos(t), Math.sin(t), fb(1))], .005, TR);
      }
    }
    eixos(2.75, 2.7, 2.45);
    const tp = -.75;
    proj('parede', [SC * r0 * Math.cos(tp), SC * r0 * Math.sin(tp), SC * ZS * fb(r0) * .5 * CR]);
    proj('topoParede', [SC * r0 * Math.cos(tp), SC * r0 * Math.sin(tp), SC * ZS * fb(r0) * CR + .05]);
    proj('peParede', [SC * r0 * Math.cos(tp), SC * r0 * Math.sin(tp), 0]); proj('centro', [0, 0, 0]); proj('pico', [0, 0, SC * ZS * CR + .08]);
    proj('borda', [SC * Math.cos(-.95), SC * Math.sin(-.95), 0]); proj('rRaio', [SC * r0 * .5 * Math.cos(-.3), SC * r0 * .5 * Math.sin(-.3), 0]);
  }

  if (K === 'casca') {
    // handoff v2 §4.1 (porte do c3d34t2.html v2, chave casca). Estados: traco (0 → 1: o sino opaco do B4-1 "descasca" para fora e para dentro
    // até sobrar só a casca r0 ≤ r ≤ r1 opaca; o resto vira traço #6C7698 — a peça nunca se separa), r0 (0,10 … 0,85; r1 = r0 + 0,10),
    // anel (0 → 1: o tubo lima no chão em r1 cresce em θ de 0 a 2π, inteiro, sem raio até o centro).
    SC = 2; ZS = .95; VMAX = 1;
    const tr = sm(e.traco ?? 0), r0 = e.r0 ?? .45, r1 = r0 + .10, an = e.anel ?? 0;
    const lo = r0 * tr, hi = r1 + (1 - r1) * (1 - tr);           // a parte opaca vai de [0, 1] (tr = 0) até [r0, r1] (tr = 1)
    chaoDisco(1); gradePolar(1, 4, 12); tubo(anel(t => W0(Math.cos(t), Math.sin(t))), .007, GEO);
    if (tr > 1e-3) {                                             // traço fora da parte opaca: anéis e meridianos do sino
      for (const r of [.25, .42, .84, 1]) if (r < lo - .005 || r > hi + .005) tubo(anel(t => W3(r * Math.cos(t), r * Math.sin(t), fb(r))), .0045, TR);
      for (let k = 0; k < 8; k++) {
        const t = 2 * PI * k / 8 + PI / 8;
        if (lo > .02) tubo(Array.from({ length: 15 }, (_, s) => { const r = lo * s / 14; return W3(r * Math.cos(t), r * Math.sin(t), fb(r)); }), .0045, TR);
        if (hi < .98) tubo(Array.from({ length: 15 }, (_, s) => { const r = hi + (1 - hi) * s / 14; return W3(r * Math.cos(t), r * Math.sin(t), fb(r)); }), .0045, TR);
      }
    }
    const nT = Math.max(3, Math.round(40 * (hi - lo)));
    sup((r, t) => [r * Math.cos(t), r * Math.sin(t), fb(r)], lo, hi, 0, 2 * PI, nT, 128);                     // teto opaco (cor por altura)
    const sh = (s, t) => mixc(BG, RR, .40 + .18 * Math.max(0, Math.cos(t + .75)));
    if (hi < .999) sup((s, t) => [hi * Math.cos(t), hi * Math.sin(t), s * fb(hi)], 0, 1, 0, 2 * PI, 2, 128, sh);   // parede de fora
    if (lo > .001) sup((s, t) => [lo * Math.cos(t), lo * Math.sin(t), s * fb(lo)], 0, 1, 0, 2 * PI, 2, 128, (s, t) => mixc(BG, RR, .18));  // de dentro
    if (tr > .02) for (const r of [lo, hi]) if (r > .001 && r < .999) tubo(anel(t => W3(r * Math.cos(t), r * Math.sin(t), fb(r))), .008, RR);
    if (an > 1e-3) { const f = sm(an); tubo(anel(t => W0(r1 * Math.cos(t), r1 * Math.sin(t), .004), Math.max(8, Math.round(180 * f)), 0, 2 * PI * f), .013, LI); }
    eixos(2.75, 2.7, 2.45);
    const tf = -.75; proj('pico', [0, 0, SC * ZS * CR + .08]); proj('centro', [0, 0, 0]);
    proj('baseFrente', [SC * r1 * Math.cos(tf - .5), SC * r1 * Math.sin(tf - .5), 0]);
    proj('paredeBaixo', [SC * r1 * Math.cos(tf), SC * r1 * Math.sin(tf), 0]); proj('paredeTopo', [SC * r1 * Math.cos(tf), SC * r1 * Math.sin(tf), SC * ZS * fb(r1)]);
    proj('tetoDentro', [SC * r0 * Math.cos(tf + .35), SC * r0 * Math.sin(tf + .35), SC * ZS * fb(r0)]); proj('tetoFora', [SC * r1 * Math.cos(tf + .35), SC * r1 * Math.sin(tf + .35), SC * ZS * fb(r1)]);
    proj('raioPe', [SC * r1 * Math.cos(.35), SC * r1 * Math.sin(.35), 0]);
  }

  if (K === 'gauss') {
    SC = 1.15; ZS = 1.3; VMAX = 1; const Rq = 1.25, Rc = Rq * Math.SQRT2, dk = e.discos ?? 0;
    // R6 (handoff §3.2): o plano quadrado do c3d34t2 passava da borda da coluna; o chão vira um disco logo além do circunscrito e a grade
    // (as mesmas linhas a cada 0,5) fica recortada nele.
    const RF = Rc + .12;
    const m = add(new T.Mesh(new T.CircleGeometry(SC * RF, 160), new T.MeshBasicMaterial({ color: C('#1C1846') }))); m.position.z = -.004;
    for (let k = -4; k <= 4; k++) { const a = k * .5, h = Math.sqrt(Math.max(0, RF * RF - a * a)); if (h < .02) continue;
      tubo([W0(a, -h), W0(a, h)], .004, '#3A3470'); tubo([W0(-h, a), W0(h, a)], .004, '#3A3470'); }
    sup((X, Y) => [X, Y, Math.exp(-(X * X + Y * Y))], -Rq, Rq, -Rq, Rq, 60, 60);
    tubo([[-Rq, -Rq], [Rq, -Rq], [Rq, Rq], [-Rq, Rq], [-Rq, -Rq]].map(p => W0(p[0], p[1], .002)), .009, GEO);
    if (dk > 1e-3) {                                     // os dois discos se desenham no chão (traço), a partir do ângulo −π/2
      const f = sm(dk), t0 = -PI / 2;
      tubo(anel(t => W0(Rq * Math.cos(t), Rq * Math.sin(t), .003), Math.max(8, Math.round(120 * f)), t0, t0 + 2 * PI * f), .011, AZC);
      tubo(anel(t => W0(Rc * Math.cos(t), Rc * Math.sin(t), .003), Math.max(8, Math.round(120 * f)), t0, t0 + 2 * PI * f), .011, CORAL);
    }
    for (const s of [-1, 1]) tubo(Array.from({ length: 41 }, (_, i) => { const X = -Rq + 2 * Rq * i / 40; return W3(X, s * Rq, Math.exp(-(X * X + Rq * Rq))); }), .006, '#2A2456');
    seta([0, 0, .012], [2.2, 0, .012], .011, E1); seta([0, 0, .012], [0, 2.2, .012], .011, E2); seta([0, 0, 0], [0, 0, 2.0 * Math.max(.05, CR)], .011, CI);
    proj('ex', [2.33, 0, 0]); proj('ey', [0, 2.33, 0]); proj('ez', [0, 0, 2.13]); proj('pico', [0, 0, SC * ZS * CR + .08]);
    proj('cin', [SC * Rq * Math.cos(-2.2), SC * Rq * Math.sin(-2.2), 0]); proj('ccirc', [SC * Rc * Math.cos(-1.05), SC * Rc * Math.sin(-1.05), 0]); proj('quina', [SC * Rq, -SC * Rq, 0]);
    proj('origem', [0, 0, 0]);
  }
  R.render(S, cam);
  return PTS;
};
window.cenaPronta = true;
