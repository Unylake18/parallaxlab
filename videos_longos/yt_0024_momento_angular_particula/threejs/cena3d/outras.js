// yt_0024 v2 — cenas 'painel_queda' (B3-4/B3-5), 'orbita' (B5) e 'nuvem' (S2), no mesmo laboratório (base3d.js). window.CENA escolhe.
// painel_queda: painel vertical de compósito no plano x–z (y = 0), grade cartesiana de 10 cm, pino de aço em O = (0,0,0), trilho vertical
//   em x = 0,40 m, eletroímã em cima (LED apaga na soltura), esfera de aço (r 4 cm) com anel rosa; estado: esfera [x,z], estrobo [[x,z]...], ima 0..1.
// orbita: estrela no foco (origem) com bloom, plano orbital de vidro escuro com grade polar, órbita elíptica (a, e) e planeta de aço com anel rosa;
//   estado: planeta [x,y], a, ex, orbOp 0..1.
// nuvem: disco de ~400 partículas rosa girando em torno de z; estado: ang (rad), acesas [i...] (índices que acendem), op 0..1.
(function () {
  const { T3, PI, W, H, cl, lin, scene, fis, canvas, normalDe } = B3;
  const brilho = B3.brilho, CENA = window.CENA;
  B3.ambiente({ caixa: 17, int: 0.19 });
  const mPolido = fis('#8A96A6', 0.95, 0.18, 0.5);
  const mAco = fis('#3A414D', 0.9, 0.28, 0.4);
  const rosa = (r, t, z) => { const m = new T3.Mesh(new T3.TorusGeometry(r, t, 12, 96), new T3.MeshBasicMaterial({ color: lin('#FF7EB6').multiplyScalar(1.25) })); brilho.push(m); return m; };
  let atualiza = () => ({});

  if (CENA === 'painel_queda') {
    // painel 1,40 (x: −0,30..1,10) × 2,40 (z: −2,10..0,30), espessura 4 cm, atrás do plano y = 0
    const X0 = -0.30, X1 = 1.10, Z0 = -2.10, Z1 = 0.30, TX = 1024, TZ = Math.round(1024 * (Z1 - Z0) / (X1 - X0));
    const px = x => (x - X0) / (X1 - X0) * TX, pz = z => (Z1 - z) / (Z1 - Z0) * TZ, m = v => v / (X1 - X0) * TX;
    const gr = (g, cor, larg, forte) => { for (let k = Math.ceil(X0 * 10); k <= X1 * 10; k++) { g.strokeStyle = k % 5 ? cor : forte; g.lineWidth = larg; g.beginPath(); g.moveTo(px(k / 10), 0); g.lineTo(px(k / 10), TZ); g.stroke(); }
      for (let k = Math.ceil(Z0 * 10); k <= Z1 * 10; k++) { g.strokeStyle = k % 5 ? cor : forte; g.beginPath(); g.moveTo(0, pz(k / 10)); g.lineTo(TX, pz(k / 10)); g.stroke(); } };
    const GEO = lin('#B8C4DA'), c = k => `rgb(${Math.round(255 * GEO.r * k)},${Math.round(255 * GEO.g * k)},${Math.round(255 * GEO.b * k)})`;
    const cEm = canvas(TX, TZ, g => { g.fillStyle = '#000'; g.fillRect(0, 0, TX, TZ); gr(g, c(0.28), 1.6, c(0.55)); });
    const cAlt = canvas(TX, TZ, g => { g.fillStyle = '#fff'; g.fillRect(0, 0, TX, TZ); gr(g, '#666', 2, '#555'); });
    const tx = cv => { const t = new T3.CanvasTexture(cv); t.anisotropy = 8; return t; };
    const mPainel = fis('#0C111C', 0.35, 0.6, 0.15, { normalMap: tx(normalDe(cAlt, 2.5)), emissive: new T3.Color(1, 1, 1), emissiveMap: tx(cEm), emissiveIntensity: 0.2, envMapIntensity: 0.85 });
    const geo = new T3.BoxGeometry(X1 - X0, 0.04, Z1 - Z0);
    // UV da face da frente (−y) cobre o painel inteiro
    const painel = new T3.Mesh(geo, [fis('#7A8696', 0.92, 0.25, 0.2), fis('#7A8696', 0.92, 0.25, 0.2), mPainel, mPainel, fis('#7A8696', 0.92, 0.25, 0.2), fis('#7A8696', 0.92, 0.25, 0.2)]);
    painel.position.set((X0 + X1) / 2, 0.02 + 0.002, (Z0 + Z1) / 2); painel.receiveShadow = true; scene.add(painel);
    // faixa de LED da borda (sem bloom): ciano em cima → magenta embaixo
    const led = (x0, z0, x1, z1, ca, cb) => { const g = new T3.BufferGeometry(); const a = lin(ca).multiplyScalar(0.22), b = lin(cb).multiplyScalar(0.22);
      const dx = x1 - x0, dz = z1 - z0, L = Math.hypot(dx, dz), nx = -dz / L * 0.004, nz = dx / L * 0.004;
      g.setAttribute('position', new T3.Float32BufferAttribute([x0 - nx, -0.001, z0 - nz, x0 + nx, -0.001, z0 + nz, x1 - nx, -0.001, z1 - nz, x1 + nx, -0.001, z1 + nz], 3));
      g.setAttribute('color', new T3.Float32BufferAttribute([a.r, a.g, a.b, a.r, a.g, a.b, b.r, b.g, b.b, b.r, b.g, b.b], 3)); g.setIndex([0, 2, 1, 1, 2, 3]);
      scene.add(new T3.Mesh(g, new T3.MeshBasicMaterial({ vertexColors: true, side: T3.DoubleSide }))); };
    led(X0 + 0.02, Z1 - 0.02, X0 + 0.02, Z0 + 0.02, '#35D9FF', '#EA63FF'); led(X1 - 0.02, Z1 - 0.02, X1 - 0.02, Z0 + 0.02, '#35D9FF', '#EA63FF');
    // pino O
    const pino = new T3.Group();
    const h = new T3.Mesh(new T3.CylinderGeometry(0.008, 0.008, 0.05, 20), mPolido); h.position.y = -0.025;
    const b = new T3.Mesh(new T3.SphereGeometry(0.018, 32, 16), mPolido); b.position.y = -0.05;
    const anelO = new T3.Mesh(new T3.TorusGeometry(0.026, 0.0022, 12, 64), new T3.MeshBasicMaterial({ color: lin('#BFE6FF').multiplyScalar(1.5) })); anelO.rotation.x = PI / 2; anelO.position.y = -0.003; brilho.push(anelO);
    pino.add(h, b, anelO); scene.add(pino);
    // trilho vertical em x = 0,40 (duas barras finas) e eletroímã em cima
    for (const dx of [-0.055, 0.055]) { const t = new T3.Mesh(new T3.BoxGeometry(0.010, 0.012, Z1 - 0.06 - (Z0 + 0.04)), mPolido); t.position.set(0.40 + dx, -0.008, (Z1 - 0.06 + Z0 + 0.04) / 2); scene.add(t); }
    const ima = new T3.Mesh(new T3.BoxGeometry(0.14, 0.07, 0.06), mAco); ima.position.set(0.40, -0.04, 0.12); ima.castShadow = true; scene.add(ima);
    const mLed = new T3.MeshBasicMaterial({ color: lin('#35D9FF').multiplyScalar(1.4) });
    const ledIma = new T3.Mesh(new T3.BoxGeometry(0.08, 0.004, 0.008), mLed); ledIma.position.set(0.40, -0.077, 0.12); scene.add(ledIma); brilho.push(ledIma);
    // esfera de aço com anel rosa
    const R = 0.055, esf = new T3.Group();
    const corpo = new T3.Mesh(new T3.SphereGeometry(R, 64, 32), fis('#2E3440', 0.95, 0.22, 0.5)); corpo.castShadow = true;
    const anel = rosa(R * 1.01, 0.0035); anel.rotation.x = PI / 2;
    esf.add(corpo, anel); scene.add(esf);
    // estroboscópio: cópias translúcidas
    const fantasmas = []; for (let i = 0; i < 8; i++) { const m = new T3.Mesh(new T3.SphereGeometry(R, 32, 16), new T3.MeshBasicMaterial({ color: lin('#FF7EB6'), transparent: true, opacity: 0.14, depthWrite: false })); scene.add(m); fantasmas.push(m); }
    B3.sol.position.set(-1.0, -2.5, 1.5);
    atualiza = e => {
      const p = e.esfera || [0.40, 0.0];
      esf.position.set(p[0], -0.06, p[1]); esf.rotation.y = -p[1] * 6;
      fantasmas.forEach((m, i) => { const q = (e.estrobo || [])[i]; m.visible = !!q; if (q) m.position.set(q[0], -0.06, q[1]); });
      mLed.color.copy(lin('#35D9FF').multiplyScalar(1.4 * (e.ima === undefined ? 1 : e.ima) + 0.02));
      return { esfera: B3.projeta([p[0], -0.06, p[1]]), pino: B3.projeta([0, 0, 0]) };
    };
  }

  if (CENA === 'orbita') {
    // plano orbital de vidro escuro (disco de raio 5,2 u) com grade polar; estrela no foco; órbita elíptica; planeta
    const RP = 3.6, PC = -1.56, TX = 2048;                // plano centrado na elipse do B5-5; a grade polar fica centrada na estrela (O)
    const cEm = canvas(TX, TX, g => { g.fillStyle = '#000'; g.fillRect(0, 0, TX, TX); const s = TX / (2 * RP), c0 = TX / 2;
      const c = c0 - PC * s, cy = c0;
      g.strokeStyle = 'rgb(60,68,84)'; g.lineWidth = 2;
      for (let k = 1; k <= 12; k++) { g.beginPath(); g.arc(c, cy, k * 0.5 * s, 0, 2 * PI); g.stroke(); }
      for (let k = 0; k < 24; k++) { const a = k * PI / 12; g.beginPath(); g.moveTo(c + 0.3 * s * Math.cos(a), cy + 0.3 * s * Math.sin(a)); g.lineTo(c + 2 * RP * s * Math.cos(a), cy + 2 * RP * s * Math.sin(a)); g.stroke(); }
      const rg = g.createRadialGradient(c0, c0, 0.7 * c0, c0, c0, c0); rg.addColorStop(0, 'rgba(0,0,0,0)'); rg.addColorStop(1, 'rgba(0,0,0,1)'); g.fillStyle = rg; g.fillRect(0, 0, TX, TX); });
    const cAl = canvas(512, 512, g => { const rg = g.createRadialGradient(256, 256, 150, 256, 256, 256); rg.addColorStop(0, 'rgba(255,255,255,1)'); rg.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = rg; g.fillRect(0, 0, 512, 512); });
    const plano = new T3.Mesh(new T3.CircleGeometry(RP, 128), new T3.MeshPhysicalMaterial({ color: lin('#0E1626'), metalness: 0.2, roughness: 0.15, clearcoat: 1, clearcoatRoughness: 0.08,
      transparent: true, opacity: 0.78, alphaMap: new T3.CanvasTexture(cAl), emissive: new T3.Color(1, 1, 1), emissiveMap: new T3.CanvasTexture(cEm), emissiveIntensity: 0.55, envMapIntensity: 0.3, depthWrite: false }));
    plano.position.set(PC, 0, -0.002); plano.renderOrder = 1; scene.add(plano);
    // estrela: núcleo branco-quente e halo âmbar
    const est = new T3.Mesh(new T3.SphereGeometry(0.22, 48, 24), new T3.MeshBasicMaterial({ color: lin('#FFF1C9').multiplyScalar(2.2) })); scene.add(est); brilho.push(est);
    const halo = new T3.Mesh(new T3.SphereGeometry(0.34, 48, 24), new T3.MeshBasicMaterial({ color: lin('#FFC24D').multiplyScalar(0.9), transparent: true, opacity: 0.35, depthWrite: false })); scene.add(halo); brilho.push(halo);
    const luzE = new T3.PointLight(lin('#FFE3A8'), 2.5, 12, 1.2); scene.add(luzE);
    // órbita (linha fina) e planeta
    const NO = 400, gOrb = new T3.BufferGeometry(); gOrb.setAttribute('position', new T3.BufferAttribute(new Float32Array(NO * 3), 3));
    const orb = new T3.LineLoop(gOrb, new T3.LineBasicMaterial({ color: lin('#9FB4D6').multiplyScalar(0.8), transparent: true, opacity: 0.8 })); scene.add(orb);
    const pl = new T3.Group();
    const corpo = new T3.Mesh(new T3.SphereGeometry(0.15, 48, 24), fis('#3A414D', 0.9, 0.3, 0.4)); const anel = rosa(0.155, 0.016);
    pl.add(corpo, anel); scene.add(pl);
    atualiza = e => {
      const a = e.a || 2.6, ex = e.ex === undefined ? 0.6 : e.ex, b = a * Math.sqrt(1 - ex * ex), P = gOrb.attributes.position.array;
      for (let i = 0; i < NO; i++) { const t = 2 * PI * i / NO; P[3 * i] = a * Math.cos(t) - a * ex; P[3 * i + 1] = b * Math.sin(t); P[3 * i + 2] = 0.001; }
      gOrb.attributes.position.needsUpdate = true; orb.material.opacity = 0.8 * (e.orbOp === undefined ? 1 : e.orbOp); orb.visible = orb.material.opacity > 0.01;
      plano.material.opacity = 0.78 * (e.planoOp === undefined ? 1 : e.planoOp);
      const p = e.planeta || [a - a * ex, 0]; pl.position.set(p[0], p[1], 0.15); pl.visible = e.planeta !== null;
      return { est: B3.projeta([0, 0, 0]), planeta: B3.projeta([p[0], p[1], 0]) };
    };
  }

  if (CENA === 'nuvem') {
    const N = 400; let sd = 11; const rnd = () => { sd = (sd * 16807) % 2147483647; return sd / 2147483647; };
    const pts = []; for (let i = 0; i < N; i++) { const r = 0.25 + 1.75 * Math.sqrt(rnd()), f = 2 * PI * rnd(), z = (rnd() - 0.5) * 0.35 * (1 - r / 2.2); pts.push([r, f, z]); }
    window.NUVEM = pts;
    const geo = new T3.SphereGeometry(0.030, 12, 8);
    const inst = new T3.InstancedMesh(geo, new T3.MeshBasicMaterial({ color: lin('#FF7EB6').multiplyScalar(0.9) }), N); scene.add(inst); brilho.push(inst);
    const acesa = new T3.InstancedMesh(new T3.SphereGeometry(0.075, 24, 12), new T3.MeshBasicMaterial({ color: lin('#FFC9E0').multiplyScalar(2.0) }), 6); scene.add(acesa); brilho.push(acesa);
    const eixo = new T3.Mesh(new T3.CylinderGeometry(0.012, 0.012, 3.6, 16), new T3.MeshBasicMaterial({ color: lin('#B8C4DA').multiplyScalar(0.6) })); eixo.rotation.x = PI / 2; scene.add(eixo);
    const M4 = new T3.Matrix4();
    atualiza = e => {
      const a = e.ang || 0, ac = e.acesas || [], out = {};
      pts.forEach(([r, f, z], i) => { M4.makeTranslation(r * Math.cos(f + a), r * Math.sin(f + a), z); inst.setMatrixAt(i, M4); });
      inst.instanceMatrix.needsUpdate = true;
      acesa.count = ac.length;
      ac.forEach((i, k) => { const [r, f, z] = pts[i]; const p = [r * Math.cos(f + a), r * Math.sin(f + a), z]; M4.makeTranslation(...p); acesa.setMatrixAt(k, M4); out['p' + k] = B3.projeta(p); });
      acesa.instanceMatrix.needsUpdate = true;
      out.O = B3.projeta([0, 0, 0]);
      return out;
    };
  }

  window.setEstado = function (e) {
    B3.posicionaCamera(e.cam);
    const p = atualiza(e);
    B3.render(e, {});
    p.webgl2 = B3.gl2;
    (e.pontos || []).forEach((q, k) => { p['q' + k] = B3.projeta(q); });
    return p;
  };
  window.projeta = B3.projeta;
  window.medidas = () => ({ webgl2: B3.gl2, W, H });
  window.cenaPronta = true;
})();
