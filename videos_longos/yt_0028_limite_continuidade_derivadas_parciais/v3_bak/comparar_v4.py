"""yt_0028 v4 (handoff v4; v3 em v3_bak/comparar.py): render × alvo nos 37 quadros-alvo (v2: 31, em v2_bak/comparar.py) (v1: 18, em v1_bak/comparar_v1.py). Para cada alvo, acha o instante no lote pelos logs do render ([ancora],
[gatilho], [tempo]) — sempre com o estado completo (fora de escrita ou transição) —, tira o quadro do preview 960×540 e põe ao lado do alvo reduzido
a 960×540. Mede o deslocamento global (correlação de fase das bordas, px a 1080p) e a diferença média.
Saídas: renders/v1/qa/still_NN.png (só o render), renders/v1/qa/comparacao_v4.jpg (uma linha por quadro: render à esquerda, alvo à direita),
renders/v1/qa/comparacao_v4.txt (instantes e medidas).  uso: python comparar.py"""
import re
from pathlib import Path

import av
import numpy as np
from PIL import Image, ImageDraw, ImageFont

U = Path(__file__).resolve().parent
OUT = U / "renders" / "v4" / "qa"
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
    1: ("PH", lambda: gat("PH", "H3", "que número mede isso", -0.2)),
    2: ("PH", lambda: ancora("PH", "A1", -1.0)),
    3: ("PB1", lambda: ancora("PB1", "B1-4", -0.07)),
    4: ("PB1", lambda: gat("PB1", "B1-4", "diminui o delta", -0.2)),
    5: ("PB1", lambda: gat("PB1", "B1-5", "agora sim escrito", -0.2)),
    6: ("PB1", lambda: ancora("PB1", "B1-6", -0.5)),
    7: ("PB1", lambda: total("PB1")),
    8: ("PB2", lambda: ancora("PB2", "B2-3")),
    9: ("PB2", lambda: gat("PB2", "B2-4", "e fica um cuidado", -0.2)),
    10: ("PB2", lambda: total("PB2")),
    11: ("PB3", lambda: ancora("PB3", "B3-2")),
    12: ("PB3", lambda: ancora("PB3", "B3-3")),
    13: ("PB3", lambda: total("PB3")),
    14: ("PB4", lambda: gat("PB4", "B4-2", "desenha uma curva", -0.3)),
    15: ("PB4", lambda: ancora("PB4", "B4-4")),
    16: ("PB4", lambda: gat("PB4", "B4-4", "tangente ao círculo", -0.2)),
    17: ("PB4", lambda: total("PB4")),
    18: ("PB5", lambda: ancora("PB5", "B5-2")),
    19: ("PB5", lambda: ancora("PB5", "B5-3")),
    20: ("PB5", lambda: ancora("PB5", "B5-4")),
    21: ("PB5", lambda: gat("PB5", "B5-4", "dividindo o erro pelo passo", -0.2)),
    22: ("PB5", lambda: total("PB5", -0.5)),
    23: ("PB6", lambda: gat("PB6", "B6-1", "essa janelinha vira o palco inteiro", 0.45)),
    24: ("PB6", lambda: gat("PB6", "B6-1", "tira a seta do centro de todas", -0.2)),
    25: ("PB6", lambda: gat("PB6", "B6-2", "então coloca as duas lado a lado", -0.2)),
    26: ("PB6", lambda: ancora("PB6", "B6-3")),
    27: ("PB6", lambda: ancora("PB6", "B6-4")),
    28: ("PB6", lambda: gat("PB6", "B6-4", "solta o fluido no modelo", -0.2)),
    29: ("PB6", lambda: total("PB6")),
    30: ("PB7", lambda: ancora("PB7", "B7-2")),
    31: ("PB7", lambda: ancora("PB7", "B7-3")),
    32: ("PB7", lambda: gat("PB7", "B7-3", "quatro medidas saem", -0.1)),
    33: ("PB7", lambda: gat("PB7", "B7-3", "o atrito viscoso vem da deformação", -0.2)),
    34: ("PB7", lambda: ancora("PB7", "B7-4")),
    35: ("PB7", lambda: ancora("PB7", "B7-5")),
    36: ("PB7", lambda: gat("PB7", "B7-5", "quem achou um de segundo grau", 3.0)),
    37: ("PS", lambda: ancora("PS", "S2", -0.1)),
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


if __name__ == "__main__":
    linhas, rel = [], ["yt_0028 v4 · render × alvo (960×540 cada; deslocamento global por correlação de fase das bordas, px a 1080p)"]
    fonte = ImageFont.load_default()
    for n, (lote, ft) in ALVO.items():
        t = ft()
        r = quadro(lote, t)
        r.save(OUT / f"still_{n:02d}.png")
        arq = next((U / "referencia_v4").glob(f"{n:02d}_*.jpg"))
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
    pr.save(OUT / "comparacao_v4.jpg", quality=90)
    (OUT / "comparacao_v4.txt").write_text("\n".join(rel) + "\n", encoding="utf-8")
    print("\n".join(rel))
