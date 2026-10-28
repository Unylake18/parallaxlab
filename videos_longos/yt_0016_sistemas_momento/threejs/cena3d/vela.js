// Coda: vela solar refletora no espaço (estrelas), abrindo devagar; fótons chegando da esquerda e voltando.
// Estado: {abre: 0–1, ang: giro da vela em torno de z, fase: tempo dos fótons (s), x: posição da vela, vis_f: 0–1, cam}
(function () {
  const B = B3D, T3 = THREE, PI = Math.PI;
  B.ceu(true);
  B.luz.chave.position.set(-8, -3, 4); B.luz.chave.intensity = 1.7;
  const g = new T3.Group(); B.scene.add(g);
  // vela: plano fino espelhado, com leve ondulação
  const geo = new T3.PlaneGeometry(4, 4, 24, 24);
  { const p = geo.attributes.position; for (let i = 0; i < p.count; i++) { const x = p.getX(i), y = p.getY(i); p.setZ(i, 0.05 * Math.sin(1.7 * x) * Math.cos(1.3 * y)); } geo.computeVertexNormals(); }
  const vela = new T3.Mesh(geo, new T3.MeshStandardMaterial({ color: 0xD5DEEE, metalness: 1.0, roughness: 0.18, envMapIntensity: 1.1, side: T3.DoubleSide }));
  vela.rotation.y = PI / 2;                                // a face da vela olha para −x (para o Sol)
  g.add(vela);
  const mB = B.mat(0x7A8696, 0.6, 0.4, 0.4);
  const hastes = [0, 1].map(k => { const h = new T3.Mesh(new T3.CylinderGeometry(0.03, 0.03, 5.6, 8), mB); h.rotation.x = PI / 4 + k * PI / 2; g.add(h); return h; });
  const cubo = new T3.Mesh(new T3.BoxGeometry(0.35, 0.35, 0.35), B.mat(0x5A6372, 0.5, 0.4, 0.4)); g.add(cubo);
  // fótons
  const tex = B.sprite(64, 0.55), N = 46;
  const fot = [];
  let s = 17; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
  for (let i = 0; i < N; i++) {
    const sp = new T3.Sprite(new T3.SpriteMaterial({ map: tex, color: 0xFFE7A8, transparent: true, depthWrite: false }));
    sp.scale.set(0.13, 0.13, 1); B.scene.add(sp);
    fot.push({ sp, y: (rnd() - 0.5) * 3.2, z: (rnd() - 0.5) * 3.2, ph: rnd() });
  }
  function atualiza(e) {
    const a = 0.15 + 0.85 * (e.abre === undefined ? 1 : e.abre);
    vela.scale.set(a, a, 1); hastes.forEach(h => h.scale.set(1, a, 1));
    g.position.x = e.x || 0; g.rotation.z = e.ang || 0;
    const L = 9.0, v = 3.2, T = 2 * L / v;
    for (const f of fot) {
      const u = (((e.fase || 0) / T) + f.ph) % 1.0;      // 0–0,5 chegando; 0,5–1 voltando (reflete)
      const dentro = Math.abs(f.y) < 2 * a * 0.95 && Math.abs(f.z) < 2 * a * 0.95;
      const xs = g.position.x;
      let x = u < 0.5 ? xs - L * (1 - 2 * u) : (dentro ? xs - L * (2 * u - 1) : xs + L * (2 * u - 1));
      f.sp.position.set(x, f.y, f.z);
      f.sp.material.opacity = (e.vis_f === undefined ? 1 : e.vis_f) * Math.min(1, 4 * Math.min(u, 1 - u) + 0.1);
    }
  }
  window.CENA = { atualiza };
  window.pontos3d = () => ({ vela: B.projeta(g.position.toArray()) });
  window.cenaPronta = true;
})();
