"""Cores das legendas do vid_0027: a mesma cor que a grandeza tem na tela (paleta da cena)."""
FLD = '#EA63FF'   # campo magnético, fluxo, fluxo concatenado, energia, densidade de energia
CUR = '#3FE08B'   # corrente
GEO = '#B8C4DA'   # raio, espiras por metro, comprimento, área, volume, trecho
EMF = '#35D9FF'   # força eletromotriz e potência da fonte

_GRUPOS = {
    FLD: ['campo magnético', 'densidade de energia', 'fluxo concatenado', 'fluxo', 'campo', 'energia'],
    CUR: ['corrente'],
    GEO: ['espiras por metro', 'raio', 'comprimento', 'área', 'volume', 'trecho'],
    EMF: ['força eletromotriz', 'potência'],
}
SUBTITLE_TERM_COLORS = {}
for _cor, _termos in _GRUPOS.items():
    for _t in _termos:
        SUBTITLE_TERM_COLORS[_t] = _cor
        SUBTITLE_TERM_COLORS[_t.capitalize()] = _cor
