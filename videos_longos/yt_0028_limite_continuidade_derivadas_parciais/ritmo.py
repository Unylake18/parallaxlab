"""yt_0028 final §5.3: lê os logs dos lotes (log_<L>.txt) e atualiza ritmo.json (fator por trecho entre gatilhos, ver v28.py). Um trecho cujo
gatilho seguinte chegou mais de 0,1 s atrasado, ou cuja âncora seguinte estourou, encolhe: fator ← fator · (D − E)/D (piso 0,35).
uso: python ritmo.py [prefixo do log]   (rodar, re-renderizar os lotes afetados, repetir até não sobrar atraso)"""
import json
import re
import sys
from pathlib import Path

U = Path(__file__).resolve().parent
PRE = sys.argv[1] if len(sys.argv) > 1 else "log_"
R = json.loads((U / "ritmo.json").read_text(encoding="utf-8")) if (U / "ritmo.json").is_file() else {}
mud = []
for lote in ["PH", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PB7", "PS"]:
    log = (U / f"{PRE}{lote}.txt").read_text(encoding="utf-8", errors="replace").splitlines()
    aid, t_an, n, ult, pend, herd = None, 0.0, 0, 0.0, None, 0.0
    for l in log:
        m = re.match(r"\[estouro\] (\S+) começou ([0-9.]+)s", l)
        if m and aid:
            pend = float(m.group(2))
        m = re.match(r"\[ancora\] (\S+) ([0-9.]+)", l)
        if m:
            t = float(m.group(2))
            if pend and aid:
                D = t - t_an - ult
                E = pend + 0.05
                f0 = R.setdefault(aid, {}).get(str(n), 1.0)
                f = max(0.35, f0 * max(0.0, D - E) / D) if D > 0.3 else f0
                R[aid][str(n)] = round(f, 3)
                mud.append(f"{aid} trecho {n} (até o fim; estouro {pend:.2f} s em {D:.2f} s): {f0:.2f} → {f:.2f}")
            pend = None
            aid, t_an, n, ult, herd = m.group(1), t, 0, 0.0, 0.0
            continue
        m = re.match(r"\[gatilho\] (\S+)\s+([-0-9.]+)s \(alvo\s+([-0-9.]+)s, atraso ([-+0-9.]+)s\) (.*)", l)
        if m:
            rel, alvo = float(m.group(2)), float(m.group(3))
            E = rel - alvo - herd                # só o excesso do PRÓPRIO trecho (o atraso herdado do anterior se resolve lá)
            herd = max(0.0, rel - alvo)
            if E > 0.1:
                D = rel - ult
                f0 = R.setdefault(aid, {}).get(str(n), 1.0)
                f = max(0.35, f0 * max(0.0, D - E - 0.05) / D) if D > 0.3 else f0
                R[aid][str(n)] = round(f, 3)
                mud.append(f"{aid} trecho {n} → «{m.group(5)}» (atraso {E:.2f} s em {D:.2f} s): {f0:.2f} → {f:.2f}")
            n += 1
            ult = max(rel, alvo)
(U / "ritmo.json").write_text(json.dumps(R, ensure_ascii=False, indent=1), encoding="utf-8")
print("\n".join(mud) or "nada a mudar")
print(len(mud), "trechos ajustados")
