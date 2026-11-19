"""yt_0032 final §9: renders/capitulos_final.txt com os tempos da voz (início da âncora de cada capítulo em ancoras.json)."""
import json
from pathlib import Path

U = Path(__file__).resolve().parent
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
CAP = [("H1", "A BALANÇA"), ("A1", "BEM-VINDOS"), ("B1-1", "SOMAR E MULTIPLICAR"), ("B2-1", "SINAL E COMPARAÇÃO"), ("B3-1", "A SOLDA NÃO PESA"),
       ("B4-1", "MUDAR f SEM MUDAR A INTEGRAL"), ("B5-1", "DIVIDIR A REGIÃO"), ("B6-1", "VALOR MÉDIO"), ("B7-1", "INTEGRAL SEM INTEGRAR"),
       ("S1", "SÍNTESE E PRÓXIMO")]
linhas = []
for aid, tit in CAP:
    t = 0.0 if aid == "H1" else A[aid]["ini"]
    linhas.append(f"{int(t // 60)}:{int(t % 60):02d} {tit}")
(U / "renders" / "capitulos_final.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
print("\n".join(linhas))
