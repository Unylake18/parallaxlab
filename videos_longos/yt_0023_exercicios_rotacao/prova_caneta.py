"""Vídeo-prova da caneta (v5 §3.1b): um voa (termos fixos escritos) e dois passo (glyph map com termos novos), em sequência, 960×540 / 15 fps.
uso: uv run python -m manim -r 960,540 --fps 15 prova_caneta.py ProvaCaneta"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manim import *  # noqa: F401,F403,E402
from MF_Tools import TransformByGlyphMap  # noqa: E402
from prob2 import CanetaAnim, CanetaIntro, Vez  # noqa: E402

BG = "#0A1428"


def eq(s, cor=WHITE):
    return MathTex(s, color=cor).scale(1.5)


class ProvaCaneta(Scene):
    def construct(self):
        self.camera.background_color = BG
        t = Text("CANETA · VOA E PASSO COM TERMO NOVO", font_size=22, color="#8FA6C9").to_edge(UP)
        self.add(t)
        # 1) voa: a linha é escrita termo a termo (fixos) enquanto o termo com origem voa do desenho
        orig = MathTex(r"I_a", color="#FF7EB6").scale(1.3).move_to(LEFT * 5 + UP * 1.5)
        self.add(orig)
        linha1 = MathTex(r"T=mg-ma", color=WHITE).scale(1.5).move_to(UP * 1.5 + RIGHT * 0.5)
        g1 = linha1[0]
        itens = [CanetaAnim(VGroup(g1[0], g1[1]), run_time=1.0), CanetaAnim(VGroup(g1[2], g1[3]), run_time=1.0),
                 CanetaAnim(VGroup(g1[4]), run_time=0.7), CanetaAnim(VGroup(g1[5], g1[6]), run_time=1.0)]
        self.play(AnimationGroup(*[Vez(0.9 * k, a) if k else a for k, a in enumerate(itens)], lag_ratio=0), run_time=4.0)
        self.add(linha1)
        self.wait(0.5)
        # 2) passo 1: T = mg - ma  →  T + ma = mg   (a parte "+ ma" é nova na posição; mg passa de lado)
        l2 = MathTex(r"T+ma=mg", color=WHITE).scale(1.5).move_to(UP * 0.0 + RIGHT * 0.5)
        self.play(TransformByGlyphMap(linha1.copy(), l2, ([0], [0]), ([1], [4]), ([2, 3], [5, 6]), ([5, 6], [2, 3]),
                                      default_introducer=CanetaIntro, auto_fade=True), run_time=2.6)
        self.add(l2)
        self.wait(0.5)
        # 3) passo 2: com termos novos  →  a = (mg - T)/m
        l3 = MathTex(r"a=\frac{mg-T}{m}", color=WHITE).scale(1.5).move_to(DOWN * 1.5 + RIGHT * 0.5)
        self.play(TransformByGlyphMap(l2.copy(), l3, ([3], [0]), ([4], [1]), default_introducer=CanetaIntro, auto_fade=True), run_time=3.0)
        self.add(l3)
        self.wait(1.0)


class ProvaCanetaV6(Scene):
    """v6 §1/§5: linha literal → linha numérica numa linha nova abaixo; os números saem das pílulas e a estrutura nova é escrita pela caneta (E1-4 e E2-2)."""
    def construct(self):
        self.camera.background_color = BG
        t = Text("CANETA · LINHA LITERAL → LINHA NUMÉRICA", font_size=22, color="#8FA6C9").to_edge(UP)
        self.add(t)
        for k, (lit, num, pa, pb, mapa) in enumerate([
            (r"\tau=I\alpha", r"\tau=0{,}50\cdot 2{,}0", ("I=0{,}50", "#FF7EB6"), (r"\alpha=2{,}0", "#C8FF2E"), 0),
            (r"\Sigma\tau=I\alpha", r"\Sigma\tau=0{,}30\cdot 4{,}0", ("I=0{,}30", "#FF7EB6"), (r"\alpha=4{,}0", "#C8FF2E"), 0)]):
            ya = 1.6 if k == 0 else -0.6
            p1 = MathTex(pa[0], color=pa[1]).scale(0.9).move_to(LEFT * 5.4 + UP * (ya + 0.6))
            p2 = MathTex(pb[0], color=pb[1]).scale(0.9).move_to(LEFT * 5.4 + UP * (ya - 0.2))
            self.add(p1, p2)
            l1 = MathTex(lit, color=WHITE).scale(1.4).move_to(RIGHT * 0.6 + UP * (ya + 0.3))
            g = l1[0]
            self.play(AnimationGroup(*[Vez(0.7 * j, CanetaAnim(VGroup(g[j]), run_time=0.8)) if j else CanetaAnim(VGroup(g[j]), run_time=0.8) for j in range(len(g))], lag_ratio=0), run_time=0.7 * len(g) + 0.8)
            self.add(l1)
            l2 = MathTex(num, color=WHITE).scale(1.4).move_to(RIGHT * 0.6 + UP * (ya - 0.5))
            g2 = l2[0]                                                              # v7 §2.2: a linha numérica nasce já no lugar final; a caneta só revela
            self.play(AnimationGroup(*[Vez(0.35 * j, CanetaAnim(VGroup(g2[j]), run_time=0.7)) if j else CanetaAnim(VGroup(g2[j]), run_time=0.7) for j in range(len(g2))], lag_ratio=0), run_time=0.35 * len(g2) + 0.7)
            self.add(l2)
            self.wait(0.6)
        self.wait(0.8)
