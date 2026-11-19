// yt_0023 v2: carretel, volante, haste e pêndulo de discos por ESTADO (Three.js r128, base b3d.js).
// Eixo de rotação = eixo y (aponta para longe da câmera frontal); plano do giro = xz (z para cima).
// v2 §1.2: UM eixo de aço atravessando tudo, garfo de dois braços no plano x = 0 (um na frente, um atrás) com mancais,
// porca saliente na frente, todas as peças coaxiais filhas de um único `spin` com origem no eixo, fios tangentes.
// Valores, setas e rótulos ficam no Manim (presos pelo pontos3d / projeta3d do Python).
(function () {
  const B = B3D, T = THREE, PI = Math.PI, id = window.CENA_ID;
  const std = (color, met, rug, extra) => new T.MeshStandardMaterial(Object.assign({ color, metalness: met, roughness: rug, envMapIntensity: 0.22 }, extra || {}));
  const ACO = std(0x7A8696, 0.55, 0.45), ACO_CLARO = std(0x9AA7BA, 0.5, 0.4), ACO_ESC = std(0x3E4A5E, 0.5, 0.5), ACO_GARFO = std(0x3A4558, 0.55, 0.5);
  const ARESTA = new T.MeshBasicMaterial({ color: 0xDCE6F5 }), ARESTA_ESC = new T.MeshBasicMaterial({ color: 0x1A2233 });
  const ROSA = std(0x8A3163, 0.15, 0.55), FIO = std(0xFFF1DC, 0.0, 0.55, { emissive: new T.Color(0x000000) });
  const FANT = new T.MeshBasicMaterial({ color: 0xFF7EB6, transparent: true, opacity: 0.0, depthWrite: false });
  // luz B: chave branca de cima-frente, azul de baixo, magenta lateral fraca
  B.luz.chave.intensity = 0.95; B.luz.chave.position.set(-3, -7, 6); B.luz.rim.intensity = 0.4; B.luz.amb.intensity = 0.32;
  const azul = new T.DirectionalLight(0x7FB2FF, 0.55); azul.position.set(-4, -6, -5); B.scene.add(azul);
  const mag = new T.DirectionalLight(0xEA63FF, 0.25); mag.position.set(7, -2, 2); B.scene.add(mag);
  B.ceu(false);

  function cil(r, h, m, y0, seg) { const o = new T.Mesh(new T.CylinderGeometry(r, r, h, seg || 96), m); o.position.y = y0 || 0; return o; }
  function aro(r, w, m, y0) { const o = new T.Mesh(new T.TorusGeometry(r, w, 8, 128), m); o.rotation.x = PI / 2; o.position.y = y0 || 0; return o; }
  function caixa(w, h, d, m, x, y, z) { const o = new T.Mesh(new T.BoxGeometry(w, h, d), m); o.position.set(x || 0, y || 0, z || 0); return o; }
  function anel(ri, ro, h, m, y0) {
    const s = new T.Shape(); s.absarc(0, 0, ro, 0, 2 * PI, false); const f = new T.Path(); f.absarc(0, 0, ri, 0, 2 * PI, true); s.holes.push(f);
    const g = new T.ExtrudeGeometry(s, { depth: h, bevelEnabled: false, curveSegments: 128 }); g.translate(0, 0, -h / 2);
    const o = new T.Mesh(g, m); o.rotation.x = PI / 2; o.position.y = y0 || 0; return o;
  }
  function tubo(pts, r, m) { return new T.Mesh(new T.TubeGeometry(new T.CatmullRomCurve3(pts), Math.max(64, pts.length * 2), r, 8, false), m); }
  function arestas(o, cor) { o.add(new T.LineSegments(new T.EdgesGeometry(o.geometry, 25), new T.LineBasicMaterial({ color: cor || 0xDCE6F5 }))); return o; }
  // espiras do fio no tambor: hélice de raio rr entre y0 e y1; a última espira sai tangente em x = s*rr, z = 0
  function espiras(rr, y0, y1, voltas, s) {
    const p = [], n = 60 * voltas;
    for (let k = 0; k <= n; k++) { const u = k / n, a = s > 0 ? -2 * PI * voltas * (1 - u) : PI + 2 * PI * voltas * (1 - u);
      p.push(new T.Vector3(rr * Math.cos(a), y0 + (y1 - y0) * u, rr * Math.sin(a))); }
    return tubo(p, 0.008, FIO);
  }
  function bloco(lado, x, y, z) { return arestas(caixa(lado, lado * 0.8, lado, ROSA, x, y, z), 0xFF7EB6); }
  function fio(x, y) { const o = cil(0.008, 1, FIO, 0, 10); o.rotation.x = PI / 2; o.userData = { x, y }; return o; }
  function estica(o, z0, z1) { const h = Math.max(1e-3, z0 - z1); o.scale.set(1, h, 1); o.position.set(o.userData.x, o.userData.y, (z0 + z1) / 2); o.userData.topo = z0; }
  // eixo de aço de yA (frente) a yB (trás), porca sextavada saliente na frente, mancais nos braços, garfo no plano x = 0.
  // dir = +1: braços sobem até a viga superior em zTopo; dir = −1: descem até a base em zTopo (< 0).
  function garfo(pai, yF, yT, zTopo, dir) {
    const g = new T.Group(); pai.add(g);
    const eixo = cil(0.02, (yT + 0.02) - (yF - 0.045), ACO_CLARO, ((yT + 0.02) + (yF - 0.045)) / 2, 48); g.add(eixo);
    const porca = cil(0.036, 0.024, ACO_CLARO, yF - 0.04, 6); g.add(porca, aro(0.036, 0.0035, ARESTA, yF - 0.052));
    const capa = cil(0.022, 0.01, ARESTA, yF - 0.056, 32); g.add(capa);
    const mancais = [], est = [];
    for (const y of [yF, yT]) {
      const m = anel(0.021, 0.05, 0.022, ACO_GARFO, y); g.add(m, aro(0.05, 0.004, ARESTA, y + 0.012 * Math.sign(y - (yF + yT) / 2)));
      const z0 = dir > 0 ? 0.045 : -0.045, h = Math.abs(zTopo - z0);
      const br = arestas(caixa(0.044, 0.022, h, ACO_GARFO, 0, y, (zTopo + z0) / 2), 0x9FB0C8); g.add(br); est.push(br);
      mancais.push(m);
    }
    const viga = arestas(caixa(0.07, (yT - yF) + 0.06, 0.05, ACO_GARFO, 0, (yF + yT) / 2, zTopo + dir * 0.025), 0x9FB0C8); g.add(viga); est.push(viga);
    g.userData = { yF, yT, porcaY: yF - 0.056, mancais, est };
    return g;
  }

  const raiz = new T.Group(); B.scene.add(raiz);
  let P = {};
  const coax = [];     // peças coaxiais: [obj, y, raio] para a auditoria CONCÊNTRICO

  if (id === 'carretel') {
    const R = 0.30, r = 0.10, yG = 0.05, yP = -0.085;
    const spin = new T.Group(); raiz.add(spin);
    spin.add(cil(R, 0.11, ACO, yG), aro(R, 0.006, ARESTA, yG - 0.046), aro(R, 0.006, ARESTA, yG + 0.046));
    const fl1 = cil(R + 0.018, 0.012, ACO_ESC, yG - 0.051), fl2 = cil(R + 0.018, 0.012, ACO_ESC, yG + 0.051);
    spin.add(fl1, fl2, aro(R + 0.018, 0.004, ARESTA, yG - 0.058));
    const tp = cil(r, 0.08, ACO_CLARO, yP); spin.add(tp, aro(r, 0.005, ARESTA_ESC, yP - 0.041));
    const flp = cil(r + 0.03, 0.01, ACO_ESC, yP - 0.045); spin.add(flp, aro(r + 0.03, 0.004, ARESTA, yP - 0.051));
    // furo da trava no flange grande (frente) e faixa radial assimétrica na face da frente do tambor grande
    const furo = cil(0.016, 0.004, ARESTA_ESC, yG - 0.059, 24); furo.position.x = -0.16; furo.position.z = 0.16; spin.add(furo);
    const fx = caixa(R * 0.5, 0.004, 0.032, ARESTA, R * 0.66, yG - 0.06, 0); spin.add(fx);
    const pt = cil(0.022, 0.006, ARESTA, yG - 0.061, 24); pt.position.x = R * 0.95; spin.add(pt);
    P.esp1 = espiras(R + 0.008, yG - 0.035, yG + 0.035, 5, +1); P.esp2 = espiras(r + 0.008, yP - 0.03, yP + 0.03, 4, -1);
    spin.add(P.esp1, P.esp2);
    coax.push([tp, yP - 0.04, r], [flp, yP - 0.05, r + 0.03], [fl1, yG - 0.057, R + 0.018], [fl2, yG + 0.057, R + 0.018]);
    P.g = garfo(raiz, -0.16, 0.135, R + 0.16, +1);
    // trava: pino de aço preso ao braço da frente; entra no furo do flange grande (x = −0,22 com θ = 0) deslizando ao longo do eixo
    raiz.add(arestas(caixa(0.19, 0.022, 0.026, ACO_GARFO, -0.085, -0.16, 0.16), 0x9FB0C8));
    P.trava = new T.Group(); raiz.add(P.trava);
    const pino = cil(0.014, 0.17, ACO_CLARO, -0.085); pino.position.set(-0.16, -0.085, 0.16); P.trava.add(pino, aro(0.014, 0.003, ARESTA, -0.17));
    P.trava.children[1].position.set(-0.16, -0.17, 0.16);
    P.b1 = bloco(0.14, R + 0.008, yG, 0); P.b2 = bloco(0.166, -(r + 0.008), yP, 0); raiz.add(P.b1, P.b2);
    P.f1 = fio(R + 0.008, yG); P.f2 = fio(-(r + 0.008), yP); raiz.add(P.f1, P.f2);
    P.spin = spin; P.R = R; P.r = r; P.yG = yG; P.yP = yP;
  } else if (id === 'volante') {
    // anel R1 0,30 / R2 0,40, cubo 0,10, 4 raios, 2 discos de 0,05 a 0,25, tambor leve 0,15 na frente; bloco 10 kg no fio
    function monta(tipo, x0) {
      const g = new T.Group(); g.position.x = x0; raiz.add(g);
      const spin = new T.Group(); g.add(spin);
      const q = { g, spin, partes: {}, coax: [] };
      if (tipo === 'aro') {
        const a = anel(0.385, 0.40, 0.06, ACO, 0); spin.add(a, aro(0.40, 0.005, ARESTA, -0.031), aro(0.385, 0.004, ARESTA, -0.031));
        q.partes.anel = [a];
        const cb = cil(0.035, 0.06, ACO_ESC, 0); spin.add(cb);
        for (let i = 0; i < 4; i++) { const ang = i * PI / 2 + PI / 4, sp = caixa(0.016, 0.02, 0.35, ACO_ESC, Math.sin(ang) * 0.21, 0, Math.cos(ang) * 0.21); sp.rotation.y = ang; spin.add(sp); }
        q.coax.push([a, -0.03, 0.40], [cb, -0.03, 0.035]);
      } else {
        const MA = ACO.clone(); q.MA = MA; const a = anel(0.30, 0.40, 0.065, MA, 0); const ar = [aro(0.40, 0.006, ARESTA, -0.034), aro(0.30, 0.005, ARESTA, -0.034)];
        spin.add(a, ...ar); q.partes.anel = [a, ...ar];
        const MC = ACO_CLARO.clone(); q.MC = MC; const c = cil(0.10, 0.08, MC, 0); const cr = aro(0.10, 0.005, ARESTA_ESC, -0.041); spin.add(c, cr); q.partes.cubo = [c, cr];
        for (let i = 0; i < 4; i++) { const ang = i * PI / 2, sp = caixa(0.018, 0.022, 0.20, ACO_ESC, Math.cos(ang) * 0.20, 0, Math.sin(ang) * 0.20); sp.rotation.y = -ang + PI / 2; spin.add(sp); }
        q.partes.discos = [];
        for (const s of [-1, 1]) { q.MD = q.MD || ACO_CLARO.clone(); const d = cil(0.05, 0.05, q.MD, -0.005, 48); d.position.x = s * 0.25; const e = aro(0.05, 0.004, ARESTA_ESC, -0.031); e.position.x = s * 0.25; spin.add(d, e); q.partes.discos.push(d, e); }
        q.miolo = cil(0.30, 0.066, FANT, 0); spin.add(q.miolo);
        q.calor = new T.MeshBasicMaterial({ color: 0xFF5A36, transparent: true, opacity: 0, depthWrite: false });
        spin.add(aro(0.40, 0.012, q.calor, 0));
        q.coax.push([a, -0.033, 0.40], [c, -0.04, 0.10]);
      }
      const fx = caixa(0.07, 0.004, 0.03, ARESTA, 0, -0.036, 0); fx.position.set(0.0, -0.036, 0.35); fx.rotation.y = PI / 2; spin.add(fx);
      const fx2 = cil(0.016, 0.005, ARESTA, -0.037, 20); fx2.position.set(0.0, -0.037, 0.35); spin.add(fx2);
      const tb = cil(0.15, 0.045, ACO_CLARO, -0.085); spin.add(tb, aro(0.15, 0.005, ARESTA_ESC, -0.108), aro(0.12, 0.003, ARESTA_ESC, -0.108));
      q.partes.tambor = [tb]; q.coax.push([tb, -0.107, 0.15]);
      q.esp = espiras(0.158, -0.10, -0.07, 3, +1); spin.add(q.esp);
      // garfo por BAIXO (pedestal): deixa o topo do anel livre para a pastilha do freio
      q.gf = garfo(g, -0.135, 0.07, -2.4, -1);
      q.b = bloco(0.17, 0.158, -0.085, 0); g.add(q.b); q.f = fio(0.158, -0.085); g.add(q.f);
      return q;
    }
    P.v = monta('vol', 0); P.a = monta('aro', 1.25); P.a.g.visible = false;
    // freio: pastilha com volume no topo do anel, braço que a pressiona (articulado à direita) e calor no contato
    P.freio = new T.Group(); raiz.add(P.freio);
    P.freio.add(arestas(caixa(0.17, 0.075, 0.045, ACO_ESC, 0, 0, 0.4265), 0x9FB0C8));
    P.freio.add(arestas(caixa(0.19, 0.03, 0.03, ACO_GARFO, 0.02, 0, 0.465), 0x9FB0C8));
    const brf = arestas(caixa(0.03, 0.03, 0.30, ACO_GARFO, 0.17, 0, 0.58), 0x9FB0C8); brf.rotation.y = -0.6; P.freio.add(brf);
    P.calorP = new T.MeshBasicMaterial({ color: 0xFF5A36, transparent: true, opacity: 0 }); P.freio.add(caixa(0.17, 0.075, 0.01, P.calorP, 0, 0, 0.405));
  } else if (id === 'haste') {
    // haste d = 1,0 m (−0,25 a 0,75 em x), seção 5 × 3,5 cm, furo com pino em x = 0 (d/4 da ponta), garfo por cima
    const spin = new T.Group(); raiz.add(spin);
    const corpo = arestas(caixa(1.0, 0.05, 0.035, ACO, 0.25, 0, 0), 0xDCE6F5); spin.add(corpo);
    const furo = anel(0.02, 0.034, 0.052, ACO_CLARO, 0); spin.add(furo, aro(0.034, 0.003, ARESTA, -0.027));
    P.caps = [-0.25, 0.75].map(xx => { const c = caixa(0.004, 0.052, 0.037, ARESTA, xx, 0, 0); spin.add(c); return c; });
    P.g = garfo(raiz, -0.06, 0.06, 0.30, +1);
    P.spin = spin; P.corpo = corpo; coax.push([furo, -0.026, 0.034]);
  } else if (id === 'pendulo') {
    // até 3 pêndulos de discos (R = 0,10 m, 3 cm de espessura, chanfro claro), haste leve, pino com garfo por cima.
    // e.p = [[x, z, l, ang, duplo, fant], ...] em metros de cena (1 m de cena = 1 m do problema)
    P.pend = [];
    for (let i = 0; i < 3; i++) {
      const g = new T.Group(); raiz.add(g);
      const spin = new T.Group(); g.add(spin);
      const mkDisco = () => { const d = new T.Group(); const c = cil(0.10, 0.03, ACO, 0); d.add(c, aro(0.10, 0.0045, ARESTA, -0.016), aro(0.10, 0.0045, ARESTA, 0.016), aro(0.07, 0.002, ARESTA_ESC, -0.0155)); return d; };
      const dB = mkDisco(), dC = mkDisco(); spin.add(dB, dC);
      const haste = arestas(caixa(0.014, 0.012, 1, ACO_CLARO, 0, -0.022, 0), 0xDCE6F5); spin.add(haste);
      const furo = cil(0.012, 0.034, ARESTA_ESC, 0, 24); spin.add(furo);
      const gf = garfo(g, -0.05, 0.05, 0.13, +1);
      P.pend.push({ g, spin, dB, dC, haste, furo, gf });
    }
  }

  function atualiza(e) {
    const th = e.th || 0;
    raiz.visible = (e.op == null ? 1 : e.op) > 0.01;
    if (id === 'carretel') {
      P.spin.rotation.y = th;
      const z1 = (e.z1 == null ? -0.62 : e.z1) - P.R * th, z2 = (e.z2 == null ? -0.80 : e.z2) + P.r * th;
      const l2 = 0.166 * Math.cbrt((e.m2 || 10) / 10);
      P.b2.scale.setScalar(l2 / 0.166);
      P.b1.position.z = z1; P.b2.position.z = z2;
      estica(P.f1, 0, z1 + 0.056); estica(P.f2, 0, z2 + 0.4 * l2);
      const tv = e.trava != null ? e.trava : (e.lock ? 1 : 0);          // 1 = pino dentro do furo; 0 = recuado 9 cm (fora)
      P.trava.position.y = -0.10 * (1 - tv);
      const fl = e.esp_flash || 0;
      FIO.emissive.setRGB(0.25 * fl, 0.85 * fl, 0.95 * fl);
    } else if (id === 'volante') {
      const v = P.v; v.spin.rotation.y = th;
      const zb = (e.zb == null ? -0.5 : e.zb) - 0.15 * th - (e.cai || 0);
      v.b.position.z = zb; v.b.visible = e.cord !== false; v.f.visible = v.b.visible;
      if (v.b.visible) estica(v.f, (e.cai ? -e.cai : 0), zb + 0.068);
      v.esp.visible = e.cord !== false || (e.cai || 0) > 0;
      const ex = e.explode || 0;
      v.partes.cubo.forEach(o => o.position.y = (o.geometry.type === 'TorusGeometry' ? -0.041 : 0) - 0.16 * ex);
      v.partes.discos.forEach(o => o.position.y = (o.geometry.type === 'TorusGeometry' ? -0.031 : -0.005) - 0.30 * ex);
      v.partes.anel.forEach(o => o.position.y = (o.geometry.type === 'TorusGeometry' ? -0.034 : 0) + 0.10 * ex);
      v.gf.visible = ex < 0.02;
      const foco = e.foco || '';
      v.MA.emissive.setHex(foco.includes('anel') ? 0x5A2442 : 0x000000);
      v.MC.emissive.setHex(foco.includes('cubo') ? 0x5A2442 : 0x000000);
      v.MD.emissive.setHex(foco.includes('discos') ? 0x5A2442 : 0x000000);
      v.miolo.material.opacity = e.miolo == null ? 0 : 0.55 * e.miolo;
      v.miolo.visible = (e.miolo || 0) > 0.01; v.miolo.position.y = -(e.miolo_dy || 0);
      v.calor.opacity = 0.75 * (e.heat || 0);
      P.freio.visible = !!e.freio; P.freio.position.z = e.freio_dz || 0; P.calorP.opacity = 0.9 * (e.heat || 0);
      P.a.g.visible = !!e.dois;
      if (e.dois) { P.a.spin.rotation.y = e.th2 || 0; const z2 = -0.5 - 0.15 * (e.th2 || 0); P.a.b.position.z = z2; estica(P.a.f, 0, z2 + 0.068); }
      v.g.position.x = e.x1 || 0; P.a.g.position.x = e.x2 == null ? 1.25 : e.x2;
    } else if (id === 'haste') {
      P.spin.rotation.y = th;
      const sx = e.sx == null ? 0.25 : e.sx;                 // distância eixo → centro (o eixo desliza no E2-3)
      P.corpo.position.x = sx; P.caps[0].position.x = sx - 0.5; P.caps[1].position.x = sx + 0.5;
    } else if (id === 'pendulo') {
      const lista = e.p || [];
      P.pend.forEach((q, i) => {
        const p = lista[i]; q.g.visible = !!p; if (!p) return;
        const [x, z, l, ang, duplo] = p;
        q.g.position.set(x, 0, z); q.spin.rotation.y = -ang;
        q.gf.userData.est.forEach(o => o.visible = e.garfo !== 0);            // ang > 0: o disco de baixo vai para +x
        q.dB.position.set(0, 0, -l); q.dC.visible = !!duplo;
        const h = Math.max(0, l - 0.10);
        q.haste.visible = h > 0.005; q.haste.scale.set(1, 1, Math.max(h, 1e-3)); q.haste.position.z = -h / 2;
      });
    }
  }
  window.CENA = { atualiza };

  // ── pontos para o Manim e para a auditoria CONCÊNTRICO (px) ──
  const W = (o) => { const v = new T.Vector3(); o.getWorldPosition(v); return v; };
  const Pj = (v) => B.projeta([v.x, v.y, v.z]);
  function concentrico(gx, spin, lista, gf) {
    // c: [centro da peça projetado, eixo projetado na mesma profundidade]; p: [ponto médio 3D de dois pontos opostos da borda, eixo]
    const out = { c: [], p: [], m: [] };
    for (const [o, y, rr] of lista) {
      const wc = W(o); out.c.push([Pj(wc), B.projeta([gx, wc.y, 0])]);
      const a = spin.localToWorld(new T.Vector3(rr, y, 0)), b = spin.localToWorld(new T.Vector3(-rr, y, 0));
      out.p.push([Pj(a.clone().add(b).multiplyScalar(0.5)), B.projeta([gx, (a.y + b.y) / 2, 0])]);
    }
    if (gf) for (const m of gf.userData.mancais) { const wc = W(m); out.m.push([Pj(wc), B.projeta([gx, wc.y, 0])]); }
    out.porca = gf ? B.projeta([gx, gf.userData.porcaY, 0]) : null;
    out.eixo = [B.projeta([gx, -0.3, 0]), B.projeta([gx, 0.3, 0])];
    return out;
  }
  window.pontos3d = e => {
    if (id === 'carretel') {
      const f = (o, x, y) => [Pj(new T.Vector3(x, y, o.userData.topo)), Pj(new T.Vector3(x, y, o.userData.topo - 0.5)), B.projeta([x, y, 0])];
      return { eixo: B.projeta([0, 0, 0]), b1: Pj(W(P.b1)), b2: Pj(W(P.b2)), th: e.th || 0,
        conc: concentrico(0, P.spin, coax, P.g), fios: [f(P.f1, P.R + 0.008, P.yG), f(P.f2, -(P.r + 0.008), P.yP)] };
    }
    if (id === 'volante') {
      const v = P.v, gx = v.g.position.x;
      const f = [Pj(new T.Vector3(gx + 0.158, -0.085, v.f.userData.topo || 0)), Pj(new T.Vector3(gx + 0.158, -0.085, (v.f.userData.topo || 0) - 0.5)), B.projeta([gx + 0.158, -0.085, -(e.cai || 0)])];
      return { eixo: B.projeta([gx, 0, 0]), b: Pj(W(v.b)), th: e.th || 0,
        conc: (e.explode || 0) < 0.02 ? concentrico(gx, v.spin, v.coax, v.gf) : null, fios: v.f.visible ? [f] : [] };
    }
    if (id === 'haste') return { eixo: B.projeta([0, 0, 0]), th: e.th || 0, conc: concentrico(0, P.spin, coax, P.g) };
    if (id === 'pendulo') {
      const out = { pend: [] };
      P.pend.forEach(q => { if (!q.g.visible) return; const gx = q.g.position.x, gz = q.g.position.z;
        const c = Pj(W(q.dB)), ei = B.projeta([gx, 0, gz]);
        out.pend.push({ eixo: ei, disco: c, conc: [[Pj(W(q.furo)), ei]].concat(q.gf.userData.mancais.map(m => [Pj(W(m)), B.projeta([gx, W(m).y, gz])])) }); });
      return out;
    }
    return {};
  };
  window.cenaPronta = true;
})();
