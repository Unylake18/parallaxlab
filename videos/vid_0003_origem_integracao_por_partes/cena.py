"""Regra do produto reorganizada e integrada; preview visual, sem voz.

As integrais da derivação representam primitivas, até uma constante.
Na coda, representam acumulações ao longo do arco desenhado desde (0, 0).
"""

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UP, Axes, Create, Dot, FadeIn, FadeOut,
    ImageMobject, Indicate, Line, MathTex, Polygon, ReplacementTransform,
    Scene, SurroundingRectangle, Text, VGroup, VMobject, Write,
    ValueTracker, always_redraw, linear,
)

from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH

VDU = PRIMARY_COLOR
UDV = "#EA63FF"


class Integral003(Scene):
    include_coda = True

    def equation(self, *tex, y=1.5, size=60, cyan=(), pink=()):
        mob = MathTex(*tex, font_size=size, color=TEXT_COLOR)
        if mob.width > 7.6:
            mob.scale_to_fit_width(7.6)
        mob.move_to([0, y, 0])
        for index in cyan:
            mob[index].set_color(VDU)
        for index in pink:
            mob[index].set_color(UDV)
        return mob

    def note(self, text, y=5.2, size=30):
        mob = Text(text, font_size=size, color=TEXT_COLOR, line_spacing=1.1)
        if mob.width > 7.6:
            mob.scale_to_fit_width(7.6)
        return mob.move_to([0, y, 0])

    def guide(self, *parts, y=-1.2, size=27):
        """Texto-base temporário; uma tupla contém LaTeX para os símbolos."""
        mob = VGroup(*(
            MathTex(part[0], font_size=size + 9, color=TEXT_COLOR)
            if isinstance(part, tuple)
            else Text(part, font_size=size, color=TEXT_COLOR)
            for part in parts
        )).arrange(RIGHT, buff=0.08)
        if mob.width > 7.6:
            mob.scale_to_fit_width(7.6)
        return mob.move_to([0, y, 0])

    def until(self, seconds):
        remaining = seconds - self.time
        if remaining > 1e-6:
            self.wait(remaining)

    def morph(self, source, target, mappings, run_time=1.2, arcs=None):
        """Mapeamento explícito de fatores; nenhum matching de símbolos repetidos."""
        arcs = arcs or {}
        animations = []
        for number, (old, new) in enumerate(mappings):
            old_part = VGroup(*(source[i] for i in old))
            new_part = VGroup(*(target[i] for i in new))
            animations.append(ReplacementTransform(
                old_part, new_part, path_arc=arcs.get(number, 0)))
        self.play(*animations, run_time=run_time)
        self.remove(source, *source.submobjects, *target.submobjects)
        self.add(target)
        return target

    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.add(ImageMobject(str(WATERMARK_PATH)).set_width(1.8)
                 .set_opacity(0.35).to_corner(UP + RIGHT, buff=0.28))
        heading = self.note("De onde vem a fórmula\nda integração por partes?")
        caption = self.guide("Tudo começa na regra do produto")
        eq = self.equation(r"(uv)'", "=", "u'", "v", "+", "u", "v'",
                           cyan=(2, 3), pink=(5, 6))
        self.play(FadeIn(heading, caption), Write(eq), run_time=1)
        self.until(4)

        # Os três dx entram juntos; fatores antigos continuam identificáveis.
        dx = self.equation(r"(uv)'", r"\,dx", "=", "u'", "v", r"\,dx",
                           "+", "u", "v'", r"\,dx", cyan=(3, 4, 5), pink=(7, 8, 9))
        next_caption = self.guide("Multiplicando a igualdade por ", (r"dx",))
        self.play(FadeOut(heading), ReplacementTransform(caption, next_caption),
                  *(ReplacementTransform(eq[a], dx[b]) for a, b in
                    ((0, 0), (1, 2), (2, 3), (3, 4), (4, 6), (5, 7), (6, 8))),
                  *(Write(dx[i]) for i in (1, 5, 9)), run_time=1.5)
        self.remove(eq, *dx.submobjects)
        self.add(dx)
        eq = dx
        self.until(9)

        caption = self.guide("Cada derivada agora vira seu diferencial")
        self.play(FadeOut(next_caption), run_time=0.25)
        self.play(FadeIn(caption),
                  Indicate(VGroup(eq[0], eq[1]), color=TEXT_COLOR), run_time=0.75)
        target = self.equation(r"d(uv)", "=", "u'", "v", r"\,dx", "+",
                               "u", "v'", r"\,dx", cyan=(2, 3, 4), pink=(6, 7, 8))
        eq = self.morph(eq, target, [([0, 1], [0])] +
                        [([i], [i - 1]) for i in range(2, 10)])
        self.play(FadeOut(caption), run_time=0.25)
        self.until(14)

        # v sai do meio: u' dx fica contíguo antes de virar du.
        reordered = self.equation(r"d(uv)", "=", "v", "u'", r"\,dx", "+",
                                  "u", "v'", r"\,dx", cyan=(2, 3, 4), pink=(6, 7, 8))
        eq = self.morph(eq, reordered,
                        [([i], [j]) for i, j in ((0, 0), (1, 1), (2, 3), (3, 2),
                                                 (4, 4), (5, 5), (6, 6), (7, 7), (8, 8))],
                        arcs={2: -np.pi / 2, 3: -np.pi / 2})
        self.play(Indicate(VGroup(eq[3], eq[4]), color=VDU), run_time=0.8)
        target = self.equation(r"d(uv)", "=", "v", r"\,du", "+", "u", "v'", r"\,dx",
                               cyan=(2, 3), pink=(5, 6, 7))
        eq = self.morph(eq, target, [([0], [0]), ([1], [1]), ([2], [2]), ([3, 4], [3]),
                                     ([5], [4]), ([6], [5]), ([7], [6]), ([8], [7])])
        self.play(Indicate(eq[3], color=VDU), run_time=0.6)
        self.until(20)

        self.play(Indicate(VGroup(eq[6], eq[7]), color=UDV), run_time=0.8)
        target = self.equation(r"d(uv)", "=", "v", r"\,du", "+", "u", r"\,dv",
                               cyan=(2, 3), pink=(5, 6))
        eq = self.morph(eq, target, [([i], [i]) for i in range(6)] + [([6, 7], [6])])
        self.play(Indicate(eq[6], color=UDV), run_time=0.6)
        self.until(25)

        # Expõe a igualdade com u dv à esquerda antes da transposição central.
        caption = self.guide("Agora queremos isolar ", (r"u\,dv",))
        self.play(FadeIn(caption), run_time=0.5)
        target = self.equation(r"u\,dv", "+", r"v\,du", "=", r"d(uv)",
                               cyan=(2,), pink=(0,))
        eq = self.morph(eq, target, [([0], [4]), ([1], [3]), ([2, 3], [2]),
                                     ([4], [1]), ([5, 6], [0])],
                        run_time=1.8, arcs={0: -np.pi / 2, 4: -np.pi / 2})
        self.until(29)

        next_caption = self.guide("Subtraímos ", (r"v\,du",), " dos dois lados")
        self.play(ReplacementTransform(caption, next_caption), run_time=0.5)
        caption = next_caption
        target = self.equation(r"u\,dv", "=", r"d(uv)", "-", r"v\,du",
                               cyan=(4,), pink=(0,))
        # + e v du viajam juntos acima da linha. A mudança de sinal acontece
        # durante a travessia da igualdade, sem FadeOut da relação inteira.
        traveling = VGroup(eq[1], eq[2])
        destination = VGroup(target[3], target[4])
        raised = destination.copy().shift(UP * 1.5)
        self.play(Indicate(traveling, color=VDU),
                  eq[0].animate.set_opacity(0.35),
                  eq[3].animate.set_opacity(0.35),
                  eq[4].animate.set_opacity(0.35), run_time=0.5)
        self.play(traveling.animate.shift(UP * 1.5), run_time=0.6)
        self.play(ReplacementTransform(eq[0], target[0]),
                  ReplacementTransform(eq[3], target[1]),
                  ReplacementTransform(eq[4], target[2]),
                  ReplacementTransform(traveling, raised),
                  run_time=2)
        # Reúne os objetos transitórios sem trocar a equação visível.
        self.play(ReplacementTransform(raised, destination), run_time=0.6)
        self.remove(eq, *eq.submobjects, *target.submobjects)
        target.set_opacity(1)
        self.add(target)
        eq = target
        self.play(FadeOut(caption), run_time=0.25)
        self.until(35)

        next_caption = self.guide("Integramos os dois lados")
        target = self.equation(r"\int", r"u\,dv", "=", r"\int", r"d(uv)", "-",
                               r"\int", r"v\,du", cyan=(6, 7), pink=(0, 1))
        self.play(FadeIn(next_caption),
                  *(ReplacementTransform(eq[a], target[b]) for a, b in
                    ((0, 1), (1, 2), (2, 4), (3, 5), (4, 7))),
                  *(Write(target[i]) for i in (0, 3, 6)), run_time=1.5)
        self.remove(eq, *target.submobjects)
        self.add(target)
        eq, caption = target, next_caption
        self.play(FadeOut(caption), run_time=0.25)
        self.until(39)
        target = self.equation(r"\int u\,dv", "=", "uv", "-", r"\int v\,du",
                               pink=(0,), cyan=(4,))
        eq = self.morph(eq, target, [([0, 1], [0]), ([2], [1]), ([3, 4], [2]),
                                     ([5], [3]), ([6, 7], [4])])
        box = SurroundingRectangle(eq, color=PRIMARY_COLOR, buff=0.25)
        constant = self.guide("Para primitivas, a constante fica implícita", size=24)
        self.play(Create(box), FadeIn(constant), run_time=0.6)
        self.until(44)

        verify_heading = self.guide("Cheque: derivando, voltamos a ", (r"uv'",), y=5.2)
        derivative = self.equation(r"\frac{d}{dx}", r"\left(uv-\int vu'\,dx\right)", size=58)
        self.play(FadeOut(eq, box, constant), FadeIn(verify_heading, derivative), run_time=0.6)
        self.until(46)
        check = self.equation("u'v", "+", "uv'", "-", "vu'", cyan=(0, 4), pink=(2,))
        self.play(ReplacementTransform(derivative, check), run_time=1)
        self.until(48)
        slashes = VGroup(*(Line(check[i].get_corner(DOWN + LEFT),
                                check[i].get_corner(UP + RIGHT), color=VDU, stroke_width=4)
                           for i in (0, 4)))
        self.play(Create(slashes), run_time=0.6)
        cancellation = self.equation("u'v", "-", "vu'", "=0", y=-0.2, size=48, cyan=(0, 2))
        self.play(FadeIn(cancellation), run_time=0.5)
        self.until(50)
        recovered = self.equation("uv'", pink=(0,))
        self.play(FadeOut(slashes, cancellation, check[0], check[1], check[3], check[4]),
                  ReplacementTransform(check[2], recovered[0]), run_time=0.8)
        self.remove(check)
        self.add(recovered)
        self.until(52)
        summary = self.note("Regra do produto\nreorganizada e integrada")
        final = self.equation(r"\int u\,dv", "=", "uv", "-", r"\int v\,du",
                              pink=(0,), cyan=(4,))
        final_box = SurroundingRectangle(final, color=PRIMARY_COLOR, buff=0.25)
        self.play(FadeOut(verify_heading, recovered), FadeIn(summary, final, final_box, constant), run_time=0.6)
        self.until(56)
        if self.include_coda:
            self.geometry_coda(VGroup(summary, final, final_box, constant))

    def geometry_coda(self, previous):
        """Fatia em cada direção, seguida da acumulação no caso desenhado."""
        start = self.time
        heading = self.note("Uma segunda forma de enxergar", size=28)
        scope = self.guide("Caso: curva crescente de ", (r"(0,0)",),
                           " a ", (r"(U,V)",), y=4.2, size=21)
        axes = Axes(x_range=[0, 1.12, 1], y_range=[0, 1.15, 1],
                    x_length=6.1, y_length=4.8, tips=True,
                    axis_config={"include_ticks": False, "color": TEXT_COLOR, "stroke_width": 2})
        axes.move_to([0, 0.6, 0])
        origin, corner = axes.c2p(0, 0), axes.c2p(1, 1)
        controls = np.array([[0, 0], [0.25, 0.10], [0.65, 0.40], [1, 1]])
        def point(t):
            return ((1-t)**3 * controls[0] + 3*(1-t)**2*t * controls[1]
                    + 3*(1-t)*t*t * controls[2] + t**3 * controls[3])

        def arc(through):
            return [axes.c2p(*point(t)) for t in np.linspace(0, through, 61)]

        samples = arc(1)
        lower = Polygon(origin, axes.c2p(1, 0), *reversed(samples[1:]),
                        fill_color=VDU, fill_opacity=0.27, stroke_width=0)
        upper = Polygon(*samples, axes.c2p(0, 1), fill_color=UDV,
                        fill_opacity=0.25, stroke_width=0)

        def accumulated(through, vertical):
            path = arc(max(0.001, through))
            u, v = point(max(0.001, through))
            corners = ([origin, axes.c2p(u, 0), *reversed(path[1:])]
                       if vertical else [*path, axes.c2p(0, v)])
            return Polygon(*corners, fill_color=VDU if vertical else UDV,
                           fill_opacity=0.27 if vertical else 0.25,
                           stroke_width=0)

        def slice_at(through, vertical):
            u, v = point(through)
            if vertical:
                corners = [axes.c2p(u-0.023, 0), axes.c2p(u+0.023, 0),
                           axes.c2p(u+0.023, v), axes.c2p(u-0.023, v)]
            else:
                corners = [axes.c2p(0, v-0.028), axes.c2p(u, v-0.028),
                           axes.c2p(u, v+0.028), axes.c2p(0, v+0.028)]
            return Polygon(*corners, fill_color=VDU if vertical else UDV,
                           fill_opacity=0.85, stroke_width=0)

        border = VGroup(Line(axes.c2p(0, 1), corner), Line(corner, axes.c2p(1, 0)))
        border.set_stroke(TEXT_COLOR, width=2, opacity=0.65)
        curve = VMobject(color=TEXT_COLOR, stroke_width=4).set_points_as_corners(samples)
        labels = VGroup(
            MathTex("u", font_size=36).next_to(axes.x_axis.get_end(), RIGHT, buff=0.12),
            MathTex("v", font_size=36).next_to(axes.y_axis.get_end(), UP, buff=0.12),
            MathTex("0", font_size=30).next_to(origin, DOWN + LEFT, buff=0.08),
            MathTex("U", font_size=34).next_to(axes.c2p(1, 0), DOWN, buff=0.16),
            MathTex("V", font_size=34).next_to(axes.c2p(0, 1), LEFT, buff=0.16),
            MathTex("(U,V)", font_size=32).next_to(corner, UP, buff=0.16),
        ).set_color(TEXT_COLOR)
        low_label = MathTex(r"\int_0^U v\,du", color=VDU, font_size=39).move_to(axes.c2p(0.73, 0.16))
        high_label = MathTex(r"\int_0^V u\,dv", color=UDV, font_size=39).move_to(axes.c2p(0.27, 0.71))

        self.play(FadeOut(previous), FadeIn(heading, scope, axes, labels, border), run_time=0.5)
        self.play(Create(curve), FadeIn(Dot(corner, radius=0.055, color=TEXT_COLOR)), run_time=0.5)

        # Uma fatia vertical: altura v, largura du, contribuição v du.
        sample_v = slice_at(0.55, True)
        height_v = MathTex("v", color=VDU, font_size=35).next_to(sample_v, LEFT, buff=0.12)
        width_du = MathTex("du", color=VDU, font_size=35).next_to(sample_v, DOWN, buff=0.14)
        low_cue = MathTex(r"v\,du", color=VDU, font_size=44).move_to([0, -3.5, 0])
        self.play(FadeIn(sample_v, height_v, width_du, low_cue), run_time=0.7)
        self.wait(0.5)
        sweep_u = ValueTracker(0.001)
        lower_growing = always_redraw(lambda: accumulated(sweep_u.get_value(), True))
        moving_v = always_redraw(lambda: slice_at(sweep_u.get_value(), True))
        self.play(FadeOut(sample_v, height_v, width_du),
                  FadeIn(lower_growing, moving_v), run_time=0.25)
        self.play(sweep_u.animate.set_value(1), run_time=1.5, rate_func=linear)
        self.remove(lower_growing, moving_v)
        self.add(lower)
        self.bring_to_front(axes, border, curve, labels)
        self.play(ReplacementTransform(low_cue, low_label), run_time=0.5)

        # Uma fatia horizontal: largura u, espessura dv, contribuição u dv.
        sample_h = slice_at(0.55, False)
        width_u = MathTex("u", color=UDV, font_size=35).next_to(sample_h, UP, buff=0.10)
        height_dv = MathTex("dv", color=UDV, font_size=35).next_to(sample_h, LEFT, buff=0.14)
        high_cue = MathTex(r"u\,dv", color=UDV, font_size=44).move_to([0, -3.5, 0])
        self.play(FadeIn(sample_h, width_u, height_dv, high_cue), run_time=0.7)
        self.wait(0.5)
        sweep_v = ValueTracker(0.001)
        upper_growing = always_redraw(lambda: accumulated(sweep_v.get_value(), False))
        moving_h = always_redraw(lambda: slice_at(sweep_v.get_value(), False))
        self.play(FadeOut(sample_h, width_u, height_dv),
                  FadeIn(upper_growing, moving_h), run_time=0.25)
        self.play(sweep_v.animate.set_value(1), run_time=1.5, rate_func=linear)
        self.remove(upper_growing, moving_h)
        self.add(upper)
        self.bring_to_front(axes, border, curve, labels, low_label)
        self.play(ReplacementTransform(high_cue, high_label), run_time=0.5)

        total = MathTex("UV", font_size=56, color=TEXT_COLOR).move_to([0, -3.5, 0])
        synthesis = self.equation("UV", "=", r"\int_0^U v\,du", "+",
                                  r"\int_0^V u\,dv", y=-3.5, size=48,
                                  cyan=(2,), pink=(4,))
        box = SurroundingRectangle(synthesis, color=PRIMARY_COLOR, buff=0.16)
        qualifier = self.guide("As duas regiões completam o retângulo ",
                               (r"UV",), y=-4.9, size=21)
        self.play(FadeIn(total), Indicate(border, color=TEXT_COLOR), run_time=0.6)
        self.play(ReplacementTransform(total, synthesis[0]),
                  Write(VGroup(*synthesis[1:])), Create(box), FadeIn(qualifier),
                  run_time=1)
        self.add(synthesis)
        self.until(start + 11.5)


class Integral003SemCoda(Integral003):
    """Derivação, verificação e síntese completas, com encerramento em 56 s."""

    include_coda = False
