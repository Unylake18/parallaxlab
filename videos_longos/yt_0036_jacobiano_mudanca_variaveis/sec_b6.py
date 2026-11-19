"""yt_0036 · B6 · o trapézio (alvos 14 e 15) — v2. B6-1: o papel com a grade inclinada; C10 (x + y e x − y voam do expoente; o 2 atravessa a
igualdade por glyph map, M8) e C11 (−1/4 − 1/4 → −1/2 por mapa; |J| = 1/2 nasce da conta, ganha a moldura lima e o selo O MEIO DO LOSANGO por
3 s; a conferência −2). B6-2: layout B; cada lado acende com a equação, glyph map 12 e voa para o plano u, v; a faixa de baixo é uma grade 2 × 2
que acumula (Q12), a linha dos vértices e B_uv. B6-3: layout A (plano u, v em vista(420, 700, 140)), C13 montada por mapas em quatro passos (Q13),
C14 e C15 por mapas (M9). B6-4: as células 1 e 2 inteiras, as duas pontas que viram uma célula (½ + ½ = 1) e o 3 (Q14); C16; 1/2 = O JACOBIANO."""
from j36 import *

AX = (-.45, 2.6, -2.45, .55)
VX7 = Vw(420, 300, 175)
VX, VU, AU = Vw(1180, 300, 175), Vw(400, 600, 120), (-2.4, 2.4, -.3, 2.6)
VU8, AU8 = Vw(420, 700, 140), (-2.15, 2.15, -.2, 2.5)
VX9, AX9 = Vw(820, 380, 120), (-.25, 2.3, -2.3, .35)
EMENDA_B62 = 840
TRAP = [(1, 0), (2, 0), (0, -2), (0, -1)]
TRAP_UV = [(1, 1), (2, 2), (-2, 2), (-1, 1)]
LHS = [("ii", r"\iint_B"), ("e", "e"), ("ex", r"^{\frac{\Uc{\X+\Y}}{\Vc{\X-\Y}}}"), ("dA", r"\,dA")]


def papel_trap(v, alpha=.55):
    d = monta_plano(v, AX, 2.55, .5, -.4, -2.4, ticks=[("x", 1, r"\Am{1}"), ("x", 2, r"\Am{2}"), ("y", -1, r"\Mg{-1}"), ("y", -2, r"\Mg{-2}")])
    fu = familia(v, mapT, range(-3, 4), "u", AX, CU, 1.6, alpha)
    fv = familia(v, mapT, range(-1, 5), "v", AX, CVV, 1.6, alpha)
    reg = poligono(v, TRAP, RB, 1.0, GEO, 3, z=1)
    return d, fu, fv, reg


def lado_a_lado(sc, A, pecas, pares, nota, gap=30):
    """M8: a linha B nasce À DIREITA de A, na mesma altura, por glyph map de uma cópia de A (A fica)."""
    B = Lp(pecas, dir_(A) + gap, centro(A)[1], A._size)
    B._xy = (esq(B), centro(B)[1])
    estava = A in sc.mobjects
    passo(sc, A, B, pares(B) if callable(pares) else pares, copia=True, rt=1.1, nota=nota)
    if estava and A not in sc.mobjects:
        sc.add(A)
    if getattr(sc, "col", None) is not None:
        sc.col.registra(B)                 # a fração de B é mais alta que A: a próxima linha da coluna vem abaixo dela
    return B


