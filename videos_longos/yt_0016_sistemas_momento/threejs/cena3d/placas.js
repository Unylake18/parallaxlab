// v7 (C-1): duas placas penduradas por fios finos (suspensão bifilar: deslocam sem girar) numa campânula de vácuo de vidro.
// Em cima a placa preta (absorve; esquenta: brilho laranja); embaixo o espelho (reflete o feixe de volta). Dois lasers do lado de
// fora; feixe LUZ com brilho volumétrico (camadas aditivas). As setas, os fótons e os rótulos ficam no Manim.
// Estado: {rows: [{y, piv: [x, z], th, quente, refl}], xem, feixe: 0–1, cam}   (unidades 3D = Manim na vista frontal)
(function () {
  const B = B3D, T3 = THREE, PI = Math.PI, L_FIO = 1.0, H_PL = 1.0, XPL = -1.35;
  B.luzLab();
  const piso = B.chao(); piso.position.z = -3.46;               // o chão do laboratório fica sob a base da campânula
  const vidro = B.mat(0xBFD4F0, 0.0, 0.04, 1.4, { transparent: true, opacity: 0.11, depthWrite: false, side: T3.DoubleSide });
  const jarra = new T3.Group();
  { const c = new T3.Mesh(new T3.CylinderGeometry(0.95, 0.95, 5.2, 64, 1, true).rotateX(PI / 2), vidro); c.position.set(XPL, 0, -0.7); jarra.add(c);
    const t = new T3.Mesh(new T3.SphereGeometry(0.95, 64, 24, 0, 2 * PI, 0, PI / 2).rotateX(PI / 2), vidro); t.scale.z = 0.35; t.position.set(XPL, 0, 1.9); jarra.add(t);
    for (const z of [-3.3, 1.9]) { const a = new T3.Mesh(new T3.TorusGeometry(0.95, 0.014, 8, 64), B.mat(0xDCE8FF, 0.2, 0.1, 1.2, { transparent: true, opacity: 0.5 }));
      a.position.set(XPL, 0, z); jarra.add(a); }
    const base = new T3.Mesh(new T3.CylinderGeometry(1.18, 1.25, 0.16, 64).rotateX(PI / 2), B.mat(0x5C6676, 0.85, 0.32, 0.8)); base.position.set(XPL, 0, -3.38); jarra.add(base);
    const tubo = new T3.Mesh(new T3.CylinderGeometry(0.06, 0.06, 1.2, 12).rotateZ(PI / 2), B.mat(0x3A414C, 0.5, 0.5, 0.4)); tubo.position.set(XPL + 1.6, 0.3, -3.36); jarra.add(tubo);
  }
  B.scene.add(jarra);
  const mA = B.mat(0x8A95A6, 0.8, 0.3, 0.8);
  // estrutura interna: dois postes atrás e as travessas de cada placa
  for (const dx of [-0.72, 0.72]) { const p = new T3.Mesh(new T3.CylinderGeometry(0.03, 0.03, 5.0, 10).rotateX(PI / 2), mA); p.position.set(XPL + dx, 0.45, -0.8); B.scene.add(p); }
  const travessas = [0, 1].map(() => { const t = new T3.Mesh(new T3.BoxGeometry(1.5, 0.06, 0.05), mA); B.scene.add(t); return t; });
  // placas e fios
  const mPreta = B.mat(0x0B0D12, 0.1, 0.75, 0.2, { emissive: new T3.Color(0x000000) });
  const mEsp = B.mat(0xF0F4FA, 0.9, 0.1, 2.2);
  const placas = [mPreta, mEsp].map(m => { const p = new T3.Mesh(new T3.BoxGeometry(0.2, 0.7, H_PL), m); B.scene.add(p); return p; });
  const brilhoPreta = new T3.Sprite(new T3.SpriteMaterial({ map: B.sprite(128, 0.6), color: 0xFF7A3D, transparent: true, opacity: 0, depthWrite: false, blending: T3.AdditiveBlending }));
  B.scene.add(brilhoPreta);
  const mFio = new T3.MeshBasicMaterial({ color: 0xB8C4DA });
  const fios = [0, 1].map(() => [-0.25, 0.25].map(() => { const f = new T3.Mesh(new T3.CylinderGeometry(0.006, 0.006, 1, 6), mFio); B.scene.add(f); return f; }));
  // lasers e feixes (núcleo + duas camadas de brilho aditivo)
  const lasers = [0, 1].map(() => { const g = new T3.Group();
    g.add(new T3.Mesh(new T3.BoxGeometry(0.62, 0.36, 0.42), B.mat(0x5A6372, 0.7, 0.36, 0.7)));
    const l = new T3.Mesh(new T3.CylinderGeometry(0.07, 0.07, 0.08, 16).rotateZ(PI / 2), B.mat(0xFFE9A8, 0.0, 0.3, 0.2, { emissive: new T3.Color(0xFFD25A) }));
    l.position.x = 0.33; g.add(l);
    const pe = new T3.Mesh(new T3.CylinderGeometry(0.035, 0.035, 1, 8), mA); pe.name = 'pe'; g.add(pe);
    B.scene.add(g); return g; });
  function camadas() {
    const g = new T3.Group();
    for (const [r, o, c, ad] of [[0.018, 1.0, 0xFFF4D0, false], [0.06, 0.32, 0xFFD25A, true], [0.16, 0.12, 0xFFD25A, true], [0.32, 0.05, 0xFFD25A, true]]) {
      const m = new T3.Mesh(new T3.CylinderGeometry(r, r, 1, 16, 1, true).rotateZ(PI / 2), new T3.MeshBasicMaterial({ color: c, transparent: true, opacity: o,
        depthWrite: false, blending: ad ? T3.AdditiveBlending : T3.NormalBlending }));
      m.userData.op = o; g.add(m);
    }
    B.scene.add(g); return g;
  }
  const feixes = [camadas(), camadas(), camadas()];      // ida (preta), ida (espelho), volta (espelho)
  function poeFeixe(f, x0, x1, z, op) {
    f.visible = op > 0.01 && x1 > x0; f.position.set((x0 + x1) / 2, 0, z); f.scale.set(x1 - x0, 1, 1);
    f.children.forEach(m => { m.material.opacity = m.userData.op * op; });
  }
  function atualiza(e) {
    const op = e.feixe === undefined ? 1 : e.feixe;
    e.rows.forEach((r, i) => {
      const [px, pz] = r.piv, th = r.th || 0;
      const tx = px + L_FIO * Math.sin(th), tz = pz - L_FIO * Math.cos(th);
      const p = placas[i]; p.position.set(tx, 0, tz - H_PL / 2);
      travessas[i].position.set(XPL, 0, pz + 0.03);
      fios[i].forEach((f, k) => { const y = k ? 0.25 : -0.25, a = new T3.Vector3(px, y, pz), b = new T3.Vector3(tx, y, tz), d = b.clone().sub(a);
        f.scale.set(1, d.length(), 1); f.position.copy(a.clone().add(b).multiplyScalar(0.5)); f.quaternion.setFromUnitVectors(new T3.Vector3(0, 1, 0), d.normalize()); });
      const ls = lasers[i]; ls.position.set(e.xem, 0, r.y); const pe = ls.children.find(o => o.name === 'pe');
      const h = r.y + 3.3; pe.scale.set(1, h, 1); pe.rotation.x = PI / 2; pe.position.set(-0.1, 0, -h / 2 - 0.18);
      const xf = tx - 0.1;
      poeFeixe(feixes[i], e.xem + 0.37, xf, r.y, op);
      if (r.refl) poeFeixe(feixes[2], e.xem + 0.37, xf, r.y - 0.22, 0.6 * op);
      if (!r.refl) { mPreta.emissive.setRGB(1.0 * r.quente, 0.42 * r.quente, 0.18 * r.quente);
        brilhoPreta.position.set(tx - 0.12, -0.2, r.y); const k = 0.6 + 1.6 * r.quente; brilhoPreta.scale.set(k, k, 1); brilhoPreta.material.opacity = 0.25 + 0.6 * r.quente; }
    });
  }
  window.CENA = { atualiza };
  window.pontos3d = e => { const r = {}; placas.forEach((p, i) => { r['pl' + i] = B.projeta(p.position.toArray()); }); r.em0 = B.projeta([e.xem + 0.37, 0, e.rows[0].y]); return r; };
  window.cenaPronta = true;
})();
