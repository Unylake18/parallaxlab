"""Seções 5–8: correntes distribuídas, clínica do ângulo (produto vetorial), superposição e método geral."""
import math

import numpy as np
from manim import (
    VGroup, Line, DashedLine, Dot, Polygon, ParametricFunction, Axes, FadeIn, FadeOut, Create, Indicate, ValueTracker,
    always_redraw, linear, smooth, DecimalNumber, LaggedStart, TransformFromCopy, Transform, ReplacementTransform,
    UP, DOWN, LEFT, RIGHT,
)
from base import *  # noqa: F401,F403


class Sec4:
    # ── correntes distribuídas ──────────────────────────────────────────────────────────────────────────────
    def distribuidas(self):
        self.section("distribuidas", "Da linha à superfície e ao volume")
        self.clear()
        self.reset_view(x=-4.3, y=-0.7, scale=1.0, beta=30, tau=24)
        W = self.W
        self.dw, self.dh = ValueTracker(0.0), ValueTracker(0.0)
        X = 2.3

        def geometry():
            w, h = self.dw.get_value(), self.dh.get_value()
            g = VGroup(Line(W([-X, 0, 0]), W([X, 0, 0]), color=BLUE_L, stroke_width=7 if w < 0.05 else 3))
            if w > 0.02:
                g.add(Polygon(W([-X, -w, 0]), W([X, -w, 0]), W([X, w, 0]), W([-X, w, 0]), color=BLUE_L, fill_color=BLUE_L,
                              fill_opacity=0.14, stroke_width=2.5))
                if h > 0.02:
                    top = [W([-X, -w, h]), W([X, -w, h]), W([X, w, h]), W([-X, w, h])]
                    g.add(Polygon(*top, color=BLUE_L, fill_color=BLUE_L, fill_opacity=0.10, stroke_width=2.5))
                    for yy in (-w, w):
                        g.add(Polygon(W([-X, yy, 0]), W([X, yy, 0]), W([X, yy, h]), W([-X, yy, h]), color=BLUE_L,
                                      fill_color=BLUE_L, fill_opacity=0.08, stroke_width=2))
                    for xx in (-X, X):
                        g.add(Polygon(W([xx, -w, 0]), W([xx, w, 0]), W([xx, w, h]), W([xx, -w, h]), color=BLUE_L,
                                      fill_color=BLUE_L, fill_opacity=0.08, stroke_width=2))
            return g
        geo = self.cached(lambda: (self.dw.get_value(), self.dh.get_value(), *self.view_key()), geometry)
        paths = [lambda u, yy=yy, zz=zz: W([-X + 2 * X * u, yy * self.dw.get_value(), zz * self.dh.get_value()])
                 for yy in (-0.8, -0.4, 0, 0.4, 0.8) for zz in (0.15, 0.85)]
        flows = self.flow(paths, count=4)
        self.add(geo, flows)
        self.play(FadeIn(geo), run_time=0.8)
        H = lambda: self.slots["H"]["eq"]
        # ── linha ─────────────────────────────────────────────────────────────────────────────────────────
        el = Line(W([-0.4, 0, 0]), W([0.4, 0, 0]), color=GREEN, stroke_width=11).set_z_index(9)
        dll = self.lab(r"d\boldsymbol\ell", W([0, -0.55, 0]), r"d\boldsymbol\ell", size=M_M)
        il = self.lab("I", W([-1.5, 0.5, 0]), "I", size=M_M)
        self.play(Create(el), FadeIn(dll), FadeIn(il), run_time=1.0)
        self.caption("Fio fino: a fonte é a corrente $I$ no elemento $d\\boldsymbol\\ell$")
        self.show(E(r"I\,d\boldsymbol\ell", "I", r"d\boldsymbol\ell", size=M_XL), src={("I", 0): il, (r"d\boldsymbol\ell", 0): dll},
                  rt=1.8, wait=1.0)
        self.show(E(r"\mathbf B=\frac{\mu_0}{4\pi}\int\frac{I\,d\boldsymbol\ell\times\hat{\mathbf R}}{R^2}", r"\mathbf B", "I",
                    r"d\boldsymbol\ell", r"\hat{\mathbf R}", "R^2", r"\times", size=M_M), slot="A",
                  src={("I", 0): glyphs(H(), "I", 0), (r"d\boldsymbol\ell", 0): glyphs(H(), r"d\boldsymbol\ell", 0)}, rt=2.0, wait=1.5)
        self.mark("distribuicao_linha")
        # ── superfície: dI = K dw ─────────────────────────────────────────────────────────────────────────
        self.caption("Numa lâmina, a corrente se espalha em largura")
        self.play(FadeOut(el), FadeOut(il), FadeOut(dll), self.dw.animate.set_value(0.95), run_time=2.5)
        patch = Polygon(W([-0.4, -0.3, 0]), W([0.4, -0.3, 0]), W([0.4, 0.3, 0]), W([-0.4, 0.3, 0]), color=GREEN, fill_color=GREEN,
                        fill_opacity=0.35, stroke_width=3).set_z_index(9)
        tarr = arrow(W([-0.5, 0.62, 0]), W([0.5, 0.62, 0]), GREEN, 5, z=9)
        tl = self.lab(r"\hat{\mathbf t}", W([0.0, 0.95, 0]), r"\hat{\mathbf t}", size=M_M)
        kl = self.lab("K", W([-1.5, -0.1, 0]), "K", size=M_M)
        dwl = self.lab("dw", W([0.78, 0.0, 0]), "dw", size=M_M)
        dl2 = self.lab(r"d\ell", W([0, -0.62, 0]), r"d\ell", size=M_M)
        dwbr = VGroup(Line(W([0.52, -0.3, 0]), W([0.52, 0.3, 0]), color=VIOLET, stroke_width=3),
                      Line(W([0.46, -0.3, 0]), W([0.58, -0.3, 0]), color=VIOLET, stroke_width=3),
                      Line(W([0.46, 0.3, 0]), W([0.58, 0.3, 0]), color=VIOLET, stroke_width=3))
        self.play(Create(patch), FadeIn(dwbr), FadeIn(dwl), FadeIn(dl2), FadeIn(kl), Create(tarr), FadeIn(tl), run_time=1.5)
        self.caption("A corrente na faixa de largura $dw$ é $dI=K\\,dw$")
        self.show(E(r"dI=K\,dw", "dI", "K", "dw", size=M_XL), ("I", "dI"), (r"d\boldsymbol\ell", None),
                  src={("K", 0): kl, ("dw", 0): dwl}, rt=2.2, wait=1.0)
        self.show(E(r"d\boldsymbol\ell=\hat{\mathbf t}\,d\ell", r"d\boldsymbol\ell", r"\hat{\mathbf t}", r"d\ell", size=M_M), slot="A",
                  src={(r"\hat{\mathbf t}", 0): tl, (r"d\ell", 0): dl2, (r"d\boldsymbol\ell", 0): dl2}, rt=1.8, wait=1.2)
        aux = self.slots["A"]["eq"]
        self.caption("O elemento de comprimento é o versor $\\hat{\\mathbf t}$ vezes $d\\ell$")
        self.show(E(r"dI\,d\boldsymbol\ell=K\,dw\,\hat{\mathbf t}\,d\ell", "dI", r"d\boldsymbol\ell", "K", "dw", r"\hat{\mathbf t}", r"d\ell", size=M_L),
                  src={(r"d\boldsymbol\ell", 0): glyphs(aux, r"d\boldsymbol\ell", 0), (r"\hat{\mathbf t}", 0): glyphs(aux, r"\hat{\mathbf t}", 0),
                       (r"d\ell", 0): glyphs(aux, r"d\ell", 0)}, rt=2.4, wait=1.2)
        self.show(E(r"\mathbf K=K\,\hat{\mathbf t}", r"\mathbf K", "K", r"\hat{\mathbf t}", size=M_M), slot="A",
                  src={("K", 0): glyphs(H(), "K", 0), (r"\hat{\mathbf t}", 0): glyphs(H(), r"\hat{\mathbf t}", 0)}, rt=1.8, wait=1.2)
        aux = self.slots["A"]["eq"]
        self.caption("$\\mathbf K=K\\hat{\\mathbf t}$ é a corrente por unidade de largura, em A/m")
        self.show(E(r"dI\,d\boldsymbol\ell=\mathbf K\,dw\,d\ell", "dI", r"d\boldsymbol\ell", r"\mathbf K", "dw", r"d\ell", size=M_L),
                  ("K", None), (r"\hat{\mathbf t}", None), src={(r"\mathbf K", 0): glyphs(aux, r"\mathbf K", 0)}, rt=2.2, wait=1.2)
        self.show(E(r"da=dw\,d\ell", "da", "dw", r"d\ell", size=M_M), slot="A",
                  src={("dw", 0): glyphs(H(), "dw", 0), (r"d\ell", 0): glyphs(H(), r"d\ell", 0)}, rt=1.8, wait=1.2)
        aux = self.slots["A"]["eq"]
        self.caption("$da=dw\\,d\\ell$ é a área do elemento de superfície")
        self.show(E(r"dI\,d\boldsymbol\ell=\mathbf K\,da", "dI", r"d\boldsymbol\ell", r"\mathbf K", "da", size=M_XL),
                  ("dw", None), (r"d\ell", None), src={("da", 0): glyphs(aux, "da", 0)}, rt=2.2, wait=1.2)
        hs = H()
        self.show(E(r"\mathbf B=\frac{\mu_0}{4\pi}\int\frac{\mathbf K\times\hat{\mathbf R}}{R^2}\,da", r"\mathbf B", r"\mathbf K",
                    r"\hat{\mathbf R}", "R^2", r"\times", "da", size=M_M), slot="A",
                  src={(r"\mathbf K", 0): glyphs(hs, r"\mathbf K", 0), ("da", 0): glyphs(hs, "da", 0)}, rt=2.4, wait=2.0)
        self.mark("distribuicao_superficie")
        # ── volume: dI = J dA⊥ ────────────────────────────────────────────────────────────────────────────
        self.caption("Num volume, a corrente atravessa uma seção transversal")
        self.play(FadeOut(VGroup(patch, kl, dwl, dl2, dwbr, tarr, tl)), self.dh.animate.set_value(0.9), run_time=2.5)
        sec = Polygon(W([0.4, -0.3, 0]), W([0.4, 0.3, 0]), W([0.4, 0.3, 0.9]), W([0.4, -0.3, 0.9]), color=VIOLET, fill_color=VIOLET,
                      fill_opacity=0.35, stroke_width=3).set_z_index(9)
        jl = self.lab("J", W([-1.5, 0.0, 0.45]), "J", size=M_M)
        dal = self.lab(r"dA_\perp", W([0.4, 0.0, 0.45]) + np.array([0.75, 0.15, 0]), r"dA_\perp", size=M_M)
        tl2 = self.lab(r"\hat{\mathbf t}", W([0.0, 0.0, 1.35]), r"\hat{\mathbf t}", size=M_M)
        tarr2 = arrow(W([-0.55, 0.0, 1.05]), W([0.5, 0.0, 1.05]), GREEN, 5, z=9)
        dl3 = self.lab(r"d\ell", W([0.0, -0.55, 0.0]), r"d\ell", size=M_M)
        self.play(Create(sec), FadeIn(dal), FadeIn(jl), FadeIn(dl3), Create(tarr2), FadeIn(tl2), run_time=1.6)
        self.caption("A corrente na seção $dA_\\perp$ é $dI=J\\,dA_\\perp$")
        self.show(E(r"dI=J\,dA_\perp", "dI", "J", r"dA_\perp", size=M_XL), ("dI", "dI"), (r"\mathbf K", None), ("da", None),
                  (r"d\boldsymbol\ell", None), src={("J", 0): jl, (r"dA_\perp", 0): dal}, rt=2.2, wait=1.0)
        self.show(E(r"\mathbf J=J\,\hat{\mathbf t}", r"\mathbf J", "J", r"\hat{\mathbf t}", size=M_M), slot="A",
                  src={("J", 0): glyphs(H(), "J", 0), (r"\hat{\mathbf t}", 0): tl2}, rt=1.8, wait=1.2)
        aux = self.slots["A"]["eq"]
        self.caption("$\\mathbf J=J\\hat{\\mathbf t}$ é a corrente por unidade de área transversal, em A/m²")
        self.show(E(r"dI\,d\boldsymbol\ell=\mathbf J\,dA_\perp\,d\ell", "dI", r"d\boldsymbol\ell", r"\mathbf J", r"dA_\perp", r"d\ell", size=M_L),
                  ("J", None), src={(r"\mathbf J", 0): glyphs(aux, r"\mathbf J", 0), (r"d\boldsymbol\ell", 0): dl3, (r"d\ell", 0): dl3},
                  rt=2.4, wait=1.2)
        self.show(E(r"d\tau=dA_\perp\,d\ell", r"d\tau", r"dA_\perp", r"d\ell", size=M_M), slot="A",
                  src={(r"dA_\perp", 0): glyphs(H(), r"dA_\perp", 0), (r"d\ell", 0): glyphs(H(), r"d\ell", 0)}, rt=1.8, wait=1.2)
        aux = self.slots["A"]["eq"]
        blk = VGroup(*[Polygon(W([-0.4, -0.3, zz]), W([0.4, -0.3, zz]), W([0.4, 0.3, zz]), W([-0.4, 0.3, zz]), color=GREEN,
                               fill_color=GREEN, fill_opacity=0.25, stroke_width=3) for zz in (0, 0.9)])
        for xx in (-0.4, 0.4):
            for yy in (-0.3, 0.3):
                blk.add(Line(W([xx, yy, 0]), W([xx, yy, 0.9]), color=GREEN, stroke_width=3))
        self.play(Create(blk.set_z_index(8)), run_time=1.2)
        self.caption("A seção percorre $d\\ell$ e varre o volume $d\\tau$")
        self.show(E(r"dI\,d\boldsymbol\ell=\mathbf J\,d\tau", "dI", r"d\boldsymbol\ell", r"\mathbf J", r"d\tau", size=M_XL),
                  (r"dA_\perp", None), (r"d\ell", None), src={(r"d\tau", 0): glyphs(aux, r"d\tau", 0)}, rt=2.2, wait=1.2)
        hv = H()
        self.show(E(r"\mathbf B=\frac{\mu_0}{4\pi}\int\frac{\mathbf J\times\hat{\mathbf R}}{R^2}\,d\tau", r"\mathbf B", r"\mathbf J",
                    r"\hat{\mathbf R}", "R^2", r"\times", r"d\tau", size=M_M), slot="A",
                  src={(r"\mathbf J", 0): glyphs(hv, r"\mathbf J", 0), (r"d\tau", 0): glyphs(hv, r"d\tau", 0)}, rt=2.4, wait=2.0)
        self.caption("A medida de integração acompanha a distribuição: $d\\ell$, $da$ ou $d\\tau$")
        self.mark("distribuicao_volume")
        self.hold(3)

    # ── clínica do ângulo ───────────────────────────────────────────────────────────────────────────────────
    def clinica(self):
        self.section("clinica", "Isolar o efeito do ângulo")
        self.clear()
        self.reset_view(x=-4.5, y=-1.3, scale=1.05)
        self.theta_local = ValueTracker(math.radians(35))
        self.Rd = ValueTracker(2.4)
        L = self.build_local()
        self.L = L
        W, th = self.W, self.theta_local
        # só o elemento e sua vizinhança: P nunca cai sobre o filamento
        L["wire"] = always_redraw(lambda: self.tube(W([-0.8, 0, 0]), W([1.3, 0, 0])))
        L["flow"] = self.flow([lambda u: W([-0.8 + 2.1 * u, 0, 0])], count=4)
        dbs = always_redraw(lambda: self.out_symbol(W(self.local_pt()) + np.array([0.62, 0, 0]), 1,
                                                    radius=max(0.0, 0.24 * math.sin(th.get_value()))) if math.sin(th.get_value()) > 0.02 else VGroup())
        dbl = self.lab(r"d\mathbf B", [0, 0, 0], r"d\mathbf B", size=M_M)
        dbl.add_updater(lambda m: m.move_to(W(self.local_pt()) + np.array([1.25, 0, 0])).set_opacity(1.0 if math.sin(th.get_value()) > 0.03 else 0.0))
        zero_l = self.lab(r"dB=0", [0, 0, 0], "dB", size=M_M)
        zero_l.add_updater(lambda m: m.move_to(W(self.local_pt()) + np.array([0, 0.55, 0])).set_opacity(0.0 if math.sin(th.get_value()) > 0.03 else 1.0))
        self.add(zero_l)
        self.add(L["wire"], L["flow"], L["f"], L["P"], L["R"], L["dl"], L["guide"], L["arc"], L["Pl"], L["Rl"], L["dll"], L["thl"], dbs, dbl)
        self.play(FadeIn(VGroup(L["wire"], L["f"], L["P"], L["R"], L["dl"], L["Pl"], L["Rl"], L["dll"], L["guide"])), run_time=1.2)
        self.show(E(r"dB\propto\sin\theta", "dB", r"\sin\theta", r"\propto", size=M_XL),
                  src={("dB", 0): dbl, (r"\sin\theta", 0): L["thl"]}, rt=2.0, wait=1.0)
        # gráfico de sinθ no cartão auxiliar
        ax = Axes(x_range=[0, math.pi, math.pi / 2], y_range=[0, 1.15, 1], x_length=4.7, y_length=1.55,
                  axis_config={"color": DIM, "stroke_width": 2, "include_ticks": False}, tips=False).move_to(AUX + np.array([0, -0.15, 0]))
        curve = ax.plot(lambda t: math.sin(t), x_range=[0, math.pi], color=MAG, stroke_width=4)
        dot = always_redraw(lambda: Dot(ax.c2p(th.get_value(), math.sin(th.get_value())), radius=0.09, color=WHITE).set_z_index(8))
        drop_l = always_redraw(lambda: DashedLine(ax.c2p(th.get_value(), 0), ax.c2p(th.get_value(), math.sin(th.get_value())), color=WHITE,
                                                  stroke_width=2))
        ticks = VGroup(txt("0°", 20, DIM).next_to(ax.c2p(0, 0), DOWN, buff=0.1), txt("90°", 20, DIM).next_to(ax.c2p(math.pi / 2, 0), DOWN, buff=0.1),
                       txt("180°", 20, DIM).next_to(ax.c2p(math.pi, 0), DOWN, buff=0.1), self.lab(r"\sin\theta", ax.c2p(0, 1.15) + np.array([0.55, 0.0, 0]), size=26))
        card = self._card("A")
        self.play(FadeIn(card), Create(ax), Create(curve), FadeIn(ticks), FadeIn(dot), FadeIn(drop_l), run_time=1.5)
        self.slots["A"]["eq"] = VGroup(ax, curve, ticks, dot, drop_l)
        self.play(th.animate.set_value(0.0), run_time=2.5)
        self.caption("$\\theta=0$: $dB=0$, embora a corrente continue")
        self.mark("clinica_zero")
        self.hold(3)
        for ang, note in [(30, "$\\theta=30^\\circ$"), (60, "$\\theta=60^\\circ$"), (90, "$\\theta=90^\\circ$: contribuição máxima para este $R$"),
                          (150, "$\\theta=150^\\circ$: volta a enfraquecer"), (180, "$\\theta=180^\\circ$: oposto ao elemento, também zero")]:
            self.delcap()
            self.play(th.animate.set_value(math.radians(ang)), run_time=3, rate_func=linear)
            self.caption(note)
            self.mark(f"clinica_{ang}")
            self.hold(2)
        self.play(th.animate.set_value(math.pi / 2), run_time=2)
        # mão direita em 2.5D
        self.drop("A")
        self.caption("Mas o produto vetorial também dá a direção: vamos olhar em perspectiva")
        self.remove(dbs)
        self.play(FadeOut(dbl), run_time=0.4)
        b3 = always_redraw(lambda: self.vec(self.local_pt(), [0, 0, 1], MAG, scale=1.3 * math.sin(th.get_value()) + 0.001, width=7))
        b3l = self.lab(r"d\mathbf B", [0, 0, 0], r"d\mathbf B", size=M_M)
        b3l.add_updater(lambda m: m.move_to(W(self.local_pt() + np.array([0, 0, 1.3 * math.sin(th.get_value())])) + np.array([0.55, 0.15, 0])))
        turn = always_redraw(lambda: ParametricFunction(lambda u: W([1.35 * math.cos(u), 1.35 * math.sin(u), 0]),
                                                       t_range=[0.001, max(0.002, th.get_value())], color=WHITE, stroke_width=4,
                                                       fill_opacity=0))
        self.add(b3, b3l, turn)
        self.play(self.beta.animate.set_value(32), self.tau.animate.set_value(52), run_time=3)
        self.play(FadeIn(b3), FadeIn(b3l), run_time=0.8)
        self.caption("Dedos de $d\\boldsymbol\\ell$ para $\\mathbf R$; o polegar dá o sentido de $d\\mathbf B$")
        self.hold(4)
        self.mark("clinica_perpendicular_espacial")
        self.show(E(r"d\boldsymbol\ell\times\mathbf R=-\,\mathbf R\times d\boldsymbol\ell", r"d\boldsymbol\ell", r"\mathbf R", r"\times", size=M_L),
                  slot="A", src={(r"d\boldsymbol\ell", 0): L["dll"], (r"\mathbf R", 0): L["Rl"]}, rt=1.8, wait=1.0)
        self.caption("Trocar a ordem dos fatores inverte $d\\mathbf B$")
        b4 = always_redraw(lambda: self.vec(self.local_pt(), [0, 0, -1], MAG, scale=1.3, width=7))
        self.play(FadeOut(b3), run_time=0.3)
        self.add(b4)
        self.play(FadeIn(b4), run_time=0.8)
        self.hold(3)
        self.remove(b4)

    # ── superposição ────────────────────────────────────────────────────────────────────────────────────────
    def superposicao(self):
        from fisica import trecho
        self.section("superposicao", "Construir uma soma vetorial")
        self.clear()
        self.reset_view(x=-4.0, y=-1.0, scale=0.95, beta=0, tau=44)
        W = self.W
        wire = self.tube(W([-2.5, 0, 0]), W([2.5, 0, 0]))
        P = np.array([0.0, 2.1, 0.0])
        pd = Dot(W(P), color=WHITE, radius=0.1)
        pl = self.lab("P", W(P) + np.array([-0.35, 0.2, 0]), size=M_M)
        flow = self.flow([lambda u: W([-2.5 + 5 * u, 0, 0])])
        self.play(Create(wire), FadeIn(pd), FadeIn(pl), run_time=1.0)
        self.add(flow)
        self.caption("Um observador $P$; cada elemento da fonte dá uma contribuição")
        self.hold(1.5)
        SC = 2.75
        base = np.array([-0.7, -2.6, 0.0])
        start = base.copy()
        chain, labels, firsts = VGroup(), [], []
        for i, x in enumerate(np.linspace(-2, 2, 5)):
            f, pt, dl, Rv, rm, thv, al, b = trecho(x, dl=1.0)
            src = VGroup(Dot(W(f), color=GREEN, radius=0.09), self.vec(f, dl, GREEN, width=6), self.vec(f, Rv, VIOLET, width=3))
            contrib = self.vec(pt, b, MAG, scale=SC * 2.4, width=6)
            self.play(FadeIn(src), Create(contrib), run_time=0.8)
            delta = W(pt + SC * 2.4 * b) - W(pt)
            target = arrow(base, base + delta, MAG, width=5, tip=0.16)
            self.play(TransformFromCopy(contrib, target), run_time=1.0)
            chain.add(target)
            firsts.append(target)
            base = base + delta
            self.play(FadeOut(src), FadeOut(contrib), run_time=0.35)
        lab1 = self.lab(r"\Delta\mathbf B_1", firsts[0].get_center() + np.array([-0.65, 0, 0]), r"\Delta\mathbf B_1", size=M_S)
        lab2 = self.lab(r"\Delta\mathbf B_2", firsts[1].get_center() + np.array([-0.65, 0, 0]), r"\Delta\mathbf B_2", size=M_S)
        lab5 = self.lab(r"\Delta\mathbf B_5", firsts[4].get_center() + np.array([-0.65, 0, 0]), r"\Delta\mathbf B_5", size=M_S)
        self.play(FadeIn(lab1), FadeIn(lab2), FadeIn(lab5), run_time=0.8)
        total = arrow(start + np.array([0.8, 0, 0]), base + np.array([0.8, 0, 0]), MAG, width=8)
        tl = self.lab(r"\mathbf B", base + np.array([1.15, -1.2, 0]), r"\mathbf B", size=M_M)
        self.play(Create(total), FadeIn(tl), run_time=1.2)
        self.caption("Ponta a ponta: a resultante liga a origem à ponta final da soma")
        self.show(E(r"\mathbf B\approx\Delta\mathbf B_1+\Delta\mathbf B_2+\cdots+\Delta\mathbf B_5", r"\mathbf B", r"\Delta\mathbf B_1",
                    r"\Delta\mathbf B_2", r"\Delta\mathbf B_5", size=M_M),
                  src={(r"\mathbf B", 0): tl, (r"\Delta\mathbf B_1", 0): lab1, (r"\Delta\mathbf B_2", 0): lab2, (r"\Delta\mathbf B_5", 0): lab5},
                  rt=2.4, wait=2.5)
        self.mark("soma_ponta_cauda")
        # refinar
        small = VGroup(*[Line(W([x, 0, 0]), W([x + 0.14, 0, 0]), color=GREEN, stroke_width=9) for x in np.arange(-2.5, 2.4, 0.25)])
        self.play(Create(small), run_time=2)
        self.caption("Refinar a fonte: mais elementos, cada contribuição menor")
        fine, tip = VGroup(), start.copy()
        for x in np.linspace(-2.375, 2.375, 20):
            b = trecho(x, dl=0.25)[-1]
            d = W(P + SC * 2.4 * b) - W(P)
            fine.add(arrow(tip, tip + d, MAG, width=3, tip=0.08))
            tip = tip + d
        self.play(ReplacementTransform(chain, fine), Transform(total, arrow(start + np.array([0.8, 0, 0]), tip + np.array([0.8, 0, 0]), MAG, width=8)),
                  FadeOut(lab1), FadeOut(lab2), FadeOut(lab5), run_time=2.4)
        self.show(E(r"\mathbf B\approx\sum_{i=1}^{N}\Delta\mathbf B_i", r"\mathbf B", r"\sum_{i=1}^{N}", r"\Delta\mathbf B_i", size=M_L),
                  (r"\Delta\mathbf B_1", r"\Delta\mathbf B_i"), (r"\Delta\mathbf B_2", None), (r"\Delta\mathbf B_5", None), rt=2.2, wait=2.0)
        self.show(E(r"\mathbf B=\int d\mathbf B", r"\mathbf B", r"\int", r"d\mathbf B", size=M_XL),
                  (r"\sum_{i=1}^{N}", r"\int"), (r"\Delta\mathbf B_i", r"d\mathbf B"),
                  rt=2.2, wait=2.0)
        self.caption("No limite $\\Delta\\ell\\to0$ e $N\\to\\infty$, a soma vira integral")
        self.mark("integral_superposicao")
        self.hold(3)

    # ── método geral ────────────────────────────────────────────────────────────────────────────────────────
    def metodo(self):
        self.section("metodo", "Aplicar o método ao desenho")
        self.clear()
        self.reset_view(x=-4.0, y=-1.3, scale=1.0)
        W = self.W
        wire = self.tube(W([-2.5, 0, 0]), W([2.5, 0, 0]))
        P = np.array([0.0, 2.1, 0.0])
        f = np.array([1.5, 0.0, 0.0])
        pd, pl = Dot(W(P), radius=0.1), self.lab("P", W(P) + np.array([-0.3, 0.3, 0]), size=M_M)
        flow = self.flow([lambda u: W([-2.5 + 5 * u, 0, 0])])
        self.play(Create(wire), FadeIn(pd), FadeIn(pl), run_time=1.0)
        self.add(flow)
        steps = ["1  separação  $\\mathbf R$", "2  direção de $d\\mathbf B$", "3  elemento $d\\boldsymbol\\ell$ e variável", "4  limites e integral"]
        rows = VGroup(*[rich(s, 26, DIM) for s in steps]).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(AUX)
        rows.align_to(AUX + np.array([-2.7, 0, 0]), LEFT)
        card = self._card("A")
        self.play(FadeIn(card), FadeIn(rows), run_time=1.0)
        self.slots["A"]["eq"] = rows

        def hot(i):
            for j, r in enumerate(rows):
                r.set_color(WHITE if j == i else DIM)
        self.caption("Quem produz o campo e onde queremos calculá-lo?")
        self.hold(1.2)
        hot(0)
        fd = Dot(W(f), color=GREEN, radius=0.1)
        sep = arrow(W(f), W(P), VIOLET, 5, z=6)
        rl = self.lab(r"\mathbf R", W((f + P) / 2) + np.array([0.4, 0.1, 0]), r"\mathbf R", size=M_M)
        self.play(FadeIn(fd), Create(sep), FadeIn(rl), run_time=1.2)
        self.show(E(r"\mathbf R=\mathbf r-\mathbf r'", r"\mathbf R", r"\mathbf r", r"\mathbf r'", size=M_L), src={(r"\mathbf R", 0): rl}, rt=1.6, wait=1.5)
        self.caption("A geometria fornece a distância e a direção de $\\mathbf R$")
        hot(1)
        out = self.out_symbol(W(P) + np.array([0.55, 0.0, 0]), 1, 0.2)
        dbl = self.lab(r"d\mathbf B", W(P) + np.array([1.2, 0, 0]), r"d\mathbf B", size=M_M)
        self.play(FadeIn(out), FadeIn(dbl), run_time=0.9)
        self.caption("Pela regra da mão direita, todas as parcelas apontam para fora da tela")
        self.hold(1.5)
        hot(2)
        xa = self.lab("x_A", W([-2.5, -0.5, 0]), "x_A", size=M_M, color=VIOLET)
        xb = self.lab("x_B", W([2.5, -0.5, 0]), "x_B", size=M_M, color=VIOLET)
        dxl = self.lab(r"d\boldsymbol\ell", W([1.5, -0.55, 0]), r"d\boldsymbol\ell", size=M_M)
        self.play(FadeIn(xa), FadeIn(xb), FadeIn(dxl), run_time=0.9)
        self.show(E(r"d\boldsymbol\ell=dx\,\hat x", r"d\boldsymbol\ell", "dx", r"\hat x", size=M_L), src={(r"d\boldsymbol\ell", 0): dxl}, rt=1.8, wait=1.5)
        self.caption("Percorrer o fio é percorrer $x$: o elemento é $dx$ no sentido de $\\hat x$")
        hot(3)
        self.show(E(r"B_{\rm trecho}=\int_{x_A}^{x_B}dB", r"B_{\rm trecho}", "x_A", "x_B", "dB", size=M_L,
                    colors={"x_A": VIOLET, "x_B": VIOLET}),
                  src={("x_A", 0): xa, ("x_B", 0): xb, ("dB", 0): dbl}, rt=2.2, wait=2.5)
        self.mark("metodo_aplicado")
        self.hold(1.2)
