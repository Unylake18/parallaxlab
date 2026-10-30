"""Lote P8: T8 — força interna não move o sistema. Cavalo 600 kg + pedra 800 kg (μc = 0,3): 2.352 N, 2.800 N, 448 N → 0,32 m/s²;
T = 2.608 N e 192 N; gelo sob as patas (588 N); Cyrano; andar."""
from kit import *  # noqa: F401,F403
from sec_cavalo import Tropa

G_ = 9.8
M_CAV, M_PED, MU_C, F_CHAO = 600.0, 800.0, 0.3, 2800.0
F_PED = MU_C * M_PED * G_                         # 2352
A_SIS = (F_CHAO - F_PED) / (M_CAV + M_PED)        # 0,32
TENS = F_PED + M_PED * A_SIS                      # 2608
RES_CAV = F_CHAO - TENS                           # 192
F_GELO = 0.1 * M_CAV * G_                         # 588
assert abs(F_PED - 2352) < 1e-9 and abs(A_SIS - 0.32) < 1e-12 and abs(TENS - 2608) < 1e-9 and abs(RES_CAV - 192) < 1e-9
assert abs(RES_CAV - M_CAV * A_SIS) < 1e-9 and abs(F_GELO - 588) < 1e-9
S = 1 / 1600                                      # u por newton
Y_CH = -1.5
XR = 4.0                                          # centro da coluna da direita


def num(s, cor=WHITE_, size=M_LAB):
    return MathTex(s, font_size=size, color=cor)


