(function () {
  const T3 = THREE, PI = Math.PI, W = innerWidth, H = innerHeight;
  const cl = (x, a, b) => Math.min(b, Math.max(a, x));
  const lin = hex => new T3.Color(hex).convertSRGBToLinear();
  const renderer = new T3.WebGLRenderer({ antialias: false, alpha: true, preserveDrawingBuffer: true, premultipliedAlpha: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H); renderer.setClearColor(0x000000, 0);
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = T3.PCFShadowMap;
  renderer.outputEncoding = T3.LinearEncoding; renderer.toneMapping = T3.NoToneMapping;
  renderer.autoClear = false;
  document.body.appendChild(renderer.domElement);
  const gl2 = renderer.capabilities.isWebGL2;
  const scene = new T3.Scene();
  const K_PX = H / 9;                                  // px por unidade Manim

  // ── ambiente azul-espacial (softbox branca em cima, faixa fria ciano à esquerda, reflexo magenta baixo no horizonte) ──
  {
    const s = new T3.Scene();
    const g = new T3.SphereGeometry(50, 64, 32), cor = [], pos = g.attributes.position;
    const c0 = lin('#081230'), c1 = lin('#1B3263');
    for (let i = 0; i < pos.count; i++) { const u = cl((pos.getZ(i) / 50 + 0.3) / 1.3, 0, 1); const c = c0.clone().lerp(c1, u); cor.push(c.r, c.g, c.b); }
    g.setAttribute('color', new T3.Float32BufferAttribute(cor, 3));
    s.add(new T3.Mesh(g, new T3.MeshBasicMaterial({ vertexColors: true, side: T3.BackSide })));
    const painel = (w, h, hex, int, x, y, z) => {
      const m = new T3.Mesh(new T3.PlaneGeometry(w, h), new T3.MeshBasicMaterial({ color: lin(hex).multiplyScalar(int), side: T3.DoubleSide }));
      m.position.set(x, y, z); m.lookAt(0, 0, 0); s.add(m);
    };
    painel(34, 34, '#F5F7FF', 0.42, 18, 24, 32);        // softbox grande em cima (fora do zênite: a vista de cima reflete o céu escuro)
    painel(10, 40, '#35D9FF', 1.6, -38, 0, 14);        // faixa fria à esquerda
    painel(60, 5, '#EA63FF', 0.9, 0, 40, 2);           // magenta baixo no horizonte
    painel(60, 5, '#EA63FF', 0.5, 0, -40, 2);
    scene.environment = new T3.PMREMGenerator(renderer).fromScene(s, 0.02).texture;
  }

  // ── luzes: chave (cima à direita) e contraluz fria, presas à câmera; sol de cima só para a sombra de contato ──
  const chave = new T3.DirectionalLight(0xffffff, 2.2), contra = new T3.DirectionalLight(lin('#8CC8FF'), 1.2);
  const alvoL = new T3.Object3D(); scene.add(alvoL); chave.target = alvoL; contra.target = alvoL;
  const sol = new T3.DirectionalLight(0xffffff, 0.35);
  sol.position.set(1.4, -1.1, 2.2); sol.castShadow = true;
  sol.shadow.mapSize.set(2048, 2048); sol.shadow.radius = 3; sol.shadow.bias = -0.0004; sol.shadow.normalBias = 0.0015;
  Object.assign(sol.shadow.camera, { left: -1.6, right: 1.6, top: 1.6, bottom: -1.6, near: .1, far: 7 });
  scene.add(chave, contra, sol, sol.target, new T3.AmbientLight(0xffffff, 0.06));

