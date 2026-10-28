"""Lote P9 (v2): T9 — escolher o sistema. Bola de 1 kg caindo 10 m em loop (só a bola × bola + Terra); blocos de 1 kg e 2 kg com mola
num chão com atrito (μ = 0,2), o experimento em câmera lenta e em loop no PALCO, com P(t) e P_Terra(t) logo abaixo e o ponto do gráfico
andando junto com os blocos. P(t) = −1,96 t até 0,510 s, depois −(2,0 − 1,96 t) até 1,020 s; P_Terra = −P."""
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


assert abs(T2 - 0.5102) < 1e-3 and abs(T1 - 1.0204) < 1e-3
assert abs(P(T2) + 1.0) < 1e-9 and abs(P(T1)) < 1e-9 and abs(P(0.3) + 1.96 * 0.3) < 1e-9 and abs(P(0.8) + (2.0 - 1.96 * 0.8)) < 1e-9
assert abs(x1(T1) + 1.0204) < 1e-3 and abs(x2(T2) - 0.2551) < 1e-3
assert abs(1 * math.sqrt(2 * G_ * 10) / 5.97e24 - 2.35e-24) < 0.01e-24

Y_CH = 0.85                    # chão dos blocos (metade de cima do PALCO)
ESC = 1.9                      # u por metro
XC = -3.6                      # centro da mola
LL, HL, LP, HP = 1.0, 1.0, 1.35, 1.3
SLOW, PER, T0P = 4.0, 7.6, 0.9  # câmera lenta ×4; período do loop; tempo parado antes do disparo


