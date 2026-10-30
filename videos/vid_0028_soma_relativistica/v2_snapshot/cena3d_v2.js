// vid_0028 v2 — camada 3D (Three.js r128): foguetes, Terra/estação, chão com balizas, estrelas, carros e câmera.
// Regra de ouro do pipeline: tudo é função do quadro (window.setFrame(f)); sem relógio nem estado entre quadros.
// O 3D NÃO desenha número, sinal nem seta de grandeza: isso é do Manim. Movimento galileano e só visual
// (timeline.trajetoria, gerada por movimento.py); nada de contração, aberração ou Doppler.
// Vista lateral: K = 1 e centro (0, 0) ⇒ o ponto (x, y, 0) do 3D cai em (x, y) do Manim (dolly-zoom do modelo).
(function () {
  const TL = window.TIMELINE, FPS = window.FPS || 15, G = TL.geometria, PI = Math.PI;
  const COR = { aco: 0x8A96A8, acoEsc: 0x3A4560, terra: 0x5E6B82, geo: 0xB8C4DA, gelo: 0xEEF3FF, fundo: 0x050816, chao: 0x0E1E3C,
               ciano: 0x35D9FF, azul: 0x267BFF, magenta: 0xEA63FF };
  const W = innerWidth, H = innerHeight;
  const YF = G.y_foguete, YC = G.y_chao, L = G.comprimento_foguete;

  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H); renderer.setClearColor(COR.fundo, 1);
  document.body.appendChild(renderer.domElement);
  const veu = document.createElement('div');       // corte suave: o 3D escurece até o fundo e volta
  veu.style.cssText = `position:fixed;inset:0;background:#050816;opacity:0;pointer-events:none`;
  document.body.appendChild(veu);

  const scene = new THREE.Scene();
  scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new THREE.RoomEnvironment(), 0.04).texture;
  const chave = new THREE.DirectionalLight(0xffffff, 1.6); chave.position.set(-3, 6, 7);
  const contra = new THREE.DirectionalLight(0x9fb0d0, 0.5); contra.position.set(4, -2, -5);
  scene.add(chave, contra, new THREE.AmbientLight(0xffffff, 0.14));

  // ---------- tempo (mesmas funções do movimento.py / cena.py) ----------
  const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
  const suave = u => u * u * (3 - 2 * u);
  function chaves(lista, t, campo = 'v') {
    if (t <= lista[0].t) return lista[0][campo];
    for (let i = 0; i < lista.length - 1; i++) {
      const a = lista[i], b = lista[i + 1];
      if (t <= b.t) {
        let u = (t - a.t) / Math.max(b.t - a.t, 1e-9);
        if (b.ease !== 'linear') u = suave(u);
        return a[campo] + (b[campo] - a[campo]) * u;
      }
    }
    return lista[lista.length - 1][campo];
  }
  const TR = TL.trajetoria;
  const amostra = (nome, t) => TR[nome][clamp(Math.round(t / TR.passo_s), 0, TR[nome].length - 1)];

  // ---------- materiais ----------
  const mats = [];   // [material, cor base] para o "3D recua"
  const mat = (cor, metal = 0.75, rough = 0.38, env = 0.35) => {
    const m = new THREE.MeshStandardMaterial({ color: cor, metalness: metal, roughness: rough, envMapIntensity: env });
    mats.push([m, new THREE.Color(cor)]); return m;
  };
  const mAco = mat(COR.aco), mEsc = mat(COR.acoEsc, 0.6, 0.5), mTerra = mat(COR.terra, 0.55, 0.55, 0.3);
  const mGeo = mat(COR.geo, 0.2, 0.6, 0.2), mChao = mat(COR.chao, 0.1, 0.9, 0.1), mVidro = mat(0x0A1428, 0.9, 0.15, 0.6);
  const emiss = [];  // [material, intensidade base] para o "3D recua"
  const neon = (cor, k) => {
    const m = new THREE.MeshStandardMaterial({ color: new THREE.Color(cor).multiplyScalar(0.35), emissive: cor, emissiveIntensity: k, metalness: 0.1, roughness: 0.4 });
    emiss.push([m, k]); return m;
  };
  const mAzul = mat(COR.azul, 0.55, 0.32, 0.45), mCiano = neon(COR.ciano, 0.55);

  // ---------- foguete ----------
  function foguete() {
    const g = new THREE.Group();
    const v2 = l => l.map(([r, y]) => new THREE.Vector2(r, y));
    const corpo = new THREE.Mesh(new THREE.LatheGeometry(v2([[0, -1.02], [0.27, -1.02], [0.31, -0.92], [0.31, 0.5], [0.27, 0.78]]), 48), mAco);
    const nariz = new THREE.Mesh(new THREE.LatheGeometry(v2([[0.27, 0.78], [0.17, 1.02], [0.05, 1.2], [0, 1.25]]), 48), mAzul);
    const faixa2 = new THREE.Mesh(new THREE.CylinderGeometry(0.312, 0.312, 0.035, 48), mCiano); faixa2.position.y = 0.38;
    const bocal = new THREE.Mesh(new THREE.CylinderGeometry(0.17, 0.25, 0.24, 32, 1, true), mEsc);
    bocal.position.y = -1.14; bocal.material.side = THREE.DoubleSide;
    const faixa = new THREE.Mesh(new THREE.CylinderGeometry(0.315, 0.315, 0.07, 48), mCiano); faixa.position.y = -0.7;
    const janela = new THREE.Mesh(new THREE.TorusGeometry(0.11, 0.025, 12, 32), mCiano);
    const vidro = new THREE.Mesh(new THREE.CircleGeometry(0.105, 32), mVidro);
    janela.position.set(0, 0.62, 0.285); vidro.position.set(0, 0.62, 0.283); janela.rotation.x = vidro.rotation.x = -0.08;
    g.add(corpo, nariz, faixa, faixa2, bocal, janela, vidro);
    const forma = new THREE.Shape([[0, 0], [0.42, -0.2], [0.42, -0.58], [0, -0.38]].map(([x, y]) => new THREE.Vector2(x, y)));
    const geoAleta = new THREE.ExtrudeGeometry(forma, { depth: 0.035, bevelEnabled: false });
    for (let k = 0; k < 4; k++) {
      const a = new THREE.Mesh(geoAleta, mAzul), piv = new THREE.Group();
      a.position.set(0.27, -0.5, -0.0175); piv.add(a); piv.rotation.y = PI / 4 + k * PI / 2; g.add(piv);
    }
    // brilho do motor: sprite branco-gelo (gradiente desenhado em canvas, determinístico)
    const cv = document.createElement('canvas'); cv.width = cv.height = 64;
    const cx = cv.getContext('2d'), gr = cx.createRadialGradient(32, 32, 0, 32, 32, 32);
    gr.addColorStop(0, 'rgba(238,243,255,1)'); gr.addColorStop(0.3, 'rgba(53,217,255,0.6)'); gr.addColorStop(1, 'rgba(38,123,255,0)');
    cx.fillStyle = gr; cx.fillRect(0, 0, 64, 64);
    const brilho = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(cv), blending: THREE.AdditiveBlending, depthWrite: false, transparent: true }));
    brilho.position.y = -1.36; g.add(brilho); g.userData.brilho = brilho;
    g.rotation.z = -PI / 2;                          // eixo do foguete (lathe y) → +x
    const raiz = new THREE.Group(); raiz.add(g); raiz.userData.brilho = brilho; return raiz;
  }
  const fA = foguete(), fB = foguete(); fB.rotation.y = PI;       // B aponta para −x
  scene.add(fA, fB);

  // linhas de velocidade atrás de cada foguete (GEO, opacidade baixa): comprimento ∝ |v − v_ref| (visual)
  function rastro() {
    const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(new Array(18).fill(0), 3));
    const m = new THREE.LineBasicMaterial({ color: COR.ciano, transparent: true, opacity: 0.4, depthWrite: false });
    const l = new THREE.LineSegments(geo, m); scene.add(l); return l;
  }
  const rA = rastro(), rB = rastro();
  function poeRastro(l, x, y, z, vrel, visivel, alfa) {
    const p = l.geometry.attributes.position, s = Math.sign(vrel), comp = Math.min(1.5, 1.05 * Math.abs(vrel));
    const ofs = [[0.16, 0.0], [-0.16, 0.25], [0.0, -0.25]];
    for (let k = 0; k < 3; k++) {
      const x0 = x - s * (L / 2 + 0.15 + 0.12 * k), y0 = y + ofs[k][0], z0 = z + ofs[k][1];
      p.setXYZ(2 * k, x0, y0, z0); p.setXYZ(2 * k + 1, x0 - s * comp * (1 - 0.2 * k), y0, z0);
    }
    p.needsUpdate = true; l.visible = visivel && comp > 0.02; l.material.opacity = 0.62 * alfa;
  }

  // ---------- carros (C07) ----------
  function carro() {
    const g = new THREE.Group();
    const corpo = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.32, 0.72), mAzul); corpo.position.y = 0.33;
    const cab = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.62, 0.3, 4, 1), mAco);
    cab.rotation.y = PI / 4; cab.scale.set(1.0, 1, 0.75); cab.position.set(-0.08, 0.64, 0);
    g.add(corpo, cab);
    for (const [x, z] of [[-0.48, 0.36], [0.48, 0.36], [-0.48, -0.36], [0.48, -0.36]]) {
      const r = new THREE.Mesh(new THREE.CylinderGeometry(0.17, 0.17, 0.12, 24), mEsc);
      r.rotation.x = PI / 2; r.position.set(x, 0.17, z); g.add(r);
    }
    return g;
  }
  const cA = carro(), cB = carro(); cB.rotation.y = PI;
  cA.position.set(-2.4, YC, 0); cB.position.set(2.4, YC, 0); scene.add(cA, cB);

  // ---------- chão, balizas e Terra/estação ----------
  const chao = new THREE.Mesh(new THREE.BoxGeometry(80, 0.14, 3.0), mChao); chao.position.set(0, YC - 0.07, 0); scene.add(chao);
  const borda = new THREE.Mesh(new THREE.BoxGeometry(80, 0.022, 0.02), mCiano); borda.position.set(0, YC, 1.5); scene.add(borda);
  const balizas = [], VAO = 1.5, NB = 24;
  for (let i = 0; i < NB; i++) {
    const b = new THREE.Group();
    const poste = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.42, 10), mGeo); poste.position.y = 0.21;
    const topo = new THREE.Mesh(new THREE.SphereGeometry(0.05, 12, 8), mCiano); topo.position.y = 0.44;
    b.add(poste, topo); b.position.set(0, YC, 1.1); scene.add(b); balizas.push(b);
  }
  // Terra = estação de solo (prédio com janelas, torre de controle, radar girando, luz de topo) + serras ao fundo.
  // Cinzas-azulados neutros; só as janelas e a luz de topo brilham, em branco-gelo. Altura máx. ~1,0 (abaixo das aletas).
  const luz = (k) => {
    const m = new THREE.MeshStandardMaterial({ color: 0x0B1020, emissive: COR.gelo, emissiveIntensity: k, metalness: 0, roughness: 0.4 });
    emiss.push([m, k]); return m;
  };
  const mPredio = mat(COR.terra, 0.25, 0.7, 0.25), mJanela = neon(COR.ciano, 0.7), mFarol = neon(COR.magenta, 1.0);
  const terra = new THREE.Group();
  const caixa = (w, h, d, m, x, y, z = 0) => { const b = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m); b.position.set(x, y, z); terra.add(b); return b; };
  caixa(2.0, 0.07, 1.1, mEsc, 0, 0.035);                                   // plataforma
  caixa(1.15, 0.42, 0.7, mPredio, -0.28, 0.28);                            // prédio
  caixa(1.19, 0.04, 0.74, mEsc, -0.28, 0.51);                              // beiral
  for (let i = 0; i < 5; i++) caixa(0.13, 0.085, 0.02, mJanela, -0.72 + i * 0.22, 0.3, 0.36);   // janelas
  const torre = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.1, 0.56, 16), mPredio); torre.position.set(0.58, 0.35, 0);
  const cabine = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.16, 0.17, 20), mPredio); cabine.position.set(0.58, 0.71, 0);
  const vidros = new THREE.Mesh(new THREE.CylinderGeometry(0.205, 0.19, 0.06, 20), mJanela); vidros.position.set(0.58, 0.73, 0);
  const teto = new THREE.Mesh(new THREE.ConeGeometry(0.23, 0.1, 20), mEsc); teto.position.set(0.58, 0.845, 0);
  const antena = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.16, 6), mGeo); antena.position.set(0.58, 0.97, 0);
  const farol = new THREE.Mesh(new THREE.SphereGeometry(0.028, 12, 8), mFarol); farol.position.set(0.58, 1.05, 0);
  const haste = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 0.2, 8), mGeo); haste.position.set(-0.62, 0.63, 0);
  const radar = new THREE.Group(); radar.position.set(-0.62, 0.74, 0);
  const prato = new THREE.Mesh(new THREE.LatheGeometry([[0, 0], [0.06, 0.004], [0.13, 0.025], [0.19, 0.06]].map(([r, y]) => new THREE.Vector2(r, y)), 28), mGeo);
  prato.material.side = THREE.DoubleSide; prato.rotation.z = 1.15; radar.add(prato);
  terra.add(torre, cabine, vidros, teto, antena, farol, haste, radar); scene.add(terra);
  // Cidade em volta da estação (parada na Terra): prédios azul-escuros com janelas acesas em ciano, azul e gelo.
  {
    let s = 7; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    const mPr = [mat(0x1C2C50, 0.2, 0.7, 0.2), mat(0x24365E, 0.2, 0.7, 0.2), mat(0x18264A, 0.2, 0.7, 0.2)];
    const mJ = [neon(COR.ciano, 0.8), neon(COR.azul, 1.0), neon(COR.gelo, 0.45)], geoJ = new THREE.PlaneGeometry(0.06, 0.05);
    const lotes = [];
    for (let x = -3.0; x < -1.15; x += 0.34 + 0.1 * rnd()) lotes.push(x);
    for (let x = 1.2; x < 3.05; x += 0.34 + 0.1 * rnd()) lotes.push(x);
    for (const x of lotes) {
      const w = 0.26 + 0.1 * rnd(), h = 0.35 + 0.62 * rnd(), z = -0.75 - 0.35 * rnd();
      const b = new THREE.Mesh(new THREE.BoxGeometry(w, h, 0.4), mPr[Math.floor(rnd() * 3)]); b.position.set(x, h / 2, z); terra.add(b);
      for (let jy = 0.1; jy < h - 0.06; jy += 0.11) for (let jx = -w / 2 + 0.07; jx < w / 2 - 0.05; jx += 0.09) {
        if (rnd() < 0.42) continue;
        const j = new THREE.Mesh(geoJ, mJ[rnd() < 0.55 ? 0 : rnd() < 0.6 ? 1 : 2]); j.position.set(x + jx, jy, z + 0.201); terra.add(j);
      }
      if (h > 0.8) { const a = new THREE.Mesh(new THREE.SphereGeometry(0.02, 8, 6), mFarol); a.position.set(x, h + 0.03, z); terra.add(a); }
    }
  }

  // Serras ao fundo (paradas na Terra, deslizam com x_E): perfil periódico de 30 unidades, 3 cópias.
  const mSerra = mat(0x15295A, 0.05, 0.95, 0.1), PER = 30;
  function perfilSerra(x) { const w = 2 * PI / PER; return 0.32 + 0.22 * Math.sin(3 * w * x + 0.7) + 0.14 * Math.sin(7 * w * x + 2.1) + 0.08 * Math.sin(13 * w * x); }
  const serras = new THREE.Group();
  for (const ofs of [-PER, 0, PER]) {
    const pts = [new THREE.Vector2(-PER / 2, 0)];
    for (let k = 0; k <= 240; k++) { const x = -PER / 2 + PER * k / 240; pts.push(new THREE.Vector2(x, perfilSerra(x))); }
    pts.push(new THREE.Vector2(PER / 2, 0));
    const m = new THREE.Mesh(new THREE.ShapeGeometry(new THREE.Shape(pts)), mSerra); m.position.x = ofs; serras.add(m);
  }
  serras.position.set(0, YC, -2.5); scene.add(serras);
  const cva = document.createElement('canvas'); cva.width = 4; cva.height = 64;
  const ga = cva.getContext('2d'), gga = ga.createLinearGradient(0, 64, 0, 0);
  gga.addColorStop(0, '#ffffff'); gga.addColorStop(1, '#000000'); ga.fillStyle = gga; ga.fillRect(0, 0, 4, 64);
  const mAtm = new THREE.MeshBasicMaterial({ color: COR.ciano, alphaMap: new THREE.CanvasTexture(cva), transparent: true, opacity: 0.2, depthWrite: false });
  const atmosfera = new THREE.Mesh(new THREE.PlaneGeometry(80, 1.8), mAtm); atmosfera.position.set(0, YC + 0.9, -6); scene.add(atmosfera);
  // Subsolo: faixa escura logo abaixo do chão que some em gradiente (o chão vira "chão", não uma linha no espaço).
  const cvs = document.createElement('canvas'); cvs.width = 4; cvs.height = 64;
  const gx = cvs.getContext('2d'), gg = gx.createLinearGradient(0, 0, 0, 64);
  gg.addColorStop(0, '#ffffff'); gg.addColorStop(1, '#000000');           // alphaMap lê a luminância gx.fillStyle = gg; gx.fillRect(0, 0, 4, 64);
  const subsolo = new THREE.Mesh(new THREE.PlaneGeometry(80, 1.3), new THREE.MeshBasicMaterial({ color: 0x0C1324, alphaMap: new THREE.CanvasTexture(cvs), transparent: true, depthWrite: false }));
  subsolo.position.set(0, YC - 0.14 - 0.65, 1.55); scene.add(subsolo);

  // ---------- estrelas: volume com profundidade, paradas em relação à Terra (deslizam com x_E) ----------
  const NE = 520, est = [];
  {
    let s = 28; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    for (let i = 0; i < NE; i++) est.push([44 * rnd() - 22, 46 * rnd() - 20, -6 - 34 * rnd() ** 1.3, 0.3 + 0.6 * rnd() ** 2]);
  }
  const gPts = new THREE.BufferGeometry(), gLin = new THREE.BufferGeometry();
  gPts.setAttribute('position', new THREE.Float32BufferAttribute(new Array(NE * 3).fill(0), 3));
  const tinta = est.map((e, i) => (i % 7 === 0 ? [0.21, 0.85, 1] : i % 11 === 0 ? [0.3, 0.55, 1] : [1, 1, 1]).map(c => c * e[3]));
  gPts.setAttribute('color', new THREE.Float32BufferAttribute(tinta.flat(), 3));
  gLin.setAttribute('position', new THREE.Float32BufferAttribute(new Array(NE * 6).fill(0), 3));
  gLin.setAttribute('color', new THREE.Float32BufferAttribute(tinta.flatMap(c => [...c, 0, 0, 0]), 3));
  const mPts = new THREE.PointsMaterial({ size: 2.1, sizeAttenuation: false, vertexColors: true, transparent: true });
  const mLin = new THREE.LineBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.75 });
  scene.add(new THREE.Points(gPts, mPts), new THREE.LineSegments(gLin, mLin));
  function poeEstrelas(xE, vE) {
    const p = gPts.attributes.position, q = gLin.attributes.position, comp = 1.6 * Math.abs(vE), s = Math.sign(vE);
    est.forEach(([x0, y, z], i) => {
      const x = ((x0 + xE + 22) % 44 + 44) % 44 - 22;
      p.setXYZ(i, x, y, z); q.setXYZ(2 * i, x, y, z); q.setXYZ(2 * i + 1, x - s * comp, y, z);
    });
    p.needsUpdate = q.needsUpdate = true;
  }

  // ---------- câmera ----------
  const camera = new THREE.PerspectiveCamera(8, W / H, 1, 400);
  function cameraLateral() {                                       // modo 'topo' do modelo com K = 1, centro (0, 0)
    const fov = 8, alt = 16, D = (alt / 2) / Math.tan(fov * PI / 360);
    camera.fov = fov; camera.position.set(0, 0, D); camera.up.set(0, 1, 0); camera.lookAt(0, 0, 0);
    camera.near = D - 6; camera.far = D + 45; camera.clearViewOffset(); camera.updateProjectionMatrix();
  }
  function cameraAbertura(t) {                                     // cold open: perspectiva baixa, leve paralaxe
    camera.fov = 50; camera.position.set(2.6 - 0.35 * t, 3.0 + 0.08 * t, 7.4 - 0.25 * t); camera.up.set(0, 1, 0);
    camera.lookAt(-0.3 + 0.15 * t, 3.7, 0); camera.near = 0.1; camera.far = 200; camera.clearViewOffset(); camera.updateProjectionMatrix();
  }

  // ---------- quadro ----------
  window.setFrame = function (f) {
    const t = f / FPS, E = TL.eventos, abertura = t < E.lateral;
    const realce = chaves(TL.realce_3d, t), escuro = 1 - 0.78 * realce;
    for (const [m, c] of mats) m.color.copy(c).multiplyScalar(escuro);
    for (const [m, k] of emiss) m.emissiveIntensity = k * escuro;
    mAtm.opacity = 0.2 * escuro;
    mFarol.emissiveIntensity = escuro * (0.2 + 1.1 * Math.max(0, Math.sin(2 * PI * t / 1.6)) ** 6);
    radar.rotation.y = 0.9 * t;
    mPts.opacity = 1 - 0.7 * realce; mLin.opacity = 0.75 * (1 - 0.7 * realce);
    veu.style.opacity = chaves(TL.veu, t).toFixed(4);
    const vFog = chaves(TL.foguetes, t) > 0.5;
    fA.visible = fB.visible = vFog; cA.visible = cB.visible = !vFog;
    const pisca = 1 + 0.07 * Math.sin(41 * t) + 0.04 * Math.sin(97 * t + 1.3);
    for (const fg of [fA, fB]) { fg.userData.brilho.scale.setScalar(0.62 * pisca); fg.userData.brilho.material.opacity = escuro; }

    if (abertura) {
      // A vem da esquerda (mais perto da câmera), B da direita (mais longe); cruzam por volta de 1,9 s.
      const xa = -3.6 + 1.9 * t, xb = 3.6 - 1.9 * t;
      fA.position.set(xa, YF + 0.25, 0.85); fB.position.set(xb, YF - 0.1, -0.85);
      fA.rotation.x = 0.05 * Math.sin(1.7 * t); fB.rotation.x = -0.05 * Math.sin(1.5 * t);
      terra.visible = chao.visible = borda.visible = serras.visible = subsolo.visible = atmosfera.visible = false; balizas.forEach(b => { b.visible = false; });
      poeEstrelas(0, 0);
      poeRastro(rA, xa, YF + 0.25, 0.85, 1.25, true, 1); poeRastro(rB, xb, YF - 0.1, -0.85, -1.25, true, 1);
      cameraAbertura(t);
    } else {
      const xa = amostra('xA', t), xb = amostra('xB', t), xe = amostra('xE', t);
      const vr = amostra('vr', t), va = amostra('vA', t) - vr, vb = amostra('vB', t) - vr;
      fA.position.set(xa, YF, 0); fB.position.set(xb, YF, 0); fA.rotation.x = fB.rotation.x = 0;
      terra.visible = chao.visible = borda.visible = serras.visible = subsolo.visible = atmosfera.visible = true; balizas.forEach(b => { b.visible = true; });
      serras.position.x = ((xe % PER) + PER) % PER;
      terra.position.set(xe, YC, -0.3);
      balizas.forEach((b, i) => { b.position.x = (((i * VAO + xe + NB * VAO / 2) % (NB * VAO)) + NB * VAO) % (NB * VAO) - NB * VAO / 2; });
      poeEstrelas(xe, -vr);
      poeRastro(rA, xa, YF, 0, va, vFog, escuro); poeRastro(rB, xb, YF, 0, vb, vFog, escuro);
      cameraLateral();
    }
    renderer.render(scene, camera);
    return true;
  };
  window.projeta = p => { const v = new THREE.Vector3(...p).project(camera); return [(v.x + 1) / 2 * W, (1 - v.y) / 2 * H]; };
  window.posicoes = () => ({ A: fA.position.toArray(), B: fB.position.toArray(), E: terra.position.toArray() });
  window.cenaPronta = true;
})();
