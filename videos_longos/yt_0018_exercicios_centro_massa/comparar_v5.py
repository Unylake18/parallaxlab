"""v5 §4/§6: prancha de 12 quadros nos tempos do handoff v5 (tempos do preview v4), v4 e v5 lado a lado. Os tempos do v5 saem da posição dentro da âncora
(as durações das âncoras mudaram com a narração v1.1). uso: python comparar_v5.py → renders/v5/prancha_12_v4_x_v5.png"""
import json
import sys
from pathlib import Path

import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
T4 = [105, 129, 171, 264, 285, 384, 438, 516, 565, 636, 675, 801]
a4 = json.loads((U / "_v4" / "ancoras_v4.json").read_text(encoding="utf-8"))
a5 = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
ordem = a5["ordem"]


def inicios(a):
    t, d = 0.0, {}
    for k in ordem:
        d[k] = t
        t += a["ancoras"][k]["dur"]
    return d


i4, i5 = inicios(a4), inicios(a5)


def mapa(t4):
    for k in reversed(ordem):
        if t4 >= i4[k]:
            return k, i5[k] + (t4 - i4[k])
    return ordem[0], t4


def quadros(video, ts):
    c = av.open(str(video))
    fps = float(c.streams.video[0].average_rate)
    alvo = {int(round(t * fps)): t for t in ts}
    ims = {}
    for i, fr in enumerate(c.decode(video=0)):
        if i in alvo:
            ims[alvo[i]] = fr.to_image()
        if i > max(alvo):
            break
    return ims


v4 = quadros(U / "renders" / "preview_yt0018_v4_960x540.mp4", T4)
pares = [mapa(t) for t in T4]
v5p = U / "renders" / "preview_yt0018_v5_960x540.mp4"
v5 = quadros(v5p, [p[1] for p in pares]) if v5p.exists() else {}
W, H = 640, 360
pr = Image.new("RGB", (W * 4, (H + 18) * 6), "black")
d = ImageDraw.Draw(pr)
for k, (t, (aid, t5)) in enumerate(zip(T4, pares)):
    x, y = (k % 2) * 2 * W, (k // 2) * (H + 18)
    for j, (nome, im, tt) in enumerate((("v4", v4.get(t), t), ("v5", v5.get(t5), t5))):
        if im is not None:
            pr.paste(im.resize((W, H)), (x + j * W, y + 18))
        d.text((x + j * W + 4, y + 3), f"{nome}  {int(tt // 60)}:{tt % 60:04.1f}  ({aid})", fill="yellow")
(U / "renders" / "v5").mkdir(parents=True, exist_ok=True)
pr.save(U / "renders" / "v5" / "prancha_12_v4_x_v5.png")
print(json.dumps([(t, a, round(t5, 1)) for t, (a, t5) in zip(T4, pares)]))
