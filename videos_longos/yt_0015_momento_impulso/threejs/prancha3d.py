"""python prancha3d.py pasta saida.png n1 n2 ... → prancha 3 colunas dos quadros f<n>.png"""
import sys
from PIL import Image
pasta, saida, ns = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3:]]
ims = [Image.open(f"{pasta}/f{n:05d}.png") for n in ns]
w, h = ims[0].size
sh = Image.new("RGB", (3 * w, ((len(ims) + 2) // 3) * h))
for i, im in enumerate(ims):
    sh.paste(im, ((i % 3) * w, (i // 3) * h))
sh.save(saida)
