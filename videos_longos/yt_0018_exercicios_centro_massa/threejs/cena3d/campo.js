// yt_0017 v3 (handoff v3 do lote 1, §1.2 e §1.3): campo de provas em vácuo e a granada de fragmentação que se estilhaça.
//   campo()   — piso escuro com grade fina ciano (10 m; mais forte a cada 50 m) que some no horizonte por névoa, linha de contato
//               (y = 0 do gráfico), céu estrelado parado com brilho magenta baixo no horizonte, marco hexagonal com três luzes ciano.
//   granada() — elipsoide 1 : 1 : 1,3 de aço escuro com 6 anéis × 8 colunas de pastilhas, sulcos entre elas, cinta lisa no topo;
//               espoleta, alavanca e anel (sem massa). O corpo É a união de três cacos: cones a partir do centro sobre três regiões
//               da superfície (fronteiras em zigue-zague, faces de fratura com relevo), com os volumes ajustados às massas 2 : 1 : 1,5.
//               Ponto físico de cada caco = centroide da malha (medidas()). Unidade 3D: 1 = 20 m na física do Manim.
// Tudo por estado (sem relógio): o Manim manda posição física, ângulo e o tempo desde a explosão; os efeitos sem massa (clarão,
// faíscas, fumaça) são função desse tempo.
window.CAMPO = (function () {
  const T3 = THREE, PI = Math.PI, B = B3D;
  const MS = [2, 1, 1.5], MT = 4.5, AZ = 1.3;
  const cl = (x, a, b) => Math.min(b, Math.max(a, x));
  const sm = (a, b, x) => { const t = cl((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); };
  const v3 = (x, y, z) => new T3.Vector3(x, y, z);
  const hex = c => new T3.Color(c);

  // ── superfície da granada (coordenadas do corpo, z = eixo longo) ──────────────────────────────────────────────────────────
  const TH0 = 0.27 * PI, TH1 = 0.93 * PI, NR = 6, NC = 8, HP = 0.075, WG = 0.22;
  function sup(d) {                       // d unitário → ponto da superfície na direção d, fator de sulco (0..1) e coordenada da onda
    const k = 1 / Math.sqrt(d.x * d.x + d.y * d.y + d.z * d.z / (AZ * AZ));
    const pe = d.clone().multiplyScalar(k), qz = pe.z / AZ;
    const th = Math.acos(cl(qz, -1, 1)), ph = Math.atan2(pe.y, pe.x);
    let pad = 0, sul = 0;
    const fu = (th - TH0) / (TH1 - TH0) * NR;
    if (fu > 0 && fu < NR) {
      let fv = ((ph + PI / 2) / (2 * PI) * NC + 0.5) % 1;
      if (fv < 0) fv += 1;
      const s = x => sm(0, WG, x) * sm(0, WG, 1 - x);
      pad = s(fu % 1) * s(fv);
      sul = 1 - cl(pad * 2.4, 0, 1);
    }
    const cinta = 0.045 * sm(0.11 * PI, 0.135 * PI, th) * (1 - sm(TH0 - 0.05 * PI, TH0 - 0.025 * PI, th));
    return { p: pe.multiplyScalar(1 + HP * pad + cinta), sul, wco: Math.acos(cl(-pe.y, -1, 1)) / PI };   // onda: do centro da face visível para fora
  }
  function normal(d) {
    const a = Math.abs(d.x) < 0.9 ? v3(1, 0, 0) : v3(0, 1, 0);
    const t1 = a.sub(d.clone().multiplyScalar(a.dot(d))).normalize(), t2 = d.clone().cross(t1);
    const e = 2e-3, p = sup(d).p;
    const pa = sup(d.clone().addScaledVector(t1, e).normalize()).p.sub(p), pb = sup(d.clone().addScaledVector(t2, e).normalize()).p.sub(p);
    const n = pa.cross(pb).normalize();
    return n.dot(p) < 0 ? n.negate() : n;
  }

  // ── fratura: três regiões em volta de um eixo inclinado (os dois pontos triplos ficam na frente e atrás) ───────────────────
  const W = v3(0.22, -1, 0.16).normalize();
  const E1 = v3(1, 0, 0).sub(W.clone().multiplyScalar(W.x)).normalize(), E2 = W.clone().cross(E1);    // vistos da câmera: direita e cima
  const dir = (a, b) => W.clone().multiplyScalar(Math.cos(a)).addScaledVector(E1, Math.sin(a) * Math.cos(b)).addScaledVector(E2, Math.sin(a) * Math.sin(b));
  const eb = (a, b) => E1.clone().multiplyScalar(-Math.sin(b)).addScaledVector(E2, Math.cos(b));
  const zig = (k, a) => 0.15 * Math.sin(3 * a + 1.3 * k) + 0.07 * Math.sin(8 * a + 2.1 * k) + 0.035 * Math.sin(19 * a + 0.7 * k);
  const ruido = (k, a, t) => 0.11 * Math.sin(PI * t) * Math.sin(a) *
    (Math.sin(5 * a + 3.1 * t + k) + 0.6 * Math.sin(11 * a - 6.3 * t + 2 * k) + 0.3 * Math.sin(23 * a + 9 * t + k));
  let BK = [10, 170, 250].map(g => g * PI / 180);   // fronteiras: 2 kg em cima (90°), 1 kg embaixo à esquerda (210°), 1,5 kg à direita (330°)
  const bnd = (k, a) => (k >= 3 ? BK[0] + 2 * PI : BK[k]) + zig(k % 3, a);

  function face(k, NA, NT, sinal, alvo) {          // face de fratura da fronteira k (compartilhada pelos dois vizinhos)
    const pos = [], idx = [], kk = k % 3;
    for (let i = 0; i <= NA; i++) {
      const a = PI * i / NA, b = bnd(k, a), s = sup(dir(a, b)).p, e = eb(a, b);
      for (let l = 0; l <= NT; l++) { const t = l / NT, q = s.clone().multiplyScalar(t).addScaledVector(e, ruido(kk, a, t)); pos.push(q.x, q.y, q.z); }
    }
    for (let i = 0; i < NA; i++) for (let l = 0; l < NT; l++) {
      const v = (ii, ll) => ii * (NT + 1) + ll, am = PI * (i + 0.5) / NA, des = eb(am, bnd(k, am)).multiplyScalar(sinal);
      tri(pos, idx, v(i, l), v(i + 1, l), v(i + 1, l + 1), des);
      tri(pos, idx, v(i, l), v(i + 1, l + 1), v(i, l + 1), des);
    }
    alvo.push({ pos, idx });
  }
  function tri(pos, idx, a, b, c, des) {           // orienta cada triângulo para fora (des: direção desejada; null = radial)
    const P = j => v3(pos[3 * j], pos[3 * j + 1], pos[3 * j + 2]);
    const A = P(a), n = P(b).sub(A).cross(P(c).sub(A));
    const d = des || A.clone().add(P(b)).add(P(c));
    if (n.dot(d) < 0) idx.push(a, c, b); else idx.push(a, b, c);
  }
  function peca(k, NA, dens, NT, completo) {
    const w = bnd(k + 1, 0) - zig((k + 1) % 3, 0) - (BK[k]);
    const NS = Math.max(6, Math.round(dens * w / (2 * PI)));
    const pos = [], nor = [], sul = [], wco = [], idx = [];
    for (let i = 0; i <= NA; i++) {
      const a = PI * i / NA, b0 = bnd(k, a), b1 = bnd(k + 1, a);
      for (let j = 0; j <= NS; j++) {
        const d = dir(a, b0 + (b1 - b0) * j / NS), s = sup(d);
        pos.push(s.p.x, s.p.y, s.p.z); sul.push(s.sul); wco.push(s.wco);
        if (completo) { const n = normal(d); nor.push(n.x, n.y, n.z); }
      }
    }
    for (let i = 0; i < NA; i++) for (let j = 0; j < NS; j++) {
      const v = (ii, jj) => ii * (NS + 1) + jj;
      tri(pos, idx, v(i, j), v(i + 1, j), v(i + 1, j + 1), null);
      tri(pos, idx, v(i, j), v(i + 1, j + 1), v(i, j + 1), null);
    }
    const faces = [];
    face(k, NA, NT, -1, faces); face(k + 1, NA, NT, +1, faces);
    // volume e centroide (tetraedros a partir da origem; malha fechada)
    let V = 0; const C = v3(0, 0, 0);
    for (const m of [{ pos, idx }, ...faces]) for (let t = 0; t < m.idx.length; t += 3) {
      const P = j => v3(m.pos[3 * j], m.pos[3 * j + 1], m.pos[3 * j + 2]);
      const a = P(m.idx[t]), b = P(m.idx[t + 1]), c = P(m.idx[t + 2]), dv = a.dot(b.clone().cross(c)) / 6;
      V += dv; C.addScaledVector(a.add(b).add(c), dv / 4);
    }
    return { V, C: C.divideScalar(V), ext: { pos, nor, sul, wco, idx }, faces };
  }
  // ajuste das fronteiras: volume de cada caco ∝ massa (malha grossa), depois a malha final
  for (let it = 0; it < 7; it++) {
    const vs = [0, 1, 2].map(k => peca(k, 40, 90, 6, false).V), vt = vs[0] + vs[1] + vs[2];
    const f0 = vs[0] / vt, f1 = vs[1] / vt;
    BK[1] += (MS[0] / MT - f0) * 2 * PI;
    BK[2] += (MS[0] / MT + MS[1] / MT - f0 - f1) * 2 * PI;
  }
  const PECAS = [0, 1, 2].map(k => peca(k, 120, 200, 16, true));
  const VT = PECAS.reduce((s, p) => s + p.V, 0);
  const CB = PECAS.reduce((s, p) => s.addScaledVector(p.C, p.V / VT), v3(0, 0, 0));   // centroide do corpo → origem
  // volume do corpo inteiro por quadratura independente (∫ r³/3 dΩ): confere a soma dos cacos
  let VQ = 0;
  { const N = 360, M = 720;
    for (let i = 0; i < N; i++) { const th = PI * (i + 0.5) / N;
      for (let j = 0; j < M; j++) { const ph = 2 * PI * (j + 0.5) / M, d = v3(Math.sin(th) * Math.cos(ph), Math.sin(th) * Math.sin(ph), Math.cos(th));
        VQ += sup(d).p.lengthSq() ** 1.5 / 3 * Math.sin(th) * (PI / N) * (2 * PI / M); } } }
  const medidas = {
    vol: PECAS.map(p => +p.V.toFixed(5)), vol_corpo: +VQ.toFixed(5), soma: +VT.toFixed(5),
    frac: PECAS.map(p => +(p.V / VQ).toFixed(4)), frac_alvo: MS.map(m => +(m / MT).toFixed(4)),
    cen: PECAS.map(p => p.C.clone().sub(CB).toArray().map(x => +x.toFixed(5))),
    req: PECAS.map(p => +Math.cbrt(3 * p.V / (4 * PI)).toFixed(4)), req_corpo: +Math.cbrt(3 * VQ / (4 * PI)).toFixed(4),
    fronteiras_graus: BK.map(b => +(b * 180 / PI).toFixed(2)),
  };

  // ── materiais (aço escuro com luz B; sulcos emissivos no degradê ciano → magenta; faces de fratura quentes) ─────────────────
  const U = { onda: { value: -1 }, brilho: { value: 0 } };
  function acoSulcos(extra, uu) {
    const u_ = uu || U;
    const m = new T3.MeshStandardMaterial(Object.assign({ color: 0x4A5262, metalness: 0.78, roughness: 0.36, envMapIntensity: 0.62, fog: false }, extra || {}));
    m.onBeforeCompile = sh => {
      sh.uniforms.uOnda = u_.onda; sh.uniforms.uBrilho = u_.brilho;
      sh.vertexShader = 'attribute float sul;\nattribute float wco;\nvarying float vS;\nvarying float vW;\n' +
        sh.vertexShader.replace('#include <begin_vertex>', '#include <begin_vertex>\n  vS = sul; vW = wco;');
      sh.fragmentShader = 'uniform float uOnda;\nuniform float uBrilho;\nvarying float vS;\nvarying float vW;\n' +
        sh.fragmentShader.replace('#include <emissivemap_fragment>', `#include <emissivemap_fragment>
  float onda_ = smoothstep(vW - 0.1, vW, uOnda);
  vec3 cor_ = mix(vec3(0.208, 0.851, 1.0), vec3(0.918, 0.388, 1.0), clamp(vW * 1.35, 0.0, 1.0));
  totalEmissiveRadiance += cor_ * vS * onda_ * uBrilho;`);
    };
    return m;
  }
  const matExt = acoSulcos();
  const matFace = new T3.MeshStandardMaterial({ color: 0x23272F, metalness: 0.35, roughness: 0.75, envMapIntensity: 0.35, emissive: hex(0xFF7A3D),
    emissiveIntensity: 0, fog: false });
  const matFant = acoSulcos({ transparent: true, opacity: 0.25, depthWrite: false, envMapIntensity: 0.4 }, { onda: { value: -1 }, brilho: { value: 0 } });   // fantasmas: sem brilho
  const matDeco = B.mat(0x9AA5B6, 0.8, 0.3, 0.7, { fog: false });

  function geoExt(p) {
    const g = new T3.BufferGeometry(), e = p.ext;
    g.setAttribute('position', new T3.Float32BufferAttribute(e.pos, 3));
    g.setAttribute('normal', new T3.Float32BufferAttribute(e.nor, 3));
    g.setAttribute('sul', new T3.Float32BufferAttribute(e.sul, 1));
    g.setAttribute('wco', new T3.Float32BufferAttribute(e.wco, 1));
    g.setIndex(e.idx); g.translate(-CB.x, -CB.y, -CB.z);
    return g;
  }
  function geoFaces(p) {
    const gs = p.faces.map(f => { const g = new T3.BufferGeometry(); g.setAttribute('position', new T3.Float32BufferAttribute(f.pos, 3)); g.setIndex(f.idx);
      g.translate(-CB.x, -CB.y, -CB.z); g.computeVertexNormals(); return g; });
    return gs;
  }
  const GEX = PECAS.map(geoExt), GFA = PECAS.map(geoFaces);
  const CEN = medidas.cen.map(c => v3(...c));
  // amostras de cada caco (relativas ao centroide), para apoiar no chão sem afundar
  const AMOS = PECAS.map((p, k) => { const a = [], ps = p.ext.pos;
    for (let i = 0; i < ps.length; i += 3 * 5) a.push(v3(ps[i] - CB.x, ps[i + 1] - CB.y, ps[i + 2] - CB.z).sub(CEN[k]));
    return a; });
  const ZMIN_CORPO = Math.min(...PECAS.map(p => Math.min(...p.ext.pos.filter((_, i) => i % 3 === 2)))) - CB.z;
  const EIXOS = [v3(0.3, 0.5, 0.8), v3(-0.7, 0.25, 0.45), v3(0.5, -0.6, -0.35)].map(v => v.normalize());   // eixo de giro de cada caco

  function novaPeca(k, mats) {
    const piv = new T3.Group(), off = new T3.Group();
    off.position.copy(CEN[k]).negate();
    off.add(new T3.Mesh(GEX[k], mats[0]), ...GFA[k].map(g => new T3.Mesh(g, mats[1])));
    piv.add(off);
    return piv;
  }
  function deco() {                                  // espoleta + alavanca + anel com pino: sem massa (somem na explosão)
    const g = new T3.Group(), topo = sup(v3(0, 0, 1)).p.z - CB.z;
    const esp = new T3.Mesh(new T3.CylinderGeometry(0.2, 0.25, 0.3, 28).rotateX(PI / 2), matDeco); esp.position.set(-CB.x, -CB.y, topo + 0.1);
    const curva = new T3.CatmullRomCurve3([v3(0.18, 0, topo + 0.2), v3(0.5, 0, topo + 0.1), v3(0.86, 0, topo - 0.5), v3(1.06, 0, topo - 1.1), v3(1.08, 0, topo - 1.6)]
      .map(v => v.sub(v3(CB.x, CB.y, 0))));
    const alav = new T3.Mesh(new T3.TubeGeometry(curva, 40, 0.05, 8, false), matDeco);
    const anel = new T3.Mesh(new T3.TorusGeometry(0.19, 0.03, 10, 36).rotateY(PI / 2), matDeco); anel.position.set(-0.36 - CB.x, -CB.y, topo + 0.08);
    const pino = new T3.Mesh(new T3.CylinderGeometry(0.03, 0.03, 0.5, 10).rotateZ(PI / 2), matDeco); pino.position.set(-0.12 - CB.x, -CB.y, topo + 0.08);
    g.add(esp, alav, anel, pino);
    return g;
  }

  // ── campo de provas ─────────────────────────────────────────────────────────────────────────────────────────────────────────
  const HOR = hex(0x0E2A52).lerp(hex(0xEA63FF), 0.2);          // cor do horizonte (névoa do piso e base do céu)
  let marcoLuzes = null, comPiso = false;
  function campo() {
    comPiso = true;
    const S = B.scene;
    S.fog = new T3.FogExp2(HOR, 0.0095);          // a grade some antes de adensar no horizonte
    const piso = new T3.Mesh(new T3.PlaneGeometry(1400, 900), new T3.MeshBasicMaterial({ color: 0x070B18 }));
    piso.position.set(60, 420, -0.004); S.add(piso);
    const linhas = (passo, op) => { const p = [];
      for (let x = -200; x <= 330; x += passo) p.push(x, -40, 0, x, 860, 0);
      for (let y = -40; y <= 860; y += passo) p.push(-200, y, 0, 330, y, 0);
      const g = new T3.BufferGeometry(); g.setAttribute('position', new T3.Float32BufferAttribute(p, 3));
      return new T3.LineSegments(g, new T3.LineBasicMaterial({ color: 0x35D9FF, transparent: true, opacity: op, depthWrite: false })); };
    S.add(linhas(0.5, 0.16), linhas(2.5, 0.34));                 // 10 m e 50 m (1 unidade = 20 m)
    const contato = new T3.Mesh(new T3.PlaneGeometry(530, 0.05), new T3.MeshBasicMaterial({ color: 0x9CC2F0, transparent: true, opacity: 0.75, depthWrite: false }));
    contato.position.set(65, 0, 0.001); S.add(contato);
    // marco de lançamento: base hexagonal de aço, três luzes ciano
    const marco = new T3.Group();
    const base = new T3.Mesh(new T3.CylinderGeometry(0.44, 0.5, 0.08, 6).rotateX(PI / 2), B.mat(0x5A6474, 0.8, 0.35, 0.6, { fog: false })); base.position.z = -0.005;
    const tampo = new T3.Mesh(new T3.CylinderGeometry(0.34, 0.34, 0.012, 6).rotateX(PI / 2), B.mat(0x2A303A, 0.6, 0.5, 0.4, { fog: false })); tampo.position.z = 0.036;
    marcoLuzes = [0, 1, 2].map(k => { const l = new T3.Mesh(new T3.SphereGeometry(0.035, 12, 8), new T3.MeshBasicMaterial({ color: 0x35D9FF, fog: false }));
      const a = PI / 2 + k * 2 * PI / 3; l.position.set(0.4 * Math.cos(a), 0.4 * Math.sin(a), 0.04); marco.add(l); return l; });
    marco.add(base, tampo); S.add(marco);
    // céu: domo em degradê (azul-noite → horizonte) com o brilho magenta baixo; as estrelas do b3d por cima
    const g = new T3.SphereGeometry(800, 64, 48), cor = [], pos = g.attributes.position;
    for (let i = 0; i < pos.count; i++) {
      const el = Math.asin(cl(pos.getZ(i) / 800, -1, 1)) * 180 / PI;        // elevação em graus (z para cima no mundo)
      const c = hex(0x050816).lerp(hex(0x0E2A52), Math.exp(-Math.max(el, 0) / 6)).lerp(hex(0xEA63FF), 0.2 * Math.exp(-Math.max(el, 0) / 1.3));
      cor.push(c.r, c.g, c.b);
    }
    g.setAttribute('color', new T3.Float32BufferAttribute(cor, 3));
    B.cenaCeu.add(new T3.Mesh(g, new T3.MeshBasicMaterial({ vertexColors: true, side: T3.BackSide, depthWrite: false })));
    B.cenaCeu.children.forEach(o => { if (o.isPoints) o.renderOrder = 1; });
    B.ceu(true);
  }

  // ── a granada em cena ──────────────────────────────────────────────────────────────────────────────────────────────────────
  function granada() {
    const S = B.scene, root = new T3.Group(); S.add(root);
    const pecas = [0, 1, 2].map(k => novaPeca(k, [matExt, matFace]));
    pecas.forEach(p => root.add(p));
    const dc = deco(); root.add(dc);
    // fotos fantasma: passada só de profundidade antes da cor (cada foto se mistura uma vez só: 25–30% de verdade, sem as camadas internas somando)
    const matZ = new T3.MeshBasicMaterial({ colorWrite: false, depthWrite: true });
    const fant = [0, 1, 2].map(k => [...Array(26)].map(() => { const p = novaPeca(k, [matFant, new T3.MeshBasicMaterial({ visible: false })]); p.visible = false;
      const ms = []; p.traverse(o => { if (o.isMesh) ms.push(o); });
      ms.forEach(o => { const z = new T3.Mesh(o.geometry, matZ); z.renderOrder = -1; o.renderOrder = 1; o.add(z); });
      root.add(p); return p; }));
    // efeitos sem massa
    const clarao = new T3.Mesh(new T3.SphereGeometry(1, 24, 16), new T3.MeshBasicMaterial({ color: 0xEAF6FF, transparent: true, depthWrite: false, fog: false }));
    root.add(clarao);
    let sd = 7; const rnd = () => { sd = (sd * 16807) % 2147483647; return sd / 2147483647; };
    const NF = 170, fdir = [], fv = [], fpos = new Float32Array(NF * 3), fcor = new Float32Array(NF * 3);
    for (let i = 0; i < NF; i++) { const u = 2 * rnd() - 1, th = 2 * PI * rnd(), q = Math.sqrt(1 - u * u);
      fdir.push(v3(q * Math.cos(th), q * Math.sin(th) * 0.6, u)); fv.push(5 + 11 * rnd()); }
    const fgeo = new T3.BufferGeometry(); fgeo.setAttribute('position', new T3.BufferAttribute(fpos, 3)); fgeo.setAttribute('color', new T3.BufferAttribute(fcor, 3));
    const faiscas = new T3.Points(fgeo, new T3.PointsMaterial({ size: 2.6, sizeAttenuation: false, vertexColors: true, transparent: true,
      blending: T3.AdditiveBlending, depthWrite: false, fog: false }));
    root.add(faiscas);
    const texF = B.sprite(64, 0.7);
    const fumaca = [...Array(9)].map(() => { const s = new T3.Sprite(new T3.SpriteMaterial({ map: texF, color: 0x6E7FA0, transparent: true, depthWrite: false, fog: false }));
      s.userData.d = v3(2 * rnd() - 1, (2 * rnd() - 1) * 0.5, 2 * rnd() - 1).normalize(); root.add(s); return s; });
    const qn = new T3.Quaternion(), mundo = [null, null, null], fis = [null, null, null];
    let estado = {}, modo = 'corpo';

    function poe(p, k, x, z, ang, sig, esc, chao) {      // caco k com o ponto físico (x, z); sig: 0 = ainda encaixado no corpo, 1 = solto
      p.visible = true; p.scale.setScalar(esc);
      p.quaternion.setFromAxisAngle(EIXOS[k], ang || 0);
      p.position.set(x, 0, z).addScaledVector(CEN[k], esc * (1 - (sig || 0)));
      if (chao) {                                      // nunca dentro do chão: apoia a malha na linha de contato
        let zm = Infinity;
        for (const a of AMOS[k]) { qn.copy(p.quaternion); const w = a.clone().applyQuaternion(qn); zm = Math.min(zm, p.position.z + esc * w.z); }
        if (zm < 0) p.position.z -= zm;
        p.userData.lift = Math.max(0, -zm);
      } else p.userData.lift = 0;
      return p.position.clone();
    }

    function atualiza(g) {
      estado = g;
      const esc = g.esc || 0.3, chao = !!g.chao;
      U.onda.value = g.onda != null ? g.onda : -1; U.brilho.value = g.brilho || 0;
      matFace.emissiveIntensity = 0.6 * (g.calor || 0);
      matFace.color.copy(hex(0x23272F)).lerp(hex(0x3A2418), g.calor || 0);
      if (g.cen) {                                     // granada inteira (os três cacos encaixados) + espoleta e alavanca
        let lift = 0;
        if (chao) { const piso = Math.abs(g.cen[0]) < 0.5 ? 0.04 : 0; lift = Math.max(0, piso - (g.cen[1] + esc * ZMIN_CORPO)); }
        pecas.forEach((p, k) => { poe(p, k, g.cen[0], g.cen[1] + lift, 0, 0, esc, false); mundo[k] = p.position.clone(); fis[k] = v3(g.cen[0], 0, g.cen[1]).addScaledVector(CEN[k], esc); });
        modo = 'corpo';
        dc.visible = g.deco !== 0; dc.position.set(g.cen[0], 0, g.cen[1] + lift); dc.scale.setScalar(esc);
      } else {
        dc.visible = false;
        pecas.forEach((p, k) => { const f = (g.frags || [])[k];
          if (!f) { p.visible = false; return; }
          mundo[k] = poe(p, k, f[0], f[1], f[2], f[3], esc, chao); fis[k] = v3(f[0], 0, f[1]); });
        modo = 'cacos';
      }
      // fotos fantasma (estroboscopia): [k, x, z, ang]; k = −1 é a granada inteira
      const usados = [0, 0, 0];
      fant.forEach(l => l.forEach(p => { p.visible = false; }));
      for (const q of (g.fant || [])) {
        const ks = q[0] < 0 ? [0, 1, 2] : [q[0]];
        for (const k of ks) { if (usados[k] >= fant[k].length) continue; const p = fant[k][usados[k]++];
          poe(p, k, q[1], q[2], q[0] < 0 ? 0 : q[3], q[0] < 0 ? 0 : 1, esc, chao); }
      }
      // clarão, faíscas e fumaça (função do tempo desde a explosão, dx, em s de física)
      const dx = g.dx, pe = g.pe || [0, 0], P0 = v3(pe[0], 0, pe[1]);
      const u = dx == null ? 9 : dx / 0.075;
      clarao.visible = u >= 0 && u < 1;
      if (clarao.visible) { clarao.position.copy(P0); clarao.scale.setScalar(esc * (0.6 + 2.4 * u)); clarao.material.opacity = 0.95 * (1 - u) ** 1.5; }
      const vf = dx != null && dx >= 0 && dx < 0.55;
      faiscas.visible = vf;
      if (vf) { const s = (1 - Math.exp(-4 * dx)) / 4, a = (1 - dx / 0.55) ** 2;
        for (let i = 0; i < NF; i++) { const q = P0.clone().addScaledVector(fdir[i], esc * fv[i] * s); fpos.set([q.x, q.y, q.z], 3 * i);
          const c = i % 2 ? [0.208, 0.851, 1.0] : [0.918, 0.388, 1.0]; fcor.set(window.TRANSP ? c : c.map(x => x * a), 3 * i); }
        faiscas.material.opacity = window.TRANSP ? a : 1;               // sem fundo: apaga pela opacidade (cor escura viraria ponto preto)
        fgeo.attributes.position.needsUpdate = true; fgeo.attributes.color.needsUpdate = true; }
      fumaca.forEach((s, i) => { const vis = dx != null && dx >= 0 && dx < 0.8; s.visible = vis;
        if (vis) { s.position.copy(P0).addScaledVector(s.userData.d, esc * 1.3 * (1 - Math.exp(-3 * dx))); s.scale.setScalar(esc * (1.4 + 3.2 * dx));
          s.material.opacity = 0.3 * (1 - dx / 0.8) * Math.min(1, dx / 0.04); } });
      if (marcoLuzes) { const l = g.marco || 0; marcoLuzes.forEach(m => m.material.color.copy(hex(0x0E2A52).lerp(hex(0x35D9FF), 0.35 + 0.65 * l))); }
    }
    function pontos() {
      const M = [0, 1, 2].map(k => mundo[k]);
      const out = { modo, fis: fis.map(p => p ? B.projeta(p.toArray()) : null), cen: M.map(p => p ? B.projeta(p.toArray()) : null),
        lift: pecas.map(p => +(p.userData.lift || 0).toFixed(4)) };
      if (M.every(p => p)) out.cm = B.projeta(M.reduce((s, p, k) => s.addScaledVector(p, MS[k] / MT), v3(0, 0, 0)).toArray());
      return out;
    }
    return { atualiza, pontos };
  }
  return { campo, granada, medidas, MS, MT };
})();
