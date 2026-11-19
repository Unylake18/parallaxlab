"""Cores da legenda do vid_0030: a mesma cor que a grandeza tem na tela (h magenta; raio do furo a violeta; altura do corte
z em GEO; R e o restante em branco). Usado por videos/montar_legendado.py (--color-module) e por gerar_legenda.py (frases
coloridas nunca quebram entre linhas). O termo mais longo vence ("altura do corte" é z, não h)."""
H = "#EA63FF"     # altura h do anel, metade da altura h/2 e as potências dela, os 6 cm
A = "#9C8CFF"     # raio do furo a (o raio de dentro da coroa é o próprio a)
GEO = "#B8C4DA"   # altura do corte z

_GRUPOS = {
    H: ["altura", "mesma altura", "metade da altura", "quadrado da metade da altura", "cubo da metade da altura",
        "cubo da metade", "altura ao cubo", "altura do anel", "seis centímetros"],
    A: ["raio do furo", "raio de dentro"],
    GEO: ["altura do corte", "altura qualquer"],
}
SUBTITLE_TERM_COLORS = {}
for _cor, _termos in _GRUPOS.items():
    for _t in _termos:
        SUBTITLE_TERM_COLORS[_t] = _cor
        SUBTITLE_TERM_COLORS[_t[0].upper() + _t[1:]] = _cor
