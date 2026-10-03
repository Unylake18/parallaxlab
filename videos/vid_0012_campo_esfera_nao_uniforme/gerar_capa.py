"""Gera as 6 propostas de capa do vid_0012 (EXERCÍCIO RESOLVIDO · EP. 05).

Uso, na raiz do repositório:
    uv run python videos/vid_0012_campo_esfera_nao_uniforme/gerar_capa.py [PASTA_SAIDA [NUMERO]]

Reaproveita o compositor das capas do vid_0009 (mesmo layout aprovado: símbolo, título em duas linhas,
divisor, linha de série, painel neon, marca e horizonte). Só mudam o título, a série e o desenho do painel.
Todo painel traz a esfera com densidade decrescente (miolo denso, borda tênue), a gaussiana tracejada, os
vetores E⃗ sobre ela (comprimento ∝ E(r) da cena) e a expressão ρ(r) = ρ0(1 − r/R).
Paleta da cena: ciano = campo E, magenta = densidade, violeta = gaussiana/r, azul = geometria.
"""
import importlib.util
import os
import sys
from pathlib import Path

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UP, Arc, Arrow, Circle, Dot, Ellipse, Line, ManimColor, MathTex, VGroup,
    interpolate_color,
)

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
_spec = importlib.util.spec_from_file_location("capa9", ROOT / "videos" / "vid_0009_campo_solenoide" / "gerar_capa.py")
g9 = importlib.util.module_from_spec(_spec)
sys.modules["capa9"] = g9
_spec.loader.exec_module(g9)
g9.SERIE = "EXERCÍCIO RESOLVIDO · EP. 05"

CYAN, WHITE, BLUE, VIOLET, MAGENTA = g9.CYAN, g9.WHITE, g9.BLUE, g9.VIOLET, g9.MAGENTA
VIOLET_L, BLUE_L = "#9C8CFF", "#7FB2FF"
GAUSS = "#D4CBFF"                                 # gaussiana: violeta bem claro, para não sumir sobre o miolo rosa
E_PICO = 1 / 9                                    # E(2R/3) em unidades de ρ0R/ε0


def E(x):
    """Campo (unidades de ρ0R/ε0) em x = r/R, igual ao da cena."""
    return x / 3 - x * x / 4 if x <= 1 else 1 / (12 * x * x)


# ── Peças ───────────────────────────────────────────────────────────────────
def neon(mob, color, w=10):
    """Traço com brilho: duas cópias largas e translúcidas por baixo do traço."""
    a = mob.copy().set_stroke(color, w * 2.8, 0.22)
    b = mob.copy().set_stroke(color, w * 1.7, 0.32)
    mob.set_stroke(color, w, 1.0)
    return VGroup(a, b, mob)


def tx(s, size=120, color=WHITE):
    return MathTex(s, font_size=size, color=color)


def tracejado(raio_, w=9, cor=GAUSS, n=18):
    """Círculo tracejado (arcos de 58% do passo)."""
    return VGroup(*(Arc(radius=raio_, start_angle=a, angle=0.58 * 2 * np.pi / n).set_stroke(cor, w)
                    for a in np.linspace(0, 2 * np.pi, n, endpoint=False)))


def esfera(R=1.4, aneis=24):
    """Esfera isolante com ρ(r) = ρ0(1 − r/R): miolo denso e brilhante, borda quase vazia, equador em perspectiva."""
    g = VGroup()
    for i in range(aneis):
        t = (i + 1) / aneis                                       # 1 = borda, 0 = centro
        c = Circle(radius=R * (1 - i / aneis)).set_stroke(width=0)
        c.set_fill(interpolate_color(ManimColor("#FFC2FF"), ManimColor(MAGENTA), min(1.0, t * 1.6)), 0.14)
        g.add(c)
    g.add(Arc(radius=1, start_angle=np.pi, angle=np.pi).stretch(R, 0).stretch(0.26 * R, 1).set_stroke(BLUE_L, 4, 0.55))
    g.add(neon(Circle(radius=R), BLUE_L, 8))
    return g


def gaussiana(r, w=9):
    """Superfície gaussiana de raio r: círculo tracejado + equador tracejado (metade da frente)."""
    g = VGroup(tracejado(r, w))
    for a in np.linspace(np.pi, 2 * np.pi, 7)[:-1]:
        g.add(Arc(radius=1, start_angle=a, angle=0.58 * np.pi / 6).stretch(r, 0).stretch(0.26 * r, 1)
              .set_stroke(GAUSS, w * 0.6, 0.9))
    return g


def vetores(r, comp, n=8, w=9, fase=np.pi / 8):
    """E⃗ radiais sobre a gaussiana de raio r, todos do mesmo comprimento (|E| constante nela)."""
    g = VGroup()
    for a in np.linspace(0, 2 * np.pi, n, endpoint=False) + fase:
        d = np.array([np.cos(a), np.sin(a), 0.0])
        g.add(Arrow(r * d, (r + comp) * d, buff=0, stroke_width=w, tip_length=0.2, color=CYAN,
                    max_tip_length_to_length_ratio=0.6, max_stroke_width_to_length_ratio=60))
    return g


def raio_marcado(r, nome, ang=0.0, size=110):
    """Raio do centro até a gaussiana, com ponto e rótulo (acima do raio, em branco para ler sobre o miolo)."""
    p = r * np.array([np.cos(ang), np.sin(ang), 0.0])
    lab = tx(nome, size, WHITE).move_to(p * 0.5 + np.array([0.0, 0.34, 0.0]))
    return VGroup(Line([0, 0, 0], p).set_stroke(WHITE, 6), Dot(p, 0.12, color=WHITE), Dot([0, 0, 0], 0.08, color=WHITE), lab)


