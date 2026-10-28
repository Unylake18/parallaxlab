"""Lote PS (v2): síntese (S1 o cavalo 3D com a fronteira; S2 as três ideias com desenhos) e encerramento. Antes: síntese (S1 o cavalo com a fronteira; S2 as três ideias) e encerramento (EN1 inscreva-se; EN2 granada → centro de massa)."""
from kit import *  # noqa: F401,F403
from sec_cavalo import Cavalo3D


class LoteFim(Base):
    def construct(self):
        self.setup_base(cap="RESUMO")
        self.sintese()
        self.cta()
        self.fim()
        self.relatorio()

    def sintese(self):
        self.an("S1")
        cv = self.cv = Cavalo3D(self, v=lambda t: 0.42, K=0.95, xt=2.1, yc=-2.4, op=0.0)
        self.add(cv.f3d)
        self.play(cv.f3d.op.animate.set_value(1.0), run_time=1.0)

        def front():
            p = cv.pts()
            xl, xr = p["pedra_tras"][0] - 0.3, p["cabeca"][0] + 0.35
            y0, y1 = p["cascos"][1] - 0.15, p["topo"][1] + 0.22
            r = RoundedRectangle(corner_radius=0.3, width=xr - xl, height=y1 - y0).move_to(P3((xl + xr) / 2, (y0 + y1) / 2))
            r.set_stroke(WHITE_, 2.2, opacity=0.62)
            return VGroup(DashedVMobject(r, num_dashes=int((xr - xl + y1 - y0) * 5), dashed_ratio=0.55).set_z_index(1),
                          mtxt("SISTEMA", 16, op=0.8).next_to(r.get_corner(UL), UP, buff=0.1).align_to(r, LEFT).shift(0.25 * RIGHT))
        fr = always_redraw(front)
        tens = ValueTracker(0.0)
        ext = ValueTracker(0.0)

        def forcas():
            p = cv.pts()
            k = cv.K.get_value()
            g = VGroup()
            if tens.get_value() > 0.01:
                g.add(arrow(p["corda_pedra"] + P3(0.05, -0.14), p["corda_pedra"] + P3(1.4, -0.14), color=INT, width=6, tip=0.17, z=12),
                      arrow(p["peito"] + P3(0.55 * k + 1.35, 0), p["peito"] + P3(0.55 * k, 0), color=INT, width=6, tip=0.17, z=12),
                      mtxt("INTERNA", 15, color=INT).move_to(p["peito"] + P3(0.55 * k + 0.7, -0.32)))
            if ext.get_value() > 0.01:
                yb = p["cascos"][1] - 0.3
                g.add(arrow(P3(p["cascos"][0] - 0.2, yb), P3(p["cascos"][0] + 1.4, yb), color=FC, width=7, tip=0.2, z=12),
                      arrow(P3(p["pedra_base"][0] + 0.2, yb), P3(p["pedra_base"][0] - 0.98, yb), color=FC, width=7, tip=0.2, z=12),
                      mtxt("CHÃO NAS PATAS", 15, color=FC).move_to(P3(p["cascos"][0] + 0.6, yb - 0.3)),
                      mtxt("CHÃO NA PEDRA", 15, color=FC).move_to(P3(p["pedra_base"][0] - 0.4, yb - 0.3)))
            return g
        fz = always_redraw(forcas)
        self.add(fz)
        self.ate(0.12)
        self.play(FadeIn(fr), run_time=1.0)
        self.ate(0.3)
        self.play(tens.animate.set_value(1.0), run_time=0.6)
        self.ate(0.6)
        self.play(ext.animate.set_value(1.0), run_time=0.6)
        r = txt("QUEM ACELERA O CAVALO E A PEDRA É O CHÃO", 26, bold=True).move_to(P3(0, 2.3))
        self.ate(0.75)
        self.play(FadeIn(r, shift=0.1 * UP), run_time=0.7)
        self.ate(0.97)
        # S2 — três ideias, cada uma com o seu desenho pequeno no PALCO (o cavalo encolhe para a terceira)
        self.an("S2")
        fr.clear_updaters(); fz.clear_updaters()
        self.play(FadeOut(fr), FadeOut(fz), FadeOut(r), cv.K.animate.set_value(0.3), cv.xt.animate.set_value(-4.35), cv.yc.animate.set_value(-2.55),
                  run_time=1.0)
        self.remove(fr, fz)
        t0 = self.clk.get_value()

        def esferas():
            a = math.sin(2 * PI * (self.clk.get_value() - t0) / 2.4)
            c = P3(-5.0, 1.45)
            ps = [c + P3(-0.55 - 0.05 * a, -0.35), c + P3(0.55 + 0.05 * a, -0.35), c + P3(0, 0.45 - 0.06 * a)]
            g = VGroup()
            for i, j in ((0, 1), (0, 2), (1, 2)):
                g.add(mola(ps[i], ps[j], n=5, amp=0.06, cor=FC, w=2))
            for q in ps:
                g.add(bola(0.17, GEO).move_to(q))
            return g

        def blocos():
            s = ((self.clk.get_value() - t0) % 3.0) / 3.0
            c = P3(-5.0, -0.25)
            d = 0.5 * math.sin(PI * s)
            g = VGroup(Arc(radius=3.0, start_angle=PI * 0.38, angle=PI * 0.24, arc_center=c + P3(0, -3.35)).set_stroke(mix(TERRA, 0.35), 2)
                       .set_fill(TERRA, 1))
            g.add(Square(0.32).set_stroke(width=0).set_fill(GEO, 1).move_to(c + P3(-0.25 - d, 0.0)),
                  Square(0.42).set_stroke(width=0).set_fill(STEEL, 1).move_to(c + P3(0.3 + 0.5 * d, 0.05)))
            return g
        de = always_redraw(esferas)
        db = always_redraw(blocos)
        i1 = linha(tex(r"\frac{d\vec P}{dt}", MAG, 46), mais(40, "="), tex(r"\vec F^{\,ext}", FC, 46),
                   txt("COMPONENTE POR COMPONENTE", 18, color=DIM), buff=0.25)
        i2 = txt("MOMENTO SE DIVIDE IGUAL; ENERGIA, NÃO", 26, bold=True)
        i3 = linha(txt("NÃO CONSERVA?", 26, bold=True), txt("AUMENTE O SISTEMA", 26, bold=True, color=MAG), buff=0.18)
        for m_, y in ((i1, 1.45), (i2, -0.2), (i3, -1.85)):
            m_.move_to(P3(-3.6 + m_.width / 2, y))
        for (m_, dsn, frac) in ((i1, de, 0.05), (i2, db, 0.42), (i3, None, 0.75)):
            self.ate(frac)
            self.play(FadeIn(m_, shift=0.1 * UP), *([FadeIn(dsn)] if dsn is not None else [Indicate(m_, color=WHITE_, scale_factor=1.02)]),
                      run_time=0.8)
        self.ate(0.97)
        de.clear_updaters(); db.clear_updaters()

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
