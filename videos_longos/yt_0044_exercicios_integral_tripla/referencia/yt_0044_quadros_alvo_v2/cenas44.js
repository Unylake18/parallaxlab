// ===== Cenas 3D-alvo do 3.5-E1 · v2 (2026-11-18) · yt_0044 provisório =====
// v2 = legibilidade: piso finito com borda (G2), origem num cruzamento do papel (G8), câmera mais afastada (peça menor, nunca cortada),
// cotas desenhadas no lugar de letras soltas (G10), pontos separados ≥ 40 px (G11), sem arame redundante (G12). Opaco, tom fixo, sem luz.
const MEN_='#8CFFD2',LIL='#B9A6FF',HEL='#FFB36B',COTA='#C9D2E6';
function eixoZ(z0=-.1,z1=1.45,cor=EZ,r=.010,cx=0,cy=0){tubo([Wp(cx,cy,z0),Wp(cx,cy,z1)],r,cor);proj('ez',Wp(cx,cy,z1+.08));}
function giroSeta(cx,cy,zz,rr=.32,cor=GEO){const A=arco(t=>Wp(cx+rr*Math.cos(t),cy+rr*Math.sin(t),zz),-PI*.9,PI*.55,60);tubo(A,.010,cor);
 const a1=Wp(cx+rr*Math.cos(PI*.55),cy+rr*Math.sin(PI*.55),zz),a0=Wp(cx+rr*Math.cos(PI*.48),cy+rr*Math.sin(PI*.48),zz);seta(a0,a1,.010,cor);proj('giro',Wp(cx+rr,cy,zz));}
// cota (G10): segmento fino com dois tiques nas pontas, fora da peça; o rótulo vai no ponto 'nome' (meio, deslocado para fora)
function cota(A,B,nome,fora=[0,0,0],cor=COTA){tubo([Wp(...A),Wp(...B)],.006,cor);
 const d=[B[0]-A[0],B[1]-A[1],B[2]-A[2]],L=Math.hypot(...d);let t=[fora[0],fora[1],fora[2]];const tl=Math.hypot(...t)||1;t=t.map(v=>v/tl*.06);
 for(const P of [A,B])tubo([Wp(P[0]-t[0],P[1]-t[1],P[2]-t[2]),Wp(P[0]+t[0],P[1]+t[1],P[2]+t[2])],.006,cor);
 proj(nome,Wp((A[0]+B[0])/2+t[0]*2.2,(A[1]+B[1])/2+t[1]*2.2,(A[2]+B[2])/2+t[2]*2.2));}
function lataSolida(cx=0){const Cc=(s,t,z)=>Wp(cx+s*Math.cos(t),s*Math.sin(t),z);
 sup((t,z)=>Cc(1,t,z),0,2*PI,0,1,96,4,(t,z)=>tom(GEO,[Math.cos(t),Math.sin(t),0],.10,.20));
 sup((s,t)=>Cc(s,t,1),0,1,0,2*PI,8,72,()=>mixc(BG,GEO,.28));
 for(const z of [0,1])tubo(arco(t=>Cc(1,t,z),0,2*PI,120),.009,GEO);}
function caixa(x0,x1,y0,y1,z0,z1,corF){const F=[[n=>Wp(x1,n[0],n[1]),[y0,y1,z0,z1],[1,0,0]],[n=>Wp(x0,n[0],n[1]),[y0,y1,z0,z1],[-1,0,0]],[n=>Wp(n[0],y0,n[1]),[x0,x1,z0,z1],[0,-1,0]],[n=>Wp(n[0],y1,n[1]),[x0,x1,z0,z1],[0,1,0]],[n=>Wp(n[0],n[1],z1),[x0,x1,y0,y1],[0,0,1]],[n=>Wp(n[0],n[1],z0),[x0,x1,y0,y1],[0,0,-1]]];
 for(const [f,[a0,a1,b0,b1],nn] of F)sup((a,b)=>f([a,b]),a0,a1,b0,b1,1,1,()=>corF(nn));}
function arestasCaixa(x0,x1,y0,y1,z0,z1,cor,w=.006){const P=[[x0,y0],[x1,y0],[x1,y1],[x0,y1],[x0,y0]];for(const z of [z0,z1])tubo(P.map(([a,b])=>Wp(a,b,z)),w,cor);for(const [a,b] of P.slice(0,4))tubo([Wp(a,b,z0),Wp(a,b,z1)],w,cor);}
function tri(A,B,Cc,cor,n=24){sup((a,b)=>{const p=[0,1,2].map(i=>A[i]+a*((1-b)*(B[i]-A[i])+b*(Cc[i]-A[i])));return Wp(...p);},0,1,0,1,n,n,(a,b)=>{const p=[0,1,2].map(i=>A[i]+a*((1-b)*(B[i]-A[i])+b*(Cc[i]-A[i])));return cor(p);});}
const corRho3=(p,mx)=>mixc(RAMP0,CI,Math.pow(Math.min(1,(p[0]+p[1]+p[2])/mx),1.5));
const CAMLATA=()=>ver([9.2,-6.2,5.8],[0,0,.45],600,560);

