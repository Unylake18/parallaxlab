// T7: esferas de aço ligadas por molas (vista 'frente', plano y = 0) e disco sobre gelo com binário (vista 'topo').
// Estado: {esf: [[x, z, vis, brilho], ...], molas: [[i, j, vis, brilho], ...], piso: 0|1,
//          disco: {vis, x, y, ang} | null, cam}
// Posições calculadas no Manim (sec_t7.py). brilho 0–1 acende a mola (azul-claro) ou a esfera.
(function () {
  const B = B3D, T3 = THREE, PI = Math.PI, R = 0.45;
  const AZUL = new T3.Color(0x5AA2FF), PRETO = new T3.Color(0x000000);
  const piso = B.chao(0x080C18);
  { // pedrinhas no chão: mostram a deriva do conjunto quando a câmera acompanha o centro
    let s = 9; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    const g = new T3.IcosahedronGeometry(1, 0), m = B.mat(0x2A3140, 0.1, 0.9, 0.25, { flatShading: true });
    const N = 500, inst = new T3.InstancedMesh(g, m, N), o = new T3.Object3D();
    for (let i = 0; i < N; i++) {
      const r = 0.025 + 0.05 * rnd() ** 2;
      o.position.set(-30 + 90 * rnd(), -2.5 + 9 * rnd(), r * 0.2); o.scale.set(r * 1.6, r, r * 0.5); o.updateMatrix(); inst.setMatrixAt(i, o.matrix);
    }
    piso.add(inst);
  }
  const esf = [0, 1, 2].map(() => {
    const m = new T3.Mesh(new T3.SphereGeometry(R, 40, 28), B.mat(0x8C97A8, 0.75, 0.3, 0.55));
    B.scene.add(m); return m;
  });
  const sombras = esf.map(() => B.sombra(R * 2.6, R * 1.0));
  const matMola = () => B.mat(0xB8C4DA, 0.6, 0.35, 0.5);
  const molas = [0, 1, 2].map(() => { const m = new T3.Mesh(new T3.BufferGeometry(), matMola()); B.scene.add(m); return m; });
  class Helice extends T3.Curve {
    constructor(a, b, n, r) { super(); this.a = a; this.b = b; this.n = n; this.r = r; }
    getPoint(t, alvo = new T3.Vector3()) {
      const d = this.b.clone().sub(this.a), L = d.length(); d.normalize();
      const u = new T3.Vector3(-d.z, 0, d.x), w = new T3.Vector3(0, 1, 0);       // perpendiculares no plano e fora dele
      const ang = 2 * PI * this.n * t, ext = Math.min(1, Math.min(t, 1 - t) / 0.08);  // pontas retas
      return alvo.copy(this.a).addScaledVector(d, L * t).addScaledVector(u, this.r * ext * Math.cos(ang)).addScaledVector(w, this.r * ext * Math.sin(ang));
    }
  }
  // disco sobre gelo (vista de cima): cilindro de aço com uma faixa radial para ver o giro
  const gGelo = new T3.Mesh(new T3.PlaneGeometry(7.0, 5.2), B.mat(0x15233B, 0.3, 0.3, 0.45)); gGelo.position.z = 0.004; B.scene.add(gGelo);
  const disco = new T3.Group();
  disco.add(new T3.Mesh(new T3.CylinderGeometry(1.35, 1.35, 0.2, 64).rotateX(PI / 2), B.mat(0x7A8696, 0.7, 0.32, 0.5)));
  const faixa = new T3.Mesh(new T3.BoxGeometry(2.4, 0.16, 0.03), B.mat(0xB8C4DA, 0.5, 0.35, 0.5)); faixa.position.z = 0.11; disco.add(faixa);
  const furo = new T3.Mesh(new T3.CylinderGeometry(0.12, 0.12, 0.04, 24).rotateX(PI / 2), B.mat(0x434C5A, 0.4, 0.5, 0.3)); furo.position.z = 0.115; disco.add(furo);
  disco.position.z = 0.1; B.scene.add(disco);

  function atualiza(e) {
    const top = e.cam && e.cam.modo === 'topo';
    piso.visible = !top && e.piso !== 0;
    gGelo.visible = !!(e.disco && e.disco.vis); disco.visible = gGelo.visible;
    if (disco.visible) { disco.position.x = e.disco.x || 0; disco.position.y = e.disco.y || 0; disco.rotation.z = e.disco.ang || 0; gGelo.position.x = e.disco.gx || 0; gGelo.position.y = e.disco.gy || 0; }
    esf.forEach((m, i) => { m.visible = false; sombras[i].visible = false; });
    (e.esf || []).forEach((s, i) => {
      const m = esf[i]; m.visible = !!s[2] && !top;
      m.position.set(s[0], 0, s[1]);
      m.material.emissive = PRETO.clone().lerp(new T3.Color(0x6E5A10).set(0x2A3F66), s[3] || 0);
      sombras[i].visible = m.visible; sombras[i].position.x = s[0];
      sombras[i].material.opacity = Math.max(0, 1 - (s[1] - R) / 1.5);
    });
    for (let k = 0; k < 3; k++) molas[k].visible = false;
    (e.molas || []).forEach((q, k) => {
      const [i, j, vis, br] = q, m = molas[k];
      if (!vis || top) return;
      const a = esf[i].position.clone(), b = esf[j].position.clone(), d = b.clone().sub(a).normalize();
      a.addScaledVector(d, R * 0.92); b.addScaledVector(d, -R * 0.92);
      m.geometry.dispose();
      m.geometry = new T3.TubeGeometry(new Helice(a, b, 7, 0.11), 220, 0.025, 8, false);
      m.material.color.set(0xB8C4DA).lerp(AZUL, br || 0);
      m.material.emissive = PRETO.clone().lerp(AZUL, 0.55 * (br || 0));
      m.visible = true;
    });
  }
  window.CENA = { atualiza };
  window.pontos3d = e => ({ esf: esf.map(m => B.projeta(m.position.toArray())), disco: B.projeta(disco.position.toArray()) });
  window.cenaPronta = true;
})();
