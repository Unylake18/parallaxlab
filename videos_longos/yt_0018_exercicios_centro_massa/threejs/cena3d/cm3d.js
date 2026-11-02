// yt_0017: cenas 3D por estado (geometria e parâmetros das fichas do arsenal centro_de_massa_3d e explosao, portados para Three.js).
// A cena é escolhida por window.CENA_ID (definido no .html). Posições, ângulos e câmera vêm do Manim; nada aqui tem relógio.
//   'hal' — haltere: bolas de aço de massas 1 e 3 (raio 0,8·(m/3)^(1/3), regra da ficha `halteres`), haste de 4; gira no plano horizontal
//           em torno do CM (ang, eixo z) e pode inclinar no plano da tela sobre um apoio triangular (tilt, eixo y, pivô no CM).
//           Estado: {hal: {x, y, ang, tilt, vis}, apoio: [x, vis, baixa], cam}. ang = 0 → bola leve à esquerda (−x).
//   'exp' — explosão no espaço, no plano vertical y = 0 (câmera frontal): {corpo: [x, z, vis], frags: [[x, z, vis] ×3], cam}.
//   'gra' — a mesma granada com gravidade e chão de aço escuro (câmera frontal): {corpo, frags, chao, cam} (chao = z do piso).
//   'hem' — semiesfera maciça de vidro (LatheGeometry, base em z = 0), base levemente preenchida, eixo tracejado e a fatia translúcida
//           ciano-acinzentada de espessura dz: {fz, vis, cam} (fz = centro da fatia).
// O ⊕, as setas, as cotas e os rótulos são do Manim (kit.marcador_cm / projeta3d), presos pelos pontos projetados.
(function () {
  const B = B3D, T3 = THREE, PI = Math.PI, id = window.CENA_ID;
  const aco = () => B.mat(0x8C97A8, 0.75, 0.3, 0.55);
  const MS = [2, 1, 1.5], MT = 4.5;
  let atualiza = () => {}, pontos = () => ({});

  // ── luz: A = a do teste (ambiente cinza do RoomEnvironment); B = ambiente em gradiente azul-noite (#050816 → #0E2A52) com painéis suaves
  // e luzes de recorte nas cores da marca (BLUE_L por trás à esquerda, um toque magenta por trás à direita). O aço continua aço: só o brilho muda.
  const envA = B.scene.environment;
  const envB = (() => {
    const s = new T3.Scene();
    const g = new T3.SphereGeometry(60, 48, 24), cor = [], c0 = new T3.Color(0x1A2B4A), c1 = new T3.Color(0x3A5C8E), pos = g.attributes.position;
    for (let i = 0; i < pos.count; i++) { const u = Math.min(1, Math.max(0, (pos.getY(i) / 60 + 0.35) / 1.1)); const c = c0.clone().lerp(c1, u); cor.push(c.r, c.g, c.b); }
    g.setAttribute('color', new T3.Float32BufferAttribute(cor, 3));
    s.add(new T3.Mesh(g, new T3.MeshBasicMaterial({ vertexColors: true, side: T3.BackSide })));
    const painel = (w, h, cor, int, x, y, z) => { const m = new T3.Mesh(new T3.PlaneGeometry(w, h), new T3.MeshBasicMaterial({ color: new T3.Color(cor).multiplyScalar(int), side: T3.DoubleSide }));
      m.position.set(x, y, z); m.lookAt(0, 0, 0); s.add(m); };
    painel(36, 16, 0xF5F7FF, 2.4, 0, 40, 0);         // céu: o brilho principal vem de cima (o 3D da RoomEnvironment fica com y para cima)
    painel(22, 30, 0x7FB2FF, 2.6, -38, 10, 18);      // recorte azul, atrás à esquerda
    painel(12, 20, 0xEA63FF, 1.5, 38, 8, 18);         // toque magenta, atrás à direita
    return new T3.PMREMGenerator(B.renderer).fromScene(s, 0.04).texture;
  })();
  const recA = new T3.DirectionalLight(0x7FB2FF, 0.0), recB = new T3.DirectionalLight(0xEA63FF, 0.0);
  recA.position.set(-6, 9, 4); recB.position.set(6, 9, 3); B.scene.add(recA, recB);
  let luzAtual = null;
  const KREC = id === 'exp' || id === 'band' ? 1.8 : 1.0;              // v4: recorte azul mais forte no espaço e na bandeja
  function luz(qual) {
    if (qual === luzAtual) return;
    luzAtual = qual;
    const b = qual !== 'A';
    B.scene.environment = b ? envB : envA;
    B.luz.rim.intensity = b ? 0.2 : 0.5;
    recA.intensity = b ? 0.9 * KREC : 0.0;
    recB.intensity = b ? 0.32 * Math.sqrt(KREC) : 0.0;
  }

  if (id === 'hal') {
    const M1 = 1, M2 = 3, SEP = 4, M = M1 + M2;
    const x1 = -SEP * M2 / M, x2 = SEP * M1 / M, r1 = 0.8 * Math.cbrt(M1 / 3), r2 = 0.8 * Math.cbrt(M2 / 3);
    const giro = new T3.Group(), incl = new T3.Group();
    const b1 = new T3.Mesh(new T3.SphereGeometry(r1, 48, 32), aco()); b1.position.x = x1;
    const b2 = new T3.Mesh(new T3.SphereGeometry(r2, 48, 32), aco()); b2.position.x = x2;
    const haste = new T3.Mesh(new T3.CylinderGeometry(0.07, 0.07, x2 - x1, 24).rotateZ(PI / 2), B.mat(0xB8C4DA, 0.6, 0.35, 0.5));
    haste.position.x = (x1 + x2) / 2;
    giro.add(b1, b2, haste); incl.add(giro); B.scene.add(incl);
    // apoio triangular (prisma de aço) com a ponta logo abaixo da haste, sobre uma base baixa
    const tri = new T3.Shape(); tri.moveTo(0, 0); tri.lineTo(0.36, -0.62); tri.lineTo(-0.36, -0.62); tri.closePath();
    const apoio = new T3.Group();
    const prisma = new T3.Mesh(new T3.ExtrudeGeometry(tri, { depth: 0.5, bevelEnabled: false }).rotateX(PI / 2).translate(0, 0.25, 0), aco());
    const pe = new T3.Mesh(new T3.BoxGeometry(1.3, 0.6, 0.12), B.mat(0x5A6474, 0.6, 0.4, 0.4)); pe.position.z = -0.68;
    apoio.add(prisma, pe); B.scene.add(apoio);
    atualiza = e => {
      const h = e.hal || {};
      incl.visible = h.vis !== 0; incl.position.set(h.x || 0, h.y || 0, 0);
      incl.rotation.y = h.tilt || 0; giro.rotation.z = h.ang || 0;
      const a = e.apoio || [0, 0, 0]; apoio.visible = !!a[1]; apoio.position.set(a[0], 0, -0.07 - (a[2] || 0));
    };
    pontos = () => { incl.updateMatrixWorld(); const w = o => o.getWorldPosition(new T3.Vector3()).toArray();
      return { cm: B.projeta(incl.position.toArray()), b1: B.projeta(w(b1)), b2: B.projeta(w(b2)), apoio: B.projeta(apoio.position.toArray()) }; };
  }

  if (id === 'exp' || id === 'gra') {
    // v3: a granada de fragmentação (campo.js). 'gra' = campo de provas em vácuo (piso com grade, céu, marco); 'exp' = o mesmo céu, sem
    // piso nem horizonte. Estado: {gr: {esc, cen | frags, onda, brilho, calor, dx, pe, fant, marco, chao, deco}, cam}.
    const C = CAMPO, gr = C.granada();
    if (id === 'gra') C.campo();                                      // 'exp': sem céu próprio (o do Manim aparece por trás)
    atualiza = e => gr.atualiza(e.gr || {});
    pontos = () => gr.pontos();
    window.medidas = () => C.medidas;
  }

  if (id === 'hem') {
    const R = 1.8, DZ = 0.14;
    const vidro = new T3.MeshStandardMaterial({ color: 0x4F86D8, metalness: 0.0, roughness: 0.18, envMapIntensity: 0.9, transparent: true,
      opacity: 0.30, side: T3.DoubleSide, depthWrite: false });
    const perfil = [new T3.Vector2(0, 0), ...[...Array(49)].map((_, k) => new T3.Vector2(R * Math.cos(PI / 2 * k / 48), R * Math.sin(PI / 2 * k / 48)))];
    const casca = new T3.Mesh(new T3.LatheGeometry(perfil, 96).rotateX(PI / 2), vidro);
    const base = new T3.Mesh(new T3.CircleGeometry(R * 0.999, 96), new T3.MeshBasicMaterial({ color: 0x6F93C8, transparent: true, opacity: 0.16,
      side: T3.DoubleSide, depthWrite: false }));
    base.position.z = 0.002;
    const anel = (r, z, cor, op) => new T3.LineLoop(new T3.BufferGeometry().setFromPoints([...Array(97)].map((_, k) =>
      new T3.Vector3(r * Math.cos(2 * PI * k / 96), r * Math.sin(2 * PI * k / 96), z))), new T3.LineBasicMaterial({ color: cor, transparent: true, opacity: op }));
    const borda = anel(R, 0, 0x9CC7FF, 0.85);
    const eixo = new T3.LineSegments(new T3.BufferGeometry().setFromPoints([...Array(24)].flatMap((_, k) => [new T3.Vector3(0, 0, -0.3 + k * 0.17), new T3.Vector3(0, 0, -0.3 + k * 0.17 + 0.09)])
      .filter(v => v.z <= R * 1.6)), new T3.LineBasicMaterial({ color: 0xB8C4DA, transparent: true, opacity: 0.7 }));
    const fatia = new T3.Group();
    fatia.add(new T3.Mesh(new T3.CylinderGeometry(1, 1, DZ, 96).rotateX(PI / 2),
      new T3.MeshStandardMaterial({ color: 0x7FA9B8, metalness: 0.1, roughness: 0.35, envMapIntensity: 0.6, transparent: true, opacity: 0.55, depthWrite: false })));
    fatia.add(anel(1, DZ / 2, 0xD8E6F0, 0.95), anel(1, -DZ / 2, 0xD8E6F0, 0.6));
    B.scene.add(base, casca, borda, eixo, fatia);
    atualiza = e => {
      const z = Math.min(Math.max(e.fz || 0.5, DZ / 2), R - DZ / 2), r = Math.sqrt(Math.max(R * R - z * z, 1e-4));
      fatia.visible = e.vis !== 0; fatia.position.z = z; fatia.scale.set(r, r, 1);
    };
    pontos = e => { const z = e.fz || 0.5, r = Math.sqrt(Math.max(R * R - z * z, 0));
      return { base: B.projeta([0, 0, 0]), cm: B.projeta([0, 0, 3 * R / 8]), topo: B.projeta([0, 0, R]), borda_fatia: B.projeta([r, 0, z]), centro_fatia: B.projeta([0, 0, z]) }; };
  }

  if (id === 'band') {
    // T1-7: bandeja de aço horizontal (o triângulo do T1-6, em metros: massas 2 kg em (0, 0), 1 kg em (4, 0), 1 kg em (2, 4)) com um pino de aço
    // por baixo. Estado: {band: {px, py, ax, ay, ang}, pino: [x, y, z_ponta, vis], cam}. A bandeja gira de `ang` em torno do eixo horizontal
    // (ax, ay) que passa pelo ponto de apoio (px, py, 0): o mesmo cálculo está no Manim (pecas3d.Bandeja3D) para prender ⊕, setas e rótulos.
    const DADOS = [[2, 0, 0], [1, 4, 0], [1, 2, 4]], ESP = 0.08, folga = 0.55;
    const piv = new T3.Group(), tab = new T3.Group();
    piv.add(tab); B.scene.add(piv);
    const cg = [2, 4 / 3], vs = DADOS.map(([m, x, y]) => { const d = [x - cg[0], y - cg[1]], n = Math.hypot(...d); return [x + d[0] / n * folga, y + d[1] / n * folga]; });
    const forma = new T3.Shape(); forma.moveTo(...vs[0]); forma.lineTo(...vs[1]); forma.lineTo(...vs[2]); forma.closePath();
    const placa = new T3.Mesh(new T3.ExtrudeGeometry(forma, { depth: ESP, bevelEnabled: true, bevelThickness: 0.02, bevelSize: 0.03, bevelSegments: 2 }),
      B.mat(0x4A5262, 0.78, 0.36, 0.62));                                 // o aço da granada
    placa.position.z = -ESP; tab.add(placa);
    const bolas = DADOS.map(([m, x, y]) => { const r = 0.3 * Math.cbrt(m), b_ = new T3.Mesh(new T3.SphereGeometry(r, 40, 28), aco());
      b_.position.set(x, y, r); tab.add(b_); return b_; });
    const pino = new T3.Group();
    const cone = new T3.Mesh(new T3.CylinderGeometry(0.0, 0.13, 1.7, 32).rotateX(PI / 2), aco()); cone.position.z = -0.85; pino.add(cone);
    const pe = new T3.Mesh(new T3.CylinderGeometry(0.42, 0.48, 0.1, 40).rotateX(PI / 2), B.mat(0x3A4250, 0.6, 0.45, 0.4)); pe.position.z = -1.72; pino.add(pe);
    B.scene.add(pino);
    atualiza = e => {
      const b_ = e.band || {}, px = b_.px || 0, py = b_.py || 0;
      piv.position.set(px, py, 0); tab.position.set(-px, -py, 0);
      const eixo = new T3.Vector3(b_.ax || 1, b_.ay || 0, 0).normalize();
      piv.setRotationFromAxisAngle(eixo, b_.ang || 0);
      const q = e.pino || [0, 0, -1, 0]; pino.visible = !!q[3]; pino.position.set(q[0], q[1], q[2] - ESP);
    };
    pontos = () => { piv.updateMatrixWorld(); const w = o => o.getWorldPosition(new T3.Vector3()).toArray();
      const cm = new T3.Vector3(1.5, 1.0, 0); tab.localToWorld(cm);
      return { bolas: bolas.map(o => B.projeta(w(o))), cm: B.projeta(cm.toArray()) }; };
  }

  if (id === 'cubo') {
    // EN3: fio de aço dobrado em três arestas de um cubo de 1 m (x, depois y, depois z), arestas do cubo apagadas; a câmera gira (o ⊕ é do Manim)
    const P = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [1, 1, 1]].map(q => new T3.Vector3(...q)), R = 0.035;
    const fio = new T3.Group();
    for (let i = 0; i < 3; i++) {
      const a = P[i], b = P[i + 1], L = a.distanceTo(b);
      const c = new T3.Mesh(new T3.CylinderGeometry(R, R, L, 20), aco());
      c.position.copy(a.clone().add(b).multiplyScalar(0.5));
      c.quaternion.setFromUnitVectors(new T3.Vector3(0, 1, 0), b.clone().sub(a).normalize());
      fio.add(c);
    }
    P.forEach(q => { const s_ = new T3.Mesh(new T3.SphereGeometry(R, 16, 12), aco()); s_.position.copy(q); fio.add(s_); });
    const caixa = new T3.LineSegments(new T3.EdgesGeometry(new T3.BoxGeometry(1, 1, 1)), new T3.LineBasicMaterial({ color: 0xB8C4DA, transparent: true, opacity: 0.28 }));
    caixa.position.set(0.5, 0.5, 0.5);
    B.scene.add(fio, caixa);
    atualiza = e => { fio.visible = !!e.cubo; caixa.visible = !!e.cubo; };
    pontos = () => ({ cm: B.projeta([5 / 6, 1 / 2, 1 / 6]) });
  }

  const atu0 = atualiza;
  atualiza = e => { luz(e.luz || 'B'); atu0(e); };
  window.CENA = { atualiza };
  window.pontos3d = e => pontos(e);
  window.cenaPronta = true;
})();
