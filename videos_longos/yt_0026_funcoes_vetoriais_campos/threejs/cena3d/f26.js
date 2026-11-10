// yt_0026: cenas 3D por estado (Three.js r128, base b3d.js copiada do yt_0022). Cena escolhida por window.CENA_ID (no .html).
// Fundo transparente: o Manim põe o fundo_calculo_liso atrás. Fórmulas, textos, rótulos e contadores são do Manim (projeta3d, a mesma câmera).
// Sistema visual v3 da série de Cálculo (handoff v4 §2.3): saída linear sem tone mapping; superfícies OPACAS com cor diferente em cada lado
// (fora #6E9EF0, dentro #35589E) e borda de luz (fresnel); luz chave com sombra + hemisférica + contraluz + preenchimento; linhas sobre
// superfícies em tubos com teste de profundidade; chão com sombra (ShadowMaterial) e o domínio projetado; setas com corpo (haste de raio
// 0,03 no mundo, cone largo, emissivo + borda de luz, cor pela intensidade); colunas em três tons fixos com aresta clara (estilo vid_0020).
//   'colunas'           — T5: z = 1,5 + 0,5·sen(1,5x)·cos(1,2y) sobre [0, 3] × [0, 2]; e.nivel 0..3 = colunas 6×4, 12×8, 24×16, 96×64
//                         (vão de 12%, arestas; a 96×64 sem vão nem aresta); e.nivel 4 = superfície sólida com paredes.
//   'caixa'             — T3: caixa fechada em três tons com uma fonte escondida; setas ciano saem pelas paredes (a parte de dentro fica
//                         escondida pela própria caixa). Seta i (i = 0..15): direção de Fibonacci (N = 30, z = 1 − (2i+1)/30), fase
//                         frac(0,618034·i)·S, velocidade V; a ponta cruza a parede a cada volta da fase (o Manim conta com a mesma conta).
//   'folha_paraboloide' — B4: disco de raio 2 no plano (u, v) com as duas famílias (passo 0,5) e as circunferências de raio 1 e 2;
//                         a folha sobe para z = s·(u² + v²). Tigela sólida, chão com sombra e o disco do domínio projetado.
//   'campo_espaco'      — B7: cascas de raio 1,25 / 1,75 / 2,25 com 14 / 22 / 30 direções de Fibonacci (cada casca girada, semente fixa);
//                         setas para a origem com 0,92/r²; fora as que fazem menos de 25° com a linha de visada do quadro de referência da
//                         órbita (azimute 95°, elevação 22°); três círculos máximos por casca; anel vazado no furo (pulsa no B7-2).
(function () {
  const B = B3D, T3 = THREE, PI = Math.PI, id = window.CENA_ID;
  const COR = { geo: 0xB8C4DA, e1: 0xFFC24D, e2: 0xEA63FF, fora: 0x6E9EF0, dentro: 0x35589E, linha: 0xDCEBFF, fundo: 0x091226, chao: 0x14254A,
    tampo: 0x9CC6FF, ladoX: 0x4470C0, ladoY: 0x1F3A72, aresta: 0xA5C0EC, fraca: 0x2EE6A0, forte: 0x8CFFD2, circ: 0x323D55 };
  B.ceu(false);
  const SOMBRA = !window.SEM_SOMBRA;
  // saída linear, sem tone mapping (padrão do r128); sem mapa de ambiente: só as quatro luzes
  B.scene.environment = null;
  B.renderer.shadowMap.enabled = SOMBRA; B.renderer.shadowMap.type = T3.PCFSoftShadowMap;
  const chave = B.luz.chave; chave.color.set(0xFFFFFF); chave.intensity = 0.95; chave.position.set(-5, -3, 8); chave.castShadow = SOMBRA;
  chave.shadow.mapSize.set(2048, 2048); chave.shadow.radius = 6; chave.shadow.bias = -0.0008;
  Object.assign(chave.shadow.camera, { left: -5, right: 5, top: 5, bottom: -5, near: 1, far: 30 }); chave.shadow.camera.updateProjectionMatrix();
  B.luz.amb.intensity = 0;
  B.luz.rim.color.set(0x9CC8FF); B.luz.rim.intensity = 0.45; B.luz.rim.position.set(4, 6, 2);                 // contraluz
  const hemi = new T3.HemisphereLight(0xBFD6FF, 0x0A1326, 0.45); hemi.position.set(0, 0, 1);
  const preen = new T3.DirectionalLight(0xAFC8FF, 0.55); preen.position.set(6, -9, -1);                          // de baixo-frente: a parede de fora não fica preta
  B.scene.add(hemi, preen);
  // profundidade: neblina linear relativa à distância da câmera (a câmera fica longe, fov 16°)
  B.scene.fog = new T3.Fog(COR.fundo, 10, 20);
  const ganchos = [];
  window.aposCamera = D => { B.scene.fog.near = D - 1.0; B.scene.fog.far = D + 10.0; ganchos.forEach(g => g(D)); };

  const cor = c => new T3.Color(c);
  const basic = c => new T3.MeshBasicMaterial({ color: c });
  // borda de luz (fresnel): recorta a silhueta
  function comBorda(m, c, forca) {
    m.onBeforeCompile = sh => {
      sh.uniforms.rimC = { value: new T3.Color(c) }; sh.uniforms.rimK = { value: forca };
      sh.fragmentShader = 'uniform vec3 rimC; uniform float rimK;\n' + sh.fragmentShader.replace('#include <dithering_fragment>',
        '#include <dithering_fragment>\n float fr = 1.0 - abs(dot(normalize(vViewPosition), normalize(vNormal)));\n gl_FragColor.rgb += rimC * pow(fr, 2.6) * rimK;');
    };
    return m;
  }
  const std = (c, lado) => new T3.MeshStandardMaterial({ color: c, metalness: 0.0, roughness: 0.55, side: lado, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
  // superfície opaca de dois lados: `frenteDentro` diz qual face da geometria é o lado de dentro
  function solido(geo, frenteDentro) {
    const g = new T3.Group();
    const mi = new T3.Mesh(geo, comBorda(std(COR.dentro, frenteDentro ? T3.FrontSide : T3.BackSide), '#7FB2FF', 0.25));
    const mo = new T3.Mesh(geo, comBorda(std(COR.fora, frenteDentro ? T3.BackSide : T3.FrontSide), '#BFD8FF', 0.55));
    mi.castShadow = mo.castShadow = true; mi.receiveShadow = true;
    g.add(mi, mo); return g;
  }
  const tubo = (pts, r, mat) => new T3.Mesh(new T3.TubeGeometry(new T3.CatmullRomCurve3(pts.map(p => new T3.Vector3(...p))), Math.max(8, pts.length * 2), r, 8, false), mat);
  const circulo = (r, z, n) => { const p = []; for (let i = 0; i <= n; i++) { const a = 2 * PI * i / n; p.push([r * Math.cos(a), r * Math.sin(a), z]); } return p; };
  const geoHaste = new T3.CylinderGeometry(1, 1, 1, 14), geoCone = new T3.ConeGeometry(1, 1, 24);
  const Y = new T3.Vector3(0, 1, 0), RH = 0.03;
  // seta com corpo (v3): pé em a, vetor v; haste de raio rh (mundo), cone min(0,24; 0,42 L) com raio max(2,8 rh; 0,40 × cone)
  function seta3d(a, v, mat, rh) {
    rh = rh || RH;
    const L = Math.hypot(...v), cone = Math.min(0.24, 0.42 * L), rc = Math.max(2.8 * rh, 0.40 * cone), g = new T3.Group();
    const h = new T3.Mesh(geoHaste, mat), c = new T3.Mesh(geoCone, mat);
    h.scale.set(rh, L - cone, rh); h.position.y = (L - cone) / 2; c.scale.set(rc, cone, rc); c.position.y = L - cone / 2;
    g.add(h, c); g.position.set(...a); g.quaternion.setFromUnitVectors(Y, new T3.Vector3(...v).normalize()); return g;
  }
  // seta de campo: cor pela intensidade f = ‖F‖/‖F‖máx, emissivo 0,35 e borda de luz
  const matSeta = f => { const c = cor(COR.fraca).lerp(cor(COR.forte), f);
    return comBorda(new T3.MeshStandardMaterial({ color: c, metalness: 0.0, roughness: 0.4, emissive: c.clone(), emissiveIntensity: 0.25 }), '#D2FFEF', 0.45); };
  // chão: recebe a sombra (ShadowMaterial) e mostra o domínio projetado como chapa a 35% (as duas transparências declaradas da §2.3.6)
  function chao(z) {
    const m = new T3.ShadowMaterial({ opacity: 0.5 }); m.fog = false; m.userData.excecao = 'sombra do chão (ShadowMaterial 0,5)';
    const p = new T3.Mesh(new T3.PlaneGeometry(16, 16), m); p.position.z = z; p.receiveShadow = true; B.scene.add(p); return p;
  }
  function chapaChao(geo, z) {
    const m = new T3.MeshBasicMaterial({ color: COR.chao, transparent: true, opacity: 0.35, depthWrite: false }); m.userData.excecao = 'chapa do domínio no chão (0,35)';
    const p = new T3.Mesh(geo, m); p.position.z = z; B.scene.add(p); return p;
  }
  // caixa/coluna em três tons fixos (não dependem da luz): tampo, lado ±x, lado ±y
  const tresTons = () => [basic(COR.ladoX), basic(COR.ladoX), basic(COR.ladoY), basic(COR.ladoY), basic(COR.tampo), basic(COR.ladoY)];
  // arestas claras como cilindros finos instanciados: lista de [a, b]
  function arestas(lista, r) {
    const im = new T3.InstancedMesh(geoHaste, basic(COR.aresta), lista.length), m = new T3.Matrix4(), q = new T3.Quaternion();
    lista.forEach(([a, b], k) => {
      const va = new T3.Vector3(...a), d = new T3.Vector3(...b).sub(va), L = d.length();
      q.setFromUnitVectors(Y, d.normalize()); m.compose(va.addScaledVector(d, L / 2), q, new T3.Vector3(r, L, r)); im.setMatrixAt(k, m);
    });
    return im;
  }
  const arestasCaixa = (x0, x1, y0, y1, z1, comBase) => {
    const c = [[x0, y0], [x1, y0], [x1, y1], [x0, y1]], l = [];
    for (let k = 0; k < 4; k++) { const [a, b] = [c[k], c[(k + 1) % 4]]; l.push([[...a, z1], [...b, z1]], [[...a, 0], [...a, z1]]); if (comBase) l.push([[...a, 0], [...b, 0]]); }
    return l;
  };

  const suave2 = u => u * u * (3 - 2 * u);
  let atualiza = () => {}, pontos = () => ({});

  if (id === 'colunas') {
    const f = (x, y) => 1.5 + 0.5 * Math.sin(1.5 * x) * Math.cos(1.2 * y);
    const raiz = new T3.Group(); B.scene.add(raiz);
    chao(-0.02);
    chapaChao(new T3.PlaneGeometry(3.7, 2.7), -0.01).position.set(1.5, 1, -0.01);
    { const c = [[0, 0, 0], [3, 0, 0], [3, 2, 0], [0, 2, 0]], mg = basic(COR.geo); c.forEach((p, i) => raiz.add(tubo([p, c[(i + 1) % 4]], 0.012, mg))); }
    // superfície por cima, em linhas claras (tubos): x e y de 0,5 em 0,5
    const fios = new T3.Group(), matL = basic(COR.linha);
    for (let k = 0; k <= 6; k++) { const x = 0.5 * k, p = []; for (let i = 0; i <= 40; i++) { const y = 2 * i / 40; p.push([x, y, f(x, y) + 0.004]); } fios.add(tubo(p, 0.008, matL)); }
    for (let k = 0; k <= 4; k++) { const y = 0.5 * k, p = []; for (let i = 0; i <= 60; i++) { const x = 3 * i / 60; p.push([x, y, f(x, y) + 0.004]); } fios.add(tubo(p, 0.008, matL)); }
    raiz.add(fios);
    // colunas em três tons, vão de 12%, arestas claras
    const box = new T3.BoxGeometry(1, 1, 1); box.translate(0, 0, 0.5);
    const mats = tresTons();
    const niveis = [[6, 4], [12, 8], [24, 16], [96, 64]].map(([nx, ny], nv) => {
      const g = new T3.Group(), im = new T3.InstancedMesh(box, mats, nx * ny), m = new T3.Matrix4(), dx = 3 / nx, dy = 2 / ny, w = nv < 3 ? 0.88 : 1.0, ar = [];
      let k = 0;
      for (let i = 0; i < nx; i++) for (let j = 0; j < ny; j++) {
        const cx = (i + 0.5) * dx, cy = (j + 0.5) * dy, h = f(cx, cy);
        m.makeScale(dx * w, dy * w, h); m.setPosition(cx, cy, 0); im.setMatrixAt(k++, m);
        if (nv < 3) ar.push(...arestasCaixa(cx - dx * w / 2, cx + dx * w / 2, cy - dy * w / 2, cy + dy * w / 2, h, false));
      }
      im.castShadow = true; g.add(im);
      if (ar.length) g.add(arestas(ar, [0.007, 0.0055, 0.004][nv]));
      g.visible = false; raiz.add(g); return g;
    });
    // superfície sólida (nível 4): tampo com luz e borda de luz; paredes nos tons das colunas
    const sol = new T3.Group();
    const gS = new T3.PlaneGeometry(3, 2, 90, 60), pS = gS.attributes.position;
    for (let i = 0; i < pS.count; i++) { const x = pS.getX(i) + 1.5, y = pS.getY(i) + 1; pS.setXYZ(i, x, y, f(x, y)); }
    gS.computeVertexNormals();
    const topo = new T3.Mesh(gS, comBorda(std(COR.fora, T3.FrontSide), '#BFD8FF', 0.55)); topo.castShadow = true; sol.add(topo);
    const parede = (p0, p1, mat) => {
      const N = 60, pos = [], idx = [];
      for (let i = 0; i <= N; i++) { const x = p0[0] + (p1[0] - p0[0]) * i / N, y = p0[1] + (p1[1] - p0[1]) * i / N; pos.push(x, y, 0, x, y, f(x, y)); }
      for (let i = 0; i < N; i++) idx.push(2 * i, 2 * i + 2, 2 * i + 1, 2 * i + 1, 2 * i + 2, 2 * i + 3);
      const g = new T3.BufferGeometry(); g.setAttribute('position', new T3.Float32BufferAttribute(pos, 3)); g.setIndex(idx);
      mat.side = T3.DoubleSide; return new T3.Mesh(g, mat);
    };
    sol.add(parede([0, 0], [3, 0], basic(COR.ladoY)), parede([3, 0], [3, 2], basic(COR.ladoX)), parede([3, 2], [0, 2], basic(COR.ladoY)), parede([0, 2], [0, 0], basic(COR.ladoX)));
    sol.add(arestas([[[0, 0, 0], [0, 0, f(0, 0)]], [[3, 0, 0], [3, 0, f(3, 0)]], [[3, 2, 0], [3, 2, f(3, 2)]], [[0, 2, 0], [0, 2, f(0, 2)]]], 0.007));
    sol.visible = false; raiz.add(sol);
    atualiza = e => { const nv = e.nivel || 0; niveis.forEach((g, k) => { g.visible = nv === k; }); sol.visible = nv === 4; };
    pontos = () => ({ o: B.projeta([0, 0, 0]), c: B.projeta([3, 2, 0]) });
  }

  if (id === 'caixa') {
    const HX = 1.1, HY = 0.8, HZ = 0.7, N = 30, NS = 16, S = 2.4, L = 0.45, V = 0.7, LIFT = 0.35, raiz = new T3.Group(); B.scene.add(raiz);
    raiz.position.z = LIFT;                      // v5: a caixa fica 0,35 acima do chão (a sombra continua); as setas saem pelas seis faces
    chao(-0.02);
    chapaChao(new T3.PlaneGeometry(2 * HX + 0.9, 2 * HY + 0.9), -0.01);
    const cx = new T3.Mesh(new T3.BoxGeometry(2 * HX, 2 * HY, 2 * HZ), tresTons()); cx.position.z = HZ; cx.castShadow = true; raiz.add(cx);
    raiz.add(arestas(arestasCaixa(-HX, HX, -HY, HY, 2 * HZ, true), 0.011));
    const GA = PI * (3 - Math.sqrt(5)), mat = matSeta(1.0), frac = x => x - Math.floor(x);
    const st = [];
    for (let i = 0; i < NS; i++) {
      const z = 1 - (2 * i + 1) / N, rr = Math.sqrt(1 - z * z), ph = i * GA, d = [rr * Math.cos(ph), rr * Math.sin(ph), z];
      const wl = Math.min(HX / Math.abs(d[0] || 1e-9), HY / Math.abs(d[1] || 1e-9), HZ / Math.abs(d[2] || 1e-9));       // distância do centro até a parede
      const g = seta3d([0, 0, 0], d.map(c => L * c), mat); raiz.add(g); st.push({ g, d, wl, fase: frac(0.618034 * i) * S });
    }
    atualiza = e => {
      const t = e.t || 0;
      for (const s of st) {
        const u = (s.fase + V * t) % S, rho = s.wl - L + u, k = Math.min(1, (S - u) / 0.5);       // u = 0: a ponta está na parede; encolhe no fim do voo
        s.g.position.set(s.d[0] * rho, s.d[1] * rho, HZ + s.d[2] * rho); s.g.scale.setScalar(Math.max(0.001, k));
      }
    };
    pontos = () => ({ cx: B.projeta([0, 0, HZ + LIFT]) });
  }

  if (id === 'folha_paraboloide') {
    const R = 2, raiz = new T3.Group(); B.scene.add(raiz);
    chao(-0.03);
    chapaChao(new T3.CircleGeometry(R, 96), -0.02);
    raiz.add(tubo(circulo(R, -0.02, 120), 0.012, basic(COR.geo)));
    const matEixo = basic(0x8A93A8);                                     // GEO a 75% sobre o fundo
    raiz.add(seta3d([0, 0, -0.015], [3.0, 0, 0], matEixo, 0.012), seta3d([0, 0, -0.015], [0, 3.0, 0], matEixo, 0.012), seta3d([0, 0, 0], [0, 0, 4.7], matEixo, 0.012));
    const gF = new T3.RingGeometry(0.0001, R, 96, 40), pF = gF.attributes.position, base = Float32Array.from(pF.array);
    raiz.add(solido(gF, true));                                           // face da frente (normal +z) = lado de dentro da tigela
    const matU = basic(COR.e1), matV = basic(COR.e2), matC = basic(COR.linha);
    let ls = [];
    function monta(s) {
      ls.forEach(m => { raiz.remove(m); m.geometry.dispose(); }); ls = [];
      const z = (x, y) => s * (x * x + y * y);
      for (let k = -3; k <= 3; k++) {
        const c = 0.5 * k, h = Math.sqrt(R * R - c * c), N = 48, pu = [], pv = [];
        for (let i = 0; i <= N; i++) { const w = -h + 2 * h * i / N; pu.push([c, w, z(c, w)]); pv.push([w, c, z(w, c)]); }
        ls.push(tubo(pu, 0.017, matU), tubo(pv, 0.017, matV));
      }
      for (const r of [1, 2]) ls.push(tubo(circulo(r, s * r * r, 120), 0.022, matC));
      ls.forEach(m => raiz.add(m));
      for (let i = 0; i < pF.count; i++) { const x = base[3 * i], y = base[3 * i + 1]; pF.setZ(i, s * (x * x + y * y)); }
      pF.needsUpdate = true; gF.computeVertexNormals();
    }
    let sAtual = -1;
    atualiza = e => { const s = e.s || 0; if (Math.abs(s - sAtual) > 1e-5) { monta(s); sAtual = s; } };
    pontos = e => { const s = e.s || 0; return { o: B.projeta([0, 0, 0]), a1: B.projeta([1, 0, s]), a4: B.projeta([2, 0, 4 * s]) }; };
  }

  if (id === 'campo_espaco') {
    const raiz = new T3.Group(); B.scene.add(raiz);
    let semente = 2611; const rnd = () => { semente = (semente * 16807) % 2147483647; return semente / 2147483647; };
    const GA = PI * (3 - Math.sqrt(5)), CASCAS = [[1.25, 14], [1.75, 22], [2.25, 30]], K1 = 1.1, LMAX = K1 / (1.25 * 1.25);
    const matC = basic(COR.circ), mats = [], bases = [], flechas = [], aneis = [];
    let n = 0, perto = 9; const comp = [];
    CASCAS.forEach(([r, N], k) => {
      const q = new T3.Quaternion().setFromAxisAngle(new T3.Vector3(rnd() - 0.5, rnd() - 0.5, rnd() - 0.5).normalize(), 2 * PI * rnd());
      const L = K1 / (r * r); mats.push([]); bases.push(cor(COR.fraca).lerp(cor(COR.forte), L / LMAX)); comp.push(L.toFixed(3));
      for (let i = 0; i < N; i++) {
        const yy = 1 - 2 * (i + 0.5) / N, rr = Math.sqrt(1 - yy * yy), ph = i * GA;
        const d = new T3.Vector3(rr * Math.cos(ph), yy, rr * Math.sin(ph)).applyQuaternion(q);
        const m = matSeta(L / LMAX); m.transparent = true; m.userData.excecao = 'opacidade por quadro das setas alinhadas com a visada (B7)';
        const g = seta3d([r * d.x, r * d.y, r * d.z], [-L * d.x, -L * d.y, -L * d.z], m); raiz.add(g);
        flechas.push({ g, m, d, p: new T3.Vector3(r * d.x, r * d.y, r * d.z) }); mats[k].push(m);
        n++; perto = Math.min(perto, r - L);
      }
      // referência de profundidade: UM anel por casca, sempre de frente para a câmera (GEO a 22% sobre o fundo, opaco)
      const an = new T3.Mesh(new T3.TorusGeometry(r, 0.006, 8, 120), matC); raiz.add(an); aneis.push(an);
    });
    // por quadro: a opacidade de cada seta cai a 0 quando o ângulo com a linha de visada (câmera → pé da seta) fica abaixo de 30° (rampa 35° → 25°)
    window.fadeVisada = [];
    ganchos.push(() => {
      aneis.forEach(a => a.quaternion.copy(B.camera.quaternion));
      let f0 = 0, fa = 0;
      flechas.forEach(f => {
        const v = B.camera.position.clone().sub(f.p).normalize(), ang = Math.acos(Math.min(1, Math.abs(v.dot(f.d)))) * 180 / PI;
        const u = Math.min(1, Math.max(0, (ang - 25) / 10)); f.m.opacity = u * u * (3 - 2 * u); f.g.visible = f.m.opacity > 0.01; if (f.m.opacity < 0.5) f0++; else fa++;
      });
      window.fadeVisada = [fa, f0];
    });
    console.log(`campo_espaco: ${n} setas em 3 cascas, comprimentos ${comp.join(' / ')} (1,1/r²), sem descarte fixo; ponta mais próxima da origem a ${perto.toFixed(2)}`);
    const anel = new T3.Mesh(new T3.TorusGeometry(0.11, 0.018, 10, 48), basic(COR.geo)); raiz.add(anel);
    ganchos.push(() => { anel.quaternion.copy(B.camera.quaternion); });
    const cF = cor(COR.fundo);
    atualiza = e => {
      const dim = 0.6 * (1 - (e.longe == null ? 1 : e.longe)) / 0.65;            // B7-2: as cascas de fora escurecem (sem transparência)
      [1, 2].forEach(k => mats[k].forEach(m => { m.color.copy(bases[k]).lerp(cF, dim); m.emissive.copy(m.color); }));
      anel.scale.setScalar(1 + 0.7 * (e.pulso || 0));
    };
    pontos = () => ({ o: B.projeta([0, 0, 0]), p1: B.projeta([1, 0, 0]) });
  }

  if (id === 'tigela') {
    // T3 (abertura v5.1): tigela aberta z = x² + y² (R = 1,4) em retalhos (3 anéis × 12 setores); uma chuva de setas ciano (campo constante −z)
    // desce e atravessa; cada retalho acende quando a ponta cruza o seu centro. Os tempos de cruzamento são os que o Manim usa no contador.
    const R = 1.4, NA = 3, NS = 12, ZT = 3.4, VQ = 1.05, LS = 0.45, raiz = new T3.Group(); B.scene.add(raiz);
    chao(-0.03);
    chapaChao(new T3.CircleGeometry(R + 0.35, 96), -0.02);
    const patches = [], claro = cor(COR.forte), base = cor(COR.dentro);
    for (let i = 0; i < NA; i++) for (let j = 0; j < NS; j++) {
      const r0 = R * i / NA, r1 = R * (i + 1) / NA, a0 = 2 * PI * j / NS, da = 2 * PI / NS;
      const g = new T3.RingGeometry(Math.max(r0, 1e-4), r1, 6, 3, a0, da), p = g.attributes.position;
      for (let k = 0; k < p.count; k++) { const x = p.getX(k), y = p.getY(k); p.setZ(k, x * x + y * y); }
      g.computeVertexNormals();
      const mi = comBorda(std(COR.dentro, T3.FrontSide), '#7FB2FF', 0.25), mo = comBorda(std(COR.fora, T3.BackSide), '#BFD8FF', 0.55);
      const A = new T3.Mesh(g, mi), Bm = new T3.Mesh(g, mo); A.castShadow = Bm.castShadow = true; A.receiveShadow = true; raiz.add(A, Bm);
      const rc = (r0 + r1) / 2; patches.push({ mi, tc: (ZT - rc * rc) / VQ });
    }
    const matL = basic(COR.linha);
    for (let i = 1; i <= NA; i++) raiz.add(tubo(circulo(R * i / NA, (R * i / NA) ** 2 + 0.004, 96), 0.008, matL));
    for (let j = 0; j < NS; j++) { const a = 2 * PI * j / NS, p = []; for (let k = 0; k <= 12; k++) { const r = R * k / 12; p.push([r * Math.cos(a), r * Math.sin(a), r * r + 0.004]); } raiz.add(tubo(p, 0.008, matL)); }
    const mat = matSeta(1.0), fl = [];
    for (let x = -R; x <= R + 1e-6; x += 0.3) for (let y = -R; y <= R + 1e-6; y += 0.3) {
      if (Math.hypot(x, y) > R - 0.08) continue;
      const g = seta3d([x, y, ZT + LS], [0, 0, -LS], mat); raiz.add(g); fl.push({ g, x, y });
    }
    atualiza = e => {
      const t = e.t || 0, zt = ZT - VQ * t;
      fl.forEach(f => { f.g.position.set(f.x, f.y, zt + LS); f.g.visible = zt > f.x * f.x + f.y * f.y - 0.3; });      // some depois de atravessar
      patches.forEach(p => {
        const u = Math.min(1, Math.max(0, (t - p.tc) / 0.3)), lv = u * (1 - 0.35 * Math.min(1, Math.max(0, (t - p.tc - 0.3) / 0.6)));
        p.mi.color.copy(base).lerp(claro, 0.85 * lv); p.mi.emissive.copy(claro).multiplyScalar(0.5 * lv);
      });
    };
    pontos = () => ({ o: B.projeta([0, 0, 0]) });
    console.log(`tigela: ${patches.length} retalhos, ${fl.length} setas, cruzamentos de ${patches[NS * (NA - 1)].tc.toFixed(2)} s (borda) a ${patches[0].tc.toFixed(2)} s (centro)`);
  }

  // ── v6: Stokes (calota em células) e Gauss (cubinhos) — o cancelamento entre vizinhos, com tudo em movimento ─────────────────────────────
  const matMenta = basic(COR.forte), matMentaF = basic(COR.fraca), matBranco = basic(0xE8F0FF);
  const esfera = new T3.SphereGeometry(1, 10, 8);
  const ponto3 = (r, mat) => { const m = new T3.Mesh(esfera, mat); m.scale.setScalar(r); return m; };

  if (id === 'calota') {
    // calota z = sqrt(R² − r²) até r = RB, 2 anéis × 8 setores. Arestas internas (24) cancelam em pares (cada uma tem dois pontos correndo em sentidos
    // opostos); sobra a circunferência da borda (8 arcos) com os pontos correndo mais claros. Rotores (toros) giram em cada célula até o fim.
    const R = 1.5, RB = 1.15, NA = 2, NS = 8, raiz = new T3.Group(); B.scene.add(raiz);
    chao(-0.03); chapaChao(new T3.CircleGeometry(RB + 0.4, 96), -0.02);
    const zc = (x, y) => Math.sqrt(R * R - x * x - y * y) - Math.sqrt(R * R - RB * RB);
    const P = (r, a) => [r * Math.cos(a), r * Math.sin(a), zc(r * Math.cos(a), r * Math.sin(a)) + 0.012];
    const gT = new T3.RingGeometry(0.0001, RB, 96, 24), pT = gT.attributes.position;
    for (let i = 0; i < pT.count; i++) { const x = pT.getX(i), y = pT.getY(i); pT.setZ(i, zc(x, y)); }
    gT.computeVertexNormals(); raiz.add(solido(gT, true));
    const arestas3 = [], rot = [];
    const arco = (r, a0, a1) => { const p = []; for (let k = 0; k <= 10; k++) p.push(P(r, a0 + (a1 - a0) * k / 10)); return p; };
    const reta = (a, r0, r1) => { const p = []; for (let k = 0; k <= 8; k++) p.push(P(r0 + (r1 - r0) * k / 8, a)); return p; };
    const da = 2 * PI / NS; let n = 0;
    for (let j = 0; j < NS; j++) {
      const a = j * da;
      [[0, RB / 2], [RB / 2, RB]].forEach(([r0, r1]) => arestas3.push({ p: reta(a, r0, r1), int: true, tc: 0.2 + 0.04 * (n++) }));
      arestas3.push({ p: arco(RB / 2, a, a + da), int: true, tc: 0.2 + 0.04 * (n++) });
      arestas3.push({ p: arco(RB, a, a + da), int: false, tc: 1e9 });
      const rc = 0.75 * RB, ac = a + da / 2, x = rc * Math.cos(ac), y = rc * Math.sin(ac);
      const t = new T3.Mesh(new T3.TorusGeometry(0.1, 0.014, 6, 24, 4.6), matMenta); t.position.set(x, y, zc(x, y) + 0.03); raiz.add(t); rot.push(t);
      const rc2 = 0.3 * RB, x2 = rc2 * Math.cos(ac), y2 = rc2 * Math.sin(ac);
      const t2 = new T3.Mesh(new T3.TorusGeometry(0.08, 0.014, 6, 24, 4.6), matMenta); t2.position.set(x2, y2, zc(x2, y2) + 0.03); raiz.add(t2); rot.push(t2);
    }
    const tTot = 0.2 + 0.04 * n + 0.3;
    arestas3.forEach((e, i) => {
      e.fios = tubo(e.p, 0.011, e.int ? matMentaF : matMenta); raiz.add(e.fios);
      e.d1 = ponto3(0.03, matBranco); e.d2 = ponto3(0.03, matBranco); raiz.add(e.d1, e.d2); e.ph = (i * 0.37) % 1;
    });
    const em = (p, u) => { const L = p.length - 1, x = Math.min(L - 1e-6, u * L), k = Math.floor(x), f = x - k; return p[k].map((v, c) => v + (p[k + 1][c] - v) * f); };
    atualiza = e => {
      const t = e.t || 0;
      arestas3.forEach(a => {
        const viva = t < a.tc, flash = a.int && t >= a.tc - 0.12 && t < a.tc + 0.12, u1 = (t * 0.45 + a.ph) % 1;
        a.fios.visible = viva; a.fios.scale.set(flash ? 1.8 : 1, flash ? 1.8 : 1, flash ? 1.8 : 1);
        const mostra = viva || !a.int;
        a.d1.visible = mostra; a.d1.position.set(...em(a.p, u1));
        a.d2.visible = a.int ? viva : false; if (a.int) a.d2.position.set(...em(a.p, 1 - u1));
        const todos = t > tTot; a.d1.scale.setScalar(a.int ? 0.03 : (todos ? 0.05 : 0.03));
      });
      rot.forEach((r, i) => { r.rotation.z = 2.2 * t + i; r.visible = t < tTot; });
    };
    pontos = () => ({ o: B.projeta([0, 0, 0]) });
  }

  if (id === 'gauss') {
    // 2×2×2 cubinhos de lado 0,55 levemente afastados (gap g); em cada face comum, duas setas opostas que se cancelam e somem (aos pares);
    // os cubinhos se juntam e só as setas das faces de fora continuam saindo (e correndo).
    const H = 0.275, raiz = new T3.Group(); B.scene.add(raiz); raiz.position.z = 0.35;
    chao(-0.02); chapaChao(new T3.PlaneGeometry(2.0, 2.0), -0.01);
    const cubos = [], faces = [];
    for (let i = 0; i < 2; i++) for (let j = 0; j < 2; j++) for (let k = 0; k < 2; k++) {
      const c = new T3.Mesh(new T3.BoxGeometry(2 * H, 2 * H, 2 * H), tresTons()); c.castShadow = true; raiz.add(c);
      const ar = new T3.Group(); ar.add(arestas(arestasCaixa(-H, H, -H, H, 2 * H, true).map(([a, b]) => [[a[0], a[1], a[2] - H], [b[0], b[1], b[2] - H]]), 0.007)); c.add(ar);
      cubos.push({ c, i, j, k });
    }
    const dirs = [[1, 0, 0], [0, 1, 0], [0, 0, 1]], mat = matSeta(1.0); let nf = 0; const so = [];
    cubos.forEach(({ i, j, k }, idx) => {
      [[0, i, [1, 0, 0]], [1, j, [0, 1, 0]], [2, k, [0, 0, 1]]].forEach(([ax, v, d]) => {
        const sg = v === 0 ? -1 : 1, interna = true;
        // face de dentro: seta que sai do cubo na direção do vizinho (par com a do vizinho)
        const g = seta3d([0, 0, 0], d.map(c => 0.28 * c * -sg), mat); raiz.add(g); faces.push({ g, idx, d: d.map(c => c * -sg), int: true, tc: 0.2 + 0.08 * (ax * 4 + [i, j, k].filter((_, q) => q !== ax).reduce((s, v2) => s * 2 + v2, 0)) });
        // face de fora
        const g2 = seta3d([0, 0, 0], d.map(c => 0.28 * c * sg), mat); raiz.add(g2); faces.push({ g: g2, idx, d: d.map(c => c * sg), int: false, tc: 1e9, ph: (nf * 0.173) % 1 }); nf++;
      });
    });
    const tF = 0.2 + 0.08 * 12 + 0.3;
    atualiza = e => {
      const t = e.t || 0, gap = 0.16 * (1 - suave2(Math.min(1, Math.max(0, (t - tF) / 0.5))));
      cubos.forEach(({ c, i, j, k }) => c.position.set((i - 0.5) * (2 * H + gap), (j - 0.5) * (2 * H + gap), (k - 0.5) * (2 * H + gap) + H + 0.55 * 0));
      faces.forEach(f => {
        const cb = cubos[f.idx], p = cb.c.position, v = f.d;
        let off = H, s = 1;
        if (f.int) { s = t < f.tc ? 1 : 0; off = H + 0.5 * gap * 0 + 0.02; } else { off = H + 0.02 + 0.28 * ((t * 0.5 + f.ph) % 1) * 0.6; s = 1; }
        f.g.position.set(p.x + v[0] * off, p.y + v[1] * off, p.z + v[2] * off);
        f.g.scale.setScalar(Math.max(0.001, s)); f.g.visible = s > 0.01;
      });
    };
    pontos = () => ({ cx: B.projeta([0, 0, 0.35 + 0.275]) });
  }

  // QA de estilo: materiais com opacidade < 0,75 (alvo 0, fora as exceções declaradas)
  let nT = 0; const exc = new Set();
  B.scene.traverse(o => { for (const m of [].concat(o.material || [])) if (m.transparent && m.opacity < 0.75) { if (m.userData.excecao) exc.add(m.userData.excecao); else nT++; } });
  console.log(`[estilo3d] ${id}: ${nT} materiais com opacidade < 0,75; exceções declaradas: ${[...exc].join('; ') || 'nenhuma'}; sombra ${SOMBRA ? 'ligada' : 'desligada'}`);

  window.CENA = { atualiza };
  window.pontos3d = e => pontos(e);
  window.cenaPronta = true;
})();
