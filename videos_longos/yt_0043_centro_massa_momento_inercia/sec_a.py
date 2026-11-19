"""yt_0043 · Lote PA: A1 (abertura do episódio)."""
from k43 import *  # noqa: F401,F403


class PA(B43):
    ANTES = "UMA CONTA POR PEDAÇO"

    def corpo(self):
        self.an("A1")
        self.titulo("CENTRO DE MASSA E MOMENTO DE INÉRCIA")
        lg = self.logo(4.4).move_to(PX(960, 260))
        t1 = T("CENTRO DE MASSA E MOMENTO DE INÉRCIA", 960, 470, 52, "center", BR)
        t2 = T("NA INTEGRAL TRIPLA", 960, 545, 52, "center", CI)
        ct = cartao(240, 660, 1440, 130)
        res = mixl([
            ("t", "NESTE VÍDEO:", GEO),
            ("m", r"\zb"),
            ("t", "·  SIMETRIA  ·", GEO),
            ("m", r"I=\iiint\S^2\de\,dV"),
            ("t", "·  A LATA PESADA", CI),
        ], 300, 725, 38)
        self.dentro(ct._painel, res)
        self.play(FadeIn(lg, scale=0.96), run_time=0.5)
        self.pena(t1, t2)
        self.pena(res, extra=[FadeIn(ct)])          # I10: o cartão nasce junto do texto (nenhum quadro com cartão vazio)
        self.sai_fim()
