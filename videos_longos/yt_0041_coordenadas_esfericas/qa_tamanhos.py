"""yt_0041 R2: tamanhos pedidos por bloco (log_pressa_<LOTE>.txt, linhas [tam]) → altura real a 1080p: x minúsculo ≈ 0,43·tam, algarismo ≈ 0,66·tam
(fórmulas: KaTeX px = tam). Escreve qa/tamanhos_final.txt. Regra: texto de coluna/legenda ≥ 26 px de corpo; fórmula ≥ 36 (principal 44–58)."""
import re, sys
from collections import defaultdict
from pathlib import Path
U = Path(__file__).resolve().parent
LOTES = ["PH", "PA", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PB7", "PS"]
por = defaultdict(lambda: {"F": [], "T": []})
for L in LOTES:
    p = U / f"log_pressa_{L}.txt"
    if not p.exists():
        continue
    for l in p.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"\[tam\] (\S+) (\S+) ([FT]) (\d+) (.*)", l)
        if m:
            por[m.group(2)][m.group(3)].append((int(m.group(4)), m.group(5)))
out = ["TAMANHOS REAIS POR BLOCO (1080p): corpo = tamanho pedido (px); x minúsculo ≈ 0,43·corpo; algarismo ≈ 0,66·corpo", "",
       f"{'bloco':6} {'fórm.max':>8} {'fórm.min':>8} {'x(max)':>7} {'alg.(min fórm.)':>16} {'texto.min':>10}  abaixo do limite (fórm < 36 · texto < 26)"]
ruim = 0
for aid, d in por.items():
    F = [s for s, _ in d["F"]]
    Tt = [s for s, _ in d["T"]]
    if not (F or Tt):
        continue
    fm, fM = (min(F), max(F)) if F else (0, 0)
    tm = min(Tt) if Tt else 0
    bad = [f"{t}({s})" for s, t in d["F"] if s < 36] + [f"{t}({s})" for s, t in d["T"] if s < 26]
    ruim += len(bad)
    out.append(f"{aid:6} {fM:8d} {fm:8d} {0.43 * fM:7.1f} {0.66 * fm:16.1f} {tm:10d}  {'; '.join(bad[:4])}{' …' if len(bad) > 4 else ''}")
out += ["", f"itens abaixo do limite: {ruim}"]
(U / "qa").mkdir(exist_ok=True)
R = sys.argv[1] if len(sys.argv) > 1 else "v5"
(U / "qa" / "tamanhos_final.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
(U / "renders" / R / "qa" / "tamanhos_final.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
