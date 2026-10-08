"""Coaxial: apresentação 3D breve (Blender) + corte transversal 2D grande como explicação principal (Manim). Sandbox, fora do yt_0002.

Só o quadro de apresentação vem do Blender (render_apresentacao.py). A gaussiana é uma circunferência tracejada controlada por um
ValueTracker no próprio Manim (nada de sequência de imagens); a região, Q_env e E(r) seguem o mesmo r. Modelo ideal: +λ na superfície do
condutor interno (raio a), −λ na superfície interna da casca externa ideal (raio b), L fixo perpendicular ao corte; sem gráfico.

Rodar, a partir da raiz do repositório:
    uv run python -m manim -r 960,540 --fps 30 --media_dir media/preview_coaxial_corte2d experimentos/blender/preview_coaxial_corte2d/cena_coaxial_corte2d.py CoaxialCorte2D
"""

import sys
from pathlib import Path

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UL, UP, Annulus, Arrow, Circle, DashedLine, DashedVMobject, FadeIn, FadeOut, Group, ImageMobject, Line, Scene,
    ValueTracker, VGroup, always_redraw, smooth,
)

HERE = Path(__file__).resolve().parent
RAIZ = HERE.parents[2]
sys.path.insert(0, str(HERE.parent / "teste_gauss_coaxial"))
from cena_manim import BACKGROUND_COLOR, BLUE_L, CYAN, VIOLET, WHITE, P, eq, text  # noqa: E402  (helpers da v1; ela não é alterada)

MAG = "#EA63FF"
A, B = 0.5, 1.5                                   # raios do condutor interno e da casca externa ideal
R0, R1 = 0.25, 1.75                               # faixa de r da gaussiana
K = 1.9                                           # unidades de cena por unidade física
C = P(-3.0, -0.15)                                # centro do corte
RL = 1.6                                          # borda esquerda da coluna de texto
Q_ENV = r"Q_{\mathrm{env}}"
U = lambda g: P(np.cos(np.radians(g)), np.sin(np.radians(g)))      # noqa: E731
PX = lambda px, py: P((px / 1120 - 0.5) * 9.4, -0.1 + (0.5 - py / 784) * 6.58)    # pixel do quadro 3D → cena


def mix(*pedacos, size=24, cor=WHITE, op=0.92):
    return VGroup(*[text(q, size, cor, op) if isinstance(q, str) else q for q in pedacos]).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)


def col(m, y):
    return m.move_to(P(0, y)).align_to(P(RL, 0), LEFT)


def sinal(txt, cor, pos):
    """Marcador esquemático de carga (+ ou −), desenhado com traços e um disco do fundo atrás; não é uma contagem de cargas."""
    s_ = 0.11
    fundo = Circle(radius=0.17).move_to(pos).set_stroke(width=0).set_fill(BACKGROUND_COLOR, 0.9)
    tr = [Line(pos + P(-s_, 0), pos + P(s_, 0)).set_stroke(cor, 4.5)]
    if txt == "+":
        tr.append(Line(pos + P(0, -s_), pos + P(0, s_)).set_stroke(cor, 4.5))
    return VGroup(fundo, *tr).set_z_index(8)


