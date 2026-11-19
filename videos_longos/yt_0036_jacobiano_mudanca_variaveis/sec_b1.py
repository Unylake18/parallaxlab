"""yt_0036 · B1 · a régua esticada (alvo 04) e o fator numa curva (sem alvo). Layout A: palco à esquerda, coluna em x = 1120.
C1 inteira (o comprimento 2 da régua de x voa para dx = 2 dt; os limites 0 e 1 voam das pontas da régua de t); o Δt desce pelas linhas finas
e vira Δx. B1-2: γ(t), o arco Δs aceso em lima, a seta γ′(t) Δt tangente; Δt encolhe (um movimento) e a seta gruda no arco."""
from j36 import *

VT, VR = Vw(160, 360, 400), Vw(160, 640, 400)
VC = Vw(150, 900, 280)


def regua(v, a1, cor, nome, ticks, labs):
    lin = lin_px([v.px(0, 0), v.px(a1, 0)], cor, 5, z=5)
    tk = VGroup(*[lin_px([v.px(a, -.03), v.px(a, .03)], cor, 3, z=5) for a in ticks])
    nm = TC(nome, *v.px(a1 + .12, 0), 34, "c")
    ls = {a: TC(t, *v.px(a, -.12), 26, "c") for a, t in labs}
    return lin, tk, nm, ls


def gam(t):
    return (0.3 + t, 0.5 + 0.8 * math.sin(1.2 * t) + 0.3 * t)


def dgam(t):
    return (1.0, 0.96 * math.cos(1.2 * t) + 0.3)


