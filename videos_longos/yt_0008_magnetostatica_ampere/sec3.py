"""N08–N10: rotacional de B a partir de Biot–Savart — quatro termos, o delta de Dirac e o segundo termo (∇ → −∇', partes,
continuidade). Tudo numa só equação de duas linhas que vai sendo transformada (BUILD)."""
import math

import numpy as np
from manim import (
    VGroup, Line, DashedLine, Dot, FadeIn, FadeOut, Create, Indicate, ValueTracker, LaggedStart, DecimalNumber, Circle,
    DashedVMobject, TransformFromCopy, linear, smooth, UP, DOWN, LEFT, RIGHT,
)
from base import *  # noqa: F401,F403
from fisica import TAU
from sec2 import J_at, BLOB_C, BLOB_A, BLOB_B

# termos (tokens) da equação de trabalho
LHS = (r"\nabla\times", r"\mathbf B(\mathbf r)")
T1J, T1D = r"\mathbf J", r"(\nabla\cdot\mathbf F)"
T2 = r"\mathbf F(\nabla\cdot\mathbf J)"
T3 = r"(\mathbf F\cdot\nabla)\mathbf J"
T4A, T4N, T4B = r"(\mathbf J\cdot", r"\nabla", r")\mathbf F"
MU, P4 = r"\mu_0", r"4\pi"
K2 = r"-\frac{\mu_0}{4\pi}"
DEL = r"\delta^3(\mathbf r-\mathbf r')"
CF = {**FAM, r"\nabla\times\mathbf B": None}


