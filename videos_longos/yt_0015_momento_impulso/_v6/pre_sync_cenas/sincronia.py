"""yt_0015 — mapa da sincronia fina (padrão dos longos: alinhamento forçado, sem silêncio inserido na voz).

Entrada: audio/alinhamento_forcado_bruto.json (palavra a palavra), narracao_tags.md (v5.3, um parágrafo por âncora) e
narracao_sugestao_v4.md (o texto em que as frações `ate(f)` da cena foram pensadas).
Saída:
- sync/mapa.json: para cada âncora, o início S (1ª palavra − LEAD) e, para cada palavra da v4, o instante (s) da palavra
  correspondente na v5.3 (alinhamento de sequência v4 → v5.3 por difflib; trechos novos por interpolação). `ate(f)` cai na palavra
  f·n da v4 levada para a fala real; nas âncoras em V5 (refeitas na v6.1 em cima do texto v5.3) a fração vale direto na v5.3.
- ancoras.json: durações reais (S da próxima − S desta; a última vai até o fim da voz + FIM_EXTRA).
Uso: uv run --no-sync python sincronia.py
"""
import difflib
import json
import re
from pathlib import Path

AQUI = Path(__file__).resolve().parent
LEAD, FIM_EXTRA = 0.10, 1.8
V5 = {"E4-2", "E4-4"}                     # frações escritas já em cima do texto v5.3
# pontos presos a uma palavra da v5.3 (onde a v5.3 reordenou a frase e a fração da v4 cairia no lugar errado)
OVR = {"T4-2": {0.2: "pelo tempo da colisão", 0.45: "vai encolhendo", 0.62: "O que sobra"},
       "E2-3": {0.3: "a força média dá", 0.45: "Mas espera", 0.5: "e a força média encaixa", 0.62: "em cima dela",
                0.8: "A força não aponta"}}


def tok(s):
    return [re.sub(r"[^\w]", "", w.lower()) for w in s.split()]


def paragrafos(md, corte):
    src = (AQUI / md).read_text(encoding="utf-8")
    corpo = src.split("## HOOK", 1)[1].split(corte, 1)[0]
    out = []
    for aid, txt in re.findall(r"^### (\S+) — [^\n]*\n(.*?)(?=^### |^## |^---|\Z)", corpo, flags=re.M | re.S):
        fala = " ".join(l.strip() for l in txt.strip().splitlines() if l.strip() and not l.strip().startswith(">"))
        out.append((aid, re.sub(r"\[[^\]]*\]\s*", "", fala).strip()))
    return out


v5 = paragrafos("narracao_sugestao.md", "## Números de conferência")
v4 = dict(paragrafos("narracao_sugestao_v4.md", "## Números de conferência"))
ws = [w for w in json.loads((AQUI / "audio/alinhamento_forcado_bruto.json").read_text(encoding="utf-8"))["words"] if w["text"].strip()]
assert sum(len(t.split()) for _, t in v5) == len(ws), "palavras do alinhamento ≠ texto"
mapa, k = {}, 0
for aid, txt in v5:
    n5 = len(txt.split())
    t5 = [round(w["start"], 3) for w in ws[k:k + n5]]
    fim5 = ws[k + n5 - 1]["end"]
    k += n5
    a4 = tok(v4.get(aid, txt))
    a5 = tok(txt)
    idx = [None] * (len(a4) + 1)
    for blk in difflib.SequenceMatcher(None, a4, a5, autojunk=False).get_matching_blocks():
        for j in range(blk.size):
            idx[blk.a + j] = blk.b + j
    idx[len(a4)] = n5
    if idx[0] is None:
        idx[0] = 0
    ult = 0
    for i in range(len(idx)):                         # interpola o que não casou (monótono)
        if idx[i] is None:
            prox = next(j for j in range(i + 1, len(idx)) if idx[j] is not None)
            idx[i] = ult + (idx[prox] - ult) * (i - (i - 1)) / max(1, prox - (i - 1))
        ult = idx[i]
    tempos = []
    for i in range(len(a4) + 1):
        b = idx[i]
        j = min(int(b), n5 - 1)
        tt = t5[j] if j + 1 >= n5 else t5[j] + (b - int(b)) * (t5[j + 1] - t5[j])
        tempos.append(round(tt if b < n5 else fim5, 3))
    mapa[aid] = {"S": max(0.0, round(t5[0] - LEAD, 3)), "t4": tempos, "t5": t5 + [round(fim5, 3)], "v5": aid in V5}
    if aid in OVR:
        ovr = {}
        for f, frase in OVR[aid].items():
            ft = tok(frase)
            j = next(j for j in range(len(a5)) if a5[j:j + len(ft)] == ft)
            ovr[str(f)] = t5[j]
        mapa[aid]["ovr"] = ovr
ordem = [a for a, _ in v5]
fim_voz = ws[-1]["end"]
for i, a in enumerate(ordem):
    prox = mapa[ordem[i + 1]]["S"] if i + 1 < len(ordem) else fim_voz + FIM_EXTRA
    mapa[a]["dur"] = round(prox - mapa[a]["S"], 3)
(AQUI / "sync").mkdir(exist_ok=True)
(AQUI / "sync" / "mapa.json").write_text(json.dumps({"lead": LEAD, "ordem": ordem, "fim": round(fim_voz + FIM_EXTRA, 3), "ancoras": mapa},
                                                    ensure_ascii=False), encoding="utf-8")
anc = json.loads((AQUI / "ancoras.json").read_text(encoding="utf-8"))
for a in ordem:
    anc["ancoras"][a]["dur"] = mapa[a]["dur"]
anc["_sync"] = "durações reais da voz (sincronia.py, LEAD 0,10 s)"
(AQUI / "ancoras.json").write_text(json.dumps(anc, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{len(ordem)} âncoras; voz {fim_voz:.2f} s; vídeo {fim_voz + FIM_EXTRA:.2f} s")
for a in ("H1", "A1", "T1-1", "T3-1", "T5-1", "E1-1", "E4-1", "S1", "F2"):
    print(f"  {a:5s} S = {mapa[a]['S']:8.3f} s · dur {mapa[a]['dur']:6.2f} s")
