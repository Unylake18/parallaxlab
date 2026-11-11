"""yt_0028 (copiado do yt_0027; handoff v1.2 §8.2: a seta INTEIRA, haste e ponta, + 4 px): junta as linhas [sobrepos] dos logs do render (QA_SOBREPOS=1; checagem em cada gatilho e no fim de cada âncora)
em renders/<rodada>/qa/sobreposicoes_<rodada>.txt. uso: python qa_sobrepos_rel.py [rodada]"""
import re
import sys
from pathlib import Path

U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "v1"
LOTES = ["PH", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PB7", "PS"]
linhas, n_chk, resumo = [], 0, []
for L in LOTES:
    arq = U / f"log_sob_{L}.txt"          # passagem seca com QA_SOBREPOS=1 (o render usa os mesmos gatilhos)
    t = (arq if arq.exists() else U / f"log_{L}.txt").read_text(encoding="utf-8", errors="replace")
    chk = re.findall(r"^\[sobrepos-chk\] .*: (\d+) textos, (\d+) setas", t, re.M)
    n_chk += len(chk)
    n_tx = sum(int(a) for a, _ in chk); n_st = sum(int(b) for _, b in chk)
    resumo.append(f"  {L}: {len(chk)} checagens; {n_tx} textos e {n_st} setas visíveis somados")
    linhas += [f"{L}  {m}" for m in re.findall(r"^\[sobrepos\] (.*)$", t, re.M)]
out = [f"yt_0028 {R} · R5 (sobreposição): {n_chk} checagens (cada gatilho e o fim de cada âncora, nos 9 lotes)",
       "critério: caixas de texto/MathTex não se cruzam; nenhuma seta de campo visível cruza a caixa de um texto, medindo a seta INTEIRA (haste e ponta: 24 amostras por segmento) com margem de 4 px + meia espessura",
       *resumo, f"OCORRÊNCIAS: {len(linhas)}", *[f"  {l}" for l in linhas]]
(U / "renders" / R / "qa").mkdir(parents=True, exist_ok=True)
(U / "renders" / R / "qa" / f"sobreposicoes_{R}.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out[:60]))
