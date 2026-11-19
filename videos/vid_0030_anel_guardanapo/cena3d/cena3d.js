// vid_0030 — Anel de guardanapo (Three.js r128). Geometria 3D do pipeline Three.js + Manim (+ Remotion experimental).
// Regra de ouro: tudo é função do quadro. window.setFrame(f) desenha o quadro f a partir de t = f/FPS, sem relógio.
// window.TIMELINE (timeline.json) e window.FPS são injetados pelo render3d.js / ancoras.js antes da página carregar.
// Mundo: 1 unidade = 1 cm, eixo do anel = z (as geometrias do Three, que nascem em torno de y, são giradas para z).
//
// Exporta, além de setFrame:
//  - window.projeta(p): ponto 3D → pixel (QA e âncoras);
//  - window.ancoras(): pontos 3D nomeados do quadro atual (o ancoras.js projeta e salva em ancoras.json, que o Manim
//    e o Remotion leem para pôr rótulos em cima do 3D);
//  - window.valores(): números do quadro atual (z do plano, raios, áreas, R e a do anel), mesmos para as três camadas.
(function () {
  const TL = window.TIMELINE, FPS = window.FPS || 15, G = TL.geometria, CH = TL.chaves;
  // Paleta Parallax Lab: h = ciano (protagonista), R = magenta (some da conta), a = violeta (furo), z/eixos = GEO.
  // v2: o anel é azul em todas as cenas (o trio só varia a luminosidade); esferas de comparação em magenta (esfera de
  // Cavalieri e seu disco; esfera original fantasma); material removido pelo furo em violeta (cor de a); aço só em
  // estrutura neutra. (Kaio, 27/10: nada de âmbar/amarelo.)
  const COR = { geo: 0xB8C4DA, aco: 0x7A8696, fundo: 0x050816, secao: 0x23459A, h: 0xEA63FF,   // v4.2: h magenta
    R: 0xEA63FF, a: 0x9C8CFF,
    anel: 0x3D7BFF, esf: 0xEA63FF, esfClaro: 0xF7B8FF, azulClaro: 0x9CC8FF, trio: [0x5C93FF, 0x3D7BFF, 0x2C68EA] };
  const W = innerWidth, H = innerHeight, PI = Math.PI, V3 = (x, y, z) => new THREE.Vector3(x, y, z);

  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H); renderer.setClearColor(COR.fundo, 1); renderer.autoClear = false;
  renderer.localClippingEnabled = true;
  document.body.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new THREE.RoomEnvironment(), 0.04).texture;
  const chave = new THREE.DirectionalLight(0xffffff, 1.3), contra = new THREE.DirectionalLight(0xffffff, 0.35);
  scene.add(chave, chave.target, contra, contra.target, new THREE.AmbientLight(0xffffff, 0.22));

  // ---------- funções de tempo (as MESMAS no cena.py e no Remotion) ----------
  const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
  const suave = u => u * u * (3 - 2 * u);
  function chaves(lista, t, campo = 'v') {
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
  const K = (nome, t) => chaves(CH[nome], t);

  // ---------- materiais ----------
  // acetinado (pouco metal, rugoso): azul saturado sem brilho especular estourado
  const aco = (extra = {}) => new THREE.MeshStandardMaterial(Object.assign(
    { color: COR.anel, metalness: 0.12, roughness: 0.55, envMapIntensity: 0.3, side: THREE.DoubleSide }, extra));
  const basico = (cor, extra = {}) => new THREE.MeshBasicMaterial(Object.assign(
    { color: cor, transparent: true, depthWrite: false, side: THREE.DoubleSide }, extra));
  const tracos = [];                                     // materiais de aço (escurecem com realce_3d)
  // v4 · estilo do sólido (§5.2), escolhido em 3 quadros de teste: 'A' = v3 (azul chapado); 'B' = gradiente vertical
  // #2E5BD8 → #1B3FA6 + rim light #8EC5FF + parede do furo mais escura; 'C' = B + meridianos e paralelos finos.
  const ESTILO = window.ESTILO || 'C', NOVO = ESTILO !== 'A';
  const GRAD = { topo: new THREE.Color(0x2E5BD8), base: new THREE.Color(0x1B3FA6),
    topoIn: new THREE.Color(0x1F3F9E), baseIn: new THREE.Color(0x10276A) };
  function pinta(geo, h, interno = false) {             // cor por vértice: gradiente vertical (z) do sólido
    if (!NOVO) return geo;
    const p = geo.attributes.position, c = new Float32Array(p.count * 3), col = new THREE.Color();
    for (let i = 0; i < p.count; i++) {
      const u = clamp((p.getZ(i) + h / 2) / h, 0, 1);
      col.copy(interno ? GRAD.baseIn : GRAD.base).lerp(interno ? GRAD.topoIn : GRAD.topo, u).toArray(c, 3 * i);
    }
    geo.setAttribute('color', new THREE.BufferAttribute(c, 3));
    return geo;
  }
  // material do sólido: no estilo novo é branco × cor do vértice, acetinado, reflexo suave sem estourar
  const solido = (extra = {}) => NOVO
    ? new THREE.MeshStandardMaterial(Object.assign({ color: 0xffffff, vertexColors: true, metalness: 0.18, roughness: 0.42,
        envMapIntensity: 0.45, side: THREE.DoubleSide }, extra))
    : aco(extra);
  // rim light (fresnel aditivo) na mesma geometria do sólido
  const rims = [];
  function rim(malha, clip) {
    const m = new THREE.ShaderMaterial({
      uniforms: { uA: { value: 0 }, uCor: { value: new THREE.Color(0x8EC5FF) } },
      vertexShader: `varying vec3 vN; varying vec3 vV;
        #include <clipping_planes_pars_vertex>
        void main(){ vec4 w = modelMatrix * vec4(position,1.0); vN = normalize(mat3(modelMatrix) * normal);
          vV = normalize(cameraPosition - w.xyz); vec4 mvPosition = viewMatrix * w; gl_Position = projectionMatrix * mvPosition;
          #include <clipping_planes_vertex>
        }`,
      fragmentShader: `uniform float uA; uniform vec3 uCor; varying vec3 vN; varying vec3 vV;
        #include <clipping_planes_pars_fragment>
        void main(){
          #include <clipping_planes_fragment>
          float f = pow(1.0 - abs(dot(normalize(vN), normalize(vV))), 3.0);
          gl_FragColor = vec4(uCor * f * 0.85 * uA, 1.0); }`,
      transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.FrontSide,
      clipping: true, clippingPlanes: clip || null,
    });
    const r = new THREE.Mesh(malha.geometry, m); r.renderOrder = (malha.renderOrder || 0) + 0.5;
    r.userData.dono = malha; malha.parent ? malha.parent.add(r) : scene.add(r); rims.push(r);
    return r;
  }
  // meridianos (8) e paralelos (3) finos sobre a zona esférica
  function geoMalha(R, h) {
    const p = [], e = 1.004;
    for (let k = 0; k < 8; k++) {
      const f = 2 * PI * k / 8;
      for (let j = 0; j < 24; j++) for (const jj of [j, j + 1]) {
        const z = -h / 2 + h * jj / 24, r = Math.sqrt(Math.max(R * R - z * z, 0)) * e;
        p.push(r * Math.cos(f), r * Math.sin(f), z);
      }
    }
    for (const z of [-h / 4, 0, h / 4]) {
      const r = Math.sqrt(Math.max(R * R - z * z, 0)) * e;
      for (let i = 0; i < 96; i++) for (const ii of [i, i + 1])
        p.push(r * Math.cos(2 * PI * ii / 96), r * Math.sin(2 * PI * ii / 96), z);
    }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(p, 3)); return g;
  }
  const malhas = [];
  function malha(grupo, R, h, clip) {
    const m = new THREE.LineBasicMaterial({ color: 0xDCEBFF, transparent: true, opacity: 0, depthWrite: false,
      clippingPlanes: clip || null });
    const l = new THREE.LineSegments(geoMalha(R, h), m); l.renderOrder = 2.5; l.visible = ESTILO === 'C';
    grupo.add(l); malhas.push(l); return l;
  }
  function opac(m, v, base = 1) {                        // opacidade com troca automática de modo
    const o = v * base;
    m.opacity = o; m.visible = o > 0.003;
    m.transparent = o < 0.999 || m.userData.semprTransp === true;
    m.depthWrite = m.userData.semprTransp ? false : o > 0.6;
  }

  // ---------- geometrias do anel (zona esférica + parede do furo, sem tampas) ----------
  const geoZona = (R, h) => {
    const th = Math.acos(clamp(h / (2 * R), -1, 1));
    return new THREE.SphereGeometry(R, 128, 64, 0, 2 * PI, th, PI - 2 * th).rotateX(PI / 2);
  };
  const geoParede = (a, h) => new THREE.CylinderGeometry(a, a, h, 128, 1, true).rotateX(PI / 2);

  // Anel principal: solido (abaixo do plano de corte) + fantasma (acima), ambos cortáveis pelo plano vertical y = 0.
  const planoY = new THREE.Plane(V3(0, 1, 0), 6);       // corta y < −c (c = corte_v); c = 6 não corta nada
  const planoZs = new THREE.Plane(V3(0, 0, -1), 100);   // mantém z ≤ z0
  const planoZg = new THREE.Plane(V3(0, 0, 1), -100);   // mantém z ≥ z0
  const anel = new THREE.Group(); scene.add(anel);
  const mZonaS = solido({ clippingPlanes: [planoY, planoZs] }), mParS = solido({ clippingPlanes: [planoY, planoZs], side: THREE.BackSide });
  const mZonaG = solido({ clippingPlanes: [planoY, planoZg] }), mParG = solido({ clippingPlanes: [planoY, planoZg], side: THREE.BackSide });
  tracos.push(mZonaS, mParS, mZonaG, mParG);
  if (NOVO) for (const m of [mZonaS, mParS, mZonaG, mParG]) m.userData.base = 0xffffff;
  const zonaS = new THREE.Mesh(pinta(geoZona(G.R, G.h), G.h), mZonaS), parS = new THREE.Mesh(pinta(geoParede(G.a, G.h), G.h, true), mParS);
  const zonaG = new THREE.Mesh(zonaS.geometry, mZonaG), parG = new THREE.Mesh(parS.geometry, mParG);
  zonaG.renderOrder = parG.renderOrder = 2;
  const cat = (c, ...objs) => objs.forEach(o => o.traverse(x => (x.userData.cat = c)));   // categoria do modo máscara
  cat('solido', zonaS, parS, zonaG, parG);
  anel.add(zonaS, parS, zonaG, parG);
  const rimS = rim(zonaS, [planoY, planoZs]), rimG = rim(zonaG, [planoY, planoZg]);
  const malhaAnel = malha(anel, G.R, G.h, [planoY, planoZs]);
  let Ratual = G.R, Hatual = G.h;
  function refazAnel(R, h) {                     // v4: h também muda (C07: o furo fecha / o anel afina)
    if (Math.abs(R - Ratual) < 1e-6 && Math.abs(h - Hatual) < 1e-6) return;
    Ratual = R; Hatual = h;
    const a = Math.sqrt(Math.max(R * R - h * h / 4, 0));
    zonaS.geometry.dispose(); parS.geometry.dispose(); malhaAnel.geometry.dispose();
    zonaS.geometry = zonaG.geometry = rimS.geometry = rimG.geometry = pinta(geoZona(R, h), h);
    parS.geometry = parG.geometry = pinta(geoParede(Math.max(a, 1e-3), h), h, true);
    malhaAnel.geometry = geoMalha(R, h);
  }

  // Tampão removido pelo furo: calotas + miolo cilíndrico (FrontSide, para não brigar com a parede do anel).
  // Azul enquanto é parte da esfera; vira violeta fantasma (cor de a) quando a broca passa e se dissolve ao sair.
  const th0 = Math.acos(G.h / (2 * G.R));
  const mTampa = aco({ side: THREE.FrontSide });
  const COR_SOLIDO = NOVO ? 0x2850C8 : COR.anel;
  const tampa = new THREE.Group(); scene.add(tampa);
  tampa.add(new THREE.Mesh(new THREE.SphereGeometry(G.R, 96, 32, 0, 2 * PI, 0, th0).rotateX(PI / 2), mTampa));
  tampa.add(new THREE.Mesh(new THREE.SphereGeometry(G.R, 96, 32, 0, 2 * PI, PI - th0, th0).rotateX(PI / 2), mTampa));
  tampa.add(new THREE.Mesh(new THREE.CylinderGeometry(G.a, G.a, G.h, 96, 1, true).rotateX(PI / 2), mTampa));
  cat('solido', tampa);

  // Broca: cilindro translúcido de raio a, aros nas pontas.
  const broca = new THREE.Group(); scene.add(broca);
  const mBroca = basico(COR.a, { opacity: 0.2 }); mBroca.userData.semprTransp = true;
  const mBrocaAro = basico(COR.a, { opacity: 0.8 }); mBrocaAro.userData.semprTransp = true;
  broca.add(new THREE.Mesh(new THREE.CylinderGeometry(G.a + 0.03, G.a + 0.03, 14, 96, 1, true).rotateX(PI / 2), mBroca));
  for (const s of [-7, 7]) { const aro = new THREE.Mesh(new THREE.TorusGeometry(G.a + 0.03, 0.05, 8, 128), mBrocaAro); aro.position.z = s; broca.add(aro); }
  broca.renderOrder = 3; cat('solido', broca);

  // Seção do corte vertical (plano y = 0): a ≤ |x| ≤ √(R² − z²), |z| ≤ h/2.
  const mSecao = new THREE.MeshStandardMaterial({ color: COR.secao, metalness: 0.0, roughness: 1.0, side: THREE.DoubleSide, envMapIntensity: 0.0 });
  mSecao.userData.base = COR.secao; tracos.push(mSecao);
  const secao = new THREE.Group(); scene.add(secao);
  for (const lado of [1, -1]) {
    const sh = new THREE.Shape(), n = 64;
    sh.moveTo(lado * G.a, -G.h / 2); sh.lineTo(lado * G.a, G.h / 2);
    for (let i = 0; i <= n; i++) { const z = G.h / 2 - G.h * i / n; sh.lineTo(lado * Math.sqrt(G.R * G.R - z * z), z); }
    const g = new THREE.ShapeGeometry(sh).rotateX(PI / 2);      // (x, y) da forma → (x, 0, y)
    const m = new THREE.Mesh(g, mSecao); m.position.y = 0.004; secao.add(m);
  }
  cat('solido', secao);

  // ---------- segmentos (tubos finos entre dois pontos) ----------
  const geoSeg = new THREE.CylinderGeometry(1, 1, 1, 12, 1, false).translate(0, 0.5, 0);   // base na origem, cresce em +y
  // cada tubo leva gêmeos atrás dele: halo escuro (#050816, ~88 %) e, na linha de h, um brilho ciano externo
  const gemeos = [];
  function seg(mat, raio = 0.05, brilho = false) {
    const m = new THREE.Mesh(geoSeg, mat); m.userData.r = raio; m.userData.cat = 'aux'; scene.add(m);
    if (!window.HALO) {                  // v4.1: sem halo escuro (pedido do Kaio); v5: só a linha de h ganha brilho magenta suave
      if (brilho) {
        const g = new THREE.Mesh(geoSeg, new THREE.MeshBasicMaterial({ color: COR.h, transparent: true, opacity: 0,
          depthTest: false, depthWrite: false, blending: THREE.AdditiveBlending }));
        g.userData = { r: raio + 0.12, base: 0.35, dono: m }; scene.add(g); gemeos.push(g);
      }
      return m;
    }
    const halo = new THREE.Mesh(geoSeg, new THREE.MeshBasicMaterial({ color: COR.fundo, transparent: true, opacity: 0,
      depthTest: false, depthWrite: false }));
    halo.userData = { r: raio + 0.16, base: 0.9, dono: m }; scene.add(halo); gemeos.push(halo);
    if (brilho) {
      const g = new THREE.Mesh(geoSeg, new THREE.MeshBasicMaterial({ color: COR.h, transparent: true, opacity: 0,
        depthTest: false, depthWrite: false }));
      g.userData = { r: raio + 0.26, base: 0.4, dono: m }; scene.add(g); gemeos.push(g);
    }
    return m;
  }
  function poeSeg(m, p, q, frac = 1) {
    const d = q.clone().sub(p), L = d.length() * frac;
    m.visible = L > 1e-4 && m.material.visible;
    if (!m.visible) return;
    m.position.copy(p); m.scale.set(m.userData.r, L, m.userData.r);
    m.quaternion.setFromUnitVectors(V3(0, 1, 0), d.normalize());
  }
  function poeGemeos() {                           // depois de posicionar os tubos: halos seguem o dono
    for (const gm of gemeos) {
      const m = gm.userData.dono, ext = gm.userData.r - m.userData.r;
      gm.visible = m.visible && m.material.visible;
      if (!gm.visible) continue;
      gm.material.opacity = gm.userData.base * m.material.opacity;
      gm.quaternion.copy(m.quaternion);
      const dir = V3(0, 1, 0).applyQuaternion(m.quaternion);
      gm.position.copy(m.position).sub(dir.clone().multiplyScalar(ext * 0.6));
      gm.scale.set(gm.userData.r, m.scale.y + 1.2 * ext, gm.userData.r);
      gm.renderOrder = m.renderOrder - (gm.userData.base < 0.5 ? 0.7 : 0.4);
    }
  }
  const linhaCor = c => { const m = basico(c, { opacity: 1, depthTest: false }); m.userData.semprTransp = true; return m; };
  // v4.1 (Kaio): sobre o sólido azul, R em branco e h, h/2 em magenta
