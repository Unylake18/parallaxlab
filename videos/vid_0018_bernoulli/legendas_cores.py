"""Grandezas nas mesmas cores dos símbolos da V5; SRT permanece texto simples."""
PRESSURE, KINETIC, GRAVITY, AREA = "#35D9FF", "#745CFF", "#EA63FF", "#267BFF"
_terms = {
    "pressão": PRESSURE, "pressões": PRESSURE, "força": PRESSURE, "forças": PRESSURE,
    "trabalho": PRESSURE, "trabalho líquido": PRESSURE,
    "velocidade": KINETIC, "velocidades": KINETIC,
    "energia cinética": KINETIC, "cinética": KINETIC,
    "parcela cinética": KINETIC,
    "altura": GRAVITY, "alturas": GRAVITY,
    "energia potencial gravitacional": GRAVITY, "potencial gravitacional": GRAVITY,
    "gravitacional": GRAVITY,
    "área": AREA, "áreas": AREA,
}
SUBTITLE_TERM_COLORS = {variant: color for term, color in _terms.items()
                        for variant in (term, term.capitalize(), term.upper())}
