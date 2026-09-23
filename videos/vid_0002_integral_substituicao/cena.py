"""Substituição sincronizada com a narração; cena visual sem áudio embutido."""

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UP, Axes, Brace, Create, Dot, FadeIn, FadeOut,
    ImageMobject, Indicate, Line, MathTex, Scene, SurroundingRectangle,
    Succession, Text, TransformFromCopy, ValueTracker, VGroup, Write, always_redraw, linear,
)

from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH

INNER = PRIMARY_COLOR
DIFFERENTIAL = "#EA63FF"


class Integral002(Scene):
    include_coda = True

    def equation(self, *tex, y=1.5, size=58):
        mob = MathTex(*tex, font_size=size, color=TEXT_COLOR)
        if mob.width > 7.6:
            mob.scale_to_fit_width(7.6)
        return mob.move_to([0, y, 0])

    def note(self, text, y=5.2):
        mob = Text(text, font_size=30, color=TEXT_COLOR)
        if mob.width > 7.6:
            mob.scale_to_fit_width(7.6)
        return mob.move_to([0, y, 0])

    def until(self, seconds):
        remaining = seconds - self.time
        if remaining > 1e-6:
            self.wait(remaining)

    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.add(ImageMobject(str(WATERMARK_PATH)).set_width(1.8)
                 .set_opacity(0.35).to_corner(UP + RIGHT, buff=0.28))
        heading = self.note("Integral por substituição")
        original = self.equation(r"\int", "2x", r"\cos(", "x^2", r")\,dx")
        original[1].set_color(DIFFERENTIAL)
        original[3].set_color(INNER)
        self.add(heading, original)
        self.wait(1.8)
        self.play(Indicate(original[3], color=INNER),
                  Indicate(original[1], color=DIFFERENTIAL), run_time=1)
        self.until(5)

        relation = self.equation("x^2", r"\xrightarrow{d/dx}", "2x", y=0.9)
        relation[0].set_color(INNER)
        relation[2].set_color(DIFFERENTIAL)
        boxes = VGroup(SurroundingRectangle(relation[0], color=INNER, buff=0.18),
                       SurroundingRectangle(relation[2], color=DIFFERENTIAL, buff=0.18))
        clue = self.note("Função interna e sua derivada", y=-1)
        self.play(original.animate.move_to([0, 3.4, 0]),
                  FadeIn(relation, boxes, clue), run_time=0.8)
        self.until(11.2)

        choice = self.equation("u", "=", "x^2", y=1.4)
        choice[0].set_color(INNER)
        choice[2].set_color(INNER)
        differential = self.equation("du", "=", r"2x\,dx", y=-0.5)
        differential[0].set_color(DIFFERENTIAL)
        differential[2].set_color(DIFFERENTIAL)
        brace = Brace(differential[2], DOWN, color=DIFFERENTIAL)
        piece = self.note("Uma única peça", y=-2.2)
        self.play(FadeOut(relation, boxes, clue), run_time=0.2)
        self.play(FadeIn(choice), run_time=0.4)
        self.until(13.5)
        self.play(Write(differential), run_time=0.8)
        self.play(FadeIn(brace, piece), run_time=0.5)
        self.until(15.8)

        # Chaves e rótulos separados: somente cópias limpas de u/du viajam.
        source = self.equation(r"\int", r"2x\,dx",
                               r"\cos(", r"x^2", ")", y=2.6)
        source[1].set_color(DIFFERENTIAL)
        source[3].set_color(INNER)
        arrow = self.equation(r"\Downarrow", y=0.3).shift(LEFT * 3.1)
        target = self.equation(r"\int", r"\cos(", "u", ")", r"\,du", y=-1.4)
        target[2].set_color(INNER)
        target[4].set_color(DIFFERENTIAL)
        brace_du = Brace(source[1], DOWN, color=DIFFERENTIAL, buff=0.08)
        brace_u = Brace(source[3], DOWN, color=INNER, buff=0.08)
        label_du = MathTex("du", font_size=42, color=DIFFERENTIAL).next_to(brace_du, DOWN, buff=0.08)
        label_u = MathTex("u", font_size=42, color=INNER).next_to(brace_u, DOWN, buff=0.08)
        annotations = VGroup(brace_du, brace_u, label_du, label_u)
        self.play(FadeOut(original, choice, differential, brace, piece), run_time=0.2)
        self.play(FadeIn(source, annotations), run_time=0.5)
        self.wait(1.1)
        # A integral de destino já pode ser lida antes de receber u e du.
        self.play(FadeIn(arrow, target[0], target[1], target[3]), run_time=0.5)
        for label, destination in ((label_u, target[2]), (label_du, target[4])):
            moving = label.copy().shift(DOWN * 0.65)
            self.play(FadeIn(moving), run_time=0.2)
            self.play(moving.animate.move_to(destination).set_height(destination.height),
                      run_time=1.5)
            self.remove(moving)
            self.add(destination)
        self.until(22.5)

        evaluated = self.equation(r"\int\cos(", "u", r")\,du", "=",
                                  r"\sin(", "u", ")+C", y=1.2, size=54)
        evaluated[1].set_color(INNER)
        evaluated[5].set_color(INNER)
        self.play(FadeOut(source, annotations, arrow, target), run_time=0.2)
        self.play(FadeIn(evaluated), run_time=0.5)
        self.until(30.9)

        back = self.equation(r"\sin(", "u", ")+C", y=2.7)
        back[1].set_color(INNER)
        result = self.equation(r"\sin(", "x^2", ")+C", y=0)
        result[1].set_color(INNER)
        box = SurroundingRectangle(result, color=INNER, buff=0.25)
        back_arrow = self.equation(r"\Downarrow", y=1.4)
        self.play(FadeOut(evaluated), FadeIn(back, back_arrow), run_time=0.5)
        self.play(TransformFromCopy(back[1], result[1]),
                  FadeIn(result[0], result[2]), run_time=1)
        self.play(Create(box), run_time=0.5)
        self.until(35.8)

        rule_heading = self.note("Regra da cadeia")
        rule = self.equation(r"\frac{d}{dx}\sin(x^2)", "=",
                             r"\cos(x^2)\cdot\frac{d}{dx}(x^2)", y=2.4, size=50)
        rule_box = SurroundingRectangle(rule, color=INNER, buff=0.22)
        inner_derivative = self.equation(r"\frac{d}{dx}(x^2)=2x", y=0.1, size=52)
        inner_derivative.set_color(INNER)
        concrete = self.equation(r"=\cos(x^2)\cdot 2x", y=-1.8, size=54)
        self.play(FadeOut(heading, back, back_arrow, result, box), run_time=0.2)
        self.play(FadeIn(rule_heading), run_time=0.2)
        self.play(Write(rule), Create(rule_box), run_time=1)
        self.until(39.6)
        self.play(FadeIn(inner_derivative), run_time=0.6)
        self.until(41.5)
        self.play(FadeIn(concrete), run_time=0.6)
        self.until(42.2)

        verify = self.note("Conferindo pela regra da cadeia")
        derivative = self.equation(r"\frac{d}{dx}\bigl[\sin(", "x^2", r")+C\bigr]", y=3)
        derivative[1].set_color(INNER)
        chain = self.equation(r"=\cos(", "x^2", r")\cdot", "2x", y=0.8)
        chain[1].set_color(INNER)
        chain[3].set_color(DIFFERENTIAL)
        checked = self.equation("=", "2x", r"\cos(", "x^2", ")", y=-1.2)
        checked[1].set_color(DIFFERENTIAL)
        checked[3].set_color(INNER)
        explanation = self.note("O integrando original", y=-3)
        # As duas linhas concretas continuam visíveis durante a fala que as explica.
        self.play(FadeOut(rule_heading, rule, rule_box), run_time=0.2)
        self.play(FadeIn(verify, derivative), run_time=0.4)
        self.until(44.2)
        self.play(FadeOut(inner_derivative, concrete), run_time=0.2)
        self.play(Write(chain), run_time=0.8)
        self.until(46.2)
        self.play(Write(checked), FadeIn(explanation), run_time=1)
        self.until(50)
        summary_heading = self.note("A substituição desfaz\na regra da cadeia")
        forward = self.equation(r"\sin(x^2)\xrightarrow{\ d/dx\ }2x\cos(x^2)", y=2.2, size=48)
        reverse = self.equation(r"2x\cos(x^2)\xrightarrow{\ \int dx\ }\sin(x^2)+C", y=-0.2, size=48)
        self.play(FadeOut(verify, derivative, chain, checked, explanation), run_time=0.2)
        self.play(FadeIn(summary_heading, forward, reverse), run_time=0.2)
        self.until(52.5)
        if self.include_coda:
            self.play(FadeOut(summary_heading, forward, reverse), run_time=0.2)
            self.graph_coda()

    def graph_coda(self):
        """Uma única abscissa governa cursores, pontos e tangente; sem área."""
        heading = self.note("A inclinação aparece em F′", y=5.5)
        top = Axes(x_range=[0, 1.65, 0.5], y_range=[-0.15, 1.2, 0.5],
                   x_length=6.6, y_length=2.4, tips=False,
                   axis_config={"include_ticks": False, "color": TEXT_COLOR,
                                "stroke_width": 1.5}).move_to([0, 2.45, 0])
        bottom = Axes(x_range=[0, 1.65, 0.5], y_range=[-3, 2, 1],
                      x_length=6.6, y_length=2.4, tips=False,
                      axis_config={"include_ticks": False, "color": TEXT_COLOR,
                                   "stroke_width": 1.5}).move_to([0, -1.85, 0])
        f = lambda x: np.sin(x * x)
        df = lambda x: 2 * x * np.cos(x * x)
        label_f = self.equation(r"F(x)=\sin(x^2)", y=4.35, size=44).set_color(INNER)
        label_df = self.equation(r"F'(x)=2x\cos(x^2)", y=0.1, size=44).set_color(DIFFERENTIAL)
        curves = VGroup(top.plot(f, x_range=[0, 1.6, 0.015], color=INNER),
                        bottom.plot(df, x_range=[0, 1.6, 0.015], color=DIFFERENTIAL))
        x = ValueTracker(0.15)
        dots = always_redraw(lambda: VGroup(
            Dot(top.c2p(x.get_value(), f(x.get_value())), radius=0.08, color=INNER),
            Dot(bottom.c2p(x.get_value(), df(x.get_value())), radius=0.08, color=DIFFERENTIAL)))
        cursors = always_redraw(lambda: VGroup(
            Line(top.c2p(x.get_value(), -0.15), top.c2p(x.get_value(), 1.2)),
            Line(bottom.c2p(x.get_value(), -3), bottom.c2p(x.get_value(), 2))
        ).set_stroke(TEXT_COLOR, width=1.5, opacity=0.4))
        tangent = always_redraw(lambda: Line(
            top.c2p(x.get_value() - 0.12, f(x.get_value()) - 0.12 * df(x.get_value())),
            top.c2p(x.get_value() + 0.12, f(x.get_value()) + 0.12 * df(x.get_value())),
            color=TEXT_COLOR, stroke_width=4))
        maximum = float(np.sqrt(np.pi / 2))
        # Seleção atômica a cada frame, pelo mesmo x dos gráficos. Sem fades
        # de sinais: zero durante toda a pausa, negativo só após sair do máximo.
        signs = [self.equation(tex, y=-4.1, size=46)
                 for tex in (r"F'>0", r"F'=0", r"F'<0")]
        def current_sign():
            value = x.get_value()
            index = 1 if abs(value - maximum) < 1e-9 else (0 if value < maximum else 2)
            return signs[index].copy()
        sign = always_redraw(current_sign)
        self.play(FadeIn(heading, top, bottom, label_f, label_df, curves,
                         cursors, dots, tangent), run_time=0.3)
        self.add(sign)
        self.play(x.animate.set_value(maximum), run_time=9.7, rate_func=linear)
        self.wait(1.1)
        self.play(x.animate.set_value(1.6), run_time=3.0, rate_func=linear)
        # A fala "segue o Parallax Lab" começa em 68,07 s na narração sincronizada.
        # O CTA assume somente o lugar do título, preservando gráficos e sinais.
        cta = VGroup(
            Text("Siga o Parallax Lab", font_size=30, color=TEXT_COLOR),
            Text("@labparallax", font_size=30, color=PRIMARY_COLOR),
        ).arrange(RIGHT, buff=0.18).move_to([0, 5.5, 0])
        if cta.width > 7.6:
            cta.scale_to_fit_width(7.6)
        self.until(68.07)
        self.play(Succession(FadeOut(heading, run_time=0.12),
                             FadeIn(cta, run_time=0.23)), run_time=0.35)
        # Mantém o CTA legível até depois da última palavra, sem mudar o total.
        self.wait(1.0)


class Integral002SemCoda(Integral002):
    """Mesma resolução, encerrada após a síntese, sem a coda."""

    include_coda = False
