// Renderer HDR/PBR, ambiente, câmera e bloom portados de mesa.js do yt_0024.
(function () {
  const T3 = THREE, PI = Math.PI, W = innerWidth, H = innerHeight;
  const cl = (x, a, b) => Math.min(b, Math.max(a, x));
  const lin = hex => new T3.Color(hex).convertSRGBToLinear();
  const renderer = new T3.WebGLRenderer({ antialias: false, alpha: true, preserveDrawingBuffer: true, premultipliedAlpha: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H); renderer.setClearColor(0x000000, 0);
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = T3.PCFShadowMap;
  renderer.outputEncoding = T3.LinearEncoding; renderer.toneMapping = T3.NoToneMapping;
  renderer.autoClear = false;
  document.body.appendChild(renderer.domElement);
  const gl2 = renderer.capabilities.isWebGL2;
  const scene = new T3.Scene();
  const K_PX = H / 9;                                  // px por unidade Manim

  // ── ambiente azul-espacial (softbox branca em cima, faixa fria ciano à esquerda, reflexo magenta baixo no horizonte) ──
  {
    const s = new T3.Scene();
    const g = new T3.SphereGeometry(50, 64, 32), cor = [], pos = g.attributes.position;
    const c0 = lin('#081230'), c1 = lin('#1B3263');
    for (let i = 0; i < pos.count; i++) { const u = cl((pos.getZ(i) / 50 + 0.3) / 1.3, 0, 1); const c = c0.clone().lerp(c1, u); cor.push(c.r, c.g, c.b); }
    g.setAttribute('color', new T3.Float32BufferAttribute(cor, 3));
    s.add(new T3.Mesh(g, new T3.MeshBasicMaterial({ vertexColors: true, side: T3.BackSide })));
    const painel = (w, h, hex, int, x, y, z) => {
      const m = new T3.Mesh(new T3.PlaneGeometry(w, h), new T3.MeshBasicMaterial({ color: lin(hex).multiplyScalar(int), side: T3.DoubleSide }));
      m.position.set(x, y, z); m.lookAt(0, 0, 0); s.add(m);
    };
    painel(34, 34, '#F5F7FF', 0.42, 18, 24, 32);        // softbox grande em cima (fora do zênite: a vista de cima reflete o céu escuro)
    painel(10, 40, '#35D9FF', 1.6, -38, 0, 14);        // faixa fria à esquerda
    painel(60, 5, '#EA63FF', 0.9, 0, 40, 2);           // magenta baixo no horizonte
    painel(60, 5, '#EA63FF', 0.5, 0, -40, 2);
    scene.environment = new T3.PMREMGenerator(renderer).fromScene(s, 0.02).texture;
  }

  // ── luzes: chave (cima à direita) e contraluz fria, presas à câmera; sol de cima só para a sombra de contato ──
  const chave = new T3.DirectionalLight(0xffffff, 2.2), contra = new T3.DirectionalLight(lin('#8CC8FF'), 1.2);
  const alvoL = new T3.Object3D(); scene.add(alvoL); chave.target = alvoL; contra.target = alvoL;
  const sol = new T3.DirectionalLight(0xffffff, 0.35);
  sol.position.set(1.4, -1.1, 2.2); sol.castShadow = true;
  sol.shadow.mapSize.set(2048, 2048); sol.shadow.radius = 3; sol.shadow.bias = -0.0004; sol.shadow.normalBias = 0.0015;
  Object.assign(sol.shadow.camera, { left: -1.6, right: 1.6, top: 1.6, bottom: -1.6, near: .1, far: 7 });
  scene.add(chave, contra, sol, sol.target, new T3.AmbientLight(0xffffff, 0.06));

  const fis=(hex,met,rough,cc=0.35)=>new T3.MeshPhysicalMaterial({color:lin(hex),metalness:met,roughness:rough,clearcoat:cc,envMapIntensity:1.0});
  const estrut=fis('#7D899E',.6,.4), polido=fis('#7A8696',.92,.22,.6), massa=fis('#A9B5CC',.35,.36), rosa=fis('#FF7EB6',.2,.45), liga=fis('#AEB7C4',.95,.18), claro=fis('#C9D2DE',.85,.3);
  const haste=fis('#C6D1E4',.22,.3,.5);haste.emissive=lin('#5D7FB5');haste.emissiveIntensity=.16;const colunaH=fis('#9CA9C0',.3,.4,.3);colunaH.emissive=lin('#44648F');colunaH.emissiveIntensity=.12;
  const PRETO=new T3.MeshBasicMaterial({color:0x000000}), brilho=[];
  const geoMat=new T3.ShaderMaterial({uniforms:{cor:{value:lin('#B8C4DA')},op:{value:.10},borda:{value:.35}},transparent:true,side:T3.DoubleSide,depthWrite:false,vertexShader:'varying vec3 n,v;void main(){vec4 p=modelViewMatrix*vec4(position,1.0);n=normalize(normalMatrix*normal);v=-p.xyz;gl_Position=projectionMatrix*p;}',fragmentShader:'uniform vec3 cor;uniform float op,borda;varying vec3 n,v;void main(){float f=pow(1.0-abs(dot(normalize(n),normalize(v))),3.0);gl_FragColor=vec4(cor,op+borda*f);}'});geoMat.userData.fantasma=true;
  function mesh(g,m,p,par){const o=new T3.Mesh(g,m);if(p)o.position.set(...p);o.castShadow=o.receiveShadow=true;(par||scene).add(o);return o;}
  function tubo(a,b,r,m,par){const A=new T3.Vector3(...a),B=new T3.Vector3(...b),d=B.clone().sub(A);const o=mesh(new T3.CylinderGeometry(r,r,d.length(),24),m,A.clone().add(B).multiplyScalar(.5).toArray(),par);o.quaternion.setFromUnitVectors(new T3.Vector3(0,1,0),d.normalize());return o;}
  function disco(r,h,z,m,par){const o=mesh(new T3.CylinderGeometry(r,r,h,64),m,[0,0,z],par);o.rotation.x=PI/2;return o;}
  function esfera(r,par){const g=new T3.Group();par.add(g);mesh(new T3.SphereGeometry(r,40,24),massa,[0,0,0],g);const an=mesh(new T3.SphereGeometry(r+.0004,48,8,0,2*PI,PI/2-.12,.24),rosa,[0,0,0],g);an.rotation.x=PI/2;return g;}
  function anel(r,t,p,m,par){return mesh(new T3.TorusGeometry(r,t,10,80),m,p,par);}
  const raizes={};function raiz(n){const g=new T3.Group();scene.add(g);raizes[n]=g;return g;}
  const gaiolas=[];
  function mancal(z,par){const g=new T3.Group();g.position.z=z;par.add(g);disco(.068,.025,0,estrut,g);disco(.047,.032,.002,polido,g);disco(.025,.036,.004,estrut,g);const gg=new T3.Group();g.add(gg);for(let k=0;k<12;k++){let a=k*PI/6;mesh(new T3.SphereGeometry(.008,16,12),claro,[.036*Math.cos(a),.036*Math.sin(a),.021],gg);}anel(.056,.006,[0,0,.019],polido,g);anel(.022,.004,[0,0,.025],polido,g);gaiolas.push(gg);return g;}
  function bancada(par,mb){const bg=new T3.Group();par.add(bg);disco(.30,.05,-1.05,mb||estrut,bg);disco(.115,.18,-.94,polido,bg);tubo([0,0,-.9],[0,0,-.4],.039,colunaH,bg);for(const z of [-.45,-.85]){mancal(z,bg);tubo([-.13,.05,z],[.13,.05,z],.012,polido,bg);}tubo([0,0,-.95],[0,0,-.36],.012,haste,bg);tubo([0,0,-.36],[0,0,.04],.012,haste,par);disco(.03,.055,0,polido,par);return bg;}
  const chao=mesh(new T3.PlaneGeometry(5,5),new T3.ShadowMaterial({opacity:.32}),[0,0,-1.08]);chao.receiveShadow=true;
  // Pêndulo: pórtico de 30 mm; olhal 8 mm; fio 1,2 mm.
  const pe=raiz('pendulo_conico');
  for(const x of [-.8,.8]){tubo([x,0,-1.05],[x,0,.05],.015,estrut,pe);mesh(new T3.BoxGeometry(.15,.18,.025),estrut,[x,0,-1.05],pe);}
  tubo([-.8,0,.05],[.8,0,.05],.015,estrut,pe);
  const ol=anel(.008,.002,[0,0,0],polido,pe);ol.rotation.x=PI/2;
  const discoPe=disco(.62,.006,-1.064,fis('#2A3A5E',.1,.9,0),pe);
  const bol=esfera(.035,pe), fio=tubo([0,0,0],[.5,0,-Math.sqrt(.75)],.0012,fis('#F2EEE6',0,.85,0),pe);
  const cone=mesh(new T3.ConeGeometry(.5,Math.sqrt(.75),96,1,true),geoMat.clone(),[0,0,-Math.sqrt(.75)/2],pe);cone.rotation.x=PI/2;cone.material.uniforms.op.value=.08;
  // Batata e haltere compartilham a mesma bancada, cada qual numa raiz independente.
  const vo=raiz('corpo_voxel');const contextoV=new T3.Group();vo.add(contextoV);const bgV=bancada(contextoV);const vr=new T3.Group();vo.add(vr);
  const vt=window.FISICA25.voxel,nvxl=vt.posicoes.length;
  const acoVox=fis('#AEBCD6',.3,.5,.2);acoVox.emissive=lin('#4E6A98');acoVox.emissiveIntensity=.2;const cubos=new T3.InstancedMesh(new T3.BoxGeometry(.03,.03,.03),acoVox,nvxl);cubos.castShadow=cubos.receiveShadow=true;vr.add(cubos);
  const mat4=new T3.Matrix4();vt.posicoes.forEach((p,i)=>{mat4.makeTranslation(...p);cubos.setMatrixAt(i,mat4);cubos.setColorAt(i,new T3.Color(.75+.25*vt.ao[i],.75+.25*vt.ao[i],.75+.25*vt.ao[i]));});cubos.instanceMatrix.needsUpdate=true;
  const cuboRosa=mesh(new T3.BoxGeometry(.0306,.0306,.006),rosa,vt.posicoes[vt.destaque],vr);
  const ondaCubos=new T3.InstancedMesh(new T3.BoxGeometry(.0304,.0304,.0304),rosa,nvxl);for(let i=0;i<nvxl;i++)ondaCubos.setColorAt(i,new T3.Color(1,1,1));ondaCubos.count=0;ondaCubos.visible=false;vr.add(ondaCubos);
  const ha=raiz('haltere_torto');const bgH=bancada(ha);const hr=new T3.Group();ha.add(hr);
  const rr=[.15,0,.3*Math.cos(PI/6)],rr2=rr.map(x=>-x);
  tubo(rr2,rr,.011,haste,hr);const es1=esfera(.045,hr),es2=esfera(.045,hr);es1.position.set(...rr);es2.position.set(...rr2);
  for(const es of [es1,es2]){es.children[0].material=massa.clone();es.children[0].material.emissive=lin('#FF7EB6');es.children[0].material.emissiveIntensity=0;}
  const hx=new T3.Group();hr.add(hx);const xr=[-.15,0,rr[2]],xr2=xr.map(x=>-x);tubo(xr2,xr,.011,haste,hx);esfera(.045,hx).position.set(...xr);esfera(.045,hx).position.set(...xr2);
  const plano=mesh(new T3.PlaneGeometry(.42,.42),geoMat.clone(),[0,0,0],hr);plano.rotation.x=PI/2;
  // Hook v2: duas bancadas idênticas (haltere reto α = 90° e torto α = 30°), mesmo motor, mesma rotação; a base do torto balança sobre pés de borracha.
  const bd=raiz('bancada_dupla'),AZD=35*PI/180,dirD=[-Math.sin(AZD),Math.cos(AZD),0],bdPivo=[],bdHr=[],PE_Z=-1.115;
  const borrachaPe=fis('#14171C',0,.92,0),baseD=fis('#566074',.12,.85,0);
  [[-.75,PI/2],[.75,PI/6]].forEach(([s_,al],i)=>{
    const piv=new T3.Group();piv.position.set(s_*dirD[0],s_*dirD[1],PE_Z);bd.add(piv);
    const corpo=new T3.Group();corpo.position.z=-PE_Z;piv.add(corpo);bancada(corpo,baseD);
    for(const [qx,qy] of [[.23,0],[-.115,.2],[-.115,-.2]])mesh(new T3.CylinderGeometry(.042,.048,.04,32),borrachaPe,[qx,qy,-1.095],corpo).rotation.x=PI/2;
    const hh=new T3.Group();corpo.add(hh);bdHr.push(hh);bdPivo.push(piv);
    const a_=[.3*Math.sin(al),0,.3*Math.cos(al)],b_=a_.map(x=>-x);tubo(b_,a_,.011,haste,hh);
    const e1=esfera(.045,hh),e2=esfera(.045,hh);e1.position.set(...a_);e2.position.set(...b_);
  });
  // Gancho v2: plataforma circular de aço sobre rolamento LIVRE; carretel central recolhe os fios das duas massas (mecanismo interno, sem torque externo).
  const pl=raiz('plataforma_livre');
  disco(.26,.05,-.88,estrut,pl);tubo([0,0,-.86],[0,0,-.075],.028,polido,pl);const rolPl=anel(.075,.014,[0,0,-.06],polido,pl);rolPl.rotation.x=PI/2;
  const pg=new T3.Group();pl.add(pg);disco(.55,.035,0,fis('#7D8DB5',.2,.55,.2),pg);mesh(new T3.BoxGeometry(.5,.045,.004),fis('#F4F6FA',0,.5,0),[.27,0,.0195],pg);for(const k of [-1,1]){mesh(new T3.BoxGeometry(.5,.045,.004),fis('#F4F6FA',0,.5,0),[0,.27*k,.0195],pg).rotation.z=PI/2;}
  for(const y of [-.022,.022])mesh(new T3.BoxGeometry(1.06,.014,.018),claro,[0,y,.027],pg);
  const carretel=new T3.Group();pg.add(carretel);disco(.06,.09,.06,claro,carretel);disco(.085,.01,.025,polido,carretel);disco(.085,.01,.095,polido,carretel);
  const fioPl=fis('#FFF6DD',0,.6,0),massasPl=[],fiosPl=[];
  for(const s_ of [-1,1]){const g=new T3.Group();pg.add(g);const m=mesh(new T3.CylinderGeometry(.09,.09,.08,40),rosa,[0,0,0],g);m.rotation.x=PI/2;const an=mesh(new T3.CylinderGeometry(.0906,.0906,.02,40),rosa,[0,0,0],g);an.rotation.x=PI/2;g.position.z=.06;massasPl.push(g);
    const f=mesh(new T3.CylinderGeometry(.009,.009,1,10),fioPl,[0,0,.06],pg);f.rotation.z=PI/2;fiosPl.push(f);}
  // Roda sem marca: pneu de perfil arredondado, banda normal procedural, liga com cinco raios e cinco porcas.
  const ro=raiz('roda_balanceamento'),wr=new T3.Group();ro.add(wr);
  const canvasN=document.createElement('canvas');canvasN.width=canvasN.height=256;const ctxN=canvasN.getContext('2d'),imN=ctxN.createImageData(256,256);for(let y=0;y<256;y++)for(let x=0;x<256;x++){const k=(y*256+x)*4,sg=((x+Math.floor(y/32)*7)%32<4)?50:0;imN.data.set([128+sg,128,250,255],k);}ctxN.putImageData(imN,0,0);const normalPneu=new T3.CanvasTexture(canvasN);normalPneu.wrapS=normalPneu.wrapT=T3.RepeatWrapping;normalPneu.repeat.set(12,1);
  const borracha=fis('#7F8CA3',0,.6,0);borracha.normalMap=normalPneu;borracha.normalScale=new T3.Vector2(.25,.25);
  // Lathe gira em torno de y: perfil radial/axial com largura 205 mm.
  const perfil=[[.203,-.1025],[.25,-.1025],[.286,-.085],[.300,-.055],[.300,.055],[.286,.085],[.25,.1025],[.203,.1025]].map(p=>new T3.Vector2(...p));
  const pneu=mesh(new T3.LatheGeometry(perfil,128),borracha,[0,0,0],wr);
  const fresnelPneu=mesh(pneu.geometry,geoMat.clone(),[0,0,0],wr);pneu.userData.translucido=fresnelPneu.userData.translucido=true;fresnelPneu.material.uniforms.op.value=0;fresnelPneu.material.uniforms.borda.value=1;fresnelPneu.castShadow=false;fresnelPneu.receiveShadow=false;
  for(const y of [-.10,.10]){const a=anel(.203,.009,[0,y,0],liga,wr);a.rotation.x=PI/2;const b=anel(.195,.0015,[0,y+.001,0],new T3.MeshBasicMaterial({color:lin('#B8C4DA')}),wr);b.rotation.x=PI/2;}
  const raios=new T3.Group();wr.add(raios);for(let k=0;k<5;k++){const a=2*PI*k/5;tubo([.045*Math.cos(a),0,.045*Math.sin(a)],[.196*Math.cos(a),0,.196*Math.sin(a)],.016,liga,raios);tubo([.032*Math.cos(a),-.035,.032*Math.sin(a)],[.032*Math.cos(a),.035,.032*Math.sin(a)],.007,polido,raios);}tubo([0,-.045,0],[0,.045,0],.047,liga,raios);
  const excessos=[],contrapesos=[];for(const s of [-1,1]){excessos.push(mesh(new T3.BoxGeometry(.075,.06,.085),rosa,[s*.20,s*.10,0],wr));contrapesos.push(mesh(new T3.BoxGeometry(.075,.06,.085),claro,[-s*.20,s*.10,0],wr));}
  tubo([0,-.4,0],[0,.4,0],.012,polido,ro);const pedMat=fis('#2E3649',.4,.55,0),baseRoda=fis('#232B3D',.3,.7,0);for(const y of [-.25,.25]){const pedG=new T3.BoxGeometry(.10,.10,.43);mesh(pedG,pedMat,[0,y,-.25],ro);const aresta=new T3.LineSegments(new T3.EdgesGeometry(pedG),new T3.LineBasicMaterial({color:lin('#B8C4DA')}));aresta.position.set(0,y,-.25);ro.add(aresta);const b=anel(.045,.014,[0,y,0],polido,ro);b.rotation.x=PI/2;}mesh(new T3.BoxGeometry(.42,.85,.035),baseRoda,[0,0,-.47],ro);
  // Caudas de 0,8 s com oito amostras por quadro; só a cabeça é HDR/bloom.
  const tails=[];for(let j=0;j<2;j++){const g=new T3.BufferGeometry();g.setAttribute('position',new T3.BufferAttribute(new Float32Array(100*3),3));g.setAttribute('color',new T3.BufferAttribute(new Float32Array(100*3),3));const m=new T3.LineBasicMaterial({vertexColors:true,transparent:true,opacity:.75});const o=new T3.Line(g,m);scene.add(o);brilho.push(o);tails.push(o);}
  const cRa=lin('#9FB4D6');
  function rastro3(e){tails.forEach((o,j)=>{o.visible=!!e.rastro&&j<(e.tipo==='haltere_torto'?2:1);if(!o.visible)return;const p=o.geometry.attributes.position.array,c=o.geometry.attributes.color.array;for(let k=0;k<100;k++){let a=e.phi-(1-k/99)*.8*(e.tipo==='pendulo_conico'?window.FISICA25.pendulo.omega:2*PI),r=e.tipo==='pendulo_conico'?.5:.15,z=e.tipo==='pendulo_conico'?-Math.sqrt(.75):rr[2],s=j?-1:1;p.set([s*r*Math.cos(a),s*r*Math.sin(a),s*z],k*3);const v=cRa.clone().multiplyScalar(k>94?1.6:Math.pow(k/99,2));c.set([v.r,v.g,v.b],k*3);}o.geometry.attributes.position.needsUpdate=o.geometry.attributes.color.needsUpdate=true;});}
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

  const depthRT=new T3.WebGLRenderTarget(W,H,{format:T3.RGBAFormat,type:T3.UnsignedByteType});
  const depthMat=new T3.MeshDepthMaterial({depthPacking:T3.RGBADepthPacking});depthMat.blending=T3.NoBlending;
  const depthPixels=new Uint8Array(W*H*4);
  let ultimo={};
  const acumulado=[mk(W,H),mk(W,H)];
  const pretoTex=new T3.DataTexture(new Uint8Array([0,0,0,255]),1,1,T3.RGBAFormat);pretoTex.needsUpdate=true;
  const mistura=new T3.ShaderMaterial({uniforms:{a:{value:null},b:{value:null},peso:{value:1}},vertexShader:VS,fragmentShader:'uniform sampler2D a,b; uniform float peso; varying vec2 vUv; void main(){gl_FragColor=mix(texture2D(a,vUv),texture2D(b,vUv),peso);}'});
  const bokeh=new T3.ShaderMaterial({uniforms:{t:{value:null},depth:{value:depthRT.texture},perto:{value:.01},longe:{value:10},foco:{value:3},forca:{value:1},pixel:{value:new T3.Vector2(1/W,1/H)}},vertexShader:VS,fragmentShader:`
    #include <packing>
    uniform sampler2D t,depth;uniform float perto,longe,foco,forca;uniform vec2 pixel;varying vec2 vUv;
    void main(){float d=unpackRGBAToDepth(texture2D(depth,vUv));float z=-perspectiveDepthToViewZ(d,perto,longe);float coc=clamp(abs(z-foco)*forca*2.5,0.0,2.4);vec2 r=pixel*coc;vec4 c=texture2D(t,vUv)*.2;for(int k=0;k<8;k++){float a=float(k)*.785398163; c+=texture2D(t,vUv+r*vec2(cos(a),sin(a)))*.1;}gl_FragColor=c;}`});
  function prepara(e){
    ultimo=e;posicionaCamera(e.cam);sol.castShadow=e.sombra!==false&&e.tipo!=='plataforma_livre';   // v6 §2.1: sem sombra no gancho (S2)
    chao.visible=e.tipo!=='plataforma_livre';Object.entries(raizes).forEach(([k,g])=>g.visible=k===e.tipo);
    const ph=e.phi||0;bol.position.set(.5*Math.cos(ph),.5*Math.sin(ph),-Math.sqrt(.75));
    fio.position.copy(bol.position).multiplyScalar(.5);fio.quaternion.setFromUnitVectors(new T3.Vector3(0,1,0),bol.position.clone().normalize());cone.visible=!!e.cone;
    // Espessura mínima de rasterização (2 px a 1080p), sem alterar a linha física do fio.
    const minRaio=H>=1080?1:0.5;const grossura=Math.max(1,minRaio/(.0012*e.cam.K*K_PX));fio.scale.set(grossura,1,grossura);
    hr.rotation.z=ph;hx.visible=(e.x||0)>0;hx.scale.setScalar(Math.max(.00001,e.x||0));plano.visible=!!e.plano;
    es1.children[0].material.emissiveIntensity=e.massafoco===1?.22:0;es2.children[0].material.emissiveIntensity=e.massafoco===2?.22:0;
    gaiolas.forEach(g=>g.rotation.z=ph*.4);
    const R=e.rotacao||vt.inicial;const m=new T3.Matrix4();m.set(R[0][0],R[0][1],R[0][2],0,R[1][0],R[1][1],R[1][2],0,R[2][0],R[2][1],R[2][2],0,0,0,0,1);vr.quaternion.setFromRotationMatrix(m);vr.scale.setScalar(e.expansao||1);cuboRosa.visible=!!e.destaque;contextoV.visible=!e.livre;bgV.visible=!e.sem_base;bgH.visible=!e.sem_base&&!(e.cam&&e.cam.el>60);
    if(e.tipo==='plataforma_livre'){pg.rotation.z=ph;const rr_=e.raio_m||.4;massasPl.forEach((g,i)=>{g.position.x=(i?-1:1)*rr_;});fiosPl.forEach((f,i)=>{f.scale.set(1,rr_,1);f.position.x=(i?-1:1)*rr_/2;});}
    if(e.tipo==='bancada_dupla'){bdHr.forEach(g=>g.rotation.z=ph);const Am=(e.tilt||0)*PI/180;bdPivo[0].quaternion.identity();bdPivo[1].quaternion.setFromAxisAngle(new T3.Vector3(-Math.sin(ph),Math.cos(ph),0),Am);}
    wr.rotation.y=ph;pneu.material.transparent=!!e.raiox;pneu.material.opacity=e.raiox?.25:1;pneu.material.depthWrite=!e.raiox;
    ondaCubos.count=0;
    if(e.onda){const rs=vt.posicoes.map(p=>Math.hypot(R[0][0]*p[0]+R[0][1]*p[1]+R[0][2]*p[2],R[1][0]*p[0]+R[1][1]*p[1]+R[1][2]*p[2]));const frente=(e.onda_u||0)*Math.max(...rs)*1.15;for(let i=0;i<nvxl;i++){if(Math.abs(rs[i]-frente)>.022)continue;mat4.makeTranslation(...vt.posicoes[i]);ondaCubos.setMatrixAt(ondaCubos.count++,mat4);}ondaCubos.instanceMatrix.needsUpdate=true;}
    ondaCubos.visible=ondaCubos.count>0;
    fresnelPneu.visible=!!e.raiox;
    contrapesos.forEach((o,i)=>{const u=e.balanceada||0;o.visible=u>0;o.position.x=(i?-.2:.2)+(1-u)*.25;o.position.z=(1-u)*.15;});
    chao.position.z=e.tipo==='roda_balanceamento'?-.49:(e.tipo==='bancada_dupla'?-1.118:(e.tipo==='plataforma_livre'?-.905:-1.08));
    rastro3(e);scene.updateMatrixWorld(true);
  }
  function desenha(e){
    renderer.setRenderTarget(rtCena);renderer.setClearColor(0x000000,0);renderer.clear();renderer.render(scene,cam);
    if(e.tipo==='roda_balanceamento'&&e.movendo&&e.motion!==false){
      // Oito exposições: somente pneu e raios se movem dentro do obturador; massas nítidas.
      const auto=renderer.shadowMap.autoUpdate;renderer.shadowMap.autoUpdate=false;
      for(let k=0;k<8;k++){
        const delta=(k/7-.5)*(1.5*PI/15)*.5;pneu.rotation.y=delta;raios.rotation.y=delta;
        renderer.setRenderTarget(rtCena);renderer.clear();renderer.render(scene,cam);
        mistura.uniforms.a.value=acumulado[(k+1)%2].texture;mistura.uniforms.b.value=rtCena.texture;mistura.uniforms.peso.value=1/(k+1);passa(mistura,acumulado[k%2]);
      }
      pneu.rotation.y=raios.rotation.y=0;renderer.shadowMap.autoUpdate=auto;
      shCopia.uniforms.t.value=acumulado[1].texture;passa(shCopia,rtCena);
    }
    let t0=pretoTex,t1=pretoTex,t2=pretoTex;
    if(e.bloom!==0){passadaBrilho();shPassa.uniforms.t.value=rtBrilho.texture;passa(shPassa,nv[0][0]);t0=blur(nv[0][0].texture,[nv[0][1],nv[0][0]],.8);t1=blur(t0,nv[1],.96);t2=blur(t1,nv[2],1.12);}
    Object.assign(shComp.uniforms,{c:{value:rtCena.texture},b0:{value:t0},b1:{value:t1},b2:{value:t2}});shComp.uniforms.forca.value=e.bloom===undefined?.40:e.bloom;
    const desf=e.desf||0;passa(shComp,desf>0?rtOut:null);
    if(desf>0){bokeh.uniforms.t.value=rtOut.texture;bokeh.uniforms.perto.value=cam.near;bokeh.uniforms.longe.value=cam.far;bokeh.uniforms.foco.value=cam.position.distanceTo(new T3.Vector3(...e.cam.alvo))*.65;bokeh.uniforms.forca.value=desf;passa(bokeh,null);}
  }
  function profundidade(){
    const old=scene.overrideMaterial;scene.overrideMaterial=depthMat;const vis=tails.map(x=>x.visible);tails.forEach(x=>x.visible=false);const cv=chao.visible;chao.visible=false;const dv=discoPe.visible;discoPe.visible=false;const pc=plano.visible,cc=cone.visible;plano.visible=cone.visible=false;
    renderer.setRenderTarget(depthRT);renderer.setClearColor(0xffffff,1);renderer.clear();renderer.render(scene,cam);renderer.readRenderTargetPixels(depthRT,0,0,W,H,depthPixels);
    scene.overrideMaterial=old;tails.forEach((x,i)=>x.visible=vis[i]);chao.visible=cv;discoPe.visible=dv;plano.visible=pc;cone.visible=cc;renderer.setRenderTarget(null);
  }
  function depthAt(x,y){const i=(Math.max(0,Math.min(H-1,Math.round(H-1-y)))*W+Math.max(0,Math.min(W-1,Math.round(x))))*4;return depthPixels[i]/(256**3)+depthPixels[i+1]/(256**2)+depthPixels[i+2]/256+depthPixels[i+3];}
  function ponto(p){const v=new T3.Vector3(...p).project(cam),view=new T3.Vector3(...p).applyMatrix4(cam.matrixWorldInverse);const px=[(v.x+1)*W/2,(1-v.y)*H/2];const z=(v.z+1)/2,d=depthAt(...px)/256;const frente=cam.isPerspectiveCamera?cam.near*cam.far/(cam.far-(cam.far-cam.near)*d):cam.near+(cam.far-cam.near)*d;return {px,depth:z,view_depth:-view.z,perspectiva:ePersp(p),oculto:-view.z>frente+.002};}
  function ePersp(p){if(cam.isOrthographicCamera)return 1;const q=new T3.Vector3(...p).applyMatrix4(cam.matrixWorldInverse),a=new T3.Vector3(...ultimo.cam.alvo).applyMatrix4(cam.matrixWorldInverse);return a.z/q.z;}
  window.setEstado=function(e){prepara(e);profundidade();desenha(e);const pts={};Object.entries(e.pontos||{}).forEach(([k,v])=>pts[k]=ponto(v));const sil=[];for(let y=0;y<H;y+=6){let lo=W,hi=-1;for(let x=0;x<W;x+=2){if(depthAt(x,y)<255.9999){lo=Math.min(lo,x);hi=x;}}if(hi>=0)sil.push([lo,y,hi,y+6]);}return {O:projeta([0,0,0]),pontos:pts,silhueta:sil,webgl2:gl2};};
  window.calibra25=function(e,ps){const g=new T3.Group();ps.forEach(p=>{const o=mesh(new T3.SphereGeometry(.009,16,12),new T3.MeshBasicMaterial({color:lin('#00FF00'),depthTest:false,depthWrite:false}),p,g);o.renderOrder=9999;});scene.add(g);window.setEstado(e);const png=renderer.domElement.toDataURL('image/png');scene.remove(g);return png;};
  window.frames25={};window.setFrame=f=>window.setEstado(window.frames25[f]);window.projeta=projeta;
  window.mascara=()=>{const cv=document.createElement('canvas');cv.width=W;cv.height=H;const cx=cv.getContext('2d'),im=cx.createImageData(W,H);for(let y=0;y<H;y++)for(let x=0;x<W;x++){const k=(y*W+x)*4,v=depthAt(x,y)<255.9999?255:0;im.data[k]=im.data[k+1]=im.data[k+2]=v;im.data[k+3]=255;}cx.putImageData(im,0,0);return cv.toDataURL('image/png');};
  window.mascaraPalco=()=>{if(ultimo.tipo!=='corpo_voxel')return window.mascara();const v=contextoV.visible;contextoV.visible=false;profundidade();const p=window.mascara();contextoV.visible=v;profundidade();return p;};
  window.mascaraTexto=()=>{const ocultos=[];scene.traverse(o=>{if(o.userData&&o.userData.translucido&&o.visible){o.visible=false;ocultos.push(o);}});if(!ocultos.length)return window.mascara();profundidade();const p=window.mascara();ocultos.forEach(o=>o.visible=true);profundidade();return p;};   // G28 v5: texto sobre superfície translúcida (pneu) não é 'sobre objeto'
  window.medidas=()=>({webgl2:gl2,W,H});window.cenaPronta=true;


})();
