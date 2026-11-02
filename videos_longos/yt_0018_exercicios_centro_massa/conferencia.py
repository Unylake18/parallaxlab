"""Quadros de conferência do handoff v2 (§6): um quadro de cada estado-chave, localizado pela âncora (log do lote) + fração.
uso: python conferencia.py → renders/v4/conferencia_v5.png (e um PNG por estado em renders/v4/conferencia/)"""
import re
from pathlib import Path

import av
from PIL import Image, ImageDraw

from kit import ANC

U = Path(__file__).resolve().parent
ESTADOS = [("PH", "H1", 0.6, "H1 gafanhoto na folha"), ("PH", "H2", 0.8, "H2 folha recuando"), ("PX0", "X0-1", 0.9, "X0-1 dados fora do disco"),
           ("PX0", "X1-3", 0.9, "X1-3 massa negativa"), ("PX2", "X2-3b", 0.85, "X2-3b pegadinha"), ("PX3", "X3-1", 0.9, "X3-1 dados no desenho"),
           ("PX3", "X3-3", 0.9, "X3-3 V da folha"), ("PX3", "X3-6", 0.9, "X3-6 condição sen 2θ"), ("PX3", "X3-7", 0.3, "X3-7 limite rasante"),
           ("PX3", "X3-7", 0.9, "X3-7 limite vertical"), ("PX3", "X3-10", 0.9, "X3-10 fecho do gafanhoto"), ("PX4", "X4-2", 0.9, "X4-2 momentos"),
           ("PX4", "X4-4", 0.95, "X4-4 energia → velocidades"), ("PX5", "X5-1", 0.95, "X5-1 travado: 6,0 kg"), ("PX5", "X5-2", 0.15, "X5-2 solto: 5,0 kg"),
           ("PX5", "X5-4", 0.62, "X5-4 T e −T riscando"), ("PX5", "X5-5", 0.4, "X5-5 ⊕ descendo"), ("PX5", "X5-7", 0.95, "X5-7 confere"),
           ("PEP", "EP2", 0.75, "EP2 replay fantasma + ponto ciano"), ("PEP", "S2", 0.95, "S2 cinco ferramentas"), ("PX3", "X3-5", 0.6, "X3-5 voo, câmera recuada (ESCALA ÷3)")]
inicio = {}
for lote in {e[0] for e in ESTADOS}:
    for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", (U / f"log_{lote}.txt").read_text(encoding="utf-8", errors="replace")):
        inicio[(lote, m.group(1))] = float(m.group(2))
(U / "renders" / "v5" / "conferencia").mkdir(parents=True, exist_ok=True)
ims = []
for lote, aid, fr, nome in ESTADOS:
    q = int(round((inicio[(lote, aid)] + fr * ANC[aid]["dur"]) * 15))
    c = av.open(str(U / f"media_{lote}/videos/cena/540p15/{lote}.mp4"))
    im = None
    for i, f in enumerate(c.decode(video=0)):
        im = f.to_image()
        if i >= q:
            break
    c.close()
    im.save(U / "renders" / "v5" / "conferencia" / f"{aid}_{int(fr * 100):02d}.png")
    ims.append((nome, q, im))
W, H = 640, 360
pr = Image.new("RGB", (2 * W, ((len(ims) + 1) // 2) * (H + 20)), "black")
d = ImageDraw.Draw(pr)
for k, (nome, q, im) in enumerate(ims):
    x, y = (k % 2) * W, (k // 2) * (H + 20)
    pr.paste(im.resize((W, H)), (x, y + 20))
    d.text((x + 4, y + 4), f"{nome} · q{q}", fill="yellow")
pr.save(U / "renders" / "v5" / "conferencia_v5.png")
print("ok", [(n, q) for n, q, _ in ims])
