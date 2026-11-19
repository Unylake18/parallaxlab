"""yt_0024 — MOMENTO ANGULAR DE UMA PARTÍCULA (longo horizontal, Física I · Rotação 4.11) — preview silencioso v1.

Cada classe é um lote (preview 960×540 / 15 fps: ./render.sh Classe; com 3D: ./render3d.sh Classe).
Kit em kit.py, prob.py, prob2.py, pecas22.py (copiados do yt_0022); peças da unidade em pecas24.py; 3D em threejs/cena3d/mesa.js ('mesa_furo').
"""
import importlib
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

LOTES = {
    "PH": ("sec_ph", "LotePH"),     # H1–H3, A1–A2 (mesa 3D)
    "PB1": ("sec_b1", "LoteB1"),    # B1 de p a L (mesa 3D)
    "PB2": ("sec_b2", "LoteB2"),    # B2 a reta (mesa 3D, vista de cima)
    "PB3": ("sec_b3", "LoteB3"),    # B3 τ = dL/dt (2.5D)
    "PB4": ("sec_b4", "LoteB4"),    # B4 o círculo (mesa 3D, vista de cima)
    "PB5": ("sec_b5", "LoteB5"),    # B5 força central (2.5D)
    "PB6": ("sec_b6", "LoteB6"),    # B6 de volta à mesa (mesa 3D)
    "PS": ("sec_ps", "LotePS"),     # S1, S2, EN (mesa 3D)
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
