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

