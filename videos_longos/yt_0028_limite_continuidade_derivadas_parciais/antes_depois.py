"""yt_0028 v4 (handoff v4 §0.3): antes × depois em 8 momentos — gancho (alvo 01), B1-3 (03), B2-4 (10), B4-4 (17), B5-3 (20), B5-5 (22, o gráfico novo),
B7-3 (32) e o resumo (37). Esquerda: preview v3 no mesmo ponto da fala (âncora + mesmo deslocamento; a narração é a mesma); direita: lote v4.
Saídas: renders/v4/qa/antes_depois/NN_*.png (960×540 cada lado) e renders/v4/qa/antes_depois_v4.jpg (prancha). (v3 em v3_bak/antes_depois.py)"""
import json
import re
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageFont

from comparar import ALVO, ini, quadro, total

U = Path(__file__).resolve().parent
q3 = json.loads((U / "renders" / "v3" / "quadros_v3.json").read_text(encoding="utf-8"))
V3 = U / "renders" / "v3" / "yt_0028_preview_v3_540p15.mp4"
OUT = U / "renders" / "v4" / "qa" / "antes_depois"
OUT.mkdir(parents=True, exist_ok=True)


def q_v3(t):
    c = av.open(str(V3))
    alvo = round(t * 15)
    for i, fr in enumerate(c.decode(video=0)):
        if i >= alvo:
            im = fr.to_image()
            c.close()
            return im


M = [(1, "gancho"), (3, "B1-3 desafio eps"), (10, "B2-4 retas e parábola"), (17, "B4-4 derivadas no palco"), (20, "B5-3 gráficos C1"),
     (22, "B5-5 erro ÷ passo (novo)"), (32, "B7-3 três cartões"), (37, "resumo")]
FIM = {10: "B3-1", 17: "B5-1", 22: "B6-1"}
f = ImageFont.load_default()
L = []
for n, nome in M:
    lote, ft = ALVO[n]
    t4 = ft()
    an = ini(lote)
    anc = max((a for a in an if an[a] <= t4 + 1e-6), key=lambda a: an[a])
    t3 = q3[anc] / 15 + (t4 - an[anc])
    if n in FIM:                                   # alvo medido a partir do fim do lote: no v3, o mesmo recuo antes do início do lote seguinte
        t3 = q3[FIM[n]] / 15 - (total(lote, 0.0) - t4)
    a, b = q_v3(t3), quadro(lote, t4)
    a.save(OUT / f"{n:02d}_v3.png")
    b.save(OUT / f"{n:02d}_v4.png")
    im = Image.new("RGB", (1920, 568), (12, 10, 30))
    im.paste(a, (0, 28))
    im.paste(b, (960, 28))
    d = ImageDraw.Draw(im)
    d.text((8, 7), f"{n:02d} {nome} · ANTES v3 ({int(t3 // 60)}:{t3 % 60:04.1f}, âncora {anc})", fill=(255, 150, 150), font=f)
    d.text((968, 7), f"DEPOIS v4 (alvo {n:02d}, {lote} t={t4:.2f}s)", fill=(140, 255, 200), font=f)
    L.append(im)
pr = Image.new("RGB", (1920, 568 * len(L)))
for i, im in enumerate(L):
    pr.paste(im, (0, 568 * i))
pr.save(U / "renders" / "v4" / "qa" / "antes_depois_v4.jpg", quality=90)
print("ok")