class LoteT8(Base):
    def construct(self):
        self.setup_base(cap="FORÇA INTERNA NÃO MOVE O SISTEMA", selo="MOYSÉS §8.1–8.3")
        self.cena()
        self.t8_1()
        self.t8_2_3_4()
        self.t8_5_6()
        self.t8_7()
        self.t8_8()
        self.fim()
        self.relatorio()

    # ── a cena (cavalo, corda, pedra, forças) ────────────────────────────────────────────────────────────────
    def cena(self):
        self.tr = tr = Tropa(esc=0.62, xc=-1.75, xp=-5.55, y=Y_CH)
        self.fchao = ValueTracker(F_CHAO)
        self.op_int, self.op_ext, self.op_vert = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        self.op_val = ValueTracker(0.0)          # rótulos numéricos
        self.op_tval = ValueTracker(0.0)         # valor da tensão
        self.base_dx = 0.0

        def forcas():
            p = tr.pts()
            u = tr.dir_corda()
            n = P3(-u[1], u[0])
            g = VGroup()
            oi, oe, ov, on, ot = (self.op_int.get_value(), self.op_ext.get_value(), self.op_vert.get_value(), self.op_val.get_value(),
                                  self.op_tval.get_value())
            if oi > 0.01:
                g.add(arrow(p["gancho"] + 0.08 * u, p["gancho"] + (0.08 + TENS * S * 0.6) * u, color=INT, width=6, tip=0.18, op=oi, z=9))
                g.add(arrow(p["traseira"] - 0.04 * u, p["traseira"] - (0.04 + TENS * S * 0.6) * u, color=INT, width=6, tip=0.18, op=oi, z=9))
                g.add(mtex(r"\vec T", INT, 32).set_opacity(oi).move_to(p["gancho"] + 0.55 * u + 0.38 * n))
                g.add(mtex(r"-\vec T", INT, 32).set_opacity(oi).move_to(p["traseira"] - 0.55 * u + 0.38 * n))
                meio = (p["gancho"] + p["traseira"]) / 2
                g.add(mtxt("INTERNA", 18, color=INT, op=oi).move_to(meio - 0.36 * n + P3(0.1, 0)))
                if ot > 0.01:
                    g.add(mtex(r"2.608\ \mathrm{N}", INT, 26).set_opacity(ot).move_to(p["gancho"] + 0.55 * u + 0.78 * n))
                    g.add(mtex(r"2.608\ \mathrm{N}", INT, 26).set_opacity(ot).move_to(p["traseira"] - 0.55 * u + 0.78 * n))
            if oe > 0.01:
                xh = p["cav"][0]
                fc = self.fchao.get_value()
                g.add(arrow(P3(xh, Y_CH - 0.3), P3(xh + fc * S, Y_CH - 0.3), color=FC, width=7, tip=0.2, op=oe, z=9))
                xp_ = p["ped"][0] + 0.45
                g.add(arrow(P3(xp_, Y_CH - 0.3), P3(xp_ - F_PED * S, Y_CH - 0.3), color=FC, width=7, tip=0.2, op=oe, z=9))
                g.add(mtxt("ATRITO DO CHÃO NAS PATAS", 16, color=FC, op=oe).move_to(P3(xh + 0.85, Y_CH - 0.62)))
                g.add(mtxt("ATRITO DO CHÃO NA PEDRA", 16, color=FC, op=oe).move_to(P3(xp_ - 0.75, Y_CH - 0.62)))
                if on > 0.01:
                    g.add(mtex(rf"{fc:,.0f}".replace(",", ".") + r"\ \mathrm{N}", FC, 28).set_opacity(on).move_to(P3(xh + 0.85, Y_CH - 0.95)))
                    g.add(mtex(r"2.352\ \mathrm{N}", FC, 28).set_opacity(on).move_to(P3(xp_ - 0.75, Y_CH - 0.95)))
            if ov > 0.01:
                for c in (p["cav"], p["ped"]):
                    g.add(arrow(c, c + P3(0, -0.55), color=FC, width=2.5, tip=0.11, op=0.55 * ov, z=9))
                    g.add(arrow(c, c + P3(0, 0.55), color=FC, width=2.5, tip=0.11, op=0.55 * ov, z=9))
            return g
        self.forcas = forcas

    def fronteira_tropa(self):
        fr = fronteira(6.65, 2.55, P3(-3.22, -0.2), rotulo="SISTEMA")
        fr.dx0 = 0.0

        def segue(m):
            d = self.tr.dx.get_value() - m.dx0
            if abs(d) > 1e-6:
                m.shift(P3(d, 0))
                m.dx0 = self.tr.dx.get_value()
        fr.add_updater(segue)
        return fr

    # ── T8-1 ────────────────────────────────────────────────────────────────────────────────────────────────
    def t8_1(self):
        self.an("T8-1")
        tr = self.tr
        self.ch = chao(-7.4, 7.4, Y_CH)
        self.g = tr.grupo()
        self.fg = always_redraw(self.forcas)
        self.play(FadeIn(self.ch), FadeIn(self.g), run_time=1.0)
        self.add(self.fg)
        self.ate(0.12)
        self.fr = self.fronteira_tropa()
        self.play(Create(self.fr[0]), FadeIn(self.fr[1]), run_time=1.2)
        self.ate(0.25)
        self.play(self.op_int.animate.set_value(1.0), run_time=1.0)
        self.ate(0.5)
        self.play(self.op_int.animate.set_value(0.45), self.op_ext.animate.set_value(1.0), run_time=1.2)
        le = txt("EXTERNAS NA HORIZONTAL", 20, color=FC).move_to(P3(XR, 1.6))
        li = txt("INTERNA: SOME DA CONTA", 20, color=INT).move_to(P3(XR, 1.1))
        self.play(FadeIn(le), FadeIn(li), run_time=0.6)
        self.ate(0.86)
        self.play(self.op_vert.animate.set_value(1.0), run_time=0.8)
        lv = txt("PESO E NORMAL SE CANCELAM", 20, color=DIM).move_to(P3(XR, 0.6))
        self.play(FadeIn(lv), run_time=0.5)
        self.ate(0.97)
        self.play(FadeOut(le), FadeOut(li), FadeOut(lv), self.op_vert.animate.set_value(0.0), run_time=0.5)

    # ── T8-2, T8-3, T8-4 ────────────────────────────────────────────────────────────────────────────────────
    def t8_2_3_4(self):
        self.an("T8-2")
        d1 = num(r"m_{\text{cavalo}}=600\ \mathrm{kg}", WHITE_, 38)
        d2 = num(r"m_{\text{pedra}}=800\ \mathrm{kg}", WHITE_, 38)
        dados = VGroup(d1, d2).arrange(RIGHT, buff=0.6).move_to(P3(XR, 1.85))
        r2 = txt("ATRITO CINÉTICO NA PEDRA", 20, color=DIM).move_to(P3(XR, 1.05))
        r3 = num(r"f_p=0{,}3\cdot 800\cdot 9{,}8=2.352\ \mathrm{N}", FC, 42).move_to(P3(XR, 0.5))
        r4 = txt("EMPURRÃO DO CHÃO NAS PATAS", 20, color=DIM).move_to(P3(XR, -0.35))
        r5 = num(r"f_c=2.800\ \mathrm{N}", FC, 42).move_to(P3(XR, -0.9))
        self.play(FadeIn(d1, shift=0.1 * UP), run_time=0.7)
        self.play(FadeIn(d2, shift=0.1 * UP), run_time=0.7)
        self.ate(0.3)
        self.play(FadeIn(r2), run_time=0.5)
        self.ate(0.42)
        self.play(FadeIn(r3, shift=0.1 * UP), run_time=0.9)
        self.ate(0.68)
        self.play(self.op_val.animate.set_value(1.0), run_time=0.6)
        self.ate(0.8)
        self.play(FadeIn(r4), FadeIn(r5, shift=0.1 * UP), run_time=0.9)
        self.ate(0.97)
        # T8-3 -----------------------------------------------------------------------------------------------
        self.an("T8-3")
        self.play(FadeOut(r2), FadeOut(r3), FadeOut(r4), FadeOut(r5), run_time=0.5)
        s0 = txt("SISTEMA", 24, bold=True).move_to(P3(XR, 1.1))
        s1 = num(r"(2.800-2.352)=(600+800)\,a", WHITE_, 42).move_to(P3(XR, 0.4))
        s2 = num(r"448=1.400\,a", WHITE_, 42).move_to(P3(XR, -0.45))
        s3 = num(r"a=0{,}32\ \mathrm{m/s^2}", WHITE_, 50).move_to(P3(XR, -1.4))
        nota = txt("A CORDA NEM APARECE", 20, color=INT).move_to(P3(XR, -2.3))
        self.play(FadeIn(s0), self.op_int.animate.set_value(0.2), run_time=0.6)
        self.play(FadeIn(s1, shift=0.1 * UP), run_time=0.9)
        self.ate(0.2)
        self.play(FadeIn(nota), run_time=0.5)
        self.ate(0.45)
        self.play(FadeIn(s2, shift=0.1 * UP), run_time=0.8)
        self.ate(0.75)
        self.play(FadeIn(s3, shift=0.1 * UP), run_time=0.8)
        cx = SurroundingRectangle(s3, buff=0.15, corner_radius=0.08).set_stroke(WHITE_, 2)
        self.play(Create(cx), run_time=0.5)
        self.ate(0.97)
        # T8-4 -----------------------------------------------------------------------------------------------
        self.an("T8-4")
        a_top = num(r"a=0{,}32\ \mathrm{m/s^2}", WHITE_, 38).move_to(P3(XR, 1.15))
        self.play(FadeOut(s0), FadeOut(s1), FadeOut(s2), FadeOut(nota), FadeOut(cx), FadeOut(dados), ReplacementTransform(s3, a_top),
                  run_time=0.8)
        pl = txt("PEDRA", 24, bold=True).move_to(P3(1.4, 0.35))
        p1 = num(r"T-2.352=800\cdot 0{,}32", WHITE_, 40).move_to(P3(4.6, 0.35))
        p2 = num(r"T=2.608\ \mathrm{N}", INT, 44).move_to(P3(4.6, -0.4))
        cl = txt("CAVALO", 24, bold=True).move_to(P3(1.4, -1.25))
        c1 = num(r"2.800-T=600\cdot 0{,}32", WHITE_, 40).move_to(P3(4.6, -1.25))
        c2 = Mc(r"2.800-2.608", "=", r"192\ \mathrm{N}", "=", r"600\cdot 0{,}32", size=40).move_to(P3(4.6, -2.0))
        self.play(self.op_int.animate.set_value(1.0), FadeIn(pl), FadeIn(p1, shift=0.1 * UP), run_time=0.9)
        self.ate(0.3)
        self.play(FadeIn(p2, shift=0.1 * UP), self.op_tval.animate.set_value(1.0), run_time=0.8)
        self.ate(0.45)
        self.play(FadeIn(cl), FadeIn(c1, shift=0.1 * UP), run_time=0.9)
        self.ate(0.62)
        self.play(FadeIn(c2, shift=0.1 * UP), run_time=0.9)
        for _ in range(2):
            self.play(c2[2].animate.set_color(MAG).scale(1.15), c2[4].animate.set_color(MAG), run_time=0.35)
            self.play(c2[2].animate.set_color(WHITE_).scale(1 / 1.15), c2[4].animate.set_color(WHITE_), run_time=0.35)
        mt = txt("MESMA TENSÃO NAS DUAS PONTAS", 20, color=INT).move_to(P3(XR, -2.85))
        self.ate(0.86)
        self.play(FadeIn(mt), run_time=0.6)
        self.ate(0.97)
        self.direita = VGroup(a_top, pl, p1, p2, cl, c1, c2, mt)

    # ── T8-5, T8-6 ──────────────────────────────────────────────────────────────────────────────────────────
    def t8_5_6(self):
        self.an("T8-5")
        tr = self.tr
        self.play(FadeOut(self.direita), self.op_ext.animate.set_value(0.0), self.op_int.animate.set_value(0.0),
                  self.op_tval.animate.set_value(0.0), run_time=0.7)
        # no cavalo: o chão (2.800, para a frente) × a corda (2.608, para trás), lado a lado
        p = tr.pts()
        xh, yb = p["cav"][0], p["cav"][1]
        ach = arrow(P3(xh - 0.2, Y_CH - 0.3), P3(xh - 0.2 + F_CHAO * S, Y_CH - 0.3), color=FC, width=8, tip=0.22, z=11)
        aco = arrow(P3(xh + 0.4, yb + 0.95), P3(xh + 0.4 - TENS * S, yb + 0.95), color=INT, width=8, tip=0.22, z=11)
        lch = num(r"2.800\ \mathrm{N}", FC, 32).next_to(ach, DOWN, buff=0.12)
        lco = num(r"2.608\ \mathrm{N}", INT, 32).next_to(aco, UP, buff=0.12)
        tch = txt("CHÃO", 18, color=FC).next_to(lch, RIGHT, buff=0.2)
        tco = txt("CORDA", 18, color=INT).next_to(lco, LEFT, buff=0.2)
        self.play(GrowArrow(ach), FadeIn(lch), FadeIn(tch), run_time=0.9)
        self.ate(0.18)
        self.play(GrowArrow(aco), FadeIn(lco), FadeIn(tco), run_time=0.9)
        self.ate(0.4)
        r1 = txt("O CAVALO ANDA PORQUE", 30, bold=True)
        r2 = txt("O CHÃO O EMPURRA;", 30, bold=True, color=FC)
        r3 = txt("A CORDA SÓ TRANSMITE", 30, bold=True, color=INT)
        res = VGroup(r1, r2, r3).arrange(DOWN, buff=0.22).move_to(P3(XR, 0.9))
        rn = linha("RESULTANTE NO CAVALO:", num(r"192\ \mathrm{N}", WHITE_, 34), size=20, buff=0.18).move_to(P3(XR, -0.7))
        self.play(FadeIn(r1, shift=0.1 * UP), run_time=0.6)
        self.play(FadeIn(r2, shift=0.1 * UP), run_time=0.6)
        self.play(FadeIn(r3, shift=0.1 * UP), run_time=0.6)
        self.ate(0.75)
        self.play(FadeIn(rn), run_time=0.6)
        self.ate(0.97)
        # T8-6 -----------------------------------------------------------------------------------------------
        self.an("T8-6")
        self.play(FadeOut(res), FadeOut(rn), FadeOut(ach), FadeOut(aco), FadeOut(lch), FadeOut(lco), FadeOut(tch), FadeOut(tco),
                  run_time=0.6)
        gl = gelo(-3.0, 1.2, Y_CH)
        lg = txt("GELO SOB AS PATAS", 18, color=mix(GELO, 0.3)).move_to(P3(-0.9, Y_CH - 1.35))
        self.play(FadeIn(gl), FadeIn(lg), self.op_ext.animate.set_value(1.0), self.op_val.animate.set_value(1.0), run_time=1.0)
        g1 = num(r"\mu_e\approx 0{,}1", WHITE_, 42).move_to(P3(XR, 1.5))
        g2 = num(r"f_{c,\,\max}=0{,}1\cdot 600\cdot 9{,}8=588\ \mathrm{N}", FC, 40).move_to(P3(XR, 0.7))
        g3 = num(r"588\ \mathrm{N}<2.352\ \mathrm{N}", WHITE_, 42).move_to(P3(XR, -0.15))
        self.ate(0.12)
        self.play(FadeIn(g1, shift=0.1 * UP), run_time=0.7)
        self.ate(0.22)
        self.play(FadeIn(g2, shift=0.1 * UP), self.fchao.animate.set_value(F_GELO), run_time=1.4)
        self.ate(0.45)
        self.play(FadeIn(g3, shift=0.1 * UP), run_time=0.8)
        # o conjunto desacelera (estava andando; agora as patas escorregam): a = (588 − 2.352)/1.400
        g4 = txt("O CONJUNTO DESACELERA", 26, bold=True).move_to(P3(XR, -1.0))
        a_ = num(r"a=\frac{588-2.352}{1.400}\approx -1{,}26\ \mathrm{m/s^2}", WHITE_, 36).move_to(P3(XR, -1.85))
        assert abs((F_GELO - F_PED) / (M_CAV + M_PED) + 1.26) < 0.001
        self.ate(0.55)
        t0, x0, f0 = self.clk.get_value(), tr.dx.get_value(), tr.fase.get_value()
        V0, TD = 0.36, 3.2

        def desliza(m):
            s = min(self.clk.get_value() - t0, TD)
            tr.dx.set_value(x0 + V0 * s - V0 * s * s / (2 * TD))
            tr.passo.set_value(0.35 * (1 - s / TD))
            tr.fase.set_value(f0 + 3.0 * s)
        motor = Mobject().add_updater(desliza)
        self.add(motor)
        self.play(FadeIn(g4, shift=0.1 * UP), run_time=0.7)
        self.play(FadeIn(a_), run_time=0.7)
        self.ate(0.85)
        mesmo = txt("O QUE MUDOU FOI A FORÇA EXTERNA", 20, color=FC).move_to(P3(XR, -2.7))
        self.play(FadeIn(mesmo), run_time=0.6)
        self.ate(0.97)
        motor.clear_updaters()
        self.remove(motor)

    # ── T8-7 ────────────────────────────────────────────────────────────────────────────────────────────────
    def t8_7(self):
        self.an("T8-7")
        self.fg.clear_updaters()
        self.g.clear_updaters()
        self.fr.clear_updaters()
        self.clear(rt=0.6)
        piso = chao(-7.2, 0.4, Y_CH)
        chapa = RoundedRectangle(corner_radius=0.04, width=2.7, height=0.2).set_stroke(mix(TERRA, 0.4), 2).set_fill(TERRA, 1) \
            .move_to(P3(-3.4, Y_CH + 0.1))
        lch = txt("PLACA DE FERRO", 16, color=DIM).next_to(chapa, DOWN, buff=0.12)
        pz = dict(cf=1.52, jf=1.62, ct=1.5, jt=1.6)
        pes = PessoaPerfil(-4.2, 0, 1.9, 1, "joga", quadril=Y_CH + 0.2 + 0.1, extra=pz)
        mao = pes.pts["mao_f"]
        yi = ValueTracker(0.0)
        im = always_redraw(lambda: ima().move_to(mao + P3(0.05, 0.25 + yi.get_value())))
        lua = VGroup(Circle(radius=0.3).set_stroke(width=0).set_fill(GEO, 0.85),
                     Circle(radius=0.27).set_stroke(width=0).set_fill(BACKGROUND_COLOR, 1).shift(P3(0.12, 0.06))).move_to(P3(-0.4, 1.85))
        self.play(FadeIn(piso), FadeIn(chapa), FadeIn(lch), FadeIn(pes), FadeIn(im), FadeIn(lua), run_time=1.0)
        self.ate(0.2)
        self.play(yi.animate.set_value(1.0), run_time=1.6, rate_func=lambda u: 1 - (1 - u) ** 2)
        ai = arrow(mao + P3(0.05, 1.05), mao + P3(0.05, 0.6), color=INT, width=5, tip=0.15, z=10)
        ap = arrow(chapa.get_top() + P3(0.9, 0.02), chapa.get_top() + P3(0.9, 0.48), color=INT, width=5, tip=0.15, z=10)
        la = txt("ATRAÇÃO", 16, color=INT).next_to(ai, RIGHT, buff=0.15)
        self.play(GrowArrow(ai), GrowArrow(ap), FadeIn(la), run_time=0.8)
        self.ate(0.45)
        fr = fronteira(4.3, 3.6, P3(-3.45, 0.15), rotulo=["PESSOA", mais(), "PLACA", mais(), "ÍMÃ"])
        self.play(Create(fr[0]), FadeIn(fr[1]), run_time=1.0)
        c1 = txt("CORDA E ÍMÃ:", 30, bold=True)
        c2 = txt("SÓ FORÇAS INTERNAS", 30, bold=True, color=INT)
        VGroup(c1, c2).arrange(DOWN, buff=0.22).move_to(P3(XR, 0.6))
        nf = txt("NÃO FUNCIONA", 22, color=DIM).move_to(P3(XR, -0.6))
        self.ate(0.62)
        self.play(FadeIn(c1, shift=0.1 * UP), FadeIn(c2, shift=0.1 * UP), run_time=0.8)
        self.ate(0.78)
        self.play(FadeIn(nf), run_time=0.5)
        self.ate(0.97)
        im.clear_updaters()

    # ── T8-8 ────────────────────────────────────────────────────────────────────────────────────────────────
    def t8_8(self):
        self.an("T8-8")
        self.clear(rt=0.6)
        piso = chao(-7.4, 7.4, Y_CH)
        t0 = self.clk.get_value()
        V, W = 0.35, 1.6

        def pessoa():
            s = self.clk.get_value() - t0
            fase = W * s
            pe = PessoaPerfil(-5.6 + V * s, Y_CH, 2.1, 1, andar(fase))
            planta = pe.pts["pe_f"] if math.cos(fase) < 0 else pe.pts["pe_t"]
            x = planta[0]
            g = VGroup(pe)
            g.add(arrow(P3(x - 0.1, Y_CH - 0.3), P3(x + 1.0, Y_CH - 0.3), color=FC, width=7, tip=0.2, z=10))
            g.add(arrow(P3(x + 0.1, Y_CH - 0.75), P3(x - 0.7, Y_CH - 0.75), color=INT, width=4, tip=0.14, z=10, op=0.8))
            g.add(mtxt("ATRITO DO CHÃO NO PÉ", 16, color=FC).move_to(P3(x + 0.5, Y_CH - 0.52)))
            g.add(mtxt("O PÉ EMPURRA O CHÃO", 16, color=INT).move_to(P3(x - 0.3, Y_CH - 1.0)))
            return g
        pg = always_redraw(pessoa)
        self.play(FadeIn(piso), FadeIn(pg), run_time=0.8)
        self.ate(0.6)
        d = dica("QUEM ACELERA O CONJUNTO É A FORÇA EXTERNA.", "A CORDA SÓ TRANSMITE")
        self.dica_entra(d)
        self.ate(0.97)
        pg.clear_updaters()
        self.dica_sai()
        self.clear(rt=0.5)
