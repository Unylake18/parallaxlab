"""Lote PC (v2): coda — a luz também tem momento. C-1: feixe na superfície preta (F) e no espelho (2F), p = E/c (2D, PALCO vivo).
C-2/C-3: vela solar refletora 3D (threejs/cena3d/vela.js) abrindo no espaço, fótons batendo e voltando, a seta da força crescendo;
números na CONTA. Sol 1.361 W/m²: 4,5 μPa (absorvida), 9,1 μPa (refletida); vela de 100 m²: ≈ 0,9 mN; laser de 1 W: 3,3 nN."""
from kit import *  # noqa: F401,F403

C_LUZ, I_SOL = 2.998e8, 1361.0
P_ABS, P_REF = I_SOL / C_LUZ, 2 * I_SOL / C_LUZ
F_VELA, F_LASER = P_REF * 100, 1.0 / C_LUZ
assert abs(P_ABS - 4.54e-6) < 0.01e-6 and abs(P_REF - 9.08e-6) < 0.01e-6 and abs(F_VELA - 0.908e-3) < 0.002e-3
assert abs(F_LASER - 3.34e-9) < 0.01e-9


def num(s, cor=WHITE_, size=M_LAB):
    return MathTex(s, font_size=size, color=cor)


class LoteCoda(Base):
    def construct(self):
        self.setup_base(cap="A LUZ TAMBÉM TEM MOMENTO")
        self.c1()
        self.c2_3()
        self.fim()
        self.relatorio()

    def feixe(self, y, x0, x1, volta=False):
        g = VGroup(Rectangle(width=x1 - x0, height=0.34).move_to(P3((x0 + x1) / 2, y)).set_stroke(width=0).set_fill(WHITE_, 0.08))

        def ondas():
            s = self.clk.get_value()
            h = VGroup()
            L = x1 - x0
            for k in range(7):
                x = x0 + ((s * 1.4 + k * L / 7) % L)
                h.add(Line(P3(x, y + (0.08 if volta else 0)), P3(min(x + 0.3, x1), y + (0.08 if volta else 0))).set_stroke(WHITE_, 3, opacity=0.8))
                if volta:
                    xr = x1 - ((s * 1.4 + k * L / 7) % L)
                    h.add(Line(P3(xr, y - 0.1), P3(max(xr - 0.3, x0), y - 0.1)).set_stroke(WHITE_, 3, opacity=0.5))
            return h
        return g, always_redraw(ondas)

    def c1(self):
        self.an("C-1")
        ya, yb = 1.1, -1.5
        preta = Rectangle(width=0.4, height=1.6).move_to(P3(-1.4, ya)).set_stroke(DIM, 1.5).set_fill("#0A0C12", 1)
        espelho = Rectangle(width=0.4, height=1.6).move_to(P3(-1.4, yb)).set_stroke(WHITE_, 2).set_fill(GEO, 0.9)
        la = txt("SUPERFÍCIE PRETA: ABSORVE", 18, color=DIM).move_to(P3(-4.3, ya + 1.05))
        lb = txt("ESPELHO: REFLETE", 18, color=DIM).move_to(P3(-4.3, yb + 1.05))
        fa, oa = self.feixe(ya, -7.2, -1.6)
        fb, ob = self.feixe(yb, -7.2, -1.6, volta=True)
        self.play(FadeIn(preta), FadeIn(espelho), FadeIn(la), FadeIn(lb), FadeIn(fa), FadeIn(fb), run_time=0.9)
        self.add(oa, ob)
        self.ate(0.28)
        pe = Mc((r"p", MAG), "=", (r"\frac{E}{c}", WHITE_), size=M_MAIN)
        na_conta(pe, 1.3)
        self.play(FadeIn(pe, shift=0.1 * UP), run_time=0.9)
        self.ate(0.6)
        pul = ValueTracker(0.0)
        u = 0.85
        fs = always_redraw(lambda: VGroup(
            arrow(P3(-1.15, ya), P3(-1.15 + u * (1 + 0.12 * math.sin(4 * self.clk.get_value())), ya), color=FC, width=8, tip=0.22),
            arrow(P3(-1.15, yb), P3(-1.15 + 2 * u * (1 + 0.12 * math.sin(4 * self.clk.get_value())), yb), color=FC, width=8, tip=0.22),
            mtex(r"F", FC, 38).move_to(P3(-0.6, ya + 0.42)), mtex(r"2F", FC, 38).move_to(P3(-0.2, yb + 0.42))))
        self.play(FadeIn(fs), run_time=0.8)
        fr = Mc((r"\frac{\Delta p}{\Delta t}", MAG), "=", (r"F", FC), size=50)
        nf = txt("MOMENTO POR SEGUNDO É FORÇA", 18, color=DIM)
        na_conta(fr, -0.6); na_conta(nf, -1.45)
        self.ate(0.82)
        self.play(FadeIn(fr, shift=0.1 * UP), FadeIn(nf), run_time=0.8)
        self.ate(0.97)
        for m_ in (oa, ob, fs):
            m_.clear_updaters()
        self.clear(rt=0.6)

    def c2_3(self):
        self.an("C-2")
        t0 = self.clk.get_value()
        self.afasta = None

        def estado(t):
            s = t - t0
            x = 0.0 if self.afasta is None else 0.08 * (t - self.afasta) ** 2
            return {"abre": min(1.0, s / 6.0), "ang": 0.22 * math.sin(0.18 * s), "fase": s, "x": x, "vis_f": 1.0,
                    "cam": {"modo": "obl", "az": -120, "el": 18, "fov": 30, "alt": 9, "alvo": [0, 0, 0], "xc": -3.3, "yc": -0.1}}
        f3d = Fundo3D(self, "vela", estado, op=0.0)
        self.add(f3d)
        self.play(f3d.op.animate.set_value(1.0), run_time=1.0)
        fseta = always_redraw(lambda: VGroup(
            arrow(P3(-2.2, -2.45), P3(-2.2 + 1.5 * min(1.0, (self.clk.get_value() - t0) / 6.0), -2.45), color=FC, width=7, tip=0.18, z=12),
            mtxt("FORÇA DA LUZ NA VELA", 15, color=FC).move_to(P3(-1.5, -2.85))))
        self.play(FadeIn(fseta), run_time=0.6)
        c1 = txt("LUZ DO SOL", 22, bold=True)
        q1 = num(r"1.361\ \mathrm{W/m^2}", WHITE_, 36)
        q2 = linha(tex(r"4{,}5\ \mu\mathrm{Pa}", FC, 38), "ABSORVIDA", size=16, buff=0.15)
        q3 = linha(tex(r"9{,}1\ \mu\mathrm{Pa}", FC, 38), "REFLETIDA", size=16, buff=0.15)
        c2 = txt("VELA SOLAR DE 100 M² REFLETORA", 20, bold=True)
        q4 = tex(r"\approx 0{,}9\ \mathrm{mN}", FC, 44)
        c3 = linha("LASER DE 1 W:", tex(r"3{,}3\ \mathrm{nN}", FC, 40), size=20, buff=0.2)
        for m_, y in ((c1, 2.35), (q1, 1.8), (q2, 1.2), (q3, 0.65), (c2, -0.15), (q4, -0.75), (c3, -1.6)):
            na_conta(m_, y)
        self.play(FadeIn(c1), FadeIn(q1), run_time=0.7)
        self.ate(0.3)
        self.play(FadeIn(q2, shift=0.1 * UP), run_time=0.6)
        self.ate(0.42)
        self.play(FadeIn(q3, shift=0.1 * UP), run_time=0.6)
        self.ate(0.55)
        self.play(FadeIn(c2), FadeIn(q4, shift=0.1 * UP), run_time=0.8)
        vac = txt("NO VÁCUO, EMPURRANDO O TEMPO TODO", 16, color=DIM)
        na_conta(vac, -2.25)
        self.ate(0.72)
        self.play(FadeIn(vac), run_time=0.5)
        self.ate(0.85)
        self.play(FadeIn(c3, shift=0.1 * UP), run_time=0.6)
        self.ate(0.97)
        # C-3 — a vela se afasta; a frase de fechamento entra na CONTA com o PALCO trabalhando
        self.an("C-3")
        self.afasta = self.clk.get_value()
        self.play(FadeOut(VGroup(c1, q1, q2, q3, c2, q4, c3, vac)), run_time=0.6)
        a = txt("O MODELO DO NEWTON CAIU.", 30, bold=True, color=APAGADO)
        b = txt("A CONSERVAÇÃO DO MOMENTO FICOU.", 30, bold=True, color=MAG)
        na_conta(a, 1.0); na_conta(b, 0.2)
        if b.get_right()[0] > 7.4:
            b.scale_to_fit_width(7.4 - XC0); na_conta(b, 0.2)
        self.play(FadeIn(a, shift=0.1 * UP), run_time=0.8)
        self.ate(0.2)
        self.play(FadeIn(b, shift=0.1 * UP), run_time=0.8)
        v1 = txt("VALE PARA A LUZ, NA FÍSICA QUÂNTICA", 16, color=DIM)
        v2 = txt("E EM TUDO O QUE A GENTE SABE MEDIR", 16, color=DIM)
        na_conta(v1, -0.7); na_conta(v2, -1.1)
        self.ate(0.5)
        self.play(FadeIn(v1), FadeIn(v2), run_time=0.7)
        self.ate(0.97)
        fseta.clear_updaters()
        self.clear(rt=0.5)
