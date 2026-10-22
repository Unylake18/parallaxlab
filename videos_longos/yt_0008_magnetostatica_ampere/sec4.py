"""N11–N13 (V5): fio de raio finito, região externa e limite filamentar a → 0 com I fixo.

2.5D só para estabelecer o cilindro; a derivação acontece numa SEÇÃO TRANSVERSAL 2D (vista de cima: J sai da tela ⊙),
com uma sonda radial P(s) cujo vetor B tem comprimento ∝ B(s), sincronizada com um ponto no gráfico B(s) do cartão auxiliar.
Unidades da cena: μ0 = 1, I = 1 (B(s) = s/(2πa²) dentro, 1/(2πs) fora).

Gráfico (V5): UM ÚNICO objeto Axes (`self.gax`, criado uma vez e fixo no cartão). Curvas, marcas, pontos e rótulos usam sempre
`self.gax.c2p(...)`; nada é recalculado a partir de uma origem antiga. Eixo vertical em unidades de B_ref = 1/(2π a0).
"""
import math

import numpy as np
from manim import (
    VGroup, Line, DashedLine, Dot, Polygon, Circle, FadeIn, FadeOut, Create, Indicate, ValueTracker, LaggedStart, DecimalNumber,
    DashedVMobject, VMobject, TransformFromCopy, Axes, linear, smooth, UP, DOWN, LEFT, RIGHT,
)
from base import *  # noqa: F401,F403
from fisica import TAU, b_cilindro, bphi_cilindro, circulacao

A0 = 0.75          # raio inicial do fio
HW = 2.1           # meia altura desenhada (2.5D)
SMAX = 2.6         # alcance do gráfico em s
KB = 5.6           # comprimento de tela do vetor B por unidade de B (B(a0) ≈ 0,21 ↦ 1,2)
YMAX = 1.15        # teto do gráfico, em unidades de B_ref = 1/(2π a0)
BREF = 1 / (TAU * A0)


