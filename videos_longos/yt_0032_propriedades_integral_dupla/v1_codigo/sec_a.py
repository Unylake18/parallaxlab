"""yt_0032 · A · apresentação (alvo 03). Sem canto."""
from lib32 import *


class PA(B32):
    CANTO = False

    def corpo(self):
        self.an("A1")
        k = leg("INTEGRAIS DUPLAS · VÍDEO 3", 960, 420, CI, "center", 28)
        t = T("PROPRIEDADES DA INTEGRAL DUPLA", 960, 500, 60, "center")
        self.wait(0.3)
        self.pena(t)
        self.gat("o terceiro do módulo")
        self.pena(k)
        self.gat("agora vamos aprender")
        nv = leg("NESTE VÍDEO", 960, 600, GEO, "center", 26)
        self.pena(nv)
        rot = ["SOMAR", "COMPARAR", "DIVIDIR", "MÉDIA"]
        gats = ["somar comparar estimar", "comparar estimar e", "dividir integrais sem", "teorema do valor médio"]
        for i, (r, gg) in enumerate(zip(rot, gats)):
            self.gat(gg)
            X = 600 + i * 240
            cx = moldura(X - 112, 630, 224, 56, GEO, 0.5, 2, 10)
            tt = T(f"{i + 1} · {r}", X, 668, 26, "center", CI if i == 3 else BR)
            self.play(Create(cx), run_time=0.3)
            self.pena(tt)
        self.marca("03")
        self.sai_fim()
