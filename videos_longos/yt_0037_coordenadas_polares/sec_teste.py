"""Teste do kit (não entra no vídeo)."""
from p37 import *


class PT(B37):
    ANTES = "A INTEGRAL QUE NÃO COLABORA"

    def corpo(self):
        self.an("H1")
        a = T("MESMO Δr, MESMO Δθ", 960, 300, 26, "center", LI, bold=False)
        b = T("NO INTERIOR: φ(INTERIOR) = INTERIOR · φ INJETORA · r ≠ 0", 960, 360, 26, "center", CANTO_S, bold=False)
        c = T("METRO²: É A ÁREA · x² + y² · r CONSTANTE → CÍRCULO", 960, 420, 26, "center", MEN, bold=False)
        d = TC(r"\iint_{\X^2+\Y^2\le 1} \Ci{e^{-(\X^2+\Y^2)}}\,dA \quad \int_0^{2\pi}\!\!\int_0^1 \Ci{e^{-\R^2}}\,\J\,\dr\,\dt \quad \rb\,\Dr\,\Dt \quad \uu=\R^2,\ \du", 960, 540, 40, "c")
        e = TC(r"\dfrac{\partial(\X,\Y)}{\partial(\R,\T)}=\begin{vmatrix}\cos\T & -\R\sen\T\ \sen\T & \R\cos\T\end{vmatrix}", 960, 700, 40, "c")
        self.add(a, b, c, d, e)
        for m in (a, b, c, d, e):
            ja_escrita(m)
        self.wait(1)
