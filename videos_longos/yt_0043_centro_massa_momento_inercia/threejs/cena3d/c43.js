// yt_0043 · cenas 3D (porte exato de referencia/yt_0043_quadros_alvo_v1/c3d43.html, three.js r128).
// Uma página por cena (<cena>.html) define window.CENA_ID. Estilo da série: opaco, sem luz (MeshBasicMaterial), tom fixo por face (LDIR),
// sem sombra/névoa/brilho/transparência, outputEncoding linear, antialias, fundo transparente (o Manim põe o papel por baixo).
// A câmera vem do Manim no estado: {pos, tgt, up, cx, cy, fov}.
const T = THREE, PI = Math.PI, K = window.CENA_ID;
const W = window.innerWidth, H = window.innerHeight, ESC = W / 1920;
const R = new T.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
R.setPixelRatio(1); R.setSize(W, H, false); R.setClearColor(0x000000, 0); R.outputEncoding = T.LinearEncoding;
document.body.appendChild(R.domElement);
const S = new T.Scene(); T.Object3D.DefaultUp.set(0, 0, 1);
const cam = new T.PerspectiveCamera(22, W / H, .05, 400);
const BG = '#131030', CI = '#35D9FF', E1 = '#FFC24D', E2 = '#EA63FF', EZ = '#5AA2FF', GEO = '#B8C4DA', BR = '#F5F7FF', RO = '#FF9440', TH = '#2EE6A6',
  FI = '#B48CFF', SOMB = '#FFC08A', LI = '#C6F26B', AZC = '#7FB2FF', CORAL = '#FF7A8A', TR = '#6C7698', AL = '#FF5D5D', RAMP0 = '#10243A', MEN_ = '#8CFFD2';
const C = h => new T.Color(h), mixc = (a, b, t) => C(a).lerp(C(b), t);
let SC = 2, G = null, PTS = {}, SEGS = [];
const sm = u => { u = Math.min(1, Math.max(0, u)); return u * u * (3 - 2 * u); };

