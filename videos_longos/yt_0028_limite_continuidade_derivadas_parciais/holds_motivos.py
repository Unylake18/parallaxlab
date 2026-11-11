"""yt_0028 v4 (handoff v4 §8.7; v3 em v3_bak/): acrescenta o MOTIVO a cada trecho parado > 3 s do holds_v4.txt (qa_holds.py). uso: python holds_motivos.py"""
import re
from pathlib import Path

U = Path(__file__).resolve().parent
arq = U / "renders" / "v4" / "qa" / "holds_v4.txt"
GERAL = "a fala comenta o que acabou de entrar; o próximo elemento tem gatilho próprio logo adiante (entre dois gatilhos)"
LONGO = {
    "B6-2": "exceção aceita (handoff v4 §8.7): a matriz simbólica acaba de ser escrita e a fala lê as duas colunas antes de os valores voltarem",
    "B7-5": "exceção aceita (handoff v4 §8.7): TAMBÉM VALE (x² − y², −2xy) fica ≥ 4 s na tela, como o handoff v3 pede (B7-6), e a fala fecha o bloco",
    "S1": "exceção aceita (handoff v4 §8.7): resumo falado sobre a figura do resumo e o 1,5 s parado do E7 antes do CTA",
}
linhas = arq.read_text(encoding="utf-8").splitlines()
out = [linhas[0], "motivo de cada trecho (handoff v4 §8.7: nenhum > 6 s, salvo B6-2, B7-5 TAMBÉM VALE e o S):"]
for l in linhas[1:]:
    m = re.search(r"([0-9.]+) s\s+âncora (\S+)", l)
    if not m:
        continue
    dur, anc = float(m.group(1)), m.group(2)
    mot = LONGO.get(anc) if dur > 6.0 else GERAL
    out.append(f"{l}  → {'(> 6 s) ' if dur > 6 else ''}{mot or GERAL}")
arq.write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(o for o in out if "(> 6 s)" in o))
