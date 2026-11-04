"""Lote PT5: T5 — TRABALHO E POTÊNCIA NO GIRO.
T5-1: roda 2,5D de raio R girando por dθ sob força tangencial F_t; arco ds = R dθ → dW = F_t ds = F_t R dθ = τ dθ → W = ∫ τ dθ (caixa PANEL ciano)
e selo 'AGORA SIM: N·m · rad = J'.
T5-2: gráfico de τ(θ) com área preenchida em ciano + cadeia τ = I α = I dω/dt = I ω dω/dθ → W = ∫ τ dθ = ∫ I ω dω = ½ I ω_f² − ½ I ω_i² = ΔK_rot.
T5-3: P = dW/dt = τ dθ/dt = τ ω + motor 2,5D (100 N·m a 4000 RPM → ω ≈ 418,9 rad/s, P ≈ 41,9 kW ≈ 57 cv).
T5-4: duas engrenagens 2,5D em razão 3:1 (8 dentes e 24 dentes acopladas sem interpenetração): ω e τ na menor vs ω/3 e 3τ na maior, com barras
ciano iguais de potência P = τ ω."""
from pecas22 import *  # noqa: F401,F403


class LoteT5(Lote22):
    def corpo(self):
        self.secao("TRABALHO E POTÊNCIA NO GIRO")

        # ── T5-1: roda 2,5D de raio R, arco ds = R dθ, dW = τ dθ e W = ∫ τ dθ ──
        self.an("T5-1")
        C_R = P3(-3.8, -0.45)
        R_W = 1.95
        dth_val = 0.55

        rd = roda(C_R, R=R_W, ang=0.15, raios=6)
        p0 = C_R + R_W * np.array([math.cos(0.15), math.sin(0.15), 0.0])
        p1 = C_R + R_W * np.array([math.cos(0.15 + dth_val), math.sin(0.15 + dth_val), 0.0])
        tg1 = np.array([-math.sin(0.15 + dth_val), math.cos(0.15 + dth_val), 0.0])

        lin_r0 = DashedLine(C_R, p0, dash_length=0.08).set_stroke(GEO, 2.4)
        lin_r1 = Line(C_R, p1).set_stroke(GEO, 3.0)
        arco_ds = Arc(radius=R_W, start_angle=0.15, angle=dth_val, arc_center=C_R).set_stroke(KC, 6.0).set_z_index(12)
        arco_dth = Arc(radius=0.68, start_angle=0.15, angle=dth_val, arc_center=C_R).set_stroke(GEO, 2.8)
        l_R = T("R", 38, GEO).move_to((C_R + p1) / 2 + P3(-0.34, 0.28))
        l_dth = T(r"d\theta", 36, GEO).move_to(C_R + 1.05 * np.array([math.cos(0.42), math.sin(0.42), 0.0]))
        l_ds = T("ds", 38, KC).move_to(C_R + (R_W + 0.42) * np.array([math.cos(0.42), math.sin(0.42), 0.0]))
        s_ft = seta(p1, p1 + tg1 * 1.35, FC, 6, tip=0.20, z=14)
        l_ft = T("F_t", 40, FC).next_to(p1 + tg1 * 1.35, UL, buff=0.12)

        cab_t51 = txt("TRABALHO DE UM GIRO ELEMENTAR:", 26, bold=True, color=KC)
        self.pilha.poe(cab_t51)
        self.play(FadeIn(rd), Create(lin_r0), Create(lin_r1), FadeIn(l_R), FadeIn(s_ft), FadeIn(l_ft), FadeIn(cab_t51), run_time=0.8)
        self.gat("gira um ângulo pequenininho")
        self.play(Create(arco_dth), FadeIn(l_dth), Create(arco_ds), FadeIn(l_ds), run_time=0.8)

        A1, ia1 = M("ds", "=", "R", r"d\theta", size=50)
        self.pilha.poe(A1)
        self.gat("raio vezes esse ângulo")
        self.monta(A1, ia1, {0: l_ds, 2: l_R, 3: l_dth}, rt=0.9)

        A2, ia2 = M("dW", "=", "F_t", "ds", "=", "F_t", "R", r"d\theta", size=48)
        self.pilha.poe(A2)
        self.gat("força vezes deslocamento")
        self.monta(A2, ia2, {2: l_ft, 3: mp(A1, ia1, [0])}, rt=1.0)

        A3, ia3 = M("dW", "=", r"\tau", r"d\theta", size=52)
        self.pilha.poe(A3)
        self.gat("força tangencial vezes raio é o torque")
        self.passo(
            A2, A3,
            (J(ia2, 0), J(ia3, 0)),
            (J(ia2, 1), J(ia3, 1)),
            (J(ia2, 5, 6), J(ia3, 2)),
            (J(ia2, 7), J(ia3, 3)),
            rt=1.1,
            origem=True,
        )

        A4, ia4 = M("W", "=", r"\int_{\theta_i}^{\theta_f}", r"\tau\,d\theta", size=54)
        A4b = caixa_l(A4, KC)
        self.pilha.so(A3, anims=[FadeOut(cab_t51), FadeOut(A1), FadeOut(A2)])
        self.pilha.poe(A4b)
        self.gat("integral do torque")
        self.cx(A4b[0])
        self.passo(A3, A4, (J(ia3, 0), J(ia4, 0)), (J(ia3, 1), J(ia4, 1)), (J(ia3, 2, 3), J(ia4, 3)), rt=1.1, origem=False)
        self.pilha.so(A4b)

        self.selo("UNIDADE DE ENERGIA", "AGORA SIM:  N·m · rad = J  (TORQUE × ÂNGULO = TRABALHO)")
        self.foco = A4b
        self.ate(0.99)

        # ── T5-2: gráfico de τ(θ) preenchido em ciano + teorema trabalho-energia na rotação ──
        self.an("T5-2")
        self.sem_selo()
        self.pilha.limpa()
        self.play(
            FadeOut(VGroup(rd, lin_r0, lin_r1, arco_ds, arco_dth, l_R, l_dth, l_ds, s_ft, l_ft, A4b)),
            run_time=0.45,
        )

        # Gráfico τ(θ) na metade esquerda com área preenchida em ciano (#22D3EE)
        O_g = P3(-6.1, -2.25)
        W_G, H_G = 4.6, 3.2
        ex_g = Arrow(O_g, O_g + RIGHT * (W_G + 0.35), buff=0, stroke_width=2.6, tip_length=0.18).set_color(GEO)
        ey_g = Arrow(O_g, O_g + UP * (H_G + 0.35), buff=0, stroke_width=2.6, tip_length=0.18).set_color(GEO)
        l_ex = T(r"\theta", 36, GEO).next_to(ex_g.get_end(), DOWN, buff=0.12)
        l_ey = T(r"\tau(\theta)", 36, TQ).next_to(ey_g.get_end(), LEFT, buff=0.12)

        def _f_tau(u):
            return 1.35 + 0.85 * math.sin(math.pi * u) + 0.25 * math.cos(2 * math.pi * u)

        xs_u = np.linspace(0.12, 0.88, 50)
        pts_curva = [O_g + P3(u * W_G, _f_tau(u)) for u in xs_u]
        curva = VMobject().set_points_smoothly(pts_curva).set_stroke(TQ, 4.0).set_z_index(10)
        area_w = Polygon(O_g + P3(xs_u[0] * W_G, 0.0), *pts_curva, O_g + P3(xs_u[-1] * W_G, 0.0)).set_fill(KC, 0.32).set_stroke(KC, 1.8).set_z_index(8)
        lbl_w = T(r"W = \int \tau\,d\theta", 36, KC).move_to(O_g + P3(0.50 * W_G, 0.85))
        l_thi = T(r"\theta_i", 32, GEO).move_to(O_g + P3(xs_u[0] * W_G, -0.35))
        l_thf = T(r"\theta_f", 32, GEO).move_to(O_g + P3(xs_u[-1] * W_G, -0.35))

        self.play(FadeIn(ex_g), FadeIn(ey_g), FadeIn(l_ex), FadeIn(l_ey), Create(curva), FadeIn(area_w), FadeIn(lbl_w), FadeIn(l_thi), FadeIn(l_thf), run_time=0.9)

        # Cadeia da regra da cadeia: τ = I α = I dω/dt = I (dω/dθ)(dθ/dt) = I ω dω/dθ
        B1, ib1 = M(r"\tau", "=", "I", r"\alpha", "=", "I", r"\frac{d\omega}{dt}", "=", "I", r"\omega", r"\frac{d\omega}{d\theta}", size=46)
        self.pilha.poe(B1)
        self.gat("troca o torque por momento de inércia")
        self.monta(B1, ib1, {}, rt=1.1)

        B2, ib2 = M("W", "=", r"\int_{\theta_i}^{\theta_f}", r"\tau\,d\theta", "=", r"\int_{\omega_i}^{\omega_f}", "I", r"\omega\,d\omega", size=46)
        self.pilha.poe(B2)
        self.gat("variação dela por ângulo")
        self.monta(B2, ib2, {}, rt=1.1)

        B3, ib3 = M("W", "=", r"\frac{1}{2}", "I", r"\omega_f^2", "-", r"\frac{1}{2}", "I", r"\omega_i^2", "=", r"\Delta K_{\mathrm{rot}}", size=48)
        B3b = caixa_l(B3, KC)
        self.pilha.so(B1, B2)
        self.pilha.poe(B3b)
        self.gat("energia cinética de rotação")
        self.cx(B3b[0])
        self.passo(B2, B3, (J(ib2, 0), J(ib3, 0)), (J(ib2, 1), J(ib3, 1)), rt=1.1, origem=False)
        self.pilha.so(B3b)
        self.foco = B3b
        self.ate(0.99)

        # ── T5-3: P = dW/dt = τ ω + exemplo do motor 2,5D (100 N·m a 4000 RPM → 41,9 kW ≈ 57 cv) ──
        self.an("T5-3")
        self.pilha.limpa()
        self.play(
            FadeOut(VGroup(ex_g, ey_g, l_ex, l_ey, curva, area_w, lbl_w, l_thi, l_thf, B3b)),
            run_time=0.45,
        )

        C_MOT = P3(-3.8, -0.45)
        ang_m = ValueTracker(0.0)
        ang_m.add_updater(lambda m, dt: m.increment_value(4.5 * dt))
        self.add(ang_m)

        mv = vivo(lambda: VGroup(
            motor(C_MOT, escala=1.25, ang=ang_m.get_value()),
            arco_torque(C_MOT, r=0.98, sentido=1, a0=0.3, amp=1.8, cor=TQ, w=5),
        ))
        lbl_mot = VGroup(
            VGroup(T(r"\tau =", 36, TQ), nm(r"100\ \mathrm{N\cdot m}", TQ, 36)).arrange(RIGHT, buff=0.10),
            nm(r"4000\ \mathrm{RPM}", VEL, 36),
        ).arrange(DOWN, buff=0.12).move_to(C_MOT + P3(0.0, 1.85))
        self.play(FadeIn(mv), FadeIn(lbl_mot), run_time=0.7)

        C1, ic1 = M("P", "=", r"\frac{dW}{dt}", "=", r"\tau", r"\frac{d\theta}{dt}", "=", r"\tau", r"\omega", size=50)
        C1b = caixa_l(C1, KC)
        self.pilha.poe(C1b)
        self.gat("potência é torque vezes velocidade angular")
        self.cx(C1b[0])
        self.monta(C1, ic1, {}, rt=1.1)

        self.gat("quatro mil rotações por minuto")
        C2, ic2 = M(r"\omega", "=", r"4000\cdot\frac{2\pi}{60}", r"\approx", "418{,}9", r"\,\mathrm{rad/s}", size=44)
        self.pilha.poe(C2)
        self.monta(C2, ic2, {}, rt=1.0)

        self.gat("quarenta e dois quilowatts")
        C3, ic3 = M("P", "=", "100", r"\cdot", "418{,}9", r"\approx", "41{,}9", r"\,\mathrm{kW}", r"\approx", "57", r"\,\mathrm{cv}", size=44)
        self.pilha.poe(C3)
        self.monta(C3, ic3, {2: lbl_mot[0][1], 4: mp(C2, ic2, [4])}, rt=1.1)
        self.foco = C3
        self.ate(0.99)

        # ── T5-4: duas engrenagens 2,5D acopladas em razão 3:1 (8 dentes e 24 dentes) + barras de potência iguais ──
        self.an("T5-4")
        mv.clear_updaters()
        ang_m.clear_updaters()
        self.pilha.limpa()
        self.play(FadeOut(VGroup(mv, lbl_mot, C1b, C2, C3)), run_time=0.45)

        C_ENG = P3(-3.8, -0.35)
        ang_e = ValueTracker(0.0)
        ang_e.add_updater(lambda m, dt: m.increment_value(1.8 * dt))
        self.add(ang_e)

        ev = vivo(lambda: engrenagens(C_ENG, ang1=ang_e.get_value(), r1=0.58, razao=3, n1=8))
        ref_e = engrenagens(C_ENG, ang1=0.0, r1=0.58, razao=3, n1=8)
        lbl_e1 = VGroup(T("R_1", 36, GEO), T(r"\omega,\ \tau", 36)).arrange(DOWN, buff=0.08).move_to(ref_e.c1 + P3(0.0, -1.25))
        lbl_e2 = VGroup(T("R_2 = 3R_1", 36, GEO), T(r"\tfrac{\omega}{3},\ 3\tau", 36)).arrange(DOWN, buff=0.08).move_to(ref_e.c2 + P3(0.0, -2.35))

        D1, id1 = M("P", "=", r"\tau", r"\omega", "=", r"(3\tau)", r"\Big(\frac{\omega}{3}\Big)", size=50)
        D1b = caixa_l(D1, KC)
        self.pilha.poe(D1b)
        self.play(FadeIn(ev), FadeIn(lbl_e1), FadeIn(lbl_e2), run_time=0.8)
        self.cx(D1b[0])
        self.monta(D1, id1, {}, rt=1.1)
        self.gat("multiplica o torque três vezes")

        # Duas barras de potência iguais em ciano (#22D3EE)
        b_p1 = VGroup(barra_E(1.5, -2.6, 2.2, larg=0.44, cor=KC, hmax=2.4), T("P_1", 36, KC).move_to(P3(1.5, -2.95)))
        b_p2 = VGroup(barra_E(2.6, -2.6, 2.2, larg=0.44, cor=KC, hmax=2.4), T("P_2", 36, KC).move_to(P3(2.6, -2.95)))
        ig_p = txt("IGUAIS", 24, bold=True, color=KC).move_to(P3(2.05, -0.15))

        self.play(FadeIn(b_p1), FadeIn(ig_p), FadeIn(b_p2), run_time=0.8)
        self.selo("CAIXA DE MARCHAS", "TROCA VELOCIDADE ANGULAR POR TORQUE COM A MESMA POTÊNCIA")
        self.foco = D1b
        self.ate(0.99)
