"""Lote C: C07 (de volta ao muro) e C08 (a pulga)."""
from kit import *  # noqa: F401,F403

M_PES, H_MURO, G_ = 80.0, 2.5, 9.8
V_CHEGADA = math.sqrt(2 * G_ * H_MURO)           # 7,0 m/s
DP = M_PES * V_CHEGADA                           # 560 kg·m/s = N·s
DT_DURA, DT_JOELHO = 0.01, 2 * 0.5 / V_CHEGADA   # 0,01 s ; 1/7 s ≈ 0,14 s (meio metro de agachamento)
PESO = M_PES * G_                                # 784 N


def tex(s, cor=WHITE_, size=M_MID):
    return MathTex(s, font_size=size, color=cor)


class LoteC(Base):
    def construct(self):
        self.setup_base(cap="EXERCÍCIO 3 · FORÇA QUE CRESCE COM O TEMPO", selo="SEARS · EXERC. 8.11")
        self.c07()
        self.c08()
        self.fim()
        self.relatorio()

    # ── C07 ─────────────────────────────────────────────────────────────────────────────────────────────────
    def c07(self):
        self.clear(rt=0.6)
        self.secao("EXERCÍCIO 4 · DE VOLTA AO MURO", "MOYSÉS · PROB. 9.1")
        self.an("C07-1")
        piso = Line(P3(-7.6, -3.2), P3(-0.4, -3.2)).set_stroke(GEO, 2.5, opacity=0.55)
        h = 2.5 * 0.9
        muro = Rectangle(width=1.0, height=h).set_stroke(GEO, 2).set_fill(STEEL, 0.35).move_to(P3(-5.0, -3.2 + h / 2))
        pes = Pessoa(GEO, esc=0.75).pose(-4.9, -3.2 + h, None)
        cota = VGroup(DoubleArrow(P3(-5.9, -3.18), P3(-5.9, -3.2 + h - 0.02), buff=0, color=GEO, stroke_width=3, tip_length=0.14),
                      tex(r"2{,}5\ \mathrm{m}", GEO, 30).move_to(P3(-5.9, -3.2 + h / 2)))
        cota[1].next_to(cota[0], LEFT, buff=0.08)
        dados = tex(r"m=80\ \mathrm{kg}", WHITE_, 44).move_to(P3(3.4, 2.2))
        dados2 = tex(r"h=2{,}5\ \mathrm{m}", WHITE_, 44).next_to(dados, DOWN, buff=0.3, aligned_edge=LEFT)
        vv = Mc((r"v=\sqrt{2\cdot 9{,}8\cdot 2{,}5}=7{,}0\ \mathrm{m/s}", VEL), size=44).move_to(P3(3.4, -0.2))
        self.play(FadeIn(piso), FadeIn(muro), FadeIn(pes), FadeIn(cota), run_time=0.8)
        self.play(FadeIn(dados), FadeIn(dados2), run_time=0.7)
        self.ate(0.45)
        self.play(FadeIn(vv, shift=0.1 * UP), run_time=0.8)
        # queda curta de ilustração
        tau = ValueTracker(0.0)
        y0 = -3.2 + h

        def pos(m):
            s = tau.get_value()
            m.pose(-4.9 + 2.8 * s, y0 - h * s * s, None)
        pes.add_updater(pos)
        self.ate(0.6)
        self.play(tau.animate.set_value(1.0), run_time=1.4, rate_func=linear)
        pes.clear_updaters()
        self.ate(0.97)
        # C07-2 ----------------------------------------------------------------------------------------------
        self.an("C07-2")
        self.play(FadeOut(dados), FadeOut(dados2), run_time=0.4)
        dp = Mc((r"\Delta p=80\cdot7{,}0=560\ \mathrm{kg\cdot m/s}", MAG), size=44).move_to(P3(3.4, 1.7))
        igual = txt("IGUAL NOS DOIS CASOS", T_LAB, color=MAG).next_to(dp, DOWN, buff=0.35)
        self.play(FadeIn(dp, shift=0.1 * UP), run_time=0.9)
        self.ate(0.5)
        self.play(FadeIn(igual), run_time=0.6)
        self.ate(0.97)
        # C07-3 ----------------------------------------------------------------------------------------------
        self.an("C07-3")
        self.clear(rt=0.6)
        FMAX = 7000.0
        gh, gy = 3.6, -2.0
        Ga = Graf(-6.5, gy, 4.4, gh, 0.02, FMAX, MathTex(r"F_{res}", font_size=36, color=FC))
        Gb = Graf(0.0, gy, 6.6, gh, 0.20, FMAX, MathTex(r"F_{res}", font_size=36, color=FC))
        fa = meia_senoide(DP, DT_DURA)
        fb = meia_senoide(DP, DT_JOELHO)
        la = txt("PERNAS DURAS", T_LAB, bold=True).move_to(P3(-4.2, 2.35))
        lb = txt("JOELHOS", T_LAB, bold=True).move_to(P3(3.2, 2.35))
        ca, cb = Ga.curva(fa, 0, 0.02, n=400), Gb.curva(fb, 0, 0.20, n=400)
        ara, arb = Ga.area(fa, 0, DT_DURA, n=200), Gb.area(fb, 0, DT_JOELHO, n=200)
        Ja, Jb = area_num(fa, 0, DT_DURA), area_num(fb, 0, DT_JOELHO)
        print(f"[QA] C07-3 áreas: pernas duras {Ja:.3f} N·s, joelhos {Jb:.3f} N·s (alvo 560); picos {max(fa(t) for t in np.linspace(0, DT_DURA, 999)):.0f} N e {max(fb(t) for t in np.linspace(0, DT_JOELHO, 999)):.0f} N")
        pico = Mc((r"\uparrow\ \mathrm{pico}\approx 88.000\ \mathrm{N}", FC), size=30).move_to(P3(-3.1, 0.7))
        dta = Mc((r"\Delta t=0{,}01\ \mathrm{s}", DIM), size=30).move_to(Ga.pt(0.014, 0) + P3(0.0, -0.45))
        dtb = Mc((r"\Delta t\approx0{,}14\ \mathrm{s}", DIM), size=30).move_to(Gb.pt(0.10, 0) + P3(0.0, -0.45))
        ala = Mc((r"\text{ÁREA}=560\ \mathrm{N\cdot s}", JC), size=30).move_to(P3(-4.2, -3.35))
        alb = Mc((r"\text{ÁREA}=560\ \mathrm{N\cdot s}", JC), size=30).move_to(P3(3.2, -3.35))
        self.play(FadeIn(Ga.eixos), FadeIn(Gb.eixos), FadeIn(la), FadeIn(lb), run_time=0.8)
        self.play(Create(ca), Create(cb), run_time=1.4)
        self.ate(0.4)
        self.play(FadeIn(ara), FadeIn(arb), FadeIn(ala), FadeIn(alb), run_time=1.0)
        self.ate(0.7)
        self.play(FadeIn(dta), FadeIn(dtb), FadeIn(pico), run_time=0.8)
        self.ate(0.97)
        # C07-4 ----------------------------------------------------------------------------------------------
        self.an("C07-4")
        fma, fmb = DP / DT_DURA, DP / DT_JOELHO
        print(f"[QA] C07-4 F_res,méd: {fma:.0f} N e {fmb:.0f} N")
        rb = Gb.retangulo(0.0, DT_JOELHO, fmb)
        ma = Mc((r"F_{res,\mathrm{m\acute{e}d}}=56.000\ \mathrm{N}", FC), size=32).move_to(P3(-4.2, -3.9))
        mb = Mc((r"F_{res,\mathrm{m\acute{e}d}}=3.920\ \mathrm{N}", FC), size=32).move_to(P3(3.2, -3.9))
        self.play(FadeOut(ala), FadeOut(alb), run_time=0.3)
        self.play(Create(rb), FadeIn(ma), FadeIn(mb), run_time=1.2)
        self.ate(0.97)
        # C07-5 ----------------------------------------------------------------------------------------------
        self.an("C07-5")
        banda_a = Rectangle(width=Ga.w * 0.02 / Ga.tmax * 1.0, height=Ga.h * PESO / FMAX).set_stroke(width=0).set_fill(FC, 0.8)
        banda_a.move_to((Ga.pt(0, 0) + Ga.pt(0.02, PESO)) / 2).set_z_index(8)
        banda_b = Rectangle(width=Gb.w, height=Gb.h * PESO / FMAX).set_stroke(width=0).set_fill(FC, 0.8)
        banda_b.move_to((Gb.pt(0, 0) + Gb.pt(0.2, PESO)) / 2).set_z_index(8)
        pw = Mc((r"m g=784\ \mathrm{N}", FC), size=28).move_to(P3(0.0, 2.35))
        na = Mc((r"N\approx72\ \mathrm{pesos}", FC), size=34).move_to(P3(-4.2, -3.9))
        nb = Mc((r"N\approx6\ \mathrm{pesos}", FC), size=34).move_to(P3(3.2, -3.9))
        nn = Mc((r"N=F_{res}+m g", FC), size=40).move_to(P3(-0.3, 2.6))
        self.play(FadeOut(ma), FadeOut(mb), FadeOut(rb), FadeOut(pico), FadeOut(dta), FadeOut(dtb), run_time=0.4)
        self.play(FadeIn(nn), run_time=0.7)
        self.play(FadeIn(banda_a), FadeIn(banda_b), run_time=0.8)
        self.ate(0.6)
        self.play(FadeIn(na), FadeIn(nb), run_time=0.8)
        print(f"[QA] C07-5 N/(m g): {(fma + PESO) / PESO:.1f} e {(fmb + PESO) / PESO:.1f}")
        self.ate(0.97)
        # C07-6 ----------------------------------------------------------------------------------------------
        self.an("C07-6")
        self.clear(rt=0.6)
        fr = txt("MESMO IMPULSO. MAIS TEMPO. MENOS FORÇA.", 40, bold=True).move_to(P3(0, 0.6))
        sub = txt("PERGUNTA RESPONDIDA", T_LAB, color=DIM).move_to(P3(0, 1.7))
        self.play(FadeIn(sub), FadeIn(fr, shift=0.1 * UP), run_time=1.0)
        self.ate(0.97)
        # C07-7 ----------------------------------------------------------------------------------------------
        self.an("C07-7")
        self.play(FadeOut(sub), fr.animate.move_to(P3(0, 2.4)).scale(0.7), run_time=0.7)
        linhas = [(txt("SAQUE DE TÊNIS", T_MAIN), tex(r"\approx 49\ \mathrm{kgf}", WHITE_, 44)),
                  (txt("PÊNALTI", T_MAIN), tex(r"\approx 92\ \mathrm{kgf}", WHITE_, 44)),
                  (txt("CARRO A 60 KM/H NO MURO", T_MAIN), tex(r"\approx 25\ \mathrm{tf}", WHITE_, 44))]
        ys = (0.9, -0.3, -1.5)
        for (a, b), y in zip(linhas, ys):
            a.move_to(P3(-1.5, y))
            a.align_to(np.array([-5.8, 0, 0]), LEFT)
            b.move_to(P3(5.6, y)).align_to(np.array([6.4, 0, 0]), RIGHT)
        self.play(*[FadeIn(a, shift=0.1 * UP) for a, _ in linhas[:1]], *[FadeIn(b) for _, b in linhas[:1]], run_time=0.7)
        self.ate(0.4)
        self.play(FadeIn(linhas[1][0], shift=0.1 * UP), FadeIn(linhas[1][1]), run_time=0.7)
        self.ate(0.6)
        self.play(FadeIn(linhas[2][0], shift=0.1 * UP), FadeIn(linhas[2][1]), run_time=0.7)
        self.ate(0.97)

    # ── C08 — a pulga ───────────────────────────────────────────────────────────────────────────────────────
    def pulga(self, esc=1.0):
        corpo = Ellipse(width=0.55 * esc, height=0.32 * esc).set_stroke(mix(STEEL, 0.5), 2).set_fill(STEEL, 1.0)
        cab = Circle(radius=0.11 * esc).set_stroke(mix(STEEL, 0.5), 2).set_fill(GEO, 1.0).move_to(corpo.get_center() + P3(0.36 * esc, 0.03 * esc))
        pernas = VGroup(*[Line(corpo.get_center() + P3(dx * esc, -0.1 * esc), corpo.get_center() + P3((dx - 0.1) * esc, -0.34 * esc))
                          .set_stroke(GEO, 3) for dx in (-0.18, 0.0, 0.16)])
        return VGroup(pernas, corpo, cab)

    def c08(self):
        self.clear(rt=0.6)
        self.secao("EXERCÍCIO 5 · A PULGA", "MOYSÉS · PROB. 4.7")
        self.an("C08-1")
        chao = Line(P3(-7.5, -3.2), P3(-0.8, -3.2)).set_stroke(GEO, 2.5, opacity=0.55)
        cota = DoubleArrow(P3(-7.0, -3.2), P3(-7.0, 0.4), buff=0, color=GEO, stroke_width=3, tip_length=0.14)
        h_lab = tex(r"h=50\ \mathrm{cm}", GEO, 34).next_to(cota, RIGHT, buff=0.12)
        pu = self.pulga(1.0).move_to(P3(-4.5, -3.0))
        ref = DashedLine(P3(-7.2, 0.4), P3(-2.2, 0.4), color=DIM, stroke_width=2)
        dados = VGroup(tex(r"m=2\ \mathrm{mg}", WHITE_, 44), tex(r"d=1\ \mathrm{mm}", WHITE_, 44)) \
            .arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(P3(4.0, 2.1))
        self.play(FadeIn(chao), FadeIn(pu), run_time=0.7)
        self.play(FadeIn(cota), FadeIn(h_lab), FadeIn(ref), run_time=0.8)
        self.ate(0.35)
        self.play(pu.animate.shift(UP * 3.3), run_time=1.0, rate_func=rush_from)
        self.play(pu.animate.shift(DOWN * 3.3), run_time=1.0, rate_func=rush_into)
        # zoom: patas esticam 1 mm
        zoom = placa(3.4, 2.2, P3(-4.3, -1.6), op=0.08).set_z_index(-1)
        zl = txt("ZOOM", T_SMALL, color=DIM).move_to(P3(-4.3, -0.65))
        zpu = self.pulga(1.4).move_to(P3(-4.3, -1.7))
        zd = DoubleArrow(P3(-3.2, -2.5), P3(-3.2, -1.95), buff=0, color=GEO, stroke_width=2.5, tip_length=0.1)
        zd_l = tex(r"d=1\ \mathrm{mm}", GEO, 28).next_to(zd, RIGHT, buff=0.1)
        self.play(FadeIn(zoom), FadeIn(zl), FadeIn(zpu), run_time=0.7)
        self.play(zpu.animate.shift(UP * 0.28), FadeIn(zd), FadeIn(zd_l), run_time=0.9)
        self.play(FadeIn(dados), run_time=0.6)
        self.ate(0.97)
        # C08-2 ----------------------------------------------------------------------------------------------
        self.an("C08-2")
        vv = Mc((r"v=\sqrt{2gh}=3{,}13\ \mathrm{m/s}", VEL), size=44).move_to(P3(4.0, -0.2))
        self.play(FadeIn(vv, shift=0.1 * UP), run_time=0.9)
        self.ate(0.97)
        # C08-3 ----------------------------------------------------------------------------------------------
        self.an("C08-3")
        self.play(FadeOut(dados), FadeOut(vv), run_time=0.4)
        c1 = txt("CAMINHO 1", T_LAB, color=DIM).move_to(P3(4.0, 2.7))
        e1 = Mc("a", "=", r"\frac{v^{2}}{2d}", "=", r"\frac{g\,h}{d}", "=", r"500\,g", size=44).move_to(P3(4.0, 1.5))
        self.play(FadeIn(c1), FadeIn(e1, shift=0.1 * UP), run_time=1.0)
        self.ate(0.97)
        # C08-4 ----------------------------------------------------------------------------------------------
        self.an("C08-4")
        c2 = txt("CAMINHO 2", T_LAB, color=DIM).move_to(P3(4.0, 0.2))
        e2 = Mc(r"\Delta t", "=", r"\frac{2d}{v}", "=", r"0{,}64\ \mathrm{ms}", size=44).move_to(P3(4.0, -0.9))
        e3 = Mc((r"F_{res}", FC), "=", r"\frac{m\,v}{\Delta t}", "=", r"m\,a", size=44).move_to(P3(4.0, -2.3))
        self.play(FadeIn(c2), FadeIn(e2, shift=0.1 * UP), run_time=1.0)
        self.ate(0.45)
        self.play(FadeIn(e3, shift=0.1 * UP), run_time=1.0)
        self.ate(0.7)
        self.play(Indicate(e3[4], color=WHITE_), Indicate(e1[0], color=WHITE_), run_time=1.0)
        self.ate(0.97)
        # C08-5 ----------------------------------------------------------------------------------------------
        self.an("C08-5")
        self.play(*[FadeOut(m) for m in (c1, e1, c2, e2, e3)], run_time=0.4)
        n1 = Mc((r"N", FC), "=", r"m\,(a+g)", "=", r"m\,g\,(\frac{h}{d}", r"+1)", size=44).move_to(P3(4.0, 1.0))
        n2 = Mc((r"N", FC), "=", (r"501\ \mathrm{pesos}", FC), size=48).move_to(P3(4.0, -0.5))
        nao = txt("NÃO 500", T_LAB, color=APAGADO).move_to(P3(4.0, -1.5))
        self.play(FadeIn(n1, shift=0.1 * UP), run_time=1.0)
        self.ate(0.45)
        self.play(Indicate(n1[5], color=WHITE_, scale_factor=1.35), run_time=1.0)
        self.play(Indicate(n1[5], color=WHITE_, scale_factor=1.35), run_time=1.0)
        self.play(FadeIn(n2, shift=0.1 * UP), FadeIn(nao), run_time=0.8)
        self.ate(0.97)
        # C08-6 ----------------------------------------------------------------------------------------------
        self.an("C08-6")
        self.play(*[FadeOut(m) for m in (n1, n2, nao)], run_time=0.4)
        n3 = Mc((r"N\approx9{,}8\times10^{-3}\ \mathrm{N}\approx1{,}0\times10^{-3}\ \mathrm{kgf}", FC), size=36, w=6.6).move_to(P3(4.2, 1.8))
        pes = Pessoa(GEO, esc=0.8).pose(2.6, -3.1, None)
        pl = tex(r"70\ \mathrm{kg}", WHITE_, 36).move_to(P3(2.6, -0.7))
        bloco = Corpo("", STEEL, 1.3, 1.0).at(5.8, -3.1)
        bl = tex(r"35\ \mathrm{t}", WHITE_, 40).move_to(P3(5.8, -1.7))
        self.play(FadeIn(n3, shift=0.1 * UP), run_time=0.9)
        self.ate(0.4)
        self.play(FadeIn(pes), FadeIn(pl), FadeIn(bloco), FadeIn(bl), run_time=0.9)
        self.ate(0.97)
