"""yt_0036 · B8 · o jacobiano no mundo (sem alvo). Dois cartões de traço GEO, sem foto e sem efeito: (1) a grade de Mercator (meridianos
verticais, paralelos cada vez mais espaçados para o norte), uma célula em 72° acesa com × sec²(LATITUDE) e ≈ × 10, e a célula do equador ao lado
para a comparação; legenda TERRA COMO ESFERA; (2) o quadradinho do EP. 03 escoando num campo (um movimento curto) com ÁREA × (1 + t · div F + …)."""
from j36 import *

K1, K2 = (100, 220, 820, 640), (1000, 220, 820, 640)
RAD = PI / 180
SM = 250                                          # px por radiano na projeção
X0M, YEQ = 510, 790                               # meridiano 0 e equador (px)


def merc_y(lat):
    return YEQ - SM * math.log(math.tan(PI / 4 + lat * RAD / 2))


def merc_x(lon):
    return X0M + SM * lon * RAD


def campo(x, y):
    """Campo do cartão 2 (em px, centro do quadradinho em (1410, 500)): expansão + giro leve."""
    dx, dy = (x - 1410) / 120, (500 - y) / 120
    return (.45 * dx - .30 * dy, .30 * dx + .45 * dy)


class PB8(J36):
    ANTES = "PAUSE E TENTE"

    def corpo(self):
        self.an("B8")
        self.secao("O JACOBIANO NO MUNDO")
        p1, p2 = painel(*K1), painel(*K2)
        self.play(Create(p1), Create(p2), run_time=0.6)
        # cartão 1: Mercator
        self.gat("a projeção de mercator")
        mer = VGroup(*[lin_px([(merc_x(l), merc_y(0)), (merc_x(l), merc_y(76))], GEO, 1.5, alpha=.55, z=-9) for l in range(-80, 81, 20)])
        par = VGroup(*[lin_px([(merc_x(-80), merc_y(a)), (merc_x(80), merc_y(a))], GEO, 1.5, alpha=.55, z=-9) for a in range(0, 76, 15)])
        self.play(LaggedStart(*[Create(m) for m in mer], lag_ratio=0.08), LaggedStart(*[Create(m) for m in par], lag_ratio=0.12), run_time=1.6)
        labs = [TC(r"\Ge{%d^\circ}" % a, merc_x(-80) - 14, merc_y(a), 26, "r") for a in (0, 30, 60)]
        self.pena(*labs, lag=0.1)
        self.gat("como uma esfera")
        te = leg("TERRA COMO ESFERA", 510, 840, GEO, "center", 26)
        self.pena(te)
        self.gat("a secante da latitude")
        s = 35                                        # lado (px) de um quadrado de 8° no equador
        L72 = s / math.cos(72 * RAD)
        c72 = Vw(600 - L72 / 2, merc_y(72) + L72 / 2, L72)
        cel72 = celula(c72, ID, 0, 1, 0, 1, n=4, wb=3, N=8)
        entra_cel(self, cel72, rt=0.7)
        r1 = rotm([("m", r"\times\,\Lm{\sec^2}("), ("t", "LATITUDE", LIMA), ("m", ")")], 600 + L72 / 2 + 20, merc_y(72) - 22, 26, "l")
        self.pena(r1)
        self.gat("mais de dez vezes")
        r2 = TP(r"\approx\times\,\Lm{10}", 600 + L72 / 2 + 20, merc_y(72) + 34, 30, "l")
        self.pena(r2)
        self.gat("catorze vezes")
        ce = Vw(600 - s / 2, merc_y(4) + s / 2, s)
        celE = celula(ce, ID, 0, 1, 0, 1, n=1, wb=3, N=4)
        entra_cel(self, celE, rt=0.6)
        realca(self, cel72.borda, celE.borda, cor=LIMA, rt=0.4, wpx=4)
        # cartão 2: o quadradinho escoando num campo
        self.gat("e nos fluidos")
        set_ = VGroup()
        for x in range(1090, 1760, 90):
            for y in range(300, 700, 90):
                vx, vy = campo(x, y)
                set_.add(seta_px((x, y), (x + 34 * vx, y - 34 * vy), GEO, 2, 10, z=3))
        vq = Vw(1370, 540, 80)
        q = celula(vq, ID, 0, 1, 0, 1, n=4, wb=3, N=12)
        self.play(LaggedStart(*[GrowArrow(a) if False else FadeIn(a) for a in set_], lag_ratio=0.02), run_time=1.0)
        entra_cel(self, q, rt=0.6)
        self.gat("estica ou encolhe")

        def flui(p):
            X, Y = pxof(p)
            vx, vy = campo(X, Y)
            return PX(X + 60 * vx, Y - 60 * vy)
        self.play(ApplyPointwiseFunction(flui, q), run_time=2.2)
        self.gat("um mais tê vezes o divergente")
        f = rotm([("t", "ÁREA"), ("m", r"\times\left(1+t\cdot\operatorname{div}\Ci{\vec F}+\dots\right)")], 1410, 810, 32, "c", placa=False)
        self.pena(f)
        self.gat("a soma dos estiramentos")
        acende(self, (f.p[1], CI), rt=0.8)
        self.marca("B8")
        self.sai_fim()
