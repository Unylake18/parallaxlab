"""Lote Q7 (v2): E7 — o caçador no lago. PALCO fixo: manequim 3D com a arma no lago congelado; tiro horizontal e depois a 56° (arco no
Manim), recuo deslizando; a normal do gelo como seta Manim vertical durante o disparo. 72,5 kg; bala 4,20 g a 965 m/s.
Horizontal: 0,0559 m/s; a 56°: 0,0313 m/s. Energias 1.956 J × 0,113 J (razão ≈ 17.262), barras na CONTA."""
from kit import *  # noqa: F401,F403
from sec_manequim import Manequim3D, boca, pose_mira

MC, MBALA, VBALA, ANG = 72.5, 0.00420, 965.0, math.radians(56.0)
V_H = MBALA * VBALA / MC
V_56 = V_H * math.cos(ANG)
KB, KCZ = MBALA * VBALA ** 2 / 2, MC * V_H ** 2 / 2
RAZ = MC / MBALA
assert abs(V_H - 0.0559) < 1e-4 and abs(V_56 - 0.0313) < 1e-4 and abs(KB - 1955.6) < 0.1 and abs(KCZ - 0.1133) < 1e-3
assert abs(KB / KCZ - RAZ) < 1e-6 * RAZ and round(RAZ) == 17262 and abs(KB / (KB + KCZ) - 0.999942) < 1e-6

PER, TS = 6.0, 1.6            # loop do tiro; instante do disparo no ciclo
VBV = 9.0                     # a bala na tela (m/s, câmera lenta)
KREC = 1.5                    # o recuo é mostrado ×1,5 (é de poucos centímetros por segundo)


