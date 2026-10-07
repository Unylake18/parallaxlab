"""Exemplo e teste da ponte Blender -> Manim (sandbox; não é uma cena de vídeo).

Mostra o uso típico: sólido 3D animado com elementos Manim atrás (fundo) e na frente (seta, equação), FadeIn/FadeOut,
pausa do movimento, e um sólido estático.

Rodar, a partir da raiz do repositório:
    uv run --no-sync python -m manim -r 960,540 --fps 15 experimentos/blender/arsenal/exemplo_manim.py ExemploSolido3D
(A primeira execução renderiza as sequências no Blender e guarda em renders/arsenal3d/; as seguintes só leem.)
"""

import sys
from pathlib import Path

from manim import (
    DOWN, LEFT, RIGHT, UP, Arrow, FadeIn, FadeOut, MathTex, Rectangle, Scene, config,
)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manim_solido3d import Solido3D  # noqa: E402

config.background_color = "#050816"
TEXTO, CAMPO, GAUSS = "#F5F7FF", "#35D9FF", "#9C8CFF"


class ExemploSolido3D(Scene):
    def construct(self):
        # 1) fio com corrente: sólido animado à direita; Manim atrás (painel) e na frente (seta, equação)
        painel = Rectangle(width=7.2, height=6.2, stroke_color=GAUSS, stroke_width=2, fill_color="#0B1030",
                           fill_opacity=0.9).move_to(RIGHT * 3.4)
        eq = MathTex(r"B\,(2\pi r)=\mu_0 I_{\mathrm{env}}", color=TEXTO, font_size=44).move_to(LEFT * 3.6 + UP * 1.0)
        fio = Solido3D("fio_infinito")
        img = fio.mobject(cena=self, largura=7.0, centro=RIGHT * 3.4, periodo=2.0)
        seta = Arrow(RIGHT * 1.8 + DOWN * 2.6, RIGHT * 4.4 + DOWN * 2.6, color=CAMPO, buff=0)   # sentido: Manim
        rot = MathTex("I", color=CAMPO, font_size=44).next_to(seta, DOWN, buff=0.1)

        self.add(painel)
        self.play(FadeIn(img), FadeIn(eq), run_time=1.0)     # FadeIn com o movimento ligado
        self.add(seta, rot)
        self.wait(4.0)                                        # 2 loops
        img.pausar()
        self.wait(1.0)                                        # congelado
        img.retomar()
        self.wait(1.0)
        self.play(FadeOut(img), FadeOut(eq), FadeOut(seta), FadeOut(rot), run_time=0.8)

        # 2) sólido estático e depois um animado de outra família (disco girando)
        casca = Solido3D("casca_cilindrica_oca")
        est = casca.mobject(altura=5.0, centro=LEFT * 3.4)
        disco = Solido3D("disco_carregado")
        rodando = disco.mobject(cena=self, altura=5.0, centro=RIGHT * 3.4, periodo=3.0)
        self.play(FadeIn(est), FadeIn(rodando), run_time=0.8)
        self.wait(3.0)
