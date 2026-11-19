"""yt_0034 final §9 (copiado do yt_0032): renders/capitulos_final.txt com os tempos da voz (início da âncora de cada capítulo em ancoras.json)."""
import json
from pathlib import Path

U = Path(__file__).resolve().parent
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
CAP = [("H0", "UMA INTEGRAL QUE TRAVA"), ("A1", "BEM-VINDOS"), ("B1-1", "A FATIA QUE TERMINA NA CURVA"), ("B2-1", "O TEOREMA EM REGIÕES GERAIS"),
       ("B3-1", "A CUNHA NAS DUAS ORDENS"), ("B4-1", "TROCAR A ORDEM: O SINO"), ("B4-3", "O ERRO CLÁSSICO"), ("B5-1", "A CHAPA NA DIAGONAL"),
       ("B6-1", "SENO DE X AO CUBO"), ("B7-1", "QUANDO A REGIÃO SE DIVIDE"), ("B7-2", "QUANDO VALE TROCAR"), ("B8", "NO MUNDO: PROBABILIDADE"),
       ("S1", "SÍNTESE E DESAFIO")]
linhas = []
for aid, tit in CAP:
    t = 0.0 if aid == "H0" else A[aid]["ini"]
    linhas.append(f"{int(t // 60)}:{int(t % 60):02d} {tit}")
(U / "renders").mkdir(exist_ok=True)
(U / "renders" / "capitulos_final.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
print("\n".join(linhas))
