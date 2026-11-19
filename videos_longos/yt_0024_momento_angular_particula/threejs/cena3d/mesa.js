// yt_0024 v2 — cena 'mesa_furo' (Three.js r128), "laboratório Parallax" (handoff v2 §2.1). Dirigida por ESTADO (window.setEstado(e)).
// Tampo de compósito preto-azulado fosco (1,60 × 1,60 × 0,05 m) com grade polar gravada (anéis a cada 0,10 m, raios a cada 15°; 0,30 e
// 0,60 mais marcados, com cota gravada), micro-furos de ar a cada 4 cm (brilho interno fraco; mais forte perto do disco, some em 0,3 s),
// borda de alumínio usinado com faixa de LED ciano → magenta (sem bloom), dois cavaletes em A (centro livre), tubo-guia de vidro sob o
// furo, bucha de aço com anel emissivo frio, disco de aço escuro (r 4,5 cm, h 2 cm) com anel de LED rosa, fio 1,8 mm com emissivo 15 %,
// rastro de 6 mm, chão escuro com reflexo de 8 % (desfocado) só na vista baixa. Origem no centro do furo, tampo em z = 0, z para cima (m).
// Campos do estado: cam, disco [x,y], fio, zp, pinos [[x,y]...], pinosLuz [k...], aneis {r30, r60} (0..1), furoLuz (×), rastro [[x,y]...],
//   bloom, desf, pontos [[x,y,z]...]. Devolve os pontos projetados (px) para o QA de alinhamento 3D × Manim.
(function () {
  const { T3, PI, W, H, cl, lin, renderer, scene, fis, canvas, normalDe } = B3;
  B3.ambiente({ caixa: 17, int: 0.19 });
  const brilho = B3.brilho;
  const mundo = new T3.Group(); scene.add(mundo);       // tudo o que reflete no chão

  // ── texturas do tampo (2048², 1,60 m): altura (sulcos e furos), cor (vinheta 10 %), emissivo (tinta GEO + furos azuis) ──
  const TAM = 2048, LADO = 1.60, L2 = LADO / 2;
  const px = m => (m / LADO + 0.5) * TAM, py = m => (0.5 - m / LADO) * TAM, mpx = m => m / LADO * TAM;
  const GEO = lin('#B8C4DA'), AZ = lin('#7FB2FF');
  const rgbLin = (c, k) => `rgb(${Math.round(255 * cl(c.r * k, 0, 1))},${Math.round(255 * cl(c.g * k, 0, 1))},${Math.round(255 * cl(c.b * k, 0, 1))})`;
  const EM_ESC = 0.2;                                   // emissivo do tampo gravado em escala 1/0,12 (precisão de 8 bits)
  let tampoMesh = null;
  const furos = [];
  for (let i = -19; i <= 19; i++) for (let j = -19; j <= 19; j++) {
    const X = i * 0.04, Y = j * 0.04;
    if (Math.hypot(X, Y) < 0.055 || Math.abs(X) > 0.75 || Math.abs(Y) > 0.75) continue;
    furos.push([X, Y]);
  }
  const grade = (g, larg, f) => {                       // anéis a cada 0,10 m e raios a cada 15°, recortados no quadrado de 0,77 m
    g.save(); g.beginPath(); g.rect(px(-0.77), py(0.77), mpx(1.54), mpx(1.54)); g.clip();
    for (let k = 1; k <= 10; k++) { const r = 0.1 * k; f(r); g.lineWidth = mpx(larg * (k === 3 || k === 6 ? 1.6 : 1)); g.beginPath(); g.arc(px(0), py(0), mpx(r), 0, 2 * PI); g.stroke(); }
    f(0); g.lineWidth = mpx(larg);
    for (let k = 0; k < 24; k++) { const a = k * PI / 12; g.beginPath(); g.moveTo(px(0.035 * Math.cos(a)), py(0.035 * Math.sin(a))); g.lineTo(px(1.2 * Math.cos(a)), py(1.2 * Math.sin(a))); g.stroke(); }
    g.restore();
  };
  const cAlt = canvas(TAM, TAM, g => {
    g.fillStyle = '#fff'; g.fillRect(0, 0, TAM, TAM);
    g.strokeStyle = '#555'; grade(g, 0.0016, () => {});
    g.fillStyle = '#000'; for (const [X, Y] of furos) { g.beginPath(); g.arc(px(X), py(Y), mpx(0.0011), 0, 2 * PI); g.fill(); }
    g.font = `${Math.round(mpx(0.020))}px Arial`; g.fillStyle = '#666';
  });
  const cCor = canvas(TAM, TAM, g => {
    const rg = g.createRadialGradient(px(0), py(0), mpx(0.2), px(0), py(0), mpx(1.1));
    rg.addColorStop(0, '#ffffff'); rg.addColorStop(1, '#e6e6e6'); g.fillStyle = rg; g.fillRect(0, 0, TAM, TAM);   // vinheta interna 10 %
    g.strokeStyle = '#9a9a9a'; grade(g, 0.0016, () => {});
    g.fillStyle = '#000'; for (const [X, Y] of furos) { g.beginPath(); g.arc(px(X), py(Y), mpx(0.0011), 0, 2 * PI); g.fill(); }
  });
  const cEm = canvas(TAM, TAM, g => {
    g.fillStyle = '#000'; g.fillRect(0, 0, TAM, TAM);
    grade(g, 0.0011, r => { g.strokeStyle = rgbLin(GEO, (r === 0.3 || r === 0.6 ? 0.30 : 0.11) / EM_ESC); });
    g.fillStyle = rgbLin(GEO, 0.16 / EM_ESC); g.font = `${Math.round(mpx(0.020))}px Arial`;
    g.fillStyle = rgbLin(AZ, 0.030 / EM_ESC); for (const [X, Y] of furos) { g.beginPath(); g.arc(px(X), py(Y), mpx(0.0009), 0, 2 * PI); g.fill(); }
  });
  // v5: variante do tampo SEM a grade gravada (a B2 desenha todas as grades como camada móvel, centradas no pino ativo)
  const cAlt0 = canvas(TAM, TAM, g => { g.fillStyle = '#fff'; g.fillRect(0, 0, TAM, TAM); g.fillStyle = '#000'; for (const [X, Y] of furos) { g.beginPath(); g.arc(px(X), py(Y), mpx(0.0011), 0, 2 * PI); g.fill(); } });
  const cCor0 = canvas(TAM, TAM, g => {
    const rg = g.createRadialGradient(px(0), py(0), mpx(0.2), px(0), py(0), mpx(1.1));
    rg.addColorStop(0, '#ffffff'); rg.addColorStop(1, '#e6e6e6'); g.fillStyle = rg; g.fillRect(0, 0, TAM, TAM);
    g.fillStyle = '#000'; for (const [X, Y] of furos) { g.beginPath(); g.arc(px(X), py(Y), mpx(0.0011), 0, 2 * PI); g.fill(); }
  });
  const cEm0 = canvas(TAM, TAM, g => {
    g.fillStyle = '#000'; g.fillRect(0, 0, TAM, TAM);
    g.fillStyle = rgbLin(AZ, 0.030 / EM_ESC); for (const [X, Y] of furos) { g.beginPath(); g.arc(px(X), py(Y), mpx(0.0009), 0, 2 * PI); g.fill(); }
  });
  const cFuros = canvas(1024, 1024, g => {                // só os furos (para o "sopro" perto do disco)
    g.fillStyle = '#000'; g.fillRect(0, 0, 1024, 1024); g.fillStyle = '#fff';
    for (const [X, Y] of furos) { g.beginPath(); g.arc((X / LADO + 0.5) * 1024, (0.5 - Y / LADO) * 1024, 1.6, 0, 2 * PI); g.fill(); }
  });
  const tx = (c, enc) => { const t = new T3.CanvasTexture(c); t.wrapS = t.wrapT = T3.ClampToEdgeWrapping; t.repeat.set(1 / LADO, 1 / LADO); t.offset.set(0.5, 0.5); t.anisotropy = 8; t.encoding = enc || T3.LinearEncoding; return t; };

  // ── materiais ──
  const mTampo = fis('#141B2A', 0.35, 0.55, 0.25, { map: tx(cCor), normalMap: tx(normalDe(cAlt, 3.0)), normalScale: new T3.Vector2(0.8, 0.8),
    emissive: new T3.Color(1, 1, 1), emissiveMap: tx(cEm), emissiveIntensity: EM_ESC, clearcoatRoughness: 0.3, envMapIntensity: 0.85 });
  const mTampo0 = fis('#141B2A', 0.35, 0.55, 0.25, { map: tx(cCor0), normalMap: tx(normalDe(cAlt0, 3.0)), normalScale: new T3.Vector2(0.8, 0.8),
    emissive: new T3.Color(1, 1, 1), emissiveMap: tx(cEm0), emissiveIntensity: EM_ESC, clearcoatRoughness: 0.3, envMapIntensity: 0.85 });
  const mAlu = fis('#7A8696', 0.92, 0.25, 0.2, { envMapIntensity: 0.8 });
  const mAluEsc = fis('#5C6676', 0.9, 0.38, 0.0, { envMapIntensity: 0.7 });
  const mBorracha = fis('#151820', 0.0, 0.9, 0.0);
  const mPolido = fis('#8A96A6', 0.95, 0.18, 0.5);
  const mDisco = fis('#2A303B', 0.9, 0.32, 0.4, { envMapIntensity: 0.9 });
  const mFio = new T3.MeshPhysicalMaterial({ color: lin('#F2EEE6'), metalness: 0.0, roughness: 0.8, emissive: lin('#F2EEE6'), emissiveIntensity: 0.15 });
  const mVidro = new T3.MeshPhysicalMaterial({ color: lin('#CFE6FF'), metalness: 0, roughness: 0.08, clearcoat: 1, clearcoatRoughness: 0.05, transparent: true, opacity: 0.20,
    envMapIntensity: 1.6, depthWrite: false, side: T3.DoubleSide });
  const mVazio = new T3.MeshBasicMaterial({ color: 0x000000 });

  // ── tampo com cantos arredondados (3 cm), chanfro de 4 mm e furo central; borda de alumínio com faixa de LED ──
  const raiz = new T3.Group(); mundo.add(raiz);
  const ESP = 0.05;
  const contorno = (() => {
    const rc = 0.03, sh = new T3.Shape();
    sh.moveTo(-L2 + rc, -L2); sh.lineTo(L2 - rc, -L2); sh.quadraticCurveTo(L2, -L2, L2, -L2 + rc); sh.lineTo(L2, L2 - rc); sh.quadraticCurveTo(L2, L2, L2 - rc, L2);
    sh.lineTo(-L2 + rc, L2); sh.quadraticCurveTo(-L2, L2, -L2, L2 - rc); sh.lineTo(-L2, -L2 + rc); sh.quadraticCurveTo(-L2, -L2, -L2 + rc, -L2);
    return sh;
  })();
  {
    const sh = contorno.clone ? contorno : contorno;
    const fu = new T3.Path(); fu.absarc(0, 0, 0.0095, 0, 2 * PI, true); sh.holes.push(fu);
    const g = new T3.ExtrudeGeometry(sh, { depth: ESP - 0.008, bevelEnabled: true, bevelThickness: 0.004, bevelSize: 0.004, bevelSegments: 3, curveSegments: 24 });
    const tampo = new T3.Mesh(g, [mTampo, mAlu]); tampoMesh = tampo;
    tampo.position.z = -(ESP - 0.004); tampo.receiveShadow = true; tampo.castShadow = true;
    raiz.add(tampo);
    // faixa de LED embutida no perfil: degradê ciano → magenta → ciano ao longo do perímetro, 35 % de luminância, fora do bloom
    const pts = contorno.getSpacedPoints(480), pos = [], cor = [], idx = [];
    const c1 = lin('#35D9FF'), c2 = lin('#EA63FF');
    for (let i = 0; i < pts.length; i++) {
      const p = pts[i], q = pts[(i + 1) % pts.length], u = i / (pts.length - 1);
      const k = 0.5 - 0.5 * Math.cos(2 * PI * u), c = c1.clone().lerp(c2, k).multiplyScalar(0.22);
      const d = Math.hypot(p.x, p.y), nx = p.x / d, ny = p.y / d, o = 0.0046;
      pos.push(p.x + nx * o, p.y + ny * o, -0.027, p.x + nx * o, p.y + ny * o, -0.021);
      cor.push(c.r, c.g, c.b, c.r, c.g, c.b);
      if (i < pts.length - 1) { const a = 2 * i; idx.push(a, a + 2, a + 1, a + 1, a + 2, a + 3); }
    }
    const gl = new T3.BufferGeometry(); gl.setAttribute('position', new T3.Float32BufferAttribute(pos, 3)); gl.setAttribute('color', new T3.Float32BufferAttribute(cor, 3)); gl.setIndex(idx);
    raiz.add(new T3.Mesh(gl, new T3.MeshBasicMaterial({ vertexColors: true, side: T3.DoubleSide })));
    // cavaletes em A (perfil de alumínio escovado), pé largo com sapatas de borracha; o centro embaixo do furo fica livre
    const viga = (x, y0, z0, y1, z1, s, mat) => {
      const L = Math.hypot(y1 - y0, z1 - z0), m = new T3.Mesh(new T3.BoxGeometry(s, L, s), mat);
      m.position.set(x, (y0 + y1) / 2, (z0 + z1) / 2); m.rotation.x = Math.atan2(z1 - z0, y1 - y0); m.castShadow = true; m.receiveShadow = true; raiz.add(m);
    };
    for (const sx of [-1, 1]) {
      const x = 0.60 * sx;
      viga(x, -0.62, -0.075, 0.62, -0.075, 0.045, mAlu);                         // travessa sob o tampo
      viga(x, -0.16, -0.10, -0.60, -0.80, 0.040, mAlu); viga(x, 0.16, -0.10, 0.60, -0.80, 0.040, mAlu);  // pernas do A
      viga(x, -0.37, -0.45, 0.37, -0.45, 0.030, mAluEsc);                        // barra do A
      viga(x, -0.70, -0.815, 0.70, -0.815, 0.050, mAluEsc);                      // pé largo
      for (const sy of [-1, 1]) { const s = new T3.Mesh(new T3.BoxGeometry(0.08, 0.10, 0.014), mBorracha); s.position.set(x, 0.66 * sy, -0.847); s.castShadow = true; raiz.add(s); }
    }
    // bucha de aço polido com anel emissivo frio (1,5 mm) na borda interna: o ponto O
    const perfil = [[0.0060, -0.050], [0.0060, 0.0024], [0.0068, 0.0030], [0.0112, 0.0030], [0.0120, 0.0022], [0.0120, 0.0], [0.0095, 0.0], [0.0095, -0.050]].map(p => new T3.Vector2(p[0], p[1]));
    const bucha = new T3.Mesh(new T3.LatheGeometry(perfil, 64), mPolido);
    bucha.rotation.x = PI / 2; bucha.castShadow = true; bucha.receiveShadow = true; raiz.add(bucha);
    const vazio = new T3.Mesh(new T3.CircleGeometry(0.0061, 48), mVazio); vazio.position.z = -0.004; raiz.add(vazio);
    // tubo-guia de vidro (r 2 cm, 0,35 m) sob o furo, com anéis de aço nas bocas
    const tubo = new T3.Mesh(new T3.CylinderGeometry(0.02, 0.02, 0.35, 48, 1, true), mVidro); tubo.rotation.x = PI / 2; tubo.position.z = -0.055 - 0.175; tubo.renderOrder = 6; raiz.add(tubo);
    for (const z of [-0.058, -0.402]) { const a = new T3.Mesh(new T3.TorusGeometry(0.0205, 0.0028, 12, 48), mPolido); a.position.z = z; raiz.add(a); }
  }
  const mAnelO = new T3.MeshBasicMaterial({ color: lin('#BFE6FF').multiplyScalar(1.6) });
  const anelO = new T3.Mesh(new T3.TorusGeometry(0.0064, 0.00075, 12, 72), mAnelO); anelO.position.z = 0.0026; mundo.add(anelO); brilho.push(anelO);
  // anéis de 0,30 m e 0,60 m que acendem (B6-2)
  const aneisLuz = {};
  for (const [k, r] of [['r30', 0.30], ['r60', 0.60]]) {
    const m = new T3.Mesh(new T3.RingGeometry(r - 0.0018, r + 0.0018, 256), new T3.MeshBasicMaterial({ color: lin('#B8C4DA').multiplyScalar(1.4), transparent: true, opacity: 0, depthWrite: false }));
    m.position.z = 0.0006; m.renderOrder = 3; mundo.add(m); brilho.push(m); aneisLuz[k] = m;
  }
  // "sopro" dos micro-furos perto do disco: 6 manchas aditivas nos últimos 0,3 s da trajetória
  const mkSopro = () => new T3.ShaderMaterial({
    uniforms: { t: { value: new T3.CanvasTexture(cFuros) }, c: { value: new T3.Vector2() }, k: { value: 0 } }, transparent: true, depthWrite: false, blending: T3.AdditiveBlending,
    vertexShader: 'varying vec2 vP; void main(){ vec4 w = modelMatrix * vec4(position,1.0); vP = w.xy; gl_Position = projectionMatrix * viewMatrix * w; }',
    fragmentShader: `uniform sampler2D t; uniform vec2 c; uniform float k; varying vec2 vP;
      void main(){ float d = length(vP - c); float f = k * (1.0 - smoothstep(0.045, 0.075, d)) * step(0.040, d);
        float h = texture2D(t, vec2(vP.x / ${LADO.toFixed(2)} + 0.5, vP.y / ${LADO.toFixed(2)} + 0.5)).r;
        gl_FragColor = vec4(vec3(0.50, 0.70, 1.0) * h * f, 1.0); }` });
  const sopros = [];
  for (let i = 0; i < 6; i++) { const m = new T3.Mesh(new T3.PlaneGeometry(0.16, 0.16), mkSopro()); m.position.z = 0.0004; m.renderOrder = 2; mundo.add(m); sopros.push(m); brilho.push(m); }

  // ── chão escuro com reflexo de 8 % desfocado (só na vista baixa) + sombra dos cavaletes ──
  const ZCH = -0.854;
  const sombraChao = new T3.Mesh(new T3.PlaneGeometry(7, 7), new T3.ShadowMaterial({ opacity: 0.35 }));
  sombraChao.position.z = ZCH + 0.0005; sombraChao.receiveShadow = true; scene.add(sombraChao);
  const rtRef = new T3.WebGLRenderTarget(W / 3, H / 3, { type: T3.HalfFloatType, minFilter: T3.LinearFilter, magFilter: T3.LinearFilter });
  const chao = new T3.Mesh(new T3.PlaneGeometry(7, 7), new T3.ShaderMaterial({
    uniforms: { ref: { value: rtRef.texture }, res: { value: new T3.Vector2(W, H) }, k: { value: 0.08 } }, transparent: true, depthWrite: false,
    vertexShader: 'varying vec2 vP; void main(){ vec4 w = modelMatrix * vec4(position,1.0); vP = w.xy; gl_Position = projectionMatrix * viewMatrix * w; }',
    fragmentShader: `uniform sampler2D ref; uniform vec2 res; uniform float k; varying vec2 vP;
      void main(){ float r = length(vP); float a = 0.62 * (1.0 - smoothstep(0.7, 2.2, r));
        vec4 R = texture2D(ref, gl_FragCoord.xy / res);
        vec3 c = vec3(0.004, 0.006, 0.012) + R.rgb * k * (1.0 - smoothstep(0.6, 1.8, r));
        gl_FragColor = vec4(c * a, a); }`,
    blending: T3.CustomBlending, blendSrc: T3.OneFactor, blendDst: T3.OneMinusSrcAlphaFactor }));
  chao.position.z = ZCH; chao.renderOrder = -1; scene.add(chao);

  // ── disco: r 4,5 cm, h 2 cm, aço escuro, anel de LED rosa no topo, ponto branco no centro, sombra de contato ──
  const Z0 = 0.0012, HD = 0.020, RD = 0.045;
  const disco = new T3.Group(); mundo.add(disco);
  {
    const corpo = new T3.Mesh(new T3.CylinderGeometry(RD, RD * 0.985, HD, 72), mDisco); corpo.rotation.x = PI / 2; corpo.position.z = Z0 + HD / 2; corpo.castShadow = true;
    const chanf = new T3.Mesh(new T3.TorusGeometry(RD - 0.001, 0.0012, 10, 72), mPolido); chanf.position.z = Z0 + HD;
    const led = new T3.Mesh(new T3.RingGeometry(RD - 0.0105, RD - 0.0050, 96), new T3.MeshBasicMaterial({ color: lin('#FF7EB6').multiplyScalar(1.25) }));
    led.position.z = Z0 + HD + 0.0003; brilho.push(led);
    const sulco = new T3.Mesh(new T3.RingGeometry(RD - 0.0125, RD - 0.0105, 96), new T3.MeshBasicMaterial({ color: 0x05070c })); sulco.position.z = Z0 + HD + 0.0002;
    const ponto = new T3.Mesh(new T3.CircleGeometry(0.0042, 32), new T3.MeshBasicMaterial({ color: lin('#F5F7FF').multiplyScalar(1.1) })); ponto.position.z = Z0 + HD + 0.0004; brilho.push(ponto);
    const cs = canvas(128, 128, g => { const rg = g.createRadialGradient(64, 64, 0, 64, 64, 64); rg.addColorStop(0, 'rgba(0,0,0,0.95)'); rg.addColorStop(0.6, 'rgba(0,0,0,0.85)'); rg.addColorStop(0.8, 'rgba(0,0,0,0.35)'); rg.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = rg; g.fillRect(0, 0, 128, 128); });
    const somb = new T3.Mesh(new T3.PlaneGeometry(RD * 2.8, RD * 2.8), new T3.MeshBasicMaterial({ map: new T3.CanvasTexture(cs), transparent: true, depthWrite: false }));
    somb.position.set(0.004, -0.003, 0.0005); somb.renderOrder = 2;
    disco.add(corpo, chanf, led, sulco, ponto, somb);
  }
  // ── fio (1,8 mm, branco-quente com emissivo 15 %): horizontal rente ao tampo e vertical pela bucha e pelo tubo até o puxador ──
  const ZF = 0.010, RF = 0.0024;
  const fioH = new T3.Mesh(new T3.CylinderGeometry(RF, RF, 1, 12), mFio); fioH.castShadow = true;
  const fioV = new T3.Mesh(new T3.CylinderGeometry(RF, RF, 1, 12), mFio); fioV.rotation.x = PI / 2;
  mundo.add(fioH, fioV);
  // ── puxador em T (sai pela boca de baixo do tubo); topo da haste em z = −0,45 + zp ──
  const pux = new T3.Group(); mundo.add(pux);
  {
    const haste = new T3.Mesh(new T3.CylinderGeometry(0.005, 0.005, 0.06, 20), mPolido); haste.rotation.x = PI / 2; haste.position.z = -0.03; haste.castShadow = true;
    const barra = new T3.Mesh(new T3.CylinderGeometry(0.0085, 0.0085, 0.13, 24), mPolido); barra.rotation.z = PI / 2; barra.position.z = -0.06 - 0.0085; barra.castShadow = true;
    const ponta = (s) => { const m = new T3.Mesh(new T3.CylinderGeometry(0.0105, 0.0105, 0.025, 24), mBorracha); m.rotation.z = PI / 2; m.position.set(0.065 * s, 0, -0.06 - 0.0085); return m; };
    const olhal = new T3.Mesh(new T3.TorusGeometry(0.004, 0.0013, 10, 24), mPolido); olhal.rotation.x = PI / 2; olhal.position.z = 0.002;
    pux.add(haste, barra, ponta(1), ponta(-1), olhal);
  }
  // ── pinos O1, O2, O3 (B2): haste + topo esférico + anel que acende na cor do L ──
  const pinos = [];
  for (let k = 0; k < 3; k++) {
    const g = new T3.Group();
    const h = new T3.Mesh(new T3.CylinderGeometry(0.003, 0.003, 0.012, 16), mPolido); h.rotation.x = PI / 2; h.position.z = 0.006;
    const b = new T3.Mesh(new T3.SphereGeometry(0.009, 32, 16), mPolido); b.position.z = 0.014; b.castShadow = true;
    const anel = new T3.Mesh(new T3.RingGeometry(0.014, 0.019, 64), new T3.MeshBasicMaterial({ color: lin('#F19AFF').multiplyScalar(1.3), transparent: true, opacity: 0, depthWrite: false }));
    anel.position.z = 0.0007; brilho.push(anel);
    g.add(h, b, anel); g.visible = false; g.userData.anel = anel; mundo.add(g); pinos.push(g);
  }
  // ── v5 (ajuste 4): grade polar móvel, centrada num pino (B2). Camada aditiva na cor GEO, recortada ao tampo (±0,77 m); o estado traz
  //    grades [[x, y, op], ...] (até 2, para o crossfade de 0,5 s entre referências) e gradeBase (0..1: escala da grade gravada no furo). ──
  const gradeMoveis = [];
  {
    const GR = 1.95, TG = 4096, pg = m => (m / (2 * GR) + 0.5) * TG, mg = m => m / (2 * GR) * TG;
    const cG = canvas(TG, TG, g => {
      g.fillStyle = '#000'; g.fillRect(0, 0, TG, TG);
      for (let k = 1; k <= 19; k++) {
        const r = 0.1 * k, v = (k === 3 || k === 6) ? 0.30 : 0.11, c = Math.round(255 * v);
        g.strokeStyle = `rgb(${c},${c},${c})`; g.lineWidth = mg(0.0011 * (k === 3 || k === 6 ? 1.6 : 1)); g.beginPath(); g.arc(pg(0), pg(0), mg(r), 0, 2 * PI); g.stroke();
      }
      const c = Math.round(255 * 0.11); g.strokeStyle = `rgb(${c},${c},${c})`; g.lineWidth = mg(0.0011);
      for (let k = 0; k < 24; k++) { const a = k * PI / 12; g.beginPath(); g.moveTo(pg(0.035 * Math.cos(a)), pg(-0.035 * Math.sin(a))); g.lineTo(pg(1.9 * Math.cos(a)), pg(-1.9 * Math.sin(a))); g.stroke(); }
    });
    const tG = new T3.CanvasTexture(cG); tG.anisotropy = 8; tG.encoding = T3.LinearEncoding;
    renderer.localClippingEnabled = true;
    const cp = [new T3.Plane(new T3.Vector3(1, 0, 0), 0.77), new T3.Plane(new T3.Vector3(-1, 0, 0), 0.77), new T3.Plane(new T3.Vector3(0, 1, 0), 0.77), new T3.Plane(new T3.Vector3(0, -1, 0), 0.77)];
    for (let i = 0; i < 2; i++) {
      const m = new T3.Mesh(new T3.PlaneGeometry(2 * GR, 2 * GR), new T3.MeshBasicMaterial({ map: tG, color: GEO.clone().multiplyScalar(1.0), transparent: true, opacity: 0, blending: T3.AdditiveBlending,
        depthWrite: false, clippingPlanes: cp, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 }));
      m.position.z = 0.0002; m.visible = false; m.renderOrder = 2; mundo.add(m); gradeMoveis.push(m);
    }
  }
  // ── rastro: fita de 6 mm no plano do tampo, cauda na cor RAST que some, cabeça (últimos 6 cm) em HDR com bloom ──
  const NR = 160, rastroGeo = new T3.BufferGeometry();
  rastroGeo.setAttribute('position', new T3.BufferAttribute(new Float32Array(NR * 2 * 3), 3));
  rastroGeo.setAttribute('color', new T3.BufferAttribute(new Float32Array(NR * 2 * 4), 4));
  { const id = []; for (let i = 0; i < NR - 1; i++) { const a = 2 * i; id.push(a, a + 1, a + 2, a + 1, a + 3, a + 2); } rastroGeo.setIndex(id); }
  const mRastro = new T3.ShaderMaterial({
    transparent: true, depthWrite: false,
    vertexShader: 'attribute vec4 color; varying vec4 vC; void main(){ vC = color; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
    fragmentShader: 'varying vec4 vC; void main(){ gl_FragColor = vec4(vC.rgb * vC.a, vC.a); }',
    blending: T3.CustomBlending, blendSrc: T3.OneFactor, blendDst: T3.OneMinusSrcAlphaFactor,
  });
  const rastro = new T3.Mesh(rastroGeo, mRastro); rastro.frustumCulled = false; rastro.renderOrder = 5; mundo.add(rastro); brilho.push(rastro);
  const cRast = lin('#9FB4D6');
  function poeRastro(pts) {
    const n = pts ? pts.length : 0; rastro.visible = n > 1;
    sopros.forEach(m => { m.visible = false; });
    if (n < 2) return;
    const P = rastroGeo.attributes.position.array, C = rastroGeo.attributes.color.array;
    const s = [0]; for (let i = 1; i < n; i++) s.push(s[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
    const tot = s[n - 1], w = 0.003;
    for (let i = 0; i < NR; i++) {
      const k = Math.min(n - 1, i), a = pts[Math.max(0, k - 1)], b = pts[Math.min(n - 1, k + 1)];
      let tx_ = b[0] - a[0], ty = b[1] - a[1]; const l = Math.hypot(tx_, ty) || 1; tx_ /= l; ty /= l;
      const p = pts[k], u = k / (n - 1), dFim = tot - s[k];
      const cab = dFim < 0.06 ? 1 + 0.7 * (1 - dFim / 0.06) : 1;
      const al = cl(u, 0, 1) * (i < n ? 1 : 0) * 0.68;
      for (let q = 0; q < 2; q++) {
        const sg = q ? -1 : 1, o = (2 * i + q);
        P[3 * o] = p[0] - ty * w * sg; P[3 * o + 1] = p[1] + tx_ * w * sg; P[3 * o + 2] = 0.0009;
        C[4 * o] = cRast.r * cab; C[4 * o + 1] = cRast.g * cab; C[4 * o + 2] = cRast.b * cab; C[4 * o + 3] = al;
      }
    }
    rastroGeo.attributes.position.needsUpdate = true; rastroGeo.attributes.color.needsUpdate = true;
    // sopro: os últimos 0,3 s (1/3 da cauda de 0,9 s), do mais forte (agora) ao mais fraco
    if (tot > 0.01) for (let i = 0; i < 6; i++) {
      const k = Math.max(0, Math.round((n - 1) * (1 - i / 6 / 3))), m = sopros[i];
      m.visible = true; m.position.set(pts[k][0], pts[k][1], 0.0004); m.material.uniforms.c.value.set(pts[k][0], pts[k][1]);
      m.material.uniforms.k.value = 0.10 * (1 - i / 6);
    }
  }

  window.setEstado = function (e) {
    const cam = B3.posicionaCamera(e.cam);
    if (e.solT !== undefined) {     // v3 §4 PARADO: o sol das sombras deriva devagar (±20°, período 16 s): luz e sombra do tampo nunca ficam congeladas
      const ang = 0.35 * Math.sin(e.solT * 0.39);
      B3.sol.position.set(Math.cos(ang) + 0.8 * Math.sin(ang), -0.8 * Math.cos(ang) + Math.sin(ang), 2.6);
    }
    const baixa = e.cam.el < 30;
    chao.visible = baixa; sombraChao.visible = e.cam.el < 50;
    const temD = !!e.disco;
    disco.visible = temD;
    if (temD) disco.position.set(e.disco[0], e.disco[1], 0);
    const fio = temD && e.fio !== false;
    fioH.visible = fio; fioV.visible = pux.visible = e.fio !== false;
    const zp = -0.45 + (e.zp || 0);
    pux.position.set(0, 0, zp);
    if (fio) {
      const dx = e.disco[0], dy = e.disco[1], L = Math.hypot(dx, dy);
      fioH.scale.set(1, L, 1); fioH.position.set(dx / 2, dy / 2, ZF); fioH.rotation.set(0, 0, Math.atan2(dy, dx) - PI / 2);
    }
    fioV.scale.set(1, ZF - zp, 1); fioV.position.set(0, 0, (ZF + zp) / 2);
    pinos.forEach((p, k) => { const q = (e.pinos || [])[k]; p.visible = !!q; if (q) p.position.set(q[0], q[1], 0); p.userData.anel.material.opacity = cl(((e.pinosLuz || [])[k] || 0), 0, 1); });
    tampoMesh.material[0] = (e.grades !== undefined) ? mTampo0 : mTampo;      // v5: com `grades` no estado, o tampo vai sem a grade gravada
    gradeMoveis.forEach((m, k) => { const q = (e.grades || [])[k]; m.visible = !!q && q[2] > 0.003; if (q) { m.position.set(q[0], q[1], 0.0002); m.material.opacity = cl(q[2], 0, 1); } });
    for (const k in aneisLuz) { const v = cl(((e.aneis || {})[k] || 0), 0, 1); aneisLuz[k].visible = v > 0.003; aneisLuz[k].material.opacity = 0.85 * v; }
    mAnelO.color.copy(lin('#BFE6FF').multiplyScalar(1.6 * (e.furoLuz === undefined ? 1 : e.furoLuz)));
    poeRastro(e.rastro);
    B3.render(e, {
      esconderNoBrilho: [chao, sombraChao],
      antes: () => {
        if (!baixa) return;
        // reflexo: o mundo espelhado no plano do chão, renderizado pela mesma câmera em 1/3 da resolução (desfoque natural)
        chao.visible = false; sombraChao.visible = false;
        mundo.scale.z = -1; mundo.position.z = 2 * ZCH;
        const sm = renderer.shadowMap.enabled; renderer.shadowMap.enabled = false;
        renderer.setRenderTarget(rtRef); renderer.setClearColor(0x000000, 0); renderer.clear(); renderer.render(scene, B3.cam);
        renderer.shadowMap.enabled = sm;
        mundo.scale.z = 1; mundo.position.z = 0; chao.visible = true; sombraChao.visible = true;
      },
    });
    const pr = B3.projeta;
    const p = { O: pr([0, 0, 0]), webgl2: B3.gl2 };
    if (temD) { p.disco = pr([e.disco[0], e.disco[1], 0]); p.disco_topo = pr([e.disco[0], e.disco[1], Z0 + HD]); }
    p.pux = pr([0, 0, zp]);
    (e.pontos || []).forEach((q, k) => { p['q' + k] = pr(q); });
    return p;
  };
  window.projeta = B3.projeta;
  window.medidas = () => ({ webgl2: B3.gl2, W, H });
  window.cenaPronta = true;
})();
