"""Teste de cena: o 3D inteiro vem do Blender; o Manim só põe texto, fórmulas e gráfico por cima (sandbox, fora do yt_0002).

Painel esquerdo: sequência de PNG com alpha de render_sequencia.py (cabo coaxial + cilindro gaussiano que cresce + setas de E no
vão). Painel direito: região, Q_env, E(r) e um gráfico, todos ligados ao MESMO ValueTracker que escolhe o quadro 3D, então o
raio desenhado, o texto e o marcador do gráfico nunca saem de sincronia.

Rodar, a partir da raiz do repositório (primeiro gere a sequência com render_sequencia.py):
    uv run python -m manim -r 960,540 --fps 15 experimentos/blender/teste_gauss_coaxial/cena_manim.py TesteCoaxial3D
"""

import json
import sys
from collections import OrderedDict
from contextlib import contextmanager
from pathlib import Path

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UL, UP, Axes, Circle, DashedLine, FadeIn, ImageMobject, Line, MathTex, Scene, ValueTracker, VGroup,
    VMobject, always_redraw, config, smooth,
)
from PIL import Image

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ))
from template.config_horizontal import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR  # noqa: E402
from template.fonts import screen_text  # noqa: E402

WHITE, CYAN, BLUE_L, VIOLET = TEXT_COLOR, PRIMARY_COLOR, "#7FB2FF", "#9C8CFF"
PASTA = RAIZ / "renders" / "teste_gauss_coaxial" / "1120x784"
RL = 1.6                                    # borda esquerda da coluna de texto
PAINEL_X, PAINEL_Y, PAINEL_L = -3.3, -0.2, 9.0


@contextmanager
def wide_pango():
    pw, ph = config.pixel_width, config.pixel_height
    config.pixel_width, config.pixel_height = 4000, 4000
    try:
        yield
    finally:
        config.pixel_width, config.pixel_height = pw, ph


def text(content, size=24, color=WHITE, opacity=1.0):
    with wide_pango():
        t = screen_text(content, size)
    return t.set_color(color).set_opacity(opacity)


def eq(*parts, size=40, color=WHITE, colors=None):
    m = MathTex(*parts, font_size=size, color=color)
    for i, c in (colors or {}).items():
        m[i].set_color(c)
    return m


def P(x, y):
    return np.array([x, y, 0.0])


def col(m, y, dx=0.0):
    return m.move_to(P(0, y)).align_to(P(RL + dx, 0), LEFT)


class Sequencia:
    """Quadros PNG do Blender lidos do disco sob demanda (cache LRU curto)."""

    def __init__(self, pasta):
        self.pasta = Path(pasta)
        if not (self.pasta / "meta.json").exists():
            raise SystemExit(f"Sequência não encontrada em {pasta}. Gere com:\n  blender.exe -b -P "
                             "experimentos/blender/teste_gauss_coaxial/render_sequencia.py -- --frames 90 --res 1120x784")
        self.meta = json.loads((self.pasta / "meta.json").read_text(encoding="utf-8"))
        self.n = self.meta["frames"]
        self._cache = OrderedDict()

    def quadro(self, i):
        if i not in self._cache:
            self._cache[i] = np.array(Image.open(self.pasta / f"frame_{i + 1:04d}.png").convert("RGBA"))
            while len(self._cache) > 12:
                self._cache.popitem(last=False)
        return self._cache[i]


def painel_3d(seq, s):
    """ImageMobject cujo quadro segue o tracker `s` (0 a 1): quadro i = raio r0 + (r1 - r0) * i / (n - 1)."""
    mob = ImageMobject(seq.quadro(0)).set_width(PAINEL_L).move_to(P(PAINEL_X, PAINEL_Y))
    estado = {"i": -1}

    def aplicar(m):
        i = int(round(min(max(s.get_value(), 0.0), 1.0) * (seq.n - 1)))
        arr = seq.quadro(i)
        if i != estado["i"] or m.stroke_opacity < 1:
            m.pixel_array = arr.copy()
            m.orig_alpha_pixel_array = arr[:, :, 3]
            if m.stroke_opacity < 1:                       # preserva um FadeIn em andamento
                m.pixel_array[:, :, 3] = (arr[:, :, 3] * m.stroke_opacity).astype(m.pixel_array.dtype)
            estado["i"] = i

    mob.add_updater(aplicar)
    return mob


