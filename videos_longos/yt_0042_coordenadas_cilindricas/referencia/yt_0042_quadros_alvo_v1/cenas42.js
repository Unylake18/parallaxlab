// ===== Cenas 3D-alvo do 3.5-T3 (coordenadas cilíndricas) =====
// cyl(s,θ,z) → cartesianas; WC = no mundo (× SC)
const cyl=(s,t,z)=>[s*Math.cos(t),s*Math.sin(t),z];
const WC=(s,t,z)=>Wp(...cyl(s,t,z));
const bolinha=(p,cor,r=.055)=>{const b=new T.Mesh(new T.SphereGeometry(r,20,12),new T.MeshBasicMaterial({color:C(cor)}));b.position.set(...p);S.add(b);return b;};
const RMAX=Math.SQRT2, corR=(s,z)=>corDens(Math.sqrt(s*s+z*z)/RMAX);
// lata em traço: dois círculos + verticais a cada 30°
function lataTraco(R=1,Hh=1,{cor=GEO,w=.008,nv=12,t0=0,t1=2*PI,cv=TR}={}){for(const z of [0,Hh])tubo(arco(t=>WC(R,t,z),t0,t1,120),w,cor);
 for(let k=0;k<nv;k++){const t=2*PI*k/nv;if(t<t0-1e-9||t>t1+1e-9)continue;tubo([WC(R,t,0),WC(R,t,Hh)],w*.6,cv);}}
// célula cilíndrica s∈[s1,s2], θ∈[t1,t2], z∈[z1,z2]
function celC(s1,s2,t1,t2,z1,z2,cor=LI,{w=.010,borda=LI,fill=true}={}){
 if(fill){const fc=n=>tom(cor,n,.40,.45);
  sup((t,z)=>WC(s2,t,z),t1,t2,z1,z2,10,4,(t,z)=>fc([Math.cos(t),Math.sin(t),0]));
  if(s1>1e-6)sup((t,z)=>WC(s1,t,z),t1,t2,z1,z2,10,4,()=>mixc(BG,cor,.30));
  for(const z of [z1,z2])sup((s,t)=>WC(s,t,z),s1,s2,t1,t2,4,10,()=>fc([0,0,z===z2?1:-1]));
  for(const t of [t1,t2])sup((s,z)=>WC(s,t,z),s1,s2,z1,z2,3,3,()=>fc(t===t1?[Math.sin(t),-Math.cos(t),0]:[-Math.sin(t),Math.cos(t),0]));}
 for(const s of [s1,s2])for(const z of [z1,z2])if(s>1e-6)tubo(arco(t=>WC(s,t,z),t1,t2,24),w,borda);
 for(const t of [t1,t2])for(const z of [z1,z2])tubo([WC(s1,t,z),WC(s2,t,z)],w,borda);
 for(const s of [s1,s2])for(const t of [t1,t2])if(s>1e-6||t===t1)tubo([WC(s,t,z1),WC(s,t,z2)],w,borda);}

