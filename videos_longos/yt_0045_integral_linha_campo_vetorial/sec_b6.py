"""yt_0045 · Lote PB6: B6-1 (outra notação: P dx + Q dy) e B6-2 (a elipse e o dobro da área). C6.1–C7.7, GM8–GM9, alvos 12–13.
B6-1 sem palco (faixa de álgebra em x = 120, mini-desenho no painel); B6-2 palco vista(480, 560, 150) (papel passo 0,4 = 60 px)."""
from k45 import *  # noqa: F401,F403

COL = 1020
V = Vista2D(480, 560, 150)
fe = lambda t: (2 * math.cos(t), math.sin(t))
Frd = lambda X, Y: (-Y, X)


class PB6(B45):
    ANTES = "POR QUE DEU ZERO"

    def corpo(self):
        # ── B6-1 · outra notação (alvo 12, C6.1–C6.6, GM8) ───────────────────────────────────────────────────
        self.an("B6-1")
        self.titulo("OUTRA NOTAÇÃO", rt=0.2)

        self.gat("Agora a outra notação")
        pn = painel2d44(1420, 150, 440, 300)
        ox, oy = 1480, 410
        fm = lambda s: (ox + 40 + 320 * s, oy - 40 - 170 * s - 50 * math.sin(PI * s))
        cm_ = lin_px([fm(i / 60) for i in range(61)], HEL, 5, z=6)
        ax_ = seta_px((ox, oy), (ox + 400, oy), E1, 3, 14, z=6)
        ay_ = seta_px((ox, oy), (ox, oy - 240), E2, 3, 14, z=6)
        q = fm(.55)
        pq = ponto_px(*q, BR, 8, z=9)
        g1 = lin_px([q, (q[0], oy)], GEO, 2, dash=(6, 6), z=5)
        g2 = lin_px([q, (ox, q[1])], GEO, 2, dash=(6, 6), z=5)
        tx = TC(r"\X(\Tt)", q[0], oy + 20, 26, "c")
        ty = TC(r"\Y(\Tt)", ox - 12, q[1], 26, "r")
        d1a = TC(r"\Fv=(P,\ Q),", 120, 215, 48)
        d1b = TC(r"\g(\Tt)=(\X(\Tt),\ \Y(\Tt))", 120, 215, 48)
        d1b.shift(RIGHT * ((pxof(d1a.get_right())[0] + 105 - pxof(d1b.get_left())[0]) / 120))
        self.dentro(pn._painel, tx, ty)
        self.pena(tx, ty, extra=[FadeIn(pn), Create(ax_), Create(ay_), Create(cm_), FadeIn(pq), Create(g1), Create(g2)])   # o painel nasce com o 1º rótulo dele
        self.gat("F igual a P, Q")
        self.degrau("C6.1", "F = (P, Q), gamma(t) = (x(t), y(t))")
        self.pena(d1a)
        self.gat("E a curva também pelas componentes")
        self.pena(d1b)
        self.col("B6-1", VGroup(d1a, d1b))

        self.gat("abrindo coordenada por coordenada")
        self.degrau("C6.2", "F(gamma(t)) . gamma'(t) dt = P(x(t), y(t)) x'(t) dt + Q(x(t), y(t)) y'(t) dt")
        d2 = L([("lhs", r"\Fv(\g(\Tt))\cdot\gp(\Tt)\,\dTt"), ("eq", "="), ("P", r"P(\X(\Tt),\Y(\Tt))\,"), ("xd", r"\X'(\Tt)\,\dTt"), ("pl", "+"),
                ("Q", r"Q(\X(\Tt),\Y(\Tt))\,"), ("yd", r"\Y'(\Tt)\,\dTt")], 120, 330, 40)
        self.pena(d2)
        self.col("B6-1", d2)

        self.gat("d x é x linha de t, d t")
        self.degrau("C6.3", "dx = x'(t) dt, dy = y'(t) dt  (A MESMA DA SUBSTITUIÇÃO)")
        d3 = mixl([("m", r"\dX=\X'(\Tt)\,\dTt,\qquad \dY=\Y'(\Tt)\,\dTt"), ("g", 34), ("t", "A MESMA DA SUBSTITUIÇÃO", GEO)], 120, 445, 44)
        self.pena(*d3.p)
        self.col("B6-1", d3)

        self.gat("integral sobre gama de P d x mais Q d y")
        self.degrau("C6.4", "int_gamma F . dgamma = int_gamma P dx + Q dy")
        d4 = L([("l", r"\int_{\g}\Fv\cdot\dg"), ("eq", "="), ("i", r"\int_{\g}"), ("P", r"P\,"), ("dx", r"\dX"), ("pl", "+"), ("Q", r"Q\,"), ("dy", r"\dY")],
               120, 575, 54)
        self.gm(8, d2, d4, [("P", "P"), ("xd", "dx"), ("pl", "pl"), ("Q", "Q"), ("yd", "dy")], rt=1.4, copia=True,
                nota="GM8: x'(t) dt -> dx e y'(t) dt -> dy (cada par voa da linha 2 para o seu lugar; a C6.3 fica ao lado)")
        m4 = caixa_men(d4, 18)
        self.play(Create(m4), run_time=0.4)
        self.col("B6-1", d4)

        self.gat("No espaço")
        self.degrau("C6.5", "NO ESPAÇO: F = (P, Q, R) => int_gamma P dx + Q dy + R dz")
        d5 = mixl([("t", "NO ESPAÇO:", GEO), ("m", r"\Fv=(P,\ Q,\ R)\ \Rightarrow\ \int_{\g}P\,\dX+Q\,\dY+R\,\dZ")], 120, 705, 46)
        self.pena(*d5.p)
        self.col("B6-1", d5)

        self.gat("Cuidado")
        cgC, cfC, cmC = chipm([("t", "NÃO É", AL), ("m", r"\int"), ("t", "EM x MAIS", AL), ("m", r"\int"), ("t", "EM y: VOLTA SEMPRE PARA O", AL), ("m", r"\Tt")],
                              120, 820, 32, AL)
        self.chip_pena(cgC, cfC, cmC)
        self.col("B6-1", cgC, chips=1)

        self.gat("o redemoinho, nessa notação")
        self.degrau("C6.6", "REDEMOINHO: int_gamma -y dx + x dy")
        d6 = mixl([("t", "REDEMOINHO:", CAMPO), ("m", r"\int_{\g}-\Y\,\dX+\X\,\dY")], 120, 940, 46)
        self.pena(*d6.p)
        self.col("B6-1", d6)
        self.marca("12_B6-1")

        # ── B6-2 · a elipse e o dobro da área (alvo 13, C7.1–C7.7, GM9) ──────────────────────────────────────
        self.an("B6-2")
        self.titulo("A ELIPSE E O DOBRO DA ÁREA", rt=0.3)
        self.sobe_sai(d1a, d1b, d2, d3, d4, m4, d5, cgC, d6)
        self.col_zera("B6-1")
        self.limpa(rt=0.3)
        eix, (rx, ry) = eixos2(V, -2.9, 3.0, -2.2, 2.4)
        self.papel_vista(V, rt=0.4, extra=[Create(eix[0]), Create(eix[1])])
        self.pena(rx, ry)

        self.gat("o redemoinho numa elipse")
        self.degrau("C7.1", "int_gamma -y dx + x dy, x = 2 cos t, y = sen t, 0 <= t <= 2pi")
        el = curva(V, fe, 0, 2 * PI, HEL, 5)
        se = sentido(V, fe, PI * .55)
        sts = VGroup(*[seta_campo(V, fe(t), Frd(*fe(t)), .38, .8, CAMPO, 4, 15, z=7) for t in (PI / 4, 3 * PI / 4, 5 * PI / 4, 7 * PI / 4)])
        sx = V.linha([(0, 0), (2, 0)], E1, 4)
        sy = V.linha([(0, 0), (0, 1)], E2, 4)
        t2 = TC(r"\textcolor{ca}{2}", V.P(1, 0)[0], V.P(1, 0)[1] + 26, 30, "c")
        t1 = TC(r"\textcolor{cm}{1}", V.P(0, .5)[0] - 20, V.P(0, .5)[1], 30, "c")
        sqE, lqE = legq(HEL, "x = 2 cos t, y = sen t", 120, 1020, 28)
        sqR, lqR = legq(CAMPO, "REDEMOINHO", 560, 1020, 28)
        e1 = TC(r"\int_{\g}-\Y\,\dX+\X\,\dY,\qquad \X=2\cos\Tt,\ \Y=\sen\Tt,\ 0\le\Tt\le2\pi", COL - 40, 180, 36)
        self.play(Create(el), run_time=1.3)
        self.play(FadeIn(se), Create(sx), Create(sy), LaggedStart(*[Create(s) for s in sts], lag_ratio=0.15), FadeIn(sqE), FadeIn(sqR), run_time=0.8)
        self.pena(t2, t1, lqE, lqR)
        self.pena(e1)
        self.col("B6-2", e1)

        self.gat("O d x é a derivada")
        self.degrau("C7.2", "dx = -2 sen t dt, dy = cos t dt")
        e2 = TC(r"\dX=-2\sen\Tt\,\dTt,\qquad \dY=\cos\Tt\,\dTt", COL, 270, 42)
        self.pena(e2)
        self.col("B6-2", e2)

        self.gat("Menos y d x")
        self.degrau("C7.3", "-y dx = -sen t . (-2 sen t dt) = 2 sen^2 t dt")
        e3 = TC(r"-\Y\,\dX=-\sen\Tt\cdot(-2\sen\Tt\,\dTt)=2\sen^2\Tt\,\dTt", COL, 360, 40)
        self.pena(e3)
        self.col("B6-2", e3)

        self.gat("x d y: dois cosseno")
        self.degrau("C7.4", "x dy = 2 cos t . cos t dt = 2 cos^2 t dt")
        e4 = TC(r"\X\,\dY=2\cos\Tt\cdot\cos\Tt\,\dTt=2\cos^2\Tt\,\dTt", COL, 450, 40)
        self.pena(e4)
        self.col("B6-2", e4)

        self.gat("Somando, coloca o dois em evidência")
        self.degrau("C7.5", "-y dx + x dy = 2(sen^2 t + cos^2 t) dt = 2 dt")
        e5a = L([("l", r"-\Y\,\dX+\X\,\dY="), ("two", "2"), ("par", r"(\sen^2\Tt+\cos^2\Tt)"), ("dt", r"\,\dTt")], COL, 540, 40)
        self.pena(e5a)
        self.sub(gl(e5a, "par"), rt=0.8, cor=MEN)          # o parêntese acende menta (= 1)
        e5b = L([("eq", "="), ("two", "2"), ("dt", r"\,\dTt")], COL, 540, 40)
        ao_lado(e5a, e5b, sel(e5a, "l")[-1], 0, gap=12)
        self.gm(9, e5a, e5b, [("two", "two"), ("dt", "dt")], rt=1.1, copia=True,
                nota="GM9: 2(sen^2 t + cos^2 t) dt -> 2 dt (o parêntese acende menta e vira 1)")
        self.col("B6-2", VGroup(e5a, e5b))

        self.gat("Integra de zero a dois pi")
        self.degrau("C7.6", "int_0^2pi 2 dt = 2[t]_0^2pi = 4pi")
        e6 = TC(r"\int_0^{2\pi}2\,\dTt=2\Big[\Tt\Big]_0^{2\pi}=4\pi", COL, 650, 46)
        self.pena(e6)
        m6 = caixa_men(e6, 14)
        self.play(Create(m6), run_time=0.4)
        self.col("B6-2", e6)

        self.gat("Agora a área dessa elipse")
        self.degrau("C7.7", "AREA DA ELIPSE = pi.2.1 = 2pi => 4pi = 2 x AREA")
        elL = curva(V, fe, 0, 2 * PI, LI, 11)
        elL.set_z_index(5)
        qA = V.P(-1.45, -.45)
        tA = mixl([("t", "ÁREA", LI), ("m", r"\Lim{=2\pi}")], qA[0], qA[1], 30)
        e7 = mixl([("t", "ÁREA DA ELIPSE", LI), ("m", r"=\pi\cdot2\cdot1=2\pi\ \Rightarrow\ 4\pi=2\times"), ("t", "ÁREA", LI)], COL, 780, 40)
        self.play(Create(elL), run_time=1.0)
        self.pena(*tA.p)
        self.pena(*e7.p)
        self.col("B6-2", e7)

        self.gat("o dobro da área, de novo")
        ck = check_px(pxof(e7.get_right())[0] + 32, 780, MEN, 1.1)
        cgK, cfK, cmK = chipm([("t", "CÍRCULO:", GEO), ("m", r"2\pi R^2=2\times"), ("t", "ÁREA", GEO)], COL, 890, 32, GEO)
        self.play(Create(ck), run_time=0.4)
        self.chip_pena(cgK, cfK, cmK)
        self.col("B6-2", cgK, chips=1)
        self.calib("13_B6-2", V, axes=eix, curva_pts=[("(2, 0)", el, (2, 0)), ("(0, 1)", el, (0, 1))],
                   setas=[(f"campo t={k}pi/4", sts[i], fe(t), seta_ponta(V, fe(t), Frd(*fe(t)), .38, .8))
                          for i, (k, t) in enumerate(((1, PI / 4), (3, 3 * PI / 4), (5, 5 * PI / 4)))])
        self.marca("13_B6-2")
        self.sai_fim(rt=0.35)
