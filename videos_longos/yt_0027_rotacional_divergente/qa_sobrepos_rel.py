"""yt_0027 v3 (handoff v3 R5): junta as linhas [sobrepos] dos logs do render (QA_SOBREPOS=1; checagem em cada gatilho e no fim de cada âncora)
em renders/<rodada>/qa/sobreposicoes_<rodada>.txt. uso: python qa_sobrepos_rel.py [rodada]"""
import re
import sys
from pathlib import Path

U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "v3"
LOTES = ["PHA", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PF", "PB7", "PS"]
linhas, n_chk, resumo = [], 0, []
for L in LOTES:
    arq = U / f"log_sob_{L}.txt"          # passagem seca com QA_SOBREPOS=1 (o render usa os mesmos gatilhos)
    t = (arq if arq.exists() else U / f"log_{L}.txt").read_text(encoding="utf-8", errors="replace")
    chk = re.findall(r"^\[sobrepos-chk\] .*: (\d+) textos, (\d+) setas", t, re.M)
    n_chk += len(chk)
    n_tx = sum(int(a) for a, _ in chk); n_st = sum(int(b) for _, b in chk)
    resumo.append(f"  {L}: {len(chk)} checagens; {n_tx} textos e {n_st} setas visíveis somados")
    linhas += [f"{L}  {m}" for m in re.findall(r"^\[sobrepos\] (.*)$", t, re.M)]
out = [f"yt_0027 {R} · R5 (sobreposição): {n_chk} checagens (cada gatilho e o fim de cada âncora, nos 10 lotes)",
       "critério: caixas de texto/MathTex não se cruzam; nenhuma seta de campo visível com o centro dentro da caixa de um texto (+4 px)",
       *resumo, f"OCORRÊNCIAS: {len(linhas)}", *[f"  {l}" for l in linhas]]
# R6 (v4): amostras a cada 0,2 s durante o render; ocorrências seguidas iguais viram um trecho
r6, amostras = [], 0
for L in LOTES:
    t = (U / f"log_{L}.txt").read_text(encoding="utf-8", errors="replace")
    m_ = re.search(r"\[tempo\] total ([0-9.]+)s", t)
    amostras += int(float(m_.group(1)) / 0.2) if m_ else 0
    tr = {}
    for m in re.finditer(r"^\[r6\] (\S+)\s+([0-9.]+)s (\S+): (.*)$", t, re.M):
        k = (m.group(3), m.group(4))
        tt = float(m.group(2))
        if k in tr and tt - tr[k][-1][1] <= 0.21:
            tr[k][-1][1] = tt
        else:
            tr.setdefault(k, []).append([tt, tt])
    for (aid, msg), lst in tr.items():
        for a0, a1 in lst:
            r6.append(f"  {L} {aid} {a0:7.2f}–{a1:7.2f}s ({a1 - a0 + 0.2:.1f} s): {msg}")
out += ["", f"R6 (v4): amostragem a cada 0,2 s DURANTE o render, inclusive em Transform/FadeIn/FadeOut: ~{amostras} amostras nos 10 lotes",
        "critério: texto×texto (+4 px), seta de campo com o centro numa caixa de texto (+4 px) ou cruzando a caixa, imagem sobre seta de campo, DUPLICATA de MathTex",
        f"TRECHOS COM OCORRÊNCIA: {len(r6)}", *sorted(r6)]
if any("0{,}219" in l or "0{,}927" in l for l in r6):
    out += ["", "JUSTIFICATIVA (R6, DUPLICATA no B5-2/B5-3): é intencional, como no alvo b52bv3. O 0,219 aparece nas duas paredes horizontais da caixa "
            "(o mesmo fluxo em cima e embaixo, por simetria). O 0,927 aparece junto da parede de entrada e na coluna, em ENTRA. Não são linhas empilhadas "
            "nem cópias esquecidas. Na passagem B5-2 → B5-3 eles somem junto com a caixa (0,2 a 0,4 s de fade)."]
(U / "renders" / R / "qa").mkdir(parents=True, exist_ok=True)
(U / "renders" / R / "qa" / f"sobreposicoes_{R}.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out[:60]))
