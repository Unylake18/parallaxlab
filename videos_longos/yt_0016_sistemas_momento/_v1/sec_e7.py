"""Lote Q7: E7 — o caçador no lago (Sears, exercício 8.25). 72,5 kg; bala 4,20 g a 965 m/s. Horizontal: 0,0559 m/s. A 56°: só P_x
se conserva (a normal do gelo é externa, vertical e impulsiva): 0,0313 m/s. Energias 1.956 J × 0,113 J (razão ≈ 17.262)."""
from kit import *  # noqa: F401,F403

MC, MBALA, VBALA, ANG = 72.5, 0.00420, 965.0, math.radians(56.0)
V_H = MBALA * VBALA / MC
V_56 = V_H * math.cos(ANG)
KB, KCZ = MBALA * VBALA ** 2 / 2, MC * V_H ** 2 / 2
RAZ = MC / MBALA
assert abs(V_H - 0.0559) < 1e-4 and abs(V_56 - 0.0313) < 1e-4 and abs(KB - 1955.6) < 0.1 and abs(KCZ - 0.1133) < 1e-3
assert abs(KB / KCZ - RAZ) < 1e-6 * RAZ and round(RAZ) == 17262 and abs(KB / (KB + KCZ) - 0.999942) < 1e-6
Y_G = -1.6
XR = 3.9
XC = -4.6


def num(s, cor=WHITE_, size=M_LAB):
    return MathTex(s, font_size=size, color=cor)


def cacador(x, ang):
    """Caçador de perfil (para a direita) segurando o rifle no ângulo `ang`; devolve (pessoa, rifle, boca)."""
    if ang < 0.1:
        ex = dict(bf=1.25, af=1.62, bt=0.95, at=1.62)
    else:
        ex = dict(bf=1.7, af=PI / 2 + ang, bt=1.35, at=PI / 2 + ang)
    pe = PessoaPerfil(x, Y_G, 2.0, 1, "mira", extra=ex)
    o = pe.pts["ombro"] + P3(0.02, -0.12)
    rf, boca = rifle(ang, comp=1.55)
    rf.shift(o - P3(0.15 * math.cos(ang), 0.15 * math.sin(ang)))
    return pe, rf, boca + o - P3(0.15 * math.cos(ang), 0.15 * math.sin(ang))