class PB1(J36):
    CANTO = True

    def corpo(self):
        self.an("B1-1")
        self.secao("A RÉGUA ESTICADA")
        col = self.col = Coluna36(self, 1120, 186)
        # régua de x (0 a 2) já no começo: o palco não abre vazio
        rx, tkx, nmx, lx = regua(VR, 2, E1, r"\X", [0, .5, 1, 1.5, 2], [(0, r"\Am{0}"), (2, r"\Am{2}")])
        self.play(Create(rx), Create(tkx), run_time=0.8)
        self.pena(nmx, *lx.values(), lag=0.1)
        # C1 linha 1: ∫₀² x dx = [x²/2]₀² = 2²/2 − 0²/2 = 2
        self.gat("a integral de zero a dois")
        A = Lp([("i", r"\int_{\Am{0}}^{\Am{2}}"), ("f", r"\X\,\dX")], 1120, 0, 40)
        col.poe(A)
        A._xy = (1120, centro(A)[1])
        lo, hi = idx_lims(A, "i")
        self.escreve_voos(A, [(lx[0], lo), (lx[2], hi, (940, 520))])
        self.gat("a primitiva é")
        A = cresce(self, A, [("e1", "="), ("lb", r"\Big["), ("F", r"\dfrac{\X^2}{2}"), ("rb", r"\Big]"), ("sb", r"_{\Am{0}}^{\Am{2}}")],
                   voos=lambda B: [(VGroup(*[B_[0][k] for k in lo]).copy(), lims_sb(B, "sb")[0]) for B_ in [A]] +
                   [(VGroup(*[A[0][k] for k in hi]).copy(), lims_sb(B, "sb")[1])], col=col, nota="C1 colchete")
        self.gat("em dois quatro sobre dois")                           # final §4: a fala lê G(2) − G(0)
        A = cresce(self, A, [("e2", "="), ("d", r"\dfrac{2^2}{2}-\dfrac{0^2}{2}")], col=col, nota="C1 G(b) − G(a)")
        self.gat("em zero zero dá dois")
        A = cresce(self, A, [("e3", "="), ("r", "2")], col=col, nota="C1 número")
        L1 = A
        # régua de t e x = 2t
        self.gat("xis igual a dois tê")
        rt_, tkt, nmt, lt = regua(VT, 1, CU, r"\Uc{t}", [0, .5, 1], [(0, r"\Uc{0}"), (1, r"\Uc{1}")])
        self.play(Create(rt_), Create(tkt), run_time=0.8)
        self.pena(nmt, *lt.values(), lag=0.1)
        L2 = Lp([("x", r"\X=2\Uc{t}")], 1120, 0, 40)
        col.poe(L2)
        L2._xy = (1120, centro(L2)[1])
        self.pena(L2)
        self.gat("quando tê vai de")
        L2b = Lp([("a", r"\X=\Am{0}\ \Rightarrow\ \Uc{t}="), ("t0", r"\Uc{0}"), ("b", r"\qquad\X=\Am{2}\ \Rightarrow\ \Uc{t}="), ("t1", r"\Uc{1}")], 1120, 0, 40)
        col.poe(L2b)
        self.escreve_voos(L2b, [(lt[0], "t0"), (lt[1], "t1")])
        self.gat("vira dois dê tê")
        L2 = cresce(self, L2, [("i", r"\ \Rightarrow\ "), ("dx", r"\dX=\Lm{2}\,\Uc{dt}")], voos=lambda B: [(lx[2].copy(), [B._ix["dx"][3]], (1060, centro(L2)[1] + 20))],
                    col=col, nota="C1 dx = 2 dt (o 2 voa da régua, por fora da linha dos limites)")
        # o pedacinho Δt desce e vira Δx, duas vezes maior
        self.gat("duas vezes maior")
        a0, a1 = VT.px(.55, 0), VT.px(.65, 0)
        b0, b1 = VR.px(1.1, 0), VR.px(1.3, 0)
        st = lin_px([a0, a1], LIMA, 10, z=7)
        ldt = TC(r"\Uc{\Delta t}", (a0[0] + a1[0]) / 2, a0[1] - 36, 28, "c")
        self.play(Create(st), run_time=0.4)
        self.pena(ldt)
        d1 = lin_px([(a0[0], a0[1] + 12), (b0[0], b0[1] - 12)], GEO, 2, dash=(6, 8), z=3)
        d2 = lin_px([(a1[0], a1[1] + 12), (b1[0], b1[1] - 12)], GEO, 2, dash=(6, 8), z=3)
        sx = lin_px([b0, b1], LIMA, 10, z=7)
        self.play(Create(d1), Create(d2), TransformFromCopy(st, sx, path_arc=0), run_time=1.4)
        self.gat("esse dois é o fator")
        ldx = TC(r"\Am{\Delta x}=\Lm{2}\,\Uc{\Delta t}", (b0[0] + b1[0]) / 2, b0[1] + 54, 30, "c")
        self.pena(ldx)
        ltx = TP(r"\Uc{t}=\dfrac{\X}{2}", 300, 500, 30, "c")
        self.pena(ltx)
        # C1 linha 3: ∫₀² x dx = ∫₀¹ (2t)·2 dt = 4 ∫₀¹ t dt = 4 [t²/2]₀¹ = 4·(1/2 − 0) = 2 ✓
        self.gat("e a conta confirma")
        P3 = [("I0", r"\int_{\Am{0}}^{\Am{2}}"), ("x0", r"\X\,\dX"), ("e1", "="), ("I1", r"\int_{\Uc{0}}^{\Uc{1}}"), ("g", r"(2\Uc{t})"),
              ("c2", r"\cdot\Lm{2}\,\Uc{dt}")]
        L3 = Lp(P3, 1120, 0, 40)
        col.poe(L3)
        L3._xy = (1120, centro(L3)[1])
        l3lo, l3hi = idx_lims(L3, "I1")
        ig = L2._ix["x"]
        idx_ = L2._ix["dx"]
        self.escreve_voos(L3, [(VGroup(*[L1[0][k] for k in L1._ix["i"] + L1._ix["f"]]), ["I0", "x0"]), (lt[0], l3lo), (lt[1], l3hi),
                               (VGroup(*[L2[0][k] for k in ig[2:]]), [L3._ix["g"][1], L3._ix["g"][2]]),
                               (VGroup(*[L2[0][k] for k in idx_[3:]]), [L3._ix["c2"][k] for k in (1, 2, 3)])])
        # v2 Q02: a linha 3 vira três linhas alinhadas no =; cada uma nasce da de cima por glyph map (os dois 2 acendem e viram o 4)
        self.gat("é quatro vezes a")
        g_, c_ = L3._ix["g"], L3._ix["c2"]
        acende(self, (VGroup(L3[0][g_[1]]), LIMA), (VGroup(L3[0][c_[1]]), LIMA), rt=0.5)
        xe = eq_x(L3, "e1")
        L3b = deriva(self, L3, [("e2", "="), ("q4", "4"), ("I2", r"\int_{\Uc{0}}^{\Uc{1}}"), ("td", r"\Uc{t}\,\Uc{dt}")],
                     lambda B: [("e1", "e2"), ([g_[1], c_[1]], "q4"), ("I1", "I2"), ([g_[2]], [B._ix["td"][0]]), ([c_[2], c_[3]], B._ix["td"][1:])],
                     col, x=xe,
                     nota="C1 4∫t dt (os dois 2 viram 4)")
        self.gat("que é um meio")
        i2lo, i2hi = idx_lims(L3b, "I2")
        PC = [("e3", "="), ("q4", "4"), ("lb", r"\Big["), ("F", r"\dfrac{\Uc{t}^2}{2}"), ("rb", r"\Big]"), ("sb", r"_{\Uc{0}}^{\Uc{1}}")]
        L3c = deriva(self, L3b, PC, lambda B: [("e2", "e3"), ("q4", "q4"), (i2lo, lims_sb(B, "sb")[0]), (i2hi, lims_sb(B, "sb")[1]),
                                               ([L3b._ix["td"][0]], [B._ix["F"][0]])], col, x=xe,
                     nota="C1 4[t²/2]₀¹ (o t e os limites descem)")
        self.gat("quatro vezes um meio")
        L3c = cresce(self, L3c, [("e4", "="), ("m", r"4\cdot\left(\dfrac{1}{2}-0\right)")], col=col, nota="C1 G(1) − G(0)")
        L3c = cresce(self, L3c, [("e5", "="), ("r", "2")], col=col, nota="C1 = 2")
        self.gat("o mesmo valor")
        ck = check_px(dir_(L3c) + 34, centro(L3c)[1], MEN)
        self.play(Create(ck), run_time=0.5)
        # C1 linha 4: x = g(t) ⇒ Δx ≅ g′(t) Δt e o fator de comprimento |g′(t)|
        self.gat("xis igual a gê")
        L4 = Lp([("a", r"\X=g(\Uc{t})"), ("i", r"\ \Rightarrow\ "), ("b", r"\Am{\Delta x}\cong\Lm{g'(\Uc{t})}\,\Uc{\Delta t}")], 1120, 0, 40)
        col.poe(L4, gap=26)
        self.pena(L4)
        self.gat("gê linha de tê")
        bb = L4._ix["b"]
        acende(self, (VGroup(*[L4[0][k] for k in bb[3:8]]), LIMA), rt=1.0)
        self.gat("esse delta xis tem")
        lg = mixl([("t", "FATOR DE COMPRIMENTO:", LIMA), ("m", r"\Lm{|g'(\Uc{t})|}")], 1120, 0, 40)
        col.poe(lg)
        self.pena(lg)
        self.gat("o módulo de gê")
        mm = lg.p[1]
        acende(self, (VGroup(mm[0][0], mm[0][-1]), LIMA), rt=1.2)
        self.marca("04")

        # ════ B1-2 · o fator numa curva ════
        self.an("B1-2")
        self.limpa_tudo()
        self.secao("O FATOR NUMA CURVA")
        self.fundo(VC)                      # v2 §1: um gráfico → a grade dele na tela inteira
        d = plano(self, VC, (0, 3.2, 0, 2.45), 3.25, 2.5)
        col = self.col = Coluna36(self, 1120, 300)
        self.gat("um ponto andando")
        ts = np.linspace(0, 2.6, 120)
        cur = lin_px([VC.px(*gam(t)) for t in ts], BR, 4, z=5)
        pt = ponto_px(*VC.px(*gam(0)), BR, 8)
        self.play(Create(cur), MoveAlongPath(pt, VMobject().set_points_as_corners([VC.P(*gam(t)) for t in ts])), run_time=2.2)
        t0 = .75
        dt = ValueTracker(.6)
        p0 = ponto_px(*VC.px(*gam(t0)), BR, 8)
        self.play(pt.animate.move_to(VC.P(*gam(t0))), run_time=0.8)
        self.remove(pt)
        self.add(p0)
        lg0 = TP(r"\gamma(\Uc{t})", VC.px(*gam(t0))[0] - 20, VC.px(*gam(t0))[1] - 30, 28, "r")
        self.pena(lg0)
        self.gat("ele percorre um arco")

        def arco():
            tt = np.linspace(t0, t0 + dt.get_value(), 30)
            return lin_px([VC.px(*gam(t)) for t in tt], LIMA, 7, z=6)

        def fim_pt():
            return ponto_px(*VC.px(*gam(t0 + dt.get_value())), BR, 7)

        arc = arco()
        pf = fim_pt()
        self.play(Create(arc), FadeIn(pf), run_time=0.8)
        q = VC.px(*gam(t0 + dt.get_value()))
        lg1 = TP(r"\gamma(\Uc{t}+\Uc{\Delta t})", q[0] + 24, q[1] + 34, 28, "l")
        mid = VC.px(*gam(t0 + dt.get_value() / 2))
        lds = TP(r"\Lm{\Delta s}", mid[0] + 26, mid[1] + 40, 30, "l")
        self.pena(lg1, lds, lag=0.2)
        self.gat("o vetor velocidade")

        def seta_g():
            A_ = VC.px(*gam(t0))
            g1 = dgam(t0)
            B_ = VC.px(gam(t0)[0] + g1[0] * dt.get_value(), gam(t0)[1] + g1[1] * dt.get_value())
            return seta_px(A_, B_, BR, 4, 18, z=7)

        sg = seta_g()
        self.play(GrowFromPoint(sg, VC.P(*gam(t0))), run_time=0.9)
        tip = pxof(sg[1].get_center())
        lsg = TP(r"\gamma'(\Uc{t})\,\Uc{\Delta t}", tip[0] - 20, tip[1] - 38, 28, "r")
        self.pena(lsg)
        self.gat("a norma de gama")
        F1 = Lp([("ds", r"\Lm{\Delta s}"), ("c", r"\cong"), ("n", r"\|\gamma'(\Uc{t})\|"), ("dt", r"\,\Uc{\Delta t}")], 1120, 0, 44)
        col.poe(F1)
        self.escreve_voos(F1, [(lds.f, "ds", (800, 560))])
        acende(self, (gl(F1, "n"), BR), rt=0.8)
        self.gat("quanto menor o")
        self.remove(arc, pf, sg)
        arc_d, pf_d, sg_d = always_redraw(arco), always_redraw(fim_pt), always_redraw(seta_g)
        self.add(arc_d, pf_d, sg_d)
        self.play(FadeOut(lsg), FadeOut(lg1), FadeOut(lds), run_time=0.4)
        self.remove(lsg, lg1, lds)
        self.play(dt.animate.set_value(.16), run_time=3.5)
        for m in (arc_d, pf_d, sg_d):
            m.clear_updaters()
        self.gat("qual é o fator de área")
        cd = mixl([("t", "NO PLANO:", GEO), ("t", "FATOR DE ÁREA ="), ("m", r"\Al{?}")], 1120, 0, 40)
        col.poe(cd, gap=60)
        self.pena(cd)
        self.marca("B1-2")
        self.sai_fim()
