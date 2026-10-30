"""Cores da legenda do vid_0028: a mesma cor que a grandeza tem na tela (A violeta, B e v_B′ ciano, 1,6c e γ em GEO).
Usado por videos/montar_legendado.py (--color-module) e por gerar_legenda.py (frases coloridas nunca quebram entre linhas)."""
VA = "#9C8CFF"    # foguete A, velocidade de A
VB = "#35D9FF"    # foguete B, velocidade de B, o que A mede de B (0,976c, 40/41, 0,99995c)
GEO = "#B8C4DA"   # o palpite 1,6c (seta tracejada), o fator gama

_GRUPOS = {
    VA: ["foguete A", "velocidade de A", "a de A"],
    VB: ["foguete B", "velocidade de B", "medida por A", "medido por A",
         "noventa e sete vírgula seis", "quarenta sobre quarenta e um",
         "noventa e nove vírgula", "nove nove cinco"],
    GEO: ["um vírgula seis", "cento e sessenta por cento", "gama"],
}
SUBTITLE_TERM_COLORS = {}
for _cor, _termos in _GRUPOS.items():
    for _t in _termos:
        SUBTITLE_TERM_COLORS[_t] = _cor
        SUBTITLE_TERM_COLORS[_t[0].upper() + _t[1:]] = _cor
