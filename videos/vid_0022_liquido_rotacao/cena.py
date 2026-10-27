"""VID22 — preview silencioso. Física/storyboard do handoff de Produção.

uv run python -m manim -r 540,960 --fps 15 videos/vid_0022_liquido_rotacao/cena.py LiquidoRotacao022
Preparar antes com preparar_3d.py. O render nunca dispara Blender implicitamente.
"""
import json
import sys
from pathlib import Path

import numpy as np
from manim import *

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(UNIT))
sys.path.insert(0, str(ROOT / 'experimentos/blender/arsenal'))
from template.config import BACKGROUND_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text
from manim_solido3d import Solido3D
from configuracao_3d import SEQUENCIAS, RES, AMOSTRAS, ALTURA_IMAGEM, CENTRO_IMAGEM

config.media_dir = str(UNIT/'media')
config.background_color = BACKGROUND_COLOR
BLUE = '#267BFF'
LIGHT = '#7FB2FF'
MUTED = '#8492AE'
VIOLET = '#745CFF'


class LiquidoRotacao022(Scene):
    def words(self, text, y, size=28, color=TEXT_COLOR, x=0, width=7.5):
        m = screen_text(text, font_size=size, color=color, oversample=2 if size>=25 else 4)
        if m.width > width:
            m.scale_to_fit_width(width)
        return m.move_to([x,y,0])

    def eq(self, *tex, y=-1.5, size=40, color=TEXT_COLOR, x=0, width=7.5):
        m = MathTex(*tex, font_size=size, color=color)
        if m.width > width:
            m.scale_to_fit_width(width)
        return m.move_to([x,y,0])

    def change(self, old, *tex, y=None, size=40):
        new = self.eq(*tex, y=old.get_y() if y is None else y, size=size)
        self.play(TransformMatchingTex(old,new), run_time=1.2)
        return new

    def until(self, t):
        if self.time > t+0.1:
            raise RuntimeError(f'Marco {t}s excedido: {self.time:.2f}s')
        if t-self.time > 0.001:
            self.wait(t-self.time)

    def heading(self, text, subtitle=None):
        new = self.words(text,6.3,33)
        anim = [FadeOut(self.title),FadeIn(new)]
        if self.subtitle is not None:
            anim.append(FadeOut(self.subtitle))
        sub = self.words(subtitle,5.45,24,MUTED) if subtitle else None
        if sub is not None:
            anim.append(FadeIn(sub))
        self.play(*anim,run_time=0.7)
        self.title,self.subtitle = new,sub

    def strike(self, mob):
        return Line(mob.get_corner(DL)+0.03*LEFT,mob.get_corner(UR)+0.03*RIGHT,color=LIGHT,stroke_width=2.5)

    def asset(self, nome, fase=0):
        source = Solido3D('liquido_rotacao',res=RES,amostras=AMOSTRAS,render='nunca',**SEQUENCIAS[nome])
        image = source.mobject(cena=self,altura=ALTURA_IMAGEM,centro=np.array(CENTRO_IMAGEM),autoplay=False,fase=fase)
        return source,image

    def track_image(self, image, phase):
        image.add_updater(lambda m: m.set_fase(phase.get_value()))

    def graph(self):
        # Coordenadas normalizadas apenas para desenho; nenhum exemplo numérico na tela.
        axes = Axes(x_range=[0,1.12,1],y_range=[0,1.85,1],x_length=5.7,y_length=3.65,
                    tips=True,axis_config=dict(color=MUTED,stroke_width=1.6,include_ticks=False,
                                              tip_width=0.12,tip_height=0.14))
        axes.move_to([0.0,2.6,0])
        f = lambda r: 0.58+0.94*r*r
        curve = axes.plot(f,x_range=[0,1,0.015],color=LIGHT,stroke_width=3.7)
        labels = VGroup(self.eq('r',y=0,size=29).next_to(axes.x_axis.get_end(),RIGHT,buff=0.15),
                        self.eq('z',y=0,size=29).next_to(axes.y_axis.get_end(),UP,buff=0.12))
        origin = self.eq('0',size=24).next_to(axes.c2p(0,0),DL,buff=0.13)
        radial = self.eq(r'r\ge0',y=0.05,size=26,x=2.5,color=MUTED)
        wall = Line(axes.c2p(1,0),axes.c2p(1,1.7),color=BLUE,stroke_width=2.2)
        water_pts = [axes.c2p(0,0),axes.c2p(1,0)] + [axes.c2p(r,f(r)) for r in np.linspace(1,0,65)]
        water = Polygon(*water_pts,fill_color=BLUE,fill_opacity=0.12,stroke_width=0)
        return axes,f,curve,VGroup(axes,labels,origin,radial,wall,water)

    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        brand = self.words('POR TRÁS DA FÓRMULA  •  22',7.35,18,MUTED)
        watermark = ImageMobject(str(WATERMARK_PATH)).scale_to_fit_width(1.5).set_opacity(0.32).move_to([3.1,-7.3,0])
        self.add(brand,watermark)
        self.title = self.words('Por que a superfície de um\nlíquido girando vira uma parábola?',6.3,30)
        self.subtitle = None
        self.add(self.title)

        # 0–14: mesmo setor angular, fase contínua; λ só percorre a metade crescente do morph.
        _,plano = self.asset('plano')
        self.play(FadeIn(plano),run_time=1)
        self.until(2)
        phase = ValueTracker(0)
        self.track_image(plano,phase)
        rotation_label = self.eq(r'\omega',y=-3.5,size=40)
        self.play(FadeIn(rotation_label),phase.animate.set_value(1/12),run_time=1,rate_func=linear)
        self.play(phase.animate.set_value(1/6),run_time=1,rate_func=linear)
        stable = self.words('após estabilizar',-4.55,27)
        self.play(FadeIn(stable),phase.animate.set_value(0.25),run_time=1,rate_func=linear)
        plano.clear_updaters()
        self.remove(plano)
        _,morph = self.asset('morph')
        self.add(morph)
        mp = ValueTracker(0)
        self.track_image(morph,mp)
        self.play(mp.animate.set_value(0.5),run_time=6,rate_func=linear)
        morph.clear_updaters()
        self.remove(morph)
        _,final = self.asset('final',fase=0.75)
        fp = ValueTracker(0.75)
        self.add(final)
        self.track_image(final,fp)
        self.play(fp.animate.set_value(1),run_time=3,rate_func=linear)

        # 14–30: raio positivo para fora; aceleração centrípeta no referencial inercial.
        final.clear_updaters()
        self.play(FadeOut(final),FadeOut(stable),FadeOut(rotation_label),run_time=0.6)
        self.heading('Girar exige aceleração','Seção vertical • referencial inercial')
        axes,f,curve,diagram = self.graph()
        self.play(FadeIn(diagram),Create(curve),run_time=1.2)
        r=0.72
        point=axes.c2p(r,0.75)
        element=Square(side_length=0.23,color=TEXT_COLOR,fill_color=LIGHT,fill_opacity=0.6).move_to(point)
        radius=DoubleArrow(axes.c2p(0,0.3),axes.c2p(r,0.3),buff=0,color=MUTED,stroke_width=2,tip_length=0.12)
        rlabel=self.eq('r',size=27).next_to(radius,DOWN,buff=0.12)
        self.play(FadeIn(element),GrowArrow(radius),FadeIn(rlabel),run_time=1)
        velocity=self.eq(r'v=\omega r',y=-1.55,size=43)
        self.play(Write(velocity),run_time=1.2)
        acceleration=Arrow(point+0.05*LEFT,point+1.6*LEFT,color=TEXT_COLOR,buff=0,stroke_width=4)
        ar=self.eq(r'a_r=-\omega^2r',y=-3.1,size=44)
        out=Arrow(axes.c2p(0,0)+0.4*UP,axes.c2p(0.25,0)+0.4*UP,buff=0,color=LIGHT,stroke_width=2)
        plus=self.eq('+r',size=27,color=LIGHT).next_to(out,UP,buff=0.12)
        self.play(GrowArrow(acceleration),Write(ar),FadeIn(out),FadeIn(plus),run_time=1.5)
        inward=self.words('A aceleração aponta para o eixo.',-4.7,27)
        self.play(FadeIn(inward),run_time=0.6)
        self.until(30)

        # 30–58: faces de um elemento local; pressão interna para +r, externa maior para −r.
        self.play(*[FadeOut(m) for m in [diagram,curve,element,radius,rlabel,velocity,acceleration,ar,out,plus,inward]],run_time=0.6)
        self.heading('Duas faces, duas forças','Elemento local pequeno • faces planas')
        cell=Rectangle(width=1.45,height=1.3,stroke_color=BLUE,fill_color=BLUE,fill_opacity=0.16).move_to([0,2.6,0])
        leftface=Line(cell.get_corner(DL),cell.get_corner(UL),color=LIGHT,stroke_width=5)
        rightface=Line(cell.get_corner(DR),cell.get_corner(UR),color=LIGHT,stroke_width=5)
        force_in=Arrow([-2.35,2.6,0],[-0.76,2.6,0],buff=0,color=TEXT_COLOR,stroke_width=4.5)
        force_out=Arrow([2.75,2.6,0],[0.76,2.6,0],buff=0,color=TEXT_COLOR,stroke_width=4.5)
        li=self.eq(r'p(r)A',y=3.45,x=-2.0,size=31,width=2.8)
        lo=self.eq(r'p(r+dr)A',y=3.45,x=2.0,size=31,width=3.0)
        area=self.eq('A',y=2.75,size=29,color=LIGHT)
        dr=DoubleArrow([-0.725,1.6,0],[0.725,1.6,0],buff=0,color=MUTED,stroke_width=2,tip_length=0.11)
        drtext=self.eq(r'dr',size=28).next_to(dr,DOWN,buff=0.14)
        positive=Arrow([-3.1,4.4,0],[-1.9,4.4,0],buff=0,color=MUTED,stroke_width=2)
        positive_label=self.eq('+r',size=27).next_to(positive,UP,buff=0.12)
        local=VGroup(cell,leftface,rightface,force_in,force_out,li,lo,area,dr,drtext,positive,positive_label)
        self.play(FadeIn(cell),Create(leftface),Create(rightface),FadeIn(area),GrowArrow(dr),FadeIn(drtext),
                  GrowArrow(positive),FadeIn(positive_label),run_time=1.2)
        self.play(GrowArrow(force_in),FadeIn(li),run_time=1)
        self.play(GrowArrow(force_out),FadeIn(lo),run_time=1)
        mass=self.eq(r'dm=\rho A\,dr',y=-0.15,size=37)
        self.play(Write(mass),run_time=1)
        self.until(40)
        force=self.eq('F_r','=',r'p(r)A','-',r'p(r+dr)A',y=-1.8,size=40)
        self.play(Write(force),run_time=1.4)
        self.until(44)
        taylor=self.eq(r'p(r+dr)\approx p(r)+\frac{\partial p}{\partial r}\,dr',y=-3.5,size=36)
        self.play(Write(taylor),run_time=1.7)
        self.until(49)
        self.play(FadeOut(taylor),mass.animate.move_to([0,-4.85,0]),run_time=0.7)
        expanded=self.eq('F_r',r'\approx',r'p(r)A','-',r'p(r)A','-',r'\frac{\partial p}{\partial r}A\,dr',y=-1.8,size=38)
        self.play(TransformMatchingTex(force,expanded),run_time=1.3)
        cancels=VGroup(self.strike(expanded[2]),self.strike(expanded[4]))
        self.play(Create(cancels),run_time=0.8)
        self.wait(1)
        self.play(FadeOut(cancels),run_time=0.3)
        force=self.change(expanded,r'F_r\approx-\frac{\partial p}{\partial r}A\,dr',size=42)
        self.until(58)

        # 58–75: Newton e cancelamentos explícitos, inclusive os dois sinais negativos.
        self.heading('A força resultante é centrípeta')
        self.play(FadeOut(force),FadeOut(mass),run_time=0.5)
        newton=self.eq('-',r'\frac{\partial p}{\partial r}','A',r'dr','=','-',r'\rho','A',r'dr',r'\omega^2r',y=-1.4,size=40)
        self.play(Write(newton),run_time=1.5)
        self.wait(2)
        cuts=VGroup(*[self.strike(newton[i]) for i in [0,2,3,5,7,8]])
        self.play(Create(cuts),run_time=1)
        self.wait(1)
        self.play(FadeOut(cuts),run_time=0.3)
        radial_gradient=self.change(newton,r'\frac{\partial p}{\partial r}=\rho\omega^2r',size=44)
        sign=self.eq(r'\frac{\partial p}{\partial r}>0',y=-3.3,size=42,color=LIGHT)
        interpretation=self.words('Na mesma altura,\na pressão aumenta para fora.',-4.8,27)
        self.play(Write(sign),FadeIn(interpretation),rightface.animate.set_stroke(width=7),run_time=1.2)
        self.until(75)

        # 75–91: balanço vertical curto, a_z=0; a área agora é normal a z.
        self.play(*[FadeOut(m) for m in [local,radial_gradient,sign,interpretation]],run_time=0.6)
        self.heading('Na vertical, equilíbrio','A pressão equilibra o peso')
        vcell=Rectangle(width=1.3,height=1.35,color=BLUE,fill_color=BLUE,fill_opacity=0.16).move_to([0,2.6,0])
        bot=Arrow([0,0.5,0],[0,1.89,0],buff=0,color=TEXT_COLOR,stroke_width=4)
        top=Arrow([0,4.65,0],[0,3.31,0],buff=0,color=TEXT_COLOR,stroke_width=4)
        weight=Arrow([1.25,3.0,0],[1.25,1.9,0],buff=0,color=TEXT_COLOR,stroke_width=3)
        vb=self.eq(r'p(z)A',y=1.15,x=-1.6,size=29,width=2.8)
        vt=self.eq(r'p(z+dz)A',y=4.1,x=-1.65,size=29,width=3.0)
        vg=self.eq(r'dm\,g',y=2.45,x=2.35,size=29,width=2.0)
        zdirection=Arrow([-3,1.8,0],[-3,3.7,0],buff=0,color=MUTED,stroke_width=2)
        zlabel=self.eq('+z',size=27).next_to(zdirection,UP,buff=0.12)
        vertical=VGroup(vcell,bot,top,weight,vb,vt,vg,zdirection,zlabel)
        self.play(FadeIn(vcell),GrowArrow(bot),GrowArrow(top),GrowArrow(weight),FadeIn(vb),FadeIn(vt),FadeIn(vg),
                  GrowArrow(zdirection),FadeIn(zlabel),run_time=1.2)
        balance=self.eq(r'p(z)A-p(z+dz)A-dm\,g=0',y=-1.1,size=36)
        self.play(Write(balance),run_time=1.2)
        self.wait(1.5)
        balance=self.change(balance,r'-\frac{\partial p}{\partial z}A\,dz-\rho A\,dz\,g=0',size=38)
        self.wait(1.8)
        hydro=self.change(balance,r'\frac{\partial p}{\partial z}=-\rho g',size=46)
        self.until(91)

        # 91–117: isobárica e regra da cadeia, sem pular a derivada total.
        self.play(FadeOut(vertical),FadeOut(hydro),run_time=0.6)
        self.heading('Uma superfície, uma pressão','A superfície livre é isobárica')
        axes,f,curve,diagram=self.graph()
        self.play(FadeIn(diagram),Create(curve),run_time=1.2)
        surface_dots=VGroup(*[Dot(axes.c2p(r,f(r)),radius=0.065,color=TEXT_COLOR) for r in [0.16,0.51,0.86]])
        patm_labels=VGroup(*[self.eq(r'p_{\rm atm}',size=25).next_to(dot,UP,buff=0.22) for dot in surface_dots])
        self.play(FadeIn(surface_dots),FadeIn(patm_labels),run_time=1)
        iso=self.eq(r'p(r,z(r))=p_{\rm atm}',y=-1.0,size=43)
        self.play(Write(iso),run_time=1.4)
        self.until(101)
        total=self.eq(r'0=\frac{d}{dr}p(r,z(r))',y=-2.65,size=43)
        self.play(Write(total),run_time=1.5)
        self.until(107)
        chain=self.eq(r'=\frac{\partial p}{\partial r}+\frac{\partial p}{\partial z}\frac{dz}{dr}',y=-4.2,size=43)
        self.play(Write(chain),run_time=2)
        self.until(117)

        # 117–136: substituir os dois gradientes e cancelar a densidade.
        self.heading('A inclinação cresce com o raio')
        self.play(FadeOut(iso),FadeOut(total),FadeOut(surface_dots),FadeOut(patm_labels),run_time=0.6)
        sub=self.eq('0','=',r'\rho',r'\omega^2r','-',r'\rho','g',r'\frac{dz}{dr}',y=-1.7,size=43)
        self.play(TransformMatchingTex(chain,sub),run_time=1.2)
        rho_cuts=VGroup(self.strike(sub[2]),self.strike(sub[5]))
        self.play(Create(rho_cuts),run_time=0.8)
        self.wait(1)
        self.play(FadeOut(rho_cuts),run_time=0.3)
        slope=self.change(sub,r'\frac{dz}{dr}=\frac{\omega^2r}{g}',size=48)
        r_tangent=ValueTracker(0.15)
        def tangent():
            r=r_tangent.get_value()
            p=axes.c2p(r,f(r))
            direction=axes.c2p(r+0.12,f(r)+1.88*r*0.12)-p
            direction=direction/np.linalg.norm(direction)
            return VGroup(Line(p-0.55*direction,p+0.55*direction,color=TEXT_COLOR,stroke_width=3),Dot(p,radius=0.06,color=TEXT_COLOR))
        tan=always_redraw(tangent)
        self.add(tan)
        note=self.words('Quanto maior r,\nmaior a inclinação.',-4.4,29)
        self.play(FadeIn(note),r_tangent.animate.set_value(0.95),run_time=5,rate_func=linear)
        self.until(136)

        # 136–156: integração somente com r>=0; z0 é o centro do estado FINAL.
        self.play(FadeOut(tan),FadeOut(note),FadeOut(curve),run_time=0.6)
        tan.clear_updaters()
        self.heading('Integrando a inclinação')
        differential=self.change(slope,r'dz=\frac{\omega^2}{g}\,r\,dr',y=-1.2,size=44)
        integral=self.eq(r'\int_{z_0}^{z(r)} dz=\frac{\omega^2}{g}\int_0^r s\,ds',y=-2.8,size=40)
        self.play(Write(integral),run_time=1.7)
        center_guide=DashedLine(axes.c2p(0,0.58),axes.c2p(1,0.58),color=MUTED,stroke_width=1.3)
        z0=self.eq('z_0',size=28).next_to(axes.c2p(0,0.58),LEFT,buff=0.15)
        self.play(Create(center_guide),FadeIn(z0),Create(curve),run_time=2)
        self.play(FadeOut(differential),run_time=0.4)
        result=self.change(integral,r'z(r)=z_0+\frac{\omega^2r^2}{2g}',y=-1.7,size=46)
        center_note=VGroup(self.eq('z_0',size=28),self.words('é a altura no eixo, no estado final.',0,25))
        center_note.arrange(RIGHT,buff=0.14)
        if center_note.width>7.5:
            center_note.scale_to_fit_width(7.5)
        center_note.move_to([0,-3.5,0])
        square_law=self.eq(r'z-z_0\propto r^2',y=-4.8,size=42,color=LIGHT)
        self.play(FadeIn(center_note),Write(square_law),run_time=1)
        self.until(151)
        # Só agora introduzir a outra metade: r continua a denotar distância ao eixo.
        origin=np.array([0,1.25,0])
        pt=lambda x,z:origin+np.array([2.8*x,1.8*z,0])
        half=VMobject(stroke_color=LIGHT,stroke_width=3.7).set_points_as_corners([pt(r,f(r)) for r in np.linspace(0,1,65)])
        right_axis=Arrow(origin,origin+3.25*RIGHT,color=MUTED,stroke_width=1.5,buff=0,tip_length=0.12)
        z_axis=Arrow(origin,origin+3.35*UP,color=MUTED,stroke_width=1.5,buff=0,tip_length=0.12)
        final_axes=VGroup(right_axis,z_axis,self.eq('r',size=28).next_to(right_axis,RIGHT,buff=0.12),
                          self.eq('z',size=28).next_to(z_axis,UP,buff=0.1))
        self.play(FadeOut(diagram),FadeOut(center_guide),FadeOut(z0),Transform(curve,half),FadeIn(final_axes),run_time=1.2)
        mirror=VMobject(stroke_color=LIGHT,stroke_width=3.7).set_points_as_corners([pt(-r,f(r)) for r in np.linspace(0,1,65)])
        self.play(Create(mirror),run_time=1.5)
        full=VMobject(stroke_color=LIGHT,stroke_width=3.7).set_points_as_corners([pt(x,f(abs(x))) for x in np.linspace(-1,1,129)])
        self.remove(curve,mirror)
        self.add(full)
        self.until(156)

        # 156–174: correspondência explícita com a seção projetada do asset; revelar o volume.
        self.heading('Da parábola ao paraboloide')
        self.play(FadeOut(final_axes),FadeOut(center_note),FadeOut(square_law),run_time=0.5)
        projection=json.loads((UNIT/'projecao_3d.json').read_text(encoding='utf-8'))
        target=VMobject(stroke_color=TEXT_COLOR,stroke_width=3.2).set_points_as_corners(projection['curva'])
        self.play(Transform(full,target),result.animate.move_to([0,-3.1,0]).scale(0.9),run_time=2)
        _,geo=self.asset('geometria')
        self.add(geo)
        geo.set_opacity(0)
        full.set_z_index(5)
        self.play(geo.animate.set_opacity(1),run_time=2.5)
        self.play(FadeOut(full),run_time=0.4)
        delta=self.eq(r'\Delta h=z(R)-z(0)=\frac{\omega^2R^2}{2g}',y=-3.25,size=40)
        self.play(TransformMatchingTex(result,delta),run_time=1.3)
        endpoints=[np.array(p) for p in projection['delta']]
        height=DoubleArrow(endpoints[0]+0.27*RIGHT,endpoints[1]+0.27*RIGHT,color=TEXT_COLOR,buff=0,
                           stroke_width=2.2,tip_length=0.11)
        height_label=self.eq(r'\Delta h',size=27).next_to(height,RIGHT,buff=0.12)
        self.play(GrowArrow(height),FadeIn(height_label),run_time=0.8)
        closing=self.words('A FORMA É CONSEQUÊNCIA\nDA DINÂMICA.',-5.0,29)
        self.play(FadeIn(closing),run_time=1)
        self.until(174)
        (UNIT/'duracao_preview.json').write_text(json.dumps({'segundos':round(self.time,3),'fps':config.frame_rate,
              'resolucao':[config.pixel_width,config.pixel_height]}),encoding='utf-8')
