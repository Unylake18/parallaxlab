"""yt_0020 v2: resumo do portão G28 por (classe, assinatura) com intervalos de tempo.
uso: python g28.py LOTE [LOTE ...] [--top N] [--classe NOME]   (lê log_aud_<LOTE>.txt; roda ./auditar.sh LOTE antes)
Uma linha por ocorrência única: classe · assinatura sem coordenadas · intervalos [t0–t1 s] · nº de passadas. O objetivo é 0 real por classe."""
import re
import sys
from collections import defaultdict
from pathlib import Path

U = Path(__file__).resolve().parent
CLASSES = ["TEXTO SOBRE OBJETO", "TEXTO SOBRE CAIXA", "TEXTO PEQUENO", "ENCOSTADO", "OBJETO FORA DA MARGEM", "FORA DA MARGEM", "FORA DA ZONA", "CALHA",
           "CHAMADA CRUZA CORPO", "SOBREPOSICAO", "SELO DUPLO", "RÓTULO SOLTO", "SEM PALCO", "LINHA ÓRFÃ", "TRÂNSITO", "COR POR TOKEN",
           "CAIXA SEM LADO ESQUERDO", "OPACIDADE", "MARCADORES COLADOS"]
PAD = re.compile(r"^\[audit\]\s+([0-9.]+)s (.*)$")


def le(lote):
    ocs = defaultdict(list)
    f = U / f"log_aud_{lote}.txt"
    if not f.exists():
        return ocs
    for ln in f.read_text(encoding="utf-8", errors="replace").splitlines():
        m = PAD.match(ln)
        if not m:
            continue
        t, resto = float(m.group(1)), m.group(2)
        cls = next((c for c in CLASSES if resto.startswith(c)), resto.split(" ")[0])
        sig = resto[len(cls):]
        sig = re.sub(r"\([-0-9.; ]+\)", "", sig)                        # coordenadas
        sig = re.sub(r"\((folga|topo|base|y|x)[^)]*\)", "", sig)
        sig = re.sub(r"\s+", " ", sig).strip()
        ocs[(cls, sig)].append(t)
    return ocs


def intervalos(ts, gap=0.8):
    ts = sorted(set(ts))
    out, a, b = [], ts[0], ts[0]
    for t in ts[1:]:
        if t - b > gap:
            out.append((a, b))
            a = t
        b = t
    out.append((a, b))
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    top = int(args[args.index("--top") + 1]) if "--top" in args else 40
    so = args[args.index("--classe") + 1] if "--classe" in args else None
    lotes = [a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or args[i - 1] not in ("--top", "--classe"))]
    for lote in lotes:
        ocs = le(lote)
        tot = sum(len(v) for v in ocs.values())
        print(f"== {lote}: {tot} passadas, {len(ocs)} ocorrências únicas")
        por_cls = defaultdict(int)
        for (c, _), v in ocs.items():
            por_cls[c] += 1
        print("   " + " · ".join(f"{c} {n}" for c, n in sorted(por_cls.items(), key=lambda x: -x[1])))
        for (c, s), v in sorted(ocs.items(), key=lambda kv: -len(kv[1]))[:top]:
            if so and c != so:
                continue
            iv = ", ".join(f"{a:.1f}–{b:.1f}" for a, b in intervalos(v)[:4])
            print(f"   {len(v):5d}  {c} {s[:90]}  [{iv}]")
