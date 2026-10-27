"""Seções 9–11: trecho retilíneo finito, fio infinito como limite e força entre fios."""
import math

import numpy as np
from manim import (
    VGroup, Line, DashedLine, Dot, Polygon, ParametricFunction, FadeIn, FadeOut, Create, Indicate, ValueTracker,
    always_redraw, linear, smooth, DecimalNumber, VMobject, ReplacementTransform,
    UP, DOWN, LEFT, RIGHT,
)
from base import *  # noqa: F401,F403
from fisica import trecho, fios


class Sec5:
    A_FIO = 2.1

    def seg_shapes(self):
        """Geometria do trecho no estado atual: elemento em x, separação, componentes, ângulos (conforme flags)."""
        W, x, a = self.W, self.x_src.get_value(), self.A_FIO
        F = self.seg_flags
        f = np.array([x, 0.0, 0.0])
        P = np.array([0.0, a, 0.0])
        R = P - f
        th = math.acos(np.clip(np.dot([1, 0, 0], R) / np.linalg.norm(R), -1, 1))
        al = math.atan2(x, a)
        g = VGroup(DashedLine(W([0, 0, 0]), W(P), color=VIOLET, stroke_width=2.4),
                   Dot(W(f), radius=0.1, color=GREEN).set_z_index(9),
                   arrow(W(f), W(f + [0.8, 0, 0]), GREEN, 8, z=8),
                   arrow(W(f), W(P), VIOLET, 5, z=6),
                   Dot(W(P), radius=0.11, color=WHITE).set_z_index(9))
        if abs(x) > 0.3:
            s = 1 if x > 0 else -1
            g.add(VMobject(color=WHITE, stroke_width=2).set_points_as_corners(
                [W([0.22 * s, 0, 0]), W([0.22 * s, 0.22, 0]), W([0, 0.22, 0])]))
        if F.get("sym", True):
            g.add(self.out_symbol(W(P) + np.array([0.6, 0, 0]), 1, 0.19))
        if F.get("par"):
            g.add(arrow(W(f), W([0, 0, 0]), VIOLET, 5, z=7, tip=0.2).set_opacity(0.95))
        if F.get("perp"):
            g.add(arrow(W([0, 0, 0]), W(P), CYAN, 5, z=7, tip=0.2))
        if F.get("theta"):
            g.add(ParametricFunction(lambda u: W(f + 0.55 * np.array([math.cos(u), math.sin(u), 0])), t_range=[0.001, th],
                                     color=WHITE, stroke_width=2.6, fill_opacity=0))
        if F.get("alpha") and abs(al) > 1e-3:
            g.add(ParametricFunction(lambda u: W(P + 0.7 * np.array([math.sin(u), -math.cos(u), 0])),
                                     t_range=[min(0, al), max(0, al)], color=CYAN, stroke_width=3.2, fill_opacity=0))
        return g

    def view_to(self, x, y, s, rt=1.4):
        self.play(self.ox.animate.set_value(x), self.oy.animate.set_value(y), self.gs.animate.set_value(s), run_time=rt)

    def trecho_finito(self):
        self.section("trecho", "Contribuição de um trecho retilíneo do circuito")
        self.clear()
        self.reset_view(x=-4.0, y=-1.55, scale=1.12)
        W, a = self.W, self.A_FIO
        H = lambda: self.slots["H"]["eq"]
        A_ = lambda: self.slots["A"]["eq"]
        self.x_src = ValueTracker(1.7)
        self.seg_flags = {"sym": True}
        key = lambda: (self.x_src.get_value(), tuple(sorted(self.seg_flags.items())), *self.view_key())
        geo = self.cached(key, self.seg_shapes)
        wire = always_redraw(lambda: self.tube(W([-2.6, 0, 0]), W([2.6, 0, 0])))
        flow = self.flow([lambda u: W([-2.6 + 5.2 * u, 0, 0])])
        circ = VMobject(color=BLUE_L, stroke_width=3.5).set_points_as_corners(
            [W([2.6, 0, 0]), W([2.6, -1.3, 0]), W([-2.6, -1.3, 0]), W([-2.6, 0, 0])]).set_stroke(opacity=0.4)
        pl = self.lab("P", W([0, a, 0]) + np.array([-0.3, 0.3, 0]), size=M_M)
        pl.add_updater(lambda m: m.move_to(W([0, a, 0]) + np.array([-0.3, 0.3, 0])))
        xv = lambda: self.x_src.get_value()
        dll = self.lab(r"d\boldsymbol\ell", [0, 0, 0], r"d\boldsymbol\ell", size=M_M)
        dll.add_updater(lambda m: m.move_to(W([xv() + 0.4, -0.5, 0])))
        Rl = self.lab(r"\mathbf R", [0, 0, 0], r"\mathbf R", size=M_M)
        Rl.add_updater(lambda m: m.move_to(W([xv() / 2, a / 2, 0]) + np.array([0.42, 0.05, 0])))
        al_ = self.lab("a", [0, 0, 0], "a", size=M_M, color=VIOLET)
        al_.add_updater(lambda m: m.move_to(W([0, a / 2, 0]) + np.array([-0.3, 0, 0])))
        xl = self.lab("x", [0, 0, 0], "x", size=M_M, color=VIOLET)
        xl.add_updater(lambda m: m.move_to(W([xv() / 2, -0.4, 0])))
        self.play(FadeIn(wire), FadeIn(geo), FadeIn(pl), run_time=1.2)
        self.add(flow)
        # ── 1 · o trecho dentro do circuito ──────────────────────────────────────────────────────────────
        self.play(Create(circ), run_time=1.2)
        seg_l = txt("trecho", T_NOTE, GREEN).move_to(W([-1.75, 0.45, 0]))
        rest_l = txt("resto do circuito", T_NOTE, DIM).move_to(W([0, -0.7, 0]))
        self.play(FadeIn(seg_l), FadeIn(rest_l), run_time=0.8)
        self.caption("Somamos vetorialmente: trecho + resto do circuito")
        self.show(E(r"\mathbf B_{\rm total}=\mathbf B_{\rm trecho}+\mathbf B_{\rm restante}", r"\mathbf B_{\rm total}", r"\mathbf B_{\rm trecho}",
                    r"\mathbf B_{\rm restante}", size=M_M),
                  src={(r"\mathbf B_{\rm trecho}", 0): seg_l, (r"\mathbf B_{\rm restante}", 0): rest_l}, rt=2.0, wait=1.5)
        self.mark("trecho_circuito")
        self.caption("Calcule só o trecho")
        self.play(FadeOut(circ), FadeOut(seg_l), FadeOut(rest_l), run_time=0.8)
        self.drop("H")
        self.play(FadeIn(dll), FadeIn(Rl), FadeIn(al_), FadeIn(xl), run_time=0.8)
        # ── 2 · elemento e separação ─────────────────────────────────────────────────────────────────────
        self.show(E(r"d\boldsymbol\ell=dx\,\hat x", r"d\boldsymbol\ell", r"dx\,\hat x", size=M_L), src={(r"d\boldsymbol\ell", 0): dll},
                  rt=1.8, wait=1.0)
        self.caption("Percorrer o fio é percorrer $x$")
        self.seg_flags["par"] = True
        self.seg_flags["perp"] = True
        parl = self.lab(r"-x\,\hat x", W([0.85, 0, 0]) + np.array([0, -0.45, 0]), r"-x\,\hat x", size=M_M)
        perl = self.lab(r"a\,\hat y", W([0, a * 0.5, 0]) + np.array([-0.62, 0, 0]), r"a\,\hat y", size=M_M)
        self.play(FadeOut(al_), FadeOut(xl), FadeIn(parl), FadeIn(perl), run_time=1.2)
        self.show(E(r"\mathbf R=-x\,\hat x+a\,\hat y", r"\mathbf R", r"-x\,\hat x", r"a\,\hat y", size=M_M), slot="A",
                  src={(r"\mathbf R", 0): Rl, (r"-x\,\hat x", 0): parl, (r"a\,\hat y", 0): perl}, rt=2.2, wait=1.5)
        self.caption("$\\mathbf R$ = parte paralela + parte perpendicular")
        self.mark("trecho_modelagem")
        # ── 3 · produto vetorial, passo a passo ──────────────────────────────────────────────────────────
        aux = A_()
        self.show(E(r"d\boldsymbol\ell\times\mathbf R=dx\,\hat x\times\left(-x\,\hat x+a\,\hat y\right)", r"d\boldsymbol\ell", r"\mathbf R",
                    r"dx\,\hat x", r"-x\,\hat x", r"a\,\hat y", size=M_M),
                  src={(r"\mathbf R", 0): glyphs(aux, r"\mathbf R", 0), (r"-x\,\hat x", 0): glyphs(aux, r"-x\,\hat x", 0),
                       (r"a\,\hat y", 0): glyphs(aux, r"a\,\hat y", 0)}, rt=2.4, wait=1.5)
        self.drop("A")
        self.caption("Distribua o produto vetorial")
        self.show(E(r"d\boldsymbol\ell\times\mathbf R=-x\,dx\left(\hat x\times\hat x\right)+a\,dx\left(\hat x\times\hat y\right)", r"d\boldsymbol\ell",
                    r"\mathbf R", r"-x\,dx", r"\left(\hat x\times\hat x\right)", r"a\,dx", r"\left(\hat x\times\hat y\right)", size=M_M,
                    colors={r"-x\,dx": VIOLET}),
                  (r"-x\,\hat x", r"-x\,dx"), (r"a\,\hat y", r"a\,dx"), (r"dx\,\hat x", r"\left(\hat x\times\hat x\right)"),
                  (r"dx\,\hat x", r"\left(\hat x\times\hat y\right)"), rt=2.6, wait=2.0, structure=False)
        self.caption("Paralelo: $\\hat x\\times\\hat x=0$.  Perpendicular: $\\hat x\\times\\hat y=\\hat z$")
        self.play(Indicate(self.slots["H"]["eq"], color=MAG, scale_factor=1.02), run_time=0.8)
        self.show(E(r"d\boldsymbol\ell\times\mathbf R=-x\,dx\,\mathbf 0+a\,dx\,\hat z", r"d\boldsymbol\ell", r"\mathbf R", r"-x\,dx", r"\mathbf 0", r"a\,dx",
                    r"\hat z", size=M_L, colors={r"-x\,dx": VIOLET, r"\mathbf 0": VIOLET}),
                  (r"\left(\hat x\times\hat x\right)", r"\mathbf 0"), (r"\left(\hat x\times\hat y\right)", r"\hat z"), rt=2.2, wait=1.5, structure=False)
        self.seg_flags["par"] = False
        self.hold(0.6)
        self.caption("A parte paralela zera; a perpendicular vira $\\hat z$, para fora da tela")
        zl = self.lab(r"\hat z", [0, 0, 0], r"\hat z", size=M_M)
        self.play(self.beta.animate.set_value(20), self.tau.animate.set_value(38), FadeOut(parl), FadeOut(perl), run_time=2.0)
        zv = self.vec(np.array([0, a, 0]), [0, 0, 1], MAG, scale=1.1, width=6)
        zl.move_to(W(np.array([0, a, 1.2])) + np.array([0.35, 0.1, 0]))
        self.play(FadeIn(zv), FadeIn(zl), run_time=0.9)
        self.show(E(r"d\boldsymbol\ell\times\mathbf R=a\,dx\,\hat z", r"d\boldsymbol\ell", r"\mathbf R", r"a\,dx", r"\hat z", size=M_XL),
                  (r"-x\,dx", None), (r"\mathbf 0", None), rt=2.0, wait=1.5, structure=False)
        self.mark("trecho_componente_perpendicular")
        # ── 4 · entra na lei ─────────────────────────────────────────────────────────────────────────────
        lei = E(r"d\mathbf B=\frac{\mu_0}{4\pi}\frac{I\,d\boldsymbol\ell\times\mathbf R}{R^3}", r"d\mathbf B", "I", r"d\boldsymbol\ell",
                r"\times", r"\mathbf R", "R^3", r"\frac{\mu_0}{4\pi}", "=", size=M_S)
        lei_t = txt("lei de Biot–Savart", T_NOTE, DIM).move_to(AUX + np.array([0, 0.95, 0]))
        self.show(lei, slot="A", rt=1.2, wait=0.5)
        self.play(FadeIn(lei_t), run_time=0.5)
        self.caption("Substitua na lei")
        self.hold(1.2)
        aux = A_()
        self.show(E(r"d\mathbf B=\frac{\mu_0 I}{4\pi}\frac{a\,dx}{R^3}\,\hat z", r"d\mathbf B", "I", r"a\,dx", r"\hat z", "R^3", r"\mu_0", "=", size=M_L),
                  (r"d\boldsymbol\ell", None), (r"\mathbf R", None),
                  src={(r"d\mathbf B", 0): glyphs(aux, r"d\mathbf B", 0), ("I", 0): glyphs(aux, "I", 0),
                       ("R^3", 0): glyphs(aux, "R^3", 0), (r"\mu_0", 0): glyphs(aux, r"\frac{\mu_0}{4\pi}", 0)},
                  rt=2.6, wait=1.5)
        self.play(FadeOut(lei_t), FadeOut(zv), FadeOut(zl), run_time=0.4)
        self.drop("A")
        self.mark("trecho_dB_R3")
        # ── 5 · triângulo grande: Pitágoras ──────────────────────────────────────────────────────────────
        self.seg_flags["par"] = True
        self.seg_flags["perp"] = True
        self.play(self.beta.animate.set_value(0), self.tau.animate.set_value(0), run_time=1.2)
        self.relayout("geo", 1.0)
        self.view_to(-2.7, -1.75, 1.4, 1.4)
        self.play(FadeIn(xl), FadeIn(al_), run_time=0.6)
        self.caption("Pitágoras: $R^2=x^2+a^2$")
        self.show(E(r"R=\sqrt{x^2+a^2}", "R", r"x^2+a^2", size=M_M), slot="A",
                  src={("R", 0): Rl, (r"x^2+a^2", 0): [xl, al_]}, rt=2.0, wait=2.0)
        self.show(E(r"d\mathbf B=\frac{\mu_0 I}{4\pi}\frac{a\,dx}{(x^2+a^2)^{3/2}}\,\hat z", r"d\mathbf B", "I", r"a\,dx", r"\hat z",
                    r"(x^2+a^2)^{3/2}", r"\mu_0", "=", size=M_M, colors={r"(x^2+a^2)^{3/2}": VIOLET}),
                  ("R^3", r"(x^2+a^2)^{3/2}"), rt=2.2, wait=1.5)
        self.drop("A")
        self.relayout("split", 1.0)
        self.view_to(-4.0, -1.55, 1.12, 1.2)
        self.mark("trecho_dB_x")
        # ── 6 · mover a fonte ────────────────────────────────────────────────────────────────────────────
        self.seg_flags["par"] = False
        self.seg_flags["perp"] = False
        self.seg_flags["theta"] = True
        self.seg_flags["alpha"] = True
        self.caption("Mova o elemento: $|d\\mathbf B|$ muda, o sentido não")
        nums = VGroup(E("x=", size=M_S), DecimalNumber(1.7, num_decimal_places=2, font_size=36), E("R=", "R", size=M_S),
                      DecimalNumber(0, num_decimal_places=2, font_size=36)).arrange(RIGHT, buff=0.25).move_to(AUX + np.array([0, 0.25, 0]))
        nums[1].add_updater(lambda m: m.set_value(self.x_src.get_value()))
        nums[3].add_updater(lambda m: m.set_value(trecho(self.x_src.get_value())[4]))
        ang = VGroup(E(r"\theta=", size=M_S), DecimalNumber(0, num_decimal_places=1, unit=r"^\circ", font_size=36),
                     E(r"\alpha=", size=M_S), DecimalNumber(0, num_decimal_places=1, unit=r"^\circ", font_size=36)).arrange(
            RIGHT, buff=0.45).move_to(AUX + np.array([0, -0.55, 0]))
        ang[2].set_color(CYAN)
        ang[1].add_updater(lambda m: m.set_value(math.degrees(trecho(self.x_src.get_value())[5])))
        ang[3].add_updater(lambda m: m.set_value(math.degrees(trecho(self.x_src.get_value())[6])))
        nums.update(0)
        ang.update(0)
        card = self._card("A")
        self.play(FadeIn(card), FadeIn(nums), FadeIn(ang), run_time=0.9)
        self.slots["A"]["eq"] = VGroup(nums, ang)
        for xx in (-2.1, 0.0, 2.1):
            self.play(self.x_src.animate.set_value(xx), run_time=3, rate_func=linear)
            self.hold(0.8)
        self.mark("trecho_x_move")
        self.caption("$\\theta$ (da lei) e $\\alpha$ (da perpendicular) são ângulos diferentes")
        self.hold(2.5)
        nums.clear_updaters(recursive=True)
        ang.clear_updaters(recursive=True)
        self.drop("A")
        # ── 7 · mudança de variável (álgebra dominante) ──────────────────────────────────────────────────
        self.seg_flags["theta"] = False
        self.x_src.set_value(1.7)
        self.relayout("alg", 1.0)
        self.view_to(-4.3, -1.3, 0.95, 1.2)
        self.show(E(r"\tan\alpha=\frac{x}{a}", r"\tan\alpha", r"\frac{x}{a}", size=M_L, colors={r"\tan\alpha": CYAN}), slot="A",
                  src={(r"\frac{x}{a}", 0): [xl, al_]}, rt=1.8, wait=1.5)
        self.caption("Reescreva $x$ em função de $\\alpha$")
        self.show(E(r"x=a\tan\alpha", r"a\tan\alpha", size=M_L, colors={r"a\tan\alpha": CYAN}), (r"\tan\alpha", r"a\tan\alpha"),
                  slot="A", rt=1.8, wait=1.5)
        self.show(E(r"dx=a\sec^2\alpha\,d\alpha", "dx", r"a\sec^2\alpha\,d\alpha", size=M_L, colors={r"a\sec^2\alpha\,d\alpha": CYAN}),
                  (r"a\tan\alpha", r"a\sec^2\alpha\,d\alpha"), slot="A", rt=1.8, wait=1.5)
        aux2 = A_()
        self.caption("Derive: $dx=a\\sec^2\\alpha\\,d\\alpha$")
        self.hold(0.5)
        new = E(r"d\mathbf B=\frac{\mu_0 I}{4\pi}\frac{a\,a\sec^2\alpha\,d\alpha}{(x^2+a^2)^{3/2}}\,\hat z", r"d\mathbf B", "I", r"\hat z",
                r"a\sec^2\alpha\,d\alpha", r"(x^2+a^2)^{3/2}", r"\mu_0", "=", size=M_L,
                colors={r"a\sec^2\alpha\,d\alpha": CYAN, r"(x^2+a^2)^{3/2}": VIOLET})
        self.hl(r"a\,dx")
        self.show(new, (r"a\,dx", None), src={(r"a\sec^2\alpha\,d\alpha", 0): glyphs(aux2, r"a\sec^2\alpha\,d\alpha", 0)}, rt=2.4, wait=1.2)
        self.drop("A")
        # denominador, sem pular etapas
        self.caption("Reescreva o denominador em função de $\\alpha$")
        self.show(E(r"x^2+a^2=a^2\tan^2\alpha+a^2", "x^2+a^2", r"a^2\tan^2\alpha", size=M_L, colors={r"a^2\tan^2\alpha": CYAN}), slot="A",
                  src={("x^2+a^2", 0): glyphs(self.slots["H"]["eq"], r"(x^2+a^2)^{3/2}", 0)}, rt=1.8, wait=1.2)
        self.show(E(r"x^2+a^2=a^2\left(1+\tan^2\alpha\right)", "x^2+a^2", r"a^2\left(1+\tan^2\alpha\right)", size=M_L,
                    colors={r"a^2\left(1+\tan^2\alpha\right)": CYAN}), (r"a^2\tan^2\alpha", r"a^2\left(1+\tan^2\alpha\right)"), slot="A", rt=1.6, wait=1.2)
        self.show(E(r"x^2+a^2=a^2\sec^2\alpha", "x^2+a^2", r"a^2\sec^2\alpha", size=M_L, colors={r"a^2\sec^2\alpha": CYAN}),
                  (r"a^2\left(1+\tan^2\alpha\right)", r"a^2\sec^2\alpha"), slot="A", rt=1.6, wait=1.2)
        self.show(E(r"(x^2+a^2)^{3/2}=a^3\sec^3\alpha", r"(x^2+a^2)^{3/2}", r"a^3\sec^3\alpha", size=M_L,
                    colors={r"a^3\sec^3\alpha": CYAN}), (r"x^2+a^2", r"(x^2+a^2)^{3/2}"), (r"a^2\sec^2\alpha", r"a^3\sec^3\alpha"),
                  slot="A", rt=1.8, wait=1.5)
        aux3 = A_()
        new = E(r"d\mathbf B=\frac{\mu_0 I}{4\pi}\frac{a\,a\sec^2\alpha\,d\alpha}{a^3\sec^3\alpha}\,\hat z", r"d\mathbf B", "I", r"\hat z",
                r"a\sec^2\alpha\,d\alpha", r"a^3\sec^3\alpha", r"\mu_0", "=", size=M_L,
                colors={r"a\sec^2\alpha\,d\alpha": CYAN, r"a^3\sec^3\alpha": CYAN})
        self.hl(r"(x^2+a^2)^{3/2}")
        self.show(new, (r"(x^2+a^2)^{3/2}", None), src={(r"a^3\sec^3\alpha", 0): glyphs(aux3, r"a^3\sec^3\alpha", 0)}, rt=2.4, wait=1.5)
        self.drop("A")
        self.mark("trecho_substituicao")
        # ── 8 · cancelamentos visíveis ───────────────────────────────────────────────────────────────────
        self.caption("Junte os $a$ do numerador")
        self.show(E(r"d\mathbf B=\frac{\mu_0 I}{4\pi}\frac{a^2\sec^2\alpha\,d\alpha}{a^3\sec^3\alpha}\,\hat z", r"d\mathbf B", "I", r"\hat z",
                    r"a^2\sec^2\alpha\,d\alpha", r"a^3\sec^3\alpha", r"\mu_0", "=", size=M_L,
                    colors={r"a^2\sec^2\alpha\,d\alpha": CYAN, r"a^3\sec^3\alpha": CYAN}),
                  (r"a\sec^2\alpha\,d\alpha", r"a^2\sec^2\alpha\,d\alpha"), rt=2.0, wait=1.2, structure=False)
        self.show(E(r"\frac{a^2}{a^3}=\frac{1}{a}\ ,\qquad\frac{\sec^2\alpha}{\sec^3\alpha}=\frac{1}{\sec\alpha}=\cos\alpha", r"\cos\alpha",
                    size=M_L, colors={r"\cos\alpha": CYAN}), slot="A", rt=1.8, wait=2.2)
        aux4 = A_()
        self.caption("Cancele potências de $a$ e as secantes")
        self.show(E(r"d\mathbf B=\frac{\mu_0 I}{4\pi a}\cos\alpha\,d\alpha\,\hat z", r"d\mathbf B", "I", r"\hat z", r"\cos\alpha",
                    r"d\alpha", r"\mu_0", "=", size=M_XL),
                  (r"a^2\sec^2\alpha\,d\alpha", r"d\alpha"), (r"a^3\sec^3\alpha", None),
                  src={(r"\cos\alpha", 0): glyphs(aux4, r"\cos\alpha", 0)}, rt=2.4, wait=2.0, structure=False)
        self.drop("A")
        self.mark("trecho_integrando")
        # ── 9 · limites ──────────────────────────────────────────────────────────────────────────────────
        self.relayout("split", 1.0)
        self.view_to(-4.0, -1.55, 1.12, 1.2)
        self.seg_flags["alpha"] = True
        self.x_src.set_value(-2.6)
        al_a = self.lab(r"\alpha_A", W([-2.6, 0, 0]) + np.array([0, -1.05, 0]), r"\alpha_A", size=M_M)
        al_b = self.lab(r"\alpha_B", W([2.6, 0, 0]) + np.array([0, -1.05, 0]), r"\alpha_B", size=M_M)
        self.play(FadeIn(al_a), FadeIn(al_b), run_time=0.8)
        self.caption("Os limites são os ângulos nas extremidades")
        self.show(E(r"\alpha_A<0<\alpha_B", r"\alpha_A", r"\alpha_B", size=M_L), slot="A", src={(r"\alpha_A", 0): al_a, (r"\alpha_B", 0): al_b},
                  rt=1.8, wait=1.5)
        aux = A_()
        self.show(E(r"B_{\rm trecho}=\frac{\mu_0 I}{4\pi a}\int_{\alpha_A}^{\alpha_B}\cos\alpha\,d\alpha", r"B_{\rm trecho}", "I", r"\cos\alpha", r"d\alpha",
                    r"\alpha_A", r"\alpha_B", r"\mu_0", "=", size=M_M),
                  (r"d\mathbf B", r"B_{\rm trecho}"), (r"\hat z", None),
                  src={(r"\alpha_A", 0): glyphs(aux, r"\alpha_A", 0), (r"\alpha_B", 0): glyphs(aux, r"\alpha_B", 0)}, rt=2.6, wait=1.5)
        self.show(E(r"B_{\rm trecho}=\frac{\mu_0 I}{4\pi a}[\sin\alpha]_{\alpha_A}^{\alpha_B}", r"B_{\rm trecho}", "I", r"\sin\alpha",
                    r"\alpha_A", r"\alpha_B", r"\mu_0", "=", size=M_M),
                  (r"\cos\alpha", r"\sin\alpha"), (r"d\alpha", None), rt=2.0, wait=1.5)
        self.show(E(r"B_{\rm trecho}=\frac{\mu_0 I}{4\pi a}\left(\sin\alpha_B-\sin\alpha_A\right)", r"B_{\rm trecho}", "I", r"\sin\alpha_A",
                    r"\sin\alpha_B", r"\mu_0", "=", size=M_M),
                  (r"\alpha_B", r"\sin\alpha_B"), (r"\alpha_A", r"\sin\alpha_A"), (r"\sin\alpha", None), rt=2.0, wait=1.5)
        self.mark("trecho_diferenca_senos")
        self.show(E(r"\alpha_A=-\alpha_1\ ,\quad\alpha_B=\alpha_2", r"\alpha_1", r"\alpha_2", size=M_M), slot="A", rt=1.4, wait=2.0)
        self.caption("Com $\\alpha_1,\\alpha_2>0$ a diferença de senos vira soma")
        self.show(E(r"B_{\rm trecho}=\frac{\mu_0 I}{4\pi a}\left(\sin\alpha_1+\sin\alpha_2\right)", r"B_{\rm trecho}", "I", r"\sin\alpha_1",
                    r"\sin\alpha_2", r"\mu_0", "=", size=M_M),
                  (r"\sin\alpha_A", r"\sin\alpha_1"), (r"\sin\alpha_B", r"\sin\alpha_2"), rt=2.2, wait=2.0)
        self.drop("A")
        bx = box(self.slots["H"]["eq"], MAG)
        self.play(FadeIn(bx), run_time=0.6)
        self.mark("resultado_trecho_finito")
        self.hold(3.5)
        self.play(FadeOut(bx), FadeOut(al_a), FadeOut(al_b), run_time=0.5)
        self.seg_geo, self.seg_extra = geo, VGroup(wire, flow, pl, dll, Rl)

    # ── fio infinito ────────────────────────────────────────────────────────────────────────────────────────
    def infinito(self):
        self.section("infinito", "O fio infinito como limite")
        W, a = self.W, self.A_FIO
        self.seg_geo.clear_updaters()
        self.play(FadeOut(self.seg_geo), FadeOut(self.seg_extra), run_time=0.8)
        self.Lw = ValueTracker(2.6)

        def geom():
            L, P = self.Lw.get_value(), W([0, a, 0])
            clip = 3.0
            g = VGroup(Line(W([-min(L, clip), 0, 0]), W([min(L, clip), 0, 0]), color=BLUE_L, stroke_width=7), Dot(P, radius=0.11),
                       DashedLine(W([0, 0, 0]), P, color=VIOLET, stroke_width=2.4))
            for s in (-1, 1):
                fr = min(1, clip / L)
                e = np.array([s * L * fr, a * (1 - fr), 0])
                g.add(Line(P, W(e), color=VIOLET, stroke_width=3))
                if L <= clip:
                    g.add(Dot(W([s * L, 0, 0]), color=GREEN, radius=0.09))
                else:
                    # a fonte continua além do quadro
                    g.add(arrow(W([s * clip, 0, 0]), W([s * (clip + 0.45), 0, 0]), BLUE_L, 6, tip=0.22))
                alv = math.atan2(L, a)
                g.add(ParametricFunction(lambda u, s=s: W(np.array([0, a, 0]) + 0.7 * np.array([s * math.sin(u), -math.cos(u), 0])),
                                         t_range=[0, alv], color=CYAN, stroke_width=3.2, fill_opacity=0))
            return g
        geo = self.cached(lambda: (self.Lw.get_value(), *self.view_key()), geom)
        pl = self.lab("P", W([0, a, 0]) + np.array([-0.3, 0.3, 0]), size=M_M)
        pl.add_updater(lambda m: m.move_to(W([0, a, 0]) + np.array([-0.3, 0.3, 0])))
        a1 = self.lab(r"\alpha_1", W([-0.75, a - 0.95, 0]), r"\alpha_1", size=M_M, colors={r"\alpha_1": CYAN})
        a2 = self.lab(r"\alpha_2", W([0.75, a - 0.95, 0]), r"\alpha_2", size=M_M, colors={r"\alpha_2": CYAN})
        self.add(geo)
        self.play(FadeIn(geo), FadeIn(pl), FadeIn(a1), FadeIn(a2), run_time=1.0)
        nums = VGroup(E(r"\alpha_1=\alpha_2=", size=M_S), DecimalNumber(0, num_decimal_places=1, unit=r"^\circ", font_size=40)).arrange(
            RIGHT, buff=0.2).move_to(AUX)
        nums[0].set_color(CYAN)
        nums[1].add_updater(lambda m: m.set_value(math.degrees(math.atan2(self.Lw.get_value(), a))))
        nums.update(0)
        card = self._card("A")
        self.play(FadeIn(card), FadeIn(nums), run_time=0.8)
        self.slots["A"]["eq"] = nums
        self.show(E(r"B_{\rm trecho}=\frac{\mu_0 I}{4\pi a}\left(\sin\alpha_1+\sin\alpha_2\right)", r"B_{\rm trecho}", "I", r"\sin\alpha_1",
                    r"\sin\alpha_2", r"\mu_0", "=", size=M_M), rt=1.2, wait=0.5)
        self.caption("$L\\to\\infty$: $\\alpha_1,\\alpha_2\\to90^\\circ$")
        self.play(self.Lw.animate.set_value(30), run_time=8, rate_func=smooth)
        self.mark("extremidades_distantes")
        nums.clear_updaters(recursive=True)
        self.show(E(r"\sin\alpha_1\to1\ ,\quad\sin\alpha_2\to1", r"\sin\alpha_1", r"\sin\alpha_2", size=M_M), slot="A", rt=1.4, wait=2.5)
        self.show(E(r"B_\infty=\frac{\mu_0 I}{4\pi a}\left(1+1\right)", r"B_\infty", "I", r"\mu_0", "=", size=M_M),
                  (r"B_{\rm trecho}", r"B_\infty"), (r"\sin\alpha_1", None), (r"\sin\alpha_2", None), rt=2.0, wait=2.0)
        self.show(E(r"B_\infty=\frac{\mu_0 I}{2\pi a}", r"B_\infty", "I", r"\mu_0", "=", size=M_L), rt=2.0, wait=1.5)
        self.drop("A")
        bx = box(self.slots["H"]["eq"], MAG)
        self.play(FadeIn(bx), run_time=0.5)
        self.caption("$B\\propto1/a$: o fio infinito nasce como limite do trecho finito")
        self.mark("resultado_fio_infinito")
        self.hold(4)
        self.play(FadeOut(bx), run_time=0.4)

    # ── força entre fios ────────────────────────────────────────────────────────────────────────────────────
    def fios_forca(self):
        self.section("fios", "A corrente cria o campo que produz a força")
        self.clear()
        X1, X2, YC = -5.3, -2.3, 0.1
        self.I2s = 1
        w1 = self.tube([X1, -2.0, 0], [X1, 2.0, 0])
        f1 = self.flow([lambda u: np.array([X1, -2.0 + 4.0 * u, 0])], count=8)
        a1 = arrow([X1 - 0.55, YC - 0.5, 0], [X1 - 0.55, YC + 0.6, 0], GREEN, 6)
        i1 = self.lab("I_1", [X1 - 1.0, YC + 0.05, 0], "I_1", size=M_S)
        self.play(Create(w1), run_time=1.0)
        self.add(f1)
        self.play(FadeIn(a1), FadeIn(i1), run_time=0.8)
        self.caption("Fio 1 com corrente $I_1$ para cima")
        self.hold(1.5)
        # campo de B₁: vista frontal, ⊗ à direita e ⊙ à esquerda; o raio acompanha a intensidade (∝ 1/r)
        syms = VGroup()
        for dist in (0.9, 1.7, 3.0):
            for yy in (YC - 1.3, YC, YC + 1.3):
                rad = 0.2 * min(1.0, 1.15 / dist) + 0.05
                syms.add(self.out_symbol(np.array([X1 + dist, yy, 0]), -1, rad))
                if dist < 3.0:
                    syms.add(self.out_symbol(np.array([X1 - dist - 0.4, yy, 0]), 1, rad))
        self.play(LaggedStart(*[FadeIn(s) for s in syms], lag_ratio=0.05), run_time=2.0)
        self.caption("Mão direita: à direita do fio, $\\mathbf B_1$ entra na tela; à esquerda, sai")
        p2 = np.array([X2, YC, 0])
        b1l = self.lab(r"\mathbf B_1", p2 + np.array([0.0, 0.55, 0]), r"\mathbf B_1", size=M_S)
        dline = VGroup(DashedLine([X1, -2.35, 0], [X2, -2.35, 0], color=VIOLET, stroke_width=3), self.lab("d", [(X1 + X2) / 2, -2.65, 0], "d", size=M_S))
        self.play(FadeIn(b1l), FadeIn(dline), run_time=1.0)
        self.hold(2.0)
        self.show(E(r"B_1=\frac{\mu_0 I_1}{2\pi d}", r"B_1", "I_1", "d", r"\mu_0", size=M_L),
                  src={(r"B_1", 0): b1l, ("I_1", 0): i1, ("d", 0): dline[1]}, rt=2.2, wait=1.5)
        self.mark("fios_campo_no_segundo")
        # fio 2, corrente I₂ (estado discreto: I2s = ±1)
        w2 = self.tube([X2, -2.0, 0], [X2, 2.0, 0])
        f2 = self.flow([lambda u: np.array([X2, -2.0 + 4.0 * u, 0])], count=8, direction=lambda: self.I2s)
        a2 = always_redraw(lambda: arrow([X2 + 0.55, YC - 0.55 * self.I2s, 0], [X2 + 0.55, YC + 0.55 * self.I2s, 0], GREEN, 6))
        i2 = self.lab("I_2", [X2 + 1.0, YC + 0.9, 0], "I_2", size=M_S)
        La = always_redraw(lambda: arrow([X2 + 0.2, YC - 0.9 * self.I2s - 0.6, 0], [X2 + 0.2, YC + 0.9 * self.I2s - 0.6, 0], GREEN, 3, tip=0.18))
        Lm = self.lab(r"\mathbf L", [X2 + 0.55, YC - 1.45, 0], r"\mathbf L", size=M_S)
        self.play(Create(w2), run_time=0.8)
        self.add(f2)
        self.play(FadeIn(a2), FadeIn(i2), FadeIn(La), FadeIn(Lm), run_time=0.9)
        fy = YC - 0.1
        fa = always_redraw(lambda: arrow([X2, fy, 0], [X2 - 1.4 * self.I2s, fy, 0], FC, 7))
        fm = self.lab(r"\mathbf F_2", [X2 - 0.9, fy - 0.45, 0], r"\mathbf F_2", size=M_S)
        self.play(Create(fa), FadeIn(fm), run_time=1.0)
        self.caption("Força no fio 2: $\\mathbf L\\times\\mathbf B_1$ aponta para o fio 1")
        self.show(E(r"\mathbf F_2=I_2\,\mathbf L\times\mathbf B_1", r"\mathbf F_2", "I_2", r"\mathbf L", r"\mathbf B_1", size=M_M), slot="A",
                  src={(r"\mathbf F_2", 0): fm, ("I_2", 0): i2, (r"\mathbf L", 0): Lm, (r"\mathbf B_1", 0): b1l}, rt=2.2, wait=1.5)
        aux = self.slots["A"]["eq"]
        self.show(E(r"F_2=I_2\,L\,\frac{\mu_0 I_1}{2\pi d}", "I_1", "I_2", r"\mu_0", "L", "=", size=M_L),
                  src={("I_2", 0): glyphs(aux, "I_2", 0), ("L", 0): glyphs(aux, r"\mathbf L", 0)}, rt=2.4, wait=1.5)
        self.show(E(r"\frac{F_2}{L}=\frac{\mu_0 I_1 I_2}{2\pi d}", "I_1", "I_2", r"\mu_0", "=", size=M_L), ("L", None), rt=2.2, wait=1.5)
        self.drop("A")
        unit = E(r"\left[\frac{F_2}{L}\right]=\mathrm{N/m}", size=M_S).move_to([3.95, 0.35, 0])
        self.play(FadeIn(unit), run_time=0.8)
        self.caption("Mesmo sentido de corrente: os fios se atraem")
        self.mark("fios_atracao")
        self.hold(3.5)
        self.play(FadeOut(unit), run_time=0.5)
        self.I2s = -1
        self.caption("Inverta $I_2$: $\\mathbf B_1$ não muda, a força inverte")
        self.mark("fios_repulsao")
        self.hold(7)
