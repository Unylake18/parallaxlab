"""yt_0045 · Lote PB1: B1 (força constante, caminho reto). C1.1–C1.5, alvo 03. 2D: palco vista(180, 720, 120), coluna em 1020."""
from k45 import *  # noqa: F401,F403

COL = 1020
V = Vista2D(180, 720, 120)


class PB1(B45):
    ANTES = "INTEGRAL DE LINHA DE UM CAMPO VETORIAL"

    def corpo(self):
        self.an("B1")
        self.titulo("FORÇA CONSTANTE, CAMINHO RETO")
        eix, (rx, ry) = eixos2(V, -.6, 5.6, -.6, 4.2)
        nums = [TC(r"\Ge{%d}" % i, V.P(i, 0)[0], V.P(i, 0)[1] + 28, 26, "c") for i in range(1, 6)]
        nums += [TC(r"\Ge{%d}" % j, V.P(0, j)[0] - 22, V.P(0, j)[1], 26, "c") for j in range(1, 4)]
        self.papel_vista(V, rt=0.4, extra=[Create(eix[0]), Create(eix[1])])
        self.pena(rx, ry, *nums)

        self.gat("força constante e caminho reto")
        seg = V.linha([(1, 1), (4, 1)], HEL, 6)
        sseg = V.seta((1.55, 1), (1.95, 1), HEL, 6, 22)
        pA, pB = V.ponto((1, 1), BR, 10), V.ponto((4, 1), BR, 10)
        tA = placa_tc("A", V.P(1, 1)[0] - 34, V.P(1, 1)[1] + 30, 36)
        tB = placa_tc("B", V.P(4, 1)[0] + 30, V.P(4, 1)[1] + 30, 36)
        l0 = leg("F CONSTANTE, CAMINHO RETO", COL, 190, GEO, "left", 30)
        self.play(FadeIn(pA), run_time=0.2)
        self.play(Create(seg), run_time=0.9)
        self.play(FadeIn(pB), FadeIn(sseg), run_time=0.3)
        self.pena(tA, tB, l0)
        self.col("B1", l0)

        self.gat("F igual a dois, um")
        k = .48
        xm = 2.25
        sF = [V.seta((xx, 1), (xx + 2 * k, 1 + k), CAMPO, 4, 16) for xx in (1.08, 3.45)]
        sFm = V.seta((xm, 1), (xm + 2 * k, 1 + k), CAMPO, 5, 18)
        q = V.P(xm + .3, 1 + k)
        tF = placa_tc(r"\Fv=(2,\ 1)", q[0], q[1] - 40, 36, "l")
        self.play(*[Create(s) for s in sF + [sFm]], run_time=0.6)
        self.pena(tF)

        self.gat("F escalar B menos A")
        self.degrau("C1.1", "W = F . (B - A)")
        c1 = TC(r"W=\Fv\cdot(B-A)", COL, 265, 50)
        self.pena(c1)
        self.col("B1", c1)

        self.gat("ponto final menos ponto inicial")
        self.degrau("C1.2", "B - A = (4 - 1, 1 - 1) = (3, 0)")
        c2 = TC(r"B-A=(4-1,\ 1-1)=(3,\ 0)", COL, 360, 44)
        self.pena(c2)
        self.col("B1", c2)

        self.gat("multiplica coordenada com coordenada")
        self.degrau("C1.3", "W = 2.3 + 1.0 = 6")
        c3 = L([("a", r"W=2\cdot 3+"), ("b", r"1\cdot 0"), ("c", "=6")], COL, 455, 46)
        self.pena(c3)
        m3 = caixa_men(c3, 14)
        self.play(Create(m3), run_time=0.4)
        self.col("B1", c3)

        self.gat("aquele um da força")
        sL = V.seta((xm, 1), (xm + 2 * k, 1), LI, 4, 16)
        sG = V.seta((xm + 2 * k, 1), (xm + 2 * k, 1 + k), GEO, 4, 14)
        q2 = V.P(xm + k, 1)
        q1 = V.P(xm + 2 * k, 1 + k / 2)
        t2 = TC(r"\Lim{2}", q2[0], q2[1] + 28, 28, "c")
        t1 = TC(r"\Ge{1}", q1[0] + 20, q1[1], 28, "l")
        self.play(Create(sL), Create(sG), run_time=0.6)
        self.pena(t2, t1)
        self.sub(gl(c3, "b"), rt=1.2, cor=GEO)          # o 1 · 0 que some

        self.gat("o tamanho da força, vezes")
        self.degrau("C1.4", "W = |F| |B - A| cos alpha")
        c4 = TC(r"W=|\Fv|\,|B-A|\cos\al", COL, 560, 46)
        self.pena(c4)
        self.col("B1", c4)

        chips = [("Ângulo agudo", [("m", r"\cos\al>0:"), ("t", "AJUDA, ", LI), ("m", "W>0")], LI, 665),
                 ("Ângulo reto", [("m", r"\al=90^\circ:"), ("t", "DE LADO, ", GEO), ("m", "W=0")], GEO, 755),
                 ("Ângulo obtuso", [("m", r"\cos\al<0:"), ("t", "ATRAPALHA, ", AL), ("m", "W<0")], AL, 845)]
        cgs = []
        for g, partes, cor, y in chips:
            self.gat(g)
            self.degrau("C1.5", g)
            cg, cf, cm_ = chipm(partes, COL, y, 34, cor)
            self.chip_pena(cg, cf, cm_)
            cgs.append(cg)
        self.col("B1", *cgs, chips=3)
        self.calib("03_B1", V, axes=eix, curva_pts=[("A = (1, 1)", seg, (1, 1)), ("B = (4, 1)", seg, (4, 1))],
                   setas=[(f"F em x={xx}", s, (xx, 1), (xx + 2 * k, 1 + k)) for xx, s in ((1.08, sF[0]), (3.45, sF[1]), (xm, sFm))])
        self.marca("03_B1")
        self.sai_fim(rt=0.35)


def gl_all(m, i0, i1):
    return VGroup(*[m[0][i] for i in range(i0, min(i1, len(m[0])))])
