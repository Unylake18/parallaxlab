"""final (NÃO USADO: sem o template, o quadro tem largura 14,2 e a grade não bate; a referência é o quadro 3245 do preview v5, papel vazio entre PB1 e PB2): quadro de referência do 'papel vazio' (violeta + placas + grade padrão) para o detector de quadros vazios (folha_contato.py).
uso: python -m manim -r 960,540 -s ref_papel.py RefPapel → renders/fundo/papel_vazio_960x540.png"""
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manim import Scene, config  # noqa: E402
from papel27 import papel, placas27, usar_violeta  # noqa: E402


class RefPapel(Scene):
    def construct(self):
        usar_violeta(self)
        self.add(placas27(), papel())
        self.wait(0.1)
