"""Sequência de quadros (escrita em ordem): python _seq.py MP4 t0 t1 [fps=10] [x0 y0 x1 y1] [saida] → renders/_seq.png
Recorta a região da CONTA (padrão x 480…960, y 60…330 em 960×540) e empilha os quadros em grade."""
import sys
from pathlib import Path
import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
mp4, t0, t1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
fps = float(sys.argv[4]) if len(sys.argv) > 4 else 10.0
box = tuple(int(v) for v in sys.argv[5:9]) if len(sys.argv) >= 9 else (480, 60, 960, 330)
saida = Path(sys.argv[9]) if len(sys.argv) > 9 else U / "renders" / "_seq.png"
c = av.open(mp4)
src_fps = float(c.streams.video[0].average_rate)
passo = max(1, round(src_fps / fps))
alvo = set(range(int(t0 * src_fps), int(t1 * src_fps) + 1, passo))
quadros = []
for f, fr in enumerate(c.decode(video=0)):
    if f in alvo:
        im = fr.to_image().crop(box)
        ImageDraw.Draw(im).text((4, 4), f"{f / src_fps:.2f}s", fill=(255, 255, 0))
        quadros.append(im)
    if f > t1 * src_fps:
        break
cols = 3
w, h = quadros[0].size
lin = (len(quadros) + cols - 1) // cols
pr = Image.new("RGB", (w * cols, h * lin))
for i, im in enumerate(quadros):
    pr.paste(im, ((i % cols) * w, (i // cols) * h))
pr.save(saida)
print(saida, len(quadros), "quadros")
