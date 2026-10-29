"""Prancha de conferência de um lote: quadros escolhidos (ou espaçados) do preview, com o tempo em cada miniatura.
uso: python prancha.py LOTE saida.png [q1 q2 ...]  (sem quadros: 18 espaçados)"""
import sys

import av
from PIL import Image, ImageDraw

lote, saida = sys.argv[1], sys.argv[2]
c = av.open(f"media_{lote}/videos/cena/540p15/{lote}.mp4")
n = c.streams.video[0].frames
alvo = [int(x) for x in sys.argv[3:]] or [int(i * (n - 1) / 17) for i in range(18)]
ims = {i: fr.to_image() for i, fr in enumerate(c.decode(video=0)) if i in alvo}
W, H, C = 640, 360, 3
L = (len(alvo) + C - 1) // C
pr = Image.new("RGB", (W * C, (H + 18) * L), "black")
d = ImageDraw.Draw(pr)
for k, i in enumerate(alvo):
    x, y = (k % C) * W, (k // C) * (H + 18)
    if i in ims:
        pr.paste(ims[i].resize((W, H)), (x, y + 18))
    d.text((x + 4, y + 3), f"q{i}  {int(i / 15 // 60)}:{i / 15 % 60:04.1f}", fill="yellow")
pr.save(saida)
print(n, "quadros")
