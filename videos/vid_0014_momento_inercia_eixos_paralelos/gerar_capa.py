"""Gera as 6 propostas de capa do vid_0014 (POR TRÁS DA FÓRMULA · EP. 05).

Uso, na raiz do repositório:
    uv run python videos/vid_0014_momento_inercia_eixos_paralelos/gerar_capa.py [PASTA_SAIDA [NUMERO]]

Reaproveita o compositor das capas do vid_0009 (mesmo layout aprovado: símbolo, título em duas linhas,
divisor, linha de série, painel neon, marca e horizonte). Só mudam o título, a série e o desenho do painel.
Paleta da cena: ciano = I_CM / x² / r²; violeta = d e Md²; magenta = termo cruzado; azul = barra e velocidade.
Física congelada: I_CM = ML²/12, I' = I_CM + Md², I_ponta = ML²/3 = 4 I_CM.
"""
import importlib.util
import sys
from pathlib import Path

from manim import (
    DOWN, LEFT, RIGHT, UP, Arrow, Brace, Circle, DashedLine, Dot, Line, MathTex, Rectangle, VGroup,
)

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
_spec = importlib.util.spec_from_file_location("capa9", ROOT / "videos" / "vid_0009_campo_solenoide" / "gerar_capa.py")
g9 = importlib.util.module_from_spec(_spec)
sys.modules["capa9"] = g9
_spec.loader.exec_module(g9)
g9.SERIE = "POR TRÁS DA FÓRMULA · EP. 05"

CYAN, WHITE, BLUE, MAGENTA = g9.CYAN, g9.WHITE, g9.BLUE, g9.MAGENTA
VIOLET, BLUE_L = "#9C8CFF", "#7FB2FF"


# ── Peças ───────────────────────────────────────────────────────────────────
def neon(mob, color, w=10):
    """Traço com brilho: duas cópias largas e translúcidas por baixo do traço."""
    a = mob.copy().set_stroke(color, w * 2.8, 0.22)
    b = mob.copy().set_stroke(color, w * 1.7, 0.32)
    mob.set_stroke(color, w, 1.0)
    return VGroup(a, b, mob)


def tx(s, size=100, color=WHITE):
    return MathTex(s, font_size=size, color=color)


def barra(comp=3.4, h=0.26):
    """Barra fina e rígida (azul), centrada na origem."""
    r = Rectangle(width=comp, height=h).set_fill(BLUE, 0.42)
    return neon(r, BLUE_L, 6)


def cm_x(x=0.0, s=0.13):
    """Marca × do centro de massa, branca."""
    return VGroup(Line([x - s, -s, 0], [x + s, s, 0]), Line([x - s, s, 0], [x + s, -s, 0])).set_stroke(WHITE, 6)


def eixo(x, cor=CYAN, r=0.24):
    """Eixo ⊙ perpendicular ao plano, em x."""
    c = Circle(radius=r).set_stroke(cor, 7).set_fill("#06081A", 1.0).move_to([x, 0, 0])
    return VGroup(neon(c, cor, 7)[:2], c, Dot([x, 0, 0], 0.075, color=cor))


def seta(p0, p1, cor=WHITE, w=9, tip=0.22):
    return Arrow(p0, p1, buff=0, stroke_width=w, tip_length=tip, color=cor,
                 max_tip_length_to_length_ratio=0.6, max_stroke_width_to_length_ratio=60)


def seta_baixo(h=0.5):
    return seta([0, 0, 0], [0, -h, 0], WHITE, 10, 0.24)


def i_cm(size=100, extra=""):
    return tx(r"I_{\mathrm{CM}}" + extra, size, CYAN)


# ── Painéis ─────────────────────────────────────────────────────────────────
def painel_1():
    """Mesma barra: eixo no centro (I_CM) → eixo na ponta (4 I_CM)."""
    def lado(x_eixo, rotulo):
        return VGroup(VGroup(barra(), cm_x(), eixo(x_eixo)), rotulo).arrange(DOWN, buff=0.35)
    esq = lado(0.0, i_cm(105))
    f = tx(r"4\,I_{\mathrm{CM}}", 105, WHITE)
    f[0][1:].set_color(CYAN)
    dir_ = lado(-1.7, f)
    return VGroup(esq, seta([0, 0, 0], [0.9, 0, 0], WHITE, 12, 0.3), dir_).arrange(RIGHT, buff=0.35)


def painel_2():
    """Um pedacinho dm a distância r do eixo, com v; à direita dK = ½ dm ω² r² (r² em ciano)."""
    b = barra(2.9)
    ex = -1.45
    dm = Rectangle(width=0.34, height=0.26).set_stroke(WHITE, 5).set_fill(WHITE, 0.55).move_to([0.6, 0, 0])
    reg = Line([ex, -0.42, 0], [0.6, -0.42, 0]).set_stroke(CYAN, 7)
    ticks = VGroup(*(Line([x, -0.54, 0], [x, -0.3, 0]).set_stroke(CYAN, 7) for x in (ex, 0.6)))
    r = tx("r", 80, CYAN).move_to([-0.4, -0.88, 0])
    v = seta([0.6, 0.2, 0], [0.6, 1.1, 0], BLUE_L, 11, 0.26)
    vl = tx("v", 80, BLUE_L).next_to(v, RIGHT, buff=0.15)
    diag = VGroup(b, eixo(ex), dm, reg, ticks, r, v, vl)
    f = tx(r"\tfrac{1}{2}\,dm\,\omega^2 r^2", 105, WHITE)
    f[0][7:9].set_color(CYAN)       # ω²
    f[0][9:11].set_color(CYAN)      # r²
    return VGroup(diag, f).arrange(RIGHT, buff=0.7)


