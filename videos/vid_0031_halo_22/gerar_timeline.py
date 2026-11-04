"""Gera timeline.json do vid_0031 (v3) a partir de roteiro.py: tempos, chaves das camadas 3D, câmera do céu, pontos presos
(centro do Sol, borda interna do anel), perfil do anel e o ESTADO DO CRISTAL POR QUADRO (vértices da face da frente, feixe e
fantasma), que o cena3d.js desenha uma vez só e o Manim relê de roteiro.py.
Uso: uv run python videos/vid_0031_halo_22/gerar_timeline.py
"""
import json
from pathlib import Path

import numpy as np

from fisica import d_min, perfil_anel
from roteiro import (CENAS, DURACAO, E, ESC_HOOK, FPS, FAIXA, FOV_H, MERGULHO, PITCH, SOL_DIR, SOL_MANIM, TAN_V,
                     ZOOM, dir_de_manim, estado_json, manim_de_dir)

UNIT = Path(__file__).resolve().parent
DIR_SETA = -38.       # direção na tela (graus) em que a seta 22° vai do Sol até a borda interna


def no_cone(s, ang, phi_tela):
    """Direção a 'ang' graus do Sol s, no rumo (tangente) que sai do Sol na direção 'phi_tela' da tela."""
    alvo = manim_de_dir(s) + .01 * np.array([np.cos(np.radians(phi_tela)), np.sin(np.radians(phi_tela))])
    t = dir_de_manim(*alvo) - s
    t -= (t @ s) * s
    t /= np.linalg.norm(t)
    a = np.radians(ang)
    return np.cos(a) * s + np.sin(a) * t


def curva_cone(s, ang, n=361):
    """Borda do cone de 'ang' graus em volta de s, projetada na tela (Manim)."""
    e1 = np.cross(s, [0, 1, 0]); e1 /= np.linalg.norm(e1)
    e2 = np.cross(s, e1)
    a = np.radians(ang)
    return [manim_de_dir(np.cos(a) * s + np.sin(a) * (np.cos(q) * e1 + np.sin(q) * e2)).round(4).tolist()
            for q in np.linspace(0, 2 * np.pi, n)]


def tom_v2(rgb):
    """Cor de apresentação do anel: o brilho de fisica.perfil_anel fica igual; o tom vira corpo branco-azulado com borda
    interna quente e fina (#FFB08A) onde o vermelho excede o violeta (e recuperado do canal azul: 1 − 0,68·e)."""
    b = rgb.max(1)
    tom = rgb / np.where(b > 1e-9, b, 1)[:, None]
    e = np.clip((1 - tom[:, 2]) / .68, 0, 1)
    corpo, quente = np.array([.90, .94, 1.]), np.array([1., .69, .54])
    return b[:, None] * (corpo + .85 * e[:, None] ** 2 * (quente - corpo))      # e²: borda quente mais fina


