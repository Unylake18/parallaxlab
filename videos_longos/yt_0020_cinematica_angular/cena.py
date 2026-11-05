"""yt_0020 — CINEMÁTICA ANGULAR: POR QUE A PONTA DA HÉLICE CHEGA A QUASE 1.000 km/h? (longo horizontal, Física I · Rotação 4.11) — preview silencioso v1.

Cada classe é um lote renderizável (preview 960×540 / 15 fps: ./render.sh Classe; com 3D: ./render3d.sh Classe).
Kit copiado do yt_0019 (kit.py, prob.py, prob2.py); peças em pecas20.py; 3D em threejs/cena3d/r20.js ('helice', 'disco', 'livros', 'terra').
"""
import importlib
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

LOTES = {   # classe: (arquivo, classe-base)
    "PH": ("sec_hook", "LoteHook"),        # H1–H3 (hélice 3D), A1–A3
    "PT1": ("sec_t1", "LoteT1"),           # T1 como medir um giro
    "PT2": ("sec_t2", "LoteT2"),           # T2 quão rápido gira
    "PT3": ("sec_t3", "LoteT3"),           # T3 quando o giro acelera
    "PT4": ("sec_t4", "LoteT4"),           # T4 cada ponto do corpo (hélice 3D no T4-2)
    "PT5": ("sec_t5", "LoteT5"),           # T5 para onde aponta um giro (disco 3D, livros 3D)
    "PE1": ("sec_e1", "LoteE1"),           # E1 ventilador
    "PE2": ("sec_e2", "LoteE2"),           # E2 bicicleta
    "PE3": ("sec_e3", "LoteE3"),           # E3 Terra (3D)
    "PS": ("sec_fim", "LoteFim"),          # S1, S2 (hélice 3D), EN1, EN2
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
