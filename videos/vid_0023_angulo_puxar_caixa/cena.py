"""vid_0023 — Qual o melhor ângulo para puxar uma caixa? (V0.4, preview silencioso).
Curto vertical, Manim-only. F(θ) = μ m g / (cos θ + μ sin θ); tan θ_ideal = μ.
"""
import sys
from contextlib import contextmanager
from pathlib import Path

import numpy as np
from manim import (
    Axes, Circle, Create, DashedLine, DecimalNumber, DOWN, DoubleArrow, FadeIn, FadeOut,
    ImageMobject, Indicate, LEFT, Line, MathTex, PI, Rectangle, ReplacementTransform,
    RIGHT, Scene, SurroundingRectangle, TransformMatchingTex, UP, ValueTracker, VGroup,
    VMobject, WHITE, Write, always_redraw, config, linear, smooth, Arrow, Dot, Transform,
)

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text

CYAN, VIOLET, PINK, DIM = PRIMARY_COLOR, '#9C8CFF', '#EA63FF', '#9AA6C5'
CYAN_L = '#8FE9FF'
GOLD = '#FFD166'

M, MU, GR = 20, 0.5, 9.8
MG = M * GR                       # 196 N
TH_IDEAL = np.arctan(MU)          # 26,565°
F0, FMIN = MU * MG, MU * MG / (np.cos(TH_IDEAL) + MU * np.sin(TH_IDEAL))


def Fth(t):
    return MU * MG / (np.cos(t) + MU * np.sin(t))


def rad(deg):
    return deg * PI / 180


@contextmanager
def wide_pango():
    pw, ph = config.pixel_width, config.pixel_height
    config.pixel_width, config.pixel_height = 4000, 4000
    try:
        yield
    finally:
        config.pixel_width, config.pixel_height = pw, ph


def label(content, size=30, color=TEXT_COLOR, width=7.0, opacity=1.0):
    lines = []
    for line in content.split('\n'):
        with wide_pango():
            t = screen_text(line, size, oversample=2 if size >= 30 else 4)
        lines.append(t.set_color(color).set_opacity(opacity))
    group = VGroup(*lines).arrange(DOWN, buff=.14)
    if group.width > width:
        group.scale_to_fit_width(width)
    return group


def tex(*parts, size=44, color=TEXT_COLOR, width=7.3):
    r = MathTex(*parts, font_size=size, color=color)
    if r.width > width:
        r.scale_to_fit_width(width)
    return r


def arr(a, b, color, sw=6):
    a, b = np.array(a, float), np.array(b, float)
    if np.linalg.norm(b - a) < .08:
        return VMobject()
    return Arrow(a, b, buff=0, color=color, stroke_width=sw, tip_length=.2,
                 max_tip_length_to_length_ratio=.4, max_stroke_width_to_length_ratio=60)


def dash(a, b, color, sw=3):
    a, b = np.array(a, float), np.array(b, float)
    if np.linalg.norm(b - a) < .1:
        return VMobject()
    return DashedLine(a, b, dash_length=.1, color=color, stroke_width=sw)


class Coma(VGroup):
    """Número com vírgula decimal (1 casa) e sufixo, atualizado por função."""
    def __init__(self, fn, suffix, color, size, anchor):
        super().__init__()
        self.fn, self.anchor = fn, np.array(anchor, float)
        self.ip = DecimalNumber(0, num_decimal_places=0, font_size=size, color=color)
        self.cm = MathTex(',', font_size=size, color=color)
        self.dp = DecimalNumber(0, num_decimal_places=0, font_size=size, color=color)
        self.sf = MathTex(suffix, font_size=size * .85, color=color)
        self.add(self.ip, self.cm, self.dp, self.sf)
        self.add_updater(lambda m: m.refresh())
        self.refresh()

    def refresh(self):
        v = round(float(self.fn()), 1)
        ip = int(v)
        self.ip.set_value(ip)
        self.dp.set_value(int(round((v - ip) * 10)))
        self.ip.move_to(self.anchor, aligned_edge=LEFT)
        self.cm.next_to(self.ip, RIGHT, buff=.03).align_to(self.ip, DOWN).shift(DOWN * .06)
        self.dp.next_to(self.cm, RIGHT, buff=.03).align_to(self.ip, DOWN)
        self.sf.next_to(self.dp, RIGHT, buff=.1)
        self.sf.set_y(self.ip.get_y() + (.08 if 'circ' in self.sf.tex_string else 0))


