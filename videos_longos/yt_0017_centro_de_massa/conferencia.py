"""Quadros de conferência rápida (handoff v4, §5.3): um quadro de cada estado-chave, localizado pela âncora (log do lote) + fração.
uso: python conferencia.py → renders/conferencia_v4.png (e um PNG por estado em renders/conferencia/)"""
import re
from pathlib import Path

import av
from PIL import Image, ImageDraw

from kit import ANC

U = Path(__file__).resolve().parent
ESTADOS = [("P1", "T1-1", 0.5, "T1-1 haltere (aço com luz B)"), ("P2", "T2-4", 0.72, "T2-4 molas e ⊕"), ("P2", "T2-6", 0.84, "T2-6 soma ponta com ponta"),
           ("P2", "T2-8", 0.8, "T2-8 triângulo no PALCO"), ("P3", "T3-2", 0.8, "T3-2 troca de referencial"), ("P3", "T3-3", 0.5, "T3-3 triângulo"),
           ("P3", "T3-4", 0.27, "T3-4 termo do meio sumindo"), ("P3", "T3-6", 0.75, "T3-6 barras"), ("P4", "T4-3", 0.8, "T4-3 anel"),
           ("P4", "T4-4", 0.78, "T4-4 densidade crescente"), ("P5", "E1-2", 0.85, "E1-2 três triângulos"), ("P5", "E1-3", 0.9, "E1-3 os dois no mesmo ponto"),
           ("P5", "E2-2", 0.8, "E2-2 ⊕ parado"), ("P5", "E2-4", 0.5, "E2-4 não alcança"), ("P5", "EN2", 0.75, "EN2 colisão com o ⊕"), ("P5", "EN3", 0.95, "EN3 prévias")]
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
pr.save(U / "renders" / "conferencia_v4.png")
print("ok", [(n, q) for n, q, _ in ims])
