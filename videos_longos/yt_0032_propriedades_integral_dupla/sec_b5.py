"""yt_0032 · B5 · dividir a região (alvos 15, 16 v2, 17). 2D e cartões.
v2: números da mini-balança ≥ 26 px, únicos, que VOAM para a soma; os pedaços se reencaixam (R5); ∪/∩ legíveis (T4); f em todo termo e o
lado esquerdo fica no mapa M6; a faixa nasce de 0,2·2 = 0,4 m² (M11); as miniaturas se partem e se remontam (palco)."""
from lib32 import *


def faixa_hach(v, meia=0.1, cor=AL, z=3):
    """Faixa de largura 2·meia em volta da solda, em ALERTA, com hachura cruzada fina dentro (segmentos calculados na faixa)."""
    up = curva_g(v, meia, 160)
    dn = curva_g(v, -meia, 160)
    corpo = poly_px(up + dn[::-1], mixh(BG_, cor, .55), z=z)
    h = VGroup()
    passo = 0.045
    for a in np.arange(0, 2 - 1e-6, passo):
        b = min(2.0, a + passo * 2.2)
        for s in (1, -1):
            p0 = v.px(a, float(g_solda(a)) - s * meia)
            p1 = v.px(b, float(g_solda(b)) + s * meia)
            h.add(lin_px([p0, p1], mixh(BG_, "#FFFFFF", .35), 1.2, z=z + 1))
    return VGroup(corpo, sem_ctn(h))


def voa_move(sc, F, pares, atraso_caneta=0.4, rt=1.0):
    """Como escreve(), mas a fonte VAI (ReplacementTransform): o número sai da balança e chega na soma; um só, sem duplicado."""
    gl_ = list(F[0])
    usados, anims = set(), []
    for src, idx in pares:
        anims.append(ReplacementTransform(src, VGroup(*[gl_[i] for i in idx]), path_arc=-0.6))
        usados |= set(idx)
    resto = VGroup(*[g for i, g in enumerate(gl_) if i not in usados])
    resto._tex = F._tex + " (resto)"
    can = caneta(resto, atraso=atraso_caneta, ritmo=CANETA_P / 0.30)
    F._em_caneta = True
    sc.play(*anims, can, run_time=max(rt, can.tot))
    F._em_caneta, F._esc = False, True
    sc.remove(resto)
    sc.add(F)


