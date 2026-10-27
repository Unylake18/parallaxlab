"""Repaginação aprovada: fenômeno → geometria → equação → fenômeno.

As únicas entradas físicas são as de modelo_orbital.py. A câmera é uma
projeção compartilhada e não aplica forças nem altera as trajetórias SI.
"""
import json, math, os
from pathlib import Path
import numpy as np
from functools import lru_cache
from manim import *
from MF_Tools import TransformByGlyphMap
from template.config_horizontal import BACKGROUND_COLOR, WATERMARK_PATH
from modelo_orbital import R_T, MU, integrar, lancamento, conica, periodo, v_circular, validar
from cena_v1 import texto, equacao, satelite, astronauta
from cena_v1 import seta as seta_base
from geometria_visual import CameraOrbital, globo, BLUE, LIGHT, WHITE, VIOLET
from superficie import lua_visual
from cadeia_equacoes import EquacoesOrbitais
from sistema_lunar import SistemaLunar
from matematica_visual import formula, medida, MAGENTA, valor_tempo

PASTA=Path(__file__).resolve().parent


@lru_cache(maxsize=256)
def _texto_base(s,size,cor): return texto(s,size,cor)


def texto_cache(s,size,cor=WHITE):
    return _texto_base(s,size,cor).copy()
CYAN='#35D9FF'; MUTED='#BCC9ED'


def seta(*args,**kwargs):
    return seta_base(*args,**kwargs).set_z_index(45)


TITULOS={
 'E se a pedra fosse lançada cada vez mais rápido?':'E se lançássemos a pedra cada vez mais rápido?',
 'Ele nunca parou de cair.':'Ele continua caindo.',
 'O que muda quando retiramos a gravidade?':'Sem gravidade, seguiria em linha reta.',
 'Como a velocidade gira':'A gravidade muda a direção da velocidade.',
 'Agora: órbita circular a 400 km':'Quanto ele cai em um segundo?',
 'Ele cai — e a Terra curva para longe.':'A queda acompanha a curva da órbita.',
 'Dentro da estação: tudo cai junto':'Por que os astronautas flutuam?',
 'Duas órbitas circulares. O mesmo relógio.':'Mais alto, mais devagar.',
 'Ajustar a velocidade. Depois, lançar.':'Só a velocidade inicial muda.',
 'Retomando o caso de impacto':'A Terra está no caminho.',
 'Experimento mental de Newton':'O canhão de Newton.',
 }


