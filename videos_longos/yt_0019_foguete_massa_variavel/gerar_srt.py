"""yt_0019 v10: legenda .srt a partir da narração (narracao_v10.md, sem as tags) e dos instantes de cada palavra no WAV final (audio/voz10_tempos.json).
Cada token separado por espaço herda o início da sua primeira palavra e o fim da última; as falas são agrupadas em cues de até 2 linhas × 42 caracteres, quebrando
em pontuação quando possível, no máximo 6,5 s por cue. A pontuação e a grafia ficam como no texto (Tsiolkovsky etc.).
uso: python gerar_srt.py → renders/legenda - yt0019.srt"""
import json
import re
from pathlib import Path

U = Path(__file__).resolve().parent
T = json.loads((U / "audio" / "voz10_tempos.json").read_text(encoding="utf-8"))["ancoras"]
ordem = json.loads((U / "ancoras_nominal_v10.json").read_text(encoding="utf-8"))["ordem"]
texto = {}
aid = None
for l in (U / "narracao_v10.md").read_text(encoding="utf-8").splitlines():
    if l.startswith("### "):
        aid = l[4:].strip(); texto[aid] = []
    elif aid and l.strip() and not l.startswith("#"):
        texto[aid].append(l.strip())
toks = []                                     # (texto do token, início, fim)
for a in ordem:
    linha = re.sub(r"\[[^\]]*\]", " ", " ".join(texto[a]))
    pal = T[a]
    k = 0
    for tok in linha.split():
        n = len(re.findall(r"\w+", tok))
        if n == 0:
            if toks:
                toks[-1] = (toks[-1][0] + " " + tok, toks[-1][1], toks[-1][2])
            continue
        toks.append((tok, pal[k]["t"], pal[k + n - 1]["e"]))
        k += n
    assert k == len(pal), (a, k, len(pal))
MAXC, MAXD = 42, 6.5
cues, atual = [], []
def tamanho(ts):
    return len(" ".join(t[0] for t in ts))
def fecha():
    global atual
    if atual:
        cues.append(atual); atual = []
for i, t in enumerate(toks):
    if atual and (tamanho(atual + [t]) > 2 * MAXC or t[2] - atual[0][1] > MAXD or t[1] - atual[-1][2] > 0.9):
        fecha()
    if t[0].startswith('Lab') and atual and atual[-1][0] == 'Parallax' and len(atual) > 1:      # nunca separa 'Parallax' de 'Lab'
        p_ = atual.pop(); fecha(); atual.append(p_)
    atual.append(t)
    if re.search(r"[.?!:…]$", t[0]) and tamanho(atual) > 22:
        fecha()
    elif re.search(r"[,;]$", t[0]) and tamanho(atual) > 0.8 * 2 * MAXC:
        fecha()
fecha()
for i_ in range(1, len(cues)):                                           # nunca separa 'Parallax' de 'Lab'
    if cues[i_][0][0].startswith('Lab') and cues[i_ - 1][-1][0] == 'Parallax' and len(cues[i_ - 1]) > 1:
        cues[i_].insert(0, cues[i_ - 1].pop())
def ts(x):
    ms = int(round(x * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
def quebra(txt):
    if len(txt) <= MAXC:
        return txt
    pal = txt.split(); melhor = None
    for i in range(1, len(pal)):
        a, b = " ".join(pal[:i]), " ".join(pal[i:])
        if len(a) <= MAXC and len(b) <= MAXC:
            d = abs(len(a) - len(b))
            if melhor is None or d < melhor[0]:
                melhor = (d, a + "\n" + b)
    return melhor[1] if melhor else txt
out = []
for n, c in enumerate(cues, 1):
    ini = max(0.0, c[0][1] - 0.05)
    fim = c[-1][2] + 0.12
    if n < len(cues):
        fim = min(fim, cues[n][0][1] - 0.07)
    out.append(f"{n}\n{ts(ini)} --> {ts(fim)}\n{quebra(' '.join(t[0] for t in c))}\n")
(U / "renders" / "legenda - yt0019.srt").write_text("\n".join(out), encoding="utf-8")
print(len(cues), "cues;", sum(len(t[0]) for t in toks), "caracteres")
