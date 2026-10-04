"""Guias de composição do formato longo_horizontal (frame lógico 16 × 9).

Regiões, não painéis: nada aqui desenha na tela, exceto safe_guides(), que é só desenvolvimento.
Valores iniciais e internos de composição, não especificação de plataforma; ajustar com evidência.

Modos (ver docs/formatos.md):
  FOCUS   — região FOCUS: um elemento dominante, bastante espaço negativo.
  SPLIT   — split(0.5) ou split(0.55): fenômeno/geometria à esquerda, análise à direita.
  COMPARE — split(0.5): duas perspectivas comparáveis, no máximo duas ideias simultâneas.
  BUILD   — derivação transformando a relação atual dentro de FOCUS ou de um lado do split.
"""

import os
from typing import NamedTuple

import numpy as np
from manim import DashedLine, DashedVMobject, Rectangle, VGroup

SAFE_X, SAFE_Y = 7.2, 3.8      # conteúdo crítico em |x| <= 7.2 e |y| <= 3.8
CONTENT_TOP = 2.6              # acima: faixa de título/headline
CONTENT_BOTTOM = -3.0          # abaixo: faixa reservada a legendas/controles/respiro

GUIAS = os.environ.get("GUIAS") == "1"   # liga safe_guides() em desenvolvimento; desligado por padrão


class Region(NamedTuple):
    x: float
    y: float
    width: float
    height: float

    @property
    def center(self):
        return np.array([self.x, self.y, 0.0])

    def place(self, mob):
        """Centraliza mob na região, reduzindo (nunca ampliando) se não couber."""
        if mob.width > self.width or mob.height > self.height:
            mob.scale(min(self.width / mob.width, self.height / mob.height))
        return mob.move_to(self.center)


_MID_Y = (CONTENT_TOP + CONTENT_BOTTOM) / 2
_H = CONTENT_TOP - CONTENT_BOTTOM

FOCUS = Region(0.0, _MID_Y, 2 * SAFE_X - 3, _H)


def split(left_fraction=0.5, gap=0.6):
    """(esquerda, direita) dentro da safe area. 0.5 = 50/50; 0.55 = 55/45 a favor da esquerda."""
    usable = 2 * SAFE_X - gap
    wl = usable * left_fraction
    wr = usable - wl
    return Region(-SAFE_X + wl / 2, _MID_Y, wl, _H), Region(SAFE_X - wr / 2, _MID_Y, wr, _H)


def safe_guides():
    """Safe area, faixas de título/legenda e eixo central. Só com GUIAS=1; nunca no render final."""
    lines = VGroup(
        DashedVMobject(Rectangle(width=2 * SAFE_X, height=2 * SAFE_Y), num_dashes=90),
        DashedLine([-SAFE_X, CONTENT_TOP, 0], [SAFE_X, CONTENT_TOP, 0]),
        DashedLine([-SAFE_X, CONTENT_BOTTOM, 0], [SAFE_X, CONTENT_BOTTOM, 0]),
        DashedLine([0, CONTENT_BOTTOM, 0], [0, CONTENT_TOP, 0]),
    )
    return lines.set_stroke("#FF5A5A", width=1.5, opacity=0.7).set_z_index(100)


if __name__ == "__main__":
    for frac in (0.5, 0.55):
        left, right = split(frac)
        assert left.x - left.width / 2 >= -SAFE_X - 1e-9 and right.x + right.width / 2 <= SAFE_X + 1e-9
        assert left.x + left.width / 2 < right.x - right.width / 2   # há vão entre os lados
        assert abs(left.width / (left.width + right.width) - frac) < 1e-9
    print("layout_horizontal ok")
