"""Preview refinado (sandbox, fora do yt_0002): coaxial, duas folhas e esfera maciça — Blender (3D) + Manim (leitura física).

Manim: fórmulas, regiões, Q_env, gráfico com marcador, corte/vista 2D e esquemas vetoriais 2D. Tudo ligado ao MESMO ValueTracker que
escolhe o quadro 3D. Sinal: + azul, − magenta; a carga em Q_env ganha halo violeta (no 3D), nunca muda de cor.

Rodar, a partir da raiz do repositório (antes: render_refinado.py --caso todos):
    uv run python -m manim -r 960,540 --fps 15 --media_dir media/preview_gauss_refinado experimentos/blender/preview_gauss_refinado/cena_refinado.py PreviewGaussRefinado
"""

import sys
from pathlib import Path

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UL, UP, Annulus, Arrow, Axes, Circle, DashedLine, DashedVMobject, FadeIn, FadeOut, Group, Line, Rectangle, Scene,
    ValueTracker, VGroup, VMobject, always_redraw, smooth,
)

HERE = Path(__file__).resolve().parent
RAIZ = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "teste_gauss_coaxial"))
from casos_ref import CASOS, ORDEM, PASTA_SEQ, RES  # noqa: E402
from cena_manim import (  # noqa: E402  (helpers da v1 do coaxial; ela não é alterada)
    BACKGROUND_COLOR, BLUE_L, CYAN, RL, VIOLET, WHITE, P, Sequencia, col, eq, painel_3d, text,
)

MAG = "#EA63FF"
Q_ENV = r"Q_{\mathrm{env}}"
U = lambda g: P(np.cos(np.radians(g)), np.sin(np.radians(g)))      # noqa: E731


def mix(*pedacos, size=24, cor=WHITE, op=0.92):
    return VGroup(*[text(q, size, cor, op) if isinstance(q, str) else q for q in pedacos]).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)


def frac(num, den, esq="E"):
    return lambda: eq(esq, "=", rf"\frac{{{num}}}{{{den}}}", size=50, colors={0: CYAN})


ZERO = lambda: eq("E", "=0", size=50, colors={0: CYAN})      # noqa: E731

# ── especificação por caso ──────────────────────────────────────────────────
UI = {
    "coax": dict(
        titulo=["CABO COAXIAL ·", eq(r"+\lambda", size=28, color=BLUE_L), "e", eq(r"-\lambda", size=28, color=MAG)],
        reg=[(lambda p: p < 0.5 - 1e-3, r"r<a", Q_ENV + "=0", ZERO, "dentro do metal: nada envolvido"),
             (lambda p: 0.5 - 1e-3 <= p <= 1.5 + 1e-3, r"a<r<b", Q_ENV + r"=\lambda L", frac(r"\lambda", r"2\pi\varepsilon_0 r"), "o campo existe só no vão"),
             (lambda p: p > 1.5 + 1e-3, r"r>b", Q_ENV + r"=(\lambda-\lambda)L=0", ZERO, "o campo do vão continua; fora, E = 0")],
        E=lambda p: 0.5 / p if 0.5 < p < 1.5 else 0.0, x=(0.0, 1.9), marcas=[(0.5, "a"), (1.5, "b")], xlab="r", ylab="E",
        plano=[(0.9, 2.2, 1.4), (1.7, 2.2, 1.6)]),
    "duas": dict(
        titulo=["DUAS FOLHAS ·", eq(r"+\sigma", size=28, color=BLUE_L), "e", eq(r"-\sigma", size=28, color=MAG)],
        reg=[(lambda p: p < -1.1, r"x<-d", Q_ENV + "=0", ZERO, "o zero vem da superposição"),
             (lambda p: -1.1 <= p <= 1.1, r"-d<x<d", Q_ENV + r"=\sigma A", frac(r"\sigma", r"\varepsilon_0"), "entre as folhas: os campos somam"),
             (lambda p: p > 1.1, r"x>d", Q_ENV + r"=(\sigma-\sigma)A=0", ZERO, "fora: campos opostos se cancelam")],
        E=lambda p: 0.9 if -1.1 < p < 1.1 else 0.0, x=(-1.7, 1.9), marcas=[(-1.1, "-d"), (1.1, "d")], xlab="x", ylab="E",
        plano=[(0.0, 2.2, 1.8), (1.7, 2.2, 1.8)]),
    "esfera": dict(
        titulo=["ESFERA MACIÇA ·", eq(r"\rho", size=28, color=BLUE_L), "constante"],
        reg=[(lambda p: p < 1.0 - 1e-3, r"r<R", Q_ENV + r"=\frac{4}{3}\pi\rho r^{3}", frac(r"\rho r", r"3\varepsilon_0"), "Q_env cresce com r³; E cresce com r"),
             (lambda p: p >= 1.0 - 1e-3, r"r>R", Q_ENV + r"=\frac{4}{3}\pi\rho R^{3}", frac(r"\rho R^{3}", r"3\varepsilon_0 r^{2}"), "fora do corpo: Q_env fixa; E cai como 1/r²")],
        E=lambda p: p if p <= 1 else 1 / p ** 2, x=(0.0, 1.5), marcas=[(1.0, "1")], xlab=r"r/R", ylab=r"E/E_R",
        plano=[(0.55, 2.0, 0.9), (1.0, 1.4, 1.3), (1.45, 1.8, 1.4)]),
}


