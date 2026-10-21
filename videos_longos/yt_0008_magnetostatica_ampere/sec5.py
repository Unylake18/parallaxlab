"""N14–N16: integrar a lei local numa superfície, Stokes → Lei de Ampère, superfícies com a mesma borda, e a diferença entre
Ampère ser verdadeira e Ampère ser útil.

Superfície S no plano y = 0 do mundo (horizontal), normal +y; C percorrido no sentido +θ de p(r,θ) = r (sen θ, 0, cos θ),
que é o sentido da mão direita em torno de +y. Correntes verticais: +y atravessa S no sentido de n̂ (conta +).
"""
import math

import numpy as np
from manim import (
    VGroup, Line, DashedLine, Dot, FadeIn, FadeOut, Create, Indicate, ValueTracker, LaggedStart, DecimalNumber, Transform,
    DashedVMobject, VMobject, ReplacementTransform, linear, smooth, there_and_back, UP, DOWN, LEFT, RIGHT,
)
from base import *  # noqa: F401,F403
from fisica import TAU, b_fio

RS = 1.9
WIRES = [((0.65, 0.35), 1, "I_1"), ((-0.75, -0.25), 1, "I_2"), ((-0.15, 0.95), -1, "I_3"), ((2.75, -0.7), 1, "I_4")]
YW = 2.1


def pp(r, th, y=0.0):
    return np.array([r * math.sin(th), y, r * math.cos(th)])


