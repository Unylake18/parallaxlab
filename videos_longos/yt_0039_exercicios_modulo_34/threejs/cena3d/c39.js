// yt_0039 · cenas 3D (porte de referencia/yt_0039_quadros_alvo_v1/c3d39.html, three.js r128; motor do c37.js do yt_0037).
// Uma página por cena (octante.html, pappus.html) define window.CENA_ID. Estilo da série: opaco e sem luz (MeshBasicMaterial), tom por face
// calculado uma vez (normal · direção fixa), sem sombra/névoa/brilho, outputEncoding linear, antialias, fundo transparente (o Manim põe o violeta).
// A CÂMERA VEM DO MANIM no estado: {pos, tgt, up, cx, cy, fov} (perspectiva + setViewOffset: o alvo cai em (cx, cy) px de 1080p) ou, com
// orto = true, a OrthographicCamera de k px por unidade do mundo (pouso).
// octante: casca da esfera de raio SC no 1º octante (tom pela normal, #123A5A → #2FA9D6), quarto de disco no chão, paredes de corte x = 0 e y = 0,
//   três arcos de borda (tubo GEO fino), setas x (âmbar), y (magenta), z (branco). Estados: casca (0 → 1: a casca sobe do chão; z escala).
// pappus: perfil da chapa no plano (x, s), s = distância ao eixo x; giro G(x, s, φ) = [x, s·sen φ, s·cos φ]. Estados: forma (md | arr | toro),
//   phi (0 → 2π, o ângulo da chapa que avança), solido (0 → 1: opacidade do sólido varrido, 1 = opaco; < 1 só na saída do sólido), traco (1: o
//   sólido varrido inteiro vira traço GEO de meridianos e paralelos), quad (0/1: o quadradinho lima), anel (0 → 1: o anel lima que o quadradinho
//   percorre), circ (0 → 1: o círculo tracejado magenta do centroide/centro), cfrac (raio do círculo, em unidades de SC).
const T = THREE, PI = Math.PI, K = window.CENA_ID;
const W = window.innerWidth, H = window.innerHeight, ESC = W / 1920;
const R = new T.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
R.setPixelRatio(1); R.setSize(W, H, false); R.setClearColor(0x000000, 0); R.outputEncoding = T.LinearEncoding;
document.body.appendChild(R.domElement);
const S = new T.Scene(); T.Object3D.DefaultUp.set(0, 0, 1);
const camP = new T.PerspectiveCamera(22, W / H, .05, 4000), camO = new T.OrthographicCamera(-1, 1, 1, -1, .05, 4000);
let cam = camP;
const BG = '#131030', E1 = '#FFC24D', E2 = '#EA63FF', GEO = '#B8C4DA', BR = '#F5F7FF', LIMA = '#C6F26B', SOL0 = '#123A5A', SOL1 = '#2FA9D6',
  CHAPA = '#9AA6C4';
const C = h => new T.Color(h), mixc = (a, b, t) => C(a).lerp(C(b), t);
let G = null, PTS = {};
const sm = u => { u = Math.min(1, Math.max(0, u)); return u * u * (3 - 2 * u); };

