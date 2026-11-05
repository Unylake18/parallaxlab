// yt_0020: cenas 3D por estado (Three.js r128, base b3d.js do yt_0019). Cena escolhida por window.CENA_ID (no .html).
//   'helice' — H1–H3, T4-2, S2: hélice de três pás (diâmetro 1,9 m) no plano x–z, eixo ao longo de y (aponta para a câmera 'frente').
//   'disco'  — T5-1, T5-5…T5-8: o disco de referência com volume (raio 1, face de cima em z = 0, eixo +z), ω⃗, α⃗, r⃗, r_⊥, v⃗ = ω⃗ × r⃗, a⃗.
//   'livros' — T5-2…T5-4: dois livros iguais girados por matrizes do LABORATÓRIO (x direita, y cima, z para a câmera), eixos fixos.
//   'terra'  — E3-1/E3-2 (modo 'orbita': Sol, Terra inclinada, estrela) e E3-4…E3-6 (modo 'geo': Terra no centro, eixo vertical, São Paulo).
// Toda conta de vetor que aparece desenhada (v⃗ = ω⃗ × r⃗, α⃗ × r⃗, ω⃗ × (ω⃗ × r⃗)) é feita AQUI, a cada quadro; o Manim faz a mesma conta para os
// rótulos e o qa20.py compara os pontos projetados (pontos.json) com os do Manim.
(function () {
  const B = B3D, T3 = THREE, PI = Math.PI, id = window.CENA_ID;
  const v3 = (x, y, z) => new T3.Vector3(x, y, z);
  const cl = (x, a, b) => Math.min(b, Math.max(a, x));
  const COR = { vel: 0x9C8CFF, acc: 0x3FE08B, geo: 0xB8C4DA, ang: 0xFFC24D, branco: 0xF5F7FF };

  // ── luz B (a mesma do yt_0017/0018/0019): ambiente azul-noite com recorte BLUE_L e toque magenta ─────────────────────────────
  const envB = (() => {
    const s = new T3.Scene();
    const g = new T3.SphereGeometry(60, 48, 24), cor = [], c0 = new T3.Color(0x1A2B4A), c1 = new T3.Color(0x3A5C8E), pos = g.attributes.position;
    for (let i = 0; i < pos.count; i++) { const u = cl((pos.getY(i) / 60 + 0.35) / 1.1, 0, 1); const c = c0.clone().lerp(c1, u); cor.push(c.r, c.g, c.b); }
    g.setAttribute('color', new T3.Float32BufferAttribute(cor, 3));
    s.add(new T3.Mesh(g, new T3.MeshBasicMaterial({ vertexColors: true, side: T3.BackSide })));
    const painel = (w, h, cor, int, x, y, z) => { const m = new T3.Mesh(new T3.PlaneGeometry(w, h), new T3.MeshBasicMaterial({ color: new T3.Color(cor).multiplyScalar(int), side: T3.DoubleSide }));
      m.position.set(x, y, z); m.lookAt(0, 0, 0); s.add(m); };
    painel(36, 16, 0xF5F7FF, 2.4, 0, -20, 40);
    painel(22, 30, 0x7FB2FF, 2.6, -38, -10, 18);
    painel(12, 20, 0xEA63FF, 1.5, 38, -8, 18);
    return new T3.PMREMGenerator(B.renderer).fromScene(s, 0.04).texture;
  })();
  B.scene.environment = envB;
  B.luz.rim.intensity = 0.2;
  const recA = new T3.DirectionalLight(0x7FB2FF, 1.1), recB = new T3.DirectionalLight(0xEA63FF, 0.34);
  recA.position.set(-6, -4, 6); recB.position.set(6, -3, 7); B.scene.add(recA, recB);

  const aco = (op) => new T3.MeshStandardMaterial({ color: 0x7A8696, metalness: 0.78, roughness: 0.34, envMapIntensity: 0.7, transparent: op != null, opacity: op == null ? 1 : op });
  const plano = (cor, op) => new T3.MeshBasicMaterial({ color: cor, transparent: true, opacity: op == null ? 1 : op, depthWrite: false, side: T3.DoubleSide });

  // ── primitivas: haste (cilindro unitário), seta (haste + cone), tracejado (vários segmentos), anel/arco (tubo) ─────────────────────────────
  const GCIL = new T3.CylinderGeometry(1, 1, 1, 20, 1, false), GCONE = new T3.ConeGeometry(1, 1, 24);
  const UP = v3(0, 1, 0);
  function haste(mat) { const m = new T3.Mesh(GCIL, mat); m.renderOrder = 5; B.scene.add(m); return m; }
  function poeHaste(m, a, b, r) {
    const A = v3(...a), Bv = v3(...b), d = Bv.clone().sub(A), L = d.length();
    m.visible = L > 1e-4 && r > 0;
    if (!m.visible) return;
    m.position.copy(A).addScaledVector(d, 0.5);
    m.quaternion.setFromUnitVectors(UP, d.normalize());
    m.scale.set(r, L, r);
  }
  function seta(cor) {
    const mat = new T3.MeshBasicMaterial({ color: cor, transparent: true, opacity: 1, depthTest: true });
    const h = new T3.Mesh(GCIL, mat), p = new T3.Mesh(GCONE, mat);
    h.renderOrder = p.renderOrder = 6; B.scene.add(h, p);
    return { h, p, mat };
  }
  function poeSeta(s, a, b, r, op, tip) {
    const A = v3(...a), Bv = v3(...b), d = Bv.clone().sub(A), L = d.length();
    const vis = L > 1e-4 && (op == null || op > 0.01);
    s.h.visible = s.p.visible = vis;
    if (!vis) return;
    s.mat.opacity = op == null ? 1 : op;
    const u = d.clone().normalize(), tl = Math.min(tip || 6 * r, 0.45 * L);
    const base = Bv.clone().addScaledVector(u, -tl);
    s.h.position.copy(A).addScaledVector(base.clone().sub(A), 0.5);
    s.h.quaternion.setFromUnitVectors(UP, u); s.h.scale.set(r, Math.max(1e-4, base.distanceTo(A)), r);
    s.p.position.copy(base).addScaledVector(u, tl / 2);
    s.p.quaternion.setFromUnitVectors(UP, u); s.p.scale.set(2.6 * r, tl, 2.6 * r);
  }
  function tracejado(cor, n) {
    const mat = new T3.MeshBasicMaterial({ color: cor, transparent: true, opacity: 1 });
    const segs = []; for (let i = 0; i < n; i++) { const m = new T3.Mesh(GCIL, mat); m.renderOrder = 5; B.scene.add(m); segs.push(m); }
    return { segs, mat };
  }
  function poeTracejado(t, a, b, r, op, passo) {
    const A = v3(...a), Bv = v3(...b), L = A.distanceTo(Bv), n = t.segs.length;
    const k = Math.min(n, Math.max(1, Math.floor(L / (passo || 0.08))));
    t.mat.opacity = op == null ? 1 : op;
    for (let i = 0; i < n; i++) {
      if (i >= k || !(op == null || op > 0.01)) { t.segs[i].visible = false; continue; }
      const u0 = i / k, u1 = (i + 0.55) / k;
      poeHaste(t.segs[i], A.clone().lerp(Bv, u0).toArray(), A.clone().lerp(Bv, u1).toArray(), r);
    }
  }
  function linhaPts(cor, n, r) {          // polilinha grossa (tubos curtos) para arcos e círculos
    const mat = new T3.MeshBasicMaterial({ color: cor, transparent: true, opacity: 1 });
    const segs = []; for (let i = 0; i < n; i++) { const m = new T3.Mesh(GCIL, mat); m.renderOrder = 5; B.scene.add(m); segs.push(m); }
    return { segs, mat, r };
  }
  function poeLinha(l, pts, op, tracej) {
    l.mat.opacity = op == null ? 1 : op;
    for (let i = 0; i < l.segs.length; i++) {
      if (i >= pts.length - 1 || !(op == null || op > 0.01) || (tracej && i % 2)) { l.segs[i].visible = false; continue; }
      poeHaste(l.segs[i], pts[i], pts[i + 1], l.r);
    }
  }
  const cruz = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  const soma = (a, b, k) => [a[0] + (k == null ? 1 : k) * b[0], a[1] + (k == null ? 1 : k) * b[1], a[2] + (k == null ? 1 : k) * b[2]];
  const esc = (a, k) => [a[0] * k, a[1] * k, a[2] * k];
  const P = {};                            // pontos projetados do quadro (QA de alinhamento)
  const prj = (nome, p) => { P[nome] = p; };          // projetados em pontos3d, depois de a câmera do quadro ser posta

  // ════════════════════════════════════ hélice ════════════════════════════════════
  if (id === 'helice') {
    const R = 0.95, R0 = 0.12, NB = 3;
    const hel = new T3.Group(); B.scene.add(hel);
    // aço escovado: riscos ao longo do raio (a textura varia só em v), em vez de uma cor chapada
    const texAco = (() => {
      const c = document.createElement('canvas'); c.width = 64; c.height = 256; const g = c.getContext('2d');
      let sd = 7; const rnd = () => { sd = (sd * 16807) % 2147483647; return sd / 2147483647; };
      for (let y = 0; y < 256; y++) { const v = 175 + Math.floor(rnd() * 70); g.fillStyle = 'rgb(' + v + ',' + (v + 4) + ',' + (v + 10) + ')'; g.fillRect(0, y, 64, 1); }
      return new T3.CanvasTexture(c);
    })();
    const mAco = new T3.MeshStandardMaterial({ color: 0xBCC4D4, map: texAco, metalness: 0.55, roughness: 0.5, envMapIntensity: 0.6, side: T3.DoubleSide });
    const mFaixa = new T3.MeshStandardMaterial({ color: 0xF4F6FF, emissive: 0x4A5070, metalness: 0.05, roughness: 0.45, envMapIntensity: 0.5, side: T3.DoubleSide });
    const naca = (x, tt) => 5 * tt * (0.2969 * Math.sqrt(x) - 0.126 * x - 0.3516 * x * x + 0.2843 * x * x * x - 0.1036 * x * x * x * x);
    // pá: perfil de aerofólio (NACA simétrico) com corda que afina e torção que cai do cubo para a ponta; t ∈ [0, 1] ao longo do raio
    function lamina(t0, t1, nR) {
      const Mq = 16, pos = [], uv = [], ind = [], S = 2 * Mq + 1;
      for (let i = 0; i <= nR; i++) {
        const t = t0 + (t1 - t0) * i / nR, r = R0 + (R - R0) * t;
        const c = 0.2 * (1 - 0.5 * t) * (t > 0.94 ? 1 - 0.45 * Math.pow((t - 0.94) / 0.06, 2) : 1);
        const tt = 0.13 - 0.06 * t, tw = (28 - 20 * t) * PI / 180;
        for (let j = 0; j < S; j++) {
          const k = j <= Mq ? Mq - j : j - Mq, xs = 0.5 * (1 - Math.cos(PI * k / Mq)), yy = (j <= Mq ? 1 : -1) * naca(xs, tt) * c, zc = (0.25 - xs) * c;
          pos.push(r, zc * Math.sin(tw) + yy * Math.cos(tw), zc * Math.cos(tw) - yy * Math.sin(tw)); uv.push(i / nR, j / (S - 1));
        }
      }
      for (let i = 0; i < nR; i++) for (let j = 0; j < S - 1; j++) { const a = i * S + j, b = a + 1, c2 = a + S, d = c2 + 1; ind.push(a, c2, b, b, c2, d); }
      if (t1 >= 1) {                                                   // tampa a ponta (leque até o centro da última seção)
        const base = pos.length / 3, last = nR * S; let cx = 0, cy = 0, cz = 0;
        for (let j = 0; j < S; j++) { cx += pos[3 * (last + j)]; cy += pos[3 * (last + j) + 1]; cz += pos[3 * (last + j) + 2]; }
        pos.push(cx / S, cy / S, cz / S); uv.push(1, 0.5); for (let j = 0; j < S - 1; j++) ind.push(last + j, last + j + 1, base);
      }
      const g = new T3.BufferGeometry(); g.setAttribute('position', new T3.Float32BufferAttribute(pos, 3)); g.setAttribute('uv', new T3.Float32BufferAttribute(uv, 2));
      g.setIndex(ind); g.computeVertexNormals(); return g;
    }
    // cubo: placa, spinner cônico (aponta para a câmera, −y) e seis parafusos
    const placa = new T3.Mesh(new T3.CylinderGeometry(0.17, 0.17, 0.035, 56), mAco); hel.add(placa);
    const spinner = new T3.Mesh(new T3.LatheGeometry([[0, -0.205], [0.025, -0.2], [0.055, -0.18], [0.085, -0.145], [0.105, -0.105], [0.113, -0.06], [0.115, -0.0175]].map(q => new T3.Vector2(q[0], q[1])), 40), mAco);
    hel.add(spinner);
    const mParaf = new T3.MeshStandardMaterial({ color: 0xE3E8F4, metalness: 0.9, roughness: 0.22, envMapIntensity: 1.0 });
    for (let k = 0; k < 6; k++) { const a = k * PI / 3 + PI / 6, q = new T3.Mesh(new T3.CylinderGeometry(0.013, 0.013, 0.016, 14), mParaf); q.position.set(0.145 * Math.cos(a), -0.0255, 0.145 * Math.sin(a)); hel.add(q); }
    for (let k = 0; k < NB; k++) {
      const piv = new T3.Group();
      piv.add(new T3.Mesh(lamina(0, 0.86, 22), mAco), new T3.Mesh(lamina(0.86, 1, 8), mFaixa));           // a faixa clara da ponta marca o ponto de 967 km/h
      piv.rotation.y = -k * 2 * PI / NB; hel.add(piv);
    }
    var atualiza = e => {
      hel.rotation.set(0, -(e.ang || 0), 0);                   // anti-horário na tela (eixo +(-y) aponta para a câmera)
      hel.visible = e.op == null || e.op > 0.01;
      const a = e.ang || 0;
      prj('r10', [0.10 * Math.cos(a), -0.07, 0.10 * Math.sin(a)]); prj('r95', [R * Math.cos(a), -0.07, R * Math.sin(a)]); prj('eixo', [0, -0.07, 0]);
    };
  }

  // ════════════════════════════════════ disco ════════════════════════════════════
  if (id === 'disco') {
    const H = 0.14, Rd = 1.0, ch = 0.035;
    const dg = new T3.Group(); B.scene.add(dg);
    // aço escovado com riscos concêntricos (a textura varia ao longo do perfil) e chanfro na borda; topo em z = 0, base em z = −H
    const texEsc = (() => {
      const c = document.createElement('canvas'); c.width = 8; c.height = 256; const g = c.getContext('2d');
      let sd = 11; const rnd = () => { sd = (sd * 16807) % 2147483647; return sd / 2147483647; };
      for (let y = 0; y < 256; y++) { const v = 222 + Math.floor(rnd() * 26); g.fillStyle = 'rgb(' + v + ',' + (v + 1) + ',' + (v + 3) + ')'; g.fillRect(0, y, 8, 1); }
      return new T3.CanvasTexture(c);
    })();
    const mDisco = new T3.MeshStandardMaterial({ color: 0x8793A3, map: texEsc, metalness: 0.6, roughness: 0.4, envMapIntensity: 0.24 });
    const gDisco = new T3.LatheGeometry([[0, -H], [Rd - ch, -H], [Rd, -H + ch], [Rd, -ch], [Rd - ch, 0], [0, 0]].map(q => new T3.Vector2(q[0], q[1])), 128); gDisco.rotateX(PI / 2);
    const corpo = new T3.Mesh(gDisco, mDisco); dg.add(corpo);
    const linha = new T3.Mesh(new T3.PlaneGeometry(Rd, 0.065), new T3.MeshBasicMaterial({ color: COR.ang })); linha.position.set(Rd / 2, 0, 0.002); dg.add(linha);
    const aroE = new T3.Mesh(new T3.RingGeometry(Rd - 0.07, Rd - 0.035, 128), new T3.MeshBasicMaterial({ color: 0x1A2438 })); aroE.position.z = 0.0015; dg.add(aroE);
    const aroC = new T3.Mesh(new T3.RingGeometry(Rd - 0.035, Rd - 0.012, 128), new T3.MeshBasicMaterial({ color: 0xDCE4F2 })); aroC.position.z = 0.0016; dg.add(aroC);      // linha pintada âmbar
    recA.intensity = 0.12; recB.intensity = 0.04; B.luz.chave.intensity = 1.35; B.luz.amb.intensity = 0.22;      // luz mais neutra: o aço lê como aço (a luz B azul/magenta deixava a face de cima lavanda)
    const sombraD = B.sombra(3.5, 3.5); sombraD.position.z = -H - 0.07;                                                                                                       // sombra de contato suave no "chão"
    const pontosD = [1, 2, 3].map(k => { const g = new T3.Group();
      const b = new T3.Mesh(new T3.CircleGeometry(0.05, 32), new T3.MeshBasicMaterial({ color: COR.branco })); const c = new T3.Mesh(new T3.RingGeometry(0.05, 0.065, 32), new T3.MeshBasicMaterial({ color: 0x2A3550 }));
      g.add(b, c); g.position.set(Rd * k / 3, 0, 0.004); dg.add(g); return g; });
    const pino = new T3.Mesh(new T3.CylinderGeometry(0.06, 0.06, 0.05, 32), aco()); pino.rotation.x = PI / 2; pino.position.z = 0.025; dg.add(pino);
    const eixo = haste(new T3.MeshStandardMaterial({ color: 0xB8C4DA, metalness: 0.6, roughness: 0.4, transparent: true, opacity: 1 }));
    const ref = tracejado(COR.geo, 20);
    const sW = seta(COR.vel), sAl = seta(COR.acc), sR = seta(COR.geo), sV = seta(COR.vel), sAt = seta(COR.acc), sAc = seta(COR.acc), sR2 = seta(COR.geo), sV2 = seta(COR.vel), sAt2 = seta(COR.acc);
    const rp = tracejado(COR.geo, 14);
    const par = new T3.Mesh(new T3.BufferGeometry(), plano(0x9C8CFF, 0.42)); B.scene.add(par);
    par.geometry.setAttribute('position', new T3.Float32BufferAttribute(new Float32Array(18), 3));
    const arcoPhi = linhaPts(COR.ang, 24, 0.02);
    const Oball = new T3.Mesh(new T3.SphereGeometry(0.035, 16, 12), new T3.MeshBasicMaterial({ color: COR.branco, transparent: true })); B.scene.add(Oball);
    // mão direita: palma achatada, quatro dedos (arcos de tubo empilhados em z) curvados no sentido do giro em volta do eixo, polegar ao longo de +z; contorno escuro nítido
    const matMao = new T3.MeshStandardMaterial({ color: 0xC4CFE4, metalness: 0.05, roughness: 0.5, transparent: true, opacity: 0 });
    const matCt = new T3.MeshBasicMaterial({ color: 0x0B1530, transparent: true, opacity: 0, side: T3.BackSide });
    const mao = new T3.Group(); B.scene.add(mao);
    const peca = (geo, geoCt, f) => { const a = new T3.Mesh(geo, matMao), b = new T3.Mesh(geoCt, matCt); if (f) { f(a); f(b); } mao.add(b, a); return a; };
    const ARC = 1.2 * PI;
    for (let k = 0; k < 4; k++) { const z = -0.105 + 0.07 * k, rr = 0.26 - 0.012 * Math.abs(k - 1.5);
      peca(new T3.TorusGeometry(rr, 0.036, 14, 40, ARC), new T3.TorusGeometry(rr, 0.052, 14, 40, ARC), m => { m.position.z = z; });
      const ang = ARC; peca(new T3.SphereGeometry(0.036, 14, 10), new T3.SphereGeometry(0.052, 14, 10), m => { m.position.set(rr * Math.cos(ang), rr * Math.sin(ang), z); }); }
    peca(new T3.BoxGeometry(0.12, 0.2, 0.3), new T3.BoxGeometry(0.15, 0.23, 0.33), m => { m.position.set(0.26, 0.0, 0.0); });
    peca(new T3.CylinderGeometry(0.05, 0.05, 0.36, 16), new T3.CylinderGeometry(0.068, 0.068, 0.39, 16), m => { m.rotation.x = PI / 2; m.position.set(0.2, 0, 0.3); });
    peca(new T3.SphereGeometry(0.05, 14, 10), new T3.SphereGeometry(0.068, 14, 10), m => { m.position.set(0.2, 0, 0.48); });
    var atualiza = e => {
      const th = e.th || 0, esp = e.esp == null ? 1 : e.esp;
      dg.rotation.set(0, 0, th);
      corpo.scale.set(1, 1, Math.max(0.02, esp)); sombraD.material.opacity = cl(esp, 0, 1);
      pontosD.forEach(g => { g.visible = true; });
      const zt = e.eixo || 0;
      poeHaste(eixo, [0, 0, -1.1], [0, 0, 1.25], 0.022 * zt); eixo.material.opacity = cl(zt, 0, 1);
      poeTracejado(ref, [0.0, 0.0, 0.001], [1.32, 0, 0.001], 0.007, e.ref == null ? 0.7 : e.ref, 0.07);
      const w = e.w || 0, al = e.al || 0, kw = e.kw || 1, ka = e.ka || 0.35, kv = e.kv || 0.8;
      const O = [0, 0, e.z0 || 0];
      const wz0 = e.wbase == null ? 0.02 : (e.wbase === 'O' ? O[2] : e.wbase);
      poeSeta(sW, [0, 0, wz0], [0, 0, wz0 + kw * w], 0.03, e.ow == null ? (w ? 1 : 0) : e.ow);
      poeSeta(sAl, [0.12, 0, 0.02], [0.12, 0, 0.02 + kw * al], 0.03, e.oal == null ? (al ? 1 : 0) : e.oal);
      const Pp = [Rd * Math.cos(th), Rd * Math.sin(th), 0.01], P2 = [-Pp[0], -Pp[1], 0.01];
      const om = [0, 0, w], alv = [0, 0, al];
      const r = soma(Pp, O, -1), r2 = soma(P2, O, -1);
      const v = cruz(om, r), v2 = cruz(om, r2), at = cruz(alv, r), ac = cruz(om, cruz(om, r)), at2 = cruz(alv, r2);
      poeSeta(sR, O, Pp, 0.018, e.or || 0, 0.07); poeSeta(sR2, O, P2, 0.014, e.or2 || 0, 0.07);
      poeSeta(sV, Pp, soma(Pp, v, kv), 0.03, e.ov || 0); poeSeta(sV2, P2, soma(P2, v2, kv), 0.03, e.ov2 || 0);
      poeSeta(sAt, Pp, soma(Pp, at, ka), 0.03, e.oat || 0); poeSeta(sAc, Pp, soma(Pp, ac, ka), 0.03, e.oac || 0); poeSeta(sAt2, P2, soma(P2, at2, ka), 0.03, e.oat2 || 0);
      poeTracejado(rp, [0, 0, Pp[2]], Pp, 0.009, e.orp || 0, 0.07);
      Oball.visible = (e.oO || 0) > 0.01; Oball.position.set(...O); Oball.material.opacity = e.oO || 0;
      const po = par.geometry.attributes.position.array, A0 = O, A1 = soma(O, [0, 0, kw * w]), A2 = soma(A1, r), A3 = Pp;
      [A0, A1, A2, A0, A2, A3].forEach((q, i) => { po[3 * i] = q[0]; po[3 * i + 1] = q[1]; po[3 * i + 2] = q[2]; });
      par.geometry.attributes.position.needsUpdate = true; par.geometry.computeBoundingSphere();
      par.visible = (e.opar || 0) > 0.01; par.material.opacity = 0.42 * (e.opar || 0);
      // φ entre ω⃗ (eixo) e r⃗, em O: arco âmbar de 0,32 de raio no plano de ω⃗ e r⃗
      const rn = Math.hypot(...r), ru = esc(r, 1 / rn), phi = Math.acos(cl(ru[2], -1, 1)), hu = [Math.cos(th), Math.sin(th), 0], arc = [];
      for (let i = 0; i <= 20; i++) { const a = phi * i / 20; arc.push(soma(O, soma(esc([0, 0, 1], 0.32 * Math.cos(a)), hu, 0.32 * Math.sin(a)))); }
      poeLinha(arcoPhi, arc, e.ophi || 0);
      const om_ = e.omao || 0; matMao.opacity = om_; matCt.opacity = om_; mao.visible = om_ > 0.01;
      mao.position.set(0, 0, 0.55); mao.rotation.set(0, 0, 0.4);
      prj('centro', [0, 0, 0]); prj('P', Pp); prj('P2', P2); prj('O', O); prj('wtopo', [0, 0, wz0 + kw * w]); prj('vtopo', soma(Pp, v, kv)); prj('v2topo', soma(P2, v2, kv));
      prj('at', soma(Pp, at, ka)); prj('ac', soma(Pp, ac, ka)); prj('altopo', [0.12, 0, 0.02 + kw * al]);
      window._vet = { v, v2, at, ac, r, r2 };
    };
  }

  // ════════════════════════════════════ livros ════════════════════════════════════
  if (id === 'livros') {
    const W = 0.23, Hh = 0.16, E = 0.04, LOG = window.TEX20 || {};
    const ld = new T3.TextureLoader();
    const tCapa = ld.load(LOG.capa), tContra = ld.load(LOG.contra);
    const mCapa = new T3.MeshStandardMaterial({ map: tCapa, metalness: 0.0, roughness: 0.55, envMapIntensity: 0.6 });
    const mContra = new T3.MeshStandardMaterial({ map: tContra, metalness: 0.0, roughness: 0.6, envMapIntensity: 0.6 });
    const mLomb = new T3.MeshStandardMaterial({ color: 0x1FA8D8, metalness: 0.25, roughness: 0.45, envMapIntensity: 0.7 });          // lombada: ciano da marca
    const mPag = new T3.MeshStandardMaterial({ color: 0xEDE3C8, metalness: 0.0, roughness: 0.85, envMapIntensity: 0.4 });
    const fant = (m) => { const c = m.clone(); c.transparent = true; c.opacity = 0.5; c.depthWrite = false; c.emissive = new T3.Color(COR.ang); c.emissiveIntensity = 0.55; return c; };
    // BoxGeometry: faces +x, −x, +y, −y, +z, −z (coordenadas do LIVRO = do laboratório no estado inicial: capa em +z, lombada em −x)
    const livro = (ghost) => {
      const ms = [mPag, mLomb, mPag, mPag, mCapa, mContra].map(m => ghost ? fant(m) : m);
      const g = new T3.Group(); const b = new T3.Mesh(new T3.BoxGeometry(W, Hh, E), ms); g.add(b);
      // o livro vive no LAB; o grupo de fora converte LAB → mundo (x, y, z) → (x, −z, y)
      const o = new T3.Group(); o.add(g); o.matrixAutoUpdate = true; B.scene.add(o); return { o, g, ms };
    };
    const Lv = livro(false), Rv = livro(false), Gv = livro(true);
    const M = new T3.Matrix4().set(1, 0, 0, 0, 0, 0, -1, 0, 0, 1, 0, 0, 0, 0, 0, 1);         // LAB → mundo
    const eixos = [0, 1].map(() => ({ x: seta(COR.geo), y: seta(COR.geo), z: seta(COR.geo) }));
    const sNorm = [seta(COR.geo), seta(COR.geo)], sNormG = seta(COR.ang);       // seta normal à capa (D27) e a do fantasma de comparação (D29)
    const poeLivro = (L, c, R9, op) => {
      L.o.visible = op == null || op > 0.01;
      const R4 = new T3.Matrix4().set(R9[0], R9[1], R9[2], 0, R9[3], R9[4], R9[5], 0, R9[6], R9[7], R9[8], 0, 0, 0, 0, 1);
      const Mw = M.clone().multiply(R4);
      L.o.matrix.identity(); L.o.matrixAutoUpdate = false;
      L.o.matrix.copy(new T3.Matrix4().makeTranslation(...c).multiply(Mw)); L.o.matrixWorldNeedsUpdate = true;
      if (op != null && L.ms[0].transparent) L.ms.forEach(m => { m.opacity = 0.5 * op; });
    };
    var atualiza = e => {
      const cs = e.c || [[-0.2, 0, 0], [0.2, 0, 0]];
      poeLivro(Lv, cs[0], e.L || [1, 0, 0, 0, 1, 0, 0, 0, 1], e.oL);
      poeLivro(Rv, cs[1], e.R || [1, 0, 0, 0, 1, 0, 0, 0, 1], e.oR);
      poeLivro(Gv, cs[0], e.G || [1, 0, 0, 0, 1, 0, 0, 0, 1], e.oG || 0);
      const s = e.sx || 0.17, oe = e.oe == null ? 1 : e.oe;
      const normal = (R9) => { const n = [R9[2], -R9[8], R9[5]]; return n; };           // terceira coluna da matriz do livro (LAB) → mundo (x, −z, y)
      [[Lv, e.L, 0], [Rv, e.R, 1]].forEach(([L_, R9, k]) => {
        R9 = R9 || [1, 0, 0, 0, 1, 0, 0, 0, 1]; const n = normal(R9), c = cs[k], b = soma(c, n, E / 2), len = e.ln || 0.12;
        poeSeta(sNorm[k], b, soma(b, n, len), 0.0075, e.on == null ? 1 : e.on, 0.03); prj('nb' + k, b); prj('nt' + k, soma(b, n, len));
      });
      { const R9 = e.G || [1, 0, 0, 0, 1, 0, 0, 0, 1], n = normal(R9), b = soma(cs[0], n, E / 2), len = e.ln || 0.12;
        poeSeta(sNormG, b, soma(b, n, len), 0.0075, e.oNg == null ? (e.oG || 0) : e.oNg, 0.03); prj('ngt', soma(b, n, len)); }
      cs.forEach((c, k) => {      // eixos do LAB em cada livro: x (direita) e y (cima → mundo +z); z (para a câmera → mundo −y) só se pedido
        poeSeta(eixos[k].x, c, soma(c, [s, 0, 0]), 0.0035, oe, 0.025);
        poeSeta(eixos[k].y, c, soma(c, [0, 0, s]), 0.0035, oe, 0.025);
        poeSeta(eixos[k].z, c, soma(c, [0, -s, 0]), 0.0035, e.oz || 0, 0.025);
        prj('c' + k, c); prj('x' + k, soma(c, [s, 0, 0])); prj('y' + k, soma(c, [0, 0, s]));
      });
    };
  }

  // ════════════════════════════════════ terra ════════════════════════════════════
  if (id === 'terra') {
    const tex = new T3.TextureLoader().load((window.TEX20 || {}).terra);
    const mT = new T3.MeshStandardMaterial({ map: tex, bumpMap: tex, bumpScale: 0.07, metalness: 0.0, roughness: 0.85, envMapIntensity: 0.35, transparent: true, opacity: 1 });   // relevo suave
    const geoT = new T3.SphereGeometry(1, 96, 64); geoT.rotateX(PI / 2);   // polos em ±z; textura: u = longitude (0 em −x… gira com +z)
    // atmosfera fina: halo azul aditivo (fresnel) numa esfera 4,5% maior, filha do mesmo grupo (acompanha posição, escala e opacidade)
    const matAtm = () => new T3.ShaderMaterial({ uniforms: { uOp: { value: 1 } }, transparent: true, depthWrite: false, side: T3.BackSide, blending: T3.AdditiveBlending,
      vertexShader: 'varying vec3 vN; void main(){ vN = normalize(normalMatrix * normal); gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
      fragmentShader: 'uniform float uOp; varying vec3 vN; void main(){ float f = pow(max(0.0, 0.68 - dot(vN, vec3(0.0, 0.0, 1.0))), 2.6); gl_FragColor = vec4(0.30, 0.58, 1.0, 1.0) * f * 1.25 * uOp; }' });
    const terras = [0, 1].map(k => { const tilt = new T3.Group(), spin = new T3.Mesh(geoT, k ? mT.clone() : mT); tilt.add(spin);
      const atm = new T3.Mesh(new T3.SphereGeometry(1.045, 64, 48), matAtm()); tilt.add(atm); B.scene.add(tilt); return { tilt, spin, atm }; });
    const sol = new T3.Mesh(new T3.SphereGeometry(1, 48, 32), new T3.MeshBasicMaterial({ color: 0xFFF3DA })); B.scene.add(sol);
    const brilho = new T3.Sprite(new T3.SpriteMaterial({ map: B.sprite(128, 0.55), color: 0xFFE9C2, transparent: true, depthWrite: false, opacity: 0.75 })); B.scene.add(brilho);
    const estrela = new T3.Sprite(new T3.SpriteMaterial({ map: B.sprite(64, 0.5), color: 0xFFFFFF, transparent: true, depthWrite: false })); B.scene.add(estrela);
    const orbita = linhaPts(COR.geo, 160, 0.02);
    const luzSol = new T3.PointLight(0xFFF1DD, 2.2, 0, 1.2); B.scene.add(luzSol);
    // modo geo: eixo, círculo da latitude, São Paulo, vetores
    const eixoT = haste(new T3.MeshBasicMaterial({ color: COR.geo, transparent: true }));
    const lat = linhaPts(COR.ang, 96, 0.011), arcL = linhaPts(COR.ang, 24, 0.008);                  // círculo de latitude de São Paulo: faixa âmbar sobre a superfície
    const sp = new T3.Mesh(new T3.SphereGeometry(0.03, 16, 12), new T3.MeshBasicMaterial({ color: COR.branco, depthTest: false })); sp.renderOrder = 9; B.scene.add(sp);
    const sW = seta(COR.vel), sR = seta(COR.geo), sV = seta(COR.vel), sAc = seta(COR.acc);
    [sW, sR, sV, sAc].forEach(s => { s.mat.depthTest = false; s.h.renderOrder = s.p.renderOrder = 8; });
    const rp = tracejado(COR.geo, 18), rad = tracejado(COR.branco, 14);
    [rp, rad].forEach(t => { t.mat.depthTest = false; t.segs.forEach(m => { m.renderOrder = 8; }); });
    const par = new T3.Mesh(new T3.BufferGeometry(), plano(0x9C8CFF, 0.2)); par.material.depthTest = false; par.renderOrder = 7; B.scene.add(par);
    par.geometry.setAttribute('position', new T3.Float32BufferAttribute(new Float32Array(18), 3));
    const LAT = -23.55 * PI / 180;
    var atualiza = e => {
      const geo = e.modo === 'geo';
      B.ceu(false);
      (e.terras || [{}]).forEach((t, k) => {
        const T = terras[k]; T.tilt.visible = (t.op == null ? 1 : t.op) > 0.01;
        T.tilt.position.set(...(t.p || [0, 0, 0])); T.tilt.scale.setScalar(t.r || 1);
        T.tilt.rotation.set(0, (t.incl || 0) * PI / 180, 0);           // inclinação do eixo (em torno de y do mundo)
        T.spin.rotation.set(0, 0, t.rot || 0);
        T.spin.material.opacity = t.op == null ? 1 : t.op; T.spin.material.depthWrite = (t.op == null ? 1 : t.op) > 0.9; T.atm.material.uniforms.uOp.value = t.op == null ? 1 : t.op;
      });
      terras[1].tilt.visible = terras[1].tilt.visible && (e.terras || []).length > 1;
      const s = e.sol || null; sol.visible = brilho.visible = !!s;
      if (s) { sol.position.set(...s.p); sol.scale.setScalar(s.r); brilho.position.set(...s.p); brilho.scale.setScalar(s.r * 4.2); luzSol.position.set(...s.p); }
      luzSol.intensity = s ? 2.2 : 0; B.luz.chave.intensity = s ? 0.25 : 1.4; B.luz.amb.intensity = s ? 0.12 : 0.25;
      const es = e.estrela; estrela.visible = !!es; if (es) { estrela.position.set(...es.p); estrela.scale.setScalar(es.s || 0.4); }
      const ob = e.orbita;
      if (ob) { const pts = []; for (let i = 0; i <= 159; i++) { const a = 2 * PI * i / 159; pts.push([ob.R * Math.cos(a), ob.R * Math.sin(a), 0]); } poeLinha(orbita, pts, ob.op == null ? 0.55 : ob.op, true); }
      else poeLinha(orbita, [], 0);
      // ── geo ──
      const g = e.g || {};
      const w = g.w || 0, kw = g.kw || 0.9, rot = (e.terras && e.terras[0].rot) || 0, lon = (g.lon || 0) + rot;
      const SP = [Math.cos(LAT) * Math.cos(lon), Math.cos(LAT) * Math.sin(lon), Math.sin(LAT)];
      const om = [0, 0, w], v = cruz(om, SP), ac = cruz(om, cruz(om, SP));
      poeHaste(eixoT, [0, 0, -1.35], [0, 0, 1.35], 0.012 * (g.oeixo || 0)); eixoT.material.opacity = g.oeixo || 0;
      poeSeta(sW, [0, 0, 1.02], [0, 0, 1.02 + kw * w], 0.018, g.ow || 0);
      const lp = []; for (let i = 0; i <= 95; i++) { const a = 2 * PI * i / 95; lp.push([1.004 * Math.cos(LAT) * Math.cos(a), 1.004 * Math.cos(LAT) * Math.sin(a), 1.004 * Math.sin(LAT)]); }
      poeLinha(lat, lp, g.olat || 0, false);
      sp.visible = (g.osp || 0) > 0.01; sp.position.set(...SP);
      poeSeta(sR, [0, 0, 0], SP, 0.011, g.or || 0, 0.06);
      poeTracejado(rp, [0, 0, SP[2]], SP, 0.008, g.orp || 0, 0.06);
      poeSeta(sV, SP, soma(SP, v, g.kv || 0.6), 0.016, g.ov || 0);
      poeSeta(sAc, SP, soma(SP, ac, g.ka || 0.6), 0.016, g.oac || 0);
      poeTracejado(rad, SP, esc(SP, 0.45), 0.007, g.orad || 0, 0.06);
      const po = par.geometry.attributes.position.array, A1 = [0, 0, kw * w], A2 = soma(A1, SP);
      [[0, 0, 0], A1, A2, [0, 0, 0], A2, SP].forEach((q, i) => { po[3 * i] = q[0]; po[3 * i + 1] = q[1]; po[3 * i + 2] = q[2]; });
      par.geometry.attributes.position.needsUpdate = true; par.geometry.computeBoundingSphere();
      par.visible = (g.opar || 0) > 0.01; par.material.opacity = 0.2 * (g.opar || 0);
      // λ: arco âmbar em São Paulo, entre a direção de a_c (para o eixo, horizontal) e a radial para o centro
      const hu = [-Math.cos(lon), -Math.sin(lon), 0], ru = esc(SP, -1), arc = [];
      for (let i = 0; i <= 22; i++) { const u = i / 22, d = soma(esc(hu, 1 - u), ru, u), n = Math.hypot(...d); arc.push(soma(SP, d, 0.22 / n)); }
      poeLinha(arcL, arc, g.olam || 0);
      prj('centro', [0, 0, 0]); prj('SP', SP); prj('wtopo', [0, 0, 1.02 + kw * w]); prj('vtopo', soma(SP, v, g.kv || 0.6)); prj('actopo', soma(SP, ac, g.ka || 0.6));
      (e.terras || []).forEach((t, k) => prj('T' + k, t.p || [0, 0, 0]));
      if (s) prj('sol', s.p);
      window._vet = { v, ac, SP };
    };
  }

  window.CENA = { atualiza: e => { for (const k in P) delete P[k]; atualiza(e); } };
  window.pontos3d = e => { const o = {}; for (const k in P) o[k] = B.projeta(P[k]); if (window._vet) o.vet = window._vet; return o; };
  if (id === 'livros' || id === 'terra') T3.DefaultLoadingManager.onLoad = () => { window.cenaPronta = true; };
  else window.cenaPronta = true;
})();
