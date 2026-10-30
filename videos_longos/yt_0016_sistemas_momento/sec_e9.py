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


SEPIA, SEPIA_E = "#C8B8A0", "#17161A"          # v7: gravura em tom sépia frio (linha fina sobre fundo escuro)


def _elipse(c, w, h, n=40):
    return [c + P3(w / 2 * math.cos(2 * PI * k / n), h / 2 * math.sin(2 * PI * k / n)) for k in range(n)]


def hachura(polys, ang, passo, cor=SEPIA, w=1.0, op=0.55):
    """Hachura de gravura: linhas paralelas (ângulo `ang`) recortadas pela união par-ímpar dos polígonos (varredura)."""
    ca, sa = math.cos(ang), math.sin(ang)
    rot = lambda q: (q[0] * ca + q[1] * sa, -q[0] * sa + q[1] * ca)
    des = lambda u, v: P3(u * ca - v * sa, u * sa + v * ca)
    arestas = []
    for pts in polys:
        r = [rot(q) for q in pts]
        arestas += [(r[k], r[(k + 1) % len(r)]) for k in range(len(r))]
    vs = [a[1] for e in arestas for a in e]
    g = VGroup()
    v = min(vs) + passo / 2
    while v < max(vs):
        xs = sorted(a[0] + (v - a[1]) * (b[0] - a[0]) / (b[1] - a[1]) for a, b in arestas if (a[1] - v) * (b[1] - v) < 0)
        for k in range(0, len(xs) - 1, 2):
            g.add(Line(des(xs[k], v), des(xs[k + 1], v)).set_stroke(cor, w, op))
        v += passo
    return g


def retrato(c):
    """v7: retrato estilizado do século XVII em gravura (linha fina, sépia frio, hachura cruzada), de perfil, peruca longa, gola."""
    g = VGroup(RoundedRectangle(corner_radius=0.15, width=2.7, height=3.3).set_stroke(SEPIA, 2.2, 0.9).set_fill(SEPIA_E, 0.92).move_to(c))
    g.add(RoundedRectangle(corner_radius=0.1, width=2.45, height=3.05).set_stroke(SEPIA, 0.8, 0.5).move_to(c))
    capa = [c + P3(-1.15, -1.45), c + P3(-1.0, -0.75), c + P3(-0.45, -0.45), c + P3(0.45, -0.5), c + P3(1.0, -0.85), c + P3(1.15, -1.45)]
    gola = [c + P3(-0.35, -0.5), c + P3(0.35, -0.5), c + P3(0.2, -0.85), c + P3(-0.2, -0.85)]
    cachos = [_elipse(c + P3(x, y), 0.55, 0.75) for x, y in ((-0.45, 0.65), (-0.55, 0.15), (-0.5, -0.3), (-0.15, 0.85), (0.15, 0.8), (-0.25, -0.35))]
    rosto = _elipse(c + P3(0.18, 0.3), 0.72, 0.95)
    nariz = [c + P3(0.5, 0.42), c + P3(0.66, 0.2), c + P3(0.5, 0.16)]
    g.add(hachura([capa], 0.6, 0.075), hachura([capa], -0.6, 0.11, op=0.35))            # capa: hachura cruzada (sombra)
    for e in cachos:
        g.add(hachura([e], 1.1, 0.07, op=0.45))
        g.add(VMobject().set_points_smoothly(e + [e[0]]).set_stroke(SEPIA, 1.2, 0.85))
    g.add(hachura([rosto], 0.25, 0.11, op=0.25), hachura([gola], 0.0, 0.06, op=0.3))
    for poly in (capa, gola, nariz):
        g.add(Polygon(*poly).set_stroke(SEPIA, 1.4, 0.95).set_fill(opacity=0))
    g.add(VMobject().set_points_smoothly(rosto + [rosto[0]]).set_stroke(SEPIA, 1.4, 0.95))
    g.add(Dot(c + P3(0.33, 0.42), radius=0.03, color=SEPIA))                                  # olho
    return g


