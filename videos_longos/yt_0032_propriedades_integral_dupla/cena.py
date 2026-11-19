"""yt_0032 · CÁLCULO III · EP. 07 · Propriedades da integral dupla — preview v1 (handoff v1). Um lote por bloco (./render.sh Classe;
./render3d.sh Classe nos lotes com 3D); concatenar na ordem de LOTES (montar.py). Classes criadas aqui (o Manim só acha cenas definidas neste módulo)."""
import importlib
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

LOTES = {"PH": "sec_h", "PA": "sec_a", "PB1": "sec_b1", "PB2": "sec_b2", "PB3": "sec_b3", "PB4": "sec_b4", "PB5": "sec_b5",
         "PB6": "sec_b6", "PB7": "sec_b7", "PS": "sec_s"}
COM_3D = ["PB1", "PB2", "PB3", "PB6"]
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