// ---------- lata pesada: densidade = distância à origem, um quarto aberto (θ ∈ [−π/2, 0]) ----------
if(K==='lata'||K==='lata0'){SC=2.2;DF=1.4;const ta=-PI/2,tb=0;const dens=K==='lata';
 const cw=(s,z)=>dens?corR(s,z):mixc(BG,GEO,.30);
 sup((t,z)=>WC(1,t,z),tb,ta+2*PI,110,8,(t,z)=>dens?tom(corR(1,z),[Math.cos(t),Math.sin(t),0],.55,.40):tom(GEO,[Math.cos(t),Math.sin(t),0],.12,.20));
 sup((s,t)=>WC(s,t,1),0,1,tb,ta+2*PI,24,90,(s,t)=>dens?mixc(BG,corR(s,1).getStyle?'#000':'#000',0).copy(corR(s,1)).lerp(C(BR),.06):mixc(BG,GEO,.30));
 for(const t of [ta,tb])sup((s,z)=>WC(s,t,z),0,1,0,1,30,30,(s,z)=>dens?corR(s,z):mixc(BG,GEO,.20));
 for(const z of [0,1])tubo(arco(t=>WC(1,t,z),tb,ta+2*PI,120),.009,dens?CI:GEO);
 for(const z of [0,1])tubo(arco(t=>WC(1,t,z),ta,tb,40),.005,TR);
 tubo([WC(1,ta,0),WC(1,ta,1)],.005,TR);
 for(const t of [ta,tb])tubo([WC(0,t,0),WC(1,t,0),WC(1,t,1),WC(0,t,1)],.009,dens?CI:GEO);
 if(dens)for(const r of [.5,1])for(const t of [ta,tb])tubo(arco(a=>{const s=r*Math.cos(a),z=r*Math.sin(a);return WC(s,t,z);},0,PI/2,40).filter(p=>true),.004,'#1E5C7A');
 tubo([Wp(0,0,0),Wp(0,0,1.45)],.010,EZ);
 seta([SC*1.03,0,0],[SC*1.55,0,0],.012,E1);seta([0,SC*1.03,0],[0,SC*1.55,0],.012,E2);
 ver([9.2,-6.2,5.8],[0,0,.45],600,560);
 proj('ex',[SC*1.68,0,0]);proj('ey',[0,SC*1.68,0]);proj('ez',Wp(0,0,1.55));proj('O',[0,0,0]);proj('fundo',Wp(.08,0,.08));
 proj('quina',WC(1,tb,1));proj('quinaB',WC(1,ta,1));proj('faceA',WC(.5,tb,.5));proj('faceB',WC(.5,ta,.5));proj('parede',WC(1,PI*.65,.5));proj('tampa',WC(.55,PI*.6,1));}

// ---------- grade da lata: lata em traço, a casca s = 0,5, duas células (eixo e parede) ----------
if(K==='grade'||K==='superf'){SC=2.2;DF=1.4;
 lataTraco(1,1,{nv:12});
 tubo([Wp(0,0,-.1),Wp(0,0,1.45)],.010,EZ);
 if(K==='grade'){for(const z of [0,.5,1])tubo(arco(t=>WC(.5,t,z),0,2*PI,90),.005,'#4A4F78');tubo(arco(t=>WC(1,t,.5),0,2*PI,90),.005,'#4A4F78');}
 if(K==='superf'){sup((t,z)=>WC(.5,t,z),0,2*PI,0,1,72,4,(t,z)=>tom(SOMB,[Math.cos(t),Math.sin(t),0],.30,.25));
  const tp=PI*.15;sup((s,z)=>WC(s,tp,z),0,1,0,1,4,4,()=>mixc(BG,TH,.30));tubo([WC(0,tp,0),WC(1,tp,0),WC(1,tp,1),WC(0,tp,1)],.008,TH);
  sup((s,t)=>WC(s,t,.5),0,1,0,2*PI,6,72,()=>mixc(BG,EZ,.26));tubo(arco(t=>WC(1,t,.5),0,2*PI,96),.008,EZ);
  proj('cil',WC(.5,-PI*.35,.8));proj('pag',WC(.75,tp,.85));proj('andar',WC(.85,-PI*.15,.5));}
 const e1=-PI*.47,e2=e1+PI/6,p1=-PI*.13,p2=p1+PI/6;
 if(K==='grade'){celC(0,.5,e1,e2,.5,1);celC(.5,1,p1,p2,.5,1);}
 ver([9.2,-6.2,5.8],[0,0,.45],600,560);
 proj('celEixo',WC(.30,(e1+e2)/2,1.0));proj('celPar',WC(.8,(p1+p2)/2,1.0));proj('celEixoIn',WC(.25,(e1+e2)/2,.75));proj('celParIn',WC(.75,(p1+p2)/2,.75));
 proj('ez',Wp(0,0,1.55));proj('O',[0,0,0]);}

