"""Folha de comparação yt_0001/yt_0002 × yt_0003 V1.6 (quadros reais lado a lado).

uso: comparar_serie_v1_6.py SAIDA.png  REF1.png:rótulo  YT3.mp4:segundos:rótulo  ...
Cada par (referência, yt_0003) vira uma linha; entradas "ref" são PNGs, "vid" são MP4 + instante.
"""
import sys
from pathlib import Path
import av
from PIL import Image, ImageDraw, ImageFont

saida = Path(sys.argv[1])
pares = []
args = sys.argv[2:]
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 22)


def quadro(video, t):
    with av.open(video) as c:
        for f in c.decode(video=0):
            if f.time + 1e-5 >= t:
                return f.to_image().resize((960, 540))
    raise SystemExit(f'sem quadro em {t}s de {video}')


linhas = []
for i in range(0, len(args), 2):
    ref, vid = args[i], args[i+1]
    rpath, rlabel = ref.rsplit(':', 1)
    vpath, vt, vlabel = vid.rsplit(':', 2)
    im_ref = Image.open(rpath).convert('RGB').resize((960, 540))
    im_vid = quadro(vpath, float(vt))
    linhas.append(((im_ref, rlabel), (im_vid, vlabel)))

sheet = Image.new('RGB', (1920, 575*len(linhas)), '#050816')
d = ImageDraw.Draw(sheet)
for r, ((a, la), (b, lb)) in enumerate(linhas):
    for k, (im, lab) in enumerate(((a, la), (b, lb))):
        sheet.paste(im, (k*960, r*575+35))
        d.text((k*960+18, r*575+5), lab, font=font, fill='white')
sheet.save(saida)
print(saida)
