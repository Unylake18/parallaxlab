// yt_0044 · cenas 3D (porte de referencia/yt_0044_quadros_alvo_v1/c3d44.html, three.js r128; helpers do c43.js do yt_0043).
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
  proj('ex', [lx + .10, 0, 0]); proj('ey', [0, ly + .10, 0]); proj('ez', [0, 0, lz + .12]);
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
function eixoZ(z0 = -.1, z1 = 1.45, cor = EZ, r = .010) { tubo([Wp(0, 0, z0), Wp(0, 0, z1)], r, cor); proj('ez', Wp(0, 0, z1 + .08)); }
function setasXY(lx = 1.55) { seta([SC * 1.03, 0, 0], [SC * lx, 0, 0], .012, E1); seta([0, SC * 1.03, 0], [0, SC * 1.55, 0], .012, E2); proj('ex', [SC * (lx + .13), 0, 0]); proj('ey', [0, SC * 1.68, 0]); }
function giroSeta(cx, cy, zz, rr = .32, cor = GEO, desenha = true) {
  if (desenha) {
    const A = arco(t => Wp(cx + rr * Math.cos(t), cy + rr * Math.sin(t), zz), -PI * .9, PI * .55, 60); tubo(A, .010, cor);
    const a1 = Wp(cx + rr * Math.cos(PI * .55), cy + rr * Math.sin(PI * .55), zz), a0 = Wp(cx + rr * Math.cos(PI * .48), cy + rr * Math.sin(PI * .48), zz); seta(a0, a1, .010, cor);
  }
  proj('giro', Wp(cx + rr, cy, zz)); proj('omega', Wp(cx + rr * Math.cos(-PI * .35), cy + rr * Math.sin(-PI * .35), zz));
}
function piso(a0, a1, b0, b1, off = -.03, step = .5, cor = '#3E4474', r = .0030) {   // v2 (G2): finito, só em volta da peça, com moldura; abaixo das faces
  NOSEG = true;
  const n0 = Math.round((a1 - a0) / step), n1 = Math.round((b1 - b0) / step);
  for (let i = 1; i < n0; i++) { const a = a0 + i * step; tubo([Wp(a, b0, off), Wp(a, b1, off)], r * SC, cor); }
  for (let j = 1; j < n1; j++) { const b = b0 + j * step; tubo([Wp(a0, b, off), Wp(a1, b, off)], r * SC, cor); }
  tubo([Wp(a0, b0, off), Wp(a1, b0, off), Wp(a1, b1, off), Wp(a0, b1, off), Wp(a0, b0, off)], r * 1.5 * SC, '#545A8C');
  NOSEG = false;
}

// F1 (handoff final): piso octogonal regular (apótema ap) centrado em (cx, cy), grade a cada 0,5 a partir da origem recortada pelo octógono e moldura fechando nele
function pisoOct(cx, cy, ap, off = -.03, step = .5, cor = '#3E4474', r = .0030) {
  NOSEG = true;
  const Rv = ap / Math.cos(PI / 8), V = [];
  for (let k = 0; k < 8; k++) { const th = PI / 8 + k * PI / 4; V.push([cx + Rv * Math.cos(th), cy + Rv * Math.sin(th)]); }
  const clip = (P, D) => {   // Cyrus–Beck contra o octógono convexo (anti-horário)
    let t0 = 0, t1 = 1;
    for (let k = 0; k < 8; k++) {
      const A = V[k], B = V[(k + 1) % 8], nx = -(B[1] - A[1]), ny = B[0] - A[0];
      const num = nx * (A[0] - P[0]) + ny * (A[1] - P[1]), den = nx * D[0] + ny * D[1];
      if (Math.abs(den) < 1e-12) { if (num > 0) return null; continue; }
      const t = num / den; if (den > 0) t1 = Math.min(t1, t); else t0 = Math.max(t0, t);
    }
    return t0 < t1 - 1e-6 ? [[P[0] + D[0] * t0, P[1] + D[1] * t0], [P[0] + D[0] * t1, P[1] + D[1] * t1]] : null;
  };
  const ext = ap * 2 + 2;
  for (let i = Math.ceil((cx - ap * 1.2) / step); i <= Math.floor((cx + ap * 1.2) / step); i++) {
    const a = i * step, c = clip([a, cy - ext], [0, 2 * ext]); if (c) tubo([Wp(c[0][0], c[0][1], off), Wp(c[1][0], c[1][1], off)], r * SC, cor);
  }
  for (let j = Math.ceil((cy - ap * 1.2) / step); j <= Math.floor((cy + ap * 1.2) / step); j++) {
    const b = j * step, c = clip([cx - ext, b], [2 * ext, 0]); if (c) tubo([Wp(c[0][0], c[0][1], off), Wp(c[1][0], c[1][1], off)], r * SC, cor);
  }
  tubo([...V, V[0]].map(q => Wp(q[0], q[1], off)), r * 1.5 * SC, '#545A8C');
  NOSEG = false;
}

