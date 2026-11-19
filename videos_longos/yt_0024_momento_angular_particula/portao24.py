"""yt_0024 v2: triagem do portão G28 e afins (linhas [audit] de log_aud_<L>.txt) em REAL × FALSO POSITIVO, com a justificativa de cada regra.
Agrupa por (lote, classe, rótulo, objeto); uma regra de falso positivo só vale para o padrão que descreve. Tudo o que não casa é REAL.
uso: python portao24.py → renders/portao_triagem.txt"""
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
U = Path(__file__).resolve().parent
LOTES = ["PH", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PS"]
FP = [
    (r"TEXTO SOBRE OBJETO '0\{,\}075' x Polygon", "o número da área acende DENTRO do triângulo que ele mede (handoff v2 §2.3, area_lab)"),
    (r"TEXTO SOBRE OBJETO '0\{,\}090.*' x Polygon", "o número da área fica dentro da área que ele mede (area_lab)"),
    (r"TEXTO SOBRE OBJETO '(0\{,\}30\\,\\mathrm\{s\}|-0\{,\}59|-1\{,\}96\\,\\mathrm\{N\\,m\})' x Line",
     "cotas do triângulo de inclinação sobre a grade do gráfico (linhas DIM a 12 % de opacidade, v2 §2.3 grafico_lab)"),
    (r"TEXTO SOBRE OBJETO '.*' x Line em .*grade", "grade do gráfico (12 %)"),
    (r"TEXTO SOBRE OBJETO .* x Brace", "a chave marca o termo (r sen φ) da própria linha: encosta nela por construção"),
    (r"COR OPERADOR 'd'", "d é a distância (grandeza, laranja VETC), não o operador diferencial"),
]


def classe(ln):
    m = re.search(r"\[audit\]\s+[0-9.]+s\s+(.*)$", ln)
    if not m:
        return None
    s = m.group(1)
    s = re.sub(r" em \(?-?[0-9.]+[;…].*$", "", s)
    s = re.sub(r"\(folga [^)]*\)", "(folga)", s)
    s = re.sub(r"\([0-9.]+x[0-9.]+\)", "", s)
    s = re.sub(r"por [0-9.]+s.*$", "", s)
    return s.strip()


out, tot_real, tot_fp = [], Counter(), Counter()
for l in LOTES:
    f = U / f"log_aud_{l}.txt"
    if not f.exists():
        out.append(f"{l}: auditoria não rodada")
        continue
    c = Counter(x for x in (classe(ln) for ln in f.read_text(encoding="utf-8", errors="replace").splitlines() if "[audit]" in ln) if x)
    real, fp = [], []
    for k, n in c.most_common():
        why = next((w for rx, w in FP if re.search(rx, k)), None)
        (fp if why else real).append((k, n, why))
    tot_real[l] = sum(n for _, n, _ in real)
    tot_fp[l] = sum(n for _, n, _ in fp)
    out.append(f"== {l}: REAL {tot_real[l]} quadros auditados · falso positivo {tot_fp[l]}")
    for k, n, _ in real:
        out.append(f"   REAL  {n:5d}  {k}")
    for k, n, w in fp:
        out.append(f"   FP    {n:5d}  {k}  ← {w}")
out.insert(0, f"yt_0024 v2 — triagem do portão (G28 e afins, a cada 3 quadros): REAL {sum(tot_real.values())} · falso positivo {sum(tot_fp.values())}")
out.insert(1, "")
(U / "renders" / "portao_triagem.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
