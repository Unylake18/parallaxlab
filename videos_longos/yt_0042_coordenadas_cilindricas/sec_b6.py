"""yt_0042 · B6 · quando usar cilíndricas. 2D com papel; quatro cartões opacos com miniaturas (lata ✓, meio cilindro ✓, cano ✓, bola ✗ em contorno) e
cinco legendas ✓/✗."""
from k42 import *


def _cil(v, X, Y, u, cor, H=1.0, R=.7):
    """Silhueta de um cilindro em pé (retângulo + elipse do topo), origem do eixo no pé."""
    body = v.linha([(-R, 0), (R, 0), (R, H), (-R, H), (-R, 0)], cor, 3)
    top = v.arco(R * u, 0, 2 * PI, cor, 3)
    return VGroup(body, top)


class PB6(B42):
    ANTES = "QUANDO USAR"

    def corpo(self):
        self.an("B6")
        self.grade = papel(passo=0.5).set_z_index(-10)
        self.play(FadeIn(self.grade), run_time=0.4)
        self.titulo("QUANDO USAR", rt=0.3)
        XC = [300, 760, 1220]
        cards = [painel41(XC[k] - 180, 220, 360, 360) for k in range(3)]
        cards.append(painel41(1620, 220, 240, 360))
        self.play(*[Create(c) for c in cards], run_time=0.5)
        # lata ✓
        v1 = Vista2D(XC[0], 380, 130)
        self.play(Create(_cil(v1, XC[0], 380, 130, GEO)), run_time=0.4)
        self.pena(leg("LATA", XC[0], 560, GEO, "center", 30))
        # deslocado ✓ (meio cilindro deitado)
        v2 = Vista2D(XC[1], 380, 130)
        self.play(Create(v2.linha([(-.9, 0), (.9, 0), (.9, .8), (-.9, .8), (-.9, 0)], GEO, 3)), run_time=0.4)
        self.pena(leg("MEIO CILINDRO", XC[1], 560, GEO, "center", 30))
        # cano ✓
        v3 = Vista2D(XC[2], 380, 130)
        self.play(Create(_cil(v3, XC[2], 380, 130, GEO)), run_time=0.4)
        self.pena(leg("CANO", XC[2], 560, GEO, "center", 30))
        # bola ✗ (contorno simples)
        v4 = Vista2D(1740, 380, 130)
        self.play(Create(v4.arco(100, 0, 2 * PI, GEO, 3)), run_time=0.4)
        self.pena(leg("BOLA", 1740, 560, GEO, "center", 30))
        cks = [check_px(XC[0], 260), check_px(XC[1], 260), check_px(XC[2], 260)]
        self.play(*[Create(c) for c in cks], run_time=0.4)
        self.play(Create(cruz_px(1740, 260)), run_time=0.4)
        # legendas
        self.gat("quando a região tem um eixo")
        l1 = leg("✓ TEM UM EIXO", 60, 680, MEN, "left", 32)
        self.pena(l1)
        self.gat("vira s ao quadrado")
        l2 = leg("✓ APARECE x² + y²", 60, 760, MEN, "left", 32)
        self.pena(l2)
        self.gat("entra por um piso e sai por um teto")
        l3 = leg("✓ PISO E TETO EM z", 60, 840, MEN, "left", 32)
        self.pena(l3)
        self.gat("numa bola")
        l4 = leg("✗ BOLA → ESFÉRICAS", 60, 920, AL, "left", 32)
        self.pena(l4)
        self.gat("numa caixa")
        l5 = leg("✗ CAIXA → CARTESIANAS", 60, 1000, AL, "left", 32)
        self.pena(l5)
        self.col("B6", l1, l2, l3, l4, l5)
        self.marca("B6", agora=True)
        self.sai_fim()
