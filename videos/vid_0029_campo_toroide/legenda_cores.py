"""Cores da legenda do vid_0029 (lido por videos/montar_legendado.py --color-module).

Mesmas cores das grandezas na tela: B magenta, corrente verde, geometria (raios, disco) cinza-claro.
O artigo "a" fica de fora (casaria com o artigo); o raio da seção aparece como "raio do tubo".
"""
MAG, GREEN, GEO = '#EA63FF', '#3FE08B', '#B8C4DA'

SUBTITLE_TERM_COLORS = {
    'campo magnético': MAG, 'campo': MAG, 'Campo': MAG,
    'corrente': GREEN, 'Corrente': GREEN, 'I': GREEN,
    'raio do caminho': GEO, 'raio médio': GEO, 'raio do tubo': GEO, 'raio': GEO, 'R': GEO, 'r': GEO, 'disco': GEO,
}
