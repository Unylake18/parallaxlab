"""Lote P1 (handoff v3 do lote 1, visual novo): T1 — onde está o centro de massa?
T1-1 haltere 2D de cima, girando em torno do ⊕ em degradê, rastros circulares finos · T1-2 o giro para com a haste alinhada à régua e passa
ao perfil no mesmo lugar; régua colada às bolas, cotas acima da régua, apoio e balanço · T1-3 alavanca m₁d₁ = m₂d₂ (pesos 1 : 3) · T1-4 abre os parênteses → junta os X → X em evidência →
X = (m₁x₁ + m₂x₂)/(m₁ + m₂) (TransformByGlyphMap em cada passo), caixa PANEL · T1-5 origem nova · T1-6 três massas; Σ mᵢ r⃗ᵢ = (6, 4) como soma
de vetores ponta com ponta; ÷ 4 → R⃗_cm · T1-7 bandeja 3D (Three.js): pino no centro geométrico → tomba para o 2 kg; pino no ⊕ → parada;
Σ mᵢ (r⃗ᵢ − R⃗_cm) = 0⃗; pesos → M g⃗ (DICA) · T1-8 por partes: as duas de 1 kg viram uma de 2 kg em (3, 2); o ⊕ no meio.
Cor por token (G12): X e R⃗_cm ciano-claro, posições GEO, pesos FC."""
from MF_Tools import TransformByGlyphMap

from camadas import *  # noqa: F401,F403

YC = 0.0                      # altura do ⊕ (e da haste) na tela
O6, K6 = P3(-6.15, -2.3), 1.05  # origem e escala do plano do T1-6 (a bandeja do T1-7 nasce no mesmo lugar)


def mp(m, idx, partes):
    """Glifos das partes `partes` (índices de eqp) de um MathTex."""
    return VGroup(*[m[0][j] for k in partes for j in idx[k]])


