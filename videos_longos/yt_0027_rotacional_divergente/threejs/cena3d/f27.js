// yt_0027 v2 (handoff v2 §3; construção do referencia_v2/c3d27.html): três vistas simples, fundo transparente composto sobre o milimetrado.
// (r128 sem gerenciamento de cor: intensidades 0,75 / 0,25 / 0,22 calibradas para o tom do alvo.) Câmera e projeção pela base b3d.js (a mesma do kit.projeta3d). Luz do c3d27: ambiente 0,55 + chave 1,6 em (4, −6, 8) + contraluz 0x9fb8ff 0,5 em (−6, 4, 2).
// Materiais MeshStandard (rugosidade 0,55, emissivo leve). Setas com corpo (haste + cone de raio 3,2 × haste).
//   'cubo' (B6-1, v3 = cubo3): cubo-chapa translúcido, UMA seta por parede (sai 2× a entra), molduras por eixo que acendem com a parcela.
//   'roda' (B6-2/3): giro rígido em torno de W (inclinado 35°): 2 anéis de 10 setas finas (raio 1,9, alturas ±0,9 ao longo de W) que giram com o
//                  fluido (e.giro) e uma linha-guia escura por anel; rodinha de 4 pás coral 0,8 × 0,55 (pá marcada azul-clara), eixo GEO e cubo escuro,
//                  orientada por e.n e girando e.fase em torno do próprio eixo; eixo do giro tracejado (e.eixo); seta violeta do rot ao longo de W (e.rot).
(function () {
  const B = B3D, T3 = THREE, PI = Math.PI, id = window.CENA_ID;
  B.ceu(false);
  B.scene.environment = null;
  B.renderer.shadowMap.enabled = false;
  B.luz.chave.color.set(0xffffff); B.luz.chave.intensity = 0.75; B.luz.chave.position.set(4, -6, 8);
  B.luz.rim.color.set(0x9fb8ff); B.luz.rim.intensity = 0.25; B.luz.rim.position.set(-6, 4, 2);
  B.luz.amb.color.set(0xffffff); B.luz.amb.intensity = 0.22;
  const mat = (c, e = 0) => new T3.MeshStandardMaterial({ color: c, roughness: 0.55, metalness: 0, emissive: c, emissiveIntensity: e, side: T3.DoubleSide });
  const Y = new T3.Vector3(0, 1, 0);
  function seta(a, b, cor, raio = 0.035, pai = B.scene) {
    const A = new T3.Vector3(...a), Bv = new T3.Vector3(...b), v = Bv.clone().sub(A), L = v.length(), h = Math.min(0.26, 0.42 * L), g = new T3.Group();
    const m = mat(cor, 0.25), c1 = new T3.Mesh(new T3.CylinderGeometry(raio, raio, L - h, 16), m); c1.position.y = (L - h) / 2;
    const c2 = new T3.Mesh(new T3.ConeGeometry(raio * 3.2, h, 24), m); c2.position.y = L - h / 2; g.add(c1, c2);
    g.position.copy(A); g.quaternion.setFromUnitVectors(Y, v.normalize()); pai.add(g); return g;
  }
  const MENTA = 0x2EE6A0, MENTA2 = 0x8CFFD2, GEO = 0xB8C4DA, VEL = 0x9C8CFF, CORAL = 0xFF7A8A;
  let atualiza = () => {}, pontos = () => ({});

  if (id === 'cubo') {
    // v3 (handoff v3 §3.3; c3d27.html ?k=cubo3): cubo-chapa translúcido (#1A2C52 a 32 %, sem escrever profundidade) com arestas GEO; UMA seta por
    // parede, material chapado (MeshBasic: sem luz, sem brilho). F = (x, y, z) no cubo [1, 2]³: em cada par de paredes entra 1 e sai 2 (a de saída
    // tem o dobro do comprimento). Moldura fina da cor do eixo por dentro de cada parede (x âmbar, y magenta, z ciano), que acende com a parcela (e.acende).
    // e.onda (0..3): as setas de cada par crescem (x, depois y, depois z).
    const a = 1.6, h = a / 2, flat = c => new T3.MeshBasicMaterial({ color: c });
    const caixa = new T3.Mesh(new T3.BoxGeometry(a, a, a), new T3.MeshBasicMaterial({ color: 0x1A2C52, transparent: true, opacity: 0.32, depthWrite: false, side: T3.DoubleSide }));
    caixa.material.userData.excecao = 'chapa do cubo a 32 % (handoff v3 §3.3)';
    B.scene.add(caixa);
    B.scene.add(new T3.LineSegments(new T3.EdgesGeometry(new T3.BoxGeometry(a, a, a)), new T3.LineBasicMaterial({ color: 0xB8C4DA })));
    // v4 N5: as de ENTRADA em menta a 70 %, comprimento 0,75, desenhadas depois da chapa (renderOrder 2: não escurecem através do vidro, ponta inteira).
    function setaP(A, Bv, cor, op = 1) {
      const v = Bv.clone().sub(A), L = v.length(), hl = 0.22, g = new T3.Group();
      const mt = () => { const m = flat(cor); if (op < 1) { m.transparent = true; m.opacity = op; m.userData.excecao = 'seta de entrada a 70 % (handoff v4 N5)'; } return m; };
      const sh = new T3.Mesh(new T3.CylinderGeometry(0.03, 0.03, L - hl, 16), mt()); sh.position.y = (L - hl) / 2;
      const cn = new T3.Mesh(new T3.ConeGeometry(0.095, hl, 24), mt()); cn.position.y = L - hl / 2; g.add(sh, cn);
      if (op < 1) { sh.renderOrder = cn.renderOrder = 2; }
      g.position.copy(A); g.quaternion.setFromUnitVectors(Y, v.normalize()); B.scene.add(g); return g;
    }
    const AX = [0xFFC24D, 0xEA63FF, 0x35D9FF], Lin = 0.75, Lout = 1.1, pares = [], molduras = [];
    for (let ax = 0; ax < 3; ax++) {
      const n = new T3.Vector3(); n.setComponent(ax, 1);
      const mold = [];
      for (const s of [-1, 1]) {
        const fr = new T3.Group(), w = a * 0.78, t = 0.03;
        for (const [dx, dy, sx, sy] of [[0, w / 2, w, t], [0, -w / 2, w, t], [w / 2, 0, t, w], [-w / 2, 0, t, w]]) {
          const mm = new T3.MeshBasicMaterial({ color: AX[ax], side: T3.DoubleSide });
          if (s < 0) { mm.transparent = true; mm.opacity = 0.5; mm.userData.excecao = 'moldura da parede de trás a 50 % (handoff v4 N5)'; }
          const m = new T3.Mesh(new T3.PlaneGeometry(sx, sy), mm); m.position.set(dx, dy, 0); fr.add(m);
        }
        fr.quaternion.setFromUnitVectors(new T3.Vector3(0, 0, 1), n.clone().multiplyScalar(s)); fr.position.copy(n.clone().multiplyScalar(s * (h + 0.004)));
        B.scene.add(fr); mold.push(fr);
      }
      molduras.push(mold);
      const pIn = n.clone().multiplyScalar(-h), pOut = n.clone().multiplyScalar(h);
      const e = setaP(pIn.clone().sub(n.clone().multiplyScalar(Lin)), pIn, 0x2EE6A0, 0.7);
      const sa = setaP(pOut, pOut.clone().add(n.clone().multiplyScalar(Lout)), 0x8CFFD2);
      pares.push([e, sa]);
    }
    atualiza = e => {
      const onda = e.onda == null ? 9 : e.onda, ac = e.acende || [1, 1, 1];
      pares.forEach((pr, k) => { const s = Math.min(1, Math.max(0, onda - k)); pr.forEach(m => { m.scale.setScalar(Math.max(0.001, s)); m.visible = s > 0.01; }); });
      molduras.forEach((mold, k) => mold.forEach(m => { m.visible = ac[k] > 0.5; }));
    };
    pontos = () => ({ o: B.projeta([0, 0, 0]), face: B.projeta([h, 0, 0]) });
    console.log(`cubo3: aresta ${a}, 3 pares de paredes (entra ${Lin}, sai ${Lout}), molduras por eixo`);
  }

  if (id === 'roda') {
    const th = 35 * PI / 180, W = new T3.Vector3(Math.sin(th), 0, Math.cos(th));
    const e1 = new T3.Vector3(Math.cos(th), 0, -Math.sin(th)), e2 = new T3.Vector3(0, 1, 0);
    const aneis = new T3.Group(); B.scene.add(aneis);
    for (const z of [-0.9, 0.9]) {
      const R = 1.9, n = 10;
      for (let i = 0; i < n; i++) {
        const a = 2 * PI * i / n, p = W.clone().multiplyScalar(z).add(e1.clone().multiplyScalar(R * Math.cos(a))).add(e2.clone().multiplyScalar(R * Math.sin(a)));
        const t = e1.clone().multiplyScalar(-Math.sin(a)).add(e2.clone().multiplyScalar(Math.cos(a))).multiplyScalar(0.55);
        seta(p.clone().sub(t.clone().multiplyScalar(0.5)).toArray(), p.clone().add(t.clone().multiplyScalar(0.5)).toArray(), MENTA, 0.028, aneis);
      }
      const ring = [];
      for (let i = 0; i <= 96; i++) { const a = 2 * PI * i / 96; ring.push(W.clone().multiplyScalar(z).add(e1.clone().multiplyScalar(1.9 * Math.cos(a))).add(e2.clone().multiplyScalar(1.9 * Math.sin(a)))); }
      B.scene.add(new T3.Line(new T3.BufferGeometry().setFromPoints(ring), new T3.LineBasicMaterial({ color: 0x1A5F55 })));
    }
    const ax = new T3.Line(new T3.BufferGeometry().setFromPoints([W.clone().multiplyScalar(-2.2), W.clone().multiplyScalar(2.2)]), new T3.LineDashedMaterial({ color: GEO, dashSize: 0.12, gapSize: 0.1 }));
    ax.computeLineDistances(); B.scene.add(ax);
    const g = new T3.Group(), giro = new T3.Group(); g.add(giro);
    giro.add(new T3.Mesh(new T3.CylinderGeometry(0.13, 0.13, 0.22, 24), mat(0x0B1530)));
    g.add(new T3.Mesh(new T3.CylinderGeometry(0.03, 0.03, 1.5, 12), mat(GEO)));
    for (let k = 0; k < 4; k++) {
      // pá marcada INTEIRA azul-clara, como a rodinha 2D (decisão do Kaio, 11/11)
      const p = new T3.Mesh(new T3.BoxGeometry(0.8, 0.55, 0.05), mat(k === 0 ? 0xA9CCFF : CORAL, 0.12)); p.position.set(0.52, 0, 0);
      const q = new T3.Group(); q.add(p); q.rotation.y = k * PI / 2 + 0.4; giro.add(q);
    }
    B.scene.add(g);
    const rot = seta([0, 0, 0], W.clone().multiplyScalar(2.0).toArray(), VEL, 0.045);
    atualiza = e => {
      const n = new T3.Vector3(...(e.n || [W.x, W.y, W.z])).normalize();
      g.quaternion.setFromUnitVectors(Y, n);
      giro.rotation.y = e.fase || 0;
      aneis.quaternion.setFromAxisAngle(W, e.giro || 0);
      ax.visible = !!e.eixo;
      const r = e.rot || 0; rot.scale.setScalar(Math.max(0.001, r)); rot.visible = r > 0.01;
    };
    pontos = e => { const r = e.rot || 0; return { o: B.projeta([0, 0, 0]), ponta: B.projeta(W.clone().multiplyScalar(2.0 * r).toArray()) }; };
    console.log(`roda: W = (${W.x.toFixed(3)}, 0, ${W.z.toFixed(3)}), 2 anéis x 10 setas`);
  }

  window.CENA = { atualiza };
  window.pontos3d = e => pontos(e);
  window.cenaPronta = true;
})();
