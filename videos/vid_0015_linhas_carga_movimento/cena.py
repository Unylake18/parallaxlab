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
# Regiões locais (9×16): header > title > physics > math > secondary > safe.
HEADER_Y = 7.4
TITLE_Y = 6.45
PHYSICS_TOP_Y, PHYSICS_BOTTOM_Y = 4.0, 1.45
CY = 3.55
MATH_Y = -1.65
SECONDARY_Y = -3.75
SUBTITLE_SAFE_Y = -5.7
# O relógio editorial da V4 permanece em 15 fps também no render de postagem.
TIMING_FPS = 15
GRAPH_ORIGIN = np.array([-2.6, -4.45, 0])
# Ritmo nativo por bloco: geometrias ganham respiro, álgebra continua encadeada.
# Não se altera a velocidade do MP4 depois do render.
PLAY_TEMPO = {"enunciado_conflito": 2.05, "Gauss": 1.6, "forca_eletrica": 1.05,
              "superficie_curva": 1.30, "Ampere": 1.33,
              "mao_direita_forca_magnetica": 1.18, "igualdade_payoff_c": 1.44,
              "corrente_payoff_v": 0.83, "derivacao_razao": 1.0,
              "grafico": 1.14, "conclusao": 1.3}
GEOMETRY_HOLDS = {"cilindro_horizontal": 1.0, "lateral_E_paralelo_dA": 1.8,
                  "duas_tampas_zero_individual": 1.8, "Gauss_lei_integral": 0.7,
                  "Gauss_carga_encerrada": 0.5, "Gauss_fluxo_E_A_lateral": 0.5,
                  "Gauss_area_lateral_explicita": 0.7, "Gauss_area_carga_substituidas": 0.5,
                  "cancelar_ell_Gauss": 0.5, "Gauss_apos_cancelar_ell": 0.5,
                  "campo_E_d": 1.0, "Ampere_B_paralelo_dl_constante": 1.2,
                  "Ampere_lei_integral": 0.5, "Ampere_comprimento_curva": 0.5,
                  "campo_B_d": 1.0, "comparacao_forcas_origem_comum": 1.0,
                  "raiz_modulos_antes_de_c": 0.5}


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
        self.name = text(f"linha {number}", 25, opacity=0.7)
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
    def __init__(self, *parts, size=56, y=MATH_Y):
        multi = mt(*parts, size=size, width=100)
        self.offsets = np.concatenate([[0], np.cumsum([len(p) for p in multi])]).astype(int)
        self.mob = mt(" ".join(parts), size=size, y=y)
        assert len(self.mob[0]) == int(self.offsets[-1]), parts
        self.parts = parts

    def p(self, i):
        return list(range(int(self.offsets[i]), int(self.offsets[i+1])))

    def frac(self, i):
        return self.frac_ids(self.p(i))

    def frac_ids(self, ids):
        glyphs = self.mob[0]
        bar = max(ids, key=lambda k: glyphs[k].width)
        by = glyphs[bar].get_y()
        num = sorted([k for k in ids if k != bar and glyphs[k].get_y() > by], key=lambda k: glyphs[k].get_x())
        den = sorted([k for k in ids if k != bar and glyphs[k].get_y() < by], key=lambda k: glyphs[k].get_x())
        return num, [bar], den

    def nested_frac(self, i):
        ids = self.p(i)
        bar = max(ids, key=lambda k:self.mob[0][k].width)
        y = self.mob[0][bar].get_y()
        upper = [k for k in ids if k != bar and self.mob[0][k].get_y() > y]
        lower = [k for k in ids if k != bar and self.mob[0][k].get_y() < y]
        return self.frac_ids(upper), self.frac_ids(lower), [bar]

    def group(self, ids):
        return VGroup(*[self.mob[0][i] for i in ids])

    def copied_reference(self, glyphs):
        """Glifos de uma referência visível, copiados deliberadamente para o mapa."""
        first = len(self.mob[0])
        copies = [glyph.copy() for glyph in glyphs]
        self.mob[0].add(*copies)
        return list(range(first,first+len(copies)))


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
    def beat_duration(self, requested, kind="other"):
        duration = requested*PLAY_TEMPO[self.blocks[-1]["bloco"]]
        if kind == "glyph":
            duration = np.clip(duration, 0.8, 1.5)
        elif kind == "matching":
            duration = np.clip(duration, 0.6, 1.2)
        return round(float(duration)*TIMING_FPS)/TIMING_FPS

    def block(self, name):
        if self.blocks:
            self.blocks[-1]["fim_s"] = round(float(self.time), 3)
        self.blocks.append({"bloco": name, "inicio_s": round(float(self.time), 3)})

    def play(self, *args, **kwargs):
        kind = "glyph" if any(isinstance(a,TransformByGlyphMap) for a in args) else (
            "matching" if any(isinstance(a,TransformMatchingTex) for a in args) else "other")
        if "run_time" in kwargs and not isinstance(args[0],Wait):
            kwargs["run_time"] = self.beat_duration(kwargs["run_time"],kind)
        duration = kwargs.get("run_time", getattr(args[0], "run_time", 1))
        if hasattr(self, "beats"):
            self.beats.append({"bloco": self.blocks[-1]["bloco"],
                               "tipo": "wait" if isinstance(args[0], Wait) else "play",
                               "duracao_s": round(float(duration), 6)})
        return super().play(*args, **kwargs)

    def checkpoint(self, name, hold=0.2, equation=None):
        if name[:2].isdigit() and name[2:3] == "_":
            name = name[3:]
        hold = GEOMETRY_HOLDS.get(name,hold)
        hold = round(hold*TIMING_FPS)/TIMING_FPS
        self.qa.append({"estado": name, "tempo_s": round(float(self.time+hold/2), 3),
                        "equacao": equation, "pausa_s": round(hold,3)})
        if hold:
            self.wait(hold)
        if getattr(self, "timing_audit", False):
            return
        out = UNIT / getattr(self, "qa_frame_dir", "frames_preview_v4")
        out.mkdir(exist_ok=True)
        self.renderer.update_frame(self)
        self.renderer.camera.get_image().save(out / f"{len(self.qa):02d}_{name}.png")

    def heading(self, content):
        self.play(Transform(self.title, text(content, 38).move_to([0, TITLE_Y, 0])), run_time=0.4)

    def match(self, old, new, **kwargs):
        self.play(TransformMatchingTex(old, new, **kwargs), run_time=0.8)
        return new

    def glyph(self, old, new, *maps, extras=(), rt=1.0, local_fade=False):
        if local_fade:
            # Termos sem matching saem antes de os substitutos entrarem;
            # o intervalo total e os deslocamentos legíveis permanecem iguais.
            used_from = {i for entry in maps for i in entry[0]}
            used_to = {i for entry in maps for i in entry[1]}
            leaving = [i for i in range(len(old.mob[0])) if i not in used_from]
            entering = [i for i in range(len(new.mob[0])) if i not in used_to]
            maps = (*maps,
                    (leaving, [], {"rate_func": lambda t: smooth(min(1, t/0.4))}),
                    ([], entering, {"rate_func": lambda t: smooth(max(0, (t-0.6)/0.4))}))
        midpoint = float(self.time + self.beat_duration(rt,"glyph")/2)
        self.play(TransformByGlyphMap(old.mob, new.mob, *maps, auto_fade=True, printing=False), *extras, run_time=rt)
        self.remove(old.mob)
        self.mf_steps.append({"de": " ".join(old.parts), "para": " ".join(new.parts), "tempo_meio_s": round(midpoint,3)})
        return new

    def step(self, old, new, label, hold=0.2):
        """Matching contínuo; marcador de QA sem pausa longa entre passos."""
        self.play(TransformMatchingTex(old, new), run_time=0.9)
        self.checkpoint(label, hold, equation=" ".join(new.tex_strings))
        return new

    def struck(self, eq, spans):
        marks = VGroup()
        for span in spans:
            eq.group(span).set_color(CYAN)
            marks.add(Line(eq.group(span).get_corner(DL), eq.group(span).get_corner(UR), color=CYAN, stroke_width=2.8))
        self.play(Create(marks), run_time=0.55)
        return marks

    def forces(self, line, sign, b=0.58, electric=1.55, x=-0.45):
        y = line.y.get_value()
        e, m = vec([x,y,0], [x,y+sign*electric,0], CYAN), vec([x,y,0], [x,y-sign*electric*b,0], MAGENTA)
        el = mt("F_E", size=34, color=CYAN).move_to([x-0.6, y+sign*electric*0.6, 0])
        ml = mt("F_B", size=34, color=MAGENTA).move_to([x+0.58, y-sign*electric*b*0.7, 0])
        return VGroup(e,el), VGroup(m,ml)

    def flow(self, line, symbol, color):
        self.play(Transform(line.flow_label, mt(symbol, size=36, color=color).move_to(line.flow_label.get_center())),
                  line.flow_arrow.animate.set_color(color), run_time=0.35)

    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.qa, self.mf_steps, self.motion_samples = [], [], []
        self.blocks, self.beats = [], []
        self.block("enunciado_conflito")
        rng = np.random.default_rng(15)
        self.add(VGroup(*[Dot([rng.uniform(-4.4,4.4), rng.uniform(-4,7.2),0], radius=rng.uniform(0.01,0.025),
                             color=WHITE, fill_opacity=rng.uniform(0.08,0.2)) for _ in range(46)]))
        # Branding igual ao build_stage do vid_0014, respeitando a família editorial.
        wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(0.35)
        self.add(wm.to_corner(UP+RIGHT, buff=0.28))
        self.add(text("EXERCÍCIO RESOLVIDO · EP. 06",20,opacity=0.65).to_corner(UP+LEFT,buff=0.4))
        self.title = text("Duas linhas carregadas",38).move_to([0,TITLE_Y,0])
        phase, self.speed = ValueTracker(0), ValueTracker(0.55)
        phase.add_updater(lambda m,dt: m.increment_value(0.9*self.speed.get_value()*dt))
        self.add(phase,self.speed)
        top, bottom = ChargeLine(1,PHYSICS_TOP_Y,phase), ChargeLine(2,PHYSICS_BOTTOM_Y,phase)
        dim = DoubleArrow([3.6,1.45,0],[3.6,4.0,0],buff=0,color=MUTED,stroke_width=2,tip_length=0.13)
        d_label = mt("d",size=36).move_to([3.95,2.7,0])
        info = text("Infinitas · paralelas · cargas positivas",24,opacity=0.7).move_to([0,-1.6,0])
        self.play(FadeIn(self.title),Create(top),Create(bottom),GrowArrow(dim),FadeIn(d_label,info),run_time=0.85)
        self.checkpoint("01_enunciado_horizontal",1.2)
        et,bt = self.forces(top,1,electric=1.25)
        eb,bb = self.forces(bottom,-1)
        self.heading("A carga repele")
        self.play(GrowArrow(et[0]),GrowArrow(eb[0]),FadeIn(et[1],eb[1]),run_time=0.65)
        self.checkpoint("02_repulsao_eletrica")
        self.heading("O movimento também atrai")
        self.flow(top,"I",MAGENTA); self.flow(bottom,"I",MAGENTA)
        self.play(GrowArrow(bt[0]),GrowArrow(bb[0]),FadeIn(bt[1],bb[1]),FadeOut(info),run_time=0.65)
        question = text("Qual velocidade iguala os módulos?",29).move_to([0,-1.1,0])
        qeq = mt("F_E","=","F_B",r"\;?",y=-2.2,size=54)
        qeq[0].set_color(CYAN); qeq[2].set_color(MAGENTA)
        self.play(FadeIn(question),Write(qeq),run_time=0.65)
        self.checkpoint("03_forcas_coexistindo_abertura",1.2)

        self.block("Gauss")
        self.heading("A geometria do campo elétrico")
        self.play(FadeOut(bottom,et,eb,bt,bb,dim,d_label,question,qeq,top.name),top.y.animate.set_value(CY),run_time=0.75)
        self.flow(top,"v",BLUE)
        cylinder = GaussianCylinder()
        ell_dim = DoubleArrow([-2.3,1.45,0],[2.3,1.45,0],buff=0,color=MUTED,stroke_width=2,tip_length=0.13)
        ell_label = mt(r"\ell",size=37).move_to([0,1.12,0])
        rdim = DashedLine([0,CY,0],[0,CY-1,0],color=MUTED)
        rlabel = mt("d",size=33).move_to([0.35,CY-0.6,0])
        gtag = text("GAUSS · SUPERFÍCIE FECHADA",27,VIOLET).move_to([0,0.35,0])
        self.play(Create(cylinder),GrowArrow(ell_dim),FadeIn(ell_label,gtag),Create(rdim),FadeIn(rlabel),run_time=0.85)
        self.checkpoint("04_cilindro_horizontal")
        field = VGroup(*[vec(surface_point(x,t),surface_point(x,t,r=1.65),CYAN,4)
                         for x,t in ((-1.2,0),(0.8,0),(-1.2,PI),(1.2,PI),(-0.6,PI/2),(0.7,3*PI/2))])
        elab = mt(r"\vec E",size=36,color=CYAN).move_to([-1.55,5.2,0])
        patch = Polygon(*[surface_point(x,t) for x,t in ((-0.15,-0.18),(0.35,-0.18),(0.35,0.18),(-0.15,0.18))],color=VIOLET,fill_opacity=0.5,stroke_width=2)
        normal = vec(surface_point(0.1,0),surface_point(0.1,0,r=1.65),VIOLET,4)
        alab = mt(r"d\vec A",size=32,color=VIOLET).move_to([0.15,5.53,0])
        seq = mt(r"\vec E\parallel d\vec A",r"\quad\Rightarrow\quad",r"\vec E\cdot d\vec A=E\,dA",y=-1.05,size=43)
        self.play(LaggedStart(*[GrowArrow(a) for a in field],lag_ratio=0.12),FadeIn(elab),
                  Create(patch),GrowArrow(normal),FadeIn(alab),Write(seq),run_time=0.85)
        self.checkpoint("06_lateral_E_paralelo_dA",1.2)
        self.play(FadeOut(seq,patch,normal,alab,field,elab),run_time=0.35)
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
        cmsg = text("Cada tampa tem fluxo zero individualmente",26).move_to([0,-4.1,0])
        self.play(*[GrowArrow(a) for cap in cv for a in cap[:2]],
                  FadeIn(*[m for cap in cv for m in cap[2:]],cnames,cmsg),
                  Create(angles),Write(czeros),Write(perp),run_time=0.85)
        self.checkpoint("08_duas_tampas_zero_individual",1.2)
        self.heading("Só a lateral contribui")
        self.play(FadeOut(cv,angles,cnames,czeros,perp,cmsg),cylinder.body.animate.set_fill(opacity=0.22),cylinder.caps.animate.set_fill(opacity=0.025),run_time=0.55)
        gauss = mt(r"\oint_{\mathcal S}\vec E\cdot d\vec A","=",r"\frac{Q_{\rm env}}{\varepsilon_0}",y=MATH_Y,size=55)
        qenv = mt(r"Q_{\rm env}","=",r"\lambda\ell",y=SECONDARY_Y,size=48)
        self.play(Write(gauss),run_time=0.65)
        self.checkpoint("Gauss_lei_integral", equation=" ".join(gauss.tex_strings))
        self.play(TransformFromCopy(top.density,qenv[2][0]),TransformFromCopy(ell_label,qenv[2][1]),Write(qenv[:2]),run_time=0.7)
        self.checkpoint("Gauss_carga_encerrada", equation=" ".join(qenv.tex_strings))
        flux = mt(r"\oint_{\mathcal S}\vec E\cdot d\vec A","=",r"E A_{\rm lat}",y=SECONDARY_Y,size=48)
        self.play(FadeOut(qenv),Write(flux),Indicate(cylinder.body,color=VIOLET),run_time=0.8)
        self.checkpoint("Gauss_fluxo_E_A_lateral", equation=" ".join(flux.tex_strings))
        applied = mt(r"E A_{\rm lat}","=",r"\frac{\lambda\ell}{\varepsilon_0}",y=MATH_Y,size=56)
        gauss = self.step(gauss,applied,"Gauss_carga_substituida")
        area = mt(r"A_{\rm lat}","=",r"2\pi d\ell",y=SECONDARY_Y,size=50)
        self.play(FadeOut(flux),Write(area),Indicate(ell_dim,color=CYAN),Indicate(rdim,color=CYAN),run_time=0.8)
        self.checkpoint("Gauss_area_lateral_explicita", equation=" ".join(area.tex_strings))
        g = GlyphEq(r"E(2\pi d\ell)","=",r"\frac{\lambda\ell}{\varepsilon_0}",size=58)
        self.play(TransformMatchingTex(gauss,g.mob),FadeOut(area),run_time=1.0)
        self.checkpoint("Gauss_area_carga_substituidas", equation=" ".join(g.parts))
        left_ids = g.p(0); gn,gb,gd = g.frac(2)
        le,re = [left_ids[-2]],[gn[-1]]
        assert len(gn)==2 and len(gd)==2
        cuts = VGroup(*[Line(g.group(ids).get_corner(DL),g.group(ids).get_corner(UR),color=CYAN,stroke_width=3) for ids in (le,re)])
        self.play(Indicate(g.group(le),color=CYAN),Indicate(g.group(re),color=CYAN),Create(cuts),run_time=0.65)
        self.checkpoint("10_cancelar_ell_Gauss")
        reduced = GlyphEq(r"E(2\pi d)","=",r"\frac{\lambda}{\varepsilon_0}",size=58)
        rn,rb,rd = reduced.frac(2)
        g = self.glyph(g,reduced,([i for i in left_ids if i not in le],reduced.p(0)),(g.p(1),reduced.p(1)),([gn[0]],rn),(gb,rb),(gd,rd),extras=(FadeOut(cuts),))
        self.checkpoint("Gauss_apos_cancelar_ell", equation=" ".join(reduced.parts))
        eg = GlyphEq("E(d)","=",r"\frac{\lambda}{2\pi\varepsilon_0d}",size=61)
        en,ebar,eden = eg.frac(2)
        lp = g.p(0)
        g = self.glyph(g,eg,(lp[:2],eg.p(0)[:2]),([lp[-1]],[eg.p(0)[-1]]),
                       (g.p(1),eg.p(1)),(rn,en),(rb,ebar),(rd,eden[2:4]),
                       rt=1.1,local_fade=True)
        ef = eg.mob
        ebox = boxed(ef); self.play(Create(ebox),run_time=0.4)
        self.checkpoint("11_campo_E_d",0.8)

        self.block("forca_eletrica")
        self.heading("Campo da linha 1, força na linha 2")
        self.play(FadeOut(cylinder,ell_dim,ell_label,rdim,rlabel,gtag),top.y.animate.set_value(4),FadeIn(bottom,dim,d_label,top.name),run_time=0.7)
        segment = Line([-1.6,1.45,0],[0.6,1.45,0],color=CYAN,stroke_width=7)
        brace = Brace(segment,DOWN,buff=0.17,color=MUTED)
        sl = mt(r"\ell",size=35).next_to(brace,DOWN,buff=0.08).shift(LEFT*0.65)
        ea = vec([-0.45,1.45,0],[-0.45,-0.1,0],CYAN)
        eal = mt(r"\vec E_1(d)",size=34,color=CYAN).move_to([0.55,0.65,0])
        qe = mt("q","=",r"\lambda\ell",size=54,y=MATH_Y)
        self.play(ef.animate.scale(0.68).move_to([0,SECONDARY_Y,0]),FadeOut(ebox),run_time=0.45)
        self.play(Create(segment),GrowFromCenter(brace),FadeIn(sl),GrowArrow(ea),FadeIn(eal),Write(qe),run_time=0.7)
        self.checkpoint("12_campo_externo_e_carga_trecho")
        fe = self.step(qe,mt("F_E","=","qE",size=57,y=MATH_Y),"eletrica_F_qE")
        fe = self.step(fe,mt("F_E","=",r"(\lambda\ell)E(d)",size=57,y=MATH_Y),"eletrica_substituir_carga")
        product = GlyphEq("F_E","=",r"\lambda\ell",r"\frac{\lambda}{2\pi\varepsilon_0d}",size=58)
        self.play(TransformMatchingTex(fe,product.mob),Indicate(ef,color=CYAN),run_time=1.0)
        self.checkpoint("eletrica_substituir_E", equation=" ".join(product.parts))
        combined = GlyphEq("F_E","=",r"\frac{\lambda^2\ell}{2\pi\varepsilon_0d}",size=60)
        pn,pb,pd = product.frac(3); fn,fb,fd = combined.frac(2)
        self.glyph(product,combined,(product.p(0),combined.p(0)),(product.p(1),combined.p(1)),
                   ([product.p(2)[0],pn[0]],fn[:2]),([product.p(2)[1]],fn[-1:]),(pb,fb),(pd,fd))
        self.checkpoint("eletrica_multiplicar_lambda", equation=" ".join(combined.parts))
        per_length = GlyphEq(r"\frac{F_E}{\ell}","=",r"\frac{\lambda^2}{2\pi\varepsilon_0d}",size=61)
        ln,lb,ld = per_length.frac(0); rn,rb,rd = per_length.frac(2)
        self.glyph(combined,per_length,(combined.p(0),ln),(combined.p(1),per_length.p(1)),
                   (fn[:2],rn),(fn[-1:],ld),(fb,rb),(fd,rd),extras=(FadeOut(ef),),rt=1.15)
        fer = per_length.mob.set_color(CYAN)
        self.play(Transform(eal,mt("F_E",size=35,color=CYAN).move_to([0.2,0.55,0])),run_time=0.4)
        feb = boxed(fer); self.play(Create(feb),run_time=0.35)
        self.checkpoint("13_forca_eletrica",0.6)
        self.block("superficie_curva")
        self.heading("Mesma simetria, outra construção")
        self.play(FadeOut(bottom,dim,d_label,segment,brace,sl,ea,eal,feb,fer,top.name),top.y.animate.set_value(CY),FadeIn(cylinder),run_time=0.7)
        sr = mt(r"\vec E\cdot d\vec A",size=54,color=CYAN,y=MATH_Y)
        sw = text("atravessa uma superfície",29).move_to([0,SECONDARY_Y,0])
        section = ring(0,color=VIOLET,fill=0.1).set_stroke(width=4)
        section_label = text("seção transversal",27,VIOLET).move_to([0,1.7,0])
        self.play(Create(section),Write(sr),FadeIn(sw,section_label),FadeIn(rdim,rlabel),run_time=0.8)
        self.checkpoint("secao_marcada_no_cilindro_inteiro",0.6)
        self.motion_samples.append({"estado":"superficie_removida_secao_preservada", "tempo_s":round(float(self.time+self.beat_duration(1)/2),3)})
        self.play(cylinder.animate.set_opacity(0.12),run_time=1.0)
        acurve = section
        cr = mt(r"\vec B\cdot d\vec\ell",size=54,color=MAGENTA,y=MATH_Y)
        self.play(FadeOut(cylinder),acurve.animate.set_fill(opacity=0).set_stroke(width=4.5),FadeOut(section_label),
                  TransformMatchingTex(sr,cr),Transform(sw,text("percorre uma curva",29).move_to([0,SECONDARY_Y,0])),FadeIn(top.name),run_time=0.9)
        self.checkpoint("15_superficie_para_curva")
        self.block("Ampere")
        self.play(FadeOut(cr,sw),run_time=0.35)
        self.flow(top,"I",MAGENTA); self.heading("B contorna a corrente")
        orbit = ring(0,r=1.23,color=MAGENTA).set_stroke(width=1.5,opacity=0.45)
        tangents = VGroup()
        for t in (0.22,PI/2,PI+0.22,3*PI/2):
            p = surface_point(0,t,r=1.23)
            tangent = np.array([0.4*np.cos(t),-np.sin(t)-0.22*np.cos(t),0]); tangent /= np.linalg.norm(tangent)
            tangents.add(vec(p-tangent*0.23,p+tangent*0.23,MAGENTA,4))
        atag = text("AMPÈRE · CURVA FECHADA",27,VIOLET).move_to([0,1.65,0])
        ol = mt(r"\vec B",size=37,color=MAGENTA).move_to([-1.2,4.7,0])
        self.play(Create(orbit),LaggedStart(*[GrowArrow(a) for a in tangents],lag_ratio=0.15),FadeIn(atag,ol),run_time=0.85)
        parallel = mt(r"\vec B\parallel d\vec\ell",size=56,y=MATH_Y)
        const_note = VGroup(mt("B=",size=43,color=MAGENTA),text("constante ao longo da curva",27)).arrange(RIGHT,buff=0.18).move_to([0,SECONDARY_Y,0])
        dl = tangents[0].copy().set_color(VIOLET).shift(DOWN*0.16)
        dll = mt(r"d\vec\ell",size=35,color=VIOLET).next_to(dl,RIGHT,buff=0.12)
        self.play(Write(parallel),FadeIn(const_note),GrowArrow(dl),FadeIn(dll),run_time=0.7)
        self.checkpoint("Ampere_B_paralelo_dl_constante",0.7, equation=r"\vec B\parallel d\vec\ell")
        circulation = mt(r"\oint_{\mathcal C}\vec B\cdot d\vec\ell","=",r"\mu_0I_{\rm enc}",size=57,y=MATH_Y)
        self.play(TransformMatchingTex(parallel,circulation),FadeOut(const_note,dl,dll),run_time=0.9)
        self.checkpoint("Ampere_lei_integral", equation=" ".join(circulation.tex_strings))
        ie = mt(r"I_{\rm enc}","=","I",size=50,y=SECONDARY_Y)
        self.play(Write(ie),Indicate(top.flow_arrow,color=MAGENTA),run_time=0.7)
        self.checkpoint("Ampere_corrente_encerrada", equation=" ".join(ie.tex_strings))
        circulation = self.step(circulation,mt(r"\oint_{\mathcal C}\vec B\cdot d\vec\ell","=",r"\mu_0I",size=57,y=MATH_Y),"Ampere_I_substituido")
        factor = mt(r"\oint_{\mathcal C}\vec B\cdot d\vec\ell","=",r"B\oint_{\mathcal C}d\ell",size=57,y=MATH_Y)
        self.play(TransformMatchingTex(circulation,factor),FadeOut(ie),run_time=1.0)
        self.checkpoint("Ampere_retirar_B_da_integral", equation=" ".join(factor.tex_strings))
        reduced_integral = mt(r"B\oint_{\mathcal C}d\ell","=",r"\mu_0I",size=57,y=MATH_Y)
        circulation = self.step(factor,reduced_integral,"Ampere_B_integral_igual_muI")
        circumference = mt(r"\oint_{\mathcal C}d\ell","=",r"2\pi d",size=53,y=SECONDARY_Y)
        self.play(Write(circumference),Indicate(acurve,color=VIOLET),run_time=0.7)
        self.checkpoint("Ampere_comprimento_curva", equation=" ".join(circumference.tex_strings))
        bstep = mt("B(d)",r"(2\pi d)","=",r"\mu_0I",size=59,y=MATH_Y)
        self.play(TransformMatchingTex(circulation,bstep),FadeOut(circumference),run_time=1.0)
        self.checkpoint("Ampere_substituir_circunferencia", equation=" ".join(bstep.tex_strings))
        bg = GlyphEq("B(d)",r"(2\pi d)","=",r"\mu_0I",size=59)
        self.remove(bstep); self.add(bg.mob)
        br = GlyphEq("B(d)","=",r"\frac{\mu_0I}{2\pi d}",size=61)
        bnum,bbar,bden = br.frac(2)
        self.glyph(bg,br,(bg.p(0),br.p(0)),(bg.p(1)[1:-1],bden),(bg.p(2),br.p(1)),(bg.p(3),bnum),rt=1.15)
        bf = br.mob
        bbox = boxed(bf,MAGENTA); self.play(Create(bbox),run_time=0.4)
        self.checkpoint("18_campo_B_d",0.7)
        self.block("mao_direita_forca_magnetica")
        self.heading("Regra da mão direita")
        # Resultados locais explícitos; a elipse é apenas apoio à circulação.
        above = VGroup(mt(r"\odot",size=52,color=MAGENTA),text("B sai da tela",25,MAGENTA)).arrange(RIGHT,buff=0.18).move_to([-1.4,5.15,0])
        below = VGroup(mt(r"\otimes",size=52,color=MAGENTA),text("B entra na tela",25,MAGENTA)).arrange(RIGHT,buff=0.18).move_to([-1.4,1.95,0])
        current_axis = mt(r"+\hat x",size=35,color=MAGENTA).move_to([3.5,4.05,0])
        moving = Dot(surface_point(0,0,r=1.23),radius=0.08,color=MAGENTA)
        self.play(FadeIn(above,below,moving,current_axis),FadeOut(ol),Indicate(top.flow_arrow,color=MAGENTA),run_time=0.45)
        self.motion_samples.append({"estado":"enrolamento_B", "tempo_s":round(float(self.time+self.beat_duration(2)/2),3)})
        self.play(MoveAlongPath(moving,orbit),above.animate.set_opacity(0.28),run_time=2.0,rate_func=linear)
        self.checkpoint("17_regra_mao_direita_enrolamento")

        self.heading("Abaixo da linha 1: B entra na tela")
        self.play(FadeOut(acurve,orbit,tangents,atag,rdim,rlabel,moving,above,below,current_axis),top.y.animate.set_value(4),FadeIn(bottom,dim,d_label),run_time=0.7)
        self.flow(bottom,"I",MAGENTA)
        evaluation = Dot([-0.45,1.45,0],color=WHITE,radius=0.055)
        marker = VGroup(Circle(radius=0.27,color=BACKGROUND_COLOR,fill_opacity=1,fill_color=BACKGROUND_COLOR,stroke_width=0),mt(r"\otimes",size=57,color=MAGENTA)).move_to([-1.65,2.05,0])
        marker[0].set_z_index(1)
        marker[1].set_z_index(2)
        point_label = mt("P",size=31).move_to([-0.15,1.05,0])
        ml = mt(r"\vec B_1(d)=-B\hat z",size=41,color=MAGENTA).move_to([1.35,2.55,0])
        self.play(FadeIn(evaluation,point_label),TransformFromCopy(below[0],marker[1]),FadeIn(marker[0]),Write(ml),run_time=0.85)
        self.checkpoint("19_B_entra_sem_sobreposicao",0.8)
        self.heading("A força aponta para a outra linha")
        self.play(FadeOut(bf,bbox,point_label),run_time=0.45)
        lv = vec([-1.15,1.1,0],[0.25,1.1,0],WHITE,4)
        lvl = mt(r"\vec\ell=\ell\hat x",size=40).move_to([1.9,0.9,0])
        ba = vec([-0.45,1.45,0],[-0.45,3,0],MAGENTA)
        bal = mt(r"\vec F_B",size=36,color=MAGENTA).move_to([0.2,2.1,0])
        cross = mt(r"\vec F_B","=",r"I\vec\ell",r"\times",r"\vec B_1(d)",size=58,y=MATH_Y)
        cross[0].set_color(MAGENTA); cross[4].set_color(MAGENTA)
        direction = mt(r"+\hat x\times(-\hat z)=+\hat y",size=52,y=SECONDARY_Y)
        self.play(GrowArrow(lv),FadeIn(lvl),Write(cross[:2]),run_time=0.55)
        self.play(TransformFromCopy(lv,cross[2]),Write(cross[3]),TransformFromCopy(marker[1],cross[4]),run_time=0.7)
        self.play(Write(direction),GrowArrow(ba),FadeIn(bal),run_time=0.65)
        self.checkpoint("20_produto_vetorial_atracao",0.8)
        self.play(FadeOut(marker,ml,lv,lvl,direction),run_time=0.45)
        cross = self.step(cross,mt("F_B","=",r"I\ell B\sin90^\circ",size=58,y=MATH_Y),"magnetica_seno_90")
        cross = self.step(cross,mt("F_B","=",r"I\ell B",size=58,y=MATH_Y),"magnetica_modulo_I_ell_B")
        bref = mt("B(d)","=",r"\frac{\mu_0I}{2\pi d}",size=44,color=MAGENTA,y=SECONDARY_Y)
        self.play(FadeIn(bref),run_time=0.45)
        mprod = GlyphEq("F_B","=",r"I\ell",r"\frac{\mu_0I}{2\pi d}",size=60)
        self.play(TransformMatchingTex(cross,mprod.mob),Indicate(bref,color=MAGENTA),run_time=1.0)
        self.checkpoint("magnetica_substituir_B", equation=" ".join(mprod.parts))
        mcomb = GlyphEq("F_B","=",r"\frac{\mu_0I^2\ell}{2\pi d}",size=61)
        mn,mb,md = mprod.frac(3); cn,cb,cd = mcomb.frac(2)
        self.glyph(mprod,mcomb,(mprod.p(0),mcomb.p(0)),(mprod.p(1),mcomb.p(1)),(mn[:2],cn[:2]),
                   ([mprod.p(2)[0],mn[-1]],cn[2:4]),([mprod.p(2)[1]],cn[-1:]),(mb,cb),(md,cd))
        self.checkpoint("magnetica_multiplicar_I", equation=" ".join(mcomb.parts))
        mper = GlyphEq(r"\frac{F_B}{\ell}","=",r"\frac{\mu_0I^2}{2\pi d}",size=61)
        ln,lb,ld = mper.frac(0); rn,rb,rd = mper.frac(2)
        self.glyph(mcomb,mper,(mcomb.p(0),ln),(mcomb.p(1),mper.p(1)),(cn[:-1],rn),
                   (cn[-1:],ld),(cb,rb),(cd,rd),extras=(FadeOut(bref),),rt=1.15)
        fbr = mper.mob.set_color(MAGENTA)
        fbb = boxed(fbr,MAGENTA); self.play(Create(fbb),run_time=0.35)
        self.checkpoint("21_forca_magnetica",0.6)
        self.block("igualdade_payoff_c")
        self.heading("Atração e repulsão coexistem")
        ea = vec([-0.45,1.45,0],[-0.45,-0.1,0],CYAN)
        eal = mt("F_E",size=36,color=CYAN).move_to([-1.05,0.55,0])
        fec_eq = GlyphEq(r"\frac{F_E}{\ell}","=",r"\frac{\lambda^2}{2\pi\varepsilon_0d}",size=55,y=SECONDARY_Y)
        fec = fec_eq.mob.set_color(CYAN)
        self.play(GrowArrow(ea),FadeIn(eal),TransformFromCopy(fer,fec),run_time=0.8)
        self.checkpoint("22_comparacao_forcas_origem_comum",0.6)

        self.heading("Quando os módulos seriam iguais?")
        bal_eq = GlyphEq(r"\frac{\lambda^2}{2\pi\varepsilon_0d}","=",r"\frac{\mu_0I^2}{2\pi d}",size=61)
        lhs, equals, rhs = (bal_eq.group(bal_eq.p(i)) for i in range(3))
        self.play(TransformFromCopy(fec_eq.group(fec_eq.p(2)),lhs),TransformFromCopy(mper.group(mper.p(2)),rhs),
                  Write(equals),FadeOut(fec,fbr,fbb,dim,d_label),run_time=1.15)
        self.remove(lhs,equals,rhs); self.add(bal_eq.mob)
        an,ab,ad = bal_eq.frac(0); bn,bb,bd = bal_eq.frac(2)
        assert (len(an),len(ad),len(bn),len(bd))==(2,5,4,3)
        slashes = VGroup()
        for ids in (ad[:2]+ad[-1:],bd):
            bal_eq.group(ids).set_color(CYAN)
            for k in ids:
                gl = bal_eq.mob[0][k]
                slashes.add(Line(gl.get_corner(DL)+0.03*DL,gl.get_corner(UR)+0.03*UR,color=CYAN,stroke_width=2.5))
        self.play(Create(slashes),run_time=0.45)
        cc = mt(r"2\pi d",size=38,color=CYAN,y=-3.2); self.play(FadeIn(cc),run_time=0.35)
        self.checkpoint("23_cancelamento_2pi_d")
        red = GlyphEq(r"\frac{\lambda^2}{\varepsilon_0}","=",r"\mu_0I^2",size=61)
        rn,rb,rd = red.frac(0)
        bal_eq = self.glyph(bal_eq,red,(an,rn),(ab,rb),(ad[2:4],rd),(bal_eq.p(1),red.p(1)),(bn,red.p(2)),extras=(FadeOut(slashes),FadeOut(cc)))
        self.checkpoint("24_termos_sobreviventes")
        product_constants = GlyphEq(r"\lambda^2","=",r"\mu_0\varepsilon_0I^2",size=61)
        rhs = red.p(2)
        self.glyph(red,product_constants,(rn,product_constants.p(0)),(red.p(1),product_constants.p(1)),
                   (rhs[:2],product_constants.p(2)[:2]),(rd,product_constants.p(2)[2:4],{"path_arc":PI/3}),
                   (rhs[2:],product_constants.p(2)[4:]),rt=1.2)
        self.checkpoint("cancelamento_epsilon_multiplica", equation=" ".join(product_constants.parts))
        reorg = GlyphEq(r"\frac{I^2}{\lambda^2}","=",r"\frac{1}{\mu_0\varepsilon_0}",size=61)
        xn,xb,xd = reorg.frac(0); yn,yb,yd = reorg.frac(2); rhs = red.p(2)
        rhs = product_constants.p(2)
        bal_eq = self.glyph(product_constants,reorg,(product_constants.p(0),xd,{"path_arc":-PI/3}),
                            (product_constants.p(1),reorg.p(1)),(rhs[:4],yd),(rhs[4:],xn,{"path_arc":PI/3}),rt=1.2)
        self.checkpoint("25_reorganizacao_I2_lambda2")
        root = GlyphEq(r"\frac{|I|}{|\lambda|}","=",r"\frac{1}{\sqrt{\mu_0\varepsilon_0}}",size=61)
        un,ub,ud = root.frac(0); vn,vb,vd = root.frac(2)
        assert len(un)==3 and len(ud)==3
        bal_eq = self.glyph(reorg,root,([xn[0]],[un[1]]),(xb,ub),([xd[0]],[ud[1]]),(reorg.p(1),root.p(1)),
                            (yn,vn),(yb,vb),(yd,root.p(2)[-4:]),rt=1.0)
        self.checkpoint("raiz_modulos_antes_de_c", equation=" ".join(root.parts))
        cdef = mt(r"c=\frac{1}{\sqrt{\mu_0\varepsilon_0}}",size=45,color=CYAN,y=SECONDARY_Y); self.play(Write(cdef),run_time=0.65)
        self.checkpoint("identificar_c", equation=" ".join(cdef.tex_strings))
        saved_cdef = cdef.copy()
        payoff = GlyphEq(r"\frac{|I|}{|\lambda|}","=","c",size=77)
        c_copy = root.copied_reference(cdef[0][:1])
        bal_eq = self.glyph(root,payoff,(root.p(0),payoff.p(0)),(root.p(1),payoff.p(1)),(c_copy,payoff.p(2)),rt=0.9)
        pbox = boxed(payoff.mob); self.play(Create(pbox),run_time=0.4)
        self.checkpoint("26_payoff_I_lambda_c",1.8)
        self.block("corrente_payoff_v")
        self.heading("Volte ao movimento das cargas")
        phrase = VGroup(text("Mas aqui a corrente é produzida justamente",27),text("pela própria linha de carga em movimento.",27)).arrange(DOWN,buff=0.12).move_to([0,-4.2,0])
        self.play(*[Transform(line.flow_label,mt("v",size=36,color=BLUE).move_to(line.flow_label.get_center())) for line in (top,bottom)],
                  *[line.flow_arrow.animate.set_color(BLUE) for line in (top,bottom)],
                  Indicate(top.particles,color=CYAN),FadeOut(cdef),FadeIn(phrase),run_time=0.8)
        self.checkpoint("27_retorno_movimento_cargas",1.2)
        saved_payoff = payoff.mob.copy()
        self.play(FadeOut(payoff.mob,pbox,phrase,ea,eal,ba,bal,evaluation),run_time=0.55)
        fixed = Dot([0.6,1.45,0],radius=0.08,color=WHITE)
        fixed_label = mt("P",size=35).move_to([0.6,0.95,0])
        swept = ValueTracker(0)
        length = 1.5
        moving_segment = always_redraw(lambda:Line([-0.9+swept.get_value()*length,1.45,0],
                                                   [0.6+swept.get_value()*length,1.45,0],color=CYAN,stroke_width=8))
        moving_brace = always_redraw(lambda:Brace(moving_segment,UP,buff=0.15,color=MUTED))
        swept_label = mt(r"v\Delta t",size=39,color=CYAN)
        swept_label.add_updater(lambda m:m.next_to(moving_brace,UP,buff=0.38))
        dt_label = mt(r"\Delta t",size=53,y=MATH_Y)
        self.play(FadeIn(fixed,fixed_label,moving_segment,moving_brace,swept_label),Write(dt_label),run_time=0.7)
        self.motion_samples.append({"estado":"trecho_v_Delta_t_atravessa_P", "tempo_s":round(float(self.time+self.beat_duration(1.4)/2),3)})
        self.play(swept.animate.set_value(1),Indicate(fixed,color=CYAN),run_time=1.4,rate_func=linear)
        self.checkpoint("corrente_trecho_v_Delta_t_ponto_fixo")
        dq = mt(r"\Delta q","=",r"\lambda v\Delta t",size=58,y=MATH_Y)
        self.play(TransformMatchingTex(dt_label,dq),run_time=0.9)
        self.checkpoint("corrente_carga_que_atravessa", equation=" ".join(dq.tex_strings))
        current = self.step(dq,mt("I","=",r"\frac{\Delta q}{\Delta t}",size=61,y=MATH_Y),"corrente_definicao_Delta_q_Delta_t")
        time_sub = GlyphEq("I","=",r"\frac{\lambda v\Delta t}{\Delta t}",size=61)
        self.play(TransformMatchingTex(current,time_sub.mob),run_time=1.0)
        self.checkpoint("corrente_substituir_carga", equation=" ".join(time_sub.parts))
        tn,tb,td = time_sub.frac(2)
        cuts = self.struck(time_sub,(tn[-2:],td))
        self.checkpoint("corrente_cancelar_Delta_t")
        plain_current = GlyphEq("I","=",r"\lambda v",size=65)
        self.glyph(time_sub,plain_current,(time_sub.p(0),plain_current.p(0)),(time_sub.p(1),plain_current.p(1)),
                   (tn[:2],plain_current.p(2)),extras=(FadeOut(cuts),))
        self.checkpoint("corrente_I_lambda_v", equation=" ".join(plain_current.parts))
        relation = GlyphEq(r"|I|","=",r"|\lambda|v",size=65)
        self.glyph(plain_current,relation,(plain_current.p(0),[relation.p(0)[1]]),
                   (plain_current.p(1),relation.p(1)),([plain_current.p(2)[0]],[relation.p(2)[1]]),
                   ([plain_current.p(2)[1]],[relation.p(2)[-1]]))
        rbox = boxed(relation.mob)
        self.play(Create(rbox),run_time=0.35)
        self.checkpoint("28_corrente_lambda_v",0.4, equation=" ".join(relation.parts))
        motion_ratio = GlyphEq(r"\frac{|I|}{|\lambda|}","=","v",size=68)
        cn,cb,cd = motion_ratio.frac(0)
        self.glyph(relation,motion_ratio,(relation.p(0),cn),(relation.p(1),motion_ratio.p(1)),
                   (relation.p(2)[-1:],motion_ratio.p(2)),extras=(FadeOut(rbox),),rt=1.2,local_fade=True)
        self.checkpoint("corrente_I_sobre_lambda_igual_v", equation=" ".join(motion_ratio.parts))
        recovered = GlyphEq(r"\frac{|I|}{|\lambda|}","=","c",size=48,y=SECONDARY_Y)
        self.play(TransformFromCopy(saved_payoff,recovered.mob),
                  Indicate(motion_ratio.group(motion_ratio.p(0)),color=CYAN),run_time=0.9)
        self.checkpoint("recuperar_primeiro_payoff_mesmo_lado_esquerdo",0.4)
        joined = GlyphEq("v","=",r"\frac{|I|}{|\lambda|}","=","c",size=66)
        self.glyph(motion_ratio,joined,(motion_ratio.p(1),joined.p(3)),
                   (motion_ratio.p(0),joined.p(2)),extras=(FadeOut(recovered.mob),),rt=1.2,local_fade=True)
        self.checkpoint("v_igual_razao_igual_c", equation=" ".join(joined.parts))
        vp = GlyphEq("v","=","c",size=84*1.225)
        bal_eq = self.glyph(joined,vp,(joined.p(0),vp.p(0)),(joined.p(1),vp.p(1)),(joined.p(4),vp.p(2)),
                            extras=(FadeOut(fixed,fixed_label,moving_segment,moving_brace,swept_label),),rt=1.2)
        vbox = SurroundingRectangle(vp.mob,buff=0.2*1.225,corner_radius=0.1,color=CYAN,stroke_width=2.5)
        self.play(Create(vbox),run_time=0.4)
        self.checkpoint("29_payoff_v_c",1.8)

        self.block("derivacao_razao")
        self.play(FadeOut(vp.mob,vbox),run_time=0.4)
        self.heading("Compare os módulos das forças")
        divided = GlyphEq(r"\frac{F_B}{F_E}","=",r"\dfrac{\dfrac{\mu_0I^2}{2\pi d}}{\dfrac{\lambda^2}{2\pi\varepsilon_0d}}",size=57)
        self.play(TransformFromCopy(VGroup(fbr,fer),divided.mob),run_time=0.9)
        self.checkpoint("razao_divisao_expressoes_completa",0.4, equation=" ".join(divided.parts))
        (un,ub,ud),(dn,db,dd),outer = divided.nested_frac(2)
        assert (len(un),len(ud),len(dn),len(dd)) == (4,3,2,5)
        cuts = self.struck(divided,[[k] for k in ud+dd[:2]+dd[-1:]])
        self.checkpoint("razao_cancelar_2pi_d")
        ra = GlyphEq(r"\frac{F_B}{F_E}","=",r"\mu_0\varepsilon_0",r"\frac{I^2}{\lambda^2}",size=58)
        an,ab,ad = ra.frac(3)
        self.glyph(divided,ra,(divided.p(0),ra.p(0)),(divided.p(1),ra.p(1)),
                   (un[2:],an),(dn,ad),extras=(FadeOut(cuts),),rt=1.2,local_fade=True)
        self.checkpoint("razao_mu_epsilon_I2_lambda2", equation=" ".join(ra.parts))
        rref = GlyphEq(r"\frac{|I|}{|\lambda|}","=","v",size=47,y=SECONDARY_Y)
        self.play(TransformFromCopy(motion_ratio.mob,rref.mob),run_time=0.7)
        self.checkpoint("razao_recuperar_I_lambda_v", equation=" ".join(rref.parts))
        squared = GlyphEq(r"\frac{I^2}{\lambda^2}","=","v^2",size=47,y=SECONDARY_Y)
        abs_n,abs_b,abs_d = rref.frac(0); sq_n,sq_b,sq_d = squared.frac(0)
        self.glyph(rref,squared,([abs_n[1]],[sq_n[0]]),(abs_b,sq_b),([abs_d[1]],[sq_d[0]]),
                   (rref.p(1),squared.p(1)),(rref.p(2),squared.p(2)[:1]))
        self.checkpoint("razao_elevar_ao_quadrado", equation=" ".join(squared.parts))
        rbeta = GlyphEq(r"\frac{F_B}{F_E}","=",r"\mu_0\varepsilon_0","v^2",size=58)
        v2_copy = ra.copied_reference(squared.group(squared.p(2)))
        self.glyph(ra,rbeta,*[(ra.p(i),rbeta.p(i)) for i in range(3)],(v2_copy,rbeta.p(3)))
        self.checkpoint("razao_mu_epsilon_v2", equation=" ".join(rbeta.parts))
        constants = mt(r"\mu_0\varepsilon_0","=",r"\frac1{c^2}",size=48,y=SECONDARY_Y)
        self.play(FadeOut(squared.mob),TransformFromCopy(saved_cdef,constants),run_time=0.9)
        self.checkpoint("razao_recuperar_constantes_c", equation=" ".join(constants.tex_strings))
        reciprocal = GlyphEq(r"\frac{F_B}{F_E}","=",r"\frac{1}{c^2}","v^2",size=58)
        inverse_copy = rbeta.copied_reference(constants[2])
        self.glyph(rbeta,reciprocal,(rbeta.p(0),reciprocal.p(0)),(rbeta.p(1),reciprocal.p(1)),
                   (inverse_copy,reciprocal.p(2)),(rbeta.p(3),reciprocal.p(3)))
        self.checkpoint("razao_substituir_1_c2", equation=" ".join(reciprocal.parts))
        ratio_g = GlyphEq(r"\frac{F_B}{F_E}","=",r"\frac{v^2}{c^2}",size=62)
        pn,pb,pd = reciprocal.frac(2); fn,fb,fd = ratio_g.frac(2)
        self.glyph(reciprocal,ratio_g,(reciprocal.p(0),ratio_g.p(0)),(reciprocal.p(1),ratio_g.p(1)),
                   (reciprocal.p(3),fn),(pb,fb),(pd,fd),extras=(FadeOut(constants),))
        ratio_box = boxed(ratio_g.mob)
        self.play(Create(ratio_box),run_time=0.4)
        self.checkpoint("razao_final_antes_do_grafico",0.6, equation=" ".join(ratio_g.parts))
        self.block("grafico")
        self.heading("O que muda quando v/c varia?")
        graph_relation = GlyphEq(r"F_B/F_E","=",r"(v/c)^2",size=46,y=-0.15)
        ln,lb,ld = ratio_g.frac(0); rn,rb,rd = ratio_g.frac(2)
        gl,gr = graph_relation.p(0),graph_relation.p(2)
        # Frações viram formas compactas por fade local, sem convergir glifos
        # sobre as barras; a igualdade mantém a continuidade da expressão.
        self.glyph(ratio_g,graph_relation,(ratio_g.p(1),graph_relation.p(1)),
                   extras=(FadeOut(ratio_box),top.y.animate.set_value(4.5),bottom.y.animate.set_value(2.35)),
                   local_fade=True)
        model = text("MODELO IDEAL · linhas infinitas de carga",24,CYAN).move_to([0,5.6,0])
        qualifier = text("Parâmetro do modelo; não elétrons num fio real.",23,opacity=0.7).move_to([0,-5.28,0])
        qualitative = text("visualização qualitativa",25,opacity=0.7).move_to([0,0.3,0])
        self.play(FadeIn(model,qualifier,qualitative),run_time=0.4)
        beta = self.speed; self.play(beta.animate.set_value(0),run_time=0.4)
        # A referência fica fixa; a linha atual desloca-se de modo qualitativo.
        reference_y = 2.35
        bottom.y.add_updater(lambda m:m.set_value(reference_y-0.45*(1-beta.get_value()**2)))
        for line in (top,bottom):
            line.flow_arrow.clear_updaters()
            line.flow_arrow.add_updater(lambda m,line=line: m.put_start_and_end_on([1,line.y.get_value()+0.48,0],
                [1+1.5*max(beta.get_value(),0.001),line.y.get_value()+0.48,0]).set_opacity(1 if beta.get_value()>0.001 else 0))
            line.flow_label.clear_updaters()
            line.flow_label.add_updater(lambda m,line=line: m.move_to([1+1.5*beta.get_value()+0.35,line.y.get_value()+0.48,0]))
        axes = Axes(x_range=[0,1,0.5],y_range=[0,1,0.5],x_length=5.2,y_length=3,tips=False,
                    axis_config={"color":MUTED,"stroke_width":2,"include_ticks":False})
        axes.shift(GRAPH_ORIGIN-axes.c2p(0,0))
        ticks = VGroup(*[mt(str(t),size=31).move_to(axes.c2p(t,0)+DOWN*0.3) for t in (0,0.5,1)])
        labels = VGroup(mt("1",size=31).move_to(axes.c2p(0,1)+LEFT*0.35),
                        mt("v/c",size=37).move_to(axes.c2p(1,0)+RIGHT*0.65+DOWN*0.23),
                        mt(r"F_B/F_E",size=37).rotate(PI/2).move_to(axes.c2p(0,0.5)+LEFT*0.7))
        equal_line = DashedLine(axes.c2p(0,1),axes.c2p(1,1),color=VIOLET,stroke_width=1.5,dash_length=0.12).set_opacity(0.55)
        boundary = DashedLine(axes.c2p(1,0),axes.c2p(1,1),color=VIOLET,stroke_width=1.5,dash_length=0.12)
        endpoint = Circle(radius=0.09,color=VIOLET,stroke_width=2).move_to(axes.c2p(1,1))
        limit = VGroup(mt("v=c",size=33,color=VIOLET).move_to(axes.c2p(1,1)+RIGHT*0.7),
                       text("limite",25,VIOLET).move_to(axes.c2p(1,1)+RIGHT*0.7+DOWN*0.45))
        self.play(Create(axes),FadeIn(ticks,labels),Create(equal_line),Create(boundary),FadeIn(endpoint,limit),run_time=0.75)
        self.reached = 0.0001
        def plot():
            self.reached = max(self.reached,beta.get_value())
            return ParametricFunction(lambda t:axes.c2p(t,t*t),t_range=[0,self.reached],color=CYAN,stroke_width=4)
        curve = always_redraw(plot)
        point = always_redraw(lambda:Dot(axes.c2p(beta.get_value(),beta.get_value()**2),radius=0.095,color=CYAN))
        gx = always_redraw(lambda:DashedLine(axes.c2p(beta.get_value(),0),axes.c2p(beta.get_value(),max(beta.get_value()**2,0.0001)),color=CYAN,stroke_width=1.3,dash_length=0.1).set_opacity(0.5))
        bp = mt("v/c=",size=38).move_to([-2.2,-0.87,0])
        bv = DecimalNumber(0,num_decimal_places=3,font_size=38,color=CYAN).move_to([-0.85,-0.87,0])
        bv.add_updater(lambda m:m.set_value(beta.get_value()))
        fp = mt(r"F_B/F_E=",size=38).move_to([0.6,-0.87,0])
        fv = DecimalNumber(0,num_decimal_places=3,font_size=38,color=MAGENTA).move_to([2.4,-0.87,0])
        fv.add_updater(lambda m:m.set_value(beta.get_value()**2))
        def scaled_arrow(sign,amount,x,color):
            y, length = bottom.y.get_value(),1.4*amount
            return VGroup(vec([x,y,0],[x,y+sign*length,0],color)) if length>0.0001 else VGroup()
        ed = always_redraw(lambda:scaled_arrow(-1,1,-0.6,CYAN))
        bd = always_redraw(lambda:scaled_arrow(1,beta.get_value()**2,-0.6,MAGENTA))
        nd = always_redraw(lambda:scaled_arrow(-1,1-beta.get_value()**2,1,WHITE))
        names = VGroup(mt("F_E",size=37,color=CYAN),mt("F_B",size=37,color=MAGENTA),mt(r"F_{\rm liq}",size=35))
        names[0].add_updater(lambda m:m.move_to([-1.2,bottom.y.get_value()-0.8,0]))
        names[1].add_updater(lambda m:m.move_to([0,bottom.y.get_value()+0.7*beta.get_value()**2+0.25,0]).set_opacity(min(1,beta.get_value()**2/0.04)))
        net_plain = names[2].copy()
        net_positive = mt(r"F_{\rm liq}>0",size=35)
        def update_net_label(m):
            remainder = 1-beta.get_value()**2
            near_limit = remainder < 0.05
            m.become(net_positive if near_limit else net_plain)
            m.move_to([2.05 if near_limit else 1.8,
                       bottom.y.get_value()-(0.45 if near_limit else 0.7*remainder+0.25),0])
        names[2].add_updater(update_net_label)
        ghost = DashedLine([-2.4,reference_y,0],[0.5,reference_y,0],color=WHITE,stroke_width=2,dash_length=0.14).set_opacity(0.3)
        ghost_label = text("referência",23,opacity=0.6).move_to([-2.7,2.7,0])
        self.play(FadeIn(curve,point,gx,bp,bv,fp,fv,ed,bd,nd,names,ghost,ghost_label),run_time=0.55)
        self.checkpoint("30_grafico_beta_zero",0.2)
        for value,name,seconds,pause in ((0.6,"32_grafico_beta_intermediario",5.4,0.4),
                                        (0.95,"grafico_proximo_1",5,0),
                                        (0.995,"35_grafico_beta_0995",3.6,1)):
            self.motion_samples.append({"estado":f"grafico_durante_{value}", "tempo_s":round(float(self.time+self.beat_duration(seconds)/2),3)})
            self.play(beta.animate.set_value(value),run_time=seconds,rate_func=smooth)
            assert 0 <= beta.get_value() < 1
            self.checkpoint(name,pause)
            if value == 0.6:
                self.play(FadeOut(qualifier,qualitative),run_time=0.45)
        self.block("conclusao")
        self.heading("Para partículas massivas")
        bottom.y.clear_updaters()
        self.play(FadeOut(axes,ticks,labels,equal_line,boundary,endpoint,limit,curve,point,gx,bp,bv,fp,fv,ghost,ghost_label),
                  graph_relation.mob.animate.move_to([0,MATH_Y,0]),
                  beta.animate.set_value(0.6),top.y.animate.set_value(4.4),bottom.y.animate.set_value(2.1),run_time=1.2)
        condition = mt("v<c",size=59,y=0)
        self.play(Write(condition),run_time=0.65)
        self.checkpoint("36_particulas_massivas_v_menor_c",0.4)
        fr = GlyphEq(r"\frac{F_B}{F_E}","=",r"\frac{v^2}{c^2}","<1",size=63)
        ln,lb,ld = fr.frac(0); rn,rb,rd = fr.frac(2)
        gl,gr = graph_relation.p(0),graph_relation.p(2)
        squared_copy = graph_relation.copied_reference(graph_relation.group([gr[5]]))
        self.glyph(graph_relation,fr,(gl[:2],ln),(gl[3:],ld),
                   (graph_relation.p(1),fr.p(1)),([gr[1]],[rn[0]]),
                   ([gr[3]],[rd[0]]),([gr[5]],[rn[1]]),(squared_copy,[rd[1]]),rt=1.2)
        self.checkpoint("conclusao_razao_menor_1", equation=" ".join(fr.parts))
        force_order = mt("F_B","<","F_E",size=63,y=SECONDARY_Y)
        force_order[0].set_color(MAGENTA); force_order[2].set_color(CYAN)
        self.play(TransformFromCopy(fr.group(ln),force_order[0]),
                  TransformFromCopy(fr.group(fr.p(3)[:1]),force_order[1]),
                  TransformFromCopy(fr.group(ld),force_order[2]),run_time=0.85)
        self.remove(*force_order.submobjects); self.add(force_order)
        self.checkpoint("conclusao_F_B_menor_F_E")
        self.play(Transform(self.title,text("REPULSÃO LÍQUIDA",38).move_to([0,TITLE_Y,0])),
                  FadeOut(ed,bd,names[0],names[1],condition),run_time=0.4)
        self.checkpoint("37_repulsao_liquida_final",1.2)
        self.blocks[-1]["fim_s"] = round(float(self.time),3)
        metadata = {"duracao_cena_s":round(float(self.time),3),
            "referencia_visual":"vid_0014 — build_stage","MF_Tools":self.mf_steps,"estados":self.qa,
            "transicoes":self.motion_samples,"blocos":self.blocks,"ritmo":self.beats}
        output = "qa_ritmo_preflight_v4.json" if getattr(self,"timing_audit",False) else "qa_estados_v4.json"
        UNIT.joinpath(getattr(self,"qa_output",output)).write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding="utf-8")
