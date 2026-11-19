"""yt_0021 v9: renders/sync.txt — para cada gatilho `gat()` do código: (âncora, palavra, t_voz, t_imagem, delta).
t_voz = início da 1ª palavra da frase (ancoras.json, voz real); t_imagem = instante em que o evento começa (log `[gatilho]`, relativo à âncora).
O kit começa o evento LEAD = 0,12 s antes da palavra, então o delta esperado é ≈ −0,12 s. Janela do handoff v8 §7: −0,15 … +0,20 s.
Saída também: histograma, delta médio, pior caso e as violações. uso: python sync21.py"""
import json
import os
import re
import statistics
from pathlib import Path

U = Path(__file__).resolve().parent
ANC = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
LOTES = ["PH", "PA", "PT1", "PT2", "PT3", "PT4", "PT5", "PT6", "PE1", "PE2", "PE3", "PS"]
LO, HI = -0.15, 0.20
lin, viol, sem = [], [], []
for lote in LOTES:
    log = (U / f"{os.environ.get('LOGPFX', 'log_')}{lote}.txt").read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"^\[gatilho\] (\S+) ([0-9.]+) (.*)$", log, flags=re.M):
        aid, t_img, frase = m.group(1), float(m.group(2)), m.group(3).strip()
        a = ANC[aid]
        fala = a["fala"].split()
        alvo = re.findall(r"\w+", frase.lower())
        k = next((i for i in range(len(fala)) if fala[i:i + len(alvo)] == alvo), None)
        if k is None:
            sem.append((aid, frase))
            continue
        t_voz = a["t"][k]
        d = t_img - t_voz
        lin.append((aid, frase, t_voz, t_img, d, lote))
        if not (LO <= d <= HI):
            viol.append((aid, frase, t_voz, t_img, d, lote))
ds = [x[4] for x in lin]
out = [f"SYNC yt_0021 v9 — {len(lin)} gatilhos; janela [{LO:+.2f}; {HI:+.2f}] s; delta = t_imagem − t_voz (esperado ≈ −0,12)",
       f"delta médio {statistics.mean(ds):+.3f} s · mediana {statistics.median(ds):+.3f} · mínimo {min(ds):+.3f} · máximo {max(ds):+.3f}",
       f"VIOLAÇÕES: {len(viol)} · gatilhos sem frase no texto: {len(sem)}", "", "histograma (delta, s):"]
bins = [(-9, -0.5), (-0.5, -0.3), (-0.3, -0.15), (-0.15, -0.05), (-0.05, 0.05), (0.05, 0.2), (0.2, 0.5), (0.5, 1.0), (1.0, 99)]
for a_, b_ in bins:
    n = sum(1 for d in ds if a_ <= d < b_)
    out.append(f"  [{a_:+.2f}; {b_:+.2f}) {n:4d} {'#' * min(60, n)}")
out += ["", "violações (âncora · frase · t_voz · t_imagem · delta):"]
out += [f"  {a:6s} {f[:55]:55s} {tv:7.2f} {ti:7.2f} {d:+.2f}  ({lt})" for a, f, tv, ti, d, lt in sorted(viol, key=lambda x: -abs(x[4]))]
out += ["", "sem frase:"] + [f"  {a} {f}" for a, f in sem]
out += ["", "todos:"] + [f"  {a:6s} {f[:55]:55s} {tv:7.2f} {ti:7.2f} {d:+.2f}" for a, f, tv, ti, d, lt in lin]
(U / "renders" / os.environ.get("SYNCOUT", "sync.txt")).write_text("\n".join(out), encoding="utf-8")
print("\n".join(out[:20]))