function aplicaCam(c) {
  cam.fov = c.fov || 22;
  const dd = Math.hypot(c.pos[0] - c.tgt[0], c.pos[1] - c.tgt[1], c.pos[2] - c.tgt[2]);
  cam.near = Math.max(.05, dd - 14); cam.far = dd + 14;
  cam.up.set(...c.up); cam.position.set(...c.pos); cam.lookAt(...c.tgt);
  cam.setViewOffset(W, H, (960 - c.cx) * ESC, (540 - c.cy) * ESC, W, H);
  cam.updateProjectionMatrix(); cam.updateMatrixWorld(true);
}
function proj(nome, v) { const q = new T.Vector3(...v).project(cam); PTS[nome] = [+((q.x + 1) / 2 * 1920).toFixed(2), +((1 - q.y) / 2 * 1080).toFixed(2)]; }
function add(o) { G.add(o); return o; }
const Wp = (X, Y, Z) => [SC * X, SC * Y, SC * Z];
const sph = (r, f, t) => [r * Math.sin(f) * Math.cos(t), r * Math.sin(f) * Math.sin(t), r * Math.cos(f)];
const WS = (r, f, t) => Wp(...sph(r, f, t));
const cyl = (s, t, z) => [s * Math.cos(t), s * Math.sin(t), z];
const WC = (s, t, z) => Wp(...cyl(s, t, z));
function poli(pts) { const cp = new T.CurvePath(); for (let i = 0; i + 1 < pts.length; i++) cp.add(new T.LineCurve3(new T.Vector3(...pts[i]), new T.Vector3(...pts[i + 1]))); return cp; }
let NOSEG = false;
const tubo = (pts, r, cor) => { if (!NOSEG) SEGS.push(pts.map(p => p.slice())); return tubo0(pts, r, cor); };
const tubo0 = (pts, r, cor) => add(new T.Mesh(new T.TubeGeometry(poli(pts), Math.max(8, (pts.length - 1) * 3), r, 8, false), new T.MeshBasicMaterial({ color: C(cor) })));
function tracejado(pts, r, cor, on = .12, off = .09, seg = false) {
  if (seg) SEGS.push(pts.map(p => p.slice()));
  let acc = 0, cur = [pts[0]], ligado = true; const segs = [];
  for (let i = 1; i < pts.length; i++) {
    const a = new T.Vector3(...pts[i - 1]), b = new T.Vector3(...pts[i]); let L = a.distanceTo(b), pos = 0;
    while (pos < L) {
      const lim = (ligado ? on : off) - acc, step = Math.min(lim, L - pos); pos += step; acc += step; const p = a.clone().lerp(b, pos / L);
      if (ligado) cur.push([p.x, p.y, p.z]); if (acc >= (ligado ? on : off) - 1e-9) { if (ligado && cur.length > 1) segs.push(cur); ligado = !ligado; acc = 0; cur = [[p.x, p.y, p.z]]; }
    }
  }
  if (ligado && cur.length > 1) segs.push(cur); const sv = NOSEG; NOSEG = true; for (const s of segs) tubo(s, r, cor); NOSEG = sv;
}
function seta(a, b, r, cor) {
  const A = new T.Vector3(...a), B = new T.Vector3(...b), d = B.clone().sub(A), L = d.length();
  if (L < 1e-4) return;
  SEGS.push([a.slice(), b.slice()]);
  const hl = Math.min(.18, .3 * L), g = new T.Group(), m = new T.MeshBasicMaterial({ color: C(cor) });
  const s = new T.Mesh(new T.CylinderGeometry(r, r, L - hl, 12), m); s.position.y = (L - hl) / 2; const c = new T.Mesh(new T.ConeGeometry(r * 3, hl, 18), m); c.position.y = L - hl / 2; g.add(s, c);
  g.position.copy(A); g.quaternion.setFromUnitVectors(new T.Vector3(0, 1, 0), d.normalize()); add(g); return g;
}
const bolinha = (p, cor, r = .055) => { const b = new T.Mesh(new T.SphereGeometry(r, 20, 12), new T.MeshBasicMaterial({ color: C(cor) })); b.position.set(...p); add(b); return b; };
function malhaTri(tris) {
  const pos = [], col = []; for (const [a, b, c, cc] of tris) { for (const p of [a, b, c]) { pos.push(...p); col.push(cc.r, cc.g, cc.b); } }
  const g = new T.BufferGeometry(); g.setAttribute('position', new T.Float32BufferAttribute(pos, 3)); g.setAttribute('color', new T.Float32BufferAttribute(col, 3));
  return add(new T.Mesh(g, new T.MeshBasicMaterial({ vertexColors: true, side: T.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 })));
}
function sup(F, a0, a1, b0, b1, na, nb, cor) {
  const tris = []; for (let i = 0; i < na; i++) for (let j = 0; j < nb; j++) {
    const a = a0 + (a1 - a0) * i / na, b = a0 + (a1 - a0) * (i + 1) / na, c = b0 + (b1 - b0) * j / nb, d = b0 + (b1 - b0) * (j + 1) / nb;
    const cc = typeof cor === 'function' ? cor((a + b) / 2, (c + d) / 2) : C(cor); tris.push([F(a, c), F(b, c), F(b, d), cc], [F(a, c), F(b, d), F(a, d), cc]);
  } return malhaTri(tris);
}
const arco = (f, a0, a1, n = 80) => Array.from({ length: n + 1 }, (_, k) => f(a0 + (a1 - a0) * k / n));
const LDIR = new T.Vector3(.55, -.75, .45).normalize();
const tom = (cor, n, base = .50, amp = .32) => mixc(BG, cor, base + amp * Math.max(0, new T.Vector3(...n).normalize().dot(LDIR)));
const corDens = r => mixc(RAMP0, CI, Math.pow(Math.min(1, Math.max(0, r)), .85));
const RMAX = Math.SQRT2, corR = (s, z) => corDens(Math.sqrt(s * s + z * z) / RMAX);