class Sec3:
    # ── N08 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def rot_formal(self):
        self.section("rot_formal", "O rotacional de B a partir de Biot–Savart")
        L = self.dL
        self.relayout("alg", 0.6)
        self.view_to(-4.35, -0.15, 1.05, 1.0)
        T = (r"\mathbf B(\mathbf r)", r"\frac{\mu_0}{4\pi}", r"\int", r"\mathbf J(\mathbf r')", r"\mathbf F", r"d\tau'")
        self.show(E(r"\mathbf B(\mathbf r)=\frac{\mu_0}{4\pi}\int\mathbf J(\mathbf r')\times\mathbf F\,d\tau'", *T, size=M_L, colors=FAM), rt=1.2, wait=1.0)
        self.caption("Agora o rotacional dos dois lados; de novo o operador entra na integral")
        self.show(E(r"\nabla\times\mathbf B(\mathbf r)=\frac{\mu_0}{4\pi}\,\nabla\times\!\int\mathbf J(\mathbf r')\times\mathbf F\,d\tau'", *T, r"\nabla\times",
                    size=M_L, colors=FAM), (None, r"\nabla\times"), rt=1.4, wait=0.6)
        self.show(E(r"\nabla\times\mathbf B(\mathbf r)=\frac{\mu_0}{4\pi}\int\nabla\times\big(\mathbf J(\mathbf r')\times\mathbf F\big)\,d\tau'", *T, r"\nabla\times",
                    size=M_L, colors=FAM), rt=1.8, wait=1.0)
        self.mark("n08_rot_entra")
        # 1 · identidade (diagrama recua; os quatro termos precisam de espaço)
        self.view_to(-5.6, -0.45, 0.72, 1.0)
        idt = (r"\nabla\times(\mathbf A\times\mathbf C)", r"\mathbf A(\nabla\cdot\mathbf C)", r"\mathbf C(\nabla\cdot\mathbf A)", r"(\mathbf C\cdot\nabla)\mathbf A",
               r"(\mathbf A\cdot\nabla)\mathbf C")
        self.show(E(r"\nabla\times(\mathbf A\times\mathbf C)&=\mathbf A(\nabla\cdot\mathbf C)-\mathbf C(\nabla\cdot\mathbf A)\\&\quad+(\mathbf C\cdot\nabla)\mathbf A-(\mathbf A\cdot\nabla)\mathbf C",
                    *idt, size=M_L, colors=FAM), slot="A", rt=1.4, wait=0.3)
        self.caption("O rotacional de um produto vetorial se abre em quatro termos")
        self.hold(1.5)
        # 2 · substituição
        sub = rich("com $\\mathbf A=\\mathbf J(\\mathbf r')$ e $\\mathbf C=\\mathbf F$", T_NOTE).next_to(self.slots["A"]["card"], DOWN, buff=0.1)
        self.play(FadeIn(sub), run_time=0.5)
        self.hold(1.0)
        # 3 · os quatro termos nascem da identidade
        aux = self.slots["A"]["eq"]
        C2 = E(r"\nabla\times\mathbf B(\mathbf r)&=\frac{\mu_0}{4\pi}\int\Big[\mathbf J(\nabla\cdot\mathbf F)-\mathbf F(\nabla\cdot\mathbf J)\\&\qquad+(\mathbf F\cdot\nabla)\mathbf J-(\mathbf J\cdot\nabla)\mathbf F\Big]d\tau'",
               *LHS, MU, P4, r"\int", T1J, T1D, T2, T3, T4A, T4N, T4B, r"d\tau'", size=M_L, colors=CF)
        self.show(C2, (r"\mathbf J(\mathbf r')", None), (r"\mathbf F", None), (r"\nabla\times", None, 1), (r"\frac{\mu_0}{4\pi}", None),
                  src={((T1J, 0), (T1D, 0)): glyphs(aux, idt[1], 0), (T2, 0): glyphs(aux, idt[2], 0), (T3, 0): glyphs(aux, idt[3], 0),
                       ((T4A, 0), (T4N, 0), (T4B, 0)): glyphs(aux, idt[4], 0),
                       ((MU, 0), (P4, 0)): glyphs(self.slots["H"]["eq"], r"\frac{\mu_0}{4\pi}", 0)},
                  rt=2.8, wait=0.5, structure=False)
        eqH = self.slots["H"]["eq"]
        corr = [(idt[1], [T1J, T1D]), (idt[2], [T2]), (idt[3], [T3]), (idt[4], [T4A, T4N, T4B])]
        for k, (ti, tts) in enumerate(corr):
            bxs = VGroup(box(glyphs(aux, ti, 0), WHITE, buff=0.07, width=2.5), box(VGroup(*[glyphs(eqH, t, 0) for t in tts]), WHITE, buff=0.07, width=2.5))
            self.play(Create(bxs), run_time=0.45)
            self.hold(0.5)
            self.out(bxs, rt=0.2)
        self.mark("n08_quatro_termos")
        self.out(sub, rt=0.3)
        # 4 · quais derivam J(r') em relação a r  →  5 · justificativa  →  6 · anular
        self.caption("Dois termos derivam $\\mathbf J(\\mathbf r')$ em relação a $\\mathbf r$")
        self.hl_many([(T2, 0), (T3, 0)], color=CYAN, rt=1.2)
        self.show(E(r"\nabla\cdot\mathbf J(\mathbf r')=0\qquad(\mathbf F\cdot\nabla)\,\mathbf J(\mathbf r')=\mathbf 0", r"\nabla\cdot", r"\nabla",
                    r"\mathbf J(\mathbf r')", r"\mathbf F", r"\mathbf 0", size=M_L, colors=FAM), slot="A", rt=1.4, wait=0.3)
        why = rich("$\\mathbf J(\\mathbf r')$ independe de $\\mathbf r$ (variáveis independentes)", T_NOTE)
        why.next_to(self.slots["A"]["card"], DOWN, buff=0.1)
        self.play(FadeIn(why), run_time=0.4)
        self.caption("Como $\\mathbf J(\\mathbf r')$ não muda quando $\\mathbf r$ se move, esses dois termos são zero")
        self.hold(2.0)
        cut = self.strike([(T2, 0), (T3, 0)], color=CYAN)
        self.hold(0.6)
        self.play(FadeOut(cut), run_time=0.2)
        self.purge(cut)
        C3 = E(r"\nabla\times\mathbf B(\mathbf r)=\frac{\mu_0}{4\pi}\int\Big[\mathbf J(\nabla\cdot\mathbf F)-(\mathbf J\cdot\nabla)\mathbf F\Big]d\tau'",
               *LHS, MU, P4, r"\int", T1J, T1D, T4A, T4N, T4B, r"d\tau'", size=M_L, colors=CF)
        self.show(C3, (T2, None), (T3, None), rt=2.0, wait=1.0)
        self.out(why, rt=0.3)
        self.drop("A", keep_card=False)
        self.view_to(-4.35, -0.15, 1.05, 1.0)
        self.caption("Separe em dois termos e trate cada um")
        old = self.slots["H"]["eq"]
        C4 = E(r"\nabla\times\mathbf B(\mathbf r)&=\frac{\mu_0}{4\pi}\int\mathbf J(\nabla\cdot\mathbf F)\,d\tau'\\&\quad-\frac{\mu_0}{4\pi}\int(\mathbf J\cdot\nabla)\mathbf F\,d\tau'",
               *LHS, MU, P4, K2, r"\int", T1J, T1D, T4A, T4N, T4B, r"d\tau'", size=M_L, colors=CF)
        self.show(C4, (r"\int", r"\int", 0, 0), (r"d\tau'", r"d\tau'", 0, 1),
                  src={(K2, 0): VGroup(glyphs(old, MU, 0), glyphs(old, P4, 0)), (r"\int", 1): glyphs(old, r"\int", 0), (r"d\tau'", 0): glyphs(old, r"d\tau'", 0)},
                  rt=2.2, wait=1.5, structure=False)
        self.n1 = E(r"(1)", size=M_S).set_color(DIM)
        self.n2 = E(r"(2)", size=M_S).set_color(DIM)
        eq = self.slots["H"]["eq"]
        xl = self.slots["H"]["card"].get_left()[0] + 0.15         # numeração dentro do cartão
        self.n1.move_to([xl, glyphs(eq, r"d\tau'", 0).get_center()[1], 0], aligned_edge=LEFT)
        self.n2.move_to([xl, glyphs(eq, r"d\tau'", 1).get_center()[1], 0], aligned_edge=LEFT)
        self.play(FadeIn(self.n1), FadeIn(self.n2), run_time=0.5)
        self.mark("n08_dois_termos")
        self.hold(1.5)

    # ── N09 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def delta(self):
        self.section("delta", "Primeiro termo: o delta de Dirac")
        L = self.dL
        self.hl_many([(T1D, 0)], color=VIOLET, rt=0.8)
        # F em torno da fonte: zero divergência longe, fluxo 4π em volta
        self.df.update(J=False, cell=False, origin=False, R=False)      # a região de corrente sai de cena: agora o protagonista é F
        self.play(*[FadeOut(L[k]) for k in ("J", "dt", "r", "rp", "B", "R")], self.dimk.animate.set_value(0.0), run_time=0.8)
        sx, sy = self.s_x.get_value(), self.s_y.get_value()
        # uma única família de 8 direções radiais, colineares com os raios e de mesmo comprimento: esquema da DIREÇÃO de F (não codifica 1/R²)
        rad = VGroup(*[arrow(self.WD(sx + 0.55 * math.cos(t), sy + 0.55 * math.sin(t)), self.WD(sx + 1.25 * math.cos(t), sy + 1.25 * math.sin(t)),
                             VIOLET, 4, z=5, tip=0.22) for t in np.linspace(0, TAU, 8, endpoint=False)])
        self.play(LaggedStart(*[Create(a) for a in rad], lag_ratio=0.05), run_time=1.4)
        self.caption("$\\mathbf F=\\mathbf R/R^3$, com $R=|\\mathbf R|$, é o núcleo de Biot–Savart (não é $\\mathbf B$): aponta radialmente; $|\\mathbf F|=1/R^2$")
        bx0, by0, c = sx + 1.55, sy + 0.55, 0.26
        cell = self.poly([self.D(bx0 - c, by0 - c), self.D(bx0 + c, by0 - c), self.D(bx0 + c, by0 + c), self.D(bx0 - c, by0 + c)], WHITE, 0.08, z=7).set_stroke(WHITE, 2.5)
        self.play(FadeIn(cell), run_time=0.5)
        self.show(E(r"\nabla\cdot\mathbf F=0\quad(\mathbf r\neq\mathbf r')", r"\nabla\cdot", r"\mathbf F", r"\mathbf r", r"\mathbf r'", size=M_M, colors=FAM), slot="A",
                  rt=1.4, wait=0.5)
        self.caption("Longe de $\\mathbf r'$, o que entra numa célula sai: divergente zero")
        self.hold(2.0)
        self.out(cell, rt=0.4)
        self.rs = ValueTracker(1.3)

        def sphere():
            rr = self.rs.get_value() * self.gs.get_value()
            c0 = self.WD(sx, sy)
            # esfera vista de cima: disco translúcido, borda, brilho deslocado e equador em perspectiva → lê como volume
            return VGroup(Circle(radius=rr, stroke_width=0).set_fill(WHITE, 0.10).move_to(c0).set_z_index(6),
                          Circle(radius=rr * 0.55, stroke_width=0).set_fill(WHITE, 0.08).move_to(c0 + rr * np.array([-0.28, 0.3, 0])).set_z_index(6),
                          Circle(radius=rr, color=WHITE, stroke_width=2.8).move_to(c0).set_z_index(7),
                          DashedVMobject(Circle(radius=rr, color=WHITE, stroke_width=1.8).stretch(0.3, 1).move_to(c0), num_dashes=24).set_opacity(0.6).set_z_index(7))
        sph = self.cached(lambda: (self.rs.get_value(), *self.view_key()), sphere)
        self.play(FadeIn(sph), run_time=0.6)
        self.show(E(r"\oint\mathbf F\cdot d\mathbf a=\frac{1}{R^2}\,4\pi R^2=4\pi", r"\mathbf F", r"\frac{1}{R^2}", r"4\pi R^2", r"4\pi", size=M_M,
                    colors={r"\frac{1}{R^2}": VIOLET, r"4\pi R^2": VIOLET}), slot="A", rt=1.6, wait=0.5)
        self.caption("Mas uma esfera em volta de $\\mathbf r'$ recebe fluxo $4\\pi$, qualquer que seja o raio")
        self.play(self.rs.animate.set_value(0.25), run_time=3.0)
        self.play(self.rs.animate.set_value(0.8), run_time=1.2)
        self.caption("Divergente zero fora da singularidade; todo o fluxo $4\\pi$ está concentrado em $\\mathbf r=\\mathbf r'$")
        self.show(E(r"\nabla\cdot\mathbf F=4\pi\,\delta^3(\mathbf r-\mathbf r')", r"\nabla\cdot", r"\mathbf F", r"4\pi", DEL, size=M_L, colors=FAM), slot="A",
                  rt=1.8, wait=1.5)
        self.mark("n09_div_F_delta")
        self.out(sph, rad, rt=0.5)
        aux = self.slots["A"]["eq"]
        old = self.slots["H"]["eq"]
        D1 = E(r"\nabla\times\mathbf B(\mathbf r)&=\frac{\mu_0}{4\pi}\int\mathbf J(\mathbf r')\,4\pi\,\delta^3(\mathbf r-\mathbf r')\,d\tau'\\&\quad-\frac{\mu_0}{4\pi}\int(\mathbf J\cdot\nabla)\mathbf F\,d\tau'",
               *LHS, MU, P4, K2, r"\int", r"\mathbf J(\mathbf r')", DEL, T4A, T4N, T4B, r"d\tau'", size=M_L, colors=CF)
        self.play(FadeOut(self.n1), FadeOut(self.n2), run_time=0.3)
        self.show(D1, (T1J, r"\mathbf J(\mathbf r')"), (T1D, None), (P4, P4, 0, 0),
                  src={(P4, 1): glyphs(aux, P4, 0), (DEL, 0): glyphs(aux, DEL, 0)}, rt=2.4, wait=1.2, structure=False)
        self.drop("A", keep_card=False)
        self.hl_many([(P4, 0), (P4, 1)], color=WHITE, rt=0.8)
        self.caption("Os dois $4\\pi$ se cancelam")
        D2 = E(r"\nabla\times\mathbf B(\mathbf r)&=\mu_0\int\mathbf J(\mathbf r')\,\delta^3(\mathbf r-\mathbf r')\,d\tau'\\&\quad-\frac{\mu_0}{4\pi}\int(\mathbf J\cdot\nabla)\mathbf F\,d\tau'",
               *LHS, MU, K2, r"\int", r"\mathbf J(\mathbf r')", DEL, T4A, T4N, T4B, r"d\tau'", size=M_L, colors=CF)
        self.show(D2, (P4, None), rt=1.8, wait=1.2, structure=False)
        self.mark("n09_cancela_4pi")
        # ── o delta seleciona r' = r ──────────────────────────────────────────────────────────────────────
        self.caption("Para o rotacional dentro da corrente, leve o observador $\\mathbf r$ para dentro dela")
        self.play(self.dimk.animate.set_value(0.25), self.r_x.animate.set_value(0.75), self.r_y.animate.set_value(0.25), FadeIn(L["obs"]), run_time=2.0)
        self.play(FadeOut(L["obs"]), self.view_to_anims(-4.35, -0.75, 1.15, tau=-58), run_time=2.2)
        self.wd = ValueTracker(0.75)          # largura do delta (esquema)
        rx, ry = self.r_x.get_value(), self.r_y.get_value()
        # a região verde fica fora de cena (dimk = 0): só as contribuições J(r') e o observador, com r fixo e destacado
        od = self.cached(lambda: (*self.view_key(),), lambda: Dot(self.WD(rx, ry), radius=0.11, color=CYAN).set_z_index(11))
        odl = self.pin(self.lab(r"\mathbf r", [0, 0, 0], r"\mathbf r", size=M_M, color=CYAN), lambda: self.WD(rx, ry) + np.array([-0.45, -0.3, 0]))
        self.play(FadeIn(od), FadeIn(odl), run_time=0.5)

        def hgt(rho):
            w = self.wd.get_value()
            return min(3.2, 0.33 / w ** 2) * math.exp(-rho * rho / (2 * w * w))

        def spike():
            w = self.wd.get_value()
            g = VGroup()
            for k in np.linspace(0.15, 2.6, 7):
                rho = k * w
                g.add(self.curve([self.D(rx + rho * math.cos(t), ry + rho * math.sin(t), hgt(rho)) for t in np.linspace(0, TAU, 40)], VIOLET, 2.2, 0.85, z=8))
            for t in np.linspace(0, TAU, 8, endpoint=False):
                g.add(self.curve([self.D(rx + rho * math.cos(t), ry + rho * math.sin(t), hgt(rho)) for rho in np.linspace(0, 2.8 * w, 24)], VIOLET, 1.6, 0.6, z=8))
            return g

        def jgrid():
            w = self.wd.get_value()
            sel = self.sel.get_value()
            g = VGroup()
            for X in rx + 0.42 * np.arange(-7, 5):          # grade passa EXATAMENTE pelo observador: sobra uma única seta
                for Y in ry + 0.36 * np.arange(-4, 3):
                    j = J_at(X, Y)
                    if np.linalg.norm(j) < 1e-6:
                        continue
                    wt = math.exp(-((X - rx) ** 2 + (Y - ry) ** 2) / (2 * w * w)) if sel > 0 else 1.0
                    op = (1 - sel) * 0.85 + sel * wt * 0.85
                    if op < 0.03:
                        continue
                    g.add(arrow(self.WD(X, Y), self.WD(*(np.array([X, Y]) + 0.9 * j)), GREEN, 4, z=6, tip=0.15).set_opacity(op))
            return g
        self.sel = ValueTracker(0.0)
        grid = self.cached(lambda: (self.wd.get_value(), self.sel.get_value(), *self.view_key()), jgrid)
        self.play(FadeIn(grid), run_time=0.8)
        self.caption("Cada ponto-fonte $\\mathbf r'$ contribui com $\\mathbf J(\\mathbf r')$")
        self.hold(1.5)
        sp = self.cached(lambda: (self.wd.get_value(), *self.view_key()), spike)
        self.play(FadeIn(sp), run_time=1.0)
        dl = self.pin(self.lab(DEL, [0, 0, 0], DEL, size=M_S), lambda: self.WD(rx, ry, hgt(0)) + np.array([1.35, 0.15, 0]))
        dsk = txt("esquema da delta 3D", 20, DIM).move_to([-4.2, -2.72, 0])      # fora da figura, sem tocar pico nem rótulos
        self.play(FadeIn(dl), FadeIn(dsk), run_time=0.5)
        norm = self.readout(E(r"\int\delta^3\,d\tau'=", r"d\tau'", size=M_M, colors=FAM), lambda: 1.0, places=2)
        self.caption("O delta é um pico em $\\mathbf r'=\\mathbf r$, com integral 1")
        self.hold(1.5)
        # multiplicar pelo delta pesa cada contribuição; estreitar o pico elimina, uma a uma, as que não estão em r' = r
        self.caption("No integrando, cada $\\mathbf J(\\mathbf r')$ é pesado pelo delta: longe do pico, peso quase zero")
        self.play(self.sel.animate.set_value(1.0), run_time=2.5)
        self.hold(1.0)
        # aviso honesto: a altura desenhada tem teto; a integral 1 é da função, não da figura cortada
        self.oos = self.pin(txt("altura fora de escala", 22, DIM), lambda: self.WD(rx, ry, min(3.2, 0.33 / self.wd.get_value() ** 2)) + np.array([-1.25, 0.0, 0]))
        self.oos.add_updater(lambda m: m.set_opacity(1.0 if 0.33 / self.wd.get_value() ** 2 > 3.2 else 0.0))
        self.add(self.oos)
        self.caption("Estreite o pico: as contribuições somem uma a uma, de fora para dentro")
        self.play(self.wd.animate.set_value(0.4), run_time=3.0, rate_func=linear)
        self.play(self.wd.animate.set_value(0.2), run_time=3.0, rate_func=linear)
        self.play(self.wd.animate.set_value(0.09), run_time=2.5, rate_func=linear)
        self.mark("n09_pico_delta")
        self.caption("Sobrevive uma única contribuição: a do ponto-fonte que coincide com o observador, $\\mathbf r'=\\mathbf r$")
        self.hold(1.5)
        self.play(FadeOut(sp), FadeOut(dl), FadeOut(dsk), FadeOut(grid), FadeOut(self.oos), run_time=0.6)      # fundo sai: só a contribuição que coincide com r
        jr = arrow(self.WD(rx, ry), self.WD(*(np.array([rx, ry]) + 1.6 * J_at(rx, ry))), GREEN, 10, z=12, tip=0.32)
        jl = self.lab(r"\mathbf J(\mathbf r)", self.WD(*(np.array([rx, ry]) + 1.6 * J_at(rx, ry))) + np.array([1.6, -0.5, 0]), r"\mathbf J(\mathbf r)", size=M_L)
        self.play(FadeIn(jr), FadeIn(jl), run_time=0.8)
        self.mark("n09_delta_seleciona")
        self.drop("A", keep_card=False)
        D3 = E(r"\nabla\times\mathbf B(\mathbf r)&=\mu_0\,\mathbf J(\mathbf r)\\&\quad-\frac{\mu_0}{4\pi}\int(\mathbf J\cdot\nabla)\mathbf F\,d\tau'",
               *LHS, MU, K2, r"\int", r"\mathbf J(\mathbf r)", T4A, T4N, T4B, r"d\tau'", size=M_L, colors=CF)
        self.show(D3, (r"\int", None, 0), (r"\mathbf J(\mathbf r')", None), (DEL, None), (r"d\tau'", None, 0),
                  src={(r"\mathbf J(\mathbf r)", 0): VGroup(jr, jl)}, rt=2.4, wait=0.5, structure=False)
        eq = self.slots["H"]["eq"]
        b1 = box(VGroup(glyphs(eq, MU, 0), glyphs(eq, r"\mathbf J(\mathbf r)", 0)), GREEN)
        self.play(FadeIn(b1), run_time=0.5)
        self.caption("Primeiro termo: $\\mu_0\\,\\mathbf J(\\mathbf r)$, a corrente no próprio ponto")
        self.mark("n09_primeiro_termo")
        self.hold(3.0)
        self.out(b1, jr, jl, od, odl, rt=0.8)
        self.df.update(J=True, cell=True, R=True, origin=False)
        self.play(self.view_to_anims(-4.35, -0.15, 1.05, tau=-90), self.dimk.animate.set_value(1.0), self.r_x.animate.set_value(1.75), self.r_y.animate.set_value(1.3), run_time=2.0)

    def view_to_anims(self, x, y, s, **more):
        anims = [self.ox.animate.set_value(x), self.oy.animate.set_value(y), self.gs.animate.set_value(s)]
        return AnimationGroup(*anims, *[getattr(self, k).animate.set_value(v) for k, v in more.items()])

    # ── N10 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def segundo_termo(self):
        self.section("segundo_termo", "Segundo termo: por que ele se anula")
        L = self.dL
        self.hl_many([(K2, 0), (T4A, 0), (T4N, 0), (T4B, 0)], color=VIOLET, rt=0.8)
        self.df["origin"] = True
        self.play(FadeIn(L["R"]), FadeIn(L["r"]), FadeIn(L["rp"]), run_time=0.5)
        self.caption("$\\mathbf F$ depende só da diferença $\\mathbf r-\\mathbf r'$")
        self.show(E(r"\mathbf F=\mathbf F(\mathbf r-\mathbf r')", r"\mathbf F", r"\mathbf r", r"\mathbf r'", size=M_L, colors=FAM), slot="A", rt=1.4, wait=0.5)
        # mover os dois juntos não muda R
        d = np.array([0.5, 0.35])
        self.play(self.r_x.animate.increment_value(d[0]), self.r_y.animate.increment_value(d[1]),
                  self.s_x.animate.increment_value(d[0]), self.s_y.animate.increment_value(d[1]), run_time=2.0)
        self.caption("Mover observador e fonte juntos não muda $\\mathbf R$")
        self.hold(1.2)
        self.play(self.r_x.animate.increment_value(-d[0]), self.r_y.animate.increment_value(-d[1]),
                  self.s_x.animate.increment_value(-d[0]), self.s_y.animate.increment_value(-d[1]), run_time=1.6)
        self.play(self.r_x.animate.increment_value(0.45), run_time=1.4)
        self.caption("Afastar $\\mathbf r$ de $+dx$ muda $\\mathbf R$ como aproximar $\\mathbf r'$ de $-dx$")
        self.play(self.r_x.animate.increment_value(-0.45), self.s_x.animate.increment_value(-0.45), run_time=1.6)
        self.hold(1.0)
        self.play(self.s_x.animate.increment_value(0.45), run_time=1.0)
        self.show(E(r"\frac{\partial\mathbf F}{\partial x}=-\frac{\partial\mathbf F}{\partial x'}", r"\mathbf F", r"\partial x", r"\partial x'", size=M_L,
                    colors={r"\partial x": CYAN, r"\partial x'": GREEN}), slot="A", rt=1.6, wait=1.0)
        self.caption("Vale para cada coordenada: $\\nabla$ agindo em $\\mathbf F$ é $-\\nabla'$")
        self.show(E(r"\nabla\mathbf F=-\nabla'\mathbf F", r"\nabla", r"-\nabla'", r"\mathbf F", size=M_XL, colors=FAM), slot="A", rt=1.6, wait=1.2)
        self.mark("n10_nabla_menos_nabla_linha")
        aux = self.slots["A"]["eq"]
        E4a = E(r"\nabla\times\mathbf B(\mathbf r)&=\mu_0\,\mathbf J(\mathbf r)\\&\quad-\frac{\mu_0}{4\pi}\int(\mathbf J\cdot(-\nabla'))\mathbf F\,d\tau'",
                *LHS, MU, K2, r"\int", r"\mathbf J(\mathbf r)", T4A, r"(-\nabla')", T4B, r"d\tau'", size=M_L, colors=CF)
        # a troca de operador, explícita: o ∇ do integrando e o −∇' da relação acendem juntos antes da substituição
        swap = VGroup(box(glyphs(self.slots["H"]["eq"], T4N, 0), CYAN, buff=0.08, width=3), box(glyphs(aux, r"-\nabla'", 0), GREEN, buff=0.08, width=3))
        self.caption("Troque o $\\nabla$ que age em $\\mathbf F$ por $-\\nabla'$")
        self.play(Create(swap), run_time=0.6)
        self.hold(1.0)
        self.out(swap, rt=0.25)
        self.show(E4a, (T4N, None), src={(r"(-\nabla')", 0): glyphs(aux, r"-\nabla'", 0)}, rt=2.2, wait=1.0, structure=False)
        self.caption("Os dois sinais negativos se cancelam")
        E4b = E(r"\nabla\times\mathbf B(\mathbf r)&=\mu_0\,\mathbf J(\mathbf r)\\&\quad+\frac{\mu_0}{4\pi}\int(\mathbf J\cdot\nabla')\mathbf F\,d\tau'",
                *LHS, MU, r"+\frac{\mu_0}{4\pi}", r"\int", r"\mathbf J(\mathbf r)", T4A, r"\nabla'", T4B, r"d\tau'", size=M_L, colors=CF)
        self.show(E4b, (K2, r"+\frac{\mu_0}{4\pi}"), (r"(-\nabla')", r"\nabla'"), rt=2.0, wait=1.5, structure=False)
        self.mark("n10_sinal")
        # integração por partes, componente a componente
        self.caption("Regra do produto, para cada componente $F_i$")
        self.show(E(r"(\mathbf J\cdot\nabla')F_i=\nabla'\cdot(F_i\,\mathbf J)-F_i\,(\nabla'\cdot\mathbf J)", r"(\mathbf J\cdot\nabla')F_i",
                    r"\nabla'\cdot(F_i\,\mathbf J)", r"F_i\,(\nabla'\cdot\mathbf J)", size=M_M, colors=FAM), slot="A", rt=1.6, wait=1.5)
        self.caption("Pelo teorema da divergência, o termo de divergente vira fluxo numa superfície que envolve a corrente")
        SURF, DIVJ = r"\oint_\infty F_i\,\mathbf J\cdot d\mathbf a'", r"\int F_i\,(\nabla'\cdot\mathbf J)\,d\tau'"
        self.show(E(r"\int(\mathbf J\cdot\nabla')F_i\,d\tau'&=\oint_\infty F_i\,\mathbf J\cdot d\mathbf a'\\&\quad-\int F_i\,(\nabla'\cdot\mathbf J)\,d\tau'",
                    r"(\mathbf J\cdot\nabla')F_i", SURF, DIVJ, size=M_L, colors=FAM),
                  (r"\nabla'\cdot(F_i\,\mathbf J)", SURF), (r"F_i\,(\nabla'\cdot\mathbf J)", DIVJ), slot="A", rt=2.0, wait=1.0)
        self.mark("n10_partes")
        # 1ª razão — corrente localizada: o termo de superfície no infinito é zero (o outro continua na tela)
        self.play(self.view_to_anims(-4.35, -0.15, 0.62), run_time=1.4)
        big = DashedVMobject(self.curve([self.D(BLOB_C[0] + 3.3 * math.cos(t), BLOB_C[1] + 3.3 * math.sin(t)) for t in np.linspace(0, TAU, 80)], WHITE, 2.4, z=7),
                             num_dashes=44)
        bl = rich("superfície distante: $\\mathbf J=0$", T_NOTE).move_to([-4.2, -2.72, 0])
        self.play(Create(big), FadeIn(bl), run_time=1.4)
        self.hl(SURF, slot="A", color=WHITE)
        self.caption("Corrente localizada: na superfície distante não passa corrente, então o termo de superfície é zero")
        self.show(E(r"\int(\mathbf J\cdot\nabla')F_i\,d\tau'&=0\\&\quad-\int F_i\,(\nabla'\cdot\mathbf J)\,d\tau'", r"(\mathbf J\cdot\nabla')F_i", "0", DIVJ, size=M_L,
                    colors=FAM), (SURF, "0"), slot="A", rt=1.8, wait=1.5)
        self.mark("n10_superficie_zero")
        self.out(big, bl, rt=0.5)
        self.play(self.view_to_anims(-4.35, -0.15, 1.05), run_time=1.2)
        # 2ª razão — continuidade + magnetostática: ∇'·J = 0 (mesma célula pequena + zoom do N07)
        def eq_cont():
            cont = E(r"\nabla'\cdot\mathbf J=-\frac{\partial\rho}{\partial t}=0", r"\nabla'\cdot", r"\mathbf J", r"\frac{\partial\rho}{\partial t}", size=M_M, colors=FAM)
            cont.move_to([-4.0, 2.0, 0])
            self.play(FadeIn(cont, shift=UP * 0.1), run_time=0.8)
            self.caption("Continuidade com $\\rho$ constante (magnetostática): $\\nabla'\\cdot\\mathbf J=0$, e o termo restante também é zero")
            self.hl(DIVJ, slot="A", color=GREEN)
            self.show(E(r"\int(\mathbf J\cdot\nabla')F_i\,d\tau'=0-0=0", r"(\mathbf J\cdot\nabla')F_i", "0", size=M_L, colors=FAM), (DIVJ, "0", 0, 1), slot="A",
                      rt=1.8, wait=1.5, structure=False)
            self.mark("n10_continuidade")
            return cont
        self.cont_celula(False, eq_cont)
        self.caption("Com as duas razões, e só agora, o segundo termo some")
        E5 = E(r"\nabla\times\mathbf B(\mathbf r)&=\mu_0\,\mathbf J(\mathbf r)\\&\quad+0", *LHS, MU, r"\mathbf J(\mathbf r)", "0", size=M_L, colors=CF)
        self.show(E5, (r"+\frac{\mu_0}{4\pi}", None), (r"\int", None), (T4A, None), (r"\nabla'", None), (T4B, None), (r"d\tau'", None),
                  rt=2.0, wait=1.0, structure=False)
        self.drop("A", keep_card=False)
        self.show(E(r"\nabla\times\mathbf B=\mu_0\mathbf J", r"\nabla\times", r"\mathbf B", MU, r"\mathbf J", size=M_XL),
                  ("0", None), (r"\mathbf B(\mathbf r)", r"\mathbf B"), (r"\mathbf J(\mathbf r)", r"\mathbf J"), rt=1.8, wait=0.3)
        bx = box(self.slots["H"]["eq"], MAG)
        self.play(FadeIn(bx), run_time=0.5)
        self.caption("A lei local da magnetostática: o rotacional de $\\mathbf B$ é a corrente no ponto")
        self.mark("n10_rot_B_mu0_J")
        self.hold(3.5)
        self.play(FadeOut(bx), run_time=0.3)