// ---------- ponto P = (s, θ, z) = (2, π/3, 3/2) ----------
if(K==='ponto'){SC=1.05;DF=1.3;const s0=2,t0=PI/3,z0=1.5,P=cyl(s0,t0,z0),P1=[P[0],P[1],0],Pz=[0,0,z0];
 for(const rr of [.5,1,1.5,2])tubo(arco(a=>Wp(rr*Math.cos(a),rr*Math.sin(a),0),0,2*PI,96),.0045,'#3A3470');
 for(let k=0;k<12;k++){const a=2*PI*k/12;tubo([Wp(0,0,0),Wp(2*Math.cos(a),2*Math.sin(a),0)],.0045,'#3A3470');}
 seta([0,0,0],[SC*2.3,0,0],.013,E1);seta([0,0,0],[0,SC*2.6,0],.013,E2);seta([0,0,0],[0,0,SC*2.2],.013,EZ);
 proj('ex',[SC*2.45,0,0]);proj('ey',[0,SC*2.75,0]);proj('ez',[0,0,SC*2.35]);
 sup((a,b)=>Wp(...[0,1,2].map(i=>a*(P1[i]*(1-b)+P[i]*b))),0,1,0,1,4,4,()=>mixc(BG,TH,.16));     // triângulo O, P1, P (a página)
 tubo([Wp(0,0,0),Wp(...P1)],.016,SOMB);                 // s no chão
 tracejado([Wp(...P1),Wp(...P)],.011,EZ);               // altura z
 tubo([Wp(0,0,0),Wp(...Pz)],.016,EZ);                  // z no eixo
 tracejado([Wp(...Pz),Wp(...P)],.011,SOMB,.10,.07);     // o fio horizontal: distância ao eixo
 tubo([Wp(0,0,0),Wp(...P)],.009,RO);                    // r (hipotenusa)
 tubo(arco(a=>Wp(.8*Math.cos(a),.8*Math.sin(a),0),0,t0,40),.012,TH);
 tracejado([Wp(...P1),Wp(P[0],0,0)],.006,E1,.08,.07);tracejado([Wp(...P1),Wp(0,P[1],0)],.006,E2,.08,.07);
 bolinha(Wp(...P),BR,.07);bolinha(Wp(...P1),SOMB,.045);bolinha([0,0,0],GEO,.04);
 ver([8.2,2.4,4.8],[.5,.95,.8],560,600);
 proj('P',Wp(...P));proj('P1',Wp(...P1));proj('O',[0,0,0]);proj('meioS',Wp(P1[0]/2,P1[1]/2,0));proj('meioFio',Wp(P[0]/2,P[1]/2,z0));proj('meioZ',Wp(P[0],P[1],z0/2));
 proj('arcoTh',Wp(1.0*Math.cos(t0/2),1.0*Math.sin(t0/2),0));proj('Pz',Wp(...Pz));proj('meioR',Wp(P[0]*.45,P[1]*.45,z0*.45));proj('xP',Wp(P[0],0,0));proj('yP',Wp(0,P[1],0));}

