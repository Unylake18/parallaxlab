"""Lote PX0 (v2): X0 o disco furado e X1 a placa com furo. G23: cada símbolo da conta sai de um rótulo do desenho (TransformFromCopy); a
substituição é um glyph map símbolo → número numa linha nova; os passos descem pela Pilha (G25); resultado em PANEL. G27: os dados nascem fora
do objeto (cotas com linhas de chamada). G22: massa negativa = fantasma tracejado por cima do corpo inteiro.
X0: R = 1 m, furo r = 0,5 m em x = +0,25 m → X = −1/12 m. X1: placa de 40 cm, furo r = 10 cm em (8; 8) cm → X = Y = −1,95 cm (2,76 cm).
v3: o disco já está na tela no quadro 0 (nasceu no fim do A4, lote PH); sem o selo DESAFIO; rótulos de massa DENTRO dos próprios corpos (sem linha
de chamada); "O" à esquerda do ponto; cotas com linhas de chamada; filhas da Pilha alinham o "=" (P2)."""
from prob2 import *  # noqa: F401,F403

F = lambda a, b: rf"\tfrac{{{a}}}{{{b}}}"


def disco_furado(C, R, c_furo, r_furo):
    if r_furo < 0.005:
        return aco(Circle(radius=R).move_to(C), 2.0)
    return aco(Difference(Circle(radius=R).move_to(C), Circle(radius=r_furo).move_to(c_furo)), 2.0)


def placa_furada(C, L, c_furo, r_furo):
    if r_furo < 0.005:
        return aco(Square(L).move_to(C), 2.0)
    return aco(Difference(Square(L).move_to(C), Circle(radius=r_furo).move_to(c_furo)), 2.0)


def miniatura_x0():
    """A miniatura do disco furado (nasce no fim do A4, no lote PH, e cresce no X0-1): sobreposição de 0,5 s entre os lotes (v3 §9)."""
    K, C = 2.3, P3(-3.8, -0.35)
    R, r, d = K * 1.0, K * 0.5, K * 0.25
    cf = C + P3(d, 0)
    dc = disco_furado(C, R, cf, r)
    borda = DashedVMobject(Circle(radius=r).move_to(cf).set_stroke(WHITE_, 2, opacity=0.75), num_dashes=30, dashed_ratio=0.55).set_z_index(6)
    return VGroup(dc, borda).scale(0.25).move_to(P3(-3.8, -0.35))


