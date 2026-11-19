"""yt_0032 · B6 · valor médio (alvos 18 v2, 19, 20 v2, 21, 22 v2). 3D: b61 (terraplanagem até 8/3). Depois 2D e cartões.
v2: média com fórmula-mãe e mapa M12 (D8); nível só tracejado, legendas saem com o objeto, 8/3 em dfrac (R6); Space Grotesk e ✓/✗ com respiro
(T1, T5); prova com ÷ α (M7) e conclusão ∬f = α f(r, s) (M8), gráfico com 0, 8/3 e 8 (R7); degraus com o salto; cartões dizem qual média (R8)."""
from lib32 import *

R83 = math.sqrt(8 / 3)


def arco_r(v, r, cor, wpx, a0=0.0, a1=PI / 2, n=90, z=6):
    return lin_px([v.px(r * math.cos(a0 + (a1 - a0) * k / n), r * math.sin(a0 + (a1 - a0) * k / n)) for k in range(n + 1)], cor, wpx, z=z)


def caminho(t):
    return (2 * t + .35 * math.sin(PI * t), 2 * t - .35 * math.sin(PI * t))


class PB6(B32):
    ANTES = "DIVIDIR A REGIÃO"

    def corpo(self):
        # ── B6-1 · a terraplanagem (alvo 18 v2), 3D b61 ──
        self.an("B6-1")
        self.secao("VALOR MÉDIO")
        pal = Palco3D(self, "b61", CAM_PREDIO, cresce=0.0, nivel=0.0, acende=0.0, nivela=0.0, arco=0.0, raio=0.0)
        pal.fundo.op.set_value(0.0)
        self.add(pal.fundo)
        self.play(pal.fundo.op.animate.set_value(1.0), run_time=0.9)
        # fontes dos números da média (D8): a régua da massa e a área
        self.gat("a massa é trinta")
        cm_ = L([("lab", r"\text{massa}="), ("v", r"\Ci{32/3}"), ("u", r"\ \text{kg}")], 1120, 880, 36)
        self.pena(cm_)
        self.gat("e a área é")
        ca_ = L([("lab", r"\text{área}="), ("v", "4"), ("u", r"\ \text{m}^2")], 1500, 880, 36)
        self.pena(ca_)
        self.gat("dividindo a densidade média")
        M0 = L([("m", r"\text{média}"), ("eq", "="), ("fr", r"\dfrac{\text{massa}}{\text{área}}")], 1120, 250, 38)
        self.pena(M0)                                     # a fórmula-mãe antes do número
        x1 = pxof(M0.get_right())[0] + 14
        K1 = L([("e2", "="), ("fv", r"\dfrac{\Ci{32/3}}{4}")], x1, 250, 38)
        fv = K1._ix["fv"]
        self.escreve(K1, voos=[(gl(cm_, "v"), fv[0:4]), (gl(ca_, "v"), [fv[5]])], atraso_caneta=0.2)
        K2 = L([("e2", "="), ("fv", r"\dfrac{\Ci{32/3}}{4}"), ("e3", "="), ("r", r"\Ci{\dfrac{8}{3}}"), ("ap", r"\approx\Ci{2{,}67}")], x1, 250, 38)
        gm(self, K1, K2, [("e2", "e2"), ("fv", "fv"), ("fv", "r")], rt=1.4, copia=True, nota="mapa 12 (M12, B6-1: (32/3)/4 = 8/3)")
        self.remove(K1)
        self.some(cm_, ca_, rt=0.4)
        self.gat("agora transforma a densidade")
        self.play(*pal.anim(2.6, cresce=1.0), run_time=2.6)
        self.gat("se nivelarmos tudo")
        l83 = pal.prende(TP(r"\Ci{\dfrac{8}{3}}", 0, 0, 38), "nivel", 34, 4, "l")
        self.pena(l83, extra=pal.anim(1.1, rate=linear, nivel=1.0), rt=1.1)        # R6: só o retângulo tracejado no topo; sync: o 8/3 nasce enquanto sobe
        self.gat("olha a terraplanagem")
        self.play(*pal.anim(0.8, acende=1.0), run_time=0.8)
        la = pal.prende(TPt("ACIMA DO NÍVEL", 0, 0, 26, CORAL), "acima", -20, -40, "r")
        self.pena(la)
        self.gat("vai preencher o espaço")
        lb = pal.prende(TPt("O QUE FALTA", 0, 0, 26, MEN), "abaixo", -160, -40, "l")
        self.pena(lb, extra=pal.anim(1.8, nivela=1.0), rt=1.8)                   # sync: o morro nivela enquanto a legenda nasce
        self.some(la, lb, rt=0.4)                         # R6: cada legenda sai com o que ela legenda
        self.gat("o volume retirado e")
        Vv = TC(r"\Co{\text{acima}}=\Me{\text{abaixo}}=\dfrac{8\pi}{9}\approx 2{,}79", 1120, 390, 38)
        self.pena(Vv)
        lt = leg("A TERRAPLANAGEM NIVELA NA MÉDIA", 1120, 460, GEO, "left", 26)
        self.pena(lt)
        self.gat("mas será que algum")
        self.play(*pal.anim(3.2, rate=linear, arco=1.0), run_time=3.2)
        self.gat("todos os pontos deste")
        Ar = L([("x2", r"\X^2+\Y^2"), ("eq", r"\Lr{=}"), ("fr", r"\Lr{\dfrac{8}{3}}")], 1120, 570, 40)
        self.pena(Ar)
        lr = leg("ONDE f = MÉDIA", 1120, 640, POS, "left", 26)
        self.pena(lr)
        self.gat("a um vírgula sessenta")                 # C6 (final): o raio com conta (mapa 15) e o segmento r no 3D
        lr_ = pal.prende(TP(r"\Lr{r}", 0, 0, 28), "rmeio", 0, -24)
        ld = leg("r: DISTÂNCIA ATÉ A ORIGEM", 1500, 580, GEO, "left", 26)
        self.pena(lr_, ld, lag=0.2, passo=0.04, extra=pal.anim(1.2, raio=1.0), rt=1.2)   # sync: o segmento r cresce enquanto r e a legenda nascem
        R1 = L([("r2", r"\Lr{r^2}"), ("eq", r"\Lr{=}"), ("fr", r"\Lr{\dfrac{8}{3}}")], 1120, 570, 40)
        gm(self, Ar, R1, [("x2", "r2"), ("eq", "eq"), ("fr", "fr")], rt=0.9, nota="mapa 15a (C6, B6-1: x² + y² = r²)")
        R2 = L([("r", r"\Lr{r}"), ("eq", r"\Lr{=}"), ("sq", r"\Lr{\sqrt{\dfrac{8}{3}}}"), ("ap", r"\approx\Lr{1{,}63}")], 1120, 570, 40)
        r2i = R1._ix["r2"]
        gm(self, R1, R2, [([r2i[0]], "r"), ("eq", "eq"), ("fr", R2._ix["sq"][1:]), ([r2i[1]], [R2._ix["sq"][0]])], rt=1.0,
           nota="mapa 15b (C6, B6-1: r = √(8/3) ≈ 1,63)")
        self.marca("18")

        # ── B6-2 · o teorema aparece (alvo 19), 2D ──
        self.an("B6-2")
        self.limpa(rt=0.5)
        self.grade_on(CH, rt=0.3)
        mapa = img_chapa(arr_dens(64), CH)
        bord = borda_ch(CH, GEO, 3)
        sx, sy, lx, ly = eixos_chapa(CH)
        arco = arco_r(CH, R83, POS, 4)
        self.play(FadeIn(mapa), FadeIn(bord), GrowFromPoint(sx, CH.P(0, 0)), GrowFromPoint(sy, CH.P(0, 0)), run_time=0.8)
        self.pena(lx, ly)
        self.play(Create(arco), run_time=0.8)
        self.gat("as hipóteses a região")
        H1 = mista([("m", "B"), ("t", "COMPACTO, FRONTEIRA DE CONTEÚDO NULO")], 1120, 410, 28)      # T1
        self.pena(H1)
        self.gat("fechada quer dizer que")
        i1 = VGroup(circ_px(1150, 250, 38, BR, 3, fill=mixh(BG_, CI, .3), fop=1, z=4), check_px(1218, 250, MEN, .7))    # T5: ✓ à direita, com respiro
        i2 = VGroup(circ_px(1330, 250, 38, BR, 3, dash=(6, 5), z=4), cruz_px(1398, 250, AL, .7))
        i2.add_to_back(circ_px(1330, 250, 38, BR, 0, fill=mixh(BG_, CI, .3), fop=1, z=3))
        t1, t2 = leg("FECHADO", 1150, 320, GEO, "center", 26), leg("ABERTO", 1330, 320, GEO, "center", 26)
        self.play(GrowFromCenter(i1[0]), run_time=0.4)
        self.play(Create(i1[1]), run_time=0.3)
        self.pena(t1)
        self.play(GrowFromCenter(i2[0]), Create(i2[1]), run_time=0.4)
        self.play(Create(i2[2]), run_time=0.3)
        self.pena(t2)
        self.gat("limitada que cabe dentro")
        i3 = VGroup(ret_px(1450, 222, 1590, 278, fill=mixh(BG_, CI, .3), z=3), lin_px([(1450, 222), (1590, 222)], GEO, 3, z=4),
                    lin_px([(1450, 278), (1590, 278)], GEO, 3, z=4), cruz_px(1626, 250, AL, .7))
        t3 = leg("ILIMITADO", 1520, 320, GEO, "center", 26)
        self.play(GrowFromEdge(i3[0], LEFT), Create(i3[1]), Create(i3[2]), run_time=0.6)
        self.play(Create(i3[3]), run_time=0.3)
        self.pena(t3)
        self.gat("dois pontos quaisquer da")
        pA = ponto_px(*CH.px(0.4, 1.5), BR, 6, z=9)       # C15 (final): dois pontos quaisquer e um caminho que não sai de B
        pB = ponto_px(*CH.px(1.7, 0.4), BR, 6, z=9)
        self.play(FadeIn(pA, scale=0.4), FadeIn(pB, scale=0.4), run_time=0.4)
        H2 = mista([("t", "CAMINHO DENTRO DE"), ("m", r"B,\ \ \f"), ("t", "CONTÍNUA")], 1120, 465, 28)
        self.pena(H2)
        self.gat("por um caminho contínuo")
        cam15 = CubicBezier(CH.P(0.4, 1.5), CH.P(0.7, 0.6), CH.P(1.3, 1.6), CH.P(1.7, 0.4)).set_stroke(POS, W(3)).set_fill(opacity=0)
        cam15 = sem_ctn(cam15).set_z_index(8)
        self.play(Create(cam15), run_time=1.2)
        self.gat("e a função é contínua")
        self.play(FadeOut(cam15), FadeOut(pA), FadeOut(pB), run_time=0.4)
        self.remove(cam15, pA, pB)
        self.gat("com essas condições existe")
        Te = L([("imp", r"\Rightarrow\ "), ("ex", r"\exists"), ("rs", r"\,\Lr{(r,s)}\in B:\ \iint_B\f="), ("al", r"\al"), ("fr", r"\,\f(\Lr{r,s})")], 1120, 580, 42)
        self.pena(Te, passo=0.045)                         # sync: caneta um pouco mais rápida
        self.gat("existe pelo menos um")
        self.sublinha(gl(Te, "ex"), 0.6)
        self.gat("érre ésse da região")
        p = (R83 * math.cos(.7), R83 * math.sin(.7))
        pt = ponto_px(*CH.px(*p), POS, 10, z=8)
        self.play(FadeIn(pt, scale=0.3), run_time=0.4)
        lrs = TP(r"(r,s)", *CH.px(1.42, 1.3), 30, "l")
        self.pena(lrs)
        self.gat("na fórmula a integral")
        self.sublinha(gl(Te, "rs", "al", "fr"), 2.4)
        self.gat("sendo alfa a área")
        self.sublinha(gl(Te, "al"), 0.6)
        la = leg("α = ÁREA DE B", 1120, 645, GEO, "left", 26)
        self.pena(la)
        self.gat("em outras palavras desde")
        lu = leg("UM PONTO VALE EXATAMENTE A MÉDIA", 1120, 710, POS, "left", 26)    # T7: respiro ≥ 0,2
        self.pena(lu)
        self.marca("19")

        # ── B6-3 · por que isso é verdade? (alvo 20 v2) ──
        self.an("B6-3")
        v = Vw(200, 800, 190)
        sai = [m for m in self.snap() if m not in (mapa, bord)]
        k = 190 / 240
        ch = Group(mapa, bord)
        ch.generate_target()
        ch.target.scale(k, about_point=PX(360, 780)).shift(PX(200, 800) - PX(360, 780))
        self.play(*[FadeOut(m) for m in sai], MoveToTarget(ch), run_time=1.2)
        for m in sai:
            m.clear_updaters()
        self.remove(*sai)
        self.grade_off(rt=0)
        self.grade_on(v, rt=0.3)
        arco2 = arco_r(v, R83, POS, 3)                     # R7: o arco volta a ter cor
        self.play(Create(arco2), run_time=0.6)
        self.gat("ela atinge um mínimo")
        pmin, pmax = ponto_px(*v.px(0, 0), AZC, 11, z=8), ponto_px(*v.px(2, 2), CORAL, 11, z=8)
        self.play(FadeIn(pmin, scale=0.3), FadeIn(pmax, scale=0.3), run_time=0.5)
        self.gat("o mínimo é zero")
        lmin = TP(r"m=\f(0,0)=0", *v.px(.15, -.22), 28, "l")
        self.pena(lmin)
        self.gat("e o máximo é")
        lmax = TP(r"M=\f(2,2)=2^2+2^2=8", *v.px(0.95, 2.24), 28, "l")
        self.pena(lmax)
        self.gat("pela comparação a integral")
        C1 = L([("m", r"m\cdot\al"), ("le1", r"\le"), ("ii", r"\iint_B\f"), ("le2", r"\le"), ("M", r"M\cdot\al")], 1200, 250, 38)
        self.escreve(C1, voos=[(lmin.f[0][0], [C1._ix["m"][0]]), (lmax.f[0][0], [C1._ix["M"][0]])], atraso_caneta=0.2)   # C7 (final)
        self.gat("dividindo pela área a")
        # M7 (v2): os dois α deslizam para baixo de uma barra de fração; só depois ∬f/α vira média
        C1b = L([("m", "m"), ("le1", r"\le"), ("fr", r"\dfrac{\iint_B\f}{\al}"), ("le2", r"\le"), ("M", "M")], 1200, 345, 38)
        fr = C1b._ix["fr"]
        cm, cM = C1._ix["m"], C1._ix["M"]
        gm(self, C1, C1b, [([cm[0]], "m"), ("le1", "le1"), ("ii", fr[0:4]), ([cm[2]], [fr[5]]), ([cM[2]], [fr[5]]), ("le2", "le2"), ([cM[0]], "M")],
           rt=1.6, copia=True, nota="mapa 7a (M7, B6-3: ÷ α)")
        da = TC(r"\Ge{\div\,\alpha}", pxof(C1b.get_right())[0] + 24, pxof(C1b.get_center())[1], 30, "l")       # C7: encostado em C1b
        self.pena(da)
        C1c = L([("m", "m"), ("le1", r"\le"), ("med", r"\text{média}"), ("le2", r"\le"), ("M", "M")], 1200, 440, 38)
        gm(self, C1b, C1c, [("m", "m"), ("le1", "le1"), ("fr", "med"), ("le2", "le2"), ("M", "M")], rt=1.3, copia=True,
           nota="mapa 7b (M7, B6-3: ∬f/α é a média)")
        self.gat("agora escolhe um caminho")
        gx = lambda t: 700 + 340 * t
        gy = lambda val: 860 - val * 42
        ax = VGroup(lin_px([(680, 860), (1060, 860)], GEO, 2, z=3), lin_px([(690, 870), (690, 500)], GEO, 2, z=3))
        tk = VGroup(*[lin_px([(682, gy(vv)), (698, gy(vv))], GEO, 2, z=3) for vv in (0, 8)])
        tl = VGroup(leg("0", 670, gy(0) + 9, GEO, "right", 26), leg("8", 670, gy(8) + 9, GEO, "right", 26))     # R7: 0 e 8 no eixo
        nv = lin_px([(690, gy(8 / 3)), (1060, gy(8 / 3))], CI, 2, dash=(8, 6), z=3)
        l83 = TC(r"\Ci{\dfrac{8}{3}}", 650, gy(8 / 3), 30, "r")
        lfc = leg("f AO LONGO DO CAMINHO", 870, 910, GEO, "center", 26)
        self.play(Create(ax), Create(tk), Create(nv), run_time=0.7)
        self.pena(tl, l83, lfc, lag=0.2)
        ts = np.linspace(0, 1, 121)
        cam = [caminho(t) for t in ts]
        path = lin_px([v.px(*c) for c in cam], POS, 5, z=7)
        curva = lin_px([(gx(t), gy(a * a + b * b)) for t, (a, b) in zip(ts, cam)], POS, 4, z=5)
        self.play(Create(path), Create(curva), run_time=2.8, rate_func=linear)
        lc = leg("CAMINHO DO MÍNIMO AO MÁXIMO", 1200, 515, POS, "left", 26)
        self.pena(lc)
        self.gat("pelo teorema do valor")
        ic = next(i for i, (a, b) in enumerate(cam) if a * a + b * b >= 8 / 3)
        dcam = ponto_px(*v.px(*cam[0]), POS, 11, z=9)          # o ponto percorre o caminho; o do gráfico anda junto
        dgr = ponto_px(gx(0), gy(0), POS, 10, z=9)
        rotac = lin_px([v.px(*c) for c in cam[:ic + 1]], POS, 1, z=1)
        rotag = lin_px([(gx(t), gy(a * a + b * b)) for t, (a, b) in zip(ts[:ic + 1], cam[:ic + 1])], POS, 1, z=1)
        self.add(dcam, dgr)
        self.play(MoveAlongPath(dcam, rotac), MoveAlongPath(dgr, rotag), run_time=2.2, rate_func=smooth)
        lvi = leg("VALOR INTERMEDIÁRIO: PASSA POR 8/3", 1200, 555, BR, "left", 26)
        self.pena(lvi)
        self.gat("em algum lugar desse")
        lrs = TP(r"\Lr{(r,s)}", *v.px(cam[ic][0] - .62, cam[ic][1] + .2), 30, "l")
        self.pena(lrs)
        # M8 (v2): f(r, s) = média = ∬f/α → ∬_B f = α f(r, s): o α atravessa a igualdade
        D1 = L([("f", r"\f(\Lr{r,s})"), ("e1", "="), ("med", r"\text{média}"), ("e2", "="), ("fr", r"\dfrac{\iint_B\f}{\al}")], 1200, 650, 36)
        fi = D1._ix["f"]
        self.escreve(D1, voos=[(VGroup(lrs.f[0][1], lrs.f[0][3]), [fi[2], fi[4]]), (gl(C1c, "med"), D1._ix["med"]), (gl(C1b, "fr"), D1._ix["fr"])],
                     atraso_caneta=0.3)
        D2 = L([("ii", r"\iint_B\f"), ("eq", "="), ("al", r"\al"), ("f", r"\,\f(\Lr{r,s})")], 1200, 750, 40)
        dfr = D1._ix["fr"]
        gm(self, D1, D2, [(dfr[0:4], "ii"), ("e2", "eq"), ([dfr[5]], "al"), ("f", "f")], rt=1.6, copia=True, nota="mapa 8 (M8, B6-3: o teorema)")
        self.gat("e se a região")
        l0 = leg("ÁREA 0: QUALQUER PONTO SERVE", 1200, 830, GEO, "left", 26)
        self.pena(l0)
        self.marca("20")

        # ── B6-4 · quando a média não aparece (alvo 21), cartões ──
        self.an("B6-4")
        self.limpa(rt=0.5)
        self.grade_off(rt=0)
        self.gat("volta à chapa de")
        p1, t1, s1 = cartao(80, 200, 540, 560, "SALTO", "MÉDIA 1,76 PULADA")
        gy = lambda val: 560 - val * 80
        deg = VGroup(ret_px(180, gy(1), 350, 560, fill=LEVE, z=3), ret_px(350, gy(3), 520, 560, fill=PESADO, z=3))
        degrade(deg[0], LEVE_A, LEVE_B)
        degrade(deg[1], PES_A, PES_B)
        self.play(Create(p1), LaggedStart(*[GrowFromEdge(d, DOWN) for d in deg], lag_ratio=0.4), run_time=1.0)
        self.gat("só assume dois valores")
        self.pena(TC("1", 265, 520, 30, "c"), TC("3", 435, 440, 30, "c"), lag=0.5)
        self.gat("nenhum ponto tem densidade")
        md = lin_px([(160, gy(1.76)), (540, gy(1.76))], CI, 3, dash=(8, 6), z=5)
        l176 = TC(r"\Ci{1{,}76}", 548, gy(1.76), 26, "l")
        self.play(Create(md), run_time=0.6)
        self.pena(l176)
        self.gat("a função salta de")
        self.play(Create(cruz_px(330, 250, AL, .8)), run_time=0.3)
        self.pena(t1, s1, lag=0.3)
        mc1 = TC(r"\dfrac{\Ci{7{,}06}}{4}\approx\Ci{1{,}76}", 350, 622, 30, "c")             # C8 (final): a média com conta
        self.pena(mc1)
        self.gat("passando por cima da")
        perfil = lin_px([(190, gy(1) - 8), (348, gy(1) - 8), (352, gy(3) - 8), (510, gy(3) - 8)], POS, 1, z=1)
        dp_ = ponto_px(190, gy(1) - 8, POS, 9, z=9)        # o valor anda no degrau de baixo e salta por cima da média, sem passar por ela
        self.add(dp_)
        self.play(MoveAlongPath(dp_, perfil), run_time=1.6, rate_func=linear)
        self.play(FadeOut(dp_), run_time=0.2)              # C8 (final): o ponto sai depois do salto
        self.remove(dp_)
        self.gat("outro exemplo dois quadrados")
        p2, t2, s2 = cartao(690, 200, 540, 560, "SEM CAMINHO", "MÉDIA 2 NUNCA")
        q = VGroup(ret_px(760, 380, 910, 530, fill=LEVE, z=3), ret_px(1000, 380, 1150, 530, fill=PESADO, z=3))
        degrade(q[0], LEVE_A, LEVE_B)
        degrade(q[1], PES_A, PES_B)
        self.play(Create(p2), FadeIn(q[0], shift=RIGHT * 0.2), FadeIn(q[1], shift=LEFT * 0.2), run_time=0.8)
        self.pena(TC("1", 835, 455, 32, "c"), TC("3", 1075, 455, 32, "c"))
        self.gat("a função é contínua na")
        ct = VGroup(ret_px(760, 380, 910, 530, stroke=MEN, wpx=2, z=4), ret_px(1000, 380, 1150, 530, stroke=MEN, wpx=2, z=4))
        self.play(Create(ct), run_time=1.0)
        self.gat("mas não existe caminho")
        cm = lin_px([(910, 455), (1000, 455)], POS, 3, dash=(7, 6), z=5)
        self.play(Create(cm), run_time=1.6, rate_func=linear)
        self.play(Create(cruz_px(955, 455, AL, .6)), run_time=0.4)
        self.gat("a média é dois")
        self.play(Create(cruz_px(955, 250, AL, .8)), run_time=0.3)
        self.pena(t2, s2, lag=0.3)
        mc2 = TC(r"\dfrac{1+3}{2}=2", 900, 615, 30, "c")                                      # C8 (final)
        lai = leg("ÁREAS IGUAIS", 1010, 625, GEO, "left", 26)
        self.pena(mc2, lai, lag=0.3)
        self.gat("dá para colocar um")
        p3, t3, s3 = cartao(1300, 200, 540, 560, "1,76 NA SOLDA", "MÉDIA ATINGIDA", MEN)
        v3 = Vw(1400, 620, 100)
        a3, b3 = metais_liso(v3)
        c3 = cordao_ch(v3, 4)
        self.play(Create(p3), FadeIn(a3), FadeIn(b3), FadeIn(c3), run_time=0.8)
        self.gat("exatamente sobre a solda")
        self.play(Transform(c3, Cordao(curva_g(v3, 0, 160), 5, z=7, corpo=MEN, borda=mixh(MEN, BG_, .5), escama=mixh(MEN, "#FFFFFF", .5))), run_time=0.6)
        dp = ponto_px(*v3.px(1, float(g_solda(1))), POS, 10, z=9)
        self.play(GrowFromCenter(dp), run_time=0.5)          # o ponto laranja nasce NA solda
        self.gat("aí a média aparece")
        self.play(Create(check_px(1560, 250, MEN, .9)), run_time=0.3)
        self.pena(t3, s3, lag=0.3)
        self.gat("então continuidade e caminho")
        su = T("SUFICIENTE, NÃO NECESSÁRIA", 960, 850, 40, "center")
        self.pena(su)
        self.gat("sem essas hipóteses a")
        sh = leg("SEM AS HIPÓTESES, O TEOREMA NÃO GARANTE", 960, 905, GEO, "center", 26)
        self.pena(sh)
        self.marca("21")

        # ── B6-5 · onde encontramos essa média? (alvo 22 v2): cada cartão diz QUAL média ──
        self.an("B6-5")
        self.limpa(rt=0.5)
        gats = ["a temperatura média de", "a altura média de", "a altura de uma", "o brilho médio de"]
        nomes = [("PLACA AQUECIDA", "TEMPERATURA MÉDIA"), ("CHUVA NUMA REGIÃO", "ALTURA MÉDIA DA CHUVA"), ("TERRAPLANAGEM", "NÍVEL MÉDIO"),
                 ("IMAGEM", "BRILHO MÉDIO")]
        for i, (X, gg, (nm, sb)) in enumerate(zip((80, 530, 980, 1430), gats, nomes)):
            self.gat(gg)
            p, t, s = cartao(X, 230, 410, 430, nm, sb)
            if i == 0:
                yy, xx = np.mgrid[0:200, 0:270]
                d = np.clip(np.hypot(xx - 135, yy - 100) / 150, 0, 1)[..., None]
                arr = hx("#FFC24D") * (1 - d) + hx(mixh(BG_, "#FF7A8A", .4)) * d
                des = img_px(arr, 150, 300, 270, 200, z=3)
                ent = FadeIn(des)
            elif i == 1:                                   # R8: região de contorno irregular, mais funda no meio, com pingos
                cb = [CubicBezier(PX(600, 470), PX(590, 330), PX(760, 290), PX(860, 350)), CubicBezier(PX(860, 350), PX(920, 400), PX(880, 500), PX(760, 505)),
                      CubicBezier(PX(760, 505), PX(680, 510), PX(610, 500), PX(600, 470))]
                reg = VMobject()
                reg.set_points(np.concatenate([c.points for c in cb]))
                reg.set_fill(mixh(BG_, CI, .25), 1).set_stroke(GEO, W(2))
                manchas = VGroup(*[sem_ctn(Circle(radius=r / 120).move_to(PX(cx, cy)).set_fill(mixh(BG_, CI, a), 1).set_stroke(width=0)).set_z_index(4)
                                   for cx, cy, r, a in ((700, 410, 62, .42), (812, 392, 42, .38), (676, 466, 30, .34), (710, 412, 30, .6))])
                pingos = VGroup(*[lin_px([(xp, yp), (xp - 4, yp + 14)], CI, 2, z=5) for xp, yp in
                                  ((640, 300), (700, 285), (760, 300), (820, 290), (680, 330), (790, 320))])
                des = VGroup(sem_ctn(reg).set_z_index(3), manchas, pingos)
                ent = AnimationGroup(FadeIn(des[0]), FadeIn(manchas), LaggedStart(*[p_.animate.shift(DOWN * 0.15) for p_ in pingos], lag_ratio=0.1),
                                     lag_ratio=0.3)
                self.add(pingos)
            elif i == 2:
                mt = poly_px([(1010, 520), (1080, 380), (1150, 470), (1220, 340), (1360, 520)], mixh(BG_, "#C8A070", .6), z=3)
                nvl = lin_px([(1000, 450), (1370, 450)], CI, 3, dash=(8, 6), z=4)
                des = VGroup(mt, nvl)
                ent = AnimationGroup(GrowFromEdge(mt, DOWN), Create(nvl), lag_ratio=0.6)
            else:
                des = VGroup(*[ret_px(1500 + a * 22, 300 + c * 24, 1521 + a * 22, 323 + c * 24, fill=mixh("#10101A", "#F5F7FF", ((a * 7 + c * 5) % 11) / 11), z=3)
                               for a in range(12) for c in range(8)])
                ent = LaggedStart(*[FadeIn(r) for r in des], lag_ratio=0.01)
            self.play(Create(p), ent, run_time=0.9)
            self.pena(t, s, lag=0.3)
        self.gat("a integral dupla dá")
        Mf = TC(r"\text{média}=\dfrac{\iint_B\f}{\al}", 960, 820, 48, "c")
        self.pena(Mf)
        self.gat("e o teorema acrescenta")
        self.sublinha(Mf[0], 2.4)
        self.gat("algum lugar assume exatamente")
        al_ = leg("ALGUM PONTO ATINGE A MÉDIA", 960, 905, POS, "center", 26)
        self.pena(al_)
        self.marca("22")
        self.sai_fim()
