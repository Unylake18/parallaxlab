"""yt_0036 final §9 (copiado do yt_0034): renders/capitulos_final.txt com os tempos da voz (início da âncora de cada capítulo em ancoras.json)."""
import json
from pathlib import Path

U = Path(__file__).resolve().parent
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
CAP = [("H1", "A INTEGRAL QUE TRAVA"), ("A1", "BEM-VINDOS"), ("B1-1", "A RÉGUA ESTICADA"), ("B2-1", "A TRANSFORMAÇÃO"),
       ("B3-1", "O PARALELOGRAMO E O DETERMINANTE"), ("B4-1", "A GRADE CURVA"), ("B4-3", "O JACOBIANO"), ("B5-2", "O TEOREMA DE MUDANÇA DE VARIÁVEIS"),
       ("B5-3", "POR QUE INVERSÍVEL"), ("B6-1", "O TRAPÉZIO DO COMEÇO"), ("B7", "PAUSE E TENTE"), ("B8", "O JACOBIANO NO MUNDO"), ("S1", "JUNTANDO TUDO")]
linhas = []
for aid, tit in CAP:
    t = 0.0 if aid == "H1" else A[aid]["ini"]
    linhas.append(f"{int(t // 60)}:{int(t % 60):02d} {tit}")
(U / "renders").mkdir(exist_ok=True)
(U / "renders" / "capitulos_final.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
print("\n".join(linhas))
