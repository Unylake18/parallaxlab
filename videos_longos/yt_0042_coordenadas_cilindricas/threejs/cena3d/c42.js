// yt_0042 · cenas 3D (porte de referencia/yt_0042_quadros_alvo_v1/c3d42.html, three.js r128; motor e câmera do c41.js).
// Uma página por cena (<cena>.html) define window.CENA_ID. Estilo da série: opaco, sem luz (MeshBasicMaterial), tom fixo por face (LDIR),
// sem sombra/névoa/brilho/transparência, outputEncoding linear, antialias, fundo transparente (o Manim põe o violeta liso por baixo).
// A CÂMERA VEM DO MANIM no estado: {pos, tgt, up, cx, cy, fov} (perspectiva + setViewOffset). O giro da câmera em volta de z é do Palco42 (Manim).
// Chaves: lata, grade, ponto, caixa, latagrade, caixinha, cilindroRot, deslocadoSonda, giro.
const T = THREE, PI = Math.PI, K = window.CENA_ID;
const W = window.innerWidth, H = window.innerHeight, ESC = W / 1920;
const R = new T.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
R.setPixelRatio(1); R.setSize(W, H, false); R.setClearColor(0x000000, 0); R.outputEncoding = T.LinearEncoding;
document.body.appendChild(R.domElement);
const S = new T.Scene(); T.Object3D.DefaultUp.set(0, 0, 1);
const cam = new T.PerspectiveCamera(22, W / H, .05, 400);
const BG = '#131030', CI = '#35D9FF', E1 = '#FFC24D', E2 = '#EA63FF', EZ = '#5AA2FF', GEO = '#B8C4DA', BR = '#F5F7FF', RO = '#FF9440',
  TH = '#2EE6A6', SOMB = '#FFC08A', LI = '#C6F26B', AZC = '#7FB2FF', CORAL = '#FF7A8A', TR = '#6C7698', AL = '#FF5D5D', RAMP0 = '#10243A';
const C = h => new T.Color(h), mixc = (a, b, t) => C(a).lerp(C(b), t);
let SC = 2, G = null, PTS = {};
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
const cyl = (s, t, z) => [s * Math.cos(t), s * Math.sin(t), z];
const WC = (s, t, z) => Wp(...cyl(s, t, z));
function poli(pts) { const cp = new T.CurvePath(); for (let i = 0; i + 1 < pts.length; i++) cp.add(new T.LineCurve3(new T.Vector3(...pts[i]), new T.Vector3(...pts[i + 1]))); return cp; }
const tubo = (pts, r, cor) => add(new T.Mesh(new T.TubeGeometry(poli(pts), Math.max(8, (pts.length - 1) * 3), r, 8, false), new T.MeshBasicMaterial({ color: C(cor) })));
function tracejado(pts, r, cor, on = .12, off = .09) {
  let acc = 0, cur = [pts[0]], ligado = true; const segs = [];
  for (let i = 1; i < pts.length; i++) {
    const a = new T.Vector3(...pts[i - 1]), b = new T.Vector3(...pts[i]); let L = a.distanceTo(b), pos = 0;
    while (pos < L) {
      const lim = (ligado ? on : off) - acc, step = Math.min(lim, L - pos); pos += step; acc += step; const p = a.clone().lerp(b, pos / L);
      if (ligado) cur.push([p.x, p.y, p.z]); if (acc >= (ligado ? on : off) - 1e-9) { if (ligado && cur.length > 1) segs.push(cur); ligado = !ligado; acc = 0; cur = [[p.x, p.y, p.z]]; }
    }
  }
  if (ligado && cur.length > 1) segs.push(cur); for (const s of segs) tubo(s, r, cor);
}
function seta(a, b, r, cor) {
  const A = new T.Vector3(...a), B = new T.Vector3(...b), d = B.clone().sub(A), L = d.length(), hl = Math.min(.18, .3 * L), g = new T.Group(), m = new T.MeshBasicMaterial({ color: C(cor) });
  const s = new T.Mesh(new T.CylinderGeometry(r, r, L - hl, 12), m); s.position.y = (L - hl) / 2; const c = new T.Mesh(new T.ConeGeometry(r * 3, hl, 18), m); c.position.y = L - hl / 2; g.add(s, c);
  g.position.copy(A); g.quaternion.setFromUnitVectors(new T.Vector3(0, 1, 0), d.normalize()); add(g); return g;
}
function bolinha(p, rad, cor) { const b = new T.Mesh(new T.SphereGeometry(rad, 24, 16), new T.MeshBasicMaterial({ color: C(cor) })); b.position.set(...p); add(b); return b; }
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

