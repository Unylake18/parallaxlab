"""v7 (§1.3): fundo espacial único da unidade — gradiente azul-noite #0B1A3A → #08122B → #0A1030, estrelas estáticas fracas
(rarefeitas atrás da coluna da CONTA) e brilho magenta baixo no horizonte. O yt_0017 não está neste repositório: refeito pela
especificação do handoff. Gera assets_unidade/fundo_lab.png (1920×1080), a versão 960×540 (redução BOX, a mesma que o Three.js
faz ao amostrar a textura no meio de cada 2×2) e threejs/cena3d/fundo_lab.js (data URL para a textura do clear 3D).
uso: python fundo_lab.py"""
import base64
import io
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

U = Path(__file__).resolve().parent
W, H = 1920, 1080


def hexrgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], dtype=np.float64)


def gera():
    y = np.linspace(0, 1, H)[:, None]
    c0, c1, c2 = hexrgb("#0B1A3A"), hexrgb("#08122B"), hexrgb("#0A1030")
    u = np.clip(y / 0.55, 0, 1)
    v = np.clip((y - 0.55) / 0.45, 0, 1)
    img = np.where(y[..., None] < 0.55, c0 + (c1 - c0) * (u * u * (3 - 2 * u))[..., None], c1 + (c2 - c1) * (v * v * (3 - 2 * v))[..., None])
    img = np.broadcast_to(img, (H, W, 3)).copy()
    # brilho magenta baixo no horizonte (faixa larga e fraca, centrada no PALCO)
    X, Y = np.meshgrid(np.linspace(-8, 8, W), np.linspace(4.5, -4.5, H))
    g = np.exp(-((Y + 1.6) / 1.5) ** 2) * np.exp(-((X + 2.2) / 7.5) ** 2)
    img += g[..., None] * (hexrgb("#EA63FF") - img) * 0.075
    # estrelas: fracas, determinísticas; atrás da CONTA (x > 0,6 no Manim) só 30 % delas
    rng = np.random.default_rng(2017)
    est = np.zeros((H, W))
    n = 0
    while n < 340:
        xs, ys = rng.uniform(0, W), rng.uniform(0, H)
        xm = xs / W * 16 - 8
        if xm > 0.6 and rng.uniform() > 0.3:
            continue
        b = 0.10 + 0.32 * rng.uniform() ** 2.2
        r = 0.6 + 0.7 * rng.uniform() ** 3
        x0, y0 = int(xs), int(ys)
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                xx, yy = x0 + dx, y0 + dy
                if 0 <= xx < W and 0 <= yy < H:
                    d2 = (xx + 0.5 - xs) ** 2 + (yy + 0.5 - ys) ** 2
                    est[yy, xx] = max(est[yy, xx], b * np.exp(-d2 / (2 * r * r)))
        n += 1
    img += est[..., None] * (hexrgb("#DCE6FF") - img)
    # ruído fino (sem bandas no gradiente depois do CRF)
    img += rng.normal(0, 0.45, img.shape)
    return Image.fromarray(np.clip(np.round(img), 0, 255).astype(np.uint8), "RGB")


if __name__ == "__main__":
    im = gera()
    (U / "assets_unidade").mkdir(exist_ok=True)
    im.save(U / "assets_unidade" / "fundo_lab.png")
    im.resize((960, 540), Image.BOX).save(U / "assets_unidade" / "fundo_lab_960x540.png")
    b = io.BytesIO()
    im.save(b, "PNG")
    (U / "threejs" / "cena3d" / "fundo_lab.js").write_text(
        "// gerado por fundo_lab.py (v7): fundo espacial da unidade, o mesmo PNG do Manim\nwindow.FUNDO_LAB = 'data:image/png;base64,"
        + base64.b64encode(b.getvalue()).decode() + "';\n", encoding="utf-8")
    print("ok", im.size, len(b.getvalue()) // 1024, "KB")
