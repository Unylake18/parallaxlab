from manim import *


class TesteIntegral(Scene):
    def construct(self):
        titulo = Text("Integração por partes", font_size=48)

        integral = MathTex(
            r"\int x^2e^x\,dx"
        ).scale(1.5)

        integral.next_to(titulo, DOWN, buff=1)

        self.play(Write(titulo))
        self.play(Write(integral))

        self.wait(2)