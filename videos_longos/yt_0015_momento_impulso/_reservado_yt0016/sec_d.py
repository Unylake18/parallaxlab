"""Lote D: C09 (conservação), C10 (agarrar ou rebater), C11 (caçador), C12 (gases do rifle) e C13-1."""
from kit import *  # noqa: F401,F403


def tex(s, cor=WHITE_, size=M_MID):
    return MathTex(s, font_size=size, color=cor)


def fluxo_pontos(sc, x0, x1, y, n=16, v=2.2, tam=0.07):
    """Corpúsculos de luz: pontos brancos em fila, andando da esquerda para a direita (função do relógio da cena)."""
    L = x1 - x0
    esp = L / n

    def make():
        g = VGroup()
        for k in range(n):
            x = x0 + ((sc.clk.get_value() * v + k * esp) % L)
            g.add(Dot(P3(x, y), radius=tam, color=WHITE_).set_z_index(6))
        return g
    return always_redraw(make)


class LoteD(Base):
    def construct(self):
        self.setup_base(cap="EXERCÍCIO 5 · A PULGA", selo="MOYSÉS · PROB. 4.7")
        self.c09()
        self.c10()
        self.c11()
        self.c12()
        self.c13_1()
        self.fim()
        self.relatorio()

    # ── C09 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def c09(self):
        self.clear(rt=0.6)
        self.secao("POR QUE O MOMENTO SE CONSERVA")
        self.an("C09-1")
        b1 = Corpo("1", GEO, 1.0, size=40).at(-3.4, -0.5)
        b2 = Corpo("2", STEEL, 1.0, size=40).at(-2.2, -0.5)
        pista = Line(P3(-7.2, -0.5), P3(0.2, -0.5)).set_stroke(GEO, 2, opacity=0.5)
        f12 = arrow(P3(-3.9, 0.0), P3(-5.9, 0.0), color=FC, width=8, tip=0.24)
        f21 = arrow(P3(-1.7, 0.0), P3(0.3, 0.0), color=FC, width=8, tip=0.24)
        l12 = tex(r"\vec F_{12}", FC, 44).next_to(f12, UP, buff=0.12)
        l21 = tex(r"\vec F_{21}", FC, 44).next_to(f21, UP, buff=0.12)
        self.play(FadeIn(pista), FadeIn(b1), FadeIn(b2), run_time=0.7)
        self.play(GrowArrow(f12), GrowArrow(f21), FadeIn(l12), FadeIn(l21), run_time=1.0)
        self.ate(0.55)
        ig = txt("IGUAIS E OPOSTAS", T_LAB, color=FC).move_to(P3(-2.8, -1.9))
        self.play(FadeIn(ig), run_time=0.6)
        self.ate(0.97)
        # C09-2 ----------------------------------------------------------------------------------------------
        self.an("C09-2")
        e1 = Mc((r"\frac{d\vec p_1}{dt}", MAG), "=", (r"\vec F_{12}", FC), size=M_MID).move_to(P3(4.4, 2.3))
        e2 = Mc((r"\frac{d\vec p_2}{dt}", MAG), "=", (r"\vec F_{21}", FC), size=M_MID).move_to(P3(4.4, 0.6))
        e3 = Mc((r"\frac{d(\vec p_1+\vec p_2)}{dt}", MAG), "=", r"0", size=M_MID).move_to(P3(4.4, -1.3))
        self.play(FadeIn(e1, shift=0.1 * UP), run_time=0.8)
        self.ate(0.3)
        self.play(FadeIn(e2, shift=0.1 * UP), run_time=0.8)
        self.ate(0.6)
        self.play(FadeIn(e3, shift=0.1 * UP), run_time=1.0)
        self.ate(0.97)
        # C09-3 ----------------------------------------------------------------------------------------------
        self.an("C09-3")
        self.play(*[FadeOut(m) for m in (b1, b2, f12, f21, l12, l21, ig, e1, e2, e3)], run_time=0.5)
        cs = [bola(0.28, GEO if k % 2 == 0 else STEEL).move_to(p) for k, p in
              enumerate((P3(-5.2, 0.6), P3(-3.6, 1.2), P3(-2.6, -0.2), P3(-4.4, -0.7)))]
        contorno = DashedVMobject(Ellipse(width=5.2, height=3.4).move_to(P3(-3.9, 0.3)).set_stroke(WHITE_, 2, opacity=0.6),
                                  num_dashes=50)
        pares = VGroup(*[VGroup(arrow(a.get_center() + 0.32 * (b.get_center() - a.get_center()) / np.linalg.norm(b.get_center() - a.get_center()),
                                      a.get_center() + 0.75 * (b.get_center() - a.get_center()) / np.linalg.norm(b.get_center() - a.get_center()),
                                      color=FC, width=3, tip=0.1),
                                arrow(b.get_center() - 0.32 * (b.get_center() - a.get_center()) / np.linalg.norm(b.get_center() - a.get_center()),
                                      b.get_center() - 0.75 * (b.get_center() - a.get_center()) / np.linalg.norm(b.get_center() - a.get_center()),
                                      color=FC, width=3, tip=0.1)) for a, b in ((cs[0], cs[3]), (cs[1], cs[2]), (cs[0], cs[1]), (cs[3], cs[2]))])
        ext = arrow(P3(-1.3, -2.3), P3(-2.2, -1.2), color=FC, width=7, tip=0.22)
        lext = tex(r"\vec F_{ext}", FC, 40).next_to(ext, RIGHT, buff=0.1)
        lint = txt("FORÇAS INTERNAS SE CANCELAM", T_SMALL, color=DIM).move_to(P3(-3.9, 2.55))
        self.play(FadeIn(VGroup(*cs)), Create(contorno), run_time=0.9)
        self.play(FadeIn(pares), FadeIn(lint), run_time=0.8)
        self.ate(0.45)
        self.play(GrowArrow(ext), FadeIn(lext), run_time=0.7)
        pp = Mc((r"\vec P", MAG), "=", (r"\vec p_1+\vec p_2+\cdots", MAG), size=44).move_to(P3(4.4, 2.2))
        dp = Mc((r"\frac{d\vec P}{dt}", MAG), "=", (r"\vec F_{ext}", FC), size=M_MAIN).move_to(P3(4.4, 0.7))
        cc = Mc((r"\vec F_{ext}=0\ \Rightarrow\ \vec P\ \text{constante}", MAG), size=40, w=6.0).move_to(P3(4.4, -0.9))
        self.play(FadeIn(pp), run_time=0.6)
        self.play(FadeIn(dp, shift=0.1 * UP), run_time=0.8)
        self.ate(0.8)
        self.play(FadeIn(cc, shift=0.1 * UP), run_time=0.8)
        self.ate(0.97)
        # C09-4 ----------------------------------------------------------------------------------------------
        self.an("C09-4")
        self.play(FadeOut(pp), FadeOut(cc), FadeOut(dp), run_time=0.4)
        cx = Mc((r"\frac{dP_x}{dt}", MAG), "=", (r"F_{ext,x}", FC), size=M_MAIN).move_to(P3(4.4, 1.4))
        cy = Mc((r"\frac{dP_y}{dt}", MAG), "=", (r"F_{ext,y}", FC), size=M_MAIN).move_to(P3(4.4, -0.4))
        nota = txt("COMPONENTE POR COMPONENTE", T_LAB, color=DIM).move_to(P3(4.4, -1.9))
        self.play(FadeIn(cx, shift=0.1 * UP), run_time=0.8)
        self.ate(0.4)
        self.play(FadeIn(cy, shift=0.1 * UP), FadeIn(nota), run_time=0.8)
        self.ate(0.97)

    # ── C10 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def c10(self):
        self.clear(rt=0.6)
        self.secao("EXERCÍCIO 6 · AGARRAR OU REBATER", "SEARS · EXERC. 8.20")
        self.an("C10-1")
        gelo = Line(P3(-7.4, -2.2), P3(0.6, -2.2)).set_stroke(GEO, 2.5, opacity=0.55)
        pes = Pessoa(GEO, esc=0.8).pose(-2.0, -2.2, None)
        bl = bola(0.2).move_to(P3(-6.5, -0.4))
        va = arrow(P3(-6.2, -0.4), P3(-4.4, -0.4), color=VEL, width=6)
        vl = tex(r"10{,}0\ \mathrm{m/s}", VEL, 32).next_to(va, UP, buff=0.1)
        dad = VGroup(tex(r"m_{voc\hat{e}}=70{,}0\ \mathrm{kg}", WHITE_, 40), tex(r"m_{bola}=0{,}600\ \mathrm{kg}", WHITE_, 40)) \
            .arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(P3(4.2, 1.8))
        self.play(FadeIn(gelo), FadeIn(pes), run_time=0.7)
        self.play(FadeIn(bl), GrowArrow(va), FadeIn(vl), FadeIn(dad), run_time=0.9)
        self.ate(0.97)
        # C10-2 ----------------------------------------------------------------------------------------------
        self.an("C10-2")
        t1 = txt("AGARRA", T_MAIN, bold=True).move_to(P3(4.2, -0.1))
        e1 = Mc((r"V=\frac{0{,}600\cdot10{,}0}{70{,}6}=0{,}085\ \mathrm{m/s}", VEL), size=40, w=6.2).move_to(P3(4.2, -1.3))
        self.play(FadeIn(t1), run_time=0.5)
        self.play(FadeOut(va), FadeOut(vl), bl.animate.move_to(P3(-1.55, -0.3)), run_time=1.6)
        grupo = VGroup(pes, bl)
        vV = arrow(P3(-2.0, 0.9), P3(-1.3, 0.9), color=VEL, width=6)
        vVl = tex(r"V", VEL, 40).next_to(vV, UP, buff=0.1)
        self.play(grupo.animate.shift(RIGHT * 0.5), GrowArrow(vV), FadeIn(vVl), FadeIn(e1, shift=0.1 * UP), run_time=1.4)
        self.ate(0.97)
        # C10-3 ----------------------------------------------------------------------------------------------
        self.an("C10-3")
        self.play(*[FadeOut(m) for m in (t1, e1, vV, vVl, bl, pes)], run_time=0.5)
        pes = Pessoa(GEO, esc=0.8).pose(-2.0, -2.2, None)
        bl = bola(0.2).move_to(P3(-6.5, -0.4))
        t2 = txt("REBATE", T_MAIN, bold=True).move_to(P3(4.2, -0.1))
        va2 = arrow(P3(-6.2, -0.4), P3(-4.4, -0.4), color=VEL, width=6)
        e2 = Mc(r"70{,}0\,V=0{,}600\,(10{,}0+8{,}0)", size=36, w=6.2).move_to(P3(4.2, -1.1))
        e3 = Mc((r"V=0{,}154\ \mathrm{m/s}", VEL), size=40).move_to(P3(4.2, -2.1))
        self.play(FadeIn(pes), FadeIn(bl), FadeIn(va2), FadeIn(t2), run_time=0.7)
        self.play(FadeOut(va2), bl.animate.move_to(P3(-1.6, -0.3)), run_time=1.2)
        vb = arrow(P3(-1.7, -0.3), P3(-3.1, -0.3), color=VEL, width=6)
        vbl = tex(r"8{,}0\ \mathrm{m/s}", VEL, 30).next_to(vb, UP, buff=0.1)
        vV = arrow(P3(-2.0, 0.9), P3(-0.9, 0.9), color=VEL, width=6)
        vVl = tex(r"V", VEL, 40).next_to(vV, UP, buff=0.1)
        self.play(bl.animate.shift(LEFT * 1.5), FadeIn(vb), FadeIn(vbl), pes.animate.shift(RIGHT * 0.8), GrowArrow(vV), FadeIn(vVl),
                  run_time=1.6)
        self.ate(0.5)
        self.play(FadeIn(e2), run_time=0.7)
        self.play(FadeIn(e3, shift=0.1 * UP), run_time=0.7)
        # miniatura do C04-6
        k = 0.075
        mini = VGroup(txt("PARAR", 20, color=DIM).move_to(P3(0, 0)), txt("REBATER", 20, color=DIM).move_to(P3(0, -0.8)))
        for y, ex in ((0.0, 0.0), (-0.8, 8 * k)):
            pass
        pa = arrow(P3(1.5, 3.0), P3(1.5 - 12 * k, 3.0), color=MAG, width=4, tip=0.1)
        da = arrow(P3(1.5 - 12 * k, 2.7), P3(1.5, 2.7), color=MAG, width=5, tip=0.12)
        pb = arrow(P3(1.5, 2.2), P3(1.5 - 12 * k, 2.2), color=MAG, width=4, tip=0.1)
        db = arrow(P3(1.5 - 12 * k, 1.9), P3(1.5 + 8 * k, 1.9), color=MAG, width=5, tip=0.12)
        mn = VGroup(pa, da, pb, db, txt("PARAR", 18, color=DIM).next_to(da, LEFT, buff=0.15), txt("REBATER", 18, color=DIM).next_to(db, LEFT, buff=0.15))
        mn.move_to(P3(4.6, -3.0))
        self.play(FadeIn(mn), run_time=0.7)
        self.ate(0.97)

    # ── C11 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def c11(self):
        self.clear(rt=0.6)
        self.secao("EXERCÍCIO 7 · O CAÇADOR NO LAGO", "SEARS · EXERC. 8.25")
        self.an("C11-1")
        gelo = Line(P3(-7.4, -2.4), P3(0.4, -2.4)).set_stroke(GEO, 2.5, opacity=0.55)
        ca = Pessoa(GEO, esc=0.8).pose(-4.0, -2.4, None)
        arma = Line(P3(-3.9, -0.55), P3(-2.3, -0.55)).set_stroke(mix(STEEL, 0.3), 7)
        dad = VGroup(tex(r"M=72{,}5\ \mathrm{kg}", WHITE_, 40), tex(r"m_{bala}=4{,}20\ \mathrm{g}", WHITE_, 40),
                     tex(r"v_{bala}=965\ \mathrm{m/s}", VEL, 40)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(P3(4.2, 1.6))
        self.play(FadeIn(gelo), FadeIn(ca), FadeIn(arma), run_time=0.8)
        self.play(FadeIn(dad), run_time=0.8)
        self.ate(0.97)
        # C11-2 ----------------------------------------------------------------------------------------------
        self.an("C11-2")
        bala = Dot(P3(-2.2, -0.55), radius=0.07, color=WHITE_)
        e1 = Mc((r"V=\frac{0{,}00420\cdot965}{72{,}5}=0{,}0559\ \mathrm{m/s}", VEL), size=40, w=6.4).move_to(P3(4.2, -0.6))
        self.add(bala)
        self.play(bala.animate.shift(RIGHT * 3.6), run_time=0.7, rate_func=linear)
        vb = arrow(P3(-2.2, -0.2), P3(-0.6, -0.2), color=VEL, width=6)
        self.play(FadeIn(vb), VGroup(ca, arma).animate.shift(LEFT * 0.5), run_time=1.2)
        vr = arrow(P3(-4.7, 0.4), P3(-5.7, 0.4), color=VEL, width=5)
        vrl = tex(r"V", VEL, 38).next_to(vr, UP, buff=0.1)
        self.play(GrowArrow(vr), FadeIn(vrl), FadeIn(e1, shift=0.1 * UP), run_time=1.0)
        self.ate(0.97)
        # C11-3 ----------------------------------------------------------------------------------------------
        self.an("C11-3")
        self.play(*[FadeOut(m) for m in (bala, vb, vr, vrl, e1, ca, arma, dad)], run_time=0.5)
        ca = Pessoa(GEO, esc=0.8).pose(-4.0, -2.4, None)
        ang = math.radians(56)
        d = np.array([math.cos(ang), math.sin(ang), 0.0])
        a0 = P3(-3.9, -0.55)
        arma = Line(a0, a0 + 1.5 * d).set_stroke(mix(STEEL, 0.3), 7)
        self.play(FadeIn(ca), FadeIn(arma), run_time=0.7)
        bala = Dot(a0 + 1.5 * d, radius=0.07, color=WHITE_)
        self.add(bala)
        self.play(bala.animate.shift(d * 2.0), run_time=0.7, rate_func=linear)
        nn = ValueTracker(0.01)
        na = always_redraw(lambda: arrow(P3(-4.0, -2.4), P3(-4.0, -2.4 + 2.2 * nn.get_value()), color=FC, width=7, tip=0.22)
                           if nn.get_value() > 0.05 else VMobject())
        nl = tex(r"\vec N", FC, 44).move_to(P3(-3.4, -1.5))
        self.add(na)
        self.play(nn.animate.set_value(1.0), FadeIn(nl), run_time=1.2)
        q = txt("QUEM SEGUROU O CAÇADOR?", T_LAB, color=WHITE_).move_to(P3(4.2, 1.2))
        self.play(FadeIn(q), run_time=0.6)
        self.ate(0.97)
        # C11-4 ----------------------------------------------------------------------------------------------
        self.an("C11-4")
        py = linha(tex(r"P_y", MAG, 40), txt("NÃO SE CONSERVA", T_LAB), buff=0.25).move_to(P3(4.2, 2.2))
        px = linha(tex(r"P_x", MAG, 40), txt("SE CONSERVA", T_LAB), buff=0.25).move_to(P3(4.2, 1.1))
        ev = Mc((r"V=0{,}0559\,\cos 56^\circ=0{,}031\ \mathrm{m/s}", VEL), size=40, w=6.4).move_to(P3(4.2, -0.4))
        self.play(FadeOut(q), run_time=0.3)
        self.play(FadeIn(py), run_time=0.8)
        self.ate(0.4)
        self.play(FadeIn(px), run_time=0.8)
        self.ate(0.65)
        self.play(FadeIn(ev, shift=0.1 * UP), run_time=0.9)
        na.clear_updaters()
        self.ate(0.97)

    # ── C12 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def c12(self):
        self.clear(rt=0.6)
        self.secao("EXERCÍCIO 8 · OS GASES DO RIFLE", "SEARS · EXERC. 8.17")
        self.an("C12-1")
        chao = Line(P3(-7.4, -1.2), P3(0.6, -1.2)).set_stroke(GEO, 2.5, opacity=0.55)
        rifle = VGroup(RoundedRectangle(corner_radius=0.05, width=2.4, height=0.28), RoundedRectangle(corner_radius=0.05, width=0.6, height=0.5)) \
            .set_stroke(mix(STEEL, 0.5), 2).set_fill(STEEL, 1.0)
        rifle[1].move_to(P3(-4.4, -0.85))
        rifle[0].move_to(P3(-3.1, -0.78))
        rifle = rifle.move_to(P3(-3.4, -0.8))
        bala = Dot(P3(-2.0, -0.78), radius=0.07, color=WHITE_)
        dad = VGroup(tex(r"m_{rifle}=2{,}80\ \mathrm{kg}", WHITE_, 38), tex(r"m_{bala}=7{,}20\ \mathrm{g}", WHITE_, 38),
                     Mc((r"601\ \mathrm{m/s}", VEL), size=38), Mc((r"1{,}85\ \mathrm{m/s}", VEL), size=38)) \
            .arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(P3(3.2, 1.3))
        rot3 = txt("EM RELAÇÃO AO CANO", 18, color=DIM).next_to(dad[2], RIGHT, buff=0.2)
        rot4 = txt("RECUO EM RELAÇÃO AO CHÃO", 18, color=DIM).next_to(dad[3], RIGHT, buff=0.2)
        self.play(FadeIn(chao), FadeIn(rifle), FadeIn(bala), run_time=0.8)
        self.play(FadeIn(dad[0]), FadeIn(dad[1]), run_time=0.7)
        self.ate(0.4)
        self.play(FadeIn(dad[2]), FadeIn(rot3), run_time=0.7)
        self.play(FadeIn(dad[3]), FadeIn(rot4), run_time=0.7)
        self.ate(0.97)
        # C12-2 ----------------------------------------------------------------------------------------------
        self.an("C12-2")
        self.play(FadeOut(dad), FadeOut(rot3), FadeOut(rot4), run_time=0.4)
        self.play(bala.animate.shift(RIGHT * 3.4), rifle.animate.shift(LEFT * 0.4), run_time=0.9, rate_func=linear)
        e1 = Mc((r"v_{bala}=601-1{,}85=599{,}15\ \mathrm{m/s}", VEL), size=36, w=6.6).move_to(P3(3.6, 2.4))
        self.play(FadeIn(e1, shift=0.1 * UP), run_time=0.8)
        k = 0.5
        o = P3(-2.2, 1.5)
        pb = arrow(o, o + P3(4.31 * k, 0), color=MAG, width=7)
        pr = arrow(o, o + P3(-5.18 * k, 0), color=MAG, width=7)
        lb = Mc((r"p_{bala}=+4{,}31", MAG), size=32).next_to(pb, UP, buff=0.12).shift(RIGHT * 0.3)
        lr = Mc((r"p_{rifle}=-5{,}18", MAG), size=32).next_to(pr, UP, buff=0.12).shift(LEFT * 0.3)
        un = tex(r"\mathrm{kg\cdot m/s}", MAG, 30).move_to(P3(3.6, 1.2))
        self.ate(0.4)
        self.play(GrowArrow(pb), FadeIn(lb), run_time=0.8)
        self.play(GrowArrow(pr), FadeIn(lr), FadeIn(un), run_time=0.8)
        self.ate(0.97)
        # C12-3 ----------------------------------------------------------------------------------------------
        self.an("C12-3")
        falta = txt("AS SETAS NÃO SE CANCELAM", T_SMALL, color=APAGADO).move_to(P3(3.6, 0.3))
        self.play(FadeIn(falta), run_time=0.6)
        gases = VGroup(*[Circle(radius=0.18 + 0.05 * (k % 3)).set_stroke(WHITE_, 1.5, opacity=0.5).set_fill(WHITE_, 0.12)
                         .move_to(P3(-1.6 + 0.3 * k, -0.45 + 0.17 * math.sin(2.1 * k))) for k in range(8)])
        pg = arrow(P3(-1.6, -0.2), P3(-1.0, -0.2), color=MAG, width=6, tip=0.15)
        lg = Mc((r"p_{gases}=+0{,}866", MAG), size=30).next_to(gases, UP, buff=0.3)
        zero = Mc((r"\sum\vec p=0", MAG), size=44).move_to(P3(3.6, -1.2))
        self.ate(0.35)
        self.play(FadeIn(gases), GrowArrow(pg), FadeIn(lg), run_time=1.0)
        self.play(FadeOut(falta), FadeIn(zero, shift=0.1 * UP), run_time=0.8)
        self.ate(0.97)
        # C12-4 ----------------------------------------------------------------------------------------------
        self.an("C12-4")
        sis = txt("SISTEMA = BALA + RIFLE + GASES", T_MAIN, bold=True).move_to(P3(0, -3.2))
        self.play(FadeIn(sis, shift=0.1 * UP), run_time=0.9)
        self.ate(0.97)

    # ── C13-1 ───────────────────────────────────────────────────────────────────────────────────────────────
    def c13_1(self):
        self.clear(rt=0.6)
        self.secao("EXERCÍCIO 9 · NEWTON E A LUZ", "MOYSÉS · PROB. 9.2")
        self.an("C13-1")
        mold = RoundedRectangle(corner_radius=0.15, width=2.6, height=3.2).set_stroke(GEO, 2).set_fill(WHITE_, 0.04).move_to(P3(-5.2, 0.2))
        cab = Circle(radius=0.55).set_stroke(mix(STEEL, 0.5), 2).set_fill(STEEL, 1.0).move_to(P3(-5.2, 0.8))
        peruca = VGroup(*[Arc(radius=0.62 + 0.05 * i, start_angle=PI * 0.9, angle=-PI * 0.8 if False else PI * 1.2,
                              arc_center=P3(-5.2, 0.75)).set_stroke(GEO, 3) for i in range(3)])
        ombros = Arc(radius=1.0, start_angle=0, angle=PI, arc_center=P3(-5.2, -1.0)).set_stroke(mix(STEEL, 0.5), 2).set_fill(STEEL, 1.0)
        retrato = VGroup(mold, ombros, cab, peruca)
        sec = txt("SÉCULO XVII", T_MAIN, bold=True).move_to(P3(-5.2, -2.1))
        luz = Line(P3(-3.0, 0.2), P3(7.0, 0.2)).set_stroke(WHITE_, 1.5, opacity=0.35)
        fl = fluxo_pontos(self, -3.0, 7.0, 0.2, n=18, v=2.0)
        lab = txt("RAIO DE LUZ = FLUXO DE CORPÚSCULOS", T_SMALL, color=DIM).move_to(P3(2.2, -0.7))
        self.play(FadeIn(retrato), FadeIn(sec), run_time=0.9)
        self.ate(0.3)
        self.play(FadeIn(luz), run_time=0.5)
        self.add(fl)
        self.play(FadeIn(lab), run_time=0.7)
        self.ate(0.97)
        fl.clear_updaters()
