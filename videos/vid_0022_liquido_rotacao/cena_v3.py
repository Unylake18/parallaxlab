"""VID22 / EP. 08 — continuidade editorial V3, silenciosa, 168 s.

Reutiliza os caches preparados por preparar_3d_v2.py. V1 e V2 preservadas.
"""
import json
import sys
from pathlib import Path

import numpy as np
from manim import *
from MF_Tools import TransformByGlyphMap, CombineTex

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(UNIT))
sys.path.insert(0,str(ROOT/'experimentos/blender/arsenal'))
from template.config import BACKGROUND_COLOR, TEXT_COLOR, PRIMARY_COLOR, WATERMARK_PATH
from template.fonts import screen_text
from manim_solido3d import Solido3D
from configuracao_3d import SEQUENCIAS, RES, AMOSTRAS, ALTURA_IMAGEM, CENTRO_IMAGEM
from preparar_3d_v2 import SECAO
import ponte

config.media_dir=str(UNIT/'media')
config.background_color=BACKGROUND_COLOR
CYAN=PRIMARY_COLOR
SURFACE='#75BDFF'
PRESSURE='#D77CFF'
BLUE='#267BFF'
MUTED='#8492AE'
WHITE=TEXT_COLOR


class LiquidoRotacao022V3(Scene):
    def text(self,s,y=0,size=28,color=WHITE,x=0,width=7.6):
        mob=screen_text(s,font_size=size,color=color,oversample=2 if size>=25 else 4)
        if mob.width>width:
            mob.scale_to_fit_width(width)
        return mob.move_to([x,y,0]).set_z_index(30)

    def formula(self,tex,y=-2.1,size=43,color=WHITE):
        mob=MathTex(tex,font_size=size,color=color)
        if mob.width>7.5:
            mob.scale_to_fit_width(7.5)
        return mob.move_to([0,y,0]).set_z_index(25)

    def glyph(self,runs,y=-2.1,size=41):
        """Uma string MathTex; faixas de glifos verificadas após LaTeX estabilizado."""
        mob=self.formula(' '.join(tex for name,tex,color in runs),y,size)
        mob.runs={}
        n=0
        for name,tex,color in runs:
            count=len(MathTex(tex)[0])
            ids=list(range(n,n+count))
            mob.runs[name]=ids
            VGroup(*[mob[0][i] for i in ids]).set_color(color)
            n+=count
        assert n==len(mob[0]),(n,len(mob[0]),mob.tex_string)
        return mob

    def part(self,mob,*names):
        return VGroup(*[mob[0][i] for name in names for i in mob.runs[name]])

    def combined(self,**sources):
        mob=CombineTex(*sources.values())
        mob.runs={}
        offset=0
        for prefix,source in sources.items():
            mob.runs.update({prefix+':'+name:[offset+i for i in ids] for name,ids in source.runs.items()})
            offset+=len(source[0])
            self.remove(*source.get_family())
        self.add(mob)
        return mob

    def morph(self,old,new,links,rt=1.6,extras=()):
        settled=new.copy()
        entries=[(old.runs[a] if isinstance(a,str) else a,new.runs[b] if isinstance(b,str) else b)
                 for a,b in links]
        animation=TransformByGlyphMap(old,new,*entries,auto_fade=True,printing=False)
        assert not animation.show_indices
        self.play(animation,*extras,run_time=rt)
        self.remove(*old.get_family(),*new.get_family())
        new.become(settled)
        self.add(new)
        self.maps.append(dict(t=round(self.time,3),de=getattr(old,'tex_string','fontes combinadas'),
                              para=new.tex_string,ligacoes=len(links)))
        return new

    def cue(self,s):
        mob=self.text(s,5.65,29)
        if self.caption is None:
            self.play(FadeIn(mob,shift=.1*UP),run_time=.4)
        else:
            # A leitura do texto antigo termina antes de começar o próximo.
            self.play(FadeOut(self.caption),run_time=.18)
            self.play(FadeIn(mob,shift=.08*UP),run_time=.22)
        self.caption=mob

    def until(self,t):
        assert self.time<=t+.1,(t,self.time)
        if t>self.time+.001:
            self.wait(t-self.time)

    def mark(self,s):
        self.events.append(dict(t=round(self.time,3),nome=s))

    def asset(self,name,fase=0):
        kw=dict(params=SECAO,animado=False) if name=='secao' else SEQUENCIAS[name]
        source=Solido3D('liquido_rotacao',res=RES,amostras=AMOSTRAS,render='nunca',**kw)
        return source.mobject(cena=self,altura=ALTURA_IMAGEM,centro=np.array(CENTRO_IMAGEM),autoplay=False,fase=fase)

    def path(self,points,color=SURFACE,width=3):
        return VMobject(stroke_color=color,stroke_width=width).set_points_as_corners(points)

    def gradient_strip(self,y=.1):
        return VGroup(*[Rectangle(width=.68,height=.33,stroke_width=0,fill_color=PRESSURE,
                                   fill_opacity=.12+.1*i).move_to([-2.38+.69*i,y,0]) for i in range(8)])

    def cross(self,mob):
        return Line(mob.get_corner(DL)-.04*RIGHT,mob.get_corner(UR)+.04*RIGHT,color=WHITE,stroke_width=2.3)

    def add_header(self):
        # Mesma composição de vid_0020; fica em primeiro plano durante os PNGs.
        self.logo=ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(.35)
        self.logo.to_corner(UP+RIGHT,buff=.28).set_z_index(200)
        self.header=screen_text('POR TRÁS DA FÓRMULA · EP. 08',20,oversample=2)
        self.header.set_opacity(.65).to_corner(UP+LEFT,buff=.4).set_z_index(200)
        self.add_foreground_mobjects(self.logo,self.header)

    def construct(self):
        self.maps=[]
        self.events=[]
        self.caption=None
        projection=json.loads((UNIT/'projecao_3d_v2.json').read_text(encoding='utf-8'))
        p3=projection['inicial']
        # Composição copiada do último curto aprovado (vid_0020 / EP. 07).
        self.add_header()
        question=self.text('Por que a superfície de um\nlíquido girando vira uma parábola?',6.05,30)
        self.add(question)

        # A — fenômeno, com o setor existente; fase e forma são independentes.
        self.mark('fenomeno')
        plane=self.asset('plano')
        self.play(FadeIn(plane),run_time=.8)
        phase=ValueTracker(0)
        plane.add_updater(lambda m:m.set_fase(phase.get_value()))
        omega=self.formula(r'\omega',-3.5,40)
        self.play(FadeIn(omega),phase.animate.set_value(.25),run_time=3,rate_func=linear)
        stable=self.text('após estabilizar',-4.5,27)
        self.play(FadeIn(stable),run_time=.4)
        plane.clear_updaters()
        self.remove(plane)
        morph=self.asset('morph')
        self.add(morph)
        phase.set_value(0)
        morph.add_updater(lambda m:m.set_fase(phase.get_value()))
        self.play(phase.animate.set_value(.5),run_time=6,rate_func=linear)
        morph.clear_updaters()
        self.remove(morph)
        final=self.asset('final',.75)
        phase.set_value(.75)
        self.add(final)
        final.add_updater(lambda m:m.set_fase(phase.get_value()))
        self.play(phase.animate.set_value(.9),run_time=1.8,rate_func=linear)
        final.clear_updaters()

        # B — corte real do asset; a região destacada nasce dentro do líquido.
        self.mark('extracao_3d')
        section_asset=self.asset('secao')
        self.play(FadeOut(question),FadeOut(omega),FadeOut(stable),FadeOut(final),FadeIn(section_asset),run_time=.7)
        self.cue('Um corte vertical do líquido')
        section=Polygon(*p3['secao'],stroke_color=SURFACE,stroke_width=2,
                        fill_color=BLUE,fill_opacity=.12).set_z_index(5)
        meridian=self.path(p3['curva'],WHITE,3.2).set_z_index(6)
        axis=DashedLine(*p3['eixo'],color=CYAN,stroke_width=1.5)
        self.play(Create(section),Create(meridian),Create(axis),run_time=1.2)
        cell=Polygon(*p3['regiao'],stroke_color=PRESSURE,stroke_width=3,
                     fill_color=PRESSURE,fill_opacity=.5).set_z_index(10)
        note=self.text('Isolamos um pequeno elemento do líquido,\na uma distância r do eixo.',-3.9,26)
        self.play(FadeIn(cell),FadeIn(note),run_time=.8)
        self.play(Indicate(cell,color=PRESSURE,scale_factor=1.3),run_time=1)
        self.until(17.5)

        # A mesma região e a mesma seção tornam-se a representação frontal.
        fullpt=lambda r,z:np.array([2.85*r,.65+2.2*z,0])
        f=lambda r:.5+.95*r*r
        section2=Polygon(fullpt(-1,0),fullpt(1,0),
                         *[fullpt(r,f(r)) for r in np.linspace(1,-1,121)],
                         stroke_color=SURFACE,stroke_width=2,fill_color=BLUE,fill_opacity=.24)
        curve2=self.path([fullpt(r,f(r)) for r in np.linspace(-1,1,121)],SURFACE,3.5)
        small=Rectangle(width=.31,height=.31,color=PRESSURE,fill_color=PRESSURE,fill_opacity=.5).move_to(fullpt(.585,.30))
        axis2=DashedLine(fullpt(0,0),fullpt(0,1.7),color=CYAN,stroke_width=1.5)
        self.play(FadeOut(section_asset),Transform(section,section2),Transform(meridian,curve2),
                  Transform(axis,axis2),Transform(cell,small),run_time=2)
        level=DashedLine(fullpt(-1,.30),fullpt(1,.30),color=CYAN,stroke_width=1.1).set_opacity(.45)
        origin=self.formula('r=0',0,25,CYAN).next_to(axis,LEFT,buff=.1)
        radius=DoubleArrow(fullpt(0,.30),fullpt(.585,.30),color=CYAN,buff=0,tip_length=.1,stroke_width=2)
        rlabel=self.formula('r',0,29,CYAN).next_to(radius,DOWN,buff=.12)
        self.play(Create(level),FadeIn(origin),GrowArrow(radius),FadeIn(rlabel),run_time=.7)
        self.mark('elemento_dentro_da_agua')
        self.until(22)
        enlarged=Rectangle(width=1.45,height=1.3,stroke_color=PRESSURE,fill_color=PRESSURE,fill_opacity=.5).move_to([0,2.65,0])
        self.cue('Aproximando o mesmo elemento')
        self.play(Transform(cell,enlarged),FadeOut(section),FadeOut(meridian),FadeOut(axis),FadeOut(radius),
                  FadeOut(rlabel),FadeOut(level),FadeOut(origin),FadeOut(note),run_time=2)
        self.mark('elemento_ampliado')
        # Coordenadas nas faces; área e espessura só depois da origem espacial.
        radial_axis=Arrow([-2.9,1.35,0],[2.95,1.35,0],buff=0,color=CYAN,stroke_width=1.7)
        faces=VGroup(*[Line([x,2,0],[x,3.3,0],color=PRESSURE,stroke_width=4) for x in [-.725,.725]])
        coords=VGroup(self.formula('r',0,28,CYAN).move_to([-.725,.9,0]),
                      self.formula(r'r+dr',0,28,CYAN).move_to([.95,.9,0]))
        dr=DoubleArrow([-.725,1.75,0],[.725,1.75,0],buff=0,color=CYAN,tip_length=.1,stroke_width=2)
        drlabel=self.formula('dr',0,27,CYAN).next_to(dr,DOWN,buff=.12)
        area=self.formula('A',0,31).move_to(cell)
        self.play(FadeIn(area),Create(faces),run_time=.4)
        self.play(GrowArrow(dr),FadeIn(drlabel),run_time=.4)
        self.play(GrowArrow(radial_axis),FadeIn(coords),run_time=.4)
        mass=self.glyph([('dm','dm=',WHITE),('rho',r'\rho',WHITE),('A','A',WHITE),('dr','dr',CYAN)],y=-.3,size=34)
        v=self.formula(r'v=\omega r',-1.5,40,CYAN)
        ar=self.glyph([('ar','a_r=',WHITE),('minus','-',WHITE),('omega',r'\omega^2r',WHITE)],y=-3.0,size=42)
        accel=Arrow([-.1,3.75,0],[-1.65,3.75,0],buff=0,color=WHITE,stroke_width=3.5)
        accel_note=self.text('para o eixo',4.15,22,x=-1.4)
        self.play(Write(mass),Write(v),GrowArrow(accel),FadeIn(accel_note),Write(ar),run_time=1.4)
        self.until(32)

        # Pressão sobre todas as faces; destacar apenas a componente radial.
        self.cue('A pressão age nas duas faces')
        self.play(FadeOut(v),FadeOut(accel),FadeOut(accel_note),FadeOut(ar),run_time=.5)
        ar.move_to([0,-4.85,0])
        inward=Arrow([-2.4,2.65,0],[-.76,2.65,0],buff=0,color=WHITE,stroke_width=4.3)
        outward=Arrow([2.82,2.65,0],[.76,2.65,0],buff=0,color=WHITE,stroke_width=4.3)
        other_faces=VGroup(Arrow([0,4.15,0],[0,3.34,0],buff=0,color=PRESSURE,stroke_width=2),
                           Arrow([0,1.04,0],[0,1.96,0],buff=0,color=PRESSURE,stroke_width=2)).set_opacity(.3)
        pin=self.formula(r'p(r)A',0,31,PRESSURE).move_to([-2.1,3.45,0])
        pout=self.formula(r'p(r+dr)A',0,31,PRESSURE).move_to([2.0,3.45,0])
        self.play(GrowArrow(inward),GrowArrow(outward),FadeIn(other_faces),FadeIn(pin),FadeIn(pout),run_time=1.2)
        self.cue('A face externa empurra um pouco mais')
        self.play(FadeOut(other_faces),Indicate(outward,color=WHITE),run_time=.8)
        inequality=self.formula(r'p(r+dr)>p(r)',-1.2,34,PRESSURE)
        self.play(Write(inequality),run_time=.7)
        self.until(37)
        force=self.glyph([('Fr','F_r',WHITE),('eq','=',WHITE),('inner','p(r)A',PRESSURE),
                          ('minus','-',WHITE),('outer','p(r+dr)',PRESSURE),('A','A',WHITE)],y=-2.45,size=39)
        self.play(Write(self.part(force,'Fr','eq','minus')),
                  TransformFromCopy(pin,self.part(force,'inner')),
                  TransformFromCopy(pout,self.part(force,'outer','A')),run_time=1.2)
        self.remove(*force.get_family())
        self.add(force)
        self.play(FadeOut(inequality),mass.animate.move_to([0,-.2,0]),run_time=.4)
        taylor=self.glyph([('outer','p(r+dr)',PRESSURE),('approx',r'\approx',WHITE),('base','p(r)',PRESSURE),
                           ('plus','+',WHITE),('grad',r'\frac{\partial p}{\partial r}',PRESSURE),('dr','dr',CYAN)],y=-3.9,size=35)
        self.cue('A diferença deixa uma resultante para o eixo')
        self.play(TransformFromCopy(self.part(force,'outer'),self.part(taylor,'outer')),
                  Write(self.part(taylor,'approx','base','plus','grad','dr')),run_time=1.5)
        self.remove(*taylor.get_family())
        self.add(taylor)
        self.until(43)
        expanded=self.glyph([('Fr','F_r',WHITE),('approx',r'\approx',WHITE),('inner','p(r)A',PRESSURE),
                             ('minus','-',WHITE),('outer','p(r)',PRESSURE),('Ao','A',WHITE),('minus2','-',WHITE),
                             ('grad',r'\frac{\partial p}{\partial r}',PRESSURE),('Ag','A',WHITE),('dr','dr',CYAN)],y=-2.45,size=37)
        both=self.combined(f=force,t=taylor)
        self.morph(both,expanded,[('f:Fr','Fr'),('f:eq','approx'),('f:inner','inner'),('f:minus','minus'),
                                 ('t:base','outer'),('f:A','Ao'),('t:plus','minus2'),('t:grad','grad'),
                                 ('f:A','Ag'),('t:dr','dr')],rt=2.1)
        cuts=VGroup(self.cross(self.part(expanded,'inner')),self.cross(self.part(expanded,'outer','Ao')))
        self.play(Create(cuts),run_time=.8)
        self.wait(.8)
        reduced=self.glyph([('Fr','F_r',WHITE),('approx',r'\approx',WHITE),('minus','-',WHITE),
                            ('grad',r'\frac{\partial p}{\partial r}',PRESSURE),('A','A',WHITE),('dr','dr',CYAN)],y=-2.45,size=44)
        self.morph(expanded,reduced,[('Fr','Fr'),('approx','approx'),('minus2','minus'),('grad','grad'),('Ag','A'),('dr','dr')],
                   extras=(FadeOut(cuts),),rt=1.8)
        self.mark('gradiente_construido')
        self.until(55)

        # Newton sem remover ou reconstruir o elemento.
        self.cue('A pressão fornece a força centrípeta')
        accel=Arrow([-.1,3.85,0],[-1.8,3.85,0],buff=0,color=WHITE,stroke_width=3.5)
        self.play(GrowArrow(accel),FadeIn(ar),run_time=.7)
        newton_law=self.formula(r'F_r=dm\,a_r',-3.6,34)
        self.play(Write(newton_law),run_time=.7)
        newton=self.glyph([('minus','-',WHITE),('grad',r'\frac{\partial p}{\partial r}',PRESSURE),
                           ('Al','A',WHITE),('drl','dr',CYAN),('eq','=',WHITE),('minus2','-',WHITE),
                           ('rho',r'\rho',WHITE),('Ar','A',WHITE),('drr','dr',CYAN),('omega',r'\omega^2r',WHITE)],y=-2.5,size=38)
        sources=self.combined(f=reduced,m=mass,a=ar)
        self.morph(sources,newton,[('f:minus','minus'),('f:grad','grad'),('f:A','Al'),('f:dr','drl'),
                                  ('f:approx','eq'),('a:minus','minus2'),('m:rho','rho'),('m:A','Ar'),
                                  ('m:dr','drr'),('a:omega','omega')],rt=2,extras=(FadeOut(newton_law),))
        cuts=VGroup(*[self.cross(self.part(newton,name)) for name in ['minus','Al','drl','minus2','Ar','drr']])
        self.play(Create(cuts),run_time=.8)
        radial=self.glyph([('grad',r'\frac{\partial p}{\partial r}',PRESSURE),('eq','=',WHITE),
                           ('rho',r'\rho',WHITE),('omega',r'\omega^2r',CYAN)],y=-2.5,size=45)
        self.morph(newton,radial,[('grad','grad'),('eq','eq'),('rho','rho'),('omega','omega')],rt=1.7,extras=(FadeOut(cuts),))
        sign=self.formula(r'\frac{\partial p}{\partial r}>0',-4.05,40,PRESSURE)
        strip=self.gradient_strip(-.15)
        strip_arrow=Arrow([-2.6,-.6,0],[2.65,-.6,0],buff=0,color=CYAN,stroke_width=2)
        strip_labels=VGroup(self.text('perto do eixo',-.98,22,CYAN,x=-1.95,width=2.4),
                            self.text('mais longe',-.98,22,CYAN,x=1.95,width=2.4),
                            self.text('menor pressão',.32,22,PRESSURE,x=-1.95,width=2.4),
                            self.text('maior pressão',.32,22,PRESSURE,x=1.95,width=2.4))
        self.play(LaggedStart(*[FadeIn(m) for m in strip],lag_ratio=.15),GrowArrow(strip_arrow),Write(sign),FadeIn(strip_labels),run_time=1.3)
        self.cue('Na mesma altura, a pressão cresce para fora')
        self.mark('pressao_cresce')
        self.until(69)

        # Mesmo elemento, outra direção; faces radiais giram para cima/baixo.
        self.cue('Na vertical, a pressão precisa equilibrar o peso')
        self.play(*[FadeOut(m) for m in [coords,dr,drlabel,radial_axis,strip,strip_arrow,strip_labels,sign,accel,area,radial]],run_time=.6)
        diagram=VGroup(cell,faces,inward,outward,pin,pout)
        # Os vetores se transformam enquanto o retângulo gira, preservando sua identidade.
        bottom=Arrow([0,.45,0],[0,1.9,0],buff=0,color=WHITE,stroke_width=4)
        top=Arrow([0,4.65,0],[0,3.4,0],buff=0,color=WHITE,stroke_width=4)
        pb=self.formula(r'p(z)A',0,29,PRESSURE).move_to([-1.45,1.2,0])
        pt=self.formula(r'p(z+dz)A',0,29,PRESSURE).move_to([-1.65,4.2,0])
        self.play(Rotate(cell,PI/2),Rotate(faces,PI/2,about_point=cell.get_center()),
                  Transform(inward,bottom),Transform(outward,top),Transform(pin,pb),Transform(pout,pt),run_time=1.5)
        weight=Arrow([1.25,3.2,0],[1.25,1.9,0],buff=0,color=WHITE,stroke_width=3)
        weight_label=self.formula(r'dm\,g',0,29).move_to([2.25,2.5,0])
        zdir=Arrow([-3.2,1.6,0],[-3.2,3.6,0],buff=0,color=CYAN,stroke_width=2)
        zlabel=self.formula('+z',0,27,CYAN).next_to(zdir,UP,buff=.12)
        self.play(GrowArrow(weight),FadeIn(weight_label),GrowArrow(zdir),FadeIn(zlabel),run_time=.7)
        balance=self.glyph([('bot','p(z)A',PRESSURE),('minus','-',WHITE),('top','p(z+dz)A',PRESSURE),
                            ('minus2','-',WHITE),('mg',r'dm\,g',WHITE),('eq','=0',WHITE)],y=-1.7,size=36)
        self.play(Write(balance),run_time=1)
        vertical=self.glyph([('minus','-',WHITE),('grad',r'\frac{\partial p}{\partial z}',PRESSURE),
                             ('Adz',r'A\,dz',CYAN),('minus2','-',WHITE),('rho',r'\rho',WHITE),
                             ('Adz2',r'A\,dz',CYAN),('g','g',WHITE),('eq','=0',WHITE)],y=-1.7,size=38)
        self.morph(balance,vertical,[('minus','minus'),('top','grad'),('minus2','minus2'),('mg','rho'),('eq','eq')],rt=1.3)
        hydro=self.glyph([('grad',r'\frac{\partial p}{\partial z}',PRESSURE),('eq','=',WHITE),
                          ('minus','-',WHITE),('rho',r'\rho',WHITE),('g','g',WHITE)],y=-1.7,size=44)
        self.morph(vertical,hydro,[('grad','grad'),([vertical.runs['eq'][0]],'eq'),('minus2','minus'),('rho','rho'),('g','g')],rt=1.4)
        self.mark('vertical')
        self.until(81)

        # C — superfície inteira no 3D; os pontos indicam pressão, não partículas.
        self.cue('Na superfície livre, a pressão é a mesma')
        self.play(*[FadeOut(m) for m in [diagram,weight,weight_label,zdir,zlabel,hydro]],run_time=.6)
        surface_asset=self.asset('secao')
        self.play(FadeIn(surface_asset),run_time=.8)
        rings=VGroup(*[self.path(pts,CYAN,1.6) for pts in p3['aneis']]).set_stroke(opacity=.7)
        dots=VGroup(*[Dot(point,radius=.065,color=CYAN) for point in p3['superficie']])
        labels=VGroup(*[self.formula(r'p_{\rm atm}',0,29,PRESSURE).next_to(dot,UP,buff=.15) for dot in dots])
        iso=self.glyph([('p','p(r,z(r))',PRESSURE),('eq','=',WHITE),('atm',r'p_{\rm atm}',PRESSURE)],y=-3.5,size=42)
        self.play(Create(rings),FadeIn(dots),FadeIn(labels),run_time=1.4)
        self.play(ShowPassingFlash(rings.copy().set_stroke(width=3),time_width=.7),run_time=1.4)
        self.mark('isobarica_3d')
        self.until(87)
        # Match cut apenas da metade r>=0 da seção para o gráfico de análise.
        half3=self.path(p3['curva'][len(p3['curva'])//2:],WHITE,3.7)
        self.add(half3)
        # A curva fica imóvel enquanto o objeto ao redor desaparece.
        self.play(FadeOut(surface_asset),FadeOut(rings),FadeOut(dots),FadeOut(labels),run_time=1.2)
        self.mark('meridiana_extraida_imovel')
        self.wait(.4)
        point=lambda r:np.array([-2.75+5.5*r,1+2.05*f(r),0])
        curve=self.path([point(r) for r in np.linspace(0,1,121)],SURFACE,3.7)
        axes=VGroup(Arrow([-2.75,1,0],[3.2,1,0],buff=0,color=CYAN,stroke_width=1.5,tip_length=.12),
                    Arrow([-2.75,1,0],[-2.75,4.6,0],buff=0,color=CYAN,stroke_width=1.5,tip_length=.12),
                    self.formula('r',0,27,CYAN).move_to([3.45,1,0]),self.formula('z',0,27,CYAN).move_to([-2.75,4.85,0]),
                    self.formula(r'r\ge0',0,26,CYAN).move_to([2.6,.55,0]))
        self.play(Transform(half3,curve),Create(axes),run_time=1.0)
        iso.move_to([0,-1.0,0])
        curve=half3
        walk=ValueTracker(.13)
        marker=always_redraw(lambda:Dot(point(walk.get_value()),radius=.07,color=WHITE))
        def increments():
            r=walk.get_value()
            a,b=point(r),point(r+.09)
            corner=np.array([b[0],a[1],0])
            horiz=Line(a,corner,color=CYAN,stroke_width=3)
            vert=Line(corner,b,color=SURFACE,stroke_width=3)
            return VGroup(horiz,vert,self.formula('dr',0,24,CYAN).next_to(horiz,DOWN,buff=.12),
                          self.formula('dz',0,24,SURFACE).next_to(vert,RIGHT,buff=.12))
        steps=always_redraw(increments)
        self.add(marker,steps)
        self.cue('r e z mudam na superfície; a pressão não')
        local_atm=self.formula(r'p_{\rm atm}',0,27,PRESSURE)
        local_atm.add_updater(lambda m:m.next_to(point(walk.get_value()),UP,buff=.22))
        self.add(local_atm)
        self.play(walk.animate.set_value(.78),run_time=3,rate_func=linear)
        self.play(Write(iso),run_time=.6)
        total=self.glyph([('zero','0',WHITE),('eq','=',WHITE),('der',r'\frac{d}{dr}',CYAN),
                          ('p','p(r,z(r))',PRESSURE)],y=-2.6,size=42)
        self.play(Write(total),run_time=.7)
        chain=self.glyph([('zero','0',WHITE),('eq','=',WHITE),('gr',r'\frac{\partial p}{\partial r}',PRESSURE),
                          ('plus','+',WHITE),('gz',r'\frac{\partial p}{\partial z}',PRESSURE),
                          ('slope',r'\frac{dz}{dr}',CYAN)],y=-2.6,size=42)
        # Os componentes da regra da cadeia respondem aos dois deslocamentos.
        self.morph(total,chain,[('zero','zero'),('eq','eq'),('p','gr'),('p','gz'),('der','slope')],rt=1.6,
                   extras=(Indicate(steps[0],color=CYAN),Indicate(steps[1],color=SURFACE)))
        self.mark('regra_cadeia')
        self.until(101)

        # Substituir gradientes; ponto e tangente caminham continuamente até R.
        self.cue('Quanto mais longe do eixo, maior a inclinação')
        steps.clear_updaters()
        marker.clear_updaters()
        local_atm.clear_updaters()
        self.play(FadeOut(steps),FadeOut(marker),FadeOut(iso),FadeOut(local_atm),run_time=.5)
        sub=self.glyph([('zero','0',WHITE),('eq','=',WHITE),('rho1',r'\rho',WHITE),('omega',r'\omega^2r',CYAN),
                        ('minus','-',WHITE),('rho2',r'\rho',WHITE),('g','g',WHITE),('slope',r'\frac{dz}{dr}',CYAN)],y=-2.6,size=44)
        self.morph(chain,sub,[('zero','zero'),('eq','eq'),('gr',sub.runs['rho1']+sub.runs['omega']),
                             ('plus','minus'),('gz',sub.runs['rho2']+sub.runs['g']),('slope','slope')],rt=2)
        cuts=VGroup(self.cross(self.part(sub,'rho1')),self.cross(self.part(sub,'rho2')))
        self.play(Create(cuts),run_time=.7)
        slope=self.glyph([('slope',r'\frac{dz}{dr}',CYAN),('eq','=',WHITE),('coef',r'\frac{\omega^2}{g}',WHITE),('r','r',CYAN)],y=-2.6,size=48)
        self.morph(sub,slope,[('slope','slope'),('eq','eq'),(sub.runs['omega'][:-1]+sub.runs['g'],'coef'),
                              ([sub.runs['omega'][-1]],'r')],rt=1.8,extras=(FadeOut(cuts),))
        walk.set_value(.02)
        def moving_tangent():
            r=walk.get_value()
            center=point(r)
            direction=np.array([5.5,2.05*1.9*r,0])
            direction/=np.linalg.norm(direction)
            projection_line=DashedLine(center,[center[0],1,0],color=CYAN,stroke_width=1.2).set_opacity(.5)
            foot=np.array([center[0],1,0])
            rmark=self.formula('r',0,23,CYAN).next_to(foot,DOWN,buff=.12)
            dx=.48
            corner=center+dx*RIGHT
            end=corner+UP*(dx*2.05*1.9*r/5.5)
            triangle=VGroup(Line(center,corner,color=CYAN,stroke_width=2),
                            Line(corner,end,color=SURFACE,stroke_width=2))
            return VGroup(Dot(center,radius=.075,color=WHITE),
                          Line(center-.6*direction,center+.6*direction,color=WHITE,stroke_width=3),projection_line,rmark,triangle)
        tangent=always_redraw(moving_tangent)
        increasing=self.formula(r'r\uparrow\quad\Longrightarrow\quad\frac{dz}{dr}\uparrow',-4.05,35,CYAN)
        self.add(tangent)
        self.play(walk.animate.set_value(1),Indicate(self.part(slope,'r'),color=CYAN),FadeIn(increasing),run_time=6,rate_func=linear)
        self.mark('tangente_na_borda')
        self.until(119)

        # Integração e desenho compartilham o mesmo ValueTracker.
        self.cue('Integrar a inclinação constrói a curva')
        tangent.clear_updaters()
        self.play(FadeOut(tangent),FadeOut(curve),FadeOut(increasing),run_time=.5)
        growth=ValueTracker(.001)
        growing=always_redraw(lambda:self.path([point(r) for r in np.linspace(0,growth.get_value(),100)],SURFACE,3.7))
        self.add(growing)
        diff=self.glyph([('dz','dz',SURFACE),('eq','=',WHITE),('coef',r'\frac{\omega^2}{g}',WHITE),('r','r',CYAN),('dr','dr',CYAN)],y=-2.6,size=45)
        ids=slope.runs['slope']
        assert len(ids)==5,ids
        self.morph(slope,diff,[(ids[:2],'dz'),('eq','eq'),('coef','coef'),('r','r'),(ids[-2:],'dr')],
                   rt=2,extras=(growth.animate.set_value(.3),))
        integral=self.glyph([('intz',r'\int_{z_0}^{z(r)}',SURFACE),('dz','dz',SURFACE),('eq','=',WHITE),
                             ('coef',r'\frac{\omega^2}{g}',WHITE),('intr',r'\int_0^r',CYAN),('r','s',CYAN),('dr','ds',CYAN)],y=-2.6,size=41)
        self.morph(diff,integral,[('dz','dz'),('eq','eq'),('coef','coef'),('r','r'),('dr','dr')],rt=2.5,
                   extras=(growth.animate.set_value(.65),))
        guide=DashedLine(point(0),[point(1)[0],point(0)[1],0],color=MUTED,stroke_width=1.1)
        z0=self.formula('z(0)=z_0',0,29).next_to(point(0),DOWN+RIGHT,buff=.17)
        self.play(Create(guide),FadeIn(z0),run_time=.5)
        result=self.glyph([('z','z(r)',SURFACE),('eq','=',WHITE),('z0','z_0',WHITE),('plus','+',WHITE),
                           ('coef',r'\frac{\omega^2}{2g}',WHITE),('r2','r^2',CYAN)],y=-2.6,size=47)
        self.morph(integral,result,[('intz',result.runs['z']+result.runs['z0']),('eq','eq'),('coef','coef'),
                                   ('r','r2')],rt=3,extras=(growth.animate.set_value(1),))
        self.mark('parabola_integrada')
        vertex=Dot(point(0),radius=.065,color=WHITE)
        self.play(FadeIn(vertex),run_time=.6)
        self.until(131)
        growing.clear_updaters()
        right=self.path([fullpt(r,f(r)) for r in np.linspace(0,1,100)],SURFACE,3.7)
        self.play(Transform(growing,right),FadeOut(axes),FadeOut(guide),
                  vertex.animate.move_to(fullpt(0,f(0))),z0.animate.next_to(fullpt(0,f(0)),DOWN,buff=.22),run_time=1.2)
        left=self.path([fullpt(-r,f(r)) for r in np.linspace(0,1,100)],SURFACE,3.7)
        self.play(Create(left),run_time=1.4)
        full=self.path([fullpt(r,f(abs(r))) for r in np.linspace(-1,1,181)],SURFACE,3.7)
        self.remove(growing,left)
        self.add(full)
        law=self.formula(r'z-z_0\propto r^2',-1.05,39,CYAN)
        self.play(Write(law),run_time=.7)
        self.mark('secao_espelhada')
        self.until(140)

        # Uma só cadeia: intensidade de pressão -> subida -> tangente -> curva.
        self.cue('Da pressão à forma da superfície')
        self.play(FadeOut(law),FadeOut(result),FadeOut(vertex),FadeOut(z0),FadeOut(full),run_time=.35)
        strip=self.gradient_strip(1.15)
        causal=self.formula(r'\frac{\partial p}{\partial r}>0',-1.05,39,PRESSURE)
        self.play(LaggedStart(*[FadeIn(m) for m in strip],lag_ratio=.08),Write(causal),run_time=.7)
        self.mark('sintese_gradiente')
        rise=Line(fullpt(.82,f(0)),fullpt(.82,f(.82)),color=SURFACE,stroke_width=4)
        iso_final=self.formula(r'p=p_{\rm atm}',-1.05,39,PRESSURE)
        self.play(ReplacementTransform(strip,rise),TransformMatchingTex(causal,iso_final),run_time=1)
        self.mark('sintese_subida')
        walk2=ValueTracker(.06)
        def causal_tangent():
            r=walk2.get_value()
            pivot=fullpt(r,f(r))
            direction=np.array([2.85,2.2*1.9*r,0])
            direction/=np.linalg.norm(direction)
            return VGroup(Line(pivot-.55*direction,pivot+.55*direction,color=WHITE,stroke_width=3),
                          Dot(pivot,radius=.07,color=WHITE))
        causal_tan=always_redraw(causal_tangent)
        tangent_seed=causal_tangent()
        proportional=self.formula(r'\frac{dz}{dr}\propto r',-1.05,39,CYAN)
        self.play(ReplacementTransform(rise,tangent_seed),TransformMatchingTex(iso_final,proportional),run_time=.8)
        self.remove(tangent_seed)
        self.add(causal_tan)
        trail=always_redraw(lambda:self.path([fullpt(r,f(r)) for r in np.linspace(0,walk2.get_value(),100)],SURFACE,3.7))
        self.add(trail)
        self.play(walk2.animate.set_value(1),run_time=2,rate_func=linear)
        self.mark('sintese_tangente')
        trail.clear_updaters()
        causal_tan.clear_updaters()
        quadratic=self.formula(r'z-z_0\propto r^2',-1.05,39,CYAN)
        causal_left=left.copy()
        self.play(TransformMatchingTex(proportional,quadratic),FadeOut(causal_tan),Create(causal_left),run_time=.8)
        self.mark('sintese_parabola')
        # Substitui as duas metades pelo perfil único que fará match com o 3D.
        self.remove(trail,causal_left)
        self.add(full)
        self.until(148.4)
        self.play(FadeOut(quadratic),run_time=.35)
        self.mark('sintese_causal')
        self.until(149)

        # D — match exato com a meridiana branca; revela volume/grid e paralaxe real.
        self.cue('Da seção meridiana ao paraboloide')
        self.mark('payoff_match')
        # Reserva espaço real para a medição junto da borda, sem cortar a fórmula.
        payoff_point=lambda q:.88*np.array(q)+.65*LEFT
        target=self.path([payoff_point(q) for q in p3['curva']],WHITE,3.7)
        payoff_axis=DashedLine(*[payoff_point(q) for q in p3['eixo']],color=CYAN,stroke_width=1.3).set_opacity(.6)
        self.play(Transform(full,target),Create(payoff_axis),run_time=1.2)
        cache=json.loads((UNIT/'cache_3d_v2.json').read_text(encoding='utf-8'))
        # Usa o leitor de PNGs da ponte; sequência editorial de ciclo único, local à unidade.
        reader=Solido3D('liquido_rotacao',params=SECAO,animado=False,res=RES,amostras=AMOSTRAS,render='nunca')
        reader.seq=ponte.Sequencia('liquido_rotacao',Path(cache['payoff']),cache['meta']['frames'],True,RES,True)
        reader.unico=True
        movie=reader.mobject(cena=self,altura=ALTURA_IMAGEM,centro=np.array(CENTRO_IMAGEM),autoplay=False)
        movie.scale(.88,about_point=ORIGIN).shift(.65*LEFT)
        self.add(movie)
        self.remove(full)
        reveal=ValueTracker(0)
        movie.add_updater(lambda m:m.set_fase(reveal.get_value()))
        self.play(reveal.animate.set_value(1),FadeOut(payoff_axis),run_time=4,rate_func=linear)
        movie.clear_updaters()
        ends=[payoff_point(q) for q in projection['final']['delta']]
        bx=max(q[0] for q in ends)+.18
        low,high=ends[0][1],ends[1][1]
        height=VGroup(Line([bx,low,0],[bx,high,0],color=WHITE,stroke_width=2.3),
                      Line([bx-.11,low,0],[bx+.11,low,0],color=WHITE,stroke_width=2.3),
                      Line([bx-.11,high,0],[bx+.11,high,0],color=WHITE,stroke_width=2.3))
        guides=VGroup(*[DashedLine(q,[bx,q[1],0],color=WHITE,stroke_width=1.2) for q in ends])
        final_curve=projection['final']['curva']
        center=payoff_point(final_curve[len(final_curve)//2])
        guides.add(DashedLine(center,ends[0],color=WHITE,stroke_width=1.1).set_opacity(.5))
        delta=MathTex(r'\begin{gathered}\Delta h\\=z(R)-z(0)\\=\frac{\omega^2R^2}{2g}\end{gathered}',font_size=31)
        delta.scale_to_fit_width(1.9).next_to(height,RIGHT,buff=.13).set_z_index(30)
        assert delta.get_right()[0]<4.35,delta.get_right()
        self.play(Create(height),Create(guides),Write(delta),run_time=1)
        self.mark('delta_h')
        self.cue('A pressão fornece a força centrípeta')
        self.wait(.6)
        self.cue('A superfície se inclina para continuar isobárica')
        conclusion=self.formula(r'\frac{dz}{dr}\propto r\quad\Longrightarrow\quad z-z_0\propto r^2',-3.25,36,CYAN)
        self.play(Write(conclusion),run_time=.8)
        closing=self.text('A FORMA É CONSEQUÊNCIA\nDA DINÂMICA.',-5.05,28)
        self.play(FadeIn(closing),run_time=.6)
        self.mark('conclusao')
        self.until(164)

        # Encerramento com logo real e identificador; sem nova etapa de produção.
        self.play(*[FadeOut(m) for m in [movie,delta,height,guides,conclusion,closing,self.caption,self.header,self.logo]],run_time=.7)
        endlogo=ImageMobject(str(WATERMARK_PATH)).set_width(4.6).move_to([0,1,0])
        handle=self.text('@labparallax',-.65,33,CYAN)
        self.play(FadeIn(endlogo),FadeIn(handle),run_time=.8)
        self.mark('branding')
        self.until(168)
        (UNIT/'marcos_v3.json').write_text(json.dumps(dict(duracao=round(self.time,3),eventos=self.events,
            mapas_mf_tools=self.maps),indent=2,ensure_ascii=False),encoding='utf-8')
