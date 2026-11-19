"""yt_0042 · A · bem-vindos (padrão do canal). Papel de borda a borda (passo 0,5), logo, CÁLCULO III · INTEGRAL TRIPLA (ciano), o título e a linha
NESTE VÍDEO (O ENDEREÇO · O FATOR s · A LATA PESADA). Sem canto."""
from k42 import *


class PA(B42):
    CANTO = False

    def corpo(self):
        self.an("A1")
        lg = self.logo(4.2).move_to(PX(960, 245)).set_z_index(20)
        self.grade = papel(passo=0.5).set_z_index(-10)
        self.play(FadeIn(self.grade), FadeIn(lg, scale=0.96), run_time=0.5)
        k = leg("CÁLCULO III · INTEGRAL TRIPLA", 960, 400, CI, "center", 32)
        self.pena(k, passo=0.02)
        t = T("COORDENADAS CILÍNDRICAS NA INTEGRAL TRIPLA", 960, 492, 60, "center")
        self.pena(t, passo=0.028)
        nv = leg("NESTE VÍDEO", 960, 600, GEO, "center", 30)
        self.pena(nv, passo=0.06)
        it = mixl([("t", "O ENDEREÇO", BR), ("m", r"(\S,\ \T,\ \Z)"), ("t", "· O FATOR", GEO), ("m", r"\Js"), ("t", "· A LATA PESADA", BR)], 960, 676, 40)
        it.shift(RIGHT * (PX(960, 0)[0] - it.get_center()[0]))
        mol = moldura(960 - 700, 632, 1400, 66, GEO, .5, 2, 10)
        self.pena(*it.p, passo=0.04, extra=[Create(mol)])
        self.marca("A1", agora=True)
        self.sai_fim()
