"""Coaxial 3D v2 (sandbox, fora do yt_0002): 3D do Blender + texto, fórmulas, gráfico e corte transversal 2D em Manim.

Painel esquerdo: sequência de render_sequencia_v2.py (câmera ortográfica fixa; quem muda é a gaussiana). Coluna direita: região,
Q_env, E(r), nota, gráfico E(r) e um pequeno corte transversal, todos ligados ao MESMO ValueTracker que escolhe o quadro 3D.

Rodar, a partir da raiz do repositório (antes gere a sequência com render_sequencia_v2.py):
    uv run python -m manim -r 960,540 --fps 15 --media_dir media/teste_blender_coaxial experimentos/blender/teste_gauss_coaxial/cena_manim_v2.py TesteCoaxial3Dv2
"""

import sys
from pathlib import Path

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UL, UP, Annulus, Axes, Circle, DashedLine, DashedVMobject, FadeIn, Line, VGroup, VMobject, ValueTracker,
    always_redraw, smooth,
)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cena_manim import (  # noqa: E402  (helpers e tracker de quadros da v1; a v1 não é alterada)
    BACKGROUND_COLOR, BLUE_L, CYAN, RL, VIOLET, WHITE, P, Sequencia, col, eq, painel_3d, text,
)
from manim import Scene  # noqa: E402

RAIZ = Path(__file__).resolve().parents[3]
PASTA = RAIZ / "renders" / "teste_gauss_coaxial_v2" / "1120x784"
PX = lambda px, py: P(-3.3 + (px / 1120 - 0.5) * 9.0, -0.2 + (0.5 - py / 784) * 6.3)   # pixel do quadro 3D → coordenadas da cena


