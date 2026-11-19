"""Storyboard completo do handoff v1. Fenômeno à esquerda, construção na Pilha à direita."""
from pecas25 import *
from conteudo25 import CONTAS,SELOS,TITULOS,LOTES
FCD=interpolate_color(ManimColor(FC),ManimColor('#08122B'),.6).to_hex()     # FC a 40% sobre o fundo (forças dos mancais em B5-4)

ZERO=np.zeros(3)
# Plano de câmera (handoff v3 §1.2): (fração inicial, fração final, câmera) por âncora; interpola do plano anterior ao alvo e segura.
PLANO={'B1-3':[(.30,.48,'P_CLOSE')],'B1-4':[(.0,.0,'P_CLOSE')],'B1-5':[(.0,.14,'P_TOPO'),(.80,.94,'P_34')],
       'B2-2':[(.12,.30,'V_CLOSE'),(.78,.94,'V_34')],
       'B5-1':[(.12,.30,'H_TOPO'),(.62,.82,'H_MANCAL')],
       'B6-2':[(.10,.26,'R_CLOSE'),(.40,.56,'R_AXIAL'),(.84,.96,'R_34')],'B6-3':[(.0,.12,'R_AXIAL'),(.40,.58,'R_34')],
       'S2':[(.02,.06,'PL_TOPO'),(.58,.74,'PL_34')]}
SEM_DRIFT={'B3-5','B5-1','B6-2','B6-3','B1-3','B1-4','B1-5','B2-2','S2'}
ESC_P=1.0
ESC_H=1.5

def icone25(tipo):
    if tipo=='pendulo':
        return VGroup(Polygon(P3(0,.5),P3(-.4,-.3),P3(.4,-.3)).set_fill(GEO,.1).set_stroke(GEO,2),Ellipse(width=.8,height=.22).move_to(DOWN*.3).set_stroke(GEO,2),Line(UP*.5,P3(.3,-.32)).set_stroke(STEEL,3),Dot(P3(.3,-.32),radius=.08,color=MAS))
    if tipo=='haltere':
        return VGroup(Line(P3(-.25,-.45),P3(.25,.45)).set_stroke(STEEL,6),Line(DOWN*.55,UP*.55).set_stroke(GEO,1.5),*[Circle(.12).move_to(p).set_fill(STEEL,1).set_stroke(MAS,3) for p in (P3(-.25,-.45),P3(.25,.45))])
    if tipo=='disco':
        return VGroup(Ellipse(width=.95,height=.3).set_fill(STEEL,1).set_stroke(GEO,3),Line(DOWN*.5,UP*.55).set_stroke(GEO,2))
    return VGroup(Circle(.43).set_stroke('#5E6878',10),Circle(.28).set_stroke(GEO,3),*[Line(ORIGIN,.28*P3(math.cos(t),math.sin(t))).set_stroke(STEEL,3) for t in np.linspace(0,2*PI,6)[:-1]],Dot(RIGHT*.33,radius=.05,color=MAS))

def mapa_icones25(tipos,nomes,y):
    return VGroup(*[VGroup(icone25(tp),txt(nm,24)).arrange(DOWN,buff=.18).move_to(P3(1.8+2.05*k,y)) for k,(tp,nm) in enumerate(zip(tipos,nomes))])

def curva3(c,pts,cor=GEO,w=2,trace=False):
    m=VMobject().set_points_as_corners([proj(c,p) for p in pts]).set_stroke(cor,w)
    return DashedVMobject(m,num_dashes=40) if trace else m

