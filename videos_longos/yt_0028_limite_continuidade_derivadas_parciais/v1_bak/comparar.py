"""yt_0028 v1 (handoff v1.2 §8.1): render × alvo nos 18 quadros-alvo. Para cada alvo, acha o instante no lote pelos logs do render ([ancora],
[gatilho], [tempo]) — sempre com o estado completo (fora de escrita ou transição) —, tira o quadro do preview 960×540 e põe ao lado do alvo reduzido
a 960×540. Mede o deslocamento global (correlação de fase das bordas, px a 1080p) e a diferença média.
Saídas: renders/v1/qa/still_NN.png (só o render), renders/v1/qa/comparacao_v1.jpg (uma linha por quadro: render à esquerda, alvo à direita),
renders/v1/qa/comparacao_v1.txt (instantes e medidas).  uso: python comparar.py"""
import re
from pathlib import Path

import av
import numpy as np
from PIL import Image, ImageDraw, ImageFont

U = Path(__file__).resolve().parent
OUT = U / "renders" / "v1" / "qa"
OUT.mkdir(parents=True, exist_ok=True)


def log(l):
    return (U / f"log_{l}.txt").read_text(encoding="utf-8", errors="replace")


def ini(l):
    return {m.group(1): float(m.group(2)) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", log(l))}


def gat(l, anc, frase, d=0.0):
    for x in log(l).splitlines():
        m = re.match(r"\[gatilho\] (\S+)\s+([0-9.]+)s .*?\) (.*)$", x)
        if m and m.group(1) == anc and m.group(3).strip() == frase:
            return ini(l)[anc] + float(m.group(2)) + d
    raise KeyError((l, anc, frase))


def total(l, d=-0.8):
    return float(re.search(r"\[tempo\] total ([0-9.]+)s", log(l)).group(1)) + d


def ancora(l, anc, d=-0.3):
    return ini(l)[anc] + d


ALVO = {
    1: ("PH", lambda: ancora("PH", "A1", -1.0)),
    2: ("PB1", lambda: gat("PB1", "B1-3", "aperta para meio", -0.3)),
    3: ("PB1", lambda: ancora("PB1", "B1-4")),
    4: ("PB2", lambda: total("PB2")),
    5: ("PB3", lambda: total("PB3")),
    6: ("PB4", lambda: ancora("PB4", "B4-3")),
    7: ("PB4", lambda: gat("PB4", "B4-3", "tangente ao círculo", -0.2)),
    8: ("PB4", lambda: total("PB4")),
    9: ("PB5", lambda: total("PB5")),
    10: ("PB6", lambda: gat("PB6", "B6-2", "então coloca as duas lado a lado", 0.0)),
    11: ("PB6", lambda: ancora("PB6", "B6-3")),
    12: ("PB6", lambda: gat("PB6", "B6-3", "solta o fluido no modelo", -0.2)),
    13: ("PB6", lambda: total("PB6")),
    14: ("PB7", lambda: gat("PB7", "B7-2", "entre as duas diagonais", -0.2)),
    15: ("PB7", lambda: gat("PB7", "B7-3", "e isso não é só matemática", -0.2)),
    16: ("PB7", lambda: ancora("PB7", "B7-5")),
    17: ("PB7", lambda: gat("PB7", "B7-5", "quem achou um de segundo grau", 2.5)),
    18: ("PS", lambda: ancora("PS", "S2", -0.07)),
}


def quadro(l, t):
    c = av.open(str(U / f"media_{l}/videos/cena/540p15/{l}.mp4"))
    q = round(t * 15)
    for i, fr in enumerate(c.decode(video=0)):
        if i >= q:
            im = fr.to_image()
            c.close()
            return im
    c.close()
    return fr.to_image()


def bordas(im):
    g = np.asarray(im.convert("L"), float)
    gx = np.abs(np.diff(g, axis=1, prepend=g[:, :1]))
    gy = np.abs(np.diff(g, axis=0, prepend=g[:1]))
    e = gx + gy
    e[:80, :] = 0                 # o canto e o logo ficam fora da medida (o logo do kit é a marca-d'água do canal)
    return e - e.mean()


def deslocamento(a, b):
    A, B = np.fft.fft2(bordas(a)), np.fft.fft2(bordas(b))
    R = A * np.conj(B)
    r = np.fft.ifft2(R / (np.abs(R) + 1e-9)).real
    dy, dx = np.unravel_index(np.argmax(r), r.shape)
    h, w = r.shape
    dy, dx = (dy - h if dy > h // 2 else dy), (dx - w if dx > w // 2 else dx)
    return dx * 2, dy * 2          # px a 1080p


linhas, rel = [], ["yt_0028 v1 · render × alvo (960×540 cada; deslocamento global por correlação de fase das bordas, px a 1080p)"]
fonte = ImageFont.load_default()
for n, (lote, ft) in ALVO.items():
    t = ft()
    r = quadro(lote, t)
    r.save(OUT / f"still_{n:02d}.png")
    arq = next((U / "referencia_v1").glob(f"{n:02d}_*.jpg"))
    a = Image.open(arq).convert("RGB").resize((960, 540), Image.LANCZOS)
    dx, dy = deslocamento(r, a)
    dif = float(np.abs(np.asarray(r, float) - np.asarray(a, float)).mean())
    rel.append(f"{n:02d} {arq.stem:34s} lote {lote:4s} t = {t:7.2f} s  deslocamento ({dx:+d}, {dy:+d}) px  diferença média {dif:5.1f}/255")
    lin = Image.new("RGB", (1920, 540 + 28), (5, 11, 24))
    lin.paste(r, (0, 28))
    lin.paste(a, (960, 28))
    d = ImageDraw.Draw(lin)
    d.text((8, 7), f"{n:02d} RENDER  {lote} t={t:.2f}s", fill=(255, 220, 90), font=fonte)
    d.text((968, 7), f"ALVO  {arq.stem}", fill=(160, 220, 255), font=fonte)
    linhas.append(lin)
pr = Image.new("RGB", (1920, sum(l.height for l in linhas)))
y = 0
for l in linhas:
    pr.paste(l, (0, y))
    y += l.height
pr.save(OUT / "comparacao_v1.jpg", quality=90)
(OUT / "comparacao_v1.txt").write_text("\n".join(rel) + "\n", encoding="utf-8")
print("\n".join(rel))
