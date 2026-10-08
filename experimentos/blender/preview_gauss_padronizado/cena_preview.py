"""Preview comparativo (sandbox, fora do yt_0002): os casos de Gauss no padrão híbrido do coaxial v2 — 3D no Blender, leitura em Manim.

Cada caso: sequência de PNG com alpha do Blender (render_casos.py) + região ativa, Q_env, E, nota, gráfico E(p) com marcador e um corte 2D
sincronizado, todos ligados ao MESMO ValueTracker que escolhe o quadro 3D. Carga + em azul, − em magenta, envolvida em violeta claro.

Rodar, a partir da raiz do repositório (antes: render_casos.py --caso todos):
    uv run python -m manim -r 960,540 --fps 15 --media_dir media/preview_gauss_padronizado experimentos/blender/preview_gauss_padronizado/cena_preview.py PreviewGaussPadronizado
"""

import sys
from pathlib import Path

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UL, UP, Annulus, Axes, Circle, DashedLine, DashedVMobject, FadeIn, FadeOut, Group, ImageMobject, Line, Rectangle, Scene,
    ValueTracker, VGroup, VMobject, always_redraw, smooth,
)

HERE = Path(__file__).resolve().parent
RAIZ = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "teste_gauss_coaxial"))
from casos import CASOS, ORDEM, PASTA_SEQ, RES  # noqa: E402
from cena_manim import (  # noqa: E402  (helpers da v1 do coaxial; ela não é alterada)
    BACKGROUND_COLOR, BLUE_L, CYAN, RL, VIOLET, WHITE, P, Sequencia, col, eq, painel_3d, text,
)

MAG, ENV = "#EA63FF", "#D6CCFF"
PX = lambda px, py: P(-3.3 + (px / 1120 - 0.5) * 9.0, -0.2 + (0.5 - py / 784) * 6.3)       # pixel do quadro 3D → cena
Q_ENV = r"Q_{\mathrm{env}}"
ZERO = lambda: eq("E", "=0", size=50, colors={0: CYAN})


def mix(*pedacos, size=24, cor=WHITE, op=0.92):
    return VGroup(*[text(q, size, cor, op) if isinstance(q, str) else q for q in pedacos]).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)


def frac(num, den, esq="E"):
    return lambda: eq(esq, "=", rf"\frac{{{num}}}{{{den}}}", size=50, colors={0: CYAN})


