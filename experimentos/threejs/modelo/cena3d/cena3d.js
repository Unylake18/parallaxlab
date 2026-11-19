// MODELO de cena 3D (Three.js r128) para o pipeline Three.js + Manim do Parallax Lab.
// Regra de ouro: tudo é função do quadro. window.setFrame(f) desenha o quadro f sem relógio nem requestAnimationFrame,
// para o render ser determinístico e casar quadro a quadro com o Manim.
// window.TIMELINE (timeline.json) e window.FPS são injetados pelo render3d.js antes da página carregar.
//
// O que já vem pronto (copiado e simplificado do vid_0029, o toroide):
//  - renderer com fundo do canal, luz e reflexo de ambiente (RoomEnvironment) discretos;
//  - funções de tempo (rampa, chaves) iguais às do Manim;
//  - câmera por modos ('orbita', 'topo') com transição suave e DOLLY-ZOOM: na vista 'topo' o plano z = 0 cai exatamente
//    nas coordenadas do Manim (fator_3d_manim, centro_topo_manim), então o Manim pode desenhar por cima;
//  - estrelas numa cena separada (não "zoomam" no dolly);
//  - exemplo de objeto: anel de aço com um RASTRO de luz verde (corrente) e um anel magenta com pulsos (campo);
//  - window.projeta(p) para o QA de alinhamento.
// Troque o bloco "OBJETO" pelo sólido do seu vídeo; o resto normalmente fica igual.
(function () {
  const TL = window.TIMELINE, FPS = window.FPS || 15, G = TL.geometria, K = G.fator_3d_manim;
  const COR = { corrente: 0x3FE08B, campo: 0xEA63FF, geo: 0xB8C4DA, aco: 0x7A8696, fundo: 0x050816 };
  const W = innerWidth, H = innerHeight, PI = Math.PI;

  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H); renderer.setClearColor(COR.fundo, 1); renderer.autoClear = false;
  document.body.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new THREE.RoomEnvironment(), 0.04).texture;
  const chave = new THREE.DirectionalLight(0xffffff, 1.7); chave.position.set(3, -4, 6);
  scene.add(chave, new THREE.AmbientLight(0xffffff, 0.12));

  // ---------- funções de tempo (use as MESMAS no cena.py do Manim) ----------
  const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
  const suave = u => u * u * (3 - 2 * u);
  const rampa = (t, t0, dur) => suave(clamp((t - t0) / dur, 0, 1));
  function chaves(lista, t, campo) {            // interpola uma lista [{t, campo, ease?}] do timeline
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

  // ---------- OBJETO (troque pelo do seu vídeo) ----------
  const R = G.raio_objeto;
  const obj = new THREE.Group(); scene.add(obj);
  const matAco = new THREE.MeshStandardMaterial({ color: COR.aco, metalness: 0.8, roughness: 0.45, envMapIntensity: 0.35 });
  obj.add(new THREE.Mesh(new THREE.TorusGeometry(R, 0.06, 16, 200), matAco));

  // Corrente = rastro de luz (cometa) num tubo um pouco mais grosso por cima do fio. uv.x = fração do comprimento.
  // Δ = quanto o ponto está atrás da cabeça; intensidade exp(−Δ/τ). Cor sólida (sem somar luz), cabeça ~30% mais clara.
  const RS = TL.rastros;
  const matRastro = new THREE.ShaderMaterial({
    uniforms: { uT: { value: 0 }, uOn: { value: 0 }, uCor: { value: new THREE.Color(COR.corrente) } },
    vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
    fragmentShader: `uniform float uT, uOn; uniform vec3 uCor; varying vec2 vUv;
      void main(){
        float tr = 0.0, cab = 0.0;
        for (int j = 0; j < ${RS.quantidade}; j++) {
          float d = fract(fract(uT / ${RS.periodo_s.toFixed(4)} + float(j) / ${RS.quantidade.toFixed(1)}) - vUv.x);
          tr = max(tr, exp(-d / ${RS.cauda.toFixed(4)})); cab = max(cab, exp(-d / 0.01));
        }
        gl_FragColor = vec4(mix(uCor, vec3(1.0), 0.3 * cab), uOn * tr);
      }`,
    transparent: true, depthWrite: false,
  });
  // TorusGeometry: uv.x percorre o anel maior (0 → 1), que é o caminho do rastro.
  obj.add(new THREE.Mesh(new THREE.TorusGeometry(R, 0.085, 8, 200), matRastro));

  // Campo = anel magenta concêntrico com pulsos correndo no sentido da grandeza (sem setas 3D).
  const matCampo = new THREE.ShaderMaterial({
    uniforms: { uT: { value: 0 }, uA: { value: 0 }, uCor: { value: new THREE.Color(COR.campo) } },
    vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
    fragmentShader: `uniform float uT, uA; uniform vec3 uCor; varying vec2 vUv;
      void main(){ float x = fract(vUv.x * 3.0 - uT * 0.25); float p = exp(-(1.0 - x) / 0.07);
        gl_FragColor = vec4(mix(uCor, vec3(1.0), 0.2 * p), uA * (0.5 + 0.6 * p)); }`,
    transparent: true, depthWrite: false,
  });
  obj.add(new THREE.Mesh(new THREE.TorusGeometry(R * 0.7, 0.016, 6, 200), matCampo));

  // ---------- estrelas (cena separada, fov fixo) ----------
  const ceu = new THREE.Scene(), camCeu = new THREE.PerspectiveCamera(40, W / H, 1, 1000);
  {
    let s = 29; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };   // determinístico
    const pos = [], cor = [];
    for (let i = 0; i < 700; i++) {
      const u = 2 * rnd() - 1, th = 2 * PI * rnd(), q = Math.sqrt(1 - u * u), b = 0.25 + 0.55 * rnd() ** 2;
      pos.push(400 * q * Math.cos(th), 400 * q * Math.sin(th), 400 * u); cor.push(b, b, b);
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    geo.setAttribute('color', new THREE.Float32BufferAttribute(cor, 3));
    ceu.add(new THREE.Points(geo, new THREE.PointsMaterial({ size: 1.6, sizeAttenuation: false, vertexColors: true })));
  }

  // ---------- câmera por modos + dolly-zoom alinhado ao Manim ----------
  // 'alt' = altura visível (unid. 3D) no plano do alvo. Com alt = 16/K, 1 unidade do Manim = 1/K unidade 3D.
  // 'yc' = em que altura do quadro do Manim (unid., de −8 a 8) o alvo aparece.
  const camera = new THREE.PerspectiveCamera(30, W / H, 0.05, 3000);
  function estado(modo, t) {
    if (modo === 'topo') return { az: -90, el: 90, fov: 8, alt: 16 / K, alvo: [0, 0, 0], yc: G.centro_topo_manim[1] };
    return { az: -110 + 5 * t, el: 25, fov: 30, alt: 16 / K * 1.05, alvo: [0, 0, 0], yc: G.centro_orbita_manim_y };  // órbita 5°/s
  }
  function misturaCamera(t) {
    const L = TL.camera; let i = 0;
    while (i < L.length - 2 && t > L[i + 1].t) i++;
    const a = L[i], b = L[i + 1], u = suave(clamp((t - a.t) / Math.max(b.t - a.t, 1e-9), 0, 1));
    const e0 = estado(a.modo, t), e1 = estado(b.modo, t), lerp = (x, y) => x + (y - x) * u;
    const dAz = ((e1.az - e0.az) % 360 + 540) % 360 - 180;
    return { az: e0.az + dAz * u, el: lerp(e0.el, e1.el), fov: lerp(e0.fov, e1.fov), alt: lerp(e0.alt, e1.alt),
      alvo: e0.alvo.map((v, k) => lerp(v, e1.alvo[k])), yc: lerp(e0.yc, e1.yc) };
  }
  function posicionaCamera(c) {
    const az = c.az * PI / 180, el = c.el * PI / 180, D = (c.alt / 2) / Math.tan(c.fov * PI / 360);
    const alvo = new THREE.Vector3(...c.alvo);
    camera.fov = c.fov;
    camera.position.set(alvo.x + D * Math.cos(el) * Math.cos(az), alvo.y + D * Math.cos(el) * Math.sin(az), alvo.z + D * Math.sin(el));
    camera.up.set(-Math.sin(el) * Math.cos(az), -Math.sin(el) * Math.sin(az), Math.cos(el));
    camera.lookAt(alvo);
    camera.near = Math.max(0.05, D - 10); camera.far = D + 10;
    camera.setViewOffset(W, H, 0, c.yc / 16 * H, W, H);        // desloca a janela: o alvo vai para y = yc
    camCeu.quaternion.copy(camera.quaternion);
  }

  // ---------- quadro ----------
  window.setFrame = function (f) {
    const t = f / FPS, E = TL.eventos;
    obj.scale.setScalar(0.85 + 0.15 * rampa(t, E.surge, 1.2));
    matRastro.uniforms.uT.value = t; matRastro.uniforms.uOn.value = rampa(t, E.corrente_liga, 0.8);
    const realce = chaves(TL.realce_3d, t, 'v');                 // 1 = o 3D recua para o Manim falar
    matAco.color.set(COR.aco).multiplyScalar(1 - 0.45 * realce);
    matCampo.uniforms.uT.value = t; matCampo.uniforms.uA.value = rampa(t, E.campo_acende, 1.0) * (1 - 0.65 * realce);
    posicionaCamera(misturaCamera(t));
    renderer.clear(); renderer.render(ceu, camCeu); renderer.clearDepth(); renderer.render(scene, camera);
    return true;
  };
  window.projeta = p => { const v = new THREE.Vector3(...p).project(camera); return [(v.x + 1) / 2 * W, (1 - v.y) / 2 * H]; };
  window.cenaPronta = true;
})();