// ---------- H1: lata uniforme; eixo central (azul) e reta da parede (ALERTA) saem bem acima da tampa; a seta de giro fica ACIMA da tampa ----------
if(K==='lataParede'){SC=2.2;DF=2.0;lataSolida(0);
 tubo([Wp(0,0,1.0),Wp(0,0,1.5)],.011,EZ);proj('ez',Wp(0,0,1.58));
 tracejado([Wp(1,0,-.15),Wp(1,0,1.75)],.013,AL,.08,.05);giroSeta(1,0,1.6,.22,AL);
 cota([-1,-1.25,0],[1,-1.25,0],'d2R',[0,-1,0]);
 CAMLATA();proj('O',Wp(0,0,0));proj('reta',Wp(1,0,2.02));}

// ---------- E5: a mesma lata, centro em (1, 0); o eixo z (azul) na parede ----------
if(K==='lataDobradica'||K==='lataDob3'){SC=2.2;DF=2.0;lataSolida(1);tubo([Wp(0,0,-.15),Wp(0,0,1.75)],.012,EZ);proj('ez',Wp(0,0,1.83));
 giroSeta(0,0,1.6,.22,EZ);
 if(K==='lataDob3'){const sc=.55;tubo(arco(t=>Wp(1+sc*Math.cos(t),sc*Math.sin(t),1.004),0,2*PI,90),.012,SOMB);
  tubo([Wp(1,0,1.006),Wp(1+sc*Math.cos(-PI*.3),sc*Math.sin(-PI*.3),1.006)],.010,SOMB);
  tubo([Wp(0,0,1.01),Wp(1,0,1.01)],.012,LIL);bolinha(Wp(1,0,1.01),BR,.03*SC);
  proj('s',Wp(1+.5*sc*Math.cos(-PI*.3)+.10,.5*sc*Math.sin(-PI*.3)-.10,1.0));proj('fioR',Wp(.5,.12,1.0));proj('C',Wp(1,0,1.0));
  proj('cmais',Wp(1+.78*Math.cos(PI*.35),.78*Math.sin(PI*.35),1.0));proj('cmenos',Wp(1+.78*Math.cos(PI*1.35),.78*Math.sin(PI*1.35),1.0));}
 ver([10.2,-6.2,5.8],[1,0,.45],600,560);proj('O',Wp(0,0,0));proj('Ct',Wp(1,0,1));}