class OrbitaRepaginada(EquacoesOrbitais, SistemaLunar, Scene):
    def get_moving_and_static_mobjects(self, animations):
        # Cairo guarda referências à família inicial durante cada play. A Terra
        # troca imagem por horizonte e as linhas mudam de segmentos; desenhar
        # apenas as raízes atuais evita reapresentar filhos já removidos.
        # Sobrescrever esta etapa evita a expansão antecipada da família feita
        # pelo método padrão, mesmo quando get_moving_mobjects retorna raízes.
        return list(self.mobjects), []

    def construct(self):
        self.camera.background_color=BACKGROUND_COLOR
        self.cam=CameraOrbital(); self.orb=lancamento(1.06*R_T,.55)
        self.tau=ValueTracker(0); self.fator=ValueTracker(.55)
        self.loop=False; self.tracar=True; self.prever=False
        self.mostrar_montanha=True; self.mostrar_bola=True
        self.earth_alpha=ValueTracker(1); self.path_alpha=ValueTracker(1); self.bola_alpha=ValueTracker(1)
        self.earth_marker=ValueTracker(0)
        self.earth_center=lambda: np.array([0.,0.])
        self.custom_pos=None; self.overlays=[]; self.tempos=[]; self.marcos=[]
        self.historias=[]; self.extra=[]; self.cabecalho=None
        self.wm=ImageMobject(str(WATERMARK_PATH)).set_width(1.92).set_opacity(.45).to_corner(UR,buff=.30).set_z_index(200)
        self.tag=texto('GRAVITAÇÃO — ÓRBITAS',18).set_opacity(.6).to_corner(UL,buff=.38).set_z_index(200)
        self.terra=Group()
        def atualizar_terra(m):
            m.remove(*m.submobjects)
            if self.earth_marker.get_value()>self.cam.k:
                m.add(globo(self.cam.p(self.earth_center()),self.earth_marker.get_value(),
                            np.degrees(self.cam.incl.get_value()),np.degrees(self.cam.roll.get_value()),self.earth_alpha.get_value()))
            else: m.add(self.cam.planeta(self.earth_center(),self.earth_alpha.get_value()))
        self.terra.add_updater(atualizar_terra,call_updater=True)
        self.relevo=always_redraw(lambda:self.cam.montanha() if self.mostrar_montanha else VGroup())
        self.trilha=always_redraw(self.desenhar_trilha)
        self.pedra=always_redraw(self.desenhar_bola)
        faixa=VGroup(Rectangle(width=17,height=1.9,stroke_width=0,fill_color=BACKGROUND_COLOR,fill_opacity=1).move_to([0,3.61,0]))
        for i in range(7):
            faixa.add(Rectangle(width=17,height=.05,stroke_width=0,fill_color=BACKGROUND_COLOR,
                                fill_opacity=1-(i+.5)/7).move_to([0,2.63-.05*i-.025,0]))
        self.faixa=faixa.set_z_index(90)
        self.add(self.terra,self.relevo,self.trilha,self.pedra,self.faixa,self.wm,self.tag)
        selecionados={int(x) for x in os.environ.get('SO','').split(',') if x.strip()}
        self.capturas=os.environ.get('QUADROS')=='1'
        for n in range(1,19):
            pular=bool(selecionados and n not in selecionados)
            self.gravando=not pular
            self.renderer._original_skipping_status=pular or self.capturas
            self.renderer.skip_animations=pular or self.capturas
            inicio=float(self.time)
            getattr(self,f'n{n:02d}')()
            if not pular:
                self.tempos.append(dict(bloco=f'N{n:02d}',inicio=inicio,fim=float(self.time)))
                if self.capturas: self.marco(f'N{n:02d}_final')
            elif selecionados:
                self.renderer.time=inicio
            if selecionados and n>=max(selecionados): break
        nome='timing_v2' + ('_'+ '_'.join(map(str,sorted(selecionados))) if selecionados else '')
        if not self.capturas:
            (PASTA/(nome+'.json')).write_text(json.dumps(dict(blocos=self.tempos,marcos=self.marcos,
                duracao=float(self.time),fps=config.frame_rate),indent=2,ensure_ascii=False),encoding='utf-8')
        validar()

    def wait(self,duration=1,**kwargs):
        kwargs.setdefault('frozen_frame',True)
        return super().wait(duration,**kwargs)

    def marco(self,nome):
        if not self.gravando: return
        self.marcos.append(dict(nome=nome,tempo=float(self.time)))
        if self.capturas:
            from PIL import Image
            out=PASTA/'qa_v2_estatico'; out.mkdir(exist_ok=True)
            self.update_mobjects(0); self.renderer.static_image=None
            self.renderer.update_frame(self,ignore_skipping=True)
            Image.fromarray(self.renderer.get_frame()).save(out/(nome+'.png'))

    def estado(self):
        if self.custom_pos: return self.custom_pos(),np.zeros(2)
        t=self.tau.get_value()
        if self.loop: t=t%self.orb.t[-1]
        return self.orb.estado(t)

    def pos(self): return self.cam.si(self.estado()[0])

    def desenhar_bola(self):
        p=self.estado()[0]/R_T
        vis=self.mostrar_bola and self.cam.visivel(p,self.earth_center())
        r=max(.058,min(.145,.003*self.cam.k))
        m=VGroup(Dot(self.cam.p(p),r*2.6,color=WHITE).set_opacity(.14),Dot(self.cam.p(p),r,color='#C4D2DF'),
                 Dot(self.cam.p(p)+r*np.array([-.24,.24,0]),r*.55,color=WHITE)).set_z_index(35)
        ba=self.bola_alpha.get_value()
        m.set_opacity(ba if vis else 0)
        m[0].set_opacity(.14*ba if vis else 0)
        return m

    def desenhar_trilha(self):
        if self.custom_pos: return VGroup()
        if self.prever:
            pts=conica(np.linalg.norm(self.orb.r[0]),self.fator.get_value(),alcance=6*R_T)[0]
            return self.cam.linha(pts/R_T,BLUE,2.4,ocultar=True).set_stroke(opacity=.55)
        if self.tracar and not self.loop:
            t=self.tau.get_value(); i=np.searchsorted(self.orb.t,t)
            pts=np.vstack([self.orb.r[:max(i,1):4],self.orb.estado(t)[0]])
        else: pts=np.vstack([self.orb.r[::4],self.orb.r[-1]])
        a=self.path_alpha.get_value()
        halo=self.cam.linha(pts/R_T,BLUE,8,ocultar=True).set_stroke(opacity=.16*a)
        return VGroup(halo,self.cam.linha(pts/R_T,BLUE,2.6,ocultar=True).set_stroke(opacity=a)).set_z_index(20)

    def trocar(self,antigo,novo,junto=(),sai=.3,entra=.4):
        """Saída antes da entrada: nunca duas frases legíveis na mesma região.
        `junto` roda em paralelo, preservando o movimento físico durante a troca."""
        passos=([FadeOut(antigo,run_time=sai)] if antigo else [])+[FadeIn(novo,run_time=entra)]
        self.play(AnimationGroup(Succession(*passos),*junto))

    def titulo(self,s,junto=()):
        s=TITULOS.get(s,s)
        novo=texto(s,34,largura=13.6).move_to([0,2.9,0]).set_z_index(100)
        for palavra,cor in (('gravidade',CYAN),('gravitacional',CYAN),('volta',MAGENTA),('tempo',MAGENTA),('Terra',BLUE)):
            if palavra in s:
                i=s.index(palavra)
                # Text(str): glifos em ordem; espaços não geram submobjetos
                antes=len(s[:i].replace(' ',''))
                novo[antes:antes+len(palavra)].set_color(cor)
        self.trocar(self.cabecalho,novo,junto)
        self.cabecalho=novo

    def nota_equacao(self,s,xy=(2.8,-1.95)):
        novo=texto(s,25,WHITE,largura=6.8).move_to([*xy,0]).set_z_index(100)
        antigo=getattr(self,'nota_atual',None)
        if antigo and antigo in self.overlays: self.overlays.remove(antigo)
        self.trocar(antigo,novo,sai=.25,entra=.35)
        self.nota_atual=novo; self.overlays.append(novo)

    def glifos(self,a,b,*mapas,dur=1.7):
        """Mapas explícitos, com fades dos termos novos e normalização final."""
        ids={id(x) for x in a.get_family()+b.get_family()}
        self.play(TransformByGlyphMap(a,b,*mapas,auto_fade=True,shift_fades=False,
                                     printing=False),run_time=dur)
        restos=[m for m in self.mobjects if any(id(x) in ids for x in m.get_family())]
        self.remove(*restos); self.add(b)

    def escrever(self,s,xy=(0,-2.55),size=27,color=WHITE):
        m=texto(s,size,color,largura=13.7).move_to([*xy,0]).set_z_index(100)
        self.overlays.append(m); self.play(FadeIn(m),run_time=.5); return m

    def math(self,s,xy=(0,-2.48),size=45):
        m=formula(s,size).move_to([*xy,0]); self.overlays.append(m)
        self.play(FadeIn(m),run_time=.75); return m

    def limpar(self):
        if self.overlays:
            for m in self.overlays: m.clear_updaters(recursive=True)
            self.play(*[FadeOut(m) for m in self.overlays],run_time=.6)
            self.overlays=[]

    def olhar(self,x=0,y=0,span=6.4,incl=0,roll=0,dur=1.6):
        inicio=np.array([self.cam.x.get_value(),self.cam.y.get_value()]); fim=np.array([x,y])
        s0=self.cam.span.get_value(); i0=self.cam.incl.get_value(); r0=self.cam.roll.get_value()
        dummy=ValueTracker(0)
        def mover(m,a):
            u=smooth(a); s=math.exp(math.log(s0)*(1-u)+math.log(span)*u)
            if span<s0:
                foco=fim+(inicio-fim)*(1-u)*s/s0
            else:
                foco=inicio+(fim-inicio)*u*s/span
            self.cam.x.set_value(foco[0]); self.cam.y.set_value(foco[1]); self.cam.span.set_value(s)
            self.cam.incl.set_value(i0+(incl-i0)*u); self.cam.roll.set_value(r0+(roll-r0)*u)
        self.play(UpdateFromAlphaFunc(dummy,mover),run_time=dur,rate_func=linear)
        self.remove(dummy)

    def configurar(self,r,f,duracao=None):
        self.orb=(integrar([0,r],[f*v_circular(r),0],duracao) if duracao else lancamento(r,f))
        self.tau.set_value(0); self.fator.set_value(f); self.loop=False
        self.custom_pos=None; self.tracar=True; self.prever=False; self.mostrar_bola=True

    def vetor_v(self,comprimento=1.1):
        def criar():
            r,v=self.estado(); p=self.cam.si(r)
            q=self.cam.si(r+v*100)-p
            a=seta(p,p+comprimento*q/max(np.linalg.norm(q),1e-8),WHITE)
            return a.set_opacity(1 if self.cam.visivel(r/R_T,self.earth_center()) else 0)
        return always_redraw(criar)

    def vetor_g(self,comprimento=.9):
        def criar():
            p=self.pos(); d=self.cam.p(self.earth_center())-p
            a=seta(p,p+comprimento*d/max(np.linalg.norm(d),1e-8),CYAN)
            return a.set_opacity(1 if self.cam.visivel(self.estado()[0]/R_T,self.earth_center()) else 0)
        return always_redraw(criar)

    def voo(self,segundos=6,span=None,seguir=True,foco_final=None):
        fim=self.orb.t[-1]
        if self.fator.get_value()>=math.sqrt(2):
            ids=np.flatnonzero(np.linalg.norm(self.orb.r,axis=1)>=6*R_T)
            if len(ids): fim=self.orb.t[ids[0]]
        inicio=self.tau.get_value(); cam0=np.array([self.cam.x.get_value(),self.cam.y.get_value()]); sp0=self.cam.span.get_value()
        sp1=span or sp0; dummy=ValueTracker(0)
        def mover(m,a):
            u=smooth(a); self.tau.set_value(inicio+(fim-inicio)*a)
            p=self.estado()[0]/R_T
            if seguir:
                s=sp0+(sp1-sp0)*a**.55
                if sp1>3:
                    peso=1-u
                    foco=np.zeros(2) if foco_final is None else np.asarray(foco_final)
                    alvo=p*peso+foco*(1-peso)
                else:
                    v=self.estado()[1]; alvo=p+.08*s*v/max(np.linalg.norm(v),1e-8)
                entrada=smooth(min(1,a/.06))
                alvo=cam0*(1-entrada)+alvo*entrada
                self.cam.x.set_value(alvo[0]); self.cam.y.set_value(alvo[1])
                self.cam.span.set_value(s)
        self.play(UpdateFromAlphaFunc(dummy,mover),run_time=segundos,rate_func=linear)

    def n01(self):
        self.titulo('E se a pedra fosse lançada cada vez mais rápido?')
        self.escrever('montanha idealizada · sem atmosfera',(0,-2.6),23,MUTED)
        canhao=self.escrever('canhão idealizado',(-3.6,1.45),27,WHITE)
        lc=Line([-2.2,1.3,0],self.cam.p((-.023,1.061)),color=WHITE,stroke_width=1.5).set_z_index(100)
        self.play(Create(lc),run_time=.5); self.wait(.8)
        pedra=self.escrever('pedra',(2.5,1.55),27,WHITE)
        lp=Line([1.85,1.4,0],self.pos()+.15*UP,color=WHITE,stroke_width=1.5).set_z_index(100)
        self.play(Create(lp),run_time=.5)
        self.marco('N01_canhao_proximo'); self.wait(1)
        self.play(*[FadeOut(x) for x in (canhao,lc,pedra,lp)],run_time=.6)
        self.overlays.remove(canhao); self.overlays.remove(pedra)
        for j,(f,span) in enumerate(zip((.55,.80,.985,1.),(.75,1.5,6.4,6.4))):
            if j:
                self.escrever('Nova tentativa · mesmo ponto de lançamento',(0,2.25),23,VIOLET)
                self.olhar(0,1.035,.30,dur=1.5); self.configurar(1.06*R_T,f)
                self.limpar(); self.escrever('montanha idealizada · sem atmosfera',(0,-2.6),23,MUTED)
            else: self.configurar(1.06*R_T,f)
            av=self.vetor_v(.7+.2*j); self.add(av)
            if j==0:
                vl=self.escrever('velocidade inicial',(2.8,1.3),24,WHITE)
                lv=Line([1.55,1.12,0],av.get_end(),color=WHITE,stroke_width=1.3).set_z_index(100)
                self.play(Create(lv),run_time=.35)
                self.wait(.8); self.play(FadeOut(vl),FadeOut(lv),run_time=.35); self.overlays.remove(vl)
            self.wait(.7); self.play(FadeOut(av),run_time=.35)
            self.voo(5 if j<2 else 7,span)
            if self.orb.impacto:
                self.play(Flash(self.pos(),color=LIGHT,line_length=.09,flash_radius=.16),run_time=.5)
                pts=self.orb.r.copy()/R_T
                hist=always_redraw(lambda ps=pts:self.cam.linha(ps[::4],BLUE,1.3).set_stroke(opacity=.28))
                self.historias.append(hist); self.add(hist)
            else:
                self.loop=True; self.tracar=False
            self.marco(f'N01_lancamento_{j+1}'); self.wait(.8)
        self.limpar(); self.titulo('A última tentativa continua em voo')
        aviso=self.escrever('mesma órbita circular · vista oblíqua',(0,-2.6),23,VIOLET)
        self.play(self.cam.incl.animate.set_value(.55),self.tau.animate.increment_value(.30*self.orb.t[-1]),run_time=3,rate_func=linear)
        self.marco('N01_vista_obliqua')
        self.play(self.cam.incl.animate.set_value(0),run_time=1.7)
        self.limpar()

    def n02(self):
        for h in self.historias: h.clear_updaters()
        self.play(*[FadeOut(h) for h in self.historias],run_time=.6); self.historias=[]
        self.titulo('Ele nunca parou de cair.')
        self.g=self.vetor_g(); self.add(self.g)
        gn=texto('gravidade',24,CYAN).set_z_index(100)
        def seguir_g(m):
            p=self.pos(); u=p-self.cam.p(self.earth_center()); u=u/max(np.linalg.norm(u),1e-8)
            m.move_to(p+.62*u+.18*np.array([-u[1],u[0],0]))
        gn.add_updater(seguir_g,call_updater=True)
        self.play(FadeIn(gn),self.tau.animate.increment_value(.22*self.orb.t[-1]),run_time=3,rate_func=linear)
        gn.clear_updaters(); self.play(FadeOut(gn),self.tau.animate.increment_value(.12*self.orb.t[-1]),run_time=1,rate_func=linear)
        self.play(self.tau.animate.increment_value(.36*self.orb.t[-1]),run_time=3.5,rate_func=linear)
        self.olhar(0,0,6.4,dur=1)
        self.marco('N02_gravidade_unica'); self.wait(3)

    def n03(self):
        self.titulo('O que muda quando retiramos a gravidade?')
        self.play(FadeOut(self.g),run_time=.5)
        self.loop=True
        instante_inicial=self.tau.get_value()
        r0,v0=self.estado(); dur=.19*self.orb.t[-1]
        tang=always_redraw(lambda:self.cam.linha(np.vstack([r0,r0+v0*dur])/R_T,VIOLET,2.4,ocultar=False,tracejado=True))
        fantasma=Dot(self.cam.si(r0),.085,color=VIOLET).set_z_index(40)
        p0=self.cam.si(r0); fora=p0-self.cam.p((0,0)); fora=fora/np.linalg.norm(fora)
        anel=Circle(radius=.2,color=WHITE,stroke_width=2).move_to(p0).set_z_index(41)
        partida=texto('mesmo ponto · mesma velocidade',21,WHITE).set_z_index(100)
        partida.add_background_rectangle(color=BACKGROUND_COLOR,opacity=.8,buff=.07)
        partida.move_to(p0-1.0*fora)
        self.add(tang,fantasma)
        self.play(Create(anel),FadeIn(partida),run_time=.7)
        ramo1=texto('sem gravidade',24,VIOLET).set_z_index(100)
        ramo1.add_updater(lambda m:m.move_to(fantasma.get_center()+.55*fora+[0,.1,0]),call_updater=True)
        self.escrever('sem gravidade → linha reta',(0,-2.6),27,VIOLET)
        self.play(FadeIn(ramo1),fantasma.animate.move_to(self.cam.si(r0+v0*dur)),run_time=3.5,rate_func=linear)
        self.wait(1); self.play(fantasma.animate.move_to(self.cam.si(r0)),FadeOut(ramo1),run_time=.7)
        ramo1.clear_updaters(); self.limpar()
        self.escrever('com gravidade → a direção da velocidade muda',(0,-2.6),27,CYAN)
        ramo2=texto('com gravidade',24,CYAN).set_z_index(100)
        def lado_interno(m):
            u=self.pos()-self.cam.p((0,0)); u=u/max(np.linalg.norm(u),1e-8)
            m.move_to(self.pos()+.75*u)
        ramo2.add_updater(lado_interno,call_updater=True)
        self.play(FadeIn(ramo2),self.tau.animate.set_value(instante_inicial+dur),fantasma.animate.move_to(self.cam.si(r0+v0*dur)),run_time=3.5,rate_func=linear)
        self.marco('N03_ramos_mesmo_instante'); self.wait(2)
        ramo2.clear_updaters()
        self.play(FadeOut(tang),FadeOut(fantasma),FadeOut(ramo2),FadeOut(anel),FadeOut(partida),run_time=.6); self.limpar()

    def n04(self):
        self.titulo('Como a velocidade gira')
        self.play(self.cam.ax.animate.set_value(-3.5),run_time=.8)
        self.olhar(0,0,8.5,dur=1.3)
        eq=self.math(r'\Delta\vec v\approx\vec a\,\Delta t',(3.6,-2.65),40)
        base=self.tau.get_value()
        o=np.array([3.6,.2,0]); L=1.7
        for i,f in enumerate((.03,.28,.55)):
            instante=base+f*self.orb.t[-1]
            self.play(self.tau.animate.set_value(instante),run_time=.8,rate_func=linear)
            r0,v0=self.estado()
            dt=.07*self.orb.t[-1]; r1,v1=self.orb.estado((instante+dt)%self.orb.t[-1])
            v0=v0/np.linalg.norm(v0); v1=v1/np.linalg.norm(v1)
            p0=self.cam.si(r0); p1=self.cam.si(r1)
            fora0=(p0-self.cam.p((0,0))); fora0=fora0/np.linalg.norm(fora0)
            fora1=(p1-self.cam.p((0,0))); fora1=fora1/np.linalg.norm(fora1)
            a=seta(p0,p0+np.r_[v0,0]*1.35); b=seta(p1,p1+np.r_[v1,0]*1.35,WHITE)
            esq=lambda d:np.array([-d[1],d[0],0]); dir_=lambda d:np.array([d[1],-d[0],0])
            l0=formula(r'\vec v(t)',30).move_to(a.get_end()+.3*np.r_[v0,0]+.5*esq(v0))
            l1=formula(r'\vec v(t+\Delta t)',30).move_to(b.get_end()+.3*np.r_[v1,0]+.75*dir_(v1))
            labs=VGroup(l0,l1)
            aa=seta(o,o+np.r_[v0,0]*L); bb=seta(o,o+np.r_[v1,0]*L,WHITE)
            dv=seta(aa.get_end(),bb.get_end(),CYAN,5)
            la=formula(r'\vec v(t)',30).move_to(aa.get_end()+.3*np.r_[v0,0]+.5*esq(v0))
            lb=formula(r'\vec v(t+\Delta t)',30).move_to(bb.get_end()+.3*np.r_[v1,0]+.75*dir_(v1))
            mid=(aa.get_end()+bb.get_end())/2; n=mid-o; n=n/np.linalg.norm(n)
            ldv=formula(r'\Delta\vec v',34).set_color(CYAN).move_to(mid+.6*n)
            ldv.set_z_index(100)
            anel=Circle(radius=.13,color=WHITE,stroke_width=2).move_to(o).set_z_index(70)
            origem=texto('mesma origem',21,WHITE).move_to(o+[0,-.38,0] if f>.1 and f<.4 else o+[0,.38,0]).set_z_index(100)
            self.play(Create(a),FadeIn(l0),run_time=.5)
            self.play(self.tau.animate.increment_value(dt),Create(b),FadeIn(l1),run_time=.9)
            self.play(TransformFromCopy(a,aa),TransformFromCopy(b,bb),FadeIn(la),FadeIn(lb),Create(anel),run_time=1.1)
            self.play(Create(dv),FadeIn(ldv),aa.animate.set_opacity(.45),bb.animate.set_opacity(.45),run_time=.7)
            if i==0: self.play(FadeIn(origem),run_time=.4)
            self.marco(f'N04_origem_comum_{i+1}'); self.wait(1.3)
            self.play(*[FadeOut(x) for x in (a,b,labs,aa,bb,dv,la,lb,ldv,anel)+((origem,) if i==0 else ())],run_time=.5)
        eq2=formula(r'd\vec v=\vec a\,dt',42).move_to(eq)
        lim=texto('para Δt cada vez menor',24,WHITE).move_to([3.6,-1.9,0]).set_z_index(100)
        self.overlays.append(lim)
        self.play(FadeIn(lim),TransformMatchingTex(eq,eq2),run_time=1.2)
        self.overlays.remove(eq); self.overlays.append(eq2)
        self.wait(2); self.limpar()

    def n07(self):
        self.titulo('Agora: órbita circular a 400 km')
        self.mostrar_montanha=False; self.configurar(R_T+400e3,1); self.loop=True; self.tracar=False
        caso=VGroup(texto('órbita circular · altitude',23,WHITE),medida('400','km',28)).arrange(RIGHT,buff=.12).move_to([0,2.15,0]).set_z_index(100)
        self.add(caso)
        self.olhar(0,0,6.5,dur=1.3)
        r=self.orb.r[0,1]; v=v_circular(r)
        seletor=Circle(radius=.18,color=VIOLET,stroke_width=2).move_to(self.pos()).set_z_index(60)
        self.play(Create(seletor)); self.marco('N07_trecho_na_orbita')
        aviso=VGroup(texto('aproximação local ·',23,WHITE),formula(r't=1\,\mathrm s',28)).arrange(RIGHT,buff=.12).move_to([0,2.16,0]).set_z_index(100)
        self.overlays.append(aviso); self.trocar(caso,aviso,junto=[FadeOut(seletor,run_time=.3)])
        a1=self.escrever('curvatura ampliada · escalas horizontal e vertical diferentes',(0,1.77),22,VIOLET)
        self.avisos7=[aviso,a1]
        # A mesma órbita recebe amostras densas no trecho de 1 segundo.
        T=self.orb.t[-1]
        ts=np.r_[np.arange(0,2,.02),np.arange(2,T-2,4),np.arange(T-2,T,.02),T]
        self.orb.r=np.column_stack([r*np.sin(v*ts/r),r*np.cos(v*ts/r)])
        self.orb.v=np.column_stack([v*np.cos(v*ts/r),-v*np.sin(v*ts/r)]); self.orb.t=ts
        self.olhar(v/(2*R_T),r/R_T-.00000035,.00185,dur=3.3)
        self.play(self.cam.stretch.animate.set_value(350),run_time=1.5)
        r0=self.orb.r[0].copy()
        tang=always_redraw(lambda:self.cam.linha(np.vstack([r0,r0+np.array([v*1.08,0])])/R_T,VIOLET,2,ocultar=False,tracejado=True))
        self.add(tang); self.local_tang=tang
        self.local_ghost=always_redraw(lambda:Dot(self.cam.si(r0+np.array([v*self.tau.get_value(),0])),.07,color=VIOLET).set_z_index(36))
        self.add(self.local_ghost)
        trot=texto('tempo físico',22,MAGENTA).move_to([-5.9,1.95,0]).set_z_index(100)
        self.add(trot); self.overlays.append(trot)
        relogio=DecimalNumber(0,num_decimal_places=2,unit=r'\,\mathrm s',font_size=40,color=MAGENTA).move_to([-5.9,1.45,0]).set_z_index(100)
        relogio.add_updater(lambda m:valor_tempo(m,self.tau.get_value()))
        self.add(relogio); self.overlays.append(relogio)
        self.play(self.tau.animate.set_value(1),run_time=5,rate_func=linear)
        a=self.cam.si(r0); b=self.cam.si(r0+np.array([v,0])); c=self.pos()
        dh=DoubleArrow(a+.28*UP,b+.28*UP,buff=0,color=VIOLET,tip_length=.1,stroke_width=2).set_z_index(60)
        dg=DoubleArrow(b,c,buff=0,color=VIOLET,tip_length=.1,stroke_width=3).set_z_index(60)
        self.add(dh,dg); self.overlays.extend([dh,dg])
        distancia=VGroup(medida('7{,}67','km',32),texto('na tangente',25,WHITE)).arrange(RIGHT,buff=.12).move_to([0,1.18,0]).set_z_index(100)
        self.overlays.append(distancia); self.play(FadeIn(distancia),run_time=.65)
        self.escrever('queda',(5.4,.16),24,CYAN)
        vertical=medida('4{,}35','m',30).move_to([5.4,-.32,0])
        self.overlays.append(vertical); self.play(FadeIn(vertical),run_time=.75)
        self.marco('N07_medidas_antes_das_contas')
        self.wait(1.3)
        qnome=self.escrever('queda',(-3.4,-1.55),25,CYAN)
        queda=self.math(r'\frac12gt^2\approx4{,}35\,\mathrm m',(-3.4,-2.2),37)
        self.wait(1.3)
        cnome=self.escrever('curvatura da órbita',(3.2,-1.55),25,VIOLET)
        curvatura=self.math(r'\frac{s^2}{2r}\approx4{,}35\,\mathrm m',(3.2,-2.2),37)
        self.marco('N07_queda_e_curvatura')
        self.wait(1.5)
        for x in (qnome,queda,cnome,curvatura): self.overlays.remove(x)
        self.play(*[FadeOut(x) for x in (qnome,queda,cnome,curvatura)],run_time=.5)
        self.math(r'\frac12gt^2\approx\frac{s^2}{2r}',(0,-2.25),43)
        self.marco('N07_um_segundo_ampliado'); self.wait(4)

    def n08(self):
        self.titulo('Ele cai — e a Terra curva para longe.')
        # 1) sai tudo o que depende da escala vertical; os avisos ficam enquanto houver distorção.
        dependentes=[m for m in self.overlays if m not in self.avisos7]
        for m in dependentes: m.clear_updaters(recursive=True)
        self.play(*[FadeOut(m) for m in dependentes],FadeOut(self.local_ghost),FadeOut(self.local_tang),run_time=.7)
        for m in dependentes: self.overlays.remove(m)
        # 2) desfaz a distorção só com o corpo e a curva
        self.play(self.cam.stretch.animate.set_value(1),run_time=1.5)
        self.limpar(); self.olhar(0,0,6.5,dur=3)
        self.play(self.tau.animate.set_value(.65*self.orb.t[-1]),run_time=5,rate_func=linear)
        self.marco('N08_detalhe_reintegrado'); self.wait(1.5)

    def n09(self):
        self.titulo('Dentro da estação: tudo cai junto')
        rp=self.estado()[0]/R_T
        self.escrever('vista local que acompanha a estação · tamanhos ampliados',(0,-2.7),22,MUTED)
        self.olhar(rp[0],rp[1],.09,roll=math.atan2(rp[0],rp[1]),dur=2.6)
        self.mostrar_bola=False; self.path_alpha.set_value(0)
        nave=satelite([0,-.2,0],.5); self.add(nave)
        self.play(nave.animate.scale(5),run_time=2)
        cabine=VGroup(RoundedRectangle(width=7.3,height=3.5,corner_radius=.23,stroke_color=LIGHT,stroke_width=3,fill_color='#10233C',fill_opacity=.95),
            Line([-3.4,-1.55,0],[3.4,-1.55,0],color='#395575',stroke_width=2)).shift(.1*DOWN).set_z_index(50)
        pessoa=astronauta([-.9,.15,0],1.25).set_z_index(60)
        objeto=VGroup(Circle(radius=.16,color=WHITE,fill_color=WHITE,fill_opacity=1),Line([-.1,0,0],[.1,0,0],color=BLUE)).move_to([1.55,.3,0]).set_z_index(60)
        self.play(FadeIn(cabine),FadeIn(pessoa),FadeIn(objeto),nave.animate.set_opacity(.22),run_time=1.5)
        self.play(pessoa.animate.shift(.35*RIGHT+.12*UP),objeto.animate.shift(.5*LEFT+.10*DOWN),run_time=5,rate_func=linear)
        # aceleração g: uma seta em cada corpo e uma na própria estação (casco), cada uma ancorada no corpo
        base_est=np.array([2.85,-.45,0])
        gs=VGroup(seta(pessoa.get_center(),pessoa.get_center()+.8*DOWN,CYAN),seta(objeto.get_center(),objeto.get_center()+.8*DOWN,CYAN),
                  seta(base_est,base_est+.8*DOWN,CYAN)).set_z_index(80)
        gl=VGroup(*[formula('g',30).next_to(a,RIGHT,buff=.08) for a in gs]).set_z_index(100)
        est=texto('estação',21,WHITE).move_to([2.85,-.1,0]).set_z_index(100)
        self.play(Create(gs),FadeIn(gl),FadeIn(est)); q=self.escrever('Queda livre conjunta: todos aceleram igual',(0,2.18),27,CYAN)
        self.marco('N09_interior_queda_conjunta'); self.wait(2)
        self.play(FadeOut(gs),FadeOut(gl),FadeOut(est),FadeOut(cabine),FadeOut(nave),FadeOut(objeto),FadeOut(q),pessoa.animate.scale(.7).move_to([-2.8,-.45,0]),run_time=1.5)
        self.overlays.remove(q)
        apoio=astronauta([3,-.45,0],.875).set_z_index(60)
        y=apoio.get_bottom()[1]
        chao=Line([1.8,y,0],[4.2,y,0],color=LIGHT).set_z_index(60)
        c1=pessoa.get_center(); c2=apoio.get_center()
        fg1=seta(c1,c1+.9*DOWN,CYAN); fg2=seta(c2,c2+.9*DOWN,CYAN)
        normal=seta(c2,c2+.9*UP,WHITE)
        l1=formula('F_g',29).next_to(fg1,RIGHT,buff=.12); l2=formula('F_g',29).next_to(fg2,RIGHT,buff=.12)
        nlabel=formula('N',29).next_to(normal,RIGHT,buff=.15)
        self.escrever('forças sobre o corpo',(0,2.18),26,WHITE)
        self.play(FadeIn(apoio),Create(chao),Create(fg1),Create(fg2),Create(normal),FadeIn(l1),FadeIn(l2),FadeIn(nlabel))
        self.escrever('sem apoio: só a gravidade',(-2.8,-1.85),24,CYAN); self.escrever('com apoio: gravidade e normal',(3,-1.85),24,WHITE)
        self.math(r'\frac{g_{\mathrm{orbita}}}{g_{\mathrm{superficie}}}=\left(\frac{R_T}{R_T+h}\right)^2\approx0{,}89',(0,1.35),34)
        self.marco('N09_apoio_e_gravidade'); self.wait(3)
        self.play(*[FadeOut(x) for x in (pessoa,apoio,chao,normal,nlabel,fg1,fg2,l1,l2)],run_time=.7)
        self.limpar(); self.mostrar_bola=True; self.path_alpha.set_value(1)
        self.olhar(0,0,7.4,dur=2.4)

    def n10(self):
        self.titulo('Duas órbitas circulares. O mesmo relógio.')
        self.configurar(R_T+400e3,1); self.loop=True; self.tracar=False
        self.play(self.cam.ax.animate.set_value(-3.9),run_time=.8)
        self.olhar(0,0,10.2,dur=1.5)
        alto=lancamento(1.8*R_T,1); clock=ValueTracker(0)
        P=self.cam.p; rb=(R_T+400e3)/R_T
        ang=lambda g,r:P((r*math.sin(math.radians(g)),r*math.cos(math.radians(g))))
        caminho=always_redraw(lambda:self.cam.linha(alto.r[::5]/R_T,LIGHT,2,ocultar=False))
        posalto=lambda:self.cam.si(alto.estado(clock.get_value()%alto.t[-1])[0])
        corpo=always_redraw(lambda:Circle(radius=.085,color=WHITE,stroke_width=2).move_to(posalto()).set_z_index(35))
        va=always_redraw(lambda:seta(posalto(),posalto()+np.r_[alto.estado(clock.get_value()%alto.t[-1])[1]/v_circular(R_T+400e3),0]*1.1))
        vb=self.vetor_v(1.1)
        cota_baixa=always_redraw(lambda:Line(P((0,0)),self.pos(),color=VIOLET,stroke_width=1.3).set_z_index(23))
        cota_alta=always_redraw(lambda:Line(P((0,0)),posalto(),color=VIOLET,stroke_width=1.3).set_z_index(23))
        trot=texto('tempo físico',23,MAGENTA).move_to([3.8,1.95,0]).set_z_index(100)
        relogio=DecimalNumber(0,num_decimal_places=0,group_with_commas=False,unit=r'\,\mathrm s',font_size=42,color=MAGENTA).move_to([3.8,1.4,0]).set_z_index(100)
        relogio.add_updater(lambda m:valor_tempo(m,clock.get_value()))
        self.add(caminho,corpo,va,vb,cota_baixa,cota_alta,relogio,trot)
        self.overlays.extend([relogio,trot])
        indep=self.escrever('casos independentes · tempo comum',(3.8,.7),21,MUTED)
        # chamadas terminam no arco certo, fora dos símbolos
        a_alto=ang(38,1.8); a_baixo=ang(128,rb)
        alta=texto('órbita alta',24,VIOLET).move_to(a_alto+[1.15,.5,0]).set_z_index(100)
        baixa=texto('órbita baixa',24,VIOLET).move_to([-.65,-1.75,0]).set_z_index(100)
        la=Line(a_alto,alta.get_left()+[-.06,0,0],color=VIOLET,stroke_width=1.4).set_z_index(100)
        lb=Line(a_baixo,baixa.get_left()+[-.06,0,0],color=VIOLET,stroke_width=1.4).set_z_index(100)
        for m in (alta,baixa,la,lb): self.add(m); self.overlays.append(m)
        self.play(clock.animate.set_value(alto.t[-1]),self.tau.animate.set_value(alto.t[-1]),run_time=11,rate_func=linear)
        relogio.clear_updaters()
        self.math(r'v_{\mathrm{orb}}=\sqrt{\frac{GM}{r}}',(3.8,-.35),44)
        self.nota_equacao('Mais longe, menor velocidade:\na volta demora mais.',xy=(3.8,-1.65))
        self.marco('N10_mesmo_tempo'); self.wait(2.5)
        self.play(*[FadeOut(x) for x in (caminho,corpo,va,vb,cota_baixa,cota_alta)],self.cam.ax.animate.set_value(0),run_time=.8); self.limpar(); self.nota_atual=None

    def n13(self):
        self.titulo('Ajustar a velocidade. Depois, lançar.')
        self.mostrar_bola=True; self.mostrar_montanha=False
        PX=4.5; X0,X1=2.5,6.5
        nomes=lambda z,info:('impacto · ligada' if info['colide'] else 'aberta' if not info['ligada']
                             else 'circular' if abs(z-1)<.012 else 'elipse externa · ligada' if z>1 else 'elipse ligada')
        for j,f in enumerate((.70,.92,1.,1.2,1.44)):
            self.janela_n13=(-7.2,1.3,-2.85,2.55)
            if j:
                rein=self.escrever('Reinício · mesmo ponto de lançamento',(PX,2.1),22,VIOLET)
                self.wait(.5); self.limpar()
            dur=periodo(1.5*R_T)/max(.06,(2-f*f))**1.5 if f<math.sqrt(2) else periodo(1.5*R_T)
            self.configurar(1.5*R_T,f,dur); self.prever=True
            self.fator.set_value((.55,.70,.92,1.,1.2)[j])
            self.cam.janela=self.janela_n13
            self.play(self.cam.ax.animate.set_value(-3.2),run_time=.8)
            self.olhar(0,.3,7.4,dur=1.2)
            av=always_redraw(lambda:seta(self.pos(),self.pos()+1.1*self.fator.get_value()*RIGHT))
            def info_z(): z=self.fator.get_value(); return z,conica(1.5*R_T,z,amostras=2)[1]
            def painel_nome():
                z,i=info_z(); return texto_cache(nomes(z,i),30,WHITE).move_to([PX,1.5,0]).set_z_index(100)
            def painel_valor():
                z,_=info_z(); return texto_cache('v₀ = %s v_circ'%('%.2f'%z).replace('.',','),24,WHITE).move_to([PX,.75,0]).set_z_index(100)
            nome=always_redraw(painel_nome); valor=always_redraw(painel_valor)
            trilho=Line([X0,0,0],[X1,0,0],color=VIOLET,stroke_width=3).set_z_index(100)
            marcas=VGroup(*[Line([X0+(X1-X0)*(z-.5),-.12,0],[X0+(X1-X0)*(z-.5),.12,0],color=WHITE,stroke_width=1.5) for z in (.70,.92,1.,1.2,1.44)]).set_z_index(100)
            titulo_ctrl=texto('velocidade inicial',22,MUTED).move_to([PX,2.05-.0,0]).set_z_index(100)
            manopla=always_redraw(lambda:VGroup(Dot([X0+(X1-X0)*(self.fator.get_value()-.5),0,0],.2,color=WHITE).set_opacity(.18),
                                                Dot([X0+(X1-X0)*(self.fator.get_value()-.5),0,0],.09,color=WHITE)).set_z_index(101))
            ctrl=VGroup(trilho,marcas)
            ctrl.shift(UP*.0)
            nota=VGroup(texto('mesmo ponto de lançamento',22,WHITE),
                        VGroup(formula(r'r_0=1{,}5R_T',29),texto('· direção tangencial',22,WHITE)).arrange(RIGHT,buff=.12)
                        ).arrange(DOWN,buff=.14).move_to([PX,-1.0,0]).set_z_index(100)
            self.add(av,nome,valor,ctrl,manopla); self.overlays.extend([titulo_ctrl,nota])
            self.play(FadeIn(titulo_ctrl),FadeIn(nota),run_time=.6)
            self.play(self.fator.animate.set_value(f),run_time=1.5,rate_func=linear)
            info=conica(1.5*R_T,f)[1]
            self.marco(f'N13_ajuste_{j+1}'); self.wait(.9)
            for m in (nome,valor,manopla,av): m.clear_updaters()
            self.play(*[FadeOut(m) for m in (av,valor,ctrl,manopla,nome)],run_time=.35); self.limpar(); self.prever=False
            self.remove(valor,manopla,av,ctrl)
            self.cam.janela=None
            self.play(self.cam.ax.animate.set_value(0),run_time=.7)
            self.remove(nome)
            esc=self.escrever(nomes(f,info),(4.6,2.0),28,WHITE)
            if f<math.sqrt(2):
                semieixo=1.5/(2-f*f)
                centro=np.array([0,-semieixo*(f*f-1)])
                span=max(7.4,5.6*semieixo)
            else:
                ids=np.flatnonzero(np.linalg.norm(self.orb.r,axis=1)>=6*R_T)
                fim=self.orb.r[ids[0] if len(ids) else -1]/R_T
                centro=(np.array([0,1.5])+fim)/2
                span=18
            self.voo(5.2,span,True,centro)
            self.marco(f'N13_voo_{j+1}'); self.wait(1.1); self.limpar()
        self.cam.janela=None

    def n14(self):
        self.titulo('Retomando o caso de impacto')
        self.escrever('reinício do lançamento ligado que colide',(-3.6,2.2),23,VIOLET)
        self.configurar(1.5*R_T,.70); self.olhar(0,.3,7.4,dur=1.3)
        self.voo(4.5,7.4,False)
        self.play(Flash(self.pos(),color=WHITE,line_length=.14,flash_radius=.3),run_time=.5)
        self.marco('N14_impacto_fisico')
        impacto=self.estado()[0]/R_T
        self.olhar(impacto[0],impacto[1],.9,dur=1.8); self.wait(1.5)
        self.olhar(0,.2,8.4,dur=1.8); self.limpar()
        ps=conica(1.5*R_T,.70,fisica=False)[0]/R_T
        ang=np.linspace(0,2*np.pi,len(ps)); hit=math.atan2(impacto[0],impacto[1])
        resto=ps[ang>=hit]
        matematica=always_redraw(lambda:self.cam.linha(resto,VIOLET,2.5,ocultar=False,tracejado=True))
        self.play(self.earth_alpha.animate.set_value(.4),run_time=.8); self.add(matematica)
        amostra_fis=Line(ORIGIN,[.7,0,0],color=BLUE,stroke_width=4)
        amostra_mat=DashedLine(ORIGIN,[.7,0,0],color=VIOLET,stroke_width=4,dash_length=.12)
        leg=VGroup(VGroup(amostra_fis,texto('trajetória física',26,BLUE)).arrange(RIGHT,buff=.18),
                   VGroup(amostra_mat,texto('continuação matemática',26,VIOLET)).arrange(RIGHT,buff=.18)).arrange(RIGHT,buff=.9).move_to([0,-2.65,0]).set_z_index(100)
        self.overlays.append(leg); self.play(FadeIn(leg),run_time=.6)
        self.escrever('Ligada matematicamente. Com colisão.',(0,2.38),25,WHITE)
        self.marco('N14_continuacao_tracejada'); self.wait(4)
        self.play(FadeOut(matematica),run_time=.6); self.limpar()

    def n15(self):
        self.titulo('Experimento mental de Newton')
        self.path_alpha.set_value(0); self.earth_alpha.set_value(1)
        self.mostrar_montanha=True; self.mostrar_bola=False
        # reencontra o aparato, abre as quatro curvas a partir da boca e só então mostra o conjunto
        self.olhar(0,1.035,.30,dur=2.2); self.wait(.8)
        caminhos=[]
        for f in (.55,.80,.985,1.):
            ps=lancamento(1.06*R_T,f).r[::4]/R_T
            m=always_redraw(lambda pts=ps:self.cam.linha(pts,BLUE,2.2))
            caminhos.append(m); self.add(m); self.wait(.4)
        self.olhar(0,0,6.7,dur=3.4)
        self.marco('N15_diagrama_canhao'); self.wait(2.5)
        self.play(*[FadeOut(x) for x in caminhos],self.earth_alpha.animate.set_value(1),run_time=.8)

    def n18(self):
        self.titulo('De volta à montanha')
        self.play(self.cam.ax.animate.set_value(0),run_time=.5)
        self.configurar(1.06*R_T,1); self.mostrar_montanha=True; self.path_alpha.set_value(1)
        self.olhar(0,0,7.4,incl=0,dur=1.2)
        self.olhar(0,1.035,.30,dur=2.6)
        self.marco('N18_reencontro_montanha'); self.wait(1.5)
        self.titulo('Orbitar não é vencer a gravidade.')
        self.wait(.8)
        self.voo(8,6.4,True); self.loop=True; self.tracar=False
        self.titulo('É cair… e continuar errando o chão.',junto=[self.tau.animate.increment_value(.04*self.orb.t[-1])])
        self.play(self.tau.animate.increment_value(.25*self.orb.t[-1]),run_time=4,rate_func=linear)
        self.marco('N18_fechamento'); self.wait(3)
        self.play(FadeOut(self.cabecalho),FadeOut(self.tag),run_time=1.3)
        self.play(self.tau.animate.increment_value(.18*self.orb.t[-1]),run_time=3,rate_func=linear)

