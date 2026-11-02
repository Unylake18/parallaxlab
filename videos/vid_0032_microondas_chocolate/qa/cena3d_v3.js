// vid_0032 v2 — forno de micro-ondas 3D (C01 gancho; C05/C06 relevo de calor e gotas), Three.js r128.
// Tudo é função do quadro: window.setFrame(f). Unidade do mundo = 1 cm, z para cima, frente do forno em y negativo.
// Cavidade: x ∈ ±18,3 (36,6 = 3λ), y ∈ ±15,5, z ∈ [0, 22]. Corpo: timeline.geometria.corpo_cm.
// window.TIMELINE (timeline.json), window.FPS e window.CAMPO (campo.json) são injetados pelo render3d.js.
(function () {
  const TL = window.TIMELINE, FPS = window.FPS || 15, G = TL.geometria, E = TL.eventos, CAMPO = window.CAMPO;
  const [CW, CD, CH] = G.cavidade_cm, B = G.barra, P = G.prato, CO = G.corpo_cm, F = G.fita;
  const W = innerWidth, H = innerHeight, PI = Math.PI;
  const cor = h => new THREE.Color(h).convertSRGBToLinear();
  const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
  const suave = u => u * u * (3 - 2 * u);
  const rampa = (t, t0, dur) => suave(clamp((t - t0) / dur, 0, 1));
  const passo = (a, b, x) => suave(clamp((x - a) / (b - a), 0, 1));

  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H); renderer.setClearColor(0x050816, 1);
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 0.9;
  renderer.outputEncoding = THREE.sRGBEncoding; renderer.physicallyCorrectLights = true;
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  document.body.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new THREE.RoomEnvironment(), 0.04).texture;
  // Luz: nenhuma pontual no quadro. Principal direcional (cima-frente-esquerda, sombra suave) + hemisfério fraco.
  const sol = new THREE.DirectionalLight(0xffffff, 1.5);
  sol.position.set(-30, -45, 90); sol.target.position.set(0, 0, 0);
  sol.castShadow = true; sol.shadow.mapSize.set(2048, 2048); sol.shadow.bias = -0.0004; sol.shadow.radius = 4;
  Object.assign(sol.shadow.camera, { left: -32, right: 32, top: 32, bottom: -32, near: 20, far: 200 });
  const hemi = new THREE.HemisphereLight(0xDDE6F5, 0x2A2F3A, 0.45); hemi.position.set(0, 0, 1);
  scene.add(sol, sol.target, hemi);

  // ---------- texturas procedurais (canvas, sem nada aleatório sem semente) ----------
  let semente = 32;
  const rnd = () => (semente = (semente * 1664525 + 1013904223) >>> 0) / 4294967296;
  function canvasTex(w, h, desenha, srgb) {
    const c = document.createElement('canvas'); c.width = w; c.height = h;
    desenha(c.getContext('2d'), w, h);
    const t = new THREE.CanvasTexture(c); t.anisotropy = 8;
    if (srgb) t.encoding = THREE.sRGBEncoding;
    return t;
  }
  // Tela perfurada da porta: furos de 1,5 mm em grade hexagonal (alphaMap: branco = metal, preto = furo).
  const telaTex = canvasTex(128, 128 * Math.sqrt(3) | 0, (g, w, h) => {
    g.fillStyle = '#fff'; g.fillRect(0, 0, w, h); g.fillStyle = '#000';
    const p = w / 4;
    for (let j = 0; j <= 8; j++) for (let i = -1; i <= 4; i++) {
      g.beginPath(); g.arc((i + (j % 2) / 2) * p, j * p * Math.sqrt(3) / 2, p * 0.3, 0, 2 * PI); g.fill();
    }
  });
  telaTex.wrapS = telaTex.wrapT = THREE.RepeatWrapping;
  // Ruído fino de normal para o chocolate não ficar plástico.
  const ruidoTex = canvasTex(256, 256, (g, w, h) => {
    const alt = new Float32Array(w * h).map(() => rnd());
    const img = g.createImageData(w, h);
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const a = k => alt[((y + h) % h) * w + ((k + w) % w)], b = k => alt[((k + h) % h) * w + x];
      const dx = a(x + 1) - a(x - 1), dy = b(y + 1) - b(y - 1), i = 4 * (y * w + x);
      img.data[i] = 128 + 60 * dx; img.data[i + 1] = 128 + 60 * dy; img.data[i + 2] = 255; img.data[i + 3] = 255;
    }
    g.putImageData(img, 0, 0);
  });
  ruidoTex.wrapS = ruidoTex.wrapT = THREE.RepeatWrapping; ruidoTex.repeat.set(6, 2);
  // Etiqueta do batente: branca, texto preto "2450 MHz", sem marca.
  const etqTex = canvasTex(440, 240, (g, w, h) => {
    g.fillStyle = '#F4F4F0'; g.fillRect(0, 0, w, h);
    g.strokeStyle = '#111'; g.lineWidth = 6; g.strokeRect(10, 10, w - 20, h - 20);
    g.fillStyle = '#111'; g.font = 'bold 92px Arial'; g.textAlign = 'center'; g.textBaseline = 'middle';
    g.fillText('2450 MHz', w / 2, h / 2 - 18);
    g.fillStyle = '#9A9A9A';
    for (let k = 0; k < 2; k++) g.fillRect(70, 170 + k * 22, w - 140 - k * 90, 9);
  }, true);

  // ---------- materiais ----------
  const matCav = new THREE.MeshStandardMaterial({ color: cor('#9AA4B2'), roughness: 0.7, metalness: 0.2, envMapIntensity: 0.25, side: THREE.DoubleSide });
  const matGraf = new THREE.MeshStandardMaterial({ color: cor('#1C2129'), roughness: 0.35, metalness: 0.6, envMapIntensity: 1.6 });
  const matCorte = new THREE.MeshStandardMaterial({ color: cor('#3A424E'), roughness: 0.5, metalness: 0.4, envMapIntensity: 0.4, side: THREE.DoubleSide });
  const transp = m => { m.transparent = true; return m; };
  const plano = (w, h, mat) => new THREE.Mesh(new THREE.PlaneGeometry(w, h), mat);
  const recebe = m => { m.receiveShadow = true; return m; };
  const projeta = m => { m.castShadow = true; m.receiveShadow = true; return m; };

  // ---------- cavidade ----------
  const cav = new THREE.Group(); scene.add(cav);
  cav.add(recebe(plano(CW, CD, matCav)));                                                    // piso
  const fundo = recebe(plano(CW, CH, matCav)); fundo.rotation.x = PI / 2; fundo.position.set(0, CD / 2, CH / 2); cav.add(fundo);
  for (const s of [-1, 1]) {
    const lado = recebe(plano(CD, CH, matCav)); lado.rotation.set(PI / 2, s * PI / 2, 0); lado.position.set(s * CW / 2, 0, CH / 2); cav.add(lado);
  }
  const matTeto = transp(matCav.clone());
  const teto = plano(CW, CD, matTeto); teto.position.z = CH; scene.add(teto);
  // Lâmpada: só um pequeno painel emissivo no canto do teto (não ilumina, não gera mancha especular).
  const lampada = new THREE.Mesh(new THREE.PlaneGeometry(4, 2.5), transp(new THREE.MeshBasicMaterial({ color: cor('#FFE9C2'), side: THREE.DoubleSide })));
  lampada.position.set(-13, 11, CH - 0.05); scene.add(lampada);
  // Tampa do guia de onda (mica) na parede esquerda, com 2 parafusos.
  const mica = new THREE.Mesh(new THREE.PlaneGeometry(9, 7), new THREE.MeshStandardMaterial({ color: cor('#A9A49A'), roughness: 0.55,
    metalness: 0, transparent: true, opacity: 0.92, side: THREE.DoubleSide }));
  mica.rotation.set(PI / 2, PI / 2, 0); mica.position.set(-CW / 2 + 0.06, 3, 14); cav.add(mica);
  for (const dy of [-3.6, 3.6]) {
    const p = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.3, 0.2, 16), matCorte);
    p.rotation.z = PI / 2; p.position.set(-CW / 2 + 0.12, 3 + dy, 14); cav.add(p);
  }
  // Grade de ventilação na parede direita.
  const matFuro = new THREE.MeshBasicMaterial({ color: cor('#1A1F27'), side: THREE.DoubleSide });
  for (let i = 0; i < 7; i++) for (let j = 0; j < 5; j++) {
    const f = new THREE.Mesh(new THREE.CircleGeometry(0.3, 12), matFuro);
    f.rotation.y = PI / 2; f.position.set(CW / 2 - 0.06, 2 + i * 1.2, 12 + j * 1.2); cav.add(f);
  }

  // ---------- corpo por fora ----------
  const [x0, x1] = CO.x, [y0, y1] = CO.y, [z0, z1] = CO.z, YF = y0;          // YF: face da frente
  const invis = new THREE.MeshBasicMaterial({ visible: false });
  const matTopo = transp(matGraf.clone());
  function caixaCorpo(zt, topo) {                                            // caixa sem a face da frente
    const m = new THREE.Mesh(new THREE.BoxGeometry(x1 - x0, y1 - y0, zt - z0), [matGraf, matGraf, matGraf, invis, topo, matGraf]);
    m.position.set((x0 + x1) / 2, (y0 + y1) / 2, (z0 + zt) / 2); return m;
  }
  const corpo = caixaCorpo(z1, matTopo); scene.add(corpo);
  const naFrente = (shape, mat, y) => { const m = new THREE.Mesh(new THREE.ShapeGeometry(shape), mat); m.rotation.x = PI / 2; m.position.y = y; return m; };
  const ret = (a, b, c, d) => { const s = new THREE.Path(); s.moveTo(a, b); s.lineTo(c, b); s.lineTo(c, d); s.lineTo(a, d); s.lineTo(a, b); return s; };
  const fr = new THREE.Shape(); fr.moveTo(x0, z0); fr.lineTo(x1, z0); fr.lineTo(x1, z1); fr.lineTo(x0, z1); fr.lineTo(x0, z0);
  fr.holes.push(ret(-CW / 2, 0, CW / 2, CH));
  const matFrente = transp(matGraf.clone()); matFrente.side = THREE.DoubleSide;
  const frente = naFrente(fr, matFrente, YF); scene.add(frente);
  // Batente: faces entre a frente (y0) e a abertura da cavidade (−CD/2).
  const prof = -CD / 2 - YF, batente = new THREE.Group(); scene.add(batente);
  const matBat = transp(matCav.clone());
  for (const s of [-1, 1]) {
    const p = plano(prof, CH, matBat); p.rotation.set(PI / 2, PI / 2, 0); p.position.set(s * CW / 2, YF + prof / 2, CH / 2); batente.add(p);
  }
  const batPiso = plano(CW, prof, matBat); batPiso.position.set(0, YF + prof / 2, 0); batente.add(batPiso);
  const batTeto = plano(CW, prof, matBat); batTeto.position.set(0, YF + prof / 2, CH); batente.add(batTeto);
  // Etiqueta na frente, à direita da abertura (coberta pela porta quando fechada).
  const ETQ = G.etiqueta_cm;
  const etiqueta = new THREE.Mesh(new THREE.PlaneGeometry(...ETQ.tamanho), new THREE.MeshStandardMaterial({ map: etqTex, roughness: 0.8, metalness: 0, envMapIntensity: 0.2 }));
  etiqueta.rotation.x = PI / 2; etiqueta.position.set(ETQ.centro[0], YF - 0.03, ETQ.centro[1]); scene.add(etiqueta);
  // Painel de controle (display apagado, sem cronômetro) à direita.
  const XP = 23.5, painel = new THREE.Group(); scene.add(painel);
  const display = plano(4.4, 1.7, new THREE.MeshStandardMaterial({ color: cor('#06080B'), roughness: 0.15, metalness: 0.2 }));
  display.rotation.x = PI / 2; display.position.set((XP + x1) / 2, YF - 0.04, 19.5); painel.add(display);
  for (let k = 0; k < 6; k++) {
    const b = new THREE.Mesh(new THREE.CylinderGeometry(0.6, 0.6, 0.3, 24), matCorte);
    b.position.set((XP + x1) / 2 + (k % 2 ? 1.2 : -1.2), YF - 0.15, 14.5 - Math.floor(k / 2) * 2.2); painel.add(b);
  }
  const botao = new THREE.Mesh(new THREE.BoxGeometry(4, 0.4, 1.4), matCorte); botao.position.set((XP + x1) / 2, YF - 0.2, 4); painel.add(botao);
  // Porta: dobradiça à esquerda; vidro escuro + tela perfurada; puxador.
  const porta = new THREE.Group(); porta.position.set(x0, YF, 0); scene.add(porta);
  const pw = XP - x0, pf = new THREE.Shape(); pf.moveTo(0, z0); pf.lineTo(pw, z0); pf.lineTo(pw, z1); pf.lineTo(0, z1); pf.lineTo(0, z0);
  const JAN = [4, 1, pw - 7, 21];                                           // janela no referencial da porta (x, z)
  pf.holes.push(ret(...JAN));
  const matPorta = transp(matGraf.clone());
  const portaCorpo = new THREE.Mesh(new THREE.ExtrudeGeometry(pf, { depth: 2, bevelEnabled: false }), matPorta);
  portaCorpo.rotation.x = PI / 2; portaCorpo.position.y = 0; porta.add(portaCorpo);            // extrusão vai de y = 0 a y = −2
  const jw = JAN[2] - JAN[0], jh = JAN[3] - JAN[1];
  const vidro = plano(jw, jh, transp(new THREE.MeshStandardMaterial({ color: cor('#0B0F14'), roughness: 0.05, metalness: 0.1, opacity: 0.5, envMapIntensity: 0.8 })));
  vidro.rotation.x = PI / 2; vidro.position.set(JAN[0] + jw / 2, -1.9, JAN[1] + jh / 2); porta.add(vidro);
  const tela = plano(jw, jh, new THREE.MeshStandardMaterial({ color: cor('#3A3F47'), roughness: 0.6, metalness: 0.5, alphaMap: telaTex,
    transparent: true, side: THREE.DoubleSide, depthWrite: false }));
  telaTex.repeat.set(jw / 0.5, jh / (0.5 * Math.sqrt(3)));
  tela.rotation.x = PI / 2; tela.position.set(JAN[0] + jw / 2, -1.0, JAN[1] + jh / 2); porta.add(tela);
  const puxador = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.6, 20), matCorte); puxador.position.set(pw - 2.6, -2.8, 11); porta.add(puxador);
  const matsPorta = [matPorta, vidro.material, tela.material, puxador.material];

  // Modo corte (C05/C06): sem teto e sem a parede da frente; bordas com espessura.
  const corte = new THREE.Group(); scene.add(corte);
  const corpoCorte = caixaCorpo(CH, invis); corte.add(corpoCorte);
  corpoCorte.scale.y = (y1 + CD / 2) / (y1 - y0); corpoCorte.position.y = (y1 - CD / 2) / 2;     // frente cortada no plano da abertura
  const u = new THREE.Shape();
  [[x0, z0], [x1, z0], [x1, CH], [CW / 2, CH], [CW / 2, 0], [-CW / 2, 0], [-CW / 2, CH], [x0, CH]].forEach(([a, b], i) => i ? u.lineTo(a, b) : u.moveTo(a, b));
  corte.add(naFrente(u, matCorte, -CD / 2 - 0.01));
  const tampoS = new THREE.Shape();                                         // borda de cima em U (sem a faixa da frente)
  [[x0, -CD / 2], [-CW / 2, -CD / 2], [-CW / 2, CD / 2], [CW / 2, CD / 2], [CW / 2, -CD / 2], [x1, -CD / 2], [x1, y1], [x0, y1]]
    .forEach(([a, b], i) => i ? tampoS.lineTo(a, b) : tampoS.moveTo(a, b));
  const matTampo = transp(matCorte.clone());
  const tampo = new THREE.Mesh(new THREE.ShapeGeometry(tampoS), matTampo); tampo.position.z = CH + 0.01; scene.add(tampo);

  // ---------- prato de vidro, anel de rodinhas e acoplador ----------
  const ZP = P.altura_cm, ZT0 = ZP + P.espessura_cm;                      // base e topo do prato
  const R = P.raio_cm, perfil = [[0, 0], [R - 0.7, 0], [R, 0.22], [R, P.espessura_cm - 0.15], [R - 0.3, P.espessura_cm], [0, P.espessura_cm]];
  const pratoGeo = new THREE.LatheGeometry(perfil.map(([r, z]) => new THREE.Vector2(r, z)), 128);
  const matVidro = new THREE.MeshPhysicalMaterial({ color: cor('#DDEFF2'), roughness: 0.05, metalness: 0, clearcoat: 1, clearcoatRoughness: 0.05,
    transparent: true, opacity: 0.16, envMapIntensity: 0.35, depthWrite: false, side: THREE.DoubleSide });
  const prato = new THREE.Mesh(pratoGeo, matVidro); prato.rotation.x = PI / 2; prato.position.z = ZP; prato.renderOrder = 5;
  const giro = new THREE.Group(); scene.add(giro); giro.add(prato);
  const matPlast = new THREE.MeshStandardMaterial({ color: cor('#3B4049'), roughness: 0.5, metalness: 0.1 });
  const anel = projeta(new THREE.Mesh(new THREE.TorusGeometry(8.5, 0.28, 12, 96), matPlast)); anel.position.z = 0.9; scene.add(anel);
  for (let k = 0; k < 3; k++) {
    const a = k * 2 * PI / 3, rod = projeta(new THREE.Mesh(new THREE.CylinderGeometry(0.85, 0.85, 0.6, 24), matPlast));
    rod.position.set(8.5 * Math.cos(a), 8.5 * Math.sin(a), 0.9); rod.rotation.z = a; anel.parent.add(rod); rod.userData.a = a;
    anel.userData.rodas = (anel.userData.rodas || []).concat(rod);
  }
  const acop = projeta(new THREE.Mesh(new THREE.CylinderGeometry(1.4, 1.4, 1.4, 6), matPlast)); acop.rotation.x = PI / 2; acop.position.z = 0.75; scene.add(acop);

  // ---------- barra de chocolate (C01): malha de altura com gomos chanfrados ----------
  const L = B.comprimento_cm, Wb = B.largura_cm, [gx, gy] = B.gomos, POR = 40, NX = gx * POR, NY = gy * POR;
  const Z0 = ZT0, ZT = Z0 + B.altura_cm, SULCO = 0.08;
  const barraGeo = new THREE.PlaneGeometry(L, Wb, NX, NY), pos = barraGeo.attributes.position, nV = pos.count;
  const cores = new Float32Array(nV * 3); barraGeo.setAttribute('color', new THREE.BufferAttribute(cores, 3));
  const perfilZ = new Float32Array(nV), mascara = new Float32Array(nV), sig2 = 2 * G.mancha_sigma_cm ** 2;
  const lx = L / gx, ly = Wb / gy, CH0 = B.chanfro_cm;
  for (let v = 0; v < nV; v++) {
    const x = pos.getX(v), y = pos.getY(v), i = v % (NX + 1), j = Math.floor(v / (NX + 1));
    const dx = Math.min(((x + L / 2) % lx + lx) % lx, lx - ((x + L / 2) % lx + lx) % lx);
    const dy = Math.min(((y + Wb / 2) % ly + ly) % ly, ly - ((y + Wb / 2) % ly + ly) % ly);
    const d = Math.min(dx, dy) - SULCO;                                       // distância à borda do gomo
    let z = d < 0 ? Z0 + B.base_cm : Math.min(ZT, ZT - CH0 + d);              // lateral do gomo e chanfro de 45°
    if (i === 0 || j === 0 || i === NX || j === NY) z = Z0;                    // saia: fecha as laterais da barra
    perfilZ[v] = z;
    let m = 0; for (const c of G.manchas_x_cm) m += Math.exp(-((x - c) ** 2 + y * y) / sig2);
    mascara[v] = Math.min(1, 1.6 * m);
  }
  const N1 = (NX + 1) * (NY + 1);
  const texRC = new THREE.DataTexture(new Uint8Array(N1 * 4), NX + 1, NY + 1, THREE.RGBAFormat);     // R = clearcoat, G = rugosidade
  const texE = new THREE.DataTexture(new Uint8Array(N1 * 4), NX + 1, NY + 1, THREE.RGBAFormat);
  const matChoc = new THREE.MeshPhysicalMaterial({ vertexColors: true, roughness: 1, roughnessMap: texRC, metalness: 0, clearcoat: 1,
    clearcoatMap: texRC, clearcoatRoughness: 0.4, normalMap: ruidoTex, normalScale: new THREE.Vector2(0.12, 0.12), envMapIntensity: 0.6,
    emissive: new THREE.Color(1, 1, 1), emissiveMap: texE });
  const barra = projeta(new THREE.Mesh(barraGeo, matChoc)); scene.add(barra);
  // Cores: a luz da vista de cima muda o tom; LUZ (por canal) faz o pixel final da troca bater com o 2D do Manim.
  // Na vista de cima (troca 3D → 2D) o fator vai de 1 até G.luz_topo (sólido 's', derretido 'd'), medido no quadro da troca.
  const LT = G.luz_topo || { s: [1, 1, 1], d: [1, 1, 1] };
  const cS = new THREE.Color(), cD = new THREE.Color(), cQ = cor('#FF7A3D');
  const fator = (h, f, w) => { const c = cor(h); return c.setRGB(c.r * (1 + (f[0] - 1) * w), c.g * (1 + (f[1] - 1) * w), c.b * (1 + (f[2] - 1) * w)); };
  let ultimo = '';
  function derrete(m, brilho, w) {
    const chave = m.toFixed(4) + '|' + brilho.toFixed(3) + '|' + w.toFixed(3);
    if (chave === ultimo) return;
    ultimo = chave;
    cS.copy(fator('#4A2C1E', LT.s, w)); cD.copy(fator('#6B4029', LT.d, w));
    const rc = texRC.image.data, e = texE.image.data, ZM = ZT - G.afundamento_cm;
    for (let v = 0; v < nV; v++) {
      const u = m * mascara[v], z0 = perfilZ[v];
      pos.setZ(v, z0 === Z0 ? Z0 : z0 + (ZM - z0) * u);
      cores[3 * v] = cS.r + (cD.r - cS.r) * u; cores[3 * v + 1] = cS.g + (cD.g - cS.g) * u; cores[3 * v + 2] = cS.b + (cD.b - cS.b) * u;
      const i = v % (NX + 1), j = Math.floor(v / (NX + 1)), k = 4 * ((NY - j) * (NX + 1) + i);
      rc[k] = Math.round(255 * (0.3 + 0.7 * u)); rc[k + 1] = Math.round(255 * (0.45 - 0.33 * u));
      const q = brilho * u; e[k] = 255 * q * cQ.r; e[k + 1] = 255 * q * cQ.g; e[k + 2] = 255 * q * cQ.b;
    }
    pos.needsUpdate = true; barraGeo.attributes.color.needsUpdate = true; barraGeo.computeVertexNormals();
    texRC.needsUpdate = true; texE.needsUpdate = true;
  }

  // ---------- fitas de onda ----------
  const K = 2 * PI / F.lambda_cm, OMEGA = 2 * PI * 0.8;
  function fita(P0, dir, comp) {
    const S = 200, mk = (larg, op) => {
      const g = new THREE.BufferGeometry(), v = new Float32Array((S + 1) * 2 * 3), idx = [];
      for (let s = 0; s < S; s++) { const a = 2 * s, b = a + 1, c = a + 2, d = a + 3; idx.push(a, b, c, b, d, c); }
      g.setAttribute('position', new THREE.BufferAttribute(v, 3)); g.setIndex(idx);
      const m = new THREE.Mesh(g, new THREE.MeshBasicMaterial({ color: cor('#35D9FF'), transparent: true, opacity: op, side: THREE.DoubleSide,
        blending: THREE.AdditiveBlending, depthWrite: false }));
      m.userData = { larg, op }; m.renderOrder = 10; scene.add(m); return m;
    };
    const faixas = [mk(F.largura_cm, 0.35), mk(0.22, 0.9)];
    return {
      // desl(s) = deslocamento vertical no ponto s ∈ [0, comp]; op = opacidade global; zc = altura do centro
      set(desl, op, zc) {
        for (const m of faixas) {
          const a = m.geometry.attributes.position.array, h = m.userData.larg / 2;
          for (let k = 0; k <= S; k++) {
            const s = comp * k / S, x = P0[0] + dir[0] * s, y = P0[1] + dir[1] * s, z = zc + desl(s);
            a.set([x, y, z - h, x, y, z + h], 6 * k);
          }
          m.geometry.attributes.position.needsUpdate = true; m.geometry.computeBoundingSphere();
          m.material.opacity = m.userData.op * op; m.visible = op > 0.002;
        }
      }
    };
  }
  // Onda que vai (½A cos(ks − ωτ)), bate na parede, volta (−½A cos(ks + ωτ)); juntas = A sen(ks) sen(ωτ).
  function vaiVolta(t, t0, comp, v, A) {
    const tau = t - t0, frente = v * tau, volta = comp - v * (tau - comp / v);
    return s => {
      const e1 = clamp((frente - s) / 1.5, 0, 1), e2 = clamp((s - volta) / 1.5, 0, 1) * (tau > comp / v ? 1 : 0);
      return 0.5 * A * Math.cos(K * s - OMEGA * tau) * e1 - 0.5 * A * Math.cos(K * s + OMEGA * tau) * e2;
    };
  }
  const fitaC01 = fita([-CW / 2, 0], [1, 0], CW);
  const diag = Math.hypot(CW, CD);
  const fitasC05 = [fita([-CW / 2, -3], [1, 0], CW), fita([4, -CD / 2], [0, 1], CD), fita([-CW / 2, -CD / 2], [CW / diag, CD / diag], diag)];

  // ---------- relevo de calor e gotas (C05/C06) ----------
  const nx = CAMPO.nx, ny = CAMPO.ny, CA = CAMPO.a_cm, CB = CAMPO.b_cm;
  const amostra = (arr, x, y) => {                                          // bilinear; x, y em cm a partir do centro
    const fx = clamp((x + CA / 2) / CA * (nx - 1), 0, nx - 1.001), fy = clamp((y + CB / 2) / CB * (ny - 1), 0, ny - 1.001);
    const i = Math.floor(fx), j = Math.floor(fy), a = fx - i, b = fy - j, k = j * nx + i;
    return (arr[k] * (1 - a) + arr[k + 1] * a) * (1 - b) + (arr[k + nx] * (1 - a) + arr[k + nx + 1] * a) * b;
  };
  const Imed = CAMPO.P.map((p, k) => (p + CAMPO.Q[k]) / 2);
  const relevoGeo = new THREE.PlaneGeometry(CA, CB, nx - 1, ny - 1), rpos = relevoGeo.attributes.position;
  const relevoTex = new THREE.TextureLoader().load(window.RELEVO_URL || 'relevo.png', () => { window.cenaPronta = true; }); relevoTex.encoding = THREE.sRGBEncoding; relevoTex.anisotropy = 8;
  const matRelevo = new THREE.MeshStandardMaterial({ map: relevoTex, emissive: new THREE.Color(1, 1, 1), emissiveMap: relevoTex, emissiveIntensity: 0.75,
    roughness: 0.8, color: new THREE.Color(0.35, 0.35, 0.35), metalness: 0, transparent: true, opacity: 0.8, side: THREE.DoubleSide, depthWrite: false });
  const relevo = new THREE.Mesh(relevoGeo, matRelevo); relevo.renderOrder = 8; scene.add(relevo);
  const HREL = 4, ZREL = ZT0 + 0.9;                                           // altura máxima e base (logo acima das gotas)
  function moldaRelevo(base, escala, w, t) {
    const c = Math.cos(OMEGA * t), s = Math.sin(OMEGA * t);
    for (let v = 0; v < rpos.count; v++) {
      const i = v % nx, k = (ny - 1 - Math.floor(v / nx)) * nx + i;            // PlaneGeometry: linha 0 em cima (y = +b/2)
      const inst = CAMPO.P[k] * c * c + CAMPO.Q[k] * s * s - 2 * CAMPO.R[k] * s * c;
      rpos.setZ(v, base + escala * HREL * Math.max(0, Imed[k] + w * (inst - Imed[k])));
    }
    rpos.needsUpdate = true; relevoGeo.computeVertexNormals();
  }
  const GOTAS = CAMPO.gotas_cm, NG = GOTAS.length;
  const gotaGeo = new THREE.SphereGeometry(0.45, 20, 10, 0, 2 * PI, 0, PI / 2); gotaGeo.rotateX(PI / 2);
  const matGota = new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: 0.35, metalness: 0, clearcoat: 0.5, clearcoatRoughness: 0.3, envMapIntensity: 0.6 });
  const gotas = projeta(new THREE.InstancedMesh(gotaGeo, matGota, NG)); giro.add(gotas);
  const gS = cor('#4A2C1E'), gD = cor('#6B4029'), gQ = cor('#FF7A3D'), gC = new THREE.Color(), mtx = new THREE.Matrix4();
  const Igota = GOTAS.map(([x, y]) => amostra(Imed, x, y));
  // C06: calor acumulado por gota ao girar (fração da média da volta), tabela em 720 passos de ângulo.
  const NA = 720, acum = GOTAS.map(([x, y]) => {
    const r = Math.hypot(x, y), a0 = Math.atan2(y, x), tab = new Float32Array(NA + 1);
    for (let k = 0; k < NA; k++) tab[k + 1] = tab[k] + amostra(Imed, r * Math.cos(a0 + 2 * PI * k / NA), r * Math.sin(a0 + 2 * PI * k / NA)) / NA;
    return tab;
  });
  function poeGotas(m, brilho, pulsoCentro) {
    for (let g = 0; g < NG; g++) {
      const u = m[g], esc = g === 0 ? 1 + 0.18 * pulsoCentro : 1;
      mtx.makeScale((1 + 0.45 * u) * esc, (1 + 0.45 * u) * esc, (1 - 0.65 * u) * esc).setPosition(GOTAS[g][0], GOTAS[g][1], ZT0);
      gotas.setMatrixAt(g, mtx);
      gC.copy(gS).lerp(gD, u).lerp(gQ, Math.min(1, brilho[g]));
      gotas.setColorAt(g, gC);
    }
    gotas.instanceMatrix.needsUpdate = true; gotas.instanceColor.needsUpdate = true;
  }

  // ---------- câmera: chaves do timeline, dolly-zoom (altura visível 'alt' no plano do alvo) ----------
  const camera = new THREE.PerspectiveCamera(60, W / H, 0.5, 2000);
  function estadoCamera(t) {
    const Lc = TL.camera;
    let i = 0;
    while (i < Lc.length - 2 && t > Lc[i + 1].t) i++;
    const a = Lc[i], b = Lc[i + 1], u = suave(clamp((t - a.t) / Math.max(b.t - a.t, 1e-9), 0, 1));
    const lerp = (x, y) => x + (y - x) * u;
    return { az: lerp(a.az, b.az), el: lerp(a.el, b.el), fov: lerp(a.fov, b.fov), alt: lerp(a.alt, b.alt),
      alvo: a.alvo.map((v, k) => lerp(v, b.alvo[k])), yc: lerp(a.yc, b.yc) };
  }
  function posicionaCamera(c) {
    const az = c.az * PI / 180, el = Math.min(c.el, 89.999) * PI / 180, D = (c.alt / 2) / Math.tan(c.fov * PI / 360);
    const alvo = new THREE.Vector3(...c.alvo);
    camera.fov = c.fov;
    camera.position.set(alvo.x + D * Math.cos(el) * Math.cos(az), alvo.y + D * Math.cos(el) * Math.sin(az), alvo.z + D * Math.sin(el));
    camera.up.set(-Math.sin(el) * Math.cos(az), -Math.sin(el) * Math.sin(az), Math.cos(el));
    camera.lookAt(alvo);
    camera.setViewOffset(W, H, 0, c.yc / 16 * H, W, H);                     // o alvo aparece em y = yc (unidades do Manim)
    camera.near = Math.max(0.5, D / 200); camera.far = D + 300;
    camera.updateProjectionMatrix();
  }

  // ---------- quadro ----------
  const opac = (mats, o) => mats.forEach(m => { m.opacity = o * (m.userData.op0 ?? (m.userData.op0 = m.opacity)); });
  window.setFrame = function (f) {
    // t ≥ c07_macro: o fecho do C07 reaproveita o macro do C01 (câmera travada em c07_macro_ref)
    const t = f / FPS >= E.c07_macro ? E.c07_macro_ref : f / FPS, c05 = t > 100;
    // --- visibilidade por modo ---
    for (const o of [frente, porta, painel, etiqueta, batente, corpo, barra, teto, lampada]) o.visible = !c05;
    corte.visible = c05;
    for (const fi of fitasC05) fi.set(() => 0, 0, 0);
    fitaC01.set(() => 0, 0, 0);
    relevo.visible = gotas.visible = c05;
    if (!c05) {
      // derretimento: já derretida no macro, rebobina, liga, derrete sob os ventres
      const m = t < E.c01_rebobina ? 1 : t < E.c01_derrete_ini ? 1 - rampa(t, E.c01_rebobina, E.c01_recua - E.c01_rebobina)
        : rampa(t, E.c01_derrete_ini, E.c01_derrete_fim - E.c01_derrete_ini);
      const aquece = t > E.c01_derrete_ini && t < E.c01_fitas_somem + 0.6 ? 1 : 0;
      derrete(m, aquece * 0.25 * Math.sin(PI * Math.min(m, 0.999)) * (0.35 + 0.65 * Math.sin(OMEGA * (t - E.c01_liga)) ** 2), rampa(t, E.c01_teto_some, E.c01_camera_topo - E.c01_teto_some));
      // porta: aberta (−100°) até fechar; a porta inteira (vidro e tela juntos) se dissolve quando a câmera a atravessa
      porta.rotation.z = -100 * PI / 180 * (1 - rampa(t, E.c01_porta_fecha, 1.0));
      opac(matsPorta, 1 - rampa(t, E.c01_tela_some, 0.8)); porta.visible = t < E.c01_tela_some + 0.8;
      // fitas
      const opF = rampa(t, E.c01_liga, 0.3) * (1 - rampa(t, E.c01_fitas_somem, 0.6));
      fitaC01.set(vaiVolta(t, E.c01_liga, CW, CW / (E.c01_fita_reflete - E.c01_liga), F.amplitude_cm), opF, ZT + F.altura_sobre_barra_cm);
      // teto, tampo do corpo e frente somem quando a câmera sobe (ela atravessa o plano do teto): corte de maquete
      const some = rampa(t, E.c01_teto_some, 0.8);
      opac([matTeto, matTopo, matFrente, lampada.material], 1 - some); opac([matTampo], some);
      teto.visible = lampada.visible = some < 0.999; corpo.material[4] = some < 0.999 ? matTopo : invis;
      frente.visible = painel.visible = etiqueta.visible = some < 0.999; tampo.visible = some > 0.001;
      etiqueta.visible = etiqueta.visible && t >= E.c01_recua + 0.3;     // fora do enquadramento do macro, a etiqueta não aparece
      opac([matBat], 1);
      giro.rotation.z = 0;
    } else {
      tampo.visible = true; opac([matTampo], 1);
      // C05: fitas cruzando, relevo sobe e ondula, gotas sob os morros derretem. C06: relevo a 40%, prato gira, anéis.
      fitasC05.forEach((fi, k) => {
        const t0 = E.c05_fitas + 0.6 * k, cmp = k === 2 ? diag : k === 0 ? CW : CD;
        const op = rampa(t, t0, 0.3) * (1 - rampa(t, E.c05_fitas_fim - 0.6, 0.6));
        fi.set(vaiVolta(t, t0, cmp, cmp / 1.4, F.amplitude_cm * 0.8), op, ZT0 + 6 + 1.2 * k);
      });
      const sobe = rampa(t, E.c05_relevo, 1.5), onda = t < E.c05_assenta ? rampa(t, E.c05_relevo + 1.5, 0.5) * (1 - rampa(t, E.c05_assenta - 1.5, 1.5)) : 0;
      relevo.visible = t > E.c05_relevo;
      if (relevo.visible) moldaRelevo(ZREL * sobe, sobe, 0.5 * onda, t);
      matRelevo.opacity = 0.8 * (t < E.c06 ? 1 : 0.4);
      const m = new Float32Array(NG), br = new Float32Array(NG);
      let phi = 0;
      if (t < E.c06) {
        const r = rampa(t, E.c05_derrete, 4);
        for (let g = 0; g < NG; g++) { m[g] = passo(0.5, 0.8, Igota[g]) * r; br[g] = 0.45 * m[g] * Math.sin(PI * r); }
      } else {
        const d = E.c06_prato_fim - E.c06_prato_ini;
        phi = 2 * PI * rampa(t, E.c06_prato_ini, d);
        const kk = phi / (2 * PI) * NA, k0 = Math.floor(kk), fr = kk - k0;
        const quente = t > E.c06_prato_ini && t < E.c06_prato_fim + 0.5 ? 1 : 0;
        for (let g = 0; g < NG; g++) {
          const a = acum[g], h = a[Math.min(k0, NA)] * (1 - fr) + a[Math.min(k0 + 1, NA)] * fr;
          m[g] = passo(0.33, 0.55, h); br[g] = quente * 0.3 * m[g] * (1 - m[g]) * 4;
        }
      }
      const pulso = t > E.c06_centro && t < E.c06_centro_fim ? Math.sin(PI * (t - E.c06_centro) / 1) ** 2 : 0;
      if (pulso) br[0] = Math.max(br[0], 0.6 * pulso);
      poeGotas(m, br, pulso);
      giro.rotation.z = phi;
      for (const rod of anel.userData.rodas) rod.position.set(8.5 * Math.cos(rod.userData.a + phi / 2), 8.5 * Math.sin(rod.userData.a + phi / 2), 0.9);
    }
    posicionaCamera(estadoCamera(t));
    renderer.render(scene, camera);
    return true;
  };
  // Pixel de um ponto 3D no quadro atual; e caixas (em unidades do Manim) dos objetos que rótulo nenhum pode cobrir.
  const v3 = new THREE.Vector3();
  window.projeta = p => { v3.set(...p).project(camera); return [(v3.x + 1) / 2 * W, (1 - v3.y) / 2 * H]; };
  const manim = p => { const [px, py] = window.projeta(p); return [px / W * 9 - 4.5, 8 - py / H * 16]; };
  const caixa = pts => { const q = pts.map(manim), xs = q.map(a => a[0]), ys = q.map(a => a[1]);
    return [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)].map(v => +v.toFixed(3)); };
  window.caixas3d = function () {
    const out = {}, circ = (r, z, n = 32) => [...Array(n).keys()].map(k => [r * Math.cos(2 * PI * k / n), r * Math.sin(2 * PI * k / n), z]);
    if (barra.visible) out.barra = caixa([-1, 1].flatMap(sx => [-1, 1].flatMap(sy => [Z0, ZT].map(z => [sx * L / 2, sy * Wb / 2, z]))));
    out.prato = caixa([...circ(R, ZP), ...circ(R, ZT0)]);
    if (gotas.visible) out.gotas = caixa([...circ(13.3, ZT0), ...circ(13.3, ZT0 + 0.5)]);
    if (relevo.visible) out.relevo = caixa([-1, 1].flatMap(sx => [-1, 1].flatMap(sy => [ZREL, ZREL + HREL].map(z => [sx * CA / 2, sy * CB / 2, z]))));
    return out;
  };
  window.TOPO_BARRA = ZT;
  // Conferência: os ventres da fita (|sen(k·x')| = 1, x' da parede esquerda) caem sobre os centros das manchas.
  window.erroVentres = Math.max(...G.manchas_x_cm.map(x => 1 - Math.abs(Math.sin(K * (x + CW / 2)))));
})();
