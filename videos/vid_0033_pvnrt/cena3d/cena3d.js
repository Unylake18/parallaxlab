// vid_0033 v2 — gás ideal em uma caixa (Three.js r128). Tudo é função do quadro: window.setFrame(f), sem relógio.
// window.TIMELINE (timeline.json) é injetado pelo render3d.js. Posição de cada molécula = onda triangular da coordenada desdobrada
// s = s0 + v·G (colisões elásticas, sem colisão molécula–molécula). Os CENTROS ficam em [−1, 1] (x: [−1, −1 + Lx]); a caixa é desenhada
// em ±(1 + r) para a esfera nunca atravessar a parede. O pistão (C07) é a parede +x do mesmo recipiente (Lx de 2 a 1).
(function () {
  const TL = window.TIMELINE, FPS = TL.fps, N = TL.s0.length, PI = Math.PI, DEBUG = !!window.DEBUG_ALINHA, R = TL.r_esf;
  const COR = { aco: 0x86A0C6, acomp: 0xDCE9FF, geo: 0xB8C4DA, gelo: 0x9CC7FF, fundo: 0x0B1426 };
  const W = innerWidth, H = innerHeight, WALL = 1 + R;
  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H); renderer.setClearColor(0x050816, 1); renderer.autoClear = false;
  document.body.appendChild(renderer.domElement);

  const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
  const suave = u => { u = clamp(u, 0, 1); return u * u * (3 - 2 * u); };
  const tri = s => 2 - Math.abs((((s % 4) + 4) % 4) - 2);
  const mod4 = s => ((s % 4) + 4) % 4;

  // ---------- fundo (azul espacial do vid_0031) ----------
  const matFundo = new THREE.ShaderMaterial({
    vertexShader: 'void main(){ gl_Position = vec4(position.xy, 0.0, 1.0); }',
    fragmentShader: `void main(){ vec2 p = gl_FragCoord.xy / vec2(${W.toFixed(1)}, ${H.toFixed(1)});
      vec3 cor = mix(vec3(0.020, 0.031, 0.075), vec3(0.055, 0.095, 0.175), pow(p.y, 1.3)); gl_FragColor = vec4(cor, 1.0); }`,
    depthTest: false, depthWrite: false,
  });
  const cenaFundo = new THREE.Scene(); cenaFundo.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), matFundo));
  const camOrto = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);

  const scene = new THREE.Scene();
  if (!DEBUG) {
    scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new THREE.RoomEnvironment(), 0.04).texture;
    const chave = new THREE.DirectionalLight(0xffffff, 0.8); chave.position.set(3, 4, 6);
    const borda = new THREE.DirectionalLight(0x8FB4FF, 0.6); borda.position.set(-4, -2, -3);
    scene.add(chave, borda, new THREE.AmbientLight(0xffffff, 0.3));
  }
  const camera = new THREE.PerspectiveCamera(36, W / H, 0.05, 100);

  // ---------- recipiente: arestas finas (cilindros), faces quase transparentes; xl..xr varia com o pistão ----------
  const matAresta = new THREE.MeshBasicMaterial({ color: COR.geo, transparent: true, opacity: 0.9 });
  const matGhost = new THREE.MeshBasicMaterial({ color: COR.geo, transparent: true, opacity: 0 });
  const matFace = new THREE.MeshBasicMaterial({ color: COR.gelo, transparent: true, opacity: 0.03, side: THREE.DoubleSide, depthWrite: false });
  const cilG = new THREE.CylinderGeometry(0.014, 0.014, 1, 6);
  function arestas(mat) { const a = []; for (let i = 0; i < 12; i++) { const m = new THREE.Mesh(cilG, mat); scene.add(m); a.push(m); } return a; }
  function poeArestas(a, xl, xr) {                 // 4 arestas por eixo
    const cx = (xl + xr) / 2, lx = xr - xl;
    for (let i = 0; i < 12; i++) {
      const eixo = i >> 2, k = i & 3, u = (k & 1) ? 1 : -1, v = (k & 2) ? 1 : -1, m = a[i];
      m.rotation.set(0, 0, 0);
      if (eixo === 0) { m.scale.set(1, lx, 1); m.rotation.z = PI / 2; m.position.set(cx, u * WALL, v * WALL); }
      else if (eixo === 1) { m.scale.set(1, 2 * WALL, 1); m.position.set(u > 0 ? xr : xl, 0, v * WALL); }
      else { m.scale.set(1, 2 * WALL, 1); m.rotation.x = PI / 2; m.position.set(u > 0 ? xr : xl, v * WALL, 0); }
    }
  }
  const aresA = arestas(matAresta), aresG = arestas(matGhost);
  const face = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), matFace); scene.add(face);

  // pistão: placa + haste (só no C07)
  const matPist = new THREE.MeshStandardMaterial({ color: 0x5B74A0, metalness: 0.3, roughness: 0.45, transparent: true, opacity: 0.9 });
  const placa = new THREE.Mesh(new THREE.BoxGeometry(0.08, 2 * WALL + 0.04, 2 * WALL + 0.04), matPist);
  const haste = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.4, 12), matPist); haste.rotation.z = PI / 2;
  scene.add(placa, haste);

  // parede +x: pisca nas batidas; brilho local na batida da acompanhada
  const matFlash = new THREE.MeshBasicMaterial({ color: COR.gelo, transparent: true, opacity: 0, side: THREE.DoubleSide, depthWrite: false });
  const parede = new THREE.Mesh(new THREE.PlaneGeometry(2 * WALL, 2 * WALL), matFlash); parede.rotation.y = PI / 2; scene.add(parede);
  const matGlow = new THREE.MeshBasicMaterial({ color: 0xE8F4FF, transparent: true, opacity: 0, depthWrite: false });
  const glow = new THREE.Mesh(new THREE.CircleGeometry(0.2, 32), matGlow); glow.rotation.y = PI / 2; scene.add(glow);

  // ladrilho A (face da parede) e preenchimento V (o volume): translúcidos, cor de geometria
  const matTile = new THREE.MeshBasicMaterial({ color: COR.geo, transparent: true, opacity: 0, side: THREE.DoubleSide, depthWrite: false });
  const tile = new THREE.Mesh(new THREE.PlaneGeometry(2 * WALL, 2 * WALL), matTile); tile.rotation.y = PI / 2; scene.add(tile);
  const matFill = new THREE.MeshBasicMaterial({ color: COR.geo, transparent: true, opacity: 0, depthWrite: false });
  const fillBox = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), matFill); scene.add(fillBox);

  // ---------- balão do hook: membrana de borracha (fresnel + brilho), centro tal que a superfície toca a parede no ladrilho ----------
  const RB = 1.55, ESCY = 1.1, XR0 = 1 + R, PCY0 = 0.1, PCZ0 = -0.1;
  const uA = { value: 1 };
  const matBal = new THREE.ShaderMaterial({
    uniforms: { uA }, transparent: true, side: THREE.DoubleSide, depthWrite: false,
    vertexShader: 'varying vec3 vN; varying vec3 vV; void main(){ vec4 mv = modelViewMatrix * vec4(position, 1.0); vN = normalize(normalMatrix * normal); vV = normalize(-mv.xyz); gl_Position = projectionMatrix * mv; }',
    fragmentShader: `varying vec3 vN; varying vec3 vV; uniform float uA;
      void main(){ vec3 N = normalize(vN), V = normalize(vV); if (!gl_FrontFacing) N = -N;
        float f = pow(1.0 - abs(dot(N, V)), 2.2);
        vec3 col = mix(vec3(0.16, 0.36, 0.95), vec3(0.62, 0.84, 1.0), f);
        vec3 L = normalize(vec3(0.4, 0.8, 0.6)); float sp = pow(max(dot(reflect(-L, N), V), 0.0), 36.0);
        vec3 L2 = normalize(vec3(-0.7, 0.2, 0.5)); float sp2 = pow(max(dot(reflect(-L2, N), V), 0.0), 18.0) * 0.35;
        col += vec3(sp + sp2);
        gl_FragColor = vec4(col, clamp((0.11 + 0.72 * f + 0.55 * (sp + sp2)) * uA, 0.0, 1.0)); }`,
  });
  const balao = new THREE.Mesh(new THREE.SphereGeometry(RB, 64, 48), matBal);
  balao.scale.set(1, ESCY, 1); balao.position.set(XR0 - RB, PCY0, PCZ0); scene.add(balao);
  const matNo = new THREE.MeshStandardMaterial({ color: 0x2F63E8, metalness: 0.1, roughness: 0.35, transparent: true, opacity: 1 });
  const no = new THREE.Group();
  const cone = new THREE.Mesh(new THREE.ConeGeometry(0.16, 0.26, 24), matNo); cone.rotation.x = PI; cone.position.y = -0.04;
  const anel = new THREE.Mesh(new THREE.TorusGeometry(0.075, 0.035, 12, 24), matNo); anel.rotation.x = PI / 2; anel.position.y = -0.2;
  no.add(cone, anel); no.position.set(XR0 - RB, PCY0 - RB * ESCY - 0.02, PCZ0); scene.add(no);

  // ---------- moléculas ----------
  const geoEsf = new THREE.SphereGeometry(R, 22, 16);
  const matEsf = DEBUG ? new THREE.MeshBasicMaterial({ color: 0xff00ff })
    : new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 0.45, roughness: 0.32, envMapIntensity: 0.55, emissive: 0x16253f, emissiveIntensity: 0.35 });
  const esf = new THREE.InstancedMesh(geoEsf, matEsf, N);
  esf.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
  for (let i = 0; i < N; i++) esf.setColorAt(i, new THREE.Color(COR.aco));
  scene.add(esf);
  const ring = new THREE.Mesh(new THREE.RingGeometry(0.15, 0.178, 48), new THREE.MeshBasicMaterial({ color: 0xE6F2FF, transparent: true, opacity: 0, side: THREE.DoubleSide, depthTest: false }));
  ring.renderOrder = 5; scene.add(ring);
  const cAco = new THREE.Color(COR.aco), cAcomp = new THREE.Color(COR.acomp), cFundo = new THREE.Color(COR.fundo), tmpC = new THREE.Color();

  // hook: coluna de esferas (ilustrativa) que bate num patch quadrado da parede, cada vez mais rápido
  const HK = TL.hook, NH = HK.y.length, RH = 0.018, PCY = 0.1, PCZ = -0.1;
  const esfH = new THREE.InstancedMesh(new THREE.SphereGeometry(RH, 18, 14), matEsf, NH);     // mesmo material das moléculas
  esfH.instanceMatrix.setUsage(THREE.DynamicDrawUsage); for (let i = 0; i < NH; i++) esfH.setColorAt(i, new THREE.Color(0xA9BFE0)); scene.add(esfH);
  const matPatch = new THREE.MeshBasicMaterial({ color: 0xE8F4FF, transparent: true, opacity: 0, depthWrite: false });
  const patch = new THREE.Mesh(new THREE.PlaneGeometry(2 * HK.patch, 2 * HK.patch), matPatch); patch.rotation.y = PI / 2; scene.add(patch);
  const matBorda = new THREE.MeshBasicMaterial({ color: 0x9CC7FF, transparent: true, opacity: 0 });
  const bordaP = []; for (let i = 0; i < 4; i++) { const m = new THREE.Mesh(new THREE.CylinderGeometry(0.0035, 0.0035, 2 * HK.patch, 6), matBorda); scene.add(m); bordaP.push(m); }

  const dummy = new THREE.Object3D(), S0 = TL.s0, SP = TL.sp;
  function estado(i, f, tau, Lx, Gx) {
    const p = [], sg = [];
    const sx = S0[i][0] + SP[i][0] * Gx;
    p.push(-1 + Lx * tri(sx) / 2); sg.push(mod4(sx) < 2 ? 1 : -1);
    for (let k = 1; k < 3; k++) { const s = S0[i][k] + SP[i][k] * tau; p.push(-1 + tri(s)); sg.push(mod4(s) < 2 ? 1 : -1); }
    return { p, sg };
  }
  function chaves(f) {
    const t = f / FPS, Kc = TL.camera, out = {};
    let a = Kc[0], b = Kc[0], u = 0;
    if (t >= Kc[Kc.length - 1].t) { a = b = Kc[Kc.length - 1]; }
    else for (let i = 0; i < Kc.length - 1; i++) if (t <= Kc[i + 1].t) { a = Kc[i]; b = Kc[i + 1]; u = t <= a.t ? 0 : suave((t - a.t) / (b.t - a.t)); break; }
    for (const k of Object.keys(a)) if (k !== 't') out[k] = a[k] + (b[k] - a[k]) * u;
    return out;
  }
  let ultimo = { proj: null };
  function projeta(v) { const p = v.clone().project(camera); return [(p.x + 1) / 2 * W, (1 - p.y) / 2 * H]; }

  window.setFrame = function (f) {
    const K = chaves(f), tau = TL.tau[f], Lx = TL.Lx[f], Gx = TL.Gx[f], tauH = TL.tauH[f], gh = TL.ghost[f];
    const xl = -1 - R, xr = -1 + Lx + R;
    const az = K.az * PI / 180, el = K.el * PI / 180;
    const po = new THREE.Vector3(K.cx + K.D * Math.sin(az) * Math.cos(el), K.D * Math.sin(el), K.D * Math.cos(az) * Math.cos(el));
    const pe = new THREE.Vector3(K.px, K.py, K.pz), lo = new THREE.Vector3(K.cx, 0, 0), le = new THREE.Vector3(K.lx, K.ly, K.lz);
    camera.fov = K.fov; camera.aspect = W / H;
    camera.position.copy(po.lerp(pe, K.mix)); camera.up.set(0, 1, 0); camera.lookAt(lo.lerp(le, K.mix));
    camera.setViewOffset(W, H, 0, K.dy * H, W, H);
    camera.updateProjectionMatrix(); camera.updateMatrixWorld();

    const op = K.op, vis = DEBUG ? 0 : 1;
    const voo = 1 - 4 * K.mix * (1 - K.mix);        // some as arestas durante o voo da câmera do hook
    matAresta.opacity = 0.9 * op * vis * voo; matGhost.opacity = 0.4 * gh * op * vis; matFace.opacity = 0.03 * op * vis * voo;
    poeArestas(aresA, xl, xr); poeArestas(aresG, xl, -1 + 2 + R);
    aresA.forEach(m => m.visible = !DEBUG); aresG.forEach(m => m.visible = !DEBUG && gh > 0.01);
    face.visible = !DEBUG; face.scale.set(xr - xl, 2 * WALL, 2 * WALL); face.position.set((xl + xr) / 2, 0, 0);
    const pv = K.pist * vis;
    placa.visible = haste.visible = pv > 0.01; matPist.opacity = 0.9 * pv;
    placa.position.set(xr + 0.04, 0, 0); haste.position.set(xr + 0.08 + 0.2, 0, 0);
    parede.position.set(xr + 0.002, 0, 0);
    uA.value = DEBUG ? 0 : TL.bal[f]; balao.visible = no.visible = uA.value > 0.01; matNo.opacity = uA.value;
    matTile.opacity = DEBUG ? 0 : 0.38 * TL.tile[f] * op; tile.visible = matTile.opacity > 0.005; tile.position.set(xr + 0.006, 0, 0);
    matFill.opacity = DEBUG ? 0 : 0.2 * TL.fill[f] * op; fillBox.visible = matFill.opacity > 0.005; fillBox.scale.set(xr - xl, 2 * WALL, 2 * WALL); fillBox.position.set((xl + xr) / 2, 0, 0);

    let flash = 0;
    const tc = 0.14, molK = clamp(TL.mv[f], 0.0001, 1), fadeF = TL.fade[f], alfaArr = new Array(N);
    for (let i = 0; i < N; i++) {
      const e = estado(i, f, tau, Lx, Gx);
      dummy.position.set(e.p[0], e.p[1], e.p[2]); dummy.scale.setScalar(DEBUG && i > 0 || molK < 0.02 ? 0.0001 : 1); dummy.updateMatrix(); esf.setMatrixAt(i, dummy.matrix);
      const ehAc = i === 0, mixA = ehAc ? clamp(Math.max((1 - op) * 0.95, (1 - molK) * 0.95), 0, 0.95) : clamp(Math.max((1 - op) * 0.95, fadeF * 0.9, (1 - molK) * 0.95), 0, 0.95);
      tmpC.copy(ehAc ? cAcomp : cAco).lerp(cFundo, mixA); esf.setColorAt(i, tmpC); alfaArr[i] = molK < 0.02 ? 0 : 1 - mixA;
      const age = mod4(S0[i][0] + SP[i][0] * Gx - 2) / SP[i][0];
      flash += Math.exp(-age / tc);
    }
    esf.instanceMatrix.needsUpdate = true; esf.instanceColor.needsUpdate = true;
    matFlash.opacity = DEBUG ? 0 : op * clamp(0.015 + 0.06 * flash, 0, 0.3) * molK;
    const e0 = estado(0, f, tau, Lx, Gx), pos0 = new THREE.Vector3(...e0.p);
    ring.position.copy(pos0); ring.quaternion.copy(camera.quaternion); ring.material.opacity = DEBUG ? 0 : 0.95 * K.ring * op;
    const age0 = mod4(S0[0][0] + SP[0][0] * Gx - 2) / SP[0][0];
    const tH = tau - age0 * Lx / 2, eH = estado(0, f, tH, Lx, Gx);
    const ph = new THREE.Vector3(xr + 0.003, eH.p[1], eH.p[2]);
    glow.position.copy(ph); matGlow.opacity = DEBUG ? 0 : op * 0.85 * Math.exp(-age0 / 0.11) * K.ring;

    // hook
    const hv = DEBUG ? 0 : TL.hv[f], wx = xr - RH - 0.01;
    esfH.visible = hv > 0.01; patch.visible = bordaP[0].visible = hv > 0.01;
    let fl = 0;
    for (let i = 0; i < NH; i++) {
      const s = HK.s0[i] + HK.sp[i] * tauH, x = HK.xmin + (wx - HK.xmin) * tri(s) / 2;
      dummy.position.set(x, PCY + HK.y[i], PCZ + HK.z[i]); dummy.scale.setScalar(hv < 0.02 ? 0.0001 : 1); dummy.updateMatrix(); esfH.setMatrixAt(i, dummy.matrix); tmpC.set(0xA9BFE0).lerp(cFundo, (1 - hv) * 0.95); esfH.setColorAt(i, tmpC);
      if (Math.abs(HK.y[i]) < HK.patch && Math.abs(HK.z[i]) < HK.patch) fl += Math.exp(-(mod4(s - 2) / HK.sp[i]) / 0.05);
    }
    esfH.instanceMatrix.needsUpdate = true; esfH.instanceColor.needsUpdate = true;
    patch.position.set(xr + 0.004, PCY, PCZ); matPatch.opacity = hv * clamp(0.12 + 0.55 * fl, 0, 0.9); matBorda.opacity = hv * 0.9;
    const P = HK.patch;
    [[0, P, 0], [0, -P, 0], [P, 0, 1], [-P, 0, 1]].forEach((q, i) => { const m = bordaP[i]; m.rotation.set(0, 0, 0); m.position.set(xr + 0.005, PCY + (q[2] ? 0 : q[1]), PCZ + (q[2] ? q[0] : 0)); if (q[2]) m.rotation.x = 0; else m.rotation.x = PI / 2; });

    renderer.clear(); renderer.render(cenaFundo, camOrto); renderer.clearDepth(); renderer.render(scene, camera);

    // projeções (px no quadro W×H) para o Manim
    const k = 0.3, r2 = a => a.map(x => Math.round(x * 100) / 100);
    const vv = [e0.sg[0] * SP[0][0], e0.sg[1] * SP[0][1], e0.sg[2] * SP[0][2]];
    const tip = d => projeta(pos0.clone().add(new THREE.Vector3(d[0] * k, d[1] * k, d[2] * k)));
    const dir = new THREE.Vector3(1, 0, 0).applyQuaternion(camera.quaternion).multiplyScalar(R);
    const pm = projeta(pos0), pr = projeta(pos0.clone().add(dir));
    const cantos = (a, b) => { const o = []; for (let i = 0; i < 8; i++) o.push(r2(projeta(new THREE.Vector3((i & 1) ? b : a, (i & 2) ? WALL : -WALL, (i & 4) ? WALL : -WALL)))); return o; };
    ultimo.proj = {
      m: r2(pm), r: Math.round(Math.hypot(pr[0] - pm[0], pr[1] - pm[1]) * 100) / 100,
      tx: r2(tip([vv[0], 0, 0])), ty: r2(tip([0, vv[1], 0])), tz: r2(tip([0, 0, vv[2]])), tv: r2(tip(vv)),
      v: vv, parede: r2(projeta(ph)), cA: cantos(xl, xr), cG: cantos(xl, 1 + R), age: Math.round(age0 * 1000) / 1000,
      todas: window.AUDIT ? Array.from({ length: N }, (_, i) => { const e = estado(i, f, tau, Lx, Gx), q = new THREE.Vector3(e.p[0], e.p[1], e.p[2]), a = projeta(q), b = projeta(q.clone().add(dir)); return [...r2(a), Math.round(Math.hypot(b[0] - a[0], b[1] - a[1]) * 100) / 100, Math.round(alfaArr[i] * 100) / 100]; }) : null,
      wc: r2(projeta(new THREE.Vector3(xr, 0, 0))), bc: r2(projeta(new THREE.Vector3((xl + xr) / 2, 0, 0))),
      patch: [r2(projeta(new THREE.Vector3(xr, PCY + P, PCZ - P))), r2(projeta(new THREE.Vector3(xr, PCY - P, PCZ + P)))],
    };
  };
  window.getProj = () => ultimo.proj;
  window.cenaPronta = true;
})();
