"""Hook (H1–H3) + abertura (A1–A3)."""
from kit import *  # noqa: F401,F403

PISO = -3.2
MURO_X0, MURO_X1, MURO_H = -5.0, -3.8, 2.5 * ESC_M
BORDA = MURO_X1 - 0.12
T_ANDA, T_QUEDA = 0.6, 1.7
G_TELA = MURO_H / T_QUEDA ** 2


def estado_queda(tau, joelhos):
    """Pés (x, y) e altura do quadril no instante tau do salto (andar até a borda → queda → aterrissagem)."""
    x0, x_pouso = -4.45, -2.2
    if tau <= T_ANDA:
        return x0 + (BORDA - x0) * suave(tau / T_ANDA), PISO + MURO_H, None
    s = min(tau - T_ANDA, T_QUEDA)
    x = BORDA + (x_pouso - BORDA) * (s / T_QUEDA)
    y = PISO + MURO_H - G_TELA * s * s
    if tau <= T_ANDA + T_QUEDA:
        return x, y, None
    u = min((tau - T_ANDA - T_QUEDA) / 0.9, 1.0)
    hip = None if not joelhos else 2 * Pessoa.COXA - (2 * Pessoa.COXA - 0.55) * suave(u)
    return x_pouso, PISO, hip


class P1Hook(Base):
    def construct(self):
        self.setup_base()
        self.hook()
        self.abertura()
        self.fim()
        self.relatorio()

    def cenario(self):
        piso = Line(P3(-7.6, PISO), P3(7.6, PISO)).set_stroke(GEO, 2.5, opacity=0.55)
        muro = Rectangle(width=MURO_X1 - MURO_X0, height=MURO_H).set_stroke(GEO, 2).set_fill(STEEL, 0.35) \
            .move_to(P3((MURO_X0 + MURO_X1) / 2, PISO + MURO_H / 2))
        cota = VGroup(DoubleArrow(P3(-5.55, PISO + 0.02), P3(-5.55, PISO + MURO_H - 0.02), buff=0, color=GEO,
                                  stroke_width=3, tip_length=0.15),
                      MathTex(r"2{,}5\ \mathrm{m}", font_size=34, color=GEO).move_to(P3(-6.45, PISO + MURO_H / 2)))
        return VGroup(piso, muro, cota)

    def pessoa_queda(self, joelhos):
        p = Pessoa(GEO)
        tau = ValueTracker(0.0)
        p.add_updater(lambda m: m.pose(*estado_queda(tau.get_value(), joelhos)))
        p.pose(*estado_queda(0.0, joelhos))
        return p, tau

    def hook(self):
        cen = self.cenario()
        # H1 — pernas duras ---------------------------------------------------------------------------------
        self.an("H1")
        p, tau = self.pessoa_queda(False)
        self.play(FadeIn(cen), FadeIn(p), run_time=0.8)
        self.ate(0.18)
        self.play(tau.animate.set_value(T_ANDA + T_QUEDA), run_time=T_ANDA + T_QUEDA, rate_func=linear)
        fl = flash(P3(-2.2, PISO + 0.05)).set_z_index(20)
        self.play(FadeIn(fl, scale=0.6), tau.animate.set_value(T_ANDA + T_QUEDA + 0.9), run_time=0.35, rate_func=linear)
        self.play(FadeOut(fl), run_time=0.3)
        self.ate(0.9)
        p.clear_updaters()
        self.play(FadeOut(p), run_time=0.4)
        # H2 — joelhos dobrados -----------------------------------------------------------------------------
        self.an("H2")
        p, tau = self.pessoa_queda(True)
        self.play(FadeIn(p), run_time=0.5)
        self.play(tau.animate.set_value(T_ANDA + T_QUEDA), run_time=T_ANDA + T_QUEDA, rate_func=linear)
        self.play(tau.animate.set_value(T_ANDA + T_QUEDA + 0.9), run_time=0.9, rate_func=linear)
        self.ate(0.9)
        p.clear_updaters()
        self.play(FadeOut(p), FadeOut(cen), run_time=0.5)
        # H3 — lado a lado ----------------------------------------------------------------------------------
        self.an("H3")
        piso = Line(P3(-7.6, -2.3), P3(7.6, -2.3)).set_stroke(GEO, 2.5, opacity=0.55)
        pa = Pessoa(GEO).pose(-5.3, -2.3, None)
        pb = Pessoa(GEO).pose(5.0, -2.3, 2 * Pessoa.COXA - (2 * Pessoa.COXA - 0.55))
        la = txt("PERNAS DURAS", T_SMALL, color=DIM).move_to(P3(-5.3, -2.85))
        lb = txt("JOELHOS DOBRADOS", T_SMALL, color=DIM).move_to(P3(5.0, -2.85))
        va = arrow(P3(-6.6, 2.0), P3(-6.6, 0.5), color=VEL, width=6)
        vb = arrow(P3(6.3, 2.0), P3(6.3, 0.5), color=VEL, width=6)
        vl = MathTex(r"\vec v", font_size=40, color=VEL)
        vl_a, vl_b = vl.copy().next_to(va, RIGHT, buff=0.12), vl.copy().next_to(vb, LEFT, buff=0.12)
        self.play(FadeIn(piso), FadeIn(pa), FadeIn(pb), FadeIn(la), FadeIn(lb), run_time=0.8)
        self.play(FadeIn(va), FadeIn(vb), FadeIn(vl_a), FadeIn(vl_b), run_time=0.6)
        t1 = txt("MESMA QUEDA. MESMA VELOCIDADE.", 36, bold=True).move_to(P3(0, 1.5))
        self.ate(0.18)
        self.play(FadeIn(t1, shift=0.1 * UP), run_time=0.7)
        self.ate(0.55)
        self.play(FadeOut(t1), run_time=0.4)
        t2 = txt("POR QUE DOBRAR OS JOELHOS", 40, bold=True).move_to(P3(0, 1.45))
        t3 = txt("SALVA SUAS PERNAS?", 40, color=CYAN, bold=True).move_to(P3(0, 0.6))
        self.play(FadeIn(t2, shift=0.1 * UP), run_time=0.7)
        self.play(FadeIn(t3, shift=0.1 * UP), run_time=0.7)
        self.ate(0.97)
        self.clear(rt=0.5)

    def abertura(self):
        # A1 -------------------------------------------------------------------------------------------------
        self.an("A1")
        logo = self.logo(4.6).move_to(P3(0, 0.6))
        wel = txt("BEM-VINDOS AO PARALLAX LAB", 34).move_to(P3(0, -1.3))
        self.play(FadeIn(logo, scale=0.94), FadeIn(wel, shift=0.1 * UP), run_time=1.0)
        self.ate(0.92)
        self.play(FadeOut(logo), FadeOut(wel), run_time=0.5)
        # A2 -------------------------------------------------------------------------------------------------
        self.an("A2")
        tit = txt("MOMENTO LINEAR E IMPULSO", 52, color=CYAN, bold=True).move_to(P3(0, 0.45))
        sub = txt("NESTE VÍDEO: O QUE UMA FORÇA FAZ AO LONGO DO TEMPO", 28, op=0.85).move_to(P3(0, -0.5))
        self.play(FadeIn(tit, shift=0.1 * UP), run_time=1.0)
        self.ate(0.4)
        self.play(FadeIn(sub, shift=0.1 * UP), run_time=0.8)
        self.ate(0.92)
        self.play(FadeOut(tit), FadeOut(sub), run_time=0.5)
        # A3 — miniaturas dos vídeos de colisões -------------------------------------------------------------
        self.an("A3")
        p1 = placa(6.2, 3.3, P3(-3.7, 0.9))
        p2 = placa(6.2, 3.3, P3(3.7, 0.9))
        l1 = txt("COLISÕES EM 1D", T_LAB, color=DIM).move_to(P3(-3.7, 2.2))
        l2 = txt("COLISÕES EM 2D", T_LAB, color=DIM).move_to(P3(3.7, 2.2))
        # 1D: dois corpos de aço indo um ao encontro do outro; depois seguem separados
        c1 = Corpo("", GEO, 0.7).at(-4.6, 0.0)
        c2 = Corpo("", STEEL, 0.55).at(-2.9, 0.0)
        a1 = arrow(P3(-4.6, 1.2), P3(-3.9, 1.2), color=VEL, width=5)
        a2 = arrow(P3(-2.85, 1.2), P3(-3.5, 1.2), color=VEL, width=5)
        pista = Line(P3(-6.4, 0.0), P3(-1.0, 0.0)).set_stroke(GEO, 2, opacity=0.5)
        # 2D: duas bolas, vetores após o contato
        d1, d2 = bola(0.3, GEO).move_to(P3(2.6, 0.5)), bola(0.3, STEEL).move_to(P3(4.5, 0.9))
        b1 = arrow(P3(2.6, 0.5), P3(3.6, -0.4), color=VEL, width=5)
        b2 = arrow(P3(4.5, 0.9), P3(5.4, 1.6), color=VEL, width=5)
        eq = Mc((r"\vec P_i", MAG), "=", (r"\vec P_f", MAG), size=M_MAIN).move_to(P3(0, -1.6))
        self.play(FadeIn(p1), FadeIn(p2), FadeIn(l1), FadeIn(l2), run_time=0.8)
        self.play(FadeIn(pista), FadeIn(c1), FadeIn(c2), FadeIn(a1), FadeIn(a2),
                  FadeIn(d1), FadeIn(d2), FadeIn(b1), FadeIn(b2), run_time=0.9)
        self.ate(0.4)
        self.play(FadeIn(eq, shift=0.1 * UP), run_time=0.8)
        self.ate(0.97)
        self.clear(rt=0.5)