class PB5(B32):
    ANTES = "MUDAR f SEM MUDAR A INTEGRAL"

    def corpo(self):
        # ── B5-1 · a propriedade da balança (alvo 15) ──
        self.an("B5-1")
        self.secao("DIVIDIR A REGIÃO")
        v0, vl, vp = Vw(330, 820, 230), Vw(330, 840, 230), Vw(330, 800, 230)
        self.grade_on(v0, rt=0)
        leve, pes = metais_liso(v0)
        cord = cordao_ch(v0, 6)
        Bm = balanca(1690, 940, 34, ANG_BAL)
        n1 = TP(r"\Ci{2{,}472}", Bm["_vl"].cx + 34, 1010, 30)       # R5: ≥ 26 px, embaixo de cada prato
        n2 = TP(r"\Ci{4{,}584}", Bm["_vr"].cx + 34, 1010, 30)
        nomes = [k for k in Bm if not k.startswith("_")]
        self.play(FadeIn(leve), FadeIn(pes), FadeIn(cord), *[FadeIn(Bm[k]) for k in nomes], run_time=0.9)
        self.pena(n1, n2, lag=0.2)
        self.gat("a chapa foi dividida")
        leve2 = metais_liso(vl, dy_leve=-.06)[0]
        pes2 = metais_liso(vp, dy_pes=.06)[1]
        leve0, pes0 = leve.copy(), pes.copy()
        cl = cordao_ch(vl, 5, dy=-.06)
        cp = cordao_ch(vp, 5, dy=.06)
        for c in (cl, cp):
            c.corpo.set_stroke(BR)
        cord2 = cord.copy()
        self.add(cord2)
        self.play(Transform(leve, leve2), Transform(pes, pes2), ReplacementTransform(cord, cl), ReplacementTransform(cord2, cp), run_time=1.2)
        self.gat("que vamos chamar de")
        lB = TP(r"B", *vp.px(1.7, .45), 40)
        self.pena(lB)
        self.gat("o metal pesado b")
        lB1 = TP(r"B_1", *vp.px(.35, 1.7), 40)
        self.pena(lB1)
        self.gat("e a parte comum")
        C1 = mista([("L", [("cap", r"B\cap B_1")]), ("t", "TEM CONTEÚDO NULO"), ("m", r"\Rightarrow")], 1120, 260, 32)
        self.pena(C1)
        self.gat("a integral sobre a")
        C2 = L([("ii", r"\iint_{B\cup B_1}"), ("r", r"\f=\iint_B\f+\iint_{B_1}\f")], 1120, 360, 48)
        self.pena(C2)
        self.gat("o u normal é")
        cup = C2[0][C2._ix["ii"][2]]
        self.sublinha(cup, 0.5)
        xu = pxof(cup.get_left())[0]                     # T4: o rótulo de leitura começa embaixo do símbolo, com espaço
        u1 = mista([("m", r"\cup"), ("t", "UNIÃO: OS DOIS JUNTOS", GEO)], xu, 445, 24)
        self.pena(u1)
        self.gat("o u de cabeça")
        cap = C1.p[0][0][C1.p[0]._ix["cap"][1]]
        self.sublinha(cap, 0.5)
        u2 = mista([("m", r"\cap"), ("t", "INTERSEÇÃO: A PARTE EM COMUM", GEO)], xu, 488, 24)
        self.pena(u2)
        self.gat("lê se a integral")
        self.sublinha(C2[0], 2.6)
        self.gat("a solda está na")
        self.play(Transform(cl, cl.cor(MEN, mixh(MEN, BG_, .4))), Transform(cp, cp.cor(MEN, mixh(MEN, BG_, .4))), run_time=0.6)
        self.gat("mas ela tem conteúdo")
        self.sublinha(C1, 2.2)
        self.gat("por isso a balança")
        S = L([("a", r"\Ci{2{,}472}"), ("p", "+"), ("b", r"\Ci{4{,}584}"), ("ap", r"\approx\Ci{7{,}06}\ \text{kg}")], 1120, 600, 44)
        self.play(FadeOut(n1[0]), FadeOut(n2[0]), run_time=0.2)
        self.remove(n1[0], n2[0])
        voa_move(self, S, [(n1.f, S._ix["a"]), (n2.f, S._ix["b"])])     # R5: um só 2,472 e um só 4,584, que vão para a soma
        self.play(*[FadeOut(Bm[k]) for k in nomes], run_time=0.5)
        self.remove(*[Bm[k] for k in nomes])
        self.gat("sem arredondar o total")
        cj = cordao_ch(v0, 6)                            # R5: os pedaços voltam a se encaixar na solda
        cj.corpo.set_stroke(MEN)
        self.play(Transform(leve, leve0), Transform(pes, pes0), ReplacementTransform(cl, cj), FadeOut(cp), lB.animate.shift(UP * 20 / 120),
                  lB1.animate.shift(DOWN * 20 / 120), run_time=1.2)
        self.remove(cp)
        ls = leg("A SOLDA NAS DUAS REGIÕES, COM INTEGRAL 0", 1120, 660, MEN, "left", 26)
        self.pena(ls)
        self.marca("15")

        # ── B5-2 · e se houver sobreposição? (alvo 16 v2) ──
        self.an("B5-2")
        self.limpa(rt=0.5)
        self.grade_off(rt=0)
        self.grade_on(CH, rt=0.3)
        lv, ps = metais_liso(CH)
        bord = borda_ch(CH, GEO, 2)
        cord = cordao_ch(CH, 5)
        sx, sy, lx, ly = eixos_chapa(CH)
        self.play(FadeIn(lv), FadeIn(ps), FadeIn(cord), FadeIn(bord), GrowFromPoint(sx, CH.P(0, 0)), GrowFromPoint(sy, CH.P(0, 0)), run_time=0.8)
        self.pena(lx, ly)
        self.gat("conta essa parte duas")
        c_a = cordao_ch(CH, 5, dy=4 / 240)
        c_b = cordao_ch(CH, 5, dy=-4 / 240)
        for c in (c_a, c_b):
            c.corpo.set_stroke(BR)
        cord_b = cord.copy()
        self.add(cord_b)
        self.play(ReplacementTransform(cord, c_a), ReplacementTransform(cord_b, c_b), run_time=0.8)
        self.gat("a conta correta é")
        PE = [("u", r"\iint_{B\cup B_1}\f"), ("eq", "="), ("a", r"\iint_B\f"), ("p", "+"), ("b", r"\iint_{B_1}\f"), ("m", "-"), ("c", r"\iint_{B\cap B_1}\f")]
        E = L(PE, 1120, 270, 38)                         # D7: todo termo com f
        self.pena(E)
        self.gat("é como contar os")
        l1 = leg("A PARTE EM COMUM ENTROU DUAS VEZES", 1120, 330, GEO, "left", 26)
        self.pena(l1)
        self.gat("faz os dois pedaços")
        fx = faixa_hach(CH)
        self.play(FadeIn(fx), run_time=0.8)
        lf = TPt("FAIXA DE 0,2 m DE ALTURA", *CH.px(2.08, 1.62), 26, AL, "left")
        self.pena(lf)
        self.gat("numa faixa de vinte")
        gx_ = float(g_solda(0.5))                          # C14 (final): cota vertical cruzando a faixa em x = 0,5
        xc_, y0_ = CH.px(0.5, gx_ - 0.1)
        _, y1_ = CH.px(0.5, gx_ + 0.1)
        ym_ = (y0_ + y1_) / 2
        cotaf = VGroup(seta_px((xc_, ym_), (xc_, y1_), GEO, 2, 8), seta_px((xc_, ym_), (xc_, y0_), GEO, 2, 8),
                       lin_px([(xc_ - 7, y1_), (xc_ + 7, y1_)], GEO, 2, z=5), lin_px([(xc_ - 7, y0_), (xc_ + 7, y0_)], GEO, 2, z=5))
        l02 = TP(r"0{,}2\ \text{m}", xc_ - 14, ym_ - 40, 26, "r")
        self.play(GrowFromCenter(cotaf), run_time=0.6)
        self.pena(l02)
        cota2 = VGroup(lin_px([CH.px(0, -.17), CH.px(2, -.17)], GEO, 2, z=4), lin_px([CH.px(0, -.13), CH.px(0, -.21)], GEO, 2, z=4),
                       lin_px([CH.px(2, -.13), CH.px(2, -.21)], GEO, 2, z=4))
        l2m = TP(r"2\ \text{m}", *CH.px(1, -.3), 28)       # o lado da chapa (fonte do 2)
        self.gat("a chapa tem quatro")
        self.play(Create(cota2), run_time=0.5)
        self.pena(l2m)
        self.gat("a soma das áreas")
        # M11 (v2): 0,2 · 2 → 0,4 m²; 4 + 0,4 → 4,4 m²
        FX = mista([("t", "FAIXA:"), ("L", [("a", r"0{,}2"), ("d", r"\cdot"), ("b", "2")])], 1120, 545, 34)
        F0 = FX.p[1]
        lf_txt = lf.f
        self.pena(FX.p[0])
        self.escreve(F0, voos=[(VGroup(*lf_txt[0][7:10]), F0._ix["a"]), (VGroup(*l2m.f[0][:1]), F0._ix["b"])], atraso_caneta=0.3)
        F1 = L([("a", r"0{,}2"), ("d", r"\cdot"), ("b", "2"), ("eq", "="), ("r", r"\Al{0{,}4}\ \text{m}^2")], pxof(F0.get_left())[0], 545, 34 * 1.18)
        gm(self, F0, F1, [("a", "a"), ("d", "d"), ("b", "b"), (["a", "d", "b"], "r")], rt=1.3, copia=True, nota="mapa 11a (M11, B5-2: 0,2·2 = 0,4 m²)")
        self.remove(F0)
        alw = leg("ALTURA × LARGURA", pxof(F1.get_left())[0], 588, GEO, "left", 26)        # C14 (final)
        self.pena(alw)
        Q0 = L([("q", "4"), ("p", "+"), ("r", r"\Al{0{,}4}")], 1120, 642, 40)
        self.escreve(Q0, voos=[(gl(F1, "r")[:3], Q0._ix["r"])], atraso_caneta=0.0)
        Q1 = L([("q", "4"), ("p", "+"), ("r", r"\Al{0{,}4}"), ("eq", "="), ("t", r"\Al{4{,}4}\ \text{m}^2")], 1120, 642, 40)
        gm(self, Q0, Q1, [("q", "q"), ("p", "p"), ("r", "r"), (["q", "p", "r"], "t")], rt=1.3, copia=True, nota="mapa 11b (M11, B5-2: 4 + 0,4 = 4,4 m²)")
        self.remove(Q0)
        n4 = leg("NUMA CHAPA DE 4 m²", 1500, 650, GEO, "left", 26)
        self.pena(n4)
        self.gat("quando a interseção tem")
        # M6 (v2): o lado esquerdo FICA; o último termo acende em menta, vira 0 e sai junto com o −
        SL = mista([("t", "SOLDA:"), ("L", PE)], 1120, 420, 30)
        S0 = SL.p[1]
        self.pena(SL.p[0])
        gm(self, E, S0, [(k, k) for k, _ in PE], rt=1.2, copia=True, nota="mapa 6a (M6, B5-2: a conta na solda)")
        self.play(gl(S0, "c").animate.set_color(MEN), run_time=0.4)
        self.gat("esse desconto vale zero")
        x0 = pxof(S0.get_left())[0]
        S1 = L(PE[:6] + [("z", "0")], x0, 420, 30 * 1.18)
        S1[0][S1._ix["z"][0]].set_color(MEN)
        gm(self, S0, S1, [(k, k) for k, _ in PE[:6]] + [("c", "z")], rt=1.0, nota="mapa 6b (M6, B5-2: o termo vira 0)")
        self.gat("e desaparece com área")
        self.play(gl(S1, "m", "z").animate.set_color(MEN), run_time=0.25)
        S2 = L(PE[:5], x0, 420, 30 * 1.18)
        gm(self, S1, S2, [(k, k) for k, _ in PE[:5]], rt=0.75, nota="mapa 6c (M6, B5-2: −0 sai junto)")
        self.gat("com área positiva precisamos")
        l3 = leg("SOBREPOSIÇÃO COM ÁREA: DESCONTAR", 1120, 712, AL, "left", 26)
        self.pena(l3)
        self.marca("16")

        # ── B5-3 · por que dividir ajuda? (alvo 17): cada miniatura se parte e se remonta no seu gatilho ──
        self.an("B5-3")
        self.limpa(rt=0.5)
        self.grade_off(rt=0)
        self.gat("a massa de uma")
        p1, t1, s1 = cartao(140, 230, 480, 500, "PEÇAS MONTADAS", "SÓ SE TOCAM PELAS FACES")
        d1 = VGroup(ret_px(210, 320, 360, 510, fill=mixh(BG_, CI, .6), z=3), ret_px(362, 380, 482, 510, fill=mixh(BG_, CI, .35), z=3),
                    ret_px(250, 290, 330, 318, fill=mixh(BG_, CI, .8), z=3))
        f1 = lin_px([(361, 380), (361, 510)], BR, 2, z=4)
        self.pena(t1, s1, lag=0.2, rt=1.5, extra=[Create(p1), LaggedStart(*[GrowFromEdge(r, DOWN) for r in d1], Create(f1), lag_ratio=0.25)])   # sync: cartão e título juntos
        self.gat("sai das massas de")
        self.play(d1[0].animate.shift(LEFT * 0.18), d1[1].animate.shift(RIGHT * 0.18), d1[2].animate.shift(UP * 0.15), run_time=0.7)
        self.play(d1[0].animate.shift(RIGHT * 0.18), d1[1].animate.shift(LEFT * 0.18), d1[2].animate.shift(DOWN * 0.15), run_time=0.7)
        self.gat("uma região em formato")
        p2, t2, s2 = cartao(720, 230, 480, 500, "REGIÃO EM L", "DOIS RETÂNGULOS")
        d2 = VGroup(ret_px(820, 300, 950, 600, fill=mixh(BG_, CI, .55), z=3), ret_px(952, 470, 1122, 600, fill=mixh(BG_, CI, .35), z=3))
        f2 = lin_px([(951, 470), (951, 600)], BR, 2, dash=(8, 6), z=4)
        self.play(Create(p2), LaggedStart(*[GrowFromEdge(r, DOWN) for r in d2], Create(f2), lag_ratio=0.3), run_time=1.0)
        self.play(d2[1].animate.shift(RIGHT * 0.2), run_time=0.45)
        self.play(d2[1].animate.shift(LEFT * 0.2), run_time=0.45)
        self.pena(t2, s2, lag=0.2)
        self.gat("uma chapa de materiais")
        p3, t3, s3 = cartao(1300, 230, 480, 500, "DOIS METAIS", "CORTE ONDE ρ MUDA")
        v3 = Vw(1420, 610, 120)
        a3, b3 = metais_liso(v3)
        c3 = cordao_ch(v3, 4)
        self.play(Create(p3), FadeIn(a3), FadeIn(b3), run_time=0.8)
        self.play(deposita(c3, 1.0), run_time=1.0)
        self.play(VGroup(a3).animate.shift(DOWN * 0.15), VGroup(b3).animate.shift(UP * 0.15), run_time=0.6)
        self.play(VGroup(a3).animate.shift(UP * 0.15), VGroup(b3).animate.shift(DOWN * 0.15), run_time=0.6)
        self.pena(t3, s3, lag=0.3)
        self.gat("em vez de uma")
        vv = T("VÁRIAS INTEGRAIS SIMPLES", 960, 850, 40, "center")
        self.pena(vv)
        self.marca("17")
        self.sai_fim()