// lata em traço: dois círculos + verticais a cada 30°
function lataTraco(Rr = 1, Hh = 1, { cor = GEO, w = .008, nv = 12, t0 = 0, t1 = 2 * PI, cv = TR } = {}) {
  for (const z of [0, Hh]) tubo(arco(t => WC(Rr, t, z), t0, t1, 120), w, cor);
  for (let k = 0; k < nv; k++) { const t = 2 * PI * k / nv; if (t < t0 - 1e-9 || t > t1 + 1e-9) continue; tubo([WC(Rr, t, 0), WC(Rr, t, Hh)], w * .6, cv); }
}
// célula cilíndrica s∈[s1,s2], θ∈[t1,t2], z∈[z1,z2]
function celC(s1, s2, t1, t2, z1, z2, cor = LI, { w = .010, borda = LI, fill = true } = {}) {
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
}

window.setEstado = e => {
  if (G) { S.remove(G); G.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.material) o.material.dispose(); }); }
  G = new T.Group(); S.add(G); PTS = {};
  aplicaCam(e.cam);
  const v = (k, d = 0) => (e[k] ?? d);

  // ---------- lata pesada: densidade = distância à origem, um quarto aberto (θ ∈ [−π/2, 0]); `quina` = contorno ALERTA na quina da tampa ----------
  if (K === 'lata') {
    SC = 2.2; const ta = -PI / 2, tb = 0;
    sup((t, z) => WC(1, t, z), tb, ta + 2 * PI, 110, 8, (t, z) => tom(corR(1, z), [Math.cos(t), Math.sin(t), 0], .55, .40));
    sup((s, t) => WC(s, t, 1), 0, 1, tb, ta + 2 * PI, 24, 90, (s, t) => mixc(corR(s, 1), BR, .06));
    for (const t of [ta, tb]) sup((s, z) => WC(s, t, z), 0, 1, 0, 1, 30, 30, (s, z) => corR(s, z));
    for (const z of [0, 1]) tubo(arco(t => WC(1, t, z), tb, ta + 2 * PI, 120), .009, CI);
    for (const z of [0, 1]) tubo(arco(t => WC(1, t, z), ta, tb, 40), .005, TR);
    tubo([WC(1, ta, 0), WC(1, ta, 1)], .005, TR);
    for (const t of [ta, tb]) tubo([WC(0, t, 0), WC(1, t, 0), WC(1, t, 1), WC(0, t, 1)], .009, CI);
    for (const r of [.5, 1]) for (const t of [ta, tb]) tubo(arco(a => { const s = r * Math.cos(a), z = r * Math.sin(a); return WC(s, t, z); }, 0, PI / 2, 40), .004, '#1E5C7A');
    tubo([Wp(0, 0, 0), Wp(0, 0, 1.45)], .010, EZ);
    seta([SC * 1.03, 0, 0], [SC * 1.55, 0, 0], .012, E1); seta([0, SC * 1.03, 0], [0, SC * 1.55, 0], .012, E2);
    if (v('quina') > 1e-3) { tubo([WC(1, tb, .85), WC(1, tb, 1)], .016, AL); }
    proj('ex', [SC * 1.68, 0, 0]); proj('ey', [0, SC * 1.68, 0]); proj('ez', Wp(0, 0, 1.55)); proj('O', [0, 0, 0]); proj('fundo', Wp(.08, 0, .08));
    proj('quina', WC(1, tb, 1)); proj('quinaB', WC(1, ta, 1)); proj('faceA', WC(.5, tb, .5)); proj('faceB', WC(.5, ta, .5)); proj('parede', WC(1, PI * .65, .5)); proj('tampa', WC(.55, PI * .6, 1));
  }

  // ---------- grade da lata: lata em traço; famílias (cil s=0,5, página θ=tp, andar z=0,5) uma por vez; duas células lima ----------
  if (K === 'grade') {
    SC = 2.2;
    lataTraco(1, 1, { nv: 12 });
    tubo([Wp(0, 0, -.1), Wp(0, 0, 1.45)], .010, EZ);
    const kcil = sm(v('cil')), kpag = sm(v('pag')), kand = sm(v('andar'));
    if (kcil > 1e-3) { sup((t, z) => WC(.5, t, z), 0, 2 * PI * Math.min(1, kcil), 0, 1, 72, 4, (t, z) => tom(SOMB, [Math.cos(t), Math.sin(t), 0], .30, .25)); tubo(arco(t => WC(.5, t, 1), 0, 2 * PI * kcil, 90), .006, SOMB); }
    const tp = PI * .15;
    if (kpag > 1e-3) { sup((s, z) => WC(s, tp, z), 0, Math.min(1, kpag), 0, 1, 4, 4, () => mixc(BG, TH, .30)); tubo([WC(0, tp, 0), WC(Math.min(1, kpag), tp, 0), WC(Math.min(1, kpag), tp, 1), WC(0, tp, 1)], .008, TH); }
    if (kand > 1e-3) { sup((s, t) => WC(s, t, .5), 0, 1, 0, 2 * PI * Math.min(1, kand), 6, 72, () => mixc(BG, EZ, .26)); tubo(arco(t => WC(1, t, .5), 0, 2 * PI * kand, 96), .008, EZ); }
    const kcel = sm(v('cels'));
    if (kcel > 1e-3) {
      const e1 = -PI * .47, e2 = e1 + PI / 6, p1 = -PI * .13, p2 = p1 + PI / 6;
      celC(0, .5, e1, e2, .5, 1); celC(.5, 1, p1, p2, .5, 1);
    }
    proj('celEixo', WC(.30, (-PI * .47 + (-PI * .47 + PI / 6)) / 2, 1.0)); proj('celPar', WC(.8, (-PI * .13 + (-PI * .13 + PI / 6)) / 2, 1.0));
    proj('celEixoIn', WC(.25, (-PI * .47 + (-PI * .47 + PI / 6)) / 2, .75)); proj('celParIn', WC(.75, (-PI * .13 + (-PI * .13 + PI / 6)) / 2, .75));
    proj('ez', Wp(0, 0, 1.55)); proj('O', [0, 0, 0]);
    proj('cil', WC(.5, -PI * .35, .8)); proj('pag', WC(.75, tp, .85)); proj('andar', WC(.85, -PI * .15, .5));
  }

  // ---------- ponto P = (s, θ, z) = (2, π/3, 3/2) ----------
  if (K === 'ponto') {
    SC = 1.05; const s0 = 2, t0 = PI / 3, z0 = 1.5, P = cyl(s0, t0, z0), P1 = [P[0], P[1], 0], Pz = [0, 0, z0];
    for (const rr of [.5, 1, 1.5, 2]) tubo(arco(a => Wp(rr * Math.cos(a), rr * Math.sin(a), 0), 0, 2 * PI, 96), .0045, '#3A3470');
    for (let k = 0; k < 12; k++) { const a = 2 * PI * k / 12; tubo([Wp(0, 0, 0), Wp(2 * Math.cos(a), 2 * Math.sin(a), 0)], .0045, '#3A3470'); }
    seta([0, 0, 0], [SC * 2.3, 0, 0], .013, E1); seta([0, 0, 0], [0, SC * 2.6, 0], .013, E2); seta([0, 0, 0], [0, 0, SC * 2.2], .013, EZ);
    const kpag = sm(v('pag'));
    if (kpag > 1e-3) { sup((a, b) => Wp(...[0, 1, 2].map(i => a * (P1[i] * (1 - b) + P[i] * b))), 0, 1, 0, kpag, 4, 4, () => mixc(BG, TH, .16)); tubo([Wp(0, 0, 0), Wp(...P), Wp(...[P[0] * (1 - kpag) + P1[0] * kpag, P[1] * (1 - kpag) + P1[1] * kpag, P[2] * (1 - kpag) + P1[2] * kpag]), Wp(0, 0, 0)], .004, TH); }
    const ks = sm(v('sombra'));
    if (ks > 1e-3) { tubo([Wp(0, 0, 0), Wp(P1[0] * ks, P1[1] * ks, 0)], .016, SOMB); if (ks > .999) bolinha(Wp(...P1), .045, SOMB); }
    const ka = sm(v('arco'));
    if (ka > 1e-3) tubo(arco(a => Wp(.8 * Math.cos(a), .8 * Math.sin(a), 0), 0, t0 * Math.min(1, ka), 40), .012, TH);
    const kz = sm(v('z'));
    if (kz > 1e-3) { tracejado([Wp(...P1), Wp(P[0], P[1], P1[2] + (P[2] - P1[2]) * kz)], .011, EZ); tubo([Wp(0, 0, 0), Wp(0, 0, z0 * kz)], .016, EZ); }
    const kf = sm(v('fio'));
    if (kf > 1e-3) tracejado([Wp(...Pz), Wp(Pz[0] + (P[0] - Pz[0]) * kf, Pz[1] + (P[1] - Pz[1]) * kf, z0)], .011, SOMB, .10, .07);
    const kxy = sm(v('xy'));
    if (kxy > 1e-3) { tracejado([Wp(...P1), Wp(P[0], P[1] * (1 - kxy), 0)], .006, E1, .08, .07); tracejado([Wp(...P1), Wp(P[0] * (1 - kxy), P[1], 0)], .006, E2, .08, .07); }
    tubo([Wp(0, 0, 0), Wp(...P)], .009, RO);
    bolinha(Wp(...P), .07, BR);
    proj('ex', [SC * 2.45, 0, 0]); proj('ey', [0, SC * 2.75, 0]); proj('ez', [0, 0, SC * 2.35]);
    proj('P', Wp(...P)); proj('P1', Wp(...P1)); proj('O', [0, 0, 0]); proj('meioS', Wp(P1[0] / 2, P1[1] / 2, 0)); proj('meioFio', Wp(P[0] / 2, P[1] / 2, z0)); proj('meioZ', Wp(P[0], P[1], z0 / 2));
    proj('arcoTh', Wp(Math.cos(t0 / 2), Math.sin(t0 / 2), 0)); proj('Pz', Wp(...Pz)); proj('meioR', Wp(P[0] * .45, P[1] * .45, z0 * .45)); proj('xP', Wp(P[0], 0, 0)); proj('yP', Wp(0, P[1], 0));
  }

  // ---------- caixa no espaço (s, θ, z) ----------
  if (K === 'caixa') {
    SC = 1; const CX = (s, t, z) => Wp(1.6 * s, 2.4 * t / (2 * PI), 1.2 * z), f = CX;
    const meia = v('meia') > .5, sep = v('sep');
    const Q = (s, t, z) => [1.6 * s * SC, 2.4 * ((t > PI - 1e-9 && meia) ? t + sep : t) / (2 * PI) * SC, 1.2 * z * SC];
    const face = (F, a0, a1, b0, b1, c) => sup(F, a0, a1, b0, b1, 2, 2, () => c);
    // face s = 0 (ruim: vira o eixo)
    face((t, z) => Q(0, t, z), 0, 2 * PI, 0, 1, mixc(BG, AL, v('eixo') > .5 ? .40 : .22));
    for (const t of [2 * PI]) face((s, z) => Q(s, t, z), 0, 1, 0, 1, mixc(BG, AL, v('costura') > .5 ? .34 : .16));   // θ = 2π (colada com θ = 0)
    face((s, t) => Q(s, t, 0), 0, 1, 0, 2 * PI, mixc(BG, GEO, .14));
    for (const z of [.25, .5, .75]) tubo([Q(1, 0, z), Q(1, 2 * PI, z)], .004, '#4A4F78');
    for (let k = 1; k < 12; k++) tubo([Q(1, 2 * PI * k / 12, 0), Q(1, 2 * PI * k / 12, 1)], .004, '#4A4F78');
    const E = [[0, 0, 0], [1, 0, 0], [1, 2 * PI, 0], [0, 2 * PI, 0], [0, 0, 1], [1, 0, 1], [1, 2 * PI, 1], [0, 2 * PI, 1]];
    for (const [a, b] of [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]]) tubo([Q(...E[a]), Q(...E[b])], .008, GEO);
    if (v('eixo') > .5) tracejado([Q(0, 0, 0), Q(0, 2 * PI, 0), Q(0, 2 * PI, 1), Q(0, 0, 1), Q(0, 0, 0)], .011, AL, .08, .06);
    if (v('costura') > .5) for (const t of [0, 2 * PI]) tracejado([Q(0, t, 0), Q(1, t, 0), Q(1, t, 1), Q(0, t, 1)], .011, AL, .08, .06);
    if (v('celula') > .5) {
      const c1 = [.5, PI / 3, .5], c2 = [1, PI / 2, 1], V8 = [];
      for (const a of [c1[0], c2[0]]) for (const b of [c1[1], c2[1]]) for (const c of [c1[2], c2[2]]) V8.push([a, b, c]);
      for (const [nrm, fx] of [[[1, 0, 0], p => p[0] === 1], [[0, 0, 1], p => p[2] === 1], [[0, -1, 0], p => p[1] === PI / 3]]) {
        const q = V8.filter(fx); sup((u, vv) => { const A = q[0], B = q[1], D = q[2]; return Q(...[0, 1, 2].map(i => A[i] + (B[i] - A[i]) * u + (D[i] - A[i]) * vv)); }, 0, 1, 0, 1, 1, 1, () => tom(LI, nrm, .40, .45));
      }
      for (let i = 0; i < 8; i++) for (let j = i + 1; j < 8; j++) { const d = [0, 1, 2].filter(k => V8[i][k] !== V8[j][k]); if (d.length === 1) tubo([Q(...V8[i]), Q(...V8[j])], .009, LI); }
    }
    seta(Q(0, 0, 0), Q(1.35, 0, 0), .012, SOMB); seta(Q(0, 0, 0), Q(0, 2 * PI * 1.15, 0), .012, TH); seta(Q(0, 0, 0), Q(0, 0, 1.35), .012, EZ);
    proj('eS', Q(1.45, 0, 0)); proj('eT', Q(0, 2 * PI * 1.22, 0)); proj('eZ', Q(0, 0, 1.45)); proj('um_s', Q(.5, 0, -.1)); proj('dois_pi', Q(0, PI, -.12)); proj('um_z', Q(0, 0, .5));
    proj('cel', Q(1, (PI / 3 + PI / 2) / 2, 1)); proj('face0', Q(0, PI * 1.2, .5)); proj('faceT0', Q(.5, 0, .5)); proj('faceT2', Q(.5, 2 * PI, .5)); proj('O', Q(0, 0, 0));
  }

  // ---------- latagrade: a imagem da caixa (lata em traço), eixo e costura em alerta ----------
  if (K === 'latagrade') {
    SC = 2;
    lataTraco(1, 1, { nv: 12 }); for (const z of [.5]) tubo(arco(t => WC(1, t, z), 0, 2 * PI, 90), .004, '#4A4F78'); for (const z of [0, .5, 1]) tubo(arco(t => WC(.5, t, z), 0, 2 * PI, 90), .004, '#4A4F78');
    if (v('eixo') > .5) { tubo([Wp(0, 0, 0), Wp(0, 0, 1)], .016, AL); } else { tubo([Wp(0, 0, 0), Wp(0, 0, 1)], .008, TR); }
    tubo([Wp(0, 0, 1), Wp(0, 0, 1.4)], .009, EZ);
    if (v('costura') > .5) { tracejado([WC(0, 0, 0), WC(1, 0, 0), WC(1, 0, 1), WC(0, 0, 1)], .012, AL, .08, .06); sup((s, z) => WC(s, 0, z), 0, 1, 0, 1, 2, 2, () => mixc(BG, AL, .18)); }
    if (v('celula') > .5) celC(.5, 1, PI / 3, PI / 2, .5, 1);
    proj('cel', WC(.8, PI * .42, 1.05)); proj('eixo', Wp(0, 0, .5)); proj('costura', WC(.7, 0, .5)); proj('ez', Wp(0, 0, 1.5)); proj('O', [0, 0, 0]);
  }

  // ---------- caixinha: zoom numa célula da parede; arestas a partir do canto (s2, θ1, z1) ----------
  if (K === 'caixinha') {
    SC = 3.2; const s1 = .55, s2 = 1, t1 = -PI * .30, t2 = t1 + PI / 6, z1 = .35, z2 = .8;
    celC(s1, s2, t1, t2, z1, z2, LI, { w: .008 });
    const a1 = sm(v('a1')), a2 = sm(v('a2')), a3 = sm(v('a3'));
    if (a1 > 1e-3) tubo([WC(s2, t1, z1), WC(s2 - (s2 - s1) * a1, t1, z1)], .020, SOMB);
    if (a2 > 1e-3) { tubo(arco(t => WC(s2, t, z1), t1, t1 + (t2 - t1) * a2, 30), .020, TH); if (a2 > .999) { tracejado([Wp(0, 0, z1), WC(s2, t1, z1)], .008, SOMB, .06, .05); tracejado([Wp(0, 0, z1), WC(s2, t2, z1)], .008, SOMB, .06, .05); } }
    if (a3 > 1e-3) tubo([WC(s2, t1, z1), WC(s2, t1, z1 + (z2 - z1) * a3)], .020, EZ);
    tubo(arco(t => WC(.18, t, z1), t1, t2, 20), .008, TH);
    tubo([Wp(0, 0, -.05), Wp(0, 0, 1.15)], .010, EZ);
    lataTraco(1, 1, { nv: 24, t0: -PI * .75, t1: PI * .25, w: .005, cor: '#4A4F78', cv: '#3A3470' });
    bolinha(WC(s2, t1, z1), .03, BR);
    proj('dS', WC((s1 + s2) / 2, t1, z1)); proj('arco', WC(s2, (t1 + t2) / 2, z1)); proj('dZ', WC(s2, t1, (z1 + z2) / 2)); proj('raio', WC(s2 * .5, t1, z1));
    proj('ang', WC(.25, (t1 + t2) / 2, z1)); proj('canto', WC(s2, t1, z1)); proj('ez', Wp(0, 0, 1.22));
  }

  // ---------- cilindro de raio R e altura h (teste); `rotulo` = parede em contorno ALERTA ----------
  if (K === 'cilindroRot') {
    SC = 1.9; const Hh = 1.4;
    sup((t, z) => WC(1, t, z), 0, 2 * PI, 0, Hh, 96, 4, (t, z) => tom(GEO, [Math.cos(t), Math.sin(t), 0], .10, .18));
    sup((s, t) => WC(s, t, Hh), 0, 1, 0, 2 * PI, 8, 72, () => mixc(BG, GEO, .26));
    const cb = v('rotulo') > .5 ? AL : GEO;
    for (const z of [0, Hh]) tubo(arco(t => WC(1, t, z), 0, 2 * PI, 120), v('rotulo') > .5 ? .014 : .009, cb);
    if (v('rotulo') > .5) for (const t of [PI * .62, -PI * .28]) tubo([WC(1, t, 0), WC(1, t, Hh)], .012, AL);
    tubo([WC(0, 0, Hh), WC(1, -PI * .20, Hh)], .016, SOMB);
    tubo([WC(1, -PI * .47, 0), WC(1, -PI * .47, Hh)], .016, EZ);
    tubo([Wp(0, 0, -.1), Wp(0, 0, Hh + .35)], .010, EZ);
    proj('R', WC(.5, -PI * .20, Hh)); proj('h', WC(1, -PI * .47, Hh / 2)); proj('ez', Wp(0, 0, Hh + .45)); proj('rotulo', WC(1, -PI * .05, Hh * .5));
  }

  // ---------- o meio cilindro fora do eixo: (x−1)² + y² ≤ 1, y ≥ 0, 0 ≤ z ≤ x + y ----------
  if (K === 'deslocadoSonda') {
    SC = 1.3;
    const DX = (s, t, z) => Wp(1 + s * Math.cos(t), s * Math.sin(t), z);
    const teto = (s, t) => 1 + s * Math.cos(t) + s * Math.sin(t);
    for (const rr of [.5, 1, 1.5, 2, 2.5]) tubo(arco(a => Wp(rr * Math.cos(a), rr * Math.sin(a), 0), -PI * .1, PI * .6, 60), .004, '#3A3470');
    const ksomb = sm(v('sombra'));
    if (ksomb > 1e-3) sup((s, t) => DX(s, t, 0), 0, 1, 0, PI * Math.min(1, ksomb), 6, 48, () => mixc(BG, AZC, .22));
    for (let k = 1; k < 6; k++) { const t = PI * k / 6; tubo([DX(1, t, 0), DX(1, t, teto(1, t))], .005, TR); }
    for (const ss of [.5]) tubo(arco(t => DX(ss, t, teto(ss, t)), 0, PI, 60), .005, '#3F6FB0'); for (let k = 1; k < 6; k++) { const t = PI * k / 6; tubo(arco(q => DX(q, t, teto(q, t)), 0, 1, 10), .005, '#3F6FB0'); }
    tubo(arco(t => DX(1, t, teto(1, t)), 0, PI, 80), .009, EZ); tubo([Wp(0, 0, 0), Wp(2, 0, 2)], .009, EZ);
    tubo(arco(t => DX(1, t, 0), 0, PI, 80), .008, GEO); tubo([Wp(0, 0, 0), Wp(2, 0, 0)], .008, GEO); tubo([Wp(2, 0, 0), Wp(2, 0, 2)], .008, GEO);
    const keixo = sm(v('eixoNovo'));
    if (keixo > 1e-3) tracejado([Wp(1, 0, 0), Wp(1, 0, 3.0 * keixo)], .009, BR, .10, .07);
    seta([0, 0, 0], [SC * 2.6, 0, 0], .012, E1); seta([0, 0, 0], [0, SC * 1.6, 0], .012, E2); seta([0, 0, 0], [0, 0, SC * 3.0], .012, EZ);
    bolinha(Wp(1, 0, 0), .045, BR);
    const ss = .6, tt = PI * .55, pb = DX(ss, tt, 0), pt = DX(ss, tt, teto(ss, tt));
    const ksonda = sm(v('sonda'));
    if (ksonda > 1e-3) { tubo([pb, [pb[0] + (pt[0] - pb[0]) * ksonda, pb[1] + (pt[1] - pb[1]) * ksonda, pb[2] + (pt[2] - pb[2]) * ksonda]], .013, RO); bolinha(pb, .045, AZC); if (ksonda > .999) bolinha(pt, .045, CORAL); }
    proj('ex', [SC * 2.72, 0, 0]); proj('ey', [0, SC * 1.72, 0]); proj('ez', [0, 0, SC * 3.12]);
    proj('entra', pb); proj('sai', pt); proj('polo', Wp(1, 0, 0)); proj('eixoNovo', Wp(1, 0, 3.05)); proj('telhado', DX(.55, PI * .35, teto(.55, PI * .35))); proj('parede', DX(1, PI * .62, .5));
    proj('sombra', DX(.6, PI * .75, 0)); proj('face0', Wp(1.45, 0, .45)); proj('O', [0, 0, 0]); proj('dois', Wp(2, 0, 0));
  }

  // ---------- girar a lata (S2): lata em traço, eixo, seta de giro, célula na parede com o fio s ----------
  if (K === 'giro') {
    SC = 2.2;
    lataTraco(1, 1, { nv: 12 });
    tubo([Wp(0, 0, -.25), Wp(0, 0, 1.6)], .016, EZ);
    if (v('seta') > 1e-3) {
      const A = arco(t => Wp(.32 * Math.cos(t), .32 * Math.sin(t), 1.38), -PI * .9, PI * .55, 60); tubo(A, .010, GEO);
      const a1 = Wp(.32 * Math.cos(PI * .55), .32 * Math.sin(PI * .55), 1.38), a0 = Wp(.32 * Math.cos(PI * .48), .32 * Math.sin(PI * .48), 1.38); seta(a0, a1, .010, GEO);
    }
    const t1 = -PI * .18, t2 = t1 + PI / 10;
    if (v('cel') > 1e-3) { celC(.85, 1, t1, t2, .45, .65); tracejado([Wp(0, 0, .55), WC(.85, (t1 + t2) / 2, .55)], .010, SOMB, .07, .05); }
    proj('cel', WC(1.04, (t1 + t2) / 2, .55)); proj('fio', WC(.45, (t1 + t2) / 2, .55)); proj('giro', Wp(.32, 0, 1.38)); proj('ez', Wp(0, 0, 1.7));
  }

  const clip = K !== 'caixa' && K !== 'latagrade';
  R.setScissorTest(false); R.clear(); R.setScissorTest(clip); if (clip) R.setScissor(0, 0, Math.round(975 * ESC), H);
  R.render(S, cam);
  return PTS;
};
window.cenaPronta = true;
