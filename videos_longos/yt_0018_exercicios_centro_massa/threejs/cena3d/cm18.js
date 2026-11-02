// yt_0018: cenas 3D por estado (Three.js r128, base b3d.js do yt_0017). Cena escolhida por window.CENA_ID (no .html).
//   'cubo' — X2: cubo de 1 m em arame fantasma (GEO 25%), eixos x, y, z do canto (0,0,0), fio de aço nas arestas (0,0,0)→(1,0,0)→(1,1,0)→(1,1,1).
//            Estado: {cubo: {ar: [[brilho, enc] ×3], part: [s ×3], caixa}, cam}. enc 0 → 1 encolhe a aresta até o ponto médio; part = escala
//            da partícula de aço (raio 0,06) no ponto médio. Pontos: cantos, meios, ⊕ (5/6, 1/2, 1/6), projeções nos eixos.
//   'roj'  — X5: o campo de provas do yt_0017 (campo.js) + rojão de aço (cilindro, ogiva, 4 aletas) que se parte em dois pedaços do próprio
//            corpo (fratura em zigue-zague compartilhada; volumes 2/3 e 1/3 ajustados por bissecção e medidos na malha). Unidade 3D: 1 = 20 m.
//            Estado: {rj: {esc, cen: [x, z], ang} | {frags: [[x, z, ang, sep] ×2], dx, pe}, emenda, marco}, cam}.
//   'fog'  — EN2: o mesmo perfil, inteiro, como foguete no céu sem piso (bocal aceso). Estado: {fg: {x, z, esc, chama}, cam}.
// O ⊕, setas, rótulos, rastros, gás e eixos são do Manim (projeta3d, a mesma câmera do b3d.js).
(function () {
  const B = B3D, T3 = THREE, PI = Math.PI, id = window.CENA_ID;
  const v3 = (x, y, z) => new T3.Vector3(x, y, z);
  const cl = (x, a, b) => Math.min(b, Math.max(a, x));

  // ── luz B (a mesma do cm3d.js do yt_0017): ambiente azul-noite com recorte BLUE_L e toque magenta ─────────────────────────────
  const envB = (() => {
    const s = new T3.Scene();
    const g = new T3.SphereGeometry(60, 48, 24), cor = [], c0 = new T3.Color(0x1A2B4A), c1 = new T3.Color(0x3A5C8E), pos = g.attributes.position;
    for (let i = 0; i < pos.count; i++) { const u = cl((pos.getY(i) / 60 + 0.35) / 1.1, 0, 1); const c = c0.clone().lerp(c1, u); cor.push(c.r, c.g, c.b); }
    g.setAttribute('color', new T3.Float32BufferAttribute(cor, 3));
    s.add(new T3.Mesh(g, new T3.MeshBasicMaterial({ vertexColors: true, side: T3.BackSide })));
    const painel = (w, h, cor, int, x, y, z) => { const m = new T3.Mesh(new T3.PlaneGeometry(w, h), new T3.MeshBasicMaterial({ color: new T3.Color(cor).multiplyScalar(int), side: T3.DoubleSide }));
      m.position.set(x, y, z); m.lookAt(0, 0, 0); s.add(m); };
    painel(36, 16, 0xF5F7FF, 2.4, 0, 40, 0);
    painel(22, 30, 0x7FB2FF, 2.6, -38, 10, 18);
    painel(12, 20, 0xEA63FF, 1.5, 38, 8, 18);
    return new T3.PMREMGenerator(B.renderer).fromScene(s, 0.04).texture;
  })();
  B.scene.environment = envB;
  B.luz.rim.intensity = 0.2;
  const recA = new T3.DirectionalLight(0x7FB2FF, 1.2), recB = new T3.DirectionalLight(0xEA63FF, 0.38);
  recA.position.set(-6, 9, 4); recB.position.set(6, 9, 3); B.scene.add(recA, recB);
  const aco = (extra) => B.mat(0x8C97A8, 0.75, 0.3, 0.55, Object.assign({ fog: false }, extra || {}));

  let atualiza = () => {}, pontos = () => ({});

  // ════════════════════════════════════════ cubo (X2) ════════════════════════════════════════
  if (id === 'cubo') {
    const P = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [1, 1, 1]].map(q => v3(...q)), R = 0.032;
    const arestas = [], parts = [];
    for (let i = 0; i < 3; i++) {
      const a = P[i], b = P[i + 1], L = a.distanceTo(b), m = aco({ emissive: new T3.Color(0x7FB2FF), emissiveIntensity: 0 });
      const piv = new T3.Group(); piv.position.copy(a.clone().add(b).multiplyScalar(0.5));
      piv.quaternion.setFromUnitVectors(v3(0, 1, 0), b.clone().sub(a).normalize());
      const c = new T3.Mesh(new T3.CylinderGeometry(R, R, L, 20), m);
      const e1 = new T3.Mesh(new T3.SphereGeometry(R, 16, 12), m), e2 = e1.clone(); e1.position.y = L / 2; e2.position.y = -L / 2;
      piv.add(c, e1, e2); B.scene.add(piv); arestas.push({ piv, c, e1, e2, m, L });
      const p = new T3.Mesh(new T3.SphereGeometry(0.062, 32, 24), aco()); p.position.copy(piv.position); B.scene.add(p); parts.push(p);
    }
    const caixa = new T3.LineSegments(new T3.EdgesGeometry(new T3.BoxGeometry(1, 1, 1)), new T3.LineBasicMaterial({ color: 0xB8C4DA, transparent: true, opacity: 0.25 }));
    caixa.position.set(0.5, 0.5, 0.5); B.scene.add(caixa);
    const eixoMat = new T3.LineBasicMaterial({ color: 0xB8C4DA, transparent: true, opacity: 0.85 });
    const eixos = new T3.Group();
    [[1.38, 0, 0], [0, 1.38, 0], [0, 0, 1.38]].forEach(q => {
      eixos.add(new T3.Line(new T3.BufferGeometry().setFromPoints([v3(0, 0, 0), v3(...q)]), eixoMat));
      const cone = new T3.Mesh(new T3.ConeGeometry(0.03, 0.09, 16), new T3.MeshBasicMaterial({ color: 0xB8C4DA }));
      const d = v3(...q).normalize(); cone.position.copy(v3(...q)); cone.quaternion.setFromUnitVectors(v3(0, 1, 0), d); eixos.add(cone);
    });
    B.scene.add(eixos);
    atualiza = e => {
      const c = e.cubo || {}, ar = c.ar || [[0, 0], [0, 0], [0, 0]], pt = c.part || [0, 0, 0];
      caixa.material.opacity = 0.25 * (c.caixa == null ? 1 : c.caixa);
      arestas.forEach((a, k) => { const br = ar[k][0], enc = ar[k][1], dr = ar[k].length > 2 ? ar[k][2] : 1; const s = Math.max(1e-3, (1 - enc) * dr);
        a.m.emissiveIntensity = 0.9 * br; a.c.scale.set(1, s, 1);
        const off = (1 - dr) * a.L / 2;                       // desenhando: cresce a partir do início da aresta
        a.c.position.y = -off; a.e1.position.y = s * a.L / 2 - off; a.e2.position.y = -s * a.L / 2 - off;
        a.piv.visible = enc < 0.995 && dr > 0.002; });
      parts.forEach((p, k) => { p.visible = pt[k] > 0.01; p.scale.setScalar(Math.max(pt[k], 1e-3)); });
    };
    pontos = () => {
      const pr = q => B.projeta(q);
      return { cm: pr([5 / 6, 1 / 2, 1 / 6]), meios: [[0.5, 0, 0], [1, 0.5, 0], [1, 1, 0.5]].map(pr), cantos: P.map(q => pr(q.toArray())),
        proj_x: [[0.5, 0, 0], [1, 0, 0], [5 / 6, 0, 0]].map(pr), proj_y: [[0, 0, 0], [0, 0.5, 0], [0, 1, 0], [0, 0.5, 0]].map(pr),
        proj_z: [[0, 0, 0], [0, 0, 0.5], [0, 0, 1 / 6]].map(pr), errado: pr([0.75, 0.5, 0.25]) };
    };
  }

  // ════════════════════════════════════════ rojão / foguete (X5, EN2) ════════════════════════════════════════
  // perfil (unidades do corpo; eixo x do nariz): cauda em −0,5, cilindro até 0,2, ogiva até a ponta em 0,5; raio 0,085; 4 aletas na cauda
  const XT = -0.5, XO = 0.2, XP = 0.5, RR = 0.085, FA = { x0: -0.5, x1: -0.27, h0: 0.11, h1: 0.0, t: 0.014 };
  const raio = x => x <= XO ? RR : RR * Math.pow(Math.max(0, 1 - ((x - XO) / (XP - XO)) ** 2), 0.62);
  const altAleta = x => (x < FA.x0 || x > FA.x1) ? 0 : FA.h0 + (FA.h1 - FA.h0) * (x - FA.x0) / (FA.x1 - FA.x0) + 0.03 * Math.min(1, (x - FA.x0) / 0.04);
  const area = x => PI * raio(x) ** 2 + 4 * FA.t * altAleta(x);
  const integra = (a, b) => { let s = 0; const n = 2000; for (let i = 0; i < n; i++) { const x = a + (b - a) * (i + 0.5) / n; s += area(x); } return s * (b - a) / n; };
  const VTOT = integra(XT, XP);
  let lo = XT, hi = XP;
  for (let it = 0; it < 60; it++) { const m = (lo + hi) / 2; if (integra(m, XP) > VTOT / 3) lo = m; else hi = m; }
  const XC = (lo + hi) / 2;                      // corte médio: frente (ogiva) = 1/3 do volume = 50 g; trás (aletas) = 2/3 = 100 g
  const zig = (f, rho) => 0.022 * (Math.sin(3 * f + 0.4) + 0.45 * Math.sin(7 * f + 1.1) + 0.25 * Math.sin(13 * f + 2.0)) * (0.35 + 0.65 * rho / RR)
    + 0.008 * Math.sin(9 * rho / RR + 2 * f);
  const xcut = (f, rho) => XC + zig(f, rho);

  function malha() { return { pos: [], idx: [] }; }
  function tri(M, a, b, c, des) {
    const P_ = j => v3(M.pos[3 * j], M.pos[3 * j + 1], M.pos[3 * j + 2]);
    const A = P_(a), n = P_(b).sub(A).cross(P_(c).sub(A));
    if (n.dot(des(A.clone().add(P_(b)).add(P_(c)).multiplyScalar(1 / 3))) < 0) M.idx.push(a, c, b); else M.idx.push(a, b, c);
  }
  const NF = 96, NR = 14, NU = 60;
  const radial = q => v3(0, q.y, q.z);
  function capa(M, sinal, xf) {               // disco em x = xf(φ, ρ), normal ±x
    const base = M.pos.length / 3;
    M.pos.push(xf(0, 0), 0, 0);
    for (let i = 1; i <= NR; i++) for (let j = 0; j < NF; j++) { const f = 2 * PI * j / NF, r = RR * i / NR; M.pos.push(xf(f, r), r * Math.cos(f), r * Math.sin(f)); }
    const V = (i, j) => i === 0 ? base : base + 1 + (i - 1) * NF + (j % NF);
    for (let j = 0; j < NF; j++) tri(M, V(0, 0), V(1, j), V(1, j + 1), () => v3(sinal, 0, 0));
    for (let i = 1; i < NR; i++) for (let j = 0; j < NF; j++) { tri(M, V(i, j), V(i + 1, j), V(i + 1, j + 1), () => v3(sinal, 0, 0)); tri(M, V(i, j), V(i + 1, j + 1), V(i, j + 1), () => v3(sinal, 0, 0)); }
  }
  function casca(M, xa, xb) {                  // superfície externa de xa(φ) a xb(φ) (raio do perfil)
    const base = M.pos.length / 3;
    for (let i = 0; i <= NU; i++) for (let j = 0; j < NF; j++) { const f = 2 * PI * j / NF, x = xa(f) + (xb(f) - xa(f)) * i / NU, r = raio(x); M.pos.push(x, r * Math.cos(f), r * Math.sin(f)); }
    const V = (i, j) => base + i * NF + (j % NF);
    for (let i = 0; i < NU; i++) for (let j = 0; j < NF; j++) { tri(M, V(i, j), V(i + 1, j), V(i + 1, j + 1), radial); tri(M, V(i, j), V(i + 1, j + 1), V(i, j + 1), radial); }
  }
  function aleta(M, k) {                      // prisma fino (trapézio) na direção radial k·90°
    const f = PI / 4 + k * PI / 2, c = Math.cos(f), s = Math.sin(f), nx = -s, ny = c, base = M.pos.length / 3;
    const xs = [FA.x0, FA.x1, FA.x1, FA.x0], hs = [RR - 0.004, RR - 0.004, RR + altAleta(FA.x1 - 1e-6), RR + altAleta(FA.x0 + 0.04)];
    for (const sg of [-1, 1]) for (let i = 0; i < 4; i++) M.pos.push(xs[i], hs[i] * c + sg * FA.t / 2 * nx, hs[i] * s + sg * FA.t / 2 * ny);
    const q = [[0, 1, 2], [0, 2, 3], [4, 6, 5], [4, 7, 6], [0, 4, 5], [0, 5, 1], [1, 5, 6], [1, 6, 2], [2, 6, 7], [2, 7, 3], [3, 7, 4], [3, 4, 0]];
    const cen = v3((FA.x0 + FA.x1) / 2, (RR + 0.05) * c, (RR + 0.05) * s);
    for (const [a, b, d] of q) tri(M, base + a, base + b, base + d, p => p.clone().sub(cen));
  }
  function medir(M) {
    let V = 0; const C = v3(0, 0, 0);
    for (let t = 0; t < M.idx.length; t += 3) {
      const P_ = j => v3(M.pos[3 * j], M.pos[3 * j + 1], M.pos[3 * j + 2]);
      const a = P_(M.idx[t]), b = P_(M.idx[t + 1]), c = P_(M.idx[t + 2]), dv = a.dot(b.clone().cross(c)) / 6;
      V += dv; C.addScaledVector(a.add(b).add(c), dv / 4);
    }
    return { V, C: C.divideScalar(V) };
  }
  // pedaço de trás (100 g): tampa da cauda, casca até o corte, face de fratura, 4 aletas · pedaço da frente (50 g): face, casca até a ponta
  const TRAS = malha(), FRENTE = malha(), ALETAS = malha();
  capa(TRAS, -1, () => XT); casca(TRAS, () => XT, f => xcut(f, RR)); capa(TRAS, +1, xcut);
  for (let k = 0; k < 4; k++) aleta(ALETAS, k);
  capa(FRENTE, -1, xcut); casca(FRENTE, f => xcut(f, RR), () => XP - 1e-4);
  const mT = medir(TRAS), mA = medir(ALETAS), mF = medir(FRENTE);
  const VT_ = mT.V + mA.V, CT = mT.C.clone().multiplyScalar(mT.V).addScaledVector(mA.C, mA.V).divideScalar(VT_);
  const VTOT_M = VT_ + mF.V, CG = CT.clone().multiplyScalar(VT_).addScaledVector(mF.C, mF.V).divideScalar(VTOT_M);
  const CEN = [CT.clone().sub(CG), mF.C.clone().sub(CG)];          // centroides dos pedaços, relativos ao centroide do corpo
  window.medidas = () => ({ vol: [+VT_.toFixed(6), +mF.V.toFixed(6)], frac: [+(VT_ / VTOT_M).toFixed(4), +(mF.V / VTOT_M).toFixed(4)],
    frac_alvo: [0.6667, 0.3333], vol_integral: +VTOT.toFixed(6), x_corte: +XC.toFixed(4), cen: CEN.map(c => c.toArray().map(x => +x.toFixed(5))),
    comp: XP - XT, raio: RR });
  const geo = M => { const g = new T3.BufferGeometry(); g.setAttribute('position', new T3.Float32BufferAttribute(M.pos, 3)); g.setIndex(M.idx);
    g.translate(-CG.x, -CG.y, -CG.z); g.computeVertexNormals(); return g; };
  const matCorpo = B.mat(0x7A8696, 0.78, 0.34, 0.65, { fog: false });
  const matFace = new T3.MeshStandardMaterial({ color: 0x23272F, metalness: 0.35, roughness: 0.75, envMapIntensity: 0.35, emissive: new T3.Color(0xFF7A3D),
    emissiveIntensity: 0, fog: false });
  // emenda (G15: degradê só aqui, ~0,5 s antes de explodir): tubo fino na borda da fratura, ciano → magenta ao longo da volta
  const borda = []; for (let j = 0; j <= 192; j++) { const f = 2 * PI * j / 192; borda.push(v3(xcut(f, RR) - CG.x, (RR + 0.003) * Math.cos(f) - CG.y, (RR + 0.003) * Math.sin(f) - CG.z)); }
  const tubo = new T3.TubeGeometry(new T3.CatmullRomCurve3(borda, true), 384, 0.009, 6, true);
  { const c = [], n = tubo.attributes.position.count, a = new T3.Color(0x35D9FF), b = new T3.Color(0xEA63FF);
    for (let i = 0; i < n; i++) { const u = (i / n), w = 0.5 - 0.5 * Math.cos(2 * PI * u), q = a.clone().lerp(b, w); c.push(q.r, q.g, q.b); }
    tubo.setAttribute('color', new T3.Float32BufferAttribute(c, 3)); }
  const matEm = new T3.MeshBasicMaterial({ vertexColors: true, transparent: true, opacity: 0, depthWrite: false, fog: false });
  function rojao() {
    const pecas = [new T3.Group(), new T3.Group()], off = [new T3.Group(), new T3.Group()];
    off[0].add(new T3.Mesh(geo(TRAS), [matCorpo]), new T3.Mesh(geo(ALETAS), matCorpo));
    off[0].children[0].material = matCorpo;
    off[1].add(new T3.Mesh(geo(FRENTE), matCorpo));
    // a face de fratura escurece/aquece: malha da capa com o material da face, levemente por dentro
    const faceT = malha(); capa(faceT, +1, (f, r) => xcut(f, r) - 0.0015); const faceF = malha(); capa(faceF, -1, (f, r) => xcut(f, r) + 0.0015);
    off[0].add(new T3.Mesh(geo(faceT), matFace)); off[1].add(new T3.Mesh(geo(faceF), matFace));
    const em = new T3.Mesh(tubo, matEm);
    pecas.forEach((p, k) => { off[k].position.copy(CEN[k]).negate(); p.add(off[k]); B.scene.add(p); });
    const inteiro = new T3.Group(); B.scene.add(inteiro); inteiro.add(em);
    return { pecas, inteiro, em };
  }

  if (id === 'roj') {
    CAMPO.campo();
    const r = rojao();
    // faíscas e fumaça sem massa (somem em ~1 s)
    let sd = 11; const rnd = () => { sd = (sd * 16807) % 2147483647; return sd / 2147483647; };
    const NFA = 120, fdir = [], fv = [], fpos = new Float32Array(NFA * 3), fcor = new Float32Array(NFA * 3);
    for (let i = 0; i < NFA; i++) { const u = 2 * rnd() - 1, th = 2 * PI * rnd(), q = Math.sqrt(1 - u * u); fdir.push(v3(q * Math.cos(th), q * Math.sin(th) * 0.5, u)); fv.push(3 + 7 * rnd()); }
    const fgeo = new T3.BufferGeometry(); fgeo.setAttribute('position', new T3.BufferAttribute(fpos, 3)); fgeo.setAttribute('color', new T3.BufferAttribute(fcor, 3));
    const faiscas = new T3.Points(fgeo, new T3.PointsMaterial({ size: 2.4, sizeAttenuation: false, vertexColors: true, blending: T3.AdditiveBlending, depthWrite: false, fog: false, transparent: true }));
    B.scene.add(faiscas);
    const texF = B.sprite(64, 0.7);
    const fumaca = [...Array(7)].map(() => { const s = new T3.Sprite(new T3.SpriteMaterial({ map: texF, color: 0x6E7FA0, transparent: true, depthWrite: false, fog: false }));
      s.userData.d = v3(2 * rnd() - 1, (2 * rnd() - 1) * 0.5, 2 * rnd() - 1).normalize(); B.scene.add(s); return s; });
    const mundo = [null, null];
    atualiza = e => {
      const g = e.rj || {}, esc = g.esc || 0.3;
      matEm.opacity = cl(g.emenda || 0, 0, 1);
      matFace.emissiveIntensity = 0.7 * (g.calor || 0);
      if (g.cen) {
        r.inteiro.visible = true; r.inteiro.position.set(g.cen[0], 0, g.cen[1]); r.inteiro.scale.setScalar(esc); r.inteiro.rotation.set(0, -(g.ang || 0), 0);
        r.pecas.forEach((p, k) => { p.visible = true; p.scale.setScalar(esc); p.rotation.set(0, -(g.ang || 0), 0);
          const c = CEN[k].clone().applyAxisAngle(v3(0, 1, 0), -(g.ang || 0)).multiplyScalar(esc); p.position.set(g.cen[0] + c.x, c.y, g.cen[1] + c.z); mundo[k] = p.position.clone(); });
      } else {
        r.inteiro.visible = matEm.opacity > 0.01 && false;
        r.pecas.forEach((p, k) => { const f = (g.frags || [])[k]; if (!f) { p.visible = false; return; }
          p.visible = true; p.scale.setScalar(esc); p.rotation.set(0.25 * Math.sin(f[2] * 0.7) * f[3], -f[2], 0);
          const enc = CEN[k].clone().multiplyScalar(esc * (1 - f[3]));     // logo depois da explosão o pedaço ainda está no lugar dele no corpo
          p.position.set(f[0] + enc.x, enc.y, f[1] + enc.z); mundo[k] = p.position.clone(); });
      }
      const dx = g.dx, pe = g.pe || [0, 0], P0 = v3(pe[0], 0, pe[1]);
      const vf = dx != null && dx >= 0 && dx < 0.6; faiscas.visible = vf;
      if (vf) { const s = (1 - Math.exp(-4 * dx)) / 4, a = (1 - dx / 0.6) ** 2;
        for (let i = 0; i < NFA; i++) { const q = P0.clone().addScaledVector(fdir[i], esc * fv[i] * s); fpos.set([q.x, q.y, q.z], 3 * i);
          const c = i % 2 ? [0.95, 0.8, 0.6] : [1.0, 0.48, 0.24]; fcor.set(c.map(x => x * a), 3 * i); }
        fgeo.attributes.position.needsUpdate = true; fgeo.attributes.color.needsUpdate = true; }
      fumaca.forEach(s => { const vis = dx != null && dx >= 0 && dx < 1.0; s.visible = vis;
        if (vis) { s.position.copy(P0).addScaledVector(s.userData.d, esc * 0.9 * (1 - Math.exp(-3 * dx))); s.scale.setScalar(esc * (0.8 + 2.2 * dx));
          s.material.opacity = 0.32 * (1 - dx) * Math.min(1, dx / 0.04); } });
    };
    pontos = () => ({ pecas: mundo.map(p => p ? B.projeta(p.toArray()) : null) });
  }

  if (id === 'fog') {
    const r = rojao();
    matEm.opacity = 0;
    const bocal = new T3.Mesh(new T3.SphereGeometry(0.05, 20, 14), new T3.MeshBasicMaterial({ color: 0x8BE9FF, transparent: true, opacity: 0.9, fog: false }));
    B.scene.add(bocal);
    atualiza = e => {
      const g = e.fg || {}, esc = g.esc || 1;
      r.inteiro.visible = false;
      r.pecas.forEach((p, k) => { p.visible = true; p.scale.setScalar(esc); p.rotation.set(g.rol || 0, 0, 0);
        p.position.set(g.x + CEN[k].x * esc, CEN[k].y * esc, g.z + CEN[k].z * esc); });
      bocal.position.set(g.x + (XT - CG.x - 0.01) * esc, 0, g.z); bocal.scale.setScalar(esc * (0.7 + 0.5 * (g.chama || 0))); bocal.visible = (g.chama || 0) > 0.02;
    };
    pontos = e => { const g = e.fg || {}, esc = g.esc || 1; return { cm_corpo: B.projeta([g.x, 0, g.z]), bocal: B.projeta([g.x + (XT - CG.x) * esc, 0, g.z]) }; };
  }

  window.CENA = { atualiza };
  window.pontos3d = e => pontos(e);
  window.cenaPronta = true;
})();
