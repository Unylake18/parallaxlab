"""yt_0003: V1.5 visual; física e ordem V1.2. Preview silencioso horizontal.

TRECHO=A/B/C/D/E/F seleciona os gates antes do preview completo.
Construção principal inteiramente em Manim, conforme handoff V1.5.
"""
import os
import json
import re
import sys
from pathlib import Path
import numpy as np
from manim import *
from manim.mobject.text.tex_mobject import MathTexPart

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from template.config_horizontal import BACKGROUND_COLOR, PRIMARY_COLOR, WATERMARK_PATH
from template.fonts import screen_text
from MF_Tools import TransformByGlyphMap

# Preserva os intermediários desta unidade para retomar correções localizadas.
config.max_files_cached = 600

E = PRIMARY_COLOR
Q = "#7FB2FF"
GEO = "#9C8CFF"
FLUX = "#D6CCFF"
NORMAL = "#267BFF"
AMBER = "#FFC24D"
MAG = "#EA63FF"
MUTED = "#8A97B5"
CM = {r"\mathbf E": E, r"E_x": E, r"E_y": E, r"E_z": E,
      r"\rho": Q, "q": Q, r"Q_{\rm env}": Q,
      r"\Phi_E": FLUX, r"d\Phi_x": FLUX, r"d\Phi_y": FLUX,
      r"d\Phi_z": FLUX, r"d\Phi": FLUX, r"\Delta V": GEO,
      "dV": GEO, r"\partial V": GEO, r"\mathbf B": MAG,
      "V": GEO, "S": GEO, r"\nabla\cdot": GEO, r"\nabla\times": AMBER}
CM.update({r"d\mathbf A":"#745CFF", "dA":"#745CFF", r"\hat{\mathbf n}":NORMAL})
CM[r"\Phi"]=FLUX
CM[r"\kappa"]=WHITE


def text(s, size=28, color=WHITE, width=13.8):
    # Mesmo cuidado do yt_0001 com o oversampling de títulos longos no Pango.
    old = config.pixel_width
    config.pixel_width = 4000
    try:
        m = screen_text(s, font_size=size, color=color)
    finally:
        config.pixel_width = old
    if m.width > width:
        m.scale_to_fit_width(width)
    return m


def math(s, size=46, pos=ORIGIN, width=13.5):
    # Os marcadores SVG do Manim precisam ficar dentro do argumento TeX.
    s = s.replace("_S", "_{S}").replace("_V", "_{V}")
    s = s.replace(r"\frac q", r"\frac{q}").replace(r"\frac1", r"\frac{1}")
    # Manim 0.21 usa substrings_to_isolate para selecionar glifos por SVG;
    # o matching exige partes Tex reais, criadas pela notação {{ ... }}.
    pattern='|'.join(re.escape(token) for token in sorted(CM,key=len,reverse=True))
    marked=re.sub(pattern,lambda match:' {{ '+match.group(0)+' }} ',s)
    m = MathTex(marked, font_size=size, substrings_to_isolate=list(CM))
    for part in m:
        part.tex_string=part.tex_string.strip()
        if part.tex_string in CM:part.set_color(CM[part.tex_string])
    for token, color in CM.items():
        m.set_color_by_tex(token, color, substring=False)
    if m.width > width:
        m.scale_to_fit_width(width)
    return m.move_to(pos).set_z_index(15)


def vec(a, b, color=E, width=3, opacity=1):
    if np.linalg.norm(np.array(b)-np.array(a))<.025:
        return VMobject()
    return Arrow(a, b, buff=0, color=color, stroke_width=width,
                 max_tip_length_to_length_ratio=.19).set_opacity(opacity)


def charge(p, radius=.16):
    return VGroup(Circle(radius, color=Q, fill_color=BLUE, fill_opacity=.5),
                  text("+", 24, WHITE)).move_to(p).set_z_index(8)


def cube(p, side=2.2, axis=0):
    """Projeção afim de um cubo centrado exatamente em p.

    Ordem: face menos, face mais, arestas, P. A permutação das bases muda
    o eixo examinado sem deslocar o ponto material central.
    """
    p = np.array(p, dtype=float)
    bases = [np.array([1., 0, 0]), np.array([.44, .32, 0]), np.array([0, 1., 0])]
    order = [[0, 1, 2], [1, 0, 2], [2, 1, 0]][axis]
    basis = [bases[i] for i in order]
    def at(i, j, k):
        return p + side / 2 * (i*basis[0]+j*basis[1]+k*basis[2])
    faces = []
    for sign in [-1, 1]:
        faces.append(Polygon(*[at(sign,j,k) for j,k in [(-1,-1),(1,-1),(1,1),(-1,1)]],
                             color=GEO, stroke_width=2, fill_color=GEO, fill_opacity=.17))
    edges = VGroup()
    for i in [-1,1]:
        for j in [-1,1]:
            edges.add(Line(at(i,j,-1),at(i,j,1),color=GEO,stroke_width=1.4))
            edges.add(Line(at(i,-1,j),at(i,1,j),color=GEO,stroke_width=1.4))
            edges.add(Line(at(-1,i,j),at(1,i,j),color=GEO,stroke_width=1.4))
    return VGroup(*faces, edges, Dot(p, radius=.055, color=WHITE)).set_z_index(4)


