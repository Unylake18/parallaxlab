// Cavalo CC0 da Quaternius (assets_unidade/cavalo, ver LICENCA.txt) puxando uma pedra por uma corda — adaptado do F2 do yt_0015.
// Estado: {xp: x do peitoral, tau: tempo do ciclo Walk, incl: inclinação para a frente, L: comprimento da corda (horizontal),
//          gelo: opacidade do gelo sob as patas, gx0/gx1: faixa do gelo, cam}
// O peitoral fica em (xp, −meia_larg, zp); a corda vai até a pedra, que fica atrás (−x). pontos3d devolve as pontas da corda,
// os cascos e o topo, já projetados em pixels, para a camada Manim prender setas e rótulos.
(function () {
  const B = B3D, T3 = THREE, PI = Math.PI;
  const C = { comprimento: 4.0, pedra_r: 0.5, yaw: 1.5708, peito_fx: 0.24, peito_fz: 0.6 };
  const CORES = { Main: 0x56606F, Main_Dark: 0x434C5A, Main_Light: 0x646F7F, Muzzle: 0x434C5A, Hair: 0x9AA6BA, Hooves: 0x2A3140,
    Eye_Black: 0x0A0F1E, Eye_White: 0xB8C4DA };
  B.scene.fog = new T3.Fog(0x050816, 30, 60);
  window.aposCamera = D => { B.scene.fog.near = D + 4; B.scene.fog.far = D + 22; };
  B.chao(0x080C18);
  { // pedrinhas e tufos no chão (dão a noção de deslocamento quando a câmera acompanha)
    let s = 5; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    const g = new T3.IcosahedronGeometry(1, 0), m = B.mat(0x2A3140, 0.1, 0.9, 0.25, { flatShading: true });
    const N = 900, inst = new T3.InstancedMesh(g, m, N), o = new T3.Object3D();
    for (let i = 0; i < N; i++) {
      const r = 0.03 + 0.07 * rnd() ** 2;
      o.position.set(-60 + 320 * rnd(), -2.5 + 9 * rnd(), r * 0.2); o.rotation.set(rnd() * 3, rnd() * 3, rnd() * 3);
      o.scale.set(r * 1.6, r, r * 0.5); o.updateMatrix(); inst.setMatrixAt(i, o.matrix);
    }
    B.scene.add(inst);
  }
  const gelo = new T3.Mesh(new T3.PlaneGeometry(1, 6), B.mat(0x4F79B8, 0.3, 0.12, 0.6, { transparent: true, opacity: 0 }));
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
  let cavalo = null, mixer = null, larg = 1, alt = 1, meia = 0.3, xoff = 0;
  const sCav = B.sombra(1, 1);
  const ancora = new T3.Vector3(), vB = new T3.Vector3(), cascos = [];

  function atualiza(e) {
    if (!cavalo) return;
    mixer.setTime(e.tau || 0);
    const xc = e.xp - C.peito_fx * larg;                       // centro da caixa do cavalo
    cavalo.position.x = xc + xoff;
    cavalo.rotation.set(PI / 2, 0, 0); cavalo.rotateY(C.yaw); cavalo.rotateOnWorldAxis(new T3.Vector3(0, 1, 0), e.incl || 0);
    cavalo.updateMatrixWorld(true);
    ancora.set(e.xp, -meia - 0.02, C.peito_fz * alt);
    faixa.position.set(ancora.x, -meia + 0.01, ancora.z); faixa.rotation.set(0, -0.35, 0);
    const xa = e.xp - (e.L || 2.0);                            // ponta da corda na pedra
    pedra.position.set(xa - xPedraFrente * 0.92, 0, zPedra);
    vB.set(xa, -meia - 0.02, zPedra + C.pedra_r * 0.25);
    sPedra.position.x = pedra.position.x;
    sCav.position.x = xc; sCav.scale.set(larg * 0.9, larg * 0.32, 1);
    gelo.material.opacity = 0.7 * (e.gelo || 0); gelo.visible = (e.gelo || 0) > 0.001;
    if (e.gx0 !== undefined) { gelo.scale.x = e.gx1 - e.gx0; gelo.position.x = (e.gx0 + e.gx1) / 2; }
    if (corda) { B.scene.remove(corda); corda.geometry.dispose(); }
    corda = new T3.Mesh(new T3.TubeGeometry(new T3.LineCurve3(vB.clone(), ancora.clone()), 4, 0.032, 8, false), matCorda);
    B.scene.add(corda);
  }
  window.CENA = { atualiza };
  window.pontos3d = () => {
    const r = { corda_pedra: B.projeta(vB.toArray()), corda_peito: B.projeta(ancora.toArray()) };
    const bb = new T3.Box3().setFromObject(cavalo);
    r.topo = B.projeta([(bb.min.x + bb.max.x) / 2, 0, bb.max.z]);
    r.cascos = B.projeta([(bb.min.x + bb.max.x) / 2, 0, 0]);
    r.cav_tras = B.projeta([bb.min.x, 0, alt * 0.55]); r.cav_frente = B.projeta([bb.max.x, 0, alt * 0.55]);
    r.pedra_base = B.projeta([pedra.position.x, 0, 0]); r.pedra_topo = B.projeta([pedra.position.x, 0, 2 * zPedra]);
    r.pedra_tras = B.projeta([pedra.position.x - C.pedra_r * 1.2, 0, zPedra]);
    return r;
  };
  window.medidas = () => ({ larg, alt, meia, zPedra, xPedraFrente, peito_z: C.peito_fz * alt, corda_z0: zPedra + C.pedra_r * 0.25, clip: window.clipDur });

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
    B.scene.add(cavalo); B.scene.add(faixa);
    window.cenaPronta = true;
  }, e => { console.error('GLTF', e); });
})();
