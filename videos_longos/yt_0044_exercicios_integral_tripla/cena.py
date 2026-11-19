"""yt_0044 · CÁLCULO III · EP. 19 (provisório) · Exercícios do módulo: integral tripla — preview v1.
Classes criadas aqui (o Manim só acha cenas definidas neste módulo)."""
import importlib
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

LOTES = {"PH": "sec_h", "PA": "sec_a", "PE1": "sec_e1", "PE2": "sec_e2", "PE3": "sec_e3", "PE4": "sec_e4", "PE5": "sec_e5", "PE6": "sec_e6", "PS": "sec_s"}
COM_3D = ["PH", "PE1", "PE2", "PE3", "PE4", "PE5", "PS"]
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