def painel_3():
    """O eixo desliza do CM por d: a integral de x² vira a de (x − d)²?"""
    b = barra(4.2)
    d = 1.3
    arco = DashedLine([0, 0.55, 0], [d, 0.55, 0], dash_length=0.12).set_stroke(VIOLET, 5)
    ponta = seta([d - 0.3, 0.55, 0], [d, 0.55, 0], VIOLET, 5, 0.18)
    diag = VGroup(b, cm_x(), eixo(0.0), arco, ponta, eixo(d, VIOLET))
    diag[3:5].shift([0, 0, 0])
    f = tx(r"\int x^2\,dm\;\to\;\int (x-d)^2\,dm\;?", 82, WHITE)
    f[0][1:3].set_color(CYAN)
    f[0][9:15].set_color(VIOLET)
    f[0][-1].set_color(MAGENTA)
    return VGroup(diag, f).arrange(DOWN, buff=0.4)


def painel_4():
    """(x − d)² abre em três termos; o do meio (magenta) soma zero."""
    f = tx(r"(x-d)^2=x^2\,-\,2xd\,+\,d^2", 92, WHITE)
    f[0][8:10].set_color(CYAN)       # x²
    f[0][10:14].set_color(MAGENTA)   # −2xd
    f[0][14:17].set_color(VIOLET)    # +d² (inclui o sinal)
    g = tx(r"-2d\int x\,dm=0", 92, MAGENTA)
    return VGroup(f, seta_baixo(), g).arrange(DOWN, buff=0.22)


def painel_5():
    """Quatro blocos: um ciano (I_CM) e três violetas (Md²) = 4 I_CM."""
    lado, gap = 0.95, 0.07
    blocos = VGroup(*(Rectangle(width=lado, height=lado).set_fill(c, 0.78).set_stroke("#F5F7FF", 4, 0.9)
                      for c in (CYAN, VIOLET, VIOLET, VIOLET))).arrange(RIGHT, buff=gap)
    ciano = VGroup(blocos[0])
    violeta = VGroup(*blocos[1:])
    l1 = Brace(ciano, DOWN, buff=0.12, color=CYAN, sharpness=1.5)
    l2 = Brace(violeta, DOWN, buff=0.12, color=VIOLET, sharpness=1.5)
    t1 = i_cm(70).next_to(l1, DOWN, buff=0.1)
    t2 = tx(r"Md^2", 70, VIOLET).next_to(l2, DOWN, buff=0.1)
    t2.align_to(t1, UP)
    return VGroup(blocos, l1, l2, t1, t2)


def painel_6():
    """O teorema: I = I_CM + Md², com a barra e os dois eixos paralelos (d entre eles)."""
    f = tx(r"I=I_{\mathrm{CM}}+Md^2", 110, WHITE)
    f[0][2:6].set_color(CYAN)        # I_CM
    f[0][7:10].set_color(VIOLET)     # Md²
    d = 1.4
    b = barra(3.6)
    ex = VGroup(eixo(0.0), eixo(d, VIOLET))
    dd = seta([0.3, 0.52, 0], [d - 0.3, 0.52, 0], VIOLET, 6, 0.18)
    dd2 = seta([d - 0.3, 0.52, 0], [0.3, 0.52, 0], VIOLET, 6, 0.18)
    dl = tx("d", 62, VIOLET).move_to([d / 2, 0.92, 0])
    diag = VGroup(b, cm_x(), ex, dd, dd2, dl)
    return VGroup(f, diag).arrange(DOWN, buff=0.4)


PAINEIS = {1: painel_1, 2: painel_2, 3: painel_3, 4: painel_4, 5: painel_5, 6: painel_6}
TITULOS = {
    1: ("MESMA BARRA,", "4× MAIS INÉRCIA?"),
    2: ("DE ONDE VEM O", "RAIO AO QUADRADO?"),
    3: ("MUDOU O EIXO.", "REFAZ A INTEGRAL?"),
    4: ("O TERMO DO MEIO", "SOME. POR QUÊ?"),
    5: ("1 + 3 = 4", "O TEOREMA EM BLOCOS"),
    6: ("TEOREMA DOS", "EIXOS PARALELOS"),
}


def linhas(n):
    a, b = TITULOS[n]
    start = min(g9.fit(t, g9.BOLD, 870, 150).size for t in (a, b))     # as duas linhas no mesmo corpo
    fator = {5: 1.7}.get(n, 1.0)                                       # capa 5: "1 + 3 = 4" maior que a 2ª linha
    return [([(a, "white")], round(start * fator)), ([(b, "grad")], start)]


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
