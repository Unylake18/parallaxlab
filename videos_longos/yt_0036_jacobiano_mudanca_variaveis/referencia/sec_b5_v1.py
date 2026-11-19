"""yt_0036 · B5 · o teorema (alvos 12 e 13). B5-1: partição de B_uv = [0, 1]² (4 × 4, depois 8 × 8) e as imagens B_ij; o ponto branco e a sua
imagem; C7 (①→②→③) na faixa de baixo com α(B_ij) voando da célula da direita e Δu_i Δv_j da esquerda. B5-2: o enunciado, uma hipótese por linha,
e as seis miniaturas à direita (x ≥ 1460), cada uma no gatilho do seu papel; selo CONDIÇÕES SUFICIENTES; quadro-receita. B5-3: a dobra
φ(u, v) = (u², v) (um movimento), 2 ≠ 1, SOBREPOSIÇÃO, J = 2u = 0, NA BORDA, PODE. B5-4: C8 (com jacobiano) e C9 (sem, fatiando deitado)."""
from j36 import *

VU5, AU5 = Vw(130, 700, 400), (-.05, 1.1, -.05, 1.1)
VX5, AX5 = Vw(1180, 720, 220), (-1.1, 1.15, -.05, 2.15)
VU6, AU6 = Vw(360, 700, 240), (-1.2, 1.2, -.1, 1.3)
VX6, AX6 = Vw(1020, 700, 300), (-.1, 1.2, -.1, 1.3)
VR, AR = Vw(520, 880, 320), (-1.1, 1.1, -.05, 2.1)


def malha_n(v, F, n, hi=None, wb=1.2):
    g = VGroup()
    for i in range(n):
        for j in range(n):
            c = celula(v, F, i / n, (i + 1) / n, j / n, (j + 1) / n, n=1, wb=wb, N=16, fill=mixh(BG_, CHAPA, .55))
            c.borda.set_stroke(mixh(BG_, MALHA, .7))
            c._ij = (i, j)
            g.add(c)
    return g


def mini(X, Y, titulo):
    return painel(X, Y, 420, 118), leg(titulo, X + 16, Y + 34, GEO, "left", 26)


