"""yt_0031 · B7 · o teorema (alvos 22 a 25). v2: lupa recortada na janela (G5); mapas 2–4 do MF-Tools no B7-2 (cancelamento em coral);
teoremas com miniaturas e \\emptyset (alvo 24 v2); os três painéis do B7-4 voltam já no lugar e acendem um por vez."""
from v31 import *
from sec_b3 import cobertura


def via_px(A, B, *wps):
    """final F2: caminho de voo por pontos de passagem (px a 1080p) para o centro do grupo A → B; cada glifo segue o mesmo desvio, a forma
    interpola em linha reta. Devolve kwargs de entrada do TransformByGlyphMap ({"path_func": ...})."""
    ca, cb = A.get_center(), B.get_center()
    P = [ca, *[PX(x, y) for x, y in wps], cb]
    L = [float(np.linalg.norm(P[i + 1] - P[i])) for i in range(len(P) - 1)]
    tot = sum(L)

    def pf(s, e, a):
        d = a * tot
        c = P[-1]
        for i, l in enumerate(L):
            if d <= l or i == len(L) - 1:
                c = P[i] + (P[i + 1] - P[i]) * (min(d, l) / l if l > 0 else 1.0)
                break
            d -= l
        return s + (e - s) * a + (c - (ca + (cb - ca) * a))
    return {"path_func": pf}


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
        m1 = TC(r"|\f|\le M", 1120, 250, 40)
        self.pena(m1)
        self.gat("e chama de d")
        lD = TP("D", *CH.px(.1, 1.3), 30)
        self.pena(lD)
        self.gat("onde ela não é contínua")          # v3: a solda (onde f não é contínua) acende na palavra
        self.acende([sold], cor=POS, rt=1.0)
        self.gat("o objetivo é provar")            # v3: a solda e o D acendem juntos
        g_ = lD.f.copy().set_fill(POS)
        self.play(Transform(lD.f, g_, rate_func=there_and_back), Transform(sold, sold.copy().set_stroke(POS), rate_func=there_and_back), run_time=1.4)
        self.gat("primeiro cobre d")
        cob = cobertura(8, fill=0, wpx=3, z=6)
        self.play(LaggedStart(*[Create(r) for r in cob], lag_ratio=0.15), run_time=1.2)
        s1 = leg("1 · COBRE D: ÁREA < ε₁", 1124, 340, MEN, "left", 26)
        self.pena(s1)
        self.gat("depois engorda um")
        eng = cobertura(8, fill=0, wpx=2, eng=.06, dash=(8, 6), z=6)
        self.play(*[TransformFromCopy(a, b) for a, b in zip(cob, eng)], run_time=1.0)
        s2 = leg("2 · ENGORDA: ÁREA < 2ε₁", 1124, 400, MEN, "left", 26)
        self.pena(s2)
        self.gat("é uma margem de segurança")
        e = .06
        celz = ret_px(*CH.px(.8333, 1.4167), *CH.px(.9167, 1.3333), stroke=BR, wpx=2, z=9)
        jan = lin_px([CH.px(.6, 1.65), CH.px(1.15, 1.65), CH.px(1.15, 1.1), CH.px(.6, 1.1), CH.px(.6, 1.65)], GEO, 1.5, dash=(5, 5), z=9)
        self.play(Create(celz), Create(jan), run_time=0.6)
        # G5: tudo da lupa é calculado para caber na janela [1121, 1459] × [441, 779] (v3: 240 px abaixo; a coluna fica em cima)
        LY = 240
        Z = lambda u_, v_: (1290 + (u_ - .875) * 700, 370 + LY - (v_ - 1.37) * 700)
        pl = painel(1120, 200 + LY, 340, 340)
        fundo = ret_px(1121, 201 + LY, 1459, 539 + LY, fill=BG_, z=2)
        lg = VGroup()
        for k in range(-6, 7):
            qx = Z(.8333 + k / 12, 0)[0]
            ry = Z(0, 1.3333 + k / 12)[1]
            if 1121 < qx < 1459:
                lg.add(lin_px([(qx, 201 + LY), (qx, 539 + LY)], mixh(BG_, GEO, .4), 1, z=3))
            if 201 + LY < ry < 539 + LY:
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
        mg = leg("MARGEM: A CÉLULA CABE", 1290, 820, GEO, "center", 24)
        self.pena(mg)
        self.gat("fora da cobertura sobra")
        # v3: a lupa já mostrou a margem; sai, e a linha de fora da cobertura entra no lugar dela (uma linha só)
        self.play(*[FadeOut(m) for m in (pl, lupa, mg, celz, jan)], run_time=0.4)
        self.remove(pl, lupa, mg, celz, jan)
        fc1 = leg("FORA DA COBERTURA: CONTINUIDADE UNIFORME (ε₂)", 1124, 470, GEO, "left", 24)
        self.pena(fc1)
        self.gat("agora escolhe uma grade")
        n, h = 24, 2 / 24
        tc = toca_cob(n)
        verm = VGroup(*[ret_px(*CH.px(i * h, j * h + h), *CH.px(i * h + h, j * h), fill=mixh(BG_, AL, .55), z=1) for i, j in tc])
        g24 = grade_ch(n, CH, mixh(BG_, GEO, .4), 1, z=2)
        self.play(LaggedStart(*[Create(l) for l in g24], lag_ratio=0.01), run_time=1.2)
        self.play(FadeIn(verm), run_time=0.6)
        s3 = leg("3 · GRADE: MARGEM E δ", 1124, 540, BR, "left", 26)
        self.pena(s3)
        self.marca("22")

        # ── B7-2 · dois grupos de tampas (alvo 23) ───────────────────────────────────────────────────
        self.an("B7-2")
        sai = [s1, s2, s3, fc1, m1, lD, cob, eng]
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
        al_ = leg("α: ÁREA DO RETÂNGULO", 1124, 880, GEO, "left", 24)

        def _alfa():                       # v3: o contorno da chapa acende em "a área do retângulo"; a legenda de α entra em "a gente chama de alfa"
            self.gat("área do retângulo")
            self.acende([bd], cor=BR, rt=1.2, largura=4)
            self.gat("a gente chama de alfa")
            self.pena(al_)
        self.pena_partes(la, [na1, na2, len(la.family_members_with_points())], [None, "e a área total delas", "contribuição menos que alfa"],
                         antes={2: _alfa})
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
        sm = TC(r"\SP-\sP<\alpha\,\Me{\varepsilon_2}+4M\Me{\varepsilon_1}", 1120, 600, 42)
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
        self.marca("23", agora=True, dt=0.4)

        # v3 (ALTA 2, alvo 23b): a coluna vira a das escolhas de ε. CALMAS/VERMELHAS (com as cotas já dentro da soma) saem; a soma sobe a 250
        self.gat("mais quatro eme épsilon um")
        col = [cc, la, cv, lb, al_]
        self.play(*[FadeOut(m) for m in col], run_time=0.3)
        self.remove(*col)
        self.play(sm.animate.shift(UP * (600 - 250) / 120), run_time=0.5)
        self.gat("escolhe os dois épsilons")
        esc = leg("ESCOLHA DOS DOIS", 1124, 346, MEN, "left", 26)
        # final F7: o ε da legenda é um MathTex próprio a 34 px, menta, na linha de base da legenda (era ≈ 10 px dentro do texto)
        epsl = TP(r"\eps", 0, 0, 34, "l")
        epsl.shift(RIGHT * (esc.get_right()[0] + 10 / 120 - epsl[1].get_left()[0]) + UP * (esc.get_bottom()[1] - epsl[1].get_bottom()[1]))
        self.pena(esc, epsl)

        def no_igual(F, k, y):             # a linha fica com o "=" (glifo k) na altura y do alvo
            F.shift(UP * (PX(0, y)[1] - F[0][k].get_center()[1]))
            return F

        E2 = no_igual(TC(r"\Me{\varepsilon_2}=\dfrac{\eps}{2\alpha}", 1120, 420, 38), 2, 418)
        E1 = no_igual(TC(r"\Me{\varepsilon_1}=\dfrac{\eps}{8M}", 1335, 420, 38), 2, 418)
        M3a = no_igual(TC(r"\alpha\,\Me{\varepsilon_2}=\alpha\cdot\dfrac{\eps}{2\,\alpha}", 1120, 550, 38), 3, 548)
        M3b = no_igual(TC(r"\alpha\,\Me{\varepsilon_2}=\Co{\cancel{\alpha}}\cdot\dfrac{\eps}{2\,\Co{\cancel{\alpha}}}", 1120, 550, 38), 3, 548)
        R3 = no_igual(TC(r"=\dfrac{\eps}{2}", 1120, 550, 38), 0, 548)
        R3.shift(RIGHT * (M3b.get_right()[0] + 20 / 120 - R3.get_left()[0]))
        M4a = no_igual(TC(r"4M\Me{\varepsilon_1}=4\,M\cdot\dfrac{\eps}{8\,M}", 1120, 690, 38), 4, 676)
        M4b = no_igual(TC(r"4M\Me{\varepsilon_1}=4\,\Co{\cancel{M}}\cdot\dfrac{\eps}{8\,\Co{\cancel{M}}}", 1120, 690, 38), 4, 676)
        M4c = no_igual(TC(r"4M\Me{\varepsilon_1}=\Co{\cancel{4}}\,\Co{\cancel{M}}\cdot\dfrac{\eps}{\Co{\underset{\textstyle 2}{\cancel{8}}}\,\Co{\cancel{M}}}",
                          1120, 690, 38), 4, 676)
        R4 = no_igual(TC(r"=\dfrac{\eps}{2}", 1120, 690, 38), 0, 676)
        R4.shift(RIGHT * (M4c.get_right()[0] + 20 / 120 - R4.get_left()[0]))
        S840 = no_igual(TC(r"\SP-\sP<\dfrac{\eps}{2}+\dfrac{\eps}{2}=\eps", 1120, 840, 42), 9, 838)
        for F, n in ((E2, 7), (E1, 7), (M3a, 10), (M3b, 12), (R3, 4), (M4a, 12), (M4b, 16), (M4c, 19), (R4, 4), (S840, 19)):
            assert len(F[0]) == n, (F._tex, len(F[0]), n)

        def sub(F, a, b, nome):
            g = VGroup(VGroup(*F[0][a:b]))
            g._tex = nome
            return g

        # ε₂ = ε/(2α): o ε₂ voa da soma, o resto a caneta
        self.gat("épsilon dois igual a")
        # final §7: ε₂ desce entre a soma e a legenda (y = 298), passa por fora da coluna à esquerda (x = 1060) e entra na linha 420
        se2 = VGroup(*sm[0][11:13])
        self.escreve(E2, voos=[(se2, [0, 1], [(pxof(se2.get_center())[0], 298), (1060, 298), (1060, pxof(E2[0][0].get_center())[1])])],
                     rt_voo=1.0, atraso_caneta=0.6, passo=0.03)
        # mapa 3a: αε₂ (da soma) e ε/(2α) (da escolha) montam αε₂ = α·ε/(2α); "=", "α", "·" a caneta
        A3 = CombineTex(sub(sm, 10, 13, "αε₂"), sub(E2, 3, 7, "ε/(2α)"))
        A3._tex = "αε₂ (soma)  +  ε/(2α) (escolha)"
        # final §7: αε₂ sai da soma pelo corredor y = 298, desce por fora da coluna (x = 1540), passa entre as linhas 420 e 550 (y = 485) e
        # pousa; ε/(2α) desce direto da linha 420 (nada no caminho)
        g3s, g3t = VGroup(*sm[0][10:13]), VGroup(*M3a[0][0:3])
        v3a = via_px(g3s, g3t, (pxof(g3s.get_center())[0], 298), (1540, 298), (1540, 485), (pxof(g3t.get_center())[0], 485))
        self.tbgm_copia(A3, M3a, [([0, 1, 2], [0, 1, 2], v3a), ([3], [6]), ([4], [7]), ([5], [8]), ([6], [9])], rt=1.1,
                        rotulo="mapa 3a (B7-2): αε₂ = α·ε/(2α)", cedo=True)
        # mapa 3b: o par α…α fica coral e ganha o \cancel (o traço a caneta)
        self.gat("o alfa cancela")
        self.tbgm(M3a, M3b, [([k], [j]) for k, j in ((0, 0), (1, 1), (2, 2), (3, 3), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 11))], rt=0.7,
                  rotulo="mapa 3b (B7-2): α cancela (coral + \\cancel)", cedo=True)
        # mapa 3c: ε/(2α̸) → ε/2 (a cópia do α̸ cai); "=" a caneta
        self.gat("e sobra épsilon sobre dois")
        self.tbgm_copia(M3b, R3, [([7], [1]), ([8], [2]), ([9], [3])], rt=0.7, rotulo="mapa 3c (B7-2): sobra ε/2", cedo=True)
        # ε₁ = ε/(8M)
        self.gat("épsilon um igual a")
        # final §7: ε₁ desce entre a soma e a legenda (y = 298), contorna o ε da legenda pela direita (x = 1460) e entra por cima (y = 378)
        se1 = VGroup(*sm[0][16:18])
        tx1 = pxof(VGroup(*E1[0][0:2]).get_center())[0]
        self.escreve(E1, voos=[(se1, [0, 1], [(pxof(se1.get_center())[0], 298), (1460, 298), (1460, 378), (tx1, 378)])],
                     rt_voo=1.0, atraso_caneta=0.6, passo=0.03)
        A4 = CombineTex(sub(sm, 14, 18, "4Mε₁"), sub(E1, 3, 7, "ε/(8M)"))
        A4._tex = "4Mε₁ (soma)  +  ε/(8M) (escolha)"
        # final F2: 4Mε₁ desce pela direita (centro em x = 1770, borda ≥ 1700), passa por baixo da linha 690 (y = 770, a linha 840 ainda está
        # vazia) e sobe ao lugar; ε/(8M) sai pela direita da própria linha (x = 1620, entre a coluna e o voo do 4Mε₁) e entra na 690 pela direita.
        # (Pela esquerda, x ≤ 1300, ele cruzaria o ε₂ = ε/(2α) da 420 e o αε₂ da 550: não há corredor livre entre as linhas.)
        g4s, g4t = VGroup(*sm[0][14:18]), VGroup(*M4a[0][0:4])
        e8s, e8t = VGroup(*E1[0][3:7]), VGroup(*M4a[0][8:12])
        x4t = pxof(g4t.get_center())[0]
        y8s, y8t = pxof(e8s.get_center())[1], pxof(e8t.get_center())[1]
        v4 = via_px(g4s, g4t, (1770, pxof(g4s.get_center())[1]), (1770, 770), (x4t, 770))
        v8 = via_px(e8s, e8t, (1620, y8s), (1620, y8t))
        self.tbgm_copia(A4, M4a, [([0, 1, 2, 3], [0, 1, 2, 3], v4), ([4, 5, 6, 7], [8, 9, 10, 11], v8)], rt=1.2,
                        rotulo="mapa 4a (B7-2): 4Mε₁ = 4M·ε/(8M)", cedo=True)
        # mapa 4b: o par M…M
        self.gat("o eme cancela")
        self.tbgm(M4a, M4b, [([k], [j]) for k, j in ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 8), (7, 9), (8, 10), (9, 11), (10, 12), (11, 15))],
                  rt=0.7, rotulo="mapa 4b (B7-2): M cancela (coral + \\cancel)", cedo=True)
        # mapa 4c: 4 e 8 riscados juntos, o 2 pequeno entra a caneta (o 8 não vira 2)
        self.gat("o quatro com o oito")
        self.tbgm(M4b, M4c, [([k], [j]) for k, j in ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12),
                                                     (12, 14), (13, 16), (14, 17), (15, 18))],
                  rt=0.8, rotulo="mapa 4c (B7-2): 4 com 8 (\\cancel + 2 pequeno)", cedo=True)
        self.gat("e sobra épsilon sobre dois de novo")
        self.tbgm_copia(M4c, R4, [([11], [1]), ([12], [2]), ([15], [3])], rt=0.7, rotulo="mapa 4d (B7-2): sobra ε/2 (o 2 do 8 ÷ 4)", cedo=True)
        # a soma final (final F2): S(P) − s(P) < entra a caneta (sem voo); os dois ε/2 voam em arco pela DIREITA (x ≥ 1600), descem por fora da
        # coluna, passam por baixo da linha 840 (y = 945) e sobem ao lugar; o da 690 sai 0,55 s depois (o da 550 já está no lugar).
        self.gat("meio épsilon mais meio")
        A5 = CombineTex(R3, R4)
        A5._tex = "= ε/2 (550)  +  = ε/2 (690)"
        h3s, h3t = VGroup(*R3[0][1:4]), VGroup(*S840[0][10:13])
        h4s, h4t = VGroup(*R4[0][1:4]), VGroup(*S840[0][14:17])
        v3 = via_px(h3s, h3t, (1650, pxof(h3s.get_center())[1]), (1650, 945), (pxof(h3t.get_center())[0], 945))
        v4b = via_px(h4s, h4t, (1735, pxof(h4s.get_center())[1]), (1735, 945), (pxof(h4t.get_center())[0], 945))
        v3["run_time"] = 1.0
        v4b.update(run_time=1.0, delay=0.55)
        self.tbgm_copia(A5, S840, [([1, 2, 3], [10, 11, 12], v3), ([5, 6, 7], [14, 15, 16], v4b)], rt=1.55,
                        rotulo="ε/2 + ε/2 = ε (B7-2)", cedo=True)
        self.gat("as tampas somem")
        ts_ = T("AS TAMPAS SOMEM", 1120, 960, 40, cor=CI)
        self.pena(ts_)
        self.marca("23b", agora=True, dt=0.6)
        # a saída do B7-2 cabe no fim da fala do B7-2 (a caixa do Teorema 1 não nasce por cima das fórmulas que saem)
        self._fecha(antes=0.5)
        sai = [calm, verm, g24, sold, bd, lc, lv, sm, esc, epsl, E2, E1, M3b, R3, M4c, R4, S840, ts_]
        self.grade_off(rt=0.45, junto=[FadeOut(m) for m in sai])
        self.remove(*sai)

        # ── B7-3 · o teorema (alvo 24, v2): quatro caixas a 38 px, cada uma com a sua miniatura ───────────
        self.an("B7-3")
        cx1 = caixa_px(140, 160, 1640, 170, CI, 2, 1.0, 12)
        cx2 = caixa_px(140, 350, 1640, 170, MEN, 2, 1.0, 12)
        cx3 = caixa_px(140, 540, 1640, 220, CI, 2, 1.0, 12)
        cx4 = caixa_px(140, 780, 1640, 150, GEO, 2, 1.0, 12)
        t1 = leg("TEOREMA 1", 164, 200, CI, "left", 24)
        t2a, t2b = leg("CASO", 164, 392, MEN, "left", 24), TC(r"\Me{D=\emptyset}", 238, 383, 34, "l")
        t3 = leg("TEOREMA 2", 164, 580, CI, "left", 24)
        t4 = leg("OBSERVAÇÃO", 164, 820, GEO, "left", 24)
        f1a = TC(r"\f\ \text{limitada em } R\ \ \text{e}\ \ D=\{\text{descontinuidades}\}\ \text{com conteúdo nulo}", 170, 240, 38)
        f1b = TC(r"\Rightarrow\ \f\ \text{integrável em } R", 170, 295, 38)
        f2 = TC(r"\text{toda}\ \f\ \text{contínua num retângulo é integrável}", 170, 462, 38)
        f3a = TC(r"B\ \text{limitado},\ \ \f\ \text{contínua e limitada em } B,", 170, 630, 38)
        f3b = TC(r"\text{fronteira de } B\ \text{com conteúdo nulo}\ \Rightarrow\ \f\ \text{integrável em } B", 170, 700, 38)
        f4 = TC(r"\text{``contínua'' pode virar ``contínua fora de um conjunto de conteúdo nulo''}", 170, 880, 38)
        # v3: as quatro miniaturas com 130 px (moldura de 150), centradas na altura de cada caixa, 14 px da borda direita
        Gm, _ = mini_metais(1626, 310, 130, 16)
        Gd, _ = mini_dens(1626, 500, 130)
        Gq, _ = mini_disco(1626, 715, 130, 16)
        Go = mini_obs(1626, 920, 130)
        ics = [Group(ic_moldura(1616, 170, 150), Gm), Group(ic_moldura(1616, 360, 150), Gd), Group(ic_moldura(1616, 575, 150), Gq),
               Group(ic_moldura(1616, 780, 150), Go)]
        self.gat("e esse é o teorema")
        self.play(Create(cx1), FadeIn(ics[0]), run_time=0.5)
        self.pena(t1)
        a = nglifos(r"\f\ \text{limitada em } R")
        b0 = nglifos(r"\f\ \text{limitada em } R\ \ \text{e}")
        self.pena_partes(f1a, [a, len(f1a.family_members_with_points())], [None, "e o conjunto dos pontos"], passo=0.035)
        self.gat("então ela é integrável")
        self.pena(f1b, passo=0.035)
        self.gat("repara na força disso")             # v3: a caixa do teorema acende (sem parado longo antes do sublinhado)
        self.acende([cx1], cor=BR, rt=1.2)
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
            if k == 0:
                self.pena(b_, extra=[Transform(Gm[3], Gm[3].copy().set_stroke(POS), rate_func=there_and_back, run_time=1.4)], rt=1.4)
            else:
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
