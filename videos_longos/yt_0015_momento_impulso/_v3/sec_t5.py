"""Lote PD: T5 — impulso. v3: força constante (PALCO + gráfico na CONTA), a força da parede (parede grande no PALCO, gráfico na
CONTA), Riemann 4 → 8 → 32 com contador no canto do gráfico, Σ → ∫, o dt se cancelando no CENTRO, área e força média, duas curvas
com a mesma área (DOIS PAINÉIS) e o vetor J⃗ no CENTRO com a DICA."""
from MF_Tools import TransformByGlyphMap

from kit import *  # noqa: F401,F403

J_PAREDE, DT_PAREDE = 20.0, 0.010          # N·s ; s  (bola de 0,40 kg: 0,40·(20 − (−30)))
F_MED = J_PAREDE / DT_PAREDE               # 2000 N
PAREDE_X = -5.9
RAIO_BOLA = 0.48
CONTATO_X = PAREDE_X + RAIO_BOLA
YB = -0.9


def bola_x(tp, t0=DT_PAREDE, tau=DT_PAREDE):
    """Centro da bola: velocidade constante até o contato, parada comprimida durante o contato, volta mais devagar."""
    if tp < t0:
        return CONTATO_X + 240.0 * (t0 - tp)
    if tp <= t0 + tau:
        return CONTATO_X
    return CONTATO_X + 160.0 * (tp - t0 - tau)


def squash(tp, t0=DT_PAREDE, tau=DT_PAREDE):
    if t0 <= tp <= t0 + tau:
        return 1.0 - 0.28 * math.sin(math.pi * (tp - t0) / tau)
    return 1.0


def triangulo(J, t0, tp, t1):
    """F(t) triangular (sobe até tp, desce até t1) com área exatamente J."""
    pico = 2 * J / (t1 - t0)

    def f(t):
        if t0 <= t <= tp:
            return pico * (t - t0) / (tp - t0)
        if tp < t <= t1:
            return pico * (t1 - t) / (t1 - tp)
        return 0.0
    return f


def s_tex(s, size=48):
    m = MathTex(s, font_size=size)
    g = m[0]
    return m, g


