"""N17–N20 (V2): fio, lâmina, solenoide (dois amperianos) e toroide ideal — sempre geometria → simetria → caminho → B·dℓ →
corrente encerrada → álgebra, com a barra de estratégia acendendo o passo atual.

Política 2.5D × 2D: o objeto é estabelecido em 2.5D; o raciocínio com caminho amperiano acontece em 2D (vista de cima para
fio e toroide, corte frontal para lâmina e solenoide).
"""
import math

import numpy as np
from manim import (
    VGroup, Line, DashedLine, Dot, Polygon, Rectangle, Circle, FadeIn, FadeOut, Create, Indicate, ValueTracker, LaggedStart,
    DashedVMobject, VMobject, Ellipse, Transform, TransformFromCopy, ReplacementTransform, linear, smooth, there_and_back,
    UP, DOWN, LEFT, RIGHT,
)
from base import *  # noqa: F401,F403
from fisica import TAU

CI = {"2\\pi s": VIOLET, "(2\\pi s)": VIOLET, "B": MAG, "B_{\\rm dentro}": MAG, "B_{\\rm fora}": MAG, "\\,L": WHITE, "\\,n": VIOLET,
      "\\,I": GREEN, "\\mu_0 K": GREEN, "2B": MAG, "(nL)": VIOLET}


