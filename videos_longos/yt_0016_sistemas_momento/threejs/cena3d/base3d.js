// Base comum dos trechos 3D do yt_0015 (Three.js r128). Adaptada do modelo experimentos/threejs/modelo (9×16) para 16:9.
// Regras do pipeline: tudo é função do quadro (window.setFrame), uma única fonte de tempo (timeline_<trecho>.json),
// cores da paleta sem sRGBEncoding (README, regra 6), aço com envMapIntensity baixo.
// Quadro do Manim: 16 × 9 unidades (x de −8 a 8, y de −4,5 a 4,5). Na vista 'frente' (az −90°, el 0°) o plano y = 0
// cai em Manim (cx + K·(x − x_cam), cy + K·z).
window.B3D = (function () {
  const TL = window.TIMELINE, FPS = window.FPS || 15, G = TL.geometria, K = G.fator_3d_manim;
  const COR = { geo: 0xB8C4DA, aco: 0x7A8696, fundo: 0x050816, painel: 0x0E2A52, dim: 0x8FA3C4 };
  const W = innerWidth, H = innerHeight, PI = Math.PI, FW = 16, FH = 9;

  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H); renderer.setClearColor(COR.fundo, 1); renderer.autoClear = false;
  document.body.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new THREE.RoomEnvironment(), 0.04).texture;
  const chave = new THREE.DirectionalLight(0xffffff, 1.5); chave.position.set(-3, -6, 7);
  const rim = new THREE.DirectionalLight(0x9CB4E8, 0.5); rim.position.set(6, 4, 3);
  scene.add(chave, rim, new THREE.AmbientLight(0xffffff, 0.22));

  const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
  const suave = u => u * u * (3 - 2 * u);
  const rampa = (t, t0, dur) => suave(clamp((t - t0) / dur, 0, 1));
  function chaves(lista, t, campo) {            // [{t, campo, ease?}] — 'linear' liga o trecho reto
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

  // ---- estrelas (cena separada: não "zoomam" no dolly) ----
  const ceu = new THREE.Scene(), camCeu = new THREE.PerspectiveCamera(40, W / H, 1, 1000);
  {
    let s = 29; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    const pos = [], cor = [];
    for (let i = 0; i < 500; i++) {
      const u = 2 * rnd() - 1, th = 2 * PI * rnd(), q = Math.sqrt(1 - u * u), b = 0.18 + 0.4 * rnd() ** 2;
      pos.push(400 * q * Math.cos(th), 400 * q * Math.sin(th), 400 * u); cor.push(b, b, b);
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    geo.setAttribute('color', new THREE.Float32BufferAttribute(cor, 3));
    ceu.add(new THREE.Points(geo, new THREE.PointsMaterial({ size: 1.4, sizeAttenuation: false, vertexColors: true })));
  }

  // ---- câmera por modos: 'frente' (alinhada ao Manim) e 'obl' (cênica) ----
  const camera = new THREE.PerspectiveCamera(30, W / H, 0.05, 3000);
  function estado(ent, t, camx) {
    const modo = ent.modo;
    if (modo === 'frente')
      return { az: -90, el: G.el_frente || 0, fov: G.fov_frente || 14, alt: FH / K, alvo: [camx, 0, 0], yc: G.centro_manim[1], xc: G.centro_manim[0] };
    const o = ent.cfg || G.obl;                                  // câmera 3/4 baixa (cfg própria da chave, se houver)
    return { az: o.az + (o.d_az || 0) * t, el: o.el, fov: o.fov, alt: o.alt, alvo: o.alvo, yc: o.yc, xc: o.xc };
  }
  function misturaCamera(t) {
    const L = TL.camera; let i = 0;
    while (i < L.length - 2 && t > L[i + 1].t) i++;
    const a = L[i], b = L[i + 1], u = suave(clamp((t - a.t) / Math.max(b.t - a.t, 1e-9), 0, 1));
    const camx = TL.cam_x ? chaves(TL.cam_x, t, 'x') : 0;
    const e0 = estado(a, t, camx), e1 = estado(b, t, camx), lerp = (x, y) => x + (y - x) * u;
    return { az: lerp(e0.az, e1.az), el: lerp(e0.el, e1.el), fov: lerp(e0.fov, e1.fov), alt: lerp(e0.alt, e1.alt),
      alvo: e0.alvo.map((v, k) => lerp(v, e1.alvo[k])), yc: lerp(e0.yc, e1.yc), xc: lerp(e0.xc, e1.xc) };
  }
  function posicionaCamera(c) {
    const az = c.az * PI / 180, el = c.el * PI / 180, D = (c.alt / 2) / Math.tan(c.fov * PI / 360);
    const alvo = new THREE.Vector3(...c.alvo);
    camera.fov = c.fov;
    camera.position.set(alvo.x + D * Math.cos(el) * Math.cos(az), alvo.y + D * Math.cos(el) * Math.sin(az), alvo.z + D * Math.sin(el));
    camera.up.set(-Math.sin(el) * Math.cos(az), -Math.sin(el) * Math.sin(az), Math.cos(el));
    camera.lookAt(alvo);
    camera.near = Math.max(0.05, D - 60); camera.far = D + 80;
    camera.setViewOffset(W, H, -c.xc / FW * W, c.yc / FH * H, W, H);   // o alvo aparece em Manim (xc, yc)
    camCeu.quaternion.copy(camera.quaternion);
    if (window.aposCamera) window.aposCamera(D);                         // ex.: névoa relativa à distância da câmera
  }

  // ---- sombra de contato discreta e escurecimento final ("o 3D recua e some") ----
  const ortho = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 2), cena2 = new THREE.Scene();
  const veu = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), new THREE.MeshBasicMaterial({ color: COR.fundo, transparent: true, opacity: 0, depthTest: false }));
  cena2.add(veu);

  function sprite(tam, bordas) {                                  // disco brilhante (corpúsculo de luz)
    const c = document.createElement('canvas'); c.width = c.height = tam; const g = c.getContext('2d');
    const r = g.createRadialGradient(tam / 2, tam / 2, 0, tam / 2, tam / 2, tam / 2);
    r.addColorStop(0, 'rgba(255,255,255,1)'); r.addColorStop(0.35, 'rgba(255,255,255,0.95)');
    r.addColorStop(bordas, 'rgba(255,255,255,0.25)'); r.addColorStop(1, 'rgba(255,255,255,0)');
    g.fillStyle = r; g.fillRect(0, 0, tam, tam);
    return new THREE.CanvasTexture(c);
  }

  function desenha(f, atualiza) {
    const t = f / FPS;
    atualiza(t);
    posicionaCamera(misturaCamera(t));
    veu.material.opacity = TL.fade_out ? chaves(TL.fade_out, t, 'v') : 0;
    renderer.clear(); if (!TL.sem_ceu) renderer.render(ceu, camCeu); renderer.clearDepth(); renderer.render(scene, camera);
    if (veu.material.opacity > 0.001) { renderer.clearDepth(); renderer.render(cena2, ortho); }
  }
  return { TL, FPS, G, K, COR, W, H, PI, scene, renderer, camera, clamp, suave, rampa, chaves, desenha, sprite,
    projeta: p => { const v = new THREE.Vector3(...p).project(camera); return [(v.x + 1) / 2 * W, (1 - v.y) / 2 * H]; } };
})();
