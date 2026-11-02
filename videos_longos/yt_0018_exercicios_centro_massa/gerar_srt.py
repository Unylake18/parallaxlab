"""yt_0018: legenda .srt a partir do texto da narração (narracao_tags_v1_4.md) e dos tempos das palavras da voz contínua (audio/voz7_tempos.json).
Cada bloco tem até 2 linhas de ~42 caracteres e até 6 s; quebra em fim de frase ou em vírgula. O vídeo começa junto com o WAV, então o tempo da voz é o do vídeo.
uso: python gerar_srt.py [saida.srt]"""
import json
import re
import sys
from pathlib import Path

U = Path(__file__).resolve().parent
SAIDA = Path(sys.argv[1]) if len(sys.argv) > 1 else U / "renders" / "legenda_yt0018.srt"
T = json.loads((U / "audio" / "voz7_tempos.json").read_text(encoding="utf-8"))["ancoras"]
ordem = json.loads((U / "ancoras_nominal.json").read_text(encoding="utf-8"))["ordem"]
texto = (U / "narracao_tags_v1_4.md").read_text(encoding="utf-8")
corpo = texto[texto.index("## Texto corrido (para gravação)"):].split("\n", 1)[1]
linhas = [l.strip() for l in corpo.splitlines() if l.strip()]
assert len(linhas) == len(ordem)

toks = []                                        # (texto, início, fim)
for aid, linha in zip(ordem, linhas):
    limpo = " ".join(re.sub(r"\[[^\]]*\]", "", linha).replace("**", "").split())
    pal = T[aid]
    k = 0
    atual = None
    for tk in limpo.split():
        n = len(re.findall(r"\w+", tk))
        if n == 0 and toks:                      # pontuação solta: cola na anterior
            toks[-1] = (toks[-1][0] + " " + tk, toks[-1][1], toks[-1][2])
            continue
        ini = pal[k]["t"]
        fim = pal[min(k + n, len(pal)) - 1]["e"]
        k += n
        toks.append((tk, ini, fim))
assert toks

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
    proximo_gap = (toks[i + 1][1] - b) if i + 1 < len(toks) else 9
    if fim_frase or len(txt) >= 84 or dur >= 5.5 or (virgula and len(txt) >= 46) or proximo_gap > 0.9:
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


out = []
for k, c in enumerate(cues):
    ini = c[0][1]
    fim = c[-1][2] + 0.25
    if k + 1 < len(cues):
        fim = min(fim, cues[k + 1][0][1] - 0.04)
    fim = max(fim, ini + 0.4)
    out.append(f"{k + 1}\n{tc(ini)} --> {tc(fim)}\n{duas_linhas(' '.join(x[0] for x in c))}\n")
SAIDA.write_text("\n".join(out), encoding="utf-8")
print(f"{len(cues)} blocos → {SAIDA}")
