"""Helpers reutilizáveis para as cenas Manim do Parallax Lab."""

from manim import MathTex, Text


def make_title(text: str) -> Text:
    return Text(text, font_size=42)


def make_equation(tex: str) -> MathTex:
    return MathTex(tex).scale(1.15)
