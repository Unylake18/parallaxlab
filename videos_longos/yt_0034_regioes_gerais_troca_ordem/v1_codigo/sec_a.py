"""yt_0034 · A · bem-vindos (alvo 03). Sem canto. As cinco etiquetas a 26 px (no alvo, 24): a moldura acompanha a largura do texto."""
from pecas34 import *


class PA(B34):
    CANTO = False

    def corpo(self):
        self.an("A1")
        t = T("REGIÕES GERAIS E TROCA DE ORDEM", 960, 500, 64, "center")
        self.pena(t, passo=0.11)
        self.gat("o teorema de fubini")
        k = leg("CÁLCULO DE INTEGRAL DUPLA · VÍDEO 2", 960, 420, CI, "center", 28)
        self.pena(k, passo=0.07)
        self.gat("em duas integrais")
        nv = leg("NESTE VÍDEO", 960, 600, GEO, "center", 26)
        self.pena(nv, passo=0.09)
        rot_ = ["A FATIA NA CURVA", "O TEOREMA", "DUAS ORDENS", "A TROCA", "QUANDO VALE"]
        gats = ["a fatia que termina", "o teorema para regiões", "as duas ordens de", "como trocar uma", "quando vale a pena"]
        tt = [T(f"{i + 1} · {r}", 0, 670, 26, "center", MEN if i == 3 else BR) for i, r in enumerate(rot_)]
        ws = [x.width * 120 + 36 for x in tt]
        gap = 22
        X = 960 - (sum(ws) + gap * 4) / 2
        mols = []
        for x, w in zip(tt, ws):
            x.move_to(PX(X + w / 2, 0)[0] * RIGHT + x.get_center()[1] * UP)
            mols.append(moldura(X, 630, w, 60, GEO, .5, 2, 10))
            X += w + gap
        self.gat("sai do retângulo")
        self.play(LaggedStart(*[Create(m) for m in mols], lag_ratio=0.25), run_time=2.0)
        for x, gg in zip(tt, gats):
            self.gat(gg)
            self.pena(x, passo=0.07)
        self.marca("03")
        self.sai_fim()
