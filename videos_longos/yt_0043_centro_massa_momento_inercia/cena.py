"""yt_0043 · CÁLCULO III · EP. 18 (provisório) · Centro de massa e momento de inércia na integral tripla — preview v1.
Classes criadas aqui (o Manim só acha cenas definidas neste módulo)."""
import importlib
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

LOTES = {"PH": "sec_h", "PA": "sec_a", "PB1": "sec_b1", "PB2": "sec_b2", "PB3": "sec_b3", "PB4": "sec_b4", "PS": "sec_s"}
COM_3D = ["PH", "PB1", "PB2", "PB3", "PB4", "PS"]
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
