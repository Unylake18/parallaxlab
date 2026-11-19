"""yt_0031 · B7 · o teorema (alvos 22 a 25)."""
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


def clip_ret(x0, y0, x1, y1, J=(1121, 201, 1459, 539)):
    return max(x0, J[0]), max(y0, J[1]), min(x1, J[2]), min(y1, J[3])


class PB7(B31):
    ANTES = "CONTINUIDADE UNIFORME"

    def corpo(self):
        # ── B7-1 · separando os pontos problemáticos (alvo 22) ────────────────────────────────────────
        self.an("B7-1")
        self.secao("O TEOREMA")
        self.grade_on(rt=0.4)
        mapa = img_chapa(arr_generica())
        bd = borda_ch(CH, GEO, 3)
        self.play(FadeIn(mapa), Create(bd), run_time=1.0)
        self.gat("existe um número eme")
        m1 = TC(r"|\f|\le M", 1120, 680, 40)
        m2 = leg("f LIMITADA", 1124, 740, GEO, "left", 24)
        self.pena(m1)
        self.gat("que limita o módulo")
        self.pena(m2)
        self.gat("e chama de d")
        sold = solda_px(CH, BR, 3)
        self.play(Create(sold), run_time=0.8)
        lD = TP("D", *CH.px(.1, 1.3), 30)
        self.pena(lD)
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
        solz = lin_px([Z(u_, float(g_solda(u_))) for u_ in np.linspace(.6, 1.15, 41)], BR, 3, z=6)
        lupa = VGroup(fundo, lg, verm_z, boxz, engz, celzz, solz)
        self.play(Create(pl), FadeIn(lupa), run_time=0.9)
        mg = leg("MARGEM: A CÉLULA CABE", 1290, 580, GEO, "center", 22)
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
        al_ = leg("α: ÁREA DO RETÂNGULO", 1124, 880, GEO, "left", 22)
        self.pena(al_)
        self.gat("o segundo grupo")
        lv = leg("VERMELHAS", *CH.px(1.15, 1.66), AL, "center", 26)
        cv = leg("VERMELHAS", 1124, 410, AL, "left", 28)
        self.pena(lv, cv, lag=0.3)
        self.gat("então a tampa nunca")
        lb = TC(r"\text{tampa}\le 2M,\ \ \text{área}<2\varepsilon_1\ \Rightarrow\ <4M\varepsilon_1", 1120, 470, 36)
        nb1 = nglifos(r"\text{tampa}\le 2M,")
        nb2 = nglifos(r"\text{tampa}\le 2M,\ \ \text{área}<2\varepsilon_1")
        self.pena_partes(lb, [nb1, nb2, len(lb.family_members_with_points())], [None, "e essas células cabem", "contribuição menos que quatro"])
        self.gat("somando os dois grupos")
        sm = TC(r"\SP-\sP<\alpha\,\varepsilon_2+4M\varepsilon_1", 1120, 600, 44)
        na, nb = len(la[0]), len(lb[0])
        assert len(sm[0]) == 18, len(sm[0])
        ca, cb = la.copy(), lb.copy()
        mapa_glifos(self, [ca, cb], sm, [((ca, list(range(na - 3, na))), [10, 11, 12]), ((cb, list(range(nb - 4, nb))), [14, 15, 16, 17])], rt=1.4)
        self.add(la, lb)
        self.gat("agora escolhe os dois")
        mt = TC(r"\alpha\,\varepsilon_2<\tfrac{\eps}{2}\quad\text{e}\quad 4M\varepsilon_1<\tfrac{\eps}{2}", 1120, 700, 40)
        self.pena(mt)
        self.gat("as tampas somem")
        ts_ = T("AS TAMPAS SOMEM", 1120, 820, 40, cor=CI)
        self.pena(ts_)
        self.marca("23")

        # ── B7-3 · o teorema (alvo 24) ──────────────────────────────────────────────────────────────
        self.an("B7-3")
        sai = [calm, verm, g24, sold, bd, lc, cc, la, al_, lv, cv, lb, sm, mt, ts_]
        self.grade_off(rt=0.5, junto=[FadeOut(m) for m in sai])
        self.remove(*sai)
        cx = [(140, 170, 190, "TEOREMA 1", CI, r"\f\ \text{limitada em } R\ \ \text{e}\ \ D=\{\text{descontinuidades}\}\ \text{com conteúdo nulo}\ \Rightarrow\ \f\ \text{integrável em } R", 290, 38),
              (140, 390, 150, "CASO D = ∅", MEN, r"\text{toda}\ \f\ \text{contínua num retângulo é integrável}", 490, 40),
              (140, 570, 190, "TEOREMA 2", CI, r"B\ \text{limitado},\ \f\ \text{contínua e limitada em } B,\ \text{fronteira de } B\ \text{com conteúdo nulo}\ \Rightarrow\ \f\ \text{integrável em } B", 690, 34),
              (140, 790, 150, "OBSERVAÇÃO", GEO, r"\text{``contínua'' pode virar ``contínua fora de um conjunto de conteúdo nulo''}", 890, 36)]
        objs = []
        caixas = []
        for (X, Y, hh, tit, cor, tex, yf, sz) in cx:
            caixas.append((caixa_px(X, Y, 1640, hh, cor, 2, 1.0, 12), leg(tit, X + 24, Y + 40, cor, "left", 24), TC(tex, 170, yf, sz)))
            objs += list(caixas[-1])

        def abre(k, fr):
            self.gat(fr)
            self.play(Create(caixas[k][0]), run_time=0.5)
            self.pena(caixas[k][1])
        # teorema 1: inteiro; depois as duas hipóteses sublinhadas na leitura
        abre(0, "e esse é o teorema")
        f1 = caixas[0][2]
        a = nglifos(r"\f\ \text{limitada em } R")
        b0 = nglifos(r"\f\ \text{limitada em } R\ \ \text{e}")
        b1 = nglifos(r"\f\ \text{limitada em } R\ \ \text{e}\ \ D=\{\text{descontinuidades}\}\ \text{com conteúdo nulo}")
        self.pena_partes(f1, [a, b1, len(f1.family_members_with_points())], ["se uma função é limitada", "e o conjunto dos pontos", "então ela é integrável"], passo=0.035)
        self.gat("repara na força")
        self.pulso(caixas[0][0], 1.02, 0.8)
        self.gat("basta verificar duas")
        g1 = sorted(f1.family_members_with_points(), key=lambda g_: g_.get_left()[0])
        self.sublinha(VGroup(*g1[:a]), 1.0)
        self.sublinha(VGroup(*g1[b0:b1]), 1.2)
        # caso D = ∅
        abre(1, "e sai uma consequência")
        self.gat("o conjunto das descontinuidades é vazio")
        self.sublinha(caixas[1][1], 1.2)
        self.gat("então toda função contínua")
        self.pena(caixas[1][2], passo=0.035)
        # teorema 2, em quatro pedaços com a voz
        abre(2, "dá para ir além")
        nA = nglifos(r"B\ \text{limitado},")
        nB = nglifos(r"B\ \text{limitado},\ \f\ \text{contínua e limitada em } B,")
        nC = nglifos(r"B\ \text{limitado},\ \f\ \text{contínua e limitada em } B,\ \text{fronteira de } B\ \text{com conteúdo nulo}")
        nT = len(caixas[2][2].family_members_with_points())
        self.pena_partes(caixas[2][2], [nA, nB, nC, nT], [None, "se ela é contínua e limitada", "só pode ser descontínua", "e o teorema garante"], passo=0.035)
        abre(3, "e o livro ainda observa")
        self.pena(caixas[3][2], passo=0.035)
        self.marca("24")

        # ── B7-4 · as três respostas (alvo 25) ──────────────────────────────────────────────────────
        self.an("B7-4")
        self.play(*[FadeOut(m) for m in objs], run_time=0.5)
        self.remove(*objs)
        Ls = 200
        destinos = [560, 860, 1160]
        Gm, _ = mini_metais(140, 760, 420)
        Gd, _ = mini_disco(750, 760, 420)
        Ge, _ = mini_dens(1360, 760, 420)
        grandes = [(80, 140, Gm), (690, 750, Gd), (1300, 1360, Ge)]
        pequenos = []
        for (X0p, Xc, G), X0 in zip(grandes, destinos):
            G.scale(Ls / 420, about_point=PX(Xc, 760)).shift(PX(X0, 110 + Ls + 20) - PX(Xc, 760))
            pequenos.append(painel(X0 - 20, 110, Ls + 40, Ls + 40))
        self.play(*[FadeIn(p) for p in pequenos], *[FadeIn(G) for _, _, G in grandes], run_time=0.8)
        info = {1: ("ÁREA = π", "FRONTEIRA DE CONTEÚDO NULO", 960), 0: ("MASSA ≈ 7,06 kg", "SALTA SÓ NA SOLDA", 350), 2: ("INTEGRÁVEL", "CONTÍNUA NO RETÂNGULO", 1570)}
        ordem = [(1, "o quarto de disco a", "é pi a chapa"), (0, "a chapa de dois metais a", "mais ou menos"), (2, "e a chapa de densidade", "sem refazer a conta")]
        fixos = []
        frs = {1: ("todos com conteúdo nulo", "e a área existe"), 0: ("só é descontínua na solda", "a massa está bem"),
               2: ("a função é contínua no", "então é integrável sem")}
        for k, fr1, fr2 in ordem:
            self.gat(fr1)
            X0p, Xc, G = grandes[k]
            G.generate_target()
            G.target.scale(420 / Ls, about_point=G.get_corner(DL)).shift(PX(Xc, 760) - G.get_corner(DL))
            pg = painel(X0p, 200, 540, 740)
            self.play(MoveToTarget(G), ReplacementTransform(pequenos[k], pg), run_time=1.0)
            t1, t2, X = info[k]
            a_ = T(t1, X, 850, 34, "center")
            b_ = leg(t2, X, 905, GEO, "center", 22)
            self.gat(frs[k][0])
            self.pena(b_)
            self.gat(frs[k][1])
            self.pena(a_)
            self.gat(fr2)
            ck = check_px(X + 170, 240)
            self.play(Create(ck), run_time=0.4)
            fixos += [pg, a_, b_, ck]
        self.gat("três problemas diferentes")
        tp = T("TRÊS PROBLEMAS, UM TEOREMA", 960, 1010, 32, "center", CI)
        self.pena(tp)
        self.marca("25")
        self.sai_fim()
