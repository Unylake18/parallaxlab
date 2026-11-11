"""Prancha antes (master v9 entregue) × depois (papel v2: violeta liso + grade dos eixos), 960×540 cada."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
D = Path(__file__).parent
PARES = [("T0", "T0 · campo (-y, x)"), ("B1", "B1 · três cartões (2D + 3D)"), ("B2", "B2 · dois painéis (θρ e disco)"), ("B3alg", "B3 · passo de álgebra"),
         ("B4", "B4 · tigela 3D"), ("B5", "B5 · campo radial"), ("B6vel", "B6 · γ′ (violeta)"), ("B7", "B7 · campo 3D"), ("S", "S · resumo")]
f = ImageFont.truetype("arial.ttf", 22)
W, H, M, T = 960, 540, 16, 34
img = Image.new("RGB", (2 * W + 3 * M, len(PARES) * (H + T + M) + M), (20, 20, 24))
d = ImageDraw.Draw(img)
for i, (k, rot) in enumerate(PARES):
    y = M + i * (H + T + M)
    for j, lado in enumerate(("antes", "depois")):
        x = M + j * (W + M)
        p = D / lado / f"{k}.png"
        if p.exists():
            img.paste(Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS), (x, y + T))
        d.text((x, y + 4), f"{'ANTES (v9 entregue)' if j == 0 else 'DEPOIS (papel v2)'} · {rot}", fill=(230, 230, 240), font=f)
img.save(D / "prancha_antes_depois.png")
for k, _ in PARES:      # uma prancha por momento também (2 × 960 lado a lado)
    a, b = D / "antes" / f"{k}.png", D / "depois" / f"{k}.png"
    if a.exists() and b.exists():
        par = Image.new("RGB", (2 * W + 8, H), (20, 20, 24))
        par.paste(Image.open(a).convert("RGB"), (0, 0)); par.paste(Image.open(b).convert("RGB").resize((W, H), Image.LANCZOS), (W + 8, 0))
        par.save(D / f"par_{k}.png")
print("ok")