class LoteT9(Base):
    def construct(self):
        self.setup_base(cap="ESCOLHER O SISTEMA")
        self.t9_1_2()
        self.t9_3()
        self.t9_4()
        self.t9_5_6()
        self.t9_7()
        self.fim()
        self.relatorio()

    # ── T9-1, T9-2: bola e Terra, bola caindo em loop ──────────────────────────────────────────────────────
    def t9_1_2(self):
        self.an("T9-1")
        XB, YT, YB = -3.6, 2.0, -2.0
        terra = Circle(radius=7.6, arc_center=P3(XB, -9.9)).set_stroke(mix(TERRA, 0.35), 2.5).set_fill(TERRA, 1)
        lt = txt("TERRA", 22, color=GEO).move_to(P3(XB + 2.4, -3.0))
        topo = DashedLine(P3(XB - 0.9, YT), P3(XB + 0.9, YT)).set_stroke(DIM, 1.5, opacity=0.5)
        cota = VGroup(DoubleArrow(P3(XB - 1.4, YT), P3(XB - 1.4, YB - 0.28), buff=0, color=DIM, stroke_width=2, tip_length=0.12),
                      tex(r"10\ \mathrm{m}", DIM, 30).move_to(P3(XB - 1.95, (YT + YB) / 2)))
        self.terra_on = ValueTracker(0.0)
        t0 = self.clk.get_value()
        PB = 3.2

        def u_():
            s = (self.clk.get_value() - t0) % PB
            return min(1.0, (s / 2.4) ** 2), s

        def bola_cai():
            u, s = u_()
            c = P3(XB, YT - (YT - YB) * u)
            v = 14.0 * math.sqrt(u)
            g = VGroup(bola(0.3, STEEL).move_to(c))
            g.add(arrow(c, c + P3(0, -0.85), color=FC, width=6, tip=0.16, z=9))
            g.add(mtex(r"m\vec g", FC, 30).next_to(c + P3(0, -0.5), LEFT, buff=0.38))
            if v > 0.3:
                g.add(arrow(c + P3(0.55, 0), c + P3(0.55, -0.12 * v), color=MAG, width=7, tip=0.17, z=9))
                g.add(mtex(r"\vec p", MAG, 34).next_to(c + P3(0.55, -0.06 * v), RIGHT, buff=0.12))
                if self.terra_on.get_value() > 0.5:
                    sp = P3(XB + 1.6, -2.75)
                    g.add(arrow(sp, sp + P3(0, 0.12 * v), color=MAG, width=7, tip=0.17, z=9))
                    g.add(mtex(r"-\vec p", MAG, 34).next_to(sp + P3(0, 0.06 * v), RIGHT, buff=0.12))
            op = min(1.0, (PB - s) / 0.25, s / 0.12 + 0.2)
            return escala_op(g, op) if op < 1 else g
        bg = always_redraw(bola_cai)
        fr_b = always_redraw(lambda: DashedVMobject(Circle(radius=0.56, arc_center=P3(XB, YT - (YT - YB) * u_()[0]))
                                                    .set_stroke(WHITE_, 2, opacity=0.65), num_dashes=16))
        self.play(FadeIn(terra), FadeIn(lt), FadeIn(topo), FadeIn(cota), FadeIn(bg), run_time=1.0)
        ls = txt("SISTEMA: SÓ A BOLA", 22, op=0.85).move_to(P3(XB + 2.3, YT + 0.62))
        self.play(Create(fr_b), FadeIn(ls), run_time=0.8)
        r1 = MathTex(r"v=\sqrt{2gh}=14{,}0\ \mathrm{m/s}", font_size=42, color=VEL)
        r2 = linha(tex(r"\vec p", MAG, 42), "MUDA O TEMPO TODO", size=24, buff=0.18)
        r3 = txt("O PESO É EXTERNO", 24, color=FC)
        for m_, y in ((r1, 1.8), (r2, 0.85), (r3, 0.1)):
            na_conta(m_, y)
        self.ate(0.25)
        self.play(FadeIn(r1, shift=0.1 * UP), run_time=0.8)
        self.ate(0.55)
        self.play(FadeIn(r2, shift=0.1 * UP), run_time=0.7)
        self.ate(0.75)
        self.play(FadeIn(r3, shift=0.1 * UP), run_time=0.7)
        self.ate(0.97)
        # T9-2 — bola + Terra
        self.an("T9-2")
        fr_b.clear_updaters()
        big = fronteira(6.6, 5.9, P3(XB + 0.4, -0.75), rotulo=None)
        lsb = linha("SISTEMA: BOLA", mais(30), "TERRA", size=22, buff=0.12).set_opacity(0.85).move_to(ls)
        self.play(FadeOut(fr_b), Create(big[0]), FadeOut(ls), FadeIn(lsb), FadeOut(r2), FadeOut(r3), run_time=1.4)
        self.terra_on.set_value(1.0)
        ie = txt("A FORÇA ENTRE ELAS FICA INTERNA", 22, color=INT)
        na_conta(ie, 0.85)
        self.play(FadeIn(ie), run_time=0.6)
        e0 = Mc((r"\vec P_{\text{total}}", MAG), "=", "0", size=50)
        n0 = txt("EM TODO INSTANTE", 20, color=DIM)
        na_conta(e0, -0.1); na_conta(n0, -0.75)
        self.ate(0.3)
        self.play(FadeIn(e0, shift=0.1 * UP), FadeIn(n0), run_time=0.8)
        et = MathTex(r"v_{\text{Terra}}=\frac{1\cdot 14}{5{,}97\times10^{24}}\approx 2{,}3\times10^{-24}\ \mathrm{m/s}", font_size=36, color=VEL)
        na_conta(et, -1.85)
        ni = txt("IMPOSSÍVEL DE PERCEBER", 18, color=DIM)
        na_conta(ni, -2.65)
        self.ate(0.6)
        self.play(FadeIn(et, shift=0.1 * UP), run_time=0.9)
        self.ate(0.8)
        self.play(FadeIn(ni), run_time=0.5)
        self.ate(0.97)
        bg.clear_updaters()

    # ── experimento dos blocos (loop em câmera lenta) ──────────────────────────────────────────────────────
    def tau(self, t0):
        """Tempo físico do experimento no instante atual (−1 = antes do disparo) e a opacidade da troca de ciclo."""
        s = (self.clk.get_value() - t0) % PER
        op = min(1.0, (PER - s) / 0.3, s / 0.3 + 0.15)
        if s < T0P:
            return -1.0, op
        return min((s - T0P) / SLOW, 1.2), op

    def blocos(self, t0, iguais=False, forcas=False, setas_v=True):
        def f():
            t, op = self.tau(t0)
            if iguais:
                ve = 1.5
                T = ve / AF
                tc = min(max(t, 0), T)
                d = ve * tc - AF * tc * tc / 2
                xa, xb = XC - 0.5 - LP / 2 - ESC * d, XC + 0.5 + LP / 2 + ESC * d
                va, vb = (-(ve - AF * tc), ve - AF * tc) if 0 <= t < T else (0.0, 0.0)
                la, ha, lb, hb = LP, HP, LP, HP
                fa, fb = (MU * 1.5 * G_, -MU * 1.5 * G_) if 0 <= t < T else (0, 0)
            else:
                xa, xb = XC - 0.5 - LL / 2 + ESC * x1(max(t, 0)), XC + 0.5 + LP / 2 + ESC * x2(max(t, 0))
                va, vb = (v1(t), v2(t)) if t >= 0 else (0.0, 0.0)
                la, ha, lb, hb = LL, HL, LP, HP
                fa = F1 if 0 <= t < T1 else 0.0
                fb = F2 if 0 <= t < T2 else 0.0
            A = Corpo("", STEEL if iguais else GEO, la, ha).at(xa, Y_CH)
            B = Corpo("", STEEL, lb, hb).at(xb, Y_CH)
            g = VGroup(A, B, mtex(r"m" if iguais else r"1\ \mathrm{kg}", WHITE_ if iguais else BACKGROUND_COLOR, 30).move_to(A),
                       mtex(r"m" if iguais else r"2\ \mathrm{kg}", WHITE_, 32).move_to(B))
            if t < 0.02:
                g.add(mola(P3(xa + la / 2, Y_CH + 0.42), P3(xb - lb / 2, Y_CH + 0.42), n=6, amp=0.12))
            if forcas and t >= 0:
                if abs(fa) > 0:
                    g.add(arrow(P3(xa, Y_CH - 0.28), P3(xa + 0.32 * fa, Y_CH - 0.28), color=FC, width=7, tip=0.17, z=10))
                if abs(fb) > 0:
                    g.add(arrow(P3(xb, Y_CH - 0.28), P3(xb + 0.32 * fb, Y_CH - 0.28), color=FC, width=7, tip=0.17, z=10))
            if setas_v:
                yv = Y_CH + max(ha, hb) + 0.35
                for x, v in ((xa, va), (xb, vb)):
                    if abs(v) > 0.04:
                        g.add(arrow(P3(x, yv), P3(x + 0.55 * v, yv), color=VEL, width=6, tip=0.16, z=10))
            return escala_op(g, op) if op < 1 else g
        return f

    def t9_3(self):
        self.an("T9-3")
        self.clear(rt=0.6)
        self.piso = chao(-7.3, 0.6, Y_CH, dens=3.0)
        self.lat = txt("CHÃO COM ATRITO", 16, color=DIM).move_to(P3(-1.0, Y_CH - 0.5))
        self.eixo = VGroup(arrow(P3(-1.7, 2.5), P3(-0.7, 2.5), color=DIM, width=3, tip=0.13), tex(r"+x", DIM, 30).move_to(P3(-0.35, 2.5)))
        self.t0 = self.clk.get_value() + 0.6
        bg = always_redraw(self.blocos(self.t0))
        tl = txt("LEVE", 18, color=DIM).move_to(P3(XC - 1.6, Y_CH + HP + 0.95))
        tp = txt("PESADO", 18, color=DIM).move_to(P3(XC + 1.4, Y_CH + HP + 0.95))
        self.play(FadeIn(self.piso), FadeIn(self.lat), FadeIn(bg), FadeIn(tl), FadeIn(tp), run_time=1.0)
        self.ate(0.3)
        self.play(FadeIn(self.eixo), run_time=0.6)
        d1 = Mc((r"v_1=-2\ \mathrm{m/s}", VEL), size=40)
        d2 = Mc((r"v_2=+1\ \mathrm{m/s}", VEL), size=40)
        na_conta(d1, 1.8); na_conta(d2, 1.15)
        self.ate(0.5)
        self.play(FadeIn(d1, shift=0.1 * UP), FadeIn(d2, shift=0.1 * UP), run_time=0.8)
        pm = Mc((r"p_1=-2", MAG), ",", (r"\ p_2=+2\ \mathrm{kg\cdot m/s}", MAG), size=40)
        p0 = Mc((r"P", MAG), "=", "0", size=48)
        lg = txt("LOGO DEPOIS DO DISPARO", 18, color=DIM)
        na_conta(pm, 0.1); na_conta(p0, -0.75); na_conta(lg, -1.35)
        self.ate(0.75)
        self.play(FadeIn(pm, shift=0.1 * UP), run_time=0.7)
        self.play(FadeIn(p0, shift=0.1 * UP), FadeIn(lg), run_time=0.6)
        self.ate(0.97)
        self.bg, self.tl = bg, VGroup(tl, tp)
        self.conta3 = VGroup(d1, d2, pm, p0, lg)

    # ── gráficos P(t) e P_Terra(t), no PALCO, logo abaixo dos blocos ───────────────────────────────────────
    def graficos(self):
        self.GP = Graf(-6.7, -1.0, 6.3, 1.2, -1.0, 0.2, 1.0, rot_y=tex(r"P", MAG, 32))
        self.GT = Graf(-6.7, -3.35, 6.3, 1.2, -0.05, 1.0, 0.85, rot_y=tex(r"P_{\text{Terra}}", MAG, 28))
        for G, ys in ((self.GP, (-1.0,)), (self.GT, (1.0,))):
            for y in ys:
                G.eixos.add(DashedLine(G.pt(0, y), G.pt(1.2, y), dash_length=0.06).set_stroke(DIM, 1, opacity=0.4))
                G.eixos.add(tex(f"{y:+.1f}".replace(".", "{,}"), DIM, 22).next_to(G.pt(0, y), LEFT, buff=0.12))
        self.GP.eixos.add(tex(r"\mathrm{kg\cdot m/s}", DIM, 22).next_to(self.GP.ey, RIGHT, buff=0.15))

    def traco(self, G, fun, t0, cor=MAG):
        def f():
            t, op = self.tau(t0)
            g = VGroup()
            if t > 0:
                g.add(G.curva(fun, 0.0, t, n=80, cor=cor))
                g.add(Dot(G.pt(t, fun(t)), radius=0.07, color=WHITE_).set_z_index(9))
            return escala_op(g, op) if op < 1 else g
        return always_redraw(f)

    # ── T9-4: massas iguais ───────────────────────────────────────────────────────────────────────────────
    def t9_4(self):
        self.an("T9-4")
        self.graficos()
        self.bg.clear_updaters()
        self.play(FadeOut(self.bg), FadeOut(self.tl), FadeOut(self.conta3), FadeIn(self.GP.eixos), run_time=0.7)
        self.remove(self.bg)
        t0 = self.clk.get_value()
        bi = always_redraw(self.blocos(t0, iguais=True, forcas=True))
        cu = self.traco(self.GP, lambda t: 0.0, t0)
        tit = txt("MASSAS IGUAIS", 26, bold=True)
        r1 = txt("ATRITOS IGUAIS E OPOSTOS", 20, color=FC)
        r0 = Mc((r"P(t)", MAG), "=", "0", size=44)
        r2 = txt("PARAM JUNTOS", 20, color=DIM)
        for m_, y in ((tit, 1.8), (r1, 1.15), (r0, 0.2), (r2, -0.45)):
            na_conta(m_, y)
        self.play(FadeIn(bi), FadeIn(cu), FadeIn(tit), run_time=0.6)
        self.ate(0.3)
        self.play(FadeIn(r1), run_time=0.6)
        self.ate(0.6)
        self.play(FadeIn(r0, shift=0.1 * UP), FadeIn(r2), run_time=0.7)
        self.ate(0.95)
        bi.clear_updaters(); cu.clear_updaters()
        self.play(FadeOut(bi), FadeOut(cu), FadeOut(VGroup(tit, r1, r0, r2)), run_time=0.5)
        self.remove(bi, cu)

    # ── T9-5, T9-6: massas diferentes, P(t) ───────────────────────────────────────────────────────────────
    def t9_5_6(self):
        self.an("T9-5")
        t0 = self.t0p = self.clk.get_value()
        bg = always_redraw(self.blocos(t0, forcas=True))
        cu = self.traco(self.GP, P, t0)
        relog = always_redraw(lambda: mtex(rf"t={max(0.0, self.tau(t0)[0]):.2f}".replace(".", "{,}") + r"\ \mathrm{s}", DIM, 28)
                              .move_to(P3(-3.3, -0.5)))
        self.play(FadeIn(bg), FadeIn(cu), FadeIn(relog), run_time=0.6)
        d = MathTex(r"m_1=1\ \mathrm{kg},\ m_2=2\ \mathrm{kg},\ \mu=0{,}2", font_size=34, color=WHITE_)
        f1 = linha("ATRITO NO LEVE", tex(r"+1{,}96\ \mathrm{N}", FC, 36), size=20, buff=0.2)
        f2 = linha("ATRITO NO PESADO", tex(r"-3{,}92\ \mathrm{N}", FC, 36), size=20, buff=0.2)
        f3 = linha("RESULTANTE", tex(r"-1{,}96\ \mathrm{N}", FC, 40), size=22, buff=0.2)
        for m_, y in ((d, 2.0), (f1, 1.2), (f2, 0.55), (f3, -0.2)):
            na_conta(m_, y)
        self.play(FadeIn(d), run_time=0.6)
        self.ate(0.2)
        self.play(FadeIn(f1), run_time=0.6)
        self.ate(0.42)
        self.play(FadeIn(f2), run_time=0.6)
        self.ate(0.62)
        self.play(FadeIn(f3, shift=0.1 * UP), run_time=0.7)
        dc = txt("O MOMENTO TOTAL DESCE", 18, color=MAG)
        na_conta(dc, -0.85)
        self.ate(0.8)
        self.play(FadeIn(dc), run_time=0.5)
        self.ate(0.97)
        # T9-6 — o pesado para em 0,51 s (pico); o leve para em 1,02 s
        self.an("T9-6")
        pk = Dot(self.GP.pt(T2, -1.0), radius=0.075, color=WHITE_).set_z_index(9)
        lpk = MathTex(r"(0{,}51\ \mathrm{s};\ -1{,}0)", font_size=24, color=WHITE_).next_to(pk, DOWN, buff=0.12)
        z = Dot(self.GP.pt(T1, 0.0), radius=0.075, color=WHITE_).set_z_index(9)
        lz = MathTex(r"(1{,}02\ \mathrm{s};\ 0)", font_size=24, color=WHITE_).next_to(z, UP, buff=0.12)
        r1 = linha(txt("PESADO PARA:", 20, color=DIM), tex(r"t=0{,}51\ \mathrm{s},\ P=-1{,}0", MAG, 34), buff=0.2)
        r2 = linha(txt("LEVE PARA:", 20, color=DIM), tex(r"t=1{,}02\ \mathrm{s},\ P=0", MAG, 34), buff=0.2)
        self.play(FadeOut(VGroup(d, f1, f2, dc)), f3.animate.move_to(P3(XC0 + f3.width / 2, 2.0)), run_time=0.6)
        na_conta(r1, 1.1); na_conta(r2, 0.3)
        self.ate(0.2)
        self.play(FadeIn(pk, scale=0.5), FadeIn(lpk), FadeIn(r1), run_time=0.7)
        self.ate(0.6)
        self.play(FadeIn(z, scale=0.5), FadeIn(lz), FadeIn(r2), run_time=0.7)
        self.ate(0.97)
        self.bg, self.cu, self.relog = bg, cu, relog
        self.conta6 = VGroup(f3, r1, r2)
        self.marcas = VGroup(pk, lpk, z, lz)

    # ── T9-7: a Terra ─────────────────────────────────────────────────────────────────────────────────────
    def t9_7(self):
        self.an("T9-7")
        t0 = self.t0p
        self.play(FadeOut(self.conta6), FadeOut(self.lat), FadeIn(self.GT.eixos), run_time=0.7)
        ct = self.traco(self.GT, lambda t: -P(t), t0)
        self.add(ct)
        lt = txt("O CHÃO GANHA, DEPOIS DEVOLVE", 18, color=DIM)
        na_conta(lt, -0.9)
        self.play(FadeIn(lt), run_time=0.5)
        GS = Graf(1.6, 0.9, 4.6, 1.2, -0.6, 0.6, 1.0, rot_y=None)
        ls = Mc((r"P+P_{\text{Terra}}", MAG), size=32).next_to(GS.pt(0, 0.6), UP, buff=0.12).align_to(GS.pt(0, 0), LEFT)
        soma = GS.curva(lambda t: P(t) - P(t), 0.0, 1.2, n=60, cor=WHITE_, w=5)
        z0 = Mc("=", "0", size=40).next_to(GS.pt(1.0, 0), UP, buff=0.2)
        at = txt("A TODO INSTANTE", 18, color=DIM).next_to(GS.pt(0.6, 0), DOWN, buff=0.45)
        self.ate(0.3)
        self.play(FadeIn(GS.eixos), FadeIn(ls), run_time=0.6)
        self.play(Create(soma), run_time=1.2)
        self.play(FadeIn(z0), FadeIn(at), run_time=0.5)
        self.ate(0.62)
        d = dica("NÃO CONSERVA? PERGUNTE QUEM", "FICOU DE FORA DO SISTEMA")
        self.dica_entra(d)
        self.ate(0.97)
        for m_ in (self.bg, self.cu, self.relog, ct):
            m_.clear_updaters()
        self.dica_sai()
        self.clear(rt=0.5)
