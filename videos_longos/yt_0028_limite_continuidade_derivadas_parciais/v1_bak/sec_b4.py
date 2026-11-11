"""Lote PB4 · DERIVADA PARCIAL (alvos 06, 07 e 08). B4-1/B4-2 (layout B, em x, âmbar): reta horizontal tracejada por P, P + h; à direita F(P), F(P + h),
a corda e o quociente ΔF/h (h = 1 → 0,5 → 0,2 → 0,1, um número por degrau); a curva da ponta (s ∈ [−0,75; 1]) e a tangente; o quociente termina sobre
a tangente: ∂F/∂x = (1, 2). B4-3 (em y, magenta): F(P) vira fantasma GEO; a curva é o círculo; ∂F/∂y = (−1, 0). B4-4 (layout A): as duas setas voam
para o P do palco; a coluna em cinco linhas na caneta (x = 1090)."""
from v28 import *  # noqa: F401,F403
from sec_b1 import nomes_b

VE = Vista(480, 540, 140)
VDX, VDY = Vista(1270, 650, 140), Vista(1300, 660, 140)
V = Vista(600, 540, 120)
NUMS_X = [r"\h=1:\ (0{,}84;\ 2{,}14)", r"\h=0{,}5:\ (0{,}96;\ 2{,}16)", r"\h=0{,}1:\ (1{,}00;\ 2{,}05)", r"\to\ (1,\ 2)"]
NUMS_Y = [r"\k=1:\ (-0{,}84;\ 0{,}46)", r"\k=0{,}5:\ (-0{,}96;\ 0{,}25)", r"\k=0{,}1:\ (-1{,}00;\ 0{,}05)", r"\to\ (-1,\ 0)"]


class Parcial:
    """Estado do B4-1/B4-2: direção H (x) ou vertical, passo h (ValueTracker); objetos com updater (sem MathTex redesenhado)."""

    def __init__(self, cena, H):
        self.c, self.H = cena, H
        self.cor = E1 if H else E2
        self.VD = VDX if H else VDY
        self.h = ValueTracker(1.0)
        self.A = np.array(F_AULA(0, 0), float)

    def Q(self):
        h = self.h.get_value()
        return (h, 0.0) if self.H else (0.0, h)

    def B(self):
        return np.array(F_AULA(*self.Q()), float)

    def q(self):
        h = self.h.get_value()
        return (self.B() - self.A) / h

    def objs(self):
        c, VD, A = self.cor, self.VD, self.A
        self.pQ = ponto7(VE.c2p(*self.Q()), POS, 7, 10)
        self.pQ.add_updater(lambda m: m.move_to(VE.c2p(*self.Q())))
        self.sB = seta7(VD.c2p(0, 0), VD.c2p(*self.B()), CAMPO, 5, 20).set_z_index(8)
        self.sB.add_updater(lambda m: m.become(seta7(VD.c2p(0, 0), VD.c2p(*self.B()), CAMPO, 5, 20).set_z_index(8)))
        self.corda = vlinha(VD, [A, self.B()], c, 4).set_z_index(9)
        self.corda.add_updater(lambda m: m.set_points_as_corners([VD.c2p(*A), VD.c2p(*self.B())]))
        self.sq = seta7(VD.c2p(*A), VD.c2p(*(A + self.q())), c, 8, 26).set_z_index(10)
        self.sq.add_updater(lambda m: m.become(seta7(VD.c2p(*A), VD.c2p(*(A + self.q())), c, 8, 26).set_z_index(10)))
        lh = TP(r"\h" if self.H else r"\k", *canto_xy(VE, *self.pos_lh()), 32)
        self.lh = segue(lh, lambda: canto_xy(VE, *self.pos_lh()))
        self.lq = segue(TP(r"\dfrac{\Delta\F}{\h}" if self.H else r"\dfrac{\Delta\F}{\k}", *canto_xy(VD, *self.pos_lq()), 34), lambda: canto_xy(VD, *self.pos_lq()))

    def pos_lh(self):
        h = self.h.get_value()
        return (h / 2, .28) if self.H else (-.28, h / 2)

    def pos_lq(self):
        t = self.A + self.q()
        return (t[0] + .5, t[1] - .15) if self.H else (t[0] - .05, t[1] + .55)

    def clareira_esq(self):
        if self.H:
            fix = clar28([(-2.4, -.1, 2.4, .1), (-.5, -.55, 0, -.1)], [(0, 0, .2)])
        else:
            fix = clar28([(-.1, -1.9, .1, 1.9), (.1, -.5, .6, -.1)], [(0, 0, .2)])
        return lambda: ou(fix, clar28([], [(*self.Q(), .2)]), clar28([(lambda a, b: (a - .25, b - .2, a + .25, b + .2))(*self.pos_lh())]))

    def curva(self):
        ss = np.linspace(-.75, 1, 200) if self.H else np.linspace(-1.25, 1.6, 200)
        a = F_AULA(ss, 0 * ss) if self.H else F_AULA(0 * ss, ss)
        return vlinha(self.VD, list(zip(a[0], a[1])), self.cor, 2.5).set_z_index(6)

    def tangente(self):
        tg = np.array([1.0, 2.0]) if self.H else np.array([-1.0, 0.0])
        return vlinha(self.VD, [self.A - tg * .45, self.A + tg * 1.1], GEO, 2, alpha=.6, dash=(6, 8)).set_z_index(5)

    def passo(self, h, rt=1.0):
        return self.h.animate(run_time=rt).set_value(h)


