"""yt_0044 · Lote PA: A1 (abertura do episódio)."""
from k44 import *  # noqa: F401,F403


class PA(B44):
    ANTES = "A RECEITA EM QUATRO PERGUNTAS"

    def corpo(self):
        self.an("A1")
        self.titulo("EXERCÍCIOS DO MÓDULO")
        lg = self.logo(4.4).move_to(PX(960, 300))
        t1 = T("EXERCÍCIOS DO MÓDULO:", 960, 520, 52, "center", BR)
        t2 = T("INTEGRAL TRIPLA", 960, 595, 52, "center", CI)
        ct = cartao(200, 690, 1520, 120)
        res = T("CUBO · TETRAEDRO · CONE · MEIA BOLA · A LATA NA DOBRADIÇA", 960, 762, 34, "center", GEO)
        self.dentro(ct._painel, res)
        self.play(FadeIn(lg, scale=0.96), run_time=0.5)
        self.pena(t1, t2)
        self.pena(res, extra=[FadeIn(ct)])          # o cartão nasce junto do texto
        self.sai_fim()
