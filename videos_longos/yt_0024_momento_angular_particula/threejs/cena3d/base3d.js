// yt_0024 v2 — base comum das cenas Three.js (r128) do "laboratório Parallax": renderer HDR com MSAA, ambiente PMREM próprio,
// câmera {az, el, alvo, K, fov, xc, yc} com a MESMA projeção do Python (pecas24.proj), luz chave e contraluz presas à câmera,
// bloom seletivo (só as malhas em B3.brilho brilham; o resto é oclusor preto), tom com ombro, vinheta, sRGB e saída com alfa.
// Uso: B3.render(e, {bloom, desf, antes(cam), esconderNoBrilho:[...]}) → nada; B3.projeta([x,y,z]) → [px, py].
window.B3 = (function () {
  const T3 = THREE, PI = Math.PI, W = innerWidth, H = innerHeight;
  const cl = (x, a, b) => Math.min(b, Math.max(a, x));
  const lin = hex => new T3.Color(hex).convertSRGBToLinear();
  const renderer = new T3.WebGLRenderer({ antialias: false, alpha: true, preserveDrawingBuffer: true, premultipliedAlpha: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H); renderer.setClearColor(0x000000, 0);
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = T3.PCFSoftShadowMap;
  renderer.outputEncoding = T3.LinearEncoding; renderer.toneMapping = T3.NoToneMapping;
  renderer.autoClear = false;
  document.body.appendChild(renderer.domElement);
  const gl2 = renderer.capabilities.isWebGL2;
  const scene = new T3.Scene();

  // ── ambiente: céu azul-espacial, softbox pequena e fraca fora do zênite, faixa fria ciano, magenta baixo no horizonte ──
  function ambiente(o) {
    o = Object.assign({ caixa: 17, int: 0.19, ciano: 1.1, mag: 0.6 }, o || {});
    const s = new T3.Scene();
    const g = new T3.SphereGeometry(50, 64, 32), cor = [], pos = g.attributes.position;
    const c0 = lin('#060D22'), c1 = lin('#14264C');
    for (let i = 0; i < pos.count; i++) { const u = cl((pos.getZ(i) / 50 + 0.3) / 1.3, 0, 1); const c = c0.clone().lerp(c1, u); cor.push(c.r, c.g, c.b); }
    g.setAttribute('color', new T3.Float32BufferAttribute(cor, 3));
    s.add(new T3.Mesh(g, new T3.MeshBasicMaterial({ vertexColors: true, side: T3.BackSide })));
    const painel = (w, h, hex, int, x, y, z) => {
      const m = new T3.Mesh(new T3.PlaneGeometry(w, h), new T3.MeshBasicMaterial({ color: lin(hex).multiplyScalar(int), side: T3.DoubleSide }));
      m.position.set(x, y, z); m.lookAt(0, 0, 0); s.add(m);
    };
    painel(o.caixa, o.caixa, '#F5F7FF', o.int, 22, 26, 30);
    painel(8, 36, '#35D9FF', o.ciano, -38, 0, 12);
    painel(60, 4, '#EA63FF', o.mag, 0, 40, 2);
    painel(60, 4, '#EA63FF', o.mag * 0.6, 0, -40, 2);
    scene.environment = new T3.PMREMGenerator(renderer).fromScene(s, 0.02).texture;
  }

  // ── luzes presas à câmera (o contraste não muda quando a câmera anda) + sol para as sombras ──
  const chave = new T3.DirectionalLight(0xffffff, 0.9), contra = new T3.DirectionalLight(lin("#8CC8FF"), 0.9);
  const alvoL = new T3.Object3D(); scene.add(alvoL); chave.target = alvoL; contra.target = alvoL;
  const sol = new T3.DirectionalLight(0xffffff, 0.30);
  sol.position.set(1.0, -0.8, 2.6); sol.castShadow = true;
  sol.shadow.mapSize.set(2048, 2048); sol.shadow.radius = 4; sol.shadow.bias = -0.0004; sol.shadow.normalBias = 0.0015;
  Object.assign(sol.shadow.camera, { left: -1.1, right: 1.1, top: 1.1, bottom: -1.1, near: 1, far: 5 });
  const amb = new T3.AmbientLight(0xffffff, 0.05);
  scene.add(chave, contra, sol, sol.target, amb);

  // ── câmeras ──
  const camP = new T3.PerspectiveCamera(30, W / H, 0.01, 100), camO = new T3.OrthographicCamera(-1, 1, 1, -1, 0.01, 100);
  let cam = camP;
  function base(c) {
    const a = c.az * PI / 180, e = c.el * PI / 180, al = new T3.Vector3(...c.alvo);
    const dir = new T3.Vector3(Math.cos(e) * Math.cos(a), Math.cos(e) * Math.sin(a), Math.sin(e));
    const up = new T3.Vector3(-Math.sin(e) * Math.cos(a), -Math.sin(e) * Math.sin(a), Math.cos(e));
    return { al, dir, up };
  }
  function posicionaCamera(c) {
    const { al, dir, up } = base(c), K = c.K;
    if (c.fov > 0) {
      const D = (9 / K / 2) / Math.tan(c.fov * PI / 360);
      cam = camP; cam.fov = c.fov; cam.aspect = W / H;
      cam.position.copy(al).addScaledVector(dir, D); cam.up.copy(up); cam.lookAt(al);
      cam.near = Math.max(0.01, D - 6); cam.far = D + 8;
      cam.setViewOffset(W, H, -(c.xc || 0) / 16 * W, (c.yc || 0) / 9 * H, W, H);
    } else {
      cam = camO;
      cam.left = (-8 - (c.xc || 0)) / K; cam.right = (8 - (c.xc || 0)) / K; cam.top = (4.5 - (c.yc || 0)) / K; cam.bottom = (-4.5 - (c.yc || 0)) / K;
      cam.position.copy(al).addScaledVector(dir, 10); cam.up.copy(up); cam.lookAt(al); cam.near = 4; cam.far = 16;
    }
    cam.updateProjectionMatrix(); cam.updateMatrixWorld();
    const dirCam = new T3.Vector3(); cam.getWorldDirection(dirCam);
    const dir_ = dirCam.clone().negate(), dir_dir = new T3.Vector3().crossVectors(dirCam, up).normalize();
    alvoL.position.copy(al);
    chave.position.copy(al).addScaledVector(dir_, 0.6).addScaledVector(dir_dir, 2.2).addScaledVector(up, 3.2);
    contra.position.copy(al).addScaledVector(dirCam, 3).addScaledVector(up, 0.35).addScaledVector(dir_dir, -1.6);
    return cam;
  }
  function projeta(p) { const v = new T3.Vector3(...p).project(cam); return [(v.x + 1) / 2 * W, (1 - v.y) / 2 * H]; }

  // ── pós-processamento ──
  const opt = { type: T3.HalfFloatType, format: T3.RGBAFormat, minFilter: T3.LinearFilter, magFilter: T3.LinearFilter, depthBuffer: true };
  const ms = (w, h) => { const r = gl2 ? new T3.WebGLMultisampleRenderTarget(w, h, opt) : new T3.WebGLRenderTarget(w, h, opt); if (gl2) r.samples = 4; return r; };
  const rtCena = ms(W, H), rtBrilho = ms(W / 2, H / 2);
  const mk = (w, h) => new T3.WebGLRenderTarget(w, h, Object.assign({}, opt, { depthBuffer: false }));
  const nv = [[mk(W / 2, H / 2), mk(W / 2, H / 2)], [mk(W / 4, H / 4), mk(W / 4, H / 4)], [mk(W / 8, H / 8), mk(W / 8, H / 8)]];
  const rtOut = mk(W, H), rtTmp = mk(W, H);
  const quadCam = new T3.OrthographicCamera(-1, 1, 1, -1, 0, 1), quadCena = new T3.Scene();
  const quad = new T3.Mesh(new T3.PlaneGeometry(2, 2)); quadCena.add(quad);
  const VS = 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }';
  const shPassa = new T3.ShaderMaterial({ uniforms: { t: { value: null }, lim: { value: 0.55 } }, vertexShader: VS,
    fragmentShader: 'uniform sampler2D t; uniform float lim; varying vec2 vUv; void main(){ vec4 c = texture2D(t, vUv); float l = max(c.r, max(c.g, c.b)); float k = smoothstep(lim, lim + 0.25, l); gl_FragColor = vec4(c.rgb * k, 1.0); }' });
  const shBlur = new T3.ShaderMaterial({ uniforms: { t: { value: null }, d: { value: new T3.Vector2() } }, vertexShader: VS,
    fragmentShader: 'uniform sampler2D t; uniform vec2 d; varying vec2 vUv; void main(){ vec4 s = texture2D(t, vUv) * 0.2270270; s += (texture2D(t, vUv + d * 1.3846154) + texture2D(t, vUv - d * 1.3846154)) * 0.3162162; s += (texture2D(t, vUv + d * 3.2307692) + texture2D(t, vUv - d * 3.2307692)) * 0.0702703; gl_FragColor = s; }' });
  const shComp = new T3.ShaderMaterial({ uniforms: { c: { value: null }, b0: { value: null }, b1: { value: null }, b2: { value: null }, forca: { value: 0.40 }, vin: { value: 0.16 }, asp: { value: W / H } }, vertexShader: VS,
    fragmentShader: `uniform sampler2D c, b0, b1, b2; uniform float forca, vin, asp; varying vec2 vUv;
      vec3 tom(vec3 x){ vec3 k = 0.8 + 0.2 * (1.0 - exp(-(x - 0.8) / 0.2)); return mix(x, k, step(0.8, x)); }
      vec3 srgb(vec3 x){ x = clamp(x, 0.0, 1.0); return mix(x * 12.92, 1.055 * pow(x, vec3(1.0 / 2.4)) - 0.055, step(0.0031308, x)); }
      void main(){
        vec4 s = texture2D(c, vUv); float a = clamp(s.a, 0.0, 1.0);
        vec3 col = s.rgb / max(a, 1e-4);
        vec3 bl = (texture2D(b0, vUv).rgb * 0.5 + texture2D(b1, vUv).rgb * 0.3 + texture2D(b2, vUv).rgb * 0.2) * forca * 2.0;
        vec2 q = (vUv - 0.5) * vec2(asp, 1.0); float v = 1.0 - vin * smoothstep(0.35, 1.05, length(q) * 1.15);
        vec3 dentro = srgb(tom((col + bl) * v));
        float ab = clamp(max(bl.r, max(bl.g, bl.b)), 0.0, 1.0);
        vec3 fora = srgb(tom(bl * v));
        gl_FragColor = vec4(dentro * a + fora * (1.0 - a), a + (1.0 - a) * ab);
      }` });
  const shCopia = new T3.ShaderMaterial({ uniforms: { t: { value: null } }, vertexShader: VS, fragmentShader: 'uniform sampler2D t; varying vec2 vUv; void main(){ gl_FragColor = texture2D(t, vUv); }' });
  const passa = (mat, alvo) => { quad.material = mat; renderer.setRenderTarget(alvo); renderer.clear(); renderer.render(quadCena, quadCam); };
  function blur(src, par, raio) {
    const [a, b] = par, w = a.width, h = a.height;
    shBlur.uniforms.t.value = src; shBlur.uniforms.d.value.set(raio / w, 0); passa(shBlur, a);
    shBlur.uniforms.t.value = a.texture; shBlur.uniforms.d.value.set(0, raio / h); passa(shBlur, b);
    return b.texture;
  }
  const brilho = [], PRETO = new T3.MeshBasicMaterial({ color: 0x000000 }), guarda = new Map();
  function passadaBrilho(esconder) {
    scene.traverse(o => { if (o.isMesh && !brilho.includes(o)) { guarda.set(o, o.material); o.material = Array.isArray(o.material) ? o.material.map(() => PRETO) : PRETO; } });
    const vis = (esconder || []).map(o => [o, o.visible]); vis.forEach(([o]) => { o.visible = false; });
    const env = scene.environment; scene.environment = null; const sombra = renderer.shadowMap.enabled; renderer.shadowMap.enabled = false;
    renderer.setRenderTarget(rtBrilho); renderer.setClearColor(0x000000, 1); renderer.clear(); renderer.render(scene, cam);
    vis.forEach(([o, v]) => { o.visible = v; });
    guarda.forEach((m, o) => { o.material = m; }); guarda.clear();
    scene.environment = env; renderer.shadowMap.enabled = sombra;
  }
  function render(e, o) {
    o = o || {};
    if (o.antes) o.antes(cam);
    renderer.setRenderTarget(rtCena); renderer.setClearColor(0x000000, 0); renderer.clear(); renderer.render(scene, cam);
    passadaBrilho(o.esconderNoBrilho);
    shPassa.uniforms.t.value = rtBrilho.texture; shPassa.uniforms.lim.value = o.limiar === undefined ? 0.55 : o.limiar; passa(shPassa, nv[0][0]);
    const r0 = 0.8;
    const t0 = blur(nv[0][0].texture, [nv[0][1], nv[0][0]], r0);
    const t1 = blur(t0, nv[1], r0 * 1.2), t2 = blur(t1, nv[2], r0 * 1.4);
    Object.assign(shComp.uniforms, { c: { value: rtCena.texture }, b0: { value: t0 }, b1: { value: t1 }, b2: { value: t2 } });
    shComp.uniforms.forca.value = e.bloom === undefined ? 0.40 : e.bloom;
    const desf = e.desf || 0;
    renderer.setRenderTarget(desf > 0 ? rtOut : null); renderer.setClearColor(0x000000, 0); renderer.clear();
    quad.material = shComp; renderer.render(quadCena, quadCam);
    if (desf > 0) {
      let t = rtOut.texture;
      for (let k = 0; k < 3; k++) {
        shBlur.uniforms.t.value = t; shBlur.uniforms.d.value.set(desf * 2.2 / W, 0); passa(shBlur, rtTmp);
        shBlur.uniforms.t.value = rtTmp.texture; shBlur.uniforms.d.value.set(0, desf * 2.2 / H); passa(shBlur, rtOut); t = rtOut.texture;
      }
      shCopia.uniforms.t.value = rtOut.texture; renderer.setRenderTarget(null); renderer.clear(); quad.material = shCopia; renderer.render(quadCena, quadCam);
    }
    renderer.setRenderTarget(null);
  }
  const fis = (hex, met, rug, cc, extra) => new T3.MeshPhysicalMaterial(Object.assign({ color: lin(hex), metalness: met, roughness: rug, clearcoat: cc, clearcoatRoughness: 0.3, envMapIntensity: 1.0 }, extra || {}));
  // canvas utilitário
  function canvas(w, h, f) { const c = document.createElement('canvas'); c.width = w; c.height = h || w; const g = c.getContext('2d'); f(g, c); return c; }
  // normal map a partir de um canvas de altura (branco = alto)
  function normalDe(cAlt, forca) {
    const w = cAlt.width, h = cAlt.height, src = cAlt.getContext('2d').getImageData(0, 0, w, h).data;
    return canvas(w, h, (g) => {
      const im = g.createImageData(w, h), d = im.data;
      const a = (x, y) => src[4 * (Math.min(h - 1, Math.max(0, y)) * w + Math.min(w - 1, Math.max(0, x)))] / 255;
      for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
        const gx = (a(x + 1, y) - a(x - 1, y)) * forca, gy = (a(x, y + 1) - a(x, y - 1)) * forca, n = Math.hypot(gx, gy, 1), k = 4 * (y * w + x);
        d[k] = 255 * (0.5 - 0.5 * gx / n); d[k + 1] = 255 * (0.5 + 0.5 * gy / n); d[k + 2] = 255 * (0.5 + 0.5 / n); d[k + 3] = 255;
      }
      g.putImageData(im, 0, 0);
    });
  }
  return { T3, PI, W, H, cl, lin, renderer, scene, gl2, ambiente, chave, contra, sol, amb, posicionaCamera, projeta, render, brilho, fis, canvas, normalDe,
           get cam() { return cam; } };
})();
