"""yt_0045 · CÁLCULO III · EP. 20 (provisório) · Integral de linha de um campo vetorial — preview v2.
Classes criadas aqui (o Manim só acha cenas definidas neste módulo)."""
import importlib
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

LOTES = {"PH": "sec_h", "PA": "sec_a", "PB1": "sec_b1", "PB2": "sec_b2", "PB4": "sec_b4", "PB5": "sec_b5", "PB6": "sec_b6", "PB7": "sec_b7", "PS": "sec_s"}
COM_3D = []
_pedido = [a for a in sys.argv if a in LOTES]
for _nome, _arq in LOTES.items():
    if _pedido and _nome not in _pedido:
        continue
    try:
        globals()[_nome] = type(_nome, (getattr(importlib.import_module(_arq), _nome),), {})
    except Exception:
        if _nome in _pedido:
            raise
        print(f"[cena] {_nome} indisponível:\n{traceback.format_exc(limit=1)}")
