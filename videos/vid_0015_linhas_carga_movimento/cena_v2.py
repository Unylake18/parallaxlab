"""EXERCÍCIO RESOLVIDO · EP. 06 — reconstrução visual silenciosa.

Fonte acima, corrente +x. Abaixo: r=-y, B=-z, Iℓ×B=+y.
Um parâmetro controla gráfico, forças e ghosts qualitativos; não há dinâmica.
MF-Tools controla cancelamentos e reorganizações, com MathTex de string única.
"""
from contextlib import contextmanager
import json
from pathlib import Path
import sys
import numpy as np
from manim import *
from MF_Tools import TransformByGlyphMap

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from template.config import BACKGROUND_COLOR, TEXT_COLOR, PRIMARY_COLOR, WATERMARK_PATH
from template.fonts import screen_text

UNIT = Path(__file__).resolve().parent
WHITE, CYAN = TEXT_COLOR, PRIMARY_COLOR
BLUE, BLUE_L, MAGENTA, VIOLET, MUTED = "#267BFF", "#7FB2FF", "#EA63FF", "#9C8CFF", "#ADB8D1"
CY = 3.55


@contextmanager
def wide_pango():
    pw, ph = config.pixel_width, config.pixel_height
    config.pixel_width, config.pixel_height = 4000, 4000
    try:
        yield
    finally:
        config.pixel_width, config.pixel_height = pw, ph


def text(content, size=26, color=WHITE, opacity=1, width=8):
    with wide_pango():
        mob = screen_text(content, size, color=color)
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob.set_opacity(opacity)


def mt(*parts, size=52, color=WHITE, width=7.9, y=None):
    m = MathTex(*parts, font_size=size, color=color)
    if m.width > width:
        m.scale_to_fit_width(width)
    return m.move_to([0, y, 0]) if y is not None else m


def vec(a, b, color=WHITE, width=5):
    return Arrow(a, b, buff=0, stroke_width=width, color=color, tip_length=0.18,
                 max_tip_length_to_length_ratio=0.28)


def boxed(m, color=CYAN):
    return SurroundingRectangle(m, buff=0.2, corner_radius=0.1, color=color, stroke_width=2.5)


def charge():
    return VGroup(Circle(radius=0.095, stroke_width=1.4, color=BLUE_L, fill_color=BLUE, fill_opacity=0.55),
                  Line(LEFT*0.052, RIGHT*0.052, color=WHITE, stroke_width=1.7),
                  Line(DOWN*0.052, UP*0.052, color=WHITE, stroke_width=1.7))


class ChargeLine(VGroup):
    def __init__(self, number, y, phase):
        super().__init__()
        self.y, self.phase = ValueTracker(y), phase
        self.wire = Line([-3.3, y, 0], [3.3, y, 0], color=BLUE_L, stroke_width=2.4)
        self.wire.add_updater(lambda m: m.put_start_and_end_on([-3.3, self.y.get_value(), 0], [3.3, self.y.get_value(), 0]))
        self.particles = VGroup(*[charge() for _ in range(11)])
        for i, p in enumerate(self.particles):
            p.add_updater(lambda m, i=i: m.move_to([-3.3+((i*0.6+self.phase.get_value()) % 6.6), self.y.get_value(), 0]))
        self.name = text(f"linha {number}", 21, opacity=0.65)
        self.name.add_updater(lambda m: m.move_to([-2.8, self.y.get_value()-0.37, 0]))
        self.density = mt(r"\lambda", size=35, color=CYAN)
        self.density.add_updater(lambda m: m.move_to([-3.65, self.y.get_value()+0.03, 0]))
        self.flow_arrow = vec([1, y+0.48, 0], [2.5, y+0.48, 0], BLUE)
        self.flow_arrow.add_updater(lambda m: m.put_start_and_end_on([1, self.y.get_value()+0.48, 0], [2.5, self.y.get_value()+0.48, 0]))
        self.flow_label = mt("v", size=36, color=BLUE)
        self.flow_label.add_updater(lambda m: m.move_to([2.85, self.y.get_value()+0.48, 0]))
        self.add(self.wire, self.particles, self.name, self.density, self.flow_arrow, self.flow_label)
        self.update(0)


class GlyphEq:
    """Spans semânticos calculados em LaTeX estabilizado, sem índices no render."""
    def __init__(self, *parts, size=56, y=-1.2):
        multi = mt(*parts, size=size, width=100)
        self.offsets = np.concatenate([[0], np.cumsum([len(p) for p in multi])]).astype(int)
        self.mob = mt(" ".join(parts), size=size, y=y)
        assert len(self.mob[0]) == int(self.offsets[-1]), parts
        self.parts = parts

    def p(self, i):
        return list(range(int(self.offsets[i]), int(self.offsets[i+1])))

    def frac(self, i):
        ids, glyphs = self.p(i), self.mob[0]
        bar = max(ids, key=lambda k: glyphs[k].width)
        by = glyphs[bar].get_y()
        num = sorted([k for k in ids if k != bar and glyphs[k].get_y() > by], key=lambda k: glyphs[k].get_x())
        den = sorted([k for k in ids if k != bar and glyphs[k].get_y() < by], key=lambda k: glyphs[k].get_x())
        return num, [bar], den

    def group(self, ids):
        return VGroup(*[self.mob[0][i] for i in ids])


def surface_point(x, theta, r=1):
    # Projeção linear (x,y,z) -> (x+.4z,y-.22z), eixo horizontal preservado.
    return np.array([x+0.4*r*np.sin(theta), CY+r*np.cos(theta)-0.22*r*np.sin(theta), 0])


