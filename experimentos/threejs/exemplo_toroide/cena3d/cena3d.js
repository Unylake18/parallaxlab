// vid_0029 — toroide 3D (Three.js r128). Tudo é função do quadro: window.setFrame(f), sem relógio.
// window.TIMELINE (timeline.json) e window.FPS são injetados pelo render3d.js antes do carregamento.
(function () {
  const TL = window.TIMELINE, FPS = window.FPS || 15, G = TL.geometria;
  const R = G.raio_maior, A = G.raio_menor, RF = G.raio_fio, N = G.n_espiras, PHI0 = G.phi0, K = G.fator_3d_manim;
  const COR = { corrente: 0x3FE08B, campo: 0xEA63FF, geo: 0xB8C4DA, aco: 0x7A8696, fundo: 0x050816 };
  const W = innerWidth, H = innerHeight, PI = Math.PI;

  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H); renderer.setClearColor(COR.fundo, 1); renderer.autoClear = false;
  document.body.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new THREE.RoomEnvironment(), 0.04).texture;
  const chave = new THREE.DirectionalLight(0xffffff, 1.7); chave.position.set(3, -4, 6);
  const contra = new THREE.DirectionalLight(COR.campo, 0.08); contra.position.set(-4, 5, 1.5);
  scene.add(chave, contra, new THREE.AmbientLight(0xffffff, 0.12));

  // ---------- funções de tempo (mesmas regras do cena.py) ----------
  const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
  const suave = u => u * u * (3 - 2 * u);
  const rampa = (t, t0, dur) => suave(clamp((t - t0) / dur, 0, 1));
  function chaves(lista, t, campo) {
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

  // ---------- enrolamento: hélice toroidal ----------
  // θ = π − 2πN s: no lado de dentro (θ = π) o fio sobe (+z) no sentido de s crescente, que é o sentido da corrente.
  class Helice extends THREE.Curve {
    getPoint(s, alvo = new THREE.Vector3()) {
      const phi = PHI0 + 2 * PI * s, th = PI - 2 * PI * N * s, rho = R + A * Math.cos(th);
      return alvo.set(rho * Math.cos(phi), rho * Math.sin(phi), A * Math.sin(th));
    }
  }
  const helice = new Helice();
  helice.arcLengthDivisions = N * 100;                       // uv.x do tubo = fração do comprimento do fio
  const SEG = N * 64;
  const toro = new THREE.Group(); scene.add(toro);
  const ACO = new THREE.Color(COR.aco), ENV_ACO = 0.35;
  const matFio = new THREE.MeshStandardMaterial({ color: COR.aco, metalness: 0.8, roughness: 0.45, envMapIntensity: ENV_ACO });
  toro.add(new THREE.Mesh(new THREE.TubeGeometry(helice, SEG, RF, 10, true), matFio));

  // Corrente = rastros de luz (cometas) num tubo envolvente; cor sólida (mistura normal).
  // Rastro: Δ = fração do fio atrás da cabeça; intensidade exp(−Δ/τ), τ = cauda_espiras/N; cabeça ~30% mais clara.
  // Contagens: o trecho de dentro da espira k (s ≈ k/N) e o de fora (s ≈ (k + ½)/N) acendem em t_k (timeline).
  const RS = TL.rastros, CD = TL.contagem_dentro, CF = TL.contagem_fora, liga0 = TL.eventos.corrente_liga;
  const f1 = x => x.toFixed(4);
  const matCorrente = new THREE.ShaderMaterial({
    uniforms: { uT: { value: 0 }, uOn: { value: 0 }, uGanho: { value: 1 }, uCor: { value: new THREE.Color(COR.corrente) } },
    vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
    fragmentShader: `
      uniform float uT, uOn, uGanho; uniform vec3 uCor; varying vec2 vUv;
      const float NE = ${f1(N)}, TAU_U = ${f1(RS.cauda_espiras / N)}, CAB_U = ${f1(0.15 / N)};
      float tk(float k, float t0, float dur, float ex){ return t0 + dur * pow(k / (NE - 1.0), ex); }
      void main(){
        float u = vUv.x;
        float c = cos(3.14159265 - 6.2831853 * NE * u);
        float dentro = 1.0 - smoothstep(-0.92, -0.62, c), fora = smoothstep(0.62, 0.92, c);
        float tr = 0.0, cab = 0.0;
        for (int j = 0; j < ${RS.quantidade}; j++) {
          float d = fract(fract(uT / ${f1(RS.periodo_s)} + float(j) / ${f1(RS.quantidade)}) - u);
          tr = max(tr, exp(-d / TAU_U)); cab = max(cab, exp(-d / CAB_U));
        }
        tr *= uOn; cab *= uOn;
        // Ligar: um rastro só percorre o fio inteiro e deixa o fio aceso por um instante.
        float h = (uT - ${f1(liga0)}) / ${f1(RS.liga_dur_s)}, tp = uT - (${f1(liga0)} + u * ${f1(RS.liga_dur_s)});
        float liga = tp >= 0.0 ? 0.55 * exp(-tp / 0.7) : 0.0, cabL = 0.0;
        if (h >= 0.0 && h <= 1.0 && u <= h) { liga = max(liga, exp(-(h - u) / TAU_U)); cabL = exp(-(h - u) / CAB_U); }
        float kin = mod(floor(u * NE + 0.5), NE), kout = floor(u * NE);
        float ti = tk(kin, ${f1(CD.inicio_s)}, ${f1(CD.dur_s)}, ${f1(CD.expoente)});
        float to = tk(kout, ${f1(CF.inicio_s)}, ${f1(CF.dur_s)}, ${f1(CF.expoente)});
        float litIn = smoothstep(ti, ti + 0.12, uT) * (1.0 - smoothstep(${f1(CD.apaga_s)}, ${f1(CD.apaga_s + 0.8)}, uT));
        float todos = smoothstep(${f1(CF.todos_dentro_s)}, ${f1(CF.todos_dentro_s + 0.4)}, uT) * (1.0 - smoothstep(${f1(CF.apaga_s)}, ${f1(CF.apaga_s + 0.8)}, uT));
        float litOut = smoothstep(to, to + 0.12, uT) * (1.0 - smoothstep(${f1(CF.apaga_s)}, ${f1(CF.apaga_s + 0.8)}, uT));
        float cnt = max(litIn, todos) * dentro + litOut * fora;
        float a = clamp(max(uGanho * max(tr, liga), cnt), 0.0, 1.0);
        float claro = clamp(max(uGanho * max(cab, cabL), cnt), 0.0, 1.0);
        gl_FragColor = vec4(mix(uCor, vec3(1.0), 0.3 * claro), a);
      }`,
    transparent: true, depthWrite: false,
  });
  toro.add(new THREE.Mesh(new THREE.TubeGeometry(helice, SEG, RF * 1.45, 8, true), matCorrente));

  // ---------- campo do MODELO IDEAL: anéis concêntricos ao eixo, só dentro da seção ----------
  // 3 raios × 3 alturas. Pulsos magenta correm no sentido de B (anti-horário visto de cima, +φ),
  // com velocidade ∝ 1/r; brilho base ∝ 1/r. Sem setas.
  const campo = [];
  [-0.6, 0, 0.6].forEach((o, i) => {
    const rho = R + A * o, forca = (R - A) / rho, w = 0.9 * forca / rho;   // w: rad/s
    [-0.5, 0, 0.5].forEach((hz, j) => {
      const mat = new THREE.ShaderMaterial({
        uniforms: { uT: { value: 0 }, uA: { value: 0 }, uCor: { value: new THREE.Color(COR.campo) } },
        vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
        fragmentShader: `uniform float uT, uA; uniform vec3 uCor; varying vec2 vUv;
          void main(){
            float x = fract(vUv.x * 3.0 - uT * ${f1(w * 3 / (2 * PI))} + ${f1(0.29 * i + 0.13 * j)});
            float p = exp(-(1.0 - x) / 0.07);
            gl_FragColor = vec4(mix(uCor, vec3(1.0), 0.2 * p), uA * ${f1(forca)} * (0.55 + 0.6 * p));
          }`,
        transparent: true, depthWrite: false,
      });
      const anel = new THREE.Mesh(new THREE.TorusGeometry(rho, 0.016, 6, 200), mat);
      anel.position.z = hz * A; toro.add(anel);
      campo.push(mat);
    });
  });

  // ---------- círculo amperiano (plano z = 0), raio vem do timeline em unidades do Manim ----------
  const matAmp = new THREE.ShaderMaterial({
    uniforms: { uN: { value: 8 }, uA: { value: 0 }, uRot: { value: 0 }, uCor: { value: new THREE.Color(COR.geo) } },
    vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
    fragmentShader: `uniform float uN, uA, uRot; uniform vec3 uCor; varying vec2 vUv;
      void main(){ if (fract((vUv.x - uRot / 6.2831853) * uN) > 0.5) discard; gl_FragColor = vec4(uCor, uA * 0.85); }`,
    transparent: true, depthWrite: false,
  });
  const amp = new THREE.Mesh(new THREE.BufferGeometry(), matAmp); scene.add(amp);
  let rAmpAnterior = -1;
  function atualizaAmperiano(t) {
    const r = chaves(TL.amperiano, t, 'r'), a = chaves(TL.amperiano, t, 'alpha');
    amp.visible = a > 0.001 && r > 0.02;
    if (!amp.visible) return;
    if (Math.abs(r - rAmpAnterior) > 1e-6) {
      amp.geometry.dispose();
      amp.geometry = new THREE.TorusGeometry(r / K, 0.011, 6, 256);
      rAmpAnterior = r;
    }
    matAmp.uniforms.uN.value = Math.max(8, Math.round(2 * PI * r / 0.22)); // mesma regra do Manim
    matAmp.uniforms.uA.value = a;
    // Giro rígido do B03 (mesma regra do cena.py): o tracejado gira junto com as setas do Manim.
    const gs = TL.giro_setas;
    matAmp.uniforms.uRot.value = gs.omega_rad_s * (clamp(t, gs.inicio_s, gs.fim_s) - gs.inicio_s);
  }

  // ---------- estrelas (cena separada, câmera de fov fixo: não "zoomam" no dolly) ----------
  const ceu = new THREE.Scene(), camCeu = new THREE.PerspectiveCamera(40, W / H, 1, 1000);
  {
    let semente = 29;
    const rnd = () => { semente = (semente * 16807) % 2147483647; return semente / 2147483647; };
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

  // ---------- câmera por modo; transições suaves entre chaves do timeline ----------
  const camera = new THREE.PerspectiveCamera(30, W / H, 0.05, 3000);
  const AZ0 = -90 - 20 - 5 * 28.5, OMEGA = 5;               // órbita lenta: 5°/s
  function estado(modo, t) {
    const orbita = { az: AZ0 + OMEGA * t, el: 25, fov: 30, alt: 16 / K * 1.05, alvo: [0, 0, 0], yc: G.centro_orbita_manim_y, preto: 0 };
    if (modo === 'topo') return { az: -90, el: 90, fov: 8, alt: 16 / K, alvo: [0, 0, 0], yc: G.centro_topo_manim[1], preto: 0 };
    if (modo === 'solenoide') return { az: -90, el: 8, fov: 30, alt: 4.2, alvo: [0, -R, 0], yc: G.centro_orbita_manim_y, preto: 0 };
    if (modo === 'preto') return Object.assign(orbita, { preto: 1 });
    return orbita;
  }
  function misturaCamera(t) {
    const L = TL.camera;
    let i = 0;
    while (i < L.length - 2 && t > L[i + 1].t) i++;
    const a = L[i], b = L[i + 1], u = suave(clamp((t - a.t) / Math.max(b.t - a.t, 1e-9), 0, 1));
    const e0 = estado(a.modo, t), e1 = estado(b.modo, t);
    const dAz = ((e1.az - e0.az) % 360 + 540) % 360 - 180;    // menor ângulo
    const lerp = (x, y) => x + (y - x) * u;
    return { az: e0.az + dAz * u, el: lerp(e0.el, e1.el), fov: lerp(e0.fov, e1.fov), alt: lerp(e0.alt, e1.alt),
      alvo: e0.alvo.map((v, k) => lerp(v, e1.alvo[k])), yc: lerp(e0.yc, e1.yc), preto: lerp(e0.preto, e1.preto) };
  }
  function posicionaCamera(c) {
    // Dolly-zoom: a altura visível no plano do alvo é 'alt' (unid. 3D) para qualquer fov.
    const az = c.az * PI / 180, el = c.el * PI / 180, D = (c.alt / 2) / Math.tan(c.fov * PI / 360);
    const alvo = new THREE.Vector3(...c.alvo);
    camera.fov = c.fov;
    camera.position.set(alvo.x + D * Math.cos(el) * Math.cos(az), alvo.y + D * Math.cos(el) * Math.sin(az), alvo.z + D * Math.sin(el));
    camera.up.set(-Math.sin(el) * Math.cos(az), -Math.sin(el) * Math.sin(az), Math.cos(el));
    camera.lookAt(alvo);
    camera.near = Math.max(0.05, D - 10); camera.far = D + 10;
    // O alvo aparece em y = yc (unid. do Manim, quadro de 16 de altura): janela deslocada para baixo.
    camera.setViewOffset(W, H, 0, c.yc / 16 * H, W, H);
    camCeu.quaternion.copy(camera.quaternion);
    renderer.domElement.style.opacity = String(1 - c.preto);
  }

  // ---------- quadro ----------
  window.setFrame = function (f) {
    const t = f / FPS, E = TL.eventos;
    const surge = rampa(t, E.toroide_surge, 1.2);
    toro.scale.setScalar(0.85 + 0.15 * surge);
    matFio.transparent = surge < 1; matFio.opacity = surge;

    const realce = chaves(TL.realce_3d, t, 'v');            // 1 = modo contagem (o 3D recua)
    matFio.color.copy(ACO).multiplyScalar(1 - 0.45 * realce);
    matFio.envMapIntensity = ENV_ACO * (1 - 0.45 * realce);
    const U = matCorrente.uniforms;
    U.uT.value = t;
    U.uOn.value = rampa(t, liga0 + RS.liga_dur_s, RS.entrada_s);
    U.uGanho.value = 1 - 0.6 * realce;
    const acende = rampa(t, E.campo_acende, 1.0) * (1 - 0.65 * realce);
    for (const m of campo) { m.uniforms.uT.value = t; m.uniforms.uA.value = 0.95 * acende; }
    atualizaAmperiano(t);
    posicionaCamera(misturaCamera(t));

    renderer.clear();
    renderer.render(ceu, camCeu);
    renderer.clearDepth();
    renderer.render(scene, camera);
    return true;
  };
  // QA: pixel de um ponto 3D no quadro atual (para medir o alinhamento com o Manim).
  window.projeta = p => { const v = new THREE.Vector3(...p).project(camera); return [(v.x + 1) / 2 * W, (1 - v.y) / 2 * H]; };
  window.cenaPronta = true;
})();
