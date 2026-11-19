"""Lote PT1: T1 — QUANTA ENERGIA TEM UM GIRO? O disco de referência (aço) em 4 anéis × 10 setores rosa (opacidade ∝ massa) gira devagar;
o pedaço i (anel de fora) tem mᵢ, rᵢ (raio quadrático médio do setor) e vᵢ = ωrᵢ; setas violeta em quatro pedaços de um mesmo raio crescem com r.
T1-2/T1-3: ½mᵢvᵢ² → ½mᵢrᵢ²ω² → K = ½(Σmᵢrᵢ²)ω² (ω² atravessa a soma); a energia dos anéis soma numa barra ciano. T1-4: I e a tradução
m ↔ I, v ↔ ω. T1-5: vista oblíqua com um pedaço fora do plano (r_⊥ ao eixo × r⃗ da origem) e um pedaço no próprio eixo (não contribui)."""
from pecas21 import *  # noqa: F401,F403

C1, R1 = P3(-3.75, -0.45), 2.2
W1 = 0.28                                            # rad/s na tela (≈ 1° por quadro)
NR, NT = 4, 10
KSEL = 3 * NT + 1                                    # pedaço i: anel de fora


class LoteT1(Lote21):
    def corpo(self):
        self.an("T1-1")
        self.secao("QUANTA ENERGIA TEM UM GIRO?")
        self.guia(['PERGUNTA:', 'QUANTA ENERGIA TEM', 'O DISCO INTEIRO?'])                                      # v6 G4: a coluna da direita não fica vazia
        ang = ValueTracker(0.0)                      # giro do disco (rad); gira = 1 → W1 rad/s; os rótulos só se prendem com o disco estacionado
        gira = ValueTracker(1.0)
        ang.add_updater(lambda m, dt: m.increment_value(W1 * gira.get_value() * dt))
        fi = lambda: ang.get_value()
        ref = DiscoPedacos(C1, R1, NR, NT)
        dados = ref.dados
        realce = ValueTracker(0.0)
        setas_on = ValueTracker(0.0)
        self.add(ang, gira, realce, setas_on)
        PARK = 0.35                                  # o pedaço i estaciona à direita (rótulos fora do disco, longe do rótulo de energia)

        def pos(k, extra=0.0, r=None):
            d = dados[k]
            a = d["a"] + fi() + extra
            rr = d["r"] if r is None else r
            return C1 + rr * np.array([math.cos(a), math.sin(a), 0])

        RAIO_SETAS = [k * NT + 1 for k in range(NR)]           # um pedaço por anel, no mesmo raio do pedaço i

        def disco():
            g = DiscoPedacos(C1, R1, NR, NT)
            g.rotate(fi(), about_point=C1)
            o = realce.get_value()
            if o > 0.01:
                g.pec[KSEL].set_fill(mix(MAS, 0.25), 0.5 + 0.45 * o).set_stroke(WHITE_, 3, opacity=o)
            s_ = setas_on.get_value()
            if s_ > 0.01:
                for k in RAIO_SETAS:
                    p = pos(k)
                    a = dados[k]["a"] + fi()
                    tg = np.array([-math.sin(a), math.cos(a), 0])
                    g.add(seta(p, p + tg * 0.62 * dados[k]["r"] * min(1.0, s_), VEL, 6, tip=0.2, z=12))
            g.add(eixo_cruz(C1, 0.17))
            return g
        dv = vivo(disco)
        self.play(FadeIn(dv), run_time=0.6)
        aw = seta_curva(C1, R1 + 0.38, 1.95, 0.8, VEL, 6)
        lw = T(r"\omega", 44).next_to(C1 + (R1 + 0.38) * np.array([math.cos(2.4), math.sin(2.4), 0]), UL, buff=0.3)
        self.play(FadeIn(aw), FadeIn(lw), run_time=0.5)
        self.hip("CORPO RÍGIDO · EIXO FIXO")
        # rótulos do pedaço i (presos ao pedaço que gira; texto sempre na horizontal, fora do disco)
        rlin = ValueTracker(0.0)
        self.add(rlin)
        lin = always_redraw(lambda: DashedLine(C1, pos(KSEL), dash_length=0.08).set_stroke(GEO, 3, opacity=rlin.get_value()).set_z_index(13)
                            if rlin.get_value() > 0.01 else VMobject())
        ext = always_redraw(lambda: DashedLine(pos(KSEL, r=R1 + 0.02), pos(KSEL, r=R1 + 0.32), dash_length=0.05).set_stroke(GEO, 2, opacity=0.7 * rlin.get_value())
                            if rlin.get_value() > 0.01 else VMobject())
        lm = T("m_i", 42)
        lr = T("r_i", 42)
        lv = T("v_i", 42)
        fora = lambda m, da, rr: m.move_to(pos(KSEL, da, rr) + 0 * UP)
        lm.add_updater(lambda m: fora(m, -0.2, R1 + 0.42))
        lr.add_updater(lambda m: fora(m, 0.0, R1 + 0.46))
        lv.add_updater(lambda m: fora(m, 0.32, R1 + 0.5))
        self.gat("vamos cortar o disco em pedacinhos")
        self.play(self.ind_copia(dv, WHITE_, 1.02, 0.8), run_time=0.8)
        self.gat("o pedaço número i")
        gira.set_value(0.0)
        alvo = ang.get_value() + ((PARK - dados[KSEL]["a"] - ang.get_value()) % (2 * PI))
        self.play(ang.animate(rate_func=rate_functions.ease_out_sine).set_value(alvo), realce.animate.set_value(1.0), run_time=1.6)
        self.play(FadeIn(lm), run_time=0.4)
        self.gat("está a uma distância r i do eixo")
        self.add(lin, ext)
        self.play(rlin.animate.set_value(1.0), FadeIn(lr), run_time=0.7)
        self.gat("todos os pedaços têm a mesma velocidade angular")
        self.play(self.ind_copia(aw, WHITE_, 1.1, 0.8), self.ind_copia(lw, VEL, 1.2, 0.8), run_time=0.8)
        self.gat("mas a velocidade de cada um depende")
        self.play(setas_on.animate.set_value(1.0), run_time=1.2)
        self.play(FadeIn(lv), run_time=0.4)
        A, ia = M("v_i", "=", r"\omega", "r_i", size=52)
        self.pilha.poe(A)
        self.gat("v i é a velocidade angular vezes r i")
        self.sem_selo()
        self.monta(A, ia, {0: lv, 2: lw, 3: lr})
        soma = sum(0.5 * d["m"] * (1.0 * d["r"]) ** 2 for d in dados)
        self.reg("soma", soma_pedacos=soma, meio_I_w2=0.5 * (0.5 * 1.0 * R1 ** 2) * 1.0, M=1.0, R=R1, w=1.0, n=len(dados))
        self.ate(0.99)
        # ── T1-2 ──
        self.an("T1-2")
        lE = VGroup(txt("ENERGIA DO PEDAÇO", 24, color=KC), T(r"\tfrac{1}{2}m_iv_i^2", 40)).arrange(DOWN, buff=0.1)
        lE.move_to(P3(-1.0 - lE.width / 2, 2.55))      # v6 S2: acima do disco, fora da borda
        B, ib = M(r"K_i", "=", r"\tfrac{1}{2}", "m_i", "v_i^2", size=52)
        self.pilha.poe(B)
        self.gat("a energia cinética desse pedaço")
        self.play(FadeIn(lE, shift=0.1 * DOWN), run_time=0.6)
        self.monta(B, ib, {3: lm, 4: lv})
        C_, ic = M("=", r"\tfrac{1}{2}", "m_i", r"(\omega r_i)^2", size=52)
        self.pilha.poe(C_)
        self.gat("troca v i por velocidade angular")
        self.passo(B, C_, (J(ib, 1), J(ic, 0)), (J(ib, 2), J(ic, 1)), (J(ib, 3), J(ic, 2)), rt=1.2, origem=False)
        D_, id_ = M("=", r"\tfrac{1}{2}", "m_i", "r_i^2", r"\omega^2", size=52)
        self.pilha.poe(D_)
        self.gat("fica meio m i r i ao quadrado")
        ic3 = ic[3]                                                         # (ωr_i)^2: ( ω r i ) 2
        self.passo(C_, D_, (J(ic, 0), J(id_, 0)), (J(ic, 1), J(id_, 1)), (J(ic, 2), J(id_, 2)),
                   ([ic3[2]], J(id_, 3)[:1]), ([ic3[1]], J(id_, 4)[:1]), rt=1.4, origem=False)
        self.gat("repara de onde veio o r i ao quadrado")
        self.play(self.ind(D_, id_, [3], MAS, 1.15, 0.9), run_time=0.9)
        self.foco = D_
        self.ate(0.99)
        # ── T1-3 ──
        self.an("T1-3")
        for m in (lm, lr, lv, lin, ext):
            m.clear_updaters()
        self.play(FadeOut(lE), FadeOut(lm), FadeOut(lr), FadeOut(lv), FadeOut(lin), FadeOut(ext), realce.animate.set_value(0.0), run_time=0.4)
        self.remove(lm, lr, lv, lin, ext)
        self.play(gira.animate.set_value(1.0), run_time=1.0)            # o disco volta a girar: a soma vale para todos os pedaços
        E_, ie = M("K", "=", r"\sum", r"\tfrac{1}{2}", "m_i", "r_i^2", r"\omega^2", size=52)
        self.pilha.poe(E_)
        self.gat("soma a de todos os pedaços")
        self.passo(D_, E_, (J(id_, 1), J(ie, 3)), (J(id_, 2), J(ie, 4)), (J(id_, 3), J(ie, 5)), (J(id_, 4), J(ie, 6)), rt=1.2, origem=False)
        # barra: a energia de cada anel (ciano) empilha numa barra única
        XB, YB0, HT = -0.85, -3.0, 3.6
        aneis_E = []
        for i in range(NR):
            ks = [k for k in range(len(dados)) if i * NT <= k < (i + 1) * NT]
            aneis_E.append(sum(0.5 * dados[k]["m"] * dados[k]["r"] ** 2 for k in ks))
        tot = sum(aneis_E)
        segs, y = VGroup(), YB0
        for i, e in enumerate(aneis_E):
            h = HT * e / tot
            segs.add(Rectangle(width=0.4, height=h).move_to(P3(XB, y + h / 2)).set_fill(interpolate_color(ManimColor(escuro(KC, 0.45)), ManimColor(KC), i / (NR - 1)), 0.95)
                     .set_stroke(KC, 1.5).set_z_index(10))
            y += h
        lK = T("K", 44).next_to(segs, UP, buff=0.14)
        self.gat("a velocidade angular é a mesma para todos")
        F_, if_ = M("=", r"\tfrac{1}{2}", r"\Big(", r"\sum", "m_i", "r_i^2", r"\Big)", r"\omega^2", size=52)
        self.pilha.poe(F_)
        self.passo(E_, F_, (J(ie, 1), J(if_, 0)), (J(ie, 3), J(if_, 1)), (J(ie, 2), J(if_, 3)), (J(ie, 4), J(if_, 4)), (J(ie, 5), J(if_, 5)),
                   (J(ie, 6), J(if_, 7)), rt=1.6, origem=False)
        self.selo("DESTAQUE", [[MathTex(r"\omega", font_size=38, color=VEL), "É IGUAL EM TODOS"]])
        self.play(LaggedStart(*[GrowFromEdge(s_, DOWN) for s_ in segs], lag_ratio=0.5), FadeIn(lK), run_time=1.6)
        self.reg("barra_t1", aneis=aneis_E, total=tot, h=HT)
        self.gat("sobra dentro do parêntese")
        self.play(self.ind(F_, if_, [2, 3, 4, 5, 6], MAS, 1.12, 1.0), run_time=1.0)
        par = SurroundingRectangle(mp(F_, if_, [2, 3, 4, 5, 6]), buff=0.08, corner_radius=0.08).set_stroke(MAS, 3)
        self.gat("não depende de quão rápido")
        self.play(Create(par), run_time=0.7)
        self.foco = F_
        self.ate(0.99)
        # ── T1-4 ──
        self.an("T1-4")
        self.sem_selo()
        G_, ig = M("I", "=", r"\sum", "m_i", "r_i^2", size=54)
        self.pilha.so(F_, anims=[FadeOut(par)])
        self.pilha.poe(G_)
        self.gat("e esse parêntese ganha nome")
        self.voa([(mp(F_, if_, [3, 4, 5]), mp(G_, ig, [2, 3, 4]))], extra=[FadeIn(mp(G_, ig, [0, 1]))], rt=1.0, origem=False)
        un = linha_m(T(r"[\,\mathrm{kg\cdot m^2}\,]", 40, MAS), buff=0.1)
        self.pilha.poe(un, dx=0.6)
        self.gat("a unidade é quilograma")
        self.play(FadeIn(un), run_time=0.5)
        H_, ih = M("K", "=", r"\tfrac{1}{2}", "I", r"\omega^2", size=58)
        Hb = caixa_l(H_, KC)
        self.pilha.poe(Hb)
        self.gat("a energia cinética de rotação fica")
        self.cx(Hb[0])
        self.voa([(mp(G_, ig, [0]), mp(H_, ih, [3])), (mp(F_, if_, [7]), mp(H_, ih, [4]))], extra=[FadeIn(mp(H_, ih, [0, 1, 2]))], rt=1.0, origem=False)
        self.pilha.so(Hb)
        def ph_():
            return [Dot(P3(-0.1, 0), radius=0.001).set_opacity(0), Dot(P3(5.9, 0), radius=0.001).set_opacity(0)]

        def linha_t(l_, r_):                                                    # v6 §5: grade de 3 colunas (TRANSLAÇÃO | ↔ | ROTAÇÃO) alinhadas entre as linhas
            Lm, Am, Rm = T(l_, 48), T(r"\leftrightarrow", 44), T(r_, 48)
            Lm.move_to(P3(1.1, 0))
            Am.move_to(P3(2.9, 0))
            Rm.move_to(P3(4.7, 0))
            return VGroup(Lm, Am, Rm, *ph_()), Lm, Am, Rm
        cab = VGroup(txt("TRANSLAÇÃO", 26, bold=True).move_to(P3(1.1, 0)), txt("ROTAÇÃO", 26, bold=True).move_to(P3(4.7, 0)), *ph_())
        self.pilha.poe(cab, dx=0.3)
        self.gat("olha a tradução")
        self.play(FadeIn(cab), run_time=0.4)
        fontes = (mp(H_, ih, [3]), mp(H_, ih, [4])[:1], mp(H_, ih, [2, 3, 4]))                 # I, ω e ½Iω² saem da própria conta da energia
        for (l_, r_), fr, src in zip((("m", "I"), ("v", r"\omega"), (r"\tfrac{1}{2}mv^2", r"\tfrac{1}{2}I\omega^2")), ("a massa da translação", "a velocidade vira", "mesma forma"), fontes):
            row, Lm, Am, Rm = linha_t(l_, r_)
            self.pilha.poe(row, dx=0.3)
            self.gat(fr)
            self.voa([(src, Rm)], extra=[FadeIn(Lm), FadeIn(Am)], rt=1.0, origem=False)
        self.foco = Hb
        self.ate(0.99)
        # ── T1-5: vista oblíqua: pedaço fora do plano ──
        self.an("T1-5")
        dv.clear_updaters()
        ang.clear_updaters()
        velhos = [dv, aw, lw, segs, lK]
        self.pilha.so(Hb)
        CO = P3(-3.7, -1.9)
        ell = Ellipse(width=4.6, height=1.3).move_to(CO)
        aco(ell, 2.0)
        ell.set_z_index(4)
        pec_ob = VGroup(*[Ellipse(width=4.6 * f, height=1.3 * f).move_to(CO).set_stroke(MAS, 2, opacity=0.6) for f in (0.25, 0.5, 0.75)]).set_z_index(5)
        eixo_v = Line(CO + 1.1 * DOWN, CO + 4.4 * UP).set_stroke(GEO, 3).set_z_index(6)
        lz = txt("EIXO", 24, color=GEO).next_to(eixo_v.get_end(), RIGHT, buff=0.12)
        Pp = CO + P3(1.55, 3.2)                       # pedaço fora do plano, longe do eixo
        pino = DashedLine(CO + P3(1.55, -0.18), Pp, dash_length=0.08).set_stroke(GEO, 2, opacity=0.6).set_z_index(5)
        ped = Dot(Pp, radius=0.15, color=MAS).set_z_index(9)
        rperp = DashedLine(CO + P3(0, 3.2), Pp, dash_length=0.09).set_stroke(GEO, 3.4).set_z_index(8)
        rvec = Arrow(CO, Pp, buff=0.05, stroke_width=4, max_tip_length_to_length_ratio=0.08).set_color(VETC).set_z_index(7)
        lperp = T(r"r_\perp", 42).next_to(rperp, UP, buff=0.14)
        lvec = T(r"\vec r", 42, VETC).next_to(rvec.point_from_proportion(0.55), RIGHT, buff=0.18)
        self.troca(velhos, FadeIn(ell), FadeIn(pec_ob), FadeIn(eixo_v), FadeIn(lz), seq=True)
        nn = linha_m(txt("NÃO É ENERGIA NOVA:", 26, bold=True), T(r"\sum \tfrac{1}{2}m_iv_i^2", 40), buff=0.2)
        self.pilha.poe(nn)
        self.gat("isso não é uma energia nova")
        self.play(FadeIn(nn), run_time=0.6)
        self.gat("o r i que entra na conta")
        self.selo("ATENÇÃO", ["A DISTÂNCIA É AO EIXO"])
        self.play(FadeIn(pino), FadeIn(ped), run_time=0.6)
        self.play(GrowArrow(rvec), FadeIn(lvec), run_time=0.7)
        self.gat("e não a distância até a origem")
        self.play(Create(rperp), FadeIn(lperp), self.ind_copia(rvec, APAGADO, 1.0, 0.6), run_time=0.8)
        Ii, ii = M(r"I", "=", r"\sum", "m_i", r"r_{\perp,i}^2", size=50)
        self.pilha.poe(Ii)
        self.voa([(lperp, mp(Ii, ii, [4]))], extra=[FadeIn(mp(Ii, ii, [0, 1, 2, 3]))], rt=0.9, origem=False)
        P2 = CO + P3(0, 3.6)
        ped2 = Dot(P2, radius=0.15, color=MAS).set_z_index(9)
        l0 = T(r"r_\perp=0", 40).next_to(ped2, LEFT, buff=0.2)
        self.gat("se o pedaço está lá em cima")
        self.play(FadeIn(ped2, scale=0.5), run_time=0.5)
        self.gat("ele não contribui com nada")
        self.play(FadeIn(l0), run_time=0.5)
        self.foco = l0
        self.ate(0.99)
