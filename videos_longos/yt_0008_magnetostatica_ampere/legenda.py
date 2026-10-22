"""yt_0008 — legenda.srt (texto SEM tags, tempos de sync.json) + um .srt por capítulo + capitulos.txt (formato YouTube).

  uv run --no-sync python videos_longos/yt_0008_magnetostatica_ampere/legenda.py [DESLOC_S]
DESLOC_S: segundos somados a todos os tempos (se o vídeo final começar a voz com atraso em relação ao WAV; padrão 0).
Saída: legenda.srt (tempos absolutos) e legendas_capitulos/NN - nome.srt (tempos relativos ao início do capítulo).
"""
import json
import re
import sys
import textwrap
from pathlib import Path

P = Path(__file__).resolve().parent
S = json.loads((P / "sync.json").read_text(encoding="utf-8"))
DESL = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0
NOMES = {m.group(1): m.group(2).strip() for m in re.finditer(r"^## (B\d\d) — (.*?) \(", (P / "narracao_sugestao.md").read_text(encoding="utf-8"), re.M)}
NOMES["B00"] = "Abertura: o paradoxo do fio"


def srt_t(t):
    t = max(0.0, t)
    ms = round(t * 1000)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def cues():
    out, atual = [], []
    for k, (p, a, b) in enumerate(S["words"]):
        atual.append((p, a, b))
        txt = " ".join(w[0] for w in atual)
        fim_frase = p[-1] in ".?!…"
        quebra = len(txt) >= 80 or (p[-1] in ",:;" and len(txt) >= 42) or fim_frase
        if quebra or k == len(S["words"]) - 1:
            out.append([atual[0][1], atual[-1][2], txt])
            atual = []
    # duração: até o início da próxima fala (no máx. +0,4 s de resíduo), mínimo 1 s
    for i, c in enumerate(cues_ := out):
        prox = out[i + 1][0] if i + 1 < len(out) else c[1] + 1
        c[1] = min(max(c[1] + 0.25, c[0] + 1.0), prox - 0.04) if prox - c[0] > 0.3 else c[1]
    return out


def bloco(i, c, t0=0.0):
    linhas = textwrap.wrap(c[2], 42)
    if len(linhas) > 2:
        linhas = textwrap.wrap(c[2], 60)[:2]
    return f"{i}\n{srt_t(c[0] + DESL - t0)} --> {srt_t(c[1] + DESL - t0)}\n" + "\n".join(linhas) + "\n"


C = cues()
(P / "legenda.srt").write_text("\n".join(bloco(i + 1, c) for i, c in enumerate(C)), encoding="utf-8")
caps = S["capitulos"]
saida = P / "legendas_capitulos"
saida.mkdir(exist_ok=True)
for f in saida.glob("*.srt"):
    f.unlink()
yt = []
for n, cp in enumerate(caps):
    t0 = cp["t"]
    t1 = caps[n + 1]["t"] if n + 1 < len(caps) else 1e9
    sel = [c for c in C if t0 - 0.05 <= c[0] < t1 - 0.05]
    nome = NOMES.get(cp["bloco"], cp["bloco"])
    seguro = re.sub(r'[\/:*?"<>|]', "-", nome)
    (saida / f"{n:02d} - {seguro}.srt").write_text("\n".join(bloco(i + 1, c, t0) for i, c in enumerate(sel)), encoding="utf-8")
    t = round(t0 + DESL)
    yt.append(f"{t // 60}:{t % 60:02d} {nome}")
(P / "capitulos.txt").write_text("\n".join(yt) + "\n", encoding="utf-8")
print(len(C), "falas;", len(caps), "capítulos")
print("\n".join(yt))
