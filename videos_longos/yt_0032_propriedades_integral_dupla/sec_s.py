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
        props = [("I", "SOMA E CONSTANTE"), ("II", "SINAL"), ("III", "COMPARAÇÃO"), ("IV", "CONTEÚDO NULO = 0"), ("V", "MUDAR f NO NULO"),
                 ("VI", "DIVIDIR A REGIÃO"), ("VII", "VALOR MÉDIO")]
        grupos = [(range(0, 3), "por isso podemos somar"), (range(3, 5), "um conjunto de conteúdo"), (range(5, 7), "dividir a região funciona")]
        for ids, gg in grupos:                            # C16 (final): mesmo gatilho do agrupamento de antes
            self.gat(gg)
            linhas_ = []
            for k in ids:
                Y = 610 + 44 * k
                rn = T(props[k][0], 1100, Y, 30, "left", CI)
                tx = T(props[k][1], 1170, Y, 30, "left", BR)
                linhas_ += [rn, tx]
            self.pena(*linhas_, lag=0.25)
        self.gat("e o teorema do")                         # palco: o ponto laranja da média nasce na solda (o 1,76 do B6-4)
        dmed = ponto_px(*B["_vr"].px(1, float(g_solda(1))), POS, 9, z=9)
        self.play(GrowFromCenter(dmed), run_time=0.6)
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
            if i == 1:                                    # palco: a solda acende em ρ = 100 e volta (tanto faz para a massa)
                self.play(Transform(B["sl"], B["sl"].cor(CORAL, mixh(CORAL, "#FFFFFF", .45))), Transform(B["sp"], B["sp"].cor(CORAL, mixh(CORAL, "#FFFFFF", .45))),
                          run_time=0.6)
                self.play(Transform(B["sl"], B["sl"].cor(PRATA, PRATA_C)), Transform(B["sp"], B["sp"].cor(PRATA, PRATA_C)), run_time=0.6)
        self.marca("25")

        # ── S2 · o próximo vídeo e CTA (alvo 26) ──
        self.an("S2")
        self.secao("O PRÓXIMO PASSO")                    # C18 (final): o canto não fica vazio no S2
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
        self.gat("grades cada vez mais")                  # palco: a grade refina sobre a chapa
        grd = VGroup()
        for nn in (4, 8, 16):                             # C17 (final): só as linhas novas, por Create no lugar; as velhas ficam
            novas = grade_ch(4, v, mixh(BG_, "#FFFFFF", .55), 1, z=6) if nn == 4 else linhas_novas(v, nn, mixh(BG_, "#FFFFFF", .55), 1, z=6)
            self.play(LaggedStart(*[Create(l) for l in novas], lag_ratio=0.05), run_time=0.8)
            grd.add(*novas)
            self.wait(0.4)
        self.gat("dá para achar a")
        q = T("COMO CALCULAR O 7,06 EXATO?", 1120, 690, 40, "left", MEN)
        self.pena(q)
        self.gat("numa conta no papel")                    # D10: a massa com origem (3 em toda a chapa, menos 2 no pedaço leve)
        o1 = leg("3 kg/m² NA CHAPA TODA, MENOS 2 NO PEDAÇO LEVE", 1120, 400, GEO, "left", 26)
        P0 = L([("m", r"\text{massa}"), ("eq", "="), ("t3", "3"), ("d", r"\cdot"), ("t4", "4"), ("mn", "-"), ("r", r"2\cdot\text{área leve}")], 1120, 470, 40)
        self.pena(o1, P0, lag=0.5, passo=0.04)             # sync: legenda e conta quase juntas
        reg_l = poly_px([v.px(0, 0), v.px(2, 0)] + curva_g(v)[::-1], CI, .25, z=5)       # C11 (final): onde está a área leve
        reg_l.set_stroke(CI, W(3), 1)
        lal = leg("ÁREA LEVE: ABAIXO DA SOLDA", 250, 950, GEO, "left", 26)
        self.pena(lal, passo=0.045, extra=[FadeIn(reg_l)])  # a região acende enquanto a legenda nasce
        P1 = L([("m", r"\Ci{7{,}06}"), ("eq", "="), ("doze", "12"), ("mn", "-"), ("r", r"2\cdot\text{área leve}")], 1120, 560, 40)
        gm(self, P0, P1, [("m", "m"), ("eq", "eq"), (["t3", "d", "t4"], "doze"), ("mn", "mn"), ("r", "r")], rt=1.1, copia=True,
           extra=[reg_l.animate(rate_func=lambda t: max(0.0, (t - 0.4) / 0.6)).set_fill(opacity=0)],   # C11: o preenchimento apaga durante o mapa 13
           nota="mapa 13 (M13, S2: 3·4 colapsa em 12)")
        self.gat("a ideia é fatiar")
        self.play(FadeOut(grd), FadeOut(reg_l), *[t.animate.shift(RIGHT * i * 0.035 * 240 / 120) for i, t in enumerate(tiras)], run_time=1.2)
        self.remove(grd, reg_l)
        self.gat("duas integrais simples trabalhando")
        lf = leg("FATIAR: DUAS INTEGRAIS SIMPLES", 1120, 745, GEO, "left", 26)
        self.pena(lf)
        self.gat("é isso que vamos")                       # D11: o cartão entra aqui e fica até "deixa o like..." terminar
        p1 = leg("NO PRÓXIMO VÍDEO", 960, 170, GEO, "center", 34)
        p2 = T("TEOREMA DE FUBINI", 960, 255, 66, "center")
        print(f"[fubini] entra {self.t:.2f}")
        self._fixo_rt = True                              # o cartão é escrito no ritmo normal da caneta (sem alongar)
        self.pena(p1)
        self.pena(p2)
        self._fixo_rt = False
        self.marca("26", agora=True)
        self.gat("e conta nos comentários")
        print(f"[fubini] sai {self.t:.2f}")
        logo_cta(self)