// ---------- caixa no espaço (s, θ, z) e a lata em traço com a mesma célula ----------
const CX=(s,t,z)=>Wp(1.6*s,2.4*t/(2*PI),1.2*z);
if(K==='caixa'){SC=1;DF=1.35;
 const f=(a,b,c)=>CX(a,b,c);
 sup((t,z)=>f(0,t,z),0,2*PI,0,1,2,2,()=>mixc(BG,AL,.22));   // face s = 0 (ruim: vira o eixo)
 for(const t of [2*PI])sup((s,z)=>f(s,t,z),0,1,0,1,2,2,()=>mixc(BG,AL,.16));  // θ = 0 só em traço: não esconde o eixo θ  // faces θ = 0 e 2π (coladas)
 sup((s,t)=>f(s,t,0),0,1,0,2*PI,2,2,()=>mixc(BG,GEO,.14));
 for(const z of [.25,.5,.75])tubo([f(1,0,z),f(1,2*PI,z)],.004,'#4A4F78');
 for(let k=1;k<12;k++)tubo([f(1,2*PI*k/12,0),f(1,2*PI*k/12,1)],.004,'#4A4F78');
 const E=[[0,0,0],[1,0,0],[1,2*PI,0],[0,2*PI,0],[0,0,1],[1,0,1],[1,2*PI,1],[0,2*PI,1]];
 for(const [a,b] of [[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]])tubo([f(...E[a]),f(...E[b])],.008,GEO);
 tracejado([f(0,0,0),f(0,2*PI,0),f(0,2*PI,1),f(0,0,1),f(0,0,0)],.011,AL,.08,.06);
 for(const t of [0,2*PI])tracejado([f(0,t,0),f(1,t,0),f(1,t,1),f(0,t,1)],.011,AL,.08,.06);
 celC(0,0,0,0,0,0,LI,{fill:false,w:0});
 // célula lima: s∈[.5,1], θ∈[π/3,π/2], z∈[.5,1] (caixa reta no espaço dos endereços)
 const c1=[.5,PI/3,.5],c2=[1,PI/2,1];const V8=[];for(const a of [c1[0],c2[0]])for(const b of [c1[1],c2[1]])for(const c of [c1[2],c2[2]])V8.push([a,b,c]);
 for(const [nrm,fx] of [[[1,0,0],p=>p[0]===1],[[0,0,1],p=>p[2]===1],[[0,-1,0],p=>p[1]===PI/3]]){const q=V8.filter(fx);sup((u,v)=>{const A=q[0],B=q[1],D=q[2];return f(...[0,1,2].map(i=>A[i]+(B[i]-A[i])*u+(D[i]-A[i])*v));},0,1,0,1,1,1,()=>tom(LI,nrm,.40,.45));}
 for(let i=0;i<8;i++)for(let j=i+1;j<8;j++){const d=[0,1,2].filter(k=>V8[i][k]!==V8[j][k]);if(d.length===1)tubo([f(...V8[i]),f(...V8[j])],.009,LI);}
 seta(f(0,0,0),f(1.35,0,0),.012,SOMB);seta(f(0,0,0),f(0,2*PI*1.15,0),.012,TH);seta(f(0,0,0),f(0,0,1.35),.012,EZ);
 DF=.95;ver([7.4,-6.6,5.2],[.8,1.2,.6],600,560);
 proj('eS',f(1.45,0,0));proj('eT',f(0,2*PI*1.22,0));proj('eZ',f(0,0,1.45));proj('um_s',f(.5,0,-.1));proj('dois_pi',f(0,PI,-.12));proj('um_z',f(0,0,.5));
 proj('cel',f(1,(PI/3+PI/2)/2,1));proj('face0',f(0,PI*1.2,.5));proj('faceT0',f(.5,0,.5));proj('faceT2',f(.5,2*PI,.5));proj('O',f(0,0,0));}
if(K==='latagrade'){SC=2;DF=1.4;
 lataTraco(1,1,{nv:12});for(const z of [.5])tubo(arco(t=>WC(1,t,z),0,2*PI,90),.004,'#4A4F78');for(const z of [0,.5,1])tubo(arco(t=>WC(.5,t,z),0,2*PI,90),.004,'#4A4F78');
 tubo([Wp(0,0,0),Wp(0,0,1)],.016,AL);tubo([Wp(0,0,1),Wp(0,0,1.4)],.009,EZ);   // o eixo (s = 0) em alerta
 tracejado([WC(0,0,0),WC(1,0,0),WC(1,0,1),WC(0,0,1)],.012,AL,.08,.06);         // a costura θ = 0 = 2π
 sup((s,z)=>WC(s,0,z),0,1,0,1,2,2,()=>mixc(BG,AL,.18));
 celC(.5,1,PI/3,PI/2,.5,1);
 ver([9.2,-6.2,5.8],[0,0,.45],600,560);
 proj('cel',WC(.8,PI*.42,1.05));proj('eixo',Wp(0,0,.5));proj('costura',WC(.7,0,.5));proj('ez',Wp(0,0,1.5));proj('O',[0,0,0]);}

