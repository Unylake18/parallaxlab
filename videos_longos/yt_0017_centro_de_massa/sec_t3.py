"""Lote P3 (handoff v4, lote 2): T3 — que energia é do movimento relativo?
T3-1 a explosão no espaço de novo (os mesmos cacos, massas e direções do T2-6), vista do chão: velocidades violeta, todas com a parte comum
para a direita · T3-2 a câmera passa a acompanhar o ⊕ (para no centro): a parte comum V⃗_cm sai das velocidades e vai para o canto;
v⃗ᵢ = V⃗_cm + v⃗ᵢ′ · T3-3 momentos relativos (30 N·s cada, da borda dos cacos) ponta com ponta fecham o triângulo; Σ mᵢv⃗ᵢ′ = Σ mᵢv⃗ᵢ − M V⃗_cm
= P⃗ − P⃗ = 0⃗ · T3-4 K = ½ Σ mᵢ(V⃗_cm + v⃗ᵢ′)² abre em três termos; o do meio recebe o 0⃗ e some; K = ½ M V²_cm + K_rel; barras ciano num
painel próprio · T3-5 replay do chão: K do CM parada, K relativa nasce quando as emendas acendem, a energia química (laranja) esvazia ·
T3-6 blocos de aço 2 kg a 6 m/s × 1 kg parado, grudam: 36 = 24 + 12 J; os 12 J saem em laranja · T3-7 cadeado na barra de 24 J; com
gravidade o cadeado abre; DICA."""
from MF_Tools import TransformByGlyphMap

from camadas import *  # noqa: F401,F403


def mp(m, idx, partes):
    return VGroup(*[m[0][j] for k in partes for j in idx[k]])


J = lambda idx, *ks: [j for k in ks for j in idx[k]]

LENTO = 0.35                                                       # T3-2…T3-4: os cacos se afastam devagar (ficam no PALCO)
KCM, KREL = 0.5 * MT * Explosao3D.V0 ** 2, sum(Explosao3D.C ** 2 / (2 * m) for m in MS)   # unidades do modelo (só proporção nas barras)


