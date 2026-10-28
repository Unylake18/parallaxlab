"""Lote PS: síntese (S1 o cavalo com a fronteira; S2 as três ideias) e encerramento (EN1 inscreva-se; EN2 granada → centro de massa)."""
from kit import *  # noqa: F401,F403
from sec_cavalo import Tropa


class LoteFim(Base):
    def construct(self):
        self.setup_base(cap="RESUMO")
        self.sintese()
        self.cta()
        self.fim()
        self.relatorio()

    def sintese(self):
        self.an("S1")
        tr = Tropa(esc=0.8, xc=1.9, xp=-3.6, y=-2.0)
        ch = chao(-7.4, 7.4, -2.0)
        g = tr.grupo()
        self.play(FadeIn(ch), FadeIn(g), run_time=1.0)
        p = tr.pts()
        u = tr.dir_corda()
        fr = fronteira(9.6, 3.6, P3(-0.25, -0.15), rotulo="SISTEMA")
        ta = arrow(p["gancho"] + 0.08 * u, p["gancho"] + 1.2 * u, color=INT, width=6, tip=0.18)
        tb = arrow(p["traseira"] - 0.04 * u, p["traseira"] - 1.16 * u, color=INT, width=6, tip=0.18)
        lt = txt("INTERNA", 18, color=INT).move_to((p["gancho"] + p["traseira"]) / 2 + P3(0.3, -0.45))
        fc = arrow(P3(p["cav"][0], -2.3), P3(p["cav"][0] + 1.75, -2.3), color=FC, width=7, tip=0.2)
        fp = arrow(P3(p["ped"][0] + 0.45, -2.3), P3(p["ped"][0] + 0.45 - 1.47, -2.3), color=FC, width=7, tip=0.2)
        lfc = txt("CHÃO NAS PATAS", 16, color=FC).next_to(fc, DOWN, buff=0.1)
        lfp = txt("CHÃO NA PEDRA", 16, color=FC).next_to(fp, DOWN, buff=0.1)
        self.ate(0.12)
        self.play(Create(fr[0]), FadeIn(fr[1]), run_time=1.0)
        self.ate(0.3)
        self.play(GrowArrow(ta), GrowArrow(tb), FadeIn(lt), run_time=0.8)
        self.ate(0.6)
        self.play(GrowArrow(fc), GrowArrow(fp), FadeIn(lfc), FadeIn(lfp), run_time=0.9)
        r = txt("QUEM ACELERA O CAVALO E A PEDRA É O CHÃO", 26, bold=True).move_to(P3(0, 2.35))
        self.ate(0.75)
        self.play(FadeIn(r, shift=0.1 * UP), run_time=0.7)
        self.ate(0.97)
        g.clear_updaters()
        self.an("S2")
        self.clear(rt=0.5)
        i1 = VGroup(txt("1", 30, color=CYAN, bold=True), Mc((r"\frac{d\vec P}{dt}", MAG), "=", (r"\vec F^{\,ext}", FC), size=56),
                    txt("COMPONENTE POR COMPONENTE", 20, color=DIM)).arrange(RIGHT, buff=0.45)
        i2 = VGroup(txt("2", 30, color=CYAN, bold=True), txt("MOMENTO SE DIVIDE IGUAL; ENERGIA, NÃO", 30, bold=True)).arrange(RIGHT, buff=0.45)
        i3 = VGroup(txt("3", 30, color=CYAN, bold=True), linha(txt("NÃO CONSERVA?", 30, bold=True),
                                                               txt("AUMENTE O SISTEMA", 30, bold=True, color=MAG), buff=0.15)).arrange(RIGHT, buff=0.45)
        col = VGroup(i1, i2, i3).arrange(DOWN, buff=0.75, aligned_edge=LEFT).move_to(P3(0, -0.2))
        for m, frac in ((i1, 0.05), (i2, 0.42), (i3, 0.75)):
            self.ate(frac)
            self.play(FadeIn(m, shift=0.1 * UP), run_time=0.8)
        self.ate(0.97)

    def cta(self):
        self._pend = []
        self.an("EN1")
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
        # EN2 — granada --------------------------------------------------------------------------------------
        self.an("EN2")
        self.play(FadeOut(logo), FadeOut(msg), *[FadeOut(r_) for r_ in rings], run_time=0.6)
        for r_ in rings:
            r_.clear_updaters()
        self.remove(*rings)
        X0, X1, Y0, H = -5.8, 5.8, -2.5, 3.0

        def par(s):
            return P3(X0 + (X1 - X0) * s, Y0 + 4 * H * s * (1 - s))

        caminho = DashedVMobject(VMobject().set_points_smoothly([par(s) for s in np.linspace(0, 1, 40)]).set_stroke(DIM, 2, opacity=0.6),
                                 num_dashes=60)
        pergunta = txt("SE A GRANADA EXPLODE NO AR, O QUE CONTINUA NA PARÁBOLA?", 30, bold=True).move_to(P3(0, 3.0))
        s_ = ValueTracker(0.0)
        # fragmentos de massas iguais com velocidades relativas opostas aos pares: o centro de massa segue a parábola
        dirs = [(math.cos(a), math.sin(a)) for a in np.linspace(0, 2 * PI, 7)[:-1] + 0.3]

        def granada():
            s = s_.get_value()
            c = par(s)
            g = VGroup()
            if s < 0.45:
                g.add(bola(0.22, STEEL).move_to(c))
            else:
                k = (s - 0.45) * 6.5
                for dx, dy in dirs:
                    g.add(Circle(radius=0.08).set_stroke(mix(STEEL, 0.5), 1.5).set_fill(STEEL, 1.0).move_to(c + P3(dx * k, dy * k * 0.9)))
                g.add(Dot(c, radius=0.1, color=CYAN).set_z_index(9))
                if s < 0.51:
                    g.add(flash(c).set_z_index(9))
            return g
        gr = always_redraw(granada)
        self.play(FadeIn(pergunta, shift=0.1 * UP), Create(caminho), run_time=1.4)
        self.add(gr)
        self.ate(0.12)
        self.play(s_.animate.set_value(1.0), run_time=7.0, rate_func=linear)
        prox1 = txt("PRÓXIMO VÍDEO:", 26, op=0.9)
        prox2 = txt("CENTRO DE MASSA", 30, color=CYAN, bold=True)
        VGroup(prox1, prox2).arrange(RIGHT, buff=0.3).move_to(P3(0, -3.4))
        self.play(FadeIn(prox1), FadeIn(prox2, shift=0.1 * UP), run_time=0.8)
        self.ate(0.97)
        gr.clear_updaters()
