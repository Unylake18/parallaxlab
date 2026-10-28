"""Lote P10 (v2): T10 — como a energia se divide. PALCO: os blocos do T9 disparando pela mola em loop (sem atrito), com as setas de
momento iguais e as barras de momento (iguais) e de energia (2 J e 1 J) crescendo juntas. CONTA: P = 0 ⇒ m1v1 = m2v2 → v1/v2 = m2/m1
→ K1/K2 = m2/m1; fração do leve 2/3 (67%); massas iguais 50%."""
from fractions import Fraction

from kit import *  # noqa: F401,F403

M1, M2, PP = 1.0, 2.0, 2.0
K1, K2 = PP ** 2 / (2 * M1), PP ** 2 / (2 * M2)
assert (K1, K2) == (2.0, 1.0) and Fraction(int(K1), int(K1 + K2)) == Fraction(2, 3)
Y_CH = 0.75
XC = -3.6
LL, HL, LP, HP = 1.0, 1.0, 1.35, 1.3
PER, T0, TP = 4.6, 0.8, 0.25          # loop: parado T0, empurrão TP, depois voam
ESC = 0.75                            # u por metro na tela
YB = -3.1                             # base das barras


class LoteT10(Base):
    def construct(self):
        self.setup_base(cap="COMO A ENERGIA SE DIVIDE")
        self.palco()
        self.t10_1()
        self.t10_2()
        self.t10_3_4()
        self.fim()
        self.relatorio()

    def fase(self):
        s = (self.clk.get_value() - self.t0) % PER
        op = min(1.0, (PER - s) / 0.3, s / 0.3 + 0.15)
        return s, op

    def palco(self):
        self.t0 = self.clk.get_value()
        piso = chao(-7.3, 0.6, Y_CH, dens=3.0)
        sl = txt("SEM ATRITO AGORA", 16, color=DIM).move_to(P3(-1.0, Y_CH - 0.45))

        def cena():
            s, op = self.fase()
            u = 0.0 if s < T0 else min(1.0, (s - T0) / TP)       # fração do empurrão
            tl = max(0.0, s - T0 - TP)
            d1 = ESC * (2.0 * (0.5 * u * u * TP if u < 1 else 0.5 * TP) + 2.0 * tl)
            d2 = ESC * (1.0 * (0.5 * u * u * TP if u < 1 else 0.5 * TP) + 1.0 * tl)
            xa, xb = XC - 0.45 - LL / 2 - d1, XC + 0.45 + LP / 2 + d2
            A = Corpo("", GEO, LL, HL).at(xa, Y_CH)
            B = Corpo("", STEEL, LP, HP).at(xb, Y_CH)
            g = VGroup(A, B, mtex(r"1\ \mathrm{kg}", BACKGROUND_COLOR, 30).move_to(A), mtex(r"2\ \mathrm{kg}", WHITE_, 32).move_to(B))
            if u < 1:
                g.add(mola(P3(xa + LL / 2, Y_CH + 0.42), P3(xb - LP / 2, Y_CH + 0.42), n=6, amp=0.12 * (1 - 0.6 * u)))
            if u > 0:
                y = Y_CH + HP + 0.4
                g.add(arrow(P3(xa, y), P3(xa - 1.15 * u, y), color=MAG, width=8, tip=0.2, z=10))
                g.add(arrow(P3(xb, y), P3(xb + 1.15 * u, y), color=MAG, width=8, tip=0.2, z=10))
                g.add(mtex(r"\vec p_1", MAG, 32).move_to(P3(xa - 0.6, y + 0.35)), mtex(r"\vec p_2", MAG, 32).move_to(P3(xb + 0.6, y + 0.35)))
            # barras: momentos iguais (magenta) e energias 2 J e 1 J (ciano), crescendo com o empurrão
            xs = (-6.4, -5.6, -3.9, -3.1)
            alt = (1.2 * u, 1.2 * u, 0.9 * K1 * u * u, 0.9 * K2 * u * u)
            for x, h, c in zip(xs, alt, (MAG, MAG, KC, KC)):
                if h > 0.01:
                    g.add(Rectangle(width=0.58, height=h).set_stroke(mix(c, 0.3), 2).set_fill(c, 0.75).move_to(P3(x, YB + h / 2)))
            return escala_op(g, op) if op < 1 else g
        self.cn = always_redraw(cena)
        base = Line(P3(-6.9, YB), P3(-2.6, YB)).set_stroke(DIM, 2)
        rot = VGroup(*[tex(r, c, 28).move_to(P3(x, YB - 0.28)) for x, r, c in
                       ((-6.4, r"p_1", MAG), (-5.6, r"p_2", MAG), (-3.9, r"K_1", KC), (-3.1, r"K_2", KC))])
        lm = txt("MOMENTO", 16, color=MAG).move_to(P3(-6.0, YB - 0.65))
        le = txt("ENERGIA", 16, color=KC).move_to(P3(-3.5, YB - 0.65))
        self.barras = VGroup(base, rot, lm, le)
        self.play(FadeIn(piso), FadeIn(sl), FadeIn(self.cn), FadeIn(self.barras), run_time=0.9)

    def t10_1(self):
        self.an("T10-1")
        ri = txt("SÓ FORÇA INTERNA (A MOLA)", 18, color=INT)
        na_conta(ri, 2.25)
        e0 = Mc((r"\vec P", MAG), "=", "0", size=50)
        na_conta(e0, 1.45)
        self.play(FadeIn(ri), run_time=0.5)
        self.ate(0.3)
        self.play(FadeIn(e0, shift=0.1 * UP), run_time=0.7)
        e1 = Mc("m_1 v_1", "=", "m_2 v_2", size=54)
        na_conta(e1, 0.35)
        mo = txt("(MÓDULOS)", 18, color=DIM).next_to(e1, RIGHT, buff=0.25)
        self.ate(0.62)
        self.play(FadeIn(e1, shift=0.1 * UP), FadeIn(mo), run_time=0.8)
        self.ate(0.97)
        self.e0, self.e1, self.mo, self.ri = e0, e1, mo, ri

    def t10_2(self):
        self.an("T10-2")
        kp = Mc((r"K", KC), "=", (r"\frac{p^2}{2m}", MAG), size=48)
        nk = txt("DO VÍDEO ANTERIOR", 16, color=DIM)
        self.play(FadeOut(self.ri), FadeOut(self.e0), run_time=0.4)
        na_conta(kp, 2.05)
        nk.next_to(kp, RIGHT, buff=0.3)
        self.play(FadeIn(kp, shift=0.1 * UP), FadeIn(nk), run_time=0.8)
        inv = txt("MESMO MOMENTO: ENERGIA INVERSA À MASSA", 16, color=DIM)
        na_conta(inv, 1.2)
        self.ate(0.32)
        self.play(FadeIn(inv), run_time=0.6)
        self.play(self.e1.animate.move_to(P3(XC0 + self.e1.width / 2, 0.45)), self.mo.animate.next_to(P3(XC0 + self.e1.width, 0.45), RIGHT, buff=0.25),
                  run_time=0.5)
        e2 = Mc(r"\frac{v_1}{v_2}", "=", r"\frac{m_2}{m_1}", size=52)
        na_conta(e2, -0.75)
        self.ate(0.5)
        self.play(TransformMatchingTex(self.e1.copy(), e2), run_time=1.2)
        e3 = Mc((r"\frac{K_1}{K_2}", KC), "=", r"\frac{m_1}{m_2}", r"\left(\frac{v_1}{v_2}\right)^2", "=", r"\frac{m_2}{m_1}", size=50)
        na_conta(e3, -2.2)
        self.ate(0.72)
        self.play(FadeIn(e3[:4], shift=0.1 * UP), run_time=0.9)
        self.play(FadeIn(e3[4:], shift=0.1 * LEFT), run_time=0.7)
        cx = SurroundingRectangle(e3[5], buff=0.12, corner_radius=0.08).set_stroke(KC, 2.5)
        self.play(Create(cx), run_time=0.5)
        self.ate(0.97)
        self.esq = VGroup(kp, nk, inv, self.e1, self.mo, e2, cx)
        self.e3 = e3

    def t10_3_4(self):
        self.an("T10-3")
        topo = Mc((r"\frac{K_1}{K_2}", KC), "=", r"\frac{m_2}{m_1}", size=50)
        na_conta(topo, 2.0)
        self.play(FadeOut(self.esq), ReplacementTransform(self.e3, topo), run_time=0.9)
        dm = txt("MOMENTO SE DIVIDE IGUAL; ENERGIA, NÃO", 20, bold=True)
        na_conta(dm, 1.05)
        self.ate(0.12)
        self.play(FadeIn(dm), Indicate(self.barras[2], color=WHITE_), run_time=0.7)
        k12 = Mc((r"K_1=2\ \mathrm{J}", KC), r",\quad", (r"K_2=1\ \mathrm{J}", KC), size=42)
        fr = linha("FRAÇÃO DO MAIS LEVE:", tex(r"\tfrac{2}{3}\ (67\%)", KC, 40), size=20, buff=0.2)
        ig = linha("MASSAS IGUAIS:", tex(r"50\%", KC, 40), size=20, buff=0.2)
        for m_, y in ((k12, 0.2), (fr, -0.6), (ig, -1.3)):
            na_conta(m_, y)
        self.ate(0.3)
        self.play(FadeIn(k12, shift=0.1 * UP), Indicate(self.barras[3], color=WHITE_), run_time=0.7)
        self.ate(0.45)
        self.play(FadeIn(fr, shift=0.1 * UP), run_time=0.7)
        self.ate(0.58)
        self.play(FadeIn(ig, shift=0.1 * UP), run_time=0.6)
        f1 = txt("QUANTO MAIOR A DIFERENÇA DE MASSAS,", 18)
        f2 = txt("MAIS ENERGIA FICA COM O MAIS LEVE", 18, color=KC)
        f3 = txt("GUARDA PARA O CAÇADOR", 16, color=DIM)
        for m_, y in ((f1, -2.05), (f2, -2.45), (f3, -2.95)):
            na_conta(m_, y)
        self.ate(0.66)
        self.play(FadeIn(VGroup(f1, f2)), run_time=0.8)
        self.ate(0.88)
        self.play(FadeIn(f3), run_time=0.5)
        self.ate(0.97)
        # T10-4 — DICA
        self.an("T10-4")
        self.play(FadeOut(VGroup(f1, f2, f3)), run_time=0.3)
        d = dica("MESMO MOMENTO: QUANTO MAIS LEVE,", "MAIOR A FRAÇÃO DA ENERGIA")
        self.dica_entra(d)
        self.ate(0.97)
        self.cn.clear_updaters()
        self.dica_sai()
        self.clear(rt=0.5)
