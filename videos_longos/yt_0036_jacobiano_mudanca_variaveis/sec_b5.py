"""yt_0036 · B5 · o teorema (alvos 12 e 13) — v2. B5-1: partição de B_uv = [0, 1]² (4 × 4, depois 8 × 8) e as imagens B_ij; C7 (①→②→③)
na faixa de baixo; os glifos Δu_i, Δv_j (rótulos nas arestas de R_ij) e B_ij voam um de cada vez, por fora da linha ① e sem cruzar o eixo u (Q09).
B5-2: o enunciado e as miniaturas que explicam (Q10): cada moldura nasce com o seu conteúdo; 1–5 e NOTA · NA BORDA, PODE. B5-3: a dobra
φ(u, v) = (u², v) com a conta C18 inteira (derivadas, J = 2u, as duas metades, 2 ≠ 1) e a metade da direita (§6.6). B5-4: C8 e C9 com
G(b) − G(a) em todo colchete."""
from j36 import *

VU5, AU5 = Vw(130, 640, 380), (-.05, 1.1, -.05, 1.1)
VX5, AX5 = Vw(1180, 660, 200), (-1.1, 1.15, -.05, 2.15)
VU6, AU6 = Vw(262, 600, 170), (-1.2, 1.2, -.1, 1.3)
VX6, AX6 = Vw(640, 600, 170), (-.1, 1.2, -.1, 1.3)
VR, AR = Vw(500, 880, 300), (-1.1, 1.1, -.05, 2.1)
EMENDA_B51, EMENDA_B53 = 760, 525
PT5 = (.70, .45)                                    # o ponto branco no canto de cima de R_ij (a seta sai por cima, longe dos rótulos)


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
    CHIP = False                            # v2 §6.3: sem chip no B5 (o B5 fala de outros J)

    def corpo(self):
        self.an("B5-1")
        self.secao("DA ÁREA PARA A INTEGRAL")
        dU = monta_plano(VU5, AU5, 1.12, 1.12, -.05, -.05, uv=True, ticks=[("x", 1, r"\Uc{1}"), ("y", 1, r"\Vc{1}")])
        dX = monta_plano(VX5, AX5, 1.15, 2.2, -1.1, -.05)
        self.fundo(VU5, VX5, emenda=EMENDA_B51, rt=0)
        self.play(FadeIn(dU["g"]), FadeIn(dX["g"]), *[GrowFromPoint(d[k], d["v"].P(0, 0)) for d in (dU, dX) for k in ("sx", "sy")],
                  *[Create(t[0]) for t in dU["tk"]], run_time=0.8)
        self.pena(dU["lx"], dU["ly"], *[t[1] for t in dU["tk"]], dX["lx"], dX["ly"], lag=0.05)
        bU = poligono(VU5, [(0, 0), (1, 0), (1, 1), (0, 1)], RB, 1.0, GEO, 2, z=1)
        self.play(FadeIn(bU[0]), Create(bU[1]), run_time=0.6)
        self.gat("erre í jota")
        mU = malha_n(VU5, ID, 4)
        self.play(LaggedStart(*[FadeIn(c) for c in mU], lag_ratio=0.04), run_time=1.2)
        cu = celula(VU5, ID, .5, .75, .25, .5, n=1, wb=3, N=16)
        lR = TP(r"R_{ij}", VU5.px(.5, .375)[0] - 12, VU5.px(.5, .375)[1], 26, "r")      # à esquerda da célula (a seta sai pela direita)
        self.play(*anim_cel(cu), run_time=0.6)
        self.pena(lR)
        # os lados de R_ij levam os seus glifos (é deles que Δu_i e Δv_j voam para a ②)
        lDu = TP(r"\Uc{\Delta u_i}", VU5.px(.625, .25)[0], VU5.px(.625, .25)[1] + 26, 26, "c")
        lDv = TP(r"\Vc{\Delta v_j}", VU5.px(.75, .3)[0] + 14, VU5.px(.75, .3)[1], 26, "l")
        self.pena(lDu, lDv, lag=0.2)
        self.gat("bê í jota")
        ps, pl = phi_seta(640, 880, 300)
        mX = malha_n(VX5, mapC, 4)
        voos(self, [(mU, mX)], rt=1.6, extra=[Create(ps)], livre=(lR, lDu, lDv))
        self.pena(pl)
        cx = celula(VX5, mapC, .5, .75, .25, .5, n=1, wb=3, N=16)
        cb = VX5.px(*mapC(.66, .42))
        lB = TP(r"B_{ij}", VX5.px(.95, mapC(.75, .375)[1])[0] + 20, VX5.px(.95, mapC(.75, .375)[1])[1], 26, "l")      # fora da região, à direita (dentro há malha)
        voos(self, [(cu, cx)], rt=1.0, livre=(lR, lDu, lDv))
        self.pena(lB)
        # C7 na faixa de baixo (tamanho 40): ① 750 · ② 835 · ③ 920; quando ④ chega, a ② (já usada) sai e a ③ sobe
        y1, y2, y3 = 752, 838, 924
        n1, n2, n3 = circ_num(1, 70, y1), circ_num(2, 70, y3), circ_num(3, 70, y3)      # ① C1 · ② a linha 3 do código · ③ a linha 4
        self.gat("como na soma de riemann")
        C1 = Lp([("ii", r"\iint_B\f\,\dX\,\dY"), ("ap", r"\cong"), ("S", r"\sum_i\sum_j"), ("f", r"\f("), ("pt", r"\Am{\bar x_i},\Mg{\bar y_j}"), ("fc", ")"),
                 ("al", r"\alpha(B_{ij})")], 110, y1, 40)
        self.pena(C1, n1, lag=0.3)
        self.gat("a imagem de um ponto")
        pu = ponto_px(*VU5.px(*PT5), BR, 7)
        px_ = ponto_px(*VX5.px(*mapC(*PT5)), BR, 7)
        self.play(FadeIn(pu), run_time=0.3)
        sv = voo(PX(*VU5.px(*PT5)), PX(*VX5.px(*mapC(*PT5))), angle=0.8)
        self.play(Create(sv), TransformFromCopy(pu, px_, path_arc=0.8), run_time=1.3)
        C2 = Lp([("al", r"\alpha(B_{ij})"), ("ap", r"\cong"), ("J", r"\Lm{|J(\Uc{\bar u_i},\Vc{\bar v_j})|}"), ("dd", r"\Uc{\Delta u_i}\,\Vc{\Delta v_j}"),
                 ("sp", r"\qquad(\Am{\bar x_i},\Mg{\bar y_j})"), ("eq", "="), ("ph", r"\varphi(\Uc{\bar u_i},\Vc{\bar v_j})")], 110, y2, 40)
        self.pena(parte(C2, C2._ix["sp"] + C2._ix["eq"], "(x̄, ȳ) ="))
        # φ(ū, v̄) nasce da seta entre o ponto branco e a sua imagem (o glifo φ escrito na seta desce para a ②, pela direita da ①)
        X1d = dir_(C1) + 110                                             # por fora da ①, com a folga da largura do glifo
        q_ = VX5.px(*mapC(*PT5))
        yph = mapC(*PT5)[1]
        lph = TP(r"\varphi(\Uc{\bar u_i},\Vc{\bar v_j})", VX5.px(yph * yph / 4 - 1, yph)[0] - 16, q_[1], 26, "r")     # à esquerda da região, na altura da imagem
        self.pena(lph)
        voos(self, [(lph.f, parte(C2, C2._ix["ph"], "φ(ū, v̄)"), [(X1d, q_[1]), (X1d, y2)])], rt=1.0)
        self.gat("o módulo do jacobiano vezes")
        # Q09: um de cada vez (≥ 0,6 s), glifo (nunca bloco), por fora da ①: sobem/descem pela direita da linha ① e entram pela linha de baixo
        ybx = y2 + 62
        al_ = parte(C2, C2._ix["al"], "α")
        voos(self, [(VGroup(*lB.f[0]), al_, [(centro(lB)[0] - 70, centro(lB)[1]), (centro(lB)[0] - 70, ybx), (esq(al_) + 30, ybx)])], rt=1.2)   # longe do x do eixo
        dd_ = parte(C2, C2._ix["dd"], "ΔuΔv")
        voos(self, [(VGroup(*lDu.f[0], *lDv.f[0]), dd_, [(VU5.px(1.25, .3)[0], VU5.px(1.25, .3)[1]), (X1d, 690), (X1d, ybx), (centro(dd_)[0], ybx)])], rt=1.2)
        self.pena(parte(C2, C2._ix["ap"] + C2._ix["J"], "≅ |J|"))
        self.gat("a soma fica quase")
        C3 = Lp([("ap", r"\cong"), ("S", r"\sum_i\sum_j"), ("f", r"\f("), ("ph", r"\varphi(\Uc{\bar u_i},\Vc{\bar v_j})"), ("fc", ")"),
                 ("J", r"\Lm{|J(\Uc{\bar u_i},\Vc{\bar v_j})|}"), ("dd", r"\Uc{\Delta u_i}\,\Vc{\Delta v_j}")], esq(gl(C1, "ap")), y3, 40)
        # M5 (① → ②): no lugar — α(B_ij) vira |J| Δu Δv e (x̄, ȳ) vira φ(ū, v̄) (os termos da ② voam para os seus lugares na ③)
        passo(self, C1, C3, [("ap", "ap"), ("S", "S"), ("f", "f"), ("fc", "fc")], copia=True, rt=1.2,
              voos=[(gl(C2, "ph").copy(), "ph"), (gl(C2, "J").copy(), "J"), (gl(C2, "dd").copy(), "dd")], nota="M5 C7 (① → ②)")
        self.pena(n2)
        self.gat("no plano u vê")
        realca(self, cu.borda, cor=LIMA, rt=0.5, wpx=5)
        self.gat("as divisões encolhem")
        mU8, mX8 = malha_n(VU5, ID, 8, wb=1), malha_n(VX5, mapC, 8, wb=1)
        cu8 = celula(VU5, ID, .5, .625, .25, .375, n=1, wb=3, N=12)
        cx8 = celula(VX5, mapC, .5, .625, .25, .375, n=1, wb=3, N=12)
        self.play(FadeOut(lR), FadeOut(lB), FadeOut(lDu), FadeOut(lDv), run_time=0.3)
        self.remove(lR, lB, lDu, lDv)
        self.play(FadeOut(mU), FadeOut(mX), FadeIn(mU8), FadeIn(mX8), Transform(cu, cu8), Transform(cx, cx8), run_time=1.4)
        self.remove(mU, mX)
        self.gat("dê u dê vê")
        # a ② já serviu: sai; a ③ sobe para o lugar dela e a ④ nasce embaixo (M5, ② → ③: Σ Σ → ∬, Δu Δv → du dv)
        self.play(FadeOut(C2), run_time=0.4)  # final K12: troca de página em dois tempos (sai, depois sobe)
        self.play(C3.animate.shift(UP * (y3 - y2) / 120), n2.animate.shift(UP * (y3 - y2) / 120), run_time=0.6)
        self.remove(C2)
        C4 = Lp([("to", r"\to"), ("ii", r"\iint_{B_{uv}}"), ("f", r"\f("), ("ph", r"\varphi(\uu,\vv)"), ("fc", ")"), ("J", r"\JJ"), ("dd", r"\du\,\dv")],
                esq(C3), y3, 40)
        ph3, ph4 = C3._ix["ph"], C4._ix["ph"]
        passo(self, C3, C4, [("ap", "to"), ("S", "ii"), ("f", "f"), ([ph3[0]], [ph4[0]]), ([ph3[1]], [ph4[1]]), (ph3[2:5], [ph4[2]]), ([ph3[5]], [ph4[3]]),
                             (ph3[6:9], [ph4[4]]), ([ph3[9]], [ph4[5]]), ("fc", "fc"), ("J", "J"), ("dd", "dd")], copia=True, rt=1.6, nota="M5 C7 (② → ③)")
        self.pena(n3)
        self.marca("B5-1")

        # ════ B5-2 · o teorema (Q10: cada moldura nasce com a sua miniatura; nenhuma vazia) ════
        self.an("B5-2")
        self.secao("O TEOREMA")
        # v2 (palco vazio): enquanto a fala anuncia o resultado ("o livro enuncia esse resultado sem demonstrar…"), o resultado do B5-1 fica;
        # na linha 1 ele sai, o papel vira o padrão e o título TEOREMA entra junto com a hipótese 1
        self.gat("sem demonstrar")
        acende(self, (C4, LIMA), rt=1.6)                               # o resultado que o livro enuncia acende na leitura (palco vivo)
        self.gat("cada hipótese tem um papel")
        acende(self, (gl(C4, "J"), LIMA), rt=1.2)
        tt = T("TEOREMA", 80, 205, 30, "left", LIMA)
        H = [[("m", r"\varphi"), ("t", "DE CLASSE"), ("m", r"C^1"), ("t", "NO ABERTO"), ("m", r"\Omega")],
             [("m", r"B_{uv}\subset\Omega"), ("t", "COMPACTO, FRONTEIRA DE CONTEÚDO NULO")],
             [("m", r"B=\varphi(B_{uv}),\quad\varphi(\mathring B_{uv})=\mathring B")],
             [("m", r"\varphi"), ("t", "INVERSÍVEL NO INTERIOR DE"), ("m", r"B_{uv}")],
             [("m", r"\Jq\neq 0"), ("t", "NO INTERIOR DE"), ("m", r"B_{uv}")],
             [("m", r"\f"), ("t", "INTEGRÁVEL EM"), ("m", "B")]]
        gh = ["classe cê um num aberto", "bê u vê contido", "o interior vai no interior", "fi inversível no interior", "diferente de zero", "se f é integrável"]
        gm_ = ["as derivadas são contínuas", "a borda não pesa", "as duas regiões se correspondem", "contado duas vezes", "se achata", None]
        tits = ["1 · DENTRO DE UM ABERTO", "2 · CONTEÚDO NULO", "3 · MIOLO NO MIOLO", "4 · SEM DOBRA", "5 · A CÉLULA NÃO COLAPSA"]
        XM = 1440

        def figura(i, X0, Y0):
            if i == 0:
                return VGroup(sem_ctn(DashedVMobject(Ellipse(width=240 / 120, height=64 / 120).move_to(PX(X0 + 210, Y0 + 80)), num_dashes=30)
                                      .set_stroke(GEO, W(2))).set_z_index(3), ret_px(X0 + 170, Y0 + 66, X0 + 250, Y0 + 96, fill=RB, z=2),
                              TC(r"\Ge{\Omega}", X0 + 350, Y0 + 72, 28, "c"))
            if i == 1:                     # a borda acesa num traço fino brilhante: a borda não pesa
                return VGroup(ret_px(X0 + 40, Y0 + 56, X0 + 150, Y0 + 104, fill=RB, z=2), ret_px(X0 + 40, Y0 + 56, X0 + 150, Y0 + 104, stroke=BR, wpx=1.5, z=3),
                              T("BORDA: ÁREA 0", X0 + 176, Y0 + 90, 26, "left", BR, bold=False))
            if i == 2:
                return VGroup(ret_px(X0 + 60, Y0 + 56, X0 + 150, Y0 + 104, fill=RB, stroke=BR, wpx=2, z=2), seta_px((X0 + 170, Y0 + 80), (X0 + 222, Y0 + 80), GEO, 3, 14),
                              sem_ctn(Ellipse(width=110 / 120, height=50 / 120).move_to(PX(X0 + 300, Y0 + 80)).set_fill(RB, 1).set_stroke(BR, W(2))).set_z_index(2))
            if i == 3:
                return VGroup(ret_px(X0 + 60, Y0 + 54, X0 + 120, Y0 + 106, fill=mixh(BG_, CU, .4), z=2), ret_px(X0 + 120, Y0 + 54, X0 + 180, Y0 + 106, fill=mixh(BG_, CVV, .4), z=2),
                              seta_px((X0 + 196, Y0 + 80), (X0 + 246, Y0 + 80), GEO, 3, 14), ret_px(X0 + 262, Y0 + 54, X0 + 322, Y0 + 106, fill=mixh(BG_, AL, .5), z=2),
                              T("2×", X0 + 292, Y0 + 90, 26, "center"))
            if i == 4:
                cel5 = celula(Vw(X0, Y0, 1), lambda a, b: (120 + 100 * a + 30 * b, -(105 - 15 * a - 38 * b)), 0, 1, 0, 1, n=3, wb=2, N=4)
                return VGroup(cel5, TC(r"\Lm{J\neq 0}", X0 + 330, Y0 + 80, 28, "c"))
            # NOTA · NA BORDA, PODE: o quadrado com a aresta da esquerda em ALERTA e J = 0 SÓ NA BORDA
            return VGroup(ret_px(X0 + 40, Y0 + 54, X0 + 112, Y0 + 106, fill=RB, stroke=GEO, wpx=2, z=2),
                          lin_px([(X0 + 40, Y0 + 54), (X0 + 40, Y0 + 106)], AL, 5, z=4),
                          mixl([("m", r"\Al{J=0}"), ("t", "SÓ NA BORDA", GEO)], X0 + 134, Y0 + 80, 28))

        def entra_mini(i, titulo):
            Ym = 240 + i * 130
            pn, tl = mini(XM, Ym, titulo)
            d = figura(i, XM, Ym)
            txs = [x for x in d.get_family() if (getattr(x, "_caneta", False) and hasattr(x, "_tex")) or hasattr(x, "p")]   # mixl também vai pela caneta
            fig = [x for x in d if x not in txs and not any(x in t_.get_family() for t_ in txs)]
            # a moldura desenha (≤ 0,5 s) enquanto o primeiro conteúdo começa: nunca fica vazia
            self.play(Create(pn), *[FadeIn(x) for x in fig], run_time=0.5)
            self.pena(tl, *txs, lag=0.1)
        for i in range(6):
            Y = 268 + i * 76
            self.gat(gh[i])
            num_ = T(str(i + 1), 90, Y + 12, 30, "left", GEO, bold=False)
            ln = mixl(H[i], 130, Y, 40)
            if i == 0:
                self.limpa_tudo()
                self.fundo(rt=0.3)          # v2 §1.2: sem gráfico → papel() (o FadeOut do B5-1 vai junto)
                self.pena(tt)
            self.pena(num_, ln, lag=0.15, passo=0.04)
            if i == 1:
                acende(self, (ln.p[0], BR), rt=0.4)
            if gm_[i] is not None:
                self.gat(gm_[i])
                entra_mini(i, tits[i])
        self.gat("é igual à integral")
        cc = TC(r"\Rightarrow\ \iint_B\f(\X,\Y)\,\dX\,\dY=\iint_{B_{uv}}\f(\varphi(\uu,\vv))\,\JJ\,\du\,\dv", 90, 800, 48, "l")      # resultado: ≥ 32 px
        self.pena(cc)
        self.gat("essas condições bastam")
        sl = selo("CONDIÇÕES SUFICIENTES", 90, 712, GEO, 26)
        poe_selo(self, sl)
        self.gat("não são as únicas")
        entra_mini(5, "NOTA · NA BORDA, PODE")
        self.gat("na prática")
        pr = painel(80, 878, 1300, 150)                               # ≥ 32 px das miniaturas (x = 1440)
        r1 = TC(r"\dX\,\dY=\JJ\,\du\,\dv", 110, 925, 40, "l")
        r2 = mixl([("t", "DETERMINAR", GEO), ("m", r"B_{uv}"), ("t", "COM", GEO), ("m", r"B=\varphi(B_{uv})")], 110, 992, 40)
        self.pena(r1, r2, lag=0.3, extra=[Create(pr)])                 # final K2: o painel nasce com o conteúdo
        self.marca("12")

        # ════ B5-3 · por que inversível (C18 inteira; Q11; §6.6 a metade da direita) ════
        self.an("B5-3")
        self.limpa_tudo()
        self.secao("POR QUE INVERSÍVEL")
        # final K8: enquanto a coluna está vazia, os dois planos ficam GRANDES e centrados (unidade 270 px, emenda do papel sob a seta de φ);
        # no gatilho do 1º degrau da coluna, um único movimento de 0,8 s leva tudo para o tamanho e o lugar do v2.
        def monta53(VUx, VXx, ux_seta):
            dU = monta_plano(VUx, AU6, 1.25, 1.35, -1.2, -.1, uv=True, ticks=[("x", -1, r"\Uc{-1}"), ("x", 1, r"\Uc{1}"), ("y", 1, r"\Vc{1}")])
            _t, _q = dU["tk"][2][1], VUx.px(-1, 1)
            _t.move_to(PX(_q[0] - 16 - _t.width * 60, _q[1]))
            dX = monta_plano(VXx, AX6, 1.25, 1.35, -.1, -.1, ticks=[("x", 1, r"\Am{1}"), ("y", 1, r"\Mg{1}")])
            hE = poly_px([VUx.px(*p) for p in ((-1, 0), (0, 0), (0, 1), (-1, 1))], mixh(BG_, CU, .45), 1.0, z=1)
            hD = poly_px([VUx.px(*p) for p in ((0, 0), (1, 0), (1, 1), (0, 1))], mixh(BG_, CVV, .4), 1.0, z=1)
            bd = lin_px([VUx.px(*p) for p in ((-1, 0), (1, 0), (1, 1), (-1, 1), (-1, 0))], GEO, 2, z=3)
            ps, pl = phi_seta(*ux_seta, r"\varphi(\uu,\vv)=(\uu^2,\vv)", size=30)
            for m in (hE, hD):
                m.insert_n_curves(30)
            sq = lin_px([VXx.px(*p) for p in ((0, 0), (1, 0), (1, 1), (0, 1), (0, 0))], AL, 3, z=4)
            return dict(dU=dU, dX=dX, hE=hE, hD=hD, bd=bd, ps=ps, pl=pl, sq=sq)
        VU6b, VX6b = Vw(597, 708, 270), Vw(1310, 708, 270)
        Gb = monta53(VU6b, VX6b, (975, 1245, 420))                       # a seta de φ no vão entre os planos grandes (x 975–1245)
        Gs = monta53(VU6, VX6, (470, 600, 330))
        dU, dX = Gb["dU"], Gb["dX"]
        self.fundo(VU6b, VX6b, emenda=1110)                              # emenda sob o meio da seta de φ
        self.play(FadeIn(dU["g"]), FadeIn(dX["g"]), *[GrowFromPoint(d[k], d["v"].P(0, 0)) for d in (dU, dX) for k in ("sx", "sy")],
                  *[Create(t[0]) for d in (dU, dX) for t in d["tk"]], run_time=0.8)
        self.pena(dU["lx"], dU["ly"], dX["lx"], dX["ly"], *[t[1] for d in (dU, dX) for t in d["tk"]], lag=0.04)
        self.gat("se não for")
        hE, hD, bd = Gb["hE"], Gb["hD"], Gb["bd"]
        self.play(FadeIn(hE), FadeIn(hD), Create(bd), run_time=0.8)
        self.gat("u ao quadrado")
        ps, pl = Gb["ps"], Gb["pl"]
        self.play(Create(ps), run_time=0.5)
        self.pena(pl)
        self.gat("dobra por cima")
        dobra = lambda u, v: (u * u, v)
        dE, dD = hE.copy(), hD.copy()
        self.add(dD, dE)
        self.play(ApplyPointwiseFunction(leva(VU6b, VX6b, dobra), dD), ApplyPointwiseFunction(leva(VU6b, VX6b, dobra), dE), run_time=2.4)
        dE.set_z_index(dD.z_index + 1)
        self.play(dE.animate.set_fill(opacity=.55), run_time=0.5)
        sq = Gb["sq"]
        self.play(Create(sq), run_time=0.5)
        CX6 = 880
        col = Coluna36(self, CX6, 200)
        col.GAP36 = 24
        # C18.1: φ(u, v) = (u², v) (voa da seta) · as quatro derivadas
        self.gat("as derivadas")
        # o movimento único (0,8 s): planos grandes → tamanho e lugar do v2, com o papel junto (emenda sob a seta de φ do v2)
        dEs, dDs = Gs["hE"].copy(), Gs["hD"].copy()
        dEs.apply_function(leva(VU6, VX6, dobra))
        dDs.apply_function(leva(VU6, VX6, dobra))
        dEs.set_fill(opacity=.55).set_z_index(dDs.z_index + 1)
        grandes = todos_plano(Gb["dU"]) + todos_plano(Gb["dX"]) + [hE, hD, bd, ps, pl, sq, dE, dD]
        pequenos = todos_plano(Gs["dU"]) + todos_plano(Gs["dX"]) + [Gs["hE"], Gs["hD"], Gs["bd"], Gs["ps"], Gs["pl"], Gs["sq"], dEs, dDs]
        for m in pequenos:
            ja_escrita(m)
            for x in m.get_family():
                if getattr(x, "_caneta", False):
                    x._esc = True
        self.fundo(VU6, VX6, emenda=EMENDA_B53, rt=0.8, extra=[ReplacementTransform(a, b) for a, b in zip(grandes, pequenos)])
        dU, dX = Gs["dU"], Gs["dX"]
        hE, hD, bd, ps, pl, sq, dE, dD = Gs["hE"], Gs["hD"], Gs["bd"], Gs["ps"], Gs["pl"], Gs["sq"], dEs, dDs
        print(f"[k8] {self._aid} {self.t:.2f} planos grandes (unidade {VU6b.u:.0f} px) → v2 (unidade {VU6.u:.0f} px) em 0,8 s")
        L1 = Lp([("f", r"\varphi(\uu,\vv)=(\uu^2,\vv)"), ("a", r"\quad\xu=2\uu"), ("b", r"\quad\xv=0"), ("c", r"\quad\yu=0"), ("d", r"\quad\yv=1")], CX6, 0, 40)
        col.poe(L1)
        L1._xy = (CX6, centro(L1)[1])
        voos(self, [(pl, parte(L1, L1._ix["f"], "φ"))], rt=0.8)
        self.pena(*[parte(L1, L1._ix[k], k) for k in "abcd"], lag=0.5)
        # C18.2: J = det[2u 0; 0 1] = 2u·1 − 0·0 = 2u (as derivadas voam para a matriz; os produtos e o 2u por voo)
        self.gat("dois u vezes um")
        L2 = Lp([("J", "J"), ("e", r"=\det"), ("M", r"\begin{bmatrix}2\uu&0\\ 0&1\end{bmatrix}")], CX6, 0, 40)
        col.poe(L2)
        L2._xy = (CX6, centro(L2)[1])
        c2 = casas(L2, L2._ix["M"], 2, 2)
        vb = lambda k, n: VGroup(*[L1[0][i] for i in L1._ix[k][-n:]])
        self.escreve_voos(L2, [(vb("a", 2), c2[(0, 0)]), (vb("b", 1), c2[(0, 1)]), (vb("c", 1), c2[(1, 0)]), (vb("d", 1), c2[(1, 1)])], rt=0.4)
        L2 = cresce(self, L2, [("e2", "="), ("p", r"2\uu\cdot 1-0\cdot 0")],
                    voos=lambda B: [(VGroup(*[L2[0][i] for i in c2[(0, 0)]]).copy(), B._ix["p"][0:2]), (VGroup(*[L2[0][i] for i in c2[(1, 1)]]).copy(), [B._ix["p"][3]]),
                                    (VGroup(*[L2[0][i] for i in c2[(0, 1)]]).copy(), [B._ix["p"][5]]), (VGroup(*[L2[0][i] for i in c2[(1, 0)]]).copy(), [B._ix["p"][7]])],
                    col=col, nota="M6 C18.2 (det → 2u·1 − 0·0)")
        L2 = cresce(self, L2, [("e3", "="), ("r", r"\Lm{2\uu}")], voos=lambda B: [(VGroup(*[L2[0][i] for i in L2._ix["p"][0:2]]).copy(), "r")], col=col,
                    nota="M6 C18.2 (= 2u)")
        # C18.3: ∬ |2u| du dv (o 2u voa do J)
        self.gat("agora a integral do módulo")
        L3 = Lp([("ii", r"\iint_{[-1,1]\times[0,1]}"), ("m", r"\Lm{|2\uu|}"), ("d", r"\,\du\,\dv")], CX6, 0, 40)
        col.poe(L3)
        L3._xy = (CX6, centro(L3)[1])
        self.escreve_voos(L3, [(gl(L2, "r"), L3._ix["m"][1:3])])
        # C18.4: ∫₋₁¹ |2u| du = ∫₋₁⁰ (−2u) du + ∫₀¹ 2u du — a metade da direita acende com a sua parte, depois a da esquerda (mapa: |2u| se parte em dois)
        self.gat("na metade da direita")
        L4 = Lp([("i", r"\int_{-1}^{1}"), ("m", r"\Lm{|2\uu|}"), ("d", r"\,\du"), ("e", "="), ("iE", r"\int_{-1}^{0}"), ("fE", r"(-2\uu)\,\du"), ("p", "+"),
                 ("iD", r"\int_{0}^{1}"), ("fD", r"2\uu\,\du")], CX6, 0, 40)
        col.poe(L4)
        L4._xy = (CX6, centro(L4)[1])
        estava = L3 in self.mobjects
        m3, m4 = L3._ix["m"], L4._ix["m"]
        passo(self, L3, L4, [(m3, m4), ([L3._ix["d"][0], L3._ix["d"][1]], L4._ix["d"])], copia=True, rt=0.8,
              voos=[(VGroup(*[L3[0][i] for i in m3[1:3]]).copy(), L4._ix["fD"][0:2])],          # final K3: o 2u da metade esquerda vem pela caneta
              nota="M6 C18.4 (|2u| se parte nas duas metades)")
        if estava and L3 not in self.mobjects:
            self.add(L3)
        realca(self, hD, cor=CVV, rt=0.4, wpx=4)
        # C18.5: = [−u²]₋₁⁰ + [u²]₀¹ = (0 − (−1)) + (1 − 0) = 1 + 1 = 2 (a da direita primeiro, como na fala)
        # v2 (margem): a linha quebra no segundo =; a continuação fica embaixo, alinhada no =
        L5 = Lp([("e", "="), ("FE", r"\Big[-\uu^2\Big]_{-1}^{0}"), ("p", "+"), ("FD", r"\Big[\uu^2\Big]_{0}^{1}")], 0, 0, 40)
        col.poe(L5, x=eq_x(L4, "e"))
        L5._xy = (esq(L5), centro(L5)[1])
        L5b = Lp([("e2", "="), ("vE", r"(0-(-1))"), ("p2", "+"), ("vD", r"(1-0)"), ("e3", "="), ("s", "1+1"), ("e4", "="), ("r", r"\Al{2}")], 0, 0, 40)
        L5b.shift(PX(eq_x(L4, "e"), pxof(L5.get_bottom())[1] + col.GAP36 + L5b.height * 60) - PX(esq(L5b), centro(L5b)[1]))
        L5b._xy = (esq(L5b), centro(L5b)[1])
        col.registra(L5b)
        self.gat("a primitiva de dois u")
        loD, hiD = [L5._ix["FD"][-2]], [L5._ix["FD"][-1]]              # _{0}^{1}: os dois últimos glifos da peça
        iloD, ihiD = idx_lims(L4, "iD")
        voos(self, [(VGroup(*[L4[0][i] for i in iloD]), parte(L5, loD, "0")), (VGroup(*[L4[0][i] for i in ihiD]), parte(L5, hiD, "1"))], rt=0.4)
        self.pena(parte(L5, [i for i in L5._ix["e"] + L5._ix["FD"] if i not in loD + hiD], "= [u²]"))
        self.gat("um menos zero, um")
        voos(self, [(VGroup(*[L5[0][i] for i in hiD]), parte(L5b, [L5b._ix["vD"][1]], "1")), (VGroup(*[L5[0][i] for i in loD]), parte(L5b, [L5b._ix["vD"][3]], "0"))], rt=0.4)
        self.pena(parte(L5b, [L5b._ix["vD"][k] for k in (0, 2, 4)], "( − )"))
        self.gat("na da esquerda")
        realca(self, hE, cor=CU, rt=0.4, wpx=4)
        loE, hiE = L5._ix["FE"][-3:-1], [L5._ix["FE"][-1]]              # _{-1}^{0}
        iloE, ihiE = idx_lims(L4, "iE")
        voos(self, [(VGroup(*[L4[0][i] for i in iloE]), parte(L5, loE, "−1")), (VGroup(*[L4[0][i] for i in ihiE]), parte(L5, hiE, "0"))], rt=0.4)
        self.pena(parte(L5, [i for i in L5._ix["FE"] + L5._ix["p"] if i not in loE + hiE], "[−u²] +"))
        self.gat("menos menos um")
        vE = L5b._ix["vE"]                                             # ( 0 − ( − 1 ) )
        voos(self, [(VGroup(*[L5[0][i] for i in hiE]), parte(L5b, [vE[1]], "0")), (VGroup(*[L5[0][i] for i in loE]), parte(L5b, vE[4:6], "−1"))], rt=0.4)
        self.pena(parte(L5b, [vE[k] for k in (0, 2, 3, 6, 7)] + L5b._ix["e2"] + L5b._ix["p2"], "( − ( ) ) e +"))
        self.gat("somando")
        voos(self, [(VGroup(*[L5b[0][i] for i in vE]), parte(L5b, [L5b._ix["s"][0]], "1")), (VGroup(*[L5b[0][i] for i in L5b._ix["vD"]]), parte(L5b, [L5b._ix["s"][2]], "1"))],
             rt=0.4)
        self.pena(parte(L5b, L5b._ix["e3"] + [L5b._ix["s"][1]], "= +"))
        voos(self, [(VGroup(*[L5b[0][i] for i in L5b._ix["s"]]), parte(L5b, L5b._ix["r"], "2"))], rt=0.4)
        self.pena(parte(L5b, L5b._ix["e4"], "="))
        L5 = L5b
        # C18.6: ∫₀¹ 2 dv = [2v]₀¹ = 2 − 0 = 2
        self.gat("em vê")
        L6 = Lp([("i", r"\int_{\Vc{0}}^{\Vc{1}}"), ("f", "2"), ("d", r"\,\dv")], CX6, 0, 40)
        col.poe(L6)
        L6._xy = (CX6, centro(L6)[1])
        self.escreve_voos(L6, [(gl(L5, "r"), "f")])
        self.gat("dois vê")
        L6 = cresce(self, L6, [("e1", "="), ("lb", r"\Big["), ("F", r"2\vv"), ("rb", r"\Big]"), ("sb", r"_{\Vc{0}}^{\Vc{1}}")],
                    voos=lambda B: [(VGroup(*[L6[0][k] for k in idx_lims(L6, "i")[0]]).copy(), lims_sb(B, "sb")[0]),
                                    (VGroup(*[L6[0][k] for k in idx_lims(L6, "i")[1]]).copy(), lims_sb(B, "sb")[1]), (gl(L6, "f").copy(), [B._ix["F"][0]])],
                    col=col, nota="M6 C18.6 colchete")
        self.gat("dois menos zero")
        L6 = cresce(self, L6, [("e2", "="), ("g", "2-0")], voos=lambda B: [(gl(L6, "F").copy(), [B._ix["g"][0]]),
                                                                       (VGroup(*[L6[0][k] for k in lims_sb(L6, "sb")[0]]).copy(), [B._ix["g"][2]])],
                    col=col, nota="M6 C18.6 G(1) − G(0)")
        L6 = cresce(self, L6, [("e3", "="), ("r", r"\Al{2}")], voos=lambda B: [(gl(L6, "g").copy(), "r")], col=col, nota="M6 C18.6 = 2")
        # C18.7: ÁREA DA IMAGEM = 1 · 1 = 1 (BASE e ALTURA com chave no quadrado) → 2 ≠ 1
        self.gat("a área do quadrado é um")
        chB = chave_h(VX6.px(0, 0)[0] + 4, VX6.px(1, 0)[0] - 4, VX6.px(0, 0)[1] + 46, GEO, 2, para_baixo=True)
        lBa = TP(r"\Ge{1}", (VX6.px(0, 0)[0] + VX6.px(1, 0)[0]) / 2, VX6.px(0, 0)[1] + 82, 26, "c")
        tBa = leg("BASE", VX6.px(1, 0)[0] + 10, VX6.px(0, 0)[1] + 66, GEO, "left", 26)
        # a ALTURA fica do lado esquerdo do quadrado (à direita só há o vão estreito até a coluna)
        chA = chave_v(VX6.px(0, 0)[0] - 44, VX6.px(0, 1)[1] + 4, VX6.px(0, 0)[1] - 4, GEO, 2, para_esq=True)
        lAl = TP(r"\Ge{1}", VX6.px(0, .5)[0] - 70, VX6.px(0, .5)[1], 26, "r")
        tAl = leg("ALTURA", VX6.px(0, .5)[0] - 100, VX6.px(0, .5)[1] + 10, GEO, "right", 26)
        self.play(Create(chB), Create(chA), run_time=0.5)
        self.pena(lBa, tBa, lAl, tAl, lag=0.1)
        k3t, K3 = mixLp("ÁREA DA IMAGEM", [("e", "="), ("a", "1"), ("x", r"\cdot"), ("b", "1"), ("e2", "="), ("r", "1")], CX6, 0, 40)
        y3 = col.y_prox(K3)
        VGroup(k3t, K3).shift(UP * (PX(0, y3)[1] - K3.get_center()[1]))
        K3._xy = (esq(K3), y3)
        col.registra(K3)
        yK3 = centro(K3)[1]
        self.escreve_voos(K3, [(lBa.f, "a", [(centro(lBa)[0], yK3)]), (lAl.f, "b", [(centro(lAl)[0], yK3)])], depois=["e2", "r"])   # descem e entram pela linha
        self.pena(k3t)
        K4 = Lp([("a", r"\Al{2}"), ("n", r"\Al{\neq}"), ("b", r"\Al{1}")], CX6 + 300, 0, 48)
        K4.move_to(PX(dir_(K3) + 70 + K4.width * 60, centro(K3)[1]))           # ao lado da área da imagem
        col.registra(K4)
        self.pena(parte(K4, K4._ix["n"], "≠"))
        voos(self, [(gl(L6, "r").copy(), parte(K4, K4._ix["a"], "2"), [(dir_(L6) + 50, centro(L6)[1]), (dir_(L6) + 50, centro(K4)[1])]),
                    (gl(K3, "r").copy(), parte(K4, K4._ix["b"], "1"))], rt=0.8)
        self.gat("é a sobreposição")
        realca(self, sq, cor=AL, rt=0.4, wpx=6)
        sl = selo("SOBREPOSIÇÃO: CONTOU DUAS VEZES", 90, 760, AL, 26)
        poe_selo(self, sl)
        self.marca("13", agora=True)
        # Q11: J = 2u = 0 à direita da reta da dobra (u = 0), com placa, longe do eixo v
        self.gat("zera no meio")
        l0 = lin_px([VU6.px(0, -.05), VU6.px(0, 1.05)], AL, 4, z=5)
        lj = TP(r"\Al{J=2\uu=0}", VU6.px(.08, .9)[0], VU6.px(.08, .9)[1], 26, "l")       # à direita da dobra, dentro da metade direita, longe do eixo v
        self.play(Create(l0), run_time=0.5)
        self.pena(lj)
        self.gat("já na borda")
        realca(self, bd, cor=LIMA, rt=0.5, wpx=4)
        # §6.6: fica só com a metade da direita — u = 0 vira borda; a imagem continua o quadrado inteiro; a integral dá 1 ✓
        self.gat("fica só com a metade")
        self.play(FadeOut(hE), FadeOut(dE), FadeOut(lj), run_time=0.6)
        self.remove(hE, dE, lj)
        self.gat("é borda")
        realca(self, l0, cor=AL, rt=0.4, wpx=6)
        lb0 = rotm([("m", r"\Uc{\uu=0}"), ("t", "É BORDA:", AL), ("m", r"\Al{J=0}"), ("t", "SÓ ALI", AL)], VU6.px(-1.12, -.42)[0], VU6.px(-1.12, -.42)[1], 26, "l")   # sob o eixo u (≥ 48 px da borda)
        self.pena(lb0)
        self.gat("a área certa")
        L8 = Lp([("ii", r"\iint_{[0,1]\times[0,1]}"), ("f", r"\Lm{2\uu}\,\du\,\dv")], CX6, 0, 40)
        col.poe(L8, gap=40)
        L8._xy = (CX6, centro(L8)[1])
        self.escreve_voos(L8, [(VGroup(*[L4[0][i] for i in L4._ix["fD"]]), "f")])
        L8 = cresce(self, L8, [("e1", "="), ("i2", r"\int_0^1"), ("b", r"\Big[\uu^2\Big]_0^1\,\dv")], col=col, nota="M6 C18.8 colchete")
        L8 = cresce(self, L8, [("e2", "="), ("i3", r"\int_0^1"), ("g", r"(1-0)\,\dv"), ("e3", "="), ("r", r"\Lm{1}")], col=col, nota="M6 C18.8 = 1")
        ck = check_px(dir_(L8) + 30, centro(L8)[1], MEN)
        self.play(Create(ck), run_time=0.4)
        # final K9: o ✓ do C18.8 fica ≥ 2,0 s antes do B5-4 (se a fala acabar antes, a âncora seguinte começa mais tarde: [estouro])
        t_ck = self.t
        self._hold = True
        self.wait(2.0)
        self._hold = False
        print(f"[hold] {self._aid} C18.8 ✓ parado ≥ {self.t - t_ck:.2f} s")

        # ════ B5-4 · conferindo o teorema (C8 e C9: cada colchete → G(b) − G(a) → número) ════
        self.an("B5-4")
        self.limpa_tudo()
        self.secao("CONFERINDO O TEOREMA")
        self.fundo(VR, rt=0.3)
        d = plano(self, VR, AR, 1.15, 2.2, -1.1, -.05)
        reg = poly_px([VR.px(*mapC(1, t)) for t in np.linspace(0, 1, 40)] + [VR.px(*mapC(t, 1)) for t in np.linspace(1, 0, 40)], RB, 1.0, z=1)
        eU = lin_px([VR.px(*mapC(1, t)) for t in np.linspace(0, 1, 60)], CORAL, 3, z=5)
        eV = lin_px([VR.px(*mapC(t, 1)) for t in np.linspace(0, 1, 60)], AZC, 3, z=5)
        self.play(FadeIn(reg), Create(eU), Create(eV), run_time=0.8)
        CX7 = 930                                                      # v2 (margem): as linhas do C8 e o ✓ do C9 cabem até x = 1872
        col = Coluna36(self, CX7, 200)
        col.GAP36 = 24
        self.gat("com f igual a um")
        t1, G1 = mixLp("ÁREA", [("e", "="), ("i", r"\iint_{[0,1]^2}"), ("f", r"\Lm{(4\uu^2+4\vv^2)}"), ("d", r"\,\du\,\dv")], CX7, 0, 40)
        y_ = col.y_prox(G1)
        VGroup(t1, G1).shift(UP * (PX(0, y_)[1] - G1.get_center()[1]))
        col.registra(G1)
        self.pena(t1, G1, lag=0.2)
        self.gat("por dentro, em u")
        G2 = Lp([("i", r"\int_{\Uc{0}}^{\Uc{1}}"), ("f", r"(4\uu^2+4\vv^2)\,\du")], CX7, 0, 40)
        col.poe(G2)
        G2._xy = (CX7, centro(G2)[1])
        self.escreve_voos(G2, [(gl(G1, "f"), G2._ix["f"][:-2])])
        G2 = cresce(self, G2, [("e1", "="), ("lb", r"\Big["), ("F", r"\dfrac{4\uu^3}{3}+4\vv^2\uu"), ("rb", r"\Big]"), ("sb", r"_{\uu=0}^{\uu=1}")],
                    voos=lambda B: [(VGroup(*[G2[0][k] for k in idx_lims(G2, "i")[0]]).copy(), [lims_sb(B, "sb")[0][-1]]),
                                    (VGroup(*[G2[0][k] for k in idx_lims(G2, "i")[1]]).copy(), [lims_sb(B, "sb")[1][-1]])], col=col, nota="M7 C8.2 colchete u")
        # C8.3 (mapa): em u = 1 → (4/3 + 4v²); em u = 0 → (0 + 0)
        self.gat("em um, quatro terços")
        F2 = G2._ix["F"]                                                # 4 u 3 — 3 + 4 v 2 u
        G3 = deriva(self, G2, [("e", "="), ("g1", r"\left(\dfrac{4}{3}+4\vv^2\right)"), ("m", "-"), ("g0", r"(0+0)")],
                    lambda B: [("e1", "e"), ([F2[0], F2[3], F2[4]], [B._ix["g1"][k] for k in (1, 2, 3)]), ([F2[5]], [B._ix["g1"][4]]), (F2[6:9], B._ix["g1"][5:8])],
                    col, x=eq_x(G2, "e1"), rt=1.0, nota="M7 C8.3 (u = 1: G(1))")
        self.gat("quatro vê ao quadrado em zero")
        realca(self, VGroup(*[G3[0][i] for i in G3._ix["g0"]]), cor=GEO, rt=0.3, wpx=3)
        self.gat("fica quatro terços")
        G3 = cresce(self, G3, [("e2", "="), ("r", r"\dfrac{4}{3}+4\vv^2")], voos=lambda B: [(VGroup(*[G3[0][i] for i in G3._ix["g1"][1:-1]]).copy(), "r")],
                    col=col, nota="M7 C8.3 (= 4/3 + 4v²)")
        self.gat("por fora, em vê")
        G4 = Lp([("i", r"\int_{\Vc{0}}^{\Vc{1}}"), ("f", r"\left(\dfrac{4}{3}+4\vv^2\right)\dv")], CX7, 0, 40)
        col.poe(G4)
        G4._xy = (CX7, centro(G4)[1])
        ym4 = (pxof(G3.get_bottom())[1] + pxof(G4.get_top())[1]) / 2          # pelo vão entre a linha de cima e a de baixo (sem cruzar texto)
        idx4 = [G4._ix["f"][k] for k in range(1, len(G4._ix["f"]) - 3)]
        self.escreve_voos(G4, [(gl(G3, "r"), idx4, [(centro(gl(G3, "r"))[0], ym4), (centro(VGroup(*[G4[0][i] for i in idx4]))[0], ym4)])])
        G4 = cresce(self, G4, [("e1", "="), ("lb", r"\Big["), ("F", r"\dfrac{4\vv}{3}+\dfrac{4\vv^3}{3}"), ("rb", r"\Big]"), ("sb", r"_{\Vc{0}}^{\Vc{1}}")],
                    voos=lambda B: [(VGroup(*[G4[0][k] for k in idx_lims(G4, "i")[0]]).copy(), lims_sb(B, "sb")[0]),
                                    (VGroup(*[G4[0][k] for k in idx_lims(G4, "i")[1]]).copy(), lims_sb(B, "sb")[1])], col=col, nota="M7 C8.4 colchete v")
        # C8.5 (mapa): (4/3 + 4/3) − (0 + 0) = 8/3
        self.gat("quatro terços mais quatro terços")
        F4 = G4._ix["F"]                                                # 4 v — 3 + 4 v 3 — 3
        G5 = deriva(self, G4, [("e", "="), ("g1", r"\left(\dfrac{4}{3}+\dfrac{4}{3}\right)"), ("m", "-"), ("g0", r"(0+0)")],
                    lambda B: [("e1", "e"), ([F4[0], F4[2], F4[3]], [B._ix["g1"][k] for k in (1, 2, 3)]), ([F4[4]], [B._ix["g1"][4]]),
                               ([F4[5], F4[8], F4[9]], [B._ix["g1"][k] for k in (5, 6, 7)])], col, x=eq_x(G4, "e1"), rt=1.0, nota="M7 C8.5 (v = 1: G(1))")
        self.gat("oito terços")
        G5 = cresce(self, G5, [("e2", "="), ("r", r"\Lm{\dfrac{8}{3}}")], voos=lambda B: [(VGroup(*[G5[0][i] for i in G5._ix["g1"][1:-1]]).copy(), "r")],
                    col=col, nota="M7 C8.5 (= 8/3)")
        t83 = self.t
        # final K10: o 8/3 fica escrito no fim da escada (≥ 2,5 s); a escada sai em fade (0,6 s), menos o 8/3, que VOA para COM J: ÁREA = 8/3
        self.gat("sem jacobiano")
        if self.t - t83 < 2.5:
            self._hold = True
            self.wait(2.5 - (self.t - t83) + 0.07)                         # + 1 quadro: o arredondamento não deixa abaixo de 2,5 s
            self._hold = False
        print(f"[hold] {self._aid} 8/3 parado {self.t - t83:.2f} s")
        r83 = VGroup(*[G5[0][i] for i in G5._ix["r"]])
        resto5 = VGroup(*[G5[0][i] for i in range(len(G5[0])) if i not in G5._ix["r"]])
        sai8 = [t1, G1, G2, G3, G4]
        self.play(*[FadeOut(m) for m in sai8], resto5.animate.set_opacity(0), run_time=0.6)      # o resto da linha some sem desmontar a linha
        self.remove(*sai8)
        lab8 = mixl([("t", "COM J:", LIMA), ("t", "ÁREA"), ("m", "=")], CX7, 230, 40)
        val8 = TC(r"\Lm{\dfrac{8}{3}}", dir_(lab8) + 10, 230, 40, "l")
        self.pena(lab8)
        voa(self, r83, val8, rt=0.8)
        self.remove(G5, r83, lab8, val8)
        chip8 = VGroup(lab8, val8)
        self.add(chip8)
        col.ls = [chip8]
        yf = 1.0
        tH = tiraH(VR, yf, yf * yf / 4 - 1, 1 - yf * yf / 4, h=.06, cor=E2)
        pe, ps_ = pontos_es(VR, (yf * yf / 4 - 1, yf), (1 - yf * yf / 4, yf))
        self.play(FadeIn(tH), run_time=0.5)
        self.gat("entra na parábola")
        realca(self, eV, cor=AZC, rt=0.2, wpx=6)
        self.play(FadeIn(pe), run_time=0.3)
        lv1 = TP(r"\Vc{\vv=1}", VR.px(-.95, .45)[0] - 18, VR.px(-.95, .45)[1], 26, "r")             # a borda tem nome: é esse glifo que voa (nada de curva virando fórmula)
        self.pena(lv1)
        n2a = Lp([("v", r"\vv=1"), ("a", r":\ \X=\uu^2-1,\ \ \Y=2\uu")], CX7, 0, 40)
        col.poe(n2a)
        n2a._xy = (CX7, centro(n2a)[1])
        self.escreve_voos(n2a, [(lv1.f, "v")], rt=0.9)
        a2 = n2a._ix["a"]                                               # : x = u ² − 1 , y = 2 u
        n2b = deriva(self, n2a, [("i1", r"\Rightarrow\uu=\dfrac{\Y}{2}"), ("i2", r"\ \Rightarrow\Az{\X=\dfrac{\Y^2}{4}-1}")],
                     lambda B: [([a2[11]], [B._ix["i1"][1]]), ([a2[9]], [B._ix["i1"][2]]), ([a2[8]], [B._ix["i1"][3]]), ([a2[10]], [B._ix["i1"][5]]),
                                ([a2[1]], [B._ix["i2"][1]]), ([a2[2]], [B._ix["i2"][2]]), ([a2[3]], [B._ix["i2"][3]]), ([a2[4]], [B._ix["i2"][4]]),
                                ([a2[5]], [B._ix["i2"][7]]), ([a2[6]], [B._ix["i2"][8]])],
                     col, x=CX7 + 40, rt=1.0, nota="M7 C9 (y = 2u ⇒ u = y/2 ⇒ x = y²/4 − 1)")
        lE = T("ENTRADA", dir_(n2b) + 16, centro(n2b)[1] + 9, 26, "left", AZC, bold=False)
        self.pena(lE)
        self.gat("e sai na da direita")
        realca(self, eU, cor=CORAL, rt=0.2, wpx=6)
        self.play(FadeIn(ps_), run_time=0.3)
        lu1 = TP(r"\Uc{\uu=1}", VR.px(.95, .45)[0] + 18, VR.px(.95, .45)[1], 26, "l")
        self.pena(lu1)
        n1a = Lp([("u", r"\uu=1"), ("a", r":\ \X=1-\vv^2,\ \ \Y=2\vv")], CX7, 0, 40)
        col.poe(n1a)
        n1a._xy = (CX7, centro(n1a)[1])
        self.escreve_voos(n1a, [(lu1.f, "u", [(centro(lu1)[0], centro(n1a)[1])])], rt=0.9)          # desce e entra pela linha (por baixo da de cima)
        a1 = n1a._ix["a"]                                               # : x = 1 − v ² , y = 2 v
        n1b = deriva(self, n1a, [("i1", r"\Rightarrow\vv=\dfrac{\Y}{2}"), ("i2", r"\ \Rightarrow\Co{\X=1-\dfrac{\Y^2}{4}}")],
                     lambda B: [([a1[11]], [B._ix["i1"][1]]), ([a1[9]], [B._ix["i1"][2]]), ([a1[8]], [B._ix["i1"][3]]), ([a1[10]], [B._ix["i1"][5]]),
                                ([a1[1]], [B._ix["i2"][1]]), ([a1[2]], [B._ix["i2"][2]]), ([a1[3]], [B._ix["i2"][3]]), ([a1[4]], [B._ix["i2"][4]]),
                                ([a1[5]], [B._ix["i2"][5]]), ([a1[6]], [B._ix["i2"][6]])],
                     col, x=CX7 + 40, rt=1.0, nota="M7 C9 (y = 2v ⇒ v = y/2 ⇒ x = 1 − y²/4)")
        lS = T("SAÍDA", dir_(n1b) + 16, centro(n1b)[1] + 9, 26, "left", CORAL, bold=False)
        self.pena(lS)
        self.gat("a saída menos a entrada")
        t3_, G6 = mixLp("COMPRIMENTO", [("e", "="), ("s", r"\Co{\left(1-\dfrac{\Y^2}{4}\right)}"), ("m", "-"), ("en", r"\Az{\left(\dfrac{\Y^2}{4}-1\right)}")], CX7, 0, 40)
        y6 = col.y_prox(G6, gap=30)
        VGroup(t3_, G6).shift(UP * (PX(0, y6)[1] - G6.get_center()[1]))
        G6._xy = (esq(G6), y6)
        col.registra(G6)
        self.escreve_voos(G6, [(VGroup(*[n1b[0][i] for i in n1b._ix["i2"][3:]]), [G6._ix["s"][k] for k in range(1, len(G6._ix["s"]) - 1)]),
                               (VGroup(*[n2b[0][i] for i in n2b._ix["i2"][3:]]), [G6._ix["en"][k] for k in range(1, len(G6._ix["en"]) - 1)])])
        self.pena(t3_)
        self.gat("distribuindo o sinal")                                # final §4: "Distribuindo o sinal" → = 2 − y²/2
        G6 = cresce(self, G6, [("e2", "="), ("r", r"2-\dfrac{\Y^2}{2}")], voos=lambda B: [(VGroup(gl(G6, "s"), gl(G6, "en")).copy(), "r")], col=col,
                    nota="C9 (saída − entrada)")
        self.gat("a primitiva é dois")
        G7 = Lp([("i", r"\int_{\Mg{0}}^{\Mg{2}}"), ("f", r"\left(2-\dfrac{\Y^2}{2}\right)\dY"), ("e1", "="), ("lb", r"\Big["), ("F", r"2\Y-\dfrac{\Y^3}{6}"),
                 ("rb", r"\Big]"), ("sb", r"_{\Mg{0}}^{\Mg{2}}")], CX7, 0, 40)
        col.poe(G7)
        G7._xy = (CX7, centro(G7)[1])
        self.escreve_voos(G7, [(gl(G6, "r"), [G7._ix["f"][k] for k in range(1, len(G7._ix["f"]) - 3)])])
        # C9.4 (mapa): em y = 2 → (4 − 8/6); em y = 0 → (0 − 0); 4 − 8/6 = 4 − 4/3 = 8/3
        self.gat("em dois, quatro menos")
        F7 = G7._ix["F"]                                                # 2 y − y 3 — 6
        G8 = deriva(self, G7, [("e", "="), ("g2", r"\left(4-\dfrac{8}{6}\right)"), ("m", "-"), ("g0", r"(0-0)")],
                    lambda B: [("e1", "e"), ([F7[2]], [B._ix["g2"][2]]), ([F7[5]], [B._ix["g2"][4]]), ([F7[6]], [B._ix["g2"][5]])],
                    col, x=eq_x(G7, "e1"), rt=1.0, nota="M7 C9.4 (G(2) − G(0))")
        self.gat("quatro menos quatro terços")
        G8 = cresce(self, G8, [("e2", "="), ("s", r"4-\dfrac{4}{3}")], voos=lambda B: [(VGroup(*[G8[0][i] for i in G8._ix["g2"][1:-1]]).copy(), "s")],
                    col=col, nota="M7 C9.4 (8/6 → 4/3)")
        self.gat("quatro terços, oito terços")
        G8 = cresce(self, G8, [("e3", "="), ("r", r"\Lm{\dfrac{8}{3}}")], voos=lambda B: [(gl(G8, "s").copy(), "r")], col=col, nota="M7 C9.4 (= 8/3)")
        self.gat("bateu")
        ck = check_px(dir_(G8) + 32, centro(G8)[1], MEN)
        self.play(Create(ck), run_time=0.4)
        self.marca("B5-4")
        self.sai_fim()