class LoteT1(Camadas):
    def construct(self):
        self.setup_base(cap="ONDE ESTÁ O CENTRO DE MASSA?")
        self.t1_1()
        self.t1_2()
        self.t1_3()
        self.t1_4()
        self.t1_5()
        self.t1_6()
        self.t1_7()
        self.t1_8()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    # ── T1-1 ────────────────────────────────────────────────────────────────────────────────────────────
    def t1_1(self):
        self.an("T1-1")
        h = self.haltere_giro(giro=0.1)                       # o lote abre com o haltere já em cena (G5): vista de cima, sem 3D
        q = txt("ONDE ESTÁ?", 40, bold=True).move_to(CONTA_C + 0.6 * UP)
        self.play(FadeIn(q, shift=0.1 * UP), run_time=0.6)
        self.q = q
        self.ate(0.8)                                         # "ele fica bem mais perto da bola pesada"
        self.play(self.h_pul.animate(rate_func=there_and_back).set_value(1.0), run_time=0.7)
        self.ate(0.97)

    # ── T1-2: régua colada, apoio e balanço ─────────────────────────────────────────────────────────────
    def t1_2(self):
        h = self.h
        self.an("T1-2")
        self.play(FadeOut(self.selo_cam), run_time=0.4)
        h.parar(2.6)                                             # para alinhado à régua: a vista de perfil, sem salto
        xs = [h.p(x)[0] for x in (-3, -2, -1, 0, 1)]
        self.xs = xs
        yr = YC + h.R2 * h.K + 0.22                             # logo acima das bolas
        self.yr = yr
        reg = VGroup(Line(P3(xs[0] - 0.45, yr), P3(xs[-1] + 0.45, yr)).set_stroke(GEO, 2.4))
        for x in xs:
            reg.add(Line(P3(x, yr - 0.1), P3(x, yr + 0.1)).set_stroke(GEO, 2.4))
        nums = VGroup(*[rot(str(k), 30, GEO).next_to(P3(x, yr + 0.1), UP, buff=0.08) for k, x in enumerate(xs)])
        un = VGroup(MathTex("x", font_size=36, color=GEO), rot("(m)", 30, GEO)).arrange(RIGHT, buff=0.1) \
            .next_to(P3(xs[-1] + 0.45, yr), RIGHT, buff=0.14)
        b1, b2 = h.p(h.X1), h.p(h.X2)
        m1 = rot("1 kg", 34).move_to(b1 + P3(-0.8, -h.R1 * h.K - 0.32))
        m2 = rot("3 kg", 34).move_to(b2 + P3(1.0, -h.R2 * h.K - 0.3))
        self.ate(0.3)
        self.play(Create(reg), FadeIn(nums), FadeIn(un), FadeIn(m1), FadeIn(m2), run_time=0.9)
        self.reg_, self.nums, self.un, self.m1, self.m2 = reg, nums, un, m1, m2
        self.ate(0.5)
        h.apoiar(dur=1.6, balanco=2.6)                           # o balanço cai em "em equilíbrio"
        yc_ = yr + 1.05                                          # cotas acima da régua: os pesos (T1-3) não as cruzam
        self.d1 = cota(xs[0], xs[3], yc_, rot_cota("3 m", "d_1"), lado=UP)
        self.d2 = cota(xs[3], xs[4], yc_, rot_cota("1 m", "d_2"), lado=UP)
        self.yc_ = yc_
        self.d2[1].shift(0.35 * RIGHT)
        self.ate(0.82)
        self.play(FadeIn(self.d1), FadeIn(self.d2), run_time=0.8)
        self.ate(0.97)

    # ── T1-3 ────────────────────────────────────────────────────────────────────────────────────────────
    def t1_3(self):
        h = self.h
        self.an("T1-3")
        pul = ValueTracker(0.0)
        self.add(pul)

        def pesos():
            w = 6 + 3 * pul.get_value()
            b1, b2 = h.p(h.X1), h.p(h.X2)
            r1, r2 = h.R1 * h.K, h.R2 * h.K
            return VGroup(seta(b1 + r1 * DOWN, b1 + (r1 + 0.6) * DOWN, FC, w, tip=0.2),
                          seta(b2 + r2 * DOWN, b2 + (r2 + 1.8) * DOWN, FC, w, tip=0.24)).set_z_index(12)   # 1 : 3
        self.pesos = vivo(pesos)
        self.play(FadeIn(self.pesos), FadeOut(self.q), run_time=0.6)
        e1 = Mc((r"m_1", WHITE_), (r"d_1", GEO), "=", (r"m_2", WHITE_), (r"d_2", GEO), size=56)
        na_conta(e1, 1.7)
        self.ate(0.25)
        self.play(TransformFromCopy(self.m1, e1[0]), TransformFromCopy(self.d1[1][0], e1[1]), run_time=1.0)
        self.play(FadeIn(e1[2]), TransformFromCopy(self.m2, e1[3]), TransformFromCopy(self.d2[1][0], e1[4]), run_time=1.0)
        xs = self.xs
        pr1 = rot("1 kg · 3 m", 30).move_to(P3((xs[0] + xs[3]) / 2, self.yc_ + 0.85))       # cada lado do apoio: massa × distância
        pr2 = rot("3 kg · 1 m", 30).move_to(P3(xs[4] + 0.6, self.yc_ + 0.85))
        self.ate(0.42)
        self.play(FadeIn(pr1, shift=0.1 * UP), Indicate(self.m1, color=WHITE_, scale_factor=1.15), run_time=0.7)
        self.ate(0.5)
        self.play(FadeIn(pr2, shift=0.1 * UP), Indicate(self.m2, color=WHITE_, scale_factor=1.15), run_time=0.7)
        e2 = Mc(r"1\cdot 3", "=", r"3\cdot 1", size=56)
        na_conta(e2, 0.6)
        self.ate(0.62)
        self.play(FadeIn(e2, shift=0.1 * DOWN), run_time=0.7)
        for _ in range(2):
            self.play(pul.animate.set_value(1.0), run_time=0.5, rate_func=there_and_back)
        n12 = cartao("MASSA GRANDE, PERTO;", "MASSA PEQUENA, LONGE")
        na_conta(n12, -0.85)
        self.ate(0.82)
        self.play(FadeIn(n12), run_time=0.6)
        self.ate(0.97)
        self.c13 = VGroup(e1, e2, n12, pr1, pr2)

    # ── T1-4: a fórmula passo a passo ───────────────────────────────────────────────────────────────────
    def t1_4(self):
        self.an("T1-4")
        xs = self.xs
        l1 = eqp("X", "-", "x_1", size=36, cores={0: CMC, 2: GEO})[0].move_to(self.d1[1])
        l2 = eqp("x_2", "-", "X", size=36, cores={0: GEO, 2: CMC})[0].move_to(self.d2[1])
        yb = YC - self.h.R2 * self.h.K - 0.95                    # x₁, X, x₂ abaixo das bolas e do apoio (os pesos já saíram)
        lx = VGroup(mtex("x_1", GEO, 36).move_to(P3(xs[0], yb)), mtex("X", CMC, 36).move_to(P3(xs[3], yb)), mtex("x_2", GEO, 36).move_to(P3(xs[4], yb)))
        self.play(FadeOut(self.c13), FadeOut(self.pesos), FadeOut(self.d1[1]), FadeOut(self.d2[1]), run_time=0.6)   # os rótulos velhos saem antes
        self.pesos.clear_updaters()
        self.remove(self.pesos)
        self.play(FadeIn(l1), FadeIn(l2), FadeIn(lx), run_time=0.7)
        self.d1[1], self.d2[1] = l1, l2
        G, X_ = GEO, CMC
        A, ia = eqp("m_1", "(", "X", "-", "x_1", ")", "=", "m_2", "(", "x_2", "-", "X", ")", size=46, cores={2: X_, 4: G, 9: G, 11: X_})
        S1, i1 = eqp("m_1", "X", "-", "m_1", "x_1", "=", "m_2", "x_2", "-", "m_2", "X", size=46, cores={1: X_, 4: G, 7: G, 10: X_})
        S2, i2 = eqp("m_1", "X", "+", "m_2", "X", "=", "m_1", "x_1", "+", "m_2", "x_2", size=46, cores={1: X_, 4: X_, 7: G, 10: G})
        S3, i3 = eqp("X", "(", "m_1", "+", "m_2", ")", "=", "m_1", "x_1", "+", "m_2", "x_2", size=46, cores={0: X_, 8: G, 11: G})
        C = MathTex(r"X=\frac{m_1x_1+m_2x_2}{m_1+m_2}", font_size=56, color=WHITE_)
        C[0][0].set_color(X_)
        for j in (4, 5, 9, 10):
            C[0][j].set_color(G)
        C._partes = [("X", X_), ("x_1", G), ("x_2", G)]
        for E_, y_ in ((A, 2.45), (S1, 1.7), (S2, 0.95), (S3, 0.2)):
            na_conta(E_, y_)
        na_conta(C, -1.0)
        J = lambda idx, *ks: [j for k in ks for j in idx[k]]
        self.ate(0.1)
        self.play(TransformFromCopy(VGroup(self.m1, l1), mp(A, ia, range(0, 6))), TransformFromCopy(VGroup(self.m2, l2), mp(A, ia, range(7, 13))),
                  FadeIn(mp(A, ia, [6])), run_time=1.2)
        # abre os parênteses: m₁ e m₂ distribuem
        self.ate(0.22)
        self.play(TransformByGlyphMap(A.copy(), S1, (J(ia, 0), J(i1, 0, 3)), (J(ia, 2), J(i1, 1)), (J(ia, 3), J(i1, 2)), (J(ia, 4), J(i1, 4)),
                                      (J(ia, 6), J(i1, 5)), (J(ia, 7), J(i1, 6, 9)), (J(ia, 9), J(i1, 7)), (J(ia, 10), J(i1, 8)), (J(ia, 11), J(i1, 10)),
                                      (J(ia, 1, 5, 8, 12), []), auto_fade=True), run_time=1.4)
        # junta os X: −m₂X atravessa e vira +m₂X; −m₁x₁ atravessa e vira +m₁x₁
        self.ate(0.3)
        self.play(TransformByGlyphMap(S1.copy(), S2, (J(i1, 0), J(i2, 0)), (J(i1, 1), J(i2, 1)), (J(i1, 8), J(i2, 2)), (J(i1, 9), J(i2, 3)),
                                      (J(i1, 10), J(i2, 4)), (J(i1, 5), J(i2, 5)), (J(i1, 3), J(i2, 6)), (J(i1, 4), J(i2, 7)), (J(i1, 2), J(i2, 8)),
                                      (J(i1, 6), J(i2, 9)), (J(i1, 7), J(i2, 10))), run_time=1.6)
        # X em evidência
        self.ate(0.38)
        self.play(TransformByGlyphMap(S2.copy(), S3, (J(i2, 1, 4), J(i3, 0)), (J(i2, 0), J(i3, 2)), (J(i2, 2), J(i3, 3)), (J(i2, 3), J(i3, 4)),
                                      (J(i2, 5), J(i3, 6)), (J(i2, 6, 7, 8, 9, 10), J(i3, 7, 8, 9, 10, 11)), ([], J(i3, 1, 5)), auto_fade=True),
                  run_time=1.4)
        # (m₁ + m₂) desce como divisor: aparece a fórmula
        self.ate(0.45)
        self.play(TransformByGlyphMap(S3.copy(), C, (J(i3, 0), [0]), (J(i3, 6), [1]), (J(i3, 7, 8, 9, 10, 11), list(range(2, 11))),
                                      (J(i3, 2, 3, 4), [12, 13, 14, 15, 16]), (J(i3, 1, 5), []), ([], [11]), auto_fade=True), run_time=1.6)
        cx = caixa(C, cor=CMC)
        self.play(FadeIn(cx), run_time=0.5)                       # "aparece a fórmula"
        self.wait(2.0)                                            # pausa útil: é a fórmula do vídeo
        # os passos saem; a fórmula sobe; a frase em cartão; os números da régua entram na substituição
        self.play(FadeOut(VGroup(A, S1, S2, S3)), VGroup(C, cx).animate.move_to(P3(CONTA_C[0], 1.75)), run_time=0.8)
        nt = cartao("MÉDIA DAS POSIÇÕES,", "PESADA PELAS MASSAS")
        na_conta(nt, 0.15)
        self.ate(0.66)
        self.play(FadeIn(nt), run_time=0.6)
        D, idd = eqp("X", "=", r"\frac{1\cdot 0+3\cdot 4}{4}", "=", r"3\ \mathrm{m}", size=50, cores={0: X_})
        na_conta(D, -1.35)
        self.ate(0.8)
        num = D[0][2:11]                                          # 1 · 0 + 3 · 4 , barra, 4
        fora = VGroup(*[g_ for k, g_ in enumerate(D[0]) if k not in (2, 4, 6, 8)])
        self.play(TransformFromCopy(self.m1[0], num[0]), TransformFromCopy(self.nums[0], num[2]), TransformFromCopy(self.m2[0], num[4]),
                  TransformFromCopy(self.nums[4], num[6]), FadeIn(fora), run_time=1.2)
        self.play(self.h_pul.animate(rate_func=there_and_back).set_value(1.0), run_time=0.6)
        self.ate(0.97)
        self.form, self.cx, self.D, self.lx, self.nt4 = C, cx, D, lx, nt

    # ── T1-5 ────────────────────────────────────────────────────────────────────────────────────────────
    def t1_5(self):
        self.an("T1-5")
        xs = self.xs
        self.play(FadeOut(self.nt4), self.D.animate.move_to(P3(CONTA_C[0], 0.2)), run_time=0.7)
        tri = Triangle().scale(0.13).set_stroke(width=0).set_fill(GEO, 1).rotate(PI).move_to(P3(xs[0], self.yr + 0.66))
        org = VGroup(tri, VGroup(MathTex("x", font_size=42, color=GEO), rot("= 0", 36, GEO)).arrange(RIGHT, buff=0.1).next_to(tri, RIGHT, buff=0.12))
        self.ate(0.08)
        self.play(FadeOut(self.lx), FadeIn(org), run_time=0.5)
        ext = Line(P3(xs[0] - 0.45, self.yr), P3(max(-7.5, xs[0] - 2 * self.h.K - 0.3), self.yr)).set_stroke(GEO, 2.4)
        tk = VGroup(*[Line(P3(xs[0] - k * self.h.K, self.yr - 0.1), P3(xs[0] - k * self.h.K, self.yr + 0.1)).set_stroke(GEO, 2.4) for k in (1, 2)])
        self.play(Create(ext), FadeIn(tk), run_time=0.6)
        novos = VGroup(*[rot(str(k + 2), 30, GEO).move_to(n) for k, n in enumerate(self.nums)])
        self.play(org.animate.shift(2 * self.h.K * LEFT), *[FadeTransform(a, b) for a, b in zip(self.nums, novos)], run_time=1.6)
        self.nums = novos
        D2, _ = eqp("X", "=", r"\frac{1\cdot 2+3\cdot 6}{4}", "=", r"5\ \mathrm{m}", size=50, cores={0: CMC})
        D2.move_to(self.D)
        self.ate(0.4)
        self.play(TransformByGlyphMap(self.D, D2, *[([i], [i]) for i in range(len(D2[0]))]), run_time=1.2)     # só os números trocam, no lugar
        self.play(self.h_pul.animate(rate_func=there_and_back).set_value(1.0), run_time=0.6)                  # o ⊕ não andou
        self.D = D2
        selo = txt("O NÚMERO MUDA, O PONTO NÃO", 30, bold=True).move_to(P3(PALCO_C[0], -2.85))
        self.ate(0.62)
        self.play(FadeIn(selo, shift=0.1 * UP), run_time=0.8)
        # "O centro de massa é um lugar do sistema": o prumo do ⊕ até a régua marca o lugar; o número embaixo dele é só a leitura
        cmh = self.h.cm
        prumo = DashedLine(cmh + 0.3 * UP, P3(cmh[0], self.yr - 0.05), dash_length=0.08).set_stroke(WHITE_, 2, opacity=0.75)
        self.ate(0.74)
        self.play(Create(prumo), onda(cmh), run_time=0.8)
        self.ate(0.86)
        self.play(Indicate(self.nums[3], color=WHITE_, scale_factor=1.35), run_time=0.8)
        self.ate(0.97)
        self.t15 = VGroup(org, ext, tk, selo, prumo)

    # ── T1-6: três massas no plano; Σ mᵢ r⃗ᵢ como soma de vetores ────────────────────────────────────────
    def t1_6(self):
        h = self.h
        self.an("T1-6")
        h.mob.clear_updaters()
        velhos = [self.reg_, self.nums, self.un, self.m1, self.m2, self.d1, self.d2, self.t15, h.mob, self.form, self.cx, self.D, *h.trackers()]
        O, k = O6, K6
        Pw = lambda x, y: O + k * P3(x, y)
        ax = self.eixos6()
        dados = self.dados = [(2.0, (0, 0)), (1.0, (4, 0)), (1.0, (2, 4))]
        self.massas, self.kgs, self.coords = VGroup(), VGroup(), VGroup()
        lados = [(UP, DOWN), (UP, DOWN), (UP, RIGHT)]                 # (rótulo de massa, coordenadas)
        for (m, (x, y)), (lk, lc) in zip(dados, lados):
            b = esfera2d(0.32 * m ** (1 / 3)).move_to(Pw(x, y)).set_z_index(6)
            self.massas.add(b)
            self.kgs.add(rot(f"{m:g} kg", 30).next_to(b, lk, buff=0.16))
            self.coords.add(mtex(rf"({x},\,{y})", GEO, 36).next_to(b, lc, buff=0.18))
        self.coords[0].shift(0.45 * RIGHT)
        self.kgs[0].shift(0.6 * LEFT + 0.05 * DOWN)
        self.kgs[1].shift(1.0 * LEFT)                                   # acima à esquerda: a cópia de r⃗₃ sai desta bola para cima
        r2 = seta(O, Pw(4, 0) + 0.34 * LEFT, GEO, 4, tip=0.22, z=5)
        r3e = Pw(2, 4)
        r3 = seta(O, r3e - (r3e - O) / np.linalg.norm(r3e - O) * 0.36, GEO, 4, tip=0.22, z=5)
        self.vets = VGroup(r2, r3, mtex(r"\vec r_2", GEO, 38).move_to(Pw(3.0, 0) + 0.4 * DOWN),   # longe do tique "2"
                           mtex(r"\vec r_3", GEO, 38).move_to(Pw(0.75, 2.2) + 0.25 * LEFT),
                           mtex(r"\vec r_1=\vec 0", GEO, 36).move_to(O + P3(0.45, -1.15)))
        ex, _ = eqp("X", "=", r"\frac{\sum_i m_i x_i}{M}", size=48, cores={0: CMC})
        ey, _ = eqp("Y", "=", r"\frac{\sum_i m_i y_i}{M}", size=48, cores={0: CMC})
        na_conta(ex, 2.55); na_conta(ey, 2.55, x0=4.55)
        self.troca(velhos, FadeIn(ax), LaggedStart(*[FadeIn(b, scale=0.8) for b in self.massas], lag_ratio=0.2), FadeIn(self.kgs),
                   FadeIn(ex), seq=True)
        self.play(FadeIn(self.vets), FadeIn(self.coords), run_time=0.7)
        pv = DashedLine(Pw(2, 4) + 0.34 * DOWN, Pw(2, 0), dash_length=0.08).set_stroke(GEO, 2, opacity=0.7)
        ph = DashedLine(Pw(2, 4) + 0.34 * LEFT, Pw(0, 4), dash_length=0.08).set_stroke(GEO, 2, opacity=0.7)
        tx = VGroup(Line(Pw(2, 0) + 0.1 * DOWN, Pw(2, 0) + 0.1 * UP).set_stroke(GEO, 2.4), rot("2", 28, GEO).next_to(Pw(2, 0), DOWN, buff=0.16))
        ty = VGroup(Line(Pw(0, 4) + 0.1 * LEFT, Pw(0, 4) + 0.1 * RIGHT).set_stroke(GEO, 2.4), rot("4", 28, GEO).next_to(Pw(0, 4), LEFT, buff=0.16))
        self.ate(0.07)
        self.play(Create(pv), FadeIn(tx), run_time=0.7)                  # a coordenada horizontal
        self.ate(0.13)
        self.play(Create(ph), FadeIn(ty), run_time=0.7)                  # a vertical
        self.ate(0.2)
        self.play(LaggedStart(*[Indicate(cd, color=WHITE_, scale_factor=1.2) for cd in self.coords], lag_ratio=0.4), run_time=1.8)
        self.ate(0.3)
        self.play(FadeIn(ey), run_time=0.7)
        ez = VGroup(DashedLine(O, O + P3(-0.75, -0.62), dash_length=0.08).set_stroke(GEO, 2, opacity=0.6),
                    mtex("z", GEO, 36).set_opacity(0.8).move_to(O + P3(-0.98, -0.62)))
        self.ate(0.37)
        self.play(Create(ez[0]), FadeIn(ez[1]), run_time=0.8)          # "e a de profundidade, igual"
        R, ir = eqp(r"\vec R_{cm}", "=", r"\frac{\sum_i m_i\vec r_i}{M}", size=56, cores={0: CMC})
        na_conta(R, 1.2)
        self.ate(0.45)
        self.play(TransformMatchingTex(VGroup(ex, ey).copy(), R), run_time=1.2)
        # Σ mᵢ r⃗ᵢ = 2 (0, 0) + 1 (4, 0) + 1 (2, 4) = (6, 4): cada massa e cada par saem do desenho
        S, i_s = eqp(r"\sum_i m_i\vec r_i", "=", "2", r"\,(0,\,0)", "+", "1", r"\,(4,\,0)", size=46)
        S[0][0:len(i_s[0])][-3:].set_color(GEO)
        na_conta(S, -0.05)
        Sb, i_b = eqp("+", "1", r"\,(2,\,4)", size=46)
        Sb.move_to(P3(XC0 + 1.3 + Sb.width / 2, -0.8))
        S2, _ = eqp("=", r"(6,\,4)", size=46, cores={1: GEO})
        S2.next_to(Sb, RIGHT, buff=0.2)
        self.ate(0.6)
        anims = [FadeIn(mp(S, i_s, [0, 1, 4])), FadeIn(mp(Sb, i_b, [0]))]
        for i, (E_, ix_, km, kp) in enumerate(((S, i_s, 2, 3), (S, i_s, 5, 6), (Sb, i_b, 1, 2))):
            anims += [TransformFromCopy(self.kgs[i][0], mp(E_, ix_, [km])), TransformFromCopy(self.coords[i][0], mp(E_, ix_, [kp]))]
        self.play(*anims, run_time=1.4)
        # no PALCO: 1·r⃗₂ e 1·r⃗₃ ponta com ponta dão a seta (6, 4)
        r3b = seta(Pw(4, 0), Pw(6, 4), GEO, 4, tip=0.22, z=5)
        soma = seta(O, Pw(6, 4), GEO, 6, tip=0.26, z=7)
        ls = mtex(r"\sum_i m_i\vec r_i", GEO, 38).move_to(Pw(6, 4) + P3(-1.45, 0.22))       # à esquerda da ponta (longe da CONTA)
        self.play(TransformFromCopy(r3, r3b), run_time=0.9)
        self.play(Create(soma), FadeIn(ls), FadeIn(S2), run_time=0.9)
        self.ate(0.77)                                                 # "seis na horizontal e quatro na vertical"
        self.play(Indicate(S2, color=WHITE_, scale_factor=1.15), Indicate(ls, color=WHITE_, scale_factor=1.15), run_time=0.9)
        # ÷ 4: a seta encolhe até o ⊕
        F, i_f = eqp(r"\vec R_{cm}", "=", r"\frac{(6,\,4)}{4}", "=", r"(1{,}5;\ 1{,}0)", size=50, cores={0: CMC, 4: CMC})
        na_conta(F, -2.15)
        rcm = seta(O, Pw(1.5, 1.0) - (Pw(1.5, 1.0) - O) / np.linalg.norm(Pw(1.5, 1.0) - O) * 0.24, GEO, 6, tip=0.24, z=7)
        self.cm6 = marcador_cm(Pw(1.5, 1.0))
        self.ate(0.88)
        self.play(ReplacementTransform(soma, rcm), FadeOut(ls), FadeOut(r3b), FadeIn(F), run_time=1.2)
        cxF = caixa(F, cor=CMC)
        c = self.cm6.get_center()
        cotas = VGroup(DashedLine(c, P3(c[0], O[1]), dash_length=0.08).set_stroke(WHITE_, 1.8, opacity=0.7),
                       DashedLine(c, P3(O[0], c[1]), dash_length=0.08).set_stroke(WHITE_, 1.8, opacity=0.7),
                       rot("1,5", 28).next_to(P3(c[0], O[1]), DOWN, buff=0.14),
                       rot("1,0", 28).next_to(P3(O[0], c[1]), LEFT, buff=0.14))
        self.play(FadeIn(self.cm6, scale=1.4), FadeIn(cxF), Create(cotas[0]), Create(cotas[1]), FadeIn(cotas[2:]), run_time=0.8)
        self.ate(0.97)
        self.t16 = VGroup(ax, self.vets, self.coords, cotas, ex, ey, S, Sb, S2, F, cxF, rcm, self.kgs, pv, ph, tx, ty, ez)
        self.R = R

    # ── T1-7: bandeja 3D; pino fora do ⊕ → tomba; no ⊕ → parada ─────────────────────────────────────────
    def t1_7(self):
        self.an("T1-7")
        cmt = O6 + K6 * P3(1.5, 1.0)
        bd = self.bd = Bandeja3D(self, K=K6, cm_tela=cmt, op=0.0)
        self.add(*bd.trackers(), bd.f3d)
        self._corpos3d = [lambda: [(c_, r_) for c_, r_, _ in bd.bolas()]]
        cmv = vivo(lambda: marcador_cm(self.reg("band", cm=bd.p((1.5, 1.0, 0.0)), bolas=[c_ for c_, _, _ in bd.bolas()])["cm"]))
        velhos = [*self.t16, self.massas, self.cm6]
        # o plano vira a bandeja (vista de cima, mesmas posições); a câmera inclina até ~25°
        self.play(*[FadeOut(m) for m in velhos], bd.f3d.op.animate.set_value(1.0), FadeIn(cmv),
                  self.R.animate.move_to(P3(CONTA_C[0], 2.4)), run_time=0.8)
        for m in velhos:
            m.clear_updaters()
        self.remove(*velhos)
        self.play(bd.el.animate.set_value(25.0), run_time=1.4)
        # "Apoia fora dele": o pino sobe no centro geométrico (2; 1,33) e a bandeja tomba para o lado do 2 kg
        self.ate(0.1)
        bd.pv.set_value(1.0)
        self.play(bd.pz.animate.set_value(0.0), run_time=0.8)
        self.play(bd.ang.animate(rate_func=rate_functions.ease_in_quad).set_value(math.radians(8)), run_time=1.4)
        self.wait(0.3)
        # volta à horizontal; o pino vai para o ⊕ (1,5; 1,0): "apoia nele, e ela fica parada"
        self.play(bd.ang.animate.set_value(0.0), bd.pz.animate.set_value(-0.9), run_time=0.7)
        self.play(bd.px.animate.set_value(1.5), bd.py.animate.set_value(1.0), run_time=0.9)
        self.play(bd.pz.animate.set_value(0.0), run_time=0.6)
        parada = txt("PARADA", 28, bold=True).move_to(cmt + P3(2.2, 1.6))
        self.play(FadeIn(parada), run_time=0.4)
        # a conta: Σ mᵢ (r⃗ᵢ − R⃗_cm) = Σ mᵢ r⃗ᵢ − M R⃗_cm = M R⃗_cm − M R⃗_cm = 0⃗ ; no PALCO as setas r⃗ᵢ − R⃗_cm saem do ⊕
        G = GEO
        B1, i1 = eqp(r"\sum_i", "m_i", "(", r"\vec r_i", "-", r"\vec R_{cm}", ")", size=48, cores={3: G, 5: CMC})
        B2, i2 = eqp("=", r"\sum_i", "m_i", r"\vec r_i", "-", "M", r"\vec R_{cm}", size=48, cores={3: G, 6: CMC})
        B3, i3 = eqp("=", "M", r"\vec R_{cm}", "-", "M", r"\vec R_{cm}", size=48, cores={2: CMC, 5: CMC})
        B4, i4 = eqp("=", r"\vec 0", size=48)
        na_conta(B1, 1.15)
        for E_, y_ in ((B2, 0.1), (B3, -0.85), (B4, -1.65)):
            E_.move_to(P3(XC0 + 0.55 + E_.width / 2, y_))
        rel = ValueTracker(0.0)
        self.add(rel)

        def relativas():
            o = rel.get_value()
            if o < 0.01:
                return VGroup()
            c0 = bd.p((1.5, 1.0, 0.0))
            g = VGroup()
            for c_, r_, _ in bd.bolas():
                d = c_ - c0
                g.add(seta(c0 + d / np.linalg.norm(d) * 0.26, c_ - d / np.linalg.norm(d) * (r_ + 0.04), mix(GEO, 0.35), 4, tip=0.2, op=o))
            return g.set_z_index(12)
        relv = vivo(relativas)
        self.add(relv)
        self.ate(0.22)
        self.play(FadeOut(parada), FadeIn(B1), rel.animate.set_value(1.0), run_time=0.9)
        J = lambda idx, *ks: [j for k in ks for j in idx[k]]
        self.ate(0.36)
        self.play(TransformByGlyphMap(B1.copy(), B2, ([], J(i2, 0)), (J(i1, 0), J(i2, 1)), (J(i1, 1), J(i2, 2)), (J(i1, 3), J(i2, 3)),
                                      (J(i1, 4), J(i2, 4)), (J(i1, 5), J(i2, 6)), ([], J(i2, 5)), (J(i1, 2, 6), []), auto_fade=True), run_time=1.3)
        # Σ mᵢ r⃗ᵢ vira M R⃗_cm (da fórmula do T1-6, no alto da CONTA)
        self.ate(0.44)
        self.play(FadeIn(mp(B3, i3, [0])), TransformFromCopy(self.R, mp(B3, i3, [1, 2])), TransformFromCopy(mp(B2, i2, [4, 5, 6]), mp(B3, i3, [3, 4, 5])),
                  run_time=1.2)
        riscos = VGroup(risco(mp(B3, i3, [1, 2]), WHITE_, 3), risco(mp(B3, i3, [4, 5]), WHITE_, 3))
        self.play(Create(riscos), run_time=0.6)
        self.play(FadeIn(B4, shift=0.1 * DOWN), run_time=0.6)
        cx4 = caixa(B4, cor=GEO)
        self.play(FadeIn(cx4), run_time=0.4)
        # no PALCO, as mᵢ(r⃗ᵢ − R⃗_cm) ponta com ponta fecham: a soma é 0⃗ (mapa linear da tela no ⊕: a cadeia fecha exatamente)
        cu = ValueTracker(0.0)
        self.add(cu)

        def cadeia():
            u = cu.get_value()
            if u < 0.01:
                return VGroup()
            R0 = np.array([1.5, 1.0, 0.0])
            p0 = bd.p(R0)
            Jl = lambda v: (bd.p(R0 + 0.01 * np.asarray(v, float)) - p0) / 0.01
            s0, g = P3(-1.35, 1.75), VGroup()
            pt = s0
            for m, (x, y) in bd.DADOS:
                w = Jl((m * (x - 1.5), m * (y - 1.0), 0.0)) * 0.36
                g.add(seta(pt, pt + w, mix(GEO, 0.35), 5, tip=0.2, op=u))
                pt = pt + w
            g.add(Dot(s0, radius=0.06, color=WHITE_).set_opacity(u))
            return g.set_z_index(12)
        cad = vivo(cadeia)
        self.add(cad)
        self.ate(0.52)
        self.play(cu.animate.set_value(1.0), run_time=1.0)
        self.play(onda(P3(-1.35, 1.75), r=0.16), run_time=0.8)             # fecha no ponto de partida
        # pesos ∝ massa (azul-claro) nas bolas; M g⃗ sai do ⊕ ao lado do pino
        pe = ValueTracker(0.0)
        self.add(pe)

        def pesos():
            o = pe.get_value()
            if o < 0.01:
                return VGroup()
            g = VGroup()
            for c_, r_, m in bd.bolas():
                g.add(seta(c_ + (r_ + 0.03) * DOWN, c_ + (r_ + 0.03 + 0.6 * m) * DOWN, FC, 6, tip=0.22, op=o))
            return g.set_z_index(12)
        pes = vivo(pesos)
        self.add(pes)
        self.ate(0.6)
        self.play(rel.animate.set_value(0.0), cu.animate.set_value(0.0), pe.animate.set_value(1.0), run_time=0.8)
        braco = VGroup(*[DashedLine(bd.p((1.5, 1.0, 0.0)), c_, dash_length=0.08).set_stroke(GEO, 2, opacity=0.6) for c_, _, _ in bd.bolas()])
        self.ate(0.64)
        self.play(Create(braco), run_time=0.8)                             # "as alavancas dos pesos se compensam"
        c0 = bd.p((1.5, 1.0, 0.0)) + 0.15 * RIGHT
        Mg = VGroup(seta(c0 + 0.28 * DOWN, c0 + (0.28 + 0.6 * 4) * DOWN, FC, 8, tip=0.26).set_z_index(13),
                    mtex(r"M\vec g", FC, 40).next_to(c0 + 0.95 * DOWN, RIGHT, buff=0.12).set_z_index(13))          # à direita da seta
        self.ate(0.7)
        self.play(TransformFromCopy(pes.submobjects[0].copy(), Mg), FadeOut(braco), run_time=1.0)            # os pesos se somam no ⊕
        cg = txt("CENTRO DE GRAVIDADE", 32, bold=True)
        na_conta(cg, -2.5)
        self.ate(0.78)
        self.play(FadeIn(cg, shift=0.1 * UP), run_time=0.7)
        self.ate(0.84)
        self.dica_entra(dica("O CENTRO DE MASSA FICA MAIS PERTO", "DE ONDE ESTÁ A MAIOR PARTE DA MASSA"))
        self.ate(0.9)
        self.play(onda(bd.p((1.5, 1.0, 0.0))), run_time=1.0)
        gu = VGroup(txt("SÓ COINCIDEM SE", 28), mtex(r"\vec g", FC, 40), txt("FOR UNIFORME", 28)).arrange(RIGHT, buff=0.14)
        gu.move_to(P3(-3.9, -3.55))
        self.ate(0.92)
        self.play(FadeIn(gu, shift=0.1 * UP), FadeOut(Mg), pe.animate.set_value(0.0), run_time=0.7)   # "só se a gravidade mudasse…" (os pesos já foram)
        self.ate(0.97)

    # ── T1-8: por partes ─────────────────────────────────────────────────────────────────────────────────
    def t1_8(self):
        """Volta o plano do T1-6; as duas massas de 1 kg deslizam pelo segmento tracejado e se fundem numa de 2 kg em (3, 2) (o rótulo
        `2 kg` nasce dos dois `1 kg` por TransformByGlyphMap); o ⊕ já estava no meio do segmento entre as duas de 2 kg (só pisca).
        CONTA: R⃗_cm = (M_I R⃗_I + M_II R⃗_II)/(M_I + M_II) → (2·(0, 0) + 2·(3, 2))/4 → (6, 4)/4 = (1,5; 1,0); o (6, 4) vem da conta do T1-6."""
        self.an("T1-8")
        O, k = O6, K6
        Pw = lambda x, y: O + k * P3(x, y)
        velhos = self.snap()
        self._corpos3d = []                                            # a bandeja do T1-7 saiu
        ax = self.eixos6()
        bolas = [esfera2d(0.32 * m ** (1 / 3)).move_to(Pw(x, y)).set_z_index(6) for m, (x, y) in self.dados]
        kgs = [rot(f"{m:g} kg", 30).next_to(b, UP, buff=0.16) for (m, _), b in zip(self.dados, bolas)]
        kgs[0].next_to(bolas[0], DOWN, buff=0.18).shift(0.55 * LEFT)          # embaixo (o M_I, R⃗_I fica em cima)
        kgs[1].shift(1.0 * LEFT)
        coords = [mtex(rf"({x},\,{y})", GEO, 36) for _, (x, y) in self.dados]
        for c_, b, l_ in zip(coords, bolas, (DOWN, DOWN, RIGHT)):
            c_.next_to(b, l_, buff=0.18)
        coords[0].shift(0.45 * RIGHT)
        cm = marcador_cm(Pw(1.5, 1.0))
        selo = txt("POR PARTES", 30, bold=True)
        selo.move_to(P3(-1.2, 2.55))                                    # à direita do eixo y, acima das massas
        lem, il = eqp(r"\sum_i m_i\vec r_i", "=", r"(6,\,4)", size=46)
        lem.set_opacity(OP_FUNDO)
        tag6 = txt("DO T1-6:", 24, color=DIM)
        VGroup(tag6, lem).arrange(RIGHT, buff=0.25)
        na_conta(VGroup(tag6, lem), 2.8)
        self.troca(velhos, FadeIn(ax), *[FadeIn(b) for b in bolas], *[FadeIn(l_) for l_ in kgs + coords], FadeIn(cm), FadeIn(selo),
                   FadeIn(tag6), FadeIn(lem), seq=True)
        # "qualquer pedaço do sistema": as duas de 1 kg, contornadas, com o segmento tracejado e o ponto médio
        a_, b_ = Pw(4, 0), Pw(2, 4)
        u_ = (b_ - a_) / np.linalg.norm(b_ - a_)
        n_ = P3(-u_[1], u_[0])
        seg1 = DashedLine(a_, b_, dash_length=0.1).set_stroke(GEO, 2.2, opacity=0.8).set_z_index(3)
        mid = Circle(radius=0.1).move_to(Pw(3, 2)).set_stroke(GEO, 2.4)
        self.ate(0.1)
        self.play(onda(a_, r=0.36), onda(b_, r=0.36), Create(seg1), FadeOut(coords[1]), FadeOut(coords[2]), run_time=0.9)   # "qualquer pedaço"
        self.ate(0.2)
        self.play(FadeIn(mid, scale=1.5), run_time=0.5)
        # "as duas de um quilograma viram uma de dois, no ponto médio, em (3, 2)"
        self.ate(0.31)
        b2 = esfera2d(0.32 * 2 ** (1 / 3)).move_to(Pw(3, 2)).set_z_index(6)
        k2 = rot("2 kg", 30).next_to(b2, UP, buff=0.16)
        src = VGroup(*kgs[1].copy(), *kgs[2].copy())
        self.remove(kgs[1], kgs[2])
        self.add(src)
        c32 = mtex(r"(3,\,2)", GEO, 36).next_to(b2, RIGHT, buff=0.2)
        self.play(bolas[1].animate.move_to(Pw(3, 2)), bolas[2].animate.move_to(Pw(3, 2)), FadeOut(seg1), run_time=1.3)
        self.play(FadeIn(b2), FadeOut(bolas[1]), FadeOut(bolas[2]), FadeOut(mid),
                  TransformByGlyphMap(src, k2, ([0, 3], [0]), ([1, 4], [1]), ([2, 5], [2]), mobA_submobject_index=[], mobB_submobject_index=[]),
                  FadeIn(c32), run_time=1.0)
        # "sobram duas massas de dois quilogramas": o segmento entre elas; o ⊕ já estava no meio dele (pisca)
        seg2 = DashedLine(Pw(0, 0), Pw(3, 2), dash_length=0.1).set_stroke(GEO, 2.2, opacity=0.8).set_z_index(3)
        tI = VGroup(mtex(r"M_{\rm I}", WHITE_, 36), mtex(",", WHITE_, 36), mtex(r"\vec R_{\rm I}", GEO, 36)).arrange(RIGHT, buff=0.08, aligned_edge=DOWN)
        tII = VGroup(mtex(r"M_{\rm II}", WHITE_, 36), mtex(",", WHITE_, 36), mtex(r"\vec R_{\rm II}", GEO, 36)).arrange(RIGHT, buff=0.08, aligned_edge=DOWN)
        tI[0].move_to(P3(-6.95, -1.25)); tI[1].next_to(tI[0], RIGHT, buff=0.06, aligned_edge=DOWN)
        tI[2].next_to(tI[0], DOWN, buff=0.12).align_to(tI[0], LEFT)                 # em duas linhas, à esquerda do eixo y
        tII.next_to(b2, DR, buff=0.12).shift(0.15 * RIGHT)
        pm = mtex(r"\frac{(4,\,0)+(2,\,4)}{2}=(3,\,2)", GEO, 46)
        na_conta(pm, 1.45)
        self.ate(0.37)
        self.play(FadeIn(pm, shift=0.1 * DOWN), run_time=0.7)                      # "no ponto médio entre elas, em três e dois"
        self.ate(0.47)
        self.play(FadeOut(pm), run_time=0.4)
        self.ate(0.48)
        self.play(Create(seg2), FadeIn(tI), FadeIn(tII), run_time=0.8)
        self.play(onda(cm.get_center()), Indicate(cm, color=WHITE_, scale_factor=1.25), run_time=0.9)
        # a CONTA, cada símbolo saindo do desenho
        A, ia = eqp(r"\vec R_{cm}", "=", r"\frac{M_{\rm I}\vec R_{\rm I}+M_{\rm II}\vec R_{\rm II}}{M_{\rm I}+M_{\rm II}}", size=48, cores={0: CMC})
        fr = ia[2]                                       # M I R I + M II R II barra M I + M II
        ngl = [ng(r"M_{\rm I}"), ng(r"\vec R_{\rm I}"), ng("+"), ng(r"M_{\rm II}"), ng(r"\vec R_{\rm II}")]
        cur, num = fr[0], []
        for n__ in ngl:
            num.append(list(range(cur, cur + n__)))
            cur += n__
        for j in num[1] + num[4]:
            A[0][j].set_color(GEO)
        A._partes += [(r"\vec R_{\rm I}", GEO), (r"\vec R_{\rm II}", GEO)]
        na_conta(A, 1.45)
        self.ate(0.53)
        dI, dII = num[0], num[3]
        self.play(FadeIn(VGroup(*[A[0][j] for j in ia[0] + ia[1]])),
                  TransformFromCopy(tI[0][0], VGroup(*[A[0][j] for j in dI])), TransformFromCopy(tI[2][0], VGroup(*[A[0][j] for j in num[1]])),
                  TransformFromCopy(tII[0][0], VGroup(*[A[0][j] for j in dII])), TransformFromCopy(tII[2][0], VGroup(*[A[0][j] for j in num[4]])),
                  FadeIn(VGroup(*[A[0][j] for j in num[2]])), FadeIn(VGroup(*[A[0][j] for j in range(cur, len(A[0]))])), run_time=1.3)
        Bq, ib = eqp("=", r"\frac{2\cdot(0,\,0)+2\cdot(3,\,2)}{4}", size=48)
        Bq.move_to(P3(XC0 + 0.55 + Bq.width / 2, 0.15))
        fb = ib[1]                                       # 2 · ( 0 , 0 ) + 2 · ( 3 , 2 ) barra 4
        g_ = lambda *js: VGroup(*[Bq[0][fb[j]] for j in js])
        self.ate(0.6)
        self.play(FadeIn(Bq[0][ib[0][0]]), TransformFromCopy(kgs[0][0], g_(0)), TransformFromCopy(coords[0][0], g_(2, 3, 4, 5, 6)),
                  TransformFromCopy(k2[0], g_(8)), TransformFromCopy(c32[0], g_(10, 11, 12, 13, 14)), FadeIn(g_(1, 7, 9, 15, 16)), run_time=1.3)
        Cq, ic = eqp("=", r"\frac{(6,\,4)}{4}", r"=\ ", r"(1{,}5;\ 1{,}0)", size=48, cores={3: CMC})
        Cq.move_to(P3(XC0 + 0.55 + Cq.width / 2, -1.1))
        fc = ic[1]                                       # ( 6 , 4 ) barra 4
        self.ate(0.66)
        self.play(Indicate(lem, color=WHITE_, scale_factor=1.12), run_time=0.6)
        self.play(FadeIn(Cq[0][ic[0][0]]), TransformFromCopy(lem[0][il[2][0]:il[2][-1] + 1], VGroup(*[Cq[0][j] for j in fc[:5]])),
                  FadeIn(VGroup(*[Cq[0][j] for j in fc[5:]])), run_time=1.0)            # "dá o mesmo": o (6, 4) é o do T1-6
        self.play(FadeIn(VGroup(*[Cq[0][j] for j in ic[2] + ic[3]])), run_time=0.6)
        bx = caixa(VGroup(*[Cq[0][j] for j in ic[3]]), cor=CMC)
        self.play(FadeIn(bx), self.h_pul.animate(rate_func=there_and_back).set_value(1.0) if hasattr(self, "h_pul") else Wait(0.01),
                  Indicate(cm, color=WHITE_, scale_factor=1.2), run_time=0.7)
        # "na razão inversa das massas. Massas iguais, bem no meio."
        meio = Pw(1.5, 1.0)
        u2 = (Pw(3, 2) - Pw(0, 0)) / np.linalg.norm(Pw(3, 2) - Pw(0, 0))
        nn = P3(u2[1], -u2[0])
        dd = VGroup()
        for a0, a1 in ((Pw(0, 0), meio), (meio, Pw(3, 2))):
            ca = a0 + u2 * 0.42 + nn * 0.32
            cb = a1 - u2 * 0.42 + nn * 0.32
            dd.add(Line(ca, cb).set_stroke(GEO, 2.2), Line(ca - nn * 0.08, ca + nn * 0.08).set_stroke(GEO, 2.2),
                   Line(cb - nn * 0.08, cb + nn * 0.08).set_stroke(GEO, 2.2), mtex("d", GEO, 36).move_to((ca + cb) / 2 + nn * 0.6))
        nt = cartao("MASSAS IGUAIS: BEM NO MEIO", "SENÃO, NA RAZÃO INVERSA", "DAS MASSAS")
        na_conta(nt, -2.55)
        self.ate(0.76)
        self.play(FadeIn(dd), run_time=0.8)
        self.ate(0.86)
        self.play(FadeIn(nt), run_time=0.6)
        iguais = VGroup()                                                          # "massas iguais, bem no meio": marcas de segmentos iguais
        for a0, a1 in ((Pw(0, 0), meio), (meio, Pw(3, 2))):
            c_ = (a0 + a1) / 2
            for k_ in (-1, 1):
                iguais.add(Line(c_ + u2 * 0.05 * k_ - nn * 0.13, c_ + u2 * 0.05 * k_ + nn * 0.13).set_stroke(WHITE_, 2.6))
        self.ate(0.9)
        self.play(Create(iguais), onda(meio), run_time=0.8)
        self.ate(0.97)

    def eixos6(self):
        O = O6
        return VGroup(Line(O + 0.3 * LEFT, O + 6.6 * RIGHT).set_stroke(GEO, 1.8, opacity=0.7), Line(O + 0.3 * DOWN, O + 4.85 * UP).set_stroke(GEO, 1.8, opacity=0.7),
                      Triangle().scale(0.07).set_stroke(width=0).set_fill(GEO, 0.7).rotate(-PI / 2).move_to(O + 6.6 * RIGHT),
                      Triangle().scale(0.07).set_stroke(width=0).set_fill(GEO, 0.7).move_to(O + 4.85 * UP),
                      mtex("x", GEO, 36).next_to(O + 6.6 * RIGHT, DOWN, buff=0.14),
                      mtex("y", GEO, 36).next_to(O + 4.85 * UP, LEFT, buff=0.14)).set_z_index(-1)
