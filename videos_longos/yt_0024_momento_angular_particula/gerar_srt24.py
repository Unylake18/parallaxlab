"""yt_0024: legenda .srt a partir do texto da narração (narracao_tags.md, SEM as tags [ ]) e dos tempos reais das palavras (ancoras.json: t[k] relativo à âncora).
O vídeo começa junto com o WAV, então o tempo da voz é o do vídeo. Cada bloco tem até 2 linhas de ~42 caracteres e até 5,5 s; quebra em fim de frase ou em vírgula.
uso: python gerar_srt21.py [saida.srt]"""
import json
import re
import sys
from pathlib import Path

U = Path(__file__).resolve().parent
SAIDA = Path(sys.argv[1]) if len(sys.argv) > 1 else U / "renders" / "legenda_yt0024.srt"
AL = json.loads((U / "alinhamento_palavras.json").read_text(encoding="utf-8"))     # uma entrada por palavra \w+ do texto: start/end ABSOLUTOS na voz
texto = (U / "narracao_tags.md").read_text(encoding="utf-8")
corpo = texto.split("## Texto corrido (para gravação)", 1)[1]
limpo = " ".join(re.sub(r"\[[^\]]*\]", "", corpo).split())
toks, k = [], 0                                  # (texto, início, fim) em segundos do vídeo (o vídeo começa junto com o WAV)
for tk in limpo.split():
    n = len(re.findall(r"\w+", tk))
    if n == 0 and toks:
        toks[-1] = (toks[-1][0] + " " + tk, toks[-1][1], toks[-1][2])
        continue
    n = max(n, 1)
    ini = AL[min(k, len(AL) - 1)]["start"]
    prox = AL[k + n]["start"] if k + n < len(AL) else AL[-1]["end"]
    fim = max(ini + 0.12, prox - 0.04)
    k += n
    toks.append((tk, ini, fim))
assert k == len(AL), (k, len(AL))

cues, atual = [], []


def fecha():
    global atual
    if atual:
        cues.append(atual)
        atual = []


for i, (tk, a, b) in enumerate(toks):
    atual.append((tk, a, b))
    txt = " ".join(x[0] for x in atual)
    dur = b - atual[0][1]
    fim_frase = bool(re.search(r"[.?!…]$", tk))
    virgula = bool(re.search(r"[,:;]$", tk))
    gap = (toks[i + 1][1] - b) if i + 1 < len(toks) else 9
    if fim_frase or len(txt) >= 84 or dur >= 5.5 or (virgula and len(txt) >= 46) or gap > 0.9:
        fecha()
fecha()


def duas_linhas(t):
    if len(t) <= 42:
        return t
    pal = t.split()
    melhor, dif = 1, 1e9
    for j in range(1, len(pal)):
        d = abs(len(" ".join(pal[:j])) - len(" ".join(pal[j:])))
        if d < dif:
            melhor, dif = j, d
    return " ".join(pal[:melhor]) + "\n" + " ".join(pal[melhor:])


def tc(s):
    s = max(0.0, s)
    h, r = divmod(s, 3600)
    m, r = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(r):02d},{int(round((r - int(r)) * 1000)):03d}"


linhas = []
for n, c in enumerate(cues, 1):
    ini, fim = c[0][1], c[-1][2]
    if n < len(cues):
        fim = min(fim + 0.15, cues[n][0][1] - 0.02)
    linhas.append(f"{n}\n{tc(ini)} --> {tc(fim)}\n{duas_linhas(' '.join(x[0] for x in c))}\n")
SAIDA.write_text("\n".join(linhas), encoding="utf-8")
print(len(cues), "cues;", tc(cues[-1][-1][2]), "último fim")
