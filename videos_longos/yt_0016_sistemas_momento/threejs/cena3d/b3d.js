// Base 3D do yt_0016 (Three.js r128), dirigida por ESTADO: a cena Manim calcula o estado de cada quadro (passagem seca,
// PEDIDOS3D=1) e o r3d.js chama window.setEstado(estado) e tira o print. Nada aqui depende de relógio próprio.
// Quadro do Manim 16 × 9 (x de −8 a 8, y de −4,5 a 4,5). Câmeras alinhadas ao Manim:
//   'frente' (az −90°): o plano y = 0 cai em Manim (xc + K·(x − camx), yc + K·z);
//   'topo'   (el 90°):  o plano z = 0 cai em Manim (xc + K·(x − camx), yc + K·(y − camy)).
// Cores da paleta sem sRGBEncoding; aço com envMapIntensity baixo (padrão do yt_0015).
window.B3D = (function () {
  const COR = { geo: 0xB8C4DA, aco: 0x7A8696, fundo: 0x050816, painel: 0x0E2A52, dim: 0x8FA3C4, terra: 0x4A5262 };
  const W = innerWidth, H = innerHeight, PI = Math.PI, FW = 16, FH = 9;
  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H); renderer.setClearColor(COR.fundo, 1); renderer.autoClear = false;
  document.body.appendChild(renderer.domElement);
  const scene = new THREE.Scene();
  scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new THREE.RoomEnvironment(), 0.04).texture;
  const chave = new THREE.DirectionalLight(0xffffff, 1.5); chave.position.set(-3, -6, 7);
  const rim = new THREE.DirectionalLight(0x9CB4E8, 0.5); rim.position.set(6, 4, 3);
  const amb = new THREE.AmbientLight(0xffffff, 0.22);
  scene.add(chave, rim, amb);
  const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
  const suave = u => u * u * (3 - 2 * u);
  // v7 (§1.3): fundo espacial da unidade (o mesmo PNG do Manim, fundo_lab.js) desenhado antes de tudo, em tela cheia
  const fundo = new THREE.Scene();
  window.fundoPronto = !window.FUNDO_LAB;
  if (window.FUNDO_LAB) {
    const img = new Image();
    img.onload = () => {
      const t = new THREE.Texture(img); t.minFilter = THREE.LinearFilter; t.magFilter = THREE.LinearFilter; t.generateMipmaps = false;
      t.needsUpdate = true; fundo.background = t; window.fundoPronto = true;
    };
    img.src = window.FUNDO_LAB;
  }
  const mat = (cor, met, rug, env, extra) => new THREE.MeshStandardMaterial(Object.assign({ color: cor, metalness: met, roughness: rug, envMapIntensity: env }, extra || {}));

  // estrelas (cena separada; só nas cenas de espaço)
  const ceu = new THREE.Scene(), camCeu = new THREE.PerspectiveCamera(40, W / H, 1, 1000);
  {
    let s = 29; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    const pos = [], cor = [];
    for (let i = 0; i < 700; i++) {
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
    camera.lookAt(new THREE.Vector3(...alvo)); camera.userData.alvo = new THREE.Vector3(...alvo); camera.userData.alt = alt;
    camera.near = Math.max(0.05, D - 80); camera.far = D + 120;
    camera.setViewOffset(W, H, -(c.xc || 0) / FW * W, (c.yc || 0) / FH * H, W, H);
    camera.updateProjectionMatrix();
    camCeu.quaternion.copy(camera.quaternion);
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
  // v7 (§1.3): chão do laboratório — azul-noite com grade ciano fina. Chão e grade esmaecem com a profundidade além do alvo da
  // câmera (d, em alturas de quadro `alt`): o chão some no céu, sem aresta. esmaece(material, o) aplica o mesmo a gelo/concreto.
  const uAlvo = { value: new THREE.Vector3() }, uDir = { value: new THREE.Vector2(0, 1) }, uAlt = { value: 9 };
  function esmaece(m, o) {
    o = Object.assign({ fa: 0.0, fb: 0.9, grade: 0, gop: 0.06, ga: 0.0, gb: 0.6 }, o || {});
    m.transparent = true; m.depthWrite = false;
    m.onBeforeCompile = sh => {
      Object.assign(sh.uniforms, { uAlvo, uDir, uAlt, uFa: { value: o.fa }, uFb: { value: o.fb }, uG: { value: o.grade }, uGo: { value: o.gop },
        uGa: { value: o.ga }, uGb: { value: o.gb }, uGc: { value: new THREE.Color(0x35D9FF) } });
      sh.vertexShader = 'varying vec3 vW;\n' + sh.vertexShader.replace('#include <project_vertex>',
        '#include <project_vertex>\n vW = (modelMatrix * vec4(transformed, 1.0)).xyz;');
      sh.fragmentShader = 'varying vec3 vW;\nuniform float uAlt, uFa, uFb, uG, uGo, uGa, uGb;\nuniform vec3 uGc, uAlvo;\nuniform vec2 uDir;\n' +
        sh.fragmentShader.replace('#include <dithering_fragment>',
        `float dp = dot(vW.xy - uAlvo.xy, uDir) / uAlt;
         float fade = 1.0 - smoothstep(uFa, uFb, dp);
         if (uG > 0.0) {
           vec2 q = vW.xy / (uG * uAlt / 9.0), w = fwidth(q);
           vec2 l = abs(fract(q - 0.5) - 0.5) / max(w * 0.9, vec2(1e-4));
           float linha = (1.0 - min(min(l.x, l.y), 1.0)) * (1.0 - smoothstep(uGa, uGb, dp)) * (1.0 - smoothstep(0.6, 1.6, max(w.x, w.y)));
           gl_FragColor.rgb += uGc * linha * uGo;
         }
         gl_FragColor.a *= fade;
         #include <dithering_fragment>`);
    };
    return m;
  }
  function chao(cor, o) {
    o = Object.assign({ grade: 1.0 }, (typeof cor === 'object' ? cor : o) || {});
    const m = esmaece(mat(o.cor || 0x070D22, 0.0, 0.85, 0.08), o);
    const c = new THREE.Mesh(new THREE.PlaneGeometry(600, 240), m); c.renderOrder = -5; scene.add(c); return c;
  }
  // v7: luz das cenas novas — key quente suave, rim ciano frio nos contornos (as cenas antigas mantêm a luz do v6)
  const luz0 = [chave.color.getHex(), chave.intensity, chave.position.clone(), rim.color.getHex(), rim.intensity, rim.position.clone(), amb.intensity];
  function luzV6() {
    chave.color.set(luz0[0]); chave.intensity = luz0[1]; chave.position.copy(luz0[2]);
    rim.color.set(luz0[3]); rim.intensity = luz0[4]; rim.position.copy(luz0[5]); amb.intensity = luz0[6];
  }
  function luzLab() {
    chave.color.set(0xFFE7CF); chave.intensity = 1.45; chave.position.set(-4, -7, 8);
    rim.color.set(0x5FD3FF); rim.intensity = 0.95; rim.position.set(5, 9, 4);
    amb.intensity = 0.17;
  }

  let comCeu = false;
  window.setEstado = function (e) {
    if (window.CENA) window.CENA.atualiza(e);
    posicionaCamera(e.cam || { modo: 'frente' });
    { const a = camera.userData.alvo || new THREE.Vector3(), d = new THREE.Vector2(a.x - camera.position.x, a.y - camera.position.y);
      uAlvo.value.copy(a); if (d.length() > 1e-6) uDir.value.copy(d.normalize()); uAlt.value = camera.userData.alt || 9; }
    renderer.clear(); renderer.render(fundo, camera); if (comCeu) { renderer.clearDepth(); renderer.render(ceu, camCeu); }
    renderer.clearDepth(); renderer.render(scene, camera);
    return window.pontos3d ? window.pontos3d(e) : null;
  };
  window.projeta = projeta;
  return { COR, W, H, PI, scene, renderer, camera, clamp, suave, mat, sombra, sprite, chao, esmaece, projeta, luz: { chave, rim, amb }, luzLab, luzV6,
    ceu: v => { comCeu = v; } };
})();
