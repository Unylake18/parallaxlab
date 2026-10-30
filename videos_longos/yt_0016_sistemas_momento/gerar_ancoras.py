"""v5: âncoras pela voz real. narracao_final_v4.md (texto de cada âncora) + alinhamento_palavras.json (forced alignment da
audio/narracao_v4.wav) → ancoras.json. Cada âncora começa LEAD = 0,15 s antes da primeira palavra da sua fala; a duração vai até o
começo da seguinte (a última ganha CAUDA s de cartão final). PAD: deslocamento da voz no vídeo (a âncora H1 começa em 0).
Cada âncora leva também as palavras (normalizadas) com o instante no vídeo, para a sincronia fina (Base.diz).
(v4 e anteriores: duração nominal de 2,7 palavras/s; ver _v4/gerar_ancoras.py.)"""
import json
import re
import unicodedata
from pathlib import Path

AQUI = Path(__file__).resolve().parent
LEAD, CAUDA = 0.15, 2.4


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c) and (c.isalnum()))


t = (AQUI / "narracao_final_v4.md").read_text(encoding="utf-8")
t = t[:t.rindex("## Números de conferência")]
blocos = []
for bloco in re.split(r"^### ", t, flags=re.M)[1:]:
    cab, *resto = bloco.split("\n")
    aid = cab.split(" — ")[0].strip()
    fala = " ".join(l for l in resto if l.strip() and not l.startswith(("---", "## ")))
    fala = re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", "", fala)).strip()
    blocos.append((aid, fala.split(" ")))
al = json.loads((AQUI / "alinhamento_palavras_v6.json").read_text(encoding="utf-8"))
n_txt = sum(len(p) for _, p in blocos)
assert n_txt == len(al), (n_txt, len(al))
k = 0
for (aid, pal) in blocos:
    for w in pal:
        assert norm(w) == norm(al[k]["word"]), (aid, w, al[k]["word"])
        k += 1
PAD = LEAD - al[0]["start"]
fim_voz = al[-1]["end"] + PAD
out, ordem, k = {}, [], 0
for aid, pal in blocos:
    ws = al[k:k + len(pal)]
    k += len(pal)
    out[aid] = {"t0": round(ws[0]["start"] + PAD - LEAD, 3), "palavras": [[norm(w["word"]), round(w["start"] + PAD, 3)] for w in ws],
                "fim_fala": round(ws[-1]["end"] + PAD, 3), "n": len(pal)}
    ordem.append(aid)
for a, b in zip(ordem, ordem[1:]):
    out[a]["dur"] = round(out[b]["t0"] - out[a]["t0"], 3)
out[ordem[-1]]["dur"] = round(fim_voz + CAUDA - out[ordem[-1]]["t0"], 3)
out[ordem[0]]["t0"] = 0.0
total = out[ordem[-1]]["t0"] + out[ordem[-1]]["dur"]
(AQUI / "ancoras.json").write_text(json.dumps({"ordem": ordem, "pad": round(PAD, 3), "total": round(total, 3), "ancoras": out},
                                              ensure_ascii=False, indent=0), encoding="utf-8")
print(f"{len(ordem)} âncoras; PAD {PAD:+.3f} s; vídeo {total:.2f} s ({int(total // 60)}:{total % 60:05.2f})")
for a in ordem:
    m, s = divmod(out[a]["t0"], 60)
    print(f"{int(m)}:{s:05.2f} {a} {out[a]['dur']:.2f} s ({out[a]['n']} palavras)")
