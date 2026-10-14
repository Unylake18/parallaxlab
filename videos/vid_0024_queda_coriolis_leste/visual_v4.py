import sys
from pathlib import Path
import numpy as np
from manim import *

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from template.config import BACKGROUND_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text

config.background_color = BACKGROUND_COLOR

# Gramática semântica de cores oficial Parallax Lab
WHITE_COLOR = "#F5F7FF"
CYAN_COLOR = "#35D9FF"     # Coriolis, leste, desvio lateral, resultado principal
BLUE_COLOR = "#267BFF"     # Velocidade da bola, movimento radial da conta
VIOLET_COLOR = "#745CFF"   # Rotação, omega, omega_T, norte entrando na tela
MAGENTA_COLOR = "#EA63FF"  # Aviso excepcional de desvio exagerado
MUTED_COLOR = "#8492AE"    # Rótulos secundários, eixos neutros, linhas de apoio


def build_torre(x_c=-1.6, y_solo=-3.8, y_topo=4.2, w_base=1.1, w_topo=0.45):
    """Torre estilizada, esguia, simétrica e estruturalmente limpa."""
    corpo = Polygon(
        [x_c - w_base / 2, y_solo, 0],
        [x_c + w_base / 2, y_solo, 0],
        [x_c + w_topo / 2, y_topo, 0],
        [x_c - w_topo / 2, y_topo, 0],
        color=WHITE_COLOR, stroke_width=0, fill_color="#0A1124", fill_opacity=0.75
    )
    m_esq = Line([x_c - w_base / 2, y_solo, 0], [x_c - w_topo / 2, y_topo, 0], color=WHITE_COLOR, stroke_width=2.4)
    m_dir = Line([x_c + w_base / 2, y_solo, 0], [x_c + w_topo / 2, y_topo, 0], color=WHITE_COLOR, stroke_width=2.4)

    # Plataforma de lançamento horizontal com cantilever
    x_soltura = x_c + w_topo / 2 + 0.35  # ~ -1.025
    plat = Line([x_c - w_topo / 2 - 0.15, y_topo, 0], [x_soltura + 0.18, y_topo, 0], color=WHITE_COLOR, stroke_width=3.2)
    topo_cap = Line([x_c - w_topo / 2, y_topo + 0.08, 0], [x_soltura + 0.18, y_topo + 0.08, 0], color=CYAN_COLOR, stroke_width=1.5, stroke_opacity=0.6)

    # Sapatas de assentamento na base
    base_esq = Line([x_c - w_base / 2 - 0.15, y_solo, 0], [x_c - w_base / 2 + 0.15, y_solo, 0], color=WHITE_COLOR, stroke_width=3.0)
    base_dir = Line([x_c + w_base / 2 - 0.15, y_solo, 0], [x_c + w_base / 2 + 0.15, y_solo, 0], color=WHITE_COLOR, stroke_width=3.0)

    # Treliças em X regulares
    trelicas = VGroup()
    n_andares = 6
    for i in range(n_andares):
        y1 = y_solo + i * (y_topo - y_solo) / n_andares
        y2 = y_solo + (i + 1) * (y_topo - y_solo) / n_andares
        xa1 = x_c - np.interp(y1, [y_solo, y_topo], [w_base / 2, w_topo / 2])
        xa2 = x_c + np.interp(y1, [y_solo, y_topo], [w_base / 2, w_topo / 2])
        xb1 = x_c - np.interp(y2, [y_solo, y_topo], [w_base / 2, w_topo / 2])
        xb2 = x_c + np.interp(y2, [y_solo, y_topo], [w_base / 2, w_topo / 2])
        trelicas.add(Line([xa1, y1, 0], [xb2, y2, 0], color=WHITE_COLOR, stroke_width=1.1, stroke_opacity=0.30))
        trelicas.add(Line([xa2, y1, 0], [xb1, y2, 0], color=WHITE_COLOR, stroke_width=1.1, stroke_opacity=0.30))
        trelicas.add(Line([xb1, y2, 0], [xb2, y2, 0], color=WHITE_COLOR, stroke_width=1.2, stroke_opacity=0.35))

    torre_grupo = VGroup(corpo, m_esq, m_dir, trelicas, base_esq, base_dir, plat, topo_cap)
    return torre_grupo, x_soltura


def symbol_into_screen(center, radius=0.18, color=VIOLET_COLOR):
    """Símbolo vetorial entrando no plano (Norte / +y)."""
    c = Circle(radius=radius, color=color, stroke_width=2.4)
    d = radius * 0.70
    l1 = Line([-d, -d, 0], [d, d, 0], color=color, stroke_width=2.0)
    l2 = Line([-d, d, 0], [d, -d, 0], color=color, stroke_width=2.0)
    return VGroup(c, l1, l2).move_to(center)


def glowing_ball(point, radius=0.11, color=WHITE_COLOR, glow_color=CYAN_COLOR):
    """Bola estilizada apoiada com brilho volumétrico suave."""
    glow2 = Circle(radius=radius * 2.2, stroke_width=0, fill_color=glow_color, fill_opacity=0.12)
    glow1 = Circle(radius=radius * 1.5, stroke_width=1.5, stroke_color=glow_color, fill_color=glow_color, fill_opacity=0.22)
    core = Dot(radius=radius, color=color)
    return VGroup(glow2, glow1, core).move_to(point)


