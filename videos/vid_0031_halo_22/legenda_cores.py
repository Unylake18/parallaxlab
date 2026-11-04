"""Cores da legenda do vid_0031 (lido por videos/montar_legendado.py --color-module e por gerar_legenda.py).

Mesmas cores das grandezas na tela: desvio e 60° em ciano, incidência em violeta, refração em magenta,
vermelho e violeta do espectro nas cores das curvas, Sol em âmbar, gelo em azul-gelo.
"""
CYAN, VIO, MAG, RED, VIOC, SOL, GELO = '#35D9FF', '#745CFF', '#EA63FF', '#FF5A4A', '#9B7BFF', '#FFC857', '#CFE8FF'

_GRUPOS = {
    CYAN: ['desvio', 'sessenta graus', 'vinte e dois graus', 'vinte e um vírgula oito'],
    VIO: ['incidência', 'incidências'],
    MAG: ['refração', 'refrações'],
    RED: ['vermelho', 'vinte e um vírgula sete'],
    VIOC: ['violeta', 'vinte e dois vírgula cinco'],
    SOL: ['Sol', 'raios paralelos'],
    GELO: ['gelo', 'cristal', 'cristais'],
}
SUBTITLE_TERM_COLORS = {}
for _cor, _termos in _GRUPOS.items():
    for _t in _termos:
        SUBTITLE_TERM_COLORS[_t] = _cor
        SUBTITLE_TERM_COLORS[_t[0].upper() + _t[1:]] = _cor
