"""Seções 1–4: abertura, regime magnetostático, geometria fonte–observador, lei de Biot–Savart."""
import math

import numpy as np
from manim import (
    VGroup, Line, DashedLine, Arc, Circle, Dot, Polygon, ParametricFunction, FadeIn, FadeOut, Create, Write,
    Indicate, LaggedStart, ReplacementTransform, TransformFromCopy, ValueTracker, always_redraw, linear, smooth,
    UP, DOWN, LEFT, RIGHT, BOLD,
)
from base import *  # noqa: F401,F403
from fisica import clinica


class Sec1:
    # ── 1 · abertura ────────────────────────────────────────────────────────────────────────────────────────
    def ring3d(self, cx, h, r, op=0.9, w=3.2):
        """Linha de B em torno de um fio vertical: metade de trás (abaixo do fio) + metade da frente, com setas."""
        back = ParametricFunction(lambda u: self.W([cx + r * math.cos(u), h, r * math.sin(u)]), t_range=[math.pi, 2 * math.pi],
                                  color=MAG, stroke_width=w, fill_opacity=0).set_stroke(opacity=op * 0.5).set_z_index(2)
        front = ParametricFunction(lambda u: self.W([cx + r * math.cos(u), h, r * math.sin(u)]), t_range=[0, math.pi],
                                   color=MAG, stroke_width=w, fill_opacity=0).set_stroke(opacity=op).set_z_index(5)
        g = VGroup(back, front)
        for ph, z in [(math.pi / 2, 5), (3 * math.pi / 2, 2)]:
            p = lambda a: self.W([cx + r * math.cos(a), h, r * math.sin(a)])
            g.add(arrow(p(ph + 0.16), p(ph - 0.16), MAG, 4, z=z, tip=0.22).set_opacity(op if z > 3 else op * 0.6))
        return g

    def abertura(self):
        self.section("abertura", "Como calcular o campo criado pela corrente?")
        self.reset_view(x=-3.7, y=-0.25, scale=0.98, beta=0, tau=36)
        X1, X2, H = -0.2, 2.7, 0.3
        L1 = self.tube(self.W([X1, -1.9, 0]), self.W([X1, 1.9, 0]))
        self.play(Create(L1), run_time=1.2)
        f1 = self.flow([lambda u: self.W([X1, -1.9 + 3.8 * u, 0])], count=7)
        self.add(f1)
        a1 = arrow(self.W([X1 - 0.55, -0.4, 0]), self.W([X1 - 0.55, 0.7, 0]), GREEN, 6)
        i1 = self.lab("I_1", self.W([X1 - 0.95, 0.15, 0]), "I_1", size=M_S)
        self.play(Create(a1), FadeIn(i1), run_time=0.9)
        self.caption("Um fio percorrido por corrente $I_1$")
        self.hold(2.5)
        rings = [self.ring3d(X1, h, r) for h, r in [(1.35, 1.15), (0.3, 2.9), (-1.0, 1.9)]]
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.45), run_time=3.0)
        b1 = self.lab(r"\mathbf B_1", self.W([X1 - 1.9, 1.55, 0]), r"\mathbf B_1", size=M_S)
        self.play(FadeIn(b1), run_time=0.7)
        self.caption("A corrente cria um campo magnético que envolve o fio")
        self.hold(2.5)
        e = self.show(E(r"I_1\ \longrightarrow\ \mathbf B_1", "I_1", r"\mathbf B_1", size=M_XL),
                      src={("I_1", 0): i1, (r"\mathbf B_1", 0): b1}, rt=1.8, wait=2.0)
        self.mark("gancho_campo")
        # segundo fio dentro do campo
        L2 = self.tube(self.W([X2, -1.9, 0]), self.W([X2, 1.9, 0]))
        self.play(Create(L2), run_time=1.0)
        P2 = self.W([X2, H, 0])
        sym = Dot(P2, radius=0.07, color=MAG)
        b1b = self.lab(r"\mathbf B_1", P2 + np.array([0.7, 0.8, 0]), r"\mathbf B_1", size=M_S)
        self.play(FadeIn(sym), FadeIn(b1b), run_time=0.9)
        self.caption("No fio 2, $\\mathbf B_1$ é tangente ao anel, perpendicular ao fio")
        self.hold(3)
        f2 = self.flow([lambda u: self.W([X2, -1.9 + 3.8 * u, 0])], count=7)
        a2 = arrow(self.W([X2 + 0.55, -0.4, 0]), self.W([X2 + 0.55, 0.7, 0]), GREEN, 6)
        i2 = self.lab("I_2", self.W([X2 + 0.95, 0.15, 0]), "I_2", size=M_S)
        Lbr = VGroup(Line(self.W([X2 + 1.15, -1.2, 0]), self.W([X2 + 1.15, 1.2, 0]), color=GREEN, stroke_width=3),
                     Line(self.W([X2 + 1.05, -1.2, 0]), self.W([X2 + 1.25, -1.2, 0]), color=GREEN, stroke_width=3),
                     Line(self.W([X2 + 1.05, 1.2, 0]), self.W([X2 + 1.25, 1.2, 0]), color=GREEN, stroke_width=3))
        Lm = self.lab(r"\mathbf L", self.W([X2 + 1.55, 0, 0]), r"\mathbf L", size=M_S)
        self.play(FadeIn(a2), FadeIn(i2), FadeIn(Lbr), FadeIn(Lm), run_time=0.9)
        self.add(f2)
        fy = -1.0
        fa = arrow(self.W([X2, fy, 0]), self.W([X2 - 1.3, fy, 0]), FC, 7)
        fm = self.lab(r"\mathbf F_2", self.W([X2 - 0.65, fy - 0.3, 0]), r"\mathbf F_2", size=M_S)
        self.play(Create(fa), FadeIn(fm), run_time=1.0)
        self.caption("O campo do fio 1 empurra as cargas em movimento do fio 2")
        self.show(E(r"\mathbf F_2=I_2\,\mathbf L\times\mathbf B_1", r"\mathbf F_2", "I_2", r"\mathbf L", r"\mathbf B_1", size=M_L),
                  (r"\mathbf B_1", r"\mathbf B_1"),
                  src={(r"\mathbf F_2", 0): fm, ("I_2", 0): i2, (r"\mathbf L", 0): Lm}, rt=2.0, wait=2.5)
        self.mark("gancho_dois_fios")
        # a pergunta: de onde vem B₁?
        q = self.show(E(r"\mathbf B_1=\ ?", r"\mathbf B_1", size=M_L), slot="A",
                      src={(r"\mathbf B_1", 0): glyphs(self.slots["H"]["eq"], r"\mathbf B_1", 0)}, rt=1.4, wait=0.5)
        bx = box(self.slots["H"]["eq"], MAG)
        self.play(FadeIn(bx), run_time=0.5)
        self.caption("Falta a regra que liga o campo à corrente que o produz")
        self.hold(4)
        self.play(FadeOut(bx), run_time=0.4)
        self.clear()
        self.cap = None
        self.play(FadeOut(self.head), run_time=0.5)
        self.head = None
        title = official_text("LEI DE BIOT–SAVART", DISPLAY_FONT, BOLD, 64).move_to([0, 0.5, 0])
        sub = txt("do elemento de corrente ao campo magnético", T_BODY, opacity=0.85).move_to([0, -0.5, 0])
        self.play(Write(title), run_time=1.8)
        self.play(FadeIn(sub), run_time=0.8)
        self.hold(2.5)
        self.mark("titulo")
        self.play(FadeOut(title), FadeOut(sub), run_time=0.7)
