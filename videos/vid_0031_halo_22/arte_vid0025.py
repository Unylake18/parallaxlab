"""Arte do vid_0025 (Por que o arco-íris tem 42°), copiada sem alterações de videos/vid_0025_arco_iris/cena.py
(main, commit 84de462f; ~l. 35–40 e 141–146 as constantes, ~l. 276–335 as funções). Copiado, não importado
(regra do AGENTS.md: não depender de outra unidade). Ajustes permitidos pelo handoff v4 §B.2 ficam em funções à parte,
no fim do arquivo: espelhar a pessoa em torno do eixo vertical do pé (recalculando o eye_point).
"""
import numpy as np
from manim import *

from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, TEXT_COLOR

# ----------------------------------------------------------------------------- cores (vid_0025)
INK = TEXT_COLOR            # texto, equações, raio solar
BLUE = "#267BFF"            # gota
DIM = "#8FA3C4"
GEO = "#B8C4DA"        # geometria (b, R, normais, construções)
BLUE_L = "#7FB2FF"
SHIRT = "#5AA2FF"
WARM = "#FFC857"       # Sol (decoração; o espectro do arco-íris também usa amarelo)
SUN_CORE = "#FFD166"


def make_person(foot, H=1.25):
    """Pessoa de perfil, olhando para a direita (de costas para o Sol). O centro da cabeça fica a altura H do pé."""
    fx, fy = float(foot[0]), float(foot[1])
    u = H / 1.25
    P = lambda dx, dy: np.array([fx + dx * u, fy + dy * u, 0.0])
    cap = dict(cap_style=CapStyleType.ROUND)
    head = Circle(radius=0.135 * u, fill_color=INK, fill_opacity=1, stroke_width=0).move_to(P(0, 1.25))
    nose = Polygon(P(0.125, 1.28), P(0.205, 1.235), P(0.125, 1.2), fill_color=INK, fill_opacity=1, stroke_width=0)
    eye = Dot(P(0.065, 1.285), radius=0.022 * u, color=BACKGROUND_COLOR)
    neck = Line(P(0, 1.12), P(0, 1.03), color=INK, stroke_width=6 * u, **cap)
    torso = Polygon(P(-0.15, 1.04), P(0.15, 1.04), P(0.12, 0.60), P(-0.12, 0.60), fill_color=SHIRT, fill_opacity=0.95,
                    stroke_color=SHIRT, stroke_width=3, stroke_opacity=1.0).round_corners(0.05 * u)
    arm_b = Line(P(-0.02, 1.0), P(-0.17, 0.66), color=GEO, stroke_width=6 * u, **cap)
    arm_f = Line(P(0.02, 1.0), P(0.24, 0.72), color=INK, stroke_width=6 * u, **cap)
    leg_b = Line(P(-0.04, 0.6), P(-0.12, 0.04), color=GEO, stroke_width=7 * u, **cap)
    leg_f = Line(P(0.04, 0.6), P(0.12, 0.04), color=INK, stroke_width=7 * u, **cap)
    foot_b = Line(P(-0.12, 0.03), P(-0.01, 0.03), color=GEO, stroke_width=5 * u, **cap)
    foot_f = Line(P(0.12, 0.03), P(0.23, 0.03), color=INK, stroke_width=5 * u, **cap)
    g = VGroup(arm_b, leg_b, foot_b, torso, leg_f, foot_f, arm_f, neck, head, nose, eye)
    g.eye_point = P(0, 1.25)
    return g


def make_sun(c, r=0.3):
    c = np.array([c[0], c[1], 0.0])
    halo = VGroup(*[Circle(radius=r * k, stroke_width=0, fill_color=WARM, fill_opacity=o).move_to(c)
                    for k, o in ((3.1, 0.04), (2.4, 0.07), (1.8, 0.12), (1.4, 0.2))])
    rays = VGroup(*[Line(c + r * 1.55 * np.array([np.cos(q), np.sin(q), 0]), c + r * (2.15 if k % 2 == 0 else 1.9) * np.array([np.cos(q), np.sin(q), 0]),
                         color=WARM, stroke_width=3.2, cap_style=CapStyleType.ROUND)
                    for k, q in enumerate(np.linspace(0, TAU, 12, endpoint=False))])
    core = Circle(radius=r, stroke_width=0, fill_color=SUN_CORE, fill_opacity=1).move_to(c)
    g = VGroup(halo, rays, core)
    g.audit_skip = True
    return g


def make_drop(c, size=0.1, color=BLUE_L, opacity=0.8):
    """Gota de chuva (formato de lágrima)."""
    c = np.array([c[0], c[1], 0.0])
    r = size
    body = Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=opacity).move_to(c)
    apex = c + np.array([0, 2.3 * r, 0])
    a1, a2 = np.radians(28), np.radians(152)
    tip = Polygon(c + r * np.array([np.cos(a1), np.sin(a1), 0]), apex, c + r * np.array([np.cos(a2), np.sin(a2), 0]),
                  stroke_width=0, fill_color=color, fill_opacity=opacity)
    g = VGroup(body, tip)
    g.audit_skip = True
    return g


def make_ground(y_top, depth=1.6, color=BLUE, bands=7, op=0.09, width=9.4):
    """Chão em degradê (faixas)."""
    g = VGroup()
    for k in range(bands):
        h = depth / bands
        g.add(Rectangle(width=width, height=h, stroke_width=0, fill_color=color, fill_opacity=op * (1 - k / bands))
              .move_to([0, y_top - h * (k + 0.5), 0]))
    g.audit_skip = True
    return g


# ----------------------------------------------------------------------------- ajustes do vid_0031 (§B.2)
def make_person_espelhada(foot, H=1.25):
    """make_person espelhada em torno do eixo vertical que passa pelo pé (olha para a esquerda); eye_point recalculado."""
    g = make_person(foot, H)
    eye = np.array(g.eye_point, float)
    g.flip(UP, about_point=np.array([float(foot[0]), float(foot[1]), 0.0]))
    g.eye_point = np.array([2 * float(foot[0]) - eye[0], eye[1], 0.0])
    return g


def raio_sol(a, b, principal=False):
    """Raio de sol no estilo do vid_0025 (~l. 765): WARM, 2,4–3,0 de traço, opacidade 0,85–0,9."""
    if principal:
        return Line(a, b, color=WARM, stroke_width=3.0, stroke_opacity=0.9)
    return Arrow(a, b, color=WARM, stroke_width=2.4, buff=0, max_tip_length_to_length_ratio=0.12, stroke_opacity=0.85)
