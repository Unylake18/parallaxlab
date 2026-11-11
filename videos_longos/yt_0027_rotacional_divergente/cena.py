"""yt_0027 — ROTACIONAL E DIVERGENTE (longo horizontal, Cálculo III · EP. 02) — preview silencioso v2 (handoff v2, 2026-11-10: sistema visual do yt_0026 v7/v8, quadros-alvo em referencia_v2/).

Cada classe é um lote = uma seção (preview 960×540 / 15 fps: ./render.sh Classe; com 3D: ./render3d.sh Classe).
Kit em kit.py (copiado do yt_0026) e v27.py (helpers do v7 do yt_0026 + peças do sb27.html); 3D em threejs/cena3d/f27.js (cubo, roda).
"""
import importlib
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

LOTES = {   # classe: (arquivo, classe-base)
    "PHA": ("sec_ha", "LoteHA"),     # H1–H3 dois redemoinhos; A1 bem-vindos (o canto entra)
    "PB1": ("sec_b1", "LoteB1"),     # um pedacinho de fluido
    "PB2": ("sec_b2", "LoteB2"),     # rotacional: os dois braços
    "PB3": ("sec_b3", "LoteB3"),     # dois enganos, tornado, rio
    "PB4": ("sec_b4", "LoteB4"),     # divergente: a caixa
    "PB5": ("sec_b5", "LoteB5"),     # a falsa fonte
    "PB6": ("sec_b6", "LoteB6"),     # no espaço (Three.js: cubo_saldo, rodinha_eixo)
    "PF": ("sec_f", "LoteF"),        # na física
    "PB7": ("sec_b7", "LoteB7"),     # laplaciano
    "PS": ("sec_s", "LoteS"),        # resumo e CTA
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
