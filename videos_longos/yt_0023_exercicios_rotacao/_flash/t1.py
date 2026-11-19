from manim import *
class T1(Scene):
    def construct(self):
        m = MathTex("a=b+c").scale(2).shift(DOWN*2)
        g = AnimationGroup(Succession(Wait(1.0), FadeIn(m, run_time=0.3)), Wait(1.5), lag_ratio=0)
        self.play(g, run_time=1.6)
        self.wait(0.3)
class T2(Scene):
    def construct(self):
        m = MathTex("a=b+c").scale(2).shift(DOWN*2)
        g = AnimationGroup(Succession(Wait(1.0), TransformFromCopy(MathTex("x").shift(UP*2), m, run_time=0.3)), lag_ratio=0)
        self.play(g, run_time=1.6)