const mLinha = linhaCor(COR.geo), mLinhaR = linhaCor(0xF2F6FF), mLinhaA = linhaCor(COR.a), mLinhaH = linhaCor(COR.h);
  // linhas auxiliares sempre por cima (depthTest off) e grossas: ≥ 3 px no 540×960 em todas as vistas
  const mLinhaFat = linhaCor(COR.geo), mLinhaFatR = linhaCor(0xF2F6FF), mLinhaFatA = linhaCor(COR.a);
  const triR = seg(mLinhaR, 0.08), triA = seg(mLinhaA, 0.08), triH = seg(mLinhaH, 0.08, true), triHc = seg(mLinhaH, 0.095, true);   // v5: h +1 px
  const triQ1 = seg(mLinha, 0.04), triQ2 = seg(mLinha, 0.04);
  const ponto = (mat, r) => { const m = new THREE.Mesh(new THREE.SphereGeometry(r, 16, 12), mat); m.userData.cat = 'aux'; scene.add(m); return m; };
  const triO = ponto(mLinha, 0.13);
  [triR, triA, triH, triHc, triQ1, triQ2, triO].forEach(m => (m.renderOrder = 10));

  // ---------- plano de corte horizontal, coroa e disco ----------
  const plano = new THREE.Group(); scene.add(plano);
  const mPlano = basico(COR.geo, { opacity: 0.07 }); mPlano.userData.semprTransp = true;
  const mPlanoBorda = new THREE.LineBasicMaterial({ color: COR.geo, transparent: true, opacity: 0.55, depthWrite: false });
  plano.add(new THREE.Mesh(new THREE.PlaneGeometry(1, 1), mPlano));
  plano.add(new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.PlaneGeometry(1, 1)), mPlanoBorda));
  plano.renderOrder = 4; cat('plano', plano);

  const mCoroa = basico(0xffffff, { opacity: 0.9 }); mCoroa.userData.semprTransp = true;
  const mContorno = new THREE.LineBasicMaterial({ color: COR.azulClaro, transparent: true, opacity: 1, depthWrite: false });
  const mContDisco = new THREE.LineBasicMaterial({ color: COR.esfClaro, transparent: true, opacity: 1, depthWrite: false });
  const coroa = new THREE.Mesh(new THREE.RingGeometry(G.a, G.R, 160, 1), mCoroa); coroa.renderOrder = 6; scene.add(coroa);
  const circ = n => { const p = []; for (let i = 0; i <= n; i++) p.push(Math.cos(2 * PI * i / n), Math.sin(2 * PI * i / n), 0);
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(p, 3)); return g; };
  const geoCirc = circ(160);
  const contExt = new THREE.Line(geoCirc, mContorno), contInt = new THREE.Line(geoCirc, mContorno);
  contExt.renderOrder = contInt.renderOrder = 7; scene.add(contExt, contInt);
  cat('solido', coroa); cat('aux', contExt, contInt);

  // Esfera de Cavalieri (raio h/2): magenta translúcida, contorno por fresnel; abaixo do plano mais densa que acima.
  const fresnel = (borda, corpo) => new THREE.ShaderMaterial({
    uniforms: { uZ: { value: 100 }, uA: { value: 0 }, uCor: { value: new THREE.Color(borda) }, uCorpo: { value: new THREE.Color(corpo) } },
    vertexShader: `varying vec3 vN; varying vec3 vW; varying vec3 vV;
      void main(){ vec4 w = modelMatrix * vec4(position,1.0); vW = w.xyz; vN = normalize(mat3(modelMatrix) * normal);
        vV = normalize(cameraPosition - w.xyz); gl_Position = projectionMatrix * viewMatrix * w; }`,
    fragmentShader: `uniform float uZ, uA; uniform vec3 uCor, uCorpo; varying vec3 vN; varying vec3 vW; varying vec3 vV;
      void main(){ float f = pow(1.0 - abs(dot(normalize(vN), normalize(vV))), 2.2);
        float abaixo = step(vW.z, uZ);
        float a = mix(0.06 + 0.40 * f, 0.20 + 0.55 * f, abaixo);
        gl_FragColor = vec4(mix(uCorpo * 0.75, uCor, 0.15 + 0.6 * f), uA * a); }`,
    transparent: true, depthWrite: false, side: THREE.DoubleSide,
  });
  const mCav = fresnel(COR.esfClaro, COR.esf);
  const cav = new THREE.Mesh(new THREE.SphereGeometry(G.h / 2, 96, 64).rotateX(PI / 2), mCav);
  cav.position.x = G.x_esfera_cav; cav.renderOrder = 5; scene.add(cav);
  const mDisco = basico(COR.esf, { opacity: 0.8 }); mDisco.userData.semprTransp = true;
  const disco = new THREE.Mesh(new THREE.CircleGeometry(1, 128), mDisco); disco.renderOrder = 6; scene.add(disco);
  const contDisco = new THREE.Line(geoCirc, mContDisco); contDisco.renderOrder = 7; scene.add(contDisco);
  cat('solido', cav, disco); cat('aux', contDisco);

  // Esfera original fantasma (C03, quando o R sai da conta): magenta translúcida de raio R, aparece e some.
  const mFant = fresnel(0xF7B8FF, COR.R);
  const fantasma = new THREE.Mesh(new THREE.SphereGeometry(G.R, 96, 64).rotateX(PI / 2), mFant);
  fantasma.renderOrder = 8; scene.add(fantasma); cat('solido', fantasma);

  // Guardanapo do hook (C01a): tecido claro franzido, enrolado e passado pelo anel R = 7 (eixo z). Dentro do anel o raio
  // fica abaixo do furo (a = 6,32); fora dele o tecido se abre e fecha arredondado nas pontas.
  const mGuard = new THREE.MeshStandardMaterial({ color: 0xCFC8B8, metalness: 0, roughness: 1.0, envMapIntensity: 0.12,
    side: THREE.DoubleSide });
  const ZG = 8.6;
  const perfilGuard = u => {                                  // raio médio do tecido em |z| = u
    if (u <= 3.2) return 5.5;
    if (u <= 6.4) return 5.5 + 0.9 * suave((u - 3.2) / 3.2);
    return 6.4 * Math.sqrt(Math.max(0.12, 1 - ((u - 6.4) / 2.3) ** 2));
  };
  const geoGuard = (() => {
    const nT = 192, nZ = 96, pos = [], idx = [];
    for (let j = 0; j <= nZ; j++) {
      const z = -ZG + 2 * ZG * j / nZ, b = perfilGuard(Math.abs(z));
      for (let i = 0; i <= nT; i++) {
        const th = 2 * PI * i / nT, r = b * (1 + 0.035 * Math.sin(13 * th + 0.5 * Math.sin(0.9 * z)) + 0.012 * Math.sin(29 * th));
        pos.push(r * Math.cos(th), r * Math.sin(th), z);
      }
    }
    for (let j = 0; j < nZ; j++) for (let i = 0; i < nT; i++) {
      const a = j * (nT + 1) + i, b = a + 1, c = a + nT + 1, d = c + 1;
      idx.push(a, c, b, b, c, d);
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setIndex(idx); g.computeVertexNormals();
    return g;
  })();
  const guardanapo = new THREE.Group(); scene.add(guardanapo);
  guardanapo.add(new THREE.Mesh(geoGuard, mGuard));
  for (const s of [-1, 1]) {                                   // miolo das pontas
    const tampaG = new THREE.Mesh(new THREE.CircleGeometry(perfilGuard(ZG) * 1.02, 64), mGuard);
    tampaG.position.z = s * ZG; guardanapo.add(tampaG);
  }
  cat('solido', guardanapo);

  // Elementos da fatia (C03): eixo z, raios externo/interno e o R do centro até a borda.
  const fatZ = seg(mLinhaFat, 0.06), fatExt = seg(mLinhaFat, 0.06), fatInt = seg(mLinhaFatA, 0.065), fatR = seg(mLinhaFatR, 0.065);
  const fatO = ponto(mLinhaFat, 0.13), fatZc = ponto(mLinhaFat, 0.11);
  [fatZ, fatExt, fatInt, fatR, fatO, fatZc].forEach(m => (m.renderOrder = 9));

  // Triângulo dentro da esfera pequena (C04): z (centro → plano), ρ (raio do disco), h/2 (hipotenusa).
  const mCavZ = linhaCor(COR.geo), mCavRho = linhaCor(COR.esfClaro), mCavHip = linhaCor(COR.h);
  const cavZ = seg(mCavZ, 0.075), cavRho = seg(mCavRho, 0.085), cavHip = seg(mCavHip, 0.08), cavO = ponto(mCavZ, 0.16);
  [cavZ, cavRho, cavHip, cavO].forEach(m => (m.renderOrder = 11));

  // ---------- trio do gancho (R = 5, 7, 10; h = 6), mesma escala e mesma câmera ----------
  // v4 (C01c): cada anel nasce de uma esfera (tampa = calotas + miolo, como no C02) furada por sua broca; as três
  // esferas ficam espalhadas em z (sem se tocar) e os anéis se juntam no trio depois do furo.
  const ESPALHADO = TL.geometria.trio_espalhado_zc;
  const LUZ_TRIO = [1.0, 0.9, 0.8];                    // fator ≤ 1 (getHex estoura acima de 1)
  const trio = TL.geometria.trio.map(({ R, zc }, i) => {
    const a = Math.sqrt(R * R - G.h * G.h / 4), g = new THREE.Group(), c = COR.trio[i];
    const mz = solido(NOVO ? {} : { color: c }), mp = solido(NOVO ? { side: THREE.BackSide } : { color: c, side: THREE.BackSide });
    mz.userData.base = mp.userData.base = NOVO ? new THREE.Color(1, 1, 1).multiplyScalar(LUZ_TRIO[i]).getHex() : c;
    tracos.push(mz, mp);
    const zona = new THREE.Mesh(pinta(geoZona(R, G.h), G.h), mz);
    g.add(zona, new THREE.Mesh(pinta(geoParede(a, G.h), G.h, true), mp));
    scene.add(g); cat('solido', g);
    const rz = NOVO ? rim(zona) : null;
    const ml = malha(g, R, G.h);
    const th = Math.acos(G.h / (2 * R)), mt = aco({ side: THREE.FrontSide }), tp = new THREE.Group();
    tp.add(new THREE.Mesh(new THREE.SphereGeometry(R, 96, 32, 0, 2 * PI, 0, th).rotateX(PI / 2), mt));
    tp.add(new THREE.Mesh(new THREE.SphereGeometry(R, 96, 32, 0, 2 * PI, PI - th, th).rotateX(PI / 2), mt));
    tp.add(new THREE.Mesh(new THREE.CylinderGeometry(a, a, G.h, 96, 1, true).rotateX(PI / 2), mt));
    scene.add(tp); cat('solido', tp);
    const br = new THREE.Group(), mb = basico(COR.a, { opacity: 0.2 }), mba = basico(COR.a, { opacity: 0.8 });
    mb.userData.semprTransp = mba.userData.semprTransp = true;
    br.add(new THREE.Mesh(new THREE.CylinderGeometry(a + 0.03, a + 0.03, 1, 96, 1, true).rotateX(PI / 2), mb));
    for (const s of [-0.5, 0.5]) { const aro = new THREE.Mesh(new THREE.TorusGeometry(a + 0.03, 0.06, 8, 128), mba); aro.position.z = s; br.add(aro); }
    br.renderOrder = 3; scene.add(br); cat('solido', br);
    return { R, a, zc, z0: ESPALHADO[i], g, mats: [mz, mp], lado: i !== 1, rz, ml, mt, tp, br, mb, mba, zAtual: zc, esf: 0 };
  });

  // ---------- estrelas (cena separada, fov fixo) ----------
  const ceu = new THREE.Scene(), camCeu = new THREE.PerspectiveCamera(40, W / H, 1, 1000);
  {
    let s = 29; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    const pos = [], cor = [];
    for (let i = 0; i < 700; i++) {
      const u = 2 * rnd() - 1, th = 2 * PI * rnd(), q = Math.sqrt(1 - u * u), b = 0.22 + 0.5 * rnd() ** 2;
      pos.push(400 * q * Math.cos(th), 400 * q * Math.sin(th), 400 * u); cor.push(b, b, b);
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    geo.setAttribute('color', new THREE.Float32BufferAttribute(cor, 3));
    ceu.add(new THREE.Points(geo, new THREE.PointsMaterial({ size: 1.6, sizeAttenuation: false, vertexColors: true })));
  }

  // ---------- câmera por chaves de vista + dolly-zoom ----------
  // alt = altura visível (cm) no plano do alvo → 1 cm = 16/alt unidades do Manim. yc = altura do alvo no quadro do Manim.
  const camera = new THREE.PerspectiveCamera(30, W / H, 0.05, 3000);
  const CAMPOS = ['az', 'el', 'fov', 'alt', 'yc', 'xc'];
  const estadoChave = k => Object.assign({}, TL.vistas[k.vista], k.az !== undefined ? { az: k.az } : {});
  // v2: interpolação cúbica monótona (Fritsch–Carlson) por canal, através de TODAS as chaves. A velocidade da câmera é
  // contínua: um giro não para de repente para recomeçar na vista seguinte (era a "travada" das transições do v1),
  // trechos parados continuam parados e não há passagem do alvo (sem overshoot). 'ease' nas chaves fica sem efeito.
  const camCanais = (() => {
    const L = TL.camera, ts = L.map(k => k.t), E = L.map(estadoChave);
    const canal = vs => {
      const n = vs.length, d = [], m = new Array(n).fill(0);
      for (let i = 0; i < n - 1; i++) d.push((vs[i + 1] - vs[i]) / Math.max(ts[i + 1] - ts[i], 1e-9));
      for (let i = 1; i < n - 1; i++) {
        if (d[i - 1] * d[i] <= 0) continue;
        const h0 = ts[i] - ts[i - 1], h1 = ts[i + 1] - ts[i], w1 = 2 * h1 + h0, w2 = h1 + 2 * h0;
        m[i] = (w1 + w2) / (w1 / d[i - 1] + w2 / d[i]);
      }
      return { vs, m };
    };
    const c = {};
    for (const k of CAMPOS) c[k] = canal(E.map(e => e[k]));
    for (let j = 0; j < 3; j++) c['alvo' + j] = canal(E.map(e => e.alvo[j]));
    return { ts, c };
  })();
  function estadoCamera(t) {
    const { ts, c } = camCanais, n = ts.length;
    t = clamp(t, ts[0], ts[n - 1]);
    let i = 0;
    while (i < n - 2 && t > ts[i + 1]) i++;
    const h = Math.max(ts[i + 1] - ts[i], 1e-9), u = (t - ts[i]) / h, u2 = u * u, u3 = u2 * u;
    const herm = ({ vs, m }) => (2 * u3 - 3 * u2 + 1) * vs[i] + (u3 - 2 * u2 + u) * h * m[i] +
      (-2 * u3 + 3 * u2) * vs[i + 1] + (u3 - u2) * h * m[i + 1];
    const o = {};
    for (const k of CAMPOS) o[k] = herm(c[k]);
    o.alvo = [0, 1, 2].map(j => herm(c['alvo' + j]));
    return o;
  }
  let camAz = -90;
  function posicionaCamera(c) {
    const az = c.az * PI / 180, el = c.el * PI / 180, D = (c.alt / 2) / Math.tan(c.fov * PI / 360);
    const alvo = V3(...c.alvo);
    camAz = c.az; camera.fov = c.fov;
    camera.position.set(alvo.x + D * Math.cos(el) * Math.cos(az), alvo.y + D * Math.cos(el) * Math.sin(az), alvo.z + D * Math.sin(el));
    camera.up.set(-Math.sin(el) * Math.cos(az), -Math.sin(el) * Math.sin(az), Math.cos(el));
    camera.lookAt(alvo);
    camera.near = Math.max(0.05, D - 45); camera.far = D + 45;
    camera.setViewOffset(W, H, -c.xc / 9 * W, c.yc / 16 * H, W, H);   // v4: xc desloca o alvo na horizontal
    camera.updateProjectionMatrix();
    camera.updateMatrixWorld();      // v3: projeta() no mesmo quadro (caixas de silhueta) usa a câmera atual
    camCeu.quaternion.copy(camera.quaternion);
    // luz principal presa à câmera (acima e à esquerda), contraluz do lado oposto: mesma leitura em todas as vistas
    const dir = camera.position.clone().sub(alvo).normalize(), dir_up = camera.up.clone(), dir_dir = V3(-Math.sin(az), Math.cos(az), 0);
    chave.position.copy(alvo).add(dir.clone().multiplyScalar(30)).add(dir_up.clone().multiplyScalar(22)).add(dir_dir.clone().multiplyScalar(-14));
    chave.target.position.copy(alvo);
    contra.position.copy(alvo).add(dir.clone().multiplyScalar(-20)).add(dir_dir.clone().multiplyScalar(18)).add(V3(0, 0, 10));
    contra.target.position.copy(alvo);
  }
  const direita = () => { const az = camAz * PI / 180; return V3(-Math.sin(az), Math.cos(az), 0); };

  // ---------- estado numérico do quadro ----------
  let VAL = {}, ANC = {}, CX = {}, r_vis = [0, 0, 0];
  function calcula(t) {
    const pv = K('plano_vis', t), z = K('plano_z', t), R = K('R_anel', t), h = K('h_anel', t), a = Math.sqrt(Math.max(R * R - h * h / 4, 0));
    const rext = Math.sqrt(Math.max(G.R * G.R - z * z, 0)), rdis = Math.sqrt(Math.max(G.h * G.h / 4 - z * z, 0));
    VAL = { t, z, plano_vis: pv, rext, rint: G.a, rdisco: rdis,
      A_anel: PI * (rext * rext - G.a * G.a), A_esfera: PI * rdis * rdis,
      A_anel_pi: rext * rext - G.a * G.a, A_esfera_pi: rdis * rdis,
      R, a_furo: a, V_pi: G.h ** 3 / 6, h, V_anel: PI * h ** 3 / 6 };
    return VAL;
  }

  // ---------- quadro ----------
  window.setFrame = function (f) {
    const t = f / FPS, v = calcula(t);
    posicionaCamera(estadoCamera(t));
    const u = direita();

    // realce: 1 = o 3D recua para a álgebra, no máximo até 75 % do brilho
    const realce = K('realce_3d', t);
    for (const m of tracos) m.color.set(m.userData.base !== undefined ? m.userData.base : COR.anel).multiplyScalar(1 - 0.25 * realce);

    // trio
    const tv = K('trio_vis', t), tl = K('trio_lados', t), junta = K('trio_junta', t);
    trio.forEach((r, i) => {
      const vis = tv * (r.lado ? tl : 1), dt = 0.35 * i;          // furo escalonado: pequena, média, grande
      for (const m of r.mats) opac(m, vis);
      r.zAtual = r.z0 + (r.zc - r.z0) * junta;
      r.g.position.z = r.zAtual;
      if (r.rz) r.rz.material.uniforms.uA.value = vis;
      r.ml.material.opacity = 0.12 * vis;
      const furo = K('trio_furo', t - dt), tpv = K('trio_tampa', t) * vis;
      r.mt.color.set(COR_SOLIDO).lerp(new THREE.Color(COR.a), furo);
      opac(r.mt, tpv * (1 - 0.7 * furo)); r.tp.position.z = r.zAtual - K('trio_tampa_desce', t);
      r.esf = tpv * (1 - furo);
      const L = Math.max(2 * r.R * K('trio_broca_L', t - dt), 1e-3), bvv = K('trio_broca_vis', t - dt) * vis * (L > 0.01 ? 1 : 0);
      opac(r.mb, bvv, 0.2); opac(r.mba, bvv, 0.8);
      r.br.scale.set(1, 1, L); r.br.position.z = r.zAtual + r.R - L / 2;
      for (const ch of r.br.children) if (ch.geometry.type === 'TorusGeometry') ch.scale.z = 1 / L;   // aro não estica
    });
    r_vis = trio.map(r => tv * (r.lado ? tl : 1));

    // guardanapo (hook)
    opac(mGuard, K('guardanapo_vis', t)); guardanapo.position.z = K('guardanapo_z', t);

    // anel principal (R pode variar no C06)
    refazAnel(v.R, Math.max(v.h, 0.04));          // v5: h vai a 0 no C07 (geometria com piso)
    const av = K('anel_vis', t), pv = v.plano_vis;
    planoY.constant = K('corte_v', t);
    const z0 = pv > 0.001 ? v.z : 100;
    planoZs.constant = z0; planoZg.constant = -z0;
    opac(mZonaS, av); opac(mParS, av);
    const fant = av * (1 + (0.13 - 1) * pv);                        // acima do plano: some para 13 % com o plano
    opac(mZonaG, fant); opac(mParG, fant);
    if (pv > 0.001) { mZonaG.transparent = mParG.transparent = true; mZonaG.depthWrite = mParG.depthWrite = false; }
    rimS.material.uniforms.uA.value = NOVO ? av * (1 - 0.25 * realce) : 0;
    rimG.material.uniforms.uA.value = NOVO ? fant * (1 - 0.25 * realce) : 0;
    malhaAnel.material.opacity = 0.12 * av * (1 - 0.85 * pv);

    // furo
    const amb = K('tampa_furo', t), tpv = K('tampa_vis', t) * av * (1 - 0.7 * amb);
    mTampa.color.set(COR_SOLIDO).lerp(new THREE.Color(COR.a), amb);
    opac(mTampa, tpv); tampa.position.z = -K('tampa_desce', t);
    const bv = K('broca_vis', t);
    // v3: a broca avança a partir do topo da esfera (comprimento broca_L): nunca sai da zona do 3D pelo alto
    const sb = (K('broca_a', t) + 0.03) / (G.a + 0.03), bL = Math.max(K('broca_L', t), 1e-3);
    opac(mBroca, bv * (bL > 0.01 ? 1 : 0), 0.2); opac(mBrocaAro, bv * (bL > 0.01 ? 1 : 0), 0.8);
    broca.scale.set(sb, sb, bL / 14); broca.position.z = K('broca_topo', t) - bL / 2;
    for (const ch of broca.children) if (ch.geometry.type === 'TorusGeometry') ch.scale.z = 14 / bL;
    opac(mSecao, K('secao_vis', t) * av);

    // triângulo do corte vertical
    const tri = K('tri_vis', t), O = V3(0, -0.08, 0), Q = V3(G.a, -0.08, 0), P = V3(G.a, -0.08, G.h / 2);
    for (const m of [mLinha, mLinhaR, mLinhaA, mLinhaH]) opac(m, tri);
    poeSeg(triR, O, P, K('tri_R', t)); poeSeg(triA, O, Q, K('tri_a', t)); poeSeg(triH, Q, P, K('tri_h', t));
    poeSeg(triHc, V3(-G.a, -0.08, -G.h / 2), V3(-G.a, -0.08, G.h / 2), K('tri_hcheia', t));
    const q = 0.45 * Math.min(1, K('tri_h', t) * 3);
    poeSeg(triQ1, V3(G.a - q, -0.08, 0), V3(G.a - q, -0.08, q)); poeSeg(triQ2, V3(G.a - q, -0.08, q), V3(G.a, -0.08, q));
    triO.position.copy(O); triO.visible = tri > 0.003 && K('tri_R', t) > 0;

    // plano horizontal
    // v3: o plano gira com o azimute da câmera (bordas paralelas ao quadro): largura projetada = plano_w, sem quina
    // saindo pelas laterais
    plano.position.set(K('plano_x', t), 0, v.z); plano.scale.set(K('plano_w', t), Math.min(K('plano_w', t), 11), 1);
    plano.rotation.z = (camAz + 90) * PI / 180;
    opac(mPlano, pv, 0.07); mPlanoBorda.opacity = 0.55 * pv; mPlanoBorda.visible = pv > 0.003;

    // coroa no anel (só com o plano dentro do anel e o anel visível)
    const cv = pv * av * (v.rext > G.a + 1e-3 ? 1 : 0);
    opac(mCoroa, cv, 0.9);
    if (cv > 0.003) { coroa.geometry.dispose(); coroa.geometry = new THREE.RingGeometry(G.a, v.rext, 160, 1); }
    coroa.position.set(0, 0, v.z + 0.012);
    contExt.scale.set(v.rext, v.rext, 1); contExt.position.set(0, 0, v.z + 0.02);
    contInt.scale.set(G.a, G.a, 1); contInt.position.set(0, 0, v.z + 0.02);
    mContorno.opacity = pv; mContorno.visible = pv > 0.003;
    contExt.visible = contInt.visible = cv > 0.003;

    // esfera de Cavalieri e o disco
    const kv = K('cav_vis', t);
    mCav.uniforms.uA.value = kv * (1 - 0.25 * realce); mCav.uniforms.uZ.value = pv > 0.001 ? v.z : 100; cav.visible = kv > 0.003;
    const dv = pv * kv * (v.rdisco > 1e-3 ? 1 : 0);
    opac(mDisco, dv, 0.85);
    disco.scale.set(Math.max(v.rdisco, 1e-3), Math.max(v.rdisco, 1e-3), 1); disco.position.set(G.x_esfera_cav, 0, v.z + 0.012);
    contDisco.scale.copy(disco.scale); contDisco.position.set(G.x_esfera_cav, 0, v.z + 0.02); contDisco.visible = dv > 0.003;
    mContDisco.opacity = pv;

    // esfera original fantasma (o R saindo da conta)
    const ef = K('esfera_fantasma', t);
    mFant.uniforms.uA.value = 0.75 * ef; mFant.uniforms.uZ.value = 100; fantasma.visible = ef > 0.003;
    fantasma.scale.setScalar(K('fantasma_R', t) / G.R);

    // triângulo na esfera pequena: centro → (z) → borda do disco (ρ), hipotenusa h/2
    const ct = K('cav_tri', t) * kv, xs = G.x_esfera_cav;
    for (const m of [mCavZ, mCavRho, mCavHip]) opac(m, ct);
    const cC = V3(xs, 0, 0), cZ = V3(xs, 0, v.z), cE = cZ.clone().add(u.clone().multiplyScalar(v.rdisco));
    poeSeg(cavZ, cC, cZ); poeSeg(cavRho, cZ, cE); poeSeg(cavHip, cC, cE);
    cavO.position.copy(cC); cavO.visible = ct > 0.003;

    // fatia: eixo z, raios, R
    const fv = K('fatia_vis', t), zc = V3(0, 0, v.z + 0.03), o = V3(0, 0, 0);
    for (const m of [mLinhaFat, mLinhaFatR, mLinhaFatA]) opac(m, fv);
    poeSeg(fatZ, o, zc); poeSeg(fatExt, zc, zc.clone().add(u.clone().multiplyScalar(v.rext)));
    poeSeg(fatInt, zc, zc.clone().add(u.clone().multiplyScalar(-G.a)));
    poeSeg(fatR, o, zc.clone().add(u.clone().multiplyScalar(v.rext)));
    fatO.position.copy(o); fatZc.position.copy(zc); fatO.visible = fatZc.visible = fv > 0.003;

    // âncoras nomeadas (pontos 3D) para o Manim e o Remotion
    const pZ = V3(0, 0, v.z + 0.03), ext = pZ.clone().add(u.clone().multiplyScalar(v.rext)), int = pZ.clone().add(u.clone().multiplyScalar(-G.a));
    const pZs = V3(xs, 0, v.z + 0.03), extS = pZs.clone().add(u.clone().multiplyScalar(v.rdisco));
    ANC = {
      O: [0, 0, 0], Q: [G.a, 0, 0], P: [G.a, 0, G.h / 2], meio_R: [G.a / 2, 0, G.h / 4], meio_a: [G.a / 2, 0, 0],
      meio_h2: [G.a, 0, G.h / 4], parede_e_baixo: [-G.a, 0, -G.h / 2], parede_e_cima: [-G.a, 0, G.h / 2],
      fat_zc: pZ.toArray(), fat_zmeio: [0, 0, v.z / 2], fat_ext: ext.toArray(), fat_int: int.toArray(),
      fat_ext_meio: pZ.clone().lerp(ext, 0.5).toArray(), fat_int_meio: pZ.clone().lerp(int, 0.5).toArray(),
      fat_R_meio: V3(0, 0, 0).lerp(ext, 0.5).toArray(),
      anel_base: [0, 0, -G.h / 2], anel_topo: [0, 0, G.h / 2], esf_centro: [xs, 0, 0], esf_base: [xs, 0, -G.h / 2],
      esf_topo: [xs, 0, G.h / 2], esf_ext: extS.toArray(), anel_dir: u.clone().multiplyScalar(v.R).toArray(),
    };
    Object.assign(ANC, { cav_zc: cZ.toArray(), cav_z_meio: cC.clone().lerp(cZ, 0.5).toArray(),
      cav_rho_meio: cZ.clone().lerp(cE, 0.5).toArray(), cav_hip_meio: cC.clone().lerp(cE, 0.5).toArray() });
    // Réguas de h ancoradas em 3D: a haste fica fora da silhueta (−(R + folga)·u), no MESMO plano de profundidade das
    // arestas do anel (os pontos −a·u, ±h/2 das bordas do furo); por isso a altura projetada da haste é a da aresta.
    const regua = (c, R, a, n) => {
      const f = u.clone().multiplyScalar(-(R + 0.9)), e = u.clone().multiplyScalar(-a);
      ANC[`${n}_cima`] = c.clone().add(f).add(V3(0, 0, G.h / 2)).toArray();
      ANC[`${n}_baixo`] = c.clone().add(f).add(V3(0, 0, -G.h / 2)).toArray();
      ANC[`${n}_aresta_cima`] = c.clone().add(e).add(V3(0, 0, G.h / 2)).toArray();
      ANC[`${n}_aresta_baixo`] = c.clone().add(e).add(V3(0, 0, -G.h / 2)).toArray();
    };
    regua(V3(0, 0, 0), v.R, v.a_furo, 'regua_anel');
    trio.forEach((r, i) => {
      const c = V3(0, 0, r.zAtual), dir = u.clone().multiplyScalar(r.R + 0.5);
      regua(c, r.R, r.a, `regua${i}`);
      ANC[`rot${i}`] = c.clone().add(dir).toArray();
      ANC[`trio${i}_centro`] = c.toArray();
    });

    // caixas projetadas das silhuetas (px), para rótulos que se afastam do sólido e para o QA de margens
    CX = {};
    const caixa = pts => { let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
      for (const p of pts) { const [x, y] = window.projeta(p); x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); }
      return [x0, y0, x1, y1]; };
    const ptsAnel = (c, R, h) => { const p = [];
      for (let j = 0; j <= 8; j++) { const z = -h / 2 + h * j / 8, r = Math.sqrt(R * R - z * z);
        for (let i = 0; i < 48; i++) p.push([c[0] + r * Math.cos(2 * PI * i / 48), c[1] + r * Math.sin(2 * PI * i / 48), c[2] + z]); }
      return p; };
    const ptsEsf = (c, R) => { const p = [];
      for (let j = 0; j <= 12; j++) { const z = -R + 2 * R * j / 12, r = Math.sqrt(Math.max(R * R - z * z, 0));
        for (let i = 0; i < 36; i++) p.push([c[0] + r * Math.cos(2 * PI * i / 36), c[1] + r * Math.sin(2 * PI * i / 36), c[2] + z]); }
      return p; };
    if (av > 0.05) CX.anel = caixa(ptsAnel([0, 0, 0], v.R, v.h));
    // trio: enquanto a esfera existe, a caixa cresce até a dela (rótulos R = … acompanham sem pular)
    trio.forEach((r, i) => {
      if (r_vis[i] <= 0.05) return;
      const b = caixa(ptsAnel([0, 0, r.zAtual], r.R, G.h)), e = caixa(ptsEsf([0, 0, r.zAtual], r.R)), w = clamp(r.esf, 0, 1);
      CX['trio' + i] = b.map((x, j) => x + (e[j] - x) * w);
    });
    if (kv > 0.05) CX.esf = caixa(ptsEsf([xs, 0, 0], G.h / 2));
    if (ef > 0.05) CX.fantasma = caixa(ptsEsf([0, 0, 0], K('fantasma_R', t)));
    if (K('guardanapo_vis', t) > 0.05) {
      const p = [], zg = K('guardanapo_z', t);
      for (let j = 0; j <= 24; j++) { const z = -ZG + 2 * ZG * j / 24, r = 1.05 * perfilGuard(Math.abs(z));
        for (let i = 0; i < 36; i++) p.push([r * Math.cos(2 * PI * i / 36), r * Math.sin(2 * PI * i / 36), z + zg]); }
      CX.guardanapo = caixa(p);
    }
    if (pv > 0.05) {
      const w = K('plano_w', t), d = Math.min(w, 11), rz = plano.rotation.z, px0 = K('plano_x', t);
      const ex = [Math.cos(rz) * w / 2, Math.sin(rz) * w / 2], ey = [-Math.sin(rz) * d / 2, Math.cos(rz) * d / 2];
      CX.plano = caixa([[1, 1], [1, -1], [-1, 1], [-1, -1]].map(([a, b]) => [px0 + a * ex[0] + b * ey[0], a * ex[1] + b * ey[1], v.z]));
    }

    poeGemeos();
    if (window.MASCARA) { mascara(); return true; }
    renderer.clear(); renderer.render(ceu, camCeu); renderer.clearDepth(); renderer.render(scene, camera);
    return true;
  };

  // ---------- modo máscara (QA de sobreposição) ----------
  // Cada objeto visível sai em cor chapada aditiva por categoria: sólido = vermelho, linha auxiliar = verde, plano = azul.
  // Sem estrelas, sem luz. O qa/sobreposicao.py lê os canais separados.
  const COR_MASC = { solido: 0xff0000, aux: 0x00ff00, plano: 0x0000ff }, cacheMasc = new Map();
  const alfaEfetivo = m => (m.uniforms && m.uniforms.uA ? m.uniforms.uA.value : m.opacity);
  function mascara() {
    const trocas = [];
    scene.traverse(o => {
      const c = o.userData.cat;
      if (rims.includes(o) || malhas.includes(o) || gemeos.includes(o)) { trocas.push([o, o.material, o.visible]); o.visible = false; return; }
      if (!c || !o.material || !(o.isMesh || o.isLine)) return;
      const m = o.material, vis = o.visible && m.visible !== false && alfaEfetivo(m) > (c === 'plano' ? 0.003 : 0.04);
      const chaveM = m.uuid + (o.isLine ? 'L' : 'M');
      if (!cacheMasc.has(chaveM)) {
        const base = { color: COR_MASC[c], transparent: true, opacity: 1, blending: THREE.AdditiveBlending, depthTest: false,
          depthWrite: false, side: THREE.DoubleSide, clippingPlanes: m.clippingPlanes || null };
        cacheMasc.set(chaveM, o.isLine ? new THREE.LineBasicMaterial(base) : new THREE.MeshBasicMaterial(base));
      }
      trocas.push([o, m, o.visible]);
      o.material = cacheMasc.get(chaveM); o.visible = vis;
    });
    renderer.setClearColor(0x000000, 1); renderer.clear(); renderer.render(scene, camera);
    renderer.setClearColor(COR.fundo, 1);
    for (const [o, m, v] of trocas) { o.material = m; o.visible = v; }
  }
  window.projeta = p => { const v = V3(...p).project(camera); return [(v.x + 1) / 2 * W, (1 - v.y) / 2 * H]; };
  window.ancoras = () => ANC;
  window.caixas = () => CX;
  // QA: pontas reais dos tubos desenhados (da matriz do mesh), para conferir com as âncoras dos rótulos
  const TUBOS = { triR, triA, triH, fatZ, fatExt, fatInt, fatR, cavZ, cavRho, cavHip };
  window.pontas = () => {
    const o = {};
    for (const [n, m] of Object.entries(TUBOS)) {
      if (!m.visible) continue;
      m.updateMatrixWorld();
      o[n] = [V3(0, 0, 0).applyMatrix4(m.matrixWorld).toArray(), V3(0, 1, 0).applyMatrix4(m.matrixWorld).toArray()];
    }
    return o;
  };
  window.valores = () => VAL;
  window.cenaPronta = true;
})();
