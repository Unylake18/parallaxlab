 // ===== Quadros-alvo do 3.6-T1 · yt_0045 provisório =====
 // Cores novas: campo F verde-menta #2EE6A0 (padrão do EP. 01), γ′ e deslocamentos violeta #B48CFF, curva laranja #FFB36B, t #E08A3C.
 // Componentes do campo: P, Q, R (decisão do Kaio). A hélice usa a lata do canal: raio 1, altura 1, z = c t.
 Object.assign(M,{'\\g':'\\textcolor{#FFB36B}{\\gamma}','\\gp':"\\textcolor{#B48CFF}{\\gamma'}",'\\Fv':'\\textcolor{#2EE6A0}{\\vec F}',
  '\\dg':'\\textcolor{#B48CFF}{d\\gamma}','\\Dg':'\\textcolor{#B48CFF}{\\Delta\\gamma}','\\DTt':'\\textcolor{#E08A3C}{\\Delta t}',
  '\\al':'\\textcolor{#B48CFF}{\\alpha}','\\Lim':'\\textcolor{#C6F26B}','\\Om':'\\Omega','\\uu':'\\textcolor{#E08A3C}{u}'});
 const CAMPO='#2EE6A0',HEL='#FFB36B',VIO='#B48CFF',TT='#E08A3C';
 let EVITA=[];
 // v2 · campo NA GRADE: cada seta é CENTRADA num nó do papel (meio-inteiro do desenho), meia-seta ≤ 0,4 u;
 // nó descartado se a seta passar a menos de `folga` (unidades) de uma curva, ou cair numa caixa px de rótulo.
 function amostra(f,a,b,n=200){const r=[];for(let i=0;i<=n;i++)r.push(f(a+(b-a)*i/n));return r;}
 function campoG(F,xs,ys,{k=.32,mx=.8,curvas=[],folga=.15,evitaPx=[],w=3,head=12}={}){
  for(const X of xs)for(const Y of ys){const v=F(X,Y),L=Math.hypot(...v);if(L<1e-9)continue;const l=Math.min(k*L,mx),u=[v[0]/L,v[1]/L];
   const A=[X-u[0]*l/2,Y-u[1]*l/2],B=[X+u[0]*l/2,Y+u[1]*l/2];let ok=true;
   for(let i=0;i<=10&&ok;i++){const q=[A[0]+(B[0]-A[0])*i/10,A[1]+(B[1]-A[1])*i/10];for(const c of curvas)for(const p of c){if(Math.hypot(p[0]-q[0],p[1]-q[1])<folga){ok=false;break;}}
    const Q=P(...q);for(const [x0,y0,x1,y1] of evitaPx)if(Q[0]>x0-6&&Q[0]<x1+6&&Q[1]>y0-6&&Q[1]<y1+6)ok=false;}
   if(ok)seta(A,B,CAMPO,w,head);}}
 const meio=(a,b,s=1)=>{const r=[];for(let v=a;v<=b+1e-9;v+=s)r.push(+v.toFixed(3));return r;};
 // ---- helpers 2D do palco ----
 function eixos2(x0,x1,y0,y1,{lx=true}={}){seta([x0,0],[x1,0],E1,3,16);seta([0,y0],[0,y1],E2,3,16);
  if(lx){tex('\\X',P(x1,0)[0]+10,P(x1,0)[1]+22,34);tex('\\Y',P(0,y1)[0]+16,P(0,y1)[1]+6,34);}}
 function curvaF(f,a,b,cor=HEL,w=5,n=160){linha(arco2(f,a,b,n),cor,w);}
 function sentido(f,t,cor=HEL,h=22){const A=f(t-.02),B=f(t+.02);const a=P(...A),b=P(...B);const ux=b[0]-a[0],uy=b[1]-a[1],L=Math.hypot(ux,uy);
  const c=P(...f(t));setaPx([c[0]-ux/L*h,c[1]-uy/L*h],[c[0]+ux/L*4,c[1]+uy/L*4],cor,0,h);}
 // seta de campo comprimida: comprimento na tela = min(k·|F|, mx) unidades
 function setaCampo(p,v,{k=.35,mx=.9,cor=CAMPO,w=3.5,head=14}={}){const L=Math.hypot(...v);if(L<1e-9)return;const s=Math.min(k*L,mx)/L;seta(p,[p[0]+v[0]*s,p[1]+v[1]*s],cor,w,head);}
 function campo(F,pts,o={}){for(const p of pts)setaCampo(p,F(...p),o);}
 function grade(xs,ys){const r=[];for(const a of xs)for(const b of ys)r.push([a,b]);return r;}
 function chipMix(parts,X,Y,cor=GEO,size=34){const end=mixl(parts,X+16,Y,size);x.strokeStyle=cor;x.globalAlpha=.8;x.lineWidth=2;x.beginPath();x.roundRect(X,Y-size*.75,end-X+4,size*1.5,10);x.stroke();x.globalAlpha=1;return end;}
 function regua(X0,X1,Y,marks){x.strokeStyle=TT;x.lineWidth=3;x.beginPath();x.moveTo(X0,Y);x.lineTo(X1,Y);x.stroke();
  for(const [X,s] of marks){x.beginPath();x.moveTo(X,Y-10);x.lineTo(X,Y+10);x.stroke();if(s)tex(s,X,Y+34,26,'c');}}
 const RA=2;   // raio do círculo no desenho (unidade 120 px)

 // 02 · H2 · só a parte ao longo do caminho trabalha
 if(K==='h2'){fundoV();vista(480,600,120);papelTela(.5);await logo();canto('SÓ A PARTE AO LONGO DO CAMINHO TRABALHA');
  const f=s=>[-3.4+6.6*s,-1.6+2.2*s+1.0*Math.sin(PI*1.6*s)];curvaF(f,0,1,HEL,6);sentido(f,.85);
  const s0=.42,p=f(s0),q=f(s0+.001),tx=(q[0]-p[0]),ty=(q[1]-p[1]),L=Math.hypot(tx,ty),T=[tx/L,ty/L],N=[-T[1],T[0]];
  const a=1.55,b=1.05,Fv=[a*T[0]+b*N[0],a*T[1]+b*N[1]];
  seta(p,[p[0]+a*T[0],p[1]+a*T[1]],LI,4,16);seta(p,[p[0]+b*N[0],p[1]+b*N[1]],GEO,4,16);
  guia(P(p[0]+a*T[0],p[1]+a*T[1]),P(p[0]+Fv[0],p[1]+Fv[1]));guia(P(p[0]+b*N[0],p[1]+b*N[1]),P(p[0]+Fv[0],p[1]+Fv[1]));
  seta(p,[p[0]+Fv[0],p[1]+Fv[1]],CAMPO,6,22);ponto(p,BR,11);
  tex('\\Fv',P(p[0]+Fv[0],p[1]+Fv[1])[0]+14,P(p[0]+Fv[0],p[1]+Fv[1])[1]-14,38,'l',true);
  legq('AO LONGO DO CAMINHO: TRABALHA',120,1020,LI);legq('DE LADO: NÃO TRABALHA',720,1020,GEO);
  txt('SÓ A PARTE DA FORÇA',COL,250,{size:44});txt('AO LONGO DO CAMINHO',COL,310,{size:44,cor:LI});txt('TRABALHA',COL,370,{size:44});
  leg('CAMINHO EM PEDACINHOS:',COL,500,GEO,'left',32);leg('SOMA DE TRABALHINHOS',COL,545,GEO,'left',32);}

 // 03 · B1 · força constante, caminho reto
 if(K==='b1'){fundoV();vista(180,720,120);papelTela(.5);await logo();canto('FORÇA CONSTANTE, CAMINHO RETO');
  eixos2(-.6,5.6,-.6,4.2);for(let i=1;i<=5;i++){tex(String(i),P(i,0)[0],P(i,0)[1]+28,26,'c');}for(let j=1;j<=3;j++)tex(String(j),P(0,j)[0]-22,P(0,j)[1],26,'c');
  linha([[1,1],[4,1]],HEL,6);seta([1.55,1],[1.95,1],HEL,6,22);ponto([1,1],BR,10);ponto([4,1],BR,10);
  tex('A',P(1,1)[0]-34,P(1,1)[1]+30,36,'c',true);tex('B',P(4,1)[0]+30,P(4,1)[1]+30,36,'c',true);
  const k=.48;for(const xx of [1.08,3.45])seta([xx,1],[xx+2*k,1+k],CAMPO,4,16);
  const xm=2.25;seta([xm,1],[xm+2*k,1],LI,4,16);seta([xm+2*k,1],[xm+2*k,1+k],GEO,4,14);seta([xm,1],[xm+2*k,1+k],CAMPO,5,18);
  tex('\\Fv=(2,\\ 1)',P(xm+.3,1+k)[0],P(xm+.3,1+k)[1]-40,36,'l',true);tex('\\Lim{2}',P(xm+k,1)[0],P(xm+k,1)[1]+28,28,'c');tex('\\Ge{1}',P(xm+2*k,1+k/2)[0]+20,P(xm+2*k,1+k/2)[1],28,'l');
  leg('F CONSTANTE, CAMINHO RETO',COL,190,GEO,'left',30);
  tex('W=\\Fv\\cdot(B-A)',COL,265,50);
  tex('B-A=(4-1,\\ 1-1)=(3,\\ 0)',COL,360,44);
  const r=caixaMen(tex('W=2\\cdot 3+1\\cdot 0=6',COL,455,46));
  tex('W=|\\Fv|\\,|B-A|\\cos\\al',COL,560,46);
  chipMix([['m','\\cos\\al>0:'],['t','AJUDA, ',LI],['m','W>0']],COL,665,LI,34);
  chipMix([['m','\\al=90^\\circ:'],['t','DE LADO, ',GEO],['m','W=0']],COL,755,GEO,34);
  chipMix([['m','\\cos\\al<0:'],['t','ATRAPALHA, ',AL],['m','W<0']],COL,845,AL,34);}

 // 04 · B2-1 · a partição
 const fB2=s=>[0.5+5.8*s,1.2+2.6*s+0.9*Math.sin(2*PI*s)];
 const FB2=(X,Y)=>[0.9,0.6-0.25*X];
 function palcoB2(){/*v2*/eixos2(-.3,6.6,-.3,5.6,{lx:true});campoG(FB2,meio(.5,6.5),meio(.5,5.5),{k:.5,mx:.6,curvas:[amostra(fB2,0,1,240)],folga:.2,evitaPx:EVITA});
  curvaF(fB2,0,1,HEL,6);sentido(fB2,.93);tex('\\g(a)',P(...fB2(0))[0]-6,P(...fB2(0))[1]+42,32,'c',true);tex('\\g(b)',P(...fB2(1))[0]+4,P(...fB2(1))[1]-42,32,'c',true);
  const ts=[0,1,2,3,4,5,6].map(i=>i/6);for(let i=1;i<7;i++)seta(fB2(ts[i-1]),fB2(ts[i]),VIO,4,15);for(const s of ts)ponto(fB2(s),BR,7);
  regua(200,890,990,ts.map((s,i)=>[200+690*s,i===0?'a=\\Tt_0':i===6?'\\Tt_6=b':'\\Tt_'+i]));return ts;}
 if(K==='b21'){fundoV();vista(140,890,120);EVITA=[[150,760,240,820],[860,365,940,415],[660,530,820,590],[550,640,660,700]];papelTela(.5);await logo();canto('CAMINHO CURVO, FORÇA QUE MUDA');
  const ts=palcoB2();const p4=fB2(ts[4]);setaCampo(p4,FB2(...p4),{k:1.0,mx:1.2,w:6,head:20});
  tex('\\Fv(\\g(\\Tt_4))',P(...p4)[0]+20,P(...p4)[1]-70,32,'l',true);tex('\\Dg_4',P(...fB2(.6))[0]-50,P(...fB2(.6))[1]+40,32,'c',true);
  mixl([['m','\\g:[a,b]\\to\\Om,'],['m','\\g(\\Tt)'],['t','= POSIÇÃO NO INSTANTE',BR],['m','\\Tt']],COL,195,40);
  tex('a=\\Tt_0<\\Tt_1<\\cdots<\\Tt_n=b',COL,290,44);
  tex('\\Dg_i=\\g(\\Tt_i)-\\g(\\Tt_{i-1})',COL,385,46);
  mixl([['t','TRABALHINHO',BR],['m','\\approx\\Fv(\\g(\\Tt_i))\\cdot\\Dg_i']],COL,485,44);
  tex('W\\approx\\sum_i \\Fv(\\g(\\Tt_i))\\cdot\\Dg_i',COL,600,50);}

 // 05 · B2-2 · da corda à velocidade
 if(K==='b22'){fundoV();vista(140,890,120);EVITA=[[150,760,240,820],[860,365,940,415],[510,140,940,375]];papelTela(.5);await logo();canto('APARECE UMA SOMA DE RIEMANN');
  const ts=palcoB2();
  painel2d(520,150,410,215);const c=[610,320],ch=[250,-120];setaPx(c,[c[0]+ch[0],c[1]+ch[1]],VIO,6,22);
  x.setLineDash([10,7]);setaPx([c[0],c[1]+10],[c[0]+ch[0]*1.04+6,c[1]+ch[1]*1.04+14],VIO,3,18);x.setLineDash([]);pontoPx(c,BR,8);
  tex('\\Dg_4',c[0]+120,c[1]-110,30,'c');tex('\\gp(\\Tt_4)\\DTt_4',c[0]+190,c[1]+24,28,'l');leg('QUASE IGUAIS',540,190,GEO,'left',26);
  mixl([['m','\\Dg_i\\approx\\gp(\\Tt_i)\\,\\DTt_i'],['t','VELOCIDADE × TEMPO',GEO]],COL,190,46);
  tex('W\\approx\\sum_i \\Fv(\\g(\\Tt_i))\\cdot\\gp(\\Tt_i)\\,\\DTt_i',COL,295,44);
  mixl([['m','g(\\Tt)=\\Fv(\\g(\\Tt))\\cdot\\gp(\\Tt)'],['t','UM NÚMERO PARA CADA',GEO],['m','\\Tt']],COL,400,40);
  mixl([['m','W\\approx\\sum_i g(\\Tt_i)\\,\\DTt_i'],['t','SOMA DE RIEMANN DE g EM [a, b]',GEO]],COL,500,40);
  const r=tex('\\max\\DTt_i\\to0:\\quad W=\\int_a^b \\Fv(\\g(\\Tt))\\cdot\\gp(\\Tt)\\,\\dTt',COL,630,44);
  chipMix([['m','\\g'],['t','DE CLASSE',GEO],['m','C^1:'],['t','O ERRO DA TROCA SOME NO LIMITE',GEO]],COL,770,GEO,30);}

 // 06 · B3 · a definição
 if(K==='b3'){fundoV();vista(300,600,100);papelTela(.6);await logo();canto('A DEFINIÇÃO');
  const f=s=>[-2.2+4.4*s,-1.2+1.4*s+0.9*Math.sin(PI*1.4*s)];curvaF(f,0,1,HEL,5);sentido(f,.9);
  const s0=.55,p=f(s0),q=f(s0+.001),tx=q[0]-p[0],ty=q[1]-p[1],L=Math.hypot(tx,ty);const T=[tx/L,ty/L];
  seta(p,[p[0]+1.3*T[0],p[1]+1.3*T[1]],VIO,5,18);const Fv=[1.2*T[0]-0.9*T[1],1.2*T[1]+0.9*T[0]];seta(p,[p[0]+Fv[0],p[1]+Fv[1]],CAMPO,5,18);ponto(p,BR,9);
  const a0=Math.atan2(T[1],T[0]),a1=Math.atan2(Fv[1],Fv[0]);x.strokeStyle=BR;x.lineWidth=2;x.beginPath();x.arc(...P(...p),48,-a1,-a0);x.stroke();
  tex('\\Fv',P(p[0]+Fv[0],p[1]+Fv[1])[0]-8,P(p[0]+Fv[0],p[1]+Fv[1])[1]-28,34,'c',true);tex('\\gp',P(p[0]+1.3*T[0],p[1]+1.3*T[1])[0]+44,P(p[0]+1.3*T[0],p[1]+1.3*T[1])[1]-8,34,'c',true);
  cartao(640,150,1220,880);txt('DEFINIÇÃO',680,210,{size:30,f:'SGM',cor:GEO});
  mixl([['m','\\Fv'],['t','CONTÍNUO NO ABERTO',BR],['m','\\Om\\subset\\mathbb{R}^3']],680,280,40);
  mixl([['m','\\g:[a,b]\\to\\Om'],['t','DE CLASSE',BR],['m','C^1']],680,360,40);
  caixaMen(tex('\\int_{\\g}\\Fv\\cdot\\dg=\\int_a^b \\Fv(\\g(\\Tt))\\cdot\\gp(\\Tt)\\,\\dTt',700,490,52),18);
  tex('\\dg=\\gp(\\Tt)\\,\\dTt',700,620,44);
  mixl([['t','①',BR],['m','\\Fv(\\g(\\Tt))'],['t','   ②',BR],['m','\\gp(\\Tt)'],['t','   ③ PRODUTO ESCALAR E INTEGRA EM',BR],['m','\\Tt']],700,730,38);
  chipMix([['m','\\Fv(\\g(\\Tt))\\cdot\\gp(\\Tt):'],['m','>0'],['t','AJUDA ·',LI],['m','=0'],['t','DE LADO ·',GEO],['m','<0'],['t','ATRAPALHA',AL]],700,850,GEO,32);}

 // 07–09 · B4 · o redemoinho
 const Frd=(X,Y)=>[-Y,X];
 function palcoB4({campoOn=true,circ=HEL}={}){eixos2(-3.6,3.7,-3.4,3.4);
  if(campoOn){const circ=amostra(t=>[RA*Math.cos(t),RA*Math.sin(t)],0,2*PI,240);campoG(Frd,meio(-3.5,3.5),meio(-2.5,2.5),{k:.3,mx:.8,curvas:[circ],folga:.16,evitaPx:EVITA});}
  const fc=t=>[RA*Math.cos(t),RA*Math.sin(t)];curvaF(fc,0,2*PI,circ,circ===HEL?6:2.5);if(circ===HEL)sentido(fc,PI*.62);return fc;}
 if(K==='b41'){fundoV();vista(480,560,120);EVITA=[[500,250,700,330],[560,620,620,680]];papelTela(.5);await logo();canto('O REDEMOINHO NO CÍRCULO');
  const fc=palcoB4();const t=PI/4,p=fc(t),T=[-Math.sin(t),Math.cos(t)];
  seta(p,[p[0]+.9*T[0],p[1]+.9*T[1]],CAMPO,6,20);const o=[.16*Math.cos(t),.16*Math.sin(t)];seta([p[0]+o[0],p[1]+o[1]],[p[0]+o[0]+.9*T[0],p[1]+o[1]+.9*T[1]],VIO,5,18);ponto(p,BR,8);
  tex('\\Fv',P(p[0]+.9*T[0],p[1]+.9*T[1])[0]-30,P(p[0]+.9*T[0],p[1]+.9*T[1])[1]-14,32,'c',true);tex('\\gp',P(p[0]+o[0]+.9*T[0],p[1]+o[1]+.9*T[1])[0]+30,P(p[0]+o[0]+.9*T[0],p[1]+o[1]+.9*T[1])[1]-6,32,'c',true);
  tex('R',P(RA*.5*Math.cos(-PI/5),RA*.5*Math.sin(-PI/5))[0]+10,P(RA*.5*Math.cos(-PI/5),RA*.5*Math.sin(-PI/5))[1]+20,32,'c');linha([[0,0],[RA*Math.cos(-PI/5),RA*Math.sin(-PI/5)]],GEO,2);
  legq('F = (−y, x): GIRA EM VOLTA DA ORIGEM',120,1020,CAMPO,28);legq('CÍRCULO DE RAIO R',700,1020,HEL,28);
  tex('\\Fv(\\X,\\Y)=(-\\Y,\\ \\X)',COL,190,48);
  tex('\\g(\\Tt)=(R\\cos\\Tt,\\ R\\sen\\Tt),\\quad 0\\le\\Tt\\le2\\pi',COL,285,42);
  tex('①\\ \\ \\Fv(\\g(\\Tt))=(-R\\sen\\Tt,\\ R\\cos\\Tt)',COL,380,42);
  tex('②\\ \\ \\gp(\\Tt)=(-R\\sen\\Tt,\\ R\\cos\\Tt)',COL,470,42);
  tex('③\\ \\ \\Fv(\\g(\\Tt))\\cdot\\gp(\\Tt)=R^2\\sen^2\\Tt+R^2\\cos^2\\Tt',COL,565,38);
  tex('=R^2(\\sen^2\\Tt+\\cos^2\\Tt)=R^2',COL+92,640,38);
  caixaMen(tex('W=\\int_0^{2\\pi}R^2\\,\\dTt=R^2\\Big[\\Tt\\Big]_0^{2\\pi}=R^2(2\\pi-0)=2\\pi R^2',COL,770,40),16);}
 if(K==='b42'){fundoV();vista(480,560,120);papelTela(.5);await logo();canto('CONFERINDO PELA SOMA, NA MÃO');
  const fc=palcoB4({campoOn:false,circ:GEO});const n=8;for(let i=1;i<=n;i++)seta(fc(2*PI*(i-1)/n),fc(2*PI*i/n),VIO,4,15);for(let i=0;i<n;i++)ponto(fc(2*PI*i/n),BR,7);
  linha([[0,0],fc(0)],GEO,2);linha([[0,0],fc(2*PI/n)],GEO,2);x.strokeStyle=BR;x.lineWidth=2;x.beginPath();x.arc(...P(0,0),60,-PI/4,0);x.stroke();tex('\\tfrac{2\\pi}{n}',P(0,0)[0]+88,P(0,0)[1]-30,30,'c',true);
  legq('n = 8 PEDAÇOS IGUAIS',120,1020,VIO,28);
  tex('\\Fv(\\g(\\Tt_i))\\cdot\\Dg_i=(-R\\sen\\Tt_i)(R\\cos\\Tt_i-R\\cos\\Tt_{i-1})',COL-40,185,34);
  tex('+(R\\cos\\Tt_i)(R\\sen\\Tt_i-R\\sen\\Tt_{i-1})',COL+160,250,34);
  tex('=R^2(\\sen\\Tt_i\\cos\\Tt_{i-1}-\\cos\\Tt_i\\sen\\Tt_{i-1})',COL+160,330,36);
  tex('=R^2\\sen(\\Tt_i-\\Tt_{i-1})=R^2\\sen\\tfrac{2\\pi}{n}',COL+160,415,40);
  tex('\\sum_i=n\\,R^2\\sen\\tfrac{2\\pi}{n}',COL,520,46);
  tex('n=4:\\ 4R^2\\qquad n=8:\\ \\approx5{,}66R^2\\qquad n=16:\\ \\approx6{,}12R^2',COL,625,36);
  const e=tex('n\\to\\infty:\\ \\ n\\sen\\tfrac{2\\pi}{n}\\to2\\pi\\ \\Rightarrow\\ 2\\pi R^2\\approx6{,}28R^2',COL,735,42);const r=e.getBoundingClientRect();check(r.right+34,735,MEN,1.1);}
 if(K==='b43'){fundoV();vista(480,560,120);EVITA=[[280,580,440,650],[470,480,730,580]];papelTela(.5);await logo();canto('NO RAIO: A FORÇA DE LADO');
  const fc=palcoB4({campoOn:true,circ:GEO});x.strokeStyle=LI;x.lineWidth=5;x.beginPath();x.arc(...P(0,0),RA*U,0,7);x.stroke();
  linha([[0,0],[RA,0]],HEL,7);seta([1.2,0],[1.55,0],HEL,7,24);for(const t of [.5,1,1.5,2])setaCampo([t,0],[0,t],{k:.32,mx:1,w:5,head:16});
  {const q=P(-1.6,-.45);x.fillStyle='#16123A';x.fillRect(q[0]-10,q[1]-26,148,50);}mixl([['t','ÁREA',LI],['m','\\Lim{\\pi R^2}']],P(-1.6,-.45)[0],P(-1.6,-.45)[1],32);
  legq('SEGMENTO DA ORIGEM ATÉ (R, 0)',120,1020,HEL,28);legq('F SEMPRE DE LADO',680,1020,CAMPO,28);
  tex('\\g(\\Tt)=(\\Tt,\\ 0),\\quad 0\\le\\Tt\\le R',COL,190,46);
  tex('\\Fv(\\g(\\Tt))=(0,\\ \\Tt),\\qquad \\gp(\\Tt)=(1,\\ 0)',COL,290,44);
  caixaMen(tex('\\Fv(\\g(\\Tt))\\cdot\\gp(\\Tt)=0\\cdot1+\\Tt\\cdot0=0\\ \\Rightarrow\\ W=\\int_0^R0\\,\\dTt=0',COL,395,38),14);
  selo('MESMO CAMPO, OUTRO CAMINHO, OUTRO TRABALHO',COL,520,GEO,30);
  mixl([['t','NA VOLTA:',BR],['m','2\\pi R^2=2\\cdot\\pi R^2'],['t','= 2 × ÁREA DO DISCO',LI]],COL,640,42);}

 // 10–11 · B5 · o vento que sopra para fora
 const fp=t=>[t,t*t];
 function palcoB5(cores=false){eixos2(-1.8,1.85,-.75,2.45);for(const v of [-1,1])tex(String(v),P(v,0)[0],P(v,0)[1]+28,26,'c');tex('1',P(0,1)[0]-22,P(0,1)[1],26,'c');
  campoG((X,Y)=>[X,Y],[-1.75,-1.25,-.75,-.25,.25,.75,1.25,1.75],[-.25,.25,.75,1.25,1.75,2.25],{k:.28,mx:.4,curvas:[amostra(fp,-1.2,1.2,200),amostra(t=>[Math.SQRT2*Math.cos(t),Math.SQRT2*Math.sin(t)],-.2,PI+.2,120)],folga:.1,evitaPx:[[30,440,420,500],[700,440,920,500],[200,770,280,820],[680,770,760,820],[420,500,470,540]]});
  if(cores){curvaF(fp,-1,0,AL,7);curvaF(fp,0,1,LI,7);}else curvaF(fp,-1,1,HEL,6);sentido(fp,-.45,cores?AL:HEL);sentido(fp,.55,cores?LI:HEL);
  ponto([-1,1],BR,9);ponto([1,1],BR,9);tex('\\g(-1)=(-1,\\ 1)',P(-1,1)[0]-20,P(-1,1)[1]-40,28,'r',true);tex('\\g(1)=(1,\\ 1)',P(1,1)[0]+20,P(1,1)[1]-40,28,'l',true);}
 if(K==='b51'){fundoV();vista(480,760,240);papelTela(.25);await logo();canto('O VENTO QUE SOPRA PARA FORA');palcoB5(false);
  legq('F = (x, y): EMPURRA PARA LONGE DA ORIGEM',120,1020,CAMPO,28);
  tex('\\Fv(\\X,\\Y)=(\\X,\\ \\Y)',COL,185,46);
  tex('\\g(\\Tt)=(\\Tt,\\ \\Tt^2),\\quad -1\\le\\Tt\\le1',COL,275,44);
  tex('①\\ \\ \\Fv(\\g(\\Tt))=(\\Tt,\\ \\Tt^2)\\qquad ②\\ \\ \\gp(\\Tt)=(1,\\ 2\\Tt)',COL,365,40);
  tex('③\\ \\ \\Fv(\\g(\\Tt))\\cdot\\gp(\\Tt)=\\Tt\\cdot1+\\Tt^2\\cdot2\\Tt=\\Tt+2\\Tt^3',COL,455,40);
  tex('W=\\int_{-1}^{1}(\\Tt+2\\Tt^3)\\,\\dTt=\\Big[\\dfrac{\\Tt^2}{2}+\\dfrac{\\Tt^4}{2}\\Big]_{-1}^{1}',COL,575,42);
  caixaMen(tex('=\\Big(\\tfrac12+\\tfrac12\\Big)-\\Big(\\tfrac12+\\tfrac12\\Big)=1-1=0',COL+70,700,42),14);}
 if(K==='b52'){fundoV();vista(480,760,240);papelTela(.25);await logo();canto('POR QUE DEU ZERO');palcoB5(true);
  x.strokeStyle=GEO;x.lineWidth=2.5;x.setLineDash([10,8]);x.beginPath();x.arc(...P(0,0),Math.SQRT2*U,-PI*1.07,PI*.07,false);x.stroke();x.setLineDash([]);
  tex('\\sqrt2',P(-.55,.62)[0]-6,P(-.55,.62)[1],30,'c',true);linha([[0,0],[-1,1]],GEO,2);
  legq('IDA ATÉ A ORIGEM: CONTRA',120,1020,AL,28);legq('VOLTA: A FAVOR',560,1020,LI,28);
  mixl([['t','IDA:',AL],['m','\\int_{-1}^{0}(\\Tt+2\\Tt^3)\\,\\dTt=0-1=\\Al{-1}']],COL,190,42);
  mixl([['t','VOLTA:',LI],['m','\\int_{0}^{1}(\\Tt+2\\Tt^3)\\,\\dTt=1-0=\\Lim{+1}']],COL,300,42);
  mixl([['m','\\dfrac{\\Tt^2}{2}+\\dfrac{\\Tt^4}{2}=\\dfrac12(\\X^2+\\Y^2)'],['t','NO PONTO',GEO],['m','\\g(\\Tt)']],COL,420,42);
  const e=mixl([['t','AS DUAS PONTAS À DISTÂNCIA',BR],['m','\\sqrt2\\ \\Rightarrow\\ W=0']],COL,545,42);check(e+20,545,MEN,1.1);
  selo('SÓ IMPORTAM AS PONTAS: CAMPO CONSERVATIVO',COL,660,MEN,30);}

 // 12 · B6-1 · outra notação
 if(K==='b61'){fundoV();vista(960,540,120);papelTela(.5);await logo();canto('OUTRA NOTAÇÃO');
  painel2d(1420,150,440,300);{const ox=1480,oy=410,f=s=>[ox+40+320*s,oy-40-170*s-50*Math.sin(PI*s)];x.strokeStyle=HEL;x.lineWidth=5;x.beginPath();for(let i=0;i<=60;i++){const q=f(i/60);i?x.lineTo(...q):x.moveTo(...q);}x.stroke();
   setaPx([ox,oy],[ox+400,oy],E1,3,14);setaPx([ox,oy],[ox,oy-240],E2,3,14);const q=f(.55);pontoPx(q,BR,8);guia(q,[q[0],oy]);guia(q,[ox,q[1]]);
   tex('\\X(\\Tt)',q[0],oy+24,26,'c');tex('\\Y(\\Tt)',ox-12,q[1],26,'r');}
  tex('\\Fv=(P,\\ Q),\\qquad \\g(\\Tt)=(\\X(\\Tt),\\ \\Y(\\Tt))',120,215,48);
  tex('\\Fv(\\g(\\Tt))\\cdot\\gp(\\Tt)\\,\\dTt=P(\\X(\\Tt),\\Y(\\Tt))\\,\\X\'(\\Tt)\\,\\dTt+Q(\\X(\\Tt),\\Y(\\Tt))\\,\\Y\'(\\Tt)\\,\\dTt',120,330,40);
  mixl([['m','\\dX=\\X\'(\\Tt)\\,\\dTt,\\qquad \\dY=\\Y\'(\\Tt)\\,\\dTt'],['t','A MESMA DA SUBSTITUIÇÃO',GEO]],120,445,44);
  caixaMen(tex('\\int_{\\g}\\Fv\\cdot\\dg=\\int_{\\g}P\\,\\dX+Q\\,\\dY',120,575,54),18);
  mixl([['t','NO ESPAÇO:',GEO],['m','\\Fv=(P,\\ Q,\\ R)\\ \\Rightarrow\\ \\int_{\\g}P\\,\\dX+Q\\,\\dY+R\\,\\dZ']],120,705,46);
  chipMix([['t','NÃO É',AL],['m','\\int'],['t','EM x MAIS',AL],['m','\\int'],['t','EM y: VOLTA SEMPRE PARA O',AL],['m','\\Tt']],120,820,AL,32);
  mixl([['t','REDEMOINHO:',CAMPO],['m','\\int_{\\g}-\\Y\\,\\dX+\\X\\,\\dY']],120,940,46);}

 // 13 · B6-2 · a elipse
 if(K==='b62'){fundoV();vista(480,560,150);papelTela(.4);await logo();canto('A ELIPSE E O DOBRO DA ÁREA');
  eixos2(-2.9,3.0,-2.2,2.4);const fe=t=>[2*Math.cos(t),Math.sin(t)];x.strokeStyle=LI;x.lineWidth=11;x.beginPath();x.ellipse(...P(0,0),2*U,U,0,0,7);x.stroke();curvaF(fe,0,2*PI,HEL,5);sentido(fe,PI*.55);
  for(const t of [PI/4,3*PI/4,5*PI/4,7*PI/4]){const p=fe(t);setaCampo(p,Frd(...p),{k:.38,mx:.8,w:4,head:15});}
  linha([[0,0],[2,0]],E1,4);linha([[0,0],[0,1]],E2,4);tex('\\textcolor{#FFC24D}{2}',P(1,0)[0],P(1,0)[1]+26,30,'c');tex('\\textcolor{#EA63FF}{1}',P(0,.5)[0]-20,P(0,.5)[1],30,'c');
  mixl([['t','ÁREA',LI],['m','\\Lim{=2\\pi}']],P(-1.45,-.45)[0],P(-1.45,-.45)[1],30);
  legq('x = 2 cos t, y = sen t',120,1020,HEL,28);legq('REDEMOINHO',560,1020,CAMPO,28);
  tex('\\int_{\\g}-\\Y\\,\\dX+\\X\\,\\dY,\\qquad \\X=2\\cos\\Tt,\\ \\Y=\\sen\\Tt,\\ 0\\le\\Tt\\le2\\pi',COL-40,180,36);
  tex('\\dX=-2\\sen\\Tt\\,\\dTt,\\qquad \\dY=\\cos\\Tt\\,\\dTt',COL,270,42);
  tex('-\\Y\\,\\dX=-\\sen\\Tt\\cdot(-2\\sen\\Tt\\,\\dTt)=2\\sen^2\\Tt\\,\\dTt',COL,360,40);
  tex('\\X\\,\\dY=2\\cos\\Tt\\cdot\\cos\\Tt\\,\\dTt=2\\cos^2\\Tt\\,\\dTt',COL,450,40);
  tex('-\\Y\\,\\dX+\\X\\,\\dY=2(\\sen^2\\Tt+\\cos^2\\Tt)\\,\\dTt=2\\,\\dTt',COL,540,40);
  caixaMen(tex('\\int_0^{2\\pi}2\\,\\dTt=2\\Big[\\Tt\\Big]_0^{2\\pi}=4\\pi',COL,650,46),14);
  const e=mixl([['t','ÁREA DA ELIPSE',LI],['m','=\\pi\\cdot2\\cdot1=2\\pi\\ \\Rightarrow\\ 4\\pi=2\\times'],['t','ÁREA',LI]],COL,780,40);check(e+18,780,MEN,1.1);
  chipMix([['t','CÍRCULO:',GEO],['m','2\\pi R^2=2\\times'],['t','ÁREA',GEO]],COL,890,GEO,32);}

 // 14–16 · B7 · a hélice da lata
 // ===== v2: a lata desenhada em PROJEÇÃO OBLÍQUA no próprio papel (sem Three.js, sem piso) =====
 // tela: X = CX + U·x ;  Y = CY − U·(z + k·y).  Verticais da lata = linhas do papel; x = ±1 cai em linha; z = 0, ½, 1 caem em linha.
 // atrás (y > 0) = traço tracejado mais apagado (cor sólida, sem transparência).
