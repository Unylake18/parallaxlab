"""Lote A: C01-6, C01-7 (2D), C02 e C03."""
from kit import *  # noqa: F401,F403

J_PAREDE, DT_PAREDE = 20.0, 0.010          # N·s ; s  (bola de 0,40 kg: 0,40·(20 − (−30)))
F_MED = J_PAREDE / DT_PAREDE               # 2000 N
PAREDE_X = -5.7                            # face da parede (u)
RAIO_BOLA = 0.3
CONTATO_X = PAREDE_X + RAIO_BOLA


def bola_x(tp, t0=DT_PAREDE, tau=DT_PAREDE):
    """Centro da bola (u) no tempo físico tp (s): chega a 270 u/s, fica comprimida durante o contato, sai a 180 u/s."""
    if tp < t0:
        return CONTATO_X + 270.0 * (t0 - tp)
    if tp <= t0 + tau:
        return CONTATO_X
    return CONTATO_X + 180.0 * (tp - t0 - tau)


def squash(tp, t0=DT_PAREDE, tau=DT_PAREDE):
    if t0 <= tp <= t0 + tau:
        return 1.0 - 0.28 * math.sin(math.pi * (tp - t0) / tau)
    return 1.0


class LoteA(Base):
    def construct(self):
        self.setup_base(cap="POR QUE MASSA VEZES VELOCIDADE?")
        self.c01_final()
        self.c02()
        self.c03()
        self.fim()
        self.relatorio()

    # ── C01-6 e C01-7 (Manim 2D puro) ───────────────────────────────────────────────────────────────────────
    def caso(self, y, m1, m2, v1, v2, tex):
        """Um caso rápido: ANTES (setas violeta) → DEPOIS (grudados, parados) e a soma m·v dos dois estados."""
        c1 = Corpo(f"{m1}m" if m1 != 1 else "m", GEO, 0.45 + 0.28 * m1, size=30).at(-5.9, y)
        c2 = Corpo(f"{m2}m", STEEL, 0.45 + 0.28 * m2, size=30).at(-3.3, y)
        a1 = arrow(P3(-5.9, y + c1.alt + 0.28), P3(-5.9 + 0.55 * v1, y + c1.alt + 0.28), color=VEL, width=5)
        a2 = arrow(P3(-3.3, y + c2.alt + 0.28), P3(-3.3 - 0.55 * v2, y + c2.alt + 0.28), color=VEL, width=5)
        eq = MathTex(*tex, font_size=44, color=MAG).move_to(P3(3.4, y + 0.35))
        pista = Line(P3(-7.0, y), P3(-1.8, y)).set_stroke(GEO, 2, opacity=0.5)
        return c1, c2, a1, a2, eq, pista

    def c01_final(self):
        self.an("C01-6")
        linhas = []
        for y, args in ((1.0, (1, 2, 2.0, 1.0, [r"m\cdot 2v", r"+\,2m\cdot(-v)", r"=0"])),
                        (-1.7, (2, 3, 3.0, 2.0, [r"2m\cdot 3v", r"+\,3m\cdot(-2v)", r"=0"]))):
            c1, c2, a1, a2, eq, pista = self.caso(y, *args)
            linhas.append((c1, c2, a1, a2, eq, pista))
            self.play(FadeIn(pista), FadeIn(c1), FadeIn(c2), FadeIn(a1), FadeIn(a2), run_time=0.7)
            self.play(FadeIn(eq, shift=0.1 * UP), run_time=0.6)
            self.ate(0.45 if y > 0 else 0.95)
        lab = txt("SOMA DE MASSA VEZES VELOCIDADE: ANTES = DEPOIS", T_SMALL, color=DIM).move_to(P3(0, -3.4))
        self.play(FadeIn(lab), run_time=0.5)
        self.an("C01-7")
        self.clear(rt=0.6)
        mv = Mc(("m", WHITE_), ("v", VEL), size=120).move_to(P3(0, 0.3))
        mv[1].set_color(VEL)
        mvm = Mc(("m", WHITE_), (r"\vec v", VEL), size=120)
        mvm.set_color(MAG)
        mvm.move_to(P3(0, 0.3))
        caixa = SurroundingRectangle(mvm, color=MAG, buff=0.35, stroke_width=3, corner_radius=0.1)
        self.play(FadeIn(mvm, scale=0.9), Create(caixa), run_time=1.0)
        self.ate(0.35)
        so_v = MathTex("v", font_size=70, color=APAGADO).move_to(P3(-4.6, 0.3))
        mv2 = MathTex(r"m\,v^2", font_size=70, color=APAGADO).move_to(P3(4.6, 0.3))
        self.play(FadeIn(so_v), FadeIn(mv2), run_time=0.6)
        self.play(Create(risco(so_v, w=5)), Create(risco(mv2, w=5)), run_time=0.7)
        n1 = txt("NÃO É ESSA", T_SMALL, color=APAGADO).next_to(so_v, DOWN, buff=0.35)
        n2 = txt("NEM ESSA", T_SMALL, color=APAGADO).next_to(mv2, DOWN, buff=0.35)
        gr = txt("A GRANDEZA QUE SE CONSERVA", T_MAIN, color=MAG).next_to(caixa, DOWN, buff=0.5)
        self.play(FadeIn(n1), FadeIn(n2), FadeIn(gr), run_time=0.6)
        self.ate(0.97)

    # ── C02 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def c02(self):
        self.clear(rt=0.6)
        self.secao("MOMENTO LINEAR")
        self.an("C02-1")
        blk = Corpo("m", STEEL, 1.1, size=44).at(-3.6, -0.2)
        trilho = Line(P3(-7.0, -0.2), P3(0.2, -0.2)).set_stroke(GEO, 2, opacity=0.5)
        v = arrow(P3(-3.6, 1.3), P3(-1.4, 1.3), color=VEL, width=8, tip=0.26)
        vl = MathTex(r"\vec v", font_size=48, color=VEL).next_to(v, UP, buff=0.12)
        p = arrow(P3(-3.6, -1.35), P3(-1.4, -1.35), color=MAG, width=8, tip=0.26)
        pl = MathTex(r"\vec p", font_size=48, color=MAG).next_to(p, DOWN, buff=0.12)
        self.play(FadeIn(trilho), FadeIn(blk), run_time=0.6)
        self.play(GrowArrow(v), FadeIn(vl), run_time=0.8)
        self.ate(0.4)
        self.play(GrowArrow(p), FadeIn(pl), run_time=0.8)
        eq = Mc((r"\vec p", MAG), "=", "m", (r"\vec v", VEL), size=M_MAIN).move_to(P3(4.3, 0.6))
        self.ate(0.6)
        self.play(FadeIn(eq, shift=0.1 * UP), run_time=0.7)
        self.ate(0.97)
        self.an("C02-2")
        un = MathTex(r"\mathrm{kg\cdot m/s}", "=", r"\mathrm{N\cdot s}", font_size=M_MID).move_to(P3(4.3, -1.0))
        un[0].set_color(MAG)
        un[2].set_color(JC)
        self.play(FadeIn(un, shift=0.1 * UP), run_time=0.8)
        self.ate(0.97)
        self.an("C02-3")
        self.play(FadeOut(un), FadeOut(eq), run_time=0.4)
        e1 = Mc((r"\vec F_{res}", FC), "=", (r"\frac{d\vec p}{dt}", MAG), size=M_MAIN).move_to(P3(4.3, 1.0))
        e2 = Mc("=", "m", (r"\vec a", WHITE_), size=M_MAIN).next_to(e1, DOWN, buff=0.45, aligned_edge=LEFT)
        e2n = linha(txt("COM", T_SMALL, DIM), MathTex("m", font_size=30, color=DIM), txt("CONSTANTE", T_SMALL, DIM), buff=0.12).next_to(e2, RIGHT, buff=0.3)
        self.play(FadeIn(e1, shift=0.1 * UP), run_time=0.8)
        self.ate(0.6)
        self.play(FadeIn(e2), FadeIn(e2n), run_time=0.8)
        self.ate(0.97)

    # ── C03 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def c03(self):
        self.clear(rt=0.6)
        self.secao("IMPULSO")
        self.an("C03-1")
        yb = -0.6                                    # linha da bola e da parede
        parede = Rectangle(width=0.5, height=2.2).set_stroke(GEO, 2).set_fill(STEEL, 0.45).move_to(P3(PAREDE_X - 0.25, yb + 0.5))
        chao = Line(P3(-7.2, yb - RAIO_BOLA), P3(-0.9, yb - RAIO_BOLA)).set_stroke(GEO, 2, opacity=0.5)
        gx0, gy0, gw, gh = 0.55, -2.3, 6.2, 4.6
        self.G = G = Graf(gx0, gy0, gw, gh, 0.030, 7000, MathTex(r"F_x", font_size=40, color=FC))
        lab = txt("FORÇA DA PAREDE", T_SMALL, color=FC).next_to(G.ey, RIGHT, buff=0.3)
        tp = ValueTracker(0.0)
        fun = meia_senoide(J_PAREDE, DT_PAREDE, DT_PAREDE)
        b = bola(RAIO_BOLA)
        b.add_updater(lambda m: m.become(bola(RAIO_BOLA).stretch(squash(tp.get_value()), 0).move_to(P3(bola_x(tp.get_value()), yb))))
        curva = always_redraw(lambda: G.curva(fun, 0.0, max(tp.get_value(), 1e-4), n=int(40 + 600 * tp.get_value())))
        marca = always_redraw(lambda: Dot(G.pt(tp.get_value(), fun(tp.get_value())), radius=0.07, color=WHITE_).set_z_index(9))
        vel = always_redraw(lambda: arrow(P3(bola_x(tp.get_value()), yb + 0.6), P3(bola_x(tp.get_value()) + (-1.3 if tp.get_value() < DT_PAREDE else (0 if tp.get_value() <= 2 * DT_PAREDE else 0.9)), yb + 0.6),
                                           color=VEL, width=5) if (tp.get_value() < DT_PAREDE or tp.get_value() > 2 * DT_PAREDE) else VMobject())
        self.play(FadeIn(parede), FadeIn(chao), FadeIn(b), FadeIn(G.eixos), FadeIn(lab), run_time=1.0)
        self.add(curva, marca, vel)
        self.ate(0.2)
        self.play(tp.animate.set_value(0.030), run_time=10.0, rate_func=linear)
        self.ate(0.97)
        # C03-2 ----------------------------------------------------------------------------------------------
        self.an("C03-2")
        marca.clear_updaters()
        self.remove(marca, vel)
        curva.clear_updaters()
        area = G.area(fun, DT_PAREDE, 2 * DT_PAREDE)
        self.play(FadeIn(area), run_time=1.0)
        teo = Mc((r"\vec J", JC), "=", (r"\int \vec F_{res}\,dt", FC), "=", (r"\Delta\vec p", MAG), size=M_MID).move_to(P3(-2.7, -3.2))
        self.ate(0.45)
        self.play(FadeIn(teo, shift=0.1 * UP), run_time=0.9)
        self.ate(0.97)
        # C03-3 ----------------------------------------------------------------------------------------------
        self.an("C03-3")
        ret = G.retangulo(DT_PAREDE, 2 * DT_PAREDE, F_MED)
        fm = Mc((r"F_{\mathrm{m\acute{e}d}}", FC), "=", (r"\frac{J}{\Delta t}", JC), size=M_MID).move_to(P3(-2.7, -3.2))
        dt_ = MathTex(r"\Delta t", font_size=38, color=DIM).next_to(G.pt(1.5 * DT_PAREDE, 0), DOWN, buff=0.12)
        self.play(Create(ret), run_time=1.2)
        self.play(FadeOut(teo), FadeIn(fm, shift=0.1 * UP), FadeIn(dt_), run_time=0.8)
        self.ate(0.97)
        # C03-4 ----------------------------------------------------------------------------------------------
        self.an("C03-4")
        self.play(FadeOut(curva), FadeOut(area), FadeOut(ret), run_time=0.4)
        tau = ValueTracker(DT_PAREDE)
        f_ = lambda t: meia_senoide(J_PAREDE, tau.get_value(), DT_PAREDE)(t)
        c4 = always_redraw(lambda: G.curva(f_, 0.0, 0.030, n=400))
        a4 = always_redraw(lambda: G.area(f_, DT_PAREDE, DT_PAREDE + tau.get_value(), n=120))
        r4 = always_redraw(lambda: G.retangulo(DT_PAREDE, DT_PAREDE + tau.get_value(), J_PAREDE / tau.get_value()))
        num = DecimalNumber(J_PAREDE, num_decimal_places=1, font_size=44, color=JC).set_z_index(10)
        num.add_updater(lambda m: m.set_value(area_num(f_, 0.0, 0.030, 2001)))
        ar = txt("ÁREA =", T_MAIN, color=JC)
        un = MathTex(r"\mathrm{N\cdot s}", font_size=44, color=JC)
        cont = VGroup(ar, num, un).arrange(RIGHT, buff=0.2).move_to(P3(-3.3, 2.7)).set_z_index(10)
        num.add_updater(lambda m: None)
        self.add(c4, a4, r4)
        self.play(FadeIn(cont), run_time=0.6)
        self.ate(0.3)
        self.play(tau.animate.set_value(0.004), run_time=5.0)
        self.ate(0.65)
        self.play(tau.animate.set_value(0.012), run_time=3.5)
        self.ate(0.97)
        self.AREA_MEDIDA = area_num(f_, 0.0, 0.030, 20001)
        print(f"[QA] C03-4 área sob F_x(t) com τ = {tau.get_value() * 1000:.1f} ms: {self.AREA_MEDIDA:.4f} N·s (alvo 20)")
        for m in (c4, a4, r4, num):
            m.clear_updaters()