# cada região: (condição em p, domínio, Q_env, fábrica de E, nota)
UI = {
    "linha": dict(
        titulo=["LINHA INFINITA ·", eq(r"+\lambda", size=28, color=BLUE_L)], leg=["pos"],
        reg=[(lambda p: True, r"r>0", Q_ENV + r"=\lambda L", frac(r"\lambda", r"2\pi\varepsilon_0 r"), "a área cresce; a carga envolvida, não")],
        E=lambda p: 0.5 / p, marcas=[], widget=dict(tipo="radial", fontes=[("ponto",)]),
        plano=[(1.0, 1.8, 0.8), (1.9, 1.8, 1.0)]),
    "casca_cil": dict(
        titulo=["CASCA CILÍNDRICA ·", eq(r"+\lambda", size=28, color=BLUE_L)], leg=["pos"],
        reg=[(lambda p: p < 1.0 - 1e-3, r"r<R", Q_ENV + "=0", ZERO, "por dentro: nada envolvido"),
             (lambda p: p >= 1.0 - 1e-3, r"r>R", Q_ENV + r"=\lambda L", frac(r"\lambda", r"2\pi\varepsilon_0 r"), "por fora: igual à linha")],
        E=lambda p: 0.0 if p < 1 else 1 / p, marcas=[(1.0, "R")], widget=dict(tipo="radial", fontes=[("anel", 1.0, BLUE_L)]),
        plano=[(1.5, 2.2, 1.6)]),
    "macico_cil": dict(
        titulo=["CILINDRO MACIÇO ·", eq(r"\rho", size=28, color=BLUE_L), "constante"], leg=["pos", "env"],
        reg=[(lambda p: p < 1.0 - 1e-3, r"r<R", Q_ENV + r"=\rho\pi r^{2}L", frac(r"\rho r", r"2\varepsilon_0"), "a carga envolvida cresce com r²"),
             (lambda p: p >= 1.0 - 1e-3, r"r>R", Q_ENV + r"=\rho\pi R^{2}L", frac(r"\rho R^{2}", r"2\varepsilon_0 r"), "fora do corpo: carga envolvida fixa")],
        E=lambda p: p if p <= 1 else 1 / p, marcas=[(1.0, "R")], widget=dict(tipo="radial", fontes=[("disco", 1.0, BLUE_L)]),
        plano=[(1.0, 1.8, 0.8), (1.8, 1.8, 1.4)]),
    "coax": dict(
        titulo=["CABO COAXIAL ·", eq(r"+\lambda", size=28, color=BLUE_L), "e", eq(r"-\lambda", size=28, color=MAG)], leg=["pos", "neg"],
        reg=[(lambda p: p < 0.5 - 1e-3, r"r<a", Q_ENV + "=0", ZERO, "dentro do metal: nada envolvido"),
             (lambda p: 0.5 - 1e-3 <= p <= 1.5 + 1e-3, r"a<r<b", Q_ENV + r"=\lambda L", frac(r"\lambda", r"2\pi\varepsilon_0 r"), "o campo existe só no vão"),
             (lambda p: p > 1.5 + 1e-3, r"r>b", Q_ENV + r"=(\lambda-\lambda)L=0", ZERO, "cargas opostas: campo confinado")],
        E=lambda p: 0.5 / p if 0.5 < p < 1.5 else 0.0, marcas=[(0.5, "a"), (1.5, "b")],
        widget=dict(tipo="radial", fontes=[("nucleo", 0.5, BLUE_L), ("casca", 1.5, MAG)], vao=(0.5, 1.5)),
        plano=[(1.0, 2.0, 1.2), (1.75, 2.0, 1.2)]),
    "folha": dict(
        titulo=["FOLHA INFINITA ·", eq(r"+\sigma", size=28, color=BLUE_L)], leg=["pos", "env"],
        reg=[(lambda p: True, r"x>0", Q_ENV + r"=\sigma A", frac(r"\sigma", r"2\varepsilon_0"), "as tampas se afastam: E não muda")],
        E=lambda p: 0.8, marcas=[], widget=dict(tipo="lateral", barras=[(0.0, 0.03, BLUE_L)], caixa=lambda p: (-p, p)),
        plano=[(1.6, 2.4, 1.2)]),
    "placa": dict(
        titulo=["PLACA COM ESPESSURA ·", eq(r"\rho", size=28, color=BLUE_L)], leg=["pos", "env"],
        reg=[(lambda p: p < 0.7 - 1e-3, r"0<x<a", Q_ENV + r"=2\rho xA", frac(r"\rho x", r"\varepsilon_0", "E_x"), "a carga envolvida cresce com x"),
             (lambda p: p >= 0.7 - 1e-3, r"x>a", Q_ENV + r"=2\rho aA", frac(r"\rho a", r"\varepsilon_0", "E_x"), "fora da placa: campo constante")],
        E=lambda p: min(p / 0.7, 1.0) * 0.9, marcas=[(0.7, "a")], widget=dict(tipo="lateral", barras=[(0.0, 0.7, BLUE_L)], caixa=lambda p: (-p, p)),
        plano=[(0.55, 1.5, 0.8), (1.8, 2.0, 1.2)]),
    "duas": dict(
        titulo=["DUAS FOLHAS ·", eq(r"+\sigma", size=28, color=BLUE_L), "e", eq(r"-\sigma", size=28, color=MAG)], leg=["pos", "neg", "env"],
        reg=[(lambda p: p < -1.1, r"x<-d", Q_ENV + "=0", ZERO, "a gaussiana ainda não envolve carga"),
             (lambda p: -1.1 <= p <= 1.1, r"-d<x<d", Q_ENV + r"=\sigma A", frac(r"\sigma", r"\varepsilon_0"), "entre as folhas: os campos somam"),
             (lambda p: p > 1.1, r"x>d", Q_ENV + r"=(\sigma-\sigma)A=0", ZERO, "fora: se cancelam")],
        E=lambda p: 0.9 if -1.1 < p < 1.1 else 0.0, marcas=[(-1.1, "-d"), (1.1, "d")],
        widget=dict(tipo="lateral", barras=[(-1.1, 0.04, BLUE_L), (1.1, 0.04, MAG)], caixa=lambda p: (-1.9, max(p, -1.72))),
        plano=[(0.0, 2.0, 1.2), (1.7, 2.0, 1.2)]),
    "face": dict(
        titulo=["FACE DE CONDUTOR ·", eq(r"\sigma_{\mathrm{face}}", size=28, color=BLUE_L)], leg=["pos", "env"],
        reg=[(lambda p: True, r"x>0", Q_ENV + r"=\sigma_{\mathrm{face}}A", frac(r"\sigma_{\mathrm{face}}", r"\varepsilon_0", r"E_{\mathrm{fora}}"),
              "só a tampa de fora contribui")],
        E=lambda p: 0.9 if p > 0 else 0.0, xplot=(-0.7, 1.8), marcas=[(0.0, "0")],
        widget=dict(tipo="lateral", barras=[(-0.85, 0.85, "#26345A"), (0.0, 0.03, BLUE_L)], caixa=lambda p: (-0.75, p)),
        plano=[(1.5, 2.4, 1.4)]),
    "casca_esf": dict(
        titulo=["CASCA ESFÉRICA ·", eq(r"+Q", size=28, color=BLUE_L)], leg=["pos"],
        reg=[(lambda p: p < 1.0 - 1e-3, r"r<R", Q_ENV + "=0", ZERO, "por dentro: nada envolvido"),
             (lambda p: p >= 1.0 - 1e-3, r"r>R", Q_ENV + "=Q", frac("Q", r"4\pi\varepsilon_0 r^{2}"), "por fora: como carga pontual")],
        E=lambda p: 0.0 if p < 1 else 1 / p ** 2, marcas=[(1.0, "R")], widget=dict(tipo="radial", fontes=[("anel", 1.0, BLUE_L)]),
        plano=[(1.6, 2.2, 1.6)]),
    "macico_esf": dict(
        titulo=["ESFERA MACIÇA ·", eq(r"\rho", size=28, color=BLUE_L), "constante"], leg=["pos", "env"],
        reg=[(lambda p: p < 1.0 - 1e-3, r"r<R", Q_ENV + r"=\frac{4}{3}\pi\rho r^{3}", frac(r"\rho r", r"3\varepsilon_0"), "a carga envolvida cresce com r³"),
             (lambda p: p >= 1.0 - 1e-3, r"r>R", Q_ENV + r"=\frac{4}{3}\pi\rho R^{3}", frac(r"\rho R^{3}", r"3\varepsilon_0 r^{2}"), "fora do corpo: carga envolvida fixa")],
        E=lambda p: p if p <= 1 else 1 / p ** 2, marcas=[(1.0, "R")], widget=dict(tipo="radial", fontes=[("disco", 1.0, BLUE_L)]),
        plano=[(1.0, 1.8, 0.8), (1.8, 1.8, 1.4)]),
    "cap_esf": dict(
        titulo=["CAPACITOR ESFÉRICO ·", eq(r"+Q", size=28, color=BLUE_L), "e", eq(r"-Q", size=28, color=MAG)], leg=["pos", "neg"],
        reg=[(lambda p: p < 0.8 - 1e-3, r"r<a", Q_ENV + "=0", ZERO, "dentro do metal: nada envolvido"),
             (lambda p: 0.8 - 1e-3 <= p <= 1.6 + 1e-3, r"a<r<b", Q_ENV + "=Q", frac("Q", r"4\pi\varepsilon_0 r^{2}"), "o campo existe só no vão"),
             (lambda p: p > 1.6 + 1e-3, r"r>b", Q_ENV + "=Q-Q=0", ZERO, "cargas opostas: campo confinado")],
        E=lambda p: (0.8 / p) ** 2 if 0.8 < p < 1.6 else 0.0, marcas=[(0.8, "a"), (1.6, "b")],
        widget=dict(tipo="radial", fontes=[("nucleo", 0.8, BLUE_L), ("casca", 1.6, MAG)], vao=(0.8, 1.6)),
        plano=[(1.2, 2.0, 1.2), (1.85, 2.0, 1.2)]),
}
LEG = {"pos": (BLUE_L, "carga +"), "neg": (MAG, "carga −"), "env": (ENV, "carga envolvida")}
C = P(6.7, -2.45)                                         # centro do corte 2D


