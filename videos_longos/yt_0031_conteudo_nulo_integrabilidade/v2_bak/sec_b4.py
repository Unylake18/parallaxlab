"""yt_0031 · B4 · curvas têm conteúdo nulo (alvos 15 a 17). v2: a contagem de caixas segue a voz (4 → 8 → 16) com o mapa 5 do MF-Tools;
os dois painéis do B4-2 nascem juntos e o arco refina com a voz; o B4-3 ganha a figura (alvo 17 v2)."""
from v31 import *

MEN_ = lambda a: mixh(BG_, MEN, a)


def caixa_v(v, a, b, c, d, fill, wpx=2, z=4):
    return ret_px(*v.px(a, d), *v.px(b, c), fill=MEN_(fill), stroke=MEN, wpx=wpx, z=z)


def caixas_par(v, n, fill=.25, wpx=2):
    h = 2 / n
    return VGroup(*[caixa_v(v, i * h, i * h + h, (i * h) ** 2, (i * h + h) ** 2, fill, wpx) for i in range(n)])


def coluna_par(v, n, x0, fill=.35, wpx=2):
    h, z, g = 2 / n, 0.0, VGroup()
    for i in range(n):
        d = (i * h + h) ** 2 - (i * h) ** 2
        g.add(caixa_v(v, x0, x0 + h, z, z + d, fill, wpx))
        z += d
    return g


def caixas_arco(v, n, fill=.28):
    h = 2 / n
    return VGroup(*[caixa_v(v, i * h, i * h + h, math.sqrt(max(0, 4 - (i * h + h) ** 2)), math.sqrt(4 - (i * h) ** 2), fill) for i in range(n)])


def coluna_arco(v, n, x0=2.3, fill=.35):
    h, z, g = 2 / n, 0.0, VGroup()
    for i in range(n):
        d = math.sqrt(4 - (i * h) ** 2) - math.sqrt(max(0, 4 - (i * h + h) ** 2))
        g.add(caixa_v(v, x0, x0 + h, z, z + d, fill, 2 if n <= 16 else 1))
        z += d
    return g


