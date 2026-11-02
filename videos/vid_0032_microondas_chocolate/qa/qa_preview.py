"""QA do preview do vid_0032: prancha de quadros (um por bloco + troca 3D → 2D) e faixa da legenda vazia.

Faixa: fora do 3D (27–106 s e 144 s até o fim), toda linha abaixo de y = −4,5 (Manim) tem de ser a cor de fundo (tolerância do H.264).
Uso (na raiz): uv run python videos/vid_0032_microondas_chocolate/qa/qa_preview.py [renders/preview_540x960.mp4]
"""
import json
import sys
from pathlib import Path

import av
import numpy as np
from PIL import Image, ImageDraw

UNIT = Path(__file__).resolve().parents[1]
TL = json.loads((UNIT / 'timeline.json').read_text(encoding='utf-8'))
EV = TL['eventos']
QUADROS = [('C01 macro', 1.5), ('C01 manchete', 5.5), ('C01 salto', 9.5), ('C01 régua 3', 10.8), ('C01 etiqueta', 15.5),
           ('C01 forno por fora', 18.0), ('C01 prato parado', 19.3), ('C01 chip 1', 21.5), ('C01 chip 2', 24.0), ('C01 chip 3', 26.0),
           ('C02 bate e volta', 29.0), ('C02 estacionária', 35.0), ('C02 nós e ventres', 43.5), ('C03 vetor', 47.0),
           ('C03 MF1/MF2 +E', 50.5), ('C03 MF2 -E', 52.5), ('C03b média', 57.5), ('C03c chaves', 62.5), ('C03d manchas', 66.5),
           ('C04 L1 + régua', 72.0), ('C04 L1 12,2', 78.5), ('C04 L2 etiqueta', 82.0), ('C04 viajante', 88.5), ('C04 L3', 92.0),
           ('C04 c=2df', 98.5), ('C04 L4', 100.3), ('C04 resultado', 103.5), ('C04 pulso', 105.3),
           ('C05 caixa', 108.0), ('C05 relevo', 112.0), ('C05 gotas', 118.0), ('C06 parado', 123.0), ('C06 gira 128', 128.0),
           ('C06 gira 131', 131.0), ('C06 média', 133.5), ('C06 anel', 135.0), ('C06 centro', 137.0), ('C06 fim', 142.5),
           ('C07 143,7', 143.7), ('C07 145', 145.0), ('C07 148', 148.0), ('C07 CTA', 150.5), ('C07 último', 151.9)]
FAIXA = [(27.2, 106.4), (144.2, 152)]       # sem 3D: a faixa da legenda tem de ser só fundo (no 3D o Manim não desenha lá)
TROCAS = [27.2, 45.3, 68.0, 106.8, 119.8, 143.6]
# transições do C04 (S22–S25): quadros soltos a cada 0,2 s, recortados na zona das contas
C04_TRANS = [round(73.6 + .2 * k, 1) for k in range(40)] + [round(98.4 + .2 * k, 1) for k in range(26)]


def main():
    mp4 = UNIT / (sys.argv[1] if len(sys.argv) > 1 else 'renders/preview_540x960.mp4')
    c = av.open(str(mp4))
    st = c.streams.video[0]
    fps = float(st.average_rate)
    alvo = {round(t * fps): (n, t) for n, t in QUADROS + [(f'troca {x:g} s', x) for x in TROCAS]}
    bg = np.array([5, 8, 22])
    alvoT = {round(t * fps): t for t in C04_TRANS}
    pega, pegaT, pior, pior_t, n = {}, {}, 0., None, 0
    y_lim = round((8 + 4.5) / 16 * 960 * st.height / 960)
    for i, fr in enumerate(c.decode(video=0)):
        a = fr.to_ndarray(format='rgb24')
        n += 1
        if i in alvo:
            pega[i] = a
        if i in alvoT:
            pegaT[i] = a
        t = i / fps
        if any(a + .05 < t < b for a, b in FAIXA):
            d = np.abs(a[y_lim + 2:].astype(int) - bg).max()
            if d > pior:
                pior, pior_t = d, round(t, 2)
    dur = n / fps
    print(json.dumps({'quadros': n, 'duracao_s': round(dur, 3), 'faixa_abaixo_y-4.5_desvio_max': int(pior), 'no_instante_s': pior_t}))
    w, h = 270, 480
    cols = 6
    rows = (len(alvo) + cols - 1) // cols
    P = Image.new('RGB', (cols * (w + 4), rows * (h + 22)), (30, 30, 30))
    d = ImageDraw.Draw(P)
    for k, i in enumerate(sorted(pega)):
        x, y = (k % cols) * (w + 4), (k // cols) * (h + 22)
        P.paste(Image.fromarray(pega[i]).resize((w, h)), (x, y))
        nome, t = alvo[i]
        d.text((x + 4, y + h + 5), f'{t:.1f}s  {nome}', fill=(225, 225, 225))
    suf = '_v5' if 'v5' in mp4.name else '_v4' if 'v4' in mp4.name else '_v3' if 'v3' in mp4.name else '_v2' if 'v2' in mp4.name else ''
    P.save(UNIT / 'qa' / ('prancha_preview' + suf + '.png'))
    cw, ch, ccols = 270, 230, 9
    T = Image.new('RGB', (ccols * (cw + 2), ((len(pegaT) + ccols - 1) // ccols) * (ch + 14)), (30, 30, 30))
    dT = ImageDraw.Draw(T)
    for k, i in enumerate(sorted(pegaT)):
        x, y = (k % ccols) * (cw + 2), (k // ccols) * (ch + 14)
        T.paste(Image.fromarray(pegaT[i]).resize((cw, 480)).crop((0, 100, cw, 100 + ch)), (x, y))
        dT.text((x + 4, y + ch + 1), f'{alvoT[i]:.1f}s', fill=(225, 225, 225))
    T.save(UNIT / 'qa' / ('c04_transicoes' + suf + '.png'))
    for i, a in pega.items():
        if alvo[i][0].startswith('troca 27'):
            Image.fromarray(a).save(UNIT / 'qa' / f'troca_3d_2d{suf}.png')


if __name__ == '__main__':
    main()
