// T7: esferas de aço ligadas por molas (vista 'frente', plano y = 0); v7: disco de hóquei em aço escovado sobre gelo com binário
// (câmera 3/4 baixa, fantasmas estroboscópicos do giro) e a bola da parábola com rastro estroboscópico (T7-9).
// Estado: {esf: [[x, z, vis, brilho], ...], molas: [[i, j, vis, brilho], ...], piso: 0|1,
//          disco: {vis, x, y, ang, fant: [ang, ...]} | null, bola: {x, z, fant: [[x, z, op], ...]} | null, cam}
// Posições calculadas no Manim (sec_t7.py). brilho 0–1 acende a mola (azul-claro) ou a esfera.
(function () {
  const B = B3D, T3 = THREE, PI = Math.PI, R = 0.45;
  const AZUL = new T3.Color(0x5AA2FF), PRETO = new T3.Color(0x000000), MAGC = 0xEA63FF;
  const piso = B.chao();
  { // pedrinhas no chão: mostram a deriva do conjunto quando a câmera acompanha o centro
    let s = 9; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    const g = new T3.IcosahedronGeometry(1, 0), m = B.mat(0x2A3140, 0.1, 0.9, 0.25, { flatShading: true });
    const N = 500, inst = new T3.InstancedMesh(g, m, N), o = new T3.Object3D();
    for (let i = 0; i < N; i++) {
      const r = 0.025 + 0.05 * rnd() ** 2;
      o.position.set(-30 + 90 * rnd(), -2.5 + 9 * rnd(), r * 0.2); o.scale.set(r * 1.6, r, r * 0.5); o.updateMatrix(); inst.setMatrixAt(i, o.matrix);
    }
    piso.add(inst);
    var seixos = inst;
  }
  const esf = [0, 1, 2].map(() => {
    const m = new T3.Mesh(new T3.SphereGeometry(R, 40, 28), B.mat(0x8C97A8, 0.75, 0.3, 0.55));
    B.scene.add(m); return m;
  });
  const sombras = esf.map(() => B.sombra(R * 2.6, R * 1.0));
  const matMola = () => B.mat(0xB8C4DA, 0.6, 0.35, 0.5);
  const molas = [0, 1, 2].map(() => { const m = new T3.Mesh(new T3.BufferGeometry(), matMola()); B.scene.add(m); return m; });
  class Helice extends T3.Curve {
    constructor(a, b, n, r) { super(); this.a = a; this.b = b; this.n = n; this.r = r; }
    getPoint(t, alvo = new T3.Vector3()) {
      const d = this.b.clone().sub(this.a), L = d.length(); d.normalize();
      const u = new T3.Vector3(-d.z, 0, d.x), w = new T3.Vector3(0, 1, 0);       // perpendiculares no plano e fora dele
      const ang = 2 * PI * this.n * t, ext = Math.min(1, Math.min(t, 1 - t) / 0.08);  // pontas retas
      return alvo.copy(this.a).addScaledVector(d, L * t).addScaledVector(u, this.r * ext * Math.cos(ang)).addScaledVector(w, this.r * ext * Math.sin(ang));
    }
  }

  // ── v7: disco de hóquei (aço escovado, borda chanfrada, faixa magenta num trecho da lateral) sobre a pista de gelo ──
  const RD = 1.35, HD = 0.62, CH = 0.09;
  const texEscovado = (() => {                           // escovado circular (riscos concêntricos finos)
    const c = document.createElement('canvas'); c.width = c.height = 512; const g = c.getContext('2d');
    g.fillStyle = '#9aa5b6'; g.fillRect(0, 0, 512, 512);
    let s = 41; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    for (let i = 0; i < 900; i++) {
      const r = 256 * Math.sqrt(rnd()), a0 = 2 * PI * rnd(), da = 0.2 + 1.4 * rnd(), v = 130 + Math.floor(110 * rnd());
      g.strokeStyle = `rgba(${v},${v + 6},${v + 16},${0.25 + 0.3 * rnd()})`; g.lineWidth = 0.6 + rnd();
      g.beginPath(); g.arc(256, 256, r, a0, a0 + da); g.stroke();
    }
    return new T3.CanvasTexture(c);
  })();
  const mAcoD = B.mat(0x9AA4B4, 0.8, 0.36, 0.75, { map: texEscovado });
  function corpoDisco(mLat, mTopo) {                     // o corpo do disco (lateral chanfrada, topo escovado, fundo)
    const g = new T3.Group();
    const perf = [[RD - CH, HD], [RD - CH * 0.3, HD - CH * 0.3], [RD, HD - CH], [RD, CH], [RD - CH * 0.3, CH * 0.3], [RD - CH, 0]]
      .reverse().map(p => new T3.Vector2(p[0], p[1]));          // de baixo para cima: normais para fora
    const lat = new T3.LatheGeometry(perf, 96); lat.rotateX(PI / 2); lat.computeVertexNormals();
    g.add(new T3.Mesh(lat, mLat || B.mat(0xA8B2C2, 0.85, 0.28, 0.8)));
    const topo = new T3.Mesh(new T3.CircleGeometry(RD - CH, 96), mTopo || mAcoD); topo.position.z = HD; g.add(topo);
    const fundo = new T3.Mesh(new T3.CircleGeometry(RD - CH, 48).rotateX(PI), B.mat(0x5A6372, 0.8, 0.4, 0.5)); g.add(fundo);
    return g;
  }
  const disco = corpoDisco();
  const mFaixa = B.mat(MAGC, 0.2, 0.4, 0.3, { emissive: new T3.Color(MAGC).multiplyScalar(0.35) });
  const mRisco = new T3.MeshBasicMaterial({ color: 0xDCE6FF });
  function marca(mf, mr) {                               // faixa magenta (60° da lateral) + risco radial claro no topo (lê o giro)
    const g = new T3.Group();
    const fx = new T3.Mesh(new T3.CylinderGeometry(RD + 0.006, RD + 0.006, HD - 2 * CH - 0.02, 24, 1, true, PI / 2 - PI / 6, PI / 3), mf);
    fx.rotation.x = PI / 2; fx.position.z = HD / 2; g.add(fx);
    const rr = new T3.Mesh(new T3.PlaneGeometry(RD - CH - 0.18, 0.055), mr); rr.position.set((RD - CH - 0.18) / 2 + 0.16, 0, HD + 0.003); g.add(rr);
    return g;
  }
  disco.add(marca(mFaixa, mRisco));
  const fantD = [0.42, 0.26, 0.14].map(op => {          // fantasmas estroboscópicos do giro (só faixa e risco, esmaecendo)
    const g = marca(new T3.MeshBasicMaterial({ color: MAGC, transparent: true, opacity: op, depthWrite: false }),
      new T3.MeshBasicMaterial({ color: 0xDCE6FF, transparent: true, opacity: op, depthWrite: false }));
    B.scene.add(g); return g;
  });
  B.scene.add(disco);
  const sombraD = B.sombra(RD * 2.5, RD * 2.5);
  // pista de gelo: material sobre o chão (borda que some, sem tapete), brilho especular, riscos de patins e a cruz gravada no centro
  const texGeloD = (() => {
    const c = document.createElement('canvas'); c.width = c.height = 512; const g = c.getContext('2d');
    const r = g.createRadialGradient(256, 256, 40, 256, 256, 256);
    r.addColorStop(0, 'rgba(64,98,150,0.95)'); r.addColorStop(0.62, 'rgba(48,78,128,0.75)'); r.addColorStop(1, 'rgba(30,50,90,0)');
    g.fillStyle = r; g.fillRect(0, 0, 512, 512);
    let s = 13; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    for (let i = 0; i < 90; i++) {
      const x = 512 * rnd(), y = 512 * rnd(), a = rnd() * PI, L = 30 + 120 * rnd(), d = Math.hypot(x - 256, y - 256) / 256;
      g.strokeStyle = `rgba(210,230,255,${0.16 * Math.max(0, 1 - d)})`; g.lineWidth = 0.8;
      g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + L / 2 * Math.cos(a) + 10, y + L / 2 * Math.sin(a), x + L * Math.cos(a), y + L * Math.sin(a)); g.stroke();
    }
    return new T3.CanvasTexture(c);
  })();
  const geloD = new T3.Mesh(new T3.PlaneGeometry(10, 10), B.mat(0x4A6494, 0.0, 0.16, 0.25, { map: texGeloD, transparent: true, depthWrite: false }));
  geloD.position.z = 0.002; geloD.renderOrder = -4; B.scene.add(geloD);
  const cruz = new T3.Group();
  for (const r of [0, PI / 2]) {
    const l = new T3.Mesh(new T3.PlaneGeometry(4.4, 0.035), new T3.MeshBasicMaterial({ color: 0xB8D4FF, transparent: true, opacity: 0.8, depthWrite: false }));
    l.rotation.z = r; cruz.add(l);
  }
  for (const r of [RD + 0.5, RD + 0.9]) {                // marcas de referência (anéis tracejados no gelo)
    const a = new T3.Mesh(new T3.RingGeometry(r - 0.012, r + 0.012, 96), new T3.MeshBasicMaterial({ color: 0xB8D4FF, transparent: true, opacity: 0.18, depthWrite: false }));
    cruz.add(a);
  }
  cruz.position.z = 0.004; cruz.renderOrder = -3; B.scene.add(cruz);
  // reflexo do disco no gelo (cópia espelhada, esmaecida)
  const refl = disco.clone(true);
  refl.traverse(o => { if (o.isMesh) { o.material = o.material.clone(); o.material.side = T3.DoubleSide; o.material.transparent = true; o.material.opacity = 0.22; o.material.depthWrite = false; } });
  refl.scale.z = -1; B.scene.add(refl); refl.visible = false;

  // ── v7 (A3/A4): os discos do vídeo anterior (o mesmo disco, sem as marcas) numa mesa de ar, vistos de lado ──
  const discosA = [corpoDisco(), corpoDisco(B.mat(0x4A515C, 0.5, 0.42, 0.55), B.mat(0x565E6A, 0.45, 0.45, 0.5, { map: texEscovado }))];
  discosA.forEach(d => B.scene.add(d));
  const sombrasA = discosA.map(() => B.sombra(1, 1));
  const texMesa = (() => {
    const c = document.createElement('canvas'); c.width = 1024; c.height = 512; const g = c.getContext('2d');
    g.fillStyle = 'rgba(0,0,0,0)'; g.fillRect(0, 0, 1024, 512);
    const rg = g.createLinearGradient(0, 0, 0, 512); rg.addColorStop(0, 'rgba(40,64,104,0)'); rg.addColorStop(0.18, 'rgba(40,64,104,0.9)');
    rg.addColorStop(0.82, 'rgba(40,64,104,0.9)'); rg.addColorStop(1, 'rgba(40,64,104,0)');
    g.fillStyle = rg; g.fillRect(0, 0, 1024, 512);
    for (let x = 16; x < 1024; x += 32) for (let y = 40; y < 480; y += 32) {
      const a = Math.min(1, x / 90, (1024 - x) / 90); g.fillStyle = `rgba(150,190,255,${0.5 * a})`; g.beginPath(); g.arc(x, y, 2.6, 0, 2 * PI); g.fill(); }
    const lx = g.createLinearGradient(0, 0, 1024, 0); lx.addColorStop(0, 'rgba(0,0,0,1)'); lx.addColorStop(0.06, 'rgba(0,0,0,0)');
    lx.addColorStop(0.94, 'rgba(0,0,0,0)'); lx.addColorStop(1, 'rgba(0,0,0,1)');
    g.globalCompositeOperation = 'destination-out'; g.fillStyle = lx; g.fillRect(0, 0, 1024, 512);
    return new T3.CanvasTexture(c);
  })();
  const mesa = new T3.Mesh(new T3.PlaneGeometry(8.6, 3.2), B.mat(0x7F8FB0, 0.1, 0.4, 0.15, { map: texMesa, transparent: true, depthWrite: false }));
  mesa.position.z = 0.003; mesa.renderOrder = -4; B.scene.add(mesa);

  // ── v7: bola da parábola (T7-9) com rastro estroboscópico ──
  const mBola = B.mat(0xC0CAD8, 0.8, 0.26, 0.8);
  const bola = new T3.Mesh(new T3.SphereGeometry(R, 40, 28), mBola); B.scene.add(bola);
  const sombraB = B.sombra(R * 2.6, R * 1.0);
  const fantB = [...Array(9)].map(() => {
    const m = new T3.Mesh(new T3.SphereGeometry(R, 28, 20), B.mat(0xC0CAD8, 0.5, 0.4, 0.5, { transparent: true, opacity: 0, depthWrite: false }));
    B.scene.add(m); return m;
  });

  function atualiza(e) {
    if (e.luz === 'lab') B.luzLab(); else B.luzV6();
    mesa.visible = !!e.mesa; if (e.mesa) mesa.position.x = e.mesa.x;
    discosA.forEach((d, i) => {
      const q = (e.discos || [])[i]; d.visible = !!q; sombrasA[i].visible = !!q;
      if (q) { d.scale.setScalar(q.s); d.position.set(q.x, 0, 0.0); d.rotation.z = q.ang || 0;
        sombrasA[i].position.set(q.x, 0, 0.005); sombrasA[i].scale.set(RD * 2.4 * q.s, RD * 2.4 * q.s, 1); sombrasA[i].material.opacity = 0.85; }
    });
    piso.visible = e.piso !== 0;
    const dv = !!(e.disco && e.disco.vis);
    [disco, geloD, cruz, sombraD].forEach(o => { o.visible = dv; }); seixos.visible = !dv && !e.mesa;
    fantD.forEach(g => { g.visible = false; });
    if (dv) {
      const d = e.disco;
      disco.position.set(d.x || 0, d.y || 0, 0); disco.rotation.z = d.ang || 0;
      refl.position.copy(disco.position); refl.rotation.z = disco.rotation.z;
      sombraD.position.set(disco.position.x, disco.position.y, 0.005); sombraD.material.opacity = 0.9;
      geloD.position.set(d.x || 0, d.y || 0, 0.002); cruz.position.set(0, 0, 0.004);
      (d.fant || []).forEach((a, k) => { if (k < fantD.length) { fantD[k].visible = true; fantD[k].position.copy(disco.position); fantD[k].rotation.z = a; } });
    }
    const bv = !!e.bola;
    bola.visible = bv; sombraB.visible = bv; fantB.forEach(m => { m.visible = false; });
    if (bv) {
      bola.position.set(e.bola.x, 0, e.bola.z);
      sombraB.position.x = e.bola.x; sombraB.material.opacity = Math.max(0.15, 1 - (e.bola.z - R) / 3.5);
      const sk = 1 + 0.25 * (e.bola.z - R); sombraB.scale.set(R * 2.6 * sk, R * sk, 1);
      (e.bola.fant || []).forEach((f, k) => { const m = fantB[k]; if (!m) return; m.visible = true; m.position.set(f[0], 0, f[1]); m.material.opacity = f[2]; });
    }
    esf.forEach((m, i) => { m.visible = false; sombras[i].visible = false; });
    (e.esf || []).forEach((s, i) => {
      const m = esf[i]; m.visible = !!s[2];
      m.position.set(s[0], 0, s[1]);
      m.material.emissive = PRETO.clone().lerp(new T3.Color(0x2A3F66), s[3] || 0);
      sombras[i].visible = m.visible; sombras[i].position.x = s[0];
      sombras[i].material.opacity = Math.max(0, 1 - (s[1] - R) / 1.5);
    });
    for (let k = 0; k < 3; k++) molas[k].visible = false;
    (e.molas || []).forEach((q, k) => {
      const [i, j, vis, br] = q, m = molas[k];
      if (!vis) return;
      const a = esf[i].position.clone(), b = esf[j].position.clone(), d = b.clone().sub(a).normalize();
      a.addScaledVector(d, R * 0.92); b.addScaledVector(d, -R * 0.92);
      m.geometry.dispose();
      m.geometry = new T3.TubeGeometry(new Helice(a, b, 7, 0.11), 220, 0.025, 8, false);
      m.material.color.set(0xB8C4DA).lerp(AZUL, br || 0);
      m.material.emissive = PRETO.clone().lerp(AZUL, 0.55 * (br || 0));
      m.visible = true;
    });
  }
  window.CENA = { atualiza };
  window.pontos3d = e => ({ esf: esf.map(m => B.projeta(m.position.toArray())), dc: B.projeta([disco.position.x, disco.position.y, HD]),
    bola: B.projeta(bola.position.toArray()) });
  window.cenaPronta = true;
})();
