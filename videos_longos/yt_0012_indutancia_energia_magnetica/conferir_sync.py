"""yt_0012 — confere a sincronia num vídeo renderizado com SYNC=ritmo.json.

1) Tabela: para cada âncora, instante do play ancorado (ritmo.json) − instante da palavra na voz sincronizada (deve ser −LEAD).
2) Imagem: primeiro quadro em que a imagem muda a partir de alvo − 0,3 s; desvio = início − alvo (quadros parados decodificam
   idênticos). Âncoras em que a tela já se movia antes ficam como "em movimento".
3) Pranchas tela × fala: um quadro no fim da animação de cada âncora, com a frase falada embaixo (pasta quadros/sync/).
Uso: uv run --no-sync python conferir_sync.py VIDEO.mp4 [--pranchas]
"""
import json
import sys
import textwrap
from pathlib import Path

import av
import numpy as np
from PIL import Image, ImageDraw

P = Path(__file__).resolve().parent
VID = Path(sys.argv[1])
rit = json.loads((P / "ritmo.json").read_text(encoding="utf-8"))
pads = sorted((a, d) for a, d, *_ in rit["pads"])


def desloca(t):
    return t + sum(d for a, d in pads if a <= t)


c = av.open(str(VID))
s = c.streams.video[0]
fps = float(s.average_rate)
alvos = [(nome, rit["t"][i], desloca(tw)) for nome, i, tw in rit["anchors"]]
tab = [round(a - v, 3) for _, a, v in alvos]
print(f"{len(alvos)} âncoras · play − palavra: mín {min(tab):+.3f} máx {max(tab):+.3f} (alvo −0,150)")

prancha = "--pranchas" in sys.argv
# quadro no fim da animação ancorada (o estado que o espectador vê enquanto a frase é dita)
fim = [min(rit["t"][i + 1] + 0.1, rit["dur"] - 0.1) for _, i, _ in rit["anchors"]]
quer = {int(round(f * fps)): k for k, f in enumerate(fim)} if prancha else {}
shots = {}
prev, dif = None, []
for k, f in enumerate(c.decode(s)):
    g = f.reformat(width=240, height=135, format="gray").to_ndarray().astype(np.int16)
    dif.append(0.0 if prev is None else float(np.abs(g - prev).mean()))
    prev = g
    if k in quer:
        shots[quer[k]] = f.to_image().resize((480, 270))
dif = np.array(dif)
res = []
for nome, a, v in alvos:
    k0 = int(round(a * fps))
    antes = dif[max(0, k0 - int(0.3 * fps)):k0 - 1]
    if len(antes) and antes.max() > 0:
        res.append((nome, a, None))
        continue
    jan = np.nonzero(dif[k0 - 1:k0 + int(fps)] > 0)[0]
    res.append((nome, a, (k0 - 1 + jan[0]) / fps - a if len(jan) else float("inf")))
med = [d for _, _, d in res if d is not None and d != float("inf")]
ruins = [(n, a, d) for n, a, d in res if d is not None and abs(d) > 1.5 / fps]
print(f"início detectável em {len(med)} · em movimento antes: {sum(d is None for *_, d in res)}")
if med:
    print(f"desvio (início − alvo): mediana {np.median(med):+.3f} s · máx {max(med):+.3f} · mín {min(med):+.3f}")
print(f"fora de ±1,5 quadro: {len(ruins)}")
for n, a, d in ruins:
    print(f"  {n[:40]:40s} alvo {a:8.2f}  desvio {d:+.2f}")
if prancha:
    out = P / "quadros" / "sync"
    out.mkdir(parents=True, exist_ok=True)
    ks = sorted(shots)
    for b in range(0, len(ks), 12):
        sh = Image.new("RGB", (3 * 480, 4 * 330), "black")
        for j, k in enumerate(ks[b:b + 12]):
            nome, a, _ = alvos[k]
            im = shots[k]
            sh.paste(im, ((j % 3) * 480, (j // 3) * 330))
            d = ImageDraw.Draw(sh)
            txt = f"{int(a // 60)}:{a % 60:04.1f}  «{nome}»"
            d.text(((j % 3) * 480 + 6, (j // 3) * 330 + 274), "\n".join(textwrap.wrap(txt, 70)), fill="yellow")
        sh.save(out / f"sync_{b // 12 + 1:02d}.png")
    print("pranchas em", out)