function aplicaCam(c) {
  if (c.orto) {
    cam = camO;
    const k = c.k;
    camO.left = -c.cx / k; camO.right = (1920 - c.cx) / k; camO.top = c.cy / k; camO.bottom = -(1080 - c.cy) / k;
    camO.near = .05; camO.far = 4000;
    camO.up.set(...c.up); camO.position.set(...c.pos); camO.lookAt(...c.tgt);
    camO.updateProjectionMatrix(); camO.updateMatrixWorld(true);
  } else {
    cam = camP;
    camP.fov = c.fov || 22;
    const dd = Math.hypot(c.pos[0] - c.tgt[0], c.pos[1] - c.tgt[1], c.pos[2] - c.tgt[2]);
    camP.near = Math.max(.05, dd - 30); camP.far = dd + 30;
    camP.up.set(...c.up); camP.position.set(...c.pos); camP.lookAt(...c.tgt);
    camP.setViewOffset(W, H, (960 - c.cx) * ESC, (540 - c.cy) * ESC, W, H);
    camP.updateProjectionMatrix(); camP.updateMatrixWorld(true);
  }
}
function proj(nome, v) { const q = new T.Vector3(...v).project(cam); PTS[nome] = [+((q.x + 1) / 2 * 1920).toFixed(2), +((1 - q.y) / 2 * 1080).toFixed(2)]; }
function add(o) { G.add(o); return o; }
function poli(pts) { const cp = new T.CurvePath(); for (let i = 0; i + 1 < pts.length; i++) cp.add(new T.LineCurve3(new T.Vector3(...pts[i]), new T.Vector3(...pts[i + 1]))); return cp; }
const tubo = (pts, r, cor) => pts.length > 1 ? add(new T.Mesh(new T.TubeGeometry(poli(pts), Math.max(8, (pts.length - 1) * 2), r, 8, false), new T.MeshBasicMaterial({ color: C(cor) }))) : null;
function tracejado(pts, r, cor, on = 6, off = 5) { for (let i = 0; i < pts.length - 1; i += on + off) { const seg = pts.slice(i, Math.min(pts.length, i + on + 1)); if (seg.length > 1) tubo(seg, r, cor); } }
function seta3(a, b, cor, r = .018) {
  tubo([a, b], r, cor); const d = new T.Vector3(...b).sub(new T.Vector3(...a)).normalize();
  const cone = add(new T.Mesh(new T.ConeGeometry(r * 3.2, r * 11, 12), new T.MeshBasicMaterial({ color: C(cor) })));
  cone.position.set(...new T.Vector3(...b).addScaledVector(d, r * 5).toArray()); cone.quaternion.setFromUnitVectors(new T.Vector3(0, 1, 0), d);
}
function malha(tris, op = 1) {
  const pos = [], col = []; for (const [a, b, c, cc] of tris) { for (const p of [a, b, c]) { pos.push(...p); col.push(cc.r, cc.g, cc.b); } }
  const g = new T.BufferGeometry(); g.setAttribute('position', new T.Float32BufferAttribute(pos, 3)); g.setAttribute('color', new T.Float32BufferAttribute(col, 3));
  const mt = new T.MeshBasicMaterial({ vertexColors: true, side: T.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  if (op < .999) { mt.transparent = true; mt.opacity = op; mt.depthWrite = false; }
  return add(new T.Mesh(g, mt));
}
const DIR = new T.Vector3(.35, -.55, .76).normalize();
function tom(n, c0 = SOL0, c1 = SOL1) { const t = Math.max(0, Math.min(1, .5 + .5 * n.dot(DIR))); return mixc(c0, c1, Math.pow(t, 1.1)); }
function quad(a, b, c, d, cc, T3) { T3.push([a, b, c, cc], [a, c, d, cc]); }
function nrm(a, b, c) { const A = new T.Vector3(...a), B = new T.Vector3(...b), Cc = new T.Vector3(...c); return B.sub(A).cross(Cc.sub(A)).normalize(); }

window.setEstado = e => {
  if (G) { S.remove(G); G.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.material) o.material.dispose(); }); }
  G = new T.Group(); S.add(G); PTS = {};
  aplicaCam(e.cam);

  if (K === 'octante') {
    const SC = e.SC ?? 2.4, cr = Math.max(1e-3, sm(e.casca ?? 1)), T3 = [];
    const piso = e.piso ? C(e.piso) : mixc(BG, GEO, .30);
    const nr = 40, nt = 60;
    for (let i = 0; i < nr; i++) for (let j = 0; j < nt; j++) {
      const r0 = SC * i / nr, r1 = SC * (i + 1) / nr, t0 = PI / 2 * j / nt, t1 = PI / 2 * (j + 1) / nt, P = (r, t) => [r * Math.cos(t), r * Math.sin(t), 0];
      quad(P(r0, t0), P(r1, t0), P(r1, t1), P(r0, t1), piso, T3);
    }
    const Sp = (ph, th) => [SC * Math.sin(ph) * Math.cos(th), SC * Math.sin(ph) * Math.sin(th), SC * Math.cos(ph) * cr];
    if (cr > .002) {
      const np = 48, nq = 48;
      for (let i = 0; i < np; i++) for (let j = 0; j < nq; j++) {
        const p0 = PI / 2 * i / np, p1 = PI / 2 * (i + 1) / np, t0 = PI / 2 * j / nq, t1 = PI / 2 * (j + 1) / nq;
        const pm = (p0 + p1) / 2, tm = (t0 + t1) / 2;
        const n = new T.Vector3(Math.sin(pm) * Math.cos(tm), Math.sin(pm) * Math.sin(tm), Math.cos(pm)).normalize();   // tom da casca pronta
        quad(Sp(p0, t0), Sp(p1, t0), Sp(p1, t1), Sp(p0, t1), tom(n), T3);
      }
      for (let i = 0; i < nr; i++) for (let j = 0; j < nt; j++) {
        const r0 = SC * i / nr, r1 = SC * (i + 1) / nr, t0 = PI / 2 * j / nt, t1 = PI / 2 * (j + 1) / nt;
        const A = (r, t) => [r * Math.cos(t), 0, r * Math.sin(t) * cr], B = (r, t) => [0, r * Math.cos(t), r * Math.sin(t) * cr];
        quad(A(r0, t0), A(r1, t0), A(r1, t1), A(r0, t1), mixc(BG, SOL1, .38), T3); quad(B(r0, t0), B(r1, t0), B(r1, t1), B(r0, t1), mixc(BG, SOL1, .30), T3);
      }
    }
    malha(T3);
    const arco = (f, n = 90) => Array.from({ length: n + 1 }, (_, k) => f(PI / 2 * k / n));
    tubo(arco(t => [SC * Math.cos(t), SC * Math.sin(t), 0.004]), .012, GEO);
    if (cr > .02) { tubo(arco(t => [SC * Math.cos(t), 0, SC * Math.sin(t) * cr]), .012, GEO); tubo(arco(t => [0, SC * Math.cos(t), SC * Math.sin(t) * cr]), .012, GEO); }
    const lx = e.lx ?? SC + .55, lz = e.lz ?? SC + .5;
    seta3([0, 0, 0], [lx, 0, 0], E1); seta3([0, 0, 0], [0, lx, 0], E2);
    const zl = e.zl ?? 1;
    if (zl > .02) seta3([0, 0, 0], [0, 0, lz * zl], BR);
    proj('ex', [lx + .2, 0, 0]); proj('ey', [0, lx + .2, 0]); proj('ez', [0, 0, lz * zl + .22]); proj('a_x', [SC, 0, 0]); proj('a_y', [0, SC, 0]);
    proj('a_z', [0, 0, SC * cr]); proj('origem', [0, 0, 0]); proj('casca', Sp(PI / 4.2, PI / 4));
  }

  if (K === 'pappus') {
    const forma = e.forma || 'md';
    const SC = forma === 'md' ? 2.2 : (forma === 'arr' ? 1.15 : 1.0);
    const PH = e.phi ?? 0, sol = e.solido ?? 0, trc = e.traco ?? 0;
    const Gf = (x, s, ph) => [x, s * Math.sin(ph), s * Math.cos(ph)];
    let chapaPts;
    if (forma === 'md') chapaPts = (u, v) => { const r = SC * u, t = PI * v; return [r * Math.cos(t), r * Math.sin(t)]; };
    if (forma === 'arr') chapaPts = (u, v) => { const r = SC * (1 + u), t = PI * v; return [r * Math.cos(t), r * Math.sin(t)]; };
    if (forma === 'toro') chapaPts = (u, v) => { const r = SC * u, t = 2 * PI * v; return [r * Math.cos(t), 2 * SC + r * Math.sin(t)]; };
    const bordas = [], NB = 120, lado = f => Array.from({ length: NB + 1 }, (_, k) => f(k / NB));
    if (forma === 'md') bordas.push(lado(t => { const a = PI * t; return [SC * Math.cos(a), SC * Math.sin(a)]; }));
    if (forma === 'arr') { bordas.push(lado(t => { const a = PI * t; return [2 * SC * Math.cos(a), 2 * SC * Math.sin(a)]; })); bordas.push(lado(t => { const a = PI * t; return [SC * Math.cos(a), SC * Math.sin(a)]; })); }
    if (forma === 'toro') bordas.push(lado(t => { const a = 2 * PI * t; return [SC * Math.cos(a), 2 * SC + SC * Math.sin(a)]; }));
    // sólido varrido de 0 a PH (opaco; opacidade < 1 só na saída)
    const T3 = [];
    if (sol > .002 && PH > 1e-3 && trc < .5) {
      const nph = Math.max(2, Math.round(90 * PH / (2 * PI)));
      for (const B of bordas) for (let k = 0; k < B.length - 1; k++) for (let j = 0; j < nph; j++) {
        const p0 = PH * j / nph, p1 = PH * (j + 1) / nph;
        const a = Gf(B[k][0], B[k][1], p0), b = Gf(B[k + 1][0], B[k + 1][1], p0), c = Gf(B[k + 1][0], B[k + 1][1], p1), d = Gf(B[k][0], B[k][1], p1);
        const mx = (B[k][0] + B[k + 1][0]) / 2, ms = (B[k][1] + B[k + 1][1]) / 2, pm = (p0 + p1) / 2; let n = nrm(a, b, c);
        // normal para fora do perfil (a do ponto médio da borda, girado): tom da casca pronta
        const ctr = new T.Vector3(mx, 0, 0), pmid = new T.Vector3(...Gf(mx, ms, pm));
        if (n.dot(pmid.clone().sub(ctr)) < 0) n.negate(); quad(a, b, c, d, tom(n), T3);
      }
      // a face de corte em φ = 0 (escurecida) fecha o sólido parcial
      if (PH < 2 * PI - 1e-3) {
        const nu = 30, nv = 90;
        for (let i = 0; i < nu; i++) for (let j = 0; j < nv; j++) {
          const q = [chapaPts(i / nu, j / nv), chapaPts((i + 1) / nu, j / nv), chapaPts((i + 1) / nu, (j + 1) / nv), chapaPts(i / nu, (j + 1) / nv)].map(p => Gf(p[0], p[1], 0));
          quad(q[0], q[1], q[2], q[3], mixc(BG, CHAPA, .55), T3);
        }
      }
      malha(T3, sol);
    }
    // a chapa que avança (GEO claro) em φ = PH
    if ((e.chapa ?? 1) > .5) {
      const T4 = [], nu = 40, nv = 90;
      for (let i = 0; i < nu; i++) for (let j = 0; j < nv; j++) {
        const q = [chapaPts(i / nu, j / nv), chapaPts((i + 1) / nu, j / nv), chapaPts((i + 1) / nu, (j + 1) / nv), chapaPts(i / nu, (j + 1) / nv)].map(p => Gf(p[0], p[1], PH));
        quad(q[0], q[1], q[2], q[3], C(CHAPA), T4);
      }
      malha(T4);
      for (const B of bordas) tubo(B.map(p => Gf(p[0], p[1], PH)), .011, GEO);
    }
    // bola (ou bola oca) inteira em traço GEO: meridianos e paralelos (E6-2)
    if (trc > .5) {
      for (const B of bordas) {
        for (let m = 0; m < 12; m++) { const ph = 2 * PI * m / 12; tubo(B.map(p => Gf(p[0], p[1], ph)), .006, GEO); }
        for (let k = 1; k < 6; k++) { const p = B[Math.round(k * (B.length - 1) / 6)]; tubo(Array.from({ length: 121 }, (_, j) => Gf(p[0], p[1], 2 * PI * j / 120)), .006, GEO); }
      }
    }
    // eixo de rotação (âmbar)
    const XM = forma === 'toro' ? 2.0 : (forma === 'md' ? SC + .9 : 2 * SC + .7);
    seta3([-XM, 0, 0], [XM, 0, 0], E1, .02);
    if (forma === 'md') {
      const y0 = .6 * SC, h = .28, xq = -.55;
      if ((e.quad ?? 0) > .5) {
        const sq = [[xq - h / 2, y0 - h / 2], [xq + h / 2, y0 - h / 2], [xq + h / 2, y0 + h / 2], [xq - h / 2, y0 + h / 2]].map(p => Gf(p[0], p[1], PH));
        const T5 = []; quad(sq[0], sq[1], sq[2], sq[3], C(LIMA), T5);
        const nn = new T.Vector3(...Gf(0, 1, PH + PI / 2)), sg = nn.dot(cam.position.clone().sub(new T.Vector3(...Gf(xq, y0, PH)))) > 0 ? 1 : -1;
        const dn = nn.toArray().map(v => .006 * sg * v);                                 // um fio à frente da chapa (do lado da câmera)
        malha(T5.map(t => [t[0].map((v, i) => v + dn[i]), t[1].map((v, i) => v + dn[i]), t[2].map((v, i) => v + dn[i]), t[3]]));
      }
      const an = e.anel ?? 0;
      if (an > 1e-3) { const f = sm(an), n = Math.max(8, Math.round(180 * f)); tubo(Array.from({ length: n + 1 }, (_, k) => Gf(xq, y0, PH - 2 * PI * f + 2 * PI * f * k / n)), .016, LIMA); }
      proj('quad', Gf(xq, y0, PH)); proj('anel_topo', Gf(xq, y0, PH + PI)); proj('anel_frente', Gf(xq, y0, PH + PI / 2 * 3)); proj('eixo_fim', [XM + .2, 0, 0]);
      proj('centro', [0, 0, 0]); proj('chapa_topo', Gf(0, SC, PH)); proj('borda_dir', [SC, 0, 0]);
      proj('cm', Gf(0, (e.cfrac ?? 4 / (3 * PI)) * SC, PH)); proj('quad_dir', Gf(xq + h / 2 + .02, y0, PH));
    }
    const cf = e.circ ?? 0;
    if (cf > 1e-3) {
      const yb = (e.cfrac ?? (forma === 'arr' ? 28 / (9 * PI) : (forma === 'toro' ? 2 : 4 / (3 * PI)))) * SC, f = sm(cf), n = Math.max(6, Math.round(240 * f));
      tracejado(Array.from({ length: n + 1 }, (_, k) => Gf(0, yb, PH - 2 * PI * f + 2 * PI * f * k / n)), .013, E2, 5, 4);
    }
    if (forma === 'arr') {
      const yb = 28 / (9 * PI) * SC;
      proj('cm', Gf(0, yb, PH)); proj('cm_ini', Gf(0, yb, 0)); proj('cm_fim', Gf(0, yb, PH)); proj('oco', Gf(0, SC * .55, PH * .62)); proj('eixo_fim', [XM + .2, 0, 0]);
      proj('r1', Gf(SC, 0, PH)); proj('r2', Gf(2 * SC, 0, PH)); proj('topo', Gf(0, 2 * SC, PH)); proj('centro', [0, 0, 0]);
      proj('circ_frente', Gf(0, yb, PI / 2)); proj('circ_baixo', Gf(0, yb, PI));
    }
    if (forma === 'toro') {
      proj('centro_disco', Gf(0, 2 * SC, PH)); proj('eixo_fim', [XM + .2, 0, 0]); proj('centro', [0, 0, 0]); proj('topo_disco', Gf(0, 3 * SC, PH));
      proj('base_disco', Gf(0, SC, PH)); proj('circ_baixo', Gf(0, 2 * SC, PI)); proj('circ_frente', Gf(0, 2 * SC, PI / 2));
    }
  }
  // v2 B3 · massa como volume: a chapa ganha altura ρ sobre cada ponto (massa = volume sob o gráfico de ρ). forma: 'elipse' (meia elipse
  // x² + 4y² ≤ 1, ρ = k y: uma rampa, 0 no eixo e máxima no topo) ou 'arruela' (1 ≤ r ≤ 2, ρ = k r: rampa radial, o buraco vazio). alt (0 → 1)
  // = fração da altura (0 = a chapa plana, idêntica ao mapa 2D vista de cima). Cor do topo = o degradê #10243A → ciano do mapa 2D (uma vez por
  // face); paredes escurecidas; sem luz, sem sombra, sem transparência.
  if (K === 'massa') {
    const forma = e.forma || 'elipse', alt = e.alt ?? 1, H = (e.H ?? (forma === 'elipse' ? .55 : .9)) * alt, T3 = [];
    const CI = '#35D9FF', C0 = '#10243A';
    let P, rho, nu, nv, bordas;
    if (forma === 'elipse') {
      P = (s, t) => [s * Math.cos(PI * t), .5 * s * Math.sin(PI * t)]; rho = (x, y) => Math.max(0, y) / .5; nu = 30; nv = 90;
      bordas = [Array.from({ length: 121 }, (_, k) => [Math.cos(PI * k / 120), .5 * Math.sin(PI * k / 120)]), [[-1, 0], [1, 0]]];
    } else {
      P = (s, t) => [(1 + s) * Math.cos(PI * t), (1 + s) * Math.sin(PI * t)]; rho = (x, y) => Math.hypot(x, y) / 2; nu = 24; nv = 90;
      const arc = r => Array.from({ length: 121 }, (_, k) => [r * Math.cos(PI * k / 120), r * Math.sin(PI * k / 120)]);
      bordas = [arc(2), arc(1), [[-2, 0], [-1, 0]], [[1, 0], [2, 0]]];
    }
    const Z = (x, y) => H * rho(x, y), cor = (x, y) => mixc(C0, CI, Math.pow(Math.min(1, rho(x, y)), .85));
    for (let i = 0; i < nu; i++) for (let j = 0; j < nv; j++) {
      const q = [P(i / nu, j / nv), P((i + 1) / nu, j / nv), P((i + 1) / nu, (j + 1) / nv), P(i / nu, (j + 1) / nv)];
      const m = [(q[0][0] + q[2][0]) / 2, (q[0][1] + q[2][1]) / 2];
      quad(...q.map(p => [p[0], p[1], Z(p[0], p[1])]), cor(m[0], m[1]), T3);
    }
    if (H > 1e-3) for (const B of bordas) for (let k = 0; k + 1 < B.length; k++) {
      const a = B[k], b = B[k + 1], m = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2];
      quad([a[0], a[1], 0], [b[0], b[1], 0], [b[0], b[1], Z(...b)], [a[0], a[1], Z(...a)], mixc(BG, cor(...m), .55), T3);
    }
    malha(T3);
    for (const B of bordas) { tubo(B.map(p => [p[0], p[1], Z(p[0], p[1]) + .004]), .007, GEO); if (H > 1e-3) tubo(B.map(p => [p[0], p[1], .002]), .006, GEO); }
    // curvas de nível de ρ no topo (a rampa lida pelos degraus de altura): y constante na elipse, r constante na arruela
    if (H > 1e-3 && (e.niveis ?? 1) > .5 && (e.alt ?? 1) > .12) {
      if (forma === 'elipse') for (const yk of [.1, .2, .3, .4]) { const xm = Math.sqrt(1 - 4 * yk * yk); tubo([[-xm, yk, Z(0, yk) + .006], [xm, yk, Z(0, yk) + .006]], .005, BG); }
      else for (const rk of [1.25, 1.5, 1.75]) tubo(Array.from({ length: 91 }, (_, k) => [rk * Math.cos(PI * k / 90), rk * Math.sin(PI * k / 90), Z(rk, 0) + .006]), .007, BG);
    }
    const ex = forma === 'elipse' ? [-1.1, 1.12, .78] : [-2.35, 2.4, 2.45];
    seta3([ex[0], 0, 0], [ex[1], 0, 0], E1, forma === 'elipse' ? .008 : .014); seta3([0, -.04, 0], [0, ex[2], 0], E2, forma === 'elipse' ? .008 : .014);
    proj('ex', [ex[1], 0, 0]); proj('ey', [0, ex[2], 0]); proj('topo', forma === 'elipse' ? [0, .5, Z(0, .5)] : [0, 2, Z(0, 2)]); proj('origem', [0, 0, 0]);
  }
  R.render(S, cam);
  return PTS;
};
window.cenaPronta = true;
