// yt_0021: cenas 3D por estado (Three.js r128, base b3d.js copiada do yt_0019). Cena escolhida por window.CENA_ID (no .html).
//   'bastao' — H1–H3, T5-6, S2: bastões de madeira deitados no plano horizontal z = 0 (câmera de cima), cada um num pino vertical de aço.
//   'esfera' — T4-4, T6-4: esfera maciça de aço (R = 1) que se fatia em discos finos empilhados no eixo vertical z; câmera a 3/4.
// Estado 'bastao': {bs: [{x, y, ang, piv, tint: [a, b], op}], cam}. (x, y) = pino em metros; ang = direção do bastão a partir do pino;
//   piv 0: o pino está na ponta do cabo (x local 0); piv 1: o pino está na ponta grossa (x local 0,84). tint: rosa nas metades (cabo, grossa).
// Estado 'esfera': {cut, sep, hi, rot, eixos, cam}. cut 0 → 1: esfera lisa → discos; sep: folga entre discos (fração de dz); hi: disco destacado
//   (rosa), −1 nenhum; eixos 0 → 1: eixos x, y, z pelo centro (GEO).
// O que é número, rótulo, seta, cota e sinal é do Manim (projeta3d, a mesma câmera do b3d.js).
(function () {
  const B = B3D, T3 = THREE, PI = Math.PI, id = window.CENA_ID;
  const v3 = (x, y, z) => new T3.Vector3(x, y, z);
  const cl = (x, a, b) => Math.min(b, Math.max(a, x));

  // ── luz B (a mesma do yt_0017/0018/0019): ambiente azul-noite com recorte BLUE_L (~35%) e toque magenta (~12%) ──
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
  const recA = new T3.DirectionalLight(0x7FB2FF, 1.0), recB = new T3.DirectionalLight(0xEA63FF, 0.32);
  recA.position.set(-6, 9, 6); recB.position.set(6, 9, 4); B.scene.add(recA, recB);
  B.ceu(false);

  let atualiza = () => {}, pontos = () => ({});

  if (id === 'bastao') {
    // ── bastão: 0,84 m; cabo 0–0,42 m (fino, madeira clara), parte grossa 0,42–0,84 m (madeira escura). Eixo local +x. ──
    const L = 0.84, MEIO = 0.42;
    const perfil = x => {                                  // raio (m) ao longo do bastão: botão no cabo, cabo fino, transição, barril, ponta arredondada
      if (x < 0.012) return 0.019 * Math.sqrt(Math.max(0, x / 0.012)) + 0.004;
      if (x < 0.02) return 0.023;
      if (x < 0.36) return 0.0135;
      if (x < 0.52) { const u = (x - 0.36) / 0.16; return 0.0135 + (0.031 - 0.0135) * u * u * (3 - 2 * u); }
      if (x < 0.815) return 0.031;
      const u = (x - 0.815) / 0.025; return 0.031 * Math.sqrt(Math.max(0, 1 - u * u)) + 0.002;
    };
    const ENG = 2.2;                                     // espessura exagerada 2,2× (legível a 960×540 visto de cima); comprimento e massas são os reais
    const lathePts = (x0, x1, n) => { const p = []; for (let i = 0; i <= n; i++) { const x = x0 + (x1 - x0) * i / n; p.push(new T3.Vector2(ENG * perfil(x), x)); } return p; };
    const madeira = cor => new T3.MeshStandardMaterial({ color: cor, metalness: 0.0, roughness: 0.8, envMapIntensity: 0.28, emissive: new T3.Color(0xFF7EB6), emissiveIntensity: 0,
      transparent: true, opacity: 1 });
    const aco = new T3.MeshStandardMaterial({ color: 0x7A8696, metalness: 0.8, roughness: 0.32, envMapIntensity: 0.8 });
    function monta() {
      const raiz = new T3.Group(), corpo = new T3.Group();
      const mA = madeira(0x9C7A58), mB = madeira(0x66422C);     // alvo na tela ≈ #C9A27A e #8A5A3C (as luzes clareiam ~30%)
      const a = new T3.Mesh(new T3.LatheGeometry([new T3.Vector2(0, 0), ...lathePts(0, MEIO, 60)], 48), mA);
      const b = new T3.Mesh(new T3.LatheGeometry([...lathePts(MEIO, L, 80), new T3.Vector2(0, L)], 48), mB);
      [a, b].forEach(m => { m.rotation.z = -PI / 2; corpo.add(m); });        // eixo do lathe (y) → +x
      corpo.position.z = 0.07;                                              // deitado sobre o plano z = 0
      const pino = new T3.Mesh(new T3.CylinderGeometry(0.03, 0.03, 0.16, 32), aco); pino.rotation.x = PI / 2; pino.position.z = 0.08;
      const cab = new T3.Mesh(new T3.CylinderGeometry(0.042, 0.042, 0.012, 32), aco); cab.rotation.x = PI / 2; cab.position.z = 0.14;
      raiz.add(corpo, pino, cab);
      B.scene.add(raiz);
      return { raiz, corpo, pino, cab, mA, mB };
    }
    const BS = [monta(), monta()];
    atualiza = e => {
      const bs = e.bs || [];
      BS.forEach((o, k) => {
        const s = bs[k];
        o.raiz.visible = !!s && (s.op == null || s.op > 0.01);
        if (!s) return;
        o.raiz.position.set(s.x, s.y, 0);
        o.raiz.rotation.set(0, 0, s.ang || 0);
        // piv 0: cabo no pino (x local 0 no pino); piv 1: ponta grossa no pino → o corpo vira (x local L no pino)
        o.corpo.rotation.set(0, 0, s.piv === 1 ? PI : 0);
        o.corpo.position.set(s.piv === 1 ? L : 0, 0, 0.07);
        const op = s.op == null ? 1 : s.op, t = s.tint || [0, 0];
        o.mA.opacity = o.mB.opacity = op; o.mA.depthWrite = o.mB.depthWrite = op > 0.98;
        o.mA.emissiveIntensity = 0.55 * t[0]; o.mB.emissiveIntensity = 0.55 * t[1];
      });
    };
    pontos = e => {
      const out = {};
      (e.bs || []).forEach((s, k) => {
        const o = BS[k]; o.raiz.updateMatrixWorld(true);
        const w = x => { const v = v3(x, 0, 0); o.corpo.localToWorld(v); return B.projeta(v.toArray()); };
        out['b' + k] = { cabo: w(0), grossa: w(L), meio: w(MEIO), cm_cabo: w(0.21), cm_grossa: w(0.63), pino: B.projeta([s.x, s.y, 0.14]) };
      });
      return out;
    };
  }

  if (id === 'esfera') {
    // ── esfera maciça R = 1 fatiada em N discos de espessura dz = 2R/N; o disco k tem raio √(R² − z_k²) no meio da fatia ──
    const R = 1.0, N = 14, DZ = 2 * R / N;
    const matS = new T3.MeshStandardMaterial({ color: 0x6E8CBF, metalness: 0.4, roughness: 0.65, envMapIntensity: 0.55, transparent: true, opacity: 1 });
    const esf = new T3.Mesh(new T3.SphereGeometry(R, 96, 64), matS); esf.rotation.x = PI / 2; B.scene.add(esf);
    const malha = new T3.LineSegments(new T3.WireframeGeometry(new T3.SphereGeometry(R * 1.003, 24, 14)), new T3.LineBasicMaterial({ color: 0xB8C4DA, transparent: true, opacity: 0.3 })); esf.add(malha);   // meridianos e paralelos: a rotação fica visível
    const eixoObl = new T3.Vector3(0.3, 0.25, 0.92).normalize();
    const grupo = new T3.Group(); B.scene.add(grupo);
    const discos = [], matD = [];
    for (let k = 0; k < N; k++) {
      const z = -R + DZ * (k + 0.5), r = Math.sqrt(R * R - z * z);
      const m = new T3.MeshStandardMaterial({ color: 0x7E9CCB, metalness: 0.35, roughness: 0.6, envMapIntensity: 0.6, emissive: new T3.Color(0xFF7EB6), emissiveIntensity: 0,
        transparent: true, opacity: 0 });
      const d = new T3.Mesh(new T3.CylinderGeometry(r, r, DZ * 0.92, 96), m); d.rotation.x = PI / 2; d.userData = { z, r };
      grupo.add(d); discos.push(d); matD.push(m);
    }
    const matE = new T3.MeshBasicMaterial({ color: 0xB8C4DA, transparent: true, opacity: 0 });
    const eixos = [0, 1, 2].map(k => { const c = new T3.Mesh(new T3.CylinderGeometry(0.012, 0.012, 3.0, 12), matE);
      if (k === 0) c.rotation.z = PI / 2; if (k === 2) c.rotation.x = PI / 2; B.scene.add(c); return c; });
    atualiza = e => {
      const cut = cl(e.cut || 0, 0, 1), sep = e.sep || 0, hi = e.hi == null ? -1 : e.hi;
      matS.opacity = 1 - cut; esf.visible = cut < 0.99; matS.depthWrite = cut < 0.5;
      grupo.rotation.z = e.rot || 0; esf.setRotationFromQuaternion(new T3.Quaternion().setFromAxisAngle(eixoObl, e.rot || 0));
      discos.forEach((d, k) => {
        d.position.z = d.userData.z * (1 + sep);
        matD[k].opacity = cut; matD[k].depthWrite = cut > 0.5; d.visible = cut > 0.01;
        const on = k === hi ? (e.hiop == null ? 1 : e.hiop) : 0;
        matD[k].emissiveIntensity = 0.7 * on;
        matD[k].color.set(on > 0.5 ? 0xC9A0B4 : 0x7E9CCB);
      });
      matE.opacity = 0.9 * cl(e.eixos || 0, 0, 1);
      eixos.forEach(c => { c.visible = (e.eixos || 0) > 0.01; });
    };
    pontos = e => {
      const sep = e.sep || 0, hi = e.hi == null ? -1 : e.hi, out = { centro: B.projeta([0, 0, 0]), topo: B.projeta([0, 0, R * (1 + sep)]) };
      if (hi >= 0) { const d = discos[hi], z = d.userData.z * (1 + sep), r = d.userData.r;
        out.hi = { centro: B.projeta([0, 0, z]), borda: B.projeta([r, 0, z]), z: d.userData.z, r }; }
      out.ex = B.projeta([1.5, 0, 0]); out.ey = B.projeta([0, 1.5, 0]); out.ez = B.projeta([0, 0, 1.5]);
      return out;
    };
    window.medidas = () => discos.map(d => ({ z: d.userData.z, r: d.userData.r, vol: PI * d.userData.r ** 2 * DZ }));
  }

  window.CENA = { atualiza };
  window.pontos3d = e => pontos(e);
  window.cenaPronta = true;
})();
