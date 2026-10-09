"""Teste rápido (sem Blender) das passagens de glifos do trecho do máximo: y = H − y → y/H = 1/2 e a substituição em x/H.

  uv run python -m manim -r 540,960 --fps 15 --media_dir videos/vid_0016_torricelli_alcance/media_teste videos/vid_0016_torricelli_alcance/teste_maximo.py TesteMaximo
"""
import sys
from pathlib import Path

from manim import *
from MF_Tools import TransformByGlyphMap

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cena import EQS, MAPAS  # noqa: E402


class TesteMaximo(Scene):
    def construct(self):
        self.camera.background_color = "#050816"
        config.frame_width, config.frame_height = 9, 16

        def E(k, y):
            s, sz = EQS[k]
            return MathTex(s, font_size=sz).move_to([0, y, 0])

        atual = E("M0", 3)
        self.add(atual)
        self.wait(0.3)
        for de, para in [("M0", "M1"), ("M1", "M2"), ("M2", "M3"), ("M3", "M4")]:
            novo = E(para, 3)
            self.play(TransformByGlyphMap(atual, novo, *MAPAS[(de, para)], auto_fade=True, printing=False), run_time=1.0)
            self.remove(atual)
            atual = novo
            self.wait(0.4)
        m4 = atual
        s = E("S0", -2)
        self.add(s)
        self.wait(0.3)
        s1 = E("S1", -2)
        half = m4[0][4:7]
        self.play(TransformByGlyphMap(s, s1, ([0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4, 5, 6]), ([10, 11, 12, 16], [10, 11, 12, 16]), auto_fade=True, printing=False),
                  TransformFromCopy(half, s1[0][7:10]), TransformFromCopy(half, s1[0][13:16]), run_time=1.5)
        self.remove(s)
        atual = s1
        self.wait(0.4)
        for de, para in [("S1", "S2"), ("S2", "S3"), ("S3", "S4"), ("S4", "S5")]:
            novo = E(para, -2)
            self.play(TransformByGlyphMap(atual, novo, *MAPAS[(de, para)], auto_fade=True, printing=False), run_time=1.0)
            self.remove(atual)
            atual = novo
            self.wait(0.4)
