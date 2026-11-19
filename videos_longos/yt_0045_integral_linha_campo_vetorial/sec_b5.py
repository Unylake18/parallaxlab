"""yt_0045 · Lote PB5: B5-1 (o vento que sopra para fora) e B5-2 (por que deu zero). C5.1–C5.9, GM6–GM7, alvos 10–11.
2D: palco vista(480, 760, 240) (papel passo 0,25 = 60 px), coluna em 1020."""
from k45 import *  # noqa: F401,F403

COL = 1020
V = Vista2D(480, 760, 240)
fp = lambda t: (t, t * t)
PTS = grade_pts([-1.5, -.75, .75, 1.5], [.4, 2.0]) + [(-.75, 1.2), (.75, 1.2)] + [(0, .4), (0, 1.2), (0, 2.0), (-1.5, -.4), (1.5, -.4), (-.75, -.4), (.75, -.4)]
Fout = lambda X, Y: (X, Y)


class PB5(B45):
    ANTES = "NO RAIO: A FORÇA DE LADO"

    def corpo(self):
        # ── B5-1 · o vento que sopra para fora (alvo 10, C5.1–C5.5, GM6) ──────────────────────────────────────
        self.an("B5-1")
        self.titulo("O VENTO QUE SOPRA PARA FORA")
        eix, (rx, ry) = eixos2(V, -1.8, 1.85, -.75, 2.45)
        nums = [TC(r"\Ge{%d}" % v, V.P(v, 0)[0], V.P(v, 0)[1] + 28, 26, "c") for v in (-1, 1)] + [TC(r"\Ge{1}", V.P(0, 1)[0] - 22, V.P(0, 1)[1], 26, "c")]
        self.papel_vista(V, rt=0.4, extra=[Create(eix[0]), Create(eix[1])])
        self.pena(rx, ry, *nums)

        self.gat("O campo agora é F de x, y igual a x, y")
        self.degrau("C5.1a", "F(x, y) = (x, y)")
        cp = campo_grade(V, Fout, [-1.75, -1.25, -.75, -.25, .25, .75, 1.25, 1.75], [-.25, .25, .75, 1.25, 1.75, 2.25], k=.28, mx=.4,
                         curvas=[arco2(fp, -1.2, 1.2, 200), arco2(lambda t: (math.sqrt(2) * math.cos(t), math.sqrt(2) * math.sin(t)), -.2, PI + .2, 120)],
                         folga=.1, evita_px=[(30, 440, 420, 500), (700, 440, 920, 500), (200, 770, 280, 820), (680, 770, 760, 820), (420, 500, 470, 540)])
        sqF, lqF = legq(CAMPO, "F = (x, y): EMPURRA PARA LONGE DA ORIGEM", 120, 1020, 28)
        a1 = TC(r"\Fv(\X,\Y)=(\X,\ \Y)", COL, 185, 46)
        self.play(LaggedStart(*[Create(s) for s in cp], lag_ratio=0.04), FadeIn(sqF), run_time=1.0)
        self.pena(a1, lqF)
        self.col("B5-1", a1)

        self.gat("a conta anda pela parábola")
        self.degrau("C5.1b", "gamma(t) = (t, t^2), -1 <= t <= 1")
        par = curva(V, fp, -1, 1, HEL, 6)
        se1, se2 = sentido(V, fp, -.45), sentido(V, fp, .55)
        pA, pB = V.ponto((-1, 1), BR, 9), V.ponto((1, 1), BR, 9)
        qA, qB = V.P(-1, 1), V.P(1, 1)
        tA = placa_tc(r"\g(-1)=(-1,\ 1)", 54, qA[1] - 40, 28, "l")          # margem de 48 px (no alvo encosta em x = 20)
        tB = placa_tc(r"\g(1)=(1,\ 1)", qB[0] + 20, qB[1] - 40, 28, "l")
        a2 = TC(r"\g(\Tt)=(\Tt,\ \Tt^2),\quad -1\le\Tt\le1", COL, 275, 44)
        self.play(FadeIn(pA), run_time=0.2)
        self.play(Create(par), run_time=1.2)
        self.play(FadeIn(pB), FadeIn(se1), FadeIn(se2), run_time=0.3)
        self.pena(tA, tB, a2)
        self.col("B5-1", a2)

        self.gat("Passo um")
        self.degrau("C5.2a", "(1) F(gamma(t)) = (t, t^2)")
        n1 = num(1, 1045, 365, 50)
        a3a = TC(r"\Fv(\g(\Tt))=(\Tt,\ \Tt^2)", 1090, 365, 40)
        self.pena(n1, a3a)
        self.gat("Passo dois")
        self.degrau("C5.2b", "(2) gamma'(t) = (1, 2t)")
        x2 = pxof(a3a.get_right())[0] + 50
        n2 = num(2, x2 + 25, 365, 50)
        a3b = TC(r"\gp(\Tt)=(1,\ 2\Tt)", x2 + 70, 365, 40)
        self.pena(n2, a3b)
        self.col("B5-1", VGroup(a3a, a3b))

        self.gat("Passo três")
        self.degrau("C5.3", "(3) F(gamma(t)) . gamma'(t) = t.1 + t^2.2t = t + 2t^3")
        n3 = num(3, 1045, 455, 50)
        a4 = TC(r"\Fv(\g(\Tt))\cdot\gp(\Tt)=\Tt\cdot1+\Tt^2\cdot2\Tt=\Tt+2\Tt^3", 1090, 455, 40)
        self.pena(n3, a4)
        self.col("B5-1", a4)

        self.gat("Agora integra de menos um até um")
        self.degrau("C5.4", "W = int_-1^1 (t + 2t^3) dt = [t^2/2 + t^4/2]_-1^1")
        a5 = L([("w", r"W=\int_{-1}^{1}(\Tt+2\Tt^3)\,\dTt="), ("br", r"\Big[\dfrac{\Tt^2}{2}+\dfrac{\Tt^4}{2}\Big]_{-1}^{1}")], COL, 575, 42)
        self.pena(a5)
        self.col("B5-1", a5)

        self.gat("Aplica os limites")
        self.degrau("C5.5a", "= (1/2 + 1/2) - (1/2 + 1/2)")
        a6 = L([("eq", "="), ("a", r"\Big(\tfrac12+\tfrac12\Big)"), ("mn", "-"), ("b", r"\Big(\tfrac12+\tfrac12\Big)")], COL + 70, 700, 42)
        self.gm(6, a5, a6, [("br", ["a", "mn", "b"])], rt=1.3, copia=True,
                nota="GM6: [t^2/2 + t^4/2]_-1^1 -> (1/2 + 1/2) - (1/2 + 1/2) (os limites descem para dentro)")
        self.col("B5-1", a6)

        self.gat("Um menos um: zero")
        self.degrau("C5.5", "= 1 - 1 = 0")
        a7 = TC(r"=1-1=0", 0, 700, 42, "l")
        ao_lado(a6, a7, sel(a6, "eq")[0], 0, gap=12)
        self.pena(a7)
        m7 = caixa_men(VGroup(a6, a7), 14)
        self.play(Create(m7), run_time=0.4)
        self.calib("10_B5-1", V, axes=eix, curva_pts=[("(-1, 1)", par, (-1, 1)), ("(1, 1)", par, (1, 1)), ("(0, 0)", par, (0, 0))],
                   setas=calib_setas(cp, (0, len(cp) // 2, len(cp) - 1)))
        self.marca("10_B5-1")

        # ── B5-2 · por que deu zero (alvo 11, C5.6–C5.9, GM7) ────────────────────────────────────────────────
        self.an("B5-2")

        self.gat("Quebra o caminho no meio")
        pAL = curva(V, fp, -1, 0, AL, 7)
        pLI = curva(V, fp, 0, 1, LI, 7)
        s1, s2 = sentido(V, fp, -.45, AL), sentido(V, fp, .55, LI)
        sqI, lqI = legq(AL, "IDA ATÉ A ORIGEM: CONTRA", 120, 1020, 28)
        sqV, lqV = legq(LI, "VOLTA: A FAVOR", 560, 1020, 28)
        self.sobe_sai(a1, a2, n1, a3a, n2, a3b, n3, a4, a5, a6, a7, m7, rt=0.8,
                      extra=[FadeOut(sqF), FadeOut(lqF), FadeOut(par), FadeOut(se1), FadeOut(se2), Create(pAL), Create(pLI), FadeIn(s1), FadeIn(s2),
                             FadeIn(sqI), FadeIn(sqV)])
        self.remove(sqF, lqF, par, se1, se2)
        self.titulo("POR QUE DEU ZERO", rt=0.3)
        self.pena(lqI, lqV)

        self.gat("o trabalho dessa metade é menos um")
        self.degrau("C5.6", "IDA: int_-1^0 (t + 2t^3) dt = 0 - 1 = -1")
        b1 = mixl([("t", "IDA:", AL), ("m", r"\int_{-1}^{0}(\Tt+2\Tt^3)\,\dTt=0-1=\Al{-1}")], COL, 190, 42)
        self.pena(*b1.p)
        self.col("B5-2", b1)

        self.gat("o trabalho é mais um")
        self.degrau("C5.7", "VOLTA: int_0^1 (t + 2t^3) dt = 1 - 0 = +1")
        b2 = mixl([("t", "VOLTA:", LI), ("m", r"\int_{0}^{1}(\Tt+2\Tt^3)\,\dTt=1-0=\Lim{+1}")], COL, 300, 42)
        self.pena(*b2.p)
        self.col("B5-2", b2)

        self.gat("Olha a primitiva")
        self.degrau("C5.8", "t^2/2 + t^4/2 = 1/2 (x^2 + y^2) NO PONTO gamma(t)")
        b3a = L([("a", r"\dfrac{\Tt^2}{2}"), ("p", "+"), ("b", r"\dfrac{\Tt^4}{2}")], COL, 420, 42)
        self.pena(b3a)
        b3b = L([("eq", "="), ("h", r"\dfrac12"), ("po", "("), ("x", r"\X^2"), ("pl", "+"), ("y", r"\Y^2"), ("pc", ")")], COL, 420, 42)
        ao_lado(b3a, b3b, sel(b3a, "p")[0], sel(b3b, "pl")[0], gap=12)
        b3b.shift(UP * (b3a[0][sel(b3a, "p")[0]].get_center()[1] - b3b[0][sel(b3b, "pl")[0]].get_center()[1]))
        self.gm(7, b3a, b3b, [("a", "x"), ("p", "pl"), ("b", "y")], rt=1.2, copia=True,
                nota="GM7: t^2/2 + t^4/2 -> 1/2 (x^2 + y^2) (o t vira x, o t^2 vira y)")
        b3c = mixl([("t", "NO PONTO", GEO), ("m", r"\g(\Tt)")], pxof(b3b.get_right())[0] + 14, 420, 42)
        self.pena(*b3c.p)
        self.col("B5-2", VGroup(b3a, b3b, b3c))

        self.gat("na mesma distância, raiz de dois")
        self.degrau("C5.9", "AS DUAS PONTAS À DISTÂNCIA sqrt2 => W = 0")
        o = V.P(0, 0)
        R2 = math.sqrt(2) * 240
        arcpts = [(o[0] + R2 * math.cos(a), o[1] - R2 * math.sin(a)) for a in np.linspace(PI * 1.07, -PI * .07, 120)]
        circ = lin_px(arcpts, GEO, 2.5, dash=(10, 8), z=4)
        rr = V.linha([(0, 0), (-1, 1)], GEO, 2)
        qs = V.P(-.55, .62)
        ts = placa_tc(r"\sqrt2", qs[0] - 6, qs[1], 30)
        b4 = mixl([("t", "AS DUAS PONTAS À DISTÂNCIA", BR), ("m", r"\sqrt2\ \Rightarrow\ W=0")], COL, 545, 42)
        self.play(Create(circ), Create(rr), run_time=1.0)
        self.pena(ts)
        self.pena(*b4.p)
        ck = check_px(pxof(b4.get_right())[0] + 34, 545, MEN, 1.1)
        self.play(Create(ck), run_time=0.4)
        self.col("B5-2", b4)

        self.gat("os campos conservativos")
        sm_, st_ = selo("SÓ IMPORTAM AS PONTAS: CAMPO CONSERVATIVO", COL, 660, MEN, 30)
        self.pena(st_, extra=[Create(sm_)])
        self.col("B5-2", st_)
        self.calib("11_B5-2", V, axes=eix, curva_pts=[("(-1, 1)", pAL, (-1, 1)), ("(1, 1)", pLI, (1, 1))],
                   setas=calib_setas(cp, (0, len(cp) // 2, len(cp) - 1)))
        self.marca("11_B5-2")
        self.sai_fim(rt=0.35)
