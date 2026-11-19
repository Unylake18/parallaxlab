"""yt_0045 · Lote PB4: B4-1 a B4-3 (o redemoinho no círculo; conferindo pela soma; no raio e o dobro da área). C4.1–C4.15, GM3–GM5,
alvos 07 a 09. Tudo 2D: palco vista(480, 560, 120), coluna em 1020."""
from k45 import *  # noqa: F401,F403

COL = 1020
RA = 2.0                                   # raio do círculo no desenho (240 px)
V = Vista2D(480, 560, 120)
Frd = lambda X, Y: (-Y, X)
fc = lambda t: (RA * math.cos(t), RA * math.sin(t))
PTS_CAMPO = [(r * math.cos(k * PI / 4 + PI / 8), r * math.sin(k * PI / 4 + PI / 8)) for r in (1, 2, 3) for k in range(8)]


def poligono(n):
    """n cordas violeta (setas, 4 px, ponta 15) + n pontos brancos (7 px) + os dois raios GEO + o arco do ângulo 2π/n e o rótulo."""
    cordas = VGroup(*[V.seta(fc(2 * PI * (i - 1) / n), fc(2 * PI * i / n), VIO, 4, 15) for i in range(1, n + 1)])
    pts = VGroup(*[V.ponto(fc(2 * PI * i / n), BR, 7) for i in range(n)])
    raios = VGroup(V.linha([(0, 0), fc(0)], GEO, 2), V.linha([(0, 0), fc(2 * PI / n)], GEO, 2))
    arco = V.arco(60, 0, 2 * PI / n, BR, 2)
    return cordas, pts, raios, arco


