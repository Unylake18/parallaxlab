"""yt_0032 · B4 · mudar f sem mudar a integral (alvos 13 v2 e 14 v2). 2D.
v2: f e g definidos antes do conjunto (D5); sem letras novas no B4-2 (D6): f − g, o disco de f com furo na origem; mapa M10 em 3 linhas."""
from lib32 import *

COR_RHO = {"1": "#4F86AE", "3": "#5ED2F0", "2": GEO, "100": CORAL}


def cordao_rho(v, v_rho, w=10):
    c = COR_RHO[v_rho]
    return Cordao(curva_g(v, 0, 160), w, z=7, corpo=c, borda=mixh(c, BG_, .55), escama=mixh(c, "#FFFFFF", .45))


class PB4(B32):
    ANTES = "A SOLDA NÃO PESA"

    def corpo(self):
        # ── B4-1 · cem, dois ou três? (alvo 13 v2) ──
        self.an("B4-1")
        self.secao("MUDAR f SEM MUDAR A INTEGRAL")
        self.grade_on(CH, rt=0)
        leve, pes = metais_liso(CH)
        bord = borda_ch(CH, GEO, 2)
        cord = cordao_ch(CH, 6)
        sx, sy, lx, ly = eixos_chapa(CH)
        self.play(FadeIn(leve), FadeIn(pes), FadeIn(bord), FadeIn(cord), GrowFromPoint(sx, CH.P(0, 0)), GrowFromPoint(sy, CH.P(0, 0)), run_time=0.9)
        self.pena(lx, ly)
        self.gat("qual densidade devemos colocar")
        self.play(Transform(cord, cordao_rho(CH, "100")), run_time=0.8)
        tags, labs = [], []
        for i, (v, c) in enumerate((("1", LEVE), ("3", PESADO), ("2", GEO), ("100", CORAL))):
            X = 380 + i * 120
            r = RoundedRectangle(width=104 / 120, height=48 / 120, corner_radius=8 / 120).move_to(PX(X + 52, 894))
            r.set_fill(mixh(BG_, c, .14), 1).set_stroke(mixh(BG_, c, .5), W(1.5))
            r._acesa = mixh(BG_, c, .5)
            tags.append(sem_ctn(r).set_z_index(3))
            labs.append(TC(r"\rr=" + v, X + 52, 894, 26, "c"))
        ns = leg("NA SOLDA:", 220, 902, GEO, "left", 26)
        self.play(*[FadeIn(t) for t in tags], run_time=0.4)
        self.pena(ns)
        caixa = moldura(1120, 650, 380, 110, CI, 1.0, 3, 12)
        lm = leg("MASSA", 1145, 690, GEO, "left", 26)
        mv = TC(r"\Ci{\approx 7{,}06}\ \text{kg}", 1145, 730, 44)
        self.play(Create(caixa), run_time=0.4)
        self.pena(lm, mv, lag=0.2)
        fdef = gdef = None
        for k, (v, gg) in enumerate(zip(("1", "3", "2", "100"), ("a do metal leve", "a do pesado três", "o meio termo dois", "ou aquele exagero de"))):
            self.gat(gg)
            r = tags[k]
            self.play(Transform(cord, cordao_rho(CH, v)), r.animate.set_fill(r._acesa, 1), run_time=0.3)
            self.pena(labs[k])
            if v == "1":                                  # D5: f é a densidade com ρ = 1 na solda
                fdef = mista([("m", r"\f:\ \rr=1"), ("t", "NA SOLDA")], 1120, 230, 30)
                self.pena(fdef)
            if v == "100":                                # D5: g é a mesma densidade com ρ = 100 na solda
                gdef = mista([("m", r"\g:\ \rr=100"), ("t", "NA SOLDA")], 1120, 290, 30)
                self.pena(gdef)
        self.gat("para a massa total")
        tf = leg("TANTO FAZ", 1530, 720, MEN, "left", 30)
        self.pena(tf)
        self.gat("se duas funções integráveis")
        ig = leg("IGUAIS FORA DA SOLDA", 1120, 340, GEO, "left", 26)
        self.pena(ig)
        self.gat("na fórmula aparece o")
        Cj = L([("a", r"\{(\X,\Y)\in B\ "), ("bar", "|"), ("c", r"\ \f\neq\g\}")], 1120, 430, 44)
        self.pena(Cj)
        self.gat("se lê tais que")
        lt = leg('| : "TAIS QUE"', 1120, 485, GEO, "left", 26)
        gb_ = gl(Cj, "bar")                                   # sync: o sublinhado fica enquanto a legenda nasce
        sb_ = sublinha_px(pxof(gb_.get_left())[0] - 2, pxof(gb_.get_right())[0] + 2, pxof(gb_.get_bottom())[1] + 7)
        self.play(Create(sb_), run_time=0.25)
        self.pena(lt)
        self.play(FadeOut(sb_), run_time=0.25)
        self.remove(sb_)
        self.gat("se esse conjunto tem")
        Cn = mista([("t", "TEM CONTEÚDO NULO"), ("m", r"\Rightarrow\ \iint_B\f=\iint_B\g")], 1120, 565, 30)
        self.pena(Cn)
        self.gat("então podemos mudar a")
        for v in ("1", "3", "2", "100"):
            self.play(Transform(cord, cordao_rho(CH, v)), run_time=0.25)
            self.wait(0.35)
        self.marca("13")

        # ── B4-2 · o motivo e a função com furo (alvo 14 v2) ──
        self.an("B4-2")
        self.limpa(rt=0.5)
        self.grade_off(rt=0)
        v1 = Vw(140, 760, 180)
        fundo = ret_px(*v1.px(0, 2), *v1.px(2, 0), fill="#1A1534", z=1)
        g8 = grade_ch(8, v1, mixh(BG_, GEO, .35), 1, z=2)
        b1 = borda_ch(v1, GEO, 2)
        lfg = TC(r"\f-\g", *v1.px(1, 2.2), 36, "c")
        self.play(FadeIn(fundo), Create(b1), FadeIn(g8), run_time=0.6)
        self.pena(lfg)
        self.gat("a diferença entre elas")
        z0 = leg("ZERO FORA DA SOLDA", 320, 880, GEO, "center", 26)
        self.pena(z0)

        def cel(n):
            h = 2 / n
            g = VGroup()
            for i, j in sorted(celulas_verm(n)):
                g.add(ret_px(*v1.px(i * h, (j + 1) * h), *v1.px((i + 1) * h, j * h), fill=mixh(BG_, CORAL, .8), z=2))
            return g
        self.gat("só contam as células")
        cc = cel(16)
        self.play(LaggedStart(*[FadeIn(c) for c in cc], lag_ratio=0.04), run_time=1.0)
        self.gat("pode ser tornada arbitrariamente")
        for n in (32, 64):
            nv = cel(n)
            self.play(ReplacementTransform(cc, nv), run_time=1.0)
            cc = nv
            self.wait(0.3)
        self.gat("a integral da diferença")
        A1 = L([("ii", r"\iint_B"), ("lp", "("), ("f", r"\f"), ("m", "-"), ("g", r"\g"), ("rp", ")"), ("eq", "="), ("z", "0")], 1240, 330, 48)
        self.escreve(A1, voos=[(lfg, A1._ix["f"] + A1._ix["m"] + A1._ix["g"])], atraso_caneta=0.15)    # o f − g liga às caixas
        la = leg("SÓ AS CÉLULAS DA SOLDA → ÁREA → 0", 1240, 388, GEO, "left", 26)
        self.pena(la, passo=0.035)                         # sync
        self.gat("e pela propriedade da")
        # M10 (v2): ∬(f − g) = 0 → ∬f − ∬g = 0 → ∬f = ∬g, os três passos visíveis
        A2 = L([("ii", r"\iint_B"), ("f", r"\f"), ("m", "-"), ("ii2", r"\iint_B"), ("g", r"\g"), ("eq", "="), ("z", "0")], 1240, 470, 44)
        gm(self, A1, A2, [("ii", "ii"), ("f", "f"), ("m", "m"), ("ii", "ii2"), ("g", "g"), ("eq", "eq"), ("z", "z")], rt=1.3, copia=True,
           nota="mapa 5a (M10, B4-2: a integral se distribui)")
        A3 = L([("ii", r"\iint_B"), ("f", r"\f"), ("eq", "="), ("ii2", r"\iint_B"), ("g", r"\g")], 1240, 550, 44)
        gm(self, A2, A3, [("ii", "ii"), ("f", "f"), ("m", "eq"), ("ii2", "ii2"), ("g", "g")], rt=1.3, copia=True,
           nota="mapa 5b (M10, B4-2: ∬g atravessa)")
        lp = leg("PELA PROPRIEDADE DA SOMA", 1240, 605, GEO, "left", 26)
        self.pena(lp)
        self.gat("isso também resolve uma")
        di = disco_img(840, 580, 180, lambda t: np.cos(t) ** 2, "#1A1534", E1, z=1)       # o disco do B7: f = x²/(x² + y²)
        cdi = circ_px(840, 580, 180, GEO, 2, z=3)
        self.play(FadeIn(di, scale=0.7), Create(cdi), run_time=0.8)
        lfu = leg("UMA FUNÇÃO COM FURO NA ORIGEM", 840, 880, GEO, "center", 26)          # C13 (final)
        self.pena(lfu)
        self.gat("como um furo na")
        furo = circ_px(840, 580, 12, BR, 2, dash=(5, 4), fill=BG_, fop=1, z=4)
        self.play(FadeIn(furo, scale=0.5), run_time=0.5)
        it = TC(r"\iint_{\text{disco}}\Am{\dfrac{x^2}{x^2+y^2}}", 840, 352, 34, "c")       # C13 (final): a função do B7
        self.pena(it)
        self.gat("podemos preenchê los com")
        tampa, lv = None, None
        for val, c in (("0", "#1A1534"), ("1", E1), ("5", CORAL)):      # 3 valores diferentes; o contador ∬ fica parado
            nova = circ_px(840, 580, 11, c, 1, fill=c, fop=1, z=5)
            nl = TP(r"\text{no furo}=" + val, 1036, 640, 28, "l")    # C13 (final): à direita do disco
            if tampa is None:
                self.play(FadeIn(nova), run_time=0.4)
                tampa = nova
                self.pena(nl)
            else:
                self.play(Transform(tampa, nova), FadeOut(lv), run_time=0.4)
                self.remove(lv)
                self.pena(nl)
            lv = nl
            self.wait(0.6)
        self.gat("o valor da integral")
        p2 = leg("PREENCHE O FURO: A INTEGRAL NÃO MUDA", 1240, 700, MEN, "left", 26)
        self.pena(p2)
        self.marca("14")
        self.sai_fim()