class LoteB4(Base):
    ANTES = "CONTINUIDADE"

    def nums(self, partes, cena_nums):
        return linha_partes(partes, 960, 955, 38, gap=40)

    def corpo(self):
        # ── B4-1 · em x ──
        self.an("B4-1")
        self.secao("DERIVADA PARCIAL")
        pE, pD = painel(130, 260, 700, 560), painel(1090, 260, 700, 560)
        nm = nomes_b()
        X = Parcial(self, True)
        cmp = campo28(VE, F_AULA, -2.25, 2.25, -1.75, 1.75, .5, rmin=0, mmax=3.5, ctx=True, nome="B4 campo da aula (contexto)")
        st = {"t": lambda: clar28([], [(0, 0, .2)])}
        clareira(cmp, lambda: st["t"]())
        P = ponto7(VE.c2p(0, 0), POS, 9)
        lP = TP(r"\Pt", *canto_xy(VE, -.25, -.32), 34)
        org = ponto7(VDX.c2p(0, 0), GEO, 6)
        sA = seta7(VDX.c2p(0, 0), VDX.c2p(*X.A), CAMPO2, 7, 24).set_z_index(9)
        lA = TP(r"\F(\Pt)", *canto_xy(VDX, .5, -.3), 30)
        self.play(Create(pE), Create(pD), cresce_campo(cmp, 1.0), FadeIn(P), FadeIn(lP), FadeIn(org), GrowArrow(sA), FadeIn(lA), FadeIn(nm), run_time=1.0)
        lin = vlinha(VE, [(-2.3, 0), (2.3, 0)], E1, 3, dash=(10, 9))
        X.objs()
        self.gat("anda só na horizontal")
        st["t"] = X.clareira_esq()
        self.play(Create(lin), FadeIn(X.pQ, scale=0.5), FadeIn(X.lh), GrowArrow(X.sB), run_time=0.9)
        self.gat("a diferença entre as duas é um vetor")
        self.play(Create(X.corda), run_time=0.7)
        self.gat("divide esse vetor")
        self.play(GrowArrow(X.sq), FadeIn(X.lq), run_time=0.8)
        self.ate(0.97)

        # ── B4-2 · os números; a curva; a tangente ──
        self.an("B4-2")
        nx = self.nums(NUMS_X, None)
        self.gat("com passo um")
        self.play(caneta(nx[0], ritmo=0.4))
        self.gat("com meio")
        self.play(X.passo(.5, 0.8), caneta(nx[1], ritmo=0.4))
        self.gat("com passo cada vez menor")
        self.play(X.passo(.2, 0.6), run_time=0.6)
        self.play(X.passo(.1, 0.6), caneta(nx[2], ritmo=0.4))
        print(f"[quociente] x: h = 0,1 → ({X.q()[0]:.3f}; {X.q()[1]:.3f})")
        self.gat("ele vai chegando em um e dois")
        self.play(caneta(nx[3], ritmo=0.5))
        cx, tx = X.curva(), X.tangente()
        self.gat("desenha uma curva")
        self.play(Create(cx), run_time=1.6)
        self.play(Create(tx), run_time=0.6)
        self.gat("é exatamente a seta tangente")
        self.play(X.passo(1e-4), FadeOut(X.pQ), FadeOut(X.lh), run_time=1.2)
        X.lq.clear_updaters()
        print(f"[quociente] x: limite → ({X.q()[0]:.4f}; {X.q()[1]:.4f}) (∂F/∂x = (1, 2))")
        dX = TP(r"\dfrac{\partial\F}{\dx}", *canto_xy(VDX, *X.pos_lq()), 34)
        self.play(FadeOut(X.lq), FadeIn(dX), run_time=0.6)
        self.ate(0.97)

        # ── B4-3 · em y ──
        self.an("B4-3")
        for m in (X.sB, X.corda, X.sq):
            m.clear_updaters()
        derx = X.sq                                       # a seta ∂F/∂x fica guardada (volta no B4-4)
        sai = [lin, X.sB, X.corda, X.sq, X.pQ, X.lh, dX, cx, tx, org, sA, lA, *nx]
        Y = Parcial(self, False)
        orgY = ponto7(VDY.c2p(0, 0), GEO, 6)
        fant = seta7(VDY.c2p(0, 0), VDY.c2p(*Y.A), GEO, 3, 16).set_z_index(7)
        lAY = TP(r"\F(\Pt)", *canto_xy(VDY, .5, -.3), 30)
        linY = vlinha(VE, [(0, -1.9), (0, 1.9)], E2, 3, dash=(10, 9))
        Y.objs()
        lP2 = TP(r"\Pt", *canto_xy(VE, .35, -.28), 34)
        self.gat("agora na vertical")
        st["t"] = Y.clareira_esq()
        self.play(*[FadeOut(m) for m in sai], FadeOut(lP), run_time=0.5)
        self.remove(*sai, lP)
        self.play(FadeIn(orgY), FadeIn(fant), FadeIn(lAY), FadeIn(lP2), Create(linY), FadeIn(Y.pQ, scale=0.5), FadeIn(Y.lh), GrowArrow(Y.sB), run_time=0.8)
        self.play(Create(Y.corda), GrowArrow(Y.sq), FadeIn(Y.lq), run_time=0.8)
        cy, ty = Y.curva(), Y.tangente()
        self.gat("anda num círculo")
        self.play(Create(cy), run_time=1.6)
        ny = self.nums(NUMS_Y, None)
        self.gat("e o quociente vai chegando")
        self.play(caneta(ny[0], ritmo=0.3))
        self.play(Y.passo(.5, 0.6), caneta(ny[1], ritmo=0.3))
        self.play(Y.passo(.2, 0.5), run_time=0.5)
        self.play(Y.passo(.1, 0.5), caneta(ny[2], ritmo=0.3))
        print(f"[quociente] y: k = 0,1 → ({Y.q()[0]:.3f}; {Y.q()[1]:.3f})")
        self.play(caneta(ny[3], ritmo=0.4))
        self.gat("tangente ao círculo")
        self.play(Create(ty), Y.passo(1e-4), FadeOut(Y.pQ), FadeOut(Y.lh), run_time=1.2)
        Y.lq.clear_updaters()
        print(f"[quociente] y: limite → ({Y.q()[0]:.4f}; {Y.q()[1]:.4f}) (∂F/∂y = (−1, 0))")
        dY = TP(r"\dfrac{\partial\F}{\dy}", *canto_xy(VDY, *Y.pos_lq()), 34)
        self.play(FadeOut(Y.lq), FadeIn(dY), run_time=0.6)
        self.ate(0.97)

        # ── B4-4 · as duas setas voam para o palco; a coluna ──
        self.an("B4-4")
        for m in (Y.sB, Y.corda, Y.sq):
            m.clear_updaters()
        dery = Y.sq
        self.add(derx)
        derx.set_opacity(0)
        resto = [m for m in self.snap() if m not in (derx, dery)]
        cmp.clear_updaters()
        self.play(*[FadeOut(m) for m in resto], derx.animate.set_opacity(1), run_time=0.6)
        self.remove(*resto)
        cmp2 = campo28(V, F_AULA, rmin=0, mmax=3.5, ctx=True, nome="B4-4 palco (contexto)",
                       skip=ou(clarSeg([((0, 0), (1, 2)), ((0, 0), (-1, 0))], .3), clar28([], [(0, 0, .05)]), clar28([(1.05, 1.6, 2.55, 2.45), (-2.65, .2, -1.15, .8)])))
        Pp = ponto7(V.c2p(0, 0), POS, 10)
        ax = seta7(V.c2p(0, 0), V.c2p(1, 2), E1, 8, 28).set_z_index(10)
        ay = seta7(V.c2p(0, 0), V.c2p(-1, 0), E2, 8, 28).set_z_index(10)
        self.gat("então a derivada parcial de um campo")
        self.play(cresce_campo(cmp2, 0.9), FadeIn(Pp), Transform(derx, ax), Transform(dery, ay), run_time=1.4)
        ldx = TP(r"\dfrac{\partial\F}{\dx}=(1,\,2)", *canto_xy(V, 1.8, 2.1), 36)
        ldy = TP(r"\dfrac{\partial\F}{\dy}=(-1,\,0)", *canto_xy(V, -1.9, .5), 36)
        lPp = TP(r"\Pt", *canto_xy(V, .3, -.35), 34)
        self.play(FadeIn(ldx), FadeIn(ldy), FadeIn(lPp), run_time=0.6)
        l1 = TC(r"\dfrac{\partial \F}{\dx}(\xo,\yo)=\lim\limits_{\h\to0}\dfrac{\F(\xo+\h,\,\yo)-\F(\xo,\,\yo)}{\h}", 1090, 290, 36)
        self.gat("é um vetor")
        self.play(caneta(l1, ritmo=0.45))
        l2 = TC(r"\dfrac{\partial \F}{\dx}=\left(\dfrac{\partial \Pp}{\dx},\ \dfrac{\partial \Qq}{\dx}\right)", 1090, 450, 40)
        self.gat("a conta é por componentes")
        self.play(caneta(l2, ritmo=0.6))
        lc = TC(r"\F = (1+\sen\X-\sen\Y,\ \ 2\sen\X+2-\cos\X-\cos\Y)", 1090, 880, 30)
        npt = legenda("NO PONTO (0, 0)", 1094, 940, GEO)
        self.gat("derivada da componente vertical")
        self.play(caneta(lc, ritmo=0.35))
        l3a = TC(r"=(\cos\X,\ 2\cos\X+\sen\X)", 1150, 545, 38)
        l3 = TC(r"=(\cos\X,\ 2\cos\X+\sen\X)=\Am{(1,\ 2)}", 1150, 545, 38)
        self.gat("dá cosseno")
        self.play(caneta(l3a, ritmo=0.5))
        self.gat("no ponto um e dois")
        n = len(l3a[0])
        self.play(tbgm(l3a, l3, *[([k], [k]) for k in range(n)], rt=1.0), FadeIn(npt, shift=0.05 * UP), run_time=1.0)
        limpa_soltos(self)
        l4 = TC(r"\dfrac{\partial \F}{\dy}=\left(\dfrac{\partial \Pp}{\dy},\ \dfrac{\partial \Qq}{\dy}\right)", 1090, 665, 40)
        self.gat("a derivada na direção vertical dá")
        self.play(caneta(l4, ritmo=0.5))
        l5a = TC(r"=(-\cos\Y,\ \sen\Y)", 1150, 760, 38)
        l5 = TC(r"=(-\cos\Y,\ \sen\Y)=\Mg{(-1,\ 0)}", 1150, 760, 38)
        self.play(caneta(l5a, ritmo=0.5))
        self.gat("no ponto menos um e zero")
        n = len(l5a[0])
        self.play(tbgm(l5a, l5, *[([k], [k]) for k in range(n)], rt=1.0), run_time=1.0)
        limpa_soltos(self)
        self.ate(0.97)
        self.sai_fim()
