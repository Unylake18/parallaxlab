"""Gera as 6 propostas de capa do vid_0013 (DA EQUAÇÃO AO FENÔMENO · EP. 04).

Uso, na raiz do repositório:
    uv run python videos/vid_0013_potencial_poco_duplo/gerar_capa.py [PASTA_SAIDA [NUMERO]]

Reaproveita o compositor das capas do vid_0009 (layout aprovado: símbolo, título em duas linhas, divisor, linha de
série, painel neon, marca e horizonte), como o vid_0012. Só mudam o título, a série e o desenho do painel.
Paleta da cena: ciano = força, violeta = potencial U(x), magenta = barreira U_b, azul = níveis de energia.
A partícula fica sempre no eixo x (nunca "rolando" sobre a curva: U não é uma altura espacial).
"""
import importlib.util
import os
import sys
from pathlib import Path

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UP, Arrow, CurvedArrow, DashedLine, Dot, Line, MathTex, Text, VGroup, VMobject,
)

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
_spec = importlib.util.spec_from_file_location("capa9", ROOT / "videos" / "vid_0009_campo_solenoide" / "gerar_capa.py")
g9 = importlib.util.module_from_spec(_spec)
sys.modules["capa9"] = g9
_spec.loader.exec_module(g9)
g9.SERIE = "DA EQUAÇÃO AO FENÔMENO · EP. 04"

CYAN, WHITE, BLUE, MAGENTA = g9.CYAN, g9.WHITE, g9.BLUE, g9.MAGENTA
VIOLET_L, BLUE_L, ENERGIA = "#9C8CFF", "#7FB2FF", "#4D94FF"
SX, SY, XR = 1.55, 0.95, 1.6          # escala horizontal (por ℓ), vertical (por U_b) e domínio |x| ≤ 1,6 ℓ
PY = -0.75                            # eixo espacial abaixo do gráfico


def u(x):
    """U/U_b em função de x/ℓ (a mesma curva da cena)."""
    return (x * x - 1.0) ** 2


def p(x, uu):
    return np.array([SX * x, SY * uu, 0.0])


# ── Peças ───────────────────────────────────────────────────────────────────
def neon(mob, color, w=10):
    """Traço com brilho: duas cópias largas e translúcidas por baixo do traço."""
    a = mob.copy().set_stroke(color, w * 2.8, 0.22)
    b = mob.copy().set_stroke(color, w * 1.7, 0.32)
    mob.set_stroke(color, w, 1.0)
    return VGroup(a, b, mob)


def tx(s, size=100, color=WHITE):
    return MathTex(s, font_size=size, color=color)


def curva_u(w=10):
    c = VMobject().set_points_smoothly([p(x, u(x)) for x in np.linspace(-XR, XR, 140)])
    return neon(c, VIOLET_L, w)


def poco(niveis=(), barreira=True, pontos=True, w=10):
    """Gráfico de U(x): base, curva, barreira U_b tracejada e níveis de energia (linhas azuis com brilho)."""
    g = VGroup(Line(p(-XR - 0.1, 0), p(XR + 0.1, 0)).set_stroke(WHITE, 4, 0.35))
    for E in niveis:
        g.add(neon(Line(p(-1.75, E), p(1.75, E)), ENERGIA, 6))
    if barreira:
        g.add(DashedLine(p(-XR - 0.1, 1), p(0, 1), dash_length=0.12).set_stroke(MAGENTA, 5, 0.85))
    g.add(curva_u(w))
    if pontos:
        g.add(Dot(p(0, 1), 0.13, color=MAGENTA), Dot(p(-1, 0), 0.12, color=VIOLET_L), Dot(p(1, 0), 0.12, color=VIOLET_L))
    return g


def eixo(regioes=(), particula=None, marcas=True):
    """Eixo espacial x abaixo do gráfico, com regiões permitidas (azul) e a partícula (branca, com halo)."""
    g = VGroup(Arrow([SX * -XR - 0.1, PY, 0], [SX * XR + 0.35, PY, 0], buff=0, stroke_width=5, tip_length=0.2,
                     color=WHITE).set_opacity(0.7))
    if marcas:
        for x in (-1, 0, 1):
            g.add(Line([SX * x, PY - 0.09, 0], [SX * x, PY + 0.09, 0]).set_stroke(MAGENTA if x == 0 else VIOLET_L, 5))
    for a, b in regioes:
        g.add(neon(Line([SX * a, PY, 0], [SX * b, PY, 0]), ENERGIA, 9))
    if particula is not None:
        g.add(Dot([SX * particula, PY, 0], 0.25, color=WHITE).set_opacity(0.2),
              Dot([SX * particula, PY, 0], 0.12, color=WHITE))
    return g


def projecoes(E, xs):
    return VGroup(*(DashedLine(p(x, E), [SX * x, PY + 0.08, 0], dash_length=0.07).set_stroke(BLUE_L, 3, 0.55)
                    for x in xs))


def f_expr(size=90):
    f = tx(r"F(x)=F_0\left[\frac{x}{\ell}-\left(\frac{x}{\ell}\right)^3\right]", size)
    f[0][0:4].set_color(CYAN)
    return f


def u_expr(size=90):
    f = tx(r"U(x)=\frac{F_0\ell}{4}\left[\left(\frac{x}{\ell}\right)^2-1\right]^2", size)
    f[0][0:4].set_color(VIOLET_L)
    return f


def ule(size=120):
    f = tx(r"U(x)\le E", size)
    f[0][0:4].set_color(VIOLET_L)
    f[0][5].set_color(BLUE_L)
    return f