def main():
    s = SOL_DIR
    borda = manim_de_dir(no_cone(s, d_min(), DIR_SETA))
    angs, rgb = perfil_anel()
    rgb = tom_v2(rgb)
    k = lambda *pares: [{'t': t, 'v': v} for t, v in pares]
    n = round(DURACAO * FPS)
    f0 = round((E['lupa'] - .3) * FPS)                  # v4: o cristal aparece já na lupa do C02
    cristal = [estado_json(f / FPS) for f in range(f0, n)]
    tl = {
        '_leia_me': 'Fonte única de tempos e pontos presos do vid_0031 (gerada por gerar_timeline.py a partir de roteiro.py; '
                    'não editar à mão). Tempos = orçamento da fala v3 (490 palavras, ≤ 180 s); preview silencioso v3.',
        'duracao_s': DURACAO,
        'cenas': [{'id': c, 'inicio_s': a, 'fim_s': b} for c, a, b in CENAS],
        'eventos': E,
        'layout': {'legenda_y': [-6.0, -4.67], 'conteudo_min_y': -4.5},
        'camadas': {
            # céu: C01 (hook: o halo solar, sem poste e sem chão), C04 (sobe do verão até o véu), fim do C09 (o cone vira o céu),
            # C10 (cores), C11 (terço de cima)
            'ceu': k((0, 1), (E['c02'] - .2, 1), (E['c02'] + .2, 0), (E['c04'] - .2, 0), (E['c04'] + .2, 1), (E['globo'] - .4, 1),
                     (E['globo'], 0), (E['ceu_volta'] - .05, 0), (E['ceu_volta'] + .4, 1), (E['cores'] - .25, 1), (E['cores'] + .15, 0),
                     (E['ceu_cores'], 0), (E['ceu_cores'] + .5, 1), (E['sintese'] - .45, 1), (E['sintese'] - .3, 0),
                     (E['sintese'] - .29, 1), (E['cta'], 1), (E['cta'] + .5, 0)),
            'acende': k((0, 0), (E['acende'], 0), (E['acende'] + 2.0, 1), (E['sintese'] - .5, 1), (E['sintese'] - .45, 0), (E['halo11'] - .2, 0),
                        (E['halo11'] + 1.0, 1)),     # v8: o halo da faixa do C11 acende em "aparece o halo"
            'lugar': k((0, 0), (DURACAO, 0)),
            'poste': k((0, 0), (DURACAO, 0)),
            'chao': k((0, 0), (DURACAO, 0)),
            'sol': k((0, 1), (DURACAO, 1)),
            'inclina': k((0, 0), (E['c04'] - .2, 0), (E['c04'] - .1, -26), (E['c04'] + .5, -26), (E['c04'] + 3.6, 38),
                         (E['globo'], 38), (E['globo'] + .1, 0)),
            'veu': k((0, 0), (E['c04'] + 1.6, 0), (E['c04'] + 3.6, .7), (E['globo'], .7), (E['globo'] + .1, 0)),
            'cristais': k((0, 0), (E['c04'] + 2.6, 0), (E['c04'] + 3.3, .85), (E['globo'] - .6, .85), (E['globo'] - .1, 0)),
            # zoom/translação da vista do céu (tela = tr + esc · vista)
            'esc': k((0, 1.0), (E['mergulho'], ESC_HOOK), (E['c02'], MERGULHO[0]), (E['c02'] + .25, MERGULHO[0]),
                     (E['c02'] + .26, 1.0), (E['ceu_cores'], 1.0), (E['zoom'] + .9, ZOOM[0]), (E['sintese'] - .31, ZOOM[0]),
                     (E['sintese'] - .3, FAIXA[0]), (DURACAO, FAIXA[0])),
            'tx': k((0, 0), (E['mergulho'], 0), (E['c02'], MERGULHO[1][0]), (E['c02'] + .25, MERGULHO[1][0]), (E['c02'] + .26, 0),
                    (E['zoom'], 0), (E['zoom'] + .9, ZOOM[1][0]), (E['sintese'] - .31, ZOOM[1][0]), (E['sintese'] - .3, FAIXA[1][0]),
                    (DURACAO, FAIXA[1][0])),
            'ty': k((0, 0), (E['mergulho'], (1 - ESC_HOOK) * SOL_MANIM[1]), (E['c02'], MERGULHO[1][1]), (E['c02'] + .25, MERGULHO[1][1]), (E['c02'] + .26, 0),
                    (E['zoom'], 0), (E['zoom'] + .9, ZOOM[1][1]), (E['sintese'] - .31, ZOOM[1][1]), (E['sintese'] - .3, FAIXA[1][1]),
                    (DURACAO, FAIXA[1][1])),
            'faixa': k((0, 0), (E['sintese'] - .31, 0), (E['sintese'] - .3, 1), (DURACAO, 1)),
        },
        'ceu': {
            'pitch_deg': PITCH, 'fov_h_deg': FOV_H, 'fov_v_deg': round(2 * np.degrees(np.arctan(TAN_V)), 3),
            'sol_manim': list(SOL_MANIM), 'sol_dir': s.round(6).tolist(), 'sol_raio_manim': .13,
            'borda_interna_deg': round(float(d_min()), 4), 'borda_manim': borda.round(4).tolist(), 'dir_seta_tela_deg': DIR_SETA,
            'poste': {'x_inicio_manim': 6.2, 'x_final_manim': SOL_MANIM[0], 'largura_manim': .62, 'topo_manim': SOL_MANIM[1] + 1.9},
            'curva_22': curva_cone(s, d_min()),
            'curva_24': curva_cone(s, d_min() + 2.),
        },
        'perfil_anel': {'a0_deg': float(angs[0]), 'passo_deg': .1, 'rgb': rgb.round(4).tolist()},
        'heroi': {'centro_manim': [1.75, .95], 'raio_manim': .85, 'comprimento': 2.4},   # cristal-coluna preso à câmera (C02)
        'cristal': {'fps': FPS, 'quadro_inicial': f0, 'raio_3d': 1.0, 'comprimento_3d': 2.4, 'fov_v_deg': 18.,
                    'desloc_camera': [-.22, .3], 'quadros': cristal},
    }
    (UNIT / 'timeline.json').write_text(json.dumps(tl, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    c = np.array(tl['ceu']['curva_22'])
    print('sol', SOL_MANIM, 'borda', borda.round(3), 'anel x', c[:, 0].min().round(2), c[:, 0].max().round(2),
          'y', c[:, 1].min().round(2), c[:, 1].max().round(2), '| quadros de cristal', sum(q is not None for q in cristal))


if __name__ == '__main__':
    main()
