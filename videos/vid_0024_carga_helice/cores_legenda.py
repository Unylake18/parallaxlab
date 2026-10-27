"""Cores das legendas do vid_0024: a mesma cor que a grandeza tem na tela (paleta da cena)."""
BLUE_L = '#5AA2FF'     # campo magnético (B)
PINK = '#EA63FF'       # força magnética (F)
VIOLET = '#9C8CFF'     # componente perpendicular (v⊥) e giro
PARALLEL = '#63E6BE'   # componente paralela (v∥), avanço e passo
CYAN = '#35D9FF'       # trajetória, raio e período (resultados em caixa ciano)

_GRUPOS = {
    BLUE_L: ['campo magnético', 'campo'],
    PINK: ['força magnética', 'força centrípeta', 'força', 'forças'],
    VIOLET: ['componente perpendicular', 'componentes perpendicular', 'perpendicular', 'perpendiculares',
             'frequência angular', 'giro', 'gira'],
    PARALLEL: ['componente paralela', 'paralela', 'paralelo', 'avanço', 'avança', 'passo da hélice', 'passo'],
    CYAN: ['hélice', 'círculo', 'reta', 'raio', 'período', 'trajetória', 'caminho'],
}
SUBTITLE_TERM_COLORS = {}
for _cor, _termos in _GRUPOS.items():
    for _t in _termos:
        SUBTITLE_TERM_COLORS[_t] = _cor
        SUBTITLE_TERM_COLORS[_t.capitalize()] = _cor
