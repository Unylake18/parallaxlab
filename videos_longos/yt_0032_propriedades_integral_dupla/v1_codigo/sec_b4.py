"""yt_0032 · B4 · mudar f sem mudar a integral (alvos 13 e 14). 2D."""
from lib32 import *

COR_RHO = {"1": "#4F86AE", "3": "#5ED2F0", "2": GEO, "100": CORAL}


def cordao_rho(v, v_rho, w=10):
    c = COR_RHO[v_rho]
    return Cordao(curva_g(v, 0, 160), w, z=7, corpo=c, borda=mixh(c, BG_, .55), escama=mixh(c, "#FFFFFF", .45))


class PB4(B32):
    ANTES = "A SOLDA NÃO PESA"

    def corpo(self):
        # ── B4-1 · cem, dois ou três? (alvo 13) ──
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
        ns = leg("NA SOLDA:", 230, 902, GEO, "left", 26)
        self.play(*[FadeIn(t) for t in tags], run_time=0.4)
        self.pena(ns)
        caixa = moldura(1120, 560, 380, 110, CI, 1.0, 3, 12)
        lm = leg("MASSA", 1145, 600, GEO, "left", 26)
        mv = TC(r"\Ci{\approx 7{,}06}\ \text{kg}", 1145, 640, 44)
        self.play(Create(caixa), run_time=0.4)
        self.pena(lm, mv, lag=0.2)
        for k, (v, gg) in enumerate(zip(("1", "3", "2", "100"), ("a do metal leve", "a do pesado três", "a média dois", "ou aquele exagero de"))):
            self.gat(gg)
            r = tags[k]
            self.play(Transform(cord, cordao_rho(CH, v)), r.animate.set_fill(r._acesa, 1), run_time=0.3)
            self.pena(labs[k])
        self.gat("para a massa total")
        tf = leg("TANTO FAZ", 1530, 630, MEN, "left", 30)
        self.pena(tf)
        self.gat("na fórmula aparece o")
        Cj = L([("a", r"\{(\X,\Y)\in B\ "), ("bar", "|"), ("c", r"\ \f\neq\g\}")], 1120, 290, 44)
        self.pena(Cj)
        self.gat("se lê tais que")
        self.sublinha(gl(Cj, "bar"), 1.0)
        lt = leg('| : "TAIS QUE"', 1120, 345, GEO, "left", 26)
        self.pena(lt)
        self.gat("se esse conjunto tem")
        Cn = TC(r"\text{tem conteúdo nulo}\ \Rightarrow\ \iint_B\f=\iint_B\g", 1120, 430, 40)
        self.pena(Cn)
        self.gat("então podemos mudar a")
        for v in ("1", "3", "2", "100"):
            self.play(Transform(cord, cordao_rho(CH, v)), run_time=0.25)
            self.wait(0.35)
        self.marca("13")

        # ── B4-2 · o motivo e a função com furo (alvo 14) ──
        self.an("B4-2")
        self.limpa(rt=0.5)
        self.grade_off(rt=0)
        v1 = Vw(140, 760, 180)
        fundo = ret_px(*v1.px(0, 2), *v1.px(2, 0), fill="#1A1534", z=1)
        b1 = borda_ch(v1, GEO, 2)
        lfg = TC(r"\f-\g", *v1.px(1, 2.2), 34, "c")
        self.play(FadeIn(fundo), Create(b1), run_time=0.6)
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
        A1 = L([("ii", r"\iint_B"), ("lp", "("), ("f", r"\f"), ("m", "-"), ("g", r"\g"), ("rp", ")"), ("eq", "=0")], 1240, 330, 48)
        self.pena(A1)
        la = leg("SÓ AS CÉLULAS DA SOLDA → ÁREA → 0", 1240, 385, GEO, "left", 26)
        self.pena(la)
        self.gat("e pela propriedade da")
        A2 = L([("ii", r"\iint_B"), ("f", r"\f"), ("m", "-"), ("ii2", r"\iint_B"), ("g", r"\g"), ("eq", "=0")], 1240, 480, 44)
        gm(self, A1, A2, [("ii", "ii"), ("f", "f"), ("m", "m"), ("ii", "ii2"), ("g", "g"), ("eq", "eq")], rt=1.3, copia=True, nota="mapa 5a")
        A3 = L([("imp", r"\Rightarrow\ "), ("ii", r"\iint_B"), ("f", r"\f"), ("eq", "="), ("ii2", r"\iint_B"), ("g", r"\g")], 1240, 480, 44)
        gm(self, A2, A3, [("ii", "ii"), ("f", "f"), ("m", "eq"), ("ii2", "ii2"), ("g", "g")], rt=1.3, nota="mapa 5b")
        lp = leg("PELA PROPRIEDADE DA SOMA", 1240, 530, GEO, "left", 26)
        self.pena(lp)
        self.gat("isso também resolve uma")
        C = PX(840, 580)
        disco = sem_ctn(Circle(radius=180 / 120).move_to(C).set_fill(mixh(BG_, CI, .45), 1).set_stroke(GEO, W(2))).set_z_index(1)
        self.play(GrowFromCenter(disco), run_time=0.8)
        self.gat("como um furo na")
        furo = circ_px(840, 580, 12, BR, 2, dash=(5, 4), fill=BG_, fop=1, z=4)
        self.play(FadeIn(furo, scale=0.5), run_time=0.5)
        lfu = leg("FURO: QUALQUER VALOR", 840, 880, GEO, "center", 26)
        self.pena(lfu)
        self.gat("podemos preenchê los com")
        it = TC(r"\iint_D \Ci{h}\ \text{não muda}", 840, 350, 30, "c")
        self.pena(it)
        tampa = None
        for c in (E1, E2, CORAL):
            nova = circ_px(840, 580, 11, c, 1, fill=c, fop=1, z=5)
            self.play(FadeIn(nova) if tampa is None else Transform(tampa, nova), run_time=0.4)
            if tampa is None:
                tampa = nova
            self.wait(0.5)
        self.gat("o valor da integral")
        p1 = leg("PONTOS SEM DEFINIÇÃO, COM CONTEÚDO NULO:", 1240, 650, MEN, "left", 26)
        p2 = leg("PREENCHE E A INTEGRAL NÃO MUDA", 1240, 690, MEN, "left", 26)
        self.pena(p1, p2, lag=0.5)
        self.marca("14")
        self.sai_fim()
