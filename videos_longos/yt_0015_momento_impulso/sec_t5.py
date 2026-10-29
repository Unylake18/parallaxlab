"""Lote PD (v4): T5 — IMPULSO, construído do caso constante até as componentes. Força constante (bloco + relógio no PALCO; F×t
e p×t empilhados na CONTA) → triângulo de inclinação → ΣF⃗(t₂−t₁) = p⃗₂−p⃗₁ → J⃗ e unidades → a força da parede → Riemann com os
pedaços de Δp⃗ somando na seta da bola → a integral (dt cancela, limites viram p⃗₁, p⃗₂) → força média e mesma área → componentes."""
# v6: TransformByGlyphMap vem do kit (TrocaGlifos, sem morph)

from kit import *  # noqa: F401,F403
from sec_teoria import relogio

J_PAREDE, DT_PAREDE = 20.0, 0.010          # N·s ; s  (bola de 0,40 kg: 0,40·(20 − (−30)))
F_MED = J_PAREDE / DT_PAREDE               # 2000 N
P_I, P_F = -12.0, 8.0                      # kg·m/s (0,40·(−30) e 0,40·20)
KP = 0.15                                  # tela por kg·m/s
PAREDE_X = -5.9
RAIO_BOLA = 0.48
CONTATO_X = PAREDE_X + RAIO_BOLA
YB = 0.35
T1G, T2G, FN, P1G = 0.15, 0.85, 0.62, 0.18   # caso constante (unidades do gráfico)


def bola_x(tp, t0=DT_PAREDE, tau=DT_PAREDE):
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


def pinta(m, cores):
    for idx, c in cores:
        for i in idx:
            m[0][i].set_color(c)
    return m


def grupo(m, idx):
    return VGroup(*[m[0][i] for i in idx])