// ---------- E1: cubo [0,1]³, ρ = x + y + z ----------
if(K==='cubo'||K==='cuboCaixas'||K==='cuboSonda'||K==='cuboDiag'){SC=2.0;DF=1.55;
 const faces=()=>{sup((x,y)=>Wp(x,y,0),0,1,0,1,20,20,(x,y)=>mixc(BG,'#'+corRho3([x,y,0],3).getHexString(),.75));
  sup((y,z)=>Wp(0,y,z),0,1,0,1,20,20,(y,z)=>mixc(BG,'#'+corRho3([0,y,z],3).getHexString(),.70));sup((x,z)=>Wp(x,1,z),0,1,0,1,20,20,(x,z)=>mixc(BG,'#'+corRho3([x,1,z],3).getHexString(),.80));};
 if(K==='cuboCaixas'){const g=.035;   // v2: sem a caixa de arame em volta
  for(const a of [0,.5])for(const b of [0,.5])for(const c of [0,.5]){const v=(a+b+c+.75)/3,cc='#'+mixc(RAMP0,CI,Math.pow(v,1.3)).getHexString();caixa(a+g,a+.5-g,b+g,b+.5-g,c+g,c+.5-g,nn=>tom(cc,nn,.55,.40));arestasCaixa(a+g,a+.5-g,b+g,b+.5-g,c+g,c+.5-g,'#0F0C26',.005);
   proj('c'+(a*2)+(b*2)+(c*2),Wp(a+.25,b+.25,c+.5-g));}}
 if(K==='cubo'){const fc=(p,nn)=>{const c=corRho3(p,3);return mixc(BG,'#'+c.getHexString(),.80+.20*Math.max(0,new T.Vector3(...nn).normalize().dot(LDIR)));};
  sup((y,z)=>Wp(1,y,z),0,1,0,1,30,30,(y,z)=>fc([1,y,z],[1,0,0]));sup((x,z)=>Wp(x,0,z),0,1,0,1,30,30,(x,z)=>fc([x,0,z],[0,-1,0]));sup((x,y)=>Wp(x,y,1),0,1,0,1,30,30,(x,y)=>fc([x,y,1],[0,0,1]));
  arestasCaixa(0,1,0,1,0,1,CI,.008);}
 if(K==='cuboSonda'){arestasCaixa(0,1,0,1,0,1,GEO,.008);faces();   // v2: sem os tracejados no chão
  const xs=.7,ys=.3;tubo([Wp(xs,ys,0),Wp(xs,ys,1)],.014,'#E8ECF8');bolinha(Wp(xs,ys,0),AZC,.035*SC);bolinha(Wp(xs,ys,1),CORAL,.035*SC);proj('entra',Wp(xs,ys,0));proj('sai',Wp(xs,ys,1));}
 if(K==='cuboDiag'){arestasCaixa(0,1,0,1,0,1,GEO,.008);faces();   // v2: sem anel do centro; tique GEO em 1/2, ⊕ em 5/9 (2D)
  tracejado([Wp(0,0,0),Wp(1,1,1)],.009,GEO,.07,.05);
  const m=.5,u=[.08,-.08,0];tubo([Wp(m-u[0],m-u[1],m),Wp(m+u[0],m+u[1],m)],.010,GEO);
  proj('centro',Wp(.5,.5,.5));proj('cm',Wp(5/9,5/9,5/9));proj('t12',Wp(.5+.17,.5-.17,.5));proj('t59',Wp(5/9-.15,5/9+.15,5/9+.06));proj('quina',Wp(1,1,1));}
 eixos3(SC*1.35,SC*1.35,SC*1.3);ver([9.2,-6.2,5.8],[.5,.5,.45],600,560);proj('O',Wp(0,0,0));proj('mid',Wp(.5,.5,1));}

// ---------- E1-5: a folha z = 1 e UMA camada de altura Δz (v2: sem as 16 caixinhas de arame) ----------
if(K==='cuboFolha'){SC=2.0;DF=1.55;arestasCaixa(0,1,0,1,0,1,TR,.006);
 sup((x,y)=>Wp(x,y,1),0,1,0,1,4,4,()=>C(LI));
 const dz=.12;arestasCaixa(0,1,0,1,1-dz/2,1+dz/2,'#E9FF9E',.006);
 cota([1.12,0,1-dz/2],[1.12,0,1+dz/2],'dz',[1,-.4,0]);
 eixos3(SC*1.35,SC*1.35,SC*1.3);ver([9.2,-6.2,5.8],[.5,.5,.45],600,560);proj('O',Wp(0,0,0));proj('folha',Wp(.5,.5,1.05));}

// ---------- E2: tetraedro x+y+z ≤ 1, ρ = x + y, aberto pela face inclinada ----------
// v2: câmera fora da diagonal (o centroide não cai em cima da origem); a base é a sombra (pêssego) no estado 'sombra'; sem contorno duplicado
if(K==='tetra'||K==='tetraSonda'||K==='tetraCent'||K==='tetraPlano'){SC=2.4;DF=1.85;
 const fc=(p,k)=>mixc(BG,'#'+corDens(p[0]+p[1]).getHexString(),k);
 const somb=(K==='tetraSonda'||K==='tetra');
 tri([0,0,0],[1,0,0],[0,1,0],p=>somb?mixc(BG,SOMB,.55):fc(p,.85));tri([0,0,0],[1,0,0],[0,0,1],p=>fc(p,.62));tri([0,0,0],[0,1,0],[0,0,1],p=>fc(p,.72));
 const V=[[0,0,0],[1,0,0],[0,1,0],[0,0,1]];for(const [a,b] of [[1,2],[1,3],[2,3]])tubo([Wp(...V[a]),Wp(...V[b])],.009,GEO);
 if(K==='tetraSonda'){const xs=.3,ys=.2,zt=1-xs-ys;tubo([Wp(xs,ys,0),Wp(xs,ys,zt)],.014,'#E8ECF8');bolinha(Wp(xs,ys,0),AZC,.035*SC);bolinha(Wp(xs,ys,zt),CORAL,.035*SC);proj('entra',Wp(xs,ys,0));proj('sai',Wp(xs,ys,zt));}
 if(K==='tetraCent'){for(const v of V.slice(1))bolinha(Wp(...v),BR,.028*SC);bolinha(Wp(0,0,0),BR,.028*SC);for(const v of V)tracejado([Wp(.25,.25,.25),Wp(...v)],.005,GEO,.05,.04);proj('cent',Wp(.25,.25,.25));V.forEach((v,i)=>proj('v'+i,Wp(...v)));}
 if(K==='tetraPlano'){const z5=.2,z4=.25;tubo([Wp(1-z5,0,z5),Wp(0,1-z5,z5),Wp(0,0,z5),Wp(1-z5,0,z5)],.010,MEN_);tracejado([Wp(1-z4,0,z4),Wp(0,1-z4,z4),Wp(0,0,z4),Wp(1-z4,0,z4)],.006,GEO,.05,.04);
  proj('z5',Wp(1-z5,0,z5));proj('z4',Wp(0,0,z4));}
 eixos3(SC*1.3,SC*1.3,SC*1.25);ver([8.6,4.2,5.4],[.36,.36,.30],600,560);proj('O',Wp(0,0,0));proj('vx',Wp(1,0,0));proj('vy',Wp(0,1,0));proj('vz',Wp(0,0,1));}

