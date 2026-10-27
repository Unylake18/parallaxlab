"""Quadros de composição para depuração, sem renderizar intervalos de tempo.

Não substitui o QA do preview. Não escreve os arquivos de timing da cena.
"""

import argparse
from pathlib import Path

from manim import ImageMobject, tempconfig
from PIL import Image

from cena import OrbitaQuedaContinua007, BACKGROUND_COLOR, WATERMARK_PATH

PASTA = Path(__file__).resolve().parent


class Composicoes(OrbitaQuedaContinua007):
    blocos = (9, 11, 12, 13, 14, 17, 18)

    def capturar(self, nome):
        self.update_mobjects(0)
        self.renderer.static_image = None
        self.renderer.update_frame(self, ignore_skipping=True)
        destino = PASTA / 'qa_estatico'
        destino.mkdir(exist_ok=True)
        Image.fromarray(self.renderer.get_frame()).save(destino / f'{nome}.png')

    def marco(self, nome):
        self.capturar(nome)

    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.92).set_opacity(.45)
        self.wm.move_to([6.25, -3.91, 0]).set_z_index(50)
        for n in self.blocos:
            getattr(self, f'n{n:02d}')()
            self.capturar(f'N{n:02d}_final')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--blocos', default='9,11,12,13,14,17,18')
    args = parser.parse_args()
    Composicoes.blocos = tuple(map(int, args.blocos.split(',')))
    with tempconfig(dict(dry_run=True, write_to_movie=False, save_last_frame=False,
                         pixel_width=960, pixel_height=540, frame_rate=15,
                         media_dir=str(PASTA / 'media_estatico'), verbosity='WARNING')):
        Composicoes(skip_animations=True).render()
    print('Quadros estáticos prontos em', PASTA / 'qa_estatico')
