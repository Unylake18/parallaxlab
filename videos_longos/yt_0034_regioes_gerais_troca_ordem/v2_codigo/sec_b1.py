"""yt_0034 · B1 · a fatia na curva (alvo 04), por que o Fubini vale (alvo 05) e a área π (alvo 06). Glyph maps 2 e 3.
Nota (handoff §5 B1-2 × narração): "nada de especial do disco" transforma o disco na região genérica (prévia do enunciado); como a narração
volta ao quarto de disco no B1-3, a região genérica volta ao disco (um movimento) no início do B1-3."""
from pecas34 import *
from sec_h import quarto_disco

CHF = Vw(360, 760, 240)          # v2: o quarto de disco sobe 20 px para caber R = [0, 2] × [−½, 2]
PQ2 = Vw(330, 600, 170)          # v2: palco pequeno do B1-2 a 170 px/unidade


def g_f(Y):
    return 1.5 + .35 * math.sin(2.2 * Y)


def regiao_gen(v):
    a, b = .3, 1.85
    return regiao(v, cX(c_b21, a, b) + cX(d_b21, a, b)[::-1])


class PB1(B34):
    ANTES = "A FATIA NA CURVA"

    def corpo(self):
        # ── B1-1 · a fatia que termina na curva (alvo v2_03): R = [0, 2] × [−½, 2] ──
        self.an("B1-1")
        V = CHF
        Q = quarto_disco(self, arco_cor=CORAL, v=V)
        g = papel_v(V, (0, 2.2, -.5, 2.2))
        self.grade = g
        sx, sy, lx, ly = eixos_v(V, 2.35, 2.35, b0=-.62)
        t2y = tick(V, "y", 2, r"\Mg{2}")
        tmy = tick(V, "y", -.5, r"\Mg{-\dfrac{1}{2}}", 26)
        self.play(FadeIn(g), FadeIn(Q["reg"]), GrowFromPoint(sx, V.P(0, 0)), GrowFromPoint(sy, V.P(0, 0)), run_time=0.7)
        self.pena(lx, ly)
        self.play(Create(t2y[0]), Create(tmy[0]), run_time=0.3)
        self.pena(t2y[1], tmy[1])
        self.gat("quarto de disco de")
        self.play(Create(Q["arc"]), run_time=2.4)
        lB = TC("B", *V.px(.42, .62), 44, "c")
        self.gat("regiões que não são")
        self.pena(lB)
        self.gat("dentro de um retângulo")
        Rr = curva(V, [(0, -.5), (2, -.5), (2, 2), (0, 2), (0, -.5)], GEO, 2, dash=(8, 8), z=3)
        lR = TC("R", *V.px(2.1, 2.16), 34, "l")             # folga ≥ 12 px do canto de R
        self.play(Create(Rr), run_time=1.0)
        self.pena(lR)
        self.gat("contido em r")
        BR_ = L([("b", "B"), ("c", r"\subset"), ("r", "R")], 1120, 240, 42)
        self.pena(BR_)
        acende(self, (gl(BR_, "c"), None), rt=1.0)
        self.gat("valer zero fora")
        zs_ = [TC(r"\Ge{0}", *V.px(*p_), 34, "c") for p_ in ((1.82, 1.45), (.45, -.27), (1.6, -.27))]
        self.pena(*zs_, lag=0.2)
        F1 = mixl([("m", r"F=\f"), ("t", "EM B"), ("m", r"\cdot"), ("m", "F=0"), ("t", "FORA")], 1120, 240, 42)
        self.play(FadeOut(BR_), run_time=0.3)
        self.remove(BR_)
        self.pena(*F1.p, lag=0.12)

        # a faca em x (ValueTracker): reta tracejada de −½ a 2, tira cheia em B, trechos apagados embaixo e em cima, pontos
        xt = ValueTracker(1.0)
        self.add(xt)
        sai_ = lambda: math.sqrt(max(0.0, 4 - xt.get_value() ** 2))
        self.gat("xis congelado em um")
        faca = always_redraw(lambda: curva(V, [(xt.get_value(), -.56), (xt.get_value(), 2.06)], E1, 2, dash=(6, 8), alpha=.7, z=3))
        self.play(Create(faca.copy()), run_time=0.7)
        self.add(faca)
        q1 = V.px(1, 0)
        t1l = lin_px([(q1[0], q1[1] - 7), (q1[0], q1[1] + 7)], GEO, 2, z=6)
        t1 = TP(r"\Am{1}", q1[0] - 22, q1[1] + 30, 28, "c")
        q2 = V.px(2, 0)
        t2l = lin_px([(q2[0], q2[1] - 7), (q2[0], q2[1] + 7)], GEO, 2, z=6)
        t2 = TP(r"\Am{2}", q2[0] + 24, q2[1] + 30, 28, "c")
        self.play(Create(t1l), Create(t2l), run_time=0.3)
        self.pena(t1, t2, lag=0.2)
        self.gat("a fatia atravessa")
        contorno_ = curva(V, [(.97, -.5), (1.03, -.5), (1.03, 2), (.97, 2), (.97, -.5)], mixh(BG_, E1, .55), 2, dash=(6, 6), z=4)
        self.play(Create(contorno_), run_time=2.2, rate_func=linear)
        self.gat("até ípsilon igual a dois")
        realce(self, contorno_, tmy[0], t2y[0])                        # a fatia inteira, de −½ a 2
        self.gat("só soma zeros")
        tira = always_redraw(lambda: tiraV(V, xt.get_value(), 0, max(.002, sai_())))
        apag = always_redraw(lambda: VGroup(
            curva(V, [(xt.get_value() - .03, sai_()), (xt.get_value() - .03, 2), (xt.get_value() + .03, 2), (xt.get_value() + .03, sai_())],
                  mixh(BG_, E1, .55), 2, dash=(6, 6), z=4),
            curva(V, [(xt.get_value() - .03, 0), (xt.get_value() - .03, -.5), (xt.get_value() + .03, -.5), (xt.get_value() + .03, 0)],
                  mixh(BG_, E1, .55), 2, dash=(6, 6), z=4)))
        self.add(apag)
        self.play(GrowFromEdge(tira.copy(), DOWN), FadeOut(contorno_), run_time=0.9)
        self.add(tira)
        self.remove(contorno_)
        self.gat("então a integral da")
        F2 = L([("ia", r"\int_{\Mg{-1/2}}^{\Mg{2}}"), ("a", r"F(\Am{1},\Y)\,\dY="), ("i", r"\int_{\Az{0}}^{\Co{\sqrt3}}"), ("b", r"\f(\Am{1},\Y)\,\dY")],
               1120, 380, 42, caneta=False)
        altoA = max(gl(F2, "ia"), key=lambda x: x.height)
        supA = [k for k in sel(F2, "ia") if F2[0][k] is not altoA and F2[0][k].get_center()[1] > altoA.get_center()[1]]
        infA = [k for k in sel(F2, "ia") if F2[0][k] is not altoA and k not in supA]
        alto = max(gl(F2, "i"), key=lambda x: x.height)
        idx_s3 = [k for k in sel(F2, "i") if F2[0][k] is not alto and F2[0][k].get_center()[1] > alto.get_center()[1]]   # o √3 fica para o voo
        voos(self, [(tmy[1].copy(), parte(F2, infA, "−1/2")), (t2y[1].copy(), parte(F2, supA, "2"))], rt=0.9)     # −½ e 2 voam das marcas
        self.pena(parte(F2, [k for k in range(len(F2[0])) if k not in idx_s3 + supA + infA], "sem √3"))
        self.gat("onde ela entra no")
        pe = always_redraw(lambda: ponto_px(*V.px(xt.get_value(), 0), AZC, 9))
        self.play(FadeIn(pe), run_time=0.4)
        self.gat("até onde ela sai")
        ps = always_redraw(lambda: ponto_px(*V.px(xt.get_value(), sai_()), CORAL, 9))
        self.play(FadeIn(ps), run_time=0.4)
        self.gat("na circunferência")
        M0 = L([("x", r"\X^2"), ("p", "+"), ("y", r"\Y^2"), ("e", "="), ("q", "4")], 1120, 510, 42)
        self.pena(M0, extra=[Q["arc"].animate.set_stroke(width=W(6))])
        self.play(Q["arc"].animate.set_stroke(width=W(4)), run_time=0.4)
        self.gat("com xis igual a")
        M1 = L([("x", r"\Am{1}^2"), ("p", "+"), ("y", r"\Y^2"), ("e", "="), ("q", "4")], 1120, 510, 42)
        passo(self, M0, M1, [("p", "p"), ("y", "y"), ("e", "e"), ("q", "q")], voos=[(t1.f, [max(sel(M1, "x"), key=lambda k: M1[0][k].height)])], rt=0.7,
              nota="mapa 2a (B1-1: x = 1 na circunferência)")
        M2 = L([("x", r"\Am{1}^2"), ("p", "+"), ("y", r"\Y^2"), ("e", "="), ("q", "4"), ("im", r"\ \Rightarrow\ "), ("yy", r"\Y^2"), ("e2", "="), ("tr", "3")],
               1120, 510, 42)
        passo(self, M1, M2, [(k, k) for k in ("x", "p", "y", "e", "q")], rt=0.6, copia=False,
              nota="mapa 2b (B1-1: 1² + y² = 4 ⇒ y² = 3)")
        M3 = L([("x", r"\Am{1}^2"), ("p", "+"), ("y", r"\Y^2"), ("e", "="), ("q", "4"), ("im", r"\ \Rightarrow\ "), ("yy", r"\Y"), ("e2", "="),
                ("tr", r"\sqrt3")], 1120, 510, 42)
        self.gat("é raiz de três")
        i3 = max(sel(M3, "tr"), key=lambda k: M3[0][k].get_left()[0])          # o "3" é o glifo mais à direita do √3
        passo(self, M2, M3, [(k, k) for k in ("x", "p", "y", "e", "q", "im", "e2")] + [([sel(M2, "yy")[0]], "yy"),
                                                                                    ([sel(M2, "yy")[1]], [k for k in sel(M3, "tr") if k != i3]),
                                                                                    ("tr", [i3])], rt=0.9,
              nota="mapa 2c (B1-1: y² = 3 → y = √3; o quadrado vira a raiz)")
        hl = curva(V, [(0, S3), (1, S3)], GEO, 2, dash=(6, 6), z=3)
        ts3 = tick(V, "y", S3, r"\Mg{\sqrt3}")
        self.play(Create(hl), Create(ts3[0]), run_time=0.5)
        voos(self, [(VGroup(*gl(M3, "tr")), ts3[1]), (ps, VGroup(*[F2[0][k] for k in idx_s3]))], rt=1.0)
        junta(self, *F2._partes)
        F2._esc = True
        # "deixa o xis andar": x de 1 a 0, depois quase 2, e volta a 1 (a tira, os dois pontos e os trechos apagados andam juntos)
        self.gat("deixa o xis andar")
        self.play(FadeOut(hl), FadeOut(ts3[0]), FadeOut(ts3[1]), *[FadeOut(z_) for z_ in zs_], FadeOut(t1), FadeOut(t2), FadeOut(lB), run_time=0.3)
        self.play(xt.animate.set_value(0.0), run_time=1.6)
        self.gat("perto de xis igual")
        self.play(xt.animate.set_value(1.9), run_time=2.6)
        self.play(xt.animate.set_value(1.0), run_time=1.4)
        self.play(FadeIn(hl), FadeIn(ts3[0]), FadeIn(ts3[1]), *[FadeIn(z_) for z_ in zs_], FadeIn(t1), FadeIn(t2), FadeIn(lB), run_time=0.3)
        ja_escrita(ts3[1])
        self.gat("raiz de quatro menos")
        r1 = rot(V, r"\Co{\Y=\sqrt{4-\X^2}}", (1.3, 1.78), 0, 0, 30)
        self.pena(r1)
        self.gat("ípsilon igual a zero")
        r0 = rot(V, r"\Az{\Y=0}", (1.16, 0), 0, -30, 28)
        self.pena(r0)
        self.gat("a fatia começa numa")
        tc = leg("A FATIA TERMINA NA CURVA", 1120, 620, CORAL, "left", 30)
        self.pena(tc)
        self.marca("v2_03")

        # ── B1-2 · por que o Fubini ainda vale (alvos v2_04, v2_05), layout A-pequeno a 170 px/unidade ──
        self.an("B1-2")
        self.secao("POR QUE O FUBINI VALE")
        fixos = [g, Q["reg"], sx, sy, lx, ly, Q["arc"], Rr, lR, lB]
        sai = [m for m in self.snap() if m not in fixos]
        k = 170 / 240
        def leva(m):
            return m.animate.scale(k, about_point=V.P(0, 0)).shift(PQ2.P(0, 0) - V.P(0, 0))
        for m in sai:
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in sai], run_time=0.4)                 # os rótulos saem antes de o palco encolher (sem cruzar traços)
        self.play(*[leva(m) for m in fixos], run_time=1.0)
        self.remove(*sai, xt)
        self.gat("duas coisas")                                              # as caixas já nascem com o título (GEO) e um círculo vazio
        cx1, cx2 = [], []
        for Y, t, lst in ((290, "F INTEGRÁVEL EM R", cx1), (410, "FATIA INTEGRÁVEL", cx2)):
            lst += [moldura(1120, Y - 45, 640, 80, GEO, .45, 2, 12), circ_px(1160, Y - 6, 15, GEO, 2.5), T(t, 1200, Y + 8, 30, "left", GEO),
                    TC(r"\Ge{?}", 1730, Y - 4, 34, "c")]
        self.play(Create(cx1[0]), Create(cx2[0]), Create(cx1[1]), Create(cx2[1]), run_time=0.6)
        self.pena(cx1[2], cx1[3], cx2[2], cx2[3], lag=0.15)
        self.marca("v2_04", agora=True)

        def confirma(lst, Y, t):
            ck = check_px(1160, Y - 6, MEN, .9)
            tb = T(t, 1200, Y + 8, 30, "left", BR)
            ja_escrita(tb)
            self.play(FadeOut(lst[1]), Create(ck), Transform(lst[2], tb), FadeOut(lst[3]), run_time=0.6)
            self.remove(lst[1], lst[3])
            return ck
        self.gat("a função integrável no")
        self.play(Rr.animate.set_stroke(width=W(4)), run_time=0.5)
        self.play(Rr.animate.set_stroke(width=W(2)), run_time=0.5)
        self.gat("cada fatia com integral")
        tq = tiraV(PQ2, 1, 0, S3)
        self.play(GrowFromEdge(tq, DOWN), run_time=0.8)
        self.gat("f é contínua em")
        self.play(FadeOut(tq), Q["reg"].animate.set_fill(mixh(BG_, GEO, .3)), run_time=0.6)
        self.remove(tq)
        self.play(Q["reg"].animate.set_fill(RB), run_time=0.5)
        self.gat("fechado e limitado")
        bd = curva(PQ2, [(0, 2)] + [(0, 0), (2, 0)], BR, 2, z=6)
        self.play(Create(bd), run_time=0.8)
        self.gat("com zero fora")
        zq1 = TC(r"\Ge{0}", *PQ2.px(1.82, 1.6), 30, "c")
        zq2 = TC(r"\Ge{0}", *PQ2.px(1.6, -.27), 30, "c")
        self.pena(zq1, zq2, lag=0.2)
        self.gat("na fronteira de b")
        fa = curva(PQ2, arco_q(), AL, 2.5, z=7)
        fs1 = curva(PQ2, [(0, 0), (2, 0)], AL, 2.5, z=7)
        fs2 = curva(PQ2, [(0, 0), (0, 2)], AL, 2.5, z=7)
        self.play(Create(fa), run_time=0.9)
        self.gat("os dois segmentos")
        self.play(Create(fs1), Create(fs2), FadeOut(bd), run_time=0.9)
        self.remove(bd)
        self.gat("estudou conteúdo nulo")
        cn = leg("CONTEÚDO NULO", *PQ2.px(2.1, 1.25), AL, "left", 26)
        self.pena(cn)
        self.gat("essas linhas têm")
        self.play(*[m.animate.set_stroke(width=W(5)) for m in (fa, fs1, fs2)], run_time=0.5)
        self.play(*[m.animate.set_stroke(width=W(2.5)) for m in (fa, fs1, fs2)], run_time=0.5)
        self.gat("a estendida é integrável")
        ck1 = confirma(cx1, 290, "F INTEGRÁVEL EM R")
        # "cada fatia vale zero, depois f, depois zero": a tira x = 1 do palco e o painel grande da MESMA fatia
        self.gat("cada fatia vale zero")
        trR = curva(PQ2, [(.96, -.5), (1.04, -.5), (1.04, 2), (.96, 2), (.96, -.5)], E1, 2, dash=(5, 5), z=4)
        trB = tiraV(PQ2, 1, 0, S3, h=.08)
        q1 = PQ2.px(1, 0)
        t1p = TP(r"\Am{1}", q1[0] - 24, q1[1] + 26, 26, "c")
        Lp = Lat(330, 975, 250, 70)
        ff = lambda Y: 1.3 + .35 * math.sin(2.2 * Y)
        gp = VGroup()
        a_ = -.5
        while a_ <= 2.25 + 1e-9:
            gp.add(lin_px([Lp.px(a_, 0), Lp.px(a_, 2)], GRADE, 1.2, z=-9))
            a_ += .25
        for b_ in (0, .5, 1, 1.5, 2):
            gp.add(lin_px([Lp.px(-.5, b_), Lp.px(2.25, b_)], GRADE, 1.2, z=-9))
        ehp = seta_px(Lp.px(-.6, 0), Lp.px(2.3, 0), E2, 3, 16, z=6)
        evp = seta_px(Lp.px(-.5, 0), Lp.px(-.5, 2.1), CI, 3, 16, z=6)
        q = Lp.px(2.3, 0)
        lyp = TC(r"\Y", q[0] + 24, q[1], 30, "c")
        q = Lp.px(-.5, 2.1)
        lfp = TC(r"\f", q[0], q[1] - 24, 30, "c")
        tks = VGroup(*[TC(r"\Mg{" + s_ + "}", Lp.px(a, 0)[0], Lp.px(a, 0)[1] + 40, 26, "c") for a, s_ in ((-.5, r"-\dfrac{1}{2}"), (0, "0"), (S3, r"\sqrt3"), (2, "2"))])
        uf = mixl([("t", "UMA FATIA:", GEO), ("m", r"\X=\Am{1}")], 140, 770, 30)
        self.play(Create(trR), GrowFromEdge(trB, DOWN), FadeIn(gp), GrowFromPoint(ehp, Lp.P(-.5, 0)), GrowFromPoint(evp, Lp.P(-.5, 0)), run_time=0.8)
        self.pena(t1p, *uf.p, lyp, lfp, tks, lag=0.08)
        c_a = curva(Lp, [(-.5, 0), (0, 0)], CI, 5, z=6)
        c_f = curva(Lp, cX(ff, 0, S3, 60), CI, 5, z=6)
        c_b = curva(Lp, [(S3, 0), (2, 0)], CI, 5, z=6)
        self.gat("zero depois f depois")
        l0a = TC("0", *Lp.px(-.25, .45), 28, "c")
        self.play(Create(c_a), run_time=0.4)
        self.pena(l0a)
        self.play(Create(c_f), run_time=0.8)
        lf = TC(r"\f", *Lp.px(.9, ff(.9) + .55), 30, "c")
        self.pena(lf)
        self.play(Create(c_b), run_time=0.4)
        l0b = TC("0", *Lp.px(1.87, .45), 28, "c")
        self.pena(l0b)
        self.gat("dois saltos e")
        j1 = curva(Lp, [(0, 0), (0, ff(0))], AL, 2, dash=(5, 5), z=5)
        j2 = curva(Lp, [(S3, 0), (S3, ff(S3))], AL, 2, dash=(5, 5), z=5)
        ds = leg("DOIS SALTOS", 800, 880, AL, "left", 26)
        self.play(Create(j1), Create(j2), run_time=0.7)
        self.pena(ds)
        self.gat("tem integral lá")
        ar_ = poly_px([Lp.px(0, 0)] + [Lp.px(a, ff(a)) for a in np.linspace(0, S3, 40)] + [Lp.px(S3, 0)], mixh(BG_, CI, .3), z=4)
        self.play(FadeIn(ar_), run_time=0.8)
        self.gat("as duas hipóteses valem")
        ck2 = confirma(cx2, 410, "FATIA INTEGRÁVEL")
        self.gat("o teorema de fubini")
        tf = leg("TEOREMA DE FUBINI", 1120, 540, GEO, "left", 26)
        self.pena(tf)
        self.gat("garante a integral")
        FF = L([("im", r"\Rightarrow\ "), ("a", r"\iint_B\f\,dA="), ("io", r"\int_{\Am{a}}^{\Am{b}}\!"), ("ii", r"\int_{\Az{c(\X)}}^{\Co{d(\X)}}"),
                ("r", r"\f\,\dY\,\dX")], 1120, 630, 42)
        self.pena(FF)
        self.gat("com os limites de dentro")
        pq1, pq2 = pontos_es(PQ2, (1, 0), (1, S3))
        self.play(FadeIn(pq1, scale=.5), FadeIn(pq2, scale=.5), run_time=0.4)
        acende(self, (VGroup(*[x for x in gl(FF, "ii") if x.height < max(y.height for y in gl(FF, "ii"))]), CORAL), rt=1.2)
        self.marca("v2_05", agora=True)
        self.gat("nada de especial do")
        gen = regiao_gen(PQ2)
        painel_ = [trR, trB, t1p, gp, ehp, evp, lyp, lfp, tks, *uf.p, c_a, c_f, c_b, l0a, lf, l0b, j1, j2, ds, ar_, pq1, pq2, zq1, zq2]
        self.play(*[FadeOut(m) for m in painel_], run_time=0.4)
        self.remove(*painel_)
        self.play(ReplacementTransform(Q["reg"], gen), FadeOut(fa), FadeOut(fs1), FadeOut(fs2), FadeOut(cn), FadeOut(Q["arc"]),
                  lB.animate.move_to(PX(*PQ2.px(1.0, 1.05))), run_time=1.6)
        self.remove(fa, fs1, fs2, cn, Q["arc"])
        cc = curva(PQ2, cX(c_b21, .3, 1.85), AZC, 3, z=6)
        dd = curva(PQ2, cX(d_b21, .3, 1.85), CORAL, 3, z=6)
        self.gat("entre os gráficos de")
        self.play(Create(cc), Create(dd), run_time=1.0)

        # ── B1-3 · a área π (alvo 06) ──
        self.an("B1-3")
        self.secao("O QUARTO DE DISCO")
        sai = [m for m in self.snap() if m not in (gen, sx, sy, lx, ly, lB, Rr, lR)]
        for m in sai:
            m.clear_updaters()
        k2 = 240 / 170
        def volta(m):
            return m.animate.scale(k2, about_point=PQ2.P(0, 0)).shift(CH.P(0, 0) - PQ2.P(0, 0))
        disco = regiao(CH, disco_pts())
        arc = curva(CH, arco_q(), CORAL, 4)
        g2 = papel_v(CH, (0, 2.2, 0, 2.2))
        sx2, sy2, lx2, ly2 = eixos_v(CH, 2.35, 2.35)
        for m in (lx2, ly2):
            ja_escrita(m)
        self.play(*[FadeOut(m) for m in sai + [Rr, lR, g]], ReplacementTransform(sx, sx2), ReplacementTransform(sy, sy2), ReplacementTransform(lx, lx2),
                  ReplacementTransform(ly, ly2), FadeIn(g2), FadeOut(lB), ReplacementTransform(gen, disco), run_time=1.4)
        self.remove(*sai, Rr, lR, lB, g)
        self.grade = g2
        t2x, t2y = tick(CH, "x", 2, r"\Am{2}"), tick(CH, "y", 2, r"\Mg{2}")
        self.play(Create(arc), Create(t2x[0]), Create(t2y[0]), run_time=0.8)
        self.pena(t2x[1], t2y[1])
        self.gat("f igual a um")
        A1 = L([("l", r"\iint_B 1\,dA="), ("io", r"\int_0^2\!"), ("ii", r"\int_{\Az{0}}^{\Co{\sqrt{4-\X^2}}}"), ("u", r"1\,\dY"), ("dx", r"\,\dX")],
               1120, 240, 40)
        self.pena(A1)
        self.gat("a integral de dentro")
        seg = curva(CH, [(1, 0), (1, S3)], E1, 5, z=6)
        self.play(Create(seg), run_time=1.6)
        self.gat("raiz de quatro menos")
        sp1, sp2 = pontos_es(CH, (1, 0), (1, S3))
        self.play(FadeIn(sp1, scale=.5), FadeIn(sp2, scale=.5), run_time=0.4)
        self.gat("de um dê ípsilon")
        realce(self, seg)                                              # o segmento que a integral de dentro mede
        self.gat("comprimento da fatia")
        self.play(FadeOut(sp1), FadeOut(sp2), seg.animate.set_stroke(width=W(8)), run_time=0.5)
        self.remove(sp1, sp2)
        acende(self, (VGroup(*[x for x in gl(A1, "ii") if x.height < max(y.height for y in gl(A1, "ii"))]), CORAL), rt=0.8)
        self.gat("dá a área")
        segs = [curva(CH, [(a, 0), (a, math.sqrt(4 - a * a))], E1, 3, z=5) for a in np.arange(.1, 2, .2)]
        self.play(FadeOut(seg), LaggedStart(*[Create(s) for s in segs], lag_ratio=0.18), run_time=1.8)
        self.remove(seg)
        self.gat("fica a integral de")
        A2 = L([("eq", "="), ("io", r"\int_0^2"), ("r", r"\Co{\sqrt{4-\X^2}}"), ("dx", r"\,\dX")], 1160, 360, 40)
        ii = list(gl(A1, "ii"))
        alto = max(ii, key=lambda x: x.height)
        sup = [k for k in sel(A1, "ii") if A1[0][k] is not alto and A1[0][k].get_center()[1] > alto.get_center()[1]]
        passo(self, A1, A2, [("io", "io"), (sup, "r"), ("dx", "dx")], rt=1.4, copia=True,
              nota="mapa 3a (B1-3: a de dentro vira o comprimento; o 1 dy sai)")
        realce(self, *segs)                                            # os comprimentos que a integral de fora soma
        self.gat("uma integral do cálculo")
        xs_ = ValueTracker(.05)
        self.add(xs_)
        sv = always_redraw(lambda: curva(CH, [(xs_.get_value(), 0), (xs_.get_value(), math.sqrt(max(0.0, 4 - xs_.get_value() ** 2)))], CORAL, 4, z=7))
        self.play(FadeIn(sv), run_time=0.2)
        self.play(xs_.animate.set_value(1.97), run_time=2.6, rate_func=linear)
        self.play(FadeOut(sv), run_time=0.3)
        sv.clear_updaters()
        self.remove(sv, xs_)
        self.gat("a geometria já")
        rr = curva(CH, [(0, 0), (1, S3)], GEO, 3, z=7)                     # raio a 60°; o 2 fica fora das fatias, além do arco
        lr = TP(r"2", *CH.px(1.2, 2.08), 30, "c")
        self.play(*[s_.animate.set_stroke(opacity=.25) for s_ in segs], run_time=0.5)
        self.play(Create(rr), run_time=0.7)
        self.pena(lr)
        self.gat("um quarto de pi")
        A3 = L([("eq", "="), ("fr", r"\dfrac{\pi\cdot 2^2}{4}"), ("e2", "="), ("pi", r"\pi")], 1160, 470, 44)
        passo(self, A2, A3, [("eq", "eq"), (["io", "r", "dx"], "fr")], rt=1.4, copia=True, nota="mapa 3b (B1-3: área do quarto de disco)")
        self.gat("lembra das caixinhas")
        self.play(FadeOut(rr), FadeOut(lr), *[s_.animate.set_stroke(opacity=1) for s_ in segs], run_time=0.5)    # as fatias voltam (alvo 06)
        self.remove(rr, lr)
        cx_ = leg("CAIXINHAS", 1130, 690, GEO, "left", 26)
        X = lambda v: 1150 + (v - 3.1) * 3200
        Y = 760
        reg_ = lin_px([(1130, Y), (1820, Y)], GEO, 3, z=3)
        self.play(Create(reg_), run_time=0.8)
        self.pena(cx_)
        for v, s_, gg, dy in ((3.25, "3,25", "três vírgula vinte", -24), (3.17, "3,17", "três vírgula dezessete", -24), (3.15, "3,15", "três vírgula quinze", -24)):
            self.gat(gg)
            d = ponto_px(X(v), Y, GEO, 8, z=6)
            lb = leg(s_, X(v), Y + dy, GEO, "center", 26)
            self.play(FadeIn(d, scale=0.5), run_time=0.3)
            self.pena(lb)
        self.gat("chegando em pi")
        dp = ponto_px(X(math.pi), Y, MEN, 10, z=7)
        lp = TC(r"\Me{\pi\approx 3{,}1416}", X(math.pi) - 30, Y + 50, 30, "c")
        self.play(FadeIn(dp, scale=0.5), run_time=0.3)
        self.pena(lp)
        self.gat("o valor exato")
        acende(self, (gl(A3, "pi"), MEN), (lp, MEN), rt=0.8)
        self.marca("06")
        self.sai_fim()
