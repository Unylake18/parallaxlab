"""yt_0042 · S · síntese (S1, sem alvo) e girar a lata (S2, alvo 17). S1: três colunas ✓ com os resultados (πR²h, π/2+2/3, ≈2,76). S2: o 3D `giro`
com a seta de giro, a célula e o fio s; I = ∭ s² ρ dV; o cartão NO PRÓXIMO VÍDEO (≥ 8 s) e o CTA liso."""
from k42 import *

XC = [340, 960, 1580]
CW = 560


class PS(B42):
    ANTES = "RESUMINDO"

    def corpo(self):
        # ── S1 ────────────────────────────────────────────────────────────────────────────────────────────
        self.an("S1")
        self.grade = papel(passo=0.5).set_z_index(-10)
        cards = [painel41(XC[k] - CW / 2, 190, CW, 700) for k in range(3)]
        self.play(FadeIn(self.grade), Create(cards[0]), run_time=0.4)
        self.titulo("RESUMINDO", rt=0.3)
        t0 = T("O ENDEREÇO (s, θ, z) · O FATOR s", 960, 250, 34, "center")
        self.pena(t0)
        c0 = check_px(XC[0] + 230, 250)
        self.play(Create(c0), run_time=0.3)
        self.gat("o cilindro deu")
        self.play(Create(cards[1]), run_time=0.4)
        t1 = mixl([("t", "CILINDRO", BR), ("m", r"\Me{\pi R^2h}")], XC[0] - 200, 430, 44)
        self.pena(*t1.p, lag=0.1)
        c1 = check_px(XC[0] + 230, 330)
        self.play(Create(c1), run_time=0.3)
        self.gat("o cilindro fora do eixo deu")
        self.play(Create(cards[2]), run_time=0.4)
        t2 = mixl([("t", "FORA DO EIXO", BR), ("m", r"\Me{\dfrac{\pi}{2}+\dfrac23}")], XC[1] - 200, 430, 44)
        self.pena(*t2.p, lag=0.1)
        c2 = check_px(XC[1] + 230, 330)
        self.play(Create(c2), run_time=0.3)
        self.gat("a lata pesada deu")
        t3 = mixl([("t", "LATA PESADA", BR), ("m", r"\Me{\approx 2{,}76}")], XC[2] - 200, 430, 44)
        self.pena(*t3.p, lag=0.1)
        c3 = check_px(XC[2] + 230, 330)
        self.play(Create(c3), run_time=0.3)
        dv = TC(r"dV=\Js\,\dS\,\dT\,\dZ", 960, 650, 46, "c")
        self.pena(dv)
        l1 = leg("O s SAI POR TRÊS CAMINHOS:", 960, 760, GEO, "center", 30)
        l2 = leg("ARESTAS · POLARES × ALTURA · DETERMINANTE", 960, 810, GEO, "center", 30)
        self.pena(l1, l2, lag=0.3)
        self.marca("S1", agora=True)

        # ── S2 ────────────────────────────────────────────────────────────────────────────────────────────
        self.an("S2")
        self.titulo("GIRAR A LATA", rt=0.3)
        saem = [m for m in self.mobjects if m not in self.fixos() and not isinstance(m, ValueTracker) and m is not self.clk and m is not self.grade]
        gi = self.palco("giro", cam_alvo("s2"), seta=0.0, cel=0.0)
        gi.fundo.op.set_value(0.0)
        self.add(gi.fundo)
        self.play(*[FadeOut(m) for m in saem], gi.fundo.op.animate.set_value(1.0), run_time=0.6)
        self.remove(*saem)
        rz = self.rot3(gi, "ez", r"\Z", dx=20, size=36)
        self.pena(rz)
        self.gat("girar essa lata em volta do eixo")
        self.play(gi.tr["seta"].animate(rate_func=linear).set_value(1.0), run_time=0.7)
        self.gat("cada pedacinho entra pesando")
        self.play(gi.tr["cel"].animate(rate_func=linear).set_value(1.0), run_time=0.6)
        l1 = mixl([("t", "CADA PEDAÇO CUSTA", GEO), ("m", r"\S^2\cdot dm")], 1010, 200, 44)
        self.pena(*l1.p, lag=0.1)
        self.gat("a distância até o eixo, ao quadrado")
        l2 = L([("i", r"I"), ("eq", "="), ("p", r"\iiint \S^2\,\de\,dV")], 1010, 310, 50)
        self.pena(l2)
        self.degrau("C10", "I = ∭ s² ρ dV")
        self.gat("vira s ao cubo")
        l3 = mixl([("t", "EM CILÍNDRICAS:", GEO), ("m", r"\S^2\cdot\Js=\S^3")], 1010, 420, 44)
        self.pena(*l3.p, lag=0.1)
        self.gat("no próximo vídeo")
        cd = painel41(1060, 540, 760, 330)
        n1 = T("NO PRÓXIMO VÍDEO", 1440, 620, 30, "center", GEO)
        n2 = T("CENTRO DE MASSA", 1440, 705, 46, "center", BR)
        n3 = T("E MOMENTO DE INÉRCIA", 1440, 775, 46, "center", SOMB)
        n4 = leg("NA INTEGRAL TRIPLA", 1440, 840, GEO, "center", 28)
        t_card = self.t
        self.play(Create(cd), run_time=0.4)
        self.pena(n1)
        self.pena(n2, n3, lag=0.3)
        self.pena(n4)
        self.dentro((1060, 540, 1820, 870), n1, n2, n3, n4)
        self.marca("17_S2", agora=True)
        self.gat("deixa o like")
        print(f"[cartao] próximo vídeo na tela por {self.t - t_card:.2f} s antes do CTA")
        cta42(self, rt_fim=0.0)
