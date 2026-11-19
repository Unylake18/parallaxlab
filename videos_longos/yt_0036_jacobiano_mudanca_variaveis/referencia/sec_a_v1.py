"""yt_0036 · A · bem-vindos (alvo 03). Sem canto. Linha de série (sem número de vídeo), título, NESTE VÍDEO e as cinco etiquetas, uma por gatilho
(a última em lima)."""
from j36 import *


class PA(J36):
    CANTO = False

    def corpo(self):
        self.an("A1")
        k = leg("CÁLCULO III · MUDANÇA DE VARIÁVEIS", 960, 420, CI, "center", 28)
        self.pena(k, passo=0.03)
        self.gat("bem-vindos ao parallax")
        mols = [moldura(380 + i * 290 - 135, 630, 270, 60, GEO, .5, 2, 10) for i in range(5)]
        self.play(LaggedStart(*[Create(m) for m in mols], lag_ratio=0.15), run_time=1.6)
        self.gat("as próprias variáveis")
        t = T("JACOBIANO E MUDANÇA DE VARIÁVEIS", 960, 500, 62, "center")
        self.pena(t, passo=0.07)
        nv = leg("NESTE VÍDEO", 960, 600, GEO, "center", 26)
        self.pena(nv, passo=0.08)
        rot_ = ["A RÉGUA", "O PARALELOGRAMO", "O FATOR LOCAL", "O TEOREMA", "O TRAPÉZIO"]
        gats = ["a régua esticada", "o paralelogramo das", "o fator local de", "o teorema de mudança", "o trapézio inteiro"]
        for i, (r, gg) in enumerate(zip(rot_, gats)):
            self.gat(gg)
            tt = T(f"{i + 1} · {r}", 380 + i * 290, 670, 26, "center", LIMA if i == 4 else BR)
            self.pena(tt, passo=0.05)
        self.marca("03", agora=True)
        self.sai_fim()
