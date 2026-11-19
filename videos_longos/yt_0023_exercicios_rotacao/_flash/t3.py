from manim import *
from vez import Vez
class V2(Scene):
    def construct(self):
        m = MathTex("a=b+c").scale(2).shift(DOWN*2)
        self.play(AnimationGroup(Vez(1.0, TransformFromCopy(MathTex("x").shift(UP*2), m, run_time=0.3)), Wait(1.5), lag_ratio=0), run_time=1.6)
        self.wait(0.5)
class V3(Scene):
    def construct(self):
        m = MathTex("a=b+c").scale(2).shift(DOWN*2); s = MathTex("x").shift(UP*2); self.add(s)
        g = AnimationGroup(UpdateFromAlphaFunc(s.copy(), lambda mm,t: None), FadeIn(m, rate_func=lambda t: max(0,(t-.4)/.6)), run_time=0.4)
        self.play(AnimationGroup(Vez(1.0, g), Wait(1.5), lag_ratio=0), run_time=1.6)
        self.wait(0.5)
class W3(Scene):
    def construct(self):
        m = MathTex("a=b+c").scale(2).shift(DOWN*2)
        self.play(AnimationGroup(Succession(Wait(1.0), AnimationGroup(FadeIn(m, rate_func=lambda t: max(0,(t-.4)/.6)), run_time=.4)), Wait(1.5), lag_ratio=0), run_time=1.6)
class W4(Scene):
    def construct(self):
        m = MathTex("a=b+c").scale(2).shift(DOWN*2)
        self.play(AnimationGroup(Succession(Wait(1.0), Write(m, run_time=.4)), Wait(1.5), lag_ratio=0), run_time=1.6)