def caixa_dec(g):
    """v7: a decomposição numa caixa própria (painel escuro, borda violeta fina), afastada do raio."""
    return SurroundingRectangle(g, buff=0.16, corner_radius=0.1).set_stroke(VEL, 1, 0.35).set_fill("#081028", 0.62).set_z_index(-1)


def fluxo(sc, a, b, n=12, v=1.6, r=0.06, op=1.0):
    """Corpúsculos andando de a para b (função do relógio da cena)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    L = np.linalg.norm(b - a)
    u = (b - a) / L

    def make():
        g = VGroup()
        for k in range(n):
            s = (sc.clk.get_value() * v + k * L / n) % L
            g.add(Line(a + max(0.0, s - 0.32) * u, a + s * u).set_stroke(LUZ, 3, 0.3 * op).set_z_index(5))   # v7: rastro curto
            g.add(ponto_luz(a + s * u, r, op).set_z_index(6))          # v4: a luz é sempre amarela (LUZ)
        return g
    return always_redraw(make)


def fluxo_esp(sc, a, b, esp, v, r=0.07, op=1.0):
    """v6 (1.2): corpúsculos com espaçamento `esp` (mesmo ritmo de chegada: mais rápido = mais espaçado)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    L = np.linalg.norm(b - a)
    u = (b - a) / L
    n = int(math.ceil(L / esp)) + 1

    def make():
        g = VGroup()
        for k in range(n):
            s_ = (sc.clk.get_value() * v + k * esp) % (n * esp)
            if s_ < L:
                g.add(Line(a + max(0.0, s_ - 0.32) * u, a + s_ * u).set_stroke(LUZ, 3, 0.3 * op).set_z_index(5))
                g.add(ponto_luz(a + s_ * u, r, op).set_z_index(6))
        return g
    return always_redraw(make)


LR = 3.4                       # v6 (1.6): raios do E9 ×1,2 (diagramas maiores)


def arco_ang(o, a0, a1, r=0.7, cor=WHITE_):
    return Arc(radius=r, start_angle=a0, angle=a1 - a0, arc_center=o).set_stroke(cor, 2)


