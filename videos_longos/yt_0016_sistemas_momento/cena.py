"""yt_0016 — MOMENTO EM SISTEMAS (longo horizontal, Física I · Mecânica) — preview silencioso v2 (Parte 2 de 2 do 4.9).

Cada classe é um lote renderizável (preview 960×540 / 15 fps: ./render.sh Classe; com fundo 3D: ./render3d.sh Classe).
Ordem do vídeo em montar_preview.py. Helpers em kit.py; cavalo 3D em sec_cavalo.py; manequim 3D em sec_manequim.py.
Cada lote importa só o próprio arquivo (um lote em obra não quebra os outros).
"""
import importlib
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

LOTES = {   # classe: (arquivo, classe-base)
    "PH": ("sec_abertura", "LoteHook"),      # H1–H3, A1–A6
    "P7": ("sec_t7", "LoteT7"),              # T7 — sistemas de partículas
    "P8": ("sec_t8", "LoteT8"),              # T8 — força interna não move o sistema
    "P9": ("sec_t9", "LoteT9"),              # T9 — escolher o sistema
    "P10": ("sec_t10", "LoteT10"),           # T10 — como a energia se divide
    "Q6": ("sec_e6", "LoteE6"),              # E6 — agarrar ou rebater
    "Q7": ("sec_e7", "LoteE7"),              # E7 — o caçador no lago
    "Q8": ("sec_e8", "LoteE8"),              # E8 — os gases do rifle
    "Q9": ("sec_e9", "LoteE9"),              # E9 — Newton e a luz
    "PC": ("sec_coda", "LoteCoda"),          # coda — a luz também tem momento
    "PS": ("sec_fim", "LoteFim"),            # síntese e encerramento
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
