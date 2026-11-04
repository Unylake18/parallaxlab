"""Referência da pessoa e do Sol (§B.2/§B.11): à esquerda, as funções ORIGINAIS do vid_0025 (importadas só para este still de
QA, sem alterar a unidade); à direita, as cópias da unidade (arte_vid0025.py), com os mesmos parâmetros.
Uso (na raiz): uv run python -m manim -s -r 540,960 videos/vid_0031_halo_22/qa/ref_vid0025.py RefPessoaSol
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
UNIT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(UNIT))
spec = importlib.util.spec_from_file_location('vid0025', ROOT / 'videos' / 'vid_0025_arco_iris' / 'cena.py')
V25 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(V25)

from manim import *  # noqa: E402
import arte_vid0025 as A  # noqa: E402
from template.fonts import screen_text  # noqa: E402

config.media_dir = str(UNIT / 'media_ref')


class RefPessoaSol(Scene):
    def construct(self):
        for x0, mod, nome in ((-2.25, V25, 'vid_0025 (original)'), (2.25, A, 'vid_0031 (cópia)')):
            chao = VGroup(mod.make_ground(-2.0, 1.2), Line([x0 - 2, -2.0, 0], [x0 + 2, -2.0, 0], color=mod.GEO, stroke_width=2.2))
            p = mod.make_person([x0 - .6, -2.0], 1.5)
            s = mod.make_sun([x0 + .9, 1.8], .3)
            t = screen_text(nome.upper(), 18).move_to([x0, 3.6, 0])
            self.add(chao, p, s, t)
        self.add(screen_text('PESSOA E SOL: VID_0025 × VID_0031', 22).move_to([0, 5.4, 0]))
