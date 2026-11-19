 function painel2d(X0,Y0,w,h){x.save();x.fillStyle='#16123A';x.beginPath();x.roundRect(X0,Y0,w,h,14);x.fill();x.clip();
  x.strokeStyle='#2B2558';x.lineWidth=1.2;const s=30;for(let X=X0;X<=X0+w;X+=s){x.beginPath();x.moveTo(X+.5,Y0);x.lineTo(X+.5,Y0+h);x.stroke();}
  for(let Y=Y0;Y<=Y0+h;Y+=s){x.beginPath();x.moveTo(X0,Y+.5);x.lineTo(X0+w,Y+.5);x.stroke();}x.restore();painel(X0,Y0,w,h,{a:.45});}
 function arcoPx(c,R,a0,a1,cor,w=4){x.strokeStyle=cor;x.lineWidth=w;x.beginPath();x.arc(...P(...c),R,-a1,-a0);x.stroke();}
 function retTrac(X0,Y0,w,h,cor){x.strokeStyle=cor;x.lineWidth=2.5;x.setLineDash([10,7]);x.beginPath();x.roundRect(X0,Y0,w,h,8);x.stroke();x.setLineDash([]);}
 function placaTxt(s,X,Y,cor,size=28,al='left'){leg(s,X,Y,cor,al,size,true);}
 const COL=1010;

 // 01 · H1 · a lata pesada
 if(K==='h1'){fundoV();await logo();canto('A LATA PESADA');const o={dx:-110,dy:20,esc:1};await cena3d('lata',o);
  for(const [n,s] of [['ex','\\X'],['ey','\\Y'],['ez','\\Z']])rotulo3('lata',n,s,{...o,size:38,al:'c'});
  let q=Q3('lata','fundo',o);placaTxt('LEVE NA ORIGEM',q[0]-60,q[1]+120,CI,28,'center');guia([q[0]-60,q[1]+92],q);
  q=Q3('lata','quina',o);placaTxt('PESADA NA QUINA',q[0]-300,q[1]+110,CI,28);guia([q[0]-60,q[1]+84],q);
  mixl([['t','DENSIDADE',CI],['m','\\de=\\Ci{\\sqrt{\\X^2+\\Y^2+\\Z^2}}']],COL,190,44);
  mixl([['t','LATA',GEO],['m','\\X^2+\\Y^2\\le 1,\\quad 0\\le\\Z\\le 1']],COL,280,40);
  mixl([['t','MASSA',GEO],['m','M=\\iiint \\de\\,dV']],COL,370,44);
  tex('\\int_{-1}^{1}\\!\\int_{-\\sqrt{1-\\X^2}}^{\\sqrt{1-\\X^2}}\\!\\int_0^1\\Ci{\\sqrt{\\X^2+\\Y^2+\\Z^2}}\\,\\dZ\\,\\dY\\,\\dX',COL,480,40);
  tex('\\Big[\\dfrac{\\Z\\sqrt{k^2+\\Z^2}}{2}+\\dfrac{k^2}{2}\\ln\\!\\big(\\Z+\\sqrt{k^2+\\Z^2}\\big)\\Big]_0^1',COL,600,36);
  leg('COM k² = x² + y²',COL+700,665,GEO,'left',24);selo('TRAVA',COL,712,AL,30);
  painel2d(COL,760,400,272);txt('EM ESFÉRICAS',COL+20,800,{size:26,f:'SGM',cor:GEO});
  vista(COL+50,1010,180);preenche([[0,0],[1,0],[1,1],[0,1]],mix('#16123A',GEO,.25));linha([[1,0],[1,1],[0,1]],GEO,3);linha([[0,0],[1,1]],AL,3,{dash:[9,7]});
  const a=PI/3,pw=[1,1/Math.tan(a)],b=PI/8,pt=[Math.tan(b),1];linha([[0,0],pw],RO,5);linha([[0,0],pt],RO,5);pontoPx(P(0,0),AZC,8);ponto(pw,CORAL,8);ponto(pt,CORAL,8);
  leg('A SONDA BATE NA PAREDE',COL+430,850,GEO,'left',28);leg('OU NA TAMPA:',COL+430,890,GEO,'left',28);leg('RACHA NA QUINA',COL+430,950,AL,'left',30);}

 // 02 · H2 · a grade da lata
 if(K==='h2'){fundoV();await logo();canto('QUAL É O VOLUME DE CADA PEDAÇO?');const o={dx:-80,dy:90,esc:1};await cena3d('grade',o);
  rotulo3('grade','ez','\\Z',{...o,size:38,ox:30,oy:40});
  let q=Q3('grade','celEixo',o);txt('?',q[0]-40,q[1]-40,{size:64,cor:LI});q=Q3('grade','celPar',o);txt('?',q[0]+30,q[1]-50,{size:64,cor:LI});
  painel(1080,250,760,480,{fill:'rgba(19,16,48,.92)'});txt('A GRADE DA LATA',1120,320,{size:34});
  mixl([['t','CILINDROS',SOMB],['m','\\S=\\text{cte}']],1120,410,40);mixl([['t','PÁGINAS',TH],['m','\\T=\\text{cte}']],1120,490,40);
  mixl([['t','ANDARES',EZ],['m','\\Z=\\text{cte}']],1120,570,40);mixl([['t','MESMO',GEO],['m','\\DS,\\ \\DT,\\ \\DZ']],1120,670,40);}

 // 03 · B1-1 · o endereço
 if(K==='b11'){fundoV();await logo();canto('O ENDEREÇO CILÍNDRICO');const o={dx:-90,dy:30,esc:.95};await cena3d('ponto',o);
  for(const [n,s] of [['ex','\\X'],['ey','\\Y'],['ez','\\Z']])rotulo3('ponto',n,s,{...o,size:38,al:'c'});
  rotulo3('ponto','P','P',{...o,size:38,ox:18,oy:-26});rotulo3('ponto','meioS','\\S',{...o,size:40,ox:-10,oy:34});rotulo3('ponto','arcoTh','\\T',{...o,size:38,ox:16,oy:20});
  rotulo3('ponto','meioZ','\\Z',{...o,size:40,ox:18});rotulo3('ponto','meioR','\\R',{...o,size:38,ox:-40,oy:-20});
  let q=Q3('ponto','meioFio',o);placaTxt('DISTÂNCIA AO EIXO',q[0]-80,q[1]-70,SOMB,26);
  // painel DE CIMA
  painel2d(COL,150,410,330);txt('DE CIMA',COL+20,190,{size:26,f:'SGM',cor:GEO});vista(COL+80,440,120);
  seta([0,0],[2.6,0],E1,3,14);seta([0,0],[0,2.0],E2,3,14);const P1=[1,Math.sqrt(3)];linha([[0,0],P1],SOMB,5);linha([P1,[1,0]],E1,2,{dash:[6,6]});linha([P1,[0,P1[1]]],E2,2,{dash:[6,6]});
  arcoPx([0,0],70,0,PI/3,TH,4);ponto(P1,SOMB,8);tex('\\S',P(.42,.95)[0],P(.42,.95)[1],34,'c');tex('\\T',P(.85,.22)[0],P(.85,.22)[1],32,'c');tex('\\X',P(2.6,0)[0]-14,P(2.6,0)[1]-26,30);tex('\\Y',P(0,2)[0]+14,P(0,2)[1]+6,30);
  // painel DE LADO
  painel2d(COL+440,150,420,330);txt('DE LADO',COL+460,190,{size:26,f:'SGM',cor:GEO});vista(COL+500,440,105);
  seta([0,0],[3.1,0],SOMB,3,14);seta([0,0],[0,2.2],EZ,3,14);const Q=[2,1.5];preenche([[0,0],[2,0],Q],mix('#16123A',TH,.18));linha([[0,0],[2,0]],SOMB,5);linha([[2,0],Q],EZ,5);linha([[0,0],Q],RO,5);ponto(Q,BR,8);
  tex('\\S',P(1,0)[0],P(1,0)[1]+26,32,'c');tex('\\Z',P(2,.75)[0]+24,P(2,.75)[1],32,'l');tex('\\R',P(.9,.85)[0]-10,P(.9,.85)[1]-18,32,'c');tex('\\S',P(3.1,0)[0]-6,P(3.1,0)[1]-26,28);tex('\\Z',P(0,2.2)[0]+14,P(0,2.2)[1]+6,28);
  tex('\\X=\\S\\cos\\T,\\qquad \\Y=\\S\\sen\\T,\\qquad \\Z=\\Z',COL,560,48);
  mixl([['m','\\S'],['t','= DISTÂNCIA AO EIXO z',SOMB]],COL,650,46);leg('NÃO É A DISTÂNCIA ATÉ A ORIGEM',COL,725,AL,'left',30);
  tex('\\R^2=\\S^2+\\Z^2',COL,810,52);tex('\\S\\ge 0,\\qquad 0\\le\\T<2\\pi',COL,910,44);}

 // 04 · B1-2 · um ponto de exemplo (etapa 1)
 if(K==='b12'){fundoV();await logo();canto('UM PONTO DE EXEMPLO');const o={dx:-90,dy:30,esc:.95};await cena3d('ponto',o);
  for(const [n,s] of [['ex','\\X'],['ey','\\Y'],['ez','\\Z']])rotulo3('ponto',n,s,{...o,size:38,al:'c'});
  rotulo3('ponto','P','P',{...o,size:38,ox:18,oy:-26});rotulo3('ponto','meioFio','\\Ro{}2',{...o,size:38,oy:-32,al:'c'});rotulo3('ponto','arcoTh','\\dfrac{\\pi}{3}',{...o,size:32,ox:16,oy:26});
  rotulo3('ponto','meioZ','\\dfrac32',{...o,size:34,ox:-56});rotulo3('ponto','xP','1',{...o,size:34,ox:-8,oy:30,al:'c'});rotulo3('ponto','yP','\\sqrt3',{...o,size:34,ox:40,oy:26,al:'c'});
  tex('(\\S,\\T,\\Z)=\\Big(2,\\ \\dfrac{\\pi}{3},\\ \\dfrac32\\Big)',COL,200,50);
  tex('\\X=2\\cos\\dfrac{\\pi}{3}=2\\cdot\\dfrac12=1',COL,340,48);
  tex('\\Y=2\\sen\\dfrac{\\pi}{3}=2\\cdot\\dfrac{\\sqrt3}{2}=\\sqrt3',COL,480,48);
  tex('\\Z=\\dfrac32',COL,610,48);
  tex('\\X^2+\\Y^2=1+3=4=2^2',COL,730,48);check(COL+640,730);
  leg('ETAPA 2 (RENOVA): r = √(4 + 9/4) = √(25/4) = 5/2 · O 3-4-5 PELA METADE',COL,860,GEO,'left',24);}

 // 05 · B1-3 · a caixa vira a lata
 if(K==='b13'){fundoV();await logo();canto('A CAIXA VIRA A LATA');const oc={dx:-60,dy:160,esc:.72},ol={dx:600,dy:210,esc:.58};await cena3d('caixa',oc);await cena3d('latagrade',ol);
  rotulo3('caixa','eS','\\S',{...oc,size:36,al:'c'});{const q=Q3('caixa','O',oc);tex('\\T',q[0]+95,q[1]-70,36,'c',true);}rotulo3('caixa','eZ','\\Z',{...oc,size:36,al:'c'});
  rotulo3('caixa','um_s','1',{...oc,size:32,oy:24,al:'c'});rotulo3('caixa','dois_pi','2\\pi',{...oc,size:32,oy:28,al:'c'});rotulo3('caixa','um_z','1',{...oc,size:32,ox:-26,al:'c'});
  setaPx([640,560],[760,560],GEO,4,18);tex('T',700,520,40,'c');
  let q=Q3('latagrade','eixo',ol);placaTxt('O EIXO',q[0]-130,q[1]+10,AL,26);
  mixl([['t','UMA CAIXA!',MEN]],1250,200,40);tex('0\\le\\S\\le 1,\\ \\ 0\\le\\T\\le 2\\pi,\\ \\ 0\\le\\Z\\le 1',1250,270,36);
  txt('BORDAS RUINS',1250,400,{size:32,cor:AL});mixl([['m','\\S=0'],['t','→ O EIXO (ACHATA)',GEO]],1250,470,36);
  mixl([['m','\\T=0'],['t','E',GEO],['m','\\T=2\\pi']],1250,560,36);leg('→ A MESMA PÁGINA (COLA)',1250,630,GEO,'left',28);leg('VOLUME ZERO',1250,720,MEN,'left',32);}

 // 06 · B2-1 · a caixinha curva
 if(K==='b21'){fundoV();await logo();canto('A CAIXINHA CURVA');const o={dx:-60,dy:30,esc:1};await cena3d('caixinha',o);
  let q=Q3('caixinha','dS',o);tex('\\DS',q[0]-80,q[1]+60,40,'c',true);guia([q[0]-60,q[1]+40],q);
  q=Q3('caixinha','arco',o);tex('\\S\\,\\DT',q[0]+90,q[1]+70,40,'c',true);guia([q[0]+60,q[1]+48],q);
  q=Q3('caixinha','dZ',o);tex('\\DZ',q[0]+80,q[1],40,'c',true);guia([q[0]+50,q[1]],q);
  q=Q3('caixinha','raio',o);tex('\\S',q[0]-10,q[1]-36,36,'c',true);
  mixl([['t','ARESTA 1:',GEO],['m','\\DS'],['t','ARESTA 3:',GEO],['m','\\DZ']],COL,190,40);
  mixl([['t','ARESTA 2:',GEO],['m','\\S\\,\\DT'],['t','ARCO = RAIO · ÂNGULO',TH]],COL,270,40);
  tex('\\Delta V\\approx \\DS\\cdot \\S\\DT\\cdot\\DZ=\\Js\\,\\DS\\,\\DT\\,\\DZ',COL,380,50);
  painel(COL,470,860,500,{fill:'rgba(19,16,48,.92)'});
  tex('\\DS=\\dfrac12,\\quad \\DT=\\dfrac{\\pi}{6},\\quad \\DZ=\\dfrac12',COL+30,550,40);
  mixl([['t','EIXO',GEO],['m','\\bar{\\S}=\\dfrac14\\ \\to\\ \\dfrac{\\pi}{96}\\approx 0{,}033']],COL+30,670,40);
  mixl([['t','PAREDE',GEO],['m','\\bar{\\S}=\\dfrac34\\ \\to\\ \\dfrac{\\pi}{32}\\approx 0{,}098']],COL+30,790,40);
  mixl([['t','RAZÃO',MEN],['m','\\Me{3}']],COL+30,895,40);leg('AQUI O ≈ É EXATO',COL+330,905,GEO,'left',28);}

 // 07 · B2-2 · polares vezes a altura
 if(K==='b22'){fundoV();vista(960,540,120);papelTela(.5);await logo();canto('POLARES VEZES A ALTURA');
  painel2d(60,170,560,560);txt('DE CIMA',84,212,{size:26,f:'SGM',cor:GEO});vista(110,690,440);
  const a0=PI/9,a1=PI/9+PI/6,s1=.62,s2=1.0;linha(arco2(a=>[Math.cos(a),Math.sin(a)],0,PI/2),'#4A4F78',2);
  const sec=[...arco2(a=>[s1*Math.cos(a),s1*Math.sin(a)],a0,a1),...arco2(a=>[s2*Math.cos(a),s2*Math.sin(a)],a1,a0)];preenche(sec,mix('#16123A',LI,.45));
  linha([[s1*Math.cos(a0),s1*Math.sin(a0)],[s2*Math.cos(a0),s2*Math.sin(a0)]],SOMB,5);linha(arco2(a=>[s2*Math.cos(a),s2*Math.sin(a)],a0,a1),TH,5);
  linha([[0,0],[s2*Math.cos(a0),s2*Math.sin(a0)]],SOMB,2,{dash:[7,6]});pontoPx(P(0,0),GEO,6);
  tex('\\DS',P(.82*Math.cos(a0),.82*Math.sin(a0))[0]+10,P(.82*Math.cos(a0),.82*Math.sin(a0))[1]+30,34,'c',true);
  tex('\\S\\,\\DT',P(1.06*Math.cos((a0+a1)/2),1.06*Math.sin((a0+a1)/2))[0]+40,P(1.06*Math.cos((a0+a1)/2),1.06*Math.sin((a0+a1)/2))[1],34,'l',true);
  painel2d(660,170,540,560);txt('DE LADO',684,212,{size:26,f:'SGM',cor:GEO});vista(720,690,300);
  seta([0,0],[1.6,0],SOMB,3,14);seta([0,0],[0,1.5],EZ,3,14);preenche([[.6,.3],[1.05,.3],[1.05,.95],[.6,.95]],mix('#16123A',LI,.45));linha([[1.05,.3],[1.05,.95]],EZ,5);linha([[.6,.3],[1.05,.3]],SOMB,5);
  tex('\\DZ',P(1.05,.62)[0]+20,P(1.05,.62)[1],34,'l',true);tex('\\DS',P(.82,.3)[0],P(.82,.3)[1]+30,32,'c',true);tex('\\S',P(1.6,0)[0]-24,P(1.6,0)[1]-30,30);tex('\\Z',P(0,1.5)[0]+14,P(0,1.5)[1]+6,30);
  painel(1240,170,620,560,{fill:'rgba(19,16,48,.92)'});
  leg('ÁREA DO CHÃO',1270,240,GEO,'left',30);tex('\\Js\\,\\DS\\,\\DT',1270,310,50);
  leg('× ALTURA',1270,420,GEO,'left',30);tex('\\DZ',1270,490,50);leg('A ALTURA NÃO ESTICA',1270,600,TH,'left',30);
  const d=tex('dV=\\Js\\,\\dS\\,\\dT\\,\\dZ',960,870,58,'c');const r=d.getBoundingClientRect();moldura(r.left-28,r.top-16,r.width+56,r.height+32,MEN);}

 // 08 · B2-3 · o determinante
 if(K==='b23'){fundoV();vista(960,540,120);papelTela(.5);await logo();canto('O DETERMINANTE');
  mixl([['t','1ª COLUNA: EM',GEO],['m','\\S'],['t','· 2ª: EM',GEO],['m','\\T'],['t','· 3ª: EM',GEO],['m','\\Z']],60,185,30);
  const m=tex('\\dfrac{\\partial(\\X,\\Y,\\Z)}{\\partial(\\S,\\T,\\Z)}=\\left|\\begin{matrix}\\cos\\T & -\\S\\sen\\T & 0\\\\ \\sen\\T & \\S\\cos\\T & 0\\\\ 0 & 0 & 1\\end{matrix}\\right|',60,360,54);
  const cols=[...m.querySelectorAll('.col-align-c')].map(c=>c.getBoundingClientRect());
  const rws=[...m.querySelectorAll('.col-align-c')[0].querySelectorAll('.vlist > span')].map(e=>e.querySelector('.mord')||e).map(e=>e.getBoundingClientRect()).filter(r=>r.height>0);console.log(JSON.stringify(rws.map(r=>[r.top,r.bottom])));
  const X0=cols[0].left-14,X1=cols[1].right+14,Y0=rws[0].top-8,Y1=rws[1].bottom+8;retTrac(X0,Y0,X1-X0,Y1-Y0,LI);
  const yb=(rws[2].top+rws[2].bottom)/2,xr=cols[2].right+40;setaPx([xr+150,yb],[xr+10,yb],MEN,4,16);txt('LINHA DE BAIXO:  +   −   +',xr+170,yb+11,{size:30,f:'SGM',cor:MEN});
  tex('=\\Ge{0}\\cdot M_{31}-\\Ge{0}\\cdot M_{32}+1\\cdot M_{33}',60,610,48);
  leg('O MENOR DO 1: TAMPA A LINHA 3 E A COLUNA 3',60,720,LI,'left',30);
  tex('M_{33}=\\left|\\begin{matrix}\\cos\\T & -\\S\\sen\\T\\\\ \\sen\\T & \\S\\cos\\T\\end{matrix}\\right|',60,860,48);
  tex('M_{33}=\\cos\\T\\cdot\\S\\cos\\T-(-\\S\\sen\\T)\\cdot\\sen\\T',1010,560,46);
  tex('=\\S\\cos^2\\T+\\S\\sen^2\\T',1060,680,48);
  const u=tex('=\\S\\,\\underbrace{(\\cos^2\\T+\\sen^2\\T)}_{=1}',1060,800,48);
  const f=tex('=\\Js',u.getBoundingClientRect().right+36,800,54);const r=f.getBoundingClientRect();moldura(r.left-16,r.top-10,r.width+32,r.height+20,MEN);
  chip('\\S\\ge 0\\ \\Rightarrow\\ |J|=\\Js',1060,950,40,MEN);}

 // 09 · B2-4 · o teste: o cilindro
 if(K==='b24'){fundoV();await logo();canto('O TESTE: O CILINDRO');const o={dx:-110,dy:40,esc:.95};await cena3d('cilindroRot',o);
  rotulo3('cilindroRot','R','R',{...o,size:38,oy:-30,al:'c'});rotulo3('cilindroRot','h','h',{...o,size:38,ox:-34,al:'c'});rotulo3('cilindroRot','ez','\\Z',{...o,size:36,ox:20});
  let q=Q3('cilindroRot','rotulo',o);placaTxt('O RÓTULO',q[0]+120,q[1]+230,AL,26);
  tex('V=\\int_0^{2\\pi}\\!\\!\\int_0^R\\!\\!\\int_0^h \\Js\\,\\dZ\\,\\dS\\,\\dT',COL,190,50);
  leg('LIMITES FIXOS, PRODUTO ⇒ SEPARA',COL,285,GEO,'left',30);
  tex('=\\big[\\Z\\big]_0^h\\cdot\\Big[\\dfrac{\\S^2}{2}\\Big]_0^R\\cdot\\big[\\T\\big]_0^{2\\pi}',COL,375,46);
  tex('=(h-0)\\cdot\\Big(\\dfrac{R^2}{2}-0\\Big)\\cdot(2\\pi-0)',COL,490,44);
  tex('=\\pi R^2h',COL,600,54);check(COL+250,600);leg('BASE × ALTURA',COL+300,612,MEN,'left',30);
  painel(COL,690,860,300,{fill:'rgba(19,16,48,.92)'});txt('SEM O s:',COL+30,750,{size:32,cor:AL});
  tex('\\int\\!\\!\\int\\!\\!\\int 1\\,\\dZ\\,\\dS\\,\\dT=h\\cdot R\\cdot 2\\pi=2\\pi Rh',COL+30,830,42);leg('m²: A ÁREA DO RÓTULO, NÃO O VOLUME',COL+30,935,AL,'left',30);}

 // 10 · B3-1 · o teorema
 if(K==='b31'){fundoV();vista(960,540,120);papelTela(.5);await logo();canto('O TEOREMA');
  const oc={dx:-20,dy:40,esc:.5},ol={dx:560,dy:60,esc:.42};
  painel(40,150,1180,430,{fill:'#18143A',a:0});await cena3d('caixa',oc);await cena3d('latagrade',ol);
  setaPx([470,330],[640,330],GEO,4,18);tex('T',555,292,40,'c');
  leg('O EIXO E A COSTURA:',1240,300,AL,'left',30);leg('VOLUME ZERO',1240,345,AL,'left',30);
  tex('\\T\\in[0,\\pi]\\ +\\ \\T\\in[\\pi,2\\pi]',1240,440,40);
  painel2d(60,600,1800,432);
  tex('\\iiint_B f(\\X,\\Y,\\Z)\\,\\dX\\,\\dY\\,\\dZ=\\iiint_{B_{uvw}} f\\big(T(u,v,w)\\big)\\Big|\\dfrac{\\partial(\\X,\\Y,\\Z)}{\\partial(u,v,w)}\\Big|\\,du\\,dv\\,dw',100,680,40);
  leg('NO INTERIOR: T DE CLASSE C¹, INJETORA, JACOBIANO ≠ 0',100,775,GEO,'left',28);
  mixl([['t','NA LATA:',GEO],['m','\\S=0'],['t','→ JACOBIANO 0 ·',GEO],['m','\\T=0,\\ 2\\pi'],['t','→ NÃO INJETORA',GEO]],100,835,30);
  tex('\\iiint_B f(\\X,\\Y,\\Z)\\,\\dX\\,\\dY\\,\\dZ=\\iiint_{B_{\\S\\T\\Z}} f(\\S\\cos\\T,\\ \\S\\sen\\T,\\ \\Z)\\,\\Js\\,\\dS\\,\\dT\\,\\dZ',100,945,44);}

 // 11 · B4-1 · o cilindro fora do eixo: montar (etapa 2)
 if(K==='b41'){fundoV();await logo();canto('O CILINDRO FORA DO EIXO');const o={dx:-40,dy:60,esc:1};await cena3d('deslocadoSonda',o);
  for(const [n,s] of [['ex','\\X'],['ey','\\Y'],['ez','\\Z']])rotulo3('deslocadoSonda',n,s,{...o,size:36,al:'c',ox:n==='ez'?30:0,oy:n==='ez'?40:0});
  let q=Q3('deslocadoSonda','eixoNovo',o);placaTxt('EIXO NOVO',q[0]+16,q[1]+40,GEO,26);
  q=Q3('deslocadoSonda','sai',o);placaTxt('SAI NO TELHADO',q[0]+20,q[1]-20,CORAL,26);q=Q3('deslocadoSonda','entra',o);placaTxt('ENTRA NO CHÃO',q[0]+20,q[1]+30,AZC,26);
  chip('(\\X-1)^2+\\Y^2\\le 1,\\quad \\X=1+\\S\\cos\\T,\\ \\ \\Y=\\S\\sen\\T',COL,180,30);
  leg('O 1 NÃO DEPENDE DE NADA ⇒ JACOBIANO s',COL,255,MEN,'left',28);
  selo('①',COL,350,GEO,30);tex('0\\le\\T\\le\\pi\\ \\ (\\Y\\ge 0),\\qquad 0\\le\\S\\le 1',COL+80,340,44);
  selo('②',COL,460,GEO,30);tex('0\\le\\Z\\le 1+\\S\\cos\\T+\\S\\sen\\T',COL+80,450,46);
  selo('③',COL,600,GEO,30);tex('V=\\int_0^{\\pi}\\!\\!\\int_0^1\\!\\!\\int_0^{1+\\S\\cos\\T+\\S\\sen\\T}\\Js\\,\\dZ\\,\\dS\\,\\dT',COL+80,590,46);
  painel2d(COL,712,560,320);txt('DE CIMA',COL+24,754,{size:26,f:'SGM',cor:GEO});vista(COL+60,990,120);
  seta([0,0],[3.6,0],E1,3,14);seta([0,0],[0,1.9],E2,3,14);preenche(arco2(a=>[1+Math.cos(a),Math.sin(a)],0,PI),mix('#16123A',CI,.30));
  linha(arco2(a=>[1+Math.cos(a),Math.sin(a)],0,PI),CI,3);
  const A=PI*.3;linha([[1,0],[1+Math.cos(A),Math.sin(A)]],SOMB,5);arcoPx([1,0],40,0,A,TH,4);ponto([1,0],BR,7);ponto([1+Math.cos(A),Math.sin(A)],SOMB,7);
  tex('\\S',P(1+.55*Math.cos(A),.55*Math.sin(A))[0]-6,P(1+.55*Math.cos(A),.55*Math.sin(A))[1]-26,30,'c');tex('\\T',P(1.42,.12)[0]+8,P(1.42,.12)[1]-6,28,'l');
  tex('(1,0)',P(1,0)[0],P(1,0)[1]+26,26,'c');tex('2',P(2,0)[0],P(2,0)[1]+26,26,'c');tex('\\X',P(3.6,0)[0]-14,P(3.6,0)[1]-24,28);tex('\\Y',P(0,1.9)[0]+14,P(0,1.9)[1]+4,28);}

 // 12 · B4-2 · a conta (tela 2: a de téta)
 if(K==='b42'){fundoV();vista(960,540,120);papelTela(.5);await logo();canto('O CILINDRO FORA DO EIXO');
  painel2d(60,160,440,460);txt('DE CIMA',84,202,{size:26,f:'SGM',cor:GEO});vista(100,570,170);
  seta([0,0],[2.25,0],E1,3,14);seta([0,0],[0,2.0],E2,3,14);preenche(arco2(a=>[1+Math.cos(a),Math.sin(a)],0,PI),mix('#16123A',CI,.30));linha(arco2(a=>[1+Math.cos(a),Math.sin(a)],0,PI),CI,3);ponto([1,0],BR,7);
  tex('\\X',P(2.25,0)[0]-10,P(2.25,0)[1]-26,28);tex('\\Y',P(0,2.0)[0]+14,P(0,2.0)[1]+4,28);tex('(1,0)',P(1,0)[0],P(1,0)[1]+28,24,'c');
  chip('\\int_0^1(\\ldots)\\,\\dS=\\dfrac12+\\dfrac13\\cos\\T+\\dfrac13\\sen\\T',540,200,30);
  tex('\\int_0^{\\pi}\\!\\Big(\\dfrac12+\\dfrac13\\cos\\T+\\dfrac13\\sen\\T\\Big)\\dT=\\Big[\\dfrac{\\T}{2}+\\dfrac13\\sen\\T\\Al{-\\dfrac13\\cos\\T}\\Big]_0^{\\pi}',560,330,44);
  chip('\\sen\\pi=0',560,450,32);chip('\\cos\\pi=-1',800,450,32);chip('\\cos 0=1',1080,450,32);
  tex('=\\Big(\\dfrac{\\pi}{2}+0+\\dfrac13\\Big)-\\Big(0+0-\\dfrac13\\Big)',560,570,46);
  const f=tex('=\\dfrac{\\pi}{2}+\\dfrac23\\approx 2{,}24',560,700,54);const r=f.getBoundingClientRect();moldura(r.left-16,r.top-10,r.width+32,r.height+20,MEN);check(r.right+50,700);
  leg('LEITURA:',560,820,GEO,'left',28);chip('1\\ \\to\\ \\dfrac{\\pi}{2}',700,820,32);chip('\\cos\\T\\ \\to\\ 0',930,820,32);chip('\\sen\\T\\ \\to\\ \\dfrac23',1180,820,32);
  leg('DESAFIO: POLO NA ORIGEM (s ≤ 2 cos θ) TEM DE DAR O MESMO',560,950,MEN,'left',28);}

 // 13 · B5-2 · a integral em s
 if(K==='b52'){fundoV();await logo();canto('A INTEGRAL EM s');const o={dx:-60,dy:80,esc:.8};await cena3d('lata',o);
  chip('M=\\int_0^{2\\pi}\\!\\!\\int_0^1\\!\\!\\int_0^1 \\Ci{\\sqrt{\\S^2+\\Z^2}}\\,\\Js\\,\\dS\\,\\dZ\\,\\dT',880,180,30);
  mixl([['m','\\uu=\\S^2+\\Z^2'],['t','(z PARADO)',GEO]],880,300,46);
  tex('\\du=2\\S\\,\\dS\\ \\Rightarrow\\ \\Js\\,\\dS=\\dfrac{\\du}{2}',880,400,46);
  tex('\\S=0\\to\\uu=\\Z^2;\\qquad \\S=1\\to\\uu=1+\\Z^2',880,500,42);
  tex('\\int_0^1\\Ci{\\sqrt{\\S^2+\\Z^2}}\\,\\Js\\,\\dS=\\dfrac12\\int_{\\Z^2}^{1+\\Z^2}\\uu^{1/2}\\,\\du=\\dfrac12\\cdot\\dfrac23\\Big[\\uu^{3/2}\\Big]_{\\Z^2}^{1+\\Z^2}',880,640,38);
  const f=tex('=\\dfrac13\\Big[(1+\\Z^2)^{3/2}-\\Z^3\\Big]',880,790,50);const r=f.getBoundingClientRect();chip('\\Z\\ge 0:\\ (\\Z^2)^{3/2}=\\Z^3',r.right+30,790,30);}

 // 14 · B5-3 · a integral em z: o triângulo
 if(K==='b53'){fundoV();vista(960,540,120);papelTela(.5);await logo();canto('A INTEGRAL EM z');
  painel2d(60,170,560,520);txt('O TRIÂNGULO',84,212,{size:26,f:'SGM',cor:GEO});vista(120,620,260);
  const z0=1.15;preenche([[0,0],[1.4,0],[1.4,z0]],mix('#16123A',GEO,.18));linha([[0,0],[1.4,0]],GEO,5);linha([[1.4,0],[1.4,z0]],EZ,5);linha([[0,0],[1.4,z0]],BR,5);
  linha([[1.28,0],[1.28,.12],[1.4,.12]],GEO,2);arcoPx([0,0],70,0,Math.atan2(z0,1.4),UU,4);
  tex('1',P(.7,0)[0],P(.7,0)[1]+30,34,'c');tex('\\Z=\\tg\\,\\Tt',P(1.4,z0/2)[0]+16,P(1.4,z0/2)[1],30,'l');tex('\\sqrt{1+\\Z^2}=\\sec\\Tt',P(.55,.62)[0]-30,P(.55,.62)[1]-70,30,'c',true);tex('\\Tt',P(.38,.13)[0],P(.38,.13)[1],32,'c');
  chip('\\dfrac13\\Big[(1+\\Z^2)^{3/2}-\\Z^3\\Big]',680,190,30);
  tex('\\int_0^1(\\ldots)\\,\\dZ=\\dfrac13\\int_0^1(1+\\Z^2)^{3/2}\\dZ-\\dfrac13\\Big[\\dfrac{\\Z^4}{4}\\Big]_0^1=\\dfrac13\\,I-\\dfrac1{12}',680,310,36);
  tex('I=\\int_0^1(1+\\Z^2)^{3/2}\\,\\dZ',680,430,46);
  tex('\\Z=\\tg\\,\\Tt,\\qquad \\dZ=\\sec^2\\Tt\\,\\dTt',680,540,46);
  tex('\\Z=0\\to\\Tt=0;\\qquad \\Z=1\\to\\Tt=\\dfrac{\\pi}{4}',680,650,44);
  tex('1+\\tg^2\\Tt=\\sec^2\\Tt\\ \\Rightarrow\\ (1+\\Z^2)^{3/2}=\\sec^3\\Tt',680,770,44);
  const f=tex('I=\\int_0^{\\pi/4}\\sec^3\\Tt\\cdot\\sec^2\\Tt\\,\\dTt=\\int_0^{\\pi/4}\\sec^5\\Tt\\,\\dTt',680,900,46);}

 // 15 · B5-4 · a secante à quinta (etapa 2)
 if(K==='b54'){fundoV();vista(960,540,120);papelTela(.5);await logo();canto('A SECANTE À QUINTA');
  painel2d(60,170,440,400);txt('t = π/4',84,212,{size:26,f:'SGM',cor:GEO});vista(130,500,230);
  preenche([[0,0],[1.2,0],[1.2,1.2]],mix('#16123A',GEO,.18));linha([[0,0],[1.2,0]],GEO,5);linha([[1.2,0],[1.2,1.2]],EZ,5);linha([[0,0],[1.2,1.2]],BR,5);arcoPx([0,0],60,0,PI/4,UU,4);
  tex('1',P(.6,0)[0],P(.6,0)[1]+28,32,'c');tex('1',P(1.2,.6)[0]+22,P(1.2,.6)[1],32,'l');tex('\\sqrt2',P(.5,.62)[0]-30,P(.5,.62)[1]-20,32,'c');
  chip('\\Tt=\\dfrac{\\pi}{4}:\\ \\sec=\\sqrt2,\\ \\tg=1',60,660,30,MEN);chip('\\Tt=0:\\ \\sec=1,\\ \\tg=0',60,770,30,MEN);
  painel(560,150,1300,150,{fill:'rgba(19,16,48,.92)'});leg('RECORRÊNCIA (POR PARTES)',590,198,GEO,'left',24);
  tex('\\int\\sec^n\\Tt\\,\\dTt=\\dfrac{\\sec^{n-2}\\Tt\\,\\tg\\,\\Tt}{n-1}+\\dfrac{n-2}{n-1}\\int\\sec^{n-2}\\Tt\\,\\dTt',1000,232,36);
  tex('\\Big[\\dfrac14\\sec^3\\Tt\\,\\tg\\,\\Tt\\Big]_0^{\\pi/4}=\\dfrac14(\\sqrt2)^3\\cdot 1-0=\\dfrac{2\\sqrt2}{4}=\\dfrac{\\sqrt2}{2}',560,370,40);
  tex('\\int_0^{\\pi/4}\\!\\sec^3\\Tt\\,\\dTt=\\Big(\\dfrac{\\sqrt2}{2}+\\dfrac12\\ln(\\sqrt2+1)\\Big)-\\Big(0+\\dfrac12\\ln 1\\Big)',560,500,40);
  tex('I=\\dfrac{\\sqrt2}{2}+\\dfrac34\\Big(\\dfrac{\\sqrt2}{2}+\\dfrac12\\ln(1+\\sqrt2)\\Big)',560,640,44);
  tex('=\\dfrac{4\\sqrt2}{8}+\\dfrac{3\\sqrt2}{8}+\\dfrac38\\ln(1+\\sqrt2)',600,770,44);
  const f=tex('=\\dfrac{7\\sqrt2}{8}+\\dfrac38\\ln(1+\\sqrt2)\\approx 1{,}568',600,900,50);const r=f.getBoundingClientRect();moldura(r.left-16,r.top-10,r.width+32,r.height+20,MEN);}

 // 16 · B5-5 · a massa
 if(K==='b55'){fundoV();await logo();canto('A MASSA DA LATA');const o={dx:-60,dy:80,esc:.8};await cena3d('lata',o);
  let q=Q3('lata','quina',o);placaTxt('√2 DA ORIGEM',q[0]+30,q[1]-50,CI,26);
  chip('I=\\dfrac{7\\sqrt2}{8}+\\dfrac38\\ln(1+\\sqrt2)',880,180,30);
  tex('M=2\\pi\\Big[\\dfrac13\\,I-\\dfrac1{12}\\Big]',880,310,48);
  tex('=2\\pi\\Big[\\dfrac{7\\sqrt2}{24}+\\dfrac18\\ln(1+\\sqrt2)-\\dfrac1{12}\\Big]',880,440,46);
  tex('=\\dfrac{7\\sqrt2\\,\\pi}{12}+\\dfrac{\\pi}{4}\\ln(1+\\sqrt2)-\\dfrac{\\pi}{6}',880,570,46);
  const f=tex('=\\dfrac{\\pi}{12}\\big(7\\sqrt2-2+3\\ln(1+\\sqrt2)\\big)\\approx 2{,}76',880,710,50);const r=f.getBoundingClientRect();moldura(r.left-16,r.top-10,r.width+32,r.height+20,MEN);check(r.right+46,710);
  leg('CONFERE: CARTESIANAS NO COMPUTADOR ≈ 2,7603',880,840,MEN,'left',30);
  leg('ETAPA 2 (RENOVA): MÉDIA = M/V = 2,76/π ≈ 0,88 · ρ VAI DE 0 A √2',880,930,GEO,'left',24);}

 // 17 · S2 · girar a lata e o próximo vídeo
 if(K==='s2'){fundoV();await logo();canto('GIRAR A LATA');const o={dx:-110,dy:40,esc:.95};await cena3d('giro',o);
  let q=Q3('giro','fio',o);tex('\\S',q[0],q[1]-34,36,'c',true);q=Q3('giro','cel',o);tex('dm',q[0]+50,q[1],34,'l',true);rotulo3('giro','ez','\\Z',{...o,size:36,ox:20});
  mixl([['t','CADA PEDAÇO CUSTA',GEO],['m','\\S^2\\cdot dm']],COL,200,44);
  tex('I=\\iiint \\S^2\\,\\de\\,dV',COL,310,50);
  mixl([['t','EM CILÍNDRICAS:',GEO],['m','\\S^2\\cdot\\Js=\\S^3']],COL,420,44);
  painel(1060,540,760,330,{fill:'rgba(19,16,48,.92)'});txt('NO PRÓXIMO VÍDEO',1440,620,{size:30,f:'SGM',cor:GEO,al:'center'});
  txt('CENTRO DE MASSA',1440,705,{size:46,al:'center'});txt('E MOMENTO DE INÉRCIA',1440,775,{size:46,cor:SOMB,al:'center'});leg('NA INTEGRAL TRIPLA',1440,840,GEO,'center',28);}

 document.title='ok';}
function arco2(f,a0,a1,n=80){return Array.from({length:n+1},(_,k)=>f(a0+(a1-a0)*k/n));}
main();
</script></body></html>
