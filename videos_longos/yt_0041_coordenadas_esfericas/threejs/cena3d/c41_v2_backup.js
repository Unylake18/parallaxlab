// yt_0041 · cenas 3D (porte de referencia/yt_0041_quadros_alvo_v1_1/c3d41.html, three.js r128; motor e câmera do c37.js do yt_0037).
// Uma página por cena (<cena>.html) define window.CENA_ID. Estilo da série: opaco, sem luz (MeshBasicMaterial), tom fixo por face (LDIR),
// sem sombra/névoa/brilho/transparência, outputEncoding linear, antialias, fundo transparente (o Manim põe o violeta liso por baixo).
// A CÂMERA VEM DO MANIM no estado: {pos, tgt, up, cx, cy, fov} (perspectiva + setViewOffset: o alvo cai em (cx, cy) px de 1080p).
// O c3d41.html desenha só o estado final; aqui cada cena tem os estados do handoff §2.2 (todos numéricos, 0/1 ou contínuos).
// Regra da série: a peça NUNCA se separa (exceto o único afastamento da caixa2 no B3-1, que volta); o lado de fora do corte vira traço #6C7698.
const T = THREE, PI = Math.PI, K = window.CENA_ID;
const W = window.innerWidth, H = window.innerHeight, ESC = W / 1920;
const R = new T.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
R.setPixelRatio(1); R.setSize(W, H, false); R.setClearColor(0x000000, 0); R.outputEncoding = T.LinearEncoding;
document.body.appendChild(R.domElement);
const S = new T.Scene(); T.Object3D.DefaultUp.set(0, 0, 1);
const cam = new T.PerspectiveCamera(22, W / H, .05, 400);
const BG = '#131030', CI = '#35D9FF', E1 = '#FFC24D', E2 = '#EA63FF', EZ = '#5AA2FF', GEO = '#B8C4DA', BR = '#F5F7FF', RO = '#FF9440', TH = '#2EE6A6',
  FI = '#B48CFF', SOMB = '#FFC08A', LI = '#C6F26B', AZC = '#7FB2FF', CORAL = '#FF7A8A', TR = '#6C7698', AL = '#FF5D5D', RAMP0 = '#10243A';
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
const sph = (r, f, t) => [r * Math.sin(f) * Math.cos(t), r * Math.sin(f) * Math.sin(t), r * Math.cos(f)];
const WS = (r, f, t) => Wp(...sph(r, f, t));
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
// superfície paramétrica (a,b) -> ponto do mundo (já em unidades SC); cor(a,b) -> THREE.Color ou cor fixa
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

function bolaCortada(ta, tb, { dens = true, cor = CI, tracoGomo = true, casca084 = 0 } = {}) {
  const aberto = tb - ta > 1e-3;
  if (!aberto) { sup((f, t) => WS(1, f, t), 0, PI, 0, 2 * PI, 48, 128, (f, t) => tom(dens ? corDens(1) : C(cor), sph(1, f, t), .42, .42)); return; }
  sup((f, t) => WS(1, f, t), 0, PI, tb, ta + 2 * PI, 48, 110, (f, t) => tom(dens ? corDens(1) : C(cor), sph(1, f, t), .42, .42));
  for (const t of [ta, tb]) sup((r, f) => WS(r, f, t), 0, 1, 0, PI, 40, 60, (r, f) => dens ? corDens(r) : mixc(BG, cor, .5));
  for (const t of [ta, tb]) tubo(arco(f => WS(1, f, t), 0, PI), .012, dens ? CI : cor);
  tubo([Wp(0, 0, -1), Wp(0, 0, 1)], .010, GEO);
  if (tracoGomo) {
    for (let k = 1; k <= 3; k++) { const t = ta + (tb - ta) * k / 4; tubo(arco(f => WS(1, f, t), 0, PI), .006, TR); }
    for (const f of [PI / 4, PI / 2, 3 * PI / 4]) tubo(arco(t => WS(1, f, t), ta, tb, 30), .006, TR);
  }
  if (casca084 > .5) {             // B5: a casca de r = 0,84 a 1 ganha o contorno laranja nas duas faces do corte (sem brilho)
    const c = Math.pow(.5, .25);
    for (const t of [ta, tb]) { tubo(arco(f => WS(c, f, t), 0, PI, 60), .013, RO); tubo(arco(f => WS(1.004, f, t), 0, PI, 60), .013, RO);
      tubo([Wp(0, 0, c), Wp(0, 0, 1.004)], .013, RO); tubo([Wp(0, 0, -c), Wp(0, 0, -1.004)], .013, RO); }
  }
}
function celula(r1, r2, f1, f2, t1, t2, cor = LI, { w = .010, borda = LI, fill = true } = {}) {
  if (fill) {
    const fc = (n) => tom(cor, n, .40, .45);
    sup((f, t) => WS(r2, f, t), f1, f2, t1, t2, 8, 8, (f, t) => fc(sph(1, f, t)));
    sup((f, t) => WS(r1, f, t), f1, f2, t1, t2, 8, 8, (f, t) => mixc(BG, cor, .30));
    for (const t of [t1, t2]) sup((r, f) => WS(r, f, t), r1, r2, f1, f2, 4, 8, (r, f) => fc([-Math.sin(t) * (t === t1 ? 1 : -1), Math.cos(t) * (t === t1 ? 1 : -1), 0].map(v => -v)));
    for (const f of [f1, f2]) if (Math.sin(f) > 1e-6) sup((r, t) => WS(r, f, t), r1, r2, t1, t2, 4, 8, (r, t) => fc(f === f1 ? [-Math.cos(f) * Math.cos(t), -Math.cos(f) * Math.sin(t), Math.sin(f)] : [Math.cos(f) * Math.cos(t), Math.cos(f) * Math.sin(t), -Math.sin(f)]));
  }
  for (const r of [r1, r2]) for (const f of [f1, f2]) if (Math.sin(f) > 1e-6) tubo(arco(t => WS(r, f, t), t1, t2, 20), w, borda);
  for (const r of [r1, r2]) for (const t of [t1, t2]) tubo(arco(f => WS(r, f, t), f1, f2, 20), w, borda);
  for (const f of [f1, f2]) for (const t of [t1, t2]) tubo([WS(r1, f, t), WS(r2, f, t)], w, borda);
}
function esferaTraco(r, { nm = 12, np = [PI / 6, PI / 3, PI / 2, 2 * PI / 3, 5 * PI / 6], cor = TR, w = .005, t0 = 0, t1 = 2 * PI } = {}) {
  for (let k = 0; k < nm; k++) { const t = 2 * PI * k / nm; if (t < t0 - 1e-9 || t > t1 + 1e-9) continue; tubo(arco(f => WS(r, f, t), 0, PI, 60), w, cor); }
  for (const f of np) tubo(arco(t => WS(r, f, t), t0, t1, 90), w, cor);
}
const CAZ = Math.atan2(-6.2, 9.2);

