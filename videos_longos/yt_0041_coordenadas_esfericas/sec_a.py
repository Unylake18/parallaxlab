"""yt_0041 · A · bem-vindos (padrão do canal). Papel de borda a borda (passo 0,5), logo, CÁLCULO III · INTEGRAL TRIPLA (ciano), o título,
NESTE VÍDEO e as cinco etiquetas, uma por item falado. Sem canto (como o A1 da série)."""
from k41 import *


class PA(B41):
    CANTO = False

    def corpo(self):
        self.an("A1")
        lg = self.logo(4.2).move_to(PX(960, 245)).set_z_index(20)
        self.grade = papel(passo=0.5).set_z_index(-10)
        self.play(FadeIn(self.grade), FadeIn(lg, scale=0.96), run_time=0.5)
        self.gat("bem-vindos ao parallax")
        k = leg("CÁLCULO III · INTEGRAL TRIPLA", 960, 400, CI, "center", 32)
        self.pena(k, passo=0.02)
        self.gat("hoje é dia de")
        t = T("COORDENADAS ESFÉRICAS NA INTEGRAL TRIPLA", 960, 492, 60, "center")
        self.pena(t, passo=0.028)
        nv = leg("NESTE VÍDEO", 960, 600, GEO, "center", 30)
        self.pena(nv, passo=0.06)
        itens = [("t", "O ENDEREÇO"), ("m", "O"), ("t", "O TEOREMA"), ("t", "A BOLA"), ("t", "A CASQUINHA")]
        gats = ["o endereço de um ponto", "o fator de volume", "o teorema", "a bola a bola pesada", "uma casquinha de sorvete"]
        W_, PASSO_ = 318, 344
        for i, ((tp, r), gg) in enumerate(zip(itens, gats)):
            self.gat(gg)
            X = 960 + (i - 2) * PASSO_
            if tp == "t":
                tt = T(r, X, 676, 30, "center")
            else:                                   # O r² sen φ: palavra em Space Grotesk + o fator em MathTex (lima), lado a lado
                tt = mixl([("t", "O", BR), ("m", r"\J")], X, 664, 36)
                tt.shift(PX(X, 0) - np.array([tt.get_center()[0], 0, 0]) - PX(0, 0) * 0 + np.array([0, 0, 0]) - np.array([PX(X, 0)[0] - tt.get_center()[0], 0, 0]) * 0)
                tt.shift(RIGHT * (PX(X, 0)[0] - tt.get_center()[0]))
            mol = moldura(X - W_ / 2, 632, W_, 66, GEO, .5, 2, 10)
            self.pena(tt, passo=0.04, extra=[Create(mol)])
        self.marca("A1", agora=True)
        self.sai_fim()