// ---------- caixinha: zoom numa célula da parede; arestas a partir do canto (s2, θ1, z1) ----------
if(K==='caixinha'){SC=3.2;DF=1.25;const s1=.55,s2=1,t1=-PI*.30,t2=t1+PI/6,z1=.35,z2=.8;
 celC(s1,s2,t1,t2,z1,z2,LI,{w:.008});
 tubo(arco(t=>WC(s2,t,z1),t1,t2,30),.020,TH);           // aresta 2: s Δθ (arco)
 tubo([WC(s2,t1,z1),WC(s1,t1,z1)],.020,SOMB);            // aresta 1: Δs
 tubo([WC(s2,t1,z1),WC(s2,t1,z2)],.020,EZ);              // aresta 3: Δz
 tracejado([Wp(0,0,z1),WC(s2,t1,z1)],.008,SOMB,.06,.05);tracejado([Wp(0,0,z1),WC(s2,t2,z1)],.008,SOMB,.06,.05);
 tubo(arco(t=>WC(.18,t,z1),t1,t2,20),.008,TH);
 tubo([Wp(0,0,-.05),Wp(0,0,1.15)],.010,EZ);
 lataTraco(1,1,{nv:24,t0:-PI*.75,t1:PI*.25,w:.005,cor:'#4A4F78',cv:'#3A3470'});
 bolinha(WC(s2,t1,z1),BR,.03);
 {const tc=Wp(.62,-.50,.58);DF=1;ver([tc[0]-2.5,tc[1]-11.5,tc[2]+8.5],tc,560,600);}
 proj('dS',WC((s1+s2)/2,t1,z1));proj('arco',WC(s2,(t1+t2)/2,z1));proj('dZ',WC(s2,t1,(z1+z2)/2));proj('raio',WC(s2*.5,t1,z1));proj('ang',WC(.25,(t1+t2)/2,z1));
 proj('canto',WC(s2,t1,z1));proj('ez',Wp(0,0,1.22));}

// ---------- cilindro de raio R e altura h (teste) ----------
if(K==='cilindro'||K==='cilindroRot'){SC=1.9;DF=1.4;const Hh=1.4;
 sup((t,z)=>WC(1,t,z),0,2*PI,0,Hh,96,4,(t,z)=>tom(GEO,[Math.cos(t),Math.sin(t),0],.10,.18));
 sup((s,t)=>WC(s,t,Hh),0,1,0,2*PI,8,72,()=>mixc(BG,GEO,.26));
 const cb=K==='cilindroRot'?AL:GEO;for(const z of [0,Hh])tubo(arco(t=>WC(1,t,z),0,2*PI,120),K==='cilindroRot'?.014:.009,cb);
 if(K==='cilindroRot')for(const t of [PI*.62,-PI*.28])tubo([WC(1,t,0),WC(1,t,Hh)],.012,AL);
 tubo([WC(0,0,Hh),WC(1,-PI*.20,Hh)],.016,SOMB);
 tubo([WC(1,-PI*.47,0),WC(1,-PI*.47,Hh)],.016,EZ);
 tubo([Wp(0,0,-.1),Wp(0,0,Hh+.35)],.010,EZ);
 ver([9.2,-6.2,5.0],[0,0,.65],600,560);
 proj('R',WC(.5,-PI*.20,Hh));proj('h',WC(1,-PI*.47,Hh/2));proj('ez',Wp(0,0,Hh+.45));proj('rotulo',WC(1,-PI*.05,Hh*.5));}