class LoteT3(Camadas):
    def construct(self):
        self.setup_base(cap="QUE ENERGIA É DO MOVIMENTO RELATIVO?")
        self.t3_1()
        self.t3_2()
        self.t3_3()
        self.t3_4()
        self.t3_5()
        self.t3_6()
        self.t3_7()
        self.fim()
        self.relatorio()
        self.gravar_reg()

    # ── T3-1: visto do chão, velocidades ──────────────────────────────────────────────────────────────────
    def t3_1(self):
        self.an("T3-1")
        e = self.e = Explosao3D(self, K=1.5, camx=-1.6, xc=PALCO_C[0], yc=-0.4, op=0.0)
        e.dolly = (1.5, 1.15, -1.6, 0.6, 4.8)
        self.add(e.tau, e.K, e.camx, e.xc, e.yc, e.seg, e.f3d)
        cam, ref = self._explosao_camadas(e)
        self._corpos3d = [lambda: [(c_, r_) for c_, r_, _ in e.corpos()] if e.f3d in self.mobjects and e.f3d.op.get_value() > 0.15 else []]
        selo = self.selo_esp = txt("NO ESPAÇO, SEM GRAVIDADE", 24, color=DIM, op=0.95)
        for k_, m_ in self._refs.items():                      # no T3 os selos vão para o rodapé do PALCO: no topo, as setas do caco de 2 kg passam
            m_.move_to(P3(PALCO_C[0], -3.0))
        selo.move_to(P3(PALCO_C[0], -3.38))
        T = self.ex
        T["op_p"].set_value(0.0)
        T["op_vel"].set_value(1.0)
        self.add(cam)
        self.play(e.f3d.op.animate.set_value(1.0), FadeIn(ref), FadeIn(selo), e.tau.animate(rate_func=linear).set_value(0.5), run_time=0.8)
        self.play(e.tau.animate(rate_func=linear).set_value(e.TE), run_time=(e.TE - 0.5) / 0.6)
        self.play(e.tau.animate(rate_func=linear).set_value(2.4), run_time=2.4)
        # "todas elas carregam um pedaço comum: o conjunto inteiro está andando para a direita" → V⃗_cm no ⊕ (a parte comum)
        self.ate(0.62)
        T["w"].set_value(1e-4)
        self.play(onda(e.cm()), e.tau.animate(rate_func=linear).set_value(2.7), run_time=0.8)
        self.ate_mov(0.97, e.tau, 2.9)

    # ── T3-2: a câmera passa a acompanhar o ⊕; v⃗ᵢ = V⃗_cm + v⃗ᵢ′ ──────────────────────────────────────────────
    def t3_2(self):
        e, T = self.e, self.ex
        self.an("T3-2")
        tau = e.tau.get_value()
        K0, K1, c0, c1, Td = e.dolly
        u = suave(tau / Td)
        e.K.set_value(K0 + (K1 - K0) * u)
        e.camx.set_value(c0 + (c1 - c0) * u)
        e.dolly = None
        self.play(e.seg.animate.set_value(1.0), T["w"].animate.set_value(1.0), e.tau.animate(rate_func=linear).set_value(tau + LENTO * 0.35), run_time=2.2)
        self.troca_ref("VISTO DO CENTRO DE MASSA")
        E, ie = eqp(r"\vec v_i", "=", r"\vec V_{cm}", "+", r"\vec v_i'", size=56, cores={0: VEL, 2: VEL, 4: VREL})
        na_conta(E, 1.6)
        vlab = mtex(r"\vec V_{cm}", VEL, 36).move_to(P3(-1.6 + 0.55, 2.45 + 0.32))          # o rótulo do canto (camada)
        c1kg = e.corpos()[1][0]
        vr = mtex(r"\vec v_i'", VREL, 40).move_to(c1kg + P3(-0.95, -1.1))
        self.ate(0.45)
        self.play(FadeIn(vr), e.tau.animate(rate_func=linear).set_value(tau + LENTO * 0.45), run_time=0.5)
        self.play(FadeIn(mp(E, ie, [0, 1, 3])), TransformFromCopy(vlab, mp(E, ie, [2])), TransformFromCopy(vr, mp(E, ie, [4])),
                  e.tau.animate(rate_func=linear).set_value(tau + LENTO * 0.6), run_time=1.3)
        self.play(FadeOut(vr), e.tau.animate(rate_func=linear).set_value(tau + LENTO * 0.65), run_time=0.4)
        self.E32 = E, ie
        self.ate_mov(0.97, e.tau, tau + LENTO * 0.9)

    # ── T3-3: momentos relativos fecham o triângulo; Σ mᵢv⃗ᵢ′ = 0⃗ ───────────────────────────────────────────
    def t3_3(self):
        e, T = self.e, self.ex
        self.an("T3-3")
        tau = e.tau.get_value()
        E, ie = self.E32
        self.play(T["op_vel"].animate.set_value(0.0), T["op_rel"].animate.set_value(1.0), E.animate.set_opacity(0.4).move_to(P3(E.get_center()[0], 2.65)),
                  e.tau.animate(rate_func=linear).set_value(tau + LENTO * 0.08), run_time=1.0)
        self.ate(0.1)
        self.play(onda(e.cm(), r=0.3), e.tau.animate(rate_func=linear).set_value(tau + LENTO * 0.16), run_time=1.0)   # "se afastam de um ponto parado"
        self.ate(0.2)
        self.play(T["op_30"].animate.set_value(1.0), e.tau.animate(rate_func=linear).set_value(tau + LENTO * 0.24), run_time=0.8)   # "o mesmo tamanho"
        self.ate(0.36)
        self.play(T["op_30"].animate.set_value(0.0), T["u_tri"].animate.set_value(1.0), e.tau.animate(rate_func=linear).set_value(tau + LENTO * 0.4), run_time=1.6)
        self.ate(0.48)
        self.play(onda(e.corpos()[1][0], r=0.5), e.tau.animate(rate_func=linear).set_value(tau + LENTO * 0.48), run_time=0.9)   # o mais leve, mais rápido
        # a conta
        A, ia = eqp(r"\sum_i", r"m_i\vec v_i'", size=52, cores={1: VREL})
        B, ib = eqp("=", r"\sum_i", r"m_i\vec v_i", "-", "M", r"\vec V_{cm}", size=52, cores={2: MAG, 5: VEL})
        C, ic = eqp("=", r"\vec P", "-", r"\vec P", size=52, cores={1: MAG, 3: MAG})
        D, id_ = eqp("=", r"\vec 0", size=52)
        na_conta(A, 1.75)
        for M_, y_ in ((B, 0.5), (C, -0.6), (D, -1.5)):
            M_.move_to(P3(XC0 + 0.55 + M_.width / 2, y_))
        self.ate(0.56)
        self.play(FadeIn(A), e.tau.animate(rate_func=linear).set_value(tau + LENTO * 0.52), run_time=0.8)
        self.ate(0.62)
        self.play(TransformByGlyphMap(A.copy(), B, ([], J(ib, 0)), (J(ia, 0), J(ib, 1)), (J(ia, 1), J(ib, 2)), ([], J(ib, 3, 4, 5)), auto_fade=True),
                  e.tau.animate(rate_func=linear).set_value(tau + LENTO * 0.58), run_time=1.3)
        self.ate(0.72)
        self.play(TransformByGlyphMap(B.copy(), C, (J(ib, 0), J(ic, 0)), (J(ib, 1, 2), J(ic, 1)), (J(ib, 3), J(ic, 2)), (J(ib, 4, 5), J(ic, 3))),
                  e.tau.animate(rate_func=linear).set_value(tau + LENTO * 0.64), run_time=1.3)
        rs = VGroup(risco(mp(C, ic, [1]), WHITE_, 3), risco(mp(C, ic, [3]), WHITE_, 3))
        self.ate(0.8)
        self.play(Create(rs), e.tau.animate(rate_func=linear).set_value(tau + LENTO * 0.68), run_time=0.6)
        self.play(TransformByGlyphMap(C.copy(), D, (J(ic, 0), J(id_, 0)), (J(ic, 1, 2, 3), J(id_, 1))), FadeOut(rs),
                  e.tau.animate(rate_func=linear).set_value(tau + LENTO * 0.74), run_time=1.0)
        bx = caixa(D, cor=MAG)
        self.ate(0.88)
        self.play(FadeIn(bx), e.tau.animate(rate_func=linear).set_value(tau + LENTO * 0.78), run_time=0.5)
        self.ate_mov(0.97, e.tau, tau + LENTO * 0.85)
        self.c33 = VGroup(A, B, C, bx)
        self.zero, self.zero_i = D, id_

    # ── T3-4: K = ½ M V²_cm + K_rel; barras ─────────────────────────────────────────────────────────────────
    def barras(self, c0):
        """Painel próprio das barras: K do CM e K relativa (ciano) e, no T3-5, o reservatório de energia química (laranja). Fica no PALCO
        no T3-4 (o 3D sai) e vai para a CONTA no T3-5 (o 3D volta). Alturas ∝ energias do modelo."""
        self.kb = dict(cm=ValueTracker(0.0), rel=ValueTracker(0.0), qui=ValueTracker(0.0), opq=ValueTracker(0.0))
        self.add(*self.kb.values())
        H0, DX = 1.75, 1.3
        esc = H0 / max(KCM, KREL)
        self.kb_ref = Dot(c0, radius=0.01).set_opacity(0.0)               # o centro do painel (as barras vivas seguem)
        base = lambda: self.kb_ref.get_center() + P3(-DX, -0.75)
        fundo = RoundedRectangle(corner_radius=0.12, width=4.0, height=3.3).move_to(c0).set_fill(PANEL, 0.85).set_stroke(BLUE_L, 2)
        fundo._fundo = True
        b0 = base()
        labs = VGroup(*[VGroup(mtex("K", KC, 36), txt(t_, 24)).arrange(DOWN, buff=0.06).move_to(b0 + P3(DX * k, -0.5)) for k, t_ in enumerate(("DO CM", "REL."))])
        self.kb_dq = P3(2 * DX, -0.5)

        def bars():
            g, b_ = VGroup(), base()
            for k, (chave, cor, val) in enumerate((("cm", KC, KCM), ("rel", mix(KC, 0.25), KREL))):
                h = max(0.001, self.kb[chave].get_value() * val * esc)
                g.add(Rectangle(width=0.6, height=h).set_stroke(width=0).set_fill(cor, 1).move_to(b_ + P3(DX * k, h / 2)))
            oq = self.kb["opq"].get_value()
            if oq > 0.01:
                hq = max(0.001, self.kb["qui"].get_value() * KREL * esc)
                g.add(Rectangle(width=0.6, height=KREL * esc).set_stroke(HEAT, 2, opacity=0.6 * oq).set_fill(opacity=0).move_to(b_ + P3(2 * DX, KREL * esc / 2)),
                      Rectangle(width=0.6, height=hq).set_stroke(width=0).set_fill(escuro(HEAT, 0.25), oq).move_to(b_ + P3(2 * DX, hq / 2)))
            g.add(Line(b_ + P3(-0.45, 0), b_ + P3(2 * DX + 0.45, 0)).set_stroke(GEO, 2))
            return g.set_z_index(20)
        self.kbar = vivo(bars)
        return VGroup(fundo, labs, self.kb_ref)

    def t3_4(self):
        e, T = self.e, self.ex
        self.an("T3-4")
        tau = e.tau.get_value()
        self.play(FadeOut(self.c33), self.zero.animate.set_opacity(0.45).move_to(P3(6.75, 3.05)), self.E32[0].animate.set_opacity(0.0),
                  e.tau.animate(rate_func=linear).set_value(tau + LENTO * 0.04), run_time=0.7)
        self.remove(self.E32[0])
        K1, i1 = eqp("K", "=", r"\tfrac{1}{2}", r"\sum_i", "m_i", r"\big(", r"\vec V_{cm}", "+", r"\vec v_i'", r"\big)^2", size=50,
                     cores={0: KC, 6: VEL, 8: VREL})
        na_conta(K1, 2.2)
        self.ate(0.04)
        self.play(FadeIn(K1), e.tau.animate(rate_func=linear).set_value(tau + LENTO * 0.1), run_time=0.9)
        K2, i2 = eqp("=", r"\tfrac{1}{2}", "M", r"V_{cm}^2", "+", r"\vec V_{cm}", r"\cdot", r"\sum_i m_i\vec v_i'", size=46, cores={3: VEL, 5: VEL})
        K2b, i2b = eqp("+", r"\tfrac{1}{2}", r"\sum_i m_i v_i'^2", size=46)
        na_conta(K2, 1.05, x0=XC0 + 0.3)
        na_conta(K2b, 0.0, x0=XC0 + 0.3)
        self.ate(0.12)
        self.play(TransformByGlyphMap(K1.copy(), K2, (J(i1, 1), J(i2, 0)), (J(i1, 2), J(i2, 1)), (J(i1, 6), J(i2, 3)), (J(i1, 0, 3, 4, 5, 7, 8, 9), []),
                                      ([], J(i2, 2, 4, 5, 6, 7)), auto_fade=True), FadeIn(K2b, shift=0.1 * DOWN),
                  e.tau.animate(rate_func=linear).set_value(tau + LENTO * 0.18), run_time=1.6)
        # o termo do meio: recebe o 0⃗ do T3-3 e apaga
        meio = mp(K2, i2, [5, 6, 7])
        self.ate(0.22)
        self.play(meio.animate.set_color(MAG), e.tau.animate(rate_func=linear).set_value(tau + LENTO * 0.22), run_time=0.5)
        z0 = mp(self.zero, self.zero_i, [1])
        self.play(TransformFromCopy(z0, mp(K2, i2, [7])), e.tau.animate(rate_func=linear).set_value(tau + LENTO * 0.28), run_time=0.9)
        K3, i3 = eqp("K", "=", r"\tfrac{1}{2}", "M", r"V_{cm}^2", "+", r"\tfrac{1}{2}", r"\sum_i m_i v_i'^2", size=50, cores={0: KC, 4: VEL})
        na_conta(K3, -1.2, x0=1.3)
        self.ate(0.3)
        self.play(FadeIn(mp(K3, i3, [0])), TransformFromCopy(mp(K2, i2, [0, 1, 2, 3]), mp(K3, i3, [1, 2, 3, 4])),
                  TransformFromCopy(mp(K2b, i2b, [0, 1, 2]), mp(K3, i3, [5, 6, 7])), mp(K2, i2, [4, 5, 6, 7]).animate.set_opacity(0.25),
                  e.tau.animate(rate_func=linear).set_value(tau + LENTO * 0.34), run_time=1.4)          # o termo do meio fica para trás
        K4, i4 = eqp("K", "=", r"\tfrac{1}{2}", "M", r"V_{cm}^2", "+", r"K_{rel}", size=56, cores={0: KC, 4: VEL, 6: KC})
        na_conta(K4, -2.45, x0=XC0 + 0.2)
        bx = caixa(K4, cor=KC)
        defi, idf = eqp(r"K_{rel}", "=", r"\tfrac{1}{2}", r"\sum_i", "m_i", r"\left|\vec v_i-\vec V_{cm}\right|^2", size=46, cores={0: KC})
        na_conta(defi, 1.6, x0=XC0 + 0.2)
        self.ate(0.42)
        self.play(TransformByGlyphMap(K3.copy(), K4, *[(J(i3, k), J(i4, k)) for k in range(6)], (J(i3, 6, 7), J(i4, 6))), FadeIn(bx),
                  e.tau.animate(rate_func=linear).set_value(tau + LENTO * 0.4), run_time=1.3)
        quadro = self.quadro = self.barras(P3(PALCO_C[0], 0.1))
        self.ate(0.5)
        self.play(e.f3d.op.animate.set_value(0.0), FadeOut(self.selo_esp), *[FadeOut(m_) for m_ in self._refs.values() if m_ in self.mobjects],
                  run_time=0.5)                                                                     # os cacos saem; o PALCO vira o painel das energias
        self.play(FadeIn(quadro), FadeIn(self.kbar), self.kb["cm"].animate.set_value(1.0), run_time=1.0)
        self.ate(0.6)
        self.play(self.kb["rel"].animate.set_value(1.0), run_time=1.0)
        self.ate(0.66)
        self.play(FadeOut(VGroup(K1, K2, K2b)), FadeIn(defi, shift=0.1 * DOWN), run_time=0.8)
        nota = cartao("TUDO ENERGIA DE MOVIMENTO:", "NÃO É A ENERGIA INTERNA", "DA TERMODINÂMICA", size=26)
        nota.move_to(P3(PALCO_C[0], -2.75))
        self.ate(0.74)
        self.play(FadeIn(nota), K3.animate.set_opacity(0.4), run_time=0.8)
        self.ate(0.97)
        self.c34 = VGroup(K3, defi, nota, self.zero)
        self.K4, self.bx4 = K4, bx

    # ── T3-5: replay do chão: K do CM parada, K relativa nasce da energia química ─────────────────────────────
    def t3_5(self):
        e, T = self.e, self.ex
        self.an("T3-5")
        self.play(FadeOut(self.c34), VGroup(self.K4, self.bx4).animate.move_to(P3(CONTA_C[0], 2.3)), self.quadro.animate.move_to(P3(CONTA_C[0], 0.0)),
                  T["op_rel"].animate.set_value(0.0), T["w"].animate.set_value(0.0), run_time=0.8)
        self.lab_q = txt("QUÍMICA", 24, color=HEAT).move_to(self.kb_ref.get_center() + P3(-1.3, -0.75) + self.kb_dq)
        e.seg.set_value(0.0)
        e.dolly = (1.5, 1.15, -1.6, 0.6, 4.8)
        e.tau.set_value(0.0)
        T["u_tri"].set_value(0.0)
        self.kb["rel"].set_value(0.0)
        self.kb["qui"].set_value(1.0)
        self.add(self.lab_q)
        self.play(e.f3d.op.animate.set_value(1.0), self.kb["opq"].animate.set_value(1.0), FadeIn(self.lab_q), FadeIn(self.selo_esp), run_time=0.6)
        self.troca_ref("VISTO DO CHÃO", rt=0.4)
        seta_q = VGroup(txt("ENERGIA QUÍMICA", 26, color=HEAT), MathTex(r"\rightarrow", font_size=40, color=WHITE_),
                        VGroup(mtex("K", KC, 36), txt("RELATIVA", 26)).arrange(RIGHT, buff=0.12)).arrange(RIGHT, buff=0.16)
        na_conta(seta_q, -2.1)
        self.play(e.tau.animate(rate_func=linear).set_value(e.TE - 0.45), run_time=(e.TE - 0.45) / 0.45)
        self.play(e.tau.animate(rate_func=linear).set_value(e.TE + 0.3), self.kb["rel"].animate(rate_func=linear).set_value(1.0),
                  self.kb["qui"].animate(rate_func=linear).set_value(0.0), FadeIn(seta_q), run_time=2.2)    # as emendas acendem: a química vira relativa
        cmp_ = VGroup(txt("A ENERGIA DO CENTRO DE MASSA", 26), txt("NÃO MUDA: A EXPLOSÃO É INTERNA", 26)).arrange(DOWN, buff=0.1)
        na_conta(cmp_, -3.05)
        self.ate(0.6)
        self.play(FadeIn(cmp_), Indicate(self.K4[0][:5], color=WHITE_, scale_factor=1.1), e.tau.animate(rate_func=linear).set_value(e.TE + 1.0), run_time=1.0)
        self.ate_mov(0.97, e.tau, e.TE + 2.6)
        self.c35 = VGroup(seta_q, cmp_)

    # ── T3-6: colisão de blocos; 36 = 24 + 12 J ─────────────────────────────────────────────────────────────
    def t3_6(self):
        self.an("T3-6")
        e = self.e
        self.kbar.clear_updaters()
        velhos = self.snap()
        Y, S, XC = -2.35, 0.16, -3.35                                  # trilho, tela por metro, ponto do contato
        W1, H1, W2, H2 = 1.1, 0.9, 0.85, 0.7
        tt = self.b_t = ValueTracker(-3.1)
        self.add(tt)

        def xs(t):
            if t < 0:
                return XC - W1 / 2 + 6 * t * S, XC + W2 / 2
            return XC - W1 / 2 + 4 * t * S, XC + W2 / 2 + 4 * t * S
        b1, b2 = bloco_aco(W1, H1), bloco_aco(W2, H2)
        k1, k2 = rot("2 kg", 30), rot("1 kg", 30)

        def blocos():
            t = tt.get_value()
            x1, x2 = xs(t)
            g = VGroup(Line(P3(-7.3, Y), P3(0.6, Y)).set_stroke(GEO, 2.4, opacity=0.6))
            g.add(b1.copy().move_to(P3(x1, Y + H1 / 2)), b2.copy().move_to(P3(x2, Y + H2 / 2)))
            g.add(k1.copy().move_to(P3(x1, Y - 0.32)), k2.copy().move_to(P3(x2, Y - 0.32)))                 # embaixo do trilho
            if t < 0:
                a = P3(x1 - W1 / 2, Y + H1 + 0.32)
                g.add(seta(a, a + RIGHT * 6 * 0.15, VEL, 6, tip=0.22), mrot("6 m/s", 28, VEL).next_to(a + RIGHT * 0.45, UP, buff=0.22))
            else:
                a = P3(x1 - W1 / 2, Y + H1 + 0.32)
                g.add(seta(a, a + RIGHT * 4 * 0.15, VEL, 6, tip=0.22), mrot("4 m/s", 28, VEL).next_to(a + RIGHT * 0.3, UP, buff=0.22))
            xc_ = (2 * x1 + 1 * x2) / 3
            g.add(marcador_cm(P3(xc_, Y + 0.45), r=0.17))
            self.reg("blocos", cm=P3(xc_, Y + 0.45), media=P3((2 * x1 + x2) / 3, Y + 0.45))
            return g
        bv = vivo(blocos)
        self.troca(velhos, FadeIn(bv), seq=True)
        self.play(tt.animate(rate_func=linear).set_value(0.0), run_time=3.1 * 0.9)
        self.play(Flash(P3(XC, Y + 0.4), color=WHITE_, line_length=0.2, flash_radius=0.12, num_lines=10), run_time=0.35)
        self.play(tt.animate(rate_func=linear).set_value(1.2), run_time=1.2)
        # barras empilhadas (ANTES / DEPOIS), em joules
        SB, X0 = 0.14, -6.85
        def barra(y, partes, rot_=True):
            g, x = VGroup(), X0
            for val, cor, op in partes:
                r = Rectangle(width=val * SB, height=0.5).set_stroke(width=0).set_fill(cor, op).move_to(P3(x + val * SB / 2, y))
                r._fundo = True                                                # a barra é o fundo do próprio rótulo
                g.add(r)
                x += val * SB
            return g
        yA, yD = 1.75, 0.55
        tA = txt("ANTES", 26).move_to(P3(X0 + 0.55, yA + 0.5))
        bA = barra(yA, [(36, KC, 1.0)])
        lA = rot("36 J", 30, BACKGROUND_COLOR).move_to(bA)
        # a conta, cada número saindo do desenho
        G1, g1 = eqp("K", "=", r"\tfrac{1}{2}\cdot 2\cdot 6^2", "=", r"36\ \mathrm{J}", size=46, cores={0: KC})
        G2, g2 = eqp(r"V_{cm}", "=", r"\frac{2\cdot 6}{3}", "=", r"4\ \mathrm{m/s}", size=46, cores={0: VEL})
        G3, g3 = eqp(r"\tfrac{1}{2}", "M", r"V_{cm}^2", "=", r"\tfrac{1}{2}\cdot 3\cdot 4^2", "=", r"24\ \mathrm{J}", size=46, cores={2: VEL})
        G4, g4 = eqp(r"K_{rel}", "=", "36", "-", "24", "=", r"12\ \mathrm{J}", size=46, cores={0: KC})
        for M_, y_ in ((G1, 2.3), (G2, 1.15), (G3, 0.0), (G4, -1.15)):
            na_conta(M_, y_)
        self.play(tt.animate(rate_func=linear).set_value(-3.1), FadeIn(tA), run_time=0.6)          # volta ao ANTES
        self.ate(0.2)
        self.play(FadeIn(G1), FadeIn(bA), FadeIn(lA), tt.animate(rate_func=linear).set_value(-2.5), run_time=0.9)
        self.ate(0.27)
        self.play(FadeIn(G2), tt.animate(rate_func=linear).set_value(-2.1), run_time=0.9)
        self.ate(0.33)
        self.play(FadeIn(G3), tt.animate(rate_func=linear).set_value(-1.7), run_time=0.9)
        bA2 = barra(yA, [(24, KC, 1.0), (12, mix(KC, 0.35), 1.0)])
        lA2 = VGroup(rot("24 J", 30, BACKGROUND_COLOR).move_to(bA2[0]), rot("12 J", 30, BACKGROUND_COLOR).move_to(bA2[1]))
        sub = VGroup(txt("CENTRO DE MASSA", 24).next_to(bA2[0], DOWN, buff=0.12), txt("RELATIVA", 24).next_to(bA2[1], DOWN, buff=0.12))
        self.ate(0.4)
        self.play(FadeIn(G4), TransformFromCopy(mp(G3, g3, [6]), lA2[0]), ReplacementTransform(bA, bA2), FadeOut(lA), FadeIn(lA2[1]), FadeIn(sub),
                  tt.animate(rate_func=linear).set_value(-1.3), run_time=1.1)
        # "Depois do choque, os blocos andam juntos, e sobram exatamente vinte e quatro"
        self.ate_mov(0.53, tt, 0.0)
        self.play(Flash(P3(XC, Y + 0.4), color=WHITE_, line_length=0.2, flash_radius=0.12, num_lines=10), run_time=0.35)
        tD = txt("DEPOIS", 26).move_to(P3(X0 + 0.65, yD - 0.5 - 0.3))
        bD = barra(yD, [(24, KC, 1.0), (12, mix(KC, 0.35), 1.0)])
        lD = VGroup(rot("24 J", 30, BACKGROUND_COLOR).move_to(bD[0]), rot("12 J", 30, BACKGROUND_COLOR).move_to(bD[1]))
        self.play(FadeIn(tD), FadeIn(bD), FadeIn(lD), tt.animate(rate_func=linear).set_value(0.6), run_time=0.8)
        # os 12 J saem em laranja para DEFORMAÇÃO · AQUECIMENTO · SOM
        dest = VGroup(*[txt(s_, 26, color=HEAT) for s_ in ("DEFORMAÇÃO", "AQUECIMENTO", "SOM")]).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        dest.move_to(P3(-0.75, -0.6))
        laranja = bD[1].copy().set_fill(HEAT, 1)
        self.ate(0.66)
        self.play(Transform(bD[1], laranja), FadeOut(lD[1]), tt.animate(rate_func=linear).set_value(1.2), run_time=0.7)
        self.play(bD[1].animate.move_to(dest.get_center()).scale(0.2).set_opacity(0.0), FadeIn(dest, shift=0.2 * RIGHT),
                  tt.animate(rate_func=linear).set_value(2.0), run_time=1.3)
        self.ate(0.88)
        self.play(Indicate(G4, color=WHITE_, scale_factor=1.08), tt.animate(rate_func=linear).set_value(2.4), run_time=0.9)   # "consumiu toda a energia relativa"
        self.ate(0.97)
        self.c36 = VGroup(G1, G2, G3, G4, dest, tA, bA2, lA2, sub, tD)
        self.bD, self.lD, self.bv = bD, lD, bv

    # ── T3-7: cadeado ───────────────────────────────────────────────────────────────────────────────────────
    def t3_7(self):
        self.an("T3-7")
        bD, lD = self.bD, self.lD
        cad = cadeado(s=0.95).move_to(bD[0].get_left() + P3(0.45, 0.08))               # na barra de 24 J
        sem = txt("SEM FORÇA EXTERNA", 28, bold=True).next_to(bD[0], RIGHT, buff=0.3)
        self.play(FadeOut(VGroup(*self.c36[:4])), run_time=0.5)
        self.ate(0.04)
        self.play(Indicate(bD[0], color=WHITE_, scale_factor=1.05), run_time=0.7)
        self.play(FadeIn(cad, shift=0.2 * DOWN), FadeIn(sem), run_time=0.8)
        f1 = VGroup(txt("SEM FORÇA EXTERNA,", 28), txt("UMA COLISÃO NUNCA PERDE", 28),
                    VGroup(txt("MAIS QUE A", 28), mtex("K", KC, 40), txt("RELATIVA", 28)).arrange(RIGHT, buff=0.12)) \
            .arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        na_conta(f1, 1.7)
        self.ate(0.12)
        self.play(FadeIn(f1), run_time=0.8)
        # "Na granada, a gravidade é externa e faz trabalho": miniatura da granada com o peso; o cadeado abre
        gx = P3(4.4, -0.2)
        gran = VGroup(Ellipse(width=0.62, height=0.78).set_fill(["#9AA6B8", "#3A4252"], 1).set_sheen_direction(UP).set_stroke("#7FB2FF", 2, opacity=0.6))
        gran[0]._degrade = "aco"
        for k in (-1, 0, 1):
            gran.add(Line(gx + P3(-0.28, 0.2 * k), gx + P3(0.28, 0.2 * k)).set_stroke("#2A303A", 2).shift(-gx))
        gran.add(RoundedRectangle(corner_radius=0.03, width=0.22, height=0.12).set_fill("#9AA6B8", 1).set_stroke(width=0).move_to(P3(0, 0.44)))
        gran.move_to(gx)
        peso = VGroup(seta(gx + 0.42 * DOWN, gx + 1.2 * DOWN, FC, 7, tip=0.24), mtex(r"M\vec g", FC, 40).next_to(gx + 0.75 * DOWN, RIGHT, buff=0.28))
        cad2 = cadeado(aberto=True, s=1.0).move_to(gx + P3(-1.4, -0.3))
        cg = VGroup(txt("COM GRAVIDADE,", 28), txt("O CADEADO ABRE", 28)).arrange(DOWN, buff=0.1).move_to(P3(CONTA_C[0], -2.0))
        self.ate(0.6)
        self.play(FadeIn(gran), FadeIn(peso), run_time=0.8)
        self.ate(0.72)
        self.play(FadeIn(cad2, shift=0.1 * UP), FadeIn(cg), run_time=0.8)
        self.ate(0.82)
        self.dica_entra(dica("NUMA COLISÃO, SÓ A ENERGIA", "RELATIVA PODE SE PERDER"))
        self.ate(0.97)
        self.bv.clear_updaters()
