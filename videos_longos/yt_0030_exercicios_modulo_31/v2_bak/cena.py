"""yt_0030 — CÁLCULO III · EP. 04 · EXERCÍCIOS DO MÓDULO 3.1 (longo horizontal) — preview silencioso v1 (handoff v1, 2026-11-11; quadros-alvo em
referencia_v1/, gerador sb30.html).

Cada classe é um lote = um bloco do roteiro (preview 960×540 / 15 fps: ./render.sh Classe). Biblioteca: kit.py + v30.py (cópias do yt_0028) e lib30.py
(acréscimos do sb30). Tempos: tempos.py (orçamento a 3 palavras/s; na fase da voz, os tempos medidos).
"""
import importlib
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

LOTES = {   # classe: (arquivo, classe-base)
    "PH": ("sec_h", "LoteH"),        # H gancho + A bem-vindos (o canto entra no fim)
    "PD1": ("sec_d1", "LoteD1"),     # mesma fórmula, dois filmes
    "PD2": ("sec_d2", "LoteD2"),     # desenhar sem mil setas
    "PD3": ("sec_d3", "LoteD3"),     # a família de redemoinhos
    "PD3B": ("sec_d3b", "LoteD3b"),  # duas regras
    "PD4": ("sec_d4", "LoteD4"),     # o campo que não melhora de perto
    "PD5": ("sec_d5", "LoteD5"),     # o desafio prometido
    "PA1": ("sec_a1", "LoteA1"),     # P2 transição + A1 o rio
    "PA2": ("sec_a2", "LoteA2"),     # água batendo na parede
    "PA4": ("sec_a4", "LoteA4"),     # mapas que não entortam
    "PA3": ("sec_a3", "LoteA3"),     # por que um sobre a distância
    "PS": ("sec_s", "LoteS"),        # resumo, próximo vídeo e CTA
}
ORDEM = list(LOTES)
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