class LoteX01(Prob2):
    def construct(self):
        self.setup_base(cap="PROBLEMA 1 · O DISCO FURADO")
        self.x0()
        self.x1()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    # ════════════════════════════════════════ X0 ════════════════════════════════════════
    def x0(self):
        K, C = 2.3, P3(-3.8, -0.35)
        R, r, d = K * 1.0, K * 0.5, K * 0.25
        cf = C + P3(d, 0)
        self.an("X0-1")
        dc = disco_furado(C, R, cf, r)
        borda = DashedVMobject(Circle(radius=r).move_to(cf).set_stroke(WHITE_, 2, opacity=0.75), num_dashes=30, dashed_ratio=0.55).set_z_index(6)
        mini = miniatura_x0()
        eixo = VGroup(Line(C + P3(-R - 0.35, 0), C + P3(R + 0.45, 0)).set_stroke(GEO, 2, opacity=0.8))
        for xm in (-1, 1):
            eixo.add(Line(C + P3(K * xm, -0.09), C + P3(K * xm, 0.09)).set_stroke(GEO, 2))
        eixo.set_z_index(3)
        self.add(mini)                                                                              # quadro 0: a miniatura que nasceu no fim do A4
        self.chip(1)
        self.pede("TIRAR MASSA")                                                                      # v5 G32: o selo entra já no começo (a direita nunca fica vazia)
        self.play(ReplacementTransform(mini, VGroup(dc, borda)), FadeIn(eixo), run_time=1.1)          # a miniatura cresce até o disco
        self.add(dc, borda)
        nx = self.rotulo(mtex("x", GEO, 36), C + P3(R + 0.45, 0), lados=(RIGHT, UR, DR), buffs=(0.22, 0.3))
        yc = C[1] - r - 0.3                                                        # cota 0,25 m abaixo do eixo, abaixo do furo (dentro do disco)
        oo = VGroup(Dot(C, radius=0.05, color=WHITE_))
        o_lab = mtex("O", GEO, 36).next_to(C, DR, buff=0.2)                      # embaixo à direita do ponto (o ⊕ nasce à esquerda)
        self.play(FadeIn(nx), FadeIn(oo), FadeIn(o_lab), run_time=0.5)
        self.ate(0.18)
        pR = C + R * P3(math.cos(2.45), math.sin(2.45))
        rR = Line(C, pR).set_stroke(GEO, 2.4)
        lR = self.rotulo(rot("R = 1 m", 30, GEO), pR, lados=(UL, LEFT, UP))
        self.play(Create(rR), FadeIn(lR), run_time=0.6)
        pr = cf + r * P3(math.cos(-PI / 4), math.sin(-PI / 4))                     # o raio desce para a direita: o rótulo fica em cima
        rr = Line(cf, pr).set_stroke(GEO, 2.4)
        lr = rot("r = 0,5 m", 24, GEO).move_to(cf + P3(0.0, 0.5))                 # dentro do furo, em cima do centro
        cr = VGroup()
        self.ate(0.42)
        self.play(Create(rr), FadeIn(lr), Create(cr), run_time=0.6)
        cd = VGroup(tracejado(C + P3(0, -0.14), P3(C[0], yc + 0.13), WHITE_, 1.4, 0.5), tracejado(cf + P3(0, -0.65), P3(cf[0], yc + 0.13), WHITE_, 1.4, 0.5),
                    Dot(cf, radius=0.045, color=GEO))
        c25 = cota(C[0], cf[0], yc, rot("0,25 m", 28, GEO), lado=DOWN, buff=0.16)
        fd25 = RoundedRectangle(corner_radius=0.06, width=c25[1].width + 0.2, height=c25[1].height + 0.12).move_to(c25[1]).set_fill(PANEL, 0.85).set_stroke(width=0)
        fd25._fundo = fd25._caixa = True                                        # contraste do rótulo sobre o disco claro
        c25 = VGroup(c25[0], VGroup(fd25, c25[1]))
        self.ate(0.62)
        self.play(FadeIn(cd), FadeIn(c25), run_time=0.6)
        self.foco = dc
        self.ate(0.97)
        # ── X0-2 ──
        self.an("X0-2")
        L1, l1 = M("r", "=", F("R", "2"), r"\ \Rightarrow\ ", r"A_{furo}", "=", F("1", "4"), r"\,A_{disco}", size=48, cores={0: GEO, 2: GEO, 4: GEO, 7: GEO})
        self.pilha.poe(L1)
        self.voa([(lr, mp(L1, l1, [0])), (lR, mp(L1, l1, [2]))], extra=[FadeIn(mp(L1, l1, [1, 3, 4, 5, 6, 7]))], rt=1.3)
        self.foco = L1
        cheio = aco(Circle(radius=R).move_to(C), 2.0)
        self.ate(0.17)
        self.play(FadeOut(dc), FadeIn(cheio), FadeOut(borda), FadeOut(rr), FadeOut(rR), FadeOut(lR), FadeOut(cr), FadeOut(lr), run_time=0.9)
        m1 = VGroup(VGroup(txt("MASSA", 28), rot("1", 30)).arrange(RIGHT, buff=0.14).move_to(C + P3(-1.0, 1.25)))      # dentro do disco cheio
        g1 = VGroup()
        self.ate(0.24)
        self.play(FadeIn(m1), run_time=0.7)
        fant = fantasma_circ(cf, r)
        pf = Dot(cf, radius=0.06, color=mix(MAG, 0.2)).set_z_index(10)
        m2 = VGroup(txt("MASSA", 24), rot("−¼", 28)).arrange(DOWN, buff=0.06).move_to(cf + P3(-0.1, 0.55))          # dentro do furo, fonte menor
        g2 = VGroup()
        self.ate(0.34)
        self.play(Create(fant), FadeIn(m2), FadeIn(pf), run_time=1.0)
        num = ["m_1", r"\,x_1", "+", "m_2", r"\,x_2"]
        den = ["m_1", "+", "m_2"]
        L2, l2 = eqf(["X", "="], num, den, size=48, cores={("pre", 0): CMC, ("num", 1): GEO, ("num", 4): GEO})
        self.pilha.poe(L2)
        N_, D_ = l2["num"], l2["den"]
        self.ate(0.42)
        self.voa([(m1[0][1], gl(L2, N_[0])), (o_lab[0], gl(L2, N_[1])), (m2[1], gl(L2, N_[3])), (c25[1][1], gl(L2, N_[4])), (m1[0][1], gl(L2, D_[0])),
                  (m2[1], gl(L2, D_[2]))], extra=[FadeIn(gl(L2, sum(l2["pre"], []) + N_[2] + l2["bar"] + D_[1]))], rt=1.4)
        L3, l3 = eqf(["="], ["1", r"\cdot", "0", "+", r"(-\tfrac{1}{4})", r"\cdot", r"0{,}25"], ["1", "-", F("1", "4")], size=48,
                     cores={("num", 2): GEO, ("num", 6): GEO})
        self.pilha.poe(L3)
        self.ate(0.52)
        n3, d3 = l3["num"], l3["den"]
        self.voa([(m1[0][1], gl(L3, n3[0])), (o_lab[0], gl(L3, n3[2])), (m2[1], gl(L3, n3[4])), (c25[1][1][:4], gl(L3, n3[6])), (m1[0][1], gl(L3, d3[0])),
                  (m2[1][1:], gl(L3, d3[2]))], extra=[FadeIn(gl(L3, l3["pre"][0] + n3[1] + n3[3] + n3[5] + l3["bar"] + d3[1]))], rt=1.2, origem=False)   # v4 #8
        L4, l4 = eqf(["="], [r"-\tfrac{1}{16}"], [F("3", "4")], size=48)
        self.pilha.poe(L4)
        self.ate(0.62)
        self.passo(L3, L4, (l3["pre"][0], l4["pre"][0]), (sum(l3["num"], []), l4["num"][0]), (l3["bar"], l4["bar"]), (sum(l3["den"], []), l4["den"][0]), rt=1.3)
        L5, l5 = M("X", "=", r"-\tfrac{1}{12}\ \mathrm{m}", r"\approx", r"-8{,}3\ \mathrm{cm}", size=48, cores={0: CMC, 2: GEO, 4: GEO})
        L5b = caixa_l(L5, CMC)
        self.pilha.poe(L5b)
        self.ate(0.7)
        self.passo(L4, L5, (l4["pre"][0], J(l5, 1)), (sum(l4["num"], []) + l4["bar"] + sum(l4["den"], []), J(l5, 2)), rt=1.2, extra=[FadeIn(L5b[0])],
                   origem=False)                                                         # −1/12 m é o valor calculado (não troca de símbolo)
        X_ = C + P3(-K / 12, 0)
        cm = marcador_cm(X_, r=0.17)
        self.play(FadeIn(cm, scale=1.5), oo.animate.set_opacity(0.3), run_time=0.7)
        self.reg("x0", cm=cm.get_center(), esperado=C + P3(-K / 12, 0))
        self.ate(0.83)
        nt = cartao("NINGUÉM TEM MASSA NEGATIVA:", "É SÓ A CONTA DE TIRAR MATERIAL", size=28)
        self.pilha.poe(nt)
        self.play(FadeIn(nt, shift=0.1 * UP), run_time=0.7)
        self.foco = nt
        self.ate(0.97)
        # ── X0-3 ──
        self.an("X0-3")
        cx_ = ValueTracker(d)

        def disco_vivo():
            c = C + P3(cx_.get_value(), 0)
            X = -(1 / 4) * (cx_.get_value() / K) / (3 / 4)
            g = VGroup(disco_furado(C, R, c, r), DashedVMobject(Circle(radius=r).move_to(c).set_stroke(WHITE_, 2, opacity=0.75), num_dashes=30).set_z_index(6),
                       marcador_cm(C + P3(K * X, 0), r=0.17))
            self.reg("x0", cm=C + P3(K * X, 0), esperado=C + P3(-cx_.get_value() / 3, 0))
            return g
        dv = vivo(disco_vivo)
        velhos = [cheio, fant, pf, m1, m2, cm, cd, c25, oo, o_lab]
        self._em_troca = True
        self.play(*[FadeOut(m) for m in velhos], run_time=0.35)                             # sai o disco cheio e só então entra o disco que anda
        self.remove(*velhos)
        self.play(FadeIn(dv), run_time=0.35)
        self._em_troca = False
        self.pilha.limpa()
        self.confere(["FURO NO MEIO → ⊕ NO MEIO"])
        self.foco = None
        self.play(cx_.animate.set_value(0.0), run_time=2.2)
        Z_, z_ = M("X", "=", "0", size=52, cores={0: CMC})
        self.pilha.poe(Z_)
        self.play(FadeIn(Z_), run_time=0.6)
        self.foco = Z_
        self.ate(0.5)
        Z6, z6 = M("X", "=", r"-\tfrac{1}{12}\ \mathrm{m}", r"\approx", r"-8{,}3\ \mathrm{cm}", size=52, cores={0: CMC, 2: GEO, 4: GEO})
        Z6b = caixa_l(Z6, CMC)
        self.pilha.tira(Z_)
        self.pilha.poe(Z6b)
        self.play(cx_.animate.set_value(d), AnimationGroup(FadeOut(Z_, run_time=0.6), FadeIn(Z6b, run_time=0.8), lag_ratio=1.0), run_time=1.6)   # v5 G33: o furo volta e o ⊕ anda junto
        self.remove(Z_)
        self.foco = Z6b
        self.ate(0.62)
        self.dica18("O ⊕ FOGE DO FURO")
        lado = Arrow(C + P3(-0.25, 0.45), C + P3(-0.95, 0.45), buff=0, stroke_width=5, color=GEO, max_tip_length_to_length_ratio=0.35)
        self.play(Create(lado), run_time=0.6)
        self.foco = lado
        self.ate(0.97)

    # ════════════════════════════════════════ X1 ════════════════════════════════════════
    def x1(self):
        k, C = 0.115, P3(-3.8, -0.35)
        S = 40 * k
        h = S / 2
        cf = C + P3(8 * k, 8 * k)
        rf = 10 * k
        self.an("X1-1")
        velhos = self.snap()
        self.pilha.linhas = []
        self.secao("PROBLEMA 2 · A PLACA COM FURO")
        pl = placa_furada(C, S, cf, rf)
        borda = DashedVMobject(Circle(radius=rf).move_to(cf).set_stroke(WHITE_, 2, opacity=0.75), num_dashes=30, dashed_ratio=0.55).set_z_index(6)
        ax = VGroup(Line(C + P3(-h - 0.2, 0), C + P3(h + 0.15, 0)).set_stroke(GEO, 2, opacity=0.85), Line(C + P3(0, -h - 0.15), C + P3(0, h + 0.2)).set_stroke(GEO, 2, opacity=0.85))
        for c_ in range(-20, 21, 10):
            ax.add(Line(C + P3(c_ * k, -0.08), C + P3(c_ * k, 0.08)).set_stroke(GEO, 2), Line(C + P3(-0.08, c_ * k), C + P3(0.08, c_ * k)).set_stroke(GEO, 2))
        ax.set_z_index(3)
        self.troca(velhos, FadeIn(pl), Create(borda), FadeIn(ax), seq=True)
        self.s1 = None
        self.chip(1)
        self.pede("TIRAR MASSA + SIMETRIA")                                               # v5 G32: o selo entra logo depois do chip (CONTA nunca vazia > 1 s)
        nx = self.rotulo(mtex("x", GEO, 36), C + P3(h + 0.15, 0), lados=(DR, DOWN), buffs=(0.22, 0.3))
        ny_ = mtex("y", GEO, 36).next_to(C + P3(0, h + 0.2), RIGHT, buff=0.18)
        ny_.shift((C[1] + h + 0.18 - ny_.get_bottom()[1]) * UP)                                 # à direita do eixo, entre a placa e o chip
        ny = VGroup(ny_)
        self.play(FadeIn(nx), FadeIn(ny), run_time=0.4)
        c40 = VGroup(cota_v(C[0] - h - 0.3, C[1] - h, C[1] + h), rot("40 cm", 30, GEO).rotate(PI / 2).next_to(P3(C[0] - h - 0.3, C[1]), LEFT, buff=0.12))
        self.ate(0.12)
        self.play(FadeIn(c40), run_time=0.6)
        pr_ = cf + rf * P3(math.cos(-0.4), math.sin(-0.4))                         # o raio desce para a direita (o "10 cm" fica em cima, livre)
        lr = rot("10 cm", 24, GEO).move_to(cf + P3(0.3, 0.45))                    # dentro do furo, em cima à direita (nenhuma linha passa ali)
        crr = VGroup(Line(cf, pr_).set_stroke(GEO, 2.4), Dot(cf, radius=0.045, color=GEO), VGroup())
        self.ate(0.25)
        self.play(FadeIn(crr), FadeIn(lr), run_time=0.6)
        yb = C[1] - h - 0.35
        cx8 = VGroup(cota(C[0], cf[0], yb, rot("8 cm", 30, GEO), lado=DOWN, buff=0.2), tracejado(cf, P3(cf[0], yb + 0.14), WHITE_, 1.4, 0.5),
                     tracejado(C, P3(C[0], yb + 0.14), WHITE_, 1.4, 0.35))
        xr = C[0] + h + 0.35
        cy8 = VGroup(cota_v(xr, C[1], cf[1]), rot("8 cm", 30, GEO).next_to(P3(xr, (C[1] + cf[1]) / 2), RIGHT, buff=0.22),
                     tracejado(cf, P3(xr - 0.14, cf[1]), WHITE_, 1.4, 0.5))
        self.ate(0.38)
        self.play(FadeIn(cx8), run_time=0.6)
        self.play(FadeIn(cy8), run_time=0.6)
        self.ate(0.72)
        self.hip("ESPESSURA UNIFORME → MASSA ∝ ÁREA")
        self.foco = self.s1                                                          # o destaque pulsa o selo (a placa crescendo encostaria no y)
        self.ate(0.97)
        # ── X1-2 ──
        self.an("X1-2")
        self.foco = pl                                                                     # v7: nos primeiros segundos ("procura a simetria") a placa é o destaque
        d0_, d1_ = C + P3(-h - 0.15, -h - 0.15), C + P3(h + 0.15, h + 0.15)
        partes_d = [tracejado(d0_ + (d1_ - d0_) * k / 4, d0_ + (d1_ - d0_) * (k + 1) / 4, WHITE_, 2.6, 0.8, dash=0.12).set_z_index(8) for k in range(4)]
        diag = VGroup(*partes_d)                                                           # v7: a diagonal nasce em 4 trechos, cada um com a placa pulsando
        self.gat("a diagonal que passa")
        self.play(FadeOut(lr), run_time=0.3)                                                # o "10 cm" sai antes da diagonal passar por ele
        for k_ in range(4):                                                                 # v7: a diagonal se desenha durante "a diagonal que passa pelo centro…"
            self.pulsa([pl], 0.75, Create(partes_d[k_], rate_func=linear))
        self.gat("duas metades iguais")
        esp = VGroup(pl, borda).copy()
        self.remove(pl, borda)
        self.add(esp)
        self.play(Rotate(esp, PI, axis=np.array([1.0, 1.0, 0.0]), about_point=C), run_time=2.4)     # v7: o espelhamento em "duas metades iguais, espelhadas"
        self.remove(esp)
        self.add(pl, borda)
        S1, s1_ = M("X", "=", "Y", size=52, cores={0: CMC, 2: CMC})
        sim = linha_m("SIMETRIA", MathTex(r"\Rightarrow", font_size=48), S1)
        sim[1]._partes = [(r"\Rightarrow", WHITE_)]
        self.pilha.poe(sim)
        self.gat("nessa diagonal")
        self._voando_raiz = [S1]
        self.play(FadeIn(sim[0]), FadeIn(sim[1]), TransformFromCopy(diag, S1), run_time=0.9)
        self._voando_raiz = []
        self.foco = sim
        self.ate(0.97)
        # ── X1-3 ──
        self.an("X1-3")
        cheio = aco(Square(S).move_to(C), 2.0)
        fant = fantasma_circ(cf, rf)
        pc = Dot(C, radius=0.06, color=GEO).set_z_index(10)
        pf = Dot(cf, radius=0.06, color=mix(MAG, 0.2)).set_z_index(10)
        self.play(FadeOut(pl), FadeOut(borda), FadeIn(cheio), Create(fant), FadeOut(diag), FadeOut(crr[0]), run_time=0.8)
        A1, a1 = M(r"A_\square", "=", r"40^2", "=", r"1600\ \mathrm{cm^2}", size=48, cores={0: GEO, 2: GEO, 4: GEO})
        A2, a2 = M(r"A_\circ", "=", r"\pi\cdot 10^2", "=", r"100\pi", r"\approx", r"314\ \mathrm{cm^2}", size=46, cores={0: GEO, 2: GEO, 4: GEO, 6: GEO})
        self.pilha.poe(A1)
        self.ate(0.06)
        self.voa([(c40[1], mp(A1, a1, [2]))], extra=[FadeIn(mp(A1, a1, [0, 1, 3, 4])), FadeIn(pc)], rt=1.1)
        self.pilha.poe(A2)
        self.ate(0.2)
        self.voa([(lr.copy().set_opacity(1.0), mp(A2, a2, [2]))], extra=[FadeIn(mp(A2, a2, [0, 1, 3, 4, 5, 6])), FadeIn(pf)], rt=1.1)
        ma = VGroup(txt("MASSA", 24), MathTex(r"\propto 1600", font_size=36, color=WHITE_)).arrange(DOWN, buff=0.1)
        ma[1]._partes = [(r"\propto 1600", WHITE_)]
        mb = VGroup(txt("MASSA", 24), MathTex(r"\propto -100\pi", font_size=36, color=WHITE_)).arrange(DOWN, buff=0.1)
        mb[1]._partes = [(r"\propto -100\pi", WHITE_)]
        ma.move_to(C + P3(-h + 0.95, h - 0.75))                                    # canto superior esquerdo da placa (a diagonal tracejada do d passa pelo inferior esquerdo)
        mb.move_to(cf + P3(0.05, 0.52))                                            # dentro do furo, acima da linha de 8 cm, longe do eixo y
        ga = gb = VGroup()
        self.ate(0.32)
        self.voa([(mp(A1, a1, [4])[:4], ma[1]), (mp(A2, a2, [4]), mb[1])], extra=[FadeIn(ma[0]), FadeIn(mb[0])], rt=1.0, origem=False)   # área → massa
        num = [r"A_\square", r"\,x_\square", "+", r"A_\circ", r"\,x_\circ"]
        den = [r"A_\square", "+", r"A_\circ"]
        B1, b1 = eqf(["X", "="], num, den, size=48, cores={("pre", 0): CMC, ("num", 0): GEO, ("num", 1): GEO, ("num", 3): GEO, ("num", 4): GEO,
                                                         ("den", 0): GEO, ("den", 2): GEO})
        self.pilha.poe(B1)
        N_, D_ = b1["num"], b1["den"]
        self.ate(0.4)
        self.voa([(mp(A1, a1, [0]), gl(B1, N_[0])), (pc, gl(B1, N_[1])), (mp(A2, a2, [0]), gl(B1, N_[3])), (cx8[0][1], gl(B1, N_[4])),
                  (mp(A1, a1, [0]), gl(B1, D_[0])), (mp(A2, a2, [0]), gl(B1, D_[2]))], extra=[FadeIn(gl(B1, sum(b1["pre"], []) + N_[2] + b1["bar"] + D_[1]))], rt=1.4)
        B2, b2 = eqf(["="], ["1600", r"\cdot 0", "+", r"(-100\pi)", r"\cdot 8"], ["1600", "-", r"100\pi"], size=48,
                     cores={("num", 0): GEO, ("num", 1): GEO, ("num", 3): GEO, ("num", 4): GEO, ("den", 0): GEO, ("den", 2): GEO})
        self.pilha.poe(B2)
        self.ate(0.5)
        self.passo(B1, B2, (b1["pre"][1], b2["pre"][0]), *[(N_[i], b2["num"][i]) for i in range(5)], (b1["bar"], b2["bar"]),
                   *[(D_[i], b2["den"][i]) for i in range(3)], (b1["pre"][0], []), rt=1.5)
        B3, b3 = M("=", r"-\tfrac{2513}{1286}", r"\approx", r"-1{,}95\ \mathrm{cm}", size=48, cores={1: GEO, 3: GEO})
        self.pilha.poe(B3)
        self.ate(0.62)
        self.passo(B2, B3, (b2["pre"][0], J(b3, 0)), (sum(b2["num"], []) + b2["bar"] + sum(b2["den"], []), J(b3, 1)), rt=1.3)
        B4, b4 = M("X", "=", "Y", r"\approx", r"-1{,}95\ \mathrm{cm}", size=48, cores={0: CMC, 2: CMC, 4: GEO})
        B4b = caixa_l(B4, CMC)
        self.pilha.poe(B4b)
        self.ate(0.72)
        self.voa([(mp(B3, b3, [2, 3]), mp(B4, b4, [3, 4]))], extra=[FadeIn(B4b[0], rate_func=lambda u: min(1.0, 3.0 * u)), FadeIn(mp(B4, b4, [0, 1, 2]))],
                 rt=1.0, origem=False)                                                                # v4 #9: a caixa nasce vazia; o resultado desce em arco por fora
        xc = -800 * PI / (1600 - 100 * PI)
        pcm = C + P3(xc * k, xc * k)
        cm = marcador_cm(pcm, r=0.15)
        self.play(FadeIn(cm, scale=1.5), pc.animate.set_opacity(0.35), run_time=0.7)
        self.reg("x1", cm=pcm, esperado=C + P3(-1.9546 * k, -1.9546 * k))
        dd = Line(C, pcm).set_stroke(WHITE_, 3).set_z_index(11)
        B5, b5 = M("d", "=", r"\sqrt{2}\cdot 1{,}95", r"\approx", r"2{,}76\ \mathrm{cm}", size=48, cores={0: GEO, 4: GEO})
        self.pilha.poe(B5)
        self.ate(0.86)
        dd.set_stroke(GEO, 3.2)
        dtk = VGroup(Line(C + P3(-0.1, 0.1) * 0.7, C + P3(0.1, -0.1) * 0.7).set_stroke(GEO, 2.4), Line(pcm + P3(-0.1, 0.1) * 0.7, pcm + P3(0.1, -0.1) * 0.7).set_stroke(GEO, 2.4)).set_z_index(11)
        ld = VGroup(mtex(r"d", GEO, 40), rot("≈ 2,76 cm", 26, GEO)).arrange(RIGHT, buff=0.1)
        ld.move_to(P3(-6.05, -3.38))                                                   # fora da placa, no canto de baixo à esquerda
        cham = DashedLine(pcm + P3(-0.1, -0.1), C + P3(-h - 0.42, -h - 0.42), dash_length=0.1).set_stroke(GEO, 1.5, opacity=0.7)   # a diagonal prolongada até o rótulo
        self.voa([(mp(B4, b4, [4]), mp(B5, b5, [2]))], extra=[Create(dd), FadeIn(dtk), FadeIn(cham), FadeIn(ld), FadeIn(mp(B5, b5, [0, 1, 3, 4]))], rt=1.0)
        self.foco = B4b
        self.ate(0.97)
        # ── X1-4 ──
        self.an("X1-4")
        rr = ValueTracker(rf)

        def placa_viva():
            r_ = rr.get_value()
            a = PI * (r_ / k) ** 2
            X = -a * 8 / (1600 - a)
            g = VGroup(placa_furada(C, S, cf, r_))
            if r_ > 0.01:
                g.add(DashedVMobject(Circle(radius=r_).move_to(cf).set_stroke(WHITE_, 2, opacity=0.75), num_dashes=max(8, int(30 * r_ / rf))).set_z_index(6))
            g.add(marcador_cm(C + P3(X * k * sd.get_value(), X * k * sd.get_value()), r=0.15))
            self.reg("x1", cm=C + P3(X * k * sd.get_value(), X * k * sd.get_value()), esperado=C + P3(X * k * sd.get_value(), X * k * sd.get_value()), r=r_ / k)
            return g
        sd = ValueTracker(1.0)
        self.add(sd)
        pv = vivo(placa_viva)
        velhos = [cheio, fant, pc, pf, ma, mb, cm, dd, crr, dtk, ld, cham]
        self.play(*[FadeOut(m) for m in velhos], FadeIn(pv), run_time=0.7)
        self.remove(*velhos)
        self.pilha.limpa()
        self.confere(["FURO ENCOLHE ATÉ SUMIR → ⊕ VOLTA AO MEIO"])
        RC = M(r"r\to 0", r"\ \Rightarrow\ ", r"A_{furo}\to 0", r"\ \Rightarrow\ ", r"X\to 0", size=38, cores={4: CMC})[0]
        self.pilha.poe(RC)
        xslot = mtex("X", CMC, 46)                                                       # a vaga da linha viva (invisível): a Pilha guarda o lugar
        xslot.scale_to_fit_height(0.6).set_opacity(0)
        self.pilha.poe(xslot)

        def x_vivo():
            r_ = rr.get_value()
            a_ = PI * (r_ / k) ** 2
            Xc = -a_ * 8 / (1600 - a_)
            s_ = f"{Xc:.2f}".replace("-", "−").replace(".", ",") + " cm"
            g_ = VGroup(mtex("X", CMC, 46), mtex("=", WHITE_, 46), mrot(s_, 36, GEO)).arrange(RIGHT, buff=0.16)
            return g_.move_to(P3(RC.get_left()[0] + g_.width / 2, xslot.get_y()))
        xv = vivo(x_vivo)
        self.play(FadeIn(RC), FadeIn(xv), run_time=0.5)
        self.play(rr.animate.set_value(0.0), run_time=2.4)
        self.ate(0.3)
        self.play(rr.animate.set_value(rf), run_time=1.4)
        Q1, q1 = M(r"\tfrac{100\pi}{1600}", r"\approx", r"\tfrac{1}{5}", size=48)
        Q2 = linha_m("NO DISCO:", M(r"\tfrac{1}{4}", size=48)[0])
        self.pilha.poe(Q1)
        self.ate(0.36)
        self.play(FadeIn(Q1), run_time=0.7)
        self.pilha.poe(Q2)
        self.play(FadeIn(Q2), run_time=0.6)
        self.foco = Q1
        self.ate(0.6)
        self.dica18(["ACHE A SIMETRIA PRIMEIRO: ELA CORTA", "A CONTA PELA METADE E JÁ DÁ O SINAL"])
        d2 = tracejado(C + P3(-h - 0.15, -h - 0.15), C + P3(h + 0.15, h + 0.15), WHITE_, 2.6, 0.8, dash=0.12).set_z_index(8)
        um = cartao("1 CONTA EM VEZ DE 2", size=28)
        self.pilha.poe(um)
        self.play(Create(d2), FadeIn(um, shift=0.1 * UP), run_time=0.9)
        self.foco = d2
        self.play(d2.animate(rate_func=there_and_back).set_stroke(opacity=0.25), run_time=0.8)                            # a diagonal pisca
        esp = VGroup(placa_furada(C, S, cf, rf), DashedVMobject(Circle(radius=rf).move_to(cf).set_stroke(WHITE_, 2, opacity=0.75), num_dashes=30).set_z_index(6))
        self.play(FadeOut(pv, run_time=0.01))
        pv.clear_updaters()
        self.add(esp)
        self.play(Rotate(esp, PI, axis=np.array([1.0, 1.0, 0.0]), about_point=C), run_time=1.0)                          # um lado espelha sobre o outro
        self.play(Rotate(esp, PI, axis=np.array([1.0, 1.0, 0.0]), about_point=C), run_time=0.6)
        self.remove(esp)
        sd.set_value(0.0)
        pv2 = vivo(placa_viva)
        self.add(pv2)
        self.play(sd.animate.set_value(1.0), run_time=1.6)                                                               # o ⊕ desliza pela diagonal até o lugar dele
        self.foco = d2
        k_ = 0
        while self.resta() > 1.5:                                                                                        # v6 §1.2: algo muda a cada ≤ 1,5 s até o fim da fala
            if k_ % 2 == 0:
                self.play(d2.animate(rate_func=there_and_back).set_stroke(opacity=0.25), run_time=0.7)
            else:
                self.play(Indicate(um, color=CYAN, scale_factor=1.0), run_time=0.7)
            k_ += 1
        self.ate(0.97)
