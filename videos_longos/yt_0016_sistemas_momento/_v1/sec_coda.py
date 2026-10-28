"""Lote PC: coda — a luz também tem momento (Feynman §10-5). p = E/c; superfície preta F, espelho 2F; Sol 1.361 W/m²: 4,5 μPa
(absorvida), 9,1 μPa (refletida); vela solar refletora de 100 m²: ≈ 0,9 mN; laser de 1 W absorvido: 3,3 nN."""
from kit import *  # noqa: F401,F403

C_LUZ, I_SOL = 2.998e8, 1361.0
P_ABS, P_REF = I_SOL / C_LUZ, 2 * I_SOL / C_LUZ
F_VELA, F_LASER = P_REF * 100, 1.0 / C_LUZ
assert abs(P_ABS - 4.54e-6) < 0.01e-6 and abs(P_REF - 9.08e-6) < 0.01e-6 and abs(F_VELA - 0.908e-3) < 0.002e-3
assert abs(F_LASER - 3.34e-9) < 0.01e-9


def num(s, cor=WHITE_, size=M_LAB):
    return MathTex(s, font_size=size, color=cor)


def vela(c, esc=1.0):
    """Vela solar (silhueta preenchida): quatro velas triangulares espelhadas em volta de um corpo central."""
    g = VGroup()
    for k in range(4):
        a = k * PI / 2 + PI / 4
        tri = Polygon(c, c + esc * 1.1 * P3(math.cos(a - 0.38), math.sin(a - 0.38)), c + esc * 1.1 * P3(math.cos(a + 0.38), math.sin(a + 0.38)))
        g.add(tri.set_stroke(mix(GEO, 0.3), 1.5).set_fill(GEO, 0.55 if k % 2 else 0.75))
    g.add(Square(side_length=0.22 * esc).rotate(PI / 4).move_to(c).set_stroke(mix(STEEL, 0.4), 1.5).set_fill(STEEL, 1))
    return g


