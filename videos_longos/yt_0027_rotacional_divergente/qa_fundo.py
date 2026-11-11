"""[fundo] luminância média por faixa de 1/9 da altura num quadro sem conteúdo (alvo: variação <= 10% entre o centro e a faixa de baixo)."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image
raiz = Path(__file__).resolve().parents[2] / "assets" / "calculo"
for nome, arq in (("fundo27_milimetrado (unidade)", Path(__file__).resolve().parent / "renders" / "fundo" / "fundo27_milimetrado_1920x1080.png"),
                  ("fundo_calculo_liso", raiz / "fundo_calculo_liso_1920x1080.png")):
    a = np.asarray(Image.open(arq).convert("L"), float)
    h = a.shape[0] // 9
    faixas = [a[i * h:(i + 1) * h, 960:1900].mean() for i in range(9)]       # fora da placa do canto (x < 1240) só nas faixas de cima: usa x >= 960
    var = abs(faixas[8] - faixas[4]) / faixas[4] * 100
    print(f"[fundo] {nome}: faixas {' '.join(f'{f:.1f}' for f in faixas)}; variação centro × baixo {var:.1f}% ({'ok' if var <= 10 else 'FORA'})")