class LoteE7(Base):
    def construct(self):
        self.setup_base(cap="EXERCÍCIO 7 · O CAÇADOR NO LAGO", selo="SEARS · EX. 8.25")
        self.e7_1_2()
        self.e7_3_4()
        self.e7_5()
        self.fim()
        self.relatorio()

    def e7_1_2(self):
        self.an("E7-1")
        gl = gelo(-7.3, 0.4, Y_G)
        lg = txt("LAGO CONGELADO · SEM ATRITO", 16, color=mix(GELO, 0.3)).move_to(P3(-1.6, Y_G - 0.5))
        pe, rf, boca = cacador(XC, 0.0)
        fr = fronteira(5.0, 3.5, P3(XC + 0.4, Y_G + 1.65), rotulo=["CAÇADOR", tex("+", WHITE_, 28), "ARMA", tex("+", WHITE_, 28), "BALA"])
        dados = VGroup(num(r"M=72{,}5\ \mathrm{kg}"), num(r"m=4{,}20\ \mathrm{g}"), num(r"v=965\ \mathrm{m/s}", VEL)) \
            .arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(P3(XR, 1.5))
        self.play(FadeIn(gl), FadeIn(lg), FadeIn(pe), FadeIn(rf), run_time=0.9)
        self.play(Create(fr[0]), FadeIn(fr[1]), run_time=0.9)
        self.ate(0.3)
        self.play(LaggedStart(*[FadeIn(d, shift=0.1 * UP) for d in dados], lag_ratio=0.3), run_time=1.4)
        self.ate(0.97)
        # E7-2: tiro horizontal --------------------------------------------------------------------------------
        self.an("E7-2")
        bl = bala_mob().move_to(boca)
        self.add(bl)
        self.play(Flash(boca, color=WHITE_, line_length=0.18, num_lines=10, flash_radius=0.15, run_time=0.3),
                  bl.animate.shift(RIGHT * 5.0), run_time=0.5, rate_func=linear)
        self.remove(bl)
        vb = arrow(boca + P3(0.2, 0.35), boca + P3(1.6, 0.35), color=VEL, width=6, tip=0.17)
        lvb = num(r"965\ \mathrm{m/s}", VEL, 28).next_to(vb, UP, buff=0.08)
        rec = VGroup(pe, rf)
        vr = arrow(P3(XC - 0.2, Y_G + 2.45), P3(XC - 1.3, Y_G + 2.45), color=VEL, width=6, tip=0.17)
        lvr = num(r"V", VEL, 40).next_to(vr, LEFT, buff=0.12)
        self.play(GrowArrow(vb), FadeIn(lvb), rec.animate.shift(LEFT * 0.3), GrowArrow(vr), FadeIn(lvr), run_time=1.2)
        e1 = num(r"V=\frac{0{,}00420\cdot 965}{72{,}5}=0{,}0559\ \mathrm{m/s}", VEL, 40).move_to(P3(XR, -0.6))
        z = Mc((r"P_{antes}=P_{depois}=0", MAG), size=34).move_to(P3(XR, -1.55))
        self.ate(0.3)
        self.play(FadeIn(z), run_time=0.6)
        self.play(FadeIn(e1, shift=0.1 * UP), run_time=0.8)
        self.ate(0.97)
        self.e72 = VGroup(pe, rf, vb, lvb, vr, lvr, e1, z, dados)
        self.gl, self.lg, self.fr = gl, lg, fr

    def e7_3_4(self):
        self.an("E7-3")
        self.play(FadeOut(self.e72), run_time=0.5)
        pe, rf, boca = cacador(XC, ANG)
        self.play(FadeIn(pe), FadeIn(rf), run_time=0.6)
        d = np.array([math.cos(ANG), math.sin(ANG), 0.0])
        base = boca - 1.55 * d
        arco = Arc(radius=0.75, start_angle=0, angle=ANG, arc_center=base).set_stroke(WHITE_, 2)
        ref = DashedLine(base, base + P3(1.1, 0), dash_length=0.06).set_stroke(WHITE_, 1.5, opacity=0.6)
        la = num(r"56^\circ", WHITE_, 30).move_to(base + 1.05 * P3(math.cos(ANG / 2), math.sin(ANG / 2)))
        self.play(Create(ref), Create(arco), FadeIn(la), run_time=0.7)
        bl = bala_mob(ANG).move_to(boca)
        self.add(bl)
        nn = ValueTracker(0.0)
        pes = P3(XC + 0.05, Y_G)
        na = always_redraw(lambda: arrow(pes + P3(0, -1.25), pes + P3(0, -1.25 + 1.2 * nn.get_value() + 0.05), color=FC, width=8, tip=0.22, z=11)
                           if nn.get_value() > 0.04 else VMobject())
        ln = num(r"\vec N", FC, 40).move_to(pes + P3(0.55, -0.7))
        self.add(na)
        self.play(bl.animate.shift(d * 4.0), nn.animate.set_value(1.0), run_time=0.45, rate_func=linear)
        self.remove(bl)
        self.play(FadeIn(ln), run_time=0.3)
        self.play(nn.animate.set_value(0.35), run_time=1.0)
        q = txt("QUEM SEGUROU ELE?", 26, bold=True).move_to(P3(XR, 1.5))
        self.ate(0.6)
        self.play(FadeIn(q), run_time=0.6)
        self.ate(0.97)
        # E7-4 -----------------------------------------------------------------------------------------------
        self.an("E7-4")
        lg2 = txt("O GELO: A NORMAL É EXTERNA E IMPULSIVA", 18, color=FC).move_to(P3(XR, 1.5))
        self.play(FadeOut(q), nn.animate.set_value(1.0), run_time=0.35)
        self.play(FadeIn(lg2), run_time=0.35)
        self.play(nn.animate.set_value(0.35), run_time=0.6)
        py = linha(tex(r"P_y", MAG, 42), "NÃO SE CONSERVA", size=26, buff=0.2).move_to(P3(XR, 0.75))
        px = linha(tex(r"P_x", MAG, 42), "SE CONSERVA", size=26, buff=0.2).move_to(P3(XR, 0.05))
        # componentes do momento da bala na boca do cano
        k = 0.95
        cx_ = arrow(boca, boca + P3(k * math.cos(ANG), 0), color=MAG, width=5, tip=0.14, z=10)
        cy_ = arrow(boca + P3(k * math.cos(ANG), 0), boca + P3(k * math.cos(ANG), k * math.sin(ANG)), color=MAG, width=5, tip=0.14, z=10, op=0.5)
        pt_ = arrow(boca, boca + k * d, color=MAG, width=6, tip=0.16, z=10)
        lp = num(r"\vec p_{bala}", MAG, 30).next_to(boca + 0.6 * k * d, LEFT, buff=0.12)
        lx = num(r"p_x", MAG, 28).next_to(cx_, DOWN, buff=0.08)
        ly = num(r"p_y", MAG, 28).next_to(cy_, RIGHT, buff=0.08).set_opacity(0.6)
        self.ate(0.18)
        self.play(GrowArrow(pt_), FadeIn(lp), run_time=0.6)
        self.play(GrowArrow(cx_), GrowArrow(cy_), FadeIn(lx), FadeIn(ly), run_time=0.7)
        self.play(FadeIn(py, shift=0.1 * UP), run_time=0.7)
        self.ate(0.42)
        self.play(FadeIn(px, shift=0.1 * UP), run_time=0.7)
        self.ate(0.62)
        vr = arrow(P3(XC - 0.2, Y_G + 2.5), P3(XC - 0.85, Y_G + 2.5), color=VEL, width=6, tip=0.17)
        lvr = num(r"V", VEL, 40).next_to(vr, LEFT, buff=0.12)
        ev = num(r"V=0{,}0559\cdot\cos 56^\circ=0{,}031\ \mathrm{m/s}", VEL, 40).move_to(P3(XR, -0.95))
        self.play(VGroup(pe, rf).animate.shift(LEFT * 0.18), GrowArrow(vr), FadeIn(lvr), FadeIn(ev, shift=0.1 * UP), run_time=1.0)
        self.ate(0.97)
        na.clear_updaters()

    def e7_5(self):
        self.an("E7-5")
        self.clear(rt=0.6)
        th = txt("TIRO HORIZONTAL", 20, color=DIM).move_to(P3(XR, 2.0))
        # momentos iguais (magenta)
        yb = -2.6
        pb = Rectangle(width=0.6, height=2.0).set_stroke(width=0).set_fill(MAG, 0.75).move_to(P3(-6.0, yb + 1.0))
        pc = Rectangle(width=0.6, height=2.0).set_stroke(width=0).set_fill(MAG, 0.75).move_to(P3(-5.1, yb + 1.0))
        lpb, lpc = txt("BALA", 16, color=DIM).next_to(pb, DOWN, buff=0.1), txt("CAÇADOR", 16, color=DIM).next_to(pc, DOWN, buff=0.1)
        lm = txt("MOMENTO", 18, color=MAG).move_to(P3(-5.55, 1.0))
        vm = num(r"4{,}05\ \mathrm{kg\cdot m/s}", MAG, 24).move_to(P3(-5.55, 0.55))
        # energias em escala logarítmica (ciano): 10^-2 … 10^4 J
        x0, H = -3.2, 4.2
        y_of = lambda K: yb + H * (math.log10(K) + 2) / 6
        eixo = Line(P3(x0, yb), P3(x0, yb + H + 0.1)).set_stroke(DIM, 2)
        marcas = VGroup()
        for e in (-2, 0, 2, 4):
            y = y_of(10 ** e)
            marcas.add(Line(P3(x0 - 0.08, y), P3(x0 + 0.08, y)).set_stroke(DIM, 2),
                       num(rf"10^{{{e}}}", DIM, 24).next_to(P3(x0 - 0.1, y), LEFT, buff=0.1))
        eb = Rectangle(width=0.62, height=y_of(KB) - yb).set_stroke(width=0).set_fill(KC, 0.8).move_to(P3(-2.4, (y_of(KB) + yb) / 2))
        ec = Rectangle(width=0.62, height=y_of(KCZ) - yb).set_stroke(width=0).set_fill(KC, 0.8).move_to(P3(-1.5, (y_of(KCZ) + yb) / 2))
        leb = num(r"1.956\ \mathrm{J}", KC, 26).next_to(eb, UP, buff=0.08)
        lec = num(r"0{,}11\ \mathrm{J}", KC, 26).next_to(ec, UP, buff=0.08)
        lb2, lc2 = txt("BALA", 16, color=DIM).next_to(eb, DOWN, buff=0.1), txt("CAÇADOR", 16, color=DIM).next_to(ec, DOWN, buff=0.1)
        le = txt("ENERGIA (ESCALA LOG)", 18, color=KC).move_to(P3(-2.2, 2.2))
        lj = num(r"\mathrm{J}", DIM, 26).next_to(eixo, UP, buff=0.08)
        self.play(FadeIn(th), FadeIn(pb), FadeIn(pc), FadeIn(lpb), FadeIn(lpc), FadeIn(lm), FadeIn(vm), run_time=0.9)
        self.ate(0.18)
        self.play(FadeIn(eixo), FadeIn(marcas), FadeIn(le), FadeIn(lj), GrowFromEdge(eb, DOWN), FadeIn(leb), FadeIn(lb2), run_time=1.0)
        self.ate(0.4)
        self.play(GrowFromEdge(ec, DOWN), FadeIn(lec), FadeIn(lc2), run_time=0.8)
        r1 = num(r"\frac{K_{\text{bala}}}{K_{\text{caçador}}}\approx 17.262=\frac{72{,}5}{0{,}0042}", KC, 40).move_to(P3(XR, 1.1))
        r2 = linha(tex(r"\approx 99{,}994\%", KC, 44), "NA BALA", size=28, buff=0.2).move_to(P3(XR, 0.0))
        self.ate(0.52)
        self.play(FadeIn(r1, shift=0.1 * UP), run_time=0.9)
        self.ate(0.72)
        self.play(FadeIn(r2, shift=0.1 * UP), run_time=0.8)
        self.ate(0.82)
        d = dica("ISOLADO NA HORIZONTAL", "NÃO É ISOLADO NA VERTICAL")
        self.dica_entra(d)
        self.ate(0.97)
        self.dica_sai()
        self.clear(rt=0.5)
