from manim import Rectangle, Scene, Text, config

import template.config


class Integral001(Scene):
    def construct(self):
        frame = Rectangle(
            width=config.frame_width - 0.2,
            height=config.frame_height - 0.2,
        )

        label = Text(
            "Parallax Lab\nTemplate vertical OK",
            font_size=40,
        )

        self.add(frame, label)
        self.wait(1)
