"""yt_0039 · A · bem-vindos (padrão do canal). Logo, EXERCÍCIOS DO MÓDULO, NESTE VÍDEO e os seis chips (26 px), um por item falado. Sem canto."""
from k39 import *


class PA(B39x):
    CANTO = False

    def corpo(self):
        self.an("A1")
        lg = self.logo(4.2).move_to(PX(960, 245)).set_z_index(20)
        self.grade = papel_cartao()
        self.play(FadeIn(self.grade), FadeIn(lg, scale=0.96), run_time=0.5)
        self.gat("bem-vindos ao parallax")
        k = leg("CÁLCULO III · INTEGRAL DUPLA", 960, 400, CI, "center", 32)
        self.pena(k, passo=0.018)
        self.gat("seis problemas")
        t = T("EXERCÍCIOS DO MÓDULO", 960, 492, 64, "center")
        self.pena(t, passo=0.03)
        nv = leg("NESTE VÍDEO", 960, 600, GEO, "center", 30)
        self.pena(nv, passo=0.06)
        rot_ = ["1 · PARÁBOLAS", "2 · HIPÉRBOLES", "3 · OITAVO DE BOLA", "4 · ELIPSE", "5 · MEIA ARRUELA", "6 · PAPPUS"]
        gats = ["duas parábolas", "duas hipérboles", "um oitavo de bola", "uma elipse", "a meia arruela", "o teorema de pappus"]
        W_, PASSO_ = 286, 300
        for i, (r, gg) in enumerate(zip(rot_, gats)):
            self.gat(gg)
            X = 960 + (i - 2.5) * PASSO_
            tt = T(r, X, 676, 26, "center")
            mol = moldura_de(tt, X - W_ / 2, 636, W_, 58, GEO, .5, 2, 10)
            self.pena(tt, passo=0.035, extra=[Create(mol)])
        self.sai_fim()