class PB4(B45):
    ANTES = "A DEFINIÇÃO"

    def corpo(self):
        # ── B4-1 · o redemoinho no círculo (alvo 07, C4.1–C4.5, GM3) ──────────────────────────────────────────
        self.an("B4-1")
        self.titulo("O REDEMOINHO NO CÍRCULO")
        eix, (rx, ry) = eixos2(V, -3.6, 3.7, -3.4, 3.4)
        self.papel_vista(V, rt=0.4, extra=[Create(eix[0]), Create(eix[1])])
        self.pena(rx, ry)

        self.gat("o redemoinho")
        self.degrau("C4.1a", "F(x, y) = (-y, x)")
        cp = campo_grade(V, Frd, meio(-3.5, 3.5), meio(-2.5, 2.5), k=.3, mx=.8, curvas=[arco2(fc, 0, 2 * PI, 240)], folga=.16,
                         evita_px=[(500, 250, 700, 330), (560, 620, 620, 680)])
        sqF, lqF = legq(CAMPO, "F = (−y, x): GIRA EM VOLTA DA ORIGEM", 120, 1020, 28)
        l1 = TC(r"\Fv(\X,\Y)=(-\Y,\ \X)", COL, 190, 48)
        self.play(LaggedStart(*[Create(s) for s in cp], lag_ratio=0.03), FadeIn(sqF), run_time=1.0)
        self.pena(l1, lqF)
        self.col("B4-1", l1)

        self.gat("A curva é o círculo de raio R")
        self.degrau("C4.1b", "gamma(t) = (R cos t, R sen t), 0 <= t <= 2pi")
        circ = curva(V, fc, 0, 2 * PI, HEL, 6)
        sent = sentido(V, fc, PI * .62, HEL)
        rq = fc(-PI / 5)
        raio = V.linha([(0, 0), rq], GEO, 2)
        qR = V.P(RA * .5 * math.cos(-PI / 5), RA * .5 * math.sin(-PI / 5))
        tR = TC("R", qR[0] + 10, qR[1] + 20, 32, "c")
        sqC, lqC = legq(HEL, "CÍRCULO DE RAIO R", 700, 1020, 28)
        l2 = TC(r"\g(\Tt)=(R\cos\Tt,\ R\sen\Tt),\quad 0\le\Tt\le2\pi", COL, 285, 42)
        self.play(Create(circ), run_time=1.4)
        self.play(FadeIn(sent), Create(raio), FadeIn(sqC), run_time=0.4)
        self.pena(tR, lqC, l2)
        self.col("B4-1", l2)

        self.gat("Passo um")
        self.degrau("C4.2", "(1) F(gamma(t)) = (-R sen t, R cos t)")
        n1 = num(1, 1049, 380, 55)
        l3 = TC(r"\Fv(\g(\Tt))=(-R\sen\Tt,\ R\cos\Tt)", 1098, 380, 42)
        self.pena(n1, l3)
        self.col("B4-1", l3)

        self.gat("Passo dois")
        self.degrau("C4.3", "(2) gamma'(t) = (-R sen t, R cos t)")
        n2 = num(2, 1049, 470, 55)
        l4 = TC(r"\gp(\Tt)=(-R\sen\Tt,\ R\cos\Tt)", 1098, 470, 42)
        self.pena(n2, l4)
        self.col("B4-1", l4)

        self.gat("deu exatamente o mesmo vetor")
        t0 = PI / 4
        p = fc(t0)
        T_ = (-math.sin(t0), math.cos(t0))
        o = (.16 * math.cos(t0), .16 * math.sin(t0))
        sF = V.seta(p, (p[0] + .9 * T_[0], p[1] + .9 * T_[1]), CAMPO, 6, 20)
        sG = V.seta((p[0] + o[0], p[1] + o[1]), (p[0] + o[0] + .9 * T_[0], p[1] + o[1] + .9 * T_[1]), VIO, 5, 18)
        pt = V.ponto(p, BR, 8)
        qF = V.P(p[0] + .9 * T_[0], p[1] + .9 * T_[1])
        qG = V.P(p[0] + o[0] + .9 * T_[0], p[1] + o[1] + .9 * T_[1])
        rF = placa_tc(r"\Fv", qF[0] - 30, qF[1] - 14, 32)
        rG = placa_tc(r"\gp", qG[0] + 30, qG[1] - 6, 32)
        self.play(FadeIn(pt), Create(sF), Create(sG), run_time=0.6)
        self.pena(rF, rG)

        self.gat("Passo três")
        self.degrau("C4.4a", "(3) F(gamma(t)) . gamma'(t) = R^2 sen^2 t + R^2 cos^2 t")
        n3 = num(3, 1047, 565, 50)
        l5 = L([("lhs", r"\Fv(\g(\Tt))\cdot\gp(\Tt)"), ("eq", "="), ("a", "R^2"), ("s", r"\sen^2\Tt"), ("pl", "+"), ("b", "R^2"), ("c", r"\cos^2\Tt")],
               1092, 565, 38)
        self.pena(n3, l5)
        self.col("B4-1", l5)
        self.wait(1.2)
        self.degrau("C4.4b", "= R^2 (sen^2 t + cos^2 t) = R^2")
        l6 = L([("eq", "="), ("a", "R^2"), ("po", "("), ("s", r"\sen^2\Tt"), ("pl", "+"), ("c", r"\cos^2\Tt"), ("pc", ")"), ("eq2", "="), ("r", "R^2")],
               COL + 92, 640, 38)
        self.gm(3, l5, l6, [("eq", "eq"), ("a", "a"), ("s", "s"), ("pl", "pl"), ("c", "c")], rt=1.2, copia=True,
                nota="GM3: R^2 sen^2 t + R^2 cos^2 t -> R^2(sen^2 t + cos^2 t) = R^2 (o R^2 sai em evidência)")
        self.wait(0.8)
        self.sub(gl(l6, "s", "pl", "c"), rt=1.6, cor=MEN)          # sen² + cos² acende menta (= 1)
        self.col("B4-1", l6)

        self.gat("Integra de zero a dois pi")
        self.degrau("C4.5", "W = int_0^2pi R^2 dt = R^2[t]_0^2pi = R^2(2pi - 0) = 2piR^2")
        l7 = TC(r"W=\int_0^{2\pi}R^2\,\dTt=R^2\Big[\Tt\Big]_0^{2\pi}=R^2(2\pi-0)=2\pi R^2", COL, 770, 40)
        self.pena(l7)
        m7 = caixa_men(l7, 16)
        self.play(Create(m7), run_time=0.4)
        self.col("B4-1", l7)
        self.calib("07_B4-1", V, axes=eix, curva_pts=[("(R, 0)", circ, (RA, 0)), ("(0, R)", circ, (0, RA))],
                   setas=calib_setas(cp, (0, len(cp) // 2, len(cp) - 1)))
        self.marca("07_B4-1")

        # ── B4-2 · conferindo pela soma, na mão (alvo 08, C4.6–C4.11, GM4, GM5) ────────────────────────────────
        self.an("B4-2")
        self.titulo("CONFERINDO PELA SOMA, NA MÃO", rt=0.3)
        circG = curva(V, fc, 0, 2 * PI, GEO, 2.5)
        self.sobe_sai(l1, l2, n1, l3, n2, l4, n3, l5, l6, l7, m7)
        self.play(FadeOut(cp), FadeOut(sF), FadeOut(sG), FadeOut(pt), FadeOut(rF), FadeOut(rG), FadeOut(sent), FadeOut(raio), FadeOut(tR),
                  FadeOut(sqF), FadeOut(lqF), FadeOut(sqC), FadeOut(lqC), ReplacementTransform(circ, circG), run_time=0.5)
        self.remove(cp, sF, sG, pt, rF, rG, sent, raio, tR, sqF, lqF, sqC, lqC)

        self.gat("Divide a volta em n pedaços iguais")
        self.degrau("C4.6", "F(gamma(t_i)) . Dgamma_i = (-R sen t_i)(R cos t_i - R cos t_{i-1}) + (R cos t_i)(R sen t_i - R sen t_{i-1})")
        cord, pts, rai, arc = poligono(8)
        q0 = V.P(0, 0)
        tang = placa_tc(r"\tfrac{2\pi}{n}", q0[0] + 88, q0[1] - 30, 30)
        sqN, lqN = legq(VIO, "n = 8 PEDAÇOS IGUAIS", 120, 1020, 28)
        self.play(LaggedStart(*[Create(c) for c in cord], lag_ratio=0.08), FadeIn(pts), Create(rai), Create(arc), FadeIn(sqN), run_time=1.2)
        self.pena(tang, lqN)
        m1a = TC(r"\Fv(\g(\Tt_i))\cdot\Dg_i=(-R\sen\Tt_i)(R\cos\Tt_i-R\cos\Tt_{i-1})", COL - 40, 185, 34)
        m1b = TC(r"+(R\cos\Tt_i)(R\sen\Tt_i-R\sen\Tt_{i-1})", COL + 160, 250, 34)
        self.pena(m1a)
        self.pena(m1b)
        self.col("B4-2", m1a, m1b)

        self.gat("dois termos aparecem com sinais contrários")
        self.degrau("C4.7", "= R^2(sen t_i cos t_{i-1} - cos t_i sen t_{i-1}) (os termos -R^2 sen t_i cos t_i e +R^2 cos t_i sen t_i se cancelam)")
        # abrindo os produtos (estado de passagem do GM4, na linha da C4.7; começa sob a 1ª linha para caber na margem)
        ab = L([("eq", "="), ("r1", "R^2"), ("po", r"\big("), ("x1", r"-\sen\Tt_i\cos\Tt_i"), ("p1", "+"), ("s", r"\sen"), ("ti", r"\Tt_i"), ("cj", r"\cos\Tt_{i-1}"),
                ("x2", r"+\cos\Tt_i\sen\Tt_i"), ("mn", "-"), ("cs", r"\cos\Tt_i"), ("sn2", r"\sen"), ("tj", r"\Tt_{i-1}"), ("pc", r"\big)")], COL - 66, 330, 32)
        self.pena(ab)
        self.play(*[g_.animate.set_color(AL) for g_ in (gl(ab, "x1"), gl(ab, "x2"))], run_time=0.4)
        self.wait(0.6)
        m2 = L([("eq", "="), ("r", "R^2"), ("po", "("), ("s", r"\sen"), ("ti", r"\Tt_i"), ("cj", r"\cos\Tt_{i-1}"), ("mn", "-"), ("cs", r"\cos\Tt_i"),
                ("sn2", r"\sen"), ("tj", r"\Tt_{i-1}"), ("pc", ")")], COL + 160, 330, 36)
        self.gm(4, ab, m2, [("eq", "eq"), ("r1", "r"), ("po", "po"), ("s", "s"), ("ti", "ti"), ("cj", "cj"), ("mn", "mn"), ("cs", "cs"), ("sn2", "sn2"), ("tj", "tj"),
                                ("pc", "pc")], rt=1.2,
                nota="GM4: -R^2 sen t_i cos t_i e +R^2 cos t_i sen t_i acendem (ALERTA) e saem juntos; o R^2 sai em evidência")
        self.col("B4-2", m2)

        self.gat("a fórmula do seno da diferença")
        self.degrau("C4.8", "= R^2 sen(t_i - t_{i-1}) = R^2 sen(2pi/n)")
        m3 = L([("eq", "="), ("r", "R^2"), ("s", r"\sen"), ("po", "("), ("ti", r"\Tt_i"), ("mn", "-"), ("tj", r"\Tt_{i-1}"), ("pc", ")"),
                ("eq2", "="), ("r2", "R^2"), ("sf", r"\sen\tfrac{2\pi}{n}")], COL + 160, 415, 40)
        self.gm(5, m2, m3, [("eq", "eq"), ("r", "r"), ("s", "s"), ("po", "po"), ("ti", "ti"), ("mn", "mn"), ("tj", "tj"), ("pc", "pc")], rt=1.2,
                copia=True, nota="GM5: sen t_i cos t_{i-1} - cos t_i sen t_{i-1} -> sen(t_i - t_{i-1}) -> sen(2pi/n)")
        self.col("B4-2", m3)

        self.gat("a soma inteira é")
        self.degrau("C4.9", "Sum_i = n R^2 sen(2pi/n)")
        m4 = TC(r"\sum_i=n\,R^2\sen\tfrac{2\pi}{n}", COL, 520, 46)
        self.pena(m4)
        self.col("B4-2", m4)

        tab = [TC(r"n=4:\ 4R^2", COL, 625, 36), TC(r"n=8:\ \approx5{,}66R^2", 1280, 625, 36), TC(r"n=16:\ \approx6{,}12R^2", 1590, 625, 36)]
        atual = (cord, pts, rai, arc)
        for k, (g, n) in enumerate((("Com quatro pedaços", 4), ("Com oito", 8), ("Com dezesseis", 16))):
            self.gat(g)
            self.degrau(f"C4.10{'abc'[k]}", f"n = {n}: n R^2 sen(2pi/n)")
            novo = poligono(n)
            sqN2, lqN2 = legq(VIO, f"n = {n} PEDAÇOS IGUAIS", 120, 1020, 28)
            pronto(lqN2)
            self.remove(*atual, lqN)                 # corte limpo (handoff: troca de n sem animação)
            self.add(*novo, lqN2)
            atual, lqN = novo, lqN2
            self.pena(tab[k])
        self.col("B4-2", VGroup(*tab))              # a tabela é uma linha

        self.gat("o limite fundamental disfarçado")
        self.degrau("C4.11", "n -> inf: n sen(2pi/n) -> 2pi => 2piR^2 ~ 6,28R^2")
        m6 = TC(r"n\to\infty:\ \ n\sen\tfrac{2\pi}{n}\to2\pi\ \Rightarrow\ 2\pi R^2\approx6{,}28R^2", COL, 735, 40)
        self.pena(m6)
        ck = check_px(pxof(m6.get_right())[0] + 30, 735, MEN, 1.1)
        self.play(Create(ck), run_time=0.4)
        self.col("B4-2", m6)
        self.marca("08_B4-2")

        # ── B4-3 · no raio: força de lado; e o dobro da área (alvo 09, C4.12–C4.15) ────────────────────────────
        self.an("B4-3")
        self.titulo("NO RAIO: A FORÇA DE LADO", rt=0.3)
        self.sobe_sai(m1a, m1b, m2, m3, m4, *tab, m6, ck)
        cp2 = campo_grade(V, Frd, meio(-3.5, 3.5), meio(-2.5, 2.5), k=.3, mx=.8, curvas=[arco2(fc, 0, 2 * PI, 240)], folga=.16,
                          evita_px=[(280, 580, 440, 650), (470, 480, 730, 580)])
        self.play(FadeOut(VGroup(*atual)), FadeOut(tang), FadeOut(sqN), FadeOut(lqN),
                  LaggedStart(*[Create(s) for s in cp2], lag_ratio=0.03), run_time=1.0)
        self.remove(*atual, tang, sqN, lqN)

        self.gat("a conta anda pelo raio")
        self.degrau("C4.12", "gamma(t) = (t, 0), 0 <= t <= R")
        seg = V.linha([(0, 0), (RA, 0)], HEL, 7)
        sseg = V.seta((1.55, 0), (1.82, 0), HEL, 7, 24)
        sqS, lqS = legq(HEL, "SEGMENTO DA ORIGEM ATÉ (R, 0)", 120, 1020, 28)
        r1 = TC(r"\g(\Tt)=(\Tt,\ 0),\quad 0\le\Tt\le R", COL, 190, 46)
        self.play(Create(seg), run_time=0.8)
        self.play(FadeIn(sseg), FadeIn(sqS), run_time=0.3)
        self.pena(lqS, r1)
        self.col("B4-3", r1)

        self.gat("a força vira zero, t")
        self.degrau("C4.13", "F(gamma(t)) = (0, t), gamma'(t) = (1, 0)")
        sv = VGroup(*[seta_campo(V, (t, 0), (0, t), .32, 1.0, CAMPO, 5, 16, z=7) for t in (.5, 1, 1.5)])
        sqL, lqL = legq(CAMPO, "F SEMPRE DE LADO", 680, 1020, 28)
        r2 = TC(r"\Fv(\g(\Tt))=(0,\ \Tt),\qquad \gp(\Tt)=(1,\ 0)", COL, 290, 44)
        self.play(LaggedStart(*[Create(s) for s in sv], lag_ratio=0.15), FadeIn(sqL), run_time=0.7)
        self.pena(lqL, r2)
        self.col("B4-3", r2)

        self.gat("Produto escalar: zero")
        self.degrau("C4.14", "F(gamma(t)) . gamma'(t) = 0.1 + t.0 = 0 => W = int_0^R 0 dt = 0")
        r3 = TC(r"\Fv(\g(\Tt))\cdot\gp(\Tt)=0\cdot1+\Tt\cdot0=0\ \Rightarrow\ W=\int_0^R0\,\dTt=0", COL, 395, 36)
        self.pena(r3)
        m_r3 = caixa_men(r3, 14)
        self.play(Create(m_r3), run_time=0.4)
        self.col("B4-3", r3)

        self.gat("a integral de linha depende do caminho")
        sm_, st_ = selo("MESMO CAMPO, OUTRO CAMINHO, OUTRO TRABALHO", COL, 520, GEO, 30)
        self.pena(st_, extra=[Create(sm_)])
        self.col("B4-3", st_)

        self.gat("duas vezes a área do disco")
        self.degrau("C4.15", "NA VOLTA: 2piR^2 = 2 . piR^2 = 2 x AREA DO DISCO")
        cL = curva(V, fc, 0, 2 * PI, LI, 5)
        qA = V.P(-1.6, -.45)
        fundoA = ret_px(qA[0] - 10, qA[1] - 26, qA[0] + 138, qA[1] + 24, fill="#16123A", fop=1.0, z=8)
        tA = mixl([("t", "ÁREA", LI), ("m", r"\Lim{\pi R^2}")], qA[0], qA[1], 32)
        for _p in tA.p:
            _p._com_placa = True                    # §5.2: placa opaca atrás do rótulo, como no alvo 09 (a seta sob ela fica escondida)
        r5 = mixl([("t", "NA VOLTA:", BR), ("m", r"2\pi R^2=2\cdot\pi R^2"), ("t", "= 2 × ÁREA DO DISCO", LI)], COL, 640, 42)
        self.play(Create(cL), FadeIn(fundoA), run_time=1.0)
        self.pena(*tA.p)
        self.pena(*r5.p)
        self.col("B4-3", r5)
        self.calib("09_B4-3", V, axes=eix, curva_pts=[("(R, 0)", cL, (RA, 0)), ("(0, R)", cL, (0, RA))],
                   setas=calib_setas(cp2, (0, len(cp2) // 2, len(cp2) - 1)))
        self.marca("09_B4-3")
        self.sai_fim(rt=0.35)