def nivel_lab(s, size=62):
    """Rótulos 0<E<U_b, E=U_b, E>U_b: E em azul, U_b em magenta (um glifo por caractere, sem o "_")."""
    f = tx(s, size)
    for g, ch in zip(f[0], [c for c in s if c != "_"]):
        if ch == "E":
            g.set_color(BLUE_L)
        elif ch in "Ub":
            g.set_color(MAGENTA)
    return f


def seta_branca(w=1.0):
    return Arrow([0, 0, 0], [w, 0, 0], buff=0, stroke_width=11, tip_length=0.3, color=WHITE,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=60)


# ── Painéis ─────────────────────────────────────────────────────────────────
def painel_1():
    """Poço com um nível abaixo da barreira; no eixo, a partícula de um lado e a pergunta: chega ao outro lado?"""
    E = 0.5
    a, b = np.sqrt(1 - np.sqrt(E)), np.sqrt(1 + np.sqrt(E))
    g = VGroup(poco((E,)), eixo([(-b, -a), (a, b)], particula=1.15))
    salto = CurvedArrow([SX * 1.0, PY - 0.25, 0], [SX * -1.0, PY - 0.25, 0], angle=-np.pi * 0.45, color=WHITE,
                        stroke_width=7, tip_length=0.26)
    q = Text("?", font="Arial", weight="BOLD", color=WHITE).scale(1.1).next_to(salto, DOWN, buff=0.08)
    return VGroup(g, salto, q)


def painel_2():
    """Os três níveis de energia sobre o mesmo poço, identificados à direita (níveis mais espaçados)."""
    global SY
    sy0, SY = SY, 1.55
    try:
        niveis = ((0.5, r"0<E<U_b"), (1.0, r"E=U_b"), (1.5, r"E>U_b"))
        g = poco(tuple(E for E, _ in niveis))
        labs = VGroup(*(nivel_lab(s_, 58).next_to(p(1.75, E), RIGHT, buff=0.3) for E, s_ in niveis))
        labs.align_to(labs[0], LEFT)
        return VGroup(g, labs).center()          # o compositor escala sem recentrar
    finally:
        SY = sy0


def painel_3():
    """Da força ao potencial: F(x) (ciano) → U(x) (violeta)."""
    fx = VMobject().set_points_smoothly([[1.25 * x, 1.1 * (x - x ** 3), 0] for x in np.linspace(-1.45, 1.45, 100)])
    fg = VGroup(Line([-2.0, 0, 0], [2.0, 0, 0]).set_stroke(WHITE, 4, 0.35), neon(fx, CYAN, 10))
    fl = tx(r"F(x)", 90, CYAN).next_to(fg, DOWN, buff=0.35)
    ug = poco(pontos=True, barreira=False).scale(0.82)
    ul = tx(r"U(x)", 90, VIOLET_L).next_to(ug, DOWN, buff=0.35)
    seta = tx(r"\xrightarrow{\ U=-\int F\,dx\ }", 80)
    return VGroup(VGroup(fg, fl), seta, VGroup(ug, ul)).arrange(RIGHT, buff=0.5)


def painel_4():
    """O poço duplo com mínimos e barreira, e a forma final de U(x)."""
    g = poco()
    ub = tx(r"U_b", 70, MAGENTA).next_to(p(-XR - 0.1, 1), LEFT, buff=0.15)
    return VGroup(VGroup(g, ub), u_expr(78)).arrange(RIGHT, buff=0.7)


def painel_5():
    """Onde a partícula pode ir: nível E, interseções, regiões permitidas no eixo, e U(x) ≤ E."""
    E = 0.5
    a, b = np.sqrt(1 - np.sqrt(E)), np.sqrt(1 + np.sqrt(E))
    xs = (-b, -a, a, b)
    g = VGroup(poco((E,)), projecoes(E, xs), eixo([(-b, -a), (a, b)], particula=1.2),
               *(Dot(p(x, E), 0.1, color=BLUE_L) for x in xs))
    return VGroup(g, ule(130)).arrange(RIGHT, buff=0.9)


def painel_6():
    """Acima da barreira: a partícula atravessa o centro, mas retorna nos extremos."""
    E = 1.5
    b = np.sqrt(1 + np.sqrt(E))
    g = VGroup(poco((E,)), projecoes(E, (-b, b)), eixo([(-b, b)], particula=-0.35),
               Dot(p(-b, E), 0.1, color=BLUE_L), Dot(p(b, E), 0.1, color=BLUE_L))
    ida = Arrow([SX * -0.15, PY - 0.42, 0], [SX * 0.9, PY - 0.42, 0], buff=0, stroke_width=7, tip_length=0.22,
                color=WHITE, max_tip_length_to_length_ratio=0.4)
    g.add(ida)
    lab = nivel_lab(r"E>U_b", 110)
    return VGroup(g, lab).arrange(RIGHT, buff=0.9)


PAINEIS = {1: painel_1, 2: painel_2, 3: painel_3, 4: painel_4, 5: painel_5, 6: painel_6}
TITULOS = {
    1: ("FICA PRESA DE UM LADO", "OU ATRAVESSA?"),
    2: ("A ENERGIA DECIDE", "A TRAVESSIA"),
    3: ("DA FORÇA AO", "POTENCIAL"),
    4: ("POTENCIAL DE", "POÇO DUPLO"),
    5: ("ONDE A PARTÍCULA", "PODE IR?"),
    6: ("ATRAVESSA O CENTRO,", "MAS NÃO ESCAPA"),
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
