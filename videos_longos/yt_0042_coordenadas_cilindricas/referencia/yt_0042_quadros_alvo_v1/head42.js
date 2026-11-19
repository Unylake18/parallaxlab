<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="katex/katex.min.css">
<script src="katex/katex.min.js"></script>
<script src="r3d_pts.js"></script>
<style>
@font-face{font-family:SG;src:url(SpaceGrotesk-Bold.ttf)}
@font-face{font-family:SGM;src:url(SpaceGrotesk-Medium.ttf)}
html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:#131030}
canvas{position:absolute;left:0;top:0}
.f{position:absolute;color:#F5F7FF;white-space:nowrap;line-height:1}
.f .katex{font-size:1em}
.pl{position:absolute;background:rgba(19,16,48,.88);border-radius:6px}
</style></head><body><canvas id="o" width="1920" height="1080"></canvas>
<script>
// Quadros-alvo v1 do 3.5-T3 (Cálculo III · coordenadas cilíndricas na integral tripla) · yt_0042 provisório · ?k=<chave>
// 3D = r3d_<k>.png gerados por c3d42.html (r3d42.js); pontos de tela em r3d_pts.js
// Sistema da série: fundo violeta #18143A → #0F0C26; grade #2B2558 na TELA INTEIRA (papelTela) em todo quadro 2D; o 3D (r3d_<k>.png de c3d41.html) fica sobre o liso;
// palavra em Space Grotesk, matemática em KaTeX; cor por grandeza; operadores brancos; \dfrac; legendas ≥ 26 px.
const K=new URLSearchParams(location.search).get('k'), x=document.getElementById('o').getContext('2d'), PI=Math.PI;
const CI='#35D9FF',AZC='#7FB2FF',CORAL='#FF7A8A',E1='#FFC24D',E2='#EA63FF',EZ='#5AA2FF',GEO='#B8C4DA',BR='#F5F7FF',AL='#FF5D5D',MEN='#8CFFD2',BG='#131030',
 RO='#FF9440',TH='#2EE6A6',FI='#B48CFF',SOMB='#FFC08A',LI='#C6F26B',UU='#E08A3C';
const M={'\\X':'\\textcolor{#FFC24D}{x}','\\Y':'\\textcolor{#EA63FF}{y}','\\Z':'\\textcolor{#5AA2FF}{z}','\\dX':'\\textcolor{#FFC24D}{dx}','\\dY':'\\textcolor{#EA63FF}{dy}','\\dZ':'\\textcolor{#5AA2FF}{dz}',
 '\\R':'\\textcolor{#FF9440}{r}','\\F':'\\textcolor{#B48CFF}{\\varphi}','\\T':'\\textcolor{#2EE6A6}{\\theta}','\\Rs':'\\textcolor{#FFC08A}{s}',
 '\\dR':'\\textcolor{#FF9440}{dr}','\\dF':'\\textcolor{#B48CFF}{d\\varphi}','\\dT':'\\textcolor{#2EE6A6}{d\\theta}',
 '\\DR':'\\textcolor{#FF9440}{\\Delta r}','\\DF':'\\textcolor{#B48CFF}{\\Delta\\varphi}','\\DT':'\\textcolor{#2EE6A6}{\\Delta\\theta}',
 '\\sen':'\\operatorname{sen}','\\J':'\\textcolor{#C6F26B}{r^2\\operatorname{sen}\\varphi}','\\Li':'\\textcolor{#C6F26B}','\\Ci':'\\textcolor{#35D9FF}','\\de':'\\textcolor{#35D9FF}{\\rho}',
 '\\Me':'\\textcolor{#8CFFD2}','\\Al':'\\textcolor{#FF5D5D}','\\Co':'\\textcolor{#FF7A8A}','\\Az':'\\textcolor{#7FB2FF}','\\Ro':'\\textcolor{#FF9440}','\\Fi':'\\textcolor{#B48CFF}','\\Th':'\\textcolor{#2EE6A6}',
 '\\Uu':'\\textcolor{#E08A3C}','\\uu':'\\textcolor{#E08A3C}{u}','\\du':'\\textcolor{#E08A3C}{du}','\\Ge':'\\textcolor{#B8C4DA}','\\dV':'dV','\\S':'\\textcolor{#FFC08A}{s}','\\dS':'\\textcolor{#FFC08A}{ds}','\\DS':'\\textcolor{#FFC08A}{\\Delta s}','\\DZ':'\\textcolor{#5AA2FF}{\\Delta z}','\\Js':'\\textcolor{#C6F26B}{s}','\\Tt':'\\textcolor{#E08A3C}{t}','\\dTt':'\\textcolor{#E08A3C}{dt}','\\tg':'\\operatorname{tg}'};
let O=[960,540],U=100; const P=(a,b)=>[O[0]+a*U,O[1]-b*U]; const vista=(cx,cy,u)=>{O=[cx,cy];U=u;};
const img=s=>new Promise(r=>{const i=new Image();i.onload=()=>r(i);i.onerror=()=>r(null);i.src=s;});
function mix(a,b,t){const h=s=>[1,3,5].map(i=>parseInt(s.slice(i,i+2),16));const A=h(a),B=h(b);return 'rgb('+A.map((v,i)=>Math.round(v+(B[i]-v)*t)).join(',')+')';}
function tex(s,X,Y,size=40,al='l',placa=false){const d=document.createElement('div');d.className='f';d.style.fontSize=size+'px';
 katex.render(s,d,{macros:M,throwOnError:false});document.body.appendChild(d);const w=d.offsetWidth,h=d.offsetHeight;
 const L=(al==='c'?X-w/2:al==='r'?X-w:X),T=(Y-h/2);d.style.left=L+'px';d.style.top=T+'px';
 if(placa){const p=document.createElement('div');p.className='pl';p.style.left=(L-6)+'px';p.style.top=(T-4)+'px';p.style.width=(w+12)+'px';p.style.height=(h+8)+'px';document.body.insertBefore(p,d);}return d;}
function txt(s,X,Y,{size=30,f='SG',cor=BR,al='left',alpha=1,placa=false}={}){x.font=`${size}px ${f}`;if(placa){const w=x.measureText(s).width,L=al==='center'?X-w/2:al==='right'?X-w:X;x.fillStyle='rgba(19,16,48,.88)';x.beginPath();x.roundRect(L-8,Y-size*.82,w+16,size*1.05,6);x.fill();}
 x.globalAlpha=alpha;x.fillStyle=cor;x.textAlign=al;x.fillText(s,X,Y);x.globalAlpha=1;x.textAlign='left';}
function leg(s,X,Y,cor=GEO,al='left',size=28,placa=false){txt(s,X,Y,{size,f:'SGM',cor,al,placa});}
function caminho(pts){x.beginPath();pts.forEach((p,i)=>{const q=P(...p);i?x.lineTo(...q):x.moveTo(...q)});}
function linha(pts,cor,w,{dash=null,alpha=1}={}){x.lineCap='round';x.lineJoin='round';x.setLineDash(dash||[]);caminho(pts);x.globalAlpha=alpha;x.strokeStyle=cor;x.lineWidth=w;x.stroke();x.globalAlpha=1;x.setLineDash([]);}
function preenche(pts,cor){caminho(pts);x.closePath();x.fillStyle=cor;x.fill();}
function seta(a,b,cor,w=4,head=18){const A=P(...a),B=P(...b);setaPx(A,B,cor,w,head);}
function setaPx(A,B,cor,w=4,head=18){const dx=B[0]-A[0],dy=B[1]-A[1],L=Math.hypot(dx,dy);if(L<3)return;const ux=dx/L,uy=dy/L;
 x.strokeStyle=cor;x.lineWidth=w;x.lineCap='round';x.beginPath();x.moveTo(...A);x.lineTo(B[0]-ux*head*.8,B[1]-uy*head*.8);x.stroke();
 x.fillStyle=cor;x.beginPath();x.moveTo(...B);x.lineTo(B[0]-ux*head-uy*head*.5,B[1]-uy*head+ux*head*.5);x.lineTo(B[0]-ux*head+uy*head*.5,B[1]-uy*head-ux*head*.5);x.closePath();x.fill();}
function ponto(p,cor,r=9){const q=P(...p);x.beginPath();x.arc(...q,r,0,7);x.fillStyle=cor;x.fill();}
function pontoPx(q,cor,r=9){x.beginPath();x.arc(...q,r,0,7);x.fillStyle=cor;x.fill();}
function canto(s){txt('CÁLCULO III · INTEGRAL TRIPLA',36,73,{size:22,f:'SGM',cor:'#C8D6F0',alpha:.6});if(s)txt(s,36,118,{size:36});}
async function logo(){const lg=await img('logo_crop.png');if(lg)x.drawImage(lg,1650,24);}
function painel(X0,Y0,w,h,{fill=null,a=.35}={}){if(fill){x.fillStyle=fill;x.beginPath();x.roundRect(X0,Y0,w,h,14);x.fill();}x.strokeStyle=`rgba(184,196,218,${a})`;x.lineWidth=2;x.beginPath();x.roundRect(X0,Y0,w,h,14);x.stroke();}
function check(X,Y,cor=MEN,s=1){x.strokeStyle=cor;x.lineWidth=6*s;x.lineCap='round';x.beginPath();x.moveTo(X-14*s,Y);x.lineTo(X-3*s,Y+11*s);x.lineTo(X+16*s,Y-13*s);x.stroke();}
function cruz(X,Y,cor=AL,s=1){x.strokeStyle=cor;x.lineWidth=6*s;x.lineCap='round';x.beginPath();x.moveTo(X-12*s,Y-12*s);x.lineTo(X+12*s,Y+12*s);x.moveTo(X+12*s,Y-12*s);x.lineTo(X-12*s,Y+12*s);x.stroke();}
function fundoV(){const g=x.createLinearGradient(0,0,0,1080);g.addColorStop(0,'#18143A');g.addColorStop(1,'#0F0C26');x.fillStyle=g;x.fillRect(0,0,1920,1080);}
// grade na TELA INTEIRA, nascendo da origem O do palco (passo p na unidade U); sem palco: passo 0,5 com U = 120 → 60 px
function papelTela(p=.25){x.strokeStyle='#2B2558';x.lineWidth=1.2;const s=p*U;let X0=O[0]%s,Y0=O[1]%s;
 for(let X=X0;X<=1920;X+=s){x.beginPath();x.moveTo(Math.round(X)+.5,0);x.lineTo(Math.round(X)+.5,1080);x.stroke();}
 for(let Y=Y0;Y<=1080;Y+=s){x.beginPath();x.moveTo(0,Math.round(Y)+.5);x.lineTo(1920,Math.round(Y)+.5);x.stroke();}}
const P3=(k,n)=>(window.R3D&&R3D[k]&&R3D[k][n])||[0,0];
async function cena3d(k,{dx=0,dy=0,esc=1}={}){const im=await img('r3d_'+k+'.png');if(!im)return;x.drawImage(im,dx,dy,1920*esc,1080*esc);}
const Q3=(k,n,{dx=0,dy=0,esc=1}={})=>{const p=P3(k,n);return [dx+p[0]*esc,dy+p[1]*esc];};
function mixl(parts,X,Y,size=36,cor=BR){let cx=X;for(const [t,s,c] of parts){if(t==='m'){const d=tex(s,cx,Y,size,'l');cx+=d.getBoundingClientRect().width+14;}
 else{x.font=`${Math.round(size*.78)}px SG`;txt(s,cx,Y+size*.27,{size:Math.round(size*.78),cor:c||cor});cx+=x.measureText(s).width+14;}}return cx;}
function chip(s,X,Y,size=30,cor=GEO){const d=tex(s,X+16,Y,size,'l');const r=d.getBoundingClientRect();x.strokeStyle=cor;x.globalAlpha=.75;x.lineWidth=2;x.beginPath();x.roundRect(X,r.top-10,r.width+32,r.height+20,10);x.stroke();x.globalAlpha=1;return r.right+16;}
function moldura(X,Y,w,h,cor=MEN){x.strokeStyle=cor;x.lineWidth=3;x.beginPath();x.roundRect(X,Y,w,h,12);x.stroke();}
function selo(s,X,Y,cor=GEO,size=26){x.font=`${size}px SGM`;const w=x.measureText(s).width;x.strokeStyle=cor;x.lineWidth=2;x.beginPath();x.roundRect(X,Y-size-6,w+28,size+22,8);x.stroke();txt(s,X+14,Y+2,{size,f:'SGM',cor});}
function sublinha(X0,X1,Y,cor=BR){x.strokeStyle=cor;x.lineWidth=2.5;x.beginPath();x.moveTo(X0,Y);x.lineTo(X1,Y);x.stroke();}
function guia(A,B,cor=GEO){x.strokeStyle=cor;x.globalAlpha=.7;x.lineWidth=2;x.setLineDash([6,6]);x.beginPath();x.moveTo(...A);x.lineTo(...B);x.stroke();x.setLineDash([]);x.globalAlpha=1;}
function rotulo3(k,n,s,{dx=0,dy=0,esc=1,ox=0,oy=0,size=34,al='l'}={}){const q=Q3(k,n,{dx,dy,esc});return tex(s,q[0]+ox,q[1]+oy,size,al,true);}
// fundo liso do 3D + grade que entra no pouso: nos alvos 3D a grade fica fora (liso), como na série
async function main(){await document.fonts.load('30px SG');await document.fonts.load('30px SGM');
 for(const f of ['KaTeX_Main','KaTeX_Math','KaTeX_Size1','KaTeX_Size2','KaTeX_Size3','KaTeX_Size4','KaTeX_AMS']){try{await document.fonts.load(`40px ${f}`);await document.fonts.load(`italic 40px ${f}`);}catch(e){}}
 {const w=tex('\\iiint\\int_0^1\\dfrac{a}{b}\\sqrt{x}\\rho\\varphi\\theta\\Big[\\Big]\\left|\\begin{matrix}a\\\\b\\end{matrix}\\right|',0,-200,40);await document.fonts.ready;await new Promise(r=>setTimeout(r,300));w.remove();}

