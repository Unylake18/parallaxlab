// v7 (E8): rifle low-poly (coronha de madeira escura, cano e caixa de aço, luneta) num apoio frouxo (bipé com a forquilha solta
// na frente, descanso atrás). O rifle desliza para trás de verdade; a bala é um traço metálico; os gases são uma nuvem de
// partículas cinza-azulada que se expande e se dissipa (semente fixa). Câmera lateral.
// Estado: {xr: x da boca do cano (mundo), zb: altura do eixo do cano, tiros: [idade (s), ...] (o último é o corrente),
//          bala: x | null, nv: idade do destaque dos gases (E8-3) | null, wob: inclinação da forquilha (rad), cam}
(function () {
  const B = B3D, T3 = THREE, PI = Math.PI;
  B.luzLab();
  const piso = B.chao();
  const mMad = B.mat(0x2C1A11, 0.05, 0.55, 0.4, { flatShading: true }), mMadE = B.mat(0x22140D, 0.0, 0.66, 0.3, { flatShading: true });
  const mAco = B.mat(0x8C96A6, 0.85, 0.3, 0.9), mEsc = B.mat(0x30353D, 0.6, 0.42, 0.6), mLente = B.mat(0x1E3A6A, 0.2, 0.1, 1.2);
  function perfil(pts, prof, mat) {                      // polígono no plano xz extrudado em y (low-poly)
    const s = new T3.Shape(); s.moveTo(pts[0][0], pts[0][1]); pts.slice(1).forEach(p => s.lineTo(p[0], p[1]));
    const g = new T3.ExtrudeGeometry(s, { depth: prof, bevelEnabled: true, bevelThickness: 0.025, bevelSize: 0.02, bevelSegments: 1 });
    g.translate(0, 0, -prof / 2); g.rotateX(PI / 2);
    return new T3.Mesh(g, mat);
  }
  const cil = (r, L, mat, seg = 18) => { const m = new T3.Mesh(new T3.CylinderGeometry(r, r, L, seg).rotateZ(PI / 2), mat); return m; };
  const rifle = new T3.Group();
  rifle.add(perfil([[-4.97, 0.10], [-3.3, 0.05], [-2.95, -0.02], [-2.72, -0.02], [-2.72, -0.12], [-2.6, -0.52], [-2.82, -0.56],
    [-3.02, -0.2], [-4.97, -0.5]], 0.16, mMad));                                   // coronha com empunhadura
  rifle.add(perfil([[-2.55, -0.03], [-0.95, -0.03], [-0.9, -0.09], [-1.0, -0.17], [-2.55, -0.19]], 0.15, mMadE));   // telha
  { const bp = new T3.Mesh(new T3.BoxGeometry(0.06, 0.18, 0.62), mEsc); bp.position.set(-4.99, 0, -0.2); rifle.add(bp); }   // soleira
  { const cx = new T3.Mesh(new T3.BoxGeometry(0.95, 0.15, 0.2), mEsc); cx.position.set(-2.3, 0, 0.03); rifle.add(cx); }    // caixa da culatra
  { const c = cil(0.052, 1.95, mAco); c.position.set(-0.97, 0, 0.0); rifle.add(c); }                                        // cano
  { const c = cil(0.068, 0.2, mEsc); c.position.set(-0.1, 0, 0.0); rifle.add(c); }                                          // quebra-chamas
  { const c = cil(0.07, 1.25, mEsc, 20); c.position.set(-2.25, 0, 0.3); rifle.add(c);                                       // luneta
    for (const [x, r] of [[-2.92, 0.1], [-1.6, 0.11]]) { const b = cil(r, 0.18, mEsc, 20); b.position.set(x, 0, 0.3); rifle.add(b);
      const l = new T3.Mesh(new T3.CircleGeometry(r * 0.8, 20).rotateY(x > -2 ? PI / 2 : -PI / 2), mLente); l.position.set(x + (x > -2 ? 0.091 : -0.091), 0, 0.3); rifle.add(l); }
    for (const x of [-2.6, -1.95]) { const a = new T3.Mesh(new T3.BoxGeometry(0.08, 0.1, 0.2), mEsc); a.position.set(x, 0, 0.17); rifle.add(a); } }
  { const h = new T3.Mesh(new T3.CylinderGeometry(0.02, 0.02, 0.22, 8).rotateX(PI / 2), mAco); h.position.set(-2.05, 0.15, 0.05); rifle.add(h);
    const k = new T3.Mesh(new T3.SphereGeometry(0.04, 10, 8), mAco); k.position.set(-2.05, 0.26, 0.05); rifle.add(k); }   // ferrolho
  { const g = new T3.Mesh(new T3.TorusGeometry(0.11, 0.015, 6, 14, PI).rotateX(PI / 2), mEsc); g.rotation.z = 0; g.position.set(-2.55, 0, -0.13);
    g.rotation.x = 0; rifle.add(g); }                                                                                     // guarda-mato
  B.scene.add(rifle);
  // apoio frouxo: bipé com forquilha solta na frente (x = −2,82), descanso atrás (x = −5,48); ficam no chão, o rifle desliza
  const mA = B.mat(0x6E7888, 0.8, 0.36, 0.7);
  function forquilha() {
    const g = new T3.Group();
    for (const s of [-1, 1]) { const b = new T3.Mesh(new T3.BoxGeometry(0.05, 0.05, 0.22), mEsc); b.position.set(0, s * 0.09, 0.08); b.rotation.x = s * 0.35; g.add(b); }
    const base = new T3.Mesh(new T3.BoxGeometry(0.12, 0.24, 0.04), mEsc); base.position.z = -0.02; g.add(base);
    return g;
  }
  const bipe = new T3.Group(), yoke = forquilha(), desc = new T3.Group(), yoke2 = forquilha();
  bipe.add(yoke); desc.add(yoke2);
  const pernas = [], hastes = [];
  for (const s of [-1, 1]) { const p = new T3.Mesh(new T3.CylinderGeometry(0.035, 0.03, 1, 10), mA); bipe.add(p); pernas.push([p, s]); }
  { const h = new T3.Mesh(new T3.CylinderGeometry(0.05, 0.05, 1, 12), mA); desc.add(h); hastes.push(h);
    const b = new T3.Mesh(new T3.CylinderGeometry(0.26, 0.3, 0.06, 20).rotateX(PI / 2), mA); b.name = 'base'; desc.add(b); }
  B.scene.add(bipe, desc);
  const sombraR = B.sombra(5.6, 1.1), sbi = B.sombra(1.0, 1.4), sde = B.sombra(0.8, 0.8);
  // bala: traço metálico com rastro
  const bala = new T3.Group();
  { const c = new T3.Mesh(new T3.CylinderGeometry(0.028, 0.028, 0.14, 12).rotateZ(PI / 2), B.mat(0xC8A86A, 0.9, 0.25, 1.0)); bala.add(c);
    const p = new T3.Mesh(new T3.ConeGeometry(0.028, 0.06, 12).rotateZ(-PI / 2), B.mat(0xC8A86A, 0.9, 0.25, 1.0)); p.position.x = 0.1; bala.add(p);
    const cv = document.createElement('canvas'); cv.width = 256; cv.height = 8; const g = cv.getContext('2d');
    const lg = g.createLinearGradient(0, 0, 256, 0); lg.addColorStop(0, 'rgba(220,230,255,0)'); lg.addColorStop(1, 'rgba(235,240,255,0.85)');
    g.fillStyle = lg; g.fillRect(0, 0, 256, 8);
    const r = new T3.Mesh(new T3.PlaneGeometry(0.9, 0.035), new T3.MeshBasicMaterial({ map: new T3.CanvasTexture(cv), transparent: true, depthWrite: false }));
    r.rotation.x = PI / 2; r.position.x = -0.48; bala.add(r);
    const r2 = r.clone(); r2.rotation.x = 0; bala.add(r2); }
  B.scene.add(bala);
  const clarao = new T3.Sprite(new T3.SpriteMaterial({ map: B.sprite(128, 0.55), color: 0xFFD9A0, transparent: true, depthWrite: false, blending: T3.AdditiveBlending }));
  B.scene.add(clarao);
  // gases: partículas macias (sprites), determinísticas
  const txF = (() => {
    const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d');
    const r = g.createRadialGradient(64, 64, 0, 64, 64, 64);
    r.addColorStop(0, 'rgba(255,255,255,0.9)'); r.addColorStop(0.45, 'rgba(255,255,255,0.45)'); r.addColorStop(1, 'rgba(255,255,255,0)');
    g.fillStyle = r; g.fillRect(0, 0, 128, 128); return new T3.CanvasTexture(c);
  })();
  let sd = 77; const rnd = () => { sd = (sd * 16807) % 2147483647; return sd / 2147483647; };
  const NG = 64;
  const parts = [...Array(NG)].map(() => ({ dx: 0.2 + 1.9 * rnd() ** 0.8, dy: (rnd() - 0.5) * 1.2, dz: (rnd() - 0.5) * 0.9, tau: 0.25 + 0.5 * rnd(),
    r0: 0.12 + 0.16 * rnd(), sp: 0.5 + rnd(), ph: rnd() }));
  const nuvens = [0, 1].map(() => parts.map(() => {
    const s = new T3.Sprite(new T3.SpriteMaterial({ map: txF, color: 0x9DABC2, transparent: true, opacity: 0, depthWrite: false })); B.scene.add(s); return s;
  }));
  const dest = parts.slice(0, 24).map(() => {
    const s = new T3.Sprite(new T3.SpriteMaterial({ map: txF, color: 0x8FB8FF, transparent: true, opacity: 0, depthWrite: false })); B.scene.add(s); return s;
  });
  const boca0 = [0, 0];

  function atualiza(e) {
    const xr = e.xr, zb = e.zb;
    rifle.position.set(xr, 0, zb);
    sombraR.position.set(xr - 2.5, 0, 0.005); sombraR.material.opacity = 0.6;
    // apoios (no chão, fixos): alturas até o rifle em repouso
    const zf = zb - 0.19, zt = zb - 0.335, wob = e.wob || 0;
    bipe.position.set(e.xr0 - 1.23, 0, 0); yoke.position.set(0, 0, zf); yoke.rotation.y = wob;
    pernas.forEach(([p, s]) => { const a = new T3.Vector3(0, s * 0.45, 0), b = new T3.Vector3(0, 0, zf - 0.05), d = b.clone().sub(a);
      p.scale.set(1, d.length(), 1); p.position.copy(a.clone().add(b).multiplyScalar(0.5)); p.quaternion.setFromUnitVectors(new T3.Vector3(0, 1, 0), d.normalize()); });
    desc.position.set(e.xr0 - 3.89, 0, 0); yoke2.position.set(0, 0, zt);
    hastes.forEach(h => { h.scale.set(1, zt - 0.05, 1); h.rotation.x = PI / 2; h.position.set(0, 0, (zt - 0.05) / 2); });
    sbi.position.set(e.xr0 - 1.23, 0, 0.005); sde.position.set(e.xr0 - 3.89, 0, 0.005);
    const tiros = e.tiros || [];
    const s = tiros.length ? tiros[tiros.length - 1] : -1;
    clarao.visible = s >= 0 && s < 0.12;
    if (clarao.visible) { const k = 1 - s / 0.12; clarao.position.set(e.xb0 + 0.25, 0, zb); clarao.scale.set(0.9 * k + 0.3, 0.6 * k + 0.2, 1); clarao.material.opacity = k; }
    bala.visible = e.bala !== null && e.bala !== undefined; if (bala.visible) bala.position.set(e.bala, 0, zb);
    nuvens.forEach((nv, k) => {
      const a = tiros.length - 1 - k >= 0 ? tiros[tiros.length - 1 - k] : -1;
      nv.forEach((sp, i) => {
        const p = parts[i];
        if (a < 0 || a > 40) { sp.visible = false; return; }
        const f = 1 - Math.exp(-a / p.tau), lin = Math.max(0, a - 1.2) * 0.1 * p.sp;   // v7: os gases seguem se dispersando (palco vivo)
        sp.visible = true;
        sp.position.set(e.xb0 + 0.15 + p.dx * f + lin * 1.2, p.dy * f + lin * 0.3, zb + p.dz * f * 0.6 + lin * 0.5);
        const r = p.r0 * (0.5 + 1.6 * f) + 0.06 * Math.min(a, 6);
        sp.scale.set(2 * r, 2 * r, 1);
        sp.material.opacity = (0.3 * Math.exp(-a / 1.3) + 0.16 * Math.exp(-a / 14)) * Math.min(1, a / 0.05) * (k ? 0.6 : 1);
      });
    });
    dest.forEach((sp, i) => {
      const p = parts[i], a = e.nv;
      if (a === null || a === undefined) { sp.visible = false; return; }
      const u = Math.min(1, a / 1.4);
      sp.visible = true; sp.position.set(e.xb0 + 0.15 + 1.1 * p.dx / 1.75 * u, p.dy * 0.7 * u, zb + p.dz * 0.5 * u);
      const r = p.r0 * (0.6 + 0.8 * u); sp.scale.set(2 * r, 2 * r, 1); sp.material.opacity = 0.42 * Math.min(1, a / 0.3);
    });
  }
  window.CENA = { atualiza };
  window.pontos3d = e => ({ boca: B.projeta([e.xr, 0, e.zb]), coronha: B.projeta([e.xr - 4.97, 0, e.zb - 0.5]), topo: B.projeta([e.xr - 2.25, 0, e.zb + 0.4]),
    bipe: B.projeta([e.xr0 - 1.23, 0, 0]), desc: B.projeta([e.xr0 - 3.89, 0, 0]) });
  window.cenaPronta = true;
})();