class PreviewGaussRefinado(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.abertura()
        for cid in ORDEM:
            self.caso(cid)
        self.fechamento()

    def abertura(self):
        t = text("LEI DE GAUSS · PADRÃO HÍBRIDO REFINADO", 34, WHITE).move_to(P(0, 1.2))
        s = text("coaxial · duas folhas · esfera maciça", 26, CYAN, 0.9).move_to(P(0, 0.5))
        chaves = VGroup(*[VGroup(Circle(radius=0.08).set_stroke(width=0).set_fill(c, 1), text(n, 22, WHITE, 0.9)).arrange(RIGHT, buff=0.15)
                          for c, n in ((BLUE_L, "carga +"), (MAG, "carga −"), (VIOLET, "halo = em Q_env"), (CYAN, "campo E"))]
                         ).arrange(RIGHT, buff=0.55).move_to(P(0, -0.6))
        aviso = text("preview experimental · não substitui o vídeo principal", 20, WHITE, 0.55).move_to(P(0, -2.2))
        self.play(FadeIn(t, shift=0.1 * UP), FadeIn(s), run_time=0.9)
        self.play(FadeIn(chaves), FadeIn(aviso), run_time=0.8)
        self.wait(2.0)
        self.play(FadeOut(VGroup(t, s, chaves, aviso)), run_time=0.5)

    def fechamento(self):
        t = text("campo existente × campo avaliado · sinal sempre legível · setas com oclusão", 24, WHITE, 0.9).move_to(P(0, 0.2))
        self.play(FadeIn(t), run_time=0.7)
        self.wait(2.2)
        self.play(FadeOut(t), run_time=0.5)

    def caso(self, cid):
        spec, ui = CASOS[cid], UI[cid]
        p0, p1 = spec["p0"], spec["p1"]
        seq = Sequencia(RAIZ / PASTA_SEQ / cid / RES)
        s = ValueTracker(0.0)
        s_de = lambda p: (p - p0) / (p1 - p0)
        p_atual = lambda: p0 + s.get_value() * (p1 - p0)

        titulo = col(mix(*ui["titulo"]), 2.95)
        regioes = []
        for cond, dom, q, fe, nota in ui["reg"]:
            d = eq(dom, size=34, color=VIOLET).move_to(P(0, 1.7)).align_to(P(RL, 0), LEFT)
            qq = eq(q, size=40).move_to(P(0, 1.7)).align_to(P(RL + 1.9, 0), LEFT)
            g = VGroup(d, qq, col(fe(), 0.6), col(text(nota, 22, WHITE, 0.92), -0.4))
            g.add_updater(lambda m, c=cond: m.set_opacity(1.0 if c(p_atual()) else 0.0))
            g.update()
            regioes.append(g)

        # gráfico: a curva parte de x = xa (origem no caso da esfera: E(0) = 0) e o marcador segue o mesmo p do quadro 3D
        xa, xb = ui["x"]
        larg = 2.3 if cid == "duas" else 2.9
        ax = Axes(x_range=[xa, xb, 1], y_range=[0, 1.25, 1], x_length=larg, y_length=1.9, tips=False,
                  axis_config={"color": WHITE, "stroke_width": 2, "include_ticks": False, "stroke_opacity": 0.8})
        ax.shift(P(RL + 0.35, -3.55) - ax.c2p(xa, 0))
        E = ui["E"]
        curva = VMobject().set_points_as_corners([ax.c2p(x, E(x)) for x in np.linspace(xa, xb, 260)]).set_stroke(CYAN, 4)
        marcas = VGroup(*[eq(n, size=28, color=BLUE_L).move_to(ax.c2p(v, 0) + P(0, -0.3)) for v, n in ui["marcas"]],
                        eq(ui["ylab"], size=30, color=CYAN).move_to(ax.c2p(xa, 1.25) + P(0.4, 0.05)),
                        eq(ui["xlab"], size=30, color=VIOLET).move_to(ax.c2p(xb, 0) + P(0.3, -0.3)))
        guias = VGroup(*[DashedLine(ax.c2p(v, 0), ax.c2p(v, 1.0), dash_length=0.07).set_stroke(VIOLET, 1.8, 0.45) for v, _ in ui["marcas"]])
        marcador = always_redraw(lambda: Circle(radius=0.1).move_to(ax.c2p(p_atual(), E(p_atual()))).set_stroke(WHITE, 2).set_fill(CYAN, 1).set_z_index(6))
        linha_p = always_redraw(lambda: DashedLine(ax.c2p(p_atual(), 0), ax.c2p(p_atual(), E(p_atual())), dash_length=0.07).set_stroke(VIOLET, 2.5, 0.9))

        fixo, dinamico = {"coax": self.w_coax, "duas": self.w_duas, "esfera": self.w_esfera}[cid](p_atual)

        img = painel_3d(seq, s)
        img.set_opacity(0.0)
        self.add(img)
        estatico = VGroup(titulo, ax, curva, marcas, guias, fixo)
        self.play(img.animate.set_opacity(1.0), FadeIn(estatico), run_time=0.7)
        self.add(*regioes, marcador, linha_p, *dinamico)
        self.wait(1.2)
        for alvo, mover, parar in ui["plano"]:
            self.play(s.animate.set_value(s_de(alvo)), run_time=mover, rate_func=smooth)
            self.wait(parar)
        for m in (marcador, linha_p, *regioes, *dinamico):          # congela o estado final: o fade-out não é desfeito pelos updaters
            m.clear_updaters()
        self.play(FadeOut(Group(img, estatico, *regioes, marcador, linha_p, *dinamico)), run_time=0.4)
        img.clear_updaters()
        self.remove(img, marcador, linha_p, *regioes, *dinamico)

    # ── esquemas 2D (Manim): onde estou radialmente / como os campos se compõem ─────────────────
    def w_coax(self, p_atual):
        C, k, a, b = P(6.45, -2.3), 0.62, 0.5, 1.5
        vao = Annulus(inner_radius=k * a, outer_radius=k * (b - 0.07)).move_to(C).set_stroke(width=0).set_fill(CYAN, 0.0)
        vao.add_updater(lambda m: m.set_fill(CYAN, 0.15 if a - 1e-3 <= p_atual() <= b + 1e-3 else 0.0))
        nuc = Circle(radius=k * a).move_to(C).set_stroke(BLUE_L, 3).set_fill("#267BFF", 0.45)
        cas = Annulus(inner_radius=k * (b - 0.07), outer_radius=k * b).move_to(C).set_stroke(MAG, 2).set_fill(MAG, 0.55)
        setas = VGroup()
        for i in range(8):                                           # campo existente no vão (radial, ∝ 1/r), com oclusão natural do desenho
            r0 = 0.72 if i % 2 == 0 else 1.08
            setas.add(Arrow(C + k * r0 * U(45 * i + 10), C + k * (r0 + 0.30 / r0) * U(45 * i + 10), buff=0, stroke_width=3, tip_length=0.1, color=CYAN))
        setas.add_updater(lambda m: m.set_stroke(opacity=1.0 if a <= p_atual() <= b else 0.5))
        gauss = always_redraw(lambda: VGroup(
            Circle(radius=k * p_atual()).move_to(C).set_stroke(width=0).set_fill(VIOLET, 0.07),
            DashedVMobject(Circle(radius=k * p_atual()).move_to(C), num_dashes=44, dashed_ratio=0.6).set_stroke(VIOLET, 3, 0.95),
            DashedLine(C, C + k * p_atual() * U(-38), dash_length=0.06).set_stroke(VIOLET, 2.5, 0.95),
            eq("r", size=28, color=VIOLET).move_to(C + (k * p_atual() * 0.5 + 0.0) * U(-38) + 0.2 * U(-128))).set_z_index(5))
        marcas = VGroup(Line(C, C + k * a * U(100)).set_stroke(BLUE_L, 2, 0.9), eq("a", size=26, color=BLUE_L).move_to(C + (k * a * 0.5 + 0.0) * U(100) + 0.17 * U(190)),
                        Line(C + k * a * U(135), C + k * b * U(135)).set_stroke(MAG, 2, 0.9), eq("b", size=26, color=MAG).move_to(C + k * b * U(135) + 0.22 * U(135)))
        rot = text("corte transversal", 18, WHITE, 0.6).move_to(C + P(0, 1.55))
        return VGroup(nuc, cas, setas, marcas, rot), [vao, gauss]

    def w_duas(self, p_atual):
        C, ks, d = P(6.05, -2.2), 0.82, 1.1
        sz = lambda x: C.copy() + P(x * ks, 0)                        # noqa: E731
        linhas = {"E₊": 0.62, "E₋": 0.14, "E": -0.38}
        zonas = [(-2.05, -d), (-d, d), (d, 2.05)]
        fundos = []
        for i, (x0, x1) in enumerate(zonas):
            r = Rectangle(width=(x1 - x0) * ks, height=1.85).move_to(C + P((x0 + x1) / 2 * ks, 0.1)).set_stroke(width=0).set_fill(VIOLET, 0.0)
            ind = (lambda p, i=i: (p < -d, -d <= p <= d, p > d)[i])
            r.add_updater(lambda m, ind=ind: m.set_fill(VIOLET, 0.13 if ind(p_atual()) else 0.0))
            fundos.append(r)
        barras = VGroup(Line(sz(-d) + P(0, -0.75), sz(-d) + P(0, 0.95)).set_stroke(BLUE_L, 4), Line(sz(d) + P(0, -0.75), sz(d) + P(0, 0.95)).set_stroke(MAG, 4),
                        eq(r"+\sigma", size=24, color=BLUE_L).move_to(sz(-d) + P(0, 1.18)), eq(r"-\sigma", size=24, color=MAG).move_to(sz(d) + P(0, 1.18)))

        def seta(x, y, sentido, comp=0.5, cor=CYAN):
            return Arrow(sz(x) + P(-sentido * comp / 2, y), sz(x) + P(sentido * comp / 2, y), buff=0, stroke_width=3.5, tip_length=0.11, color=cor)
        xl, xm, xr = -1.58, 0.0, 1.58
        s_ = VGroup(
            seta(xl, linhas["E₊"], -1), seta(xm, linhas["E₊"], 1), seta(xr, linhas["E₊"], 1),            # campo da folha + (afasta-se dela)
            seta(xl, linhas["E₋"], 1), seta(xm, linhas["E₋"], 1), seta(xr, linhas["E₋"], -1),            # campo da folha − (aproxima-se dela)
            seta(xm, linhas["E"], 1, 0.95),                                                              # soma entre as folhas
            eq("0", size=30, color=CYAN).move_to(sz(xl) + P(0, linhas["E"])), eq("0", size=30, color=CYAN).move_to(sz(xr) + P(0, linhas["E"])))
        rotulos = VGroup(eq(r"E_{+}", size=26, color=CYAN).move_to(C + P(-2.0, linhas["E₊"])), eq(r"E_{-}", size=26, color=CYAN).move_to(C + P(-2.0, linhas["E₋"])),
                         eq("E", size=26, color=CYAN).move_to(C + P(-2.0, linhas["E"])))
        veredito = VGroup(text("cancelam", 16, WHITE, 0.75).move_to(sz(xl) + P(0, -0.82)), text("somam", 16, WHITE, 0.75).move_to(sz(xm) + P(0, -0.82)),
                          text("cancelam", 16, WHITE, 0.75).move_to(sz(xr) + P(0, -0.82)))
        rot = text("superposição", 18, WHITE, 0.6).move_to(C + P(0.45, -1.38))
        return VGroup(barras, s_, rotulos, veredito, rot), fundos

    def w_esfera(self, p_atual):
        C, k, R = P(6.45, -2.3), 0.80, 1.0
        corpo = Circle(radius=k * R).move_to(C).set_stroke(BLUE_L, 3).set_fill("#267BFF", 0.4)
        cargas = VGroup(*[Circle(radius=0.025).move_to(C + k * R * 0.8 * q * U(a)).set_stroke(width=0).set_fill(BLUE_L, 0.9)
                          for q, a in ((0.3, 20), (0.6, 100), (0.9, 190), (0.5, 260), (0.75, 320), (0.2, 150), (0.85, 60), (0.45, 230))])

        def E(u):
            return u if u <= 1 else 1 / u ** 2
        gauss = always_redraw(lambda: VGroup(
            Circle(radius=k * p_atual()).move_to(C).set_stroke(width=0).set_fill(VIOLET, 0.07),
            DashedVMobject(Circle(radius=k * p_atual()).move_to(C), num_dashes=44, dashed_ratio=0.6).set_stroke(VIOLET, 3, 0.95),
            DashedLine(C, C + k * p_atual() * U(-38), dash_length=0.06).set_stroke(VIOLET, 2.5, 0.95),
            eq("r", size=28, color=VIOLET).move_to(C + k * p_atual() * 0.5 * U(-38) + 0.2 * U(-128)),
            *[Arrow(C + k * p_atual() * U(45 * i + 20), C + (k * p_atual() + 0.55 * E(p_atual())) * U(45 * i + 20), buff=0, stroke_width=3, tip_length=0.1, color=CYAN)
              for i in range(8) if 0.55 * E(p_atual()) > 0.05]).set_z_index(5))
        marcaR = VGroup(Line(C, C + k * R * U(110)).set_stroke(BLUE_L, 2, 0.9), eq("R", size=26, color=BLUE_L).move_to(C + k * R * 0.55 * U(110) + 0.18 * U(200)))
        rot = text("corte transversal", 18, WHITE, 0.6).move_to(C + P(0, 1.45))
        return VGroup(corpo, cargas, marcaR, rot), [gauss]
