"""yt_0019 v8 — R0 dos 12 itens do handoff v8 §2 (+ D1 e D3) antes (v7) × depois (v8) no mesmo instante + prancha de 6 quadros fora da lista.
Saídas em renders/v8/: r0/NN_<tempo>.png (v7|v8 960×540 cada), r0_folha_K.png, zoom_NN.png (recorte 2×), extra_sorteio.png.  uso: python conferencia8.py"""
from pathlib import Path

import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
OUT = U / "renders" / "v8"
(OUT / "r0").mkdir(parents=True, exist_ok=True)
FPS = 15
mm = lambda s: int(s.split(":")[0]) * 60 + float(s.split(":")[1])
ITENS = [("01", "5:15"), ("02", "6:26"), ("03", "7:18"), ("04", "8:51"), ("05", "9:30"), ("06", "10:43"), ("07", "11:25"), ("08", "14:20"), ("09_D1", "14:55"),
         ("10", "15:46"), ("11", "16:25"), ("12a_inset", "18:58"), ("12b_dica", "14:46"), ("12c_sintese", "20:25"), ("D3", "5:10")]
ZOOM = {"01": (420, 90, 940, 360), "02": (0, 380, 960, 540), "03": (0, 380, 480, 540), "04": (480, 90, 960, 360), "05": (0, 330, 960, 540), "06": (480, 90, 960, 360),
        "08": (0, 90, 480, 360), "10": (0, 360, 480, 540), "11": (0, 180, 480, 450), "12a_inset": (0, 330, 960, 540), "12c_sintese": (480, 0, 960, 540)}
SORTEIO = ["1:05", "3:00", "9:50", "13:45", "17:05", "19:45"]
alvo = {int(mm(t) * FPS) for _, t in ITENS} | {int(mm(t) * FPS) for t in SORTEIO}


def pega(arq):
    c = av.open(str(arq))
    out, mx = {}, max(alvo)
    for i, fr in enumerate(c.decode(video=0)):
        if i in alvo:
            out[i] = fr.to_image()
        if i >= mx:
            break
    return out


a = pega(U / "renders" / "preview_yt0019_v7_960x540.mp4")
b = pega(U / "renders" / "preview_yt0019_v8_960x540.mp4")
W, H = 480, 270
for n, t in ITENS:
    q = int(mm(t) * FPS)
    par = Image.new("RGB", (1920, 540))
    par.paste(a[q], (0, 0))
    par.paste(b[q], (960, 0))
    par.save(OUT / "r0" / f"{n}_{t.replace(':', 'm')}.png")
    if n in ZOOM:
        x0, y0, x1, y1 = ZOOM[n]
        z = [im.crop((x0, y0, x1, y1)) for im in (a[q], b[q])]
        zw = 960
        zz = [im.resize((zw, int(zw * (y1 - y0) / (x1 - x0)))) for im in z]
        fo = Image.new("RGB", (1920, zz[0].height), "black")
        fo.paste(zz[0], (0, 0))
        fo.paste(zz[1], (960, 0))
        fo.save(OUT / f"zoom_{n}.png")
for k in range(0, len(ITENS), 8):
    bloco = ITENS[k:k + 8]
    fo = Image.new("RGB", (2 * (2 * W + 10), (H + 22) * ((len(bloco) + 1) // 2)), "black")
    d = ImageDraw.Draw(fo)
    for j, (n, t) in enumerate(bloco):
        q = int(mm(t) * FPS)
        x, y = (j % 2) * (2 * W + 10), (j // 2) * (H + 22)
        d.text((x + 4, y + 5), f"#{n} · {t}   (v7 ← → v8)", fill="yellow")
        fo.paste(a[q].resize((W, H)), (x, y + 22))
        fo.paste(b[q].resize((W, H)), (x + W, y + 22))
    fo.save(OUT / f"r0_folha_{k // 8 + 1}.png")
ims = [b[int(mm(t) * FPS)].resize((640, 360)) for t in SORTEIO]
fo = Image.new("RGB", (640 * 3, 360 * 2), "black")
for j, im in enumerate(ims):
    fo.paste(im, ((j % 3) * 640, (j // 3) * 360))
fo.save(OUT / "extra_sorteio.png")
print("ok", len(ITENS))