class DivergenteRotacional(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.live = []
        self.layout_checks=[]
        self.offset = {"A":0, "B":70, "C":155, "D":270, "E":395, "F":590, "K":245}.get(os.getenv("TRECHO"), 0)
        self.atmosphere()
        self.heading = text("DO GLOBAL AO LOCAL", 33).move_to([0,3.4,0])
        self.add(self.heading)
        section = os.getenv("TRECHO", "")
        if section in ("", "A"):
            self.opening(); self.gauss()
        if section in ("", "B"):
            self.divergence()
        if section in ("", "C"):
            self.theorem(); self.local_gauss()
        if section in ("", "K"):
            self.example()
        if section in ("", "D"):
            self.point_delta()
        if section in ("", "E"):
            self.comparison(); self.wheel()
            self.circulation(); self.stokes()
        if section in ("", "F"):
            self.synthesis(); self.coda()
        if os.getenv('QA_LAYOUT')=='1':
            target=Path(__file__).resolve().parent/'renders'/f'qa_layout_{section or "completo"}_v1_5.json'
            target.write_text(json.dumps(self.layout_checks,ensure_ascii=False,indent=2),encoding='utf-8')

    def atmosphere(self):
        # Três planos discretos, sem ocupar a faixa inferior ou competir com E.
        stars = VGroup(*[Dot([((i*3.17)%15)-7.5, ((i*1.71)%7.5)-3.7,0],
                                radius=.008+(i%3)*.003,color=MUTED).set_opacity(.14)
                         for i in range(32)]).set_z_index(-100)
        stars.add_updater(lambda m,dt: m.shift(RIGHT*dt*.003))
        self.add(stars)
        for r in (2.8,3.2,3.8):
            self.add(Circle(r,color=GEO,stroke_width=.7,stroke_opacity=.035)
                     .stretch(.65,1).move_to([-3,0,0]).set_z_index(-101))
        self.add(ImageMobject(str(WATERMARK_PATH)).set_width(1.92).set_opacity(.45)
                 .to_corner(UR,buff=.3))
        self.add(text("ELETROMAGNETISMO",15,MUTED).move_to([-5.85,3.96,0]).set_opacity(.6))
        # y < -3 permanece livre, conforme layout_horizontal.CONTENT_BOTTOM.

    def title(self, s):
        new = text(s,33).move_to(self.heading)
        self.play(Transform(self.heading,new),run_time=.6)

    def show(self, *items, t=.8):
        for m in items:
            if m not in self.live:
                self.live.append(m)
        self.play(*[FadeIn(m) for m in items],run_time=t)
        return items[0] if len(items)==1 else items

    def erase(self, *items, t=.5):
        items = [m for m in items if m in self.live]
        if not items:
            return
        self.play(*[FadeOut(m) for m in items],run_time=t)
        for m in items:
            m.clear_updaters(recursive=True)
            self.remove(m)
            self.live.remove(m)

    def clear(self, keep=()):
        self.erase(*[m for m in self.live if m not in keep])

    def change(self, a, b, t=1.2):
        self.morph(a,b,t)
        if a in self.live:
            self.live.remove(a)
        self.live.append(b)
        return b

    def morph(self,a,b,t=1.2):
        """Matching em três fases: retirar, mover identidades, completar.

        Os termos sem correspondência nunca fazem crossfade sobre o destino.
        Não deforma glifos sem relação matemática em manchas intermediárias.
        """
        def parts(m):
            if isinstance(m,MathTexPart):return [m]
            if isinstance(m,(Group,VGroup)):
                return [p for child in m.submobjects for p in parts(child)]
            return list(TransformMatchingTex.get_mobject_parts(m))
        ap=parts(a);bp=parts(b)
        keys=lambda parts:{m.tex_string for m in parts}
        common=keys(ap)&keys(bp)
        old=[m for m in ap if m.tex_string not in common]
        new=[m for m in bp if m.tex_string not in common]
        am=[m for m in ap if m.tex_string in common]
        bm=[m for m in bp if m.tex_string in common]
        self.remove(a);self.add(*ap)
        if old:self.play(*[FadeOut(m) for m in old],run_time=t*.25)
        if am:
            # Contêiner Tex leve: preserva MathTexPart como unidade do matching,
            # inclusive quando a origem é um termo extraído de outra expressão.
            ac,bc=VMobject(),VMobject()
            ac.tex_string=bc.tex_string=''
            ac.add(*am);bc.add(*bm)
            self.play(TransformMatchingTex(ac,bc),run_time=t*.5)
            self.remove(ac)
        if new:self.play(*[FadeIn(m) for m in new],run_time=t*.25)
        self.remove(*ap,*bp)
        if am:self.remove(ac,bc)
        # Remove os containers temporários criados pelo matching.
        for mob in list(self.mobjects):
            if mob is not b and isinstance(mob,VGroup) and mob.submobjects and all(x in bp for x in mob.submobjects):
                self.remove(mob)
        self.add(b)

    def fly(self, source, target, t=.8):
        # Cópia geométrica indica a proveniência sem mutar os glifos do alvo.
        ghost = source.copy().clear_updaters()
        self.add(ghost)
        self.play(ghost.animate.move_to(target).scale_to_fit_width(max(target.width,.06)),
                  run_time=t)
        self.remove(ghost)
        self.show(target,t=.25)
        return target

    def note(self,s,anchor,pos,color=GEO,size=25):
        label=text(s,size,color,width=6).move_to(pos).set_z_index(18)
        line=Line(anchor,label.get_bottom() if pos[1]>anchor[1] else label.get_top(),
                  color=color,stroke_width=1.1).set_z_index(10)
        n=VGroup(line,Dot(anchor,radius=.035,color=color),label)
        self.show(n)
        return n

    def beat(self, target):
        self.qa_layout(str(target))
        remaining=target-self.offset-self.time
        if remaining>.01:
            self.wait(remaining)

    def qa_layout(self,tag):
        if os.getenv('QA_LAYOUT')!='1':return
        labels=[];geometries=[]
        def visit(m):
            if isinstance(m,(MathTex,Text,Paragraph)):
                if m.width>.6 and m.height>.1:labels.append(m)
                return
            if isinstance(m,VMobject) and m.has_points() and np.max(m.get_stroke_width())>.1 and np.max(m.get_stroke_opacity())>.05:
                geometries.append(m)
            for child in m.submobjects:visit(child)
        for m in self.live:visit(m)
        labels.append(self.heading)
        issues=[]
        def bounds(m,shrink=.035):
            return [float(m.get_left()[0]+shrink),float(m.get_right()[0]-shrink),
                    float(m.get_bottom()[1]+shrink),float(m.get_top()[1]-shrink)]
        def ident(m):return getattr(m,'tex_string',getattr(m,'text',type(m).__name__))
        boxes=[bounds(m) for m in labels]
        for i,(m,box) in enumerate(zip(labels,boxes)):
            if m is not self.heading and (box[0]<-7.2 or box[1]>7.2 or box[2]<-2.95 or box[3]>3.05):
                issues.append({'tipo':'safe_area','objeto':ident(m),'caixa':box})
            for j in range(i):
                b=boxes[j]
                if min(box[1],b[1])-max(box[0],b[0])>.06 and min(box[3],b[3])-max(box[2],b[2])>.06:
                    issues.append({'tipo':'textos','a':ident(m),'b':ident(labels[j])})
            for g in geometries:
                # Amostragem do traço, sem considerar preenchimentos translúcidos.
                if not g.has_points():continue
                pts=[g.point_from_proportion(t) for t in np.linspace(0,1,81)]
                if any(box[0]<p[0]<box[1] and box[2]<p[1]<box[3] for p in pts):
                    issues.append({'tipo':'traco_texto','texto':ident(m),'traco':type(g).__name__})
        self.layout_checks.append({'marco':tag,'tempo_local':float(self.time),'problemas':issues})

    def particles(self, paths, color=E, speed=.2, count=2):
        group=VGroup()
        start=self.time
        for i,path in enumerate(paths):
            for j in range(count):
                dot=Dot(radius=.035,color=color).set_z_index(7)
                phase=(i*.137+j/count)%1
                dot.add_updater(lambda m,dt,p=path,f=phase:
                    m.move_to(p((f+(self.time-start)*speed)%1)))
                group.add(dot)
        return group

    def radial(self, origin, radius=3.2, n=18):
        origin=np.array(origin,dtype=float)
        lines=VGroup()
        paths=[]
        for theta in np.linspace(0,TAU,n,endpoint=False):
            u=np.array([np.cos(theta),np.sin(theta),0.])
            lines.add(Line(origin+.3*u,origin+radius*u,color=E,stroke_opacity=.23,stroke_width=1))
            for r in [.65,1.35,2.35]:
                if r<radius-.25:
                    length=min(.65,.68/r**2)
                    lines.add(vec(origin+r*u,origin+(r+length)*u,width=2,opacity=.65))
            paths.append(lambda a,u=u: origin+(.3+a*(radius-.3))*u)
        return VGroup(lines,self.particles(paths,speed=.11,count=2))

    def flow_cube(self,p,kind=1,extent=1.8):
        p=np.array(p,dtype=float)
        arrows=VGroup(); paths=[]
        if kind==0:
            for y in [-.7,0,.7]:
                a=p+[-extent,y,0]; b=p+[extent,y,0]
                arrows.add(vec(a,b,opacity=.8))
                paths.append(lambda t,a=a,b=b:interpolate(a,b,t))
        else:
            for ang in np.linspace(0,TAU,8,endpoint=False):
                u=np.array([np.cos(ang),np.sin(ang),0])
                a=p+.5*u; b=p+extent*u
                if kind<0:a,b=b,a
                arrows.add(vec(a,b,opacity=.75))
                paths.append(lambda t,a=a,b=b:interpolate(a,b,t))
        return VGroup(arrows,self.particles(paths,speed=.3))


    def opening(self):
        p=np.array([-3.8,.15,0]);self.origin=p
        self.field=self.radial(p,2.45,18);self.q=charge(p)
        self.surface=Circle(2.05,color=GEO,stroke_width=3,fill_color=GEO,fill_opacity=.06).move_to(p)
        self.show(self.field,self.q,t=1);self.show(self.surface,t=1.4)
        theta=.48;u=np.array([np.cos(theta),np.sin(theta),0]);tangent=np.array([-u[1],u[0],0])
        at=p+2.05*u
        patch=Arc(radius=2.05,start_angle=theta-.13,angle=.26,color="#745CFF",stroke_width=9).move_arc_center_to(p)
        self.show(patch)
        label=math("dA",43,[3.1,1.8,0]);self.show(label)
        normal=vec(at+.14*tangent,at+.14*tangent+.65*u,NORMAL,4)
        self.show(normal)
        area=math(r"d\mathbf A=\hat{\mathbf n}\,dA",48,[3.1,.55,0],width=6.5);self.show(area)
        self.beat(9)
        e=vec(at-.14*tangent,at-.14*tangent+.95*u,E,4.5);self.show(e)
        fieldlabel=math(r"\mathbf E",47,[3.1,-.65,0]);self.show(fieldlabel)
        self.beat(13)
        self.erase(label)
        integrand=math(r"\mathbf E\cdot d\mathbf A",58,[3.1,.55,0],width=6.5)
        self.morph(VGroup(area,fieldlabel),integrand,1.5)
        self.live.remove(area);self.live.remove(fieldlabel);self.live.append(integrand)
        self.erase(normal,e)
        patches=VGroup(*[Arc(radius=2.05,start_angle=a-.055,angle=.11,color="#745CFF",stroke_width=5).move_arc_center_to(p)
                          for a in np.linspace(0,TAU,12,endpoint=False)])
        self.play(LaggedStart(*[Create(m) for m in patches],lag_ratio=.13),run_time=3);self.live.append(patches)
        self.beat(21)
        integral=self.change(integrand,math(r"\oint_S\mathbf E\cdot d\mathbf A",59,[3.1,.55,0],width=6.5),t=1.7)
        self.play(LaggedStart(*[Indicate(m,color=FLUX,scale_factor=1.08) for m in patches],lag_ratio=.1),run_time=2)
        self.beat(27)
        self.erase(patch,patches,integral)
        self.field.clear_updaters(recursive=True)
        self.local_cube=cube([2.8,.15,0],1.4)
        local=Dot(at,color=WHITE,radius=.07)
        neighborhood=Circle(.16,color=GEO,stroke_width=2).move_to(at)
        self.show(local,neighborhood,t=.4)
        self.play(self.surface.animate.scale(.55),self.field.animate.scale(.8),
                  local.animate.move_to([2.8,.15,0]),ReplacementTransform(neighborhood,self.local_cube),run_time=2.4)
        self.live.remove(neighborhood);self.live.append(self.local_cube)
        self.beat(35);self.clear(keep=(self.local_cube,))


    def gauss(self):
        self.title("CARGA ENVOLVIDA: DO DISCRETO AO CONTÍNUO")
        self.play(Transform(self.local_cube,cube([-3.8,.15,0],2.3)),run_time=1.2)
        charges=VGroup(*[charge([-3.8+x,.15+y,0],.075) for x,y in [(-.6,-.6),(.5,.6),(.5,-.5),(-.5,.6),(0,0)]])
        self.show(charges)
        qlabel=MathTex(r"Q_{\rm env}",font_size=54,color=Q).move_to([3.1,1.8,0]);self.show(qlabel)
        law=math(r"\oint_S\mathbf E\cdot d\mathbf A=\frac{Q_{\rm env}}{\varepsilon_0}",47,[2.7,.15,0],width=8.1);self.show(law)
        self.beat(43)
        more=VGroup(*[Dot([-3.8+x,.15+y,0],radius=.045,color=Q) for x in np.linspace(-.85,.85,5) for y in np.linspace(-.85,.85,5)])
        self.play(ReplacementTransform(charges,more),run_time=2);self.live.remove(charges);self.live.append(more)
        density=VGroup(*[Dot([-3.8+x,.15+y,0],radius=.023,color=Q) for x in np.linspace(-.9,.9,13) for y in np.linspace(-.9,.9,13)])
        self.play(ReplacementTransform(more,density),run_time=2);self.live.remove(more);self.live.append(density)
        integral=MathTex(r"\int_V\rho\,dV",font_size=54).move_to(qlabel)
        assert len(qlabel[0])==4 and len(integral[0])==5,(len(qlabel[0]),len(integral[0]))
        integral[0][2].set_color(Q)
        for i in [1,4]:integral[0][i].set_color(GEO)
        self.play(TransformByGlyphMap(qlabel,integral,([0],[2]),([1,2,3],[]),([],[0,1,3,4])),run_time=2)
        self.live.remove(qlabel);self.live.append(integral)
        self.beat(52)
        continuum=Polygon([-5,-1.1,0],[-2.6,-1.1,0],[-2.6,1.4,0],[-5,1.4,0],stroke_width=0,fill_color=Q,fill_opacity=.1)
        self.show(continuum)
        law=self.change(law,math(r"\oint_S\mathbf E\cdot d\mathbf A=\frac{1}{\varepsilon_0}\int_V\rho\,dV",48,[2.7,.15,0],width=8.1),t=1.8)
        self.play(Indicate(integral,color=Q),run_time=1)
        self.beat(59)
        self.erase(integral)
        question=text("Como isso vale ponto a ponto?",30,GEO).move_to([2.7,-1.65,0]);self.show(question)
        self.play(density.animate.scale(.22,about_point=[-3.8,.15,0]),continuum.animate.scale(.22,about_point=[-3.8,.15,0]),
                  self.local_cube.animate.scale(.22,about_point=[-3.8,.15,0]),run_time=6,rate_func=linear)
        self.beat(70);self.clear()

    def divergence(self):
        self.clear()
        self.title("FLUXO EM UM CUBO CENTRADO")
        p=np.array([-3.8,.3,0]); self.local_p=p
        axis=vec(p+[-2.5,0,0],p+[2.4,0,0],MUTED,1.5)
        point=Dot(p,radius=.07,color=WHITE)
        center=math("x",40,p+[0,.45,0])
        self.show(axis,point,center)
        guide=text("Primeiro, um intervalo centrado em P",27,GEO).move_to([2.8,1.2,0])
        self.show(guide);self.beat(75)
        segment=Line(p+[-.95,0,0],p+[.95,0,0],color=GEO,stroke_width=5)
        halves=VGroup(BraceBetweenPoints(p+[-.95,-.12,0],p+[0,-.12,0],DOWN,color=GEO),
                      BraceBetweenPoints(p+[0,-.12,0],p+[.95,-.12,0],DOWN,color=GEO))
        half_labels=VGroup(*[math(r"dx/2",32,[x,-.48,0]) for x in [-4.35,-3.25]])
        self.show(segment,halves,half_labels)
        whole=math("dx",47,[2.8,-.15,0]);self.show(whole)
        self.beat(80)
        ends=VGroup(math(r"x-\frac{dx}{2}",36,[-5,-1.55,0]),
                    math(r"x+\frac{dx}{2}",36,[-2.6,-1.55,0]))
        assert all(len(m[0])==4 for m in half_labels) and all(len(m[0])==6 for m in ends)
        half_map=[([0],[2]),([1],[3]),([2],[4]),([3],[5]),([],[0,1])]
        self.play(*[TransformByGlyphMap(half_labels[i],ends[i],*half_map) for i in [0,1]],run_time=1.1)
        self.live.remove(half_labels);self.remove(half_labels);self.add(ends)
        self.live.append(ends)
        self.beat(83)
        self.erase(halves,half_labels,guide,whole,axis,center)
        self.local_cube=cube(p,1.9)
        self.play(ReplacementTransform(segment,self.local_cube),run_time=1.5)
        self.live.remove(segment);self.live.append(self.local_cube);self.erase(point)
        plabel=math("P",30,p+[.18,.25,0]);self.show(plabel)
        self.beat(87)
        # As normais nascem nos centros das faces. Toda a álgebra fica à direita.
        normals=VGroup(vec(p+[-.95,-.25,0],p+[-1.8,-.25,0],NORMAL,4),
                       vec(p+[.95,-.25,0],p+[1.8,-.25,0],NORMAL,4))
        nlabels=VGroup(math(r"-\hat x",33,[-5.6,-.5,0]).set_color(NORMAL),
                       math(r"+\hat x",33,[-2,-.5,0]).set_color(NORMAL))
        self.show(normals,nlabels)
        note=text("Normais externas em sentidos opostos",26,NORMAL,width=7.5).move_to([2.9,2.1,0]);self.show(note)
        general=math(r"d\Phi=\mathbf E\cdot d\mathbf A",48,[2.9,.9,0],width=7.5);self.show(general)
        self.beat(92)
        self.erase(note,ends)
        self.play(self.local_cube[1].animate.set_fill(GEO,.45),self.local_cube[0].animate.set_fill(GEO,.04),run_time=.7)
        area=math(r"dA=dy\,dz",40,[2.9,-.3,0]);self.show(area)
        elab=math(r"E_x\left(x+\frac{dx}{2}\right)",39,[-3.8,2.35,0],width=5.5)
        evec=vec(p+[.95,.35,0],p+[2,.35,0],E,4);self.show(evec,elab)
        plus=math(r"d\Phi_{x,+}=E_x\left(x+\frac{dx}{2}\right)dy\,dz",46,[2.9,.9,0],width=7.7)
        self.play(elab.animate.move_to([2.9,2.35,0]),run_time=.6)
        self.morph(VGroup(general,elab),plus,1.2)
        self.live.remove(elab);self.live.remove(general);self.live.append(plus);general=plus
        self.play(Indicate(area,color=GEO),Indicate(self.local_cube[1],color=GEO),run_time=.8)
        self.beat(99)
        self.erase(area,evec,elab)
        # Memória da face direita: descer pela coluna livre, depois recuar sob o cubo.
        self.play(general.animate.move_to([2.9,-2,0]).scale_to_fit_width(6.3),run_time=.6)
        self.play(general.animate.move_to([-3.8,-2,0]),self.local_cube[0].animate.set_fill(GEO,.45),
                  self.local_cube[1].animate.set_fill(GEO,.04),run_time=.6)
        elab=math(r"E_x\left(x-\frac{dx}{2}\right)",39,[-3.8,2.35,0],width=5.5)
        evec=vec(p+[-1.8,.35,0],p+[-.95,.35,0],E,4);self.show(elab,evec)
        minus=math(r"d\Phi_{x,-}=-E_x\left(x-\frac{dx}{2}\right)dy\,dz",46,[2.9,.6,0],width=7.7)
        self.play(elab.animate.move_to([2.9,2.35,0]),run_time=.6)
        self.morph(elab,minus,1.2)
        self.live.remove(elab);self.live.append(minus);self.play(Indicate(normals[0],color=NORMAL),run_time=.7)
        self.beat(105)
        self.erase(elab,evec,normals,nlabels,plabel)
        net=math(r"d\Phi_x=\left[E_x\left(x+\frac{dx}{2}\right)-E_x\left(x-\frac{dx}{2}\right)\right]dy\,dz",47,[0,-2,0],width=13.5)
        # As duas expressões saem de suas faixas antes de se unir: sem alvos duplicados.
        joined=VGroup(general,minus)
        self.morph(joined,net,1.6)
        self.live.remove(general);self.live.remove(minus);self.live.append(net)
        self.beat(110)
        ratio=math(r"\frac{E_x(x+dx/2)-E_x(x-dx/2)}{dx}",48,[2.9,.8,0],width=7.5)
        source=VGroup(*[part.copy() for part in net if part.tex_string==r"E_x"])
        self.morph(source,ratio,1.2);self.live.append(ratio)
        shrinking=math(r"dx\downarrow",37,[2.9,-.65,0]);self.show(shrinking)
        self.play(self.local_cube.animate.scale(.38,about_point=p),run_time=3)
        self.beat(117)
        ratio=self.change(ratio,math(r"\frac{\partial E_x}{\partial x}",62,[2.9,.8,0]),t=1.6)
        net=self.change(net,math(r"d\Phi_x\approx\frac{\partial E_x}{\partial x}\,dx\,dy\,dz",50,[0,-2,0]))
        self.erase(shrinking,ratio)
        dv=math(r"dV=dx\,dy\,dz",44,[2.9,.7,0]);self.show(dv)
        self.beat(123)
        self.erase(dv)
        net=self.change(net,math(r"d\Phi_x=\frac{\partial E_x}{\partial x}dV",51,[2.9,.7,0]))
        chips=[]
        for index,(symbol,xpos) in enumerate(zip('xyz',[-4,0,4])):
            if index:
                self.play(Transform(self.local_cube,cube(p,.95,index)),run_time=.7)
                net=self.change(net,math(r"d\Phi_"+symbol+r"=\frac{\partial E_"+symbol+r"}{\partial "+symbol+r"}dV",51,[2.9,.7,0]),t=.8)
            chip=math(r"\frac{\partial E_"+symbol+r"}{\partial "+symbol+"}",45,[xpos,-1.8,0])
            source=next(part for part in net if part.tex_string==r"E_"+symbol).copy()
            self.morph(source,chip,.8);self.live.append(chip);chips.append(chip)
            self.beat([127,131,135][index])
        self.erase(net)
        self.play(self.local_cube.animate.scale(1.3,about_point=p),run_time=.6)
        summed=math(r"d\Phi=\left(\frac{\partial E_x}{\partial x}+\frac{\partial E_y}{\partial y}+\frac{\partial E_z}{\partial z}\right)dV",48,[2.7,.7,0],width=8.3)
        self.morph(VGroup(*chips),summed,1.3)
        for c in chips:self.live.remove(c)
        self.live.append(summed);self.beat(139)
        definition=self.change(summed,math(r"\nabla\cdot\mathbf E=\frac{\partial E_x}{\partial x}+\frac{\partial E_y}{\partial y}+\frac{\partial E_z}{\partial z}",46,[2.7,.7,0],width=8.3))
        self.title("DIVERGENTE: FLUXO LÍQUIDO POR VOLUME")
        self.beat(142)
        definition=self.change(definition,math(r"\nabla\cdot\mathbf E=\lim_{\Delta V\to0}\frac{1}{\Delta V}\oint_{\partial V}\mathbf E\cdot d\mathbf A",44,[2.5,.7,0],width=8.4))
        self.beat(146)
        self.erase(definition)
        for kind,sign,label,at in [(1,'>','Fluxo líquido saindo',149),(-1,'<','Fluxo líquido entrando',152),(0,'=','Fluxo líquido local nulo',155)]:
            f=self.flow_cube(p,kind,1.6)
            value=math(r"\nabla\cdot\mathbf E"+sign+'0',54,[2.8,.8,0])
            caption=text(label,27,FLUX).move_to([2.8,-.35,0]);self.show(f,value,caption,t=.35)
            if kind==0:
                warning=math(r"\nabla\cdot\mathbf E=0\;\not\Rightarrow\;\mathbf E=0",42,[0,-2.3,0]);self.show(warning,t=.4)
            self.beat(at);self.erase(f,value,caption,t=.2)
        self.clear(keep=(self.local_cube,))


    def theorem(self):
        self.clear();self.title("UMA INTERFACE, DUAS NORMAIS EXTERNAS")
        a=cube([-4.2,.2,0],1.6);b=cube([-2.6,.2,0],1.6)
        self.show(a,b)
        interface=a[1].copy().set_fill(GEO,.5).set_stroke(FLUX,4)
        assert np.allclose(a[1].get_vertices(),b[0].get_vertices())
        self.show(interface)
        ca=np.array([-3.4,.2,0])
        normals=VGroup(vec(ca+[0,.2,0],ca+[.85,.2,0],NORMAL,4),
                       vec(ca+[0,-.2,0],ca+[-.85,-.2,0],NORMAL,4))
        self.show(normals)
        tags=VGroup(math(r"+\hat x",34,[-2.65,1.6,0]).set_color(NORMAL),math(r"-\hat x",34,[-4.2,-1.3,0]).set_color(NORMAL))
        self.show(tags)
        description=text("A mesma face física",29,GEO).move_to([3.3,2.1,0]);self.show(description)
        field=vec([-5.6,.8,0],[-1.4,.8,0],E,4)
        flow=self.particles([lambda t:np.array([-5.6+4.2*t,.8,0])],speed=.22,count=4)
        self.show(field,flow)
        plus=math(r"+\mathbf E\cdot d\mathbf A",46,[3.3,.7,0]);minus=math(r"-\mathbf E\cdot d\mathbf A",46,[3.3,-.7,0]);self.show(plus,minus)
        self.play(Indicate(normals[0],color=NORMAL),Indicate(plus,color=FLUX),run_time=.9)
        self.play(Indicate(normals[1],color=NORMAL),Indicate(minus,color=FLUX),run_time=.9)
        self.beat(168)
        cancellation=MathTex(r"+\Phi-\Phi=0",font_size=56,color=FLUX).move_to([3.3,0,0]);self.morph(VGroup(plus,minus),cancellation,1.6)
        self.live.remove(plus);self.live.remove(minus);self.live.append(cancellation)
        self.play(Indicate(interface,color=FLUX),run_time=.8)
        zero=MathTex('0',font_size=56,color=FLUX).move_to(cancellation)
        assert len(cancellation[0])==6
        self.play(TransformByGlyphMap(cancellation,zero,([5],[0]),([0,1,2,3,4],[])),run_time=1)
        self.live.remove(cancellation);self.live.append(zero)
        self.beat(173)
        self.clear()
        # 2 → 4 → 8 cellules; interfaces da malha coincidem exatamente.
        cells=VGroup()
        for count in [2,4,8]:
            new=VGroup(*[cube([-4.9+(i%4)*1.05,-.55+(i//4)*1.05,0],1.05) for i in range(len(cells),count)])
            self.show(new,t=.8)
            cells.add(*new)
            for cell in new:
                self.play(Indicate(cell[0],color=FLUX,scale_factor=1),run_time=.25)
        self.clear()
        cells=VGroup(*[cube([-4.9+i*1.05,-.55+j*1.05,0],1.05) for j in range(2) for i in range(4)])
        self.show(cells,t=.3)
        interfaces=VGroup(*[cells[j*4+i][1].copy().set_fill(GEO,.3).set_stroke(FLUX,2) for j in range(2) for i in range(3)])
        self.play(LaggedStart(*[ShowPassingFlash(x,time_width=.8) for x in interfaces],lag_ratio=.15),run_time=2.2)
        # Envoltória: soma de Minkowski da malha com a profundidade projetada.
        x0,x1=-5.656,-.994;y0,y1=-1.243,1.193
        hull=Polygon([x0,y0,0],[x1-.462,y0,0],[x1,y0+.336,0],[x1,y1,0],[x0+.462,y1,0],[x0,y1-.336,0],color=FLUX,stroke_width=3.5)
        self.play(cells.animate.set_opacity(.18),Create(hull),run_time=1.2);self.live.append(hull)
        caption=text("INTERIOR → cancela\nFRONTEIRA → permanece",28,FLUX).move_to([3.1,1.3,0]);self.show(caption)
        self.beat(185)
        volume=math(r"\sum_{\rm celulas}(\nabla\cdot\mathbf E)\Delta V",45,[2.7,-.4,0],width=8);self.show(volume)
        volume=self.change(volume,math(r"\int_V\nabla\cdot\mathbf E\,dV",56,[2.9,-.4,0]))
        self.play(Indicate(cells,color=GEO),run_time=.9)
        self.beat(192)
        self.erase(volume)
        surface=math(r"\sum_{\rm faces\ externas}\Phi",49,[2.9,-.4,0],width=7.8);self.show(surface)
        surface=self.change(surface,math(r"\oint_S\mathbf E\cdot d\mathbf A",55,[2.9,-.4,0]))
        self.play(Indicate(hull,color=FLUX),run_time=.9)
        self.beat(199)
        self.erase(surface,caption,cells,hull)
        theorem=math(r"\oint_S\mathbf E\cdot d\mathbf A=\int_V\nabla\cdot\mathbf E\,dV",56,[0,.4,0])
        self.show(theorem);self.beat(205)
        self.clear();self.flux=math(r"\oint_S\mathbf E\cdot d\mathbf A",54,[0,1.3,0]);self.show(self.flux,t=.3)


    def local_gauss(self):
        self.title("O MESMO FLUXO, DUAS LEITURAS")
        tags=VGroup(text("TEOREMA DA DIVERGÊNCIA",24,GEO).move_to([-3.7,2.25,0]),
                    text("LEI DE GAUSS",24,Q).move_to([3.7,2.25,0]));self.show(tags)
        left=math(r"\oint_S\mathbf E\cdot d\mathbf A",43,[-3.7,.5,0],width=6.5)
        right=math(r"\oint_S\mathbf E\cdot d\mathbf A",43,[3.7,.5,0],width=6.5)
        self.play(TransformFromCopy(self.flux,left),TransformFromCopy(self.flux,right),run_time=1.2);self.live.extend([left,right]);self.erase(self.flux)
        left=self.change(left,math(r"\int_V\nabla\cdot\mathbf E\,dV",51,[-3.7,.5,0],width=6.5))
        right=self.change(right,math(r"\frac{1}{\varepsilon_0}\int_V\rho\,dV",51,[3.7,.5,0],width=6.5))
        same=text("Duas leituras da mesma grandeza",28,FLUX).move_to([0,-1.1,0]);self.show(same)
        self.beat(216)
        self.erase(tags,same)
        equality=math(r"\int_V\nabla\cdot\mathbf E\,dV=\int_V\frac{\rho}{\varepsilon_0}dV",55,[0,.9,0])
        self.morph(VGroup(left,right),equality,1.6);self.live.remove(left);self.live.remove(right);self.live.append(equality)
        self.beat(222)
        equality=self.change(equality,math(r"\int_V\left(\nabla\cdot\mathbf E-\frac{\rho}{\varepsilon_0}\right)dV=0",55,[0,.9,0]),t=1.5)
        vol=cube([-3.8,-1.4,0],1.1);self.show(vol)
        note=text("Qualquer volume regular apropriado",27,GEO).move_to([2.1,-1.4,0]);self.show(note)
        self.play(vol.animate.scale(.2,about_point=[-3.8,-1.4,0]),run_time=4)
        self.beat(231)
        self.erase(vol,note)
        equality=self.change(equality,math(r"\nabla\cdot\mathbf E=\frac{\rho}{\varepsilon_0}",76,[0,.6,0]),t=1.6)
        self.title("LEI DE GAUSS — FORMA DIFERENCIAL")
        box=SurroundingRectangle(equality,color=GEO,buff=.3);self.show(box)
        positive=math(r"\rho>0\Rightarrow\nabla\cdot\mathbf E>0",43,[0,-1.2,0]);self.show(positive)
        self.beat(239)
        positive=self.change(positive,math(r"\rho<0\Rightarrow\nabla\cdot\mathbf E<0",43,[0,-1.2,0]))
        self.beat(245);self.clear()


    def example(self):
        self.title("UM CAMPO QUE CRESCE COM A POSIÇÃO")
        base=np.array([-4,.1,0]);progress=ValueTracker(.5)
        arrows=VGroup(*[vec(base+[x,y,0],base+1.25*np.array([x,y,0]),E,2.8,.5) for x in [-1.6,-.8,0,.8,1.6] for y in [-1.4,-.7,0,.7,1.4] if abs(x)+abs(y)>.1])
        probe=always_redraw(lambda:Dot(base+[progress.get_value(),.4,0],radius=.075,color=Q))
        arrow=always_redraw(lambda:vec(base+[progress.get_value(),.4,0],base+1.65*np.array([progress.get_value(),.4,0]),E,5))
        self.show(arrows,probe,arrow)
        formula=math(r"\mathbf E=\kappa(x\hat x+y\hat y+z\hat z)",49,[2.9,1.7,0],width=7.9);self.show(formula)
        grows=math(r"|\mathbf E|\propto r",42,[2.9,.2,0]);self.show(grows)
        self.play(progress.animate.set_value(1.6),run_time=3,rate_func=linear)
        self.erase(grows,arrows,probe,arrow)
        basis=[RIGHT,np.array([.5,.35,0]),UP]
        axes=VGroup(*[vec(base,base+1.8*u,MUTED,2) for u in basis]);self.show(axes)
        axislabels=VGroup(math('x',31,[-1.8,-.25,0]),math('y',31,[-3.6,1.15,0]),math('z',31,[-4.3,2.25,0]));self.show(axislabels,t=.3)
        terms=[]
        for i,sym in enumerate('xyz'):
            probe_axis=Dot(base+.3*basis[i],radius=.07,color=Q)
            field_axis=always_redraw(lambda:vec(probe_axis.get_center(),base+1.55*(probe_axis.get_center()-base),E,4))
            self.show(probe_axis,field_axis,t=.25)
            self.play(probe_axis.animate.move_to(base+1.4*basis[i]),run_time=.9)
            self.play(Indicate(axes[i],color=E),run_time=.4)
            component=math(r"E_"+sym+r"=\kappa "+sym,48,[2.9,.1,0]);self.show(component,t=.3)
            component=self.change(component,math(r"\frac{\partial E_"+sym+r"}{\partial "+sym+r"}=\kappa",48,[2.9,.1,0]),t=.8)
            self.wait(.5)
            term=math(r"\kappa",49,[1.5+1.4*i,-1.3,0])
            kappa=component.get_part_by_tex(r"\kappa")
            assert kappa is not None
            self.play(TransformFromCopy(kappa,term),run_time=.5);self.live.append(term);terms.append(term)
            self.erase(component,probe_axis,field_axis,t=.2)
        summed=MathTex(r"\kappa+\kappa+\kappa",font_size=54).move_to([2.9,-.4,0])
        for i,m in enumerate(terms):
            self.play(ReplacementTransform(m,summed[0][2*i]),run_time=.35)
            self.live.remove(m)
        self.play(Write(summed[0][1]),Write(summed[0][3]),run_time=.35)
        self.remove(*list(summed[0]));self.add(summed)
        self.live.append(summed)
        result=MathTex(r"3\kappa",font_size=54).move_to(summed)
        self.play(TransformByGlyphMap(summed,result,([0],[1]),([1,2,3,4],[]),([],[0])),run_time=1)
        self.live.remove(summed);self.live.append(result)
        label=math(r"\nabla\cdot\mathbf E=",47).next_to(result,LEFT,buff=.2);self.show(label,t=.3)
        self.beat(270);self.clear()


    def point_delta(self):
        self.title("CARGA PONTUAL: FLUXO SEMPRE IGUAL")
        self.origin=np.array([-3.8,.15,0]);self.q=charge(self.origin)
        field=self.radial(self.origin,2.45,24);self.show(field,self.q)
        formula=math(r"\mathbf E=\frac{q}{4\pi\varepsilon_0}\frac{\hat{\mathbf r}}{r^2}",51,[3,1.5,0],width=7.5)
        outside=math(r"\nabla\cdot\mathbf E=0\;(r\ne0)",46,[3,-.1,0],width=7.5);self.show(formula,outside)
        probe=cube([-2,1.5,0],.5);self.show(probe)
        for target,ctrls,at in [([-5.5,1.4,0],([-2.6,2.7,0],[-4.9,2.7,0]),283),
                               ([-5.4,-1.3,0],([-6.3,1.2,0],[-6.3,-1.1,0]),293),
                               ([-2,-1.3,0],([-4.6,-1.7,0],[-2.7,-1.7,0]),303)]:
            path=CubicBezier(probe[3].get_center(),*ctrls,target)
            self.play(MoveAlongPath(probe,path),run_time=6,rate_func=linear)
            self.play(Indicate(outside,color=GEO),Indicate(probe,color=GEO),run_time=.8)
            self.beat(at)
        self.erase(probe,formula)
        self.play(outside.animate.move_to([3,-2.25,0]),run_time=.7)
        radius=ValueTracker(2.1)
        surface=always_redraw(lambda:Circle(radius.get_value(),color=GEO,stroke_width=3,fill_color=GEO,fill_opacity=.045).move_to(self.origin))
        boundary_field=always_redraw(lambda:VGroup(*[vec(self.origin+radius.get_value()*np.array([np.cos(a),np.sin(a),0]),
                  self.origin+(radius.get_value()+min(.72,.13/radius.get_value()**2))*np.array([np.cos(a),np.sin(a),0]),E,4)
                  for a in np.linspace(0,TAU,12,endpoint=False)]))
        self.show(surface,boundary_field)
        flux=math(r"\oint_S\mathbf E\cdot d\mathbf A=\frac{q}{\varepsilon_0}",48,[3,1.6,0],width=7.5);self.show(flux)
        flux=self.change(flux,math(r"\Phi_E=\frac{q}{\varepsilon_0}",61,[3,1.6,0]),t=1.3)
        constant=text("FLUXO CONSTANTE",27,FLUX).move_to([3,.35,0]);self.show(constant)
        bar=Line([1.1,-.35,0],[4.9,-.35,0],color=FLUX,stroke_width=7);self.show(bar)
        rlabel=math(r"R/R_0=",40,[2,-1.25,0])
        value=DecimalNumber(1,num_decimal_places=2,font_size=42,color=GEO).move_to([4.1,-1.25,0])
        value.add_updater(lambda m:m.set_value(radius.get_value()/2.1));self.show(rlabel,value)
        self.beat(310)
        self.play(radius.animate.set_value(.315),run_time=29,rate_func=linear)
        self.erase(rlabel,value,bar,constant,boundary_field)
        question=text("Fora da origem, divergente zero.\nOnde está a fonte?",28,Q,width=7.5).move_to([3,-.45,0]);self.show(question)
        self.beat(345)
        self.title("DELTA: O VOLUME ENCONTRA A ORIGEM")
        self.erase(question,flux,surface,field)
        self.play(outside.animate.scale(.85).move_to([3,2.2,0]),run_time=.5)
        test=Circle(.85,color=GEO,stroke_width=3,fill_color=GEO,fill_opacity=.12).move_to([-1.7,.15,0]);self.show(test)
        integral=math(r"I(V)=0",58,[3,.6,0]);self.show(integral)
        state=text("Origem fora de V",27,GEO).move_to([3,-.6,0]);self.show(state)
        self.beat(350)
        self.play(test.animate.move_to([-2.9,.15,0]),run_time=5,rate_func=linear)
        # O valor na fronteira não é afirmado: ocultar antes de atravessá-la.
        self.erase(integral,state,t=.25)
        self.play(test.animate.move_to([-3.01,.15,0]),run_time=.7,rate_func=linear)
        self.play(Flash(self.q,color=Q,flash_radius=.45),run_time=.6)
        integral=math(r"I(V)=1",58,[3,.6,0]);state=text("Origem no interior de V",27,GEO).move_to([3,-.6,0]);self.show(integral,state,t=.4)
        self.play(test.animate.move_to(self.origin),run_time=3.5,rate_func=linear)
        self.beat(363)
        integral=self.change(integral,math(r"I(V)=\int_V\delta^3(\mathbf r)\,dV=1",48,[3,.6,0],width=7.8),t=1.5)
        delta0=math(r"\delta^3(\mathbf r)=0\;(r\ne0)",42,[3,-1.7,0],width=7.5);self.show(delta0)
        self.beat(369)
        self.erase(integral,state,delta0)
        qlabel=math("q",48,[-3.8,1.6,0]);self.show(qlabel)
        rho=self.change(qlabel,math(r"\rho(\mathbf r)=q\delta^3(\mathbf r)",55,[3,1,0],width=7.8),t=1.7)
        distribution=text("Distribuição: ação em integrais",26,MUTED).move_to([3,-2.2,0]);self.show(distribution)
        gauss=math(r"\nabla\cdot\mathbf E=\frac{\rho}{\varepsilon_0}",57,[3,-.65,0]);self.show(gauss)
        self.beat(380)
        result=math(r"\nabla\cdot\mathbf E=\frac{q}{\varepsilon_0}\delta^3(\mathbf r)",57,[3,.25,0],width=7.8)
        self.morph(VGroup(gauss,rho),result,2);self.live.remove(gauss);self.live.remove(rho);self.live.append(result)
        self.play(test.animate.scale(.32,about_point=self.origin),run_time=5)
        self.beat(389)
        interior=text("Carga concentrada na origem",27,Q).move_to([3,-1.1,0]);self.show(interior)
        self.beat(395);self.clear()

    def vector_field(self,center,rot=False,scale=.65):
        center=np.array(center,dtype=float); arrows=VGroup();paths=[]
        for x in np.linspace(-1.6,1.6,5):
            for y in np.linspace(-1.4,1.4,5):
                v=np.array([-y,x,0])*scale*.43 if rot else np.array([.62,0,0])
                if np.linalg.norm(v)>.04:
                    a=center+[x,y,0];arrows.add(vec(a,a+v,width=2.2,opacity=.75))
        if rot:
            for r in [.6,1.1,1.6]:
                paths.append(lambda t,r=r:center+r*np.array([np.cos(TAU*t),np.sin(TAU*t),0]))
        else:
            for y in [-1.1,0,1.1]:
                paths.append(lambda t,y=y:center+[-1.6+3.2*t,y,0])
        return VGroup(arrows,self.particles(paths,speed=.13,count=3))


    def comparison(self):
        self.title("MESMO DIVERGENTE, OUTRA GEOMETRIA")
        f1=self.vector_field([-3.7,.1,0]);self.show(f1)
        label1=math(r"\mathbf F_1=F_0\hat{\mathbf x}",45,[-3.7,2.3,0]);self.show(label1)
        probe1=cube([-3.7,.1,0],.6);self.show(probe1)
        z1=math(r"\nabla\cdot\mathbf F_1=0",42,[-3.7,-1.9,0]);self.show(z1)
        self.beat(401)
        center=np.array([3.7,.1,0]);blend=ValueTracker(0)
        arrows=always_redraw(lambda:VGroup(*[vec(center+[x,y,0],center+np.array([x,y,0])+.42*((1-blend.get_value())*RIGHT+blend.get_value()*np.array([-y,x,0])),E,2.5,.7)
                    for x in np.linspace(-1.35,1.35,5) for y in np.linspace(-1.05,1.05,5) if abs(x)+abs(y)>.1]))
        dots=VGroup(*[Dot(center+[x,y,0],radius=.035,color=E) for x,y in [(-1.3,-.8),(-.8,.5),(.4,1.2),(.9,-.7),(-.2,-1.2),(1.2,.1)]])
        def advect(m,dt):
            lam=blend.get_value();m.rotate(.75*lam*dt,about_point=center).shift(.65*(1-lam)*dt*RIGHT)
            if np.linalg.norm(m.get_center()-center)>1.7:m.move_to(center+[-1.5,.7*np.sin(self.time),0])
        for dot in dots:dot.add_updater(advect)
        self.show(arrows,dots)
        probe2=cube(center,.6);self.show(probe2)
        self.play(blend.animate.set_value(1),run_time=4,rate_func=linear)
        label2=math(r"\mathbf F_2=\Omega(-y\hat{\mathbf x}+x\hat{\mathbf y})",40,[3.7,2.3,0],width=6.5);self.show(label2)
        z2=math(r"\nabla\cdot\mathbf F_2=0",42,[3.7,-1.9,0]);self.show(z2)
        same=text("MESMO DIVERGENTE · GEOMETRIA DIFERENTE",27,GEO).move_to([0,-2.65,0]);self.show(same)
        self.beat(414)
        self.erase(same)
        curls=VGroup(math(r"\nabla\times\mathbf F_1=0",33,[-3.7,-2.65,0]),math(r"\nabla\times\mathbf F_2=2\Omega\hat{\mathbf z}",33,[3.7,-2.65,0]));self.show(curls)
        self.beat(420);self.clear()


    def wheel(self):
        self.title("COMO DETECTAR CIRCULAÇÃO LOCAL?")
        center=np.array([-3.8,.15,0]);omega=ValueTracker(0)
        wheel=VGroup(Circle(.92,color=AMBER,stroke_width=2),Circle(.13,color=AMBER,fill_color=AMBER,fill_opacity=1),
                     *[Line(center+np.zeros(3),center+np.zeros(3)) for _ in []])
        for a in np.linspace(0,TAU,8,endpoint=False):
            paddle=Polygon([.18,-.06,0],[.85,-.06,0],[.85,.18,0],[.58,.18,0],color=AMBER,fill_color=AMBER,fill_opacity=.38,stroke_width=2)
            paddle.rotate(a,about_point=ORIGIN);wheel.add(paddle)
        wheel.move_to(center);self.show(wheel)
        uniform=self.vector_field(center);self.show(uniform)
        caption=text("Sonda geométrica de um campo genérico F",26,MUTED,width=7.5).move_to([3,2.1,0]);self.show(caption)
        formula=math(r"\nabla\times\mathbf F_1=0",54,[3,.6,0]);self.show(formula)
        stopped=text("Sonda sem giro",28,AMBER).move_to([3,-.75,0]);self.show(stopped)
        self.beat(429)
        self.erase(uniform,stopped)
        formula=self.change(formula,math(r"\mathbf F_2=\Omega(-y\hat x+x\hat y)",45,[3,1,0],width=7.8))
        field=always_redraw(lambda:VGroup(*[vec(center+[x,y,0],center+np.array([x,y,0])+.38*omega.get_value()*np.array([-y,x,0]),E,3,.7)
                    for x in [-1.8,-1.2,0,1.2,1.8] for y in [-1.7,-1.1,0,1.1,1.7] if x*x+y*y>1.1]))
        self.show(field)
        phase=ValueTracker(0)
        phase.add_updater(lambda m,dt:m.increment_value(dt*.7*omega.get_value()))
        self.add(phase)
        particles=always_redraw(lambda:VGroup(*[Dot(center+r*np.array([np.cos(a+phase.get_value()),np.sin(a+phase.get_value()),0]),radius=.045,color=E)
                for r in [1.3,1.8] for a in np.linspace(0,TAU,5,endpoint=False)]))
        wheel.add_updater(lambda m,dt:m.rotate(dt*.7*omega.get_value(),about_point=center))
        self.show(particles)
        label=math(r"\Omega=",44,[2.2,-.25,0]);value=DecimalNumber(0,num_decimal_places=2,font_size=44,color=AMBER).move_to([3.8,-.25,0])
        value.add_updater(lambda m:m.set_value(omega.get_value()));self.show(label,value)
        self.beat(434)
        self.play(omega.animate.set_value(1),run_time=10,rate_func=linear)
        result=math(r"\nabla\times\mathbf F_2=2\Omega\hat{\mathbf z}",52,[3,-1.65,0],width=7.8);self.show(result)
        z=VGroup(Circle(.15,color=AMBER,stroke_width=2),Dot(radius=.045,color=AMBER)).move_to([-1.6,-1.7,0])
        zlabel=math(r"+\hat z",32,[-1.55,-2.2,0]).set_color(AMBER);self.show(z,zlabel)
        self.beat(453)
        self.erase(label,value,result,formula,caption,z,zlabel)
        concept=math(r"\nabla\times\mathbf F",61,[3,.7,0]);self.show(concept)
        self.beat(458)
        self.erase(field,particles,wheel);phase.clear_updaters();self.remove(phase)
        concept=self.change(concept,math(r"\nabla\times\mathbf E",66,[0,.4,0]),t=1.7)
        self.title("AGORA, O CAMPO ELETROSTÁTICO")
        self.beat(465);self.clear()


    def circulation(self):
        self.title("CIRCULAÇÃO: ACUMULAR AO LONGO DO CAMINHO")
        self.origin=np.array([-6.2,.1,0]);self.q=charge(self.origin);self.show(self.q)
        a=np.array([-4.7,-.8,0]);b=np.array([-1.1,1.1,0])
        self.path1=CubicBezier(a,[-4.4,2,0],[-2.3,2.1,0],b,color=GEO,stroke_width=3)
        self.path2=CubicBezier(a,[-4,-2,0],[-1.4,-1.7,0],b,color=E,stroke_width=3)
        labels=VGroup(math('a',34,a+[0,-.4,0]),math('b',34,b+[0,.4,0]));self.show(labels)
        formula=VGroup(math(r"\int_a^b\mathbf E\cdot d\mathbf l=",46,[3,1.65,0],width=7.5),
                      math(r"\frac{q}{4\pi\varepsilon_0}\left(\frac{1}{r_a}-\frac{1}{r_b}\right)",46,[3,.5,0],width=7.5));self.show(formula)
        accumulator=text("ACUMULAÇÃO",25,FLUX).move_to([3,-.65,0]);self.show(accumulator)
        r0=np.linalg.norm(a-self.origin);r1=np.linalg.norm(b-self.origin);final=1/r0-1/r1
        progress=ValueTracker(0)
        track=Line([1.1,-1.2,0],[4.9,-1.2,0],color=MUTED,stroke_width=2);self.show(track)
        results=[]
        for i,path in enumerate([self.path1,self.path2]):
            progress.set_value(0);path.set_stroke(opacity=.28);self.show(path,t=.6)
            visited=always_redraw(lambda p=path:p.copy().pointwise_become_partial(p,0,max(.001,progress.get_value())).set_stroke(width=4,opacity=1))
            dot=always_redraw(lambda p=path:Dot(p.point_from_proportion(progress.get_value()),radius=.075,color=AMBER))
            def accumulated(p=path):
                pt=p.point_from_proportion(progress.get_value());val=(1/r0-1/np.linalg.norm(pt-self.origin))/final
                return Line([1.1,-1.2,0],[1.1+max(.002,3.8*val),-1.2,0],color=[GEO,E][i],stroke_width=7)
            bar=always_redraw(accumulated);self.show(visited,dot,bar,t=.4)
            self.play(progress.animate.set_value(1),run_time=7,rate_func=linear)
            result=math(r"I_"+str(i+1)+r"=\frac{q}{4\pi\varepsilon_0}\left(\frac{1}{r_a}-\frac{1}{r_b}\right)",38,[3,-2,0],width=7.8)
            if results:self.erase(results[-1],t=.3)
            self.show(result,t=.5);results.append(result)
            self.erase(dot,bar,visited,t=.3)
        self.erase(formula,accumulator,track,*results,labels)
        equal=math(r"I_1=I_2",63,[3,1.2,0]);self.show(equal)
        ends=text("Mesmos extremos, mesmo resultado",25,FLUX,width=7.5).move_to([3,-.1,0]);self.show(ends)
        self.play(Indicate(self.path1,color=GEO),run_time=1.4)
        self.play(Indicate(self.path2,color=E),run_time=1.4)
        self.beat(497)
        self.erase(equal,ends)
        self.closed=VMobject(color=GEO,stroke_width=3)
        pts=[self.path1.point_from_proportion(t) for t in np.linspace(0,1,60)]
        pts += [self.path2.point_from_proportion(t) for t in np.linspace(1,0,60)]
        self.closed.set_points_as_corners(pts).close_path()
        self.erase(self.path1,self.path2);self.show(self.closed,t=.4)
        progress.set_value(0)
        dot=always_redraw(lambda:Dot(self.closed.point_from_proportion(progress.get_value()),radius=.075,color=AMBER))
        traversed=always_redraw(lambda:self.closed.copy().pointwise_become_partial(self.closed,0,max(.001,progress.get_value())).set_stroke(AMBER,4))
        def closedbar():
            pt=self.closed.point_from_proportion(progress.get_value());val=(1/r0-1/np.linalg.norm(pt-self.origin))/final
            return Line([1.1,-.4,0],[1.1+max(.002,3.8*val),-.4,0],color=FLUX,stroke_width=7)
        bar=always_redraw(closedbar)
        label=text("VOLTA COMPLETA",27,AMBER).move_to([3,1.1,0]);self.show(label,dot,traversed,bar,t=.4)
        self.play(progress.animate.set_value(1),run_time=12,rate_func=linear)
        self.erase(label,dot,traversed,bar)
        zero=math(r"\oint_C\mathbf E\cdot d\mathbf l=0",60,[3,.5,0],width=7.8);self.show(zero,t=.5)
        self.beat(515);self.clear(keep=(self.closed,self.q))


    def stokes(self):
        self.title("STOKES: DA BORDA AO INTERIOR")
        center=np.array([-3.5,.25,0]);rx,ry=1.85,1.2
        contour=Ellipse(width=2*rx,height=2*ry,color=GEO,stroke_width=3).move_to(center)
        self.play(Transform(self.closed,contour),run_time=1.3)
        source=math('r=0',28,[-6.2,-.4,0]);self.show(source,t=.3)
        borderlabel=text("Borda C",27,GEO).move_to([-3.5,1.9,0]);self.show(borderlabel,t=.4)
        tracer=self.particles([lambda t:center+[rx*np.cos(TAU*t),ry*np.sin(TAU*t),0]],AMBER,.18,1);self.show(tracer,t=.4)
        left=math(r"\oint_C\mathbf E\cdot d\mathbf l",53,[3,1.5,0],width=7.7);self.show(left)
        self.beat(522)
        # Fatias concêntricas crescem a partir da borda e preenchem S.
        membrane=Ellipse(width=2*rx,height=2*ry,color=GEO,stroke_width=0,fill_color=GEO,fill_opacity=.13).move_to(center)
        self.play(DrawBorderThenFill(membrane),run_time=2);self.live.append(membrane)
        tiles=VGroup()
        for x in [-1.05,0,1.05]:
            for y in [-.5,.5]:
                tile=Rectangle(width=.68,height=.55,color=AMBER,stroke_width=1.3,fill_color=AMBER,fill_opacity=.09).move_to(center+[x,y,0])
                orient=Arc(radius=.17,start_angle=.2,angle=TAU*.75,color=AMBER,stroke_width=1.7).add_tip(tip_length=.08).move_to(tile)
                tiles.add(VGroup(tile,orient))
        self.show(tiles,t=1.2)
        orientation=text("Patches com orientação coerente",24,AMBER,width=7.6).move_to([3,-1.5,0]);self.show(orientation)
        positive=VGroup(Circle(.13,color=NORMAL),Dot(radius=.04,color=NORMAL)).move_to([-5.7,1.35,0])
        nhat=math(r"+\hat{\mathbf n}",30,[-5.7,1.85,0]);self.show(positive,nhat)
        term=math(r"(\nabla\times\mathbf E)\cdot d\mathbf A",45,[3,-.05,0],width=7.7)
        self.play(Indicate(tiles[0][0],color=AMBER),run_time=.7);self.show(term)
        for tile in tiles[1:]:
            marker=Dot(tile[0].get_center(),radius=.045,color=AMBER)
            self.add(marker)
            self.play(Indicate(tile[0],color=AMBER,scale_factor=1.08),marker.animate.move_to([-.8,-1.4,0]),run_time=.4)
            self.play(marker.animate.move_to(term.get_left()+[-.2,0,0]),run_time=.35)
            self.remove(marker)
        self.beat(537)
        term=self.change(term,math(r"\sum(\nabla\times\mathbf E)\cdot\Delta\mathbf A",43,[3,-.05,0],width=7.7))
        term=self.change(term,math(r"\int_S(\nabla\times\mathbf E)\cdot d\mathbf A",49,[3,-.05,0],width=7.7))
        self.beat(543)
        self.erase(orientation,borderlabel)
        full=math(r"\oint_C\mathbf E\cdot d\mathbf l=\int_S(\nabla\times\mathbf E)\cdot d\mathbf A",50,[0,-2.3,0],width=13.6)
        self.morph(VGroup(left,term),full,1.8);self.live.remove(left);self.live.remove(term);self.live.append(full)
        regular=text("Superfície inteira em região regular",26,GEO,width=7.5).move_to([3,1.2,0]);self.show(regular)
        self.play(LaggedStart(*[Indicate(tile[0],color=GEO) for tile in tiles],lag_ratio=.15),run_time=3)
        self.beat(555)
        self.play(Indicate(self.closed,color=AMBER),run_time=1.4)
        self.beat(560)
        self.title("DA CIRCULAÇÃO ZERO AO ROTACIONAL ZERO")
        self.erase(regular)
        # O mesmo Stokes continua na tela; primeiro o zero da borda.
        zero=math(r"0=\int_S(\nabla\times\mathbf E)\cdot d\mathbf A",53,[2.9,.7,0],width=7.8)
        full=self.change(full,zero,t=1.7)
        full=self.change(full,math(r"\int_S(\nabla\times\mathbf E)\cdot d\mathbf A=0",53,[2.9,.7,0],width=7.8),t=1.3)
        chosen=tiles[2][0].copy().set_fill(AMBER,.18).set_stroke(AMBER,3)
        self.show(chosen,t=.3)
        self.play(tiles.animate.set_stroke(opacity=.12).set_fill(opacity=.015),membrane.animate.set_fill(opacity=.025),
                  self.closed.animate.set_stroke(opacity=.22),chosen.animate.move_to(center).scale(2.2),run_time=1.5)
        self.erase(positive,nhat,tracer)
        full=self.change(full,math(r"(\nabla\times\mathbf E)\cdot\hat{\mathbf n}\,\Delta A=0",50,[2.9,.7,0],width=7.9),t=1.3)
        theta=ValueTracker(0);size=ValueTracker(.9)
        px,py=ValueTracker(center[0]),ValueTracker(center[1])
        position=lambda:np.array([px.get_value(),py.get_value(),0])
        def patch():
            u=RIGHT;v=np.array([.35*np.sin(theta.get_value()),np.cos(theta.get_value())+.8*np.sin(theta.get_value()),0])
            return Polygon(*[position()+size.get_value()*(i*u+j*v) for i,j in [(-1,-1),(1,-1),(1,1),(-1,1)]],
                           color=AMBER,stroke_width=2.5,fill_color=AMBER,fill_opacity=.12)
        self.erase(chosen,t=.3);chosen=always_redraw(patch);self.show(chosen,t=.3)
        normal=always_redraw(lambda:vec(position(),position()+1.25*np.array([.35*np.cos(theta.get_value()),-.7*np.sin(theta.get_value())+.8*np.cos(theta.get_value()),0]),NORMAL,4))
        self.show(normal,t=.3)
        anysurface=text("Qualquer pequena superfície,\nem qualquer orientação,\nnuma região regular.",27,GEO,width=7.7).move_to([2.9,-1.1,0]);self.show(anysurface,t=.5)
        self.play(theta.animate.set_value(.9),size.animate.set_value(.5),run_time=3)
        self.play(theta.animate.set_value(-.7),size.animate.set_value(.25),run_time=3)
        self.play(theta.animate.set_value(.3),size.animate.set_value(.13),run_time=2)
        self.play(px.animate.set_value(-4.5),py.animate.set_value(.55),theta.animate.set_value(.8),run_time=4)
        self.play(px.animate.set_value(-2.4),py.animate.set_value(0),theta.animate.set_value(-.5),run_time=4)
        self.play(px.animate.set_value(-3.5),py.animate.set_value(.25),theta.animate.set_value(.3),run_time=2)
        full=self.change(full,math(r"\nabla\times\mathbf E=0",75,[2.9,.7,0],width=7.8),t=1.6)
        self.title("CAMPO ELETROSTÁTICO É IRROTACIONAL")
        self.beat(590);self.clear()


    def synthesis(self):
        self.title("ELETROSTÁTICA: DUAS PERGUNTAS LOCAIS")
        central=math(r"\mathbf E(\mathbf r)",58,[0,2.1,0]);self.show(central)
        question=text("Há fonte local?",27,Q).move_to([-4,2.5,0]);self.show(question)
        c=cube([-4,1.05,0],.9);flow=self.flow_cube([-4,1.05,0],1,1);self.show(c,flow)
        leftlink=VMobject().set_points_as_corners([[-.95,2.1,0],[-2.7,2.1,0],[-2.7,1.05,0],[-2.9,1.05,0]]).set_stroke(E,1.5,.45);self.show(leftlink,t=.4)
        mechanism=text("FLUXO",26,FLUX).move_to([-4,-.15,0]);self.show(mechanism)
        self.beat(603)
        op=math(r"\nabla\cdot\mathbf E",46,[-4,-.95,0]);self.show(op)
        left=self.change(op,math(r"\nabla\cdot\mathbf E=\frac{\rho}{\varepsilon_0}",52,[-4,-1.6,0],width=6.5))
        tag=text("GAUSS · GLOBAL → LOCAL",22,GEO).move_to([-4,-2.65,0]);self.show(tag)
        self.beat(611)
        question2=text("Há circulação local?",27,AMBER).move_to([4,2.5,0]);self.show(question2)
        wheel=VGroup(Circle(.65,color=AMBER,stroke_width=2),*[Line([0,0,0],[.65*np.cos(a),.65*np.sin(a),0],color=AMBER,stroke_width=3) for a in np.linspace(0,TAU,8,endpoint=False)]).move_to([4,1.05,0]);self.show(wheel)
        rightlink=VMobject().set_points_as_corners([[.95,2.1,0],[2.7,2.1,0],[2.7,1.05,0],[2.9,1.05,0]]).set_stroke(E,1.5,.45);self.show(rightlink,t=.4)
        uniform=VGroup(*[vec([2.9,y,0],[3.35,y,0],E,2,.65) for y in [.65,1.05,1.45]],
                       *[vec([4.65,y,0],[5.1,y,0],E,2,.65) for y in [.65,1.05,1.45]])
        dots=self.particles([lambda t,y=y:np.array([2.9+2.2*t,y,0]) for y in [.65,1.45]],speed=.2,count=2);self.show(uniform,dots)
        mechanism2=text("CIRCULAÇÃO LOCAL",25,AMBER).move_to([4,-.15,0]);self.show(mechanism2)
        self.beat(619)
        right=math(r"\nabla\times\mathbf E",46,[4,-.95,0]);self.show(right)
        right=self.change(right,math(r"\nabla\times\mathbf E=0",57,[4,-1.6,0],width=6.5))
        tag2=text("STOKES · GLOBAL → LOCAL",22,AMBER).move_to([4,-2.65,0]);self.show(tag2)
        self.beat(627)
        self.play(Indicate(left,color=Q),Indicate(c,color=GEO),run_time=1.2)
        self.play(Indicate(right,color=AMBER),Indicate(wheel,color=AMBER),run_time=1.2)
        self.beat(635);self.clear(keep=(right,));self.map_curl=right


    def coda(self):
        self.title("FARADAY: QUANDO B VARIA NO TEMPO")
        self.play(self.map_curl.animate.move_to([3,.6,0]),run_time=.8)
        law=self.change(self.map_curl,math(r"\nabla\times\mathbf E=-\frac{\partial\mathbf B}{\partial t}",62,[3,.6,0],width=7.8),t=1.5)
        phase=ValueTracker(0);amplitude=ValueTracker(1)
        phase.add_updater(lambda m,dt:m.increment_value(2.2*dt));self.add(phase)
        def magnetic():
            factor=1+.25*amplitude.get_value()*np.sin(phase.get_value())
            circles=VGroup(*[Circle(r*factor,color=MAG,stroke_width=2.5,stroke_opacity=.4+.4*factor/1.25).move_to([-3.8,.2,0]) for r in [.7,1.2,1.7]])
            return circles
        rings=always_redraw(magnetic);self.show(rings)
        label=text("Campo B variando",28,MAG).move_to([-3.8,-2.65,0]);self.show(label)
        self.beat(644)
        self.play(amplitude.animate.set_value(0),run_time=4,rate_func=linear)
        phase.clear_updaters();self.remove(phase)
        static=math(r"\frac{\partial\mathbf B}{\partial t}=0",47,[3,-1.25,0]);self.show(static)
        self.erase(label);label=text("B constante no tempo",28,MAG).move_to([-3.8,-2.65,0]);self.show(label)
        self.beat(653)
        self.erase(static,rings,label)
        law=self.change(law,math(r"\nabla\times\mathbf E=0",63,[3,1.1,0]),t=1.4)
        self.title("PRÓXIMA IDEIA: POTENCIAL ELÉTRICO")
        center=np.array([-5.9,.1,0])
        arcs=VGroup(*[Arc(radius=r,start_angle=-.7,angle=1.4,color=AMBER,stroke_width=2.4,stroke_opacity=.65).shift(center) for r in [2,2.7,3.4]])
        self.play(LaggedStart(*[Create(a) for a in arcs],lag_ratio=.25),run_time=2);self.live.append(arcs)
        radius=ValueTracker(2.7);theta=ValueTracker(-.55)
        point=always_redraw(lambda:Dot(center+radius.get_value()*np.array([np.cos(theta.get_value()),np.sin(theta.get_value()),0]),radius=.075,color=WHITE));self.show(point)
        self.play(theta.animate.set_value(.45),run_time=3,rate_func=linear)
        def direction(sign,color,offset):
            u=np.array([np.cos(theta.get_value()),np.sin(theta.get_value()),0]);v=np.array([-u[1],u[0],0]);p=center+radius.get_value()*u+offset*v
            return vec(p,p+sign*.6*u,color,4)
        gradient=always_redraw(lambda:direction(-1,AMBER,.13));electric=always_redraw(lambda:direction(1,E,-.13))
        self.show(gradient,electric)
        gradlabel=math(r"\nabla V",42,[3,-.25,0]);gradlabel.set_color(AMBER);self.show(gradlabel)
        self.play(radius.animate.set_value(3.3),run_time=3,rate_func=linear)
        target=math(r"\mathbf E=-\nabla V",74,[3,-.65,0],width=7.8);target.set_color_by_tex('V',AMBER,substring=False)
        potential=self.change(gradlabel,target,t=1.5)
        self.play(theta.animate.set_value(.1),run_time=2.5,rate_func=linear)
        self.beat(675)
