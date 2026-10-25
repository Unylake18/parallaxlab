"""Divide o alinhamento forçado (ElevenLabs, por palavra) nas âncoras ### de narracao_sugestao.md -> alinhamento_forcado.json."""
import json, re
from pathlib import Path

P = Path(__file__).resolve().parent
src = (P.parent / "narracao_sugestao.md").read_text(encoding="utf-8").split("## Notas para a sincronização")[0]
blocos = re.findall(r"^### (\S+) — [^\n]*\n(.*?)(?=^### |^## |^---|\Z)", src, flags=re.M | re.S)
cel = []
for aid, txt in blocos:
    falas = [l.strip() for l in txt.strip().splitlines() if l.strip() and not l.strip().startswith("(")]
    if falas:
        cel.append((aid, " ".join(falas).split()))
bruto = json.loads((P / "alinhamento_forcado_bruto.json").read_text(encoding="utf-8"))
ws = [w for w in bruto["words"] if w["text"].strip()]
assert len(ws) == sum(len(p) for _, p in cel), (len(ws), sum(len(p) for _, p in cel))
saida, i = [], 0
for aid, pal in cel:
    seg = ws[i:i + len(pal)]
    i += len(pal)
    saida.append({"chave": aid, "palavras": [[p, round(w["start"], 2), round(w["end"], 2)] for p, w in zip(pal, seg)]})
(P / "alinhamento_forcado.json").write_text(json.dumps({"loss": bruto["loss"], "celulas": saida}, ensure_ascii=False, indent=0), encoding="utf-8")
for c in saida:
    print(f'{c["chave"]:7s} {c["palavras"][0][1]:7.2f} {c["palavras"][-1][2]:7.2f}  {" ".join(p[0] for p in c["palavras"][:6])}')
