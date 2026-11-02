"""Cores da legenda do vid_0032 (lido por videos/montar_legendado.py --color-module e por gerar_legenda.py).

Mesmas cores das grandezas na tela: campo elétrico e ondas em ciano, calor e E² em laranja, comprimento de onda e
distância entre as manchas em cinza-claro (GEO), frequência em violeta.
"""
CYAN, HEAT, GEO, VIO = '#35D9FF', '#FF7A3D', '#B8C4DA', '#9C8CFF'

_GRUPOS = {
    CYAN: ['campo elétrico', 'onda estacionária', 'micro-ondas'],
    HEAT: ['ao quadrado', 'pico de calor', 'média do quadrado', 'calor'],
    GEO: ['meio comprimento de onda', 'comprimento de onda', 'distância entre as manchas', 'distância',
          'seis vírgula um centímetros', 'doze vírgula dois centímetros'],
    VIO: ['dois mil quatrocentos e cinquenta megahertz', 'novecentos e quinze megahertz', 'megahertz', 'frequência'],
}
SUBTITLE_TERM_COLORS = {}
for _cor, _termos in _GRUPOS.items():
    for _t in _termos:
        SUBTITLE_TERM_COLORS[_t] = _cor
        SUBTITLE_TERM_COLORS[_t[0].upper() + _t[1:]] = _cor
