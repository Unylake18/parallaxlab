"""Lote P9: T9 — escolher o sistema. Bola de 1 kg caindo 10 m (só a bola × bola + Terra); blocos de 1 kg e 2 kg com mola num chão
com atrito (μ = 0,2): P(t) = −1,96 t até 0,510 s, depois −(2,0 − 1,96 t) até 1,020 s; P_Terra = −P; a soma é identicamente zero."""
from kit import *  # noqa: F401,F403

G_ = 9.8
MU = 0.2
M1, M2, V1, V2 = 1.0, 2.0, -2.0, 1.0
AF = MU * G_                                     # 1,96 m/s²
T2, T1 = V2 / AF, -V1 / AF                       # 0,510 s (pesado para) · 1,020 s (leve para)
F1, F2 = MU * M1 * G_, -MU * M2 * G_             # +1,96 N · −3,92 N
assert abs(M1 * V1 + M2 * V2) < 1e-12 and abs(F1 - 1.96) < 1e-12 and abs(F2 + 3.92) < 1e-12


def v1(t):
    return V1 + AF * t if t < T1 else 0.0


def v2(t):
    return V2 - AF * t if t < T2 else 0.0


def x1(t):
    t = min(t, T1)
    return V1 * t + AF * t * t / 2


def x2(t):
    t = min(t, T2)
    return V2 * t - AF * t * t / 2


def P(t):
    return M1 * v1(t) + M2 * v2(t)


# conferências do briefing (§3, T9)
assert abs(T2 - 0.5102) < 1e-3 and abs(T1 - 1.0204) < 1e-3
assert abs(P(T2) + 1.0) < 1e-9 and abs(P(T1)) < 1e-9 and abs(P(0.3) + 1.96 * 0.3) < 1e-9 and abs(P(0.8) + (2.0 - 1.96 * 0.8)) < 1e-9
assert abs(x1(T1) + 1.0204) < 1e-3 and abs(x2(T2) - 0.2551) < 1e-3
assert abs(1 * math.sqrt(2 * G_ * 10) / 5.97e24 - 2.35e-24) < 0.01e-24

Y_CH = 0.55
ESC = 2.0                                        # u por metro
XL0, XP0 = -0.85, 0.95                           # centros iniciais (leve, pesado)
LL, LP, HP = 0.72, 1.05, 0.95


