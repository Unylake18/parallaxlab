"""Seções 2–3: regime magnetostático e geometria fonte–observador."""
import math

import numpy as np
from manim import (
    VGroup, Line, Dot, Polygon, ParametricFunction, FadeIn, FadeOut, Create, Indicate, ValueTracker, always_redraw, linear,
)
from base import *  # noqa: F401,F403


class Sec2:
    # ── regime magnetostático ───────────────────────────────────────────────────────────────────────────────
    def regime(self):
        self.section("regime", "Corrente estacionária: fluxo sem acúmulo")
        self.clear()
        Y = 0.35
        wire = self.tube([-6.9, Y, 0], [-0.9, Y, 0])
        region = Polygon([-5.4, -0.7, 0], [-2.4, -0.7, 0], [-2.4, 1.45, 0], [-5.4, 1.45, 0], color=VIOLET, fill_color=VIOLET,
                         fill_opacity=0.10, stroke_width=3).set_z_index(1)
        rlab = self.lab("V", [-2.75, 1.15, 0], size=M_S, color=VIOLET)
        self.play(Create(wire), Create(region), FadeIn(rlab), run_time=1.3)
        flow = self.flow([lambda u: np.array([-6.9 + 6.0 * u, Y, 0])], count=11)
        self.add(flow)
        self.Qt = ValueTracker(0.35)
        self.win, self.wout = ValueTracker(9), ValueTracker(3)
        gauge_frame = Polygon([-5.4, -2.15, 0], [-2.4, -2.15, 0], [-2.4, -1.75, 0], [-5.4, -1.75, 0], color=BLUE_L,
                              stroke_width=2.5, fill_opacity=0)
        gauge = always_redraw(lambda: Polygon([-5.4, -2.15, 0], [-5.4 + 3 * self.Qt.get_value(), -2.15, 0],
                                              [-5.4 + 3 * self.Qt.get_value(), -1.75, 0], [-5.4, -1.75, 0],
                                              color=BLUE_L, fill_color=BLUE_L, fill_opacity=0.85, stroke_width=0))
        ql = self.lab("Q", [-5.85, -1.95, 0], "Q", size=M_M)
        qd = txt("carga dentro de V", T_NOTE, color=DIM).move_to([-3.9, -1.3, 0])
        ain = always_redraw(lambda: arrow([-6.3, Y + 0.95, 0], [-5.55, Y + 0.95, 0], GREEN, self.win.get_value()))
        aout = always_redraw(lambda: arrow([-2.25, Y + 0.95, 0], [-1.5, Y + 0.95, 0], GREEN, self.wout.get_value()))
        lin = self.lab(r"I_{\rm entra}", [-5.9, Y + 1.6, 0], r"I_{\rm entra}", size=M_S)
        lout = self.lab(r"I_{\rm sai}", [-1.9, Y + 1.6, 0], r"I_{\rm sai}", size=M_S)
        self.play(FadeIn(gauge_frame), FadeIn(gauge), FadeIn(ql), FadeIn(qd), FadeIn(ain), FadeIn(aout), FadeIn(lin), FadeIn(lout),
                  run_time=1.0)
        self.caption("Se entra mais corrente do que sai, a carga dentro de $V$ cresce")
        self.play(self.Qt.animate.set_value(0.95), run_time=4.5, rate_func=linear)
        self.show(E(r"\frac{dQ}{dt}=I_{\rm entra}-I_{\rm sai}", r"\frac{dQ}{dt}", r"I_{\rm entra}", r"I_{\rm sai}", size=M_L),
                  src={(r"\frac{dQ}{dt}", 0): ql, (r"I_{\rm entra}", 0): lin, (r"I_{\rm sai}", 0): lout}, rt=2.0, wait=2.0)
        self.mark("regime_saldo")
        self.caption("Agora entra e sai a mesma corrente")
        self.play(self.wout.animate.set_value(9), run_time=1.5)
        self.hold(3.5)
        self.show(E(r"I_{\rm entra}=I_{\rm sai}\ \implies\ \frac{dQ}{dt}=0", r"I_{\rm entra}", r"I_{\rm sai}", r"\frac{dQ}{dt}", size=M_M),
                  rt=2.0, wait=2.5)
        self.caption("$Q$ permanece constante: a corrente atravessa $V$ sem se acumular")
        self.mark("regime_balanco")
        self.hold(3)
        jl = self.lab(r"\mathbf J", [-4.0, 1.05, 0], r"\mathbf J", size=M_M)
        rl = self.lab(r"\rho", [-3.2, -0.3, 0], r"\rho", size=M_M)
        self.play(FadeIn(jl), FadeIn(rl), run_time=0.8)
        self.show(E(r"\frac{\partial\rho}{\partial t}+\nabla\cdot\mathbf J=0", r"\frac{\partial\rho}{\partial t}",
                    r"\nabla\cdot\mathbf J", size=M_L),
                  src={(r"\frac{\partial\rho}{\partial t}", 0): rl, (r"\nabla\cdot\mathbf J", 0): jl}, rt=2.2, wait=2.0)
        self.caption("Forma local: $\\rho$ é a densidade de carga e $\\mathbf J$ a corrente por área")
        self.hold(3)
        self.show(E(r"\frac{\partial\rho}{\partial t}=0\ \implies\ \nabla\cdot\mathbf J=0", r"\frac{\partial\rho}{\partial t}",
                    r"\nabla\cdot\mathbf J", size=M_M), rt=2.0, wait=2.0)
        self.caption("Sem acúmulo num pequeno volume")
        self.mark("regime_divergente")
        self.hold(2)
        self.show(E(r"\frac{\partial\mathbf J}{\partial t}=0", size=M_L), slot="A", rt=1.2, wait=1.0)
        self.caption("Hipótese extra: a distribuição de corrente também é constante")
        self.mark("regime_hipoteses")
        self.hold(4)

    # ── geometria fonte–observador ──────────────────────────────────────────────────────────────────────────
    def local_pt(self):
        th, rd = self.theta_local.get_value(), self.Rd.get_value()
        return np.array([rd * math.cos(th), rd * math.sin(th), 0.0])

    def build_local(self):
        """Diagrama vivo: fonte f na origem, dℓ ao longo do fio, observador P a distância Rd e ângulo θ."""
        f = np.zeros(3)
        W = self.W
        L = {}
        L["wire"] = always_redraw(lambda: self.tube(W([-2.2, 0, 0]), W([3.6, 0, 0])))
        L["flow"] = self.flow([lambda u: W([-2.2 + 5.8 * u, 0, 0])], count=8)
        L["f"] = always_redraw(lambda: Dot(W(f), radius=0.1, color=GREEN).set_z_index(9))
        L["P"] = always_redraw(lambda: Dot(W(self.local_pt()), radius=0.11, color=WHITE).set_z_index(9))
        L["R"] = always_redraw(lambda: arrow(W(f), W(self.local_pt()), VIOLET, 5, z=6))
        L["dl"] = always_redraw(lambda: arrow(W(f), W([1.0, 0, 0]), GREEN, 8, z=7))
        L["guide"] = always_redraw(lambda: ParametricFunction(
            lambda u: W([self.Rd.get_value() * math.cos(u), self.Rd.get_value() * math.sin(u), 0]), t_range=[0.02, math.pi - 0.02],
            color=VIOLET, stroke_width=1.6, fill_opacity=0).set_stroke(opacity=0.28))
        L["arc"] = always_redraw(lambda: ParametricFunction(
            lambda u: W([0.62 * math.cos(u), 0.62 * math.sin(u), 0]), t_range=[0.001, max(0.002, self.theta_local.get_value())],
            color=WHITE, stroke_width=3, fill_opacity=0))
        pl = self.lab("P", [0, 0, 0], size=M_M)
        pl.add_updater(lambda m: m.move_to(W(self.local_pt()) + np.array([-0.05, 0.38, 0])))
        rl = self.lab(r"\mathbf R", [0, 0, 0], r"\mathbf R", size=M_M)
        rl.add_updater(lambda m: m.move_to(W(0.5 * self.local_pt()) + np.array(
            [-0.42 * math.sin(self.theta_local.get_value()) - 0.1, 0.42 * math.cos(self.theta_local.get_value()), 0])))
        dll = self.lab(r"d\boldsymbol\ell", W([0.5, -0.5, 0]), r"d\boldsymbol\ell", size=M_M)
        dll.add_updater(lambda m: m.move_to(W([0.5, -0.5, 0])))
        thl = self.lab(r"\theta", [0, 0, 0], r"\theta", size=M_M)
        thl.add_updater(lambda m: m.move_to(W([1.1 * math.cos(self.theta_local.get_value() / 2),
                                               1.1 * math.sin(self.theta_local.get_value() / 2), 0])))
        L.update(Pl=pl, Rl=rl, dll=dll, thl=thl)
        return L

    def geometria(self):
        self.section("geometria", "Construir a separação fonte–observador")
        self.clear()
        self.reset_view(x=-4.6, y=-1.2, scale=1.1)
        self.theta_local = ValueTracker(math.radians(58))
        self.Rd = ValueTracker(2.6)
        L = self.build_local()
        self.L = L
        W = self.W
        self.play(Create(L["wire"]), run_time=1.2)
        self.add(L["flow"])
        self.play(FadeIn(L["f"]), run_time=0.6)
        self.caption("Cada pedaço do fio é uma fonte do campo")
        self.hold(2)
        self.play(FadeIn(L["P"]), FadeIn(L["Pl"]), run_time=0.8)
        self.caption("Queremos o campo em um ponto $P$ qualquer do espaço")
        self.hold(2)
        o = np.array([-1.7, -1.1, 0])
        od = Dot(W(o), radius=0.07)
        ol = self.lab("O", W(o) + np.array([-0.3, -0.28, 0]), size=M_S)
        rp = arrow(W(o), W(np.zeros(3)), VIOLET, 3.5, z=5)
        rr = arrow(W(o), W(self.local_pt()), VIOLET, 3.5, z=5)
        rpl = self.lab(r"\mathbf r'", W(o / 2) + np.array([-0.35, 0.05, 0]), r"\mathbf r'", size=M_M)
        rrl = self.lab(r"\mathbf r", W(o + 0.45 * (self.local_pt() - o)) + np.array([0.15, -0.45, 0]), r"\mathbf r", size=M_M)
        self.play(FadeIn(od), FadeIn(ol), run_time=0.6)
        self.caption("Escolha uma origem $O$ qualquer")
        self.play(Create(rp), FadeIn(rpl), run_time=1.2)
        self.play(Create(rr), FadeIn(rrl), run_time=1.2)
        self.caption("$\\mathbf r'$ localiza a fonte; $\\mathbf r$ localiza o ponto $P$")
        self.hold(2)
        self.play(Create(L["R"]), FadeIn(L["Rl"]), run_time=1.2)
        self.caption("Dois caminhos de $O$ até $P$: direto, ou passando pela fonte")
        self.play(Indicate(rp, color=WHITE), Indicate(L["R"], color=WHITE), run_time=1.4)
        self.show(E(r"\mathbf r'+\mathbf R=\mathbf r", r"\mathbf r'", r"\mathbf R", r"\mathbf r", "+", "=", size=M_XL),
                  src={(r"\mathbf r'", 0): rpl, (r"\mathbf R", 0): L["Rl"], (r"\mathbf r", 0): rrl}, rt=2.2, wait=2.5)
        self.mark("geo_soma")
        self.caption("Isolando $\\mathbf R$: ele aponta da fonte até o observador")
        self.show(E(r"\mathbf R=\mathbf r-\mathbf r'", r"\mathbf r'", r"\mathbf R", r"\mathbf r", "-", "=", size=M_XL),
                  (r"\mathbf r'", r"\mathbf r'"), ("+", "-"), rt=2.2, wait=2.5)
        self.mark("geo_separacao")
        self.play(FadeOut(VGroup(od, ol, rp, rr, rpl, rrl)), run_time=0.8)
        self.caption("Fixe $P$ e mova a fonte: só $\\mathbf R$ muda")
        xs = ValueTracker(0.0)
        Pfix = self.local_pt()
        mv_dot = always_redraw(lambda: Dot(W([xs.get_value(), 0, 0]), radius=0.1, color=GREEN).set_z_index(10))
        mv_R = always_redraw(lambda: arrow(W([xs.get_value(), 0, 0]), W(Pfix), VIOLET, 5, z=6))
        self.play(FadeOut(L["R"]), FadeOut(L["Rl"]), FadeOut(L["f"]), FadeIn(mv_dot), FadeIn(mv_R), run_time=0.6)
        self.play(xs.animate.set_value(-1.4), run_time=2.0)
        self.play(xs.animate.set_value(1.8), run_time=3.0)
        self.play(xs.animate.set_value(0.0), run_time=1.5)
        self.play(FadeOut(mv_dot), FadeOut(mv_R), FadeIn(L["R"]), FadeIn(L["Rl"]), FadeIn(L["f"]), run_time=0.6)
        self.play(Create(L["dl"]), FadeIn(L["dll"]), run_time=1.0)
        self.play(Create(L["arc"]), FadeIn(L["thl"]), run_time=1.0)
        self.caption("$d\\boldsymbol\\ell$ é o elemento de fio, tangente à corrente; $\\theta$ é o ângulo entre $d\\boldsymbol\\ell$ e $\\mathbf R$")
        self.show(E(r"\theta=\angle\left(d\boldsymbol\ell,\mathbf R\right)", r"\theta", r"d\boldsymbol\ell", r"\mathbf R", size=M_M),
                  slot="A", src={(r"\theta", 0): L["thl"], (r"d\boldsymbol\ell", 0): L["dll"], (r"\mathbf R", 0): L["Rl"]},
                  rt=2.0, wait=3.5)
        self.mark("geometria_fonte_observador")
