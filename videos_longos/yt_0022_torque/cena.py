"""yt_0022 — TORQUE: POR QUE A PONTA DA RÉGUA ACELERA MAIS QUE A GRAVIDADE? (longo horizontal, Física I · Rotação 4.11) — preview silencioso v1.

Cada classe é um lote renderizável (preview 960×540 / 15 fps: ./render.sh Classe; com 3D: ./render3d.sh Classe).
Kit em kit.py, prob.py, prob2.py; peças em pecas22.py; 3D em threejs/cena3d/f22.js ('regua', 'porta').
"""
import importlib
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

LOTES = {   # classe: (arquivo, classe-base)
    "PH": ("sec_hook", "LoteHook"),        # H1–H3 (regua 3D)
    "PA": ("sec_abertura", "LoteA"),       # A1–A3
    "PT1": ("sec_t1", "LoteT1"),           # T1 o que é torque e braço de alavanca (porta 3D em T1-1, T1-2)
    "PT2": ("sec_t2", "LoteT2"),           # T2 torque como vetor: produto vetorial (porta 3D em T2-1, T2-2)
    "PT3": ("sec_t3", "LoteT3"),           # T3 segunda lei de Newton da rotação
    "PT4": ("sec_t4", "LoteT4"),           # T4 de volta à régua: onde a ponta passa de g (regua 3D em T4-1)
    "PT5": ("sec_t5", "LoteT5"),           # T5 trabalho e potência no giro
    "PT6": ("sec_t6", "LoteT6"),           # T6 quando nada acelera: equilíbrio
    "PS": ("sec_fim", "LoteFim"),          # S1, S2 (regua 3D), EN1, EN2 (regua 3D)
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
