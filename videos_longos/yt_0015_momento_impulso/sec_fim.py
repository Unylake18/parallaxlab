"""Lote PS: síntese (S1, S2) e F1 (inscreva-se). v3: o mesmo gráfico F_res(t) em escala real do E4; o F2 (cavalo e corda) virou o
trecho 3D `cavalo` (CamadaCavalo em sec_3d.py)."""
from kit import *  # noqa: F401,F403
from sec_muro import f_joelho, grafico_escala, mostra_grafico


def tex(s, cor=WHITE_, size=M_MID):
    return MathTex(s, font_size=size, color=cor)


class LoteFim(Base):
    def construct(self):
        self.setup_base()
        self.secao("RESUMO")
        self.sintese()
        self.cta()
        self.fim()
        self.relatorio()

    def sintese(self):
        self.an("S1")
        g = grafico_escala(x0=-5.7, y0=-2.45, w=5.9, h=4.55)
        c1 = txt("MESMO IMPULSO", T_MAIN, color=JC, bold=True)
        c2a = linha(txt("MAIS TEMPO", T_LAB), MathTex(r"\Rightarrow", font_size=40, color=DIM), buff=0.2)
        c2b = txt("MENOS FORÇA MÉDIA", T_LAB, color=FC)
        c2 = VGroup(c2a, c2b).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        conta(c1, c2, topo=1.2, buff=0.6, x0=1.3)
        mostra_grafico(self, g, rt=0.8)
        self.play(FadeIn(g["aa"]), FadeIn(g["ab_l"]), run_time=0.6)
        self.add(cursor(self, g["G"], 0.0, 0.2, 4.0, f_joelho))
        self.ate(0.3)
        self.play(Write(c1), run_time=0.8)
        self.ate(0.5)                                    # v6 (G5): as duas áreas acendem (nada parado)
        self.play(Indicate(g["ret"], color=WHITE_, scale_factor=1.0), Indicate(g["aa"], color=WHITE_, scale_factor=1.1), run_time=0.8)
        self.play(Indicate(g["ab"], color=WHITE_, scale_factor=1.0), Indicate(g["ab_l"], color=WHITE_, scale_factor=1.1), run_time=0.8)
        self.ate(0.75)
        self.play(FadeIn(c2, shift=0.1 * UP), run_time=0.8)
        self.play(Indicate(g["cb"], color=WHITE_, scale_factor=1.0), run_time=0.8)
        self.ate(0.97)
        self.an("S2")
        self.play(FadeOut(c1), FadeOut(c2), run_time=0.5)
        e1 = Mc((r"\vec p", MAG), "=", "m", (r"\vec v", VEL), size=M_MID)
        e2 = Mc((r"\vec J", JC), "=", (r"\int \vec F_{res}\,dt", FC), "=", (r"\Delta\vec p", MAG), size=48)
        seta = lambda: MathTex(r"\to", font_size=40, color=DIM)
        e3 = linha(txt("TEMPO", T_MAIN), seta(), txt("MOMENTO", T_MAIN, color=MAG), buff=0.3)
        e4 = linha(txt("DISTÂNCIA", T_MAIN), seta(), txt("ENERGIA", T_MAIN), buff=0.3)
        conta(e1, e2, e3, e4, topo=2.1, buff=0.55, x0=1.3)
        self.play(Write(e1), run_time=0.9)
        self.ate(0.3)
        self.play(Write(e2), Indicate(VGroup(g["ab"], g["ret"]), color=WHITE_, scale_factor=1.0), run_time=1.1)
        self.ate(0.68)
        self.play(FadeIn(e3, shift=0.1 * RIGHT), Indicate(g["ab"], color=WHITE_, scale_factor=1.0), run_time=0.6)
        self.play(FadeIn(e4, shift=0.1 * RIGHT), run_time=0.6)
        self.ate(0.85)
        self.play(Indicate(e3[2], color=WHITE_, scale_factor=1.1), Indicate(e4[2], color=WHITE_, scale_factor=1.1), run_time=0.8)
        self.ate(0.97)

    def cta(self):
        self._pend = []
        self.an("F1")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.clk], run_time=0.8)
        for m in self.mobjects:
            m.clear_updaters()
        Scene.clear(self)
        self.h2 = self._sl = None
        oc = P3(0, 0.7)
        rings = VGroup(*[DashedVMobject(Circle(radius=r, arc_center=oc), num_dashes=max(12, int(14 * r)), dashed_ratio=0.6)
                         .set_stroke(VEL, 3.5, 0.16) for r in (2.0, 3.0, 4.0)])
        for i, r_ in enumerate(rings):
            r_.add_updater(lambda m, dt, sg=(1 if i % 2 == 0 else -1) * (0.06 - 0.01 * i): m.rotate(sg * dt, about_point=oc))
        logo = self.logo(6.0).move_to(oc + P3(0, 0.4))
        msg = txt("INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS", 28, op=0.9).move_to(oc + P3(0, -1.0))
        self.play(LaggedStart(*[FadeIn(r_, scale=0.85) for r_ in rings], lag_ratio=0.3), FadeIn(logo, scale=0.92), run_time=1.6)
        self.play(FadeIn(msg, shift=0.1 * UP), run_time=0.8)
        self.ate(0.97)
        self.play(FadeOut(logo), FadeOut(msg), *[FadeOut(r_) for r_ in rings], run_time=0.5)
        for r_ in rings:
            r_.clear_updaters()
