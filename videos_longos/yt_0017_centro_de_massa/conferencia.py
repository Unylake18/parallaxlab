"""Quadros de conferência rápida (handoff v4, §5.3): um quadro de cada estado-chave, localizado pela âncora (log do lote) + fração.
uso: python conferencia.py → renders/conferencia_v6.png (e um PNG por estado em renders/conferencia/)"""
import re
from pathlib import Path

import av
from PIL import Image, ImageDraw

from kit import ANC

U = Path(__file__).resolve().parent
ESTADOS = [("P3", "T3-4", 0.215, "T3-4 a chave do 0⃗ no termo do meio"), ("P3", "T3-4", 0.27, "T3-4 logo depois do sumiço"),
           ("P2", "T2-8", 0.8, "T2-8 triângulo: ANTES tracejada, DEPOIS cheia, ΔV⃗_cm"), ("P2", "T2-6", 0.84, "T2-6 rótulos de massa"),
           ("P5", "EN1", 0.43, "EN1 passo 1: v_f = V_cm"), ("P5", "EN1", 0.5, "EN1 passo 3: (m₁v₁ᵢ + m₂v₂ᵢ)/(m₁ + m₂)"),
           ("P5", "EN1", 0.54, "EN1 passo 4: ⅔ m/s"), ("P5", "EN1", 0.17, "EN1 grudados: 3 kg")]
inicio = {}
for lote in {e[0] for e in ESTADOS}:
    for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", (U / f"log_{lote}.txt").read_text(encoding="utf-8", errors="replace")):
        inicio[(lote, m.group(1))] = float(m.group(2))
(U / "renders" / "conferencia").mkdir(parents=True, exist_ok=True)
ims = []
for lote, aid, fr, nome in ESTADOS:
    q = int(round((inicio[(lote, aid)] + fr * ANC[aid]["dur"]) * 15))
    c = av.open(str(U / f"media_{lote}/videos/cena/540p15/{lote}.mp4"))
    for i, f in enumerate(c.decode(video=0)):
        if i == q:
            im = f.to_image()
            break
    c.close()
    im.save(U / "renders" / "conferencia" / f"{aid}_{int(fr * 100):02d}.png")
    ims.append((nome, q, im))
W, H = 640, 360
pr = Image.new("RGB", (2 * W, ((len(ims) + 1) // 2) * (H + 20)), "black")
d = ImageDraw.Draw(pr)
for k, (nome, q, im) in enumerate(ims):
    x, y = (k % 2) * W, (k // 2) * (H + 20)
    pr.paste(im.resize((W, H)), (x, y + 20))
    d.text((x + 4, y + 4), f"{nome} · q{q}", fill="yellow")
pr.save(U / "renders" / "conferencia_v6.png")
print("ok", [(n, q) for n, q, _ in ims])
