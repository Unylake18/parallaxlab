"""yt_0027: fundo milimetrado da unidade (cópia de assets/calculo/gerar_fundos.py, sem alterar o global).
Única mudança (pedido do Kaio, 2026-11-10): o canto sobe para a altura do logo e a placa lisa atrás dele encolhe para o tamanho do texto
(x 0–700, y 22–124 px a 1080p, em vez de x 0–1240, y 72–170). A placa do logo fica igual. Grava em renders/fundo/ (uma vez).
uso: python fundo27.py  (ou kit._mil(), que gera sob demanda)"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

AQUI = Path(__file__).resolve().parent
SAIDA = AQUI / "renders" / "fundo"
PLACA_CANTO = (22, 124, 0, 700)        # y0, y1, x0, x1 (px a 1080p)


def gera():
    W, H = 1920, 1080
    gx, gy = np.arange(W)[None, :] - W / 2, np.arange(H)[:, None] - H / 2
    fina = (np.abs((gx + 0.5) % 24 - 12) > 11.4) | (np.abs((gy + 0.5) % 24 - 12) > 11.4)
    grossa = (np.abs((gx + 0.5) % 120 - 60) > 59.3) | (np.abs((gy + 0.5) % 120 - 60) > 59.3)
    BASE, BRILHO = np.array([0x09, 0x12, 0x26], float), 0.10
    r = np.hypot(gx / (W * 0.55), gy / (H * 0.55))
    liso = np.ones((H, W, 3)) * BASE * (1 + BRILHO * np.exp(-r ** 2))[..., None]
    mil = liso + fina[..., None] * np.array([18, 30, 52]) * 0.30 + grossa[..., None] * np.array([40, 70, 120]) * 0.32
    m = np.zeros((H, W))
    y0, y1, x0, x1 = PLACA_CANTO
    m[y0:y1, x0:x1] = 1
    m[34:96, 1656:1920] = 1
    m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(16)), float)[..., None] / 255
    mil = mil * (1 - m) + liso * m
    rng = np.random.default_rng(7)
    mil = mil + rng.uniform(-0.5, 0.5, mil.shape)
    SAIDA.mkdir(parents=True, exist_ok=True)
    im = Image.fromarray(np.clip(mil, 0, 255).astype(np.uint8))
    im.save(SAIDA / "fundo27_milimetrado_1920x1080.png")
    im.resize((960, 540), Image.LANCZOS).save(SAIDA / "fundo27_milimetrado_960x540.png")


if __name__ == "__main__":
    gera()
    print("ok", SAIDA)