class Sec5:
    def dome_y(self, r):
        return self.hb.get_value() * max(0.0, 1 - (r / RS) ** 2)

    def tubes(self):
        """Fios verticais: parte de baixo da superfície apagada (atrás de S, vista de cima)."""
        g = VGroup()
        for (x, z), sg, _ in WIRES:
            r = math.hypot(x, z)
            yc = self.dome_y(r) if r < RS else 0.0
            g.add(self.tube(self.W([x, -YW, z]), self.W([x, yc, z]), STEEL, LW_WIRE).set_opacity(0.4).set_z_index(0))
            g.add(self.tube(self.W([x, yc, z]), self.W([x, YW, z]), STEEL, LW_WIRE))
            a, b = (np.array([x + 0.32, -0.9 * sg + 1.1, z]), np.array([x + 0.32, 0.9 * sg + 1.1, z]))
            g.add(arrow(self.W(a), self.W(b), GREEN, 5, z=6, tip=0.18))
        return g

    def surf(self, inner=0.0, op=0.2, color=VIOLET, dome=True):
        """S como malha polar (permite crescer da borda: inner → 0, e virar cúpula: hb > 0)."""
        g = VGroup()
        nr, nt = 7, 36
        r0 = inner
        rs = np.linspace(r0, RS, nr + 1)
        ths = np.linspace(0, TAU, nt + 1)
        for i in range(nr):
            for j in range(nt):
                q = [(rs[i], ths[j]), (rs[i + 1], ths[j]), (rs[i + 1], ths[j + 1]), (rs[i], ths[j + 1])]
                pts = [pp(r, t, self.dome_y(r) if dome else 0.0) for r, t in q]
                g.add(self.poly(pts, color, op, z=1))
        if self.hb.get_value() > 0.02 and dome:
            for r in np.linspace(RS * 0.35, RS * 0.85, 3):
                g.add(self.curve([pp(r, t, self.dome_y(r)) for t in np.linspace(0, TAU, 60)], color, 1.4, 0.32, z=2))
            for t in np.linspace(0, TAU, 8, endpoint=False):
                g.add(self.curve([pp(r, t, self.dome_y(r)) for r in np.linspace(0, RS, 16)], color, 1.4, 0.32, z=2))
        return g

    def pierce(self):
        g = VGroup()
        for (x, z), sg, _ in WIRES:
            r = math.hypot(x, z)
            if r < RS:
                p = self.W([x, self.dome_y(r), z])
                g.add(Dot(p, radius=0.09, color=GREEN).set_z_index(9), Dot(p, radius=0.15, color=WHITE).set_fill(opacity=0).set_stroke(WHITE, 2).set_z_index(9))
        return g

    # ── N14 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def superficie(self):
        self.section("superficie", "Da lei local a uma lei sobre superfícies")
        self.clear()
        self.reset_view(x=-3.9, y=-0.2, scale=1.0, beta=12, tau=-34)
        self.hb = ValueTracker(0.0)
        W = self.W
        tb = self.cached(lambda: (self.hb.get_value(), *self.view_key()), self.tubes)
        fl = self.flow([lambda u, x=x, z=z: self.W([x, -YW + 2 * YW * u, z]) for (x, z), sg, _ in WIRES if sg > 0], count=6)
        fl2 = self.flow([lambda u, x=x, z=z: self.W([x, -YW + 2 * YW * u, z]) for (x, z), sg, _ in WIRES if sg < 0], count=6, direction=-1)
        labs = {nm: self.pin(self.lab(nm, [0, 0, 0], nm, size=M_S), lambda x=x, z=z: self.W([x, YW + 0.25, z]) + np.array([0.0, 0.1, 0])) for (x, z), sg, nm in WIRES}
        self.play(FadeIn(tb), run_time=1.0)
        self.add(fl, fl2)
        self.play(*[FadeIn(m) for m in labs.values()], run_time=0.6)
        self.show(E(r"\nabla\times\mathbf B=\mu_0\mathbf J", r"\nabla\times\mathbf B", r"\mu_0", r"\mathbf J", size=M_XL), rt=1.2, wait=1.0)
        self.caption("A lei local vale em cada ponto. Some ela sobre uma superfície")
        # C primeiro, depois S nasce da borda
        cC = self.cached(self.view_key, lambda: self.loop3d([0, 0, 0], RS, [0, 1, 0], VIOLET, 4.5, arrows=4, tip=0.22))
        self.play(Create(cC), run_time=1.6)
        cL = self.pin(self.lab("C", [0, 0, 0], "C", size=M_M, color=VIOLET), lambda: self.W([RS, 0, 0]) + np.array([0.38, 0.05, 0]))
        self.play(FadeIn(cL), run_time=0.4)
        self.caption("Primeiro a borda $C$, com um sentido de percurso")
        self.hold(1.2)
        self.inner = ValueTracker(RS - 0.01)
        S = self.cached(lambda: (self.inner.get_value(), self.hb.get_value(), *self.view_key()), lambda: self.surf(self.inner.get_value()))
        self.add(S)
        self.play(self.inner.animate.set_value(0.0), run_time=3.0, rate_func=smooth)
        sL = self.pin(self.lab("S", [0, 0, 0], "S", size=M_M, color=VIOLET), lambda: self.W([-1.05, 0.0, 1.15]) + np.array([-0.3, -0.25, 0]))
        self.play(FadeIn(sL), run_time=0.4)
        self.caption("A superfície $S$ nasce da borda: $\\partial S=C$")
        self.mark("n14_superficie_da_borda")
        self.hold(1.5)
        # normal e mão direita
        nn = self.cached(lambda: (self.hb.get_value(), *self.view_key()), lambda: VGroup(
            *[self.normal(pp(r, t, self.dome_y(r)), [0, 1, 0], 0.6, WHITE, 3) for r, t in [(0.0, 0), (1.2, 1.1), (1.2, 4.0)]],
            self.loop3d([0, 1.05 + self.dome_y(0), 0], 0.28, [0, 1, 0], WHITE, 2.5, arrows=1, tip=0.13)))
        daL = self.pin(self.lab(r"d\mathbf a", [0, 0, 0], r"d\mathbf a", size=M_S), lambda: self.W(pp(1.2, 1.1, 0.75 + self.dome_y(1.2))) + np.array([0.35, 0.05, 0]))
        self.play(FadeIn(nn), FadeIn(daL), run_time=0.8)
        self.caption("Mão direita: dedos no sentido de $C$, polegar na normal de $S$")
        self.mark("n14_mao_direita")
        self.hold(2.5)
        self.caption("Integre os dois lados sobre $S$")
        self.show(E(r"\int_S(\nabla\times\mathbf B)\cdot d\mathbf a=\mu_0\int_S\mathbf J\cdot d\mathbf a", r"\int_S", r"(\nabla\times\mathbf B)", r"\mu_0", r"\mathbf J",
                    r"\cdot d\mathbf a", size=M_M), (r"\nabla\times\mathbf B", r"(\nabla\times\mathbf B)"),
                  src={((r"\int_S", 0), (r"\int_S", 1)): sL, ((r"\cdot d\mathbf a", 0), (r"\cdot d\mathbf a", 1)): daL}, rt=2.2, wait=1.5)
        # J·da: quem atravessa S, e em que sentido
        pc = self.cached(lambda: (self.hb.get_value(), *self.view_key()), self.pierce)
        self.play(FadeIn(pc), run_time=0.6)
        self.caption("$\\mathbf J\\cdot d\\mathbf a$ só não é zero onde a corrente fura $S$; o sinal vem do sentido")
        self.hold(1.5)
        self.show(E(r"\int_S\mathbf J\cdot d\mathbf a=I_1+I_2-I_3", r"\mathbf J", r"\cdot d\mathbf a", r"\int_S", "I_1", "I_2", "I_3", size=M_L), slot="A",
                  src={("I_1", 0): labs["I_1"], ("I_2", 0): labs["I_2"], ("I_3", 0): labs["I_3"]}, rt=2.2, wait=1.0)
        n4 = rich("$I_4$ não atravessa $S$", T_NOTE).next_to(self.slots["A"]["card"], DOWN, buff=0.1)
        self.play(FadeIn(n4), Indicate(labs["I_4"], color=WHITE), run_time=0.8)
        self.hold(1.5)
        old = self.slots["A"]["eq"]
        self.show(E(r"\int_S\mathbf J\cdot d\mathbf a=I_{\rm env}", r"\mathbf J", r"\cdot d\mathbf a", r"\int_S", r"I_{\rm env}", size=M_L),
                  ("I_1", None), ("I_2", None), ("I_3", None), slot="A",
                  src={(r"I_{\rm env}", 0): VGroup(glyphs(old, "I_1", 0), glyphs(old, "I_2", 0), glyphs(old, "I_3", 0))}, rt=1.6, wait=1.0)
        self.play(FadeOut(n4), run_time=0.3)
        aux = self.slots["A"]["eq"]
        self.show(E(r"\int_S(\nabla\times\mathbf B)\cdot d\mathbf a=\mu_0 I_{\rm env}", r"\int_S", r"(\nabla\times\mathbf B)", r"\mu_0", r"I_{\rm env}", r"\cdot d\mathbf a",
                    size=M_M), (r"\int_S", None, 1), (r"\cdot d\mathbf a", None, 1), (r"\mathbf J", None),
                  src={(r"I_{\rm env}", 0): glyphs(aux, r"I_{\rm env}", 0)}, rt=2.0, wait=1.0)
        self.drop("A", keep_card=False)
        self.mark("n14_corrente_envolvida")
        self.st = dict(tb=tb, fl=fl, fl2=fl2, labs=labs, cC=cC, cL=cL, S=S, sL=sL, nn=nn, daL=daL, pc=pc)

    # ── N15 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def stokes(self):
        self.section("stokes", "Stokes: do interior para a borda")
        st = self.st
        self.play(FadeOut(st["nn"]), FadeOut(st["daL"]), run_time=0.4)
        # ladrilhos: cada célula é uma sonda que circula no mesmo sentido de C
        nr, nt, m = 3, 8, 0.0          # m=0: lados vizinhos coincidem exatamente (o cancelamento depende disso)
        rs = np.linspace(0.0, RS, nr + 1)
        ths = np.linspace(0, TAU, nt + 1)

        def edges(i, j, color=WHITE, w=1.8, tip=0.05):
            """Os 4 lados orientados da célula (anel i, setor j): [arco externo, raio em t1, arco interno, raio em t0]."""
            r0, r1 = rs[i] + (m if i else 0.0), rs[i + 1] - m          # setores centrais chegam a r = 0: sem furo no meio
            t0, t1 = ths[j] + m / max(rs[i + 1], 0.5), ths[j + 1] - m / max(rs[i + 1], 0.5)
            out = []
            for f, a, b in [(lambda t, r=r1: pp(r, t), t0, t1), (None, (r1, r0), t1), (lambda t, r=r0: pp(r, t), t1, t0), (None, (r0, r1), t0)]:
                if f is not None:
                    if f(t0)[0] == 0.0 and f(t0)[2] == 0.0:            # arco de raio zero: o setor central é um triângulo
                        out.append(VGroup())
                        continue
                    pts = [f(t) for t in np.linspace(a, b, 10)]
                    mid = a + 0.3 * (b - a)          # as duas setas do mesmo lado ficam em pontos distintos
                    d = np.sign(b - a) * 0.02
                    p0, p1 = self.W(f(mid - d)), self.W(f(mid + d))
                    out.append(VGroup(self.curve(pts, color, w, 0.95, z=7), self.arrowhead(self.W(f(mid)), p1 - p0, 2.2 * tip, color, z=8)))
                else:
                    pa, pb = pp(a[0], b), pp(a[1], b)
                    mid = pa + 0.3 * (pb - pa)
                    out.append(VGroup(Line(self.W(pa), self.W(pb), color=color, stroke_width=w).set_z_index(7),
                                      self.arrowhead(self.W(mid), self.W(pb) - self.W(pa), 2.2 * tip, color, z=8)))
            return out

        # 1 · duas células vizinhas: a aresta comum é percorrida em sentidos opostos
        self.caption("Comece com duas sondas vizinhas, ambas circulando no sentido de $C$")
        hide = [st["tb"], st["fl"], st["fl2"], st["pc"], *st["labs"].values()]
        self.play(*[FadeOut(m) for m in hide], run_time=0.5)      # fios saem só durante a demonstração (updaters preservados)
        self.view_to(-3.9, 0.2, 1.4, 1.6, tau=-90, beta=0)         # vista de cima, disco inteiro no quadro: as duas células ficam grandes
        cA, cB = edges(2, 0, WHITE, 3.4, 0.17), edges(2, 1, CYAN, 3.4, 0.17)
        gA, gB = VGroup(*cA), VGroup(*cB)
        self.play(Create(gA), run_time=1.2)
        self.play(Create(gB), run_time=1.2)
        shared = VGroup(cA[1], cB[3])                       # raio em t1 de A (para dentro) e raio em t0 de B (para fora)
        self.play(Indicate(shared, color=MAG, scale_factor=1.0), run_time=1.2)
        self.caption("O lado comum é percorrido uma vez para dentro e outra para fora: as contribuições se cancelam")
        self.hold(1.5)
        self.out(shared, rt=0.8)
        self.caption("Somadas, as duas sondas equivalem a uma só, contornando apenas a borda de fora")
        self.mark("n15_duas_celulas")
        self.hold(2.0)
        self.out(gA, gB, rt=0.5)
        self.view_to(-3.9, -0.2, 1.0, 1.6, tau=-34, beta=12)
        self.play(*[FadeIn(m) for m in hide], run_time=0.5)
        # 2 · a malha inteira
        inner_edges, outer_edges = VGroup(), VGroup()
        for i in range(nr):
            for j in range(nt):
                e = edges(i, j)
                if i == nr - 1:
                    outer_edges.add(e[0])
                    inner_edges.add(e[1], e[2], e[3])
                else:
                    inner_edges.add(*e)
        mesh = VGroup(inner_edges, outer_edges)
        self.play(Create(mesh), run_time=2.4)
        self.caption("Agora a superfície inteira: cada sonda mede o rotacional vezes a sua área")
        self.show(E(r"\int_S(\nabla\times\mathbf B)\cdot d\mathbf a=\sum_{\rm sondas}\oint\mathbf B\cdot d\boldsymbol\ell", r"\int_S", r"(\nabla\times\mathbf B)",
                    r"\cdot d\mathbf a", r"\sum_{\rm sondas}", r"\oint\mathbf B\cdot d\boldsymbol\ell", size=M_M), slot="A", rt=1.6, wait=1.0)
        self.mark("n15_sondas")
        self.caption("Todos os lados internos se cancelam aos pares, como nas duas células")
        self.play(Indicate(inner_edges, color=CYAN, scale_factor=1.0), run_time=1.2)
        self.play(FadeOut(inner_edges), run_time=1.6)
        self.caption("Só sobra a borda: a circulação em $C$")
        self.play(Indicate(outer_edges, color=VIOLET, scale_factor=1.0), run_time=1.2)
        self.play(FadeOut(outer_edges), Indicate(st["cC"], color=WHITE, scale_factor=1.0), run_time=1.0)
        self.purge(mesh)
        self.show(E(r"\int_S(\nabla\times\mathbf B)\cdot d\mathbf a=\oint_C\mathbf B\cdot d\boldsymbol\ell", r"\int_S", r"(\nabla\times\mathbf B)", r"\cdot d\mathbf a",
                    r"\oint_C", r"\mathbf B\cdot d\boldsymbol\ell", size=M_M), (r"\sum_{\rm sondas}", None),
                  (r"\oint\mathbf B\cdot d\boldsymbol\ell", r"\mathbf B\cdot d\boldsymbol\ell"), src={(r"\oint_C", 0): st["cL"]}, slot="A", rt=2.0, wait=0.5)
        tS = txt("teorema de Stokes", T_NOTE, DIM).next_to(self.slots["A"]["card"], DOWN, buff=0.1)
        self.play(FadeIn(tS), run_time=0.4)
        self.mark("n15_stokes")
        self.hold(1.5)
        aux = self.slots["A"]["eq"]
        hb1 = box(VGroup(glyphs(aux, r"\int_S", 0), glyphs(aux, r"(\nabla\times\mathbf B)", 0), glyphs(aux, r"\cdot d\mathbf a", 0)), MAG, buff=0.14)     # UM único destaque
        self.play(Create(hb1), run_time=0.6)
        self.hold(0.6)
        self.out(hb1, rt=0.3)
        self.show(E(r"\oint_C\mathbf B\cdot d\boldsymbol\ell=\mu_0 I_{\rm env}", r"\oint_C", r"\mathbf B\cdot d\boldsymbol\ell", r"\mu_0", r"I_{\rm env}", size=M_XL),
                  (r"\int_S", None), (r"(\nabla\times\mathbf B)", None), (r"\cdot d\mathbf a", None),
                  src={((r"\oint_C", 0), (r"\mathbf B\cdot d\boldsymbol\ell", 0)): VGroup(glyphs(aux, r"\oint_C", 0), glyphs(aux, r"\mathbf B\cdot d\boldsymbol\ell", 0))},
                  rt=2.2, wait=0.3)
        self.play(FadeOut(tS), run_time=0.3)
        self.drop("A", keep_card=False)
        bx = box(self.slots["H"]["eq"], MAG)
        nm = txt("Lei de Ampère · magnetostática", T_NOTE, WHITE).next_to(self.slots["H"]["card"], DOWN, buff=0.12)
        self.play(FadeIn(bx), FadeIn(nm), run_time=0.6)
        self.caption("Agora sim: a Lei de Ampère, nascida de $\\nabla\\times\\mathbf B=\\mu_0\\mathbf J$ e de Stokes")
        self.mark("n15_ampere")
        self.hold(3.5)
        self.play(FadeOut(bx), run_time=0.3)
        # outra superfície, mesma borda
        self.caption("Troque $S$ por outra superfície com a mesma borda $C$")
        ghost = self.cached(self.view_key, lambda: VGroup(*[m.set_fill(opacity=0.06) for m in self.surf(0.0, 0.06, VIOLET, dome=False)]))
        self.add(ghost)
        self.play(self.hb.animate.set_value(1.25), FadeOut(st["sL"]), run_time=3.0, rate_func=smooth)
        s1 = self.pin(self.lab("S_1", [0, 0, 0], "S_1", size=M_M, color=VIOLET), lambda: self.W([-1.35, 0, 1.25]) + np.array([-0.35, -0.3, 0]))
        s2 = self.pin(self.lab("S_2", [0, 0, 0], "S_2", size=M_M, color=VIOLET), lambda: self.W([1.25, self.dome_y(1.27), 0.25]) + np.array([0.5, 0.25, 0]))
        self.play(FadeIn(s1), FadeIn(s2), run_time=0.5)
        self.caption("As mesmas correntes atravessam a cúpula $S_2$")
        self.show(E(r"I_{S_1}=I_1+I_2-I_3=I_{S_2}", r"I_{S_1}", r"I_{S_2}", "I_1", "I_2", "I_3", size=M_L, colors={r"I_{S_1}": GREEN, r"I_{S_2}": GREEN}),
                  slot="A", rt=1.6, wait=1.5)
        self.mark("n15_cupula")
        self.caption("Juntas, $S_1$ e $S_2$ fecham um volume $V$: o que entra por $S_1$ sai por $S_2$")
        self.play(ghost.animate.set_fill(opacity=0.28), run_time=0.8)          # o fundo plano fica visível: superfície fechada
        vL = self.pin(self.lab("V", [0, 0, 0], "V", size=M_L, color=WHITE), lambda: self.W([-0.45, 0.45 * self.hb.get_value(), 0.25]))
        self.play(FadeIn(vL), run_time=0.5)
        self.hold(1.0)
        self.show(E(r"\oint_{S_1-S_2}\mathbf J\cdot d\mathbf a=\int_V\nabla\cdot\mathbf J\,d\tau=0", r"\mathbf J", r"\nabla\cdot\mathbf J", size=M_M,
                    colors={r"\nabla\cdot\mathbf J": GREEN}), slot="A", rt=1.6, wait=1.5)
        self.caption("Corrente estacionária: $\\nabla\\cdot\\mathbf J=0$, nada se acumula dentro. Logo a corrente envolvida não depende de $S$")
        self.show(E(r"I_{S_1}=I_{S_2}", r"I_{S_1}", r"I_{S_2}", size=M_XL, colors={r"I_{S_1}": GREEN, r"I_{S_2}": GREEN}), slot="A", rt=1.4, wait=0.5)
        self.mark("n15_mesma_corrente")
        self.hold(3.0)
        self.out(vL, s1, s2, nm, rt=0.5)
        self.play(self.hb.animate.set_value(0.0), run_time=2.0)
        self.purge(ghost)

    # ── N16 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def validade(self):
        self.section("validade", "Verdadeira não é o mesmo que útil")
        self.clear()
        self.reset_view(x=-4.0, y=-0.35, scale=1.05, beta=0, tau=-90)     # caminho amperiano: raciocínio em 2D, vista de cima
        W = self.W
        self.km = ValueTracker(0.0)

        def cpt(t):
            k = self.km.get_value()
            r = 1.75 * (1 + (1 - k) * (0.28 * math.cos(2 * t) + 0.16 * math.sin(3 * t)))
            c = (1 - k) * np.array([0.35, 0, -0.25])
            return c + pp(r, t)

        def sdir(p, v):
            d = self.W(p + 1e-3 * v) - self.W(p)
            return d / np.linalg.norm(d)

        def contour():
            g = VGroup(self.path3d(cpt, 0, TAU, [0, 0, 0], VIOLET, 4.5, N=140))
            for t in np.linspace(0, TAU, 8, endpoint=False) + 0.2:
                p = cpt(t)
                tang = cpt(t + 1e-3) - cpt(t - 1e-3)
                s = math.hypot(p[0], p[2])
                bdir = np.array([p[2], 0, -p[0]]) / s                    # φ̂
                q = self.W(p)
                g.add(arrow(q, q + 0.55 * sdir(p, tang), WHITE, 4, z=7, tip=0.2),
                      arrow(q, q + 1.05 * (1.75 / s) * sdir(p, bdir), MAG, 6, z=8, tip=0.26),
                      Dot(q, radius=0.05, color=WHITE).set_z_index(9))
            return g
        wire = self.out_symbol(W([0, 0, 0]), 1, 0.2, GREEN)
        il = self.lab("I", W([0, 0, 0]) + np.array([-0.45, 0.4, 0]), "I", size=M_M)
        cg = self.cached(lambda: (self.km.get_value(), *self.view_key()), contour)
        self.play(FadeIn(wire), FadeIn(il), run_time=0.6)
        self.play(FadeIn(cg), run_time=1.2)
        fl = VGroup()
        self.caption("Um contorno qualquer em volta do fio: $\\mathbf B$ (magenta) e $d\\boldsymbol\\ell$ (branco) mudam de um ponto a outro")
        self.show(E(r"\oint_C\mathbf B\cdot d\boldsymbol\ell=\mu_0 I", r"\oint_C", r"\mathbf B\cdot d\boldsymbol\ell", "I", size=M_XL), rt=1.4, wait=0.3)
        ok = txt("verdadeira", T_NOTE, GREEN).next_to(self.slots["H"]["card"], DOWN, buff=0.12)
        self.play(FadeIn(ok), run_time=0.4)
        self.hold(1.5)
        self.caption("Mas $\\mathbf B\\cdot d\\boldsymbol\\ell$ varia ao longo de $C$: não há como tirar $B$ da integral")
        self.show(E(r"\mathbf B\cdot d\boldsymbol\ell\ \text{varia em}\ C\ \Rightarrow\ B=\,?", r"\mathbf B\cdot d\boldsymbol\ell", size=M_M), slot="A", rt=1.4, wait=2.0)
        self.mark("n16_contorno_qualquer")
        self.caption("Ampère ser verdadeira $\\neq$ Ampère ser útil para calcular $\\mathbf B$")
        self.hold(2.5)
        self.caption("Com simetria, escolha o caminho: um círculo centrado no fio")
        self.play(self.km.animate.set_value(1.0), run_time=3.5, rate_func=smooth)
        self.caption("Agora $\\mathbf B$ é paralelo a $d\\boldsymbol\\ell$ e tem o mesmo módulo em todo o caminho")
        self.show(E(r"\oint_C\mathbf B\cdot d\boldsymbol\ell=B\oint_C d\ell", r"\oint_C", r"\mathbf B\cdot d\boldsymbol\ell", "B", r"d\ell", size=M_L, colors={"B": MAG}),
                  slot="A", rt=1.6, wait=1.0)
        self.caption("$B$ sai da integral: a lei verdadeira virou ferramenta")
        self.mark("n16_circulo_simetrico")
        self.hold(2.0)
        self.drop("A", keep_card=False)
        self.play(FadeOut(ok), run_time=0.3)
        self.drop("H", keep_card=False)
        bar = self.strategy_bar()
        self.play(FadeOut(self.head), run_time=0.3)
        self.head = None
        self.play(FadeIn(bar), run_time=0.8)
        for i in range(5):
            self.light(bar, i, rt=0.45)
            self.hold(0.5)
        self.caption("Com simetria, Ampère vira método: cada passo da barra prepara a integral para ficar simples")
        self.mark("n16_estrategia")
        self.hold(3.0)
        self.bar = bar
        for m in bar.steps:
            m.set_opacity(0.35)
        self.out(cg, wire, il, rt=0.6)
