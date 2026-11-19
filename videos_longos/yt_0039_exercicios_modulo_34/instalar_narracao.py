"""yt_0039 handoff final §4.1: monta narracao.md (v3.1) = Tela da v1 + Gatilhos e parágrafo da v3.1; confere gatilhos; gera narracao_tags.md e narracao_limpa.md."""
import re
import shutil
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
V31 = Path(sys.argv[1])  # yt_0039_narracao_v3_1.md
v1 = (AQUI / "narracao_v1.md").read_text(encoding="utf-8")
v3 = V31.read_text(encoding="utf-8")


def blocos(t):
    d, ordem = {}, []
    for b in re.split(r"^### ", t, flags=re.M)[1:]:
        cab, *res = b.split("\n")
        if cab.startswith("Tempo por"):
            continue
        aid = cab.split(" · ")[0].strip()
        d[aid] = (cab, res)
        ordem.append(aid)
    return d, ordem


b1, o1 = blocos(v1)
b3, o3 = blocos(v3)
assert o1 == o3 and len(o3) == 28, (o1, o3)
tok = lambda s: re.findall(r"\w+", s.lower())  # noqa: E731
saida = ["# yt_0039 · CÁLCULO III · EP. 14 · Exercícios do módulo: jacobiano, polares e centro de massa",
         "## Narração v3.1 · por âncora, com a Tela (da v1) e os Gatilhos e a fala (da v3.1)", ""]
tags, limpa, tot, ok, falt = [], [], 0, 0, 0
for a in o3:
    cab3, r3 = b3[a]
    _, r1 = b1[a]
    tela = [l for l in r1 if l.startswith("**Tela:**") or l.startswith("Canto:")]
    gat = [l for l in r3 if l.startswith("**Gatilhos:**")]
    fala = " ".join(l[1:].strip() for l in r3 if l.startswith(">"))
    assert tela and gat and fala, a
    saida += [f"### {cab3}"] + tela + gat + ["> " + fala, ""]
    tags.append(fala)
    sem = re.sub(r"\[[^\]]*\]", "", fala)
    sem = " ".join(sem.split())
    limpa.append(sem)
    tk = tok(sem)
    tot += len(tk)
    pos = 0
    for f in re.findall(r"\"([^\"]+)\"", gat[0]):
        ft = tok(f)
        n = len(ft)
        achou = next((i for i in range(pos, len(tk) - n + 1) if tk[i:i + n] == ft), -1)
        if achou < 0:
            falt += 1
            print("FALTA", a, repr(f))
        else:
            ok += 1
            pos = achou
print(f"âncoras {len(o3)} · frases {ok}/{ok + falt} · faltando {falt} · palavras {tot}")
shutil.copy(AQUI / "narracao_v1.md", AQUI / "narracao_v1_historico.md") if not (AQUI / "narracao_v1_historico.md").exists() else None
(AQUI / "narracao.md").write_text("\n".join(saida), encoding="utf-8")
(AQUI / "narracao_tags.md").write_text("# yt_0039 · narração com tags ElevenLabs v4 (v3.1)\n\n## Texto corrido (para gravação)\n\n" + "\n\n".join(tags) + "\n", encoding="utf-8")
(AQUI / "narracao_limpa.md").write_text("# yt_0039 · narração limpa (v3.1)\n\n" + "\n\n".join(limpa) + "\n", encoding="utf-8")
