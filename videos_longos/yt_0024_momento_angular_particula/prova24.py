"""yt_0024 v3 §1.6 — renders/prova_caneta_yt0024.mp4 (≈ 20 s, 960×540): B3-2 inteiro + B6-4 e B6-5 (de τ_z = d(Iω)/dt até α = +5,9), cortados dos
mp4 dos lotes PB3 e PB6; mais 6 quadros consecutivos de um voo pousando na vez dele e 6 de uma linha só de caneta (renders/prova/).
uso: python prova24.py → renders/prova_caneta_yt0024.mp4 e renders/prova/*.png"""
import re
import sys
from pathlib import Path

import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
R = U / "renders"
(R / "prova").mkdir(exist_ok=True)


def ancoras(l):
    s = (U / f"log_{l}.txt").read_text(encoding="utf-8", errors="replace")
    an = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", s)]
    tt = re.search(r"\[tempo\] total ([0-9.]+)", s)
    fim = float(tt.group(1)) if tt else an[-1][1] + 5
    return {a: (t0, (an[k + 1][1] if k + 1 < len(an) else fim)) for k, (a, t0) in enumerate(an)}


def frames(l):
    with av.open(str(U / f"media_{l}/videos/cena/540p15/{l}.mp4")) as c:
        return [f.to_image() for f in c.decode(video=0)]


def trecho(fr, a, b):
    return fr[int(a * 15):int(b * 15)]


out = []
a3, a6 = ancoras("PB3"), ancoras("PB6")
f3, f6 = frames("PB3"), frames("PB6")
# B3-2 inteiro (cadeia com o cartão), B6-4 (da cadeia ao α) — duração total alvo ≈ 20 s: acelera ×k por amostragem uniforme se passar
b32 = trecho(f3, *a3["B3-2"])
b64 = trecho(f6, *a6["B6-4"])
b65 = trecho(f6, a6["B6-5"][0], a6["B6-5"][0] + 6)
seq = b32 + b64 + b65
alvo = 20 * 15
if len(seq) > alvo:
    seq = [seq[int(i * len(seq) / alvo)] for i in range(alvo)]
w = av.open(str(R / "prova_caneta_yt0024.mp4"), "w")
st = w.add_stream("libx264", rate=15)
st.width, st.height, st.pix_fmt = 960, 540, "yuv420p"
st.options = {"crf": "18"}
for im in seq:
    fr = av.VideoFrame.from_image(im.convert("RGB"))
    for p in st.encode(fr):
        w.mux(p)
for p in st.encode():
    w.mux(p)
w.close()
# 6 quadros consecutivos de um voo (B4-2: R e ω em L = mR²ω não existe mais: usa o B3-2, voo dos termos para `= v⃗ × m v⃗`) e 6 de linha de caneta (B6-3 `= Iα + İω`)
f4 = None


def faixa(fr, t0, n=6):
    return [fr[int(t0 * 15) + k] for k in range(n)]


def prancha(ims, nome):
    P = Image.new("RGB", (960 * 3, 540 * 2))
    for k, im in enumerate(ims):
        P.paste(im, ((k % 3) * 960, (k // 3) * 540))
        ImageDraw.Draw(P).text(((k % 3) * 960 + 8, (k // 3) * 540 + 6), f"{nome} q+{k}", fill=(255, 230, 0))
    P.save(R / "prova" / f"{nome}.png")


# voo: início da gm C2→C3 no B3-2 (gatilho "na mesma direção" ≈ 2,5 s depois do início da âncora) e linha só de caneta: B6-3 a 3 s do início
prancha(faixa(f3, a3["B3-2"][0] + 4.0), "voo_B3-2")
prancha(faixa(f6, a6["B6-3"][0] + 3.0), "caneta_B6-3")
print("prova ok", len(seq) / 15, "s")
