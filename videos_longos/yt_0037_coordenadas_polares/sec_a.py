"""yt_0037 · A · bem-vindos (padrão do canal) — v2 (E02: cada moldura nasce junto com a sua etiqueta). Logo, CÁLCULO DE INTEGRAL DUPLA ·
MUDANÇA DE VARIÁVEIS (ciano), o título, NESTE VÍDEO e as cinco etiquetas, uma por palavra falada. Sem canto; o cartão √π ? continua no canto."""
from v2kit import *


class PA(B37):
    CANTO = False
    CARTAO = True

    def corpo(self):
        self.an("A1")
        lg = self.logo(4.2).move_to(PX(960, 245)).set_z_index(20)
        k = leg("CÁLCULO DE INTEGRAL DUPLA · MUDANÇA DE VARIÁVEIS", 960, 400, CI, "center", 32)
        self.grade = papel(passo=0.5).set_z_index(-10)            # K2: tela sem gráfico = quadradinhos de 60 px
        self.play(FadeIn(self.grade), FadeIn(lg, scale=0.96), run_time=0.5)
        self.gat("bem-vindos ao parallax")
        self.pena(k, passo=0.018)
        t = T("COORDENADAS POLARES NA INTEGRAL DUPLA", 960, 492, 64, "center")
        self.gat("hoje é dia de")
        self.pena(t, passo=0.03)
        nv = leg("NESTE VÍDEO", 960, 600, GEO, "center", 30)
        self.pena(nv, passo=0.08)
        rot_ = ["1 · A GRADE", "2 · O FATOR r", "3 · O TEOREMA", "4 · DOIS DISCOS", "5 · O SINO"]
        gats = ["a grade de círculos", "o fator de área", "o teorema dois", "dois discos e", "a integral do sino"]
        W_, PASSO_ = 318, 344
        for i, (r, gg) in enumerate(zip(rot_, gats)):
            self.gat(gg)
            X = 960 + (i - 2) * PASSO_
            tt = T(r, X, 676, 30, "center")
            mol = moldura_de(tt, X - W_ / 2, 632, W_, 66, GEO, .5, 2, 10)
            self.pena(tt, passo=0.04, extra=[Create(mol)])
        self.sai_fim()
