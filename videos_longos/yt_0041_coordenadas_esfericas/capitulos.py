"""yt_0041 final §9 (copiado do yt_0032): renders/capitulos_final.txt com os tempos da voz (início da âncora de cada capítulo em ancoras.json)."""
import json
from pathlib import Path

U = Path(__file__).resolve().parent
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
CAP = [("H1", "A BOLA PESADA NA CASCA"), ("A1", "BEM-VINDOS"), ("B1-1", "O ENDEREÇO ESFÉRICO"), ("B1-2", "UM PONTO DE EXEMPLO"), ("B1-3", "A CAIXA VIRA A BOLA"),
       ("B2-1", "A CAIXINHA CURVA"), ("B2-2", "DUAS POLARES EM SEQUÊNCIA"), ("B2-3", "O DETERMINANTE"), ("B2-4", "O TESTE DA BOLA"),
       ("B3-1", "O TEOREMA, METADE POR METADE"), ("B3-2", "A RECEITA E A SONDA"), ("B4", "A BOLA É UMA CEBOLA"), ("B5", "DE VOLTA À BOLA"),
       ("B6-1", "A CASQUINHA: AS SUPERFÍCIES"), ("B6-2", "A CASQUINHA: A CONTA"), ("B7", "QUANDO USAR"), ("S1", "RESUMINDO"), ("S2", "E UMA LATA?")]
linhas = []
for aid, tit in CAP:
    t = 0.0 if aid == "H1" else A[aid]["ini"]
    linhas.append(f"{int(t // 60)}:{int(t % 60):02d} {tit}")
(U / "renders").mkdir(exist_ok=True)
(U / "renders" / "capitulos_final.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
print("\n".join(linhas))
