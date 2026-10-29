"""Lote E: C13-6 e C13-7 (2D), síntese (S1, S2) e encerramento (E1, E2)."""
from kit import *  # noqa: F401,F403
from sec_c import DP, DT_DURA, DT_JOELHO


def tex(s, cor=WHITE_, size=M_MID):
    return MathTex(s, font_size=size, color=cor)


class LoteE(Base):
    def construct(self):
        self.setup_base(cap="EXERCÍCIO 9 · NEWTON E A LUZ", selo="MOYSÉS · PROB. 9.2")
        self.c13_fim()
        self.sintese()
        self.cta()
        self.fim()
        self.relatorio()

    def c13_fim(self):
        self.an("C13-6")
        ano = txt("1850 · FOUCAULT", 40, bold=True).move_to(P3(-3.6, 1.7))
        lenta = txt("A LUZ É MAIS LENTA NA ÁGUA", T_MAIN).move_to(P3(-3.6, 0.6))
        ve = tex(r"v_2>v_1", WHITE_, 56).move_to(P3(-3.6, -1.0))
        nw = txt("PREVISÃO DE NEWTON", T_SMALL, color=DIM).next_to(ve, DOWN, buff=0.3)
        ond = txt("DESCRIÇÃO ONDULATÓRIA", T_LAB, color=DIM).move_to(P3(4.2, 1.2))
        eo = Mc((r"\frac{\sin\theta_1}{\sin\theta_2}", WHITE_), "=", (r"\frac{v_1}{v_2}", VEL), size=M_MAIN).move_to(P3(4.2, -0.2))
        self.play(FadeIn(ano, shift=0.1 * UP), run_time=0.9)
        self.ate(0.3)
        self.play(FadeIn(lenta, shift=0.1 * UP), run_time=0.9)
        self.ate(0.45)
        self.play(FadeIn(ve), FadeIn(nw), run_time=0.7)
        self.play(ve.animate.set_color(APAGADO), Create(risco(ve, w=6)), run_time=0.8)
        self.ate(0.7)
        self.play(FadeIn(ond), FadeIn(eo, shift=0.1 * UP), run_time=0.9)
        self.ate(0.97)
        self.an("C13-7")
        self.clear(rt=0.6)
        a = txt("IMPULSO CERTO", 48, bold=True).move_to(P3(0, 1.4))
        b = txt("+ MODELO ERRADO", 48, bold=True, color=APAGADO).move_to(P3(0, 0.3))
        c = txt("= PREVISÃO TESTÁVEL", 48, bold=True, color=CYAN).move_to(P3(0, -1.0))
        self.play(FadeIn(a, shift=0.1 * UP), run_time=0.9)
        self.ate(0.35)
        self.play(FadeIn(b, shift=0.1 * UP), run_time=0.9)
        self.ate(0.65)
        self.play(FadeIn(c, shift=0.1 * UP), run_time=0.9)
        self.ate(0.97)

    # ── síntese ─────────────────────────────────────────────────────────────────────────────────────────────
    def sintese(self):
        self.clear(rt=0.6)
        self.secao("RESUMO")
        self.an("S1")
        FMAX = 7000.0
        Ga = Graf(-6.5, -2.4, 4.4, 3.6, 0.02, FMAX, MathTex(r"F_{res}", font_size=36, color=FC))
        Gb = Graf(0.2, -2.4, 6.6, 3.6, 0.20, FMAX, MathTex(r"F_{res}", font_size=36, color=FC))
        fa, fb = meia_senoide(DP, DT_DURA), meia_senoide(DP, DT_JOELHO)
        itens = [Ga.eixos, Gb.eixos, Ga.curva(fa, 0, 0.02, n=400), Gb.curva(fb, 0, 0.20, n=400),
                 Ga.area(fa, 0, DT_DURA, n=200), Gb.area(fb, 0, DT_JOELHO, n=200)]
        la = txt("PERNAS DURAS", T_LAB, bold=True).move_to(P3(-4.3, 2.0))
        lb = txt("JOELHOS", T_LAB, bold=True).move_to(P3(3.5, 2.0))
        ala = Mc((r"\text{ÁREA}=560\ \mathrm{N\cdot s}", JC), size=32).move_to(P3(-4.3, -3.4))
        alb = Mc((r"\text{ÁREA}=560\ \mathrm{N\cdot s}", JC), size=32).move_to(P3(3.5, -3.4))
        self.play(*[FadeIn(m) for m in itens], FadeIn(la), FadeIn(lb), run_time=1.2)
        self.ate(0.45)
        self.play(FadeIn(ala), FadeIn(alb), run_time=0.8)
        self.ate(0.97)
        self.an("S2")
        self.clear(rt=0.6)
        e1 = Mc((r"\vec J", JC), "=", (r"\int \vec F_{res}\,dt", FC), "=", (r"\Delta\vec p", MAG), size=M_MAIN).move_to(P3(0, 1.2))
        e2 = Mc((r"\frac{d\vec P}{dt}", MAG), "=", (r"\vec F_{ext}", FC), size=M_MAIN).move_to(P3(0, -1.2))
        n1 = txt("IMPULSO DA FORÇA RESULTANTE", T_SMALL, color=DIM).next_to(e1, DOWN, buff=0.3)
        n2 = txt("COMPONENTE POR COMPONENTE", T_SMALL, color=DIM).next_to(e2, DOWN, buff=0.3)
        self.play(FadeIn(e1, shift=0.1 * UP), FadeIn(n1), run_time=1.0)
        self.ate(0.5)
        self.play(FadeIn(e2, shift=0.1 * UP), FadeIn(n2), run_time=1.0)
        self.ate(0.97)

    # ── encerramento ────────────────────────────────────────────────────────────────────────────────────────
    def cta(self):
        self._pend = []
        self.an("E1")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.clk], run_time=1.0)
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
        self.play(LaggedStart(*[FadeIn(r_, scale=0.85) for r_ in rings], lag_ratio=0.3), FadeIn(logo, scale=0.92), run_time=1.8)
        self.play(FadeIn(msg, shift=0.1 * UP), run_time=0.9)
        self.ate(0.97)
        # E2 — granada ---------------------------------------------------------------------------------------
        self.an("E2")
        self.play(FadeOut(logo), FadeOut(msg), *[FadeOut(r_) for r_ in rings], run_time=0.6)
        for r_ in rings:
            r_.clear_updaters()
        self.remove(*rings)
        X0, X1, Y0, H = -5.8, 5.8, -2.5, 3.0

        def par(s):
            return P3(X0 + (X1 - X0) * s, Y0 + 4 * H * s * (1 - s))

        caminho = DashedVMobject(VMobject().set_points_smoothly([par(s) for s in np.linspace(0, 1, 40)]).set_stroke(DIM, 2, opacity=0.6),
                                 num_dashes=60)
        pergunta = txt("SE A GRANADA EXPLODE NO AR, O QUE CONTINUA NA PARÁBOLA?", 30, bold=True).move_to(P3(0, 3.3))
        prox1 = txt("PRÓXIMO VÍDEO:", 26, op=0.9).move_to(P3(-1.7, -3.6))
        prox2 = txt("CENTRO DE MASSA", 30, color=CYAN, bold=True).next_to(prox1, RIGHT, buff=0.3)
        s_ = ValueTracker(0.0)
        dirs = [(math.cos(a), math.sin(a)) for a in np.linspace(0, 2 * PI, 7)[:-1] + 0.3]

        def granada():
            s = s_.get_value()
            c = par(s)
            g = VGroup()
            if s < 0.5:
                g.add(bola(0.22, STEEL).move_to(c))
            else:
                k = (s - 0.5) * 7.0
                for dx, dy in dirs:
                    g.add(Circle(radius=0.08).set_stroke(mix(STEEL, 0.5), 1.5).set_fill(STEEL, 1.0).move_to(c + P3(dx * k, dy * k * 0.9)))
                g.add(Dot(c, radius=0.1, color=WHITE_).set_z_index(9))
                if s < 0.56:
                    g.add(flash(c).set_z_index(9))
            return g
        gr = always_redraw(granada)
        self.play(FadeIn(pergunta, shift=0.1 * UP), Create(caminho), run_time=1.4)
        self.add(gr)
        self.ate(0.3)
        self.play(s_.animate.set_value(1.0), run_time=7.0, rate_func=linear)
        self.play(FadeIn(prox1), FadeIn(prox2, shift=0.1 * UP), run_time=0.8)
        self.ate(0.97)
        gr.clear_updaters()
