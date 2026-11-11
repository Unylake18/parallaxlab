"""Lote PB7 · NO ESPAÇO (B7-1, B7-2), layout A (quadro 18): F⃗(X) = −X/‖X‖³, ‖F⃗‖ = 1/r². Cena 3D `c7_campo` (2 cascas de raio 1,5 e 2,3 com 26 e 40 setas para a origem,
anel vazado na origem; some a seta a menos de 55° da linha de visão); a câmera gira no máximo 20° no total. Domínio A = ℝ³ − {0} (A em GEO)."""
from v7 import *  # noqa: F401,F403

BOX = [140, 200, 920, 840]


class LoteB7(Base):
    def corpo(self):
        set_dy(48)
        seg = {}

        def est(t):
            return {"az": 20 * suave(t / 25.0), "box": caixa(BOX)}

        self.an("B7-1")
        self.secao("NO ESPAÇO")
        cmp = Fundo3D(self, "c7_campo", est, op=0.0)
        self.add(cmp)
        self.play(cmp.op.animate.set_value(1.0), run_time=0.8)
        f1 = TC(r"\F(X) = -\dfrac{X}{\|X\|^3}", 1120, 450, 58)
        f2 = TC(r"\|\F\| = \dfrac{1}{r^2}", 1120, 610, 58)
        self.gat("em cada ponto do espaço")
        self.play(self.caneta_ate(f1, "com tamanho igual a um dividido"))
        self.gat("com tamanho igual a um dividido")
        self.play(caneta(f2))

        self.an("B7-2")
        dom = TC(r"{\G A} = \mathbb{R}^3 - \{0\}", 1120, 750, 50)
        self.gat("menos um ponto")
        self.play(caneta(dom))
        self.gat("o domínio faz parte da função")
        self.play(pulso(dom, 1.05), run_time=1.0)
        self._fecha(antes=0.4 + 0.35 + 0.2)       # v9: a saída inteira cabe na âncora
        self.play(FadeOut(VGroup(f1, f2, dom)), cmp.op.animate.set_value(0.0), run_time=0.4)
        cmp.clear_updaters()
        self.remove(cmp, f1, f2, dom)
        self.sai_fim()