class TesteCoaxial3D(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        seq = Sequencia(PASTA)
        r0, r1, a, b = (seq.meta[k] for k in ("r0", "r1", "a", "b"))
        s = ValueTracker(0.0)
        s_de = lambda r: (r - r0) / (r1 - r0)
        r_atual = lambda: r0 + s.get_value() * (r1 - r0)

        header = text("TESTE · CENA 3D NO BLENDER, TEXTO EM MANIM", 18, opacity=0.6).to_corner(UL, buff=0.38)
        titulo = col(text("CABO COAXIAL · modelo infinito", 24, opacity=0.92), 2.95)
        sub = col(text("3D e texto sincronizados", 24, CYAN, 0.9), 2.4)
        rodape = col(text("3D: Blender · fórmulas e gráfico: Manim", 18, opacity=0.55), -4.15)

        # um bloco por região; só o da região atual aparece (opacidade ligada ao raio da gaussiana)
        def bloco(dominio, q, resultado, nota):
            dom = eq(dominio, size=34, color=VIOLET)
            qq = eq(q, size=40)
            dom.move_to(P(0, 1.7)).align_to(P(RL, 0), LEFT)
            qq.move_to(P(0, 1.7)).align_to(P(RL + 1.9, 0), LEFT)
            res = col(resultado, 0.6)
            nt = col(text(nota, 24, opacity=0.92), -0.4)
            return VGroup(dom, qq, res, nt)

        reg1 = bloco(r"r<a", r"Q_{\mathrm{env}}=0", eq("E", "=0", size=50, colors={0: CYAN}), "dentro do metal: nada envolvido")
        reg2 = bloco(r"a<r<b", r"Q_{\mathrm{env}}=\lambda L",
                     eq("E", "=", r"\frac{\lambda}{2\pi\varepsilon_0 r}", size=50, colors={0: CYAN}), "o campo existe só no vão")
        reg3 = bloco(r"r>b", r"Q_{\mathrm{env}}=(\lambda-\lambda)L=0", eq("E", "=0", size=50, colors={0: CYAN}),
                     "cargas opostas: campo confinado")
        regioes = ((reg1, lambda r: r < a - 1e-3), (reg2, lambda r: a - 1e-3 <= r <= b + 1e-3), (reg3, lambda r: r > b + 1e-3))
        for g, cond in regioes:
            g.add_updater(lambda m, c=cond: m.set_opacity(1.0 if c(r_atual()) else 0.0))
            g.update()

        # gráfico E(r): 0 dentro do metal, ∝ 1/r no vão, 0 fora; o marcador segue o MESMO raio do 3D
        ax = Axes(x_range=[0, r1 * 1.05, 1], y_range=[0, 1.25, 1], x_length=5.0, y_length=1.9, tips=False,
                  axis_config={"color": WHITE, "stroke_width": 2, "include_ticks": False, "stroke_opacity": 0.8})
        ax.shift(P(RL + 0.45, -3.55) - ax.c2p(0, 0))
        E = lambda r: (a / r) if a < r < b else 0.0
        rs = np.linspace(a, b, 60)
        curva = VGroup(Line(ax.c2p(0, 0), ax.c2p(a, 0)), VMobject().set_points_as_corners([ax.c2p(r, E(r)) for r in rs]),
                       Line(ax.c2p(b, 0), ax.c2p(r1, 0))).set_stroke(CYAN, 4)
        quedas = VGroup(DashedLine(ax.c2p(a, 0), ax.c2p(a, 1), dash_length=0.08), DashedLine(ax.c2p(b, 0), ax.c2p(b, a / b), dash_length=0.08)
                        ).set_stroke(VIOLET, 2, 0.6)
        marcas = VGroup(eq("a", size=30, color=BLUE_L).move_to(ax.c2p(a, 0) + P(0, -0.32)),
                        eq("b", size=30, color=BLUE_L).move_to(ax.c2p(b, 0) + P(0, -0.32)),
                        eq("r", size=34, color=VIOLET).move_to(ax.c2p(r1, 0) + P(0.25, -0.3)),
                        eq("E", size=34, color=CYAN).move_to(ax.c2p(0, 1.25) + P(0.25, 0.05)))
        marcador = always_redraw(lambda: Circle(radius=0.1).move_to(ax.c2p(r_atual(), E(r_atual()))).set_stroke(WHITE, 2).set_fill(CYAN, 1).set_z_index(6))
        linha_r = always_redraw(lambda: DashedLine(ax.c2p(r_atual(), 0), ax.c2p(r_atual(), E(r_atual())), dash_length=0.07).set_stroke(VIOLET, 2.5, 0.9))

        img = painel_3d(seq, s)
        img.set_opacity(0.0)
        self.add(img)
        self.play(img.animate.set_opacity(1.0), FadeIn(header), FadeIn(titulo), run_time=1.2)
        self.add(*[g for g, _ in regioes])
        self.play(FadeIn(sub, shift=0.1 * UP), FadeIn(rodape), run_time=0.8)
        self.play(FadeIn(VGroup(ax, curva, quedas, marcas)), run_time=0.9)
        self.add(marcador, linha_r)
        self.wait(2.0)                                                       # r < a: dentro do metal
        self.play(s.animate.set_value(s_de(1.0)), run_time=3.5, rate_func=smooth)    # atravessa r = a e para no vão
        self.wait(3.0)                                                       # a < r < b
        self.play(s.animate.set_value(s_de(1.75)), run_time=3.5, rate_func=smooth)   # atravessa r = b
        self.wait(3.0)                                                       # r > b
        self.play(s.animate.set_value(0.0), run_time=4.0, rate_func=smooth)  # volta ao início: o mesmo quadro 3D, em sentido inverso
        self.wait(1.0)
