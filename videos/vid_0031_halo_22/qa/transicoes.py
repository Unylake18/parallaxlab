"""Prancha das transições de equação do vid_0031 (§B.8): quadros a 30 %, 50 % e 70 % de cada transformação, recortados na
faixa da equação, a partir do preview composto. → qa/prancha_transicoes.png
Uso (na raiz): uv run python videos/vid_0031_halo_22/qa/transicoes.py
"""
import json
from pathlib import Path

import av
from PIL import Image, ImageDraw

QA = Path(__file__).resolve().parent
UNIT = QA.parent


def main():
    g = json.loads((UNIT / 'media_preview' / 'qa_geometria.json').read_text(encoding='utf-8'))
    trs = g['transicoes']
    alvos = {}
    for k, t in enumerate(trs):
        for p in (.3, .5, .7):
            alvos.setdefault(t['quadro0'] + int(round(p * t['quadros'])), []).append((k, p))
    c = av.open(str(UNIT / 'renders' / 'preview_540x960.mp4'))
    W, H, banda = 540, 960, 150
    quadros = {}
    for i, f in enumerate(c.decode(video=0)):
        if i in alvos:
            im = f.to_image()
            for k, p in alvos[i]:
                y = (8 - trs[k]['y']) * H / 16
                quadros[(k, p)] = im.crop((0, int(y - banda / 2), W, int(y + banda / 2)))
    cab = 26
    prancha = Image.new('RGB', (W * 3, (banda + cab) * len(trs)), (12, 14, 24))
    d = ImageDraw.Draw(prancha)
    for k, t in enumerate(trs):
        for j, p in enumerate((.3, .5, .7)):
            if (k, p) in quadros:
                prancha.paste(quadros[(k, p)], (W * j, k * (banda + cab) + cab))
            d.text((W * j + 6, k * (banda + cab) + 6), f"{t['nome']}  ·  {int(100 * p)} %", fill=(230, 230, 240))
    prancha.save(QA / 'prancha_transicoes.png')
    print(f'{len(quadros)} recortes de {len(trs)} transições')


if __name__ == '__main__':
    main()
