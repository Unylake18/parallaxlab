"""yt_0031 · B7 · o teorema (alvos 22 a 25). v2: lupa recortada na janela (G5); mapas 2–4 do MF-Tools no B7-2 (cancelamento em coral);
teoremas com miniaturas e \\emptyset (alvo 24 v2); os três painéis do B7-4 voltam já no lugar e acendem um por vez."""
from v31 import *
from sec_b3 import cobertura


def arr_generica(L=480):
    def c(i, j):
        a, b = (i + .5) / 32, (j + .5) / 32
        v = (5 if b > g_solda(a) else 2) + 1.2 * math.sin(1.3 * a + .7 * b)
        return cor_dens_arr(np.array(v))
    return arr_celulas(64, c, L)


def toca_cob(n=24):
    h = 2 / n
    out = []
    for i in range(n):
        for j in range(n):
            a, b, c, d = i * h, i * h + h, j * h, j * h + h
            for k in range(8):
                a0, b0 = k * .25, k * .25 + .25
                mn, mx = faixa(a0, b0)
                if a < b0 and b > a0 and c < mx and d > mn:
                    out.append((i, j))
                    break
    return out


def ic_moldura(X0, Y0, h):
    r = RoundedRectangle(width=h / 120, height=h / 120, corner_radius=8 / 120).move_to(PX(X0 + h / 2, Y0 + h / 2))
    r.set_fill(opacity=0).set_stroke(GEO, W(1.5), .35)
    r._sem_contorno = True
    return r.set_z_index(-4)


def mini_obs(X, Y, L):
    """Observação: o quarto de disco com uma curva de descontinuidade dentro."""
    v = Vw(X, Y, L / 2)
    pts = [v.px(0, 0)] + [v.px(2 * math.cos(PI / 2 * k / 60), 2 * math.sin(PI / 2 * k / 60)) for k in range(61)]
    return Group(poly_px(pts, mixh(BG_, CI, .55), z=1), arco_px(v, BR, 2), lin_px([v.px(*p) for p in ((.25, 1.4), (.7, 1.0), (1.2, .75), (1.6, .35))], BR, 3, z=6))


