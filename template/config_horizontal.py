"""Configuração do formato longo_horizontal (16:9). Aditiva: template/config.py (vertical) não muda.

Nas cenas horizontais, importar daqui em vez de template.config. Mesma paleta e mesmo watermark
do vertical; só o frame lógico muda. Os dois formatos têm 120 px por unidade no final
(1080/9 = 1920/16), então o mesmo font_size tem o mesmo tamanho em pixels nos dois.

Preview: -r 960,540 --fps 15 · final planejado (decisão interna, não regra de plataforma): -r 1920,1080 --fps 30.
"""

from manim import config

from template.config import (  # noqa: F401  (reexportados: paleta e watermark únicos)
    BACKGROUND_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, TEXT_COLOR, WATERMARK_PATH,
)

# Depois do import acima, que define 9 × 16.
config.frame_width = 16
config.frame_height = 9
