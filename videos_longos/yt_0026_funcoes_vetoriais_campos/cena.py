"""yt_0026 — FUNÇÕES A VALORES VETORIAIS E CAMPOS VETORIAIS (longo horizontal, Cálculo III · EP. 01) — preview silencioso v3 (sistema visual v3 da série de Cálculo).

Cada classe é um lote = uma seção (preview 960×540 / 15 fps: ./render.sh Classe; com 3D: ./render3d.sh Classe).
Kit em kit.py; 3D em threejs/cena3d/f26.js. PB7 é a seção separada (o Kaio decide no preview se fica).
"""
import importlib
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

LOTES = {   # classe: (arquivo, classe-base)
    "PT": ("sec_t", "LoteT"),        # T1–T6 abertura do Cálculo III (caixa e colunas 3D)
    "PAH": ("sec_ah", "LoteAH"),     # A1 bem-vindos, H1–H3 mesma fórmula, dois desenhos
    "PB1": ("sec_b1", "LoteB1"),     # que função é essa
    "PB2": ("sec_b2", "LoteB2"),     # transformação: polares
    "PB3": ("sec_b3", "LoteB3"),     # a dobra
    "PB4": ("sec_b4", "LoteB4"),     # para o espaço (folha_paraboloide 3D)
    "PB5": ("sec_b5", "LoteB5"),     # campo vetorial
    "PB6": ("sec_b6", "LoteB6"),     # de volta ao redemoinho
    "PB7": ("sec_b7", "LoteB7"),     # no espaço (campo_espaco 3D) — seção separada
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
