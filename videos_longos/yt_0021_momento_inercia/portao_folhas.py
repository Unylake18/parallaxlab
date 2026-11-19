"""yt_0021 v9: folhas do portão item a item. Para cada item 'real' de renders/portao_classificado.txt: o quadro do preview v9 no meio do intervalo do item,
com a legenda (lote · categoria · descrição). Serve para o veredito POR IMAGEM (corrigir / ok), não por regra. Saída: renders/v9/portao/folha_NN.jpg + indice.txt.
uso: python portao_folhas.py [v9]"""
import json
import re
import sys
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageFont

U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "v9"
FPS = 15
ANC = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
PRIM = {"PH": "H1", "PA": "A1", "PT1": "T1-1", "PT2": "T2-1", "PT3": "T3-1", "PT4": "T4-1", "PT5": "T5-1", "PT6": "T6-1", "PE1": "E1-1", "PE2": "E2-1", "PE3": "E3-1", "PS": "S1"}
itens = []
for l in (U / "renders" / "portao_classificado.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^real\s+(\w+)\s+(.+?)\s{2,}x(\d+)\s+([0-9.]+)–([0-9.]+)s\s+(.*?)\s+\|", l)
    if not m:
        continue
    lote, cat, n, t0, t1, desc = m.group(1), m.group(2).strip(), int(m.group(3)), float(m.group(4)), float(m.group(5)), m.group(6).strip()
    t = ANC[PRIM[lote]]["ini"] + 0.5 * (t0 + t1)
    itens.append((lote, cat, n, t0, t1, desc, t))
need = {}
for it in itens:
    need[min(18738, max(0, round(it[6] * FPS)))] = None
c = av.open(str(U / "renders" / f"preview_yt0021_{R}_960x540.mp4"))
for i, fr in enumerate(c.decode(video=0)):
    if i in need:
        need[i] = fr.to_image().resize((384, 216))
    if i > max(need):
        break
out = U / "renders" / R / "portao"
out.mkdir(parents=True, exist_ok=True)
for f in out.glob("*"):
    f.unlink()
fonte = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 13)
COL, LIN = 5, 6
idx = []
for s0 in range(0, len(itens), COL * LIN):
    grupo = itens[s0:s0 + COL * LIN]
    folha = Image.new("RGB", (384 * COL, 250 * LIN), (10, 14, 28))
    dr = ImageDraw.Draw(folha)
    for k, (lote, cat, n, t0, t1, desc, t) in enumerate(grupo):
        x, y = (k % COL) * 384, (k // COL) * 250
        im = need.get(min(18738, max(0, round(t * FPS))))
        if im is not None:
            folha.paste(im, (x, y + 34))
        num = s0 + k + 1
        dr.text((x + 4, y + 2), f"#{num} {lote} {cat} x{n} {t0:.1f}–{t1:.1f}s", font=fonte, fill=(255, 220, 120))
        dr.text((x + 4, y + 18), desc[:60], font=fonte, fill=(160, 240, 255))
        idx.append(f"#{num:03d} folha_{s0 // (COL * LIN) + 1:02d} {lote} {cat} x{n} {t0:.1f}–{t1:.1f}s {desc[:80]}")
    folha.save(out / f"folha_{s0 // (COL * LIN) + 1:02d}.jpg", quality=86)
(out / "indice.txt").write_text("\n".join(idx), encoding="utf-8")
print(len(itens), "itens;", (len(itens) + COL * LIN - 1) // (COL * LIN), "folhas")