class PB6(J36):
    ANTES = "CONFERINDO O TEOREMA"
    CHIP = False                            # v2 §6.3: no B6-1 o |J| = 1/2 nasce da conta C11 (não vem do B3)

    def corpo(self):
        self.an("B6-1")
        self.secao("O TRAPÉZIO: O JACOBIANO")
        d, fu, fv, reg = papel_trap(VX7)
        self.fundo(VX7, rt=0)
        self.play(FadeIn(d["g"]), GrowFromPoint(d["sx"], VX7.P(0, 0)), GrowFromPoint(d["sy"], VX7.P(0, 0)), *[Create(t[0]) for t in d["tk"]],
                  FadeIn(fu), FadeIn(fv), FadeIn(reg[0]), Create(reg[1]), run_time=1.0)
        self.pena(d["lx"], d["ly"], *[t[1] for t in d["tk"]], lag=0.04)
        A = Lp(LHS, 460 - 180, 985, 40)
        A.shift(RIGHT * (460 - (esq(A) + dir_(A)) / 2) / 120)
        self.pena(A)
        num, bar, den = nd(A, "ex")
        CX = 1120
        col = self.col = Coluna36(self, CX, 200)
        col.GAP36 = 24
        # passo um: u = x + y, v = x − y (voam do expoente)
        self.gat("então u igual a")
        U1 = Lp([("u", r"\uu="), ("s", r"\Uc{\X+\Y}"), ("v", r"\qquad\vv="), ("d", r"\Vc{\X-\Y}")], CX, 0, 40)
        col.poe(U1)
        self.escreve_voos(U1, [(VGroup(*[A[0][i] for i in num]), "s"), (VGroup(*[A[0][i] for i in den]), "d")])
        # passo dois: a inversa — M8: u + v = 2x ⇒ x = (u + v)/2 (o 2 atravessa a igualdade e vai para baixo)
        self.gat("soma as duas")
        X2 = Lp([("l", r"\uu+\vv"), ("e", "="), ("r", r"2\X")], CX, 0, 40)
        col.poe(X2)
        X2._xy = (CX, centro(X2)[1])
        self.pena(X2)
        self.gat("então xis é u")
        PX2 = [("i", r"\Rightarrow\ "), ("x", r"\X"), ("e", "="), ("f", r"\dfrac{\uu+\vv}{2}")]
        X2b = lado_a_lado(self, X2, PX2, lambda B: [(X2._ix["l"], nd(B, "f")[0]), (X2._ix["e"], "e"), ([X2._ix["r"][0]], nd(B, "f")[2]),
                                                     ([X2._ix["r"][1]], "x")], "M8 C10 (o 2 atravessa: x = (u + v)/2)")
        self.gat("subtrai")
        Y2 = deriva(self, X2, [("l", r"\uu-\vv"), ("e", "="), ("r", r"2\Y")],
                    lambda B: [([X2._ix["l"][k]], [B._ix["l"][k]]) for k in range(3)] + [("e", "e"), ([X2._ix["r"][0]], [B._ix["r"][0]]),
                                                                                       ([X2._ix["r"][1]], [B._ix["r"][1]])],
                    col, x=CX, rt=0.9, nota="M8 C10 (subtrai: o + vira −, o x vira y)")
        self.gat("então ípsilon é u")
        PY2 = [("i", r"\Rightarrow\ "), ("y", r"\Y"), ("e", "="), ("f", r"\dfrac{\uu-\vv}{2}")]
        Y2b = lado_a_lado(self, Y2, PY2, lambda B: [(Y2._ix["l"], nd(B, "f")[0]), (Y2._ix["e"], "e"), ([Y2._ix["r"][0]], nd(B, "f")[2]),
                                                     ([Y2._ix["r"][1]], "y")], "M8 C10 (o 2 atravessa: y = (u − v)/2)")
        # passo três: as derivadas, uma a uma (duas linhas), e o jacobiano
        D1a = Lp([("a", r"\dd{\X}{\uu}=\dfrac{1}{2}"), ("b", r"\qquad\dd{\X}{\vv}=\dfrac{1}{2}")], CX, 0, 40)
        col.poe(D1a)
        D1b = Lp([("c", r"\dd{\Y}{\uu}=\dfrac{1}{2}"), ("d", r"\qquad\dd{\Y}{\vv}=-\dfrac{1}{2}")], CX, 0, 40)
        for (Dk, k_), g_ in zip(((D1a, "a"), (D1a, "b"), (D1b, "c"), (D1b, "d")),
                                ("em relação a u é um meio", "em relação a vê um meio", "a de ípsilon em relação a u", "e em relação a vê menos")):
            self.gat(g_)
            if k_ == "c":
                col.poe(D1b)                   # a segunda linha das derivadas entra embaixo da primeira (já escrita)
            self.pena(parte(Dk, Dk._ix[k_], k_))
        # as linhas que já serviram saem (C10 e as derivadas ficam como origem do J até ele estar escrito)
        self.gat("um meio vezes menos um meio")
        J2 = Lp([("J", r"\Jq"), ("e", "="), ("a", r"\left(\dfrac{1}{2}\right)"), ("d", r"\left(-\dfrac{1}{2}\right)"), ("m", "-"), ("b", r"\left(\dfrac{1}{2}\right)"),
                 ("c", r"\left(\dfrac{1}{2}\right)")], CX, 0, 40)
        col.poe(J2)
        J2._xy = (CX, centro(J2)[1])
        rhs = lambda Dk, k_, n: VGroup(*[Dk[0][i] for i in Dk._ix[k_][-n:]])
        inner = lambda k_: [J2._ix[k_][i] for i in range(1, len(J2._ix[k_]) - 1)]
        self.pena(parte(J2, J2._ix["J"] + J2._ix["e"] + J2._ix["m"] + [J2._ix[k][0] for k in "adbc"] + [J2._ix[k][-1] for k in "adbc"], "J = ( )( ) − ( )( )"))
        voos(self, [(rhs(D1a, "a", 3).copy(), parte(J2, inner("a"), "xu")), (rhs(D1b, "d", 4).copy(), parte(J2, inner("d"), "yv")),
                    (rhs(D1a, "b", 3).copy(), parte(J2, inner("b"), "xv")), (rhs(D1b, "c", 3).copy(), parte(J2, inner("c"), "yu"))], rt=1.0)
        # C11 (mapa): (1/2)(−1/2) − (1/2)(1/2) → −1/4 − 1/4 → −1/2
        self.gat("menos um quarto menos um quarto")
        a_, d_, b_, c_ = J2._ix["a"], J2._ix["d"], J2._ix["b"], J2._ix["c"]

        def mapa11(B):
            q = B._ix["q"]
            return [("e", "e"), ([d_[1]], [q[0]]), ([a_[1], d_[2]], [q[1]]), ([a_[2], d_[3]], [q[2]]), ([a_[3], d_[4]], [q[3]]), ("m", [q[4]]),
                    ([b_[1], c_[1]], [q[5]]), ([b_[2], c_[2]], [q[6]]), ([b_[3], c_[3]], [q[7]])]
        J3 = deriva(self, J2, [("e", "="), ("q", r"-\dfrac{1}{4}-\dfrac{1}{4}")], mapa11, col, x=eq_x(J2, "e"), nota="M8 C11 (produtos → −1/4 − 1/4)")
        J3 = cresce(self, J3, [("e2", "="), ("r", r"\Lm{-\dfrac{1}{2}}")], voos=lambda B: [(gl(J3, "q").copy(), "r")], col=col, nota="C11 (= −1/2)")
        # |J| = 1/2 nasce da conta (mapa: o 1/2 do −1/2) e ganha a moldura lima; selo O MEIO DO LOSANGO por 3 s
        self.gat("módulo um meio")
        saem = [U1, X2, X2b, Y2, Y2b, D1a, D1b]
        dy = centro(J2)[1] - 320                                      # abaixo do chip do canto (que chega no fim do B6-1)
        self.play(*[FadeOut(m) for m in saem], run_time=0.4)  # final K12: troca de página em dois tempos (sai, depois sobe)
        self.play(*[m.animate.shift(UP * dy / 120) for m in (J2, J3)], run_time=0.6)
        self.remove(*saem)
        col.ls = [J2, J3]
        r3 = J3._ix["r"]
        Jm = deriva(self, J3, [("J", r"\Lm{|J|}"), ("e", "="), ("h", r"\Lm{\dfrac{1}{2}}")], lambda B: [(r3[1:], "h")], col, x=CX, size=48, gap=34,
                    nota="C11 (|−1/2| → |J| = 1/2)")
        molJ = moldura(esq(Jm) - 16, pxof(Jm.get_top())[1] - 12, larg(Jm) + 32, Jm.height * 120 + 24, LIMA, 1.0, 3, 10)
        self.play(Create(molJ), run_time=0.4)
        sl_ = selo("O MEIO DO LOSANGO", dir_(Jm) + 40, centro(Jm)[1] + 10, GEO, 26)
        poe_selo(self, sl_)
        t_sl = self.t
        self.gat("pelo outro lado")
        if self.t - t_sl < 3.0:
            self.wait(3.0 - (self.t - t_sl))
        self.play(*[FadeOut(m) for m in sl_], run_time=0.3)
        self.remove(*sl_)
        K = Lp([("J", r"\dfrac{\partial(\uu,\vv)}{\partial(\X,\Y)}"), ("e", "="), ("p", r"1\cdot(-1)-1\cdot 1")], CX, 0, 40)
        col.poe(K, gap=34)
        K._xy = (CX, centro(K)[1])
        self.pena(K)
        K = cresce(self, K, [("e2", "="), ("r", r"\Al{-2}")], voos=lambda B: [(gl(K, "p").copy(), "r")], col=col, nota="C11 (conferência = −2)")
        self.gat("divide por dois")
        P = Lp([("a", r"(\Al{-2})"), ("c", r"\cdot"), ("b", r"\left(\Lm{-\dfrac{1}{2}}\right)"), ("e", "="), ("r", "1")], CX, 0, 40)
        col.poe(P)
        P._xy = (CX, centro(P)[1])
        self.escreve_voos(P, [(gl(K, "r"), [P._ix["a"][1], P._ix["a"][2]]), (gl(J3, "r"), [P._ix["b"][k] for k in range(1, len(P._ix["b"]) - 1)])])
        ck = check_px(dir_(P) + 30, centro(P)[1], MEN)
        self.play(Create(ck), run_time=0.4)
        self.gat("um sobre raiz de dois")
        cel = celula(VX7, mapT, 0, 1, 1, 2, wb=2.5)
        entra_cel(self, cel, rt=0.7)
        q1 = VX7.px(1.62, -.78)
        r1 = rotm([("t", "LADO", GEO), ("m", r"\dfrac{1}{\sqrt{2}}")], q1[0], q1[1] - 30, 26, "l")
        r2 = rotm([("t", "ÁREA", LIMA), ("m", r"\Lm{\dfrac{1}{2}}")], q1[0], q1[1] + 40, 26, "l")
        self.pena(r1, r2, lag=0.2)
        # o |J| = 1/2 emoldurado vira o chip do canto (vale até o fim do B6; o 1/2 da integral do B6-3 voa dele)
        self.wait(0.4)
        ch2 = chip_J()
        rota = [(1000, centro(Jm)[1]), (1000, 185)]                 # sobe pelo vão entre o plano e a coluna e vai por cima das linhas até o canto
        voos(self, [(Jm, ch2.m, rota), (molJ, ch2.mol, rota)], rt=0.9, seq=False)
        self.remove(ch2.m, ch2.mol)
        self.add(ch2)
        self.chipJ = ch2
        self.marca("B6-1")

        # ════ B6-2 · a região nova (Q12: a faixa de baixo é uma grade 2 × 2 que acumula) ════
        self.an("B6-2")
        self.secao("O TRAPÉZIO: A REGIÃO NOVA")
        fica = [d["g"], d["sx"], d["sy"], d["lx"], d["ly"], fu, fv, reg] + [x for t in d["tk"] for x in t]
        sai = [m for m in self.snap() if m not in fica]
        # a grade do papel anda junto (mais larga que a tela, para não abrir liso) e depois vira as duas metades
        gX = papel(VX7, area=area_px(VX7, -(1180 - 420), 1920)).set_z_index(-10)
        for x in gX.get_family():
            x._sem_foco = True
        self.fundo(g=gX, rt=0.3, extra=[FadeOut(m) for m in sai])
        self.remove(*sai)
        self.play(*[m.animate.shift(RIGHT * (1180 - 420) / 120) for m in fica + [gX]], run_time=0.8)
        self.play(*[m.animate.set_stroke(opacity=.4) for f_ in (fu, fv) for m in f_], run_time=0.3)
        dU = monta_plano(VU, AU, 2.45, 2.7, -2.45, -.3, uv=True)
        ps, pl = phi_seta(880, 735, 250, r"\psi:\ \uu=\X+\Y,\ \vv=\X-\Y", size=30)
        self.gat("cada lado do trapézio")
        self.fundo(VU, VX, emenda=EMENDA_B62, rt=0.3)
        entra_plano(self, dU, rt=0.6, extra=[Create(ps)])
        self.pena(pl)
        lados = [((1, 0), (2, 0), (1, 1), (2, 2), CORAL), ((2, 0), (0, -2), (2, 2), (-2, 2), CVV), ((0, -2), (0, -1), (-2, 2), (-1, 1), AZC),
                 ((0, -1), (1, 0), (-1, 1), (1, 1), CVV)]
        # Q12: y = 0 14 px acima do eixo x, à direita do vértice (2, 0); x − y = 1 à esquerda do tique −1 (≥ 16 px)
        rotx = [TP(r"\Co{\Y=0}", VX.px(2, 0)[0] + 50, VX.px(2, 0)[1] - 14 - 15, 26, "l"),
                TP(r"\Vc{\X-\Y=2}", VX.px(1.15, -.85)[0] + 30, VX.px(1.15, -.85)[1] + 14, 26, "l"),
                TP(r"\Az{\X=0}", VX.px(0, -1.5)[0] - 22, VX.px(0, -1.5)[1] + 4, 26, "r"),
                TP(r"\Vc{\X-\Y=1}", VX.px(0, -.62)[0] - 60, VX.px(0, -.62)[1], 26, "r")]
        rotu = [TP(r"\Co{\uu=\vv}", VU.px(1.5, 1.5)[0] + 22, VU.px(1.5, 1.5)[1] + 12, 26, "l"), TP(r"\Vc{\vv=2}", VU.px(.5, 2)[0] + 30, VU.px(.5, 2)[1] - 26, 26, "c"),
                TP(r"\Az{\uu=-\vv}", VU.px(-1.5, 1.5)[0] - 22, VU.px(-1.5, 1.5)[1] + 12, 26, "r"), TP(r"\Vc{\vv=1}", VU.px(.5, 1)[0], VU.px(.5, 1)[1] + 26, 26, "c")]
        bandas = [[("a", r"\Co{\Y=0:}"), ("b", r"\ \uu=\X,\ \vv=\X")], [("a", r"\Vc{\X-\Y=2}")], [("a", r"\Az{\X=0:}"), ("b", r"\ \uu=\Y,\ \vv=-\Y")],
                  [("a", r"\Vc{\X-\Y=1}")]]
        finais = [r"\Co{\uu=\vv}", r"\Vc{\vv=2}", r"\Az{\uu=-\vv}", r"\Vc{\vv=1}"]
        gts = ["o de cima ípsilon", "a borda xis menos ípsilon igual a dois", "o lado xis igual a zero", "e a borda xis menos ípsilon igual a um"]
        GX, GY = (140, 1000), (770, 840)                             # a grade 2 × 2 da faixa de baixo (fica até o fim da cena)
        regU = poly_px([VU.px(*p) for p in TRAP_UV], RB, 1.0, z=1)
        for k, ((a0, a1, b0, b1, cor), bd_, fin, g_) in enumerate(zip(lados, bandas, finais, gts)):
            self.gat(g_)
            lx_ = lin_px([VX.px(*a0), VX.px(*a1)], cor, 4, z=4)
            self.play(Create(lx_), run_time=0.5)
            self.pena(rotx[k])
            Bd = Lp(bd_, GX[k % 2], GY[k // 2], 40)
            Bd._xy = (GX[k % 2], GY[k // 2])
            sx_ = centro(rotx[k])
            rota = [(sx_[0], GY[0])] if k < 2 else [(830, sx_[1]), (830, GY[1])]       # pela altura da própria linha / pelo vão entre as colunas
            self.escreve_voos(Bd, [(rotx[k].f, "a", rota)])
            Bd = cresce(self, Bd, [("i", r"\ \Rightarrow\ "), ("r", fin)], nota=f"M8 C12 (lado {k + 1})")
            lu_ = lin_px([VU.px(*b0), VU.px(*b1)], cor, 4, z=4)
            if k == 0:
                self.play(FadeIn(regU), run_time=0.3)
            voos(self, [(lx_, lu_)], rt=1.2, arco=0.6, livre=(rotx[k], *rotx, *rotu))
            sr_, tu_ = centro(gl(Bd, "r")), centro(rotu[k])
            ru_ = [(830, sr_[1]), (830, 250), (tu_[0], 250)] if k != 3 else [(830, sr_[1]), (830, tu_[1] + 54), (tu_[0], tu_[1] + 54)]   # o v = 1 entra por baixo
            voos(self, [(gl(Bd, "r").copy(), rotu[k].f, ru_)], rt=0.9)    # sobe pelo vão e desce no rótulo
            self.add(rotu[k])
            self.play(FadeIn(rotu[k][0]), run_time=0.3)
        # os cantos conferem; a linha dos vértices na faixa (cada par voa dos rótulos)
        self.gat("os cantos conferem")
        cx = [((1, 0), "(1,0)", 0, -40), ((2, 0), "(2,0)", 34, 28), ((0, -2), "(0,-2)", 56, 20), ((0, -1), "(0,-1)", 52, 18)]   # (2,0) abaixo do eixo
        cu = [((1, 1), "(1,1)", 34, 24), ((2, 2), "(2,2)", 38, -20), ((-2, 2), "(-2,2)", -44, -20), ((-1, 1), "(-1,1)", -40, 24)]
        LV = Lp([("p0", "(1,0)"), ("t0", r"\to"), ("q0", "(1,1)"), ("s0", r";\quad"), ("p1", "(2,0)"), ("t1", r"\to"), ("q1", "(2,2)"), ("s1", r";\quad"),
                 ("p2", "(0,-2)"), ("t2", r"\to"), ("q2", "(-2,2)"), ("s2", r";\quad"), ("p3", "(0,-1)"), ("t3", r"\to"), ("q3", "(-1,1)")], 140, 910, 40)
        LV._xy = (140, 910)
        for k, ((p, s, dx, dy), (q, t, ex, ey)) in enumerate(zip(cx, cu)):
            a, b = VX.px(*p), VU.px(*q)
            pa, pb = ponto_px(*a, BR, 6), ponto_px(*b, BR, 6)
            la = TC(s, a[0] + dx, a[1] + dy, 26, "c")
            lb_ = TC(t, b[0] + ex, b[1] + ey, 26, "c")
            self.play(FadeIn(pa), run_time=0.2)
            self.pena(la)
            self.play(TransformFromCopy(pa, pb, path_arc=0.5), run_time=0.6)
            self.pena(lb_)
            vao = 830                                                  # o vão entre as duas colunas da grade 2 × 2
            cq_ = centro(lb_)
            rq_ = {2: [(cq_[0], 290), (vao, 290), (vao, 910)], 3: [(cq_[0], 690), (vao, 690), (vao, 910)]}.get(k, [(vao, cq_[1]), (vao, 910)])  # por cima / por baixo dos rótulos
            ya_ = 372 if k == 1 else centro(la)[1]                       # o (2,0) fica sob o eixo: desce abaixo dos tiques antes de ir ao vão
            voos(self, [(la.copy(), parte(LV, LV._ix[f"p{k}"], f"p{k}"), [(centro(la)[0], ya_), (vao, ya_), (vao, 910)]),
                        (lb_.copy(), parte(LV, LV._ix[f"q{k}"], f"q{k}"), rq_)], rt=0.8)
            self.pena(parte(LV, LV._ix[f"t{k}"] + (LV._ix[f"s{k}"] if k < 3 else []), f"→{k}"))
        # a tira deitada no plano u, v e B_uv
        self.gat("entra em menos vê")
        vb = 1.55
        tira = tiraH(VU, vb, -vb, vb, h=.08, cor=CVV)
        pe, ps_ = pontos_es(VU, (-vb, vb), (vb, vb))
        self.play(FadeIn(tira), FadeIn(pe), run_time=0.6)
        self.gat("e sai em vê")
        self.play(FadeIn(ps_), run_time=0.4)
        self.gat("essa é a região")
        Bf = Lp([("B", r"B_{uv}:"), ("v", r"\quad\Vc{1}\le\vv\le\Vc{2},"), ("u", r"\qquad\Az{-\vv}\le\uu\le\Co{\vv}")], 0, 995, 44)
        Bf.shift(RIGHT * (960 - larg(Bf) / 2 - esq(Bf)) / 120)
        self.pena(Bf)
        self.marca("14", agora=True)

        # ════ B6-3 · a conta (Q13: a integral montada por mapas em quatro passos) ════
        self.an("B6-3")
        self.limpa_tudo()
        self.secao("O TRAPÉZIO: A CONTA")
        self.fundo(VU8, rt=0.3)
        dU = monta_plano(VU8, AU8, 2.2, 2.6, -2.2, -.2, uv=True)
        regU = poly_px([VU8.px(*p) for p in TRAP_UV], RB, 1.0, z=1)
        eds = VGroup(lin_px([VU8.px(1, 1), VU8.px(2, 2)], CORAL, 4, z=4), lin_px([VU8.px(-2, 2), VU8.px(-1, 1)], AZC, 4, z=4),
                     lin_px([VU8.px(-1, 1), VU8.px(1, 1)], CVV, 3, z=4), lin_px([VU8.px(-2, 2), VU8.px(2, 2)], CVV, 3, z=4))
        entra_plano(self, dU, rt=0.4, extra=[FadeIn(regU), Create(eds)], caneta=False)
        lv1 = TP(r"\Vc{\vv=1}", VU8.px(.5, 1)[0], VU8.px(.5, 1)[1] + 24, 26, "c")
        lv2 = TP(r"\Vc{\vv=2}", VU8.px(.5, 2)[0], VU8.px(.5, 2)[1] - 24, 26, "c")
        lu1 = TP(r"\Az{\uu=-\vv}", VU8.px(-1.5, 1.5)[0] - 20, VU8.px(-1.5, 1.5)[1] + 10, 26, "r")
        lu2 = TP(r"\Co{\uu=\vv}", VU8.px(1.5, 1.5)[0] + 20, VU8.px(1.5, 1.5)[1] + 10, 26, "l")
        self.pena(lv1, lv2, lu1, lu2, lag=0.05, passo=0.03)
        CX3 = 790
        col = self.col = Coluna36(self, CX3, 200)
        col.GAP36 = 20
        self.gat("passo cinco")
        C13a = Lp(LHS[:3] + [("dxy", r"\,\dX\,\dY")], CX3, 0, 40)
        col.poe(C13a)
        C13a._xy = (CX3, centro(C13a)[1])
        self.pena(C13a)
        exA = C13a._ix["ex"]                                           # ( x + y ) / ( x − y ) no expoente: x + y | bar | x − y
        nA, bA, dA_ = nd(C13a, "ex")
        PC13 = [("e", "="), ("I", r"\int_{\Vc{1}}^{\Vc{2}}"), ("Ii", r"\int_{\Az{-\vv}}^{\Co{\vv}}"), ("f", r"e^{\uu/\vv}"), ("c", r"\cdot"),
                ("h", r"\Lm{\dfrac{1}{2}}"), ("d", r"\,\du\,\dv")]

        def mapa13(B):
            lo, hi = idx_lims(B, "I")
            lo2, hi2 = idx_lims(B, "Ii")
            fB = B._ix["f"]                                            # e u / v
            dxy = C13a._ix["dxy"]                                      # d x d y
            iI = [i for i in B._ix["I"] if i not in lo + hi]
            iIi = [i for i in B._ix["Ii"] if i not in lo2 + hi2]
            return [(C13a._ix["ii"][:1], iI + iIi), (C13a._ix["e"], [fB[0]]), (nA, [fB[1]]), (bA, [fB[2]]), (dA_, [fB[3]]),
                    ([dxy[0], dxy[2]], [B._ix["d"][0], B._ix["d"][2]]), ([dxy[1]], [B._ix["d"][1]]), ([dxy[3]], [B._ix["d"][3]])]

        def voos13(B):
            lo, hi = idx_lims(B, "I")
            lo2, hi2 = idx_lims(B, "Ii")
            yC = centro(B)[1]
            via_ = lambda s, extra=(): [*extra, (765, centro(s)[1] if not extra else extra[-1][1]), (765, yC)]
            # os limites saem pelo vão entre o plano e a coluna (x = 765), um por vez; o u = −v passa por baixo do trapézio
            return [(gl(self.chipJ.m, "h"), "h"), (lv1.f, lo, [(765, centro(lv1)[1]), (765, yC)]), (lv2.f, hi, [(765, centro(lv2)[1]), (765, yC)]),
                    (lu1.f, lo2, [(centro(lu1)[0], 640), (765, 640), (765, yC)]), (lu2.f, hi2, [(765, centro(lu2)[1]), (765, yC)])]
        C13 = deriva(self, C13a, PC13, mapa13, col, voos=voos13, x=CX3 + 40, rt=1.4, seq=True,
                     nota="M8 C13 (x + y → u, x − y → v, dx dy → (1/2) du dv; o 1/2 do chip; os limites um por vez)")
        self.gat("o vê está congelado")
        vb = 1.55
        tira = tiraH(VU8, vb, -vb, vb, h=.09, cor=CVV)
        pe, ps_ = pontos_es(VU8, (-vb, vb), (vb, vb))
        self.play(FadeIn(tira), FadeIn(pe), FadeIn(ps_), run_time=0.6)
        # final K11: a placa sai de cima do trapézio — à direita do rótulo u = v, na altura da faixa, ≥ 24 px do trapézio e do rótulo
        lc = rotm([("m", r"\vv"), ("t", "CONGELADO", GEO)], dir_(lu2) + 24, VU8.px(0, vb)[1], 26, "l")
        self.pena(lc)
        self.gat("é vê vezes é elevado")
        p1t, P1 = mixLp("PRIMITIVA EM", [("u", r"\uu:"), ("F", r"\vv\,e^{\uu/\vv}")], CX3, 0, 40)
        y_ = col.y_prox(P1)
        VGroup(p1t, P1).shift(UP * (PX(0, y_)[1] - P1.get_center()[1]))
        col.registra(P1)
        self.pena(p1t, P1, lag=0.2)
        self.gat("deriva e confere")
        self.play(FadeOut(lc), run_time=0.3)                            # a placa já serviu (a linha CONFERE nasce na altura dela)
        self.remove(lc)
        p2t, P2 = mixLp("CONFERE:", [("d", r"\dfrac{d}{d\uu}\left(\vv\,e^{\uu/\vv}\right)"), ("e", r"=\vv\cdot\dfrac{1}{\vv}\,e^{\uu/\vv}"), ("r", r"=e^{\uu/\vv}")],
                        CX3, 0, 40)
        y_ = col.y_prox(P2)
        VGroup(p2t, P2).shift(UP * (PX(0, y_)[1] - P2.get_center()[1]))
        col.registra(P2)
        self.pena(p2t, P2, lag=0.2)
        ck1 = check_px(dir_(P2) + 30, centro(P2)[1], MEN)
        self.play(Create(ck1), run_time=0.4)
        # C14 (mapas M9): ∫_{−v}^{v} e^{u/v} du = [v e^{u/v}]_{u=−v}^{u=v} = v e^{v/v} − v e^{−v/v}
        self.gat("colchete de menos vê")
        Q = Lp([("Ii", r"\int_{\Az{-\vv}}^{\Co{\vv}}"), ("f", r"e^{\uu/\vv}\,\du")], CX3, 0, 40)
        col.poe(Q)
        Q._xy = (CX3, centro(Q)[1])
        self.escreve_voos(Q, [(gl(C13, "Ii"), "Ii"), (gl(C13, "f"), [Q._ix["f"][k] for k in range(len(Q._ix["f"]) - 2)])])
        Q = cresce(self, Q, [("e1", "="), ("lb", r"\Big["), ("F", r"\vv\,e^{\uu/\vv}"), ("rb", r"\Big]"), ("sb", r"_{\uu=\Az{-\vv}}^{\uu=\Co{\vv}}")],
                   voos=lambda B: [(gl(P1, "F").copy(), "F"), (VGroup(*[Q[0][k] for k in idx_lims(Q, "Ii")[0]]).copy(), lims_sb(B, "sb")[0][2:]),
                                   (VGroup(*[Q[0][k] for k in idx_lims(Q, "Ii")[1]]).copy(), lims_sb(B, "sb")[1][2:])], col=col, nota="M9 C14 (colchete)")
        FQ = Q._ix["F"]                                                # v e u / v

        def mapa14(B):
            dd = B._ix["d"]                                            # v e v / v − v e − v / v
            return [("e1", "e"), (FQ, dd[0:5])]                        # final K3: a 2ª cópia (v e^{−v/v}) vem pela caneta
        Q2 = deriva(self, Q, [("e", "="), ("d", r"\vv\,e^{\Co{\vv}/\vv}-\vv\,e^{\Az{-\vv}/\vv}")], mapa14, col, x=eq_x(Q, "e1"), rt=1.1,
                    nota="M9 C14 (G(v) − G(−v))")
        self.gat("fica vê vezes")
        d2 = Q2._ix["d"]
        Q3 = deriva(self, Q2, [("e", "="), ("a", r"\vv\,e-\vv\,e^{-1}")], lambda B: [("e", "e"), (d2[0:2], B._ix["a"][0:2]), ([d2[5]], [B._ix["a"][2]]),
                                                                              (d2[6:8], B._ix["a"][3:5]), (d2[8:9], [B._ix["a"][5]])],
                    col, x=eq_x(Q2, "e"), rt=1.0, gap=48, nota="M9 C14 (v/v = 1)")
        Q3 = cresce(self, Q3, [("e2", "="), ("r", r"\vv\left(e-\dfrac{1}{e}\right)")], voos=lambda B: [(gl(Q3, "a").copy(), "r")], col=col, nota="M9 C14 (= v(e − 1/e))")
        # C15 (mapas M9): a constante sai; [v²/2]₁² → 4/2 − 1/2 → 3/2; (1/2)(e − 1/e)(3/2) → (3/4)(e − 1/e) ≈ 1,763
        self.gat("por fora um meio")
        # v2 (margem): PRIMITIVA EM e CONFERE já serviram e saem; o C14 sobe (o C15 inteiro cabe acima de y = 1032)
        sv = [p1t, P1, p2t, P2, ck1]
        dyq = pxof(Q.get_top())[1] - min(pxof(m.get_top())[1] for m in (p1t, P1))
        self.play(*[FadeOut(m) for m in sv], run_time=0.4)  # final K12: troca de página em dois tempos (sai, depois sobe)
        self.play(*[m.animate.shift(UP * dyq / 120) for m in (Q, Q2, Q3)], run_time=0.6)
        self.remove(*sv)
        col.tira(P1, P2)
        R1 = Lp([("h", r"\Lm{\dfrac{1}{2}}"), ("I", r"\int_{\Vc{1}}^{\Vc{2}}"), ("v", r"\vv"), ("k", r"\left(e-\dfrac{1}{e}\right)"), ("d", r"\dv")], CX3, 0, 40)
        col.poe(R1)
        R1._xy = (CX3, centro(R1)[1])
        rq = Q3._ix["r"]
        self.escreve_voos(R1, [(gl(C13, "h"), "h"), (gl(C13, "I"), "I"), (VGroup(*[Q3[0][k] for k in rq]), ["v", "k"])])
        R1 = cresce(self, R1, [("e", "="), ("h2", r"\Lm{\dfrac{1}{2}}"), ("k2", r"\left(e-\dfrac{1}{e}\right)"), ("I2", r"\int_{\Vc{1}}^{\Vc{2}}"), ("v2", r"\vv\,\dv")],
                    voos=lambda B: [(gl(R1, "h").copy(), "h2"), (gl(R1, "k").copy(), "k2"), (gl(R1, "I").copy(), "I2"), (VGroup(gl(R1, "v"), gl(R1, "d")).copy(), "v2")],
                    col=col, nota="M9 C15 (a constante sai da integral)")
        self.gat("a primitiva é vê ao quadrado")
        S2 = Lp([("I", r"\int_{\Vc{1}}^{\Vc{2}}"), ("v", r"\vv\,\dv")], CX3, 0, 40)
        col.poe(S2)
        S2._xy = (CX3, centro(S2)[1])
        self.escreve_voos(S2, [(gl(R1, "I2"), "I"), (gl(R1, "v2"), "v")])
        S2 = cresce(self, S2, [("e1", "="), ("lb", r"\Big["), ("F", r"\dfrac{\vv^2}{2}"), ("rb", r"\Big]"), ("sb", r"_{\Vc{1}}^{\Vc{2}}")],
                    voos=lambda B: [(VGroup(*[S2[0][k] for k in idx_lims(S2, "I")[0]]).copy(), [B._ix["sb"][0]]),
                                    (VGroup(*[S2[0][k] for k in idx_lims(S2, "I")[1]]).copy(), [B._ix["sb"][1]])], col=col, nota="M9 C15 (colchete v²/2)")
        self.gat("quatro sobre dois menos")
        S2 = cresce(self, S2, [("e2", "="), ("d", r"\dfrac{4}{2}-\dfrac{1}{2}")], col=col, nota="M9 C15 (G(2) − G(1))")
        S2 = cresce(self, S2, [("e3", "="), ("r", r"\dfrac{3}{2}")], voos=lambda B: [(gl(S2, "d").copy(), "r")], col=col, nota="M9 C15 (= 3/2)")
        self.gat("um meio vezes três meios")
        T3 = Lp([("e", "="), ("h", r"\Lm{\dfrac{1}{2}}"), ("k", r"\left(e-\dfrac{1}{e}\right)"), ("t", r"\left(\dfrac{3}{2}\right)")], 0, 0, 40)
        col.poe(T3, x=eq_x(R1, "e"))
        T3._xy = (esq(T3), centro(T3)[1])
        self.escreve_voos(T3, [(gl(R1, "h2"), "h"), (gl(R1, "k2"), "k"), (gl(S2, "r"), [T3._ix["t"][k] for k in range(1, len(T3._ix["t"]) - 1)])])
        T3 = cresce(self, T3, [("e2", "="), ("r", r"\dfrac{3}{4}\left(e-\dfrac{1}{e}\right)")],
                    voos=lambda B: [(VGroup(gl(T3, "h"), gl(T3, "t")).copy(), B._ix["r"][:3]), (gl(T3, "k").copy(), B._ix["r"][3:])], col=col,
                    nota="M9 C15 (= 3/4 (e − 1/e))")
        self.gat("um vírgula setenta e seis")
        T3 = cresce(self, T3, [("ap", r"\approx"), ("n", r"1{,}763")], col=col, nota="C15 (≈ 1,763, o exato primeiro)")
        self.marca("15", agora=True)

        # ════ B6-4 · a conferência (Q14: as células 1 e 2 inteiras; as duas pontas viram uma célula; ½ + ½ = 1 e então o 3) ════
        self.an("B6-4")
        self.secao("A CONFERÊNCIA")
        sai = [m for m in self.snap() if pxof(m.get_center())[0] > 760 or m in (tira, pe, ps_, lc, lv1, lv2, lu1, lu2)]   # os rótulos das arestas já serviram
        self.play(*[FadeOut(m) for m in sai], run_time=0.5)
        self.remove(*sai)
        col = self.col = Coluna36(self, 1120, 262)
        col.GAP36 = 26
        self.gat("com f igual a um")
        c1 = celula(VU8, ID, -1, 0, 1, 2, n=3, wb=2)
        c2 = celula(VU8, ID, 0, 1, 1, 2, n=3, wb=2)
        t1 = poligono(VU8, [(1, 1), (2, 2), (1, 2)], mixh(BG_, CHAPA, .9), 1.0, MALHA, 2, z=3)
        t2 = poligono(VU8, [(-1, 1), (-2, 2), (-1, 2)], mixh(BG_, CHAPA, .9), 1.0, MALHA, 2, z=3)
        entra_cel(self, c1, c2, rt=0.8)
        n1 = T("1", VU8.px(-.5, 1.5)[0], VU8.px(-.5, 1.5)[1] + 12, 32, "center")
        n2 = T("2", VU8.px(.5, 1.5)[0], VU8.px(.5, 1.5)[1] + 12, 32, "center")
        self.pena(n1, n2, lag=0.3)
        # as duas pontas (triângulos de área ½) acendem juntas com ½; a da esquerda voa e encaixa na da direita: uma célula inteira
        self.play(FadeIn(t1[0]), Create(t1[1]), FadeIn(t2[0]), Create(t2[1]), run_time=0.6)
        h1 = TC(r"\dfrac{1}{2}", *VU8.px(1.36, 1.68), 26, "c")
        h2 = TC(r"\dfrac{1}{2}", *VU8.px(-1.36, 1.68), 26, "c")
        self.pena(h1, h2, lag=0.1)
        t2b = poligono(VU8, [(1, 1), (2, 1), (2, 2)], mixh(BG_, CHAPA, .9), 1.0, MALHA, 2, z=3)        # o encaixe: a ponta completa o quadrado
        voos(self, [(t2, t2b)], rt=1.0, livre=(h1, h2, n1, n2))
        self.play(FadeOut(t2), run_time=0.2)
        self.remove(t2)
        hs = Lp([("a", r"\dfrac{1}{2}"), ("p", "+"), ("b", r"\dfrac{1}{2}"), ("e", "="), ("r", "1")], 0, 0, 30)
        hs.move_to(PX(*VU8.px(2.0, 2.45)))
        self.escreve_voos(hs, [(h2, "a"), (h1, "b")], depois=["e", "r"])
        n3 = T("3", VU8.px(-1.6, .55)[0], VU8.px(-1.6, .55)[1], 34, "center", LIMA)
        tc3 = T("CÉLULAS", VU8.px(-1.6, .55)[0] + 26, VU8.px(-1.6, .55)[1], 30, "left", LIMA)
        voa(self, VGroup(n1, n2, gl(hs, "r")).copy(), n3, rt=0.9, arco=0.0, livre=(c1, c2, t1, t2b))
        self.pena(tc3)
        # C16 (mapas M9): PLANO u, v: ∫₁² (v − (−v)) dv = ∫₁² 2v dv = [v²]₁² = 2² − 1² = 4 − 1 = 3
        self.gat("comprimento dois vê")
        p0, F1 = mixLp("PLANO", [("uv", r"\uu,\vv:"), ("I", r"\int_{\Vc{1}}^{\Vc{2}}"), ("p", r"\left(\Co{\vv}-(\Az{-\vv})\right)"), ("d", r"\dv")], 1120, 0, 40)
        y_ = col.y_prox(F1)
        VGroup(p0, F1).shift(UP * (PX(0, y_)[1] - F1.get_center()[1]))
        F1._xy = (esq(F1), centro(F1)[1])
        col.registra(F1)
        self.pena(p0, F1, lag=0.1, passo=0.04)
        pp = F1._ix["p"]                                               # ( v − ( − v ) )
        F2 = deriva(self, F1, [("e", "="), ("I", r"\int_{\Vc{1}}^{\Vc{2}}"), ("t", r"2\vv\,\dv")],
                    lambda B: [("I", "I"), ([pp[1], pp[5]], [B._ix["t"][1]]), (F1._ix["d"], B._ix["t"][2:4])], col, x=esq(F1) + 60, rt=1.1,
                    nota="M9 C16 (v − (−v) → 2v)")
        self.gat("dá vê ao quadrado")
        F3 = deriva(self, F2, [("e", "="), ("lb", r"\Big["), ("F", r"\vv^2"), ("rb", r"\Big]"), ("sb", r"_{\Vc{1}}^{\Vc{2}}")],
                    lambda B: [("e", "e"), ([F2._ix["t"][1]], [B._ix["F"][0]]), (idx_lims(F2, "I")[0], [B._ix["sb"][0]]), (idx_lims(F2, "I")[1], [B._ix["sb"][1]])],
                    col, x=eq_x(F2, "e"), rt=1.0, nota="M9 C16 (∫ 2v → [v²])")
        self.gat("quatro menos um")
        F3 = cresce(self, F3, [("e2", "="), ("g", r"2^2-1^2")], voos=lambda B: [(VGroup(F3[0][B._ix["sb"][1]] if False else F3[0][F3._ix["sb"][1]]).copy(), [B._ix["g"][0]]),
                                                                          (VGroup(F3[0][F3._ix["sb"][0]]).copy(), [B._ix["g"][3]])],
                    col=col, nota="M9 C16 (G(2) − G(1))")
        F3 = cresce(self, F3, [("e3", "="), ("d", "4-1")], voos=lambda B: [(gl(F3, "g").copy(), "d")], col=col, nota="M9 C16 (2² − 1² → 4 − 1)")
        F3 = cresce(self, F3, [("e4", "="), ("r", "3")], voos=lambda B: [(VGroup(gl(F3, "d"), n3).copy(), "r")], col=col, nota="M9 C16 (= 3, as 3 células)")
        self.gat("vezes o fator")
        F4 = Lp([("t", "3"), ("c", r"\cdot"), ("h", r"\Lm{\dfrac{1}{2}}"), ("e", "="), ("r", r"\dfrac{3}{2}")], 1120, 0, 40)
        col.poe(F4)
        F4._xy = (1120, centro(F4)[1])
        self.escreve_voos(F4, [(gl(F3, "r"), "t"), (gl(self.chipJ.m, "h"), "h")], depois=["e", "r"], rt=0.6)
        self.gat("no papel o trapézio")
        dX9 = monta_plano(VX9, AX9, 2.3, .35, -.25, -2.3, ticks=[("x", 2, r"\Am{2}"), ("y", -2, r"\Mg{-2}")])
        g_ = poligono(VX9, [(0, 0), (2, 0), (0, -2)], mixh(BG_, GEO, .25), 1.0, GEO, 2, z=1)
        p_ = poly_px([VX9.px(*p) for p in ((0, 0), (1, 0), (0, -1))], mixh(BG_, AL, .35), 1.0, z=2)
        pb_ = lin_px([VX9.px(*p) for p in ((0, 0), (1, 0), (0, -1), (0, 0))], AL, 2, dash=(6, 6), z=3)
        entra_plano(self, dX9, rt=0.4, extra=[FadeIn(g_[0]), Create(g_[1])], caneta=False)
        self.play(FadeIn(p_), Create(pb_), run_time=0.5)
        # a origem nos triângulos: 2·2/2 escrito no grande, 1·1/2 no pequeno; voam para a coluna
        lg_ = TC(r"\Ge{\dfrac{2\cdot 2}{2}}", *VX9.px(1.15, -1.25), 26, "c")
        lp_ = TC(r"\Al{\dfrac{1\cdot 1}{2}}", *VX9.px(.3, -.32), 26, "c")
        self.pena(lg_, lp_, lag=0.2)
        f3t, F5 = mixLp("PAPEL:", [("g", r"\dfrac{2\cdot 2}{2}"), ("m", "-"), ("p", r"\dfrac{1\cdot 1}{2}")], 1120, 0, 40)
        y_ = col.y_prox(F5)
        VGroup(f3t, F5).shift(UP * (PX(0, y_)[1] - F5.get_center()[1]))
        F5._xy = (esq(F5), centro(F5)[1])
        col.registra(F5)
        yF5 = centro(F5)[1]
        self.escreve_voos(F5, [(lg_, "g"), (lp_, "p")])                  # final: o desvio automático escolhe o caminho livre (sem tique nem rótulo)
        self.pena(f3t)
        F5 = cresce(self, F5, [("e", "="), ("d", r"2-\dfrac{1}{2}")], voos=lambda B: [(gl(F5, "g").copy(), [B._ix["d"][0]]),
                                                                              (gl(F5, "p").copy(), B._ix["d"][2:])], col=col, nota="M9 C16 (2·2/2 − 1·1/2 → 2 − 1/2)")
        self.gat("três meios também")
        F5 = cresce(self, F5, [("e2", "="), ("r", r"\dfrac{3}{2}")], voos=lambda B: [(gl(F5, "d").copy(), "r")], col=col, nota="M9 C16 (= 3/2)")
        ck = check_px(dir_(F5) + 30, centro(F5)[1], MEN)
        self.play(Create(ck), run_time=0.4)
        self.gat("é o jacobiano")
        f4 = Lp([("h", r"\Lm{\dfrac{1}{2}}")], 1120, 0, 48)
        col.poe(f4, gap=36)
        tj = T("= O JACOBIANO", dir_(f4) + 14, centro(f4)[1] + 10, 34, "left", LIMA)
        voa(self, gl(F4, "h").copy(), f4, rt=0.9)
        self.pena(tj)
        self.gat("a troca não fez mágica")
        ps, pl = phi_seta(560, 760, 330)
        self.play(Create(ps), run_time=0.8)
        self.pena(pl)
        self.marca("B6-4")
        if self._aid is not None:
            self._fecha(antes=0.7)
        ch = self.chipJ
        self.chipJ = None
        self.play(FadeOut(ch), run_time=0.35)                      # o chip sai no fim do B6
        self.remove(ch)
        self.sai_fim()
