"""Coaxial 3D + corte 2D ampliado (sandbox, fora do yt_0002): 3D do Blender permanente + corte transversal em Manim com a gaussiana e as setas que a acompanham.

O quadro do vídeo k (30 fps) mostra a imagem do Blender para r(k) (trajetória única, a do coaxial limpo); o texto da região e o corte 2D usam o MESMO r(k).
No corte 2D: setas do campo existente no vão (discretas e fixas) e, com a gaussiana no vão, um anel de setas na própria circunferência gaussiana, com comprimento
∝ 1/r (as setas se afastam do eixo e encurtam); fora do vão (E = 0) o anel some e as setas do vão ficam em destaque. Sem gráfico.

    uv run python -m manim -r 960,540 --fps 30 --media_dir media/preview_coaxial_3d_2d experimentos/blender/preview_coaxial_3d_2d/cena_3d2d.py Coaxial3D2D
"""

import sys
from collections import OrderedDict
from pathlib import Path

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, Annulus, Arrow, Circle, DashedLine, DashedVMobject, FadeIn, FadeOut, ImageMobject, Line, Scene, VGroup, always_redraw, config,
)
from PIL import Image

HERE = Path(__file__).resolve().parent
RAIZ = HERE.parents[2]
sys.path.insert(0, str(HERE.parent / "preview_coaxial_3d_limpo"))
sys.path.insert(0, str(HERE.parent / "teste_gauss_coaxial"))
import trajetoria as T  # noqa: E402  (a mesma trajetória do coaxial limpo e do Blender)
from cena_manim import BACKGROUND_COLOR, BLUE_L, CYAN, VIOLET, WHITE, P, eq, text  # noqa: E402  (helpers da v1; ela não é alterada)

MAG = "#EA63FF"
PASTA = RAIZ / "renders" / "preview_coaxial_3d_2d" / "1120x784"
PASTA_COROA = RAIZ / "renders" / "preview_coaxial_3d_2d" / "1120x784_coroa"
RL, XMAX = 1.9, 6.95
A, B = T.A, T.B
Q_ENV = r"Q_{\mathrm{env}}"
C, K = P(5.2, -2.65), 0.90                                 # centro e escala do corte (raio da casca = K·b; gaussiana máxima K·1,9 ≈ 1,5)
K_E, FOLGA = 0.34, 0.10                                    # |E| ∝ K_E / r; folga até a casca (mesmos valores do Blender)
U = lambda g: P(np.cos(np.radians(g)), np.sin(np.radians(g)))      # noqa: E731


def comprimento(r):
    return min(K_E / r, B - FOLGA - r)


def mix(*pedacos, size=24, cor=WHITE, op=0.92):
    return VGroup(*[text(q, size, cor, op) if isinstance(q, str) else q for q in pedacos]).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)


def sinal(txt, cor, pos):
    """Marcador esquemático de carga (+ ou −): traços sobre um disco do fundo; não é uma contagem de cargas."""
    s_ = 0.085
    fundo = Circle(radius=0.14).move_to(pos).set_stroke(width=0).set_fill(BACKGROUND_COLOR, 0.9)
    tr = [Line(pos + P(-s_, 0), pos + P(s_, 0)).set_stroke(cor, 4)]
    if txt == "+":
        tr.append(Line(pos + P(0, -s_), pos + P(0, s_)).set_stroke(cor, 4))
    return VGroup(fundo, *tr).set_z_index(8)


