"""Coaxial 3D limpo (sandbox, fora do yt_0002): o 3D do Blender fica na tela durante TODA a explicação; o Manim só põe título, r/região, Q_env e E(r).

A trajetória de r vem de trajetoria.py (a mesma do Blender): o quadro do vídeo k (30 fps) mostra a imagem renderizada para r(k). Nada de dissolução
entre imagens: durante o movimento há uma imagem por quadro; nas pausas, a mesma imagem. O texto da região usa o MESMO r(k).

    uv run python -m manim -r 960,540 --fps 30 --media_dir media/preview_coaxial_3d_limpo experimentos/blender/preview_coaxial_3d_limpo/cena_limpo.py CoaxialLimpo
"""

import sys
from collections import OrderedDict
from pathlib import Path

import numpy as np
from manim import DOWN, LEFT, RIGHT, UL, UP, FadeIn, FadeOut, ImageMobject, Scene, VGroup, config
from PIL import Image

HERE = Path(__file__).resolve().parent
RAIZ = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "teste_gauss_coaxial"))
import trajetoria as T  # noqa: E402
from cena_manim import BACKGROUND_COLOR, BLUE_L, CYAN, VIOLET, WHITE, P, eq, text  # noqa: E402  (helpers da v1; ela não é alterada)

MAG = "#EA63FF"
PASTA = RAIZ / "renders" / "preview_coaxial_3d_limpo" / "1120x784"
RL = 1.9
A, B = T.A, T.B
Q_ENV = r"Q_{\mathrm{env}}"


def mix(*pedacos, size=24, cor=WHITE, op=0.92):
    return VGroup(*[text(q, size, cor, op) if isinstance(q, str) else q for q in pedacos]).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)


class CoaxialLimpo(Scene):
    def construct(self):
        assert config.frame_rate == T.FPS, f"use --fps {T.FPS}: a trajetória foi renderizada para {T.FPS} fps"
        self.camera.background_color = BACKGROUND_COLOR
        cache = OrderedDict()

        def quadro(k):
            nome = PASTA / f"q_{T.chave(k)}.png"
            if nome not in cache:
                cache[nome] = np.array(Image.open(nome).convert("RGBA"))
                while len(cache) > 24:
                    cache.popitem(last=False)
            return cache[nome]

        img = ImageMobject(quadro(0)).set_width(9.0).move_to(P(-3.0, -0.15))
        estado = {"k": 0, "t0": 0.0}                      # k = índice do quadro da animação; t0 = instante (cena) em que a animação começa
        img.set_opacity(0.0)

        # texto por região (só a região atual aparece); a região vem de r(k), o mesmo valor que o Blender renderizou
        def bloco(dom, q, e, nota):
            d = eq(dom, size=34, color=VIOLET).move_to(P(0, 1.55)).align_to(P(RL, 0), LEFT)
            qq = eq(q, size=40).move_to(P(0, 1.55)).align_to(P(RL + 1.85, 0), LEFT)
            ee = e.move_to(P(0, 0.4)).align_to(P(RL, 0), LEFT)
            nt = text(nota, 22, WHITE, 0.92).move_to(P(0, -0.55)).align_to(P(RL, 0), LEFT)
            return VGroup(d, qq, ee, nt)
        regs = [(lambda r: r < A - 1e-3, bloco(r"r<a", Q_ENV + "=0", eq("E", "=0", size=50, colors={0: CYAN}), "dentro do metal: nada envolvido")),
                (lambda r: A - 1e-3 <= r <= B + 1e-3, bloco(r"a<r<b", Q_ENV + r"=\lambda L",
                                                            eq("E", "=", r"\frac{\lambda}{2\pi\varepsilon_0 r}", size=50, colors={0: CYAN}), "o campo radial existe só no vão")),
                (lambda r: r > B + 1e-3, bloco(r"r>b", Q_ENV + r"=(\lambda-\lambda)L=0", eq("E", "=0", size=50, colors={0: CYAN}), "fora, no modelo ideal: E = 0"))]
        titulo = mix("CABO COAXIAL ·", eq(r"+\lambda", size=28, color=BLUE_L), "e", eq(r"-\lambda", size=28, color=MAG)).move_to(P(0, 2.9)).align_to(P(RL, 0), LEFT)
        a_b = mix(eq(r"a", size=30), "condutor interno ·", eq(r"b", size=30), "casca externa ideal", size=20, op=0.7).move_to(P(0, -3.55)).align_to(P(RL, 0), LEFT)

        def atualiza(m, dt=0):
            """Escolhe a imagem do quadro atual e o texto da região, a partir do tempo da cena (não de dt acumulado)."""
            t = self.time - estado["t0"]
            k = min(max(int(round(t * T.FPS)), 0), T.TOTAL - 1)
            if k != estado["k"] or m.stroke_opacity < 1:
                estado["k"] = k
                arr = quadro(k)
                m.pixel_array = arr.copy()
                m.orig_alpha_pixel_array = arr[:, :, 3]
                if m.stroke_opacity < 1:                      # preserva o FadeIn em andamento
                    m.pixel_array[:, :, 3] = (arr[:, :, 3] * m.stroke_opacity).astype(m.pixel_array.dtype)
            r = T.r_em_quadro(k)
            for cond, g in regs:
                g.set_opacity(0.0 if r is None else (1.0 if cond(r) else 0.0))

        img.add_updater(atualiza)
        for _, g in regs:
            g.set_opacity(0.0)
        self.add(img, *[g for _, g in regs])
        self.play(img.animate.set_opacity(1.0), FadeIn(titulo), FadeIn(a_b), run_time=0.8)
        estado["t0"] = self.time                              # a animação (trajetória) começa agora; 0,8 s de fade de entrada sobre o quadro 0
        self.wait(T.TOTAL / T.FPS)                            # a trajetória completa: intro, pausas e as duas passagens por a e b
        img.remove_updater(atualiza)
        for _, g in regs:
            g.clear_updaters()
        self.play(FadeOut(VGroup(titulo, a_b, *[g for _, g in regs])), img.animate.set_opacity(0.0), run_time=0.6)
