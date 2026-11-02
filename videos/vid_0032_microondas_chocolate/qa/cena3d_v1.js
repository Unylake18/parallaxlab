// vid_0032 — forno de micro-ondas 3D do gancho (C01), Three.js r128. Tudo é função do quadro: window.setFrame(f).
// Unidade do mundo = 1 cm, z para cima. Cavidade: x ∈ ±17,5, y ∈ ±15,5 (abertura em y = −15,5), z ∈ [0, 22].
// window.TIMELINE (timeline.json) e window.FPS são injetados pelo render3d.js antes do carregamento.
(function () {
  const TL = window.TIMELINE, FPS = window.FPS || 15, G = TL.geometria, E = TL.eventos;
  const [CW, CD, CH] = G.cavidade_cm, B = G.barra, P = G.prato;
  const COR = { aco: 0x7A8696, fundo: 0x050816, choc: 0x4A2C1E, chocD: 0x6B4029, calor: 0xFF7A3D };
  const W = innerWidth, H = innerHeight, PI = Math.PI;

  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H); renderer.setClearColor(COR.fundo, 1);
  document.body.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new THREE.RoomEnvironment(), 0.04).texture;
  const luz = new THREE.PointLight(0xffffff, 0.42, 0, 2); luz.position.set(-2, -8, 15);    // lâmpada interna, branca (abaixo do teto: sem reflexo atrás da manchete)
  const chave = new THREE.DirectionalLight(0xffffff, 0.4); chave.position.set(-20, -40, 60);
  scene.add(luz, chave, new THREE.AmbientLight(0xffffff, 0.2));

  const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
  const suave = u => u * u * (3 - 2 * u);
  const rampa = (t, t0, dur) => suave(clamp((t - t0) / dur, 0, 1));

  // ---------- cavidade (paredes de aço escovado discreto) ----------
  const matAco = new THREE.MeshStandardMaterial({ color: COR.aco, metalness: 0.8, roughness: 0.45, envMapIntensity: 0.35, side: THREE.DoubleSide });
  const matPiso = matAco.clone(); matPiso.color = new THREE.Color(0x5F6977);
  const plano = (w, h, mat) => new THREE.Mesh(new THREE.PlaneGeometry(w, h), mat);
  const piso = plano(CW, CD, matPiso); scene.add(piso);
  const fundo = plano(CW, CH, matAco); fundo.rotation.x = PI / 2; fundo.position.set(0, CD / 2, CH / 2); scene.add(fundo);
  for (const s of [-1, 1]) {
    const lado = plano(CD, CH, matAco); lado.rotation.set(PI / 2, s * PI / 2, 0); lado.position.set(s * CW / 2, 0, CH / 2); scene.add(lado);
  }
  const matTeto = matAco.clone(); matTeto.transparent = true;
  const teto = plano(CW, CD, matTeto); teto.position.z = CH; scene.add(teto);
  // Grade de ventilação sutil no teto (furos escuros).
  const furos = new THREE.Group(); teto.add(furos);
  const matFuro = new THREE.MeshBasicMaterial({ color: 0x1A1F27, transparent: true, side: THREE.DoubleSide });
  for (let i = 0; i < 6; i++) for (let j = 0; j < 4; j++) {
    const furo = new THREE.Mesh(new THREE.CircleGeometry(0.35, 12), matFuro);
    furo.position.set(8 + i * 1.3, 6 + j * 1.3, -0.02); furos.add(furo);
  }
  // Frente do forno: moldura de aço mais escuro em volta da abertura (a porta não existe).
  const frente = new THREE.Shape();
  frente.moveTo(-30, -9); frente.lineTo(30, -9); frente.lineTo(30, 34); frente.lineTo(-30, 34); frente.lineTo(-30, -9);
  const buraco = new THREE.Path();
  buraco.moveTo(-CW / 2, 0); buraco.lineTo(-CW / 2, CH); buraco.lineTo(CW / 2, CH); buraco.lineTo(CW / 2, 0); buraco.lineTo(-CW / 2, 0);
  frente.holes.push(buraco);
  const matFrente = new THREE.MeshStandardMaterial({ color: 0x3A424E, metalness: 0.6, roughness: 0.55, envMapIntensity: 0.25, side: THREE.DoubleSide, transparent: true });
  const moldura = new THREE.Mesh(new THREE.ShapeGeometry(frente), matFrente);
  moldura.rotation.x = PI / 2; moldura.position.y = -CD / 2; scene.add(moldura);

  // ---------- prato de vidro (parado o tempo todo) ----------
  const prato = new THREE.Mesh(new THREE.CylinderGeometry(P.raio_cm, P.raio_cm, P.espessura_cm, 96),
    new THREE.MeshPhysicalMaterial({ color: 0xCFE3F0, metalness: 0, roughness: 0.08, transparent: true, opacity: 0.35, envMapIntensity: 0.6 }));
  prato.rotation.x = PI / 2; prato.position.z = P.altura_cm + P.espessura_cm / 2; scene.add(prato);
  const Z0 = P.altura_cm + P.espessura_cm, ZT = Z0 + B.altura_cm;       // base e topo da barra

  // ---------- barra de chocolate: laterais (caixa sem tampa) + tampa em malha fina deformada por quadro ----------
  const matChoc = new THREE.MeshStandardMaterial({ color: COR.choc, roughness: 0.6, metalness: 0, envMapIntensity: 0.3 });
  const caixa = new THREE.Mesh(new THREE.BoxGeometry(B.comprimento_cm, B.largura_cm, B.altura_cm),
    [matChoc, matChoc, matChoc, matChoc, new THREE.MeshBasicMaterial({ visible: false }), matChoc]);
  caixa.position.z = Z0 + B.altura_cm / 2; scene.add(caixa);

  const NX = 440, NY = 160, L = B.comprimento_cm, Wb = B.largura_cm;
  const tampaGeo = new THREE.PlaneGeometry(L, Wb, NX, NY);
  const pos = tampaGeo.attributes.position, nV = pos.count;
  const cores = new Float32Array(nV * 3); tampaGeo.setAttribute('color', new THREE.BufferAttribute(cores, 3));
  // Máscara das manchas (gaussianas) e perfil dos sulcos, pré-calculados por vértice.
  const mascara = new Float32Array(nV), sulco = new Float32Array(nV);
  const sig2 = 2 * G.mancha_sigma_cm ** 2, [gx, gy] = B.gomos, MEIO = 0.12;
  for (let v = 0; v < nV; v++) {
    const x = pos.getX(v), y = pos.getY(v);
    let m = 0; for (const c of G.manchas_x_cm) m += Math.exp(-((x - c) ** 2 + y * y) / sig2);
    mascara[v] = Math.min(1, m);
    let s = 0;
    for (let i = 1; i < gx; i++) s = Math.max(s, 1 - Math.abs(x - (-L / 2 + i * L / gx)) / MEIO);
    for (let j = 1; j < gy; j++) s = Math.max(s, 1 - Math.abs(y - (-Wb / 2 + j * Wb / gy)) / MEIO);
    sulco[v] = s;
  }
  // Rugosidade (canal G) e brilho emissivo por texel: DataTexture alinhada à grade de vértices.
  const texR = new THREE.DataTexture(new Uint8Array((NX + 1) * (NY + 1) * 4), NX + 1, NY + 1, THREE.RGBAFormat);
  const texE = new THREE.DataTexture(new Uint8Array((NX + 1) * (NY + 1) * 4), NX + 1, NY + 1, THREE.RGBAFormat);
  const matTampa = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 1, roughnessMap: texR, metalness: 0,
    envMapIntensity: 0.3, emissive: new THREE.Color(COR.calor), emissiveMap: texE, emissiveIntensity: 1 });
  const tampa = new THREE.Mesh(tampaGeo, matTampa); scene.add(tampa);
  // A luz da vista de cima clareia a barra; o fator por canal (medido no quadro da troca) faz o pixel final
  // cair em #4A2C1E (sólido) e ~#6B4029 (derretido), as mesmas cores do 2D do Manim.
  const LUZ = [0.70, 0.66, 0.62];
  const comp = c => new THREE.Color(c.r * LUZ[0], c.g * LUZ[1], c.b * LUZ[2]);
  const cS = comp(new THREE.Color(COR.choc)), cD = comp(new THREE.Color(COR.chocD));
  matChoc.color.copy(cS);

  let ultimoDerrete = -1;
  function derrete(m, brilho) {
    if (Math.abs(m - ultimoDerrete) < 1e-6 && brilho === 0) return;
    ultimoDerrete = m;
    const r = texR.image.data, e = texE.image.data, A = G.afundamento_cm, S = B.sulco_cm;
    for (let v = 0; v < nV; v++) {
      const u = m * mascara[v];
      pos.setZ(v, ZT - S * sulco[v] * (1 - u) - A * u);
      cores[3 * v] = cS.r + (cD.r - cS.r) * u; cores[3 * v + 1] = cS.g + (cD.g - cS.g) * u; cores[3 * v + 2] = cS.b + (cD.b - cS.b) * u;
      // PlaneGeometry: vértice v = (i, j) com j = 0 no topo (y = +Wb/2); a textura tem a linha 0 em v = 0 (embaixo).
      const i = v % (NX + 1), j = Math.floor(v / (NX + 1)), k = 4 * ((NY - j) * (NX + 1) + i);
      r[k + 1] = Math.round(255 * (0.6 - 0.4 * u));
      const q = Math.round(255 * Math.min(1, brilho * u)); e[k] = e[k + 1] = e[k + 2] = q;
    }
    pos.needsUpdate = true; tampaGeo.attributes.color.needsUpdate = true; tampaGeo.computeVertexNormals();
    texR.needsUpdate = true; texE.needsUpdate = true;
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
    const az = c.az * PI / 180, el = c.el * PI / 180, D = (c.alt / 2) / Math.tan(c.fov * PI / 360);
    const alvo = new THREE.Vector3(...c.alvo);
    camera.fov = c.fov;
    camera.position.set(alvo.x + D * Math.cos(el) * Math.cos(az), alvo.y + D * Math.cos(el) * Math.sin(az), alvo.z + D * Math.sin(el));
    camera.up.set(-Math.sin(el) * Math.cos(az), -Math.sin(el) * Math.sin(az), Math.cos(el));
    camera.lookAt(alvo);
    // O alvo aparece em y = yc (unidades do Manim, quadro de 16 de altura).
    camera.setViewOffset(W, H, 0, c.yc / 16 * H, W, H);
    camera.updateProjectionMatrix();
    return D;
  }

  // ---------- quadro ----------
  window.setFrame = function (f) {
    const t = f / FPS;
    const dur = E.c01_derrete_fim - E.c01_derrete_ini;
    const m = rampa(t, E.c01_derrete_ini, dur);
    const brilho = 0.25 * Math.sin(PI * m) * (t > E.c01_derrete_ini && t < E.c01_derrete_fim + 0.5 ? 1 : 0);
    derrete(m, brilho);
    const D = posicionaCamera(estadoCamera(t));
    // O teto some quando a câmera sobe (ela atravessa o plano do teto): corte, como numa maquete.
    const some = rampa(t, E.c01_teto_some, 1.2);
    matTeto.opacity = 1 - some; matFuro.opacity = 1 - some; teto.visible = some < 0.999;
    matFrente.opacity = 1 - some; moldura.visible = some < 0.999;   // a moldura acima da abertura taparia a barra
    camera.near = 0.5; camera.far = D + 200; camera.updateProjectionMatrix();
    renderer.render(scene, camera);
    return true;
  };
  // Pixel de um ponto 3D no quadro atual (timeline e QA de alinhamento).
  window.projeta = p => { const v = new THREE.Vector3(...p).project(camera); return [(v.x + 1) / 2 * W, (1 - v.y) / 2 * H]; };
  window.TOPO_BARRA = ZT;
  window.cenaPronta = true;
})();
