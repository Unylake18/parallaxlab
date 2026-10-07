"""Cores das grandezas nas legendas, iguais às da cena V4."""
from template.config import PRIMARY_COLOR

CYAN, BLUE, MAGENTA, VIOLET = PRIMARY_COLOR, "#267BFF", "#EA63FF", "#9C8CFF"
SUBTITLE_TERM_COLORS = {
    "campo elétrico": CYAN, "campo radial": CYAN,
    "densidade linear de carga": CYAN, "carga envolvida": CYAN,
    "força elétrica": CYAN, "repulsão elétrica": CYAN, "repulsão": CYAN,
    "campo magnético": MAGENTA, "força magnética": MAGENTA,
    "atração magnética": MAGENTA, "atração": MAGENTA, "corrente": MAGENTA,
    "velocidade da luz": VIOLET, "velocidade": BLUE,
    "vetor de área": VIOLET, "superfície": VIOLET, "curva fechada": VIOLET,
    "modelo ideal": CYAN,
    "sessenta por cento": BLUE, "trinta e seis por cento": MAGENTA,
}