function linhaPx(pts,cor,w,{dash=null}={}){x.lineCap='round';x.lineJoin='round';x.setLineDash(dash||[]);x.beginPath();pts.forEach((q,i)=>i?x.lineTo(...q):x.moveTo(...q));x.strokeStyle=cor;x.lineWidth=w;x.stroke();x.setLineDash([]);}
 const HELB='#8E6C55',GEOB='#5E6788';
 function Lata(CX,CY,U,k){
  const pr=(X,Y,Z)=>[CX+U*X,CY-U*(Z+k*Y)];
  const ell=(z,t0,t1,cor,w,dash)=>{const n=120,pts=[];for(let i=0;i<=n;i++){const t=t0+(t1-t0)*i/n;pts.push(pr(Math.cos(t),Math.sin(t),z));}linhaPx(pts,cor,w,{dash});};
  const hel=(c,t0,t1,cor,w,corB=HELB)=>{const n=400;let seg=[],back=null;const flush=()=>{if(seg.length>1)linhaPx(seg,back?corB:cor,back?3:w,{dash:back?[12,9]:null});seg=[];};
   for(let i=0;i<=n;i++){const t=t0+(t1-t0)*i/n,b=Math.sin(t)>0;if(back!==null&&b!==back){const q=seg[seg.length-1];flush();seg=[q];}back=b;seg.push(pr(Math.cos(t),Math.sin(t),c*t));}flush();};
  const lata=(H=1)=>{ell(0,0,PI,GEOB,2,[8,8]);ell(0,PI,2*PI,GEO,2);ell(H,0,2*PI,GEO,2);linhaPx([pr(-1,0,0),pr(-1,0,H)],GEO,2);linhaPx([pr(1,0,0),pr(1,0,H)],GEO,2);};
  const eixo=(z1)=>{setaPx(pr(0,0,0),pr(0,0,z1),EZ,3,16);};
  const F=(t,c,s,w=4,head=16)=>{const p=pr(Math.cos(t),Math.sin(t),c*t);const f=[-Math.sin(t),Math.cos(t),-1];const q=[p[0]+U*s*f[0],p[1]-U*s*(f[2]+k*f[1])];setaPx(p,q,CAMPO,w,head);return [p,q];};
  return {pr,ell,hel,lata,eixo,F};}
 const C4=1/(4*PI);

 // 01 · H1 (v2)
 if(K==='h1'){fundoV();U=120;O=[0,0];papelTela(.5);await logo();canto('A HÉLICE NA PAREDE DA LATA');
  const L=Lata(480,780,300,.2);L.lata();L.eixo(1.36);tex('\\Z',480,330,38,'c');
  L.hel(C4,0,4*PI,HEL,5);const tc=1.62*PI;const [p,q]=L.F(tc,C4,.42,5,20);pontoPx(p,BR,11);tex('\\Fv',q[0]+26,q[1]+8,36,'c');
  legq('HÉLICE NA PAREDE DA LATA',120,1020,HEL);legq('A FORÇA EMPURRA A CONTA',560,1020,CAMPO);
  leg('LATA: RAIO 1, ALTURA 1',COL,190,GEO,'left',30);
  tex('\\g(\\Tt)=(\\cos\\Tt,\\ \\sen\\Tt,\\ c\\,\\Tt)',COL,275,48);
  mixl([['m','\\Fv'],['t','= UMA FORÇA EM CADA PONTO',BR]],COL,370,42);
  txt('QUANTO TRABALHO',COL,480,{size:48,cor:CI});txt('NUMA VOLTA?',COL,540,{size:48,cor:CI});
  leg('VOLUME? ÁREA?',COL,650,GEO,'left',30);leg('A CURVA NÃO TEM NENHUM DOS DOIS',COL,695,GEO,'left',30);}

 // 14–16 · B7 (v2): lata U = 240, k = ¼, centro da base (300, 780); 1ª volta laranja, 2ª volta só no traço GEO apagado
 if(K==='b71'||K==='b72'||K==='b73'){fundoV();U=120;O=[0,0];papelTela(.5);await logo();
  const L=Lata(300,780,240,.25);
  if(K==='b73'){L.ell(0,PI,2*PI,LI,4);L.ell(0,0,PI,'#7E9A48',3,[10,8]);} // tampa de baixo em lima (atrás: lima escuro tracejado)
  L.lata();L.eixo(1.38);tex('\\Z',300,415,34,'c');
  L.hel(C4,2*PI,4*PI,GEOB,2,GEOB);L.hel(C4,0,2*PI,HEL,6);
  for(const t of [1.2*PI,1.5*PI,1.78*PI])L.F(t,C4,.28,4,15);
  const p0=L.pr(1,0,0),p1=L.pr(1,0,.5);pontoPx(p0,BR,9);pontoPx(p1,BR,9);
  tex('\\Tt=0',p0[0]+22,p0[1]+10,26,'l');tex('\\Tt=2\\pi',p1[0]+22,p1[1]+10,26,'l');
  const C7=COLC;
  if(K==='b71'){canto('A HÉLICE DA LATA: MONTANDO');legq('UMA VOLTA: 0 ≤ t ≤ 2π',120,1020,HEL,28);legq('F = REDEMOINHO + PESO',470,1020,CAMPO,28);
   tex('\\g(\\Tt)=(\\cos\\Tt,\\ \\sen\\Tt,\\ c\\,\\Tt),\\quad 0\\le\\Tt\\le2\\pi',C7,190,46);
   tex('\\Fv(\\X,\\Y,\\Z)=(-\\Y,\\ \\X,\\ -1)',C7,290,48);
   const e=chipMix([['t','REDEMOINHO: AJUDA',LI]],C7,390,LI,32);chipMix([['t','PESO: ATRAPALHA',AL]],e+30,390,AL,32);
   tex('W=\\int_{\\g}-\\Y\\,\\dX+\\X\\,\\dY-\\dZ',C7,500,50);
   tex('\\dX=-\\sen\\Tt\\,\\dTt,\\quad \\dY=\\cos\\Tt\\,\\dTt,\\quad \\dZ=c\\,\\dTt',C7,610,44);}
  if(K==='b72'){canto('A HÉLICE DA LATA: A CONTA');legq('UMA VOLTA: 0 ≤ t ≤ 2π',120,1020,HEL,28);legq('F = REDEMOINHO + PESO',470,1020,CAMPO,28);
   chip('W=\\int_{\\g}-\\Y\\,\\dX+\\X\\,\\dY-\\dZ',C7,180,30);
   tex('-\\Y\\,\\dX=-\\sen\\Tt\\cdot(-\\sen\\Tt\\,\\dTt)=\\sen^2\\Tt\\,\\dTt',C7,285,42);
   tex('\\X\\,\\dY=\\cos\\Tt\\cdot\\cos\\Tt\\,\\dTt=\\cos^2\\Tt\\,\\dTt',C7,375,42);
   tex('-\\dZ=-c\\,\\dTt',C7,460,42);
   tex('W=\\int_0^{2\\pi}(\\Me{\\sen^2\\Tt+\\cos^2\\Tt}-c)\\,\\dTt=\\int_0^{2\\pi}(1-c)\\,\\dTt',C7,565,42);
   tex('=(1-c)\\Big[\\Tt\\Big]_0^{2\\pi}=(1-c)(2\\pi-0)',C7+40,670,42);
   caixaMen(tex('=2\\pi-2\\pi c',C7+40,775,52),16);}
  if(K==='b73'){canto('LENDO A RESPOSTA');
   const R0=[p0[0]+120,p0[1]],R1=[p1[0]+120,p1[1]];linhaPx([R0,R1],EZ,4);linhaPx([[R0[0]-10,R0[1]],[R0[0]+10,R0[1]]],EZ,3);linhaPx([[R1[0]-10,R1[1]],[R1[0]+10,R1[1]]],EZ,3);
   tex('\\textcolor{#5AA2FF}{2\\pi c}',R0[0]+16,(R0[1]+R1[1])/2+10,28,'l');
   legq('TAMPA: ÁREA π · 1²',120,1020,LI,28);legq('SUBIDA NUMA VOLTA',470,1020,EZ,28);
   chip('W=2\\pi-2\\pi c',C7,180,32);
   mixl([['m','2\\pi=2\\cdot(\\pi\\cdot1^2)=2\\times'],['t','ÁREA DA TAMPA',LI],['t','· REDEMOINHO',GEO]],C7,285,40);
   mixl([['m','2\\pi c=\\Z(2\\pi)-\\Z(0)'],['t','= SUBIDA NUMA VOLTA',EZ]],C7,385,40);
   mixl([['m','\\Rightarrow\\ -2\\pi c=-1\\times'],['t','SUBIDA',EZ],['t','· PESO',GEO]],C7+40,465,40);
   mixl([['t','NOSSA LATA: 2 VOLTAS SOBEM 1',GEO],['m','\\Rightarrow\\ 2\\pi c=\\tfrac12\\ \\Rightarrow\\ c=\\tfrac{1}{4\\pi}']],C7,570,38);
   const r=caixaMen(tex('W=2\\pi-\\tfrac12\\approx5{,}78>0',C7,685,50),16);leg('O REDEMOINHO GANHA',r.right+40,698,LI,'left',30);
   tex('W=0\\iff 2\\pi-2\\pi c=0\\iff c=1',C7,810,44);}}

 // 17 · S1 · síntese
 if(K==='s1'){fundoV();vista(960,540,120);papelTela(.5);await logo();canto('RESUMO');
  const cw=580;[[60,'① DEFINIÇÃO'],[670,'② OUTRA NOTAÇÃO'],[1280,'③ O SINAL']].forEach(([X,t])=>{cartao(X,200,cw,440);txt(t,X+30,262,{size:32,cor:GEO});});
  tex('\\int_{\\g}\\Fv\\cdot\\dg=',90,380,44);tex('\\int_a^b \\Fv(\\g(\\Tt))\\cdot\\gp(\\Tt)\\,\\dTt',110,490,40);
  tex('\\int_{\\g}P\\,\\dX+Q\\,\\dY+R\\,\\dZ',700,430,44);leg('SEMPRE VOLTANDO PARA O t',700,540,GEO,'left',28);
  mixl([['m','>0'],['t','AJUDA',LI]],1310,370,44);mixl([['m','=0'],['t','DE LADO',GEO]],1310,460,44);mixl([['m','<0'],['t','ATRAPALHA',AL]],1310,550,44);
  cartao(60,740,1800,200);
  txt('REDEMOINHO: DEPENDE DO CAMINHO',100,815,{size:32,cor:CAMPO});txt('F = (x, y): SÓ AS PONTAS',780,815,{size:32,cor:MEN});txt('VOLTA FECHADA: 2 × ÁREA',1340,815,{size:32,cor:LI});
  mixl([['m','2\\pi R^2'],['t','E',GEO],['m','0']],100,885,32);tex('W=0',780,885,32);tex('4\\pi=2\\cdot2\\pi',1340,885,32);}

 // 18 · S2 · mais rápido, ao contrário, com quina
 if(K==='s2'){fundoV();vista(320,560,110);papelTela(.5);await logo();canto('MAIS RÁPIDO, AO CONTRÁRIO, COM QUINA');
  eixos2(-2.6,2.8,-2.6,2.7,{lx:true});const fc=t=>[RA*Math.cos(t),RA*Math.sin(t)];curvaF(fc,0,2*PI,HEL,6);sentido(fc,PI*.6);
  const fo=t=>[2.4*Math.cos(t),2.4*Math.sin(t)];linha(arco2(fo,PI*1.1,PI*1.5,40),AL,4);sentido(t=>fo(-t),-PI*1.32,AL);
  const sq=[[3.3,-1.0],[5.1,-1.0],[5.1,0.8],[3.3,0.8],[3.3,-1.0]];linha(sq,HEL,6,{dash:[14,10]});for(const p of sq.slice(0,4)){ponto(p,AL,10);}
  legq('MESMA VOLTA',120,1020,HEL,28);legq('AO CONTRÁRIO',420,1020,AL,28);legq('QUINAS',720,1020,AL,28);
  tex('\\g_1(\\Tt)=(R\\cos\\Tt,\\ R\\sen\\Tt),\\quad 0\\le\\Tt\\le2\\pi',COL,200,42);
  tex('\\g_2(\\uu)=(R\\cos2\\uu,\\ R\\sen2\\uu),\\quad 0\\le\\uu\\le\\pi',COL,300,42);
  leg('DUAS VEZES MAIS RÁPIDO: W MUDA?',COL,370,CI,'left',32);
  txt('AO CONTRÁRIO? COM QUINA?',COL,465,{size:40});
  cartao(1060,560,760,330);txt('NO PRÓXIMO VÍDEO',1440,635,{size:30,f:'SGM',cor:GEO,al:'center'});
  txt('MUDANÇA DE PARÂMETRO',1440,720,{size:48,al:'center'});txt('E CAMINHOS COM QUINA',1440,790,{size:48,cor:HEL,al:'center'});leg('O MESMO TRABALHO?',1440,850,GEO,'center',28);}
