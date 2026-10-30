"""v6 (handoff v6 §1): respiro na voz sem gerar voz nova. audio/narracao_v4.wav + alinhamento_palavras.json → audio/narracao_v4_pausas.wav
(silêncio digital inserido entre palavras, no ponto mais quieto do intervalo, com fade de 10 ms nas duas emendas) e
alinhamento_palavras_v6.json (tempos das palavras somados ao deslocamento acumulado). Lista das inserções em log_pausas_v6.txt.
Regras: virada de capítulo +1,0 s (H3→A1 +0,6 s); demais viradas de âncora +BASE; depois de cada resultado +0,5 s; pergunta retórica
no meio da âncora +0,4 s (inserções no mesmo intervalo somam, até 1,2 s)."""
import json
import re
import sys
import unicodedata
import wave
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
BASE = float(sys.argv[1]) if len(sys.argv) > 1 else 0.35
CAP = {("A6", "T7-1"), ("T7-9", "T8-1"), ("T8-8", "T9-1"), ("T9-7", "T10-1"), ("T10-4", "E6-1"), ("E6-4", "E7-1"), ("E7-5", "E8-1"),
       ("E8-4", "E9-1"), ("E9-7", "C-1"), ("C-3", "S1"), ("S2", "EN1")}
RES = [("T8-3", "metros por segundo ao quadrado"), ("T8-4", "Fecha certinho"), ("T8-6", "até parar"),
       ("T9-2", "menos vinte e quatro metros por segundo"), ("T9-6", "ele volta a zero"), ("T10-3", "ficam com o mais leve"),
       ("E6-2", "Bem devagarinho"), ("E6-3", "quase o dobro"), ("E7-2", "dá para ver"), ("E7-4", "três centímetros por segundo"),
       ("E7-5", "massa da bala"), ("E8-3", "a soma dá zero"), ("E9-6", "era mais lenta"), ("C-2", "três vírgula três nanonewtons")]


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c) and c.isalnum())


t = (AQUI / "narracao_final_v4.md").read_text(encoding="utf-8")
t = t[:t.rindex("## Números de conferência")]
blocos = []
for bloco in re.split(r"^### ", t, flags=re.M)[1:]:
    cab, *resto = bloco.split("\n")
    fala = " ".join(l for l in resto if l.strip() and not l.startswith(("---", "## ")))
    fala = re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", "", fala)).strip()
    blocos.append((cab.split(" — ")[0].strip(), fala.split(" ")))
al = json.loads((AQUI / "alinhamento_palavras.json").read_text(encoding="utf-8"))
ini, k = {}, 0
for aid, pal in blocos:
    ini[aid] = (k, k + len(pal) - 1)
    k += len(pal)
assert k == len(al)
ins = {}                                              # índice da palavra ANTES do intervalo → [duração, motivos]


def add(i, d, m):
    e = ins.setdefault(i, [0.0, []])
    e[0] = min(1.2, e[0] + d)
    e[1].append(m)


for (a, _), (b, _) in zip(blocos, blocos[1:]):
    i = ini[a][1]
    add(i, 1.0 if (a, b) in CAP else 0.6 if (a, b) == ("H3", "A1") else BASE, f"virada {a}→{b}" + (" (capítulo)" if (a, b) in CAP else ""))
for aid, fr in RES:
    alvo = [norm(w) for w in fr.split()]
    i0, i1 = ini[aid]
    ws = [norm(al[i]["word"]) for i in range(i0, i1 + 1)]
    j = next(j for j in range(len(ws)) if ws[j:j + len(alvo)] == alvo)
    add(i0 + j + len(alvo) - 1, 0.5, f"resultado {aid} «{fr}»")
for aid, (i0, i1) in ini.items():
    for i in range(i0, i1):
        if al[i]["word"].endswith("?") and i not in ins:
            add(i, 0.4, f"pergunta {aid} «{al[i]['word']}»")

with wave.open(str(AQUI / "audio" / "narracao_v4.wav")) as w:
    sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)
F = int(0.010 * sr)
cortes = []
for i in sorted(ins):
    a, b = al[i]["end"], al[i + 1]["start"]
    if b - a < 0.03:                                  # palavras coladas: corta no fim da primeira
        c = int(a * sr)
    else:                                             # o ponto mais quieto (RMS de 10 ms) dentro do intervalo
        s0, s1 = int(a * sr) + F, max(int(a * sr) + F + 1, int(b * sr) - F)
        rms = [np.sqrt(np.mean(x[q - F // 2:q + F // 2] ** 2)) for q in range(s0, s1, F // 2)] or [0]
        c = s0 + int(np.argmin(rms)) * (F // 2)
    assert a * sr - 1 <= c <= max(a, b) * sr + 1, (i, a, b, c / sr)
    cortes.append((c, ins[i][0], i, ins[i][1]))
partes, pos, desloc, lista = [], 0, 0.0, []
shift = np.zeros(len(al))
for c, d, i, mot in cortes:
    seg = x[pos:c].copy()
    seg[-F:] *= np.linspace(1, 0, F)                  # fade de saída antes do silêncio
    if partes:
        seg[:F] *= np.linspace(0, 1, F)               # fade de entrada depois do silêncio anterior
    partes += [seg, np.zeros(int(round(d * sr)), np.float32)]
    lista.append((c / sr + desloc, d, " + ".join(mot)))
    desloc += int(round(d * sr)) / sr
    shift[i + 1:] = desloc
    pos = c
seg = x[pos:].copy()
seg[:F] *= np.linspace(0, 1, F)
partes.append(seg)
y = np.concatenate(partes)
pico = np.abs(y).max() / 32768
with wave.open(str(AQUI / "audio" / "narracao_v4_pausas.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes(np.clip(y, -32768, 32767).astype(np.int16).tobytes())
al2 = [dict(w, start=round(w["start"] + s, 3), end=round(w["end"] + s, 3)) for w, s in zip(al, shift)]
(AQUI / "alinhamento_palavras_v6.json").write_text(json.dumps(al2, ensure_ascii=False, indent=1), encoding="utf-8")
dur = len(y) / sr
out = [f"voz v6: {dur:.2f} s (antes {len(x) / sr:.2f} s; +{desloc:.2f} s em {len(lista)} inserções); {len(al)} palavras → "
       f"{len(al) / dur:.3f} palavras/s; pico {20 * np.log10(pico):.2f} dBFS; base das viradas {BASE:.2f} s", ""]
out += [f"{int(t0 // 60)}:{t0 % 60:05.2f} → +{d:.2f} s  {m}" for t0, d, m in lista]
(AQUI / "log_pausas_v6.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print(out[0])