class Coaxial3D2D(Scene):
    COROA = False                                          # True: quadros do Blender com coroas (frente + fundo) e sem o campo existente de dentro

    def construct(self):
        pasta = PASTA_COROA if self.COROA else PASTA
        assert config.frame_rate == T.FPS, f"use --fps {T.FPS}"
        self.camera.background_color = BACKGROUND_COLOR
        cache = OrderedDict()
        estado = {"t0": 0.0}

        def k_atual():
            return min(max(int(round((self.time - estado["t0"]) * T.FPS)), 0), T.TOTAL - 1)

        def r_atual():
            return T.r_em_quadro(k_atual())               # None na introdução (sem gaussiana)

        def no_vao():
            r = r_atual()
            return r is not None and A - 1e-3 <= r <= B + 1e-3

        def quadro(k):
            nome = pasta / f"q_{T.chave(k)}.png"
            if nome not in cache:
                cache[nome] = np.array(Image.open(nome).convert("RGBA"))
                while len(cache) > 24:
                    cache.popitem(last=False)
            return cache[nome]

        img = ImageMobject(quadro(0)).set_width(9.0).move_to(P(-3.0, -0.15))
        img.set_opacity(0.0)
        estado["k"] = 0

        # ── texto por região ────────────────────────────────────────────────
        def bloco(dom, q, e, nota):
            d = eq(dom, size=34, color=VIOLET).move_to(P(0, 1.55)).align_to(P(RL, 0), LEFT)
            qq = eq(q, size=40).move_to(P(0, 1.55)).align_to(P(max(RL + 1.85, d.get_right()[0] + 0.4), 0), LEFT)
            ee = e.move_to(P(0, 0.4)).align_to(P(RL, 0), LEFT)
            nt = text(nota, 22, WHITE, 0.92).move_to(P(0, -0.55)).align_to(P(RL, 0), LEFT)
            return VGroup(d, qq, ee, nt)
        regs = [(lambda r: r < A - 1e-3, bloco(r"r<a", Q_ENV + "=0", eq("E", "=0", size=50, colors={0: CYAN}), "dentro do metal: nada envolvido")),
                (lambda r: A - 1e-3 <= r <= B + 1e-3, bloco(r"a<r<b", Q_ENV + r"=\lambda L",
                                                            eq("E", "=", r"\frac{\lambda}{2\pi\varepsilon_0 r}", size=50, colors={0: CYAN}), "o campo radial existe só no vão")),
                (lambda r: r > B + 1e-3, bloco(r"r>b", Q_ENV + r"=(\lambda-\lambda)L=0", eq("E", "=0", size=50, colors={0: CYAN}), "fora, no modelo ideal: E = 0"))]
        titulo = mix("CABO COAXIAL ·", eq(r"+\lambda", size=28, color=BLUE_L), "e", eq(r"-\lambda", size=28, color=MAG)).move_to(P(0, 2.9)).align_to(P(RL, 0), LEFT)

        # ── corte transversal 2D (ampliado) ────────────────────────────────
        nuc = Circle(radius=K * A).move_to(C).set_stroke(BLUE_L, 3).set_fill("#1B4DB5", 0.5)
        cas = Circle(radius=K * B).move_to(C).set_stroke(BLUE_L, 5)
        sinais = VGroup(*[sinal("+", BLUE_L, C + K * A * U(45 * i)) for i in range(8)],
                        *[sinal("-", MAG, C + (K * B - 0.16) * U(45 * i + 22.5)) for i in range(8)])
        marcas = VGroup(Line(C + K * A * 0.12 * U(90), C + K * A * U(90)).set_stroke(BLUE_L, 2, 0.9), eq("a", size=30, color=BLUE_L).move_to(C + (K * A + 0.2) * U(90)),
                        Line(C + K * A * U(140), C + K * B * U(140)).set_stroke(MAG, 2, 0.9), eq("b", size=30, color=MAG).move_to(C + (K * B + 0.27) * U(140)))
        vao = Annulus(inner_radius=K * A, outer_radius=K * B).move_to(C).set_stroke(width=0).set_fill(CYAN, 0.0)
        vao.add_updater(lambda m: m.set_fill(CYAN, 0.08 if no_vao() else 0.0))
        # campo existente no vão: 8 setas iguais, radiais (discretas quando a gaussiana está no vão; em destaque fora dele)
        ra, rb = 0.70, 1.10
        existente = VGroup(*[Arrow(C + K * ra * U(22.5 + 45 * i), C + K * rb * U(22.5 + 45 * i), buff=0, stroke_width=3.5, tip_length=0.16, color=CYAN) for i in range(8)])
        existente.add_updater((lambda m: m.set_stroke(opacity=0.0 if no_vao() else 0.95)) if self.COROA else (lambda m: m.set_stroke(opacity=0.35 if no_vao() else 0.95)))

        def gauss():
            r = r_atual()
            if r is None:
                return VGroup()
            g = VGroup(Circle(radius=K * r).move_to(C).set_stroke(width=0).set_fill(VIOLET, 0.06),
                       DashedVMobject(Circle(radius=K * r).move_to(C), num_dashes=56, dashed_ratio=0.55).set_stroke(VIOLET, 4, 0.95),
                       DashedLine(C, C + K * r * U(-35), dash_length=0.07).set_stroke(VIOLET, 2.5, 0.95),
                       eq("r", size=32, color=VIOLET).move_to(C + K * r * 0.5 * U(-35) + 0.24 * U(-125)))
            if no_vao() and comprimento(r) >= 0.04:                  # anel de setas na própria gaussiana (campo avaliado), ∝ 1/r
                g.add(*[Arrow(C + K * r * U(30 * i + 15), C + K * (r + comprimento(r)) * U(30 * i + 15), buff=0, stroke_width=4, tip_length=0.15, color=CYAN)
                        for i in range(12)])
            return g.set_z_index(6)
        gauss_mob = always_redraw(gauss)
        corte = VGroup(nuc, cas, sinais, marcas)

        def atualiza(m, dt=0):
            """Imagem do quadro k atual e texto da região, ambos do tempo da cena (não de dt acumulado)."""
            k = k_atual()
            if k != estado["k"] or m.stroke_opacity < 1:
                estado["k"] = k
                arr = quadro(k)
                m.pixel_array = arr.copy()
                m.orig_alpha_pixel_array = arr[:, :, 3]
                if m.stroke_opacity < 1:
                    m.pixel_array[:, :, 3] = (arr[:, :, 3] * m.stroke_opacity).astype(m.pixel_array.dtype)
            r = r_atual()
            for cond, g in regs:
                g.set_opacity(0.0 if r is None else (1.0 if cond(r) else 0.0))

        img.add_updater(atualiza)
        for _, g in regs:
            g.set_opacity(0.0)
        self.add(img, vao, *[g for _, g in regs])
        self.play(img.animate.set_opacity(1.0), FadeIn(titulo), FadeIn(corte), FadeIn(existente), run_time=0.8)
        self.add(gauss_mob)
        estado["t0"] = self.time
        self.wait(T.TOTAL / T.FPS)                            # a trajetória completa: intro, pausas e as passagens por a e b
        img.remove_updater(atualiza)
        gauss_mob.clear_updaters()
        vao.clear_updaters()
        existente.clear_updaters()
        self.play(FadeOut(VGroup(titulo, corte, existente, vao, gauss_mob, *[g for _, g in regs])), img.animate.set_opacity(0.0), run_time=0.6)


class Coaxial3D2DCoroa(Coaxial3D2D):
    """Mesmo corte 2D e mesma trajetória; o 3D usa as coroas (frente + fundo, por fora) e o campo existente de dentro some."""
    COROA = True
