"""yt_0044 final §9 (copiado do yt_0032): renders/capitulos_final.txt com os tempos da voz (início da âncora de cada capítulo em ancoras.json)."""
import json
from pathlib import Path

U = Path(__file__).resolve().parent
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
CAP = [("H1", "A LATA NA DOBRADIÇA"), ("H2", "A RECEITA EM QUATRO PERGUNTAS"), ("A1", "BEM-VINDOS"), ("E1-1", "O CUBO: A SOMA DE RIEMANN"), ("E1-2", "O LIMITE DAS SOMAS"),
       ("E1-3", "O CUBO: A CONTA EXATA"), ("E1-4", "ONDE O CUBO EQUILIBRA"), ("E1-5", "A FOLHA QUE NÃO PESA"), ("E2-1", "O TETRAEDRO: SOMBRA E SONDA"),
       ("E2-2", "O TETRAEDRO: A MASSA"), ("E2-3", "CONFERINDO PELO CENTROIDE"), ("E2-4", "ONDE O TETRAEDRO EQUILIBRA"), ("E3-1", "O CONE EM CILÍNDRICAS"),
       ("E3-2", "ONDE O CONE EQUILIBRA"), ("E3-3", "QUANTO CUSTA GIRAR O CONE"), ("E3-4", "O CONE EM ESFÉRICAS"), ("E4-1", "A MEIA BOLA"),
       ("E4-2", "CONFERINDO POR FATIAS"), ("E4-3", "DENSIDADE QUE CRESCE PARA FORA"), ("E5-1", "A LATA NA DOBRADIÇA: MONTAR"), ("E5-2", "TRÊS PEDAÇOS"),
       ("E5-3", "CONFERINDO COM O POLO NA DOBRADIÇA"), ("E6-1", "O TEOREMA DOS EIXOS PARALELOS"), ("E6-2", "O CUBO PELA ARESTA"),
       ("E6-3", "A BOLA ENCOSTADA E O ERRO CLÁSSICO"), ("S1", "A RECEITA E OS CINCO ERROS"), ("S2", "E SE A SOMA FOR AO LONGO DE UM CAMINHO?")]
linhas = []
for aid, tit in CAP:
    t = 0.0 if aid == "H1" else A[aid]["ini"]
    linhas.append(f"{int(t // 60)}:{int(t % 60):02d} {tit}")
(U / "renders").mkdir(exist_ok=True)
(U / "renders" / "capitulos_final.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
print("\n".join(linhas))
