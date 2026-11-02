"""yt_0019 — POR QUE UM FOGUETE É QUASE TODO COMBUSTÍVEL? (longo horizontal, Física I · Mecânica 4.9) — preview silencioso v1.

Cada classe é um lote renderizável (preview 960×540 / 15 fps: ./render.sh Classe; com 3D: ./render3d.sh Classe).
Kit copiado do yt_0018 (kit.py, prob.py, prob2.py); peças e simulação em pecas19.py; 3D em threejs/cena3d/f19.js ('rampa', 'esp').
"""
import importlib
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

LOTES = {   # classe: (arquivo, classe-base)
    "PH": ("sec_hook", "LoteHook"),        # H1–H3 (rampa 3D), A1–A3
    "PT1": ("sec_t1", "LoteT1"),           # T1 carrinho de areia
    "PT2": ("sec_t2", "LoteT2"),           # T2 empuxo (espaço 3D + esquemas 2D)
    "PT3": ("sec_t3", "LoteT3"),           # T3 Tsiolkovsky (2D + espaço 3D)
    "PT4": ("sec_t4", "LoteT4"),           # T4 gravidade (rampa 3D + gráficos)
    "PE1": ("sec_e1", "LoteE1"),           # E1 decolagem
    "PE2": ("sec_e2", "LoteE2"),           # E2 estágios (2D + espaço 3D)
    "PE3": ("sec_e3", "LoteE3"),           # E3 esteira de areia
    "PS": ("sec_fim", "LoteFim"),          # S1, EN1, EN2
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
