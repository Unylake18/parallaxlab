"""yt_0032 · S · síntese e próximo (alvos 25 e 26) + CTA padrão."""
from lib32 import *


class PS(B32):
    ANTES = "INTEGRAL SEM INTEGRAR"

    def corpo(self):
        # ── S1 · voltando à balança (alvo 25) ──
        self.an("S1")
        self.secao("SÍNTESE")
        B = balanca(470, 600, 110, ANG_BAL)
        estr = [B[k] for k in ("pe", "poste", "trave", "pivo", "fiel", "anell", "anelr", "cordal", "cordar", "pratol", "prator")]
        self.play(LaggedStart(*[Create(m) for m in estr], lag_ratio=0.06), run_time=1.2)
        self.play(FadeIn(B["leve"], shift=DOWN * 0.3), FadeIn(B["pes"], shift=DOWN * 0.3), FadeIn(B["sl"], shift=DOWN * 0.3),
                  FadeIn(B["sp"], shift=DOWN * 0.3), run_time=0.8)
        lis = [("I SOMA E CONSTANTE · II SINAL · III COMPARAÇÃO", "por isso podemos somar"),
               ("IV CONTEÚDO NULO = 0 · V MUDAR f NO NULO", "um conjunto de conteúdo"),
               ("VI DIVIDIR A REGIÃO · VII VALOR MÉDIO", "dividir a região funciona")]
        for i, (t, gg) in enumerate(lis):
            self.gat(gg)
            self.pena(leg(t, 1100, 700 + 40 * i, GEO, "left", 26))
        self.gat("as três perguntas da")
        self.play(Transform(B["sl"], B["sl"].cor(BR, PRATA_E)), Transform(B["sp"], B["sp"].cor(BR, PRATA_E)), run_time=0.8)
        caixas = [("SOLDA: 0 kg", "a solda matemática não"), ("DENSIDADE NA SOLDA: TANTO FAZ", "o valor limitado que"),
                  ("MÉDIA: CONTINUIDADE + CAMINHO", "e para garantir um")]
        for i, (t, gg) in enumerate(caixas):
            self.gat(gg)
            Y = 280 + i * 110
            cx = moldura(1100, Y - 45, 720, 80, GEO, .45, 2, 12)
            ck = check_px(1140, Y - 6, MEN, .9)
            self.play(Create(cx), run_time=0.4)
            self.play(Create(ck), run_time=0.3)
            self.pena(T(t, 1180, Y + 8, 30))
        self.marca("25")

        # ── S2 · o próximo vídeo e CTA (alvo 26) ──
        self.an("S2")
        tira_canto(self, 0.3)
        self.limpa(rt=0.5)
        v = Vw(250, 900, 240)
        nf, h = 10, 0.2
        tiras = []
        for i in range(nf):
            a, b = i * h, (i + 1) * h
            ga, gb = float(g_solda(a)), float(g_solda(b))
            lv = degrade(poly_px([v.px(a, 0), v.px(b, 0), v.px(b, gb), v.px(a, ga)], LEVE, z=2), LEVE_A, LEVE_B)
            ps = degrade(poly_px([v.px(a, ga), v.px(b, gb), v.px(b, 2), v.px(a, 2)], PESADO, z=2), PES_A, PES_B)
            cs = cordao_ch(v, 3, a0=a, a1=b, z=4)
            tiras.append(VGroup(lv, ps, cs))
        self.play(LaggedStart(*[FadeIn(t) for t in tiras], lag_ratio=0.06), run_time=1.0)
        self.gat("dá para achar a")
        F = TC(r"\Ci{7{,}06}=12-2\cdot\text{área leve}", 1120, 520, 40)
        self.pena(F)
        q = T("COMO CALCULAR O 7,06 EXATO?", 1120, 680, 40, "left", MEN)
        self.pena(q)
        self.gat("a ideia é fatiar")
        self.play(*[t.animate.shift(RIGHT * i * 0.035 * 240 / 120) for i, t in enumerate(tiras)], run_time=1.2)
        self.gat("duas integrais simples trabalhando")
        lf = leg("FATIAR: DUAS INTEGRAIS SIMPLES", 1120, 740, GEO, "left", 26)
        self.pena(lf)
        self.gat("no próximo episódio com")
        p1 = leg("NO PRÓXIMO VÍDEO", 960, 190, GEO, "center", 34)
        p2 = T("TEOREMA DE FUBINI", 960, 280, 66, "center")
        self.pena(p1)
        self.pena(p2)
        self.marca("26", agora=True)
        self.gat("se essa aula te")
        logo_cta(self)
