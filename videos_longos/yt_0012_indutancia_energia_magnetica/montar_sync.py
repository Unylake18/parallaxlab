"""yt_0012 — voz sincronizada, legenda e capítulos a partir de ritmo.json (mesma base de tempo da cena).

- audio/narracao_sync.wav: narracao_v4.wav com as pausas de ritmo inseridas e cauda até o fim da cena.
- final/legenda - 0012.srt: tempos do alinhamento forçado deslocados pelas pausas; até 2 linhas de ≤ 42 caracteres.
- final/capitulos - 0012.txt: início de cada bloco = instante (na cena) da âncora que abre o bloco.
Uso: uv run --no-sync python montar_sync.py
"""
import json
import re
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
bruto = json.loads((P / "audio" / "alinhamento_forcado_bruto.json").read_text(encoding="utf-8"))
pal = [(w["text"], desloca(w["start"]), desloca(w["end"])) for w in bruto["words"] if w["text"].strip()]


def fmt(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


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
(P / "final" / "legenda - 0012.srt").write_text("\n\n".join(out) + "\n", encoding="utf-8")

# capítulos (âncora que abre cada bloco → instante do play ancorado na cena)
CAP = [("Olha esse circuito", "A corrente deveria saltar"), ("Antes de fazer uma bobina", "Indução mútua"),
       ("Agora vamos inverter o experimento", "Reciprocidade"), ("Tiramos a segunda bobina", "Autoindução"),
       ("Para enxergar o sinal negativo", "O indutor se opõe à mudança"),
       ("Agora voltamos ao circuito do começo", "A equação do circuito RL"), ("Vamos resolver", "Resolvendo a equação"),
       ("Agora vamos rodar essa carga", "A constante de tempo"), ("Agora vamos olhar fisicamente", "O campo elétrico induzido"),
       ("Agora entra a segunda pergunta", "Construir o campo custa energia"),
       ("O primeiro termo é a potência", "Balanço de potência e energia magnética"), ("Beleza", "Onde está a energia?"),
       ("Mas dá para reescrever", "Densidade de energia magnética"), ("E no vácuo essa ideia", "Campos não uniformes"),
       ("Vamos fazer o teste", "Descarga: tirando a bateria"), ("Agora a equação da malha não tem", "O indutor sustenta a corrente"),
       ("A corrente cai como uma exponencial", "O campo vira calor"), ("Quanto de calor aparece", "A conservação fecha"),
       ("Então agora dá para responder", "Síntese"), ("Só que a eletrodinâmica", "Próximo passo: Maxwell")]
an = {nome: i for nome, i, _ in rit["anchors"]}
linhas = []
for nome, tit in CAP:
    t = 0.0 if nome == "Olha esse circuito" else max(0.0, rit["t"][an[nome]] - 0.5)
    linhas.append(f"{int(t) // 60:02d}:{int(t) % 60:02d} {tit}")
(P / "final" / "capitulos - 0012.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
print(f"voz {len(y) / sr:.2f} s ({len(pads)} pausas, {sum(d for _, d in pads):.2f} s); {len(blocos)} legendas; "
      f"{len(linhas)} capítulos")
