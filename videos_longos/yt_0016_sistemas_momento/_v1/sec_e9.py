"""Lote Q9: E9 — Newton e a luz (Moysés, problema 9.2). Impulso normal: reflexão θ1′ = θ1; refração: a componente tangencial se conserva →
v1 sen θ1 = v2 sen θ2; no modelo de Newton sen θ1/sen θ2 = v2/v1 (nunca "= n12"); Foucault, 1850; ondulatória: sen θ1/sen θ2 = v1/v2.
Referência numérica: n = 1,33, 45° → 32,1°."""
from kit import *  # noqa: F401,F403

N_AGUA = 1.33
T1 = math.radians(45.0)
T2 = math.asin(math.sin(T1) / N_AGUA)
assert abs(math.degrees(T2) - 32.1) < 0.05
XR = 3.9
SEN = r"\,\mathrm{sen}\,"


def num(s, cor=WHITE_, size=M_LAB):
    return MathTex(s, font_size=size, color=cor)


def retrato(c):
    """Retrato estilizado do século XVII (silhueta preenchida de perfil, peruca longa, gola), numa moldura."""
    g = VGroup(RoundedRectangle(corner_radius=0.15, width=2.7, height=3.3).set_stroke(GEO, 2.5).set_fill(PANEL, 0.6).move_to(c))
    capa = Polygon(c + P3(-1.15, -1.55), c + P3(-1.0, -0.75), c + P3(-0.45, -0.45), c + P3(0.45, -0.5), c + P3(1.0, -0.85),
                   c + P3(1.15, -1.55)).set_stroke(mix(STEEL, 0.4), 2).set_fill(escuro(STEEL, 0.1), 1)
    gola = Polygon(c + P3(-0.35, -0.5), c + P3(0.35, -0.5), c + P3(0.2, -0.85), c + P3(-0.2, -0.85)).set_stroke(width=0).set_fill(GEO, 1)
    peruca = VGroup(*[Ellipse(width=0.55, height=0.75).set_stroke(width=0).set_fill(GEO, 0.9).move_to(c + P3(x, y))
                      for x, y in ((-0.45, 0.65), (-0.55, 0.15), (-0.5, -0.3), (-0.15, 0.85), (0.15, 0.8), (-0.25, -0.35))])
    rosto = Ellipse(width=0.72, height=0.95).set_stroke(mix(STEEL, 0.4), 2).set_fill(STEEL, 1).move_to(c + P3(0.18, 0.3))
    nariz = Polygon(c + P3(0.5, 0.42), c + P3(0.66, 0.2), c + P3(0.5, 0.16)).set_stroke(width=0).set_fill(STEEL, 1)
    g.add(capa, peruca, rosto, nariz, gola)
    return g


