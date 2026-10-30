// Cavalo CC0 da Quaternius (assets_unidade/cavalo, ver LICENCA.txt) puxando uma pedra por uma corda — adaptado do F2 do yt_0015.
// Estado: {xp: x do peitoral, tau: tempo do ciclo Walk, incl: inclinação para a frente, L: comprimento da corda (horizontal),
//          gelo: opacidade do gelo sob as patas, gx0/gx1: faixa do gelo, cam}
// O peitoral fica em (xp, −meia_larg, zp); a corda vai até a pedra, que fica atrás (−x). pontos3d devolve as pontas da corda,
// os cascos e o topo, já projetados em pixels, para a camada Manim prender setas e rótulos.
(function () {
  const B = B3D, T3 = THREE, PI = Math.PI;
  // v4: balancim (barra atrás da anca, na altura do jarrete) com dois tirantes até o peitoral; a corda sai do balancim
  const C = { comprimento: 4.0, pedra_r: 0.5, yaw: 1.5708, peito_fx: 0.24, peito_fz: 0.6, bal_dx: 3.45, bal_z: 0.85, bal_w: 1.05 };
  const CORES = { Main: 0x56606F, Main_Dark: 0x434C5A, Main_Light: 0x646F7F, Muzzle: 0x434C5A, Hair: 0x9AA6BA, Hooves: 0x2A3140,
    Eye_Black: 0x0A0F1E, Eye_White: 0xB8C4DA };
  B.scene.fog = new T3.Fog(0x0A1432, 30, 60);
  window.aposCamera = D => { B.scene.fog.near = D + 4; B.scene.fog.far = D + 22; };
  const piso = B.chao(0x080C18);
  // pedrinhas e tufos no chão (dão a noção de deslocamento quando a câmera acompanha): padrão periódico (PER m), repetido 4 vezes;
  // o chão e as pedrinhas andam junto com o cavalo em saltos de PER, invisíveis porque o padrão se repete (o cavalo anda centenas de metros)
  const PER = 80, seixos = (() => {
    let s = 5; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    const g = new T3.IcosahedronGeometry(1, 0), m = B.mat(0x2A3140, 0.1, 0.9, 0.25, { flatShading: true });
    const N0 = 230, inst = new T3.InstancedMesh(g, m, 4 * N0), o = new T3.Object3D();
    for (let i = 0; i < N0; i++) {
      const r = 0.03 + 0.07 * rnd() ** 2, x = PER * rnd(), y = -2.5 + 9 * rnd(), rot = [rnd() * 3, rnd() * 3, rnd() * 3];
      for (let k = 0; k < 4; k++) {
        o.position.set(x + (k - 1) * PER, y, r * 0.2); o.rotation.set(...rot);
        o.scale.set(r * 1.6, r, r * 0.5); o.updateMatrix(); inst.setMatrixAt(4 * i + k, o.matrix);
      }
    }
    B.scene.add(inst); return inst;
  })();
  // gelo (v3): placa translúcida azulada (#9CC7FF a ~35 %) só sob as patas, com reflexos finos; pouco ambiente (de raspão o
  // reflexo especular deixava a placa branca chapada: material sem luz)
  const gelo = new T3.Group(), matGelo = new T3.MeshBasicMaterial({ color: 0x9CC7FF, transparent: true, opacity: 0, depthWrite: false });
  gelo.add(new T3.Mesh(new T3.PlaneGeometry(1, 4), matGelo));
  const matRef = new T3.MeshBasicMaterial({ color: 0xDCEBFF, transparent: true, opacity: 0, depthWrite: false });
  { let s = 7; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    for (let i = 0; i < 9; i++) { const r = new T3.Mesh(new T3.PlaneGeometry(0.06 + 0.12 * rnd(), 0.025), matRef);
      r.position.set(-0.45 + 0.9 * rnd(), -1.6 + 3.2 * rnd(), 0.002); gelo.add(r); } }
  gelo.position.z = 0.008; B.scene.add(gelo);

  // pedra: icosaedro facetado com ruído determinístico nos vértices (aço escuro, sem translucidez)
  const gp = new T3.IcosahedronGeometry(C.pedra_r, 1);
  { const p = gp.attributes.position; let s = 11; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    const mapa = new Map();
    for (let i = 0; i < p.count; i++) {
      const k = [p.getX(i), p.getY(i), p.getZ(i)].map(v => v.toFixed(3)).join(',');
      if (!mapa.has(k)) mapa.set(k, 0.8 + 0.35 * rnd());
      const f = mapa.get(k); p.setXYZ(i, p.getX(i) * f * 1.25, p.getY(i) * f * 0.9, p.getZ(i) * f * 0.85);
    }
    gp.computeVertexNormals(); }
  const pedra = new T3.Mesh(gp, new T3.MeshStandardMaterial({ color: 0x4A5262, metalness: 0.1, roughness: 0.85, envMapIntensity: 0.3, flatShading: true }));
  B.scene.add(pedra);
  gp.computeBoundingBox();
  const zPedra = -gp.boundingBox.min.z, xPedraFrente = gp.boundingBox.max.x;
  const sPedra = B.sombra(C.pedra_r * 3.4, C.pedra_r * 1.6);
  const matCorda = B.mat(0xB8C4DA, 0.2, 0.5, 0.3);
  let corda = null;
  const faixa = new T3.Mesh(new T3.BoxGeometry(0.11, 0.03, 0.7), B.mat(0xB8C4DA, 0.2, 0.5, 0.3));
  const balancim = new T3.Mesh(new T3.BoxGeometry(0.1, C.bal_w, 0.1), B.mat(0xB8C4DA, 0.3, 0.45, 0.3));
  const matTir = B.mat(0xB8C4DA, 0.2, 0.5, 0.3);
  let tirantes = [];
  const vBal = new T3.Vector3();
  let cavalo = null, mixer = null, larg = 1, alt = 1, meia = 0.3, xoff = 0;
  const sCav = B.sombra(1, 1);
  const ancora = new T3.Vector3(), vB = new T3.Vector3(), cascos = [];

  function atualiza(e) {
    if (!cavalo) return;
    mixer.setTime(e.tau || 0);
    const salto = PER * Math.floor((e.xp || 0) / PER);
    seixos.position.x = salto; piso.position.x = salto;
    const xc = e.xp - C.peito_fx * larg;                       // centro da caixa do cavalo
    cavalo.position.x = xc + xoff;
    cavalo.rotation.set(PI / 2, 0, 0); cavalo.rotateY(C.yaw); cavalo.rotateOnWorldAxis(new T3.Vector3(0, 1, 0), e.incl || 0);
    cavalo.updateMatrixWorld(true);
    ancora.set(e.xp, -meia - 0.02, C.peito_fz * alt);
    faixa.position.set(ancora.x, -meia + 0.01, ancora.z); faixa.rotation.set(0, -0.35, 0);
    vBal.set(e.xp - C.bal_dx, 0, C.bal_z);                     // centro do balancim (a corda sai daqui)
    balancim.position.copy(vBal);
    tirantes.forEach(t => { B.scene.remove(t); t.geometry.dispose(); });
    tirantes = [-1, 1].map(sy => {
      const a = new T3.Vector3(vBal.x, sy * C.bal_w / 2, vBal.z), b = new T3.Vector3(e.xp, sy * (meia + 0.02), C.peito_fz * alt);
      const m = new T3.Mesh(new T3.TubeGeometry(new T3.LineCurve3(a, b), 2, 0.018, 6, false), matTir); B.scene.add(m); return m;
    });
    const xa = e.xp - (e.L || 2.0);                            // ponta da corda na pedra
    pedra.position.set(xa - xPedraFrente * 0.92, 0, zPedra);
    vB.set(xa, 0, zPedra + C.pedra_r * 0.25);
    sPedra.position.x = pedra.position.x;
    sCav.position.x = xc; sCav.scale.set(larg * 0.9, larg * 0.32, 1);
    matGelo.opacity = 0.35 * (e.gelo || 0); matRef.opacity = 0.45 * (e.gelo || 0); gelo.visible = (e.gelo || 0) > 0.001;
    if (e.gx0 !== undefined) { gelo.scale.x = e.gx1 - e.gx0; gelo.position.x = (e.gx0 + e.gx1) / 2; }
    if (corda) { B.scene.remove(corda); corda.geometry.dispose(); }
    corda = new T3.Mesh(new T3.TubeGeometry(new T3.LineCurve3(vB.clone(), vBal.clone()), 4, 0.032, 8, false), matCorda);
    B.scene.add(corda);
  }
  window.CENA = { atualiza };
  window.pontos3d = () => {
    const r = { corda_pedra: B.projeta(vB.toArray()), corda_peito: B.projeta(ancora.toArray()), balancim: B.projeta(vBal.toArray()),
      bal_perto: B.projeta([vBal.x, -C.bal_w / 2, vBal.z]), bal_longe: B.projeta([vBal.x, C.bal_w / 2, vBal.z]) };
    const bb = new T3.Box3().setFromObject(cavalo);
    r.topo = B.projeta([(bb.min.x + bb.max.x) / 2, 0, bb.max.z]);
    r.cascos = B.projeta([(bb.min.x + bb.max.x) / 2, 0, 0]);
    r.cav_tras = B.projeta([bb.min.x, 0, alt * 0.55]); r.cav_frente = B.projeta([bb.max.x, 0, alt * 0.55]);
    r.cabeca = B.projeta([bb.max.x, 0, bb.max.z]); r.cascos_tras = B.projeta([bb.min.x, 0, 0]); r.cascos_frente = B.projeta([bb.max.x, 0, 0]);
    r.pedra_base = B.projeta([pedra.position.x, 0, 0]); r.pedra_topo = B.projeta([pedra.position.x, 0, 2 * zPedra]);
    r.pedra_tras = B.projeta([pedra.position.x - C.pedra_r * 1.2, 0, zPedra]);
    return r;
  };
  window.medidas = () => ({ larg, alt, meia, zPedra, xPedraFrente, peito_z: C.peito_fz * alt, corda_z0: zPedra + C.pedra_r * 0.25, bal_dx: C.bal_dx, bal_z: C.bal_z, clip: window.clipDur });

  const bin = Uint8Array.from(atob(window.CAVALO_GLB), c => c.charCodeAt(0)).buffer;
  new T3.GLTFLoader().parse(bin, '', g => {
    cavalo = g.scene;
    cavalo.traverse(o => {
      if (o.isMesh) {
        const nome = (o.material && o.material.name) || 'Main';
        o.material = B.mat(CORES[nome] !== undefined ? CORES[nome] : 0x56606F, nome === 'Hair' ? 0.2 : 0.3, 0.6, 0.18, { skinning: o.isSkinnedMesh });
        o.frustumCulled = false;
      }
    });
    mixer = new T3.AnimationMixer(cavalo);
    const clip = g.animations.find(a => a.name === 'Walk') || g.animations[0];
    mixer.clipAction(clip).play();
    cavalo.rotation.set(PI / 2, 0, 0); cavalo.rotateY(C.yaw); cavalo.updateMatrixWorld(true);
    mixer.setTime(0); cavalo.updateMatrixWorld(true);
    let bb = new T3.Box3().setFromObject(cavalo);
    const s = C.comprimento / (bb.max.x - bb.min.x); cavalo.scale.setScalar(s); cavalo.updateMatrixWorld(true);
    bb = new T3.Box3().setFromObject(cavalo);
    xoff = -((bb.max.x + bb.min.x) / 2); cavalo.position.set(xoff, 0, -bb.min.z);
    alt = bb.max.z - bb.min.z; larg = bb.max.x - bb.min.x; meia = (bb.max.y - bb.min.y) / 2 * 0.95;
    window.clipDur = clip.duration;
    B.scene.add(cavalo); B.scene.add(faixa); B.scene.add(balancim);
    window.cenaPronta = true;
  }, e => { console.error('GLTF', e); });
})();
