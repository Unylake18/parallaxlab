"""Leitor do padrão visual (estilo.json). Python puro: pode ser importado dentro e fora do Blender."""

import json
from pathlib import Path

ESTILO = json.loads((Path(__file__).resolve().parent / "estilo.json").read_text(encoding="utf-8"))


def cor(nome):
    """Hex sRGB de uma cor do padrão, pelo nome (ex.: 'fonte_fisica')."""
    return ESTILO["cores"][nome]["hex"]


def hex_linear(h, alpha=1.0):
    """Hex sRGB -> RGBA linear (o Blender trabalha em linear)."""
    h = h.lstrip("#")
    canais = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in canais]
    return (*lin, alpha)
