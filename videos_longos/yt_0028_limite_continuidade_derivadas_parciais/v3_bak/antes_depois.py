"""yt_0028 v3 (handoff v3 §0.5): os 4 momentos da 00_antes_v2_depois_v3.jpg (desafio ε-δ, derivadas no palco, três cartões, arestas),
renderizados: v2 (preview v2) à esquerda e v3 (lotes v3) à direita. Saída: renders/v3/qa/antes_depois_v3.jpg"""
import json
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageFont

from comparar import ALVO, quadro

U = Path(__file__).resolve().parent
q2 = json.loads((U / "renders" / "v2" / "quadros_v2.json").read_text(encoding="utf-8"))
V2 = U / "renders" / "v2" / "yt_0028_preview_v2_540p15.mp4"


def q_v2(t):
    c = av.open(str(V2))
    alvo = round(t * 15)
    for i, fr in enumerate(c.decode(video=0)):
        if i >= alvo:
            im = fr.to_image()
            c.close()
            return im


M = [("desafio ε-δ", q2["B1-4"] / 15 - 0.07, 3), ("derivadas no palco", q2["B5-1"] / 15 - 1.2, 17),
     ("três cartões", q2["B7-3"] / 15 + 14.5, 33), ("arestas", q2["B7-3"] / 15 - 0.3, 31)]
f = ImageFont.load_default()
L = []
for nome, t2, n in M:
    lote, ft = ALVO[n]
    a, b = q_v2(t2), quadro(lote, ft())
    im = Image.new("RGB", (1920, 568), (5, 11, 24))
    im.paste(a, (0, 28))
    im.paste(b, (960, 28))
    d = ImageDraw.Draw(im)
    d.text((8, 7), f"{nome} · v2 (preview v2, {int(t2 // 60)}:{t2 % 60:04.1f})", fill=(255, 150, 150), font=f)
    d.text((968, 7), f"v3 (alvo {n:02d}, {lote})", fill=(140, 255, 200), font=f)
    L.append(im)
pr = Image.new("RGB", (1920, 568 * len(L)))
for i, im in enumerate(L):
    pr.paste(im, (0, 568 * i))
pr.save(U / "renders" / "v3" / "qa" / "antes_depois_v3.jpg", quality=90)
print("ok")
