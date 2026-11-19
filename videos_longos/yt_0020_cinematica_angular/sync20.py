"""yt_0020 v6 · sync.txt: para cada gat() do código (linha [gatilho] dos logs de auditoria), (âncora, frase, t_voz, t_imagem, delta).
t_voz = instante real (ASR) da 1ª palavra da frase dentro da âncora; t_imagem = instante em que a cena dispara o evento; delta = t_imagem − t_voz.
Janela aceita [−0,15; +0,20] s (negativo = imagem adiantada). uso: python sync20.py"""
import json
import re
from pathlib import Path

import numpy as np

U = Path(__file__).resolve().parent
anc = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
tok = lambda s: re.findall(r"\w+", s.lower())
linhas, viol = [], []
for log in sorted(U.glob("log_aud_P*.txt")):
    if log.stem.count("_") > 2:
        continue
    for ln in log.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"\[gatilho\] (\S+) ([\d.]+) (.*)", ln)
        if not m:
            continue
        aid, ti, fr = m.group(1), float(m.group(2)), m.group(3).strip()
        if aid not in anc:
            continue
        a = anc[aid]
        ft, ps = tok(a["fala"]), tok(fr)
        k = None
        for i in range(len(ft) - len(ps) + 1):
            if ft[i:i + len(ps)] == ps:
                k = i
                break
        if k is None:
            linhas.append((aid, fr, None, ti, None))
            continue
        tv = a["t"][k]
        d = ti - tv
        linhas.append((aid, fr, tv, ti, d))
        if d < -0.15 - 1e-6 or d > 0.20 + 1e-6:
            viol.append((aid, fr, tv, ti, d))
ds = np.array([l[4] for l in linhas if l[4] is not None])
out = ["# yt_0020 — sync.txt (preview v6, voz real)", "",
       f"gatilhos: {len(linhas)}; casados com a voz: {len(ds)}; sem par: {sum(1 for l in linhas if l[4] is None)}",
       f"delta médio {ds.mean():+.3f} s; mediana {np.median(ds):+.3f}; pior adiantado {ds.min():+.3f}; pior atrasado {ds.max():+.3f}",
       f"violações (fora de [−0,15; +0,20]): {len(viol)}", "", "histograma do delta (s):"]
bins = [-9, -0.5, -0.3, -0.15, -0.05, 0.05, 0.2, 0.5, 1.0, 9]
h, _ = np.histogram(ds, bins=bins)
for b0, b1, n in zip(bins[:-1], bins[1:], h):
    out.append(f"  [{b0:+.2f}; {b1:+.2f}) {n:4d} " + "#" * int(60 * n / max(h.max(), 1)))
out += ["", "## violações", "(âncora, palavra/frase, t_voz, t_imagem, delta)"]
out += [f"{a:6s} {t_v:8.2f} {t_i:8.2f} {d:+7.2f}  {f}" for a, f, t_v, t_i, d in sorted(viol, key=lambda x: -abs(x[4]))]
out += ["", "## todos os gatilhos", "(âncora, palavra/frase, t_voz, t_imagem, delta)"]
for a, f, t_v, t_i, d in linhas:
    out.append(f"{a:6s} {'—':>8} {t_i:8.2f} {'sem par':>8}  {f}" if d is None else f"{a:6s} {t_v:8.2f} {t_i:8.2f} {d:+7.2f}  {f}")
(U / "renders").mkdir(exist_ok=True)
(U / "renders" / "sync.txt").write_text("\n".join(out), encoding="utf-8")
print("\n".join(out[:12]))