// ---------- E3: cone (vértice na origem), R = 1, h = 1,4; um quarto aberto θ ∈ [−π/2, 0] ----------
// v2: R e h viram COTAS (raio desenhado na tampa; h ao lado, fora do cone); no coneCm a cota de h se divide em 3h/4 + h/4
if(K==='cone'||K==='coneCm'||K==='coneCasca'){SC=2.0;DF=1.6;const Hh=1.4,ta=-PI/2,tb=0;const Cc=(s,t,z)=>WC(s,t,z);
 sup((t,z)=>Cc(z/Hh,t,z),tb,ta+2*PI,0,Hh,96,14,(t,z)=>tom(GEO,[Math.cos(t),Math.sin(t),-1/Hh],.12,.24));
 sup((s,t)=>Cc(s,t,Hh),0,1,tb,ta+2*PI,10,90,()=>mixc(BG,GEO,.30));
 for(const t of [ta,tb])sup((s,z)=>Cc(s,t,Hh*s+(Hh-Hh*s)*z),0,1,0,1,20,20,()=>mixc(BG,GEO,t===tb?.46:.38));
 tubo(arco(t=>Cc(1,t,Hh),tb,ta+2*PI,120),.009,GEO);for(const t of [ta,tb]){tubo([Cc(0,t,0),Cc(1,t,Hh),Cc(0,t,Hh)],.009,GEO);}
 tubo(arco(t=>Cc(1,t,Hh),ta,tb,30),.005,TR);
 eixoZ(-.05,Hh+.40);
 const tR=PI*.62;tubo([Wp(0,0,Hh+.006),Cc(1,tR,Hh+.006)],.008,COTA);proj('R',Cc(.55,tR+.22,Hh));
 const cx=Cc(1.32,-PI*.62,0);const P=z=>[cx[0]/SC,cx[1]/SC,z];
 if(K==='coneCm'){cota(P(0),P(.75*Hh),'c34',[1,0,0]);cota(P(.75*Hh),P(Hh),'c14',[1,0,0]);
  tracejado([Cc(0,0,.5*Hh),Cc(.5,-PI*.25,.5*Hh)],.008,GEO,.05,.04);proj('z12',Cc(.72,-PI*.25,.5*Hh));}
 else cota(P(0),P(Hh),'h',[1,0,0]);
 if(K==='cone'){const ss=.6,tt=-.25,zi=Hh*ss;tubo([Cc(ss,tt,zi),Cc(ss,tt,Hh)],.012,'#E8ECF8');bolinha(Cc(ss,tt,zi),AZC,.035*SC);bolinha(Cc(ss,tt,Hh),CORAL,.035*SC);proj('entra',Cc(ss,tt,zi));proj('sai',Cc(ss,tt,Hh));}
 if(K==='coneCasca'){const sc=.55;sup((t,z)=>Cc(sc,t,z),ta,tb,Hh*sc,Hh,20,4,(t,z)=>tom(SOMB,[Math.cos(t),Math.sin(t),0],.55,.35));
  tubo(arco(t=>Cc(sc,t,Hh+.003),tb,ta+2*PI,90),.009,SOMB);tubo([Cc(0,0,Hh+.01),Cc(sc,-PI*.25,Hh+.01)],.009,SOMB);giroSeta(0,0,Hh+.30,.24);proj('s',Cc(sc*.55,-PI*.25-.35,Hh));proj('casca',Cc(sc,-PI/4,(Hh*sc+Hh)/2));}
 ver([9.2,-6.2,5.0],[0,0,.70],600,560);proj('O',Wp(0,0,0));proj('z34',Wp(0,0,.75*Hh));proj('topo',Wp(0,0,Hh));}