class LoteT9(Base):
    def construct(self):
        self.setup_base(cap="ESCOLHER O SISTEMA", selo="MOYSÉS §8.1–8.3")
        self.t9_1_2()
        self.t9_3()
        self.t9_4()
        self.t9_5_6()
        self.t9_7()
        self.fim()
        self.relatorio()

    # ── T9-1, T9-2: bola e Terra ────────────────────────────────────────────────────────────────────────────
    def t9_1_2(self):
        self.an("T9-1")
        XB, YT, YB = -3.6, 1.9, -2.32
        terra = VGroup(Circle(radius=7.6, arc_center=P3(XB, -10.2)).set_stroke(mix(TERRA, 0.35), 2.5).set_fill(TERRA, 1))
        lt = txt("TERRA", 22, color=GEO).move_to(P3(XB + 2.6, -3.3))
        q = ValueTracker(0.0)                     # fração da altura caída (0 → 1)
        topo = DashedLine(P3(XB - 0.9, YT), P3(XB + 0.9, YT)).set_stroke(DIM, 1.5, opacity=0.5)
        cota = VGroup(DoubleArrow(P3(XB - 1.3, YT), P3(XB - 1.3, YB - 0.25), buff=0, color=DIM, stroke_width=2, tip_length=0.12),
                      tex(r"10\ \mathrm{m}", DIM, 30).move_to(P3(XB - 1.85, (YT + YB) / 2)))
        self.terra_on = ValueTracker(0.0)

        def bola_cai():
            u = q.get_value()
            c = P3(XB, YT - (YT - YB) * u)
            v = 14.0 * math.sqrt(max(u, 0))
            g = VGroup(bola(0.25, STEEL).move_to(c))
            g.add(arrow(c, c + P3(0, -0.75), color=FC, width=5, tip=0.15, z=9))
            g.add(mtex(r"m\vec g", FC, 28).next_to(c + P3(0, -0.45), LEFT, buff=0.32))
            if v > 0.3:
                g.add(arrow(c + P3(0.5, 0), c + P3(0.5, -0.11 * v), color=MAG, width=6, tip=0.17, z=9))
                g.add(mtex(r"\vec p", MAG, 32).next_to(c + P3(0.5, -0.055 * v), RIGHT, buff=0.12))
                if self.terra_on.get_value() > 0.5:
                    s = P3(XB + 1.4, -2.7)
                    g.add(arrow(s, s + P3(0, 0.11 * v), color=MAG, width=6, tip=0.17, z=9))
                    g.add(mtex(r"-\vec p", MAG, 32).next_to(s + P3(0, 0.055 * v), RIGHT, buff=0.12))
            return g
        bg = always_redraw(bola_cai)
        fr_b = always_redraw(lambda: DashedVMobject(Circle(radius=0.48, arc_center=P3(XB, YT - (YT - YB) * q.get_value()))
                                                    .set_stroke(WHITE_, 2, opacity=0.65), num_dashes=16))
        self.play(FadeIn(terra), FadeIn(lt), FadeIn(topo), FadeIn(cota), FadeIn(bg), run_time=1.0)
        ls = txt("SISTEMA: SÓ A BOLA", 22, color=WHITE_, op=0.85).move_to(P3(XB + 2.3, YT + 0.1))
        self.play(Create(fr_b), FadeIn(ls), run_time=0.8)
        self.ate(0.1)
        self.play(q.animate.set_value(1.0), run_time=4.0, rate_func=lambda u: u * u)
        r1 = num_ = MathTex(r"v=\sqrt{2gh}=14{,}0\ \mathrm{m/s}", font_size=42, color=VEL).move_to(P3(3.9, 1.5))
        r2 = linha(tex(r"\vec p", MAG, 42), "MUDA O TEMPO TODO", size=24, buff=0.18).move_to(P3(3.9, 0.55))
        r3 = txt("O PESO É EXTERNO", 24, color=FC).move_to(P3(3.9, -0.15))
        self.play(FadeIn(r1, shift=0.1 * UP), run_time=0.8)
        self.ate(0.55)
        self.play(FadeIn(r2, shift=0.1 * UP), run_time=0.7)
        self.ate(0.75)
        self.play(FadeIn(r3, shift=0.1 * UP), run_time=0.7)
        self.ate(0.97)
        # T9-2 -----------------------------------------------------------------------------------------------
        self.an("T9-2")
        fr_b.clear_updaters()
        big = fronteira(6.2, 5.9, P3(XB + 0.25, -0.65), rotulo=None)
        lsb = linha("SISTEMA: BOLA", mais(30), "TERRA", size=22, buff=0.12).set_opacity(0.85).move_to(ls)
        self.play(ReplacementTransform(fr_b, big[0]), ReplacementTransform(ls, lsb), FadeOut(r2), FadeOut(r3), run_time=1.4)
        self.play(q.animate.set_value(0.0), run_time=0.8)
        self.terra_on.set_value(1.0)
        ie = txt("A FORÇA ENTRE ELAS FICA INTERNA", 22, color=INT).move_to(P3(3.9, 0.55))
        self.play(FadeIn(ie), run_time=0.6)
        self.ate(0.2)
        self.play(q.animate.set_value(1.0), run_time=4.0, rate_func=lambda u: u * u)
        e0 = Mc((r"\vec P_{total}", MAG), "=", "0", size=50).move_to(P3(3.9, -0.4))
        n0 = txt("EM TODO INSTANTE", 20, color=DIM).next_to(e0, DOWN, buff=0.18)
        self.play(FadeIn(e0, shift=0.1 * UP), FadeIn(n0), run_time=0.8)
        self.ate(0.6)
        et = MathTex(r"v_{Terra}=\frac{1\cdot 14}{5{,}97\times10^{24}}\approx 2{,}3\times10^{-24}\ \mathrm{m/s}", font_size=38, color=VEL) \
            .move_to(P3(3.9, -2.1))
        self.play(FadeIn(et, shift=0.1 * UP), run_time=0.9)
        self.ate(0.97)
        bg.clear_updaters()

    # ── T9-3: os dois blocos e a mola ───────────────────────────────────────────────────────────────────────
    def blocos(self, tau, m1lab=r"1\ \mathrm{kg}", m2lab=r"2\ \mathrm{kg}", forcas=True, setas_v=False, iguais=False):
        def f():
            t = tau.get_value()
            if iguais:
                ve, T = 1.4, 1.4 / AF
                tc = min(max(t, 0), T)
                d = ve * tc - AF * tc * tc / 2
                xa, xb = -0.85 - ESC * d, 0.85 + ESC * d
                va, vb = (-(ve - AF * tc), ve - AF * tc) if t < T else (0.0, 0.0)
                la, lb, ha = 0.9, 0.9, 0.9
                fa, fb = (MU * 1.5 * G_, -MU * 1.5 * G_) if t < T else (0, 0)
            else:
                xa, xb = XL0 + ESC * x1(max(t, 0)), XP0 + ESC * x2(max(t, 0))
                va, vb = v1(max(t, 0)), v2(max(t, 0))
                la, lb, ha = LL, LP, HP
                fa = F1 if t < T1 else 0.0
                fb = F2 if t < T2 else 0.0
            A = Corpo("", GEO if not iguais else STEEL, la).at(xa, Y_CH)
            B = Corpo("", STEEL, lb, ha).at(xb, Y_CH)
            g = VGroup(A, B)
            g.add(mtex(m1lab, BACKGROUND_COLOR if not iguais else WHITE_, 26).move_to(A))
            g.add(mtex(m2lab, WHITE_, 28).move_to(B))
            if forcas and t >= 0:
                if abs(fa) > 0:
                    g.add(arrow(P3(xa, Y_CH - 0.22), P3(xa + 0.4 * fa, Y_CH - 0.22), color=FC, width=6, tip=0.17, z=10))
                if abs(fb) > 0:
                    g.add(arrow(P3(xb, Y_CH - 0.45), P3(xb + 0.4 * fb, Y_CH - 0.45), color=FC, width=6, tip=0.17, z=10))
            if setas_v:
                yv = Y_CH + max(ha, la) + 0.32
                if abs(va) > 0.02:
                    g.add(arrow(P3(xa, yv), P3(xa + 0.5 * va, yv), color=VEL, width=5, tip=0.15, z=10))
                if abs(vb) > 0.02:
                    g.add(arrow(P3(xb, yv), P3(xb + 0.5 * vb, yv), color=VEL, width=5, tip=0.15, z=10))
            return g
        return f

    def t9_3(self):
        self.an("T9-3")
        self.clear(rt=0.6)
        self.piso = chao(-7.2, 7.2, Y_CH, dens=3.0)
        lat = txt("CHÃO COM ATRITO", 18, color=DIM).move_to(P3(5.6, Y_CH - 0.45))
        eixo = VGroup(arrow(P3(5.3, 2.15), P3(6.3, 2.15), color=DIM, width=3, tip=0.13), tex(r"+x", DIM, 30).move_to(P3(6.65, 2.15)))
        self.tau = ValueTracker(0.0)
        self.op_f = ValueTracker(0.0)
        self.sv = ValueTracker(0.0)
        blk = self.blocos(self.tau, forcas=False)
        # antes do disparo: blocos parados encostando na mola comprimida
        A0 = Corpo("", GEO, LL).at(XL0, Y_CH)
        B0 = Corpo("", STEEL, LP, HP).at(XP0, Y_CH)
        lab0 = VGroup(tex(r"1\ \mathrm{kg}", BACKGROUND_COLOR, 26).move_to(A0), tex(r"2\ \mathrm{kg}", WHITE_, 28).move_to(B0))
        ml = mola(P3(XL0 + LL / 2, Y_CH + 0.36), P3(XP0 - LP / 2, Y_CH + 0.36), n=7, amp=0.12)
        tl = txt("LEVE", 18, color=DIM).next_to(A0, UP, buff=0.18)
        tp = txt("PESADO", 18, color=DIM).next_to(B0, UP, buff=0.18)
        self.play(FadeIn(self.piso), FadeIn(lat), FadeIn(A0), FadeIn(B0), FadeIn(lab0), Create(ml), FadeIn(tl), FadeIn(tp), run_time=1.2)
        self.ate(0.3)
        self.play(FadeIn(eixo), run_time=0.6)
        self.ate(0.45)
        # disparo em poucos quadros: a mola estica e os blocos saem com v1 = −2 e v2 = +1 m/s
        self.play(FadeOut(tl), FadeOut(tp), run_time=0.3)
        ml2 = mola(P3(XL0 + LL / 2 - 0.25, Y_CH + 0.36), P3(XP0 - LP / 2 + 0.12, Y_CH + 0.36), n=7, amp=0.05)
        self.play(Transform(ml, ml2), A0.animate.shift(0.0 * LEFT), run_time=0.2)
        self.remove(A0, B0, lab0)
        bg = always_redraw(self.blocos(self.tau, forcas=False, setas_v=True))
        self.add(bg)
        self.play(FadeOut(ml), run_time=0.5)
        lv1 = tex(r"2\ \mathrm{m/s}", VEL, 28).move_to(P3(XL0 - 0.5, Y_CH + LL + 0.75))
        lv2 = tex(r"1\ \mathrm{m/s}", VEL, 28).move_to(P3(XP0 + 0.25, Y_CH + HP + 0.75))
        self.play(FadeIn(lv1), FadeIn(lv2), run_time=0.5)
        self.ate(0.82)
        pm = Mc((r"p_1=-2", MAG), ",", (r"\ p_2=+2\ \mathrm{kg\cdot m/s}", MAG), size=40).move_to(P3(3.9, -1.15))
        p0 = Mc((r"P", MAG), "=", "0", size=48).move_to(P3(3.9, -2.0))
        self.play(FadeIn(pm, shift=0.1 * UP), run_time=0.7)
        self.play(FadeIn(p0, shift=0.1 * UP), run_time=0.6)
        self.ate(0.97)
        self.bg, self.lv, self.eixo, self.lat, self.pm, self.p0 = bg, VGroup(lv1, lv2), eixo, lat, pm, p0

    # ── gráficos P(t) e P_Terra(t) ──────────────────────────────────────────────────────────────────────────
    def graficos(self):
        self.GP = Graf(-6.2, -0.85, 5.6, 1.2, -1.0, 0.25, 1.0, rot_y=tex(r"P", MAG, 34))
        self.GT = Graf(-6.2, -3.45, 5.6, 1.2, -0.05, 1.0, 1.0, rot_y=tex(r"P_{Terra}", MAG, 30))
        for G, ys in ((self.GP, (-1.0,)), (self.GT, (1.0,))):
            for y in ys:
                G.eixos.add(DashedLine(G.pt(0, y), G.pt(1.2, y), dash_length=0.06).set_stroke(DIM, 1, opacity=0.4))
                G.eixos.add(tex(f"{y:+.1f}".replace(".", "{,}"), DIM, 22).next_to(G.pt(0, y), LEFT, buff=0.12))
        lu = tex(r"\mathrm{kg\cdot m/s}", DIM, 22).next_to(self.GP.ey, RIGHT, buff=0.15)
        self.GP.eixos.add(lu)

    # ── T9-4: massas iguais ─────────────────────────────────────────────────────────────────────────────────
    def t9_4(self):
        self.an("T9-4")
        self.graficos()
        self.play(FadeOut(self.bg), FadeOut(self.lv), FadeOut(self.pm), FadeOut(self.p0), FadeIn(self.GP.eixos), run_time=0.7)
        tit = txt("MASSAS IGUAIS", 26, bold=True).move_to(P3(3.9, -1.1))
        te = ValueTracker(-0.001)
        bi = always_redraw(self.blocos(te, m1lab=r"m", m2lab=r"m", iguais=True))
        curva = always_redraw(lambda: self.GP.curva(lambda t: 0.0, 0.0, max(0.0, min(te.get_value(), 1.2)), n=40))
        self.play(FadeIn(bi), FadeIn(tit), run_time=0.6)
        self.add(curva)
        self.ate(0.2)
        self.play(te.animate.set_value(1.0), run_time=5.0, rate_func=linear)
        r0 = Mc((r"P(t)", MAG), "=", "0", size=44).move_to(P3(3.9, -1.9))
        r1 = txt("PARAM JUNTOS", 20, color=DIM).next_to(r0, DOWN, buff=0.2)
        self.play(FadeIn(r0, shift=0.1 * UP), FadeIn(r1), run_time=0.7)
        self.ate(0.95)
        bi.clear_updaters()
        curva.clear_updaters()
        self.play(FadeOut(bi), FadeOut(curva), FadeOut(tit), FadeOut(r0), FadeOut(r1), run_time=0.5)

    # ── T9-5, T9-6 ──────────────────────────────────────────────────────────────────────────────────────────
    def t9_5_6(self):
        self.an("T9-5")
        tau = self.tau
        bg = always_redraw(self.blocos(tau, forcas=True, setas_v=True))
        self.play(FadeIn(bg), run_time=0.6)
        d = MathTex(r"m_1=1\ \mathrm{kg},\ m_2=2\ \mathrm{kg},\ \mu=0{,}2", font_size=34, color=WHITE_).move_to(P3(3.9, -0.95))
        f1 = linha("ATRITO NO LEVE", tex(r"+1{,}96\ \mathrm{N}", FC, 36), size=20, buff=0.2)
        f2 = linha("ATRITO NO PESADO", tex(r"-3{,}92\ \mathrm{N}", FC, 36), size=20, buff=0.2)
        f3 = linha("RESULTANTE", tex(r"-1{,}96\ \mathrm{N}", FC, 40), size=22, buff=0.2)
        VGroup(f1, f2, f3).arrange(DOWN, buff=0.28, aligned_edge=RIGHT).move_to(P3(4.4, -2.45))
        self.play(FadeIn(d), run_time=0.6)
        self.ate(0.2)
        self.play(FadeIn(f1), run_time=0.6)
        self.ate(0.42)
        self.play(FadeIn(f2), run_time=0.6)
        self.ate(0.62)
        self.play(FadeIn(f3, shift=0.1 * UP), run_time=0.7)
        traco = always_redraw(lambda: self.GP.curva(P, 0.0, max(0.0, min(tau.get_value(), 1.2)), n=160))
        relog = always_redraw(lambda: MathTex(rf"t={min(tau.get_value(), 1.2):.2f}".replace(".", "{,}") + r"\ \mathrm{s}",
                                              font_size=28, color=DIM).move_to(P3(-3.4, -0.3)))
        self.add(traco, relog)
        self.ate(0.75)
        self.play(tau.animate.set_value(0.28), run_time=max(1.0, self.resta() - 0.4), rate_func=linear)
        self.ate(0.97)
        # T9-6 -----------------------------------------------------------------------------------------------
        self.an("T9-6")
        self.play(tau.animate.set_value(T2), run_time=3.0, rate_func=linear)
        pk = Dot(self.GP.pt(T2, -1.0), radius=0.07, color=WHITE_).set_z_index(9)
        lpk = MathTex(r"(0{,}51\ \mathrm{s};\ -1{,}0)", font_size=26, color=WHITE_).next_to(pk, DOWN, buff=0.12)
        para = txt("O PESADO PARA", 18, color=DIM).move_to(P3(XP0 + 0.5, Y_CH + 1.75))
        self.play(FadeIn(pk, scale=0.5), FadeIn(lpk), FadeIn(para), run_time=0.6)
        self.ate(0.45)
        self.play(tau.animate.set_value(T1), run_time=5.0, rate_func=linear)
        z = Dot(self.GP.pt(T1, 0.0), radius=0.07, color=WHITE_).set_z_index(9)
        lz = MathTex(r"(1{,}02\ \mathrm{s};\ 0)", font_size=26, color=WHITE_).next_to(z, UP, buff=0.12)
        self.play(FadeIn(z, scale=0.5), FadeIn(lz), run_time=0.6)
        self.play(tau.animate.set_value(1.2), run_time=0.8, rate_func=linear)
        self.ate(0.97)
        self.direita = VGroup(d, f1, f2, f3)
        self.traco, self.relog = traco, relog

    # ── T9-7: a Terra ──────────────────────────────────────────────────────────────────────────────────────
    def t9_7(self):
        self.an("T9-7")
        self.play(FadeOut(self.direita), FadeOut(self.lat), FadeIn(self.GT.eixos), run_time=0.7)
        u = ValueTracker(0.0)
        tt = always_redraw(lambda: self.GT.curva(lambda t: -P(t), 0.0, 1.2 * u.get_value() + 1e-3, n=160))
        self.add(tt)
        self.play(u.animate.set_value(1.0), run_time=2.0, rate_func=linear)
        lt = txt("O CHÃO GANHA, DEPOIS DEVOLVE", 18, color=DIM).move_to(P3(3.4, 0.1))
        self.play(FadeIn(lt), run_time=0.5)
        # soma dos dois gráficos = 0
        GS = Graf(1.3, -1.35, 4.2, 1.2, -0.6, 0.6, 1.0, rot_y=None)
        ls = Mc((r"P+P_{Terra}", MAG), size=32).next_to(GS.pt(0, 0.6), UP, buff=0.12).align_to(GS.pt(0, 0), LEFT)
        soma = GS.curva(lambda t: P(t) - P(t), 0.0, 1.2, n=60, cor=WHITE_, w=5)
        z0 = Mc("=", "0", size=40).next_to(GS.pt(1.0, 0), UP, buff=0.2)
        self.ate(0.35)
        self.play(FadeIn(GS.eixos), FadeIn(ls), run_time=0.6)
        self.play(Create(soma), run_time=1.2)
        self.play(FadeIn(z0), run_time=0.5)
        self.ate(0.68)
        d = dica("NÃO CONSERVA? PERGUNTE QUEM", "FICOU DE FORA DO SISTEMA")
        self.dica_entra(d)
        self.ate(0.97)
        tt.clear_updaters()
        self.traco.clear_updaters()
        self.relog.clear_updaters()
        self.dica_sai()
        self.clear(rt=0.5)
