"""yt_0030 · handoff final §8: capítulos com os tempos da voz (um por bloco; cada um começa no ini da 1ª âncora do bloco) → renders/capitulos_final.txt."""
import json
from pathlib import Path

U = Path(__file__).resolve().parent
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
CAP = [("H", "TRÊS FILMES, TRÊS FÓRMULAS"), ("A", "BEM-VINDOS"), ("D1", "MESMA FÓRMULA, DOIS FILMES"), ("D2", "DESENHAR SEM MIL SETAS"),
       ("D3", "A FAMÍLIA DE REDEMOINHOS"), ("D3b", "DUAS REGRAS"), ("D4", "O CAMPO QUE NÃO MELHORA DE PERTO"), ("D5", "O DESAFIO"),
       ("P2", "APLICAÇÃO · O RIO"), ("A2", "APLICAÇÃO · ÁGUA BATENDO NA PAREDE"), ("A4", "APLICAÇÃO · MAPAS QUE NÃO ENTORTAM"),
       ("A3", "APLICAÇÃO · POR QUE 1/r E 1/r²"), ("S", "RESUMO E PRÓXIMO VÍDEO")]
ini = {}
for a in A["ordem"]:
    ini.setdefault(A["ancoras"][a]["bloco"], A["ancoras"][a]["ini"])
L = []
for b, t in CAP:
    s = 0 if b == "H" else int(ini[b])
    L.append(f"{s // 60}:{s % 60:02d} {t}")
(U / "renders").mkdir(exist_ok=True)
(U / "renders" / "capitulos_final.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
