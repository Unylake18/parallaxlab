// vid_0031 v7 — halo de 22° (Three.js r128). Tudo é função do quadro: window.setFrame(f), sem relógio.
// window.TIMELINE (timeline.json) e window.FPS são injetados pelo render3d.js antes do carregamento.
// Camadas: fundo (gradiente escuro do céu + nuvem leve, sempre por baixo); céu com halo, poste e véu (C01, C02, fim do C08);
// campo de cristais com um cristal-herói preso à câmera (C02); cristal 2.5D com o feixe e o fantasma (C04–C07, C09), cujo estado
// por quadro (vértices da face da frente, pontos do feixe) vem do timeline (roteiro.py): o feixe é UMA malha atualizada no lugar.
(function () {
  const TL = window.TIMELINE, FPS = window.FPS || 15, E = TL.eventos, C = TL.ceu, CR = TL.cristal, HE = TL.heroi;
  const W = innerWidth, H = innerHeight, PI = Math.PI;
  const COR = { fundo: 0x050816, gelo: 0x9CC7FF, ciano: 0x35D9FF };

  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H); renderer.setClearColor(COR.fundo, 1); renderer.autoClear = false;
  document.body.appendChild(renderer.domElement);

  // ---------- tempo (mesmas regras do roteiro.py) ----------
  const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
  const suave = u => { u = clamp(u, 0, 1); return u * u * (3 - 2 * u); };
  const rampa = (t, t0, dur) => suave((t - t0) / dur);
  function chaves(lista, t) {
    if (t <= lista[0].t) return lista[0].v;
    for (let i = 0; i < lista.length - 1; i++) {
      const a = lista[i], b = lista[i + 1];
      if (t <= b.t) return a.v + (b.v - a.v) * suave((t - a.t) / Math.max(b.t - a.t, 1e-9));
    }
    return lista[lista.length - 1].v;
  }
  let semente = 31;
  const rnd = () => { semente = (semente * 16807) % 2147483647; return semente / 2147483647; };
  const f4 = x => x.toFixed(6);
  const camOrto = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  const RUIDO = `
      float h(vec2 q){ return fract(sin(dot(q, vec2(127.1, 311.7))) * 43758.5453); }
      float ruido(vec2 q){ vec2 i = floor(q), f = fract(q); f = f * f * (3.0 - 2.0 * f);
        return mix(mix(h(i), h(i + vec2(1, 0)), f.x), mix(h(i + vec2(0, 1)), h(i + vec2(1, 1)), f.x), f.y); }
      float fbm(vec2 q){ float s = 0.0, a = 0.5; for (int k = 0; k < 5; k++){ s += a * ruido(q); q *= 2.03; a *= 0.5; } return s; }`;

  // ---------- fundo: gradiente escuro do céu (azul-noite → azul do C01, bem escuro) com nuvem muito leve ----------
  const matFundo = new THREE.ShaderMaterial({
    uniforms: { uT: { value: 0 } },
    vertexShader: 'void main(){ gl_Position = vec4(position.xy, 0.0, 1.0); }',
    fragmentShader: `uniform float uT; ${RUIDO}
      void main(){
        vec2 p = gl_FragCoord.xy / vec2(${W.toFixed(1)}, ${H.toFixed(1)});
        vec3 cor = mix(vec3(0.020, 0.031, 0.075), vec3(0.055, 0.095, 0.175), pow(p.y, 1.3));
        float n = fbm(vec2(p.x * 3.0 + 0.01 * uT, p.y * 5.0 - 0.004 * uT));
        cor += vec3(0.035, 0.045, 0.065) * smoothstep(0.45, 0.85, n) * (0.4 + 0.6 * p.y);
        gl_FragColor = vec4(cor, 1.0);
      }`,
    depthTest: false, depthWrite: false,
  });
  const cenaFundo = new THREE.Scene(); cenaFundo.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), matFundo));

  // ---------- céu: quad de tela cheia; cada pixel vira uma direção (projeção retilínea, igual ao roteiro.py) ----------
  const perfil = TL.perfil_anel, NP = perfil.rgb.length;
  const dados = new Uint8Array(NP * 4);
  perfil.rgb.forEach((c, i) => { dados.set([c[0] * 255, c[1] * 255, c[2] * 255, 255].map(Math.round), 4 * i); });
  const texPerfil = new THREE.DataTexture(dados, NP, 1, THREE.RGBAFormat);
  texPerfil.magFilter = texPerfil.minFilter = THREE.LinearFilter; texPerfil.needsUpdate = true;
  const tanH = Math.tan(C.fov_h_deg * PI / 360), tanV = tanH * 16 / 9;
  const matCeu = new THREE.ShaderMaterial({
    uniforms: { uT: { value: 0 }, uA: { value: 1 }, uPosteX: { value: 99 }, uPosteA: { value: 1 }, uPerfil: { value: texPerfil },
                uDebug: { value: 0 }, uPitch: { value: C.pitch_deg * PI / 180 }, uVeu: { value: 0 },
                uEsc: { value: 1 }, uTr: { value: new THREE.Vector2(0, 0) }, uChao: { value: 1 }, uSolA: { value: 1 }, uAcende: { value: 1 }, uLugar: { value: 0 },
                uSol: { value: new THREE.Vector3(...C.sol_dir) } },
    vertexShader: 'void main(){ gl_Position = vec4(position.xy, 0.0, 1.0); }',
    fragmentShader: `
      uniform float uT, uA, uPosteX, uPosteA, uDebug, uPitch, uVeu, uEsc, uChao, uSolA, uAcende, uLugar; uniform vec2 uTr;
      uniform vec3 uSol; uniform sampler2D uPerfil; ${RUIDO}
      // halo (v4): zero por dentro de 21,6°; borda de dentro avermelhada (21,6–22°); pico branco-quente (22–22,6°); cauda azulada até ~25°
      vec3 halo(float a){
        if (a < 21.6) return vec3(0.0);
        float sobe = smoothstep(21.6, 22.0, a);
        float desce = a < 22.6 ? 1.0 : exp(-(a - 22.6) / 0.9);
        float f = sobe * desce * (1.0 - smoothstep(24.2, 25.6, a));
        vec3 tom = a < 22.0 ? mix(vec3(1.0, 0.52, 0.36), vec3(1.0, 0.95, 0.86), smoothstep(21.8, 22.1, a))
                            : mix(vec3(1.0, 0.95, 0.88), vec3(0.82, 0.9, 1.0), smoothstep(22.6, 23.6, a));
        return f * tom;
      }
      void main(){
        vec2 ms = vec2((gl_FragCoord.x / ${W.toFixed(1)} - 0.5) * 9.0, (gl_FragCoord.y / ${H.toFixed(1)} - 0.5) * 16.0);  // tela (Manim)
        vec2 m = (ms - uTr) / uEsc;                                                                                     // vista
        vec3 c = normalize(vec3(m.x / 4.5 * ${f4(tanH)}, m.y / 8.0 * ${f4(tanV)}, 1.0));
        float cp = cos(uPitch), sp = sin(uPitch);
        vec3 d = vec3(c.x, c.y * cp + c.z * sp, c.y * sp - c.z * cp);
        float el = asin(clamp(d.y, -1.0, 1.0));
        // azul saturado: zênite #1F5FAE, horizonte #9CC3E6; perto do horizonte um calor de verão
        vec3 cor = mix(vec3(0.612, 0.765, 0.902), vec3(0.122, 0.373, 0.682), pow(clamp(el / 1.25, 0.0, 1.0), 0.55));
        cor = mix(cor, vec3(1.0, 0.86, 0.68), 0.35 * exp(-max(el, 0.0) / 0.06));
        // véu de cirrostrato leitoso e fino (15–25 %)
        vec2 q = d.xz / max(d.y, 0.08) * 1.6 + vec2(0.035 * uT, 0.012 * uT);
        float veu = smoothstep(0.35, 0.85, fbm(q)) * 0.6 + 0.25 * fbm(q * 3.0 + 7.0);
        cor = mix(cor, vec3(0.93, 0.95, 0.99), (0.20 + 0.6 * uVeu) * veu * smoothstep(-0.02, 0.15, el));
        // v7 (C04): com a altura o céu escurece e satura (azul-médio → azul-profundo); os cristais claros ganham contraste
        cor = mix(cor, vec3(0.020, 0.105, 0.330), 0.78 * uVeu * smoothstep(0.0, 0.9, el));
        // halo: luz no véu, pico ≈ 1,45× o céu
        float a = degrees(acos(clamp(dot(d, uSol), -1.0, 1.0)));
        vec3 hh = halo(a);
        float rRev = 21.4 + 5.0 * uAcende;                                     // o halo acende da borda de dentro para fora
        hh *= clamp(uAcende * 3.0, 0.0, 1.0) * (1.0 - smoothstep(rRev - 0.5, rRev, a));
        // halo: puxa a cor do céu para o tom do anel com brilho ≈ 1,45× o do céu, e só onde há véu (luz no véu, não neon)
        float fh = length(hh) / 1.6;
        vec3 tomh = hh / max(fh * 1.6, 1e-4);
        float Ys = dot(cor, vec3(0.3, 0.59, 0.11)), Yt = dot(tomh, vec3(0.3, 0.59, 0.11));
        cor = mix(cor, tomh * (1.45 * Ys / max(Yt, 1e-3)), clamp(fh * 0.9 * (0.55 + 0.8 * veu), 0.0, 0.92));
        // Sol: clarão quente (#FFC857 → transparente) e disco
        vec3 quente = vec3(1.0, 0.784, 0.341);
        cor = mix(cor, quente, uSolA * 0.62 * exp(-a / 3.4));
        cor += uSolA * vec3(1.0, 0.93, 0.75) * 0.5 * exp(-a / 0.7);
        cor = mix(cor, vec3(1.0, 0.97, 0.9), uSolA * smoothstep(0.34, 0.24, a));                     // núcleo quente pequeno
        // v6: flare leve (estrela de 4 pontas + 2 diagonais fracas, na tela) em volta do Sol
        vec2 dv = m - vec2(${C.sol_manim[0].toFixed(3)}, ${C.sol_manim[1].toFixed(3)});
        float fl = exp(-abs(dv.y) / 0.016) * exp(-abs(dv.x) / 0.38) + exp(-abs(dv.x) / 0.016) * exp(-abs(dv.y) / 0.38);
        vec2 dg = vec2(dv.x + dv.y, dv.x - dv.y) * 0.7071;
        fl += 0.4 * (exp(-abs(dg.y) / 0.012) * exp(-abs(dg.x) / 0.22) + exp(-abs(dg.x) / 0.012) * exp(-abs(dg.y) / 0.22));
        cor += uSolA * vec3(1.0, 0.94, 0.82) * 0.55 * fl;
        // horizonte: silhuetas quentes (árvores e casas) sobre a linha do chão distante
        float az = atan(d.x, -d.z) * 57.2958;
        float arv = 1.2 + 2.6 * fbm(vec2(az * 0.22, 3.0)) + 3.0 * step(0.74, fbm(vec2(az * 0.05, 9.0)));
        float casa = step(0.5, fract(az / 7.0)) * step(fract(az / 23.0), 0.35) * 2.6;
        float h_sil = radians(max(arv, casa));
        float sil = smoothstep(0.002, -0.002, el - h_sil + 0.004);
        vec3 terra = mix(vec3(0.70, 0.40, 0.16), vec3(0.32, 0.16, 0.07), clamp(-el / 0.5, 0.0, 1.0));   // chão de verão (quente, C04)
        cor = mix(cor, terra, smoothstep(0.002, -0.002, el));
        cor = mix(cor, vec3(0.14, 0.10, 0.09), sil * step(-0.002, el));                               // silhuetas no horizonte
        // poste em silhueta (vista): tampa o disco do Sol
        float px = uPosteX, w = ${(C.poste.largura_manim / 2).toFixed(3)}, topo = ${C.poste.topo_manim.toFixed(3)};
        float poste = step(abs(m.x - px), w * (1.0 - 0.12 * clamp((topo - m.y) / 14.0, 0.0, 1.0)) ) * step(m.y, topo);
        poste = max(poste, step(abs(m.y - (topo - 0.25)), 0.07) * step(px - 1.6, m.x) * step(m.x, px));
        poste = max(poste, step(length((m - vec2(px - 1.6, topo - 0.38)) * vec2(1.0, 1.8)), 0.24) * step(m.y, topo - 0.32));
        cor = mix(cor, vec3(0.09, 0.08, 0.09), poste * uPosteA);
        // lugares do hook (C01): o mesmo céu e o mesmo anel, horizontes diferentes no primeiro plano (vista)
        int lug = int(uLugar + 0.5);
        float borda = -4.45 + 0.10 * sin(m.x * 0.9 + 1.3) + 0.05 * sin(m.x * 2.3);
        vec3 corChao = vec3(0.17, 0.13, 0.13);
        if (lug == 1) {                                   // praia: mar na linha do horizonte, areia, coqueiro
          borda = -4.45 + 0.03 * sin(m.x * 1.7);
          cor = mix(cor, vec3(0.16, 0.42, 0.62), smoothstep(-4.18, -4.22, m.y) * uChao);
          corChao = vec3(0.62, 0.50, 0.33);
          float u = clamp((m.y + 4.45) / 3.6, 0.0, 1.0);
          float tronco = step(abs(m.x - (2.75 + 0.38 * u * u)), 0.10 - 0.04 * u) * step(m.y, -0.85) * step(-4.45, m.y);
          vec2 copa = vec2(3.13, -0.85); float fol = 0.0;
          for (int k = 0; k < 6; k++) {
            float ak = 0.4 + float(k) * 0.9 - (float(k) > 2.5 ? 0.3 : 0.0);
            vec2 d0 = m - copa - 0.55 * vec2(cos(ak), sin(ak) * 0.6 - 0.15);
            vec2 q2 = vec2(cos(ak) * d0.x + sin(ak) * d0.y, -sin(ak) * d0.x + cos(ak) * d0.y);
            fol = max(fol, step((q2.x / 0.62) * (q2.x / 0.62) + (q2.y / 0.10) * (q2.y / 0.10), 1.0));
          }
          cor = mix(cor, vec3(0.10, 0.11, 0.10), max(tronco, fol) * uChao);
        } else if (lug == 2) {                            // montanha nevada
          corChao = vec3(0.16, 0.17, 0.22);
          float mont = 0.0, neve = 0.0;
          vec3 pk[3]; pk[0] = vec3(-3.0, -1.9, 0.95); pk[1] = vec3(0.9, -2.6, 0.85); pk[2] = vec3(3.6, -1.7, 1.0);
          for (int k = 0; k < 3; k++) {
            float topo = pk[k].y - pk[k].z * abs(m.x - pk[k].x);
            float dentro = step(m.y, topo);
            mont = max(mont, dentro);
            neve = max(neve, dentro * step(pk[k].y - 0.55, m.y));
          }
          cor = mix(cor, mix(vec3(0.30, 0.34, 0.44), vec3(0.93, 0.95, 0.99), neve), mont * uChao);
        } else if (lug == 3) {                            // cidade
          corChao = vec3(0.12, 0.12, 0.15);
          float cel = floor(m.x / 0.52), fx = fract(m.x / 0.52);
          float alt = -4.45 + 0.7 + 1.9 * fract(sin(cel * 12.9898) * 43758.5453);
          float pr = step(m.y, alt) * step(0.06, fx) * step(fx, 0.94);
          float jan = pr * step(0.6, fract(sin(dot(floor(m * vec2(9.0, 7.0)), vec2(12.9898, 78.233))) * 43758.5453))
                      * step(0.3, fract(m.x * 9.0)) * step(0.3, fract(m.y * 7.0));
          cor = mix(cor, vec3(0.11, 0.12, 0.17), pr * uChao);
          cor = mix(cor, vec3(1.0, 0.85, 0.55), 0.55 * jan * uChao);
        } else if (lug == 4) {                            // campo aberto
          corChao = vec3(0.26, 0.33, 0.17);
          float arv = 0.0;
          for (int k = 0; k < 4; k++) {
            vec2 c0 = vec2(-3.4 + 2.3 * float(k), -4.0 + 0.05 * float(k));
            arv = max(arv, step(length((m - c0 - vec2(0.0, 0.28)) * vec2(1.0, 1.25)), 0.22));
            arv = max(arv, step(abs(m.x - c0.x), 0.03) * step(c0.y - 0.45, m.y) * step(m.y, c0.y + 0.1));
          }
          cor = mix(cor, vec3(0.13, 0.17, 0.10), arv * uChao);
        }
        float chao = smoothstep(borda + 0.02, borda - 0.02, m.y) * uChao;
        cor = mix(cor, mix(corChao, corChao * 0.45, clamp((borda - m.y) / 3.0, 0.0, 1.0)), chao);
        cor = mix(cor, vec3(0.95, 0.96, 0.99), 0.12 * uVeu);
        if (uDebug > 0.5 && abs(a - ${C.borda_interna_deg.toFixed(4)}) < 0.04) cor = vec3(1.0, 0.0, 0.0);
        gl_FragColor = vec4(cor, uA);
      }`,
    transparent: true, depthTest: false, depthWrite: false,
  });
  const cenaCeu = new THREE.Scene(); cenaCeu.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), matCeu));

  // ---------- prismas hexagonais ----------
  const ambiente = new THREE.PMREMGenerator(renderer).fromScene(new THREE.RoomEnvironment(), 0.04).texture;
  function prisma(raio, alt, corpoOp, envI, grossa) {
    const g = new THREE.CylinderGeometry(raio, raio, alt, 6, 1);
    const corpo = new THREE.MeshStandardMaterial({ color: 0xCFE8FF, metalness: 0, roughness: 0.15, transparent: true,
      opacity: corpoOp, envMapIntensity: envI, depthWrite: false, side: THREE.DoubleSide, emissive: 0x16304a });
    const arestas = new THREE.LineBasicMaterial({ color: COR.gelo, transparent: true, opacity: 0.9 });
    const grupo = new THREE.Group();
    grupo.add(new THREE.Mesh(g, corpo));
    if (grossa) {                                   // v7: arestas em cilindros finos (≥ 2 px a 540 px; linhas de 1 px não passam)
      const arM = new THREE.MeshBasicMaterial({ color: 0x9CC7FF, transparent: true, opacity: 0.95, depthWrite: false });
      const pos = new THREE.EdgesGeometry(g).attributes.position, Y = new THREE.Vector3(0, 1, 0);
      for (let k = 0; k < pos.count; k += 2) {
        const a = new THREE.Vector3().fromBufferAttribute(pos, k), b = new THREE.Vector3().fromBufferAttribute(pos, k + 1);
        const d = b.clone().sub(a), m = new THREE.Mesh(new THREE.CylinderGeometry(grossa, grossa, d.length(), 5, 1), arM);
        m.position.copy(a.clone().add(b).multiplyScalar(0.5)); m.quaternion.setFromUnitVectors(Y, d.normalize()); grupo.add(m);
      }
      grupo.userData = { corpo, arestas: arM, op: corpoOp };
      return grupo;
    }
    grupo.add(new THREE.LineSegments(new THREE.EdgesGeometry(g), arestas));
    grupo.userData = { corpo, arestas, op: corpoOp };
    return grupo;
  }
  const luz = new THREE.DirectionalLight(0xffffff, 1.2); luz.position.set(-3, 5, 4);

  // campo de cristais (C02) + herói preso à câmera (barra de escala do Manim)
  const cena = new THREE.Scene(); cena.environment = ambiente;
  cena.add(luz, new THREE.AmbientLight(0xffffff, 0.25));
  const campo = new THREE.Group(); cena.add(campo);
  const cristais = [];
  for (let i = 0; i < 38; i++) {
    const coluna = rnd() < 0.6, s = 0.42 + 0.34 * rnd();
    const g = coluna ? prisma(0.5 * s, 2 * s, 0.30, 0.6, 0.013) : prisma(0.62 * s, 0.35 * s, 0.30, 0.6, 0.013);
    g.position.set((rnd() - 0.5) * 8, (rnd() - 0.5) * 9, -rnd() * 6);
    const eixo = new THREE.Vector3(rnd() - 0.5, rnd() - 0.5, rnd() - 0.5).normalize();
    g.userData.giro = { eixo, ang0: rnd() * 2 * PI, w: (0.08 + 0.18 * rnd()) * (rnd() < 0.5 ? -1 : 1) };
    campo.add(g); cristais.push(g);
  }
  const camera = new THREE.PerspectiveCamera(40, W / H, 0.05, 500);
  cena.add(camera);
  const DZ = 6, tV40 = Math.tan(20 * PI / 180), tH40 = tV40 * W / H, U = tV40 * DZ / 8;   // U: unidades do mundo por unidade Manim
  const heroi = prisma(HE.raio_manim * U, HE.comprimento * HE.raio_manim * U, 0.2, 0.6);
  heroi.position.set(HE.centro_manim[0] / 4.5 * tH40 * DZ, HE.centro_manim[1] / 8 * tV40 * DZ, -DZ);
  camera.add(heroi); heroi.visible = false;              // v4: a escala saiu (o cristal aparece na lupa do C02)

  // ---------- cristal 2.5D (C04–C07, C09): coluna com o eixo em z; a face da frente (z = +L/2) é o hexágono do Manim ----------
  const cenaCr = new THREE.Scene(); cenaCr.environment = ambiente;
  const luzCr = new THREE.DirectionalLight(0xffffff, 1.0); luzCr.position.set(-2, 3, 6);
  cenaCr.add(luzCr, new THREE.AmbientLight(0xffffff, 0.35));
  const L = CR.comprimento_3d, L2 = L / 2;
  const cr = prisma(CR.raio_3d, L, 0.06, 0.0); cr.children[0].material.roughness = 0.6;   // sem reflexo cinza do ambiente
  cr.children[0].material.color.set(0x000000); cr.children[0].material.emissive.set(0x7cc4ff); cr.children[0].material.side = THREE.FrontSide;   // gelo azul (sem cinza)
  cr.rotation.x = PI / 2;                                  // vértices em 30° + 60°k (ponta para cima) com θ = 0
  const crGiro = new THREE.Group(); crGiro.add(cr); cenaCr.add(crGiro);
  const frente = new THREE.Mesh(new THREE.CircleGeometry(CR.raio_3d, 6), new THREE.MeshBasicMaterial({ color: 0x9CC7FF,
    transparent: true, opacity: 0.07, depthWrite: false }));
  frente.rotation.z = PI / 2; frente.position.z = L2 + 0.001; crGiro.add(frente);
  const camCr = new THREE.PerspectiveCamera(CR.fov_v_deg, W / H, 0.05, 500);

  // feixe e fantasma: fitas (uma malha cada, buffers fixos, atualizadas no lugar)
  const MAXSEG = 8;
  function fita(tracejada) {
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(MAXSEG * 6 * 3), 3));
    geo.setAttribute('aX', new THREE.BufferAttribute(new Float32Array(MAXSEG * 6), 1));
    geo.setAttribute('aS', new THREE.BufferAttribute(new Float32Array(MAXSEG * 6), 1));
    geo.setAttribute('aCor', new THREE.BufferAttribute(new Float32Array(MAXSEG * 6 * 3), 3));
    geo.setAttribute('aA', new THREE.BufferAttribute(new Float32Array(MAXSEG * 6), 1));
    const mat = new THREE.ShaderMaterial({
      uniforms: { uA: { value: 1 }, uNucleo: { value: 0.25 } },
      vertexShader: `attribute float aX, aS, aA; attribute vec3 aCor; varying float vX, vS, vA; varying vec3 vCor;
        void main(){ vX = aX; vS = aS; vA = aA; vCor = aCor; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
      fragmentShader: `uniform float uA, uNucleo; varying float vX, vS, vA; varying vec3 vCor;
        void main(){
          ${tracejada ? 'if (mod(vS, 0.26) > 0.15) discard;' : ''}
          float x = abs(vX);
          float nucleo = exp(-pow(x / uNucleo, 2.0));
          float halo = 0.28 * exp(-pow(x / 0.55, 2.0));
          float a = clamp(nucleo + halo, 0.0, 1.0) * vA * uA;
          vec3 cor = mix(vCor, vec3(1.0), 0.55 * nucleo);
          gl_FragColor = vec4(cor * a, a);
        }`,
      transparent: true, depthTest: false, depthWrite: false,
      blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: THREE.OneMinusSrcAlphaFactor,
    });
    const m = new THREE.Mesh(geo, mat); m.frustumCulled = false; cenaCr.add(m);
    return m;
  }
  const feixe = fita(false), fantasma = fita(true);
  const QUENTE = [1.0, 0.784, 0.341], DENTRO = [0.62, 0.93, 1.0], FANT = [0.66, 0.93, 1.0];   // luz do Sol #FFC857

  function dentroHex(p, v) {        // p e v em unidades Manim (vértices anti-horários)
    for (let k = 0; k < 6; k++) {
      const a = v[k], b = v[(k + 1) % 6];
      if ((b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) < 0) return false;
    }
    return true;
  }
  // escreve a fita a partir de pontos Manim; prog ∈ [0,1] corta no comprimento; fadeFim apaga o último trecho
  function escreveFita(m, st, pts, prog, alpha, fadeFim, cores) {
    const G = m.geometry.attributes;
    const pos = G.position.array, ax = G.aX.array, as = G.aS.array, ac = G.aCor.array, aa = G.aA.array;
    pos.fill(0); aa.fill(0);
    const R = st.R, c = st.c, meia = 0.21 / R;               // meia largura total da fita (halo) em unidades do mundo
    const mund = p => [(p[0] - c[0]) / R, (p[1] - c[1]) / R];
    let total = 0; const seg = [];
    for (let i = 0; i < pts.length - 1; i++) { const l = Math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]); seg.push(l); total += l; }
    let resta = prog * total, s0 = 0, n = 0;
    for (let i = 0; i < seg.length && resta > 1e-6 && n < MAXSEG; i++) {
      const fr = Math.min(1, resta / seg[i]); resta -= seg[i];
      const a = pts[i], b = [pts[i][0] + fr * (pts[i + 1][0] - pts[i][0]), pts[i][1] + fr * (pts[i + 1][1] - pts[i][1])];
      const A = mund(a), B = mund(b), dx = B[0] - A[0], dy = B[1] - A[1], l = Math.hypot(dx, dy) || 1e-6;
      const nx = -dy / l * meia, ny = dx / l * meia;
      const quad = [[A[0] + nx, A[1] + ny, 1, 0], [A[0] - nx, A[1] - ny, -1, 0], [B[0] + nx, B[1] + ny, 1, 1],
                    [A[0] - nx, A[1] - ny, -1, 0], [B[0] - nx, B[1] - ny, -1, 1], [B[0] + nx, B[1] + ny, 1, 1]];
      const cor = cores(dentroHex([(a[0] + b[0]) / 2, (a[1] + b[1]) / 2], st.v));
      const ultimo = i === seg.length - 1;
      quad.forEach((q, j) => {
        const k = n * 6 + j;
        pos.set([q[0], q[1], L2 + 0.02], 3 * k); ax[k] = q[2]; ac.set(cor, 3 * k);
        as[k] = s0 + q[3] * fr * seg[i];
        aa[k] = alpha * (fadeFim && ultimo ? 1 - q[3] * fr : 1.0);
      });
      s0 += seg[i]; n++;
    }
    for (const k of ['position', 'aX', 'aS', 'aCor', 'aA']) G[k].needsUpdate = true;
  }

  function posicionaCristal(st) {
    const R = st.R, c = st.c, d = CR.desloc_camera;
    const Dcam = (8 / R) / Math.tan(CR.fov_v_deg * PI / 360);
    camCr.fov = CR.fov_v_deg; camCr.position.set(d[0], d[1], L2 + Dcam); camCr.up.set(0, 1, 0);
    camCr.lookAt(d[0], d[1], 0); camCr.near = 0.05; camCr.far = Dcam + 10;
    const c0 = [c[0] + d[0] * R, c[1] + d[1] * R];
    camCr.setViewOffset(W, H, -c0[0] / 9 * W, c0[1] / 16 * H, W, H);
    if (st.caso === 'lupa') crGiro.rotation.set(0.62, st.th * PI / 180, 0.18);   // v7: gira devagar e mostra o corpo do prisma
    else crGiro.rotation.set(0, 0, st.th * PI / 180);
    crGiro.updateMatrixWorld(); camCr.updateMatrixWorld(); camCr.updateProjectionMatrix();
  }

  function posicionaCampo(t) {
    const u = rampa(t, E.c04 + 2.6, E.prisma - E.c04 - 2.6);
    camera.fov = 40; camera.up.set(0, 1, 0); camera.near = 0.05; camera.far = 500;
    camera.position.set(0.4 * (1 - u), 0.2, 13 - 6 * u); camera.lookAt(0, 0, -3);
    camera.setViewOffset(W, H, 0, 0, W, H); camera.updateProjectionMatrix();
  }

  // ---------- quadro ----------
  window.setFrame = function (f) {
    const t = f / FPS, K = TL.camadas;
    const aCeu = chaves(K.ceu, t), aCampo = chaves(K.cristais, t);
    renderer.clear();
    matFundo.uniforms.uT.value = t; renderer.render(cenaFundo, camOrto);
    if (aCeu > 0.002) {
      const U = matCeu.uniforms;
      U.uT.value = t; U.uA.value = aCeu;
      U.uPitch.value = (C.pitch_deg + chaves(K.inclina, t)) * PI / 180;
      U.uVeu.value = chaves(K.veu, t); U.uPosteA.value = chaves(K.poste, t); U.uChao.value = chaves(K.chao, t);
      U.uSolA.value = chaves(K.sol, t); U.uAcende.value = chaves(K.acende, t); U.uLugar.value = chaves(K.lugar, t);
      U.uEsc.value = chaves(K.esc, t); U.uTr.value.set(chaves(K.tx, t), chaves(K.ty, t));
      U.uPosteX.value = C.poste.x_final_manim;
      const faixa = chaves(K.faixa, t);                    // síntese: o céu só no andar de cima (y > 2,85)
      if (faixa > 0.5) { renderer.setScissorTest(true); renderer.setScissor(0, H * (8 + 2.72) / 16, W, H * (7.0 - 2.72) / 16); }
      renderer.render(cenaCeu, camOrto);
      renderer.setScissorTest(false);
    }
    if (aCampo > 0.002) {
      posicionaCampo(t);
      for (const g of cristais) {
        const G = g.userData;
        g.quaternion.setFromAxisAngle(G.giro.eixo, G.giro.ang0 + G.giro.w * t);
        G.corpo.opacity = G.op * aCampo; G.arestas.opacity = 0.9 * aCampo;
      }
      heroi.rotation.set(0.35 + 0.05 * t, 0.6 + 0.12 * t, 0.2);
      heroi.userData.corpo.opacity = heroi.userData.op * aCampo; heroi.userData.arestas.opacity = aCampo;
      renderer.setScissorTest(true); renderer.setScissor(0, H * 8.5 / 16, W, H * 6.5 / 16);   // só no alto (0,5 < y < 7): no véu, longe do cabeçalho
      renderer.clearDepth(); renderer.render(cena, camera);
      renderer.setScissorTest(false);
    }
    const q = f - CR.quadro_inicial, st = (q >= 0 && q < CR.quadros.length) ? CR.quadros[q] : null;
    if (st && st.a > 0.002) {
      posicionaCristal(st);
      const mc = cr.children[0].material, lupa = st.caso === 'lupa';
      mc.color.set(lupa ? 0x4F9CF0 : 0x000000); mc.emissive.set(lupa ? 0x123b66 : 0x7cc4ff); mc.side = lupa ? THREE.DoubleSide : THREE.FrontSide; mc.needsUpdate = true;
      cr.userData.corpo.opacity = (lupa ? 0.55 : 0.12) * st.a; cr.userData.arestas.opacity = (st.caso === 'lupa' ? 0.9 : 0.35) * st.a; frente.material.opacity = 0.0;
      feixe.visible = false; fantasma.visible = false;     // v5: o feixe é vetor no Manim (núcleo fino e nítido)
      renderer.clearDepth(); renderer.render(cenaCr, camCr);
    }
    return true;
  };
  // QA: vértices da face da frente projetados (câmera do cristal no quadro atual); contagem de objetos; borda do halo.
  window.verticesFrente = () => [...Array(6).keys()].map(k => {
    const a = (30 + 60 * k) * PI / 180, v = new THREE.Vector3(CR.raio_3d * Math.cos(a), CR.raio_3d * Math.sin(a), L2);
    crGiro.localToWorld(v); v.project(camCr); return [(v.x + 1) / 2 * W, (1 - v.y) / 2 * H];
  });
  window.objetosCristal = () => { let n = 0; cenaCr.traverse(() => n++); return n; };
  window.debugBorda = on => { matCeu.uniforms.uDebug.value = on ? 1 : 0; };
  window.cenaPronta = true;
})();
