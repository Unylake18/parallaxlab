"""Lote PB3: B3 — O QUE MUDA L (Manim 2.5D, sem a mesa). Derivada de L⃗ = r⃗ × p⃗ (regra do produto, parcela paralela some) → τ⃗ = dL⃗/dt.
Conferência: pedra de 0,50 kg solta do repouso a d = 0,40 m à direita de O; queda até 0,60 s (1,76 m) em escala (2,4 u/m); r⃗ acompanha;
peso m g azul; gráfico L_z × t (reta de 0 a −1,18 kg·m²/s em 0,60 s, inclinação −1,96 N·m). A queda anda em câmera lenta ×0,25."""
from pecas24 import *  # noqa: F401,F403

ESC = 2.4                     # u por metro no desenho (queda de 1,76 m = 4,2 u)
PO = P3(-6.3, 1.9)            # ponto O
GX0, GY0 = -3.45, 1.15        # origem do gráfico (t para a direita, L_z para baixo)
SX, SY = 4.2, 3.4 / 1.20      # u por s, u por (kg m²/s)


class LoteB3(Lote24):
    def corpo(self):
        self.canto(txt("O QUE MUDA", 30), T("L", 40, LMAG))
        tq = ValueTracker(0.0)          # tempo físico da queda
        self.add(tq)
        d = F.D_PEDRA

        def pos_pedra():
            t = tq.get_value()
            return PO + P3(d * ESC, -0.5 * F.G * t * t * ESC)

        # ── B3-1: derivada de L⃗ = r⃗ × p⃗ (desenho genérico: O e a pedra) ──
        self.an("B3-1")
        pino = pino2d(PO)
        lO = T("O", 40, WHITE_).next_to(pino, LEFT, buff=0.2)
        pedra = pedra2d(pos_pedra())
        pedra.add_updater(lambda m: m.move_to(pos_pedra()))
        rv = vivo(lambda: VGroup(seta(PO, pos_pedra() + 0.3 * (PO - pos_pedra()) / max(np.linalg.norm(PO - pos_pedra()), 1e-6), VETC, 5, tip=0.18),
                                 T(r"\vec r", 40, VETC).move_to((PO + pos_pedra()) / 2 + P3(0, 0.38))))
        self.play(FadeIn(pino), FadeIn(lO), FadeIn(pedra), OpVivo(rv), run_time=0.6)
        A, ia = Mx(r"\vec L", "=", r"\vec r", r"\times", r"\vec p")
        self.pilha.poe(A)
        self.gat("derivar a definição no tempo")
        self.lei(A, ia, rt=0.9, metodo="lei")
        B, ib = Mx(r"\frac{d\vec L}{dt}", "=", r"\frac{d\vec r}{dt}", r"\times", r"\vec p", "+", r"\vec r", r"\times", r"\frac{d\vec p}{dt}", size=44)
        self.pilha.poe(B)
        self.gat("são duas parcelas")
        self.gm(A, B, (J(ia, 0), J(ib, 0)[1:3]), (J(ia, 1), J(ib, 1)), (J(ia, 2), J(ib, 2)[1:3]), (J(ia, 3), J(ib, 3)), (J(ia, 4), J(ib, 4)), rt=2.0)
        self.ate(0.99)

        # ── B3-2: dr⃗/dt → v⃗, dp⃗/dt → F⃗ (cartão F⃗ = dp⃗/dt acende); v⃗ × m v⃗ = 0 (PARALELOS) ──
        self.an("B3-2")
        cart, ic_ = Mx(r"\vec F", "=", r"\frac{d\vec p}{dt}", size=40)
        cart.move_to(P3(-1.7, -3.2))
        self.gat("a derivada da posição é a velocidade")
        self.play(FadeIn(cart), run_time=0.4)
        C, ic = Mx("=", r"\vec v", r"\times", "m", r"\vec v", "+", r"\vec r", r"\times", r"\vec F", size=46)
        self.pilha.poe(C)
        nb = len(ib[2])
        self.gm(B, C, (J(ib, 2), J(ic, 1)), (J(ib, 3), J(ic, 2)), (J(ib, 4), J(ic, 3, 4)), (J(ib, 5), J(ic, 5)), (J(ib, 6), J(ic, 6)), (J(ib, 7), J(ic, 7)),
                (J(ib, 8), J(ic, 8)), ([], J(ic, 0)), rt=1.8, extra=(Indicate(cart, color=FC),))
        self.gat("na mesma direção")
        par = VGroup(seta(P3(-2.6, 0.2), P3(-1.2, 0.2), VEL, 6), seta(P3(-2.6, -0.3), P3(-0.9, -0.3), MAG, 6))
        lpar = txt("PARALELOS", 26, bold=True, color=GEO).next_to(par, DOWN, buff=0.2)
        self.play(FadeIn(par), FadeIn(lpar), run_time=0.5)
        risco_ = Line(gl(C, J(ic, 1))[0].get_left() + P3(-0.05, -0.1), gl(C, J(ic, 4)).get_right() + P3(0.05, 0.12)).set_stroke(APAGADO, 4)
        self.gat("ela some")
        self.play(Create(risco_), run_time=0.5)
        D, id_ = Mx("=", "0", "+", r"\vec r", r"\times", r"\vec F", size=46)
        self.pilha.poe(D)
        self.gm(C, D, (J(ic, 0), J(id_, 0)), (J(ic, 1, 2, 3, 4), J(id_, 1)), (J(ic, 5), J(id_, 2)), (J(ic, 6), J(id_, 3)), (J(ic, 7), J(id_, 4)),
                (J(ic, 8), J(id_, 5)), rt=1.3, extra=(FadeOut(risco_),))
        self.ate(0.99)

        # ── B3-3: r⃗ × F⃗ vira τ⃗: τ⃗ = dL⃗/dt; F⃗ = dp⃗/dt ao lado; hipóteses ──
        self.an("B3-3")
        self.play(FadeOut(VGroup(par, lpar)), run_time=0.3)
        Ef, ie = Mx(r"\frac{d\vec L}{dt}", "=", r"\vec r", r"\times", r"\vec F")
        self.pilha.so(B, D)
        self.pilha.poe(Ef)
        self.gat("que é o torque")
        self.gm(D, Ef, (J(id_, 0), J(ie, 1)), (J(id_, 3), J(ie, 2)), (J(id_, 4), J(ie, 3)), (J(id_, 5), J(ie, 4)), (J(id_, 1, 2), []), ([], J(ie, 0)), rt=1.3)
        G_, ig = Mx(r"\vec\tau", "=", r"\frac{d\vec L}{dt}", size=58)
        self.pilha.so(Ef)
        self.pilha.poe(G_)
        self.gat("a taxa de variação do momento angular")
        self.gm(Ef, G_, (J(ie, 2, 3, 4), J(ig, 0)), (J(ie, 1), J(ig, 1)), (J(ie, 0), J(ig, 2)), rt=1.4)
        sub_ = self.resultado(G_, FC)
        self.gat("olha como fica parecido")
        H_, ih = Mx(r"\vec F", "=", r"\frac{d\vec p}{dt}", size=58)
        self.pilha.poe(H_)
        self.play(cart.animate.move_to(H_.get_center()).scale(58 / 40), run_time=0.8)
        self.remove(cart)
        self.add(H_)
        self.alg("voo", H_, 1)
        self.gat("só com um cuidado")
        self.hip("PONTO FIXO · REFERENCIAL INERCIAL · TORQUE E MOMENTO ANGULAR NO MESMO PONTO")
        self.ate(0.99)

        # ── B3-4: CONFERE: pedra de 0,50 kg a d = 0,40 m; cota d; peso; r⃗ acompanha ──
        self.an("B3-4")
        self.pilha.so(G_)
        self.play(FadeOut(sub_), run_time=0.2)
        self.selo("CONFERE", "UMA PEDRA CAINDO RETO")
        cota = DoubleArrow(PO + P3(0, 0.45), PO + P3(d * ESC, 0.45), buff=0, stroke_width=4, tip_length=0.16).set_color(VETC)
        l_d = VGroup(T("d", 40, VETC), T(r"=\,", 40, WHITE_), T(r"0{,}40", 40, VETC), T(r"\mathrm{m}", 34, WHITE_)).arrange(RIGHT, buff=0.08).next_to(cota, UP, buff=0.12)
        l_m = VGroup(T("m", 40, MAS), T(r"=\,", 40, WHITE_), T(r"0{,}50", 40, MAS), T(r"\mathrm{kg}", 34, WHITE_)).arrange(RIGHT, buff=0.08)
        l_m.add_updater(lambda m: m.next_to(pedra, RIGHT, buff=0.3))
        trilho = DashedLine(PO + P3(d * ESC, -0.3), PO + P3(d * ESC, -1.764 * ESC), dash_length=0.1).set_stroke(GEO, 2, opacity=0.6)
        self.gat("uma pedra de meio quilo")
        self.play(FadeIn(cota), FadeIn(l_d), FadeIn(l_m), FadeIn(trilho), run_time=0.6)
        peso = vivo(lambda: VGroup(seta(pos_pedra() + P3(0, -0.35), pos_pedra() + P3(0, -1.25), FC, 6, tip=0.2),
                                   T("mg", 40, FC).move_to(pos_pedra() + P3(-0.55, -0.85))))
        self.gat("ela cai reto")
        self.play(OpVivo(peso), run_time=0.5)
        self.ate(0.99)

        # ── B3-5: queda (×0,25) com o gráfico; L_z = x p_y − y p_x → −m g d t; τ_z = −m g d = −1,96 N·m; hold ──
        self.an("B3-5")
        self.sem_selo()
        self.pilha.limpa()
        eixo_t = Arrow(P3(GX0 - 0.1, GY0), P3(GX0 + 2.95, GY0), buff=0, stroke_width=3, tip_length=0.16).set_color(GEO)
        eixo_L = Arrow(P3(GX0, GY0 + 0.3), P3(GX0, GY0 - 3.7), buff=0, stroke_width=3, tip_length=0.16).set_color(GEO)
        lt = T("t", 36, WHITE_).next_to(eixo_t, RIGHT, buff=0.12)
        lL = T("L_z", 36, LMAG).next_to(eixo_L.get_end(), RIGHT, buff=0.15)
        marca = VGroup(Line(P3(GX0 + 0.6 * SX, GY0 - 0.08), P3(GX0 + 0.6 * SX, GY0 + 0.08)).set_stroke(GEO, 2),
                       T(r"0{,}60\,\mathrm{s}", 28, WHITE_).move_to(P3(GX0 + 0.6 * SX, GY0 + 0.32)))
        self.play(FadeIn(VGroup(eixo_t, eixo_L, lt, lL, marca)), run_time=0.5)
        curva = vivo(lambda: VGroup(Line(P3(GX0, GY0), P3(GX0 + tq.get_value() * SX + 1e-4, GY0 - 1.96 * tq.get_value() * SY)).set_stroke(LMAG, 5),
                                    Dot(P3(GX0 + tq.get_value() * SX, GY0 - 1.96 * tq.get_value() * SY), radius=0.08, color=LMAG)))
        self.add(curva)
        self.gat("ganha")
        self.play(tq.animate.set_value(F.T_QUEDA), run_time=2.4, rate_func=linear)
        A5, a5 = Mx("L_z", "=", "x", "p_y", "-", "y", "p_x")
        self.pilha.poe(A5)
        self.lei(A5, a5, rt=1.2, metodo="lei")
        B5, b5 = Mx("=", "d", r"(-m g t)", "-", "y", r"\cdot", "0", cores={1: VETC})
        self.pilha.poe(B5)
        self.gat("o momento para baixo cresce")
        self.gm(A5, B5, (J(a5, 1), J(b5, 0)), (J(a5, 2), J(b5, 1)), (J(a5, 3), J(b5, 2)), (J(a5, 4), J(b5, 3)), (J(a5, 5), J(b5, 4)), (J(a5, 6), J(b5, 6)),
                ([], J(b5, 5)), (J(a5, 0), []), rt=1.5)
        risco2 = Line(gl(B5, J(b5, 3))[0].get_left() + P3(-0.05, -0.1), gl(B5, J(b5, 6)).get_right() + P3(0.05, 0.1)).set_stroke(APAGADO, 4)
        self.play(Create(risco2), run_time=0.4)
        C5, c5 = Mx("L_z", "=", "-", "m", "g", "d", "t", size=56, cores={5: VETC})
        self.pilha.poe(C5)
        self.gat("cresce em linha reta")
        self.gm(B5, C5, (J(b5, 0), J(c5, 1)), (J(b5, 2)[1:2], J(c5, 2)), (J(b5, 2)[2:3], J(c5, 3)), (J(b5, 2)[3:4], J(c5, 4)), (J(b5, 1), J(c5, 5)),
                (J(b5, 2)[4:5], J(c5, 6)), (J(b5, 2)[0:1] + J(b5, 2)[5:6] + J(b5, 3, 4, 5, 6), []), ([], J(c5, 0)), rt=1.5, extra=(FadeOut(risco2),))
        self.resultado(C5, LMAG)
        self.gat("e o torque do peso")
        D5, d5 = Mx(r"\tau_z", "=", "-", "m", "g", "d", cores={5: VETC})
        self.pilha.so(C5)
        self.pilha.poe(D5)
        self.lei(D5, d5, {3: l_m[0], 5: l_d[0]}, rt=1.2)
        l_g = VGroup(T("g", 36, ACC), T(r"=\,9{,}8\,\mathrm{m/s^2}", 34, WHITE_)).arrange(RIGHT, buff=0.06).move_to(P3(-6.0, -3.55))
        self.play(FadeIn(l_g), run_time=0.3)
        E5, e5 = Mx("=", "-", r"0{,}50", r"\cdot", r"9{,}8", r"\cdot", r"0{,}40", cores={2: MAS, 4: ACC, 6: VETC})
        self.pilha.poe(E5)
        self.gat("menos um vírgula noventa e seis")
        self.lei(E5, e5, {2: l_m[2], 4: l_g[1], 6: l_d[2]}, rt=1.4, numero=True)
        F5, f5 = Mx("=", "-", r"1{,}96", r"\,\mathrm{N\,m}", size=56, cores={2: FC})
        self.pilha.poe(F5)
        self.lei(F5, f5, rt=0.8, numero=True)
        self.resultado(F5, FC)
        # triângulo de inclinação no gráfico
        a_, b_ = P3(GX0 + 0.2 * SX, GY0 - 1.96 * 0.2 * SY), P3(GX0 + 0.5 * SX, GY0 - 1.96 * 0.5 * SY)
        tri = VGroup(Line(a_, P3(b_[0], a_[1])).set_stroke(GEO, 2.5), Line(P3(b_[0], a_[1]), b_).set_stroke(GEO, 2.5))
        l_inc = VGroup(txt("INCLINAÇÃO", 22, bold=True, color=GEO), T(r"-1{,}96", 34, FC)).arrange(DOWN, buff=0.06).next_to(tri, RIGHT, buff=0.15)
        self.gat("é exatamente a inclinação")
        self.play(Create(tri), FadeIn(l_inc), run_time=0.7)
        l_fim = T(r"-1{,}18", 32, LMAG).next_to(P3(GX0 + 0.6 * SX, GY0 - 1.176 * SY), LEFT, buff=0.2)
        self.play(FadeIn(l_fim), run_time=0.4)
        self.ate(0.97)
        pedra.clear_updaters()
        l_m.clear_updaters()
        self.play(FadeOut(VGroup(pino, lO, pedra, cota, l_d, l_m, trilho, eixo_t, eixo_L, lt, lL, marca, tri, l_inc, l_fim, l_g)), OpVivo(rv, entra=False),
                  OpVivo(peso, entra=False), OpVivo(curva, entra=False), run_time=0.4)
