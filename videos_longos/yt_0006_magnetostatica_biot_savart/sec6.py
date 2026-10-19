"""Seções 12–13: espira no eixo (construção completa) e checagens (centro e longe)."""
import math

import numpy as np
from manim import (
    VGroup, Line, DashedLine, Dot, Polygon, ParametricFunction, Ellipse, Arc, FadeIn, FadeOut, Create, Indicate, ValueTracker,
    always_redraw, linear, smooth, DecimalNumber, VMobject, ReplacementTransform, TransformFromCopy, Transform, Write,
    UP, DOWN, LEFT, RIGHT,
)
from base import *  # noqa: F401,F403
from fisica import espira


class Sec6:
    RL = 1.65

    # ── geometria viva da espira (rótulos são objetos persistentes, não parte do grupo recalculado) ──────────
    def loop_shapes(self):
        R, z, ph, W, F = self.RL, self.z_obs.get_value(), self.phi_src.get_value(), self.W, self.lf
        g = VGroup(ParametricFunction(lambda u: W([R * math.cos(u), R * math.sin(u), 0]), t_range=[0, 2 * math.pi], color=BLUE_L,
                                      stroke_width=7, fill_opacity=0))
        f, p, dl, sep, b, tr, ax = espira(ph, z, R)
        O = np.zeros(3)
        g.add(Dot(W(f), color=GREEN, radius=0.085).set_z_index(9))
        if abs(self.beta.get_value() - 90) < 0.01 and abs(math.cos(ph)) < 0.001:
            s = 1 if math.sin(ph) > 0 else -1
            g.add(self.out_symbol(W(f), s, 0.17, GREEN))
        else:
            g.add(self.vec(f, dl, GREEN, scale=0.38, width=6))
        if F["axis"]:
            g.add(DashedLine(W([0, 0, -0.3]), W([0, 0, 3.1]), color=VIOLET, stroke_width=2.4), Dot(W(p), radius=0.1).set_z_index(9))
        if F["tri"]:
            g.add(Line(W(O), W(f), color=WHITE, stroke_width=3), Line(W(O), W(p), color=VIOLET, stroke_width=3),
                  self.vec(f, sep, VIOLET, width=4))
            if z > 0.01 and abs(math.cos(ph)) < 0.001:
                rh, zh = f / R, np.array([0, 0, 1.0])
                g.add(VMobject(color=WHITE, stroke_width=2).set_points_as_corners(
                    [W(0.2 * rh), W(0.2 * rh + 0.2 * zh), W(0.2 * zh)]))
        if F["field"]:
            sc = 4.5
            if not F["only_comp"]:
                g.add(self.vec(p, b, MAG, scale=sc, width=6))
            if F["comp"] and z > 1e-5:
                g.add(self.vec(p, ax, MAG, scale=sc, width=4), self.vec(p + sc * ax, tr, CYAN, scale=sc, width=4))
        if F["pair"]:
            f2, p2, dl2, sep2, b2, tr2, ax2 = espira(ph + math.pi, z, R)
            g.add(self.out_symbol(W(f2), -1, 0.17, GREEN), Line(W(f2), W(p), color=VIOLET, stroke_width=2).set_opacity(0.5))
            if not F["only_comp"]:
                g.add(self.vec(p, b2, MAG, scale=4.5, width=5))
            if F["comp"]:
                g.add(self.vec(p + 4.5 * ax2, tr2, CYAN, scale=4.5, width=4))
        if F.get("many"):
            for ang_ in np.linspace(0, 2 * math.pi, 8, endpoint=False):
                fb, pb, dlb, rb, bb, tb, ab = espira(ang_, z, R)
                g.add(Dot(W(fb), color=GREEN, radius=0.06).set_z_index(8), self.vec(pb, bb, MAG, scale=3.5, width=3))
        return g

    def loop_key(self):
        return (self.phi_src.get_value(), self.z_obs.get_value(), tuple(sorted(self.lf.items())), *self.view_key())

    def plab(self, tex, iso, fn, size=M_M, colors=None):
        """Rótulo persistente: o termo que depois voa para a equação. fn() devolve a posição na tela."""
        m = self.lab(tex, [0, 0, 0], *([iso] if iso else []), size=size, colors=colors)
        m.add_updater(lambda mm: mm.move_to(fn()))
        m.update(0)
        return m

    def espira_eixo(self):
        self.section("espira", "Uma espira, duas vistas da mesma geometria")
        self.clear()
        self.reset_view(x=-4.0, y=-0.2, scale=1.05, beta=0, tau=0)
        R = self.RL
        W = self.W
        self.phi_src, self.z_obs = ValueTracker(math.pi / 2), ValueTracker(1.9)
        self.lf = {"axis": False, "tri": False, "field": False, "comp": False, "pair": False, "only_comp": False, "many": False}
        grp = self.cached(self.loop_key, self.loop_shapes)
        flow = self.flow([lambda u: W([R * math.cos(2 * math.pi * u), R * math.sin(2 * math.pi * u), 0])], count=10)
        self.add(grp, flow)
        self.play(FadeIn(grp), run_time=1.0)
        # ── vista frontal: I, R, dφ, dℓ ───────────────────────────────────────────────────────────────────
        frontal = txt("vista frontal · olhando de +z", T_NOTE, DIM).move_to([-4.0, 2.75, 0])
        il = self.plab("I", "I", lambda: W([R + 0.45, 0.45, 0]))
        ia = arrow(W([R, -0.05, 0]), W([R, 0.7, 0]), GREEN, 6)
        self.play(FadeIn(frontal), FadeIn(il), FadeIn(ia), run_time=0.9)
        self.caption("A corrente $I$ percorre a espira de raio $R$")
        self.hold(2.5)
        ph0 = math.pi / 2
        arc = Arc(radius=R * self.gs.get_value(), start_angle=ph0 - 0.4, angle=0.4, arc_center=W([0, 0, 0]), color=GREEN, stroke_width=12)
        rad = Line(W([0, 0, 0]), W([0, R, 0]), color=WHITE, stroke_width=2.5)
        ang = Arc(radius=0.55, start_angle=ph0 - 0.4, angle=0.4, arc_center=W([0, 0, 0]), color=WHITE, stroke_width=3)
        rl = self.plab("R", "R", lambda: W([-0.3, R / 2, 0]))
        dpl = self.plab(r"d\phi", r"d\phi", lambda: W([0.28, 0.8, 0]), size=M_S)
        dll = self.plab(r"d\ell", r"d\ell", lambda: W([0.62, R + 0.32, 0]))
        self.play(Create(rad), Create(arc), Create(ang), FadeIn(rl), FadeIn(dpl), FadeIn(dll), run_time=1.6)
        self.show(E(r"d\ell=R\,d\phi", r"d\ell", "R", r"d\phi", size=M_XL), src={(r"d\ell", 0): dll, ("R", 0): rl, (r"d\phi", 0): dpl},
                  rt=2.2, wait=2.0)
        self.caption("Um arco infinitesimal é o raio vezes o ângulo, em radianos")
        self.mark("espira_arco_frontal")
        self.hold(2.5)
        arc_eq = self.slots["H"]["eq"]
        # ── gira para a vista lateral ─────────────────────────────────────────────────────────────────────
        self.play(FadeOut(VGroup(frontal, ia, il, arc, ang, rad, dpl)), run_time=0.8)
        self.lf["axis"] = True
        side = txt("vista lateral · espira de perfil", T_NOTE, DIM).move_to([-4.4, 2.75, 0])
        self.caption("Giramos a mesma espira de $0^\\circ$ a $90^\\circ$: vemos o eixo $z$ e o ponto $P$")
        rl.clear_updaters()
        rl.add_updater(lambda m: m.move_to(W([0.0, R * 0.5, 0]) + np.array([-0.3, 0.0, 0])))
        self.play(self.beta.animate.set_value(90), self.ox.animate.set_value(-5.6), self.oy.animate.set_value(-0.2), self.gs.animate.set_value(1.3),
                  FadeOut(dll), run_time=4.0)
        self.play(FadeIn(side), run_time=0.6)
        self.caption("O ponto $P$ está no eixo; o elemento $d\\ell$ aponta para fora da tela")
        self.hold(3.5)
        # ── triângulo ─────────────────────────────────────────────────────────────────────────────────────
        O = np.zeros(3)
        self.play(FadeOut(side), run_time=0.4)
        self.relayout("geo", 1.0)
        self.view_to(-5.4, -0.2, 1.6, 1.2)
        self.lf["tri"] = True
        self.hold(0.1)
        fpos = lambda: espira(self.phi_src.get_value(), self.z_obs.get_value(), R)[0]
        ppos = lambda: espira(self.phi_src.get_value(), self.z_obs.get_value(), R)[1]
        rl2 = self.plab("R", "R", lambda: W(0.5 * fpos()) + np.array([-0.3, 0.0, 0]))
        sl = self.plab("s", "s", lambda: W(fpos() + 0.5 * (ppos() - fpos())) + np.array([0.3, 0.15, 0]))
        zl = self.plab("z", "z", lambda: W(0.5 * ppos()) + np.array([0.0, -0.38, 0]))
        self.play(FadeOut(rl), FadeIn(rl2), FadeIn(sl), FadeIn(zl), run_time=1.0)
        self.caption("Triângulo retângulo: $R$ é o raio, $z$ é a altura de $P$ e $s$ liga a fonte a $P$")
        self.hold(3)
        self.show(E(r"s^2=R^2+z^2", "s^2", "R^2", "z^2", size=M_XL), slot="A", src={("s^2", 0): sl, ("R^2", 0): rl2, ("z^2", 0): zl},
                  rt=2.2, wait=2.5)
        self.caption("Pitágoras: a separação $s$ vale $\\sqrt{R^2+z^2}$")
        self.mark("espira_triangulo")
        self.hold(1.5)
        self.relayout("split", 1.0)
        self.view_to(-5.6, -0.2, 1.3, 1.0)
        # ── ângulo reto e lei no módulo ───────────────────────────────────────────────────────────────────
        thl = self.plab(r"\theta=90^\circ", None, lambda: W(fpos()) + np.array([0.8, -0.55, 0]), size=M_S)
        self.play(FadeIn(thl), run_time=0.7)
        self.caption("$d\\ell$ sai da tela e $\\mathbf s$ está no plano: o ângulo entre eles é $90^\\circ$")
        self.mark("espira_ortogonalidade")
        self.hold(2.5)
        aux = self.slots["A"]["eq"]
        lei_eq = E(r"dB=\frac{\mu_0}{4\pi}\frac{I\,d\ell\,\sin\theta}{s^2}", "dB", "I", r"d\ell", r"\sin\theta", "s^2", r"\frac{\mu_0}{4\pi}", size=M_L)
        self.caption("Biot–Savart no módulo: a distância é $s$")
        self.show(lei_eq, src={("s^2", 0): glyphs(aux, "s^2", 0), (r"\sin\theta", 0): thl}, rt=2.0, wait=1.5)
        self.show(E(r"dB=\frac{\mu_0}{4\pi}\frac{I\,d\ell\,\sin90^\circ}{s^2}", "dB", "I", r"d\ell", r"\sin90^\circ", "s^2", r"\frac{\mu_0}{4\pi}", size=M_L),
                  (r"\sin\theta", r"\sin90^\circ"), rt=1.6, wait=1.2)
        self.caption("$\\sin90^\\circ=1$")
        self.show(E(r"dB=\frac{\mu_0}{4\pi}\frac{I\,d\ell}{s^2}", "dB", "I", r"d\ell", "s^2", r"\frac{\mu_0}{4\pi}", size=M_L),
                  (r"\sin90^\circ", None), rt=1.6, wait=1.5)
        self.play(FadeOut(thl), run_time=0.4)
        self.drop("A")
        self.mark("espira_modulo")
        # ── dB e decomposição ─────────────────────────────────────────────────────────────────────────────
        self.lf["field"] = True
        self.hold(0.1)
        dbl = self.plab(r"d\mathbf B", r"d\mathbf B", lambda: W(ppos() + 4.5 * espira(self.phi_src.get_value(), self.z_obs.get_value(), R)[4]) + np.array([0.15, 0.4, 0]))
        self.play(FadeIn(dbl), run_time=0.8)
        self.caption("A mão direita dá $d\\mathbf B$: perpendicular a $\\mathbf s$ e a $d\\ell$")
        self.hold(3.5)
        self.lf["comp"] = True
        dbz = self.plab(r"dB_z", r"dB_z", lambda: W(ppos() + 2.25 * espira(self.phi_src.get_value(), self.z_obs.get_value(), R)[6]) + np.array([0.0, -0.5, 0]), size=M_S)
        self.play(FadeIn(dbz), run_time=0.8)
        self.caption("Decompomos $d\\mathbf B$ em uma parte axial ($dB_z$) e uma transversal")
        self.show(E(r"dB_z=dB\cos\gamma", "dB", r"dB_z", r"\cos\gamma", size=M_XL), (r"dB", "dB"), src={(r"dB_z", 0): dbz}, rt=2.0, wait=1.5)
        gam = math.atan2(self.z_obs.get_value(), R)
        f0, p0 = espira(math.pi / 2, self.z_obs.get_value(), R)[0], espira(math.pi / 2, self.z_obs.get_value(), R)[1]
        a1 = Arc(radius=0.5, start_angle=-math.pi / 2, angle=gam, arc_center=W(f0), color=WHITE, stroke_width=3)
        a2 = Arc(radius=0.45, start_angle=0, angle=gam, arc_center=W(p0), color=WHITE, stroke_width=3)
        g1 = self.lab(r"\gamma", W(f0) + np.array([0.38, -0.68, 0]), r"\gamma", size=M_S, colors={r"\gamma": CYAN})
        g2 = self.lab(r"\gamma", W(p0) + np.array([0.68, 0.3, 0]), r"\gamma", size=M_S, colors={r"\gamma": CYAN})
        self.play(Create(a1), Create(a2), FadeIn(g1), FadeIn(g2), run_time=1.4)
        self.caption("Os dois ângulos $\\gamma$ são iguais: lados perpendiculares dois a dois")
        self.hold(4)
        self.show(E(r"\cos\gamma=\frac{R}{s}", r"\cos\gamma", "R", "s", size=M_L), slot="A",
                  src={(r"\cos\gamma", 0): g2, ("R", 0): rl2, ("s", 0): sl}, rt=2.0, wait=2.0)
        aux = self.slots["A"]["eq"]
        self.show(E(r"dB_z=dB\,\frac{R}{s}", "dB", r"dB_z", "R", "s", size=M_XL), (r"\cos\gamma", None),
                  src={("R", 0): glyphs(aux, "R", 0), ("s", 0): glyphs(aux, "s", 0)}, rt=2.2, wait=2.0)
        self.drop("A")
        self.play(FadeOut(VGroup(a1, a2, g1, g2)), run_time=0.6)
        self.mark("espira_projecao_axial")
        self.caption("Mova $P$: $dB_z$ acompanha $s$")
        self.play(self.z_obs.animate.set_value(0.7), run_time=3, rate_func=smooth)
        self.play(self.z_obs.animate.set_value(2.6), run_time=3, rate_func=smooth)
        self.play(self.z_obs.animate.set_value(1.9), run_time=2, rate_func=smooth)
        # ── elemento oposto: transversais se cancelam, axiais se somam ───────────────────────────────────
        self.lf["pair"] = True
        self.caption("Agora o elemento diametralmente oposto, com a mesma distância $s$ até $P$")
        self.hold(3)
        self.lf["only_comp"] = True
        self.play(FadeOut(dbl), run_time=0.4)
        self.hold(0.1)
        f1, p1, dl1, sep1, b1, tr1, ax1 = espira(math.pi / 2, self.z_obs.get_value(), R)
        sc = 4.5
        orig_t1 = self.vec(p1 + sc * ax1, tr1, CYAN, scale=sc, width=4)
        orig_t2 = self.vec(p1 + sc * ax1, -tr1, CYAN, scale=sc, width=4)
        base = np.array([2.0, -1.0, 0.0])
        delta = W(p1 + sc * tr1) - W(p1)
        t1, t2 = arrow(base, base + delta, CYAN, 5), arrow(base + delta, base, CYAN, 5)
        self.caption("Transversais, ponta a ponta: o caminho volta ao ponto de partida")
        self.show(E(r"d\mathbf B_\perp(\phi)+d\mathbf B_\perp(\phi+\pi)=\mathbf 0", r"d\mathbf B_\perp(\phi)", r"d\mathbf B_\perp(\phi+\pi)", size=M_S,
                    colors={r"d\mathbf B_\perp(\phi)": CYAN, r"d\mathbf B_\perp(\phi+\pi)": CYAN}), rt=1.6, wait=0.5)
        self.play(TransformFromCopy(orig_t1, t1), run_time=1.3)
        self.play(TransformFromCopy(orig_t2, t2), run_time=1.3)
        zero = self.lab(r"\mathbf 0", base + np.array([0.6, 0.0, 0]), r"\mathbf 0", size=M_M, colors={r"\mathbf 0": CYAN})
        self.play(FadeIn(zero), run_time=0.6)
        self.mark("espira_transversais_fecham")
        self.hold(3)
        self.play(FadeOut(VGroup(t1, t2, zero)), run_time=0.7)
        adelta = W(p1 + sc * ax1) - W(p1)
        abase = np.array([1.5, -1.9, 0.0])
        oa = self.vec(p1, ax1, MAG, scale=sc, width=4)
        a_1, a_2 = arrow(abase, abase + adelta, MAG, 5), arrow(abase + adelta, abase + 2 * adelta, MAG, 5)
        self.caption("Axiais, ponta a ponta: as duas parcelas têm o mesmo sentido e se somam")
        self.show(E(r"dB_z+dB_z=2\,dB_z", r"dB_z", size=M_L), rt=1.6, wait=0.3)
        self.play(TransformFromCopy(oa, a_1), run_time=1.1)
        self.play(TransformFromCopy(oa, a_2), run_time=1.1)
        res = arrow(abase + np.array([0.5, 0, 0]), abase + np.array([0.5, 0, 0]) + 2 * adelta, MAG, 8)
        self.play(Create(res), run_time=0.9)
        self.mark("espira_cancelamento_e_soma")
        self.caption("O par prova o cancelamento. Volte a UMA contribuição $dB_z$")
        self.hold(3.5)
        self.play(FadeOut(VGroup(a_1, a_2, res, side)), run_time=0.7)
        self.lf["pair"] = False
        self.lf["only_comp"] = False
        # ── álgebra do integrando ─────────────────────────────────────────────────────────────────────────
        self.section("algebra_espira", "Do triângulo ao integrando axial")
        self.relayout("alg", 1.0)
        self.view_to(-6.0, -0.3, 1.15, 1.2)
        mod = E(r"dB=\frac{\mu_0}{4\pi}\frac{I\,d\ell}{s^2}", "dB", "I", r"d\ell", "s^2", r"\frac{\mu_0}{4\pi}", size=M_M)
        self.show(mod, slot="A", rt=1.4, wait=1.0)
        self.caption("Troque $dB$ pelo módulo da lei")
        self.show(E(r"dB_z=\frac{\mu_0}{4\pi}\frac{I\,d\ell}{s^2}\,\frac{R}{s}", r"dB_z", "I", r"d\ell", "s^2", "R", "s", r"\frac{\mu_0}{4\pi}", size=M_L),
                  (r"dB_z", r"dB_z", 0, 0),
                  src={("I", 0): glyphs(mod, "I", 0), (r"d\ell", 0): glyphs(mod, r"d\ell", 0), ("s^2", 0): glyphs(mod, "s^2", 0),
                       (r"\frac{\mu_0}{4\pi}", 0): glyphs(mod, r"\frac{\mu_0}{4\pi}", 0)}, rt=2.6, wait=1.8)
        self.drop("A")
        self.show(E(r"d\ell=R\,d\phi", r"d\ell", "R", r"d\phi", size=M_M), slot="A", rt=1.2, wait=0.5)
        arcmem = self.slots["A"]["eq"]
        self.hl(r"d\ell")
        self.caption("Troque $d\\ell$ pelo arco $R\\,d\\phi$")
        self.show(E(r"dB_z=\frac{\mu_0}{4\pi}\frac{I\,R\,d\phi\,R}{s^2\,s}", r"dB_z", "I", "R", "s^2", "s", r"d\phi", r"\frac{\mu_0}{4\pi}", size=M_L),
                  (r"d\ell", None), ("R", "R", 0, 1),
                  src={("R", 0): glyphs(arcmem, "R", 0), (r"d\phi", 0): glyphs(arcmem, r"d\phi", 0)}, rt=2.6, wait=2.0)
        self.drop("A")
        self.caption("Agrupe os dois fatores de $R$")
        self.show(E(r"dB_z=\frac{\mu_0}{4\pi}\frac{I\,R\cdot R\,d\phi}{s^2\cdot s}", r"dB_z", "I", "R", "s^2", "s", r"d\phi", r"\frac{\mu_0}{4\pi}", size=M_L),
                  rt=1.8, wait=1.5)
        self.hl("R", 0, color=VIOLET, rt=0.4)
        self.hl("R", 1, color=VIOLET, rt=0.4)
        self.show(E(r"dB_z=\frac{\mu_0}{4\pi}\frac{I\,R^2\,d\phi}{s^3}",r"dB_z", "I", r"R^2", r"s^3", r"d\phi", r"\frac{\mu_0}{4\pi}", size=M_XL),
                  ("R", "R^2", 0, 0), ("R", None, 1), ("s^2", "s^3"), ("s", None), rt=2.2, wait=2.0)
        self.show(E(r"s^3=\left(R^2+z^2\right)^{3/2}", r"s^3", size=M_M), slot="A", src={("s^3", 0): glyphs(self.slots["H"]["eq"], "s^3", 0)}, rt=1.6, wait=1.5)
        self.caption("Use $s^2=R^2+z^2$ no denominador")
        self.hl("s^3")
        self.show(E(r"dB_z=\frac{\mu_0}{4\pi}\frac{I\,R^2}{(R^2+z^2)^{3/2}}\,d\phi", r"dB_z", "I", r"(R^2+z^2)^{3/2}", r"d\phi", r"\frac{\mu_0}{4\pi}", size=M_XL,
                    colors={r"(R^2+z^2)^{3/2}": VIOLET}),
                  (r"s^3", r"(R^2+z^2)^{3/2}"), rt=2.2, wait=2.0, structure=False)
        self.drop("A")
        self.mark("espira_origem_integrando")
        # ── volta completa ────────────────────────────────────────────────────────────────────────────────
        self.relayout("split", 1.0)
        self.view_to(-4.2, -0.2, 1.05, 1.0)
        self.lf["tri"] = False
        self.lf["comp"] = False
        self.play(FadeOut(VGroup(rl2, sl, zl, dbz)), self.beta.animate.set_value(68), run_time=2.0)
        self.caption("Percorrer uma volta: $I$, $R$, $z$ e $s$ não mudam; só $\\phi$ varre de $0$ a $2\\pi$")
        self.play(self.phi_src.animate.increment_value(2 * math.pi), run_time=8, rate_func=linear)
        self.show(E(r"B_z=\int_0^{2\pi}\frac{\mu_0}{4\pi}\frac{I\,R^2}{(R^2+z^2)^{3/2}}\,d\phi", r"B_z", "I", r"(R^2+z^2)^{3/2}", r"d\phi",
                    r"\frac{\mu_0}{4\pi}", size=M_M, colors={r"(R^2+z^2)^{3/2}": VIOLET}),
                  (r"dB_z", r"B_z"), rt=2.2, wait=2.0)
        self.show(E(r"B_z=\frac{\mu_0}{4\pi}\frac{I\,R^2}{(R^2+z^2)^{3/2}}\int_0^{2\pi}d\phi", r"B_z", "I", r"(R^2+z^2)^{3/2}", r"d\phi",
                    r"\frac{\mu_0}{4\pi}", size=M_M, colors={r"(R^2+z^2)^{3/2}": VIOLET}), rt=2.2, wait=2.0)
        self.caption("O que não depende de $\\phi$ sai da integral; resta somar o ângulo da volta")
        self.show(E(r"\int_0^{2\pi}d\phi=2\pi", r"d\phi", size=M_L), slot="A",
                  src={(r"d\phi", 0): glyphs(self.slots["H"]["eq"], r"d\phi", 0)}, rt=1.8, wait=2.0)
        aux = self.slots["A"]["eq"]
        self.show(E(r"B_z=\frac{\mu_0}{4\pi}\frac{I\,R^2}{(R^2+z^2)^{3/2}}\,2\pi", r"B_z", "I", r"(R^2+z^2)^{3/2}", r"2\pi",
                    r"\frac{\mu_0}{4\pi}", size=M_M, colors={r"(R^2+z^2)^{3/2}": VIOLET}),
                  (r"d\phi", r"2\pi"), rt=2.2, wait=1.5)
        self.drop("A")
        self.caption("A volta inteira dá $2\\pi$; junto com o $4\\pi$ da lei, resta $1/2$")
        hh = self.slots["H"]["eq"]
        self.show(E(r"\frac{2\pi}{4\pi}=\frac{1}{2}", r"\frac{2\pi}{4\pi}", size=M_L), slot="A",
                  src={(r"\frac{2\pi}{4\pi}", 0): [glyphs(hh, r"2\pi", 0), glyphs(hh, r"\frac{\mu_0}{4\pi}", 0)]}, rt=1.8, wait=2.0)
        self.show(E(r"B_z(z)=\frac{\mu_0 I R^2}{2\left(R^2+z^2\right)^{3/2}}", r"B_z", "I", r"\mu_0", size=M_XL, colors={}),
                  rt=2.4, wait=2.5)
        self.drop("A")
        bx = box(self.slots["H"]["eq"], MAG)
        self.play(FadeIn(bx), run_time=0.6)
        self.mark("resultado_espira_eixo")
        self.hold(5)
        self.play(FadeOut(bx), run_time=0.4)
        self.loop_grp, self.loop_flow = grp, flow

    # ── checagens ───────────────────────────────────────────────────────────────────────────────────────────
    def checagens(self):
        self.section("centro", "Checagem 1: o centro da espira")
        R = self.RL
        self.caption("Leve $P$ até $z=0$")
        self.lf.update(field=False, comp=False, tri=False, pair=False, only_comp=False, many=True)
        self.play(self.z_obs.animate.set_value(0), run_time=5, rate_func=smooth)
        self.show(E(r"B(0)=\frac{\mu_0 I R^2}{2R^3}", "B(0)", "I", "R^3", r"\mu_0", size=M_XL),
                  (r"B_z", "B(0)"), rt=2.4, wait=2.0)
        self.caption("Em $z=0$, a separação até cada elemento é igual ao raio $R$")
        self.show(E(r"B(0)=\frac{\mu_0 I}{2R}", "B(0)", "I", r"\mu_0", size=M_XL), rt=2.0, wait=2.0)
        self.caption("No centro não há componente lateral para cancelar")
        self.play(self.phi_src.animate.increment_value(2 * math.pi), run_time=6, rate_func=linear)
        self.mark("espira_centro_sem_laterais")
        self.lf["many"] = False
        self.hold(1.5)
        self.section("distante", "Checagem 2: muito longe da espira")
        self.show(E(r"B_z(z)=\frac{\mu_0 I R^2}{2\left(R^2+z^2\right)^{3/2}}", "B_z", "I", r"\mu_0", size=M_L), (r"B(0)", "B_z"), rt=2.0, wait=1.0)
        self.caption("Afastamos $P$ do centro: a expressão geral acompanha a geometria")
        self.play(self.z_obs.animate.set_value(2.4), run_time=4)
        self.loop_grp.clear_updaters()
        self.loop_flow.clear_updaters(recursive=True)
        self.play(FadeOut(self.loop_grp), FadeOut(self.loop_flow), run_time=0.7)
        self.reset_view(x=-5.7, y=0, scale=1, beta=0, tau=0)

        def far():
            z = self.z_obs.get_value()
            x0, x1, y = -6.7, -0.8, -0.3
            px = x0 + (x1 - x0) * z / (12 * R)
            g = VGroup(Line([x0, y, 0], [x1, y, 0], color=VIOLET, stroke_width=2.4),
                       Ellipse(width=0.35, height=1.65, color=BLUE_L, stroke_width=5).move_to([x0, y, 0]),
                       Dot([px, y, 0], radius=0.1), self.lab("P", [px, y + 0.42, 0], size=M_M), self.lab("z/R", [-0.8, -1.15, 0], size=M_S))
            for u in (0, 3, 6, 9, 12):
                xx = x0 + (x1 - x0) * u / 12
                g.add(Line([xx, y - 0.1, 0], [xx, y + 0.1, 0], color=WHITE, stroke_width=2), self.lab(str(u), [xx, y - 0.45, 0], size=M_S))
            return g
        far_g = self.cached(lambda: self.z_obs.get_value(), far)
        self.add(far_g)
        self.add(self.flow([lambda u: np.array([-6.7 + 0.175 * math.cos(2 * math.pi * u), -0.3 + 0.825 * math.sin(2 * math.pi * u), 0])], count=7))
        self.caption("Esquema axial graduado em $z/R$; a espira está ampliada para permanecer legível")
        self.play(self.z_obs.animate.set_value(12 * R), run_time=7)
        self.caption("$|z|\\gg R$: a distância domina o denominador")
        self.show(E(r"(R^2+z^2)^{3/2}=|z|^3\left(1+\frac{R^2}{z^2}\right)^{3/2}", size=M_M), slot="A", rt=1.8, wait=2.5)
        self.show(E(r"\frac{R^2}{z^2}\to0\ \implies\ (R^2+z^2)^{3/2}\sim|z|^3", size=M_M), slot="A", rt=1.8, wait=2.5)
        self.show(E(r"B_z\sim\frac{\mu_0 I R^2}{2|z|^3}", "B_z", "I", r"\mu_0", size=M_XL), (r"B_z", "B_z"), rt=2.2, wait=2.0)
        self.caption("Longe, o campo da espira cai como $1/|z|^3$ — bem mais rápido que o $1/a$ do fio")
        self.mark("espira_limite_distante")
        self.drop("A")
        cmp_ = E(r"\text{fio}:\ B\propto a^{-1}\qquad\text{espira}:\ B\propto|z|^{-3}", size=M_M)
        self.show(cmp_, slot="A", rt=1.4, wait=4.0)
        self.mark("comparacao_decaimentos")