class LoteE7(Base):
    def construct(self):
        self.setup_base(cap="EXERCÍCIO 7 · O CAÇADOR NO LAGO", selo="MOMENTO POR COMPONENTE")
        self.ang = 0.0
        self.V = V_H
        self.t0 = 0.0
        self.mq = Manequim3D(self, self.pose, K=2.3, xt=-4.3, yc=-2.95, camx=0.0, op=0.0)
        self.add(self.mq.f3d)
        self.e7_1_2()
        self.e7_3_4()
        self.e7_5()
        self.fim()
        self.relatorio()

    def s(self, t=None):
        t = self.clk.get_value() if t is None else t
        return (t - self.t0) % PER

    def pose(self, t):
        s = self.s(t)
        dt = max(0.0, s - TS)
        x = -KREC * self.V * dt
        rec = math.exp(-dt / 0.25) * (1 if s >= TS else 0)
        p = pose_mira(x, self.ang, 1, recuo=rec)
        p["rifle"] = {"on": True, "ang": self.ang}
        p["bala"] = VBV * dt if 0 < dt < 0.2 else None
        return p

    def setas(self):
        def f():
            e = self.mq.f3d.e
            s = self.s()
            g = VGroup()
            op = min(1.0, (PER - s) / 0.3, s / 0.3)
            bx, bz, (cx, cz) = boca(e, self.ang)
            if TS <= s < TS + 0.18:
                g.add(Star(n=7, outer_radius=0.22, inner_radius=0.09, color=WHITE_).set_fill(WHITE_, 0.9).set_stroke(width=0)
                      .move_to(self.mq.m(bx, bz)).set_z_index(13))
            if s >= TS:
                q = self.mq.m(e["hx"], 0.5)
                L = 9.0 * self.V
                g.add(arrow(q + P3(-0.4, 0), q + P3(-0.4 - L, 0), color=VEL, width=7, tip=0.17, z=12))
                g.add(mtex(r"\vec V", VEL, 32).move_to(q + P3(-0.4 - L / 2, 0.35)))
            if self.ang > 0.1 and TS - 0.1 <= s < TS + 0.5:          # normal do gelo: cresce de repente durante o disparo
                u = 1.0 - min(1.0, max(0.0, s - TS) / 0.5)
                pe = self.mq.m(e["hx"], 0.0)
                g.add(arrow(pe + P3(0.25, -0.6), pe + P3(0.25, -0.6 + 0.4 + 1.6 * u), color=FC, width=8, tip=0.2, z=12))
                g.add(mtex(r"\vec N", FC, 34).move_to(pe + P3(0.7, -0.35)))
            return escala_op(g, max(op, 0)) if op < 1 else g
        return always_redraw(f)

    def tiro(self, ang, V):
        self.ang, self.V = ang, V
        self.t0 = self.clk.get_value()

    # ── E7-1, E7-2: tiro horizontal ───────────────────────────────────────────────────────────────────────
    def e7_1_2(self):
        self.an("E7-1")
        self.tiro(0.0, V_H)
        self.t0 += 2.0                           # o primeiro tiro sai um pouco depois
        self.play(self.mq.f3d.op.animate.set_value(1.0), run_time=1.0)
        lg = txt("LAGO CONGELADO · SEM ATRITO", 16, color=BLUE_L).move_to(P3(-3.3, -3.25))
        fr = fronteira(7.4, 5.6, P3(-3.75, -0.6), rotulo=["CAÇADOR", mais(22), "ARMA", mais(22), "BALA"])
        sg = self.sg = self.setas()
        self.add(sg)
        self.play(FadeIn(lg), Create(fr[0]), FadeIn(fr[1]), run_time=0.9)
        dados = VGroup(MathTex(r"M=72{,}5\ \mathrm{kg}", font_size=40), MathTex(r"m=4{,}20\ \mathrm{g}", font_size=40),
                       MathTex(r"v=965\ \mathrm{m/s}", font_size=40, color=VEL)).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        na_conta(dados, 1.5)
        self.ate(0.3)
        self.play(FadeIn(dados[0]), run_time=0.5)
        self.ate(0.55)
        self.play(FadeIn(dados[1]), FadeIn(dados[2]), run_time=0.6)
        self.ate(0.97)
        self.an("E7-2")
        th = txt("TIRO HORIZONTAL", 20, bold=True)
        e1 = MathTex(r"0=m\,v-M\,V", font_size=42)
        e2 = Mc(r"V=\frac{0{,}00420\cdot 965}{72{,}5}=", (r"0{,}0559\ \mathrm{m/s}", VEL), size=40)
        for m_, y in ((th, 0.15), (e1, -0.45), (e2, -1.35)):
            na_conta(m_, y)
        self.play(FadeIn(th), FadeIn(e1, shift=0.1 * UP), run_time=0.8)
        self.ate(0.5)
        self.play(FadeIn(e2, shift=0.1 * UP), run_time=0.8)
        rc = txt("RECUO EXAGERADO NA TELA", 14, color=DIM).move_to(P3(-3.3, -3.7))
        self.play(FadeIn(rc), run_time=0.4)
        self.ate(0.97)
        self.fr, self.lg, self.rc = fr, lg, rc
        self.c2 = VGroup(dados, th, e1, e2)

    # ── E7-3, E7-4: tiro a 56°, a normal do gelo ──────────────────────────────────────────────────────────
    def e7_3_4(self):
        self.an("E7-3")
        self.play(self.c2.animate.set_opacity(0.4), run_time=0.4)
        self.tiro(ANG, V_56)

        def arco():
            e = self.mq.f3d.e
            bx, bz, (cx, cz) = boca(e, ANG)
            c = self.mq.m(cx, cz)
            r = 0.75
            g = VGroup(Arc(radius=r, start_angle=0, angle=ANG, arc_center=c).set_stroke(WHITE_, 2),
                       DashedLine(c, c + P3(1.1, 0), dash_length=0.06).set_stroke(DIM, 1.5),
                       mtex(r"56^\circ", WHITE_, 28).move_to(c + P3(1.05, 0.38)))
            return g
        ar = always_redraw(arco)
        self.play(FadeIn(ar), run_time=0.6)
        q = txt("QUEM SEGUROU ELE?", 26, bold=True)
        na_conta(q, 2.3 - 0.0)
        self.play(FadeOut(self.c2), run_time=0.4)
        self.ate(0.6)
        self.play(FadeIn(q), run_time=0.6)
        self.ate(0.97)
        self.an("E7-4")
        self.play(FadeOut(q), run_time=0.35)
        g1 = txt("O GELO: A NORMAL É EXTERNA E IMPULSIVA", 18, color=FC)
        p1 = linha(tex(r"P_y", MAG, 42), "NÃO SE CONSERVA", size=24, buff=0.2)
        p2 = linha(tex(r"P_x", MAG, 42), "SE CONSERVA", size=24, buff=0.2)
        e3 = Mc(r"V=0{,}0559\cdot\cos 56^\circ=", (r"0{,}031\ \mathrm{m/s}", VEL), size=40)
        for m_, y in ((g1, 2.3), (p1, 1.45), (p2, 0.65), (e3, -0.45)):
            na_conta(m_, y)
        self.play(FadeIn(g1), run_time=0.4)
        self.ate(0.25)
        self.play(FadeIn(p1, shift=0.1 * UP), run_time=0.7)
        self.ate(0.45)
        self.play(FadeIn(p2, shift=0.1 * UP), run_time=0.7)
        self.ate(0.7)
        self.play(FadeIn(e3, shift=0.1 * UP), run_time=0.8)
        tc = txt("UNS 3 CENTÍMETROS POR SEGUNDO", 16, color=DIM)
        na_conta(tc, -1.1)
        self.play(FadeIn(tc), run_time=0.5)
        self.ate(0.97)
        ar.clear_updaters()
        self.c4 = VGroup(g1, p1, p2, e3, tc, ar)

    # ── E7-5: energias (barras na CONTA), o PALCO repetindo o tiro horizontal ─────────────────────────────
    def e7_5(self):
        self.an("E7-5")
        self.play(FadeOut(self.c4), run_time=0.5)
        self.tiro(0.0, V_H)
        th = txt("TIRO HORIZONTAL", 16, color=DIM)
        na_conta(th, -3.3)
        ra = Mc((r"\frac{K_{\text{bala}}}{K_{\text{caçador}}}", KC), r"\approx 17.262=", (r"\frac{72{,}5}{0{,}0042}", KC), size=38)
        na_conta(ra, 2.0)
        pc = linha(tex(r"\approx 99{,}994\%", KC, 40), "NA BALA", size=22, buff=0.15)
        na_conta(pc, 1.15)
        yb = -2.15
        # momento: barras iguais
        pm = VGroup(*[Rectangle(width=0.5, height=1.5).set_stroke(mix(MAG, 0.3), 2).set_fill(MAG, 0.75).move_to(P3(x, yb + 0.75))
                      for x in (1.65, 2.55)])
        lpm = VGroup(txt("BALA", 13, color=DIM).next_to(pm[0], DOWN, buff=0.08), txt("CAÇADOR", 13, color=DIM).next_to(pm[1], DOWN, buff=0.08))
        tpm = txt("MOMENTO", 16, color=MAG).next_to(pm, UP, buff=0.15)
        vpm = tex(r"4{,}05\ \mathrm{kg\cdot m/s}", MAG, 24).next_to(tpm, UP, buff=0.08)
        # energia em escala log (10^-2 a 10^4 J)
        xa, hd = 3.8, 0.38
        ylog = lambda v: yb + hd * (math.log10(v) + 2)
        eixo = Line(P3(xa, yb), P3(xa, ylog(1e4) + 0.1)).set_stroke(DIM, 2)
        tk = VGroup(*[VGroup(Line(P3(xa - 0.06, ylog(10 ** k)), P3(xa + 0.06, ylog(10 ** k))).set_stroke(DIM, 2),
                             tex(rf"10^{{{k}}}", DIM, 20).next_to(P3(xa - 0.06, ylog(10 ** k)), LEFT, buff=0.06)) for k in (-2, 0, 2, 4)])
        te = txt("ENERGIA (ESCALA LOG)", 15, color=KC).move_to(P3(xa + 0.9, ylog(1e4) + 0.42))
        eb = Rectangle(width=0.55, height=ylog(KB) - yb).set_stroke(mix(KC, 0.3), 2).set_fill(KC, 0.75).move_to(P3(xa + 0.6, (ylog(KB) + yb) / 2))
        ec = Rectangle(width=0.55, height=ylog(KCZ) - yb).set_stroke(mix(KC, 0.3), 2).set_fill(KC, 0.75).move_to(P3(xa + 1.3, (ylog(KCZ) + yb) / 2))
        veb = tex(r"1.956\ \mathrm{J}", KC, 22).next_to(eb, RIGHT, buff=0.06).align_to(eb, UP)
        vec = tex(r"0{,}11\ \mathrm{J}", KC, 22).next_to(ec, UP, buff=0.06)
        lec = VGroup(txt("BALA", 13, color=DIM).next_to(eb, DOWN, buff=0.08), txt("CAÇADOR", 13, color=DIM).next_to(ec, DOWN, buff=0.08))
        base = Line(P3(1.3, yb), P3(5.6, yb)).set_stroke(DIM, 2)
        self.play(FadeIn(th), FadeIn(base), GrowFromEdge(pm[0], DOWN), GrowFromEdge(pm[1], DOWN), FadeIn(lpm), FadeIn(tpm), FadeIn(vpm), run_time=0.9)
        self.ate(0.25)
        self.play(FadeIn(eixo), FadeIn(tk), FadeIn(te), GrowFromEdge(eb, DOWN), FadeIn(veb), FadeIn(lec[0]), run_time=0.9)
        self.play(GrowFromEdge(ec, DOWN), FadeIn(vec), FadeIn(lec[1]), run_time=0.8)
        self.ate(0.5)
        self.play(FadeIn(ra, shift=0.1 * UP), run_time=0.8)
        self.ate(0.68)
        self.play(FadeIn(pc, shift=0.1 * UP), run_time=0.7)
        self.ate(0.8)
        d = dica("ISOLADO NA HORIZONTAL", "NÃO É ISOLADO NA VERTICAL")
        self.dica_entra(d)
        self.ate(0.97)
        self.sg.clear_updaters()
        self.dica_sai()
        self.clear(rt=0.5)
