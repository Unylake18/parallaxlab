"""yt_0045 final §9 (copiado do yt_0032): renders/capitulos_final.txt com os tempos da voz (início da âncora de cada capítulo em ancoras.json)."""
import json
from pathlib import Path

U = Path(__file__).resolve().parent
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
CAP = [("H1", "A HÉLICE NA PAREDE DA LATA"), ("H2", "SÓ A PARTE AO LONGO DO CAMINHO TRABALHA"), ("A1", "BEM-VINDOS"), ("B1", "FORÇA CONSTANTE, CAMINHO RETO"),
       ("B2-1", "CAMINHO CURVO, FORÇA QUE MUDA"), ("B2-2", "APARECE UMA SOMA DE RIEMANN"), ("B3", "A DEFINIÇÃO"), ("B4-1", "O REDEMOINHO NO CÍRCULO"),
       ("B4-2", "CONFERINDO PELA SOMA, NA MÃO"), ("B4-3", "NO RAIO: A FORÇA DE LADO"), ("B5-1", "O VENTO QUE SOPRA PARA FORA"), ("B5-2", "POR QUE DEU ZERO"),
       ("B6-1", "OUTRA NOTAÇÃO"), ("B6-2", "A ELIPSE E O DOBRO DA ÁREA"), ("B7-1", "A HÉLICE DA LATA: MONTANDO"), ("B7-2", "A HÉLICE DA LATA: A CONTA"),
       ("B7-3", "LENDO A RESPOSTA"), ("S1", "RESUMO"), ("S2", "MAIS RÁPIDO, AO CONTRÁRIO, COM QUINA")]
linhas = []
for aid, tit in CAP:
    t = 0.0 if aid == "H1" else A[aid]["ini"]
    linhas.append(f"{int(t // 60)}:{int(t % 60):02d} {tit}")
(U / "renders").mkdir(exist_ok=True)
(U / "renders" / "capitulos_final.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
print("\n".join(linhas))