// ---------- o meio cilindro fora do eixo: (x−1)² + y² ≤ 1, y ≥ 0, 0 ≤ z ≤ x + y ----------
const DX=(s,t,z)=>Wp(1+s*Math.cos(t),s*Math.sin(t),z);
const teto=(s,t)=>1+s*Math.cos(t)+s*Math.sin(t);
if(K==='deslocado'||K==='deslocadoSonda'){SC=1.3;DF=1.0;
 for(const rr of [.5,1,1.5,2,2.5])tubo(arco(a=>Wp(rr*Math.cos(a),rr*Math.sin(a),0),-PI*.1,PI*.6,60),.004,'#3A3470');
 sup((s,t)=>DX(s,t,0),0,1,0,PI,6,48,()=>mixc(BG,AZC,.22));                                   // a sombra no chão
 const solido=K==='deslocado';
 if(solido){sup((t,z)=>DX(1,t,z*teto(1,t)),0,PI,0,1,60,6,(t,z)=>tom(GEO,[Math.cos(t),Math.sin(t),0],.18,.25));   // parede curva
 sup((xx,z)=>Wp(xx,0,z*xx),0,2,0,1,6,6,()=>tom(GEO,[0,-1,0],.16,.30));                       // face y = 0 (triângulo)
 sup((s,t)=>DX(s,t,teto(s,t)),0,1,0,PI,8,48,()=>tom(EZ,[-.5,-.5,.7],.32,.30));}              // o telhado z = x + y
 else{for(let k=1;k<6;k++){const t=PI*k/6;tubo([DX(1,t,0),DX(1,t,teto(1,t))],.005,TR);}
  for(const ss of [.5])tubo(arco(t=>DX(ss,t,teto(ss,t)),0,PI,60),.005,'#3F6FB0');for(let k=1;k<6;k++){const t=PI*k/6;tubo(arco(q=>DX(q,t,teto(q,t)),0,1,10),.005,'#3F6FB0');}}
 tubo(arco(t=>DX(1,t,teto(1,t)),0,PI,80),.009,EZ);tubo([Wp(0,0,0),Wp(2,0,2)],.009,EZ);
 tubo(arco(t=>DX(1,t,0),0,PI,80),.008,GEO);tubo([Wp(0,0,0),Wp(2,0,0)],.008,GEO);tubo([Wp(2,0,0),Wp(2,0,2)],.008,GEO);
 tracejado([Wp(1,0,0),Wp(1,0,3.0)],.009,BR,.10,.07);   // o eixo novo x = 1
 seta([0,0,0],[SC*2.6,0,0],.012,E1);seta([0,0,0],[0,SC*1.6,0],.012,E2);seta([0,0,0],[0,0,SC*3.0],.012,EZ);
 proj('ex',[SC*2.72,0,0]);proj('ey',[0,SC*1.72,0]);proj('ez',[0,0,SC*3.12]);
 bolinha(Wp(1,0,0),BR,.045);
 if(K==='deslocadoSonda'){const ss=.6,tt=PI*.55,pb=DX(ss,tt,0),pt=DX(ss,tt,teto(ss,tt));tracejado([Wp(...[pb[0]/SC,pb[1]/SC,-.25].map(v=>v)),pb],.010,AZC,.06,.05);
  tubo([pb,pt],.013,RO);tracejado([pt,DX(ss,tt,teto(ss,tt)+.35)],.010,CORAL,.06,.05);bolinha(pb,AZC,.045);bolinha(pt,CORAL,.045);proj('entra',pb);proj('sai',pt);}
 {const tc=Wp(1.0,.5,.95);ver([tc[0]+7.5,tc[1]-11,tc[2]+10],tc,600,600);}
 proj('polo',Wp(1,0,0));proj('eixoNovo',Wp(1,0,3.05));proj('telhado',DX(.55,PI*.35,teto(.55,PI*.35)));proj('parede',DX(1,PI*.62,.5));proj('sombra',DX(.6,PI*.75,0));proj('face0',Wp(1.45,0,.45));proj('O',[0,0,0]);proj('dois',Wp(2,0,0));}

// ---------- girar a lata (S2): lata em traço, eixo, seta de giro, célula na parede com o fio s ----------
if(K==='giro'){SC=2.2;DF=1.4;
 lataTraco(1,1,{nv:12});
 tubo([Wp(0,0,-.25),Wp(0,0,1.6)],.016,EZ);
 const A=arco(t=>Wp(.32*Math.cos(t),.32*Math.sin(t),1.38),-PI*.9,PI*.55,60);tubo(A,.010,GEO);
 const a1=Wp(.32*Math.cos(PI*.55),.32*Math.sin(PI*.55),1.38),a0=Wp(.32*Math.cos(PI*.48),.32*Math.sin(PI*.48),1.38);seta(a0,a1,.010,GEO);
 const t1=-PI*.18,t2=t1+PI/10;celC(.85,1,t1,t2,.45,.65);
 tracejado([Wp(0,0,.55),WC(.85,(t1+t2)/2,.55)],.010,SOMB,.07,.05);
 ver([9.2,-6.2,5.8],[0,0,.45],600,560);
 proj('cel',WC(1.04,(t1+t2)/2,.55));proj('fio',WC(.45,(t1+t2)/2,.55));proj('giro',Wp(.32,0,1.38));proj('ez',Wp(0,0,1.7));}
