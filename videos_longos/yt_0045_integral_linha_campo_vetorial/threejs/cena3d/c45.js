// yt_0045 · cenas 3D (porte de referencia/yt_0045_quadros_alvo_v1/c3d45.html, three.js r128; helpers do c44.js do yt_0044 ← c43.js do yt_0043).
// Uma página por cena (<cena>.html) define window.CENA_ID. Opaco, sem luz, tom fixo por face; câmera e recorte G3 (clip) vêm do Manim no estado.
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
function piso(a0, a1, b0, b1, off = -.004, step = .5, cor = '#4A5080', r = .0032) {
  NOSEG = true;
  const n0 = Math.round((a1 - a0) / step), n1 = Math.round((b1 - b0) / step);
  for (let i = 0; i <= n0; i++) { const a = a0 + i * step; tubo([Wp(a, b0, off), Wp(a, b1, off)], r * SC, cor); }
  for (let j = 0; j <= n1; j++) { const b = b0 + j * step; tubo([Wp(a0, b, off), Wp(a1, b, off)], r * SC, cor); }
  NOSEG = false;
}

// ===================== cenas do yt_0044 (porte de referencia/yt_0044_quadros_alvo_v1/c3d44.html, mesmos parâmetros e cores) =====================
const LIL = '#B9A6FF', HEL = '#FFB36B', ESCU = '#0F0C26';
// lata uniforme opaca (GEO) com centro (cx, 0), raio 1, altura 1
function lataSolida(cx = 0) {
  const Cc = (s, t, z) => Wp(cx + s * Math.cos(t), s * Math.sin(t), z); const svc = NOSEG; NOSEG = true;
  sup((t, z) => Cc(1, t, z), 0, 2 * PI, 0, 1, 96, 4, (t, z) => tom(GEO, [Math.cos(t), Math.sin(t), 0], .10, .20));
  sup((s, t) => Cc(s, t, 1), 0, 1, 0, 2 * PI, 8, 72, () => mixc(BG, GEO, .28));
  NOSEG = svc;
  for (const z of [0, 1]) tubo(arco(t => Cc(1, t, z), 0, 2 * PI, 120), .009, GEO);
}
function giroSeta44(cx, cy, zz, rr = .32, cor = GEO) {
  const A = arco(t => Wp(cx + rr * Math.cos(t), cy + rr * Math.sin(t), zz), -PI * .9, PI * .55, 60); tubo(A, .010, cor);
  const a1 = Wp(cx + rr * Math.cos(PI * .55), cy + rr * Math.sin(PI * .55), zz), a0 = Wp(cx + rr * Math.cos(PI * .48), cy + rr * Math.sin(PI * .48), zz); seta(a0, a1, .010, cor);
}
function caixa(x0, x1, y0, y1, z0, z1, corF) {
  const F = [[n => Wp(x1, n[0], n[1]), [y0, y1, z0, z1], [1, 0, 0]], [n => Wp(x0, n[0], n[1]), [y0, y1, z0, z1], [-1, 0, 0]], [n => Wp(n[0], y0, n[1]), [x0, x1, z0, z1], [0, -1, 0]],
  [n => Wp(n[0], y1, n[1]), [x0, x1, z0, z1], [0, 1, 0]], [n => Wp(n[0], n[1], z1), [x0, x1, y0, y1], [0, 0, 1]], [n => Wp(n[0], n[1], z0), [x0, x1, y0, y1], [0, 0, -1]]];
  for (const [f, [a0, a1, b0, b1], nn] of F) sup((a, b) => f([a, b]), a0, a1, b0, b1, 1, 1, () => corF(nn));
}
function arestasCaixa(x0, x1, y0, y1, z0, z1, cor, w = .006) {
  const P = [[x0, y0], [x1, y0], [x1, y1], [x0, y1], [x0, y0]];
  for (const z of [z0, z1]) tubo(P.map(([a, b]) => Wp(a, b, z)), w, cor); for (const [a, b] of P.slice(0, 4)) tubo([Wp(a, b, z0), Wp(a, b, z1)], w, cor);
}
function tri(A, B, Cc, cor, n = 24) {
  const pt = (a, b) => [0, 1, 2].map(i => A[i] + a * ((1 - b) * (B[i] - A[i]) + b * (Cc[i] - A[i])));
  sup((a, b) => Wp(...pt(a, b)), 0, 1, 0, 1, n, n, (a, b) => cor(pt(a, b)));
}
const corRho3 = (p, mx) => mixc(RAMP0, CI, Math.pow(Math.min(1, (p[0] + p[1] + p[2]) / mx), 1.5));
const hexc = c => '#' + c.getHexString();

