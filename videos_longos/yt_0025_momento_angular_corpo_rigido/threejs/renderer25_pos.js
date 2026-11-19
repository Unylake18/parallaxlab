  // ── câmeras: perspectiva (fov > 0) e ortográfica (fov = 0), as duas com o alvo em Manim (xc, yc) ──
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
      cam.near = Math.max(0.01, D - 4); cam.far = D + 6;
      cam.setViewOffset(W, H, -(c.xc || 0) / 16 * W, (c.yc || 0) / 9 * H, W, H);
    } else {
      cam = camO;
      cam.left = (-8 - (c.xc || 0)) / K; cam.right = (8 - (c.xc || 0)) / K; cam.top = (4.5 - (c.yc || 0)) / K; cam.bottom = (-4.5 - (c.yc || 0)) / K;
      cam.position.copy(al).addScaledVector(dir, 10); cam.up.copy(up); cam.lookAt(al); cam.near = 5; cam.far = 15;
    }
    cam.updateProjectionMatrix(); cam.updateMatrixWorld();
    // luz chave em cima à direita e contraluz por trás, no referencial da câmera (o contraste do disco não muda quando a câmera anda)
    const dirCam = new T3.Vector3(); cam.getWorldDirection(dirCam);
    const dir_ = dirCam.clone().negate(), dir_dir = new T3.Vector3().crossVectors(dirCam, up).normalize();
    alvoL.position.copy(al);
    chave.position.copy(al).addScaledVector(dir_, 0.6).addScaledVector(dir_dir, 2.2).addScaledVector(up, 3.2);
    contra.position.copy(al).addScaledVector(dirCam, 3).addScaledVector(up, 1.6).addScaledVector(dir_dir, -0.8);
  }
  function projeta(p) { const v = new T3.Vector3(...p).project(cam); return [(v.x + 1) / 2 * W, (1 - v.y) / 2 * H]; }

  // ── pós-processamento: HDR → (bloom seletivo) → tom com ombro + vinheta + sRGB → (desfoque opcional) → tela ──
  const opt = { type: T3.HalfFloatType, format: T3.RGBAFormat, minFilter: T3.LinearFilter, magFilter: T3.LinearFilter, depthBuffer: true };
  const rtCena = gl2 ? new T3.WebGLMultisampleRenderTarget(W, H, opt) : new T3.WebGLRenderTarget(W, H, opt);
  if (gl2) rtCena.samples = 4;
  const rtBrilho = gl2 ? new T3.WebGLMultisampleRenderTarget(W / 2, H / 2, opt) : new T3.WebGLRenderTarget(W / 2, H / 2, opt);
  if (gl2) rtBrilho.samples = 4;
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
  const shComp = new T3.ShaderMaterial({ uniforms: { c: { value: null }, b0: { value: null }, b1: { value: null }, b2: { value: null }, forca: { value: 0.40 }, vin: { value: 0.18 }, asp: { value: W / H } }, vertexShader: VS,
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
  const shCopia = new T3.ShaderMaterial({ uniforms: { t: { value: null } }, vertexShader: VS, fragmentShader: 'uniform sampler2D t; varying vec2 vUv; void main(){ gl_FragColor = texture2D(t, vUv); }', transparent: false });
  const passa = (mat, alvo) => { quad.material = mat; renderer.setRenderTarget(alvo); renderer.clear(); renderer.render(quadCena, quadCam); };
  function blur(src, par, raio) {
    const [a, b] = par, w = a.width, h = a.height;
    shBlur.uniforms.t.value = src; shBlur.uniforms.d.value.set(raio / w, 0); passa(shBlur, a);
    shBlur.uniforms.t.value = a.texture; shBlur.uniforms.d.value.set(0, raio / h); passa(shBlur, b);
    return b.texture;
  }
  const guarda = new Map();
  function passadaBrilho() {
    // o aço (e tudo que não brilha) vira oclusor preto; só o anel da bucha e o rastro ficam com o seu material
    scene.traverse(o => { if (o.isMesh && !brilho.includes(o) && !(o.material.userData && o.material.userData.fantasma)) { guarda.set(o, o.material); o.material = Array.isArray(o.material) ? o.material.map(() => PRETO) : PRETO; } });
    const env = scene.environment; scene.environment = null; const sombra = renderer.shadowMap.enabled; renderer.shadowMap.enabled = false;
    chao.visible = false;
    renderer.setRenderTarget(rtBrilho); renderer.setClearColor(0x000000, 1); renderer.clear(); renderer.render(scene, cam);
    chao.visible = true;
    guarda.forEach((m, o) => { o.material = m; }); guarda.clear();
    scene.environment = env; renderer.shadowMap.enabled = sombra;
  }

