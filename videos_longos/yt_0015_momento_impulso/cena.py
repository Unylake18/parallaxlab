"""yt_0015 — MOMENTO LINEAR E IMPULSO (longo horizontal, Física I · Mecânica) — preview silencioso v2 (Parte 1 de 2: uma partícula).

Cada classe é um lote renderizável (preview 960×540 / 15 fps; render.sh Classe). Camadas transparentes dos trechos 3D: render.sh
Classe -t e compor.py. Ordem do vídeo em montar_preview.py. Helpers em kit.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sec_3d import CamadaE4, CamadaHook, CamadaTrilho  # noqa: E402


class PH(CamadaHook):          # H1–H3 sobre o 3D do manequim
    pass


class PT2(CamadaTrilho):       # T2-1..T2-4 sobre o 3D do trilho de ar
    pass


class PG4(CamadaE4):           # E4-1 sobre o muro recuado
    pass
from sec_t1 import LoteAbertura, LoteT1  # noqa: E402
from sec_teoria import LoteTeoria  # noqa: E402
from sec_t5 import LoteT5  # noqa: E402


class PA(LoteAbertura):        # A1–A3
    pass


class PB(LoteT1):              # T1 — o fato experimental
    pass


class PC(LoteTeoria):          # T2-5, T3, T4
    pass


class PD(LoteT5):              # T5 — impulso
    pass
from sec_ex import LoteEx  # noqa: E402
from sec_t6 import LoteT6  # noqa: E402
from sec_muro import LoteMuro  # noqa: E402
from sec_fim import LoteFim  # noqa: E402


class PE(LoteEx):              # E1, E2, E3
    pass


class PF(LoteT6):              # T6 — momento ou energia?
    pass


class PG(LoteMuro):            # E4-2..E4-6, E5
    pass


class PS(LoteFim):             # síntese e encerramento
    pass
from sec_3d import CamadaCavalo  # noqa: E402


class PF2(CamadaCavalo):       # F2 sobre o 3D do cavalo (CC0, Quaternius)
    pass
from sec_momento import LoteMomento  # noqa: E402


class PT1(LoteMomento):        # v4 · T1 — de onde vem o momento (2,5D no Manim)
    pass
from sec_trilho import LoteTrilho  # noqa: E402


class PT3(LoteTrilho):         # v4 · T3 — por que massa vezes velocidade? (trilho em 2D/2,5D)
    pass
