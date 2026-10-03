"""Gera as 6 propostas de capa do vid_0011 (POR TRÁS DA FÓRMULA · EP. 04).

Uso, na raiz do repositório:
    uv run python videos/vid_0011_adiabatica_pv_gama/gerar_capa.py [PASTA_SAIDA [NUMERO]]

Reaproveita o compositor das capas do vid_0009 (mesma base versionada, mesmo layout: símbolo, título em
duas linhas, divisor, linha de série, painel neon, marca e horizonte). Só mudam o título, a série e o
desenho do painel (Manim, paleta da cena: ciano = energia interna/adiabática, violeta = trabalho,
magenta = calor/isotérmica, azul = geometria).
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UP, Arrow, DashedLine, Dot, Line, MathTex, ParametricFunction, Polygon, Rectangle,
    SurroundingRectangle, VGroup, VMobject,
)

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
_spec = importlib.util.spec_from_file_location("capa9", ROOT / "videos" / "vid_0009_campo_solenoide" / "gerar_capa.py")
g9 = importlib.util.module_from_spec(_spec)
sys.modules["capa9"] = g9
_spec.loader.exec_module(g9)
g9.SERIE = "POR TRÁS DA FÓRMULA · EP. 04"

CYAN, WHITE, BLUE, VIOLET, MAGENTA = g9.CYAN, g9.WHITE, g9.BLUE, g9.VIOLET, g9.MAGENTA
VIOLET_L, BLUE_L = "#9C8CFF", "#7FB2FF"


# ── Peças ───────────────────────────────────────────────────────────────────
def neon(mob, color, w=10):
    """Traço com brilho: duas cópias largas e translúcidas por baixo do traço."""
    a = mob.copy().set_stroke(color, w * 2.8, 0.22)
    b = mob.copy().set_stroke(color, w * 1.7, 0.32)
    mob.set_stroke(color, w, 1.0)
    return VGroup(a, b, mob)


def tx(s, size=120, color=WHITE):
    return MathTex(s, font_size=size, color=color)


def cilindro(vol=1.0, gas=CYAN, pesos=0, pesos_fora=0, termo=None, w=2.6, h=2.1):
    """Cilindro largo (cabe no painel 2,8:1). vol regula a altura do pistão; termo em [0, 1] desenha termômetro."""
    walls = VMobject().set_points_as_corners([[-w / 2, h, 0], [-w / 2, 0, 0], [w / 2, 0, 0], [w / 2, h, 0]])
    yp = 0.55 * h * vol
    gás = Rectangle(width=w - 0.1, height=yp, stroke_width=0, fill_color=gas, fill_opacity=0.42).move_to([0, yp / 2, 0])
    pistao = Rectangle(width=w - 0.06, height=0.2, stroke_width=0, fill_color=WHITE, fill_opacity=0.95).move_to([0, yp + 0.1, 0])
    g = VGroup(gás, pistao)
    for i in range(pesos):
        g.add(Rectangle(width=1.3, height=0.2, stroke_width=0, fill_color="#B9C6EA", fill_opacity=0.95)
              .move_to([0, yp + 0.3 + 0.23 * i, 0]))
    for i in range(pesos_fora):                       # pesos já retirados, numa prateleira à direita
        g.add(Rectangle(width=1.0, height=0.2, stroke_width=0, fill_color="#B9C6EA", fill_opacity=0.95)
              .move_to([w / 2 + 0.85, h + 0.12 + 0.23 * i, 0]))
    if pesos_fora:
        g.add(Line([w / 2 + 0.3, h, 0], [w / 2 + 1.4, h, 0]).set_stroke(BLUE_L, 7))
    g.add(neon(walls, BLUE, 13))
    if termo is not None:
        x0 = -w / 2 - 0.6
        g.add(Rectangle(width=0.24, height=h, stroke_width=6, stroke_color=WHITE, fill_opacity=0).move_to([x0, h / 2, 0]))
        g.add(Rectangle(width=0.24, height=h * termo, stroke_width=0, fill_color=gas, fill_opacity=0.95)
              .move_to([x0, h * termo / 2, 0]))
    return g


def seta(p0, p1, color=WHITE, w=12, tip=0.3):
    return Arrow(p0, p1, buff=0, stroke_width=w, tip_length=tip, color=color)


# ── Painéis ─────────────────────────────────────────────────────────────────
def painel_formula():
    f = tx(r"PV^{\gamma}=\text{cte}", 150)
    f[0][2].set_color(CYAN)
    anel = neon(SurroundingRectangle(f[0][2], color=CYAN, buff=0.14, corner_radius=0.12), CYAN, 8)
    return VGroup(f, anel)


def painel_pesos():
    c = cilindro(vol=1.0, gas=BLUE_L, pesos=2, pesos_fora=3)
    c.add(seta([0, 1.55, 0], [0, 2.35, 0], CYAN, 13))                                 # pistão sobe
    q = tx(r"\delta Q=0", 160, MAGENTA)
    return VGroup(c, q).arrange(RIGHT, buff=1.0, aligned_edge=DOWN)


def painel_grafico():
    X = lambda x: (x - 0.7) * 3.4
    Y = lambda y: (y - 0.12) * 5.0
    eixos = VGroup(Line([0, 0, 0], [X(2.5), 0, 0]).set_stroke(WHITE, 8), Line([0, 0, 0], [0, Y(1.15), 0]).set_stroke(WHITE, 8))
    iso = ParametricFunction(lambda t: [X(t), Y(1 / t), 0], t_range=[1.0, 2.4], stroke_width=10)
    adi = ParametricFunction(lambda t: [X(t), Y(t ** -1.4), 0], t_range=[1.0, 2.4], stroke_width=10)
    p0 = Dot([X(1), Y(1), 0], radius=0.17, color=WHITE)
    graf = VGroup(eixos, neon(iso, MAGENTA, 9), neon(adi, CYAN, 9), p0)
    legenda = VGroup(tx(r"PV=\text{cte}", 120, MAGENTA), tx(r"PV^{\gamma}=\text{cte}", 120, CYAN)).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
    return VGroup(graf, legenda).arrange(RIGHT, buff=0.9)


def painel_cadeia():
    a = tx(r"dU=-P\,dV", 120, CYAN)
    b = tx(r"PV^{\gamma}=\text{cte}", 160, WHITE)
    caixa = neon(SurroundingRectangle(b, color=CYAN, buff=0.25, corner_radius=0.18), CYAN, 8)
    s1 = seta([0, 0, 0], [0, -0.75, 0], WHITE, 12, 0.3)
    return VGroup(a, s1, VGroup(b, caixa)).arrange(DOWN, buff=0.3)


def painel_esfria():
    quente = cilindro(vol=0.55, gas=MAGENTA, termo=0.92, w=2.0, h=2.3)
    frio = cilindro(vol=1.5, gas=BLUE_L, termo=0.30, w=2.0, h=2.3)
    mid = VGroup(seta([0, 0, 0], [1.5, 0, 0], WHITE, 13, 0.34), tx(r"\delta Q=0", 100, MAGENTA)).arrange(DOWN, buff=0.2)
    return VGroup(quente, mid, frio).arrange(RIGHT, buff=0.6, aligned_edge=DOWN)


def painel_energia():
    """Sem calor: a energia que sai de U vira trabalho (barras antes/depois)."""
    def barra(x0, w, cor):
        return neon(Rectangle(width=w, height=0.55, stroke_width=0, fill_color=cor, fill_opacity=0.55), cor, 6).move_to([x0 + w / 2, 0, 0])
    antes = VGroup(barra(0, 4.4, CYAN))
    depois = VGroup(barra(0, 2.7, CYAN), barra(2.7, 1.7, VIOLET_L))
    ru = tx("U", 100, CYAN).next_to(antes, LEFT, buff=0.35)
    seta_ = seta([0, 0, 0], [0, -0.8, 0], WHITE, 12, 0.3)
    lw = tx("W", 100, VIOLET_L).next_to(depois, RIGHT, buff=0.35)
    colunas = VGroup(antes, seta_, depois).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
    ru.next_to(colunas, LEFT, buff=0.4).align_to(antes, UP).shift(DOWN * 0.0)
    lw.move_to(depois.get_right() + [0.7, 0, 0])
    q = tx(r"\delta Q=0", 130, MAGENTA)
    desenho = VGroup(ru, colunas, lw)
    return VGroup(desenho, q).arrange(RIGHT, buff=0.9)


PAINEIS = {1: painel_formula, 2: painel_pesos, 3: painel_grafico, 4: painel_cadeia, 5: painel_esfria, 6: painel_energia}
TITULOS = {
    1: ("DE ONDE VEM", "PV ELEVADO A GAMA?"),
    2: ("O GÁS SE EXPANDE", "SEM RECEBER CALOR"),
    3: ("ADIABÁTICA", "OU ISOTÉRMICA?"),
    4: ("A FÓRMULA NÃO", "É O COMEÇO"),
    5: ("POR QUE O GÁS", "ESFRIA AO EXPANDIR?"),
    6: ("SEM CALOR,", "DE ONDE VEM A ENERGIA?"),
}


def linhas(n):
    a, b = TITULOS[n]
    start = min(g9.fit(t, g9.BOLD, 870, 150).size for t in (a, b))     # as duas linhas no mesmo corpo
    return [([(a, "white")], start), ([(b, "grad")], start)]


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else UNIT / "capas"
    out.mkdir(parents=True, exist_ok=True)
    so = int(sys.argv[2]) if len(sys.argv) > 2 else None
    for n, build in PAINEIS.items():
        if so and n != so:
            continue
        alvo = out / f"capa_{n:02d}.png"
        g9.cover(linhas(n), g9.render_rgba(build, 400)).save(alvo, optimize=True)
        print(alvo)
