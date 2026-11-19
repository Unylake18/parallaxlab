// Base 3D do yt_0016 (Three.js r128), dirigida por ESTADO: a cena Manim calcula o estado de cada quadro (passagem seca,
// PEDIDOS3D=1) e o r3d.js chama window.setEstado(estado) e tira o print. Nada aqui depende de relógio próprio.
// Quadro do Manim 16 × 9 (x de −8 a 8, y de −4,5 a 4,5). Câmeras alinhadas ao Manim:
//   'frente' (az −90°): o plano y = 0 cai em Manim (xc + K·(x − camx), yc + K·z);
//   'topo'   (el 90°):  o plano z = 0 cai em Manim (xc + K·(x − camx), yc + K·(y − camy)).
// Cores da paleta sem sRGBEncoding; aço com envMapIntensity baixo (padrão do yt_0015).
window.B3D = (function () {
  const COR = { geo: 0xB8C4DA, aco: 0x7A8696, fundo: 0x050816, painel: 0x0E2A52, dim: 0x8FA3C4, terra: 0x4A5262 };
  const W = innerWidth, H = innerHeight, PI = Math.PI, FW = 16, FH = 9;
  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true, alpha: true });
  // v4 §2: cenas no espaço (window.TRANSP) saem sem fundo, sobre o céu do laboratório do Manim (fundo_lab.png)
  renderer.setPixelRatio(1); renderer.setSize(W, H); renderer.setClearColor(COR.fundo, window.TRANSP ? 0 : 1); renderer.autoClear = false;
  document.body.appendChild(renderer.domElement);
  const scene = new THREE.Scene();
  scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new THREE.RoomEnvironment(), 0.04).texture;
  const chave = new THREE.DirectionalLight(0xffffff, 1.5); chave.position.set(-3, -6, 7);
  const rim = new THREE.DirectionalLight(0x9CB4E8, 0.5); rim.position.set(6, 4, 3);
  const amb = new THREE.AmbientLight(0xffffff, 0.22);
  scene.add(chave, rim, amb);
  const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
  const suave = u => u * u * (3 - 2 * u);
  const mat = (cor, met, rug, env, extra) => new THREE.MeshStandardMaterial(Object.assign({ color: cor, metalness: met, roughness: rug, envMapIntensity: env }, extra || {}));

  // estrelas (cena separada; só nas cenas de espaço)
  const ceu = new THREE.Scene(), camCeu = new THREE.PerspectiveCamera(40, W / H, 1, 1000);
  {
    let s = 29; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    const pos = [], cor = [];
    for (let i = 0; i < 6000; i++) {           // densidade baixa no fov 16 (~60 estrelas no quadro)
      const u = 2 * rnd() - 1, th = 2 * PI * rnd(), q = Math.sqrt(1 - u * u), b = 0.16 + 0.45 * rnd() ** 2;
      pos.push(400 * q * Math.cos(th), 400 * q * Math.sin(th), 400 * u); cor.push(b, b, b);
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    geo.setAttribute('color', new THREE.Float32BufferAttribute(cor, 3));
    ceu.add(new THREE.Points(geo, new THREE.PointsMaterial({ size: 1.4, sizeAttenuation: false, vertexColors: true })));
  }

  const camera = new THREE.PerspectiveCamera(16, W / H, 0.05, 3000);
  function posicionaCamera(c) {
    // c: {modo:'frente'|'topo', K, xc, yc, camx, camy, fov, el}
    const K = c.K || 1, fov = c.fov || 14, alt = FH / K;
    let az, el, alvo;
    if (c.modo === 'topo') { az = -90; el = 89.999; alvo = [c.camx || 0, c.camy || 0, 0]; }
    else if (c.modo === 'obl') { az = c.az; el = c.el; alvo = c.alvo; }           // cênica: o alvo aparece em Manim (xc, yc)
    else { az = -90; el = c.el || 0; alvo = [c.camx || 0, 0, c.camz || 0]; }
    const a = az * PI / 180, e = el * PI / 180, D = (alt / 2) / Math.tan(fov * PI / 360);
    camera.fov = fov;
    camera.position.set(alvo[0] + D * Math.cos(e) * Math.cos(a), alvo[1] + D * Math.cos(e) * Math.sin(a), alvo[2] + D * Math.sin(e));
    camera.up.set(-Math.sin(e) * Math.cos(a), -Math.sin(e) * Math.sin(a), Math.cos(e));
    camera.lookAt(new THREE.Vector3(...alvo));
    camera.near = c.near ? c.near * D : Math.max(0.05, D - 80); camera.far = D + (c.far || 120);
    camera.setViewOffset(W, H, -(c.xc || 0) / FW * W, (c.yc || 0) / FH * H, W, H);
    camera.updateProjectionMatrix();
    camCeu.quaternion.copy(camera.quaternion); camCeu.fov = fov; camCeu.aspect = W / H;          // mesmo enquadramento: o horizonte do céu casa com o do piso
    camCeu.setViewOffset(W, H, -(c.xc || 0) / FW * W, (c.yc || 0) / FH * H, W, H); camCeu.updateProjectionMatrix();
    if (window.aposCamera) window.aposCamera(D);
  }
  function projeta(p) { const v = new THREE.Vector3(...p).project(camera); return [(v.x + 1) / 2 * W, (1 - v.y) / 2 * H]; }

  const texSombra = (() => {
    const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d');
    const r = g.createRadialGradient(64, 64, 0, 64, 64, 64);
    r.addColorStop(0, 'rgba(0,0,0,0.8)'); r.addColorStop(0.5, 'rgba(0,0,0,0.4)'); r.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = r; g.fillRect(0, 0, 128, 128); return new THREE.CanvasTexture(c);
  })();
  function sombra(w, h) {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: texSombra, transparent: true, depthWrite: false }));
    m.scale.set(w, h, 1); m.position.z = 0.004; scene.add(m); return m;
  }
  function sprite(tam, bordas) {
    const c = document.createElement('canvas'); c.width = c.height = tam; const g = c.getContext('2d');
    const r = g.createRadialGradient(tam / 2, tam / 2, 0, tam / 2, tam / 2, tam / 2);
    r.addColorStop(0, 'rgba(255,255,255,1)'); r.addColorStop(0.35, 'rgba(255,255,255,0.95)');
    r.addColorStop(bordas, 'rgba(255,255,255,0.25)'); r.addColorStop(1, 'rgba(255,255,255,0)');
    g.fillStyle = r; g.fillRect(0, 0, tam, tam);
    return new THREE.CanvasTexture(c);
  }
  // chão: faixa escura com textura de riscos leves (o mesmo chão do yt_0015)
  function chao(cor) { const m = new THREE.Mesh(new THREE.PlaneGeometry(400, 80), mat(cor || 0x0B1020, 0.0, 0.6, 0.22)); scene.add(m); return m; }

  let comCeu = false;
  window.setEstado = function (e) {
    if (window.CENA) window.CENA.atualiza(e);
    posicionaCamera(e.cam || { modo: 'frente' });
    renderer.clear(); if (comCeu) renderer.render(ceu, camCeu); renderer.clearDepth(); renderer.render(scene, camera);
    return window.pontos3d ? window.pontos3d(e) : null;
  };
  window.projeta = projeta;
  return { COR, W, H, PI, scene, renderer, camera, clamp, suave, mat, sombra, sprite, chao, projeta, luz: { chave, rim, amb },
    ceu: v => { comCeu = v; }, cenaCeu: ceu };
})();
