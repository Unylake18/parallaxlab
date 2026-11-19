// ===== Cenas 3D-alvo do 3.5-T4 (centro de massa e momento de inércia) =====
// Mesmo estilo do EP. 17: opaco, tom fixo, sem luz, fundo transparente; piso quadriculado z = 0 (G2).
// Câmera da lata igual em lataGiro, lataDuas, lataCel, lataPlano, giroCel, lataParede: ver([9.2,-6.2,5.8],[0,0,.45],600,560), SC = 2,2.
const CM1='#35D9FF',CM2='#EA63FF',MEN_='#8CFFD2';
const CAMLATA=()=>ver([9.2,-6.2,5.8],[0,0,.45],600,560);
function eixoZ(z0=-.1,z1=1.45,cor=EZ,r=.010){tubo([Wp(0,0,z0),Wp(0,0,z1)],r,cor);proj('ez',Wp(0,0,z1+.12));}
function setasXY(){seta([SC*1.03,0,0],[SC*1.55,0,0],.012,E1);seta([0,SC*1.03,0],[0,SC*1.55,0],.012,E2);proj('ex',[SC*1.68,0,0]);proj('ey',[0,SC*1.68,0]);}
function giroSeta(cx,cy,zz,rr=.32,cor=GEO){const A=arco(t=>Wp(cx+rr*Math.cos(t),cy+rr*Math.sin(t),zz),-PI*.9,PI*.55,60);tubo(A,.010,cor);
 const a1=Wp(cx+rr*Math.cos(PI*.55),cy+rr*Math.sin(PI*.55),zz),a0=Wp(cx+rr*Math.cos(PI*.48),cy+rr*Math.sin(PI*.48),zz);seta(a0,a1,.010,cor);proj('giro',Wp(cx+rr,cy,zz));proj('omega',Wp(cx+rr*Math.cos(-PI*.35),cy+rr*Math.sin(-PI*.35),zz));}
// lata pesada com degradê (mesma do EP. 17), um quarto aberto θ ∈ [−π/2, 0]
function lataPesada(){const ta=-PI/2,tb=0;
 sup((t,z)=>WC(1,t,z),tb,ta+2*PI,110,8,(t,z)=>tom(corR(1,z),[Math.cos(t),Math.sin(t),0],.55,.40));
 sup((s,t)=>WC(s,t,1),0,1,tb,ta+2*PI,24,90,(s,t)=>corR(s,1).clone().lerp(C(BR),.06));
 for(const t of [ta,tb])sup((s,z)=>WC(s,t,z),0,1,0,1,30,30,(s,z)=>corR(s,z));
 for(const z of [0,1])tubo(arco(t=>WC(1,t,z),tb,ta+2*PI,120),.009,CI);
 for(const z of [0,1])tubo(arco(t=>WC(1,t,z),ta,tb,40),.005,TR);tubo([WC(1,ta,0),WC(1,ta,1)],.005,TR);
 for(const t of [ta,tb])tubo([WC(0,t,0),WC(1,t,0),WC(1,t,1),WC(0,t,1)],.009,CI);
 for(const r of [.5,1])for(const t of [ta,tb])tubo(arco(a=>WC(r*Math.cos(a),t,r*Math.sin(a)),0,PI/2,40),.004,'#1E5C7A');
 proj('quina',WC(1,tb,1));proj('fundo',Wp(.08,0,.08));proj('O',[0,0,0]);proj('meio',Wp(0,0,.5));proj('zbar',Wp(0,0,.5549));}

// ---------- H1 / B4: lata pesada que gira ----------
if(K==='lataGiro'||K==='lataPesada'){SC=2.2;DF=1.4;lataPesada();eixoZ(0,1.45);setasXY();if(K==='lataGiro')giroSeta(0,0,1.32);CAMLATA();}

// ---------- H2: lata em traço + duas células (origem e quina) com o fio s ----------
if(K==='lataDuas'){SC=2.2;DF=1.4;lataTraco(1,1,{nv:12});eixoZ(-.1,1.45);
 const a1=-PI*.30,a2=a1+PI/8;celC(.12,.32,a1,a2,.04,.24);const b1=-PI*.12,b2=b1+PI/10;celC(.8,1,b1,b2,.8,1);
 tracejado([Wp(0,0,.14),WC(.12,(a1+a2)/2,.14)],.010,SOMB,.05,.04);tracejado([Wp(0,0,.9),WC(.8,(b1+b2)/2,.9)],.010,SOMB,.07,.05);
 CAMLATA();proj('c1',WC(.32,a1,.14));proj('c2',WC(1.02,(b1+b2)/2,.9));proj('f1',WC(.06,(a1+a2)/2,.18));proj('f2',WC(.4,(b1+b2)/2,.9));}