class Video25(Lote25):
    def corpo(self):
        nome=type(self).__name__
        if nome=='PB1':
            self.h2=VGroup(txt('UM',30),T('L',40,LMAG),txt('QUE SÓ VIRA',30)).arrange(RIGHT,buff=.13).next_to(self.h1,DOWN,buff=.14,aligned_edge=LEFT);self.add(self.h2)
        else:self.secao(TITULOS[nome])
        for aid in LOTES[nome]:
            if self.plano_cam:self.camera25=dict(CAMS[self.plano_cam[-1][2]])
            self.quadro(aid)
            self._ta0=self._q0/FPS;self._dur=ANC[aid]['dur'];self.plano_cam=PLANO.get(aid)
            self.drift=None if (aid in SEM_DRIFT or aid=='EN' or aid.startswith('A')) else (3.5,.03,9.)
            self.configura(aid)
            if aid in SELOS:self.selo(*SELOS[aid],cor=GEO,borda=GEO)
            self.evento(aid)
            if aid in CONTAS and aid!='B3-4':self.cadeia(aid)
            self.ate(.99)

    def configura(self,a):
        bloco=a.split('-')[0]
        if bloco in ('H1','H2','H3','A1','A2'):
            if self.tipo!='bancada_dupla' or self._q0==0:self.prepara('bancada_dupla','D_34')
            self.flags=dict(desf=0)      # v7: sem desfoque de profundidade (a cena da esquerda fica nítida em 1080p)
            if a in ('H1','A1','A2'):self.tilt.set_value(0 if a=='H1' else self.tilt.get_value())
            if a in ('H1','H2','A1','A2'):self.anda(F.WD,phi=0 if a=='H1' else None)
        elif bloco=='B1':
            if self.tipo!='pendulo_conico' or self._q0==0:self.prepara('pendulo_conico','P_34')
            self.flags=dict(cone=a in ('B1-0','B1-4'),rastro=a in ('B1-0','B1-4'),desf=0)
            self.anda(F.WP if a in ('B1-0','B1-4','B1-7') else 0,phi=0 if a=='B1-1' else None)
        elif bloco=='B2' or a=='B4-3':
            if self.tipo!='corpo_voxel':self.prepara('corpo_voxel','V_34',math.pi)
            self.flags=dict(destaque=a in ('B2-2','B2-3','B2-4'),onda=a=='B2-4',sem_base=True)
            self.anda(math.pi if a in ('B2-1','B2-6','B4-3') else 0,phi=0 if a=='B2-2' else None)
        elif a=='S2':
            self._pl_t0=self.clk.get_value();self.prepara('plataforma_livre','PL_34');self.flags={}
            t0_=self._pl_t0;self.fase_fn=lambda t:F.plataforma(t-t0_)['phi']
        elif a=='S1':
            self.prepara('bancada_dupla','D_S1');self.flags={};self.tilt.set_value(10);self.anda(F.WD,phi=0)
        elif bloco=='B6':
            if self.tipo!='roda_balanceamento':self.prepara('roda_balanceamento','R_34')
            self.flags=dict(raiox=a!='B6-4')
            self.anda(0 if a=='B6-1' else 1.5*PI,phi=0 if a=='B6-1' else None)
        elif a not in ('EN','S1','S2'):
            if self.tipo!='haltere_torto':self.prepara('haltere_torto','H_34B' if bloco=='B4' else ('H_34' if bloco=='B3' else 'H_MANCAL'))
            self.flags=dict(plano=a in ('B3-5','B3-7') or bloco=='B5',rastro=a in ('B3-1','B3-7'),sem_base=bloco in ('B3','B4'))
            self.anda((.8*PI if a in ('B5-1','B5-2','B5-3','B5-4') else 2*PI) if a in ('B3-1','B3-7','B5-1','B5-2','B5-3','B5-4','B5-5','S1') else 0,      # v7: PB5 em câmera lenta (0,4 volta/s na tela)

                      phi=0 if a in ('B3-2','B3-5','B4-1') else None)

    def partes(self,total=True,li=False):
        esc=ESC_P if self.tipo=='pendulo_conico' else (ESC_V*(.55 if self._aid=='B4-3' else 1.) if self.tipo=='corpo_voxel' else (ESC_H if self._aid.startswith(('B3','B4','B5')) else 1.8))
        # B4-3: o corpo remontado fica em pé e esconderia a seta; a base da seta sobe para o topo do corpo e o comprimento acompanha a remontagem (V6)
        if self._aid=='B4-3':
            sm=lambda:(lambda u_:u_*u_*(3-2*u_))(float(np.clip(self.u.get_value(),0,1)))
            b0=lambda e:np.array([0,0,float(np.max(e['posicoes'][:,2]))])*sm();fac=lambda:1.0
            if total:self.seta25('L',b0,lambda e:fac()*e['L'],esc,LMAG)
            self.seta25('Lz',b0,lambda e:fac()*e['axial'],esc,LMAG)
            self.seta25('Lh',lambda e:b0(e)+esc*fac()*e['axial'],lambda e:fac()*e['transversal'],esc,LMAG,True)
            self.label('Lz',r'L_z',lambda e:b0(e)+esc*fac()*e['axial'],LMAG,(-.45,.08,0))
            self.label('Lh',r'L_\perp',lambda e:b0(e)+esc*fac()*(e['axial']+.5*e['transversal']),LMAG,(0,.35,0))
            return esc
        if total:self.seta25('L',ZERO,'L',esc,LMAG)
        if li:
            self.seta25('Li_z',lambda e:e['massa'],lambda e:e['L1']*np.array([0,0,1]),ESC_H,LMAG)
            self.seta25('Li_h',lambda e:e['massa']+ESC_H*e['L1']*np.array([0,0,1]),lambda e:e['L1']*np.array([1,1,0]),ESC_H,LMAG,True)
        else:
            self.seta25('Lz',ZERO,'axial',esc,LMAG)
            self.seta25('Lh',lambda e:esc*e['axial'],'transversal',esc,LMAG,True)
            self.label('Lz',r'L_z',lambda e:esc*e['axial'],LMAG,(-.45,.08,0) if self.tipo in ('haltere_torto','corpo_voxel') else (.4,.1,0))
            self.label('Lh',r'L_h' if self.tipo=='pendulo_conico' else r'L_\perp',lambda e:esc*(e['axial']+.5*e['transversal']),LMAG,(0,.35,0))
        return esc

    def posicao(self):
        self.seta25('r',ZERO,'r',1,VETC)
        frac=.22 if self.tipo=='pendulo_conico' else .5
        self.label('r',r'\vec r_i' if self.tipo=='corpo_voxel' else r'\vec r',lambda e:frac*e['r'],VETC,(-.38,0,0))

    def decompoe(self,indice=1):
        sufixo=str(indice) if self.tipo=='haltere_torto' else 'i'
        r=lambda e:e['massa2'] if indice==2 else e['r']
        self.seta25('r',ZERO,r,1,VETC)
        self.label('r',r'\vec r_'+sufixo,lambda e:.82*r(e),VETC,(-.38,0,0))
        self.seta25('rho',ZERO,lambda e:r(e)*np.array([1,1,0]),1,VETC)
        self.seta25('z',lambda e:r(e)*np.array([1,1,0]),lambda e:r(e)*np.array([0,0,1]),1,VETC,True)
        self.label('rho',r'\vec\rho_'+sufixo,lambda e:.95*r(e)*np.array([1,1,0]),VETC,(0,-.35,0))
        self.label('z','z_'+sufixo+r'|\hat z',lambda e:r(e)*np.array([1,1,.5]),VETC,(.4,0,0))
        self.decoracoes.append(lambda e,c:curva3(c,[[np.linalg.norm(r(e)[:2])*math.cos(t),np.linalg.norm(r(e)[:2])*math.sin(t),r(e)[2]] for t in np.linspace(0,2*PI,97)],GEO,2))

    def torque(self):
        esc=.8 if self.tipo=='pendulo_conico' else .35
        self.seta25('tau',ZERO,'torque',esc,FC)
        self.label('tau',r'\vec\tau',lambda e:esc*e['torque'],FC,(.15,.3,0))

    def inset(self):
        # Espaço dos momentos angulares; nenhum aparato físico dentro do inset.
        def desenha(e,c):
            centro=P3(-1.0,.15) if self.tipo=='pendulo_conico' else P3(-1.4,-2.4);rad=.38 if self.tipo=='pendulo_conico' else .5;cc=centro+UP*.18
            phi=math.atan2(e['transversal'][1],e['transversal'][0]);u=P3(math.cos(phi),math.sin(phi));v=P3(-math.sin(phi),math.cos(phi))
            bx=Rectangle(width=1.3 if self.tipo=='pendulo_conico' else 2.0,height=2.05 if self.tipo=='pendulo_conico' else 2.6).move_to(centro+UP*.1).set_fill('#08122B',.98).set_stroke(GEO,1.2);bx._fundo=True
            g=VGroup(bx,(VGroup(txt('VISTA',24,color=GEO),txt('DE CIMA',24,color=GEO)).arrange(DOWN,buff=.04) if self.tipo=='pendulo_conico' else txt('VISTA DE CIMA',24,color=GEO)).move_to(centro+UP*(.98 if self.tipo=='pendulo_conico' else 1.12)),Circle(rad).move_to(cc).set_stroke(LMAG,2),
                          seta(cc,cc+rad*u,LMAG,5),seta(cc+rad*u,cc+rad*u+.35*v,LMAG,5),T(r'd\vec L',36,LMAG).move_to(centro+DOWN*(.64 if self.tipo=='haltere_torto' else .84)))
            if self.tipo=='haltere_torto':
                # C7: de cima, o plano (eixo, haste) é uma reta; dL (e tau) é perpendicular a ela.
                plano=DashedLine(cc-.7*u,cc+.7*u,dash_length=.07).set_stroke(GEO,2.2)
                esq=Square(.1).set_stroke(GEO,1.6).rotate(math.atan2(u[1],u[0])).move_to(cc+rad*u+.05*(u+v))
                g.add(plano,esq,T(r'\vec\tau',36,FC).move_to(cc+rad*u+.62*v+.1*u),txt('— — PLANO',22,color=GEO).move_to(centro+DOWN*.96))
            return g
        self.decoracoes.append(desenha)

    def hook(self,a):
        """Hook v2: duas bancadas idênticas (haltere reto × torto). Só a do torto balança; o torque dos mancais gira junto com o haltere."""
        dur=ANC[a]['dur'];off=F.OFF_D;pr=lambda p:proj(self.cam(),np.array(p,float))
        if a=='H1':
            for nome,o in (('RETO',-off),('TORTO',off)):
                m=VGroup(txt(nome,28,color=WHITE_),VGroup(T(r'\omega',38,VEL),txt('= 1 VOLTA/S',26,color=VEL)).arrange(RIGHT,buff=.12)).arrange(DOWN,buff=.1).move_to(pr(o+np.array([0,0,.52])))
                m._fica25=True;self.play(Write(m),run_time=.7);m.add_updater(lambda mm,o=o:mm.move_to(pr(o+np.array([0,0,.52]))))
            if not hasattr(self,'regua25'):
                def regua():
                    c_=self.cam();d_=np.array([-math.sin(math.radians(35)),math.cos(math.radians(35)),0]);zz=-1.2
                    a_=proj(c_,-1.12*d_+[0,0,zz]);b_=proj(c_,1.12*d_+[0,0,zz]);g_=VGroup(Line(a_,b_).set_stroke(GEO,2,opacity=.85))
                    for k_ in np.linspace(0,1,11):
                        q_=a_+(b_-a_)*k_;g_.add(Line(q_,q_+DOWN*(.12 if k_ in (0,1,.5) else .07)).set_stroke(GEO,1.6,opacity=.85))
                    return g_
                self.regua25=vivo(regua);self.regua25._fica25=True;self.add(self.regua25)
            linhas=[txtc('MESMA MASSA · MESMO MOTOR',30,{'MASSA':MAS}),txtc('CENTRO DE MASSA NO EIXO',30,{'MASSA':MAS})]
            col=VGroup(*linhas).arrange(DOWN,buff=.32,aligned_edge=LEFT).move_to(P3(3.9,1.2))
            self.hook_col=col
            for k,l in enumerate(linhas):
                self.ate((.22,.6)[k]);self.play(Write(l),run_time=1.8)
            self.ate(.97)
        if a=='H2':
            self.selo('FORA DE ESCALA','',cor=MAS,borda=MAS)
            self.play(self.tilt.animate.set_value(10),run_time=1.2)
            self.forcas_hook()
            t1=txtc('A BASE DO TORTO BALANÇA',30,{'TORTO':WHITE_});t2=txtc('A DO RETO FICA PARADA',30,{})
            col=VGroup(t1,t2).arrange(DOWN,buff=.32,aligned_edge=LEFT).move_to(P3(3.9,1.2));self.hook_col=col
            self.ate(.4);self.play(Write(t1),run_time=1.8);self.ate(.62);self.play(Write(t2),run_time=1.6)
            self.ate(.86);self.congela(math.radians(125))
        if a=='H3':
            self.forcas_hook()
            l1=VGroup(T(r'\omega',48,VEL),txt('CONSTANTE…',30)).arrange(RIGHT,buff=.18)
            l2=txtc('E MESMO ASSIM HÁ TORQUE',30,{'TORQUE':FC})
            col=VGroup(l1,l2).arrange(DOWN,buff=.3,aligned_edge=LEFT).move_to(P3(3.9,1.2))
            self.play(Write(col),run_time=2.4);self.ate(.97)
            self.hook_col=col

    def forcas_hook(self):
        off=F.OFF_D
        for nome,z in (('fino_Fsup',-.45),('fino_Finf',-.85)):
            self.seta25(nome,lambda e,z=z:off+np.array([0,0,z]),nome[5:],.16,FC)

    def abre_pendulo(self):
        """B1-0: o pêndulo de perto; o torque do peso (seta azul, com sombra no piso) gira junto com a bolinha; mostrador de ω constante."""
        self.torque()
        pass      # v7: sem sombra de chão do vetor azul
        m=VGroup(T(r'\omega',48,VEL),txt('CONSTANTE',30)).arrange(RIGHT,buff=.2).move_to(P3(3.8,1.2))
        self.ate(.07);self.play(Write(m),run_time=2)       # v6: a coluna da direita não fica vazia > 3 s
        t=VGroup(txtc('O PESO FAZ TORQUE',30,{'PESO':FC,'TORQUE':FC}),txt('EM RELAÇÃO AO PREGO',30)).arrange(DOWN,buff=.2).move_to(P3(3.8,-.2))
        self.ate(.58);self.play(Write(t),run_time=2.4)
        self.ate(.95);self.play(FadeOut(m),FadeOut(t),run_time=.4)

    def evento(self,a):
        if a in ('H1','H2','H3'):self.hook(a)
        if a=='B1-0':self.abre_pendulo()
        if a in ('A1','A2'):
            logo=ImageMobject(str(ROOT/'assets/branding/overlays/parallax_lab_logo_horizontal.png')).set_width(5.2).move_to(P3(3.6,1.65))
            if a=='A1':
                self.play(FadeIn(logo),run_time=.5);t=txt('BEM-VINDOS AO PARALLAX LAB',30).move_to(P3(3.6,.28));self.play(Write(t),run_time=2.5)
            else:
                t=VGroup(txt('MOMENTO ANGULAR',40,color=LMAG),txt('DO CORPO RÍGIDO',40)).arrange(DOWN,buff=.15).move_to(P3(3.7,1.25));self.play(Write(t),run_time=3)
                mapa=mapa_icones25(['pendulo','haltere','roda'],['PÊNDULO','HALTERE','RODA'],-.8);self.play(LaggedStart(*[Write(m) for m in mapa],lag_ratio=.5),run_time=3)
            self.ate(.95);self.play(FadeOut(t),*([FadeOut(logo)] if a=='A1' else [FadeOut(mapa)]),run_time=.4)
        if a.startswith('B1'):
            if a in ('B1-1','B1-2'):self.posicao();self.seta25('p',lambda e:e['massa'],'p',1.3,MAG);self.label('p',r'\vec p',lambda e:e['massa']+1.3*e['p'],MAG,(.12,.3,0))
            if a=='B1-2':
                self.seta25('L',ZERO,lambda e:self.etapa.get_value()*e['L'],ESC_P,LMAG);self.play(self.etapa.animate.set_value(1),run_time=ANC[a]['dur']*.72)
                self.label('L',r'\vec L',lambda e:ESC_P*e['L'],LMAG,(.3,.2,0))
                self.decoracoes.append(lambda e,c:angulo_reto25(proj(c,ZERO),proj(c,e['r']),proj(c,e['L'])))
                mao=mao_direita(P3(-1.3,1.6),escala=.6);self.play(FadeIn(mao),run_time=.4);self.ate(.9);self.play(FadeOut(mao),run_time=.35)
            if a in ('B1-3','B1-4','B1-5','B1-6','B1-7'):self.partes()
            if a in ('B1-3','B1-6'):
                def angulo_pendulo(e,c):
                    direcao=e['r']*np.array([1,1,0]);direcao/=np.linalg.norm(direcao)
                    arco=[.25*(math.sin(t)*direcao-math.cos(t)*F.Z) for t in np.linspace(0,F.TH,25)]
                    return VGroup(curva3(c,[ZERO,-.45*F.Z],GEO,2,True),curva3(c,arco,ANG,3))
                self.decoracoes.append(angulo_pendulo)
                if a=='B1-3':self.label('angpend',r'\theta',lambda e:.28*(math.sin(F.TH/2)*e['r']*np.array([1,1,0])/np.linalg.norm(e['r'][:2])-math.cos(F.TH/2)*F.Z),ANG,(-.4,0,0))
            if a in ('B1-4','B1-5','B1-7'):
                self.decoracoes.append(lambda e,c:curva3(c,[ESC_P*F.pendulo(t)['L'] for t in np.linspace(0,2*PI,49)],LMAG,2))
            if a=='B1-4':
                self.escreve(r'\|\vec L\||=|0{,}336|\,\mathrm{kg\,m^2/s}',met='mostrador constante',rt=1.2,cores={2:LMAG})
            if a in ('B1-5','B1-6'):self.torque()
            if a=='B1-5':
                # v7: vista de cima em 2D (câmera P_TOPO) no lugar do inset: L_h do prego à ponta, τ no prego (perpendicular), dL na ponta (paralelo a τ)
                self.vetores.pop('Lz',None);self.rotulos.pop('Lz',None)
                self.etapa.set_value(0)
                self.seta25('tau',ZERO,lambda e:self.etapa.get_value()*e['torque'],.35,FC)
                self.label('tau',r'\vec\tau',lambda e:.35*e['torque'],FC,(.15,.3,0))
                self.seta25('dL',lambda e:ESC_P*e['L'],lambda e:self.etapa.get_value()*e['torque']/np.linalg.norm(e['torque']),.15,LMAG)
                self.label('dL',r'd\vec L',lambda e:ESC_P*e['L']+.15*e['torque']/np.linalg.norm(e['torque']),LMAG,(.15,.3,0))
                self.decoracoes.append(lambda e,c:txt('VISTA DE CIMA',24,color=GEO).move_to(P3(-5.6,2.15)).set_opacity(float(np.clip((c['el']-55)/25,0,1))))
                self.play(self.etapa.animate.set_value(1),run_time=1.2)
            if a=='B1-7':
                self.seta25('v',lambda e:e['massa'],'v',.35,VEL)
                for nome in ('Lz','Lh'):
                    self.vetores.pop(nome,None);self.rotulos.pop(nome,None)
                for j in (1,2):
                    fase=j*2*PI/3
                    self.seta25(f'v_amostra{j}',lambda e,p=fase:F.pendulo(self.phi()+p)['massa'],lambda e,p=fase:F.pendulo(self.phi()+p)['v'],.35,VEL)
                    self.seta25(f'L_amostra{j}',ZERO,lambda e,p=fase:F.pendulo(self.phi()+p)['L'],ESC_P,LMAG)
                t=VGroup(txt('RAPIDEZ CONSTANTE',30,color=VEL),txt('VELOCIDADE MUDA',30),txt('DE DIREÇÃO',30)).arrange(DOWN,buff=.25).move_to(P3(3.7,.8));self.play(Write(t),run_time=4)
        if a.startswith('B2'):
            if a in ('B2-2','B2-3'):self.decompoe();self.seta25('v',lambda e:e['massa'],'v',.6,VEL)
            if a=='B2-3':
                self.seta25('Li_z',lambda e:e['massa'],lambda e:e['L1']*np.array([0,0,1]),ESC_LI,LMAG)
                self.seta25('Li_h',lambda e:e['massa'],lambda e:e['L1']*np.array([1,1,0]),ESC_LI,LMAG,True)
            if a=='B2-4':
                self.seta25('Lz',ZERO,lambda e:self.etapa.get_value()*e['axial'],ESC_V,LMAG)
                def fatias(e,c,N=12):
                    # C9: cada cubo que a onda atinge empilha uma fatia (barra fina) na seta vertical de L_z.
                    u_=self.etapa.get_value();ax=ESC_V*e['axial'];g=VGroup()
                    for k in range(N):
                        if (k+.5)/N>u_:break
                        z0=proj(c,ax*k/N);z1=proj(c,ax*(k+1)/N)
                        g.add(Rectangle(width=.26,height=max(np.linalg.norm(z1-z0)-.02,.01)).move_to((z0+z1)/2).set_fill(LMAG,.55 if k%2 else .3).set_stroke(LMAG,1.2))
                    return g
                self.decoracoes.append(fatias)
                self.play(self.etapa.animate.set_value(1),run_time=2)
            if a=='B2-6':
                self.partes()
                ps=self.modelo()['posicoes']
                escala=.13/max(np.linalg.norm(-.01*math.pi*r[2]*r*np.array([1,1,0])) for r in ps)
                for j in range(0,len(ps),23):
                    self.seta25(f'Li{j}',lambda e,j=j:e['posicoes'][j],
                        lambda e,j=j:-.01*math.pi*e['posicoes'][j][2]*e['posicoes'][j]*np.array([1,1,0]),escala,LMAG,True)
        if a.startswith('B3'):
            if a in ('B3-2','B3-3'):
                self.decompoe(2 if a=='B3-3' else 1);self.partes(total=False,li=True)
                self.flags['massafoco']=2 if a=='B3-3' else 1
            if a=='B3-3':
                self.seta25('Li2_z',lambda e:e['massa2'],lambda e:e['L2']*np.array([0,0,1]),ESC_H,LMAG)
                self.seta25('Li2_h',lambda e:e['massa2']+ESC_H*e['L2']*np.array([0,0,1]),lambda e:e['L2']*np.array([1,1,0]),ESC_H,LMAG,True)
            if a=='B3-4':
                # Translações puras: axial com axial, transversal com transversal, sem girar os vetores.
                u=lambda:self.etapa.get_value()
                uh=lambda:self.etapa_h.get_value()
                self.etapa_h.set_value(0);self.soma_final.set_value(0)
                az=lambda e:ESC_H*e['L1']*np.array([0,0,1])
                ht=lambda e:ESC_H*e['L1']*np.array([1,1,0])
                self.seta25('L1z',lambda e:(1-u())*e['massa'],lambda e:e['L1']*np.array([0,0,1]),ESC_H,LMAG)
                self.seta25('L2z',lambda e:(1-u())*e['massa2']+u()*az(e),lambda e:e['L2']*np.array([0,0,1]),ESC_H,LMAG)
                self.seta25('L1h',lambda e:(1-uh())*((1-u())*e['massa']+az(e))+uh()*2*az(e),lambda e:e['L1']*np.array([1,1,0]),ESC_H,LMAG,True)
                self.seta25('L2h',lambda e:(1-uh())*((1-u())*e['massa2']+u()*az(e)+az(e))+uh()*(2*az(e)+ht(e)),lambda e:e['L2']*np.array([1,1,0]),ESC_H,LMAG,True)
                self.seta25('Ltotal',ZERO,lambda e:e['L']*self.soma_final.get_value(),ESC_H,LMAG)
                # Handoff v3 §3.3: a soma vetorial é desenhada ANTES da escrita; depois a caneta escreve a soma e as componentes.
                self.seta25('Ltz',ZERO,lambda e:self.soma_final.get_value()*e['axial'],ESC_H,LMAG)
                self.seta25('Ltp',lambda e:self.soma_final.get_value()*ESC_H*e['axial'],lambda e:self.soma_final.get_value()*e['transversal'],ESC_H,LMAG,True)
                self.selo('SOMA VETORIAL','DOS DOIS BRAÇOS',cor=GEO,borda=GEO)
                self.play(self.etapa.animate.set_value(1),run_time=ANC[a]['dur']*.11)
                self.play(self.etapa_h.animate.set_value(1),run_time=ANC[a]['dur']*.11)
                self.play(self.soma_final.animate.set_value(1),run_time=1.0)     # v6: a voz real é ~13% mais rápida que a estimativa de 2,7 palavras/s
                self.cadeia(a,reserva=3.9)
                self.escreve(r'L_z|=|L_{1z}|+|L_{2z}',met='escrita',rt=1.8)
                self.escreve(r'L_\perp|=|L_{1\perp}|+|L_{2\perp}',met='escrita',rt=1.8)
                self.decoracoes.append(lambda e,c:VGroup(vetor3(c,e['massa'],e['massa']+ESC_H*e['L1'],LMAG).set_opacity(.4),vetor3(c,e['massa2'],e['massa2']+ESC_H*e['L2'],LMAG).set_opacity(.4)))
            if a=='B3-5':
                self.dolly('H_LADO',rt=1.0);self.partes()
                self.decoracoes.append(lambda e,c:angulo_reto25(proj(c,ZERO),proj(c,e['r']),proj(c,e['L'])))
                self.decoracoes.append(lambda e,c:Arc(radius=.45,start_angle=PI/2,angle=PI/3,arc_center=proj(c,ZERO)).set_stroke(ANG,3))
                self.decoracoes.append(lambda e,c:T(r'60^\circ',36,ANG).move_to(proj(c,ZERO)+P3(-.55,.78)))
                self.label('Ltot',r'\vec L',lambda e:.62*ESC_H*e['L'],LMAG,(-.2,.25,0))
            if a=='B3-6':
                self.partes()
                def retangulos(e,c):
                    g=VGroup()
                    for r in (e['massa'],e['massa2']):
                        rho=r*np.array([1,1,0]);zz=r*np.array([0,0,1]);g.add(Polygon(*[proj(c,p) for p in (ZERO,rho,r,zz)]).set_fill(MAS,.12).set_stroke(MAS,2.4))
                    return g
                self.decoracoes.append(retangulos)
            if a=='B3-7':
                self.dolly('H_34');self.partes();self.decoracoes.append(lambda e,c:curva3(c,[ESC_H*F.haltere(t)['L'] for t in np.linspace(0,2*PI,49)],LMAG,2))
            if a=='B3-2':
                self.escreve(r'\vec L_1|=|\vec r_1|\times|m|\vec v_1',met='lei',rt=ANC[a]['dur']*.42)
                self.escreve(r'\vec L_1|=|\vec L_{1z}|+|\vec L_{1\perp}',met='escrita',rt=ANC[a]['dur']*.42)
        if a=='B4-1':
            self.partes();self.x.set_value(0);self.play(self.x.animate.set_value(1),run_time=2)
            self.vetores.pop('Lh',None);self.rotulos.pop('Lh',None)  # C5: L⊥ = 0, rótulo e seta somem juntos
        if a=='B4-2':
            self.partes();self.label('L',r'\vec L',lambda e:ESC_H*e['L'],LMAG,(.42,.1,0))
            self.play(Write(mapa_icones25(['disco','roda','haltere'],['DISCO','RODA','HALTERE'],-2.1)),run_time=2)
        if a=='B4-3':
            self.partes();self.escreve(r'\vec L_\perp|\ne|0',rt=2)
            self.ate(.28);self.anda(0);self.play(self.u.animate.set_value(1),run_time=1.5);self.anda(math.pi)
            self.vetores.pop('Lh',None);self.rotulos.pop('Lh',None)  # C5
            self.pilha.limpa();self.escreve(r'\vec L_\perp|=|0',rt=1.4);self.escreve(r'\vec L|=|I|\vec\omega',rt=1.8)
            eixos=lambda e,c:VGroup(*[curva3(c,[-.4*e['rotacao']@np.array(F.VOX['eixos'])[:,k],.4*e['rotacao']@np.array(F.VOX['eixos'])[:,k]],GEO,2) for k in range(3)])
            self.decoracoes.append(eixos);self.wait(1);self.decoracoes.remove(eixos)
        if a.startswith('B5'):
            self.x.set_value(0)
            if a!='B5-5':self.partes();self.torque()
            if a!='B5-5':self.decoracoes.append(lambda e,c:txt('CÂMERA LENTA',24,color=GEO).move_to(P3(-6.0,-3.4)))
            if a=='B5-1':
                def topo5(e,c):
                    op=float(np.clip((c['el']-55)/25,0,1))
                    if op<.03:return VGroup()
                    Lz_=ESC_H*np.array(e['axial'],float);Lh_=np.array(e['transversal'],float);rh=np.linalg.norm(Lh_);u=Lh_/max(rh,1e-9);tg=np.array(e['torque'],float);tg=tg/max(np.linalg.norm(tg),1e-9)
                    circ=curva3(c,[Lz_+ESC_H*rh*np.array([math.cos(t),math.sin(t),0]) for t in np.linspace(0,2*PI,97)],LMAG,2.4)
                    ponta=Lz_+ESC_H*Lh_;fim=ponta+tg*.16
                    pl=DashedLine(proj(c,Lz_-1.15*ESC_H*rh*u),proj(c,Lz_+1.15*ESC_H*rh*u),dash_length=.09).set_stroke(GEO,2.2)
                    dl=vetor3(c,ponta,fim,LMAG,False,w=6)
                    rd_=proj(c,ponta)-proj(c,Lz_);rot=T(r'd\vec L',40,LMAG).move_to(proj(c,fim)+.5*rd_/max(np.linalg.norm(rd_),1e-6))   # G28 v5: fora do círculo, na direção radial (não sobre o traço)
                    circ.set_fill(opacity=0);circ.set_stroke(opacity=op);pl.set_stroke(opacity=op);dl.set_opacity(op);rot.set_opacity(op)
                    return VGroup(circ,pl,dl,rot)
                self.decoracoes.append(topo5)
            if a=='B5-3':
                for n,z,sg in [('Fsup',-.45,1),('Finf',-.85,-1)]:self.seta25(n,np.array([0,0,z]),n,.16,FC)
                self.label('Fs',r'F',lambda e:np.array([0,0,-.45])+.16*e['Fsup'],FC,(.25,.2,0));self.label('Fi',r'F',lambda e:np.array([0,0,-.85])+.16*e['Finf'],FC,(.25,-.2,0))
                lado=np.array([-math.sin(math.radians(CAMS['H_34']['az'])),math.cos(math.radians(CAMS['H_34']['az'])),0]);q=-.13*lado
                self.decoracoes.append(lambda e,c,q=q,lado=lado:VGroup(Line(proj(c,q+[0,0,-.45]),proj(c,q+[0,0,-.85])).set_stroke(GEO,2),*[Line(proj(c,q+[0,0,z]-.025*lado),proj(c,q+[0,0,z]+.025*lado)).set_stroke(GEO,2) for z in (-.45,-.85)]))
                self.label('d',r'd',lambda e,q=q:q+[0,0,-.55],GEO,(-.3,0,0))
                self.label('distancia',r'0{,}40|\,\mathrm m',lambda e,q=q:q+[0,0,-.75],GEO,(-.3,0,0))
            if a=='B5-4':
                self.seta25('Fc',lambda e:e['massa'],'Fc',.18,FC);self.seta25('Fc2',lambda e:e['massa2'],'Fc2',.18,FC)
                for n,z in (('Fsup',-.45),('Finf',-.85)):self.seta25(n,np.array([0,0,z]),n,.16,FCD)      # v6 §2.9: forças dos mancais a 40%
                self.label('Fc',r'F_c',lambda e:e['massa']+.18*e['Fc'],FC,(.3,.25,0));self.label('Fc2',r'F_c',lambda e:e['massa2']+.18*e['Fc2'],FC,(-.3,-.25,0))
            if a=='B5-5':
                self.anda(2*PI) # 3 voltas/s físicas, exibidas a 1/3.
                crescimento=lambda:1+.6*smooth(np.clip((self.clk.get_value()-self._q0/FPS-1)/1.5,0,1))
                self.seta25('tau',ZERO,lambda e:e['torque']*crescimento()/9,.35,FC)
                self.seta25('Fsup',np.array([0,0,-.45]),lambda e:e['Fsup']*crescimento()/9,.16,FC)
                self.seta25('Finf',np.array([0,0,-.85]),lambda e:e['Finf']*crescimento()/9,.16,FC)
        if a.startswith('B6'):
            if a=='B6-1':
                def cotas_roda(e,c):      # v6 §2.10: ρ (eixo → excesso), z axial (plano central → excesso) e separação axial entre os dois excessos
                    r=e['r'];return VGroup(curva3(c,[np.array([0,.1,0]),r],GEO,2),curva3(c,[np.array([r[0],0,r[2]]),r],GEO,2),curva3(c,[np.array([0,-.1,0]),np.array([0,.1,0])],GEO,2))
                self.decoracoes.append(cotas_roda)
                self.label('rho',r'\rho|=|0{,}20|\,\mathrm m',lambda e:np.array([.5*e['r'][0],.1,.5*e['r'][2]]),GEO,(-.3,.3,0))
                self.label('zax',r'0{,}10\,\mathrm m',lambda e:np.array([e['r'][0],.05,e['r'][2]]),GEO,(.35,0,0))
                self.fixo25={'rho','zax'}
                self.escreve(r'm|=|20|\,\mathrm g',met='dado',rt=ANC[a]['dur']*.20,cores={2:MAS})
                for k,ph in enumerate([0,2*PI/3,25*PI/18]):
                    if k==1:self.selo('HIPÓTESES','ATRITO DESPREZÍVEL',cor=GEO,borda=GEO)
                    self.anda(0,ph);self.wait(1)
                self.selo('FORA DE ESCALA','',cor=MAS,borda=MAS)
            else:
                self.seta25('Lh',ZERO,'transversal',1.6,LMAG,True)
                self.seta25('L',ZERO,'L',1.6,LMAG)
                self.fixo25={'Lperp'}
                if a!='B6-5':self.label('Lperp',r'\vec L_\perp',lambda e:1.6*e['transversal'],LMAG,(-.5,.05,0))
            if a=='B6-3':
                self.decoracoes.append(lambda e,c:VGroup(curva3(c,[ZERO,np.array([0,0,-.3])],GEO,2)))
                self.label('Rrola',r'R|=|0{,}30|\,\mathrm m',lambda e:np.array([0,0,-.15]),GEO,(.45,0,0));self.fixo25=set(self.fixo25)|{'Rrola'}
            if a in ('B6-3','B6-4'):
                self.seta25('Fc',lambda e:e['massa'],'Fc',.014,FC);self.seta25('Fc2',lambda e:e['massa2'],'Fc2',.014,FC)
            if a in ('B6-3','B6-4','B6-5'):
                self.seta25('Fa1',np.array([0,.25,0]),'Fa1',.026,FC)
                self.seta25('Fa2',np.array([0,-.25,0]),'Fa2',.026,FC)
            if a=='B6-4':
                def graf(e,c):
                    o=P3(1.3,-2.15);pts=[o+P3(t*2.3,.7*math.sin(t*2*PI)) for t in np.linspace(0,2,121)]
                    return VGroup(Line(o+LEFT*.1,o+RIGHT*5.0).set_stroke(GEO,2),VMobject().set_points_as_corners(pts).set_stroke(FC,3.5),T(r'1/15\,\mathrm s',40,WHITE_).move_to(o+P3(1.15,-.82)),txt('FORÇA NUM APOIO',24,color=FC).move_to(o+P3(2.5,1.05)))
                self.decoracoes.append(graf)
            if a=='B6-5':
                self.play(self.bal.animate.set_value(1),run_time=2)
                self.label('principal','@EIXO\nPRINCIPAL',lambda e:np.array([0,.4,0]),GEO,(.4,0,0))
        if a=='S1':
            off=F.OFF_D;self.sem_ocl25={'Ltorto','Lreto'};self.grossas25={'Ltorto','Lreto'}
            def cubo_torto(e):     # o cubo do torto balança: a base da seta acompanha o cubo (rotação de 'tilt' em torno do pé, eixo girando com a fase)
                A_=math.radians(self.tilt.get_value());ph_=self.phi()
                return off+1.115*np.array([math.sin(A_)*math.cos(ph_),math.sin(A_)*math.sin(ph_),math.cos(A_)-1])
            self.seta25('Ltorto',cubo_torto,'L',1.2,LMAG)
            self.seta25('Lreto',-off,np.array([0,0,F.I_RETO*F.WD]),1.2,LMAG)
            self.label('Ltorto',r'\vec L',lambda e:cubo_torto(e)+1.2*e['L'],LMAG,(.3,.2,0))
            self.label('Lreto',r'\vec L',lambda e:-off+np.array([0,0,1.2*F.I_RETO*F.WD]),LMAG,(-.3,.2,0))
            for nome,o in (('RETO',-off),('TORTO',off)):
                t=txt(nome,28,color=WHITE_);t.add_updater(lambda mm,o=o:mm.move_to(proj(self.cam(),o+np.array([0,0,-1.32]))));self.add(t)
        if a=='S2':
            t0_=self._pl_t0
            def mostrador():
                v=round(F.plataforma(self.clk.get_value()-t0_)['omega']/(2*PI),1)
                return VGroup(T(r'\omega',60,VEL),txt(f'= {v:.1f} VOLTAS/S'.replace('.',','),34,color=VEL)).arrange(RIGHT,buff=.22).move_to(P3(3.9,.4))
            self.mos=vivo(mostrador);self.add(self.mos)
            self.selo('SEM TORQUE EXTERNO','',cor=GEO,borda=GEO)
        if a=='EN':
            logo=ImageMobject(str(ROOT/'assets/branding/overlays/parallax_lab_logo_horizontal.png')).set_width(6).move_to(P3(0,1.5))
            self.play(*[f.op.animate.set_value(0) for f in self.fundos.values()],FadeOut(self.h1),FadeOut(self.wm),*([FadeOut(self.h2)] if self.h2 is not None else []),FadeIn(logo),run_time=.7)
            if self.h2 is not None:self.h2=None
            t=txt('INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS',30).move_to(P3(0,-.15));self.play(Write(t),run_time=3)
            q=VGroup(txt('E SE A RODA TIVESSE MASSA A MAIS',30,color=MAS),txt('SÓ DE UM LADO?',30,color=MAS)).arrange(DOWN,buff=.2).move_to(P3(0,-1.6));ic=icone25('roda').scale(1.7).move_to(P3(-5.3,-1.6));self.play(Write(q),Create(ic),run_time=3)
            def desenha_aneis():
                tt=self.clk.get_value()
                return VGroup(*[DashedVMobject(ParametricFunction(lambda t,k=k:P3((3.5+.25*k)*math.cos(t+(-1)**k*.08*tt),1.7+(1.05+.10*k)*math.sin(t+(-1)**k*.08*tt)),t_range=[0,2*PI]),num_dashes=55).set_stroke(VEL,1.5,opacity=.7) for k in range(3)])
            aneis=vivo(desenha_aneis);self.add(aneis)
            self.ate(.9);ripple=Circle(.45).move_to(logo).set_stroke(VEL,3);self.play(Create(ripple),run_time=.3);self.play(FadeOut(ripple,scale=2.4),run_time=.5)
        if a=='B1-6':
            self.label('ell',r'\ell|=|1{,}00|\,\mathrm m',lambda e:.5*e['massa'],VETC,(-.4,0,0))
            self.label('theta',r'\theta|=|30^\circ',lambda e:ZERO,ANG,(-.3,.3,0))
        if a in ('B3-1','B3-5','B5-4'):
            curto=True
            if a!='B5-4':      # v7: no B5-4 só ficam L, τ e F_c (sem m, ℓ nem cota)
                self.label('m',r'm' if curto else r'm|=|0{,}40|\,\mathrm{kg}',lambda e:e['massa'],MAS,(-.55,.38,0))
                self.label('ell',r'\ell' if curto else r'\ell|=|0{,}30|\,\mathrm m',lambda e:.5*e['massa'],VETC,(-.4,0,0))
            if a=='B3-1':     # v6 §2.8: arco de α entre a haste (massa de cima) e o eixo vertical; rótulo junto do arco
                def angulo_haltere(e,c):
                    d=e['r']*np.array([1,1,0]);d=d/np.linalg.norm(d)
                    return VGroup(curva3(c,[.17*(math.cos(t)*F.Z+math.sin(t)*d) for t in np.linspace(0,F.AH,25)],ANG,3))
                self.decoracoes.append(angulo_haltere)
                self.label('alpha',r'\alpha|=|30^\circ',lambda e:.17*(math.cos(F.AH/2)*F.Z+math.sin(F.AH/2)*e['r']*np.array([1,1,0])/np.linalg.norm(e['r'][:2])),ANG,(.78,.1,0))
            elif a!='B5-4':self.label('alpha',r'\alpha' if curto else r'\alpha|=|30^\circ',lambda e:ZERO,ANG,(.4,0,0))     # v6: no B5-4 o α não leva rótulo (folga com L⊥ < 0,15)
        if a=='B3-1':
            self.wait(.8);self.selo('HIPÓTESES','MASSAS PONTUAIS',cor=GEO,borda=GEO)
            self.wait(.8);self.selo('HIPÓTESES',[[T(r'\omega',36,VEL),txt('CONSTANTE',24)]],cor=GEO,borda=GEO)
            self.escreve(r'm|=|0{,}40|\,\mathrm{kg}',met='dado',rt=2,cores={2:MAS})
            self.escreve(r'\ell|=|0{,}30|\,\mathrm m',met='dado',rt=2,cores={2:VETC})
            self.escreve(r'\alpha|=|30^\circ',met='dado',rt=2,cores={2:ANG})
        if a=='B6-1':
            self.escreve(r'\rho|=|0{,}20|\,\mathrm m',met='dado',rt=ANC[a]['dur']*.25,cores={2:VETC})
            self.escreve(r'z_{\mathrm{axial}}|=|\pm|0{,}10|\,\mathrm m',met='dado',rt=ANC[a]['dur']*.30,cores={0:VETC,3:VETC})

    def cadeia(self,a,reserva=0.):
        linhas=CONTAS[a];ant=None;deriv=None
        n_=[max(1,len(re.sub(r'[{}|^_ ]|\\[a-zA-Z]+','',l)) ) for l in linhas];peso_=[w/sum(n_) for w in n_]
        for i,s in enumerate(linhas):
            # Cada passo ocupa sua janela de fala. O movimento do fenômeno continua em cada play.
            alvo=.02 if i==0 else .08+.86*i/len(linhas);self.ate(alvo)
            if a=='B1-1' and i==1:self.selo('HIPÓTESES','REFERENCIAL INERCIAL',cor=GEO,borda=GEO)
            if a=='B2-1' and i==1:self.selo('HIPÓTESES','AOS PARES',cor=GEO,borda=GEO)
            if a=='B2-1' and i==2:self.selo('HIPÓTESES','NA MESMA LINHA',cor=GEO,borda=GEO)
            mesmo=ant is not None and (tokens(nota(s))[0]==ant[0]._partes[0][0] or a in ('B1-3','B2-4','B3-3','B4-2'))
            met='GM' if mesmo else ('lei' if i==0 else 'escrita')
            if a=='B4-1' and i==1:met='GM'
            if a=='B2-1' and i in (1,3):met='GM'
            if a=='B2-1' and i==3:
                ant=deriv;self.pilha.so(deriv[0],rt=.3)
            voos={}
            for j,t in enumerate(tokens(s)):
                for key,(tex,fn,cor,off) in self.rotulos.items():
                    if t==tex or t in tokens(tex):
                        m,idx=rotulo_modelo(tex,cor)
                        if key in getattr(self,'_rotulos_atuais',{}):m.move_to(self._rotulos_atuais[key])
                        else:m.move_to(proj(self.cam(),fn(self.modelo()))+np.array(off))
                        voos[j]=m if idx is None else VGroup(*[m[0][n] for n in idx[tokens(tex).index(t)]])
                        break
            if met=='GM':voos={}
            mapas=None
            if a=='B1-1' and i==2:
                mapas=lambda B,ib,A,ia:[(ib[0],ia[0]),(ib[1],ia[1]),(ib[2],ia[2]),(ib[3],ia[3]+ia[4])]
            if a=='B1-6' and i==2:
                riscos=VGroup()
                riscos._risco=True
                for ids in [ant[1][0][:1],ant[1][0][2:3],ant[1][0][3:7],ant[1][4][:1],ant[1][4][2:3],ant[1][4][4:8]]:
                    gg=gl(ant[0],ids);riscos.add(Line(gg.get_corner(DL),gg.get_corner(UR)).set_stroke(WHITE_,2))
                self.play(Create(riscos),run_time=.4)
                self.play(FadeOut(riscos),run_time=.25)
                mapas=lambda B,ib,A,ia:[(ib[0][1:2],ia[0]),(ib[1],ia[1]),(ib[2]+ib[4][1:2],ia[2]),(ib[4][2:4],ia[3]),(ib[4][-4:-1],ia[4]),(ib[4][-1:],ia[5])]
            if a=='B3-3' and i==3:
                B,ib=ant
                neg1=gl(B,ib[3][1:2]);neg2=gl(B,ib[4][1:2]);ponto=(neg1.get_center()+neg2.get_center())/2+DOWN*.85
                cp1,cp2=neg1.copy(),neg2.copy();self.add(cp1,cp2)
                cp1._risco=cp2._risco=True
                self.play(cp1.animate(rate_func=rush_from).move_to(ponto),cp2.animate(rate_func=rush_from).move_to(ponto).rotate(PI/2),run_time=.35)
                fusao=VGroup(cp1,cp2);self.wait(.12);self.play(FadeOut(fusao),run_time=.2)
                mapas=lambda B,ib,A,ia:[(ib[0],ia[0]),(ib[1],ia[1]),(ib[2],ia[2]),(ib[3][2:-1],ia[3]),(ib[4][2:-1],ia[4])]
            if a=='B2-3' and i==2:
                mapas=lambda B,ib,A,ia:[(ib[0],ia[0]),(ib[1],ia[1]),(ib[2][1:4],ia[2]),(ib[3],ia[3]),(ib[4],ia[4]),(ib[5],ia[5]),(ib[2][5:7],ia[7]),(ib[2][7:9],ia[8]),(ib[3],ia[9]),(ib[4],ia[10]),(ib[5],ia[11])]
            cs={};lhs=tokens(s)[0]
            familia=LMAG if 'L' in lhs else (FC if ('F' in lhs or 'tau' in lhs) else (VEL if ('omega' in lhs or lhs=='v') else WHITE_))
            if lhs==r'\sum':familia=MAS
            for j,t in enumerate(tokens(s)):
                if re.fullmatch(r'\d+\{,\}\d+|\d{2,}',t):cs[j]=familia
                if t in ('0{,}40','0{,}020') and a not in ('B5-3',):cs[j]=MAS
                if t in ('0{,}30','0{,}15','0{,}20'):cs[j]=VETC
                if t=='0{,}52':cs[j]=GEO
                if a=='B6-4' and t=='50':cs[j]=VEL
            if s.startswith('T|'):cs[0]=WHITE_
            # v6 (voz real): a janela da linha nunca passa da fatia que sobra da fala (a cena segue a voz); piso 0,16 s/glifo (handoff §2.6), 0,20 quando couber
            rt_=max(1.0,ANC[a]['dur']*.86*peso_[i]-1);disp_=(self.resta()-(.9 if i==len(linhas)-1 else .5)-reserva-.45*(len(linhas)-1-i))*n_[i]/sum(n_[i:])   # .45 s de sobra por linha restante (sublinha, voo, resultado)
            rt_=max(.16*n_[i],min(rt_,disp_))
            ant=self.escreve(s,src=ant,met=met,voos=voos,rt=rt_,acc=a in ('B2-5','B5-2'),cores=cs,mapas=mapas,final=i==len(linhas)-1 or a=='S1',cor_final=familia)
            if a=='B2-1' and i==1:deriv=ant
            if i==len(linhas)-1:self.resultado(ant,FC if a.startswith('B5') or a=='B6-3' else LMAG)
        if a=='B3-6':
            ult=self.pilha.ultima();t=txt('PRODUTOS DE INÉRCIA',26,color=MAS).next_to(ult,DOWN,buff=.3,aligned_edge=LEFT);self.play(Write(t),run_time=1)
        if a=='S1':
            self.ate(.79);self.pilha.limpa(rt=.4)
            defs=[(r'L_z|=|I_z|\omega','NÃO É O VETOR INTEIRO'),(r'\vec L','GIRANDO PEDE TORQUE'),(r'\vec L|\parallel|\vec\omega','EIXO PRINCIPAL')]
            for k,(m,t) in enumerate(defs):
                text=VGroup(Mx(m,size=46)[0],txt(t,30)).arrange(DOWN,buff=.12).move_to(P3(4,1.65-k*1.65))
                bx=RoundedRectangle(width=6.4,height=1.4,corner_radius=.14).move_to(text).set_fill(PANEL,.95).set_stroke(width=0)
                self.play(FadeIn(bx),Write(text),run_time=1)
            fim_=VGroup(T(r'\omega',44,VEL),txt('CONSTANTE ·',26),T(r'\vec L',44,LMAG),txt('MUDA DE DIREÇÃO',26)).arrange(RIGHT,buff=.18)
            if fim_.width>6.4:fim_.scale(6.4/fim_.width)
            fim_.move_to(P3(4,-3.08));self.play(Write(fim_),run_time=1.6);self.wait(1)     # v6 §2.12

def angulo_reto25(o,a,b):
    u=(a-o)/max(np.linalg.norm(a-o),1e-8);v=(b-o)/max(np.linalg.norm(b-o),1e-8)
    return VMobject().set_points_as_corners([o+.2*u,o+.2*(u+v),o+.2*v]).set_stroke(GEO,2.4)
