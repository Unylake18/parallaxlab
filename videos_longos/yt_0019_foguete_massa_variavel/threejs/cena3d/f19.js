// yt_0019: cenas 3D por estado (Three.js r128, base b3d.js do yt_0018). Cena escolhida por window.CENA_ID (no .html).
//   'rampa' — hook, T4-1, S1: foguete de dois estágios de pé na rampa (z para cima), torre simples, piso escuro com grade ciano.
//   'esp'   — T2-1, T2-6, T3-7/T3-8, E2-3: o mesmo foguete deitado (nariz em +x) no céu sem piso, jato de partículas.
// Estado: {f: {x, y, z, esc, eixo: 'z'|'x', corte, tq: [t1, t2], carga, ch1, ch2, sep: [d, ang], op2}, gas: {p: [x, y, z, ...], c: [k, ...], s}, cam}
//   O ponto (x, y, z) do foguete é a SAÍDA DO BOCAL do 1º estágio (o ponto de massa da simulação); o corpo vai para +eixo a partir dele.
//   esc: tamanho do foguete (1 = altura total 1 unidade). corte 0 → 1: o casco fica translúcido e os tanques acendem (tq: brilho de cada tanque).
//   ch1/ch2: chama do 1º/2º estágio (0 → 1). sep: [afastamento do 1º estágio para trás (unid. do corpo), giro (rad)]. gas.c: 0 neutro, 1 DIM, 2 branco.
// O ⊕, setas, rótulos e números são do Manim (projeta3d, a mesma câmera do b3d.js).
(function () {
  const B = B3D, T3 = THREE, PI = Math.PI, id = window.CENA_ID;
  const v3 = (x, y, z) => new T3.Vector3(x, y, z);
  const cl = (x, a, b) => Math.min(b, Math.max(a, x));

  // ── luz B (a mesma do yt_0017/0018): ambiente azul-noite com recorte BLUE_L e toque magenta ─────────────────────────────
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

  // ── foguete de dois estágios (eixo local +Y, base do bocal do 1º estágio em y = 0) ─────────────────────────────
  // medidas em unidades do corpo (altura total 1,0): bocal 1 0…0,06 · 1º estágio 0,06…0,60 · interestágio 0,60…0,65 · 2º estágio 0,65…0,85 ·
  // carenagem 0,85…1,0 (cápsula/carga dentro, 0,87…0,95). Raio 0,055.
  const RR = 0.055, Y = { b1: 0.06, s1: 0.60, ie: 0.65, s2: 0.85, topo: 1.0 };
  const matCasco = new T3.MeshStandardMaterial({ color: 0x7A8696, metalness: 0.78, roughness: 0.34, envMapIntensity: 0.65, transparent: true, opacity: 1, fog: false });
  const matEsc = new T3.MeshStandardMaterial({ color: 0x4A5262, metalness: 0.7, roughness: 0.4, envMapIntensity: 0.5, transparent: true, opacity: 1, fog: false });
  const matTq = [0, 1].map(() => new T3.MeshStandardMaterial({ color: 0x000000, metalness: 0.0, roughness: 0.9, envMapIntensity: 0.0, emissive: new T3.Color(0xFFA94D),
    emissiveIntensity: 0, transparent: true, opacity: 0, depthWrite: false, fog: false, toneMapped: false }));
  const matCarga = new T3.MeshStandardMaterial({ color: 0xF5F7FF, metalness: 0.2, roughness: 0.5, emissive: new T3.Color(0xF5F7FF), emissiveIntensity: 0,
    transparent: true, opacity: 0, fog: false });
  const matChama = [0, 1].map(() => new T3.MeshBasicMaterial({ color: 0xFFB347, transparent: true, opacity: 0, depthWrite: false, blending: T3.AdditiveBlending, fog: false }));
  const lathe = (pts, mat) => new T3.Mesh(new T3.LatheGeometry(pts.map(p => new T3.Vector2(p[0], p[1])), 64), mat);
  const cil = (r, y0, y1, mat, seg) => { const m = new T3.Mesh(new T3.CylinderGeometry(r, r, y1 - y0, seg || 64, 1, false), mat); m.position.y = (y0 + y1) / 2; return m; };
  const tubo = (r, y0, y1, mat) => { const m = new T3.Mesh(new T3.CylinderGeometry(r, r, y1 - y0, 64, 1, true), mat); m.position.y = (y0 + y1) / 2; return m; };
  function montaFoguete() {
    const raiz = new T3.Group(), est1 = new T3.Group(), est2 = new T3.Group();
    raiz.add(est1, est2);
    // 1º estágio: bocal, casco, aletas, anel de separação (interestágio)
    est1.add(lathe([[0.042, 0.0], [0.03, 0.03], [0.02, 0.06], [0.0, 0.062]], matEsc));
    est1.add(tubo(RR, Y.b1, Y.s1, matCasco));
    est1.add(cil(RR * 0.98, Y.b1 - 0.002, Y.b1 + 0.002, matEsc));
    est1.add(tubo(RR * 1.01, Y.s1, Y.ie, matEsc));
    for (let k = 0; k < 4; k++) {
      const a = new T3.Mesh(new T3.BoxGeometry(0.006, 0.12, 0.05), matCasco);
      const f = k * PI / 2; a.position.set((RR + 0.022) * Math.cos(f), Y.b1 + 0.07, (RR + 0.022) * Math.sin(f)); a.rotation.y = -f; est1.add(a);
    }
    const tq1 = cil(RR * 0.86, Y.b1 + 0.03, Y.s1 - 0.025, matTq[0]); est1.add(tq1);
    const ch1 = new T3.Mesh(new T3.ConeGeometry(0.036, 0.22, 32, 1, true), matChama[0]); ch1.rotation.x = PI; ch1.position.y = -0.11; est1.add(ch1);
    // 2º estágio: bocal pequeno (dentro do interestágio), casco, carenagem, carga
    est2.add(lathe([[0.03, Y.s1 + 0.005], [0.02, Y.s1 + 0.025], [0.012, Y.ie], [0.0, Y.ie + 0.002]], matEsc));
    est2.add(tubo(RR, Y.ie, Y.s2, matCasco));
    est2.add(cil(RR * 0.98, Y.ie - 0.002, Y.ie + 0.002, matEsc));
    const tq2 = cil(RR * 0.86, Y.ie + 0.02, Y.s2 - 0.02, matTq[1]); est2.add(tq2);
    const car = [[RR, Y.s2], [RR, Y.s2 + 0.02], [RR * 0.92, Y.s2 + 0.06], [RR * 0.7, Y.s2 + 0.1], [RR * 0.38, Y.s2 + 0.135], [0.0, Y.topo]];
    est2.add(lathe(car, matCasco));
    const carga = new T3.Mesh(new T3.SphereGeometry(0.028, 24, 16), matCarga); carga.scale.y = 1.35; carga.position.y = Y.s2 + 0.05; est2.add(carga);
    const ch2 = new T3.Mesh(new T3.ConeGeometry(0.022, 0.14, 32, 1, true), matChama[1]); ch2.rotation.x = PI; ch2.position.y = Y.s1 - 0.07; est2.add(ch2);
    B.scene.add(raiz);
    return { raiz, est1, est2, ch1, ch2 };
  }
  const F = montaFoguete();

  // ── piso com grade ciano, rampa e torre (só na 'rampa') ─────────────────────────────
  const solo = [];
  if (id === 'rampa') {
    const piso = new T3.Mesh(new T3.PlaneGeometry(40, 40), new T3.MeshBasicMaterial({ color: 0x08122B, transparent: true, opacity: 0.9, fog: false }));
    B.scene.add(piso); solo.push(piso);
    const grade = new T3.GridHelper(40, 160, 0x35D9FF, 0x35D9FF); grade.rotation.x = PI / 2; grade.position.z = 0.001;
    grade.material.transparent = true; grade.material.opacity = 0.22; grade.material.depthWrite = false; B.scene.add(grade); solo.push(grade);
    const base = new T3.Mesh(new T3.CylinderGeometry(0.16, 0.18, 0.03, 48), matEsc); base.rotation.x = PI / 2; base.position.z = 0.015; B.scene.add(base); solo.push(base);
    const torre = new T3.Group(), matT = new T3.LineBasicMaterial({ color: 0x8FA3C4, transparent: true, opacity: 0.55 });
    const tx = 0.2, H = 0.92, w = 0.05, pts = [];
    for (const dx of [-w, w]) for (const dy of [-w, w]) pts.push(v3(tx + dx, dy, 0), v3(tx + dx, dy, H));
    for (let z = 0; z <= H + 1e-6; z += 0.08) { const q = [[-w, -w], [w, -w], [w, w], [-w, w], [-w, -w]]; for (let k = 0; k < 4; k++) pts.push(v3(tx + q[k][0], q[k][1], z), v3(tx + q[k + 1][0], q[k + 1][1], z)); }
    for (let z = 0; z < H - 0.01; z += 0.08) pts.push(v3(tx - w, -w, z), v3(tx + w, -w, z + 0.08), v3(tx - w, w, z), v3(tx + w, w, z + 0.08));
    torre.add(new T3.LineSegments(new T3.BufferGeometry().setFromPoints(pts), matT));
    for (const z of [0.42, 0.78]) torre.add(new T3.LineSegments(new T3.BufferGeometry().setFromPoints([v3(tx - w, 0, z), v3(0.06, 0, z)]), matT));
    B.scene.add(torre);
    window._torre = torre;
    const fr = new T3.DirectionalLight(0xffffff, 0.9); fr.position.set(-2, -8, 3); B.scene.add(fr);       // frente: o casco de pé recebe luz
  } else {
    B.ceu(false);
  }

  // ── jato (partículas) ─────────────────────────────
  const NMAX = 4000, gpos = new Float32Array(NMAX * 3), gcor = new Float32Array(NMAX * 3);
  const ggeo = new T3.BufferGeometry(); ggeo.setAttribute('position', new T3.BufferAttribute(gpos, 3)); ggeo.setAttribute('color', new T3.BufferAttribute(gcor, 3));
  const texP = B.sprite(64, 0.6);
  const gmat = new T3.PointsMaterial({ size: 4, sizeAttenuation: false, vertexColors: true, map: texP, transparent: true, depthWrite: false, fog: false });
  const gas = new T3.Points(ggeo, gmat); gas.frustumCulled = false; B.scene.add(gas);
  // v2: duas populações distintas (T3-7/T3-8): PARA TRÁS = 2 px, #6F7F9C, opacidade 0,6, sem brilho · PARA A FRENTE = 5 px, branco, com halo leve
  const gpos2 = new Float32Array(NMAX * 3), gcor2 = new Float32Array(NMAX * 3);
  const ggeo2 = new T3.BufferGeometry(); ggeo2.setAttribute('position', new T3.BufferAttribute(gpos2, 3)); ggeo2.setAttribute('color', new T3.BufferAttribute(gcor2, 3));
  const ringTex = (() => { const c = document.createElement('canvas'); c.width = c.height = 64; const x = c.getContext('2d');
    x.fillStyle = 'rgba(255,169,77,0.30)'; x.beginPath(); x.arc(32, 32, 24, 0, 2 * Math.PI); x.fill();
    x.strokeStyle = '#FFFFFF'; x.lineWidth = 5; x.beginPath(); x.arc(32, 32, 24, 0, 2 * Math.PI); x.stroke();
    const t = new T3.CanvasTexture(c); return t; })();
  const gmat2 = new T3.PointsMaterial({ size: 7, sizeAttenuation: false, vertexColors: true, map: ringTex, transparent: true, depthWrite: false, fog: false });
  const gas2 = new T3.Points(ggeo2, gmat2); gas2.frustumCulled = false; B.scene.add(gas2);
  const CORG = [[1.0, 0.66, 0.30], [1.0, 0.66, 0.30], [1.0, 1.0, 1.0]];      // v5: tudo é a mesma massa (âmbar). PARA TRÁS = âmbar cheio · PARA A FRENTE = âmbar a 25% com anel branco      // #DDE6F5 neutro · #8FA0BE × 0,9 · branco

  const atualiza = e => {
    const f = e.f || {}, esc = f.esc || 1, ax = f.eixo || 'z';
    F.raiz.position.set(f.x || 0, f.y || 0, f.z || 0);
    F.raiz.scale.setScalar(esc);
    F.raiz.rotation.set(0, 0, 0);
    if (ax === 'z') F.raiz.rotation.x = PI / 2; else F.raiz.rotation.z = -PI / 2;
    if (f.rol) F.raiz.rotateY(f.rol);
    const corte = cl(f.corte || 0, 0, 1), tq = f.tq || [0, 0];
    matCasco.opacity = 1 - 0.72 * corte; matEsc.opacity = 1 - 0.6 * corte;
    matCasco.depthWrite = matEsc.depthWrite = corte < 0.05;
    matTq.forEach((m, k) => { m.opacity = 0.9 * corte; m.emissiveIntensity = 0.62 * (tq[k] || 0); });
    matCarga.opacity = corte; matCarga.emissiveIntensity = 0.9 * (f.carga || 0);
    matChama[0].opacity = 0.6 * cl(f.ch1 || 0, 0, 1); F.ch1.scale.set(1, 0.6 + 0.6 * cl(f.ch1 || 0, 0, 1), 1);
    matChama[1].opacity = 0.6 * cl(f.ch2 || 0, 0, 1); F.ch2.scale.set(1, 0.6 + 0.6 * cl(f.ch2 || 0, 0, 1), 1);
    const sep = f.sep || [0, 0];
    F.est1.position.set(0, -sep[0], 0); F.est1.rotation.set(0, 0, 0);
    if (sep[1]) { F.est1.position.y += Y.s1 / 2; F.est1.rotateX(sep[1]); F.est1.translateY(-Y.s1 / 2); }
    F.est2.visible = f.op2 == null || f.op2 > 0.01;
    if (window._torre) window._torre.visible = (f.torre == null ? true : !!f.torre) && !f.espaco;
    if (id === 'rampa') { solo.forEach(o => { o.visible = !f.espaco; }); B.ceu(!!f.espaco); }
    const g = e.gas || { p: [], c: [] }, n = Math.min(NMAX, (g.p || []).length / 3);
    let nA = 0, nB = 0, modo = false;
    for (let i = 0; i < n; i++) {
      const k = g.c ? g.c[i] : 0, a = g.a ? g.a[i] : 1, c = CORG[k];
      if (k) modo = true;
      if (k === 2) {
        gpos2[3 * nB] = g.p[3 * i]; gpos2[3 * nB + 1] = g.p[3 * i + 1]; gpos2[3 * nB + 2] = g.p[3 * i + 2];
        gcor2[3 * nB] = c[0] * a; gcor2[3 * nB + 1] = c[1] * a; gcor2[3 * nB + 2] = c[2] * a; nB++;
      } else {
        gpos[3 * nA] = g.p[3 * i]; gpos[3 * nA + 1] = g.p[3 * i + 1]; gpos[3 * nA + 2] = g.p[3 * i + 2];
        gcor[3 * nA] = c[0] * a; gcor[3 * nA + 1] = c[1] * a; gcor[3 * nA + 2] = c[2] * a; nA++;
      }
    }
    ggeo.setDrawRange(0, nA); ggeo.attributes.position.needsUpdate = true; ggeo.attributes.color.needsUpdate = true;
    ggeo2.setDrawRange(0, nB); ggeo2.attributes.position.needsUpdate = true; ggeo2.attributes.color.needsUpdate = true;
    gmat.size = modo ? 4 : (g.s || 4); gas.visible = nA > 0; gmat2.size = 7; gas2.visible = nB > 0;
  };
  // pontos projetados (QA de alinhamento): bocal, topo, carga, centro do 1º estágio; e as 3 primeiras partículas
  const pontos = e => {
    F.raiz.updateMatrixWorld(true);
    const w = q => { const v = v3(...q); F.raiz.localToWorld(v); return B.projeta(v.toArray()); };
    const w1 = q => { const v = v3(...q); F.est1.localToWorld(v); return B.projeta(v.toArray()); };
    const g = e.gas || { p: [] }, ps = [];
    for (let i = 0; i < Math.min(3, (g.p || []).length / 3); i++) ps.push(B.projeta([g.p[3 * i], g.p[3 * i + 1], g.p[3 * i + 2]]));
    return { bocal: w([0, 0, 0]), topo: w([0, Y.topo, 0]), carga: w([0, Y.s2 + 0.05, 0]), est1: w1([0, Y.s1 / 2, 0]), ie: w([0, Y.ie, 0]), gas: ps };
  };

  window.CENA = { atualiza };
  window.pontos3d = e => pontos(e);
  window.cenaPronta = true;
})();