window.setEstado = e => {
  if (G) { S.remove(G); G.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.material) o.material.dispose(); }); }
  G = new T.Group(); S.add(G); PTS = {}; SEGS = [];
  aplicaCam(e.cam);
  const v = (k, d = 0) => (e[k] ?? d);

  // ===================== cenas do yt_0045 (porte de referencia/yt_0045_quadros_alvo_v1/c3d45.html: mesmos parâmetros, câmera e cores) =====================
  const CAMPO = '#2EE6A0';
  const HX = t => WC(1.012, t, t / (4 * PI));                 // lata do canal: raio 1, altura 1, duas voltas ⇒ c = 1/(4π)
  const Fh = t => [-Math.sin(t), Math.cos(t), -1];             // F(γ(t)) = (−y, x, −1) na hélice
  const setaF = (t, k, r) => { const P0 = HX(t), f = Fh(t); const P1 = [P0[0] + SC * k * f[0], P0[1] + SC * k * f[1], P0[2] + SC * k * f[2]]; seta(P0, P1, r, CAMPO); return P1; };

  // ---------- H1: a hélice inteira (duas voltas) cresce; conta em t = 1,8π; força F verde-menta (k = 0,42) ----------
  if (K === 'helice') {
    SC = 2.2; lataTraco(1, 1, { nv: 12 }); eixoZ(-.1, 1.45);
    const kh = sm(v('helice', 1));
    if (kh > 1e-3) tubo(arco(HX, 0, 4 * PI * kh, Math.max(8, Math.round(400 * kh))), .014, HEL);
    const tc = PI * 1.80, P0 = HX(tc), f = Fh(tc), k = .42, P1 = [P0[0] + SC * k * f[0], P0[1] + SC * k * f[1], P0[2] + SC * k * f[2]];
    if (v('conta', 1) > .5) bolinha(P0, BR, .05 * SC);
    const kF = sm(v('F', 1));
    if (kF > 1e-3) seta(P0, [P0[0] + (P1[0] - P0[0]) * kF, P0[1] + (P1[1] - P0[1]) * kF, P0[2] + (P1[2] - P0[2]) * kF], .011, CAMPO);
    proj('conta', P0); proj('F', P1); proj('hel', HX(PI * 3.1));
  }

  // ---------- B7: a 1ª volta (0 ≤ t ≤ 2π) cresce em laranja; a 2ª já em traço apagado; 5 setas de F (k = 0,24) entram juntas ----------
  if (K === 'heliceCampo' || K === 'heliceLeitura') {
    SC = 2.2; lataTraco(1, 1, { nv: 12 }); eixoZ(-.1, 1.45);
    const kh = sm(v('helice', 1));
    if (kh > 1e-3) tubo(arco(HX, 0, 2 * PI * kh, Math.max(8, Math.round(220 * kh))), .016, HEL);
    tubo(arco(HX, 2 * PI, 4 * PI, 220), .008, TR);
    if (v('t0', 1) > .5) bolinha(HX(0), BR, .03 * SC);
    if (v('t2pi', 1) > .5) bolinha(HX(2 * PI), BR, .03 * SC);
    proj('t0', HX(0)); proj('t2pi', HX(2 * PI));
    const ks = sm(v('setas', 1));
    [.80, 1.08, 1.36, 1.64, 1.92].forEach((m, i) => {
      const t = m * PI, P0 = HX(t), f = Fh(t), k = .24, P1 = [P0[0] + SC * k * f[0], P0[1] + SC * k * f[1], P0[2] + SC * k * f[2]];
      if (ks > 1e-3) seta(P0, [P0[0] + (P1[0] - P0[0]) * ks, P0[1] + (P1[1] - P0[1]) * ks, P0[2] + (P1[2] - P0[2]) * ks], .013, CAMPO);
      proj('F' + i, P1);
    });
    if (K === 'heliceLeitura') {
      const kt = sm(v('tampa', 1));
      if (kt > 1e-3) tubo(arco(t => WC(1.0, t, 0.003), 0, 2 * PI * kt, Math.max(8, Math.round(160 * kt))), .016, LI);   // contorno da tampa de baixo (área π·1²)
      const ku = sm(v('subida', 1)), a = 0;
      if (ku > 1e-3) {
        tubo([WC(1.10, a, 0), WC(1.10, a, .5 * ku)], .012, EZ); tubo([WC(1.04, a, 0), WC(1.16, a, 0)], .010, EZ);
        if (ku > .999) tubo([WC(1.04, a, .5), WC(1.16, a, .5)], .010, EZ);
      }
      proj('sub', WC(1.18, a, .25)); proj('tampa', WC(1.0, -.62 * PI, 0));
    }
    proj('hel', HX(PI * 1.6));
  }

  const L15 = [-1.5, 1.5, -1.5, 1.5];
  const PISOK = { helice: L15, heliceCampo: L15, heliceLeitura: L15 };
  if (PISOK[K]) piso(...PISOK[K]);
  const xmax = e.clip || 975;
  R.setScissorTest(false); R.clear(); R.setScissorTest(true);
  R.setScissor(Math.round(60 * ESC), 0, Math.round((xmax - 60) * ESC), H);
  R.render(S, cam);
  return PTS;
};
window.segsPx = () => SEGS.map(pl => pl.map(v => { const q = new T.Vector3(...v).project(cam); return [+((q.x + 1) / 2 * 1920).toFixed(1), +((1 - q.y) / 2 * 1080).toFixed(1)]; }));
window.cenaPronta = true;
