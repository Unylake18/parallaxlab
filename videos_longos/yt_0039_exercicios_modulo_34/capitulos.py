"""yt_0039 final §9 (copiado do yt_0034): renders/capitulos_final.txt com os tempos da voz (início da âncora de cada capítulo em ancoras.json)."""
import json
from pathlib import Path

U = Path(__file__).resolve().parent
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
CAP = [("H1", "A CHAPA QUE EQUILIBRA NO BURACO?"), ("A1", "BEM-VINDOS"), ("E1-1", "1 · A FAIXA ENTRE PARÁBOLAS"), ("E2-1", "2 · AS HIPÉRBOLES"),
       ("E3-1", "3 · O OITAVO DE BOLA"), ("E4-1", "4 · A ELIPSE"), ("E4-2", "4 · A MEIA ELIPSE PESADA"), ("E5-1", "5 · A MEIA ARRUELA"),
       ("E6-1", "6 · O TEOREMA DE PAPPUS"), ("S1", "OS CINCO ERROS"), ("S2", "O PRÓXIMO PASSO")]
linhas = []
for aid, tit in CAP:
    t = 0.0 if aid == "H1" else A[aid]["ini"]
    linhas.append(f"{int(t // 60)}:{int(t % 60):02d} {tit}")
(U / "renders").mkdir(exist_ok=True)
(U / "renders" / "capitulos_final.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
print("\n".join(linhas))
