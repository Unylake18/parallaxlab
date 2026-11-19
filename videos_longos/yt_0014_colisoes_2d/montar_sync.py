"""yt_0014 — voz sincronizada, legenda e capítulos a partir de ritmo.json (mesma base de tempo da cena).

- audio/narracao_sync.wav: narracao_v4.wav com os silêncios de ritmo inseridos (pads) e cauda até o fim da cena.
- final/legenda - 0014.srt: tempos do alinhamento forçado deslocados pelos pads; até 2 linhas de ≤ 42 caracteres.
- final/capitulos - 0014.txt: início de cada bloco = alvo da primeira âncora dele na cena.
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
cel = json.loads((P / "audio" / "alinhamento_forcado.json").read_text(encoding="utf-8"))["celulas"]

# costuras do render em grupos (costuras.py): cada grupo começa atrasado 1–2 quadros por emenda; o atraso incremental entra como
# silêncio curto (≤ 0,08 s) no meio da pausa de fala antes da primeira âncora do grupo, para voz e imagem ficarem alinhadas
SEAM = []
if (P / "final" / "costuras.json").exists():
    TODAS = [p_ for c in cel for p_ in c["palavras"]]
    ant = 0.0
    for c in json.loads((P / "final" / "costuras.json").read_text(encoding="utf-8")):
        w = next(ch["palavras"][0] for ch in cel if ch["chave"] == c["ancora"])
        i = next(j for j, x in enumerate(TODAS) if x is w)
        SEAM.append(((TODAS[i - 1][2] + w[1]) / 2, c["atraso"] - ant))
        ant = c["atraso"]
    pads = sorted(pads + SEAM)


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
alvo = int(round((rit["dur"] + sum(d for _, d in SEAM)) * sr))
y = np.concatenate([y, np.zeros(max(0, alvo - len(y)), np.int16)])[:alvo]
o = wave.open(str(P / "audio" / "narracao_sync.wav"), "wb")
o.setparams(prm)
o.writeframes(y.tobytes())
o.close()

# legenda
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
(P / "final" / "legenda - 0014.srt").write_text("\n\n".join(out) + "\n", encoding="utf-8")

# capítulos
CAP = [("H1", "Para onde ela pode sair?"), ("C01-1", "Da linha para o plano"), ("C02-1", "Momento e impulso em 2D"),
       ("C03-1", "Componentes do momento"), ("C04-1", "Elástica, massas iguais: o ângulo reto"),
       ("C05-1", "Exemplo: bola a 30 graus"), ("C06-1", "Massas diferentes: a equação do círculo"),
       ("C07-1", "Completando o quadrado"), ("C08-1", "Os pontos do círculo e o cone"),
       ("C09-1", "O ângulo máximo e o teorema de Tales"), ("C10-1", "Alfa contra nêutron"),
       ("C11-1", "Colisão perfeitamente inelástica em 2D"), ("C12-1", "Explosão em três pedaços"),
       ("C13-1", "Roteiro para resolver qualquer colisão"), ("C14-1", "Próximo passo: o corpo extenso")]
primeiro = {}
for r in rit["trechos"]:
    primeiro.setdefault(r["id"], r["alvo"])
linhas = []
for aid, tit in CAP:
    t = 0.0 if aid == "H1" else max(0.0, desloca(primeiro[aid]) - 1.0)
    linhas.append(f"{int(t) // 60:02d}:{int(t) % 60:02d} {tit}")
(P / "final" / "capitulos - 0014.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
print(f"voz {len(y) / sr:.2f} s ({len(pads)} pausas, {sum(d for _, d in pads):.2f} s); {len(blocos)} legendas; "
      f"{len(linhas)} capítulos")
