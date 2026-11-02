"""Céu do laboratório (handoff v4 §2), gerado uma vez: fundo_lab.png (1920×1080, todas as cenas) e fundo_lab_ex.png (exercícios: metade
das estrelas). Gradiente vertical #0B1A3A → #08122B → #0A1030, vinheta radial (bordas −8%), brilho magenta baixo no horizonte (faixa de ~10%
da altura, #EA63FF a ~11%, esfumada), estrelas estáticas 1–2 px a 15–30% (~1 a cada 120×120 px), rarefeitas a 40% atrás da coluna da CONTA.
uso: python fundo.py"""
from pathlib import Path

import numpy as np
from PIL import Image

U = Path(__file__).resolve().parent
W, H = 1920, 1080
hexrgb = lambda h: np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], float)


def ceu(fr_estrelas=1.0, seed=17):
    y = np.linspace(0, 1, H)[:, None, None]
    topo, meio, base = hexrgb("#0B1A3A"), hexrgb("#08122B"), hexrgb("#0A1030")
    img = np.where(y < 0.5, topo + (meio - topo) * (y / 0.5), meio + (base - meio) * ((y - 0.5) / 0.5)) * np.ones((1, W, 1))
    # brilho magenta no horizonte: gaussiana a partir da borda de baixo (~10% da altura)
    g = np.exp(-((1 - y) / 0.075) ** 2) * 0.11
    img = img * (1 - g) + hexrgb("#EA63FF") * g
    # vinheta radial leve: −8% nas bordas
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)) / np.sqrt(2)
    img *= (1 - 0.08 * np.clip(r, 0, 1) ** 2)[..., None]
    # estrelas estáticas
    rng = np.random.default_rng(seed)
    n = int(W * H / (120 * 120) * fr_estrelas)
    est = np.zeros((H, W))
    x0c, x1c, y0c, y1c = (1.1 + 8) / 16 * W, (7.4 + 8) / 16 * W, (4.5 - 2.8) / 9 * H, (4.5 + 3.4) / 9 * H   # coluna da CONTA
    feitas = 0
    while feitas < n:
        x, y_ = rng.uniform(0, W - 2), rng.uniform(0, H * 0.93)
        if x0c < x < x1c and y0c < y_ < y1c and rng.uniform() > 0.4:          # atrás da CONTA: só 40% delas
            continue
        a = rng.uniform(0.15, 0.30)
        s = 1 if rng.uniform() < 0.7 else 2
        xi, yi = int(x), int(y_)
        est[yi:yi + s, xi:xi + s] = np.maximum(est[yi:yi + s, xi:xi + s], a)
        feitas += 1
    img = img * (1 - est[..., None]) + np.array([235, 240, 255.0]) * est[..., None]
    out = Image.fromarray(np.clip(img + 0.5, 0, 255).astype(np.uint8))
    return out


if __name__ == "__main__":
    ceu(1.0).save(U / "fundo_lab.png")
    ceu(0.5, seed=23).save(U / "fundo_lab_ex.png")
    a = np.asarray(Image.open(U / "fundo_lab.png"), float)
    Y = (0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]) / 255
    print(f"fundo_lab.png: luminância média {Y.mean():.3f}; pixels < 0,03: {100 * (Y < 0.03).mean():.1f}%")