class PB7(B31):
    ANTES = "O TEOREMA"          # v2 (G2): a linha 2 do canto já está na tela no 1º quadro do bloco

    def corpo(self):
        # ── B7-1 · separando os pontos problemáticos (alvo 22) ────────────────────────────────────────
        self.an("B7-1")
        self.grade_on(rt=0)               # v2 (G2): a grade entra junto da figura, sem quadro vazio
        mapa = img_chapa(arr_generica())
        bd = borda_ch(CH, GEO, 3)
        sold = solda_px(CH, BR, 3, n=240)                 # v2: solda lisa (paramétrica, 240 amostras)
        self.play(FadeIn(mapa), Create(bd), Create(sold), run_time=0.5)
        self.gat("existe um número eme")
        m1 = TC(r"|\f|\le M", 1120, 680, 40)
        m2 = leg("f LIMITADA", 1124, 740, GEO, "left", 24)
        self.pena(m1, m2, lag=0.5)
        self.gat("e chama de d")
        lD = TP("D", *CH.px(.1, 1.3), 30)
        self.pena(lD)
        self.acende([sold], cor=POS, rt=1.0)
        self.gat("primeiro cobre d")
        cob = cobertura(8, fill=0, wpx=3, z=6)
        self.play(LaggedStart(*[Create(r) for r in cob], lag_ratio=0.15), run_time=1.2)
        s1 = leg("1 · COBRE D: ÁREA < ε₁", 1500, 260, MEN, "left", 26)
        self.pena(s1)
        self.gat("depois engorda um")
        eng = cobertura(8, fill=0, wpx=2, eng=.06, dash=(8, 6), z=6)
        self.play(*[TransformFromCopy(a, b) for a, b in zip(cob, eng)], run_time=1.0)
        s2 = leg("2 · ENGORDA: ÁREA < 2ε₁", 1500, 320, MEN, "left", 26)
        self.pena(s2)
        self.gat("é uma margem de segurança")
        e = .06
        celz = ret_px(*CH.px(.8333, 1.4167), *CH.px(.9167, 1.3333), stroke=BR, wpx=2, z=9)
        jan = lin_px([CH.px(.6, 1.65), CH.px(1.15, 1.65), CH.px(1.15, 1.1), CH.px(.6, 1.1), CH.px(.6, 1.65)], GEO, 1.5, dash=(5, 5), z=9)
        self.play(Create(celz), Create(jan), run_time=0.6)
        # G5: tudo da lupa é calculado para caber na janela [1121, 1459] × [201, 539] (a curva tem o parâmetro restrito)
        Z = lambda u_, v_: (1290 + (u_ - .875) * 700, 370 - (v_ - 1.37) * 700)
        pl = painel(1120, 200, 340, 340)
        fundo = ret_px(1121, 201, 1459, 539, fill=BG_, z=2)
        lg = VGroup()
        for k in range(-6, 7):
            qx = Z(.8333 + k / 12, 0)[0]
            ry = Z(0, 1.3333 + k / 12)[1]
            if 1121 < qx < 1459:
                lg.add(lin_px([(qx, 201), (qx, 539)], mixh(BG_, GEO, .4), 1, z=3))
            if 201 < ry < 539:
                lg.add(lin_px([(1121, ry), (1459, ry)], mixh(BG_, GEO, .4), 1, z=3))
        c0, c1 = Z(.8333, 1.4167), Z(.9167, 1.3333)
        verm_z = ret_px(*c0, *c1, fill=mixh(BG_, AL, .6), z=4)
        mn, mx = faixa(.75, 1.0)
        b0, b1 = Z(.75, mx), Z(1.0, mn)
        boxz = ret_px(*b0, *b1, fill=MEN, fop=.15, stroke=MEN, wpx=3, z=5)
        e0, e1 = Z(.75 - e, mx + e), Z(1.0 + e, mn - e)
        engz = lin_px([e0, (e1[0], e0[1]), e1, (e0[0], e1[1]), e0], MEN, 3, dash=(8, 6), z=5)
        celzz = ret_px(*c0, *c1, stroke=BR, wpx=2, z=7)
        u0_, u1_ = .875 - 166 / 700, .875 + 166 / 700
        solz = lin_px([Z(u_, float(g_solda(u_))) for u_ in np.linspace(u0_, u1_, 60)], BR, 3, z=6)
        lupa = VGroup(fundo, lg, verm_z, boxz, engz, celzz, solz)
        self.play(Create(pl), FadeIn(lupa), run_time=0.9)
        mg = leg("MARGEM: A CÉLULA CABE", 1290, 580, GEO, "center", 24)
        self.pena(mg)
        self.gat("fora da cobertura sobra")
        fc1 = leg("FORA DA COBERTURA: f CONTÍNUA", 1124, 820, GEO, "left", 24)
        fc2 = leg("→ CONTINUIDADE UNIFORME (ε₂)", 1124, 860, GEO, "left", 24)
        self.pena(fc1)
        self.pena(fc2)
        self.gat("agora escolhe uma grade")
        n, h = 24, 2 / 24
        tc = toca_cob(n)
        verm = VGroup(*[ret_px(*CH.px(i * h, j * h + h), *CH.px(i * h + h, j * h), fill=mixh(BG_, AL, .55), z=1) for i, j in tc])
        g24 = grade_ch(n, CH, mixh(BG_, GEO, .4), 1, z=2)
        self.play(LaggedStart(*[Create(l) for l in g24], lag_ratio=0.01), run_time=1.2)
        self.play(FadeIn(verm), run_time=0.6)
        s3 = leg("3 · GRADE MENOR", 1500, 380, BR, "left", 26)
        s4 = leg("QUE OS DOIS δ", 1500, 420, BR, "left", 26)
        self.pena(s3, s4, lag=0.5)
        self.marca("22")

        # ── B7-2 · dois grupos de tampas (alvo 23) ───────────────────────────────────────────────────
        self.an("B7-2")
        sai = [pl, lupa, mg, celz, jan, s1, s2, s3, s4, fc1, fc2, m1, m2, lD, cob, eng]
        calm = VGroup(*[ret_px(*CH.px(i * h, j * h + h), *CH.px(i * h + h, j * h), fill=mixh(BG_, AZC, .22), z=1)
                        for i in range(n) for j in range(n) if (i, j) not in set(tc)])
        verm2 = VGroup(*[ret_px(*CH.px(i * h, j * h + h), *CH.px(i * h + h, j * h), fill=mixh(BG_, AL, .6), z=1) for i, j in tc])
        g24b = grade_ch(n, CH, BG_, 1.5, z=2)
        self.play(*[FadeOut(m) for m in sai], FadeOut(mapa), FadeIn(calm), Transform(verm, verm2), Transform(g24, g24b), run_time=1.0)
        self.remove(*sai, mapa)
        self.gat("o primeiro é o das células calmas")
        lc = leg("CALMAS", *CH.px(1.6, .35), AZC, "center", 26)
        cc = leg("CALMAS", 1124, 250, AZC, "left", 28)
        self.pena(lc, cc, lag=0.3)
        self.gat("nelas a continuidade")
        self.play(calm.animate(rate_func=there_and_back).set_fill(mixh(BG_, AZC, .45)), run_time=1.0)
        self.gat("cada tampa tem altura menor")
        la = TC(r"\text{tampa}<\varepsilon_2,\ \ \text{área}\le\alpha\ \Rightarrow\ <\alpha\,\varepsilon_2", 1120, 310, 36)
        na1 = nglifos(r"\text{tampa}<\varepsilon_2,")
        na2 = nglifos(r"\text{tampa}<\varepsilon_2,\ \ \text{área}\le\alpha")
        self.pena_partes(la, [na1, na2, len(la.family_members_with_points())], [None, "e a área total delas", "contribuição menos que alfa"])
        al_ = leg("α: ÁREA DO RETÂNGULO", 1124, 880, GEO, "left", 24)
        self.pena(al_)
        self.gat("o segundo grupo")
        lv = leg("VERMELHAS", *CH.px(1.15, 1.66), AL, "center", 26)
        cv = leg("VERMELHAS", 1124, 410, AL, "left", 28)
        self.pena(lv, cv, lag=0.3)
        self.gat("perto das descontinuidades")
        self.play(verm.animate(rate_func=there_and_back).set_fill(mixh(BG_, AL, .9)), run_time=1.0)
        self.gat("então a tampa nunca")
        lb = TC(r"\text{tampa}\le 2M,\ \ \text{área}<2\varepsilon_1\ \Rightarrow\ <4M\varepsilon_1", 1120, 470, 36)
        nb1 = nglifos(r"\text{tampa}\le 2M,")
        nb2 = nglifos(r"\text{tampa}\le 2M,\ \ \text{área}<2\varepsilon_1")
        self.pena_partes(lb, [nb1, nb2, len(lb.family_members_with_points())], [None, "e essas células cabem", "contribuição menos que quatro"])
        # mapa 2 (§4): as duas contribuições casam com a soma; S(P) − s(P) < e o + entram a caneta
        self.gat("somando os dois grupos")
        sm = TC(r"\SP-\sP<\alpha\,\varepsilon_2+4M\varepsilon_1", 1120, 600, 44)
        assert len(sm[0]) == 18 and len(la[0]) == 21 and len(lb[0]) == 24, (len(sm[0]), len(la[0]), len(lb[0]))
        LB = CombineTex(la, lb)
        LB._tex = "tampa < ε2 ... < αε2  +  tampa ≤ 2M ... < 4Mε1"
        an2 = [([17], [9]), ([18, 19, 20], [10, 11, 12]), ([41, 42, 43, 44], [14, 15, 16, 17])]
        for x in sm.get_family():
            if getattr(x, "_caneta", False):
                x._em_caneta = True
        mp = TransformByGlyphMap(LB, sm, *an2, from_copy=True, auto_fade=True, default_introducer=CanetaIntro, default_remover=FadeOut)
        print(f"[glyphmap] {self.t:8.2f} {self._aid} mapa 2 (B7-2) | {LB._tex!r} -> {sm._tex!r} | pares={an2} | caneta={list(mp.remaining_to_indices)}")
        self.play(mp, run_time=1.6)
        sm._em_caneta, sm._esc = False, True
        self.add(la, lb)
        self.origem(sm, "glyph map", "mapa 2: αε₂ e 4Mε₁ das duas linhas")
        # mapas 3 e 4: ε₂ = ε/(2α) e ε₁ = ε/(8M); os pares que cancelam ficam coral, ganham um traço fino e somem juntos
        self.gat("agora escolhe os dois")
        A3a = TC(r"\alpha\cdot\frac{\eps}{2\alpha}", 1120, 708, 40)
        A3b = TC(r"\frac{\eps}{2}", 1120, 708, 40)
        A3b.shift(A3a[0][2].get_center() - A3b[0][0].get_center())
        T3 = VGroup(VGroup(*sm[0][10:13]))
        T3._tex = "αε₂"
        self.tbgm_copia(T3, A3a, [([0], [0])], rt=0.6, rotulo="mapa 3a (B7-2)")
        tr3 = self.risca([A3a[0][0], A3a[0][5]], rt=0.4)
        self.tbgm(A3a, A3b, [([2], [0]), ([3], [1]), ([4], [2])], rt=0.5, rotulo="mapa 3b (B7-2)", extra=[FadeOut(tr3)])
        self.remove(tr3)
        self.gat("para que cada parcela")
        B4a = TC(r"4M\cdot\frac{\eps}{8M}", 1480, 708, 40)
        B4b = TC(r"\frac{\eps}{2}", 1480, 708, 40)
        B4b.shift(B4a[0][3].get_center() - B4b[0][0].get_center())
        T4 = VGroup(VGroup(*sm[0][14:18]))
        T4._tex = "4Mε₁"
        self.tbgm_copia(T4, B4a, [([0], [0]), ([1], [1])], rt=0.6, rotulo="mapa 4a (B7-2)")
        tr4 = self.risca([B4a[0][1], B4a[0][6], B4a[0][0]], rt=0.4)
        self.tbgm(B4a, B4b, [([3], [0]), ([4], [1]), ([5], [2])], rt=0.5, rotulo="mapa 4b (B7-2): o 8 vira 2", extra=[FadeOut(tr4)])
        self.remove(tr4)
        self.gat("metade da tolerância")
        sm2 = TC(r"\SP-\sP<\frac{\eps}{2}+\frac{\eps}{2}=\eps", 1120, 708, 40)
        assert len(sm2[0]) == 19, len(sm2[0])
        AB2 = CombineTex(A3b, B4b)
        AB2._tex = "ε/2  ε/2"
        self.tbgm(AB2, sm2, [([0, 1, 2], [10, 11, 12]), ([3, 4, 5], [14, 15, 16])], rt=0.9, rotulo="ε/2 + ε/2 = ε")
        self.remove(A3b, B4b)
        self.add(sm2)
        self.gat("as tampas somem")
        ts_ = T("AS TAMPAS SOMEM", 1120, 820, 40, cor=CI)
        self.pena(ts_)
        self.gat("pelo critério do começo")
        sm3 = TC(r"\SP-\sP<\eps", 1120, 708, 40)
        self.tbgm(sm2, sm3, [(list(range(10)), list(range(10))), ([18], [10])], rt=0.9, rotulo="S(P) − s(P) < ε")
        self.marca("23")
        # a saída do B7-2 cabe no fim da fala do B7-2 (a caixa do Teorema 1 não nasce por cima das fórmulas que saem)
        self._fecha(antes=0.5)
        sai = [calm, verm, g24, sold, bd, lc, cc, la, al_, lv, cv, lb, sm, sm3, ts_]
        self.grade_off(rt=0.45, junto=[FadeOut(m) for m in sai])
        self.remove(*sai)

        # ── B7-3 · o teorema (alvo 24, v2): quatro caixas a 38 px, cada uma com a sua miniatura ───────────
        self.an("B7-3")
        cx1 = caixa_px(140, 160, 1640, 170, CI, 2, 1.0, 12)
        cx2 = caixa_px(140, 350, 1640, 130, MEN, 2, 1.0, 12)
        cx3 = caixa_px(140, 500, 1640, 220, CI, 2, 1.0, 12)
        cx4 = caixa_px(140, 740, 1640, 150, GEO, 2, 1.0, 12)
        t1 = leg("TEOREMA 1", 164, 200, CI, "left", 24)
        t2a, t2b = leg("CASO", 164, 390, MEN, "left", 24), TC(r"\Me{D=\emptyset}", 236, 383, 26, "l")
        t3 = leg("TEOREMA 2", 164, 540, CI, "left", 24)
        t4 = leg("OBSERVAÇÃO", 164, 780, GEO, "left", 24)
        f1a = TC(r"\f\ \text{limitada em } R\ \ \text{e}\ \ D=\{\text{descontinuidades}\}\ \text{com conteúdo nulo}", 170, 240, 38)
        f1b = TC(r"\Rightarrow\ \f\ \text{integrável em } R", 170, 295, 38)
        f2 = TC(r"\text{toda}\ \f\ \text{contínua num retângulo é integrável}", 170, 445, 38)
        f3a = TC(r"B\ \text{limitado},\ \ \f\ \text{contínua e limitada em } B,", 170, 590, 38)
        f3b = TC(r"\text{fronteira de } B\ \text{com conteúdo nulo}\ \Rightarrow\ \f\ \text{integrável em } B", 170, 660, 38)
        f4 = TC(r"\text{``contínua'' pode virar ``contínua fora de um conjunto de conteúdo nulo''}", 170, 840, 38)
        Gm, _ = mini_metais(1625, 300, 110, 16)
        Gd, _ = mini_dens(1673, 460, 90)
        Gq, _ = mini_disco(1605, 685, 150, 16)
        Go = mini_obs(1653, 865, 100)
        ics = [Group(ic_moldura(1610, 175, 140), Gm), Group(ic_moldura(1660, 357, 116), Gd), Group(ic_moldura(1590, 520, 180), Gq),
               Group(ic_moldura(1640, 752, 126), Go)]
        self.gat("e esse é o teorema")
        self.play(Create(cx1), FadeIn(ics[0]), run_time=0.5)
        self.pena(t1)
        a = nglifos(r"\f\ \text{limitada em } R")
        b0 = nglifos(r"\f\ \text{limitada em } R\ \ \text{e}")
        self.pena_partes(f1a, [a, len(f1a.family_members_with_points())], [None, "e o conjunto dos pontos"], passo=0.035)
        self.gat("então ela é integrável")
        self.pena(f1b, passo=0.035)
        self.gat("basta verificar duas")
        g1 = sorted(f1a.family_members_with_points(), key=lambda g_: g_.get_left()[0])
        self.sublinha(VGroup(*g1[:a]), 1.0)
        self.sublinha(VGroup(*g1[b0:]), 1.2)
        self.gat("o conjunto das descontinuidades é vazio")
        self.play(Create(cx2), FadeIn(ics[1]), run_time=0.6)
        self.pena(t2a, t2b, rt=0.7)
        self.gat("toda função contínua num retângulo")
        self.pena(f2, passo=0.035)
        self.gat("numa região limitada com fronteira")
        self.play(Create(cx3), FadeIn(ics[2]), run_time=0.6)
        self.pena(t3)
        self.pena(f3a, passo=0.035)
        self.gat("só pode ser descontínua")
        self.pena(f3b, passo=0.035)
        self.gat("e o livro ainda observa")
        self.play(Create(cx4), FadeIn(ics[3]), run_time=0.6)
        self.pena(t4)
        self.pena(f4, passo=0.035)
        objs = [cx1, cx2, cx3, cx4, t1, t2a, t2b, t3, t4, f1a, f1b, f2, f3a, f3b, f4, *ics]
        self.marca("24")

        # ── B7-4 · as três respostas (alvo 25): os painéis voltam já no tamanho e na posição finais e acendem um por vez ──
        self.an("B7-4")
        Gm, _ = mini_metais(140, 760, 420)
        Gd, _ = mini_disco(750, 760, 420)
        Ge, _ = mini_dens(1360, 760, 420)
        pgs = [painel(X0, 200, 540, 740) for X0 in (80, 690, 1300)]
        grandes = [Gm, Gd, Ge]
        self.gat("agora volta nas três")
        self.play(*[FadeOut(m) for m in objs], *[FadeIn(p) for p in pgs], *[FadeIn(G) for G in grandes], run_time=0.8)
        self.remove(*objs)
        info = {1: ("ÁREA = π", "FRONTEIRA DE CONTEÚDO NULO", 960), 0: ("MASSA ≈ 7,06 kg", "SALTA SÓ NA SOLDA", 350), 2: ("INTEGRÁVEL", "CONTÍNUA NO RETÂNGULO", 1570)}
        ordem = [(1, "o quarto de disco a", "todos com conteúdo nulo", "e a área existe", "é pi a chapa"),
                 (0, "a chapa de dois metais a", "só é descontínua na solda", "a massa está bem", "mais ou menos"),
                 (2, "e a chapa de densidade", "a função é contínua no", "então é integrável sem", "sem refazer a conta")]
        for k, fr0, fr1, fr2, fr3 in ordem:
            self.gat(fr0)
            self.acende([pgs[k]], cor=BR, rt=1.0)
            t1_, t2_, X = info[k]
            a_ = T(t1_, X, 850, 34, "center")
            b_ = leg(t2_, X, 905, GEO, "center", 24)
            self.gat(fr1)
            self.pena(b_)
            self.gat(fr2)
            self.pena(a_)
            self.gat(fr3)
            ck = check_px(X + 170, 240)
            self.play(Create(ck), run_time=0.4)
        self.gat("três problemas diferentes")
        tp = T("TRÊS PROBLEMAS, UM TEOREMA", 960, 1010, 32, "center", CI)
        self.pena(tp)
        self.marca("25")
        # v2 (G2): a chapa x² + y² e o seu painel ficam; o B8 nasce deles
        if self._aid is not None:
            self._fecha(antes=0.4)
        self.limpa(Ge, pgs[2], rt=0.4)