class LoteE9(Base):
    def construct(self):
        self.setup_base(cap="EXERCÍCIO 9 · NEWTON E A LUZ", selo="IMPULSO NORMAL")
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
        self.diz("No fim do século dezessete")
        self.play(Indicate(sec, color=WHITE_), run_time=0.8)
        self.diz("feita de corpúsculos")
        self.play(FadeIn(luz), FadeIn(fl), run_time=0.7)
        self.diz("bolinhas minúsculas")
        self.play(FadeIn(lab), run_time=0.6)
        q = txt("O IMPULSO EXPLICA REFLEXÃO E REFRAÇÃO?", 22, bold=True).move_to(P3(1.9, -1.6))
        self.diz("Será que o impulso")
        self.play(FadeIn(q, shift=0.1 * UP), run_time=0.7)
        self.ate(0.97)
        fl.clear_updaters()
        self.virada(tudo=True)               # v4: virada em sequência (sai tudo, depois entra o novo)

    def e9_2(self):
        self.an("E9-2")
        O, Y = P3(-3.2, -1.2), -1.2
        esp = VGroup(Rectangle(width=6.0, height=0.14).set_stroke(width=0).set_fill(color=[STEEL, WHITE_, GEO, STEEL], opacity=0.95)
                     .set_sheen_direction(RIGHT).move_to(P3(-3.2, Y - 0.07)),                    # v7 (2D+): metal com reflexo em degradê
                     Line(P3(-6.2, Y), P3(-0.2, Y)).set_stroke(WHITE_, 1.5, 0.8),
                     Rectangle(width=6.0, height=0.5).set_stroke(width=0).set_fill(color=[GEO, BACKGROUND_COLOR], opacity=0.16)
                     .set_sheen_direction(DOWN).move_to(P3(-3.2, Y - 0.39)))
        for x in np.arange(-6.0, -0.3, 0.3):
            esp.add(Line(P3(x, Y - 0.16), P3(x - 0.22, Y - 0.4)).set_stroke(DIM, 1.5, opacity=0.6))
        le = txt("ESPELHO", 18, color=DIM).move_to(P3(-5.6, Y - 0.65))
        nrm = DashedLine(O + P3(0, -0.6), O + P3(0, 3.5), dash_length=0.08).set_stroke(WHITE_, 1.5, opacity=0.6)
        ln = txt("NORMAL", 14, color=DIM).next_to(nrm, UP, buff=0.05)
        th = math.radians(40)
        L = 3.6
        A = O + L * P3(-math.sin(th), math.cos(th))
        B = O + L * P3(math.sin(th), math.cos(th))
        r1 = Line(A, O).set_stroke(WHITE_, 1.2, opacity=0.35)
        r2 = Line(O, B).set_stroke(WHITE_, 1.2, opacity=0.35)
        f0 = fluxo(self, A, O, n=8, v=1.3, r=0.09, op=0.45)              # v6 (palco vivo): o raio já chega desde o começo
        self.play(FadeIn(esp), FadeIn(le), Create(nrm), FadeIn(ln), FadeIn(r1), FadeIn(r2), FadeIn(f0), run_time=0.9)
        s = ValueTracker(0.0)

        def corp():
            u = s.get_value()
            c = A + (O - A) * min(u, 1) * 1.0 if u <= 1 else O + (B - O) * (u - 1)
            return ponto_luz(c, 0.1)
        cp = always_redraw(corp)
        self.add(cp)
        self.diz("O espelho só consegue empurrar")
        self.play(s.animate.set_value(1.0), run_time=1.4, rate_func=linear)
        # decomposição antes (no ponto) e depois; impulso normal
        v = 1.6
        vt, vn = v * math.sin(th), v * math.cos(th)
        p0 = O + P3(-2.8, 1.6)                          # v6 (N4): fora do raio e acima do espelho
        antes = VGroup(arrow(p0, p0 + P3(vt, 0), color=VEL, width=5, tip=0.14), arrow(p0, p0 + P3(0, -vn), color=VEL, width=5, tip=0.14),
                       num(r"v_t", VEL, 28).next_to(p0 + P3(vt / 2, 0), UP, buff=0.08),
                       num(r"v_n", VEL, 28).next_to(p0 + P3(0, -vn / 2), LEFT, buff=0.08), txt("ANTES", 14, color=DIM).next_to(p0, UP, buff=0.32))
        antes.add(caixa_dec(antes))
        p1 = O + P3(2.3, 0.25)
        depois = VGroup(arrow(p1, p1 + P3(vt, 0), color=VEL, width=5, tip=0.14), arrow(p1, p1 + P3(0, vn), color=VEL, width=5, tip=0.14),
                        num(r"v_t", VEL, 28).next_to(p1 + P3(vt / 2, 0), DOWN, buff=0.08),
                        num(r"v_n", VEL, 28).next_to(p1 + P3(0, vn / 2), RIGHT, buff=0.08),
                        txt("DEPOIS", 14, color=DIM).next_to(p1 + P3(vt / 2, vn), UP, buff=0.12))
        depois.add(caixa_dec(depois))
        imp = arrow(O + P3(0.0, 0.05), O + P3(0, 1.3), color=JC, width=8, tip=0.22, z=11)
        limp = linha(tex(r"\vec J", JC, 34), "NORMAL", size=16, color=JC, buff=0.1).next_to(imp, UP, buff=0.1)
        self.diz("Então o impulso no corpúsculo")
        self.play(GrowArrow(imp), FadeIn(limp), FadeIn(antes), run_time=0.9)
        self.diz("ele inverte a parte normal")
        self.play(Indicate(antes[1], color=WHITE_, scale_factor=1.15), Indicate(antes[3], color=WHITE_), run_time=0.9)
        self.diz("não mexe na parte paralela")
        self.play(Indicate(imp, color=WHITE_, scale_factor=1.1), Indicate(limp, color=WHITE_), run_time=0.9)
        self.diz("Repara nas setinhas")
        self.play(s.animate.set_value(2.0), FadeIn(depois), run_time=0.8, rate_func=linear)
        a1 = arco_ang(O, PI / 2, PI / 2 + th, 0.85)
        a2 = arco_ang(O, PI / 2 - th, PI / 2, 0.85)
        lt1 = num(r"\theta_1", WHITE_, 30).move_to(O + 1.15 * P3(-math.sin(th / 2), math.cos(th / 2)))
        lt2 = num(r"\theta_1'", WHITE_, 30).move_to(O + 1.15 * P3(math.sin(th / 2), math.cos(th / 2)))
        self.play(Create(a1), Create(a2), FadeIn(lt1), FadeIn(lt2), run_time=0.4)
        cp.clear_updaters()
        self.remove(cp)
        f0.clear_updaters()
        self.remove(f0)
        fa, fb = fluxo(self, A, O, n=8, v=1.3, r=0.1), fluxo(self, O, B, n=8, v=1.3, r=0.1)    # v6: palco vivo
        self.add(fa, fb)
        r_t = txt("TANGENCIAL: IGUAL", 24).move_to(P3(XR, 1.3))
        r_n = txt("NORMAL: INVERTIDA", 24).move_to(P3(XR, 0.65))
        r_a = num(r"\theta_1'=\theta_1", WHITE_, 56).move_to(P3(XR, -0.5))
        self.diz("a parte paralela fica igual")
        self.play(FadeIn(r_t), run_time=0.5)
        self.diz("e a normal troca de sentido")
        self.play(FadeIn(r_n), run_time=0.5)
        self.diz("o ângulo de reflexão")
        self.play(FadeIn(r_a, shift=0.1 * UP), run_time=0.7)
        self.diz("o Newton está mandando bem")
        self.play(Indicate(r_a, color=WHITE_, scale_factor=1.08), run_time=0.8)
        self.ate(0.97)
        fa.clear_updaters(); fb.clear_updaters()
        self.virada(tudo=True)               # v4: virada em sequência (sai tudo, depois entra o novo)

    def e9_3(self):
        self.an("E9-3")
        Y = -0.5
        O = P3(-3.3, Y)
        self.O = O
        t_ag = self.clk.get_value()

        def agua_():                                   # v7 (2D+): água em degradê com cáustica suave (linhas de luz que ondulam devagar)
            u = self.clk.get_value() - t_ag
            g = VGroup(Rectangle(width=7.4, height=3.1).set_stroke(width=0).set_fill(color=[mix(BLUE_L, 0.1), escuro(BLUE_L, 0.75)], opacity=0.22)
                       .set_sheen_direction(DOWN).move_to(P3(-3.6, Y - 1.55)))
            for k in range(5):
                yk = Y - 0.35 - 0.55 * k
                pts = [P3(x, yk + 0.06 * math.sin(2.1 * x + 0.9 * u + 1.7 * k)) for x in np.linspace(-7.2, 0.0, 30)]
                g.add(VMobject().set_points_smoothly(pts).set_stroke(mix(BLUE_L, 0.4), 1.4, 0.16 - 0.025 * k))
            return g.set_z_index(-2)
        agua = always_redraw(agua_)
        sup = VGroup(Line(P3(-7.3, Y), P3(0.1, Y)).set_stroke(mix(BLUE_L, 0.3), 9, 0.12), Line(P3(-7.3, Y), P3(0.1, Y)).set_stroke(mix(BLUE_L, 0.3), 2.5))
        lar = txt("AR", 20, color=DIM).move_to(O + P3(2.6, 0.4))
        lag = txt("ÁGUA", 20, color=mix(BLUE_L, 0.3)).move_to(P3(-6.4, Y - 0.4))
        nrm = DashedLine(O + P3(0, -2.9), O + P3(0, 3.0), dash_length=0.08).set_stroke(WHITE_, 1.5, opacity=0.6)
        L = LR
        A = O + L * P3(-math.sin(T1), math.cos(T1))
        B = O + L * P3(math.sin(T2), -math.cos(T2))
        r1 = Line(A, O).set_stroke(WHITE_, 1.2, opacity=0.35)
        r2 = Line(O, B).set_stroke(WHITE_, 1.2, opacity=0.35)
        self.play(FadeIn(agua), Create(sup), FadeIn(lar), FadeIn(lag), Create(nrm), FadeIn(r1), FadeIn(r2), run_time=1.0)
        ESP = LR / 5
        self.ESP = ESP
        f1 = fluxo_esp(self, A, O, ESP, 1.4)
        f2 = fluxo_esp(self, O, B, ESP * N_AGUA, 1.4 * N_AGUA)          # modelo de Newton: mais rápido na água = mais espaçado
        self.add(f1, f2)
        # componentes: tangencial igual; normal cresce (modelo de Newton: v2 = 1,33 v1)
        v = 1.5
        vt, vn1 = v * math.sin(T1), v * math.cos(T1)
        vn2 = v * N_AGUA * math.cos(T2)
        p0 = O + P3(-3.5, 1.6)                          # v6 (N4): à esquerda do raio incidente, sem tocar nos corpúsculos
        c1 = VGroup(arrow(p0, p0 + P3(vt, 0), color=VEL, width=5, tip=0.14), arrow(p0, p0 + P3(0, -vn1), color=VEL, width=5, tip=0.14),
                    num(r"v_t", VEL, 28).next_to(p0 + P3(vt / 2, 0), UP, buff=0.08),
                    num(r"v_{n}", VEL, 28).next_to(p0 + P3(0, -vn1 / 2), LEFT, buff=0.08))
        c1.add(caixa_dec(c1))
        p1 = O + P3(1.9, -0.6)                          # v6 (N4): à direita do raio na água, longe do ponto de entrada
        c2 = VGroup(arrow(p1, p1 + P3(vt, 0), color=VEL, width=5, tip=0.14), arrow(p1, p1 + P3(0, -vn2), color=VEL, width=5, tip=0.14),
                    num(r"v_t", VEL, 28).next_to(p1 + P3(vt / 2, 0), UP, buff=0.08),
                    num(r"v_{n}", VEL, 28).next_to(p1 + P3(0, -vn2 / 2), RIGHT, buff=0.08))
        c2.add(caixa_dec(c2))
        imp = arrow(O + P3(0.0, -0.05), O + P3(0, -1.0), color=JC, width=8, tip=0.22, z=11)
        limp = linha(tex(r"\vec J", JC, 34), "NORMAL", size=16, color=JC, buff=0.1).next_to(imp, LEFT, buff=0.15)
        self.diz("a água também dá um impulso")
        self.play(GrowArrow(imp), FadeIn(limp), run_time=0.8)
        self.diz("De novo, a parte da velocidade")
        self.play(FadeIn(c1), run_time=0.7)
        self.play(FadeIn(c2), run_time=0.7)
        nt = txt("A TANGENCIAL SE CONSERVA", 20, color=VEL).move_to(P3(XR, 1.6))
        self.diz("à superfície se conserva")
        self.play(FadeIn(nt), run_time=0.5)
        a1 = arco_ang(O, PI / 2, PI / 2 + T1, 0.8)
        a2 = arco_ang(O, -PI / 2, -PI / 2 + T2, 0.95)
        lt1 = num(r"\theta_1", WHITE_, 30).move_to(O + 1.1 * P3(-math.sin(T1 / 2), math.cos(T1 / 2)))
        lt2 = num(r"\theta_2", WHITE_, 30).move_to(O + 1.3 * P3(math.sin(T2 / 2), -math.cos(T2 / 2)))
        mn = txt("ÂNGULOS MEDIDOS DA NORMAL", 16, color=DIM).move_to(P3(XR, 0.95))
        self.diz("Com os ângulos medidos")
        self.play(Create(a1), Create(a2), FadeIn(lt1), FadeIn(lt2), FadeIn(mn), run_time=0.9)
        e = num(r"v_1" + SEN + r"\theta_1=v_2" + SEN + r"\theta_2", WHITE_, 52).move_to(P3(XR, 0.0))
        self.diz("a velocidade no ar vezes o seno")
        self.play(FadeIn(e, shift=0.1 * UP), run_time=0.9)
        self.ate(0.97)
        self.e_tan, self.nt, self.mn = e, nt, mn
        self.fluxos = (f1, f2)

    def e9_4_5_6(self):
        self.an("E9-4")
        e4 = Mc(r"\frac{" + SEN + r"\theta_1}{" + SEN + r"\theta_2}", "=", r"\text{constante}", size=52).move_to(P3(XR, -1.2))
        ls = txt("A FORMA DA LEI DE SNELL", 18, color=DIM).next_to(e4, DOWN, buff=0.2)
        self.diz("o seno do ângulo no ar dividido")
        self.play(FadeIn(e4, shift=0.1 * UP), run_time=0.9)
        self.diz("É a forma da lei de Snell")
        self.play(FadeIn(ls), run_time=0.5)
        self.diz("essa constante é a velocidade na água")
        e4b = Mc(r"\frac{" + SEN + r"\theta_1}{" + SEN + r"\theta_2}", "=", (r"\frac{v_2}{v_1}", VEL), size=52).move_to(P3(XR, -1.2))
        lnw = txt("NO MODELO DE NEWTON", 18, color=DIM).next_to(e4b, DOWN, buff=0.2)
        self.play(TransformMatchingTex(e4, e4b), FadeOut(ls), FadeIn(lnw), run_time=1.1)
        cx = SurroundingRectangle(e4b[2], buff=0.1, corner_radius=0.06).set_stroke(VEL, 2)
        self.diz("Guarda essa ordem")
        self.play(Create(cx), run_time=0.5)
        self.ate(0.97)
        # E9-5 -----------------------------------------------------------------------------------------------
        self.an("E9-5")
        q1 = num(r"\theta_2<\theta_1", WHITE_, 44)
        q2 = num(r"\Rightarrow\ \frac{v_2}{v_1}>1", VEL, 44)
        VGroup(q1, q2).arrange(RIGHT, buff=0.4).move_to(P3(XR, -2.7))
        perto = txt("SE APROXIMA DA NORMAL", 16, color=DIM).move_to(self.O + P3(-2.4, -2.3))      # v6 (N3)
        self.diz("a luz se aproxima da normal")
        self.play(FadeIn(perto), run_time=0.5)
        self.diz("O ângulo na água é menor")
        self.play(FadeIn(q1, shift=0.1 * UP), run_time=0.7)
        self.diz("a razão dos senos é maior que um")
        self.play(FadeIn(q2, shift=0.1 * UP), run_time=0.7)
        nw = linha("NEWTON:", "LUZ MAIS RÁPIDA NA ÁGUA", size=22, buff=0.15)
        self.diz("a velocidade na água teria que ser maior")
        self.play(FadeOut(self.nt), FadeOut(self.mn), run_time=0.3)
        nw.move_to(P3(XR, 1.4))
        self.play(FadeIn(nw, shift=0.1 * UP), run_time=0.7)
        pn = txt("PREVISÃO DE NEWTON: MAIS ESPAÇADOS NA ÁGUA", 15, color=LUZ).move_to(self.O + P3(0.9, -3.35))
        self.diz("Os corpúsculos acelerariam")
        self.play(FadeIn(pn, shift=0.1 * UP), run_time=0.7)
        self.pn = pn
        self.ate(0.97)
        # E9-6 -----------------------------------------------------------------------------------------------
        self.an("E9-6")
        f1, f2 = self.fluxos
        self.play(FadeOut(self.e_tan), FadeOut(e4b), FadeOut(lnw), FadeOut(cx), FadeOut(q1), FadeOut(q2), FadeOut(nw), FadeOut(self.pn),
                  run_time=0.5)
        ano = txt("1850 · FOUCAULT", 36, bold=True).move_to(P3(XR, 1.6))
        lenta = txt("A LUZ É MAIS LENTA NA ÁGUA", 24).move_to(P3(XR, 0.95))
        ve = num(r"v_2>v_1", WHITE_, 50).move_to(P3(2.3, -0.4))
        nwp = txt("PREVISÃO DE NEWTON", 16, color=DIM).next_to(ve, DOWN, buff=0.18)
        self.diz("ninguém conseguiu medir")
        self.play(FadeIn(ve), FadeIn(nwp), run_time=0.6)
        self.diz("mil oitocentos e cinquenta")
        self.play(FadeIn(ano, shift=0.1 * UP), run_time=0.8)
        self.diz("e ela era mais lenta")
        self.play(FadeIn(lenta, shift=0.1 * UP), run_time=0.7)
        # os corpúsculos na água passam a andar mais devagar
        f2.clear_updaters()
        self.remove(f2)
        B2 = self.O + LR * P3(math.sin(T2), -math.cos(T2))
        f3 = fluxo_esp(self, self.O, B2, self.ESP / N_AGUA, 1.4 / N_AGUA)   # a luz de verdade: mais lenta na água, mais junta
        self.add(f3)
        rk = risco(ve, w=6)
        self.diz("A previsão do modelo corpuscular caiu")
        self.play(ve.animate.set_color(APAGADO), Create(rk), run_time=0.8)
        self.diz("Na descrição ondulatória")
        ond = txt("DESCRIÇÃO ONDULATÓRIA", 18, color=DIM).move_to(P3(5.4, -0.95))
        eo = Mc(r"\frac{" + SEN + r"\theta_1}{" + SEN + r"\theta_2}", "=", (r"\frac{v_1}{v_2}", VEL), size=46).move_to(P3(5.4, -0.15))
        self.play(FadeIn(eo, shift=0.1 * UP), FadeIn(ond), run_time=0.9)
        self.diz("E é essa que a natureza segue")
        self.play(Indicate(eo, color=WHITE_, scale_factor=1.06), run_time=0.9)
        self.ate(0.97)
        self.f13 = (f1, f3)
        self.c6 = VGroup(ano, lenta, ve, rk, nwp, eo, ond)     # o risco sai junto com o "v₂ > v₁"

    def e9_7(self):
        """O PALCO continua (corpúsculos no tanque, agora apagados); a frase de fechamento entra na CONTA."""
        self.an("E9-7")
        f1, f3 = self.f13
        for f in (f1, f3):
            f.clear_updaters()
        palco = [m for m in self.mobjects if m not in self.fixos() and m is not self.clk and m not in (f1, f3) and m not in self.c6]
        B2 = self.O + LR * P3(math.sin(T2), -math.cos(T2))
        A1 = self.O + LR * P3(-math.sin(T1), math.cos(T1))
        g1 = fluxo_esp(self, A1, self.O, self.ESP, 1.4, op=0.35)
        g2 = fluxo_esp(self, self.O, B2, self.ESP / N_AGUA, 1.4 / N_AGUA, op=0.35)
        self.play(FadeOut(self.c6), FadeOut(f1), FadeOut(f3), *[m.animate.fade(0.65) for m in palco if isinstance(m, VMobject)],
                  run_time=0.7)
        self.remove(f1, f3)
        self.add(g1, g2)
        a = txt("IMPULSO CERTO", 34, bold=True)
        b = linha(mais(40), txt("MODELO ERRADO", 34, bold=True, color=APAGADO), buff=0.2)
        c = linha(mais(40, "="), txt("PREVISÃO TESTÁVEL", 34, bold=True, color=CYAN), buff=0.2)
        VGroup(a, b, c).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        for m_, y in ((a, 1.6), (b, 0.8), (c, 0.0)):
            na_conta(m_, y)
        self.diz("o raciocínio do impulso estava certo")
        self.play(FadeIn(a, shift=0.1 * UP), run_time=0.8)
        self.diz("O que falhou foi o modelo")
        self.play(FadeIn(b, shift=0.1 * UP), run_time=0.8)
        self.diz("fez uma previsão que dava para testar")
        self.play(FadeIn(c, shift=0.1 * UP), run_time=0.8)
        self.diz("Até o Newton errou")
        d = dica("O IMPULSO É NORMAL: SÓ A COMPONENTE", "NORMAL DA VELOCIDADE MUDA")
        self.dica_entra(d)
        self.sobra(0.55)
        g1.clear_updaters(); g2.clear_updaters()
        self.clear(rt=0.5)
