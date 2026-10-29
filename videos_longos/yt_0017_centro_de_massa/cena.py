"""yt_0017 — CENTRO DE MASSA (longo horizontal, Física I · Mecânica) — preview silencioso v1 (3º vídeo do 4.9).

Cada classe é um lote renderizável (preview 960×540 / 15 fps: ./render.sh Classe; com fundo 3D: ./render3d.sh Classe).
Helpers em kit.py; cenas 3D (Three.js) em threejs/cena3d/cm3d.js. Cada lote importa só o próprio arquivo.
"""
import importlib
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

LOTES = {   # classe: (arquivo, classe-base)
    "X1": ("sec_teste3d", "LoteTeste3D"),     # teste das cenas 3D corrigidas (avaliação §2) + granada
    "PH": ("sec_abertura", "LoteHook"),       # H1–H3, A1–A4
    "P1": ("sec_t1", "LoteT1"),               # T1 — onde está o centro de massa?
    "P2": ("sec_t2", "LoteT2"),               # T2 — como ele se move?
    "P3": ("sec_t3", "LoteT3"),               # T3 — que energia é do movimento relativo?
    "P4": ("sec_t4", "LoteT4"),               # T4 — como achar o centro de massa de um corpo inteiro?
    "P5": ("sec_final", "LoteFinal"),         # E1, E2, síntese, encerramento
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