class Sec4:
    # ── 2.5D: o cilindro ────────────────────────────────────────────────────────────────────────────────────
    def cyl_shapes(self):
        a = self.a_t.get_value()
        W = self.W
        top = [np.array([a * math.cos(t), HW, a * math.sin(t)]) for t in np.linspace(0, TAU, 48)]
        bot = [np.array([a * math.cos(t), -HW, a * math.sin(t)]) for t in np.linspace(0, TAU, 48)]
        g = VGroup(Polygon(W([-a, -HW, 0]), W([a, -HW, 0]), W([a, HW, 0]), W([-a, HW, 0]), stroke_width=0).set_fill(GREEN, 0.16).set_z_index(1))
        g.add(self.poly(top, GREEN, 0.18, z=2), self.curve(top, STEEL, 2.4, 0.9, z=6), self.curve(bot, STEEL, 2.0, 0.5, z=2))
        g.add(Line(W([-a, -HW, 0]), W([-a, HW, 0]), color=STEEL, stroke_width=2.4), Line(W([a, -HW, 0]), W([a, HW, 0]), color=STEEL, stroke_width=2.4))
        g.add(Line(W([0, HW, 0]), W([a, HW, 0]), color=VIOLET, stroke_width=3).set_z_index(7))
        for h in (-1.3, 0.0, 1.3):                         # canônico: círculos IGUAIS ao longo do eixo
            g.add(self.ring_y(1.55, h, width=3.0, op=0.85, arrows=2, tip=0.26))
        return g

    # ── 2D: seção transversal ───────────────────────────────────────────────────────────────────────────────
    def sec_shapes(self):
        a = self.a_t.get_value()
        W, gs = self.W, self.gs.get_value()
        c0 = W([0, 0, 0])
        g = VGroup(Circle(radius=a * gs, stroke_width=2.6, color=STEEL).set_fill(GREEN, min(0.6, 0.18 * (A0 / a) ** 0.8)).move_to(c0).set_z_index(2))
        rm = max(0.025, min(0.09, 0.16 * a * gs))         # marcadores de J acompanham a região (nunca maiores que ela)
        for rr, n in ((0.0, 1), (0.48, 6), (0.82, 11)):
            for k in range(n):
                t = TAU * k / n + 0.3 * rr
                p = c0 + rr * a * gs * np.array([math.cos(t), math.sin(t), 0])
                g.add(self.out_symbol(p, 1, rm, GREEN))
        if self.cf.get("rings", True):
            for r in (1.45, 2.05):
                g.add(DashedVMobject(Circle(radius=r * gs, color=MAG, stroke_width=2).move_to(c0), num_dashes=int(20 * r)).set_stroke(opacity=0.45))
        return g

    def bval(self, s):
        return bphi_cilindro(max(s, 1e-6), self.a_t.get_value())

    def probe_shapes(self):
        s = self.sp.get_value()
        W = self.W
        p = W([s, 0, 0])
        g = VGroup(Line(W([0, 0, 0]), p, color=VIOLET, stroke_width=3).set_z_index(6), Dot(p, radius=0.07, color=WHITE).set_z_index(9))
        L = KB * self.bval(s)
        if L > 0.05:
            g.add(arrow(p, p + np.array([0, L, 0]), MAG, 7, tip=min(0.3, 0.5 * L)).set_z_index(8))
        return g

    # ── gráfico B(s): UM Axes, fixo no cartão auxiliar ──────────────────────────────────────────────────────
    def graph_make(self):
        c = self.slots["A"]["pos"]
        self.gax = Axes(x_range=[0, SMAX, 1], y_range=[0, YMAX + 0.05, 1], x_length=5.0, y_length=1.5, tips=True,
                        axis_config={"stroke_width": 2.5, "include_ticks": False, "include_numbers": False, "tip_length": 0.14, "tip_width": 0.14,
                                     "color": WHITE})
        self.gax.move_to(c + np.array([0.15, -0.12, 0]))
        self.glab = VGroup(E("s", "s", size=M_S).move_to(self.gax.c2p(SMAX, 0) + [0.33, 0, 0]),
                           E(r"B_\phi", r"B_\phi", size=M_S).move_to(self.gax.c2p(0, YMAX + 0.05) + [0.45, 0.1, 0]))

    def gP(self, s, b):
        """B (unidades da cena) → ponto de tela, SEMPRE pelo mesmo Axes."""
        return self.gax.c2p(s, b / BREF)

    def curve_capped(self, f, s0, s1, color=MAG, width=4.5, op=1.0, n=90, dashed=False):
        """Curva b = f(s); acima do teto é CORTADA (nunca achatada): uma seta para cima marca onde ela continua fora da escala.
        O ponto onde a curva cruza o teto é achado por bisseção: o início/fim do traço não pula de amostra em amostra quando a muda."""
        g, run = VGroup(), []

        def inside(s):
            return 0 <= f(s) / BREF <= YMAX

        def cross(s_in, s_out):
            for _ in range(26):
                mid = (s_in + s_out) / 2
                s_in, s_out = (mid, s_out) if inside(mid) else (s_in, mid)
            return s_in

        def flush(arrow_end=False, arrow_start=False):
            if len(run) > 1:
                m = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=op).set_points_as_corners(run)
                g.add(DashedVMobject(m, num_dashes=18) if dashed else m)
            if arrow_end and run:
                g.add(arrow(run[-1] - [0, 0.18, 0], run[-1] + [0, 0.16, 0], color, 3, tip=0.11).set_opacity(op))
            if arrow_start and run:
                g.add(arrow(run[0] + [0, 0.02, 0], run[0] + [0, 0.34, 0], color, 3, tip=0.11).set_opacity(op))

        start_arrow, prev = False, None
        for s in np.linspace(s0, s1, n):
            ok, above = inside(s), f(s) / BREF > YMAX
            if prev is not None and ok != prev[1]:
                if ok:                      # entra na escala (a curva vinha de cima): começa exatamente no teto
                    sc = cross(s, prev[0])
                    run = [self.gP(sc, f(sc))]
                    start_arrow = prev[2]
                else:                       # sai da escala: termina exatamente no teto, com a seta
                    sc = cross(prev[0], s)
                    run.append(self.gP(sc, f(sc)))
                    flush(arrow_end=above, arrow_start=start_arrow)
                    run, start_arrow = [], False
            if ok:
                run.append(self.gP(s, f(s)))
            prev = (s, ok, above)
        flush(arrow_start=start_arrow)
        return g

    def bgraph(self):
        a = self.a_t.get_value()
        F = self.gf
        g = VGroup()
        if F.get("amark"):
            g.add(DashedLine(self.gax.c2p(a, 0), self.gax.c2p(a, YMAX), color=VIOLET, stroke_width=2, dash_length=0.06).set_opacity(0.8))
        ins = F.get("inside")
        if ins:
            end = min(a, ins() if callable(ins) else a)
            if end > 0.01:
                g.add(self.curve_capped(lambda s: s / (TAU * a * a), 0.0, end, MAG, 4.5, n=max(8, int(60 * end / a))))
        fam = F.get("cfam")
        if fam is not None:                   # família C/s: 2 soluções descartadas + a escolhida pela continuidade em s = a
            sel = fam()
            for m in (0.55, 1.6):
                g.add(self.curve_capped(lambda s, m=m: m / (TAU * s), a, SMAX, WHITE, 3.0, 0.85 * (1 - sel), dashed=True))
            g.add(self.curve_capped(lambda s: 1 / (TAU * s), a, SMAX, MAG if sel > 0.5 else WHITE, 4.5 if sel > 0.5 else 3.0, 0.95))
        if F.get("outside"):
            g.add(self.curve_capped(lambda s: 1 / (TAU * s), a, SMAX, MAG, 4.5))
        if F.get("join") and 1 / (TAU * a) / BREF <= YMAX:
            g.add(Dot(self.gP(a, 1 / (TAU * a)), radius=0.07, color=WHITE).set_z_index(5))
        if F.get("dot"):
            s = self.sp.get_value()
            if self.bval(s) / BREF <= YMAX:
                g.add(Dot(self.gP(s, self.bval(s)), radius=0.08, color=WHITE).set_z_index(6))
        if F.get("clip") and 1 / (TAU * a) / BREF > YMAX:      # pico acima do teto: avisa, em vez de achatar
            g.add(txt("pico fora de escala", 18, DIM).move_to(self.gax.c2p(1.75, YMAX * 0.93)))
        return g

    # ── N11 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def fio_finito(self):
        self.section("fio_finito", "Um fio de verdade tem espessura")
        self.clear()
        self.reset_view(x=-4.0, y=-0.3, scale=0.95, beta=0, tau=-22)
        W = self.W
        self.a_t = ValueTracker(A0)
        self.cf = {"rings": True}
        cyl = self.cached(lambda: (self.a_t.get_value(), *self.view_key()), self.cyl_shapes)
        offs = [(0, 0), (0.55, 0), (-0.55, 0), (0.3, 0.45), (-0.3, -0.45)]
        fl = self.flow([lambda u, o=o: self.W([o[0] * self.a_t.get_value(), -HW + 2 * HW * u, o[1] * self.a_t.get_value()]) for o in offs], count=5, dash=0.28, width=6)
        self.play(FadeIn(cyl), run_time=1.2)
        self.add(fl)
        aL = self.pin(self.lab("a", [0, 0, 0], "a", size=M_M, color=VIOLET), lambda: W([self.a_t.get_value() / 2, HW, 0]) + np.array([0, 0.3, 0]))
        jL = self.pin(self.lab(r"\mathbf J", [0, 0, 0], r"\mathbf J", size=M_M), lambda: W([0, -HW, 0]) + np.array([0.0, -0.35, 0]))
        self.play(FadeIn(aL), FadeIn(jL), run_time=0.6)
        self.caption("Agora a corrente ocupa um cilindro de raio $a$, com densidade de corrente $\\mathbf J$ uniforme (A/m²)")
        self.show(E(r"\mathbf J=J\,\hat{\mathbf z}\quad(s<a)", r"\mathbf J", "J", r"\hat{\mathbf z}", size=M_L, colors={r"\hat{\mathbf z}": GREEN}),
                  src={(r"\mathbf J", 0): jL}, rt=1.6, wait=1.0)
        self.caption("A simetria é a mesma do fio fino: $\\mathbf B$ circula e só depende de $s$")
        self.show(E(r"\mathbf B=B_\phi(s)\,\hat{\boldsymbol\phi}", r"\mathbf B", r"B_\phi(s)", r"\hat{\boldsymbol\phi}", size=M_L), slot="A", rt=1.6, wait=1.5)
        self.mark("n11_cilindro")
        # para a seção transversal 2D: é nela que a derivação acontece
        self.caption("Para raciocinar, corte o fio e olhe a seção de cima: $\\mathbf J$ sai da tela")
        self.out(fl, aL, jL, rt=0.4)
        # o próprio cilindro gira até ser visto de ponta; só então vira a seção 2D (mesmo objeto, outra representação)
        self.play(self.tau.animate.set_value(-90), self.gs.animate.set_value(1.25), self.ox.animate.set_value(-4.4), self.oy.animate.set_value(-0.2), run_time=2.2)
        sec = self.cached(lambda: (self.a_t.get_value(), tuple(sorted(self.cf.items())), *self.view_key()), self.sec_shapes)
        self.play(FadeOut(cyl), FadeIn(sec), run_time=1.0)
        self.purge(cyl)
        aL2 = self.pin(self.lab("a", [0, 0, 0], "a", size=M_M, color=VIOLET), lambda: W([0, 0, -self.a_t.get_value()]) + np.array([0.0, 0.32, 0]))
        arad = self.cached(lambda: (self.a_t.get_value(), *self.view_key()), lambda: Line(W([0, 0, 0]), W([0, 0, -self.a_t.get_value()]), color=VIOLET, stroke_width=3)
                           .set_z_index(7))
        self.play(FadeIn(arad), FadeIn(aL2), run_time=0.6)
        self.drop("H", keep_card=False)
        # sonda local: dentro mede μ0J, fora mede 0. A sonda inicial fica INTEIRA dentro do condutor:
        # centro a (s, z) = (0,25, 0,25) → distância 0,35; raio da sonda 0,14 → alcance 0,49 < a = 0,75
        ZP = 0.25
        self.sp = ValueTracker(0.25)
        pr = 0.14
        loop = self.cached(lambda: (self.sp.get_value(), *self.view_key()), lambda: self.loop3d([self.sp.get_value(), 0, ZP], pr, [0, 1, 0], WHITE, 3.5, fill=0.25,
                                                                                               fill_color=BLUE_L, arrows=2, tip=0.16, heads=True))
        Jv = lambda: 1 / (math.pi * self.a_t.get_value() ** 2)
        val = lambda: circulacao(lambda p: b_cilindro(p, self.a_t.get_value()), [self.sp.get_value(), 0, ZP], pr, [0, 1, 0], 240) / (math.pi * pr * pr) / Jv()
        self.drop("A", keep_card=False)
        self.play(FadeIn(loop), run_time=0.6)
        ro = self.readout(E(r"\frac{1}{A}\oint\mathbf B\cdot d\boldsymbol\ell=", r"\mathbf B\cdot d\boldsymbol\ell", size=M_M), val, unit=r"\,\mu_0 J")
        self.caption("A sonda dentro do fio mede $\\mu_0 J$: onde há corrente, o rotacional de $\\mathbf B$ não é zero")
        self.hold(2.0)
        self.play(self.sp.animate.set_value(0.5), run_time=1.5, rate_func=linear)
        self.caption("Quando a sonda cruza a borda, só parte dela fica no condutor: a leitura cai de $\\mu_0 J$ até zero")
        self.play(self.sp.animate.set_value(1.55), run_time=3.5, rate_func=linear)
        self.caption("Fora do fio a mesma sonda mede zero")
        self.mark("n11_sonda_dentro_fora")
        self.hold(1.5)
        ro[1].clear_updaters()
        self.out(loop, rt=0.4)
        self.drop("A", keep_card=False)
        # sonda radial + gráfico sincronizado (um Axes só)
        self.sp.set_value(0.3)
        probe = self.cached(lambda: (self.sp.get_value(), self.a_t.get_value(), *self.view_key()), self.probe_shapes)
        sL = self.pin(self.lab("s", [0, 0, 0], "s", size=M_M), lambda: W([self.sp.get_value() / 2, 0, 0]) + np.array([0, -0.3, 0]))
        self.play(FadeIn(probe), FadeIn(sL), run_time=0.6)
        self.gf = {}
        self.graph_make()
        gr = self.cached(lambda: (self.a_t.get_value(), self.sp.get_value(), tuple(sorted((k, v() if callable(v) else v) for k, v in self.gf.items()))), self.bgraph)
        card = self._card("A")
        grp = VGroup(self.gax, self.glab, gr)
        self.play(*([FadeIn(card)] if card is not None else []), FadeIn(grp), run_time=0.8)
        self.slots["A"]["eq"] = grp
        # a marca s=a nasce da geometria
        amark = E("a", "a", size=M_S).move_to(self.gP(A0, 0) + [0, -0.27, 0])
        self.play(TransformFromCopy(aL2, amark), run_time=1.0)
        self.gf["amark"] = True
        self.hold(0.2)
        self.amark = amark
        # álgebra: dentro
        self.caption("Dentro: a componente axial de $\\nabla\\times\\mathbf B=\\mu_0\\mathbf J$ em cilíndricas")
        self.show(E(r"\frac{1}{s}\frac{d}{ds}\left(s\,B_\phi\right)=\mu_0 J", r"\frac{1}{s}", r"\frac{d}{ds}", r"s\,B_\phi", r"\mu_0 J", size=M_L), rt=1.6, wait=1.5)
        self.caption("Multiplicar por $s$ isola a derivada de $s\\,B_\\phi$")
        self.show(E(r"\frac{d}{ds}\left(s\,B_\phi\right)=\mu_0 J\,s", r"\frac{d}{ds}", r"s\,B_\phi", r"\mu_0 J", r"\,s", size=M_L), (r"\frac{1}{s}", r"\,s"),
                  rt=1.8, wait=1.2)
        self.caption("Integrar em $s$ deixa uma constante $C$ que ainda não sabemos qual é")
        self.show(E(r"s\,B_\phi=\frac{\mu_0 J}{2}\,s^2+C", r"s\,B_\phi", r"\mu_0 J", "s^2", "+C", size=M_L), (r"\frac{d}{ds}", None), (r"\,s", "s^2"), rt=1.8, wait=1.2)
        self.show(E(r"B_\phi=\frac{\mu_0 J}{2}\,s+\frac{C}{s}", r"B_\phi", r"\mu_0 J", r"\,s", r"+\frac{C}{s}", size=M_L), (r"s\,B_\phi", r"B_\phi"),
                  ("s^2", r"\,s"), ("+C", r"+\frac{C}{s}"), rt=1.8, wait=0.8)
        # C/s explode no eixo (sem desenhar curva parcial); regularidade mata C; só então a reta nasce da origem
        self.hl(r"+\frac{C}{s}", color=WHITE)
        inf = E(r"C/s\to\infty", size=M_S).move_to(self.gax.c2p(0, YMAX * 0.55) + [1.1, 0, 0])
        self.caption("Com $C\\neq0$, o termo $C/s$ explode em $s=0$: o campo no eixo seria infinito")
        self.play(FadeIn(inf), Indicate(self.gax.y_axis, color=MAG, scale_factor=1.0), run_time=1.4)
        self.hold(1.0)
        self.caption("Regularidade no eixo: o campo em $s=0$ é finito, o que elimina o termo $C/s$")
        self.play(FadeOut(inf), run_time=0.4)
        self.show(E(r"B_\phi=\frac{\mu_0 J}{2}\,s", r"B_\phi", r"\mu_0 J", r"\,s", size=M_XL), (r"+\frac{C}{s}", None), rt=1.6, wait=0.3)
        bx = box(self.slots["H"]["eq"], MAG)
        self.play(FadeIn(bx), run_time=0.4)
        self.sin_end = ValueTracker(0.0)
        self.gf["inside"] = lambda: round(self.sin_end.get_value(), 3)
        self.caption("A reta nasce na origem e cresce até a fronteira: dentro do fio, $B$ cresce linearmente com $s$")
        self.play(self.sin_end.animate.set_value(A0), run_time=2.0, rate_func=linear)
        self.gf["inside"] = True
        self.gf["dot"] = True
        self.caption("A sonda e o gráfico andam juntos")
        self.play(self.sp.animate.set_value(A0), run_time=2.5, rate_func=linear)
        self.mark("n11_dentro_linear")
        self.hold(1.5)
        self.out(bx, inf, rt=0.3)
        self.sec, self.probe_, self.sL, self.aL2, self.arad = sec, probe, sL, aL2, arad

    # ── N12 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def fio_externo(self):
        self.section("fio_externo", "Fora do fio")
        self.caption("Fora, $J=0$: o rotacional de $\\mathbf B$ se anula")
        self.show(E(r"\frac{1}{s}\frac{d}{ds}\left(s\,B_\phi\right)=0", r"\frac{1}{s}", r"\frac{d}{ds}", r"s\,B_\phi", "0", size=M_L), rt=1.6, wait=1.2)
        self.caption("Derivada nula: $s\\,B_\\phi$ é uma constante fora do fio")
        self.show(E(r"s\,B_\phi=C_{\rm ext}", r"s\,B_\phi", r"C_{\rm ext}", size=M_L), (r"\frac{1}{s}", None), (r"\frac{d}{ds}", None), ("0", None), rt=1.6, wait=1.0)
        self.show(E(r"B_\phi=\frac{C_{\rm ext}}{s}", r"B_\phi", r"C_{\rm ext}", size=M_XL), (r"s\,B_\phi", r"B_\phi"), rt=1.6, wait=0.5)
        # várias soluções C/s: surgem já nas posições finais; a continuidade em s = a seleciona uma
        self.csel = ValueTracker(0.0)
        self.gf["cfam"] = lambda: round(self.csel.get_value(), 3)
        self.gf["join"] = True
        self.caption("$C$ ainda é livre: cada valor dá uma solução $C/s$")
        self.hold(2.5)
        self.caption("A continuidade em $s=a$ seleciona uma")
        self.hold(1.5)
        self.play(self.csel.animate.set_value(1.0), run_time=2.0)
        self.caption("Sem corrente superficial em $s=a$, $B_\\phi$ é contínuo: a curva de fora passa pelo ponto de dentro")
        self.mark("n12_continuidade_seleciona")
        self.hold(1.5)
        self.show(E(r"\frac{C_{\rm ext}}{a}=\frac{\mu_0 J}{2}\,a", r"C_{\rm ext}", r"\mu_0 J", r"\,a", size=M_L), (r"C_{\rm ext}", r"C_{\rm ext}"), rt=1.8, wait=1.2)
        self.show(E(r"C_{\rm ext}=\frac{\mu_0 J}{2}\,a^2", r"C_{\rm ext}", r"\mu_0 J", "a^2", size=M_L), (r"\,a", "a^2"), rt=1.6, wait=1.0)
        self.caption("Em termos da corrente total $I=J\\pi a^2$, a constante deixa de depender do raio")
        self.show(E(r"C_{\rm ext}=\frac{\mu_0 I}{2\pi}", r"C_{\rm ext}", r"\mu_0 I", size=M_L), (r"\mu_0 J", r"\mu_0 I"), ("a^2", None), rt=1.8, wait=1.0)
        self.gf.pop("cfam")
        self.gf["outside"] = True
        self.show(E(r"B_\phi=\frac{\mu_0 I}{2\pi s}\quad(s>a)", r"B_\phi", r"\mu_0 I", r"(s>a)", size=M_L), (r"C_{\rm ext}", None), rt=1.8, wait=0.3)
        bx = box(self.slots["H"]["eq"], MAG)
        l1 = E(r"B\propto s", size=M_S).move_to(self.gax.c2p(A0 * 0.45, YMAX * 0.78))
        l2 = E(r"B\propto 1/s", size=M_S).move_to(self.gax.c2p(1.8, YMAX * 0.62))
        self.play(FadeIn(bx), FadeIn(l1), FadeIn(l2), run_time=0.6)
        self.caption("A sonda atravessa a fronteira: o campo cresce até $s=a$ e depois cai como $1/s$")
        self.play(self.sp.animate.set_value(2.3), run_time=3.0, rate_func=linear)
        self.mark("n12_dentro_fora")
        self.hold(2.0)
        self.out(bx, l1, l2, rt=0.4)

    # ── N13 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def limite_filamentar(self):
        self.section("limite", "Comprimindo o fio: a → 0 com I fixo")
        self.drop("H", keep_card=False)
        self.gf.pop("join", None)
        self.out(self.aL2, self.arad, self.amark, rt=0.3)
        self.gf.pop("amark", None)
        self.play(self.sp.animate.set_value(1.45), run_time=1.0)
        # pilar J(x,y): altura J, base πa², volume I — com aviso quando a altura é cortada
        C = self.slots["H"]["pos"] + np.array([-0.7, -0.55, 0])
        Vol = math.pi * (1.1 * A0) ** 2 * 0.55
        HC = 1.05

        def pil():
            a = self.a_t.get_value()
            rp = 1.1 * a
            h = Vol / (math.pi * rp * rp)
            hd = min(h, HC)
            ell = lambda r, y: [C + np.array([r * math.cos(t), y + 0.36 * r * math.sin(t), 0]) for t in np.linspace(0, TAU, 40)]
            g = VGroup(Polygon(*ell(1.3, 0), stroke_width=1.5, stroke_color=WHITE, stroke_opacity=0.4).set_fill(WHITE, 0.05))
            g.add(Polygon(C + [-rp, 0, 0], C + [rp, 0, 0], C + [rp, hd, 0], C + [-rp, hd, 0], stroke_width=0).set_fill(GREEN, 0.45),
                  Polygon(*ell(rp, 0), stroke_width=0).set_fill(GREEN, 0.45), Polygon(*ell(rp, hd), stroke_color=GREEN, stroke_width=2).set_fill(GREEN, 0.75))
            if h > HC:
                g.add(arrow(C + [0, hd + 0.05, 0], C + [0, hd + 0.38, 0], GREEN, 3, tip=0.13),
                      txt("fora de escala", 18, DIM).move_to(C + [-0.95, hd + 0.15, 0]))
            return g
        pillar = self.cached(lambda: self.a_t.get_value(), pil)
        nums = VGroup(VGroup(E("a=", "a", size=M_S), DecimalNumber(A0, num_decimal_places=2, font_size=34)).arrange(RIGHT, buff=0.12),
                      VGroup(E("J/J_0=", "J", size=M_S), DecimalNumber(1, num_decimal_places=1, font_size=34)).arrange(RIGHT, buff=0.12),
                      VGroup(E(r"I=J\pi a^2=", "I", "J", size=M_S), DecimalNumber(1, num_decimal_places=2, font_size=34), E("I_0", size=M_S)).arrange(RIGHT, buff=0.1)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(self.slots["H"]["pos"] + np.array([2.0, 0, 0]))
        nums[0][1].add_updater(lambda m: m.set_value(self.a_t.get_value()))
        nums[1][1].add_updater(lambda m: m.set_value((A0 / self.a_t.get_value()) ** 2))
        nums[2][1].add_updater(lambda m: m.set_value(1.0))
        grp = VGroup(pillar, nums)
        c0 = grp.get_center()
        self.card_group(grp, "H")
        C += grp.get_center() - c0          # o pilar reconstruído usa o referencial já deslocado pelo layout
        self.gf["clip"] = True
        self.caption("Pilar: altura $J$, base $\\pi a^2$, volume $I$ ($J_0$, $I_0$: valores iniciais). Mantenha $I$ fixo e diminua $a$")
        self.hold(1.5)
        self.play(self.a_t.animate.set_value(0.3), run_time=4.5, rate_func=smooth)
        self.caption("Fora do fio nada muda; o pico de $B$ sobe e se aproxima do eixo")
        self.play(self.a_t.animate.set_value(0.12), run_time=3.5, rate_func=smooth)
        self.play(self.a_t.animate.set_value(0.05), run_time=2.0, rate_func=smooth)
        self.caption("A região onde o rotacional não é zero fica cada vez mais estreita e mais intensa")
        self.mark("n13_compressao")
        self.hold(2.0)
        for n in nums:
            n[1].clear_updaters()
        self.gf.pop("clip", None)
        self.drop("H", keep_card=False)
        self.show(E(r"\mathbf J\ \longrightarrow\ I\,\delta(x)\,\delta(y)\,\hat{\mathbf z}", r"\mathbf J", "I", r"\delta(x)\,\delta(y)", r"\hat{\mathbf z}", size=M_L,
                    colors={r"\delta(x)\,\delta(y)": VIOLET, r"\hat{\mathbf z}": GREEN}), rt=1.6, wait=1.2)
        self.caption("No limite, a corrente vive só sobre o eixo: um delta bidimensional com integral $I$")
        self.show(E(r"\nabla\times\mathbf B=\mu_0 I\,\delta(x)\,\delta(y)\,\hat{\mathbf z}", r"\nabla\times\mathbf B", "I", r"\delta(x)\,\delta(y)", r"\hat{\mathbf z}",
                    size=M_L, colors={r"\delta(x)\,\delta(y)": VIOLET, r"\hat{\mathbf z}": GREEN}), (r"\mathbf J", None), rt=1.8, wait=0.3)
        bx = box(self.slots["H"]["eq"], MAG)
        self.play(FadeIn(bx), run_time=0.4)
        self.mark("n13_rot_delta")
        self.hold(2.0)
        # o paradoxo do N02, revisitado na mesma vista de cima
        self.out(bx, self.probe_, self.sL, rt=0.3)
        self.drop("A", keep_card=False)
        W = self.W
        P = np.array([1.5, 0, -0.9])
        small = self.loop3d(P, 0.32, [0, 1, 0], WHITE, 3.5, fill=0.22, fill_color=BLUE_L, arrows=3, tip=0.18, heads=True)
        big = self.loop3d([0, 0, 0], 1.7, [0, 1, 0], WHITE, 3.5, fill=0.10, fill_color=BLUE_L, arrows=4, tip=0.22, heads=True)
        l0 = self.callout(rich("aqui: $\\nabla\\times\\mathbf B=\\mathbf 0$", T_NOTE), W(P) + np.array([0.3, 0.3, 0]), W(P) + np.array([1.9, 1.1, 0]))
        l1 = self.callout(rich("envolve o eixo: $\\oint\\mathbf B\\cdot d\\boldsymbol\\ell=\\mu_0 I$", T_NOTE), W([1.2, 0, 1.2]), W([1.2, 0, 1.2]) + np.array([2.7, 0.35, 0]))
        self.play(Create(small), FadeIn(l0), run_time=1.0)
        self.play(Create(big), FadeIn(l1), run_time=1.2)
        self.caption("Fora do eixo o rotacional é zero; ele inteiro está concentrado no eixo. O paradoxo se desfaz")
        self.mark("n13_paradoxo_resolvido")
        self.hold(4.0)
        self.out(small, big, l0, l1, rt=0.6)
