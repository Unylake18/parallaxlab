"""Teste visual isolado da tipografia oficial; não é vídeo de produção.

uv run python -m manim -r 1080,1920 --fps 30 template/teste_tipografia.py TesteTipografia
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import (  # noqa: E402
    BOLD, DOWN, FadeIn, MathTex, MEDIUM, NORMAL, SEMIBOLD, Scene, VGroup,
)

from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, TEXT_COLOR  # noqa: E402
from template.fonts import DISPLAY_FONT, TEXT_FONT, official_text  # noqa: E402


def text(content, font, weight, size, color=TEXT_COLOR):
    return official_text(content, font, weight, size, color=color)


class TesteTipografia(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        display = VGroup(
            text("DE ONDE VEM?", DISPLAY_FONT, BOLD, 64),
            text("INTEGRAÇÃO POR PARTES", DISPLAY_FONT, BOLD, 40, PRIMARY_COLOR),
            text("ESCOLHENDO u", DISPLAY_FONT, BOLD, 48, SECONDARY_COLOR),
        ).arrange(DOWN, buff=0.28)
        series = VGroup(
            text("POR TRÁS DA FÓRMULA · EP. 01", DISPLAY_FONT, MEDIUM, 26),
            text("EXERCÍCIOS RESOLVIDOS · EP. 03", DISPLAY_FONT, MEDIUM, 26),
        ).arrange(DOWN, buff=0.18)
        auxiliary = VGroup(
            text("Integração por partes", TEXT_FONT, NORMAL, 30),
            text("Subtraímos dos dois lados", TEXT_FONT, MEDIUM, 30),
            text("A função exponencial permanece", TEXT_FONT, MEDIUM, 30),
            text("0123456789  + − = ×  (a, b): ç ã õ é ê í ó ú à", TEXT_FONT, NORMAL, 26),
        ).arrange(DOWN, buff=0.16)
        math = VGroup(
            text("Regra do produto:", TEXT_FONT, MEDIUM, 28),
            MathTex(r"\int u\,dv = uv - \int v\,du", font_size=58, color=TEXT_COLOR),
        ).arrange(DOWN, buff=0.22)
        caption = VGroup(
            text("Então, à direita, esse termo", TEXT_FONT, SEMIBOLD, 34),
            text("aparece com sinal negativo.", TEXT_FONT, SEMIBOLD, 34),
        ).arrange(DOWN, buff=0.1)
        cta = VGroup(
            text("Segue o Parallax Lab", TEXT_FONT, BOLD, 36),
            text("@labparallax", TEXT_FONT, BOLD, 40, PRIMARY_COLOR),
        ).arrange(DOWN, buff=0.14)
        page = VGroup(display, series, auxiliary, math, caption, cta).arrange(DOWN, buff=0.55)
        if page.height > 14.6:
            page.scale_to_fit_height(14.6)
        self.play(FadeIn(page), run_time=0.5)
        self.wait(1.5)