class Sec6:
    def app_start(self, title):
        if not hasattr(self, "bar"):          # trecho começado com DE= depois do N16
            self.bar = self.strategy_bar()
            self.add(self.bar)
        self.clear(keep=(self.bar,))
        self.relayout("app", 0.01)
        new = txt(title, T_HEAD).move_to([0, 3.3, 0])
        if self.head is not None:
            self.play(FadeOut(self.head), run_time=0.25)
            self.purge(self.head)
        self.play(FadeIn(new), run_time=0.5)
        self.head = new
        for m in self.bar.steps:
            m.set_opacity(0.35)

    def rect_path(self, x0, x1, y0, y1, color=VIOLET, width=4.5, tip=0.26, dashed=False):
        """Retângulo no plano da tela (vista frontal), anti-horário (normal saindo da tela), com pontas grandes."""
        P = [np.array(p) for p in [(x0, y0, 0), (x1, y0, 0), (x1, y1, 0), (x0, y1, 0)]]
        g = VGroup()
        for i in range(4):
            a, b = self.W(P[i]), self.W(P[(i + 1) % 4])
            ln = DashedLine(a, b, color=color, stroke_width=width, dash_length=0.12) if dashed else Line(a, b, color=color, stroke_width=width)
            g.add(ln.set_z_index(7))
            g.add(self.arrowhead((a + b) / 2, b - a, tip, color, z=9))
        return g

    # ── N17 · fio ───────────────────────────────────────────────────────────────────────────────────────────
    def amp_fio(self):
        self.section("amp_fio")
        self.app_start("Fio infinito, agora por Ampère")
        self.reset_view(x=-3.9, y=-0.55, scale=0.95, beta=0, tau=-24)
        W = self.W
        S = 1.45
        wire = self.cached(self.view_key, lambda: self.wire_y(-2.0, 2.0))
        fl = self.flow_y(-2.0, 2.0, count=7)
        il = self.lab("I", W([-0.4, 1.3, 0]), "I", size=M_M)
        rings = self.cached(self.view_key, lambda: VGroup(*[self.ring_y(S, h, width=3.0, op=0.8, tip=0.26) for h in (-1.2, 0.0, 1.2)]))
        self.play(FadeIn(wire), FadeIn(il), run_time=0.8)
        self.add(fl)
        self.caption("Geometria: um fio reto, infinito, com corrente $I$")
        self.hold(1.0)
        # 0 · simetria (em 2.5D: o objeto)
        self.light(self.bar, 0)
        self.play(FadeIn(rings), run_time=0.8)
        self.play(self.beta.animate.set_value(70), run_time=2.2)
        self.play(self.beta.animate.set_value(0), run_time=1.5)
        self.caption("Girar em torno do fio ou deslizar ao longo dele não muda nada: $B$ só depende de $s$")
        self.hold(1.0)
        # para a vista de cima (2D): é nela que o caminho é escolhido
        self.out(fl, il, rt=0.3)
        self.out(rings, rt=0.5)               # grupos dependentes da vista saem ANTES de a vista girar
        self.play(self.tau.animate.set_value(-90), self.ox.animate.set_value(-4.3), self.oy.animate.set_value(0.0), self.gs.animate.set_value(1.0), run_time=2.0)
        sym = self.out_symbol(W([0, 0, 0]), 1, 0.2, GREEN)
        il2 = self.lab("I", W([0, 0, 0]) + np.array([-0.45, 0.4, 0]), "I", size=M_M)
        self.play(FadeOut(wire), FadeIn(sym), FadeIn(il2), run_time=0.6)
        self.purge(wire)
        # 1 · direção
        self.light(self.bar, 1)
        P = W([S, 0, 0])
        bv = arrow(P, P + np.array([0, 1.15, 0]), MAG, 8, tip=0.32).set_z_index(9)
        bL = self.lab("B", P + np.array([0.45, 0.85, 0]), "B", size=M_L, color=MAG)
        self.play(FadeIn(Dot(P, radius=0.07, color=WHITE).set_z_index(10)), Create(bv), FadeIn(bL), run_time=1.0)
        self.show(E(r"\mathbf B=B(s)\,\hat{\boldsymbol\phi}", r"\mathbf B", r"B(s)", r"\hat{\boldsymbol\phi}", size=M_L), rt=1.4, wait=0.8)
        self.caption("Direção: tangente ao círculo em torno do fio")
        # 2 · caminho
        self.light(self.bar, 2)
        circ = DashedVMobject(Circle(radius=S * self.gs.get_value(), color=VIOLET, stroke_width=4).move_to(W([0, 0, 0])), num_dashes=40)
        rad = Line(W([0, 0, 0]), P, color=VIOLET, stroke_width=2.5).set_z_index(6)
        sl = self.lab("s", W([S / 2, 0, 0]) + np.array([0, -0.3, 0]), "s", size=M_M)
        self.play(Create(circ), Create(rad), FadeIn(sl), run_time=1.4)
        self.caption("Caminho: o círculo de raio $s$ centrado no fio, onde $|\\mathbf B|$ é o mesmo em todo ponto")
        self.show(E(r"\oint_C\mathbf B\cdot d\boldsymbol\ell=\mu_0 I_{\rm enc}", r"\oint_C", r"\mathbf B\cdot d\boldsymbol\ell", r"\mu_0", r"I_{\rm enc}", size=M_L),
                  rt=1.6, wait=0.8)
        # 3 · B·dℓ: primeiro um dℓ grande, paralelo a B; depois o mesmo em todo o círculo
        self.light(self.bar, 3)
        dl = arrow(P, P + np.array([0, 0.62, 0]), WHITE, 5, tip=0.22).set_z_index(10).shift(RIGHT * 0.3)
        dL = self.lab(r"d\boldsymbol\ell", P + np.array([0.55, 0.3, 0]), r"d\boldsymbol\ell", size=M_M)
        self.play(Create(dl), FadeIn(dL), run_time=0.9)
        self.caption("Em cada ponto do caminho, $\\mathbf B$ e $d\\boldsymbol\\ell$ são paralelos: $\\mathbf B\\cdot d\\boldsymbol\\ell=B\\,d\\ell$")
        self.hold(1.5)
        reps = VGroup()
        for t in np.linspace(0, TAU, 8, endpoint=False)[1:]:
            q = W([S * math.cos(t), 0, -S * math.sin(t)])
            d = np.array([-math.sin(t), math.cos(t), 0])
            reps.add(arrow(q, q + 1.15 * d, MAG, 7, tip=0.28), arrow(q + 0.3 * np.array([d[1], -d[0], 0]), q + 0.3 * np.array([d[1], -d[0], 0]) + 0.62 * d, WHITE, 4, tip=0.2))
        self.play(LaggedStart(*[TransformFromCopy(VGroup(bv, dl), VGroup(reps[2 * k], reps[2 * k + 1])) for k in range(7)], lag_ratio=0.15), run_time=2.4)
        self.caption("O mesmo vale em todo o círculo, e $B$ tem o mesmo valor: sai da integral")
        self.show(E(r"B\oint_C d\ell=\mu_0 I_{\rm enc}", "B", r"\oint_C", r"d\ell", r"\mu_0", r"I_{\rm enc}", size=M_L, colors=CI),
                  (r"\mathbf B\cdot d\boldsymbol\ell", r"d\ell"), src={("B", 0): bL}, rt=1.8, wait=1.0)
        # o perímetro 2πs nasce do círculo: ele se desenrola
        self.out(reps, dl, dL, rt=0.4)
        L = TAU * S * self.gs.get_value()
        y0 = -2.05
        seg = Line([-6.9, y0, 0], [-6.9 + L, y0, 0], color=VIOLET, stroke_width=4).set_z_index(6)
        tick = VGroup(Line([-6.9, y0 - 0.12, 0], [-6.9, y0 + 0.12, 0], color=VIOLET, stroke_width=3),
                      Line([-6.9 + L, y0 - 0.12, 0], [-6.9 + L, y0 + 0.12, 0], color=VIOLET, stroke_width=3))
        ghost = Circle(radius=S * self.gs.get_value(), color=VIOLET, stroke_width=4).move_to(W([0, 0, 0])).rotate(-math.pi / 2)
        self.caption("Desenrole o círculo: o comprimento do caminho é $2\\pi s$")
        self.play(Transform(ghost, seg), run_time=2.2)
        self.add(seg)
        self.remove(ghost)
        pl = self.lab(r"2\pi s", [-6.9 + L / 2, y0 + 0.38, 0], r"2\pi s", size=M_M, colors=CI)
        self.play(FadeIn(tick), FadeIn(pl), run_time=0.6)
        self.show(E(r"B\,(2\pi s)=\mu_0 I_{\rm enc}", "B", r"(2\pi s)", r"\mu_0", r"I_{\rm enc}", size=M_L, colors=CI),
                  (r"\oint_C", None), (r"d\ell", None), src={(r"(2\pi s)", 0): pl}, rt=1.8, wait=1.0)
        # 4 · corrente encerrada
        self.light(self.bar, 4)
        disk = Circle(radius=S * self.gs.get_value(), stroke_width=0).set_fill(VIOLET, 0.12).move_to(W([0, 0, 0])).set_z_index(1)
        self.play(FadeIn(disk), Indicate(sym, color=WHITE, scale_factor=1.4), run_time=1.0)
        self.caption("Corrente encerrada: só o fio atravessa o disco, $I_{\\rm enc}=I$")
        self.show(E(r"B\,(2\pi s)=\mu_0 I", "B", r"(2\pi s)", r"\mu_0", "I", size=M_L, colors=CI), (r"I_{\rm enc}", "I"), rt=1.6, wait=1.0)
        self.show(E(r"B=\frac{\mu_0 I}{2\pi s}", "B", r"\mu_0", "I", r"2\pi s", size=M_XL, colors=CI), (r"(2\pi s)", r"2\pi s"), rt=1.8, wait=0.3)
        bx = box(self.slots["H"]["eq"], MAG)
        self.play(FadeIn(bx), run_time=0.5)
        self.caption("Campo do fio retilíneo infinito: a integral inteira de Biot–Savart sai aqui em uma linha")
        self.mark("n17_fio_ampere")
        self.hold(3.5)
        self.out(bx, rt=0.3)

    # ── N18 · lâmina ────────────────────────────────────────────────────────────────────────────────────────
    def amp_lamina(self):
        self.section("amp_lamina")
        self.app_start("Lâmina infinita de corrente")
        self.reset_view(x=-3.8, y=-0.45, scale=1.0, beta=18, tau=-32)
        W = self.W
        XL, ZL = 2.6, 1.6
        sheet = self.cached(self.view_key, lambda: self.poly([[-XL, 0, -ZL], [XL, 0, -ZL], [XL, 0, ZL], [-XL, 0, ZL]], STEEL, 0.22, z=2).set_stroke(STEEL, 2, 0.8))
        xs = np.linspace(-XL + 0.35, XL - 0.35, 9)
        fl = self.flow([lambda u, x=x: self.W([x, 0, -ZL + 2 * ZL * u]) for x in xs], count=4, dash=0.2, width=5)
        Karr = self.cached(self.view_key, lambda: self.vec([-0.4, 0.0, -1.0], [0, 0, 1], GREEN, scale=2.0, width=9, tip=0.36))
        kl = self.pin(self.lab("K", [0, 0, 0], "K", size=M_L), lambda: W([-0.4, 0, 1.0]) + np.array([-0.45, -0.25, 0]))
        xax = VGroup(arrow(np.array([-6.5, -2.3, 0]), np.array([-5.7, -2.3, 0]), WHITE, 3, tip=0.14), E(r"\hat{\mathbf x}", size=M_S).move_to([-5.45, -2.3, 0]))
        self.play(FadeIn(sheet), FadeIn(xax), run_time=0.8)      # orientação fixa durante a rotação 3D → corte
        self.add(fl)
        self.play(Create(Karr), FadeIn(kl), run_time=1.0)
        self.caption("Lâmina plana infinita com corrente superficial $K$ (A/m: corrente por unidade de largura)")
        self.hold(1.5)
        self.light(self.bar, 0)
        self.caption("Simetria: deslizar ao longo da lâmina, em qualquer direção, não muda nada")
        self.play(self.beta.animate.set_value(-20), run_time=1.8)
        self.play(self.beta.animate.set_value(18), run_time=1.4)
        # corte 2D: daqui em diante a aplicação inteira acontece de frente
        self.caption("Gire para ver a lâmina de perfil: a corrente sai da tela")
        self.out(fl, Karr, kl, rt=0.4)        # a seta de K apontaria para fora da tela (comprimento zero) no corte: sai antes
        self.play(self.beta.animate.set_value(0), self.tau.animate.set_value(-3), run_time=2.2)   # a lâmina afina até virar uma linha
        self.out(sheet, rt=0.3)
        self.tau.set_value(0)
        line = Line(W([-XL - 0.6, 0, 0]), W([XL + 0.6, 0, 0]), color=STEEL, stroke_width=5).set_opacity(0.8).set_z_index(2)
        dots = VGroup(*[self.out_symbol(W([x, 0, 0]), 1, 0.13, GREEN) for x in np.linspace(-XL - 0.2, XL + 0.2, 15)])
        kl2 = self.lab("K", W([XL + 0.6, 0, 0]) + np.array([0.35, 0.3, 0]), "K", size=M_L)
        self.play(FadeIn(line), FadeIn(dots), FadeIn(kl2), run_time=0.8)
        self.light(self.bar, 1)
        bf = VGroup(*[arrow(W([x + 0.45, 1.65, 0]), W([x - 0.45, 1.65, 0]), MAG, 7, tip=0.28) for x in (-2.0, 1.7)],
                    *[arrow(W([x - 0.45, -1.65, 0]), W([x + 0.45, -1.65, 0]), MAG, 7, tip=0.28) for x in (-2.0, 1.7)])
        bL = self.lab(r"\mathbf B", W([-2.0, 1.65, 0]) + np.array([0, 0.4, 0]), r"\mathbf B", size=M_L)
        self.play(Create(bf), FadeIn(bL), run_time=1.0)
        self.caption("Direção: paralelo à lâmina e perpendicular a $K$; acima para a esquerda, abaixo para a direita")
        self.show(E(r"\mathbf B=\mp B\,\hat{\mathbf x}\quad(\text{acima}/\text{abaixo})", r"\mathbf B", size=M_L), rt=1.4, wait=1.0)
        self.mark("n18_lamina_direcao")
        # 2 · caminho
        self.light(self.bar, 2)
        x0, x1, y0, y1 = -0.75, 0.75, -1.15, 1.15
        rect = self.rect_path(x0, x1, y0, y1)
        Ll = self.lab("L", W([0, y1, 0]) + np.array([0, 0.32, 0]), "L", size=M_M, color=WHITE)
        self.play(Create(rect), FadeIn(Ll), run_time=1.4)
        self.caption("Caminho: retângulo que atravessa a lâmina; $L$ é a largura que ele cobre, em lados paralelos a ela")
        self.show(E(r"\oint\mathbf B\cdot d\boldsymbol\ell=\mu_0 I_{\rm enc}", r"\mathbf B\cdot d\boldsymbol\ell", r"\mu_0", r"I_{\rm enc}", size=M_L), rt=1.4, wait=0.8)
        # 3 · B·dℓ: lados curtos dão zero, longos dão BL cada
        self.light(self.bar, 3)
        zl = rich("$\\mathbf B\\perp d\\boldsymbol\\ell\\ \\Rightarrow\\ 0$", T_NOTE)
        zr = rich("$\\mathbf B\\perp d\\boldsymbol\\ell\\ \\Rightarrow\\ 0$", T_NOTE)
        zl.next_to(W([x0, 0.6, 0]), LEFT, buff=0.2)
        zr.next_to(W([x1, -0.6, 0]), RIGHT, buff=0.2)
        self.play(FadeIn(zl), FadeIn(zr), run_time=0.6)
        self.caption("Nos lados curtos $\\mathbf B$ é perpendicular ao caminho: não contribuem")
        self.hold(1.5)
        lt = rich("$BL$", T_NOTE).next_to(W([x0, y1, 0]), LEFT, buff=0.2)
        lb = rich("$BL$", T_NOTE).next_to(W([x0, y0, 0]), LEFT, buff=0.2)
        self.play(FadeIn(lt), FadeIn(lb), run_time=0.6)
        self.caption("Nos lados longos $\\mathbf B$ acompanha o sentido do percurso, acima e abaixo")
        self.show(E(r"\oint\mathbf B\cdot d\boldsymbol\ell=BL+BL=2BL", r"\mathbf B\cdot d\boldsymbol\ell", "BL", "2BL", size=M_L, colors={"BL": MAG, "2BL": MAG}),
                  src={("BL", 0): lt, ("BL", 1): lb}, rt=1.8, wait=1.0)
        # 4 · corrente encerrada: a faixa de largura L na própria lâmina
        self.light(self.bar, 4)
        strip = Line(W([x0, 0, 0]), W([x1, 0, 0]), color=GREEN, stroke_width=14).set_opacity(0.55).set_z_index(3)
        sL = self.lab("L", W([0, 0, 0]) + np.array([0, -0.45, 0]), "L", size=M_M, color=WHITE)
        self.play(Create(strip), FadeIn(sL), run_time=0.8)
        self.caption("A faixa de largura $L$ dentro do retângulo carrega $I_{\\rm enc}=KL$")
        self.show(E(r"I_{\rm enc}=KL", r"I_{\rm enc}", "K", "L", size=M_L), slot="A", src={("K", 0): kl2, ("L", 0): sL}, rt=1.4, wait=1.0)
        self.show(E(r"2B\,L=\mu_0 K\,L", "2B", r"\,L", r"\mu_0 K", size=M_L, colors=CI), ("2BL", "2B"), rt=1.8, wait=1.0)
        self.drop("A", keep_card=False)
        self.caption("$L$ aparece dos dois lados e cancela: o campo não depende da distância à lâmina")
        self.show(E(r"B=\frac{\mu_0 K}{2}", "B", r"\mu_0 K", size=M_XL, colors=CI), ("2B", "B"), (r"\,L", None), rt=1.8, wait=0.3)
        bx = box(self.slots["H"]["eq"], MAG)
        self.play(FadeIn(bx), run_time=0.5)
        self.mark("n18_lamina_resultado")
        self.hold(3.5)
        self.out(bx, xax, rt=0.3)

    # ── N19 · solenoide ─────────────────────────────────────────────────────────────────────────────────────
    def sol_shapes(self):
        """Hélice em torno do eixo x do mundo (eixo do solenoide), corrente no sentido +θ (y → z): B dentro em +x."""
        R, X0, X1 = self.SR, -2.9, 2.9
        H = lambda t: np.array([t, R * math.cos(TAU * self.SN * t), R * math.sin(TAU * self.SN * t)])
        return VGroup(self.path3d(H, X0, X1, np.array([0, 0, 0]), STEEL, 3.2, N=900),
                      self.curve([np.array([X0, R * math.cos(t), R * math.sin(t)]) for t in np.linspace(0, TAU, 40)], STEEL, 1.5, 0.4),
                      self.curve([np.array([X1, R * math.cos(t), R * math.sin(t)]) for t in np.linspace(0, TAU, 40)], STEEL, 1.5, 0.4))

    def amp_solenoide(self):
        self.section("amp_solenoide")
        self.app_start("Solenoide ideal: dois caminhos")
        self.SR, self.SN = 0.8, 2.2
        self.reset_view(x=-3.7, y=-0.45, scale=1.0, beta=28, tau=-18)
        W = self.W
        sol = self.cached(self.view_key, self.sol_shapes)
        hel = lambda u: self.W([-2.9 + 5.8 * u, self.SR * math.cos(TAU * self.SN * (-2.9 + 5.8 * u)), self.SR * math.sin(TAU * self.SN * (-2.9 + 5.8 * u))])
        fl = self.flow([hel], count=26, dash=0.2, width=5)
        self.play(Create(sol), run_time=2.0)
        self.add(fl)
        il = self.pin(self.lab("I", [0, 0, 0], "I", size=M_M), lambda: W([2.9, self.SR, 0]) + np.array([0.3, 0.3, 0]))
        self.play(FadeIn(il), run_time=0.4)
        self.caption("Geometria: um enrolamento longo, $n$ espiras por unidade de comprimento, corrente $I$")
        self.hold(1.5)
        self.light(self.bar, 0)
        self.light(self.bar, 1)
        self.caption("Simetria do solenoide infinito ideal: o campo é só axial e só depende de $s$")
        self.show(E(r"\mathbf B=B(s)\,\hat{\mathbf z}", r"\mathbf B", r"B(s)", r"\hat{\mathbf z}", size=M_XL, colors={r"\hat{\mathbf z}": MAG}), rt=1.6, wait=0.5)
        bx = box(self.slots["H"]["eq"], MAG)
        zax = arrow(W([-3.3, 0, 0]), W([3.5, 0, 0]), WHITE, 3, z=9, tip=0.24)               # eixo axial do solenoide (o $\hat z$ da equação)
        zlab = self.lab(r"\hat{\mathbf z}", W([3.5, 0, 0]) + np.array([0.3, 0.3, 0]), r"\hat{\mathbf z}", size=M_M)
        ztxt = txt("eixo axial", 20, DIM).move_to(W([3.5, 0, 0]) + np.array([0.3, -0.25, 0]))
        self.play(FadeIn(bx), Create(zax), FadeIn(zlab), FadeIn(ztxt), run_time=0.8)
        nb = txt("ainda nada sobre dentro ou fora", T_NOTE, DIM).next_to(self.slots["H"]["card"], DOWN, buff=0.1)
        self.play(FadeIn(nb), run_time=0.4)
        self.mark("n19_axial")
        self.hold(2.5)
        self.out(bx, nb, fl, il, zax, zlab, ztxt, rt=0.3)
        # corte lateral (2D): ⊙ em cima, ⊗ embaixo
        self.play(self.beta.animate.set_value(0), self.tau.animate.set_value(0), run_time=2.2)
        xs = np.arange(-2.9, 2.95, 1 / self.SN)
        top = VGroup(*[self.out_symbol(W([x, self.SR, 0]), 1, 0.11, GREEN) for x in xs])
        bot = VGroup(*[self.out_symbol(W([x, -self.SR, 0]), -1, 0.11, GREEN) for x in xs])
        axis = DashedLine(W([-3.1, 0, 0]), W([3.1, 0, 0]), color=WHITE, stroke_width=1.5, dash_length=0.08).set_opacity(0.4)
        self.play(FadeOut(sol), FadeIn(top), FadeIn(bot), FadeIn(axis), run_time=1.0)
        self.purge(sol)
        unk = VGroup(*[DashedLine(W([x - 0.3, y, 0]), W([x + 0.3, y, 0]), color=MAG, stroke_width=2.5, dash_length=0.06).set_opacity(0.6)
                       for x in (-1.9, 1.9) for y in (-1.7, -0.4, 0.4, 1.7)])
        self.play(FadeIn(unk), run_time=0.6)
        self.caption("Corte lateral: a corrente sai em cima e entra embaixo. $B(s)$ ainda é desconhecido, dentro e fora")
        self.hold(2.5)
        # ── caminho 1: totalmente fora (tracejado) ────────────────────────────────────────────────────────
        self.light(self.bar, 2)
        self.ya, self.yb = ValueTracker(1.25), ValueTracker(2.05)
        r1 = self.cached(lambda: (self.ya.get_value(), self.yb.get_value(), *self.view_key()),
                         lambda: self.rect_path(-0.9, 0.9, self.ya.get_value(), self.yb.get_value(), dashed=True))
        al = self.pin(self.lab("a", [0, 0, 0], "a", size=M_S, color=VIOLET), lambda: W([-0.9, self.ya.get_value(), 0]) + np.array([-0.3, 0, 0]))
        bl = self.pin(self.lab("b", [0, 0, 0], "b", size=M_S, color=VIOLET), lambda: W([-0.9, self.yb.get_value(), 0]) + np.array([-0.3, 0, 0]))
        c1 = txt("caminho 1 · todo fora", T_NOTE, VIOLET).move_to(W([0, -1.95, 0]))
        self.play(Create(r1), FadeIn(al), FadeIn(bl), FadeIn(c1), run_time=1.4)
        self.caption("Primeiro caminho: retângulo todo fora, com lados a distâncias $a$ e $b$ do eixo")
        self.hold(1.5)
        self.caption("Aqui $a$ e $b$ são essas distâncias, não os raios do toroide")
        self.hold(1.5)
        self.light(self.bar, 3)
        la = self.pin(self.lab(r"B(a)L", [0, 0, 0], r"B(a)", size=M_S, colors={"L": WHITE}), lambda: W([0, self.ya.get_value(), 0]) + np.array([0, -0.3, 0]))
        lb_ = self.pin(self.lab(r"-B(b)L", [0, 0, 0], r"B(b)", size=M_S), lambda: W([0, self.yb.get_value(), 0]) + np.array([0, 0.3, 0]))
        self.play(FadeIn(la), FadeIn(lb_), run_time=0.6)
        self.caption("Lados verticais: $\\mathbf B\\perp d\\boldsymbol\\ell$. Sobram os dois lados de comprimento $L$, em sentidos opostos")
        self.show(E(r"\oint\mathbf B\cdot d\boldsymbol\ell=B(a)L-B(b)L", r"\mathbf B\cdot d\boldsymbol\ell", r"B(a)", r"B(b)", size=M_L),
                  src={(r"B(a)", 0): la, (r"B(b)", 0): lb_}, rt=1.8, wait=1.2)
        self.light(self.bar, 4)
        self.caption("Sem corrente encerrada, Ampère compara os campos nos dois lados")
        self.show(E(r"B(a)L-B(b)L=0", r"B(a)", r"B(b)", "0", size=M_L), (r"\mathbf B\cdot d\boldsymbol\ell", None), rt=1.6, wait=1.0)
        self.show(E(r"B(a)=B(b)", r"B(a)", r"B(b)", size=M_XL), ("0", None), rt=1.6, wait=0.3)
        bx = box(self.slots["H"]["eq"], MAG)
        self.play(FadeIn(bx), FadeOut(la), FadeOut(lb_), run_time=0.4)
        self.purge(la, lb_)
        self.mark("n19_fora_constante")
        self.caption("Deslize o retângulo: fora, $B$ não depende da distância ao eixo")
        self.play(self.ya.animate.set_value(1.6), self.yb.animate.set_value(2.45), run_time=2.0)
        self.play(self.ya.animate.set_value(1.15), self.yb.animate.set_value(2.3), run_time=2.0)
        self.out(bx, rt=0.3)
        self.caption("Ampère deixa uma constante; longe do solenoide o campo dele vai a zero, e a constante é zero")
        self.show(E(r"B(s)\to0\quad(s\to\infty)", r"B(s)", size=M_L), slot="A", rt=1.4, wait=1.2)
        self.show(E(r"B_{\rm fora}=0", r"B_{\rm fora}", "0", size=M_XL, colors=CI), rt=1.6, wait=0.3)
        bx = box(self.slots["H"]["eq"], MAG)
        outs = VGroup(*[m for m in unk if abs(m.get_center()[1] - self.oy.get_value()) > 1.0])
        self.play(FadeIn(bx), FadeOut(outs), run_time=0.6)
        self.caption("$B_{\\rm fora}=0$ é resultado: veio de Ampère e da condição no infinito")
        self.mark("n19_fora_zero")
        self.hold(3.0)
        self.out(bx, r1, al, bl, c1, rt=0.6)
        self.drop("A", keep_card=False)
        # ── caminho 2: dentro + fora (contínuo) ───────────────────────────────────────────────────────────
        for m in self.bar.steps:
            m.set_opacity(0.35)
        self.light(self.bar, 2)
        self.yi = ValueTracker(0.35)
        x0, x1 = -0.9, 0.9
        r2 = self.cached(lambda: (self.yi.get_value(), *self.view_key()), lambda: self.rect_path(x0, x1, self.yi.get_value(), 1.45))
        c2 = txt("caminho 2 · dentro + fora", T_NOTE, VIOLET).move_to(W([0, -1.95, 0]))
        self.play(Create(r2), FadeIn(c2), run_time=1.4)
        Ll = self.lab("L", W([0, 1.45, 0]) + np.array([0, 0.3, 0]), "L", size=M_M, color=WHITE)
        self.play(FadeIn(Ll), run_time=0.4)
        self.caption("Segundo caminho: um lado dentro do solenoide, o outro fora")
        self.hold(1.2)
        self.light(self.bar, 3)
        self.caption("Fora, $B=0$; nos lados verticais, $\\mathbf B\\perp d\\boldsymbol\\ell$. Só o lado de dentro contribui")
        self.show(E(r"\oint\mathbf B\cdot d\boldsymbol\ell=B\,L", r"\mathbf B\cdot d\boldsymbol\ell", "B", r"\,L", size=M_L, colors=CI), rt=1.6, wait=1.0)
        self.light(self.bar, 4)
        inside = VGroup(*[d for d in top if x0 < d.get_center()[0] - self.ox.get_value() < x1])
        cnt = VGroup()
        for k, d in enumerate(inside):
            cnt.add(E(str(k + 1), size=M_S).set_color(GREEN).next_to(d, UP, buff=0.12))
        self.play(LaggedStart(*[AnimationGroup(Indicate(d, color=WHITE, scale_factor=1.7), FadeIn(c)) for d, c in zip(inside, cnt)], lag_ratio=0.4),
                  run_time=2.0)
        self.caption(f"Espiras atravessadas: $n$ por unidade de comprimento; em $L$ são $nL$ (aqui {len(inside)})")
        self.show(E(r"I_{\rm enc}=(nL)\,I", r"I_{\rm enc}", "(nL)", r"\,I", size=M_L, colors={r"(nL)": VIOLET, r"\,I": GREEN}), slot="A", rt=1.4, wait=1.0)
        self.show(E(r"B\,L=\mu_0\,(nL)\,I", "B", r"\,L", r"\mu_0", "(nL)", r"\,I", size=M_L, colors=CI),
                  src={(r"(nL)", 0): glyphs(self.slots["A"]["eq"], "(nL)", 0)}, rt=1.8, wait=1.0)
        self.drop("A", keep_card=False)
        self.out(cnt, rt=0.3)
        self.caption("$L$ cancela: dentro, o campo vale $\\mu_0 n I$")
        self.show(E(r"B_{\rm dentro}=\mu_0\,n\,I", r"B_{\rm dentro}", r"\mu_0", r"\,n", r"\,I", size=M_XL, colors=CI), ("B", r"B_{\rm dentro}"), (r"\,L", None),
                  ("(nL)", r"\,n"), rt=1.8, wait=0.3)
        bx = box(self.slots["H"]["eq"], MAG)
        self.play(FadeIn(bx), run_time=0.4)
        self.mark("n19_dentro")
        ins = VGroup(*[arrow(W([x - 0.4, y, 0]), W([x + 0.4, y, 0]), MAG, 6, tip=0.24) for x in (-2.2, -0.2, 1.8) for y in (-0.45, 0.0, 0.45)])
        self.play(FadeOut(unk), FadeIn(ins), run_time=0.8)
        self.purge(unk)
        self.caption("O lado de dentro pode deslizar sem mudar o resultado: dentro, o campo é uniforme")
        self.play(self.yi.animate.set_value(-0.55), run_time=2.2)
        self.play(self.yi.animate.set_value(0.35), run_time=1.6)
        self.out(bx, rt=0.3)
        q = txt("solenoide infinito ideal", T_NOTE, WHITE).next_to(self.slots["H"]["card"], DOWN, buff=0.1)
        self.play(FadeIn(q), run_time=0.5)
        self.hold(1.5)
        # contraste: solenoide real finito — palco próprio, linhas internas e de retorno conectadas
        self.out(r2, c2, Ll, top, bot, axis, ins, rt=0.6)
        C = np.array([-3.6, -0.6, 0])
        LS, RS_ = 1.7, 0.42
        coil = VGroup(*[Dot(C + [x, RS_, 0], radius=0.065, color=GREEN) for x in np.linspace(-LS, LS, 13)],
                      *[Dot(C + [x, -RS_, 0], radius=0.065, color=GREEN) for x in np.linspace(-LS, LS, 13)])
        loops = VGroup()
        for y0, H in ((0.15, 1.5), (0.32, 2.2)):
            for sgn in (1, -1):
                pts = [C + [-LS - 0.3, sgn * y0, 0], C + [0, sgn * y0, 0], C + [LS + 0.3, sgn * y0, 0], C + [LS + 1.1, sgn * (y0 + 0.35 * H), 0],
                       C + [LS + 0.6, sgn * (0.85 * H), 0], C + [0, sgn * H, 0], C + [-LS - 0.6, sgn * (0.85 * H), 0], C + [-LS - 1.1, sgn * (y0 + 0.35 * H), 0],
                       C + [-LS - 0.3, sgn * y0, 0]]
                m = VMobject(stroke_color=MAG, stroke_width=2.6).set_points_smoothly(pts).set_stroke(opacity=0.8)
                loops.add(m, self.arrowhead(C + [0, sgn * y0, 0], [1, 0, 0], 0.22, MAG), self.arrowhead(C + [0, sgn * H, 0], [-1, 0, 0], 0.22, MAG))
        tf = txt("solenoide real (finito) · esquema", T_NOTE, DIM).move_to(C + [0, 2.45, 0])
        self.play(FadeIn(coil), Create(loops), FadeIn(tf), run_time=1.8)
        self.caption("Solenoide real finito: o campo se espalha nas pontas e fora é pequeno, mas não exatamente zero")
        self.mark("n19_finito")
        self.hold(4.0)
        self.out(q, rt=0.3)

    # ── N20 · toroide ───────────────────────────────────────────────────────────────────────────────────────
    def tor_shapes(self):
        a, b, NW = self.TA, self.TB, self.TN
        Rc, rt = (a + b) / 2, (b - a) / 2
        g = VGroup()
        for k in range(NW):
            ph = TAU * k / NW
            s_hat = np.array([math.sin(ph), 0, math.cos(ph)])
            Cc = Rc * s_hat
            P = lambda psi, Cc=Cc, s_hat=s_hat: Cc + rt * (math.cos(psi) * s_hat + math.sin(psi) * np.array([0, 1, 0]))
            g.add(self.path3d(P, 0, TAU, Cc, STEEL, 2.4, N=36))
        for r in (a, b):
            g.add(self.curve([np.array([r * math.sin(t), 0, r * math.cos(t)]) for t in np.linspace(0, TAU, 80)], STEEL, 1.4, 0.35, z=1))
        return g

    def tor_paths(self):
        """Caminhos das espiras (uma a cada 3): corrente sobe pela face interna (s=a) e desce pela externa (ψ decrescente)."""
        a, b, NW = self.TA, self.TB, self.TN
        Rc, rt = (a + b) / 2, (b - a) / 2
        out = []
        for k in range(0, NW, 3):
            ph = TAU * k / NW
            s_hat = np.array([math.sin(ph), 0, math.cos(ph)])
            Cc = Rc * s_hat
            out.append(lambda u, Cc=Cc, s_hat=s_hat: self.W(Cc + rt * (math.cos(math.pi - TAU * u) * s_hat + math.sin(math.pi - TAU * u) * np.array([0, 1, 0]))))
        return out

    def tor_currents(self):
        """Setas de corrente SOBRE as espiras: na face interna (s=a) a corrente sobe (+y); na externa (s=b) desce."""
        a, b, NW = self.TA, self.TB, self.TN
        Rc, rt = (a + b) / 2, (b - a) / 2
        g = VGroup()
        for k in range(0, NW, 4):
            ph = TAU * k / NW
            s_hat = np.array([math.sin(ph), 0, math.cos(ph)])
            Cc = Rc * s_hat
            P = lambda psi: Cc + rt * (math.cos(psi) * s_hat + math.sin(psi) * np.array([0, 1, 0]))
            # face interna: ψ = π (tangente −ψ̂ = +y); face externa: ψ = 0 (tangente +ψ̂... no sentido da corrente: −y)
            g.add(arrow(self.W(P(math.pi + 0.35)), self.W(P(math.pi - 0.35)), GREEN, 5, z=9, tip=0.18),
                  arrow(self.W(P(0.35)), self.W(P(-0.35)), GREEN, 5, z=9, tip=0.18))
        return g

    def amp_toroide(self):
        self.section("amp_toroide")
        self.app_start("Toroide ideal")
        self.TA, self.TB, self.TN = 0.85, 1.95, 24
        a, b = self.TA, self.TB
        self.reset_view(x=-3.7, y=-0.5, scale=1.0, beta=0, tau=-38)
        W = self.W
        tor = self.cached(self.view_key, self.tor_shapes)
        self.play(Create(tor), run_time=2.2)
        cur = self.flow(self.tor_paths(), count=2, dash=0.2, width=6)       # corrente: traços verdes sobre as espiras
        self.add(cur)
        self.play(FadeIn(cur), run_time=0.6)
        self.caption("Geometria: $N$ espiras enroladas num anel. A corrente sobe pela face interna e desce pela externa")
        self.hold(2.0)
        self.light(self.bar, 0)
        self.play(self.beta.animate.set_value(60), run_time=2.2)
        self.play(self.beta.animate.set_value(0), run_time=1.6)
        self.light(self.bar, 1)
        self.caption("Simetria do toroide ideal: $\\mathbf B$ circula em torno do eixo, $\\mathbf B=B(s)\\,\\hat{\\boldsymbol\\phi}$")
        self.show(E(r"\mathbf B=B(s)\,\hat{\boldsymbol\phi}", r"\mathbf B", r"B(s)", r"\hat{\boldsymbol\phi}", size=M_L), rt=1.4, wait=1.0)
        # vista de cima (2D): enrolamento atenuado, correntes como ⊙/⊗, parâmetros na geometria
        self.out(cur, rt=0.5)
        self.play(self.tau.animate.set_value(-90), self.gs.animate.set_value(1.0), self.ox.animate.set_value(-3.9), self.oy.animate.set_value(-0.2), run_time=2.4)
        ins = VGroup(*[self.out_symbol(W(np.array([a * math.sin(t), 0, a * math.cos(t)])), 1, 0.09, GREEN) for t in np.linspace(0, TAU, self.TN, endpoint=False)])
        outs = VGroup(*[self.out_symbol(W(np.array([b * math.sin(t), 0, b * math.cos(t)])), -1, 0.09, GREEN) for t in np.linspace(0, TAU, self.TN, endpoint=False)])
        self.play(tor.animate.set_stroke(opacity=0.25), FadeIn(ins), FadeIn(outs), run_time=1.0)
        c0 = W([0, 0, 0])
        ra = Line(c0, c0 + a * np.array([-math.cos(0.6), -math.sin(0.6), 0]), color=WHITE, stroke_width=2).set_opacity(0.7)
        rb = Line(c0, c0 + b * np.array([-math.cos(1.0), -math.sin(1.0), 0]), color=WHITE, stroke_width=2).set_opacity(0.7)
        la = self.lab("a", ra.get_end() + np.array([-0.2, -0.15, 0]), "a", size=M_M, color=WHITE)
        lb = self.lab("b", rb.get_end() + np.array([-0.15, -0.25, 0]), "b", size=M_M, color=WHITE)
        self.play(Create(ra), Create(rb), FadeIn(la), FadeIn(lb), run_time=0.8)
        self.caption("Visto de cima: $N$ correntes saem da tela em $s=a$ e $N$ entram em $s=b$")
        self.hold(1.5)
        self.light(self.bar, 2)
        self.sr = ValueTracker(0.5)
        amp = self.cached(lambda: (self.sr.get_value(), *self.view_key()), lambda: VGroup(
            self.loop3d([0, 0, 0], self.sr.get_value(), [0, 1, 0], VIOLET, 4.5, arrows=3, dashed=True, tip=0.24, heads=True),
            Line(c0, c0 + self.sr.get_value() * self.gs.get_value() * np.array([math.cos(0.35), math.sin(0.35), 0]), color=VIOLET, stroke_width=2.5)))
        sl = self.pin(self.lab("s", [0, 0, 0], "s", size=M_M), lambda: c0 + 0.55 * self.sr.get_value() * np.array([math.cos(0.35), math.sin(0.35), 0]) + np.array([0, 0.25, 0]))
        self.play(Create(amp), FadeIn(sl), run_time=1.2)
        lhs = E(r"I_{\rm enc}=", r"I_{\rm enc}", size=M_L)
        v0, v1 = E("0", size=M_L), E(r"NI", "NI", size=M_L)
        reg = lambda: 0 if self.sr.get_value() < a else (1 if self.sr.get_value() < b else 2)
        g = VGroup(lhs, v0).arrange(RIGHT, buff=0.15)
        v1.move_to(v0, aligned_edge=LEFT)
        v0.add_updater(lambda m: m.set_opacity(0.0 if reg() == 1 else 1.0))
        v1.add_updater(lambda m: m.set_opacity(1.0 if reg() == 1 else 0.0))
        g.add(v1)
        self.card_group(g, "A")
        # região 1
        self.light(self.bar, 4)
        self.caption("Região $s<a$: o círculo não envolve nenhuma corrente")
        self.show(E(r"B\,(2\pi s)=0\ \Rightarrow\ B=0\quad(s<a)", "B", r"(2\pi s)", size=M_L, colors=CI), rt=1.4, wait=1.5)
        # região 2
        self.caption("Região $a<s<b$: o círculo envolve as $N$ correntes da face interna, todas no mesmo sentido")
        self.play(self.sr.animate.set_value((a + b) / 2), run_time=2.4)
        self.light(self.bar, 3)
        self.show(E(r"B\,(2\pi s)=\mu_0 NI", "B", r"(2\pi s)", r"\mu_0", "NI", size=M_L, colors=CI), rt=1.6, wait=1.0)
        self.show(E(r"B=\frac{\mu_0 NI}{2\pi s}\quad(a<s<b)", "B", r"\mu_0", "NI", r"2\pi s", size=M_L, colors=CI), (r"(2\pi s)", r"2\pi s"), rt=1.6, wait=1.5)
        bc = self.cached(self.view_key, lambda: VGroup(*[self.loop3d([0, 0, 0], r, [0, 1, 0], MAG, 2.6, arrows=4, tip=0.2, heads=True) for r in (1.15, 1.4, 1.65)]))
        self.play(FadeIn(bc), run_time=0.8)
        self.mark("n20_interior")
        # região 3
        self.caption("Região $s>b$: envolve $N$ correntes saindo e $N$ entrando — corrente líquida zero")
        self.play(self.sr.animate.set_value(2.3), run_time=2.4)
        self.show(E(r"B\,(2\pi s)=\mu_0(NI-NI)=0\ \Rightarrow\ B=0\quad(s>b)", "B", r"(2\pi s)", r"\mu_0", "NI", size=M_M, colors=CI), rt=1.6, wait=1.5)
        self.mark("n20_exterior")
        v0.clear_updaters()
        v1.clear_updaters()
        self.drop("A", keep_card=False)
        self.show(E(r"B(s)=\begin{cases}0,& s<a\\[2pt] \dfrac{\mu_0 NI}{2\pi s},& a<s<b\\[6pt] 0,& s>b\end{cases}", r"B(s)", "NI", size=M_M, colors=CI),
                  rt=1.8, wait=0.3)
        # gráfico sincronizado com o amperiano
        o = self.slots["A"]["pos"] + np.array([-2.6, -0.85, 0])
        kx, ky = 5.0 / 3.0, 1.2 / (1 / (TAU * a))
        Pg = lambda s, Bv: o + np.array([kx * s, ky * Bv, 0])
        Bt = lambda s: 1 / (TAU * s) if a < s < b else 0.0
        gr = VGroup(arrow(o, o + [5.3, 0, 0], WHITE, 2.5, tip=0.14), arrow(o, o + [0, 1.6, 0], WHITE, 2.5, tip=0.14),
                    Line(Pg(0, 0), Pg(a, 0), color=MAG, stroke_width=4.5),
                    VMobject(stroke_color=MAG, stroke_width=4.5).set_points_as_corners([Pg(s, 1 / (TAU * s)) for s in np.linspace(a, b, 40)]),
                    Line(Pg(b, 0), Pg(3.0, 0), color=MAG, stroke_width=4.5),
                    DashedLine(Pg(a, 0), Pg(a, 1 / (TAU * a)), color=MAG, stroke_width=2, dash_length=0.05).set_opacity(0.6),
                    DashedLine(Pg(b, 0), Pg(b, 1 / (TAU * b)), color=MAG, stroke_width=2, dash_length=0.05).set_opacity(0.6),
                    E("a", size=M_S).move_to(Pg(a, 0) + [0, -0.25, 0]), E("b", size=M_S).move_to(Pg(b, 0) + [0, -0.25, 0]),
                    E("s", size=M_S).move_to(o + [5.5, 0, 0]))
        off = np.zeros(3)
        gd = self.cached(lambda: self.sr.get_value(), lambda: Dot(Pg(self.sr.get_value(), Bt(self.sr.get_value())) + off, radius=0.08, color=WHITE).set_z_index(6))
        gr.add(E(r"B", "B", size=M_S, colors={"B": MAG}).move_to(o + [-0.3, 1.75, 0]))
        grp = VGroup(gr, gd)
        c_antes = grp.get_center()
        self.card_group(grp, "A")
        off[:] = grp.get_center() - c_antes      # o marcador usa o mesmo referencial do gráfico depois do layout
        self.caption("O mesmo amperiano percorre as três regiões: o gráfico acompanha")
        self.play(self.sr.animate.set_value(0.45), run_time=2.0)
        self.play(self.sr.animate.set_value(2.35), run_time=4.0, rate_func=linear)
        self.caption("Toroide ideal: o campo fica confinado dentro do enrolamento")
        self.mark("n20_toroide_resultado")
        self.hold(3.5)
