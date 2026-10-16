"""vid_0023 — V5 (preview silencioso; corda reconhecível e transições limpas, sobre a V4). Mesma física e narrativa da V1; muda a linguagem de animação:
origem visível de cada termo, álgebra por operações identificáveis, caixa 2.5D e gráfico construído.
Cores: ciano, azul, violeta, magenta e branco (sem amarelo).
"""
import sys
from pathlib import Path

import numpy as np
from manim import (
    Arc, Axes, Circle, Create, DashedLine, DOWN, DoubleArrow, Ellipse, FadeIn, FadeOut,
    ImageMobject, Indicate, LEFT, Line, MathTex, PI, Polygon, Rectangle, ReplacementTransform,
    RIGHT, Scene, SurroundingRectangle, Transform, TransformFromCopy, UP, ValueTracker,
    VGroup, VMobject, WHITE, Write, always_redraw, linear, smooth, Succession, Dot,
)
from manim.animation.animation import prepare_animation

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
from cena import (  # noqa: E402  (helpers e constantes da V1, que permanece intacta)
    BACKGROUND_COLOR, CYAN, CYAN_L, DIM, F0, FMIN, MG, MU, PINK, TEXT_COLOR, TH_IDEAL,
    VIOLET, WATERMARK_PATH, Coma, Fth, arr, dash, label, rad, tex,
)

EDGE = '#9AA3BA'      # contorno do grafite
VIOLET_L = '#C4B8FF'    # divisor / rótulo N
BLUE_L = '#6EA8FF'      # μs
TOKEN_COLOR = {'F': CYAN, r'\cos\theta': CYAN_L, r'\sin\theta': CYAN_L, r'\mu_s': BLUE_L,
               'N': VIOLET_L, r'f_{s,\max}': PINK}


def tex2(*parts, size=42):
    m = MathTex(*parts, font_size=size, color=TEXT_COLOR)
    for part, p in zip(m, parts):
        if p in TOKEN_COLOR:
            part.set_color(TOKEN_COLOR[p])
    return m


def left_at(m, y, x=-3.6):
    return m.move_to([x, y, 0], aligned_edge=LEFT)


def make_box(C, s):
    """Caixa e piso em falsa perspectiva (2.5D); forças permanecem no plano frontal."""
    C = np.array(C, float)
    w, h = 2.8 * s, 2.0 * s
    d = np.array([.34 * s, .28 * s, 0])
    yf = C[1] - h / 2
    TL, TR = C + [-w / 2, h / 2, 0], C + [w / 2, h / 2, 0]
    BR = C + [w / 2, -h / 2, 0]
    band = Polygon([-4.5, yf, 0], [4.5, yf, 0], [4.5, yf + .7 * s, 0], [-4.5, yf + .7 * s, 0],
                   fill_color='#0A1230', fill_opacity=1, stroke_width=0)
    back = Line([-4.5, yf + .7 * s, 0], [4.5, yf + .7 * s, 0], color=DIM, stroke_width=1.5, stroke_opacity=.35)
    persp = VGroup(*[Line([x, yf, 0], [x * .78, yf + .7 * s, 0], color=DIM, stroke_width=1.2, stroke_opacity=.16)
                     for x in np.linspace(-4.2, 4.2, 9)])
    front_edge = Line([-4.5, yf, 0], [4.5, yf, 0], color=DIM, stroke_width=3)
    floor = VGroup(band, back, persp, front_edge)
    shadow = Ellipse(width=w * 1.25, height=.3 * s, fill_color='#000000', fill_opacity=.5,
                     stroke_width=0).move_to([C[0] + d[0] / 2, yf + .02, 0])
    side = Polygon(TR, BR, BR + d, TR + d, fill_color='#262B38', fill_opacity=1, stroke_color=EDGE, stroke_width=2.5)
    top = Polygon(TL, TR, TR + d, TL + d, fill_color='#59617A', fill_opacity=1, stroke_color=EDGE, stroke_width=2.5)
    front = Rectangle(width=w, height=h, fill_color='#3A4153', fill_opacity=1, stroke_color=EDGE, stroke_width=3).move_to(C)
    return floor, VGroup(shadow, side, top, front)


