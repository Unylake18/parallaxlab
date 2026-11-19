"""yt_0045 · Lote PA: A1 (abertura do episódio)."""
from k45 import *  # noqa: F401,F403


class PA(B45):
    ANTES = "SÓ A PARTE AO LONGO DO CAMINHO TRABALHA"

    def corpo(self):
        self.an("A1")
        self.titulo("INTEGRAL DE LINHA DE UM CAMPO VETORIAL")
        lg = self.logo(4.4).move_to(PX(960, 300))
        t1 = T("INTEGRAL DE LINHA", 960, 520, 52, "center", BR)
        t2 = T("DE UM CAMPO VETORIAL", 960, 595, 52, "center", CI)
        ct = cartao(360, 690, 1200, 120)
        res = T("A FORÇA SOMADA AO LONGO DO CAMINHO", 960, 762, 34, "center", GEO)
        self.dentro(ct._painel, res)
        self.play(FadeIn(lg, scale=0.96), run_time=0.5)
        self.pena(t1, t2)
        self.pena(res, extra=[FadeIn(ct)])          # o cartão nasce junto do texto
        self.sai_fim()