def fluxo(sc, a, b, n=12, v=1.6, r=0.06, op=1.0):
    """Corpúsculos andando de a para b (função do relógio da cena)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    L = np.linalg.norm(b - a)
    u = (b - a) / L

    def make():
        g = VGroup()
        for k in range(n):
            s = (sc.clk.get_value() * v + k * L / n) % L
            g.add(Dot(a + s * u, radius=r, color=WHITE_).set_opacity(op).set_z_index(6))
        return g
    return always_redraw(make)


def arco_ang(o, a0, a1, r=0.7, cor=WHITE_):
    return Arc(radius=r, start_angle=a0, angle=a1 - a0, arc_center=o).set_stroke(cor, 2)


class LoteE9(Base):
    def construct(self):
        self.setup_base(cap="EXERCÍCIO 9 · NEWTON E A LUZ", selo="MOYSÉS · PROB. 9.2")
        self.e9_1()
        self.e9_2()
        self.e9_3()
        self.e9_4_5_6()
        self.e9_7()
        self.fim()
        self.relatorio()

    def e9_1(self):
        self.an("E9-1")
        rt = retrato(P3(-5.0, 0.0))
        sec = txt("SÉCULO XVII", 26, bold=True).move_to(P3(-5.0, -2.1))
        luz = Line(P3(-3.1, 0.2), P3(6.8, 0.2)).set_stroke(WHITE_, 1.5, opacity=0.3)
        fl = fluxo(self, P3(-3.1, 0.2), P3(6.8, 0.2), n=20, v=2.0)
        lab = linha("RAIO DE LUZ", mais(30, "="), "FLUXO DE CORPÚSCULOS", size=20, color=DIM, buff=0.14).move_to(P3(1.9, -0.55))
        self.play(FadeIn(rt), FadeIn(sec), run_time=0.9)
        self.ate(0.35)
        self.play(FadeIn(luz), FadeIn(fl), run_time=0.7)
        self.play(FadeIn(lab), run_time=0.6)
        q = txt("O IMPULSO EXPLICA REFLEXÃO E REFRAÇÃO?", 22, bold=True).move_to(P3(1.9, -1.6))
        self.ate(0.72)
        self.play(FadeIn(q, shift=0.1 * UP), run_time=0.7)
        self.ate(0.97)
        fl.clear_updaters()
        self.clear(rt=0.6)

    def e9_2(self):
        self.an("E9-2")
        O, Y = P3(-3.2, -1.2), -1.2
        esp = VGroup(Rectangle(width=6.0, height=0.14).set_stroke(width=0).set_fill(GEO, 0.9).move_to(P3(-3.2, Y - 0.07)))
        for x in np.arange(-6.0, -0.3, 0.3):
            esp.add(Line(P3(x, Y - 0.16), P3(x - 0.22, Y - 0.4)).set_stroke(DIM, 1.5, opacity=0.6))
        le = txt("ESPELHO", 18, color=DIM).move_to(P3(-5.6, Y - 0.65))
        nrm = DashedLine(O + P3(0, -0.6), O + P3(0, 3.0), dash_length=0.08).set_stroke(WHITE_, 1.5, opacity=0.6)
        ln = txt("NORMAL", 14, color=DIM).next_to(nrm, UP, buff=0.05)
        th = math.radians(40)
        L = 3.0
        A = O + L * P3(-math.sin(th), math.cos(th))
        B = O + L * P3(math.sin(th), math.cos(th))
        r1 = Line(A, O).set_stroke(WHITE_, 1.2, opacity=0.35)
        r2 = Line(O, B).set_stroke(WHITE_, 1.2, opacity=0.35)
        self.play(FadeIn(esp), FadeIn(le), Create(nrm), FadeIn(ln), FadeIn(r1), FadeIn(r2), run_time=0.9)
        s = ValueTracker(0.0)

        def corp():
            u = s.get_value()
            c = A + (O - A) * min(u, 1) * 1.0 if u <= 1 else O + (B - O) * (u - 1)
            return bola(0.1, GEO).move_to(c)
        cp = always_redraw(corp)
        self.add(cp)
        self.play(s.animate.set_value(1.0), run_time=1.4, rate_func=linear)
        # decomposição antes (no ponto) e depois; impulso normal
        v = 1.6
        vt, vn = v * math.sin(th), v * math.cos(th)
        p0 = O + P3(-2.2, 1.1)
        antes = VGroup(arrow(p0, p0 + P3(vt, 0), color=VEL, width=5, tip=0.14), arrow(p0, p0 + P3(0, -vn), color=VEL, width=5, tip=0.14),
                       num(r"v_t", VEL, 28).next_to(p0 + P3(vt / 2, 0), UP, buff=0.08),
                       num(r"v_n", VEL, 28).next_to(p0 + P3(0, -vn / 2), LEFT, buff=0.08), txt("ANTES", 14, color=DIM).next_to(p0, UP, buff=0.32))
        p1 = O + P3(2.3, 0.25)
        depois = VGroup(arrow(p1, p1 + P3(vt, 0), color=VEL, width=5, tip=0.14), arrow(p1, p1 + P3(0, vn), color=VEL, width=5, tip=0.14),
                        num(r"v_t", VEL, 28).next_to(p1 + P3(vt / 2, 0), DOWN, buff=0.08),
                        num(r"v_n", VEL, 28).next_to(p1 + P3(0, vn / 2), RIGHT, buff=0.08),
                        txt("DEPOIS", 14, color=DIM).next_to(p1 + P3(vt / 2, vn), UP, buff=0.12))
        imp = arrow(O + P3(0.0, 0.05), O + P3(0, 1.3), color=JC, width=8, tip=0.22, z=11)
        limp = linha(tex(r"\vec J", JC, 34), "NORMAL", size=16, color=JC, buff=0.1).next_to(imp, UP, buff=0.1)
        self.play(GrowArrow(imp), FadeIn(limp), FadeIn(antes), run_time=0.9)
        self.ate(0.45)
        self.play(s.animate.set_value(2.0), FadeIn(depois), run_time=1.4, rate_func=linear)
        a1 = arco_ang(O, PI / 2, PI / 2 + th, 0.85)
        a2 = arco_ang(O, PI / 2 - th, PI / 2, 0.85)
        lt1 = num(r"\theta_1", WHITE_, 30).move_to(O + 1.15 * P3(-math.sin(th / 2), math.cos(th / 2)))
        lt2 = num(r"\theta_1'", WHITE_, 30).move_to(O + 1.15 * P3(math.sin(th / 2), math.cos(th / 2)))
        self.play(Create(a1), Create(a2), FadeIn(lt1), FadeIn(lt2), run_time=0.8)
        r_t = txt("TANGENCIAL: IGUAL", 24).move_to(P3(XR, 1.3))
        r_n = txt("NORMAL: INVERTIDA", 24).move_to(P3(XR, 0.65))
        r_a = num(r"\theta_1'=\theta_1", WHITE_, 56).move_to(P3(XR, -0.5))
        self.ate(0.6)
        self.play(FadeIn(r_t), run_time=0.5)
        self.play(FadeIn(r_n), run_time=0.5)
        self.ate(0.8)
        self.play(FadeIn(r_a, shift=0.1 * UP), run_time=0.7)
        self.ate(0.97)
        cp.clear_updaters()
        self.clear(rt=0.6)

    def e9_3(self):
        self.an("E9-3")
        Y = -0.5
        O = P3(-3.3, Y)
        self.O = O
        agua = Rectangle(width=7.4, height=3.1).set_stroke(width=0).set_fill(BLUE_L, 0.14).move_to(P3(-3.6, Y - 1.55))
        sup = Line(P3(-7.3, Y), P3(0.1, Y)).set_stroke(mix(BLUE_L, 0.3), 2.5)
        lar = txt("AR", 20, color=DIM).move_to(P3(-6.6, Y + 0.4))
        lag = txt("ÁGUA", 20, color=mix(BLUE_L, 0.3)).move_to(P3(-6.4, Y - 0.4))
        nrm = DashedLine(O + P3(0, -2.9), O + P3(0, 3.0), dash_length=0.08).set_stroke(WHITE_, 1.5, opacity=0.6)
        L = 2.9
        A = O + L * P3(-math.sin(T1), math.cos(T1))
        B = O + L * P3(math.sin(T2), -math.cos(T2))
        r1 = Line(A, O).set_stroke(WHITE_, 1.2, opacity=0.35)
        r2 = Line(O, B).set_stroke(WHITE_, 1.2, opacity=0.35)
        self.play(FadeIn(agua), Create(sup), FadeIn(lar), FadeIn(lag), Create(nrm), FadeIn(r1), FadeIn(r2), run_time=1.0)
        f1 = fluxo(self, A, O, n=5, v=1.4, r=0.07)
        f2 = fluxo(self, O, B, n=5, v=1.4 * N_AGUA, r=0.07)
        self.add(f1, f2)
        # componentes: tangencial igual; normal cresce (modelo de Newton: v2 = 1,33 v1)
        v = 1.5
        vt, vn1 = v * math.sin(T1), v * math.cos(T1)
        vn2 = v * N_AGUA * math.cos(T2)
        p0 = O + P3(-2.6, 1.6)
        c1 = VGroup(arrow(p0, p0 + P3(vt, 0), color=VEL, width=5, tip=0.14), arrow(p0, p0 + P3(0, -vn1), color=VEL, width=5, tip=0.14),
                    num(r"v_t", VEL, 28).next_to(p0 + P3(vt / 2, 0), UP, buff=0.08),
                    num(r"v_{n}", VEL, 28).next_to(p0 + P3(0, -vn1 / 2), LEFT, buff=0.08))
        p1 = O + P3(1.0, -0.35)
        c2 = VGroup(arrow(p1, p1 + P3(vt, 0), color=VEL, width=5, tip=0.14), arrow(p1, p1 + P3(0, -vn2), color=VEL, width=5, tip=0.14),
                    num(r"v_t", VEL, 28).next_to(p1 + P3(vt / 2, 0), UP, buff=0.08),
                    num(r"v_{n}", VEL, 28).next_to(p1 + P3(0, -vn2 / 2), RIGHT, buff=0.08))
        imp = arrow(O + P3(0.0, -0.05), O + P3(0, -1.0), color=JC, width=8, tip=0.22, z=11)
        limp = linha(tex(r"\vec J", JC, 34), "NORMAL", size=16, color=JC, buff=0.1).next_to(imp, LEFT, buff=0.15)
        self.ate(0.15)
        self.play(GrowArrow(imp), FadeIn(limp), run_time=0.8)
        self.ate(0.35)
        self.play(FadeIn(c1), run_time=0.7)
        self.play(FadeIn(c2), run_time=0.7)
        nt = txt("A TANGENCIAL SE CONSERVA", 20, color=VEL).move_to(P3(XR, 1.6))
        self.play(FadeIn(nt), run_time=0.5)
        a1 = arco_ang(O, PI / 2, PI / 2 + T1, 0.8)
        a2 = arco_ang(O, -PI / 2, -PI / 2 + T2, 0.95)
        lt1 = num(r"\theta_1", WHITE_, 30).move_to(O + 1.1 * P3(-math.sin(T1 / 2), math.cos(T1 / 2)))
        lt2 = num(r"\theta_2", WHITE_, 30).move_to(O + 1.3 * P3(math.sin(T2 / 2), -math.cos(T2 / 2)))
        mn = txt("ÂNGULOS MEDIDOS DA NORMAL", 16, color=DIM).move_to(P3(XR, 0.95))
        self.ate(0.6)
        self.play(Create(a1), Create(a2), FadeIn(lt1), FadeIn(lt2), FadeIn(mn), run_time=0.9)
        e = num(r"v_1" + SEN + r"\theta_1=v_2" + SEN + r"\theta_2", WHITE_, 52).move_to(P3(XR, 0.0))
        self.ate(0.8)
        self.play(FadeIn(e, shift=0.1 * UP), run_time=0.9)
        self.ate(0.97)
        self.e_tan, self.nt, self.mn = e, nt, mn
        self.fluxos = (f1, f2)

    def e9_4_5_6(self):
        self.an("E9-4")
        e4 = Mc(r"\frac{" + SEN + r"\theta_1}{" + SEN + r"\theta_2}", "=", r"\text{constante}", size=52).move_to(P3(XR, -1.2))
        ls = txt("A FORMA DA LEI DE SNELL", 18, color=DIM).next_to(e4, DOWN, buff=0.2)
        self.play(FadeIn(e4, shift=0.1 * UP), FadeIn(ls), run_time=0.9)
        self.ate(0.5)
        e4b = Mc(r"\frac{" + SEN + r"\theta_1}{" + SEN + r"\theta_2}", "=", (r"\frac{v_2}{v_1}", VEL), size=52).move_to(P3(XR, -1.2))
        lnw = txt("NO MODELO DE NEWTON", 18, color=DIM).next_to(e4b, DOWN, buff=0.2)
        self.play(TransformMatchingTex(e4, e4b), FadeOut(ls), FadeIn(lnw), run_time=1.1)
        cx = SurroundingRectangle(e4b[2], buff=0.1, corner_radius=0.06).set_stroke(VEL, 2)
        self.play(Create(cx), run_time=0.5)
        self.ate(0.97)
        # E9-5 -----------------------------------------------------------------------------------------------
        self.an("E9-5")
        q1 = num(r"\theta_2<\theta_1", WHITE_, 44)
        q2 = num(r"\Rightarrow\ \frac{v_2}{v_1}>1", VEL, 44)
        VGroup(q1, q2).arrange(RIGHT, buff=0.4).move_to(P3(XR, -2.7))
        perto = txt("SE APROXIMA DA NORMAL", 16, color=DIM).move_to(self.O + P3(1.8, -2.3))
        self.play(FadeIn(perto), run_time=0.5)
        self.ate(0.25)
        self.play(FadeIn(q1, shift=0.1 * UP), run_time=0.7)
        self.ate(0.5)
        self.play(FadeIn(q2, shift=0.1 * UP), run_time=0.7)
        nw = linha("NEWTON:", "LUZ MAIS RÁPIDA NA ÁGUA", size=22, buff=0.15)
        self.ate(0.75)
        self.play(FadeOut(self.nt), FadeOut(self.mn), run_time=0.3)
        nw.move_to(P3(XR, 1.4))
        self.play(FadeIn(nw, shift=0.1 * UP), run_time=0.7)
        self.ate(0.97)
        # E9-6 -----------------------------------------------------------------------------------------------
        self.an("E9-6")
        f1, f2 = self.fluxos
        self.play(FadeOut(self.e_tan), FadeOut(e4b), FadeOut(lnw), FadeOut(cx), FadeOut(q1), FadeOut(q2), FadeOut(nw), run_time=0.5)
        ano = txt("1850 · FOUCAULT", 36, bold=True).move_to(P3(XR, 1.6))
        lenta = txt("A LUZ É MAIS LENTA NA ÁGUA", 24).move_to(P3(XR, 0.95))
        ve = num(r"v_2>v_1", WHITE_, 50).move_to(P3(2.3, -0.4))
        nwp = txt("PREVISÃO DE NEWTON", 16, color=DIM).next_to(ve, DOWN, buff=0.18)
        self.ate(0.2)
        self.play(FadeIn(ve), FadeIn(nwp), run_time=0.6)
        self.ate(0.35)
        self.play(FadeIn(ano, shift=0.1 * UP), run_time=0.8)
        self.play(FadeIn(lenta, shift=0.1 * UP), run_time=0.7)
        # os corpúsculos na água passam a andar mais devagar
        f2.clear_updaters()
        self.remove(f2)
        B2 = self.O + 2.9 * P3(math.sin(T2), -math.cos(T2))
        f3 = fluxo(self, self.O, B2, n=5, v=1.4 / N_AGUA, r=0.07)
        self.add(f3)
        self.play(ve.animate.set_color(APAGADO), Create(risco(ve, w=6)), run_time=0.8)
        self.ate(0.68)
        ond = txt("DESCRIÇÃO ONDULATÓRIA", 18, color=DIM).move_to(P3(5.4, -0.95))
        eo = Mc(r"\frac{" + SEN + r"\theta_1}{" + SEN + r"\theta_2}", "=", (r"\frac{v_1}{v_2}", VEL), size=46).move_to(P3(5.4, -0.15))
        self.play(FadeIn(eo, shift=0.1 * UP), FadeIn(ond), run_time=0.9)
        self.ate(0.97)
        f1.clear_updaters()
        f3.clear_updaters()

    def e9_7(self):
        self.an("E9-7")
        self.clear(rt=0.6)
        a = txt("IMPULSO CERTO", 46, bold=True)
        b = linha(mais(56), txt("MODELO ERRADO", 46, bold=True, color=APAGADO), buff=0.25)
        c = linha(mais(56, "="), txt("PREVISÃO TESTÁVEL", 46, bold=True, color=CYAN), buff=0.25)
        VGroup(a, b, c).arrange(DOWN, buff=0.4).move_to(P3(-0.6, 0.6))
        self.play(FadeIn(a, shift=0.1 * UP), run_time=0.8)
        self.ate(0.3)
        self.play(FadeIn(b, shift=0.1 * UP), run_time=0.8)
        self.ate(0.55)
        self.play(FadeIn(c, shift=0.1 * UP), run_time=0.8)
        self.ate(0.68)
        d = dica("O IMPULSO É NORMAL: SÓ A COMPONENTE", "NORMAL DA VELOCIDADE MUDA")
        self.dica_entra(d)
        self.ate(0.97)
        self.dica_sai()
        self.clear(rt=0.5)
