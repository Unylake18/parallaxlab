"""yt_0032 · H · a balança e as três perguntas (alvos 01 e 02). Arte v1b: metal em degradê e escovado, cordão de solda depositado por uma
ponta quente, balança com pivô, fiel e pratos em cuba, que pende para o lado do pedaço pesado."""
from lib32 import *


class PH(B32):
    CANTO = True

    def corpo(self):
        self.an("H1")
        self.secao("A SOLDA PESA ALGUMA COISA?")
        self.grade_on(CH, rt=0)
        leve, pes = metais_liso(CH)
        bord = borda_ch(CH, GEO, 2)
        cord = cordao_ch(CH, 10)
        sx, sy, lx, ly = eixos_chapa(CH)
        self.play(GrowFromEdge(leve, DOWN), FadeIn(bord), GrowFromPoint(sx, CH.P(0, 0)), GrowFromPoint(sy, CH.P(0, 0)), run_time=1.2)
        self.pena(lx, ly)
        self.gat("um quilo por metro")
        r1 = TP(r"\rr=1", *CH.px(1.0, .45), 32)
        self.pena(r1)
        self.gat("em cima três")
        self.play(GrowFromEdge(pes, UP), run_time=1.0)
        self.play(deposita(cord, 1.8), run_time=1.8)
        r3 = TP(r"\rr=3", *CH.px(1.0, 1.72), 32)
        self.pena(r3)
        self.gat("a massa total existe")
        tot = TC(r"\Ci{7{,}06}\ \text{kg}", 600, 862, 40, "c")
        self.pena(tot)

        # a chapa se parte na solda (o cordão se divide entre os dois pedaços); os pedaços descem cada um num prato
        self.gat("cortar a chapa exatamente")
        B = balanca(470, 690, 110, 0.0)
        cl, cp = cord, cord.copy()
        self.add(cp)
        self.play(VGroup(leve, cl).animate.shift(DOWN * 24 / 120), VGroup(pes, cp).animate.shift(UP * 24 / 120),
                  *[FadeOut(m) for m in (r1, r3, tot, bord, sx, sy, lx, ly, leve[1], pes[1])], run_time=0.9)
        self.remove(r1, r3, tot, bord, sx, sy, lx, ly, leve[1], pes[1])
        self.grade_off(rt=0)
        estr = [B[k] for k in ("pe", "poste", "trave", "pivo", "fiel", "anell", "anelr", "cordal", "cordar", "pratol", "prator")]
        self.play(ReplacementTransform(leve[0], B["leve"]), ReplacementTransform(pes[0], B["pes"]),
                  ReplacementTransform(cl, B["sl"]), ReplacementTransform(cp, B["sp"]),
                  LaggedStart(*[Create(m) for m in estr], lag_ratio=0.08), run_time=1.7)
        self.play(balanca_inclina(self, B, 470, 690, 110, 0.0, ANG_BAL, rt=1.8), run_time=1.8)       # o lado pesado desce
        Bt = balanca(470, 690, 110, ANG_BAL)
        self.gat("o pedaço leve tem")
        m1 = TP(r"\Ci{2{,}472}\ \text{kg}", Bt["_vl"].cx + 110, Bt["_vl"].cy - 190, 34)
        self.pena(m1)
        self.gat("o pesado quatro")
        m2 = TP(r"\Ci{4{,}584}\ \text{kg}", Bt["_vr"].cx + 110, Bt["_vr"].cy - 0.836 * 110 - 190, 34)
        self.pena(m2)
        self.gat("usando os valores sem")
        S = L([("a", r"\Ci{2{,}472}"), ("p", "+"), ("b", r"\Ci{4{,}584}"), ("ap", r"\approx \Ci{7{,}06}\ \text{kg}")], 470, 930, 44, "c")
        self.escreve(S, voos=[(VGroup(*m1.f[0][:5]), S._ix["a"]), (VGroup(*m2.f[0][:5]), S._ix["b"])])
        vs = leg("VALORES SEM ARREDONDAR", 470, 985, GEO, "center", 26)
        self.pena(vs)

        # o cordão acende nos dois pedaços
        self.gat("olha a linha branca")
        self.play(Transform(B["sl"], B["sl"].cor(BR, PRATA_E)), Transform(B["sp"], B["sp"].cor(BR, PRATA_E)), run_time=0.6)
        self.gat("ela é a fronteira")
        l1 = leg("A SOLDA É BORDA DOS DOIS PEDAÇOS", 1120, 375, GEO, "left", 26)
        self.pena(l1)
        self.gat("contou a solda duas")
        q1 = T("CONTOU DUAS VEZES?", 1120, 330, 40)
        self.pena(q1)
        self.gat("cem quilos por metro")
        q2 = TC(r"\text{E SE }\rr=100\text{ NA SOLDA?}", 1120, 500, 40)
        self.pena(q2)
        self.gat("densidade média da chapa")
        q3 = TC(r"\text{MÉDIA}\approx\Ci{1{,}76}\ \text{kg/m}^2", 1120, 640, 36)
        self.pena(q3)
        self.gat("existe algum ponto")
        q4 = T("ALGUM PONTO TEM A MÉDIA?", 1120, 710, 40)
        self.pena(q4)
        self.marca("01")

        # ── H2: a balança encolhe para o canto; a frase-tese ──
        self.an("H2")
        B2 = balanca(300, 300, 45, ANG_BAL)
        sai = [m1, m2, S, vs, l1, q1, q2, q3, q4]
        ms = [m for m in (self.h1, self.h2) if m is not None]
        nomes = [k for k in B if not k.startswith("_")]
        self.play(*[FadeOut(m) for m in sai + ms], *[ReplacementTransform(B[k], B2[k]) for k in nomes], run_time=1.4)
        self.remove(*sai, *ms)
        self.h2 = None
        self.gat("a integral nasce de")
        h1 = T("O QUE VALE NA SOMA", 960, 500, 64, "center")
        self.pena(h1)
        self.gat("então as regras que")
        h2 = T("VALE NA INTEGRAL", 960, 590, 64, "center", CI)
        self.pena(h2)
        lst = leg("SOMAR · MULTIPLICAR · COMPARAR · DIVIDIR", 960, 655, GEO, "center", 26)
        faixas_l = [range(0, 6), range(6, 18), range(18, 27), range(27, 34)]           # glifos (sem espaços): SOMAR· MULTIPLICAR· COMPARAR· DIVIDIR
        for fx_, gg in zip(faixas_l, ("somar multiplicar comparar", "multiplicar comparar e", "comparar e dividir", "dividir regiões e")):
            self.gat(gg)
            self.pena(parte(lst, list(fx_), gg.split()[0]))
        self.gat("um conjunto de conteúdo")
        h3 = T("CONTEÚDO NULO NÃO PESA", 960, 740, 44, "center", MEN)
        self.pena(h3)
        self.gat("o mistério da solda")
        self.play(Transform(B2["sl"], B2["sl"].cor(BR, PRATA_E)), Transform(B2["sp"], B2["sp"].cor(BR, PRATA_E)), run_time=0.8)
        self.marca("02")
        self.sai_fim()