class LoteT5(Base):
    def construct(self):
        self.setup_base(cap="IMPULSO")
        self.t5_1()
        self.t5_2()
        self.t5_3()
        self.t5_4()
        self.t5_5()
        self.t5_6()
        self.fim()
        self.relatorio()

    def grafico(self, tmax, fmax, rot=r"F_x"):
        return Graf(1.35, -2.6, 5.2, 4.4, tmax, fmax, MathTex(rot, font_size=42, color=FC))

    # ── T5-1 · força constante: PALCO bloco + equações; CONTA gráfico F(t) com a área ─────────────────────────
    def t5_1(self):
        self.an("T5-1")
        yt = 0.4
        trilho = Line(P3(-6.6, yt), P3(0.6, yt)).set_stroke(GEO, 2.5, opacity=0.6)
        xb = ValueTracker(-5.3)
        blk = Corpo("m", STEEL, 1.3, size=48)
        blk.add_updater(lambda m: m.move_to(P3(xb.get_value(), yt + 0.65)))
        fa = always_redraw(lambda: arrow(P3(xb.get_value() + 0.65, yt + 0.65), P3(xb.get_value() + 2.5, yt + 0.65), color=FC, width=9, tip=0.28))
        fl = always_redraw(lambda: MathTex(r"\vec F", font_size=46, color=FC).move_to(P3(xb.get_value() + 1.6, yt + 1.3)))
        G = self.grafico(1.0, 1.0, r"F")
        nivel = 0.62
        tt = ValueTracker(0.2001)
        rect = always_redraw(lambda: Rectangle(width=G.w * (tt.get_value() - 0.2), height=G.h * nivel).set_stroke(FC, 4).set_fill(JC, 0.45)
                             .move_to((G.pt(0.2, 0) + G.pt(tt.get_value(), nivel)) / 2).set_z_index(3))
        dt = BraceBetweenPoints(G.pt(0.2, 0) + P3(0, -0.05), G.pt(0.8, 0) + P3(0, -0.05), direction=DOWN, color=DIM)
        dtl = MathTex(r"\Delta t", font_size=40, color=DIM).next_to(dt, DOWN, buff=0.1)
        e2 = Mc((r"\Delta\vec p", MAG), "=", (r"\vec F", FC), (r"\,\Delta t", WHITE_), size=M_MID)
        e1 = Mc((r"\vec J", JC), "=", (r"\vec F", FC), (r"\,\Delta t", WHITE_), size=M_MID)
        nm = txt("IMPULSO", T_LAB, color=JC, bold=True)
        VGroup(e2, e1).arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to(P3(-3.6, -1.6))
        nm.next_to(e1, LEFT, buff=0.4)
        self.play(Create(trilho), FadeIn(blk), run_time=0.7)
        a0 = arrow(P3(-5.3 + 0.65, 0.4 + 0.65), P3(-5.3 + 2.5, 0.4 + 0.65), color=FC, width=9, tip=0.28)
        self.play(GrowArrow(a0), run_time=0.6)
        self.remove(a0)
        self.add(fa)
        self.play(FadeIn(fl), run_time=0.4)
        self.play(Create(G.eixos), run_time=0.8)
        self.ate(0.2)
        self.add(rect)
        self.play(xb.animate.set_value(-3.6), tt.animate.set_value(0.8), FadeIn(dt), FadeIn(dtl), run_time=2.4, rate_func=lambda u: u * u)
        rect.clear_updaters()
        self.ate(0.45)
        self.play(Write(e2), run_time=1.0)
        self.ate(0.72)
        self.play(Write(e1), FadeIn(nm), run_time=1.0)
        jl = MathTex(r"\vec J", font_size=52, color=WHITE_).move_to(rect)
        self.play(FadeIn(jl), Indicate(rect, color=JC, scale_factor=1.03), run_time=0.8)
        self.ate(0.97)
        for m in (blk, fa, fl):
            m.clear_updaters()

    # ── T5-2 · a força da parede: PALCO parede grande e bola; CONTA gráfico F_x(t) ─────────────────────────────
    def t5_2(self):
        self.clear(rt=0.5)
        self.an("T5-2")
        self.parede = Rectangle(width=0.6, height=3.4).set_stroke(GEO, 2.5).set_fill(STEEL, 1).move_to(P3(PAREDE_X - 0.3, YB + 1.2))
        self.chao = Line(P3(-6.6, YB - RAIO_BOLA), P3(0.6, YB - RAIO_BOLA)).set_stroke(GEO, 2.5, opacity=0.6)
        self.G = G = self.grafico(0.030, 7000)
        lab = txt("FORÇA DA PAREDE", T_SMALL, color=FC).next_to(G.ey, RIGHT, buff=0.3)
        self.lab_forca = lab
        tp = ValueTracker(0.0)
        self.fun = fun = meia_senoide(J_PAREDE, DT_PAREDE, DT_PAREDE)
        b = bola(RAIO_BOLA)
        b.add_updater(lambda m: m.become(bola(RAIO_BOLA).stretch(squash(tp.get_value()), 0).move_to(P3(bola_x(tp.get_value()), YB))))
        curva = always_redraw(lambda: G.curva(fun, 0.0, max(tp.get_value(), 1e-4), n=int(40 + 600 * tp.get_value())))
        marca = always_redraw(lambda: Dot(G.pt(tp.get_value(), fun(tp.get_value())), radius=0.08, color=WHITE_).set_z_index(9))
        vel = always_redraw(lambda: arrow(P3(bola_x(tp.get_value()), YB + 0.95),
                                          P3(bola_x(tp.get_value()) + (-1.6 if tp.get_value() < DT_PAREDE else 1.05), YB + 0.95), color=VEL, width=6)
                            if not (DT_PAREDE <= tp.get_value() <= 2 * DT_PAREDE) else VMobject())
        self.play(FadeIn(self.parede, shift=0.2 * RIGHT), Create(self.chao), FadeIn(b), run_time=0.8)
        self.play(Create(G.eixos), FadeIn(lab), run_time=0.8)
        self.add(curva, marca, vel)
        self.ate(0.12)
        self.play(tp.animate.set_value(0.030), run_time=0.72 * ANC["T5-2"]["dur"], rate_func=linear)
        for m in (b, curva, marca, vel):
            m.clear_updaters()
        self.remove(marca, vel)
        self.bola_ = b
        self.curva = G.curva(fun, 0.0, 0.030, n=500)
        self.add(self.curva)
        self.remove(curva)
        self.play(Indicate(self.curva, color=WHITE_, scale_factor=1.0), run_time=0.8)
        self.ate(0.97)

    # ── T5-3 · Riemann 4 → 8 → 32 (contador no canto do gráfico); Σ no PALCO ──────────────────────────────────
    def retangulos(self, n):
        G, f = self.G, self.fun
        a, b = DT_PAREDE, 2 * DT_PAREDE
        dx = (b - a) / n
        g = VGroup()
        for k in range(n):
            t0 = a + k * dx
            h = f(t0 + dx / 2)
            r = Rectangle(width=G.w * dx / G.tmax, height=max(G.h * h / G.fmax, 0.001))
            r.move_to((G.pt(t0, 0) + G.pt(t0 + dx, h)) / 2).set_stroke(FC, 1.5 if n < 32 else 0.8).set_fill(JC, 0.5).set_z_index(4)
            g.add(r)
        soma = sum(f(a + (k + 0.5) * dx) * dx for k in range(n))
        return g, soma

    def t5_3(self):
        self.an("T5-3")
        self.play(FadeOut(self.bola_), FadeOut(self.parede), FadeOut(self.chao), run_time=0.5)
        sig = Mc((r"\sum_k", WHITE_), (r"\vec F_k", FC), (r"\,\Delta t_k", WHITE_), size=88).move_to(P3(-3.0, 0.4))
        G = self.G
        cont = VGroup(txt("RETÂNGULOS", 18, color=DIM), Integer(4, font_size=36, color=WHITE_)).arrange(RIGHT, buff=0.15)
        cont.move_to(G.pt(0.0245, 6300))
        ret, s4 = self.retangulos(4)
        self.ate(0.15)
        fat = txt("FATIAS DE TEMPO", T_SMALL, color=DIM).next_to(sig, DOWN, buff=0.5)
        self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in ret], lag_ratio=0.2), FadeIn(cont), Write(sig), run_time=1.4)
        self.ate(0.4)
        self.play(Indicate(sig[1], color=FC, scale_factor=1.15), run_time=0.8)
        self.play(FadeIn(fat), run_time=0.5)
        somas = [s4]
        for n in (8, 32):
            self.ate(0.6 if n == 8 else 0.8)
            novo, s = self.retangulos(n)
            somas.append(s)
            self.play(ReplacementTransform(ret, novo), cont[1].animate.set_value(n), run_time=1.0)
            ret = novo
        print("[QA] T5-3 somas de Riemann (4, 8, 32):", ", ".join(f"{s:.3f}" for s in somas), "N·s (alvo 20)")
        self.ate(0.97)
        self.ret, self.sig, self.cont, self.fat = ret, sig, cont, fat

    # ── T5-4 · Σ → ∫ (peça por peça) e o dt se cancelando no CENTRO ───────────────────────────────────────────
    def t5_4(self):
        self.an("T5-4")
        G = self.G
        area = G.area(self.fun, DT_PAREDE, 2 * DT_PAREDE)
        integ = Mc((r"\int", WHITE_), (r"\vec F", FC), (r"\,dt", WHITE_), size=88).move_to(self.sig)
        lim = MathTex(r"\Delta t_k\to 0", font_size=44, color=DIM).move_to(self.fat)
        self.play(FadeOut(self.cont), FadeTransform(self.fat, lim), run_time=0.5)
        self.play(*[ReplacementTransform(self.sig[i], integ[i]) for i in range(3)], FadeTransform(self.ret, area), run_time=1.2)
        jl = txt("IMPULSO", T_LAB, color=JC, bold=True).next_to(integ, UP, buff=0.4)
        self.play(FadeIn(jl), run_time=0.5)
        self.ate(0.33)
        # CENTRO: ∫F_res dt = ∫(dp/dt)dt = ∫dp = Δp
        self.play(FadeOut(G.eixos), FadeOut(self.curva), FadeOut(area), FadeOut(lim), FadeOut(jl), FadeOut(self.lab_g()), run_time=0.5)
        S1 = r"\int \vec F_{res}\,dt"
        S2 = r"\int \vec F_{res}\,dt=\int\frac{d\vec p}{dt}\,dt"
        S3 = r"\int \vec F_{res}\,dt=\int d\vec p"
        S4 = r"\int \vec F_{res}\,dt=\int d\vec p=\Delta\vec p"
        s1, s2, s3, s4 = (centro(MathTex(s, font_size=78), 0.3) for s in (S1, S2, S3, S4))
        for m in (s1, s2, s3, s4):
            for i in (1, 2, 3, 4, 5):
                m[0][i].set_color(FC)
        for m in (s2, s3, s4):
            for i in (10, 11, 12):
                m[0][i].set_color(MAG)
        for i in (14, 15, 16):
            s4[0][i].set_color(MAG)
        s1.move_to(s2[0][0:8].get_center())
        s1.modo_centro = False
        self.play(FadeTransform(integ, s1), run_time=0.8)
        self.play(TransformByGlyphMap(s1, s2, ([0, 1, 2, 3, 4, 5, 6, 7], [0, 1, 2, 3, 4, 5, 6, 7]),
                                      ([], [8, 9, 10, 11, 12, 13, 14, 15, 16, 17], {"shift": 0.1 * LEFT})), run_time=1.0)
        self.ate(0.6)
        cortes = VGroup(*[Line(VGroup(*[s2[0][i] for i in par]).get_corner(DL) + P3(-0.05, -0.05),
                               VGroup(*[s2[0][i] for i in par]).get_corner(UR) + P3(0.05, 0.05)).set_stroke(MAG, 5).set_z_index(20)
                          for par in ((14, 15), (16, 17))])
        self.play(Create(cortes[0]), Create(cortes[1]), run_time=0.7)
        dts = VGroup(*[s2[0][i] for i in (13, 14, 15, 16, 17)])
        self.play(TransformByGlyphMap(s2, s3, ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
                                      ([10, 11, 12], [10, 11, 12]), ([13, 14, 15, 16, 17], [], {"shift": 0.6 * DOWN})),
                  FadeOut(cortes, shift=0.6 * DOWN), run_time=1.1)
        self.ate(0.8)
        self.play(TransformByGlyphMap(s3, s4, ([], [13, 14, 15, 16], {"shift": 0.1 * LEFT})), run_time=0.9)
        cx = SurroundingRectangle(s4, color=JC, buff=0.28, stroke_width=3, corner_radius=0.12)
        jv = legenda("O IMPULSO DA FORÇA RESULTANTE É A VARIAÇÃO DO MOMENTO", T_LAB, color=JC)
        self.play(Create(cx), FadeIn(jv), run_time=0.7)
        self.play(Indicate(s4[0][14:17], color=MAG, scale_factor=1.15), run_time=0.8)
        self.ate(0.97)
        self.cadeia = VGroup(s4, cx, jv)

    def lab_g(self):
        return getattr(self, "lab_forca", VMobject())

    # ── T5-5 · DOIS PAINÉIS: a curva da parede com o retângulo da média; outra forma com a mesma área ─────────
    def t5_5(self):
        self.an("T5-5")
        self.play(FadeOut(self.cadeia), run_time=0.5)
        GA = Graf(-6.3, -2.2, 5.4, 3.9, 0.030, 7000, MathTex(r"F_x", font_size=40, color=FC))
        GB = Graf(0.75, -2.2, 5.4, 3.9, 0.030, 7000, MathTex(r"F_x", font_size=40, color=FC))
        fA = self.fun
        fB = triangulo(J_PAREDE, 0.006, 0.009, 0.024)
        cA, cB = GA.curva(fA, 0, 0.030, n=500), GB.curva(fB, 0, 0.030, n=500)
        tA, tB = ValueTracker(DT_PAREDE + 1e-4), ValueTracker(0.006 + 1e-4)
        aA = always_redraw(lambda: GA.area(fA, DT_PAREDE, tA.get_value()))
        aB = always_redraw(lambda: GB.area(fB, 0.006, tB.get_value()))
        A1, A2 = area_num(fA, 0, 0.030), area_num(fB, 0, 0.030)
        print(f"[QA] T5-5 áreas: meia-senoide {A1:.4f} N·s, triângulo {A2:.4f} N·s (alvo 20)")
        self.play(Create(GA.eixos), Create(GB.eixos), run_time=0.8)
        self.play(Create(cA), run_time=0.8)
        self.add(aA)
        self.play(tA.animate.set_value(2 * DT_PAREDE), run_time=1.2, rate_func=linear)
        aA.clear_updaters()
        ret = GA.retangulo(DT_PAREDE, 2 * DT_PAREDE, F_MED)
        fm = Mc((r"F_{\mathrm{m\acute{e}d}}", FC), "=", (r"\frac{J}{\Delta t}", JC), size=46).move_to(P3(-3.6, 1.15))
        self.ate(0.3)
        self.play(Create(ret), run_time=1.0)
        self.play(Write(fm), run_time=0.9)
        self.ate(0.52)
        self.play(Create(cB), run_time=0.9)
        self.add(aB)
        self.play(tB.animate.set_value(0.024), run_time=1.2, rate_func=linear)
        aB.clear_updaters()
        la = Mc((r"\text{ÁREA}=20{,}0\ \mathrm{N\cdot s}", JC), size=36).next_to(GA.pt(0.015, 0), DOWN, buff=0.45)
        lb = Mc((r"\text{ÁREA}=20{,}0\ \mathrm{N\cdot s}", JC), size=36).next_to(GB.pt(0.015, 0), DOWN, buff=0.45)
        self.play(FadeIn(la), FadeIn(lb), run_time=0.6)
        self.play(Indicate(la, color=WHITE_), Indicate(lb, color=WHITE_), run_time=0.9)
        so = legenda("SÓ A ÁREA IMPORTA", T_MAIN, color=JC).shift(DOWN * 0.35)
        self.ate(0.86)
        self.play(FadeIn(so, shift=0.1 * UP), run_time=0.6)
        self.ate(0.97)

    # ── T5-6 · CENTRO: o vetor J⃗ e a DICA ──────────────────────────────────────────────────────────────────
    def t5_6(self):
        self.an("T5-6")
        self.clear(rt=0.5)
        o, fim = P3(-3.2, -1.4), P3(2.6, 1.2)
        jv = arrow(o, fim, color=JC, width=10, tip=0.32)
        cx_ = DashedLine(o, P3(fim[0], o[1]), color=JC, stroke_width=3)
        cy_ = DashedLine(P3(fim[0], o[1]), fim, color=JC, stroke_width=3)
        lj = MathTex(r"\vec J=\int\vec F_{res}\,dt", font_size=50, color=JC).next_to((o + fim) / 2, UL, buff=0.25)
        jx = MathTex(r"J_x", font_size=42, color=JC).next_to(cx_, DOWN, buff=0.15)
        jy = MathTex(r"J_y", font_size=42, color=JC).next_to(cy_, RIGHT, buff=0.15)
        md = linha(txt("MESMA DIREÇÃO DE", T_SMALL, color=DIM), MathTex(r"\Delta\vec p", font_size=34, color=MAG), buff=0.15) \
            .move_to(P3(-1.2, 2.1))
        grupo = VGroup(jv, cx_, cy_, lj, jx, jy, md)
        grupo.shift(RIGHT * (-grupo.get_center()[0]))
        grupo.modo_centro = True
        self.play(GrowArrow(jv), run_time=0.8)
        self.play(Write(lj), FadeIn(md), run_time=0.8)
        self.play(Create(cx_), Create(cy_), FadeIn(jx), FadeIn(jy), run_time=0.8)
        d = dica("IMPULSO É VETOR:", "COMPONENTE POR COMPONENTE, COM SINAL")
        self.dica_entra(d)
        self.ate(0.96)
        self.clear(rt=0.5)
