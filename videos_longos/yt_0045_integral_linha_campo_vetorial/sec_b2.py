"""yt_0045 · Lote PB2: B2-1 (a partição), B2-2 (da corda à velocidade: soma de Riemann) e B3 (a definição). C2.1–C2.11, GM1–GM2, alvos 04–06.
B2-1 e B2-2 na mesma classe: a linha C2.4 do B2-1 é o MESMO objeto que o GM1 transforma na C2.6 (handoff v1.1 §7)."""
from k45 import *  # noqa: F401,F403

COL = 1020
V = Vista2D(140, 890, 120)
fB2 = lambda s: (0.5 + 5.8 * s, 1.2 + 2.6 * s + 0.9 * math.sin(2 * PI * s))
FB2 = lambda X, Y: (0.9, 0.6 - 0.25 * X)
TS = [i / 6 for i in range(7)]
V3 = Vista2D(300, 600, 100)
f3 = lambda s: (-2.2 + 4.4 * s, -1.2 + 1.4 * s + 0.9 * math.sin(PI * 1.4 * s))


class PB2(B45):
    ANTES = "FORÇA CONSTANTE, CAMINHO RETO"

    def corpo(self):
        # ── B2-1 · caminho curvo, força que muda: a partição (alvo 04, C2.1–C2.4) ─────────────────────────────
        self.an("B2-1")
        self.titulo("CAMINHO CURVO, FORÇA QUE MUDA")
        eix, (rx, ry) = eixos2(V, -.3, 6.6, -.3, 5.6)
        kwB2 = dict(k=.5, mx=.6, curvas=[arco2(fB2, 0, 1, 240)], folga=.2)
        EV21 = [(150, 760, 240, 820), (860, 365, 940, 415), (660, 530, 820, 590), (550, 640, 660, 700)]
        EV22 = [(150, 760, 240, 820), (860, 365, 940, 415), (510, 140, 940, 375)]
        nA = nos_campo(V, FB2, meio(.5, 6.5), meio(.5, 5.5), evita_px=EV21, **kwB2)
        nB = nos_campo(V, FB2, meio(.5, 6.5), meio(.5, 5.5), evita_px=EV22, **kwB2)
        cp = seta_nos(V, nA)                                   # as setas do alvo 04 (nós fora das caixas dos rótulos do B2-1)
        só_a = [m for m, n in zip(cp, nA) if n[0] not in {q[0] for q in nB}]
        cpB = seta_nos(V, [n for n in nB if n[0] not in {q[0] for q in nA}])   # as que só existem no alvo 05
        self.papel_vista(V, rt=0.4, extra=[Create(eix[0]), Create(eix[1])])
        self.pena(rx, ry)
        self.play(LaggedStart(*[Create(s) for s in cp], lag_ratio=0.04), run_time=1.0)

        self.gat("uma curva gama")
        self.degrau("C2.0", "gamma: [a, b] -> Omega, gamma(t) = posição no instante t")
        cv = curva(V, fB2, 0, 1, HEL, 6)
        sv = sentido(V, fB2, .93)
        qa, qb = V.P(*fB2(0)), V.P(*fB2(1))
        ga = placa_tc(r"\g(a)", qa[0] - 6, qa[1] + 42, 32)
        gb = placa_tc(r"\g(b)", qb[0] + 4, qb[1] - 42, 32)
        rb, rtq, rrot = regua(200, 890, 986, [(200 + 690 * s, None) for s in (0, 1)])
        l1 = mixl([("m", r"\g:[a,b]\to\Om,"), ("m", r"\g(\Tt)"), ("t", "= POSIÇÃO NO INSTANTE", BR), ("m", r"\Tt")], COL, 195, 40)
        self.play(Create(cv), Create(rb), run_time=1.2)
        self.play(FadeIn(sv), run_time=0.2)
        self.pena(ga, gb)
        self.pena(*l1.p)
        self.col("B2-1", l1)

        self.gat("corta o intervalo de tempo em pedaços")
        self.degrau("C2.1", "a = t_0 < t_1 < ... < t_n = b")
        marks = [(200 + 690 * s, r"a=\Tt_0" if i == 0 else (r"\Tt_6=b" if i == 6 else r"\Tt_%d" % i)) for i, s in enumerate(TS)]
        _, tq, rots = regua(200, 890, 986, marks)
        pts = [V.ponto(fB2(s), BR, 7) for s in TS]
        lig = [lin_px([(X, 976), V.P(*fB2(s))], GEO, 1.5, alpha=1.0, z=3) for (X, _), s in zip(marks, TS)]
        self.play(LaggedStart(*[AnimationGroup(Create(a), Create(b), FadeIn(c)) for a, b, c in zip(tq, lig, pts)], lag_ratio=0.25), run_time=1.6)
        self.play(*[FadeOut(x) for x in lig], run_time=0.4)
        self.remove(*lig)
        self.remove(*rtq)
        self.pena(*rots)
        l2 = TC(r"a=\Tt_0<\Tt_1<\cdots<\Tt_n=b", COL, 290, 44)
        self.pena(l2)
        self.col("B2-1", l2)

        self.gat("troca o arco pela corda")
        cordas = [V.seta(fB2(TS[i - 1]), fB2(TS[i]), VIO, 4, 15) for i in range(1, 7)]
        self.play(LaggedStart(*[Create(c) for c in cordas], lag_ratio=0.15), run_time=1.2)

        self.gat("delta gama i")
        self.degrau("C2.2", "Dgamma_i = gamma(t_i) - gamma(t_{i-1})")
        q6 = V.P(*fB2(.6))
        tD = placa_tc(r"\Dg_4", q6[0] - 50, q6[1] + 40, 32)
        l3 = TC(r"\Dg_i=\g(\Tt_i)-\g(\Tt_{i-1})", COL, 385, 46)
        self.pena(tD, l3)
        self.col("B2-1", l3)

        self.gat("F de gama de t i")
        p4 = fB2(TS[4])
        sF4 = seta_campo(V, p4, FB2(*p4), 1.0, 1.2, CAMPO, 6, 20, z=7)
        q4 = V.P(*p4)
        tF4 = placa_tc(r"\Fv(\g(\Tt_4))", q4[0] + 20, q4[1] - 84, 32, "l")
        self.play(Create(sF4), run_time=0.5)
        self.pena(tF4)

        self.gat("O trabalhinho desse pedaço")
        self.degrau("C2.3", "TRABALHINHO ~ F(gamma(t_i)) . Dgamma_i")
        l4 = mixl([("t", "TRABALHINHO", BR), ("m", r"\approx\Fv(\g(\Tt_i))\cdot\Dg_i")], COL, 485, 44)
        self.pena(*l4.p)
        self.col("B2-1", l4)

        self.gat("Somando todos")
        self.degrau("C2.4", "W ~ Sum_i F(gamma(t_i)) . Dgamma_i")
        c24 = L([("w", r"W\approx\sum_i"), ("f", r"\Fv(\g(\Tt_i))"), ("dot", r"\cdot"), ("dg", r"\Dg_i")], COL, 600, 50)
        self.pena(c24)
        self.col("B2-1", c24)
        self.calib("04_B2-1", V, axes=eix, curva_pts=[("gamma(a)", cv, fB2(0)), ("gamma(b)", cv, fB2(1))],
                   setas=calib_setas(cp, (0, len(cp) // 2, len(cp) - 1)))
        self.marca("04_B2-1")

        # ── B2-2 · da corda à velocidade (alvo 05, C2.5–C2.10, GM1, GM2) ─────────────────────────────────────
        self.an("B2-2")
        self.titulo("APARECE UMA SOMA DE RIEMANN", rt=0.3)
        self.sobe_sai(l1, l2, l3, l4, extra=[FadeOut(sF4), FadeOut(tF4), FadeOut(tD)])
        self.remove(sF4, tF4, tD)
        self.col_zera("B2-1")
        self.play(c24.animate.shift(UP * (600 - 295) / 120), *[FadeOut(m) for m in só_a], *[FadeIn(m) for m in cpB], run_time=0.6)      # a C2.4 sobe (o mesmo objeto)
        self.remove(*só_a)

        self.gat("velocidade vezes tempo")
        self.degrau("C2.5", "Dgamma_i ~ gamma'(t_i) Dt_i  (VELOCIDADE x TEMPO)")
        pn = painel2d44(520, 150, 410, 215)
        pn[0].set_z_index(7)                         # a lupa é opaca: fica por cima das setas do campo (z 5) e da curva
        pn[1].set_z_index(7.5)
        c = (610, 320)
        ch = (250, -120)
        sc = seta_px(c, (c[0] + ch[0], c[1] + ch[1]), VIO, 6, 22, z=8)
        st = seta_px((c[0], c[1] + 10), (c[0] + ch[0] * 1.04 + 6, c[1] + ch[1] * 1.04 + 14), VIO, 3, 18, z=8)
        st = VGroup(DashedVMobject(st[0], num_dashes=16, dashed_ratio=10 / 17).set_stroke(VIO, W(3)), st[1])
        pc = ponto_px(*c, BR, 8, z=9)
        lD = TC(r"\Dg_4", c[0] + 120, c[1] - 110, 30, "c")
        lG = TC(r"\gp(\Tt_4)\DTt_4", c[0] + 190, c[1] + 24, 28, "l")
        lQ = leg("QUASE IGUAIS", 540, 190, GEO, "left", 26)
        for _m in (lD, lG, lQ):
            _m._com_placa = True                     # dentro da lupa opaca: a seta do campo sob ela não aparece
        self.dentro(pn._painel, lD, lG, lQ)
        self.pena(lQ, extra=[FadeIn(pn), Create(sc), Create(st), FadeIn(pc)])          # a lupa aparece com a 1ª linha dela
        self.pena(lD, lG)
        c25 = mixl([("L", [("dg", r"\Dg_i"), ("ap", r"\approx"), ("v", r"\gp(\Tt_i)\,\DTt_i")]), ("t", "VELOCIDADE × TEMPO", GEO)], COL, 190, 46)
        self.pena(*c25.p)
        self.col("B2-2", c25, c24)

        self.gat("Troca isso na soma")
        self.degrau("C2.6", "W ~ Sum_i F(gamma(t_i)) . gamma'(t_i) Dt_i")
        self.sub(gl(c24, "dg"), rt=0.6, cor=VIO)
        c26 = L([("w", r"W\approx\sum_i"), ("f", r"\Fv(\g(\Tt_i))"), ("dot", r"\cdot"), ("gp", r"\gp(\Tt_i)"), ("dt", r"\,\DTt_i")], COL, 295, 44)
        self.gm(1, c24, c26, [("w", "w"), ("f", "f"), ("dot", "dot"), ("dg", ["gp", "dt"])], rt=1.2,
                nota="GM1: o Delta gamma_i da C2.4 (mesmo objeto do B2-1) vira gamma'(t_i) Delta t_i")
        self.col("B2-2", c26)

        self.gat("Chama esse número de g de t")
        self.degrau("C2.7", "g(t) = F(gamma(t)) . gamma'(t)  (UM NÚMERO PARA CADA t)")
        c27 = mixl([("m", r"g(\Tt)=\Fv(\g(\Tt))\cdot\gp(\Tt)"), ("t", "UM NÚMERO PARA CADA", GEO), ("m", r"\Tt")], COL, 400, 40)
        self.pena(*c27.p)
        self.col("B2-2", c27)

        self.gat("uma soma de Riemann comum")
        self.degrau("C2.8", "W ~ Sum_i g(t_i) Dt_i  (SOMA DE RIEMANN DE g EM [a, b])")
        c28 = mixl([("L", [("w", r"W\approx\sum_i"), ("g", r"g(\Tt_i)"), ("dt", r"\,\DTt_i")]), ("t", "SOMA DE RIEMANN DE g EM [a, b]", GEO)], COL, 500, 40)
        self.gm(2, c26, c28.p[0], [("w", "w"), (["f", "dot", "gp"], "g"), ("dt", "dt")], rt=1.2, copia=True,
                nota="GM2: F(gamma(t_i)) . gamma'(t_i) se recolhe no g(t_i)")
        self.pena(c28.p[1])
        self.col("B2-2", c28)

        self.gat("Quando o maior pedaço de tempo vai a zero")
        self.degrau("C2.9", "max Dt_i -> 0: W = int_a^b F(gamma(t)) . gamma'(t) dt")
        c29 = TC(r"\max\DTt_i\to0:\quad W=\int_a^b \Fv(\g(\Tt))\cdot\gp(\Tt)\,\dTt", COL, 630, 44)
        self.pena(c29)
        self.col("B2-2", c29)

        self.gat("E o erro da troca")
        self.degrau("C2.10", "chip: gamma DE CLASSE C^1: O ERRO DA TROCA SOME NO LIMITE")
        cgE, cfE, cmE = chipm([("m", r"\g"), ("t", "DE CLASSE", GEO), ("m", r"C^1:"), ("t", "O ERRO DA TROCA SOME NO LIMITE", GEO)], COL, 770, 30, GEO)
        self.chip_pena(cgE, cfE, cmE)
        self.col("B2-2", cgE, chips=1)
        self.calib("05_B2-2", V, axes=eix, curva_pts=[("gamma(a)", cv, fB2(0)), ("gamma(b)", cv, fB2(1))],
                   setas=calib_setas(cp, (0, len(cp) // 2, len(cp) - 1)))
        self.marca("05_B2-2")

        # ── B3 · a definição (alvo 06, C2.11) ─────────────────────────────────────────────────────────────────
        self.an("B3")
        self.titulo("A DEFINIÇÃO", rt=0.3)
        self.sobe_sai(c25, c26, c27, c28, cgE, c29)
        self.limpa(rt=0.4)
        self.papel_vista(V3, rt=0.3)

        self.gat("F é um campo vetorial contínuo")
        self.degrau("C2.11a", "F contínuo no aberto Omega")
        cv3 = curva(V3, f3, 0, 1, HEL, 5)
        sv3 = sentido(V3, f3, .9)
        s0 = .55
        p = f3(s0)
        q_ = f3(s0 + .001)
        L_ = math.hypot(q_[0] - p[0], q_[1] - p[1])
        Tg = ((q_[0] - p[0]) / L_, (q_[1] - p[1]) / L_)
        Fv = (1.2 * Tg[0] - 0.9 * Tg[1], 1.2 * Tg[1] + 0.9 * Tg[0])
        sG = V3.seta(p, (p[0] + 1.3 * Tg[0], p[1] + 1.3 * Tg[1]), VIO, 5, 18)
        sF = V3.seta(p, (p[0] + Fv[0], p[1] + Fv[1]), CAMPO, 5, 18)
        pt = V3.ponto(p, BR, 9)
        a0, a1 = math.atan2(Tg[1], Tg[0]), math.atan2(Fv[1], Fv[0])
        qp = V3.P(*p)
        arc = lin_px([(qp[0] + 48 * math.cos(a0 + (a1 - a0) * k / 30), qp[1] - 48 * math.sin(a0 + (a1 - a0) * k / 30)) for k in range(31)], BR, 2, z=6)
        qF = V3.P(p[0] + Fv[0], p[1] + Fv[1])
        qG = V3.P(p[0] + 1.3 * Tg[0], p[1] + 1.3 * Tg[1])
        rF = placa_tc(r"\Fv", qF[0] - 8, qF[1] - 28, 34)
        rG = placa_tc(r"\gp", qG[0] + 44, qG[1] - 8, 34)
        ct = cartao(640, 150, 1220, 880)
        tD = leg("DEFINIÇÃO", 680, 210, GEO, "left", 30)
        d1 = mixl([("m", r"\Fv"), ("t", "CONTÍNUO NO ABERTO", BR), ("m", r"\Om\subset\mathbb{R}^3")], 680, 280, 40)
        self.dentro(ct._painel, tD, *d1.p)
        self.play(Create(cv3), run_time=0.9)
        self.play(FadeIn(sv3), FadeIn(pt), Create(sG), Create(sF), Create(arc), run_time=0.5)
        self.pena(rF, rG, tD, extra=[FadeIn(ct)])           # o cartão nasce com a 1ª linha dele
        self.pena(*d1.p)
        self.col("B3", d1)

        self.gat("gama é uma curva de classe C um")
        self.degrau("C2.11b", "gamma: [a, b] -> Omega de classe C^1")
        d2 = mixl([("m", r"\g:[a,b]\to\Om"), ("t", "DE CLASSE", BR), ("m", r"C^1")], 680, 360, 40)
        self.dentro(ct._painel, *d2.p)
        self.pena(*d2.p)
        self.col("B3", d2)

        self.gat("A integral de linha de F sobre gama")
        self.degrau("C2.11", "int_gamma F . dgamma = int_a^b F(gamma(t)) . gamma'(t) dt")
        d3 = TC(r"\int_{\g}\Fv\cdot\dg=\int_a^b \Fv(\g(\Tt))\cdot\gp(\Tt)\,\dTt", 700, 490, 52)
        self.dentro(ct._painel, d3)
        self.pena(d3)
        m3 = caixa_men(d3, 18)
        self.play(Create(m3), run_time=0.4)
        self.col("B3", d3)

        self.gat("O d gama do lado esquerdo")
        self.degrau("C2.11c", "dgamma = gamma'(t) dt")
        d4 = TC(r"\dg=\gp(\Tt)\,\dTt", 700, 620, 44)
        self.dentro(ct._painel, d4)
        self.pena(d4)
        self.col("B3", d4)

        self.gat("Na prática, a receita")
        n1 = num(1, 722, 730, 46)
        r1 = TC(r"\Fv(\g(\Tt))", 754, 730, 38)
        self.pena(n1, r1)
        self.gat("Dois: deriva a curva")
        x2 = pxof(r1.get_right())[0] + 40
        n2 = num(2, x2 + 22, 730, 46)
        r2 = TC(r"\gp(\Tt)", x2 + 54, 730, 38)
        self.pena(n2, r2)
        self.gat("Três: faz o produto escalar")
        x3 = pxof(r2.get_right())[0] + 40
        n3 = num(3, x3 + 22, 730, 46)
        r3 = mixl([("t", "PRODUTO ESCALAR E INTEGRA EM", BR), ("m", r"\Tt")], x3 + 54, 730, 38)
        self.dentro(ct._painel, r1, r2, *r3.p)
        self.pena(n3, *r3.p)
        self.col("B3", VGroup(r1, r2, r3))

        self.gat("o sinal do produto escalar")
        cgS, cfS, cmS = chipm([("m", r"\Fv(\g(\Tt))\cdot\gp(\Tt):"), ("m", ">0"), ("t", "AJUDA ·", LI), ("m", "=0"), ("t", "DE LADO ·", GEO), ("m", "<0"),
                               ("t", "ATRAPALHA", AL)], 700, 850, 32, GEO)
        self.dentro(ct._painel, cfS)
        self.chip_pena(cgS, cfS, cmS)
        self.col("B3", cgS, chips=1)
        self.marca("06_B3")
        self.sai_fim(rt=0.35)
