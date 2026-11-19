"""Direção por âncora; Manim para texto/diagrama, Three.js apenas para sólidos."""
from visual23 import *
from conteudo import CONTAS,SELOS
import fisica as fis
import kit
from MF_Tools import TransformByGlyphMap as GlyphMap

CAP={'H':'QUAL BLOCO DESCE?','A':'CAIXA DE FERRAMENTAS','D':'O DESAFIO DA RÉGUA','E1':'EXERCÍCIO 1 · O VOLANTE',
     'E2':'EXERCÍCIO 2 · A HASTE E O EIXO','E3':'EXERCÍCIO 3 · O CARRETEL','E4':'EXERCÍCIO 4 · O PÊNDULO MAIS RÁPIDO','S':'RESUMO','EN':'DESAFIO PARA OS COMENTÁRIOS'}

def bloco(a):return a.split('-')[0] if '-' in a else re.sub(r'\d','',a)

class Rotacao23(Prob2):
    TITULO='MECÂNICA · EXERCÍCIOS DE ROTAÇÃO'
    FUNDO='fundo_grad.png'

    def construct(self):
        self.setup_base()
        self.pilha=Pilha(self,x0=.7,topo=2.25,base=-3.4,buff=.32,larg=6.15)
        self.aparato=None;self.over=None;self.kind=None;self.adicionais=[];self.events=[]
        self.rows=[];self.prev=None;self.chapter=None;self.tokens=[]
        only=os.environ.get('ONLY')
        ids=[a for a in self.IDS if not only or a in only.split(',')]
        for aid in ids:
            self.an(aid)
            self.anchor(aid)
        self.fim();self.relatorio();self.gravar_reg()
        (AQUI/'renders').mkdir(exist_ok=True)
        (AQUI/'renders'/f'eventos_{self.lote}.json').write_text(json.dumps(dict(eventos=self.events,ancoras=self.log),ensure_ascii=False,indent=1),encoding='utf-8')

    def wait(self,duration=1,*a,**kw):
        # O tempo de física e o fundo avançam no mesmo relógio; sem pulsos decorativos para disfarçar PARADO.
        return Base.wait(self,duration,*a,**kw)

    def rel(self):return max(0,self.clk.get_value()-self._q0/FPS)

    def cue_time(self,aid,cue):
        k=self._k_frase(aid,cue)
        return max(0,ANC[aid]['t'][k]-.15) if k is not None else None

    def estado(self,_):
        a=self._aid or self.lastaid;t=self.rel();cam=cam_frente(K=3.15,xc=-3.85,yc=1.05,el=0)
        if self.kind=='regua':
            u=min(.28,max(0,(t-3)/4)) if a=='D3' else 0
            th=fis.queda(u,True)
            return dict(th=th,cam=cam_frente(K=4.4,xc=-6.1,yc=.9,el=10),massa_ponta=True,moedas=True,moeda_meio=False,m2x=.972,m2z=.042-.5*fis.G*u*u,m2th=0)
        e=dict(th=0,cam=cam,lock=False)
        if self.kind=='carretel':
            az=-60
            if a.startswith('E3-'):
                n=int(a.split('-')[1]);az=-60 if n<3 else -60-30*min(1,t/3) if n==3 else -90
            if a in ('H1','E3-1','E3-9'):e['lock']=t<1.5 or a!='E3-9'
            if a=='H2':e['th']=fis.carretel(max(0,(t-1)/2))['th']
            if a=='H3':e['th']=fis.carretel(fis.T_C)['th']
            if a=='E3-2':e['th']=.5*math.sin(min(1,t/6)*math.pi)
            if a=='E3-8':e['th']=fis.carretel(max(0,(t-1)/2))['th']
            if a=='E3-9':e['m2']=18;e['lock']=t<2
            if a=='S2':e['th']=min(2,t*.04)
            e['cam']=cam_obl(az,5 if az>-90 else 0,[0,0,0],K=3.15,xc=-3.85,yc=1.05)
        else:
            n=int(a.split('-')[1]) if a.startswith('E1-') else 0
            if n==11:e['th']=fis.volante(max(0,t-2))['th']
            if 12<=n<=14:e['th']=fis.volante(1.5)['th']
            if n==15:e.update(th=fis.volante(1.5)['th'],cord=False,brake=True)
            if n==16:
                st=fis.freio(max(0,t-2));e.update(th=fis.volante(1.5)['th']+st['th'],cord=False,brake=True,heat=st['calor']/fis.K_VOL)
            if 3<=n<=5:e['explode']=math.sin(math.pi*min(1,t/ANC[a]['dur']))
            if a=='A3':e.update(th=.12*t,cord=False)
            if a in ('S1','EN2'):e.update(th=0,cord=False)
        return e

    def ponto(self,xyz):return np.asarray(projeta3d(self.estado(0)['cam'],xyz),dtype=float)

    def overlay3d(self):
        a=self._aid or self.lastaid;e=self.estado(0);th=e.get('th',0);g=VGroup()
        if self.kind=='regua':
            c,s=math.cos(th),math.sin(th)
            mid=self.ponto([.5*c,0,-.5*s]);end=self.ponto([c,0,-s])
            g.add(label('M',mid+UP*.4,MAS),label('M',end+RIGHT*.38,MAS),label('L',self.ponto([.48,0,.2]),GEO))
            if a=='D2':
                for p in (mid,end):g.add(seta(p,p+DOWN*.8,FC,5),label('Mg',p+LEFT*.45+DOWN*.5,FC))
            return g
        car=self.kind=='carretel';r=.3 if car else .15
        z1=-.52-r*th;x1=.307 if car else .155;y1=.03 if car else -.1
        p1=self.ponto([x1,y1,z1]);o=self.ponto([0,0,0]);pT=self.ponto([x1,y1,0])
        if e.get('cord',True):g.add(label(r'6{,}0\ \mathrm{kg}' if car else r'10\ \mathrm{kg}',p1+RIGHT*.8,MAS))
        if car:
            p2=self.ponto([-.107,-.1,-.88+.1*th]);g.add(label(r'18\ \mathrm{kg}' if a=='E3-9' else r'10{,}0\ \mathrm{kg}',p2+LEFT*.95,MAS))
            if a.startswith('E3'):
                g.add(label('R',o+RIGHT*1.25+UP*.35,GEO),label('r',o+LEFT*.7+UP*.35,GEO))
        elif a.startswith('E1'):
            g.add(label('R_2',o+LEFT*1.65,GEO),label('r',o+RIGHT*.8+UP*.35,GEO),label('I',o+LEFT*.55+UP*1.5,MAS))
        if a in ('E1-6','E1-7','E3-3','E3-4'):
            g.add(seta(p1,p1+UP*.82,FC,5),seta(p1,p1+DOWN*.9,FC,5),label('T_1' if car else 'T',p1+RIGHT*.4+UP*.7,FC),label('m_1g' if car else 'mg',p1+RIGHT*.45+DOWN*.75,FC),seta(pT,pT+DOWN*.9,FC,5))
            if car:g.add(seta(p2,p2+UP*.8,FC,5),seta(p2,p2+DOWN*.9,FC,5),label('T_2',p2+LEFT*.42+UP*.6,FC),label('m_2g',p2+LEFT*.45+DOWN*.7,FC))
        if a=='E1-12':
            p=self.ponto([.4*math.cos(th),-.07,-.4*math.sin(th)]);u=(o-p)/np.linalg.norm(o-p);v=np.array([-u[1],u[0],0])
            g.add(Dot(p,color=ACC),seta(p,p+2.4*u,ACC,5),seta(p,p+.6*v,ACC,5),label('a_c',p+1.3*u+LEFT*.4,ACC),label('a_t',p+.7*v+UP*.3,ACC))
            g.add(txt('FORA DE ESCALA · RAZÃO 14,75',24,color=ACC).move_to(P3(-3.9,-2.9)))
        if a in ('E1-15','E1-16'):
            top=self.ponto([0,0,.4]);g.add(seta(top,top+DOWN*.7,FC,5),seta(top,top+LEFT*.85,FC,5),label('N',top+RIGHT*.4,FC),label('f_{at}',top+LEFT*.85+UP*.35,FC))
        return g

    def figure2d(self):
        a=self._aid or self.lastaid;t=self.rel();n=int(a.split('-')[1]) if '-' in a else 0
        if a.startswith('E2'):
            th=0 if n<=3 or n==8 else math.pi/4 if n in (6,7,9) else math.pi/2 if n==10 and t<12 else fis.queda(min(fis.HASTE[0][-1],max(0,t-1)/4))
            return haste(th,3 if n==9 else 2 if n>=6 else 1 if n>=4 else 0)
        l=.3
        if n>=5:
            if n==5:l=.03+.27*(.5+.5*math.cos(t*.35))
            elif n==6:l=.3 if t<5 else .3-.28*min(1,(t-5)/14)
            elif n==7:l=.3-(.3-.1/math.sqrt(2))*min(1,t/9)
            elif n==8:l=.05
            else:l=.1/math.sqrt(2) if n==9 and t<10 else .1
        g=pendulo(l,t,duplo=n<=3,x=-4.7,scale=7.4)
        if n in (2,3):
            leq=(.1**2+.3**2)/.3;theta=math.radians(5)*math.cos(2*math.pi*t/fis.periodo(.3,True))
            g.add(pendulo(leq,t,False,x=-1.8,scale=7.4,simples=True,ang=theta))
        if n==4:g=VGroup(pendulo(.3,t,True,x=-5.4,scale=6),pendulo(.3,t,False,x=-2.3,scale=6))
        if n==8:
            theta=math.radians(5)*math.cos(2*math.pi*t/fis.periodo(.05))
            g=VGroup(pendulo(.05,t,False,x=-5.4,scale=8,ang=theta),pendulo(.1,t,False,x=-2.4,scale=8,ang=theta))
        if n>=5:g.add(curva_periodo(l))
        return g

    def apparatus(self,kind):
        if kind==self.kind:return
        old=[x for x in (self.aparato,self.over) if x is not None]
        for x in old:x.clear_updaters()
        self.kind=kind
        if kind in ('carretel','volante','regua'):
            self.aparato=Fundo3D(self,kind,self.estado)
            self.over=vivo(self.overlay3d)
            self.add(self.aparato,self.over)
        elif kind in ('haste','pendulo'):
            self.aparato=vivo(self.figure2d);self.over=None;self.add(self.aparato)
        else:self.aparato=self.over=None
        if old:self.play(*[FadeOut(x) for x in old],run_time=.5)

    def clear_rows(self):
        self.pilha.limpa();self.prev=None;self.rows=[]

    def write_math(self,s,cue,rt=2.0):
        boxed=s.startswith('!');s=s.lstrip('!');period=self._aid.startswith('E4')
        m=Q(s,46,period)
        # Mantém o corpo: quebra fórmulas extensas em dois andares no mesmo passo.
        if m.width>6.05:
            cuts=[];depth=0
            for i,c in enumerate(s):
                if c=='{':depth+=1
                elif c=='}':depth-=1
                elif c in '=+-' and depth==0 and i>2:cuts.append(i)
            cut=min(cuts,key=lambda i:abs(i-len(s)*.52)) if cuts else None
            if cut and cut>2:
                ss=r'\begin{aligned}'+s[:cut]+r'{}\\ &'+s[cut:]+r'\end{aligned}'
                m=Q(ss,46,period)
        if m.width>6.1:
            self.events.append(dict(tipo='FORA DA MARGEM',ancora=self._aid,tex=s,largura=m.width))
        row=caixa_l(m,ACC if s.startswith(('a','\\alpha')) else MAS if s.startswith('I') else WHITE_ if period else FC) if boxed else m
        self.pilha.poe(row)
        if boxed:self.cx(row[0])
        # Um único MathTex; glifos ordenados pela posição final. Cópias saem dos rótulos já presentes.
        glyphs=m[0];order=sorted(range(len(glyphs)),key=lambda j:(round(-glyphs[j].get_y()/1.2),glyphs[j].get_x()))
        refs=[]
        if self.over:refs=[x for x in self.over.get_family() if isinstance(x,MathTex)]
        if self.aparato and not self.over:refs=[x for x in self.aparato.get_family() if isinstance(x,MathTex)]
        animations=[]
        for j in order:
            target=glyphs[j]
            color=target.get_color().to_hex()
            src=next((r for r in refs if color not in ('#F5F7FF','#FFFFFF') and any(g.get_color().to_hex()==color for g in r.family_members_with_points())),None)
            animations.append(TransformFromCopy(src,target,path_arc=-.25) if src is not None and j==order[0] else FadeIn(target))
        self.play(LaggedStart(*animations,lag_ratio=.22),*self._cx_leva(),run_time=max(1.0,rt))
        self.limpa_pecas(m);self.add(row);self.prev=m;self.rows.append(row);self.foco=row
        self.events.append(dict(tipo='equacao',ancora=self._aid,t=self.t,tex=s,cue=cue,corpo=46,caixa=boxed))

    def editorial(self,linhas):
        for s in linhas:
            m=txt(s,30,bold=True)
            if m.width>6:m=quebra(s,30,6)
            self.pilha.poe(m);self.play(Write(m),run_time=1.5);self.rows.append(m)

    def anchor(self,a):
        self.lastaid=a;b=bloco(a);n=int(a.split('-')[1]) if '-' in a else 0
        if b!=self.chapter:
            self.secao(CAP[b]);self.chapter=b
        self.clear_rows()
        for x in self.adicionais:
            if x in self.mobjects:self.play(FadeOut(x),run_time=.5)
        self.adicionais=[]
        kind='carretel' if b in ('H','E3') or a=='S2' else 'regua' if b=='D' else 'haste' if b=='E2' else 'pendulo' if b=='E4' else 'volante' if b=='E1' or a in ('A3','S1','EN2') else None
        self.apparatus(kind)
        if a in SELOS:self.selo(*SELOS[a])
        else:self.selos_sai()
        if a in ('A1','EN1'):
            self.apparatus(None)
            logo=self.logo(6).move_to(P3(0,.6));self.play(FadeIn(logo),run_time=.5)
            title=txt('BEM-VINDOS AO PARALLAX LAB' if a=='A1' else 'INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS',30).move_to(P3(0,-1.1))
            if title.width>14:title.scale_to_fit_width(14)
            self.play(Write(title),run_time=1.4);self.adicionais+=[logo,title]
        elif a=='A2':self.editorial(['DINÂMICA DA ROTAÇÃO','4 PROBLEMAS','O VOLANTE','A HASTE E O EIXO','O CARRETEL','O PÊNDULO MAIS RÁPIDO'])
        elif a=='H1':self.editorial(['6 QUILOS NO TAMBOR GRANDE','10 QUILOS NO PEQUENO'])
        elif a=='H2':self.editorial(['SEM MOTOR','SEM EMPURRÃO','SEM TRUQUE'])
        elif a=='H3':self.editorial(['TORQUE','MOMENTO DE INÉRCIA','VÍNCULO'])
        elif a=='E1-1':self.editorial(['ANEL · 15 KG','CUBO · 3 KG','DOIS DISCOS · 1 KG CADA','TAMBOR LEVE · 15 CM'])
        elif a=='E1-2':self.editorial(['A · MOMENTO DE INÉRCIA','B · ACELERAÇÃO E TRAÇÃO','C · UM SEGUNDO E MEIO','D · ENERGIA','E · FREIO','F · ARO'])
        elif a in ('E1-6','E3-3'):self.editorial(['PESO E TRAÇÃO NOS BLOCOS','TRAÇÃO NA BORDA','NO CENTRO: BRAÇO ZERO'])
        elif a=='E1-18':self.editorial(['SEPARA OS CORPOS','UMA EQUAÇÃO POR CORPO','O VÍNCULO AMARRA','CONFERE'])
        elif a=='E2-1':self.editorial(['EIXO FORA DO CENTRO','SOLTA DO REPOUSO','A FORÇA MUDA DURANTE A QUEDA'])
        elif a=='E2-11':self.editorial(['NEWTON NO CENTRO DE MASSA','TANGENCIAL E CENTRÍPETA'])
        elif a=='E3-1':self.editorial(['RAIO GRANDE · 30 CM','RAIO PEQUENO · 10 CM','ANTES DA CONTA: QUAL DESCE?'])
        elif a=='E3-10':self.editorial(['MASSA × RAIO: O SENTIDO','TRAÇÕES: A EQUAÇÃO','ENERGIA: A CONFERÊNCIA'])
        elif a=='E4-1':self.editorial(['DOIS DISCOS IGUAIS','HASTE LEVE','OSCILAÇÕES PEQUENAS'])
        elif a=='E4-5':self.editorial(['ONDE PÔR O EIXO?','O PERÍODO PODE SER MENOR'])
        elif a=='S2':self.editorial(['DESENHA O SISTEMA','ESCOLHE O EIXO','ESCREVE AS EQUAÇÕES','APLICA OS VÍNCULOS','CONFERE'])
        elif a=='EN2':self.editorial(['BLOCO DE 20 KG','A ACELERAÇÃO DOBRA?','ESCREVE NOS COMENTÁRIOS'])
        seq=CONTAS.get(a,[])
        for k,(cue,tex_) in enumerate(seq):
            target=self.cue_time(a,cue)
            if target is None:
                target=1+(ANC[a]['dur']-5)*k/max(1,len(seq));self.events.append(dict(tipo='GATILHO AUSENTE',ancora=a,cue=cue))
            now=self.t-self._q0/FPS
            if target>now:self.wait(target-now,interno=True)
            rt=min(3,max(1.1,(ANC[a]['dur']-3)/max(1,len(seq))*.23))
            self.write_math(tex_,cue,rt)
        self.ate(.995)
