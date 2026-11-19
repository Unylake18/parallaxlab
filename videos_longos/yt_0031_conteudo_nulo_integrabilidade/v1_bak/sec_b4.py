"""yt_0031 · B4 · curvas têm conteúdo nulo (alvos 15 a 17)."""
from v31 import *

MEN_ = lambda a: mixh(BG_, MEN, a)


def caixa_v(v, a, b, c, d, fill, wpx=2, z=4):
    return ret_px(*v.px(a, d), *v.px(b, c), fill=MEN_(fill), stroke=MEN, wpx=wpx, z=z)


class PB4(B31):
    ANTES = "CONTEÚDO NULO"

    def pena_partes(self, Tm, cortes, frases):
        """Escreve um texto em pedaços (um por frase da voz): cortes = índices de glifo onde cada pedaço termina."""
        gl = sorted(Tm.family_members_with_points(), key=lambda g: g.get_left()[0])
        ini, grupos = 0, []
        Tm._em_caneta = True
        for fim, fr in zip(cortes, frases):
            if fr:
                self.gat(fr)
            g = VGroup(*gl[ini:fim])
            g._tex = Tm._tex + f"[{ini}:{fim}]"
            self.play(caneta(g, ritmo=CANETA_P / 0.30))
            grupos.append(g)
            ini = fim
        self.remove(*grupos)
        Tm._em_caneta, Tm._esc = False, True
        self.add(Tm)

    def corpo(self):
        # ── B4-1 · a parábola (alvo 15) ─────────────────────────────────────────────────────────────
        self.an("B4-1")
        self.secao("CURVAS TÊM CONTEÚDO NULO")
        self.grade_on(rt=0.4)
        v = Vw(200, 900, 300, 300 * .4)
        n, h = 8, .25
        sx = seta_px(v.px(-.05, 0), v.px(2.85, 0), E1, 3, 16)
        sy = seta_px(v.px(0, -.05), v.px(0, 4.6), CI, 3, 16)
        nums = [leg(str(k), v.px(0, k)[0] - 14, v.px(0, k)[1] + 8, CI, "right", 20) for k in (1, 2, 3, 4)]
        curva = lin_px([v.px(a, a * a) for a in np.linspace(0, 2, 61)], CI, 4, z=7)
        ly = TP(r"\Ci{y=\X^2}", *v.px(1.2, 3.6), 32)
        self.gat("lembra da parábola")
        self.play(FadeIn(sx), FadeIn(sy), run_time=0.5)
        self.pena(*nums, extra=[Create(curva)], rt=1.2)
        self.pena(ly)
        self.gat("desenha uma caixa")
        cx = [caixa_v(v, i * h, i * h + h, (i * h) ** 2, (i * h + h) ** 2, .25) for i in range(n)]
        for c in cx:
            self.play(FadeIn(c), run_time=0.3)
        l0 = leg("CAIXAS: DO PISO AO TETO", 1124, 260, MEN, "left", 28)
        self.gat("juntas as caixas cobrem")
        self.pena(l0)
        self.gat("a curva é crescente")
        seta_e = seta_px(v.px(2.12, 2), v.px(2.3, 2), GEO, 3, 12)
        self.play(FadeIn(seta_e), run_time=0.3)
        self.gat("empurrar as caixas")
        z = 0
        pilha = []
        for i in range(n):
            a, b = i * h, i * h + h
            d = b * b - a * a
            nv = caixa_v(v, 2.35, 2.35 + h, z, z + d, .35)
            self.play(TransformFromCopy(cx[i], nv), run_time=0.3)
            pilha.append(nv)
            z += d
        self.gat("todas cabem numa coluna")
        c1, c2 = v.px(2.35 + h, 0), v.px(2.35 + h, 4)
        cota = lin_px([(c1[0] + 16, c1[1]), (c2[0] + 16, c2[1])], BR, 2, z=8)
        l4 = T("4", c1[0] + 30, (c1[1] + c2[1]) / 2, 28)
        lD = TC(r"\Delta", *v.px(2.35 + h / 2, -.5), 28, "c")
        self.play(Create(cota), run_time=0.5)
        self.pena(l4, lD)
        self.gat("área total no máximo")
        fa = TC(r"\text{área das caixas}\ \le\ 4\,\Delta", 1120, 350, 40)
        nfa = len(fa[0])
        self.escreve(fa, voos=[(l4, [nfa - 2])], passo=0.045)
        rows = [TC(a + r"\ \text{pedaços}\ \to\ \Me{" + b + "}", 1120, 460 + k * 70, 36) for k, (a, b) in enumerate((("4", "2"), ("8", "1"), ("16", "0{,}5")))]
        for fr, r in zip(("com quatro pedaços", "com oito um", "com dezesseis meio"), rows):
            self.gat(fr)
            self.pena(r, passo=0.04)
        self.gat("o gráfico da parábola")
        fim = T("O GRÁFICO TEM CONTEÚDO NULO", 1120, 720, 32)
        self.pena(fim)
        self.marca("15")

        # ── B4-2 · a solda e o arco (alvo 16) ───────────────────────────────────────────────────────
        self.an("B4-2")
        tudo = [sx, sy, *nums, curva, ly, *cx, l0, seta_e, *pilha, cota, l4, lD, fa, *rows, fim]
        self.grade_off(rt=0.5, junto=[FadeOut(m) for m in tudo])
        self.remove(*tudo)
        pE, pD = painel(80, 190, 860, 760), painel(990, 190, 860, 760)
        vE, vD = Vw(150, 800, 250), Vw(1050, 800, 250)
        bE, bD = borda_ch(vE, mixh(BG_, GEO, .5), 2), borda_ch(vD, mixh(BG_, GEO, .5), 2)
        sE = solda_px(vE, BR, 4)
        tE, tD = T("A SOLDA", 510, 260, 30, "center"), T("O ARCO", 1420, 260, 30, "center")
        self.play(FadeIn(pE), Create(bE), Create(sE), run_time=0.8)
        self.pena(tE)
        self.gat("então separa os dois")
        cxE, sobe = [], []
        for i in range(n):
            a, b = i * h, i * h + h
            mn, mx = faixa(a, b)
            s_ = g_solda(b) > g_solda(a)
            sobe.append(s_)
            cxE.append(caixa_v(vE, a, b, mn, mx, .30 if s_ else .12))
        self.play(LaggedStart(*[FadeIn(c) for c in cxE], lag_ratio=0.15), run_time=1.4)
        self.gat("as caixas da subida")
        zu = zd = 0
        X1, X2 = 2.25, 2.25 + h + .12
        pilE = []
        for i in range(n):
            a, b = i * h, i * h + h
            mn, mx = faixa(a, b)
            d = mx - mn
            if sobe[i]:
                nv = caixa_v(vE, X1, X1 + h, .5 + zu, .5 + zu + d, .35)
                zu += d
            else:
                nv = caixa_v(vE, X2, X2 + h, .5 + zd, .5 + zd + d, .15)
                zd += d
            self.play(TransformFromCopy(cxE[i], nv), run_time=0.45)
            pilE.append(nv)
        lsu = [TC(r"0{,}58", *vE.px(X1 + h / 2, .5 + zu + .12), 26, "c"), leg("SOBE", *vE.px(X1 + h / 2, .32), GEO, "center", 20)]
        lde = [TC(r"0{,}36", *vE.px(X2 + h / 2, .5 + zd + .12), 26, "c"), leg("DESCE", *vE.px(X2 + h / 2, .32), GEO, "center", 20)]
        self.pena(*lsu, rt=0.8)
        self.gat("e as da descida")
        self.pena(*lde, rt=0.8)
        self.gat("área total no máximo")
        aE = TC(r"\text{área}\le 0{,}94\,\Delta", 510, 900, 36, "c")
        self.pena(aE)
        self.gat("o arco do quarto")
        aD = arco_px(vD, CI, 4)
        self.play(FadeIn(pD), Create(bD), Create(aD), run_time=0.8)
        self.pena(tD)
        cxD = []
        za = 0
        pilD = []
        for i in range(n):
            a, b = i * h, i * h + h
            hi, lo = math.sqrt(4 - a * a), math.sqrt(max(0, 4 - b * b))
            cxD.append(caixa_v(vD, a, b, lo, hi, .28))
        self.play(LaggedStart(*[FadeIn(c) for c in cxD], lag_ratio=0.12), run_time=1.0)
        self.gat("então as caixas dele")
        for i in range(n):
            a, b = i * h, i * h + h
            d = math.sqrt(4 - a * a) - math.sqrt(max(0, 4 - b * b))
            nv = caixa_v(vD, 2.3, 2.3 + h, za, za + d, .35)
            self.play(TransformFromCopy(cxD[i], nv), run_time=0.3)
            pilD.append(nv)
            za += d
        l2 = TC("2", *vD.px(2.3 + h + .14, 1), 28, "c")
        aDt = TC(r"\text{área}=2\,\Delta", 1420, 900, 36, "c")
        self.pena(l2)
        self.pena(aDt)
        seq = leg("4 → 1 · 8 → 0,5 · 16 → 0,25 · 32 → 0,125", 1420, 940, MEN, "center", 22)
        self.pena_partes(seq, [4, 10, 18, 26], ["com quatro divisões", "com oito meio", "com dezesseis um quarto", "com trinta e duas"])
        self.marca("16")

        # ── B4-3 · o resultado geral (alvo 17) ──────────────────────────────────────────────────────
        self.an("B4-3")
        tudo = [pE, pD, bE, bD, sE, aD, tE, tD, *cxE, *pilE, *cxD, *pilD, *lsu, *lde, aE, l2, aDt, seq]
        self.play(*[FadeOut(m) for m in tudo], run_time=0.5)
        self.remove(*tudo)
        g1 = TC(r"\f\ \text{contínua em}\ [a,b]\ \Rightarrow\ \text{gráfico de}\ \f\ \text{tem conteúdo nulo}", 960, 280, 50, "c")
        self.gat("o gráfico de qualquer")
        self.pena(g1)
        g1l = leg("ÁREA DAS CAIXAS = S − s DA INTEGRAL SIMPLES → ZERO", 960, 360, GEO, "center", 26)
        gl1 = sorted(g1l.family_members_with_points(), key=lambda g_: g_.get_left()[0])
        p0, pa, pb = VGroup(*gl1[:13]), VGroup(*gl1[13:-5]), VGroup(*gl1[-5:])
        p0._tex, pa._tex, pb._tex = "ÁREA DAS CAIXAS", "= S − s DA INTEGRAL SIMPLES", "→ ZERO"
        g1l._em_caneta = True
        self.gat("a área das caixas")
        self.play(caneta(p0, ritmo=CANETA_P / 0.30))
        self.gat("é exatamente a diferença")
        self.play(caneta(pa, ritmo=CANETA_P / 0.30))
        self.gat("e toda função contínua")
        self.sublinha(VGroup(*g1[0][1:9]), 1.2)
        self.gat("então essa diferença vai")
        self.play(caneta(pb, ritmo=CANETA_P / 0.30))
        self.remove(p0, pa, pb)
        g1l._em_caneta, g1l._esc = False, True
        self.add(g1l)
        self.gat("o livro vai além")
        g2 = TC(r"\text{curva de classe}\ C^1\ \text{(por partes)}\ \Rightarrow\ \text{conteúdo nulo}", 960, 470, 44, "c")
        self.pena(g2)
        self.gat("ou seja com uma")
        g2l = leg("C¹: DERIVADA CONTÍNUA", 960, 540, GEO, "center", 24)
        self.pena(g2l)
        self.gat("feitas de um número finito")
        ip = len(r"curvadeclasse") + 2
        self.sublinha(VGroup(*g2[0][ip:ip + 11]), 1.2)
        Ys = 760
        ic = []
        pol = [(-80, 50), (60, 70), (90, -30), (0, -80), (-90, -20)]
        ic.append(lin_px([(420 + a, Ys + b) for a, b in pol + pol[:1]], CI, 4, z=6))
        ic.append(circ_px(800, Ys, 80, CI, 4))
        el = Ellipse(width=220 / 120, height=124 / 120).move_to(PX(1180, Ys)).set_stroke(CI, W(4)).set_fill(opacity=0)
        ic.append(sem_ctn(el).set_z_index(6))
        ic.append(lin_px([(1420, Ys + 60), (1620, Ys - 60)], CI, 4, z=6))
        nomes = [leg(t, X, Ys + 130, GEO, "center", 26) for X, t in ((420, "POLÍGONO"), (800, "CÍRCULO"), (1180, "ELIPSE"), (1520, "SEGMENTO"))]
        chk = [check_px(X + 100, Ys - 80) for X in (420, 800, 1180, 1520)]
        for fr, k in zip(("segmentos polígonos", "círculos elipses", "elipses e quase", "e quase toda borda"), (3, 0, 1, 2)):
            self.gat(fr)
            self.play(Create(ic[k]), run_time=0.45)
            self.pena(nomes[k], passo=0.025)
        for k in (0, 1, 2, 3):
            self.play(Create(chk[k]), run_time=0.35)
        self.gat("para essas bordas")
        fimq = T("1ª PERGUNTA: SIM, PARA ESSAS BORDAS", 960, 1010, 32, "center", MEN)
        self.pena(fimq)
        self.gat("mas isso não quer dizer")
        gfq = sorted(fimq.family_members_with_points(), key=lambda g_: g_.get_left()[0])
        self.sublinha(VGroup(*gfq[-11:]), 1.2)
        self.marca("17")
        self.sai_fim()
