from manim import DOWN, Rectangle, Scene, VGroup, config

import template.config
from template.helpers import make_equation, make_title


class Integral001(Scene):
    def construct(self):
        frame = Rectangle(
            width=config.frame_width - 0.2,
            height=config.frame_height - 0.2,
        )

        # Smoke test temporário dos helpers, sem conteúdo do piloto.
        title = make_title("Parallax Lab\nTemplate vertical OK")
        equation = make_equation(r"1 + 1 = 2")
        content = VGroup(title, equation).arrange(DOWN, buff=0.8)

        self.add(frame, content)
        self.wait(1)
