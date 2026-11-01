"""Cores da legenda do vid_0025: a mesma cor que a grandeza tem na tela (paleta da cena).
Usado por videos/montar_legendado.py (--color-module) e por gerar_legenda.py (frases coloridas nunca quebram entre linhas)."""
VIOLET = "#745CFF"   # i, ângulo de incidência
PINK = "#EA63FF"     # r, ângulo de refração
CYAN = "#35D9FF"     # θ, 42°, máximo
RED = "#FF4B4B"      # vermelho (42,4°)
VIO = "#9B5CFF"      # violeta (40,6°)
WARM = "#FFC857"     # Sol e direção antissolar (referência dos 42°)

_GRUPOS = {
    VIOLET: ["incidência", "cinquenta e nove graus"],
    PINK: ["refração", "refrata", "quarenta"],                    # "quarenta" sozinho = r = 40,2° ("refração de quarenta...")
    CYAN: ["quarenta e dois graus", "máximo"],
    RED: ["vermelho", "quarenta e dois vírgula quatro graus", "quarenta e dois vírgula", "vírgula quatro graus", "quatro graus", "quarenta e dois"],
    VIO: ["violeta", "quarenta vírgula seis"],
    WARM: ["Sol", "antissolar"],
}
SUBTITLE_TERM_COLORS = {}
for _cor, _termos in _GRUPOS.items():
    for _t in _termos:
        SUBTITLE_TERM_COLORS[_t] = _cor
        SUBTITLE_TERM_COLORS[_t[0].upper() + _t[1:]] = _cor
