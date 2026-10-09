"""Cores das grandezas nas legendas, iguais às da cena (v e profundidade em violeta; y, t e o furo em ciano; cancelamento e produto em magenta)."""
from template.config import PRIMARY_COLOR

CYAN, MAGENTA, VIOLET = PRIMARY_COLOR, "#EA63FF", "#9C8CFF"
SUBTITLE_TERM_COLORS = {
    "altura do furo": CYAN, "furo": CYAN, "tempo de voo": CYAN, "queda livre": CYAN,
    "Lei de Torricelli": CYAN, "modelo ideal": CYAN, "vinte por cento": CYAN,
    "oitenta por cento": CYAN,
    "profundidade": VIOLET, "velocidade de saída": VIOLET,
    "gravidade": MAGENTA, "produto": MAGENTA,
}
