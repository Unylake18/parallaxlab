"""yt_0039 · CÁLCULO III · EP. 14 · Exercícios do módulo: jacobiano, polares e centro de massa — preview v1 (handoff v1.1). Um lote por bloco
(./render.sh Classe; ./render3d.sh Classe nos lotes com 3D); concatenar na ordem de LOTES (montar.py). Classes criadas aqui (o Manim só acha
cenas definidas neste módulo)."""
import importlib
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

LOTES = {"PH": "sec_h", "PA": "sec_a", "PE1": "sec_e1", "PE2": "sec_e2", "PE3": "sec_e3", "PE4": "sec_e4", "PE5": "sec_e5",
         "PE6": "sec_e6", "PS": "sec_s", "PT": "sec_teste"}
COM_3D = ["PE3", "PE6"]
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
