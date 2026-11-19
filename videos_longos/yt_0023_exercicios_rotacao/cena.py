"""yt_0023 — DINÂMICA DA ROTAÇÃO: 4 PROBLEMAS EM QUE O MOMENTO DE INÉRCIA DECIDE TUDO (longo horizontal) — preview silencioso.

Cada classe é um lote (preview 960×540 / 15 fps: ./render.sh Classe; com 3D: ./render3d.sh Classe).
Kit: kit.py, prob.py, prob2.py, pecas22.py (copiados do yt_0022); peças da unidade em pecas23.py; 3D em threejs/cena3d/f23.js.
"""
import importlib
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

LOTES = {
    "PH": ("sec_ph", "LotePH"),        # H1–H3 (carretel 3D), A1–A3, D1–D3 (régua 3D)
    "PE1a": ("sec_e1a", "LoteE1a"),    # E1-1 a E1-10 (volante 3D)
    "PE1b": ("sec_e1b", "LoteE1b"),    # E1-11 a E1-18 (volante 3D)
    "PE2": ("sec_e2", "LoteE2"),       # E2 haste (2D)
    "PE3": ("sec_e3", "LoteE3"),       # E3 carretel (3D)
    "PE4": ("sec_e4", "LoteE4"),       # E4 pêndulo (2D)
    "PS": ("sec_ps", "LotePS"),        # S1, S2, EN1, EN2
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
