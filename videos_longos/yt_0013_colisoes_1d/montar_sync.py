"""yt_0013 — voz sincronizada, legenda e capítulos a partir de ritmo.json (mesma base de tempo da cena).

- audio/narracao_sync.wav: narracao_v4.wav com os silêncios de ritmo inseridos (pads) e cauda até o fim da cena.
- final/legenda - 0013.srt: tempos do alinhamento forçado deslocados pelos pads; até 2 linhas de ≤ 42 caracteres.
- final/capitulos - 0013.txt: início de cada bloco = alvo da primeira âncora dele na cena.
Uso: uv run --no-sync python montar_sync.py
"""
import json
import textwrap
import wave
from pathlib import Path

import numpy as np

P = Path(__file__).resolve().parent
rit = json.loads((P / "ritmo.json").read_text(encoding="utf-8"))
pads = sorted((a, d) for a, d, *_ in rit["pads"])


def desloca(t):
    return t + sum(d for a, d in pads if a <= t)


# voz
w = wave.open(str(P / "audio" / "narracao_v4.wav"))
sr, prm = w.getframerate(), w.getparams()
x = np.frombuffer(w.readframes(w.getnframes()), np.int16)
partes, ini = [], 0
for a, d in pads:
    k = int(round(a * sr))
    partes += [x[ini:k], np.zeros(int(round(d * sr)), np.int16)]
    ini = k
partes.append(x[ini:])
y = np.concatenate(partes)
alvo = int(round(rit["dur"] * sr))
y = np.concatenate([y, np.zeros(max(0, alvo - len(y)), np.int16)])[:alvo]
o = wave.open(str(P / "audio" / "narracao_sync.wav"), "wb")
o.setparams(prm)
o.writeframes(y.tobytes())
o.close()

# legenda
cel = json.loads((P / "audio" / "alinhamento_forcado.json").read_text(encoding="utf-8"))["celulas"]
pal = [(t, desloca(a), desloca(b)) for c in cel for t, a, b in c["palavras"]]


def fmt(t):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    ms = int(round((s - int(s)) * 1000))
    if ms == 1000:
        s, ms = s + 1, 0
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{ms:03d}"


blocos, cur = [], []
for p in pal:
    cur.append(p)
    t = " ".join(q[0] for q in cur)
    if p[0][-1] in ".?!:" or (p[0][-1] in ",;" and len(t) > 45) or len(t) > 64:
        blocos.append(cur)
        cur = []
if cur:
    blocos.append(cur)
out = []
for i, b in enumerate(blocos, 1):
    a, f = b[0][1], b[-1][2] + 0.25
    if i < len(blocos):
        f = min(f, blocos[i][0][1] - 0.02)
    out.append(f"{i}\n{fmt(a)} --> {fmt(f)}\n" + "\n".join(textwrap.wrap(" ".join(q[0] for q in b), 42)))
(P / "final").mkdir(exist_ok=True)
(P / "final" / "legenda - 0013.srt").write_text("\n\n".join(out) + "\n", encoding="utf-8")

# capítulos
CAP = [("H1", "Mesmo começo, três finais"), ("C01-1", "Momento linear"), ("C02-1", "Momento e impulso"),
       ("C03-1", "Tipos de colisão"), ("C04-1", "Colisão completamente inelástica"), ("C04-5", "Média ponderada"),
       ("C05-1", "Energia cinética não se conserva"), ("C06-1", "Colisão elástica: as duas equações"),
       ("C06b-1", "Velocidade relativa"), ("C07-1", "Fórmulas gerais"), ("C08-1", "Casos-limite"),
       ("C09-1", "Pêndulo balístico"), ("C10-1", "Pêndulo: o impacto"), ("C11-1", "Pêndulo: a subida"),
       ("C12-1", "O método"), ("P1", "Próximo passo: colisões em 2D")]
primeiro = {}
for r in rit["trechos"]:
    primeiro.setdefault(r["id"], r["alvo"])
linhas = []
for aid, tit in CAP:
    t = 0.0 if aid == "H1" else max(0.0, primeiro[aid] - 1.0)
    linhas.append(f"{int(t) // 60:02d}:{int(t) % 60:02d} {tit}")
(P / "final" / "capitulos - 0013.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
print(f"voz {len(y) / sr:.2f} s ({len(pads)} pausas, {sum(d for _, d in pads):.2f} s); {len(blocos)} legendas; "
      f"{len(linhas)} capítulos")