// ===================== cenas do yt_0044 (porte de referencia/yt_0044_quadros_alvo_v1/c3d44.html v2, mesmos parâmetros e cores) =====================
const LIL = '#B9A6FF', HEL = '#FFB36B', ESCU = '#0F0C26', COTA = '#C9D2E6';
// lata uniforme opaca (GEO) com centro (cx, 0), raio 1, altura 1
function lataSolida(cx = 0) {
  const Cc = (s, t, z) => Wp(cx + s * Math.cos(t), s * Math.sin(t), z); const svc = NOSEG; NOSEG = true;
  sup((t, z) => Cc(1, t, z), 0, 2 * PI, 0, 1, 96, 4, (t, z) => tom(GEO, [Math.cos(t), Math.sin(t), 0], .10, .20));
  sup((s, t) => Cc(s, t, 1), 0, 1, 0, 2 * PI, 8, 72, () => mixc(BG, GEO, .28));
  NOSEG = svc;
  for (const z of [0, 1]) tubo(arco(t => Cc(1, t, z), 0, 2 * PI, 120), .009, GEO);
}
// cota (G10): segmento fino com dois tiques nas pontas, fora da peça; o rótulo vai no ponto `nome` (meio, deslocado para fora). show = false só projeta o ponto
function cota(A, B, nome, fora = [0, 0, 0], cor = COTA, show = true) {
  let t = [fora[0], fora[1], fora[2]]; const tl = Math.hypot(...t) || 1; t = t.map(x => x / tl * .06);
  if (show) {
    tubo([Wp(...A), Wp(...B)], .006, cor);
    for (const P of [A, B]) tubo([Wp(P[0] - t[0], P[1] - t[1], P[2] - t[2]), Wp(P[0] + t[0], P[1] + t[1], P[2] + t[2])], .006, cor);
  }
  proj(nome, Wp((A[0] + B[0]) / 2 + t[0] * 2.2, (A[1] + B[1]) / 2 + t[1] * 2.2, (A[2] + B[2]) / 2 + t[2] * 2.2));
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

  // ---------- H1: lata uniforme; eixo central (azul) curto acima da tampa, reta da parede (ALERTA) tracejada, seta de giro ACIMA da tampa, cota 2R no chão ----------
  if (K === 'lataParede') {
    SC = 2.2; lataSolida(0);
    const ke = sm(v('eixo', 1)), kp = sm(v('parede', 1));
    if (ke > 1e-3) tubo([Wp(0, 0, 1.0), Wp(0, 0, 1.0 + .5 * ke)], .011, EZ);
    if (kp > 1e-3) tracejado([Wp(1, 0, -.15), Wp(1, 0, -.15 + 1.9 * kp)], .013, AL, .08, .05);
    if (v('seta', 1) > .5) giroSeta44(1, 0, 1.6, .22, AL);
    cota([-1, -1.25, 0], [1, -1.25, 0], 'd2R', [0, -1, 0], COTA, v('cota', 1) > .5);
    proj('ez', Wp(0, 0, 1.58)); proj('O', Wp(0, 0, 0)); proj('reta', Wp(1, 0, 2.02));
  }

  // ---------- E5: a mesma lata, centro em (1, 0); o eixo z (azul) na parede ----------
  if (K === 'lataDobradica' || K === 'lataDob3') {
    SC = 2.2; lataSolida(1);
    const ke = sm(v('eixo', 1));
    if (ke > 1e-3) tubo([Wp(0, 0, -.15), Wp(0, 0, -.15 + 1.9 * ke)], .012, EZ);
    if (v('seta', 1) > .5) giroSeta44(0, 0, 1.6, .22, EZ);
    if (K === 'lataDob3') {
      const sc = .55, k1 = sm(v('p1', 0)), k2 = sm(v('p2', 0)), k3 = sm(v('p3', 0));
      if (k1 > 1e-3) { tubo([Wp(0, 0, 1.01), Wp(k1, 0, 1.01)], .012, LIL); if (k1 > .999) bolinha(Wp(1, 0, 1.01), BR, .03 * SC); }
      if (k2 > 1e-3) {        // ② células gêmeas, simétricas em relação ao centro C (θ e θ + π), no plano da tampa
        const s2 = .6, d = .16 * k2, h = .05;   // F2: s = 0,6 R do centro, θ = 0 e π, em cima da tampa (z = h + 0,005)
        for (const sg of [1, -1]) {
          const cx = 1 + sg * s2, cy = 0, cc = sg > 0 ? LI : '#7E9A3A';
          const svc = NOSEG; NOSEG = true;
          caixa(cx - d / 2, cx + d / 2, cy - d / 2, cy + d / 2, 1.0, 1.0 + h, nn => tom(cc, nn, .45, .40)); NOSEG = svc;
          arestasCaixa(cx - d / 2, cx + d / 2, cy - d / 2, cy + d / 2, 1.0, 1.0 + h, cc, .005);
        }
      }
      if (k3 > 1e-3) {
        tubo(arco(t => Wp(1 + sc * Math.cos(t), sc * Math.sin(t), 1.004), 0, 2 * PI * k3, Math.max(8, Math.round(90 * k3))), .012, SOMB);
        if (k3 > .999) tubo([Wp(1, 0, 1.006), Wp(1 + sc * Math.cos(-PI * .3), sc * Math.sin(-PI * .3), 1.006)], .010, SOMB);
      }
      proj('s', Wp(1 + .5 * sc * Math.cos(-PI * .3) + .12, .5 * sc * Math.sin(-PI * .3) - .14, 1.0)); proj('fioR', Wp(.45, .3, 1.0));
      proj('cmais', Wp(1.232, 1.16, 1.0)); proj('cmenos', Wp(-.127, -.696, 1.0));   // F2: placas fora da tampa, em θ = 0 e π
    }
    proj('ez', Wp(0, 0, 1.83)); proj('O', Wp(0, 0, 0)); proj('Ct', Wp(1, 0, 1)); proj('C', Wp(1, 0, 1.0));
  }

  // ---------- E1: cubo [0,1]³, ρ = x + y + z ----------
  if (K === 'cubo' || K === 'cuboCaixas' || K === 'cuboSonda' || K === 'cuboDiag') {
    SC = 2.0;
    const faces = () => {
      const sv = NOSEG; NOSEG = true;
      sup((x, y) => Wp(x, y, 0), 0, 1, 0, 1, 20, 20, (x, y) => mixc(BG, hexc(corRho3([x, y, 0], 3)), .75));
      sup((y, z) => Wp(0, y, z), 0, 1, 0, 1, 20, 20, (y, z) => mixc(BG, hexc(corRho3([0, y, z], 3)), .70));
      sup((x, z) => Wp(x, 1, z), 0, 1, 0, 1, 20, 20, (x, z) => mixc(BG, hexc(corRho3([x, 1, z], 3)), .80)); NOSEG = sv;
    };
    if (K === 'cuboCaixas') {           // v2: sem a caixa de arame em volta
      const g = .035, sv = NOSEG; NOSEG = true;
      for (const a of [0, .5]) for (const b of [0, .5]) for (const c of [0, .5]) {
        const vv = (a + b + c + .75) / 3, cc = hexc(mixc(RAMP0, CI, Math.pow(vv, 1.3)));
        caixa(a + g, a + .5 - g, b + g, b + .5 - g, c + g, c + .5 - g, nn => tom(cc, nn, .55, .40));
        arestasCaixa(a + g, a + .5 - g, b + g, b + .5 - g, c + g, c + .5 - g, ESCU, .005);
        proj('c' + (a * 2) + (b * 2) + (c * 2), Wp(a + .25, b + .25, c + .5 - g));
      }
      NOSEG = sv;
    }
    if (K === 'cubo') {
      const fc = (p, nn) => mixc(BG, hexc(corRho3(p, 3)), .80 + .20 * Math.max(0, new T.Vector3(...nn).normalize().dot(LDIR)));
      const sv = NOSEG; NOSEG = true;
      sup((y, z) => Wp(1, y, z), 0, 1, 0, 1, 30, 30, (y, z) => fc([1, y, z], [1, 0, 0])); sup((x, z) => Wp(x, 0, z), 0, 1, 0, 1, 30, 30, (x, z) => fc([x, 0, z], [0, -1, 0]));
      sup((x, y) => Wp(x, y, 1), 0, 1, 0, 1, 30, 30, (x, y) => fc([x, y, 1], [0, 0, 1]));
      sup((y, z) => Wp(0, y, z), 0, 1, 0, 1, 4, 4, () => mixc(BG, GEO, .2)); sup((x, z) => Wp(x, 1, z), 0, 1, 0, 1, 4, 4, () => mixc(BG, GEO, .2)); NOSEG = sv;
      arestasCaixa(0, 1, 0, 1, 0, 1, CI, .008);
      const kg = sm(v('grade', 0));
      if (kg > 1e-3) {
        const q = .5, u = kg;
        tubo([Wp(1.003, q, 0), Wp(1.003, q, u)], .005, ESCU); tubo([Wp(1.003, 0, q), Wp(1.003, u, q)], .005, ESCU);
        tubo([Wp(q, -.003, 0), Wp(q, -.003, u)], .005, ESCU); tubo([Wp(0, -.003, q), Wp(u, -.003, q)], .005, ESCU);
        tubo([Wp(q, 0, 1.003), Wp(q, u, 1.003)], .005, ESCU); tubo([Wp(0, q, 1.003), Wp(u, q, 1.003)], .005, ESCU);
      }
    }
    if (K === 'cuboSonda') {            // v2: sem os tracejados no chão
      arestasCaixa(0, 1, 0, 1, 0, 1, GEO, .008); faces();
      const xs = .7, ys = .3, ks = sm(v('sonda', 1));
      if (ks > 1e-3) { tubo([Wp(xs, ys, 0), Wp(xs, ys, ks)], .014, '#E8ECF8'); bolinha(Wp(xs, ys, 0), AZC, .035 * SC); if (ks > .999) bolinha(Wp(xs, ys, 1), CORAL, .035 * SC); }
      proj('entra', Wp(xs, ys, 0)); proj('sai', Wp(xs, ys, 1));
    }
    if (K === 'cuboDiag') {             // v2: sem anel do centro; tique GEO em 1/2 (estado centro); ⊕ em 5/9 é 2D
      arestasCaixa(0, 1, 0, 1, 0, 1, GEO, .008); faces();
      const kd = sm(v('diag', 1));
      if (kd > 1e-3) { tracejado([Wp(0, 0, 0), Wp(kd, kd, kd)], .009, GEO, .07, .05); if (kd > .999) bolinha(Wp(1, 1, 1), CI, .04 * SC); }
      if (v('centro', 1) > .5) { const m = .5, u = [.08, -.08, 0]; tubo([Wp(m - u[0], m - u[1], m), Wp(m + u[0], m + u[1], m)], .010, GEO); }
      proj('centro', Wp(.5, .5, .5)); proj('cm', Wp(5 / 9, 5 / 9, 5 / 9)); proj('t12', Wp(.921, -.061, .5)); proj('t59', Wp(.134, 1.123, .556)); proj('quina', Wp(1, 1, 1));
    }
    eixos3(SC * 1.35, SC * 1.35, SC * 1.3); proj('O', Wp(0, 0, 0)); proj('mid', Wp(.5, .5, 1));
  }

  // ---------- E1-5: a folha z = 1 e UMA camada de altura Δz (v2: sem as 16 caixinhas de arame) ----------
  if (K === 'cuboFolha') {
    SC = 2.0; arestasCaixa(0, 1, 0, 1, 0, 1, TR, .006);
    if (v('folha', 1) > .5) { const sv = NOSEG; NOSEG = true; sup((x, y) => Wp(x, y, 1), 0, 1, 0, 1, 4, 4, () => C(LI)); NOSEG = sv; }
    const dz = .12, kc = v('caixas', 0) > .5;
    if (kc) arestasCaixa(0, 1, 0, 1, 1 - dz / 2, 1 + dz / 2, '#E9FF9E', .006);
    cota([1.12, 0, 1 - dz / 2], [1.12, 0, 1 + dz / 2], 'dz', [1, -.4, 0], COTA, kc);
    eixos3(SC * 1.35, SC * 1.35, SC * 1.3); proj('O', Wp(0, 0, 0)); proj('folha', Wp(.5, .5, 1.05));
  }

  // ---------- E2: tetraedro x+y+z ≤ 1, ρ = x + y, aberto pela face inclinada (v2: câmera fora da diagonal; a base é a sombra) ----------
  if (K === 'tetraSonda' || K === 'tetraCent' || K === 'tetraPlano') {
    SC = 2.4; const svc = NOSEG; NOSEG = true;
    const fc = (p, k) => mixc(BG, hexc(corDens(p[0] + p[1])), k);
    const somb = (K === 'tetraSonda') && v('sombra', 1) > .5;
    tri([0, 0, 0], [1, 0, 0], [0, 1, 0], p => somb ? mixc(BG, SOMB, .55) : fc(p, .85)); tri([0, 0, 0], [1, 0, 0], [0, 0, 1], p => fc(p, .62)); tri([0, 0, 0], [0, 1, 0], [0, 0, 1], p => fc(p, .72));
    NOSEG = svc;
    const V = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]];
    for (const [a, b] of [[1, 2], [1, 3], [2, 3]]) tubo([Wp(...V[a]), Wp(...V[b])], .009, GEO);
    if (K === 'tetraSonda') {
      const xs = .3, ys = .2, zt = 1 - xs - ys, ks = sm(v('sonda', 1));
      if (ks > 1e-3) { tubo([Wp(xs, ys, 0), Wp(xs, ys, zt * ks)], .014, '#E8ECF8'); bolinha(Wp(xs, ys, 0), AZC, .035 * SC); if (ks > .999) bolinha(Wp(xs, ys, zt), CORAL, .035 * SC); }
      proj('entra', Wp(xs, ys, 0)); proj('sai', Wp(xs, ys, zt));
    }
    if (K === 'tetraCent') {
      if (v('vertices', 1) > .5) for (const q of V) bolinha(Wp(...q), BR, .028 * SC);
      const kc = sm(v('centroide', 1));
      if (kc > 1e-3) for (const q of V) tracejado([Wp(.25, .25, .25), Wp(...[0, 1, 2].map(i => .25 + (q[i] - .25) * kc))], .005, GEO, .05, .04);
      proj('cent', Wp(.25, .25, .25)); V.forEach((q, i) => proj('v' + i, Wp(...q)));
    }
    if (K === 'tetraPlano') {
      const kp = sm(v('plano', 1)), z5 = .2, z4 = .25;
      if (kp > 1e-3) {
        tubo([Wp(1 - z5, 0, z5), Wp(0, 1 - z5, z5), Wp(0, 0, z5), Wp(1 - z5, 0, z5)], .010, MEN_);
        tracejado([Wp(1 - z4, 0, z4), Wp(0, 1 - z4, z4), Wp(0, 0, z4), Wp(1 - z4, 0, z4)], .006, GEO, .05, .04);
      }
      proj('z5', Wp(1 - z5, 0, z5)); proj('z4', Wp(0, 0, z4));
    }
    eixos3(SC * 1.3, SC * 1.3, SC * 1.25); proj('O', Wp(0, 0, 0)); proj('vx', Wp(1, 0, 0)); proj('vy', Wp(0, 1, 0)); proj('vz', Wp(0, 0, 1));
  }

  // ---------- E3: cone (vértice na origem), R = 1, h = 1,4; um quarto aberto θ ∈ [−π/2, 0]; R = raio desenhado, h = cota ----------
  if (K === 'cone' || K === 'coneCm' || K === 'coneCasca') {
    SC = 2.0; const Hh = 1.4, ta = -PI / 2, tb = 0, Cc = (s, t, z) => WC(s, t, z); const svc = NOSEG; NOSEG = true;
    sup((t, z) => Cc(z / Hh, t, z), tb, ta + 2 * PI, 0, Hh, 96, 14, (t, z) => tom(GEO, [Math.cos(t), Math.sin(t), -1 / Hh], .12, .24));
    sup((s, t) => Cc(s, t, Hh), 0, 1, tb, ta + 2 * PI, 10, 90, () => mixc(BG, GEO, .30));
    for (const t of [ta, tb]) sup((s, z) => Cc(s, t, Hh * s + (Hh - Hh * s) * z), 0, 1, 0, 1, 20, 20, () => mixc(BG, GEO, t === tb ? .46 : .38));
    NOSEG = svc;
    tubo(arco(t => Cc(1, t, Hh), tb, ta + 2 * PI, 120), .009, GEO); for (const t of [ta, tb]) { tubo([Cc(0, t, 0), Cc(1, t, Hh), Cc(0, t, Hh)], .009, GEO); }
    tubo(arco(t => Cc(1, t, Hh), ta, tb, 30), .005, TR);
    eixoZ(-.05, Hh + .40);
    const tR = PI * .62; tubo([Wp(0, 0, Hh + .006), Cc(1, tR, Hh + .006)], .008, COTA); proj('R', Cc(.55, tR + .22, Hh));
    const cx = Cc(1.2, -PI * .62, 0), P = z => [cx[0] / SC, cx[1] / SC, z];
    if (K === 'coneCm') {
      const kcs = v('cotas', 1) > .5;
      cota(P(0), P(.75 * Hh), 'c34', [1, 0, 0], COTA, kcs); cota(P(.75 * Hh), P(Hh), 'c14', [1, 0, 0], COTA, kcs);
      if (v('cm', 1) > .5) tracejado([Cc(0, 0, .5 * Hh), Cc(.5, -PI * .25, .5 * Hh)], .008, GEO, .05, .04);
      proj('z12', Cc(.72, -PI * .25, .5 * Hh));
    } else cota(P(0), P(Hh), 'h', [1, 0, 0]);
    const ss = .6, tt = -.25, zi = Hh * ss;
    if (K === 'cone') {
      const ks = sm(v('sonda', 1));
      if (ks > 1e-3) { bolinha(Cc(ss, tt, zi), AZC, .035 * SC); tubo([Cc(ss, tt, zi), Cc(ss, tt, zi + (Hh - zi) * ks)], .012, '#E8ECF8'); if (ks > .999) bolinha(Cc(ss, tt, Hh), CORAL, .035 * SC); }
    }
    if (K === 'coneCasca') {
      const sc = .55, kc = sm(v('casca', 1));
      if (kc > 1e-3) {
        const z0 = Hh * sc, z1 = z0 + (Hh - z0) * kc; const sv2 = NOSEG; NOSEG = true;
        sup((t, z) => Cc(sc, t, z), ta, tb, z0, z1, 20, 4, (t, z) => tom(SOMB, [Math.cos(t), Math.sin(t), 0], .55, .35)); NOSEG = sv2;
        if (kc > .999) { tubo(arco(t => Cc(sc, t, Hh + .003), tb, ta + 2 * PI, 90), .009, SOMB); tubo([Cc(0, 0, Hh + .01), Cc(sc, -PI * .25, Hh + .01)], .009, SOMB); giroSeta44(0, 0, Hh + .30, .24); }
      }
      proj('s', Cc(sc * .55, -PI * .25 - .35, Hh)); proj('casca', Cc(sc, -PI / 4, (Hh * sc + Hh) / 2));
    }
    proj('entra', Cc(ss, tt, zi)); proj('sai', Cc(ss, tt, Hh));
    proj('O', Wp(0, 0, 0)); proj('z34', Wp(0, 0, .75 * Hh)); proj('topo', Wp(0, 0, Hh));
  }

  // ---------- E4: meia bola, um quarto aberto (x>0, y<0) ----------
  if (K === 'semi' || K === 'semiFatia') {
    SC = 1.9; const inQ = t => (Math.cos(t) > 1e-6 && Math.sin(t) < -1e-6);
    const F = (f, t) => WS(1, f, t); const tris = []; const nf = 24, nt = 96;
    for (let i = 0; i < nf; i++) for (let j = 0; j < nt; j++) {
      const f0 = PI / 2 * i / nf, f1 = PI / 2 * (i + 1) / nf, t0 = 2 * PI * j / nt, t1 = 2 * PI * (j + 1) / nt, fm = (f0 + f1) / 2, tm = (t0 + t1) / 2; if (inQ(tm)) continue;
      const cc = tom(GEO, sph(1, fm, tm), .12, .26); tris.push([F(f0, t0), F(f1, t0), F(f1, t1), cc], [F(f0, t0), F(f1, t1), F(f0, t1), cc]);
    }
    malhaTri(tris);
    const svq = NOSEG; NOSEG = true;
    sup((a, r) => Wp(r * Math.cos(a), 0, r * Math.sin(a)), 0, PI / 2, 0, 1, 30, 12, () => mixc(BG, GEO, .48));
    sup((a, r) => Wp(0, -r * Math.cos(a), r * Math.sin(a)), 0, PI / 2, 0, 1, 30, 12, () => mixc(BG, GEO, .38)); NOSEG = svq;
    tubo(arco(a => Wp(Math.cos(a), 0, Math.sin(a)), 0, PI / 2, 40), .007, GEO); tubo(arco(a => Wp(0, -Math.cos(a), Math.sin(a)), 0, PI / 2, 40), .007, GEO);
    tubo(arco(t => WC(1, t, 0), 0, 2 * PI, 120), .007, GEO);
    const rr = .85, ff = PI * .36, Pp = [rr * Math.sin(ff), 0, rr * Math.cos(ff)];
    if (K === 'semi') {
      const kP = sm(v('P', 1));
      if (kP > 1e-3) {
        tubo([Wp(0, 0, 0), Wp(Pp[0] * kP, 0, Pp[2] * kP)], .012, RO);
        if (kP > .999) { bolinha(Wp(...Pp), BR, .035 * SC); tracejado([Wp(Pp[0], 0, 0), Wp(...Pp)], .010, EZ, .05, .04); tubo(arco(a => Wp(.30 * Math.sin(a), 0, .30 * Math.cos(a)), 0, ff, 24), .010, FI); }
      }
      proj('P', Wp(...Pp)); proj('r', Wp(Pp[0] * .62 + .07, 0, Pp[2] * .62 - .09)); proj('phi', Wp(.44 * Math.sin(ff * .62), 0, .44 * Math.cos(ff * .62))); proj('z', Wp(Pp[0] + .11, 0, Pp[2] * .45));
    }
    if (K === 'semiFatia') {
      const zf = .8, rf = Math.sqrt(1 - zf * zf), kf = sm(v('fatia', 1));
      if (kf > 1e-3) {
        const sv = NOSEG; NOSEG = true; sup((s, t) => WC(s, t, zf), 0, rf * kf, -PI / 2, 0, 8, 24, () => C(LI)); NOSEG = sv;
        tubo(arco(t => WC(rf * kf + .006, t, zf), 0, 2 * PI, 90), .010, LI);
        if (kf > .999) tubo([Wp(0, 0, zf + .004), WC(rf, -PI * .06, zf + .004)], .011, SOMB);
      }
      proj('raio', WC(rf + .55, -PI * .06, zf + .05)); proj('zf', Wp(0, 0, zf + .17));
    }
    eixoZ(-.02, 1.40); proj('O', Wp(0, 0, 0)); proj('z38', Wp(0, 0, 3 / 8));
  }

  // ---------- S2: hélice na parede da lata, conta e força (v2: só os dois aros da lata; conta na frente) ----------
  if (K === 'helice') {
    SC = 2.2; lataTraco(1, 1, { nv: 0 }); eixoZ(-.1, 1.45);
    const H = t => WC(1.012, t, t / (4 * PI)), kh = sm(v('helice', 1));
    if (kh > 1e-3) tubo(arco(H, 0, 4 * PI * kh, Math.max(8, Math.round(400 * kh))), .014, HEL);
    const tc = 2 * PI - .75, P0 = H(tc), tg = [-Math.sin(tc), Math.cos(tc), 1 / (4 * PI)], n = Math.hypot(...tg);
    const Fp = [P0[0] + tg[0] / n * 1.1, P0[1] + tg[1] / n * 1.1, P0[2] + tg[2] / n * 1.1 + .25];
    if (v('conta', 1) > .5) bolinha(P0, BR, .045 * SC);
    const kF = sm(v('F', 1));
    if (kF > 1e-3) seta(P0, [P0[0] + (Fp[0] - P0[0]) * kF, P0[1] + (Fp[1] - P0[1]) * kF, P0[2] + (Fp[2] - P0[2]) * kF], .012, '#2EE6A0');
    proj('O', Wp(0, 0, 0)); proj('conta', P0); proj('F', Fp); proj('hel', H(PI * 3.1));
  }

  const L15 = [-1.5, 1.5, -1.5, 1.5], CUB = [-.5, 1.5, -.5, 1.5], TET = [-.25, 1.25, -.25, 1.25];
  const PISOK = {
    lataParede: L15, lataDobradica: [-.5, 2.5, -1.5, 1.5], lataDob3: [-.5, 2.5, -1.5, 1.5], cubo: CUB, cuboCaixas: CUB, cuboSonda: CUB, cuboDiag: CUB, cuboFolha: CUB,
    tetraSonda: TET, tetraCent: TET, tetraPlano: TET, cone: L15, coneCm: L15, coneCasca: L15, semi: L15, semiFatia: L15, helice: L15
  };
  // F1: octógonos (apótema) onde o retângulo não cabe com folga ≥ 20 px: [cx, cy, ap]
  const PISOO = { lataParede: [0, 0, 1.25], helice: [0, 0, 1.25], lataDobradica: [1, 0, 1.1], lataDob3: [1, 0, 1.1], cone: [0, 0, 1.1], coneCm: [0, 0, 1.1], coneCasca: [0, 0, 1.1], semi: [0, 0, 1.1], semiFatia: [0, 0, 1.1] };
  if (PISOO[K] && !e.semPiso) pisoOct(...PISOO[K]);
  else if (PISOK[K] && !e.semPiso) piso(...PISOK[K]);
  const xmax = e.clip || 975;
  R.setScissorTest(false); R.clear(); R.setScissorTest(true);
  R.setScissor(Math.round(60 * ESC), 0, Math.round((xmax - 60) * ESC), H);
  R.render(S, cam);
  return PTS;
};
window.segsPx = () => SEGS.map(pl => pl.map(v => { const q = new T.Vector3(...v).project(cam); return [+((q.x + 1) / 2 * 1920).toFixed(1), +((1 - q.y) / 2 * 1080).toFixed(1)]; }));
window.cenaPronta = true;
