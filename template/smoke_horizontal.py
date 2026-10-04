"""Smoke test do formato longo_horizontal (16:9); não é vídeo de produção.

Testa fundo, headline Space Grotesk, MathTex, layout SPLIT (geometria à esquerda, equação + gráfico à
direita controlados pelo mesmo parâmetro), uma transformação matemática, watermark e safe area.

uv run python -m manim -r 960,540 --fps 15 template/smoke_horizontal.py SmokeHorizontal
GUIAS=1 mostra a safe area (só desenvolvimento).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import (  # noqa: E402
    BOLD, DOWN, LEFT, RIGHT, UP, Axes, Create, Dot, FadeIn, ImageMobject, MathTex, Scene, Square,
    TransformMatchingTex, ValueTracker, VGroup, Write, always_redraw,
)

from template.config_horizontal import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH  # noqa: E402
from template.fonts import DISPLAY_FONT, official_text, screen_text  # noqa: E402
from template.layout_horizontal import CONTENT_TOP, GUIAS, safe_guides, split  # noqa: E402

BLUE = "#267BFF"   # geometria
CYAN = PRIMARY_COLOR   # área A: mesma cor na equação, no preenchimento e na curva
UNIT = 1.2             # unidades de cena por unidade de a


class SmokeHorizontal(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        left, right = split(0.5)

        wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(0.35).to_corner(UP + RIGHT, buff=0.3)
        tag = screen_text("TESTE · LONGO HORIZONTAL", 20, color=TEXT_COLOR).set_opacity(0.65)
        tag.to_corner(UP + LEFT, buff=0.4)
        headline = official_text("UM PARÂMETRO, DUAS PERSPECTIVAS", DISPLAY_FONT, BOLD, 40,
                                 oversample=2, color=TEXT_COLOR)
        headline.move_to([0, CONTENT_TOP + 0.5, 0])
        self.add(wm)
        if GUIAS:
            self.add(safe_guides())
        self.play(FadeIn(tag), FadeIn(headline, shift=0.2 * DOWN), run_time=0.8)

        # Esquerda: o quadrado de lado a.
        a = ValueTracker(2.0)
        square = always_redraw(lambda: Square(a.get_value() * UNIT, color=BLUE, stroke_width=4)
                               .set_fill(CYAN, opacity=0.18).move_to(left.center))
        side = always_redraw(lambda: MathTex("a", font_size=48, color=TEXT_COLOR)
                             .next_to(square, DOWN, buff=0.25))
        self.play(Create(square), FadeIn(side), run_time=1.0)

        # Direita: equação no topo, gráfico A(a) embaixo; o mesmo a controla tudo.
        eq_top = right.y + right.height / 2 - 0.5
        eq1 = MathTex("A", "=", "a", r"\cdot", "a", font_size=60, color=TEXT_COLOR)
        eq1[0].set_color(CYAN)
        eq1.move_to([right.x, eq_top, 0])
        self.play(Write(eq1), run_time=1.0)
        self.wait(0.4)
        eq2 = MathTex("A", "=", "a", "^{2}", font_size=60, color=TEXT_COLOR).move_to(eq1)
        eq2[0].set_color(CYAN)
        self.play(TransformMatchingTex(eq1, eq2), run_time=1.0)

        axes = Axes(x_range=[0, 3.2, 1], y_range=[0, 10, 2], x_length=5.0, y_length=3.2,
                    axis_config={"color": TEXT_COLOR, "stroke_opacity": 0.6, "include_tip": False})
        labels = axes.get_axis_labels(MathTex("a", font_size=36), MathTex("A", font_size=36, color=CYAN))
        graph = VGroup(axes, labels)
        graph.move_to([right.x, eq_top - 0.7 - graph.height / 2, 0])
        curve = axes.plot(lambda x: x * x, x_range=[0, 3.15], color=CYAN, stroke_width=4)
        dot = always_redraw(lambda: Dot(axes.c2p(a.get_value(), a.get_value() ** 2), radius=0.09, color=CYAN))
        self.play(Create(axes), FadeIn(labels), run_time=0.8)
        self.play(Create(curve), FadeIn(dot), run_time=1.0)

        for value in (3.0, 1.2, 2.0):
            self.play(a.animate.set_value(value), run_time=1.4)
        self.wait(1.0)
