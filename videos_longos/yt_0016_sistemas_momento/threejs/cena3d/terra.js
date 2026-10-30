// v7 (T9-1/T9-2): bola de 1 kg presa num eletroímã no alto de um mastro (10 m na cota do Manim), cai sobre o chão com grade;
// no "bola mais Terra" a câmera se afasta (dolly-out) até o planeta (Terra estilizada: oceanos azul-escuros, continentes
// dessaturados, atmosfera fina). O chão some no afastamento; a fronteira e as setas ficam no Manim.
// Estado: {bz: centro da bola (z), bx, piso: 0–1, terra: 0–1, cam}   (a Terra tem o topo tangente ao chão em (bx, 0, 0))
(function () {
  const B = B3D, T3 = THREE, PI = Math.PI, RB = 0.3, RE = 60;
  B.luzLab();
  const piso = B.chao();
  const mPiso = piso.material;
  const bola = new T3.Mesh(new T3.SphereGeometry(RB, 40, 28), B.mat(0xB8C2D0, 0.8, 0.26, 0.85)); B.scene.add(bola);
  const sb = B.sombra(RB * 3, RB * 1.4);
  // mastro com braço e eletroímã (à direita da bola, longe da cota do Manim)
  const mastro = new T3.Group();
  const mA = B.mat(0x7F8A9A, 0.8, 0.35, 0.7), mE = B.mat(0x2E343D, 0.4, 0.5, 0.4);
  { const h = 5.0;
    const p = new T3.Mesh(new T3.CylinderGeometry(0.06, 0.08, h, 16).rotateX(PI / 2), mA); p.position.set(1.3, 0.2, h / 2); mastro.add(p);
    const b = new T3.Mesh(new T3.BoxGeometry(1.4, 0.1, 0.1), mA); b.position.set(0.65, 0.2, h - 0.05); mastro.add(b);
    const s = new T3.Mesh(new T3.BoxGeometry(0.08, 0.32, 0.08), mA); s.position.set(0, 0.05, h - 0.05); mastro.add(s);
    const ima = new T3.Mesh(new T3.CylinderGeometry(0.16, 0.16, 0.22, 24).rotateX(PI / 2), mE); ima.position.set(0, 0, h - 0.2); mastro.add(ima);
    const base = new T3.Mesh(new T3.CylinderGeometry(0.35, 0.4, 0.08, 24).rotateX(PI / 2), mA); base.position.set(1.3, 0.2, 0.04); mastro.add(base);
  }
  B.scene.add(mastro);
  // Terra estilizada: textura procedural (equirretangular) — oceanos azul-escuros, continentes dessaturados, calotas
  const texT = (() => {
    const W = 1024, H = 512, c = document.createElement('canvas'); c.width = W; c.height = H; const g = c.getContext('2d');
    const img = g.createImageData(W, H);
    let s = 7; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    const dir = () => { const u = 2 * rnd() - 1, t = 2 * PI * rnd(), q = Math.sqrt(1 - u * u); return [q * Math.cos(t), q * Math.sin(t), u]; };
    const blobs = [];                                         // continentes: grupos de calotas na esfera (sem distorção nos polos)
    for (let c = 0; c < 9; c++) { const d0 = dir(); for (let k = 0; k < 8; k++) {
      const d = d0.map(x => x + 0.45 * (rnd() - 0.5)), n = Math.hypot(...d); blobs.push([d[0] / n, d[1] / n, d[2] / n, 0.16 + 0.2 * rnd()]); } }
    const ruido = [...Array(10)].map(() => [...dir(), 3 + 9 * rnd(), 2 * PI * rnd()]);
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      const lo = x / W * 2 * PI, la = (0.5 - y / H) * PI, cl = Math.cos(la);
      const p = [cl * Math.cos(lo), cl * Math.sin(lo), Math.sin(la)];
      let v = -1;
      for (const [a, b2, c2, r] of blobs) { const ang = Math.acos(Math.min(1, a * p[0] + b2 * p[1] + c2 * p[2])); v = Math.max(v, (r - ang) / r); }
      for (const [a, b2, c2, f, ph] of ruido) v += 0.05 * Math.sin(f * (a * p[0] + b2 * p[1] + c2 * p[2]) + ph);
      const u = Math.min(1, Math.max(0, (v + 0.02) / 0.08)), q = u * u * (3 - 2 * u);          // borda suave da costa
      const k = Math.min(1, Math.max(0, v * 1.5)), ko = Math.max(0, Math.min(1, -v * 0.8));
      const r = (1 - q) * (12 - 5 * ko) + q * (48 - 10 * k), gg = (1 - q) * (32 - 10 * ko) + q * (56 - 8 * k), bb = (1 - q) * (68 - 18 * ko) + q * (58 - 6 * k);
      const i = 4 * (y * W + x); img.data[i] = r; img.data[i + 1] = gg; img.data[i + 2] = bb; img.data[i + 3] = 255;
    }
    g.putImageData(img, 0, 0);
    return new T3.CanvasTexture(c);
  })();
  const terra = new T3.Mesh(new T3.SphereGeometry(RE, 96, 64), B.mat(0xFFFFFF, 0.0, 0.75, 0.25, { map: texT, transparent: true }));
  terra.rotation.x = PI / 2 + 0.75; terra.rotation.y = 2.6; B.scene.add(terra);
  // atmosfera fina: casca um pouco maior, brilho na borda (fresnel)
  const atm = new T3.Mesh(new T3.SphereGeometry(RE * 1.035, 96, 64), new T3.ShaderMaterial({
    transparent: true, depthWrite: false, side: T3.BackSide, uniforms: { op: { value: 1 } },
    vertexShader: 'varying vec3 vN; varying vec3 vV; void main(){ vec4 mv = modelViewMatrix * vec4(position,1.0); vN = normalize(normalMatrix*normal); vV = normalize(-mv.xyz); gl_Position = projectionMatrix*mv; }',
    fragmentShader: 'uniform float op; varying vec3 vN; varying vec3 vV; void main(){ float f = pow(1.0 - abs(dot(vN, vV)), 3.0); gl_FragColor = vec4(0.35,0.75,1.0, 0.55*f*op); }'
  }));
  B.scene.add(atm);

  function atualiza(e) {
    const bx = e.bx || 0, pv = e.piso === undefined ? 1 : e.piso, tv = e.terra || 0;
    bola.position.set(bx, 0, e.bz); sb.position.set(bx, 0, 0.005);
    const alt = Math.max(0, e.bz - RB); sb.material.opacity = 0.8 * pv * Math.max(0.2, 1 - alt / 5); sb.scale.set(RB * 3 * (1 + alt / 6), RB * 1.4 * (1 + alt / 6), 1);
    mastro.position.set(bx, 0, 0);
    piso.visible = pv > 0.01; mPiso.opacity = pv; mastro.visible = pv > 0.01;
    mastro.traverse(o => { if (o.isMesh) { o.material.transparent = pv < 0.999; o.material.opacity = pv; } });
    terra.visible = tv > 0.01; atm.visible = terra.visible;
    terra.position.set(bx, 0, -RE); atm.position.copy(terra.position); terra.rotation.y = 2.6 + (e.rot || 0);   // v7: a Terra gira (palco vivo)
    terra.material.opacity = tv; atm.material.uniforms.op.value = tv;
  }
  window.CENA = { atualiza };
  window.pontos3d = e => ({ bola: B.projeta(bola.position.toArray()), terra: B.projeta([e.bx || 0, 0, -RE]), topo: B.projeta([e.bx || 0, 0, 0]) });
  window.cenaPronta = true;
})();
