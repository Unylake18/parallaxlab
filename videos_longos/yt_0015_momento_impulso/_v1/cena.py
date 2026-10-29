"""yt_0015 — MOMENTO LINEAR E IMPULSO (longo horizontal, Física I · Mecânica) — preview silencioso v1.

Cada classe é um lote renderizável (preview 960×540 / 15 fps); ver render_preview.py. Helpers em kit.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sec_hook import P1Hook  # noqa: E402


class P1(P1Hook):
    pass
from sec_a import LoteA  # noqa: E402


class PA(LoteA):
    pass
from sec_b import LoteB  # noqa: E402


class PB(LoteB):
    pass
from sec_c import LoteC  # noqa: E402


class PC(LoteC):
    pass
from sec_d import LoteD  # noqa: E402


class PD(LoteD):
    pass
from sec_e import LoteE  # noqa: E402


class PE(LoteE):
    pass
from sec_t import Camada01, Camada13  # noqa: E402


class PT1(Camada01):
    pass


class PT2(Camada13):
    pass