class PreviewGaussPadronizado(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.abertura()
        for cid in ORDEM:
            self.caso(cid)
        self.fechamento()

    # ── abertura e fechamento ───────────────────────────────────────────────
    def abertura(self):
        t = text("LEI DE GAUSS · PADRÃO HÍBRIDO", 36, WHITE).move_to(P(0, 1.2))
        s = text("geometria no Blender · leitura física em Manim", 26, CYAN, 0.9).move_to(P(0, 0.5))
        chaves = VGroup(*[VGroup(Circle(radius=0.08).set_stroke(width=0).set_fill(c, 1), text(n, 22, WHITE, 0.9)).arrange(RIGHT, buff=0.15)
                          for c, n in ((BLUE_L, "carga +"), (MAG, "carga −"), (ENV, "carga envolvida"), (VIOLET, "gaussiana"), (CYAN, "campo E"))]
                         ).arrange(RIGHT, buff=0.5).move_to(P(0, -0.6))
        aviso = text("preview experimental · não substitui o vídeo principal", 20, WHITE, 0.55).move_to(P(0, -2.2))
        self.play(FadeIn(t, shift=0.1 * UP), FadeIn(s), run_time=0.9)
        self.play(FadeIn(chaves), FadeIn(aviso), run_time=0.8)
        self.wait(2.2)
        self.play(FadeOut(VGroup(t, s, chaves, aviso)), run_time=0.5)

    def fechamento(self):
        cartoes = []
        for cid, f, nome, pos in (("linha", 0.55, "simetria cilíndrica", -4.7), ("folha", 0.55, "simetria planar", 0.0), ("macico_esf", 0.75, "simetria esférica", 4.7)):
            seq = Sequencia(RAIZ / PASTA_SEQ / cid / RES)
            m = ImageMobject(seq.quadro(int(f * (seq.n - 1)))).set_width(4.3).move_to(P(pos, 0.5))
            cartoes.append(Group(m, text(nome, 24, WHITE, 0.92).move_to(P(pos, -1.45))))
        titulo = text("mesma Lei, o mesmo método", 36, WHITE).move_to(P(0, 3.0))
        passos = mix("simetria", eq(r"\rightarrow", size=30), "gaussiana", eq(r"\rightarrow", size=30), eq(Q_ENV, size=34, color=BLUE_L),
                     eq(r"\rightarrow", size=30), eq("E", size=34, color=CYAN), size=28).move_to(P(0, -2.6))
        self.play(FadeIn(titulo, shift=0.1 * UP), *[FadeIn(g) for g in cartoes], run_time=1.0)
        self.play(FadeIn(passos), run_time=0.8)
        self.wait(3.5)
        self.play(FadeOut(Group(titulo, passos, *cartoes)), run_time=0.6)

    # ── um caso ─────────────────────────────────────────────────────────────
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

        # gráfico E(p): marcador no mesmo p do quadro 3D
        xa, xb = ui.get("xplot", (p0, p1))
        ax = Axes(x_range=[xa, xb, 1], y_range=[0, 1.25, 1], x_length=3.3, y_length=1.9, tips=False,
                  axis_config={"color": WHITE, "stroke_width": 2, "include_ticks": False, "stroke_opacity": 0.8})
        ax.shift(P(RL + 0.45, -3.55) - ax.c2p(xa, 0))
        E = ui["E"]
        curva = VMobject().set_points_as_corners([ax.c2p(x, E(x)) for x in np.linspace(xa + 1e-3, xb, 220)]).set_stroke(CYAN, 4)
        marcas = VGroup(*[eq(n, size=28, color=BLUE_L).move_to(ax.c2p(v, 0) + P(0, -0.3)) for v, n in ui["marcas"]],
                        eq("E", size=32, color=CYAN).move_to(ax.c2p(xa, 1.25) + P(0.25, 0.05)))
        guias = VGroup(*[DashedLine(ax.c2p(v, 0), ax.c2p(v, 1.0), dash_length=0.07).set_stroke(VIOLET, 1.8, 0.45) for v, _ in ui["marcas"]])
        marcador = always_redraw(lambda: Circle(radius=0.1).move_to(ax.c2p(p_atual(), E(p_atual()))).set_stroke(WHITE, 2).set_fill(CYAN, 1).set_z_index(6))
        linha_p = always_redraw(lambda: DashedLine(ax.c2p(p_atual(), 0), ax.c2p(p_atual(), E(p_atual())), dash_length=0.07).set_stroke(VIOLET, 2.5, 0.9))

        corte, dinamico = self.corte(ui["widget"], p_atual, p1)
        legenda = self.legenda(ui["leg"])

        img = painel_3d(seq, s)
        img.set_opacity(0.0)
        self.add(img)
        estatico = VGroup(titulo, ax, curva, marcas, guias, corte, legenda)
        self.play(img.animate.set_opacity(1.0), FadeIn(estatico), run_time=0.7)
        self.add(*regioes, marcador, linha_p, *dinamico)
        self.wait(1.0)
        for alvo, mover, parar in ui["plano"]:
            self.play(s.animate.set_value(s_de(alvo)), run_time=mover, rate_func=smooth)
            self.wait(parar)
        for m in (marcador, linha_p, *regioes, *dinamico):          # congela o estado final: o fade-out não é desfeito pelos updaters
            m.clear_updaters()
        self.play(FadeOut(Group(img, estatico, *regioes, marcador, linha_p, *dinamico)), run_time=0.4)
        img.clear_updaters()
        self.remove(img, marcador, linha_p, *regioes, *dinamico)

    def legenda(self, chaves):
        itens = [VGroup(Circle(radius=0.07).set_stroke(width=0).set_fill(LEG[k][0], 1), text(LEG[k][1], 18, WHITE, 0.85)).arrange(RIGHT, buff=0.12)
                 for k in chaves]
        itens.append(VGroup(Line(P(0, 0), P(0.3, 0)).set_stroke(CYAN, 3), text("campo E", 18, WHITE, 0.85)).arrange(RIGHT, buff=0.12))
        return VGroup(*itens).arrange(RIGHT, buff=0.45).move_to(P(-3.3, -3.85))

    def corte(self, w, p_atual, p1):
        """Corte 2D sincronizado: radial (círculos concêntricos) ou lateral (barras + pillbox). Devolve (estático, dinâmicos)."""
        if w["tipo"] == "radial":
            k = 0.8 / p1
            est = VGroup()
            if "vao" in w:
                a, b = w["vao"]
                vao = Annulus(inner_radius=k * a, outer_radius=k * b).move_to(C).set_stroke(width=0).set_fill(CYAN, 0.0)
                vao.add_updater(lambda m: m.set_fill(CYAN, 0.16 if a - 1e-3 <= p_atual() <= b + 1e-3 else 0.0))
            for f in w["fontes"]:
                if f[0] == "ponto":
                    est.add(Circle(radius=0.07).move_to(C).set_stroke(BLUE_L, 2).set_fill(BLUE_L, 1))
                elif f[0] in ("disco", "nucleo"):
                    est.add(Circle(radius=k * f[1]).move_to(C).set_stroke(f[2], 3).set_fill("#267BFF", 0.4))
                else:
                    est.add(Annulus(inner_radius=k * (f[1] - 0.07), outer_radius=k * f[1]).move_to(C).set_stroke(f[2], 2).set_fill(f[2], 0.55))
            gauss = always_redraw(lambda: VGroup(
                Circle(radius=k * p_atual()).move_to(C).set_stroke(width=0).set_fill(VIOLET, 0.07),
                DashedVMobject(Circle(radius=k * p_atual()).move_to(C), num_dashes=40, dashed_ratio=0.6).set_stroke(VIOLET, 3, 0.95),
                DashedLine(C, C + k * p_atual() * P(np.cos(-0.5), np.sin(-0.5)), dash_length=0.06).set_stroke(VIOLET, 2.5, 0.9)).set_z_index(5))
            rot = text("corte transversal", 18, WHITE, 0.6).move_to(C + P(0, 1.3))
            return VGroup(est, rot), ([gauss] + ([vao] if "vao" in w else []))
        ks = 0.45                                            # lateral: x ∈ [−2.2, 2.2] → 2 unidades
        est = VGroup(Line(C + P(-1.0, -0.65), C + P(1.0, -0.65)).set_stroke(WHITE, 1.5, 0.5))
        for x, hw, cor in w["barras"]:
            r = Rectangle(width=max(2 * hw * ks, 0.05), height=1.1).move_to(C + P(x * ks, 0)).set_stroke(cor if cor != "#26345A" else BLUE_L, 2, 0.9)
            r.set_fill(cor, 0.5 if cor == "#26345A" else 0.35)
            est.add(r)
        caixa = always_redraw(lambda: self._caixa2d(w["caixa"](p_atual()), ks))
        rot = text("vista lateral", 18, WHITE, 0.6).move_to(C + P(0, 1.0))
        return VGroup(est, rot), [caixa]

    @staticmethod
    def _caixa2d(par, ks):
        xl, xr = par
        r = Rectangle(width=max((xr - xl) * ks, 0.05), height=0.7).move_to(C + P((xl + xr) / 2 * ks, 0))
        r.set_stroke(VIOLET, 3, 0.95).set_fill(VIOLET, 0.1).set_z_index(5)
        return r