class LoteT5(Base):
    def construct(self):
        self.setup_base(cap="IMPULSO")
        self.t5_1()
        self.t5_2()
        self.t5_3()
        self.t5_4()
        self.t5_5()
        self.t5_6()
        self.t5_7()
        self.t5_8()
        self.fim()
        self.relatorio()

    # ── T5-1 · força constante: bloco + relógio (PALCO); F×t e p×t empilhados (CONTA), sincronizados ───────────────
    def t5_1(self):
        self.an("T5-1")
        yc = -0.55
        piso = Line(P3(-6.6, yc), P3(0.4, yc)).set_stroke(GEO, 2.5, opacity=0.6)
        hach = VGroup(*[Line(P3(x, yc), P3(x - 0.18, yc - 0.18)).set_stroke(GEO, 1.2, opacity=0.3) for x in np.arange(-6.4, 0.45, 0.35)])
        sem = txt("SEM ATRITO", 21, color=GEO).move_to(P3(-1.0, yc - 0.42))
        GF = Graf(1.6, 0.85, 4.3, 1.25, 1.0, 1.0, MathTex(r"\Sigma F", font_size=34, color=FC))
        Gp = Graf(1.6, -2.55, 4.3, 2.35, 1.0, 1.0, MathTex(r"p", font_size=38, color=MAG))
        tau = ValueTracker(0.0)
        pf = lambda t: P1G + (min(max(t, T1G), T2G) - T1G) * (FN / FN)      # inclinação = F (escalas casadas)

        def Pint(t):                                                          # ∫ p dt (posição do bloco)
            if t <= T1G:
                return P1G * t
            if t <= T2G:
                return P1G * T1G + P1G * (t - T1G) + 0.5 * (t - T1G) ** 2
            return P1G * T1G + P1G * (T2G - T1G) + 0.5 * (T2G - T1G) ** 2 + pf(T2G) * (t - T2G)
        blk = Corpo("m", STEEL, 1.1, 0.9, size=44)
        blk.add_updater(lambda m: m.move_to(P3(-5.6 + 3.2 * Pint(tau.get_value()), yc + 0.45)))

        def forca():
            t = tau.get_value()
            if not (T1G <= t <= T2G):
                return VGroup()
            c = blk.get_right() + P3(0, 0)
            return VGroup(arrow(c, c + P3(1.3, 0), color=FC, width=8, tip=0.26),
                          MathTex(r"\Sigma\vec F", font_size=36, color=FC).move_to(c + P3(0.65, 0.4)))
        fa = always_redraw(forca)

        def momento():
            c = blk.get_top() + P3(0, 0.35)
            L = 2.4 * pf(tau.get_value())
            return VGroup(arrow(c, c + P3(L, 0), color=MAG, width=9, tip=0.24),
                          MathTex(r"\vec p", font_size=38, color=MAG).next_to(c + P3(L / 2, 0), UP, buff=0.12))
        pm = always_redraw(momento)
        fr = ValueTracker(0.0)
        rel = relogio(P3(-1.7, 1.55), 0.55, fr)
        fr.add_updater(lambda m: m.set_value(min(max(tau.get_value() - T1G, 0), T2G - T1G) / (T2G - T1G) * 0.999))
        self.add(fr)
        lrel = MathTex(r"t_1\to t_2", font_size=34, color=JC).next_to(rel, LEFT, buff=0.25)

        def retF():
            t = tau.get_value()
            g = VGroup()
            if t > T1G:
                tf = min(t, T2G)
                g.add(Polygon(GF.pt(T1G, 0), GF.pt(T1G, FN), GF.pt(tf, FN), GF.pt(tf, 0)).set_stroke(width=0).set_fill(FC, 0.22))
            pts = [GF.pt(0, 0), GF.pt(T1G, 0)] + ([GF.pt(T1G, FN), GF.pt(min(t, T2G), FN)] if t > T1G else []) + \
                  ([GF.pt(T2G, 0), GF.pt(t, 0)] if t > T2G else [])
            pts = [p for p in pts if p[0] <= GF.pt(t, 0)[0] + 1e-6] or [GF.pt(0, 0)]
            g.add(VMobject().set_points_as_corners(pts if len(pts) > 1 else pts * 2).set_stroke(FC, 5))
            return g.set_z_index(6)

        def linP():
            t = max(tau.get_value(), 0.002)
            ts = np.linspace(0, t, 60)
            return VMobject().set_points_as_corners([Gp.pt(x, pf(x)) for x in ts]).set_stroke(MAG, 5).set_z_index(6)
        rF, lP = always_redraw(retF), always_redraw(linP)
        marcas = VGroup()
        for tt_, nm in ((T1G, "t_1"), (T2G, "t_2")):
            marcas.add(DashedLine(Gp.pt(tt_, 0), GF.pt(tt_, 1.0), dash_length=0.08).set_stroke(DIM, 1.3, opacity=0.6))
            marcas.add(MathTex(nm, font_size=30, color=DIM).next_to(Gp.pt(tt_, 0), DOWN, buff=0.12))
        self.GF, self.Gp = GF, Gp
        self.play(Create(piso), FadeIn(hach), FadeIn(sem), FadeIn(blk, shift=0.2 * RIGHT), run_time=0.8)
        self.add(fa, pm, rF, lP)
        self.play(Create(GF.eixos), Create(Gp.eixos), FadeIn(rel), FadeIn(lrel), FadeIn(marcas), tau.animate.set_value(0.11),
                  run_time=0.9, rate_func=linear)                       # v6: os eixos se desenham com o bloco já andando
        self.play(tau.animate.set_value(0.55), run_time=3.5, rate_func=linear)
        self.play(tau.animate(rate_func=linear).set_value(1.0), Indicate(rel, color=WHITE_, scale_factor=1.15),
                  Indicate(lrel, color=WHITE_, scale_factor=1.2), run_time=3.5)
        inc = MathTex(r"\text{inclina\c{c}\~ao}=\Sigma F", font_size=34, color=WHITE_)
        inc[0][-2:].set_color(FC)
        inc.next_to(Gp.pt(0.5, pf(0.5)), UL, buff=0.15)
        self.ate(0.7)
        self.play(FadeIn(inc, shift=0.1 * UP), Indicate(lP, color=WHITE_, scale_factor=1.0), run_time=0.8)
        self.ate(0.82)
        tau.set_value(0.0)
        self.play(tau.animate.set_value(1.0), run_time=0.17 * dur("T5-1") - 0.2, rate_func=linear)
        self.ate(0.97)
        for m in (rF, lP, blk, fr):
            m.clear_updaters()
        self.palco1 = VGroup(piso, hach, sem, blk, fa, pm, rel, lrel)
        self.graf1 = VGroup(GF.eixos, Gp.eixos, marcas, rF, lP, inc)
        self.tau = tau

    # ── T5-2 · triângulo de inclinação → ΣF⃗ = (p⃗₂ − p⃗₁)/(t₂ − t₁) → ΣF⃗ (t₂ − t₁) = p⃗₂ − p⃗₁ ────────────────────────
    def t5_2(self):
        self.an("T5-2")
        for m in self.palco1:
            m.clear_updaters()
        self.play(FadeOut(self.palco1), self.graf1.animate.shift(LEFT * 7.3), run_time=0.9)
        GF, Gp = self.GF, self.Gp
        for G in (GF, Gp):
            G.x0 -= 7.3
        a, b, c = Gp.pt(T1G, P1G), Gp.pt(T2G, P1G), Gp.pt(T2G, P1G + (T2G - T1G))
        tri = VGroup(Line(a, b).set_stroke(WHITE_, 3), Line(b, c).set_stroke(MAG, 4), Polygon(a, b, c).set_stroke(width=0).set_fill(WHITE_, 0.08))
        lh = MathTex(r"t_2-t_1", font_size=34, color=WHITE_).next_to(Line(a, b), DOWN, buff=0.12)
        lv = MathTex(r"\vec p_2-\vec p_1", font_size=34, color=MAG).next_to(Line(b, c), RIGHT, buff=0.12)
        self.play(Create(tri[0]), Create(tri[1]), FadeIn(tri[2]), run_time=0.9)
        self.play(FadeIn(lh), FadeIn(lv), run_time=0.5)
        c1 = MathTex(r"\Sigma\vec F=\frac{d\vec p}{dt}", font_size=M_MAIN)
        pinta(c1, [([0, 1, 2], FC), ([5, 6], MAG)])
        c2 = MathTex(r"\Sigma\vec F=\frac{\vec p_2-\vec p_1}{t_2-t_1}", font_size=M_MAIN)
        pinta(c2, [([0, 1, 2], FC), ([4, 5, 6, 8, 9, 10], MAG)])
        c3 = MathTex(r"\Sigma\vec F\,(t_2-t_1)=\vec p_2-\vec p_1", font_size=M_MID)
        pinta(c3, [([0, 1, 2], FC), ([11, 12, 13, 15, 16, 17], MAG)])
        conta(c1, topo=2.1)
        c2.move_to(c1, aligned_edge=LEFT)
        self.play(Write(c1), run_time=0.9)
        self.ate(0.28)
        self.play(*[ReplacementTransform(c1[0][i], c2[0][j]) for i, j in ((0, 0), (1, 1), (2, 2), (3, 3), (7, 11))],
                  *[FadeOut(c1[0][i]) for i in (4, 5, 6, 8, 9)], ReplacementTransform(fixa(lv), grupo(c2, range(4, 11))), run_time=0.9)
        self.play(ReplacementTransform(fixa(lh), grupo(c2, range(12, 17))), run_time=0.8)          # v6: um voo de cada vez
        self.remove(*c1[0])
        self.add(c2)
        self.ate(0.6)
        c3.next_to(c2, DOWN, buff=0.6).align_to(c2, LEFT)
        c2c = c2.copy()
        self.add(c2c)
        self.play(TransformByGlyphMap(c2c, c3, ([0, 1, 2], [0, 1, 2]), ([3], [10]), ([4, 5, 6, 7, 8, 9, 10], [11, 12, 13, 14, 15, 16, 17]),
                                      ([11], []), ([12, 13, 14, 15, 16], [4, 5, 6, 7, 8], {"path_arc": 2.2}), ([], [3, 9])), run_time=1.6)
        self.play(Indicate(grupo(c3, range(3, 10)), color=WHITE_, scale_factor=1.1), Indicate(lh, color=WHITE_), run_time=0.8)
        self.ate(0.97)
        self.c2, self.c3, self.tri, self.lh, self.lv = c2, c3, tri, lh, lv

    # ── T5-3 · J⃗ = ΣF⃗ Δt = p⃗₂ − p⃗₁ e a área do retângulo; unidades ──────────────────────────────────────────────────
    def t5_3(self):
        self.an("T5-3")
        GF = self.GF
        Jq = MathTex(r"\vec J=\Sigma\vec F\,\Delta t=\vec p_2-\vec p_1", font_size=M_MID)
        pinta(Jq, [([0, 1], JC), ([3, 4, 5], FC), ([9, 10, 11, 13, 14, 15], MAG)])
        Jq.move_to(self.c3, aligned_edge=LEFT)
        self.play(FadeOut(self.c2), self.c3.animate.align_to(P3(0, 2.1), UP), run_time=0.6)
        Jq.move_to(self.c3, aligned_edge=LEFT)
        c3c = self.c3.copy()
        self.play(TransformByGlyphMap(self.c3, Jq, ([], [0, 1, 2]), ([0, 1, 2], [3, 4, 5]), ([3, 4, 5, 6, 7, 8, 9], [6, 7]), ([10], [8]),
                                      ([11, 12, 13, 14, 15, 16, 17], [9, 10, 11, 12, 13, 14, 15])), run_time=1.4)
        bx = caixa(Jq, JC, buff=0.2)
        nm = txt("IMPULSO", T_LAB, color=JC, bold=True).next_to(bx, DOWN, buff=0.18).align_to(bx, LEFT)
        area = Polygon(GF.pt(T1G, 0), GF.pt(T1G, FN), GF.pt(T2G, FN), GF.pt(T2G, 0)).set_stroke(JC, 3).set_fill(JC, 0.55).set_z_index(7)
        jl = MathTex(r"\vec J", font_size=40, color=WHITE_).move_to(area).set_z_index(8)
        self.play(Create(bx), FadeIn(nm), FadeIn(area), run_time=0.8)
        self.play(ReplacementTransform(fixa(grupo(Jq, [0, 1])), jl), run_time=0.8)
        vet = txt("VETOR, NA DIREÇÃO DA FORÇA", T_SMALL, color=DIM).next_to(nm, RIGHT, buff=0.35)
        self.ate(0.3)
        self.play(FadeIn(vet), run_time=0.5)
        U = MathTex(r"\mathrm{N\cdot s}=(\mathrm{kg\cdot m/s^2})\cdot\mathrm{s}=\mathrm{kg\cdot m/s}", font_size=40)
        U.next_to(nm, DOWN, buff=0.55).align_to(bx, LEFT)
        if U.get_right()[0] > 6.6:
            U.scale_to_fit_width(6.6 - U.get_left()[0])
        self.ate(0.55)
        self.play(Write(grupo(U, range(0, 3))), run_time=0.6)
        self.ate(0.6)
        self.play(Write(grupo(U, range(3, 15))), run_time=1.2)
        cort = VGroup(*[Line(U[0][i].get_corner(DL) + P3(-0.03, -0.03), U[0][i].get_corner(UR) + P3(0.03, 0.03)).set_stroke(MAG, 3.5).set_z_index(20)
                        for i in (11, 14)])
        self.ate(0.72)
        self.play(Create(cort), run_time=0.7)
        self.ate(0.8)
        self.play(Write(grupo(U, range(15, 22))), run_time=0.9)
        mesma = txt("A MESMA UNIDADE DO MOMENTO", T_SMALL, color=MAG).next_to(U, DOWN, buff=0.3).align_to(U, LEFT)
        self.ate(0.9)
        self.play(FadeIn(mesma), Indicate(grupo(U, range(15, 22)), color=MAG, scale_factor=1.08), run_time=0.8)
        self.ate(0.97)

    # ── T5-4 · a força da parede: PALCO parede + bola; CONTA gráfico F_x(t) (eixos completos, rótulo opaco) ─────────────
    def t5_4(self):
        self.clear(rt=0.5)
        self.an("T5-4")
        self.parede = Rectangle(width=0.6, height=3.4).set_stroke(GEO, 2.5).set_fill(STEEL, 1).move_to(P3(PAREDE_X - 0.3, YB + 1.2 - 0.48))
        self.chao = Line(P3(-6.6, YB - RAIO_BOLA), P3(0.6, YB - RAIO_BOLA)).set_stroke(GEO, 2.5, opacity=0.6)
        self.G = G = Graf(1.45, 0.05, 4.9, 2.3, 0.030, 7000, MathTex(r"F_x", font_size=40, color=FC))
        lab = txt("FORÇA DA PAREDE", T_SMALL, color=WHITE_, bold=True).next_to(G.ey, RIGHT, buff=0.3)
        tp = ValueTracker(0.0)
        self.fun = fun = meia_senoide(J_PAREDE, DT_PAREDE, DT_PAREDE)
        b = bola(RAIO_BOLA)
        b.add_updater(lambda m: m.become(bola(RAIO_BOLA).stretch(squash(tp.get_value()), 0).move_to(P3(bola_x(tp.get_value()), YB))))
        curva = always_redraw(lambda: G.curva(fun, 0.0, max(tp.get_value(), 1e-4), n=int(40 + 600 * tp.get_value())))
        marca = always_redraw(lambda: Dot(G.pt(tp.get_value(), fun(tp.get_value())), radius=0.08, color=WHITE_).set_z_index(9))
        vel = always_redraw(lambda: arrow(P3(bola_x(tp.get_value()), YB + 0.95),
                                          P3(bola_x(tp.get_value()) + (-1.6 if tp.get_value() < DT_PAREDE else 1.05), YB + 0.95), color=VEL, width=6)
                            if not (DT_PAREDE <= tp.get_value() <= 2 * DT_PAREDE) else VMobject())
        cs = txt("CENTÉSIMOS DE SEGUNDO", T_SMALL, color=GEO).next_to(G.pt(0.015, 0), DOWN, buff=0.45)
        self.play(FadeIn(self.parede, shift=0.2 * RIGHT), Create(self.chao), FadeIn(b), Create(G.eixos), run_time=0.9)
        self.play(FadeIn(lab), run_time=0.5)
        self.add(curva, marca, vel)
        self.ate(0.12)
        self.play(tp.animate.set_value(0.030), run_time=0.6 * dur("T5-4"), rate_func=linear)
        self.play(FadeIn(cs), run_time=0.5)
        for m in (b, curva, marca, vel):
            m.clear_updaters()
        self.remove(marca, vel, curva)
        self.curva = G.curva(fun, 0.0, 0.030, n=500)
        self.add(self.curva)
        b.move_to(P3(CONTATO_X + 0.02, YB))
        self.bola_ = b
        self.play(Indicate(self.curva, color=WHITE_, scale_factor=1.0), run_time=0.8)
        self.ate(0.97)
        self.lab_f, self.cs = lab, cs

    # ── T5-5 · Riemann 4 → 8 → 32; cada retângulo é um pedaço de Δp⃗ somado na seta da bola ───────────────────────────
    def retangulos(self, n):
        G, f = self.G, self.fun
        a, b = DT_PAREDE, 2 * DT_PAREDE
        dx = (b - a) / n
        g, areas = VGroup(), []
        for k in range(n):
            t0 = a + k * dx
            h = f(t0 + dx / 2)
            areas.append(h * dx)
            r = Rectangle(width=G.w * dx / G.tmax, height=max(G.h * h / G.fmax, 0.001))
            r.move_to((G.pt(t0, 0) + G.pt(t0 + dx, h)) / 2).set_stroke(FC, 1.5 if n < 32 else 0.8).set_fill(JC, 0.5).set_z_index(4)
            g.add(r)
        return g, areas

    def pedacos(self, areas, y, x0):
        """Δp⃗ como soma de pedaços (um por retângulo), cabeça com cauda a partir da ponta de p⃗ᵢ."""
        g = VGroup()
        x = x0
        for k, a in enumerate(areas):
            L = KP * a
            g.add(Rectangle(width=max(L, 0.004), height=0.2).set_stroke(BACKGROUND_COLOR, 1).set_fill(JC if k % 2 else mix(JC, 0.45), 1)
                  .move_to(P3(x + L / 2, y)))
            x += L
        return g.set_z_index(7)

    def t5_5(self):
        self.an("T5-5")
        G = self.G
        self.play(FadeOut(self.cs), run_time=0.3)
        # diagrama de momento sob o chão: p⃗ᵢ e os pedaços de Δp⃗; p⃗_f embaixo
        ox, y1, y2 = -2.6, -1.35, -2.25
        pi_ = arrow(P3(ox, y1), P3(ox + KP * P_I, y1), color=MAG, width=8, tip=0.22)
        lpi = MathTex(r"\vec p_i", font_size=34, color=MAG).next_to(pi_, UP, buff=0.08)
        self.play(GrowArrow(pi_), FadeIn(lpi), run_time=0.7)
        cont = VGroup(txt("RETÂNGULOS", T_SMALL, color=GEO), Integer(4, font_size=38, color=WHITE_)).arrange(RIGHT, buff=0.15)
        cont.move_to(G.pt(0.0245, 6200))
        sig = MathTex(r"\sum_k\vec F_k\,\Delta t_k", font_size=56)
        pinta(sig, [([2, 3, 4], FC)])
        conta(sig, topo=-0.6, x0=2.2)
        ret, ar = self.retangulos(4)
        pd = self.pedacos(ar, y1 - 0.42, ox + KP * P_I)
        lpd = MathTex(r"\Delta\vec p", font_size=34, color=JC).next_to(pd, DOWN, buff=0.1)
        self.ate(0.12)
        self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in ret], lag_ratio=0.2), FadeIn(cont), run_time=1.2)
        self.play(LaggedStart(*[TransformFromCopy(r, p) for r, p in zip(ret, pd)], lag_ratio=0.25), run_time=1.6)
        self.play(FadeIn(lpd), Write(sig), run_time=0.9)
        somas = [sum(ar)]
        for n, fr in ((8, 0.5), (32, 0.7)):
            self.ate(fr)
            novo, ar = self.retangulos(n)
            npd = self.pedacos(ar, y1 - 0.42, ox + KP * P_I)
            somas.append(sum(ar))
            self.play(ReplacementTransform(ret, novo), ReplacementTransform(pd, npd), cont[1].animate.set_value(n), run_time=1.0)
            ret, pd = novo, npd
        print("[QA] T5-5 somas de Riemann (4, 8, 32):", ", ".join(f"{s:.3f}" for s in somas), "N·s (alvo 20)")
        cola = legenda("QUANTO MAIS FINO, MAIS COLA NA CURVA", T_SMALL)
        self.play(FadeIn(cola), run_time=0.5)
        self.ate(0.97)
        self.ret, self.sig, self.cont, self.pd, self.lpd, self.cola_ = ret, sig, cont, pd, lpd, cola
        self.pi_, self.lpi, self.ox, self.y1, self.y2 = pi_, lpi, ox, y1, y2

    # ── T5-6 · Σ → ∫; ∫(dp⃗/dt)dt = ∫dp⃗: o dt cancela e os limites viram p⃗₁, p⃗₂; a área enche e a seta acompanha ───────────
    def t5_6(self):
        self.an("T5-6")
        G = self.G
        I1 = MathTex(r"\vec J=\int_{t_1}^{t_2}\Sigma\vec F\,dt", font_size=44)
        pinta(I1, [([0, 1], JC), ([8, 9, 10], FC)])
        I1.move_to(self.sig, aligned_edge=LEFT).align_to(P3(1.3, 0), LEFT).align_to(P3(0, -0.6), UP)   # v6: caixa a ≥ 0,25 do eixo t
        self.play(FadeOut(self.cola_), FadeOut(self.cont), run_time=0.4)
        area = G.area(self.fun, DT_PAREDE, 2 * DT_PAREDE)
        self.play(ReplacementTransform(grupo(self.sig, [0, 1]), grupo(I1, range(3, 8))), ReplacementTransform(grupo(self.sig, [2, 3, 4]), grupo(I1, [8, 9, 10])),
                  ReplacementTransform(grupo(self.sig, [5, 6, 7]), grupo(I1, [11, 12])), FadeIn(grupo(I1, [0, 1, 2])),
                  FadeTransform(self.ret, area), run_time=1.3)
        self.remove(*self.sig[0])
        self.add(I1)
        lim = MathTex(r"\Delta t_k\to 0", font_size=40, color=GEO).next_to(I1, RIGHT, buff=0.35)
        self.play(FadeIn(lim), run_time=0.4)
        # a área se refaz da esquerda para a direita e a seta p⃗ da bola acompanha (p⃗ = p⃗ᵢ + área até t)
        ta = ValueTracker(DT_PAREDE + 1e-5)
        self.remove(area)
        ar_ = always_redraw(lambda: G.area(self.fun, DT_PAREDE, ta.get_value()))
        self.add(ar_)
        self.remove(self.pd, self.lpd)

        def pseta():
            J = area_num(self.fun, DT_PAREDE, ta.get_value(), n=200)
            p = P_I + J
            o = P3(self.ox, self.y2)
            return VGroup(arrow(o, o + P3(KP * p, 0), color=MAG, width=8, tip=0.22),
                          MathTex(r"\vec p", font_size=34, color=MAG).next_to(o + P3(KP * p / 2, 0), DOWN, buff=0.1))
        ps = always_redraw(pseta)
        self.add(ps)
        I2 = MathTex(r"=\int_{t_1}^{t_2}\frac{d\vec p}{dt}\,dt", font_size=44)
        pinta(I2, [([7, 8], MAG)])
        I2.next_to(I1, DOWN, buff=0.22).align_to(grupo(I1, [2]), LEFT)
        self.ate(0.22)
        self.play(FadeOut(lim), Write(I2), ta.animate.set_value(1.5 * DT_PAREDE), run_time=1.5)
        I3 = MathTex(r"=\int_{\vec p_1}^{\vec p_2}d\vec p", font_size=44)
        pinta(I3, [([2, 3, 4, 5, 6, 7], MAG), ([9, 10], MAG)])
        I3.move_to(I2, aligned_edge=LEFT)
        cortes = VGroup(*[Line(grupo(I2, par).get_corner(DL) + P3(-0.04, -0.04), grupo(I2, par).get_corner(UR) + P3(0.04, 0.04))
                          .set_stroke(MAG, 4).set_z_index(20) for par in ((10, 11), (12, 13))])
        self.ate(0.42)
        self.play(Create(cortes), run_time=0.6)
        self.play(TransformByGlyphMap(I2, I3, ([0, 1], [0, 1]), ([2, 3], [2, 3, 4], {"path_arc": 0.6}), ([4, 5], [5, 6, 7], {"path_arc": -0.6}),
                                      ([6, 7, 8], [8, 9, 10]), ([9, 10, 11, 12, 13], [], {"shift": 0.5 * DOWN})),
                  FadeOut(cortes, shift=0.5 * DOWN), ta.animate.set_value(1.75 * DT_PAREDE), run_time=1.5)
        trocam = txt("OS LIMITES VIRAM MOMENTOS", T_SMALL, color=MAG).next_to(I3, DOWN, buff=0.12).align_to(I3, LEFT)
        self.play(FadeIn(trocam), Indicate(grupo(I3, range(2, 8)), color=WHITE_, scale_factor=1.15), run_time=0.9)
        I4 = MathTex(r"=\vec p_2-\vec p_1", font_size=44)
        pinta(I4, [([1, 2, 3, 5, 6, 7], MAG)])
        I4.move_to(I3, aligned_edge=LEFT)
        self.ate(0.66)
        self.play(FadeOut(trocam), TransformByGlyphMap(I3, I4, ([0], [0]), ([1, 8, 9, 10], []), ([2, 3, 4], [1, 2, 3]), ([5, 6, 7], [5, 6, 7]), ([], [4])),
                  ta.animate.set_value(2 * DT_PAREDE - 1e-5), run_time=1.4)
        ta.set_value(2 * DT_PAREDE)
        bx = caixa(VGroup(I1, I4), JC, buff=0.2)
        teo = legenda("O IMPULSO DA FORÇA RESULTANTE É A VARIAÇÃO DO MOMENTO", T_LAB, color=JC)
        lpf = MathTex(r"\vec p_f", font_size=34, color=MAG).next_to(P3(self.ox + KP * P_F, self.y2), RIGHT, buff=0.12)
        self.ate(0.82)
        self.play(Create(bx), FadeIn(teo), FadeIn(lpf), run_time=0.8)
        self.ate(0.97)
        ar_.clear_updaters()
        ps.clear_updaters()
        self.I = VGroup(I1, I4, bx)
        self.teo, self.ps, self.ar_, self.lpf = teo, ps, ar_, lpf

    # ── T5-7 · força média: mesma base, mesma área; duas formas com a mesma área ─────────────────────────────────────
    def t5_7(self):
        self.an("T5-7")
        G = self.G
        self.play(FadeOut(self.bola_), run_time=0.4)                     # v6: a bola sai antes da troca
        self.play(*[FadeOut(m) for m in (self.parede, self.chao, self.pi_, self.lpi, self.ps, self.lpf, self.teo, self.I)],
                  VGroup(G.eixos, self.curva, self.ar_, self.lab_f).animate.shift(LEFT * 7.3), run_time=0.9)
        G.x0 -= 7.3
        M = MathTex(r"\vec J=\int\Sigma\vec F\,dt=\vec F_{\mathrm{m\acute{e}d}}\,(t_2-t_1)", font_size=48)
        pinta(M, [([0, 1], JC), ([4, 5, 6], FC), ([10, 11, 12, 13, 14, 15], FC)])
        conta(M, topo=2.15)
        ret = G.retangulo(DT_PAREDE, 2 * DT_PAREDE, F_MED)
        rf = Rectangle(width=G.w * DT_PAREDE / G.tmax, height=G.h * F_MED / G.fmax).set_stroke(width=0).set_fill(FC, 0.18) \
            .move_to((G.pt(DT_PAREDE, 0) + G.pt(2 * DT_PAREDE, F_MED)) / 2).set_z_index(2)
        # v6: F_méd fora do retângulo, à direita, com linha guia
        pr = G.pt(2 * DT_PAREDE, F_MED * 0.55)
        fm = MathTex(r"F_{\mathrm{m\acute{e}d}}", font_size=40, color=FC).move_to(pr + P3(1.15, 0))
        guia = Line(pr + P3(0.06, 0), fm.get_left() + P3(-0.1, 0)).set_stroke(FC, 1.6, opacity=0.8)
        self.play(Write(M), run_time=1.3)
        self.ate(0.28)
        self.play(Create(ret), FadeIn(rf), FadeIn(fm), Create(guia), run_time=1.0)
        mb = txt("MESMA BASE, MESMA ÁREA", T_SMALL, color=GEO).next_to(G.pt(0.015, 0), DOWN, buff=0.45)
        self.play(FadeIn(mb), Indicate(fm, color=WHITE_, scale_factor=1.3), run_time=0.8)
        # segunda forma, mesma área, na CONTA embaixo
        GB = Graf(1.5, -2.6, 4.6, 2.2, 0.030, 7000, MathTex(r"F_x", font_size=34, color=FC))
        fB = triangulo(J_PAREDE, 0.006, 0.009, 0.024)
        cB = GB.curva(fB, 0, 0.030, n=500)
        tB = ValueTracker(0.006 + 1e-4)
        aB = always_redraw(lambda: GB.area(fB, 0.006, tB.get_value()))
        A1, A2 = area_num(self.fun, 0, 0.030), area_num(fB, 0, 0.030)
        print(f"[QA] T5-7 áreas: meia-senoide {A1:.4f} N·s, triângulo {A2:.4f} N·s, retângulo da média {F_MED * DT_PAREDE:.4f} N·s (alvo 20)")
        self.ate(0.55)
        self.play(Create(GB.eixos), run_time=0.6)
        self.play(Create(cB), run_time=0.8)
        self.add(aB)
        self.play(tB.animate.set_value(0.024), run_time=1.1, rate_func=linear)
        aB.clear_updaters()
        la = MathTex(r"\text{\'AREA}=20{,}0\ \mathrm{N\cdot s}", font_size=34, color=JC).move_to(G.pt(0.024, 5200))
        lb = MathTex(r"\text{\'AREA}=20{,}0\ \mathrm{N\cdot s}", font_size=34, color=JC).move_to(GB.pt(0.0215, 5000))
        self.play(FadeIn(la), FadeIn(lb), run_time=0.6)
        so = legenda("SÓ A ÁREA IMPORTA", T_MAIN, color=JC)
        self.ate(0.84)
        self.play(FadeIn(so, shift=0.1 * UP), Indicate(la, color=WHITE_), Indicate(lb, color=WHITE_), run_time=0.9)
        self.ate(0.97)
        self.clear(rt=0.5)

    # ── T5-8 · componentes: p⃗₁, p⃗₂ e Δp⃗ no plano xy; Jx e Jy na CONTA, cada termo com a sua projeção ──────────────────
    def t5_8(self):
        self.an("T5-8")
        O = P3(-3.3, -1.6)
        u = 1.05
        p1, p2 = np.array([-1.7, 0.9]), np.array([1.6, 2.0])
        pt = lambda v: O + u * P3(v[0], v[1])
        ex = arrow(pt((-2.9, 0)), pt((2.9, 0)), color=GEO, width=3, tip=0.16)
        ey = arrow(pt((0, -0.9)), pt((0, 3.1)), color=GEO, width=3, tip=0.16)
        lx = MathTex("x", font_size=34, color=GEO).next_to(ex.get_end(), DOWN, buff=0.1)
        ly = MathTex("y", font_size=34, color=GEO).next_to(ey.get_end(), LEFT, buff=0.1)
        a1 = arrow(pt((0, 0)), pt(p1), color=MAG, width=8, tip=0.22)
        a2 = arrow(pt((0, 0)), pt(p2), color=MAG, width=8, tip=0.22)
        dp = arrow(pt(p1), pt(p2), color=JC, width=8, tip=0.22)
        l1 = MathTex(r"\vec p_1", font_size=36, color=MAG).next_to(pt(p1), UL, buff=0.06)
        l2 = MathTex(r"\vec p_2", font_size=36, color=MAG).next_to(pt(p2), UR, buff=0.06)
        ld = MathTex(r"\Delta\vec p=\vec J", font_size=38, color=JC).move_to(pt((p1 + p2) / 2) + P3(-1.35, 0.68))    # fora do triângulo, longe do J_y (v6.1)
        self.play(GrowArrow(ex), GrowArrow(ey), FadeIn(lx), FadeIn(ly), run_time=0.8)
        self.play(FadeIn(a1), FadeIn(a2), FadeIn(l1), FadeIn(l2), run_time=0.8)
        self.play(FadeIn(dp), FadeIn(ld), run_time=0.7)
        tr = lambda a, b: DashedLine(pt(a), pt(b), dash_length=0.07).set_stroke(DIM, 1.5, opacity=0.8)
        proj = VGroup(tr(p1, (p1[0], 0)), tr(p2, (p2[0], 0)), tr(p1, (0, p1[1])), tr(p2, (0, p2[1])))
        jx = DashedLine(pt((p1[0], 0)), pt((p2[0], 0)), dash_length=0.12).set_stroke(JC, 8).set_z_index(4)      # projeções de Δp⃗ = J⃗ nos eixos
        jy = DashedLine(pt((0, p1[1])), pt((0, p2[1])), dash_length=0.12).set_stroke(JC, 8).set_z_index(4)
        ljx = MathTex("J_x", font_size=38, color=JC).next_to(jx, DOWN, buff=0.12)
        ljy = MathTex("J_y", font_size=38, color=JC).next_to(jy.get_end(), LEFT, buff=0.12)
        self.play(Create(proj), run_time=0.8)
        rows = [MathTex(r"J_x=\int\Sigma F_x\,dt", font_size=44), MathTex(r"=(F_{\mathrm{m\acute{e}d}})_x\,\Delta t", font_size=44),
                MathTex(r"=m\,v_{2x}-m\,v_{1x}", font_size=44),
                MathTex(r"J_y=\int\Sigma F_y\,dt=(F_{\mathrm{m\acute{e}d}})_y\,\Delta t", font_size=40), MathTex(r"=m\,v_{2y}-m\,v_{1y}", font_size=40)]
        cor = [[([0, 1], JC), ([4, 5, 6], FC)], [([1, 2, 3, 4, 5, 6, 7, 8], FC)], [([2, 3, 4, 7, 8, 9], VEL)],
               [([0, 1], JC), ([4, 5, 6], FC), ([10, 11, 12, 13, 14, 15, 16, 17], FC)], [([2, 3, 4, 7, 8, 9], VEL)]]
        for r, c in zip(rows, cor):
            pinta(r, c)
        conta(*rows, topo=2.2, buff=0.24)
        for k in (1, 2):
            rows[k].shift(RIGHT * (rows[0][0][2].get_left()[0] - rows[k][0][0].get_left()[0]))
        rows[3].shift(DOWN * 0.3)
        rows[4].shift(DOWN * 0.3 + RIGHT * (rows[3][0][2].get_left()[0] - rows[4][0][0].get_left()[0]))
        self.ate(0.18)
        self.play(Create(jx), ReplacementTransform(fixa(ld).set_color(JC), ljx), Write(rows[0]), run_time=1.0)
        self.ate(0.3)
        self.play(Write(rows[1]), Indicate(jx, color=WHITE_), Indicate(dp, color=WHITE_, scale_factor=1.05), run_time=0.9)
        self.ate(0.42)
        self.play(Write(rows[2]), Indicate(VGroup(proj[0], proj[1]), color=WHITE_), Indicate(a1, color=WHITE_, scale_factor=1.08),
                  Indicate(a2, color=WHITE_, scale_factor=1.08), run_time=1.0)
        self.ate(0.6)
        self.play(Create(jy), FadeIn(ljy), Write(rows[3]), run_time=1.1)
        self.play(Write(rows[4]), Indicate(VGroup(proj[2], proj[3]), color=WHITE_), run_time=0.9)
        z = legenda("E O MESMO EM z", T_LAB, color=WHITE_)
        self.ate(0.8)
        self.play(FadeIn(z), run_time=0.5)
        self.ate(0.97)
        # T5-9 — DICA com o diagrama ainda no PALCO
        self.an("T5-9")
        self.play(FadeOut(z), run_time=0.3)
        d = dica("IMPULSO É VETOR:", "COMPONENTE POR COMPONENTE, COM SINAL")
        self.dica_entra(d)
        self.play(Indicate(VGroup(jx, jy), color=WHITE_, scale_factor=1.05), run_time=0.9)
        self.ate(0.96)
        self.clear(rt=0.5)
