"""yt_0021 — auditoria ÁLGEBRA (estática): para cada âncora (self.an("X")), como cada linha da CONTA (variável criada por M(), eqf(), linha_m(), caixa_l())
entrou em cena: `construida` (monta / voa / passo com a linha como destino) ou `FadeIn` (entrou pronta). Marca as linhas de exercício (E1–E3) e das âncoras
de §3.1 que ainda entram por FadeIn. uso: python algebra21.py → renders/algebra.txt"""
import re
from pathlib import Path

U = Path(__file__).resolve().parent
ARQ = ["sec_t1.py", "sec_t2.py", "sec_t3.py", "sec_t4.py", "sec_t5.py", "sec_t6.py", "sec_e1.py", "sec_e2.py", "sec_e3.py", "sec_fim.py", "sec_abertura.py"]
out, tot = [], {"construida": 0, "FadeIn": 0}
por_ancora = {}
for arq in ARQ:
    anc = None
    linhas = (U / arq).read_text(encoding="utf-8").splitlines()
    nomes = {}
    for ln in linhas:
        m = re.search(r'self\.an\("([A-Z0-9-]+)"\)', ln)
        if m:
            anc = m.group(1)
        m = re.match(r"\s+([A-Za-z0-9_]+)\s*(?:,\s*[A-Za-z0-9_]+)?\s*=\s*(M|eqf|linha_m|caixa_l)\(", ln)
        if m and anc:
            nomes[m.group(1)] = anc
    est = {}
    anc = None
    for ln in linhas:
        m = re.search(r'self\.an\("([A-Z0-9-]+)"\)', ln)
        if m:
            anc = m.group(1)
            continue
        if not anc:
            continue
        for nome in nomes:
            if nomes[nome] != anc:
                continue
            pad = r"\b" + re.escape(nome) + r"\b"
            if re.search(r"self\.(monta|voa|passo)\(.*" + pad, ln) and not re.search(r"self\.(passo)\(" + pad + r",", ln):
                est[nome] = "construida"
            elif re.search(r"self\.passo\(\w+, " + pad, ln):
                est[nome] = "construida"
            elif re.search(r"FadeIn\((mp\()?" + pad, ln) and est.get(nome) != "construida":
                est[nome] = "FadeIn"
    for nome, e in est.items():
        por_ancora.setdefault(nomes[nome], []).append((nome, e))
        tot[e] += 1
for a, lst in por_ancora.items():
    out.append(f"{a:6s} " + " · ".join(f"{n}:{e}" for n, e in lst))
out.append("")
out.append(f"TOTAL linhas construídas {tot['construida']} · entradas por FadeIn {tot['FadeIn']}")
ex = {a: [n for n, e in l if e == "FadeIn"] for a, l in por_ancora.items() if a.startswith("E") and any(e == "FadeIn" for _, e in l)}
out.append("Exercícios com linha por FadeIn: " + (", ".join(f"{a}({'/'.join(v)})" for a, v in ex.items()) or "nenhuma"))
(U / "renders").mkdir(exist_ok=True)
(U / "renders" / "algebra.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
