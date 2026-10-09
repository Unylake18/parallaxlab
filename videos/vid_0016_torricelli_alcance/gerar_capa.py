"""Dez propostas de capa do vid_0016 (DA EQUAÇÃO AO FENÔMENO · EP. 05): onde furar o tanque para o jato ir mais longe.

Uso, na raiz do repositório:
    uv run python videos/vid_0016_torricelli_alcance/gerar_capa.py [PASTA_SAIDA [NUMERO]]

Reaproveita o compositor das capas do vid_0009/vid_0014 (logo, título em duas linhas, divisor, linha de série, painel,
marca e horizonte iguais). Só mudam títulos, série e a arte do painel, desenhada para ler em miniatura.
Paleta da cena: ciano = y e t (altura do furo, tempo de voo); violeta = H − y e v (profundidade, velocidade de saída);
magenta = cancelamento e produto; branco = x e H.
Física congelada: v = √(2g(H−y)), t = √(2y/g), x = 2√(y(H−y)); x/H = 2√(u(1−u)) com u = y/H, ou seja,
(2u−1)² + (x/H)² = 1: o gráfico é um semicírculo. Máximo: u = 1/2, x_max = H.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UP, Circle, DashedLine, Dot, Line, MathTex, Rectangle, Polygon, VGroup, VMobject, ImageMobject, Arrow,
)
from PIL import Image

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
_spec = importlib.util.spec_from_file_location("capa14v2", ROOT / "videos" / "vid_0014_momento_inercia_eixos_paralelos" / "gerar_capa_v2.py")
v2 = importlib.util.module_from_spec(_spec)
sys.modules["capa14v2"] = v2
_spec.loader.exec_module(v2)
g9, c1 = v2.g9, v2.c1
g9.SERIE = "DA EQUAÇÃO AO FENÔMENO · EP. 05"
CYAN, WHITE, BLUE, MAGENTA, VIOLET, BLUE_L = c1.CYAN, c1.WHITE, c1.BLUE, c1.MAGENTA, c1.VIOLET, c1.BLUE_L
neon, tx = c1.neon, c1.tx

HH = 2.4          # altura da água (unidades do desenho)
LARG = 1.5        # largura do tanque


# ── Peças ───────────────────────────────────────────────────────────────────
def tanque(larg=LARG):
    paredes = VGroup(Line([-larg, HH * 1.12, 0], [-larg, 0, 0]), Line([-larg, 0, 0], [0, 0, 0]), Line([0, 0, 0], [0, HH * 1.12, 0]))
    agua = Rectangle(width=larg, height=HH).move_to([-larg / 2, HH / 2, 0]).set_fill(BLUE, 0.30).set_stroke(width=0)
    nivel = Line([-larg, HH, 0], [0, HH, 0]).set_stroke(CYAN, 4, 0.9)
    return VGroup(agua, nivel, neon(paredes.set_stroke(BLUE_L, 6), BLUE_L, 6))


def chao(x1=HH + 0.6, x0=-LARG - 0.35):
    return Line([x0, 0, 0], [x1, 0, 0]).set_stroke(WHITE, 3, 0.55)


def xl(u):
    return 2 * HH * np.sqrt(u * (1 - u))


def jato(u, cor, w=8):
    y0, d = u * HH, HH - u * HH
    xs = np.linspace(0, xl(u), 70)
    return neon(VMobject().set_points_as_corners([[x, y0 - x * x / (4 * d), 0] for x in xs]), cor, w)


def furo(u, r=0.075):
    return Dot([0, u * HH, 0], r, color=WHITE)


def pouso(u, cor=WHITE, r=0.12):
    return Circle(radius=r).set_stroke(cor, 6).set_fill("#06081A", 1.0).move_to([xl(u), 0, 0])


# ── Artes ───────────────────────────────────────────────────────────────────
def arte_1():
    """A pergunta: furo baixo (violeta) contra furo do meio (ciano); quem chega mais longe?"""
    g = VGroup(tanque(), chao(), jato(0.12, VIOLET), jato(0.5, CYAN), furo(0.12), furo(0.5), pouso(0.12, VIOLET), pouso(0.5, CYAN))
    q = tx(r"?", 330, MAGENTA).move_to([xl(0.5) + 1.25, 1.0, 0])
    return VGroup(g, q)


def arte_2():
    """O quadrado H × H: o jato do meio aterrissa a uma distância igual à altura da água."""
    sq = VGroup(*[DashedLine(a, b, dash_length=0.12).set_stroke(WHITE, 3.5, 0.75) for a, b in (
        ([0, HH, 0], [HH, HH, 0]), ([HH, HH, 0], [HH, 0, 0]))])
    h = VGroup(Arrow([-LARG - 0.35, 0, 0], [-LARG - 0.35, HH, 0], buff=0, stroke_width=7, tip_length=0.2, color=WHITE),
               tx(r"H", 90, WHITE).move_to([-LARG - 0.75, HH / 2, 0]))
    dx = VGroup(Arrow([0.05, -0.38, 0], [HH, -0.38, 0], buff=0, stroke_width=7, tip_length=0.2, color=WHITE),
                tx(r"x_{\max}=H", 90, WHITE).move_to([HH / 2, -0.95, 0]))
    return VGroup(tanque(), chao(), sq, jato(0.5, CYAN, 10), furo(0.5), pouso(0.5, CYAN), h, dx)


def arte_3():
    """Simetria: furos a 0,2 e 0,8 da altura acertam o mesmo ponto."""
    la = tx(r"0{,}2", 70, CYAN).move_to([-LARG / 2, 0.2 * HH + 0.3, 0])
    lb = tx(r"0{,}8", 70, VIOLET).move_to([-LARG / 2, 0.8 * HH + 0.3, 0])
    anel = Circle(radius=0.26).set_stroke(WHITE, 5, 0.8).move_to([xl(0.2), 0, 0])
    return VGroup(tanque(), chao(), jato(0.2, CYAN), jato(0.8, VIOLET), furo(0.2), furo(0.8), la, lb, anel, pouso(0.2, WHITE))


def arte_4():
    """O gráfico do alcance é um semicírculo: (2u−1)² + (x/H)² = 1, com os eixos na proporção 2 : 1."""
    R = 2.0
    base = Line([0, 0, 0], [2 * R + 0.3, 0, 0]).set_stroke(WHITE, 4, 0.7)
    vert = Line([0, 0, 0], [0, R + 0.35, 0]).set_stroke(WHITE, 4, 0.7)
    th = np.linspace(0, np.pi, 90)
    topo = VMobject().set_points_as_corners([[R - R * np.cos(a), R * np.sin(a), 0] for a in th])
    fantasma = VMobject().set_points_as_corners([[R - R * np.cos(a), -R * np.sin(a), 0] for a in th])
    fantasma = DashedLine([0, 0, 0], [0.001, 0, 0])  # (substituído abaixo)
    pts = [[R - R * np.cos(a), -R * np.sin(a), 0] for a in np.linspace(0, np.pi, 60)]
    fant = VGroup(*[Line(pts[i], pts[i + 1]).set_stroke(CYAN, 4, 0.0 if i % 2 else 0.35) for i in range(len(pts) - 1)])
    guia = DashedLine([R, 0, 0], [R, R, 0], dash_length=0.1).set_stroke(WHITE, 3, 0.8)
    topo_pt = Dot([R, R, 0], 0.13, color=WHITE)
    t1 = tx(r"\tfrac12", 80, WHITE).move_to([R, -0.38, 0])
    t2 = tx(r"1", 80, WHITE).move_to([-0.4, R, 0])
    ex = tx(r"y/H", 76, CYAN).move_to([2 * R + 0.45, -0.35, 0])
    ey = tx(r"x/H", 76, WHITE).move_to([R + 1.0, R + 0.5, 0])
    return VGroup(base, vert, fant, neon(topo, CYAN, 11), guia, topo_pt, t1, t2, ex, ey)


def arte_5():
    """Cabo de guerra: a velocidade de saída (violeta) sobe, o tempo de voo (ciano) cai; o alcance é o produto."""
    bv = Rectangle(width=4.0, height=0.5).set_fill(VIOLET, 0.9).set_stroke(width=0)
    bt = Rectangle(width=1.5, height=0.5).set_fill(CYAN, 0.9).set_stroke(width=0)
    bt.next_to(bv, DOWN, buff=0.7, aligned_edge=LEFT)
    lv = tx(r"v", 100, VIOLET).next_to(bv, LEFT, buff=0.3)
    lt = tx(r"t", 100, CYAN).next_to(bt, LEFT, buff=0.3)
    av = Arrow(bv.get_right() + RIGHT * 0.1, bv.get_right() + RIGHT * 0.9, buff=0, stroke_width=9, tip_length=0.28, color=VIOLET)
    at = Arrow(bt.get_right() + RIGHT * 0.1, bt.get_right() + RIGHT * 0.55, buff=0, stroke_width=9, tip_length=0.28, color=CYAN)
    at.rotate(np.pi, about_point=bt.get_right() + RIGHT * 0.1 + RIGHT * 0.225)
    prod = tx(r"x=v\,t", 120, WHITE)
    prod[0][2].set_color(VIOLET), prod[0][3].set_color(CYAN)
    prod.next_to(VGroup(bv, bt), RIGHT, buff=1.5)
    return VGroup(VGroup(lv, lt, bv, bt, av, at), prod)


def arte_6():
    """Soma fixa: y + (H−y) = H. O retângulo y × (H−y) é o maior quando vira quadrado."""
    W = 2.2
    cores = []
    g = VGroup()
    x = 0.0
    for u, destaque in ((0.15, False), (0.5, True), (0.85, False)):
        w, h = u * W, (1 - u) * W
        r = Rectangle(width=w, height=h).set_fill(MAGENTA, 0.6 if destaque else 0.22)
        r.set_stroke(WHITE if destaque else MAGENTA, 7 if destaque else 3.5, 1.0)
        r.move_to([x + w / 2, h / 2, 0])
        base = Line([x, -0.14, 0], [x + w, -0.14, 0]).set_stroke(CYAN, 9)
        lado = Line([x - 0.14, 0, 0], [x - 0.14, h, 0]).set_stroke(VIOLET, 9)
        g.add(r, base, lado)
        x += w + 0.55
    lbl = tx(r"y\,(H-y)", 110, WHITE)
    lbl[0][0].set_color(CYAN), lbl[0][2:6].set_color(VIOLET)
    lbl.next_to(g, DOWN, buff=0.5)
    return VGroup(g, lbl)


def arte_7():
    """A gravidade sai da conta: cancelamento em magenta, como na cena."""
    f = MathTex(r"x=\sqrt{2\,g\,(H-y)\cdot\frac{2y}{g}}", font_size=120, color=WHITE, substrings_to_isolate=["g"])
    from manim import Cross
    cruzes = VGroup()
    for i, s in enumerate(f.tex_strings):
        if s.strip() == "g":
            f[i].set_color(MAGENTA)
            cruzes.add(Cross(f[i], stroke_color=MAGENTA, stroke_width=9, scale_factor=1.5))
    res = tx(r"x=2\sqrt{y\,(H-y)}", 120, WHITE).next_to(f, DOWN, buff=0.7)
    return VGroup(f, cruzes, res)


def arte_8():
    """O tanque do próprio vídeo (Blender), furo no meio, com a cota do alcance máximo."""
    sys.path.insert(0, str(ROOT / "experimentos" / "blender" / "arsenal"))
    from manim_solido3d import Solido3D
    sol = Solido3D("tanque_torricelli", params={"altura_furo": 1.1, "enquadramento_fixo": 1, "setas": 0, "estilo_jato": 1}, frames=60,
                   res="1296x2304", render="nunca")
    arr = sol.quadro(0)
    a = arr[:, :, 3]
    ys, xs = np.where(a > 12)
    arr = arr[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    img = ImageMobject(arr)
    img.set_height(4.2)
    lab = tx(r"x_{\max}=H", 100, WHITE)
    from manim import Group
    return Group(img, lab).arrange(RIGHT, buff=0.7)


def arte_9():
    """Setas de saída: quanto mais fundo, mais rápido (violeta), mas quem chega mais longe é o furo do meio."""
    g = VGroup(tanque(), chao())
    for u in (0.1, 0.5, 0.75):
        v = 1.9 * np.sqrt(1 - u)
        g.add(Arrow([0.02, u * HH, 0], [0.02 + v, u * HH, 0], buff=0, stroke_width=9, tip_length=0.24, color=VIOLET), furo(u))
        g.add(pouso(u, CYAN if u == 0.5 else WHITE, 0.13))
    return g


def arte_10():
    """Pódio: três furos (embaixo, no meio, em cima) e a ordem de chegada."""
    g = VGroup(tanque(), chao())
    for u, n, cor in ((0.08, "3", WHITE), (0.5, "1", CYAN), (0.72, "2", WHITE)):
        g.add(jato(u, cor if n == "1" else VIOLET, 7), furo(u))
        c = Circle(radius=0.14).set_stroke(cor, 6).set_fill("#06081A", 1.0).move_to([xl(u), 0, 0])
        g.add(c, tx(n, 56, cor).move_to([xl(u), -0.95 if n == "2" else -0.5, 0]))
    return g


ARTES = {1: arte_1, 2: arte_2, 3: arte_3, 4: arte_4, 5: arte_5, 6: arte_6, 7: arte_7, 8: arte_8, 9: arte_9, 10: arte_10}
MOLDURA = {1: False, 2: False, 3: True, 4: False, 5: False, 6: False, 7: True, 8: False, 9: False, 10: False}
TITULOS = {
    1: ("O FURO MAIS BAIXO", "VAI MAIS LONGE?"),
    2: ("O MELHOR FURO", "FICA NO MEIO"),
    3: ("ALTO OU BAIXO,", "MESMO ALCANCE"),
    4: ("O ALCANCE DESENHA", "UM SEMICÍRCULO"),
    5: ("MAIS RÁPIDO,", "MENOS TEMPO"),
    6: ("O PRODUTO MÁXIMO", "É UM QUADRADO"),
    7: ("A GRAVIDADE SOME", "DO ALCANCE"),
    8: ("ONDE FURAR PARA", "IR MAIS LONGE?"),
    9: ("RÁPIDO DEMAIS", "NÃO CHEGA LONGE"),
    10: ("EM CIMA, NO MEIO", "OU EMBAIXO?"),
}
v2.ARTES, v2.MOLDURA, v2.TITULOS = ARTES, MOLDURA, TITULOS


def grade(pastas, saida):
    imgs = [Image.open(p).resize((432, 768), Image.LANCZOS) for p in pastas]
    colunas = 5
    linhas = (len(imgs) + colunas - 1) // colunas
    folha = Image.new("RGB", (colunas * 442 + 10, linhas * 778 + 10), "#161616")
    for i, im in enumerate(imgs):
        folha.paste(im, (10 + (i % colunas) * 442, 10 + (i // colunas) * 778))
    folha.save(saida)


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else UNIT / "capas"
    out.mkdir(parents=True, exist_ok=True)
    so = int(sys.argv[2]) if len(sys.argv) > 2 else None
    feitas = []
    for n in ARTES:
        if so and n != so:
            continue
        alvo = out / f"capa_{n:02d}.png"
        v2.compor(n).save(alvo, optimize=True)
        feitas.append(alvo)
        print(alvo)
    if not so:
        grade(feitas, out / "grade_2x5.png")
