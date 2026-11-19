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
