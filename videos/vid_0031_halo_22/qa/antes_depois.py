"""Prancha antes (v6) × depois (v7) dos 10 itens da Parte A.2 do handoff v7, com a conclusão de cada um (regra R0).
Antes: quadros do preview v6 (qa/antes_v6/preview_v6_540x960.mp4, no fim do estado v6 citado). Depois: estados do v7 (qa/quadros/).
Uso (na raiz): uv run python videos/vid_0031_halo_22/qa/antes_depois.py -> qa/prancha_antes_depois_v7.png
"""
import json
from pathlib import Path

import av
from PIL import Image, ImageDraw

QA = Path(__file__).resolve().parent
_V6 = {e['estado']: e['segundos'] for e in json.loads((QA / 'antes_v6' / 'estados_v6.json').read_text(encoding='utf-8'))['eventos']}
ITENS = [  # (nº, problema, estado do v6, estado do v7, conclusão)
    (1, 'C09: cone fraco, pessoa minúscula, sem o céu no fim', 'C09_cone_girando', 'C09_cone_girando',
     'pessoa grande (≈ 17 %), 48 linhas, cone preenchido, eixo no Sol; a borda vira o anel do C01'),
    (2, 'C05: Sol colado, feixe curto, metade vazia', 'C05_oposta', 'C05_oposta',
     'hexágono grande, Sol a ≥ 2,4 do contorno, feixe pelo meio da face, lista embaixo'),
    (3, 'C05: reflexão total sem rótulo', 'C05_vizinha', 'C05_vizinha',
     'entrada rasante pelo meio da face; rótulo junto da face e na lista'),
    (4, 'C04: "aqui: verão" sobre o anel; cristais invisíveis', 'C04_frio', 'C04_frio',
     'o texto sai antes do horizonte; céu azul-profundo; cristais maiores com aresta clara'),
    (5, 'C06: caderno pequeno e ilegível', 'C06_payoff', 'C06_payoff', 'linhas concluídas maiores (esc. 0,72), numeradas'),
    (6, 'C07: mini-caderno no canto', 'C07_grafico', 'C07_grafico', 'o caderno sai; D = i₁ + i₂ − 60° no topo do gráfico'),
    (7, 'C10: texto do zoom cruza a curva; gráfico baixo', 'C10_zoom_curvas', 'C10_zoom_curvas',
     'texto acima do eixo; gráfico até a altura útil; selos maiores'),
    (8, 'C11: céu em faixa estreita; vazio embaixo', 'C11_fios', 'C11_fios', 'anel maior (≥ 4,0), cristal no meio, gráfico maior embaixo'),
    (9, 'C01/C02: mancha atrás do aviso; título e rótulo pequenos', 'C01_raio', 'C01_raio',
     'sem mancha; título maior; rótulo do Sol maior em duas linhas'),
    (10, 'C02: lupa parada e chapada', 'C02_lupa', 'C02_lupa', 'o cristal gira 360° em ~4 s e mostra o corpo do prisma'),
]


def quadros_v6(tempos, w=270, h=480):
    c = av.open(str(QA / 'antes_v6' / 'preview_v6_540x960.mp4'))
    alvo = {round(t * 15) - 1: t for t in tempos}
    out = {}
    for i, f in enumerate(c.decode(video=0)):
        if i in alvo:
            out[alvo[i]] = f.to_image().resize((w, h))
    return out


def main():
    w, h, txt = 270, 480, 520
    antes = quadros_v6([_V6[t] for _, _, t, _, _ in ITENS])
    prancha = Image.new('RGB', (2 * w + txt, (h + 10) * len(ITENS)), (12, 14, 24))
    d = ImageDraw.Draw(prancha)
    for k, (n, prob, e6, est, concl) in enumerate(ITENS):
        t = _V6[e6]
        y = k * (h + 10)
        if t in antes:
            prancha.paste(antes[t], (0, y))
        prancha.paste(Image.open(QA / 'quadros' / f'{est}.png').resize((w, h)), (w, y))
        x = 2 * w + 14
        d.text((x, y + 14), f'{n}. {prob}', fill=(255, 210, 160))
        d.text((x, y + 40), f'antes: v6 {e6} ({t:.1f} s)', fill=(180, 190, 210))
        d.text((x, y + 60), f'depois: v7 {est}', fill=(180, 190, 210))
        for j, parte in enumerate([concl[i:i + 62] for i in range(0, len(concl), 62)]):
            d.text((x, y + 92 + 18 * j), parte, fill=(120, 230, 255))
    prancha.save(QA / 'prancha_antes_depois_v7.png')
    print('ok', len(ITENS))


if __name__ == '__main__':
    main()