class AnguloPuxarCaixa023(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(.35)
        self.add(wm.to_corner(UP + RIGHT, buff=.28).set_z_index(20))
        series = label('EXERCÍCIO RESOLVIDO', 20, opacity=.65)
        self.add(series.to_corner(UP + LEFT, buff=.4).set_z_index(20))

        th, bl = ValueTracker(0), ValueTracker(0)
        T = lambda: th.get_value()
        dvec = lambda: np.array([np.cos(T()), np.sin(T()), 0])
        SC = 2.6 / MG                      # unidades de cena por newton (fase 1)
        MGL = 2.6
        Fl = lambda: 1.3 * (1 - bl.get_value()) + bl.get_value() * Fth(T()) * SC
        Nl = lambda: MGL - Fl() * np.sin(T())

        # ---------------------------------------------------------------- headline
        self.head = None

        def H(text, size=34):
            new = label(text, size, width=7.2).move_to([0, 6.3, 0])
            old, self.head = self.head, new
            return ([FadeOut(old)] if old else []) + [FadeIn(new)]

        # ---------------------------------------------------------------- fase 1: geometria grande
        C = np.array([0, 2.6, 0])
        P = C + np.array([1.2, 0, 0])
        Q = np.array([-1.2, 1.78, 0])
        floor = Line([-4.3, 1.7, 0], [4.3, 1.7, 0], color=DIM, stroke_width=3)
        box = Rectangle(width=2.4, height=1.8, color=CYAN, stroke_width=3).set_fill('#0B1230', 1).move_to(C)
        rope = always_redraw(lambda: Line(P, P + 3.1 * dvec(), color=DIM, stroke_width=3))
        Fvec = always_redraw(lambda: arr(P, P + Fl() * dvec(), CYAN, 7))
        Fx = always_redraw(lambda: dash(P, P + [Fl() * np.cos(T()), 0, 0], CYAN_L))
        Fy = always_redraw(lambda: dash(P + [Fl() * np.cos(T()), 0, 0], P + Fl() * dvec(), CYAN_L))
        Wvec = arr(C, C - [0, MGL, 0], TEXT_COLOR)
        Nvec = always_redraw(lambda: arr(C, C + [0, Nl(), 0], VIOLET))
        fl = lambda: MU * Nl()
        fvec = always_redraw(lambda: arr(Q, Q - [fl(), 0, 0], PINK))

        def follow(m, fn):
            m.add_updater(lambda x: x.move_to(fn()))
            return m

        LF = follow(tex('F', size=40, color=CYAN), lambda: P + Fl() * dvec() / 2 + np.array([-.1, .38, 0]) * 1.0 + np.array([-.15, 0, 0]))
        LFx = follow(tex(r'F\cos\theta', size=34, color=CYAN_L), lambda: P + [Fl() * np.cos(T()) / 2, -.42, 0])
        LFy = follow(tex(r'F\sin\theta', size=34, color=CYAN_L), lambda: P + [Fl() * np.cos(T()) + .75, Fl() * np.sin(T()) / 2, 0])
        LN = follow(tex('N', size=40, color=VIOLET), lambda: C + [-.42, Nl() + .05, 0])
        LW = tex('mg', size=40).move_to(C + [0, -MGL - .38, 0])
        Lf = follow(tex(r'f_{s,\max}', size=34, color=PINK), lambda: Q + [-fl() / 2, -.5, 0])

        # ================================================================ 1 · pergunta
        self.play(*H('Qual é o melhor ângulo\npara puxar uma caixa?'),
                  Create(floor), FadeIn(box), Create(rope), FadeIn(Fvec, LF), run_time=2.2)
        self.wait(1.2)
        self.play(th.animate.set_value(rad(60)), run_time=3, rate_func=smooth)
        self.play(th.animate.set_value(0), run_time=2.5, rate_func=smooth)
        self.play(*H('Horizontal? 30°? 60°?'), th.animate.set_value(rad(35)), run_time=2.5, rate_func=smooth)
        self.wait(1)

        # ================================================================ 2 · decomposição
        self.play(*H('F se divide em duas partes'), Create(Fx), Create(Fy), run_time=1.8)
        self.play(Write(LFx), Write(LFy), run_time=1.6)
        self.wait(.6)
        self.play(*H('Uma puxa para a frente,\numa levanta a caixa'), run_time=.8)
        self.play(th.animate.set_value(rad(15)), run_time=2, rate_func=smooth)
        self.play(th.animate.set_value(rad(55)), run_time=2.6, rate_func=smooth)
        self.play(th.animate.set_value(rad(35)), run_time=1.8, rate_func=smooth)
        self.wait(.8)

        # ================================================================ 3 · normal
        self.play(*H('O chão empurra a caixa\npara cima: a normal N'),
                  th.animate.set_value(0), run_time=2, rate_func=smooth)
        self.play(FadeIn(Wvec, LW), FadeIn(Nvec, LN), run_time=1.5)
        self.wait(1)
        eq1 = tex('N', '=', 'm g', '-', 'F', r'\sin\theta', size=44).move_to([0, -1.5, 0])
        eq1[0].set_color(VIOLET)
        eq1[4].set_color(CYAN)
        eq1[5].set_color(CYAN_L)
        self.play(*H('Inclinar a corda\ntira peso do chão'),
                  th.animate.set_value(rad(60)), Write(eq1), run_time=4, rate_func=smooth)
        self.play(Indicate(eq1[5], color=CYAN_L), run_time=1.2)
        self.play(th.animate.set_value(rad(35)), run_time=2, rate_func=smooth)
        self.wait(.8)

        # ================================================================ 4 · limite do atrito estático
        self.play(*H('O atrito estático máximo\ndepende de N'), FadeIn(fvec, Lf), run_time=1.6)
        eq2 = tex(r'f_{s,\max}', '=', r'\mu_s', 'N', size=44).move_to([0, -2.7, 0])
        eq2[0].set_color(PINK)
        eq2[3].set_color(VIOLET)
        self.play(Write(eq2), run_time=1.8)
        self.wait(.6)
        self.play(th.animate.set_value(0), run_time=2.2, rate_func=smooth)
        self.play(*H('N diminui: o limite do\natrito estático diminui junto'),
                  th.animate.set_value(rad(60)), run_time=4.2, rate_func=smooth)
        self.play(th.animate.set_value(rad(35)), run_time=1.8, rate_func=smooth)
        self.wait(.8)

        # ================================================================ 5 · limiar e F(θ)
        self.play(*H('No limiar de deslizamento,\nF aumenta até igualar o atrito'),
                  bl.animate.set_value(1), run_time=2.2, rate_func=smooth)
        eqA = tex(r'F\cos\theta', '=', r'f_{s,\max}', size=46).move_to([0, -4.1, 0])
        eqA[0].set_color(CYAN_L)
        eqA[2].set_color(PINK)
        self.play(Write(eqA), eq1.animate.set_opacity(.4), eq2.animate.set_opacity(.4), run_time=1.8)
        self.play(Indicate(Fx, color=CYAN_L), Indicate(fvec, color=PINK), run_time=1.6)
        self.play(th.animate.set_value(rad(10)), run_time=2, rate_func=smooth)
        self.play(th.animate.set_value(rad(55)), run_time=3, rate_func=smooth)
        self.play(th.animate.set_value(rad(35)), run_time=1.6, rate_func=smooth)

        def step(parts, headline, run=2.2, wait=1.0, colors=None):
            nonlocal eqA
            new = tex(*parts, size=44).move_to([0, -4.1, 0])
            self.play(*H(headline), TransformMatchingTex(eqA, new), run_time=run)
            eqA = new
            self.wait(wait)

        step([r'F\cos\theta', '=', r'\mu_s', 'N'], 'Trocamos o atrito máximo\npelo coeficiente vezes N')
        step([r'F\cos\theta', '=', r'\mu_s', r'\left(', 'm g', '-', r'F\sin\theta', r'\right)'],
             'Trocamos N pelo peso menos\na parte vertical de F', run=2.6)
        step([r'F\cos\theta', '+', r'\mu_s F\sin\theta', '=', r'\mu_s m g'],
             'Juntamos os termos com F', run=2.6)
        step(['F', r'\left(\cos\theta+\mu_s\sin\theta\right)', '=', r'\mu_s m g'],
             'F em evidência', run=2.4)
        step(['F', '=', r'\dfrac{\mu_s m g}{\cos\theta+\mu_s\sin\theta}'],
             'Isolamos F', run=2.6, wait=.6)
        fth = tex(r'F(\theta)', '=', r'\dfrac{\mu_s m g}{\cos\theta+\mu_s\sin\theta}', size=44)
        fth.move_to(eqA)
        self.play(*H('Essa é a força mínima\npara cada ângulo'),
                  TransformMatchingTex(eqA, fth), run_time=1.8)
        eqA = fth
        box_f = SurroundingRectangle(fth, color=CYAN, buff=.18, stroke_width=3)
        self.play(Create(box_f), run_time=1)
        self.wait(1.4)

        # ================================================================ 6 · reorganização
        cC = np.array([-1.9, 4.1, 0])
        cP = cC + [.7, 0, 0]
        CS = .55
        cfloor = Line([-4.3, 3.6, 0], [4.3, 3.6, 0], color=DIM, stroke_width=3)
        cbox = Rectangle(width=1.4, height=1.0, color=CYAN, stroke_width=3).set_fill('#0B1230', 1).move_to(cC)
        crope = always_redraw(lambda: Line(cP, cP + 1.6 * dvec(), color=DIM, stroke_width=3))
        cF = always_redraw(lambda: arr(cP, cP + Fth(T()) * SC * CS * dvec(), CYAN, 5))

        gone = VGroup(Fvec, Fx, Fy, Nvec, fvec, Wvec, LF, LFx, LFy, LN, LW, Lf, eq1, eq2, box_f)
        for m in (LF, LFx, LFy, LN, Lf):
            m.clear_updaters()
        for m in (Fvec, Fx, Fy, Nvec, fvec):
            m.clear_updaters()
        zone_formula = fth.copy().scale(.88).move_to([0, 1.85, 0])
        self.play(*H('F necessária em função do ângulo'),
                  FadeOut(gone), FadeOut(rope),
                  ReplacementTransform(box, cbox), ReplacementTransform(floor, cfloor),
                  ReplacementTransform(fth, zone_formula), run_time=2.4)
        self.add(crope, cF)
        th_read = Coma(lambda: T() * 180 / PI, r'^\circ', TEXT_COLOR, 38, [1.9, 4.75, 0])
        f_read = Coma(lambda: Fth(T()), r'\,\mathrm{N}', CYAN, 38, [1.9, 4.15, 0])
        lt = tex(r'\theta =', size=34, color=DIM).move_to([1.35, 4.75, 0])
        lf = tex(r'F =', size=34, color=CYAN).move_to([1.35, 4.15, 0])
        self.play(FadeIn(crope), FadeIn(cF), FadeIn(th_read), FadeIn(f_read), FadeIn(lt), FadeIn(lf), run_time=1)
        self.wait(.6)

        # ================================================================ 7 · gráfico
        axes = Axes(x_range=[0, 70, 10], y_range=[80, 125, 10], x_length=6.8, y_length=5.2,
                    axis_config={'color': DIM, 'stroke_width': 2.5, 'include_tip': False,
                                 'include_ticks': True, 'tick_size': .06})
        axes.move_to([.3, -2.45, 0])
        xl = VGroup(*[tex(str(v), size=26, color=DIM).next_to(axes.c2p(v, 80), DOWN, buff=.14) for v in range(0, 71, 10)])
        yl = VGroup(*[tex(str(v), size=26, color=DIM).next_to(axes.c2p(0, v), LEFT, buff=.14) for v in range(80, 121, 10)])
        xt = tex(r'\theta\ (^\circ)', size=28, color=DIM).next_to(axes.c2p(62, 80), DOWN, buff=.5)
        xl[-1].shift(LEFT * .0)
        yt = tex(r'F_{\mathrm{nec}}\ (\mathrm{N})', size=28, color=CYAN).next_to(axes.c2p(0, 125), UP, buff=.1).align_to(axes.c2p(0, 125), LEFT).shift(LEFT * .3)
        brk = label('eixo vertical a partir de 80 N', 17, DIM, width=3.4).next_to(axes.c2p(70, 80), UP, buff=.1).align_to(axes.c2p(70, 80), RIGHT)
        brk.shift(DOWN * .0)
        self.play(*H('Cada ângulo, uma força mínima'), Create(axes), FadeIn(xl), FadeIn(yl), FadeIn(xt), FadeIn(yt), FadeIn(brk), run_time=2.2)

        traced = always_redraw(lambda: axes.plot(lambda d: Fth(rad(d)), x_range=[0, max(T() * 180 / PI, .6)], color=CYAN, stroke_width=5))
        dot = always_redraw(lambda: Dot(axes.c2p(T() * 180 / PI, Fth(T())), radius=.11, color=WHITE).set_z_index(6))
        self.add(traced, dot)
        th.set_value(0)
        self.wait(.6)
        self.play(th.animate.set_value(rad(70)), run_time=8, rate_func=linear)
        self.wait(.6)
        self.play(*H('F cai, atinge um mínimo\ne volta a subir'), run_time=.8)
        self.play(th.animate.set_value(rad(8)), run_time=3.5, rate_func=smooth)
        self.play(th.animate.set_value(TH_IDEAL), run_time=3, rate_func=smooth)
        full = axes.plot(lambda d: Fth(rad(d)), x_range=[0, 70], color=CYAN, stroke_width=5)
        traced.clear_updaters()
        self.remove(traced)
        self.add(full)
        xi = TH_IDEAL * 180 / PI
        pmin = axes.c2p(xi, FMIN)
        halo = Circle(radius=.2, color=GOLD, stroke_width=4).move_to(pmin)
        dot.clear_updaters()
        self.play(dot.animate.set_color(GOLD), Create(halo), run_time=1.0)
        gv = dash(pmin, axes.c2p(xi, 80), GOLD)
        lab_th = tex(r'\theta_{\mathrm{ideal}}=26{,}565^\circ', size=30, color=GOLD).next_to(axes.c2p(xi, 80), DOWN, buff=.52)
        lab_min = tex(r'F_{\min}=87{,}654\ \mathrm{N}', size=30, color=GOLD).move_to(axes.c2p(xi + 11, 111))
        self.play(*H('O mínimo da curva:\nângulo ideal = 26,565°'), Create(gv), Write(lab_th), Write(lab_min), run_time=2.2)
        self.wait(2)

        # ================================================================ 8 · otimização
        self.play(*H('F mínima: denominador máximo'),
                  FadeOut(lab_min), FadeOut(halo), FadeOut(gv), FadeOut(lab_th), run_time=1.2)
        d1 = tex(r'D(\theta)', '=', r'\cos\theta+\mu_s\sin\theta', size=42).move_to([0, 2.55, 0])
        self.play(Transform(zone_formula, d1), run_time=2.2)
        self.wait(.8)
        d2 = tex(r"D'(\theta)", '=', r'-\sin\theta+\mu_s\cos\theta', '=', '0', size=42).move_to([0, 1.55, 0])
        self.play(*H('No máximo, a derivada é zero'), Write(d2), run_time=2.2)
        self.wait(1)
        d3 = tex(r'\tan\theta_{\mathrm{ideal}}', '=', r'\mu_s', size=54, color=GOLD).move_to([0, 1.55, 0])
        self.play(*H('A condição do ótimo'), TransformMatchingTex(d2, d3), run_time=2.2)
        frame = SurroundingRectangle(d3, color=GOLD, buff=.2, stroke_width=3)
        self.play(Create(frame), run_time=.8)
        self.wait(1.4)
        d4 = tex(r'\tan\theta_{\mathrm{ideal}}', '=', r'0{,}5', r'\ \Rightarrow\ ', r'\theta_{\mathrm{ideal}}', '=', r'26{,}565^\circ',
                 size=40, color=GOLD).move_to([0, 1.55, 0])
        self.play(*H('Com coeficiente de atrito 0,5'), FadeOut(frame), TransformMatchingTex(d3, d4), FadeOut(zone_formula), run_time=2.2)
        self.wait(1.6)

        chk1 = tex('N', '=', r'm g - F_{\min}\sin\theta_{\mathrm{ideal}}', '=', r'156{,}8\ \mathrm{N}', size=32).move_to([0, 2.55, 0])
        chk2 = tex(r'f_{s,\max}', '=', r'\mu_s N', '=', r'78{,}4\ \mathrm{N}', '=', r'F_{\min}\cos\theta_{\mathrm{ideal}}', size=32).move_to([0, 1.55, 0])
        chk1[0].set_color(VIOLET)
        chk2[0].set_color(PINK)
        self.play(*H('Conferência no limiar'), FadeOut(d4), Write(chk1), run_time=2)
        self.play(Write(chk2), run_time=2.2)
        self.wait(2)

        # ================================================================ 9 · resultado numérico
        l98 = DashedLine(axes.c2p(0, F0), axes.c2p(70, F0), dash_length=.12, color=DIM, stroke_width=2.5)
        lmn = DashedLine(axes.c2p(xi, FMIN), axes.c2p(70, FMIN), dash_length=.12, color=GOLD, stroke_width=2.5)
        t98 = tex(r'98\ \mathrm{N}', size=30, color=TEXT_COLOR).next_to(axes.c2p(70, F0), UP, buff=.08).align_to(axes.c2p(70, F0), RIGHT)
        tmn = tex(r'87{,}654\ \mathrm{N}', size=30, color=GOLD).next_to(axes.c2p(70, FMIN), UP, buff=.08).align_to(axes.c2p(70, FMIN), RIGHT)
        self.play(*H('Na prática, com m = 20 kg'), FadeOut(chk1), FadeOut(chk2),
                  Create(l98), Create(lmn), Write(t98), Write(tmn), run_time=2.4)
        bracket = DoubleArrow(axes.c2p(xi, F0), axes.c2p(xi, FMIN), buff=0, color=GOLD, stroke_width=4, tip_length=.14)
        tred = tex(r'-10{,}56\,\%', size=30, color=GOLD).next_to(bracket, RIGHT, buff=.12)
        final = tex(r'98\ \mathrm{N}', r'\ \longrightarrow\ ', r'87{,}654\ \mathrm{N}', size=56).move_to([0, 2.55, 0])
        final[0].set_color(TEXT_COLOR)
        final[2].set_color(GOLD)
        sub = tex(r'\approx\ 10{,}56\,\%\ \text{menos força}', size=38, color=GOLD).move_to([0, 1.5, 0])
        self.play(Create(bracket), Write(tred), run_time=1.6)
        self.play(Write(final), run_time=2)
        self.play(Write(sub), run_time=1.6)
        self.wait(4)
