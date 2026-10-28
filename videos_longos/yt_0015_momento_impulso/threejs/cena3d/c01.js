// T1 — C01: trilho de ar, dois carrinhos iguais, explosão, colisão e a "visão do carro" (câmera que anda junto).
// O movimento dos carrinhos vem de TL.ensaios (mesma lógica em Python: threejs/modelo_c01.py → camada Manim).
(function () {
  const PI_ = Math.PI;
  const B = B3D, TL = B.TL, THREE_ = THREE, COR = B.COR, G = TL.geometria;
  const MEIA = G.carrinho_meia_largura;                       // 0,65
  const mat = (cor, met, rug, env) => new THREE_.MeshStandardMaterial({ color: cor, metalness: met, roughness: rug, envMapIntensity: env });
  const matAco = mat(COR.aco, 0.75, 0.5, 0.3), matClaro = mat(COR.geo, 0.7, 0.4, 0.3);
  const matTrilho = mat(0x6A7686, 0.8, 0.42, 0.3), matFuro = new THREE_.MeshBasicMaterial({ color: 0x0A0F1E });

  // mesa escura (só aparece na vista cênica) e trilho longo
  const mesa = new THREE_.Mesh(new THREE_.PlaneGeometry(260, 2.6), new THREE_.MeshBasicMaterial({ color: 0x0A1226 }));
  mesa.position.z = -0.62; B.scene.add(mesa);
  const trilho = new THREE_.Mesh(new THREE_.BoxGeometry(120, 1.2, 0.6), matTrilho); trilho.position.z = -0.3; B.scene.add(trilho);
  const topo = new THREE_.Mesh(new THREE_.BoxGeometry(120, 0.14, 0.07), matClaro); topo.position.set(0, -0.42, -0.035); B.scene.add(topo);
  {                                                            // furinhos do ar (em cima) e régua/furos na face frontal
    const n = 240, furos = new THREE_.InstancedMesh(new THREE_.CylinderGeometry(0.035, 0.035, 0.01, 8), matFuro, n * 2);
    const m4 = new THREE_.Matrix4(), rot = new THREE_.Matrix4().makeRotationX(PI_ / 2);
    let k = 0;
    for (let i = 0; i < n; i++) for (const y of [-0.2, 0.2]) { m4.makeTranslation(-59.75 + i * 0.5, y, 0.003); m4.multiply(rot); furos.setMatrixAt(k++, m4); }
    B.scene.add(furos);
    const nf = 240, frente = new THREE_.InstancedMesh(new THREE_.CylinderGeometry(0.045, 0.045, 0.01, 10), matFuro, nf);
    for (let i = 0; i < nf; i++) { m4.makeTranslation(-59.75 + i * 0.5, -0.606, -0.18); m4.multiply(new THREE_.Matrix4().makeRotationX(0)); frente.setMatrixAt(i, m4.clone().multiply(new THREE_.Matrix4().makeRotationX(0))); }
    // cilindros ficam com o eixo em y: viram "discos" na face frontal
    B.scene.add(frente);
    const nt = 121, ticks = new THREE_.InstancedMesh(new THREE_.BoxGeometry(0.03, 0.01, 0.16), new THREE_.MeshBasicMaterial({ color: COR.dim }), nt);
    for (let i = 0; i < nt; i++) { m4.makeTranslation(-60 + i, -0.606, -0.48); ticks.setMatrixAt(i, m4); }
    B.scene.add(ticks);
  }
  function carrinho() {
    const g = new THREE_.Group();
    const corpo = new THREE_.Mesh(new THREE_.BoxGeometry(2 * MEIA, 0.9, 0.75), matAco); corpo.position.z = 0.45; g.add(corpo);
    const faixa = new THREE_.Mesh(new THREE_.BoxGeometry(2 * MEIA + 0.02, 0.92, 0.13), matClaro); faixa.position.z = 0.45; g.add(faixa);
    const base = new THREE_.Mesh(new THREE_.BoxGeometry(2 * MEIA - 0.14, 0.7, 0.06), matClaro); base.position.z = 0.04; g.add(base);
    const somb = new THREE_.Mesh(new THREE_.PlaneGeometry(2 * MEIA + 0.5, 1.2), new THREE_.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.35, depthWrite: false }));
    somb.position.z = 0.004; g.add(somb);
    B.scene.add(g); return g;
  }
  const A = carrinho(), Bc = carrinho();
  const capsula = new THREE_.Mesh(new THREE_.CylinderGeometry(0.2, 0.2, 0.7, 16), mat(0x3A4256, 0.6, 0.5, 0.2));
  capsula.rotation.z = PI_ / 2; capsula.position.set(0, 0, 0.45); B.scene.add(capsula);
  const flash = new THREE_.Mesh(new THREE_.SphereGeometry(1, 20, 14), new THREE_.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0, depthWrite: false }));
  B.scene.add(flash);

  function estado(t) {                                         // espelho de modelo_c01.py
    let r = { xa: 1e3, xb: 1e3, va: 0, vb: 0, vis: 0, juntos: false, cap: 0, ev: null };
    for (const e of TL.ensaios) {
      const vis = B.rampa(t, e.vis[0], 0.4) * (1 - B.rampa(t, e.vis[1] - 0.4, 0.4));
      if (vis <= 0) continue;
      r.vis = vis;
      if (e.tipo === 'explosao') {
        const d = t > e.t_evento ? e.v * (t - e.t_evento) : 0;
        r.xa = -e.x0 - d; r.xb = e.x0 + d; r.va = t > e.t_evento ? -e.v : 0; r.vb = -r.va; r.cap = t < e.t_evento ? 1 : 1 - B.rampa(t, e.t_evento, 0.1);
        r.ev = e.t_evento;
      } else {
        const tc = e.t_move + (2 * e.x0 - 2 * MEIA) / (2 * e.v);
        if (t < e.t_move) { r.xa = -e.x0; r.xb = e.x0; }
        else if (t < tc) { r.xa = -e.x0 + e.v * (t - e.t_move); r.xb = e.x0 - e.v * (t - e.t_move); r.va = e.v; r.vb = -e.v; }
        else { r.xa = -MEIA; r.xb = MEIA; r.juntos = true; }
      }
    }
    return r;
  }
  window.estadoCarrinhos = estado;
  window.setFrame = function (f) {
    B.desenha(f, t => {
      const s = estado(t), ocultar = s.vis <= 0.001;
      A.visible = Bc.visible = !ocultar;
      const sc = 0.88 + 0.12 * s.vis;
      A.position.x = s.xa; Bc.position.x = s.xb;
      for (const c of [A, Bc]) c.scale.set(1, 1, 1);
      A.traverse(o => { if (o.material && o.material.transparent === false) {} });
      capsula.visible = s.cap > 0.02 && !ocultar; capsula.scale.setScalar(Math.max(s.cap, 0.01));
      const te = s.ev, u = te === null ? 2 : (t - te) / 0.35;
      flash.material.opacity = (u >= 0 && u < 1) ? 0.95 * (1 - u) * (1 - u) : 0;
      flash.scale.setScalar(0.2 + 1.5 * clampu(u)); flash.position.set(0, 0, 0.45);
      // o 3D recua (realce): aço mais escuro e sem brilho
      const re = B.chaves(TL.realce_3d, t, 'v');
      for (const m of [matAco, matClaro, matTrilho]) m.emissive.setScalar(0);
      matAco.color.set(COR.aco).multiplyScalar(1 - 0.5 * re); matClaro.color.set(COR.geo).multiplyScalar(1 - 0.5 * re);
      matTrilho.color.set(0x6A7686).multiplyScalar(1 - 0.5 * re);
    });
    return true;
  };
  function clampu(u) { return Math.min(1, Math.max(0, u)); }
  window.projeta = B.projeta;
  window.cenaPronta = true;
})();
