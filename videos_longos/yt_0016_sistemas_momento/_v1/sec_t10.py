"""Lote P10: T10 — como a energia se divide. P = 0 ⇒ m1v1 = m2v2 → v1/v2 = m2/m1 → K1/K2 = m2/m1; blocos de 1 e 2 kg (p = 2 kg·m/s):
K = 2 J e 1 J, fração do leve 2/3 (67%); massas iguais 50%."""
from kit import *  # noqa: F401,F403
from fractions import Fraction

M1, M2, PP = 1.0, 2.0, 2.0
K1, K2 = PP ** 2 / (2 * M1), PP ** 2 / (2 * M2)
assert (K1, K2) == (2.0, 1.0) and Fraction(int(K1), int(K1 + K2)) == Fraction(2, 3)
Y_CH = 0.35
XR = 3.9


class LoteT10(Base):
    def construct(self):
        self.setup_base(cap="COMO A ENERGIA SE DIVIDE")
        self.t10_1()
        self.t10_2()
        self.t10_3_4()
        self.fim()
        self.relatorio()

    def t10_1(self):
        self.an("T10-1")
        piso = chao(-7.2, -0.5, Y_CH)
        s = ValueTracker(0.0)

        def blocos():
            d = s.get_value()
            A = Corpo("", GEO, 0.72).at(-3.9 - 1.0 * d, Y_CH)
            B = Corpo("", STEEL, 1.05, 0.95).at(-2.95 + 0.5 * d, Y_CH)
            g = VGroup(A, B, tex(r"1\ \mathrm{kg}", BACKGROUND_COLOR, 26).move_to(A), tex(r"2\ \mathrm{kg}", WHITE_, 28).move_to(B))
            if d > 0.02:
                y = Y_CH + 1.35
                g.add(arrow(P3(A.get_x(), y), P3(A.get_x() - 1.2, y), color=MAG, width=7, tip=0.2, z=10))
                g.add(arrow(P3(B.get_x(), y), P3(B.get_x() + 1.2, y), color=MAG, width=7, tip=0.2, z=10))
                g.add(tex(r"\vec p_1", MAG, 32).move_to(P3(A.get_x() - 0.6, y + 0.32)))
                g.add(tex(r"\vec p_2", MAG, 32).move_to(P3(B.get_x() + 0.6, y + 0.32)))
            else:
                g.add(mola(P3(-3.9 + 0.36, Y_CH + 0.36), P3(-2.95 - 0.525, Y_CH + 0.36), n=5, amp=0.1))
            return g
        bg = always_redraw(blocos)
        self.play(FadeIn(piso), FadeIn(bg), run_time=0.8)
        ri = txt("SÓ FORÇAS INTERNAS", 20, color=INT).move_to(P3(-3.4, Y_CH - 0.55))
        self.play(FadeIn(ri), run_time=0.5)
        self.ate(0.18)
        self.play(s.animate.set_value(1.6), run_time=4.0, rate_func=lambda u: u)
        e0 = Mc((r"\vec P", MAG), "=", "0", size=50).move_to(P3(XR, 1.6))
        self.play(FadeIn(e0, shift=0.1 * UP), run_time=0.7)
        self.ate(0.62)
        e1 = Mc("m_1 v_1", "=", "m_2 v_2", size=56).move_to(P3(XR, 0.2))
        mo = txt("(MÓDULOS)", 18, color=DIM).next_to(e1, RIGHT, buff=0.25)
        self.play(FadeIn(e1, shift=0.1 * UP), FadeIn(mo), run_time=0.8)
        self.ate(0.97)
        bg.clear_updaters()
        self.bg, self.e0, self.e1, self.mo, self.piso, self.ri = bg, e0, e1, mo, piso, ri

    def t10_2(self):
        self.an("T10-2")
        kp = Mc((r"K", KC), "=", (r"\frac{p^2}{2m}", MAG), size=50).move_to(P3(XR, 2.0))
        nk = txt("DO VÍDEO ANTERIOR", 18, color=DIM).next_to(kp, RIGHT, buff=0.3)
        self.play(FadeOut(self.e0), FadeIn(kp, shift=0.1 * UP), FadeIn(nk), run_time=0.8)
        self.ate(0.32)
        inv = txt("MESMO MOMENTO: ENERGIA INVERSA À MASSA", 18, color=DIM).move_to(P3(XR, 1.05))
        self.play(FadeIn(inv), run_time=0.6)
        self.ate(0.5)
        e2 = Mc(r"\frac{v_1}{v_2}", "=", r"\frac{m_2}{m_1}", size=56).move_to(P3(XR, -0.95))
        self.play(TransformMatchingTex(self.e1.copy(), e2), run_time=1.2)
        self.ate(0.72)
        e3 = Mc((r"\frac{K_1}{K_2}", KC), "=", r"\frac{m_1}{m_2}", r"\left(\frac{v_1}{v_2}\right)^2", "=", r"\frac{m_2}{m_1}", size=56) \
            .move_to(P3(XR, -2.4))
        self.play(FadeIn(e3[:4], shift=0.1 * UP), run_time=0.9)
        self.play(FadeIn(e3[4:], shift=0.1 * LEFT), run_time=0.7)
        cx = SurroundingRectangle(e3[5], buff=0.12, corner_radius=0.08).set_stroke(KC, 2.5)
        self.play(Create(cx), run_time=0.5)
        self.ate(0.97)
        self.esq = VGroup(kp, nk, inv, self.e1, self.mo, e2, cx)
        self.e3 = e3

    def t10_3_4(self):
        self.an("T10-3")
        topo = Mc((r"\frac{K_1}{K_2}", KC), "=", r"\frac{m_2}{m_1}", size=50).move_to(P3(XR, 1.6))
        self.play(FadeOut(self.esq), ReplacementTransform(self.e3, topo), run_time=0.9)
        # barras: momentos iguais (magenta) e energias diferentes (ciano)
        yb, u = -3.2, 1.0
        xs = (-6.0, -5.1, -3.4, -2.5)
        alt = (PP * 0.8, PP * 0.8, K1 * u, K2 * u)
        cores = (MAG, MAG, KC, KC)
        rot = (r"p_1", r"p_2", r"K_1", r"K_2")
        barras = VGroup()
        for x, h, c, r in zip(xs, alt, cores, rot):
            b = Rectangle(width=0.62, height=h).set_stroke(mix(c, 0.3), 2).set_fill(c, 0.75).move_to(P3(x, yb + h / 2))
            barras.add(VGroup(b, tex(r, c, 30).next_to(b, DOWN, buff=0.12)))
        vals = VGroup(tex(r"2", MAG, 28).next_to(barras[0][0], UP, buff=0.08), tex(r"2", MAG, 28).next_to(barras[1][0], UP, buff=0.08),
                      tex(r"2\ \mathrm{J}", KC, 28).next_to(barras[2][0], UP, buff=0.08), tex(r"1\ \mathrm{J}", KC, 28).next_to(barras[3][0], UP, buff=0.08))
        base = Line(P3(-6.6, yb), P3(-1.9, yb)).set_stroke(DIM, 2)
        lm = txt("MOMENTO", 18, color=MAG).move_to(P3(-5.55, yb - 0.75))
        le = txt("ENERGIA", 18, color=KC).move_to(P3(-2.95, yb - 0.75))
        self.play(FadeIn(base), *[GrowFromEdge(b[0], DOWN) for b in barras[:2]], *[FadeIn(b[1]) for b in barras[:2]], FadeIn(vals[:2]),
                  FadeIn(lm), run_time=1.0)
        self.ate(0.15)
        self.play(*[GrowFromEdge(b[0], DOWN) for b in barras[2:]], *[FadeIn(b[1]) for b in barras[2:]], FadeIn(vals[2:]), FadeIn(le),
                  run_time=1.0)
        k12 = Mc((r"K_1=2\ \mathrm{J}", KC), r",\quad", (r"K_2=1\ \mathrm{J}", KC), size=44).move_to(P3(XR, 0.6))
        fr = linha("FRAÇÃO DO MAIS LEVE:", tex(r"\tfrac{2}{3}\ (67\%)", KC, 40), size=22, buff=0.2).move_to(P3(XR, -0.25))
        ig = linha("MASSAS IGUAIS:", tex(r"50\%", KC, 40), size=22, buff=0.2).move_to(P3(XR, -0.95))
        self.ate(0.3)
        self.play(FadeIn(k12, shift=0.1 * UP), run_time=0.7)
        self.ate(0.45)
        self.play(FadeIn(fr, shift=0.1 * UP), run_time=0.7)
        self.ate(0.58)
        self.play(FadeIn(ig, shift=0.1 * UP), run_time=0.6)
        f1 = txt("QUANTO MAIOR A DIFERENÇA DE MASSAS,", 20)
        f2 = txt("MAIOR A FRAÇÃO DA ENERGIA CINÉTICA", 20, color=KC)
        f3 = txt("QUE FICA COM O MAIS LEVE", 20, color=KC)
        VGroup(f1, f2, f3).arrange(DOWN, buff=0.12).move_to(P3(XR, -1.95))
        self.ate(0.66)
        self.play(FadeIn(VGroup(f1, f2, f3), shift=0.1 * UP), run_time=0.9)
        self.ate(0.97)
        # T10-4 ----------------------------------------------------------------------------------------------
        self.an("T10-4")
        self.play(FadeOut(VGroup(f1, f2, f3)), run_time=0.3)
        d = dica("MESMO MOMENTO: QUANTO MAIS LEVE,", "MAIOR A FRAÇÃO DA ENERGIA")
        self.dica_entra(d)
        self.ate(0.97)
        self.wait(1.2)
        self.dica_sai()
        self.clear(rt=0.5)
