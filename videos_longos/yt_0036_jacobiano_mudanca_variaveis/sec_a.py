"""yt_0036 · A · bem-vindos (alvo 03). Sem canto. Linha de série (sem número de vídeo), título, NESTE VÍDEO e as cinco etiquetas, uma por gatilho
(a última em lima). v2 (Q16): cada moldura nasce com a etiqueta dela, no gatilho. Papel: papel() na unidade padrão."""
from j36 import *


class PA(J36):
    CANTO = False

    def corpo(self):
        self.an("A1")
        # final K14: o título começa na 1ª palavra ("Fala, pessoal") e termina em ≤ 3 s; NESTE VÍDEO em "Hoje a gente troca";
        # cada caixa nasce JUNTO com o seu texto (K2: o Create da moldura dura o mesmo que a caneta do rótulo, os dois no mesmo play)
        k = leg("CÁLCULO III · MUDANÇA DE VARIÁVEIS", 960, 420, CI, "center", 28)
        t = T("JACOBIANO E MUDANÇA DE VARIÁVEIS", 960, 500, 62, "center")
        self.gat("fala pessoal")
        self.pena(t, k, passo=0.045, lag=0.3)
        mols = [moldura(380 + i * 290 - 135, 630, 270, 60, GEO, .5, 2, 10) for i in range(5)]
        self.gat("hoje a gente troca")
        nv = leg("NESTE VÍDEO", 960, 600, GEO, "center", 26)
        self.pena(nv, passo=0.06)
        rot_ = ["A RÉGUA", "O PARALELOGRAMO", "O FATOR LOCAL", "O TEOREMA", "O TRAPÉZIO"]
        gats = ["a régua esticada", "o paralelogramo das", "o fator local de", "o teorema de mudança", "o trapézio inteiro"]
        for i, (r, gg) in enumerate(zip(rot_, gats)):
            self.gat(gg)
            tt = T(f"{i + 1} · {r}", 380 + i * 290, 670, 26, "center", LIMA if i == 4 else BR)
            self.pena(tt, passo=0.05, extra=[Create(mols[i])])
        self.marca("03", agora=True)
        self.sai_fim()
