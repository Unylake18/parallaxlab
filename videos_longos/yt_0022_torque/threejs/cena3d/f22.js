// yt_0022: cenas 3D por estado (Three.js r128, base b3d.js). Cena escolhida por window.CENA_ID (no .html).
//   'regua' — H1–H3, T4-1, S2, EN2: borda de bancada de aço, dobradiça horizontal em (0, 0, 0), régua metálica L = 1,0 m
//     com marcações de 10 em 10 cm, duas moedas de aço (meio e ponta) e bloco opcional de massa M na ponta (EN2).
//   'porta' — T1-1, T1-2, T2-1, T2-2: porta de aço do laboratório com dobradiça vertical na esquerda (x = 0, y = 0) e maçaneta a 0,75 m.
// O que é número, rótulo, seta, cota, paralelogramo e sinal é do Manim (projeta3d, a mesma câmera do b3d.js).
(function () {
  const B = B3D, T3 = THREE, PI = Math.PI, id = window.CENA_ID;
  const v3 = (x, y, z) => new T3.Vector3(x, y, z);
  const cl = (x, a, b) => Math.min(b, Math.max(a, x));

  // ── luz B (padrão do laboratório): ambiente azul-noite com recorte BLUE_L (~35%) e toque magenta (~12%) ──
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
  B.luz.rim.intensity = 0.22;
  const recA = new T3.DirectionalLight(0x7FB2FF, 1.0), recB = new T3.DirectionalLight(0xEA63FF, 0.32);
  recA.position.set(-6, 9, 6); recB.position.set(6, 9, 4); B.scene.add(recA, recB);
  B.ceu(false);

  let atualiza = () => {}, pontos = () => ({});

  if (id === 'regua') {
    // ── Bancada em x <= 0, dobradiça em (0, 0, 0) com eixo em y, régua L = 1,0 m em x >= 0 que cai no plano xz por th >= 0 ──
    const L = 1.0, W_R = 0.052, H_R = 0.015; // espessura visual 1,5 cm e largura 5,2 cm para leitura nítida a 960x540; física exata de barra delgada L = 1,0 m
    const R_M = 0.025, H_M = 0.010;          // moedas com diâmetro visual 5,0 cm e espessura 10 mm para leitura limpa a 960x540
    const matMesa = new T3.MeshStandardMaterial({ color: 0x3A4354, metalness: 0.45, roughness: 0.55, envMapIntensity: 0.45, transparent: true, opacity: 1 });
    const matBorda = new T3.MeshStandardMaterial({ color: 0x7A8696, metalness: 0.7, roughness: 0.35, envMapIntensity: 0.65, transparent: true, opacity: 1 });
    const matDob = new T3.MeshStandardMaterial({ color: 0x8E9BAE, metalness: 0.82, roughness: 0.28, envMapIntensity: 0.8, transparent: true, opacity: 1 });
    const matRegua = new T3.MeshStandardMaterial({ color: 0xA8B8D0, metalness: 0.68, roughness: 0.30, envMapIntensity: 0.82, transparent: true, opacity: 1 });
    const matRisco = new T3.MeshBasicMaterial({ color: 0x1E2636, transparent: true, opacity: 0.9 });
    const matRiscoCM = new T3.MeshBasicMaterial({ color: 0xFF7EB6, transparent: true, opacity: 0.95 });
    const matMoeda = new T3.MeshStandardMaterial({ color: 0xEAF0FA, metalness: 0.75, roughness: 0.20, envMapIntensity: 1.0, emissive: new T3.Color(0x9CB4E8), emissiveIntensity: 0.22, transparent: true, opacity: 1 });
    const matBloco = new T3.MeshStandardMaterial({ color: 0xD96B9E, metalness: 0.55, roughness: 0.38, envMapIntensity: 0.65, emissive: new T3.Color(0xFF7EB6), emissiveIntensity: 0.18, transparent: true, opacity: 1 });

    const raiz = new T3.Group(); B.scene.add(raiz);

    // Bancada na esquerda (x de -0.52 a -0.012, topo em z = 0)
    const gMesa = new T3.Group();
    const tampo = new T3.Mesh(new T3.BoxGeometry(0.50, 0.28, 0.055), matMesa);
    tampo.position.set(-0.262, 0, -0.0275);
    const friso = new T3.Mesh(new T3.BoxGeometry(0.504, 0.284, 0.008), matBorda);
    friso.position.set(-0.262, 0, -0.004);
    const colMesa = new T3.Mesh(new T3.BoxGeometry(0.18, 0.20, 0.32), matMesa);
    colMesa.position.set(-0.36, 0, -0.21);
    gMesa.add(tampo, friso, colMesa);
    raiz.add(gMesa);

    // Dobradiça cilindrica em (0, 0, 0) com eixo ao longo de y
    const pinoDob = new T3.Mesh(new T3.CylinderGeometry(0.014, 0.014, 0.072, 32), matDob);
    pinoDob.position.set(0, 0, 0);
    const anel1 = new T3.Mesh(new T3.CylinderGeometry(0.019, 0.019, 0.016, 32), matBorda);
    anel1.position.set(0, -0.024, 0);
    const anel2 = new T3.Mesh(new T3.CylinderGeometry(0.019, 0.019, 0.016, 32), matBorda);
    anel2.position.set(0, 0.024, 0);
    raiz.add(pinoDob, anel1, anel2);

    // Grupo da régua que gira por th no sentido horário do plano xz (rotation.y = th faz +x cair para -z)
    const gRegua = new T3.Group();
    const corpoRegua = new T3.Mesh(new T3.BoxGeometry(L, W_R, H_R), matRegua);
    corpoRegua.position.set(L / 2, 0, -H_R / 2); // face superior da régua exatamente em z local = 0!
    gRegua.add(corpoRegua);

    // Marcações de 10 em 10 cm na face superior (z local = 0.0006) e na face frontal (y local = -W_R/2 - 0.0006)
    for (let k = 1; k <= 9; k++) {
      const x = k * 0.10, isCM = k === 5;
      const m = isCM ? matRiscoCM : matRisco;
      const w = isCM ? 0.006 : 0.0035, comp = isCM ? W_R * 0.85 : W_R * 0.55;
      const tTop = new T3.Mesh(new T3.BoxGeometry(w, comp, 0.0012), m);
      tTop.position.set(x, 0, 0.0006);
      const tFr = new T3.Mesh(new T3.BoxGeometry(w, 0.0012, isCM ? H_R * 0.9 : H_R * 0.6), m);
      tFr.position.set(x, -W_R / 2 - 0.0005, -H_R / 2);
      gRegua.add(tTop, tFr);
    }
    raiz.add(gRegua);

    // Bloco extra na ponta (EN2): massa concentrada M presa no fim da régua
    const H_BLOCO = 0.042, W_BLOCO = 0.056;
    const blocoPonta = new T3.Mesh(new T3.BoxGeometry(W_BLOCO, W_R * 1.08, H_BLOCO), matBloco);
    blocoPonta.position.set(L - W_BLOCO / 2, 0, H_BLOCO / 2);
    blocoPonta.visible = false;
    gRegua.add(blocoPonta);

    // Duas moedas (cilindros com eixo normal à face superior quando apoiadas)
    const mMeio = new T3.Mesh(new T3.CylinderGeometry(R_M, R_M, H_M, 40), matMoeda);
    mMeio.rotation.x = PI / 2;
    const mPonta = new T3.Mesh(new T3.CylinderGeometry(R_M, R_M, H_M, 40), matMoeda);
    mPonta.rotation.x = PI / 2;
    raiz.add(mMeio, mPonta);

    atualiza = e => {
      const th = e.th || 0, op = e.op == null ? 1 : e.op;
      const c = Math.cos(th), s = Math.sin(th);
      // Em Three.js, rotation.y = +th leva (x, 0, z) -> (x cos th + z sin th, 0, -x sin th + z cos th)
      gRegua.rotation.set(0, th, 0);
      const temBloco = !!e.massa_ponta;
      blocoPonta.visible = temBloco;

      // Moeda 1 (meio): coordenadas mundo (x1, 0, z1) da base da moeda, inclinação th1
      const r1 = e.r1 != null ? e.r1 : 0.50;
      const x1 = e.m1x != null ? e.m1x : r1 * c;
      const z1 = e.m1z != null ? e.m1z : -r1 * s;
      const th1 = e.m1th != null ? e.m1th : th;
      mMeio.visible = e.moedas !== false && op > 0.01;
      mMeio.position.set(x1 + (H_M / 2) * Math.sin(th1), 0, z1 + (H_M / 2) * Math.cos(th1));
      mMeio.rotation.set(PI / 2, th1, 0, 'YXZ');

      // Moeda 2 (ponta): em queda livre vertical a partir de x2 = 1.0 (ou sobre o bloco em EN2)
      const hBase2 = temBloco ? H_BLOCO : 0;
      const x2 = e.m2x != null ? e.m2x : (temBloco ? (L - W_BLOCO / 2) * c + hBase2 * s : L);
      const z2 = e.m2z != null ? e.m2z : (temBloco ? -(L - W_BLOCO / 2) * s + hBase2 * c : 0);
      const th2 = e.m2th != null ? e.m2th : 0;
      mPonta.visible = e.moedas !== false && op > 0.01;
      mPonta.position.set(x2 + (H_M / 2) * Math.sin(th2), 0, z2 + (H_M / 2) * Math.cos(th2));
      mPonta.rotation.set(PI / 2, th2, 0, 'YXZ');

      [matMesa, matBorda, matDob, matRegua, matMoeda, matBloco].forEach(m => {
        m.opacity = op; m.depthWrite = op > 0.95;
      });
      matRisco.opacity = 0.9 * op; matRiscoCM.opacity = 0.95 * op;
      raiz.visible = op > 0.01;
    };

    pontos = e => {
      const th = e.th || 0, c = Math.cos(th), s = Math.sin(th);
      const ptRegua = r => B.projeta([r * c, 0, -r * s]);
      const r1 = e.r1 != null ? e.r1 : 0.50;
      const x1 = e.m1x != null ? e.m1x : r1 * c;
      const z1 = e.m1z != null ? e.m1z : -r1 * s;
      const temBloco = !!e.massa_ponta;
      const hBase2 = temBloco ? H_BLOCO : 0;
      const x2 = e.m2x != null ? e.m2x : (temBloco ? (L - W_BLOCO / 2) * c + hBase2 * s : L);
      const z2 = e.m2z != null ? e.m2z : (temBloco ? -(L - W_BLOCO / 2) * s + hBase2 * c : 0);
      return {
        dobradica: B.projeta([0, 0, 0]),
        cm: ptRegua(0.50),
        dois_tercos: ptRegua(2 / 3),
        ponta: ptRegua(1.0),
        moeda_meio: B.projeta([x1, 0, z1]),
        moeda_ponta: B.projeta([x2, 0, z2]),
      };
    };
  }

  if (id === 'porta') {
    // ── Porta do laboratório: largura L = 0,80 m, altura H = 1,60 m (centrada em z = 0: z de -0,80 a +0,80), espessura 4,4 cm ──
    // Dobradiça vertical na esquerda em (x = 0, y = 0). Quando ang = 0, a folha vai ao longo de +x (de 0 a 0,80 m).
    const LP = 0.80, HP = 1.60, EP = 0.044;
    const matFolha = new T3.MeshStandardMaterial({ color: 0x7A889E, metalness: 0.65, roughness: 0.36, envMapIntensity: 0.7, transparent: true, opacity: 1 });
    const matMold = new T3.MeshStandardMaterial({ color: 0x566276, metalness: 0.55, roughness: 0.42, envMapIntensity: 0.55, transparent: true, opacity: 1 });
    const matDob = new T3.MeshStandardMaterial({ color: 0x9AA8BE, metalness: 0.85, roughness: 0.25, envMapIntensity: 0.85, transparent: true, opacity: 1 });
    const matMac = new T3.MeshStandardMaterial({ color: 0xDCE4F2, metalness: 0.88, roughness: 0.2, envMapIntensity: 0.9, transparent: true, opacity: 1 });
    const matPiso = new T3.MeshStandardMaterial({ color: 0x121A2E, metalness: 0.1, roughness: 0.75, envMapIntensity: 0.25, transparent: true, opacity: 0.85 });

    const raiz = new T3.Group(); B.scene.add(raiz);

    // Piso escuro sob a porta (z = -HP/2 - 0.02)
    const piso = new T3.Mesh(new T3.PlaneGeometry(2.6, 2.2), matPiso);
    piso.position.set(0.35, 0.15, -HP / 2 - 0.02);
    raiz.add(piso);

    // Batente / eixo vertical fixo em (0, 0, z)
    const hasteEixo = new T3.Mesh(new T3.CylinderGeometry(0.016, 0.016, HP + 0.16, 28), matMold);
    hasteEixo.rotation.x = PI / 2;
    raiz.add(hasteEixo);

    [-0.52, 0, 0.52].forEach(z => {
      const cil = new T3.Mesh(new T3.CylinderGeometry(0.026, 0.026, 0.09, 28), matDob);
      cil.rotation.x = PI / 2; cil.position.set(0, 0, z);
      raiz.add(cil);
    });

    // Folha da porta que gira em torno do eixo z por ang
    const gPorta = new T3.Group();
    const folha = new T3.Mesh(new T3.BoxGeometry(LP, EP, HP), matFolha);
    folha.position.set(LP / 2, 0, 0);
    gPorta.add(folha);

    // Painéis rebaixados decorativos para leitura 3D nítida tanto de topo quanto a 3/4
    const reb1 = new T3.Mesh(new T3.BoxGeometry(LP * 0.76, EP + 0.006, HP * 0.36), matMold);
    reb1.position.set(LP * 0.52, 0, HP * 0.24);
    const reb2 = new T3.Mesh(new T3.BoxGeometry(LP * 0.76, EP + 0.006, HP * 0.36), matMold);
    reb2.position.set(LP * 0.52, 0, -HP * 0.24);
    // Friso superior de aço claro (destaca a vista de topo)
    const topoFriso = new T3.Mesh(new T3.BoxGeometry(LP, EP * 0.92, 0.012), matDob);
    topoFriso.position.set(LP / 2, 0, HP / 2 + 0.004);
    gPorta.add(reb1, reb2, topoFriso);

    // Maçaneta a r = 0,75 m da dobradiça (visível nos dois lados e de cima)
    const rMac = 0.75;
    const pinoMac = new T3.Mesh(new T3.CylinderGeometry(0.014, 0.014, EP + 0.07, 24), matMac);
    pinoMac.position.set(rMac, 0, 0.04);
    const alcaFrente = new T3.Mesh(new T3.BoxGeometry(0.09, 0.018, 0.022), matMac);
    alcaFrente.position.set(rMac - 0.035, -EP / 2 - 0.032, 0.04);
    const alcaTras = new T3.Mesh(new T3.BoxGeometry(0.09, 0.018, 0.022), matMac);
    alcaTras.position.set(rMac - 0.035, EP / 2 + 0.032, 0.04);
    // Marcador no topo em r = 0,75 m e r = 0,15 m
    const pinoTopoMac = new T3.Mesh(new T3.CylinderGeometry(0.018, 0.018, 0.02, 24), matMac);
    pinoTopoMac.rotation.x = PI / 2; pinoTopoMac.position.set(rMac, 0, HP / 2 + 0.012);
    gPorta.add(pinoMac, alcaFrente, alcaTras, pinoTopoMac);

    raiz.add(gPorta);

    atualiza = e => {
      const ang = e.ang || 0, op = e.op == null ? 1 : e.op;
      gPorta.rotation.set(0, 0, ang);
      piso.visible = e.piso !== false && op > 0.01;
      [matFolha, matMold, matDob, matMac].forEach(m => { m.opacity = op; m.depthWrite = op > 0.95; });
      matPiso.opacity = 0.85 * op;
      raiz.visible = op > 0.01;
    };

    pontos = e => {
      const ang = e.ang || 0, c = Math.cos(ang), s = Math.sin(ang);
      const zRef = e.z_ref != null ? e.z_ref : 0; // plano de referência para setas (0 no 3/4 ou topo)
      const pt = (r, z) => B.projeta([r * c, r * s, z == null ? zRef : z]);
      return {
        dob_meio: B.projeta([0, 0, zRef]),
        dob_base: B.projeta([0, 0, -HP / 2]),
        dob_topo: B.projeta([0, 0, HP / 2]),
        perto: pt(0.15, zRef),
        meio: pt(0.40, zRef),
        macaneta: pt(0.75, zRef),
        borda: pt(LP, zRef),
      };
    };
  }

  window.CENA = { atualiza };
  window.pontos3d = e => pontos(e);
  window.cenaPronta = true;
})();
