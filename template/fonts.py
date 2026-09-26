"""Tipografia oficial do Parallax Lab, carregada de assets/fonts/ (sem instalação global).

Space Grotesk: display, headlines, títulos e capas. Inter: textos auxiliares,
legendas e CTA. Matemática continua em MathTex. Uso a partir do vid_0004.

Manim: importar este módulo registra as fontes no Pango do processo; use
official_text(...) em vez de Text direto. Pillow: ImageFont.truetype(str(INTER["bold"]), 40).
"""

from pathlib import Path

import manimpango
from manim import Text

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
# reduzir mantém o espaçamento original da fonte.
_OVERSAMPLE = 4


def official_text(content: str, font: str, weight: str, font_size: float, **kwargs) -> Text:
    return Text(content, font=font, weight=weight,
                font_size=font_size * _OVERSAMPLE, **kwargs).scale(1 / _OVERSAMPLE)
