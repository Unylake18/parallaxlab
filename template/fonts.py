"""Tipografia oficial do Parallax Lab, carregada de assets/fonts/ (sem instalação global).

Space Grotesk: display, títulos e capas; desde o vid_0005, também todo texto na
tela das animações (manchetes, rótulos, notas, títulos de painel, tag da série),
em Medium, via screen_text(...). Inter: legendas e textos fora da animação.
Matemática continua em MathTex.

Manim: importar este módulo registra as fontes no Pango do processo; use
screen_text(...) ou official_text(...) em vez de Text direto.
Pillow: ImageFont.truetype(str(INTER["bold"]), 40).
"""

from pathlib import Path

import manimpango
from manim import MEDIUM, Text

FONTS_DIR = Path(__file__).resolve().parents[1] / "assets" / "fonts"

DISPLAY_FONT = "Space Grotesk"
TEXT_FONT = "Inter"

SPACE_GROTESK = {
    "medium": FONTS_DIR / "space_grotesk" / "SpaceGrotesk-Medium.ttf",
    "bold": FONTS_DIR / "space_grotesk" / "SpaceGrotesk-Bold.ttf",
}
INTER = {
    "regular": FONTS_DIR / "inter" / "Inter-Regular.ttf",
    "medium": FONTS_DIR / "inter" / "Inter-Medium.ttf",
    "semibold": FONTS_DIR / "inter" / "Inter-SemiBold.ttf",
    "bold": FONTS_DIR / "inter" / "Inter-Bold.ttf",
}

for _path in (*SPACE_GROTESK.values(), *INTER.values()):
    if not manimpango.register_font(str(_path)):
        raise RuntimeError(f"Falha ao registrar fonte: {_path}")

# Pango espaça letras de forma irregular em corpos pequenos; gerar em 4× e
# reduzir mantém o espaçamento original da fonte. Em corpos grandes (manchetes
# ~38) o 4× faz o Pango quebrar linhas longas: passe oversample=2.
_OVERSAMPLE = 4


def official_text(content: str, font: str, weight: str, font_size: float,
                  oversample: int = _OVERSAMPLE, **kwargs) -> Text:
    return Text(content, font=font, weight=weight,
                font_size=font_size * oversample, **kwargs).scale(1 / oversample)


def screen_text(content: str, font_size: float, **kwargs) -> Text:
    """Texto na tela das animações: Space Grotesk Medium (decisão de 2026-09-27)."""
    return official_text(content, DISPLAY_FONT, MEDIUM, font_size, **kwargs)
