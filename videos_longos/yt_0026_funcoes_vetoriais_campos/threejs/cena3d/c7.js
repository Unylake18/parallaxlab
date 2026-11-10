// yt_0026 v7: as quatro cenas 3D do storyboard (c3d.html): colunas, fluxo, paraboloide, campo. Câmera de perspectiva (fov 22°) como no storyboard; o QUADRO inteiro
// (1920×1080 virtuais) é encolhido para dentro da caixa e.box = [bx, by, bw, bh] (px de 1080p), exatamente como o `img3d` do storyboard.
// Sem sombra, sem piso de sombra, sem névoa, sem materiais transparentes. Cena por window.CENA_ID.
(function () {
  const T = THREE, PI = Math.PI, id = window.CENA_ID;
  const W = window.innerWidth, H = window.innerHeight;
  const R = new T.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
  R.setPixelRatio(1); R.setSize(W, H, false); R.setClearColor(0x000000, 0); document.body.appendChild(R.domElement);
  const S = new T.Scene(); T.Object3D.DefaultUp.set(0, 0, 1);
  const cam = new T.PerspectiveCamera(22, 16 / 9, 0.1, 200); cam.up.set(0, 0, 1);
  const col = h => new T.Color(h);
  const key = new T.DirectionalLight(0xffffff, 0.95); key.position.set(-5, -3, 8); S.add(key);
  S.add(new T.HemisphereLight(0xBFD6FF, 0x0A1326, 0.45));
  const rim = new T.DirectionalLight(0x9CC8FF, 0.45); rim.position.set(4, 6, 2); S.add(rim);
  if (id !== 'colunas' && id !== 'campo') { const fill = new T.DirectionalLight(0xAFC8FF, 0.55); fill.position.set(6, -9, -1); S.add(fill); }
  function comBorda(m, cor, forca) {
    m.onBeforeCompile = sh => {
      sh.uniforms.rimC = { value: col(cor) }; sh.uniforms.rimK = { value: forca };
      sh.fragmentShader = 'uniform vec3 rimC; uniform float rimK;\n' + sh.fragmentShader.replace('#include <dithering_fragment>',
        '#include <dithering_fragment>\n float fr=1.0-abs(dot(normalize(vViewPosition),normalize(vNormal)));\n gl_FragColor.rgb+=rimC*pow(fr,2.6)*rimK;');
    };
    return m;
  }
  const tubo = (pts, r, cor) => new T.Mesh(new T.TubeGeometry(new T.CatmullRomCurve3(pts), Math.max(8, pts.length * 2), r, 8, false), new T.MeshBasicMaterial({ color: cor }));
  function seta(a, b, r, cor) {
    const d = new T.Vector3().subVectors(b, a), L = d.length(), g = new T.Group(), hl = Math.min(0.2, 0.4 * L), hr = Math.max(r * 2.6, hl * 0.38);
    const m = comBorda(new T.MeshStandardMaterial({ color: cor, roughness: 0.4, metalness: 0, emissive: col(cor), emissiveIntensity: 0.3 }), '#D2FFEF', 0.45);
    const sh = new T.Mesh(new T.CylinderGeometry(r, r, L - hl, 10), m); sh.position.y = (L - hl) / 2;
    const cn = new T.Mesh(new T.ConeGeometry(hr, hl, 16), m); cn.position.y = L - hl / 2; g.add(sh, cn);
    g.position.copy(a); g.quaternion.setFromUnitVectors(new T.Vector3(0, 1, 0), d.clone().normalize()); return g;
  }
  const raiz = new T.Group(); S.add(raiz);
  const matBorda = (cor, side, rimC, rimK) => comBorda(new T.MeshStandardMaterial({ color: cor, roughness: 0.6, metalness: 0, side, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 }), rimC, rimK);
  const K = 0.55;
  const fpar = (r, t, s) => new T.Vector3(r * Math.cos(t), r * Math.sin(t), s * K * r * r);
  // malha (r, θ) com z = s·K·r² atualizável
  function malhaPar(rmax, nu, nv) {
    const pos = new Float32Array((nu + 1) * (nv + 1) * 3), idx = [];
    for (let i = 0; i < nu; i++) for (let j = 0; j < nv; j++) { const a = i * (nv + 1) + j, b = a + 1, c = (i + 1) * (nv + 1) + j, d = c + 1; idx.push(a, b, c, b, d, c); }
    const g = new T.BufferGeometry(); g.setAttribute('position', new T.BufferAttribute(pos, 3)); g.setIndex(idx);
    g.userData.poe = s => { let k = 0; for (let i = 0; i <= nu; i++) for (let j = 0; j <= nv; j++) { const p = fpar(rmax * i / nu, 2 * PI * j / nv, s); pos[k++] = p.x; pos[k++] = p.y; pos[k++] = p.z; } g.attributes.position.needsUpdate = true; g.computeVertexNormals(); };
    return g;
  }
  let atualiza = () => {}, rotulos = () => ({});

  if (id === 'colunas') {
    cam.position.set(9.6, -8.2, 7.2); cam.lookAt(1.5, 1.0, 1.0);
    const z = (x, y) => 1.5 + 0.5 * Math.sin(1.5 * x) * Math.cos(1.2 * y);
    const tons = { x: 0x4470C0, y: 0x1F3A72, top: 0x9CC6FF }, mats = [tons.x, tons.x, tons.y, tons.y, tons.top, tons.top].map(c => new T.MeshBasicMaterial({ color: c }));
    const ar = new T.LineBasicMaterial({ color: 0x6F8FC4 });         // aresta clara (opaca)
    const niveis = [[6, 4], [12, 8], [24, 16]].map(([nx, ny]) => {
      const g = new T.Group(), dx = 3 / nx, dy = 2 / ny, gap = 0.12;
      for (let i = 0; i < nx; i++) for (let j = 0; j < ny; j++) {
        const x = (i + 0.5) * dx, y = (j + 0.5) * dy, h = z(x, y), bg = new T.BoxGeometry(dx * (1 - gap), dy * (1 - gap), h);
        const b = new T.Mesh(bg, mats); b.position.set(x, y, h / 2); g.add(b);
        const e = new T.LineSegments(new T.EdgesGeometry(bg), ar); e.position.copy(b.position); g.add(e);
      }
      g.visible = false; raiz.add(g); return g;
    });
    const lm = new T.LineBasicMaterial({ color: 0xDCEBFF });
    for (let k = 0; k <= 12; k++) {
      const p = [], q = [];
      for (let s = 0; s <= 40; s++) { const X = 3 * s / 40, Y = 2 * k / 12; p.push(new T.Vector3(X, Y, z(X, Y) + 0.12)); const X2 = 3 * k / 12, Y2 = 2 * s / 40; q.push(new T.Vector3(X2, Y2, z(X2, Y2) + 0.12)); }
      raiz.add(new T.Line(new T.BufferGeometry().setFromPoints(p), lm), new T.Line(new T.BufferGeometry().setFromPoints(q), lm));
    }
    const base = new T.Mesh(new T.PlaneGeometry(3.4, 2.4), new T.MeshBasicMaterial({ color: 0x0E1B38 })); base.position.set(1.5, 1, -0.003); raiz.add(base);
    atualiza = e => { niveis.forEach((g, k) => { g.visible = (e.nivel || 0) === k; }); };
  }

  if (id === 'fluxo') {
    cam.position.set(9.0, -11.2, 7.0); cam.lookAt(0, 0, 1.0);
    const g = malhaPar(1.8, 48, 96); g.userData.poe(1.0);
    raiz.add(new T.Mesh(g, matBorda(0x35589E, T.FrontSide, '#7FB2FF', 0.25)), new T.Mesh(g, matBorda(0x6E9EF0, T.BackSide, '#BFD8FF', 0.55)));
    for (let k = 1; k <= 3; k++) { const p = []; for (let i = 0; i <= 96; i++) p.push(fpar(0.6 * k, 2 * PI * i / 96, 1)); raiz.add(tubo(p, 0.014, 0xDCEBFF)); }
    for (let k = 0; k < 8; k++) { const p = []; for (let i = 0; i <= 30; i++) p.push(fpar(1.8 * i / 30, k * PI / 4, 1)); raiz.add(tubo(p, 0.01, 0xDCEBFF)); }
    const setas = [[-1.2, -0.5], [-0.6, 0.6], [0, 0], [0.6, -0.7], [1.1, 0.4], [-0.2, -1.2], [0.3, 1.1], [-1.0, 1.0], [1.0, -1.1]].map(([a, b]) => {
      const z0 = K * (a * a + b * b), s = seta(new T.Vector3(a, b, z0 - 0.35), new T.Vector3(a, b, z0 + 0.8), 0.03, 0x2EE6A0); raiz.add(s); return s;
    });
    atualiza = e => { const o = e.sobe || 0; setas.forEach(s => { s.position.z = (s.userData.z0 === undefined ? (s.userData.z0 = s.position.z) : s.userData.z0) + o; }); };
  }

  if (id === 'paraboloide') {
    cam.position.set(9.0, -11.2, 7.0); cam.lookAt(0, 0, 1.0);
    const g = malhaPar(2, 64, 128);
    raiz.add(new T.Mesh(g, matBorda(0x35589E, T.FrontSide, '#7FB2FF', 0.25)), new T.Mesh(g, matBorda(0x6E9EF0, T.BackSide, '#BFD8FF', 0.55)));
    const chapa = new T.Mesh(new T.CircleGeometry(2, 96), new T.MeshBasicMaterial({ color: 0x0F1C3A })); chapa.position.z = 0.002; raiz.add(chapa);
    const cp = []; for (let i = 0; i <= 96; i++) cp.push(new T.Vector3(2 * Math.cos(2 * PI * i / 96), 2 * Math.sin(2 * PI * i / 96), 0.004)); raiz.add(tubo(cp, 0.012, 0x4A5668));
    [[2.9, 0, 0], [0, 2.9, 0], [0, 0, 2.9 * 1.25]].forEach(v => raiz.add(seta(new T.Vector3(0, 0, 0), new T.Vector3(...v), 0.012, 0x8FA3C4)));
    let ls = [], sAtual = -1;
    function monta(s) {
      ls.forEach(m => { raiz.remove(m); m.geometry.dispose(); }); ls = [];
      for (let c = -1.5; c <= 1.51; c += 0.5) {
        const w = Math.sqrt(4 - c * c), pu = [], pv = [];
        for (let i = 0; i <= 40; i++) { const t = -w + 2 * w * i / 40; pu.push(new T.Vector3(c, t, s * K * (c * c + t * t))); pv.push(new T.Vector3(t, c, s * K * (c * c + t * t))); }
        ls.push(tubo(pu, 0.017, 0xFFC24D), tubo(pv, 0.017, 0xEA63FF));
      }
      [1, 2].forEach(r => { const p = []; for (let i = 0; i <= 96; i++) p.push(fpar(r, 2 * PI * i / 96, s)); ls.push(tubo(p, r === 2 ? 0.022 : 0.018, 0xDCEBFF)); });
      ls.forEach(m => raiz.add(m)); g.userData.poe(s);
    }
    atualiza = e => { const s = e.s === undefined ? 1 : e.s; if (Math.abs(s - sAtual) > 1e-5) { monta(s); sAtual = s; } };
    rotulos = e => { const s = e.s === undefined ? 1 : e.s; return { a4: fpar(2, -0.28, s), a1: fpar(1, -0.55, s) }; };
  }

  if (id === 'campo') {
    const p0 = new T.Vector3(8.3, -8.3, 4.6);
    const fib = n => { const out = [], ga = PI * (3 - Math.sqrt(5)); for (let i = 0; i < n; i++) { const y = 1 - 2 * (i + 0.5) / n, r = Math.sqrt(1 - y * y), t = i * ga; out.push(new T.Vector3(r * Math.cos(t), y, r * Math.sin(t))); } return out; };
    const claro = col('#8CFFD2'), escuro = col('#1FB57E'), lm = new T.LineBasicMaterial({ color: 0x1A2540 }), fl = [];
    [[1.5, 26, 0.0], [2.3, 40, 0.7]].forEach(([r, n, rot]) => {
      [[1, 0, 0], [0, 1, 0], [0, 0, 1]].forEach(ax => {
        const pts = []; for (let i = 0; i <= 96; i++) { const t = 2 * PI * i / 96; const v = ax[2] ? new T.Vector3(Math.cos(t), Math.sin(t), 0) : ax[0] ? new T.Vector3(0, Math.cos(t), Math.sin(t)) : new T.Vector3(Math.cos(t), 0, Math.sin(t)); pts.push(v.multiplyScalar(r)); }
        raiz.add(new T.Line(new T.BufferGeometry().setFromPoints(pts), lm));
      });
      fib(n).forEach(d => {
        d.applyAxisAngle(new T.Vector3(0, 0, 1), rot);
        const p = d.clone().multiplyScalar(r), L = 0.8 / (r * r) * 1.15, c = escuro.clone().lerp(claro, Math.min(1, (1 / (r * r)) / (1 / 1.5625)));
        const s = seta(p, p.clone().add(d.clone().multiplyScalar(-L)), 0.022, c.getHex()); raiz.add(s); fl.push({ s, p, d });
      });
    });
    const anel = new T.Mesh(new T.TorusGeometry(0.13, 0.022, 12, 48), new T.MeshStandardMaterial({ color: 0xF5F7FF, emissive: 0xF5F7FF, emissiveIntensity: 0.5 })); raiz.add(anel);
    atualiza = e => {
      const a = (e.az || 0) * PI / 180; cam.position.copy(p0).applyAxisAngle(new T.Vector3(0, 0, 1), a); cam.lookAt(0, 0, 0);
      fl.forEach(f => { const vis = cam.position.clone().sub(f.p).normalize(); f.s.visible = Math.abs(vis.dot(f.d)) <= Math.cos(55 * PI / 180); });
      anel.quaternion.copy(cam.quaternion);
    };
    window.contaVis = () => fl.filter(f => f.s.visible).length;
  }

  // medida do objeto (bbox em px do quadro virtual 1920×1080, estado final): o objeto é ENCAIXADO na caixa e.box (como o PNG recortado do storyboard)
  let BB = null;
  function medida() {
    atualiza({ nivel: 1, sobe: 0.25, s: 1, az: 0 });
    if (id !== 'campo') cam.lookAt(...(id === 'colunas' ? [1.5, 1.0, 1.0] : [0, 0, 1.0]));
    cam.clearViewOffset(); cam.aspect = 16 / 9; cam.updateProjectionMatrix(); cam.updateMatrixWorld(true); S.updateMatrixWorld(true);
    let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9; const v = new T.Vector3();
    S.traverse(o => {
      if (!(o.isMesh || o.isLine || o.isLineSegments)) return;
      for (let p = o; p; p = p.parent) if (!p.visible) return;
      const pos = o.geometry.attributes.position; if (!pos) return;
      const st = Math.max(1, Math.floor(pos.count / 3000));
      for (let i = 0; i < pos.count; i += st) { v.fromBufferAttribute(pos, i).applyMatrix4(o.matrixWorld).project(cam); const X = (v.x + 1) / 2 * 1920, Y = (1 - v.y) / 2 * 1080; x0 = Math.min(x0, X); x1 = Math.max(x1, X); y0 = Math.min(y0, Y); y1 = Math.max(y1, Y); }
    });
    BB = [x0, y0, x1, y1]; console.log('[bbox] ' + id + ' ' + JSON.stringify(BB.map(n => Math.round(n * 10) / 10)));
  }
  window.setEstado = function (e) {
    if (!BB) medida();
    atualiza(e);
    if (id !== 'campo') { cam.lookAt(...(id === 'colunas' ? [1.5, 1.0, 1.0] : [0, 0, 1.0])); }
    const [bx, by, bw, bh] = e.box || [0, 0, 1920, 1080], wb = BB[2] - BB[0], hb = BB[3] - BB[1], s = 0.94 * Math.min(bw / wb, bh / hb), k = W / 1920;
    const cxb = (BB[0] + BB[2]) / 2, cyb = (BB[1] + BB[3]) / 2, Fx = bx + bw / 2 + (960 - cxb) * s, Fy = by + bh / 2 + (540 - cyb) * s;
    cam.setViewOffset(1920 * s * k, 1080 * s * k, -(Fx - 960 * s) * k, -(Fy - 540 * s) * k, W, H); cam.aspect = 16 / 9; cam.updateProjectionMatrix(); cam.updateMatrixWorld();
    R.clear(); R.render(S, cam);
    const out = {}, rr = rotulos(e);
    Object.entries(rr).forEach(([n, v]) => { const p = v.clone().project(cam); out[n] = [(p.x + 1) / 2 * W, (1 - p.y) / 2 * H]; });
    const o = new T.Vector3(0, 0, 0).project(cam); out.o = [(o.x + 1) / 2 * W, (1 - o.y) / 2 * H];
    return out;
  };
  window.cenaPronta = true;
})();