function eixos3(lx, ly, lz, { neg = 0 } = {}) {
  seta([-neg * SC, 0, 0], [lx, 0, 0], .012, E1); seta([0, -neg * SC, 0], [0, ly, 0], .012, E2); seta([0, 0, -neg * SC], [0, 0, lz], .012, EZ);
  proj('ex', [lx + .16, 0, 0]); proj('ey', [0, ly + .16, 0]); proj('ez', [0, 0, lz + .16]);
}
function lataTraco(R = 1, Hh = 1, { cor = GEO, w = .008, nv = 12, t0 = 0, t1 = 2 * PI, cv = TR } = {}) {
  for (const z of [0, Hh]) tubo(arco(t => WC(R, t, z), t0, t1, 120), w, cor);
  for (let k = 0; k < nv; k++) { const t = 2 * PI * k / nv; if (t < t0 - 1e-9 || t > t1 + 1e-9) continue; tubo([WC(R, t, 0), WC(R, t, Hh)], w * .6, cv); }
}
function celC(s1, s2, t1, t2, z1, z2, cor = LI, { w = .010, borda = LI, fill = true } = {}) {
  const svc = NOSEG; NOSEG = true;
  if (fill) {
    const fc = n => tom(cor, n, .40, .45);
    sup((t, z) => WC(s2, t, z), t1, t2, z1, z2, 10, 4, (t, z) => fc([Math.cos(t), Math.sin(t), 0]));
    if (s1 > 1e-6) sup((t, z) => WC(s1, t, z), t1, t2, z1, z2, 10, 4, () => mixc(BG, cor, .30));
    for (const z of [z1, z2]) sup((s, t) => WC(s, t, z), s1, s2, t1, t2, 4, 10, () => fc([0, 0, z === z2 ? 1 : -1]));
    for (const t of [t1, t2]) sup((s, z) => WC(s, t, z), s1, s2, z1, z2, 3, 3, () => fc(t === t1 ? [Math.sin(t), -Math.cos(t), 0] : [-Math.sin(t), Math.cos(t), 0]));
  }
  for (const s of [s1, s2]) for (const z of [z1, z2]) if (s > 1e-6) tubo(arco(t => WC(s, t, z), t1, t2, 24), w, borda);
  for (const t of [t1, t2]) for (const z of [z1, z2]) tubo([WC(s1, t, z), WC(s2, t, z)], w, borda);
  for (const s of [s1, s2]) for (const t of [t1, t2]) if (s > 1e-6 || t === t1) tubo([WC(s, t, z1), WC(s, t, z2)], w, borda);
  NOSEG = svc;
}
function eixoZ(z0 = -.1, z1 = 1.45, cor = EZ, r = .010) { tubo([Wp(0, 0, z0), Wp(0, 0, z1)], r, cor); proj('ez', Wp(0, 0, z1 + .12)); }
function setasXY(lx = 1.55) { seta([SC * 1.03, 0, 0], [SC * lx, 0, 0], .012, E1); seta([0, SC * 1.03, 0], [0, SC * 1.55, 0], .012, E2); proj('ex', [SC * (lx + .13), 0, 0]); proj('ey', [0, SC * 1.68, 0]); }
function giroSeta(cx, cy, zz, rr = .32, cor = GEO, desenha = true) {
  if (desenha) {
    const A = arco(t => Wp(cx + rr * Math.cos(t), cy + rr * Math.sin(t), zz), -PI * .9, PI * .55, 60); tubo(A, .010, cor);
    const a1 = Wp(cx + rr * Math.cos(PI * .55), cy + rr * Math.sin(PI * .55), zz), a0 = Wp(cx + rr * Math.cos(PI * .48), cy + rr * Math.sin(PI * .48), zz); seta(a0, a1, .010, cor);
  }
  proj('giro', Wp(cx + rr, cy, zz)); proj('omega', Wp(cx + rr * Math.cos(-PI * .35), cy + rr * Math.sin(-PI * .35), zz));
}
function lataPesadaMalha() {
  const ta = -PI / 2, tb = 0;
  sup((t, z) => WC(1, t, z), tb, ta + 2 * PI, 0, 1, 110, 8, (t, z) => tom(corR(1, z), [Math.cos(t), Math.sin(t), 0], .55, .40));   // parede externa (faltavam os limites de z)
  sup((s, t) => WC(s, t, 1), 0, 1, tb, ta + 2 * PI, 24, 90, (s, t) => corR(s, 1).clone().lerp(C(BR), .06));
  for (const t of [ta, tb]) sup((s, z) => WC(s, t, z), 0, 1, 0, 1, 30, 30, (s, z) => corR(s, z));
  for (const z of [0, 1]) tubo(arco(t => WC(1, t, z), tb, ta + 2 * PI, 120), .009, CI);
  for (const z of [0, 1]) tubo(arco(t => WC(1, t, z), ta, tb, 40), .005, TR); tubo([WC(1, ta, 0), WC(1, ta, 1)], .005, TR);
  for (const t of [ta, tb]) tubo([WC(0, t, 0), WC(1, t, 0), WC(1, t, 1), WC(0, t, 1)], .009, CI);
  for (const r of [.5, 1]) for (const t of [ta, tb]) tubo(arco(a => WC(r * Math.cos(a), t, r * Math.sin(a)), 0, PI / 2, 40), .004, '#1E5C7A');
  proj('quina', WC(1, tb, 1)); proj('fundo', Wp(.08, 0, .08)); proj('O', [0, 0, 0]); proj('meio', Wp(0, 0, .5)); proj('zbar', Wp(0, 0, .5549));
}
function piso(a0, a1, b0, b1, off = -.004, step = .5, cor = '#4A5080', r = .0032) {
  NOSEG = true;
  const n0 = Math.round((a1 - a0) / step), n1 = Math.round((b1 - b0) / step);
  for (let i = 0; i <= n0; i++) { const a = a0 + i * step; tubo([Wp(a, b0, off), Wp(a, b1, off)], r * SC, cor); }
  for (let j = 0; j <= n1; j++) { const b = b0 + j * step; tubo([Wp(a0, b, off), Wp(a1, b, off)], r * SC, cor); }
  NOSEG = false;
}
const L15 = [-1.5, 1.5, -1.5, 1.5];
const PISOK = {
  lataGiro: L15, lataPesada: L15, lataDuas: L15, lataCel: L15, lataPlano: L15, lataSim: L15, lataSim2: L15,
  taca: L15, giroCel: L15, cilindroH: L15, esferaOct: L15, lataParede: [-1.5, 2, -1.5, 1.5],
  cmPontos: [-.5, 2.5, -.5, 2.5], distEixo: [-.5, 2, -.5, 2]
};