def esfera_gauss(R=1.4, gauss=(2 / 3,), raio_nome=None, escala_vetor=0.4):
    """Esfera de densidade variável com gaussiana(s) e E⃗. Comprimento de E⃗ ∝ E(x), como no gráfico da cena."""
    g = VGroup(esfera(R))
    for x in gauss:
        g.add(gaussiana(R * x))
        g.add(vetores(R * x, escala_vetor * R * E(x) / E_PICO))
    if raio_nome:
        g.add(raio_marcado(R * gauss[0], raio_nome))
    return g


def rho_expr(size=100):
    """ρ(r) = ρ0 (1 − r/R) com a densidade em magenta."""
    f = tx(r"\rho(r)=\rho_0\left(1-\frac{r}{R}\right)", size, WHITE)
    f[0][0].set_color(MAGENTA)          # ρ(r)
    f[0][5:7].set_color(MAGENTA)        # ρ0
    return f


def pergunta_e(size=105, txt=r"\vec{E}(r)=\,?"):
    t = tx(txt, size, WHITE)
    t[0][0:2].set_color(CYAN)
    return t


def seta_baixo(h=0.55):
    return Arrow([0, 0, 0], [0, -h, 0], buff=0, stroke_width=11, tip_length=0.26, color=WHITE,
                 max_tip_length_to_length_ratio=0.6, max_stroke_width_to_length_ratio=60)


# ── Painéis ─────────────────────────────────────────────────────────────────
def painel_1():
    """Esfera + gaussiana + E⃗ à esquerda; a expressão de ρ(r) grande à direita."""
    return VGroup(esfera_gauss(1.55), rho_expr(105)).arrange(RIGHT, buff=0.7)


def painel_2():
    """Espelhado: o enunciado (ρ(r) válido para r ≤ R) à esquerda e a esfera à direita."""
    f = tx(r"\rho(r)=\rho_0\left(1-\frac{r}{R}\right),\ r\le R", 82, WHITE)
    f[0][0].set_color(MAGENTA)
    f[0][5:7].set_color(MAGENTA)
    return VGroup(f, esfera_gauss(1.55)).arrange(RIGHT, buff=0.6)


def painel_3():
    """Esfera com o raio r da gaussiana marcado; à direita ρ(r) e a pergunta sobre E⃗(r)."""
    dir_ = VGroup(rho_expr(92), seta_baixo(), pergunta_e(100)).arrange(DOWN, buff=0.22)
    return VGroup(esfera_gauss(1.5, raio_nome="r"), dir_).arrange(RIGHT, buff=0.6)


def painel_4():
    """Duas gaussianas: dentro da esfera (E cresce) e fora (E cai), com ρ(r) ao lado."""
    s = esfera_gauss(1.2, gauss=(0.55, 1.45), escala_vetor=0.4)
    return VGroup(s, rho_expr(100)).arrange(RIGHT, buff=0.6)


def painel_5():
    """Três gaussianas (1/3, 2/3 e 1,25 de R): E⃗ cresce até 2R/3 e cai; ρ(r) e r_max = ? à direita."""
    s = esfera_gauss(1.25, gauss=(0.33, 0.67, 1.25), escala_vetor=0.5)
    t = tx(r"r_{\max}=\,?", 100, VIOLET_L)
    dir_ = VGroup(rho_expr(92), seta_baixo(), t).arrange(DOWN, buff=0.22)
    return VGroup(s, dir_).arrange(RIGHT, buff=0.55)


def painel_6():
    """Esfera e, à direita, a lei de Gauss ∮E⃗·dA⃗ = Q_enc/ε0 sobre a expressão de ρ(r)."""
    gauss = tx(r"\oint \vec{E}\cdot d\vec{A}=\frac{Q_{\mathrm{enc}}}{\varepsilon_0}", 82, WHITE)
    gauss[0][1].set_color(CYAN)
    gauss[0][2].set_color(CYAN)
    dir_ = VGroup(gauss, rho_expr(82)).arrange(DOWN, buff=0.6)
    return VGroup(esfera_gauss(1.55), dir_).arrange(RIGHT, buff=0.55)


PAINEIS = {1: painel_1, 2: painel_2, 3: painel_3, 4: painel_4, 5: painel_5, 6: painel_6}
TITULOS = {
    1: ("O CAMPO MÁXIMO", "ESTÁ NA SUPERFÍCIE?"),
    2: ("E SE A CARGA", "NÃO FOR UNIFORME?"),
    3: ("ONDE O CAMPO", "É MÁXIMO?"),
    4: ("DENTRO OU FORA,", "ONDE O CAMPO É MAIOR?"),
    5: ("O PICO DO CAMPO", "ESTÁ ONDE?"),
    6: ("LEI DE GAUSS COM", "DENSIDADE DE CARGA VARIÁVEL"),
}


def linhas(n):
    a, b = TITULOS[n]
    start = min(g9.fit(t, g9.BOLD, 870, 150).size for t in (a, b))     # as duas linhas no mesmo corpo
    fator = float(os.environ.get("FATOR_L1", "1.5"))
    start_a = round(start * fator) if n == 6 else start                 # capa 6: 1ª linha maior (a 2ª já ocupa a largura)
    return [([(a, "white")], start_a), ([(b, "grad")], start)]


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
