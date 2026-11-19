"""yt_0031 final §9: renders/capitulos_final.txt com os tempos da voz (início da âncora de cada capítulo em ancoras.json)."""
import json
from pathlib import Path

U = Path(__file__).resolve().parent
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
CAP = [("H1", "TRÊS PERGUNTAS"), ("A1", "BEM-VINDOS"), ("B1-1", "PISO, TETO E TAMPAS"), ("B2-1", "A CHAPA DE DOIS METAIS"), ("B3-1", "CONTEÚDO NULO"),
       ("B4-1", "CURVAS TÊM CONTEÚDO NULO"), ("B5-1", "FRONTEIRA"), ("B6-1", "CONTINUIDADE UNIFORME"), ("B7-1", "O TEOREMA"), ("B8-1", "QUANDO FALHA"),
       ("B9-1", "NUM EXERCÍCIO"), ("S1", "SÍNTESE E PRÓXIMO")]
linhas = []
for aid, tit in CAP:
    t = 0.0 if aid == "H1" else A[aid]["ini"]
    linhas.append(f"{int(t // 60)}:{int(t % 60):02d} {tit}")
(U / "renders").mkdir(exist_ok=True)
(U / "renders" / "capitulos_final.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
print("\n".join(linhas))