class LoteCoda(Base):
    def construct(self):
        self.setup_base(cap="A LUZ TAMBÉM TEM MOMENTO", selo="FEYNMAN §10-5")
        self.c1()
        self.c2()
        self.c3()
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
        ya, yb = 1.0, -1.4
        preta = Rectangle(width=0.35, height=1.3).move_to(P3(-1.6, ya)).set_stroke(DIM, 1.5).set_fill("#0A0C12", 1)
        espelho = Rectangle(width=0.35, height=1.3).move_to(P3(-1.6, yb)).set_stroke(WHITE_, 2).set_fill(GEO, 0.9)
        la = txt("SUPERFÍCIE PRETA: ABSORVE", 18, color=DIM).next_to(preta, UP, buff=0.15).shift(LEFT * 1.2)
        lb = txt("ESPELHO: REFLETE", 18, color=DIM).next_to(espelho, UP, buff=0.15).shift(LEFT * 1.6)
        fa, oa = self.feixe(ya, -6.8, -1.78)
        fb, ob = self.feixe(yb, -6.8, -1.78, volta=True)
        self.play(FadeIn(preta), FadeIn(espelho), FadeIn(la), FadeIn(lb), FadeIn(fa), FadeIn(fb), run_time=0.9)
        self.add(oa, ob)
        self.ate(0.28)
        pe = Mc((r"p", MAG), "=", (r"\frac{E}{c}", WHITE_), size=M_MAIN).move_to(P3(3.9, 1.0))
        self.play(FadeIn(pe, shift=0.1 * UP), run_time=0.9)
        self.ate(0.6)
        u = 0.9
        f1 = arrow(P3(-1.42, ya), P3(-1.42 + u, ya), color=FC, width=8, tip=0.22)
        f2 = arrow(P3(-1.42, yb), P3(-1.42 + 2 * u, yb), color=FC, width=8, tip=0.22)
        l1 = num(r"F", FC, 38).next_to(f1, UP, buff=0.1)
        l2 = num(r"2F", FC, 38).next_to(f2, UP, buff=0.1)
        self.play(GrowArrow(f1), FadeIn(l1), run_time=0.7)
        self.play(GrowArrow(f2), FadeIn(l2), run_time=0.7)
        fr = Mc((r"\frac{\Delta p}{\Delta t}", MAG), "=", (r"F", FC), size=50).move_to(P3(3.9, -1.0))
        nf = txt("MOMENTO POR SEGUNDO É FORÇA", 18, color=DIM).next_to(fr, DOWN, buff=0.2)
        self.ate(0.82)
        self.play(FadeIn(fr, shift=0.1 * UP), FadeIn(nf), run_time=0.8)
        self.ate(0.97)
        oa.clear_updaters()
        ob.clear_updaters()
        self.clear(rt=0.6)

    def c2(self):
        self.an("C-2")
        cards = []
        for i, (tit, linhas_) in enumerate((
                ("LUZ DO SOL", [num(r"1.361\ \mathrm{W/m^2}", WHITE_, 32),
                                linha(tex(r"4{,}5\ \mu\mathrm{Pa}", FC, 36), "ABSORVIDA", size=16, buff=0.15),
                                linha(tex(r"9{,}1\ \mu\mathrm{Pa}", FC, 36), "REFLETIDA", size=16, buff=0.15)]),
                ("VELA SOLAR", [linha(tex(r"100\ \mathrm{m^2}", WHITE_, 32), "REFLETORA", size=16, buff=0.15),
                                tex(r"\approx 0{,}9\ \mathrm{mN}", FC, 40)]),
                ("LASER DE 1 W", [linha("ABSORVIDO", size=16), tex(r"3{,}3\ \mathrm{nN}", FC, 40)]))):
            x = -4.6 + 4.6 * i
            p = placa(4.0, 4.4, P3(x, -0.35), op=0.05)
            t = txt(tit, 24, bold=True).move_to(P3(x, 1.45))
            corpo = VGroup(*linhas_).arrange(DOWN, buff=0.3).move_to(P3(x, -1.6))
            cards.append((p, t, corpo, x))
        # ícones: sol, vela, laser
        sol = VGroup(Circle(radius=0.38).set_stroke(width=0).set_fill(GEO, 0.9),
                     *[Line(0.5 * P3(math.cos(a), math.sin(a)), 0.72 * P3(math.cos(a), math.sin(a))).set_stroke(GEO, 3)
                       for a in np.linspace(0, 2 * PI, 12, endpoint=False)]).move_to(P3(cards[0][3], 0.45))
        vl = vela(P3(cards[1][3], 0.4), 0.75)
        las = VGroup(RoundedRectangle(corner_radius=0.06, width=1.0, height=0.34).set_stroke(mix(STEEL, 0.4), 1.5).set_fill(STEEL, 1),
                     Line(P3(0.5, 0), P3(1.4, 0)).set_stroke(WHITE_, 3, opacity=0.8)).move_to(P3(cards[2][3], 0.45))
        icones = (sol, vl, las)
        marcas = (0.0, 0.55, 0.85)
        for (p, t, corpo, x), ic, fr in zip(cards, icones, marcas):
            self.ate(fr)
            self.play(FadeIn(p), FadeIn(t), FadeIn(ic), run_time=0.6)
            for item in corpo:
                self.play(FadeIn(item, shift=0.1 * UP), run_time=0.5)
            if fr == 0.0:
                self.ate(0.38)
        vac = txt("NO VÁCUO, EMPURRANDO O TEMPO TODO", 18, color=DIM).move_to(P3(0, -3.2))
        self.ate(0.76)
        self.play(FadeIn(vac), run_time=0.5)
        self.ate(0.97)
        self.clear(rt=0.6)

    def c3(self):
        self.an("C-3")
        a = txt("O MODELO DO NEWTON CAIU.", 42, bold=True, color=APAGADO).move_to(P3(0, 0.8))
        b = txt("A CONSERVAÇÃO DO MOMENTO FICOU.", 42, bold=True, color=MAG).move_to(P3(0, -0.3))
        self.play(FadeIn(a, shift=0.1 * UP), run_time=0.8)
        self.ate(0.2)
        self.play(FadeIn(b, shift=0.1 * UP), run_time=0.8)
        self.ate(0.97)
        self.clear(rt=0.5)
