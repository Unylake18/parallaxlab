"""MODELO da camada Manim do pipeline Three.js + Manim (curto vertical, 9 × 16).

Esta camada é renderizada com fundo TRANSPARENTE (-t → .mov com alfa) e NÃO contém o 3D: o compor.py põe o Manim por
cima dos PNGs do Three.js. Os tempos vêm do mesmo timeline.json do 3D: nenhum número de tempo fica escrito aqui.

Exemplo: quando a câmera 3D pousa na vista de cima, um círculo GEO tracejado é desenhado exatamente sobre o anel de aço
(raio_objeto × fator_3d_manim, centrado em centro_topo_manim) e uma equação entra na área da álgebra, acima da faixa
de legenda. Troque pelo raciocínio do seu vídeo.

Render (na raiz do repositório):
  MEDIA_DIR=videos/vid_NNNN_x/media_preview uv run --no-sync python -m manim -t -r 540,960 --fps 15 videos/vid_NNNN_x/cena.py CenaModelo
"""
import json
import os
import sys
from pathlib import Path

from manim import *

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
sys.path.insert(0, str(ROOT))
from template.config import TEXT_COLOR  # noqa: E402,F401  (frame 9 × 16 e CRF do canal)
from template.fonts import screen_text  # noqa: E402

config.media_dir = os.environ.get("MEDIA_DIR", str(UNIT / "media_preview"))
TL = json.loads((UNIT / "timeline.json").read_text(encoding="utf-8"))
G, E = TL["geometria"], TL["eventos"]
K, CENTRO = G["fator_3d_manim"], np.array([*G["centro_topo_manim"], 0.0])
LEGENDA_TOPO = TL["legenda"]["y_manim"][0]          # nada da cena abaixo disto

GEO, MAG, GREEN = "#B8C4DA", "#EA63FF", "#3FE08B"


class CenaModelo(Scene):
    def construct(self):
        t = 0.0                                       # relógio da cena, sempre igual ao do timeline

        def ate(alvo):                                # espera até o instante 'alvo' do timeline
            nonlocal t
            if alvo > t + 1e-6:
                self.wait(alvo - t)
                t = alvo

        def tocar(*anims, run_time):
            nonlocal t
            self.play(*anims, run_time=run_time)
            t += run_time

        ate(E["manim_entra"])
        circulo = DashedVMobject(Circle(radius=K * G["raio_objeto"], color=GEO, stroke_width=3), num_dashes=60)
        circulo.move_to(CENTRO)
        rotulo = screen_text("VISTA DE CIMA", 26, color=GEO).next_to(circulo, DOWN, buff=.25)
        tocar(Create(circulo), FadeIn(rotulo), run_time=1.2)

        eq = MathTex(r"\oint", r"\vec B", r"\cdot", r"d\vec\ell", "=", r"\mu_0", r"I_{\text{enc}}", font_size=56)
        eq[1].set_color(MAG), eq[3].set_color(GEO), eq[6].set_color(GREEN)
        eq.move_to([0, LEGENDA_TOPO + 1.6, 0])
        assert eq.get_bottom()[1] > LEGENDA_TOPO, "a equação invadiu a faixa da legenda"
        tocar(Write(eq), run_time=1.0)
        ate(TL["duracao_s"])
