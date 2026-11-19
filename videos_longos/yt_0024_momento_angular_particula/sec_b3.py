"""Lote PB3 v2: B3 — O QUE MUDA L. Derivada de L⃗ = r⃗ × p⃗ (regra do produto, parcela paralela some) → τ⃗ = dL⃗/dt.
Conferência no Three.js 'painel_queda' (handoff v2 §2.4): painel vertical de laboratório com pino de aço em O, esfera de aço com anel rosa
(m = 0,50 kg) solta do repouso numa trilha a d = 0,40 m à direita do pino, eletroímã em cima (LED apaga na soltura), estroboscópio a cada
0,1 s; câmera ortográfica frontal (comprimentos verdadeiros, 2,4 u/m). Gráfico L_z × t no estilo grafico_lab, numa caixa própria à direita
do painel, com o ponto vivo acompanhando a esfera e o triângulo de inclinação cotado. Dados m, d, g no HUD embaixo do gráfico.
Notação (v2 §3.4): L_z = −(m g d) t; o parêntese inteiro voa para a inclinação."""
from pecas24 import *  # noqa: F401,F403

ESC = 2.4
CQ = camd(-90, 0, (0.4, 0, -0.9), ESC, 0.0, -5.44, -0.45)     # O = (0,0,0) → (−6,0; 2,0)
TQ_MAX = F.T_QUEDA


