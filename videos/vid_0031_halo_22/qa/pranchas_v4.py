"""Pranchas do v4 (§B.11): (1) o mínimo no gráfico em C08, C09 e C10, em 540 px, mostrando o 21,8° no eixo vertical;
(2) pessoa e Sol: o still de referência (funções originais do vid_0025 × cópias) ao lado da cena de lado e da comparação do v4.
Uso (na raiz): uv run python videos/vid_0031_halo_22/qa/pranchas_v4.py
"""
from pathlib import Path

from PIL import Image, ImageDraw

QA = Path(__file__).resolve().parent
REF = QA.parent / 'media_ref' / 'images' / 'ref_vid0025' / 'RefPessoaSol_ManimCE_v0.21.0.png'


def lado_a_lado(imgs, rotulos, saida):
    w, h = 540, 960
    p = Image.new('RGB', (w * len(imgs), h + 30), (12, 14, 24))
    d = ImageDraw.Draw(p)
    for k, (im, r) in enumerate(zip(imgs, rotulos)):
        p.paste(im.resize((w, h)), (w * k, 30))
        d.text((w * k + 8, 8), r, fill=(230, 230, 240))
    p.save(QA / saida)


def main():
    q = lambda n: Image.open(QA / 'quadros' / f'{n}.png')
    lado_a_lado([q('C08_payoff'), q('C09_parede'), q('C10_sintese')],
                ['C08 payoff: 21,8° no eixo vertical; i ~ 40,9° embaixo', 'C09: parede no 21,8° (eixo vertical)', 'C10 síntese: o vale com 21,8°'],
                'prancha_grafico.png')
    lado_a_lado([Image.open(REF), q('C02_cena'), q('C03_comparacao')],
                ['vid_0025 original × cópia', 'v4 C02: pessoa (espelhada) e Sol', 'v4 C03: comparação'], 'prancha_pessoa_sol.png')
    print('ok')


if __name__ == '__main__':
    main()
