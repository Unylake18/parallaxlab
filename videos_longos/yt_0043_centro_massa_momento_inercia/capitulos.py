"""yt_0043 final §9 (copiado do yt_0032): renders/capitulos_final.txt com os tempos da voz (início da âncora de cada capítulo em ancoras.json)."""
import json
from pathlib import Path

U = Path(__file__).resolve().parent
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
CAP = [("H1", "A LATA QUE GIRA"), ("A1", "BEM-VINDOS"), ("B1-1", "DO SISTEMA DE PONTOS AO CORPO"), ("B1-2", "O QUE O CENTRO DE MASSA GARANTE"), ("B1-3", "SIMETRIA"),
       ("B2-1", "A TAÇA: MONTAR"), ("B2-2", "A TAÇA: A CONTA"), ("B3-1", "MOMENTO DE INÉRCIA"), ("B3-2", "DISTÂNCIA AO EIXO"), ("B3-3", "O CILINDRO UNIFORME"),
       ("B3-4", "A BOLA UNIFORME"), ("B3-5", "QUEM GIRA MAIS FÁCIL"), ("B4-1", "ONDE A LATA PESADA EQUILIBRA"), ("B4-3", "QUANTO CUSTA GIRAR A LATA"),
       ("B4-4", "O TRIÂNGULO"), ("B4-5", "A SECANTE À SÉTIMA"), ("B4-6", "O QUE OS DOIS NÚMEROS DIZEM"), ("S1", "RESUMINDO"), ("S2", "E SE O EIXO ESTIVER NA PAREDE?")]
linhas = []
for aid, tit in CAP:
    t = 0.0 if aid == "H1" else A[aid]["ini"]
    linhas.append(f"{int(t // 60)}:{int(t % 60):02d} {tit}")
(U / "renders").mkdir(exist_ok=True)
(U / "renders" / "capitulos_final.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
print("\n".join(linhas))