class PB5(J36):
    ANTES = "O JACOBIANO"
    CHIP = True

    def corpo(self):
        self.an("B5-1")
        self.secao("DA ÁREA PARA A INTEGRAL")
        dU = monta_plano(VU5, AU5, 1.12, 1.12, -.05, -.05, uv=True, ticks=[("x", 1, r"\Uc{1}"), ("y", 1, r"\Vc{1}")])
        dX = monta_plano(VX5, AX5, 1.15, 2.2, -1.1, -.05)
        self.play(FadeIn(dU["g"]), FadeIn(dX["g"]), *[GrowFromPoint(d[k], d["v"].P(0, 0)) for d in (dU, dX) for k in ("sx", "sy")],
                  *[Create(t[0]) for t in dU["tk"]], run_time=0.8)
        self.pena(dU["lx"], dU["ly"], *[t[1] for t in dU["tk"]], dX["lx"], dX["ly"], lag=0.05)
        bU = poligono(VU5, [(0, 0), (1, 0), (1, 1), (0, 1)], RB, 1.0, GEO, 2, z=1)
        self.play(FadeIn(bU[0]), Create(bU[1]), run_time=0.6)
        self.gat("erre í jota")
        mU = malha_n(VU5, ID, 4)
        self.play(LaggedStart(*[FadeIn(c) for c in mU], lag_ratio=0.04), run_time=1.2)
        ij = (2, 1)
        cu = celula(VU5, ID, .5, .75, .25, .5, n=1, wb=3, N=16)
        lR = TP(r"R_{ij}", *VU5.px(.675, .44), 26, "c")
        self.play(*anim_cel(cu), run_time=0.6)
        self.pena(lR)
        self.gat("bê í jota")
        ps, pl = phi_seta(640, 880, 300)
        mX = malha_n(VX5, mapC, 4)
        for x in mX.get_family():
            x._voando = True
        self.play(Create(ps), TransformFromCopy(mU, mX), run_time=1.6)
        for x in mX.get_family():
            x._voando = False
        self.pena(pl)
        cx = celula(VX5, mapC, .5, .75, .25, .5, n=1, wb=3, N=16)
        cb = VX5.px(*mapC(.66, .42))
        lB = TP(r"B_{ij}", cb[0] + 4, cb[1] - 4, 24, "c")
        for x in cx.get_family():
            x._voando = True
        self.play(TransformFromCopy(cu, cx), run_time=1.0)
        for x in cx.get_family():
            x._voando = False
        self.pena(lB)
        # C7 na faixa de baixo
        y1, y2, y3, y4 = 800, 864, 928, 1005
        n1, n2, n3 = circ_num(1, 70, y1), circ_num(2, 70, y3), circ_num(3, 70, y4)
        self.gat("como na soma de riemann")
        C1 = Lp([("ii", r"\iint_B\f\,\dX\,\dY"), ("ap", r"\cong"), ("S", r"\sum_i\sum_j"), ("f", r"\f("), ("pt", r"\Am{\bar x_i},\Mg{\bar y_j}"), ("fc", ")"),
                 ("al", r"\alpha(B_{ij})")], 110, y1, 32)
        self.pena(C1, n1, lag=0.3)
        self.gat("a imagem de um ponto")
        pu = ponto_px(*VU5.px(.56, .31), BR, 7)
        px_ = ponto_px(*VX5.px(*mapC(.56, .31)), BR, 7)
        self.play(FadeIn(pu), run_time=0.3)
        sv = voo(PX(*VU5.px(.56, .31)), PX(*VX5.px(*mapC(.56, .31))), angle=-0.7)
        self.play(Create(sv), TransformFromCopy(pu, px_, path_arc=-0.7), run_time=1.3)
        C2 = Lp([("al", r"\alpha(B_{ij})"), ("ap", r"\cong"), ("J", r"\Lm{|J(\Uc{\bar u_i},\Vc{\bar v_j})|}"), ("dd", r"\Uc{\Delta u_i}\,\Vc{\Delta v_j}"),
                 ("sp", r"\qquad(\Am{\bar x_i},\Mg{\bar y_j})"), ("eq", "="), ("ph", r"\varphi(\Uc{\bar u_i},\Vc{\bar v_j})")], 110, y2, 32)
        self.pena(parte(C2, C2._ix["sp"] + C2._ix["eq"], "(x̄, ȳ) ="))
        voos(self, [(sv.copy(), parte(C2, C2._ix["ph"], "φ(ū, v̄)"))], rt=1.0)
        self.gat("o módulo do jacobiano vezes")
        voos(self, [(cx.copy(), parte(C2, C2._ix["al"], "α")), (cu.copy(), parte(C2, C2._ix["dd"], "ΔuΔv"))], rt=1.2)
        self.pena(parte(C2, C2._ix["ap"] + C2._ix["J"], "≅ |J|"))
        self.gat("a soma fica quase")
        C3 = Lp([("ap", r"\cong"), ("S", r"\sum_i\sum_j"), ("f", r"\f("), ("ph", r"\varphi(\Uc{\bar u_i},\Vc{\bar v_j})"), ("fc", ")"),
                 ("J", r"\Lm{|J(\Uc{\bar u_i},\Vc{\bar v_j})|}"), ("dd", r"\Uc{\Delta u_i}\,\Vc{\Delta v_j}")], 110 + (esq(gl(C1, "ap")) - 110), y3, 32)
        passo(self, C1, C3, [("ap", "ap"), ("S", "S"), ("f", "f"), ("fc", "fc")], copia=True, rt=1.2,
              voos=[(gl(C2, "ph").copy(), "ph"), (gl(C2, "J").copy(), "J"), (gl(C2, "dd").copy(), "dd")], nota="7 (① → ②)")
        self.pena(n2)
        self.gat("no plano u vê")
        realca(self, cu.borda, cor=LIMA, rt=0.5, wpx=5)
        self.gat("as divisões encolhem")
        mU8, mX8 = malha_n(VU5, ID, 8, wb=1), malha_n(VX5, mapC, 8, wb=1)
        cu8 = celula(VU5, ID, .5, .625, .25, .375, n=1, wb=3, N=12)
        cx8 = celula(VX5, mapC, .5, .625, .25, .375, n=1, wb=3, N=12)
        self.play(FadeOut(lR), FadeOut(lB), run_time=0.3)
        self.remove(lR, lB)
        self.play(FadeOut(mU), FadeOut(mX), FadeIn(mU8), FadeIn(mX8), Transform(cu, cu8), Transform(cx, cx8), run_time=1.4)
        self.remove(mU, mX)
        self.gat("dê u dê vê")
        C4 = Lp([("to", r"\to"), ("ii", r"\iint_{B_{uv}}"), ("f", r"\f("), ("ph", r"\varphi(\uu,\vv)"), ("fc", ")"), ("J", r"\JJ"), ("dd", r"\du\,\dv")],
                esq(C3), y4, 32)
        ph3, ph4 = C3._ix["ph"], C4._ix["ph"]
        passo(self, C3, C4, [("ap", "to"), ("S", "ii"), ("f", "f"), ([ph3[0]], [ph4[0]]), ([ph3[1]], [ph4[1]]), (ph3[2:5], [ph4[2]]), ([ph3[5]], [ph4[3]]),
                             (ph3[6:9], [ph4[4]]), ([ph3[9]], [ph4[5]]), ("fc", "fc"), ("J", "J"), ("dd", "dd")], copia=True, rt=1.6, nota="7 (② → ③)")
        self.pena(n3)
        self.marca("B5-1")

        # ════ B5-2 · o teorema ════
        self.an("B5-2")
        self.limpa_tudo()
        self.secao("O TEOREMA")
        self.gat("sem demonstrar")
        tt = T("TEOREMA", 80, 200, 28, "left", LIMA)
        self.pena(tt)
        H = [[("m", r"\varphi"), ("t", "DE CLASSE"), ("m", r"C^1"), ("t", "NO ABERTO"), ("m", r"\Omega")],
             [("m", r"B_{uv}\subset\Omega"), ("t", "COMPACTO, FRONTEIRA DE CONTEÚDO NULO")],
             [("m", r"B=\varphi(B_{uv}),\quad\varphi(\mathring B_{uv})=\mathring B")],
             [("m", r"\varphi"), ("t", "INVERSÍVEL NO INTERIOR DE"), ("m", r"B_{uv}")],
             [("m", r"\Jq\neq 0"), ("t", "NO INTERIOR DE"), ("m", r"B_{uv}")],
             [("m", r"\f"), ("t", "INTEGRÁVEL EM"), ("m", "B")]]
        gh = ["classe cê um num aberto", "bê u vê contido", "o interior vai no interior", "fi inversível no interior", "diferente de zero", "se f é integrável"]
        gm_ = ["as derivadas são contínuas", "a borda não pesa", "as duas regiões se correspondem", "contado duas vezes", "se achata", "se f é integrável"]
        tits = ["1 · DENTRO DE UM ABERTO", "2 · CONTEÚDO NULO", "3 · MIOLO NO MIOLO", "4 · SEM DOBRA", "5 · A CÉLULA NÃO COLAPSA", "6 · NA BORDA, PODE"]
        XM = 1460
        # os seis quadros (vazios) entram com o título: o palco das miniaturas não fica vazio até a primeira hipótese
        pns = [mini(XM, 240 + i * 130, tits[i]) for i in range(6)]
        self.play(LaggedStart(*[Create(p) for p, _ in pns], lag_ratio=0.15), run_time=1.2)
        for i in range(6):
            Y = 275 + i * 82 - (6 if i != 4 else 0)
            self.gat(gh[i])
            num_ = T(str(i + 1), 90, Y + 10, 26, "left", GEO, bold=False)
            ln = mixl(H[i], 130, Y, 32)
            self.pena(num_, ln, lag=0.15, passo=0.04)
            if i == 1:
                acende(self, (ln.p[0], BR), rt=0.4)
            self.gat(gm_[i])
            Ym = 240 + i * 130
            pn, tl = pns[i]
            X0, Y0 = XM, Ym
            if i == 0:
                d = VGroup(sem_ctn(DashedVMobject(Ellipse(width=240 / 120, height=64 / 120).move_to(PX(X0 + 210, Y0 + 80)), num_dashes=30)
                                   .set_stroke(GEO, W(2))).set_z_index(3), ret_px(X0 + 170, Y0 + 66, X0 + 250, Y0 + 96, fill=RB, z=2),
                           TC(r"\Ge{\Omega}", X0 + 350, Y0 + 72, 28, "c"))
            elif i == 1:
                d = VGroup(ret_px(X0 + 150, Y0 + 54, X0 + 270, Y0 + 106, fill=RB, stroke=AL, wpx=3, z=2))
            elif i == 2:
                d = VGroup(ret_px(X0 + 60, Y0 + 56, X0 + 150, Y0 + 104, fill=RB, stroke=BR, wpx=2, z=2), seta_px((X0 + 170, Y0 + 80), (X0 + 222, Y0 + 80), GEO, 3, 14),
                           sem_ctn(Ellipse(width=110 / 120, height=50 / 120).move_to(PX(X0 + 300, Y0 + 80)).set_fill(RB, 1).set_stroke(BR, W(2))).set_z_index(2))
            elif i == 3:
                d = VGroup(ret_px(X0 + 60, Y0 + 54, X0 + 120, Y0 + 106, fill=mixh(BG_, CU, .4), z=2), ret_px(X0 + 120, Y0 + 54, X0 + 180, Y0 + 106, fill=mixh(BG_, CVV, .4), z=2),
                           seta_px((X0 + 196, Y0 + 80), (X0 + 246, Y0 + 80), GEO, 3, 14), ret_px(X0 + 262, Y0 + 54, X0 + 322, Y0 + 106, fill=mixh(BG_, AL, .5), z=2),
                           T("2×", X0 + 292, Y0 + 90, 26, "center"))
            elif i == 4:
                cel5 = celula(Vw(X0, Y0, 1), lambda a, b: (120 + 100 * a + 30 * b, -(105 - 15 * a - 38 * b)), 0, 1, 0, 1, n=3, wb=2, N=4)
                d = VGroup(cel5, TC(r"\Lm{J\neq 0}", X0 + 330, Y0 + 80, 28, "c"))
            else:
                d = VGroup(ret_px(X0 + 150, Y0 + 54, X0 + 270, Y0 + 106, fill=RB, stroke=GEO, wpx=4, z=2))
            txs = [x for x in d.get_family() if getattr(x, "_caneta", False) and hasattr(x, "_tex")]
            fig = [x for x in d if x not in txs]
            self.play(*[FadeIn(x) for x in fig], run_time=0.6)
            self.pena(tl, *txs, lag=0.1)
        self.gat("é igual à integral")
        cc = TC(r"\Rightarrow\ \iint_B\f(\X,\Y)\,\dX\,\dY=\iint_{B_{uv}}\f(\varphi(\uu,\vv))\,\JJ\,\du\,\dv", 90, 772, 36, "l")
        self.pena(cc)
        self.gat("essas condições bastam")
        sl = selo("CONDIÇÕES SUFICIENTES", 90, 868, GEO, 26)
        poe_selo(self, sl)
        self.gat("na prática")
        pr = painel(560, 866, 860, 170)
        r1 = TC(r"\dX\,\dY=\JJ\,\du\,\dv", 590, 914, 32, "l")
        r2 = mixl([("t", "DETERMINAR", GEO), ("m", r"B_{uv}"), ("t", "COM", GEO), ("m", r"B=\varphi(B_{uv})")], 590, 992, 30)
        self.play(Create(pr), run_time=0.5)
        self.pena(r1, r2, lag=0.3)
        self.marca("12")

        # ════ B5-3 · por que inversível ════
        self.an("B5-3")
        self.limpa_tudo()
        self.secao("POR QUE INVERSÍVEL")
        dU = monta_plano(VU6, AU6, 1.25, 1.35, -1.2, -.1, uv=True, ticks=[("x", -1, r"\Uc{-1}"), ("x", 1, r"\Uc{1}"), ("y", 1, r"\Vc{1}")])
        _t, _q = dU["tk"][2][1], VU6.px(-1, 1)
        _t.move_to(PX(_q[0] - 16 - _t.width * 60, _q[1]))
        dX = monta_plano(VX6, AX6, 1.25, 1.35, -.1, -.1, ticks=[("x", 1, r"\Am{1}"), ("y", 1, r"\Mg{1}")])
        self.play(FadeIn(dU["g"]), FadeIn(dX["g"]), *[GrowFromPoint(d[k], d["v"].P(0, 0)) for d in (dU, dX) for k in ("sx", "sy")],
                  *[Create(t[0]) for d in (dU, dX) for t in d["tk"]], run_time=0.8)
        self.pena(dU["lx"], dU["ly"], dX["lx"], dX["ly"], *[t[1] for d in (dU, dX) for t in d["tk"]], lag=0.04)
        self.gat("olha o que acontece")
        hE = poly_px([VU6.px(*p) for p in ((-1, 0), (0, 0), (0, 1), (-1, 1))], mixh(BG_, CU, .45), 1.0, z=1)
        hD = poly_px([VU6.px(*p) for p in ((0, 0), (1, 0), (1, 1), (0, 1))], mixh(BG_, CVV, .4), 1.0, z=1)
        bd = lin_px([VU6.px(*p) for p in ((-1, 0), (1, 0), (1, 1), (-1, 1), (-1, 0))], GEO, 2, z=3)
        self.play(FadeIn(hE), FadeIn(hD), Create(bd), run_time=0.8)
        self.gat("u ao quadrado vê")
        ps, pl = phi_seta(700, 880, 330, r"\varphi(\uu,\vv)=(\uu^2,\vv)", size=30)
        self.play(Create(ps), run_time=0.5)
        self.pena(pl)
        self.gat("dobra por cima")
        for m in (hE, hD):
            m.insert_n_curves(30)
        dE, dD = hE.copy(), hD.copy()
        self.add(dD, dE)
        self.play(ApplyPointwiseFunction(leva(VU6, VX6, lambda u, v: (u * u, v)), dD), ApplyPointwiseFunction(leva(VU6, VX6, lambda u, v: (u * u, v)), dE),
                  run_time=2.4)
        # a parte sobreposta acende: as duas metades por cima uma da outra (laranja-claro sobre verde-água-claro)
        dE.set_z_index(dD.z_index + 1)
        self.play(dE.animate.set_fill(opacity=.55), run_time=0.5)
        sq = lin_px([VX6.px(*p) for p in ((0, 0), (1, 0), (1, 1), (0, 1), (0, 0))], AL, 3, z=4)
        self.play(Create(sq), run_time=0.5)
        col = Coluna36(self, 1480, 300)
        self.gat("dá dois")
        K1 = Lp([("i", r"\iint\Lm{|J|}\,\du\,\dv")], 1480, 0, 32)
        col.poe(K1)
        self.pena(K1)
        K2 = Lp([("e", "="), ("i", r"\int_{\Vc{0}}^{\Vc{1}}\!\int_{\Uc{-1}}^{\Uc{1}}2|\uu|\,\du\,\dv"), ("e2", "="), ("r", r"\Al{2}")], 1500, 0, 32)
        col.poe(K2, x=1500)
        self.pena(K2)
        self.gat("a área do quadrado é um")
        k3t, K3 = mixLp("ÁREA DA IMAGEM", [("e", "="), ("r", "1")], 1480, 0, 32)
        y3 = col.y_prox(K3)
        VGroup(k3t, K3).shift(UP * (PX(0, y3)[1] - K3.get_center()[1]))
        col.registra(K3)
        self.pena(k3t, K3, lag=0.2)
        K4 = Lp([("a", r"\Al{2}"), ("n", r"\Al{\neq}"), ("b", r"\Al{1}")], 1480, 0, 46)
        col.poe(K4, gap=40)
        self.pena(parte(K4, K4._ix["n"], "≠"))
        voos(self, [(gl(K2, "r").copy(), parte(K4, K4._ix["a"], "2")), (gl(K3, "r").copy(), parte(K4, K4._ix["b"], "1"))], rt=1.0)
        self.gat("é a sobreposição")
        realca(self, sq, cor=AL, rt=0.4, wpx=6)
        sl = selo("SOBREPOSIÇÃO: CONTOU DUAS VEZES", 990, 830, AL, 26)
        poe_selo(self, sl)
        self.gat("zera no meio")
        l0 = lin_px([VU6.px(0, -.05), VU6.px(0, 1.05)], AL, 4, z=5)
        lj = TP(r"\Al{J=2\uu=0}", VU6.px(0, 1.1)[0] + 60, VU6.px(0, 1.1)[1] - 30, 26, "l")
        self.play(Create(l0), run_time=0.5)
        self.pena(lj)
        self.gat("já na borda")
        gq = ret_px(160, 850, 300, 970, fill=RB, stroke=GEO, wpx=2, z=2)
        self.play(FadeIn(gq), run_time=0.4)
        gq2 = ret_px(160, 850, 300, 970, stroke=LIMA, wpx=2, z=3)
        self.play(Create(gq2), run_time=0.8)
        sl2 = selo("NA BORDA, PODE", 330, 925, LIMA, 26)
        poe_selo(self, sl2)
        self.marca("13")

        # ════ B5-4 · conferindo o teorema ════
        self.an("B5-4")
        self.limpa_tudo()
        self.secao("CONFERINDO O TEOREMA")
        d = plano(self, VR, AR, 1.15, 2.2, -1.1, -.05)
        reg = poly_px([VR.px(*mapC(1, t)) for t in np.linspace(0, 1, 40)] + [VR.px(*mapC(t, 1)) for t in np.linspace(1, 0, 40)], RB, 1.0, z=1)
        eU = lin_px([VR.px(*mapC(1, t)) for t in np.linspace(0, 1, 60)], CORAL, 3, z=5)
        eV = lin_px([VR.px(*mapC(t, 1)) for t in np.linspace(0, 1, 60)], AZC, 3, z=5)
        self.play(FadeIn(reg), Create(eU), Create(eV), run_time=0.8)
        col = Coluna36(self, 1120, 196)
        col.GAP36 = 26
        self.gat("com f igual a um")
        t1, G1 = mixLp("ÁREA", [("e", "="), ("i", r"\iint_{[0,1]^2}"), ("f", r"\Lm{(4\uu^2+4\vv^2)}"), ("d", r"\,\du\,\dv")], 1120, 0, 30)
        y_ = col.y_prox(G1)
        VGroup(t1, G1).shift(UP * (PX(0, y_)[1] - G1.get_center()[1]))
        col.registra(G1)
        self.pena(t1, G1, lag=0.2)
        self.gat("por dentro em u")
        G2 = Lp([("i", r"\int_{\Uc{0}}^{\Uc{1}}"), ("f", r"(4\uu^2+4\vv^2)\,\du")], 1120, 0, 30)
        col.poe(G2)
        G2._xy = (1120, centro(G2)[1])
        self.escreve_voos(G2, [(gl(G1, "f"), "f")])
        G2 = cresce(self, G2, [("e1", "="), ("lb", r"\Big["), ("F", r"\dfrac{4\uu^3}{3}+4\vv^2\uu"), ("rb", r"\Big]"), ("sb", r"_{\Uc{0}}^{\Uc{1}}")],
                    voos=lambda B: [(VGroup(*[G2[0][k] for k in idx_lims(G2, "i")[0]]).copy(), lims_sb(B, "sb")[0]),
                                    (VGroup(*[G2[0][k] for k in idx_lims(G2, "i")[1]]).copy(), lims_sb(B, "sb")[1])], col=col, nota="8 colchete u")
        self.gat("que dá quatro terços")
        G2 = cresce(self, G2, [("e2", "="), ("r", r"\dfrac{4}{3}+4\vv^2")], voos=lambda B: [(gl(G2, "F").copy(), "r")], col=col, nota="8 (= 4/3 + 4v²)")
        self.gat("por fora em vê")
        G3 = Lp([("i", r"\int_{\Vc{0}}^{\Vc{1}}"), ("f", r"\left(\dfrac{4}{3}+4\vv^2\right)\dv")], 1120, 0, 30)
        col.poe(G3)
        G3._xy = (1120, centro(G3)[1])
        self.escreve_voos(G3, [(gl(G2, "r"), [G3._ix["f"][k] for k in range(1, len(G3._ix["f"]) - 3)])])
        G3 = cresce(self, G3, [("e1", "="), ("lb", r"\Big["), ("F", r"\dfrac{4\vv}{3}+\dfrac{4\vv^3}{3}"), ("rb", r"\Big]"), ("sb", r"_{\Vc{0}}^{\Vc{1}}")],
                    voos=lambda B: [(VGroup(*[G3[0][k] for k in idx_lims(G3, "i")[0]]).copy(), lims_sb(B, "sb")[0]),
                                    (VGroup(*[G3[0][k] for k in idx_lims(G3, "i")[1]]).copy(), lims_sb(B, "sb")[1])], col=col, nota="8 colchete v")
        self.gat("quatro terços mais quatro terços")
        G3b = Lp([("e2", "="), ("d", r"\dfrac{4}{3}+\dfrac{4}{3}")], 1150, 0, 30)
        col.poe(G3b, x=1150)
        G3b._xy = (1150, centro(G3b)[1])
        self.escreve_voos(G3b, [(gl(G3, "F"), "d")])
        G3b = cresce(self, G3b, [("e3", "="), ("r", r"\Lm{\dfrac{8}{3}}")], voos=lambda B: [(gl(G3b, "d").copy(), "r")], col=col, nota="8 (= 8/3)")
        # sem jacobiano: fatiando deitado
        self.gat("sem jacobiano")
        yf = 1.0
        tH = tiraH(VR, yf, yf * yf / 4 - 1, 1 - yf * yf / 4, h=.06, cor=E2)
        pe, ps_ = pontos_es(VR, (yf * yf / 4 - 1, yf), (1 - yf * yf / 4, yf))
        self.play(FadeIn(tH), run_time=0.5)
        self.gat("entra na parábola")
        realca(self, eV, cor=AZC, rt=0.2, wpx=6)
        self.play(FadeIn(pe), run_time=0.3)
        yS = col.y_prox() + 22
        yE = yS + 74
        n2_ = Lp([("a", r"\vv=1:\ \X=\uu^2-1,\ \Y=2\uu")], 1120, yE, 28)
        n2_._xy = (1120, yE)
        self.escreve_voos(n2_, [(eV, "a")], rt=0.9)
        n2_ = cresce(self, n2_, [("i1", r"\Rightarrow\uu=\dfrac{\Y}{2}")], nota="9 (u = y/2)")
        n2_ = cresce(self, n2_, [("i2", r"\Rightarrow\Az{\X=\dfrac{\Y^2}{4}-1}")], nota="9 (x = y²/4 − 1)")
        lE = T("ENTRADA", dir_(n2_) + 16, yE + 9, 26, "left", AZC, bold=False)
        self.pena(lE)
        self.gat("e sai na da direita")
        realca(self, eU, cor=CORAL, rt=0.2, wpx=6)
        self.play(FadeIn(ps_), run_time=0.3)
        n1_ = Lp([("a", r"\uu=1:\ \X=1-\vv^2,\ \Y=2\vv")], 1120, yS, 28)
        n1_._xy = (1120, yS)
        self.escreve_voos(n1_, [(eU, "a")], rt=0.9)
        n1_ = cresce(self, n1_, [("i1", r"\Rightarrow\vv=\dfrac{\Y}{2}")], nota="9 (v = y/2)")
        n1_ = cresce(self, n1_, [("i2", r"\Rightarrow\Co{\X=1-\dfrac{\Y^2}{4}}")], nota="9 (x = 1 − y²/4)")
        lS = T("SAÍDA", dir_(n1_) + 16, yS + 9, 26, "left", CORAL, bold=False)
        self.pena(lS)
        col.registra(n1_)
        col.registra(n2_)
        self.gat("a saída menos a entrada")
        t3_, G4 = mixLp("COMPRIMENTO", [("e", "="), ("s", r"\Co{\left(1-\dfrac{\Y^2}{4}\right)}"), ("m", "-"), ("en", r"\Az{\left(\dfrac{\Y^2}{4}-1\right)}")], 1120, 0, 28)
        y4_ = col.y_prox(G4, gap=30)
        VGroup(t3_, G4).shift(UP * (PX(0, y4_)[1] - G4.get_center()[1]))
        G4._xy = (esq(G4), y4_)
        col.registra(G4)
        self.pena(t3_)
        self.escreve_voos(G4, [(ps_, "s"), (pe, "en")])
        G4 = cresce(self, G4, [("e2", "="), ("r", r"2-\dfrac{\Y^2}{2}")], voos=lambda B: [(VGroup(gl(G4, "s"), gl(G4, "en")).copy(), "r")], col=col,
                    nota="9 (saída − entrada)")
        self.gat("a integral de zero a dois dá")
        G5 = Lp([("i", r"\int_{\Mg{0}}^{\Mg{2}}"), ("f", r"\left(2-\dfrac{\Y^2}{2}\right)\dY")], 1120, 0, 28)
        col.poe(G5)
        G5._xy = (1120, centro(G5)[1])
        self.escreve_voos(G5, [(gl(G4, "r"), [G5._ix["f"][k] for k in range(1, len(G5._ix["f"]) - 3)])])
        G5 = cresce(self, G5, [("e1", "="), ("lb", r"\Big["), ("F", r"2\Y-\dfrac{\Y^3}{6}"), ("rb", r"\Big]"), ("sb", r"_{\Mg{0}}^{\Mg{2}}")],
                    voos=lambda B: [(VGroup(*[G5[0][k] for k in idx_lims(G5, "i")[0]]).copy(), lims_sb(B, "sb")[0]),
                                    (VGroup(*[G5[0][k] for k in idx_lims(G5, "i")[1]]).copy(), lims_sb(B, "sb")[1])], col=col, nota="9 colchete y")
        self.gat("quatro menos oito sextos")
        G5 = cresce(self, G5, [("e2", "="), ("d", r"4-\dfrac{8}{6}")], col=col, nota="9 (G(2) − G(0))")
        self.gat("quatro menos quatro terços")
        G6 = Lp([("e3", "="), ("d", r"4-\dfrac{4}{3}")], 1150, 0, 28)
        col.poe(G6, x=1150)
        G6._xy = (1150, centro(G6)[1])
        self.escreve_voos(G6, [(gl(G5, "d"), "d")])
        G6 = cresce(self, G6, [("e4", "="), ("r", r"\Lm{\dfrac{8}{3}}")], voos=lambda B: [(gl(G6, "d").copy(), "r")], col=col, nota="9 (= 8/3)")
        self.gat("bateu")
        ck = check_px(dir_(G6) + 32, centro(G6)[1], MEN)
        self.play(Create(ck), run_time=0.4)
        self.marca("B5-4")
        self.sai_fim()
