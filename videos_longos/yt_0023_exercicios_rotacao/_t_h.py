import sys
sys.path.insert(0, '.')
from pecas23 import *
from pecas23b import *
class T(Scene):
    def construct(self):
        self.camera.background_color = "#08122B"
        import os
        O = P3(-4.75, 1.0); LH = 5.8
        t = float(os.environ.get("TH", "0.6"))
        u = np.array([math.cos(t), -math.sin(t), 0.0]); n = np.array([math.sin(t), math.cos(t), 0.0])
        cm = O + 0.25 * LH * u
        f = forca_eixo(t)
        self.add(haste25(O, cm, t, LH), marcador_cm(cm, r=0.17, z=16), lupa_pivo(O, t, f["F"] * 1.2, -f["fr"] * 1.2 * u, f["fp"] * 1.2 * n),
                 seta_s(O, O + f["F"] * 1.2, FC, 7))