class LoteB3(Lote24):
    def corpo(self):
        self.canto(txt("O QUE MUDA", 30), T("L", 40, LMAG))
        tq = ValueTracker(0.0)          # tempo físico da queda
        ima = ValueTracker(1.0)
        sp = ValueTracker(0.35)         # parâmetro da partícula genérica (B3-1 a B3-3)
        self.add(tq, ima, sp)
        d = F.D_PEDRA

        def zq():
            t = tq.get_value()
            return -0.5 * F.G * t * t

        def estado(_t=0.0):
            t = tq.get_value()
            est = [[d, -0.5 * F.G * (0.1 * k) ** 2] for k in range(1, 7) if 0.1 * k < t - 1e-6]
            return r4(dict(cam=CQ, esfera=[d, zq()], estrobo=est, ima=float(ima.get_value())))
        # v3 §2.3: B3-1 a B3-3 sobre o mesmo compósito (tampo da mesa visto de cima, sem disco nem fio); o painel da queda só no B3-4
        self.camA = self.camB = CTOPO
        self.fio, self.disco_on, self.rastro_on = False, False, False
        fm = self.mesa()
        fm.op.set_value(1.0)
        f3 = Fundo3D(self, "painel_queda", estado, op=0.0)
        f3._fundo3d = True
        self.add(f3)
        tela = lambda x, z: proj(CQ, (x, -0.06, z))
        PO = tela(0, 0)

        def pos():
            return tela(d, zq())

        # partícula genérica numa trajetória curva no tampo: F⃗ constante (−y), v⃗ tangente, p⃗ = m v⃗
        Z = 0.012

        def pp(s):
            return np.array([-0.62 + 0.36 * s, 0.30 + 0.52 * s - 0.24 * s * s, Z])

        def vv(s):
            return np.array([0.36, 0.52 - 0.48 * s, 0.0])

        def cena_p():
            s = sp.get_value()
            p, v = pp(s), vv(s)
            a, b = self.tela((0, 0, Z)), self.tela(p)
            u = (b - a) / max(np.linalg.norm(b - a), 1e-6)
            n = np.array([-u[1], u[0], 0.0])
            if n[1] < 0:                         # §3 #5: r⃗ do lado de cima/direita (o paralelogramo r × F fica do outro lado)
                n = -n
            tv = self.tela(p + 0.42 * v)
            tpm = self.tela(p + 0.62 * v)
            tf_ = self.tela(p + np.array([0, -0.26, 0]))
            g = VGroup(vetor_lab(a, b, VETC, w=6, tip=0.2), T(r"\vec r", 40, VETC).move_to(a + 0.45 * (b - a) + 0.55 * n),
                       vetor_lab(b, tpm, MAG, w=5, origem=False), vetor_lab(b, tv, VEL, w=6, origem=False),
                       T(r"\vec p", 40, MAG).next_to(tpm, UR, buff=0.08), T(r"\vec v", 40, VEL).next_to(tv, UL, buff=0.08),
                       vetor_lab(b, tf_, FC, w=6, origem=False), T(r"\vec F", 40, FC).next_to(tf_, LEFT, buff=0.12),
                       VGroup(Circle(radius=0.12).move_to(b).set_fill(escuro(MAS, 0.3), 1).set_stroke(MAS, 3)).set_z_index(13))
            return g
        trilha = VMobject().set_points_smoothly([self.tela(pp(s)) for s in np.linspace(0, 2.2, 40)]).set_stroke(RAST, 2.5, opacity=0.55).set_z_index(4)

        # ── B3-1: derivada de L⃗ = r⃗ × p⃗ (uma partícula qualquer andando no tampo) ──
        self.an("B3-1")
        self.transicao(0.5)
        lO = T("O", 40, WHITE_).next_to(self.tela((0, 0, Z)), DR, buff=0.3)
        fase_ = [0.0]

        def vai_e_volta(m, dt):                  # v5 #16: vai e volta entre s = 0,35 e 1,00 (sem teletransporte no fim do ciclo; a partícula nunca passa por cima de O)
            fase_[0] += 0.10 * dt
            u_ = fase_[0] % 2.0
            m.set_value(0.35 + 0.65 * (u_ if u_ < 1.0 else 2.0 - u_))
        sp.add_updater(vai_e_volta)
        cp = vivo(cena_p)
        self.play(FadeIn(lO), Create(trilha), OpVivo(cp), run_time=0.6)
        A, ia = Mx(r"\vec L", "=", r"\vec r", r"\times", r"\vec p")
        self.pilha.poe(A)
        self.gat("derivar a definição no tempo")
        self.lei(A, ia, rt=0.9, metodo="lei")
        B, ib = Mx(r"\frac{d\vec L}{dt}", "=", r"\frac{d\vec r}{dt}", r"\times", r"\vec p", "+", r"\vec r", r"\times", r"\frac{d\vec p}{dt}")
        self.pilha.poe(B)
        self.gat("são duas parcelas")
        self.gm(A, B, (J(ia, 0), J(ib, 0)[1:3]), (J(ia, 1), J(ib, 1)), (J(ia, 2), J(ib, 2)[1:3]), (J(ia, 3), J(ib, 3)), (J(ia, 4), J(ib, 4)), rt=2.0)
        self.ate(0.99)

        # ── B3-2: cartão F⃗ = dp⃗/dt FORA da cadeia; dr⃗/dt → v⃗ e dp⃗/dt → F⃗; v⃗ × m v⃗: paralelogramo que se achata até zero ──
        self.an("B3-2")
        cart, cm, ic_ = cartao([r"\vec F", "=", r"\frac{d\vec p}{dt}"], "LEI DE NEWTON")
        self.gat("a derivada da posição é a velocidade")
        self.play(FadeIn(cart), run_time=0.4)
        C, ic = Mx("=", r"\vec v", r"\times", "m", r"\vec v", "+", r"\vec r", r"\times", r"\vec F")
        self.pilha.poe(C)
        self.gm(B, C, (J(ib, 2), J(ic, 1)), (J(ib, 3), J(ic, 2)), (J(ib, 4), J(ic, 3, 4)), (J(ib, 5), J(ic, 5)), (J(ib, 6), J(ic, 6)), (J(ib, 7), J(ic, 7)),
                (J(ib, 8), J(ic, 8)), ([], J(ic, 0)), rt=1.8, extra=(cart.animate(rate_func=there_and_back).set_opacity(1.0),))
        self.gat("na mesma direção")
        sp.clear_updaters()
        self.play(sp.animate.set_value(0.45), run_time=0.5)      # v5 #16: onde r⃗ × F⃗ aparece, a partícula está à esquerda de O com r⃗ a ~43° da vertical (F⃗ curta, só saindo dela)
        s0 = sp.get_value()
        P0, V0 = pp(s0), vv(s0)
        ang = ValueTracker(0.65)        # ângulo (rad) entre p⃗ e v⃗ desenhado: começa aberto e fecha até 0 (paralelos)

        def paral_vp():
            a_ = ang.get_value()
            c_, s_ = math.cos(a_), math.sin(a_)
            pv = 0.62 * np.array([V0[0] * c_ - V0[1] * s_, V0[0] * s_ + V0[1] * c_, 0.0])
            b = self.tela(P0)
            q1, q2 = self.tela(P0 + 0.42 * V0), self.tela(P0 + pv)
            return VGroup(Polygon(b, q1, q1 + (q2 - b), q2).set_fill(GEO, 0.35).set_stroke(GEO, 1.6),
                          vetor_lab(b, q2, MAG, w=5, origem=False)).set_z_index(12)
        pa = vivo(paral_vp)
        self.play(OpVivo(pa), run_time=0.4)
        self.play(ang.animate.set_value(0.0), run_time=1.2)
        lpar = txt("PARALELOS: ÁREA ZERO", 24, bold=True, color=GEO).move_to(P3(-4.25, -2.75))
        self.play(FadeIn(lpar), run_time=0.3)
        risco_ = Line(gl(C, J(ic, 1))[0].get_left() + P3(-0.05, -0.1), gl(C, J(ic, 4)).get_right() + P3(0.05, 0.12)).set_stroke(APAGADO, 4)
        self.gat("ela some")
        self.play(Create(risco_), run_time=0.5)
        D, id_ = Mx("=", "0", "+", r"\vec r", r"\times", r"\vec F")
        self.pilha.poe(D)
        zero_voo = pa.copy()
        self.gm(C, D, (J(ic, 0), J(id_, 0)), (J(ic, 1, 2, 3, 4), []), (J(ic, 5), J(id_, 2)), (J(ic, 6), J(id_, 3)), (J(ic, 7), J(id_, 4)),
                (J(ic, 8), J(id_, 5)), ([], J(id_, 1)), rt=1.3, extra=(FadeOut(risco_), zero_voo.animate.move_to(gl(D, J(id_, 1)).get_center()).scale(0.2).set_opacity(0)))
        self.remove(zero_voo)
        self.ate(0.99)

        # ── B3-3: r⃗ × F⃗ vira τ⃗ (o paralelogramo de r⃗ e F⃗ acende); τ⃗ = dL⃗/dt; o cartão acende ao lado; hipóteses em chips ──
        self.an("B3-3")
        self.play(OpVivo(pa, entra=False), FadeOut(lpar), run_time=0.3)
        self.remove(pa)
        Ef, ie = Mx(r"\frac{d\vec L}{dt}", "=", r"\vec r", r"\times", r"\vec F")
        self.pilha.poe(Ef)
        self.gat("que é o torque")
        b0, o0 = self.tela(P0), self.tela((0, 0, Z))
        fq = self.tela(P0 + np.array([0, -0.26, 0]))
        prf = Polygon(o0, b0, fq, o0 + (fq - b0)).set_fill(FC, 0.22).set_stroke(FC, 1.6).set_z_index(5)
        self.gm(D, Ef, (J(id_, 0), J(ie, 1)), (J(id_, 3), J(ie, 2)), (J(id_, 4), J(ie, 3)), (J(id_, 5), J(ie, 4)), (J(id_, 1, 2), []), ([], J(ie, 0)), rt=1.3,
                extra=(FadeIn(prf),))
        G_, ig = Mx(r"\vec\tau", "=", r"\frac{d\vec L}{dt}")
        self.pilha.poe(G_)
        self.gat("a taxa de variação do momento angular")
        self.gm(Ef, G_, (J(ie, 2, 3, 4), J(ig, 0)), (J(ie, 1), J(ig, 1)), (J(ie, 0), J(ig, 2)), rt=1.4)
        sub_ = self.resultado(G_, FC)
        self.gat("a força muda o momento linear")
        self.play(cart.animate(rate_func=there_and_back).set_opacity(1.0), pulso(G_, 1.04), run_time=1.0)
        self.alg("voo", G_, 1)
        self.gat("só com um cuidado")
        hip = chips(["PONTO FIXO", "REFERENCIAL INERCIAL",
                     linha_base([T(r"\tau", 36, FC), txt("E", 24, bold=True, color=CYAN), T("L", 36, LMAG), txt("NO MESMO PONTO", 24, bold=True, color=CYAN)], 0.1)])
        hip.move_to(P3(3.75, -3.55))
        hip.shift(RIGHT * (7.3 - hip.get_right()[0]))
        hip._chip = True
        self.play(LaggedStart(*[FadeIn(c) for c in hip], lag_ratio=0.3), run_time=0.9)
        self.ate(0.99)

        # ── B3-4: CONFERE: esfera de 0,50 kg a d = 0,40 m; cota d; peso; r⃗ acompanha ──
        self.an("B3-4")
        # troca de cena (no começo do B3-4): o tampo sai, o painel da queda entra (com a esfera presa no eletroímã)
        self.play(FadeOut(VGroup(trilha, lO, prf, hip, cart)), OpVivo(cp, entra=False), fm.op.animate.set_value(0.0), f3.op.animate.set_value(1.0), run_time=0.6)
        self.remove(cp)
        lO = T("O", 40, WHITE_).next_to(PO, LEFT, buff=0.3)

        def r_viva():
            a, b = PO, pos()
            u = (b - a) / max(np.linalg.norm(b - a), 1e-6)
            n = np.array([-u[1], u[0], 0.0])
            if n[0] + n[1] > 0:                  # v5 #28: rótulo do lado de baixo/esquerda do vetor (em cima ele encostava no LED do eletroímã)
                n = -n
            return VGroup(vetor_lab(a, b - 0.12 * u, VETC, w=6, tip=0.2), T(r"\vec r", 40, VETC).move_to(a + 0.5 * (b - a) + 0.40 * n + 0.15 * u))
        rv = vivo(r_viva)
        self.play(FadeIn(lO), OpVivo(rv), run_time=0.4)

        self.pilha.so(G_)
        self.selo("CONFERE", "UMA PEDRA CAINDO RETO")
        cota = DoubleArrow(tela(0.03, -0.15), tela(d - 0.05, -0.15), buff=0, stroke_width=4, tip_length=0.16).set_color(VETC).set_z_index(12)
        l_dc = T("d", 40, VETC).next_to(cota, DOWN, buff=0.1)
        h_m = hud("m", lambda: F.M_PEDRA if hasattr(F, "M_PEDRA") else 0.50, 2, "KG", MAS, slot=-3.3, x=-3.6)
        h_d = hud("d", lambda: d, 2, "M", VETC, slot=-3.3, x=-2.5)
        self.gat("uma pedra de meio quilo")
        self.play(FadeIn(cota), FadeIn(l_dc), OpVivo(h_m), OpVivo(h_d), run_time=0.6)

        def peso_vivo():
            p = pos()
            return VGroup(vetor_lab(p + P3(0, -0.15), p + P3(0, -1.05), FC, w=6, tip=0.2), T("mg", 40, FC).move_to(p + P3(0.62, -0.70)))      # v5 #28: o rótulo do peso na cor da força (azul), como a seta
        peso = vivo(peso_vivo)
        self.gat("ela cai reto")
        self.play(OpVivo(peso), run_time=0.5)
        self.ate(0.99)

        # ── B3-5: queda (×0,25) com o gráfico; L_z = x p_y − y p_x → −(m g d) t; τ_z = −m g d = −1,96 N·m; hold ──
        self.an("B3-5")
        self.sem_selo()
        self.pilha.limpa()
        graf, c2p = grafico_lab(-2.85, -0.95, 2.25, 2.75, (0.0, 0.66), (-1.32, 0.0), [0.2, 0.4, 0.6], [-0.39, -0.78, -1.18],
                                T("t", 36, WHITE_), T("L_z", 36, LMAG), rotx=[r"0{,}2", r"0{,}4", r"0{,}6"], roty=[r"-0{,}39", r"-0{,}78", r"-1{,}18"])
        self.play(FadeIn(graf), run_time=0.5)

        def curva_v():
            t = tq.get_value()
            if t < 1e-3:
                return ponto_vivo(c2p(0, 0), LMAG)
            return VGroup(curva_lab(c2p, lambda x: -1.96 * x, 0, t, LMAG, n=20), ponto_vivo(c2p(t, -1.96 * t), LMAG))
        curva = vivo(curva_v)
        self.add(curva)
        self.gat("ganha")
        self.play(ima.animate.set_value(0.0), run_time=0.2)
        self.play(tq.animate.set_value(TQ_MAX), run_time=2.4, rate_func=linear)
        A5, a5 = Mx("L_z", "=", "x", "p_y", "-", "y", "p_x")
        self.pilha.poe(A5)
        self.lei(A5, a5, rt=1.2, metodo="lei")
        # caso 16: a linha inteira em ORDEM, da esquerda para a direita (nada antecipado)
        B5, b5 = Mx("=", "d", r"(-m g t)", "-", "y", r"\cdot", "0", cores={1: VETC})
        self.pilha.poe(B5)
        self.gat("o momento linear para baixo cresce")
        self.lei(B5, b5, rt=1.5, metodo="escrita")
        risco2 = Line(gl(B5, J(b5, 3))[0].get_left() + P3(-0.05, -0.1), gl(B5, J(b5, 6)).get_right() + P3(0.05, 0.1)).set_stroke(APAGADO, 4)
        px0 = T(r"p_x=0", 30)                       # v13 §2.1: o termo riscado é explicado (a pedra não anda em x), abaixo do "0"
        px0.next_to(gl(B5, J(b5, 6)), DOWN, buff=0.22).align_to(gl(B5, J(b5, 6)), RIGHT)
        self.play(Create(risco2), FadeIn(px0), run_time=0.4)
        C5, c5 = Mx("L_z", "=", "-", "(", "m", "g", "d", ")", r"\,t", cores={6: VETC})
        self.pilha.poe(C5)
        self.gat("cresce em linha reta")
        self.gm(B5, C5, (J(b5, 0), J(c5, 1)), (J(b5, 2)[1:2], J(c5, 2)), (J(b5, 2)[0:1], J(c5, 3)), (J(b5, 2)[2:3], J(c5, 4)), (J(b5, 2)[3:4], J(c5, 5)),
                (J(b5, 1), J(c5, 6)), (J(b5, 2)[5:6], J(c5, 7)), (J(b5, 2)[4:5], J(c5, 8)), (J(b5, 3, 4, 5, 6), []), ([], J(c5, 0)), rt=1.5, extra=(FadeOut(risco2), FadeOut(px0)))
        self.resultado(C5, LMAG)
        # triângulo de inclinação cotado (Δt = 0,30 s; ΔL_z = −0,59)
        a_, b_ = c2p(0.2, -0.392), c2p(0.5, -0.98)
        q_ = P3(b_[0], a_[1])
        tri = VGroup(Line(a_, q_).set_stroke(GEO, 2.5), Line(q_, b_).set_stroke(GEO, 2.5)).set_z_index(15)
        c_t = T(r"0{,}30\,\mathrm{s}", 36, WHITE_).next_to(q_, UL, buff=0.08)
        c_L = T(r"-0{,}59", 36, LMAG).move_to((q_ + b_) / 2 + P3(0.55, 0))      # v3 #5: à direita do cateto vertical, longe da reta
        self.gat("e o torque do peso")
        par_ = VGroup(*gl(C5, J(c5, 2, 3, 4, 5, 6, 7))).copy()
        inc = T(r"-1{,}96\,\mathrm{N\,m}", 36, FC).move_to(c2p(0.27, -1.19))
        self.play(Create(tri), FadeIn(c_t), FadeIn(c_L), par_.animate.move_to(inc.get_center()).scale(0.6), run_time=0.9)
        self.play(FadeTransform(par_, inc), run_time=0.4)
        D5, d5 = Mx(r"\tau_z", "=", "-", "m", "g", "d", cores={5: VETC})
        self.pilha.so(C5)
        self.pilha.poe(D5)
        self.lei(D5, d5, {3: h_m, 5: h_d}, rt=1.2)
        h_g = hud("g", lambda: F.G, 1, "M/S²", ACC, slot=-3.3, x=-1.4)
        self.play(OpVivo(h_g), run_time=0.3)
        E5, e5 = Mx("=", "-", r"0{,}50", r"\cdot", r"9{,}8", r"\cdot", r"0{,}40", cores={2: MAS, 4: ACC, 6: VETC})
        self.pilha.poe(E5)
        self.gat("menos um vírgula noventa e seis")
        self.lei(E5, e5, {2: h_m, 4: h_g, 6: h_d}, rt=1.4, numero=True)
        F5, f5 = Mx("=", "-", r"1{,}96", r"\,\mathrm{N\,m}", cores={2: FC})
        self.pilha.poe(F5)
        self.lei(F5, f5, rt=0.8, numero=True)
        self.resultado(F5, FC)
        self.gat("é exatamente a inclinação")
        self.play(Indicate(inc, color=FC, scale_factor=1.15), Indicate(tri, color=FC, scale_factor=1.0), run_time=0.6)
        # pausa útil: a queda repete (o ponto vivo corre de novo a reta)
        self.play(tq.animate.set_value(0.0), ima.animate.set_value(1.0), run_time=0.4)
        self.play(ima.animate.set_value(0.0), run_time=0.2)
        self.play(tq.animate.set_value(TQ_MAX), run_time=1.2, rate_func=linear)      # v5: a repetição da queda mais curta (a escrita sequencial gastou 1,8 s da âncora)
        self.ate(0.995)
