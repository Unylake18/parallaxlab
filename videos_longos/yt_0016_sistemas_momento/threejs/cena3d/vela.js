// Coda: vela solar refletora no espaço (estrelas), abrindo devagar; fótons (riscos amarelos, v4) chegando da esquerda e voltando.
// Estado: {abre: 0–1, ang: giro da vela em torno de z, fase: tempo dos fótons (s), x: posição da vela, vis_f: 0–1, cam}
(function () {
  const B = B3D, T3 = THREE, PI = Math.PI;
  B.ceu(false);                                            // v7: as estrelas já estão no fundo da unidade
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
  // fótons (v4): riscos curtos amarelos (LUZ #FFD25A, núcleo #FFE9A8), alinhados com o movimento ao longo de x; voltam depois de bater
  const N = 46, gRisco = new T3.CylinderGeometry(0.018, 0.018, 0.42, 6), gHalo = new T3.CylinderGeometry(0.05, 0.05, 0.5, 8);
  const fot = [];
  let s = 17; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
  for (let i = 0; i < N; i++) {
    const sp = new T3.Group();
    const nucleo = new T3.Mesh(gRisco, new T3.MeshBasicMaterial({ color: 0xFFE9A8, transparent: true, depthWrite: false }));
    const halo = new T3.Mesh(gHalo, new T3.MeshBasicMaterial({ color: 0xFFD25A, transparent: true, opacity: 0.25, depthWrite: false }));
    sp.add(halo, nucleo); sp.rotation.z = PI / 2; B.scene.add(sp);
    sp.material = { set opacity(o) { nucleo.material.opacity = o; halo.material.opacity = 0.25 * o; } };
    fot.push({ sp, y: (rnd() - 0.5) * 3.2, z: (rnd() - 0.5) * 3.2, ph: rnd() });
  }
  function atualiza(e) {
    const a = 0.15 + 0.85 * (e.abre === undefined ? 1 : e.abre);
    vela.scale.set(a, a, 1); hastes.forEach(h => h.scale.set(1, a, 1));
    g.position.x = e.x || 0; g.rotation.z = e.ang || 0;
    const L = 9.0, v = 3.2, T = 2 * L / v;
    for (const f of fot) {
      const u = (((e.fase || 0) / T) + f.ph) % 1.0;      // 0–0,5 chegando; 0,5–1 voltando (reflete)
      // v6 (N5): a vela é um losango (hastes a 45°) e está girada em torno de z: o fóton bate no plano dela e volta (nunca a atravessa)
      const dentro = Math.abs(f.y) + Math.abs(f.z) < 2.8 * a * 0.92;
      const xs = g.position.x - f.y * Math.tan(e.ang || 0) - 0.24;
      let x = u < 0.5 ? xs - L * (1 - 2 * u) : (dentro ? xs - L * (2 * u - 1) : xs + 0.24 + L * (2 * u - 1));
      f.sp.position.set(x, f.y, f.z);
      f.sp.material.opacity = (e.vis_f === undefined ? 1 : e.vis_f) * Math.min(1, 4 * Math.min(u, 1 - u) + 0.1);
    }
  }
  window.CENA = { atualiza };
  window.pontos3d = () => ({ vela: B.projeta(g.position.toArray()) });
  window.cenaPronta = true;
})();