// ---------- B1-1: três bolinhas (etapa 1) e a célula com x, y, z (etapa 2) ----------
if(K==='cmPontos'){SC=1.2;DF=1.3;eixos3(SC*2.4,SC*2.4,SC*1.9);
 const B=[[[.3,2.0,1.4],1],[[2.0,.4,.5],3],[[1.8,1.9,1.6],2]];let mt=0,cm=[0,0,0];
 for(const [p,m] of B){bolinha(Wp(...p),CI,.075*Math.cbrt(m)*SC);tracejado([Wp(p[0],p[1],0),Wp(p[0],p[1],p[2]-.09*Math.cbrt(m))],.006,GEO,.06,.05);mt+=m;cm=cm.map((v,i)=>v+m*p[i]);}
 cm=cm.map(v=>v/mt);B.forEach(([p,m],i)=>proj('m'+(i+1),Wp(...p)));proj('cm',Wp(...cm));proj('cmChao',Wp(cm[0],cm[1],0));
 ver([9.0,-6.4,5.2],[1.1,1.1,.6],560,600);}
if(K==='lataCel'){SC=2.2;DF=1.4;lataTraco(1,1,{nv:12});eixoZ(-.1,1.45);setasXY();
 const t1=-PI*.30,t2=t1+PI/10,s1=.62,s2=.82,z1=.55,z2=.75;celC(s1,s2,t1,t2,z1,z2);const tm=(t1+t2)/2,sm=(s1+s2)/2,P0=cyl(sm,tm,0);
 tracejado([Wp(0,0,.002),Wp(P0[0],0,.002)],.010,E1,.06,.05);tracejado([Wp(P0[0],0,.002),Wp(P0[0],P0[1],.002)],.010,E2,.06,.05);tracejado([Wp(P0[0],P0[1],0),Wp(P0[0],P0[1],z1)],.010,EZ,.06,.05);
 CAMLATA();proj('cel',WC(s2+.06,tm,(z1+z2)/2));proj('px',Wp(P0[0]/2,0,0));proj('py',Wp(P0[0],P0[1]/2,0));proj('pz',Wp(P0[0],P0[1],z1/2));}

// ---------- B1-2: o plano z = z̄ cortando a lata, células acima e abaixo ----------
if(K==='lataPlano'){SC=2.2;DF=1.4;lataTraco(1,1,{nv:12});eixoZ(-.1,1.45);const zb=.555,L=.85;
 tubo([Wp(-L,-L,zb),Wp(L,-L,zb),Wp(L,L,zb),Wp(-L,L,zb),Wp(-L,-L,zb)],.008,MEN_);
 tubo(arco(t=>WC(1,t,zb),0,2*PI,120),.006,MEN_);
 const a1=-PI*.32,a2=a1+PI/10;celC(.7,.9,a1,a2,.82,.97);const b1=-PI*.10,b2=b1+PI/10;celC(.45,.65,b1,b2,.10,.25);
 tracejado([WC(.8,(a1+a2)/2,.82),WC(.8,(a1+a2)/2,zb)],.010,EZ,.05,.04);tracejado([WC(.55,(b1+b2)/2,.25),WC(.55,(b1+b2)/2,zb)],.010,EZ,.05,.04);
 CAMLATA();proj('cA',WC(.92,(a1+a2)/2,.9));proj('cB',WC(.67,(b1+b2)/2,.17));proj('fA',WC(.8,(a1+a2)/2,(.82+zb)/2));proj('fB',WC(.55,(b1+b2)/2,(.25+zb)/2));proj('plano',Wp(L,-L*.2,zb));proj('zbar',Wp(0,0,zb));}

// ---------- B1-3: duas células gêmeas em θ e θ + π ----------
if(K==='lataSim'||K==='lataSim2'){SC=2.2;DF=1.4;lataTraco(1,1,{nv:12});eixoZ(-.1,1.45);setasXY();
 const t0=-PI*.18,d=PI/10,s1=.6,s2=.8,z1=.4,z2=.6;const claro=K==='lataSim2';
 celC(s1,s2,t0,t0+d,z1,z2,claro?'#E9FF9E':LI);celC(s1,s2,t0+PI,t0+PI+d,z1,z2,claro?'#7E9A3A':LI);
 tracejado([Wp(0,0,.5),WC(s1,t0+d/2,.5)],.010,SOMB,.06,.05);tracejado([Wp(0,0,.5),WC(s1,t0+PI+d/2,.5)],.010,SOMB,.06,.05);
 ver([7.6,-5.0,8.6],[0,0,.4],600,560);proj('cA',WC(s2+.08,t0+d/2,.5));proj('cB',WC(s2+.08,t0+PI+d/2,.5));}

