"""Mapa de âncoras do preview (início de cada ### da narração no vídeo montado): soma o início de cada lote (montar_preview_v4) com o
[ancora] do log do lote. uso: python mapa_ancoras.py → mapa_ancoras_v4.txt"""
import re
from pathlib import Path

U = Path(__file__).resolve().parent
ordem = ["PH", "P7", "P8", "P9", "P10", "Q6", "Q7", "Q8", "Q9", "PC", "PS"]
t0, linhas = 0.0, []
for L in ordem:
    log = (U / f"log_{L}.txt").read_text(encoding="utf-8")
    an = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", log)]
    for aid, t in an:
        if aid != "FIM":
            T = t0 + t
            linhas.append(f"{int(T // 60)}:{T % 60:05.2f}  {T:8.2f} s  {aid}  ({L})")
    t0 += [t for a, t in an if a == "FIM"][0]
linhas.append(f"{int(t0 // 60)}:{t0 % 60:05.2f}  {t0:8.2f} s  FIM")
(U / "mapa_ancoras_v4.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
print(len(linhas) - 1, "âncoras; fim em", round(t0, 2), "s")
