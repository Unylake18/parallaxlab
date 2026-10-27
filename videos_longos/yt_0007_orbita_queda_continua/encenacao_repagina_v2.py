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

PASTA=Path(__file__).resolve().parent
CYAN='#35D9FF'; AMBER='#FFC24D'; MUTED='#A9BBD8'


def seta(*args,**kwargs):
    return seta_base(*args,**kwargs).set_z_index(45)


@lru_cache(maxsize=1)
def alfabeto_semantico():
    resultado=[]
    for letra,cor in [('M',LIGHT),('R',LIGHT),('r',VIOLET),('a',VIOLET),('s',VIOLET),('T',AMBER),('t',AMBER),('g',CYAN)]:
        ref=MathTex(letra,font_size=43)[0][0]
        pts=ref.get_points(); normal=(pts-ref.get_center())/max(ref.height,1e-8)
        resultado.append((letra,cor,normal))
    return resultado


def formula(tex,size=43,maxw=12):
    m=MathTex(tex,font_size=size,color=WHITE)
    for g in m.family_members_with_points():
        if not len(g.get_points()): continue
        normal=(g.get_points()-g.get_center())/max(g.height,1e-8)
        for letra,cor,ref in alfabeto_semantico():
            if normal.shape==ref.shape and np.allclose(normal,ref,atol=.002):
                if letra=='a' and r'\vec a' in tex: cor=CYAN
                if letra=='T' and 'R_T' in tex and g.height < .3: cor=LIGHT
                g.set_color(cor); break
    if m.width>maxw: m.scale_to_fit_width(maxw)
    return m.set_z_index(100)


