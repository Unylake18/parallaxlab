"""yt_0037 final §9 (copiado do yt_0032): renders/capitulos_final.txt com os tempos da voz (início da âncora de cada capítulo em ancoras.json)."""
import json
from pathlib import Path

U = Path(__file__).resolve().parent
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
CAP = [("H1", "A INTEGRAL QUE NÃO COLABORA"), ("A1", "BEM-VINDOS"), ("B1-1", "O ENDEREÇO DE UM PONTO"), ("B1-2", "A GRADE DE CÍRCULOS E RAIOS"),
       ("B2-1", "O RETÂNGULO POLAR"), ("B2-2", "O FATOR É O JACOBIANO"), ("B2-3", "O TESTE DA UNIDADE"), ("B3-1", "O TEOREMA EM POLARES"),
       ("B3-2", "A RECEITA E A RETA-SONDA"), ("B4-1", "O DISCO DO COMEÇO"), ("B4-2", "ANÉIS E CASCAS"), ("B5", "UM DISCO FORA DO CENTRO"),
       ("B6-1", "O SINO INTEIRO (GAUSS)"), ("B6-3", "A CURVA NORMAL"), ("B7", "QUANDO USAR POLARES"), ("S1", "JUNTANDO TUDO")]
linhas = []
for aid, tit in CAP:
    t = 0.0 if aid == "H1" else A[aid]["ini"]
    linhas.append(f"{int(t // 60)}:{int(t % 60):02d} {tit}")
(U / "renders").mkdir(exist_ok=True)
(U / "renders" / "capitulos_final.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
print("\n".join(linhas))
