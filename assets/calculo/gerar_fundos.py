"""Gera os fundos de Cálculo (v4 do yt_0026): cor única + brilho central suave, sem degradê vertical nem vinheta; placas lisas atrás do canto e do logo.
Rodar nesta pasta: python gerar_fundos.py"""
import numpy as np
from PIL import Image, ImageFilter
W, H = 1920, 1080
gx, gy = np.arange(W)[None, :] - W / 2, np.arange(H)[:, None] - H / 2
fina = (np.abs((gx + 0.5) % 24 - 12) > 11.4) | (np.abs((gy + 0.5) % 24 - 12) > 11.4)
grossa = (np.abs((gx + 0.5) % 120 - 60) > 59.3) | (np.abs((gy + 0.5) % 120 - 60) > 59.3)
BASE, BRILHO = np.array([0x09, 0x12, 0x26], float), 0.10          # cor única + brilho central suave (sem vinheta)
r = np.hypot(gx / (W * 0.55), gy / (H * 0.55))
liso = np.ones((H, W, 3)) * BASE * (1 + BRILHO * np.exp(-r ** 2))[..., None]
mil = liso + fina[..., None] * np.array([18, 30, 52]) * 0.30 + grossa[..., None] * np.array([40, 70, 120]) * 0.32
# v8: SEM placas no PNG; a placa do canto e a do logo são desenhadas por cena, do tamanho do texto (kit.Base)
rng = np.random.default_rng(7)                      # dithering ±0,5 nível: tira a elipse do brilho central (quantização de 8 bits)
liso = liso + rng.uniform(-0.5, 0.5, liso.shape); mil = mil + rng.uniform(-0.5, 0.5, mil.shape)
for nome, img in (("fundo_calculo_milimetrado", mil), ("fundo_calculo_liso", liso)):
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    im.save(f"{nome}_1920x1080.png"); im.resize((960, 540), Image.LANCZOS).save(f"{nome}_960x540.png")
