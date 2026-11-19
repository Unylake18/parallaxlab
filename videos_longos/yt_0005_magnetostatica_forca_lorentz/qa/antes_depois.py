"""Comparação antes/depois: linhas [quadro da entrega de referência | quadro do render final]. uso: antes_depois.py REF.mp4 NOVO.mp4 SAIDA.png t_ref:t_novo ..."""
import sys, av
from PIL import Image, ImageDraw


def quadro(v, t):
    c = av.open(v)
    s = c.streams.video[0]
    alvo = int(round(t * float(s.average_rate)))
    for i, f in enumerate(c.decode(s)):
        if i >= alvo:
            return f.to_image()


ref, novo, out = sys.argv[1:4]
pares = [tuple(float(x) for x in a.split(":")) for a in sys.argv[4:]]
imgs = [(quadro(ref, a), quadro(novo, b), a, b) for a, b in pares]
w, h = imgs[0][0].size
sheet = Image.new("RGB", (2 * w, len(imgs) * h))
d = ImageDraw.Draw(sheet)
for r, (ia, ib, a, b) in enumerate(imgs):
    sheet.paste(ia, (0, r * h)); sheet.paste(ib, (w, r * h))
    d.text((8, r * h + h - 16), "ANTES (referência) %d:%05.2f" % (int(a) // 60, a % 60), fill=(255, 255, 0))
    d.text((w + 8, r * h + h - 16), "DEPOIS (final) %d:%05.2f" % (int(b) // 60, b % 60), fill=(255, 255, 0))
sheet.save(out)
