"""Cena mínima de teste (só diagnóstico): escreve a linha do B3-5 pelo mesmo motor para ver, quadro a quadro, a ordem dos glifos."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pecas24 import *  # noqa: F401,F403


import prob2 as _p2

_orig_interp = _p2.Vez.interpolate
_cnt = [0]


def _dbg(self, alpha):
    _orig_interp(self, alpha)
    if _cnt[0] < 12:
        _cnt[0] += 1
        ops = [round(float(x.get_fill_opacity()), 2) for x, _, _ in self._salvo][:6]
        print(f"[dbg] Vez alpha={alpha:.3f} active_index={getattr(self, 'active_index', 'NA')} n={len(self._salvo)} ops={ops}")


_p2.Vez.interpolate = _dbg


class TOrd(Lote24):
    def corpo(self):
        A5, a5 = Mx("L_z", "=", "x", "p_y", "-", "y", "p_x")
        self.pilha.poe(A5)
        self.lei(A5, a5, rt=1.2, metodo="lei")
        B5, b5 = Mx("=", "d", r"(-m g t)", "-", "y", r"\cdot", "0", cores={1: VETC})
        self.pilha.poe(B5)
        self.wait(0.3)
        self.lei(B5, b5, rt=1.5, metodo="escrita")
        self.wait(0.5)
