// Hook (H1–H3) e fundo do E4-1: muro de concreto de 2,5 m e manequim articulado de artista (aço #7A8696, juntas #B8C4DA).
// Tudo é função do quadro: TL.atores[i].tau[f] é o tempo físico do salto do ator no quadro f (−1 = ator e muro ocultos) e
// TL.atores[i].modo[f] é 'd' (pernas duras) ou 'j' (joelhos). Física: queda livre de 2,5 m (0,714 s), pernas duras param em
// 0,01 s; joelhos: o quadril desce 0,5 m em 1/7 s com desaceleração constante (a = v²/2d = 49 m/s²). IK de 2 segmentos, pé fixo.
(function () {
  const B = B3D, TL = B.TL, T3 = THREE, PI = Math.PI;
  const G_ = 9.8, H_MURO = 2.5, V_CH = Math.sqrt(2 * G_ * H_MURO), T_QUEDA = Math.sqrt(2 * H_MURO / G_);
  const T_PREP = 1.0, VX = 1.5, D_AGACHA = 0.5, T_AGACHA = 2 * D_AGACHA / V_CH, A_AGACHA = V_CH * V_CH / (2 * D_AGACHA);
  const L1 = 0.46, L2 = 0.46, ANK = 0.085, HIPW = 0.095, XA0 = -0.02, X_POUSO = XA0 + VX * T_QUEDA;
  const clamp = B.clamp, sv = u => B.suave(clamp(u, 0, 1)), lerp = (a, b, u) => a + (b - a) * u;

  // ── materiais ────────────────────────────────────────────────────────────────────────────────────────────
  const mat = (cor, met, rug, env) => new T3.MeshStandardMaterial({ color: cor, metalness: met, roughness: rug, envMapIntensity: env });
  const mAco = mat(0x7A8696, 0.4, 0.45, 0.28), mJunta = mat(0xB8C4DA, 0.4, 0.4, 0.3);
  function texturaConcreto() {
    const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d');
    g.fillStyle = '#7d838c'; g.fillRect(0, 0, 256, 256);
    let s = 7; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    for (let i = 0; i < 9000; i++) { const v = 100 + 70 * rnd(); g.fillStyle = `rgba(${v},${v + 3},${v + 8},0.22)`; g.fillRect(256 * rnd(), 256 * rnd(), 1 + 2 * rnd(), 1 + 2 * rnd()); }
    g.strokeStyle = 'rgba(40,44,52,0.35)'; g.lineWidth = 1.2;
    for (const y of [64, 128, 192]) { g.beginPath(); g.moveTo(0, y); g.lineTo(256, y); g.stroke(); }   // juntas de forma
    const t = new T3.CanvasTexture(c); t.wrapS = t.wrapT = T3.RepeatWrapping; return t;
  }
  const texC = texturaConcreto();
  const mMuro = new T3.MeshStandardMaterial({ color: 0x8A919C, map: texC, metalness: 0.0, roughness: 0.92, envMapIntensity: 0.25 });
  const mTopo = mat(0x7E8794, 0.0, 0.85, 0.2);
  const mChao = mat(0x0B1020, 0.0, 0.6, 0.22);
  const BASE = new Map([[mAco, 0x7A8696], [mJunta, 0xB8C4DA], [mMuro, 0x8A919C], [mTopo, 0x7E8794], [mChao, 0x0B1020]]);

  B.scene.fog = new T3.Fog(0x050816, 20, 40);
  window.aposCamera = D => { B.scene.fog.near = D + 2.5; B.scene.fog.far = D + 16; };

  const chao = new T3.Mesh(new T3.PlaneGeometry(120, 80), mChao); B.scene.add(chao);
  if (TL.sem_chao) chao.visible = false;

  // ── geometria do manequim ────────────────────────────────────────────────────────────────────────────────
  function lathe(perfil, seg = 28) {                    // perfil [[r, y], ...] de baixo para cima → eixo z (y vira z)
    const g = new T3.LatheGeometry(perfil.map(p => new T3.Vector2(Math.max(p[0], 1e-4), p[1])), seg);
    g.rotateX(PI / 2); g.computeVertexNormals(); return g;
  }
  function capsula(rA, rB, len, cap = 0.75) {           // começa na junta (z = 0) e desce até z = −len
    const p = [];
    for (let i = 0; i <= 6; i++) { const a = -PI / 2 + (PI / 2) * i / 6; p.push([rB * Math.cos(a), -len + cap * rB * Math.sin(a)]); }
    for (let i = 0; i <= 6; i++) { const a = (PI / 2) * i / 6; p.push([rA * Math.cos(a), cap * rA * Math.sin(a)]); }
    return lathe(p);
  }
  function barril(perfil, profundidade) { const g = lathe(perfil); g.scale(profundidade, 1, 1); return g; }
  const esfera = r => new T3.SphereGeometry(r, 24, 16);
  const malha = (g, m, x = 0, y = 0, z = 0) => { const o = new T3.Mesh(g, m); o.position.set(x, y, z); return o; };

  function Manequim() {
    const raiz = new T3.Group();
    const pelve = malha(barril([[0.001, -0.07], [0.115, -0.05], [0.15, 0.02], [0.14, 0.09], [0.11, 0.13], [0.001, 0.135]], 0.62), mAco);
    raiz.add(pelve);
    const pernas = [];
    for (const lado of [1, -1]) {
      const quadril = new T3.Group(); quadril.position.set(0, lado * HIPW, 0); raiz.add(quadril);
      quadril.add(malha(esfera(0.07), mJunta));
      quadril.add(malha(capsula(0.075, 0.052, L1), mAco));
      const joelho = new T3.Group(); joelho.position.z = -L1; quadril.add(joelho);
      joelho.add(malha(esfera(0.052), mJunta));
      joelho.add(malha(capsula(0.052, 0.036, L2), mAco));
      const tornozelo = new T3.Group(); tornozelo.position.z = -L2; joelho.add(tornozelo);
      tornozelo.add(malha(esfera(0.037), mJunta));
      const gp = capsula(0.042, 0.036, 0.19, 0.9); gp.rotateY(-PI / 2); gp.scale(1, 1.15, 0.85); gp.translate(-0.045, 0, -0.05);
      tornozelo.add(malha(gp, mAco));
      pernas.push({ quadril, joelho, tornozelo, lado });
    }
    const lombar = new T3.Group(); lombar.position.z = 0.1; raiz.add(lombar);
    lombar.add(malha(esfera(0.07), mJunta));
    const torax = malha(barril([[0.001, 0.02], [0.12, 0.05], [0.15, 0.16], [0.175, 0.28], [0.16, 0.34], [0.09, 0.375], [0.001, 0.38]], 0.6), mAco);
    lombar.add(torax);
    const cabeca = new T3.Group(); cabeca.position.z = 0.385; lombar.add(cabeca);
    cabeca.add(malha(new T3.CylinderGeometry(0.035, 0.042, 0.1, 16).rotateX(PI / 2), mAco, 0, 0, 0.045));
    cabeca.add(malha(esfera(0.034), mJunta, 0, 0, 0.0));
    const cr = malha(esfera(0.1), mAco, 0.012, 0, 0.165); cr.scale.set(1.0, 0.8, 1.15); cabeca.add(cr);
    const bracos = [];
    for (const lado of [1, -1]) {
      const ombro = new T3.Group(); ombro.position.set(0, lado * 0.19, 0.33); lombar.add(ombro);
      ombro.add(malha(esfera(0.055), mJunta));
      ombro.add(malha(capsula(0.047, 0.036, 0.29), mAco));
      const cotovelo = new T3.Group(); cotovelo.position.z = -0.29; ombro.add(cotovelo);
      cotovelo.add(malha(esfera(0.037), mJunta));
      cotovelo.add(malha(capsula(0.036, 0.028, 0.25), mAco));
      const punho = new T3.Group(); punho.position.z = -0.25; cotovelo.add(punho);
      punho.add(malha(esfera(0.026), mJunta));
      const mao = malha(esfera(0.05), mAco, 0.0, 0, -0.06); mao.scale.set(0.55, 0.38, 1.0); punho.add(mao);
      bracos.push({ ombro, cotovelo, lado });
    }
    return { raiz, pernas, lombar, cabeca, bracos };
  }

  // ── sombra de contato (disco com gradiente) ──────────────────────────────────────────────────────────────
  const texSombra = (() => {
    const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d');
    const r = g.createRadialGradient(64, 64, 0, 64, 64, 64);
    r.addColorStop(0, 'rgba(0,0,0,0.85)'); r.addColorStop(0.45, 'rgba(0,0,0,0.45)'); r.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = r; g.fillRect(0, 0, 128, 128); return new T3.CanvasTexture(c);
  })();

  // ── atores: muro + manequim + sombra, cada um num grupo deslocado em x ───────────────────────────────────
  const atores = TL.atores.map(a => {
    const g = new T3.Group(); g.position.x = a.x; if (a.espelho) g.scale.x = -1; B.scene.add(g);   // espelho: x local → a.x − x
    const muro = malha(new T3.BoxGeometry(0.7, 5.0, H_MURO), mMuro, -0.35, 1.9, H_MURO / 2); g.add(muro);
    const topo = malha(new T3.BoxGeometry(0.76, 5.06, 0.06), mTopo, -0.35, 1.9, H_MURO + 0.03); g.add(topo);
    if (a.sem_muro) muro.visible = topo.visible = false;
    const m = Manequim(); g.add(m.raiz);
    const sombra = new T3.Mesh(new T3.PlaneGeometry(1, 1), new T3.MeshBasicMaterial({ map: texSombra, transparent: true, depthWrite: false }));
    sombra.position.z = 0.003; g.add(sombra);
    const sombraTopo = sombra.clone(); sombraTopo.material = sombra.material.clone(); sombraTopo.position.z = H_MURO + 0.064; g.add(sombraTopo);
    return { def: a, g, m, sombra, sombraTopo };
  });

  // ── pose em função do tempo físico τ e do modo ──────────────────────────────────────────────────────────
  function ik(hx, hz, ax, az) {
    let dx = ax - hx, dz = az - hz, d = Math.min(Math.hypot(dx, dz), 0.9995 * (L1 + L2));
    const fi = Math.atan2(dx, -dz), al = Math.acos(clamp((L1 * L1 + d * d - L2 * L2) / (2 * L1 * d), -1, 1));
    const tt = fi + al, kx = hx + L1 * Math.sin(tt), kz = hz - L1 * Math.cos(tt);
    return [tt, Math.atan2(ax - kx, -(az - kz))];
  }
  const alturaReta = dobra => 2 * L1 * Math.cos(dobra / 2) + ANK;     // altura do quadril sobre a sola, joelho com flexão `dobra`

  function pose(tau, modo, tg) {
    // p: quadril (hx, hz); tornozelos (ax ± dxp, az); tronco λ; braços (abd, flex, cot); pé φ; cabeça
    const p = { hx: XA0, hz: H_MURO + alturaReta(0.04), ax: XA0, az: H_MURO + ANK, tes: 0, lam: 0.04, abd: 0.12, flex: 0.04, cot: 0.18, fi: 0, cab: 0.05, sole: H_MURO };
    const tc = T_PREP + T_QUEDA;
    if (tau < T_PREP) {                                              // de pé na borda; respiração e impulso curto
      const r = 0.006 * Math.sin(2 * PI * tau / 3.2);
      p.hz += r;
      const u = clamp((tau - (T_PREP - 0.5)) / 0.5, 0, 1), b = Math.sin(PI * u);
      p.hz -= 0.09 * b; p.lam += 0.16 * b; p.hx += 0.05 * u * u;
      p.flex = 0.04 - 0.55 * b + 0.3 * u * u; p.abd = 0.12 + 0.35 * u * u;
    } else if (tau < tc) {                                           // queda livre
      const s = tau - T_PREP, u = s / T_QUEDA;
      p.ax = XA0 + VX * s; p.sole = H_MURO - 0.5 * G_ * s * s; p.az = p.sole + ANK;
      const dobra = 0.1 + 0.08 * Math.sin(PI * u);
      p.hx = p.ax + 0.05 - 0.04 * u; p.hz = p.sole + alturaReta(dobra);
      p.tes = 0.07 * Math.sin(PI * u);
      p.lam = 0.2 - 0.08 * sv(u / 0.6);
      p.abd = lerp(0.47, 0.95, sv(s / 0.35)); p.flex = lerp(0.34, 0.3, u); p.cot = lerp(0.18, 0.4, sv(s / 0.35));
      p.fi = 0.35 * sv(s / 0.25) * (1 - sv((u - 0.55) / 0.45));
      p.cab = 0.12;
    } else {                                                         // contato
      const c = tau - tc;
      p.ax = X_POUSO; p.sole = 0; p.az = ANK; p.tes = 0;
      const amort = (k, tauD, f) => Math.exp(-c / tauD) * Math.sin(2 * PI * f * c) * k;
      if (modo === 'd') {                                            // pernas duras: para em 0,01 s, tremor curto
        const comp = 0.012 * clamp(c / 0.01, 0, 1);
        p.hz = alturaReta(0.04) - comp + amort(0.016, 0.08, 12);
        p.hx = X_POUSO + 0.035 + amort(0.012, 0.1, 6);
        p.lam = 0.12 + amort(0.08, 0.1, 7);
        p.abd = 0.15 + 0.8 * Math.exp(-c / 0.13) * Math.cos(2 * PI * 2.2 * c);
        p.flex = 0.1 + 0.2 * Math.exp(-c / 0.15); p.cot = 0.25;
        p.cab = 0.12 + amort(0.22, 0.09, 9);
        const sw = clamp((c - 0.8) / 0.8, 0, 1) * Math.sin(2 * PI * (tg || 0) / 2.6);   // v5: balanço leve de peso depois do pouso
        p.hx += 0.045 * sw; p.lam += 0.04 * sw; p.cab += 0.06 * sw; p.abd += 0.08 * sw;
      } else {                                                       // joelhos: quadril desce 0,5 m em 1/7 s
        const cc = Math.min(c, T_AGACHA), s = V_CH * cc - 0.5 * A_AGACHA * cc * cc, u = s / D_AGACHA;
        const assenta = c > T_AGACHA ? amort(0.008, 0.12, 4) : 0;
        p.hz = alturaReta(0.1) - s + assenta;
        p.hx = X_POUSO + 0.035 - 0.27 * u;
        p.lam = 0.12 + 0.56 * u;
        p.abd = lerp(0.95, 0.16, sv(c / 0.22)); p.flex = lerp(0.3, 1.15, sv(c / 0.22)); p.cot = lerp(0.4, 0.55, sv(c / 0.22));
        p.cab = 0.12 - 0.3 * u;
        const sw = clamp((c - T_AGACHA - 0.8) / 0.8, 0, 1) * Math.sin(2 * PI * (tg || 0) / 2.6);
        p.hx += 0.03 * sw; p.lam += 0.03 * sw; p.cab += 0.04 * sw;
      }
    }
    return p;
  }
  window.poseManequim = pose;

  function aplica(m, p) {
    m.raiz.position.set(p.hx, 0, p.hz);
    for (const pe of m.pernas) {
      const dxp = pe.lado * p.tes;
      const [tt, ts] = ik(p.hx, p.hz, p.ax + dxp, p.az);
      pe.quadril.rotation.y = -tt;
      pe.joelho.rotation.y = -(ts - tt);
      pe.tornozelo.rotation.y = p.fi + ts;
    }
    m.lombar.rotation.y = p.lam;
    m.cabeca.rotation.y = p.cab;
    for (const b of m.bracos) {
      b.ombro.rotation.set(b.lado * p.abd, -p.flex, 0);
      b.cotovelo.rotation.y = -p.cot;
    }
  }

  window.pontos3d = function () {                                    // pontos com rótulo do Manim (cota, pouso, centro do muro)
    const r = {}, w = (a, p) => { a.g.updateMatrixWorld(true); return a.g.localToWorld(new T3.Vector3(...p)).toArray(); };
    for (const a of atores) {
      const id = a.def.id;
      r[id + '_base'] = w(a, [-0.7, -0.6, 0]); r[id + '_topo'] = w(a, [-0.7, -0.6, H_MURO]);
      r[id + '_base_d'] = w(a, [0, -0.6, 0]); r[id + '_topo_d'] = w(a, [0, -0.6, H_MURO]);
      r[id + '_pouso'] = w(a, [X_POUSO, 0, 0]); r[id + '_meio'] = w(a, [0.35, -0.6, 0]);
    }
    return r;
  };
  window.constantes = { V_CH, T_QUEDA, T_AGACHA, A_AGACHA, X_POUSO, T_PREP };

  window.setFrame = function (f) {
    B.desenha(f, t => {
      const re = TL.realce_3d ? B.chaves(TL.realce_3d, t, 'v') : 0;
      for (const [m, c] of BASE) m.color.set(c).multiplyScalar(1 - 0.55 * re);
      for (const a of atores) {
        const tau = a.def.tau[Math.min(f, a.def.tau.length - 1)];
        a.g.visible = tau >= 0;
        if (tau < 0) continue;
        const p = pose(tau, a.def.modo[Math.min(f, a.def.modo.length - 1)], t);
        aplica(a.m, p);
        const h = p.sole;                                            // sombra: no chão durante a queda, no topo antes dela
        const noTopo = p.sole >= H_MURO - 1e-6 && p.ax < 0.05;
        a.sombraTopo.visible = noTopo; a.sombra.visible = !noTopo;
        const sObj = noTopo ? a.sombraTopo : a.sombra, alt = noTopo ? 0 : h;
        sObj.position.x = p.hx - 0.02; sObj.scale.set(0.75 + 0.25 * alt, 0.62 + 0.2 * alt, 1);
        sObj.material.opacity = (0.75 * (1 - re * 0.5)) / (1 + 0.9 * alt);
      }
    });
    return true;
  };
  window.projeta = B.projeta;
  window.cenaPronta = true;
})();
