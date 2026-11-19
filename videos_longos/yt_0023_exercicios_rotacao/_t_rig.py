import sys
sys.path.insert(0, '.')
from pecas23 import *
class T(Scene):
    def construct(self):
        self.camera.background_color = "#08122B"
        import os
        k = os.environ.get("K", "a")
        if k == "a":
            self.add(rig25(P3(-4.55, 0.6), 4.3, 0.0))
        elif k == "b":
            self.add(rig25(P3(-3.6, -0.1), 4.3, 7.0, cai=3.0, cord=False, freio=True, heat=0.7))
        elif k == "c":
            self.add(rig25(P3(-5.0, 1.75), 2.8, 6.0), rig25(P3(-5.0, 1.75) + 2.8 * 1.25 * RIGHT, 2.8, 4.0, aro=True))
        elif k == "d":
            self.add(rig25(P3(-4.3, 0.3), 4.6, 7.4))
