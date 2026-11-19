"""yt_0021 — MOMENTO DE INÉRCIA: POR QUE O MESMO BASTÃO EXIGE O DOBRO DE ENERGIA PARA GIRAR? (longo horizontal, Física I · Rotação 4.11) — preview silencioso v1.

Cada classe é um lote renderizável (preview 960×540 / 15 fps: ./render.sh Classe; com 3D: ./render3d.sh Classe).
Kit copiado do yt_0019 (kit.py, prob.py, prob2.py); peças em pecas21.py; 3D em threejs/cena3d/f21.js ('bastao', 'esfera').
"""
import importlib
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

LOTES = {   # classe: (arquivo, classe-base)
    "PH": ("sec_hook", "LoteHook"),        # H1–H3 (bastão 3D)
    "PA": ("sec_abertura", "LoteA"),       # A1–A3
    "PT1": ("sec_t1", "LoteT1"),           # T1 energia de um giro
    "PT2": ("sec_t2", "LoteT2"),           # T2 de que depende I (haltere, r², raio de giração)
    "PT3": ("sec_t3", "LoteT3"),           # T3 barra contínua
    "PT4": ("sec_t4", "LoteT4"),           # T4 aro, disco, esfera 3D, tabela
    "PT5": ("sec_t5", "LoteT5"),           # T5 eixos paralelos (+ bastão 3D)
    "PT6": ("sec_t6", "LoteT6"),           # T6 eixos perpendiculares (+ esfera 3D)
    "PE1": ("sec_e1", "LoteE1"),           # E1 bloco e carretel
    "PE2": ("sec_e2", "LoteE2"),           # E2 haste que tomba
    "PE3": ("sec_e3", "LoteE3"),           # E3 placa com recorte
    "PS": ("sec_fim", "LoteFim"),          # S1, S2 (bastão 3D), EN1, EN2
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
