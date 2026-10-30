// T2 — C13: luz na água (corpúsculos). Espelho plano (C13-2) → tanque com água (C13-3 a C13-5).
// A trajetória de cada corpúsculo é analítica (espelhada em modelo_c13.py para a camada Manim).
(function () {
  const B = B3D, TL = B.TL, T = THREE, COR = B.COR, R = TL.raio, PI_ = Math.PI;
  const th1 = R.theta1 * PI_ / 180, th2 = Math.asin(Math.sin(th1) / R.n);
  const v1 = R.v1, v2 = R.n * R.v1, L = R.L, Ta = L / v1;
  const d1 = [Math.sin(th1), -Math.cos(th1)], d1r = [Math.sin(th1), Math.cos(th1)], d2 = [Math.sin(th2), -Math.cos(th2)];
  const T_ESP = Ta + L / v1, T_AGUA = Ta + (-R.z_fundo / Math.cos(th2)) / v2;
  function posicao(e, agua) {                               // (x, z) do corpúsculo e s depois do lançamento
    if (e < Ta) return [-L * d1[0] + d1[0] * v1 * e, L * Math.cos(th1) + d1[1] * v1 * e];
    const s = e - Ta;
    return agua ? [d2[0] * v2 * s, d2[1] * v2 * s] : [d1r[0] * v1 * s, d1r[1] * v1 * s];
  }
  const mat = (cor, met, rug, env) => new T.MeshStandardMaterial({ color: cor, metalness: met, roughness: rug, envMapIntensity: env });

  // espelho plano
  const espelho = new T.Mesh(new T.BoxGeometry(6.6, 1.4, 0.14), new T.MeshStandardMaterial({ color: 0xD5DEEE, metalness: 1, roughness: 0.1, envMapIntensity: 0.9, transparent: true }));
  espelho.position.set(0, 0, -0.07); B.scene.add(espelho);
  // tanque com água: volume translúcido (sem transmissão no r128), superfície e arestas de vidro
  const [tx0, tx1, tz0] = [TL.tanque.x0, TL.tanque.x1, R.z_fundo];
  const volume = new T.Mesh(new T.BoxGeometry(tx1 - tx0, 1.4, -tz0), new T.MeshStandardMaterial({ color: COR.painel, metalness: 0.1, roughness: 0.15, transparent: true, opacity: 0, depthWrite: false }));
  volume.position.set((tx0 + tx1) / 2, 0, tz0 / 2); B.scene.add(volume);
  const superf = new T.Mesh(new T.PlaneGeometry(tx1 - tx0, 1.4), new T.MeshStandardMaterial({ color: 0x2F6FC4, metalness: 0.2, roughness: 0.1, transparent: true, opacity: 0, depthWrite: false }));
  superf.position.set((tx0 + tx1) / 2, 0, 0.002); B.scene.add(superf);
  const arestas = new T.LineSegments(new T.EdgesGeometry(new T.BoxGeometry(tx1 - tx0, 1.4, -tz0)), new T.LineBasicMaterial({ color: COR.geo, transparent: true, opacity: 0.4 }));
  arestas.position.copy(volume.position); B.scene.add(arestas);
  // corpúsculos: pontos brancos brilhantes (sprites aditivos), um por vaga do pool
  const tex = B.sprite(64, 0.6), N = 18, sprites = [];
  for (let i = 0; i < N; i++) {
    const s = new T.Sprite(new T.SpriteMaterial({ map: tex, color: 0xffffff, transparent: true, depthTest: false, blending: T.AdditiveBlending }));
    s.scale.set(0.27, 0.27, 1); s.renderOrder = 10; B.scene.add(s); sprites.push(s);
  }
  window.setFrame = function (f) {
    B.desenha(f, t => {
      const troca = R.t_troca, a_esp = 1 - B.rampa(t, troca, 0.8), a_agua = B.rampa(t, troca + 0.2, 1.0);
      espelho.material.opacity = a_esp; espelho.visible = a_esp > 0.01;
      volume.material.opacity = 0.34 * a_agua; superf.material.opacity = 0.5 * a_agua;
      arestas.material.opacity = 0.18 + 0.6 * a_agua;
      const m = Math.floor(t / R.periodo + 1e-9);
      for (let i = 0; i < N; i++) {
        const k = m - (((m - i) % N) + N) % N, tk = k * R.periodo, e = t - tk;
        const agua = tk >= troca, fim = agua ? T_AGUA : T_ESP;
        const s = sprites[i];
        if (k < 0 || e < 0 || e > fim) { s.visible = false; continue; }
        const [x, z] = posicao(e, agua);
        s.visible = true; s.position.set(x, 0, z);
        const al = B.clamp(e / 0.25, 0, 1) * B.clamp((fim - e) / 0.3, 0, 1);
        s.material.opacity = al;
      }
    });
    return true;
  };
  window.projeta = B.projeta;
  window.cenaPronta = true;
})();
