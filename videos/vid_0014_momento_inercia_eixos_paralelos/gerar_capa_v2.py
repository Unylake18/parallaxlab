"""Segunda rodada de capas do vid_0014 (POR TRÁS DA FÓRMULA · EP. 05): 6 versões com arte maior.

Uso, na raiz do repositório:
    uv run python videos/vid_0014_momento_inercia_eixos_paralelos/gerar_capa_v2.py [PASTA_SAIDA [NUMERO]]

Mesma base da série (logo, divisor, linha de série, marca PARALLAX LAB e horizonte iguais; Space Grotesk na
headline e na série, pelo compositor do vid_0009). Aqui o painel é mais alto (ou some, nas versões sem moldura)
e a arte é desenhada para ser lida em tamanho de miniatura. Física congelada: I_CM = ML²/12, I' = I_CM + Md²,
I_ponta = ML²/3 = 4 I_CM (para a haste, I = M R_max²/3 nos dois eixos, daí os discos 1 : 4 da capa 1).
Paleta: ciano = I_CM / r² / x²; violeta = d, Md²; magenta = termo cruzado; azul = barra e v.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UP, Arc, Circle, DashedLine, Dot, Line, MathTex, Polygon, Rectangle, Sector, VGroup,
    VMobject,
)
from PIL import Image, ImageFont

UNIT = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("capa1", UNIT / "gerar_capa.py")
c1 = importlib.util.module_from_spec(_spec)
sys.modules["capa1"] = c1
_spec.loader.exec_module(c1)
g9 = c1.g9

CYAN, WHITE, BLUE, MAGENTA, VIOLET, BLUE_L = c1.CYAN, c1.WHITE, c1.BLUE, c1.MAGENTA, c1.VIOLET, c1.BLUE_L
tx, neon, seta = c1.tx, c1.neon, c1.seta

MOLDURA_ALTA = (100, 1135, 980, 1560)       # painel maior que o da série (120, 1146, 960, 1474)
ART_MAX = (800, 360)
ART_CY = 1347


def poli(pts, cor, op):
    return Polygon(*[[x, y, 0] for x, y in pts]).set_stroke(width=0).set_fill(cor, op)


def curva(f, x0, x1, cor, w=10, n=120):
    xs = np.linspace(x0, x1, n)
    return VMobject().set_points_as_corners([[x, f(x), 0] for x in xs]).set_stroke(cor, w)


# ── Artes ───────────────────────────────────────────────────────────────────
def arte_1():
    """Dois discos varridos pela mesma haste: eixo no centro (raio L/2) e na ponta (raio L). Discos 1 : 4."""
    Lb, h, ang = 1.6, 0.17, 28.0

    def disco(raio, cor, centro, pivo_na_ponta):
        g = VGroup(Circle(radius=raio).set_stroke(cor, 5, 0.9).set_fill(cor, 0.10).move_to(centro))
        for k in range(1, 7):                                      # rastro do giro: setores cada vez mais tênues
            g.add(Sector(radius=raio, angle=np.radians(14), start_angle=np.radians(ang - 14 * k - 3),
                         arc_center=centro).set_stroke(width=0).set_fill(cor, 0.55 * (1 - k / 7) ** 1.3))
        b = Rectangle(width=Lb, height=h).set_fill(BLUE, 0.55)
        b = neon(b, BLUE_L, 6)
        b.shift([Lb / 2 if pivo_na_ponta else 0.0, 0, 0]).rotate(np.radians(ang), about_point=[0, 0, 0]).shift(centro)
        g.add(b)
        cm = c1.cm_x(0.0, 0.1)
        cm.shift([Lb / 2 if pivo_na_ponta else 0.0, 0, 0]).rotate(np.radians(ang), about_point=[0, 0, 0]).shift(centro)
        g.add(cm, c1.eixo(0.0, cor, 0.17).shift(centro))
        return g

    esq = disco(Lb / 2, CYAN, np.array([0.0, 0.0, 0.0]), False)
    dir_ = disco(Lb, VIOLET, np.array([3.0, 0.0, 0.0]), True)
    discos = VGroup(esq, dir_)
    r1 = tx(r"I_{\mathrm{CM}}", 110, CYAN).next_to(esq, DOWN, buff=0.3)
    f = tx(r"4\,I_{\mathrm{CM}}", 120, WHITE)
    f[0][1:].set_color(CYAN)
    r2 = f.next_to(dir_, RIGHT, buff=0.4)
    return VGroup(discos, r1, r2)


def arte_2():
    """Quadrados de lado r, 2r e 3r (áreas 1, 4, 9) e, ao lado, 1 : 4 : 9 com K ∝ r²."""
    cores = {3: MAGENTA, 2: VIOLET, 1: CYAN}
    q = VGroup()
    for s in (3, 2, 1):
        r = Rectangle(width=s, height=s).set_stroke(cores[s], 8).set_fill(cores[s], 0.32)
        r.move_to([s / 2, s / 2, 0])
        q.add(r)
    for s, ctr in ((1, 0.5), (2, 1.5), (3, 2.5)):
        q.add(tx(str(s * s), 90, WHITE).move_to([ctr, ctr, 0]))
    marc = VGroup(*(tx(t, 62, cores[s]).move_to([s - 0.5 if s > 1 else 0.5, -0.38, 0])
                    for s, t in ((1, "r"), (2, "2r"), (3, "3r"))))
    marc[1].move_to([1.5 + 0.0, -0.38, 0])
    marc[2].move_to([2.5, -0.38, 0])
    marc[0].move_to([0.5, -0.38, 0])
    marc[1].set_opacity(0)
    marc[2].set_opacity(0)
    base = VGroup(q, marc[0])
    # 1 : 4 : 9 colorido e K ∝ r²
    seq = MathTex("1", ":", "4", ":", "9", font_size=190, color=WHITE)
    seq[0].set_color(CYAN)
    seq[2].set_color(VIOLET)
    seq[4].set_color(MAGENTA)
    k = tx(r"K\propto r^2", 110, WHITE)
    k[0][3:].set_color(CYAN)
    dir_ = VGroup(seq, k).arrange(DOWN, buff=0.35)
    return VGroup(base, dir_).arrange(RIGHT, buff=0.9, aligned_edge=DOWN)


def arte_3():
    """Perfis do integrando sobre a barra: x² (ciano, centrado no CM) e (x − d)² (violeta, centrado no eixo)."""
    d, k, x0, x1 = 1.1, 0.16, -2.2, 2.2
    xs = np.linspace(x0, x1, 80)
    f1, f2 = (lambda x: k * x * x), (lambda x: k * (x - d) ** 2)
    fill1 = poli([(x, 0) for x in (x0,)] + [(x, f1(x)) for x in xs] + [(x1, 0)], CYAN, 0.16)
    fill2 = poli([(x0, 0)] + [(x, f2(x)) for x in xs] + [(x1, 0)], VIOLET, 0.16)
    g = VGroup(fill2, fill1, curva(f2, x0, x1, VIOLET, 11), curva(f1, x0, x1, CYAN, 11))
    barra = c1.barra(2 * 2.45, 0.26).shift([0, -0.2, 0])
    cm = c1.cm_x(0.0, 0.12).shift([0, -0.2, 0])
    ax1 = c1.eixo(0.0, CYAN, 0.2).shift([0, -0.2, 0])
    ax2 = c1.eixo(d, VIOLET, 0.2).shift([0, -0.2, 0])
    a = tx(r"x^2", 90, CYAN).move_to([2.2, 1.15, 0])
    b = tx(r"(x-d)^2", 90, VIOLET).move_to([-1.75, 1.95, 0])
    return VGroup(g, barra, cm, ax1, ax2, a, b)


def arte_4():
    """O termo cruzado −2xd é uma reta: as áreas acima e abaixo do eixo se anulam (∫ x dm = M x_CM = 0)."""
    m, xm = 0.8, 1.9
    f = lambda x: -m * x
    esq = poli([(-xm, 0), (-xm, f(-xm)), (0, 0)], MAGENTA, 0.40)
    dir_ = poli([(xm, 0), (xm, f(xm)), (0, 0)], MAGENTA, 0.20)
    eixo_x = Line([-xm - 0.4, 0, 0], [xm + 0.4, 0, 0]).set_stroke(BLUE_L, 6, 0.85)
    eixo_y = DashedLine([0, -1.7, 0], [0, 1.7, 0], dash_length=0.14).set_stroke(WHITE, 4, 0.6)
    lin = curva(f, -xm, xm, MAGENTA, 12, 20)
    mais = tx("+", 100, WHITE).move_to([-1.1, 0.5, 0])
    menos = tx("-", 100, WHITE).move_to([1.1, -0.5, 0])
    g = VGroup(esq, dir_, eixo_x, eixo_y, lin, mais, menos, c1.cm_x(0.0, 0.12))
    topo = tx(r"-2xd", 110, MAGENTA)
    a = tx(r"\int -2xd\,dm", 110, WHITE)
    a[0][0].set_color(MAGENTA)
    a[0][1:4].set_color(MAGENTA)
    b = tx(r"=\,0", 130, WHITE)
    dir_txt = VGroup(topo, a, b).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    return VGroup(g, dir_txt).arrange(RIGHT, buff=0.8)


def arte_5():
    """Quadrado 2×2 de blocos de 1/12 ML²: um ciano (I_CM) e três violetas (Md²); ao lado a soma = 4 I_CM."""
    lado, gap = 1.4, 0.09
    cores = [[VIOLET, VIOLET], [CYAN, VIOLET]]                     # linhas de cima para baixo
    blocos = VGroup()
    for j, linha in enumerate(cores):
        for i, c in enumerate(linha):
            b = Rectangle(width=lado, height=lado).set_fill(c, 0.78).set_stroke("#F5F7FF", 4, 0.9)
            b.move_to([i * (lado + gap), -j * (lado + gap), 0])
            blocos.add(b)
    nums = VGroup(*(tx(r"\tfrac{1}{12}", 72, "#06081A").move_to(b) for b in blocos))
    quadro = VGroup(blocos, nums)
    a = tx(r"I_{\mathrm{CM}}", 120, CYAN)
    b = tx(r"+\,Md^2", 120, VIOLET)
    c = tx(r"=\,4\,I_{\mathrm{CM}}", 120, WHITE)
    c[0][2:].set_color(CYAN)
    dir_ = VGroup(a, b, c).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    return VGroup(quadro, dir_).arrange(RIGHT, buff=0.9)


def arte_6():
    """O teorema, grande, sobre a barra com os dois eixos paralelos e d = L/2."""
    f = tx(r"I=I_{\mathrm{CM}}+Md^2", 170, WHITE)
    f[0][2:6].set_color(CYAN)
    f[0][7:10].set_color(VIOLET)
    Lb = 4.8
    barra = c1.barra(Lb, 0.28)
    cm = c1.cm_x(0.0, 0.14)
    ex = VGroup(c1.eixo(0.0, CYAN, 0.24), c1.eixo(Lb / 2, VIOLET, 0.24))
    d1 = seta([0.35, 0.55, 0], [Lb / 2 - 0.35, 0.55, 0], VIOLET, 7, 0.2)
    d2 = seta([Lb / 2 - 0.35, 0.55, 0], [0.35, 0.55, 0], VIOLET, 7, 0.2)
    dl = tx(r"d=\tfrac{L}{2}", 70, VIOLET).move_to([Lb / 4, 1.1, 0])
    diag = VGroup(barra, cm, ex, d1, d2, dl)
    return VGroup(f, diag).arrange(DOWN, buff=0.35)


ARTES = {1: arte_1, 2: arte_2, 3: arte_3, 4: arte_4, 5: arte_5, 6: arte_6}
MOLDURA = {1: True, 2: False, 3: True, 4: False, 5: True, 6: False}
TITULOS = {
    1: ("EIXO NA PONTA:", "4× MAIS INÉRCIA?"),
    2: ("DOBROU O RAIO,", "4× A ENERGIA"),
    3: ("MUDAR O EIXO SEM", "REFAZER A CONTA"),
    4: ("A PARCELA QUE", "SOME DA CONTA"),
    5: ("UM BLOCO CIANO,", "TRÊS VIOLETAS"),
    6: ("O ATALHO DOS", "EIXOS PARALELOS"),
}


def linhas(n):
    a, b = TITULOS[n]
    start = min(g9.fit(t, g9.BOLD, 870, 150).size for t in (a, b))
    return [([(a, "white")], start), ([(b, "grad")], start)]


def compor(n):
    """Mesma base e mesmo cabeçalho do g9.cover; só o painel muda (maior, com ou sem moldura)."""
    com_moldura = MOLDURA[n]
    velha_moldura, velha_func = g9.MOLDURA, g9.desenhar_moldura
    if com_moldura:
        g9.MOLDURA = MOLDURA_ALTA
    else:
        g9.desenhar_moldura = lambda img, cantos: img            # painel sem moldura: só o fundo apagado
    try:
        arte = g9.render_rgba(lambda: ARTES[n]().move_to([0, 0, 0]), 500)
        img = g9.base()
    finally:
        g9.MOLDURA, g9.desenhar_moldura = velha_moldura, velha_func
    rows = [g9.headline_line(seg, start) for seg, start in linhas(n)]
    gap = 22
    total = sum(r[0].height for r in rows) + gap * (len(rows) - 1)
    assert total <= 340, f"headline alta demais: {total}px"
    y = 832 - total / 2
    for mask, color, glow, _ in rows:
        img = g9.glow_paste(img, mask, ((img.width - mask.width) // 2, int(y)), color, glow, 15, 0.5)
        y += mask.height + gap
    serie = g9.text_mask(g9.SERIE, ImageFont.truetype(g9.MEDIUM, 38), tracking=9)
    serie = serie.resize((min(serie.width, 850), round(serie.height * min(serie.width, 850) / serie.width)), Image.LANCZOS)
    img = g9.glow_paste(img, serie, g9.center(img, serie, 1097), Image.new("RGB", serie.size, (245, 247, 255)),
                        (60, 120, 255), 6, 0.32)
    k = min(ART_MAX[0] / arte.width, ART_MAX[1] / arte.height)
    if not com_moldura:
        k = min(900 / arte.width, 400 / arte.height)
    arte = arte.resize((round(arte.width * k), round(arte.height * k)), Image.LANCZOS)
    x, yy = (img.width - arte.width) // 2, (ART_CY if com_moldura else 1340) - arte.height // 2
    cheio = Image.new("L", img.size, 0)
    cheio.paste(arte.getchannel("A"), (x, yy))
    from PIL import ImageFilter
    halo = cheio.filter(ImageFilter.GaussianBlur(12)).point(lambda p: int(p * 0.35))
    img = Image.composite(Image.new("RGBA", img.size, (90, 110, 255, 255)), img, halo)
    img.alpha_composite(arte, (x, yy))
    return img.convert("RGB")


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else UNIT / "capas_v2"
    out.mkdir(parents=True, exist_ok=True)
    so = int(sys.argv[2]) if len(sys.argv) > 2 else None
    for n in ARTES:
        if so and n != so:
            continue
        alvo = out / f"capa_v2_{n:02d}.png"
        compor(n).save(alvo, optimize=True)
        print(alvo)