// ---------- E4: meia bola, um quarto aberto (x>0, y<0) ----------
// v2: arco de φ pequeno junto à origem; ⊕ acima dele; placas r e z fora das linhas; fatia em z = 0,65 (acima do ⊕, que fica visível)
if(K==='semi'||K==='semiFatia'){SC=1.9;DF=1.6;const inQ=t=>(Math.cos(t)>1e-6&&Math.sin(t)<-1e-6);
 const F=(f,t)=>WS(1,f,t);const tris=[];const nf=24,nt=96;
 for(let i=0;i<nf;i++)for(let j=0;j<nt;j++){const f0=PI/2*i/nf,f1=PI/2*(i+1)/nf,t0=2*PI*j/nt,t1=2*PI*(j+1)/nt,fm=(f0+f1)/2,tm=(t0+t1)/2;if(inQ(tm))continue;
  const cc=tom(GEO,sph(1,fm,tm),.12,.26);tris.push([F(f0,t0),F(f1,t0),F(f1,t1),cc],[F(f0,t0),F(f1,t1),F(f0,t1),cc]);}
 malhaTri(tris);
 sup((a,r)=>Wp(r*Math.cos(a),0,r*Math.sin(a)),0,PI/2,0,1,30,12,()=>mixc(BG,GEO,.48));
 sup((a,r)=>Wp(0,-r*Math.cos(a),r*Math.sin(a)),0,PI/2,0,1,30,12,()=>mixc(BG,GEO,.38));
 tubo(arco(a=>Wp(Math.cos(a),0,Math.sin(a)),0,PI/2,40),.007,GEO);tubo(arco(a=>Wp(0,-Math.cos(a),Math.sin(a)),0,PI/2,40),.007,GEO);
 tubo(arco(t=>WC(1,t,0),0,2*PI,120),.007,GEO);
 if(K==='semi'){const rr=.85,ff=PI*.36,Pp=[rr*Math.sin(ff),0,rr*Math.cos(ff)];
  tubo([Wp(0,0,0),Wp(...Pp)],.012,RO);bolinha(Wp(...Pp),BR,.035*SC);tracejado([Wp(Pp[0],0,0),Wp(...Pp)],.010,EZ,.05,.04);
  tubo(arco(a=>Wp(.30*Math.sin(a),0,.30*Math.cos(a)),0,ff,24),.010,FI);
  proj('P',Wp(...Pp));proj('r',Wp(Pp[0]*.62+.07,0,Pp[2]*.62-.09));proj('phi',Wp(.44*Math.sin(ff*.62),0,.44*Math.cos(ff*.62)));proj('z',Wp(Pp[0]+.11,0,Pp[2]*.45));}
 if(K==='semiFatia'){const zf=.8,rf=Math.sqrt(1-zf*zf);sup((s,t)=>WC(s,t,zf),0,rf,-PI/2,0,8,24,()=>C(LI));
  tubo(arco(t=>WC(rf+.006,t,zf),0,2*PI,90),.010,LI);
  tubo([Wp(0,0,zf+.004),WC(rf,-PI*.06,zf+.004)],.011,SOMB);proj('raio',WC(rf+.55,-PI*.06,zf+.05));proj('zf',Wp(0,0,zf+.17));}
 eixoZ(-.02,1.40);ver([9.2,-6.2,5.0],[0,0,.3],600,560);proj('O',Wp(0,0,0));proj('z38',Wp(0,0,3/8));}

// ---------- S2: hélice na parede da lata, conta e força (v2: só os dois aros da lata, sem verticais; conta na frente) ----------
if(K==='helice'){SC=2.2;DF=2.0;lataTraco(1,1,{nv:0});eixoZ(-.1,1.45);
 const H=t=>WC(1.012,t,t/(4*PI));tubo(arco(H,0,4*PI,400),.014,HEL);
 const tc=2*PI-.75;bolinha(H(tc),BR,.045*SC);const P0=H(tc),tg=[-Math.sin(tc),Math.cos(tc),1/(4*PI)];const n=Math.hypot(...tg);
 const Fp=[P0[0]+tg[0]/n*1.1,P0[1]+tg[1]/n*1.1,P0[2]+tg[2]/n*1.1+.25];seta(P0,Fp,.012,EZ);
 CAMLATA();proj('O',Wp(0,0,0));proj('conta',H(tc));proj('F',Fp);proj('hel',H(PI*3.1));}
