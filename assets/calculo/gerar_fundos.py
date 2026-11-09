import numpy as np
from PIL import Image
W, H = 1920, 1080
y = np.linspace(0, 1, H)[:, None]; x = np.linspace(0, 1, W)[None, :]
c0, c1 = np.array([0x0F, 0x1B, 0x33], float), np.array([0x0A, 0x13, 0x26], float)
liso = c0 * (1 - y[..., None]) + c1 * y[..., None] + 0 * x[..., None]
vin = (1 - 0.45 * np.clip(np.hypot((x - .5) / .75, (y - .5) / .75) - .35, 0, 1) ** 1.5)[..., None]
gx, gy = np.arange(W)[None, :] - W / 2, np.arange(H)[:, None] - H / 2
fina = (np.abs((gx + 0.5) % 24 - 12) > 11.4) | (np.abs((gy + 0.5) % 24 - 12) > 11.4)
grossa = (np.abs((gx + 0.5) % 120 - 60) > 59.3) | (np.abs((gy + 0.5) % 120 - 60) > 59.3)
mil = liso + fina[..., None] * np.array([18, 30, 52]) * 0.30 + grossa[..., None] * np.array([40, 70, 120]) * 0.32
for nome, img in (("fundo_calculo_milimetrado", mil * vin), ("fundo_calculo_liso", liso * vin)):
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    im.save(f"{nome}_1920x1080.png"); im.resize((960, 540), Image.LANCZOS).save(f"{nome}_960x540.png")
