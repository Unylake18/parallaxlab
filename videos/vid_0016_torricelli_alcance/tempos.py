"""Simulação só de tempo (sem renderizar): soma as durações das animações no passo de 1/fps e imprime os marcos e os AVISO.

  uv run python -m manim -r 540,960 --fps 15 --dry_run videos/vid_0016_torricelli_alcance/tempos.py Tempo
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cena import *          # noqa: F401,F403
from cena import _Vid0016


class Tempo(_Vid0016):
    _t = 0.0

    @property
    def time(self):
        return self._t

    def _avanca(self, d):
        self._t += max(1, math.ceil(d * config.frame_rate - 1e-6)) / config.frame_rate

    def play(self, *anims, run_time=None, **kw):
        ini = self._t
        self._avanca(run_time if run_time is not None else 1.0)
        nomes = []
        for a in anims:
            n = type(a).__name__
            m = getattr(a, "mobject", None)
            nomes.append(n + ("(" + type(m).__name__ + ")" if m is not None else ""))
        print(f"EVT {ini:7.2f} -> {self._t:7.2f}  " + ", ".join(nomes[:3]))

    def wait(self, duration=1.0, **kw):
        self._avanca(duration)

    def construct(self):
        self.preparar()
        for nome in ("rodada1", "seg_a", "seg_b", "seg_c", "seg_d", "seg_e", "seg_f", "seg_g", "seg_h"):
            getattr(self, nome)()
            print(f"MARCO {nome:8s} termina em t = {self._t:7.2f}")
        print(f"MARCO duração total = {self._t:.2f} s")