ROPE_OUT, ROPE_IN = '#7F889E', '#E4E8F4'


def rope_mob(a, b, w=1.0):
    """Corda: faixa neutra clara com acabamento escuro (sem ponta de seta)."""
    return VGroup(Line(a, b, color=ROPE_OUT, stroke_width=10 * w), Line(a, b, color=ROPE_IN, stroke_width=5 * w)).set_z_index(3)


def ring_mob(c, r):
    return Circle(radius=r, color=ROPE_IN, stroke_width=3, fill_color='#262B38', fill_opacity=1).move_to(c).set_z_index(4)


class AnguloPuxarCaixa023V5(Scene):
    # ------------------------------------------------------------------ utilidades
    def head_anim(self, text, size=34):
        if text == '':
            old, self.head = self.head, None
            return FadeOut(old, run_time=.3)
        new = label(text, size, width=7.2).move_to([0, 6.3, 0])
        old, self.head = self.head, new
        if old is None:
            return FadeIn(new, run_time=.6)
        return Succession(FadeOut(old, run_time=.3), FadeIn(new, run_time=.6))

    def go(self, rt, *anims, head=None, rf=smooth, wait=0, k=.9):
        built = []
        for a in anims:
            a = prepare_animation(a)
            a.run_time = rt * k
            if not isinstance(a, Indicate):
                a.rate_func = rf
            built.append(a)
        if head is not None:
            built.append(self.head_anim(head))
        self.play(*built)
        if wait:
            self.wait(wait * .8)

    def morph(self, rt, src, dst, pairs, copies=(), skip=(), extra=(), head=None, wait=0):
        anims, used_s = [], {i for i, _ in pairs} | set(skip)
        used_d = {j for _, j in pairs}
        for _, js in copies:
            used_d |= set(js) if isinstance(js, tuple) else {js}
        for i, j in pairs:
            anims.append(ReplacementTransform(src[i], dst[j]))
        for srcm, j in copies:
            tgt = VGroup(*[dst[k] for k in j]) if isinstance(j, tuple) else dst[j]
            anims.append(TransformFromCopy(srcm, tgt))
        anims += [FadeOut(src[i]) for i in range(len(src)) if i not in used_s]
        anims += [FadeIn(dst[j]) for j in range(len(dst)) if j not in used_d]
        self.go(rt, *anims, *extra, head=head, wait=wait, k=1.0)

    # ------------------------------------------------------------------ cena
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(.35)
        self.add(wm.to_corner(UP + RIGHT, buff=.28).set_z_index(20))
        series = label('EXERCÍCIO RESOLVIDO', 20, opacity=.65)
        self.add(series.to_corner(UP + LEFT, buff=.4).set_z_index(20))
        self.head = None

        th, bl, rv = ValueTracker(0), ValueTracker(0), ValueTracker(0)
        T = lambda: th.get_value()
        dvec = lambda: np.array([np.cos(T()), np.sin(T()), 0])
        MGL = 2.4
        SC = MGL / MG
        Fl = lambda: 1.2 * (1 - bl.get_value()) + bl.get_value() * Fth(T()) * SC
        Nl = lambda: MGL - Fl() * np.sin(T())
        fl = lambda: MU * Nl()

        # ---------------- geometria grande
        C = np.array([-.3, 2.9, 0])
        floor, box = make_box(C, 1.0)
        P = C + [1.4, 0, 0]
        Q = np.array([C[0] - 1.4, C[1] - 1.0 + .13, 0])
        rope = always_redraw(lambda: rope_mob(P, P + 3.0 * dvec()))
        ring = ring_mob(P, .1)
        Fvec = always_redraw(lambda: arr(P, P + Fl() * dvec(), CYAN, 7).set_z_index(6))
        Fx = always_redraw(lambda: arr(P, P + [Fl() * np.cos(T()), 0, 0], CYAN_L, 5).set_z_index(5))
        Fy = always_redraw(lambda: arr(P, P + [0, Fl() * np.sin(T()), 0], CYAN_L, 5).set_z_index(5))
        closure = always_redraw(lambda: VGroup(
            dash(P + [Fl() * np.cos(T()), 0, 0], P + Fl() * dvec(), CYAN_L, 2),
            dash(P + [0, Fl() * np.sin(T()), 0], P + Fl() * dvec(), CYAN_L, 2)).set_opacity(.55))
        Wvec = arr(C, C - [0, MGL, 0], TEXT_COLOR, 6).set_z_index(6)
        Nvec = always_redraw(lambda: arr(C, C + [0, Nl(), 0], VIOLET, 7).set_z_index(6))
        Fstack = always_redraw(lambda: arr(C + [0, Nl(), 0], C + [0, MGL, 0], CYAN_L, 5).set_z_index(5))
        tick = DashedLine(C + [-.6, MGL, 0], C + [.6, MGL, 0], dash_length=.1, color=TEXT_COLOR, stroke_width=2).set_z_index(5)
        fvec = always_redraw(lambda: arr(Q, Q - [fl(), 0, 0], PINK, 7).set_z_index(6))
        arc = always_redraw(lambda: Arc(radius=.85, start_angle=0, angle=max(T(), .001), arc_center=P,
                                        color=TEXT_COLOR, stroke_width=3).set_z_index(5))
        ref = DashedLine(P, P + [2.0, 0, 0], dash_length=.1, color=DIM, stroke_width=2)

        def follow(m, fn, op=None):
            def upd(x):
                x.move_to(fn())
                if op:
                    x.set_opacity(op())
            m.add_updater(upd)
            upd(m)
            return m

        nrm = lambda: np.array([-np.sin(T()), np.cos(T()), 0])
        LF = follow(tex('F', size=44, color=CYAN), lambda: P + Fl() * dvec() + nrm() * .4 + dvec() * .12)
        LFx = follow(tex(r'F\cos\theta', size=36, color=CYAN_L), lambda: P + [Fl() * np.cos(T()) / 2 + .3, -.5, 0])
        LFy = follow(tex(r'F\sin\theta', size=36, color=CYAN_L), lambda: P + [Fl() * np.cos(T()) + 1.25, Fl() * np.sin(T()) / 2, 0],
                     lambda: min(1, max(0, (Fl() * np.sin(T()) - .1) / .25)))
        LTh = follow(tex(r'\theta', size=40), lambda: P + 1.02 * np.array([np.cos(T() / 2), np.sin(T() / 2), 0]),
                     lambda: min(1, max(0, (T() - .32) / .12)))
        LN = follow(tex('N', size=48, color=VIOLET_L), lambda: C + [-.5, Nl() / 2 + .1, 0])
        LW = tex('mg', size=44).move_to(C + [0, -MGL - .42, 0])
        Lf = follow(tex(r'f_{s,\max}', size=36, color=PINK), lambda: Q + [-fl() / 2, -.5, 0])
        for m in (LF, LFx, LFy, LTh, LN, Lf, LW):
            m.set_z_index(8)

        # ================================================================ 1 · pergunta
        self.go(2.4, Create(floor), FadeIn(box), Create(rope), FadeIn(ring), FadeIn(Fvec), FadeIn(LF),
                head='Qual é o melhor ângulo\npara puxar uma caixa?', wait=1.0)
        idf = VGroup(tex('F', size=34, color=CYAN), label('tração da corda', 24, TEXT_COLOR, width=2.6)).arrange(RIGHT, buff=.14)
        idf.move_to(P + [1.8, 1.6, 0])
        idf[1].shift(UP * .02)
        self.go(.8, FadeIn(idf), wait=1.6)
        self.go(.5, FadeOut(idf))
        self.go(1.2, FadeIn(arc), FadeIn(ref), FadeIn(LTh))
        self.go(2.8, th.animate.set_value(rad(60)))
        self.go(2.4, th.animate.set_value(rad(35)), wait=.6)

        # ================================================================ 2 · decomposição
        self.go(.9, head='Componentes da força')
        self.add(closure)
        self.go(2.0, TransformFromCopy(Fvec, Fx), TransformFromCopy(Fvec, Fy))
        self.go(1.4, Write(LFx), Write(LFy), wait=.4)
        self.go(1.4, Indicate(Fx, color=CYAN_L))
        self.go(1.4, Indicate(Fy, color=CYAN_L))
        self.go(1.8, th.animate.set_value(rad(15)))
        self.go(2.4, th.animate.set_value(rad(55)), wait=.4)

        # ================================================================ 3 · normal
        self.go(2.0, th.animate.set_value(0), head='Equilíbrio vertical')
        self.go(1.6, FadeIn(Wvec), FadeIn(LW), FadeIn(Nvec), FadeIn(LN), wait=.8)
        self.add(Fstack)
        self.go(2.2, th.animate.set_value(rad(40)), FadeIn(tick))
        eq1a = tex2('N', '+', 'F', r'\sin\theta', '=', 'm g', size=44).move_to([0, -1.3, 0])
        self.go(2.6, TransformFromCopy(LN, eq1a[0]), TransformFromCopy(LFy, VGroup(eq1a[2], eq1a[3])),
                TransformFromCopy(LW, eq1a[5]), Write(eq1a[1]), Write(eq1a[4]), wait=.8)
        self.go(3.0, th.animate.set_value(rad(60)))
        self.go(2.0, th.animate.set_value(rad(35)))
        eq1b = tex2('N', '=', 'm g', '-', 'F', r'\sin\theta', size=44).move_to([0, -1.3, 0])
        self.morph(2.6, eq1a, eq1b, [(0, 0), (4, 1), (5, 2), (1, 3), (2, 4), (3, 5)],
                   extra=[FadeOut(Fstack), FadeOut(tick)], wait=1.0)

        # ================================================================ 4 · limite do atrito estático
        self.go(1.6, FadeIn(fvec), FadeIn(Lf), head='Limite do atrito estático')
        eq2 = tex2(r'f_{s,\max}', '=', r'\mu_s', 'N', size=44).move_to([0, -2.4, 0])
        self.go(2.4, TransformFromCopy(Lf, eq2[0]), TransformFromCopy(LN, eq2[3]), Write(eq2[1]), Write(eq2[2]), wait=.6)
        self.go(1.8, th.animate.set_value(0))
        self.go(3.6, th.animate.set_value(rad(60)))
        self.go(1.4, th.animate.set_value(rad(35)), wait=.5)

        # ================================================================ 5 · limiar e F(θ)
        self.go(2.2, bl.animate.set_value(1), head='Limiar de deslizamento')
        A = left_at(tex2('F', r'\cos\theta', '=', r'f_{s,\max}'), -3.8)
        self.go(2.4, TransformFromCopy(LFx, VGroup(A[0], A[1])), TransformFromCopy(Lf, A[3]), Write(A[2]),
                eq1b.animate.set_opacity(.75), eq2.animate.set_opacity(.75))
        self.go(1.6, Indicate(Fx, color=CYAN_L), Indicate(fvec, color=PINK))
        self.go(1.6, th.animate.set_value(rad(10)))
        self.go(2.6, th.animate.set_value(rad(55)))
        self.go(1.2, th.animate.set_value(rad(35)), wait=.3)

        B = left_at(tex2('F', r'\cos\theta', '=', r'\mu_s', 'N'), -3.8)
        self.morph(2.4, A, B, [(0, 0), (1, 1), (2, 2)], copies=[(VGroup(eq2[2], eq2[3]), (3, 4))],
                   extra=[eq2.animate.set_opacity(1)], head='Isolando F', wait=.5)
        self.go(.7, FadeOut(eq2))
        C_ = left_at(tex2('F', r'\cos\theta', '=', r'\mu_s', r'\left(', 'm g', '-', 'F', r'\sin\theta', r'\right)'), -3.8)
        self.morph(2.8, B, C_, [(0, 0), (1, 1), (2, 2), (3, 3)],
                   copies=[(VGroup(*eq1b[2:6]), (5, 6, 7, 8))], extra=[eq1b.animate.set_opacity(1)],
                   wait=.5)
        self.go(.7, FadeOut(eq1b))
        D = left_at(tex2('F', r'\cos\theta', '=', r'\mu_s', 'm g', '-', r'\mu_s', 'F', r'\sin\theta'), -3.8)
        self.morph(2.8, C_, D, [(0, 0), (1, 1), (2, 2), (3, 3), (5, 4), (6, 5), (7, 7), (8, 8)],
                   copies=[(C_[3], 6)], wait=.8)
        E = left_at(tex2('F', r'\cos\theta', '+', r'\mu_s', 'F', r'\sin\theta', '=', r'\mu_s', 'm g'), -3.8)
        self.morph(3.0, D, E, [(0, 0), (1, 1), (2, 6), (3, 7), (4, 8), (5, 2), (6, 3), (7, 4), (8, 5)],
                   wait=.8)
        Fa = left_at(tex2('F', r'\left(', r'\cos\theta', '+', r'\mu_s', r'\sin\theta', r'\right)', '=', r'\mu_s', 'm g'), -3.8)
        ghost = Fa[0].copy().set_opacity(0)
        self.morph(3.0, E, Fa, [(0, 0), (1, 2), (2, 3), (3, 4), (5, 5), (6, 7), (7, 8), (8, 9)], skip=(4,),
                   extra=[ReplacementTransform(E[4], ghost)], head='F em evidência', wait=.8)
        annot = tex(r'\div\ \left(\cos\theta+\mu_s\sin\theta\right)', size=36, color=VIOLET_L).move_to([0, -4.9, 0])
        self.go(1.8, VGroup(*Fa[1:7]).animate.set_color(VIOLET_L), FadeIn(annot), wait=.8)
        fin = tex2('F', r'\left(\theta\right)', '=', r'\dfrac{\mu_s m g}{\cos\theta+\mu_s\sin\theta}', size=44).move_to([0, -3.9, 0])
        fin[3].set_color(TEXT_COLOR)
        self.go(3.0, ReplacementTransform(Fa[0], fin[0]), ReplacementTransform(Fa[7], fin[2]),
                ReplacementTransform(VGroup(*Fa[1:7], Fa[8], Fa[9]), fin[3]), FadeIn(fin[1]), FadeOut(annot), wait=.4)
        box_f = SurroundingRectangle(fin, color=CYAN, buff=.18, stroke_width=3)
        self.go(1.0, Create(box_f))
        self.go(2.4, th.animate.set_value(0), wait=.8)

        # ================================================================ 6 · reorganização
        cC = np.array([-1.9, 4.15, 0])
        cP = cC + [.7, 0, 0]
        cfloor, cbox = make_box(cC, .5)
        crope = always_redraw(lambda: rope_mob(cP, cP + 1.6 * dvec(), .6))
        cring = ring_mob(cP, .055)
        cF = always_redraw(lambda: arr(cP, cP + Fth(T()) * SC * .55 * dvec(), CYAN, 5).set_z_index(6))
        gone = VGroup(Fx, Fy, Nvec, fvec, Wvec, LF, LFx, LFy, LN, LW, Lf, LTh, arc, ref, closure, box_f)
        for m in (LF, LFx, LFy, LN, Lf, LTh, Fx, Fy, Nvec, fvec, arc, closure, Fvec, rope):
            m.clear_updaters()
        zone = tex2('F', r'\left(\theta\right)', '=', r'\dfrac{\mu_s m g}{\cos\theta+\mu_s\sin\theta}', size=39).move_to([0, 1.85, 0])
        zone[3].set_color(TEXT_COLOR)
        self.go(2.6, FadeOut(gone), ReplacementTransform(box, cbox), ReplacementTransform(floor, cfloor),
                ReplacementTransform(rope, crope), ReplacementTransform(ring, cring), ReplacementTransform(Fvec, cF),
                ReplacementTransform(VGroup(*fin), zone), head='')
        self.remove(*[m for m in self.mobjects if m in (box_f,)])

        # ================================================================ 7 · gráfico
        axes = Axes(x_range=[0, 70, 10], y_range=[80, 125, 10], x_length=6.8, y_length=5.2,
                    axis_config={'color': DIM, 'stroke_width': 2.5, 'include_tip': False, 'include_ticks': True, 'tick_size': .06})
        axes.move_to([.3, -2.45, 0])
        xl = VGroup(*[tex(str(v), size=26, color=DIM).next_to(axes.c2p(v, 80), DOWN, buff=.14) for v in range(0, 71, 10)])
        yl = VGroup(*[tex(str(v), size=26, color=DIM).next_to(axes.c2p(0, v), LEFT, buff=.14) for v in range(80, 121, 10)])
        xt = tex(r'\theta\ (^\circ)', size=28, color=DIM).next_to(axes.c2p(62, 80), DOWN, buff=.5)
        yt = tex(r'F_{\mathrm{nec}}\ (\mathrm{N})', size=28, color=CYAN).next_to(axes.c2p(0, 125), UP, buff=.1).align_to(axes.c2p(0, 125), LEFT).shift(LEFT * .3)
        brk = label('eixo vertical a partir de 80 N', 17, DIM, width=3.4).next_to(axes.c2p(70, 80), UP, buff=.1).align_to(axes.c2p(70, 80), RIGHT)
        self.go(2.2, Create(axes), FadeIn(xl), FadeIn(yl), FadeIn(xt), FadeIn(yt), FadeIn(brk), wait=.4)
        xd = lambda: T() * 180 / PI
        traced = always_redraw(lambda: axes.plot(lambda d: Fth(rad(d)), x_range=[0, max(rv.get_value(), .6)],
                                                 color=CYAN, stroke_width=5))
        dot = always_redraw(lambda: Dot(axes.c2p(xd(), Fth(T())), radius=.11, color=WHITE).set_z_index(6))
        guide = always_redraw(lambda: dash(axes.c2p(xd(), 80), axes.c2p(xd(), Fth(T())), DIM, 2).set_opacity(.7))
        th_read = Coma(xd, r'^\circ', TEXT_COLOR, 38, [1.9, 4.75, 0])
        f_read = Coma(lambda: Fth(T()), r'\,\mathrm{N}', CYAN, 38, [1.9, 4.15, 0])
        lt = tex(r'\theta =', size=34, color=DIM).move_to([1.35, 4.75, 0])
        lf = tex(r'F =', size=34, color=CYAN).move_to([1.35, 4.15, 0])
        self.add(traced)
        self.add(guide)
        self.go(1.0, FadeIn(dot, scale=.3), FadeIn(th_read), FadeIn(f_read), FadeIn(lt), FadeIn(lf), wait=.4)
        # origem dos 98 N: corda horizontal, th = 0
        data = tex(r'm=20\,\mathrm{kg}\quad \mu_s=0{,}5\quad g=9{,}8\,\mathrm{m/s^2}', size=32, color=DIM).move_to([0, 2.95, 0])
        ev = tex(r'F(0^\circ)', '=', r'\dfrac{0{,}5\cdot 20\cdot 9{,}8}{\underbrace{\cos 0^\circ}_{1}+0{,}5\,\underbrace{\sin 0^\circ}_{0}}',
                 '=', r'98\ \mathrm{N}', size=38).move_to([0, 1.6, 0])
        ev[4].set_color(TEXT_COLOR)
        self.go(1.4, FadeIn(data), head='Tração horizontal')
        self.morph(2.4, zone, ev, [(0, 0), (2, 1)], wait=.3)
        self.go(1.4, Indicate(ev[4], color=CYAN, scale_factor=1.12), Indicate(dot, scale_factor=1.8, color=TEXT_COLOR))
        zone = tex2('F', r'\left(\theta\right)', '=', r'\dfrac{\mu_s m g}{\cos\theta+\mu_s\sin\theta}', size=39).move_to([0, 1.85, 0])
        zone[3].set_color(TEXT_COLOR)
        self.go(.6, FadeOut(data))
        self.morph(1.8, ev, zone, [(0, 0), (1, 2)], wait=.3)
        self.go(8.5, th.animate.set_value(rad(70)), rv.animate.set_value(70), rf=linear,
                head='Força × ângulo', wait=.6)
        traced.clear_updaters()
        note = label('ajuda até aqui;\ndepois, F volta a subir', 19, DIM, width=2.8).move_to(axes.c2p(38, 117))
        self.go(5.0, th.animate.set_value(TH_IDEAL), FadeIn(note))
        xi = TH_IDEAL * 180 / PI
        pmin = axes.c2p(xi, FMIN)
        halo = Circle(radius=.2, color=TEXT_COLOR, stroke_width=4).move_to(pmin)
        lab_th = tex(r'\theta_{\mathrm{ideal}}=26{,}565^\circ', size=30).next_to(axes.c2p(xi, 80), DOWN, buff=.52)
        lab_min = tex(r'F_{\min}=87{,}654\ \mathrm{N}', size=30).move_to(axes.c2p(xi + 11, 111))
        self.go(1.2, Create(halo), FadeOut(note), head='Ângulo ideal')
        self.go(.9, Indicate(halo, scale_factor=1.7, color=TEXT_COLOR))
        self.go(1.8, Write(lab_th), Write(lab_min), wait=1.2)

        # ================================================================ 8 · otimização
        self.go(1.2, FadeOut(lab_min))
        d1 = tex(r'D(\theta)', '=', r'\cos\theta+\mu_s\sin\theta', size=42).move_to([0, 2.85, 0])
        self.go(2.2, ReplacementTransform(VGroup(*zone), d1), wait=.8)
        zone = d1
        d2 = tex(r"D'(\theta)", '=', r'-\sin\theta', '+', r'\mu_s\cos\theta', '=', '0', size=42).move_to([0, 1.8, 0])
        self.go(2.2, Write(d2), wait=1.0)
        d2b = tex(r'\sin\theta', '=', r'\mu_s\cos\theta', size=44).move_to([0, 1.8, 0])
        self.morph(2.6, d2, d2b, [(2, 0), (5, 1), (4, 2)], wait=1.0)
        d2c = tex(r'\dfrac{\sin\theta}{\cos\theta}', '=', r'\mu_s', size=44).move_to([0, 1.8, 0])
        self.morph(2.4, d2b, d2c, [(0, 0), (1, 1)], copies=[(d2b[2], 2)], wait=.8)
        d3 = tex(r'\tan\theta_{\mathrm{ideal}}', '=', r'\mu_s', size=54, color=CYAN).move_to([0, 1.8, 0])
        self.go(2.2, Transform(d2c, d3))
        frame = SurroundingRectangle(d3, color=CYAN, buff=.2, stroke_width=3)
        self.go(.8, Create(frame), wait=1.4)
        d4 = tex(r'\tan\theta_{\mathrm{ideal}}', '=', r'0{,}5', r'\ \Rightarrow\ ', r'\theta_{\mathrm{ideal}}', '=', r'26{,}565^\circ',
                 size=40, color=CYAN).move_to([0, 1.8, 0])
        self.go(2.2, FadeOut(frame), FadeOut(zone), Transform(d2c, d4), wait=1.4)

        chk1 = tex('N', '=', r'm g - F_{\min}\sin\theta_{\mathrm{ideal}}', '=', r'156{,}8\ \mathrm{N}', size=32).move_to([0, 2.85, 0])
        chk2 = tex(r'f_{s,\max}', '=', r'\mu_s N', '=', r'78{,}4\ \mathrm{N}', '=', r'F_{\min}\cos\theta_{\mathrm{ideal}}', size=32).move_to([0, 1.8, 0])
        chk1[0].set_color(VIOLET)
        chk2[0].set_color(PINK)
        self.go(.6, FadeOut(d2c))
        self.go(3.0, Write(chk1), Write(chk2), wait=1.0)

        # ================================================================ 9 · resultado numérico
        l98 = DashedLine(axes.c2p(0, F0), axes.c2p(70, F0), dash_length=.12, color=DIM, stroke_width=2.5)
        lmn = DashedLine(axes.c2p(xi, FMIN), axes.c2p(70, FMIN), dash_length=.12, color=TEXT_COLOR, stroke_width=2.5)
        t98 = tex(r'98\ \mathrm{N}', size=30).next_to(axes.c2p(70, F0), UP, buff=.08).align_to(axes.c2p(70, F0), RIGHT)
        tmn = tex(r'87{,}654\ \mathrm{N}', size=30, color=CYAN).next_to(axes.c2p(70, FMIN), UP, buff=.08).align_to(axes.c2p(70, FMIN), RIGHT)
        ring0 = Circle(radius=.17, color=TEXT_COLOR, stroke_width=3).move_to(axes.c2p(0, F0))
        hdr1 = label('tração horizontal', 22, DIM, width=3.2).move_to([-2.0, 3.05, 0])
        hdr2 = label('ângulo ideal', 22, DIM, width=3.2).move_to([2.0, 3.05, 0])
        ang1 = tex(r'0^\circ', size=40).move_to([-2.0, 2.35, 0])
        ang2 = tex(r'26{,}565^\circ', size=40, color=CYAN).move_to([2.0, 2.35, 0])
        for1 = tex(r'98\ \mathrm{N}', size=54).move_to([-2.0, 1.45, 0])
        for2 = tex(r'87{,}654\ \mathrm{N}', size=54, color=CYAN).move_to([2.0, 1.45, 0])
        sep = Line([0, 3.3, 0], [0, 1.0, 0], color=DIM, stroke_width=2, stroke_opacity=.5)
        bracket = DoubleArrow(axes.c2p(xi, F0), axes.c2p(xi, FMIN), buff=0, color=PINK, stroke_width=4, tip_length=.14)
        tred = tex(r'-10{,}56\,\%', size=30, color=PINK).next_to(bracket, RIGHT, buff=.12)
        # 1) ponto horizontal
        self.go(.6, FadeOut(chk1), FadeOut(chk2), FadeOut(lab_th))
        self.go(1.8, Create(l98), Write(t98), Create(ring0),
                FadeIn(hdr1), FadeIn(ang1), FadeIn(for1), FadeIn(sep))
        self.go(.8, Indicate(ring0, scale_factor=1.6, color=TEXT_COLOR), wait=.5)
        # 2) ponto ótimo
        self.go(1.8, Create(lmn), Write(tmn), FadeIn(hdr2), FadeIn(ang2), FadeIn(for2))
        self.go(.8, Indicate(halo, scale_factor=1.7, color=TEXT_COLOR), wait=.5)
        # 3) redução percentual
        self.go(1.6, Create(bracket), Write(tred), head='10,56% menos força', wait=5)
