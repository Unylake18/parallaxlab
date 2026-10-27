"""Seções 14–15: síntese (uma lei, duas geometrias) e fechamento."""
import math

import numpy as np
from manim import (
    VGroup, Line, Circle, Dot, FadeIn, FadeOut, Create, ReplacementTransform, Write, ValueTracker, always_redraw, BOLD,
    UP, DOWN, LEFT, RIGHT,
)
from base import *  # noqa: F401,F403


class Sec7:
    def sintese(self):
        self.section("sintese", "Uma lei; geometrias diferentes")
        self.clear()
        self.reset_view(x=-4.3, y=-0.8, scale=1.0)
        W = self.W
        wire = self.tube(W([-2.2, 0, 0]), W([2.2, 0, 0]))
        flow = self.flow([lambda u: W([-2.2 + 4.4 * u, 0, 0])], count=7)
        P = W([0.0, 1.9, 0])
        f = W([0.0, 0.0, 0])
        self.play(Create(wire), run_time=1.0)
        self.add(flow)
        pd, pl = Dot(P, radius=0.1), self.lab("P", P + np.array([-0.3, 0.3, 0]), size=M_M)
        sep = arrow(f, P, VIOLET, 5)
        rl = self.lab(r"\mathbf R", (f + P) / 2 + np.array([0.4, 0, 0]), r"\mathbf R", size=M_M)
        self.play(FadeIn(pd), FadeIn(pl), Create(sep), FadeIn(rl), run_time=1.2)
        self.show(E(r"\mathbf R=\mathbf r-\mathbf r'", r"\mathbf R", r"\mathbf r", r"\mathbf r'", size=M_L), src={(r"\mathbf R", 0): rl}, rt=1.8, wait=1.5)
        self.caption("A fonte e o observador constroem a separação $\\mathbf R$")
        self.show(E(r"d\mathbf B=\frac{\mu_0}{4\pi}\frac{I\,d\boldsymbol\ell\times\mathbf R}{R^3}", r"d\mathbf B", "I", r"d\boldsymbol\ell", r"\times",
                    r"\mathbf R", "R^3", r"\frac{\mu_0}{4\pi}", "=", size=M_L), (r"\mathbf R", r"\mathbf R"), rt=2.2, wait=2.0)
        self.caption("Cada elemento contribui com direção e intensidade próprias")
        self.show(E(r"\mathbf B=\int d\mathbf B", r"\mathbf B", r"\int", r"d\mathbf B", size=M_XL), (r"d\mathbf B", r"d\mathbf B"), rt=2.2, wait=2.0)
        self.caption("Somar as contribuições recupera o campo da fonte")
        self.hold(2)
        self.clear()
        self.reset_view(x=-4.3, y=-0.8, scale=1.0)
        wire = self.tube(W([-2.3, 0, 0]), W([2.3, 0, 0]))
        flow = self.flow([lambda u: W([-2.3 + 4.6 * u, 0, 0])])
        self.play(Create(wire), run_time=0.8)
        self.add(flow)
        self.show(E(r"B_\infty=\frac{\mu_0 I}{2\pi a}", r"B_\infty", "I", r"\mu_0", size=M_XL), rt=1.4, wait=2.0)
        self.caption("Fio infinito: $B\\propto1/a$")
        self.hold(2.5)
        self.remove(flow)
        self.drop("H")
        self.caption("A mesma lei, agora com outra fonte")
        loop = Circle(radius=1.55, color=BLUE_L, stroke_width=7).move_to([-4.3, -0.15, 0])
        self.play(ReplacementTransform(wire, loop), run_time=2.2)
        lflow = self.flow([lambda u: np.array([-4.3 + 1.55 * math.cos(2 * math.pi * u), -0.15 + 1.55 * math.sin(2 * math.pi * u), 0])], count=10)
        self.add(lflow)
        il = self.lab("I", [-2.35, 0.75, 0], "I", size=M_M)
        ia = arrow([-2.75, 0.0, 0], [-2.75, 0.75, 0], GREEN, 6)
        self.play(FadeIn(il), FadeIn(ia), run_time=0.8)
        self.show(E(r"B_z=\frac{\mu_0 I R^2}{2\left(R^2+z^2\right)^{3/2}}", r"I", r"\mu_0", "B_z", size=M_L), src={("I", 0): il}, rt=2.4, wait=2.0)
        self.caption("Fio: $B\\propto a^{-1}$ · espira (longe): $B\\propto|z|^{-3}$")
        self.mark("sintese_geometria")
        self.hold(5)

    def fechamento(self):
        self.section("fechamento", "Que estrutura o campo magnético possui?")
        self.clear()
        rings = VGroup()
        for r in (0.85, 1.45, 2.05):
            rings.add(Circle(radius=r, color=MAG, stroke_width=3).move_to([-3.3, 0, 0]),
                      arrow([-3.3 + r, -0.12, 0], [-3.3 + r, 0.25, 0], MAG, 4, tip=0.18))
        source = VGroup(Circle(radius=0.18, color=GREEN, stroke_width=4).move_to([-3.3, 0, 0]), Dot([-3.3, 0, 0], color=GREEN, radius=0.06))
        local = Circle(radius=0.32, color=WHITE, stroke_width=2.5).move_to([-1.2, 0, 0])
        for ring in rings:
            self.play(Create(ring), run_time=0.3)
        self.play(FadeIn(source), FadeIn(local), run_time=0.8)
        q1 = txt("O que revela o divergente?", T_BODY).move_to([3.7, 0.9, 0])
        q2 = txt("E o rotacional? E Ampère?", T_BODY).move_to([3.7, -0.5, 0])
        self.play(FadeIn(q1), run_time=0.9)
        self.hold(2)
        self.play(FadeIn(q2), run_time=0.9)
        self.caption("Que propriedades esse campo necessariamente possui?")
        self.mark("gancho_estrutura_local")
        self.hold(6)
        self.clear()
        end = txt("PARALLAX LAB", 40).move_to([0, 0.7, 0])
        below = txt("LEI DE BIOT–SAVART", T_BODY, opacity=0.8).move_to([0, -0.3, 0])
        self.play(FadeIn(end), FadeIn(below), run_time=1.2)
        self.hold(4)
        self.mark("fim")