window.setEstado = e => {
  if (G) { S.remove(G); G.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.material) o.material.dispose(); }); }
  G = new T.Group(); S.add(G); PTS = {};
  aplicaCam(e.cam);
  const v = (k, d = 0) => (e[k] ?? d);

  // ---------- bola: densidade = distância; a cunha de 90° abre centrada em CAZ (H1, B5) ----------
  if (K === 'bola') {
    SC = 2; const w = (PI / 2) * sm(v('cunha', 1)), ta = CAZ - w / 2, tb = CAZ + w / 2;
    bolaCortada(ta, tb, { casca084: v('casca084') });
    if (w > 1e-3) for (const r of [.25, .5, .75]) for (const t of [ta, tb]) tubo(arco(f => WS(r, f, t), 0, PI, 50), .005, '#1E5C7A');
    seta([SC * 1.02, 0, 0], [SC * 1.55, 0, 0], .012, E1); seta([0, SC * 1.02, 0], [0, SC * 1.55, 0], .012, E2); seta([0, 0, SC * 1.0], [0, 0, SC * 1.5], .012, EZ);
    const tA = CAZ - PI / 4, tB = CAZ + PI / 4;
    proj('ex', [SC * 1.68, 0, 0]); proj('ey', [0, SC * 1.68, 0]); proj('ez', [0, 0, SC * 1.62]);
    proj('centro', [0, 0, 0]); proj('casca', WS(1, PI * .62, tB + .9).map(q => q * 1.02)); proj('faceMeio', WS(.5, PI * .35, tA)); proj('faceBorda', WS(.95, PI * .5, tA)); proj('faceB', WS(.6, PI * .55, tB));
    proj('raio', WS(.55, PI / 2, tA)); proj('topo', [0, 0, SC + .1]); proj('c084', WS(.92, PI * .62, tB));
  }

  // ---------- grade: esfera em traço; famílias (casca, cone, página) uma por vez; as duas células lima (H2) ----------
  if (K === 'grade') {
    SC = 2.1;
    esferaTraco(1, { nm: 12, np: [PI / 6, PI / 3, PI / 2, 2 * PI / 3, 5 * PI / 6] });
    const kc = sm(v('cone')), kp = sm(v('pagina')), ks = sm(v('casca'));      // cada família cresce (sem fade): o cone gira, a página sai do eixo, a casca se abre
    if (kc > 1e-3) { sup((r, t) => WS(r, PI / 4, t), 0, 1, 0, 2 * PI * kc, 6, Math.max(4, Math.round(72 * kc)), (r, t) => mixc(BG, FI, .28 + .10 * Math.max(0, Math.cos(t + 1.0)))); tubo(arco(t => WS(1, PI / 4, t), 0, 2 * PI * kc, Math.max(4, Math.round(96 * kc))), .008, FI); }
    if (kp > 1e-3) { sup((r, f) => WS(r, f, -PI / 4 + 2 * PI), 0, kp, 0, PI, 6, 40, () => mixc(BG, TH, .26)); tubo(arco(f => WS(kp, f, -PI / 4), 0, PI, 60), .008, TH); }
    if (ks > 1e-3) { sup((f, t) => WS(.6, f, t), 0, PI, PI * .05, PI * (.05 + ks), 30, Math.max(4, Math.round(50 * ks)), (f, t) => tom(RO, sph(1, f, t), .40, .30)); if (ks > .999) esferaTraco(.6, { nm: 12, np: [PI / 2], cor: '#7A5A44', t0: 0, t1: 2 * PI }); }
    tubo([Wp(0, 0, -1.25), Wp(0, 0, 1.35)], .008, EZ);
    const t1 = -PI / 2 + .15, t2 = t1 + PI / 6;
    const kcel = sm(v('celulas'));                       // as células crescem para fora (r de 0,5 até 1)
    if (kcel > 1e-3) { esferaTraco(.5, { nm: 12, np: [PI / 2], cor: '#4A4F78' }); const r2 = .5 + .5 * kcel; celula(.5, r2, 0, PI / 6, t1, t2); celula(.5, r2, PI / 3, PI / 2, t1, t2); }
    proj('celPolo', WS(1.04, PI / 12, (t1 + t2) / 2)); proj('celEq', WS(1.04, 5 * PI / 12, (t1 + t2) / 2)); proj('celPoloIn', WS(.75, PI / 12, (t1 + t2) / 2)); proj('celEqIn', WS(.75, 5 * PI / 12, (t1 + t2) / 2));
    proj('cone', WS(.95, PI / 4, PI * .85)); proj('pagina', WS(.7, PI * .62, -PI / 4)); proj('esfera', WS(1, PI * .7, PI * .15)); proj('ez', [0, 0, SC * 1.35 + .15]); proj('centro', [0, 0, 0]);
    proj('cascaP', WS(.6, PI * .3, PI * .55));
  }

  // ---------- ponto P = (2, π/6, π/3): cada peça no seu gatilho (B1-1, B1-2) ----------
  if (K === 'ponto') {
    SC = 1.35; const rho = 2, f = PI / 6, t = PI / 3, Pp = sph(rho, f, t), r = rho * Math.sin(f), P1 = [Pp[0], Pp[1], 0];
    for (const rr of [.5, 1, 1.5, 2]) tubo(arco(a => Wp(rr * Math.cos(a), rr * Math.sin(a), 0), 0, 2 * PI, 96), .0045, '#3A3470');
    for (let k = 0; k < 12; k++) { const a = 2 * PI * k / 12; tubo([Wp(0, 0, 0), Wp(2 * Math.cos(a), 2 * Math.sin(a), 0)], .0045, '#3A3470'); }
    seta([0, 0, 0], [SC * 2.45, 0, 0], .013, E1); seta([0, 0, 0], [0, SC * 2.4, 0], .013, E2); seta([0, 0, 0], [0, 0, SC * 2.35], .013, EZ);
    const kpg = sm(v('pagina'));             // a página: triângulo retângulo chapado #1E3A4A (sem transparência) com contorno fino verde-água; cresce a partir de OP
    if (kpg > 1e-3) {
      sup((s, u) => Wp(...[0, 0, 0].map((q, i) => q + s * (Pp[i] * (1 - u) + P1[i] * u))), 0, 1, 0, kpg, 4, 4, () => C('#1E3A4A'));
      const Q = [Pp[0] * (1 - kpg) + P1[0] * kpg, Pp[1] * (1 - kpg) + P1[1] * kpg, Pp[2] * (1 - kpg) + P1[2] * kpg];
      tubo([Wp(0, 0, 0), Wp(...Pp), Wp(...Q), Wp(0, 0, 0)], .005, TH);
    }
    const kr = v('rho'); if (kr > 1e-3) tubo([Wp(0, 0, 0), Wp(...Pp.map(q => q * Math.min(1, kr)))], .017, RO);
    const kal = sm(v('altura')), kso = sm(v('sombra'));
    if (kal > 1e-3) { const zc = rho * Math.cos(f); tracejado([Wp(...Pp), Wp(Pp[0], Pp[1], Pp[2] * (1 - kal))], .010, EZ); tubo([Wp(0, 0, 0), Wp(0, 0, zc * kal)], .016, EZ);
      tracejado([Wp(...Pp), Wp(Pp[0] * (1 - kal), Pp[1] * (1 - kal), zc)], .007, GEO); }
    if (kso > 1e-3) { tubo([Wp(0, 0, 0), Wp(P1[0] * kso, P1[1] * kso, 0)], .014, SOMB); if (kso > .999) bolinha(Wp(...P1), .05, SOMB); }
    const kf = v('fi'); if (kf > 1e-3) tubo(arco(a => WS(.7, a, t), 0, f * Math.min(1, kf), 30), .012, FI);
    const kt = v('teta'); if (kt > 1e-3) tubo(arco(a => Wp(.75 * Math.cos(a), .75 * Math.sin(a), 0), 0, t * Math.min(1, kt), 40), .012, TH);
    const kxy = sm(v('xy'));
    if (kxy > 1e-3) { tracejado([Wp(...P1), Wp(Pp[0], Pp[1] * (1 - kxy), 0)], .006, E1, .08, .07); tracejado([Wp(...P1), Wp(Pp[0] * (1 - kxy), Pp[1], 0)], .006, E2, .08, .07); }
    bolinha(Wp(...Pp), .07, BR);
    proj('ex', [SC * 2.58, 0, 0]); proj('ey', [0, SC * 2.53, 0]); proj('ez', [0, 0, SC * 2.5]);
    proj('P', Wp(...Pp)); proj('P1', Wp(...P1)); proj('meioRho', Wp(...Pp.map(q => q * .5))); proj('meioR', Wp(P1[0] * .5, P1[1] * .5, 0)); proj('arcoFi', WS(.78, f * .5, t));
    proj('arcoTh', Wp(.85 * Math.cos(t * .45), .85 * Math.sin(t * .45), 0)); proj('meioZ', Wp(Pp[0], Pp[1], Pp[2] * .5)); proj('zEixo', Wp(0, 0, rho * Math.cos(f))); proj('O', [0, 0, 0]);
    proj('xP', Wp(Pp[0], 0, 0)); proj('yP', Wp(0, Pp[1], 0));
  }

  // ---------- caixa (espaço r, φ, θ): bordas ruins uma por vez; caixa2 = partida em θ = π (B1-3, B3-1) ----------
  if (K === 'caixa') {
    SC = 1; const A = 2.2, B = 2.2 / PI, Cc = 3.0 / (2 * PI);
    const meia = v('meia') > .5, sep = v('sep'), nb = v('bordas'), cel = v('celula');
    const Q = (r, f, t) => [r * A, t * Cc + (meia && t > PI - 1e-9 ? sep : 0), f * B];
    const face = (F, a0, a1, b0, b1, c) => sup(F, a0, a1, b0, b1, 2, 2, () => c);
    const cT = t => meia ? (t < PI ? mixc(BG, AZC, .30) : mixc(BG, CORAL, .26)) : mixc(BG, GEO, .20);
    if (meia) {
      face((f, t) => Q(1, f, t), 0, PI, 0, PI - 1e-6, cT(0)); face((f, t) => Q(1, f, t), 0, PI, PI, 2 * PI, cT(4));
      face((r, t) => Q(r, PI, t), 0, 1, 0, PI - 1e-6, cT(0)); face((r, t) => Q(r, PI, t), 0, 1, PI, 2 * PI, cT(4));
      if (sep > 1e-4) { face((r, f) => Q(r, f, PI - 1e-6), 0, 1, 0, PI, mixc(BG, AZC, .22)); face((r, f) => Q(r, f, PI), 0, 1, 0, PI, mixc(BG, CORAL, .20)); }
    } else { face((f, t) => Q(1, f, t), 0, PI, 0, 2 * PI, mixc(BG, GEO, .24)); face((r, t) => Q(r, PI, t), 0, 1, 0, 2 * PI, mixc(BG, GEO, .30)); }
    face((r, f) => Q(r, f, 0), 0, 1, 0, PI, meia ? mixc(BG, AZC, .36) : mixc(BG, GEO, .18));
    const gl = '#4A4F78', TT = t => (meia && t > PI - 1e-9 ? t : t);
    for (let i = 1; i < 4; i++) { const r = i / 4; tubo([Q(r, 0, 0), Q(r, PI, 0)], .005, gl); tubo([Q(r, PI, 0), Q(r, PI, PI - 1e-6)], .005, gl); tubo([Q(r, PI, PI), Q(r, PI, 2 * PI)], .005, gl); }
    for (let i = 1; i < 6; i++) { const f = PI * i / 6; tubo([Q(0, f, 0), Q(1, f, 0)], .005, gl); tubo([Q(1, f, 0), Q(1, f, PI - 1e-6)], .005, gl); tubo([Q(1, f, PI), Q(1, f, 2 * PI)], .005, gl); }
    for (let i = 1; i < 12; i++) { const t = 2 * PI * i / 12; tubo([Q(1, 0, TT(t)), Q(1, PI, TT(t))], .005, gl); tubo([Q(0, PI, TT(t)), Q(1, PI, TT(t))], .005, gl); }
    const ar = [[[0, 0, 0], [1, 0, 0]], [[1, 0, 0], [1, PI, 0]], [[1, PI, 0], [0, PI, 0]], [[1, 0, 0], [1, 0, PI - 1e-6]], [[1, 0, PI], [1, 0, 2 * PI]], [[1, PI, 0], [1, PI, PI - 1e-6]], [[1, PI, PI], [1, PI, 2 * PI]],
      [[1, 0, 2 * PI], [1, PI, 2 * PI]], [[1, PI, 2 * PI], [0, PI, 2 * PI]]];
    for (const p of ar) tubo(p.map(q => Q(...q)), .010, GEO);
    if (meia && sep > 1e-4) for (const t of [PI - 1e-6, PI]) tubo([Q(0, PI, t), Q(1, PI, t), Q(1, 0, t)], .010, GEO);
    // bordas ruins (ALERTA tracejado): 1 = a face r = 0; 2 = as faces φ = 0 e φ = π; 3 = as faces θ = 0 e θ = 2π
    const borda = (cs) => { const qs = cs.map(q => Q(...q)); tracejado([...qs, qs[0]], .012, AL, .10, .07); };
    if (nb >= 1) borda([[0, 0, 0], [0, PI, 0], [0, PI, 2 * PI], [0, 0, 2 * PI]]);
    if (nb >= 2) { borda([[0, PI, 0], [1, PI, 0], [1, PI, 2 * PI], [0, PI, 2 * PI]]); borda([[0, 0, 0], [1, 0, 0], [1, 0, 2 * PI], [0, 0, 2 * PI]]); }
    if (nb >= 3) { borda([[0, 0, 0], [1, 0, 0], [1, PI, 0], [0, PI, 0]]); borda([[0, 0, 2 * PI], [1, 0, 2 * PI], [1, PI, 2 * PI], [0, PI, 2 * PI]]); }
    if (meia && v('corte') > .5) tracejado([Q(0, PI, PI - 1e-6), Q(1, PI, PI - 1e-6), Q(1, 0, PI - 1e-6)], .013, AL, .10, .07);
    const t1 = 3 * PI / 2 + .15, t2 = t1 + PI / 6;
    if (cel > .5) {
      sup((f, t) => Q(1.004, f, t), PI / 3, PI / 2, t1, t2, 1, 1, () => mixc(BG, LI, .80));
      tubo([Q(1, PI / 3, t1), Q(1, PI / 2, t1), Q(1, PI / 2, t2), Q(1, PI / 3, t2), Q(1, PI / 3, t1)], .010, LI);
      for (const t of [t1, t2]) tracejado([Q(1, PI / 3, t), Q(.5, PI / 3, t), Q(.5, PI / 2, t)], .006, LI, .06, .05); tracejado([Q(.5, PI / 3, t1), Q(.5, PI / 3, t2)], .006, LI, .06, .05);
    }
    seta(Q(1, 0, 0), Q(1.38, 0, 0), .014, RO); seta(Q(1, 0, 2 * PI), Q(1, 0, 2 * PI + .9), .014, TH); seta(Q(0, PI, 0), Q(0, PI + .55, 0), .014, FI);
    proj('eRho', Q(1.5, 0, 0)); proj('eTh', Q(1, 0, 2 * PI + 1.05)); proj('eFi', Q(0, PI + .68, 0)); proj('um', Q(1, 0, 0)); proj('pi', Q(0, PI, 0)); proj('dois_pi', Q(1, 0, 2 * PI)); proj('zero', Q(0, 0, 0));
    proj('cel', Q(1, 5 * PI / 12, (t1 + t2) / 2)); proj('faceR0', Q(0, PI / 2, 0)); proj('faceT0', Q(.5, PI / 2, 0)); proj('arestaR0', Q(0, PI, PI)); proj('meioT', Q(1, PI, PI));
    proj('cima', Q(1, PI / 2, PI / 2)); proj('baixo', Q(1, PI / 2, 3 * PI / 2)); proj('cortePi', Q(.5, PI, PI)); proj('piTh', Q(1, 0, PI));
    proj('m1', Q(.5, PI / 2, PI / 2)); proj('m2', Q(.5, PI / 2, 3 * PI / 2));
  }

  // ---------- bolagrade: a imagem da caixa; bordas ruins; célula; costura; região e sonda da receita (B1-3, B2-4, B3-1, B3-2) ----------
  if (K === 'bolagrade') {
    SC = 2.1; const nb = v('bordas');
    sup((f, t) => WS(1, f, t), 0, PI, PI * .25, PI * 1.25, 40, 60, (f, t) => mixc(BG, GEO, .10 + .06 * Math.max(0, Math.cos(f))));
    esferaTraco(1, { nm: 12, np: [PI / 6, PI / 3, PI / 2, 2 * PI / 3, 5 * PI / 6], cor: '#5C6488' });
    esferaTraco(.5, { nm: 0, np: [PI / 2], cor: '#4A4F78' });
    if (nb >= 3) { sup((r, f) => WS(r, f, 0), 0, 1, 0, PI, 6, 40, () => mixc(BG, AL, .22)); tubo(arco(f => WS(1, f, 0), 0, PI, 60), .010, AL); }
    if (nb >= 2) tracejado([Wp(0, 0, -1), Wp(0, 0, 1)], .013, AL, .09, .06);
    else tubo([Wp(0, 0, -1.12), Wp(0, 0, 1.12)], .006, EZ);
    if (nb >= 1) bolinha([0, 0, 0], .06, AL);
    const kra = sm(v('raio')), kme = sm(v('meridiano')), kvo = sm(v('volta'));
    if (kra > 1e-3) tubo([Wp(0, 0, 0), WS(kra, PI / 2, -.25)], .011, BR);                          // B2-4: o raio R
    if (kme > 1e-3) tubo(arco(f => WS(1.01, f, -PI * .5), 0, PI * kme, Math.max(4, Math.round(60 * kme))), .012, FI);   // B2-4: o φ vai de 0 a π
    if (kvo > 1e-3) tubo(arco(t => WS(1.01, PI / 2, t), -PI * .5, -PI * .5 + 2 * PI * kvo, Math.max(4, Math.round(160 * kvo))), .012, TH);   // B2-4: a volta inteira
    const t1 = -PI / 2 + .15, t2 = t1 + PI / 6;
    if (v('celula') > .5) celula(.5, 1, PI / 3, PI / 2, t1, t2);
    // B3-2: região genérica (casca entre dois cones, só contorno) e a sonda radial (entra azul-claro, sai coral)
    const ra = .45, rb = .9, fa = PI / 6, fb = PI / 3, ts = -PI * .42;
    if (v('regiao') > .5) {
      for (const r of [ra, rb]) for (const f of [fa, fb]) tubo(arco(t => WS(r, f, t), 0, 2 * PI, 120), .009, GEO);
      for (const t of [ts - .9, ts + .9]) { tubo(arco(f => WS(ra, f, t), fa, fb, 20), .009, GEO); tubo(arco(f => WS(rb, f, t), fa, fb, 20), .009, GEO);
        for (const f of [fa, fb]) tubo([WS(ra, f, t), WS(rb, f, t)], .009, GEO); }
    }
    const sd = v('sonda'), fs = PI / 4;
    if (sd > 1e-3) { const L = 1.05 * sd; tubo([Wp(0, 0, 0), WS(L, fs, ts)], .014, RO); bolinha([0, 0, 0], .05, BR);
      if (L >= ra) bolinha(WS(ra, fs, ts), .055, AZC); if (L >= rb) bolinha(WS(rb, fs, ts), .055, CORAL); }
    proj('cel', WS(1.05, 5 * PI / 12, (t1 + t2) / 2)); proj('origem', [0, 0, 0]); proj('eixo', Wp(0, 0, .85)); proj('costura', WS(.75, PI * .6, 0)); proj('ez', [0, 0, SC * 1 + .25]);
    proj('raioM', WS(.6, PI / 2, -.25)); proj('meridiano', WS(1.04, PI * .62, -PI * .5)); proj('volta', WS(1.03, PI / 2, -PI * .2)); proj('polo', WS(1.0, 0, 0)); proj('sul', WS(1.0, PI, 0));
    proj('entra', WS(ra, fs, ts)); proj('sai', WS(rb, fs, ts)); proj('regiao', WS(.68, PI / 4, ts + .9));
  }

  // ---------- caixinha: zoom na célula do equador; as três arestas uma por vez (B2-1) ----------
  if (K === 'caixinha') {
    SC = 2.6; const r1 = .62, r2 = 1, f1 = PI / 3, f2 = PI / 2 - .06, t1 = .30, t2 = .82, na = v('aresta');
    esferaTraco(1, { nm: 0, np: [PI / 2], cor: '#4A4F78' });
    tubo([Wp(0, 0, -.30), Wp(0, 0, 1.0)], .010, EZ);       // o alvo 06 recortava o PNG em y = 150: o eixo para em z = 1 (não cruza o canto)
    celula(r1, r2, f1, f2, t1, t2, LI, { w: .007, borda: '#9DBF52' });
    const zc = r2 * Math.cos(f2);
    const a1 = sm(Math.min(1, Math.max(0, na))), a2 = sm(Math.min(1, Math.max(0, na - 1))), a3 = sm(Math.min(1, Math.max(0, na - 2))), kr = sm(v('raioPar'));
    if (a1 > 1e-3) tubo([WS(r1, f2, t1), WS(r1 + (r2 - r1) * a1, f2, t1)], .020, RO);
    if (a2 > 1e-3) { tubo(arco(f => WS(r2, f, t1), f2, f2 - (f2 - f1) * a2, 30), .020, FI); if (a2 > .999) { tracejado(arco(f => WS(r2, f, t1), 0, f1, 60), .006, FI, .07, .06); tracejado([Wp(0, 0, 0), WS(r2, f1, t1)], .007, RO, .07, .05); tubo(arco(f => WS(.30, f, t1), 0, f1, 30), .010, FI); } }
    if (a3 > 1e-3) { tubo(arco(t => WS(r2, f2, t), t1, t1 + (t2 - t1) * a3, 30), .020, TH); if (a3 > .999) tracejado(arco(t => WS(r2, f2, t), t2, t1 + 2 * PI, 200), .006, TH, .07, .06); }
    if (kr > 1e-3) { const A0 = sph(r2, f2, t1); tracejado([Wp(0, 0, zc), Wp(A0[0] * kr, A0[1] * kr, zc)], .010, SOMB, .07, .05); }
    proj('dRho', WS((r1 + r2) / 2, f2, t1)); proj('dFi', WS(r2, (f1 + f2) / 2, t1)); proj('dTh', WS(r2, f2, (t1 + t2) / 2)); proj('raioPar', Wp(...sph(r2, f2, t1).map((q, i) => i < 2 ? q * .5 : zc)));
    proj('eixoPar', Wp(0, 0, zc)); proj('O', [0, 0, 0]); proj('arcoFi', WS(.34, f1 * .5, t1)); proj('ez', Wp(0, 0, 1.24)); proj('cel', WS(r2, (f1 + f2) / 2, (t1 + t2) / 2)); proj('canto', WS(r2, f2, t1));
  }

  // ---------- cebola: a casca de r ∈ [0,6; 0,7]; as cascas acendem do centro para fora (só contorno) e voltam (B4) ----------
  if (K === 'cebola') {
    SC = 2.1; const ta = CAZ - PI / 4, tb = CAZ + PI / 4, ac = v('casca', 1), onda = v('onda');
    sup((f, t) => WS(1, f, t), 0, PI, tb, ta + 2 * PI, 40, 90, (f, t) => tom(mixc(BG, GEO, .62), sph(1, f, t), .30, .30));
    const rs = [0, .2, .4, .6, .7, .8, 1];
    for (const t of [ta, tb]) for (let i = 0; i + 1 < rs.length; i++) {
      const a = rs[i], b = rs[i + 1], acesa = (a === .6) && ac > .5;
      sup((r, f) => WS(r, f, t), a, b, 0, PI, 2, 50, () => acesa ? mixc(BG, RO, .70) : mixc(BG, GEO, (i % 2) ? .20 : .13));
    }
    for (const r of [.2, .4, .8]) for (const t of [ta, tb]) tubo(arco(f => WS(r, f, t), 0, PI, 50), .005, '#8E98B8');
    if (ac > .5) for (const t of [ta, tb]) for (const r of [.6, .7]) tubo(arco(f => WS(r, f, t), 0, PI, 50), .010, RO);
    for (const t of [ta, tb]) tubo(arco(f => WS(1, f, t), 0, PI, 60), .010, GEO);
    for (let k = 1; k <= 3; k++) { const t = ta + (tb - ta) * k / 4; tubo(arco(f => WS(1, f, t), 0, PI, 60), .005, TR); }
    if (ac > .5) tubo(arco(t => WS(.7, PI / 2, t), ta, tb, 30), .006, '#9A6A44');
    if (onda > 1e-3 && onda < .999) {        // 5 cascas finas acendem do centro para fora: a casca k (de 0,2k a 0,2k + 0,2) ganha o contorno laranja
      const k = Math.min(4, Math.floor(onda * 5)), a = .2 * k, b = a + .2;
      for (const t of [ta, tb]) { if (a > 1e-3) tubo(arco(f => WS(a, f, t), 0, PI, 50), .010, RO); tubo(arco(f => WS(Math.min(b, 1.004), f, t), 0, PI, 50), .010, RO); }
    }
    tubo([Wp(0, 0, -1), Wp(0, 0, 1.25)], .009, EZ);
    proj('casca', WS(.65, PI * .25, ta)); proj('espessura', WS(.65, PI * .62, tb)); proj('raio', WS(.33, PI / 2, ta)); proj('centro', [0, 0, 0]); proj('fora', WS(1.03, PI * .62, tb + .9));
  }

  // ---------- casquinha: cone φ = π/4 + calota r = 2 cos φ, gomo aberto; a sonda cresce; as duas peças por cor (B6) ----------
  if (K === 'casquinha') {
    SC = 1.55; const CA = Math.atan2(-6.4, 8.6), ta = CA - PI / 9, tb = CA + PI / 2, R2 = f => 2 * Math.cos(f), duas = v('duas') > .5;
    sup((r, t) => WS(r, PI / 4, t), 0, Math.SQRT2, tb, ta + 2 * PI, 10, 90, (r, t) => tom(FI, [Math.cos(t), Math.sin(t), -1], .30, .30));
    sup((f, t) => WS(R2(f), f, t), 0, PI / 4, tb, ta + 2 * PI, 24, 90, (f, t) => tom(CI, sph(1, f, t).map((q, i) => i < 2 ? q : q - .2), .32, .36));
    if (!duas) for (const t of [ta, tb]) sup((s, f) => WS(s * R2(f), f, t), 0, 1, 0, PI / 4, 10, 30, () => mixc(BG, GEO, .30));
    else for (const t of [ta, tb]) {               // a mesma face do corte, pintada em duas peças: cone (z ≤ 1) violeta, meia bola (z ≥ 1) ciano
      sup((s, f) => { const rr = s * Math.min(R2(f), 1 / Math.cos(f)); return WS(rr, f, t); }, 0, 1, 0, PI / 4, 10, 30, () => mixc(BG, FI, .42));
      sup((s, f) => { const r0 = 1 / Math.cos(f), rr = r0 + s * (R2(f) - r0); return WS(rr, f, t); }, 0, 1, 0, PI / 4, 6, 30, () => mixc(BG, CI, .40));
      tubo([Wp(0, 0, 1), Wp(Math.cos(t), Math.sin(t), 1)], .007, GEO);
    }
    for (const t of [ta, tb]) { tubo(arco(f => WS(R2(f), f, t), 0, PI / 4, 40), .011, CORAL); tubo([Wp(0, 0, 0), WS(Math.SQRT2, PI / 4, t)], .011, FI); }
    for (const k of [1, 2, 3]) { const t = ta + (tb - ta) * k / 4; tubo(arco(f => WS(R2(f), f, t), 0, PI / 4, 30), .005, TR); tubo([Wp(0, 0, 0), WS(Math.SQRT2, PI / 4, t)], .005, TR); }
    tubo(arco(t => WS(Math.SQRT2, PI / 4, t), tb, ta + 2 * PI, 140), .009, BR); tubo(arco(t => WS(Math.SQRT2, PI / 4, t), ta, tb, 40), .005, TR);
    tubo([Wp(0, 0, -.2), Wp(0, 0, 2.5)], .010, EZ); seta([0, 0, 0], [SC * 1.6, 0, 0], .011, E1); seta([0, 0, 0], [0, SC * 1.6, 0], .011, E2);
    const fs = PI / 6, tm = tb - .035, sd = v('sonda');
    if (sd > 1e-3) { tubo([Wp(0, 0, 0), WS(R2(fs) * Math.min(1, sd), fs, tm)], .015, RO); bolinha([0, 0, 0], .06, AZC); if (sd >= .999) bolinha(WS(R2(fs), fs, tm), .06, CORAL); }
    if (v('arcofi') > .5) tubo(arco(f => WS(.55, f, tm), 0, fs, 20), .010, FI);
    if (v('encontro') > .5) bolinha(WS(Math.SQRT2, PI / 4, CA - PI * .3), .055, BR);
    proj('O', [0, 0, 0]); proj('saida', WS(R2(fs), fs, tm)); proj('cone', WS(1.05, PI / 4, CA - PI * .45)); proj('calota', WS(R2(.35), .35, CA - PI * .5)); proj('encontro', WS(Math.SQRT2, PI / 4, CA - PI * .3)); proj('limite', WS(R2(PI / 4) * .5, PI / 4, tm));
    proj('arcoFi', WS(.62, fs * .5, tm)); proj('meioSonda', WS(R2(fs) * .55, fs, tm)); proj('topo', Wp(0, 0, 2)); proj('ez', Wp(0, 0, 2.6)); proj('ex', [SC * 1.72, 0, 0]); proj('ey', [0, SC * 1.72, 0]); proj('um', Wp(0, 0, 1));
    proj('faceA', WS(.8, PI / 8, ta)); proj('faceB', WS(.8, PI / 8, tb)); proj('encChao', Wp(Math.cos(CA - PI * .3), Math.sin(CA - PI * .3), 0));
    proj('pecaCone', WS(.75, PI / 8, tb)); proj('pecaBola', WS(1.55, PI / 10, tb));
  }

  // ---------- lata: cilindro r ≤ 1, 0 ≤ z ≤ 1 cortado em cunha; duas sondas e a diagonal da quina (S2) ----------
  if (K === 'lata') {
    SC = 2.2; const CA = Math.atan2(-6.3, 8.4), ta = CA - PI / 9, tb = CA + PI / 2, tm = tb - .03;
    sup((z, t) => Wp(Math.cos(t), Math.sin(t), z), 0, 1, tb, ta + 2 * PI, 4, 96, (z, t) => tom(GEO, [-Math.cos(t), -Math.sin(t), 0], .12, .20));
    sup((r, t) => Wp(r * Math.cos(t), r * Math.sin(t), 1), 0, 1, tb, ta + 2 * PI, 4, 96, () => mixc(BG, GEO, .30));
    for (const t of [ta, tb]) sup((r, z) => Wp(r * Math.cos(t), r * Math.sin(t), z), 0, 1, 0, 1, 2, 2, () => mixc(BG, GEO, .20));
    for (const z of [0, 1]) tubo(arco(t => Wp(Math.cos(t), Math.sin(t), z), tb, ta + 2 * PI, 120), .009, GEO);
    for (const z of [0, 1]) tubo(arco(t => Wp(Math.cos(t), Math.sin(t), z), ta, tb, 40), .005, TR);
    for (const t of [ta, tb]) tubo([Wp(0, 0, 0), Wp(Math.cos(t), Math.sin(t), 0), Wp(Math.cos(t), Math.sin(t), 1), Wp(0, 0, 1)], .008, GEO);
    const kq = v('quina'); if (kq > 1e-3) tracejado([Wp(0, 0, 0), Wp(Math.cos(tm) * Math.min(1, kq), Math.sin(tm) * Math.min(1, kq), Math.min(1, kq))], .009, CORAL, .07, .05);
    tubo([Wp(0, 0, -.15), Wp(0, 0, 1.45)], .010, EZ);
    const s1 = PI / 3, s2 = PI / 8, p1 = WS(1 / Math.sin(s1), s1, tm), p2 = WS(1 / Math.cos(s2), s2, tm);
    const k1 = v('sonda1'), k2 = v('sonda2');
    if (k1 > 1e-3) { tubo([Wp(0, 0, 0), p1.map(q => q * Math.min(1, k1))], .013, RO); if (k1 >= .999) bolinha(p1, .055, CORAL); }
    if (k2 > 1e-3) { tubo([Wp(0, 0, 0), p2.map(q => q * Math.min(1, k2))], .013, RO); if (k2 >= .999) bolinha(p2, .055, CORAL); }
    if (k1 > 1e-3 || k2 > 1e-3) bolinha([0, 0, 0], .055, AZC);
    proj('O', [0, 0, 0]); proj('parede', p1); proj('tampa', p2); proj('quina', Wp(Math.cos(tm), Math.sin(tm), 1)); proj('meio1', Wp(...sph(1 / Math.sin(s1) * .55, s1, tm))); proj('meio2', Wp(...sph(1 / Math.cos(s2) * .6, s2, tm)));
    proj('ez', Wp(0, 0, 1.55)); proj('lado', Wp(Math.cos(tb + 1.2), Math.sin(tb + 1.2), .5)); proj('meioQ', Wp(Math.cos(tm) * .5, Math.sin(tm) * .5, .5));
  }
  R.render(S, cam);
  return PTS;
};
window.cenaPronta = true;