class PB4(B31):
    ANTES = "CURVAS TÊM CONTEÚDO NULO"          # v2 (G2): a linha 2 do canto já está na tela no 1º quadro do bloco

    def corpo(self):
        # ── B4-1 · a parábola (alvo 15) ─────────────────────────────────────────────────────────────
        self.an("B4-1")
        self.grade_on(rt=0)               # v2 (G2): a grade entra junto da figura, sem quadro vazio
        v = Vw(200, 900, 300, 300 * .4)
        sx = seta_px(v.px(-.05, 0), v.px(2.85, 0), E1, 3, 16)
        sy = seta_px(v.px(0, -.05), v.px(0, 4.6), CI, 3, 16)
        nums = [leg(str(k), v.px(0, k)[0] - 14, v.px(0, k)[1] + 8, CI, "right", 24) for k in (1, 2, 3, 4)]
        curva = lin_px([v.px(a, a * a) for a in np.linspace(0, 2, 61)], CI, 4, z=7)
        ly = TP(r"\Ci{y=\X^2}", *v.px(1.2, 3.6), 32)
        self.pena(*nums, extra=[FadeIn(sx, run_time=0.3), FadeIn(sy, run_time=0.3), Create(curva)], rt=1.0)
        self.gat("lembra da parábola")
        self.pena(ly)
        self.gat("divide o eixo em")
        cx = caixas_par(v, 4)
        self.play(LaggedStart(*[FadeIn(c) for c in cx], lag_ratio=0.3), run_time=1.0)
        l0 = leg("CAIXAS: DO PISO AO TETO", 1124, 260, MEN, "left", 28)
        self.gat("juntas as caixas cobrem")
        self.pena(l0)
        self.gat("a curva é crescente")
        seta_e = seta_px(v.px(2.12, 2), v.px(2.3, 2), GEO, 3, 12)
        self.play(FadeIn(seta_e), run_time=0.3)
        self.gat("empurrar as caixas")
        col = coluna_par(v, 4, 2.35)
        for i in range(4):
            self.play(TransformFromCopy(cx[i], col[i]), run_time=0.45)
        self.gat("todas cabem numa coluna")
        c1, c2 = v.px(2.35 + .5, 0), v.px(2.35 + .5, 4)
        cota = lin_px([(c1[0] + 16, c1[1]), (c2[0] + 16, c2[1])], BR, 2, z=8)
        l4 = T("4", c1[0] + 30, (c1[1] + c2[1]) / 2, 28)
        lD = TC(r"\Delta", *v.px(2.35 + .25, -.5), 28, "c")
        self.play(Create(cota), run_time=0.5)
        self.pena(l4, lD)
        self.gat("altura quatro a subida")
        self.acende([cota], cor=MEN, rt=1.0)
        self.gat("área total no máximo")
        fa = TC(r"\text{área das caixas}\ \le\ 4\,\Delta", 1120, 350, 40)
        nfa = len(fa[0])
        self.escreve(fa, voos=[(l4, [nfa - 2])], passo=0.045)
        # mapa 5 (§4): 4Δ com Δ = 0,5 → 0,25 → 0,125; o resultado casa por TransformByGlyphMap
        E = [TC(r"4\,\Delta=4\cdot 0{,}5=\Me{2}", 1120, 412, 34), TC(r"4\,\Delta=4\cdot 0{,}25=\Me{1}", 1120, 412, 34),
             TC(r"4\,\Delta=4\cdot 0{,}125=\Me{0{,}5}", 1120, 412, 34)]
        assert [len(e[0]) for e in E] == [10, 11, 14], [len(e[0]) for e in E]
        rows = [TC(a + r"\ \text{pedaços}\ \to\ \Me{" + b + "}", 1120, 470 + k * 66, 36) for k, (a, b) in enumerate((("4", "2"), ("8", "1"), ("16", "0{,}5")))]
        self.gat("com quatro pedaços")
        self.pena(E[0], rows[0], lag=0.4, passo=0.04)
        # com oito: cada caixa se parte em duas, a coluna se refaz; Δ e o resultado trocam por glyph map
        self.gat("com oito um")
        cx8, col8 = caixas_par(v, 8), coluna_par(v, 8, 2.35)
        lD8 = TC(r"\Delta", *v.px(2.35 + .125, -.5), 28, "c")
        lD8._origem = "troca (rótulo da largura)"
        lD8._esc = True
        rows[1]._em_caneta = True
        self.tbgm(E[0], E[1], [(list(range(7)), list(range(7))), ([7], [8]), ([8], [9])], rt=0.9, rotulo="mapa 5a (B4-1)",
                  extra=[*[ReplacementTransform(cx[i], VGroup(cx8[2 * i], cx8[2 * i + 1])) for i in range(4)], ReplacementTransform(col, col8),
                         ReplacementTransform(lD, lD8), caneta(rows[1], ritmo=0.03 / 0.30)])
        rows[1]._em_caneta, rows[1]._esc = False, True
        self.origem(rows[1], "caneta")
        self.gat("com dezesseis meio")
        cx16, col16 = caixas_par(v, 16, wpx=1.5), coluna_par(v, 16, 2.35, wpx=1.5)
        lD16 = TC(r"\Delta", *v.px(2.35 + .0625, -.5), 28, "c")
        lD16._origem = "troca (rótulo da largura)"
        lD16._esc = True
        rows[2]._em_caneta = True
        self.tbgm(E[1], E[2], [(list(range(7)), list(range(7))), ([7], [8]), ([8], [9]), ([9], [10])], rt=0.9, rotulo="mapa 5b (B4-1)",
                  extra=[*[ReplacementTransform(cx8[i], VGroup(cx16[2 * i], cx16[2 * i + 1])) for i in range(8)], ReplacementTransform(col8, col16),
                         ReplacementTransform(lD8, lD16), caneta(rows[2], ritmo=0.03 / 0.30)])
        rows[2]._em_caneta, rows[2]._esc = False, True
        self.origem(rows[2], "caneta")
        self.gat("o gráfico da parábola")
        fim = T("O GRÁFICO TEM CONTEÚDO NULO", 1120, 720, 32)
        self.pena(fim)
        self.marca("15")

        # ── B4-2 · a solda e o arco (alvo 16): os dois painéis nascem juntos ────────────────────────
        self.an("B4-2")
        tudo = [sx, sy, *nums, curva, ly, *cx16, l0, seta_e, *col16, cota, l4, lD16, fa, E[2], *rows, fim]
        pE, pD = painel(80, 190, 860, 760), painel(990, 190, 860, 760)
        vE, vD = Vw(150, 800, 250), Vw(1050, 800, 250)
        bE, bD = borda_ch(vE, mixh(BG_, GEO, .5), 2), borda_ch(vD, mixh(BG_, GEO, .5), 2)
        sE = solda_px(vE, BR, 4)
        aD = arco_px(vD, CI, 4)
        tE, tD = T("A SOLDA", 510, 260, 30, "center"), T("O ARCO", 1420, 260, 30, "center")
        self.grade_off(rt=0.5, junto=[FadeOut(m) for m in tudo] + [FadeIn(pE), FadeIn(pD)])
        self.remove(*tudo)
        n, h = 8, .25
        cxE, sobe = [], []
        for i in range(n):
            a, b = i * h, i * h + h
            mn, mx = faixa(a, b)
            s_ = g_solda(b) > g_solda(a)
            sobe.append(s_)
            cxE.append(caixa_v(vE, a, b, mn, mx, .30 if s_ else .12))
        self.play(Create(bE), Create(bD), Create(sE), Create(aD), run_time=0.9)
        self.pena(tE, tD, extra=[LaggedStart(*[FadeIn(c) for c in cxE], lag_ratio=0.1)], rt=1.0)
        self.gat("separa os dois movimentos")
        self.acende([c for c, s_ in zip(cxE, sobe) if s_], cor=BR, rt=0.7)
        self.acende([c for c, s_ in zip(cxE, sobe) if not s_], cor=BR, rt=0.7)
        self.gat("as caixas da subida")
        zu = zd = 0
        X1, X2 = 2.25, 2.25 + h + .12
        pilE = []
        for i in range(n):
            if not sobe[i]:
                continue
            a, b = i * h, i * h + h
            mn, mx = faixa(a, b)
            nv = caixa_v(vE, X1, X1 + h, .5 + zu, .5 + zu + mx - mn, .35)
            zu += mx - mn
            self.play(TransformFromCopy(cxE[i], nv), run_time=0.35)
            pilE.append(nv)
        lsu = [TC(r"0{,}58", *vE.px(X1 + h / 2, .5 + zu + .12), 26, "c"), leg("SOBE", *vE.px(X1 + h / 2, .3), GEO, "center", 24)]
        self.pena(*lsu, rt=0.7)
        self.gat("e as da descida")
        for i in range(n):
            if sobe[i]:
                continue
            a, b = i * h, i * h + h
            mn, mx = faixa(a, b)
            nv = caixa_v(vE, X2, X2 + h, .5 + zd, .5 + zd + mx - mn, .15)
            zd += mx - mn
            self.play(TransformFromCopy(cxE[i], nv), run_time=0.35)
            pilE.append(nv)
        lde = [TC(r"0{,}36", *vE.px(X2 + h / 2, .5 + zd + .12), 26, "c"), leg("DESCE", *vE.px(X2 + h / 2, .3), GEO, "center", 24)]
        self.pena(*lde, rt=0.7)
        self.gat("área total no máximo")
        aE = TC(r"\text{área}\le 0{,}94\,\Delta", 510, 880, 36, "c")
        self.pena(aE)
        # o arco: caixas na fala e refino 4 → 8 → 16 → 32 com a voz; a coluna fica com altura 2 e afina
        self.gat("o arco do quarto")
        ca = caixas_arco(vD, 4)
        self.play(LaggedStart(*[FadeIn(c) for c in ca], lag_ratio=0.2), run_time=0.8)
        self.gat("então as caixas dele")
        coa = coluna_arco(vD, 4)
        self.play(*[TransformFromCopy(ca[i], coa[i]) for i in range(4)], run_time=0.9)
        l2 = TC("2", *vD.px(2.3 + .5 + .14, 1), 28, "c")
        aDt = TC(r"\text{área}=2\,\Delta", 1420, 880, 36, "c")
        self.pena(l2, aDt, rt=1.0)
        seq = leg("4 → 1 · 8 → 0,5 · 16 → 0,25 · 32 → 0,125", 1420, 928, MEN, "center", 24)
        gls = sorted(seq.family_members_with_points(), key=lambda g_: g_.get_left()[0])
        seq._em_caneta = True
        cortes, ini, grupos = [4, 10, 18, 26], 0, []
        for k, (nn, fr) in enumerate(zip((4, 8, 16, 32), ["com quatro divisões", "com oito meio", "com dezesseis um quarto", "com trinta e duas"])):
            self.gat(fr)
            anims = []
            if nn > 4:
                ca2, coa2 = caixas_arco(vD, nn), coluna_arco(vD, nn)
                l2n = TC("2", *vD.px(2.3 + 2 / nn + .14, 1), 28, "c")
                l2n._origem = "troca (rótulo da altura)"
                l2n._esc = True
                anims += [*[ReplacementTransform(ca[i], VGroup(ca2[2 * i], ca2[2 * i + 1])) for i in range(len(ca))],
                          ReplacementTransform(coa, coa2), ReplacementTransform(l2, l2n)]
                ca, coa, l2 = ca2, coa2, l2n
            g = VGroup(*gls[ini:cortes[k]])
            g._tex = f"{seq._tex}[{ini}:{cortes[k]}]"
            self.play(caneta(g, ritmo=CANETA_P / 0.30), *anims, run_time=0.8)
            grupos.append(g)
            ini = cortes[k]
        self.remove(*grupos)
        seq._em_caneta, seq._esc = False, True
        self.add(seq)
        self.origem(seq, "caneta (por partes)")
        self.marca("16")

        # ── B4-3 · o resultado geral (alvo 17, v2): a figura das caixas fica, as bordas entram uma por vez ───────
        self.an("B4-3")
        vP = Vw(170, 800, 190, 190 * .58)
        nP, hP = 16, 2 / 16
        cxP, colP = caixas_par(vP, nP, wpx=1.5), coluna_par(vP, nP, 2.45, wpx=1.5)
        eixoP = lin_px([vP.px(-.04, 0), vP.px(2.15, 0)], E1, 3, z=5)
        curP = lin_px([vP.px(a, a * a) for a in np.linspace(0, 2, 61)], CI, 4, z=7)
        k1, k2 = vP.px(2.45 + hP, 0), vP.px(2.45 + hP, 4)
        cotaP = lin_px([(k1[0] + 14, k1[1]), (k2[0] + 14, k2[1])], BR, 2, z=8)
        pP = painel(80, 290, 820, 600)
        # a figura do B4-2 (solda, caixas e colunas) vira a parábola com 16 caixas e a coluna empilhada
        sai = [pD, bD, aD, tD, tE, *ca, *coa, l2, aDt, seq, *lsu, *lde, aE, bE]
        self.play(ReplacementTransform(VGroup(*cxE), cxP), ReplacementTransform(VGroup(*pilE), colP), ReplacementTransform(sE, curP),
                  ReplacementTransform(pE, pP), *[FadeOut(m) for m in sai], FadeIn(eixoP), Create(cotaP), run_time=1.1)
        self.remove(*sai)
        l4P = T("4", k1[0] + 26, (k1[1] + k2[1]) / 2 + 10, 28)
        lyP = TP(r"\Ci{y=\X^2}", *vP.px(1.05, 3.3), 30)
        ar = TC(r"\text{área}\le 4\,\Delta=\Me{0{,}5}", 490, 850, 34, "c")
        self.pena(l4P, lyP, ar, rt=1.0)
        g1 = TC(r"\f\ \text{contínua em}\ [a,b]\ \Rightarrow\ \text{gráfico de}\ \f\ \text{tem conteúdo nulo}", 960, 215, 46, "c")
        self.gat("o gráfico de qualquer")
        self.pena(g1)
        self.gat("é exatamente a diferença")
        cz = leg("CAIXAS = S − s → ZERO", 990, 330, MEN, "left", 28)
        gz = sorted(cz.family_members_with_points(), key=lambda g_: g_.get_left()[0])
        cz._em_caneta = True
        za, zb = VGroup(*gz[:-5]), VGroup(*gz[-5:])
        za._tex, zb._tex = "CAIXAS = S − s", "→ ZERO"
        self.play(caneta(za, ritmo=CANETA_P / 0.30))
        self.gat("e toda função contínua")
        self.sublinha(VGroup(*g1[0][1:9]), 1.2)
        self.gat("então essa diferença vai")
        self.play(caneta(zb, ritmo=CANETA_P / 0.30))
        self.remove(za, zb)
        cz._em_caneta, cz._esc = False, True
        self.add(cz)
        self.origem(cz, "caneta (por partes)")
        self.gat("classe cê um")
        c1l = TC(r"\text{curva de classe}\ C^1\ \text{(por partes)}", 990, 420, 40)
        c2l = TC(r"\Rightarrow\ \text{conteúdo nulo}", 990, 490, 40)
        self.pena(c1l, c2l, lag=0.6, passo=0.035)
        self.gat("ou seja com uma")
        ip = len("curvadeclasse") + 2
        c3l = leg("C¹: DERIVADA CONTÍNUA", 994, 550, GEO, "left", 24)
        self.pena(c3l)
        self.gat("feitas de um número finito")
        self.sublinha(VGroup(*c1l[0][ip:ip + 11]), 1.2)
        pI = painel(960, 600, 880, 290)
        self.play(Create(pI), run_time=0.5)
        Ys = 715
        ic = []
        pol = [(-55, 35), (40, 48), (60, -20), (0, -55), (-60, -14)]
        ic.append(lin_px([(1070 + a, Ys + b) for a, b in pol + pol[:1]], CI, 4, z=6))
        ic.append(circ_px(1290, Ys, 55, CI, 4))
        el = Ellipse(width=150 / 120, height=84 / 120).move_to(PX(1510, Ys)).set_stroke(CI, W(4)).set_fill(opacity=0)
        ic.append(sem_ctn(el).set_z_index(6))
        ic.append(lin_px([(1660, Ys + 42), (1800, Ys - 42)], CI, 4, z=6))
        nomes = [leg(t, X, Ys + 120, GEO, "center", 24) for X, t in ((1070, "POLÍGONO"), (1290, "CÍRCULO"), (1510, "ELIPSE"), (1730, "SEGMENTO"))]
        chk = [check_px(X + 70, Ys - 62, MEN, .8) for X in (1070, 1290, 1510, 1730)]
        for fr, k in zip(("segmentos polígonos", "polígonos círculos", "círculos elipses", "elipses e quase"), (3, 0, 1, 2)):
            self.gat(fr)
            self.pena(nomes[k], extra=[Create(ic[k]), Create(chk[k])], rt=0.32, passo=0.02)
        self.gat("a primeira pergunta tem")
        fimq = T("1ª PERGUNTA: SIM, PARA ESSAS BORDAS", 960, 1000, 32, "center", MEN)
        self.pena(fimq)
        self.gat("mas isso não quer dizer")
        gfq = sorted(fimq.family_members_with_points(), key=lambda g_: g_.get_left()[0])
        self.sublinha(VGroup(*gfq[-11:]), 1.2)
        self.marca("17")
        self.sai_fim()
