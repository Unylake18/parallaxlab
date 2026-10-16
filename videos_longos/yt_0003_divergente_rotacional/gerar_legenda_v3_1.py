"""Legenda do yt_0003: TEXTO do roteiro V3.1 (termos técnicos corretos) com os TEMPOS medidos pelo ASR (faster-whisper large-v3).

Cada palavra do roteiro é casada com a palavra reconhecida (difflib); palavras sem par recebem tempo interpolado entre as vizinhas
casadas. Cues: fim de frase/pausa, até 2 linhas de 42 caracteres, 1,2–6,5 s, sem sobreposição, na linha do tempo do vídeo final
(= áudio de montagem). Saída: legenda_yt0003.srt (+ legenda_yt0003_relatorio.json)."""
import difflib, json, re
from pathlib import Path
import numpy as np

P = Path(__file__).resolve().parent
NORM = lambda s: re.sub(r"[^\wáéíóúâêôãõàçü]", "", s.lower())
bl = []
md = (P / "narracao_v3_1.md").read_text(encoding="utf-8")
for m in re.finditer(r"### (\w+) — ([^\n]*)\n\*\*Evento visual[^:]*:\*\* ([^\n]*)\n\n> ([^\n]*)", md):
    bl.append(" ".join(re.sub(r"\*\*|\\(|\\)", "", m.group(4)).split()))
palavras = " ".join(bl).split()
A = json.loads((P / "asr_v3_1/transcricao_asr.json").read_text(encoding="utf-8"))
asr = [(NORM(w["word"]), w["start"], w["end"]) for s in A["segmentos"] for w in s["words"] if NORM(w["word"])]
alvo = [(NORM(w), i) for i, w in enumerate(palavras) if NORM(w)]
sm = difflib.SequenceMatcher(None, [a[0] for a in asr], [t[0] for t in alvo], autojunk=False)
ini = [None] * len(palavras); fim = [None] * len(palavras)
for blk in sm.get_matching_blocks():
    for k in range(blk.size):
        a = asr[blk.a + k]; i = alvo[blk.b + k][1]
        ini[i], fim[i] = a[1], a[2]
casadas = sum(x is not None for x in ini)
# interpola palavras sem par entre vizinhas casadas (por nº de caracteres)
i = 0
while i < len(palavras):
    if ini[i] is None:
        j = i
        while j < len(palavras) and ini[j] is None:
            j += 1
        t0 = fim[i - 1] if i > 0 and fim[i - 1] is not None else (ini[j] - 0.4 * (j - i) if j < len(palavras) else 0.0)
        t1 = ini[j] if j < len(palavras) else t0 + 0.4 * (j - i)
        pesos = np.array([len(palavras[k]) + 1 for k in range(i, j)], float)
        edges = t0 + np.concatenate([[0], np.cumsum(pesos)]) / pesos.sum() * max(t1 - t0, 0.12 * (j - i))
        for k in range(i, j):
            ini[k], fim[k] = float(edges[k - i]), float(edges[k - i + 1])
        i = j
    else:
        i += 1
# garante ordem não decrescente
for k in range(1, len(palavras)):
    if ini[k] < ini[k - 1]:
        ini[k] = ini[k - 1]
    if fim[k] < ini[k]:
        fim[k] = ini[k] + 0.05

def linhas(txt, largura=42):
    """Divide em até 2 linhas ≤ largura, equilibradas; None se não couber."""
    if len(txt) <= largura:
        return txt
    ws = txt.split(); melhor = None
    for k in range(1, len(ws)):
        l1, l2 = " ".join(ws[:k]), " ".join(ws[k:])
        if len(l1) <= largura and len(l2) <= largura:
            c = max(len(l1), len(l2))
            if melhor is None or c < melhor[0]:
                melhor = (c, l1 + chr(10) + l2)
    return melhor[1] if melhor else None

quebra_linhas = lambda t: linhas(t) or t

cues, cur_i = [], 0
def fecha(a, b):
    txt = " ".join(palavras[a:b + 1])
    cues.append([ini[a], fim[b], txt])
buf = []
for k, w in enumerate(palavras):
    buf.append(k)
    txt = " ".join(palavras[x] for x in buf)
    dur = fim[k] - ini[buf[0]]
    fim_frase = w[-1] in ".?!"
    virgula = w[-1] in ",;:" and len(txt) > 34
    gap = (ini[k + 1] - fim[k]) if k + 1 < len(palavras) else 9
    while linhas(txt) is None and len(buf) > 1:
        fecha(buf[0], buf[-2]); buf = [buf[-1]]; txt = palavras[buf[0]]
        dur = fim[k] - ini[buf[0]]
    if fim_frase or virgula or dur > 5.5 or gap > 0.7:
        fecha(buf[0], buf[-1]); buf = []
if buf:
    fecha(buf[0], buf[-1])
# tempos finais: sem sobreposição, duração mínima
for c in cues:
    c[0] = max(c[0] - 0.05, 0.0)
for n, c in enumerate(cues):
    nxt = cues[n + 1][0] if n + 1 < len(cues) else 1e9
    c[1] = min(max(c[1] + 0.15, c[0] + 1.0), nxt - 0.04)
def ts(t):
    return f"{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{t % 60:06.3f}".replace(".", ",")
srt = "\n".join(f"{n}\n{ts(a)} --> {ts(b)}\n{quebra_linhas(t)}\n" for n, (a, b, t) in enumerate(cues, 1))
(P / "legenda_yt0003.srt").write_text(srt, encoding="utf-8")
dmax = max(b - a for a, b, _ in cues)
n_linhas = max(len(quebra_linhas(t).split("\n")) for _, _, t in cues); larg = max(len(l) for _, _, t in cues for l in quebra_linhas(t).split("\n"))
rel = {"cues": len(cues), "palavras_roteiro": len(palavras), "palavras_com_tempo_do_asr": casadas, "pct": round(100 * casadas / len(palavras), 1),
       "maior_cue_s": round(dmax, 2), "max_linhas": n_linhas, "max_largura": larg, "sobreposicoes": sum(1 for x, y in zip(cues, cues[1:]) if y[0] < x[1]),
       "fim_ultimo_cue_s": round(cues[-1][1], 2)}
(P / "legenda_yt0003_relatorio.json").write_text(json.dumps(rel, indent=1), encoding="utf-8")
print(rel)
