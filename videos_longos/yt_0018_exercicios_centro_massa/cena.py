"""yt_0018 — CENTRO DE MASSA: 6 PROBLEMAS QUE PARECEM IMPOSSÍVEIS (longo horizontal, Física I · Mecânica) — preview silencioso v2.

Cada classe é um lote renderizável (preview 960×540 / 15 fps: ./render.sh Classe; com fundo 3D: ./render3d.sh Classe).
Helpers em kit.py (copiado do yt_0017) e prob.py; o lago (Three.js, lago3d.js) em lago2.py; cenas 3D em threejs/cena3d/cm18.js (cubo, foguete)
e cm3d.js/campo.js (a granada do yt_0017, só no A3).
"""
import importlib
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

LOTES = {   # classe: (arquivo, classe-base)
    "PH": ("sec_hook", "LoteHook"),        # H1–H3, A1–A4
    "PX0": ("sec_x01", "LoteX01"),         # X0 disco furado, X1 placa com furo
    "PX2": ("sec_x2", "LoteX2"),           # X2 fio no cubo (Three.js)
    "PX3": ("sec_x3", "LoteX3"),           # X3 gafanhoto (lago Three.js)
    "PX4": ("sec_x4", "LoteX4"),           # X4 naves
    "PX5": ("sec_x5", "LoteX5"),           # X5 a balança que marca menos (Atwood, 2D)
    "PEP": ("sec_fim", "LoteFim"),         # EP, S2, EN1–EN2 (foguete em Three.js)
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
