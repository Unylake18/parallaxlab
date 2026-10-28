// F2 (e hook do yt_0016): cavalo CC0 da Quaternius (assets_unidade/cavalo, ver LICENCA.txt) puxando uma pedra por uma corda.
// Vista lateral ('frente' do base3d: o plano y = 0 cai no quadro do Manim). Tudo função do quadro: o clip Walk é amostrado em
// mixer.setTime(τ). O cavalo força quase parado (passo lento, corpo inclinado para a frente); no fim, a pedra começa a deslizar.
(function () {
  const B = B3D, TL = B.TL, T3 = THREE, PI = Math.PI, C = TL.cavalo;
  const mat = (cor, met, rug, env, skin) => new T3.MeshStandardMaterial({ color: cor, metalness: met, roughness: rug, envMapIntensity: env, skinning: !!skin });
  const CORES = { Main: 0x56606F, Main_Dark: 0x434C5A, Main_Light: 0x646F7F, Muzzle: 0x434C5A, Hair: 0x9AA6BA, Hooves: 0x2A3140,
    Eye_Black: 0x0A0F1E, Eye_White: 0xB8C4DA };

  B.scene.fog = new T3.Fog(0x050816, 30, 60);
  window.aposCamera = D => { B.scene.fog.near = D + 4; B.scene.fog.far = D + 22; };
  const chao = new T3.Mesh(new T3.PlaneGeometry(160, 80), mat(0x0B1020, 0.0, 0.6, 0.22)); B.scene.add(chao);

  const texSombra = (() => {
    const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d');
    const r = g.createRadialGradient(64, 64, 0, 64, 64, 64);
    r.addColorStop(0, 'rgba(0,0,0,0.8)'); r.addColorStop(0.5, 'rgba(0,0,0,0.4)'); r.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = r; g.fillRect(0, 0, 128, 128); return new T3.CanvasTexture(c);
  })();
  const sombra = (w, h) => { const m = new T3.Mesh(new T3.PlaneGeometry(w, h), new T3.MeshBasicMaterial({ map: texSombra, transparent: true, depthWrite: false })); m.position.z = 0.004; B.scene.add(m); return m; };

  // pedra: icosaedro facetado com ruído determinístico nos vértices
  const gp = new T3.IcosahedronGeometry(C.pedra_r, 1);
  { const p = gp.attributes.position; let s = 11; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    const mapa = new Map();
    for (let i = 0; i < p.count; i++) {
      const k = [p.getX(i), p.getY(i), p.getZ(i)].map(v => v.toFixed(3)).join(',');
      if (!mapa.has(k)) mapa.set(k, 0.8 + 0.35 * rnd());
      const f = mapa.get(k); p.setXYZ(i, p.getX(i) * f * 1.15, p.getY(i) * f * 0.9, p.getZ(i) * f * 0.82);
    }
    gp.computeVertexNormals(); }
  const pedra = new T3.Mesh(gp, new T3.MeshStandardMaterial({ color: 0x4A5262, metalness: 0.1, roughness: 0.85, envMapIntensity: 0.3, flatShading: true }));
  B.scene.add(pedra);
  gp.computeBoundingBox();
  const zPedra = -gp.boundingBox.min.z;
  const sPedra = sombra(C.pedra_r * 3.2, C.pedra_r * 1.6);

  const matCorda = mat(0xB8C4DA, 0.2, 0.5, 0.3);
  let corda = null;
  const faixa = new T3.Mesh(new T3.BoxGeometry(0.16, 0.04, 1.05), mat(0xB8C4DA, 0.2, 0.5, 0.3));

  let cavalo = null, mixer = null, acao = null, peito = null, larg = 1, ancora = new T3.Vector3();
  const sCav = sombra(1, 1);
  const vA = new T3.Vector3(), vB = new T3.Vector3();

  function estado(t) {
    const T = TL.duracao_s, u = B.clamp((t - C.t_desliza) / 2.5, 0, 1), us = B.suave(u);
    const avanco = C.v_ini * t + (t > C.t_desliza ? 0.5 * C.a_desliza * Math.pow(t - C.t_desliza, 2) * (1 - 0.3 * us) : 0);
    return { tau: C.tau0 + C.ritmo * t + (t > C.t_desliza ? 0.35 * (t - C.t_desliza) * us : 0), dx: avanco, incl: C.incl * (1 - 0.3 * us) };
  }

  function posiciona(t) {
    if (!cavalo) return;
    const e = estado(t);
    mixer.setTime(e.tau);
    cavalo.position.x = C.x_cavalo + e.dx;
    cavalo.rotation.set(PI / 2, 0, 0); cavalo.rotateY(C.yaw); cavalo.rotateOnWorldAxis(new T3.Vector3(0, 1, 0), e.incl);
    cavalo.updateMatrixWorld(true);
    pedra.position.set(C.x_pedra + e.dx, 0, zPedra); pedra.rotation.set(0, 0, 0);
    sPedra.position.x = pedra.position.x;
    sCav.position.x = cavalo.position.x; sCav.scale.set(larg * 0.9, larg * 0.32, 1);
    // peitoral: ponto fixo no corpo (fração da caixa do modelo); a faixa é uma tira vertical no peito
    ancora.set(cavalo.position.x - C.x_off + C.peito_fx * larg, -C.meia_larg - 0.02, C.peito_fz * C.altura);
    faixa.position.set(ancora.x, -C.meia_larg + 0.01, ancora.z); faixa.rotation.set(0, -0.35, 0);
    vB.set(pedra.position.x + C.pedra_r * 1.0, -C.meia_larg - 0.02, zPedra + C.pedra_r * 0.3);
    if (corda) { B.scene.remove(corda); corda.geometry.dispose(); }
    corda = new T3.Mesh(new T3.TubeGeometry(new T3.LineCurve3(vB.clone(), ancora.clone()), 4, 0.045, 8, false), matCorda);
    B.scene.add(corda);
  }

  window.pontos3d = () => ({ corda_pedra: vB.toArray(), corda_peito: ancora.toArray(),
    topo: [cavalo.position.x, 0, C.altura + 0.2] });

  window.setFrame = function (f) { B.desenha(f, t => posiciona(t)); return true; };
  window.projeta = B.projeta;

  const bin = Uint8Array.from(atob(window.CAVALO_GLB), c => c.charCodeAt(0)).buffer;
  new T3.GLTFLoader().parse(bin, '', g => {
    cavalo = g.scene;
    cavalo.traverse(o => {
      if (o.isMesh) {
        const nome = (o.material && o.material.name) || 'Main';
        o.material = mat(CORES[nome] !== undefined ? CORES[nome] : 0x56606F, nome === 'Hair' ? 0.2 : 0.3, 0.6, 0.18, o.isSkinnedMesh);
        o.frustumCulled = false;
      }
      if (o.isBone && /chest|spine.?2|body/i.test(o.name) && !peito) peito = o;
    });
    if (!peito) cavalo.traverse(o => { if (o.isBone && /neck/i.test(o.name) && !peito) peito = o; });
    window.ossos = []; cavalo.traverse(o => { if (o.isBone) window.ossos.push(o.name); });
    mixer = new T3.AnimationMixer(cavalo);
    const clip = g.animations.find(a => a.name === 'Walk') || g.animations[0];
    acao = mixer.clipAction(clip); acao.play();
    // escala e posição: comprimento do corpo = C.comprimento (unidades do Manim), cascos em z = 0
    cavalo.rotation.set(PI / 2, 0, 0); cavalo.rotateY(C.yaw); cavalo.updateMatrixWorld(true);
    mixer.setTime(0); cavalo.updateMatrixWorld(true);
    let bb = new T3.Box3().setFromObject(cavalo);
    const s = C.comprimento / (bb.max.x - bb.min.x); cavalo.scale.setScalar(s); cavalo.updateMatrixWorld(true);
    bb = new T3.Box3().setFromObject(cavalo);
    cavalo.position.set(-((bb.max.x + bb.min.x) / 2), 0, -bb.min.z);
    C.x_off = cavalo.position.x; C.x_cavalo += cavalo.position.x; C.altura = bb.max.z - bb.min.z; larg = bb.max.x - bb.min.x;
    C.meia_larg = (bb.max.y - bb.min.y) / 2 * 0.95;
    window.medidas = { escala: s, altura: C.altura, comprimento: larg, osso_peito: peito && peito.name, clip: clip.name, dur_clip: clip.duration };
    B.scene.add(cavalo); B.scene.add(faixa);
    window.cenaPronta = true;
  }, e => { console.error('GLTF', e); });
})();