// ---------- B2: a taça x² + y² ≤ z ≤ 1, homogênea, um quarto aberto, sonda ----------
if(K==='taca'){SC=2.2;DF=1.4;const ta=-PI/2,tb=0;
 sup((t,s)=>WC(s,t,s*s),tb,ta+2*PI,0,1,96,20,(t,s)=>tom(GEO,[2*s*Math.cos(t),2*s*Math.sin(t),-1],.14,.24));
 sup((s,t)=>WC(s,t,1),0,1,tb,ta+2*PI,12,90,()=>mixc(BG,GEO,.34));
 for(const t of [ta,tb])sup((s,z)=>WC(s,t,s*s+(1-s*s)*z),0,1,0,1,30,30,(s,z)=>mixc(BG,GEO,t===tb?.46:.40));
 for(const t of [ta,tb]){tubo(arco(s=>WC(s,t,s*s),0,1,40),.009,GEO);tubo([WC(0,t,1),WC(1,t,1)],.009,GEO);}
 tubo(arco(t=>WC(1,t,1),tb,ta+2*PI,120),.009,GEO);
 tubo(arco(t=>WC(1,t,0),0,2*PI,120),.006,'#6C7698');
 eixoZ(-.05,1.45);const ss=.6,tt=-.04;
 tracejado([WC(ss,tt,0),WC(ss,tt,ss*ss)],.008,AZC,.05,.04);tubo([WC(ss,tt,ss*ss),WC(ss,tt,1)],.012,'#E8ECF8');
 bolinha(WC(ss,tt,ss*ss),AZC,.035*SC);bolinha(WC(ss,tt,1),CORAL,.035*SC);
 CAMLATA();proj('entra',WC(ss,tt,ss*ss));proj('sai',WC(ss,tt,1));proj('z23',Wp(0,0,2/3));proj('z12',Wp(0,0,.5));proj('borda',WC(1,PI*.75,1));proj('fundoT',Wp(0,0,0));}

// ---------- B3-1: girar — célula na parede, fio s, velocidade tangente ----------
if(K==='giroCel'){SC=2.2;DF=1.4;lataTraco(1,1,{nv:12});eixoZ(-.25,1.6,EZ,.016);giroSeta(0,0,1.38);
 const t1=-PI*.18,t2=t1+PI/10,tm=(t1+t2)/2;celC(.85,1,t1,t2,.45,.65);
 tracejado([Wp(0,0,.55),WC(.85,tm,.55)],.010,SOMB,.07,.05);
 const P0=WC(1.0,tm,.55),tg=[-Math.sin(tm),Math.cos(tm),0];seta(P0,[P0[0]+tg[0]*.9,P0[1]+tg[1]*.9,P0[2]],.010,BR);
 CAMLATA();proj('cel',WC(1.04,tm,.62));proj('fio',WC(.45,tm,.55));proj('v',[P0[0]+tg[0]*.95,P0[1]+tg[1]*.95,P0[2]]);}

// ---------- B3-2: distância ao eixo z (s) × até o eixo x × até a origem (r) ----------
if(K==='distEixo'){SC=1.3;DF=1.3;eixos3(SC*2.3,SC*2.3,SC*1.9);const P=[1,1.2,1];bolinha(Wp(...P),BR,.045*SC);
 tracejado([Wp(0,0,1),Wp(...P)],.010,SOMB,.07,.05);tracejado([Wp(1,0,0),Wp(...P)],.008,GEO,.06,.05);tubo([Wp(0,0,0),Wp(...P)],.012,RO);
 tracejado([Wp(1,1.2,0),Wp(...P)],.005,'#6C7698',.05,.05);tracejado([Wp(0,0,0),Wp(1,1.2,0)],.005,'#6C7698',.05,.05);
 ver([9.0,-6.4,5.2],[.9,.9,.6],560,600);proj('P',Wp(...P));proj('s',Wp(.5,.6,1));proj('fx',Wp(1,.6,.5));proj('r',Wp(.5,.6,.5));proj('pe',Wp(0,0,1));}

