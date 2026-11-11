"""yt_0028 — LIMITE, CONTINUIDADE E DERIVADAS PARCIAIS (longo horizontal, Cálculo III · EP. 03) — preview silencioso v1 (handoff v1.2, 2026-11-11;
quadros-alvo em referencia_v1/).

Cada classe é um lote = uma seção (preview 960×540 / 15 fps: ./render.sh Classe). Kit em kit.py (copiado do yt_0027) e v28.py (helpers do v27 + peças do sb28.html).
"""
import importlib
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

LOTES = {   # classe: (arquivo, classe-base)
    "PH": ("sec_h", "LoteH"),        # H o quadradinho que deforma; A bem-vindos (o canto entra)
    "PB1": ("sec_b1", "LoteB1"),     # chegar perto (ε-δ)
    "PB2": ("sec_b2", "LoteB2"),     # quando o limite não existe
    "PB3": ("sec_b3", "LoteB3"),     # continuidade
    "PB4": ("sec_b4", "LoteB4"),     # derivada parcial
    "PB5": ("sec_b5", "LoteB5"),     # o engano
    "PB6": ("sec_b6", "LoteB6"),     # a tabela
    "PB7": ("sec_b7", "LoteB7"),     # quatro números, quatro medidas; o desafio
    "PS": ("sec_s", "LoteS"),        # resumo e CTA
}
_pedido = [a for a in sys.argv if a in LOTES]
for _nome, (_arq, _base) in LOTES.items():
    if _pedido and _nome not in _pedido:
        continue
    try:
        globals()[_nome] = type(_nome, (getattr(importlib.import_module(_arq), _base),), {})
    except Exception:
        if _nome in _pedido:
            raise
        print(f"[cena] {_nome} indisponível:\n{traceback.format_exc(limit=1)}")
