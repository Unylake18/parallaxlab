"""Prancha de conferência: o quadro do vídeo logo após cada âncora, com a palavra falada. Uso: conferir_ancoras.py VIDEO SAIDA_PREFIXO [nomes...]"""
import json, sys
from pathlib import Path
import av
from PIL import Image, ImageDraw, ImageFont

PASTA = Path(__file__).resolve().parent
V, PRE = sys.argv[1], sys.argv[2]
A = json.loads((PASTA / 'ancoras.json').read_text(encoding='utf-8'))['A']
pal = json.loads((PASTA / 'alinhamento_palavras.json').read_text(encoding='utf-8'))
nomes = sys.argv[3:] or list(A)
fonte = ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf', 22)

def palavras_em(t):
    i = next((k for k, p in enumerate(pal) if p['end'] >= t), len(pal) - 1)
    return ' '.join(p['word'] for p in pal[max(0, i - 1):i + 6])

c = av.open(V); st = c.streams.video[0]
imgs = []
for n in nomes:
    t = A[n] + 0.45
    c.seek(int(t / st.time_base), stream=st)
    for f in c.decode(st):
        if f.time >= t - 0.001:
            im = f.to_image().convert('RGB'); break
    d = ImageDraw.Draw(im)
    d.rectangle([0, im.height - 62, im.width, im.height], fill=(0, 0, 0))
    d.text((6, im.height - 58), f'{n}  voz {A[n]:.2f}s  (quadro em {t:.2f}s)', fill=(120, 230, 255), font=fonte)
    d.text((6, im.height - 30), palavras_em(A[n])[:54], fill=(255, 255, 255), font=fonte)
    imgs.append(im)
w, h = imgs[0].size
for g in range(0, len(imgs), 8):
    lote = imgs[g:g + 8]
    folha = Image.new('RGB', (w * 4, h * ((len(lote) + 3) // 4)))
    for i, im in enumerate(lote): folha.paste(im, ((i % 4) * w, (i // 4) * h))
    folha.save(f'{PRE}_{g // 8 + 1}.png')
print(len(imgs), 'quadros')
