"""yt_0019 v7 — R0 dos 44 itens do handoff v7 §3 (v6 × v7, no tempo exato da tabela) + pranchas extras §2.1 e §2.2.
Saídas em renders/v7/: r0/NN_<tempo>.png (v6|v7, 960×540 cada), r0_folha_K.png (12 itens por folha), zoom_NN.png (recorte 2× com régua de 912 px / 495 px),
extra_balanco.png (12 quadros, 5:09–5:51), extra_tsiolkovsky.png (15 quadros, 7:54–8:15), extra_cor.png. uso: python conferencia7.py"""
from pathlib import Path

import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
OUT = U / "renders" / "v7"
(OUT / "r0").mkdir(parents=True, exist_ok=True)
FPS = 15
mm = lambda s: int(s.split(":")[0]) * 60 + float(s.split(":")[1])
ITENS = {1: "0:12", 2: "1:30", 3: "2:28", 4: "2:30", 5: "3:25", 6: "4:15", 7: "5:10", 8: "5:10", 9: "5:30", 10: "6:12", 11: "6:13", 12: "7:15",
         13: "7:48", 14: "8:00", 15: "8:25", 16: "8:39", 17: "8:55", 18: "10:00", 19: "10:50", 20: "11:30", 21: "11:24", 22: "11:30", 23: "12:00",
         24: "12:13", 25: "11:35", 26: "13:00", 27: "13:00", 28: "12:57", 29: "13:10", 30: "13:30", 31: "14:20", 32: "15:20", 33: "15:35", 34: "16:10",
         35: "16:12", 36: "17:08", 37: "17:30", 38: "17:52", 39: "18:24", 40: "18:30", 41: "18:36", 42: "18:50", 43: "20:20", 44: "20:24"}
# zoom: (x0, y0, x1, y1) em px do quadro 960×540; régua vertical x = 912 / horizontal y = 495 quando indicada
ZOOM = {1: ((150, 30, 630, 300), None), 11: ((0, 300, 480, 570 - 30), "h"), 13: ((150, 260, 630, 530), None), 15: ((480, 100, 960, 370), None),
        16: ((0, 270, 480, 540), "h"), 18: ((150, 100, 630, 370), None), 33: ((400, 60, 880, 330), None), 38: ((600, 0, 960, 270), "v"),
        40: ((600, 100, 960, 370), "v"), 42: ((600, 100, 960, 370), "v"), 44: ((0, 100, 480, 370), None)}
EXTRA = {"extra_balanco": [309 + k * 3.5 for k in range(12)], "extra_tsiolkovsky": [474 + k * 1.5 for k in range(15)]}
COR = ["0:20", "2:30", "5:00", "9:00", "11:20", "13:00", "16:30", "18:30", "20:20"]
alvo = {int(mm(t) * FPS): None for t in ITENS.values()}
for ts in EXTRA.values():
    for t in ts:
        alvo[int(t * FPS)] = None
for t in COR:
    alvo[int(mm(t) * FPS)] = None


def pega(arq):
    c = av.open(str(arq))
    out, mx = {}, max(alvo)
    for i, fr in enumerate(c.decode(video=0)):
        if i in alvo:
            out[i] = fr.to_image()
        if i >= mx:
            break
    return out


a = pega(U / "renders" / "preview_yt0019_v6_960x540.mp4")
b = pega(U / "renders" / "preview_yt0019_v7_960x540.mp4")
W, H = 480, 270
itens = sorted(ITENS.items())
for n, t in itens:
    q = int(mm(t) * FPS)
    par = Image.new("RGB", (1920, 540))
    par.paste(a[q], (0, 0))
    par.paste(b[q], (960, 0))
    par.save(OUT / "r0" / f"{str(n).zfill(2)}_{t.replace(':', 'm')}.png")
for k in range(0, len(itens), 12):
    bloco = itens[k:k + 12]
    fo = Image.new("RGB", (2 * (2 * W + 10), (H + 22) * ((len(bloco) + 1) // 2)), "black")
    d = ImageDraw.Draw(fo)
    for j, (n, t) in enumerate(bloco):
        q = int(mm(t) * FPS)
        x, y = (j % 2) * (2 * W + 10), (j // 2) * (H + 22)
        d.text((x + 4, y + 5), f"#{n} · {t}   (v6 ← → v7)", fill="yellow")
        fo.paste(a[q].resize((W, H)), (x, y + 22))
        fo.paste(b[q].resize((W, H)), (x + W, y + 22))
    fo.save(OUT / f"r0_folha_{k // 12 + 1}.png")
for n, (box, regua) in ZOOM.items():
    q = int(mm(ITENS[n]) * FPS)
    ims = []
    for im in (a[q], b[q]):
        x0, y0, x1, y1 = box
        z = im.crop((x0, max(0, y0), x1, min(540, y1))).resize((960, int(960 * (min(540, y1) - max(0, y0)) / (x1 - x0))))
        dz = ImageDraw.Draw(z)
        if regua == "v":
            xr = (912 - x0) * 960 / (x1 - x0)
            dz.line([(xr, 0), (xr, z.height)], fill=(255, 40, 40), width=2)
        elif regua == "h":
            yr = (495 - max(0, y0)) * 960 / (x1 - x0)
            dz.line([(0, yr), (960, yr)], fill=(255, 40, 40), width=2)
        ims.append(z)
    fo = Image.new("RGB", (1920, ims[0].height), "black")
    fo.paste(ims[0], (0, 0))
    fo.paste(ims[1], (960, 0))
    fo.save(OUT / f"zoom_{str(n).zfill(2)}.png")
for nome, ts in EXTRA.items():
    C = 3
    ims = [b[int(t * FPS)].resize((640, 360)) for t in ts]
    fo = Image.new("RGB", (640 * C, 360 * ((len(ims) + C - 1) // C)), "black")
    for j, im in enumerate(ims):
        fo.paste(im, ((j % C) * 640, (j // C) * 360))
    fo.save(OUT / f"{nome}.png")
fo = Image.new("RGB", (2 * 640, 360 * len(COR)), "black")
for j, t in enumerate(COR):
    fo.paste(a[int(mm(t) * FPS)].resize((640, 360)), (0, 360 * j))
    fo.paste(b[int(mm(t) * FPS)].resize((640, 360)), (640, 360 * j))
fo.save(OUT / "extra_cor.png")
print("ok", len(itens))