class OrbitaRepaginada(Scene):
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
        self.earth_alpha=ValueTracker(1); self.path_alpha=ValueTracker(1)
        self.earth_center=lambda: np.array([0.,0.])
        self.custom_pos=None; self.overlays=[]; self.tempos=[]; self.marcos=[]
        self.historias=[]; self.extra=[]; self.cabecalho=None
        self.wm=ImageMobject(str(WATERMARK_PATH)).set_width(1.92).set_opacity(.45).to_corner(UR,buff=.30).set_z_index(200)
        self.tag=texto('GRAVITAÇÃO — ÓRBITAS',18).set_opacity(.6).to_corner(UL,buff=.38).set_z_index(200)
        self.terra=Group()
        def atualizar_terra(m):
            m.remove(*m.submobjects)
            m.add(self.cam.planeta(self.earth_center(),self.earth_alpha.get_value()))
        self.terra.add_updater(atualizar_terra,call_updater=True)
        self.relevo=always_redraw(lambda:self.cam.montanha() if self.mostrar_montanha else VGroup())
        self.trilha=always_redraw(self.desenhar_trilha)
        self.pedra=always_redraw(self.desenhar_bola)
        self.add(self.terra,self.relevo,self.trilha,self.pedra,self.wm,self.tag)
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
        nome='timing_repagina' + ('_'+ '_'.join(map(str,sorted(selecionados))) if selecionados else '')
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
            out=PASTA/'qa_repagina_estatico'; out.mkdir(exist_ok=True)
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
        m=VGroup(Dot(self.cam.p(p),r,color='#C4D2DF'),
                 Dot(self.cam.p(p)+r*np.array([-.24,.24,0]),r*.55,color=WHITE)).set_z_index(35)
        return m.set_opacity(1 if vis else 0)

    def desenhar_trilha(self):
        if self.custom_pos: return VGroup()
        if self.prever:
            pts=conica(np.linalg.norm(self.orb.r[0]),self.fator.get_value(),alcance=6*R_T)[0]
            return self.cam.linha(pts/R_T,BLUE,2,ocultar=True).set_stroke(opacity=.45)
        if self.tracar and not self.loop:
            t=self.tau.get_value(); i=np.searchsorted(self.orb.t,t)
            pts=np.vstack([self.orb.r[:max(i,1):4],self.orb.estado(t)[0]])
        else: pts=np.vstack([self.orb.r[::4],self.orb.r[-1]])
        return self.cam.linha(pts/R_T,BLUE,2.5,ocultar=True).set_stroke(opacity=self.path_alpha.get_value())

    def titulo(self,s):
        novo=texto(s,34,largura=13.6).move_to([0,2.9,0]).set_z_index(100)
        if self.cabecalho: self.play(FadeOut(self.cabecalho),FadeIn(novo),run_time=.65)
        else: self.play(FadeIn(novo),run_time=.65)
        self.cabecalho=novo

    def escrever(self,s,xy=(0,-2.55),size=27,color=WHITE):
        m=texto(s,size,color,largura=13.7).move_to([*xy,0]).set_z_index(100)
        self.overlays.append(m); self.play(FadeIn(m),run_time=.65); return m

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
        self.wait(2); self.marco('N01_canhao_proximo')
        for j,(f,span) in enumerate(zip((.55,.80,.985,1.),(.75,1.5,6.4,6.4))):
            if j:
                self.escrever('Nova tentativa · mesmo ponto de lançamento',(0,2.25),23,VIOLET)
                self.olhar(0,1.035,.30,dur=1.5); self.configurar(1.06*R_T,f)
                self.limpar(); self.escrever('montanha idealizada · sem atmosfera',(0,-2.6),23,MUTED)
            else: self.configurar(1.06*R_T,f)
            av=self.vetor_v(.7+.2*j); self.add(av)
            self.wait(.7); self.play(FadeOut(av),run_time=.35)
            self.voo(5 if j<2 else 7,span)
            if self.orb.impacto:
                self.play(Flash(self.pos(),color=LIGHT,line_length=.09,flash_radius=.16),run_time=.5)
                pts=self.orb.r.copy()/R_T
                hist=always_redraw(lambda ps=pts:self.cam.linha(ps[::4],BLUE,1.5).set_stroke(opacity=.25))
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
        self.play(self.tau.animate.increment_value(.70*self.orb.t[-1]),run_time=7,rate_func=linear)
        self.olhar(0,0,6.4,dur=1)
        self.marco('N02_gravidade_unica'); self.wait(3)

    def n03(self):
        self.titulo('O que muda quando retiramos a gravidade?')
        self.play(FadeOut(self.g),run_time=.5)
        self.loop=True
        instante_inicial=self.tau.get_value()
        r0,v0=self.estado(); dur=.19*self.orb.t[-1]
        tang=always_redraw(lambda:self.cam.linha(np.vstack([r0,r0+v0*dur])/R_T,VIOLET,2,ocultar=False,tracejado=True))
        fantasma=Dot(self.cam.si(r0),.085,color=VIOLET).set_z_index(40)
        self.add(tang,fantasma)
        self.escrever('sem gravidade → linha reta',(0,-2.6),27,VIOLET)
        self.play(fantasma.animate.move_to(self.cam.si(r0+v0*dur)),run_time=3.5,rate_func=linear)
        self.wait(1); self.play(fantasma.animate.move_to(self.cam.si(r0)),run_time=.7)
        self.limpar(); self.escrever('com gravidade → a direção da velocidade muda',(0,-2.6),27,CYAN)
        self.play(self.tau.animate.set_value(instante_inicial+dur),fantasma.animate.move_to(self.cam.si(r0+v0*dur)),run_time=3.5,rate_func=linear)
        self.marco('N03_ramos_mesmo_instante'); self.wait(2)
        self.play(FadeOut(tang),FadeOut(fantasma),run_time=.6); self.limpar()

    def n04(self):
        self.titulo('Como a velocidade gira')
        self.play(self.cam.ax.animate.set_value(-3.1),run_time=.8)
        self.olhar(0,0,8.5,dur=1.3)
        eq=self.math(r'\Delta\vec v\approx\vec a\,\Delta t',(3.2,-1.95),40)
        base=self.tau.get_value()
        for i,f in enumerate((.03,.28,.55)):
            instante=base+f*self.orb.t[-1]
            self.play(self.tau.animate.set_value(instante),run_time=.8,rate_func=linear)
            r0,v0=self.estado()
            dt=.04*self.orb.t[-1]; r1,v1=self.orb.estado((instante+dt)%self.orb.t[-1])
            v0=v0/np.linalg.norm(v0); v1=v1/np.linalg.norm(v1)
            p0=self.cam.si(r0); p1=self.cam.si(r1)
            a=seta(p0,p0+np.r_[v0,0]*1.25); b=seta(p1,p1+np.r_[v1,0]*1.25,LIGHT)
            labs=VGroup(formula(r'\vec v(t)',28).next_to(a,UP,buff=.1),formula(r'\vec v(t+\Delta t)',28).next_to(b,DOWN,buff=.1))
            o=np.array([3.2,.25,0]); aa=seta(o,o+np.r_[v0,0]*1.7); bb=seta(o,o+np.r_[v1,0]*1.7,LIGHT)
            dv=seta(aa.get_end(),bb.get_end(),CYAN)
            self.play(Create(a),run_time=.5)
            self.play(self.tau.animate.increment_value(dt),Create(b),FadeIn(labs),run_time=.9)
            self.play(TransformFromCopy(a,aa),TransformFromCopy(b,bb),run_time=1.1)
            self.play(Create(dv),run_time=.5); self.marco(f'N04_origem_comum_{i+1}'); self.wait(1.5)
            self.play(*[FadeOut(x) for x in (a,b,labs,aa,bb,dv)],run_time=.5)
        self.math(r'd\vec v=\vec a\,dt',(3.2,.35),42); self.wait(2); self.limpar()

    def n05(self):
        self.titulo('Uma aceleração, duas descrições')
        self.play(self.cam.ax.animate.set_value(0),run_time=.8)
        self.olhar(0,0,6.8,dur=1)
        self.g=self.vetor_g(1.0); self.v=self.vetor_v(1.2)
        self.add(self.g,self.v)
        self.raio=always_redraw(lambda:DashedLine(self.cam.p((0,0)),self.pos(),color=VIOLET,dash_length=.09,stroke_width=2).set_z_index(24))
        self.add(self.raio)
        rlabel=formula('r',30); mlabel=formula('M',27)
        rlabel.add_updater(lambda m:m.move_to((self.cam.p((0,0))+self.pos())/2+.15*RIGHT))
        mlabel.add_updater(lambda m:m.move_to(self.cam.p((0,0))+.2*DOWN))
        self.grandezas=VGroup(rlabel,mlabel); self.add(self.grandezas)
        self.earth_alpha.set_value(.45)
        self.escrever('gravidade',(0,1.8),25,CYAN)
        e=self.math(r'g=\frac{GM}{r^2}',(-3.5,-2.45),45)
        self.escrever('geometria do círculo',(0,-1.9),24,VIOLET)
        self.math(r'a_c=\frac{v^2}{r}',(3.5,-2.45),45)
        self.marco('N05_raio_e_vetores'); self.wait(3)

    def n06(self):
        self.limpar(); self.titulo('A condição para a órbita circular')
        # Mesmos corpo, raio e vetores de N05; muda a distribuição em tela.
        self.play(self.cam.ax.animate.set_value(-3.3),self.cam.span.animate.set_value(8.2),run_time=1.3)
        self.escrever('A gravidade fornece a aceleração centrípeta.',(0,-2.6),25,CYAN)
        e1=formula(r'\frac{GM}{r^2}=\frac{v^2}{r}',49,6.5).move_to([3.25,.6,0])
        fatores=formula(r'\frac{GM}{r\,r}=\frac{v^2}{r}',49,6.5).move_to(e1)
        e2=formula(r'\frac{GM}{r}=v^2',49,6.5).move_to(e1)
        e3=formula(r'v^2=\frac{GM}{r}',49,6.5).move_to(e1)
        e4=formula(r'v_{\mathrm{orb}}=\sqrt{\frac{GM}{r}}',52,6.5).move_to(e1)
        self.play(FadeIn(e1),run_time=.8); self.wait(2)
        self.play(TransformMatchingTex(e1,fatores),run_time=1.2)
        e1=fatores
        op=texto('× r  (r > 0)',25,VIOLET).move_to([3.25,-.8,0]); self.play(FadeIn(op))
        # Índices estabilizados e verificados no QA de desenvolvimento.
        if len(e1[0])==10 and len(e2[0])==7:
            for idx in (3,9): e1[0][idx].set_color(VIOLET)
            riscos=VGroup(*[Line(e1[0][i].get_corner(DL),e1[0][i].get_corner(UR),color=VIOLET,stroke_width=2) for i in (4,9)])
            self.play(Create(riscos),run_time=.7)
            self.play(TransformByGlyphMap(e1,e2,([0,1,2,3,5,6,7],[0,1,2,3,4,5,6]),([4,8,9],[])),FadeOut(riscos),FadeOut(op),run_time=1.8)
        else:
            self.play(TransformMatchingTex(e1,e2),FadeOut(op),run_time=1.8)
        self.remove(e1); self.add(e2)
        self.wait(1)
        self.play(TransformMatchingTex(e2,e3),run_time=1.3)
        self.play(TransformMatchingTex(e3,e4),run_time=1.8)
        self.overlays.append(e4); self.marco('N06_raiz_e_raio'); self.wait(3)
        self.limpar(); self.play(FadeOut(self.g),FadeOut(self.v),FadeOut(self.raio),FadeOut(self.grandezas),self.earth_alpha.animate.set_value(1),run_time=.8)
        self.play(self.cam.ax.animate.set_value(0),run_time=.8)

    def n07(self):
        self.titulo('Agora: órbita circular a 400 km')
        self.mostrar_montanha=False; self.configurar(R_T+400e3,1); self.loop=True; self.tracar=False
        self.olhar(0,0,6.5,dur=1.3)
        r=self.orb.r[0,1]; v=v_circular(r)
        seletor=Circle(radius=.18,color=VIOLET,stroke_width=2).move_to(self.pos()).set_z_index(60)
        self.play(Create(seletor)); self.marco('N07_trecho_na_orbita')
        self.escrever('aproximação local · t = 1 s',(0,2.16),23,AMBER)
        self.escrever('curvatura ampliada para visualização',(0,1.77),23,VIOLET)
        self.escrever('escalas horizontal e vertical diferentes',(0,-2.89),17,MUTED)
        self.play(FadeOut(seletor),run_time=.3)
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
        relogio=DecimalNumber(0,num_decimal_places=2,unit=r'\,\mathrm s',font_size=32,color=AMBER).move_to([-5.8,1.25,0]).set_z_index(100)
        relogio.add_updater(lambda m:m.set_value(self.tau.get_value()))
        self.add(relogio); self.overlays.append(relogio)
        self.play(self.tau.animate.set_value(1),run_time=5,rate_func=linear)
        a=self.cam.si(r0); b=self.cam.si(r0+np.array([v,0])); c=self.pos()
        dh=DoubleArrow(a+.28*UP,b+.28*UP,buff=0,color=VIOLET,tip_length=.1,stroke_width=2).set_z_index(60)
        dg=DoubleArrow(b,c,buff=0,color=CYAN,tip_length=.1,stroke_width=3).set_z_index(60)
        self.add(dh,dg); self.overlays.extend([dh,dg])
        self.escrever('7,67 km na tangente',(0,1.18),25,WHITE)
        self.escrever('4,35 m',(5.5,-.1),27,CYAN)
        queda=self.math(r'\frac12gt^2\approx4{,}35\,\mathrm m',(-3.4,-1.47),34)
        curvatura=self.math(r'\frac{s^2}{2r}\approx4{,}35\,\mathrm m',(3.3,-1.47),34)
        self.play(Indicate(VGroup(queda,curvatura),color=CYAN,scale_factor=1.04),run_time=1)
        self.math(r'\frac12gt^2=\frac12\left(\frac{v^2}{r}\right)t^2\approx\frac{s^2}{2r}',(0,-2.28),33)
        self.marco('N07_um_segundo_ampliado'); self.wait(4)

    def n08(self):
        self.titulo('Ele cai — e a Terra curva para longe.')
        # Devolve o mesmo detalhe à mesma circunferência; a distorção termina
        # antes de retirar seus avisos.
        self.play(FadeOut(self.local_ghost),FadeOut(self.local_tang),run_time=.6)
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
        objeto=VGroup(Circle(radius=.16,color=WHITE,fill_color=AMBER,fill_opacity=1),Line([-.1,0,0],[.1,0,0],color=WHITE)).move_to([1.55,.3,0]).set_z_index(60)
        self.play(FadeIn(cabine),FadeIn(pessoa),FadeIn(objeto),nave.animate.set_opacity(.22),run_time=1.5)
        self.play(pessoa.animate.shift(.35*RIGHT+.12*UP),objeto.animate.shift(.5*LEFT+.10*DOWN),run_time=5,rate_func=linear)
        gs=VGroup(seta(pessoa.get_center(),pessoa.get_center()+.8*DOWN,CYAN),seta(objeto.get_center(),objeto.get_center()+.8*DOWN,CYAN),seta([3.1,.7,0],[3.1,-.1,0],CYAN)).set_z_index(80)
        self.play(Create(gs)); self.escrever('Queda livre conjunta',(0,2.18),29,CYAN)
        self.marco('N09_interior_queda_conjunta'); self.wait(2)
        self.play(FadeOut(gs),FadeOut(cabine),FadeOut(nave),FadeOut(objeto),pessoa.animate.scale(.7).move_to([-2.8,-.45,0]),run_time=1.5)
        apoio=astronauta([3,-.45,0],.875).set_z_index(60)
        y=apoio.get_bottom()[1]
        chao=Line([1.8,y,0],[4.2,y,0],color=LIGHT).set_z_index(60)
        normal=seta(apoio.get_center(),apoio.get_center()+.9*UP,WHITE)
        nlabel=formula('N',29).next_to(normal,RIGHT,buff=.15)
        self.play(FadeIn(apoio),Create(chao),Create(normal),FadeIn(nlabel))
        self.escrever('sem apoio',(-2.8,-1.6),25,CYAN); self.escrever('com apoio',(3,-1.6),25,WHITE)
        self.math(r'\frac{g_{\mathrm{orbita}}}{g_{\mathrm{superficie}}}=\left(\frac{R}{R+h}\right)^2\approx0{,}89',(0,1.3),37)
        self.marco('N09_apoio_e_gravidade'); self.wait(3)
        self.play(*[FadeOut(x) for x in (pessoa,apoio,chao,normal,nlabel)],run_time=.7)
        self.limpar(); self.mostrar_bola=True; self.path_alpha.set_value(1)
        self.olhar(0,0,7.4,dur=2.4)

    def n10(self):
        self.titulo('Duas órbitas circulares. O mesmo relógio.')
        self.configurar(R_T+400e3,1); self.loop=True; self.tracar=False
        self.olhar(0,0,10.2,dur=1.5)
        alto=lancamento(1.8*R_T,1); clock=ValueTracker(0)
        caminho=always_redraw(lambda:self.cam.linha(alto.r[::5]/R_T,LIGHT,2,ocultar=False))
        posalto=lambda:self.cam.si(alto.estado(clock.get_value()%alto.t[-1])[0])
        corpo=always_redraw(lambda:Circle(radius=.085,color=WHITE,stroke_width=2).move_to(posalto()).set_z_index(35))
        va=always_redraw(lambda:seta(posalto(),posalto()+np.r_[alto.estado(clock.get_value()%alto.t[-1])[1]/v_circular(R_T+400e3),0]*1.1))
        vb=self.vetor_v(1.1)
        cota_baixa=always_redraw(lambda:Line(self.cam.p((0,0)),self.pos(),color=VIOLET,stroke_width=1.3).set_z_index(23))
        cota_alta=always_redraw(lambda:Line(self.cam.p((0,0)),posalto(),color=VIOLET,stroke_width=1.3).set_z_index(23))
        relogio=DecimalNumber(0,num_decimal_places=0,group_with_commas=False,unit=r'\,\mathrm s',font_size=28,color=AMBER).move_to([-5.8,1.6,0]).set_z_index(100)
        relogio.add_updater(lambda m:m.set_value(clock.get_value()))
        self.add(caminho,corpo,va,vb,cota_baixa,cota_alta,relogio)
        self.escrever('casos independentes · tempo físico comum',(0,2.2),24,AMBER)
        self.play(clock.animate.set_value(self.orb.t[-1]),self.tau.animate.set_value(self.orb.t[-1]),run_time=9,rate_func=linear)
        self.play(self.earth_alpha.animate.set_value(.25),run_time=.6)
        self.math(r'v_{\mathrm{orb}}=\sqrt{\frac{GM}{r}}',(0,-.2),43)
        self.marco('N10_mesmo_tempo'); self.wait(2)
        self.play(*[FadeOut(x) for x in (caminho,corpo,va,vb,cota_baixa,cota_alta,relogio)],self.earth_alpha.animate.set_value(1),run_time=.8); self.limpar()

    def n11(self):
        self.titulo('Quanto tempo dura uma volta?')
        self.olhar(0,0,7.6,dur=1.3); self.tau.set_value(0)
        clock=DecimalNumber(0,num_decimal_places=0,group_with_commas=False,unit=r'\,\mathrm s',font_size=28,color=AMBER).move_to([4.5,1.6,0]).set_z_index(100)
        clock.add_updater(lambda m:m.set_value(self.tau.get_value()))
        arco=always_redraw(lambda:self.cam.linha(self.orb.r[:max(2,np.searchsorted(self.orb.t,self.tau.get_value())):4]/R_T,AMBER,4,ocultar=False))
        self.add(clock,arco); self.escrever('caso circular',(0,2.15),24,VIOLET)
        self.play(self.tau.animate.set_value(self.orb.t[-1]),run_time=7,rate_func=linear)
        clock.clear_updaters(); self.play(FadeOut(arco),FadeOut(clock),run_time=.5)
        a=self.math(r'T=\frac{2\pi r}{v}',(0,-2.4),46)
        sub=formula(r'T=\frac{2\pi r}{\sqrt{GM/r}}',46).move_to(a)
        b=formula(r'T=2\pi\sqrt{\frac{r^3}{GM}}',46).move_to(a)
        c=formula(r'T^2=\frac{4\pi^2}{GM}r^3',46).move_to(a)
        self.wait(2); self.play(TransformMatchingTex(a,sub),run_time=1.5); self.wait(.8)
        self.play(TransformMatchingTex(sub,b),run_time=1.8); self.wait(1.5)
        self.escrever('elevar os dois lados ao quadrado',(0,1.65),23,AMBER)
        self.play(TransformMatchingTex(b,c),run_time=1.8)
        self.overlays.remove(a); self.overlays.append(c)
        self.marco('N11_periodo_circular'); self.wait(3)

    def n12(self):
        self.limpar(); self.titulo('Novo caso: órbita elíptica')
        self.escrever('generalização · não é uma deformação da órbita anterior',(0,2.2),23,VIOLET)
        self.wait(2)
        a=3.6; ecc=.6; rp=a*(1-ecc)*R_T
        self.configurar(rp,math.sqrt(1+ecc),periodo(a*R_T)); self.tracar=False; self.mostrar_bola=False
        self.olhar(0,-a*ecc,19.4,roll=np.pi/2,dur=2)
        centro=np.array([0,-a*ecc]); ponta=centro+np.array([0,a])
        eixo=always_redraw(lambda:DoubleArrow(self.cam.p(centro),self.cam.p(ponta),buff=0,color=VIOLET,stroke_width=2,tip_length=.12).set_z_index(40))
        self.add(eixo); self.escrever('a',(0,-.65),29,VIOLET)
        e=self.math(r'T^2=\frac{4\pi^2}{GM}r^3',(0,-2.6),43)
        novo=formula(r'T^2=\frac{4\pi^2}{GM}a^3',43).move_to(e)
        self.escrever('No círculo, a = r.',(0,1.75),26,WHITE)
        self.play(TransformMatchingTex(e,novo),run_time=1.8); self.overlays.remove(e); self.overlays.append(novo)
        self.marco('N12_foco_semieixo'); self.wait(4)
        self.play(FadeOut(eixo),run_time=.5); self.limpar()

    def n13(self):
        self.titulo('Ajustar a velocidade. Depois, lançar.')
        self.mostrar_bola=True; self.mostrar_montanha=False
        for j,f in enumerate((.70,.92,1.,1.2,1.44)):
            if j:
                self.escrever('Reinício · mesmo ponto de lançamento',(0,2.17),23,VIOLET)
                self.wait(.6); self.limpar()
            dur=periodo(1.5*R_T)/max(.06,(2-f*f))**1.5 if f<math.sqrt(2) else periodo(1.5*R_T)
            self.configurar(1.5*R_T,f,dur); self.prever=True
            self.olhar(0,.3,7.4,dur=1.2)
            self.fator.set_value((.55,.70,.92,1.,1.2)[j])
            av=always_redraw(lambda:seta(self.pos(),self.pos()+1.1*self.fator.get_value()*RIGHT))
            def rotulo_parametro():
                z=self.fator.get_value(); info=conica(1.5*R_T,z,amostras=2)[1]
                if info['rotulo']=='circular' and abs(z-1)>1e-6:
                    return 'ligada' if z<1 else 'elíptica'
                return info['rotulo']
            rotulo=texto(rotulo_parametro(),26,CYAN).move_to([4.4,1.65,0]).set_z_index(100)
            def atualizar_rotulo(m):
                s=rotulo_parametro()
                if s!=getattr(m,'ultimo',None):
                    m.become(texto(s,26,CYAN).move_to([4.4,1.65,0]).set_z_index(100)); m.ultimo=s
            rotulo.add_updater(atualizar_rotulo)
            controle=VGroup(Line([-1.5,-2.16,0],[1.5,-2.16,0],color=VIOLET,stroke_width=2),
                            texto('v₀',24,WHITE).move_to([-2,-2.16,0])).set_z_index(100)
            manopla=always_redraw(lambda:Dot([-1.5+3*(self.fator.get_value()-.5),-2.16,0],.07,color=WHITE).set_z_index(100))
            self.add(av,rotulo,controle,manopla)
            info=conica(1.5*R_T,f)[1]
            self.escrever('mesmo r₀ = 1,5 R_T · direção tangencial',(0,-2.65),23,VIOLET)
            self.escrever('ajuste de v₀',(0,2.13),24,WHITE)
            self.play(self.fator.animate.set_value(f),run_time=1.5,rate_func=linear)
            self.marco(f'N13_ajuste_{j+1}'); self.wait(1)
            self.play(*[FadeOut(m) for m in (av,rotulo,controle,manopla)],run_time=.35); self.limpar(); self.prever=False
            self.escrever(info['rotulo'],(4.7,1.85),30,CYAN)
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
            self.marco(f'N13_voo_{j+1}'); self.wait(1.3); self.limpar()

    def n14(self):
        self.titulo('Retomando o caso de impacto')
        self.escrever('reinício do lançamento ligado que colide',(0,2.15),23,VIOLET)
        self.configurar(1.5*R_T,.70); self.olhar(0,.3,7.4,dur=1.3)
        self.voo(4.5,7.4,False); self.marco('N14_impacto_fisico')
        impacto=self.estado()[0]/R_T
        self.olhar(impacto[0],impacto[1],.9,dur=1.8); self.wait(1.5)
        self.olhar(0,.2,6.7,dur=1.8); self.limpar()
        ps=conica(1.5*R_T,.70,fisica=False)[0]/R_T
        ang=np.linspace(0,2*np.pi,len(ps)); hit=math.atan2(impacto[0],impacto[1])
        resto=ps[ang>=hit]
        matematica=always_redraw(lambda:self.cam.linha(resto,VIOLET,2.5,ocultar=False,tracejado=True))
        self.play(self.earth_alpha.animate.set_value(.4),run_time=.8); self.add(matematica)
        self.escrever('trajetória física  |  continuação matemática',(0,-2.6),26,VIOLET)
        self.escrever('Ligada matematicamente. Com colisão.',(0,2.15),25,WHITE)
        self.marco('N14_continuacao_tracejada'); self.wait(4)
        self.play(FadeOut(matematica),run_time=.6); self.limpar()

    def n15(self):
        self.titulo('Experimento mental de Newton')
        self.path_alpha.set_value(0)
        self.mostrar_montanha=True; self.mostrar_bola=False
        self.olhar(0,0,6.7,dur=1.4)
        caminhos=[]
        for f in (.55,.80,.985,1.):
            ps=lancamento(1.06*R_T,f).r[::4]/R_T
            m=always_redraw(lambda pts=ps:self.cam.linha(pts,BLUE,2.2))
            caminhos.append(m); self.add(m); self.wait(.5)
        self.marco('N15_diagrama_canhao'); self.wait(3)
        self.play(*[FadeOut(x) for x in caminhos],self.earth_alpha.animate.set_value(1),run_time=.8)

    def n16(self):
        self.titulo('A mesma lei gravitacional.')
        self.mostrar_montanha=False; self.mostrar_bola=True
        theta=.12; r=R_T+25
        self.orb=integrar(r*np.array([np.sin(theta),np.cos(theta)]),[0,0],4,dt=.01)
        self.loop=False; self.tracar=False; self.tau.set_value(0)
        self.path_alpha.set_value(0)
        self.escrever('pedra · novo caso, escala local',(0,2.15),24,WHITE)
        foco=(R_T+12)*np.array([np.sin(theta),np.cos(theta)])/R_T
        self.olhar(foco[0],foco[1],.000013,roll=theta,dur=2.5)
        self.voo(2.8,None,False); self.marco('N16_pedra'); self.wait(.7)
        self.limpar(); self.escrever('satélite · escala orbital',(0,2.15),24,WHITE)
        self.configurar(R_T+400e3,1); self.loop=True; self.tracar=False; self.path_alpha.set_value(1)
        self.olhar(0,0,7,dur=2.7)
        self.play(self.tau.animate.set_value(.7*self.orb.t[-1]),run_time=4,rate_func=linear)
        self.marco('N16_satelite'); self.limpar()
        self.escrever('Terra–Lua · mudança de sistema e escala',(0,2.15),24,WHITE)
        self.mostrar_bola=False; self.phase=ValueTracker(0)
        self.d=384.4e6/R_T; self.rb=4.67e6/R_T
        unit=lambda:np.array([math.cos(self.phase.get_value()),math.sin(self.phase.get_value())])
        self.earth_center=lambda:-self.rb*unit()
        self.lua=always_redraw(lambda:Dot(self.cam.p((self.d-self.rb)*unit()),radius=max(.055,.2727*self.cam.k),color=WHITE).set_z_index(35))
        self.add(self.lua); self.path_alpha.set_value(0)
        self.olhar(self.d/2,0,78,dur=3)
        self.play(self.phase.animate.set_value(.24),run_time=3,rate_func=linear)
        self.marco('N16_terra_lua'); self.wait(1)

    def n17(self):
        self.limpar(); self.titulo('Terra e Lua orbitam um ponto comum')
        self.play(self.cam.ax.animate.set_value(-2.8),run_time=.7)
        self.olhar(0,0,13.6*(self.d-self.rb)/4.2,incl=1.14,dur=2)
        bary=Dot(self.cam.p((0,0)),.035,color=CYAN).set_z_index(50)
        orbit=np.column_stack([(self.d-self.rb)*np.cos(np.linspace(0,TAU,500)),(self.d-self.rb)*np.sin(np.linspace(0,TAU,500))])
        guia=always_redraw(lambda:self.cam.linha(orbit,VIOLET,1.3,ocultar=False))
        foco=always_redraw(lambda:Circle(radius=.15,color=VIOLET,stroke_width=1.5).move_to(self.cam.p(self.earth_center())).set_z_index(50))
        bc=np.array([4.,.15,0]); R=1.15
        uv=lambda:np.array([math.cos(self.phase.get_value()),math.sin(self.phase.get_value()),0])
        ec=lambda:bc-R*self.rb*uv()
        terra_zoom=always_redraw(lambda:globo(ec(),R))
        raio=always_redraw(lambda:Line(ec(),bc,color=VIOLET,stroke_width=2).set_z_index(45))
        centro=always_redraw(lambda:Dot(ec(),.045,color=WHITE).set_z_index(50))
        bar2=Dot(bc,.065,color=CYAN).set_z_index(50)
        ligacao=always_redraw(lambda:DashedLine(self.cam.p(self.earth_center())+.15*RIGHT,[2.0,.15,0],color=VIOLET,dash_length=.12,stroke_width=1).set_z_index(5))
        self.add(bary,guia,foco,ligacao,terra_zoom,raio,centro,bar2)
        self.escrever('vista oblíqua · Lua ampliada',(-2.8,2.1),20,VIOLET)
        self.escrever('distâncias em escala',(-2.8,-2.1),20,MUTED)
        self.escrever('ampliação · vista perpendicular',(3.8,2.1),20,VIOLET)
        self.math(r'r_b=4{,}67\times10^6\,\mathrm m\approx0{,}733R_T',(3.7,-1.9),28)
        self.play(self.phase.animate.increment_value(TAU),run_time=12,rate_func=linear)
        self.marco('N17_baricentro_mesmo_sistema')
        self.escrever('Terra e Lua caem uma em direção à outra\ne orbitam um ponto comum.',(0,-2.62),26,WHITE)
        self.wait(3)
        for m in (bary,guia,foco,ligacao,terra_zoom,raio,centro,bar2,self.lua): m.clear_updaters(recursive=True)
        self.play(*[FadeOut(x) for x in (bary,guia,foco,ligacao,terra_zoom,raio,centro,bar2,self.lua)],run_time=.8)
        self.limpar(); self.earth_center=lambda:np.zeros(2)

    def n18(self):
        self.titulo('De volta à montanha')
        self.play(self.cam.ax.animate.set_value(0),run_time=.5)
        self.configurar(1.06*R_T,1); self.mostrar_montanha=True; self.path_alpha.set_value(1)
        self.olhar(0,1.035,.30,dur=3)
        self.marco('N18_reencontro_montanha'); self.wait(1.5)
        self.titulo('Orbitar não é vencer a gravidade.')
        self.voo(8,6.4,True); self.loop=True; self.tracar=False
        self.titulo('É cair… e continuar errando o chão.')
        self.play(self.tau.animate.increment_value(.25*self.orb.t[-1]),run_time=4,rate_func=linear)
        self.marco('N18_fechamento'); self.wait(3)
        self.play(FadeOut(self.cabecalho),FadeOut(self.tag),run_time=1.3)
        self.play(self.tau.animate.increment_value(.18*self.orb.t[-1]),run_time=3,rate_func=linear)