def ring(x=0, r=1, color=VIOLET, fill=0):
    out = ParametricFunction(lambda t: surface_point(x, t, r), t_range=[0, TAU], color=color, stroke_width=2.8)
    return out.set_fill(color, opacity=fill)


class GaussianCylinder(VGroup):
    def __init__(self):
        self.body = Rectangle(width=4.6, height=2, stroke_width=0, fill_color=VIOLET, fill_opacity=0.10).move_to([0, CY, 0])
        self.caps = VGroup(ring(-2.3, fill=0.11), ring(2.3, fill=0.11))
        self.rails = VGroup(*[Line(surface_point(-2.3, t), surface_point(2.3, t), color=VIOLET, stroke_width=2.4) for t in (0, PI)])
        self.mesh = VGroup(*[DashedLine(surface_point(-2.3, t), surface_point(2.3, t), color=VIOLET, stroke_width=1, dash_length=0.12).set_opacity(0.25) for t in (PI/3, 2*PI/3)])
        super().__init__(self.body, self.mesh, self.caps, self.rails)
        self.set_z_index(-1)


class LinhasCarga015(Scene):
    def play(self, *args, **kwargs):
        if "run_time" in kwargs:
            kwargs["run_time"] = round(kwargs["run_time"]*config.frame_rate)/config.frame_rate
        return super().play(*args, **kwargs)

    def checkpoint(self, name, hold=2):
        self.qa.append({"estado": name, "tempo_s": round(float(self.time+hold/2), 3)})
        self.wait(hold)
        out = UNIT / "frames_preview_v2"
        out.mkdir(exist_ok=True)
        self.renderer.update_frame(self)
        self.renderer.camera.get_image().save(out / f"{len(self.qa):02d}_{name}.png")

    def heading(self, content):
        self.play(Transform(self.title, text(content, 38).move_to([0, 6.45, 0])), run_time=0.6)

    def match(self, old, new, **kwargs):
        self.play(TransformMatchingTex(old, new, **kwargs), run_time=1.2)
        return new

    def glyph(self, old, new, *maps, extras=(), rt=1.5):
        self.play(TransformByGlyphMap(old.mob, new.mob, *maps, auto_fade=True, printing=False), *extras, run_time=rt)
        self.remove(old.mob)
        self.mf_steps.append({"de": " ".join(old.parts), "para": " ".join(new.parts)})
        return new

    def forces(self, line, sign, b=0.58, electric=1.55, x=-0.45):
        y = line.y.get_value()
        e, m = vec([x,y,0], [x,y+sign*electric,0], CYAN), vec([x,y,0], [x,y-sign*electric*b,0], MAGENTA)
        el = mt("F_E", size=34, color=CYAN).move_to([x-0.6, y+sign*electric*0.6, 0])
        ml = mt("F_B", size=34, color=MAGENTA).move_to([x+0.58, y-sign*electric*b*0.7, 0])
        return VGroup(e,el), VGroup(m,ml)

    def flow(self, line, symbol, color):
        self.play(Transform(line.flow_label, mt(symbol, size=36, color=color).move_to(line.flow_label.get_center())),
                  line.flow_arrow.animate.set_color(color), run_time=0.5)

    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.qa, self.mf_steps = [], []
        rng = np.random.default_rng(15)
        self.add(VGroup(*[Dot([rng.uniform(-4.4,4.4), rng.uniform(-4,7.2),0], radius=rng.uniform(0.01,0.025),
                             color=WHITE, fill_opacity=rng.uniform(0.08,0.2)) for _ in range(46)]))
        # Branding igual ao build_stage do vid_0014, respeitando a família editorial.
        wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(0.35)
        self.add(wm.to_corner(UP+RIGHT, buff=0.28))
        self.add(text("EXERCÍCIO RESOLVIDO · EP. 06",20,opacity=0.65).to_corner(UP+LEFT,buff=0.4))
        self.title = text("Duas linhas carregadas",38).move_to([0,6.45,0])
        phase, self.speed = ValueTracker(0), ValueTracker(0.55)
        phase.add_updater(lambda m,dt: m.increment_value(0.9*self.speed.get_value()*dt))
        self.add(phase,self.speed)
        top, bottom = ChargeLine(1,4.0,phase), ChargeLine(2,1.45,phase)
        dim = DoubleArrow([3.6,1.45,0],[3.6,4.0,0],buff=0,color=MUTED,stroke_width=2,tip_length=0.13)
        d_label = mt("d",size=36).move_to([3.95,2.7,0])
        info = text("Infinitas · paralelas · cargas positivas",24,opacity=0.7).move_to([0,-1.6,0])
        self.play(FadeIn(self.title),Create(top),Create(bottom),GrowArrow(dim),FadeIn(d_label,info),run_time=1.3)
        self.checkpoint("01_enunciado_horizontal",3)
        et,bt = self.forces(top,1,electric=1.25)
        eb,bb = self.forces(bottom,-1)
        self.heading("A carga repele")
        self.play(GrowArrow(et[0]),GrowArrow(eb[0]),FadeIn(et[1],eb[1]),run_time=0.9)
        self.checkpoint("02_repulsao_eletrica")
        self.heading("O movimento também atrai")
        self.flow(top,"I",MAGENTA); self.flow(bottom,"I",MAGENTA)
        self.play(GrowArrow(bt[0]),GrowArrow(bb[0]),FadeIn(bt[1],bb[1]),FadeOut(info),run_time=0.9)
        question = text("Qual velocidade iguala os módulos?",29).move_to([0,-1.1,0])
        qeq = mt("F_E","=","F_B",r"\;?",y=-2.2,size=54)
        qeq[0].set_color(CYAN); qeq[2].set_color(MAGENTA)
        self.play(FadeIn(question),Write(qeq),run_time=0.9)
        self.checkpoint("03_forcas_coexistindo_abertura",3)

        self.heading("A geometria do campo elétrico")
        self.play(FadeOut(bottom,et,eb,bt,bb,dim,d_label,question,qeq,top.name),top.y.animate.set_value(CY),run_time=1.1)
        self.flow(top,"v",BLUE)
        cylinder = GaussianCylinder()
        ell_dim = DoubleArrow([-2.3,1.45,0],[2.3,1.45,0],buff=0,color=MUTED,stroke_width=2,tip_length=0.13)
        ell_label = mt(r"\ell",size=37).move_to([0,1.12,0])
        rdim = DashedLine([0,CY,0],[0,CY-1,0],color=MUTED)
        rlabel = mt("d",size=33).move_to([0.35,CY-0.6,0])
        gtag = text("GAUSS · SUPERFÍCIE FECHADA",23,VIOLET).move_to([0,0.35,0])
        self.play(Create(cylinder),GrowArrow(ell_dim),FadeIn(ell_label,gtag),Create(rdim),FadeIn(rlabel),run_time=1.3)
        self.checkpoint("04_cilindro_horizontal")
        field = VGroup(*[vec(surface_point(x,t),surface_point(x,t,r=1.65),CYAN,4)
                         for x,t in ((-1.2,0),(0.8,0),(-1.2,PI),(1.2,PI),(-0.6,PI/2),(0.7,3*PI/2))])
        elab = mt(r"\vec E",size=36,color=CYAN).move_to([-1.55,5.2,0])
        self.play(LaggedStart(*[GrowArrow(a) for a in field],lag_ratio=0.12),FadeIn(elab),run_time=1.2)
        self.checkpoint("05_campo_radial")
        patch = Polygon(*[surface_point(x,t) for x,t in ((-0.15,-0.18),(0.35,-0.18),(0.35,0.18),(-0.15,0.18))],color=VIOLET,fill_opacity=0.5,stroke_width=2)
        normal = vec(surface_point(0.1,0),surface_point(0.1,0,r=1.65),VIOLET,4)
        alab = mt(r"d\vec A",size=32,color=VIOLET).move_to([0.15,5.53,0])
        seq = mt(r"\vec E\parallel d\vec A",r"\quad\Rightarrow\quad",r"\vec E\cdot d\vec A=E\,dA",y=-1.05,size=43)
        self.play(Create(patch),GrowArrow(normal),FadeIn(alab),Write(seq),run_time=1.1)
        self.checkpoint("06_lateral_E_paralelo_dA",3)
        self.play(FadeOut(seq,patch,normal,alab,field,elab),run_time=0.5)
        cv,angles,cnames,czeros = VGroup(),VGroup(),VGroup(),VGroup()
        for x,s,title in ((-2.3,-1,"tampa esquerda"),(2.3,1,"tampa direita")):
            p = surface_point(x,0)
            cv.add(VGroup(vec(p,p+UP*0.72,CYAN,4),vec(p,p+RIGHT*s*0.95,VIOLET,4),
                          mt(r"\vec E",size=31,color=CYAN).move_to(p+UP*1),
                          mt(r"d\vec A",size=31,color=VIOLET).move_to(p+RIGHT*s*1.1+DOWN*0.35)))
            angles.add(VMobject(color=WHITE,stroke_width=2).set_points_as_corners([p+UP*0.2,p+UP*0.2+RIGHT*s*0.2,p+RIGHT*s*0.2]))
            cnames.add(text(title,24,VIOLET).move_to([x,-0.45,0]))
            czeros.add(mt(r"\Phi_{\rm esq}=0" if s<0 else r"\Phi_{\rm dir}=0",size=43).move_to([x,-1.15,0]))
        self.heading("Nas tampas: campo perpendicular")
        perp = mt(r"\vec E\perp d\vec A\quad\Rightarrow\quad\vec E\cdot d\vec A=0",y=-2.6,size=42)
        self.play(*[GrowArrow(a) for a in cv[0][:2]],FadeIn(*cv[0][2:]),Create(angles[0]),FadeIn(cnames[0]),Write(czeros[0]),run_time=0.9)
        self.checkpoint("07_tampa_esquerda_normal_90graus")
        self.play(*[GrowArrow(a) for a in cv[1][:2]],FadeIn(*cv[1][2:]),Create(angles[1]),FadeIn(cnames[1]),Write(czeros[1]),Write(perp),run_time=0.9)
        cmsg = text("Cada tampa tem fluxo zero individualmente",26).move_to([0,-4.1,0])
        self.play(FadeIn(cmsg),run_time=0.5)
        self.checkpoint("08_duas_tampas_zero_individual",3)
        self.heading("Só a lateral contribui")
        self.play(FadeOut(cv,angles,cnames,czeros,perp,cmsg),cylinder.body.animate.set_fill(opacity=0.22),cylinder.caps.animate.set_fill(opacity=0.025),run_time=0.8)
        gauss = mt(r"\oint_{\mathcal S}\vec E\cdot d\vec A","=",r"\frac{Q_{\rm env}}{\varepsilon_0}",y=-0.8,size=51)
        qenv = mt(r"Q_{\rm env}","=",r"\lambda\ell",y=-2.3,size=48)
        flux = mt(r"\oint_{\mathcal S}\vec E\cdot d\vec A","=",r"E(2\pi d\ell)",y=-3.9,size=46)
        self.play(Write(gauss),run_time=0.9)
        self.play(TransformFromCopy(top.density,qenv[2][0]),TransformFromCopy(ell_label,qenv[2][1]),Write(qenv[:2]),run_time=1)
        self.play(Write(flux),Indicate(cylinder.body,color=VIOLET),run_time=1)
        self.checkpoint("09_fluxo_reduz_a_lateral",3)
        g = GlyphEq(r"E(2\pi d\ell)","=",r"\frac{\lambda\ell}{\varepsilon_0}",size=56,y=-1.1)
        self.play(TransformMatchingTex(gauss,g.mob),FadeOut(qenv,flux),run_time=1.1)
        left_ids = g.p(0); gn,gb,gd = g.frac(2)
        le,re = [left_ids[-2]],[gn[-1]]
        assert len(gn)==2 and len(gd)==2
        cuts = VGroup(*[Line(g.group(ids).get_corner(DL),g.group(ids).get_corner(UR),color=CYAN,stroke_width=3) for ids in (le,re)])
        self.play(Indicate(g.group(le),color=CYAN),Indicate(g.group(re),color=CYAN),Create(cuts),run_time=0.9)
        self.checkpoint("10_cancelar_ell_Gauss")
        reduced = GlyphEq(r"E(2\pi d)","=",r"\frac{\lambda}{\varepsilon_0}",size=56,y=-1.1)
        rn,rb,rd = reduced.frac(2)
        g = self.glyph(g,reduced,([i for i in left_ids if i not in le],reduced.p(0)),(g.p(1),reduced.p(1)),([gn[0]],rn),(gb,rb),(gd,rd),extras=(FadeOut(cuts),))
        eg = GlyphEq("E(d)","=",r"\frac{\lambda}{2\pi\varepsilon_0d}",y=-1.15,size=59)
        en,ebar,eden = eg.frac(2)
        lp = g.p(0)
        g = self.glyph(g,eg,(lp[:2],eg.p(0)[:2]),([lp[-1]],[eg.p(0)[-1]]),
                       ([lp[-2]],[eg.p(0)[-2]]),(g.p(1),eg.p(1)),(rn,en),(rb,ebar),
                       (lp[2:4],eden[:2]),(rd,eden[2:4]),([lp[-2]],eden[-1:]),rt=1.6)
        ef = eg.mob
        ebox = boxed(ef); self.play(Create(ebox),run_time=0.6)
        self.checkpoint("11_campo_E_d",3)

        self.heading("Campo da linha 1, força na linha 2")
        self.play(FadeOut(cylinder,ell_dim,ell_label,rdim,rlabel,gtag),top.y.animate.set_value(4),FadeIn(bottom,dim,d_label,top.name),run_time=1)
        segment = Line([-1.6,1.45,0],[0.6,1.45,0],color=CYAN,stroke_width=7)
        brace = Brace(segment,DOWN,buff=0.17,color=MUTED)
        sl = mt(r"\ell",size=35).next_to(brace,DOWN,buff=0.08).shift(LEFT*0.65)
        ea = vec([-0.45,1.45,0],[-0.45,-0.1,0],CYAN)
        eal = mt(r"\vec E_1(d)",size=34,color=CYAN).move_to([0.55,0.65,0])
        qe = mt(r"q=\lambda\ell",size=47,y=-2.7)
        self.play(Create(segment),GrowFromCenter(brace),FadeIn(sl),GrowArrow(ea),FadeIn(eal),Write(qe),run_time=1)
        self.checkpoint("12_campo_externo_e_carga_trecho")
        fe = mt("F_E","=","qE(d)","=",r"\lambda\ell E(d)",size=49,y=-2.7)
        self.play(TransformMatchingTex(qe,fe),run_time=1.2)
        fer = mt(r"\frac{F_E}{\ell}","=",r"\frac{\lambda^2}{2\pi\varepsilon_0d}",size=59,color=CYAN,y=-2.8)
        self.play(TransformMatchingTex(fe,fer),FadeOut(ef,ebox),Transform(eal,mt("F_E",size=35,color=CYAN).move_to([0.2,0.55,0])),run_time=1.2)
        feb = boxed(fer); self.play(Create(feb),run_time=0.5)
        self.checkpoint("13_forca_eletrica",3)
        self.heading("Superfície → curva")
        fem = mt(r"F_E/\ell=\lambda^2/(2\pi\varepsilon_0d)",size=34,color=CYAN,y=-4.5)
        self.play(FadeOut(bottom,dim,d_label,segment,brace,sl,ea,eal,feb,top.name),TransformMatchingTex(fer,fem),top.y.animate.set_value(CY),FadeIn(cylinder),run_time=1)
        self.play(cylinder.caps[0].animate.shift(RIGHT*2.3),cylinder.caps[1].animate.shift(LEFT*2.3),cylinder.body.animate.stretch_to_fit_width(0.025),
                  cylinder.rails.animate.stretch_to_fit_width(0.025),FadeOut(cylinder.mesh),FadeIn(rdim,rlabel),run_time=1.4)
        sr = mt(r"\vec E\cdot d\vec A",size=46,color=CYAN,y=0.7)
        sw = text("atravessa uma superfície",26).move_to([0,-0.1,0])
        self.play(Write(sr),FadeIn(sw),run_time=0.7)
        self.checkpoint("14_secao_perpendicular_superficie")
        acurve = ring(0,color=VIOLET).set_stroke(width=4.5).set_fill(opacity=0)
        cr = mt(r"\vec B\cdot d\vec\ell",size=46,color=MAGENTA,y=0.7)
        self.play(ReplacementTransform(cylinder.caps[1],acurve),FadeOut(cylinder.caps[0],cylinder.body,cylinder.rails),
                  TransformMatchingTex(sr,cr),Transform(sw,text("percorre uma curva",26).move_to([0,-0.1,0])),FadeIn(top.name),run_time=1.2)
        self.checkpoint("15_superficie_para_curva")
        self.play(FadeOut(cr,sw),run_time=0.5)
        self.flow(top,"I",MAGENTA); self.heading("B contorna a corrente")
        orbit = ring(0,r=1.23,color=MAGENTA).set_stroke(width=1.5,opacity=0.45)
        tangents = VGroup()
        for t in (0.22,PI/2,PI+0.22,3*PI/2):
            p = surface_point(0,t,r=1.23)
            tangent = np.array([0.4*np.cos(t),-np.sin(t)-0.22*np.cos(t),0]); tangent /= np.linalg.norm(tangent)
            tangents.add(vec(p-tangent*0.23,p+tangent*0.23,MAGENTA,4))
        atag = text("AMPÈRE · CURVA FECHADA",23,VIOLET).move_to([0,1.65,0])
        ol = mt(r"\vec B",size=37,color=MAGENTA).move_to([-1.2,4.7,0])
        self.play(Create(orbit),LaggedStart(*[GrowArrow(a) for a in tangents],lag_ratio=0.15),FadeIn(atag,ol),run_time=1.3)
        circulation = mt(r"\oint_{\mathcal C}\vec B\cdot d\vec\ell","=",r"\mu_0I",size=53,y=-1)
        self.play(Write(circulation),run_time=1)
        self.checkpoint("16_curva_amperiana_B_tangente",3)
        self.heading("Regra da mão direita")
        hints = VGroup(text("polegar",22,opacity=0.7).move_to([1.85,4.4,0]),text("dedos",22,MAGENTA).move_to([-1.1,3.9,0]))
        moving = Dot(surface_point(0,0,r=1.23),radius=0.08,color=MAGENTA)
        self.play(FadeIn(hints,moving),Indicate(top.flow_arrow,color=MAGENTA),run_time=0.7)
        self.play(MoveAlongPath(moving,orbit),run_time=2.2,rate_func=linear)
        self.checkpoint("17_regra_mao_direita_enrolamento")
        bstep = mt("B(d)",r"(2\pi d)","=",r"\mu_0I",size=56,y=-1)
        circulation = self.match(circulation,bstep)
        bg = GlyphEq("B(d)",r"(2\pi d)","=",r"\mu_0I",size=56,y=-1)
        self.remove(bstep); self.add(bg.mob)
        br = GlyphEq("B(d)","=",r"\frac{\mu_0I}{2\pi d}",size=59,y=-1)
        bnum,bbar,bden = br.frac(2)
        self.glyph(bg,br,(bg.p(0),br.p(0)),(bg.p(1)[1:-1],bden),(bg.p(2),br.p(1)),(bg.p(3),bnum),rt=1.6)
        bf = br.mob
        bbox = boxed(bf,MAGENTA); self.play(Create(bbox),FadeOut(moving,hints),run_time=0.6)
        self.checkpoint("18_campo_B_d")

        self.heading("Abaixo da linha 1: B entra na tela")
        self.play(FadeOut(acurve,orbit,tangents,atag,ol,rdim,rlabel),top.y.animate.set_value(4),FadeIn(bottom,dim,d_label),run_time=1)
        self.flow(bottom,"I",MAGENTA)
        evaluation = Dot([-0.45,1.45,0],color=WHITE,radius=0.055)
        marker = VGroup(Circle(radius=0.27,color=BACKGROUND_COLOR,fill_opacity=1,fill_color=BACKGROUND_COLOR,stroke_width=0),mt(r"\otimes",size=57,color=MAGENTA)).move_to([-2,2.7,0])
        guide = DashedLine(marker.get_bottom(),evaluation.get_center(),color=MAGENTA,stroke_width=1.5,dash_length=0.12).set_opacity(0.65)
        ml = mt(r"\vec B_1(d)=-B\hat z",size=34,color=MAGENTA).move_to([1.55,2.95,0])
        self.play(FadeIn(evaluation,marker,ml),Create(guide),run_time=1)
        self.checkpoint("19_B_entra_sem_sobreposicao",3)
        self.heading("A força aponta para a outra linha")
        b_support = VGroup(bf,bbox)
        self.play(b_support.animate.scale(0.68).move_to([0,-4.25,0]),FadeOut(fem),run_time=0.8)
        lv = vec([-1.15,1.1,0],[0.25,1.1,0],WHITE,4)
        lvl = mt(r"I\vec\ell\parallel+\hat x",size=34).move_to([1.9,0.9,0])
        ba = vec([-0.45,1.45,0],[-0.45,3,0],MAGENTA)
        bal = mt(r"\vec F_B",size=36,color=MAGENTA).move_to([0.2,2.1,0])
        cross = mt(r"\vec F_B","=",r"I\vec\ell",r"\times",r"\vec B_1(d)",size=54,y=-1.1)
        cross[0].set_color(MAGENTA); cross[4].set_color(MAGENTA)
        direction = mt(r"+\hat x\times(-\hat z)=+\hat y",size=46,y=-2.6)
        self.play(GrowArrow(lv),FadeIn(lvl),Write(cross[:2]),run_time=0.8)
        self.play(TransformFromCopy(lv,cross[2]),Write(cross[3]),TransformFromCopy(marker[1],cross[4]),run_time=1)
        self.play(Write(direction),GrowArrow(ba),FadeIn(bal),run_time=0.9)
        self.checkpoint("20_produto_vetorial_atracao",3)
        self.play(FadeOut(b_support,marker,ml,guide,lv,lvl,direction),run_time=0.7)
        fbs = mt("F_B","=",r"I\ell B(d)",size=54,y=-1.1); cross = self.match(cross,fbs)
        fbr = mt(r"\frac{F_B}{\ell}","=",r"\frac{\mu_0 I^2}{2\pi d}",size=59,color=MAGENTA,y=-1.1); cross = self.match(cross,fbr)
        fbb = boxed(fbr,MAGENTA); self.play(Create(fbb),run_time=0.5)
        self.checkpoint("21_forca_magnetica",3)
        self.heading("Atração e repulsão coexistem")
        ea = vec([-0.45,1.45,0],[-0.45,-0.1,0],CYAN)
        eal = mt("F_E",size=36,color=CYAN).move_to([-1.05,0.55,0])
        fec = mt(r"\frac{F_E}{\ell}=\frac{\lambda^2}{2\pi\varepsilon_0d}",size=52,color=CYAN,y=-2.9)
        self.play(GrowArrow(ea),FadeIn(eal),Write(fec),run_time=0.9)
        self.checkpoint("22_comparacao_forcas_origem_comum",3)

        self.heading("Quando os módulos seriam iguais?")
        bal_eq = GlyphEq(r"\frac{\lambda^2}{2\pi\varepsilon_0d}","=",r"\frac{\mu_0I^2}{2\pi d}",size=61,y=-1.4)
        self.play(FadeOut(fbr,fbb,fec,dim,d_label),Write(bal_eq.mob),run_time=1)
        an,ab,ad = bal_eq.frac(0); bn,bb,bd = bal_eq.frac(2)
        assert (len(an),len(ad),len(bn),len(bd))==(2,5,4,3)
        slashes = VGroup()
        for ids in (ad[:2]+ad[-1:],bd):
            bal_eq.group(ids).set_color(CYAN)
            for k in ids:
                gl = bal_eq.mob[0][k]
                slashes.add(Line(gl.get_corner(DL)+0.03*DL,gl.get_corner(UR)+0.03*UR,color=CYAN,stroke_width=2.5))
        self.play(Create(slashes),run_time=0.7)
        cc = mt(r"2\pi d",size=38,color=CYAN,y=-3.2); self.play(FadeIn(cc),run_time=0.5)
        self.checkpoint("23_cancelamento_2pi_d")
        red = GlyphEq(r"\frac{\lambda^2}{\varepsilon_0}","=",r"\mu_0I^2",size=61,y=-1.4)
        rn,rb,rd = red.frac(0)
        bal_eq = self.glyph(bal_eq,red,(an,rn),(ab,rb),(ad[2:4],rd),(bal_eq.p(1),red.p(1)),(bn,red.p(2)),extras=(FadeOut(slashes),FadeOut(cc)))
        self.checkpoint("24_termos_sobreviventes")
        reorg = GlyphEq(r"\frac{I^2}{\lambda^2}","=",r"\frac{1}{\mu_0\varepsilon_0}",size=61,y=-1.4)
        xn,xb,xd = reorg.frac(0); yn,yb,yd = reorg.frac(2); rhs = red.p(2)
        bal_eq = self.glyph(red,reorg,(rn,xd,{"path_arc":-PI/3}),(rb,xb),(rd,yd[2:],{"path_arc":PI/3}),
                            (red.p(1),reorg.p(1)),(rhs[:2],yd[:2]),(rhs[2:],xn,{"path_arc":PI/3}),([],yn+yb),rt=1.8)
        self.checkpoint("25_reorganizacao_I2_lambda2")
        root = GlyphEq(r"\frac{|I|}{|\lambda|}","=",r"\frac{1}{\sqrt{\mu_0\varepsilon_0}}",size=61,y=-1.4)
        un,ub,ud = root.frac(0); vn,vb,vd = root.frac(2)
        assert len(un)==3 and len(ud)==3
        bal_eq = self.glyph(reorg,root,([xn[0]],[un[1]]),(xb,ub),([xd[0]],[ud[1]]),(reorg.p(1),root.p(1)),
                            (yn,vn),(yb,vb),(yd,root.p(2)[-4:]),rt=1.5)
        cdef = mt(r"c=\frac{1}{\sqrt{\mu_0\varepsilon_0}}",size=40,color=CYAN,y=-3.2); self.play(Write(cdef),run_time=0.9)
        payoff = GlyphEq(r"\frac{|I|}{|\lambda|}","=","c",size=77,y=-1.4)
        bal_eq = self.glyph(root,payoff,(root.p(0),payoff.p(0)),(root.p(1),payoff.p(1)),(root.p(2),payoff.p(2)),rt=1.4)
        pbox = boxed(payoff.mob); self.play(Create(pbox),run_time=0.6)
        self.checkpoint("26_payoff_I_lambda_c",4)
        self.heading("Volte ao movimento das cargas")
        self.flow(top,"v",BLUE); self.flow(bottom,"v",BLUE)
        self.play(Indicate(top.particles,color=CYAN),Indicate(bottom.flow_arrow,color=BLUE),FadeOut(cdef),run_time=1)
        phrase = VGroup(text("Mas aqui a corrente é produzida justamente",26),text("pela própria linha de carga em movimento.",26)).arrange(DOWN,buff=0.12).move_to([0,-3.7,0])
        self.play(FadeIn(phrase),run_time=0.6); self.checkpoint("27_retorno_movimento_cargas",3)
        relation = mt(r"|I|","=",r"|\lambda|v",size=54,color=CYAN,y=-2.95)
        self.play(Write(relation[:2]),TransformFromCopy(bottom.flow_label,relation[2]),run_time=0.9)
        self.checkpoint("28_corrente_lambda_v",3)
        sub = GlyphEq(r"\frac{|\lambda|v}{|\lambda|}","=","c",size=68,y=-1.4)
        sn,sb,sd = sub.frac(0); self.play(FadeOut(pbox),run_time=0.4)
        bal_eq = self.glyph(payoff,sub,(payoff.p(0),sub.p(0)),(payoff.p(1),sub.p(1)),(payoff.p(2),sub.p(2)),rt=1.4)
        cuts = VGroup(*[Line(sub.group(ids).get_corner(DL),sub.group(ids).get_corner(UR),color=CYAN,stroke_width=2.5) for ids in (sn[:3],sd)])
        self.play(Create(cuts),run_time=0.7)
        vp = GlyphEq("v","=","c",size=84,y=-1.4)
        bal_eq = self.glyph(sub,vp,([sn[-1]],vp.p(0)),(sub.p(1),vp.p(1)),(sub.p(2),vp.p(2)),extras=(FadeOut(cuts),))
        vbox = boxed(vp.mob); self.play(Create(vbox),run_time=0.6)
        self.checkpoint("29_payoff_v_c",4)

        self.heading("O que muda quando v/c varia?")
        self.play(FadeOut(vp.mob,vbox,relation,phrase),run_time=0.6)
        ra = GlyphEq(r"\frac{F_B}{F_E}","=",r"\mu_0\varepsilon_0",r"\frac{I^2}{\lambda^2}",size=54,y=-1.6)
        self.play(Write(ra.mob),run_time=0.9)
        rbeta = GlyphEq(r"\frac{F_B}{F_E}","=",r"\mu_0\varepsilon_0","v^2",size=54,y=-1.6)
        self.glyph(ra,rbeta,*[(ra.p(i),rbeta.p(i)) for i in range(4)])
        reciprocal = GlyphEq(r"\frac{F_B}{F_E}","=",r"\frac{1}{c^2}","v^2",size=54,y=-1.6)
        self.glyph(rbeta,reciprocal,*[(rbeta.p(i),reciprocal.p(i)) for i in range(4)])
        ratio_g = GlyphEq(r"\frac{F_B}{F_E}","=",r"\frac{v^2}{c^2}",size=56,y=-0.55)
        pn,pb,pd = reciprocal.frac(2); fn,fb,fd = ratio_g.frac(2)
        self.glyph(reciprocal,ratio_g,(reciprocal.p(0),ratio_g.p(0)),(reciprocal.p(1),ratio_g.p(1)),
                   (reciprocal.p(3),fn),(pb,fb),(pd,fd),extras=(FadeOut(ea,eal,ba,bal,evaluation),
                   top.y.animate.set_value(4.5),bottom.y.animate.set_value(2.4)))
        ratio = ratio_g.mob
        model = text("MODELO IDEAL · linhas infinitas de carga",22,CYAN).move_to([0,5.6,0])
        qualifier = text("Parâmetro do modelo; não elétrons num fio real.",19,opacity=0.65).move_to([0,-5.45,0])
        qualitative = text("tendência qualitativa de afastamento",21,opacity=0.65).move_to([0,0.35,0])
        self.play(FadeIn(model,qualifier,qualitative),run_time=0.6)
        beta = self.speed; self.play(beta.animate.set_value(0),run_time=0.6)
        for line in (top,bottom):
            line.flow_arrow.clear_updaters()
            line.flow_arrow.add_updater(lambda m,line=line: m.put_start_and_end_on([1,line.y.get_value()+0.48,0],
                [1+1.5*max(beta.get_value(),0.001),line.y.get_value()+0.48,0]).set_opacity(1 if beta.get_value()>0.001 else 0))
            line.flow_label.clear_updaters()
            line.flow_label.add_updater(lambda m,line=line: m.move_to([1+1.5*beta.get_value()+0.35,line.y.get_value()+0.48,0]))
        axes = Axes(x_range=[0,1,0.5],y_range=[0,1,0.5],x_length=5.5,y_length=2.45,tips=False,
                    axis_config={"color":MUTED,"stroke_width":2,"include_ticks":False})
        axes.shift(np.array([-2.65,-4.5,0])-axes.c2p(0,0))
        ticks = VGroup(*[mt(str(t),size=25).move_to(axes.c2p(t,0)+DOWN*0.3) for t in (0,0.5,1)])
        labels = VGroup(mt("1",size=27).move_to(axes.c2p(0,1)+LEFT*0.35),
                        mt("v/c",size=32).move_to(axes.c2p(1,0)+RIGHT*0.55+DOWN*0.23),
                        mt(r"F_B/F_E",size=32).rotate(PI/2).move_to(axes.c2p(0,0.5)+LEFT*0.7))
        equal_line = DashedLine(axes.c2p(0,1),axes.c2p(1,1),color=VIOLET,stroke_width=1.5,dash_length=0.12).set_opacity(0.55)
        boundary = DashedLine(axes.c2p(1,0),axes.c2p(1,1),color=VIOLET,stroke_width=1.5,dash_length=0.12)
        endpoint = Circle(radius=0.09,color=VIOLET,stroke_width=2).move_to(axes.c2p(1,1))
        limit = VGroup(mt("v=c",size=28,color=VIOLET).move_to(axes.c2p(1,1)+RIGHT*0.65),
                       text("limite",20,VIOLET).move_to(axes.c2p(1,1)+RIGHT*0.65+DOWN*0.45))
        self.play(Create(axes),FadeIn(ticks,labels),Create(equal_line),Create(boundary),FadeIn(endpoint,limit),run_time=1.1)
        self.reached = 0.0001
        def plot():
            self.reached = max(self.reached,beta.get_value())
            return ParametricFunction(lambda t:axes.c2p(t,t*t),t_range=[0,self.reached],color=CYAN,stroke_width=4)
        curve = always_redraw(plot)
        point = always_redraw(lambda:Dot(axes.c2p(beta.get_value(),beta.get_value()**2),radius=0.095,color=CYAN))
        gx = always_redraw(lambda:DashedLine(axes.c2p(beta.get_value(),0),axes.c2p(beta.get_value(),max(beta.get_value()**2,0.0001)),color=CYAN,stroke_width=1.3,dash_length=0.1).set_opacity(0.5))
        bp = mt("v/c=",size=32).move_to([-2.2,-1.43,0])
        bv = DecimalNumber(0,num_decimal_places=3,font_size=32,color=CYAN).move_to([-0.85,-1.43,0])
        bv.add_updater(lambda m:m.set_value(beta.get_value()))
        fp = mt(r"F_B/F_E=",size=32).move_to([0.6,-1.43,0])
        fv = DecimalNumber(0,num_decimal_places=3,font_size=32,color=MAGENTA).move_to([2.4,-1.43,0])
        fv.add_updater(lambda m:m.set_value(beta.get_value()**2))
        def scaled_arrow(sign,amount,x,color):
            y, length = bottom.y.get_value(),1.8*amount
            return VGroup(vec([x,y,0],[x,y+sign*length,0],color)) if length>0.0001 else VGroup()
        ed = always_redraw(lambda:scaled_arrow(-1,1,-0.6,CYAN))
        bd = always_redraw(lambda:scaled_arrow(1,beta.get_value()**2,-0.6,MAGENTA))
        nd = always_redraw(lambda:scaled_arrow(-1,1-beta.get_value()**2,1,WHITE))
        names = VGroup(mt("F_E",size=33,color=CYAN).move_to([-1.2,1.35,0]),mt("F_B",size=33,color=MAGENTA).move_to([0,3.2,0]),mt(r"F_{\rm liq}",size=31).move_to([1.75,1.25,0]))
        names[1].add_updater(lambda m:m.move_to([0,bottom.y.get_value()+0.9*beta.get_value()**2+0.35,0]).set_opacity(min(1,beta.get_value()**2/0.04)))
        names[2].add_updater(lambda m:m.move_to([1.75,bottom.y.get_value()-0.9*(1-beta.get_value()**2)-0.35,0]))
        ghosts = always_redraw(lambda:VGroup(*[DashedLine([-2.2,line.y.get_value()+s*0.28*(1-beta.get_value()**2),0],
                                   [2.2,line.y.get_value()+s*0.28*(1-beta.get_value()**2),0],color=WHITE,stroke_width=1.5,dash_length=0.14).set_opacity(0.22)
                                   for line,s in ((top,1),(bottom,-1))]))
        self.play(FadeIn(curve,point,gx,bp,bv,fp,fv,ed,bd,nd,names,ghosts),run_time=0.8)
        self.checkpoint("30_grafico_beta_zero")
        for value,name,seconds in ((0.2,"31_grafico_beta_baixo",2.3),(0.6,"32_grafico_beta_intermediario",3),
                                   (0.85,"33_grafico_beta_085",2.7),(0.97,"34_grafico_proximo_1",2.7),(0.995,"35_grafico_beta_0995",2.3)):
            self.play(beta.animate.set_value(value),run_time=seconds,rate_func=smooth)
            assert 0 <= beta.get_value() < 1
            self.checkpoint(name,1.6)
        massive = mt(r"\text{partículas massivas:}\quad v<c",size=36,y=-5.35)
        self.play(FadeOut(qualifier),Write(massive),run_time=0.8)
        self.checkpoint("36_particulas_massivas_v_menor_c",3)
        self.heading("REPULSÃO LÍQUIDA")
        fr = GlyphEq(r"\frac{F_B}{F_E}","=",r"\frac{v^2}{c^2}","<1",size=56,y=-0.55)
        self.glyph(ratio_g,fr,*[(ratio_g.p(i),fr.p(i)) for i in range(3)],extras=(beta.animate.set_value(0.6),),rt=2)
        self.checkpoint("37_repulsao_liquida_final",5)
        UNIT.joinpath("qa_estados_v2.json").write_text(json.dumps({"duracao_cena_s":round(float(self.time),3),
            "referencia_visual":"vid_0014 — build_stage","MF_Tools":self.mf_steps,"estados":self.qa},ensure_ascii=False,indent=2),encoding="utf-8")
