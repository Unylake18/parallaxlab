"""Regressão visual curta: a troca horizonte/esfera não deixa filhos congelados."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from manim import *
from encenacao import OrbitaRepaginada
from geometria_visual import CameraOrbital


class TesteCamera(OrbitaRepaginada):
    def construct(self):
        self.cam = CameraOrbital()
        self.terra = Group()
        def atualizar(m):
            m.remove(*m.submobjects)
            m.add(self.cam.planeta())
        self.terra.add_updater(atualizar, call_updater=True)
        self.add(self.terra)
        self.olhar(0, 0, 6.4, dur=3)
        self.wait(.3)
