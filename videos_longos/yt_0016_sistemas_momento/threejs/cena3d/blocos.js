// v7: blocos de 1 kg (aço claro) e 2 kg (grafite) com cantos arredondados, mola helicoidal 3D comprimida entre eles, chão de
// concreto (T9, com atrito: poeira fina sob os blocos) ou gelo polido com reflexo e batentes de aço (T10, sem atrito).
// Câmera lateral um pouco elevada (~12°): as setas de momento do Manim são comparadas por comprimento.
// Estado (calculado no Manim, sec_t9.py / sec_t10.py; unidades 3D = unidades do Manim no plano y = 0):
//   {chao: 'concreto'|'gelo', blocos: [{x, w, h, d, mat: 'aco'|'grafite', op}], mola: {xa, xb, z, n} | null,
//    batentes: [x, ...], poeira: [[x, y, z, r, op], ...], cam}
(function () {
  const B = B3D, T3 = THREE, PI = Math.PI;
  B.luzLab();
  const piso = B.chao();
  function caixaArred(w, h, d, r) {                     // caixa com cantos arredondados (extrusão com chanfro redondo), base em z = 0
    const s = new T3.Shape(), x0 = -w / 2 + r, x1 = w / 2 - r, y0 = r, y1 = h - r;
    s.moveTo(x0, 0); s.lineTo(x1, 0); s.quadraticCurveTo(w / 2, 0, w / 2, y0); s.lineTo(w / 2, y1); s.quadraticCurveTo(w / 2, h, x1, h);
    s.lineTo(x0, h); s.quadraticCurveTo(-w / 2, h, -w / 2, y1); s.lineTo(-w / 2, y0); s.quadraticCurveTo(-w / 2, 0, x0, 0);
    const g = new T3.ExtrudeGeometry(s, { depth: d - 2 * r * 0.7, bevelEnabled: true, bevelThickness: r * 0.7, bevelSize: r * 0.55,
      bevelSegments: 5, curveSegments: 8 });
    g.translate(0, 0, -(d - 2 * r * 0.7) / 2); g.rotateX(PI / 2); g.computeVertexNormals();
    return g;
  }
  const MATS = { aco: () => B.mat(0xA3ADBC, 0.75, 0.32, 0.8), grafite: () => B.mat(0x3E444D, 0.35, 0.5, 0.55) };
  const bl = [0, 1].map(() => {
    const g = new T3.Group(), m = new T3.Mesh(new T3.BufferGeometry(), MATS.aco()); g.add(m); B.scene.add(g);
    const r = new T3.Group(), mr = new T3.Mesh(new T3.BufferGeometry(), MATS.aco()); r.add(mr); r.scale.z = -1; B.scene.add(r);
    const sb = B.sombra(1, 1);
    return { g, m, r, mr, sb, chave: '' };
  });
  // mola: hélice de aço (tubo), eixo em x
  class Helice extends T3.Curve {
    constructor(xa, xb, z, n, r) { super(); this.xa = xa; this.xb = xb; this.z = z; this.n = n; this.r = r; }
    getPoint(t, a = new T3.Vector3()) {
      const ang = 2 * PI * this.n * t, ext = Math.min(1, Math.min(t, 1 - t) / 0.05);
      return a.set(this.xa + (this.xb - this.xa) * t, this.r * ext * Math.cos(ang), this.z + this.r * ext * Math.sin(ang));
    }
  }
  const mola = new T3.Mesh(new T3.BufferGeometry(), B.mat(0xD0D8E4, 0.85, 0.25, 1.0)); B.scene.add(mola);
  // concreto: material sobre o chão (manchas e poros finos), borda que some no chão
  const texConc = (() => {
    const c = document.createElement('canvas'); c.width = 1024; c.height = 1024; const g = c.getContext('2d');
    const rg = g.createRadialGradient(512, 512, 60, 512, 512, 512);
    rg.addColorStop(0, 'rgba(98,104,116,1)'); rg.addColorStop(0.6, 'rgba(84,90,102,0.85)'); rg.addColorStop(1, 'rgba(70,76,88,0)');
    g.fillStyle = rg; g.fillRect(0, 0, 1024, 1024);
    let s = 23; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    for (let i = 0; i < 9000; i++) {
      const x = 1024 * rnd(), y = 1024 * rnd(), d = Math.hypot((x - 512) / 512, (y - 512) / 512), v = Math.floor(50 + 80 * rnd());
      g.fillStyle = `rgba(${v},${v + 3},${v + 8},${0.35 * Math.max(0, 1 - d)})`; g.fillRect(x, y, 1 + 2 * rnd(), 1 + 2 * rnd());
    }
    for (let i = 0; i < 40; i++) {                         // manchas
      const x = 1024 * rnd(), y = 1024 * rnd(), r = 20 + 70 * rnd(), d = Math.hypot((x - 512) / 512, (y - 512) / 512);
      const q = g.createRadialGradient(x, y, 0, x, y, r); q.addColorStop(0, `rgba(60,64,74,${0.25 * Math.max(0, 1 - d)})`); q.addColorStop(1, 'rgba(60,64,74,0)');
      g.fillStyle = q; g.fillRect(x - r, y - r, 2 * r, 2 * r);
    }
    return new T3.CanvasTexture(c);
  })();
  const conc = new T3.Mesh(new T3.PlaneGeometry(14, 7.5), B.mat(0x737A86, 0.0, 0.95, 0.1, { map: texConc, transparent: true, depthWrite: false }));
  conc.position.z = 0.002; conc.renderOrder = -4; B.scene.add(conc);
  // gelo polido: lâmina azulada brilhante e translúcida (deixa ver o reflexo dos blocos), borda que some
  const texGelo = (() => {
    const c = document.createElement('canvas'); c.width = 1024; c.height = 1024; const g = c.getContext('2d');
    const rg = g.createRadialGradient(512, 512, 60, 512, 512, 512);
    rg.addColorStop(0, 'rgba(120,160,215,0.36)'); rg.addColorStop(0.65, 'rgba(95,135,195,0.25)'); rg.addColorStop(1, 'rgba(80,120,180,0)');
    g.fillStyle = rg; g.fillRect(0, 0, 1024, 1024);
    let s = 31; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    for (let i = 0; i < 60; i++) {
      const x = 1024 * rnd(), y = 1024 * rnd(), L = 40 + 160 * rnd(), a = (rnd() - 0.5) * 0.5, d = Math.hypot((x - 512) / 512, (y - 512) / 512);
      g.strokeStyle = `rgba(225,238,255,${0.22 * Math.max(0, 1 - d)})`; g.lineWidth = 1;
      g.beginPath(); g.moveTo(x, y); g.lineTo(x + L * Math.cos(a), y + L * Math.sin(a)); g.stroke();
    }
    return new T3.CanvasTexture(c);
  })();
  const gelo = new T3.Mesh(new T3.PlaneGeometry(14, 7.5), B.mat(0x7F9CC8, 0.0, 0.08, 0.55, { map: texGelo, transparent: true, depthWrite: false }));
  gelo.position.z = 0.003; gelo.renderOrder = -3; B.scene.add(gelo);
  // batentes de aço
  const bat = [0, 1].map(() => {
    const m = new T3.Mesh(caixaArred(0.2, 1.2, 1.7, 0.04), B.mat(0x8A95A6, 0.8, 0.32, 0.8)); B.scene.add(m);
    const r = new T3.Mesh(m.geometry, m.material.clone()); r.material.transparent = true; r.material.opacity = 0.22; r.material.side = T3.DoubleSide;
    r.material.depthWrite = false; r.scale.z = -1; B.scene.add(r);
    return { m, r };
  });
  // poeira de atrito (pontos macios, cinza-azulados)
  const NP = 60, tx = B.sprite(64, 0.7);
  const po = [...Array(NP)].map(() => {
    const s = new T3.Sprite(new T3.SpriteMaterial({ map: tx, color: 0xB4BCCA, transparent: true, opacity: 0, depthWrite: false })); B.scene.add(s); return s;
  });

  function atualiza(e) {
    piso.visible = true;
    const cg = e.chao === 'gelo';
    conc.visible = !cg; gelo.visible = cg;
    const xc = (e.cam && e.cam.camx) || 0; conc.position.x = xc; gelo.position.x = xc;
    (e.blocos || []).forEach((b, i) => {
      const o = bl[i], k = [b.w, b.h, b.d, b.mat].join();
      if (o.chave !== k) {
        o.m.geometry.dispose(); o.m.geometry = caixaArred(b.w, b.h, b.d, 0.09); o.mr.geometry = o.m.geometry;
        o.m.material = MATS[b.mat](); o.mr.material = MATS[b.mat](); o.mr.material.transparent = true; o.mr.material.side = T3.DoubleSide;
        o.mr.material.depthWrite = false; o.chave = k;
      }
      const op = b.op === undefined ? 1 : b.op;
      o.g.visible = op > 0.01; o.g.position.set(b.x, 0, 0);
      o.m.material.transparent = op < 0.999; o.m.material.opacity = op;
      o.r.visible = cg && op > 0.01; o.r.position.set(b.x, 0, 0); o.mr.material.opacity = 0.11 * op;
      o.sb.visible = op > 0.01; o.sb.position.set(b.x, 0, 0.005); o.sb.scale.set(b.w * 1.35, b.d * 1.25, 1); o.sb.material.opacity = 0.75 * op;
    });
    for (let i = (e.blocos || []).length; i < 2; i++) { bl[i].g.visible = false; bl[i].r.visible = false; bl[i].sb.visible = false; }
    mola.visible = !!e.mola;
    if (e.mola) {
      mola.geometry.dispose();
      mola.geometry = new T3.TubeGeometry(new Helice(e.mola.xa, e.mola.xb, e.mola.z, e.mola.n || 7, 0.2), 260, 0.032, 8, false);
      mola.material.opacity = e.mola.op === undefined ? 1 : e.mola.op; mola.material.transparent = mola.material.opacity < 0.999;
    }
    bat.forEach((b, i) => {
      const x = (e.batentes || [])[i];
      b.m.visible = x !== undefined; b.r.visible = x !== undefined && cg;
      if (x !== undefined) { b.m.position.set(x, 0, 0); b.r.position.set(x, 0, 0); }
    });
    po.forEach((s, i) => {
      const p = (e.poeira || [])[i];
      s.visible = !!p;
      if (p) { s.position.set(p[0], p[1], p[2]); s.scale.set(p[3], p[3], 1); s.material.opacity = p[4]; }
    });
  }
  window.CENA = { atualiza };
  window.pontos3d = e => {
    const r = {};
    (e.blocos || []).forEach((b, i) => {
      r['b' + i] = B.projeta([b.x, -b.d / 2, b.h / 2]);              // centro da face da frente
      r['t' + i] = B.projeta([b.x, b.d / 2, b.h]);                   // aresta de cima, atrás
    });
    return r;
  };
  window.cenaPronta = true;
})();