class TesteCoaxial3Dv2(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        seq = Sequencia(PASTA)
        r0, r1, a, b = (seq.meta[k] for k in ("r0", "r1", "a", "b"))
        s = ValueTracker(0.0)
        s_de = lambda r: (r - r0) / (r1 - r0)
        r_atual = lambda: r0 + s.get_value() * (r1 - r0)

        header = text("TESTE · COAXIAL 3D v2 · BLENDER + MANIM", 18, opacity=0.6).to_corner(UL, buff=0.38)
        titulo = col(text("CABO COAXIAL · modelo infinito", 24, opacity=0.92), 2.95)

        # rótulos dos objetos 3D (a câmera é fixa: posições constantes no quadro) — discretos, em espaço vazio do painel
        def rotulo(linhas, pos_texto, alvo_px):
            """linhas: lista de listas de pedaços (str vira texto; MathTex fica como está). Texto alinhado à esquerda em `pos_texto`."""
            lin = [VGroup(*[text(q, 20, BLUE_L, 0.92) if isinstance(q, str) else q for q in l]).arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
                   for l in linhas]
            t = VGroup(*lin).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            t.move_to(pos_texto, aligned_edge=UL)
            ld = Line(t.get_bottom() + 0.06 * DOWN, PX(*alvo_px)).set_stroke(BLUE_L, 1.8, 0.6)
            return VGroup(t, ld)
        lam_p, lam_m = eq(r"+\lambda", size=26, color=BLUE_L), eq(r"-\lambda", size=26, color=BLUE_L)
        rot_nucleo = rotulo([["condutor interno"], [lam_p, "na superfície"]], PX(40, 60), (338, 300))
        rot_casca = rotulo([["casca condutora"], [lam_m, "na face interna"]], PX(690, 30), (640, 215))

        def bloco(dominio, q, resultado, nota):
            dom = eq(dominio, size=34, color=VIOLET)
            qq = eq(q, size=40)
            dom.move_to(P(0, 1.7)).align_to(P(RL, 0), LEFT)
            qq.move_to(P(0, 1.7)).align_to(P(RL + 1.9, 0), LEFT)
            return VGroup(dom, qq, col(resultado, 0.6), col(text(nota, 24, opacity=0.92), -0.4))

        reg1 = bloco(r"r<a", r"Q_{\mathrm{env}}=0", eq("E", "=0", size=50, colors={0: CYAN}), "dentro do metal: nada envolvido")
        reg2 = bloco(r"a<r<b", r"Q_{\mathrm{env}}=\lambda L",
                     eq("E", "=", r"\frac{\lambda}{2\pi\varepsilon_0 r}", size=50, colors={0: CYAN}), "o campo existe só no vão")
        reg3 = bloco(r"r>b", r"Q_{\mathrm{env}}=(\lambda-\lambda)L=0", eq("E", "=0", size=50, colors={0: CYAN}), "cargas opostas: campo confinado")
        regioes = ((reg1, lambda r: r < a - 1e-3), (reg2, lambda r: a - 1e-3 <= r <= b + 1e-3), (reg3, lambda r: r > b + 1e-3))
        for g, cond in regioes:
            g.add_updater(lambda m, c=cond: m.set_opacity(1.0 if c(r_atual()) else 0.0))
            g.update()

        # gráfico E(r)
        ax = Axes(x_range=[0, r1 * 1.05, 1], y_range=[0, 1.25, 1], x_length=3.3, y_length=1.9, tips=False,
                  axis_config={"color": WHITE, "stroke_width": 2, "include_ticks": False, "stroke_opacity": 0.8})
        ax.shift(P(RL + 0.45, -3.55) - ax.c2p(0, 0))
        E = lambda r: (a / r) if a < r < b else 0.0
        curva = VGroup(Line(ax.c2p(0, 0), ax.c2p(a, 0)), VMobject().set_points_as_corners([ax.c2p(r, E(r)) for r in np.linspace(a, b, 60)]),
                       Line(ax.c2p(b, 0), ax.c2p(r1, 0))).set_stroke(CYAN, 4)
        quedas = VGroup(DashedLine(ax.c2p(a, 0), ax.c2p(a, 1), dash_length=0.08), DashedLine(ax.c2p(b, 0), ax.c2p(b, a / b), dash_length=0.08)
                        ).set_stroke(VIOLET, 2, 0.6)
        marcas = VGroup(eq("a", size=30, color=BLUE_L).move_to(ax.c2p(a, 0) + P(0, -0.32)), eq("b", size=30, color=BLUE_L).move_to(ax.c2p(b, 0) + P(0, -0.32)),
                        eq("r", size=34, color=VIOLET).move_to(ax.c2p(r1, 0) + P(0.25, -0.3)), eq("E", size=34, color=CYAN).move_to(ax.c2p(0, 1.25) + P(0.25, 0.05)))
        marcador = always_redraw(lambda: Circle(radius=0.1).move_to(ax.c2p(r_atual(), E(r_atual()))).set_stroke(WHITE, 2).set_fill(CYAN, 1).set_z_index(6))
        linha_r = always_redraw(lambda: DashedLine(ax.c2p(r_atual(), 0), ax.c2p(r_atual(), E(r_atual())), dash_length=0.07).set_stroke(VIOLET, 2.5, 0.9))

        # corte transversal 2D: onde estou radialmente (núcleo, casca e a gaussiana atual)
        C, k = P(6.7, -2.45), 0.72 / b
        nuc = Circle(radius=k * a).move_to(C).set_stroke(BLUE_L, 3).set_fill("#267BFF", 0.4)
        casca = Annulus(inner_radius=k * (b - 0.07), outer_radius=k * b).move_to(C).set_stroke(BLUE_L, 2).set_fill("#267BFF", 0.55)
        vao = Annulus(inner_radius=k * a, outer_radius=k * (b - 0.07)).move_to(C).set_stroke(width=0).set_fill(CYAN, 0.0)
        vao.add_updater(lambda m: m.set_fill(CYAN, 0.16 if a - 1e-3 <= r_atual() <= b + 1e-3 else 0.0))
        gauss = always_redraw(lambda: VGroup(
            Circle(radius=k * r_atual()).move_to(C).set_stroke(width=0).set_fill(VIOLET, 0.07),
            DashedVMobject(Circle(radius=k * r_atual()).move_to(C), num_dashes=40, dashed_ratio=0.6).set_stroke(VIOLET, 3, 0.95),
            DashedLine(C, C + k * r_atual() * P(np.cos(-0.5), np.sin(-0.5)), dash_length=0.06).set_stroke(VIOLET, 2.5, 0.9),
        ).set_z_index(5))
        corte = VGroup(vao, nuc, casca)
        rot_corte = VGroup(text("corte transversal", 18, opacity=0.6).move_to(C + P(0, 1.3)),
                           eq("a", size=24, color=BLUE_L).move_to(C + P(0, -k * a - 0.2)), eq("b", size=24, color=BLUE_L).move_to(C + P(0, -k * b - 0.2)))

        img = painel_3d(seq, s)
        img.set_opacity(0.0)
        self.add(img)
        self.play(img.animate.set_opacity(1.0), FadeIn(header), FadeIn(titulo), run_time=1.2)
        self.add(*[g for g, _ in regioes])
        self.play(FadeIn(rot_nucleo), FadeIn(rot_casca), run_time=0.8)
        self.play(FadeIn(VGroup(ax, curva, quedas, marcas)), FadeIn(VGroup(corte, rot_corte)), run_time=0.9)
        self.add(marcador, linha_r, gauss)
        self.wait(2.2)                                                              # r < a: dentro do metal
        self.play(s.animate.set_value(s_de(1.0)), run_time=3.5, rate_func=smooth)   # atravessa r = a e para no vão
        self.wait(3.0)                                                              # a < r < b
        self.play(s.animate.set_value(s_de(1.75)), run_time=3.5, rate_func=smooth)  # atravessa r = b
        self.wait(3.0)                                                              # r > b
        self.play(s.animate.set_value(0.0), run_time=4.0, rate_func=smooth)
        self.wait(1.0)
