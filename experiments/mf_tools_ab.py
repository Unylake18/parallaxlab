"""Teste A/B temporario: TransformMatchingTex vs MF_Tools.TransformByGlyphMap.

uv run --frozen --with "MF-Tools[manimce]==1.4.9" python -m manim -r 540,960 --fps 15 \
    experiments/mf_tools_ab.py MFToolsABMatching MFToolsABGlyphMap
"""
from manim import *
from MF_Tools import TransformByGlyphMap

config.frame_width, config.frame_height = 9, 16
config.background_color = "#050816"
CYAN, VIOLET = "#35D9FF", "#745CFF"
S = 1.9  # escala das formulas


class Base(Scene):
    METHOD = ""

    def setup(self):
        t = Text(self.METHOD, font_size=34, color=CYAN).to_edge(UP, buff=1.2)
        self.add(t)

    def run_case(self, n, A, B, animate, pre=None):
        tag = Text(f"Caso {n}", font_size=28, color=VIOLET).next_to(self.mobjects[0], DOWN, buff=1)
        A.scale(S); B.scale(S)
        self.play(FadeIn(tag), FadeIn(A), run_time=0.4)
        self.wait(0.4)
        if pre:
            self.play(*pre(A), run_time=0.6)
        self.play(animate(A, B), run_time=1.6)
        self.wait(0.7)
        self.play(FadeOut(B), FadeOut(tag), run_time=0.3)
        self.remove(A)


class MFToolsABMatching(Base):
    METHOD = "TransformMatchingTex"

    def construct(self):
        tm = lambda A, B: TransformMatchingTex(A, B)
        # Caso 1
        self.run_case(1, MathTex("a", "+", "b", "=", "c"), MathTex("a", "=", "c", "-", "b"), tm)
        # Caso 2
        self.run_case(2, MathTex("x^2", "+", "2x", "+", "1"), MathTex("(", "x", "+", "1", ")^2"), tm)
        # Caso 3
        self.run_case(
            3, MathTex("u'v", "+", "uv'", "-vu'"), MathTex("uv'"), tm,
            pre=lambda A: [A[0].animate.set_color(RED), A[3].animate.set_color(RED)],
        )


class MFToolsABGlyphMap(Base):
    METHOD = "TransformByGlyphMap"

    def construct(self):
        # Caso 1: b atravessa a igualdade em arco
        self.run_case(
            1, MathTex("a+b=c"), MathTex("a=c-b"),
            lambda A, B: TransformByGlyphMap(
                A, B, ([0], [0]), ([3], [1]), ([4], [2]), ([1], [3]),
                ([2], [4], {"path_arc": -PI}),
            ),
        )
        # Caso 2: x^2+2x+1 -> (x+1)^2
        self.run_case(
            2, MathTex("x^2+2x+1"), MathTex("(x+1)^2"),
            lambda A, B: TransformByGlyphMap(
                A, B, ([], [0, 4]), ([0], [1]), ([2], [2]), ([6], [3]), ([1], [5], {"path_arc": -PI / 2}),
                ([3, 4, 5], []),
            ),
        )
        # Caso 3: u'v e -vu' saem em direcoes opostas, uv' fica
        self.run_case(
            3, MathTex("u'v+uv'-vu'"), MathTex("uv'"),
            lambda A, B: TransformByGlyphMap(
                A, B, ([0, 1, 2, 3], [], {"shift": UP * 0.8}), ([7, 8, 9, 10], [], {"shift": DOWN * 0.8}),
                ([4, 5, 6], [0, 1, 2]),
            ),
            pre=lambda A: [A[0][i].animate.set_color(RED) for i in (0, 1, 2, 3, 7, 8, 9, 10)],
        )