// ---------- B3-3: cilindro homogêneo + casca de raio s ----------
if(K==='cilindroH'){SC=1.9;DF=1.4;const Hh=1.4;
 sup((t,z)=>WC(1,t,z),0,2*PI,0,Hh,96,4,(t,z)=>tom(GEO,[Math.cos(t),Math.sin(t),0],.10,.18));
 sup((s,t)=>WC(s,t,Hh),0,1,0,2*PI,8,72,()=>mixc(BG,GEO,.26));
 for(const z of [0,Hh])tubo(arco(t=>WC(1,t,z),0,2*PI,120),.009,GEO);
 const sc=.55;for(const z of [Hh+.002])tubo(arco(t=>WC(sc,t,z),0,2*PI,90),.010,SOMB);
 tubo([WC(0,0,Hh+.004),WC(sc,-PI*.30,Hh+.004)],.012,SOMB);tubo([WC(0,0,Hh+.006),WC(1,PI*.08,Hh+.006)],.010,GEO);
 tubo([WC(1,-PI*.47,0),WC(1,-PI*.47,Hh)],.014,EZ);eixoZ(-.1,Hh+.35);
 ver([9.2,-6.2,5.0],[0,0,.65],600,560);proj('s',WC(sc*.55,-PI*.30,Hh));proj('R',WC(.7,PI*.08,Hh));proj('h',WC(1,-PI*.47,Hh/2));}

// ---------- B3-4: bola homogênea, octante aberto (x>0, y<0, z>0), r, φ e a sombra s ----------
if(K==='esferaOct'){SC=1.9;DF=1.4;const inOct=(t,f)=>(Math.cos(t)>1e-6&&Math.sin(t)<-1e-6&&f<PI/2);
 const F=(f,t)=>WS(1,f,t);const tris=[];const nf=48,nt=96;
 for(let i=0;i<nf;i++)for(let j=0;j<nt;j++){const f0=PI*i/nf,f1=PI*(i+1)/nf,t0=2*PI*j/nt,t1=2*PI*(j+1)/nt,fm=(f0+f1)/2,tm=(t0+t1)/2;if(inOct(tm,fm))continue;
  const cc=tom(GEO,sph(1,fm,tm),.12,.26);tris.push([F(f0,t0),F(f1,t0),F(f1,t1),cc],[F(f0,t0),F(f1,t1),F(f0,t1),cc]);}
 malhaTri(tris);
 sup((a,r)=>Wp(r*Math.cos(a),0,r*Math.sin(a)),0,PI/2,0,1,30,12,()=>mixc(BG,GEO,.48));      // face y = 0 (x>0, z>0)
 sup((a,r)=>Wp(0,-r*Math.cos(a),r*Math.sin(a)),0,PI/2,0,1,30,12,()=>mixc(BG,GEO,.38));     // face x = 0
 sup((a,r)=>Wp(r*Math.cos(a),-r*Math.sin(a),0),0,PI/2,0,1,30,12,()=>mixc(BG,GEO,.30));     // face z = 0
 tubo(arco(a=>Wp(Math.cos(a),0,Math.sin(a)),0,PI/2,40),.007,GEO);tubo(arco(a=>Wp(0,-Math.cos(a),Math.sin(a)),0,PI/2,40),.007,GEO);tubo(arco(a=>Wp(Math.cos(a),-Math.sin(a),0),0,PI/2,40),.007,GEO);
 const rr=.8,ff=PI*.30,Pp=[rr*Math.sin(ff),0,rr*Math.cos(ff)];
 tubo([Wp(0,0,0),Wp(...Pp)],.012,RO);bolinha(Wp(...Pp),BR,.04*SC);tracejado([Wp(0,0,Pp[2]),Wp(...Pp)],.010,SOMB,.05,.04);
 tubo(arco(a=>Wp(.28*Math.sin(a),0,.28*Math.cos(a)),0,ff,24),.008,FI);
 eixoZ(-.02,1.45);ver([9.2,-6.2,5.0],[0,0,.3],600,560);
 proj('P',Wp(...Pp));proj('r',Wp(Pp[0]*.55,0,Pp[2]*.55));proj('phi',Wp(.36*Math.sin(ff/2),0,.36*Math.cos(ff/2)));proj('s',Wp(Pp[0]/2,0,Pp[2]));proj('R',Wp(.72,-.72,0));}

// ---------- S2: girar a lata em volta de uma reta da parede (x = 1, y = 0) ----------
if(K==='lataParede'){SC=2.2;DF=1.4;lataTraco(1,1,{nv:12});tubo([Wp(0,0,-.1),Wp(0,0,1.45)],.006,'#6C7698');
 tracejado([Wp(1,0,-.25),Wp(1,0,1.6)],.014,AL,.08,.05);giroSeta(1,0,1.38,.30);
 CAMLATA();proj('reta',Wp(1,0,1.65));proj('ez0',Wp(0,0,1.5));}