class CoaxialCorte2D(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        r = ValueTracker(R0)
        r_atual = lambda: r.get_value()

        # ── 1) apresentação 3D breve ────────────────────────────────────────
        img = ImageMobject(str(RAIZ / "renders" / "preview_coaxial_corte2d" / "apresentacao.png")).set_width(9.4).move_to(P(0, -0.1))
        titulo3d = text("CABO COAXIAL", 36, WHITE).move_to(P(0, 3.85))
        lam_p, lam_m = eq(r"+\lambda", size=26, color=BLUE_L), eq(r"-\lambda", size=26, color=MAG)

        def rotulo(pecas, pos_texto, alvo_px, cor):
            t = VGroup(*[text(q, 20, cor, 0.92) if isinstance(q, str) else q for q in pecas]).arrange(RIGHT, buff=0.1, aligned_edge=DOWN).move_to(pos_texto)
            return VGroup(t, Line(t.get_bottom() + 0.07 * DOWN, PX(*alvo_px)).set_stroke(cor, 1.8, 0.65))
        rotulos3d = VGroup(rotulo(["condutor interno", lam_p], PX(150, 130), (420, 340), BLUE_L),
                           rotulo(["casca externa", lam_m], PX(880, 60), (700, 190), BLUE_L),
                           rotulo(["vão"], PX(250, 690), (500, 440), WHITE))
        img.set_opacity(0.0)
        self.add(img)
        self.play(img.animate.set_opacity(1.0), FadeIn(titulo3d), run_time=0.6)
        self.wait(0.4)
        self.play(FadeIn(rotulos3d), run_time=0.6)
        self.wait(1.2)

        # ── 2) corte transversal 2D (principal): geometria e sinais ─────────
        nucleo = Circle(radius=K * A).move_to(C).set_stroke(BLUE_L, 3).set_fill("#1B4DB5", 0.5)
        casca = Circle(radius=K * B).move_to(C).set_stroke(BLUE_L, 5).set_fill(opacity=0)
        sinais = VGroup(*[sinal(r"+", BLUE_L, C + K * A * U(45 * i)) for i in range(8)],
                        *[sinal(r"-", MAG, C + (K * B - 0.19) * U(45 * i + 22.5)) for i in range(8)])
        eixo = VGroup(Line(C, C + P(K * B, 0)).set_stroke(WHITE, 1.5, 0.45),
                      *[Line(C + P(K * x, -0.07), C + P(K * x, 0.07)).set_stroke(WHITE, 2, 0.7) for x in (A, B)],
                      eq("a", size=40, color=WHITE).move_to(C + P(K * A, -0.4)), eq("b", size=40, color=WHITE).move_to(C + P(K * B, -0.4)))
        vao = text("vão", 20, WHITE, 0.6).move_to(C + K * 1.0 * U(180))
        estrutura = VGroup(nucleo, casca, sinais, eixo, vao)
        titulo = col(mix("CABO COAXIAL ·", eq(r"+\lambda", size=28, color=BLUE_L), "e", eq(r"-\lambda", size=28, color=MAG)), 2.95)
        leg = VGroup(col(mix(eq(r"+\lambda", size=30, color=BLUE_L), "na superfície do condutor interno"), 1.7),
                     col(mix(eq(r"-\lambda", size=30, color=MAG), "na face interna da casca externa"), 1.0))
        self.play(FadeOut(Group(img, titulo3d, rotulos3d)), FadeIn(estrutura), FadeIn(titulo), run_time=0.8)
        self.play(FadeIn(leg, shift=0.1 * UP), run_time=0.4)
        self.wait(0.9)

        # ── 3) campo no vão: 8 setas radiais igualmente espaçadas, mesmo raio e mesmo comprimento ──
        ra, rb = 0.72, 1.17
        setas = VGroup(*[Arrow(C + K * ra * U(22.5 + 45 * i), C + K * rb * U(22.5 + 45 * i), buff=0, stroke_width=3.5, tip_length=0.2, color=CYAN)
                         for i in range(8)]).set_stroke(opacity=0.6)
        nota_campo = col(mix("campo radial só no vão", cor=CYAN), 0.2)
        self.play(FadeOut(leg), FadeIn(setas), FadeIn(nota_campo, shift=0.1 * UP), run_time=0.6)
        self.wait(0.8)

        # ── 4) gaussiana animada pelo ValueTracker + região, Q_env e E(r) (troca discreta nas fronteiras) ──
        def bloco(dom, q, e, nota):
            d = eq(dom, size=34, color=VIOLET).move_to(P(0, 1.7)).align_to(P(RL, 0), LEFT)
            qq = eq(q, size=40).move_to(P(0, 1.7)).align_to(P(RL + 1.9, 0), LEFT)
            return VGroup(d, qq, col(e, 0.6), col(text(nota, 22, WHITE, 0.92), -0.4))
        reg = [(lambda x: x < A - 1e-3, bloco(r"r<a", Q_ENV + "=0", eq("E", "=0", size=50, colors={0: CYAN}), "dentro do metal: nada envolvido")),
               (lambda x: A - 1e-3 <= x <= B + 1e-3, bloco(r"a<r<b", Q_ENV + r"=\lambda L",
                                                           eq("E", "=", r"\frac{\lambda}{2\pi\varepsilon_0 r}", size=50, colors={0: CYAN}), "campo radial no vão")),
               (lambda x: x > B + 1e-3, bloco(r"r>b", Q_ENV + r"=(\lambda-\lambda)L=0", eq("E", "=0", size=50, colors={0: CYAN}), "fora, no modelo ideal: E = 0"))]
        for cond, g in reg:
            g.add_updater(lambda m, c=cond: m.set_opacity(1.0 if c(r_atual()) else 0.0))
            g.update()
        # destaque sutil da região avaliada
        d1 = Circle(radius=K * A).move_to(C).set_stroke(width=0).set_fill(VIOLET, 0.0)
        d2 = Annulus(inner_radius=K * A, outer_radius=K * B).move_to(C).set_stroke(width=0).set_fill(CYAN, 0.0)
        d1.add_updater(lambda m: m.set_fill(VIOLET, 0.16 if r_atual() < A - 1e-3 else 0.0))
        d2.add_updater(lambda m: m.set_fill(CYAN, 0.09 if A - 1e-3 <= r_atual() <= B + 1e-3 else 0.0))
        gauss = always_redraw(lambda: VGroup(
            Circle(radius=K * r_atual()).move_to(C).set_stroke(width=0).set_fill(VIOLET, 0.05),
            DashedVMobject(Circle(radius=K * r_atual()).move_to(C), num_dashes=56, dashed_ratio=0.55).set_stroke(VIOLET, 4, 0.95),
            DashedLine(C, C + K * r_atual() * U(-40), dash_length=0.08).set_stroke(VIOLET, 2.5, 0.95),
            Circle(radius=0.09).move_to(C + K * r_atual() * U(-40)).set_stroke(VIOLET, 2.5).set_fill(WHITE, 1)).set_z_index(6))
        lab_r = eq("r", size=32, color=VIOLET)
        lab_r.add_updater(lambda m: m.move_to(C + K * r_atual() * 0.5 * U(-40) + 0.26 * U(-130)))
        lab_E, lab_E0 = eq("E(r)", size=34, color=CYAN), eq("E(r)=0", size=32, color=WHITE)
        fundo_E = Circle(radius=0.01)                      # (reservado) o rótulo ganha um retângulo do fundo logo abaixo
        for lab, dist in ((lab_E, 0.75), (lab_E0, 0.95)):
            lab.set_z_index(9)
        lab_E.add_updater(lambda m: m.move_to(C + (K * r_atual() + 0.75) * U(-40) + P(0.2, 0)).set_opacity(1.0 if A - 1e-3 <= r_atual() <= B + 1e-3 else 0.0))
        lab_E0.add_updater(lambda m: m.move_to(C + (K * r_atual() + 0.95) * U(-40) + P(0.3, 0)).set_opacity(0.0 if A - 1e-3 <= r_atual() <= B + 1e-3 else 0.95))
        nota_L = col(text("L fixo, perpendicular ao corte", 20, WHITE, 0.6), -3.7)
        self.add(d1, d2)
        self.bring_to_front(estrutura, setas)
        self.play(FadeOut(nota_campo), FadeIn(nota_L), run_time=0.4)
        self.add(*[g for _, g in reg], gauss, lab_r, lab_E, lab_E0)
        self.wait(0.7)                                                         # r < a
        self.play(r.animate.set_value(1.0), run_time=2.0, rate_func=smooth)    # atravessa r = a: salto discreto de região, Q_env e E
        self.wait(1.0)                                                         # a < r < b
        self.play(r.animate.set_value(R1), run_time=1.6, rate_func=smooth)     # atravessa r = b
        self.wait(1.0)                                                         # r > b
        self.wait(0.6)
        for m in (d1, d2, gauss, lab_r, lab_E, lab_E0, *[g for _, g in reg]):  # congela o último estado para o fade-out
            m.clear_updaters()
        self.play(FadeOut(Group(estrutura, setas, titulo, nota_L, d1, d2, gauss, lab_r, lab_E, lab_E0, *[g for _, g in reg])), run_time=0.5)
