"""yt_0016 — MOMENTO EM SISTEMAS (longo horizontal, Física I · Mecânica) — preview silencioso v1 (Parte 2 de 2 do 4.9).

Cada classe é um lote renderizável (preview 960×540 / 15 fps: ./render.sh Classe). Ordem do vídeo em montar_preview.py.
Helpers em kit.py; cavalo e pedra em sec_cavalo.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sec_abertura import LoteHook  # noqa: E402
from sec_t7 import LoteT7  # noqa: E402
from sec_t8 import LoteT8  # noqa: E402
from sec_t9 import LoteT9  # noqa: E402
from sec_t10 import LoteT10  # noqa: E402
from sec_e6 import LoteE6  # noqa: E402
from sec_e7 import LoteE7  # noqa: E402
from sec_e8 import LoteE8  # noqa: E402
from sec_e9 import LoteE9  # noqa: E402
from sec_coda import LoteCoda  # noqa: E402
from sec_fim import LoteFim  # noqa: E402


class PH(LoteHook):            # H1–H3, A1–A3
    pass


class P7(LoteT7):              # T7 — sistemas de partículas
    pass


class P8(LoteT8):              # T8 — força interna não move o sistema
    pass


class P9(LoteT9):              # T9 — escolher o sistema
    pass


class P10(LoteT10):            # T10 — como a energia se divide
    pass


class Q6(LoteE6):              # E6 — agarrar ou rebater
    pass


class Q7(LoteE7):              # E7 — o caçador no lago
    pass


class Q8(LoteE8):              # E8 — os gases do rifle
    pass


class Q9(LoteE9):              # E9 — Newton e a luz
    pass


class PC(LoteCoda):            # coda — a luz também tem momento
    pass


class PS(LoteFim):             # síntese e encerramento
    pass