window.setEstado = e => {
  if (G) { S.remove(G); G.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.material) o.material.dispose(); }); }
  G = new T.Group(); S.add(G); PTS = {}; SEGS = [];
  aplicaCam(e.cam);
  const v = (k, d = 0) => (e[k] ?? d);

  if (K === 'lataGiro' || K === 'lataPesada') {
    SC = 2.2; lataPesadaMalha(); eixoZ(0, 1.45); setasXY();
    const defSeta = K === 'lataGiro' ? 1 : 0;
    giroSeta(0, 0, 1.32, .32, GEO, v('seta', defSeta) > .5);
  }

  if (K === 'lataDuas') {
    SC = 2.2;
    if (v('traco', 1) < .5) lataPesadaMalha();
    else lataTraco(1, 1, { nv: 12 });
    eixoZ(-.1, 1.45);
    const a1 = -PI * .30, a2 = a1 + PI / 8, b1 = -PI * .12, b2 = b1 + PI / 10;
    const c1 = v('cel1', 2), c2 = v('cel2', 1);
    if (c1 > 1e-3) celC(.12, .12 + .20 * sm(Math.min(1, c1)), a1, a2, .04, .24);
    if (c2 > 1e-3) celC(.8, .8 + .20 * sm(Math.min(1, c2)), b1, b2, .8, 1);
    if (c1 > 1.05) {
      const kf = sm(c1 - 1);
      tracejado([Wp(0, 0, .14), WC(.12 * kf, (a1 + a2) / 2, .14)], .010, SOMB, .05, .04);
      tracejado([Wp(0, 0, .9), WC(.8 * kf, (b1 + b2) / 2, .9)], .010, SOMB, .07, .05);
    }
    proj('c1', WC(.32, a1, .14)); proj('c2', WC(1.02, (b1 + b2) / 2, .9));
    proj('f1', WC(.06, (a1 + a2) / 2, .18)); proj('f2', WC(.4, (b1 + b2) / 2, .9));
  }

  if (K === 'cmPontos') {
    SC = 1.2; eixos3(SC * 2.4, SC * 2.4, SC * 1.9);
    const B = [[[2.4, 2.0, .4], 1], [[2.3, .4, 1.1], 3], [[.4, 2.4, 1.8], 2]];
    let mt = 0, cm = [0, 0, 0];
    B.forEach(([p, m], i) => {
      const kb = sm(v('b' + (i + 1), 1));
      if (kb > 1e-3) {
        bolinha(Wp(...p), CI, .075 * Math.cbrt(m) * SC * kb);
        tracejado([Wp(p[0], p[1], 0), Wp(p[0], p[1], (p[2] - .09 * Math.cbrt(m)) * kb)], .006, GEO, .06, .05);
      }
      mt += m; cm = cm.map((val, idx) => val + m * p[idx]);
    });
    cm = cm.map(val => val / mt);
    B.forEach(([p], i) => proj('m' + (i + 1), Wp(...p)));
    const kcm = sm(v('cm', 1));
    if (kcm > 1e-3) tracejado([Wp(cm[0], cm[1], 0), Wp(cm[0], cm[1], cm[2] * kcm)], .006, E2, .06, .05);
    proj('cm', Wp(...cm)); proj('cmChao', Wp(cm[0], cm[1], 0));
  }

  if (K === 'lataCel') {
    SC = 2.2; lataTraco(1, 1, { nv: 12 }); eixoZ(-.1, 1.45); setasXY();
    const t1 = -PI * .30, t2 = t1 + PI / 10, s1 = .62, s2 = .82, z1 = .55, z2 = .75;
    if (v('cel', 1) > 1e-3) celC(s1, s1 + (s2 - s1) * sm(v('cel', 1)), t1, t2, z1, z2);
    const tm = (t1 + t2) / 2, sm_ = (s1 + s2) / 2, P0 = cyl(sm_, tm, 0);
    const kf = sm(v('fios', 1));
    if (kf > 1e-3) {
      tracejado([Wp(0, 0, .002), Wp(P0[0] * kf, 0, .002)], .010, E1, .06, .05);
      tracejado([Wp(P0[0], 0, .002), Wp(P0[0], P0[1] * kf, .002)], .010, E2, .06, .05);
      tracejado([Wp(P0[0], P0[1], 0), Wp(P0[0], P0[1], z1 * kf)], .010, EZ, .06, .05);
    }
    proj('cel', WC(s2 + .06, tm, (z1 + z2) / 2));
    proj('px', Wp(P0[0] / 2, 0, 0)); proj('py', Wp(P0[0], P0[1] / 2, 0)); proj('pz', Wp(P0[0], P0[1], z1 / 2));
  }

  if (K === 'lataPlano') {
    SC = 2.2; lataTraco(1, 1, { nv: 12 }); eixoZ(-.1, 1.45); const zb = .555, L = .85;
    if (v('plano', 1) > 1e-3) {
      const kp = sm(v('plano', 1)), Lk = L * kp;
      tubo([Wp(-Lk, -Lk, zb), Wp(Lk, -Lk, zb), Wp(Lk, Lk, zb), Wp(-Lk, Lk, zb), Wp(-Lk, -Lk, zb)], .008, MEN_);
      tubo(arco(t => WC(1, t, zb), 0, 2 * PI * kp, Math.max(8, Math.round(120 * kp))), .006, MEN_);
    }
    const a1 = -PI * .32, a2 = a1 + PI / 10, b1 = -PI * .10, b2 = b1 + PI / 10;
    if (v('celA', 1) > 1e-3) celC(.7, .9, a1, a2, .82, .97);
    if (v('celB', 1) > 1e-3) celC(.45, .65, b1, b2, .10, .25);
    const kf = sm(v('fios', 1));
    if (kf > 1e-3) {
      tracejado([WC(.8, (a1 + a2) / 2, .82), WC(.8, (a1 + a2) / 2, .82 + (zb - .82) * kf)], .010, EZ, .05, .04);
      tracejado([WC(.55, (b1 + b2) / 2, .25), WC(.55, (b1 + b2) / 2, .25 + (zb - .25) * kf)], .010, EZ, .05, .04);
    }
    proj('cA', WC(.92, (a1 + a2) / 2, .9)); proj('cB', WC(.67, (b1 + b2) / 2, .17));
    proj('fA', WC(.8, (a1 + a2) / 2, (.82 + zb) / 2)); proj('fB', WC(.55, (b1 + b2) / 2, (.25 + zb) / 2));
    proj('plano', Wp(L, -L * .2, zb)); proj('zbar', Wp(0, 0, zb)); proj('ponta', Wp(L, L, zb));
  }

  if (K === 'lataSim' || K === 'lataSim2') {
    SC = 2.2; lataTraco(1, 1, { nv: 12 }); eixoZ(-.1, 1.45); setasXY(1.30);
    const kd = K === 'lataSim2' ? sm(v('disco', 1)) : 0;
    if (kd > 1e-3) sup((r, t) => WC(r, t, 0), 0, 1, 0, 2 * PI, 12, 96, (r, t) => mixc(BG, LI, .88 * kd * (1 + r * Math.cos(t)) / 2));
    const t0 = -PI * .18, d = PI / 10, s1 = .6, s2 = .8, z1 = .4, z2 = .6;
    const claro = K === 'lataSim2' && v('lado', 1) > .5;
    if (K === 'lataSim2' || v('gemeos', 1) > 1e-3) {
      celC(s1, s2, t0, t0 + d, z1, z2, claro ? '#E9FF9E' : LI);
      celC(s1, s2, t0 + PI, t0 + PI + d, z1, z2, claro ? '#7E9A3A' : LI);
    }
    const kf = K === 'lataSim2' ? 1 : sm(v('fios', 1));
    if (kf > 1e-3) {
      tracejado([Wp(0, 0, .5), WC(s1 * kf, t0 + d / 2, .5)], .010, SOMB, .06, .05);
      tracejado([Wp(0, 0, .5), WC(s1 * kf, t0 + PI + d / 2, .5)], .010, SOMB, .06, .05);
    }
    proj('cA', WC(s2 + .08, t0 + d / 2, .5)); proj('cB', WC(s2 + .08, t0 + PI + d / 2, .5));
  }

  if (K === 'taca') {
    SC = 2.2; const ta = -PI / 2, tb = 0;
    sup((t, s) => WC(s, t, s * s), tb, ta + 2 * PI, 0, 1, 96, 20, (t, s) => tom(GEO, [2 * s * Math.cos(t), 2 * s * Math.sin(t), -1], .14, .24));
    sup((s, t) => WC(s, t, 1), 0, 1, tb, ta + 2 * PI, 12, 90, () => mixc(BG, GEO, .34));
    for (const t of [ta, tb]) sup((s, z) => WC(s, t, s * s + (1 - s * s) * z), 0, 1, 0, 1, 30, 30, (s, z) => mixc(BG, GEO, t === tb ? .46 : .40));
    for (const t of [ta, tb]) { tubo(arco(s => WC(s, t, s * s), 0, 1, 40), .009, GEO); tubo([WC(0, t, 1), WC(1, t, 1)], .009, GEO); }
    tubo(arco(t => WC(1, t, 1), tb, ta + 2 * PI, 120), .009, GEO);
    tubo(arco(t => WC(1, t, 0), 0, 2 * PI, 120), .006, '#6C7698');
    eixoZ(-.05, 1.45);
    const ss = .6, tt = -.04, ks = sm(v('sonda', 1));
    if (ks > 1e-3) {
      tracejado([WC(ss, tt, 0), WC(ss, tt, ss * ss)], .008, AZC, .05, .04);
      const z1 = ss * ss + (1 - ss * ss) * ks;
      tubo([WC(ss, tt, ss * ss), WC(ss, tt, z1)], .012, '#E8ECF8');
      bolinha(WC(ss, tt, ss * ss), AZC, .035 * SC);
      if (ks >= .999) bolinha(WC(ss, tt, 1), CORAL, .035 * SC);
    }
    proj('entra', WC(ss, tt, ss * ss)); proj('sai', WC(ss, tt, 1));
    proj('z23', Wp(0, 0, 2 / 3)); proj('z12', Wp(0, 0, .5));
    proj('borda', WC(1, PI * .75, 1)); proj('fundoT', Wp(0, 0, 0));
  }

  if (K === 'giroCel') {
    SC = 2.2; lataTraco(1, 1, { nv: 12 }); eixoZ(-.25, 1.45, EZ, .016);
    giroSeta(0, 0, 1.38, .32, GEO, v('seta', 1) > .5);
    const t1 = -PI * .05, t2 = t1 + PI / 10, tm = (t1 + t2) / 2;
    if (v('cel', 1) > 1e-3) celC(.85, 1, t1, t2, .45, .65);
    const kf = sm(v('fio', 1));
    if (kf > 1e-3) tracejado([Wp(0, 0, .55), WC(.85 * kf, tm, .55)], .010, SOMB, .07, .05);
    const P0 = WC(1.0, tm, .55), tg = [-Math.sin(tm), Math.cos(tm), 0];
    const kv = sm(v('v', 1));
    if (kv > 1e-3) seta(P0, [P0[0] + tg[0] * .9 * kv, P0[1] + tg[1] * .9 * kv, P0[2]], .010, BR);
    proj('cel', WC(1.04, tm, .62)); proj('fio', WC(.45, tm, .55)); proj('v', [P0[0] + tg[0] * .95, P0[1] + tg[1] * .95, P0[2]]);
  }

  if (K === 'distEixo') {
    SC = 1.3; eixos3(SC * 2.3, SC * 2.3, SC * 1.9); const P = [1, 1.2, 1];
    if (v('P', 1) > 1e-3) {
      bolinha(Wp(...P), BR, .045 * SC);
      tracejado([Wp(1, 1.2, 0), Wp(...P)], .005, '#6C7698', .05, .05);
      tracejado([Wp(0, 0, 0), Wp(1, 1.2, 0)], .005, '#6C7698', .05, .05);
    }
    const ks = sm(v('s', 1)), kx = sm(v('fioX', 1)), kr = sm(v('r', 1));
    if (ks > 1e-3) tracejado([Wp(0, 0, 1), Wp(P[0] * ks, P[1] * ks, 1)], .010, SOMB, .07, .05);
    if (kx > 1e-3) tracejado([Wp(1, 0, 0), Wp(1, P[1] * kx, P[2] * kx)], .008, GEO, .06, .05);
    if (kr > 1e-3) tubo([Wp(0, 0, 0), Wp(P[0] * kr, P[1] * kr, P[2] * kr)], .012, RO);
    proj('P', Wp(...P)); proj('s', Wp(.5, .6, 1)); proj('fx', Wp(1, .6, .5)); proj('r', Wp(.5, .6, .5)); proj('pe', Wp(0, 0, 1));
  }

  if (K === 'cilindroH') {
    SC = 1.9; const Hh = 1.4;
    lataTraco(1, Hh, { nv: 12 });                                           // a lata em traço: 12 geratrizes e dois aros
    const sc = v('casca', 0);
    if (sc > 1e-3) {                                                        // casca opaca pêssego de raio s e altura h inteira, com aro no topo e na base
      sup((t, z) => WC(sc, t, z), 0, 2 * PI, 0, Hh, 96, 4, (t, z) => tom(SOMB, [Math.cos(t), Math.sin(t), 0], .50, .40));
      for (const z of [0, Hh]) tubo(arco(t => WC(sc, t, z), 0, 2 * PI, 90), .011, SOMB);
    }
    tubo([WC(0, 0, Hh + .006), WC(1, PI * .08, Hh + .006)], .010, GEO);
    tubo([WC(1, -PI * .47, 0), WC(1, -PI * .47, Hh)], .014, EZ);
    eixoZ(-.1, Hh + .35);
    proj('s', WC(.55 * .55, -PI * .30, Hh)); proj('R', WC(.7, PI * .08, Hh)); proj('h', WC(1, -PI * .47, Hh / 2));
  }

  if (K === 'esferaOct') {
    SC = 1.9; const inOct = (t, f) => (Math.cos(t) > 1e-6 && Math.sin(t) < -1e-6 && f < PI / 2);
    const F = (f, t) => WS(1, f, t); const tris = []; const nf = 48, nt = 96;
    for (let i = 0; i < nf; i++) for (let j = 0; j < nt; j++) {
      const f0 = PI * i / nf, f1 = PI * (i + 1) / nf, t0 = 2 * PI * j / nt, t1 = 2 * PI * (j + 1) / nt, fm = (f0 + f1) / 2, tm = (t0 + t1) / 2;
      if (inOct(tm, fm)) continue;
      const cc = tom(GEO, sph(1, fm, tm), .12, .26); tris.push([F(f0, t0), F(f1, t0), F(f1, t1), cc], [F(f0, t0), F(f1, t1), F(f0, t1), cc]);
    }
    malhaTri(tris);
    sup((a, r) => Wp(r * Math.cos(a), 0, r * Math.sin(a)), 0, PI / 2, 0, 1, 30, 12, () => mixc(BG, GEO, .48));
    sup((a, r) => Wp(0, -r * Math.cos(a), r * Math.sin(a)), 0, PI / 2, 0, 1, 30, 12, () => mixc(BG, GEO, .38));
    sup((a, r) => Wp(r * Math.cos(a), -r * Math.sin(a), 0), 0, PI / 2, 0, 1, 30, 12, () => mixc(BG, GEO, .30));
    tubo(arco(a => Wp(Math.cos(a), 0, Math.sin(a)), 0, PI / 2, 40), .007, GEO);
    tubo(arco(a => Wp(0, -Math.cos(a), Math.sin(a)), 0, PI / 2, 40), .007, GEO);
    tubo(arco(a => Wp(Math.cos(a), -Math.sin(a), 0), 0, PI / 2, 40), .007, GEO);
    const rr = .85, ff = PI * .31, Pp = [rr * Math.sin(ff), 0, rr * Math.cos(ff)];
    const kr = sm(v('r', 1)), kf = sm(v('fio', 1)), kp = sm(v('phi', 1));
    if (kr > 1e-3) tubo([Wp(0, 0, 0), Wp(Pp[0] * kr, 0, Pp[2] * kr)], .012, RO);
    if (v('P', 1) > 1e-3) bolinha(Wp(...Pp), BR, .04 * SC);
    if (kf > 1e-3) tracejado([Wp(0, 0, Pp[2]), Wp(Pp[0] * kf, 0, Pp[2])], .010, SOMB, .05, .04, true);
    if (kp > 1e-3) tubo(arco(a => Wp(.42 * Math.sin(a), 0, .42 * Math.cos(a)), 0, ff * kp, 24), .008, FI);
    eixoZ(-.02, 1.45);
    proj('P', Wp(...Pp)); proj('r', Wp(Pp[0] * .55, 0, Pp[2] * .55));
    proj('phi', Wp(.30 * Math.sin(ff / 2), 0, .30 * Math.cos(ff / 2)));
    proj('s', Wp(Pp[0] / 2, 0, Pp[2])); proj('R', Wp(.72, -.72, 0));
  }

  if (K === 'lataParede') {
    SC = 2.2; lataTraco(1, 1, { nv: 12 }); tubo([Wp(0, 0, -.1), Wp(0, 0, 1.45)], .006, '#6C7698');
    const ke = sm(v('eixo', 1));
    if (ke > 1e-3) tracejado([Wp(1, 0, -.25), Wp(1, 0, -.25 + 1.85 * ke)], .014, AL, .08, .05);
    giroSeta(1, 0, 1.38, .30, GEO, v('seta', 1) > .5);
    proj('reta', Wp(1, 0, 1.65)); proj('ez0', Wp(0, 0, 1.5));
  }

  if (PISOK[K]) piso(...PISOK[K]);
  const xmax = (e.cam && e.cam.cx < 400) ? 720 : 975;
  R.setScissorTest(false); R.clear(); R.setScissorTest(true);
  R.setScissor(Math.round(60 * ESC), 0, Math.round((xmax - 60) * ESC), H);
  R.render(S, cam);
  return PTS;
};
window.segsPx = () => SEGS.map(pl => pl.map(v => { const q = new T.Vector3(...v).project(cam); return [+((q.x + 1) / 2 * 1920).toFixed(1), +((1 - q.y) / 2 * 1080).toFixed(1)]; }));
window.cenaPronta = true;
