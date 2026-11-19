import json, sys, av
from pathlib import Path
from PIL import Image, ImageDraw
U = Path(__file__).resolve().parent
# uso: python _anc_sheet.py LOTE ANCORA saida.png frac1 frac2 ...  (frações 0-1 da duração da âncora; quadros inteiros 960x540, 2 colunas)
L, aid, out = sys.argv[1:4]; fr = [float(x) for x in sys.argv[4:]]
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
anc = A["ancoras"]; ordem = A["ordem"]
lotes = {"PH": "H1", "PB1": "B1-1", "PB2": "B2-1", "PB3": "B3-1", "PB4": "B4-1", "PB5": "B5-1", "PB6": "B6-1", "PS": "S1"}
base = anc[lotes[L]]["ini"]
a = anc[aid]
ts = [a["ini"] - base + f * a["dur"] for f in fr]
alvo = {int(round(t * 15)): t for t in ts}
c = av.open(str(U / f"media_{L}/videos/cena/540p15/{L}.mp4")); imgs = []
for k, f in enumerate(c.decode(video=0)):
    if k in alvo:
        im = f.to_image(); ImageDraw.Draw(im).text((4, 2), f"{L} {aid} {alvo[k]:.2f}s", fill=(255, 255, 0)); imgs.append(im)
    if k > max(alvo): break
cols = 2; rows = (len(imgs) + 1) // 2
S = Image.new("RGB", (960 * cols, 540 * rows))
for i, im in enumerate(imgs): S.paste(im, ((i % cols) * 960, (i // cols) * 540))
S.save(out)
