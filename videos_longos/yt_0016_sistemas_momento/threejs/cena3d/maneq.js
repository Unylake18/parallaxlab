// Manequim articulado do hook do yt_0015 (geometria copiada de assets_unidade/manequim/muro_yt0015.js), sobre gelo ou chão.
// Estado (a pose é calculada no Manim, sec_manequim.py):
//   {hx, hz: quadril; pes: [[ax, az, fi], [ax, az, fi]] tornozelos (x, z) e ângulo do pé; lam: tronco; cab: cabeça;
//    bracos: [[abd, flex, cot], [abd, flex, cot]] (lado +y, lado −y); esp: −1 vira para −x;
//    bola: [x, z] | 'maos' | null; rifle: {on, ang} (na mão; ang a partir da horizontal); bala: s (m além da boca) | null;
//    chao: 'gelo' | 'terra'; cam}
// pontos3d: peito, mãos, boca do cano, bala, pés e topo da cabeça (px).
(function () {
  const B = B3D, T3 = THREE, PI = Math.PI;
  const L1 = 0.46, L2 = 0.46, HIPW = 0.095;
  const clamp = B.clamp;
  const mAco = B.mat(0x7A8696, 0.4, 0.45, 0.28), mJunta = B.mat(0xB8C4DA, 0.4, 0.4, 0.3);
  B.scene.fog = new T3.Fog(0x0A1432, 20, 40);
  window.aposCamera = D => { B.scene.fog.near = D + 2.5; B.scene.fog.far = D + 16; };
  const terra = B.chao(0x080C18);
  // gelo: lâmina azulada, brilho especular, riscos finos
  const texGelo = (() => {
    const c = document.createElement('canvas'); c.width = 512; c.height = 128; const g = c.getContext('2d');
    g.fillStyle = '#6f87ad'; g.fillRect(0, 0, 512, 128);
    let s = 3; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    g.strokeStyle = 'rgba(220,235,255,0.35)'; g.lineWidth = 1;
    for (let i = 0; i < 70; i++) { const x = 512 * rnd(), y = 128 * rnd(); g.beginPath(); g.moveTo(x, y); g.lineTo(x + 30 + 80 * rnd(), y + (rnd() - 0.5) * 12); g.stroke(); }
    const t = new T3.CanvasTexture(c); t.wrapS = t.wrapT = T3.RepeatWrapping; t.repeat.set(12, 2); return t;
  })();
  const gelo = new T3.Mesh(new T3.PlaneGeometry(200, 22), B.esmaece(B.mat(0x1C2E4C, 0.1, 0.6, 0.22, { map: texGelo }), { fa: 0.0, fb: 0.7 }));
  gelo.position.set(0, -1, 0.006); B.scene.add(gelo);

  function lathe(perfil, seg = 28) {
    const g = new T3.LatheGeometry(perfil.map(p => new T3.Vector2(Math.max(p[0], 1e-4), p[1])), seg);
    g.rotateX(PI / 2); g.computeVertexNormals(); return g;
  }
  function capsula(rA, rB, len, cap = 0.75) {
    const p = [];
    for (let i = 0; i <= 6; i++) { const a = -PI / 2 + (PI / 2) * i / 6; p.push([rB * Math.cos(a), -len + cap * rB * Math.sin(a)]); }
    for (let i = 0; i <= 6; i++) { const a = (PI / 2) * i / 6; p.push([rA * Math.cos(a), cap * rA * Math.sin(a)]); }
    return lathe(p);
  }
  function barril(perfil, prof) { const g = lathe(perfil); g.scale(prof, 1, 1); return g; }
  const esfera = r => new T3.SphereGeometry(r, 24, 16);
  const malha = (g, m, x = 0, y = 0, z = 0) => { const o = new T3.Mesh(g, m); o.position.set(x, y, z); return o; };

  function Manequim() {
    const raiz = new T3.Group();
    raiz.add(malha(barril([[0.001, -0.07], [0.115, -0.05], [0.15, 0.02], [0.14, 0.09], [0.11, 0.13], [0.001, 0.135]], 0.62), mAco));
    const pernas = [];
    for (const lado of [1, -1]) {
      const quadril = new T3.Group(); quadril.position.set(0, lado * HIPW, 0); raiz.add(quadril);
      quadril.add(malha(esfera(0.07), mJunta)); quadril.add(malha(capsula(0.075, 0.052, L1), mAco));
      const joelho = new T3.Group(); joelho.position.z = -L1; quadril.add(joelho);
      joelho.add(malha(esfera(0.052), mJunta)); joelho.add(malha(capsula(0.052, 0.036, L2), mAco));
      const tornozelo = new T3.Group(); tornozelo.position.z = -L2; joelho.add(tornozelo);
      tornozelo.add(malha(esfera(0.037), mJunta));
      const gp = capsula(0.042, 0.036, 0.19, 0.9); gp.rotateY(-PI / 2); gp.scale(1, 1.15, 0.85); gp.translate(-0.045, 0, -0.05);
      tornozelo.add(malha(gp, mAco));
      pernas.push({ quadril, joelho, tornozelo, lado });
    }
    const lombar = new T3.Group(); lombar.position.z = 0.1; raiz.add(lombar);
    lombar.add(malha(esfera(0.07), mJunta));
    lombar.add(malha(barril([[0.001, 0.02], [0.12, 0.05], [0.15, 0.16], [0.175, 0.28], [0.16, 0.34], [0.09, 0.375], [0.001, 0.38]], 0.6), mAco));
    const cabeca = new T3.Group(); cabeca.position.z = 0.385; lombar.add(cabeca);
    cabeca.add(malha(new T3.CylinderGeometry(0.035, 0.042, 0.1, 16).rotateX(PI / 2), mAco, 0, 0, 0.045));
    cabeca.add(malha(esfera(0.034), mJunta));
    const cr = malha(esfera(0.1), mAco, 0.012, 0, 0.165); cr.scale.set(1.0, 0.8, 1.15); cabeca.add(cr);
    const bracos = [];
    for (const lado of [1, -1]) {
      const ombro = new T3.Group(); ombro.position.set(0, lado * 0.19, 0.33); lombar.add(ombro);
      ombro.add(malha(esfera(0.055), mJunta)); ombro.add(malha(capsula(0.047, 0.036, 0.29), mAco));
      const cotovelo = new T3.Group(); cotovelo.position.z = -0.29; ombro.add(cotovelo);
      cotovelo.add(malha(esfera(0.037), mJunta)); cotovelo.add(malha(capsula(0.036, 0.028, 0.25), mAco));
      const punho = new T3.Group(); punho.position.z = -0.25; cotovelo.add(punho);
      punho.add(malha(esfera(0.026), mJunta));
      const mao = malha(esfera(0.05), mAco, 0.0, 0, -0.06); mao.scale.set(0.55, 0.38, 1.0); punho.add(mao);
      const ponta = new T3.Object3D(); ponta.position.z = -0.07; punho.add(ponta);
      bracos.push({ ombro, cotovelo, punho, ponta, lado });
    }
    return { raiz, pernas, lombar, cabeca, bracos, peito: (() => { const o = new T3.Object3D(); o.position.set(0.16, 0, 0.25); lombar.add(o); return o; })() };
  }
  const g = new T3.Group(); B.scene.add(g);
  const m = Manequim(); g.add(m.raiz);
  const sombra = B.sombra(0.9, 0.35); B.scene.remove(sombra); sombra.position.z = 0.01; g.add(sombra);

  // bola e rifle
  const bola = malha(esfera(0.11), B.mat(0xB8C4DA, 0.35, 0.4, 0.4, { transparent: true })); B.scene.add(bola);   // bola_op: fade na borda do PALCO
  const sBola = B.sombra(0.3, 0.12);
  const rifle = new T3.Group();
  {
    const mR = B.mat(0x5A6372, 0.5, 0.35, 0.35), mC = B.mat(0x434C5A, 0.2, 0.6, 0.25);
    const cano = malha(new T3.CylinderGeometry(0.014, 0.016, 0.78, 12), mR); cano.rotation.z = PI / 2; cano.position.x = 0.36; rifle.add(cano);
    rifle.add(malha(new T3.BoxGeometry(0.34, 0.045, 0.08), mR, 0.02, 0, -0.01));
    const co = malha(new T3.BoxGeometry(0.36, 0.04, 0.1), mC, -0.3, 0, -0.04); co.rotation.y = 0.12; rifle.add(co);
  }
  const boca = new T3.Object3D(); boca.position.x = 0.76; rifle.add(boca);
  B.scene.add(rifle);
  const bala = malha(new T3.SphereGeometry(0.016, 10, 8).scale(1, 2.2, 1), B.mat(0xD8C39A, 0.8, 0.3, 0.6));
  B.scene.add(bala);

  // v7 (T8-7, Cyrano): placa de ferro, ímã em ferradura (vermelho e prata) e a Lua 3D (relevo, terminador suave, luz própria)
  const placa = malha(new T3.BoxGeometry(1.66, 0.9, 0.06), B.mat(0x4E5664, 0.75, 0.42, 0.6)); B.scene.add(placa);
  const sPlaca = B.sombra(2.2, 1.3);
  const ima = new T3.Group();
  { const mV = B.mat(0xC8323C, 0.3, 0.42, 0.5), mP = B.mat(0xD4DCE6, 0.9, 0.22, 1.0);
    const u = new T3.Mesh(new T3.TorusGeometry(0.1, 0.04, 12, 28, PI), mV); u.rotation.x = PI / 2; u.rotation.z = 0; ima.add(u);
    for (const sx of [-1, 1]) { const l = malha(new T3.CylinderGeometry(0.04, 0.04, 0.08, 14).rotateX(PI / 2), mV, sx * 0.1, 0, -0.04); ima.add(l);
      const pt = malha(new T3.CylinderGeometry(0.041, 0.041, 0.05, 14).rotateX(PI / 2), mP, sx * 0.1, 0, -0.105); ima.add(pt); }
    }                                 // os polos para baixo (para a placa)
  B.scene.add(ima);
  const texLua = (() => {
    const c = document.createElement('canvas'); c.width = 1024; c.height = 512; const g = c.getContext('2d');
    g.fillStyle = '#b9bdc6'; g.fillRect(0, 0, 1024, 512);
    let sd = 5; const rnd = () => { sd = (sd * 16807) % 2147483647; return sd / 2147483647; };
    for (let i = 0; i < 9; i++) { const x = 1024 * rnd(), y = 120 + 280 * rnd(), r = 60 + 110 * rnd();
      const q = g.createRadialGradient(x, y, 0, x, y, r); q.addColorStop(0, 'rgba(110,116,128,0.75)'); q.addColorStop(1, 'rgba(110,116,128,0)');
      g.fillStyle = q; g.fillRect(x - r, y - r, 2 * r, 2 * r); }                                             // mares
    for (let i = 0; i < 260; i++) { const x = 1024 * rnd(), y = 512 * rnd(), r = 2 + 22 * rnd() ** 2.5;
      g.fillStyle = 'rgba(120,124,134,0.55)'; g.beginPath(); g.arc(x, y, r, 0, 2 * PI); g.fill();
      g.strokeStyle = 'rgba(225,228,235,0.45)'; g.lineWidth = Math.max(1, r * 0.18); g.beginPath(); g.arc(x - r * 0.15, y - r * 0.15, r, 0, 2 * PI); g.stroke(); }   // crateras
    return new T3.CanvasTexture(c);
  })();
  const lua = new T3.Mesh(new T3.SphereGeometry(1, 72, 48), new T3.ShaderMaterial({
    uniforms: { map: { value: texLua }, ldir: { value: new T3.Vector3(-0.9, 0.75, -0.2).normalize() }, op: { value: 1 } }, transparent: true,
    vertexShader: 'varying vec3 vN; varying vec2 vUv; void main(){ vN = normalize(mat3(modelMatrix) * normal); vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
    fragmentShader: 'uniform sampler2D map; uniform vec3 ldir; uniform float op; varying vec3 vN; varying vec2 vUv; void main(){ float d = dot(normalize(vN), ldir); float k = smoothstep(-0.06, 0.32, d); vec3 c = texture2D(map, vUv).rgb; gl_FragColor = vec4(c * (0.035 + 1.0 * k), op); }'
  }));
  lua.rotation.x = 0.4; B.scene.add(lua);

  function ik(hx, hz, ax, az) {
    const dx = ax - hx, dz = az - hz, d = Math.min(Math.hypot(dx, dz), 0.9995 * (L1 + L2));
    const fi = Math.atan2(dx, -dz), al = Math.acos(clamp((L1 * L1 + d * d - L2 * L2) / (2 * L1 * d), -1, 1));
    const tt = fi + al, kx = hx + L1 * Math.sin(tt), kz = hz - L1 * Math.cos(tt);
    return [tt, Math.atan2(ax - kx, -(az - kz))];
  }
  const v3 = () => new T3.Vector3();
  let ult = {};
  function atualiza(e) {
    const esp = e.esp || 1;
    g.scale.x = esp; g.position.x = 0;
    m.raiz.position.set(e.hx * esp, 0, e.hz);                     // dentro do grupo espelhado
    m.pernas.forEach((pe, i) => {
      const [ax, az, fi] = e.pes[i];
      const [tt, ts] = ik(e.hx * esp, e.hz, ax * esp, az);
      pe.quadril.rotation.y = -tt; pe.joelho.rotation.y = -(ts - tt); pe.tornozelo.rotation.y = (fi || 0) + ts;
    });
    m.lombar.rotation.y = e.lam || 0;
    m.cabeca.rotation.y = e.cab || 0;
    m.bracos.forEach((b, i) => { const [abd, flex, cot] = e.bracos[i]; b.ombro.rotation.set(b.lado * abd, -flex, 0); b.cotovelo.rotation.y = -cot; });
    sombra.position.x = e.hx * esp;
    g.updateMatrixWorld(true);
    gelo.visible = e.chao !== 'terra';
    const mao0 = m.bracos[0].ponta.getWorldPosition(v3()), mao1 = m.bracos[1].ponta.getWorldPosition(v3());
    // bola
    if (e.bola === 'maos') { bola.visible = true; bola.position.copy(mao0).add(mao1).multiplyScalar(0.5); bola.position.y = 0; bola.position.x += 0.05 * esp; }
    else if (e.bola) { bola.visible = true; bola.position.set(e.bola[0], 0, e.bola[1]); }
    else bola.visible = false;
    sBola.visible = bola.visible; sBola.position.x = bola.position.x;
    const bop = e.bola_op === undefined ? 1 : e.bola_op;
    bola.traverse(o => { if (o.material) o.material.opacity = bop; });
    sBola.material.opacity = bola.visible ? bop * clamp(1 - bola.position.z / 2, 0.15, 1) : 0;
    // rifle na mão (a coronha no ombro de trás, o cano para a frente)
    rifle.visible = !!(e.rifle && e.rifle.on);
    if (rifle.visible) {
      const ang = e.rifle.ang || 0;
      const c = mao0.clone().add(mao1).multiplyScalar(0.5);
      rifle.position.set(c.x, -0.02, c.z);
      rifle.quaternion.setFromUnitVectors(new T3.Vector3(1, 0, 0), new T3.Vector3(esp * Math.cos(ang), 0, Math.sin(ang)));
      rifle.updateMatrixWorld(true);
    }
    const pb = boca.getWorldPosition(v3());
    bala.visible = rifle.visible && e.bala !== null && e.bala !== undefined;
    if (bala.visible) {
      const ang = e.rifle.ang || 0, d = [Math.cos(ang) * esp, Math.sin(ang)];
      bala.position.set(pb.x + d[0] * e.bala, 0, pb.z + d[1] * e.bala);
      bala.quaternion.setFromUnitVectors(new T3.Vector3(0, 1, 0), new T3.Vector3(d[0], 0, d[1]));
    }
    // v7: Cyrano
    placa.visible = !!e.placa; sPlaca.visible = placa.visible;
    if (e.placa) { placa.position.set(e.placa.x, 0, e.placa.z - 0.03); sPlaca.position.set(e.placa.x, 0, 0.006); sPlaca.material.opacity = 0.85; }
    ima.visible = !!e.ima;
    if (e.ima) { const mh = e.ima.mao ? mao1 : mao0; ima.position.set(mh.x + (e.ima.dx || 0), mh.y, mh.z + 0.09 + (e.ima.dz || 0)); ima.rotation.y = e.ima.giro || 0; }
    lua.visible = !!e.lua;
    if (e.lua) { lua.position.set(e.lua[0], e.lua[1], e.lua[2]); lua.scale.setScalar(e.lua[3]); }
    ult = { mao0, mao1, pb, ima: ima.position.clone(), peito: m.peito.getWorldPosition(v3()), cab: m.cabeca.localToWorld(new T3.Vector3(0, 0, 0.3)),
      pe0: m.pernas[0].tornozelo.getWorldPosition(v3()), pe1: m.pernas[1].tornozelo.getWorldPosition(v3()) };
  }
  window.CENA = { atualiza };
  window.pontos3d = () => {
    const r = {};
    for (const [k, v] of Object.entries(ult)) r[k] = B.projeta([v.x, v.y, v.z]);
    r.bola = B.projeta(bola.position.toArray()); r.bala = B.projeta(bala.position.toArray());
    r.mundo = Object.fromEntries(Object.entries(ult).map(([k, v]) => [k, [v.x, v.y, v.z]]));
    return r;
  };
  window.cenaPronta = true;
})();
